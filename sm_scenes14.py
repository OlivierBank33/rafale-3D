"""30/10 : MYSTÈRES ép. 02 « la disparition de Saint-Exupéry » (31/07/1944) en style cinéma (sx_*).
P-38 / F-5B FlightGear (texture-fr, n° 223 = l'avion de Saint-Exupéry, pr/r_p38_*), Bf 109 (pr/r_bf_*), carte topo pr/map_med.png (jk_maps 'med').
Signatures : radiographie du nez photo (pas d'armes), viseur de reconnaissance qui « shoote » la côte, dernier écho radar, gourmette gravée
balayée par la lumière, descente à 85 m avec profondimètre, numéro de série révélé à la lampe."""
import cairo, math, random
from sm_lib import *
from sm_scenes2 import ease, ap, ORG, BLUE, RED, WH, GRN
from sm_scenes6 import si, stamp, eout, YEL
from sm_scenes7 import tag, label, check, cross
import sm_scenes10 as P10
from sm_scenes10 import plane, glow, letter, panel, counter
import sm_scenes12 as S12
from sm_scenes12 import sky_paint, plane_icon, radar_scope
from sm_scenes13 import route, curve_pts, mixc, CY
import pr.jk_maps as JM
R = None
SILVER = (0.86, 0.88, 0.92)


# =============================================================== décors
def sea(c, t, mode='dusk', horizon=1000, sun=(700, 860)):
    """Méditerranée : ciel + mer avec chemin de lumière ; mode dusk | night | dawn."""
    g = cairo.LinearGradient(0, 0, 0, horizon)
    if mode == 'dusk':
        g.add_color_stop_rgb(0, 0.10, 0.10, 0.26); g.add_color_stop_rgb(0.6, 0.62, 0.36, 0.40); g.add_color_stop_rgb(1, 1.0, 0.66, 0.38)
        sea_top, sea_bot, sc = (0.30, 0.22, 0.30), (0.03, 0.04, 0.09), (1.0, 0.75, 0.45)
    elif mode == 'dawn':
        g.add_color_stop_rgb(0, 0.18, 0.28, 0.48); g.add_color_stop_rgb(0.7, 0.70, 0.66, 0.70); g.add_color_stop_rgb(1, 1.0, 0.86, 0.66)
        sea_top, sea_bot, sc = (0.40, 0.46, 0.56), (0.05, 0.10, 0.18), (1.0, 0.9, 0.7)
    else:
        g.add_color_stop_rgb(0, 0.01, 0.015, 0.04); g.add_color_stop_rgb(1, 0.06, 0.08, 0.16)
        sea_top, sea_bot, sc = (0.06, 0.08, 0.15), (0.01, 0.015, 0.03), (0.85, 0.9, 1.0)
    c.rectangle(0, 0, W, horizon); c.set_source(g); c.fill()
    if mode == 'night':
        r = random.Random(7)
        for _ in range(200):
            c.new_path(); c.arc(r.random() * W, r.random() * (horizon - 40), r.choice((0.8, 1.2, 1.8)), 0, 7); c.set_source_rgba(1, 1, 1, 0.25 + 0.6 * r.random()); c.fill()
    sx, sy = sun
    if mode != 'night':
        glow(c, sx, horizon - 10, 520, sc, 0.35); glow(c, sx, horizon - 6, 90, (1, 0.95, 0.85), 0.8)
    g = cairo.LinearGradient(0, horizon, 0, H); g.add_color_stop_rgb(0, *sea_top); g.add_color_stop_rgb(1, *sea_bot)
    c.rectangle(0, horizon, W, H - horizon); c.set_source(g); c.fill()
    r = random.Random(3)
    for k in range(70):                                                          # chemin de lumière + vaguelettes
        y = horizon + 4 + (H - horizon) * (k / 70) ** 1.6; w = 60 + 600 * (k / 70) ** 1.2
        x = sx + 30 * math.sin(t * 1.3 + k) - w / 2 + r.uniform(-w * 0.3, w * 0.3)
        rr(c, x, y, w * r.uniform(0.3, 0.8), 2 + 6 * k / 70, 2); c.set_source_rgba(*sc, (0.30 if mode != 'night' else 0.12) * (1 - k / 90)); c.fill()
    for k in range(50):
        y = horizon + 6 + r.random() * (H - horizon); x = (r.random() * W - t * 25 * (1 + y / H)) % W
        c.move_to(x, y); c.line_to(x + 30 + r.random() * 90, y); c.set_source_rgba(0.6, 0.7, 0.9, 0.10); c.set_line_width(2 + 3 * (y - horizon) / (H - horizon)); c.stroke()


def clouds(c, t, a=1.0, y0=700, y1=1300, col=(0.95, 0.85, 0.85), speed=60, seed=4, n=14):
    r = random.Random(seed)
    for j in range(n):
        x = (r.uniform(0, W + 800) - t * speed * r.uniform(0.6, 1.4)) % (W + 800) - 400; y = r.uniform(y0, y1); rad = r.uniform(160, 380)
        c.save(); c.translate(x, y); c.scale(1, 0.45); glow(c, 0, 0, rad, col, 0.55 * a); c.restore()


def map_med(c, t, sc=1.0, cx=540, cy=900, fx=540, fy=900):
    """carte topo Méditerranée ; zoom sc autour du point (fx, fy) de la carte, ramené en (cx, cy)."""
    s, _ = P10.plate('map_med.png')
    c.save(); c.translate(cx, cy); c.scale(sc, sc); c.translate(-fx, -fy); c.set_source_surface(s, 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint(); c.restore()
    M0 = JM.MAP['med']
    return lambda lo, la: ((M0(lo, la)[0] - fx) * sc + cx, (M0(lo, la)[1] - fy) * sc + cy)


def camera_icon(c, x, y, s, col=YEL, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    rr(c, -30, -18, 60, 38, 6); c.set_source_rgba(*col, a); c.set_line_width(4); c.stroke()
    c.new_path(); c.arc(0, 1, 11, 0, 7); c.stroke(); rr(c, -14, -26, 16, 8, 2); c.fill()
    c.restore()


def bracelet(c, t, sweep, a=1.0, cx=540, cy=760):
    """gourmette en argent (macro) : plaque bombée gravée + maillons, reflet qui balaie."""
    c.save()
    for side in (-1, 1):                                                         # maillons
        for j in range(5):
            x = cx + side * (405 + j * 62); y = cy
            c.save(); c.translate(x, y + j * j * 6); c.rotate(side * (0.25 + 0.08 * j))
            c.new_path(); c.save(); c.scale(1.0, 0.62); c.arc(0, 0, 36, 0, 7); c.restore()
            g = cairo.LinearGradient(0, -24, 0, 24); g.add_color_stop_rgb(0, 0.95, 0.96, 0.98); g.add_color_stop_rgb(0.5, 0.55, 0.57, 0.62); g.add_color_stop_rgb(1, 0.85, 0.86, 0.9)
            c.set_source(g); c.set_line_width(11); c.stroke(); c.restore()
    w, h = 820, 220
    rr(c, cx - w / 2, cy - h / 2, w, h, 70)
    g = cairo.LinearGradient(0, cy - h / 2, 0, cy + h / 2)
    g.add_color_stop_rgb(0, 0.96, 0.97, 0.99); g.add_color_stop_rgb(0.35, 0.78, 0.80, 0.85); g.add_color_stop_rgb(0.7, 0.50, 0.52, 0.57); g.add_color_stop_rgb(1, 0.80, 0.82, 0.86)
    c.set_source(g); c.fill_preserve(); c.set_source_rgba(0.35, 0.36, 0.40, 1); c.set_line_width(3); c.stroke()
    # gravure : creux sombre décalé + arête claire
    for txt, yy, sz in (("ANTOINE DE SAINT EXUPÉRY", cy - 4, 42), ("(CONSUELO)", cy + 58, 40)):
        c.save(); c.select_font_face('Montserrat', 0, 1); c.set_font_size(sz); e = c.text_extents(txt)
        x0 = cx - e.width / 2 - e.x_bearing
        c.move_to(x0 + 1.5, yy + 1.5); c.text_path(txt); c.set_source_rgba(1, 1, 1, 0.55); c.fill()
        c.move_to(x0, yy); c.text_path(txt); c.set_source_rgba(0.18, 0.19, 0.22, 0.9); c.fill()
        c.restore()
    # reflet spéculaire qui balaie (clippé sur la plaque)
    rr(c, cx - w / 2, cy - h / 2, w, h, 70); c.clip()
    x = cx - w / 2 - 200 + (w + 400) * sweep
    g = cairo.LinearGradient(x - 90, 0, x + 90, 0); g.add_color_stop_rgba(0, 1, 1, 1, 0); g.add_color_stop_rgba(0.5, 1, 1, 1, 0.65); g.add_color_stop_rgba(1, 1, 1, 1, 0)
    c.save(); c.translate(x, cy); c.rotate(0.35); c.rectangle(-90, -400, 180, 800); c.restore(); c.set_source(g); c.fill()
    c.restore()


def underwater(c, t, depth, torch=None, a=1.0):
    """bleu qui s'assombrit avec la profondeur (0..85 m), rais de surface, particules qui montent (descente)."""
    k = min(1.0, depth / 85.0)
    top = mixc((0.10, 0.45, 0.62), (0.01, 0.05, 0.10), k ** 0.7); bot = mixc((0.03, 0.18, 0.30), (0.0, 0.01, 0.03), k ** 0.6)
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *top); g.add_color_stop_rgb(1, *bot); c.set_source(g); c.paint()
    if k < 0.8:
        c.save(); c.set_operator(cairo.OPERATOR_ADD)
        for j in range(6):
            x = 150 + j * 170 + 40 * math.sin(t * 0.4 + j); br = 0.10 * (1 - k / 0.8) * (0.7 + 0.3 * math.sin(t + j * 2))
            g = cairo.LinearGradient(x, 0, x + 300, 1500); g.add_color_stop_rgba(0, 0.6, 0.9, 1.0, br); g.add_color_stop_rgba(1, 0.6, 0.9, 1.0, 0)
            c.new_path(); c.move_to(x, -10); c.line_to(x + 60, -10); c.line_to(x + 420, 1500); c.line_to(x + 240, 1500); c.close_path(); c.set_source(g); c.fill()
        c.restore()
    r = random.Random(11)
    for j in range(90):
        sp = r.uniform(40, 140); x = r.random() * W + 10 * math.sin(t + j); y = (r.random() * H - t * sp) % H
        c.new_path(); c.arc(x, y, r.uniform(1, 3), 0, 7); c.set_source_rgba(0.7, 0.85, 1, 0.25 * a); c.fill()


def seabed(c, t, y=1180, torch=(540, 900), tr=380, k=1.0):
    """fond rocheux + fragments d'épave, visibles dans le faisceau de la lampe."""
    r = random.Random(5)
    c.new_path(); c.move_to(0, y)
    for i in range(0, W + 41, 40): c.line_to(i, y + r.uniform(-25, 25))
    c.line_to(W, H); c.line_to(0, H); c.close_path(); c.set_source_rgb(0.02, 0.04, 0.06); c.fill()
    # fragments : poutre de queue tordue, dérive, pale d'hélice, carter
    pcs = [(300, y - 30, -0.25, 260, 26), (640, y - 10, 0.15, 200, 34), (820, y - 40, -0.6, 140, 14)]
    for (x, yy, ang, L, wd) in pcs:
        c.save(); c.translate(x, yy); c.rotate(ang)
        rr(c, -L / 2, -wd / 2, L, wd, wd / 2); c.set_source_rgb(0.18, 0.22, 0.24); c.fill()
        for m in range(6):
            c.new_path(); c.arc(-L / 2 + L * r.random(), r.uniform(-wd / 2, wd / 2), r.uniform(3, 8), 0, 7); c.set_source_rgba(0.35, 0.28, 0.20, 0.8); c.fill()
        c.restore()
    c.new_path(); c.move_to(250, y - 50); c.line_to(300, y - 150); c.line_to(345, y - 150); c.line_to(330, y - 40); c.close_path(); c.set_source_rgb(0.20, 0.24, 0.27); c.fill()
    # lampe
    tx, ty = torch
    c.save(); c.set_operator(cairo.OPERATOR_ADD)
    g = cairo.RadialGradient(tx, ty, 10, tx, ty, tr); g.add_color_stop_rgba(0, 0.9, 0.95, 0.85, 0.45 * k); g.add_color_stop_rgba(1, 0.9, 0.95, 0.85, 0)
    c.new_path(); c.arc(tx, ty, tr, 0, 7); c.set_source(g); c.fill(); c.restore()


def diver(c, x, y, s, t, a=1.0, beam=1.0):
    """plongeur en silhouette, tête en bas, lampe dont le faisceau éclaire vers le bas."""
    if beam > 0:
        c.save(); c.set_operator(cairo.OPERATOR_ADD)
        g = cairo.LinearGradient(x, y + 40 * s, x, y + 900 * s); g.add_color_stop_rgba(0, 0.9, 0.95, 0.85, 0.35 * beam); g.add_color_stop_rgba(1, 0.9, 0.95, 0.85, 0)
        c.new_path(); c.move_to(x - 10 * s, y + 40 * s); c.line_to(x + 10 * s, y + 40 * s); c.line_to(x + 260 * s, y + 900 * s); c.line_to(x - 260 * s, y + 900 * s); c.close_path(); c.set_source(g); c.fill(); c.restore()
    c.save(); c.translate(x, y); c.scale(s, s); c.set_source_rgba(0.02, 0.03, 0.05, a)
    c.new_path(); c.arc(0, 30, 16, 0, 7); c.fill()                                  # tête (en bas)
    rr(c, -20, -70, 40, 95, 16); c.fill(); rr(c, -26, -60, 14, 60, 6); c.fill()         # corps + bouteille
    kick = math.sin(t * 3) * 12
    for d_ in (-1, 1):
        c.move_to(d_ * 10, -68); c.line_to(d_ * 14 + kick * d_, -150); c.set_line_width(14); c.set_line_cap(1); c.stroke()
        c.new_path(); c.move_to(d_ * 14 + kick * d_ - 14, -150); c.line_to(d_ * 14 + kick * d_ + 14, -150); c.line_to(d_ * 14 + kick * d_, -200); c.close_path(); c.fill()
    c.move_to(-16, 0); c.line_to(-30, 40); c.move_to(16, 0); c.line_to(10, 44); c.set_line_width(10); c.stroke()
    c.restore()
    for j in range(6):                                                           # bulles qui remontent
        ph = (t * 0.8 + j / 6) % 1
        c.new_path(); c.arc(x + 10 * math.sin(t * 3 + j) - 10, y - 80 * s - ph * 500, 4 + 4 * ph, 0, 7); c.set_source_rgba(0.8, 0.9, 1, 0.5 * (1 - ph) * a); c.set_line_width(2); c.stroke()


def depth_gauge(c, x, y, d, a=1.0):
    c.new_path(); c.arc(x, y, 120, 0, 7); c.set_source_rgba(0.02, 0.04, 0.06, 0.75 * a); c.fill_preserve(); c.set_source_rgba(*CY, 0.8 * a); c.set_line_width(4); c.stroke()
    for m in range(0, 101, 10):
        an = math.radians(135 + 270 * m / 100)
        c.move_to(x + 96 * math.cos(an), y + 96 * math.sin(an)); c.line_to(x + 110 * math.cos(an), y + 110 * math.sin(an)); c.set_source_rgba(*CY, 0.8 * a); c.set_line_width(3); c.stroke()
    an = math.radians(135 + 270 * min(d, 100) / 100)
    c.move_to(x, y); c.line_to(x + 90 * math.cos(an), y + 90 * math.sin(an)); c.set_source_rgba(*YEL, a); c.set_line_width(6); c.set_line_cap(1); c.stroke()
    letter(c, f"{int(d)} M", x, y + 70, 46, WH, a)


def boat(c, x, y, s, t, a=1.0, col=(0.06, 0.06, 0.09)):
    """chalutier en silhouette."""
    c.save(); c.translate(x, y + 4 * math.sin(t * 1.4)); c.rotate(0.02 * math.sin(t * 1.1)); c.scale(s, s)
    c.new_path(); c.move_to(-220, -30); c.line_to(220, -40); c.line_to(180, 30); c.line_to(-190, 30); c.close_path(); c.set_source_rgba(*col, a); c.fill()
    rr(c, -40, -110, 110, 75, 6); c.fill(); c.rectangle(-150, -200, 10, 170); c.fill()
    c.move_to(-145, -195); c.line_to(-260, 20); c.set_line_width(4); c.stroke()
    c.restore()


def stencil_panel(c, t, cx, cy, reveal, beam):
    """tôle corrodée avec le numéro peint « 2734 L », révélé par le faisceau."""
    c.save()
    rr(c, cx - 330, cy - 150, 660, 300, 20)
    g = cairo.LinearGradient(cx - 330, cy - 150, cx + 330, cy + 150); g.add_color_stop_rgb(0, 0.20, 0.24, 0.26); g.add_color_stop_rgb(1, 0.12, 0.14, 0.16)
    c.set_source(g); c.fill()
    r = random.Random(9)
    for j in range(120):
        c.new_path(); c.arc(cx + r.uniform(-320, 320), cy + r.uniform(-140, 140), r.uniform(2, 14), 0, 7); c.set_source_rgba(0.40, 0.30, 0.18, r.uniform(0.2, 0.6)); c.fill()
    for rx in (-300, 300):
        for ry in (-120, 120):
            c.new_path(); c.arc(cx + rx, cy + ry, 7, 0, 7); c.set_source_rgba(0.5, 0.5, 0.5, 0.7); c.fill()
    letter(c, "2734 L", cx, cy + 50, 170, (0.85, 0.82, 0.70), 0.85 * reveal, 'Bebas Neue')
    bx, by = beam
    c.save(); c.set_operator(cairo.OPERATOR_ADD)
    g = cairo.RadialGradient(bx, by, 10, bx, by, 300); g.add_color_stop_rgba(0, 1, 0.97, 0.85, 0.55); g.add_color_stop_rgba(1, 1, 0.97, 0.85, 0)
    c.new_path(); c.arc(bx, by, 300, 0, 7); c.set_source(g); c.fill(); c.restore()
    c.restore()


def card(c, x, y, w, h, txt, col, a):
    if a <= 0: return
    c.push_group()
    rr(c, x - w / 2, y - h / 2, w, h, 24); c.set_source_rgba(0.03, 0.04, 0.07, 0.85); c.fill_preserve(); c.set_source_rgba(*col, 1); c.set_line_width(5); c.stroke()
    letter(c, txt, x, y + h * 0.18, h * 0.55, col, 1.0)
    c.pop_group_to_source(); c.paint_with_alpha(a)


# =============================================================== scènes
def sc_sx_hook(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        sea(c, t, 'dusk')
        q = ap(t, sg['sent'][0][0], sg['sent'][0][1] + 0.3)
        P = plane(c, 'p38_hero', 700 - 260 * q, 640 + 60 * q, 0.30, alpha=1 - ap(q, 0.65, 1.0))
        clouds(c, t, 0.4 + 0.6 * ap(q, 0.5, 1.0), 560, 900, (1.0, 0.80, 0.75), 120)
        tag(c, "31 JUILLET 1944", 540, 1285, YEL, ap(p, 0.2, 0.35), 54)
    elif k == 1:
        sea(c, t, 'night')
        b = sg['sent'][1]; q = ap(t, b[0], b[1] - 0.2)
        yr = 1944 + int(54 * eout(q))
        panel(c, 260, 470, 560, 260, 0.55)
        letter(c, str(yr), 540, 660, 190, YEL if yr < 1998 else GRN)
        letter(c, "PERSONNE NE SAIT OÙ", 540, 1285, 64, WH, ap(p, 0.3, 0.5))
    else:
        sea(c, t, 'night')
        c.set_source_rgba(0, 0, 0, 0.25); c.paint()
        plane(c, 'p38_hero', 540, 720, 0.20, alpha=0.35, dark=0.6)
        stamp(c, "LA FIN DE L'HISTOIRE ?", 540, 560, 100, YEL, since, glow=1.0)


def sc_sx_takeoff(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        b = sg['sent'][0]; tm = b[0] + 0.52 * (b[1] - b[0])
        if t < tm:
            q = ap(t, b[0], tm)
            M = map_med(c, t)
            borgo, mrs = M(9.48, 42.55), M(5.37, 43.30)
            dest = M(5.9, 43.75)
            xy = curve_pts(borgo, dest, 0.10)
            hx, hy = route(c, xy, ap(q, 0.15, 1.0))
            if q > 0.15:
                i = max(1, int(len(xy) * ap(q, 0.15, 1.0)) - 1); ang = math.atan2(xy[i][1] - xy[i - 1][1], xy[i][0] - xy[i - 1][0])
                plane_icon(c, hx, hy, ang, 1.5, (1, 1, 1), 1.0)
            for nm, (x, y), anc, dx, dy in (("BORGO (CORSE)", borgo, 'r', -20, 55), ("MARSEILLE", mrs, 'l', 10, 55)):
                c.new_path(); c.arc(x, y, 10, 0, 7); c.set_source_rgb(1, 1, 1); c.fill()
                letter(c, nm, x + dx, y + dy, 36, WH, 1.0, anchor=anc)
            letter(c, "PROVENCE", *M(5.9, 43.95), 46, (0.6, 0.72, 0.85), 0.85)
            letter(c, "MER MÉDITERRANÉE", *M(6.6, 42.4), 38, (0.45, 0.6, 0.8), 0.7, 'Montserrat')
            panel(c, 250, 380, 580, 150, 0.55)
            letter(c, "31 JUILLET 1944", 540, 485, 92, YEL, ap(q, 0.0, 0.12))
            tag(c, "SAINT-EXUPÉRY, 44 ANS", 540, 1285, WH, ap(q, 0.3, 0.45), 52)
        else:
            q = ap(t, tm, b[1] + 0.2)
            sky_paint(c, 'day', t)
            clouds(c, t, 0.6, 1050, 1400, (1, 1, 1), 160, seed=8)
            x, y, sc = 540, 760, 0.46
            plane(c, 'p38_side', x, y, sc)
            # balayage radiographique : la partie gauche du balai montre le rendu « rayons X »
            sw = -100 + 1300 * ap(q, 0.05, 0.6)
            c.save(); c.rectangle(-10, 0, sw + 10, H); c.clip(); plane(c, 'p38_side', x, y, sc, xray=True); c.restore()
            c.rectangle(sw - 3, 520, 6, 480); c.set_source_rgba(*CY, 0.8 * (1 - ap(q, 0.6, 0.7))); c.fill()
            nx, ny = P10.plane(c, 'p38_side', x, y, sc, alpha=0.0)('nose')
            if q > 0.45:
                a = ap(q, 0.45, 0.6)
                for j in range(3): camera_icon(c, nx - 70 - j * 70, ny - 8, 0.8, YEL, a)
                glow(c, nx - 140, ny, 120, YEL, 0.3 * a)
                tag(c, "DES APPAREILS PHOTO, PAS D'ARMES", 540, 1285, YEL, a, 46)
            letter(c, "P-38 LIGHTNING", 540, 470, 96, WH, ap(q, 0.0, 0.15))
    else:
        M = map_med(c, t, 2.2, 540, 900, *JM.MAP['med'](5.9, 43.45))
        b = sg['sent'][1]
        shots = [(5.40, 43.30), (6.00, 43.12), (6.60, 43.25), (5.70, 43.70)]
        for j, (lo, la) in enumerate(shots):
            t0 = b[0] + 0.15 * (b[1] - b[0]) + j * 0.7
            x, y = M(lo, la); a = ap(t, t0 - 0.35, t0)
            if a <= 0: continue
            fw, fh = 300, 200
            c.set_source_rgba(1, 1, 1, 0.9 * a); c.set_line_width(4)
            for sx_, sy_ in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                c.move_to(x + sx_ * fw / 2, y + sy_ * (fh / 2 - 30)); c.line_to(x + sx_ * fw / 2, y + sy_ * fh / 2); c.line_to(x + sx_ * (fw / 2 - 30), y + sy_ * fh / 2); c.stroke()
            c.move_to(x - 16, y); c.line_to(x + 16, y); c.move_to(x, y - 16); c.line_to(x, y + 16); c.stroke()
            if t > t0:
                fl = max(0, 1 - (t - t0) / 0.25)
                c.rectangle(x - fw / 2, y - fh / 2, fw, fh); c.set_source_rgba(1, 1, 1, 0.6 * fl); c.fill()
                # vignette « photo » qui file vers le bas
                d = ap(t, t0, t0 + 0.5); px = 170 + j * 245; py = 1150
                tx_, ty_ = x + (px - x) * d, y + (py - y) * d
                rr(c, tx_ - 105, ty_ - 70, 210, 140, 6); c.set_source_rgba(0.92, 0.88, 0.78, 0.95); c.fill()
                rr(c, tx_ - 95, ty_ - 60, 190, 110, 4); c.set_source_rgba(0.35, 0.33, 0.28, 0.95); c.fill()
                letter(c, f"N° {j + 1}", tx_, ty_ + 62, 22, (0.2, 0.2, 0.2), 1.0, 'Montserrat')
        letter(c, "MISSION PHOTO", 540, 470, 96, YEL, ap(p, 0.0, 0.12))
        tag(c, "AVANT LE DÉBARQUEMENT DE PROVENCE", 540, 1285, WH, ap(p, 0.5, 0.65), 44)


def sc_sx_vanish(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    c.set_source_rgb(0.0, 0.02, 0.01); c.paint()
    b0 = sg['sent'][0][0]; last = b0 + 1.0
    vis = 1.0 if t < last else max(0.0, 1 - (t - last) / 0.4)
    blips = [(0.35, -0.45, 12, (0.4, 1, 0.5))] if vis > 0 else []
    if vis > 0 and vis < 1: blips = [(0.35, -0.45, 12 * vis, (1, 0.4, 0.3))]
    radar_scope(c, 540, 820, 400, t, blips, 1.0)
    if t >= last:
        x, y = 540 + 0.35 * 400, 820 - 0.45 * 400
        ph = ((t - last) * 0.8) % 1
        c.new_path(); c.arc(x, y, 14 + 70 * ph, 0, 7); c.set_source_rgba(1, 0.4, 0.3, 0.8 * (1 - ph)); c.set_line_width(3); c.stroke()
        letter(c, "?", x + 50, y - 30, 80, (1, 0.5, 0.4), ap(t, last, last + 0.4))
    if k == 0:
        tag(c, "DERNIER ÉCHO RADAR", 540, 1285, (0.4, 1, 0.5), ap(p, 0.1, 0.25), 54)
    else:
        stamp(c, "DISPARU", 540, 1285, 130, RED, since, glow=1.0)


def sc_sx_bracelet(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        sea(c, t, 'dawn', 1000, (300, 980))
        boat(c, 620, 1010, 1.0, t)
        q = ap(p, 0.4, 0.9)
        c.move_to(360, 1020); c.line_to(300 - 40 * q, 1180 - 180 * q); c.set_source_rgba(0.1, 0.1, 0.12, 0.9); c.set_line_width(3); c.stroke()
        if q > 0:
            gx, gy = 300 - 40 * q, 1180 - 180 * q
            glow(c, gx, gy, 60, (1, 1, 1), 0.8 * q); glow(c, gx, gy, 16, (1, 1, 1), q)
        panel(c, 380, 380, 320, 150, 0.55)
        letter(c, "1998", 540, 490, 110, YEL)
        tag(c, "UN PÊCHEUR MARSEILLAIS", 540, 1285, WH, ap(p, 0.15, 0.3), 52)
    else:
        g = cairo.RadialGradient(540, 760, 50, 540, 760, 900); g.add_color_stop_rgb(0, 0.12, 0.13, 0.17); g.add_color_stop_rgb(1, 0.01, 0.01, 0.02)
        c.set_source(g); c.paint()
        b = sg['sent'][1]
        bracelet(c, t, ap(t, b[0], b[1] + 0.3))
        tag(c, "CONSUELO : SA FEMME", 540, 1285, YEL, ap(p, 0.55, 0.7), 52)
        letter(c, "UNE GOURMETTE EN ARGENT", 540, 470, 60, WH, ap(p, 0.0, 0.2), 'Montserrat')


def sc_sx_wreck(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        b = sg['sent'][0]; q = ap(t, b[0], b[1] - 0.3)
        d = 85 * eout(q)
        underwater(c, t, d)
        if q > 0.7: seabed(c, t, 1180 + 400 * (1 - ap(q, 0.7, 1.0)), (560, 1060), 420, ap(q, 0.8, 1.0))
        diver(c, 560 + 20 * math.sin(t * 0.7), 700 + 40 * math.sin(t * 0.5), 1.4, t)
        c.save(); c.translate(860, 470); c.scale(1.25, 1.25); depth_gauge(c, 0, 0, d); c.restore()
        tag(c, "ÎLE DE RIOU · MARSEILLE", 540, 1285, CY, ap(p, 0.45, 0.6), 50)
    elif k == 1:
        underwater(c, t, 85)
        b = sg['sent'][1]; q = ap(t, b[0], b[1])
        stencil_panel(c, t, 540, 780, ap(q, 0.25, 0.55), (300 + 480 * q, 760 + 40 * math.sin(t * 2)))
        letter(c, "2003", 540, 470, 110, YEL, ap(q, 0.0, 0.1))
        if q > 0.6: stamp(c, "C'EST BIEN SON AVION", 540, 1285, 84, GRN, t - (b[0] + 0.6 * (b[1] - b[0])), glow=1.0)
    else:
        g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, 0.03, 0.03, 0.05); g.add_color_stop_rgb(1, 0.10, 0.09, 0.08)
        c.set_source(g); c.paint()
        for x in (300, 780):                                                     # projecteurs
            c.save(); c.set_operator(cairo.OPERATOR_ADD)
            g = cairo.LinearGradient(x, 200, x, 1100); g.add_color_stop_rgba(0, 1, 0.95, 0.8, 0.18); g.add_color_stop_rgba(1, 1, 0.95, 0.8, 0.02)
            c.new_path(); c.move_to(x - 20, 200); c.line_to(x + 20, 200); c.line_to(x + 260, 1100); c.line_to(x - 260, 1100); c.close_path(); c.set_source(g); c.fill(); c.restore()
        rr(c, 160, 1060, 760, 60, 8); c.set_source_rgb(0.16, 0.15, 0.14); c.fill()
        seabed_items = [(330, 1030, -0.1, 280, 30), (620, 1040, 0.05, 220, 40), (820, 1010, -0.3, 150, 16)]
        for (x, y, ang, L, wd) in seabed_items:
            c.save(); c.translate(x, y); c.rotate(ang); rr(c, -L / 2, -wd / 2, L, wd, wd / 2); c.set_source_rgb(0.42, 0.40, 0.36); c.fill(); c.restore()
        c.new_path(); c.move_to(260, 1000); c.line_to(300, 880); c.line_to(345, 880); c.line_to(335, 1010); c.close_path(); c.set_source_rgb(0.40, 0.38, 0.34); c.fill()
        letter(c, "LE BOURGET", 540, 520, 110, WH, ap(p, 0.0, 0.15))
        tag(c, "MUSÉE DE L'AIR ET DE L'ESPACE", 540, 1285, YEL, ap(p, 0.2, 0.35), 50)


def sc_sx_claim(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    sky_paint(c, 'day', t)
    clouds(c, t, 0.7, 1000, 1350, (1, 1, 1), 140, seed=12)
    gray = 0.0 if k == 0 else round(0.55 * ap(p, 0.0, 0.4), 1)
    P = plane(c, 'bf_34', 540 + 30 * math.sin(t * 0.5), 780, 0.85, dark=gray)
    if k == 0:
        panel(c, 380, 380, 320, 150, 0.55)
        letter(c, "2008", 540, 490, 110, YEL)
        tag(c, "UN EX-PILOTE ALLEMAND AFFIRME L'AVOIR ABATTU", 540, 1285, WH, ap(p, 0.2, 0.35), 40)
    else:
        r = random.Random(3)
        for j in range(5):
            a = ap(t, sg['sent'][1][0] + 0.2 + j * 0.3, sg['sent'][1][0] + 0.5 + j * 0.3)
            letter(c, "?", r.uniform(180, 900), r.uniform(560, 1050), r.uniform(90, 150), RED, a)
        stamp(c, "INCOHÉRENCES", 540, 1285, 110, RED, since - 0.3, glow=1.0)


def sc_sx_verdict(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        sea(c, t, 'night'); c.set_source_rgba(0, 0, 0, 0.3); c.paint()
        b = sg['sent'][0]; L = b[1] - b[0]
        for j, (txt, col) in enumerate((("ABATTU ?", RED), ("PANNE ?", ORG), ("MALAISE ?", YEL))):
            card(c, 540, 560 + j * 230, 700, 180, txt, col, ap(t, b[0] + j * L * 0.3, b[0] + j * L * 0.3 + 0.2))
    elif k == 1:
        sea(c, t, 'dusk')
        q = ap(t, sg['sent'][1][0], sg['sent'][1][1] + 0.4)
        plane(c, 'p38_hero', 560 - 120 * q, 700 - 60 * q, 0.22 - 0.1 * q, alpha=1 - ap(q, 0.5, 1.0))
        clouds(c, t, 0.3 + 0.7 * ap(q, 0.4, 1.0), 560, 860, (1.0, 0.8, 0.75), 120)
        letter(c, "PERSONNE NE SAIT", 540, 1285, 80, WH, ap(p, 0.2, 0.4))
    else:
        sea(c, t, 'dusk')
        stamp(c, "ET TOI ?", 540, 600, 170, ORG, since, glow=1.0)
        letter(c, "ABATTU : OUI OU NON ?", 540, 720, 60, WH, ap(since, 0.3, 0.6), 'Montserrat')


SC14 = {k[3:]: v for k, v in globals().items() if k.startswith('sc_') and callable(v)}
