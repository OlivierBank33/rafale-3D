"""Compositing des frames Blender (cut/f_XXXX.png) + titres + audio sinus -> 2026-10-08_rafale-coupes.mp4"""
import math, subprocess, sys, json
import numpy as np, soundfile as sf
import cairo
sys.argv = [sys.argv[0]]
LEVELS = [(1, 0.0, 9.0), (2, 9.0, 9.0), (3, 18.0, 9.5), (5, 27.5, 10.0), (7, 37.5, 10.5), (12, 48.0, 12.0)]
PIECES = [2, 3, 4, 4, 12, 27]
KNIFE_T, GAP, FPS, TOTAL = 1.2, 0.32, 30, 64.0
W, H = 1080, 1920
YEL = (1.0, 0.84, 0.1)


def ease_out(u):
    u = min(max(u, 0), 1); return 1 - (1 - u) ** 3


def font(c, size):
    c.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(size)


def text_c(c, txt, x, y, size, rgba=(1, 1, 1, 1), stroke=0):
    font(c, size); e = c.text_extents(txt); c.move_to(x - e.x_advance / 2, y); c.text_path(txt)
    if stroke:
        c.set_source_rgba(0, 0, 0, 0.6 * rgba[3]); c.set_line_width(stroke); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
    c.set_source_rgba(*rgba); c.fill(); c.new_path()


def bg_surface():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    g = cairo.RadialGradient(W / 2, 900, 100, W / 2, 900, 1300)
    g.add_color_stop_rgb(0, 0.47, 0.48, 0.51); g.add_color_stop_rgb(1, 0.24, 0.25, 0.27); c.set_source(g); c.paint()
    return s


BG = bg_surface()


def level_at(t):
    return max(i for i, l in enumerate(LEVELS) if l[1] <= t)


def frame(fi):
    t = fi / FPS; li = level_at(t); n, t0, dur = LEVELS[li]; lt = t - t0
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    c.set_source_surface(BG, 0, 0); c.paint()
    r = cairo.ImageSurface.create_from_png(f'cut/f_{fi:04d}.png')
    c.save(); c.scale(W / r.get_width(), W / r.get_width()); c.set_source_surface(r, 0, 0)
    c.get_source().set_filter(cairo.FILTER_BEST); c.paint(); c.restore()
    t_burst = KNIFE_T + GAP * (n - 1) + 0.25
    # titre
    if li == 0 and lt < KNIFE_T:
        a = ease_out(lt / 0.3)
        text_c(c, "1 COUPE", W / 2, 300, 120, (1, 1, 1, a), stroke=10)
        text_c(c, "VS", W / 2, 420, 90, (1, 1, 1, a), stroke=8)
        text_c(c, "UN RAFALE", W / 2, 520, 70, (*YEL, a), stroke=8)
    else:
        k = 1 + 0.3 * max(0, 1 - lt / 0.2)
        lab = f"{n} COUPE" + ("S" if n > 1 else "")
        c.save(); c.translate(W / 2, 330); c.scale(k, k); text_c(c, lab, 0, 0, 130, (1, 1, 1, 1), stroke=10); c.restore()
        # compteur de coupes pendant le passage du couteau
        done = sum(1 for kk in range(n) if lt >= KNIFE_T + GAP * kk)
        if lt < t_burst and n > 1:
            text_c(c, f"{done} / {n}", W / 2, 430, 56, (1, 1, 1, 0.8), stroke=6)
        if lt >= t_burst + 0.6 and PIECES[li] > n:
            a = ease_out((lt - t_burst - 0.6) / 0.3)
            text_c(c, f"= {PIECES[li]} MORCEAUX", W / 2, 440, 64, (*YEL, a), stroke=8)
    # éclair blanc au moment de l'éclatement
    if 0 <= lt - t_burst < 0.12:
        c.set_source_rgba(1, 1, 1, 0.35 * (1 - (lt - t_burst) / 0.12)); c.paint()
    # fin
    if t > 60.0:
        a = ease_out((t - 60.0) / 0.4)
        c.set_source_rgba(0.03, 0.03, 0.05, 0.75 * a); c.paint()
        text_c(c, "Et toi, tu le découpes", W / 2, 820, 70, (1, 1, 1, a), stroke=8)
        text_c(c, "en combien de morceaux ?", W / 2, 910, 70, (1, 1, 1, a), stroke=8)
        text_c(c, "ABONNE-TOI POUR LA SUITE", W / 2, 1060, 52, (*YEL, a), stroke=7)
    c.set_source_rgba(*YEL, 1); c.rectangle(0, 0, W * t / TOTAL, 8); c.fill()
    return s


def audio():
    SR = 48000; N = int(TOTAL * SR); t = np.arange(N) / SR; mix = np.zeros(N)
    def env(n, a=0.002, r=0.2):
        e = np.ones(n); na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na); return e * np.exp(-np.arange(n) / (r * SR))
    def add(at, sig, g=1.0):
        i = int(at * SR)
        if i < 0 or i >= N: return
        j = min(N, i + len(sig)); mix[i:j] += g * sig[:j - i]
    def sweep(f0, f1, d):
        n = int(d * SR); f = np.linspace(f0, f1, n); return np.sin(2 * np.pi * np.cumsum(f) / SR)
    pad = sum(np.sin(2 * np.pi * f * t) for f in (110, 138.6, 164.8)) * 0.04
    mix += pad
    bt = 0.0
    while bt < TOTAL - 4:
        add(bt, sweep(80, 45, 0.2) * env(int(0.2 * SR), 0.002, 0.06), 0.35); bt += 0.5
    for (n, t0, dur) in LEVELS:
        for k in range(n):
            tk = t0 + KNIFE_T + GAP * k
            add(tk - 0.1, sweep(1800, 4200, 0.18) * env(int(0.18 * SR), 0.003, 0.06), 0.35)          # « shing »
            m = int(0.6 * SR); x = np.arange(m) / SR
            add(tk, (np.sin(2 * np.pi * 2350 * x) + 0.5 * np.sin(2 * np.pi * 3520 * x)) * env(m, 0.001, 0.15), 0.12)
        tb = t0 + KNIFE_T + GAP * (n - 1) + 0.25
        add(tb, sweep(150, 40, 0.6) * env(int(0.6 * SR), 0.001, 0.2), 1.0)
        for kk, f in enumerate((523.3, 659.3, 784.0)):
            m = int(0.9 * SR); add(tb + 0.6 + kk * 0.08, np.sin(2 * np.pi * f * np.arange(m) / SR) * env(m, 0.003, 0.3), 0.18)
    for kk, f in enumerate((523.3, 659.3, 784.0, 1046.5)):
        m = int(1.6 * SR); add(60.0 + kk * 0.12, np.sin(2 * np.pi * f * np.arange(m) / SR) * env(m, 0.003, 0.5), 0.25)
    mix *= np.clip(t / 0.3, 0, 1) * np.clip((TOTAL - t) / 1.0, 0, 1)
    sf.write('cut/mix.wav', (mix / np.abs(mix).max() * 0.9).astype(np.float32), SR)


if __name__ == '__main__':
    audio()
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-i', 'pipe/brand/filigrane_video.png', '-i', 'cut/mix.wav',
                           '-filter_complex', '[1]scale=280:-1,format=rgba,colorchannelmixer=aa=0.8[w];[0][w]overlay=36:36[v];[2:a]aresample=48000,loudnorm=I=-15:TP=-1.5[a]',
                           '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
                           '-shortest', '-movflags', '+faststart', '2026-10-08_rafale-coupes.mp4'], stdin=subprocess.PIPE)
    for fi in range(int(TOTAL * FPS)):
        ff.stdin.write(bytes(frame(fi).get_data()))
    ff.stdin.close(); ff.wait(); print('done')
