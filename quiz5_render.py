import cairo, json, math, subprocess, sys
import numpy as np
from PIL import Image, ImageFilter
from quiz5_script import INTRO, OUTRO, Q

W, H, FPS = 1080, 1920, 30
D = json.load(open('qa5/durs.json'))
NQ = len(Q)
COUNT = 3.0

# ---------- Timeline ----------
T = {}
t = 0.3
T['intro'] = t; t += D['intro'] + 0.45
qs = []
for i in range(NQ):
    q0 = t
    cd0 = q0 + 0.5                       # début du compte à rebours
    rev = max(cd0 + COUNT, q0 + D[f'q{i}'] + 1.0)
    a0 = rev + 0.2
    end = a0 + D[f'a{i}'] + 0.55
    qs.append(dict(q0=q0, cd0=cd0, rev=rev, a0=a0, end=end))
    t = end
T['outro'] = t + 0.1
TOTAL = T['outro'] + D['outro'] + 2.2
json.dump(dict(T=T, qs=qs, total=TOTAL), open('qa5/timeline.json', 'w'))

YEL = (1.0, 0.84, 0.1); GRN = (0.2, 0.85, 0.4); RED = (1.0, 0.3, 0.3); CYA = (0.35, 0.85, 1.0)


def ease(u):
    u = min(max(u, 0), 1); return u * u * (3 - 2 * u)


def ease_out(u):
    u = min(max(u, 0), 1); return 1 - (1 - u) ** 3


def back_out(u):
    u = min(max(u, 0), 1); c = 1.70158
    return 1 + (c + 1) * (u - 1) ** 3 + c * (u - 1) ** 2


# ---------- Images ----------
def to_surface(img):
    a = np.array(img.convert('RGBA')).astype(np.float32)
    al = a[..., 3:4] / 255.0
    rgb = a[..., :3] * al
    bgra = np.dstack([rgb[..., 2], rgb[..., 1], rgb[..., 0], a[..., 3]]).astype(np.uint8)
    h, w = bgra.shape[:2]
    stride = cairo.ImageSurface.format_stride_for_width(cairo.FORMAT_ARGB32, w)
    buf = np.zeros((h, stride // 4, 4), np.uint8); buf[:, :w] = bgra
    s = cairo.ImageSurface.create_for_data(bytearray(buf.tobytes()), cairo.FORMAT_ARGB32, w, h, stride)
    return s


BOX_W, BOX_H = 1000, 640
IMGS = []
for q in Q:
    im = Image.open(f"r3d/{q['img']}.png").convert('RGBA')
    im = im.crop(im.getbbox())
    sc = min(BOX_W / im.width, BOX_H / im.height)
    im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
    pad = 40
    big = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0)); big.alpha_composite(im, (pad, pad))
    alpha = big.split()[3]
    # silhouette sombre + contour lumineux
    glow = alpha.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(9))
    sil = Image.new('RGBA', big.size, (0, 0, 0, 0))
    g = Image.new('RGBA', big.size, (90, 200, 255, 255)); g.putalpha(glow.point(lambda v: int(v * 0.95)))
    sil.alpha_composite(g)
    edge = alpha.filter(ImageFilter.MaxFilter(5))
    e = Image.new('RGBA', big.size, (200, 240, 255, 255)); e.putalpha(edge); sil.alpha_composite(e)
    core = Image.new('RGBA', big.size, (6, 10, 22, 255)); core.putalpha(alpha); sil.alpha_composite(core)
    # halo couleur pour la révélation
    rg = Image.new('RGBA', big.size, (255, 220, 120, 255)); rg.putalpha(alpha.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.7)))
    IMGS.append(dict(color=to_surface(big), sil=to_surface(sil), glow=to_surface(rg), w=big.width, h=big.height))


# ---------- Dessin ----------
def font(c, size, bold=True):
    c.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)


def text_c(c, txt, x, y, size, rgba=(1, 1, 1, 1), stroke=0, maxw=None):
    font(c, size)
    ext = c.text_extents(txt)
    if maxw and ext.x_advance > maxw:
        size = size * maxw / ext.x_advance; font(c, size); ext = c.text_extents(txt)
    c.move_to(x - ext.x_advance / 2, y); c.text_path(txt)
    if stroke:
        c.set_source_rgba(0, 0, 0, 0.85 * rgba[3]); c.set_line_width(stroke); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
    c.set_source_rgba(*rgba); c.fill(); c.new_path()


def wrap(c, txt, size, maxw):
    font(c, size); words = txt.split(' '); lines = []; cur = ''
    for w_ in words:
        tst = (cur + ' ' + w_).strip()
        if c.text_extents(tst).x_advance > maxw and cur:
            lines.append(cur); cur = w_
        else:
            cur = tst
    if cur: lines.append(cur)
    return lines


def rrect(c, x, y, w, h, r):
    c.new_sub_path()
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2); c.close_path()


IMG_CY = 760


def background(c, t, burst=0.0, tint=(0.08, 0.16, 0.32)):
    g = cairo.RadialGradient(W / 2, IMG_CY, 50, W / 2, IMG_CY, 1250)
    g.add_color_stop_rgb(0, *tint); g.add_color_stop_rgb(1, 0.01, 0.02, 0.05)
    c.set_source(g); c.paint()
    # rayons tournants
    n = 16; rot = t * 0.12
    c.save(); c.translate(W / 2, IMG_CY)
    for k in range(n):
        a0 = rot + k * 2 * math.pi / n
        c.move_to(0, 0); c.arc(0, 0, 1500, a0, a0 + math.pi / n * 0.55); c.close_path()
    c.set_source_rgba(1, 1, 1, 0.025 + 0.09 * burst); c.fill(); c.restore()
    # grille de fond
    c.set_source_rgba(0.5, 0.75, 1, 0.045); c.set_line_width(1)
    for x in range(0, W, 60):
        c.move_to(x, 0); c.line_to(x, H)
    off = (t * 20) % 60
    for y in range(-60, H, 60):
        c.move_to(0, y + off); c.line_to(W, y + off)
    c.stroke()


def draw_img(c, surf, w, h, cx, cy, scale, alpha):
    if alpha <= 0: return
    c.save(); c.translate(cx, cy); c.scale(scale, scale); c.translate(-w / 2, -h / 2)
    c.set_source_surface(surf, 0, 0); c.paint_with_alpha(min(1, alpha)); c.restore()


def header(c, t, qi):
    # logo
    font(c, 30); lab = "AVIONS DE LIGNE"
    e = c.text_extents(lab); bw = e.x_advance + 50
    rrect(c, W / 2 - bw / 2, 70, bw, 56, 28); c.set_source_rgba(*YEL, 1); c.fill()
    c.set_source_rgb(0.03, 0.05, 0.1); c.move_to(W / 2 - e.x_advance / 2, 109); c.show_text(lab)
    # progression
    dw = 70; x0 = W / 2 - dw * NQ / 2
    for i in range(NQ):
        cx = x0 + dw * (i + 0.5)
        done = qi is not None and (i < qi or (i == qi and t >= qs[i]['rev']))
        curq = qi == i
        rrect(c, cx - 26, 150, 52, 12, 6)
        if done: c.set_source_rgba(*GRN, 1)
        elif curq: c.set_source_rgba(*YEL, 1)
        else: c.set_source_rgba(1, 1, 1, 0.2)
        c.fill()


def draw_timer(c, t, q, cx, cy):
    u = (t - q['cd0']) / COUNT
    if u < 0 or t >= q['rev']: return
    appear = back_out((t - q['cd0']) / 0.3)
    rem = max(0, COUNT - (t - q['cd0']))
    num = int(math.ceil(rem)) if rem > 0 else 0
    col = GRN if num >= 3 else (YEL if num == 2 else RED)
    frac = rem / COUNT
    r = 62 * appear
    c.set_source_rgba(0, 0, 0, 0.55); c.arc(cx, cy, r + 10, 0, 2 * math.pi); c.fill()
    c.set_line_width(12); c.set_source_rgba(1, 1, 1, 0.15); c.arc(cx, cy, r, 0, 2 * math.pi); c.stroke()
    c.set_source_rgba(*col, 1); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.arc(cx, cy, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * frac); c.stroke(); c.set_line_cap(cairo.LINE_CAP_BUTT)
    pulse = 1 + 0.25 * max(0, 1 - ((t - q['cd0']) % 1) / 0.25)
    text_c(c, str(max(num, 1)), cx, cy + 26 * pulse * appear, 76 * pulse * appear, (*col, 1))


def draw_options(c, t, i, q):
    opts = Q[i]['options']; ans = Q[i]['answer']
    y0 = 1260; hgt = 96; gap = 22; wdt = 860
    revealed = t >= q['rev']
    for k, o in enumerate(opts):
        app = back_out((t - q['q0'] - 0.35 - 0.1 * k) / 0.35)
        if app <= 0: continue
        y = y0 + k * (hgt + gap)
        xoff = (1 - app) * 400 * (1 if k % 2 else -1)
        x = W / 2 - wdt / 2 + xoff
        ru = ease_out((t - q['rev']) / 0.25) if revealed else 0
        if revealed and k == ans:
            fill = (0.12 + 0.08 * (1 - ru), 0.55 + 0.2 * ru, 0.28, 0.95); border = GRN; ta = 1
            sc = 1 + 0.06 * math.sin(min(1, (t - q['rev']) / 0.35) * math.pi)
        elif revealed:
            fill = (0.25, 0.08, 0.1, 0.55); border = (0.6, 0.25, 0.28); ta = 0.45; sc = 1
        else:
            fill = (0.06, 0.1, 0.2, 0.85); border = (1, 1, 1); ta = 1; sc = 1
        c.save(); c.translate(W / 2, y + hgt / 2); c.scale(sc, sc); c.translate(-W / 2, -(y + hgt / 2))
        rrect(c, x, y, wdt, hgt, hgt / 2); c.set_source_rgba(*fill); c.fill_preserve()
        c.set_source_rgba(*border, 0.9 * ta); c.set_line_width(3); c.stroke()
        # lettre
        c.arc(x + hgt / 2, y + hgt / 2, 32, 0, 2 * math.pi)
        c.set_source_rgba(*(border if revealed else YEL), ta); c.fill()
        font(c, 38); L = "ABC"[k]; e = c.text_extents(L)
        c.set_source_rgb(0.03, 0.05, 0.1); c.move_to(x + hgt / 2 - e.x_advance / 2 - e.x_bearing, y + hgt / 2 + e.height / 2); c.show_text(L)
        font(c, 42); c.set_source_rgba(1, 1, 1, ta)
        e = c.text_extents(o); fs = 42
        if e.x_advance > wdt - 160:
            fs = 42 * (wdt - 160) / e.x_advance; font(c, fs); e = c.text_extents(o)
        c.move_to(x + hgt + 20, y + hgt / 2 + fs * 0.36); c.show_text(o)
        if revealed and k == ans:
            # coche
            c.set_source_rgb(1, 1, 1); c.set_line_width(8); c.set_line_cap(cairo.LINE_CAP_ROUND)
            cx = x + wdt - 55; cy = y + hgt / 2
            c.move_to(cx - 18, cy); c.line_to(cx - 5, cy + 14); c.line_to(cx + 20, cy - 16); c.stroke(); c.set_line_cap(cairo.LINE_CAP_BUTT)
        c.restore()


def draw_fact(c, t, i, q):
    u = ease_out((t - q['a0'] - 0.1) / 0.35)
    if u <= 0: return
    txt = Q[i]['a_show']
    # retirer l'intro « C'est le X ! » déjà affichée au-dessus
    if '!' in txt: txt = txt.split('!', 1)[1].strip()
    lines = wrap(c, txt, 40, 880)
    y = 1128 - (len(lines) - 1) * 24
    for k, ln in enumerate(lines):
        text_c(c, ln, W / 2, y + k * 50 + (1 - u) * 30, 40, (1, 1, 1, u), stroke=8)


def question_frame(c, t, i):
    q = qs[i]; im = IMGS[i]
    revealed = t >= q['rev']
    ru = (t - q['rev'])
    burst = max(0, 1 - ru / 1.2) if revealed else 0
    background(c, t, burst=burst, tint=(0.1, 0.2, 0.36) if not revealed else (0.16, 0.2, 0.34))
    header(c, t, i)
    # titre
    if not revealed:
        app = back_out((t - q['q0']) / 0.35)
        text_c(c, f"AVION N°{i + 1}", W / 2, 250, 44 * app, (*YEL, 1), stroke=6)
        text_c(c, "QUEL EST CET AVION ?", W / 2, 340, 70 * app, (1, 1, 1, 1), stroke=8, maxw=980)
    else:
        v = back_out(ru / 0.4)
        text_c(c, "C'EST LE...", W / 2, 250, 44, (*GRN, 1), stroke=6)
        text_c(c, Q[i]['name'].upper(), W / 2, 345, 74 * (0.6 + 0.4 * v), (*YEL, 1), stroke=9, maxw=1000)
    # avion
    enter = ease_out((t - q['q0']) / 0.45)
    zoom = 0.92 + 0.08 * ease((t - q['q0']) / (q['rev'] - q['q0']))
    bob = 8 * math.sin(t * 2.2)
    cx = W / 2 + (1 - enter) * W; cy = IMG_CY + bob
    if not revealed:
        # léger tremblement dans la dernière seconde
        if q['rev'] - t < 1.0:
            cx += 3 * math.sin(t * 70)
        draw_img(c, im['sil'], im['w'], im['h'], cx, cy, zoom, 1)
    else:
        pop = 1.0 + 0.08 * math.sin(min(1, ru / 0.35) * math.pi)
        s = 1.0 * pop + 0.03 * ease(ru / 4)
        draw_img(c, im['glow'], im['w'], im['h'], cx, cy, s, max(0, 0.9 - ru / 1.5))
        draw_img(c, im['sil'], im['w'], im['h'], cx, cy, s, 1 - ease(ru / 0.3))
        draw_img(c, im['color'], im['w'], im['h'], cx, cy, s, ease(ru / 0.3))
    draw_timer(c, t, q, W / 2, 1135)
    draw_options(c, t, i, q)
    if revealed:
        draw_fact(c, t, i, q)
        if ru < 0.25:
            c.set_source_rgba(1, 1, 1, 0.55 * (1 - ru / 0.25)); c.paint()
    # transition sortie
    if q['end'] - t < 0.2:
        c.set_source_rgba(0.01, 0.02, 0.05, 1 - (q['end'] - t) / 0.2); c.paint()
    if t - q['q0'] < 0.15:
        c.set_source_rgba(0.01, 0.02, 0.05, 1 - (t - q['q0']) / 0.15); c.paint()


def intro_frame(c, t):
    background(c, t, burst=0.3)
    header(c, t, None)
    lt = t - T['intro']
    # défilé rapide de silhouettes
    k = int(max(0, lt) / 0.42) % NQ
    im = IMGS[k]
    sc = 0.78 + 0.05 * ((max(0, lt) % 0.42) / 0.42)
    draw_img(c, im['sil'], im['w'], im['h'], W / 2, IMG_CY + 40, sc, min(1, lt / 0.2))
    a = back_out(lt / 0.4)
    text_c(c, "RECONNAIS-TU", W / 2, 300, 92 * a, (1, 1, 1, 1), stroke=10)
    text_c(c, "CES 10 AVIONS ?", W / 2, 405, 92 * a, (*YEL, 1), stroke=10, maxw=1000)
    b = back_out((lt - 1.6) / 0.4)
    if b > 0:
        c.save(); c.translate(W / 2, 1230); c.rotate(-0.05); c.scale(b, b)
        rrect(c, -330, -60, 660, 120, 30); c.set_source_rgba(*RED, 1); c.fill()
        text_c(c, "3 SECONDES CHACUN", 0, 20, 52, (1, 1, 1, 1))
        c.restore()
    b2 = back_out((lt - 3.1) / 0.4)
    if b2 > 0:
        text_c(c, "COMPTE TES POINTS !", W / 2, 1420, 64 * b2, (1, 1, 1, 1), stroke=8)
    if lt > D['intro'] + 0.25:
        c.set_source_rgba(0.01, 0.02, 0.05, min(1, (lt - D['intro'] - 0.25) / 0.2)); c.paint()


def outro_frame(c, t):
    lt = t - T['outro']
    background(c, t, burst=0.4)
    header(c, t, NQ - 1)
    a = back_out(lt / 0.4)
    text_c(c, "TON SCORE", W / 2, 300, 96 * a, (1, 1, 1, 1), stroke=10)
    text_c(c, "SUR 10 ?", W / 2, 410, 96 * a, (*YEL, 1), stroke=10)
    rows = [("0 – 3", "TOURISTE", (0.6, 0.65, 0.75)), ("4 – 6", "PASSAGER", CYA), ("7 – 9", "PILOTE", GRN), ("10", "AS DU MANCHE", YEL)]
    for k, (sc, lab, col) in enumerate(rows):
        u = back_out((lt - 0.4 - 0.2 * k) / 0.35)
        if u <= 0: continue
        y = 600 + k * 150
        c.save(); c.translate(W / 2, y + 55); c.scale(u, u); c.translate(-W / 2, -(y + 55))
        rrect(c, 110, y, 860, 110, 55); c.set_source_rgba(0.05, 0.09, 0.18, 0.9); c.fill_preserve()
        c.set_source_rgba(*col, 1); c.set_line_width(4); c.stroke()
        font(c, 50); c.set_source_rgba(*col, 1); c.move_to(160, y + 73); c.show_text(sc)
        font(c, 50); e = c.text_extents(lab); c.set_source_rgb(1, 1, 1); c.move_to(930 - e.x_advance, y + 73); c.show_text(lab)
        c.restore()
    u = back_out((lt - 1.5) / 0.4)
    if u > 0:
        text_c(c, "ÉCRIS-LE EN COMMENTAIRE", W / 2, 1300, 60 * u, (1, 1, 1, 1), stroke=8, maxw=980)
        # flèche vers le bas
        yy = 1360 + 12 * math.sin(t * 6)
        c.set_source_rgba(*YEL, u); c.move_to(W / 2 - 40, yy); c.line_to(W / 2 + 40, yy); c.line_to(W / 2, yy + 50); c.close_path(); c.fill()


_LAYER = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
_BEATS = sorted([q['q0'] for q in qs] + [q['cd0'] + k for q in qs for k in range(3)] + [q['rev'] for q in qs] + [q['a0'] for q in qs])


def _cam(t):
    last = max([b for b in _BEATS if b <= t] or [-9])
    punch = 0.05 * max(0.0, 1 - (t - last) / 0.18)
    sh = 0.0
    for q in qs:
        if 0 <= t - q['rev'] < 0.4: sh = 1 - (t - q['rev']) / 0.4
    return 1.02 + 0.015 * math.sin(t * 0.7) + punch + 0.03 * sh, 16 * sh * math.sin(t * 90), 12 * sh * math.cos(t * 77)


def render(t, surf):
    c0 = cairo.Context(surf)
    c = cairo.Context(_LAYER)
    if t < qs[0]['q0']:
        intro_frame(c, t)
    elif t >= T['outro']:
        outro_frame(c, t)
    else:
        i = max(k for k in range(NQ) if qs[k]['q0'] <= t)
        question_frame(c, t, i)
    _LAYER.flush()
    z, dx, dy = _cam(t)
    c0.save(); c0.translate(W / 2 + dx, H / 2 + dy); c0.scale(z, z); c0.translate(-W / 2, -H / 2)
    c0.set_source_surface(_LAYER, 0, 0); c0.paint(); c0.restore()
    c = c0
    if t < 0.2:
        c.set_source_rgba(0, 0, 0, 1 - t / 0.2); c.paint()
    if t > TOTAL - 0.4:
        c.set_source_rgba(0, 0, 0, (t - (TOTAL - 0.4)) / 0.4); c.paint()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        for tt in map(float, sys.argv[2:]):
            sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); render(tt, sf); sf.write_to_png(f'qa5/still_{tt:.1f}.png')
        print(json.dumps(qs[:2]), TOTAL); sys.exit()
    nframes = int(TOTAL * FPS)
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}',
                           '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
                           '-pix_fmt', 'yuv420p', 'qa5/video_noaudio.mp4'], stdin=subprocess.PIPE)
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    for f in range(nframes):
        render(f / FPS, sf); sf.flush(); ff.stdin.write(bytes(sf.get_data()))
        if f % 300 == 0: print(f, '/', nframes, flush=True)
    ff.stdin.close(); ff.wait(); print('done', TOTAL)
