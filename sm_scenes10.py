"""Film premium « Concorde, vol AF4590 » (cc_*) : Concorde 3D réel (FlightGear, livrée Air France F-BTSC, rendu Cycles -> pr/r_*.png
avec points 3D projetés pr/r_*.json), plaques de décor photoréalistes (pr/p_*.png, pr/plates.py), effets procéduraux (flammes, fumée,
réchauffe, onde de pression), infographies sobres. Signatures : vol au ras de la piste avec flamme physiquement orientée, rayons X du
réservoir 5 (onde de pression, rupture, jet de kérosène), panneau des départs à palettes, cadrans moteurs, bande de vitesse V1."""
import cairo, math, random, json, os
import numpy as np
from PIL import Image, ImageFilter
from sm_lib import *
from sm_scenes2 import ease, ap
from sm_scenes6 import si, stamp, eout
from sm_scenes7 import tag, label, mix, check, cross
R = None
PR = '/home/claude/pr/'
YEL = (1.0, 0.85, 0.25); ORG = (1.0, 0.55, 0.12); RED = (1.0, 0.25, 0.25); WH = (1, 1, 1); GRN = (0.4, 1, 0.6)
CY = (0.35, 0.9, 1.0); AMB = (1.0, 0.75, 0.2)
_KEEP = []


# =============================================================== images -> cairo
def _surf(im):
    a = np.asarray(im.convert('RGBA')).astype(np.float32)
    al = a[..., 3:4] / 255.0
    rgb = a[..., :3] * al
    h, w = a.shape[:2]
    stride = cairo.ImageSurface.format_stride_for_width(cairo.FORMAT_ARGB32, w)
    buf = np.zeros((h, stride // 4, 4), np.uint8)
    buf[:, :w, 0] = rgb[..., 2]; buf[:, :w, 1] = rgb[..., 1]; buf[:, :w, 2] = rgb[..., 0]; buf[:, :w, 3] = a[..., 3]
    _KEEP.append(buf)
    return cairo.ImageSurface.create_for_data(memoryview(buf).cast('B'), cairo.FORMAT_ARGB32, w, h, stride)


def hblur(im, r):
    a = np.asarray(im).astype(np.float32)
    k = 2 * r + 1
    pad = np.concatenate([a[:, -r:], a, a[:, :r]], axis=1)
    cs = np.cumsum(pad, axis=1); cs = np.concatenate([np.zeros_like(cs[:, :1]), cs], axis=1)
    out = (cs[:, k:] - cs[:, :-k]) / k
    return Image.fromarray(np.clip(out[:, :a.shape[1]], 0, 255).astype(np.uint8), im.mode)


_PL = {}
def plate(name, mb=0, gb=0, scale=1.0):
    key = (name, mb, gb, scale)
    if key not in _PL:
        im = Image.open(PR + name)
        im = im.convert('RGBA')
        if scale != 1.0: im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
        if gb: im = im.filter(ImageFilter.GaussianBlur(gb))
        if mb: im = hblur(im, mb)
        _PL[key] = (_surf(im), im.size)
    return _PL[key]


def draw_plate(c, name, x, y, sc=1.0, alpha=1.0, mb=0, gb=0):
    s, (w, h) = plate(name, mb, gb)
    c.save(); c.translate(x, y); c.scale(sc, sc); c.rectangle(0, 0, w, h); c.clip()
    c.set_source_surface(s, 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint_with_alpha(alpha); c.restore()


def tile_x(c, name, off, y, sc=1.0, alpha=1.0, mb=0, gb=0):
    """bande qui défile horizontalement (off en px écran, positif = le décor part vers la droite)."""
    s, (w, h) = plate(name, mb, gb)
    ww = w * sc; x0 = (off % ww) - ww
    while x0 < W:
        c.save(); c.translate(x0, y); c.scale(sc, sc); c.rectangle(0, 0, w, h); c.clip()
        c.set_source_surface(s, 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint_with_alpha(alpha); c.restore()
        x0 += ww


# =============================================================== sprites 3D
_IMG = {}
def _load(name):
    if name not in _IMG:
        im = Image.open(PR + f'r_{name}.png').convert('RGBA'); bb = im.split()[3].getbbox()
        bb = (max(0, bb[0] - 4), max(0, bb[1] - 4), min(im.width, bb[2] + 4), min(im.height, bb[3] + 4))
        im = im.crop(bb); pts = {}
        jp = PR + f'r_{name}.json'
        if os.path.exists(jp):
            js = json.load(open(jp)); pts = {k: (v[0] - bb[0], v[1] - bb[1]) for k, v in js['pts'].items()}
        _IMG[name] = (im, pts)
    return _IMG[name]


_SP = {}
def spr(name, scale, dark=0.0, warm=0.0, xray=False):
    b = 1.0
    while b * 0.8 >= scale and b > 0.04: b *= 0.8
    key = (name, round(b, 5), dark, warm, xray)
    if key not in _SP:
        im, pts = _load(name)
        im2 = im.resize((max(1, round(im.width * b)), max(1, round(im.height * b))), Image.LANCZOS)
        if xray:
            a = np.asarray(im2).astype(np.float32)
            lum = (0.3 * a[..., 0] + 0.59 * a[..., 1] + 0.11 * a[..., 2]) / 255
            e1 = np.asarray(Image.fromarray((lum * 255).astype(np.uint8)).filter(ImageFilter.FIND_EDGES)).astype(np.float32) / 255
            e2 = np.asarray(Image.fromarray(a[..., 3].astype(np.uint8)).filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(3))).astype(np.float32) / 255
            e = np.clip(e1 * 3.0 + e2 * 1.2, 0, 1)
            v = np.clip(0.18 + 0.25 * (1 - lum) + 0.85 * e, 0, 1)
            out = np.zeros_like(a)
            out[..., 0] = v * 95; out[..., 1] = v * 225; out[..., 2] = v * 255
            out[..., 3] = a[..., 3] * np.clip(0.35 + 0.65 * e, 0, 1)
            im2 = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), 'RGBA')
        if dark or warm:
            a = np.asarray(im2).astype(np.float32)
            rgb = a[..., :3]
            if warm: rgb = rgb * (1 - warm) + rgb * np.array([1.08, 0.86, 0.66]) * warm
            if dark: rgb = rgb * (1 - dark) + np.array([22, 24, 30]) * dark
            a[..., :3] = np.clip(rgb, 0, 255); im2 = Image.fromarray(a.astype(np.uint8), 'RGBA')
        _SP[key] = (_surf(im2), b, {k: (vv[0] * b, vv[1] * b) for k, vv in pts.items()}, im2.size)
    return _SP[key]


def plane(c, name, x, y, scale, rot=0.0, anchor='img', alpha=1.0, dark=0.0, warm=0.0, shadow=None, xray=False):
    """dessine le sprite ; renvoie P(nom) -> coordonnées écran d'un point 3D projeté (nose, tail, lgear, noz1..4, impact, leak, tank5...)."""
    s, b, pts, (w, h) = spr(name, scale, dark, warm, xray)
    k = scale / b
    ax, ay = pts.get(anchor, (w / 2, h / 2))
    cr, sn = math.cos(rot), math.sin(rot)
    def P(nm, ox=0.0, oy=0.0):
        px, py = pts.get(nm, (w / 2, h / 2)); px = (px - ax) * k + ox; py = (py - ay) * k + oy
        return x + cr * px - sn * py, y + sn * px + cr * py
    if shadow is not None:                                     # ombre portée douce sur le sol (y = shadow)
        gx, gy = P('center'); L = w * k * 0.5
        c.save(); c.translate(gx, shadow); c.scale(1, 0.06)
        g = cairo.RadialGradient(0, 0, 0, 0, 0, L); g.add_color_stop_rgba(0, 0, 0, 0, 0.35 * alpha); g.add_color_stop_rgba(1, 0, 0, 0, 0)
        c.arc(0, 0, L, 0, 7); c.set_source(g); c.fill(); c.restore()
    if alpha <= 0: return P
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k); c.translate(-ax, -ay)
    c.rectangle(0, 0, w, h); c.clip()
    c.set_source_surface(s, 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint_with_alpha(alpha); c.restore()
    return P


def aft_dir(P):
    nx, ny = P('nose'); tx, ty = P('noz2'); d = math.hypot(tx - nx, ty - ny) or 1
    return (tx - nx) / d, (ty - ny) / d, d


# =============================================================== effets
def glow(c, x, y, r, col, a, op=None):
    g = cairo.RadialGradient(x, y, 0, x, y, r); g.add_color_stop_rgba(0, *col, a); g.add_color_stop_rgba(1, *col, 0)
    if op is not None: c.save(); c.set_operator(op)
    c.new_path(); c.arc(x, y, r, 0, 7); c.set_source(g); c.fill()
    if op is not None: c.restore()


def flame(c, x, y, dx, dy, L, wd, t, inten=1.0, seed=0, smoke=1.0, grow=1.0, persp=0.0):
    """panache de feu de kérosène : (x,y) origine, (dx,dy) direction (vers l'arrière), L longueur, wd largeur à l'origine.
    persp > 0 : le panache s'élargit (vient vers la caméra)."""
    if inten <= 0: return
    nx, ny = -dy, dx
    N = 90
    rnd = random.Random(seed)
    ph = [rnd.random() for _ in range(N)]; sd = [rnd.uniform(-1, 1) for _ in range(N)]; sz = [rnd.uniform(0.7, 1.3) for _ in range(N)]
    # fumée d'abord (derrière le feu)
    if smoke > 0:
        for i in range(N):
            s = (ph[i] + t * 0.55) % 1.0
            if s < 0.35: continue
            q = (s - 0.35) / 0.65
            d = L * (0.55 + 0.9 * q) * grow
            off = sd[i] * wd * (0.6 + 2.2 * q) * (1 + persp * q) + math.sin(t * 1.3 + i) * wd * 0.4 * q
            px, py = x + dx * d + nx * off, y + dy * d + ny * off - wd * 1.4 * q * q
            r = wd * (0.9 + 2.6 * q) * sz[i] * (1 + persp * 1.5 * q)
            a = 0.30 * smoke * inten * (1 - q) ** 0.8
            glow(c, px, py, r, (0.14, 0.12, 0.11), a)
    for i in range(N):
        s = (ph[i] + t * 1.6) % 1.0
        d = L * s * grow
        wob = math.sin(t * 9 + i * 1.7) * 0.25 + math.sin(t * 4.1 + i) * 0.2
        off = (sd[i] * 0.7 + wob) * wd * (0.35 + 1.1 * s) * (1 + persp * s)
        px, py = x + dx * d + nx * off, y + dy * d + ny * off - wd * 0.35 * s * s
        r = wd * (0.35 + 1.15 * s) * sz[i] * (1 + persp * 1.2 * s)
        if s < 0.18: col = (1.0, 0.92, 0.65)
        elif s < 0.5: col = mix((1.0, 0.92, 0.65), (1.0, 0.5, 0.12), (s - 0.18) / 0.32)
        else: col = mix((1.0, 0.5, 0.12), (0.55, 0.12, 0.03), (s - 0.5) / 0.5)
        a = 0.42 * inten * (1 - s) ** 0.9
        glow(c, px, py, r, col, a)
        if s < 0.3:
            c.save(); c.set_operator(cairo.OPERATOR_ADD); glow(c, px, py, r * 0.6, (1.0, 0.85, 0.5), 0.25 * inten * (1 - s / 0.3)); c.restore()
    c.save(); c.set_operator(cairo.OPERATOR_ADD)
    glow(c, x + dx * L * 0.08, y + dy * L * 0.08, wd * 1.3, (1, 0.95, 0.8), 0.5 * inten)
    c.restore()
    glow(c, x + dx * L * 0.3, y + dy * L * 0.3, L * 0.6, (1.0, 0.45, 0.1), 0.18 * inten)   # lueur portée


def reheat(c, P, t, a=1.0, L=120, engines=(1, 2, 3, 4), dark=False):
    dx, dy, _ = aft_dir(P)
    c.save(); c.set_operator(cairo.OPERATOR_ADD)
    for e in engines:
        x, y = P(f'noz{e}')
        fl = 1 + 0.06 * math.sin(t * 40 + e)
        for j, (col, LL, ww, aa) in enumerate((((1.0, 0.55, 0.2), 1.0, 0.22, 0.45), ((1.0, 0.8, 0.45), 0.6, 0.14, 0.6), ((0.75, 0.85, 1.0), 0.28, 0.08, 0.8))):
            n = 10
            for k in range(n):
                u = k / n; px, py = x + dx * L * LL * u * fl, y + dy * L * LL * u * fl
                glow(c, px, py, L * ww * (1 - 0.6 * u), col, aa * a * (1 - u) * 0.5)
        for k in range(3):   # disques de Mach
            u = 0.18 + 0.16 * k; glow(c, x + dx * L * u, y + dy * L * u, L * 0.05, (1, 1, 0.95), 0.6 * a)
    c.restore()


def smoke_col(c, x, y, h, t, a=1.0, seed=3, wd=60):
    rnd = random.Random(seed)
    for i in range(60):
        ph = rnd.random(); s = (ph + t * 0.08) % 1.0
        px = x + rnd.uniform(-1, 1) * wd * (0.3 + 1.6 * s) + s * s * 160
        py = y - h * s
        r = wd * (0.5 + 2.2 * s)
        glow(c, px, py, r, (0.16, 0.15, 0.15), 0.35 * a * (1 - s) ** 0.6)


def sun_flare(c, sx, sy, a=1.0):
    c.save(); c.set_operator(cairo.OPERATOR_ADD)
    glow(c, sx, sy, 520, (1.0, 0.85, 0.6), 0.35 * a); glow(c, sx, sy, 140, (1, 1, 0.95), 0.8 * a)
    vx, vy = W / 2 - sx, H * 0.48 - sy
    for f, r, col in ((0.6, 40, (0.6, 0.8, 1)), (1.1, 90, (1, 0.7, 0.4)), (1.5, 26, (0.7, 1, 0.8)), (1.9, 140, (0.5, 0.6, 1))):
        glow(c, sx + vx * f, sy + vy * f, r, col, 0.10 * a)
    c.restore()


def grade(c, top=(1.0, 0.6, 0.3), bot=(0.1, 0.3, 0.45), a=0.12):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgba(0, *top, a); g.add_color_stop_rgba(1, *bot, a)
    c.save(); c.set_operator(cairo.OPERATOR_SOFT_LIGHT); c.set_source(g); c.paint(); c.restore()


def letter(c, s, x, y, size, col, a=1.0, fam='Bebas Neue', anchor='c'):
    c.save(); c.select_font_face(fam, 0, 1); c.set_font_size(size); e = c.text_extents(s)
    xx = x - e.width / 2 - e.x_bearing if anchor == 'c' else (x if anchor == 'l' else x - e.width)
    c.move_to(xx, y); c.text_path(s); c.set_source_rgba(*col, a); c.fill(); c.restore()


def panel(c, x, y, w, h, a=0.62, r=26):
    rr(c, x, y, w, h, r); c.set_source_rgba(0.02, 0.03, 0.05, a); c.fill()


def counter(c, val, unit, x, y, col=YEL, size=120, a=1.0):
    letter(c, val, x, y, size, col, a); letter(c, unit, x, y + size * 0.42, size * 0.32, WH, a * 0.85, 'Montserrat')


# =============================================================== décors
SUN = (886, 288)
def sky_bg(c, t, warm=False, oy=300, sc=1.0, drift=8.0):
    name = 'p_sky_warm.png' if warm else 'p_sky_day.png'
    draw_plate(c, name, 0, -oy, sc)
    return SUN[0], SUN[1] - oy


def strato_bg(c, t):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, 0.0, 0.0, 0.03); g.add_color_stop_rgb(0.55, 0.02, 0.05, 0.16); g.add_color_stop_rgb(0.78, 0.12, 0.28, 0.6)
    c.set_source(g); c.paint()
    r = random.Random(5)
    for _ in range(220):
        x = r.random() * W; y = r.random() * H * 0.55
        c.new_path(); c.arc(x, y, r.choice((0.8, 1.2, 1.7)), 0, 7); c.set_source_rgba(1, 1, 1, 0.25 + 0.6 * r.random()); c.fill()
    cx, cy, Rr = 540, 1480 + 5200, 5200
    c.new_path(); c.arc(cx, cy, Rr + 70, 0, 7)
    g = cairo.RadialGradient(cx, cy, Rr - 5, cx, cy, Rr + 70); g.add_color_stop_rgba(0, 0.4, 0.75, 1, 0.95); g.add_color_stop_rgba(1, 0.4, 0.75, 1, 0); c.set_source(g); c.fill()
    c.new_path(); c.arc(cx, cy, Rr, 0, 7)
    g = cairo.LinearGradient(0, 1480, 0, H); g.add_color_stop_rgb(0, 0.32, 0.5, 0.72); g.add_color_stop_rgb(0.15, 0.12, 0.3, 0.55); g.add_color_stop_rgb(1, 0.04, 0.12, 0.28); c.set_source(g); c.fill()
    c.save(); c.new_path(); c.arc(cx, cy, Rr, 0, 7); c.clip()
    rr_ = random.Random(9)
    for _ in range(70):
        x = (rr_.random() * W * 1.5 - t * 14) % (W * 1.5) - 200; y = 1500 + rr_.random() ** 1.4 * 420; w = 30 + 160 * rr_.random() * (y - 1480) / 420
        c.save(); c.translate(x, y); c.scale(1, 0.25); c.new_path(); c.arc(0, 0, w, 0, 7); c.restore(); c.set_source_rgba(1, 1, 1, 0.3); c.fill()
    c.restore()


def runway_side(c, t, speed, ground_y=1230, sc=1.0, off=None, sky_oy=520):
    """travelling latéral le long de la piste : speed en px/s (le décor part vers la droite : l'avion va à gauche).
    Renvoie la ligne de contact des roues (milieu de la bande d'asphalte)."""
    sky_bg(c, t, oy=sky_oy)
    off = t * speed if off is None else off
    mb = 0 if speed < 300 else (10 if speed < 1200 else 34)
    sf = min(sc, 1.4)
    tile_x(c, 'p_far.png', off * 0.05, ground_y - 462 * sf, sf, mb=0)
    c.save(); c.rectangle(0, ground_y, W, H); c.clip()
    tile_x(c, 'p_runway.png', off, ground_y + 60 * sc - 270 * sc, sc, mb=mb)
    c.restore()
    g = cairo.LinearGradient(0, ground_y, 0, ground_y + 40); g.add_color_stop_rgba(0, 0.86, 0.85, 0.8, 0.7); g.add_color_stop_rgba(1, 0.86, 0.85, 0.8, 0)
    c.rectangle(0, ground_y, W, 40); c.set_source(g); c.fill()
    g = cairo.LinearGradient(0, ground_y + 420 * sc, 0, H); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.35)
    c.rectangle(0, ground_y + 420 * sc, W, H); c.set_source(g); c.fill()
    return ground_y + 177 * sc


def runway_axis(c, t, blur=0, oy=0, low=True):
    """vue dans l'axe : low = caméra à 6 m (horizon y = 900, contact à la distance Z : y = 900 + 5400/Z, 900/Z px par mètre)."""
    sky_bg(c, t, oy=820 if low else 760)
    draw_plate(c, 'p_rw_low.png' if low else 'p_rw_persp.png', 0, oy, 1.0, gb=blur)


def ppm(name):
    im, pts = _load(name)
    (ax, ay), (bx, by) = pts.get('lwtip', (0, 0)), pts.get('rwtip', (1, 0))
    return max(1.0, math.hypot(bx - ax, by - ay)) / 24.6


def on_axis(c, name, Z, t, x=540, alpha=1.0, gear_side=-1):
    """avion posé sur la piste vue dans l'axe, à Z mètres de la caméra (6 m de haut)."""
    k = 900.0 / Z; sc = k / ppm(name)
    yc = 900 + 5400.0 / Z
    P0 = plane(c, name, 0, 0, sc, alpha=0.0)
    cx, cy = P0('center'); gx, gy = P0('lgear'); hx, hy = P0('rgear')
    gy2 = max(gy, hy)
    span = 25.6 * k
    c.save(); c.translate(x, yc + 2); c.scale(1, 0.07)
    g = cairo.RadialGradient(0, 0, 0, 0, 0, span * 0.55); g.add_color_stop_rgba(0, 0, 0, 0, 0.55 * alpha); g.add_color_stop_rgba(1, 0, 0, 0, 0)
    c.arc(0, 0, span * 0.55, 0, 7); c.set_source(g); c.fill(); c.restore()
    return plane(c, name, x - cx, yc - gy2, sc, alpha=alpha), sc


def asphalt(c, t, blur=0, zoom=1.0, cx=540, cy=960):
    s, (w, h) = plate('p_asphalt.png', 0, blur)
    c.save(); c.translate(cx, cy); c.scale(zoom * 1.45, zoom * 1.45); c.translate(-w / 2, -h / 2)
    c.rectangle(0, 0, w, h); c.clip(); c.set_source_surface(s, 0, 0); c.paint(); c.restore()


def wear_strip(c, x, y, L, rot, t, glint=True, a=1.0):
    """lamelle d'usure en titane (≈ 43 × 3 cm), légèrement tordue, trous de rivets."""
    c.save(); c.translate(x, y); c.rotate(rot)
    th = L * 0.07
    c.new_path(); c.move_to(-L / 2, -th / 2); c.curve_to(-L / 6, -th / 2 - L * 0.012, L / 6, -th / 2 + L * 0.01, L / 2, -th / 2 - L * 0.02)
    c.line_to(L / 2, th / 2 - L * 0.02); c.curve_to(L / 6, th / 2 + L * 0.01, -L / 6, th / 2 - L * 0.012, -L / 2, th / 2); c.close_path()
    g = cairo.LinearGradient(0, -th / 2, 0, th / 2); g.add_color_stop_rgba(0, 0.86, 0.87, 0.9, a); g.add_color_stop_rgba(0.45, 0.6, 0.62, 0.66, a); g.add_color_stop_rgba(1, 0.35, 0.36, 0.4, a)
    c.set_source(g); c.fill_preserve(); c.set_source_rgba(0.12, 0.12, 0.14, a); c.set_line_width(max(1.5, th * 0.06)); c.stroke()
    for j in range(7):
        c.new_path(); c.arc(-L / 2 + L * (0.07 + 0.143 * j), 0, th * 0.13, 0, 7); c.set_source_rgba(0.12, 0.12, 0.13, a); c.fill()
    if glint:
        gp = ((t * 0.5) % 1.4 - 0.2) * L - L / 2
        g = cairo.LinearGradient(gp - L * 0.1, 0, gp + L * 0.1, 0); g.add_color_stop_rgba(0, 1, 1, 1, 0); g.add_color_stop_rgba(0.5, 1, 1, 1, 0.55 * a); g.add_color_stop_rgba(1, 1, 1, 1, 0)
        c.rectangle(-L / 2, -th, L, th * 2); c.set_source(g); c.fill()
    c.restore()


def dc10_sil(c, x, y, s, rot, a=1.0, col=(0.32, 0.34, 0.38)):
    """DC-10 en silhouette lointaine (dans la brume) : triréacteur, moteur central dans la dérive. Nez à gauche."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.set_source_rgba(*col, a)
    c.new_path(); c.move_to(-300, 0); c.curve_to(-300, -18, -270, -24, -230, -24); c.line_to(220, -24); c.line_to(300, -30); c.line_to(305, -8); c.line_to(250, 10)
    c.line_to(-240, 16); c.curve_to(-280, 14, -300, 10, -300, 0); c.close_path(); c.fill()
    c.new_path(); c.move_to(200, -24); c.line_to(250, -120); c.line_to(300, -120); c.line_to(290, -26); c.close_path(); c.fill()     # dérive
    rr(c, 225, -112, 90, 26, 12); c.fill()                                                                                         # réacteur central
    c.new_path(); c.move_to(-40, 8); c.line_to(130, 60); c.line_to(170, 60); c.line_to(60, 6); c.close_path(); c.fill()          # aile
    rr(c, -10, 22, 70, 22, 10); c.fill()                                                                                           # réacteur d'aile
    c.new_path(); c.move_to(230, -14); c.line_to(300, 8); c.line_to(315, 8); c.line_to(280, -14); c.close_path(); c.fill()       # empennage
    c.restore()


def tower(c, x, y, s, a=1.0, col=(0.2, 0.22, 0.26)):
    c.save(); c.translate(x, y); c.scale(s, s); c.set_source_rgba(*col, a)
    c.new_path(); c.move_to(-26, 0); c.line_to(-18, -420); c.line_to(18, -420); c.line_to(26, 0); c.close_path(); c.fill()
    c.new_path(); c.move_to(-90, -420); c.line_to(90, -420); c.line_to(72, -500); c.line_to(-72, -500); c.close_path(); c.fill()
    c.set_source_rgba(0.95, 0.75, 0.4, 0.8 * a); c.rectangle(-70, -490, 140, 26); c.fill()
    c.set_source_rgba(*col, a); c.rectangle(-80, -520, 160, 20); c.fill(); c.rectangle(-4, -580, 8, 60); c.fill()
    c.restore()


# =============================================================== SCÈNES
def sc_cc_hook(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        sky_bg(c, t, warm=True, oy=420)
        c.set_source_rgba(0.35, 0.3, 0.25, 0.25); c.paint()
        x = 420 - 50 * p; y = 960 - 30 * p
        P = plane(c, 'side_gear', x, y, 0.30, rot=-0.04)
        dx, dy, L = aft_dir(P)
        lx, ly = P('leak')
        flame(c, lx, ly, dx, dy + 0.05, L * 1.1, 34, t, 1.0, seed=2)
        c.set_source_rgba(0.1, 0.05, 0.02, 0.15); c.paint()
        tag(c, "25 JUILLET 2000 · GONESSE", 540, 1285, WH, ap(p, 0.15, 0.3), 54)
    elif k == 1:
        asphalt(c, t, blur=0, zoom=1.0 + 0.06 * p)
        g = cairo.RadialGradient(540, 900, 200, 540, 900, 1100); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.6); c.set_source(g); c.paint()
        glow(c, 540, 880, 420, (1, 0.85, 0.6), 0.18)
        wear_strip(c, 540, 900, 760 * (1 + 0.05 * p), -0.12, t)
        a = ap(p, 0.2, 0.4)
        c.save(); c.translate(540, 900); c.rotate(-0.12)
        c.move_to(-380, 95); c.line_to(380, 95); c.set_source_rgba(*YEL, a); c.set_line_width(5); c.stroke()
        for xx in (-380, 380): c.move_to(xx, 75); c.line_to(xx, 115); c.stroke()
        c.restore()
        tag(c, "43 CM · TITANE", 540, 1180, YEL, a, 64)
    else:
        runway_axis(c, t, blur=3)
        Z = 320 - 120 * p
        P, sc = on_axis(c, 'front', Z, t)
        nx, ny = P('nose'); glow(c, nx, ny, 60, (1, 0.9, 0.7), 0.25)
        g = cairo.LinearGradient(0, 1040, 0, 1500); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.35); c.rectangle(0, 1040, W, 460); c.set_source(g); c.fill()
        c.save(); c.translate(520, 1190); c.scale(1, 0.32); c.translate(-520, -1190)
        glow(c, 520, 1205, 300, (0, 0, 0), 0.35); wear_strip(c, 520, 1190, 560, 0.04, t); c.restore()
        c.save(); c.translate(520, 1190); c.scale(1, 0.45); c.new_path(); c.arc(0, 0, 330, 0, 7); c.restore(); c.set_source_rgba(*RED, 0.75 * ap(p, 0.1, 0.3)); c.set_line_width(5); c.stroke()

def sc_cc_legend(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        strato_bg(c, t)
        P = plane(c, 'side_up', 560 - 30 * p, 880, 0.36)
        sh = 1 + 0.3 * math.sin(t * 2)
        nx, ny = P('nose')
        for j in range(3):   # cônes de choc supersoniques discrets
            c.new_path(); c.move_to(nx + 30 * j, ny); c.line_to(nx + 330 + 60 * j, ny - 280); c.move_to(nx + 30 * j, ny); c.line_to(nx + 330 + 60 * j, ny + 280)
            c.set_source_rgba(0.7, 0.85, 1, 0.10 - 0.025 * j); c.set_line_width(3); c.stroke()
        m = 2.0 * eout(ap(p, 0.0, 0.5))
        counter(c, f"MACH {m:.1f}".replace('.', ','), "2 × la vitesse du son", 540, 560, CY, 150)
        # route Paris -> New York + chrono 3 h 30
        a = ap(p, 0.35, 0.55)
        panel(c, 150, 1130, 780, 170, 0.55 * a)
        x0, x1, yy = 860, 220, 1240
        q = ap(p, 0.4, 1.0)
        c.new_path(); c.move_to(x0, yy)
        for j in range(1, int(40 * q) + 1):
            uu = j / 40; c.line_to(x0 + (x1 - x0) * uu, yy - 70 * math.sin(math.pi * uu))
        c.set_source_rgba(*YEL, a); c.set_line_width(5); c.stroke()
        for xx, nm in ((x0, "PARIS"), (x1, "NEW YORK")):
            c.new_path(); c.arc(xx, yy, 10, 0, 7); c.set_source_rgba(1, 1, 1, a); c.fill(); letter(c, nm, xx, yy + 46, 36, WH, a)
        hh = 3.5 * q; letter(c, f"{int(hh)} H {int((hh % 1) * 60):02d}", 540, 1215, 58, YEL, a)
    else:
        sx, sy = sky_bg(c, t, oy=160)
        x = 540 - 40 * p
        P = plane(c, 'hero', x, 900, 0.35 + 0.03 * p)
        sun_flare(c, sx, sy, 0.8)
        grade(c)
        tag(c, "1976 – 2000 · AUCUN ACCIDENT MORTEL", 540, 1285, WH, ap(p, 0.1, 0.3), 46)


FLAP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-:· "
def flap_text(c, s, x, y, cw, ch, t, t0, col=(1, 0.86, 0.3)):
    for i, chh in enumerate(s):
        done = t - t0 - i * 0.05
        if done < 0.6:
            r = random.Random(int(t * 30) + i * 7); chh = FLAP[r.randrange(len(FLAP) - 1)]
        xx = x + i * (cw + 6)
        rr(c, xx, y, cw, ch, 6); c.set_source_rgb(0.08, 0.08, 0.09); c.fill()
        c.move_to(xx, y + ch / 2); c.line_to(xx + cw, y + ch / 2); c.set_source_rgba(0, 0, 0, 0.8); c.set_line_width(2); c.stroke()
        letter(c, chh, xx + cw / 2, y + ch * 0.8, ch * 0.82, col)


def sc_cc_flight(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        c.set_source_rgb(0.05, 0.05, 0.06); c.paint()
        glow(c, 540, 820, 700, (0.3, 0.35, 0.45), 0.25)
        letter(c, "DÉPARTS · DEPARTURES", 540, 520, 64, WH)
        letter(c, "ROISSY – CHARLES DE GAULLE", 540, 570, 30, (0.7, 0.75, 0.85), fam='Montserrat')
        t0 = sg['sent'][0][0]
        rows = [("AF4590", "NEW YORK JFK", "CONCORDE"), ("AF1234", "LONDRES", "ROULAGE"), ("AF0456", "TOKYO", "A L'HEURE")]
        for j, (a_, b_, c_) in enumerate(rows):
            yy = 660 + j * 150; hl = (j == 0)
            al = 1.0 if hl else 0.45
            c.save(); c.push_group()
            flap_text(c, a_, 110, yy, 44, 76, t, t0 + 0.2 + j * 0.15)
            flap_text(c, b_[:12], 110 + 6 * 50 + 20, yy, 30, 76, t, t0 + 0.4 + j * 0.15)
            c.pop_group_to_source(); c.paint_with_alpha(al); c.restore()
            if hl:
                letter(c, c_, 540, yy + 130, 40, YEL, ap(t, t0 + 1.5, t0 + 1.9), fam='Bebas Neue')
        letter(c, "25 · 07 · 2000", 540, 1170, 56, WH, ap(p, 0.4, 0.6))
    elif k == 1:
        c.set_source_rgb(0.03, 0.04, 0.07); c.paint()
        P = plane(c, 'top2', 540, 900, 0.50, rot=TOPROT, alpha=0.30)
        nx, ny = P('cockpit'); tx, ty = P('tail')
        n = 100; filled = int(100 * eout(ap(p, 0.05, 0.85)))
        L = math.hypot(tx - nx, ty - ny); ux, uy = (tx - nx) / L, (ty - ny) / L; vx, vy = -uy, ux
        for i in range(n):
            row, col = i // 4, i % 4
            off = (-1.5 + col + (0.35 if col >= 2 else -0.35)) * 15
            d = 60 + row * (L * 0.62 / 25)
            x, y = nx + ux * d + vx * off, ny + uy * d + vy * off
            on = i < filled
            c.save(); c.translate(x, y); c.rotate(math.atan2(uy, ux)); rr(c, -6, -6, 12, 12, 3)
            c.set_source_rgba(*((1.0, 0.8, 0.45) if on else (0.3, 0.32, 0.38)), 0.95 if on else 0.6); c.fill(); c.restore()
            if on and i == filled - 1: glow(c, x, y, 26, (1, 0.8, 0.45), 0.6)
        counter(c, str(filled), "PASSAGERS", 820, 640, (1, 0.8, 0.45), 130)
        letter(c, "+ 9 MEMBRES D'ÉQUIPAGE", 820, 760, 34, WH, ap(p, 0.6, 0.8), fam='Montserrat')
    else:
        g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, 0.02, 0.05, 0.12); g.add_color_stop_rgb(1, 0.03, 0.12, 0.22); c.set_source(g); c.paint()
        for j in range(0, H, 60): c.move_to(0, j); c.line_to(W, j)
        c.set_source_rgba(0.3, 0.6, 1, 0.05); c.set_line_width(1); c.stroke()
        # côtes simplifiées
        eu = [(1000, 640), (930, 700), (900, 820), (950, 900), (1000, 960), (1080, 980), (1080, 600)]
        us = [(0, 760), (120, 780), (160, 840), (140, 960), (90, 1060), (0, 1100)]
        for poly in (eu, us):
            c.new_path(); c.move_to(*poly[0])
            for q in poly[1:]: c.line_to(*q)
            c.close_path(); c.set_source_rgb(0.08, 0.12, 0.16); c.fill_preserve(); c.set_source_rgba(0.4, 0.7, 1, 0.6); c.set_line_width(2.5); c.stroke()
        x0, y0, x1, y1 = 960, 820, 140, 900
        q = ap(p, 0.0, 0.8)
        c.new_path(); c.move_to(x0, y0)
        for j in range(1, int(50 * q) + 1):
            uu = j / 50; c.line_to(x0 + (x1 - x0) * uu, y0 + (y1 - y0) * uu - 260 * math.sin(math.pi * uu))
        c.set_source_rgba(*YEL, 0.9); c.set_line_width(5); c.set_dash([16, 10]); c.stroke(); c.set_dash([])
        letter(c, "PARIS", x0 - 10, y0 + 60, 40, WH); letter(c, "NEW YORK", x1 + 50, y1 + 70, 40, WH)
        letter(c, "OCÉAN ATLANTIQUE", 540, 1000, 40, (0.45, 0.65, 0.85), 0.8)
        a = ap(p, 0.35, 0.6)
        c.save(); c.translate(250, 1050); c.scale(1.2, 1.2)
        c.new_path(); c.move_to(-120, 0); c.line_to(120, 0); c.line_to(95, 32); c.line_to(-110, 32); c.close_path(); c.set_source_rgba(0.92, 0.93, 0.96, a); c.fill()
        c.rectangle(-70, -26, 130, 26); c.fill(); c.rectangle(-40, -46, 70, 20); c.fill(); c.set_source_rgba(0.8, 0.2, 0.2, a); c.rectangle(10, -68, 22, 22); c.fill()
        c.restore()
        tag(c, "UNE CROISIÈRE LES ATTEND", 540, 1285, WH, a, 54)


def sc_cc_dc10(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        yc = runway_side(c, t, 0, ground_y=975)
        q = ap(p, 0.05, 1.0)
        x = 1400 - 1400 * q; y = yc - 75 - 460 * ap(q, 0.45, 1.0) ** 1.4
        dc10_sil(c, x, y, 1.1, -0.14 * ap(q, 0.4, 0.7), 0.9, col=(0.36, 0.39, 0.44))
        glow(c, x + 280, y - 10, 90, (0.9, 0.85, 0.8), 0.25)
        tag(c, "−5 MIN · DC-10 CONTINENTAL", 540, 470, WH, ap(p, 0.05, 0.2), 52)
    else:
        asphalt(c, t, blur=0, zoom=1.15)
        g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgba(0, 0.85, 0.85, 0.82, 0.55); g.add_color_stop_rgba(0.45, 0, 0, 0, 0); c.set_source(g); c.paint()
        q = ap(p, 0.0, 0.55)
        y = 200 + 760 * q ** 1.7
        bounce = ap(p, 0.55, 0.75)
        y = y - 60 * math.sin(math.pi * bounce)
        rot = 2.6 * (1 - q) + 0.15
        if q < 1:
            for j in range(5):                                       # traînées de chute
                c.save(); c.push_group(); wear_strip(c, 560, y - 55 * (j + 1), 520, rot + 0.18 * (j + 1), t, glint=False); c.pop_group_to_source(); c.paint_with_alpha(0.12 - 0.02 * j); c.restore()
        wear_strip(c, 560, y, 520, rot, t)
        if 0.55 < p < 0.75:
            c.new_path(); c.arc(560, 960, 300 * ap(p, 0.55, 0.75), 0, 7); c.set_source_rgba(1, 1, 1, 0.5 * (1 - ap(p, 0.55, 0.75))); c.set_line_width(4); c.stroke()
        tag(c, "LAMELLE MAL FIXÉE · 43 CM", 540, 1285, YEL, ap(p, 0.6, 0.8), 56)

def sc_cc_roll(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        runway_axis(c, t)
        P, sc = on_axis(c, 'front', 650, t)
        nx, ny = P('center'); glow(c, nx, ny, 90, (1, 0.6, 0.3), 0.35)
        letter(c, "16:42", 540, 620, 240, WH, ap(since, 0.0, 0.3))
        letter(c, "HEURE LOCALE", 540, 680, 32, (0.85, 0.85, 0.9), ap(since, 0.2, 0.5), fam='Montserrat')
    elif k == 1:
        runway_axis(c, t)
        q = ap(p, 0.0, 1.0)
        Z = 26 + 50 * q ** 1.6
        P, sc = on_axis(c, 'rear_roll', Z, t)
        reheat(c, P, t, 1.0, L=3.5 * 900 / Z)
        for e in (1, 2, 3, 4):
            ex, ey = P(f'noz{e}'); glow(c, ex, ey, 0.9 * 900 / Z, (1, 0.6, 0.25), 0.5, cairo.OPERATOR_ADD)
        tag(c, "RÉCHAUFFE ALLUMÉE", 540, 1285, ORG, ap(p, 0.15, 0.3), 56)
    else:
        tau = t - sg['sent'][2][0] + 0.1
        off = 700 * tau + 650 * tau * tau
        yc = runway_side(c, t, 700 + 1300 * tau, ground_y=975, off=off)
        P0 = plane(c, 'side_roll', 0, 0, 0.34, alpha=0.0); gx, gy = P0('lgear')
        P = plane(c, 'side_roll', 560 - gx, yc - gy, 0.34, shadow=yc + 6)
        reheat(c, P, t, 1.0, L=150, engines=(1, 2))
        v = int(120 + 130 * ap(p, 0.0, 1.0))
        panel(c, 310, 410, 460, 190, 0.5)
        counter(c, f"{v} KM/H", "186 TONNES EN ACCÉLÉRATION", 540, 520, YEL, 110)

def sc_cc_burst(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    t1 = sg['sent'][1][0]
    slow = (k >= 1)
    tt = t1 + (t - t1) * 0.06 if slow else t
    zs = 2.6
    yc = runway_side(c, tt, 3000, ground_y=1330 - 177 * zs, sc=zs, sky_oy=700)
    sc = 0.34 * zs
    P0 = plane(c, 'side_roll', 0, 0, sc, alpha=0.0); gx, gy = P0('lgear')
    ox, oy = 560 - gx, yc - gy
    P = plane(c, 'side_roll', ox, oy, sc, shadow=yc + 10)
    reheat(c, P, tt, 0.8, L=380, engines=(1, 2))
    wx, wy = P('lgear')
    if k == 0:
        q = ap(p, 0.0, 1.0)
        sx = -250 + (wx + 10 + 250) * q
        wear_strip(c, sx, yc + 12, 180, 0.0, t)
        c.new_path(); c.arc(sx, yc + 12, 120, 0, 7); c.set_source_rgba(*YEL, 0.85); c.set_line_width(5); c.stroke()
        panel(c, 340, 410, 400, 170, 0.5)
        counter(c, f"{int(250 + 80 * ap(p, 0, 1))} KM/H", "VITESSE", 540, 515, YEL, 110)
        return
    st = t - t1
    ex = eout(st / 2.0)
    r = random.Random(4)
    if k == 1:
        fl = max(0, 1 - since / 0.25)
        c.set_source_rgba(1, 0.95, 0.85, 0.85 * fl); c.paint()
    glow(c, wx, wy - 40, 260 * ex + 40, (0.55, 0.52, 0.5), 0.45 * (1 - ex * 0.6))          # poussière / fumée de gomme
    for j2 in range(14):
        a = r.choice((r.uniform(-3.1, -2.3), r.uniform(-0.9, 0.35), r.uniform(2.6, 3.1))); spd = r.uniform(0.35, 1.0); d = 30 + 300 * ex * spd
        px, py = wx + math.cos(a) * d, wy - 30 + math.sin(a) * d * 0.6
        sz = r.uniform(8, 22)
        c.save(); c.translate(px, py); c.rotate(a)
        c.new_path(); c.move_to(-sz, -sz * 0.35)
        for m in range(6):
            an = m / 6 * 6.283; rr_ = sz * r.uniform(0.45, 1.0); c.line_to(math.cos(an) * rr_, math.sin(an) * rr_ * 0.5)
        c.close_path(); c.set_source_rgba(0.05, 0.05, 0.055, 0.95); c.fill()
        c.move_to(-sz * 2.5, 0); c.line_to(-sz * 0.6, 0); c.set_source_rgba(0.05, 0.05, 0.06, 0.35); c.set_line_width(sz * 0.5); c.stroke()
        c.restore()
    if k == 1:
        for j2 in range(18):                                                                   # étincelles
            a = r.uniform(-3.1, 0.0); d = 40 + 380 * ex * r.uniform(0.4, 1.0)
            c.move_to(wx + math.cos(a) * d * 0.7, wy - 40 + math.sin(a) * d * 0.7); c.line_to(wx + math.cos(a) * d, wy - 40 + math.sin(a) * d)
            c.set_source_rgba(1, 0.85, 0.4, 0.9 * (1 - ex)); c.set_line_width(3); c.stroke()
        c.new_path(); c.arc(wx, wy - 40, 60 + 500 * eout(since / 0.6), 0, 7); c.set_source_rgba(1, 1, 1, 0.6 * max(0, 1 - since / 0.6)); c.set_line_width(6); c.stroke()
        stamp(c, "LE PNEU ÉCLATE", 540, 620, 120, RED, since, glow=1.0)
    else:
        ix, iy = P('impact')
        q = ap(p, 0.05, 0.5)
        sx0, sy0 = wx + 10, wy - 60
        fx, fy = sx0 + (ix - sx0) * q, sy0 + (iy - sy0) * q - 60 * math.sin(math.pi * q)
        for m in range(8):                                   # traînée du fragment
            qq = max(0, q - m * 0.03); tx_, ty_ = sx0 + (ix - sx0) * qq, sy0 + (iy - sy0) * qq - 60 * math.sin(math.pi * qq)
            glow(c, tx_, ty_, 30 - 3 * m, (1, 0.75, 0.35), 0.25 * (1 - m / 8))
        if q < 1:
            c.save(); c.translate(fx, fy); c.rotate(t * 7); c.new_path(); c.move_to(-34, -14); c.line_to(30, -20); c.line_to(38, 10); c.line_to(-20, 22); c.close_path()
            c.set_source_rgb(0.04, 0.04, 0.045); c.fill(); c.restore()
        else:
            ff = ap(p, 0.5, 0.9)
            glow(c, ix, iy, 220, (1, 0.9, 0.6), 0.75 * (1 - ff))
            c.new_path(); c.arc(ix, iy, 40 + 260 * ff, 0, 7); c.set_source_rgba(1, 1, 1, 0.7 * (1 - ff)); c.set_line_width(6); c.stroke()
        tag(c, "4,5 KG CONTRE L'AILE", 540, 520, ORG, ap(p, 0.1, 0.25), 58)
    letter(c, "RALENTI ×20", 980, 400, 40, WH, 0.9, anchor='r')

def xray_wing(c, t, P, inten=1.0, tank=1.0, wave=0.0, crack=0.0, jet=0.0, fire=0.0, kevlar=0.0):
    """surimpression rayons X sur la vue de dessus : réservoirs, réservoir 5, train gauche, onde de pression, rupture, jet."""
    tx, ty = P('tank5'); gx, gy = P('lgear_top'); ix, iy = P('impact')
    nx, ny = P('nose'); cx_, cy_ = P('center')
    s = math.hypot(nx - cx_, ny - cy_) / 31.4                  # px par mètre
    ang = math.atan2(cy_ - ny, cx_ - nx)
    c.save(); c.translate(tx, ty); c.rotate(ang)
    w5, h5 = 5.2 * s, 3.0 * s                                   # réservoir 5 (schéma)
    rr(c, -w5 / 2, -h5 / 2, w5, h5, 0.5 * s)
    col = mix(CY, (1.0, 0.45, 0.2), tank)
    c.set_source_rgba(*mix((0.9, 0.7, 0.25), (1, 0.5, 0.15), wave * 0.3), 0.28 + 0.2 * tank); c.fill_preserve()
    c.set_source_rgba(*col, 0.95 * inten); c.set_line_width(max(2, 0.12 * s)); c.stroke()
    if kevlar > 0:
        c.save(); rr(c, -w5 / 2, -h5 / 2, w5, h5, 0.5 * s); c.clip()
        for j in range(-12, 13):
            c.move_to(-w5 / 2 + j * 0.5 * s, -h5 / 2); c.line_to(-w5 / 2 + j * 0.5 * s + h5, h5 / 2)
        c.set_source_rgba(1, 0.85, 0.2, 0.75 * kevlar); c.set_line_width(max(1.5, 0.08 * s)); c.stroke(); c.restore()
    if wave > 0:
        c.save(); rr(c, -w5 / 2, -h5 / 2, w5, h5, 0.5 * s); c.clip()
        for j in range(5):
            ph = (wave * 1.8 + j * 0.2) % 1
            c.new_path(); c.arc(w5 * 0.25, h5 * 0.35, (0.2 + 4.5 * ph) * s, 0, 7); c.set_source_rgba(1, 0.75, 0.35, 0.9 * (1 - ph)); c.set_line_width(max(2, 0.18 * s * (1 - ph))); c.stroke()
        c.restore()
    if crack > 0:
        r = random.Random(3); c.move_to(w5 * 0.3, h5 / 2)
        for j in range(6): c.rel_line_to(r.uniform(-0.5, 0.5) * s, -0.45 * s * crack)
        c.set_source_rgba(1, 1, 1, 0.95); c.set_line_width(max(2, 0.1 * s)); c.stroke()
    c.restore()
    if jet > 0:   # kérosène qui s'échappe vers l'arrière (le long de l'axe)
        dx, dy = math.cos(ang), math.sin(ang)
        jx, jy = tx + dx * 1.2 * s, ty + dy * 1.2 * s
        r = random.Random(7)
        for j in range(140):
            ph = (r.random() + t * 1.4) % 1
            d = ph * 26 * s * jet; off = r.uniform(-1, 1) * (0.4 + 3.0 * ph) * s
            px, py = jx + dx * d - dy * off, jy + dy * d + dx * off
            colj = mix((0.95, 0.85, 0.45), (1.0, 0.45, 0.1), fire) if fire < 0.99 else (1.0, 0.5 + 0.3 * (1 - ph), 0.15)
            glow(c, px, py, (0.25 + 1.2 * ph) * s * (1 + fire), colj, (0.45 if fire else 0.3) * (1 - ph))
    # train gauche
    c.new_path(); c.arc(gx, gy, 0.9 * s, 0, 7); c.set_source_rgba(1, 1, 1, 0.8 * inten); c.set_line_width(max(2, 0.08 * s)); c.stroke()
    return s


TOPROT = math.pi / 2
def xray_base(c, t, P_scale, x=540, y=900, rot=TOPROT, mix_x=1.0, grid=True):
    if grid:
        c.set_source_rgb(0.01, 0.04, 0.08); c.paint()
        for j in range(0, W, 54): c.move_to(j, 0); c.line_to(j, H)
        for j in range(0, H, 54): c.move_to(0, j); c.line_to(W, j)
        c.set_source_rgba(0.3, 0.7, 1, 0.06); c.set_line_width(1); c.stroke()
    P = plane(c, 'top2', x, y, P_scale, rot=rot, alpha=1.0 - mix_x)
    if mix_x > 0:
        plane(c, 'top2', x, y, P_scale, rot=rot, alpha=mix_x, xray=True)
    return P


def sc_cc_tank(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        mx = ap(p, 0.0, 0.6)
        P = xray_base(c, t, 0.50, 540, 860, TOPROT, mx)
        s = xray_wing(c, t, P, inten=mx, tank=0.0)
        ix, iy = P('impact')
        glow(c, ix, iy, 60, (1, 0.9, 0.6), 0.6 * mx)
        check(c, ix + 120, iy - 40, 0.9, GRN, ap(p, 0.4, 0.6))
        tag(c, "PAS DE TROU DANS L'AILE", 540, 1285, GRN, ap(p, 0.3, 0.45), 54)
        letter(c, "RAYONS X", 230, 470, 46, CY, mx)
    else:
        # zoom sur le réservoir 5
        Pz = None
        c.set_source_rgb(0.01, 0.04, 0.08); c.paint()
        base_sc = 0.50
        P0 = plane(c, 'top2', 0, 0, base_sc, rot=TOPROT, alpha=0.0)
        tx, ty = P0('tank5')
        z = 2.4
        for j in range(0, W, 54): c.move_to(j, 0); c.line_to(j, H)
        for j in range(0, H, 54): c.move_to(0, j); c.line_to(W, j)
        c.set_source_rgba(0.3, 0.7, 1, 0.06); c.set_line_width(1); c.stroke()
        c.save(); c.translate(560, 880); c.scale(z, z); c.translate(-tx, -ty)
        P = xray_base(c, t, base_sc, 0, 0, TOPROT, 1.0, grid=False)
        wave = (t - sg['sent'][1][0]) / 2.5 if k == 1 else 0.9
        crack = ap(t, sg['sent'][2][0], sg['sent'][2][0] + 0.8) if k >= 2 else 0
        jet = ap(t, sg['sent'][3][0], sg['sent'][3][0] + 0.6) if k >= 3 else 0
        fire = ap(t, sg['sent'][3][0] + 1.9, sg['sent'][3][0] + 2.2) if k >= 3 else 0
        xray_wing(c, t, P, inten=1.0, tank=0.4 + 0.6 * (k >= 2), wave=wave if k == 1 else (0.6 if k == 2 else 0), crack=crack, jet=jet, fire=fire)
        c.restore()
        if k == 1:
            tag(c, "ONDE DE PRESSION · RÉSERVOIR 5", 540, 1285, ORG, ap(p, 0.1, 0.25), 52)
            letter(c, "KÉROSÈNE", 540, 520, 54, (0.95, 0.8, 0.4), ap(p, 0.3, 0.5))
        elif k == 2:
            stamp(c, "IL CÈDE DE L'INTÉRIEUR", 540, 520, 96, RED, since, glow=1.0)
        else:
            lit = int(75 * (t - sg['sent'][3][0]) / 1.0)
            panel(c, 300, 400, 480, 190, 0.6)
            counter(c, f"{max(0, lit)} L", "75 LITRES / SECONDE", 540, 510, (1.0, 0.75, 0.3), 120)
            if fire > 0: glow(c, 540, 900, 700, (1, 0.5, 0.1), 0.35 * fire); tag(c, "LE KÉROSÈNE S'ENFLAMME", 540, 1285, RED, fire, 56)


def sc_cc_fire(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        runway_axis(c, t)
        Z = 34 + 14 * p
        P, sc = on_axis(c, 'rear_fire', Z, t)
        reheat(c, P, t, 1.0, L=10 * 900 / Z, engines=(3, 4))
        dx, dy, L = aft_dir(P)
        span = 25.6 * 900 / Z
        lx, ly = P('leak')
        g = ap(p, 0.0, 0.25)
        dx, dy = -0.5, 0.86
        flame(c, lx, ly, dx, dy, span * (0.5 + 1.3 * g), span * 0.16, t, 1.0, seed=5, persp=2.6, grow=1.0)
        glow(c, 540, 1150, 700, (1, 0.5, 0.15), 0.2)
    elif k == 1:
        sky_bg(c, t, warm=True, oy=600)
        tile_x(c, 'p_far.png', 0, 1060 - 470, 1.0)
        c.rectangle(0, 1060, W, H); c.set_source_rgb(0.42, 0.5, 0.3); c.fill()
        tower(c, 300, 1060, 1.25, 1.0)
        for j in range(4):
            ph = (t * 1.2 + j / 4) % 1
            c.new_path(); c.arc(300, 1060 - 600, 40 + 400 * ph, -0.6, 0.6); c.set_source_rgba(1, 1, 1, 0.6 * (1 - ph)); c.set_line_width(4); c.stroke()
        P = plane(c, 'side_roll', 790, 1050, 0.11)
        dx, dy, L = aft_dir(P); lx, ly = P('leak')
        flame(c, lx, ly, dx, dy, L * 1.3, 9, t, 1.0, seed=6)
        tag(c, "ALERTE DE LA TOUR", 540, 1285, WH, ap(p, 0.1, 0.25), 56)
    elif k == 2:
        c.set_source_rgb(0.02, 0.02, 0.03); c.paint()
        v = 160 + 32 * ap(p, 0.0, 1.0)
        x0, y0, w, h = 300, 420, 300, 860
        rr(c, x0, y0, w, h, 20); c.set_source_rgb(0.08, 0.08, 0.1); c.fill()
        c.save(); rr(c, x0, y0, w, h, 20); c.clip()
        for kt in range(100, 260, 5):
            yy = y0 + h / 2 - (kt - v) * 9
            if y0 - 20 < yy < y0 + h + 20:
                c.move_to(x0 + w - (40 if kt % 10 == 0 else 22), yy); c.line_to(x0 + w, yy); c.set_source_rgba(1, 1, 1, 0.8); c.set_line_width(3); c.stroke()
                if kt % 20 == 0: letter(c, str(kt), x0 + w - 110, yy + 18, 50, WH, 0.9)
        yv1 = y0 + h / 2 - (150 - v) * 9
        c.rectangle(x0, yv1 - 4, w, 8); c.set_source_rgba(*GRN, 0.95); c.fill(); letter(c, "V1 · 150 KT", x0 + w + 20, yv1 + 14, 44, GRN, 1, anchor='l')
        c.restore()
        c.rectangle(x0 - 10, y0 + h / 2 - 44, w + 20, 88); c.set_source_rgba(0, 0, 0, 0.9); c.fill()
        c.rectangle(x0 - 10, y0 + h / 2 - 44, w + 20, 88); c.set_source_rgb(*YEL); c.set_line_width(4); c.stroke()
        letter(c, f"{int(v)}", x0 + w / 2, y0 + h / 2 + 30, 86, YEL)
        letter(c, "KT", x0 + w + 30, y0 + h / 2 + 18, 44, YEL, 1, anchor='l')
        tag(c, "V1 DÉPASSÉE : PLUS DE FREINAGE", 540, 1360 - 75, RED, ap(p, 0.25, 0.4), 52)
    else:
        q = ap(t, sg['sent'][3][0] - 0.1, sg['end'])
        yc = runway_side(c, t, 2600, ground_y=975 + 300 * q)
        P0 = plane(c, 'side_gear', 0, 0, 0.40, alpha=0.0); gx, gy = P0('lgear')
        P = plane(c, 'side_gear', 520 - gx, 1150 - gy - 20 * q, 0.40, shadow=yc + 6)
        reheat(c, P, t, 0.9, L=160, engines=(3, 4))
        dx, dy, L = aft_dir(P); lx, ly = P('leak')
        flame(c, lx, ly, dx, dy, L * 1.2, 46, t, 1.0, seed=8)


def gauge_r(c, x, y, r, v, label_, t, dead=False, a=1.0):
    c.new_path(); c.arc(x, y, r + 14, 0, 7); g = cairo.LinearGradient(x, y - r, x, y + r); g.add_color_stop_rgb(0, 0.32, 0.33, 0.36); g.add_color_stop_rgb(1, 0.1, 0.1, 0.12); c.set_source(g); c.fill()
    c.new_path(); c.arc(x, y, r, 0, 7); c.set_source_rgb(0.03, 0.03, 0.04); c.fill()
    for j in range(11):
        an = math.radians(135 + 27 * j)
        c.move_to(x + math.cos(an) * r * 0.82, y + math.sin(an) * r * 0.82); c.line_to(x + math.cos(an) * r * 0.95, y + math.sin(an) * r * 0.95)
        c.set_source_rgba(1, 1, 1, 0.85); c.set_line_width(3); c.stroke()
    c.new_path(); c.arc(x, y, r * 0.88, math.radians(135 + 27 * 9), math.radians(135 + 270)); c.set_source_rgba(*RED, 0.8); c.set_line_width(6); c.stroke()
    an = math.radians(135 + 270 * v)
    c.move_to(x, y); c.line_to(x + math.cos(an) * r * 0.8, y + math.sin(an) * r * 0.8); c.set_source_rgb(1, 0.95, 0.85); c.set_line_width(6); c.set_line_cap(1); c.stroke()
    c.new_path(); c.arc(x, y, 9, 0, 7); c.set_source_rgb(0.6, 0.6, 0.62); c.fill()
    letter(c, label_, x, y + r + 60, 36, (0.85, 0.85, 0.9))
    if dead:
        c.new_path(); c.arc(x, y, r + 14, 0, 7); c.set_source_rgba(*RED, 0.25 + 0.15 * math.sin(t * 8)); c.fill()


def sc_cc_engines(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k <= 1:
        c.set_source_rgb(0.05, 0.05, 0.06); c.paint()
        glow(c, 540, 880, 650, (0.4, 0.35, 0.3), 0.2)
        letter(c, "POUSSÉE DES MOTEURS", 540, 520, 56, WH)
        t1 = sg['sent'][0][0]; t2 = sg['sent'][1][0]
        for j in range(4):
            x = 195 + j * 230
            base = 0.93 + 0.01 * math.sin(t * 5 + j)
            if j < 2:
                v = base - 0.6 * ap(t, t1 + 0.4 + 0.3 * j, t1 + 1.4 + 0.3 * j) + 0.05 * math.sin(t * 13 + j) * ap(t, t1, t1 + 1)
                if j == 1: v = v * (1 - ap(t, t2 + 0.2, t2 + 0.9))
            else: v = base
            gauge_r(c, x, 860, 88, max(0.02, v), f"MOTEUR {j + 1}", t, dead=(j < 2 and t > t1 + 0.8))
        if k == 1:
            stamp(c, "MOTEUR 2 COUPÉ", 540, 1200, 100, RED, since, glow=1.0)
        else:
            tag(c, "MOTEURS 1 ET 2 : PERTE DE POUSSÉE", 540, 1180, RED, ap(p, 0.3, 0.5), 50)
    else:
        sky_bg(c, t, warm=True, oy=300)
        sc = 0.9
        P0 = plane(c, 'side_gear', 0, 0, sc, alpha=0)
        gx, gy = P0('lgear')
        P = plane(c, 'side_gear', 560 - gx, 1000 - gy, sc)
        dx, dy, L = aft_dir(P); lx, ly = P('leak')
        flame(c, lx, ly, dx, dy, L * 0.9, 90, t, 1.0, seed=9)
        wx, wy = P('lgear')
        c.new_path(); c.arc(wx, wy - 20, 170 + 6 * math.sin(t * 6), 0, 7); c.set_source_rgba(*RED, 0.9); c.set_line_width(7); c.stroke()
        panel(c, 300, 400, 480, 150, 0.6)
        letter(c, "TRAIN : BLOQUÉ", 540, 495, 80, RED)


def sc_cc_struggle(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        sky_bg(c, t, warm=True, oy=500)
        tile_x(c, 'p_fields.png', t * 900, 1180, 1.0, mb=18)
        g = cairo.LinearGradient(0, 1150, 0, 1300); g.add_color_stop_rgba(0, 0.86, 0.83, 0.77, 0.9); g.add_color_stop_rgba(1, 0.86, 0.83, 0.77, 0); c.rectangle(0, 1150, W, 150); c.set_source(g); c.fill()
        bob = 8 * math.sin(t * 1.4)
        P = plane(c, 'side_gear', 600, 860 + bob, 0.36, rot=0.03)
        dx, dy, L = aft_dir(P); lx, ly = P('leak')
        flame(c, lx, ly, dx, dy, L * 1.25, 38, t, 1.0, seed=11)
        c.move_to(110, 1080); c.line_to(110, 1180); c.set_source_rgba(1, 1, 1, 0.8); c.set_line_width(4); c.stroke()
        letter(c, "60 M", 140, 1140, 64, YEL, ap(p, 0.1, 0.3), anchor='l')
        panel(c, 300, 400, 480, 160, 0.5)
        counter(c, "≈ 370 KM/H", "IMPOSSIBLE D'ACCÉLÉRER", 540, 500, YEL, 100)
    else:
        c.set_source_rgb(0.05, 0.07, 0.07); c.paint()
        r = random.Random(3)
        for _ in range(260):
            x = r.random() * W; y = 380 + r.random() * 1000; c.rectangle(x, y, 6 + 26 * r.random(), 6 + 26 * r.random()); c.set_source_rgba(0.2, 0.24, 0.24, 0.6); c.fill()
        for j in range(2):   # pistes de Roissy (doublet nord, 26 droite)
            c.save(); c.translate(820, 640 + j * 60); c.rotate(-0.07); rr(c, -200, -9, 400, 18, 6); c.set_source_rgb(0.55, 0.57, 0.6); c.fill(); c.restore()
        letter(c, "ROISSY-CDG", 820, 580, 44, WH)
        c.save(); c.translate(250, 1180); c.rotate(-0.5); rr(c, -150, -8, 300, 16, 5); c.set_source_rgb(0.55, 0.57, 0.6); c.fill(); c.restore()
        letter(c, "LE BOURGET", 250, 1280, 44, WH)
        gx, gy = 330, 1010
        c.new_path(); c.arc(gx, gy, 70, 0, 7); c.set_source_rgba(0.6, 0.62, 0.66, 0.25); c.fill(); letter(c, "GONESSE", gx - 10, gy - 90, 40, WH)
        p0 = (1010, 690); pc = (620, 760); p1 = (gx + 20, gy - 10)
        q = ap(p, 0.0, 0.9); n = 50
        c.new_path(); c.move_to(*p0)
        for j in range(1, int(n * q) + 1):
            uu = j / n; c.line_to((1 - uu) ** 2 * p0[0] + 2 * (1 - uu) * uu * pc[0] + uu * uu * p1[0], (1 - uu) ** 2 * p0[1] + 2 * (1 - uu) * uu * pc[1] + uu * uu * p1[1])
        c.set_source_rgba(1, 0.5, 0.3, 0.95); c.set_line_width(6); c.set_dash([16, 10]); c.stroke(); c.set_dash([])
        uu = q; hx = (1 - uu) ** 2 * p0[0] + 2 * (1 - uu) * uu * pc[0] + uu * uu * p1[0]; hy = (1 - uu) ** 2 * p0[1] + 2 * (1 - uu) * uu * pc[1] + uu * uu * p1[1]
        glow(c, hx, hy, 50, (1, 0.5, 0.15), 0.9)
        c.move_to(hx, hy); c.line_to(250, 1180); c.set_source_rgba(1, 1, 1, 0.35); c.set_line_width(3); c.set_dash([6, 8]); c.stroke(); c.set_dash([])
        tag(c, "OBJECTIF : LE BOURGET", 540, 470, WH, ap(p, 0.1, 0.3), 54)
        letter(c, "schéma simplifié", 880, 1330, 26, (0.6, 0.65, 0.7), fam='Montserrat')


def sc_cc_crash(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        sky_bg(c, t, warm=True, oy=700)
        tile_x(c, 'p_far.png', 0, 1150 - 470, 1.0)
        c.rectangle(0, 1150, W, H); c.set_source_rgb(0.4, 0.46, 0.3); c.fill()
        q = ap(p, 0.0, 0.85)
        x = 760 - 420 * q; y = 760 + 360 * q ** 1.8
        rot = -0.15 * q
        if q < 0.97:
            c.save(); c.rectangle(0, 0, W, 1135); c.clip()
            P = plane(c, 'bank', x, y, 0.13 + 0.01 * q, rot=rot, dark=0.15)
            dx, dy, L = aft_dir(P); lx, ly = P('leak')
            flame(c, lx, ly, dx, dy, L * 1.2, 12, t, 0.8, seed=12)
            c.restore()
        if p > 0.82:
            smoke_col(c, 360, 1140, 900 * ap(p, 0.82, 1.0) + 50, t, 1.0)
        c.set_source_rgba(0.1, 0.08, 0.06, 0.25 * ap(p, 0.8, 1.0)); c.paint()
    elif k == 1:
        c.set_source_rgb(0.0, 0.0, 0.0); c.paint()
        letter(c, "16:44", 540, 900, 200, (0.92, 0.93, 0.96), min(1, since / 0.6))
    else:
        c.set_source_rgb(0.0, 0.0, 0.01); c.paint()
        r = random.Random(113)
        n = int(113 * min(1, since / 1.8))
        for j in range(n):
            x = 150 + r.random() * 780; y = 1000 + r.gauss(0, 60) - (t * 12 * (0.3 + r.random())) % 140
            glow(c, x, y, 16, (1, 0.8, 0.45), 0.55); c.new_path(); c.arc(x, y, 2.4, 0, 7); c.set_source_rgba(1, 0.93, 0.75, 0.95); c.fill()
        letter(c, "113 VICTIMES", 540, 700, 120, (0.93, 0.94, 0.97), min(1, since / 0.8))
        letter(c, "109 à bord · 4 au sol", 540, 780, 44, (0.72, 0.74, 0.8), min(1, max(0, since - 0.5) / 0.8), fam='Montserrat')


CHAIN = ["LAMELLE", "PNEU", "RÉSERVOIR 5", "INCENDIE", "MOTEURS"]
def sc_cc_after(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        c.set_source_rgb(0.02, 0.04, 0.07); c.paint()
        letter(c, "LA CHAÎNE DE L'ACCIDENT", 540, 470, 60, WH)
        letter(c, "selon l'enquête du BEA", 540, 520, 30, (0.6, 0.75, 0.9), 1, fam='Montserrat')
        for j, nm in enumerate(CHAIN):
            a = ap(t, sg['sent'][0][0] + 0.3 * j, sg['sent'][0][0] + 0.3 * j + 0.3)
            y = 600 + j * 135
            rr(c, 290, y - 50, 500, 96, 48); c.set_source_rgba(0.06, 0.12, 0.18, a); c.fill_preserve(); c.set_source_rgba(*CY, a); c.set_line_width(4); c.stroke()
            letter(c, nm, 540, y + 18, 54, WH, a)
            if j < len(CHAIN) - 1:
                for m in range(2):
                    c.save(); c.translate(540, y + 58 + m * 20); rr(c, -12, -12, 24, 24, 10); c.set_source_rgba(*CY, a); c.set_line_width(4); c.stroke(); c.restore()
    elif k == 1:
        P = xray_base(c, t, 0.50, 540, 860, TOPROT, 1.0)
        xray_wing(c, t, P, inten=1.0, tank=0.0, kevlar=ap(p, 0.05, 0.4))
        tx, ty = P('tank5')
        tag(c, "KEVLAR DANS LES RÉSERVOIRS", 540, 470, YEL, ap(p, 0.1, 0.3), 52)
        tag(c, "+ PNEUS RENFORCÉS", 540, 1285, WH, ap(p, 0.5, 0.65), 54)
    else:
        sx, sy = sky_bg(c, t, oy=160)
        P = plane(c, 'hero', 560 - 50 * p, 920 - 30 * p, 0.35)
        sun_flare(c, sx, sy, 0.8)
        tag(c, "NOVEMBRE 2001 : IL REVOLE", 540, 1285, GRN, ap(p, 0.1, 0.3), 56)


def scales(c, x, y, s, tilt, a=1.0, col=(0.92, 0.82, 0.55)):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgba(*col, a)
    c.rectangle(-8, -300, 16, 300); c.fill(); c.rectangle(-120, 0, 240, 20); c.fill()
    c.save(); c.translate(0, -290); c.rotate(tilt)
    c.rectangle(-230, -6, 460, 12); c.fill()
    for sx in (-210, 210):
        c.move_to(sx, 0); c.line_to(sx - 60, 140); c.move_to(sx, 0); c.line_to(sx + 60, 140); c.set_line_width(3); c.stroke()
        c.save(); c.translate(sx, 140); c.rotate(-tilt); c.new_path(); c.arc(0, 0, 80, 0, math.pi); c.fill(); c.restore()
    c.restore(); c.restore()


def sc_cc_justice(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    c.set_source_rgb(0.05, 0.04, 0.03); c.paint(); glow(c, 540, 800, 700, (0.9, 0.7, 0.4), 0.18)
    if k == 0:
        scales(c, 540, 1000, 1.1, 0.18 * math.sin(min(1, since) * 2.2) * (1 - 0.3 * since / 3))
        tag(c, "PONTOISE · DÉCEMBRE 2010", 540, 470, WH, ap(p, 0.05, 0.2), 54)
        stamp(c, "CONTINENTAL CONDAMNÉE", 540, 1200, 84, RED, since - 0.6, glow=0.8)
    else:
        tag(c, "COUR D'APPEL DE VERSAILLES · 2012", 540, 470, WH, ap(p, 0.05, 0.2), 50)
        for j, (h, v, col) in enumerate((("PÉNAL", "RELAXÉE", GRN), ("CIVIL", "RESPONSABLE", RED))):
            a = ap(p, 0.15 + 0.3 * j, 0.3 + 0.3 * j)
            y = 680 + j * 300
            panel(c, 170, y - 110, 740, 220, 0.7 * a)
            rr(c, 170, y - 110, 740, 220, 26); c.set_source_rgba(*col, 0.8 * a); c.set_line_width(4); c.stroke()
            letter(c, h, 540, y - 30, 48, (0.85, 0.85, 0.9), a, fam='Montserrat')
            letter(c, v, 540, y + 60, 100, col, a)


def sc_cc_end(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        sky_bg(c, t, warm=True, oy=900)
        g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgba(0, 0.2, 0.08, 0.25, 0.45); g.add_color_stop_rgba(0.6, 1.0, 0.45, 0.15, 0.35); g.add_color_stop_rgba(1, 0.3, 0.1, 0.05, 0.5)
        c.set_source(g); c.paint()
        glow(c, 780, 1080, 520, (1, 0.6, 0.25), 0.7); glow(c, 780, 1080, 120, (1, 0.95, 0.8), 0.9)
        P = plane(c, 'sunset', 520 - 60 * p, 860 - 20 * p, 0.34)
        tag(c, "1976 – 2003", 540, 1285, WH, ap(p, 0.1, 0.3), 60)
    elif k == 1:
        c.set_source_rgb(0.03, 0.04, 0.07); c.paint()
        letter(c, "VITESSE DE CROISIÈRE", 540, 500, 56, WH)
        for j, (nm, m, col) in enumerate((("CONCORDE", 2.02, CY), ("AVIONS DE LIGNE ACTUELS", 0.85, (0.8, 0.82, 0.88)))):
            y = 680 + j * 260
            a = ap(p, 0.1 + 0.25 * j, 0.3 + 0.25 * j)
            letter(c, nm, 120, y - 30, 44, WH, a, fam='Montserrat', anchor='l')
            wv = 840 * (m / 2.1) * eout(ap(p, 0.15 + 0.25 * j, 0.55 + 0.25 * j))
            rr(c, 120, y, 840, 70, 35); c.set_source_rgba(1, 1, 1, 0.08 * a); c.fill()
            rr(c, 120, y, max(70, wv), 70, 35); c.set_source_rgba(*col, 0.95 * a); c.fill()
            letter(c, f"MACH {m:.2f}".replace('.', ',').replace(',00', ''), 140 + max(70, wv) + 20 if wv < 600 else 120 + wv - 20, y + 54, 54,
                   WH if wv < 600 else (0.02, 0.05, 0.1), a, anchor='l' if wv < 600 else 'r')
    else:
        sky_bg(c, t, warm=True, oy=900)
        g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgba(0, 0.2, 0.08, 0.25, 0.45); g.add_color_stop_rgba(0.6, 1.0, 0.45, 0.15, 0.35); g.add_color_stop_rgba(1, 0.3, 0.1, 0.05, 0.5)
        c.set_source(g); c.paint()
        glow(c, 780, 1080, 520, (1, 0.6, 0.25), 0.7); glow(c, 780, 1080, 120, (1, 0.95, 0.8), 0.9)
        lt2 = t - sg['sent'][2][0]
        P = plane(c, 'sunset', 440 + 18 * lt2, 860 - 4 * lt2, max(0.12, 0.34 - 0.012 * lt2))
        stamp(c, "ET TOI ?", 540, 560, 150, ORG, since, glow=1.0)


SC10 = {k[3:]: v for k, v in globals().items() if k.startswith('sc_') and callable(v)}
