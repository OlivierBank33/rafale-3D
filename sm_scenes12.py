"""29/10 : SURVIVRAIS-TU ? « le crash des Andes » (vol 571, 1972) en style cinéma 3D (aw_*) et DUEL Rafale vs F-22 la revanche (dv_*).
Andes : plaques Blender pr/p_glacier|andes_day|ridge.png (ciel transparent, peint ici), Fokker 50 FlightGear (pr/r_f_*), cartes topo pr/map_sa|zoom.png.
Duel : Rafale glb (pr/r_rf_*) et F-22 FlightGear (pr/r_fx_*)."""
import cairo, math, random, json, os
import numpy as np
from PIL import Image
from sm_lib import *
from sm_scenes2 import ease, ap, ORG, BLUE, RED, WH, GRN
from sm_scenes6 import si, stamp, eout, YEL
from sm_scenes7 import tag, label, check, cross
from sm_scenes11 import frost
import sm_scenes10 as P10
from sm_scenes10 import plane, glow, letter, panel, counter
import pr.andes_map as AM
R = None

# =============================================================== décors andins
_PG = {}
def plate_g(name, mode='day'):
    """plaque Blender (ciel transparent) étalonnée jour / crépuscule / nuit."""
    key = (name, mode)
    if key not in _PG:
        im = Image.open(P10.PR + f'p_{name}.png').convert('RGBA')
        a = np.asarray(im).astype(np.float32)
        rgb, al = a[..., :3] / 255, a[..., 3:4]
        if mode == 'day':
            rgb = np.clip(np.clip((rgb - 0.5) * 1.12 + 0.5, 0, 1) * np.array([0.95, 0.98, 1.0]), 0, 1)
        elif mode == 'dusk':
            lum = rgb.mean(-1, keepdims=True)
            rgb = np.clip(lum * np.array([1.0, 0.70, 0.62]) * 0.85 + rgb * 0.15 + np.array([0.06, 0.02, 0.05]), 0, 1)
        elif mode == 'night':
            lum = rgb.mean(-1, keepdims=True)
            rgb = np.clip(lum ** 1.2 * np.array([0.30, 0.40, 0.66]) * 0.62, 0, 1)
        out = np.concatenate([rgb * 255, al], -1).astype(np.uint8)
        _PG[key] = (P10._surf(Image.fromarray(out, 'RGBA')), im.size)
    return _PG[key]


def sky_paint(c, mode='day', t=0.0):
    g = cairo.LinearGradient(0, 0, 0, 1150)
    if mode == 'day':
        g.add_color_stop_rgb(0, 0.04, 0.16, 0.46); g.add_color_stop_rgb(0.65, 0.30, 0.52, 0.84); g.add_color_stop_rgb(1, 0.70, 0.80, 0.94)
    elif mode == 'dusk':
        g.add_color_stop_rgb(0, 0.08, 0.08, 0.24); g.add_color_stop_rgb(0.6, 0.55, 0.30, 0.42); g.add_color_stop_rgb(1, 1.0, 0.58, 0.36)
    else:
        g.add_color_stop_rgb(0, 0.005, 0.01, 0.04); g.add_color_stop_rgb(1, 0.05, 0.08, 0.16)
    c.set_source(g); c.paint()
    if mode == 'night':
        r = random.Random(4)
        for _ in range(260):
            c.new_path(); c.arc(r.random() * W, r.random() * 1000, r.choice((0.8, 1.0, 1.4, 2.0)), 0, 7)
            c.set_source_rgba(1, 1, 1, (0.3 + 0.6 * r.random()) * (0.8 + 0.2 * math.sin(t * 2 + r.random() * 9))); c.fill()
        glow(c, 820, 260, 160, (0.8, 0.85, 1.0), 0.25); c.new_path(); c.arc(820, 260, 34, 0, 7); c.set_source_rgb(0.93, 0.94, 0.98); c.fill()
    elif mode == 'day':
        glow(c, 860, 230, 420, (1, 0.95, 0.85), 0.25); glow(c, 860, 230, 90, (1, 1, 0.95), 0.6)
        c.new_path(); c.arc(860, 230, 26, 0, 7); c.set_source_rgba(1, 1, 0.97, 0.97); c.fill()


def andes(c, t, name='glacier', mode='day', zoom=1.0, pan=0.0, dy=0.0):
    sky_paint(c, mode, t)
    s, (w, h) = plate_g(name, mode)
    sc = (H / h) * zoom
    x = (W - w * sc) / 2 + pan; y = (H - h * sc) / 2 + dy
    c.save(); c.translate(x, y); c.scale(sc, sc); c.set_source_surface(s, 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint(); c.restore()
    g = cairo.LinearGradient(0, 700, 0, 1150)                                     # brume d'altitude sur l'horizon
    hz = {'day': (0.78, 0.85, 0.96), 'dusk': (1.0, 0.65, 0.5), 'night': (0.10, 0.13, 0.22)}[mode]
    g.add_color_stop_rgba(0, *hz, 0); g.add_color_stop_rgba(0.6, *hz, 0.22); g.add_color_stop_rgba(1, *hz, 0)
    c.rectangle(0, 700, W, 450); c.set_source(g); c.fill()
    g = cairo.LinearGradient(0, 1250, 0, H); g.add_color_stop_rgba(0, 0, 0, 0.02, 0); g.add_color_stop_rgba(1, 0, 0, 0.02, 0.6)   # lisibilité des sous-titres
    c.rectangle(0, 1250, W, H - 1250); c.set_source(g); c.fill()


def snow_fall(c, t, a=1.0, n=140, wind=1.0, seed=2, big=False):
    if a <= 0: return
    r = random.Random(seed)
    for j in range(n):
        sp = r.uniform(60, 160) * (2.5 if big else 1); x0 = r.random() * W; y0 = r.random() * H
        x = (x0 - t * sp * wind * 1.6) % (W + 60) - 30; y = (y0 + t * sp) % (H + 40) - 20
        rad = r.uniform(1.2, 3.2) * (2.2 if big else 1)
        c.new_path(); c.arc(x, y, rad, 0, 7); c.set_source_rgba(1, 1, 1, a * r.uniform(0.4, 0.9)); c.fill()


def wreck(c, t, x, y, sc, mode='day', bury=0.0, a=1.0, light=0.0):
    """fuselage seul (sans ailes ni queue) posé dans la neige, à moitié enfoui."""
    dark = {'day': 0.18, 'dusk': 0.42, 'night': 0.75}[mode]
    P = plane(c, 'f_wreck', x, y, sc, dark=dark, alpha=a)
    nx, ny = P('nose'); tx, ty = P('tail'); cx, cy = P('center')
    if light > 0:                                                                # lueur dans la carlingue (nuit)
        glow(c, cx + (tx - cx) * 0.2, cy - 6 * sc / 0.2, 60 * sc / 0.2, (1.0, 0.7, 0.35), 0.55 * light)
    # ombre douce sous le fuselage + neige qui recouvre le bas (plus enfoui avec bury)
    sh = {'day': (0.25, 0.32, 0.45), 'dusk': (0.25, 0.15, 0.2), 'night': (0.0, 0.0, 0.03)}[mode]
    c.save(); c.translate(cx, max(ny, ty) + 6); c.rotate(math.atan2(ny - ty, nx - tx)); c.scale(1, 0.12)
    L = math.hypot(nx - tx, ny - ty) * 0.6
    g = cairo.RadialGradient(0, 0, 0, 0, 0, L); g.add_color_stop_rgba(0, *sh, 0.3); g.add_color_stop_rgba(1, *sh, 0)
    c.new_path(); c.arc(0, 0, L, 0, 7); c.set_source(g); c.fill(); c.restore()
    if bury > 0:
        snow = {'day': (0.93, 0.95, 1.0), 'dusk': (0.72, 0.56, 0.55), 'night': (0.18, 0.22, 0.36)}[mode]
        c.save(); c.translate(cx, cy + 30 * (1 - bury)); c.rotate(math.atan2(ny - ty, nx - tx)); c.scale(1, 0.35)
        L2 = math.hypot(nx - tx, ny - ty) * 0.62
        g = cairo.RadialGradient(0, 0, 0, 0, 0, L2); g.add_color_stop_rgba(0, *snow, 0.95 * bury); g.add_color_stop_rgba(0.7, *snow, 0.8 * bury); g.add_color_stop_rgba(1, *snow, 0)
        c.new_path(); c.arc(0, 0, L2, 0, 7); c.set_source(g); c.fill(); c.restore()
    return P


def heli(c, x, y, s, t, a=1.0, col=(0.05, 0.06, 0.08)):
    """silhouette d'hélicoptère (vue de profil), rotor flou."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.new_path(); c.save(); c.scale(1.0, 0.62); c.arc(0, 0, 60, 0, 7); c.restore(); c.set_source_rgba(*col, a); c.fill()
    c.move_to(40, -8); c.line_to(190, -14); c.line_to(190, 0); c.line_to(40, 14); c.close_path(); c.fill()
    c.move_to(180, -14); c.line_to(200, -46); c.line_to(210, -46); c.line_to(198, 0); c.close_path(); c.fill()
    c.rectangle(-50, 40, 110, 6); c.fill(); c.move_to(-30, 34); c.line_to(-34, 42); c.move_to(30, 34); c.line_to(34, 42); c.set_source_rgba(*col, a); c.set_line_width(5); c.stroke()
    c.rectangle(-6, -48, 12, 14); c.fill()
    ph = (t * 13) % 1
    c.save(); c.translate(0, -50); c.scale(1, 0.12); c.new_path(); c.arc(0, 0, 170, 0, 7); c.set_source_rgba(*col, 0.25 * a); c.fill(); c.restore()
    c.move_to(-170 * math.cos(ph * 6.28), -50); c.line_to(170 * math.cos(ph * 6.28), -50); c.set_source_rgba(*col, 0.7 * a); c.set_line_width(6); c.stroke()
    c.restore()


def walker(c, x, y, s, t, a=1.0, ph=0.0, col=(0.05, 0.06, 0.08)):
    """randonneur en silhouette (pictogramme), qui gravit une pente vers la gauche."""
    c.save(); c.translate(x, y); c.scale(s, s)
    sw = math.sin(t * 4 + ph) * 0.5
    c.set_source_rgba(*col, a); c.set_line_cap(1); c.set_line_width(9)
    c.move_to(0, -40); c.line_to(-6, -2); c.stroke()                               # tronc penché
    c.move_to(-6, -2); c.line_to(-6 - 16 * sw, 26); c.move_to(-6, -2); c.line_to(-6 + 16 * sw, 26); c.stroke()
    c.move_to(-2, -32); c.line_to(-18, -12 + 6 * sw); c.move_to(-2, -32); c.line_to(12, -16 - 6 * sw); c.stroke()
    c.new_path(); c.arc(2, -52, 9, 0, 7); c.fill()
    rr(c, 2, -42, 14, 22, 4); c.fill()                                             # sac
    c.restore()


def thermo(c, x, y, v, vmin=-35, vmax=10, a=1.0):
    k = (v - vmin) / (vmax - vmin)
    rr(c, x - 26, y - 360, 52, 380, 26); c.set_source_rgba(0.9, 0.95, 1, 0.18 * a); c.fill_preserve(); c.set_source_rgba(1, 1, 1, 0.7 * a); c.set_line_width(4); c.stroke()
    hh = 330 * max(0, min(1, k))
    rr(c, x - 12, y - 10 - hh, 24, hh + 10, 12); c.set_source_rgba(0.45, 0.8, 1.0, a); c.fill()
    c.new_path(); c.arc(x, y + 20, 40, 0, 7); c.set_source_rgba(0.45, 0.8, 1.0, a); c.fill()
    for q in range(vmin, vmax + 1, 10):
        yy = y - 10 - 330 * (q - vmin) / (vmax - vmin)
        c.move_to(x + 30, yy); c.line_to(x + 50, yy); c.set_source_rgba(1, 1, 1, 0.7 * a); c.set_line_width(3); c.stroke()
        letter(c, f"{q}", x + 62, yy + 10, 30, WH, 0.8 * a, 'Montserrat', 'l')


def radio(c, t, a=1.0, on=1.0):
    """poste à transistors des années 70, gros plan."""
    x0, y0, w, h = 210, 640, 660, 440
    glow(c, 540, 860, 520, (1.0, 0.7, 0.4), 0.18 * a)
    rr(c, x0, y0, w, h, 46); c.set_source_rgba(0.32, 0.20, 0.12, a); c.fill()
    rr(c, x0 + 14, y0 + 14, w - 28, h - 28, 36); c.set_source_rgba(0.40, 0.26, 0.15, a); c.fill()
    for j in range(9):                                                           # grille du haut-parleur
        for i in range(9):
            c.new_path(); c.arc(x0 + 80 + i * 30, y0 + 110 + j * 30, 7, 0, 7); c.set_source_rgba(0.12, 0.08, 0.05, a); c.fill()
    rr(c, x0 + 380, y0 + 90, 230, 110, 12); c.set_source_rgba(0.95, 0.88, 0.7, a); c.fill()   # cadran
    for i in range(12):
        xx = x0 + 395 + i * 18; c.move_to(xx, y0 + 110); c.line_to(xx, y0 + 125 + (i % 3 == 0) * 10); c.set_source_rgba(0.2, 0.15, 0.1, a); c.set_line_width(2); c.stroke()
    nx = x0 + 420 + 150 * (0.5 + 0.5 * math.sin(t * 0.4))
    c.move_to(nx, y0 + 100); c.line_to(nx, y0 + 190); c.set_source_rgba(0.85, 0.15, 0.1, a); c.set_line_width(4); c.stroke()
    for k_, xx in enumerate((x0 + 430, x0 + 560)):
        c.new_path(); c.arc(xx, y0 + 300, 46, 0, 7); c.set_source_rgba(0.75, 0.72, 0.65, a); c.fill()
        c.new_path(); c.arc(xx, y0 + 300, 30, 0, 7); c.set_source_rgba(0.55, 0.52, 0.47, a); c.fill()
    c.move_to(x0 + w - 60, y0 + 10); c.line_to(x0 + w + 120, y0 - 300); c.set_source_rgba(0.75, 0.75, 0.78, a); c.set_line_width(7); c.stroke()
    if on > 0:
        for j in range(4):                                                       # ondes
            ph = (t * 1.2 + j / 4) % 1
            c.new_path(); c.arc(x0 + 80 + 120, y0 + 230, 160 + 360 * ph, -2.6, -0.5)
            c.set_source_rgba(1, 0.85, 0.6, 0.35 * (1 - ph) * on * a); c.set_line_width(5); c.stroke()


def map_sa(c, t, prog=1.0, labels=1.0, crash=0.0):
    s, (w, h) = P10.plate('map_sa.png')
    c.set_source_surface(s, 0, 0); c.paint()
    M = AM.MAP['sa']
    pts = [('MONTEVIDEO', (-56.16, -34.90), 'r'), ('MENDOZA', (-68.84, -32.89), 'r'), ('SANTIAGO', (-70.67, -33.45), 'l')]
    plan = [(-68.84, -32.89), (-69.58, -35.4), (-70.53, -35.2), (-71.24, -34.98), (-70.67, -33.45)]
    pp = [M(*q) for q in plan]
    c.new_path(); c.move_to(*pp[0])
    for q in pp[1:]: c.line_to(*q)
    c.set_source_rgba(1, 1, 1, 0.35 * labels); c.set_line_width(3); c.set_dash([6, 8]); c.stroke(); c.set_dash([])
    route = [(-56.16, -34.90), (-68.84, -32.89), (-69.58, -35.4), (-70.53, -35.2)]
    xy = [M(*p) for p in route]
    L = [0]
    for a_, b_ in zip(xy, xy[1:]): L.append(L[-1] + math.hypot(b_[0] - a_[0], b_[1] - a_[1]))
    d = L[-1] * prog
    c.new_path(); c.move_to(*xy[0]); hx, hy = xy[0]
    for i in range(1, len(xy)):
        if L[i] <= d: c.line_to(*xy[i]); hx, hy = xy[i]
        else:
            f = (d - L[i - 1]) / (L[i] - L[i - 1]); hx, hy = xy[i - 1][0] + (xy[i][0] - xy[i - 1][0]) * f, xy[i - 1][1] + (xy[i][1] - xy[i - 1][1]) * f
            c.line_to(hx, hy); break
    c.set_source_rgba(*YEL, 0.95); c.set_line_width(5); c.set_dash([14, 9]); c.stroke(); c.set_dash([])
    if prog > 0: glow(c, hx, hy, 40, YEL, 0.8)
    for nm, (lo, la), an in pts:
        x, y = M(lo, la); c.new_path(); c.arc(x, y, 9, 0, 7); c.set_source_rgb(1, 1, 1); c.fill()
        if nm == 'MONTEVIDEO': letter(c, nm, x, y + 50, 36, WH, labels, anchor='r'); continue
        letter(c, nm, x + (18 if an == 'r' else -18), y - 16, 36, WH, labels, anchor='l' if an == 'r' else 'r')
    letter(c, "ARGENTINE", *M(-64.5, -36.5), 44, (0.6, 0.72, 0.85), 0.8 * labels)
    letter(c, "CHILI", *M(-72.8, -37.6), 40, (0.6, 0.72, 0.85), 0.8 * labels)
    letter(c, "URUGUAY", *M(-56.0, -32.6), 36, (0.6, 0.72, 0.85), 0.8 * labels)
    letter(c, "CORDILLÈRE DES ANDES", *M(-70.3, -30.0), 34, (1.0, 0.9, 0.75), 0.85 * labels)
    if crash > 0:
        x, y = M(-70.29, -34.77); ph = (t * 1.2) % 1
        c.new_path(); c.arc(x, y, 14 + 50 * ph, 0, 7); c.set_source_rgba(*RED, crash * (1 - ph)); c.set_line_width(4); c.stroke()
        glow(c, x, y, 34, RED, 0.8 * crash)


def map_zoom(c, t, view='zoom'):
    s, (w, h) = P10.plate(f'map_{view}.png')
    c.set_source_surface(s, 0, 0); c.paint()
    return AM.MAP[view]


def plane_icon(c, x, y, ang, s=1.0, col=(1, 1, 1), a=1.0):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.new_path(); c.move_to(26, 0); c.line_to(-18, -5); c.line_to(-22, 0); c.line_to(-18, 5); c.close_path()
    c.move_to(4, 0); c.line_to(-8, -24); c.line_to(-14, -24); c.line_to(-8, 0); c.line_to(-14, 24); c.line_to(-8, 24); c.close_path()
    c.move_to(-14, 0); c.line_to(-22, -9); c.line_to(-25, -9); c.line_to(-21, 0); c.line_to(-25, 9); c.line_to(-22, 9); c.close_path()
    c.set_source_rgba(*col, a); c.fill(); c.restore()


# =============================================================== scènes Andes
def sc_aw_hook(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        andes(c, t, 'andes_day', 'day', zoom=1.04 + 0.02 * p, pan=-30 * p)
        x = 760 - 420 * p; y = 760 + 180 * p
        plane(c, 'f_hero', x, y, 0.30 + 0.06 * p)
        for j in range(5):                                                       # nuages qui défilent devant
            ph = (t * 0.25 + j * 0.2) % 1
            glow(c, W + 300 - ph * (W + 700), 980 + j * 70, 260, (1, 1, 1), 0.35)
        tag(c, "LES ANDES · 3 660 M", 540, 1285, WH, ap(p, 0.35, 0.5), 54)
    elif k == 1:
        andes(c, t, 'glacier', 'day', zoom=1.02 + 0.03 * p)
        wreck(c, t, 540, 1120, 0.26)
        snow_fall(c, t, 0.5, 90, 1.6)
        tag(c, "PERSONNE NE VIENDRA", 540, 1285, RED, ap(p, 0.2, 0.35), 56)
    else:
        andes(c, t, 'glacier', 'night', zoom=1.05)
        wreck(c, t, 540, 1120, 0.26, 'night', light=0.8)
        snow_fall(c, t, 0.6, 120, 1.2)
        stamp(c, "72 JOURS", 540, 560, 170, YEL, since, glow=1.0)
        stamp(c, "SURVIVRAIS-TU ?", 540, 1285, 110, RED, since - 0.35, glow=1.0)


def sc_aw_real(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        andes(c, t, 'glacier', 'dusk', zoom=1.06 - 0.03 * p)
        c.set_source_rgba(0, 0, 0, 0.35); c.paint()
        letter(c, "L'HISTOIRE VRAIE DU FILM", 540, 610, 52, WH, ap(since, 0.0, 0.3), 'Montserrat')
        letter(c, "LE CERCLE DES NEIGES", 540, 740, 112, (1, 1, 1), ap(since, 0.25, 0.6))
        c.move_to(260, 790); c.line_to(260 + 560 * eout(ap(since, 0.4, 1.0)), 790); c.set_source_rgba(*YEL, 0.9); c.set_line_width(4); c.stroke()
    else:
        map_sa(c, t, prog=ap(p, 0.05, 0.9))
        letter(c, "13 OCTOBRE 1972", 540, 470, 96, WH, ap(p, 0.0, 0.12))
        q = ap(p, 0.4, 0.55)
        panel(c, 290, 1150, 500, 150, 0.6 * q)
        counter(c, "45 À BORD", "UNE ÉQUIPE DE RUGBY, LEURS PROCHES", 540, 1235, YEL, 84, q)


def sc_aw_crash(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        M = map_zoom(c, t)
        cur = M(-71.24, -34.98); crash = M(-70.29, -34.77)
        for nm, (lo, la) in (('CURICÓ', (-71.24, -34.98)),):
            x, y = M(lo, la); c.new_path(); c.arc(x, y, 9, 0, 7); c.set_source_rgb(1, 1, 1); c.fill(); letter(c, nm, x - 70, y + 60, 40, WH)
        letter(c, "CHILI", *M(-71.55, -34.4), 44, (0.6, 0.72, 0.85), 0.85)
        letter(c, "ARGENTINE", *M(-69.6, -34.4), 44, (0.6, 0.72, 0.85), 0.85)
        q = ap(p, 0.0, 0.7)
        # ce que croit le pilote : déjà au-dessus de Curicó, virage au nord
        gx, gy = cur[0] + 20, cur[1] - 60 * q
        plane_icon(c, gx, gy, -math.pi / 2, 1.6, (1, 1, 1), 0.45)
        c.set_dash([10, 8]); c.new_path(); c.arc(gx, gy, 70, 0, 7); c.set_source_rgba(1, 1, 1, 0.5); c.set_line_width(3); c.stroke(); c.set_dash([])
        tag(c, "CE QUE CROIT LE PILOTE", gx + 60, gy - 120, WH, ap(p, 0.05, 0.2), 42)
        # la réalité : encore au-dessus des montagnes
        rx, ry = crash[0] + 40, crash[1] + 120 - 120 * q
        plane_icon(c, rx, ry, -math.pi / 2 - 0.2, 1.6, RED, 1.0)
        glow(c, rx, ry, 70, RED, 0.5)
        tag(c, "LA RÉALITÉ", rx, ry + 130, RED, ap(p, 0.3, 0.45), 52)
        d = M(-70.29, -34.77)[0] - M(-71.24, -34.98)[0]
        if p > 0.5:
            c.move_to(gx, gy + 40); c.line_to(rx, gy + 40); c.set_source_rgba(*YEL, ap(p, 0.5, 0.65)); c.set_line_width(4); c.stroke()
            letter(c, "ERREUR DE POSITION", (gx + rx) / 2, gy + 90, 40, YEL, ap(p, 0.55, 0.7))
    else:
        b = sg['sent'][1]; t_imp = b[0] + 0.30 * (b[1] - b[0])
        if t < t_imp:
            q = ap(t, b[0], t_imp)
            andes(c, t, 'ridge', 'day', zoom=1.05 + 0.1 * q)
            plane(c, 'f_side', 120 + 560 * q, 820 + 140 * q, 0.34 + 0.05 * q)
            for j in range(6):
                ph = (t * 0.6 + j / 6) % 1
                glow(c, W + 200 - ph * (W + 600), 700 + j * 60, 220, (1, 1, 1), 0.45)
        else:
            q = ap(t, t_imp, b[1])
            andes(c, t, 'glacier', 'day', zoom=1.03, dy=8 * math.exp(-q * 6) * math.sin(q * 40))
            x = 300 + 240 * eout(q); y = 1040 + 80 * eout(q)
            wreck(c, t, x, y, 0.26)
            r = random.Random(3)
            for j in range(60):                                                  # gerbe de neige derrière l'épave qui glisse
                ph = (j / 60 + t * 0.8) % 1
                px = x - 160 - ph * 360 * (1 - q * 0.6) + r.uniform(-30, 30); py = y + 30 - ph * 160 * r.random()
                c.new_path(); c.arc(px, py, r.uniform(4, 14) * (1 - ph), 0, 7); c.set_source_rgba(1, 1, 1, 0.75 * (1 - ph) * (1 - q * 0.8)); c.fill()
            glow(c, 540, 600, 900, (1, 1, 1), 0.7 * max(0, 1 - (t - t_imp) / 0.5))
            tag(c, "725 M DE GLISSADE", 540, 1285, WH, ap(q, 0.25, 0.4), 54)


def sc_aw_cold(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        andes(c, t, 'glacier', 'dusk', zoom=1.04 + 0.02 * p)
        wreck(c, t, 540, 1120, 0.26, 'dusk')
        snow_fall(c, t, 0.5, 90, 1.4)
        for j, (s_, col) in enumerate((("VÊTEMENTS CHAUDS", WH), ("ÉQUIPEMENT", WH), ("NOURRITURE", WH))):
            a = ap(t, sg['sent'][0][0] + 0.5 + j * 0.8, sg['sent'][0][0] + 0.8 + j * 0.8)
            y = 470 + j * 120
            panel(c, 230, y - 60, 620, 96, 0.55 * a)
            letter(c, s_, 330, y + 10, 58, col, a, anchor='l')
            cross(c, 770, y - 12, 0.9, RED, a)
    else:
        andes(c, t, 'glacier', 'night', zoom=1.06)
        wreck(c, t, 540, 1120, 0.26, 'night', light=0.5)
        snow_fall(c, t, 0.75, 160, 2.0)
        v = -30 * eout(ap(p, 0.0, 0.7))
        thermo(c, 830, 760, v)
        letter(c, f"{int(round(v))} °C", 430, 700, 180, (0.6, 0.9, 1.0))
        letter(c, "LA NUIT", 430, 770, 50, WH, ap(p, 0.2, 0.4), 'Montserrat')
        frost(c, t, ap(p, 0.0, 1.0))


def sc_aw_radio(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        c.set_source_rgb(0.03, 0.025, 0.02); c.paint()
        radio(c, t, 1.0, ap(p, 0.2, 0.4))
        letter(c, "JOUR 11", 540, 470, 120, YEL, ap(since, 0.0, 0.3))
    else:
        andes(c, t, 'andes_day', 'day', zoom=1.05)
        x = 300 + 500 * p; y = 640 - 120 * p
        plane(c, 'f_rear', x, y, 0.16 * (1 - 0.5 * p), alpha=1 - 0.6 * p)
        c.set_source_rgba(0, 0, 0, 0.25); c.paint()
        stamp(c, "RECHERCHES", 540, 990, 110, RED, since - 0.2, glow=1.0)
        stamp(c, "ABANDONNÉES", 540, 1150, 110, RED, since - 0.35, glow=1.0)


def sc_aw_decide(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    andes(c, t, 'glacier', 'night', zoom=1.08 + 0.04 * p)
    wreck(c, t, 540, 1120, 0.26, 'night', light=1.0)
    snow_fall(c, t, 0.4, 70, 0.6)
    c.set_source_rgba(0, 0, 0, 0.35); c.paint()
    letter(c, "POUR SURVIVRE", 540, 560, 64, WH, ap(p, 0.0, 0.15), 'Montserrat')
    letter(c, "UNE DÉCISION TERRIBLE", 540, 680, 104, (1, 0.85, 0.6), ap(p, 0.25, 0.45))


def avalanche(c, t, q, mode='night'):
    """nuage de neige qui dévale la pente (en haut à gauche) jusqu'à l'épave (q 0..1)."""
    if q <= 0: return
    col = (0.85, 0.9, 1.0) if mode == 'day' else (0.62, 0.68, 0.86)
    r = random.Random(12)
    front = -150 + 900 * eout(q)
    for j in range(150):
        u_ = r.random(); v_ = r.uniform(-1, 1)
        x = front - u_ * 700
        if x < -250: continue
        y = 520 + 0.85 * (x + 150) + v_ * 150 - 60 * u_
        rad = r.uniform(60, 170) * (0.7 + 0.5 * u_)
        glow(c, x, y, rad, col, 0.55 * (1 - 0.4 * u_))
    for j in range(90):
        x = front - r.random() * 500 + 30 * math.sin(t * 3 + j); y = 520 + 0.85 * (x + 150) + r.uniform(-140, 140)
        c.new_path(); c.arc(x, y, r.uniform(2, 7), 0, 7); c.set_source_rgba(1, 1, 1, 0.85); c.fill()


def sc_aw_aval(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        if p < 0.38:
            c.set_source_rgb(0.02, 0.025, 0.04); c.paint()
            letter(c, "29 OCTOBRE 1972", 540, 860, 120, WH, ap(p, 0.0, 0.08))
            letter(c, "IL Y A 54 ANS, JOUR POUR JOUR", 540, 960, 50, YEL, ap(p, 0.12, 0.22), 'Montserrat')
        else:
            q = ap(p, 0.4, 1.0)
            andes(c, t, 'glacier', 'night', zoom=1.05, dy=6 * math.sin(t * 30) * q * (1 - q))
            wreck(c, t, 540, 1120, 0.26, 'night', light=0.6 * (1 - q), bury=q)
            avalanche(c, t, q)
            snow_fall(c, t, 0.5 + 0.4 * q, 160, 2.5)
            tag(c, "AVALANCHE", 540, 1285, WH, ap(p, 0.45, 0.55), 64)
    else:
        andes(c, t, 'glacier', 'night', zoom=1.05)
        wreck(c, t, 540, 1120, 0.26, 'night', bury=1.0)
        snow_fall(c, t, 0.4, 80, 0.5)
        c.set_source_rgba(0, 0, 0, 0.45); c.paint()
        letter(c, "8 VICTIMES", 540, 760, 120, WH, ap(p, 0.0, 0.25))


def sc_aw_trek(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        andes(c, t, 'ridge', 'day', zoom=1.12, pan=-60 + 60 * p)
        snow_fall(c, t, 0.45, 110, 2.4)
        x0 = 640 - 120 * p; y0 = 980 - 60 * p
        walker(c, x0, y0, 1.7, t)
        walker(c, x0 + 150, y0 + 80, 1.7, t, ph=1.7)
        tag(c, "NANDO PARRADO", x0 - 20, y0 - 170, WH, ap(p, 0.35, 0.5), 42)
        tag(c, "ROBERTO CANESSA", x0 + 170, y0 + 170, WH, ap(p, 0.45, 0.6), 42)
    else:
        M = map_zoom(c, t, 'trek')
        path = [(-70.29, -34.77), (-70.36, -34.755), (-70.42, -34.79), (-70.50, -34.82), (-70.60, -34.86), (-70.72, -34.88)]
        xy = [M(*q) for q in path]
        q = ap(p, 0.0, 0.8); n = len(xy) - 1; f = q * n; i = min(n - 1, int(f)); fr = f - i
        c.new_path(); c.move_to(*xy[0])
        for j in range(1, i + 1): c.line_to(*xy[j])
        hx = xy[i][0] + (xy[i + 1][0] - xy[i][0]) * fr; hy = xy[i][1] + (xy[i + 1][1] - xy[i][1]) * fr
        c.line_to(hx, hy); c.set_source_rgba(*YEL, 0.95); c.set_line_width(6); c.set_dash([12, 8]); c.stroke(); c.set_dash([])
        glow(c, hx, hy, 40, YEL, 0.8); c.new_path(); c.arc(hx, hy, 9, 0, 7); c.set_source_rgb(1, 1, 1); c.fill()
        x, y = xy[0]; c.new_path(); c.arc(x, y, 12, 0, 7); c.set_source_rgb(*RED); c.fill(); letter(c, "ÉPAVE", x + 10, y + 52, 38, RED)
        letter(c, "CHILI", *M(-70.95, -34.6), 44, (0.6, 0.72, 0.85), 0.85)
        letter(c, "ARGENTINE", *M(-70.2, -34.6), 44, (0.6, 0.72, 0.85), 0.85)
        day = 1 + int(9 * q)
        panel(c, 330, 410, 420, 170, 0.55)
        counter(c, f"JOUR {day}", "DE MARCHE", 540, 515, YEL, 110)
        if p > 0.82:
            label(c, "SERGIO CATALÁN", hx - 40, hy - 70, 42, WH, ap(p, 0.82, 0.92), 'Bebas Neue')


def sc_aw_verdict(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        andes(c, t, 'andes_day', 'day', zoom=1.04 + 0.03 * p)
        for j, (x, y, s) in enumerate(((300 + 260 * p, 640, 0.9), (700 + 200 * p, 760, 0.7))):
            heli(c, x, y, s, t + j)
        panel(c, 150, 1040, 780, 250, 0.55)
        stamp(c, "16 SURVIVANTS", 540, 1150, 130, GRN, since, glow=1.0)
        letter(c, "22-23 DÉCEMBRE 1972", 540, 1250, 46, WH, ap(p, 0.3, 0.45), 'Montserrat')
    elif k == 1:
        andes(c, t, 'glacier', 'night', zoom=1.05)
        c.set_source_rgba(0, 0, 0, 0.5); c.paint()
        r = random.Random(29)
        for j in range(29):                                                      # 29 lumières, une par victime
            a = ap(t, sg['sent'][1][0] + j * 0.045, sg['sent'][1][0] + j * 0.045 + 0.3)
            row = j // 10; col = j % 10
            x = 150 + col * 87 + (row % 2) * 40 + r.uniform(-8, 8); y = 1040 + row * 70 + r.uniform(-6, 6)
            fl = 0.85 + 0.15 * math.sin(t * 7 + j)
            glow(c, x, y, 34, (1.0, 0.75, 0.4), 0.55 * a * fl)
            c.new_path(); c.arc(x, y, 5, 0, 7); c.set_source_rgba(1, 0.95, 0.8, a); c.fill()
        letter(c, "29 VICTIMES", 540, 760, 110, WH, ap(p, 0.0, 0.2))
    else:
        andes(c, t, 'andes_day', 'dusk', zoom=1.06)
        stamp(c, "ET TOI ?", 540, 640, 170, ORG, since, glow=1.0)
        letter(c, "TU AURAIS TENU ?", 540, 760, 60, WH, ap(since, 0.3, 0.6), 'Montserrat')


# =============================================================== DUEL : Rafale vs F-22, la revanche (dv_*)
CA = (0.30, 0.58, 1.0); CB = (1.0, 0.32, 0.26)
JA = {'hero': 'rf_hero', 'side': 'rf_side', 'top': 'rf_top', 'rear': 'rf_rear'}
JB = {'hero': 'fx_hero', 'side': 'fx_side', 'top': 'fx_top', 'rear': 'fx_rear'}
DKB = 0.38                                                   # le F-22 est gris foncé (le modèle 3D sort très clair)


def jet(c, side, view, x, y, sc, rot=0.0, alpha=1.0, anchor='img'):
    return plane(c, (JA if side == 'A' else JB)[view], x, y, sc, rot=rot, alpha=alpha, dark=(0 if side == 'A' else DKB), anchor=anchor)


def ab_flame(c, x, y, dx, dy, L, w, t, a=1.0):
    """postcombustion : cône additif + diamants de choc."""
    if a <= 0: return
    nx, ny = -dy, dx
    c.save(); c.set_operator(cairo.OPERATOR_ADD)
    fl = 0.9 + 0.1 * math.sin(t * 60)
    c.new_path(); c.move_to(x + nx * w, y + ny * w); c.line_to(x + dx * L * fl, y + dy * L * fl); c.line_to(x - nx * w, y - ny * w); c.close_path()
    g = cairo.LinearGradient(x, y, x + dx * L, y + dy * L); g.add_color_stop_rgba(0, 1, 0.75, 0.45, 0.9 * a); g.add_color_stop_rgba(0.5, 1, 0.45, 0.2, 0.5 * a); g.add_color_stop_rgba(1, 0.6, 0.3, 1, 0)
    c.set_source(g); c.fill()
    for k_ in range(4):
        f = 0.18 + k_ * 0.17; px, py = x + dx * L * f, y + dy * L * f
        glow(c, px, py, w * (0.9 - k_ * 0.15), (1, 0.85, 0.7), 0.6 * a)
    c.restore()


def score_hud(c, sa, sb, y=250, a=1.0, flash=None, since=9.0):
    if a <= 0: return
    panel(c, 190, y - 70, 700, 120, 0.55 * a, 30)
    letter(c, "RAFALE", 330, y + 12, 58, CA, a); letter(c, "F-22", 750, y + 12, 58, CB, a)
    sz = 92
    for v, x, col, sd in ((sa, 485, CA, 'A'), (sb, 595, CB, 'B')):
        k = 1.0
        if flash == sd and since < 0.5: k = 1 + 0.5 * math.sin(min(1, since / 0.5) * math.pi)
        c.save(); c.translate(x, y + 18); c.scale(k, k); letter(c, str(v), 0, 0, sz, col if flash == sd and since < 1.2 else WH, a); c.restore()
    letter(c, "-", 540, y + 8, 70, WH, 0.7 * a)


def round_card(c, t, n, title, since, a=1.0):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, 0.02, 0.03, 0.07); g.add_color_stop_rgb(1, 0.06, 0.09, 0.18); c.set_source(g); c.paint()
    for j in range(0, W, 60): c.move_to(j, 0); c.line_to(j, H)
    for j in range(0, H, 60): c.move_to(0, j); c.line_to(W, j)
    c.set_source_rgba(0.4, 0.7, 1, 0.05); c.set_line_width(1); c.stroke()
    jet(c, 'A', 'hero', 300 - 60 * eout(min(1, since / 0.8)), 1120, 0.20, alpha=0.9)
    jet(c, 'B', 'hero', 780 + 60 * eout(min(1, since / 0.8)), 1120, 0.20, alpha=0.9)
    letter(c, n, 540, 650, 150, YEL, a)
    stamp(c, title, 540, 830, 120, WH, since - 0.15, glow=0.8)


def mach_bar(c, x, y, w, v, vmax, col, lab, a=1.0, txt=None):
    rr(c, x, y, w, 64, 32); c.set_source_rgba(1, 1, 1, 0.1 * a); c.fill()
    ww = max(64, w * min(1, v / vmax))
    rr(c, x, y, ww, 64, 32); c.set_source_rgba(*col, a); c.fill()
    letter(c, lab, x - 20, y + 48, 46, col, a, anchor='r')
    letter(c, txt or f"MACH {v:.1f}".replace('.', ','), x + ww - 24, y + 47, 44, WH, a, anchor='r')


def sky_dark(c, t):
    P10.sky_bg(c, t, False, 300)
    c.set_source_rgba(0.0, 0.02, 0.08, 0.25); c.paint()


def sc_dv_hook(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    sky_dark(c, t)
    if k == 0:
        q = eout(ap(p, 0.0, 0.6))
        PA = jet(c, 'A', 'hero', -200 + 560 * q, 820, 0.26)
        PB = jet(c, 'B', 'hero', 1280 - 560 * q, 1150, 0.26)
        if p > 0.55:
            stamp(c, "VS", 540, 1000, 200, YEL, since - 0.55 * (sg['sent'][1][0] - sg['sent'][0][0]), glow=1.0)
    elif k == 1:
        PA = jet(c, 'A', 'hero', 360, 760, 0.26)
        PB = jet(c, 'B', 'hero', 720, 1150, 0.26)
        tag(c, "FRANCE", 300, 520, CA, ap(p, 0.05, 0.2), 64)
        tag(c, "USA", 760, 1290, CB, ap(p, 0.45, 0.6), 64)
    else:
        jet(c, 'A', 'hero', 300, 900, 0.22, alpha=0.9)
        jet(c, 'B', 'hero', 780, 900, 0.22, alpha=0.9)
        stamp(c, "LA REVANCHE", 540, 640, 150, YEL, since, glow=1.0)
        score_hud(c, 0, 0, 1150, ap(p, 0.3, 0.5))


def sc_dv_speed(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        round_card(c, t, "ROUND 1", "LA VITESSE", since); return
    sky_dark(c, t)
    for j in range(40):                                                          # lignes de vitesse
        r = random.Random(j); y = r.uniform(300, 1350); ph = (t * r.uniform(1.5, 3) + r.random()) % 1
        x = W + 200 - ph * (W + 600); c.move_to(x, y); c.line_to(x + r.uniform(120, 320), y); c.set_source_rgba(1, 1, 1, 0.18); c.set_line_width(2); c.stroke()
    t1 = sg['sent'][1][0]; t2 = sg['sent'][2][0]
    qa = ap(t, t1, t1 + 2.0); qb = ap(t, t2, t2 + 3.0)
    xa = 300 + 120 * qa + (40 * math.sin(t * 2))
    PA = jet(c, 'A', 'side', xa, 720, 0.30)
    nx, ny = PA('nose'); ax, ay = PA('aft'); d = math.hypot(nx - ax, ny - ay) or 1
    ab_flame(c, ax, ay, (ax - nx) / d, (ay - ny) / d, 180, 18, t, 1.0)
    if k >= 2:
        xb = -400 + 1000 * eout(qb)
        PB = jet(c, 'B', 'side', xb, 1010, 0.30)
        nx, ny = PB('nose'); bx, by = PB('aft'); d = math.hypot(nx - bx, ny - by) or 1
        ab_flame(c, bx, by, (bx - nx) / d, (by - ny) / d, 140, 16, t, 0.35 if p > 0.5 else 1.0)
        c.move_to(nx + 20, ny); c.line_to(nx + 140, ny); c.set_source_rgba(*CB, 0.9); c.set_line_width(8); c.stroke()  # vecteur vitesse
        c.move_to(nx + 140, ny - 18); c.line_to(nx + 168, ny); c.line_to(nx + 140, ny + 18); c.close_path(); c.fill()
        if k == 2 and p > 0.45: tag(c, "MACH 1,5 SANS POSTCOMBUSTION", 540, 470, CB, ap(p, 0.45, 0.6), 46)
    mach_bar(c, 330, 1150, 560, 1.8 * qa, 2.4, CA, "RAFALE", ap(t, t1, t1 + 0.3), "MACH 1,8")
    if k >= 2:
        mach_bar(c, 330, 1235, 560, 2.25 * qb, 2.4, CB, "F-22", ap(t, t2, t2 + 0.3), "+ DE MACH 2")
    score_hud(c, 0, 1 if k >= 3 else 0, 250, 1.0, 'B' if k >= 3 else None, t - sg['sent'][3][0] if k >= 3 else 9)
    if k >= 3: stamp(c, "POINT F-22", 540, 480, 120, CB, since, glow=1.0)


def radar_scope(c, cx, cy, r, t, blips, a=1.0):
    c.new_path(); c.arc(cx, cy, r, 0, 7); c.set_source_rgba(0.0, 0.08, 0.04, 0.85 * a); c.fill()
    for f in (0.33, 0.66, 1.0):
        c.new_path(); c.arc(cx, cy, r * f, 0, 7); c.set_source_rgba(0.3, 1, 0.5, 0.3 * a); c.set_line_width(2); c.stroke()
    ang = (t * 1.6) % (2 * math.pi)
    for j in range(30):
        aa = ang - j * 0.03
        c.move_to(cx, cy); c.line_to(cx + r * math.cos(aa), cy + r * math.sin(aa)); c.set_source_rgba(0.3, 1, 0.5, 0.3 * (1 - j / 30) * a); c.set_line_width(4); c.stroke()
    for (bx, by, bs, col) in blips:
        ba = math.atan2(by, bx); age = (ang - ba) % (2 * math.pi)
        lum = max(0.15, 1 - age / 5)
        if bs > 0:
            glow(c, cx + bx * r, cy + by * r, bs * 2.2, col, 0.7 * lum * a)
            c.new_path(); c.arc(cx + bx * r, cy + by * r, bs, 0, 7); c.set_source_rgba(*col, lum * a); c.fill()


def sc_dv_stealth(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        round_card(c, t, "ROUND 2", "LA FURTIVITÉ", since); return
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, 0.01, 0.02, 0.05); g.add_color_stop_rgb(1, 0.03, 0.07, 0.12); c.set_source(g); c.paint()
    side = 'B' if k == 1 else 'A'
    if k >= 3: side = 'A'
    P = jet(c, side, 'top', 540, 690, 0.22, rot=0.0)
    for j in range(6):                                                           # ondes radar qui montent vers l'avion
        ph = (t * 0.9 + j / 6) % 1
        c.new_path(); c.arc(540, 1700, 200 + 1100 * ph, math.pi * 1.25, math.pi * 1.75); c.set_source_rgba(0.3, 1, 0.5, 0.35 * (1 - ph)); c.set_line_width(4); c.stroke()
    ret = 0.12 if side == 'B' else 1.0                                           # écho renvoyé
    for j in range(4):
        ph = (t * 0.9 + j / 4) % 1
        c.new_path(); c.arc(540, 690, 60 + 600 * ph, math.pi * 0.25, math.pi * 0.75); c.set_source_rgba(1, 0.8, 0.3, 0.45 * (1 - ph) * ret); c.set_line_width(4 + 6 * ret); c.stroke()
    blips = [(0.25, -0.45, 3 if side == 'B' else 16, CB if side == 'B' else CA)]
    radar_scope(c, 540, 1120, 170, t, blips)
    if side == 'B':
        tag(c, "MISSILES EN SOUTE", 540, 410, CB, ap(p, 0.45, 0.6), 52)
        tag(c, "ÉCHO RADAR MINUSCULE", 540, 1330 - 30, CB, ap(p, 0.2, 0.35), 46)
    else:
        if k == 2: tag(c, "DISCRET, PAS FURTIF", 540, 410, CA, ap(p, 0.1, 0.25), 52)
    score_hud(c, 0, 2 if k >= 3 else 1, 250, 1.0, 'B' if k >= 3 else None, t - sg['sent'][3][0] if k >= 3 else 9)
    if k >= 3: stamp(c, "2 À 0", 540, 470, 130, CB, since, glow=1.0)


ROLES = [("COMBAT AÉRIEN", 28.0), ("FRAPPE AU SOL", 28.8), ("RECONNAISSANCE", 29.57), ("DISSUASION NUCLÉAIRE", 30.31), ("PORTE-AVIONS", 31.67)]
def sc_dv_multi(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        round_card(c, t, "ROUND 3", "LA POLYVALENCE", since); return
    sky_dark(c, t)
    if k == 1 or k == 3:
        jet(c, 'A', 'hero', 540, 1060, 0.28)
        for j, (nm, t0) in enumerate(ROLES):
            a = ap(t, t0 - 0.1, t0 + 0.15) * (0.35 if k == 3 else 1.0)
            tag(c, nm, 540, 440 + j * 88, CA, a, 50)
        if k == 3: stamp(c, "POINT RAFALE", 540, 640, 130, YEL, since, glow=1.0)
    else:
        jet(c, 'B', 'hero', 540, 1060, 0.28)
        tag(c, "SUPÉRIORITÉ AÉRIENNE", 540, 560, CB, ap(p, 0.4, 0.55), 56)
    score_hud(c, 1 if k >= 3 else 0, 2, 250, 1.0, 'A' if k >= 3 else None, t - sg['sent'][3][0] if k >= 3 else 9)


_WM = {}
EXP = ['Egypt', 'Qatar', 'India', 'Greece', 'Croatia', 'United Arab Emirates', 'Indonesia', 'Republic of Serbia']
EXPFR = {'Egypt': 'ÉGYPTE', 'Qatar': 'QATAR', 'India': 'INDE', 'Greece': 'GRÈCE', 'Croatia': 'CROATIE', 'United Arab Emirates': 'ÉMIRATS', 'Indonesia': 'INDONÉSIE', 'Republic of Serbia': 'SERBIE'}
def wm_proj(view):
    if view == 'eur':
        lon0, lon1, latc, yc = -12.0, 142.0, 22.0, 860
    else:
        lon0, lon1, latc, yc = -128.0, -62.0, 38.0, 860
    k = W / (lon1 - lon0); ky = k / math.cos(math.radians(latc))
    return lambda lo, la: ((lo - lon0) * k, yc - (la - latc) * ky)


def world_map(c, view, hi=(), hi_col=CA, hi_a=None, t=0.0):
    if view not in _WM:
        feats = json.load(open('/home/claude/geo/ne50.geojson'))['features']
        Pj = wm_proj(view); geo = {}
        sur = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); cc = cairo.Context(sur)
        cc.set_source_rgb(0.02, 0.035, 0.07); cc.paint()
        for f in feats:
            g = f['geometry']; parts = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
            pl = []
            for poly in parts:
                ring = poly[0]; xy = [Pj(lo, la) for lo, la in ring]
                if max(x for x, y in xy) < -50 or min(x for x, y in xy) > W + 50 or max(y for x, y in xy) < 0 or min(y for x, y in xy) > H: continue
                pl.append(xy)
                cc.new_path(); cc.move_to(*xy[0])
                for q in xy[1:]: cc.line_to(*q)
                cc.close_path(); cc.set_source_rgb(0.10, 0.13, 0.18); cc.fill_preserve(); cc.set_source_rgba(0.5, 0.65, 0.85, 0.35); cc.set_line_width(1); cc.stroke()
            geo[f['properties']['ADMIN']] = pl
        _WM[view] = (sur, geo, Pj)
    sur, geo, Pj = _WM[view]
    c.set_source_surface(sur, 0, 0); c.paint()
    for j, nm in enumerate(hi):
        a = hi_a[j] if hi_a else 1.0
        if a <= 0: continue
        col = hi_col if nm != 'France' else (0.95, 0.95, 1.0)
        for xy in geo.get(nm, []):
            c.new_path(); c.move_to(*xy[0])
            for q in xy[1:]: c.line_to(*q)
            c.close_path(); c.set_source_rgba(*col, 0.85 * a); c.fill_preserve(); c.set_source_rgba(1, 1, 1, 0.8 * a); c.set_line_width(1.5); c.stroke()
    return geo, Pj


CENT = {'France': (2.3, 46.6), 'Egypt': (30.8, 26.8), 'Qatar': (51.2, 25.3), 'India': (78.9, 21.5), 'Greece': (22.0, 39.3), 'Croatia': (16.0, 45.3),
        'United Arab Emirates': (54.2, 23.8), 'Indonesia': (113.9, -1.0), 'Republic of Serbia': (20.9, 44.0)}
def sc_dv_export(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        round_card(c, t, "ROUND 4", "L'EXPORT", since); return
    if k in (1,) or (k == 3 and False):
        t1 = sg['sent'][1][0]
        al = [ap(t, t1 + 0.25 * j, t1 + 0.25 * j + 0.3) for j in range(len(EXP))]
        geo, Pj = world_map(c, 'eur', ['France'] + EXP, CA, [1.0] + al, t)
        fx, fy = Pj(*CENT['France'])
        for j, nm in enumerate(EXP):
            if al[j] <= 0: continue
            x, y = Pj(*CENT[nm]); mx, my = (fx + x) / 2, min(fy, y) - 120
            c.move_to(fx, fy); c.curve_to(mx, my, mx, my, fx + (x - fx) * al[j], fy + (y - fy) * al[j]); c.set_source_rgba(1, 1, 1, 0.6); c.set_line_width(2.5); c.stroke()
        for j, nm in enumerate(EXP):
            x, y = Pj(*CENT[nm]); label(c, EXPFR[nm], x + {'Croatia': -60, 'Qatar': -30, 'United Arab Emirates': 40}.get(nm, 0), y + {'Croatia': -40, 'Greece': 46, 'Republic of Serbia': -12, 'Qatar': -26, 'United Arab Emirates': 70}.get(nm, 50), 36, WH, al[j], 'Bebas Neue')
        n = sum(1 for a in al if a > 0.5)
        panel(c, 330, 1130, 420, 170, 0.6)
        counter(c, f"{n} PAYS", "ONT COMMANDÉ LE RAFALE", 540, 1225, CA, 100)
    else:
        geo, Pj = world_map(c, 'usa', ['United States of America'], CB, [1.0], t)
        x, y = Pj(-98, 39)
        rr(c, x - 60, y - 20, 120, 100, 18); c.set_source_rgb(0.85, 0.8, 0.7); c.fill()                            # cadenas
        c.new_path(); c.arc(x, y - 20, 42, math.pi, 0); c.set_source_rgb(0.85, 0.8, 0.7); c.set_line_width(16); c.stroke()
        c.new_path(); c.arc(x, y + 25, 12, 0, 7); c.set_source_rgb(0.2, 0.2, 0.2); c.fill()
        stamp(c, "INTERDIT À L'EXPORT", 540, 1180, 100, CB, since - 0.4, glow=1.0)
        letter(c, "PAR LA LOI AMÉRICAINE", 540, 1260, 44, WH, ap(p, 0.4, 0.6), 'Montserrat')
    score_hud(c, 2 if k >= 3 else 1, 2, 250, 1.0, 'A' if k >= 3 else None, t - sg['sent'][3][0] if k >= 3 else 9)
    if k >= 3: stamp(c, "2 PARTOUT", 540, 520, 130, YEL, since, glow=1.0)


def timeline(c, y, y0, y1, xA, xB, a=1.0):
    c.move_to(xA, y); c.line_to(xB, y); c.set_source_rgba(1, 1, 1, 0.5 * a); c.set_line_width(3); c.stroke()
    for yr in range(y0, y1 + 1, 5):
        x = xA + (xB - xA) * (yr - y0) / (y1 - y0)
        c.move_to(x, y - 10); c.line_to(x, y + 10); c.stroke()
        letter(c, str(yr), x, y + 50, 30, WH, 0.7 * a, 'Montserrat')


def sc_dv_prod(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        round_card(c, t, "DERNIER ROUND", "L'AVENIR", since); return
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, 0.02, 0.03, 0.07); g.add_color_stop_rgb(1, 0.05, 0.08, 0.16); c.set_source(g); c.paint()
    X0, X1, Y0, Y1 = 120, 960, 1995, 2030
    def X(yr): return X0 + (X1 - X0) * (yr - Y0) / (Y1 - Y0)
    timeline(c, 1170, Y0, Y1, X0, X1)
    t1 = sg['sent'][1][0]; qb = ap(t, t1, t1 + 2.6)
    yrB = 1997 + 14 * qb
    jet(c, 'B', 'side', 540, 640 if k == 1 else 500, 0.26 if k == 1 else 0.2, alpha=1.0 if k == 1 else 0.45)
    c.move_to(X(1997), 990); c.line_to(X(yrB), 990); c.set_source_rgba(*CB, 1); c.set_line_width(26); c.set_line_cap(1); c.stroke()
    letter(c, f"{int(195 * qb)}", X(yrB), 955, 64, CB)
    if qb >= 1:
        stamp(c, "STOP 2011", X(2011) + 40, 880, 80, CB, t - t1 - 2.6, glow=1.0)
    if k >= 2:
        t2 = sg['sent'][2][0]; qa = ap(t, t2, t2 + 1.6)
        yrA = 2001 + 27 * eout(qa)
        c.move_to(X(2001), 1090); c.line_to(X(yrA), 1090); c.set_source_rgba(*CA, 1); c.set_line_width(26); c.set_line_cap(1); c.stroke()
        xe = X(yrA); c.move_to(xe + 10, 1068); c.line_to(xe + 48, 1090); c.line_to(xe + 10, 1112); c.close_path(); c.fill()
        jet(c, 'A', 'side', 540, 720, 0.26)
        tag(c, "TOUJOURS EN PRODUCTION", 540, 1290, CA, ap(qa, 0.5, 0.8), 48)
    score_hud(c, 3 if k >= 3 else 2, 2, 250, 1.0, 'A' if k >= 3 else None, t - sg['sent'][3][0] if k >= 3 else 9)
    if k >= 3: stamp(c, "POINT RAFALE", 540, 470, 120, YEL, since, glow=1.0)


def sc_dv_verdict(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    sky_dark(c, t)
    if k == 0:
        PA = jet(c, 'A', 'hero', 540, 900, 0.32)
        glow(c, 540, 900, 500, CA, 0.25)
        score_hud(c, 3, 2, 520, 1.0, 'A', since)
        stamp(c, "VICTOIRE DU RAFALE", 540, 1250, 100, YEL, since - 0.3, glow=1.0)
    elif k == 1:
        jet(c, 'B', 'hero', 540, 900, 0.32)
        tag(c, "EN COMBAT AÉRIEN PUR", 540, 520, WH, ap(p, 0.05, 0.2), 52)
        stamp(c, "LE ROI DU CIEL", 540, 1250, 120, CB, since - 1.0, glow=1.0)
    else:
        jet(c, 'A', 'hero', 320, 800, 0.24)
        jet(c, 'B', 'hero', 760, 1150, 0.24)
        stamp(c, "ET TOI ?", 540, 560, 170, ORG, since, glow=1.0)
        letter(c, "TU METS QUI ?", 540, 680, 60, WH, ap(since, 0.3, 0.6), 'Montserrat')


SC12 = {k[3:]: v for k, v in globals().items() if k.startswith('sc_') and callable(v)}
