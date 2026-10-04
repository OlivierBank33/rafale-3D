"""Edit dynamique « France » (Rafale + Mirage 2000) calé sur 120 BPM, 65 s, sans son (son TikTok ajouté dans l'app)."""
import cairo, math, random, subprocess, sys, glob, os
import numpy as np

W, H, FPS = 1080, 1920, 30
BPM = 120.0; BEAT = 60 / BPM; TOTAL = 65.0
BLEU = (0.0, 0.33, 0.64); BLANC = (1, 1, 1); ROUGE = (0.94, 0.25, 0.21); GOLD = (1.0, 0.82, 0.25)
random.seed(4)


def load(p):
    return cairo.ImageSurface.create_from_png(p)


IMG = {os.path.basename(p)[:-4]: load(p) for p in sorted(glob.glob('fr/*.png'))}
for extra in ['r3d/rafale.png', 'r3d/m2000.png', 'r3d/mirage3.png', 'r3d/duel/r_side.png', 'r3d/duel/r_34.png', 'r3d/duel/r_front.png', 'r3d/duel/r_top.png']:
    if os.path.exists(extra): IMG[extra.replace('/', '_')[:-4]] = load(extra)
RAF = [k for k in IMG if k.startswith('raf_') or 'duel_r_' in k or k == 'r3d_rafale']
M2K = [k for k in IMG if k.startswith('m2k_') or k == 'r3d_m2000']
OTHER = [k for k in IMG if 'mirage3' in k]


def ease(u):
    u = min(max(u, 0), 1); return u * u * (3 - 2 * u)


def ease_out(u):
    u = min(max(u, 0), 1); return 1 - (1 - u) ** 3


def font(c, size, bold=True):
    c.select_font_face("Poppins", cairo.FONT_SLANT_ITALIC if bold else cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(size)


def text_c(c, txt, x, y, size, rgba=(1, 1, 1, 1), stroke=0, maxw=None):
    font(c, size); e = c.text_extents(txt)
    if maxw and e.x_advance > maxw:
        size *= maxw / e.x_advance; font(c, size); e = c.text_extents(txt)
    c.move_to(x - e.x_advance / 2, y); c.text_path(txt)
    if stroke:
        c.set_source_rgba(0, 0, 0, 0.8 * rgba[3]); c.set_line_width(stroke); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
    c.set_source_rgba(*rgba); c.fill(); c.new_path()


# ---------- découpage en plans (calé sur les temps) ----------
SECTIONS = [  # (début, fin, pas en temps, banque, ciel)
    (0.0, 4.0, 1, 'mix', 'dusk'),
    (4.0, 16.0, 2, 'm2k', 'day'),
    (16.0, 32.0, 1, 'raf', 'day'),
    (32.0, 40.0, 8, 'duo', 'dusk'),
    (40.0, 48.0, 0.5, 'mix', 'night'),
    (48.0, 56.0, 1, 'raf', 'day'),
    (56.0, 65.0, 99, 'end', 'dusk'),
]
SHOTS = []
cnt = {'raf': 0, 'm2k': 0, 'mix': 0}
for (a, b, step, bank, sky) in SECTIONS:
    t = a
    while t < b - 1e-6:
        d = min(step * BEAT, b - t)
        if bank == 'mix':
            pool = (RAF, M2K, OTHER)[cnt['mix'] % 3 if cnt['mix'] % 5 == 4 else cnt['mix'] % 2]; cnt['mix'] += 1
            key = pool[cnt['mix'] % len(pool)] if pool else RAF[0]
        elif bank in ('raf', 'm2k'):
            pool = RAF if bank == 'raf' else M2K
            key = pool[cnt[bank] % len(pool)]; cnt[bank] += 1
        else:
            key = bank
        SHOTS.append(dict(t0=t, t1=t + d, key=key, sky=sky, sec=(a, b), mode=random.choice(['push', 'pan', 'pull', 'tilt']),
                          dir=random.choice([-1, 1]), sc=random.uniform(1.0, 1.45)))
        t += d

# textes calés sur les temps
TEXTS = [
    (0.0, 1.0, "LA FRANCE", BLANC), (1.0, 2.0, "DANS LE CIEL", BLANC), (2.0, 4.0, "🇫🇷", None),
    (4.0, 6.0, "MIRAGE 2000", BLANC), (8.0, 10.0, "PREMIER VOL 1978", GOLD), (12.0, 14.0, "MACH 2,2", GOLD),
    (16.0, 18.0, "RAFALE", BLANC), (20.0, 22.0, "OMNIRÔLE", GOLD), (24.0, 26.0, "PORTE-AVIONS", BLANC), (28.0, 30.0, "NUCLÉAIRE", ROUGE),
    (32.0, 36.0, "LA LÉGENDE", BLANC), (36.0, 40.0, "ET SON HÉRITIER", GOLD),
    (48.0, 50.0, "MADE IN FRANCE", BLANC), (52.0, 54.0, "BLEU · BLANC · ROUGE", BLANC),
]


def sky(c, kind, t):
    g = cairo.LinearGradient(0, 0, 0, H)
    if kind == 'day':
        g.add_color_stop_rgb(0, 0.02, 0.12, 0.34); g.add_color_stop_rgb(0.6, 0.14, 0.36, 0.66); g.add_color_stop_rgb(1, 0.42, 0.62, 0.84)
    elif kind == 'dusk':
        g.add_color_stop_rgb(0, 0.06, 0.08, 0.22); g.add_color_stop_rgb(0.55, 0.62, 0.30, 0.30); g.add_color_stop_rgb(1, 1.0, 0.62, 0.30)
    else:
        g.add_color_stop_rgb(0, 0.01, 0.02, 0.06); g.add_color_stop_rgb(1, 0.06, 0.10, 0.22)
    c.set_source(g); c.paint()
    vg = cairo.RadialGradient(W / 2, H / 2, H * 0.25, W / 2, H / 2, H * 0.7); vg.add_color_stop_rgba(0, 0, 0, 0, 0); vg.add_color_stop_rgba(1, 0, 0, 0, 0.45)
    c.set_source(vg); c.paint()
    # nuages qui défilent
    rnd = random.Random(11)
    for k in range(14):
        y = rnd.uniform(200, 1800); sp = rnd.uniform(300, 900); s = rnd.uniform(120, 340)
        x = (rnd.uniform(0, W + 800) - t * sp) % (W + 800) - 400
        al = 0.10 if kind != 'night' else 0.04
        rg = cairo.RadialGradient(x, y, 0, x, y, s); rg.add_color_stop_rgba(0, 1, 1, 1, al); rg.add_color_stop_rgba(1, 1, 1, 1, 0)
        c.save(); c.translate(x, y); c.scale(2.2, 0.55); c.translate(-x, -y); c.set_source(rg); c.arc(x, y, s, 0, 2 * math.pi); c.fill(); c.restore()


def speed_lines(c, t, amount):
    if amount <= 0: return
    rnd = random.Random(int(t * 8))
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    for k in range(26):
        y = rnd.uniform(0, H); x = rnd.uniform(-200, W); L = rnd.uniform(150, 500)
        c.set_source_rgba(1, 1, 1, 0.18 * amount); c.set_line_width(rnd.uniform(2, 5))
        c.move_to(x, y); c.line_to(x + L, y); c.stroke()


def draw_plane(c, key, cx, cy, width, alpha=1.0, rot=0.0, blur=0.0, flip=False):
    sf = IMG[key]; sw = sf.get_width(); s = width / sw
    for k, a in ([(0, 1.0)] if blur <= 0 else [(-2, 0.18), (-1, 0.3), (0, 1.0)]):
        c.save(); c.translate(cx + k * blur * 40, cy); c.rotate(rot)
        if flip: c.scale(-1, 1)
        c.scale(s, s); c.set_source_surface(sf, -sw / 2, -sf.get_height() / 2); c.paint_with_alpha(alpha * a); c.restore()


def shot(c, sh, t):
    u = (t - sh['t0']) / (sh['t1'] - sh['t0'])
    lt = t - sh['t0']
    punch = 1 + 0.10 * (1 - ease_out(lt / 0.14))
    sky(c, sh['sky'], t)
    fast = (sh['t1'] - sh['t0']) <= BEAT + 1e-6
    speed_lines(c, t, 1.0 if fast else 0.4)
    if sh['key'] == 'duo':
        a = ease(u / 0.15)
        draw_plane(c, M2K[0], W / 2 - 40 + 60 * u, 640, 1150 * (1 + 0.05 * u), alpha=a)
        draw_plane(c, RAF[0], W / 2 + 40 - 60 * u, 1280, 1150 * (1 + 0.05 * u), alpha=ease((u - 0.45) / 0.12))
        return
    if sh['key'] == 'end':
        a = ease(u / 0.08)
        draw_plane(c, RAF[0], W / 2, 620 + 10 * math.sin(t * 2), 980, alpha=a)
        draw_plane(c, M2K[0], W / 2, 1330 + 10 * math.cos(t * 2), 980, alpha=ease((u - 0.06) / 0.08))
        text_c(c, "RAFALE", W / 2, 330, 120, (*BLANC, a), stroke=12)
        text_c(c, "OU", W / 2, 1000, 90, (*GOLD, ease((u - 0.1) / 0.06)), stroke=10)
        text_c(c, "MIRAGE 2000 ?", W / 2, 1650, 110, (*BLANC, ease((u - 0.14) / 0.06)), stroke=12, maxw=980)
        text_c(c, "DIS-LE EN COMMENTAIRE", W / 2, 1790, 46, (1, 1, 1, ease((u - 0.3) / 0.08)), stroke=6)
        return
    base = 1200 * sh['sc']; d = sh['dir']
    if sh['mode'] == 'push':
        w = base * (1 + 0.18 * u); x = W / 2 + d * 40 * u; y = H / 2
    elif sh['mode'] == 'pull':
        w = base * (1.2 - 0.18 * u); x = W / 2; y = H / 2 + 30 * u
    elif sh['mode'] == 'pan':
        w = base; x = W / 2 + d * (-180 + 360 * u); y = H / 2 - 40
    else:
        w = base * 1.05; x = W / 2; y = H / 2 + d * (-120 + 240 * u)
    rot = d * 0.04 * (u - 0.5) if sh['mode'] == 'tilt' else 0
    shake = (math.sin(t * 53) * 6, math.cos(t * 47) * 6) if fast else (0, 0)
    c.save(); c.translate(W / 2, H / 2); c.scale(punch, punch); c.translate(-W / 2, -H / 2)
    draw_plane(c, sh['key'], x + shake[0], y + shake[1], w, rot=rot, blur=1.0 if fast else 0.0)
    c.restore()


def tricolore(c, t, t_cut, dur=0.5):
    """volet bleu-blanc-rouge qui traverse l'écran."""
    u = (t - t_cut) / dur
    if not (0 <= u <= 1): return
    for k, col in enumerate((BLEU, BLANC, ROUGE)):
        x = -W * 1.2 + (W * 2.6) * ease(u) - k * 220
        c.save(); c.translate(x, 0); c.transform(cairo.Matrix(1, 0, -0.25, 1, 0, 0))
        c.rectangle(0, 0, 260, H * 1.2); c.set_source_rgb(*col); c.fill(); c.restore()


def render(t, surf):
    c = cairo.Context(surf)
    sh = SHOTS[0]
    for s in SHOTS:
        if t >= s['t0']: sh = s
    shot(c, sh, t)
    # flash sur chaque temps fort (refrains) et à chaque coupe
    lt = t - sh['t0']
    if lt < 0.08 and sh['t0'] > 0:
        c.set_source_rgba(1, 1, 1, 0.55 * (1 - lt / 0.08)); c.paint()
    beat = t / BEAT
    if 16 <= t < 32 or 40 <= t < 56:
        ph = beat - math.floor(beat)
        if int(beat) % 4 == 0 and ph < 0.12:
            c.set_source_rgba(1, 1, 1, 0.25 * (1 - ph / 0.12)); c.paint()
    # textes
    for (a, b, txt, col) in TEXTS:
        if a <= t < b:
            u = (t - a) / (b - a)
            if txt == "🇫🇷":
                ww = 520 * ease_out(u / 0.2); hh = ww * 0.66
                for k, cc in enumerate((BLEU, BLANC, ROUGE)):
                    c.rectangle(W / 2 - ww / 2 + k * ww / 3, H / 2 - hh / 2, ww / 3 + 1, hh); c.set_source_rgb(*cc); c.fill()
                continue
            sc = 1.6 - 0.6 * ease_out(u / 0.12)
            al = ease(u / 0.06) * (1 - ease((u - 0.88) / 0.12))
            c.save(); c.translate(W / 2, 1520); c.scale(sc, sc)
            text_c(c, txt, 0, 0, 108, (*col, al), stroke=14, maxw=980)
            c.restore()
    # volets tricolores aux changements de section
    for (a, b, *_ ) in SECTIONS[1:]:
        tricolore(c, t, a - 0.25)
    # barre de progression + fondu
    c.set_source_rgba(*BLEU, 1); c.rectangle(0, H - 8, W * t / TOTAL / 3, 8); c.fill()
    c.set_source_rgba(*BLANC, 1); c.rectangle(W / 3, H - 8, max(0, W * t / TOTAL - W / 3) if t / TOTAL > 1 / 3 else 0, 8); c.fill()
    if t < 0.1:
        c.set_source_rgba(0, 0, 0, 1 - t / 0.1); c.paint()


if __name__ == '__main__':
    os.makedirs('frv', exist_ok=True)
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        for tt in map(float, sys.argv[2:]):
            sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); render(tt, sf); sf.write_to_png(f'frv/still_{tt:.1f}.png')
        print(len(SHOTS), 'plans'); sys.exit()
    nf = int(TOTAL * FPS)
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', 'frv/video_noaudio.mp4'], stdin=subprocess.PIPE)
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    for f in range(nf):
        render(f / FPS, sf); sf.flush(); ff.stdin.write(bytes(sf.get_data()))
        if f % 300 == 0: print(f, '/', nf, flush=True)
    ff.stdin.close(); ff.wait(); print('done')
