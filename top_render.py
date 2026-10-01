import cairo, json, math, subprocess, sys, re, random
import numpy as np
from PIL import Image, ImageFilter
from top_script import *

W, H, FPS = 1080, 1920, 30
D = json.load(open('top/durs.json'))
YEL = (1.0, 0.84, 0.1); GRN = (0.25, 0.9, 0.45); RED = (1.0, 0.28, 0.3); CYA = (0.35, 0.85, 1.0); GOLD = (1.0, 0.78, 0.2)
N = len(TOP)

# ---------- Timeline ----------
SEG = []
t = 0.3
SEG.append(dict(k='intro', t0=0.0, vt=t, end=t + D['intro'] + 0.5)); t = SEG[-1]['end']
for i in range(N):
    pre = 0.9 if i == N - 1 else 0.45
    SEG.append(dict(k=f't{i}', i=i, t0=t, vt=t + pre, end=t + pre + D[f't{i}'] + (1.2 if i == N - 1 else 0.6)))
    t = SEG[-1]['end']
SEG.append(dict(k='outro', t0=t, vt=t + 0.4, end=t + 0.4 + D['outro'] + 2.4)); t = SEG[-1]['end']
TOTAL = t
json.dump(dict(seg=SEG, total=TOTAL), open('top/timeline.json', 'w'))


def ease(u):
    u = min(max(u, 0), 1); return u * u * (3 - 2 * u)


def ease_out(u):
    u = min(max(u, 0), 1); return 1 - (1 - u) ** 3


def back_out(u):
    u = min(max(u, 0), 1); c = 1.70158
    return 1 + (c + 1) * (u - 1) ** 3 + c * (u - 1) ** 2


def to_surface(img):
    a = np.array(img.convert('RGBA')).astype(np.float32)
    al = a[..., 3:4] / 255.0; rgb = a[..., :3] * al
    bgra = np.dstack([rgb[..., 2], rgb[..., 1], rgb[..., 0], a[..., 3]]).astype(np.uint8)
    h, w = bgra.shape[:2]
    stride = cairo.ImageSurface.format_stride_for_width(cairo.FORMAT_ARGB32, w)
    buf = np.zeros((h, stride // 4, 4), np.uint8); buf[:, :w] = bgra
    return cairo.ImageSurface.create_for_data(bytearray(buf.tobytes()), cairo.FORMAT_ARGB32, w, h, stride)


def prep(key, bw, bh, pad=40):
    im = Image.open(f"r3d/{key}.png").convert('RGBA'); im = im.crop(im.getbbox())
    sc = min(bw / im.width, bh / im.height)
    im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
    big = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0)); big.alpha_composite(im, (pad, pad))
    al = big.split()[3]
    sil = Image.new('RGBA', big.size, (6, 10, 22, 255)); sil.putalpha(al)
    glow = Image.new('RGBA', big.size, (255, 200, 80, 255))
    glow.putalpha(al.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.8)))
    return dict(c=to_surface(big), s=to_surface(sil), g=to_surface(glow), w=big.width, h=big.height)


IM = [prep(x['img'], 940, 480) for x in TOP]
THUMB = [prep(x['img'], 150, 70, pad=4) for x in TOP]


def font(c, size):
    c.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(size)


def text_c(c, txt, x, y, size, rgba=(1, 1, 1, 1), stroke=0, maxw=None):
    font(c, size); e = c.text_extents(txt)
    if maxw and e.x_advance > maxw:
        size *= maxw / e.x_advance; font(c, size); e = c.text_extents(txt)
    c.move_to(x - e.x_advance / 2, y); c.text_path(txt)
    if stroke:
        c.set_source_rgba(0, 0, 0, 0.85 * rgba[3]); c.set_line_width(stroke); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
    c.set_source_rgba(*rgba); c.fill(); c.new_path()


def rrect(c, x, y, w, h, r):
    c.new_path()
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2); c.close_path()


def img(c, im, key, cx, cy, s=1.0, a=1.0):
    if a <= 0 or abs(s) < 0.02: return
    c.save(); c.translate(cx, cy); c.scale(s, s); c.translate(-im['w'] / 2, -im['h'] / 2)
    c.set_source_surface(im[key], 0, 0); c.paint_with_alpha(min(1, a)); c.restore()


def background(c, t, heat=0.0, burst=0.0):
    g = cairo.RadialGradient(W / 2, 780, 60, W / 2, 780, 1300)
    g.add_color_stop_rgb(0, 0.08 + 0.25 * heat, 0.13 + 0.03 * heat, 0.3 - 0.18 * heat); g.add_color_stop_rgb(1, 0.01, 0.015, 0.04)
    c.set_source(g); c.paint()
    # lignes de vitesse horizontales
    random.seed(1)
    spd = 600 + 2600 * heat
    for j in range(26):
        y = random.uniform(300, 1450); L = random.uniform(80, 380); ph = random.uniform(0, W + 600)
        x = W + 300 - ((ph + t * spd) % (W + 600))
        c.set_source_rgba(1, 1, 1, 0.05 + 0.08 * heat); c.set_line_width(random.uniform(1.5, 4))
        c.move_to(x, y); c.line_to(x + L, y); c.stroke()
    if burst > 0:
        c.set_source_rgba(1, 1, 1, 0.5 * burst); c.paint()


# ---------- Sous-titres karaoké ----------
def build_caps():
    caps = []
    texts = {'intro': INTRO['show'], 'outro': OUTRO['show']}
    for i, x in enumerate(TOP): texts[f't{i}'] = x['show']
    for s in SEG:
        words = texts[s['k']].replace('3 529', '3 529').replace('1 000', '1 000').replace('1 180', '1 180').split(' ')
        def wt(w_):
            n = len(re.sub(r'[^\w]', '', w_)) + 3 * sum(ch.isdigit() for ch in w_)
            if w_.endswith(('.', '!', '?', ':')): n += 6
            if '...' in w_: n += 8
            if w_.endswith(','): n += 3
            return max(n, 2) + 2
        ws = [wt(w_) for w_ in words]; tot = sum(ws); t0 = s['vt']; dur = D[s['k']]
        times = []; acc = 0
        for w_ in ws:
            times.append((t0 + dur * acc / tot, t0 + dur * (acc + w_) / tot)); acc += w_
        grp = []
        for j, w_ in enumerate(words):
            grp.append(j)
            if len(grp) == 3 or w_.endswith(('.', '!', '?', ':', ',')) or j == len(words) - 1 or (len(grp) == 2 and len(''.join(words[q] for q in grp)) > 14):
                caps.append(dict(words=[words[q] for q in grp], times=[times[q] for q in grp], t0=times[grp[0]][0], t1=times[grp[-1]][1])); grp = []
    return caps


CAPS = build_caps()


def captions(c, t):
    cap = None
    for cp in CAPS:
        if cp['t0'] - 0.02 <= t < cp['t1'] + 0.05: cap = cp
    if not cap: return
    size = 70; font(c, size)
    words = [w_ if w_.rstrip('.,!?') in ('km/h',) else w_.upper() for w_ in cap['words']]
    sp = c.text_extents(' ').x_advance; widths = [c.text_extents(w_).x_advance for w_ in words]
    total = sum(widths) + sp * (len(words) - 1)
    if total > 860:
        size *= 860 / total; font(c, size); widths = [c.text_extents(w_).x_advance for w_ in words]; sp = c.text_extents(' ').x_advance
        total = sum(widths) + sp * (len(words) - 1)
    pop = back_out((t - cap['t0']) / 0.15); y = 1560
    c.save(); c.translate(W / 2, y); c.scale(0.85 + 0.15 * pop, 0.85 + 0.15 * pop); c.translate(-W / 2, -y)
    x = W / 2 - total / 2
    for w_, wd, (a, b) in zip(words, widths, cap['times']):
        c.move_to(x, y); c.text_path(w_)
        c.set_source_rgba(0, 0, 0, 0.9); c.set_line_width(13); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
        c.set_source_rgb(*(YEL if a <= t < b + 0.05 else (1, 1, 1))); c.fill(); c.new_path()
        x += wd + sp
    c.restore()


def header(c, done):
    font(c, 30); lab = "LES PLUS RAPIDES"
    e = c.text_extents(lab); bw = e.x_advance + 50
    rrect(c, W / 2 - bw / 2, 60, bw, 56, 28); c.set_source_rgba(*YEL, 1); c.fill()
    c.set_source_rgb(0.03, 0.05, 0.1); c.move_to(W / 2 - e.x_advance / 2, 99); c.show_text(lab)
    dw = 80; x0 = W / 2 - dw * N / 2
    for j in range(N):
        cx = x0 + dw * (j + 0.5)
        rrect(c, cx - 30, 140, 60, 12, 6)
        c.set_source_rgba(*(GOLD if j < done else (1, 1, 1)), 1 if j < done else 0.2); c.fill()


def speed_bar(c, t, s, x):
    lt = t - s['vt']
    u = ease_out(lt / 1.6)
    v = x['kmh'] * u
    # compteur
    shown = x['lab'] if u >= 0.999 else f"{v:,.0f} km/h".replace(',', ' ')
    col = GOLD if x['rank'] == 1 else (CYA if x['kmh'] < 1225 else YEL)
    text_c(c, shown, W / 2, 1265, 104, (*col, 1), stroke=10)
    # barre
    X0, BW, Y = 90, 900, 1305
    rrect(c, X0, Y, BW, 40, 20); c.set_source_rgba(1, 1, 1, 0.12); c.fill()
    fw = max(40, BW * v / VMAX)
    rrect(c, X0, Y, fw, 40, 20)
    g = cairo.LinearGradient(X0, 0, X0 + BW, 0)
    g.add_color_stop_rgb(0, *CYA); g.add_color_stop_rgb(0.35, *YEL); g.add_color_stop_rgb(1, *RED)
    c.set_source(g); c.fill()
    # mur du son
    mx = X0 + BW * 1225 / VMAX
    c.set_source_rgba(1, 1, 1, 0.85); c.set_line_width(3); c.move_to(mx, Y - 14); c.line_to(mx, Y + 54); c.stroke()
    font(c, 24); lab = "MUR DU SON"; e = c.text_extents(lab)
    c.move_to(mx - e.x_advance / 2, Y + 82); c.show_text(lab)
    if x['kmh'] > 1225 and v > 1225:
        k = (v - 1225) / 300
        if k < 1:
            c.set_source_rgba(1, 1, 1, 0.5 * (1 - k)); c.set_line_width(6 + 30 * k)
            c.arc(mx, Y + 20, 20 + 120 * k, 0, 2 * math.pi); c.stroke()


def entry(c, t, s):
    i = s['i']; x = TOP[i]; lt = t - s['t0']; im = IM[i]
    final = x['rank'] == 1
    heat = x['kmh'] / VMAX
    rev = s['vt'] if not final else s['vt'] + 1.6
    burst = max(0, 1 - (t - rev) / 0.35) if (final and t >= rev) else 0
    background(c, t, heat=heat, burst=burst * 0.8)
    header(c, i if t < s['vt'] else i + 1)
    # grand numéro en fond
    a = back_out(lt / 0.35)
    font(c, 420); num = f"#{x['rank']}"; e = c.text_extents(num)
    c.set_source_rgba(1, 1, 1, 0.07); c.move_to(W / 2 - e.x_advance / 2, 950); c.show_text(num)
    text_c(c, f"N°{x['rank']}", W / 2, 270, 90 * a, (*(GOLD if final else YEL), 1), stroke=10)
    # avion
    enter = ease_out(lt / 0.55)
    cx = W / 2 + (1 - enter) * (W * 1.1); cy = 690 + 8 * math.sin(t * 2.4)
    shake = (3 + 6 * heat) * math.sin(t * 60) if lt < 0.9 else 0
    if final and t < rev:
        img(c, im, 's', cx + shake, cy, 1.0)
        text_c(c, "?", W / 2, cy + 60, 220, (*GOLD, 1), stroke=10)
    else:
        if final: img(c, im, 'g', cx, cy, 1.05, 1.0)
        img(c, im, 'c', cx + shake, cy, 1.0 + (0.06 * math.sin(min(1, (t - rev) / 0.35) * math.pi) if final else 0))
    if t >= rev:
        u = back_out((t - rev) / 0.35)
        text_c(c, x['name'], W / 2, 1100, 84 * (0.6 + 0.4 * u), (1, 1, 1, 1), stroke=10, maxw=1000)
        speed_bar(c, t, s, x)
    if s['end'] - t < 0.15:
        c.set_source_rgba(0.01, 0.015, 0.04, 1 - (s['end'] - t) / 0.15); c.paint()
    if lt < 0.1:
        c.set_source_rgba(0.01, 0.015, 0.04, 1 - lt / 0.1); c.paint()


def intro(c, t, s):
    lt = t - s['t0']
    background(c, t, heat=0.6)
    header(c, 0)
    a = back_out(lt / 0.45)
    text_c(c, "LES 8 AVIONS", W / 2, 300, 96 * a, (1, 1, 1, 1), stroke=10)
    text_c(c, "LES PLUS RAPIDES", W / 2, 410, 96 * a, (*YEL, 1), stroke=10, maxw=1000)
    im = IM[-1]
    img(c, im, 's', W / 2, 820 + 8 * math.sin(t * 2), 1.0, min(1, lt / 0.4))
    b = back_out((lt - 1.2) / 0.4)
    if b > 0:
        text_c(c, "N°1 = ?", W / 2, 880, 150 * b, (*GOLD, 1), stroke=10)
    if s['end'] - t < 0.15:
        c.set_source_rgba(0.01, 0.015, 0.04, 1 - (s['end'] - t) / 0.15); c.paint()


def outro(c, t, s):
    lt = t - s['t0']
    background(c, t, heat=0.3)
    header(c, N)
    a = back_out(lt / 0.4)
    text_c(c, "LE CLASSEMENT", W / 2, 260, 86 * a, (*YEL, 1), stroke=10)
    for j in range(N):
        x = TOP[N - 1 - j]
        u = back_out((lt - 0.15 - 0.09 * j) / 0.3)
        if u < 0.03: continue
        y = 330 + j * 132
        c.save(); c.translate(W / 2, y + 55); c.scale(u, u); c.translate(-W / 2, -(y + 55))
        rrect(c, 70, y, 940, 110, 22); c.set_source_rgba(0.05, 0.09, 0.18, 0.92); c.fill_preserve()
        c.set_source_rgba(*(GOLD if j == 0 else (1, 1, 1)), 0.9 if j == 0 else 0.25); c.set_line_width(4 if j == 0 else 2); c.stroke()
        font(c, 50); c.set_source_rgba(*(GOLD if j == 0 else YEL), 1); c.move_to(100, y + 73); c.show_text(f"{x['rank']}")
        img(c, THUMB[N - 1 - j], 'c', 245, y + 55, 1.0)
        font(c, 38); c.set_source_rgb(1, 1, 1); c.move_to(340, y + 68); c.show_text(x['name'])
        font(c, 34); e = c.text_extents(x['lab']); c.set_source_rgba(*CYA, 1); c.move_to(985 - e.x_advance, y + 68); c.show_text(x['lab'])
        c.restore()


def render(t, surf):
    c = cairo.Context(surf)
    s = SEG[0]
    for x in SEG:
        if t >= x['t0']: s = x
    if s['k'] == 'intro': intro(c, t, s)
    elif s['k'] == 'outro': outro(c, t, s)
    else: entry(c, t, s)
    captions(c, t)
    if t < 0.2:
        c.set_source_rgba(0, 0, 0, 1 - t / 0.2); c.paint()
    if t > TOTAL - 0.4:
        c.set_source_rgba(0, 0, 0, (t - (TOTAL - 0.4)) / 0.4); c.paint()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        for tt in map(float, sys.argv[2:]):
            sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); render(tt, sf); sf.write_to_png(f'top/still_{tt:.1f}.png')
        print(round(TOTAL, 1), [(x['k'], round(x['t0'], 1)) for x in SEG]); sys.exit()
    nframes = int(TOTAL * FPS)
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}',
                           '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '21',
                           '-pix_fmt', 'yuv420p', 'top/video_noaudio.mp4'], stdin=subprocess.PIPE)
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    for f in range(nframes):
        render(f / FPS, sf); sf.flush(); ff.stdin.write(bytes(sf.get_data()))
        if f % 300 == 0: print(f, '/', nframes, flush=True)
    ff.stdin.close(); ff.wait(); print('done', TOTAL)
