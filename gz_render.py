"""« Combien de G peut encaisser un humain ? » — escalade 1 G → 46,2 G (sans voix).
Usage : python3 gz_render.py [stills t1 ...]  -> gz/video_noaudio.mp4 + gz/tl.json"""
import cairo, json, math, os, random, subprocess, sys
import numpy as np
from PIL import Image, ImageFilter

W, H, FPS = 1080, 1920, 30
OUT = 'gz/'
YEL = (1.0, 0.84, 0.1); RED = (1.0, 0.28, 0.25); WHITE = (1, 1, 1); CYA = (0.4, 0.85, 1.0)

# (t0, G, titre, sous-titre, pose)
ST = [
    (0.0, 1.0, None, None, 'neutral'),
    (3.6, 1.0, "TOI, SUR TON CANAPÉ", "Tout va bien.", 'neutral'),
    (9.0, 1.2, "VIRAGE D'UN AVION DE LIGNE", "Tu le sens à peine.", 'wink_thumb'),
    (14.0, 4.0, "MONTAGNES RUSSES", "Jusqu'à 4 G, quelques secondes.", 'laugh'),
    (21.0, 5.0, "VOILE GRIS", "Le sang quitte ta tête : les couleurs disparaissent.", 'shocked'),
    (28.0, 6.0, "VOILE NOIR", "Sans entraînement… tu t'évanouis.", 'skeptical'),
    (35.5, 9.0, "PILOTE DE RAFALE", "Combinaison anti-G + respiration spéciale.", 'helmet'),
    (44.5, 12.0, "ÉJECTION", "Plus de 12 G… en une fraction de seconde.", 'panic'),
    (50.5, 46.2, "RECORD HUMAIN", "John Stapp, 1954, sur un traîneau-fusée.", 'shocked'),
    (62.0, 46.2, None, None, 'salute'),
]
TOTAL = 68.0
json.dump(dict(st=[(s[0], s[1]) for s in ST], total=TOTAL), open(OUT + 'tl.json', 'w'))


def stage(t):
    i = max(k for k, s in enumerate(ST) if s[0] <= t); return i, ST[i]


def G_at(t):
    i, s = stage(t)
    prev = ST[i - 1][1] if i else 1.0
    u = min(1, (t - s[0]) / (1.6 if s[1] < 20 else 6.0))
    u = u * u * (3 - 2 * u)
    g = prev + (s[1] - prev) * u
    if 44.5 <= t < 50.5:  # éjection : pic bref puis retour
        lt = t - 44.5; g = 1 + 11 * math.exp(-((lt - 1.2) / 0.35) ** 2) if lt < 3 else 1.0
    return g


def ease(u):
    u = min(max(u, 0), 1); return u * u * (3 - 2 * u)


def ease_out(u):
    u = min(max(u, 0), 1); return 1 - (1 - u) ** 3


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
    c.new_sub_path(); c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2); c.close_path()


def pil_to_surface(im):
    im = im.convert('RGBA'); a = np.asarray(im).astype(np.float32) / 255.0
    rgb = a[..., :3] * a[..., 3:4]; bgra = np.dstack([rgb[..., 2], rgb[..., 1], rgb[..., 0], a[..., 3]]) * 255
    h, w = im.height, im.width; stride = cairo.ImageSurface.format_stride_for_width(cairo.FORMAT_ARGB32, w)
    buf = np.zeros((h, stride // 4, 4), np.uint8); buf[:, :w] = bgra.astype(np.uint8)
    return cairo.ImageSurface.create_for_data(buf, cairo.FORMAT_ARGB32, w, h, stride), buf


# ---------- sprites ----------
REAR = Image.open('gz/rear.png').convert('RGBA'); REAR = REAR.crop(REAR.getbbox())
REAR_S, _rb = pil_to_surface(REAR)
MDIR = 'mascot/stickers/'
_STK = {}


def sticker(pose):
    if pose not in _STK:
        im = Image.open(MDIR + pose + '.png').convert('RGBA'); _STK[pose] = im.resize((720, 720), Image.LANCZOS)
    return _STK[pose]


_WC = {}


def warped(pose, g):
    """Visage qui « fond » sous les G (warp en maillage)."""
    k = round(min(max(g - 1, 0), 8) * 4) / 4
    key = (pose, k)
    if key in _WC: return _WC[key]
    im = sticker(pose); w, h = im.size
    if k == 0:
        _WC[key] = pil_to_surface(im); return _WC[key]
    A = 20.0 * k           # px d'affaissement max
    n = 12; mesh = []
    def src(x, y):
        yn = y / h; xn = x / w
        bell = math.exp(-((yn - 0.55) / 0.2) ** 2)          # joues / mâchoire
        cheek = 0.55 + 0.45 * math.exp(-((abs(xn - 0.5) - 0.13) / 0.09) ** 2)
        squash = (1 - yn) * 0.02 * k * h                   # le crâne s'écrase vers le bas
        return x, y - A * bell * cheek - squash
    for i in range(n):
        for j in range(n):
            x0, x1 = w * i / n, w * (i + 1) / n; y0, y1 = h * j / n, h * (j + 1) / n
            q = src(x0, y0) + src(x0, y1) + src(x1, y1) + src(x1, y0)
            mesh.append(((int(x0), int(y0), int(x1), int(y1)), q))
    out = im.transform((w, h), Image.MESH, mesh, Image.BICUBIC)
    _WC[key] = pil_to_surface(out); return _WC[key]


# ---------- décor ----------
CLOUDS = [(random.Random(i).uniform(-1, 1), random.Random(i + 50).uniform(0.05, 1), random.Random(i + 99).uniform(40, 120)) for i in range(26)]


def sky_window(c, t, g, x0=40, y0=470, w=1000, h=600):
    c.save(); rrect(c, x0, y0, w, h, 36); c.clip()
    cx, cy = x0 + w / 2, y0 + h / 2
    bank = math.acos(1 / max(1.0, g)) if t < 44.5 else 0.0
    bank = min(bank, math.radians(84))
    c.save(); c.translate(cx, cy + 60); c.rotate(-bank)
    gs = cairo.LinearGradient(0, -900, 0, 0); gs.add_color_stop_rgb(0, 0.10, 0.28, 0.60); gs.add_color_stop_rgb(1, 0.55, 0.75, 0.95)
    c.rectangle(-1400, -1400, 2800, 1400); c.set_source(gs); c.fill()
    gg = cairo.LinearGradient(0, 0, 0, 900); gg.add_color_stop_rgb(0, 0.42, 0.52, 0.38); gg.add_color_stop_rgb(1, 0.18, 0.26, 0.16)
    c.rectangle(-1400, 0, 2800, 1400); c.set_source(gg); c.fill()
    # champs au sol (défilent)
    sp = 40 + 60 * g
    for k in range(18):
        xx = ((k * 173 - t * sp * 2) % 2800) - 1400; yy = 30 + (k * 53) % 260
        c.set_source_rgba(0.3 + 0.05 * (k % 3), 0.4, 0.25, 0.6); c.rectangle(xx, yy, 160, 40 + (k % 4) * 20); c.fill()
    for (u, v, r) in CLOUDS:
        xx = ((u * 1400 - t * sp * 3 * (0.6 + v)) % 2800) - 1400; yy = -40 - v * 600
        c.set_source_rgba(1, 1, 1, 0.75); c.arc(xx, yy, r, 0, 2 * math.pi); c.arc(xx + r, yy + 10, r * 0.8, 0, 2 * math.pi); c.arc(xx - r, yy + 12, r * 0.7, 0, 2 * math.pi); c.fill()
    c.restore()
    # lignes de vitesse
    if g > 2:
        rr = random.Random(int(t * 20))
        for k in range(int(6 * g)):
            a = rr.uniform(0, 2 * math.pi); r1 = rr.uniform(260, 600); L = 40 + 12 * g
            c.move_to(cx + math.cos(a) * r1, cy + math.sin(a) * r1); c.line_to(cx + math.cos(a) * (r1 + L), cy + math.sin(a) * (r1 + L))
            c.set_source_rgba(1, 1, 1, 0.25); c.set_line_width(3); c.stroke()
    # Rafale vu de derrière (caméra accrochée à l'avion : il reste droit, l'horizon tourne)
    if t < 44.5 or t < 45.7:
        s = 760 / REAR.width; px, py = cx, cy + 40 + 4 * math.sin(t * 2)
        if 44.5 <= t: py += 600 * ease((t - 45.2) / 0.5)
        c.save(); c.translate(px, py); c.scale(s, s); c.translate(-REAR.width / 2, -REAR.height / 2)
        c.set_source_surface(REAR_S, 0, 0); c.paint(); c.restore()
        if g > 2.5 and t < 44.5:           # condensation : traînées de bout d'aile + nuage sur l'extrados
            f = min(1, (g - 2.5) / 3)
            for sgn in (-1, 1):
                ex, ey = px + sgn * 0.47 * 760, py + 0.06 * 760
                for k in range(10):
                    c.move_to(ex, ey); c.curve_to(ex + sgn * 10, ey + 60, ex - sgn * 20 * k * 0.1, ey + 200, ex - sgn * 10, ey + 400)
                c.set_source_rgba(1, 1, 1, 0.5 * f); c.set_line_width(5); c.stroke()
                g2 = cairo.RadialGradient(px + sgn * 150, py - 10, 5, px + sgn * 150, py - 10, 170)
                g2.add_color_stop_rgba(0, 1, 1, 1, 0.55 * f * (0.8 + 0.2 * math.sin(t * 13 + sgn))); g2.add_color_stop_rgba(1, 1, 1, 1, 0)
                c.set_source(g2); c.arc(px + sgn * 150, py - 10, 170, 0, 2 * math.pi); c.fill()
    if 44.5 <= t < 50.5:                  # éjection : siège + flamme qui monte
        lt = t - 44.5
        if lt > 0.9:
            sy = cy + 40 - 380 * ease_out((lt - 0.9) / 1.8)
            c.set_source_rgba(1, 0.6, 0.1, 0.9); c.move_to(cx - 18, sy + 60); c.line_to(cx, sy + 60 + 120 + 30 * math.sin(t * 40)); c.line_to(cx + 18, sy + 60); c.fill()
            rrect(c, cx - 35, sy - 60, 70, 120, 12); c.set_source_rgba(0.2, 0.22, 0.25, 1); c.fill()
            c.set_source_rgba(0.95, 0.85, 0.75, 1); c.arc(cx, sy - 80, 22, 0, 2 * math.pi); c.fill()
        if 0.9 < lt < 1.1:
            c.set_source_rgba(1, 1, 1, 1 - (lt - 0.9) / 0.2); c.paint()
        if lt > 2.5:                        # parachute
            a = ease((lt - 2.5) / 0.8); pyc = cy - 120
            c.save(); c.translate(cx, pyc); c.scale(1, 0.55)
            c.arc(0, 0, 180 * a, math.pi, 2 * math.pi); c.restore()
            c.set_source_rgba(1, 0.45, 0.2, a); c.fill()
            for sx in (-170, -60, 60, 170):
                c.move_to(cx + sx * a, pyc); c.line_to(cx, pyc + 200 * a); c.set_source_rgba(1, 1, 1, 0.6 * a); c.set_line_width(2); c.stroke()
            c.set_source_rgba(0.95, 0.85, 0.75, a); c.arc(cx, pyc + 215 * a, 18, 0, 2 * math.pi); c.fill()
    if t >= 50.5:                         # traîneau-fusée sur rails, désert
        lt = t - 50.5
        c.set_source_rgb(0.85, 0.72, 0.5); c.rectangle(x0, cy + 80, w, h); c.fill()
        c.set_source_rgb(0.95, 0.7, 0.45); c.rectangle(x0, y0, w, cy + 80 - y0); c.fill()
        g3 = cairo.LinearGradient(0, y0, 0, cy + 80); g3.add_color_stop_rgba(0, 0.35, 0.55, 0.85, 1); g3.add_color_stop_rgba(1, 0.95, 0.75, 0.5, 1)
        c.rectangle(x0, y0, w, cy + 80 - y0); c.set_source(g3); c.fill()
        c.set_source_rgb(0.35, 0.3, 0.28)
        for yy in (cy + 150, cy + 175): c.rectangle(x0, yy, w, 6); c.fill()
        for k in range(30):
            xx = ((k * 70 - lt * 2500) % 2100) - 50
            c.rectangle(xx, cy + 145, 10, 40); c.fill()
        u = min(1, lt / 2.5); sx = x0 - 300 + (w / 2 + 300) * ease_out(u) if lt < 4 else x0 + w / 2
        if lt > 4: sx = x0 + w / 2 + 900 * ease((lt - 4) / 1.5) ** 2 * 0
        # flamme / traînée
        c.set_source_rgba(1, 0.55, 0.1, 0.9)
        c.move_to(sx - 80, cy + 110); c.line_to(sx - 260 - 40 * math.sin(t * 50), cy + 130); c.line_to(sx - 80, cy + 150); c.fill()
        c.set_source_rgba(1, 0.9, 0.5, 0.9); c.move_to(sx - 80, cy + 118); c.line_to(sx - 170, cy + 130); c.line_to(sx - 80, cy + 142); c.fill()
        for k in range(8):
            dx = sx - 300 - k * 90 - (lt * 400) % 90; r_ = 30 + k * 12
            c.set_source_rgba(0.92, 0.82, 0.65, 0.5 * (1 - k / 8)); c.arc(dx, cy + 160 - k * 6, r_, 0, 2 * math.pi); c.fill()
        rrect(c, sx - 90, cy + 90, 200, 70, 14); c.set_source_rgb(0.75, 0.15, 0.12); c.fill()
        c.set_source_rgb(0.15, 0.15, 0.18); c.rectangle(sx + 20, cy + 50, 40, 45); c.fill()
        c.set_source_rgb(0.95, 0.85, 0.75); c.arc(sx + 40, cy + 40, 18, 0, 2 * math.pi); c.fill()
        for k in range(14):
            yy = y0 + 40 + k * 40; xx = ((k * 211 - lt * 3000) % (w + 200)) + x0 - 100
            c.set_source_rgba(1, 1, 1, 0.35); c.rectangle(xx, yy, 120, 3); c.fill()
        if lt > 1.5:
            text_c(c, "1 000 km/h à 0 en 1,4 s", cx, y0 + 90, 46, (1, 1, 1, ease_out((lt - 1.5) / 0.4)), stroke=7)
    c.restore()
    rrect(c, x0, y0, w, h, 36); c.set_source_rgba(1, 1, 1, 0.25); c.set_line_width(4); c.stroke()


def g_hud(c, t, g):
    i, s = stage(t)
    if t < ST[1][0]:
        u = ease_out(t / 0.5)
        text_c(c, "COMBIEN DE G", W / 2, 200, 96, (1, 1, 1, u), stroke=11)
        text_c(c, "PEUT ENCAISSER UN HUMAIN ?", W / 2, 300, 60, (*YEL, u), stroke=8, maxw=1000)
        return
    if t >= ST[-1][0]: return
    gtxt = f"{g:.1f}".replace('.', ',') + " G"
    age = t - s[0]; k = 1 + 0.25 * max(0, 1 - age / 0.25)
    col = YEL if g < 4.5 else (RED if g < 9.5 else (1, 0.55, 0.15))
    c.save(); c.translate(W / 2, 215); c.scale(k, k); text_c(c, gtxt, 0, 0, 170, (*col, 1), stroke=16); c.restore()
    if s[2]:
        a = ease_out(age / 0.3)
        text_c(c, s[2], W / 2, 315, 60, (1, 1, 1, a), stroke=8, maxw=1000)
        text_c(c, s[3], W / 2, 390, 38, (0.88, 0.9, 0.95, a), stroke=6, maxw=1000)


def g_bar(c, t, g):
    """Jauge verticale à gauche (échelle log jusqu'à 50 G)."""
    if t < ST[1][0] or t >= ST[-1][0]: return
    x, y0, y1 = 70, 1880, 1120
    rrect(c, x - 22, y1 - 10, 44, y0 - y1 + 20, 22); c.set_source_rgba(0, 0, 0, 0.45); c.fill()
    f = math.log(max(g, 1)) / math.log(50); yy = y0 - (y0 - y1) * f
    gr = cairo.LinearGradient(0, y0, 0, y1); gr.add_color_stop_rgb(0, 0.2, 0.85, 0.4); gr.add_color_stop_rgb(0.45, 1, 0.84, 0.1); gr.add_color_stop_rgb(0.62, 1, 0.3, 0.25); gr.add_color_stop_rgb(1, 0.6, 0.1, 0.9)
    rrect(c, x - 14, yy, 28, y0 - yy, 14); c.set_source(gr); c.fill()
    for gv in (1, 2, 5, 9, 20, 46):
        ty = y0 - (y0 - y1) * math.log(gv) / math.log(50)
        c.set_source_rgba(1, 1, 1, 0.7); c.rectangle(x + 22, ty - 1, 14, 3); c.fill()
        font(c, 24); c.move_to(x + 42, ty + 8); c.show_text(f"{gv}"); c.new_path()


def pilot(c, t, g):
    i, s = stage(t); pose = s[4]
    if 30.8 <= t < 34.0: pose = 'blink'
    if t >= ST[-1][0]: pose = 'salute'
    gw = g if t < 44.5 else 1.0
    if pose == 'helmet': gw = 1 + (g - 1) * 0.35       # combinaison anti-G : il encaisse
    surf, _b = warped(pose, gw)
    sz = 860; x = W / 2 - sz / 2 + 60; y = 1080
    tilt = -0.25 * ease((t - 31.2) / 0.5) * (1 - ease((t - 33.6) / 0.4)) if 30.8 <= t < 34.2 else 0
    c.save(); c.translate(x + sz / 2, y + sz); c.rotate(tilt); c.translate(-sz / 2, -sz)
    c.scale(sz / 720, sz / 720); c.set_source_surface(surf, 0, 0); c.paint(); c.restore()
    # poids
    if ST[1][0] <= t < 50.5:
        gg = g
        rrect(c, 730, 1150, 320, 170, 24); c.set_source_rgba(0, 0, 0, 0.6); c.fill()
        font(c, 28); c.set_source_rgba(0.85, 0.88, 0.95, 1); c.move_to(752, 1195); c.show_text("TA TÊTE PÈSE"); c.new_path()
        text_c(c, f"{5 * gg:.0f} KG", 890, 1270, 64, (*YEL, 1))
        rrect(c, 730, 1340, 320, 170, 24); c.set_source_rgba(0, 0, 0, 0.6); c.fill()
        font(c, 28); c.set_source_rgba(0.85, 0.88, 0.95, 1); c.move_to(752, 1385); c.show_text("TON CORPS PÈSE"); c.new_path()
        text_c(c, f"{75 * gg:.0f} KG", 890, 1460, 64, (*YEL, 1))


def vision(arr, t, g):
    """Voile gris (désaturation) puis tunnel, puis noir."""
    sat = 1.0; tun = None; black = 0.0
    if 21.0 <= t < 35.5:
        sat = 1 - min(1, max(0, (g - 4.0) / 1.0)) * 0.95
        if t >= 28.0:
            k = ease((t - 28.4) / 2.4); tun = 1300 - 1150 * k
        if 30.8 <= t < 34.2: black = ease((t - 30.8) / 0.5) * (1 - ease((t - 33.6) / 0.6))
        if t >= 33.6:
            r = ease((t - 33.6) / 1.4); sat = sat + (1 - sat) * r * 0.3; tun = 150 + 1150 * r
    if 35.5 <= t < 44.5:
        sat = 0.85
    if sat < 0.999:
        gray = arr[..., :3].mean(axis=2, keepdims=True); arr[..., :3] = (arr[..., :3] * sat + gray * (1 - sat))
    if tun is not None:
        yy, xx = np.ogrid[:H, :W]; d = np.sqrt((xx - W / 2) ** 2 + ((yy - 760) * 0.8) ** 2)
        m = np.clip((d - tun) / 220, 0, 1)[..., None]; arr[..., :3] *= (1 - m)
    if black > 0: arr[..., :3] *= (1 - black)
    return arr


def outro(c, t):
    if t < ST[-1][0]: return
    lt = t - ST[-1][0]; a = ease_out(lt / 0.4)
    c.set_source_rgba(0.03, 0.04, 0.08, 0.96 * a); c.paint()
    text_c(c, "46,2 G", W / 2, 420, 200, (*YEL, a), stroke=16)
    text_c(c, "et il a survécu.", W / 2, 520, 60, (1, 1, 1, a), stroke=8)
    if lt > 1.2:
        b = ease_out((lt - 1.2) / 0.4)
        text_c(c, "Et toi, tu tiendrais", W / 2, 700, 64, (1, 1, 1, b), stroke=8)
        text_c(c, "combien de G ?", W / 2, 785, 64, (1, 1, 1, b), stroke=8)
        text_c(c, "Dis-le en commentaire", W / 2, 880, 44, (*CYA, b), stroke=6)
    if lt > 2.4:
        b = ease_out((lt - 2.4) / 0.4)
        rrect(c, W / 2 - 300, 950, 600, 100, 50); c.set_source_rgba(*RED, b); c.fill()
        text_c(c, "ABONNE-TOI", W / 2, 1018, 54, (1, 1, 1, b))


def background(c, t):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, 0.06, 0.08, 0.14); g.add_color_stop_rgb(1, 0.02, 0.03, 0.06)
    c.set_source(g); c.paint()


def frame(t):
    g = G_at(t)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    background(c, t); sky_window(c, t, g); pilot(c, t, g); g_bar(c, t, g); g_hud(c, t, g)
    s.flush()
    arr = np.ndarray((H, W, 4), np.uint8, s.get_data()).astype(np.float32)
    arr = vision(arr, t, g)
    out = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    np.ndarray((H, W, 4), np.uint8, out.get_data())[:] = np.clip(arr, 0, 255).astype(np.uint8); out.mark_dirty()
    c2 = cairo.Context(out)
    if 30.8 <= t < 34.2:   # texte pendant le noir
        bl = ease((t - 31.2) / 0.4) * (1 - ease((t - 33.4) / 0.4))
        text_c(c2, "…", W / 2, 760, 140, (1, 1, 1, bl))
        text_c(c2, "G-LOC : PERTE DE CONSCIENCE", W / 2, 880, 50, (*RED, bl), stroke=6)
    outro(c2, t)
    c2.set_source_rgba(*YEL, 1); c2.rectangle(0, 0, W * t / TOTAL, 8); c2.fill()
    return out


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        for x in sys.argv[2:]: frame(float(x)).write_to_png(OUT + f'still_{x}.png')
        sys.exit()
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', OUT + 'video_noaudio.mp4'], stdin=subprocess.PIPE)
    n = int(TOTAL * FPS)
    for i in range(n):
        ff.stdin.write(bytes(frame(i / FPS).get_data()))
        if i % 300 == 0: print(i, '/', n, flush=True)
    ff.stdin.close(); ff.wait(); print('done', TOTAL)
