"""Scènes v3 « cinéma » du 27/10 : SR-71 désintégré à Mach 3,2 (sb_*), Concorde AF4590 (co_*), MH370 (mh_*).
Signatures : vue stratosphérique + échelle d'altitude avec la limite d'Armstrong, rayons X de l'entrée d'air et de la combinaison pressurisée ;
rayons X du réservoir 5 au ralenti avec onde de choc dans le kérosène ; carte satellite de nuit avec les 7 arcs Inmarsat et la dérive du flaperon."""
import cairo, math, random
from sm_lib import *
from sm_scenes2 import ease, ap, sky, ORG, BLUE, RED, WH, GRN, jet
from sm_scenes6 import si, stamp, speedlines, eout, back, YEL
from sm_scenes7 import tag, label, mix, check, cross, clock, gauge, no_sign
from sm_scenes8 import night_sky, cloud_sea, ocean_night, a330, stick_head, deep_sea, memorial, AMB, CY
from sm_scenes4 import dc10
from sm_scenes3 import sr71 as sr71_top
R = None
SEPIA = (0.93, 0.82, 0.6)


# =============================================================== SR-71
def strato(c, t, curve_y=1380, clouds_on=True):
    g = cairo.LinearGradient(0, 0, 0, curve_y); g.add_color_stop_rgb(0, 0.0, 0.0, 0.02); g.add_color_stop_rgb(0.7, 0.02, 0.04, 0.14); g.add_color_stop_rgb(1, 0.1, 0.25, 0.6)
    c.set_source(g); c.paint()
    r = random.Random(3)
    for _ in range(260):
        x = r.random() * W; y = r.random() * curve_y * 0.85
        c.new_path(); c.arc(x, y, r.choice((0.8, 1.1, 1.6)), 0, 7); c.set_source_rgba(1, 1, 1, 0.2 + 0.6 * r.random()); c.fill()
    cx, cy, Rr = 540, curve_y + 3200, 3200
    g = cairo.RadialGradient(cx, cy, Rr - 10, cx, cy, Rr + 90); g.add_color_stop_rgba(0, 0.35, 0.7, 1, 0.9); g.add_color_stop_rgba(1, 0.35, 0.7, 1, 0); c.new_path(); c.arc(cx, cy, Rr + 90, 0, 7); c.set_source(g); c.fill()
    c.new_path(); c.arc(cx, cy, Rr, 0, 7)
    g = cairo.LinearGradient(0, curve_y, 0, H); g.add_color_stop_rgb(0, 0.12, 0.3, 0.55); g.add_color_stop_rgb(1, 0.05, 0.12, 0.25); c.set_source(g); c.fill()
    if clouds_on:
        c.save(); c.new_path(); c.arc(cx, cy, Rr, 0, 7); c.clip()
        rr_ = random.Random(8)
        for _ in range(60):
            x = (rr_.random() * W * 1.4 - t * 6) % (W * 1.4) - 150; y = curve_y + 30 + rr_.random() ** 1.5 * (H - curve_y); w = 40 + 140 * rr_.random() * (y - curve_y) / (H - curve_y + 1)
            c.save(); c.translate(x, y); c.scale(1, 0.3); c.new_path(); c.arc(0, 0, w, 0, 7); c.restore(); c.set_source_rgba(1, 1, 1, 0.35); c.fill()
        c.restore()


def sr71(c, x, y, rot, s, t, parts=0.0, ab=0.8, heat=0.0, dead_r=False):
    """SR-71 de profil (nez à droite). parts 0..1 : dislocation (morceaux qui s'écartent en tournant)."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    body = (0.13, 0.14, 0.17)
    def piece(dx, dy, rr0, fn):
        c.save(); c.translate(dx * parts * 230, dy * parts * 230); c.rotate(rr0 * parts * 0.9); fn(); c.restore()
    def tail():
        c.new_path(); c.move_to(-250, -18); c.line_to(-305, -120); c.line_to(-275, -120); c.line_to(-205, -22); c.close_path(); fill_stroke(c, body, 7)
        if ab > 0 and parts < 0.2:
            for k, (col, L) in enumerate((((1, 0.5, 0.15), 150), ((1, 0.8, 0.4), 95), ((0.6, 0.85, 1), 55))):
                c.new_path(); c.move_to(-330, 6); c.line_to(-330 - L * ab * (1 + 0.08 * math.sin(t * 30 + k)), 14); c.line_to(-330, 26); c.close_path(); c.set_source_rgba(*col, 0.85); c.fill()
            for d in range(4):
                c.new_path(); c.arc(-350 - d * 30, 16, 6, 0, 7); c.set_source_rgba(1, 1, 0.9, 0.7); c.fill()
    def nacelle():
        rr(c, -330, 2, 450, 34, 16); fill_stroke(c, mix(body, (0.3, 0.32, 0.36), 0.4), 7)
        c.new_path(); c.move_to(120, 6); c.line_to(178, 19); c.line_to(120, 32); c.close_path(); fill_stroke(c, (0.45, 0.47, 0.52), 5)
        if dead_r: c.new_path(); c.arc(-340, 19, 16, 0, 7); c.set_source_rgba(0.3, 0.3, 0.35, 0.8); c.fill()
    def fuse():
        c.new_path(); c.move_to(-330, -6); c.line_to(-330, 8); c.curve_to(-100, 14, 140, 6, 200, 0); c.line_to(200, -14); c.curve_to(120, -22, -100, -24, -330, -6); c.close_path(); fill_stroke(c, body, 8)
        c.move_to(-300, -2); c.curve_to(-100, 4, 100, 2, 200, -4); c.set_source_rgba(0.5, 0.55, 0.65, 0.5); c.set_line_width(3); c.stroke()
        if heat > 0:
            c.move_to(200, -14); c.curve_to(120, -22, -100, -24, -330, -6); c.set_source_rgba(1, 0.4, 0.2, 0.5 * heat); c.set_line_width(8); c.stroke()
    def nose():
        c.new_path(); c.move_to(200, -14); c.curve_to(260, -12, 320, -4, 360, 0); c.curve_to(320, 4, 260, 6, 200, 0); c.close_path(); fill_stroke(c, body, 7)
        for cx_ in (232, 192):
            c.new_path(); c.move_to(cx_ - 26, -12); c.curve_to(cx_ - 14, -26, cx_ + 10, -26, cx_ + 22, -13); c.close_path(); fill_stroke(c, (0.25, 0.35, 0.45), 5)
    piece(-0.9, -0.3, -0.8, tail)
    piece(-0.2, 0.9, 0.5, nacelle)
    piece(0.0, 0.0, 0.15, fuse)
    piece(1.0, -0.6, 1.4, nose)
    if 0 < parts < 1:                                          # nuages de vapeur / carburant aux cassures
        r_ = random.Random(11)
        for bx_, by_ in ((-220, -10), (190, -6), (-120, 20)):
            for j in range(7):
                a_ = r_.random() * 6.28; d_ = 30 + 90 * parts * r_.random()
                c.new_path(); c.arc(bx_ + math.cos(a_) * d_, by_ + math.sin(a_) * d_ * 0.6, (14 + 26 * r_.random()) * (0.4 + parts), 0, 7); c.set_source_rgba(0.9, 0.93, 1, 0.5 * (1 - parts)); c.fill()
    c.restore()


def suit_helmet(c, x, y, r, t, frost=0.0, mood='determined', look=(0, 0), visor=0.0):
    c.new_path(); c.arc(x, y, r * 1.45, 0, 7)
    g = cairo.RadialGradient(x - r * 0.5, y - r * 0.6, r * 0.2, x, y, r * 1.45); g.add_color_stop_rgb(0, 0.98, 0.98, 1); g.add_color_stop_rgb(1, 0.72, 0.74, 0.8); c.set_source(g); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(9); c.stroke()
    c.save(); c.new_path(); c.arc(x, y + r * 0.1, r * 1.05, 0, 7); c.clip()
    c.set_source_rgb(0.08, 0.1, 0.16); c.paint()
    head(c, x, y + r * 0.15, r * 0.85, mood, look, helmet=False)
    if visor > 0: c.set_source_rgba(0.95, 0.75, 0.2, 0.75 * visor); c.paint()
    if frost > 0:
        rr_ = random.Random(5)
        for _ in range(int(90 * frost)):
            c.new_path(); c.arc(x + rr_.uniform(-r, r), y + rr_.uniform(-r, r), 3 + 10 * rr_.random(), 0, 7); c.set_source_rgba(0.9, 0.96, 1, 0.55 * frost); c.fill()
        c.set_source_rgba(0.85, 0.92, 1, 0.45 * frost); c.paint()
    c.restore()
    c.new_path(); c.arc(x, y + r * 0.1, r * 1.05, 0, 7); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    c.new_path(); c.arc(x - r * 0.35, y - r * 0.4, r * 0.25, 3.6, 4.6); c.set_source_rgba(1, 1, 1, 0.7); c.set_line_width(6); c.stroke()


def suited_body(c, x, y, s, t, pose='fall', inflate=0.0, col=(0.82, 0.7, 0.42)):
    c.save(); c.translate(x, y); c.scale(s, s)
    k = 1 + 0.18 * inflate
    if pose == 'fall':
        arms = [[(-50, -40), (-130, -70), (-170, -120)], [(50, -40), (130, -60), (175, -100)]]; legs = [[(-30, 80), (-70, 170), (-90, 250)], [(30, 80), (80, 165), (100, 245)]]
    else:
        arms = [[(-50, -40), (-90, 40), (-80, 110)], [(50, -40), (90, 40), (80, 110)]]; legs = [[(-30, 80), (-35, 170), (-35, 250)], [(30, 80), (35, 170), (35, 250)]]
    for L in legs + arms:
        limb(c, [(px * k if abs(px) > 40 else px, py) for px, py in L], w=34 * k, col=col)
    rr(c, -70 * k, -80, 140 * k, 180, 50); fill_stroke(c, col, 9)
    c.move_to(-45 * k, -70); c.line_to(-30 * k, 90); c.move_to(45 * k, -70); c.line_to(30 * k, 90); c.set_source_rgba(*INK, 0.45); c.set_line_width(7); c.stroke()
    rr(c, -26, -10, 52, 40, 8); fill_stroke(c, (0.75, 0.77, 0.82), 4)
    c.move_to(0, -80); c.curve_to(40, -60, 40, -20, 18, -10); c.set_source_rgb(0.2, 0.22, 0.26); c.set_line_width(9); c.stroke()
    c.restore()


def alt_ladder(c, t, mark_km=24.0, armstrong=1.0, x0=200, y0=1380, y1=440):
    def Y(km): return y0 - (y0 - y1) * km / 26
    g = cairo.LinearGradient(0, y1, 0, y0); g.add_color_stop_rgb(0, 0.0, 0.0, 0.03); g.add_color_stop_rgb(1, 0.15, 0.35, 0.7); c.set_source(g); c.paint()
    if armstrong > 0:
        c.new_path(); c.rectangle(0, Y(26), W, Y(19) - Y(26)); c.set_source_rgba(1, 0.15, 0.15, 0.18 * armstrong); c.fill()
        c.move_to(0, Y(19)); c.line_to(W, Y(19)); c.set_source_rgba(1, 0.3, 0.3, 0.9 * armstrong); c.set_dash([18, 10]); c.set_line_width(5); c.stroke(); c.set_dash([])
        label(c, "LIMITE D'ARMSTRONG · 19 KM", 600, Y(19) - 20, 50, (1, 0.45, 0.4), armstrong, 'Bebas Neue')
        label(c, "au-dessus : le sang « bout »", 600, Y(19) + 46, 36, (1, 0.7, 0.65), armstrong)
    c.move_to(x0, y0); c.line_to(x0, y1); c.set_source_rgba(1, 1, 1, 0.6); c.set_line_width(4); c.stroke()
    for km in range(0, 27, 5):
        c.move_to(x0 - 14, Y(km)); c.line_to(x0 + 14, Y(km)); c.stroke()
        F(c, 28, 'Montserrat'); c.move_to(x0 - 120, Y(km) + 10); c.text_path(f"{km} km"); c.set_source_rgba(1, 1, 1, 0.7); c.fill()
    c.new_path(); c.move_to(x0 + 60, Y(0)); c.line_to(x0 + 160, Y(8.8)); c.line_to(x0 + 260, Y(0)); c.close_path(); fill_stroke(c, (0.45, 0.45, 0.5), 5)
    label(c, "EVEREST 8,8 KM", x0 + 420, Y(8.8) + 14, 46, WH, 1, 'Bebas Neue')
    c.save(); c.translate(x0 + 120, Y(11)); c.scale(0.25, 0.25); jet(c, 0, 0, 0, 1.0); c.restore()
    label(c, "AVIONS DE LIGNE 11 KM", x0 + 440, Y(11) + 14, 46, WH, 1, 'Bebas Neue')
    my = Y(mark_km)
    radial(c, x0, my, 60, YEL, 0.8); c.new_path(); c.arc(x0, my, 12, 0, 7); c.set_source_rgb(*YEL); c.fill()
    label(c, "WEAVER : 24 KM", x0 + 400, my + 16, 60, YEL, 1, 'Bebas Neue')


def mesa_land(c, t, sunset=True):
    sky(c, (0.25, 0.15, 0.4), (1.0, 0.55, 0.3)); radial(c, 760, 1060, 400, (1, 0.8, 0.4), 0.6)
    c.new_path(); c.arc(760, 1060, 90, 0, 7); c.set_source_rgb(1, 0.9, 0.6); c.fill()
    for k, (y, col) in enumerate(((1060, (0.45, 0.22, 0.25)), (1140, (0.55, 0.28, 0.2)))):
        c.new_path(); c.move_to(0, H)
        pts = [(0, y), (120, y), (150, y - 90 - 30 * k), (380, y - 90 - 30 * k), (410, y), (600, y), (640, y - 60), (860, y - 60), (890, y), (W, y)]
        for p_ in pts: c.line_to(*p_)
        c.line_to(W, H); c.close_path(); c.set_source_rgb(*col); c.fill()
    c.new_path(); c.rectangle(0, 1200, W, H); c.set_source_rgb(0.72, 0.5, 0.32); c.fill()
    r = random.Random(4)
    for _ in range(40):
        x = r.random() * W; y = 1220 + r.random() * 600; c.new_path(); c.arc(x, y, 8 + 10 * r.random(), 0, 7); c.set_source_rgb(0.45, 0.5, 0.3); c.fill()


def chute(c, x, y, s, k, t, col=(1, 1, 1), col2=(0.95, 0.4, 0.15)):
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    w = 260 * k; h = 140 * k
    for j in range(6):
        a0 = math.pi + j * math.pi / 6; a1 = a0 + math.pi / 6
        c.new_path(); c.move_to(0, 0); c.save(); c.scale(1, h / w); c.arc(0, 0, w, a0, a1); c.restore(); c.close_path(); c.set_source_rgb(*(col if j % 2 == 0 else col2)); c.fill()
    c.new_path(); c.save(); c.scale(1, h / w); c.arc(0, 0, w, math.pi, 2 * math.pi); c.restore(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    for j in range(7):
        a = math.pi + j * math.pi / 6; c.move_to(math.cos(a) * w, math.sin(a) * h); c.line_to(0, 300 * k)
    c.set_source_rgba(*INK, 0.7); c.set_line_width(3); c.stroke()
    c.restore()


def sc_sb_hook(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        strato(c, t, 1350)
        brk = ap(p, 0.65, 0.95)
        sr71(c, 540 + 30 * math.sin(t), 820, -0.02, 1.25, t, parts=brk, heat=0.6)
        if 0.6 < p < 0.75: c.set_source_rgba(1, 1, 1, (0.75 - p) * 5); c.paint()
        tag(c, "≈ 24 000 M · MACH 3,2", 540, 1280, YEL, ap(p, 0.1, 0.25), 60)
    elif k == 1:
        c.set_source_rgb(0.16, 0.12, 0.08); c.paint(); radial(c, 540, 900, 700, SEPIA, 0.25)
        for side in (60, W - 60):
            c.new_path(); c.rectangle(side - 40, 0, 80, H); c.set_source_rgb(0.05, 0.04, 0.03); c.fill()
            for j in range(14):
                yy = (j * 150 + t * 300) % (H + 150) - 75; rr(c, side - 18, yy, 36, 50, 8); c.set_source_rgb(0.85, 0.8, 0.7); c.fill()
        stamp(c, "1966", 540, 860, 240, SEPIA, since, glow=0.6); stamp(c, "HISTOIRE VRAIE", 540, 1040, 110, YEL, since - 0.25, glow=0.8)
    else:
        strato(c, t, 1450)
        speedlines(c, t, 0.6, horiz=False, n=26, seed=4)
        suited_body(c, 540, 980, 1.0, t, 'fall'); suit_helmet(c, 540, 820, 70, t, mood='worried')
        stamp(c, "SURVIVRAIS-TU ?", 540, 560, 140, RED, since, glow=1.0)


def sc_sb_jet(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        strato(c, t, 1400)
        sr71(c, 540, 860, 0, 1.45, t, heat=0.8)
        speedlines(c, t, 0.5)
        tag(c, "SR-71 BLACKBIRD", 540, 1260, WH, ap(p, 0.1, 0.25), 72)
        label(c, "le plus rapide des avions à réaction pilotés", 540, 1340, 34, (0.8, 0.85, 0.95), ap(p, 0.3, 0.5))
    else:
        c.set_source_rgb(0.03, 0.04, 0.07); c.paint(); radial(c, 540, 900, 600, (0.3, 0.4, 0.8), 0.2)
        names = (("BILL WEAVER", "PILOTE", YEL), ("JIM ZWAYER", "INGÉNIEUR", CY))
        for j, (nm, role, col) in enumerate(names):
            if j > k - 1: continue
            a = ap(t, sg['sent'][1 + j][0], sg['sent'][1 + j][0] + 0.3)
            x = 330 + j * 420
            c.push_group(); suited_body(c, x, 1170, 0.75, t, 'sit'); suit_helmet(c, x, 960, 85, t + j, mood='determined', look=(10 - 20 * j, 0)); c.pop_group_to_source(); c.paint_with_alpha(a)
            tag(c, nm, x, 640, col, a, 60); label(c, role, x, 700, 36, WH, a)


def inlet_xray(c, t, unstart=0.0):
    c.set_source_rgb(0.02, 0.05, 0.1); c.paint()
    for j in range(0, W, 60): c.move_to(j, 0); c.line_to(j, H)
    for j in range(0, H, 60): c.move_to(0, j); c.line_to(W, j)
    c.set_source_rgba(0.2, 0.6, 1, 0.07); c.set_line_width(1); c.stroke()
    cy = 880
    c.new_path(); c.move_to(1000, cy - 210); c.line_to(560, cy - 210); c.curve_to(380, cy - 210, 300, cy - 160, 120, cy - 150)
    c.move_to(1000, cy + 210); c.line_to(560, cy + 210); c.curve_to(380, cy + 210, 300, cy + 160, 120, cy + 150)
    c.set_source_rgb(*CY); c.set_line_width(6); c.stroke()
    sh = 40 * ap(unstart, 0.0, 0.3)
    c.new_path(); c.move_to(60 + sh, cy); c.line_to(460 + sh, cy - 90); c.line_to(700, cy - 90); c.line_to(700, cy + 90); c.line_to(460 + sh, cy + 90); c.close_path()
    c.set_source_rgba(*CY, 0.25); c.fill_preserve(); c.set_source_rgb(*CY); c.set_line_width(5); c.stroke()
    label(c, "CÔNE MOBILE", 360, cy + 10, 30, CY, 1, 'Bebas Neue')
    if unstart < 0.5:
        for sgn in (-1, 1):
            c.move_to(60, cy); c.line_to(140, cy + sgn * 150); c.set_source_rgba(1, 1, 1, 0.9); c.set_line_width(4); c.stroke()
        c.move_to(520, cy - 205); c.line_to(560, cy - 92); c.move_to(520, cy + 205); c.line_to(560, cy + 92); c.set_source_rgba(1, 1, 1, 0.6); c.stroke()
        for j in range(9):
            ph = (t * 1.6 + j / 9) % 1; xx = -100 + 1100 * ph; yy = cy - 160 + j * 40
            if 120 < xx < 1000 and abs(yy - cy) < 90: yy = cy + (110 if yy > cy else -110)
            c.move_to(xx - 60, yy); c.line_to(xx, yy); c.set_source_rgba(0.4, 1, 0.6, 0.8 * (1 - ph)); c.set_line_width(5); c.stroke()
        label(c, "ONDE DE CHOC À SA PLACE", 540, cy - 300, 40, WH, 1, 'Bebas Neue')
    else:
        q = ap(unstart, 0.5, 0.8)
        c.save(); c.translate(-260 * q, 0)
        for sgn in (-1, 1):
            c.move_to(130, cy - 230); c.curve_to(30, cy - 60, 30, cy + 60, 130, cy + 230)
        c.set_source_rgba(1, 0.35, 0.3, 0.95); c.set_line_width(8); c.stroke(); c.restore()
        r = random.Random(int(t * 10))
        for j in range(12):
            xx = 200 + 700 * r.random(); yy = cy + r.uniform(-180, 180); c.new_path(); c.arc(xx, yy, 18 + 20 * r.random(), 0, 7); c.set_source_rgba(1, 0.3, 0.25, 0.3); c.fill()
        label(c, "L'ONDE DE CHOC EST EXPULSÉE", 540, cy - 300, 40, RED, 1, 'Bebas Neue')


def sc_sb_unstart(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        c.set_source_rgb(0.03, 0.03, 0.05); c.paint(); radial(c, 540, 820, 600, YEL, 0.1)
        mach = 3.2 * eout(ap(p, 0.0, 0.6))
        gauge(c, 540, 820, 300, mach, 4, (0, 1, 2, 3, 4), col=YEL, unit="MACH")
        tag(c, "≈ 3 400 KM/H", 540, 1290, YEL, ap(p, 0.4, 0.6), 66)
    elif k == 1:
        inlet_xray(c, t, unstart=ap(p, 0.45, 0.75))
        tag(c, "ENTRÉE D'AIR (RAYONS X)", 540, 1285, CY, 1, 56)
        if p > 0.75: tag(c, "RÉACTEUR DROIT ÉTOUFFÉ", 540, 470, RED, ap(p, 0.75, 0.85), 50)
    else:
        strato(c, t, 1500, clouds_on=False)
        roll = 0.9 * math.sin(math.pi * ap(p, 0.0, 1.0)) ; pitch = -0.6 * ap(p, 0.2, 0.9)
        c.save(); c.translate(540, 860); c.rotate(pitch); c.scale(1, max(0.25, math.cos(roll))); sr71_top(c, 0, 0, 1.25, -math.pi / 2); c.restore()
        c.new_path(); c.arc(540, 860, 360, -2.2, -0.9); c.set_source_rgb(*ORG); c.set_line_width(10); c.stroke()
        tag(c, "ROULIS + CABRÉ", 540, 1285, ORG, ap(p, 0.1, 0.3), 66)


def sc_sb_break(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        c.set_source_rgb(0.04, 0.04, 0.06); c.paint(); radial(c, 540, 900, 600, RED, 0.12)
        d = ap(p, 0.1, 0.6)
        c.save(); c.translate(540, 1150); c.rotate(-0.5 * d)
        c.move_to(0, 0); c.line_to(0, -380); c.set_source_rgb(*INK); c.set_line_width(46); c.set_line_cap(1); c.stroke()
        c.move_to(0, 0); c.line_to(0, -380); c.set_source_rgb(0.3, 0.3, 0.33); c.set_line_width(30); c.stroke()
        rr(c, -55, -470, 110, 140, 40); fill_stroke(c, (0.15, 0.15, 0.17), 8); c.restore()
        c.new_path(); c.save(); c.translate(540, 1170); c.scale(1, 0.3); c.arc(0, 0, 160, 0, 7); c.restore(); c.set_source_rgb(0.08, 0.08, 0.1); c.fill()
        c.move_to(780, 760); c.line_to(880, 700); c.set_source_rgb(*YEL); c.set_line_width(12); c.set_line_cap(1); c.stroke(); c.move_to(845, 690); c.line_to(882, 699); c.line_to(860, 733); c.stroke()
        tag(c, "MANCHE À FOND", 540, 1285, YEL, ap(p, 0.3, 0.5), 66)
    elif k == 1:
        c.set_source_rgb(0.05, 0.0, 0.0); c.paint(); on = (t * 3) % 1 < 0.5
        if on: radial(c, 540, 900, 700, RED, 0.35)
        for j, (x, y) in enumerate(((330, 700), (750, 700), (330, 1060), (750, 1060))):
            c.new_path(); c.arc(x, y, 150, 0, 7); fill_stroke(c, (0.04, 0.04, 0.06), 8)
            a = t * (3 + j) + j; c.move_to(x, y); c.line_to(x + math.cos(a) * 120, y + math.sin(a) * 120); c.set_source_rgb(1, 1, 1); c.set_line_width(7); c.stroke()
        stamp(c, "RIEN NE RÉPOND", 540, 1340, 110, RED, since, glow=1.0)
    else:
        strato(c, t, 1400)
        brk = ap(p, 0.05, 0.85)
        sr71(c, 540, 860, -0.25 * brk, 1.35, t, parts=brk, ab=0.8 * (1 - brk), dead_r=True)
        if brk > 0.05:
            r = random.Random(7)
            for _ in range(40):
                a = r.random() * 6.28; d = 50 + 600 * brk * r.random()
                c.save(); c.translate(540 + math.cos(a) * d, 860 + math.sin(a) * d); c.rotate(t * 5 + a); c.new_path(); c.rectangle(-10, -4, 20, 8); c.set_source_rgb(0.2, 0.2, 0.24); c.fill(); c.restore()
        if 0.05 < p < 0.2: c.set_source_rgba(1, 1, 1, (0.2 - p) * 6); c.paint()
        sec = min(3.0, 3.0 * ap(p, 0.05, 0.85)); text(c, f"{sec:.1f} S".replace('.', ','), 540, 520, 140, RED, glow=0.9)


def sc_sb_out(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        c.set_source_rgb(0, 0, 0); c.paint()
        g = cairo.RadialGradient(540, 900, 50, 540, 900, 700 * (1 - ap(p, 0, 0.8)) + 60); g.add_color_stop_rgba(0, 0.4, 0.1, 0.1, 0.5); g.add_color_stop_rgba(1, 0, 0, 0, 1); c.set_source(g); c.paint()
        for j in range(3): c.new_path(); c.arc(500 + 40 * j, 900, 9, 0, 7); c.set_source_rgba(0.6, 0.6, 0.7, 0.4 + 0.6 * (int(t * 2.5) % 3 >= j)); c.fill()
    elif k == 1:
        c.set_source_rgb(0.95, 0.96, 1.0); c.paint(); radial(c, 540, 900, 700, (1, 1, 1), 0.8)
        c.push_group(); suited_body(c, 540, 1050, 0.7, t, 'fall'); suit_helmet(c, 540, 900, 55, t, frost=1.0, mood='neutral'); c.pop_group_to_source(); c.paint_with_alpha(0.55)
        label(c, "IL SE CROIT MORT", 540, 620, 80, (0.3, 0.32, 0.4), ap(p, 0.2, 0.5), 'Bebas Neue')
    else:
        strato(c, t, 1500)
        speedlines(c, t, 0.7, horiz=False, n=30, seed=9)
        r = random.Random(2)
        for j in range(8):
            x = 150 + r.random() * 780; y = (r.random() * 1200 - t * 80 * (0.5 + r.random())) % 1300 + 200
            c.save(); c.translate(x, y); c.rotate(t * (1 + j % 3) + j); rr(c, -40, -12, 80, 24, 6); c.set_source_rgb(0.15, 0.15, 0.18); c.fill(); c.restore()
        suited_body(c, 540, 1000, 0.95, t, 'fall'); suit_helmet(c, 540, 830, 68, t, frost=0.8, mood='worried')
        tag(c, "ARRACHÉ DE L'AVION", 540, 1285, YEL, ap(p, 0.2, 0.4), 62)


def sc_sb_suit(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k <= 1:
        c.set_source_rgb(0.02, 0.05, 0.1); c.paint()
        for j in range(0, W, 60): c.move_to(j, 0); c.line_to(j, H)
        for j in range(0, H, 60): c.move_to(0, j); c.line_to(W, j)
        c.set_source_rgba(0.2, 0.6, 1, 0.07); c.set_line_width(1); c.stroke()
        inf = ap(p, 0.1, 0.6) if k == 0 else 1.0
        c.push_group(); suited_body(c, 540, 1000, 1.2, t, 'sit', inflate=inf, col=(0.4, 0.8, 1.0)); c.pop_group_to_source(); c.paint_with_alpha(0.55)
        suited_body(c, 540, 1000, 1.08, t, 'sit', inflate=0, col=(0.95, 0.95, 1.0))
        suit_helmet(c, 540, 760, 90, t, frost=0.4, mood='neutral')
        rr(c, 760, 900, 90, 220, 40); fill_stroke(c, (0.3, 0.8, 0.5), 6)
        label(c, "O₂", 805, 1030, 40, INK, 1, 'Montserrat')
        if k == 1:
            for j in range(10):
                ph = (t * 0.8 + j / 10) % 1
                x = 805 - 200 * ph; y = 900 - 160 * ph - 40 * math.sin(ph * 3)
                c.new_path(); c.arc(x, y, 9, 0, 7); c.set_source_rgba(0.4, 1, 0.6, 0.9 * (1 - ph)); c.fill()
            tag(c, "OXYGÈNE", 540, 1285, GRN, 1, 66)
        else:
            tag(c, "COMBINAISON PRESSURISÉE", 540, 1285, CY, ap(p, 0.1, 0.3), 60)
            if inf > 0.3: label(c, "elle se gonfle", 540, 520, 54, CY, ap(p, 0.3, 0.5), 'Bebas Neue')
    else:
        alt_ladder(c, t, 24.0, armstrong=ap(p, 0.05, 0.3))
        for j in range(8):                                  # bulles (ébullition) dans la zone rouge
            ph = (t * 0.7 + j / 8) % 1; x = 260 + j * 90; y = 740 - 220 * ph
            c.new_path(); c.arc(x, y, 6 + 10 * ph, 0, 7); c.set_source_rgba(1, 0.5, 0.45, 0.7 * (1 - ph)); c.set_line_width(3); c.stroke()


def sc_sb_chute(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        alt = int(24000 - 19500 * ap(p, 0.0, 0.7)) // 100 * 100
        sky(c, mix((0.0, 0.0, 0.05), (0.35, 0.55, 0.9), ap(p, 0, 0.7)), mix((0.1, 0.25, 0.6), (0.8, 0.85, 0.95), ap(p, 0, 0.7)))
        speedlines(c, t, 0.6 * (1 - ap(p, 0.7, 0.8)), horiz=False, n=26, seed=4)
        op = ap(p, 0.7, 0.85)
        y = 980 - 120 * op
        chute(c, 540, y - 330, 1.2, op, t)
        suited_body(c, 540, y, 0.75, t, 'sit' if op > 0.5 else 'fall'); suit_helmet(c, 540, y - 150, 52, t, frost=0.3 * (1 - op), mood='neutral')
        rr(c, 300, 430, 480, 150, 30); c.set_source_rgba(0, 0, 0, 0.5); c.fill()
        text(c, f"{alt:,} M".replace(',', ' '), 540, 545, 110, YEL if op > 0 else WH, glow=0.5)
    else:
        mesa_land(c, t)
        q = ap(p, 0.0, 0.8)
        y = 600 + 560 * q
        chute(c, 420, y - 330, 1.0, 1.0 - 0.4 * ap(p, 0.8, 1.0), t)
        suited_body(c, 420, y, 0.6, t, 'sit'); suit_helmet(c, 420, y - 120, 42, t, mood='neutral')
        hx = 900 - 100 * p
        c.save(); c.translate(hx, 820); rr(c, -40, -18, 80, 36, 18); c.set_source_rgb(0.1, 0.08, 0.1); c.fill(); c.move_to(-110, -30); c.line_to(110, -30); c.set_source_rgb(0.1, 0.08, 0.1); c.set_line_width(4); c.stroke(); c.move_to(-40, 0); c.line_to(-100, -6); c.stroke(); c.restore()
        tag(c, "NOUVEAU-MEXIQUE", 540, 1285, WH, ap(p, 0.05, 0.2), 64)


def sc_sb_verdict(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        sky(c, (0.02, 0.08, 0.05), (0.01, 0.03, 0.02)); radial(c, 540, 900, 700, GRN, 0.15)
        suited_body(c, 540, 1180, 0.8, t, 'sit'); suit_helmet(c, 540, 960, 90, t, mood='neutral')
        stamp(c, "BILL WEAVER SURVIT", 540, 600, 110, GRN, since, glow=1.0)
    elif k == 1:
        sky(c, (0.04, 0.04, 0.06), (0.01, 0.01, 0.02))
        c.push_group(); suited_body(c, 540, 1180, 0.8, t, 'sit'); suit_helmet(c, 540, 960, 90, t + 1, mood='neutral'); c.pop_group_to_source(); c.paint_with_alpha(0.35)
        label(c, "JIM ZWAYER", 540, 620, 90, (0.85, 0.87, 0.92), ap(since, 0.0, 0.6), 'Bebas Neue')
        label(c, "n'a pas survécu", 540, 690, 46, (0.7, 0.72, 0.8), ap(since, 0.3, 0.9))
    else:
        strato(c, t, 1450)
        suited_body(c, 540, 1000, 1.0, t, 'fall'); suit_helmet(c, 540, 830, 70, t, mood='worried')
        stamp(c, "ET TOI ?", 540, 560, 170, ORG, since, glow=1.0)


# =============================================================== CONCORDE
def concorde(c, x, y, rot, s, t, gear=1.0, droop=0.4, fire=0.0, eng_bad=0.0):
    """Concorde de profil (nez à droite) : fuselage effilé, aile delta ogivale, nacelles, nez basculant, train haut."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    if fire > 0:                                              # traînée de feu sous l'aile gauche
        for k, (col, L, wd) in enumerate((((1, 0.35, 0.05), 620, 46), ((1, 0.6, 0.1), 460, 30), ((1, 0.9, 0.55), 250, 16))):
            c.new_path(); c.move_to(-40, 34)
            for j in range(0, 21):
                u_ = j / 20; xx = -40 - L * u_ * fire; yy = 34 + wd * math.sin(u_ * 3.14) * (1 + 0.25 * math.sin(t * 20 + j + k)) + 20 * u_
                c.line_to(xx, yy)
            for j in range(20, -1, -1):
                u_ = j / 20; xx = -40 - L * u_ * fire; yy = 34 - wd * 0.4 * math.sin(u_ * 3.14) + 20 * u_
                c.line_to(xx, yy)
            c.close_path(); c.set_source_rgba(*col, 0.85); c.fill()
        r = random.Random(int(t * 12))
        for j in range(10):
            c.new_path(); c.arc(-300 - 400 * r.random() * fire, 60 + 60 * r.random(), 20 + 30 * r.random(), 0, 7); c.set_source_rgba(0.2, 0.2, 0.22, 0.4); c.fill()
    if gear > 0:
        for gx, L in ((-40, 70), (210, 80)):
            c.move_to(gx, 10); c.line_to(gx, 10 + L * gear); c.set_source_rgb(*INK); c.set_line_width(9); c.stroke()
            for dx in (-14, 14):
                c.new_path(); c.arc(gx + dx, 16 + L * gear, 13 * gear + 1, 0, 7); fill_stroke(c, (0.1, 0.1, 0.12), 4)
    c.new_path(); c.move_to(-200, 8); c.line_to(60, 8); c.curve_to(120, 12, 170, 20, 190, 30); c.line_to(-210, 40); c.close_path(); fill_stroke(c, (0.82, 0.84, 0.9), 6)   # aile (vue de profil)
    for nx in (-150, -60):                                     # nacelles
        rr(c, nx, 26, 95, 30, 8); fill_stroke(c, mix((0.7, 0.72, 0.78), (0.3, 0.3, 0.32), eng_bad if nx == -150 else 0), 5)
        c.new_path(); c.rectangle(nx - 12, 30, 12, 22); c.set_source_rgb(0.15, 0.15, 0.18); c.fill()
    c.new_path(); c.move_to(-330, -6); c.curve_to(-200, -22, 200, -22, 300, -12); c.line_to(300, 12); c.curve_to(200, 14, -200, 14, -330, 6); c.close_path()
    g = cairo.LinearGradient(0, -22, 0, 14); g.add_color_stop_rgb(0, 1, 1, 1); g.add_color_stop_rgb(1, 0.72, 0.74, 0.8); c.set_source(g); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    for i in range(24): rr(c, -230 + i * 20, -10, 8, 9, 3); c.set_source_rgb(0.2, 0.3, 0.45); c.fill()
    c.save(); c.translate(300, 0); c.rotate(droop * 0.22)                      # nez basculant
    c.new_path(); c.move_to(0, -12); c.curve_to(60, -10, 120, -4, 170, 2); c.curve_to(120, 8, 60, 12, 0, 12); c.close_path(); fill_stroke(c, (0.96, 0.96, 0.98), 6)
    c.restore()
    c.new_path(); c.move_to(270, -14); c.line_to(300, -14); c.line_to(300, -6); c.line_to(262, -6); c.close_path(); c.set_source_rgb(0.15, 0.2, 0.3); c.fill()
    c.new_path(); c.move_to(-300, -10); c.line_to(-345, -120); c.line_to(-315, -120); c.line_to(-230, -14); c.close_path()   # dérive
    c.set_source_rgb(0.98, 0.98, 1); c.fill_preserve(); c.save(); c.clip()
    for k_, col in enumerate(((0.05, 0.15, 0.45), (0.98, 0.98, 1), (0.85, 0.12, 0.15))):
        c.new_path(); c.move_to(-360 + k_ * 22, -130); c.line_to(-338 + k_ * 22, -130); c.line_to(-260 + k_ * 22, -6); c.line_to(-282 + k_ * 22, -6); c.close_path(); c.set_source_rgb(*col); c.fill()
    c.restore(); c.new_path(); c.move_to(-300, -10); c.line_to(-345, -120); c.line_to(-315, -120); c.line_to(-230, -14); c.close_path(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    c.restore()


def concorde_top(c, x, y, s, t, xray=False, tank5=0.0, wave=0.0, crack=0.0, leak=0.0, fire=0.0, kevlar=0.0, frag=0.0):
    """Vue de dessus (nez vers le haut) ; en rayons X : réservoirs, train gauche, réservoir 5 (aile gauche, près du train)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    col = CY if xray else (0.95, 0.96, 0.98)
    def outline():
        c.new_path(); c.move_to(0, -560); c.curve_to(14, -500, 22, -380, 24, -200)
        c.curve_to(60, -120, 200, 40, 330, 300); c.line_to(330, 340); c.line_to(30, 330); c.line_to(22, 420); c.line_to(-22, 420); c.line_to(-30, 330)
        c.line_to(-330, 340); c.line_to(-330, 300); c.curve_to(-200, 40, -60, -120, -24, -200); c.curve_to(-22, -380, -14, -500, 0, -560); c.close_path()
    outline()
    if xray:
        c.set_source_rgba(*CY, 0.08); c.fill_preserve(); c.set_source_rgba(*CY, 0.9); c.set_line_width(4); c.stroke()
        for (px, py, w_, h_, nm) in ((-210, 150, 140, 120, None), (-110, 40, 70, 160, "5"), (110, 40, 70, 160, None), (210, 150, 140, 120, None), (-15, -150, 30, 260, None)):
            rr(c, px - w_ / 2, py - h_ / 2, w_, h_, 12)
            hl = tank5 if nm == "5" else 0
            c.set_source_rgba(*mix(CY, RED, hl), 0.15 + 0.3 * hl); c.fill_preserve(); c.set_source_rgba(*mix(CY, RED, hl), 0.9); c.set_line_width(3); c.stroke()
            if nm:
                c.move_to(px - w_ / 2, py - 30); c.line_to(-300, -40); c.set_source_rgba(*mix(CY, RED, hl), 0.8); c.set_line_width(3); c.stroke()
                label(c, "RÉSERVOIR 5", -330, -60, 44, mix(CY, RED, hl), 1, 'Bebas Neue')
            if nm and kevlar > 0:
                for j in range(8): c.move_to(px - w_ / 2, py - h_ / 2 + j * h_ / 8); c.line_to(px + w_ / 2, py - h_ / 2 + (j + 1) * h_ / 8)
                c.set_source_rgba(1, 0.85, 0.2, 0.8 * kevlar); c.set_line_width(3); c.stroke()
            if nm and wave > 0:
                c.save(); rr(c, px - w_ / 2, py - h_ / 2, w_, h_, 12); c.clip()
                for j in range(4):
                    ph = (wave * 2 + j * 0.25) % 1; c.new_path(); c.arc(px - 20, py + 60, 10 + 160 * ph, 0, 7); c.set_source_rgba(1, 0.6, 0.3, 0.9 * (1 - ph)); c.set_line_width(5); c.stroke()
                c.restore()
            if nm and crack > 0:
                c.move_to(px - 30, py + 70)
                for j in range(5): c.line_to(px - 30 + random.Random(j).uniform(-25, 25), py + 70 - j * 25 * crack)
                c.set_source_rgb(1, 1, 1); c.set_line_width(4); c.stroke()
            if nm and leak > 0:
                for j in range(30):
                    ph = (t * 1.2 + j / 30) % 1; xx = px - 30 + 20 * math.sin(j); yy = py + 80 + 500 * ph * leak
                    cc = mix((0.9, 0.85, 0.5), (1, 0.4, 0.1), fire)
                    if fire > 0: radial(c, xx + 30 * ph * math.sin(j * 2), yy, 40 + 40 * ph, (1, 0.45, 0.1), 0.45 * fire * (1 - ph))
                    c.new_path(); c.arc(xx + 30 * ph * math.sin(j * 2), yy, 6 + 22 * ph * (1 + fire), 0, 7); c.set_source_rgba(*cc, (0.8 if fire else 0.5) * (1 - ph)); c.fill()
        c.new_path(); c.arc(-110, 150, 26, 0, 7); c.set_source_rgba(1, 1, 1, 0.9); c.set_line_width(4); c.stroke()   # train gauche
        c.move_to(-130, 170); c.line_to(-300, 410); c.set_source_rgba(1, 1, 1, 0.7); c.set_line_width(3); c.stroke()
        label(c, "TRAIN GAUCHE", -300, 445, 40, WH, 1, 'Bebas Neue')
        if frag > 0:
            fx = -110 + (0) * frag; fy = 150 - 70 * frag
            c.save(); c.translate(fx, fy); c.rotate(t * 8); rr(c, -14, -8, 28, 16, 4); c.set_source_rgb(0.1, 0.1, 0.1); c.fill_preserve(); c.set_source_rgb(1, 0.85, 0.3); c.set_line_width(3); c.stroke(); c.restore()
            c.move_to(-110, 150); c.line_to(fx, fy); c.set_source_rgba(1, 0.85, 0.3, 0.5); c.set_dash([6, 6]); c.set_line_width(3); c.stroke(); c.set_dash([])
    else:
        c.set_source_rgb(*col); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    c.restore()


def runway(c, t, scroll=0.0, strip=True, dusk=False):
    sky(c, (0.4, 0.6, 0.9), (0.85, 0.85, 0.8)) if not dusk else sky(c, (0.3, 0.4, 0.7), (0.95, 0.75, 0.55))
    c.new_path(); c.rectangle(0, 0, W, H); c.set_source_rgb(0.32, 0.45, 0.25); c.fill()
    c.new_path(); c.rectangle(300, 0, 480, H); c.set_source_rgb(0.28, 0.28, 0.3); c.fill()
    for j in range(14):
        yy = (j * 160 + scroll) % (H + 160) - 80; c.new_path(); c.rectangle(530, yy, 20, 90); c.set_source_rgb(0.95, 0.95, 0.9); c.fill()
    for j in range(24):
        yy = (j * 90 + scroll) % (H + 90) - 45
        for xx in (310, 770): c.new_path(); c.arc(xx, yy, 5, 0, 7); c.set_source_rgb(1, 0.95, 0.7); c.fill()
    if strip:
        sy = (900 + scroll * 0) % H
        c.save(); c.translate(470, 1000); c.rotate(0.3); rr(c, -60, -6, 120, 12, 3); c.set_source_rgb(0.85, 0.87, 0.92); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2); c.stroke(); c.restore()
        radial(c, 470, 1000, 60, (1, 1, 0.9), 0.5)


def gonesse_map(c, t, prog=1.0):
    c.set_source_rgb(0.08, 0.1, 0.12); c.paint()
    r = random.Random(3)
    for _ in range(160):
        x = r.random() * W; y = 380 + r.random() * 1050; c.new_path(); c.rectangle(x, y, 8 + 20 * r.random(), 8 + 20 * r.random()); c.set_source_rgba(0.2, 0.22, 0.25, 0.7); c.fill()
    for j in range(4):
        y0 = 560 + j * 70 + (40 if j > 1 else 0)
        c.save(); c.translate(760, y0); c.rotate(-0.05); rr(c, -230, -10, 460, 20, 6); c.set_source_rgb(0.5, 0.52, 0.56); c.fill(); c.restore()
    label(c, "ROISSY-CDG", 760, 500, 44, WH, 1, 'Bebas Neue')
    gx, gy = 260, 1180
    c.new_path(); c.arc(gx, gy, 120, 0, 7); c.set_source_rgba(0.6, 0.62, 0.66, 0.25); c.fill()
    label(c, "GONESSE", gx, gy - 140, 46, WH, 1, 'Bebas Neue')
    p0 = (980, 640); pc = (600, 700); p1 = (gx + 40, gy - 20)
    n = 50; m = int(n * prog)
    c.move_to(*p0)
    for j in range(1, m + 1):
        u_ = j / n; c.line_to((1 - u_) ** 2 * p0[0] + 2 * (1 - u_) * u_ * pc[0] + u_ * u_ * p1[0], (1 - u_) ** 2 * p0[1] + 2 * (1 - u_) * u_ * pc[1] + u_ * u_ * p1[1])
    c.set_source_rgba(1, 0.45, 0.3, 0.9); c.set_line_width(6); c.set_dash([16, 10]); c.stroke(); c.set_dash([])
    if prog >= 1:
        c.new_path(); c.arc(p1[0], p1[1], 16, 0, 7); c.set_source_rgb(*RED); c.fill()


def sc_co_hook(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    c.set_source_rgb(0.18, 0.18, 0.2); c.paint()
    r = random.Random(1)
    for _ in range(500):
        c.new_path(); c.arc(r.random() * W, r.random() * H, 1 + 2 * r.random(), 0, 7); c.set_source_rgba(1, 1, 1, 0.05 + 0.08 * r.random()); c.fill()
    c.save(); c.translate(540, 980); c.rotate(-0.12); sc_ = 1 + 0.08 * p
    c.scale(sc_, sc_)
    rr(c, -380, -26, 760, 52, 8)
    g = cairo.LinearGradient(0, -26, 0, 26); g.add_color_stop_rgb(0, 0.92, 0.93, 0.96); g.add_color_stop_rgb(0.5, 0.65, 0.67, 0.72); g.add_color_stop_rgb(1, 0.5, 0.52, 0.58); c.set_source(g); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    for j in range(6): c.new_path(); c.arc(-330 + j * 130, 0, 6, 0, 7); c.set_source_rgb(0.3, 0.3, 0.35); c.fill()
    gl = (t * 0.8) % 1; c.new_path(); c.rectangle(-380 + 760 * gl, -26, 40, 52); c.set_source_rgba(1, 1, 1, 0.4); c.fill()
    c.restore()
    c.move_to(160, 1110); c.line_to(920, 1020); c.set_source_rgb(*YEL); c.set_line_width(5); c.stroke()
    for xx, yy in ((160, 1110), (920, 1020)): c.move_to(xx, yy - 20); c.line_to(xx, yy + 20); c.stroke()
    tag(c, "43 CM", 540, 1180, YEL, ap(p, 0.2, 0.35), 80)
    if p > 0.5:
        a = ap(p, 0.5, 1.0)
        c.push_group(); concorde(c, 1400 - 1300 * a, 620, -0.05, 1.3, t, gear=1.0, droop=0.4); c.pop_group_to_source(); c.paint_with_alpha(0.9)


def sc_co_dc10(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        gonesse_map(c, t, prog=0.0)
        tag(c, "25 JUILLET 2000 · 16:42", 540, 1285, AMB, ap(p, 0.1, 0.3), 60)
    elif k == 1:
        sky(c, (0.35, 0.55, 0.88), (0.95, 0.85, 0.7))
        c.new_path(); c.rectangle(0, 1150, W, H); c.set_source_rgb(0.32, 0.45, 0.25); c.fill(); c.new_path(); c.rectangle(0, 1150, W, 40); c.set_source_rgb(0.3, 0.3, 0.32); c.fill()
        lift = ap(p, 0.3, 1.0)
        dc10(c, 200 + 600 * p, 1110 - 300 * lift, -0.15 * lift, 1.0)
        tag(c, "4 MIN AVANT : UN DC-10", 540, 520, WH, ap(p, 0.05, 0.2), 60)
    else:
        sky(c, (0.35, 0.55, 0.88), (0.95, 0.85, 0.7))
        c.new_path(); c.rectangle(0, 1150, W, H); c.set_source_rgb(0.32, 0.45, 0.25); c.fill(); c.new_path(); c.rectangle(0, 1150, W, 40); c.set_source_rgb(0.3, 0.3, 0.32); c.fill()
        dc10(c, 600 + 140 * p, 700 - 120 * p, -0.15, 1.0)
        q = ap(p, 0.05, 0.6)
        sx = 560 - 120 * q; sy = 760 + 410 * q ** 1.6
        c.save(); c.translate(sx, sy); c.rotate(t * 6 * (1 - ap(p, 0.6, 0.7))); rr(c, -40, -5, 80, 10, 3); c.set_source_rgb(0.9, 0.92, 0.96); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2); c.stroke(); c.restore()
        c.new_path(); c.arc(sx, sy, 60, 0, 7); c.set_source_rgba(*YEL, 0.9); c.set_line_width(5); c.stroke()
        tag(c, "LAMELLE DE TITANE", 540, 1285, YEL, ap(p, 0.3, 0.5), 60)


def sc_co_roll(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k <= 1:
        sky(c, (0.35, 0.55, 0.88), (0.95, 0.85, 0.7))
        c.new_path(); c.rectangle(0, 1150, W, H); c.set_source_rgb(0.32, 0.45, 0.25); c.fill(); c.new_path(); c.rectangle(0, 1150, W, 40); c.set_source_rgb(0.3, 0.3, 0.32); c.fill()
        for j in range(16):
            x = (j * 120 - t * 1400) % (W + 200) - 100; c.new_path(); c.rectangle(x, 1165, 60, 8); c.set_source_rgb(0.95, 0.95, 0.9); c.fill()
        speedlines(c, t, 0.7)
        if k == 0:
            concorde(c, 480, 1040, 0, 1.05, t, gear=1.0, droop=0.5)
            v = int(300 * ap(p, 0.0, 0.9)); tag(c, f"{v} KM/H", 540, 560, YEL, 1, 90)
        else:
            c.save(); c.translate(540, 900); c.scale(2.2, 2.2); c.translate(-540, -900)
            concorde(c, 600, 900, 0, 1.25, t, gear=1.0, droop=0.5); c.restore()
            qx = 1000 - 440 * ap(p, 0.05, 0.85); c.save(); c.translate(qx, 1168); c.rotate(0.25); rr(c, -70, -7, 140, 14, 3); c.set_source_rgb(0.92, 0.94, 0.98); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(3); c.stroke(); c.restore()
            c.new_path(); c.arc(qx, 1168, 95, 0, 7); c.set_source_rgba(*YEL, 0.9); c.set_line_width(6); c.stroke()
            if p > 0.85:
                r_ = random.Random(int(t * 20))
                for j in range(14): a_ = r_.uniform(3.4, 6.0); d_ = r_.uniform(20, 110); c.move_to(qx, 1150); c.line_to(qx + math.cos(a_) * d_, 1150 + math.sin(a_) * d_); c.set_source_rgba(1, 0.85, 0.4, 0.9); c.set_line_width(4); c.stroke()
            tag(c, "LA ROUE PASSE DESSUS", 540, 560, WH, ap(p, 0.4, 0.55), 64)
    else:
        c.set_source_rgb(0.05, 0.04, 0.04); c.paint()
        fl = max(0, 1 - since / 0.25); c.set_source_rgba(1, 0.9, 0.7, 0.9 * fl); c.paint()
        x, y = 540, 980
        c.new_path(); c.arc(x, y, 170, 0, 7); fill_stroke(c, (0.1, 0.1, 0.12), 10)
        c.new_path(); c.arc(x, y, 80, 0, 7); fill_stroke(c, (0.65, 0.67, 0.72), 8)
        r = random.Random(4)
        for j in range(26):
            a = r.random() * 6.28; d = 170 + 600 * eout(since / 0.9) * (0.4 + 0.6 * r.random())
            c.save(); c.translate(x + math.cos(a) * d, y + math.sin(a) * d); c.rotate(a + since * 6); rr(c, -22, -9, 44, 18, 4); c.set_source_rgb(0.08, 0.08, 0.09); c.fill(); c.restore()
        stamp(c, "BANG", 540, 600, 200, RED, since, glow=1.0)
        label(c, "RALENTI ×1000", 540, 1340, 40, WH, 1, 'Bebas Neue')


def sc_co_tank(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    c.set_source_rgb(0.02, 0.05, 0.1); c.paint()
    for j in range(0, W, 60): c.move_to(j, 0); c.line_to(j, H)
    for j in range(0, H, 60): c.move_to(0, j); c.line_to(W, j)
    c.set_source_rgba(0.2, 0.6, 1, 0.07); c.set_line_width(1); c.stroke()
    if k == 0:
        concorde_top(c, 540, 790, 0.95, t, xray=True, tank5=ap(p, 0.7, 0.9), frag=ap(p, 0.2, 0.9))
        tag(c, "4,5 KG · ≈ 500 KM/H", 540, 1285, YEL, ap(p, 0.1, 0.3), 60)
        label(c, "RAYONS X", 250, 520, 46, CY, 1, 'Bebas Neue'); label(c, "VUE DE DESSUS", 250, 570, 34, CY, 0.8, 'Bebas Neue')
    elif k == 1:
        concorde_top(c, 540, 790, 0.95, t, xray=True, tank5=1.0, wave=(since * 0.8) % 1, crack=ap(p, 0.4, 0.8))
        tag(c, "ONDE DE CHOC DANS LE KÉROSÈNE", 540, 1285, ORG, 1, 52)
    else:
        concorde_top(c, 540, 790, 0.95, t, xray=True, tank5=1.0, crack=1.0, leak=ap(p, 0.0, 0.4), fire=ap(p, 0.3, 0.6))
        tag(c, "LE KÉROSÈNE S'ENFLAMME", 540, 1285, RED, ap(p, 0.3, 0.45), 60)


def sc_co_fire(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        sky(c, (0.35, 0.55, 0.88), (0.95, 0.85, 0.7))
        c.new_path(); c.rectangle(0, 1250, W, H); c.set_source_rgb(0.32, 0.45, 0.25); c.fill()
        lift = ap(p, 0.2, 1.0)
        concorde(c, 480, 1080 - 260 * lift, -0.18 * lift, 1.05, t, gear=1.0, droop=0.5, fire=ap(p, 0.0, 0.3))
        tag(c, "TROP TARD POUR FREINER", 540, 520, RED, ap(p, 0.05, 0.2), 64)
    elif k == 1:
        c.set_source_rgb(0.04, 0.04, 0.06); c.paint()
        for j in range(4):
            x = 200 + j * 230; lvl = 0.92 - (0.55 * ap(p, 0.1, 0.6) if j < 2 else 0) + 0.02 * math.sin(t * 7 + j)
            rr(c, x - 60, 560, 120, 600, 20); c.set_source_rgb(0.1, 0.1, 0.12); c.fill()
            rr(c, x - 50, 570 + 580 * (1 - lvl), 100, 580 * lvl, 14); c.set_source_rgb(*(RED if j < 2 and p > 0.3 else GRN)); c.fill()
            label(c, f"MOTEUR {j + 1}", x, 1220, 40, WH, 1, 'Bebas Neue')
        tag(c, "MOTEURS 1 ET 2 : PUISSANCE PERDUE", 540, 1285, RED, ap(p, 0.3, 0.5), 50)
    else:
        sky(c, (0.4, 0.55, 0.8), (0.9, 0.75, 0.55))
        concorde(c, 470, 900, -0.12, 1.1, t, gear=1.0, droop=0.5, fire=1.0)
        gx_, gy_ = -40 * 1.1, 80 * 1.1; ca, sa = math.cos(-0.12), math.sin(-0.12)
        cxg, cyg = 470 + gx_ * ca - gy_ * sa, 900 + gx_ * sa + gy_ * ca
        c.new_path(); c.arc(cxg, cyg, 110 + 8 * math.sin(t * 6), 0, 7); c.set_source_rgba(*RED, 0.9); c.set_line_width(8); c.stroke()
        tag(c, "LE TRAIN NE REMONTE PAS", 540, 1285, RED, ap(p, 0.2, 0.4), 60)


def sc_co_crash(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        sky(c, (0.4, 0.55, 0.8), (0.9, 0.75, 0.55))
        c.new_path(); c.rectangle(0, 1300, W, H); c.set_source_rgb(0.35, 0.4, 0.32); c.fill()
        concorde(c, 470, 860 + 60 * p, -0.25, 1.05, t, gear=1.0, droop=0.5, fire=1.0, eng_bad=1.0)
        v = int(370 - 30 * ap(p, 0, 1)); tag(c, "VITESSE TROP FAIBLE", 540, 520, ORG, ap(p, 0.1, 0.3), 60)
    elif k == 1:
        gonesse_map(c, t, prog=ap(p, 0.0, 0.8))
        if p > 0.8: tag(c, "≈ 2 MIN APRÈS LE DÉCOLLAGE", 540, 1285, WH, ap(p, 0.8, 0.9), 54)
    else:
        c.set_source_rgb(0.02, 0.02, 0.03); c.paint()
        label(c, "113 VICTIMES", 540, 840, 110, (0.92, 0.93, 0.96), min(1, since / 0.8), 'Bebas Neue')
        label(c, "109 à bord · 4 au sol", 540, 920, 44, (0.7, 0.72, 0.78), min(1, max(0, since - 0.4) / 0.8))


def sc_co_after(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        c.set_source_rgb(0.02, 0.05, 0.1); c.paint()
        concorde_top(c, 540, 790, 0.95, t, xray=True, tank5=0.3, kevlar=ap(p, 0.1, 0.5))
        tag(c, "KEVLAR + PNEUS RENFORCÉS", 540, 1285, YEL, ap(p, 0.3, 0.5), 58)
    elif k == 1:
        sky(c, (0.25, 0.35, 0.7), (1.0, 0.7, 0.45)); radial(c, 780, 1000, 400, (1, 0.8, 0.5), 0.5)
        concorde(c, 380 + 160 * p, 900 - 100 * p, -0.08, 1.0, t, gear=0, droop=0.0)
        tag(c, "NOVEMBRE 2001 : IL REVOLE", 540, 1285, GRN, ap(p, 0.1, 0.3), 58)
    elif k == 2:
        c.set_source_rgb(0.03, 0.03, 0.05); c.paint()
        dim = 1 - 0.6 * ap(p, 0.4, 1.0)
        radial(c, 540, 600, 700, (1, 0.95, 0.8), 0.3 * dim)
        c.push_group(); concorde(c, 480, 1000, 0, 1.05, t, gear=1.0, droop=0.0); c.pop_group_to_source(); c.paint_with_alpha(0.4 + 0.6 * dim)
        tag(c, "2003 : RETIRÉ POUR TOUJOURS", 540, 520, WH, ap(p, 0.1, 0.3), 58)
    else:
        sky(c, (0.15, 0.1, 0.3), (1.0, 0.55, 0.3)); radial(c, 540, 1100, 500, (1, 0.8, 0.4), 0.6)
        concorde(c, 480, 860, -0.05, 1.0, t, gear=0, droop=0.0)
        label(c, "TU TE SOUVIENS DU CONCORDE ?", 540, 600, 70, WH, ap(since, 0.2, 0.7), 'Bebas Neue')


# =============================================================== MH370
LON0, LON1, LAT0, LAT1 = 40.0, 125.0, 25.0, -45.0
def P(lon, lat): return 40 + (lon - LON0) / (LON1 - LON0) * 1000, 380 + (LAT0 - lat) / (LAT0 - LAT1) * 1000

LANDS = [
    [(20, 25), (35, 25), (43.5, 12.5), (51.2, 11.8), (49, 8), (47, 4), (42, -1.5), (39.7, -5), (40, -10.5), (40.6, -15), (36, -20), (34, -25), (31, -30), (20, -35)],
    [(35, 25), (55, 25.5), (56.5, 24), (59.8, 22.5), (57.5, 19), (55, 17.5), (52, 16), (45, 13), (43, 12.8), (38, 22)],
    [(49.3, -12), (50.4, -15.5), (49.8, -17), (48.5, -20), (47.1, -24.8), (45.2, -25.5), (43.7, -23.5), (43.3, -21.5), (44, -17), (46, -15.5), (48, -13.5)],
    [(66.5, 25), (68.8, 23.5), (70, 21), (72.8, 19), (73.5, 16), (74.8, 13), (76.3, 9.5), (77.5, 8.1), (78.2, 9), (79.8, 10.3), (80.2, 13), (81, 16), (83, 17.5), (86.5, 20), (88, 22), (90, 22), (92, 21), (92.5, 25)],
    [(79.8, 9.8), (81.2, 8.5), (81.8, 7), (81, 6), (80, 6.2), (79.8, 8)],
    [(92.5, 25), (92.3, 20.5), (94, 18), (94.4, 16), (97.6, 16.5), (98.5, 13), (98.3, 10), (98.6, 8), (100.2, 6.5), (100.4, 5.2), (101.2, 2.8), (103.4, 1.3), (104.2, 1.4), (103.5, 4), (103.4, 5.4), (102.3, 6.2), (100.6, 7.2), (100, 9), (99.2, 10.5), (100, 13.4), (100.9, 12.7), (102.3, 12.1), (103, 11), (104.8, 10.5), (105.3, 8.8), (106.7, 10.4), (109, 11.7), (109.3, 13.3), (108.8, 15.3), (106.7, 17.4), (106, 19.5), (107.7, 21.5), (110, 21.4), (114, 22.3), (117, 23.2), (120, 25)],
    [(95.3, 5.6), (97.5, 5.2), (100.4, 2.2), (103.8, -1), (106, -3), (106, -5.8), (104.5, -5.9), (102.3, -4), (100.9, -2), (99, 0.2), (97.5, 2)],
    [(105.2, -6.8), (106.5, -6), (108.3, -6.3), (110.4, -6.9), (112.6, -6.9), (114.6, -7.7), (114.4, -8.7), (111, -8.2), (108.3, -7.8), (106.5, -7.4)],
    [(109, 1.5), (109.7, -1), (110.5, -3), (114.5, -3.8), (116.5, -2.5), (117.6, 1), (118.9, 5), (117, 7), (115.4, 5), (113, 3.2), (111, 1.7)],
    [(113.5, -22), (114.2, -26), (113.5, -26.5), (114.9, -29.5), (115, -33.5), (116, -34.9), (118, -35), (123, -34), (126, -33.5), (126, -14), (121, -19), (116, -20.7), (114, -21.8)],
]
KL = (101.7, 2.75); IGARI = (103.58, 6.93); PENANG = (100.3, 5.3); LASTR = (97.4, 6.9); SAT = (64.5, 0.0); REUNION = (55.5, -21.1)
ARCS = [33.0, 35.0, 37.0, 39.0, 41.0, 43.0, 44.5]


def zoomed(c, lon, lat, z):
    px, py = P(lon, lat); c.translate(540, 880); c.scale(z, z); c.translate(-px, -py)


def ZS(lon, lat, V):
    px, py = P(V[0], V[1]); x, y = P(lon, lat); return 540 + (x - px) * V[2], 880 + (y - py) * V[2]


def io_map(c, t, glow=1.0, labels=True, z=1.0):
    c.set_source_rgb(0.01, 0.02, 0.05); c.paint()
    g = cairo.LinearGradient(0, 380, 0, 1380); g.add_color_stop_rgb(0, 0.02, 0.05, 0.12); g.add_color_stop_rgb(1, 0.01, 0.03, 0.08); c.rectangle(-2000, 380, 6000, 1000); c.set_source(g); c.fill()
    for lo in range(40, 126, 10 if z < 1.8 else 5):
        x, _ = P(lo, 0); c.move_to(x, 380); c.line_to(x, 1380)
    for la in range(25, -46, -10 if z < 1.8 else -5):
        _, y = P(0, la); c.move_to(-2000, y); c.line_to(4000, y)
    c.set_source_rgba(0.3, 0.6, 1, 0.08); c.set_line_width(1.2 / z); c.stroke()
    for poly in LANDS:
        c.new_path(); c.move_to(*P(*poly[0]))
        for q in poly[1:]: c.line_to(*P(*q))
        c.close_path(); c.set_source_rgb(0.06, 0.09, 0.1); c.fill_preserve(); c.set_source_rgba(0.35, 0.75, 1, 0.55 * glow); c.set_line_width(2.6 / z); c.stroke()
    r = random.Random(4)
    for (lo, la, n) in ((101.7, 3.0, 40), (100.5, 13.7, 40), (106.8, -6.2, 50), (77, 13, 60), (72.8, 19, 40), (115.8, -31.9, 20), (55.5, 25, 20), (100.3, 5.4, 15), (98.7, 3.6, 15)):
        x, y = P(lo, la)
        for _ in range(n):
            c.new_path(); c.arc(x + r.gauss(0, 14) / max(1, z * 0.6), y + r.gauss(0, 10) / max(1, z * 0.6), (1 + 1.5 * r.random()) / max(1, z * 0.7), 0, 7); c.set_source_rgba(1, 0.8, 0.45, 0.6 * r.random() + 0.2); c.fill()
    for y0, y1 in ((380, 470), (1380, 1290)):                 # fondu haut / bas de la bande carte
        g = cairo.LinearGradient(0, y0, 0, y1); g.add_color_stop_rgba(0, 0.01, 0.02, 0.05, 1); g.add_color_stop_rgba(1, 0.01, 0.02, 0.05, 0)
        c.rectangle(-2000, min(y0, y1), 6000, abs(y1 - y0)); c.set_source(g); c.fill()
    if labels:
        for nm, (lo, la) in (("MALAISIE", (101.5, 5.6)), ("OCÉAN INDIEN", (75, -15)), ("AUSTRALIE", (120, -26)), ("INDE", (78, 19)), ("SUMATRA", (100.5, -1.2))):
            x, y = P(lo, la); label(c, nm, x, y, 40 / z, (0.55, 0.7, 0.85), 0.9, 'Bebas Neue')


def path_pts(prog):
    pts = [KL, IGARI, (101.9, 6.4), PENANG, (98.6, 6.2), LASTR]
    seg = []
    for a, b in zip(pts, pts[1:]): seg.append((a, b, math.hypot(b[0] - a[0], b[1] - a[1])))
    tot = sum(s_[2] for s_ in seg); d = tot * prog; out = [P(*pts[0])]
    for a, b, L in seg:
        if d >= L: out.append(P(*b)); d -= L
        else:
            out.append(P(a[0] + (b[0] - a[0]) * d / L, a[1] + (b[1] - a[1]) * d / L)); break
    return out
IG_FRAC = 4.58 / 11.68


def draw_route(c, prog, z=1.0, a=1.0):
    pts = path_pts(prog)
    civ = [q for q in path_pts(min(prog, IG_FRAC))]
    c.move_to(*civ[0])
    for q in civ[1:]: c.line_to(*q)
    c.set_source_rgba(1, 1, 1, 0.9 * a); c.set_line_width(5 / z); c.stroke()
    if prog > IG_FRAC:
        mil = [P(*IGARI)] + pts[2:]
        c.move_to(*mil[0])
        for q in mil[1:]: c.line_to(*q)
        c.set_source_rgba(*AMB, a); c.set_line_width(6 / z); c.set_dash([14 / z, 9 / z]); c.stroke(); c.set_dash([])
    return pts[-1]


def arc_path(c, rdeg, a0=-100, a1=70):
    sx, sy = P(*SAT); kx = 1000 / (LON1 - LON0); ky = 1000 / (LAT0 - LAT1)
    c.new_path()
    for j in range(0, 61):
        a = math.radians(a0 + (a1 - a0) * j / 60)
        x = sx + math.cos(a) * rdeg * kx; y = sy - math.sin(a) * rdeg * ky
        if j == 0: c.move_to(x, y)
        else: c.line_to(x, y)


def arc_pt(rdeg, adeg):
    sx, sy = P(*SAT); kx = 1000 / (LON1 - LON0); ky = 1000 / (LAT0 - LAT1); a = math.radians(adeg)
    return sx + math.cos(a) * rdeg * kx, sy - math.sin(a) * rdeg * ky


def radar_atc(c, x, y, r, t, block=1.0, blip=1.0, mil=False):
    col = (1, 0.7, 0.2) if mil else (0.3, 1, 0.5)
    c.new_path(); c.arc(x, y, r, 0, 7); c.set_source_rgb(0.01, 0.03, 0.02); c.fill()
    for k in range(1, 5):
        c.new_path(); c.arc(x, y, r * k / 4, 0, 7); c.set_source_rgba(*col, 0.25); c.set_line_width(2); c.stroke()
    a = (t * 1.3) % 6.283
    c.save(); c.new_path(); c.arc(x, y, r, 0, 7); c.clip()
    for j in range(12):
        aa = a - j * 0.05; c.move_to(x, y); c.line_to(x + math.cos(aa) * r, y + math.sin(aa) * r); c.set_source_rgba(*col, 0.5 * (1 - j / 12)); c.set_line_width(5); c.stroke()
    c.restore()
    c.new_path(); c.arc(x, y, r, 0, 7); c.set_source_rgb(0.3, 0.32, 0.36); c.set_line_width(10); c.stroke()
    bx, by = x + r * 0.35, y - r * 0.25
    if blip > 0:
        c.new_path(); c.arc(bx, by, 9, 0, 7); c.set_source_rgba(*col, blip); c.fill()
        for j in range(4): c.new_path(); c.arc(bx - 14 * (j + 1), by + 10 * (j + 1), 4, 0, 7); c.set_source_rgba(*col, blip * (0.5 - j * 0.1)); c.fill()
    if block > 0:
        c.move_to(bx + 10, by - 10); c.line_to(bx + 50, by - 50); c.set_source_rgba(*col, block); c.set_line_width(3); c.stroke()
        F(c, 34, 'Montserrat'); c.move_to(bx - 40, by - 90); c.text_path("MAS370"); c.set_source_rgba(*col, block); c.fill()
        F(c, 28, 'Montserrat'); c.move_to(bx - 40, by - 56); c.text_path("350  471"); c.set_source_rgba(*col, block); c.fill()


def b777(c, x, y, rot, s, t, lights=True):
    a330(c, x, y, rot, s, t, lights=lights, tail=((0.75, 0.78, 0.85), (0.97, 0.97, 0.99), (0.55, 0.6, 0.7)))


def sc_mh_hook(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        night_sky(c, t); cloud_sea(c, t, 1250, col=(0.08, 0.1, 0.18), lit=(0.3, 0.35, 0.5))
        b777(c, 540, 880 + 6 * math.sin(t), -0.02, 1.15, t)
        n = int(239 * ap(p, 0.2, 0.7)); text(c, str(n), 540, 600, 170, WH, glow=0.5); label(c, "PERSONNES À BORD", 540, 680, 52, WH, ap(p, 0.2, 0.4), 'Bebas Neue')
    elif k == 1:
        night_sky(c, t); ocean_night(c, t, 1150)
        fade = 1 - ap(p, 0.0, 0.7)
        c.push_group(); b777(c, 500 + 120 * p, 800, -0.02, 0.9, t); c.pop_group_to_source(); c.paint_with_alpha(fade)
        if fade < 0.4: text(c, "?", 500 + 120 * p, 800, 220, WH, glow=0.6)
        tag(c, "12 ANS · INTROUVABLE", 540, 1285, YEL, ap(p, 0.3, 0.5), 60)
    else:
        c.set_source_rgb(0.0, 0.02, 0.01); c.paint()
        radar_atc(c, 540, 1000, 330, t, block=0, blip=0)
        stamp(c, "MH370", 540, 520, 220, CY, since, glow=1.0)


def sc_mh_night(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k <= 1:
        zq = 0.0 if k == 0 else eout(ap(p, 0.0, 0.45))
        V = (82.5 + (103.0 - 82.5) * zq, -10 + (8.0 + 10) * zq, 1 + 1.7 * zq)
        c.save(); zoomed(c, *V); io_map(c, t, labels=True, z=V[2])
        if k == 1: draw_route(c, IG_FRAC * ap(p, 0.35, 1.0), V[2])
        c.restore()
        x, y = ZS(*KL, V); radial(c, x, y, 60, AMB, 0.9); c.new_path(); c.arc(x, y, 10, 0, 7); c.set_source_rgb(1, 1, 1); c.fill()
        label(c, "KUALA LUMPUR", x - 20, y + 62, 44, WH, 1, 'Bebas Neue')
        bx, by = ZS(116.4, 39.9, V); d = math.hypot(bx - x, by - y); L = 330; ex, ey = x + (bx - x) / d * L, y + (by - y) / d * L
        c.move_to(x, y); c.line_to(ex, ey); c.set_source_rgba(1, 1, 1, 0.55); c.set_dash([14, 10]); c.set_line_width(4); c.stroke(); c.set_dash([])
        ang = math.atan2(ey - y, ex - x); c.move_to(ex + math.cos(ang - 2.6) * 28, ey + math.sin(ang - 2.6) * 28); c.line_to(ex, ey); c.line_to(ex + math.cos(ang + 2.6) * 28, ey + math.sin(ang + 2.6) * 28)
        c.set_source_rgba(1, 1, 1, 0.8); c.set_line_width(5); c.stroke()
        label(c, "VERS PÉKIN", min(900, ex + 10), max(470, ey - 30), 44, WH, 1, 'Bebas Neue')
        tag(c, "8 MARS 2014 · 00:42", 540, 1285, AMB, ap(p, 0.05, 0.2) if k == 0 else 1, 54)
    else:
        c.set_source_rgb(0.0, 0.02, 0.01); c.paint()
        radar_atc(c, 540, 860, 340, t, block=1, blip=1)
        for j in range(30):
            xx = 160 + j * 25; hh = 20 + 60 * abs(math.sin(t * 9 + j * 0.7)) * ap(p, 0.2, 0.35) * (1 - ap(p, 0.6, 0.75))
            c.move_to(xx, 1300 - hh / 2); c.line_to(xx, 1300 + hh / 2)
        c.set_source_rgba(0.3, 1, 0.5, 0.8); c.set_line_width(6); c.set_line_cap(1); c.stroke()
        tag(c, "01:19 · « BONNE NUIT »", 540, 440, WH, ap(p, 0.2, 0.4), 56)


def sc_mh_dark(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    c.set_source_rgb(0.0, 0.02, 0.01); c.paint()
    if k == 0:
        off = ap(p, 0.4, 0.6)
        radar_atc(c, 540, 860, 340, t, block=1 - off, blip=1 - off)
        tag(c, "01:21 · TRANSPONDEUR ÉTEINT", 540, 1285, RED, ap(p, 0.4, 0.55), 52)
    else:
        radar_atc(c, 540, 860, 340, t, block=0, blip=0)
        text(c, "?", 540 + 340 * 0.35, 860 - 340 * 0.25, 160, WH, glow=0.7)
        tag(c, "DISPARU DES ÉCRANS", 540, 1285, WH, ap(p, 0.1, 0.3), 56)


def sc_mh_turn(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    V = (100.0, 5.0, 2.7)
    prog = IG_FRAC + (1 - IG_FRAC) * ap(p, 0.05, 0.95) if k == 0 else 1.0
    c.save(); zoomed(c, *V); io_map(c, t, labels=False, z=V[2]); c.restore()
    for nm, ll in (("THAÏLANDE", (101.0, 12.3)), ("SUMATRA", (99.8, -0.4))):
        x, y = ZS(*ll, V); label(c, nm, x, y, 40, (0.55, 0.7, 0.85), 0.9, 'Bebas Neue')
    c.save(); zoomed(c, *V); px, py = draw_route(c, prog, V[2]); c.restore()
    x, y = ZS(*KL, V); c.new_path(); c.arc(x, y, 9, 0, 7); c.set_source_rgb(1, 1, 1); c.fill(); label(c, "KUALA LUMPUR", x + 120, y + 30, 38, WH, 1, 'Bebas Neue')
    ix, iy = ZS(*IGARI, V); c.new_path(); c.arc(ix, iy, 12, 0, 7); c.set_source_rgb(*RED); c.fill()
    label(c, "DEMI-TOUR", ix + 20, iy - 30, 40, RED, 1, 'Bebas Neue')
    hx, hy = 540 + (px - P(*V[:2])[0]) * V[2], 880 + (py - P(*V[:2])[1]) * V[2]
    radial(c, hx, hy, 50, (1, 0.7, 0.2), 0.9)
    c.save(); c.translate(hx, hy); c.rotate(-math.pi / 2 - 0.9 if k == 1 or p > 0.6 else 0.6); c.scale(0.16, 0.16); jet(c, 0, 0, 0, 1.0); c.restore()
    tag(c, "RADAR MILITAIRE", 540, 1285, (1, 0.7, 0.2), 1, 54)
    if k == 1:
        ph = (since * 1.5) % 1
        c.new_path(); c.arc(hx, hy, 20 + 90 * ph, 0, 7); c.set_source_rgba(1, 0.4, 0.3, 1 - ph); c.set_line_width(4); c.stroke()
        tag(c, "DERNIER ÉCHO · 02:22", 540, 420, RED, ap(p, 0.1, 0.3), 54)


def sc_mh_arcs(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    io_map(c, t, labels=(k >= 2))
    sx, sy = P(*SAT)
    draw_route(c, 1.0, 1.0, 0.7)
    c.save(); c.translate(sx, sy - 130 + 6 * math.sin(t)); rr(c, -34, -22, 68, 44, 8); fill_stroke(c, (0.85, 0.75, 0.3), 5)
    for sgn in (-1, 1): c.new_path(); c.rectangle(sgn * 38 + (0 if sgn > 0 else -100), -15, 100, 30); c.set_source_rgb(0.2, 0.35, 0.7); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(3); c.stroke()
    c.restore()
    c.move_to(sx, sy - 108); c.line_to(sx, sy); c.set_source_rgba(1, 1, 1, 0.3); c.set_dash([6, 6]); c.set_line_width(2); c.stroke(); c.set_dash([])
    label(c, "SATELLITE INMARSAT", sx + 40, sy - 190, 44, WH, 1, 'Bebas Neue')
    if k == 1:
        for j in range(4):
            ph = (t * 0.9 + j / 4) % 1; c.new_path(); c.arc(sx, sy - 130, 40 + 420 * ph, 0, 7); c.set_source_rgba(0.4, 1, 0.8, 0.55 * (1 - ph)); c.set_line_width(3); c.stroke()
        tag(c, "6 H DE SIGNAUX AUTOMATIQUES", 540, 1285, CY, ap(p, 0.1, 0.3), 50)
    c.save(); c.rectangle(0, 400, W, 960); c.clip()
    n = 0
    if k >= 2: n = int(7.99 * ap(t, sg['sent'][2][0], sg['sent'][2][1])) if k == 2 else 7
    for j in range(n):
        arc_path(c, ARCS[j]); last = (j == 6)
        c.set_source_rgba(*(CY if last and k == 3 else (0.4, 0.8, 1.0)), 1.0 if (last and k == 3) else 0.5); c.set_line_width(7 if (last and k == 3) else 3); c.stroke()
        if k == 2 or not last:
            x, y = arc_pt(ARCS[j], 24); label(c, str(j + 1), x + 16, y - 6, 34, (0.6, 0.85, 1.0), 0.9, 'Bebas Neue')
    if k == 3:
        arc_path(c, ARCS[6], -100, -40); c.set_source_rgba(*CY, 0.35); c.set_line_width(28); c.stroke()
        x, y = arc_pt(ARCS[6], -40); label(c, "7E ARC", x + 110, y + 10, 56, CY, ap(p, 0.2, 0.35), 'Bebas Neue')
    c.restore()
    if k == 3: tag(c, "LE DERNIER SIGNAL", 540, 1285, CY, ap(p, 0.2, 0.35), 60)
    if k >= 2: label(c, "schéma simplifié", 880, 1200, 30, (0.6, 0.65, 0.75))


def sc_mh_flaperon(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        io_map(c, t)
        arc_path(c, ARCS[6], -100, -40); c.set_source_rgba(*CY, 0.5); c.set_line_width(4); c.stroke()
        p0 = arc_pt(ARCS[6], -55); p1 = P(*REUNION); pc = (500, 990)
        q = ap(p, 0.05, 0.85); n = 40
        c.move_to(*p0)
        for j in range(1, int(n * q) + 1):
            u_ = j / n; c.line_to((1 - u_) ** 2 * p0[0] + 2 * (1 - u_) * u_ * pc[0] + u_ * u_ * p1[0], (1 - u_) ** 2 * p0[1] + 2 * (1 - u_) * u_ * pc[1] + u_ * u_ * p1[1])
        c.set_source_rgba(1, 1, 1, 0.8); c.set_dash([12, 9]); c.set_line_width(5); c.stroke(); c.set_dash([])
        u_ = max(0.0, min(1.0, int(n * q) / n)); fx = (1 - u_) ** 2 * p0[0] + 2 * (1 - u_) * u_ * pc[0] + u_ * u_ * p1[0]; fy = (1 - u_) ** 2 * p0[1] + 2 * (1 - u_) * u_ * pc[1] + u_ * u_ * p1[1]
        c.save(); c.translate(fx, fy); c.rotate(t * 0.8); rr(c, -26, -7, 52, 14, 4); c.set_source_rgb(0.92, 0.92, 0.9); c.fill(); c.restore()
        rx, ry = p1; radial(c, rx, ry, 70, (0.3, 1, 0.6), 0.8 * ap(p, 0.8, 0.95)); c.new_path(); c.arc(rx, ry, 10, 0, 7); c.set_source_rgb(0.3, 1, 0.6); c.fill()
        label(c, "LA RÉUNION", rx + 10, ry - 40, 48, (0.3, 1, 0.6), 1, 'Bebas Neue')
        label(c, "≈ 4 000 KM DE DÉRIVE", 430, 1190, 44, WH, ap(p, 0.4, 0.6), 'Bebas Neue')
        tag(c, "JUILLET 2015", 540, 1285, WH, ap(p, 0.05, 0.2), 56)
    else:
        sky(c, (0.35, 0.6, 0.9), (0.85, 0.9, 0.95))
        c.new_path(); c.rectangle(0, 1000, W, 200); c.set_source_rgb(0.1, 0.35, 0.55); c.fill()
        c.new_path(); c.move_to(0, 1150); c.curve_to(300, 1120, 700, 1180, W, 1140); c.line_to(W, H); c.line_to(0, H); c.close_path(); c.set_source_rgb(0.15, 0.14, 0.15); c.fill()
        for j in range(3):
            ph = (t * 0.4 + j / 3) % 1; c.move_to(0, 1150 - 40 * ph); c.curve_to(300, 1120 - 40 * ph, 700, 1180 - 40 * ph, W, 1140 - 40 * ph); c.set_source_rgba(1, 1, 1, 0.5 * (1 - ph)); c.set_line_width(5); c.stroke()
        c.save(); c.translate(540, 1230); c.rotate(-0.12)
        c.new_path(); c.move_to(-260, -30); c.line_to(250, -50); c.line_to(270, 30); c.line_to(-250, 40); c.close_path(); fill_stroke(c, (0.88, 0.88, 0.86), 7)
        r = random.Random(2)
        for _ in range(60): c.new_path(); c.arc(r.uniform(-240, 240), r.uniform(-25, 30), 3 + 4 * r.random(), 0, 7); c.set_source_rgb(0.55, 0.5, 0.45); c.fill()
        c.restore()
        label(c, "FLAPERON (MORCEAU D'AILE)", 540, 1110, 40, WH, ap(p, 0.2, 0.4), 'Bebas Neue')
        tag(c, "UN MORCEAU DU MH370", 540, 600, GRN, ap(p, 0.1, 0.3), 66)


def sc_mh_search(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        V = (92.0, -33.0, 2.3)
        c.save(); zoomed(c, *V); io_map(c, t, labels=False, z=V[2])
        arc_path(c, ARCS[6], -75, -30); c.set_source_rgba(*CY, 0.8); c.set_line_width(4 / V[2]); c.stroke()
        q = ap(p, 0.05, 0.85); a0, a1 = -64.0, -44.0; ac = a0 + (a1 - a0) * q
        if q > 0:
            c.new_path(); m = 30
            for j in range(m + 1): c.line_to(*arc_pt(ARCS[6] - 1.3, a0 + (ac - a0) * j / m))
            for j in range(m, -1, -1): c.line_to(*arc_pt(ARCS[6] + 1.3, a0 + (ac - a0) * j / m))
            c.close_path(); c.set_source_rgba(*CY, 0.22); c.fill()
            aa = a0
            while aa < ac:
                c.move_to(*arc_pt(ARCS[6] - 1.3, aa)); c.line_to(*arc_pt(ARCS[6] + 1.3, aa)); aa += 0.55
            c.set_source_rgba(*CY, 0.45); c.set_line_width(1.5 / V[2]); c.stroke()
        c.restore()
        if q > 0:
            sxp, syp = arc_pt(ARCS[6] + 1.3 * math.sin(t * 2.2), ac); x, y = 540 + (sxp - P(*V[:2])[0]) * V[2], 880 + (syp - P(*V[:2])[1]) * V[2]
            radial(c, x, y, 30, YEL, 0.9); c.new_path(); c.arc(x, y, 9, 0, 7); c.set_source_rgb(*YEL); c.fill()
        n = int(120000 * ap(p, 0.0, 0.8)) // 1000 * 1000
        rr(c, 190, 420, 700, 180, 30); c.set_source_rgba(0, 0, 0, 0.6); c.fill()
        text(c, f"{n:,} KM²".replace(',', ' '), 540, 545, 110, CY, glow=0.6)
        label(c, "DE FOND MARIN RATISSÉS", 540, 1285, 46, WH, ap(p, 0.1, 0.3), 'Bebas Neue')
        ax_, ay_ = arc_pt(ARCS[6], -36); label(c, "7E ARC", 540 + (ax_ - P(*V[:2])[0]) * V[2] + 90, 880 + (ay_ - P(*V[:2])[1]) * V[2], 52, CY, 1, 'Bebas Neue')
    else:
        ocean_night(c, t, 1000, calm=0.2)
        x = 680 - 200 * p
        c.move_to(x - 150, 1040); c.curve_to(x - 260, 1200, x - 320, 1300, x - 380, 1380); c.set_source_rgba(1, 0.8, 0.3, 0.5); c.set_line_width(3); c.stroke()
        c.save(); c.translate(x - 380, 1380); rr(c, -40, -12, 80, 24, 10); fill_stroke(c, (1, 0.75, 0.15), 4); c.restore()
        c.save(); c.translate(x, 1010)
        c.new_path(); c.move_to(-170, 0); c.line_to(170, 0); c.line_to(140, 46); c.line_to(-150, 46); c.close_path(); fill_stroke(c, (0.85, 0.85, 0.88), 6)
        rr(c, -60, -70, 120, 70, 8); fill_stroke(c, (0.95, 0.95, 0.97), 5)
        c.restore()
        tag(c, "DÉBUT 2026 : RIEN", 540, 600, YEL, ap(p, 0.1, 0.3), 70)


def sc_mh_end(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    io_map(c, t, glow=0.6, labels=False)
    arc_path(c, ARCS[6], -100, -40); c.set_source_rgba(*CY, 0.6); c.set_line_width(5); c.stroke()
    r = random.Random(239)
    n = int(239 * min(1, (t - sg['t0']) / 3))
    for j in range(n):
        x, y = arc_pt(ARCS[6], -100 + 60 * r.random()); x += r.gauss(0, 12); y += r.gauss(0, 12)
        y -= (t * 20 * (0.3 + r.random())) % 120
        radial(c, x, y, 14, (1, 0.8, 0.45), 0.5); c.new_path(); c.arc(x, y, 2.5, 0, 7); c.set_source_rgba(1, 0.92, 0.7, 0.9); c.fill()
    label(c, "239", 300, 1200, 70, (1, 0.9, 0.7), min(1, (t - sg['t0']) / 3), 'Bebas Neue')
    if k == 0:
        text(c, "?", 540, 760, 260, WH, glow=0.8)
    else:
        stamp(c, "TU AS UNE THÉORIE ?", 540, 640, 120, ORG, since, glow=1.0)


SC9 = {k[3:]: v for k, v in globals().items() if k.startswith('sc_') and callable(v)}
