"""28/10 : SURVIVRAIS-TU ? « le pare-brise explose » (Sichuan 3U8633, A319 3D, style cinéma : sw_*) et
TU ES LE PILOTE ép. 4 = finale (stickman, e4_*). Les sprites A319 viennent de pr/pr3d_fg.py (pr/r_u_*.png + .json)."""
import cairo, math, random, json
from sm_lib import *
from sm_scenes2 import ease, ap, sky, ORG, BLUE, RED, WH, GRN
from sm_scenes6 import si, stamp, eout, YEL
from sm_scenes7 import tag, label, mix, check, cross, gauge, twin, pov_beach, mini_beach
import sm_scenes10 as P10
from sm_scenes10 import plane, glow, letter, panel, counter, sky_bg, runway_side, grade, sun_flare, CY
R = None


# =============================================================== SICHUAN 3U8633 (sw_*)
def alt_sky(c, t, oy=0, sun=(880, 250)):
    """ciel de croisière : bleu profond en haut, mer de nuages en bas, soleil net."""
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, 0.03, 0.12, 0.36); g.add_color_stop_rgb(0.55, 0.22, 0.45, 0.78); g.add_color_stop_rgb(0.72, 0.7, 0.82, 0.95)
    c.set_source(g); c.paint()
    sx, sy = sun
    glow(c, sx, sy, 520, (1, 0.92, 0.75), 0.28); glow(c, sx, sy, 110, (1, 0.97, 0.88), 0.55)
    c.new_path(); c.arc(sx, sy, 30, 0, 7); c.set_source_rgba(1, 1, 0.97, 0.97); c.fill()
    r = random.Random(8)
    for j in range(140):                                     # mer de nuages
        y = 1250 + r.random() ** 1.3 * 700 + oy; x = (r.random() * 1600 - t * (8 + 12 * (y - 1250) / 700)) % 1600 - 260
        w = 60 + 220 * (y - 1200) / 700 * r.uniform(0.6, 1.3)
        c.save(); c.translate(x, y); c.scale(1, 0.28); g = cairo.RadialGradient(0, 0, 0, 0, 0, w)
        sh = 0.86 + 0.12 * r.random(); g.add_color_stop_rgba(0, sh, sh, sh * 1.02, 0.95); g.add_color_stop_rgba(1, sh, sh, sh, 0)
        c.new_path(); c.arc(0, 0, w, 0, 7); c.set_source(g); c.fill(); c.restore()


_EXTRA = {'u_noseR': {'pc': (1375, 1250), 'p1': (1295, 1212), 'p2': (1409, 1203), 'p3': (1467, 1268), 'p4': (1390, 1295), 'p5': (1312, 1293)}}
def _extra(name):
    im, pts = P10._load(name)
    if name in _EXTRA and 'pc' not in pts:
        js = json.load(open(P10.PR + f'r_{name}.json'))['pts']
        ox, oy = js['nose'][0] - pts['nose'][0], js['nose'][1] - pts['nose'][1]
        for k_, (x, y) in _EXTRA[name].items(): pts[k_] = (x - ox, y - oy)


def crack_web(c, ox, oy, R_, k, seed=3):
    """fissure en toile d'araignée centrée (ox, oy), rayon R_ (k 0..1). Le clip est fait par l'appelant."""
    if k <= 0: return
    r = random.Random(seed)
    for j in range(13):
        a = j / 13 * 6.283 + r.uniform(-0.2, 0.2); L = R_ * r.uniform(0.6, 1.25) * k
        c.move_to(ox, oy); px, py = ox, oy
        for m in range(5):
            px += math.cos(a + r.uniform(-0.35, 0.35)) * L / 5; py += math.sin(a + r.uniform(-0.35, 0.35)) * L / 5; c.line_to(px, py)
    for f in (0.22, 0.45, 0.72):
        rad = R_ * f
        if rad > R_ * 1.1 * k: continue
        for j in range(13):
            a0 = j / 13 * 6.283; a1 = (j + 1) / 13 * 6.283; r0 = rad * r.uniform(0.85, 1.15)
            c.move_to(ox + math.cos(a0) * r0, oy + math.sin(a0) * r0); c.line_to(ox + math.cos(a1) * rad * r.uniform(0.85, 1.15), oy + math.sin(a1) * rad * r.uniform(0.85, 1.15))
    c.set_source_rgba(1, 1, 1, 0.92); c.set_line_width(2.2); c.stroke()
    glow(c, ox, oy, R_ * 0.25, (1, 1, 1), 0.5 * k)


def burst(c, x, y, since, s=1.0, dx=-1.0, dy=-0.25):
    """éclatement : éclair, éclats de verre et brouillard de décompression emportés vers l'arrière ; s'efface en ~2 s."""
    if since < 0: return
    e = eout(min(1.0, since / 0.9)); fade = max(0.0, 1 - since / 2.2)
    if fade <= 0: return
    glow(c, x, y, (80 + 320 * e) * s, (1, 1, 1), 0.85 * max(0, 1 - since / 0.6))
    r = random.Random(11); base = math.atan2(dy, dx)
    for j in range(46):
        a = base + r.uniform(-0.9, 0.9); d = (20 + 700 * e * r.uniform(0.3, 1.0)) * s
        px, py = x + math.cos(a) * d, y + math.sin(a) * d + 90 * e * e * r.random()
        c.save(); c.translate(px, py); c.rotate(r.random() * 6 + since * r.uniform(-7, 7))
        sz = r.uniform(4, 13) * s
        c.new_path(); c.move_to(-sz, -sz * 0.4); c.line_to(sz, -sz * 0.7); c.line_to(sz * 0.5, sz * 0.6); c.close_path()
        c.set_source_rgba(0.85, 0.93, 1, 0.9 * fade); c.fill_preserve(); c.set_source_rgba(1, 1, 1, fade); c.set_line_width(1); c.stroke(); c.restore()
    for j in range(16):
        a = base + r.uniform(-0.35, 0.35); d = (30 + 820 * e * r.uniform(0.4, 1.0)) * s
        glow(c, x + math.cos(a) * d, y + math.sin(a) * d, (40 + 150 * e) * s, (0.95, 0.97, 1), 0.4 * fade * (1 - 0.5 * e))


def wind_lines(c, t, a, y0=300, y1=1300, n=26, seed=6):
    if a <= 0: return
    r = random.Random(seed)
    for j in range(n):
        y = r.uniform(y0, y1); sp = r.uniform(1.2, 2.4); ph = (t * sp + r.random()) % 1
        x = W + 200 - ph * (W + 600); L = r.uniform(120, 300)
        c.move_to(x, y); c.line_to(x + L, y + L * 0.05); c.set_source_rgba(1, 1, 1, 0.22 * a); c.set_line_width(r.uniform(1.5, 3)); c.stroke()


def half_out(c, hx, hy, k, t, a=1.0):
    """silhouette du copilote à moitié sorti, plaquée par le vent vers l'arrière (gauche), en contre-jour, voilée de brume. Sobre."""
    if a <= 0: return
    th = math.radians(-154); ux, uy = math.cos(th), math.sin(th); nx, ny = uy, -ux
    fl = math.sin(t * 23) * 2.5; fl2 = math.sin(t * 31 + 1) * 6
    def T(u, v): return hx + (u * ux + v * nx) * k, hy + (u * uy + v * ny) * k
    torso = [(0, -19), (55, -25 + fl * 0.4), (100, -29 + fl), (118, -22), (126, -9), (124, 10), (100, 21), (50, 22), (0, 19)]
    neck = [(120, -8), (141, -6), (141, 8), (120, 10)]
    arm1 = [(108, -16), (146, -58 + fl2), (196, -76 + fl2 * 1.6)]
    arm2 = [(106, 8), (72, 40), (24, 32)]
    def poly(pts, grow=0.0):
        c.new_path(); x, y = T(*pts[0]); c.move_to(x, y)
        for p_ in pts[1:]: c.line_to(*T(*p_))
        c.close_path()
    def limb(pts, w0, w1, col, al, grow):
        for (u0, v0), (u1, v1), (wa, wb) in zip(pts, pts[1:], ((w0, (w0 + w1) / 2), ((w0 + w1) / 2, w1))):
            c.move_to(*T(u0, v0)); c.line_to(*T(u1, v1)); c.set_source_rgba(*col, al * a); c.set_line_width((wa + wb) / 2 * k + grow); c.set_line_cap(1); c.stroke()
        c.new_path(); c.arc(*T(*pts[-1]), (w1 * 0.55) * k + grow / 2, 0, 7); c.set_source_rgba(*col, al * a); c.fill()
    for col, al, grow, off in (((0.8, 0.87, 0.98), 0.55, 5.0, -3), ((0.05, 0.06, 0.09), 1.0, 0.0, 0)):
        c.save(); c.translate(0, off * k)
        limb(arm2, 16, 12, col, al, grow)
        poly(torso); c.set_source_rgba(*col, al * a); c.set_line_width(grow); c.fill_preserve(); c.stroke() if grow else c.new_path()
        poly(neck); c.set_source_rgba(*col, al * a); c.fill()
        hxx, hyy = T(160, 1); c.save(); c.translate(hxx, hyy); c.rotate(th); c.scale(1.12, 1.0); c.new_path(); c.arc(0, 0, 20 * k + grow / 2, 0, 7); c.restore()
        c.set_source_rgba(*col, al * a); c.fill()
        limb(arm1, 15, 10, col, al, grow)
        c.restore()
    for j in range(5):                                        # tissu qui claque
        ph = (t * 4 + j * 0.2) % 1; u = 20 + 18 * j
        x0, y0 = T(u, -22); x1, y1 = T(u - 30 - 30 * ph, -30 - 8 * math.sin(t * 30 + j))
        c.move_to(x0, y0); c.line_to(x1, y1); c.set_source_rgba(0.05, 0.06, 0.09, a * (1 - ph)); c.set_line_width(5 * k); c.stroke()
    for j in range(7):                                        # brume de décompression qui voile la silhouette
        ph = (t * 0.9 + j / 7) % 1
        x, y = T(20 + 260 * ph, -10 + 30 * math.sin(j * 2.1))
        glow(c, x, y, (40 + 60 * ph) * k, (0.95, 0.97, 1.0), 0.32 * (1 - ph) * a)


def buckle_macro(c, t, tens=1.0):
    """gros plan : boucle rotative du harnais, sangles tendues vers l'avant (le trou)."""
    c.set_source_rgb(0.05, 0.055, 0.07); c.paint()
    r = random.Random(2)
    for j in range(900):                                      # tissu du siège
        x, y = r.random() * W, r.random() * H; c.rectangle(x, y, 3, 3); c.set_source_rgba(0.2, 0.22, 0.28, 0.25); c.fill()
    glow(c, 540, 900, 700, (0.45, 0.55, 0.8), 0.22)
    jit = 3 * tens * math.sin(t * 47)
    cx, cy = 540 + jit, 900
    for ang, L in ((-2.35, 900), (-0.8, 900), (2.2, 900), (0.95, 900), (1.57, 900)):   # 5 sangles
        c.save(); c.translate(cx, cy); c.rotate(ang)
        c.rectangle(0, -62, L, 124); g = cairo.LinearGradient(0, -62, 0, 62); g.add_color_stop_rgb(0, 0.55, 0.45, 0.12); g.add_color_stop_rgb(0.5, 0.9, 0.75, 0.25); g.add_color_stop_rgb(1, 0.5, 0.4, 0.1)
        c.set_source(g); c.fill()
        for m in range(-50, 51, 10):
            c.move_to(0, m); c.line_to(L, m + 2 * math.sin(m)); c.set_source_rgba(0.3, 0.22, 0.05, 0.35); c.set_line_width(1.5); c.stroke()
        for m in (-50, 50):
            c.set_dash([12, 8]); c.move_to(160, m); c.line_to(L, m); c.set_source_rgba(1, 0.95, 0.7, 0.6); c.set_line_width(2.5); c.stroke(); c.set_dash([])
        c.restore()
    g = cairo.RadialGradient(cx - 50, cy - 60, 20, cx, cy, 200); g.add_color_stop_rgb(0, 0.95, 0.96, 1); g.add_color_stop_rgb(0.6, 0.55, 0.58, 0.65); g.add_color_stop_rgb(1, 0.25, 0.27, 0.32)
    c.new_path(); c.arc(cx, cy, 190, 0, 7); c.set_source(g); c.fill()
    c.new_path(); c.arc(cx, cy, 190, 0, 7); c.set_source_rgb(0.1, 0.1, 0.12); c.set_line_width(8); c.stroke()
    c.new_path(); c.arc(cx, cy, 120, 0, 7); c.set_source_rgb(0.32, 0.34, 0.4); c.fill()
    c.save(); c.translate(cx, cy); c.rotate(0.3)
    rr(c, -95, -26, 190, 52, 20); c.set_source_rgb(0.75, 0.15, 0.12); c.fill(); c.restore()
    glow(c, cx - 70, cy - 90, 90, (1, 1, 1), 0.35)
    for j in range(6):                                        # fibres tendues (traction vers l'avant / la droite)
        ph = (t * 3 + j / 6) % 1
        y = 620 + j * 70; c.move_to(780 + 160 * ph, y); c.line_to(860 + 160 * ph, y - 12); c.set_source_rgba(1, 1, 1, 0.45 * (1 - ph) * tens); c.set_line_width(3); c.stroke()


def nose_view(c, t, crack=0.0, hole=0.0, out=0.0, since_b=None, z=1.0, cx=440, cy=860, wind=0.0):
    alt_sky(c, t)
    _extra('u_noseR')
    bob = 4 * math.sin(t * 1.2)
    P = plane(c, 'u_noseR', cx, cy + bob, 1.0 * z, anchor='pc')
    poly = [P(n) for n in ('p1', 'p2', 'p3', 'p4', 'p5')]
    def pane():
        c.new_path(); c.move_to(*poly[0])
        for q in poly[1:]: c.line_to(*q)
        c.close_path()
    ox = poly[0][0] + 0.55 * (poly[2][0] - poly[0][0]); oy = poly[0][1] + 0.6 * (poly[3][1] - poly[0][1])
    if hole > 0:
        pane(); c.set_source_rgba(0.03, 0.035, 0.05, hole); c.fill()
        r = random.Random(4)                                   # quelques restes de verre déchiquetés, translucides
        pc = P('pc')
        for i in range(5):
            (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % 5]
            for j in range(2):
                u0 = r.uniform(0.0, 0.55); u1 = u0 + r.uniform(0.2, 0.4)
                um = r.uniform(u0 + 0.05, u1 - 0.05)
                mx_, my_ = x0 + (x1 - x0) * um, y0 + (y1 - y0) * um
                inx, iny = pc[0] - mx_, pc[1] - my_; dn = math.hypot(inx, iny) or 1; dep = r.uniform(10, 34) * z
                c.move_to(x0 + (x1 - x0) * u0, y0 + (y1 - y0) * u0); c.line_to(mx_ + inx / dn * dep, my_ + iny / dn * dep); c.line_to(x0 + (x1 - x0) * u1, y0 + (y1 - y0) * u1); c.close_path()
                c.set_source_rgba(0.7, 0.8, 0.9, 0.45 * hole); c.fill_preserve(); c.set_source_rgba(1, 1, 1, 0.6 * hole); c.set_line_width(1.2); c.stroke()
    elif crack > 0:
        c.save(); pane(); c.clip(); crack_web(c, ox, oy, 120 * z, crack); c.restore()
    if out > 0: half_out(c, ox - 18 * z, oy + 4 * z, z, t, out)
    if since_b is not None: burst(c, ox, oy, since_b, 1.1 * z)
    wind_lines(c, t, wind)
    return ox, oy


def cabin_masks(c, t, q, fog=0.0):
    """allée de la cabine vue de l'arrière : les masques à oxygène tombent rangée par rangée."""
    VX, VY, F = 540, 760, 520
    c.set_source_rgb(0.05, 0.06, 0.08); c.paint()
    def X(x, d): return VX + x * F / d
    def Y(h, d): return VY - h * F / d
    ds = [1.2 + 0.85 * i for i in range(13)]
    fl = 0.75 + 0.25 * (1 if (t * 7) % 1 < 0.8 else 0.3) if q > 0 else 1.0
    def quad(pts, col):
        c.new_path(); c.move_to(*pts[0])
        for p_ in pts[1:]: c.line_to(*p_)
        c.close_path(); c.set_source_rgb(*col); c.fill()
    dn, df = ds[0], ds[-1] + 1
    quad([(X(-1.0, dn), Y(0.95, dn)), (X(1.0, dn), Y(0.95, dn)), (X(1.0, df), Y(0.95, df)), (X(-1.0, df), Y(0.95, df))], tuple(v * fl for v in (0.78, 0.77, 0.74)))   # plafond
    quad([(X(-0.35, dn), Y(-1.2, dn)), (X(0.35, dn), Y(-1.2, dn)), (X(0.35, df), Y(-1.2, df)), (X(-0.35, df), Y(-1.2, df))], (0.1, 0.12, 0.25))                      # allée
    for sd in (-1, 1):
        quad([(X(sd * 1.0, dn), Y(0.95, dn)), (X(sd * 1.0, df), Y(0.95, df)), (X(sd * 1.75, df), Y(0.45, df)), (X(sd * 1.75, dn), Y(0.45, dn))], tuple(v * fl for v in (0.86, 0.85, 0.82)))   # coffres
        quad([(X(sd * 1.75, dn), Y(0.45, dn)), (X(sd * 1.75, df), Y(0.45, df)), (X(sd * 1.6, df), Y(0.38, df)), (X(sd * 1.6, dn), Y(0.38, dn))], tuple(v * fl for v in (0.55, 0.55, 0.55)))     # PSU
        quad([(X(sd * 1.85, dn), Y(0.38, dn)), (X(sd * 1.85, df), Y(0.38, df)), (X(sd * 1.85, df), Y(-1.2, df)), (X(sd * 1.85, dn), Y(-1.2, dn))], tuple(v * fl for v in (0.62, 0.62, 0.6)))   # paroi
    c.move_to(X(0, dn), Y(0.95, dn)); c.line_to(X(0, df), Y(0.95, df)); c.set_source_rgba(1, 0.97, 0.85, 0.6 * fl); c.set_line_width(10); c.stroke()
    for i in range(len(ds) - 1, -1, -1):
        d = ds[i]; sc = F / d
        for sd in (-1, 1):                                                                           # hublots
            wx = X(sd * 1.85, d + 0.4); rr(c, wx - 0.06 * sc, Y(0.25, d + 0.4), 0.12 * sc, 0.3 * sc, 0.05 * sc); c.set_source_rgba(0.75, 0.85, 1, 0.8 * fl); c.fill()
        for sd in (-1, 1):                                                                           # sièges (dos)
            for m in range(3):
                x0 = sd * (0.42 + 0.46 * m) - 0.2; x1 = x0 + 0.4
                rr(c, X(x0, d), Y(0.0, d), (x1 - x0) * sc, 1.0 * sc, 0.08 * sc); c.set_source_rgb(0.13, 0.17, 0.32); c.fill()
                rr(c, X(x0 + 0.04, d), Y(-0.02, d), (x1 - x0 - 0.08) * sc, 0.18 * sc, 0.05 * sc); c.set_source_rgb(0.85, 0.86, 0.88); c.fill()
                if (i * 3 + m + (sd > 0)) % 4 != 0:                                                  # têtes des passagers
                    c.new_path(); c.arc(X((x0 + x1) / 2, d + 0.1), Y(0.1, d + 0.1), 0.11 * F / (d + 0.1), 0, 7); c.set_source_rgb(0.07, 0.06, 0.06); c.fill()
        for sd in (-1, 1):                                                                           # masques
            for m in range(3):
                xm = sd * (0.62 + 0.42 * m)
                dl = q * 1.8 - i * 0.07
                if dl <= 0: continue
                L = 0.55 * min(1.0, dl / 0.35) * (1 + 0.12 * math.exp(-3 * max(0, dl - 0.35)) * math.sin(14 * (dl - 0.35)))
                sw = 0.03 * math.sin(t * 3 + i + m) * min(1, dl)
                tx, ty = X(xm, d), Y(0.4, d); bx, by = X(xm + sw, d), Y(0.4 - L, d)
                c.move_to(tx, ty); c.line_to(bx, by); c.set_source_rgba(0.9, 0.9, 0.95, 0.7); c.set_line_width(max(1, 0.012 * sc)); c.stroke()
                c.save(); c.translate(bx, by + 0.03 * sc); c.scale(1, 0.8); c.new_path(); c.arc(0, 0, 0.055 * sc, 0, 7); c.restore()
                c.set_source_rgb(1, 0.82, 0.12); c.fill()
    if fog > 0: c.set_source_rgba(0.92, 0.95, 1, 0.55 * fog); c.paint()
    g = cairo.RadialGradient(540, 860, 300, 540, 860, 1200); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.6); c.set_source(g); c.paint()


def windshield_xs(c, t, k):
    """coupe du pare-brise : verre double + intercalaire, film chauffant, joint abîmé, humidité, arc électrique, fissure."""
    c.set_source_rgb(0.02, 0.04, 0.08); c.paint()
    for j in range(0, W, 54): c.move_to(j, 0); c.line_to(j, H)
    for j in range(0, H, 54): c.move_to(0, j); c.line_to(W, j)
    c.set_source_rgba(0.3, 0.7, 1, 0.06); c.set_line_width(1); c.stroke()
    x0, y0, w = 230, 540, 720
    for j, (h, col, nm) in enumerate(((110, (0.55, 0.85, 1.0), "VERRE EXTÉRIEUR"), (44, (1, 0.8, 0.35), "FILM CHAUFFANT"), (140, (0.55, 0.85, 1.0), "VERRE INTÉRIEUR"))):
        yy = y0 + sum((110, 44, 140)[:j])
        rr(c, x0, yy, w, h, 6); c.set_source_rgba(*col, 0.22); c.fill_preserve(); c.set_source_rgba(*col, 0.9); c.set_line_width(3); c.stroke()
        letter(c, nm, x0 + w / 2 + 60, yy + h / 2 + 14, 40 if h > 50 else 34, col, 1)
    rr(c, x0 - 120, y0 - 14, 130, 322, 18); c.set_source_rgba(0.4, 0.4, 0.45, 1); c.fill()                # joint
    letter(c, "JOINT", x0 - 55, y0 - 30, 40, WH, 1)
    a1 = ap(k, 0.05, 0.3)
    c.move_to(x0 - 120, y0 + 70); c.line_to(x0 - 60, y0 + 100); c.line_to(x0 - 100, y0 + 150); c.line_to(x0 - 50, y0 + 190); c.set_source_rgba(*RED, a1); c.set_line_width(7); c.stroke()
    r = random.Random(3)
    for j in range(14):                                                                        # humidité qui s'infiltre
        ph = (t * 0.5 + j / 14) % 1
        px = x0 - 100 + 230 * ph * ap(k, 0.1, 0.4); py = y0 + 132 + 26 * math.sin(j)
        c.new_path(); c.arc(px, py, 8, 0, 7); c.set_source_rgba(0.4, 0.75, 1, 0.8 * a1 * (1 - ph * 0.5)); c.fill()
    a2 = ap(k, 0.35, 0.55)
    if a2 > 0:                                                                                  # arc électrique dans le film chauffant
        ax, ay = x0 + 150, y0 + 132
        for m in range(3):
            c.move_to(ax, ay)
            for q in range(7): c.line_to(ax + q * 14, ay + r.uniform(-14, 14))
            c.set_source_rgba(1, 0.95, 0.5, a2 * (0.6 + 0.4 * math.sin(t * 40 + m))); c.set_line_width(3); c.stroke()
        glow(c, ax + 50, ay, 90, (1, 0.8, 0.3), 0.6 * a2)
    a3 = ap(k, 0.6, 0.8)
    if a3 > 0:
        c.move_to(x0 + 230, y0); c.line_to(x0 + 270, y0 + 90); c.line_to(x0 + 245, y0 + 170); c.line_to(x0 + 290, y0 + 294)
        c.set_source_rgba(1, 1, 1, a3); c.set_line_width(4); c.stroke()
    for j, (s, col) in enumerate((("JOINT ABÎMÉ", RED), ("HUMIDITÉ", (0.5, 0.8, 1)), ("ARC ÉLECTRIQUE", YEL), ("VERRE FISSURÉ", WH))):
        a = ap(k, 0.1 + 0.2 * j, 0.22 + 0.2 * j)
        tag(c, s, 540, 960 + j * 88, col, a, 50)


def sc_sw_hook(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    tb = sg['sent'][0][0] + 0.7 * (sg['sent'][1][0] - sg['sent'][0][0])
    if k == 0:
        z = 1.0 + 0.12 * ap(t, sg['t0'], tb)
        nose_view(c, t, crack=ap(t, sg['t0'] + 0.3, tb - 0.1), hole=1.0 if t > tb else 0.0, since_b=(t - tb) if t > tb else None, z=z, wind=1.0 if t > tb else 0.0)
    elif k == 1:
        nose_view(c, t, hole=1.0, out=ap(p, 0.0, 0.3), since_b=t - tb, z=1.12, wind=1.0)
        tag(c, "ASPIRÉ À MOITIÉ DEHORS", 540, 1285, RED, ap(p, 0.2, 0.35), 56)
    else:
        alt_sky(c, t)
        plane(c, 'u_hero', 540, 900, 0.36)
        stamp(c, "SURVIVRAIS-TU ?", 540, 600, 130, RED, since, glow=1.0)


import pr.relief_sw as RLF
_REL = {}
def china_map(c, t, prog=1.0, labels=1.0):
    if 'img' not in _REL:
        import os
        if not os.path.exists('/home/claude/pr/topo_sw.png'): RLF.build_topo()
        _REL['img'] = cairo.ImageSurface.create_from_png('/home/claude/pr/topo_sw.png')
    c.set_source_rgb(0.025, 0.04, 0.065); c.paint(); glow(c, 400, 820, 700, (0.2, 0.35, 0.5), 0.18)
    for lo in range(90, 110, 2):
        x, _ = RLF.MAPXY(lo, 30); c.move_to(x, 0); c.line_to(x, H)
    for la in range(22, 40, 2):
        _, y = RLF.MAPXY(95, la); c.move_to(0, y); c.line_to(W, y)
    c.set_source_rgba(0.4, 0.7, 1, 0.06); c.set_line_width(1); c.stroke()
    c.set_source_surface(_REL['img'], 0, 0); c.paint()
    M = RLF.MAPXY
    for y0, y1 in ((0, 420), (H, 1250)):                       # fondus haut/bas (zones titre et sous-titres)
        g = cairo.LinearGradient(0, y0, 0, y1); g.add_color_stop_rgba(0, 0.02, 0.03, 0.04, 0.92); g.add_color_stop_rgba(1, 0.02, 0.03, 0.04, 0)
        c.rectangle(0, min(y0, y1), W, abs(y1 - y0)); c.set_source(g); c.fill()
    letter(c, "PLATEAU DU TIBET", *M(94.5, 33.0), 56, (1.0, 0.9, 0.75), 0.95 * labels)
    letter(c, "HIMALAYA", *M(91.5, 27.2), 36, (0.85, 0.85, 0.9), 0.75 * labels)
    pts = {'CHONGQING': (106.55, 29.56), 'CHENGDU': (104.07, 30.57), 'LHASSA': (91.11, 29.65)}
    x0, y0 = M(*pts['CHONGQING']); x1, y1 = M(*pts['LHASSA'])
    def route(u): return x0 + (x1 - x0) * u, y0 + (y1 - y0) * u - 110 * math.sin(math.pi * u)
    n = 80; m = int(n * prog)
    if m > 0:
        for lw, al in ((12, 0.18), (5, 0.95)):
            c.new_path(); c.move_to(x0, y0)
            for j in range(1, m + 1): c.line_to(*route(j / n))
            c.set_source_rgba(*YEL, al); c.set_line_width(lw); c.set_dash([16, 10] if lw == 5 else []); c.stroke(); c.set_dash([])
        hx, hy = route(m / n); glow(c, hx, hy, 50, YEL, 0.8); c.new_path(); c.arc(hx, hy, 9, 0, 7); c.set_source_rgb(1, 1, 1); c.fill()
    for nm, (lo, la) in pts.items():
        x, y = M(lo, la); glow(c, x, y, 40, (1, 1, 1), 0.5)
        c.new_path(); c.arc(x, y, 10, 0, 7); c.set_source_rgb(1, 1, 1); c.fill()
        dy = {'CHENGDU': -28, 'CHONGQING': 56, 'LHASSA': 56}[nm]
        letter(c, nm, x if nm != 'CHONGQING' else x - 20, y + dy, 42, WH, labels)


def sc_sw_real(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        alt_sky(c, t)
        plane(c, 'u_hero', 560, 980, 0.30, alpha=0.9)
        c.set_source_rgba(0.1, 0.06, 0.02, 0.25); c.paint()
        letter(c, "14 MAI 2018", 540, 600, 170, WH, ap(since, 0.0, 0.4))
        tag(c, "HISTOIRE VRAIE", 540, 690, YEL, ap(since, 0.3, 0.6), 56)
    else:
        china_map(c, t, prog=ap(p, 0.05, 0.8))
        tag(c, "128 PERSONNES À BORD", 540, 470, WH, ap(p, 0.1, 0.25), 54)
        tag(c, "AIRBUS A319", 540, 1240, (0.8, 0.85, 0.9), ap(p, 0.3, 0.45), 46)


def sc_sw_crack(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        nose_view(c, t, crack=ap(p, 0.5, 0.95), z=1.0 + 0.1 * ap(p, 0.0, 1.0), cx=470)
        panel(c, 330, 410, 420, 170, 0.5)
        counter(c, "9 800 M", "ALTITUDE DE CROISIÈRE", 540, 515, YEL, 110)
    else:
        nose_view(c, t, hole=1.0, since_b=since, z=1.12, cx=470, wind=1.0)
        stamp(c, "IL CÈDE", 540, 560, 150, RED, since, glow=1.0)


def cabin_alt(c, t, v, warn=0.0):
    c.set_source_rgb(0.04, 0.04, 0.05); c.paint()
    glow(c, 540, 860, 600, (0.4, 0.4, 0.5), 0.2)
    gauge(c, 540, 840, 280, v, 12000, (0, 2000, 4000, 6000, 8000, 10000, 12000), red_from=4300, col=WH, unit="M")
    letter(c, "ALTITUDE DANS LE COCKPIT", 540, 470, 52, WH)
    if warn > 0:
        on = (t * 3) % 1 < 0.55
        rr(c, 290, 1170, 500, 90, 18); c.set_source_rgba(*RED, (0.9 if on else 0.35) * warn); c.fill()
        letter(c, "CAB PR EXCESS ALT", 540, 1232, 48, WH, warn)


def sc_sw_decomp(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        q = ap(p, 0.15, 1.0)
        cabin_masks(c, t, q, fog=ap(p, 0.0, 0.12) * (1 - ap(p, 0.2, 0.9)))
        tag(c, "MASQUES À OXYGÈNE", 540, 1285, YEL, ap(p, 0.35, 0.5), 58)
    elif k == 1:
        nose_view(c, t, hole=1.0, out=ap(p, 0.0, 0.25), z=1.12, wind=1.0)
        tag(c, "À MOITIÉ HORS DE L'AVION", 540, 1285, RED, ap(p, 0.15, 0.3), 54)
    else:
        buckle_macro(c, t, 0.6 + 0.4 * math.sin(t * 9))
        stamp(c, "SA CEINTURE", 540, 1285, 120, YEL, since, glow=0.9)


def cockpit_chaos(c, t, a=1.0):
    c.set_source_rgb(0.03, 0.03, 0.05); c.paint()
    c.new_path(); c.move_to(80, 260); c.line_to(500, 300); c.line_to(480, 640); c.line_to(130, 600); c.close_path(); c.set_source_rgb(0.08, 0.1, 0.16); c.fill()   # vitre gauche
    c.new_path(); c.move_to(580, 300); c.line_to(1000, 260); c.line_to(950, 600); c.line_to(600, 640); c.close_path()
    g = cairo.LinearGradient(0, 260, 0, 640); g.add_color_stop_rgb(0, 0.2, 0.45, 0.85); g.add_color_stop_rgb(1, 0.75, 0.85, 0.95); c.set_source(g); c.fill()   # trou (ciel)
    c.new_path(); c.move_to(0, 680); c.curve_to(400, 620, 700, 620, W, 680); c.line_to(W, 900); c.line_to(0, 900); c.close_path(); c.set_source_rgb(0.1, 0.1, 0.12); c.fill()   # casquette
    r = random.Random(7)
    for j in range(36):                                                                      # objets aspirés vers le trou
        ph = (r.random() + t * r.uniform(0.4, 0.9)) % 1
        sx, sy = r.uniform(100, 980), r.uniform(900, 1400)
        tx, ty = 780 + r.uniform(-120, 120), 450 + r.uniform(-90, 90)
        x, y = sx + (tx - sx) * ph ** 1.5, sy + (ty - sy) * ph ** 1.5
        c.save(); c.translate(x, y); c.rotate(t * r.uniform(-8, 8) + j)
        rr(c, -22, -15, 44, 30, 3); c.set_source_rgba(0.92, 0.9, 0.85, a * (1 - ph * 0.7)); c.fill(); c.restore()
    for j in range(5):                                                                       # ondes sonores
        ph = (t * 1.6 + j / 5) % 1
        c.new_path(); c.arc(780, 450, 60 + 520 * ph, 0, 7); c.set_source_rgba(1, 1, 1, 0.35 * (1 - ph) * a); c.set_line_width(4); c.stroke()


def frost(c, t, f, seed=2):
    r = random.Random(seed)
    for j in range(int(220 * f)):
        side = j % 4; s_ = r.random(); d = r.random() ** 2 * 190
        x, y = ((s_ * W, d) if side == 0 else (s_ * W, H - d) if side == 1 else (d, s_ * H) if side == 2 else (W - d, s_ * H))
        c.save(); c.translate(x, y); c.rotate(r.random() * 3); sz = r.uniform(8, 22)
        for m in range(3): c.move_to(-sz, 0); c.line_to(sz, 0); c.rotate(1.047)
        c.set_source_rgba(0.85, 0.95, 1, 0.65); c.set_line_width(2); c.stroke(); c.restore()


def sc_sw_cold(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        nose_view(c, t, hole=1.0, out=1.0, z=1.12, wind=1.0)
        c.set_source_rgba(0.02, 0.06, 0.16, 0.62); c.paint()
        f = ap(p, 0.0, 1.0); frost(c, t, f)
        v = -40 * eout(ap(p, 0.0, 0.6))
        panel(c, 250, 760, 580, 300, 0.45)
        letter(c, f"{int(v)} °C", 540, 960, 230, (0.6, 0.9, 1.0))
        letter(c, "DEHORS, À 9 800 M", 540, 1035, 44, WH, ap(p, 0.2, 0.4), fam='Montserrat')
    else:
        ox, oy = nose_view(c, t, hole=1.0, out=1.0, z=1.12, wind=1.0)
        for j in range(5):                                                     # ondes sonores
            ph = (t * 1.4 + j / 5) % 1
            c.new_path(); c.arc(ox, oy, 60 + 700 * ph, 0, 7); c.set_source_rgba(1, 1, 1, 0.3 * (1 - ph)); c.set_line_width(5); c.stroke()
        r = random.Random(9)
        for j in range(34):                                                    # papiers et objets aspirés, emportés vers l'arrière
            ph = (t * r.uniform(0.5, 0.9) + r.random()) % 1
            x = ox - 40 - ph * r.uniform(500, 900); y = oy - 30 - ph * r.uniform(-60, 260) + 30 * math.sin(t * 5 + j)
            c.save(); c.translate(x, y); c.rotate(t * r.uniform(-9, 9) + j); w_ = r.uniform(16, 34)
            rr(c, -w_ / 2, -w_ * 0.35, w_, w_ * 0.7, 2); c.set_source_rgba(0.96, 0.95, 0.9, 0.95 * (1 - ph * 0.6)); c.fill(); c.restore()
        tag(c, "BRUIT ASSOURDISSANT", 540, 1285, ORG, ap(p, 0.1, 0.25), 56)


def pfd_simple(c, x, y, w, h, t, shake=0.0):
    def draw(dx, dy, a):
        c.save(); c.translate(x + dx, y + dy)
        rr(c, 0, 0, w, h, 16); c.clip()
        pitch = 6 * math.sin(t * 0.7); roll = 0.18 * math.sin(t * 0.9)
        c.save(); c.translate(w / 2, h / 2); c.rotate(roll); c.translate(0, pitch * 8)
        c.rectangle(-w, -h * 2, 2 * w, h * 2); c.set_source_rgba(0.2, 0.5, 0.95, a); c.fill()
        c.rectangle(-w, 0, 2 * w, h * 2); c.set_source_rgba(0.55, 0.36, 0.16, a); c.fill()
        c.move_to(-w, 0); c.line_to(w, 0); c.set_source_rgba(1, 1, 1, a); c.set_line_width(4); c.stroke()
        for j in (-2, -1, 1, 2):
            c.move_to(-50, -j * 80); c.line_to(50, -j * 80); c.set_source_rgba(1, 1, 1, a * 0.8); c.set_line_width(3); c.stroke()
        c.restore()
        c.move_to(w / 2 - 110, h / 2); c.line_to(w / 2 - 40, h / 2); c.move_to(w / 2 + 40, h / 2); c.line_to(w / 2 + 110, h / 2)
        c.set_source_rgba(1, 0.85, 0.2, a); c.set_line_width(10); c.stroke()
        c.restore()
    if shake > 0:
        for j in range(5):
            draw(math.sin(t * 60 + j * 1.3) * 22 * shake, math.cos(t * 47 + j) * 16 * shake, 0.28)
    else:
        draw(0, 0, 1.0)
    rr(c, x, y, w, h, 16); c.set_source_rgb(0.25, 0.26, 0.3); c.set_line_width(10); c.stroke()


def sc_sw_shake(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    c.set_source_rgb(0.03, 0.03, 0.04); c.paint()
    if k == 0:
        on = (t * 2.6) % 1 < 0.55
        rr(c, 240, 640, 600, 300, 30); c.set_source_rgb(0.1, 0.1, 0.12); c.fill()
        for j, nm in enumerate(("AP1", "AP2")):
            x = 380 + j * 320
            rr(c, x - 100, 720, 200, 140, 18); c.set_source_rgb(0.18, 0.18, 0.2); c.fill()
            letter(c, nm, x, 815, 70, (0.4, 0.4, 0.45))
        glow(c, 540, 1060, 520, RED, 0.35 if on else 0.08)
        rr(c, 330, 1000, 420, 120, 24); c.set_source_rgba(*RED, 0.95 if on else 0.3); c.fill()
        letter(c, "AP OFF", 540, 1085, 84, WH)
        tag(c, "PILOTE AUTOMATIQUE COUPÉ", 540, 520, RED, ap(p, 0.05, 0.2), 52)
    else:
        pfd_simple(c, 190, 480, 700, 700, t, shake=1.0)
        tag(c, "INSTRUMENTS ILLISIBLES", 540, 1285, ORG, ap(p, 0.1, 0.25), 56)


def sc_sw_manual(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    alt_sky(c, t, oy=-220 * p)
    plane(c, 'u_bank', 540, 860 + 60 * p, 0.34)
    alt = int(9800 - 3800 * ap(p, 0.0, 1.0)) // 100 * 100
    panel(c, 330, 410, 420, 170, 0.5)
    counter(c, f"{alt:,} M".replace(',', ' '), "DESCENTE", 540, 515, YEL, 110)
    tag(c, "PILOTAGE À LA MAIN", 540, 1285, WH, ap(p, 0.1, 0.25), 56)


def sc_sw_land(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        yc = runway_side(c, t, 900, ground_y=975)
        q = ap(p, 0.0, 0.8)
        P0 = plane(c, 'u_land', 0, 0, 0.30, alpha=0.0); gx, gy = P0('lgear')
        plane(c, 'u_land', 560 - gx, yc - gy - 120 * (1 - q), 0.30, shadow=yc + 6)
        tag(c, "CHENGDU", 540, 470, GRN, ap(p, 0.1, 0.25), 60)
    else:
        yc = runway_side(c, 0, 0, ground_y=975)
        P0 = plane(c, 'u_land', 0, 0, 0.30, alpha=0.0); gx, gy = P0('lgear')
        plane(c, 'u_land', 560 - gx, yc - gy, 0.30, shadow=yc + 6)
        for j, x in enumerate((180, 900)):
            on = (t * 2 + j * 0.5) % 1 < 0.5
            glow(c, x, yc - 30, 90, (0.3, 0.5, 1) if on else (1, 0.2, 0.2), 0.6)
        panel(c, 160, 420, 760, 230, 0.6)
        letter(c, "COPILOTE", 540, 490, 44, (0.8, 0.85, 0.9), 1, fam='Montserrat')
        letter(c, "ÉGRATIGNURES + POIGNET FOULÉ", 540, 580, 62, WH, ap(p, 0.2, 0.4))
        check(c, 860, 1200, 1.4, GRN, ap(p, 0.5, 0.65))


def sc_sw_verdict(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        alt_sky(c, t)
        plane(c, 'u_hero', 540, 980, 0.32)
        stamp(c, "128 / 128", 540, 620, 170, GRN, since - 0.15, glow=1.0)
        letter(c, "SURVIVANTS", 540, 700, 54, WH, ap(p, 0.25, 0.4))
    elif k == 1:
        windshield_xs(c, t, ap(p, 0.0, 0.95))
        letter(c, "LA CAUSE", 540, 470, 64, WH)
    else:
        alt_sky(c, t)
        lt2 = t - sg['sent'][2][0]
        plane(c, 'u_hero', 540 + 10 * lt2, 900 - 6 * lt2, max(0.2, 0.36 - 0.01 * lt2))
        stamp(c, "ET TOI ?", 540, 600, 160, ORG, since, glow=1.0)


# =============================================================== TU ES LE PILOTE — ÉPISODE 4 (e4_*)
def night_sea(c, t, horizon=1060):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, 0.02, 0.03, 0.08); g.add_color_stop_rgb(horizon / H - 0.001, 0.08, 0.10, 0.22)
    g.add_color_stop_rgb(horizon / H, 0.03, 0.05, 0.10); g.add_color_stop_rgb(1, 0.01, 0.02, 0.04); c.set_source(g); c.paint()
    r = random.Random(5)
    for _ in range(240):
        c.new_path(); c.arc(r.random() * W, r.random() * (horizon - 60), r.choice((1, 1, 1.5, 2.4)), 0, 7); c.set_source_rgba(1, 1, 1, (0.3 + 0.6 * r.random()) * (0.75 + 0.25 * math.sin(t * 2 + r.random() * 9))); c.fill()
    mx, my = 930, 170
    radial(c, mx, my, 200, (1, 0.95, 0.8), 0.18); c.new_path(); c.arc(mx, my, 52, 0, 7); c.set_source_rgb(0.98, 0.96, 0.88); c.fill()
    c.new_path(); c.arc(mx + 24, my - 12, 47, 0, 7); c.set_source_rgb(0.03, 0.04, 0.09); c.fill()
    for k in range(18):
        y = horizon + 20 + k * 38; w = 150 - k * 6
        rr(c, mx - 40 - w / 2 + 25 * math.sin(t * 1.5 + k), y, max(10, w), 6, 3); c.set_source_rgba(1, 0.95, 0.8, max(0, 0.22 - k * 0.011)); c.fill()
    for k in range(40):
        y = horizon + 10 + r.random() * (H - horizon); x = (r.random() * W - t * 40 * (1 + y / H)) % W
        c.move_to(x, y); c.line_to(x + 40 + r.random() * 80, y); c.set_source_rgba(0.5, 0.6, 0.8, 0.12); c.set_line_width(3); c.stroke()


def beach_far(c, t, horizon=1060, x0=600, people=1.0, run=0.0):
    """bande de plage à droite de l'horizon, feu de camp et silhouettes."""
    c.new_path(); c.move_to(x0, horizon); c.curve_to(x0 + 120, horizon - 10, W, horizon - 16, W + 10, horizon - 16); c.line_to(W + 10, horizon + 60)
    c.line_to(x0 - 40, horizon + 60); c.close_path(); c.set_source_rgb(0.4, 0.36, 0.28); c.fill()
    fx = x0 + 200
    R.flames(c, fx, horizon - 4, 0.28, t, 1.0); radial(c, fx, horizon - 10, 160, (1, 0.55, 0.2), 0.35)
    for j, dx in enumerate((-60, -34, 36, 62)):
        x = fx + dx - run * (120 + 40 * j); y = horizon - 2; sw = math.sin(t * 9 + j) * 8 * run
        c.move_to(x, y); c.line_to(x - 7 + sw, y + 20); c.move_to(x, y); c.line_to(x + 7 - sw, y + 20); c.move_to(x, y); c.line_to(x, y - 24)
        c.move_to(x, y - 18); c.line_to(x - 11, y - 36 - 6 * math.sin(t * 6 + j)); c.move_to(x, y - 18); c.line_to(x + 11, y - 36)
        c.set_source_rgba(*INK, people); c.set_line_width(5); c.set_line_cap(1); c.stroke()
        c.new_path(); c.arc(x, y - 32, 8, 0, 7); c.set_source_rgba(0.95, 0.75, 0.5, people); c.fill()
        if run > 0:
            c.move_to(x - 4, y - 28); c.line_to(x - 140, y + 10); c.set_source_rgba(1, 0.95, 0.7, 0.25 * people); c.set_line_width(14); c.stroke()


def spray(c, x, y, t, k, s=1.0, seed=1):
    r = random.Random(seed)
    for j in range(60):
        a = r.uniform(-3.0, -0.15); d = (20 + 260 * k * r.uniform(0.3, 1.0)) * s
        px, py = x + math.cos(a) * d * 1.3, y + math.sin(a) * d * (0.6 + 0.6 * r.random()) + 80 * k * k * s
        c.new_path(); c.arc(px, py, (4 + 12 * r.random()) * s, 0, 7); c.set_source_rgba(0.85, 0.92, 1, 0.75 * (1 - k * 0.6)); c.fill()


def sc_e4_recap(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        night_sea(c, t)
        twin(c, 540, 760 + 6 * math.sin(t * 1.3), 0.04, 0, 1.0, prop=0.0, gear=1, flaps=1)
        stamp(c, "ÉPISODE 4", 540, 520, 150, WH, since, glow=0.6)
        stamp(c, "FINAL", 540, 1290, 140, ORG, since - 0.3, glow=1.0)
    elif k == 1:
        pov_beach(c, t, light=1.0, people=1.0, fire=1.0, zoom=1.35)
        c.new_path(); c.arc(540 + 22 * 1.35, 900 + 135 * 1.35, 150 + 6 * math.sin(t * 8), 0, 7); c.set_source_rgb(*RED); c.set_line_width(9); c.stroke()
    else:
        c.set_source_rgb(0.02, 0.03, 0.06); c.paint(); radial(c, 540, 900, 700, BLUE, 0.15)
        V = getattr(R.CFG, 'VOTES', dict(A=0, B=0, src="VOTES"))
        tot = max(1, V['A'] + V['B'])
        label(c, V.get('src', 'VOTES'), 540, 560, 46, (0.85, 0.88, 0.95))
        for j, (lab, txt, col) in enumerate((("A", "L'EAU", BLUE), ("B", "AU-DESSUS", ORG))):
            y = 700 + j * 260; v = V[lab]; q = ap(p, 0.05 + 0.1 * j, 0.4 + 0.1 * j); w = 600 * v / tot * q
            text(c, lab, 150, y + 95, 150, col, glow=0.6)
            rr(c, 240, y, 620, 120, 30); c.set_source_rgba(1, 1, 1, 0.08); c.fill()
            if w > 1: rr(c, 250, y + 10, max(40, w), 100, 24); c.set_source_rgb(*col); c.fill()
            label(c, txt, 550, y + 80, 52, WH, 1, 'Bebas Neue')
            text(c, str(int(round(v * q))), 940, y + 90, 110, col)
        if p > 0.6:
            q = since - 0.6 * (sg['end'] - sg['sent'][2][0])
            rr(c, 100, 680, 880, 160, 36); c.set_source_rgb(*GRN); c.set_line_width(8); c.stroke()
            stamp(c, "A : L'EAU", 540, 1290, 140, GRN, q, glow=1.0)


def sc_e4_gear(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        if p < 0.45:
            night_sea(c, t)
            g = 1 - ap(p, 0.05, 0.4)
            twin(c, 540, 760, 0.02, 0, 1.3, prop=0.0, gear=g, flaps=1)
            tag(c, "TRAIN RENTRÉ", 540, 1285, YEL, ap(p, 0.2, 0.35), 64)
        else:
            c.set_source_rgb(0.02, 0.03, 0.06); c.paint()
            for j, (cx, ok) in enumerate(((290, False), (790, True))):
                x0, y0, w, h = cx - 230, 560, 460, 520
                c.save(); rr(c, x0, y0, w, h, 40); c.clip()
                c.set_source_rgb(0.04, 0.07, 0.15); c.paint()
                c.rectangle(x0, y0 + h * 0.6, w, h); c.set_source_rgb(0.08, 0.2, 0.38); c.fill()
                q = ap(p, 0.5, 0.95)
                if not ok:
                    twin(c, cx - 40 + 60 * q, y0 + h * 0.52 + 20 * q, -2.6 * q * q, 0, 0.42, prop=0, gear=1, flaps=1)
                    spray(c, cx, y0 + h * 0.6, t, q, 0.5, seed=4)
                else:
                    twin(c, cx - 80 + 120 * q, y0 + h * 0.56, 0.0, 0, 0.42, prop=0, gear=0, flaps=1)
                    for m in range(6): c.move_to(cx - 160 + m * 20, y0 + h * 0.6 + 4); c.line_to(cx - 200 + m * 20, y0 + h * 0.6 + 4)
                    c.set_source_rgba(1, 1, 1, 0.5); c.set_line_width(3); c.stroke()
                c.restore()
                rr(c, x0, y0, w, h, 40); c.set_source_rgb(*(GRN if ok else RED)); c.set_line_width(7); c.stroke()
                label(c, "TRAIN RENTRÉ" if ok else "TRAIN SORTI", cx, y0 - 30, 48, GRN if ok else RED, 1, 'Bebas Neue')
                (check if ok else cross)(c, cx, y0 + h + 80, 1.3, GRN if ok else RED, ap(p, 0.75, 0.9))
            tag(c, "IL CAPOTE", 290, 1285, RED, ap(p, 0.7, 0.85), 48)
    else:
        c.set_source_rgb(0.05, 0.05, 0.07); c.paint(); radial(c, 540, 860, 600, (0.4, 0.5, 0.8), 0.15)
        rr(c, 260, 450, 560, 820, 40); fill_stroke(c, (0.82, 0.83, 0.88), 9)
        rr(c, 330, 520, 420, 260, 30); fill_stroke(c, (0.2, 0.3, 0.45), 7)
        a = -0.9 * ap(p, 0.1, 0.4)
        c.save(); c.translate(700, 900); c.rotate(a); rr(c, -20, -20, 150, 40, 18); fill_stroke(c, (0.35, 0.36, 0.4), 6); c.restore()
        c.new_path(); c.arc(700, 900, 26, 0, 7); fill_stroke(c, (0.25, 0.26, 0.3), 6)
        if p > 0.4:
            c.new_path(); c.arc(700, 900, 120, -1.2, 0.0); c.set_source_rgba(*GRN, 0.9); c.set_line_width(7); c.stroke()
        tag(c, "PORTE DÉVERROUILLÉE", 540, 1285 + 10, GRN, ap(p, 0.35, 0.5), 56)


def sc_e4_flare(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    night_sea(c, t, horizon=1000)
    beach_far(c, t, horizon=1000, x0=640)
    if k == 0:
        x = 300 + 160 * p
        twin(c, x, 900 + 4 * math.sin(t * 3), 0.0, 0, 1.0, prop=0, gear=0, flaps=1)
        for j in range(5):
            ph = (t * 0.8 + j / 5) % 1
            c.move_to(0, 1060 + j * 30); c.curve_to(300, 1050 + j * 30 - 10 * math.sin(ph * 6), 700, 1070 + j * 30, W, 1060 + j * 30)
            c.set_source_rgba(1, 1, 1, 0.12); c.set_line_width(3); c.stroke()
        tag(c, "AU RAS DES VAGUES", 540, 1285, BLUE, ap(p, 0.1, 0.25), 60)
    else:
        q = ap(p, 0.0, 0.8)
        twin(c, 520, 900 + 30 * q, -0.14 * q, 0, 1.25, prop=0, gear=0, flaps=1)
        v = int(150 - 40 * q)
        gauge(c, 840, 520, 120, v, 250, (0, 50, 100, 150, 200, 250), red_from=100, col=WH, unit="KM/H")
        tag(c, "LE PLUS LENT POSSIBLE", 540, 1285, YEL, ap(p, 0.15, 0.3), 58)


def sc_e4_touch(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k <= 1:
        night_sea(c, t, horizon=1000)
        beach_far(c, t, horizon=1000, x0=640)
        if k == 0:
            twin(c, 520, 935, -0.12, 0, 1.25, prop=0, gear=0, flaps=1)
            spray(c, 520 - 200, 980, t, ap(p, 0.0, 0.9), 0.9)
        else:
            twin(c, 520 + 30 * p, 950, 0.04 * p, 0, 1.25, prop=0, gear=0, flaps=1)
            spray(c, 560, 990, t, 0.4 + 0.6 * ap(p, 0, 1), 1.6, seed=7)
            stamp(c, "COMME UN MUR", 540, 1250, 120, WH, since, glow=0.8)
    else:
        sky(c, (0.04, 0.05, 0.10), (0.01, 0.01, 0.03)); radial(c, 540, 1200, 500, YEL, 0.08)
        jolt = 40 * math.exp(-since * 3) * math.sin(since * 14)
        pilot_body(c, W / 2 + jolt, 1270, 1.0)
        for sx in (-1, 1):
            c.move_to(W / 2 + sx * 52 + jolt, 1282); c.line_to(W / 2 - sx * 26 + jolt, 1440); c.set_source_rgb(1, 0.8, 0.2); c.set_line_width(20); c.set_line_cap(1); c.stroke()
        rr(c, W / 2 - 26 + jolt, 1388, 52, 40, 8); fill_stroke(c, (0.75, 0.77, 0.82), 5)
        R.eyes_head(c, W / 2 + jolt, 1180, 115, 'worried', (0, -6), t)
        stamp(c, "TA CEINTURE", 540, 640, 130, YEL, since, glow=0.9)


def sc_e4_stop(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    night_sea(c, t, horizon=1000)
    beach_far(c, t, horizon=1000, x0=640)
    if k == 0:
        q = eout(ap(p, 0.0, 1.0))
        x = 160 + 260 * q
        c.save(); c.rectangle(0, 0, W, 1000 + 18); c.clip()
        twin(c, x, 992, 0.03, 0, 0.9, prop=0, gear=0, flaps=1)
        c.restore()
        for j in range(4):
            c.move_to(x - 220 - j * 40, 1004 + j * 6); c.line_to(x - 120 - j * 30, 1000 + j * 4); c.set_source_rgba(1, 1, 1, 0.5 * (1 - q)); c.set_line_width(4); c.stroke()
        d = int(120 - 80 * q)
        c.move_to(x + 220, 940); c.line_to(840, 940); c.set_source_rgba(1, 1, 1, 0.7); c.set_dash([10, 8]); c.set_line_width(4); c.stroke(); c.set_dash([])
        label(c, f"≈ {d} M", (x + 220 + 840) / 2, 915, 50, WH, 1, 'Bebas Neue')
    else:
        c.save(); c.rectangle(0, 0, W, 1018); c.clip()
        twin(c, 420, 992 + 4 * math.sin(t * 1.5), 0.03, 0, 0.9, prop=0, gear=0, flaps=1)
        c.restore()
        check(c, 540, 600, 2.2, GRN, ap(p, 0.1, 0.3))
        tag(c, "PAS RETOURNÉ", 540, 1285, GRN, ap(p, 0.2, 0.35), 60)


def sc_e4_out(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    night_sea(c, t, horizon=900)
    beach_far(c, t, horizon=900, x0=560, run=0.0 if k == 0 else ap(p, 0.0, 1.0))
    WL = 1130                                                   # surface de l'eau au premier plan
    c.save(); c.rectangle(0, 0, W, WL + 12); c.clip()
    twin(c, 330, WL - 10, 0.03, 0, 1.05, prop=0, gear=0, flaps=1)
    c.restore()
    q = ap(p, 0.1, 0.8) if k == 0 else 1.0
    px = 640 + 150 * q; hip = WL + 10; s = 2.0; wave = 6 * math.sin(t * 3)
    def body(col, lw):
        c.move_to(px, hip); c.line_to(px, hip - 70 * s)
        c.move_to(px, hip - 52 * s); c.line_to(px - 34 * s, hip - 14 * s + 10 * math.sin(t * 5))
        if k == 1: c.move_to(px, hip - 52 * s); c.line_to(px + 30 * s, hip - 100 * s + 8 * math.sin(t * 9))
        else: c.move_to(px, hip - 52 * s); c.line_to(px + 36 * s, hip - 16 * s)
        c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1); c.stroke()
    radial(c, px, hip - 80, 220, (1, 0.9, 0.7), 0.12)
    body((0.82, 0.84, 0.9), 22); body(INK, 13)
    R.eyes_head(c, px, hip - 70 * s - 44, 50, 'determined' if k == 0 else 'happy', (12, -4), t)
    c.rectangle(0, WL + wave * 0.3, W, H - WL); c.set_source_rgba(0.03, 0.08, 0.18, 0.88); c.fill()   # eau qui cache le bas du corps
    for j in range(5):
        ph = (t * 0.6 + j / 5) % 1; y = WL + 4 + 60 * ph
        c.move_to(0, y); c.curve_to(300, y - 8, 700, y + 8, W, y); c.set_source_rgba(1, 1, 1, 0.25 * (1 - ph)); c.set_line_width(3); c.stroke()
    c.new_path(); c.save(); c.translate(px, WL + 6); c.scale(1, 0.25); c.arc(0, 0, 70 + 10 * math.sin(t * 4), 0, 7); c.restore()
    c.set_source_rgba(1, 1, 1, 0.4); c.set_line_width(3); c.stroke()
    if k == 0: tag(c, "DE L'EAU JUSQU'À LA TAILLE", 540, 1285, BLUE, ap(p, 0.2, 0.35), 54)
    else: tag(c, "ILS ACCOURENT", 540, 1285, ORG, ap(p, 0.1, 0.25), 60)


EPS = [("1", "FEU MOTEUR"), ("2", "PLUS DE CARBURANT"), ("3", "LA PLAGE"), ("4", "L'EAU")]
def sc_e4_end(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        sky(c, (0.15, 0.12, 0.3), (0.95, 0.55, 0.35)); radial(c, 760, 1000, 420, (1, 0.75, 0.45), 0.6)
        c.rectangle(0, 1000, W, H); c.set_source_rgb(0.1, 0.16, 0.28); c.fill()
        c.save(); c.rectangle(0, 0, W, 1018); c.clip(); twin(c, 380, 992, 0.03, 0, 0.9, prop=0, gear=0, flaps=1); c.restore()
        stamp(c, "TU AS SURVÉCU", 540, 640, 130, GRN, since, glow=1.0)
        tag(c, "0 BLESSÉ", 540, 1285, WH, ap(p, 0.3, 0.45), 64)
    else:
        c.set_source_rgb(0.03, 0.04, 0.08); c.paint(); radial(c, 540, 860, 700, BLUE, 0.15)
        letter(c, "TU ES LE PILOTE", 540, 470, 90, WH)
        for j, (n, nm) in enumerate(EPS):
            a = ap(t, sg['sent'][1][0] + 0.15 * j, sg['sent'][1][0] + 0.15 * j + 0.3) if k >= 1 else 0
            y = 580 + j * 150
            rr(c, 130, y, 820, 120, 30); c.set_source_rgba(1, 1, 1, 0.07 * a); c.fill_preserve(); c.set_source_rgba(*(GRN if j == 3 else BLUE), a); c.set_line_width(4); c.stroke()
            letter(c, f"ÉPISODE {n}", 270, y + 78, 50, (0.75, 0.8, 0.9), a)
            letter(c, nm, 640, y + 78, 56, WH, a)
            check(c, 885, y + 60, 0.7, GRN, a)
        if k == 2: stamp(c, "MERCI !", 540, 1285, 140, ORG, since, glow=1.0)
        if k == 3:
            q = t - sg['sent'][3][0]
            stamp(c, "ET TOI ?", 540, 1285, 140, ORG, q, glow=1.0)


SC11 = {k[3:]: v for k, v in globals().items() if k.startswith('sc_') and callable(v)}
