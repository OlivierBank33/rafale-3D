"""Biographie cinématique (style archive) — Louis Blériot."""
import cairo, json, math, subprocess, sys, re, random
import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
from bio_script import SCENES, TITLE

W, H, FPS = 1080, 1920, 30
D = json.load(open('bio/durs.json'))
CREAM = (0.96, 0.91, 0.79); GOLD = (0.88, 0.68, 0.32); INK = (0.13, 0.09, 0.06); RUST = (0.72, 0.28, 0.16)
SEA = (0.16, 0.26, 0.3)

# ---------- Timeline ----------
SEG = []
t = 0.0
for i, s in enumerate(SCENES):
    pre = 1.4 if i == 0 else 0.5
    post = 0.9 if s['scene'] != 'outro' else 2.6
    SEG.append(dict(k=f's{i}', scene=s['scene'], t0=t, vt=t + pre, end=t + pre + D[f's{i}'] + post))
    t = SEG[-1]['end']
TOTAL = t
json.dump(dict(seg=SEG, total=TOTAL), open('bio/timeline.json', 'w'))


def ease(u):
    u = min(max(u, 0), 1); return u * u * (3 - 2 * u)


def ease_out(u):
    u = min(max(u, 0), 1); return 1 - (1 - u) ** 3


def to_surface(img):
    a = np.array(img.convert('RGBA')).astype(np.float32)
    al = a[..., 3:4] / 255.0; rgb = a[..., :3] * al
    bgra = np.dstack([rgb[..., 2], rgb[..., 1], rgb[..., 0], a[..., 3]]).astype(np.uint8)
    h, w = bgra.shape[:2]
    stride = cairo.ImageSurface.format_stride_for_width(cairo.FORMAT_ARGB32, w)
    buf = np.zeros((h, stride // 4, 4), np.uint8); buf[:, :w] = bgra
    return cairo.ImageSurface.create_for_data(bytearray(buf.tobytes()), cairo.FORMAT_ARGB32, w, h, stride)


def sepia(im, strength=0.85):
    rgb = im.convert('RGB'); al = im.split()[3]
    g = ImageOps.grayscale(rgb)
    g = ImageEnhance.Contrast(g.convert('RGB')).enhance(1.15).convert('L')
    sep = ImageOps.colorize(g, black=(30, 20, 12), mid=(150, 112, 70), white=(250, 236, 205))
    out = Image.blend(rgb, sep, strength); out.putalpha(al)
    return out


def load(name, bw, bh, tone=0.85):
    im = Image.open(f'r3d/{name}.png').convert('RGBA'); im = im.crop(im.getbbox())
    sc = min(bw / im.width, bh / im.height)
    im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
    im = sepia(im, tone)
    sil = Image.new('RGBA', im.size, (12, 8, 5, 255)); sil.putalpha(im.split()[3])
    return dict(c=to_surface(im), s=to_surface(sil), w=im.width, h=im.height)


IMG = {k: load(f'bleriot_{k}', 1000, 760) for k in 'abcde'}
ICON = load('bleriot_e', 120, 120, tone=0.0)

# grain précalculé
rng = np.random.default_rng(3)
GRAIN = []
for _ in range(6):
    n = (rng.random((H // 2, W // 2)) * 255).astype(np.uint8)
    im = Image.fromarray(n, 'L').resize((W, H), Image.NEAREST)
    rgba = Image.merge('RGBA', (im, im, im, Image.new('L', (W, H), 255)))
    GRAIN.append(to_surface(rgba))


# ---------- Helpers ----------
def font(c, size, serif=False, bold=True):
    c.select_font_face("Lora" if serif else "Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)


def text_c(c, txt, x, y, size, rgba=(1, 1, 1, 1), serif=True, stroke=0, maxw=None, bold=True):
    font(c, size, serif, bold); e = c.text_extents(txt)
    if maxw and e.x_advance > maxw:
        size *= maxw / e.x_advance; font(c, size, serif, bold); e = c.text_extents(txt)
    c.move_to(x - e.x_advance / 2, y); c.text_path(txt)
    if stroke:
        c.set_source_rgba(0, 0, 0, 0.8 * rgba[3]); c.set_line_width(stroke); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
    c.set_source_rgba(*rgba); c.fill(); c.new_path()


def text_l(c, txt, x, y, size, rgba, serif=True, bold=True):
    font(c, size, serif, bold); c.move_to(x, y); c.set_source_rgba(*rgba); c.show_text(txt)


def typewriter(c, txt, x, y, size, rgba, u, serif=True):
    n = int(len(txt) * min(1, max(0, u)))
    text_c(c, txt[:n] + ('|' if u < 1 and int(u * 20) % 2 == 0 else ''), x, y, size, rgba, serif)


def img(c, im, key, cx, cy, s=1.0, a=1.0, rot=0.0):
    if a <= 0 or s < 0.02: return
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s); c.translate(-im['w'] / 2, -im['h'] / 2)
    c.set_source_surface(im[key], 0, 0); c.paint_with_alpha(min(1, a)); c.restore()


def paper_bg(c, t, dark=True):
    if dark:
        g = cairo.RadialGradient(W / 2, 820, 80, W / 2, 820, 1250)
        g.add_color_stop_rgb(0, 0.22, 0.16, 0.1); g.add_color_stop_rgb(1, 0.04, 0.03, 0.02)
    else:
        g = cairo.RadialGradient(W / 2, 900, 80, W / 2, 900, 1300)
        g.add_color_stop_rgb(0, 0.93, 0.87, 0.74); g.add_color_stop_rgb(1, 0.55, 0.45, 0.32)
    c.set_source(g); c.paint()


def finish(c, t, s):
    """Grain, vignette, scintillement, taches."""
    fi = int(t * 12) % len(GRAIN)
    c.save(); c.set_operator(cairo.OPERATOR_OVERLAY)
    c.set_source_surface(GRAIN[fi], 0, 0); c.paint_with_alpha(0.13); c.restore()
    flick = 0.04 * (math.sin(t * 37) * 0.5 + math.sin(t * 13.7) * 0.5)
    c.set_source_rgba(0, 0, 0, max(0, 0.03 + flick)); c.paint()
    g = cairo.RadialGradient(W / 2, H / 2, 420, W / 2, H / 2, 1180)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.02, 0.01, 0, 0.78)
    c.set_source(g); c.paint()
    # rayures verticales de pellicule
    random.seed(int(t * 8))
    for _ in range(2):
        if random.random() < 0.5:
            x = random.uniform(80, W - 80)
            c.set_source_rgba(1, 0.95, 0.85, random.uniform(0.04, 0.1)); c.set_line_width(random.uniform(1, 2.5))
            c.move_to(x, 0); c.line_to(x + random.uniform(-8, 8), H); c.stroke()
    # transitions : fondu au noir + brûlure
    lt = t - s['t0']; rt = s['end'] - t
    if lt < 0.35:
        c.set_source_rgba(0, 0, 0, 1 - ease(lt / 0.35)); c.paint()
    if rt < 0.3:
        c.set_source_rgba(0, 0, 0, ease(1 - rt / 0.3)); c.paint()
        g2 = cairo.RadialGradient(W * 0.8, H * 0.2, 0, W * 0.8, H * 0.2, 900)
        g2.add_color_stop_rgba(0, 1, 0.6, 0.2, 0.35 * (1 - rt / 0.3)); g2.add_color_stop_rgba(1, 1, 0.4, 0.1, 0)
        c.set_source(g2); c.paint()


def chapter(c, txt, t, s, y=200):
    u = ease_out((t - s['t0'] - 0.2) / 0.6)
    if u <= 0: return
    font(c, 30, serif=False); e = c.text_extents(txt)
    c.set_source_rgba(*GOLD, u); c.set_line_width(2)
    c.move_to(W / 2 - e.x_advance / 2 - 70, y - 10); c.line_to(W / 2 - e.x_advance / 2 - 20, y - 10)
    c.move_to(W / 2 + e.x_advance / 2 + 20, y - 10); c.line_to(W / 2 + e.x_advance / 2 + 70, y - 10); c.stroke()
    c.move_to(W / 2 - e.x_advance / 2, y); c.show_text(txt)


# ---------- Scènes ----------
def sc_hook(c, t, s):
    lt = t - s['t0']
    c.set_source_rgb(0.02, 0.015, 0.01); c.paint()
    dawn = ease((lt - 1.0) / 5.0)
    g = cairo.LinearGradient(0, 600, 0, 1500)
    g.add_color_stop_rgba(0, 0.05, 0.04, 0.06, dawn); g.add_color_stop_rgba(0.75, 0.75, 0.42, 0.18, dawn); g.add_color_stop_rgba(1, 0.12, 0.08, 0.05, dawn)
    c.set_source(g); c.rectangle(0, 600, W, 900); c.fill()
    typewriter(c, "25 JUILLET 1909", W / 2, 360, 86, (*CREAM, 1), (lt - 0.2) / 1.4)
    text_c(c, "À L'AUBE, PRÈS DE CALAIS", W / 2, 440, 34, (*GOLD, min(1, max(0, (lt - 1.8) / 0.6))), serif=False)
    z = 0.85 + 0.12 * ease(lt / 8)
    img(c, IMG['d'], 's', W / 2, 1060, z, 1 - dawn * 0.3)
    img(c, IMG['d'], 'c', W / 2, 1060, z, dawn * 0.75)


def sc_portrait(c, t, s):
    lt = t - s['t0']
    paper_bg(c, t)
    z = 0.78 + 0.08 * ease(lt / 8)
    img(c, IMG['c'], 'c', W / 2 + 60 - 60 * ease(lt / 8), 1000, z, min(1, lt / 0.6))
    chapter(c, "LE PERSONNAGE", t, s)
    u = ease_out((lt - 0.3) / 0.7)
    text_c(c, "Louis", W / 2, 290 + 30 * (1 - u), 72, (*CREAM, u), bold=False)
    text_c(c, "BLÉRIOT", W / 2, 450 + 30 * (1 - u), 150, (*CREAM, u))
    text_c(c, "1872 – 1936", W / 2, 520, 40, (*GOLD, u), serif=False)
    v = ease_out((t - s['vt'] - 3.2) / 0.5)
    if v > 0:
        # carte « phares »
        c.save(); c.translate(W / 2, 1420); c.rotate(-0.03); c.scale(v, v)
        c.rectangle(-300, -70, 600, 140); c.set_source_rgba(*CREAM, 0.95); c.fill()
        c.set_source_rgba(*INK, 1); c.set_line_width(3); c.rectangle(-288, -58, 576, 116); c.stroke()
        c.arc(-215, 0, 34, 0, 2 * math.pi); c.set_source_rgba(*GOLD, 1); c.fill()
        for k in range(7):
            a = -0.6 + k * 0.2
            c.move_to(-215 + 40 * math.cos(a), 40 * math.sin(a)); c.line_to(-215 + 70 * math.cos(a), 70 * math.sin(a))
        c.set_source_rgba(*INK, 1); c.set_line_width(4); c.stroke()
        text_l(c, "PHARES BLÉRIOT", -150, 14, 46, (*INK, 1))
        c.restore()


def sc_journal(c, t, s):
    lt = t - s['t0']
    paper_bg(c, t)
    z = 0.92 + 0.14 * ease(lt / 7)
    c.save(); c.translate(W / 2, 880); c.rotate(-0.04 + 0.03 * ease(lt / 7)); c.scale(z, z)
    c.rectangle(-430, -560, 860, 1120); c.set_source_rgb(0.92, 0.88, 0.78); c.fill()
    c.set_source_rgba(*INK, 0.9); c.set_line_width(3); c.move_to(-400, -440); c.line_to(400, -440); c.move_to(-400, -432); c.line_to(400, -432); c.stroke()
    text_c(c, "DAILY MAIL", 0, -460, 104, (*INK, 1))
    text_c(c, "LONDRES — 1909", 0, -395, 26, (*INK, 0.8), serif=False)
    text_c(c, "1 000 £", 0, -220, 170, (*RUST, 1))
    text_c(c, "AU PREMIER AVIATEUR", 0, -120, 50, (*INK, 1))
    text_c(c, "QUI TRAVERSERA", 0, -60, 50, (*INK, 1))
    text_c(c, "LA MANCHE", 0, 20, 82, (*INK, 1))
    random.seed(5)
    for col in range(3):
        x0 = -400 + col * 275
        for r in range(15):
            w = random.uniform(150, 250)
            c.rectangle(x0, 90 + r * 28, w, 9); c.set_source_rgba(*INK, 0.25); c.fill()
    c.restore()


def sc_rival(c, t, s):
    lt = t - s['t0']
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.32, 0.33, 0.3); g.add_color_stop_rgb(0.45, 0.55, 0.53, 0.46); g.add_color_stop_rgb(0.5, *SEA); g.add_color_stop_rgb(1, 0.05, 0.08, 0.1)
    c.set_source(g); c.paint()
    for j in range(14):
        y = 980 + j * 70 + (j * j) * 3
        ph = t * (0.8 + 0.1 * j) + j
        c.set_source_rgba(0.85, 0.85, 0.8, 0.12 + 0.01 * j); c.set_line_width(2 + j * 0.3)
        c.move_to(0, y)
        for x in range(0, W + 40, 40): c.line_to(x, y + 8 * math.sin(x / 90 + ph))
        c.stroke()
    chapter(c, "LE RIVAL", t, s)
    typewriter(c, "19 JUILLET 1909", W / 2, 360, 76, (*CREAM, 1), (lt - 0.2) / 1.2)
    text_c(c, "HUBERT LATHAM", W / 2, 460, 56, (*GOLD, min(1, max(0, (lt - 1.2) / 0.5))))
    # éclaboussure
    k = (t - s['vt'] - 2.6)
    if k > 0:
        for r in range(4):
            rr = (k * 260 - r * 70)
            if rr > 0:
                c.set_source_rgba(1, 1, 1, max(0, 0.6 - rr / 700)); c.set_line_width(5)
                c.save(); c.translate(W / 2, 1150); c.scale(1, 0.3); c.arc(0, 0, rr, 0, 2 * math.pi); c.restore(); c.stroke()
        u = ease_out(k / 0.4)
        c.save(); c.translate(W / 2, 760); c.rotate(-0.08); c.scale(u, u)
        c.rectangle(-300, -60, 600, 120); c.set_source_rgba(*RUST, 0.92); c.fill()
        text_c(c, "PANNE MOTEUR", 0, 22, 64, (*CREAM, 1), serif=False)
        c.restore()


def callout(c, x0, y0, x1, y1, txt, u, right=True):
    if u <= 0: return
    c.set_source_rgba(*GOLD, u); c.set_line_width(3)
    c.arc(x0, y0, 9, 0, 2 * math.pi); c.fill()
    xm = x0 + (x1 - x0) * u; ym = y0 + (y1 - y0) * u
    c.move_to(x0, y0); c.line_to(xm, ym); c.stroke()
    if u > 0.9:
        font(c, 40, serif=False); e = c.text_extents(txt)
        tx = x1 + 14 if right else x1 - 14 - e.x_advance
        c.rectangle(tx - 12, y1 - 38, e.x_advance + 24, 54); c.set_source_rgba(0.05, 0.03, 0.02, 0.75); c.fill()
        c.set_source_rgba(*CREAM, 1); c.move_to(tx, y1); c.show_text(txt)


def sc_avion(c, t, s):
    lt = t - s['t0']; d = s['end'] - s['t0']
    paper_bg(c, t)
    chapter(c, "LA MACHINE", t, s)
    text_c(c, "BLÉRIOT XI", W / 2, 340, 120, (*CREAM, ease_out((lt - 0.3) / 0.6)))
    k = lt / d
    a1 = 1 - ease((k - 0.45) / 0.15)
    img(c, IMG['a'], 'c', W / 2, 940, 0.92 + 0.08 * k, a1)
    img(c, IMG['b'], 'c', W / 2, 940, 0.9 + 0.06 * k, 1 - a1)
    callout(c, 300, 920, 120, 1320, "BOIS & TOILE", ease((t - s['vt'] - 0.6) / 0.5), right=True)
    callout(c, 760, 880, 620, 1440, "MOTEUR 25 CH", ease((t - s['vt'] - 3.6) / 0.5), right=False)


# carte : lon/lat -> écran
LON0, LON1, LAT0, LAT1 = 0.85, 2.45, 50.55, 51.5


def P(lon, lat):
    x = 60 + (lon - LON0) / (LON1 - LON0) * (W - 120)
    y = 380 + (LAT1 - lat) / (LAT1 - LAT0) * 1180
    return x, y


FR = [(0.85, 50.55), (1.58, 50.55), (1.6, 50.72), (1.58, 50.87), (1.66, 50.92), (1.75, 50.95), (1.86, 50.96), (2.1, 51.0), (2.37, 51.04), (2.45, 51.06), (2.45, 50.55)]
EN = [(0.85, 51.5), (0.85, 50.95), (0.98, 50.98), (1.08, 51.05), (1.18, 51.08), (1.32, 51.12), (1.38, 51.15), (1.41, 51.22), (1.42, 51.33), (1.45, 51.38), (1.3, 51.42), (1.0, 51.47), (0.9, 51.5)]
START = (1.76, 50.94); END = (1.33, 51.13)


def poly(c, pts):
    c.new_path()
    for j, (lo, la) in enumerate(pts):
        x, y = P(lo, la); (c.move_to if j == 0 else c.line_to)(x, y)
    c.close_path()


def sc_carte(c, t, s):
    lt = t - s['t0']
    c.set_source_rgb(0.18, 0.26, 0.28); c.paint()
    for j in range(0, H, 14):
        c.set_source_rgba(1, 1, 1, 0.02); c.rectangle(0, j, W, 1); c.fill()
    for pts in (FR, EN):
        poly(c, pts); c.set_source_rgb(0.84, 0.77, 0.6); c.fill_preserve(); c.set_source_rgba(*INK, 0.8); c.set_line_width(3); c.stroke()
    text_c(c, "FRANCE", *P(1.95, 50.75), 64, (*INK, 0.85))
    text_c(c, "ANGLETERRE", *P(1.08, 51.3), 56, (*INK, 0.85))
    text_c(c, "LA MANCHE", *P(1.68, 51.18), 40, (*CREAM, 0.6), bold=False)
    chapter(c, "LA TRAVERSÉE", t, s)
    # trajet
    u = ease((t - s['vt'] - 0.5) / (D[s['k']] + 0.2))
    x0, y0 = P(*START); x1, y1 = P(*END)
    for (lo, la, lab, dy) in ((*START, "Les Baraques", 60), (*END, "Douvres", -30)):
        x, y = P(lo, la); c.set_source_rgba(*RUST, 1); c.arc(x, y, 12, 0, 2 * math.pi); c.fill()
        font(c, 36, serif=False); e = c.text_extents(lab)
        c.set_source_rgba(*INK, 1); c.move_to(x - e.x_advance / 2, y + dy); c.show_text(lab)
    # courbe légèrement déviée (perdu dans la brume)
    def route(k):
        x = x0 + (x1 - x0) * k + 90 * math.sin(math.pi * k) * (1 if k > 0.3 else k / 0.3)
        y = y0 + (y1 - y0) * k
        return x, y
    c.set_source_rgba(*RUST, 1); c.set_line_width(5); c.set_dash([16, 12])
    c.move_to(x0, y0)
    for j in range(1, 61):
        k = u * j / 60; c.line_to(*route(k))
    c.stroke(); c.set_dash([])
    px, py = route(u)
    img(c, ICON, 'c', px, py, 0.9, 1.0, rot=math.atan2(y1 - y0, x1 - x0) + math.pi / 2)
    # brume
    fog = ease((u - 0.3) / 0.12) * (1 - ease((u - 0.62) / 0.12))
    if fog > 0:
        for j in range(9):
            fx = W * (0.1 + 0.1 * j) + 30 * math.sin(t + j); fy = (y0 + y1) / 2 + 60 * math.cos(j * 1.3)
            g = cairo.RadialGradient(fx, fy, 0, fx, fy, 260)
            g.add_color_stop_rgba(0, 0.9, 0.9, 0.88, 0.55 * fog); g.add_color_stop_rgba(1, 0.9, 0.9, 0.88, 0)
            c.set_source(g); c.arc(fx, fy, 260, 0, 2 * math.pi); c.fill()
        text_c(c, "BROUILLARD", W / 2, (y0 + y1) / 2 + 20, 60, (*INK, fog), serif=False)
    # chrono
    mins = 37 * u
    c.rectangle(W / 2 - 170, 1630, 340, 110); c.set_source_rgba(0.05, 0.03, 0.02, 0.8); c.fill()
    text_c(c, f"{int(mins):02d} MIN", W / 2, 1712, 72, (*CREAM, 1), serif=False)


def sc_falaises(c, t, s):
    lt = t - s['t0']
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.42, 0.44, 0.42); g.add_color_stop_rgb(0.55, 0.78, 0.74, 0.64); g.add_color_stop_rgb(0.56, 0.3, 0.38, 0.38); g.add_color_stop_rgb(1, 0.08, 0.1, 0.1)
    c.set_source(g); c.paint()
    # falaises blanches
    rise = ease_out(lt / 1.5)
    base = 1150 + 200 * (1 - rise)
    c.new_path(); c.move_to(-20, base + 300); c.line_to(-20, base - 60)
    random.seed(8)
    x = -20
    while x < W + 40:
        x += random.uniform(40, 90); c.line_to(x, base - 60 - random.uniform(0, 70) - 120 * math.sin(x / W * math.pi))
    c.line_to(W + 40, base + 300); c.close_path()
    c.set_source_rgb(0.93, 0.9, 0.82); c.fill_preserve(); c.set_source_rgba(*INK, 0.5); c.set_line_width(2); c.stroke()
    for j in range(24):
        xx = j * 47 + 10
        c.set_source_rgba(0.6, 0.55, 0.45, 0.25); c.set_line_width(2); c.move_to(xx, base - 40); c.line_to(xx + 8, base + 200); c.stroke()
    c.rectangle(0, base + 180, W, H); c.set_source_rgb(0.12, 0.17, 0.18); c.fill()
    chapter(c, "DOUVRES", t, s)
    # avion qui arrive et descend
    k = ease((t - s['vt']) / 3.0)
    img(c, IMG['b'], 'c', -200 + (W / 2 + 200) * k, 600 + 260 * k, 0.62, 1.0, rot=0.06)
    v = ease_out((t - s['vt'] - 3.6) / 0.5)
    if v > 0:
        text_c(c, "37 MIN", W / 2, 400, 170 * (0.7 + 0.3 * v), (*CREAM, v), stroke=8)
        text_c(c, "≈ 38 KM AU-DESSUS DE LA MER", W / 2, 470, 38, (*GOLD, v), serif=False, stroke=5)


HEADLINES = ["L'ANGLETERRE N'EST PLUS UNE ÎLE", "BLÉRIOT A VAINCU LA MANCHE", "L'EXPLOIT DU SIÈCLE"]


def sc_gloire(c, t, s):
    lt = t - s['t0']
    paper_bg(c, t)
    chapter(c, "LA GLOIRE", t, s)
    for j, h in enumerate(HEADLINES):
        u = ease_out((lt - 0.3 - 0.9 * j) / 0.45)
        if u <= 0: continue
        c.save(); c.translate(W / 2 + (1 - u) * 900 * (-1) ** j, 470 + j * 230); c.rotate((-0.05, 0.04, -0.02)[j])
        c.rectangle(-460, -90, 920, 180); c.set_source_rgb(0.92, 0.88, 0.78); c.fill()
        c.set_source_rgba(*INK, 0.7); c.set_line_width(2); c.rectangle(-445, -75, 890, 150); c.stroke()
        text_c(c, h, 0, 20, 54, (*INK, 1), maxw=840)
        c.restore()
    v = ease_out((t - s['vt'] - 4.2) / 0.5)
    if v > 0:
        n = int(100 * min(1, (t - s['vt'] - 4.2) / 1.2))
        text_c(c, f"{n}+", W / 2, 1360, 210 * (0.7 + 0.3 * v), (*GOLD, v), stroke=8)
        text_c(c, "COMMANDES", W / 2, 1450, 60, (*CREAM, v), serif=False, stroke=5)


def sc_musee(c, t, s):
    lt = t - s['t0']
    c.set_source_rgb(0.1, 0.08, 0.06); c.paint()
    # voûte d'église
    for j in range(5):
        c.set_source_rgba(*GOLD, 0.18 + 0.05 * j); c.set_line_width(6 - j)
        x0 = 100 + j * 60; x1 = W - 100 - j * 60
        c.move_to(x0, H); c.line_to(x0, 700 + j * 40); c.curve_to(x0, 200 + j * 60, x1, 200 + j * 60, x1, 700 + j * 40); c.line_to(x1, H); c.stroke()
    g = cairo.RadialGradient(W / 2, 250, 10, W / 2, 250, 900)
    g.add_color_stop_rgba(0, 1, 0.9, 0.7, 0.35); g.add_color_stop_rgba(1, 1, 0.9, 0.7, 0)
    c.set_source(g); c.paint()
    z = 0.62 + 0.1 * ease(lt / 6); sway = 0.02 * math.sin(t * 0.8)
    cy = 900
    c.set_source_rgba(*CREAM, 0.7); c.set_line_width(2)
    c.move_to(W / 2 - 180, 0); c.line_to(W / 2 - 180 * z, cy - 150 * z); c.move_to(W / 2 + 180, 0); c.line_to(W / 2 + 180 * z, cy - 150 * z); c.stroke()
    img(c, IMG['a'], 'c', W / 2, cy, z, min(1, lt / 0.6), rot=sway)
    u = ease_out((t - s['vt'] - 1.5) / 0.6)
    text_c(c, "MUSÉE DES ARTS ET MÉTIERS", W / 2, 1360, 50, (*CREAM, u), maxw=980)
    text_c(c, "PARIS", W / 2, 1430, 40, (*GOLD, u), serif=False)


def sc_outro(c, t, s):
    lt = t - s['t0']
    paper_bg(c, t)
    img(c, IMG['d'], 'c', W / 2, 900, 0.8 + 0.05 * ease(lt / 5), min(1, lt / 0.6))
    u = ease_out((lt - 0.2) / 0.7)
    text_c(c, "LOUIS BLÉRIOT", W / 2, 340, 110, (*CREAM, u), maxw=1000)
    text_c(c, "PREMIER À TRAVERSER LA MANCHE EN AVION", W / 2, 410, 34, (*GOLD, u), serif=False, maxw=980)
    v = ease_out((t - s['vt'] - 0.8) / 0.5)
    if v > 0:
        text_c(c, "LE PROCHAIN PIONNIER ?", W / 2, 1380, 66, (*CREAM, v), serif=False, stroke=6)
        yy = 1430 + 12 * math.sin(t * 6)
        c.set_source_rgba(*GOLD, v); c.move_to(W / 2 - 40, yy); c.line_to(W / 2 + 40, yy); c.line_to(W / 2, yy + 50); c.close_path(); c.fill()


SCN = dict(hook=sc_hook, portrait=sc_portrait, journal=sc_journal, rival=sc_rival, avion=sc_avion, carte=sc_carte,
           falaises=sc_falaises, gloire=sc_gloire, musee=sc_musee, outro=sc_outro)


# ---------- Sous-titres ----------
def build_caps():
    caps = []
    for s, sc in zip(SEG, SCENES):
        words = sc['show'].replace('1 000', '1 000').split(' ')
        def wt(w_):
            n = len(re.sub(r'[^\w]', '', w_)) + 3 * sum(ch.isdigit() for ch in w_)
            if w_.endswith(('.', '!', '?', ':', '»')): n += 6
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
            if len(grp) == 3 or w_.endswith(('.', '!', '?', ':', ',', '»')) or j == len(words) - 1 or (len(grp) == 2 and len(''.join(words[q] for q in grp)) > 14):
                caps.append(dict(words=[words[q] for q in grp], times=[times[q] for q in grp], t0=times[grp[0]][0], t1=times[grp[-1]][1])); grp = []
    return caps


CAPS = build_caps()


def captions(c, t):
    cap = None
    for cp in CAPS:
        if cp['t0'] - 0.02 <= t < cp['t1'] + 0.05: cap = cp
    if not cap: return
    size = 64; font(c, size, serif=False)
    words = [w_.upper() for w_ in cap['words']]
    sp = c.text_extents(' ').x_advance; widths = [c.text_extents(w_).x_advance for w_ in words]
    total = sum(widths) + sp * (len(words) - 1)
    if total > 880:
        size *= 880 / total; font(c, size, serif=False); widths = [c.text_extents(w_).x_advance for w_ in words]; sp = c.text_extents(' ').x_advance
        total = sum(widths) + sp * (len(words) - 1)
    y = 1570; x = W / 2 - total / 2
    for w_, wd, (a, b) in zip(words, widths, cap['times']):
        c.move_to(x, y); c.text_path(w_)
        c.set_source_rgba(0, 0, 0, 0.9); c.set_line_width(12); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
        c.set_source_rgb(*(GOLD if a <= t < b + 0.05 else CREAM)); c.fill(); c.new_path()
        x += wd + sp


def render(t, surf):
    c = cairo.Context(surf)
    s = SEG[0]
    for x in SEG:
        if t >= x['t0']: s = x
    SCN[s['scene']](c, t, s)
    finish(c, t, s)
    captions(c, t)
    # barre de progression discrète
    c.set_source_rgba(*GOLD, 0.9); c.rectangle(0, 0, W * t / TOTAL, 6); c.fill()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        for tt in map(float, sys.argv[2:]):
            sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); render(tt, sf); sf.write_to_png(f'bio/still_{tt:.1f}.png')
        print(round(TOTAL, 1), [(x['scene'], round(x['t0'], 1)) for x in SEG]); sys.exit()
    nframes = int(TOTAL * FPS)
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}',
                           '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '21',
                           '-pix_fmt', 'yuv420p', 'bio/video_noaudio.mp4'], stdin=subprocess.PIPE)
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    for f in range(nframes):
        render(f / FPS, sf); sf.flush(); ff.stdin.write(bytes(sf.get_data()))
        if f % 300 == 0: print(f, '/', nframes, flush=True)
    ff.stdin.close(); ff.wait(); print('done', TOTAL)
