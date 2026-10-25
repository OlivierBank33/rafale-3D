"""Scènes v3 « cinéma » pour le Rio-Paris AF447 (af_*) : globe de nuit, A330 détaillé, orage à cristaux, zoom sur la sonde Pitot,
PFD réaliste, manche latéral, visualisation de l'écoulement sur l'aile (décrochage), trajectoire reconstituée d'après le BEA,
plongée abyssale + sonar, hommage (228 lumières). R = module sm_render injecté."""
import cairo, math, random
from sm_lib import *
from sm_scenes2 import ease, ap, sky, ORG, BLUE, RED, WH, GRN
from sm_scenes6 import si, stamp, speedlines, eout, back, YEL
from sm_scenes7 import tag, label, mix, check, cross, clock
R = None
AMB = (1.0, 0.75, 0.2)
CY = (0.2, 0.95, 1.0)
MAG = (1.0, 0.35, 0.9)


# ------------------------------------------------------------------ décors
def night_sky(c, t, top=(0.01, 0.02, 0.06), bot=(0.05, 0.08, 0.2), stars=1.0, moon=True):
    sky(c, top, bot)
    r = random.Random(1)
    for _ in range(220):
        x = r.random() * W; y = r.random() * H * 0.7; tw = 0.6 + 0.4 * math.sin(t * (1 + r.random() * 2) + r.random() * 9)
        c.new_path(); c.arc(x, y, r.choice((0.8, 1.2, 1.8, 2.5)), 0, 7); c.set_source_rgba(1, 1, 1, stars * tw * (0.25 + 0.6 * r.random())); c.fill()
    if moon:
        radial(c, 830, 300, 330, (0.85, 0.9, 1.0), 0.18); c.new_path(); c.arc(830, 300, 62, 0, 7); c.set_source_rgb(0.95, 0.96, 1.0); c.fill()


def cloud_sea(c, t, y0=1180, a=1.0, speed=60, col=(0.16, 0.2, 0.34), lit=(0.45, 0.5, 0.7)):
    """Mer de nuages éclairée par la lune, défilement lent."""
    r = random.Random(7)
    for layer in range(3):
        yy = y0 + layer * 120; sp = speed * (0.5 + layer * 0.5); k = 0.8 + layer * 0.35
        for j in range(14):
            x = (j * 110 + r.random() * 60 - t * sp) % (W + 300) - 150
            rad = (70 + 50 * r.random()) * k
            c.new_path(); c.arc(x, yy + 20 * r.random(), rad, 0, 7)
            g = cairo.RadialGradient(x - rad * 0.3, yy - rad * 0.5, rad * 0.1, x, yy, rad)
            g.add_color_stop_rgba(0, *mix(col, lit, 0.7 - 0.2 * layer), a); g.add_color_stop_rgba(1, *col, a)
            c.set_source(g); c.fill()
    c.new_path(); c.rectangle(0, y0 + 300, W, H); c.set_source_rgba(*col, a); c.fill()


def ocean_night(c, t, horizon=1050, calm=0.0):
    night_sky(c, t)
    g = cairo.LinearGradient(0, horizon, 0, H); g.add_color_stop_rgb(0, 0.04, 0.07, 0.15); g.add_color_stop_rgb(1, 0.0, 0.01, 0.03)
    c.rectangle(0, horizon, W, H - horizon); c.set_source(g); c.fill()
    for k in range(22):
        y = horizon + 10 + k * k * 1.9; w = 150 - k * 5
        rr(c, 830 - w / 2 + 25 * math.sin(t * 1.3 + k) * (1 - calm), y, max(8, w), 4 + k * 0.3, 2); c.set_source_rgba(0.9, 0.93, 1, max(0, 0.3 - k * 0.012)); c.fill()
    r = random.Random(3)
    for _ in range(50):
        y = horizon + 10 + r.random() ** 1.5 * (H - horizon); x = (r.random() * W - t * 25 * (1 + y / H)) % W
        c.move_to(x, y); c.line_to(x + 40 + 60 * (y - horizon) / (H - horizon), y); c.set_source_rgba(0.5, 0.6, 0.85, 0.12 * (1 - calm)); c.set_line_width(2 + 3 * (y - horizon) / (H - horizon)); c.stroke()


# ------------------------------------------------------------------ A330
def a330(c, x, y, rot, s, t, lights=True, lit=0.0, wing_glow=0.0, eng_glow=0.0):
    """A330-200 de profil (nez à droite), livrée blanche, empennage aux trois bandes, feux de navigation et anticollision."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    body = (0.93, 0.94, 0.97)
    # aile lointaine + moteur lointain
    c.new_path(); c.move_to(-20, 6); c.line_to(70, 6); c.line_to(-40, -60); c.line_to(-85, -60); c.close_path(); c.set_source_rgb(0.55, 0.58, 0.66); c.fill()
    rr(c, 10, -34, 70, 26, 12); c.set_source_rgb(0.5, 0.53, 0.6); c.fill()
    # empennage horizontal lointain
    c.new_path(); c.move_to(-235, -6); c.line_to(-300, -40); c.line_to(-280, -40); c.line_to(-215, -10); c.close_path(); c.set_source_rgb(0.6, 0.62, 0.7); c.fill()
    # fuselage
    c.new_path(); c.move_to(-300, -14); c.curve_to(-200, -34, 200, -36, 270, -24); c.curve_to(305, -16, 318, 4, 300, 18); c.curve_to(250, 34, 120, 36, -230, 28)
    c.curve_to(-270, 24, -300, 10, -320, -2); c.close_path()
    g = cairo.LinearGradient(0, -36, 0, 36); g.add_color_stop_rgb(0, 1, 1, 1); g.add_color_stop_rgb(0.55, *body); g.add_color_stop_rgb(1, 0.62, 0.65, 0.73)
    c.set_source(g); c.fill_preserve(); c.save(); c.clip_preserve()
    if lit > 0: c.set_source_rgba(1, 1, 1, 0.5 * lit); c.paint()
    c.restore(); c.set_source_rgb(*INK); c.set_line_width(8); c.set_line_join(1); c.stroke()
    for i in range(22):                                   # hublots
        rr(c, -210 + i * 20, -12, 9, 11, 4); c.set_source_rgb(1, 0.86, 0.55); c.fill()
    c.new_path(); c.move_to(262, -22); c.curve_to(278, -24, 292, -16, 298, -8); c.line_to(268, -8); c.close_path(); c.set_source_rgb(0.15, 0.2, 0.3); c.fill()   # pare-brise
    for x0 in (272, 284): c.move_to(x0, -21); c.line_to(x0 + 2, -8)
    c.set_source_rgb(*INK); c.set_line_width(3); c.stroke()
    c.new_path(); c.arc(285, 6, 3, 0, 7); c.set_source_rgb(0.75, 0.78, 0.82); c.fill()   # sonde Pitot (repère)
    # dérive aux trois bandes
    c.new_path(); c.move_to(-230, -24); c.line_to(-300, -165); c.line_to(-255, -165); c.line_to(-165, -30); c.close_path()
    c.set_source_rgb(0.98, 0.98, 1); c.fill_preserve(); c.save(); c.clip()
    for k, col in enumerate(((0.05, 0.15, 0.45), (0.98, 0.98, 1), (0.85, 0.12, 0.15))):
        c.new_path(); c.move_to(-320 + k * 30, -175); c.line_to(-290 + k * 30, -175); c.line_to(-200 + k * 30, -10); c.line_to(-230 + k * 30, -10); c.close_path(); c.set_source_rgb(*col); c.fill()
    c.restore(); c.new_path(); c.move_to(-230, -24); c.line_to(-300, -165); c.line_to(-255, -165); c.line_to(-165, -30); c.close_path(); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    # empennage horizontal proche
    c.new_path(); c.move_to(-240, 8); c.line_to(-312, 30); c.line_to(-295, 38); c.line_to(-215, 20); c.close_path(); fill_stroke(c, (0.82, 0.84, 0.9), 6)
    # aile proche
    c.new_path(); c.move_to(-60, 18); c.line_to(90, 18); c.line_to(-30, 100); c.line_to(-110, 100); c.close_path()
    g = cairo.LinearGradient(0, 18, 0, 100); g.add_color_stop_rgb(0, 0.86, 0.88, 0.93); g.add_color_stop_rgb(1, 0.66, 0.69, 0.76); c.set_source(g); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    c.new_path(); c.move_to(-110, 100); c.line_to(-118, 82); c.line_to(-102, 82); c.close_path(); fill_stroke(c, (0.82, 0.84, 0.9), 4)   # winglet
    if wing_glow > 0:
        c.new_path(); c.move_to(-60, 18); c.line_to(90, 18); c.line_to(-30, 100); c.line_to(-110, 100); c.close_path(); c.set_source_rgba(*GRN, 0.9 * wing_glow); c.set_line_width(10); c.stroke()
    # moteur proche (gros double flux)
    rr(c, 20, 46, 110, 48, 22); g = cairo.LinearGradient(0, 46, 0, 94); g.add_color_stop_rgb(0, 0.92, 0.93, 0.96); g.add_color_stop_rgb(1, 0.55, 0.58, 0.66); c.set_source(g); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    c.new_path(); c.save(); c.translate(130, 70); c.scale(0.35, 1); c.arc(0, 0, 22, 0, 7); c.restore(); c.set_source_rgb(0.08, 0.08, 0.1); c.fill()
    c.move_to(40, 46); c.line_to(20, 30); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    if eng_glow > 0:
        for ex, ey, rr_ in ((75, 70, 70), (45, -21, 45)):
            c.new_path(); c.arc(ex, ey, rr_, 0, 7); c.set_source_rgba(*GRN, 0.9 * eng_glow); c.set_line_width(8); c.stroke()
    radial(c, 10, 70, 60, (1, 0.6, 0.3), 0.25)
    if lights:                                              # feux
        bl = (t * 1.1) % 1 < 0.08
        if bl:
            for lx, ly in ((-20, -34), (-20, 34)): radial(c, lx, ly, 30, (1, 0.15, 0.1), 0.7); c.new_path(); c.arc(lx, ly, 5, 0, 7); c.set_source_rgb(1, 0.3, 0.2); c.fill()
        st = (t * 1.1 + 0.5) % 1 < 0.05
        if st: radial(c, -115, 92, 90, (1, 1, 1), 1.0); radial(c, -320, -2, 60, (1, 1, 1), 0.8)
        radial(c, -110, 96, 30, (0.2, 1, 0.4), 0.8)
    c.restore()


def stick_head(c, x, y, r, t, mood='worried', look=(0, 0), cap=False, headset=True, rim=None):
    head(c, x, y, r, mood, look, helmet=False, rim=rim)
    if headset:
        c.new_path(); c.arc(x, y - r * 0.1, r * 1.08, math.pi * 1.05, math.pi * 1.95); c.set_source_rgb(0.12, 0.12, 0.14); c.set_line_width(r * 0.12); c.stroke()
        for sx in (-1, 1): rr(c, x + sx * r * 1.0 - r * 0.14, y - r * 0.15, r * 0.28, r * 0.42, r * 0.1); fill_stroke(c, (0.15, 0.15, 0.17), 5)
    if cap:
        c.new_path(); c.move_to(x - r * 1.0, y - r * 0.5); c.curve_to(x - r * 0.9, y - r * 1.3, x + r * 0.9, y - r * 1.3, x + r * 1.0, y - r * 0.5); c.close_path(); fill_stroke(c, (0.06, 0.08, 0.2), 6)
        rr(c, x - r * 1.15, y - r * 0.6, r * 2.3, r * 0.2, r * 0.08); fill_stroke(c, (0.03, 0.03, 0.06), 4)
        c.new_path(); c.arc(x, y - r * 0.9, r * 0.12, 0, 7); c.set_source_rgb(1, 0.85, 0.3); c.fill()
    if (t + x * 0.001) % 3.7 < 0.12:
        for sx in (-1, 1):
            ex, ey = x + sx * r * 0.33 + look[0], y + r * 0.02 + look[1]
            c.new_path(); c.arc(ex, ey, r * 0.15, 0, 7); c.set_source_rgb(0.98, 0.98, 0.99); c.fill()
            c.move_to(ex - r * 0.12, ey); c.line_to(ex + r * 0.12, ey); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()


# ------------------------------------------------------------------ globe de nuit
def earth_night(c, t, prog=0.6, zoom=1.0):
    c.set_source_rgb(0.0, 0.0, 0.02); c.paint()
    r = random.Random(2)
    for _ in range(300):
        c.new_path(); c.arc(r.random() * W, r.random() * H, r.choice((0.7, 1, 1.5)), 0, 7); c.set_source_rgba(1, 1, 1, 0.2 + 0.6 * r.random()); c.fill()
    c.save(); c.translate(540, 1000); c.scale(zoom, zoom); c.translate(-540, -1000)
    cx, cy, R0 = 540, 1900, 1450
    radial(c, cx, cy, R0 + 120, (0.25, 0.5, 1.0), 0.0)
    g = cairo.RadialGradient(cx, cy, R0 - 30, cx, cy, R0 + 60); g.add_color_stop_rgba(0, 0.2, 0.5, 1.0, 0.7); g.add_color_stop_rgba(1, 0.2, 0.5, 1.0, 0); c.new_path(); c.arc(cx, cy, R0 + 60, 0, 7); c.set_source(g); c.fill()
    c.new_path(); c.arc(cx, cy, R0, 0, 7)
    g = cairo.RadialGradient(cx - 300, cy - 900, 100, cx, cy, R0); g.add_color_stop_rgb(0, 0.05, 0.12, 0.3); g.add_color_stop_rgb(1, 0.01, 0.03, 0.09); c.set_source(g); c.fill()
    c.save(); c.new_path(); c.arc(cx, cy, R0, 0, 7); c.clip()
    land = (0.04, 0.07, 0.08)
    c.new_path(); c.move_to(-200, 1300); c.curve_to(80, 1180, 200, 1150, 260, 1260); c.curve_to(300, 1400, 200, 1600, 120, 1900); c.line_to(-200, 1900); c.close_path(); c.set_source_rgb(*land); c.fill()   # Amérique du Sud
    c.new_path(); c.move_to(1300, 760); c.curve_to(1000, 720, 860, 820, 820, 960); c.curve_to(800, 1080, 900, 1120, 1000, 1200); c.line_to(1300, 1300); c.close_path(); c.set_source_rgb(*land); c.fill()   # Afrique
    c.new_path(); c.move_to(1300, 380); c.curve_to(1050, 420, 960, 520, 940, 600); c.curve_to(1050, 640, 1200, 620, 1300, 600); c.close_path(); c.set_source_rgb(*land); c.fill()   # Europe
    rr_ = random.Random(5)
    for (lx, ly, n, sp) in ((180, 1300, 70, 90), (230, 1420, 40, 60), (900, 950, 40, 90), (1000, 520, 60, 80), (880, 1060, 20, 50)):
        for _ in range(n):
            x = lx + rr_.gauss(0, sp); y = ly + rr_.gauss(0, sp * 0.6)
            c.new_path(); c.arc(x, y, 1 + 2 * rr_.random(), 0, 7); c.set_source_rgba(1, 0.8, 0.45, 0.4 + 0.5 * rr_.random()); c.fill()
    c.restore()
    p0, p1, pc = (230, 1290), (880, 560), (420, 780)                 # Rio -> Paris (arc)
    def bez(u): return ((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * pc[0] + u * u * p1[0], (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * pc[1] + u * u * p1[1])
    n = 60
    for j in range(n):
        u0, u1 = j / n, (j + 0.5) / n
        c.move_to(*bez(u0)); c.line_to(*bez(u1))
    c.set_source_rgba(1, 1, 1, 0.35); c.set_line_width(4); c.stroke()
    m = int(n * prog)
    c.move_to(*bez(0))
    for j in range(1, m + 1): c.line_to(*bez(j / n))
    c.set_source_rgba(*AMB, 0.95); c.set_line_width(6); c.stroke()
    px, py = bez(prog); radial(c, px, py, 60, AMB, 0.8); c.new_path(); c.arc(px, py, 9, 0, 7); c.set_source_rgb(1, 0.95, 0.8); c.fill()
    for (x, y), nm in ((p0, "RIO"), (p1, "PARIS")):
        c.new_path(); c.arc(x, y, 8, 0, 7); c.set_source_rgb(1, 1, 1); c.fill(); label(c, nm, x, y + 45, 34, WH, 1, 'Bebas Neue')
    c.restore()


# ------------------------------------------------------------------ cockpit (vue arrière)
def cockpit_rear(c, t, storm=0.0, chaos=0.0, captain=0.0, seats=2, look=(0, -8), q=False):
    c.set_source_rgb(0.02, 0.02, 0.03); c.paint()
    c.new_path(); c.move_to(80, 420); c.line_to(1000, 420); c.line_to(960, 760); c.line_to(120, 760); c.close_path()   # pare-brise
    g = cairo.LinearGradient(0, 420, 0, 760); g.add_color_stop_rgb(0, 0.02, 0.03, 0.08); g.add_color_stop_rgb(1, 0.06, 0.08, 0.16); c.set_source(g); c.fill()
    if storm > 0:
        fl = max(0.0, math.sin(t * 7.3) * math.sin(t * 3.1)) ** 6
        c.save(); c.new_path(); c.move_to(80, 420); c.line_to(1000, 420); c.line_to(960, 760); c.line_to(120, 760); c.close_path(); c.clip()
        c.set_source_rgba(0.7, 0.75, 1, storm * fl * 0.8); c.paint()
        r = random.Random(int(t * 20))
        for _ in range(int(60 * storm)):
            x = r.random() * W; y = 420 + r.random() * 340; c.new_path(); c.arc(x, y, 1.5, 0, 7); c.set_source_rgba(1, 1, 1, 0.6); c.fill()
        c.restore()
    for x0 in (540,):
        c.move_to(x0, 420); c.line_to(x0, 760); c.set_source_rgb(0.08, 0.08, 0.1); c.set_line_width(22); c.stroke()
    c.new_path(); c.move_to(0, 760); c.curve_to(300, 730, 780, 730, W, 760); c.line_to(W, 1100); c.line_to(0, 1100); c.close_path(); c.set_source_rgb(0.1, 0.1, 0.12); c.fill()   # tableau
    for j, x in enumerate((140, 300, 460, 620, 780, 940)):
        rr(c, x - 65, 790, 130, 120, 10); c.set_source_rgb(0.02, 0.03, 0.05); c.fill()
        if j in (0, 5): c.new_path(); c.rectangle(x - 55, 800, 110, 50); c.set_source_rgb(0.15, 0.4, 0.8); c.fill(); c.new_path(); c.rectangle(x - 55, 850, 110, 50); c.set_source_rgb(0.5, 0.33, 0.15); c.fill()
        elif j in (2, 3):
            for k in range(4):
                on = chaos > 0 and ((t * 3 + k + j) % 2 < 1)
                c.new_path(); c.rectangle(x - 50, 805 + k * 24, 100 * (0.5 + 0.5 * ((k * 7 + j) % 3) / 2), 12); c.set_source_rgba(*((1, 0.25, 0.2) if on else (0.3, 0.9, 0.5)), 0.9); c.fill()
        else:
            c.new_path(); c.arc(x, 850, 40, 0, 7); c.set_source_rgba(0.3, 0.9, 1, 0.5); c.set_line_width(4); c.stroke()
    if chaos > 0:
        on = (t * 2.5) % 1 < 0.5
        for x in (250, 830):
            rr(c, x - 60, 740, 120, 40, 8); c.set_source_rgb(*((1, 0.15, 0.1) if on else (0.3, 0.05, 0.05))); c.fill()
            if on: radial(c, x, 760, 260, RED, 0.35 * chaos)
    # sièges + pilotes (de dos, on voit le profil)
    for j, x in enumerate((330, 750)[:seats]):
        rr(c, x - 120, 1000, 240, 420, 60); fill_stroke(c, (0.12, 0.12, 0.14), 8)
        rr(c, x - 85, 1120, 170, 300, 50); fill_stroke(c, (0.2, 0.24, 0.42), 7)
        stick_head(c, x, 1030, 92, t + j, 'worried', (look[0] * (1 if j == 0 else -1), look[1]), cap=False, headset=True)
        if q: text(c, "?", x + 90, 920, 110, YEL, glow=0.8)
    if captain > 0:
        x = 540 + 520 * (1 - captain)
        c.save(); c.translate(x, 0)
        rr(c, -90, 1080, 180, 380, 60); fill_stroke(c, (0.06, 0.08, 0.2), 8)
        for sx in (-1, 1): rr(c, sx * 60 - 10, 1100, 20, 12, 3); c.set_source_rgb(1, 0.85, 0.3); c.fill()
        stick_head(c, 0, 990, 95, t, 'worried', (0, -6), cap=True, headset=False)
        if q: text(c, "?", 100, 870, 110, YEL, glow=0.8)
        c.restore()


# ------------------------------------------------------------------ instruments
def pfd(c, x, y, w, h, spd, alt, pitch, t, spd_fail=0.0, stall=False, ap_off=False, vs=None):
    c.save(); rr(c, x - w / 2, y - h / 2, w, h, 18); c.set_source_rgb(0.02, 0.02, 0.03); c.fill_preserve(); c.set_source_rgb(0.3, 0.32, 0.36); c.set_line_width(8); c.stroke()
    ax, ay, aw, ah = x - w * 0.22, y + h * 0.04, w * 0.46, h * 0.62
    c.save(); rr(c, ax - aw / 2, ay - ah / 2, aw, ah, 30); c.clip()
    off = pitch * 7
    c.new_path(); c.rectangle(ax - aw, ay - ah - 400 + off, aw * 2, ah + 400); c.set_source_rgb(0.15, 0.45, 0.9); c.fill()
    c.new_path(); c.rectangle(ax - aw, ay + off, aw * 2, ah + 400); c.set_source_rgb(0.55, 0.33, 0.12); c.fill()
    c.move_to(ax - aw, ay + off); c.line_to(ax + aw, ay + off); c.set_source_rgb(1, 1, 1); c.set_line_width(4); c.stroke()
    for d in (-20, -10, 10, 20, 30):
        yy = ay + off - d * 7; ww = 60 if d % 20 == 0 else 35
        c.move_to(ax - ww, yy); c.line_to(ax + ww, yy); c.set_source_rgb(1, 1, 1); c.set_line_width(3); c.stroke()
    c.restore()
    c.move_to(ax - 110, ay); c.line_to(ax - 40, ay); c.line_to(ax - 40, ay + 18); c.move_to(ax + 110, ay); c.line_to(ax + 40, ay); c.line_to(ax + 40, ay + 18)
    c.set_source_rgb(*AMB); c.set_line_width(9); c.stroke(); c.new_path(); c.rectangle(ax - 6, ay - 6, 12, 12); c.set_source_rgb(*AMB); c.fill()
    # bande de vitesse
    sx0 = x - w * 0.47; sw = w * 0.17
    rr(c, sx0, y - h * 0.38, sw, h * 0.76, 8); c.set_source_rgb(0.18, 0.19, 0.22); c.fill()
    if spd_fail > 0.5:
        c.save(); rr(c, sx0, y - h * 0.38, sw, h * 0.76, 8); c.clip(); c.set_source_rgba(1, 0.1, 0.1, 0.15 + 0.15 * math.sin(t * 12)); c.paint(); c.restore()
        text(c, "SPD", sx0 + sw / 2, y + 15, 54, RED)
    else:
        for k in range(-3, 4):
            v = int(round(spd / 20) * 20 + k * 20); yy = y - (v - spd) * 3.2
            if y - h * 0.36 < yy < y + h * 0.36:
                F(c, 30, 'Montserrat'); s_ = str(max(0, v)); c.move_to(sx0 + 10, yy + 10); c.text_path(s_); c.set_source_rgb(1, 1, 1); c.fill()
        rr(c, sx0 - 6, y - 28, sw + 12, 56, 6); c.set_source_rgb(0, 0, 0); c.fill_preserve(); c.set_source_rgb(*AMB); c.set_line_width(3); c.stroke()
        F(c, 36, 'Montserrat'); s_ = str(int(spd)); c.move_to(sx0 + 8, y + 13); c.text_path(s_); c.set_source_rgb(*(RED if stall else (0.3, 1, 0.5))); c.fill()
    # bande d'altitude
    ax0 = x + w * 0.27; aw2 = w * 0.18
    rr(c, ax0, y - h * 0.38, aw2, h * 0.76, 8); c.set_source_rgb(0.18, 0.19, 0.22); c.fill()
    for k in range(-3, 4):
        v = int(round(alt / 500) * 500 + k * 500); yy = y - (v - alt) * 0.22
        if y - h * 0.36 < yy < y + h * 0.36 and v >= 0:
            F(c, 28, 'Montserrat'); c.move_to(ax0 + 8, yy + 10); c.text_path(str(v)); c.set_source_rgb(1, 1, 1); c.fill()
    rr(c, ax0 - 6, y - 28, aw2 + 12, 56, 6); c.set_source_rgb(0, 0, 0); c.fill_preserve(); c.set_source_rgb(*AMB); c.set_line_width(3); c.stroke()
    F(c, 32, 'Montserrat'); c.move_to(ax0 + 6, y + 12); c.text_path(str(int(alt))); c.set_source_rgb(0.3, 1, 0.5); c.fill()
    label(c, "FT", ax0 + aw2 / 2, y + h * 0.45, 26, (0.7, 0.75, 0.8))
    label(c, "KT", sx0 + sw / 2, y + h * 0.45, 26, (0.7, 0.75, 0.8))
    if vs is not None:
        F(c, 26, 'Montserrat'); s_ = f"V/S {vs:+d}"; c.move_to(ax0 - 40, y - h * 0.42); c.text_path(s_); c.set_source_rgb(*(RED if vs < -3000 else (0.3, 1, 0.5))); c.fill()
    if ap_off and (t * 2) % 1 < 0.6:
        rr(c, x - 150, y - h * 0.47, 300, 54, 8); c.set_source_rgb(0.25, 0.02, 0.02); c.fill(); text(c, "AP OFF", x, y - h * 0.47 + 44, 48, RED)
    if stall and (t * 3) % 1 < 0.55:
        text(c, "STALL", ax, ay - ah * 0.2, 90, RED, glow=0.8)
    c.restore()


def sidestick(c, x, y, s, defl, t, ghost=None, labels=True):
    """Manche latéral Airbus vu de profil : defl -1 (pousser) … +1 (tirer)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    rr(c, -230, 120, 460, 140, 30); fill_stroke(c, (0.14, 0.14, 0.16), 8)
    c.new_path(); c.save(); c.scale(1, 0.35); c.arc(0, 340, 120, 0, 7); c.restore(); c.set_source_rgb(0.05, 0.05, 0.06); c.fill()
    def stick(a, col, alpha):
        c.save(); c.rotate(a); c.push_group()
        c.move_to(0, 120); c.line_to(0, -60); c.set_source_rgb(*INK); c.set_line_width(46); c.set_line_cap(1); c.stroke()
        c.move_to(0, 120); c.line_to(0, -60); c.set_source_rgb(*col); c.set_line_width(30); c.stroke()
        rr(c, -48, -230, 96, 190, 44); fill_stroke(c, (0.18, 0.18, 0.2), 8)
        rr(c, -20, -220, 40, 26, 10); c.set_source_rgb(0.85, 0.15, 0.15); c.fill()
        c.pop_group_to_source(); c.paint_with_alpha(alpha); c.restore()
    if ghost is not None:
        stick(-0.45 * ghost, (0.3, 1, 0.5), 0.35)
    stick(-0.45 * defl, (0.3, 0.3, 0.33), 1.0)
    c.restore()


def wing_flow(c, x, y, s, aoa, t, stalled=0.0):
    """Profil d'aile + filets d'air animés : attachés (aoa faible) ou décollés (décrochage) avec tourbillons."""
    c.save(); c.translate(x, y); c.scale(s, s)
    n = 13
    a = math.radians(aoa)
    for i in range(n):
        y0 = -330 + i * 55
        c.new_path()
        first = True
        for xx in range(-520, 521, 12):
            d = y0
            # déviation autour du profil (dipôle simplifié) : contournement
            dist = math.hypot(xx * 0.7, y0) + 1
            bump = 9000 / (dist + 60) * (1 if y0 < 0 else 0.6) * math.exp(-(xx / 380) ** 2)
            yy = y0 - math.copysign(bump * 0.35, y0) * (1 - 0.0) - xx * math.tan(a) * 0.25 * math.exp(-(xx / 300) ** 2)
            if stalled > 0 and y0 < 40 and xx > -40:
                k = stalled * min(1, (xx + 40) / 200)
                yy += k * (40 * math.sin(xx / 35 - t * 6 + i) + 30) * (1 if y0 > -200 else 0.4)
            if first: c.move_to(xx, yy); first = False
            else: c.line_to(xx, yy)
        col = mix((0.3, 0.85, 1.0), (1, 0.35, 0.3), stalled if y0 < 40 else 0.0)
        c.set_source_rgba(*col, 0.55); c.set_line_width(4); c.stroke()
        for j in range(4):                                # particules qui glissent sur les filets
            ph = (t * 0.6 + j / 4 + i * 0.13) % 1; xx = -520 + 1040 * ph
            dist = math.hypot(xx * 0.7, y0) + 1; bump = 9000 / (dist + 60) * (1 if y0 < 0 else 0.6) * math.exp(-(xx / 380) ** 2)
            yy = y0 - math.copysign(bump * 0.35, y0) - xx * math.tan(a) * 0.25 * math.exp(-(xx / 300) ** 2)
            if stalled > 0 and y0 < 40 and xx > -40:
                k = stalled * min(1, (xx + 40) / 200); yy += k * (40 * math.sin(xx / 35 - t * 6 + i) + 30) * (1 if y0 > -200 else 0.4)
            c.new_path(); c.arc(xx, yy, 6, 0, 7); c.set_source_rgb(1, 1, 1); c.fill()
    if stalled > 0:                                       # tourbillons
        for j in range(5):
            cx = 60 + j * 90 + 20 * math.sin(t * 2 + j); cy = -60 - 30 * math.sin(j); rot = t * 4 + j
            c.new_path()
            for k in range(60):
                u = k / 60; rad = 6 + 40 * u
                c.line_to(cx + math.cos(rot + u * 12) * rad, cy + math.sin(rot + u * 12) * rad)
            c.set_source_rgba(1, 0.4, 0.3, 0.6 * stalled); c.set_line_width(4); c.stroke()
    c.rotate(-a)                                           # profil
    c.new_path(); c.move_to(-230, 0); c.curve_to(-230, -55, -80, -70, 60, -45); c.curve_to(160, -28, 240, -8, 260, 0); c.curve_to(150, 18, -120, 30, -200, 22); c.curve_to(-232, 18, -232, 6, -230, 0); c.close_path()
    g = cairo.LinearGradient(0, -70, 0, 30); g.add_color_stop_rgb(0, 0.95, 0.96, 0.98); g.add_color_stop_rgb(1, 0.6, 0.62, 0.7); c.set_source(g); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
    c.restore()


def traj_data():
    """Profil d'altitude simplifié (ft) d'après la chronologie BEA, t en s depuis 02:10:05."""
    return [(0, 35000), (20, 35600), (45, 37200), (65, 38000), (80, 37300), (95, 35500), (115, 33500), (140, 30200), (170, 25000), (200, 19300), (230, 12500), (250, 6200), (263, 0)]


def alt_at(s):
    d = traj_data()
    for (a, h0), (b, h1) in zip(d, d[1:]):
        if a <= s <= b: return h0 + (h1 - h0) * (s - a) / (b - a)
    return 0 if s > 263 else 35000


def traj_plot(c, t, prog, x0=110, y0=470, w=860, h=760, title=True):
    """Courbe d'altitude « données » tracée en direct, axe temps réel 02:10:05 -> 02:14:28."""
    rr(c, x0 - 30, y0 - 40, w + 60, h + 120, 30); c.set_source_rgba(0.02, 0.03, 0.06, 0.82); c.fill_preserve(); c.set_source_rgba(*CY, 0.5); c.set_line_width(3); c.stroke()
    for k in range(0, 5):
        yy = y0 + h - h * k / 4; c.move_to(x0, yy); c.line_to(x0 + w, yy); c.set_source_rgba(1, 1, 1, 0.08); c.set_line_width(2); c.stroke()
        F(c, 24, 'Montserrat'); s_ = f"{int(12000 * k / 4):,} m".replace(',', ' '); c.move_to(x0 + 6, yy - 8); c.text_path(s_); c.set_source_rgba(1, 1, 1, 0.4); c.fill()
    S = 263 * prog
    def P(sv): return x0 + w * sv / 263, y0 + h - h * (alt_at(sv) * 0.3048) / 12000
    c.move_to(*P(0))
    for k in range(1, 200):
        sv = S * k / 199; c.line_to(*P(sv))
    c.set_source_rgba(*CY, 0.25); c.set_line_width(22); c.set_line_cap(1); c.set_line_join(1); c.stroke_preserve()
    c.set_source_rgb(*CY); c.set_line_width(6); c.stroke()
    px, py = P(S); radial(c, px, py, 60, CY, 0.8); c.new_path(); c.arc(px, py, 10, 0, 7); c.set_source_rgb(1, 1, 1); c.fill()
    tt = 10 * 60 + 5 + int(S); mm, ss = tt // 60, tt % 60
    text(c, f"02:{mm:02d}:{ss:02d}", x0 + w / 2, y0 + h + 60, 64, WH)
    alt_m = int(alt_at(S) * 0.3048 / 10) * 10
    text(c, f"{alt_m:,} M".replace(',', ' '), min(max(px, x0 + 120), x0 + w - 120), py - 40, 54, CY)
    label(c, "reconstitution simplifiée d'après le BEA", x0 + w / 2, y0 + h + 100, 26, (0.6, 0.65, 0.75))


def ice_storm(c, t, a=1.0, flash=True):
    sky(c, (0.04, 0.05, 0.1), (0.12, 0.14, 0.22))
    r = random.Random(4)
    for _ in range(10):
        x = r.random() * W; y = r.random() * H; rad = 200 + 300 * r.random()
        g = cairo.RadialGradient(x, y, 0, x, y, rad); g.add_color_stop_rgba(0, 0.25, 0.28, 0.4, 0.5); g.add_color_stop_rgba(1, 0.25, 0.28, 0.4, 0); c.set_source(g); c.paint()
    fl = max(0.0, math.sin(t * 5.1) * math.sin(t * 2.3 + 1)) ** 8 if flash else 0
    if fl > 0.05:
        c.set_source_rgba(0.75, 0.8, 1, 0.6 * fl); c.paint()
        rb = random.Random(int(t * 2)); x = 200 + 680 * rb.random(); y = 300
        c.move_to(x, y)
        for k in range(9): x += rb.uniform(-60, 60); y += 70; c.line_to(x, y)
        c.set_source_rgba(1, 1, 1, fl); c.set_line_width(6); c.stroke()
    for j in range(int(140 * a)):                       # cristaux qui foncent vers la caméra
        rr_ = random.Random(j); ang = rr_.random() * 6.283; ph = (t * (0.6 + rr_.random() * 0.8) + rr_.random()) % 1
        d = 30 + 900 * ph ** 2; x = 540 + math.cos(ang) * d; y = 900 + math.sin(ang) * d * 1.3
        sz = 2 + 9 * ph
        c.save(); c.translate(x, y); c.rotate(t * 2 + j)
        for k in range(3):
            c.move_to(-sz, 0); c.line_to(sz, 0); c.rotate(math.pi / 3)
        c.set_source_rgba(0.9, 0.95, 1, 0.9 * ph); c.set_line_width(1.5 + ph * 2); c.stroke(); c.restore()


def radar_scope(c, x, y, r, t, grow=1.0):
    c.save(); c.new_path(); c.arc(x, y, r, math.pi, 2 * math.pi); c.close_path(); c.set_source_rgb(0.01, 0.02, 0.02); c.fill_preserve(); c.clip()
    for k in range(1, 5):
        c.new_path(); c.arc(x, y, r * k / 4, math.pi, 2 * math.pi); c.set_source_rgba(0.3, 1, 0.6, 0.25); c.set_line_width(2); c.stroke()
    for cx, cy, s_ in ((x - 60, y - r * 0.55, 1.0), (x + 120, y - r * 0.7, 0.8), (x - 200, y - r * 0.75, 0.7)):
        for col, k in (((0.1, 0.8, 0.3), 1.0), ((1, 0.9, 0.2), 0.65), ((1, 0.2, 0.15), 0.35), ((1, 0.2, 0.9), 0.15)):
            c.new_path(); c.save(); c.translate(cx, cy); c.scale(1.4, 1); c.arc(0, 0, 120 * s_ * k * grow, 0, 7); c.restore(); c.set_source_rgba(*col, 0.8); c.fill()
    sw = (t * 1.2) % 1; a = math.pi + math.pi * sw
    c.move_to(x, y); c.line_to(x + math.cos(a) * r, y + math.sin(a) * r); c.set_source_rgba(0.3, 1, 0.6, 0.8); c.set_line_width(4); c.stroke()
    c.restore()
    c.new_path(); c.move_to(x, y - 10); c.line_to(x - 18, y + 22); c.line_to(x + 18, y + 22); c.close_path(); c.set_source_rgb(1, 1, 1); c.fill()
    c.new_path(); c.arc(x, y, r, math.pi, 2 * math.pi); c.set_source_rgb(0.4, 0.42, 0.46); c.set_line_width(8); c.stroke()


def pitot_cut(c, t, plug, x=540, y=880, s=1.0):
    """Coupe d'une sonde Pitot : l'air entre, les cristaux s'accumulent et bouchent l'orifice."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.new_path(); c.move_to(-420, -120); c.line_to(420, -120); c.line_to(420, 180); c.line_to(-420, 180); c.close_path(); c.set_source_rgb(0.85, 0.86, 0.9); c.fill()   # peau du fuselage
    rr(c, -380, -60, 640, 120, 50); g = cairo.LinearGradient(0, -60, 0, 60); g.add_color_stop_rgb(0, 0.85, 0.87, 0.9); g.add_color_stop_rgb(0.5, 0.65, 0.67, 0.72); g.add_color_stop_rgb(1, 0.4, 0.42, 0.47)
    c.set_source(g); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
    rr(c, -380, -24, 600, 48, 20); c.set_source_rgb(0.12, 0.12, 0.15); c.fill()   # canal interne
    c.new_path(); c.rectangle(200, -60, 60, 240); fill_stroke(c, (0.6, 0.62, 0.68), 6)   # mât
    for j in range(7):                                   # flux d'air entrant
        ph = (t * 1.6 + j / 7) % 1; xx = -700 + 420 * ph * (1 - 0.7 * plug) ; yy = -18 + (j % 3) * 18
        c.move_to(xx - 70, yy); c.line_to(xx, yy); c.set_source_rgba(0.4, 0.85, 1, 0.8 * (1 - ph)); c.set_line_width(6); c.set_line_cap(1); c.stroke()
    r = random.Random(3)
    for j in range(90):                                  # cristaux qui s'accumulent à l'entrée
        if j / 90 > plug: break
        xx = -385 + 70 * r.random() ** 2; yy = -22 + 44 * r.random()
        c.save(); c.translate(xx, yy); c.rotate(r.random() * 3)
        for k in range(3): c.move_to(-7, 0); c.line_to(7, 0); c.rotate(math.pi / 3)
        c.set_source_rgb(0.9, 0.97, 1); c.set_line_width(2.5); c.stroke(); c.restore()
    if plug > 0.6:
        c.new_path(); c.save(); c.translate(-372, 0); c.scale(0.5, 1); c.arc(0, 0, 32 * (plug - 0.6) / 0.4, 0, 7); c.restore(); c.set_source_rgba(0.92, 0.97, 1, 0.9); c.fill()
    c.restore()


def deep_sea(c, t, depth, sonar=0.0, rov=0.0):
    k = min(1, depth / 4000)
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *mix((0.05, 0.25, 0.45), (0.0, 0.01, 0.03), k)); g.add_color_stop_rgb(1, *mix((0.02, 0.1, 0.22), (0, 0, 0.01), k)); c.set_source(g); c.paint()
    if k < 0.5:
        for j in range(6):
            x = 150 + j * 160 + 30 * math.sin(t + j); c.move_to(x, 0); c.line_to(x - 120, H); c.line_to(x - 60, H); c.close_path(); c.set_source_rgba(0.6, 0.8, 1, 0.05 * (1 - 2 * k)); c.fill()
    r = random.Random(9)
    for _ in range(120):                                  # neige marine
        x = (r.random() * W + 10 * math.sin(t + r.random() * 6)) % W; y = (r.random() * H - t * 30) % H
        c.new_path(); c.arc(x, y, 1 + 2 * r.random(), 0, 7); c.set_source_rgba(0.8, 0.9, 1, 0.35); c.fill()
    if sonar > 0:
        c.new_path(); c.move_to(0, 1250); c.curve_to(300, 1220, 700, 1270, W, 1240); c.line_to(W, H); c.line_to(0, H); c.close_path(); c.set_source_rgb(0.04, 0.05, 0.06); c.fill()
        sw = (t * 0.7) % 1; c.new_path(); c.arc(540, 700, 900 * sw, 0.3, math.pi - 0.3); c.set_source_rgba(0.3, 1, 0.7, 0.6 * (1 - sw)); c.set_line_width(5); c.stroke()
        rd = random.Random(11)
        for _ in range(int(40 * sonar)):                  # débris (formes géométriques, sobres)
            x = 200 + 680 * rd.random(); y = 1250 + 60 * rd.random(); w_ = 10 + 40 * rd.random()
            c.save(); c.translate(x, y); c.rotate(rd.uniform(-0.6, 0.6)); c.new_path(); c.rectangle(-w_ / 2, -6, w_, 12); c.set_source_rgba(0.35, 1, 0.75, 0.75 * sonar); c.fill(); c.restore()
    if rov > 0:
        c.save(); c.new_path(); c.move_to(900, 900); c.line_to(400, 1330); c.line_to(700, 1360); c.close_path(); c.clip()
        g = cairo.LinearGradient(900, 900, 550, 1340); g.add_color_stop_rgba(0, 1, 1, 0.9, 0.0); g.add_color_stop_rgba(1, 1, 1, 0.9, 0.35 * rov); c.set_source(g); c.paint(); c.restore()
        rr(c, 820, 860, 140, 80, 16); fill_stroke(c, (0.95, 0.75, 0.15), 6, rov); radial(c, 900, 900, 50, (1, 1, 0.9), 0.8 * rov)
        c.save(); c.translate(560, 1310); c.rotate(-0.15)
        rr(c, -60, -40, 120, 80, 10); fill_stroke(c, (1, 0.45, 0.05), 6, rov)
        c.new_path(); c.arc(0, -40, 26, math.pi, 2 * math.pi); c.set_source_rgba(0.9, 0.9, 0.95, rov); c.fill(); c.restore()


def memorial(c, t, p):
    ocean_night(c, t, horizon=1100, calm=0.6)
    r = random.Random(228)
    n = int(228 * min(1, p * 1.4))
    for j in range(n):
        x = 90 + 900 * r.random(); sp = 0.15 + 0.25 * r.random(); y0 = 1150 + 300 * r.random()
        y = y0 - (t * 60 * sp + r.random() * 600) % 1100
        a = 0.35 + 0.5 * r.random()
        radial(c, x, y, 34, (1, 0.75, 0.4), a * 0.55); c.new_path(); c.arc(x, y, 5, 0, 7); c.set_source_rgba(1, 0.94, 0.75, a); c.fill()


# ------------------------------------------------------------------ scènes
def sc_af_hook(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k <= 1:
        night_sky(c, t); cloud_sea(c, t, 1180)
        a330(c, 560, 860 + 6 * math.sin(t * 1.2), -0.02, 1.2, t, eng_glow=ap(p, 0.1, 0.4) if k == 0 else 0, wing_glow=ap(p, 0.1, 0.4) if k == 1 else 0)
        if k == 0:
            check(c, 760, 1060, 1.3, GRN, ap(p, 0.2, 0.4)); tag(c, "2 MOTEURS : OK", 540, 1300, GRN, ap(p, 0.2, 0.4), 70)
        else:
            check(c, 360, 1060, 1.3, GRN, ap(p, 0.2, 0.4)); tag(c, "AILES INTACTES", 540, 1300, GRN, ap(p, 0.2, 0.4), 70)
    elif k == 2:
        night_sky(c, t); ocean_night(c, t, 1350)
        q = ap(p, 0.05, 0.9)
        c.move_to(260, 520)
        for j in range(1, 40):
            uu = j / 39 * q; c.line_to(260 + 520 * uu, 520 + 820 * uu ** 1.6)
        c.set_source_rgba(1, 0.4, 0.3, 0.8); c.set_dash([18, 12]); c.set_line_width(6); c.stroke(); c.set_dash([])
        a330(c, 260 + 520 * q, 520 + 820 * q ** 1.6, -0.25, 0.5, t)
        mm = int(4 * 60 * q); text(c, f"{mm // 60}:{mm % 60:02d}", 540, 480, 150, RED, glow=0.9)
        if q > 0.97:
            for j in range(3):
                c.new_path(); c.save(); c.translate(780, 1350); c.scale(1, 0.25); c.arc(0, 0, 60 + j * 70 + 80 * (p - 0.9) * 10, 0, 7); c.restore(); c.set_source_rgba(1, 1, 1, 0.4); c.set_line_width(3); c.stroke()
    else:
        ocean_night(c, t, 900, calm=0.3)
        for j in range(4):
            ph = (t * 0.5 + j / 4) % 1; c.new_path(); c.save(); c.translate(540, 1250); c.scale(1, 0.22); c.arc(0, 0, 80 + 600 * ph, 0, 7); c.restore(); c.set_source_rgba(1, 1, 1, 0.35 * (1 - ph)); c.set_line_width(3); c.stroke()
        stamp(c, "POURQUOI ?", 540, 700, 190, RED, since, glow=1.0)


def sc_af_night(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        earth_night(c, t, prog=0.25 + 0.3 * p, zoom=1.0 + 0.12 * p)
        tag(c, "1ER JUIN 2009 · 02:00 UTC", 540, 460, AMB, ap(p, 0.05, 0.2), 58)
    elif k == 1:
        night_sky(c, t); cloud_sea(c, t, 1250)
        c.save(); c.translate(540, 860); c.scale(1.35, 1.35); c.translate(-560, -860)
        a330(c, 540, 860, 0, 1.0, t)
        c.save(); c.translate(540, 860)                       # coupe : rangées de passagers
        rr(c, -215, -26, 470, 44, 18); c.set_source_rgba(0.08, 0.1, 0.18, ap(p, 0.05, 0.25)); c.fill()
        n = int(228 * ap(p, 0.1, 0.8))
        for i in range(n):
            col_, row = i % 57, i // 57
            c.new_path(); c.arc(-205 + col_ * 8.1, -18 + row * 10, 3, 0, 7); c.set_source_rgba(1, 0.9, 0.75, 0.9); c.fill()
        c.restore(); c.restore()
        text(c, str(int(228 * ap(p, 0.1, 0.8))), 540, 620, 190, WH, glow=0.6)
        tag(c, "216 PASSAGERS · 12 MEMBRES D'ÉQUIPAGE", 540, 1290, WH, ap(p, 0.5, 0.7), 44)
    elif k == 2:
        cockpit_rear(c, t, seats=2, captain=1 - ap(p, 0.1, 0.8))
        tag(c, "LE COMMANDANT VA SE REPOSER", 540, 520, WH, ap(p, 0.2, 0.4), 52)
    else:
        cockpit_rear(c, t, seats=2)
        for x in (330, 750): tag(c, "COPILOTE", x, 1390, CY, ap(p, 0.1 + (x > 500) * 0.15, 0.3 + (x > 500) * 0.15), 50)


def sc_af_storm(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        cockpit_rear(c, t, storm=0.6, seats=2)
        c.set_source_rgba(0, 0, 0, 0.55); c.paint()
        radar_scope(c, 540, 1080, 400, t, grow=0.6 + 0.4 * p)
        tag(c, "ZONE ORAGEUSE", 540, 560, YEL, ap(p, 0.1, 0.3), 70)
    else:
        ice_storm(c, t, a=0.5 + 0.5 * p)
        c.push_group(); a330(c, 560, 900, 0.0, 1.25, t, lights=True); c.pop_group_to_source(); c.paint_with_alpha(0.85)
        tag(c, "CRISTAUX DE GLACE", 540, 1300, CY, ap(p, 0.3, 0.5), 66)


def sc_af_pitot(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        z = ap(p, 0.0, 0.35)
        if z < 1:                                           # zoom continu : de l'avion vers la sonde
            ice_storm(c, t, a=0.4, flash=False)
            c.save(); c.translate(540, 900); sc_ = 1 + 18 * z ** 2; c.scale(sc_, sc_); c.translate(-(540 + 285 * 1.4 * z), -(900 + 6 * 1.4 * z))
            a330(c, 540, 900, 0, 1.4, t); c.restore()
            c.set_source_rgba(0.85, 0.86, 0.9, ap(z, 0.7, 1.0)); c.paint()
        else:
            sky(c, (0.08, 0.09, 0.14), (0.14, 0.15, 0.22))
            pitot_cut(c, t, ap(p, 0.4, 0.95), 600, 880, 1.15)
            tag(c, "SONDE PITOT", 540, 560, WH, 1, 70)
            if p > 0.7: tag(c, "BOUCHÉE", 540, 1300, RED, ap(p, 0.7, 0.8), 80)
    elif k == 1:
        c.set_source_rgb(0.03, 0.03, 0.05); c.paint()
        q = ap(p, 0.05, 0.7)
        spd = 275 - 215 * q + (25 * math.sin(t * 17) if q > 0.2 else 0)
        pfd(c, 540, 900, 900, 680, max(40, spd), 35000, 2.5, t, spd_fail=1.0 if (p > 0.75 and (t * 4) % 1 < 0.5) else 0.0)
        tag(c, "VITESSE FAUSSE", 540, 1360, RED, ap(p, 0.2, 0.35), 70)
    else:
        c.set_source_rgb(0.03, 0.03, 0.05); c.paint(); on = (t * 2.2) % 1 < 0.5
        if on: radial(c, 540, 900, 700, RED, 0.25)
        pfd(c, 540, 900, 900, 680, 60, 35000, 3, t, spd_fail=1.0, ap_off=True)
        tag(c, "02:10:05", 540, 1360, AMB, 1, 70)


def sc_af_climb(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        c.set_source_rgb(0.04, 0.04, 0.06); c.paint(); radial(c, 540, 900, 600, RED, 0.12)
        d = ap(p, 0.1, 0.5)
        sidestick(c, 540, 820, 1.45, d, t)
        if d > 0.3:
            c.move_to(760, 640); c.curve_to(820, 700, 820, 800, 770, 860); c.set_source_rgb(*RED); c.set_line_width(12); c.set_line_cap(1); c.stroke()
            c.move_to(745, 830); c.line_to(772, 866); c.line_to(800, 830); c.stroke()
        tag(c, "IL TIRE SUR LE MANCHE", 540, 1330, RED, ap(p, 0.3, 0.5), 60)
    else:
        night_sky(c, t); cloud_sea(c, t, 1300)
        traj_plot(c, t, 0.25 * ap(p, 0.0, 0.9), 110, 470, 860, 600)
        tag(c, "IL MONTE… ET RALENTIT", 540, 1300, ORG, ap(p, 0.3, 0.45), 56)


def sc_af_stall(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        c.set_source_rgb(0.05, 0.0, 0.0); c.paint()
        on = (t * 3) % 1 < 0.55
        if on: radial(c, 540, 900, 800, RED, 0.45)
        pfd(c, 540, 1080, 820, 560, 95, 37800, 15, t, stall=True)
        text(c, "STALL", 540, 640, 210, RED if on else (0.5, 0.1, 0.1), glow=1.0 if on else 0)
        label(c, "= DÉCROCHAGE", 540, 730, 50, WH)
    elif k == 1:
        sky(c, (0.02, 0.03, 0.07), (0.05, 0.06, 0.12))
        aoa = 6 + 34 * ap(p, 0.0, 0.6)
        wing_flow(c, 540, 900, 1.25, aoa, t, stalled=ap(p, 0.3, 0.7))
        tag(c, f"INCIDENCE {int(aoa)}°", 540, 560, YEL, 1, 60)
        if p > 0.55: tag(c, "L'AILE NE PORTE PLUS", 540, 1330, RED, ap(p, 0.55, 0.7), 64)
    else:
        c.set_source_rgb(0.04, 0.04, 0.06); c.paint()
        if k == 2:
            sidestick(c, 540, 820, 1.45, 0.9, t, ghost=-0.9 * ap(p, 0.1, 0.4))
            c.move_to(360, 860); c.curve_to(300, 800, 300, 700, 350, 640); c.set_source_rgb(*GRN); c.set_line_width(12); c.set_line_cap(1); c.stroke()
            c.move_to(325, 670); c.line_to(350, 636); c.line_to(378, 672); c.stroke()
            tag(c, "IL FAUDRAIT POUSSER", 540, 1330, GRN, ap(p, 0.2, 0.4), 62)
        else:
            sidestick(c, 540, 820, 1.45, 0.85 + 0.1 * math.sin(t * 5), t, ghost=-0.9)
            cross(c, 330, 720, 1.6, RED, ap(p, 0.2, 0.35))
            tag(c, "IL CONTINUE DE TIRER", 540, 1330, RED, ap(p, 0.1, 0.3), 62)


def sc_af_captain(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        cockpit_rear(c, t, storm=0.3, seats=2, captain=ap(p, 0.0, 0.6), chaos=0.3)
        tag(c, "02:11:40 · LE COMMANDANT REVIENT", 540, 520, AMB, ap(p, 0.1, 0.3), 46)
    elif k == 1:
        cockpit_rear(c, t, storm=0.3, seats=2, captain=1.0, chaos=1.0)
        rr(c, 170, 420, 740, 300, 24); c.set_source_rgba(0.01, 0.01, 0.02, 0.9); c.fill_preserve(); c.set_source_rgb(0.3, 0.32, 0.36); c.set_line_width(5); c.stroke()
        for j, msg in enumerate(("STALL  STALL", "AUTO FLT AP OFF", "NAV ADR DISAGREE", "F/CTL ALTN LAW")):
            on = j == 0 and (t * 3) % 1 < 0.5
            label(c, msg, 540, 485 + j * 62, 44 if j == 0 else 36, RED if j == 0 else AMB, 0.35 if (j == 0 and not on) else 1, 'Bebas Neue' if j == 0 else 'Montserrat')
    else:
        cockpit_rear(c, t, storm=0.3, seats=2, captain=1.0, chaos=0.6, q=True)
        stamp(c, "PERSONNE NE COMPREND", 540, 560, 100, YEL, since, glow=0.8)


def sc_af_fall(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        night_sky(c, t, moon=False)
        c.save(); c.translate(0, -((t * 900) % 400)); cloud_sea(c, t * 0.2, 1500, 0.9); c.restore()
        speedlines(c, t, 0.6, horiz=False, n=30, seed=3)
        pitch = 15
        a330(c, 540, 860, -math.radians(pitch), 1.15, t)
        c.move_to(560, 900); c.line_to(600, 1300); c.set_source_rgb(*RED); c.set_line_width(12); c.set_line_cap(1); c.stroke()   # vecteur vitesse
        c.move_to(570, 1270); c.line_to(600, 1310); c.line_to(625, 1265); c.stroke()
        c.move_to(560, 900); c.line_to(560 + 420 * math.cos(math.radians(pitch)), 900 - 420 * math.sin(math.radians(pitch))); c.set_source_rgba(*CY, 0.9); c.set_dash([16, 10]); c.set_line_width(6); c.stroke(); c.set_dash([])
        c.new_path(); c.arc(560, 900, 200, math.radians(-pitch), math.radians(84)); c.set_source_rgb(*YEL); c.set_line_width(6); c.stroke()
        tag(c, "NEZ EN HAUT", 830, 700, CY, ap(p, 0.05, 0.2), 48)
        tag(c, "≈ 200 KM/H VERS LE BAS", 540, 1390, RED, ap(p, 0.35, 0.5), 56)
        tag(c, "INCIDENCE > 35°", 800, 1120, YEL, ap(p, 0.2, 0.35), 46)
    elif k == 1:
        sky(c, (0.01, 0.02, 0.05), (0.02, 0.03, 0.07))
        traj_plot(c, t, 0.25 + 0.75 * ap(p, 0.0, 0.85), 110, 470, 860, 700)
        if p > 0.85: stamp(c, "4 MIN 23 S", 540, 1390, 120, RED, since - 0.85 * (sg['sent'][2][0] - sg['sent'][1][0]), glow=1.0)
    else:
        ocean_night(c, t, 1000, calm=1.0)
        c.set_source_rgba(0, 0, 0, 0.35); c.paint()
        label(c, "AUCUN SURVIVANT", 540, 760, 64, (0.9, 0.92, 0.96), min(1, since / 0.6), 'Bebas Neue')


def sc_af_search(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    depth = 3980 * ap(p, 0.0, 0.4)
    deep_sea(c, t, depth, sonar=ap(p, 0.35, 0.6), rov=ap(p, 0.6, 0.8))
    rr(c, 300, 440, 480, 150, 30); c.set_source_rgba(0, 0, 0, 0.55); c.fill()
    text(c, f"−{int(depth):,} M".replace(',', ' '), 540, 555, 110, CY, glow=0.6)
    if p > 0.35: tag(c, "AVRIL 2011 : L'ÉPAVE", 540, 680, (0.35, 1, 0.75), ap(p, 0.35, 0.45), 48)
    if p > 0.62: tag(c, "MAI 2011 : LES BOÎTES NOIRES", 540, 1420, ORG, ap(p, 0.62, 0.72), 50)


def sc_af_after(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        sky(c, (0.03, 0.05, 0.1), (0.06, 0.09, 0.16))
        for j, lab in enumerate(("SONDES REMPLACÉES", "FORMATION AU DÉCROCHAGE")):
            a = ap(p, 0.1 + 0.35 * j, 0.25 + 0.35 * j); y = 640 + j * 380
            if a <= 0: continue
            rr(c, 130, y - 140, 820, 280, 36); c.set_source_rgba(0.3, 1, 0.5, 0.08 * a); c.fill_preserve(); c.set_source_rgba(0.3, 1, 0.5, 0.8 * a); c.set_line_width(5); c.stroke()
            check(c, 230, y, 1.6, GRN, a); label(c, lab, 600, y + 20, 64, WH, a, 'Bebas Neue')
    elif k == 1:
        c.set_source_rgb(0.05, 0.04, 0.03); c.paint(); radial(c, 540, 800, 700, (0.8, 0.6, 0.3), 0.15)
        a = ap(p, 0.0, 0.15)
        rr(c, 110, 480, 860, 820, 40); c.set_source_rgba(0.97, 0.95, 0.9, a); c.fill()
        label(c, "COUR D'APPEL DE PARIS", 540, 580, 52, (0.15, 0.12, 0.1), a, 'Bebas Neue')
        label(c, "21 MAI 2026", 540, 650, 40, (0.4, 0.3, 0.2), a)
        c.move_to(200, 700); c.line_to(880, 700); c.set_source_rgba(0.6, 0.5, 0.4, a); c.set_line_width(3); c.stroke()
        label(c, "AIR FRANCE ET AIRBUS", 540, 800, 66, (0.1, 0.1, 0.12), ap(p, 0.15, 0.3), 'Bebas Neue')
        label(c, "CONDAMNÉS POUR", 540, 880, 50, (0.3, 0.3, 0.32), ap(p, 0.3, 0.45), 'Bebas Neue')
        label(c, "HOMICIDES INVOLONTAIRES", 540, 970, 70, (0.75, 0.1, 0.1), ap(p, 0.45, 0.6), 'Bebas Neue')
        label(c, "225 000 € d'amende chacun (le maximum)", 540, 1070, 36, (0.3, 0.3, 0.32), ap(p, 0.6, 0.7))
        label(c, "Airbus s'est pourvu en cassation", 540, 1130, 32, (0.45, 0.45, 0.48), ap(p, 0.7, 0.8))
        sw = math.sin(min(1, since * 1.5) * math.pi) * 0.6
        c.save(); c.translate(540, 1230); c.rotate(-0.4 + sw)
        rr(c, -14, -100, 28, 120, 8); fill_stroke(c, (0.45, 0.28, 0.15), 5, a); rr(c, -70, -140, 140, 56, 20); fill_stroke(c, (0.55, 0.35, 0.18), 6, a); c.restore()
    else:
        memorial(c, t, min(1.0, since / 2.5))
        label(c, "TU CONNAISSAIS CETTE HISTOIRE ?", 540, 640, 86, WH, ap(since, 0.2, 0.8), 'Bebas Neue')


SC8 = {k[3:]: v for k, v in globals().items() if k.startswith('sc_') and callable(v)}
