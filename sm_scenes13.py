"""30/10 : SURVIVRAIS-TU ? « Juliane Koepcke » (LANSA 508, 1971) en style cinéma (jk_*) et GRANDS CRASHS « Ténérife 1977 » (tf_*).
Juliane : jungle peinte en 2D (pr/jungle2d.py -> p_jg_air|top|floor|river), Electra en silhouette 2D (orage de nuit), carte topo pr/map_peru.png.
Ténérife : 747-200 FlightGear (pr/r_pa_*, pr/r_klm_*) dans le brouillard, carte pr/map_canary.png, plan de l'aéroport en radiographie,
signature « radio brouillée » (deux ondes qui s'additionnent en sifflement)."""
import cairo, math, random
import numpy as np
from PIL import Image
from sm_lib import *
from sm_scenes2 import ease, ap, ORG, BLUE, RED, WH, GRN
from sm_scenes6 import si, stamp, eout, YEL
from sm_scenes7 import tag, label, check, cross
import sm_scenes10 as P10
from sm_scenes10 import plane, glow, letter, panel, counter, flame, smoke_col, tower
import sm_scenes12 as S12
from sm_scenes12 import sky_paint, walker, plane_icon
import pr.jk_maps as JM
R = None
CY = (0.40, 0.88, 1.0)


def mixc(a, b, f):
    return tuple(x + (y - x) * f for x, y in zip(a, b))


def img(c, name, x, y, sc, alpha=1.0, mode=None):
    """plaque (pr/p_<name>.png) posée en (x, y) à l'échelle sc ; mode = étalonnage plate_g (day/dusk/night)."""
    if mode:
        s, (w, h) = S12.plate_g(name, mode)
    else:
        s, (w, h) = P10.plate(f'p_{name}.png')
    c.save(); c.translate(x, y); c.scale(sc, sc); c.set_source_surface(s, 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD)
    if name == 'jg_top': c.get_source().set_extend(cairo.EXTEND_REFLECT)       # vue de dessus : miroir sans couture quand on dézoome
    c.paint_with_alpha(alpha); c.restore()
    return w, h


def plate_fit(c, name, mode=None, zoom=1.0, pan=0.0, dy=0.0, cx=0.5, cy=0.5, alpha=1.0, sky=None):
    if sky: sky_paint(c, sky, 0.0)
    if mode:
        _, (w, h) = S12.plate_g(name, mode)
    else:
        _, (w, h) = P10.plate(f'p_{name}.png')
    sc = max(W / w, H / h) * zoom
    x = W / 2 - w * sc * cx + pan; y = H / 2 - h * sc * cy + dy
    img(c, name, x, y, sc, alpha, mode)
    return x, y, sc


def bottom_shade(c, a=0.6):
    g = cairo.LinearGradient(0, 1250, 0, H); g.add_color_stop_rgba(0, 0, 0, 0.02, 0); g.add_color_stop_rgba(1, 0, 0, 0.02, a)
    c.rectangle(0, 1250, W, H - 1250); c.set_source(g); c.fill()


def rays(c, t, x0, a=1.0, n=7, seed=3, col=(1.0, 0.95, 0.75)):
    """rais de lumière à travers la canopée (additifs, lente respiration)."""
    r = random.Random(seed)
    c.save(); c.set_operator(cairo.OPERATOR_ADD)
    for j in range(n):
        x = x0 + r.uniform(-420, 420); w = r.uniform(30, 110); ang = r.uniform(0.18, 0.32)
        br = a * (0.10 + 0.08 * math.sin(t * 0.9 + j * 1.7))
        g = cairo.LinearGradient(x, 0, x + math.tan(ang) * 1500, 1500)
        g.add_color_stop_rgba(0, *col, br); g.add_color_stop_rgba(0.7, *col, br * 0.4); g.add_color_stop_rgba(1, *col, 0)
        c.new_path(); c.move_to(x, -20); c.line_to(x + w, -20); c.line_to(x + w + math.tan(ang) * 1600, 1580); c.line_to(x + math.tan(ang) * 1600 - w * 0.5, 1580); c.close_path()
        c.set_source(g); c.fill()
    c.restore()


def motes(c, t, a=1.0, n=50, seed=6):
    r = random.Random(seed)
    for j in range(n):
        x = (r.random() * W + 12 * math.sin(t * 0.5 + j)) % W; y = (r.random() * 1400 - t * r.uniform(4, 14)) % 1400
        c.new_path(); c.arc(x, y, r.uniform(1, 2.6), 0, 7); c.set_source_rgba(1, 1, 0.85, a * r.uniform(0.2, 0.6)); c.fill()


# =============================================================== Electra (silhouette 2D, nez à droite)
def _electra_path(c, part=None):
    """profil en mètres (origine au centre, nez à +16 m, haut = -y). part : None | 'nose' | 'mid' | 'tail' (même dessin, découpé)."""
    c.new_path()
    # fuselage
    c.move_to(16.2, 0.2); c.curve_to(16.2, -1.2, 15.2, -1.9, 13.6, -1.9); c.line_to(-9.5, -1.9); c.curve_to(-12.5, -1.8, -14.8, -1.3, -16.0, -0.8)
    c.line_to(-16.0, -0.2); c.curve_to(-14.5, 0.5, -12.0, 1.2, -9.0, 1.6); c.line_to(12.5, 1.6); c.curve_to(15.0, 1.5, 16.2, 1.0, 16.2, 0.2); c.close_path()
    # dérive
    c.move_to(-9.0, -1.8); c.line_to(-13.6, -6.6); c.line_to(-15.6, -6.6); c.line_to(-15.4, -1.2); c.close_path()
    # stabilisateur (léger dièdre)
    c.move_to(-11.5, -0.9); c.line_to(-16.2, -1.5); c.line_to(-16.4, -0.9); c.line_to(-12.0, -0.3); c.close_path()
    # aile basse (vue de profil : profil épais)
    c.move_to(4.2, 1.1); c.curve_to(3.6, 2.0, 0.0, 2.1, -2.2, 1.7); c.line_to(-1.6, 1.0); c.close_path()


def electra(c, x, y, s, rot=0.0, a=1.0, lit=0.0, t=0.0, night=True, pieces=None, fire=0.0):
    """Lockheed L-188 Electra de profil. s = px par mètre. lit = éclair (0..1).
    pieces = dict(nose=(dx,dy,rot), mid=(...), tail=(...)) pour la rupture en vol (en px / rad)."""
    body = (0.10, 0.12, 0.16) if night else (0.80, 0.82, 0.86)
    body = mixc(body, (0.85, 0.88, 0.95), lit * 0.8)
    rim = mixc((0.55, 0.65, 0.85), (1, 1, 1), lit)
    cuts = {'nose': (3.0, 30), 'mid': (-6.0, 3.0), 'tail': (-30, -6.0)}
    for part, (x0, x1) in (cuts.items() if pieces else [(None, (-30, 30))]):
        dx, dy, dr = pieces.get(part, (0, 0, 0)) if pieces else (0, 0, 0)
        c.save(); c.translate(x + dx, y + dy); c.rotate(rot + dr); c.scale(s, s)
        c.rectangle(x0, -12, x1 - x0, 24); c.clip()
        _electra_path(c)
        c.set_source_rgba(*body, a); c.fill_preserve()
        c.set_source_rgba(*rim, a * (0.35 + 0.6 * lit)); c.set_line_width(0.12); c.stroke()
        # hublots allumés
        for j in range(16):
            wx = 10.5 - j * 1.25
            if not (x0 < wx < x1): continue
            c.rectangle(wx, -0.9, 0.42, 0.55); c.set_source_rgba(1.0, 0.85, 0.55, a * (0.85 if night else 0.5)); c.fill()
        c.move_to(13.4, -1.2); c.line_to(15.0, -1.0); c.line_to(14.8, -0.5); c.line_to(13.2, -0.6); c.close_path(); c.set_source_rgba(0.6, 0.75, 0.9, a * 0.6); c.fill()
        # nacelles + hélices (moteurs 1-2 visibles ; 3-4 derrière, plus sombres)
        for (nx0, ny, dk) in ((5.2, 1.0, 0.55), (3.6, 1.5, 1.0)):
            if not (x0 < nx0 + 2 and nx0 - 6 < x1): continue
            nb = mixc(body, (0, 0, 0), 0.35 * (1 - dk))
            c.new_path(); c.move_to(nx0 - 6.5, ny - 0.5); c.line_to(nx0 - 0.4, ny - 0.95); c.curve_to(nx0 + 0.4, ny - 0.9, nx0 + 0.6, ny - 0.4, nx0 + 0.6, ny)
            c.curve_to(nx0 + 0.6, ny + 0.4, nx0 + 0.4, ny + 0.9, nx0 - 0.4, ny + 0.95); c.line_to(nx0 - 6.5, ny + 0.7); c.close_path()
            c.set_source_rgba(*nb, a); c.fill_preserve(); c.set_source_rgba(*rim, a * 0.3); c.set_line_width(0.08); c.stroke()
            c.new_path(); c.move_to(nx0 + 0.6, ny - 0.35); c.line_to(nx0 + 1.3, ny); c.line_to(nx0 + 0.6, ny + 0.35); c.close_path(); c.set_source_rgba(*rim, a * 0.8); c.fill()   # cône d'hélice
            c.save(); c.translate(nx0 + 0.9, ny); c.scale(0.38, 1)
            c.new_path(); c.arc(0, 0, 2.05, 0, 7); c.set_source_rgba(*rim, a * 0.16); c.fill_preserve(); c.set_source_rgba(*rim, a * 0.35); c.set_line_width(0.1); c.stroke()
            ph = (t * 7 + nx0) % 1
            for bl in range(4):
                an = ph * 6.283 + bl * 1.5708
                c.move_to(0, 0); c.line_to(2.0 * math.cos(an), 2.0 * math.sin(an)); c.set_source_rgba(*rim, a * 0.28); c.set_line_width(0.35); c.stroke()
            c.restore()
        c.restore()


def storm_sky(c, t, flash=0.0, dusk=False, seed=4, rain=1.0):
    """nuit d'orage : nuages en couches, éclairés par les éclairs ; pluie oblique."""
    g = cairo.LinearGradient(0, 0, 0, H)
    if dusk:
        g.add_color_stop_rgb(0, 0.10, 0.10, 0.20); g.add_color_stop_rgb(0.6, 0.42, 0.28, 0.36); g.add_color_stop_rgb(1, 0.70, 0.42, 0.30)
    else:
        g.add_color_stop_rgb(0, 0.01, 0.015, 0.035); g.add_color_stop_rgb(1, 0.05, 0.06, 0.10)
    c.set_source(g); c.paint()
    r = random.Random(seed)
    for layer in range(4):
        for j in range(16):
            x = (r.uniform(-200, W + 200) - t * (12 + layer * 18)) % (W + 600) - 300; y = r.uniform(-100, H + 100); rad = r.uniform(180, 420) * (1.3 - layer * 0.15)
            base = (0.06, 0.07, 0.10) if not dusk else (0.30, 0.22, 0.28)
            col = mixc(base, (0.75, 0.78, 0.95), flash * (0.35 + 0.15 * layer))
            glow(c, x, y, rad, col, 0.55)
    if flash > 0:
        c.save(); c.set_operator(cairo.OPERATOR_ADD); c.set_source_rgba(0.55, 0.6, 0.85, 0.35 * flash); c.paint(); c.restore()
    if rain > 0:
        for j in range(160):
            x0 = r.random() * (W + 400); y0 = r.random() * H; sp = r.uniform(1800, 2600)
            y = (y0 + t * sp) % (H + 100) - 50; x = (x0 - (y0 + t * sp) * 0.35) % (W + 400) - 200
            c.move_to(x, y); c.line_to(x - 14, y + 40); c.set_source_rgba(0.75, 0.8, 0.95, rain * (0.18 + 0.25 * flash)); c.set_line_width(1.6); c.stroke()


def bolt(c, x0, y0, x1, y1, a=1.0, seed=1, w=5.0, branches=True):
    """éclair : ligne brisée fractale avec halo."""
    if a <= 0: return
    r = random.Random(seed)
    def seg(ax, ay, bx, by, d):
        if d == 0 or math.hypot(bx - ax, by - ay) < 18: return [(ax, ay), (bx, by)]
        mx, my = (ax + bx) / 2 + r.uniform(-0.22, 0.22) * (by - ay), (ay + by) / 2 + r.uniform(-0.1, 0.1) * (bx - ax)
        return seg(ax, ay, mx, my, d - 1)[:-1] + seg(mx, my, bx, by, d - 1)
    pts = seg(x0, y0, x1, y1, 6)
    paths = [pts]
    if branches:
        for j in range(3):
            i = r.randint(len(pts) // 5, len(pts) * 3 // 4); bx, by = pts[i]
            paths.append(seg(bx, by, bx + r.uniform(-260, 260), by + r.uniform(120, 300), 4))
    c.save(); c.set_operator(cairo.OPERATOR_ADD); c.set_line_join(1); c.set_line_cap(1)
    for k, pp in enumerate(paths):
        ww = w if k == 0 else w * 0.5
        for lw, col, aa in ((ww * 9, (0.45, 0.5, 1.0), 0.10), (ww * 3.2, (0.7, 0.75, 1.0), 0.3), (ww, (1, 1, 1), 1.0)):
            c.new_path(); c.move_to(*pp[0])
            for q in pp[1:]: c.line_to(*q)
            c.set_source_rgba(*col, aa * a); c.set_line_width(lw); c.stroke()
    c.restore()


def flash_at(t, times, dur=0.22):
    """intensité d'éclair (double impulsion) aux instants donnés."""
    v = 0.0
    for t0 in times:
        d = t - t0
        if 0 <= d < dur * 2.2:
            v = max(v, math.exp(-d / dur * 3) + 0.7 * math.exp(-max(0, d - dur * 0.8) / dur * 4) * (d > dur * 0.8))
    return min(1.0, v)


# =============================================================== siège, pictogrammes
def seat_top(c, x, y, s, rot, a=1.0, person=True, lit=(0.85, 0.9, 1.0)):
    """rangée de 3 sièges vue de dessus, une silhouette attachée au milieu (pictogramme)."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    for j in (-1, 0, 1):
        rr(c, j * 64 - 29, -40, 58, 74, 12); c.set_source_rgba(0.16, 0.20, 0.30, a); c.fill_preserve(); c.set_source_rgba(*lit, 0.6 * a); c.set_line_width(3); c.stroke()
        rr(c, j * 64 - 29, -58, 58, 20, 8); c.set_source_rgba(0.22, 0.27, 0.40, a); c.fill_preserve(); c.set_source_rgba(*lit, 0.6 * a); c.stroke()
    rr(c, -110, 30, 220, 10, 4); c.set_source_rgba(0.5, 0.52, 0.56, a); c.fill()
    if person:
        c.new_path(); c.arc(0, -30, 17, 0, 7); c.set_source_rgba(0.95, 0.85, 0.75, a); c.fill()
        rr(c, -24, -14, 48, 40, 14); c.set_source_rgba(0.9, 0.92, 0.95, a); c.fill()
        c.move_to(-30, 12); c.line_to(30, 12); c.set_source_rgba(*RED, a); c.set_line_width(5); c.stroke()      # ceinture
        for d in (-1, 1):
            c.move_to(d * 22, -6); c.line_to(d * 46, 18 + 8 * math.sin(rot * 3)); c.set_source_rgba(0.9, 0.92, 0.95, a); c.set_line_width(9); c.set_line_cap(1); c.stroke()
    c.restore()


def seat_side(c, x, y, s, a=1.0, tilt=0.0, col=(0.10, 0.12, 0.16), rim=(0.8, 0.9, 0.7)):
    """rangée de sièges renversée au sol (profil)."""
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(s, s)
    c.new_path(); c.move_to(-60, 0); c.line_to(40, 0); c.line_to(50, -14); c.line_to(-50, -18); c.close_path()
    c.move_to(-60, -6); c.line_to(-90, -120); c.line_to(-72, -126); c.line_to(-44, -14); c.close_path()
    c.move_to(-30, 0); c.line_to(-36, 40); c.line_to(-28, 40); c.line_to(-22, 0); c.close_path()
    c.move_to(20, 0); c.line_to(26, 40); c.line_to(34, 40); c.line_to(28, 0); c.close_path()
    c.set_source_rgba(*col, a); c.fill_preserve(); c.set_source_rgba(*rim, 0.45 * a); c.set_line_width(2.5); c.stroke()
    c.restore()


def person_front(c, x, y, s, a=1.0, col=CY, lw=4.0):
    """silhouette humaine de face, au trait (radiographie)."""
    c.save(); c.translate(x, y); c.scale(s, s); c.set_line_join(1); c.set_line_cap(1)
    c.new_path(); c.arc(0, -300, 52, 0, 7)
    c.move_to(-26, -246); c.line_to(-30, -226); c.curve_to(-90, -220, -120, -205, -128, -170); c.line_to(-150, -20); c.line_to(-136, 70)
    c.move_to(26, -246); c.line_to(30, -226); c.curve_to(90, -220, 120, -205, 128, -170); c.line_to(150, -20); c.line_to(136, 70)
    c.move_to(-100, -150); c.line_to(-96, 0); c.line_to(-80, 60); c.line_to(-72, 260); c.line_to(-60, 420)
    c.move_to(100, -150); c.line_to(96, 0); c.line_to(80, 60); c.line_to(72, 260); c.line_to(60, 420)
    c.move_to(-80, 60); c.curve_to(-30, 80, 30, 80, 80, 60)
    c.move_to(-14, 76); c.line_to(-18, 260); c.line_to(-26, 420)
    c.move_to(14, 76); c.line_to(18, 260); c.line_to(26, 420)
    c.set_source_rgba(*col, a); c.set_line_width(lw / s); c.stroke()
    # clavicules
    c.move_to(-8, -222); c.curve_to(-40, -232, -80, -222, -112, -206); c.move_to(8, -222); c.curve_to(40, -232, 80, -222, 112, -206)
    c.set_source_rgba(*col, a * 0.75); c.set_line_width(lw * 0.8 / s); c.stroke()
    c.restore()


def hut(c, x, y, s, a=1.0, col=(0.10, 0.08, 0.06), roof=(0.45, 0.36, 0.20), light=0.0):
    """abri de bûcherons sur pilotis, toit de palmes."""
    c.save(); c.translate(x, y); c.scale(s, s)
    for px in (-90, -30, 30, 90):
        c.rectangle(px - 5, -40, 10, 60); c.set_source_rgba(*col, a); c.fill()
    c.rectangle(-110, -50, 220, 14); c.fill()
    c.rectangle(-100, -150, 10, 100); c.fill(); c.rectangle(90, -150, 10, 100); c.fill()
    if light > 0: glow(c, 0, -95, 140, (1.0, 0.7, 0.35), 0.5 * light * a)
    c.new_path(); c.move_to(-150, -130); c.line_to(0, -230); c.line_to(150, -130); c.line_to(130, -120); c.line_to(0, -205); c.line_to(-130, -120); c.close_path()
    c.set_source_rgba(*roof, a); c.fill()
    for j in range(14):
        u = j / 13; px = -150 + 300 * u
        c.move_to(px, -130 - 100 * (1 - abs(u - 0.5) * 2)); c.line_to(px + (u - 0.5) * 30, -112); c.set_source_rgba(*mixc(roof, (0, 0, 0), 0.4), a); c.set_line_width(3); c.stroke()
    c.restore()


def pirogue(c, x, y, s, a=1.0, people=2, col=(0.12, 0.09, 0.06), t=0.0, fig=(0.08, 0.08, 0.1)):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.new_path(); c.move_to(-200, -18); c.curve_to(-120, 14, 120, 14, 200, -22); c.line_to(190, -8); c.curve_to(110, 22, -110, 22, -190, -6); c.close_path()
    c.set_source_rgba(*col, a); c.fill()
    for j in range(people):
        px = -100 + j * 110
        c.new_path(); c.arc(px, -86, 13, 0, 7); c.set_source_rgba(*fig, a); c.fill()
        rr(c, px - 16, -72, 32, 56, 10); c.fill()
        ang = 0.6 * math.sin(t * 2.4 + j)
        c.move_to(px, -60); c.line_to(px + 70 * math.cos(1.1 + ang), -60 + 90 * math.sin(1.1 + ang)); c.set_source_rgba(*fig, a); c.set_line_width(5); c.stroke()
    c.restore()


def ripples(c, x, y, t, a=1.0, n=4, w=120):
    for j in range(n):
        ph = (t * 0.6 + j / n) % 1
        c.save(); c.translate(x, y); c.scale(1, 0.18); c.new_path(); c.arc(0, 0, w * (0.4 + ph), 0, 7); c.restore()
        c.set_source_rgba(1, 1, 1, 0.35 * a * (1 - ph)); c.set_line_width(2.5); c.stroke()


def map_peru(c, t):
    s, _ = P10.plate('map_peru.png'); c.set_source_surface(s, 0, 0); c.paint()
    return JM.MAP['peru']


def map_canary(c, t):
    s, _ = P10.plate('map_canary.png'); c.set_source_surface(s, 0, 0); c.paint()
    return JM.MAP['canary']


def route(c, xy, prog, col=YEL, lw=5, a=1.0, dash=True):
    L = [0]
    for p_, q_ in zip(xy, xy[1:]): L.append(L[-1] + math.hypot(q_[0] - p_[0], q_[1] - p_[1]))
    d = L[-1] * max(0, min(1, prog)); hx, hy = xy[0]
    c.new_path(); c.move_to(*xy[0])
    for i in range(1, len(xy)):
        if L[i] <= d: c.line_to(*xy[i]); hx, hy = xy[i]
        else:
            f = (d - L[i - 1]) / max(1e-6, L[i] - L[i - 1]); hx, hy = xy[i - 1][0] + (xy[i][0] - xy[i - 1][0]) * f, xy[i - 1][1] + (xy[i][1] - xy[i - 1][1]) * f
            c.line_to(hx, hy); break
    c.set_source_rgba(*col, 0.95 * a); c.set_line_width(lw)
    if dash: c.set_dash([14, 9])
    c.stroke(); c.set_dash([])
    return hx, hy


def curve_pts(p0, p1, bend=0.25, n=40):
    (x0, y0), (x1, y1) = p0, p1
    mx, my = (x0 + x1) / 2 - (y1 - y0) * bend, (y0 + y1) / 2 + (x1 - x0) * bend
    return [((1 - u) ** 2 * x0 + 2 * (1 - u) * u * mx + u * u * x1, (1 - u) ** 2 * y0 + 2 * (1 - u) * u * my + u * u * y1) for u in (i / n for i in range(n + 1))]


# =============================================================== scènes Juliane
def sc_jk_hook(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        t0 = sg['sent'][0][0]; fl = flash_at(t, [t0 + 0.25, t0 + 1.05])
        storm_sky(c, t, fl)
        q = ap(t, t0 + 0.9, sg['sent'][0][1] + 0.1)
        pcs = dict(nose=(80 * q, 30 * q * q, 0.25 * q), mid=(0, 60 * q * q, -0.1 * q), tail=(-90 * q, 50 * q * q, -0.35 * q)) if q > 0 else None
        electra(c, 560, 820 + 10 * math.sin(t * 1.3), 26, -0.04, 1.0, fl, t, pieces=pcs)
        if q > 0: flame(c, 560 + 3 * 26, 850, -0.9, -0.3, 200, 30, t, inten=q, seed=4, smoke=0.6)
        bolt(c, 760, -20, 640, 830, fl, seed=int(t0 * 10) % 7 + 1)
    elif k == 1:
        q = ap(t, sg['sent'][1][0], sg['sent'][1][1] + 0.2)
        zs = 0.55 * (1 + 3.2 * q ** 1.7)                                          # la canopée se rapproche
        plate_fit(c, 'jg_top', None, zoom=zs * 0.82, pan=0, dy=0)
        for j in range(6):                                                       # nuages traversés (remontent)
            ph = (t * 0.7 + j / 6) % 1
            glow(c, (j * 233) % W, H + 300 - ph * (H + 700), 380, (0.85, 0.88, 0.92), 0.55 * (1 - q * 0.7))
        for j in range(26):                                                      # traits de vent
            r = random.Random(j); ph = (t * 2.2 + r.random()) % 1; x = r.uniform(80, 1000)
            c.move_to(x, H - ph * (H + 300)); c.line_to(x, H - ph * (H + 300) + 160); c.set_source_rgba(1, 1, 1, 0.25 * (1 - ph)); c.set_line_width(2); c.stroke()
        seat_top(c, 540, 820, 1.25, t * 0.9, 1.0)
        alt = int(3000 * (1 - q) / 50) * 50
        panel(c, 300, 1110, 480, 180, 0.6)
        counter(c, f"{alt:,} M".replace(',', ' '), "ATTACHÉE À SON SIÈGE", 540, 1210, YEL, 110)
    else:
        plate_fit(c, 'jg_floor', None, zoom=1.06, pan=-30 * p)
        rays(c, t, 520, 1.0)
        c.set_source_rgba(0, 0, 0, 0.35); c.paint()
        seat_side(c, 560, 1180, 1.6, 1.0, 0.25)
        stamp(c, "SURVIVRAIS-TU ?", 540, 700, 130, RED, since, glow=1.0)


def sc_jk_real(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        plate_fit(c, 'jg_air', 'dusk', zoom=1.05 + 0.03 * p, pan=-40 * p, sky='dusk')
        c.set_source_rgba(0, 0, 0, 0.45); c.paint()
        letter(c, "L'HISTOIRE VRAIE DE", 540, 600, 52, WH, ap(since, 0.0, 0.3), 'Montserrat')
        letter(c, "JULIANE KOEPCKE", 540, 740, 120, (1, 1, 1), ap(since, 0.2, 0.55))
        c.move_to(250, 790); c.line_to(250 + 580 * eout(ap(since, 0.4, 1.0)), 790); c.set_source_rgba(*YEL, 0.9); c.set_line_width(4); c.stroke()
        stamp(c, "17 ANS", 540, 930, 110, YEL, since - 1.2, glow=0.8)
    elif k == 1:
        M = map_peru(c, t)
        lima, puc = M(-77.04, -12.05), M(-74.55, -8.38)
        xy = curve_pts(lima, puc, -0.12)
        hx, hy = route(c, xy, ap(p, 0.1, 0.85))
        if p > 0.1: plane_icon(c, hx, hy, math.atan2(puc[1] - lima[1], puc[0] - lima[0]), 1.5, (1, 1, 1), 1.0)
        for nm, (x, y), dx in (("LIMA", lima, -20), ("PUCALLPA", puc, 20)):
            c.new_path(); c.arc(x, y, 10, 0, 7); c.set_source_rgb(1, 1, 1); c.fill()
            letter(c, nm, x + dx, y - 20, 40, WH, 1.0, anchor='r' if dx < 0 else 'l')
        letter(c, "PÉROU", *M(-77.5, -8.2), 52, (0.6, 0.72, 0.85), 0.8)
        letter(c, "AMAZONIE", *M(-73.2, -10.5), 50, (0.55, 0.9, 0.6), 0.9)
        letter(c, "ANDES", *M(-76.6, -11.2), 40, (1.0, 0.9, 0.75), 0.8)
        panel(c, 220, 380, 640, 150, 0.55)
        letter(c, "24 DÉCEMBRE 1971", 540, 485, 92, YEL, ap(p, 0.0, 0.12))
        tag(c, "AVEC SA MÈRE", 540, 1285, WH, ap(p, 0.45, 0.6), 54)
    else:
        sky_paint(c, 'dusk', t)
        plate_fit(c, 'jg_air', 'dusk', zoom=1.0, dy=420, alpha=1.0)
        electra(c, 420 + 160 * p, 720 - 20 * p, 20, -0.03, 1.0, 0.0, t, night=False)
        panel(c, 290, 1060, 500, 170, 0.6)
        counter(c, "92 À BORD", "LOCKHEED ELECTRA · VOL LANSA 508", 540, 1150, YEL, 96, ap(since, 0.0, 0.25))


def sky_under(c, mode, t):
    """le ciel des plaques à ciel transparent est peint DESSOUS : on repeint là où la plaque est vide (dest-over)."""
    c.save(); c.set_operator(cairo.OPERATOR_DEST_OVER); sky_paint(c, mode, t); c.restore()


def sc_jk_storm(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        t0 = sg['sent'][0][0]; fl = flash_at(t, [t0 + 0.4, t0 + 1.2])
        storm_sky(c, t, fl)
        ex, ey = 540 + 40 * math.sin(t * 0.6), 860 + 14 * math.sin(t * 1.7)
        electra(c, ex, ey, 30, 0.04 * math.sin(t * 1.2), 1.0, fl, t)
        if fl > 0.2: bolt(c, 200, -20, 120, 1100, fl, seed=3)
        tag(c, "UN VIOLENT ORAGE", 540, 1285, WH, ap(p, 0.2, 0.35), 54)
    else:
        b = sg['sent'][1]; L = b[1] - b[0]
        t_hit, t_fire, t_brk = b[0] + 0.05, b[0] + 0.30 * L, b[0] + 0.62 * L
        fl = flash_at(t, [t_hit, t_hit + 0.5])
        storm_sky(c, t, fl * 0.9)
        s = 30; ex, ey = 540, 860
        wing_x, wing_y = ex + 0.8 * s, ey + 1.6 * s                                   # aile droite (côté caméra)
        q = ap(t, t_brk, b[1] + 0.3)
        pcs = dict(nose=(160 * q, 90 * q * q, 0.45 * q), mid=(20 * q, 160 * q * q, -0.25 * q), tail=(-170 * q, 120 * q * q, -0.6 * q)) if q > 0 else None
        electra(c, ex, ey, s, 0.0, 1.0, fl, t, pieces=pcs)
        bolt(c, 760, -20, wing_x, wing_y, fl, seed=5, w=6)
        fi = ap(t, t_fire, t_fire + 0.4)
        if fi > 0:
            fx, fy = wing_x + 20 * q, wing_y + 140 * q * q
            flame(c, fx, fy, -0.95, -0.25, 260 + 200 * q, 36, t, inten=fi, seed=7, smoke=0.8)
        if q > 0:
            r = random.Random(9)
            for j in range(40):                                                  # débris
                ang = r.uniform(0, 6.28); sp = r.uniform(80, 420)
                x = ex + math.cos(ang) * sp * q; y = ey + math.sin(ang) * sp * q + 300 * q * q
                c.save(); c.translate(x, y); c.rotate(t * r.uniform(-6, 6)); c.rectangle(-6, -3, r.uniform(6, 16), r.uniform(3, 8))
                c.set_source_rgba(0.5 + 0.5 * fl, 0.5 + 0.5 * fl, 0.55 + 0.45 * fl, 0.8); c.fill(); c.restore()
        if t < t_fire: tag(c, "LA FOUDRE FRAPPE L'AILE DROITE", 540, 1285, YEL, ap(t, t_hit, t_hit + 0.2), 50)
        elif t < t_brk: tag(c, "INCENDIE", 540, 1285, ORG, 1.0, 58)
        else: stamp(c, "L'AVION SE BRISE", 540, 1285, 96, RED, t - t_brk, glow=1.0)


def sc_jk_fall(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        b = sg['sent'][0]; q = ap(t, b[0] - 0.1, b[1] + 0.25)
        zs = 0.42 * (1 + 7.0 * q ** 2.2)
        plate_fit(c, 'jg_top', None, zoom=zs, cx=0.52, cy=0.48)
        c.set_source_rgba(0.80, 0.84, 0.88, 0.55 * (1 - q) ** 2); c.paint()                # brume d'altitude qui se dissipe
        for j in range(8):
            ph = (t * 0.9 + j / 8) % 1
            glow(c, (j * 197 + 90) % W, H + 300 - ph * (H + 700), 340, (0.88, 0.9, 0.94), 0.5 * (1 - q) ** 1.5)
        for j in range(30):
            r = random.Random(j + 40); ph = (t * 2.6 + r.random()) % 1; x = r.uniform(80, 1000)
            c.move_to(x, H - ph * (H + 300)); c.line_to(x, H - ph * (H + 300) + 200); c.set_source_rgba(1, 1, 1, 0.22 * (1 - ph)); c.set_line_width(2); c.stroke()
        seat_top(c, 540, 800, 1.35, t * 0.7 + 0.6, 1.0)
        # échelle d'altitude (règle qui défile)
        alt = 3000 * (1 - q)
        c.rectangle(930, 330, 4, 900); c.set_source_rgba(1, 1, 1, 0.5); c.fill()
        for m in range(0, 3001, 250):
            y = 780 - (m - alt) * 0.9
            if 330 <= y <= 1230:
                c.rectangle(900 if m % 1000 == 0 else 914, y - 1.5, 34 if m % 1000 == 0 else 20, 3); c.set_source_rgba(1, 1, 1, 0.8); c.fill()
                if m % 500 == 0: letter(c, f"{m}", 885, y + 12, 34, WH, 0.85, anchor='r')
        c.move_to(940, 780); c.line_to(965, 765); c.line_to(965, 795); c.close_path(); c.set_source_rgba(*YEL, 1); c.fill()
        panel(c, 300, 1110, 480, 180, 0.6)
        counter(c, f"{int(alt / 50) * 50:,} M".replace(',', ' '), "DE CHUTE LIBRE", 540, 1210, YEL, 110)
    else:
        plate_fit(c, 'jg_floor', None, zoom=1.08 - 0.03 * p, pan=20 * p)
        rays(c, t, 560, 1.4)
        motes(c, t, 0.8)
        seat_side(c, 520, 1200, 1.7, 1.0, 0.2)
        glow(c, 470, 1090, 120, (1, 0.95, 0.8), 0.25)
        # électrocardiogramme : le cœur bat
        x0, y0 = 120, 560; c.new_path(); c.move_to(x0, y0)
        for i in range(0, 841, 4):
            ph = ((i / 840) * 3 - t * 1.2) % 1
            v = -120 * math.exp(-((ph - 0.5) / 0.02) ** 2) + 40 * math.exp(-((ph - 0.53) / 0.02) ** 2) - 18 * math.exp(-((ph - 0.7) / 0.05) ** 2)
            c.line_to(x0 + i, y0 + v * ap(since, 0.0, 0.3))
        c.set_source_rgba(*GRN, 0.9); c.set_line_width(5); c.stroke()
        stamp(c, "VIVANTE", 540, 820, 150, GRN, since - 0.3, glow=1.0)


def sc_jk_hurt(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        plate_fit(c, 'jg_floor', None, zoom=1.1)
        c.set_source_rgba(0.0, 0.03, 0.05, 0.72); c.paint()
        for x in range(0, W, 60):
            c.rectangle(x, 0, 1, H); c.set_source_rgba(*CY, 0.06); c.fill()
        for y in range(0, H, 60):
            c.rectangle(0, y, W, 1); c.set_source_rgba(*CY, 0.06); c.fill()
        person_front(c, 540, 760, 1.15, 0.9)
        b = sg['sent'][0]; L = b[1] - b[0]
        marks = [("CLAVICULE CASSÉE", (540 + 69, 760 - 259), (790, 330)), ("GENOU BLESSÉ", (540 + 55, 760 + 299), (790, 1180)),
                 ("COUPURE AU BRAS", (540 - 150, 760 - 110), (275, 900))]
        for j, (nm, (mx, my), (lx, ly)) in enumerate(marks):
            a = ap(t, b[0] + j * L * 0.3, b[0] + j * L * 0.3 + 0.25)
            if a <= 0: continue
            ph = (t * 1.4) % 1
            c.new_path(); c.arc(mx, my, 18 + 30 * ph, 0, 7); c.set_source_rgba(*RED, a * (1 - ph)); c.set_line_width(4); c.stroke()
            glow(c, mx, my, 40, RED, 0.8 * a)
            c.move_to(mx, my); c.line_to(lx, ly + 20); c.set_source_rgba(1, 1, 1, 0.6 * a); c.set_line_width(2.5); c.stroke()
            tag(c, nm, lx, ly, RED, a, 40)
    else:
        plate_fit(c, 'jg_air', 'day', zoom=1.25, cx=0.55, cy=0.62, sky='day')
        x, y = 600, 1080
        for j in range(4):
            ph = (t * 0.35 + j / 4) % 1
            c.save(); c.translate(x, y); c.scale(1, 0.42); c.new_path(); c.arc(0, 0, 40 + ph * 820, 0, 7); c.restore()
            c.set_source_rgba(1, 1, 1, 0.5 * (1 - ph)); c.set_line_width(3); c.stroke()
        glow(c, x, y, 40, YEL, 0.9); c.new_path(); c.arc(x, y, 8, 0, 7); c.set_source_rgb(1, 1, 1); c.fill()
        label(c, "ELLE", x, y - 40, 40, WH, ap(p, 0.0, 0.2), 'Bebas Neue')
        stamp(c, "PERSONNE", 540, 560, 150, WH, since - 0.15, glow=1.0)


def sc_jk_river(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        plate_fit(c, 'jg_floor', None, zoom=1.04, pan=-40 + 50 * p)
        rays(c, t, 600, 1.2, seed=8)
        motes(c, t, 0.7, seed=9)
        walker(c, 560 + 60 * p, 1240, 2.6, t, 1.0, col=(0.02, 0.04, 0.02))
        letter(c, "FILLE DE", 540, 470, 56, WH, ap(since, 0.0, 0.25), 'Montserrat')
        letter(c, "ZOOLOGISTES", 540, 600, 130, YEL, ap(since, 0.15, 0.45))
        tag(c, "ELLE CONNAÎT LA FORÊT", 540, 1285, GRN, ap(p, 0.45, 0.6), 50)
    else:
        b = sg['sent'][1]; tm = b[0] + 0.42 * (b[1] - b[0])
        if t < tm:                                                               # vue de dessus : le ruisseau
            q = ap(t, b[0], tm)
            x0, y0, sc = plate_fit(c, 'jg_top', None, zoom=1.15, cy=0.55 - 0.08 * q)
            S_ = 2400
            pts = [(S_ * 0.5 + 300 * math.sin(j / 420.0) + 120 * math.sin(j / 150.0 + 2), j - 20) for j in range(0, S_ + 41, 20)]
            xy = [(x0 + px * sc, y0 + py * sc) for px, py in pts if 0 < y0 + py * sc < H]
            xy = xy[::-1]
            if len(xy) > 2:
                hx, hy = route(c, xy, 0.15 + 0.7 * q, YEL, 7)
                glow(c, hx, hy, 40, YEL, 0.8); c.new_path(); c.arc(hx, hy, 9, 0, 7); c.set_source_rgb(1, 1, 1); c.fill()
            tag(c, "UN RUISSEAU", 540, 1285, WH, ap(q, 0.1, 0.3), 54)
        else:
            q = ap(t, tm, b[1] + 0.3)
            plate_fit(c, 'jg_river', None, zoom=1.04 + 0.04 * q, pan=-20 + 40 * q, sky='day')
            x, y = 560, 1170; yw = y - 8                                            # dans l'eau jusqu'aux genoux : silhouette coupée à la surface
            c.save(); c.rectangle(0, 0, W, yw); c.clip(); walker(c, x, y, 2.3, t, 1.0, col=(0.03, 0.05, 0.03)); c.restore()
            c.save(); c.rectangle(0, yw, W, 140); c.clip(); c.translate(0, 2 * yw); c.scale(1, -1)
            c.push_group(); walker(c, x, y, 2.3, t, 1.0, col=(0.03, 0.05, 0.03)); c.pop_group_to_source(); c.paint_with_alpha(0.25); c.restore()
            ripples(c, x, yw + 2, t, 1.0)
            tag(c, "PUIS UNE RIVIÈRE", 540, 1285, WH, ap(q, 0.05, 0.25), 54)
            letter(c, "EN MARCHANT DANS L'EAU", 540, 470, 60, WH, ap(q, 0.3, 0.5), 'Montserrat')


def sc_jk_found(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        plate_fit(c, 'jg_river', 'dusk', zoom=1.08, pan=40 - 40 * p, sky='dusk')
        hut(c, 905, 975, 0.9, 1.0, light=0.9)
        pirogue(c, 780, 1040, 0.8, 1.0, people=0, col=(0.20, 0.14, 0.09))
        panel(c, 330, 380, 420, 170, 0.55)
        counter(c, "JOUR 9", "SEULE DANS LA JUNGLE", 540, 485, YEL, 110)
        tag(c, "UN CAMPEMENT DE BÛCHERONS", 540, 1285, ORG, ap(p, 0.3, 0.45), 48)
    else:
        b = sg['sent'][1]; L = b[1] - b[0]; t1, t2 = b[0] + 0.30 * L, b[0] + 0.62 * L
        if t < t2:
            plate_fit(c, 'jg_river', 'dusk', zoom=1.12, sky='dusk')
            hut(c, 905, 975, 0.9, 1.0, light=1.0)
            for j in range(3):
                a = ap(t, b[0] + j * 0.25, b[0] + j * 0.25 + 0.3)
                walker(c, 560 + j * 70, 1010, 1.6, 0.0, a, ph=j, col=(0.06, 0.05, 0.05))
            panel(c, 330, 380, 420, 170, 0.55)
            counter(c, "JOUR 11", "ON LA RETROUVE", 540, 485, GRN, 110)
            if t > t1:
                a = ap(t, t1, t1 + 0.25)
                panel(c, 190, 1120, 700, 190, 0.7 * a)
                cx_, cy_ = 300, 1215                                              # bidon d'essence
                rr(c, cx_ - 40, cy_ - 52, 80, 104, 10); c.set_source_rgba(*RED, a); c.fill()
                rr(c, cx_ + 10, cy_ - 72, 24, 22, 4); c.fill()
                letter(c, "ESSENCE SUR LA PLAIE", 580, cy_ - 8, 50, WH, a)
                letter(c, "INFESTÉE DE LARVES", 580, cy_ + 46, 40, (1, 0.8, 0.6), a, 'Montserrat')
        else:
            q = ap(t, t2, b[1] + 0.4)
            plate_fit(c, 'jg_river', 'day', zoom=1.05 + 0.04 * q, sky='day')
            pirogue(c, 540, 1060 - 80 * q, 1.1 - 0.4 * q, 1.0, people=3, t=t)
            ripples(c, 540, 1062 - 80 * q, t, 0.8, 3, 240 * (1.1 - 0.4 * q))
            tag(c, "EN PIROGUE, VERS LES SECOURS", 540, 1285, GRN, ap(q, 0.05, 0.25), 48)


def sc_jk_later(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    plate_fit(c, 'jg_air', 'dusk', zoom=1.08 + 0.10 * p, cx=0.5, cy=0.55, sky='dusk')
    x, y = 640, 1010
    a = ap(p, 0.35, 0.5)
    glow(c, x, y, 70, YEL, 0.7 * a)
    c.new_path(); c.arc(x, y - 60, 26, math.pi * 0.85, math.pi * 2.15); c.line_to(x, y); c.close_path(); c.set_source_rgba(*YEL, a); c.fill()
    c.new_path(); c.arc(x, y - 60, 10, 0, 7); c.set_source_rgba(0.1, 0.1, 0.1, a); c.fill()
    label(c, "PANGUANA", x, y - 110, 54, WH, a, 'Bebas Neue')
    letter(c, "STATION DE RECHERCHE", x, y + 60, 36, WH, a, 'Montserrat')
    panel(c, 230, 380, 620, 180, 0.55)
    letter(c, "BIOLOGISTE", 540, 495, 120, GRN, ap(p, 0.0, 0.15))
    tag(c, "FONDÉE PAR SES PARENTS", 540, 1285, YEL, ap(p, 0.6, 0.75), 50)


def sc_jk_verdict(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k <= 1:
        c.set_source_rgb(0.01, 0.015, 0.025); c.paint()
        plate_fit(c, 'jg_floor', None, zoom=1.1, alpha=0.18)
        t1 = sg['sent'][1][0]
        for j in range(92):                                                       # 92 à bord : 1 survivante, 91 lumières
            row, col = j // 8, j % 8
            x = 205 + col * 96; y = 380 + row * 70
            if j == 41:
                a = ap(t, sg['sent'][0][0], sg['sent'][0][0] + 0.4)
                glow(c, x, y, 44, GRN, 0.8 * a); c.new_path(); c.arc(x, y, 12, 0, 7); c.set_source_rgba(*GRN, 0.3 + 0.7 * a); c.fill()
                continue
            if k == 0:
                c.new_path(); c.arc(x, y, 9, 0, 7); c.set_source_rgba(1, 1, 1, 0.25); c.fill()
            else:
                a = ap(t, t1 + j * 0.012, t1 + j * 0.012 + 0.35); fl = 0.85 + 0.15 * math.sin(t * 7 + j)
                glow(c, x, y, 28, (1.0, 0.75, 0.4), 0.5 * a * fl)
                c.new_path(); c.arc(x, y, 6, 0, 7); c.set_source_rgba(1, 0.95, 0.8, 0.25 + 0.75 * a); c.fill()
        if k == 0:
            stamp(c, "SEULE SURVIVANTE", 540, 1270, 110, GRN, since, glow=1.0)
        else:
            letter(c, "91 VICTIMES", 540, 1210, 110, WH, ap(p, 0.0, 0.2))
            letter(c, "DONT SA MÈRE", 540, 1280, 50, (1.0, 0.85, 0.6), ap(p, 0.35, 0.55), 'Montserrat')
    else:
        plate_fit(c, 'jg_air', 'dusk', zoom=1.12, sky='dusk')
        stamp(c, "ET TOI ?", 540, 620, 170, ORG, since, glow=1.0)
        letter(c, "TU AURAIS TENU 11 JOURS ?", 540, 740, 58, WH, ap(since, 0.3, 0.6), 'Montserrat')


# =============================================================== TÉNÉRIFE
FOG = (0.60, 0.63, 0.66)
WORLD_W = {'klm_rear': 62.0, 'klm_hero': 66.0, 'pa_front': 68.0, 'pa_side': 74.0, 'klm_rot': 76.0}


def fog_runway(c, t, dens=1.0, speed=0.0, lights=1.0, dark=0.0):
    """piste vue dans l'axe (caméra à 6 m) noyée dans le brouillard ; balisage axial qui défile (speed en m/s)."""
    P10.runway_axis(c, t, 0, 0, True)
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgba(0, *FOG, 0.97 * dens); g.add_color_stop_rgba(0.47, *FOG, 0.97 * dens); g.add_color_stop_rgba(0.62, *FOG, 0.78 * dens); g.add_color_stop_rgba(1, *FOG, 0.30 * dens)
    c.set_source(g); c.paint()
    g = cairo.RadialGradient(540, 900, 300, 540, 900, 1300); g.add_color_stop_rgba(0, 0.02, 0.03, 0.05, 0); g.add_color_stop_rgba(1, 0.02, 0.03, 0.05, 0.45)
    c.set_source(g); c.paint()
    if dark > 0: c.set_source_rgba(0.05, 0.06, 0.08, dark); c.paint()
    if lights > 0:
        off = (t * speed) % 15.0
        for i in range(40):
            Z = 8 + i * 15 - off
            if Z < 14: continue
            k = 900.0 / Z; y = 900 + 6 * k; vis = math.exp(-Z / (85 / max(0.3, dens)))
            if vis < 0.02: continue
            for xo, col, sz in ((0, (1, 1, 1), 0.35), (-29.4, (1, 0.92, 0.7), 0.4), (29.4, (1, 0.92, 0.7), 0.4)):
                if xo != 0 and i % 2: continue
                x = 540 + xo * k
                glow(c, x, y, min(46, max(3, sz * 3.2 * k)), col, 0.55 * vis * lights)
                c.new_path(); c.arc(x, y, max(1.2, sz * 0.5 * k), 0, 7); c.set_source_rgba(*col, vis * lights); c.fill()


def fog_plane(c, name, Z, t, x=540, dens=1.0, xray=0.0, alpha=1.0, ground=True, lift=0.0, yoff=0.0):
    """747 posé sur la piste à Z mètres (caméra à 6 m), voilé par le brouillard ; xray > 0 : silhouette « radiographie » à travers."""
    s, b, pts, (w, h) = P10.spr(name, 0.4)
    im, _ = P10._load(name)
    k = 900.0 / Z; scale = WORLD_W[name] * k / im.width
    yg = 900 + 6 * k - lift * k + yoff
    cx = pts.get('center', (w / 2, h / 2))[0] / b
    x0 = x - cx * scale; y0 = yg - (im.height - 4) * scale
    vis = math.exp(-max(0, Z - 30) / (95 / max(0.3, dens)))
    if alpha > 0:                                                                 # ombre de contact sous le train
        c.save(); c.translate(x, yg - 2); c.scale(1, 0.08)
        g = cairo.RadialGradient(0, 0, 0, 0, 0, im.width * scale * 0.42); g.add_color_stop_rgba(0, 0.05, 0.06, 0.07, 0.75 * alpha * min(1, 0.3 + vis)); g.add_color_stop_rgba(1, 0.05, 0.06, 0.07, 0)
        c.new_path(); c.arc(0, 0, im.width * scale * 0.42, 0, 7); c.set_source(g); c.fill(); c.restore()
    if alpha * vis > 0.01:
        c.push_group()
        P = plane(c, name, x0 + im.width * scale / 2, y0 + im.height * scale / 2, scale)
        c.set_operator(cairo.OPERATOR_ATOP); c.set_source_rgba(*FOG, 1.0); c.paint_with_alpha(min(1, (1 - vis) * 1.02))
        c.pop_group_to_source(); c.paint_with_alpha(alpha * min(1, 0.25 + vis * 1.5))
    if xray > 0:
        c.push_group(); plane(c, name, x0 + im.width * scale / 2, y0 + im.height * scale / 2, scale, xray=True); c.pop_group_to_source(); c.paint_with_alpha(xray)
    return x0, y0, scale, (im.width * scale, im.height * scale)


def fog_drift(c, t, a=1.0, seed=3, y0=700, y1=1400):
    r = random.Random(seed)
    for j in range(18):
        x = (r.uniform(0, W + 600) - t * r.uniform(20, 60)) % (W + 600) - 300; y = r.uniform(y0, y1)
        c.save(); c.translate(x, y); c.scale(1, 0.3)
        g = cairo.RadialGradient(0, 0, 0, 0, 0, 420); g.add_color_stop_rgba(0, *FOG, 0.35 * a); g.add_color_stop_rgba(1, *FOG, 0)
        c.new_path(); c.arc(0, 0, 420, 0, 7); c.set_source(g); c.fill(); c.restore()


def b747_top(c, x, y, s, rot=0.0, col=CY, a=1.0, fill=None, lw=3.0, front=None):
    """Boeing 747 vu de dessus (mètres, nez vers le haut). front = (couleur, alpha) : surligne l'avant (jusqu'au bord d'attaque de l'aile)."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    def outline():
        c.new_path()
        c.move_to(0, -35.5); c.curve_to(2.6, -35.2, 3.25, -32, 3.25, -28); c.line_to(3.25, -4)
        c.line_to(29.8, 14.0); c.line_to(29.8, 17.0); c.line_to(12.5, 11.5); c.line_to(3.25, 9.5)
        c.line_to(3.0, 25.0); c.line_to(11.0, 31.5); c.line_to(11.0, 34.0); c.line_to(2.0, 33.5); c.line_to(0.6, 36.0)
        c.line_to(-0.6, 36.0); c.line_to(-2.0, 33.5); c.line_to(-11.0, 34.0); c.line_to(-11.0, 31.5); c.line_to(-3.0, 25.0)
        c.line_to(-3.25, 9.5); c.line_to(-12.5, 11.5); c.line_to(-29.8, 17.0); c.line_to(-29.8, 14.0); c.line_to(-3.25, -4)
        c.line_to(-3.25, -28); c.curve_to(-3.25, -32, -2.6, -35.2, 0, -35.5); c.close_path()
    if fill: outline(); c.set_source_rgba(*fill, a); c.fill()
    if front:
        c.save(); c.rectangle(-40, -40, 80, 36); c.clip(); outline(); c.set_source_rgba(*front[0], front[1]); c.fill(); c.restore()
    outline()
    c.set_source_rgba(*col, a); c.set_line_width(lw / s); c.set_line_join(1); c.stroke()
    for ex, ey in ((11.8, 2.5), (21.0, 9.6)):
        for sg in (-1, 1):
            rr(c, sg * ex - 1.3, ey - 4.5, 2.6, 6.0, 1.0); c.set_source_rgba(*col, a); c.set_line_width(lw * 0.8 / s); c.stroke()
    c.save(); c.translate(0, -24); c.scale(1, 4.2); c.new_path(); c.arc(0, 0, 2.3, 0, 7); c.restore(); c.set_source_rgba(*col, 0.45 * a); c.set_line_width(lw * 0.6 / s); c.stroke()
    c.restore()


# plan de Los Rodeos (schéma) : piste verticale, extrémité NO (parking) en haut, seuil 30 en bas
RWY = (470, 330, 470, 1380)                     # x, y_haut, x, y_bas
TWY_X = 690
EXITS = {'C1': 450, 'C2': 660, 'C3': 870, 'C4': 1080}


def airport_xray(c, t, a=1.0):
    c.set_source_rgb(0.01, 0.025, 0.05); c.paint()
    for x in range(0, W, 54):
        c.rectangle(x, 0, 1, H); c.set_source_rgba(*CY, 0.05 * a); c.fill()
    for y in range(0, H, 54):
        c.rectangle(0, y, W, 1); c.set_source_rgba(*CY, 0.05 * a); c.fill()
    x, y0, _, y1 = RWY
    rr(c, x - 34, y0, 68, y1 - y0, 6); c.set_source_rgba(*CY, 0.10 * a); c.fill_preserve(); c.set_source_rgba(*CY, 0.9 * a); c.set_line_width(3); c.stroke()
    c.set_dash([18, 16]); c.move_to(x, y0 + 30); c.line_to(x, y1 - 30); c.set_source_rgba(*CY, 0.5 * a); c.set_line_width(2); c.stroke(); c.set_dash([])
    c.move_to(TWY_X, 340); c.line_to(TWY_X, 1150); c.set_source_rgba(*CY, 0.55 * a); c.set_line_width(16); c.stroke()
    for nm, yy in EXITS.items():
        c.move_to(x + 34, yy); c.line_to(TWY_X, yy - 60); c.set_source_rgba(*CY, 0.55 * a); c.set_line_width(14); c.stroke()
        letter(c, nm, TWY_X + 30, yy - 50, 34, CY, 0.9 * a, anchor='l')
    rr(c, 560, 200, 380, 110, 10); c.set_source_rgba(*CY, 0.08 * a); c.fill_preserve(); c.set_source_rgba(*CY, 0.7 * a); c.set_line_width(2); c.stroke()
    letter(c, "PARKING", 545, 272, 36, CY, 0.9 * a, anchor='r')
    letter(c, "PISTE", x - 70, y0 + 60, 34, CY, 0.9 * a, anchor='r')


def sc_tf_hook(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    q = (t - sg['sent'][0][0]) / 7.0
    fog_runway(c, t, 1.0)
    fog_plane(c, 'pa_side', 420, t, x=850, xray=(ap(t, sg['sent'][1][0], sg['sent'][1][0] + 0.3) if k >= 1 else 0) * 0.9)
    fog_plane(c, 'klm_hero', 92 - 10 * q, t, x=330)
    fog_drift(c, t, 1.0)
    if k == 0:
        tag(c, "KLM", 300, 1285, (0.45, 0.75, 1.0), ap(p, 0.15, 0.3), 56)
        tag(c, "PAN AM", 850, 1285, WH, ap(p, 0.35, 0.5), 56)
    elif k == 1:
        x0, y0, sc, (w, h) = fog_plane(c, 'pa_side', 420, t, x=850, alpha=0.0)
        label(c, "PAN AM", 850, y0 - 20, 46, CY, ap(p, 0.0, 0.3), 'Bebas Neue')
        stamp(c, "AUCUN NE VOIT L'AUTRE", 540, 1285, 84, WH, since, glow=0.8)
    else:
        c.set_source_rgba(0, 0, 0, 0.25); c.paint()
        stamp(c, "LE PIRE CRASH", 540, 540, 150, YEL, since, glow=1.0)
        letter(c, "DE L'HISTOIRE DE L'AVIATION", 540, 650, 54, WH, ap(since, 0.3, 0.6), 'Montserrat')


def sc_tf_bomb(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    M = map_canary(c, t)
    lpa, tfn = M(-15.386, 27.932), M(-16.341, 28.483)
    letter(c, "GRAN CANARIA", lpa[0] + 10, lpa[1] + 130, 44, (0.6, 0.72, 0.85), 0.9)
    letter(c, "TENERIFE", tfn[0] - 100, tfn[1] - 150, 50, (0.6, 0.72, 0.85), 0.9)
    letter(c, "OCÉAN ATLANTIQUE", 330, 1200, 36, (0.45, 0.6, 0.8), 0.6, 'Montserrat')
    if k == 0:
        panel(c, 250, 380, 580, 150, 0.55)
        letter(c, "27 MARS 1977", 540, 485, 100, YEL, ap(p, 0.0, 0.12))
        te = sg['sent'][0][0] + 0.45 * (sg['sent'][0][1] - sg['sent'][0][0])
        if t > te:
            d = t - te
            for j in range(3):
                ph = ((d * 0.9) + j / 3) % 1
                c.new_path(); c.arc(*lpa, 16 + 150 * ph, 0, 7); c.set_source_rgba(*ORG, (1 - ph) * 0.9); c.set_line_width(5); c.stroke()
            glow(c, *lpa, 90, ORG, 0.9 * math.exp(-d * 1.5) + 0.3); glow(c, *lpa, 30, (1, 1, 0.8), 0.9)
            tag(c, "UNE BOMBE À L'AÉROPORT", 540, 1285, ORG, ap(d, 0.0, 0.25), 52)
        c.new_path(); c.arc(*lpa, 9, 0, 7); c.set_source_rgb(1, 1, 1); c.fill()
    else:
        glow(c, *lpa, 50, ORG, 0.5); c.new_path(); c.arc(*lpa, 9, 0, 7); c.set_source_rgba(*ORG, 1); c.fill()
        cross(c, lpa[0], lpa[1], 0.8, RED, ap(p, 0.0, 0.15))
        for j in range(5):                                                       # déroutements : ils arrivent du nord vers Gran Canaria puis virent
            a0 = ap(p, 0.05 + j * 0.1, 0.55 + j * 0.08)
            st = (lpa[0] + 60 + j * 70 - 200, -40)
            mid = (lpa[0] + (j - 2) * 40, lpa[1] - 260)
            pts = curve_pts(st, mid, 0.05, 20) + curve_pts(mid, tfn, -0.25, 30)[1:]
            hx, hy = route(c, pts, a0, WH, 3, 0.8)
            if 0 < a0 < 1:
                i = max(1, int(len(pts) * a0) - 1); ang = math.atan2(pts[i][1] - pts[i - 1][1], pts[i][0] - pts[i - 1][0])
                plane_icon(c, hx, hy, ang, 1.2, (1, 1, 1), 1.0)
        glow(c, *tfn, 50, YEL, 0.8); c.new_path(); c.arc(*tfn, 10, 0, 7); c.set_source_rgb(*YEL); c.fill()
        tag(c, "DÉROUTÉS VERS LOS RODEOS", 540, 1285, YEL, ap(p, 0.35, 0.5), 50)
        label(c, "PETIT AÉROPORT SATURÉ", tfn[0] + 40, tfn[1] + 90, 36, WH, ap(p, 0.6, 0.75), 'Montserrat')


def sc_tf_fog(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        airport_xray(c, t)
        x = RWY[0]
        for j, (px, py) in enumerate(((620, 255), (700, 255), (780, 255), (860, 255), (TWY_X, 400), (TWY_X, 560))):  # parking et taxiway pleins
            b747_top(c, px, py, 0.9, math.pi / 2 if j < 4 else 0, CY, 0.7)
        q = ap(p, 0.1, 0.9)
        y = 360 + (1320 - 360) * q                                                # KLM remonte la piste
        b747_top(c, x, y, 1.6, math.pi, (0.45, 0.75, 1.0), 1.0, fill=(0.1, 0.3, 0.6), lw=3.5)
        c.set_dash([10, 8]); c.move_to(x - 80, 360); c.line_to(x - 80, y); c.set_source_rgba(*YEL, 0.9); c.set_line_width(5); c.stroke(); c.set_dash([])
        c.move_to(x - 80, y + 20); c.line_to(x - 96, y - 6); c.line_to(x - 64, y - 6); c.close_path(); c.set_source_rgba(*YEL, 1); c.fill()
        label(c, "KLM", x - 160, y + 10, 44, (0.45, 0.75, 1.0), 1.0, 'Bebas Neue')
        tag(c, "TAXIWAY BLOQUÉ : ON REMONTE LA PISTE", 540, 1640 - 350, YEL, ap(p, 0.3, 0.45), 40)
    elif k == 1:
        fog_runway(c, t, 0.9)
        fog_plane(c, 'klm_hero', 62 - 8 * p, t, x=600)
        fog_drift(c, t, 0.9)
        tag(c, "KLM 4805 · 248 À BORD", 540, 1285, (0.45, 0.75, 1.0), ap(p, 0.15, 0.3), 52)
        letter(c, "EN BOUT DE PISTE", 540, 470, 70, WH, ap(p, 0.0, 0.2))
    else:
        fog_runway(c, t, 1.0)
        Z = 150 - 60 * p
        fog_plane(c, 'pa_front', Z, t, x=520)
        fog_drift(c, t, 1.1)
        tag(c, "PAN AM 1736 · 396 À BORD", 540, 1285, WH, ap(p, 0.1, 0.25), 52)
        panel(c, 300, 380, 480, 170, 0.6)
        counter(c, "< 100 M", "DE VISIBILITÉ", 540, 480, YEL, 110, ap(p, 0.4, 0.55))


def wave(c, t, y, amp, f, col, a, x0=110, x1=970, noise=0.0, seed=0, phase=0.0, lw=4):
    r = random.Random(seed)
    c.new_path()
    for i in range(0, 241):
        x = x0 + (x1 - x0) * i / 240
        v = amp * math.sin(i * f + t * 9 + phase) * (0.6 + 0.4 * math.sin(i * 0.05 + t * 2)) + noise * amp * r.uniform(-1, 1)
        (c.move_to if i == 0 else c.line_to)(x, y + v)
    c.set_source_rgba(*col, a); c.set_line_width(lw); c.stroke()


def glitch_text(c, s, x, y, size, col, a, amount, t, seed=1):
    """texte qui se brouille : décalages RVB + lettres remplacées."""
    r = random.Random(int(t * 20) + seed)
    if amount > 0.02:
        chars = list(s)
        for i in range(len(chars)):
            if chars[i] != ' ' and r.random() < amount * 0.8: chars[i] = r.choice('#%&?!/*@$')
        s2 = ''.join(chars)
        c.save(); c.set_operator(cairo.OPERATOR_ADD)
        letter(c, s2, x - 12 * amount, y, size, (1, 0.1, 0.1), a * 0.8)
        letter(c, s2, x + 12 * amount, y + 3 * amount, size, (0.1, 0.5, 1), a * 0.8)
        c.restore()
        for j in range(int(6 * amount)):
            yy = y - size * r.random(); c.rectangle(x - 300, yy, 600, r.uniform(2, 8)); c.set_source_rgba(1, 1, 1, 0.3 * a); c.fill()
    else:
        letter(c, s, x, y, size, col, a)


def sc_tf_radio(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    fog_runway(c, t, 1.0, dark=0.35)
    tower(c, 880, 1330, 0.75, 1.0, (0.30, 0.32, 0.36))
    fog_drift(c, t, 0.8)
    panel(c, 90, 330, 900, 510, 0.7)
    if k == 0:
        letter(c, "KLM À LA TOUR", 540, 410, 56, (0.45, 0.75, 1.0), 1.0)
        wave(c, t, 600, 70 * ap(since, 0, 0.3), 0.32, (0.45, 0.75, 1.0), 0.95)
        letter(c, "« NOUS SOMMES PRÊTS »", 540, 790, 46, WH, ap(since, 0.3, 0.6), 'Montserrat')
    elif k == 1:
        b = sg['sent'][1]; tm = b[0] + 0.40 * (b[1] - b[0])
        letter(c, "LA TOUR AU KLM", 540, 410, 56, YEL, 1.0)
        wave(c, t, 600, 70, 0.22, YEL, 0.95)
        if t < tm:
            stamp(c, "« OK »", 540, 780, 100, GRN, t - b[0], glow=1.0)
        else:
            stamp(c, "« ATTENDEZ »", 540, 780, 96, ORG, t - tm, glow=1.0)
    else:
        b = sg['sent'][2]; m = ap(t, b[0] + 0.3, b[0] + 1.6)
        letter(c, "TOUR + PAN AM : EN MÊME TEMPS", 540, 410, 50, WH, 1.0)
        wave(c, t, 560, 60, 0.22, YEL, 0.9 * (1 - m * 0.6), seed=1)
        wave(c, t, 640, 60, 0.29, ORG, 0.9 * (1 - m * 0.6), phase=1.0, seed=2)
        if m > 0:                                                                 # somme des deux ondes : battement + sifflement
            c.new_path()
            r = random.Random(int(t * 30))
            for i in range(0, 481):
                x = 110 + 860 * i / 480
                v = 40 * (math.sin(i * 0.11 + t * 9) + math.sin(i * 0.145 + t * 9 + 1)) * (1 + 0.6 * math.sin(i * 0.9 + t * 60)) + 18 * m * r.uniform(-1, 1)
                (c.move_to if i == 0 else c.line_to)(x, 600 + v * m)
            c.set_source_rgba(1, 0.3, 0.3, m); c.set_line_width(3); c.stroke()
            label(c, "SIFFLEMENT", 540, 712, 40, RED, ap(m, 0.5, 0.8), 'Bebas Neue')
        glitch_text(c, "« ATTENDEZ »", 540, 818, 80, ORG, 1.0 - 0.5 * ap(p, 0.6, 1.0), ap(p, 0.25, 0.7), t)
        tag(c, "LE MESSAGE EST BROUILLÉ", 540, 1285, RED, ap(p, 0.5, 0.65), 52)


def sc_tf_roll(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    b0 = sg['sent'][0][0]; spd = min(72.2, 4 + (t - b0) * 24.5)                    # m/s : 260 km/h atteints quand la voix le dit
    if k == 0:
        fog_runway(c, t, 1.0, speed=spd)
        fog_drift(c, t * 3, 1.0)
        stamp(c, "SANS AUTORISATION", 540, 560, 110, RED, since - 0.5, glow=1.0)
        panel(c, 330, 1110, 420, 170, 0.6)
        counter(c, f"{min(260, int(round(spd * 3.6)))} KM/H", "LE KLM ACCÉLÈRE", 540, 1200, YEL, 96)
    else:
        b = sg['sent'][1]; tm = b[0] + 0.45 * (b[1] - b[0])
        fog_runway(c, t, 1.0, speed=spd)
        Z = max(62, 300 - (t - b[0]) * 95)
        fog_plane(c, 'pa_side', Z, t, x=600, xray=0.0)
        fog_drift(c, t * 3, 1.0)
        if t > tm:
            glow(c, 600, 900 + 6 * 900 / Z - 100, 300, RED, 0.25 * (0.6 + 0.4 * math.sin(t * 14)))
            stamp(c, "PAN AM DROIT DEVANT", 540, 560, 100, RED, t - tm, glow=1.0)
        panel(c, 330, 1110, 420, 170, 0.6)
        counter(c, f"{min(260, int(round(spd * 3.6)))} KM/H", "VITESSE DU KLM", 540, 1200, YEL, 96)


def gplane(c, name, xc, yg, width, rot=0.0, alpha=1.0, dark=0.0):
    """avion posé : centre avion en x = xc, bas de l'image (roues) en y = yg, largeur image = width px."""
    s_, b_, pts, (w, h) = P10.spr(name, 0.4)
    im, _ = P10._load(name)
    sc = width / im.width
    cx = pts.get('center', (w / 2, h / 2))[0] / b_
    x0 = xc - cx * sc; y0 = yg - (im.height - 4) * sc
    return plane(c, name, x0 + im.width * sc / 2, y0 + im.height * sc / 2, sc, rot=rot, alpha=alpha, dark=dark), (x0, y0, im.width * sc, im.height * sc)


def wreck_sil(c, x, y, s, a=1.0, col=(0.05, 0.04, 0.04), tail=True):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.new_path(); c.move_to(-200, 0); c.line_to(-210, -40); c.curve_to(-190, -62, -120, -66, -60, -64); c.line_to(-40, -30); c.line_to(10, -70); c.line_to(150, -60)
    c.line_to(170, -20); c.line_to(200, 0); c.close_path()
    if tail: c.move_to(110, -60); c.line_to(150, -160); c.line_to(180, -160); c.line_to(170, -58); c.close_path()
    c.set_source_rgba(*col, a); c.fill(); c.restore()


def sc_tf_impact(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    b = sg['sent'][0]; L = b[1] - b[0]
    if k == 0:
        q = (t - b[0]) / L; q_hit = 0.45
        g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, 0.62, 0.64, 0.67); g.add_color_stop_rgb(0.55, 0.55, 0.58, 0.60); g.add_color_stop_rgb(1, 0.20, 0.22, 0.21)
        c.set_source(g); c.paint()
        c.rectangle(0, 1112, W, H - 1112); c.set_source_rgba(0.16, 0.18, 0.16, 0.9); c.fill()
        c.rectangle(0, 1104, W, 16); c.set_source_rgba(0.12, 0.12, 0.13, 1); c.fill()                   # piste (vue de côté)
        fog_drift(c, t, 0.7, seed=5, y0=800, y1=1150)
        Ppa, bpa = gplane(c, 'pa_front', 560, 1114, 520)
        # KLM : arrive de la droite (nez à gauche), cabre, décolle trop tôt, accroche le dessus du Pan Am, retombe plus loin
        x = 1650 - 2500 * q
        climb = 0.0 if q < 0.22 else ((q - 0.22) * 900 if q < 0.5 else 252 - (q - 0.5) * 1100)
        climb = max(0.0, climb)
        rot = -0.157 * (1 - ap(q, 0.10, 0.24)) - 0.30 * ap(q, 0.5, 0.75)
        Pk, bk = gplane(c, 'klm_rot', x, 1114 - climb, 560, rot=rot)
        if 0.18 < q < 0.36:                                                       # la queue racle la piste
            tx, ty = Pk('tail')
            for j in range(12):
                r = random.Random(j + int(t * 25)); sx = tx + r.uniform(-10, 30); sy = 1106
                c.move_to(sx, sy); c.line_to(sx + r.uniform(30, 110), sy - r.uniform(0, 40)); c.set_source_rgba(1, 0.8, 0.4, 0.8); c.set_line_width(2.5); c.stroke()
        if q < q_hit:
            label(c, "PAN AM", 560, bpa[1] - 20, 44, WH, ap(q, 0.0, 0.1) * (1 - ap(q, 0.25, 0.32)), 'Bebas Neue')
            nx, ny = Pk('center'); label(c, "KLM", nx, ny - 120, 44, (0.45, 0.75, 1.0), ap(q, 0.05, 0.15), 'Bebas Neue')
            tag(c, "LE KLM DÉCOLLE TROP TÔT", 540, 1285, YEL, ap(q, 0.05, 0.15), 50)
        else:
            d = (q - q_hit) * L
            c.save(); c.set_operator(cairo.OPERATOR_ADD); glow(c, 560, 900, 700, (1, 0.85, 0.6), max(0, 1 - d / 0.6)); c.restore()
            flame(c, 600, 930, 0.15, -1, 300, 70, t, inten=min(1, d * 2.5), seed=3, smoke=1.0)
            flame(c, 470, 960, -0.1, -1, 220, 50, t, inten=min(1, d * 2), seed=6, smoke=0.8)
            if q < 0.85:
                kx, ky = Pk('center'); flame(c, kx + 40, ky + 30, 1, -0.15, 220, 34, t, inten=min(1, d * 3), seed=9, smoke=0.6)
            if q > 0.72: glow(c, 0, 1080, 380, (1.0, 0.55, 0.2), 0.8 * ap(q, 0.72, 0.8))
            tag(c, "IL PERCUTE LE DESSUS DU PAN AM", 540, 1285, RED, ap(d, 0.0, 0.2), 46)
        c.set_source_rgba(*FOG, 0.22); c.paint()
    else:
        g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, 0.10, 0.08, 0.08); g.add_color_stop_rgb(0.55, 0.42, 0.22, 0.12); g.add_color_stop_rgb(1, 0.06, 0.04, 0.04)
        c.set_source(g); c.paint()
        for j, (x, s_) in enumerate(((300, 1.0), (790, 0.85))):
            smoke_col(c, x, 1000, 1000, t, 1.0, seed=j + 2, wd=110)
        for j, (x, s_) in enumerate(((300, 1.0), (790, 0.85))):
            wreck_sil(c, x, 1120, 1.5 * s_, 1.0, tail=(j == 0))
            for m in range(3):
                flame(c, x - 160 * s_ + m * 160 * s_, 1060, 0.05 * (m - 1), -1, 360 * s_, 70 * s_, t + m, inten=1.0, seed=j * 3 + m, smoke=0.6)
        r = random.Random(4)
        for j in range(60):                                                       # braises
            ph = (r.random() + t * r.uniform(0.15, 0.4)) % 1; x = r.uniform(120, 960) + 40 * math.sin(t + j)
            c.new_path(); c.arc(x, 1100 - ph * 800, r.uniform(1.5, 3.5), 0, 7); c.set_source_rgba(1, 0.7, 0.3, 0.9 * (1 - ph)); c.fill()
        c.rectangle(0, 1120, W, H - 1120); c.set_source_rgba(0.04, 0.03, 0.03, 0.92); c.fill()
        c.set_source_rgba(*FOG, 0.10); c.paint()
        stamp(c, "LE KÉROSÈNE S'EMBRASE", 540, 520, 96, ORG, since, glow=1.0)


def sc_tf_toll(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    c.set_source_rgb(0.01, 0.012, 0.02); c.paint()
    if k == 0:
        r = random.Random(583)
        for j in range(583):                                                      # 583 lumières
            row, col = j // 22, j % 22
            x = 120 + col * 40 + (row % 2) * 20; y = 380 + row * 28
            a = ap(t, sg['sent'][0][0] + j * 0.0018, sg['sent'][0][0] + j * 0.0018 + 0.4)
            glow(c, x, y, 14, (1.0, 0.75, 0.4), 0.35 * a)
            c.new_path(); c.arc(x, y, 3, 0, 7); c.set_source_rgba(1, 0.92, 0.75, a); c.fill()
        letter(c, "583", 540, 1250, 170, WH, ap(since, 0.0, 0.3))
    else:
        b747_top(c, 540, 860, 10.0, 0.0, (0.75, 0.82, 0.9), 0.85, fill=(0.06, 0.08, 0.12), lw=4, front=(GRN, 0.35 + 0.15 * math.sin(t * 3)))
        letter(c, "PAN AM", 540, 440, 60, WH, 1.0)
        counter(c, "61", "SURVIVANTS", 800, 620, GRN, 150, ap(since, 0.0, 0.3))
        label(c, "TOUS À L'AVANT", 280, 640, 40, GRN, ap(since, 0.3, 0.6), 'Bebas Neue')
        tag(c, "AUCUN SURVIVANT DANS LE KLM", 540, 1285, RED, ap(p, 0.45, 0.6), 48)


def sc_tf_after(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        b = sg['sent'][0]; tm = b[0] + 0.48 * (b[1] - b[0])
        c.set_source_rgb(0.02, 0.03, 0.05); c.paint()
        if t < tm:
            q = ap(t, b[0], tm)
            panel(c, 120, 420, 840, 520, 0.6)
            letter(c, "« DÉCOLLAGE »", 540, 580, 110, YEL, ap(q, 0.0, 0.15))
            letter(c, "UN SEUL USAGE :", 540, 700, 52, WH, ap(q, 0.25, 0.4), 'Montserrat')
            stamp(c, "L'AUTORISATION", 540, 830, 96, GRN, t - (b[0] + 0.5 * (tm - b[0])), glow=1.0)
        else:
            q = ap(t, tm, b[1])
            for j, (x, nm, col) in enumerate(((330, "COMMANDANT", WH), (750, "COPILOTE", GRN))):
                c.new_path(); c.arc(x, 760, 60, 0, 7); c.set_source_rgba(*col, 0.9); c.fill()
                rr(c, x - 90, 830, 180, 230, 50); c.fill()
                letter(c, nm, x, 1120, 44, col, 1.0)
            a = ap(q, 0.1, 0.3)
            rr(c, 600, 500, 300, 150, 40); c.set_source_rgba(*RED, a); c.fill()
            c.move_to(700, 645); c.line_to(740, 700); c.line_to(760, 645); c.close_path(); c.fill()
            letter(c, "STOP !", 750, 600, 84, WH, a)
            tag(c, "LE COPILOTE PEUT DIRE NON", 540, 1285, GRN, ap(q, 0.35, 0.5), 50)
    else:
        fog_runway(c, t, 0.35 * (1 - p) + 0.15, lights=0.6)
        stamp(c, "ÇA A CHANGÉ L'AVIATION", 540, 600, 92, YEL, since, glow=1.0)


SC13 = {k[3:]: v for k, v in globals().items() if k.startswith('sc_') and callable(v)}
