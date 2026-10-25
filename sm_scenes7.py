"""Scènes v2 (une illustration par phrase, sg['sent'] = horodatage réel) pour le 26/10 :
SURVIVRAIS-TU chute libre (fl_*), HISTOIRE VRAIE Roland Garros (gr_*), TU ES LE PILOTE ép. 3 (e3_*).
R = module sm_render injecté (eyes_head, ocean_bg, flames, CFG)."""
import cairo, math, random
from sm_lib import *
from sm_scenes2 import ease, ap, blinkh, sky, jet, ORG, BLUE, RED, WH, GRN
from sm_scenes6 import si, stamp, speedlines, clouds, frost, eout, back, YEL
R = None
SEPIA = (0.93, 0.82, 0.6)


def mix(a, b, k): return tuple(x + (y - x) * k for x, y in zip(a, b))


def label(c, s, x, y, size=44, col=WH, a=1.0, fam='Montserrat'):
    if a <= 0: return
    c.push_group(); text(c, s, x, y, size, col, fam); c.pop_group_to_source(); c.paint_with_alpha(min(1, a))


def tag(c, s, x, y, col, a=1.0, size=56):
    """Étiquette pastille (fond sombre) : toujours lisible."""
    if a <= 0: return
    F(c, size); w = c.text_extents(s).x_advance + 50
    c.push_group(); rr(c, x - w / 2, y - size * 0.95, w, size * 1.3, size * 0.35); c.set_source_rgba(0.02, 0.02, 0.05, 0.75); c.fill_preserve()
    c.set_source_rgba(*col, 1); c.set_line_width(4); c.stroke(); text(c, s, x, y, size, col); c.pop_group_to_source(); c.paint_with_alpha(min(1, a))


def no_sign(c, x, y, r, a=1.0):
    c.new_path(); c.arc(x, y, r, 0, 7); c.set_source_rgba(*RED, a); c.set_line_width(r * 0.16); c.stroke()
    c.move_to(x - r * 0.7, y - r * 0.7); c.line_to(x + r * 0.7, y + r * 0.7); c.stroke()


def check(c, x, y, s, col=GRN, a=1.0):
    c.move_to(x - 30 * s, y); c.line_to(x - 8 * s, y + 24 * s); c.line_to(x + 34 * s, y - 26 * s)
    c.set_source_rgba(*col, a); c.set_line_width(12 * s); c.set_line_cap(1); c.set_line_join(1); c.stroke()


def cross(c, x, y, s, col=RED, a=1.0):
    for d in (1, -1):
        c.move_to(x - 30 * s, y - 30 * s * d); c.line_to(x + 30 * s, y + 30 * s * d)
    c.set_source_rgba(*col, a); c.set_line_width(13 * s); c.set_line_cap(1); c.stroke()


def clock(c, x, y, r, hh, mm, col=(0.97, 0.95, 0.9)):
    c.new_path(); c.arc(x, y, r, 0, 7); fill_stroke(c, col, 9)
    for k in range(12):
        a = k * math.pi / 6; c.move_to(x + math.cos(a) * r * 0.82, y + math.sin(a) * r * 0.82); c.line_to(x + math.cos(a) * r * 0.93, y + math.sin(a) * r * 0.93)
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    for ang, L, w in (((hh % 12 + mm / 60) / 12 * 2 * math.pi, 0.5, 13), (mm / 60 * 2 * math.pi, 0.78, 8)):
        a = ang - math.pi / 2; c.move_to(x, y); c.line_to(x + math.cos(a) * r * L, y + math.sin(a) * r * L)
        c.set_source_rgb(*INK); c.set_line_width(w); c.set_line_cap(1); c.stroke()
    c.new_path(); c.arc(x, y, 12, 0, 7); c.set_source_rgb(*RED); c.fill()


# =============================== SURVIVRAIS-TU : chute libre ===============================
def person(c, x, y, s, t, pose='spread', mood='worried', look=(0, 0), col=(0.25, 0.45, 0.75), rot=0.0, closed=False, helmet=False):
    """Passager stickman en chute. pose : spread (à plat), tumble (gesticule), limp (inconscient), brace (réception)."""
    c.save(); c.translate(x, y); c.rotate(rot)
    f = 6 * math.sin(t * 22)
    if pose == 'spread':
        arms = [[(-38, -45), (-120, -95 + f), (-175, -160 + f)], [(38, -45), (120, -95 - f), (175, -160 - f)]]
        legs = [[(-25, 60), (-85, 140 - f), (-120, 215 - f)], [(25, 60), (85, 140 + f), (120, 215 + f)]]
    elif pose == 'tumble':
        a1, a2 = t * 7, t * 6 + 2
        arms = [[(-38, -45), (-90 + 30 * math.cos(a1), -120 + 40 * math.sin(a1)), (-130 + 50 * math.cos(a1 + 1), -200 + 50 * math.sin(a1))],
                [(38, -45), (90 + 30 * math.cos(a2), -110 + 40 * math.sin(a2)), (140 + 40 * math.cos(a2 + 1), -170 + 60 * math.sin(a2))]]
        legs = [[(-25, 60), (-60 + 20 * math.sin(a2), 150), (-90 + 40 * math.sin(a1), 230)], [(25, 60), (70 + 20 * math.sin(a1), 140), (60 + 50 * math.cos(a2), 230)]]
    elif pose == 'limp':
        arms = [[(-38, -45), (-70, -130), (-80, -210)], [(38, -45), (75, -125), (70, -205)]]
        legs = [[(-25, 60), (-50, 150), (-40, 235)], [(25, 60), (55, 145), (75, 225)]]
    else:  # brace : bras autour de la tête, pieds joints, genoux fléchis
        arms = [[(-38, -45), (-95, -150), (-30, -215)], [(38, -45), (95, -150), (30, -215)]]
        legs = [[(-18, 60), (35, 140), (-8, 225)], [(18, 60), (55, 140), (12, 225)]]
    for L in legs + arms:
        limb(c, [(px * s, py * s) for px, py in L], w=22 * s)
    rr(c, -55 * s, -75 * s, 110 * s, 150 * s, 45 * s); fill_stroke(c, col, 9)
    hy = -150 * s if pose != 'brace' else -140 * s
    blinkh(c, 0, hy, 70 * s, mood, look, t, helmet)
    if closed:
        for sx in (-1, 1):
            ex = sx * 70 * s * 0.33 + look[0]; ey = hy + 2 + look[1]
            c.new_path(); c.arc(ex, ey, 70 * s * 0.16, 0, 7); c.set_source_rgb(0.98, 0.98, 0.99); c.fill()
            c.move_to(ex - 10 * s, ey); c.line_to(ex + 10 * s, ey); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    if pose == 'brace':                                   # avant-bras devant la tête
        for sx in (-1, 1): limb(c, [(sx * 95 * s, -150 * s), (sx * -30 * s, -215 * s)], w=22 * s)
    c.restore()


def fall_sky(c, alt):
    """alt : 1 = 10 000 m (bleu nuit), 0 = sol (bleu clair)."""
    top = mix((0.30, 0.52, 0.85), (0.02, 0.04, 0.16), alt); bot = mix((0.75, 0.85, 0.95), (0.18, 0.30, 0.62), alt)
    sky(c, top, bot)
    if alt > 0.5:
        r = random.Random(4)
        for _ in range(90):
            c.new_path(); c.arc(r.random() * W, r.random() * 700, r.choice((1, 1.5, 2)), 0, 7); c.set_source_rgba(1, 1, 1, (alt - 0.5) * 1.2 * r.random()); c.fill()


def rising_clouds(c, t, sp=600, n=9, seed=5, a=0.7, s=1.0):
    r = random.Random(seed)
    for _ in range(n):
        x = r.random() * W; y = (r.random() * (H + 600) - t * sp * (0.6 + 0.8 * r.random())) % (H + 600) - 300
        k = s * (0.7 + 0.9 * r.random())
        for dx, dy, rad in ((0, 0, 80), (70, 14, 62), (-72, 18, 58), (28, -32, 55)):
            c.new_path(); c.arc(x + dx * k, y + dy * k, rad * k, 0, 7); c.set_source_rgba(1, 1, 1, a); c.fill()


def up_lines(c, t, a=0.8):
    speedlines(c, t, a, horiz=False, n=34, seed=8)


def para_icon(c, x, y, s):
    c.new_path(); c.arc(x, y, 110 * s, math.pi, 2 * math.pi); c.close_path(); fill_stroke(c, (0.95, 0.5, 0.2), 7)
    for k in range(5):
        c.move_to(x - 110 * s + k * 55 * s, y); c.line_to(x, y + 130 * s)
    c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
    c.new_path(); c.arc(x, y + 140 * s, 16 * s, 0, 7); fill_stroke(c, (0.98, 0.98, 0.99), 4)


def sc_fl_hook(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        fall_sky(c, 1.0); radial(c, 860, 300, 360, (1, 0.9, 0.7), 0.25)
        rising_clouds(c, t * 0.15, 200, 6, 3, 0.55, 0.8)
        jet(c, 560 - 60 * p, 640, 0.0, 1.15)
        y = 700 + 420 * ap(p, 0.15, 1.0) ** 1.4
        person(c, 600 - 40 * p, y, 0.42, t, 'tumble', rot=t * 2.5)
        stamp(c, "10 000 M", 540, 1290, 170, WH, since)
    elif k == 1:
        fall_sky(c, 0.95); up_lines(c, t, 0.7); rising_clouds(c, t, 900, 5, 6, 0.35)
        person(c, 540, 930, 1.25, t, 'tumble', rot=0.25 * math.sin(t * 3))
        para_icon(c, 820, 1150, 0.7); no_sign(c, 820, 1230, 150, min(1, since / 0.2))
        stamp(c, "SANS PARACHUTE", 540, 600, 110, RED, since)
    elif k == 2:
        c.set_source_rgb(0.03, 0.04, 0.08); c.paint(); radial(c, 540, 900, 700, (0.3, 0.4, 0.8), 0.18)
        text(c, "IMPOSSIBLE ?", 540, 820, 170, WH, glow=0.3)
        st = ap(p, 0.4, 0.55)
        if st > 0: c.move_to(110, 765); c.line_to(110 + 860 * st, 765); c.set_source_rgb(*RED); c.set_line_width(18); c.set_line_cap(1); c.stroke()
        if p > 0.55:
            q = since - 0.55 * (sg['sent'][3][0] - sg['sent'][2][0])
            stamp(c, "ILS ONT SURVÉCU", 540, 1060, 120, GRN, q, glow=1.0)
            for j in range(3):
                a = ap(p, 0.62 + 0.08 * j, 0.7 + 0.08 * j)
                if a > 0: c.push_group(); blinkh(c, 300 + j * 240, 1260, 70, 'neutral', (0, 0), t, False); c.pop_group_to_source(); c.paint_with_alpha(a)
    else:
        fall_sky(c, 0.85); up_lines(c, t, 0.9); rising_clouds(c, t, 1100, 8, 9, 0.45)
        person(c, 540, 1000, 1.35, t, 'spread', rot=0.06 * math.sin(t * 2))
        stamp(c, "SURVIVRAIS-TU ?", 540, 560, 140, RED, since, glow=1.0)


def sc_fl_air(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    fall_sky(c, 1.0); up_lines(c, t, 0.5); rising_clouds(c, t, 500, 4, 12, 0.25)
    if k == 0:
        person(c, 540, 1000, 0.95, t, 'tumble', rot=0.3 * math.sin(t * 1.5))
        frost(c, 0.3 + 0.5 * ap(p, 0, 0.5), t)
        rr(c, 250, 430, 580, 190, 30); c.set_source_rgba(0, 0, 0, 0.55); c.fill()
        text(c, "−50 °C", 540, 575, 150, BLUE, glow=0.9)
        a = ap(p, 0.45, 0.6)
        if a > 0:
            lvl = 1 - 0.7 * ap(p, 0.55, 1.0)
            rr(c, 170, 1268, 740, 150, 30); c.set_source_rgba(0, 0, 0, 0.55 * a); c.fill()
            label(c, "OXYGÈNE", 540, 1318, 46, WH, a)
            rr(c, 200, 1340, 680, 50, 24); c.set_source_rgba(1, 1, 1, 0.15 * a); c.fill()
            rr(c, 206, 1346, 668 * lvl, 38, 19); c.set_source_rgba(*(RED if lvl < 0.5 else ORG), a); c.fill()
    else:
        sl = ap(p, 0.2, 0.8)
        person(c, 540, 1000, 1.15, t, 'tumble' if sl < 0.5 else 'limp', mood='neutral' if sl > 0.5 else 'worried', closed=sl > 0.5, rot=0.4 * math.sin(t * 1.5) + 0.8 * sl)
        frost(c, 0.8, t)
        n = int(60 * ap(p, 0.0, 0.9)); cx, cy, r = 540, 560, 120
        c.new_path(); c.arc(cx, cy, r, 0, 7); c.set_source_rgba(0, 0, 0, 0.55); c.fill()
        c.new_path(); c.arc(cx, cy, r - 12, -math.pi / 2, -math.pi / 2 + 2 * math.pi * n / 60); c.set_source_rgb(*RED); c.set_line_width(18); c.stroke()
        text(c, f"{n} S", cx, cy + 30, 80, WH)
        g = cairo.RadialGradient(W / 2, H * 0.5, W * (0.75 - 0.45 * sl), W / 2, H * 0.5, W * 1.05); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.95 * sl); c.set_source(g); c.paint()
        if p > 0.55: stamp(c, "INCONSCIENT", 540, 1300, 120, RED, since - 0.55 * (sg['end'] - sg['sent'][1][0]))


def sc_fl_wake(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        alt = 1 - 0.33 * p; fall_sky(c, alt); up_lines(c, t, 0.6)
        r = random.Random(3)                              # l'air s'épaissit : particules de plus en plus denses
        for j in range(int(30 + 140 * p)):
            x = r.random() * W; y = (r.random() * H - t * 700) % H
            c.new_path(); c.arc(x, y, 2 + 2 * r.random(), 0, 7); c.set_source_rgba(0.85, 0.92, 1, 0.35); c.fill()
        person(c, 540, 1000, 1.1, t, 'limp', mood='neutral', closed=True, rot=0.3 * math.sin(t * 0.8) + 0.6)
        alt_m = int(10000 - 3300 * p) // 100 * 100
        rr(c, 270, 430, 540, 180, 30); c.set_source_rgba(0, 0, 0, 0.5); c.fill()
        text(c, f"{alt_m:,} M".replace(',', ' '), 540, 570, 140, WH, glow=0.4)
    elif k == 1:
        fall_sky(c, 0.6); up_lines(c, t, 0.8); rising_clouds(c, t, 900, 5, 14, 0.4)
        fl = max(0, 1 - since / 0.3); c.set_source_rgba(1, 1, 1, 0.8 * fl); c.paint()
        person(c, 540, 1020, 1.25, t, 'tumble', mood='worried', look=(0, -10), rot=0.2 * math.sin(t * 2))
        for j in range(8):                                # « tilt » de réveil
            a = j * math.pi / 4; c.move_to(540 + math.cos(a) * 130, 850 + math.sin(a) * 130); c.line_to(540 + math.cos(a) * (170 + 30 * fl), 850 + math.sin(a) * (170 + 30 * fl))
        c.set_source_rgba(*YEL, 0.8); c.set_line_width(7); c.set_line_cap(1); c.stroke()
        stamp(c, "6 700 M", 540, 560, 170, ORG, since, glow=0.9)
    else:
        fall_sky(c, 0.5); up_lines(c, t, 0.8)
        g = cairo.LinearGradient(0, 1250, 0, H); g.add_color_stop_rgba(0, 0.35, 0.5, 0.3, 0); g.add_color_stop_rgba(0.3, 0.35, 0.5, 0.3, 1); g.add_color_stop_rgb(1, 0.25, 0.38, 0.22)
        c.rectangle(0, 1250, W, H - 1250); c.set_source(g); c.fill()
        r = random.Random(8)
        for _ in range(40):
            c.new_path(); c.arc(r.random() * W, 1340 + r.random() * 560, 6 + 10 * r.random(), 0, 7); c.set_source_rgba(0.18, 0.3, 0.16, 0.8); c.fill()
        person(c, 540, 980, 0.95, t, 'tumble', rot=0.2 * math.sin(t * 2))
        rem = max(0, 120 - since); mm, ss = int(rem // 60), int(rem % 60)
        rr(c, 290, 420, 500, 190, 30); c.set_source_rgba(0, 0, 0, 0.6); c.fill()
        text(c, f"{mm}:{ss:02d}", 540, 575, 160, RED, glow=0.8)
        label(c, "AVANT LE SOL", 540, 680, 48, WH)


def gauge(c, x, y, r, v, vmax, ticks, red_from=None, col=YEL, unit=""):
    c.new_path(); c.arc(x, y, r, 0, 7); fill_stroke(c, (0.04, 0.05, 0.07), 10)
    a0, a1 = math.pi * 0.75, math.pi * 2.25
    if red_from is not None:
        c.new_path(); c.arc(x, y, r * 0.86, a0, a0 + (a1 - a0) * red_from / vmax); c.set_source_rgb(*RED); c.set_line_width(r * 0.08); c.stroke()
        c.new_path(); c.arc(x, y, r * 0.86, a0 + (a1 - a0) * red_from / vmax, a1); c.set_source_rgb(*GRN); c.set_line_width(r * 0.08); c.stroke()
    for tv in ticks:
        a = a0 + (a1 - a0) * tv / vmax
        c.move_to(x + math.cos(a) * r * 0.72, y + math.sin(a) * r * 0.72); c.line_to(x + math.cos(a) * r * 0.8, y + math.sin(a) * r * 0.8)
        c.set_source_rgb(1, 1, 1); c.set_line_width(5); c.stroke()
        F(c, r * 0.15, 'Montserrat'); s = str(tv); w = c.text_extents(s).x_advance
        c.move_to(x + math.cos(a) * r * 0.56 - w / 2, y + math.sin(a) * r * 0.56 + r * 0.05); c.text_path(s); c.set_source_rgb(0.85, 0.88, 0.95); c.fill()
    a = a0 + (a1 - a0) * min(v, vmax) / vmax
    c.move_to(x, y); c.line_to(x + math.cos(a) * r * 0.82, y + math.sin(a) * r * 0.82); c.set_source_rgb(*col); c.set_line_width(r * 0.05); c.set_line_cap(1); c.stroke()
    c.new_path(); c.arc(x, y, r * 0.08, 0, 7); c.set_source_rgb(*col); c.fill()
    if unit: label(c, unit, x, y + r * 0.42, r * 0.13, (0.75, 0.8, 0.9))


def sc_fl_speed(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    fall_sky(c, 0.45); up_lines(c, t, 0.9); rising_clouds(c, t, 1300, 6, 21, 0.35)
    if k == 0:
        v = 200 * eout(ap(p, 0.05, 0.6) * 1.0) + 3 * math.sin(t * 9) * (p > 0.6)
        gauge(c, 540, 760, 260, v, 300, (0, 50, 100, 150, 200, 250, 300), col=YEL, unit="KM/H")
        if p > 0.45: stamp(c, "200 KM/H", 540, 1250, 170, YEL, since - 0.45 * (sg['sent'][1][0] - sg['sent'][0][0]), glow=1.0)
    else:
        sp = ap(p, 0.05, 0.35)
        person(c, 540, 900, 1.35, t, 'spread' if sp > 0.5 else 'tumble', rot=0.04 * math.sin(t * 2))
        for j in range(6):                                 # résistance de l'air sous le ventre
            x = 300 + j * 96; ph = (t * 1.3 + j * 0.17) % 1; y = 1380 - 200 * ph
            c.move_to(x, y); c.line_to(x, y - 90); c.move_to(x - 20, y - 66); c.line_to(x, y - 92); c.line_to(x + 20, y - 66)
            c.set_source_rgba(*GRN, (1 - ph) * sp); c.set_line_width(8); c.set_line_cap(1); c.stroke()
        stamp(c, "À PLAT = PLUS LENT", 540, 560, 110, GRN, since)


def ground_map(c, t, zoom, cx, cy, concrete=0.0):
    c.save(); c.translate(W / 2, H / 2); c.scale(zoom, zoom); c.translate(-cx, -cy)
    c.set_source_rgb(0.36, 0.5, 0.3); c.paint()
    r = random.Random(2)
    for _ in range(260):                                   # champs / bosquets
        x = r.random() * 1400 - 160; y = r.random() * 2200 - 140
        c.new_path(); c.arc(x, y, 8 + 18 * r.random(), 0, 7); c.set_source_rgba(0.2, 0.34, 0.18, 0.7); c.fill()
    c.save(); c.translate(320, 700); c.scale(1.4, 1.0); c.new_path(); c.arc(0, 0, 170, 0, 7); c.restore()   # lac
    lake = mix((0.2, 0.45, 0.75), (0.55, 0.55, 0.57), concrete); fill_stroke(c, lake, 8)
    if concrete > 0.3:
        rr_ = random.Random(6)
        for _ in range(8):
            a = rr_.random() * 6.28; c.move_to(320, 700)
            for s_ in range(3): c.line_to(320 + math.cos(a + rr_.uniform(-0.3, 0.3)) * 70 * (s_ + 1), 700 + math.sin(a + rr_.uniform(-0.3, 0.3)) * 50 * (s_ + 1))
        c.set_source_rgba(0.2, 0.2, 0.22, concrete); c.set_line_width(4); c.stroke()
    else:
        for j in range(5):
            y = 640 + j * 28; c.move_to(220 + 20 * math.sin(t * 2 + j), y); c.line_to(400 + 20 * math.sin(t * 2 + j), y); c.set_source_rgba(1, 1, 1, 0.3); c.set_line_width(4); c.stroke()
    c.new_path(); c.move_to(620, 500); c.curve_to(760, 440, 940, 480, 980, 600); c.curve_to(1000, 740, 860, 800, 720, 780); c.curve_to(600, 760, 560, 600, 620, 500); c.close_path()   # neige
    fill_stroke(c, (0.95, 0.97, 1.0), 8)
    for j in range(9):
        x = 660 + (j * 37) % 300; y = 540 + (j * 53) % 220
        c.new_path(); c.move_to(x, y - 26); c.line_to(x - 16, y + 10); c.line_to(x + 16, y + 10); c.close_path(); c.set_source_rgb(0.15, 0.3, 0.2); c.fill()
    c.new_path(); c.move_to(560, 1060); c.curve_to(700, 1000, 900, 1040, 940, 1160); c.curve_to(960, 1280, 780, 1320, 640, 1290); c.curve_to(520, 1260, 480, 1130, 560, 1060); c.close_path()   # marais
    fill_stroke(c, (0.42, 0.48, 0.3), 8)
    for j in range(7):
        c.save(); c.translate(600 + (j * 61) % 300, 1100 + (j * 41) % 170); c.scale(1.6, 0.7); c.new_path(); c.arc(0, 0, 18, 0, 7); c.restore(); c.set_source_rgba(0.25, 0.45, 0.6, 0.8); c.fill()
    for j in range(6):                                     # maisons
        rr(c, 180 + (j % 3) * 70, 1050 + (j // 3) * 70, 50, 50, 6); fill_stroke(c, (0.75, 0.72, 0.68), 5)
    c.restore()
    return lambda x, y: (W / 2 + (x - cx) * zoom, H / 2 + (y - cy) * zoom)


def reticle(c, x, y, r, t, col=WH):
    c.save(); c.translate(x, y); c.rotate(t * 0.8)
    for k in range(4):
        c.new_path(); c.arc(0, 0, r, k * math.pi / 2 + 0.25, k * math.pi / 2 + math.pi / 2 - 0.25); c.set_source_rgb(*col); c.set_line_width(8); c.stroke()
    c.restore()
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        c.move_to(x + dx * r * 0.55, y + dy * r * 0.55); c.line_to(x + dx * r * 1.25, y + dy * r * 1.25)
    c.set_source_rgb(*col); c.set_line_width(5); c.stroke()


def sc_fl_target(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k <= 3:
        z = 1.0 + 0.06 * (t - sg['t0'])
        tgt = {0: (540, 900), 1: (320, 700), 2: (320, 700)}.get(k, (790, 620) if p < 0.5 else (740, 1170))
        to_s = ground_map(c, t, z, 540, 900, concrete=ap(p, 0.2, 0.6) if k == 2 else (1.0 if k == 3 else 0.0))
        sx, sy = to_s(*tgt)
        reticle(c, sx, sy, 110, t, RED if k == 2 else (GRN if k == 3 else WH))
        if k == 0: stamp(c, "OÙ TOMBER ?", 540, 470, 140, WH, since)
        if k == 1: text(c, "?", sx, sy - 150, 160, YEL, glow=0.9); tag(c, "L'EAU", sx, sy + 230, BLUE)
        if k == 2:
            cross(c, sx, sy, 2.2, RED, ap(p, 0.4, 0.55)); stamp(c, "≈ BÉTON", 540, 470, 150, RED, since, glow=1.0)
        if k == 3:
            a1 = ap(p, 0.0, 0.2); a2 = ap(p, 0.5, 0.7)
            ns = to_s(790, 620); ms = to_s(740, 1170)
            check(c, ns[0] + 150, ns[1] - 120, 1.5, GRN, a1); tag(c, "NEIGE", ns[0], ns[1] + 210, GRN, a1)
            check(c, ms[0] + 160, ms[1] - 110, 1.5, GRN, a2); tag(c, "MARAIS", ms[0], ms[1] + 200, GRN, a2)
    else:
        sky(c, (0.35, 0.55, 0.85), (0.8, 0.88, 0.95))
        c.new_path(); c.rectangle(0, 1330, W, H); c.set_source_rgb(0.95, 0.97, 1.0); c.fill()
        c.move_to(0, 1330); c.line_to(W, 1330); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
        up_lines(c, t, 0.6)
        person(c, 330, 1040 + 6 * math.sin(t * 5), 1.2, t, 'brace', mood='determined')
        S = sg['sent']
        for j, (lab, (x, y), (ax, ay)) in enumerate((("PIEDS JOINTS", (770, 1290), (345, 1305)), ("GENOUX FLÉCHIS", (770, 1130), (400, 1205)), ("TÊTE PROTÉGÉE", (770, 760), (400, 850)))):
            ts = S[4][0] + (S[4][1] - S[4][0]) * (0.25 + 0.27 * j)
            a = ap(t, ts, ts + 0.25)
            if a <= 0: continue
            c.move_to(x - 190, y - 20); c.line_to(ax, ay); c.set_source_rgba(*YEL, a); c.set_line_width(5); c.stroke()
            c.new_path(); c.arc(ax, ay, 10, 0, 7); c.set_source_rgba(*YEL, a); c.fill()
            tag(c, lab, x, y, YEL, a, 50)


def bomber(c, x, y, s, rot, t, smoke=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    for k in range(18):
        if smoke <= 0: break
        xx = 40 - k * 40; yy = 20 + k * 6 + 8 * math.sin(t * 2 + k)
        c.new_path(); c.arc(xx, yy, 16 + k * 5, 0, 7); c.set_source_rgba(0.15, 0.15, 0.17, smoke * (0.6 - k * 0.03)); c.fill()
    od = (0.36, 0.4, 0.28)
    c.new_path(); c.move_to(-300, -10); c.curve_to(-150, -40, 200, -42, 300, -10); c.curve_to(320, 10, 300, 30, 270, 32); c.curve_to(100, 40, -150, 34, -300, 14); c.close_path(); fill_stroke(c, od, 9)
    c.new_path(); c.move_to(-260, -14); c.line_to(-300, -150); c.line_to(-240, -150); c.line_to(-180, -24); c.close_path(); fill_stroke(c, od, 8)
    c.new_path(); c.move_to(-80, 6); c.line_to(140, 6); c.line_to(60, 60); c.line_to(-150, 60); c.close_path(); fill_stroke(c, mix(od, (0, 0, 0), 0.2), 8)
    for ex in (-40, 70):
        rr(c, ex, 22, 70, 30, 12); fill_stroke(c, (0.3, 0.32, 0.25), 6)
        c.new_path(); c.save(); c.translate(ex + 75, 37); c.scale(0.25, 1); c.arc(0, 0, 44, 0, 7); c.restore(); c.set_source_rgba(0.8, 0.85, 0.9, 0.3); c.fill()
    for i in range(5): rr(c, 160 + i * 20, -24, 12, 10, 3); c.set_source_rgb(0.6, 0.8, 0.95); c.fill()
    c.new_path(); c.arc(-60, -6, 22, 0, 7); c.set_source_rgb(0.95, 0.95, 0.97); c.fill(); c.new_path(); c.arc(-60, -6, 12, 0, 7); c.set_source_rgb(0.1, 0.2, 0.5); c.fill()
    c.restore()


def station(c, shatter=0.0, t=0.0):
    """Gare 1940 : façade + grande verrière en arc."""
    c.set_source_rgb(0.12, 0.1, 0.1); c.paint()
    sky(c, (0.1, 0.1, 0.16), (0.42, 0.38, 0.4))
    c.new_path(); c.rectangle(0, 1180, W, H - 1180); c.set_source_rgb(0.22, 0.2, 0.2); c.fill()
    rr(c, 90, 900, 900, 520, 10); fill_stroke(c, (0.55, 0.36, 0.28), 9)                            # façade brique
    for j in range(6):
        rr(c, 140 + j * 140, 1110, 80, 150, 36); fill_stroke(c, (0.15, 0.13, 0.12), 6)
    c.new_path(); c.move_to(150, 910); c.curve_to(250, 650, 830, 650, 930, 910); c.close_path()              # verrière
    c.set_source_rgba(0.6, 0.8, 0.95, 0.55 * (1 - shatter) + 0.1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(9); c.stroke()
    for j in range(1, 8):
        x = 150 + j * 97.5; c.move_to(x, 910); c.line_to(540 + (x - 540) * 0.6, 720 + abs(x - 540) * 0.2)
    c.set_source_rgba(*INK, 0.7); c.set_line_width(4); c.stroke()
    text(c, "SAINT-NAZAIRE", 540, 1000, 60, (0.95, 0.9, 0.8))


def sc_fl_magee(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        c.set_source_rgb(0.16, 0.12, 0.08); c.paint(); radial(c, 540, 900, 700, SEPIA, 0.25)
        for side in (60, W - 60):                          # pellicule
            c.new_path(); c.rectangle(side - 40, 0, 80, H); c.set_source_rgb(0.05, 0.04, 0.03); c.fill()
            for j in range(14):
                y = (j * 150 + t * 300) % (H + 150) - 75; rr(c, side - 18, y, 36, 50, 8); c.set_source_rgb(0.85, 0.8, 0.7); c.fill()
        stamp(c, "ÇA A DÉJÀ", 540, 820, 150, SEPIA, since); stamp(c, "MARCHÉ", 540, 1020, 190, YEL, since - 0.2, glow=1.0)
    elif k == 1:
        sky(c, (0.3, 0.38, 0.5), (0.7, 0.68, 0.62))
        r = random.Random(9)
        for j in range(10):                                # flak
            x = r.random() * W; y = 200 + r.random() * 700; ph = (t * 0.7 + r.random()) % 1
            c.new_path(); c.arc(x, y, 20 + 40 * ph, 0, 7); c.set_source_rgba(0.1, 0.1, 0.1, 0.6 * (1 - ph)); c.fill()
        bomber(c, 560, 600, 1.05, 0.08 + 0.05 * math.sin(t), t)
        y = 680 + 460 * ap(p, 0.2, 1.0) ** 1.3
        person(c, 520, y, 0.35, t, 'limp', col=(0.4, 0.42, 0.3), closed=True, rot=t * 2)
        stamp(c, "1943", 540, 1290, 170, SEPIA, since, glow=0.6)
        label(c, "ALAN MAGEE · 6 700 M", 540, 1370, 50, WH)
    else:
        sh = ap(p, 0.42, 0.5)
        station(c, sh, t)
        y = 380 + 330 * ap(p, 0.0, 0.45) + 300 * ap(p, 0.45, 0.6)
        person(c, 540, y, 0.45, t, 'limp', col=(0.4, 0.42, 0.3), closed=True, rot=t * 3 * (1 - sh))
        if sh > 0:
            r = random.Random(12)
            for _ in range(40):
                a = r.uniform(3.4, 6.0); d = 60 + 420 * eout((p - 0.42) / 0.3) * r.random()
                x = 540 + math.cos(a) * d; yy = 740 + math.sin(a) * d * 0.5 + 300 * ap(p, 0.45, 0.9) * r.random()
                c.save(); c.translate(x, yy); c.rotate(r.random() * 6); c.new_path(); c.move_to(0, -12); c.line_to(10, 8); c.line_to(-9, 6); c.close_path()
                c.set_source_rgba(0.75, 0.9, 1.0, 0.85); c.fill(); c.restore()
            fl = max(0, 1 - (p - 0.42) * 8); c.set_source_rgba(1, 1, 1, 0.7 * fl); c.paint()
        tag(c, "GARE DE SAINT-NAZAIRE", 540, 560, WH, 1, 60)
        if p > 0.72: stamp(c, "IL SURVIT", 540, 1330, 150, GRN, since - 0.72 * (sg['end'] - sg['sent'][2][0]), glow=1.0)


def fuselage_chunk(c, x, y, s, rot):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.new_path(); c.move_to(-170, -60); c.line_to(150, -62); c.line_to(170, -40); c.line_to(150, -10); c.line_to(175, 20); c.line_to(150, 60)
    c.line_to(-160, 62); c.line_to(-180, 30); c.line_to(-165, 0); c.line_to(-185, -30); c.close_path()
    g = cairo.LinearGradient(0, -62, 0, 62); g.add_color_stop_rgb(0, 0.95, 0.95, 0.97); g.add_color_stop_rgb(1, 0.6, 0.62, 0.68); c.set_source(g); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
    for i in range(7): rr(c, -130 + i * 40, -30, 20, 22, 7); c.set_source_rgb(0.2, 0.3, 0.45); c.fill()
    c.new_path(); c.rectangle(-170, 12, 340, 8); c.set_source_rgb(0.1, 0.2, 0.5); c.fill()
    c.restore()


def snowy_slope(c, t, puff=0.0, px=600):
    sky(c, (0.18, 0.2, 0.32), (0.62, 0.62, 0.7))
    c.new_path(); c.move_to(0, 1050); c.line_to(W, 1300); c.line_to(W, H); c.line_to(0, H); c.close_path(); fill_stroke(c, (0.93, 0.95, 0.99), 8)
    r = random.Random(17)
    for j in range(16):                                    # sapins
        x = r.random() * W; y = 1050 + 250 * x / W + 40 + r.random() * 380; s = 0.6 + 0.6 * r.random()
        c.new_path(); c.move_to(x, y - 120 * s); c.line_to(x - 45 * s, y); c.line_to(x + 45 * s, y); c.close_path(); fill_stroke(c, (0.12, 0.28, 0.2), 5)
        c.new_path(); c.move_to(x, y - 120 * s); c.line_to(x - 18 * s, y - 70 * s); c.line_to(x + 18 * s, y - 70 * s); c.close_path(); c.set_source_rgb(0.97, 0.98, 1); c.fill()
    r2 = random.Random(1)
    for _ in range(70):                                    # neige qui tombe
        x = (r2.random() * W + t * 20) % W; y = (r2.random() * H + t * 80) % H
        c.new_path(); c.arc(x, y, 2 + 3 * r2.random(), 0, 7); c.set_source_rgba(1, 1, 1, 0.7); c.fill()
    if puff > 0:
        for j in range(14):
            a = math.pi + j * math.pi / 13; d = 60 + 220 * eout(puff)
            c.new_path(); c.arc(px + math.cos(a) * d, 1160 + math.sin(a) * d * 0.5, 40 + 30 * puff, 0, 7); c.set_source_rgba(1, 1, 1, 0.8 * (1 - puff)); c.fill()


def sc_fl_vesna(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        land = ap(p, 0.62, 0.7)
        snowy_slope(c, t, puff=ap(p, 0.66, 1.0), px=600)
        y = 420 + 700 * ap(p, 0.0, 0.66) ** 1.5
        fuselage_chunk(c, 600, min(y, 1120), 0.95, (1 - land) * (0.4 * math.sin(t * 1.2)) + 0.22 * land)
        stamp(c, "1972", 540, 560, 170, WH, since, glow=0.5)
        label(c, "VESNA VULOVIĆ · HÔTESSE", 540, 660, 46, WH)
    elif k == 1:
        c.set_source_rgb(0.02, 0.05, 0.04); c.paint(); radial(c, 540, 950, 600, GRN, 0.15)
        c.new_path(); x0 = 60
        for i in range(0, 961, 6):
            x = x0 + i; ph = ((x - since * 600) % 320) / 320
            yy = 950 - (220 if 0.45 < ph < 0.5 else (-90 if 0.5 < ph < 0.54 else 0))
            if x > x0 + since * 1100: break
            c.line_to(x, yy)
        c.set_source_rgb(*GRN); c.set_line_width(8); c.set_line_join(1); c.stroke()
        stamp(c, "ELLE SURVIT", 540, 600, 150, GRN, since, glow=1.0)
    else:
        c.set_source_rgb(0.05, 0.04, 0.02); c.paint(); radial(c, 540, 850, 600, YEL, 0.15)
        a = ap(p, 0.0, 0.15)
        c.new_path(); c.arc(540, 820, 230, 0, 7); fill_stroke(c, (0.95, 0.75, 0.25), 10, a)
        c.new_path(); c.arc(540, 820, 185, 0, 7); c.set_source_rgba(0.85, 0.6, 0.15, a); c.set_line_width(6); c.stroke()
        label(c, "RECORD DU MONDE", 540, 740, 40, (0.25, 0.15, 0.02), a)
        c.push_group(); text(c, "10 160 M", 540, 870, 120, (0.25, 0.15, 0.02)); c.pop_group_to_source(); c.paint_with_alpha(a)
        label(c, "GUINNESS", 540, 930, 36, (0.25, 0.15, 0.02), a)
        if p > 0.42:
            q = since - 0.42 * (sg['end'] - sg['sent'][2][0])
            stamp(c, "CONTESTÉ", 540, 840, 190, RED, q, rot=-0.18, glow=1.0)
            label(c, "2009 : DEUX JOURNALISTES ÉVOQUENT ~800 M", 540, 1200, 36, WH, ap(p, 0.55, 0.7))


def sc_fl_verdict(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    sky(c, (0.1, 0.02, 0.03), (0.02, 0.01, 0.01)); radial(c, 540, 1000, 650, RED, 0.14)
    if k == 0:
        stamp(c, "TU NE SURVIS", 540, 760, 150, WH, since); stamp(c, "PRESQUE JAMAIS", 540, 960, 160, RED, since - 0.35, glow=1.0)
    elif k == 1:
        label(c, "DE QUOI AMORTIR LE CHOC", 540, 540, 44, (0.9, 0.9, 0.95))
        for j, (lab, col) in enumerate((("VERRIÈRE", BLUE), ("NEIGE + ÉPAVE", WH))):
            x = 310 + j * 460; a = ap(p, 0.1 + 0.25 * j, 0.25 + 0.25 * j); dy = (1 - eout(a)) * 120
            if a <= 0: continue
            c.save(); c.translate(0, dy)
            rr(c, x - 200, 620, 400, 560, 40); c.set_source_rgba(*col, 0.08 * a); c.fill_preserve(); c.set_source_rgba(*col, 0.85 * a); c.set_line_width(6); c.stroke()
            if j == 0:
                c.new_path(); c.move_to(x - 150, 950); c.curve_to(x - 100, 780, x + 100, 780, x + 150, 950); c.close_path(); c.set_source_rgba(0.6, 0.8, 0.95, 0.6 * a); c.fill_preserve(); c.set_source_rgba(*INK, a); c.set_line_width(6); c.stroke()
            else:
                c.new_path(); c.move_to(x - 170, 1000); c.line_to(x + 170, 900); c.line_to(x + 170, 1060); c.line_to(x - 170, 1060); c.close_path(); c.set_source_rgba(0.95, 0.97, 1, a); c.fill()
                c.push_group(); fuselage_chunk(c, x, 880, 0.55, 0.25); c.pop_group_to_source(); c.paint_with_alpha(a)
            label(c, lab, x, 1130, 54, col, a, 'Bebas Neue')
            check(c, x, 700, 1.0, GRN, a)
    else:
        rising_clouds(c, t, 700, 5, 3, 0.15)
        person(c, 540, 1080, 1.3, t, 'spread', mood='worried', look=(0, -6), col=(0.25, 0.45, 0.75))
        stamp(c, "ET TOI ?", 540, 560, 170, ORG, since, glow=1.0)


# =============================== HISTOIRE VRAIE : Roland Garros ===============================
def morane(c, x, y, rot, s, lt, prop=1.0, smoke=0.0, pilot=True, gearw=True):
    """Monoplan Morane-Saulnier 1913, vue de profil, nez à droite."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    for k in range(16):
        if smoke <= 0: break
        xx = 140 - k * 34; yy = 10 + k * 3 + 7 * math.sin(lt * 2 + k)
        c.new_path(); c.arc(xx, yy, 10 + k * 4, 0, 7); c.set_source_rgba(0.25, 0.25, 0.28, smoke * (0.55 - k * 0.03)); c.fill()
    wood, cloth = (0.72, 0.52, 0.3), (0.94, 0.89, 0.74)
    if gearw:                                               # train : V + roue + patin
        c.move_to(60, 20); c.line_to(40, 78); c.line_to(95, 20); c.set_source_rgb(*INK); c.set_line_width(12); c.stroke()
        c.move_to(60, 20); c.line_to(40, 78); c.line_to(95, 20); c.set_source_rgb(*wood); c.set_line_width(6); c.stroke()
        c.new_path(); c.arc(40, 82, 24, 0, 7); fill_stroke(c, (0.15, 0.15, 0.16), 6); c.new_path(); c.arc(40, 82, 8, 0, 7); c.set_source_rgb(0.7, 0.7, 0.72); c.fill()
        c.move_to(-230, 6); c.line_to(-250, 30); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    c.new_path(); c.move_to(150, -24); c.curve_to(60, -28, -120, -18, -250, -4); c.line_to(-250, 8); c.curve_to(-120, 22, 60, 28, 150, 24); c.close_path()   # fuselage toilé
    g = cairo.LinearGradient(0, -28, 0, 28); g.add_color_stop_rgb(0, 1, 0.97, 0.86); g.add_color_stop_rgb(1, 0.78, 0.72, 0.58); c.set_source(g); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(8); c.set_line_join(1); c.stroke()
    for j in range(8):
        xx = 120 - j * 42; c.move_to(xx, -22 + j * 2); c.line_to(xx, 22 - j * 2)
    c.set_source_rgba(0.55, 0.45, 0.3, 0.6); c.set_line_width(3); c.stroke()
    c.new_path(); c.move_to(-235, -4); c.curve_to(-250, -70, -300, -75, -305, -30); c.curve_to(-300, 0, -270, 10, -235, 8); c.close_path(); fill_stroke(c, cloth, 7)   # dérive arrondie
    c.new_path(); c.move_to(-200, 2); c.line_to(-300, 0); c.line_to(-290, 12); c.line_to(-200, 10); c.close_path(); fill_stroke(c, cloth, 5)
    c.move_to(40, -30); c.line_to(55, -92); c.line_to(75, -30); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()   # pylône + haubans
    for wx in (-70, 160):
        c.move_to(55, -92); c.line_to(wx, -24); c.move_to(40, 26); c.line_to(wx, -18)
    c.set_source_rgba(*INK, 0.7); c.set_line_width(2.5); c.stroke()
    c.new_path(); c.move_to(-70, -24); c.curve_to(-20, -44, 120, -42, 160, -26); c.curve_to(120, -16, -20, -14, -70, -24); c.close_path(); fill_stroke(c, cloth, 6)   # aile (profil)
    if pilot:
        c.new_path(); c.arc(0, -36, 22, 0, 7); fill_stroke(c, (0.98, 0.98, 0.99), 6)
        c.new_path(); c.arc(0, -40, 23, math.pi, 2 * math.pi); c.close_path(); fill_stroke(c, (0.42, 0.26, 0.14), 5)
        c.new_path(); c.arc(10, -46, 7, 0, 7); c.set_source_rgb(0.5, 0.75, 0.9); c.fill()
        c.move_to(-20, -26); c.curve_to(-50, -22, -70, -10, -85, -14 + 5 * math.sin(lt * 9)); c.set_source_rgb(0.9, 0.9, 0.95); c.set_line_width(6); c.stroke()   # écharpe
    c.new_path(); c.move_to(150, -30); c.curve_to(185, -30, 192, 30, 150, 30); c.close_path(); fill_stroke(c, (0.62, 0.64, 0.68), 7)   # capot moteur rotatif
    if prop > 0.5:
        c.new_path(); c.save(); c.translate(196, 0); c.scale(0.18, 1); c.arc(0, 0, 95, 0, 7); c.restore(); c.set_source_rgba(0.85, 0.75, 0.55, 0.3 + 0.1 * math.sin(lt * 50)); c.fill()
    else:
        a = lt * 8 * prop
        c.move_to(196, -95 * math.cos(a)); c.line_to(196, 95 * math.cos(a)); c.set_source_rgb(*INK); c.set_line_width(14); c.stroke()
        c.move_to(196, -95 * math.cos(a)); c.line_to(196, 95 * math.cos(a)); c.set_source_rgb(*wood); c.set_line_width(8); c.stroke()
    c.new_path(); c.arc(196, 0, 9, 0, 7); c.set_source_rgb(*INK); c.fill()
    c.restore()


def med_bg(c, lt, horizon=1000, tod='day'):
    tops = {'day': ((0.25, 0.5, 0.85), (0.75, 0.85, 0.95)), 'dawn': ((0.12, 0.15, 0.38), (0.98, 0.62, 0.38)), 'noon': ((0.2, 0.5, 0.9), (0.85, 0.92, 0.98)), 'dusk': ((0.12, 0.1, 0.25), (0.85, 0.42, 0.3))}[tod]
    g = cairo.LinearGradient(0, 0, 0, horizon); g.add_color_stop_rgb(0, *tops[0]); g.add_color_stop_rgb(1, *tops[1]); c.rectangle(0, 0, W, horizon); c.set_source(g); c.fill()
    sx, sy = (820, horizon - 120) if tod in ('dawn', 'dusk') else (820, 330)
    radial(c, sx, sy, 300, (1, 0.92, 0.7), 0.5); c.new_path(); c.arc(sx, sy, 60, 0, 7); c.set_source_rgb(1, 0.95, 0.8); c.fill()
    g = cairo.LinearGradient(0, horizon, 0, H); sea = (0.1, 0.35, 0.6) if tod != 'dawn' else (0.15, 0.2, 0.4)
    g.add_color_stop_rgb(0, *mix(sea, (0.7, 0.8, 0.9), 0.4)); g.add_color_stop_rgb(1, *mix(sea, (0, 0, 0), 0.4)); c.rectangle(0, horizon, W, H - horizon); c.set_source(g); c.fill()
    r = random.Random(3)
    for k in range(60):
        y = horizon + 10 + (r.random() ** 1.6) * (H - horizon); x = (r.random() * W - lt * 30 * (1 + y / H)) % W; L = 20 + 60 * (y - horizon) / (H - horizon)
        c.move_to(x, y); c.line_to(x + L, y); c.set_source_rgba(1, 1, 1, 0.18); c.set_line_width(2 + 3 * (y - horizon) / (H - horizon)); c.stroke()
    for k in range(14):
        y = horizon + 8 + k * 30; w = 150 - k * 8
        rr(c, sx - w / 2 + 20 * math.sin(lt * 1.6 + k), y, max(8, w), 6, 3); c.set_source_rgba(1, 0.95, 0.8, max(0, 0.35 - k * 0.02)); c.fill()


def garros_head(c, x, y, r, t, mood='determined', look=(0, 0)):
    head(c, x, y, r, mood, look, helmet=False)
    c.new_path(); c.arc(x, y - r * 0.08, r * 1.05, math.pi * 1.0, math.pi * 2.0); c.close_path(); fill_stroke(c, (0.42, 0.26, 0.14), 8)   # casque cuir
    for sx in (-1, 1):
        rr(c, x + sx * r * 0.95 - r * 0.15, y - r * 0.15, r * 0.3, r * 0.6, r * 0.12); fill_stroke(c, (0.42, 0.26, 0.14), 6)
    c.move_to(x - r * 1.0, y - r * 0.55); c.line_to(x + r * 1.0, y - r * 0.55); c.set_source_rgb(0.2, 0.15, 0.1); c.set_line_width(r * 0.1); c.stroke()
    for sx in (-1, 1):                                      # lunettes relevées
        c.new_path(); c.arc(x + sx * r * 0.32, y - r * 0.6, r * 0.24, 0, 7); fill_stroke(c, (0.55, 0.78, 0.92), 6)
        c.new_path(); c.arc(x + sx * r * 0.32 - r * 0.06, y - r * 0.66, r * 0.06, 0, 7); c.set_source_rgb(1, 1, 1); c.fill()
    if (t + x * 0.001) % 3.7 < 0.12:
        for sx in (-1, 1):
            ex, ey = x + sx * r * 0.33 + look[0], y + r * 0.02 + look[1]
            c.new_path(); c.arc(ex, ey, r * 0.15, 0, 7); c.set_source_rgb(0.98, 0.98, 0.99); c.fill()
            c.move_to(ex - r * 0.12, ey); c.line_to(ex + r * 0.12, ey); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()


def LL(lon, lat): return 60 + (lon - 3) * 106.7, 380 + (44.5 - lat) * 115


def med_map(c, t, prog=0.0, col=ORG, dim=0.0):
    c.set_source_rgb(0.12, 0.32, 0.55); c.paint()
    r = random.Random(4)
    for _ in range(50):
        x = r.random() * W; y = 500 + r.random() * 800; c.move_to(x + 10 * math.sin(t + x), y); c.line_to(x + 40 + 10 * math.sin(t + x), y); c.set_source_rgba(1, 1, 1, 0.12); c.set_line_width(3); c.stroke()
    land = (0.86, 0.78, 0.58)
    fr = [(3, 43.3), (4.5, 43.4), (5.4, 43.2), (6.2, 43.1), (6.74, 43.43), (7.3, 43.7), (8.0, 43.9), (8.9, 44.4), (9.8, 44.05), (10.3, 43.5), (10.6, 42.9), (11.2, 42.4), (12, 41.9)]
    c.new_path(); c.move_to(0, 0); c.line_to(*LL(3, 43.3))
    for lo, la in fr: c.line_to(*LL(lo, la))
    c.line_to(W, LL(12, 41.9)[1]); c.line_to(W, 0); c.close_path(); fill_stroke(c, land, 7)
    af = [(3, 36.8), (4.5, 36.9), (5.3, 36.65), (6.6, 37.1), (7.75, 36.9), (8.6, 36.95), (9.2, 37.25), (9.87, 37.27), (10.3, 37.05), (11.05, 37.05), (11.1, 36.7), (12, 36.3)]
    c.new_path(); c.move_to(0, H); c.line_to(*LL(3, 36.8))
    for lo, la in af: c.line_to(*LL(lo, la))
    c.line_to(W, LL(12, 36.3)[1]); c.line_to(W, H); c.close_path(); fill_stroke(c, land, 7)
    for pts in ([(9.4, 43.0), (9.55, 42.6), (9.4, 41.9), (9.25, 41.4), (8.8, 41.6), (8.6, 42.1), (8.55, 42.5), (9.0, 42.75)],
                [(9.6, 41.2), (9.8, 40.6), (9.6, 39.9), (9.5, 39.2), (9.0, 39.0), (8.4, 39.0), (8.4, 39.6), (8.5, 40.4), (8.2, 40.9), (8.8, 41.0)]):
        c.new_path(); c.move_to(*LL(*pts[0]))
        for lo, la in pts[1:]: c.line_to(*LL(lo, la))
        c.close_path(); fill_stroke(c, land, 6)
    for name, (lo, la), dx, col in (("CORSE", (9.0, 42.2), 150, WH), ("SARDAIGNE", (9.0, 40.1), 190, WH), ("FRANCE", (5.0, 44.1), 0, (0.35, 0.28, 0.18)), ("TUNISIE", (9.4, 36.6), 0, (0.35, 0.28, 0.18))):
        x, y = LL(lo, la); label(c, name, x + dx, y + 12, 34, col)
    a, b = LL(6.74, 43.43), LL(9.87, 37.27)
    if prog > 0:
        n = 40; m = int(n * prog)
        for j in range(m):
            q0, q1 = j / n, (j + 0.55) / n
            c.move_to(a[0] + (b[0] - a[0]) * q0, a[1] + (b[1] - a[1]) * q0); c.line_to(a[0] + (b[0] - a[0]) * q1, a[1] + (b[1] - a[1]) * q1)
        c.set_source_rgb(*col); c.set_line_width(9); c.set_line_cap(1); c.stroke()
        q = prog; px, py = a[0] + (b[0] - a[0]) * q, a[1] + (b[1] - a[1]) * q
        c.new_path(); c.arc(px, py, 14 + 3 * math.sin(t * 8), 0, 7); c.set_source_rgb(*col); c.fill()
    for (x, y), nm in ((a, "FRÉJUS"), (b, "BIZERTE")):
        c.new_path(); c.arc(x, y, 13, 0, 7); fill_stroke(c, RED, 5); tag(c, nm, x, y - 30, WH, 1, 40)
    if dim > 0: c.set_source_rgba(0, 0, 0, dim); c.paint()


def clay_court(c, t, sc=1.0):
    sky(c, (0.35, 0.6, 0.9), (0.8, 0.88, 0.95))
    c.new_path(); c.rectangle(0, 640, W, H); c.set_source_rgb(0.12, 0.32, 0.2); c.fill()
    c.new_path(); c.move_to(300, 700); c.line_to(780, 700); c.line_to(1040, 1420); c.line_to(40, 1420); c.close_path(); c.set_source_rgb(0.80, 0.42, 0.22); c.fill()
    c.set_source_rgb(1, 1, 1); c.set_line_width(6)
    for (x0, y0, x1, y1) in ((300, 700, 40, 1420), (780, 700, 1040, 1420), (300, 700, 780, 700), (40, 1420, 1040, 1420), (540, 760, 540, 1360), (250, 820, 830, 820), (120, 1280, 960, 1280)):
        c.move_to(x0, y0); c.line_to(x1, y1)
    c.stroke()
    c.move_to(170, 1030); c.line_to(910, 1030); c.set_source_rgb(0.95, 0.95, 0.95); c.set_line_width(5); c.stroke()
    for j in range(25):
        x = 170 + j * 30.8; c.move_to(x, 960); c.line_to(x, 1030)
    c.set_source_rgba(0.1, 0.1, 0.1, 0.5); c.set_line_width(2); c.stroke()
    c.move_to(170, 960); c.line_to(910, 960); c.set_source_rgb(1, 1, 1); c.set_line_width(8); c.stroke()
    ph = (t * 1.2) % 1; bx = 300 + 480 * ph; by = 1250 - 900 * ph + 900 * ph * ph
    c.new_path(); c.arc(bx, by, 18, 0, 7); fill_stroke(c, (0.85, 0.95, 0.2), 4)


def sc_gr_hook(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        clay_court(c, t)
        if p > 0.35: stamp(c, "TENNIS ?", 540, 1290, 150, YEL, since - 0.35 * (sg['sent'][1][0] - sg['sent'][0][0]), glow=1.0)
    elif k == 1:
        clay_court(c, t); c.set_source_rgba(0.02, 0.03, 0.08, 0.55); c.paint()
        morane(c, -300 + 1500 * ap(p, 0.0, 1.0), 860, -0.05, 1.5, t)
        stamp(c, "PILOTE", 540, 1300, 170, ORG, since, glow=1.0)
    else:
        med_map(c, t, prog=0.0)
        a, b = LL(6.74, 43.43), LL(9.87, 37.27)
        c.move_to(*a); c.line_to(*b); c.set_source_rgba(1, 1, 1, 0.6); c.set_dash([18, 16]); c.set_line_width(6); c.stroke(); c.set_dash([])
        text(c, "?", (a[0] + b[0]) / 2 + 120, (a[1] + b[1]) / 2, 180, YEL, glow=0.9)
        stamp(c, "1913", 280, 1000, 160, WH, since, glow=0.6)


def sc_gr_takeoff(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        med_bg(c, t, 1100, 'dawn')
        rr(c, 270, 470, 540, 330, 26); fill_stroke(c, (0.98, 0.97, 0.94), 9)
        rr(c, 270, 470, 540, 90, 26); c.set_source_rgb(*RED); c.fill(); label(c, "SEPTEMBRE 1913", 540, 535, 44, WH)
        text(c, "23", 540, 760, 200, (0.1, 0.1, 0.15))
        mm = 47 * ap(p, 0.3, 0.9) if p < 0.9 else 47
        clock(c, 540, 1110, 170, 5, mm)
        if p > 0.6: tag(c, "5 H 47", 540, 1360, YEL, ap(p, 0.6, 0.75), 70)
    elif k == 1:
        med_bg(c, t, 1000, 'dawn')
        c.new_path(); c.rectangle(0, 1180, W, H); c.set_source_rgb(0.25, 0.35, 0.2); c.fill()
        for j in range(14):
            x = (j * 110 - t * 600 * (1 - ap(p, 0.6, 1))) % (W + 100) - 50; c.move_to(x, 1250); c.line_to(x + 30, 1240); c.set_source_rgba(0.5, 0.65, 0.35, 0.8); c.set_line_width(4); c.stroke()
        lift = ap(p, 0.3, 0.8)
        morane(c, 280 + 440 * ap(p, 0.0, 0.8), 1130 - 330 * lift, -0.16 * lift, 1.25, t, gearw=True)
        stamp(c, "FRÉJUS", 540, 560, 160, WH, since)
        if p > 0.55: tag(c, "BOIS + TOILE", 540, 1360, YEL, ap(p, 0.55, 0.7), 64)
    else:
        med_map(c, t, prog=ap(p, 0.1, 0.95))
        stamp(c, "SANS ESCALE", 540, 1405, 110, ORG, since, glow=1.0)


def sc_gr_sea(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        med_bg(c, t, 760, 'day')
        morane(c, 200 + 120 * p, 560, 0.0, 0.42, t)
        n = int(800 * ap(p, 0.05, 0.8)) // 10 * 10
        stamp(c, f"{n} KM", 540, 1180, 200, WH, since, rot=0, glow=0.6)
        label(c, "DE MER", 540, 1270, 56, WH)
    elif k == 1:
        c.set_source_rgb(0.05, 0.07, 0.12); c.paint(); radial(c, 540, 900, 600, (0.4, 0.5, 0.8), 0.18)
        rr(c, 330, 800, 420, 260, 30); fill_stroke(c, (0.42, 0.3, 0.2), 9)
        c.new_path(); c.arc(450, 930, 70, 0, 7); fill_stroke(c, (0.85, 0.8, 0.65), 6)
        for j in range(3): rr(c, 560, 870 + j * 40, 140, 16, 6); c.set_source_rgb(0.2, 0.15, 0.1); c.fill()
        c.move_to(700, 800); c.line_to(780, 600); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
        for j in range(3):
            ph = (t * 1.5 + j / 3) % 1; c.new_path(); c.arc(780, 600, 30 + 90 * ph, -2.4, -0.7); c.set_source_rgba(1, 1, 1, 0.5 * (1 - ph)); c.set_line_width(5); c.stroke()
        no_sign(c, 540, 900, 300, min(1, since / 0.2))
        stamp(c, "PAS DE RADIO", 540, 560, 140, RED, since, glow=0.9)
    else:
        c.set_source_rgb(0.08, 0.06, 0.04); c.paint(); radial(c, 540, 900, 700, SEPIA, 0.2)
        x, y, r = 320, 880, 190
        c.new_path(); c.arc(x, y, r, 0, 7); fill_stroke(c, (0.75, 0.6, 0.35), 10)
        c.new_path(); c.arc(x, y, r * 0.86, 0, 7); c.set_source_rgb(0.97, 0.94, 0.85); c.fill()
        for j, nm in enumerate("NESO"):
            a = -math.pi / 2 + j * math.pi / 2; text(c, nm, x + math.cos(a) * r * 0.66, y + math.sin(a) * r * 0.66 + 20, 54, (0.2, 0.15, 0.1))
        a = 0.35 * math.sin(t * 1.7) + 0.6
        c.save(); c.translate(x, y); c.rotate(a)
        c.new_path(); c.move_to(0, -r * 0.62); c.line_to(18, 0); c.line_to(-18, 0); c.close_path(); c.set_source_rgb(*RED); c.fill()
        c.new_path(); c.move_to(0, r * 0.62); c.line_to(18, 0); c.line_to(-18, 0); c.close_path(); c.set_source_rgb(0.2, 0.2, 0.25); c.fill(); c.restore()
        tag(c, "BOUSSOLE", x, 1160, SEPIA, 1, 54)
        a2 = ap(p, 0.35, 0.5)
        if a2 > 0:
            gx = 770; rr(c, gx - 110, 660, 220, 420, 30); fill_stroke(c, (0.55, 0.15, 0.12), 9, a2)
            lvl = 0.95 - 0.1 * math.sin(t); rr(c, gx - 80, 700 + 340 * (1 - lvl), 160, 340 * lvl, 20); c.set_source_rgba(1, 0.75, 0.25, a2); c.fill()
            tag(c, "≈ 8 H", gx, 1160, YEL, a2, 60)


def islands_h(c, horizon, which='corse', a=1.0):
    c.new_path(); c.move_to(0, horizon)
    if which == 'corse':
        for x, h in ((80, 40), (160, 120), (230, 80), (300, 160), (370, 90), (440, 60), (520, 0)): c.line_to(x, horizon - h)
    else:
        for x, h in ((0, 60), (200, 90), (420, 70), (650, 110), (880, 80), (W, 70)): c.line_to(x, horizon - h)
        c.line_to(W, horizon)
    c.close_path(); c.set_source_rgba(0.3, 0.38, 0.42, a); c.fill()


def sc_gr_fail(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        med_bg(c, t, 1020, 'day'); islands_h(c, 1020, 'corse')
        sput = (t * 4) % 1 < 0.45
        morane(c, 560, 780 + (6 * math.sin(t * 30) if sput else 0), 0.05, 1.3, t, prop=0.0 if sput else 1.0, smoke=0.9)
        if sput: label(c, "TEUF… TEUF…", 540, 560, 70, RED, 1, 'Bebas Neue')
        tag(c, "CORSE", 300, 1090, WH, 1, 44)
        stamp(c, "PANNE 1", 540, 1300, 160, RED, since, glow=1.0)
    elif k == 1:
        med_bg(c, t, 1100, 'day'); speedlines(c, t, 0.6)
        garros_head(c, 540, 820, 190, t, 'determined', (10, 0))
        c.move_to(360, 1010); c.curve_to(300, 1050, 220, 1060, 120, 1040 + 10 * math.sin(t * 9)); c.set_source_rgb(0.95, 0.95, 0.98); c.set_line_width(26); c.set_line_cap(1); c.stroke()
        stamp(c, "RÉGLÉ", 540, 1310, 170, GRN, since, glow=1.0)
    elif k == 2:
        sky(c, (0.3, 0.55, 0.88), (0.8, 0.88, 0.95))
        c.new_path(); c.move_to(0, 1080); c.curve_to(300, 1020, 700, 1100, W, 1040); c.line_to(W, H); c.line_to(0, H); c.close_path(); c.set_source_rgb(0.55, 0.6, 0.38); c.fill()
        c.new_path(); c.move_to(0, 1080); c.curve_to(300, 1020, 700, 1100, W, 1040); c.set_source_rgb(0.95, 0.9, 0.75); c.set_line_width(14); c.stroke()
        sput = (t * 4) % 1 < 0.5
        morane(c, 540, 720 + (6 * math.sin(t * 30) if sput else 0), 0.08, 1.25, t, prop=0.0 if sput else 1.0, smoke=1.0)
        tag(c, "SARDAIGNE", 540, 1200, WH, 1, 50)
        stamp(c, "PANNE 2", 540, 560, 160, RED, since, glow=1.0)
    else:
        med_bg(c, t, 1050, 'day')
        morane(c, 300 + 480 * p, 800 - 40 * p, -0.04, 1.1, t)
        speedlines(c, t, 0.7)
        stamp(c, "IL CONTINUE", 540, 1300, 150, ORG, since, glow=1.0)


def coast_tunisia(c, horizon, rise=1.0, t=0.0):
    h = 120 * rise
    c.new_path(); c.move_to(0, horizon)
    for x, hh in ((0, 0.3), (180, 0.5), (420, 0.45), (640, 0.7), (860, 0.5), (W, 0.4)): c.line_to(x, horizon - h * hh)
    c.line_to(W, horizon + 6); c.line_to(0, horizon + 6); c.close_path(); c.set_source_rgb(0.9, 0.8, 0.6); c.fill()
    for j in range(9):                                      # maisons blanches
        x = 200 + j * 80; y = horizon - h * 0.5
        rr(c, x, y - 30 * rise, 50, 30 * rise + 4, 4); c.set_source_rgb(0.98, 0.98, 0.98); c.fill()
    for x in (120, 760, 940):                               # palmiers
        y = horizon - h * 0.4; c.move_to(x, y); c.curve_to(x + 10, y - 70 * rise, x + 20, y - 100 * rise, x + 15, y - 130 * rise)
        c.set_source_rgb(0.4, 0.3, 0.2); c.set_line_width(8); c.stroke()
        for a in (-2.6, -2.0, -1.2, -0.6, 0.0):
            c.move_to(x + 15, y - 130 * rise); c.line_to(x + 15 + math.cos(a) * 60 * rise, y - 130 * rise + math.sin(a) * 30 * rise + 25 * rise)
        c.set_source_rgb(0.2, 0.45, 0.25); c.set_line_width(10); c.stroke()


def sc_gr_land(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        med_bg(c, t, 1150, 'noon')
        clock(c, 540, 820, 230, 13, 40)
        stamp(c, "13 H 40", 540, 1310, 170, WH, since, glow=0.6)
    elif k == 1:
        med_bg(c, t, 1000, 'noon'); coast_tunisia(c, 1000, ap(p, 0.0, 0.8), t)
        morane(c, 540, 760, 0.02, 0.9, t)
        stamp(c, "TUNISIE", 540, 560, 160, YEL, since, glow=0.8)
    elif k == 2:
        med_bg(c, t, 900, 'noon'); coast_tunisia(c, 900, 1.0, t)
        c.new_path(); c.rectangle(0, 920, W, H); c.set_source_rgb(0.85, 0.75, 0.52); c.fill()
        td = ap(p, 0.0, 0.6)
        x = 250 + 450 * ap(p, 0.0, 0.85); y = 760 + 400 * td
        morane(c, x, y, 0.1 * (1 - td), 1.2, t, prop=1.0 if p < 0.8 else 0.0)
        if td >= 1:
            for j in range(10):
                ph = (t * 1.5 + j / 10) % 1; c.new_path(); c.arc(x - 60 - 200 * ph, y + 90 - 30 * ph, 15 + 30 * ph, 0, 7); c.set_source_rgba(0.85, 0.75, 0.55, 0.6 * (1 - ph)); c.fill()
        stamp(c, "7 H 53", 540, 560, 180, YEL, since, glow=1.0)
        tag(c, "BIZERTE", 540, 690, WH, 1, 54)
    else:
        c.set_source_rgb(0.06, 0.05, 0.04); c.paint(); radial(c, 540, 900, 700, RED, 0.12)
        rr(c, 240, 620, 600, 560, 50); fill_stroke(c, (0.6, 0.62, 0.66), 10)
        lvl = 0.3 - 0.275 * ap(p, 0.0, 0.55)
        c.save(); rr(c, 255, 635, 570, 530, 40); c.clip()
        c.new_path(); c.move_to(255, 1165 - 530 * lvl)
        for x in range(255, 826, 15): c.line_to(x, 1165 - 530 * lvl + 6 * math.sin(x / 40 + t * 4))
        c.line_to(825, 1165); c.line_to(255, 1165); c.close_path(); c.set_source_rgb(1, 0.72, 0.2); c.fill(); c.restore()
        for j in range(4):
            yy = 1180 + 60 * ((t * 1.2 + j / 4) % 1); c.new_path(); c.arc(540, yy, 8, 0, 7); c.set_source_rgba(1, 0.72, 0.2, 0.8); c.fill()
        label(c, "RÉSERVOIR", 540, 700, 44, (0.15, 0.15, 0.18))
        stamp(c, "5 L", 540, 520, 200, RED, since, glow=1.0)
        if p > 0.5: label(c, "SUR UN PEU PLUS DE 200 L AU DÉPART", 540, 1300, 40, WH, ap(p, 0.5, 0.65))


def biplane_sil(c, x, y, s, rot, col=(0.05, 0.05, 0.08)):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.new_path(); c.move_to(-90, 0); c.line_to(80, -6); c.line_to(90, 6); c.line_to(-90, 8); c.close_path(); c.set_source_rgb(*col); c.fill()
    for yy in (-40, 10): rr(c, -40, yy, 110, 10, 4); c.set_source_rgb(*col); c.fill()
    c.move_to(0, -40); c.line_to(0, 10); c.move_to(50, -40); c.line_to(50, 10); c.set_source_rgb(*col); c.set_line_width(4); c.stroke()
    c.new_path(); c.move_to(-90, 0); c.line_to(-110, -30); c.line_to(-85, -30); c.close_path(); c.set_source_rgb(*col); c.fill()
    c.restore()


def sc_gr_end(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        med_bg(c, t, 1150, 'dusk')
        c.new_path(); c.rectangle(0, 1150, W, H); c.set_source_rgb(0.12, 0.1, 0.12); c.fill()
        a = t * 0.9
        biplane_sil(c, 540 + 300 * math.cos(a), 800 + 160 * math.sin(a), 1.5, a + math.pi / 2)
        fall = ap(p, 0.55, 1.0)
        x2 = 540 + 300 * math.cos(a + 2.6) + 150 * fall; y2 = 800 + 160 * math.sin(a + 2.6) + 380 * fall
        for j in range(16):
            if fall <= 0: break
            ph = j / 16; c.new_path(); c.arc(x2 - 150 * fall * ph, y2 - 380 * fall * ph, 10 + 20 * ph, 0, 7); c.set_source_rgba(0.15, 0.15, 0.17, 0.5 * (1 - ph) * min(1, fall * 3)); c.fill()
        biplane_sil(c, x2, y2, 1.5, a + 2.6 + math.pi / 2 + 2.5 * fall)
        stamp(c, "1918", 540, 560, 190, WH, since, glow=0.5)
        label(c, "5 OCTOBRE · LA VEILLE DE SES 30 ANS", 540, 1330, 38, WH, ap(p, 0.6, 0.75))
    elif k == 1:
        sky(c, (0.35, 0.6, 0.9), (0.8, 0.88, 0.95))
        for j in range(5):                                  # tribunes
            c.new_path(); c.arc(540, 1600, 1150 - j * 60, math.pi * 1.08, math.pi * 1.92); c.set_source_rgb(*mix((0.16, 0.36, 0.24), (0.3, 0.3, 0.32), j / 5)); c.set_line_width(56); c.stroke()
        r = random.Random(3)
        for _ in range(300):
            a = r.uniform(math.pi * 1.1, math.pi * 1.9); d = r.uniform(880, 1150)
            c.new_path(); c.arc(540 + math.cos(a) * d, 1600 + math.sin(a) * d, 5, 0, 7); c.set_source_rgb(*r.choice(((1, 1, 1), (0.9, 0.3, 0.2), (0.2, 0.4, 0.8), (1, 0.85, 0.3)))); c.fill()
        c.new_path(); c.move_to(250, 980); c.line_to(830, 980); c.line_to(980, 1420); c.line_to(100, 1420); c.close_path(); c.set_source_rgb(0.8, 0.42, 0.22); c.fill()
        c.set_source_rgb(1, 1, 1); c.set_line_width(5)
        for (x0, y0, x1, y1) in ((250, 980, 100, 1420), (830, 980, 980, 1420), (250, 980, 830, 980), (100, 1420, 980, 1420), (175, 1190, 905, 1190)): c.move_to(x0, y0); c.line_to(x1, y1)
        c.stroke()
        rr(c, 160, 800, 760, 120, 14); c.set_source_rgb(0.08, 0.24, 0.16); c.fill()
        name = "ROLAND-GARROS"; n = int(len(name) * ap(p, 0.2, 0.7)); text(c, name[:n], 540, 890, 96, WH)
        stamp(c, "1928", 540, 560, 170, YEL, since, glow=0.8)
    else:
        med_bg(c, t, 1150, 'day')
        morane(c, (t * 260) % (W + 600) - 300, 560, -0.03, 0.6, t)
        c.new_path(); c.arc(540, 900, 210, 0, 7); c.set_source_rgba(0, 0, 0, 0.35); c.fill()
        garros_head(c, 540, 900, 160, t, 'neutral', (0, -6))
        stamp(c, "TU LE SAVAIS ?", 540, 1310, 140, ORG, since, glow=1.0)


# =============================== TU ES LE PILOTE : ép. 3 ===============================
def twin(c, x, y, rot, lt, s=1.0, prop=1.0, flaps=0.0, gear=1.0, cough=False):
    """Bimoteur de la série (mêmes couleurs), moteur gauche hors service ; prop = moteur droit (1 tourne, 0 arrêté)."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    if cough:
        for k in range(6): c.new_path(); c.arc(110 + k * 30, 60 + k * 6, 14 + k * 6, 0, 7); c.set_source_rgba(0.2, 0.2, 0.25, 0.6 - k * 0.09); c.fill()
    if gear > 0:
        for gx in (-20, 150):
            L = 40 * gear; c.move_to(gx, 30); c.line_to(gx, 30 + L); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
            c.new_path(); c.arc(gx, 34 + L, 12 * gear + 1, 0, 7); fill_stroke(c, (0.12, 0.12, 0.14), 4)
    c.new_path(); c.move_to(-230, -10); c.curve_to(-120, -38, 150, -40, 230, -14); c.curve_to(260, -4, 262, 22, 232, 30); c.curve_to(100, 44, -120, 40, -230, 22); c.close_path(); fill_stroke(c, (0.92, 0.93, 0.96), 9)
    c.new_path(); c.move_to(-200, -12); c.line_to(-250, -110); c.line_to(-205, -110); c.line_to(-150, -20); c.close_path(); fill_stroke(c, (0.85, 0.2, 0.2), 8)
    for i in range(7): rr(c, -110 + i * 42, -18, 24, 18, 6); fill_stroke(c, (1, 0.85, 0.45), 4)
    c.new_path(); c.move_to(170, -28); c.curve_to(195, -34, 220, -26, 232, -12); c.line_to(185, -12); c.close_path(); fill_stroke(c, (0.35, 0.75, 1.0), 5)
    c.new_path(); c.move_to(-40, 14); c.line_to(80, 14); c.line_to(-10, 70); c.line_to(-90, 70); c.close_path(); fill_stroke(c, (0.8, 0.81, 0.86), 8)
    if flaps > 0:
        c.new_path(); c.move_to(-90, 70); c.line_to(-10, 70); c.line_to(-22, 70 + 38 * flaps); c.line_to(-102, 70 + 38 * flaps); c.close_path(); fill_stroke(c, (0.98, 0.75, 0.3), 6)
    rr(c, -40, 30, 110, 34, 16); fill_stroke(c, (0.6, 0.62, 0.68), 7)
    if prop > 0.5:
        c.new_path(); c.save(); c.translate(76, 47); c.scale(0.25, 1); c.arc(0, 0, 70, 0, 7); c.restore(); c.set_source_rgba(0.8, 0.85, 0.95, 0.25 + 0.1 * math.sin(lt * 40)); c.fill()
    else:
        a = lt * 10 * prop
        c.move_to(76, 47 - 60 * math.cos(a)); c.line_to(76, 47 + 60 * math.cos(a)); c.set_source_rgb(*INK); c.set_line_width(9); c.stroke()
    c.restore()


def pov_beach(c, lt, light=0.0, people=0.0, fire=0.0, frame=True, zoom=1.0):
    """Vue du pilote : plage de nuit qui file vers l'horizon (mer à gauche, dunes à droite). Point de fuite (540, 900)."""
    c.save(); c.translate(540, 900); c.scale(zoom, zoom); c.translate(-540, -900)
    g = cairo.LinearGradient(0, 0, 0, 900); g.add_color_stop_rgb(0, 0.02, 0.03, 0.08); g.add_color_stop_rgb(1, 0.08, 0.1, 0.2); c.rectangle(-300, -300, W + 600, 1200); c.set_source(g); c.fill()
    r = random.Random(5)
    for _ in range(160):
        c.new_path(); c.arc(r.random() * W, r.random() * 860, r.choice((1, 1.5, 2.2)), 0, 7); c.set_source_rgba(1, 1, 1, 0.3 + 0.6 * r.random()); c.fill()
    radial(c, 250, 380, 260, (1, 0.95, 0.8), 0.22); c.new_path(); c.arc(250, 380, 70, 0, 7); c.set_source_rgb(0.98, 0.96, 0.88); c.fill()
    Y = H + 300; wl = lambda y: 528 - 0.51 * (y - 900); wt = lambda y: 531 - 0.251 * (y - 900); dn = lambda y: 556 + 0.78 * (y - 900)
    c.new_path(); c.move_to(-300, 900); c.line_to(528, 900); c.line_to(wl(Y), Y); c.line_to(-300, Y); c.close_path(); c.set_source_rgb(0.03, 0.06, 0.13); c.fill()   # mer
    for k in range(18):
        y = 905 + k * k * 3.2; w = 24 + k * 12
        rr(c, 250 - w / 2 + 12 * math.sin(lt * 1.5 + k) - (y - 900) * 0.15, y, w, 3 + k * 0.4, 2); c.set_source_rgba(1, 0.95, 0.8, max(0, 0.34 - k * 0.017)); c.fill()
    c.new_path(); c.move_to(528, 900); c.line_to(556, 900); c.line_to(dn(Y), Y); c.line_to(wl(Y), Y); c.close_path(); c.set_source_rgb(0.44, 0.4, 0.31); c.fill()   # sable sec
    c.new_path(); c.move_to(528, 900); c.line_to(531, 900); c.line_to(wt(Y), Y); c.line_to(wl(Y), Y); c.close_path(); c.set_source_rgb(0.27, 0.26, 0.24); c.fill()   # sable mouillé
    for k in range(12):
        y = 910 + k * k * 7; x = wl(y) + 6 * math.sin(lt * 2 + k)
        c.move_to(x, y); c.line_to(x - 26 - k * 7, y + 3 + k); c.set_source_rgba(1, 1, 1, 0.4); c.set_line_width(2 + k * 0.5); c.stroke()   # écume
    c.new_path(); c.move_to(556, 900); c.curve_to(700, 880, 900, 860, W + 300, 870); c.line_to(W + 300, Y); c.line_to(dn(Y), Y); c.close_path(); c.set_source_rgb(0.05, 0.06, 0.06); c.fill()   # dunes
    for x, w_ in ((540, 22), (556, 16), (528, 12)):         # rochers au bout
        c.new_path(); c.arc(x, 903, w_, math.pi, 2 * math.pi); c.set_source_rgb(0.13, 0.13, 0.15); c.fill()
    if light > 0:                                            # cône du phare
        c.save(); c.new_path(); c.move_to(300, Y); c.line_to(505, 950); c.line_to(625, 950); c.line_to(980, Y); c.close_path(); c.clip()
        g = cairo.LinearGradient(0, 950, 0, H); g.add_color_stop_rgba(0, 1, 0.96, 0.85, 0.18 * light); g.add_color_stop_rgba(1, 1, 0.96, 0.85, 0.5 * light)
        c.set_source(g); c.paint(); c.restore()
    if fire > 0:
        R.flames(c, 562, 1052, 0.42, lt, fire); radial(c, 562, 1040, 200, (1, 0.55, 0.2), 0.35 * fire)
    if people > 0:
        for j, dx in enumerate((-48, -24, 30, 54)):
            x = 562 + dx; y = 1056; wave = math.sin(lt * 6 + j) * 9
            c.push_group()
            c.move_to(x, y); c.line_to(x - 8, y + 24); c.move_to(x, y); c.line_to(x + 8, y + 24); c.move_to(x, y); c.line_to(x, y - 28)
            c.move_to(x, y - 22); c.line_to(x - 13, y - 44 - wave); c.move_to(x, y - 22); c.line_to(x + 13, y - 44 + wave)
            c.set_source_rgb(*INK); c.set_line_width(6); c.set_line_cap(1); c.stroke()
            c.new_path(); c.arc(x, y - 38, 9, 0, 7); c.set_source_rgb(*mix(INK, (1, 0.8, 0.5), 0.35 * max(light, fire))); c.fill()
            c.pop_group_to_source(); c.paint_with_alpha(people)
    c.restore()
    if frame:                                               # montants + tableau de bord (sans cadrans : zone des sous-titres)
        c.new_path(); c.move_to(0, 0); c.line_to(W, 0); c.line_to(W, 150); c.curve_to(700, 205, 380, 205, 0, 150); c.close_path(); c.set_source_rgb(0.03, 0.03, 0.04); c.fill()
        c.new_path(); c.move_to(0, 0); c.line_to(70, 0); c.line_to(30, 1420); c.line_to(0, 1420); c.close_path(); c.fill()
        c.new_path(); c.move_to(W, 0); c.line_to(W - 70, 0); c.line_to(W - 30, 1420); c.line_to(W, 1420); c.close_path(); c.fill()
        c.new_path(); c.move_to(0, 1440); c.curve_to(380, 1385, 700, 1385, W, 1440); c.line_to(W, H); c.line_to(0, H); c.close_path(); c.set_source_rgb(0.05, 0.05, 0.07); c.fill()
        c.new_path(); c.move_to(150, 250); c.line_to(420, 225); c.set_source_rgba(1, 1, 1, 0.05); c.set_line_width(30); c.stroke()


def sc_e3_recap(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k < 2:
        R.ocean_bg(c, t)
        cough = k == 1 and ((t * 2.2) % 1 < 0.4)
        twin(c, 540 + (8 * math.sin(t * 40) if cough else 0), 760 + 8 * math.sin(t * 1.3), -0.03, t, 1.0, prop=0.0 if cough else 1.0, gear=0, cough=cough)
        if k == 0: stamp(c, "ÉPISODE 3", 540, 560, 150, WH, since, glow=0.6)
        else:
            if cough: text(c, "TEUF… TEUF…", 540, 560, 110, RED, glow=0.8)
            rr(c, 190, 1220, 700, 60, 28); c.set_source_rgba(1, 1, 1, 0.12); c.fill()
            rr(c, 198, 1228, 684 * (0.08 + 0.02 * math.sin(t * 3)), 44, 22); c.set_source_rgb(*RED); c.fill()
            label(c, "CARBURANT", 540, 1340, 44, (0.85, 0.88, 0.95))
    else:
        c.set_source_rgb(0.02, 0.03, 0.06); c.paint(); radial(c, 540, 900, 700, BLUE, 0.15)
        V = getattr(R.CFG, 'VOTES', dict(A=0, B=0, src="VOTES"))
        tot = max(1, V['A'] + V['B'])
        label(c, V.get('src', 'VOTES'), 540, 560, 46, (0.85, 0.88, 0.95))
        for j, (lab, txt, col) in enumerate((("A", "LA PLAGE", BLUE), ("B", "LA PISTE", ORG))):
            y = 700 + j * 260; v = V[lab]; w = 600 * v / tot * ap(p, 0.05 + 0.1 * j, 0.45 + 0.1 * j)
            text(c, lab, 150, y + 95, 150, col, glow=0.6)
            rr(c, 240, y, 620, 120, 30); c.set_source_rgba(1, 1, 1, 0.08); c.fill()
            if w > 1: rr(c, 250, y + 10, max(40, w), 100, 24); c.set_source_rgb(*col); c.fill()
            label(c, txt, 550, y + 80, 52, WH, 1, 'Bebas Neue')
            text(c, str(int(round(v * ap(p, 0.05 + 0.1 * j, 0.45 + 0.1 * j)))), 940, y + 90, 110, col)
        if p > 0.55:
            q = since - 0.55 * (sg['end'] - sg['sent'][2][0])
            rr(c, 120, 680, 840, 160, 36); c.set_source_rgb(*GRN); c.set_line_width(8); c.stroke()
            stamp(c, "A : LA PLAGE", 540, 1300, 140, GRN, q, glow=1.0)


def sc_e3_appr(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        R.ocean_bg(c, t, horizon=980)
        c.new_path(); c.move_to(0, 980); c.curve_to(300, 940, 700, 950, W, 960); c.line_to(W, 1000); c.line_to(0, 1000); c.close_path(); c.set_source_rgb(0.08, 0.12, 0.1); c.fill()
        rnd = random.Random(9)
        for _ in range(40):
            x = rnd.random() * W; c.new_path(); c.arc(x, 950 + rnd.random() * 30, 3 + rnd.random() * 3, 0, 7); c.set_source_rgba(1, 0.85, 0.45, 0.6 + 0.4 * math.sin(t * 3 + x)); c.fill()
        bank = -0.28 * math.sin(math.pi * ap(p, 0.0, 0.7)); fl = ap(p, 0.45, 0.9)
        twin(c, 540, 720, bank, t, 1.25, flaps=fl, gear=1.0)
        if fl > 0.2:
            c.new_path(); c.arc(540 - 70 * 1.25, 720 + 95 * 1.25, 80, 0, 7); c.set_source_rgba(*YEL, 0.9 * fl); c.set_line_width(6); c.stroke()
            tag(c, "VOLETS SORTIS", 540, 1300, YEL, fl, 70)
    else:
        pov_beach(c, t, zoom=1.0 + 0.05 * p)
        a1 = ap(p, 0.15, 0.3); a2 = ap(p, 0.5, 0.65)
        c.new_path(); c.move_to(528, 905); c.line_to(531, 905); c.line_to(405, 1400); c.line_to(273, 1400); c.close_path(); c.set_source_rgba(*GRN, 0.4 * a1); c.fill()
        tag(c, "MOUILLÉ = DUR", 300, 1250, GRN, a1, 56)
        tag(c, "SEC = MOU", 700, 1160, RED, a2, 56)
        if a1 > 0:
            c.move_to(420, 700); c.line_to(488, 1010); c.set_source_rgba(*GRN, a1); c.set_line_width(7); c.set_line_cap(1); c.stroke()
            c.move_to(470, 975); c.line_to(488, 1012); c.line_to(505, 972); c.stroke()
            stamp(c, "VISE ICI", 400, 640, 110, GRN, since - 0.15 * (sg['end'] - sg['sent'][1][0]))


def sc_e3_quit(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        pov_beach(c, t, zoom=1.05)
        stamp(c, "300 M", 540, 620, 200, ORG, since, glow=1.0)
    elif k == 1:
        R.ocean_bg(c, t, horizon=1000)
        st = ap(p, 0.45, 0.75)
        twin(c, 540, 760, -0.02, t * (1 - 0.8 * st), 1.3, prop=1.0 if st < 0.5 else 0.15 * (1 - st), gear=1.0, flaps=1.0)
        if st > 0.5:
            fl = max(0, 1 - (p - 0.6) * 5); c.set_source_rgba(1, 0.15, 0.15, 0.35 * fl); c.paint()
            stamp(c, "MOTEUR ARRÊTÉ", 540, 1300, 130, RED, since - 0.6 * (sg['sent'][2][0] - sg['sent'][1][0]), glow=1.0)
    elif k == 2:
        c.set_source_rgb(0.01, 0.01, 0.02); c.paint()
        c.new_path(); c.arc(820, 330, 70, 0, 7); c.set_source_rgba(0.98, 0.96, 0.88, 0.7); c.fill()
        c.push_group(); twin(c, 540, 900, 0.02, 0, 0.55, prop=0.0, gear=1, flaps=1); c.pop_group_to_source(); c.paint_with_alpha(0.25)
        label(c, "…", 540, 1150, 120, (0.6, 0.6, 0.7), 1, 'Bebas Neue')
    elif k == 3:
        c.set_source_rgb(0.02, 0.02, 0.04); c.paint()
        for j in range(26):
            ph = (t * 0.9 + j / 26) % 1; y = 300 + (j * 47) % 1100; x = W * (1.1 - 1.4 * ph)
            c.move_to(x, y); c.curve_to(x + 80, y - 20, x + 160, y + 20, x + 260, y); c.set_source_rgba(0.8, 0.85, 1, 0.35 * math.sin(math.pi * ph)); c.set_line_width(3); c.stroke()
        twin(c, 540, 900, 0.03, 0, 0.8, prop=0.0, gear=1, flaps=1)
    else:
        R.ocean_bg(c, t, horizon=1100)
        c.new_path(); c.move_to(0, 1100); c.line_to(W, 1100); c.line_to(W, 1180); c.line_to(0, 1160); c.close_path(); c.set_source_rgb(0.45, 0.4, 0.32); c.fill()
        x = 300 + 300 * p; y = 650 + 180 * p
        c.move_to(x + 200, y + 60); c.line_to(1000, 1110); c.set_source_rgba(1, 1, 1, 0.6); c.set_dash([20, 16]); c.set_line_width(5); c.stroke(); c.set_dash([])
        twin(c, x, y, 0.08, 0, 1.0, prop=0.0, gear=1, flaps=1)
        stamp(c, "PLANEUR", 540, 1320, 170, WH, since, glow=0.8)


def sc_e3_glide(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    c.set_source_rgb(0.03, 0.03, 0.05); c.paint()
    if k == 0:
        radial(c, 540, 900, 700, RED, 0.12)
        for j, x in enumerate((420, 660)):
            push = ap(p, 0.05 + 0.1 * j, 0.25 + 0.1 * j)
            rr(c, x - 30, 700, 60, 520, 26); fill_stroke(c, (0.15, 0.15, 0.18), 7)
            yy = 1100 - 330 * push
            c.move_to(x, 1180); c.line_to(x, yy); c.set_source_rgb(0.6, 0.62, 0.68); c.set_line_width(22); c.stroke()
            c.new_path(); c.arc(x, yy, 52, 0, 7); fill_stroke(c, (0.15, 0.15, 0.18), 7)
        label(c, "GAZ", 540, 660, 54, WH, 1, 'Bebas Neue')
        if p > 0.3:
            cross(c, 540, 940, 3.0, RED, ap(p, 0.3, 0.4))
            stamp(c, "PAS DE REMISE DES GAZ", 540, 1330, 96, RED, since - 0.3 * (sg['sent'][1][0] - sg['sent'][0][0]), glow=1.0)
    else:
        radial(c, 540, 820, 700, (0.3, 0.4, 0.8), 0.15)
        v = 150 + 12 * math.sin(t * 1.7)
        gauge(c, 540, 820, 300, v, 300, (0, 50, 100, 150, 200, 250), red_from=130, col=WH, unit="KM/H")
        tag(c, "DÉCROCHAGE", 330, 1180, RED, 1, 46)
        R.eyes_head(c, 730, 1250, 80, 'determined', (-20, -16), t)
        stamp(c, "GARDE TA VITESSE", 540, 470, 110, ORG, since)


def sc_e3_light(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    light = ap(p, 0.35, 0.5) if k == 0 else 1.0
    ppl = 0 if k == 0 else (ap(p, 0.1, 0.5) if k == 1 else 1)
    fire = 1.0 if k >= 2 else 0.0
    zoom = 1.0 if k < 3 else 1.0 + 0.9 * eout(ap(p, 0.0, 0.5))
    pov_beach(c, t, light=light, people=ppl, fire=fire, zoom=zoom)
    if k == 0 and light > 0:
        fl = max(0, 1 - (p - 0.35) * 4); c.set_source_rgba(1, 0.97, 0.85, 0.25 * fl); c.paint()
    if k == 1: tag(c, "?", 562, 960, WH, ap(p, 0.3, 0.5), 80)
    if k == 2: stamp(c, "UN FEU DE CAMP", 540, 640, 110, ORG, since, glow=0.9)
    if k == 3:
        c.new_path(); c.arc(540 + (562 - 540) * zoom, 900 + (1035 - 900) * zoom, 140 + 6 * math.sin(t * 8), 0, 7); c.set_source_rgb(*RED); c.set_line_width(9); c.stroke()
        stamp(c, "DES GENS !", 540, 600, 160, RED, since, glow=1.0)


def mini_beach(c, x0, y0, w, h, lt):
    c.save(); rr(c, x0, y0, w, h, 50); c.clip()
    c.set_source_rgb(0.03, 0.05, 0.12); c.paint()
    c.new_path(); c.rectangle(x0, y0 + h * 0.62, w, h); c.set_source_rgb(0.42, 0.38, 0.3); c.fill()
    c.new_path(); c.rectangle(x0, y0 + h * 0.62, w * 0.28, h); c.set_source_rgb(0.1, 0.2, 0.35); c.fill()        # eau peu profonde (à gauche)
    for j in range(3): c.new_path(); c.arc(x0 + w * (0.84 + 0.06 * j), y0 + h * 0.64, 20 - 4 * j, math.pi, 2 * math.pi); c.set_source_rgb(0.12, 0.12, 0.14); c.fill()   # rochers
    R.flames(c, x0 + w * 0.5, y0 + h * 0.64, 0.25, lt, 1.0)
    for dx in (-40, -22, 26, 44):
        xx = x0 + w * 0.5 + dx; yy = y0 + h * 0.6
        c.move_to(xx, yy); c.line_to(xx, yy - 26); c.set_source_rgb(0.9, 0.9, 0.95); c.set_line_width(4); c.stroke(); c.new_path(); c.arc(xx, yy - 32, 6, 0, 7); c.fill()


def sc_e3_think(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    sky(c, (0.04, 0.05, 0.10), (0.01, 0.01, 0.03))
    if k == 0:
        n = max(1, 5 - int(since * 2.2)); q = (since * 2.2) % 1
        c.save(); c.translate(540, 820); s_ = 1.4 - 0.4 * eout(q / 0.3); c.scale(s_, s_); text(c, str(n), 0, 110, 320, RED, glow=1.0); c.restore()
        label(c, "SECONDES", 540, 1000, 56, WH, 1, 'Bebas Neue')
    else:
        for side, (cx, col, lab) in enumerate(((300, BLUE, "A : L'EAU"), (780, ORG, "B : AU-DESSUS"))):
            a = ap(t, sg['sent'][1 + 2 * side][0] - 0.1, sg['sent'][1 + 2 * side][0] + 0.2)
            if a <= 0: continue
            act = (k in (1, 2)) == (side == 0); dim = 1.0 if act else 0.45
            x0, y0, w, h = cx - 220, 470, 440, 430
            c.push_group()
            mini_beach(c, x0, y0, w, h, t)
            pl = 0.0
            if side == 0:
                q = ap(t, sg['sent'][2][0], sg['sent'][2][0] + 1.6) if k >= 2 else 0
                px = x0 + w * (0.05 + 0.13 * ap(t, sg['sent'][1][0], sg['sent'][1][0] + 1.5)); py = y0 + h * (0.45 + 0.15 * ap(t, sg['sent'][1][0], sg['sent'][1][0] + 1.5))
                twin(c, px + 30 * q, py + 10 * q, -2.6 * q, 0, 0.3, prop=0, gear=1, flaps=1)
                if q > 0.1:
                    for j in range(8): c.new_path(); c.arc(px + 30 + (j - 4) * 14, py + 30 - 20 * math.sin(j), 10, 0, 7); c.set_source_rgba(0.8, 0.9, 1, 0.7 * (1 - q * 0.6)); c.fill()
            else:
                q = ap(t, sg['sent'][3][0], sg['sent'][3][0] + 1.8)
                px = x0 + w * (0.15 + 0.6 * q); py = y0 + h * (0.42 - 0.15 * math.sin(math.pi * q) + 0.15 * q)
                twin(c, px, py, 0.05, 0, 0.3, prop=0, gear=1, flaps=1)
                if k == 4:
                    c.move_to(x0 + w * 0.72, y0 + h * 0.75); c.line_to(x0 + w * 0.84, y0 + h * 0.75); c.set_source_rgb(*RED); c.set_line_width(8); c.stroke()
            c.restore()
            rr(c, x0, y0, w, h, 50); c.set_source_rgba(*col, 1); c.set_line_width(7); c.stroke()
            text(c, lab, cx, y0 + 80, 64, col, glow=0.5)
            c.pop_group_to_source(); c.paint_with_alpha(a * dim)
        if k == 2: tag(c, "CAPOTAGE", 300, 980, RED, ap(p, 0.2, 0.35), 56)
        if k == 4: tag(c, "TRÈS COURT", 780, 980, RED, ap(p, 0.2, 0.35), 56)
    by = 4 * math.sin(t * 2); left = k in (1, 2)
    pilot_body(c, W / 2, 1270 + by, 1.0)
    R.eyes_head(c, W / 2, 1180 + by, 115, 'worried', (-26 if left else 26, -18) if k else (0, -10), t, rim=BLUE if left else ORG)


def sc_e3_choice(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    c.set_source_rgb(0.02, 0.02, 0.04); c.paint()
    N = R.CFG.NEXT; nxt = int(R.CFG.EP) + 1
    text(c, "TU FAIS QUOI ?", W / 2, 350, 140, WH, glow=0.5)
    for side, (col, lab) in enumerate(((BLUE, "A"), (ORG, "B"))):
        sub, l1, l2 = N[lab]
        ts = sg['sent'][1 + side][0]
        a = ap(t, ts - 0.1, ts + 0.25); y0 = 440 + side * 430; dx = (1 - a) * (300 if side == 0 else -300)
        if a <= 0: continue
        act = (k == 1 + side)
        c.save(); c.translate(dx, 0)
        rr(c, 100, y0, 880, 390, 40); c.set_source_rgba(*col, (0.16 if act else 0.07) * a); c.fill_preserve(); c.set_source_rgba(*col, (1.0 if act else 0.7) * a); c.set_line_width(7 if act else 5); c.stroke()
        c.save(); rr(c, 100, y0, 880, 390, 40); c.clip(); radial(c, 260, y0 + 195, 420, col, 0.22 * a); c.restore()
        text(c, lab, 240, y0 + 280, 300, col, glow=a)
        text(c, sub, 640, y0 + 175, 100, WH)
        text(c, l1, 640, y0 + 245, 38, (0.75, 0.8, 0.9), 'Montserrat'); text(c, l2, 640, y0 + 305, 40, col, 'Montserrat')
        c.restore()
    lx = -22 if (t % 2.4) < 1.2 else 22
    R.eyes_head(c, W / 2, 1310, 58, 'worried', (lx * 0.5, -8), t)
    if k >= 3:
        text(c, "ÉCRIS A OU B EN COMMENTAIRE", W / 2, 1790, 46, (0.9, 0.92, 1.0), 'Montserrat')
    if k >= 4:
        text(c, f"LA MAJORITÉ DÉCIDE DE L'ÉPISODE {nxt}", W / 2, 1855, 36, ORG, 'Montserrat')


SC7 = {k[3:]: v for k, v in globals().items() if k.startswith('sc_') and callable(v)}
