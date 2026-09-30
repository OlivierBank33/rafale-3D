import cairo, json, math, subprocess, sys, re, random
import numpy as np
from PIL import Image, ImageFilter
from mc_script import SEGS

W, H, FPS = 1080, 1920, 30
D = json.load(open('mc/v/durs.json'))
YEL = (1.0, 0.84, 0.1); GRN = (0.25, 0.9, 0.45); RED = (1.0, 0.25, 0.25); CYA = (0.35, 0.85, 1.0); AMB = (1.0, 0.62, 0.1)

# ---------- Timeline ----------
TL = {}
t = 2.0  # alarme avant la voix
for s in SEGS:
    k = s['k']
    pre = 0.9 if k.startswith('c') else 0.0
    TL[k] = dict(t0=t - (1.6 if k == 'h' else 0) - 0.0, vt=t + pre)
    t = TL[k]['vt'] + D[k] + (0.8 if k != 'o' else 2.2)
    TL[k]['end'] = t
TL['h']['t0'] = 0.0
TOTAL = t
json.dump(dict(TL=TL, total=TOTAL), open('mc/timeline.json', 'w'))


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


def load(name, bw, bh, crop=True):
    im = Image.open(f'mc/{name}.png').convert('RGBA')
    off = (0, 0)
    if crop:
        bb = im.getbbox(); im = im.crop(bb); off = (bb[0], bb[1])
    sc = min(bw / im.width, bh / im.height)
    im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
    return dict(s=to_surface(im), w=im.width, h=im.height, sc=sc, off=off)


IM = {
    'a320': load('a320_hero', 980, 620), 'side': load('a320_side', 270, 120),
    'rat': load('a330_rat', 1500, 1500), 'a330': load('a330_hero', 940, 560), 'b767': load('b767_hero', 940, 560),
    'a320c': load('a320_hero', 940, 560),
}
MARK = json.load(open('mc/a330_rat.png.mark.json'))
MARK_X = (MARK['x'] - IM['rat']['off'][0]) * IM['rat']['sc']; MARK_Y = (MARK['y'] - IM['rat']['off'][1]) * IM['rat']['sc']


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


def pill(c, txt, cx, cy, size, bg, fg=(0.03, 0.05, 0.1), a=1.0, s=1.0):
    if s <= 0: return
    c.save(); c.translate(cx, cy); c.scale(s, s)
    font(c, size); e = c.text_extents(txt); bw = e.x_advance + size * 1.3; bh = size * 1.7
    rrect(c, -bw / 2, -bh / 2, bw, bh, bh / 2); c.set_source_rgba(*bg, a); c.fill()
    c.set_source_rgba(*fg, a); c.move_to(-e.x_advance / 2, size * 0.36); c.show_text(txt); c.restore()


def img(c, im, cx, cy, s=1.0, a=1.0, rot=0.0):
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s); c.translate(-im['w'] / 2, -im['h'] / 2)
    c.set_source_surface(im['s'], 0, 0); c.paint_with_alpha(min(1, max(0, a))); c.restore()


# ---------- Ciel ----------
random.seed(2)
CLOUDS = [dict(x=random.uniform(-200, W + 200), y=random.uniform(1150, 1900), r=random.uniform(90, 220), v=random.uniform(40, 110),
               a=random.uniform(0.25, 0.6)) for _ in range(40)]
STARS = [(random.uniform(0, W), random.uniform(0, 700), random.uniform(0.8, 2.2)) for _ in range(90)]


def sky(c, t, mood='high', speed=1.0):
    if mood == 'high':
        stops = [(0, (0.02, 0.05, 0.16)), (0.55, (0.1, 0.25, 0.5)), (0.72, (0.55, 0.62, 0.78)), (1, (0.75, 0.78, 0.85))]
    elif mood == 'dusk':
        stops = [(0, (0.05, 0.03, 0.12)), (0.55, (0.35, 0.16, 0.3)), (0.72, (0.95, 0.5, 0.3)), (1, (0.3, 0.2, 0.25))]
    elif mood == 'night':
        stops = [(0, (0.01, 0.02, 0.06)), (0.6, (0.04, 0.08, 0.18)), (0.75, (0.08, 0.16, 0.28)), (1, (0.02, 0.05, 0.1))]
    else:  # winter day
        stops = [(0, (0.3, 0.5, 0.75)), (0.6, (0.65, 0.75, 0.88)), (0.75, (0.85, 0.88, 0.92)), (1, (0.6, 0.65, 0.7))]
    g = cairo.LinearGradient(0, 0, 0, H)
    for p, col in stops: g.add_color_stop_rgb(p, *col)
    c.set_source(g); c.paint()
    if mood in ('high', 'night', 'dusk'):
        c.new_path()
        for x, y, r in STARS:
            c.new_sub_path(); c.arc(x, y, r, 0, 2 * math.pi)
        c.set_source_rgba(1, 1, 1, 0.5 if mood != 'dusk' else 0.25); c.fill()
    ccol = {'high': (0.9, 0.93, 1), 'dusk': (0.9, 0.6, 0.55), 'night': (0.35, 0.42, 0.55), 'day': (1, 1, 1)}[mood]
    for cl in CLOUDS:
        x = (cl['x'] - cl['v'] * t * speed) % (W + 500) - 250
        g2 = cairo.RadialGradient(x, cl['y'], 0, x, cl['y'], cl['r'])
        g2.add_color_stop_rgba(0, *ccol, cl['a']); g2.add_color_stop_rgba(1, *ccol, 0)
        c.set_source(g2); c.arc(x, cl['y'], cl['r'], 0, 2 * math.pi); c.fill()


def vignette(c, a=0.55):
    g = cairo.RadialGradient(W / 2, H / 2, 500, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, a)
    c.set_source(g); c.paint()


# ---------- Sous-titres ----------
def build_caps():
    caps = []
    for s in SEGS:
        words = s['show'].replace('11 000', '11 000').replace('12 000', '12 000').split(' ')
        def wt(w_):
            n = len(re.sub(r'[^\w]', '', w_)) + 3 * sum(ch.isdigit() for ch in w_)
            if w_.endswith(('.', '!', '?', ':')): n += 6
            if '...' in w_: n += 8
            if w_.endswith(','): n += 3
            return max(n, 2) + 2
        ws = [wt(w_) for w_ in words]; tot = sum(ws); t0 = TL[s['k']]['vt']; dur = D[s['k']]
        times = []; acc = 0
        for w_ in ws:
            times.append((t0 + dur * acc / tot, t0 + dur * (acc + w_) / tot)); acc += w_
        grp = []
        for i, w_ in enumerate(words):
            grp.append(i)
            if len(grp) == 3 or w_.endswith(('.', '!', '?', ':', ',')) or i == len(words) - 1 or (len(grp) == 2 and len(''.join(words[j] for j in grp)) > 14):
                caps.append(dict(words=[words[j] for j in grp], times=[times[j] for j in grp], t0=times[grp[0]][0], t1=times[grp[-1]][1])); grp = []
    return caps


CAPS = build_caps()


def captions(c, t):
    cap = None
    for cp in CAPS:
        if cp['t0'] - 0.02 <= t < cp['t1'] + 0.05: cap = cp
    if not cap: return
    size = 74; font(c, size)
    words = [w_ if w_.rstrip('.,!?') in ('m', 'km') else w_.upper() for w_ in cap['words']]
    sp = c.text_extents(' ').x_advance; widths = [c.text_extents(w_).x_advance for w_ in words]
    total = sum(widths) + sp * (len(words) - 1)
    if total > 840:
        size *= 840 / total; font(c, size); widths = [c.text_extents(w_).x_advance for w_ in words]; sp = c.text_extents(' ').x_advance
        total = sum(widths) + sp * (len(words) - 1)
    pop = back_out((t - cap['t0']) / 0.15); y = 1500
    c.save(); c.translate(W / 2, y); c.scale(0.85 + 0.15 * pop, 0.85 + 0.15 * pop); c.translate(-W / 2, -y)
    x = W / 2 - total / 2
    for w_, wd, (a, b) in zip(words, widths, cap['times']):
        c.move_to(x, y); c.text_path(w_)
        c.set_source_rgba(0, 0, 0, 0.9); c.set_line_width(14); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
        c.set_source_rgb(*(YEL if a <= t < b + 0.05 else (1, 1, 1))); c.fill(); c.new_path()
        x += wd + sp
    c.restore()


# ---------- Scènes ----------
def gauge(c, cx, cy, r, val, label, warn):
    c.set_source_rgba(0, 0, 0, 0.6); c.arc(cx, cy, r + 14, 0, 2 * math.pi); c.fill()
    a0, a1 = math.radians(150), math.radians(390)
    c.set_line_width(10); c.set_source_rgba(1, 1, 1, 0.2); c.arc(cx, cy, r, a0, a1); c.stroke()
    col = RED if warn else GRN
    c.set_source_rgba(*col, 1); c.arc(cx, cy, r, a0, a0 + (a1 - a0) * max(0.001, val / 100)); c.stroke()
    ang = a0 + (a1 - a0) * val / 100
    c.set_line_width(5); c.set_source_rgb(1, 1, 1); c.move_to(cx, cy); c.line_to(cx + math.cos(ang) * (r - 8), cy + math.sin(ang) * (r - 8)); c.stroke()
    text_c(c, f"{val:.0f}%", cx, cy + 58, 36, (*col, 1))
    text_c(c, label, cx, cy + r + 58, 30, (1, 1, 1, 0.9))


def scene_hook(c, t):
    s = TL['h']
    shake = 0
    fail = 1.0
    if t > fail: shake = 6 * max(0, 1 - (t - fail) / 1.2)
    sky(c, t, 'high', speed=1.0)
    bob = 10 * math.sin(t * 1.6)
    img(c, IM['a320'], W / 2 + shake * math.sin(t * 60), 760 + bob + shake * math.cos(t * 53), 1.0 + 0.03 * t / 8)
    vignette(c)
    # N1
    for k, (cx, lab, d) in enumerate([(250, 'ENG 1', 0.0), (830, 'ENG 2', 0.35)]):
        u = ease((t - fail - d) / 2.2)
        val = 84 * (1 - u) + 0 * u
        gauge(c, cx, 1060, 80, val, lab, u > 0.05)
    # alarme
    if t > fail:
        blink = (int((t - fail) * 3) % 2 == 0)
        a = back_out((t - fail) / 0.3)
        c.save(); c.translate(W / 2, 330); c.scale(a, a)
        rrect(c, -380, -62, 760, 124, 22); c.set_source_rgba(*(RED if blink else (0.5, 0.05, 0.05)), 0.95); c.fill()
        text_c(c, "ENG 1 + ENG 2 FAIL", 0, 22, 58, (1, 1, 1, 1)); c.restore()
    # altimètre
    alt = 11000 - max(0, t - 2.5) * 12
    pill(c, f"ALT {alt:,.0f} m".replace(',', ' '), W / 2, 180, 40, (0.05, 0.08, 0.15), fg=(1, 1, 1), a=0.9)
    if t > s['vt'] + 2.6:
        u = back_out((t - s['vt'] - 2.6) / 0.35)
        text_c(c, "TU AS COMBIEN DE TEMPS ?", W / 2, 1340, 64 * u, (*YEL, 1), stroke=9, maxw=1000)
    if t < 0.25:
        c.set_source_rgba(0, 0, 0, 1 - t / 0.25); c.paint()


def scene_glide(c, t):
    g1, g2 = TL['g1'], TL['g2']
    lt = t - g1['t0']
    sky(c, t, 'high', speed=0.4)
    c.set_source_rgba(0.01, 0.03, 0.08, 0.55); c.paint()
    a = back_out(lt / 0.4)
    text_c(c, "L'AVION DEVIENT", W / 2, 200, 76 * a, (1, 1, 1, 1), stroke=9)
    text_c(c, "UN PLANEUR", W / 2, 290, 88 * a, (*YEL, 1), stroke=9)
    # diagramme
    X0, Y0, X1, Y1 = 110, 470, 980, 1250
    c.set_source_rgba(0.35, 0.55, 0.3, 0.9); c.rectangle(60, Y1, W - 120, 22); c.fill()
    c.set_source_rgba(1, 1, 1, 0.5); c.set_line_width(3); c.move_to(X0 - 40, Y0); c.line_to(X0 - 40, Y1); c.stroke()
    text_c(c, "11 000 m", X0 + 40, Y0 - 25, 30, (1, 1, 1, 0.8))
    text_c(c, "0 m", X0 - 40, Y1 + 60, 28, (1, 1, 1, 0.7))
    if t < g2['vt']:
        # triangle de finesse
        u = ease_out((t - g1['vt'] - 3.5) / 1.2)
        tx0, ty0 = 190, 760
        L, Hh = 700 * u, 700 / 17 * 3.0 * u
        if u > 0:
            c.set_line_width(5)
            c.set_source_rgba(*CYA, 1); c.move_to(tx0, ty0); c.line_to(tx0 + L, ty0); c.stroke()
            c.set_source_rgba(*RED, 1); c.move_to(tx0 + L, ty0); c.line_to(tx0 + L, ty0 + Hh); c.stroke()
            c.set_source_rgba(1, 1, 1, 0.9); c.move_to(tx0, ty0); c.line_to(tx0 + L, ty0 + Hh); c.stroke()
            v = back_out((t - g1['vt'] - 4.6) / 0.4)
            if v > 0:
                text_c(c, "17 m EN AVANT", tx0 + L / 2, ty0 - 30, 50 * v, (*CYA, 1), stroke=7)
                text_c(c, "1 m EN BAS", tx0 + L - 60, ty0 + Hh + 70, 50 * v, (*RED, 1), stroke=7)
                pill(c, "FINESSE ≈ 17", W / 2, 1050, 52, YEL, s=v)
        img(c, IM['side'], 190, 700, 0.9, a=min(1, lt / 0.4), rot=0.02)
    else:
        u = ease((t - g2['vt']) / (D['g2'] * 0.85))
        px, py = X0 + (X1 - X0) * u, Y0 + (Y1 - 40 - Y0) * u
        c.set_dash([14, 12]); c.set_source_rgba(1, 1, 1, 0.35); c.set_line_width(3)
        c.move_to(X0, Y0); c.line_to(X1, Y1 - 40); c.stroke(); c.set_dash([])
        c.set_source_rgba(*YEL, 0.9); c.set_line_width(5); c.move_to(X0, Y0); c.line_to(px, py); c.stroke()
        img(c, IM['side'], px, py - 20, 0.8, rot=math.atan2(Y1 - 40 - Y0, X1 - X0) * 0.35)
        d_km = 190 * u; mins = 20 * u; alt = 11000 * (1 - u)
        for k, (lab, val, col) in enumerate([("DISTANCE", f"{d_km:.0f} km", CYA), ("TEMPS", f"{mins:.0f} min", YEL), ("ALTITUDE", f"{alt:,.0f} m".replace(',', ' '), (1, 1, 1))]):
            cx = 200 + k * 340
            text_c(c, lab, cx, 1330, 28, (1, 1, 1, 0.7))
            text_c(c, val, cx, 1400, 56, (*col, 1), stroke=7)
    vignette(c, 0.4)


def draw_prop(c, cx, cy, r, ang):
    c.set_source_rgba(0.05, 0.07, 0.12, 0.9); c.arc(cx, cy, r + 20, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(*CYA, 1); c.set_line_width(6); c.arc(cx, cy, r + 20, 0, 2 * math.pi); c.stroke()
    for k in range(2):
        a = ang + k * math.pi
        c.save(); c.translate(cx, cy); c.rotate(a)
        c.move_to(0, -10); c.curve_to(r * 0.4, -26, r * 0.9, -16, r, -4); c.line_to(r, 6); c.curve_to(r * 0.6, 14, r * 0.3, 14, 0, 10); c.close_path()
        c.set_source_rgb(0.85, 0.88, 0.92); c.fill(); c.restore()
    c.set_source_rgb(0.9, 0.2, 0.2); c.arc(cx, cy, 14, 0, 2 * math.pi); c.fill()
    # flou de rotation
    c.set_source_rgba(1, 1, 1, 0.12); c.set_line_width(r * 0.9); c.arc(cx, cy, r * 0.55, ang, ang + 1.2); c.stroke()


def scene_rat(c, t):
    s = TL['r']; lt = t - s['t0']
    sky(c, t, 'high', speed=0.6)
    z = 1.0 + 0.12 * ease((lt - 2.0) / 2.5)
    im = IM['rat']
    cx, cy = W / 2, 820
    # zoom vers le RAT
    fx = (MARK_X - im['w'] / 2); fy = (MARK_Y - im['h'] / 2)
    c.save(); c.translate(cx - fx * (z - 1) * 0.6, cy - fy * (z - 1) * 0.6)
    img(c, im, 0, 0, z * 0.72)
    mx, my = fx * z * 0.72, fy * z * 0.72
    u = back_out((t - s['vt'] - 2.4) / 0.4)
    if u > 0:
        c.set_source_rgba(*YEL, 1); c.set_line_width(6); c.arc(mx, my, 60 * u, 0, 2 * math.pi); c.stroke()
    c.restore()
    vignette(c, 0.45)
    a = back_out(lt / 0.4)
    text_c(c, "PLUS DE MOTEURS", W / 2, 200, 70 * a, (1, 1, 1, 1), stroke=9)
    text_c(c, "= PLUS DE COURANT ?", W / 2, 290, 70 * a, (*YEL, 1), stroke=9, maxw=1000)
    if u > 0:
        px, py = 790, 1170
        mxs = cx - fx * (z - 1) * 0.6 + mx; mys = cy - fy * (z - 1) * 0.6 + my
        c.set_source_rgba(*YEL, u); c.set_line_width(5); c.move_to(mxs, mys + 60); c.line_to(px - 60, py - 90); c.stroke()
        c.save(); c.translate(px, py); c.scale(u, u); draw_prop(c, 0, 0, 110, t * 25); c.restore()
        pill(c, "RAT : ÉOLIENNE DE SECOURS", W / 2 - 130, 1340, 40, YEL, s=u)


CASES = {
    'c1': dict(n=1, year='1983', title='LE PLANEUR DE GIMLI', img='b767', mood='dusk',
               chips=[(0.12, 'BOEING 767', (1, 1, 1)), (0.28, 'PANNE SÈCHE À 12 500 m', AMB), (0.48, 'ERREUR LIVRES / KILOS', RED),
                      (0.7, 'ATTERRIT SUR UNE EX-BASE MILITAIRE', CYA), (0.88, '69 SURVIVANTS', GRN)]),
    'c2': dict(n=2, year='2001', title='VOL TRANSAT 236', img='a330', mood='night',
               chips=[(0.12, 'AIRBUS A330', (1, 1, 1)), (0.25, 'FUITE DE CARBURANT', AMB), (0.45, '120 km EN VOL PLANÉ', CYA),
                      (0.65, 'RECORD POUR UN AVION DE LIGNE', YEL), (0.88, '306 SURVIVANTS', GRN)]),
    'c3': dict(n=3, year='2009', title="LE MIRACLE DE L'HUDSON", img='a320c', mood='day',
               chips=[(0.12, 'AIRBUS A320', (1, 1, 1)), (0.3, 'OIES DANS LES MOTEURS', AMB), (0.5, '3 MIN 30 POUR AGIR', RED),
                      (0.7, 'AMERRISSAGE SUR LE FLEUVE', CYA), (0.9, '155 SURVIVANTS', GRN)]),
}


def scene_case(c, t, k):
    s = TL[k]; cs = CASES[k]; lt = t - s['t0']
    sky(c, t, cs['mood'], speed=1.4)
    c.set_source_rgba(0, 0, 0, 0.25); c.paint()
    # année géante en fond
    a = back_out(lt / 0.45)
    font(c, 330); c.set_source_rgba(1, 1, 1, 0.1 * min(1, lt / 0.3))
    e = c.text_extents(cs['year']); c.move_to(W / 2 - e.x_advance / 2, 900); c.show_text(cs['year'])
    pill(c, f"CAS RÉEL {cs['n']}/3", W / 2, 150, 34, YEL, s=a)
    text_c(c, cs['year'], W / 2, 300, 110 * a, (*YEL, 1), stroke=10)
    text_c(c, cs['title'], W / 2, 390, 60 * a, (1, 1, 1, 1), stroke=8, maxw=1000)
    # avion en descente
    prog = ease((t - s['vt']) / max(1, D[k]))
    enter = ease_out(lt / 0.6)
    x = W / 2 - (1 - enter) * W * 0.8 + 60 * prog
    y = 700 + 90 * prog + 8 * math.sin(t * 2)
    img(c, IM[cs['img']], x, y, 0.95, rot=0.04 + 0.04 * prog)
    # lignes de vitesse
    c.set_source_rgba(1, 1, 1, 0.12); c.set_line_width(3)
    for j in range(10):
        yy = 520 + (j * 67 + t * 380) % 440; xx = (j * 173 + t * 900) % (W + 400) - 200
        c.move_to(xx, yy); c.line_to(xx - 160, yy - 50)
    c.stroke()
    # puces
    shown = [ch for ch in cs['chips'] if t >= s['vt'] + ch[0] * D[k]]
    for j, (fr, txt, col) in enumerate(cs['chips']):
        tt = s['vt'] + fr * D[k]
        if t < tt: continue
        u = back_out((t - tt) / 0.3)
        yy = 1010 + j * 72
        font(c, 36); e = c.text_extents(txt); bw = e.x_advance + 60
        c.save(); c.translate(W / 2, yy); c.scale(u, u)
        rrect(c, -bw / 2, -30, bw, 60, 30); c.set_source_rgba(0.03, 0.05, 0.1, 0.85); c.fill_preserve()
        c.set_source_rgba(*col, 1); c.set_line_width(3); c.stroke()
        c.set_source_rgba(*col, 1); c.move_to(-e.x_advance / 2, 13); c.show_text(txt); c.restore()
    vignette(c, 0.4)


def scene_outro(c, t):
    s = TL['o']; lt = t - s['t0']
    sky(c, t, 'high', speed=1.0)
    img(c, IM['a320'], W / 2 + 40 * math.sin(t * 0.5), 820 + 10 * math.sin(t * 1.5), 0.95)
    vignette(c, 0.45)
    a = back_out(lt / 0.4)
    text_c(c, "MORALITÉ", W / 2, 220, 90 * a, (*YEL, 1), stroke=10)
    if t > s['vt'] + 4.3:
        u = back_out((t - s['vt'] - 4.3) / 0.4)
        text_c(c, "ET TOI, TU MONTES", W / 2, 330, 64 * u, (1, 1, 1, 1), stroke=9)
        text_c(c, "ENCORE EN AVION ?", W / 2, 410, 64 * u, (1, 1, 1, 1), stroke=9)
        yy = 1290 + 14 * math.sin(t * 6)
        c.set_source_rgba(*YEL, u); c.move_to(W / 2 - 45, yy); c.line_to(W / 2 + 45, yy); c.line_to(W / 2, yy + 55); c.close_path(); c.fill()


ORDER = ['h', 'g1', 'g2', 'r', 'c1', 'c2', 'c3', 'o']


def render(t, surf):
    c = cairo.Context(surf)
    k = 'h'
    for kk in ORDER:
        if t >= TL[kk]['t0']: k = kk
    if k == 'h': scene_hook(c, t)
    elif k in ('g1', 'g2'): scene_glide(c, t)
    elif k == 'r': scene_rat(c, t)
    elif k.startswith('c'): scene_case(c, t, k)
    else: scene_outro(c, t)
    # transitions
    lt = t - TL[k]['t0']
    if k not in ('h', 'g2') and lt < 0.15:
        c.set_source_rgba(1, 1, 1, 0.6 * (1 - lt / 0.15)); c.paint()
    captions(c, t)
    # barre de progression
    c.set_source_rgba(1, 1, 1, 0.15); c.rectangle(0, 0, W, 8); c.fill()
    c.set_source_rgba(*YEL, 1); c.rectangle(0, 0, W * t / TOTAL, 8); c.fill()
    if t > TOTAL - 0.4:
        c.set_source_rgba(0, 0, 0, (t - (TOTAL - 0.4)) / 0.4); c.paint()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        for tt in map(float, sys.argv[2:]):
            sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); render(tt, sf); sf.write_to_png(f'mc/still_{tt:.1f}.png')
        print(round(TOTAL, 1), {k: (round(v['t0'], 1), round(v['vt'], 1)) for k, v in TL.items()}); sys.exit()
    nframes = int(TOTAL * FPS)
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}',
                           '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '21',
                           '-pix_fmt', 'yuv420p', 'mc/video_noaudio.mp4'], stdin=subprocess.PIPE)
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    for f in range(nframes):
        render(f / FPS, sf); sf.flush(); ff.stdin.write(bytes(sf.get_data()))
        if f % 300 == 0: print(f, '/', nframes, flush=True)
    ff.stdin.close(); ff.wait(); print('done', TOTAL)
