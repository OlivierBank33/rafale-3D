"""Scènes v2 « une illustration par phrase » (sg['sent'] = horodatage réel des phrases) pour le 25/10 :
train d'atterrissage, F-15 à une aile, planeur de Gimli. Remplacent les versions de sm_scenes5 (mêmes noms de type)."""
import cairo, math, random
from sm_lib import *
from sm_scenes2 import ease, ap, blinkh, civ_body, sky, jet, ORG, BLUE, RED, WH, GRN
from sm_scenes5 import wheelwell, stow, f15, desert, b767
from sm_scenes4 import fighter
R = None
YEL = (1.0, 0.85, 0.25)


def eout(u): u = min(max(u, 0), 1); return 1 - (1 - u) ** 3
def back(u, s=1.7):
    u = min(max(u, 0), 1) - 1; return 1 + u * u * ((s + 1) * u + s)


def si(sg, t):
    """(indice de phrase, progression 0..1 dans la phrase, secondes depuis le début de la phrase)."""
    S = sg.get('sent') or [(sg['vt'], sg['vt'] + sg['dur'])]
    k = max([i for i, (a, b) in enumerate(S) if t >= a - 0.12] or [0])
    a = S[k][0]; b = S[k + 1][0] if k + 1 < len(S) else sg['end']
    return k, min(1.0, max(0.0, (t - a) / max(0.3, b - a))), t - a


def stamp(c, s, x, y, size, col, since, rot=-0.05, glow=0.8):
    """Texte qui « tamponne » (overshoot) à l'apparition."""
    if not s or since <= 0: return
    k = back(since / 0.22, 2.4); sc = 1.6 - 0.6 * k
    c.save(); c.translate(x, y - size * 0.35); c.rotate(rot); c.scale(sc, sc)
    c.push_group(); text(c, s, 0, size * 0.35, size, col, glow=glow); c.pop_group_to_source(); c.paint_with_alpha(min(1, since / 0.06))
    c.restore()


def speedlines(c, t, a, horiz=True, n=30, seed=4, col=(1, 1, 1)):
    r = random.Random(seed)
    for _ in range(n):
        ph = (t * (2.5 + r.random() * 2) + r.random()) % 1
        if horiz:
            y = r.random() * H; x = W * (1.2 - 1.6 * ph); L = 120 + 300 * r.random()
            c.move_to(x, y); c.line_to(x + L, y)
        else:
            x = r.random() * W; y = H * (1.2 - 1.6 * ph); L = 120 + 300 * r.random()
            c.move_to(x, y); c.line_to(x, y + L)
        c.set_source_rgba(*col, a * (0.15 + 0.25 * r.random())); c.set_line_width(2 + 4 * r.random()); c.stroke()


def clouds(c, t, y0, y1, n=10, seed=2, speed=60, a=0.85, s=1.0, col=(1, 1, 1)):
    r = random.Random(seed)
    for _ in range(n):
        x = (r.random() * (W + 600) - t * speed * (0.6 + 0.8 * r.random())) % (W + 600) - 300; y = y0 + r.random() * (y1 - y0)
        k = s * (0.6 + 0.8 * r.random())
        for dx, dy, rad in ((0, 0, 70), (60, 12, 55), (-62, 15, 50), (25, -28, 48)):
            c.new_path(); c.arc(x + dx * k, y + dy * k, rad * k, 0, 7); c.set_source_rgba(*col, a); c.fill()


def city_lights(c, y0, y1, seed=3, n=420, a=1.0):
    r = random.Random(seed)
    for _ in range(n):
        y = y0 + (y1 - y0) * r.random() ** 0.7; x = r.random() * W; rad = 1 + 2.5 * (y - y0) / max(1, y1 - y0) * r.random()
        c.new_path(); c.arc(x, y, rad, 0, 7); c.set_source_rgba(1, 0.75 + 0.2 * r.random(), 0.4, a * (0.4 + 0.6 * r.random())); c.fill()


def big_wheel(c, x, y, r, rot):
    c.new_path(); c.arc(x, y, r, 0, 7); fill_stroke(c, (0.08, 0.08, 0.09), 12)
    for k in range(6):                                    # sculptures du pneu
        a = rot + k * math.pi / 3
        c.move_to(x + math.cos(a) * r * 0.78, y + math.sin(a) * r * 0.78); c.line_to(x + math.cos(a) * r * 0.97, y + math.sin(a) * r * 0.97)
    c.set_source_rgb(0.25, 0.25, 0.28); c.set_line_width(10); c.stroke()
    c.new_path(); c.arc(x, y, r * 0.5, 0, 7); fill_stroke(c, (0.62, 0.64, 0.7), 8)
    for k in range(5):
        a = rot + k * 2 * math.pi / 5; c.new_path(); c.arc(x + math.cos(a) * r * 0.28, y + math.sin(a) * r * 0.28, r * 0.05, 0, 7); c.set_source_rgb(*INK); c.fill()


def sneak(c, x, y, s, t, look=0, climb=0.0, mood='worried'):
    """Clandestin accroupi / qui grimpe."""
    bob = 4 * math.sin(t * 9)
    legs = (x - 30 * s, y + 160 * s), (x + 30 * s, y + 160 * s)
    if climb > 0:
        limb(c, [(x - 30 * s, y + 90 * s), (x - 60 * s, y + 20 * s - 40 * math.sin(t * 6) * s)], w=22 * s)
        limb(c, [(x + 30 * s, y + 90 * s), (x + 50 * s, y - 10 * s + 40 * math.sin(t * 6) * s)], w=22 * s)
    limb(c, [(x - 25 * s, y + 140 * s), (x - 45 * s, y + 190 * s + bob)], w=22 * s); limb(c, [(x + 25 * s, y + 140 * s), (x + 50 * s, y + 190 * s - bob)], w=22 * s)
    rr(c, x - 62 * s, y + 50 * s, 124 * s, 110 * s, 45 * s); fill_stroke(c, (0.25, 0.45, 0.75), 9)
    blinkh(c, x, y, 82 * s, mood, (look * 22 * s, 0), t, False)


# ======================= SURVIVRAIS-TU ? : train d'atterrissage =======================
def tarmac_dusk(c):
    sky(c, (0.16, 0.12, 0.30), (0.95, 0.52, 0.30))
    radial(c, 820, 1080, 500, (1, 0.6, 0.3), 0.35)
    c.new_path(); c.rectangle(0, 1180, W, H - 1180); g = cairo.LinearGradient(0, 1180, 0, H); g.add_color_stop_rgb(0, 0.18, 0.16, 0.2); g.add_color_stop_rgb(1, 0.05, 0.05, 0.07); c.set_source(g); c.fill()


def sc_tw_hide(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:                                             # sous l'avion, contre-plongée
        tarmac_dusk(c)
        for i in range(9):
            x = (i * 160 + 40) % W; c.new_path(); c.arc(x, 1260, 7, 0, 7); c.set_source_rgb(1, 0.85, 0.4); c.fill(); radial(c, x, 1260, 40, (1, 0.8, 0.3), 0.4)
        c.new_path(); c.move_to(-50, 0); c.line_to(W + 50, 0); c.line_to(W + 50, 420); c.curve_to(700, 520, 300, 520, -50, 440); c.close_path()
        g = cairo.LinearGradient(0, 0, 0, 520); g.add_color_stop_rgb(0, 0.55, 0.57, 0.63); g.add_color_stop_rgb(1, 0.32, 0.33, 0.38); c.set_source(g); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(10); c.stroke()
        rr(c, 560, 360, 300, 150, 20); c.set_source_rgb(0.02, 0.02, 0.03); c.fill()            # case du train (trou noir)
        c.move_to(710, 470); c.line_to(710, 1120); c.set_source_rgb(*INK); c.set_line_width(46); c.stroke()
        c.move_to(710, 470); c.line_to(710, 1120); c.set_source_rgb(0.6, 0.62, 0.68); c.set_line_width(30); c.stroke()
        big_wheel(c, 590, 1220, 170, 0); big_wheel(c, 840, 1220, 170, 0.5)
        cl = ap(p, 0.45, 0.95)
        x = 300 + 260 * ap(p, 0.0, 0.45) + 60 * cl; y = 980 - 520 * cl
        sneak(c, x, y, 1.0, t, look=-1 if (t % 1.6) < 0.8 else 1, climb=cl)
        if p < 0.45: text(c, "?", x + 90, y - 80, 90, YEL, glow=0.5)
    elif k == 1:                                           # roulage + rotation
        tarmac_dusk(c)
        for i in range(14):
            x = (i * 120 - t * 900) % (W + 200) - 100; c.new_path(); c.rectangle(x, 1300, 70, 10); c.set_source_rgb(0.9, 0.9, 0.8); c.fill()
        rot = -0.16 * ap(p, 0.4, 1.0)
        jet(c, 540, 1140 - 260 * ap(p, 0.55, 1.0), rot, 1.7, gear=1.0)
        speedlines(c, t, 0.9)
        stamp(c, "DÉCOLLAGE", 540, 520, 130, WH, since)
    elif k == 2:                                           # « depuis des décennies » : compteur 1947 -> 2020
        c.set_source_rgb(0.05, 0.05, 0.08); c.paint(); radial(c, 540, 900, 700, (0.3, 0.4, 0.7), 0.25)
        yr = int(1947 + (2020 - 1947) * ap(p, 0.05, 0.8)); n = int(128 * ap(p, 0.05, 0.8))
        text(c, str(yr), 540, 760, 220, WH, glow=0.4)
        rr(c, 140, 860, 800, 22, 10); c.set_source_rgba(1, 1, 1, 0.15); c.fill()
        rr(c, 140, 860, 800 * ap(p, 0.05, 0.8) + 1, 22, 10); c.set_source_rgb(*ORG); c.fill()
        text(c, f"{n} CAS RECENSÉS", 540, 1060, 96, ORG, glow=0.7)
        text(c, "SOURCE : FAA", 540, 1140, 36, (0.7, 0.75, 0.85), 'Montserrat')
    else:                                                  # l'avion s'éloigne, question
        sky(c, (0.06, 0.06, 0.18), (0.5, 0.3, 0.45)); clouds(c, t, 1000, 1500, 7, 3, 40, 0.25)
        x = 540 + 200 * p; y = 900 - 250 * p
        jet(c, x, y, -0.18, 0.75, gear=1 - ap(p, 0.2, 0.6))
        c.new_path(); c.arc(x - 2, y + 40, 60 + 8 * math.sin(t * 6), 0, 7); c.set_source_rgba(*RED, 0.9); c.set_line_width(6); c.stroke()
        stamp(c, "SURVIVRAIS-TU ?", 540, 470, 140, RED, since)


def sc_tw_gear(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    f = ap(p, 0.3, 0.95) if k == 0 else 1.0
    if k < 2:
        wheelwell(c, lt, fold=f if k == 0 else 1.0)
        stow(c, 330, 850 + (40 * math.sin(t * 20) * (1 - f) if k == 0 else 0), lt, 'worried')
        if k == 0:
            for j in range(3):                               # flèches de rentrée du train
                yy = 1500 - ((t * 500 + j * 160) % 480); c.move_to(700, yy); c.line_to(660, yy + 50); c.move_to(700, yy); c.line_to(740, yy + 50)
            c.set_source_rgba(1, 1, 1, 0.6); c.set_line_width(8); c.stroke()
            stamp(c, "LE TRAIN REMONTE", 540, 420, 110, WH, since)
        else:
            q = 0.5 + 0.5 * math.sin(t * 10); radial(c, 470, 1120, 380, RED, 0.18 + 0.15 * q)
            c.new_path(); c.arc(700, 1250, 300, 0, 7); c.set_source_rgba(*RED, 0.5 + 0.4 * q); c.set_dash([30, 18]); c.set_line_width(8); c.stroke(); c.set_dash([])
            stamp(c, "ZONE DANGER", 540, 420, 120, RED, since)
    else:
        wheelwell(c, lt, fold=1.0)
        c.save(); c.translate(330, 980); c.scale(1.0, 0.75); c.translate(-330, -980); stow(c, 330, 880, lt, 'worried'); c.restore()
        fl = max(0, 1 - since / 0.25); c.set_source_rgba(1, 0.2, 0.2, 0.5 * fl + 0.12); c.paint()
        r = random.Random(5)
        for _ in range(9):                                  # fissures
            a = r.random() * 6.28; c.move_to(540, 900)
            for s in range(4): c.line_to(540 + math.cos(a + r.uniform(-0.3, 0.3)) * 90 * (s + 1), 900 + math.sin(a + r.uniform(-0.3, 0.3)) * 90 * (s + 1))
        c.set_source_rgba(1, 1, 1, 0.5); c.set_line_width(4); c.stroke()
        stamp(c, "ÉCRASÉ", 540, 470, 180, RED, since, glow=1.0)


def frost(c, a, t):
    if a <= 0: return
    r = random.Random(11)
    for _ in range(160):
        side = r.randint(0, 3); d = r.random() ** 2 * 260 * a
        x = (r.random() * W, d, W - d, r.random() * W)[side] if side in (0, 3) else (d if side == 1 else W - d)
        y = (d, r.random() * H, r.random() * H, H - d)[side]
        c.new_path(); c.arc(x, y, 4 + 18 * r.random() * a, 0, 7); c.set_source_rgba(0.85, 0.93, 1, 0.35 * a); c.fill()
    g = cairo.RadialGradient(W / 2, H / 2, W * 0.45, W / 2, H / 2, W * 0.95); g.add_color_stop_rgba(0, 0.7, 0.85, 1, 0); g.add_color_stop_rgba(1, 0.75, 0.88, 1, 0.55 * a); c.set_source(g); c.paint()


def sc_tw_cold(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:                                             # l'avion monte à travers les nuages
        sky(c, (0.12, 0.25, 0.55), (0.55, 0.7, 0.9)); clouds(c, t, 200, 1700, 12, 8, 0, 0.75)
        c.save(); c.translate(0, (t * 420) % 200 - 100); clouds(c, t, -200, H + 200, 8, 9, 0, 0.35); c.restore()
        jet(c, 540, 900, -0.32, 1.2)
        alt = int(11000 * ap(p, 0.0, 1.0)); stamp(c, f"{alt:,} M".replace(',', ' '), 540, 470, 140, WH, since, rot=0)
    elif k == 1:
        wheelwell(c, lt, fold=1, cold=0.3)
        stow(c, 330, 850, lt, 'worried', 0.3)
        for j, (s_, y) in enumerate((("NON CHAUFFÉE", 420), ("NON PRESSURISÉE", 560))):
            sj = since - j * 0.9
            if sj > 0: stamp(c, s_, 560, y, 96, RED, sj, rot=-0.06 + 0.04 * j)
    else:
        cold = 0.4 + 0.6 * ap(p, 0.0, 0.8)
        wheelwell(c, lt, fold=1, cold=cold)
        stow(c, 330, 850, lt, 'worried', cold)
        for j in range(3):                                   # buée
            ph = (t * 0.8 + j / 3) % 1; c.new_path(); c.arc(400 + 60 * ph, 830 - 40 * ph, 14 + 30 * ph, 0, 7); c.set_source_rgba(1, 1, 1, 0.5 * (1 - ph)); c.fill()
        frost(c, cold, t)
        temp = int(15 - 65 * ap(p, 0.0, 0.8))
        rr(c, 230, 360, 620, 200, 30); c.set_source_rgba(0, 0, 0, 0.6); c.fill()
        text(c, f"{temp} °C".replace('-', '−'), 540, 510, 150, BLUE if temp < 0 else ORG, glow=0.8)


def sc_tw_oxy(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    wheelwell(c, lt, fold=1, cold=1)
    sleep = 0 if k == 0 else (ap(p, 0.0, 0.6) if k == 1 else 1)
    c.save(); c.translate(330, 950); c.rotate(0.5 * sleep); c.translate(-330, -950); stow(c, 330, 850, lt, 'neutral' if sleep > 0.5 else 'worried', 1); c.restore()
    if sleep > 0.5:
        for sx in (-1, 1):
            x0 = 330 + sx * 31; c.move_to(x0 - 14, 850); c.line_to(x0 + 14, 850); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    frost(c, 0.6 + 0.4 * (k == 2) * p, t)
    if k == 0:
        lvl = 1 - 0.75 * ap(p, 0.0, 0.9)
        text(c, "OXYGÈNE", 540, 420, 90, WH)
        rr(c, 190, 470, 700, 70, 30); c.set_source_rgba(1, 1, 1, 0.12); c.fill()
        rr(c, 200, 480, 680 * lvl, 50, 24); c.set_source_rgb(*(RED if lvl < 0.45 else ORG)); c.fill()
    g = cairo.RadialGradient(W / 2, H * 0.45, W * (0.7 - 0.5 * sleep), W / 2, H * 0.45, W * 1.0); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.9 * sleep); c.set_source(g); c.paint()
    if k == 1: stamp(c, "INCONSCIENT", 540, 460, 120, RED, since)
    if k == 2:                                             # horloge qui s'emballe
        x, y, r = 540, 470, 120
        c.new_path(); c.arc(x, y, r, 0, 7); fill_stroke(c, (0.95, 0.95, 0.97), 8)
        for a, L, w in ((t * 6, 0.8, 6), (t * 0.5, 0.55, 10)):
            c.move_to(x, y); c.line_to(x + math.cos(a) * r * L, y + math.sin(a) * r * L); c.set_source_rgb(*INK); c.set_line_width(w); c.set_line_cap(1); c.stroke()
        text(c, "DES HEURES", 540, 680, 80, BLUE, glow=0.6)


def sc_tw_fall(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:                                             # approche au-dessus de la ville, le train sort
        sky(c, (0.05, 0.05, 0.15), (0.35, 0.25, 0.4)); city_lights(c, 1150, H)
        jet(c, 540 - 120 * p, 700 + 160 * p, 0.06, 1.25, gear=ap(p, 0.3, 0.8), night=True)
        stamp(c, "APPROCHE", 540, 420, 120, WH, since)
    elif k == 1:                                           # vue depuis la case : les trappes s'ouvrent
        c.set_source_rgb(0.03, 0.03, 0.05); c.paint()
        o = ap(p, 0.05, 0.6)
        c.save(); rr(c, 140, 700, 800, 900, 30); c.clip()
        g = cairo.LinearGradient(0, 700, 0, 1600); g.add_color_stop_rgb(0, 0.08, 0.08, 0.16); g.add_color_stop_rgb(1, 0.02, 0.02, 0.05); c.set_source(g); c.paint()
        city_lights(c, 900, 1600, 9, 300)
        for side in (-1, 1):                                # deux trappes qui pivotent
            w = 400 * (1 - o); x0 = 540 + side * 400 - (w if side > 0 else 0) * 1
            c.new_path(); c.rectangle(540 - 400 if side < 0 else 540 + 400 - w, 700, w, 900); c.set_source_rgb(0.45, 0.47, 0.53); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
        c.restore()
        rr(c, 140, 700, 800, 900, 30); c.set_source_rgb(*INK); c.set_line_width(14); c.stroke()
        sneak(c, 540, 470, 0.9, t, look=0, mood='worried')
        if o > 0.3: radial(c, 540, 1150, 500, (0.4, 0.5, 1), 0.15)
    else:                                                  # la chute
        sky(c, (0.05, 0.05, 0.15), (0.35, 0.25, 0.4)); city_lights(c, 1250, H)
        jet(c, 760, 330, 0.06, 0.8, gear=1, night=True)
        y = 420 + 820 * ap(p, 0.0, 1.0) ** 1.6
        c.move_to(720, 380); c.line_to(700, y); c.set_source_rgba(1, 1, 1, 0.5); c.set_dash([16, 16]); c.set_line_width(4); c.stroke(); c.set_dash([])
        c.save(); c.translate(700, y); c.rotate(t * 3); c.new_path(); c.arc(0, 0, 22, 0, 7); fill_stroke(c, (0.98, 0.98, 0.99), 5)
        limb(c, [(0, 20), (-25, 55)], w=10); limb(c, [(0, 20), (28, 50)], w=10); c.restore()
        stamp(c, "CHUTE", 380, 760, 170, RED, since)


def sc_tw_verdict(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    sky(c, (0.08, 0.02, 0.03), (0.02, 0.01, 0.01)); radial(c, 540, 1000, 600, RED, 0.12)
    if k == 0:
        stamp(c, "TU NE SURVIS PAS", 540, 560, 130, RED, since, glow=1.0)
        stow(c, 540, 950, t, 'worried', 1.0, 1.4)
    elif k == 1:
        n = int(128 * ap(p, 0.0, 0.25)); text(c, f"{n} CAS", 540, 520, 150, WH, glow=0.4)
        dead = int(97 * ap(p, 0.3, 0.9))                  # « plus de 3 sur 4 » ≈ > 75 % (illustratif sur 128)
        for i in range(128):
            x = 150 + (i % 16) * 49; y = 680 + (i // 16) * 60
            c.new_path(); c.arc(x, y, 18, 0, 7); c.set_source_rgb(*((0.75, 0.15, 0.18) if i < dead else (0.92, 0.92, 0.95))); c.fill()
        if p > 0.6: text(c, "PLUS DE 3 SUR 4", 540, 1250, 100, RED, glow=0.8)
    elif k == 2:
        stamp(c, "NE LE TENTE", 540, 760, 170, WH, since, rot=-0.04); stamp(c, "JAMAIS", 540, 960, 220, RED, since - 0.25, rot=0.03, glow=1.0)
    else:
        stow(c, 540, 900, t, 'worried', 0.5, 1.5)
        stamp(c, "TU LE SAVAIS ?", 540, 520, 140, ORG, since)


# ======================= HISTOIRE VRAIE : F-15 à une aile =======================
def desert2(c, t, scroll=0.0):
    sky(c, (0.30, 0.55, 0.88), (0.98, 0.86, 0.62))
    radial(c, 820, 360, 300, (1, 0.95, 0.75), 0.6)
    for k, (y, col, sp) in enumerate(((1250, (0.86, 0.68, 0.45), 0.2), (1380, (0.80, 0.60, 0.38), 0.5), (1540, (0.72, 0.52, 0.32), 1.0))):
        c.new_path(); c.move_to(0, H)
        for x in range(0, W + 41, 40):
            c.line_to(x, y + 40 * math.sin((x + scroll * sp * 300) / (180 + 60 * k) + k))
        c.line_to(W, H); c.close_path(); c.set_source_rgb(*col); c.fill()


def sc_f_hook(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    desert2(c, t, t)
    if k == 0:
        f15(c, 540, 820, 1.2, 0.04 * math.sin(t), wing=True)
        c.save(); c.translate(540, 820); c.scale(1.2, 1.2)
        q = 0.5 + 0.5 * math.sin(t * 8); c.new_path(); c.move_to(50, -40); c.line_to(300, 120); c.line_to(300, 170); c.line_to(50, 140); c.close_path()
        c.set_source_rgba(*RED, 0.35 + 0.3 * q); c.fill(); c.restore()
        text(c, "?", 860, 900, 200, RED, glow=1.0)
    elif k == 1:
        f15(c, 540, 860, 1.0, 0.0, wing=True); speedlines(c, t, 0.7, horiz=False)
        stamp(c, "1983", 540, 520, 220, WH, since)
    else:
        f15(c, 540, 820, 1.2, 0.06 * math.sin(t * 2), wing=False, leak=1.0, lt=t)
        stamp(c, "1 SEULE AILE", 540, 1260, 130, RED, since, glow=1.0)


def sc_f_train(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    desert2(c, t, t * 0.5)
    if k == 0:
        f15(c, 540, 900, 0.5, -0.3)
        c.new_path(); c.arc(300, 1350, 26, 0, 7); fill_stroke(c, RED, 6)
        c.move_to(300, 1376); c.line_to(300, 1430); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
        stamp(c, "DÉSERT DU NÉGUEV", 540, 500, 110, WH, since)
        text(c, "1ER MAI 1983", 540, 600, 60, (0.15, 0.15, 0.2))
    else:
        a = t * 0.9
        for j in range(3):
            c.new_path(); c.arc(540, 820, 260 + 40 * j, a + j, a + j + 2.2); c.set_source_rgba(1, 1, 1, 0.55); c.set_line_width(5); c.stroke()
        f15(c, 540 + 260 * math.cos(a), 820 + 260 * math.sin(a), 0.42, a + math.pi)
        fighter(c, 540 + 300 * math.cos(a + 2.4), 820 + 300 * math.sin(a + 2.4), 0.35, a + 2.4 + math.pi / 2)
        fighter(c, 540 + 340 * math.cos(a + 4.1), 820 + 340 * math.sin(a + 4.1), 0.35, a + 4.1 + math.pi / 2)
        stamp(c, "F-15  VS  A-4", 540, 480, 120, WH, since)


def sc_f_crash(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    desert2(c, t, t)
    if k == 0:
        f15(c, 540, 820, 1.1, 0, wing=True)
        fl = max(0, 1 - since / 0.35); c.set_source_rgba(1, 1, 1, 0.9 * fl); c.paint()
        c.new_path()
        for j in range(16):
            a = j * math.pi / 8; r = 260 if j % 2 == 0 else 110; c.line_to(760 + math.cos(a) * r * eout(since / 0.3), 760 + math.sin(a) * r * eout(since / 0.3))
        c.close_path(); c.set_source_rgba(1, 0.75, 0.2, 0.9); c.fill()
        stamp(c, "COLLISION", 540, 1260, 150, RED, since, glow=1.0)
    elif k == 1:                                            # arrêt sur image explicatif
        f15(c, 540, 820, 1.1, 0, wing=True)
        fighter(c, 900, 660, 0.45, 3.6)
        c.new_path(); c.arc(760, 860, 170, 0, 7); c.set_source_rgba(*RED, 0.9); c.set_line_width(8); c.stroke()
        c.move_to(900, 660); c.line_to(800, 780); c.set_source_rgb(*RED); c.set_line_width(8); c.stroke()
        stamp(c, "AILE DROITE", 540, 1260, 120, RED, since)
    elif k == 2:                                            # le Skyhawk se disloque, parachute
        f15(c, 540, 820, 1.1, 0, wing=False, leak=0.8, lt=t)
        r = random.Random(3)
        for j in range(14):
            a = r.random() * 6.28; d = 120 + 500 * eout(since / 1.5) * (0.5 + r.random())
            c.save(); c.translate(820 + math.cos(a) * d, 640 + math.sin(a) * d); c.rotate(t * 4 + j); rr(c, -18, -10, 36, 20, 3); c.set_source_rgb(0.4, 0.42, 0.45); c.fill(); c.restore()
        py = 420 + 80 * ap(p, 0.2, 1)
        c.new_path(); c.arc(880, py, 70, math.pi, 2 * math.pi); c.close_path(); fill_stroke(c, ORG, 5)
        c.move_to(810, py); c.line_to(880, py + 90); c.move_to(950, py); c.line_to(880, py + 90); c.set_source_rgb(*INK); c.set_line_width(3); c.stroke()
        c.new_path(); c.arc(880, py + 100, 14, 0, 7); fill_stroke(c, (0.98, 0.98, 0.99), 4)
        text(c, "PILOTE DU A-4 ÉJECTÉ", 540, 1260, 80, WH, glow=0.4)
    else:                                                   # vrille dans un nuage de carburant
        c.save(); c.translate(540, 820); c.rotate(t * 3.2); c.translate(-540, -820)
        f15(c, 540, 820, 1.0, 0, wing=False, leak=1.0, lt=t); c.restore()
        for j in range(18):
            ph = (t * 0.6 + j / 18) % 1; a = j * 2.1 + t; d = 160 + 300 * ph
            c.new_path(); c.arc(540 + math.cos(a) * d, 820 + math.sin(a) * d, 30 + 50 * ph, 0, 7); c.set_source_rgba(0.9, 0.93, 1, 0.35 * (1 - ph)); c.fill()
        stamp(c, "VRILLE", 540, 1260, 160, RED, since, glow=1.0)


def pilot_head_card(c, x, y, r, t, name, since, look=(0, 0), mood='determined'):
    c.new_path(); c.arc(x, y, r * 1.35, 0, 7); c.set_source_rgba(0, 0, 0, 0.5); c.fill()
    R.eyes_head(c, x, y, r, mood, look, t, rim=ORG)
    stamp(c, name, x, y + r * 1.8, 90, ORG, since)


def sc_f_recover(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    desert2(c, t, t * 2)
    if k == 0:
        f15(c, 540, 1180, 0.75, 0.15 * math.sin(t * 3), wing=False, leak=1.0, lt=t)
        pilot_head_card(c, 540, 520, 130, t, "ZIV NEDIVI", since)
    elif k == 1:
        f15(c, 540, 820, 1.1, 0.25 * (1 - ap(p, 0, 0.6)) * math.sin(t * 3), wing=False, leak=1.0, lt=t)
        for sx in (-1, 1): radial(c, 540 + sx * 50, 1140, 120, (1, 0.6, 0.2), 0.9); radial(c, 540 + sx * 50, 1200, 70, (1, 0.9, 0.6), 0.9)
        speedlines(c, t, 0.8, horiz=False)
        stamp(c, "POST-COMBUSTION", 540, 1300, 100, ORG, since)
    else:
        f15(c, 540, 820, 1.2, 0.03 * math.sin(t), wing=False, leak=1.0, lt=t)
        for j in range(26):                                   # le brouillard de carburant cache l'aile
            ph = (t * 0.5 + j / 26) % 1; c.new_path(); c.arc(640 + 260 * ((j * 37) % 100) / 100, 720 + 420 * ph, 40 + 40 * ph, 0, 7); c.set_source_rgba(0.92, 0.95, 1, 0.45 * (1 - ph)); c.fill()
        text(c, "?", 820, 820, 180, WH, glow=0.8)
        stamp(c, "IL NE VOIT RIEN", 540, 1300, 110, WH, since)


def sc_f_land(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    sky(c, (0.35, 0.6, 0.9), (0.95, 0.85, 0.65))
    c.new_path(); c.rectangle(0, 900, W, H); c.set_source_rgb(0.82, 0.68, 0.45); c.fill()
    c.new_path(); c.move_to(420, 900); c.line_to(660, 900); c.line_to(1000, H); c.line_to(80, H); c.close_path(); fill_stroke(c, (0.3, 0.3, 0.33), 6)
    for j in range(10):
        y = 920 + ((j * 110 + t * 700 * (1 if k == 0 else 0.3 * (1 - p))) % 1000); w = 6 + 30 * (y - 900) / 1000
        c.new_path(); c.rectangle(540 - w / 2, y, w, 20 + 40 * (y - 900) / 1000); c.set_source_rgb(0.95, 0.95, 0.9); c.fill()
    if k == 0:
        kk = ap(p, 0.0, 0.8)
        f15(c, 540, 400 + 800 * kk, 0.4 + 0.55 * kk, 0, wing=False, leak=0.4, lt=t)
        kmh = int(480 * ap(p, 0.0, 0.5)); stamp(c, f"{kmh} KM/H", 540, 520, 150, RED, since)
        text(c, "≈ 2× LA NORMALE", 540, 640, 64, WH)
    elif k == 1:
        c.move_to(250, 1200); c.line_to(540, 1260 + 60 * (1 - ap(p, 0.4, 0.5))); c.line_to(830, 1200)
        c.set_source_rgb(*INK); c.set_line_width(10); c.stroke()
        f15(c, 540, 1100, 0.95, 0, wing=False)
        if p > 0.45:
            r = random.Random(int(t * 30))
            for _ in range(30):
                a = r.uniform(3.6, 5.8); d = r.random() * 200
                c.move_to(540, 1420); c.line_to(540 + math.cos(a) * d, 1420 + math.sin(a) * d); c.set_source_rgba(1, 0.8, 0.3, 0.9); c.set_line_width(3); c.stroke()
            stamp(c, "CROSSE ARRACHÉE", 540, 520, 110, RED, since - 0.45 * (sg['sent'][2][0] - sg['sent'][1][0]))
        else: stamp(c, "LE CÂBLE", 540, 520, 120, WH, since)
    else:
        for j in range(9):                                   # filet / barrière
            c.move_to(260 + j * 70, 950); c.line_to(260 + j * 70, 1080)
        c.move_to(260, 960); c.line_to(820, 960); c.move_to(260, 1020); c.line_to(820, 1020)
        c.set_source_rgb(0.9, 0.9, 0.9); c.set_line_width(5); c.stroke()
        f15(c, 540, 1180 - 40 * ap(p, 0, 0.4), 0.8, 0, wing=False)
        c.move_to(860, 980); c.line_to(860, 1100); c.set_source_rgb(*ORG); c.set_line_width(6); c.stroke()
        stamp(c, "6 M", 540, 560, 220, ORG, since)
        text(c, "DE LA BARRIÈRE", 540, 680, 70, WH)


def sc_f_reveal(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:                                             # gros plan cockpit biplace
        sky(c, (0.35, 0.6, 0.9), (0.95, 0.85, 0.65))
        c.new_path(); c.move_to(80, 1300); c.curve_to(300, 560, 780, 560, 1000, 1300); c.close_path(); c.set_source_rgba(0.6, 0.85, 1, 0.25); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(12); c.stroke()
        c.new_path(); c.rectangle(0, 1300, W, H); c.set_source_rgb(0.5, 0.55, 0.6); c.fill()
        turn = ap(p, 0.2, 0.6)
        pilot_body(c, 380, 1080, 1.0); R.eyes_head(c, 380, 990, 105, 'neutral', (40 * turn, -6), t)
        pilot_body(c, 720, 1110, 1.0); R.eyes_head(c, 720, 1020, 105, 'neutral', (-40 * turn, -6), t)
        if turn > 0.5:
            limb(c, [(440, 1120), (540, 1060)], w=22); limb(c, [(660, 1140), (560, 1070)], w=22)
    elif k == 1:                                           # il voit le moignon d'aile
        desert2(c, t, 0)
        f15(c, 340, 900, 1.5, 0, wing=False)
        q = since
        c.new_path(); c.arc(560, 1000, 150 + 20 * math.sin(t * 8), 0, 7); c.set_source_rgba(*RED, 0.9); c.set_line_width(8); c.stroke()
        stamp(c, "PLUS D'AILE !", 540, 480, 150, RED, q, glow=1.0)
    else:                                                  # schéma : le fuselage porte
        desert2(c, t, t)
        f15(c, 540, 860, 1.25, 0, wing=False)
        for j in range(5):
            x = 470 + j * 35; ph = (t * 1.2 + j * 0.2) % 1; y = 1200 - 260 * ph
            c.move_to(x, y); c.line_to(x, y - 90); c.move_to(x - 18, y - 68); c.line_to(x, y - 92); c.line_to(x + 18, y - 68)
            c.set_source_rgba(*GRN, 1 - ph); c.set_line_width(7); c.set_line_cap(1); c.stroke()
        stamp(c, "LE FUSELAGE PORTE", 540, 480, 110, GRN, since)


# ======================= QU'AURAIS-TU FAIT ? : Gimli =======================
def gauges(c, x, y, v1, v2, t):
    for j, v in enumerate((v1, v2)):
        cx = x + (j - 0.5) * 300; c.new_path(); c.arc(cx, y, 110, 0, 7); fill_stroke(c, (0.04, 0.05, 0.07), 8)
        c.new_path(); c.arc(cx, y, 88, math.pi * 0.8, math.pi * (0.8 + 1.4 * v)); c.set_source_rgb(*(GRN if v > 0.5 else RED)); c.set_line_width(14); c.stroke()
        a = math.pi * (0.8 + 1.4 * v); c.move_to(cx, y); c.line_to(cx + math.cos(a) * 80, y + math.sin(a) * 80); c.set_source_rgb(1, 1, 1); c.set_line_width(6); c.stroke()
        text(c, f"MOT {j + 1}", cx, y + 170, 48, WH)


def cockpit_panel(c, dim=0.0):
    c.set_source_rgb(0.05, 0.06, 0.08); c.paint()
    c.new_path(); c.move_to(0, 300); c.line_to(W, 300); c.line_to(W, 700); c.curve_to(700, 640, 380, 640, 0, 700); c.close_path()
    g = cairo.LinearGradient(0, 300, 0, 700); g.add_color_stop_rgb(0, 0.15, 0.35, 0.75); g.add_color_stop_rgb(1, 0.55, 0.7, 0.9); c.set_source(g); c.fill()
    c.new_path(); c.move_to(0, 700); c.curve_to(380, 640, 700, 640, W, 700); c.line_to(W, H); c.line_to(0, H); c.close_path(); fill_stroke(c, (0.12, 0.13, 0.16), 10)
    if dim > 0: c.set_source_rgba(0, 0, 0, 0.6 * dim); c.paint()


def sc_g_hook(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k <= 1:
        sky(c, (0.12, 0.3, 0.7), (0.65, 0.78, 0.92)); clouds(c, t, 1150, 1700, 9, 5, 120, 0.85)
        b767(c, 540, 820 + 8 * math.sin(t), 0.0, 1.5)
        if k == 0: stamp(c, "1983 · CANADA", 540, 640, 120, WH, since)
        else: stamp(c, "12 000 M", 540, 470, 150, WH, since)
    else:
        cockpit_panel(c, dim=ap(p, 0.4, 1.0) if k == 4 else 0)
        v1 = 0.75 - 0.75 * (ap(p, 0.1, 0.8) if k == 3 else (1 if k == 4 else 0))
        v2 = 0.75 - 0.75 * (ap(p, 0.05, 0.6) if k == 4 else 0)
        gauges(c, 540, 1050, v1, v2, t)
        on = (t * 3) % 1 < 0.5
        rr(c, 240, 760, 600, 110, 20); fill_stroke(c, RED if on else (0.35, 0.1, 0.1), 7); text(c, "FUEL", 540, 845, 80, WH)
        if on: radial(c, 540, 815, 450, RED, 0.25)
        lab = ["", "", "ALARME", "MOTEUR 1 : OFF", "MOTEUR 2 : OFF"][k]
        stamp(c, lab, 540, 1340, 110, RED if k > 2 else ORG, since)


def captain(c, x, y, r, t, look=(0, 0), mood='determined'):
    pilot_body(c, x, y + r * 0.9, r / 110)
    R.eyes_head(c, x, y, r, mood, look, t)
    c.new_path(); c.move_to(x - r * 1.05, y - r * 0.45); c.curve_to(x - r * 0.9, y - r * 1.25, x + r * 0.9, y - r * 1.25, x + r * 1.05, y - r * 0.45); c.close_path(); fill_stroke(c, (0.08, 0.1, 0.2), 7)
    rr(c, x - r * 1.2, y - r * 0.55, r * 2.4, r * 0.22, r * 0.1); fill_stroke(c, (0.05, 0.05, 0.08), 5)
    c.new_path(); c.arc(x, y - r * 0.85, r * 0.13, 0, 7); c.set_source_rgb(1, 0.85, 0.3); c.fill()


def sc_g_reveal(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        sky(c, (0.06, 0.08, 0.16), (0.12, 0.16, 0.3)); radial(c, 540, 900, 600, ORG, 0.15)
        captain(c, 540, 860, 150, t, (0, -8))
        stamp(c, "CMDT PEARSON", 540, 420, 120, ORG, since)
        text(c, "PLANEURISTE", 540, 520, 60, WH)
    elif k == 1:                                          # glissade : avion en crabe, commandes croisées
        sky(c, (0.4, 0.6, 0.88), (0.85, 0.85, 0.8))
        c.new_path(); c.rectangle(0, 1250, W, H); c.set_source_rgb(0.4, 0.55, 0.3); c.fill()
        b767(c, 540 + 60 * math.sin(t), 800 + 260 * p, 0.42, 1.25)
        for j in range(6):
            ph = (t * 1.5 + j / 6) % 1; y = 520 + j * 70; x = 120 + 820 * ph
            c.move_to(x, y); c.line_to(x + 90, y + 40); c.set_source_rgba(1, 1, 1, 0.7 * (1 - ph)); c.set_line_width(5); c.stroke()
        stamp(c, "GLISSADE", 540, 430, 150, ORG, since)
        text(c, "ON PERD DE L'ALTITUDE", 540, 540, 60, WH)
    else:                                                 # train avant qui s'effondre, arrêt avant la foule
        sky(c, (0.4, 0.6, 0.88), (0.85, 0.85, 0.8))
        c.new_path(); c.rectangle(0, 1000, W, H); c.set_source_rgb(0.4, 0.55, 0.3); c.fill()
        c.new_path(); c.move_to(470, 1000); c.line_to(610, 1000); c.line_to(1000, H); c.line_to(80, H); c.close_path(); fill_stroke(c, (0.3, 0.3, 0.33), 6)
        r = random.Random(4)
        for j in range(26):                                # foule + voitures au bout de la piste
            x = 380 + 320 * r.random(); y = 990 + 14 * r.random()
            if j % 3 == 0: rr(c, x - 12, y - 6, 24, 10, 3); fill_stroke(c, (RED, BLUE, ORG, YEL)[j % 4], 2)
            else: c.new_path(); c.arc(x, y - 8, 4, 0, 7); c.set_source_rgb(*INK); c.fill()
        kk = ap(p, 0.0, 0.7); s_ = 0.5 + 0.9 * (1 - kk)
        jet(c, 540, 1500 - 400 * kk, 0.12 * ap(p, 0.15, 0.3), s_, gear=1.0)
        if 0.15 < p < 0.85:
            rr_ = random.Random(int(t * 30))
            for _ in range(36):
                a = rr_.uniform(0.2, 2.9); d = rr_.random() * 220 * s_
                x0 = 540 + 240 * s_; y0 = 1500 - 400 * kk + 60 * s_
                c.move_to(x0, y0); c.line_to(x0 + math.cos(a) * d, y0 + math.sin(a) * d); c.set_source_rgba(1, 0.8, 0.3, 0.9); c.set_line_width(3); c.stroke()
        if p > 0.75: stamp(c, "ARRÊT AVANT LA FOULE", 540, 520, 96, GRN, since - 0.75 * (sg['end'] - sg['sent'][2][0]))
        else: stamp(c, "TRAIN AVANT EFFONDRÉ", 540, 520, 96, RED, since)


def sc_f_end(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    desert2(c, t, t * 1.5)
    if k == 0:                                             # nouvelle aile qui se fixe
        f15(c, 540, 860, 1.15, 0.03 * math.sin(t), wing=True)
        c.save(); c.translate(540, 860); c.scale(1.15, 1.15)
        q = ap(p, 0.0, 0.5); c.translate(200 * (1 - q), -120 * (1 - q))
        c.new_path(); c.move_to(50, -40); c.line_to(300, 120); c.line_to(300, 170); c.line_to(50, 140); c.close_path(); fill_stroke(c, GRN, 7, 0.9)
        c.restore()
        if q >= 1:
            for j in range(8):
                a = j * math.pi / 4 + t; c.move_to(660 + math.cos(a) * 40, 900 + math.sin(a) * 40); c.line_to(660 + math.cos(a) * 80, 900 + math.sin(a) * 80)
            c.set_source_rgba(1, 1, 0.6, 0.8); c.set_line_width(5); c.stroke()
        stamp(c, "RÉPARÉ", 540, 480, 170, GRN, since)
    elif k == 1:                                           # choix : atterrir ou s'éjecter
        for j, (lab, col) in enumerate((("ATTERRIR", BLUE), ("S'ÉJECTER", ORG))):
            x = 290 + j * 500; a = ap(since - j * 0.5, 0, 0.3)
            if a <= 0: continue
            rr(c, x - 230, 620, 460, 560, 40); c.set_source_rgba(*col, 0.12 * a); c.fill_preserve(); c.set_source_rgba(*col, 0.9 * a); c.set_line_width(6); c.stroke()
            if j == 0: f15(c, x, 880, 0.55, 0, wing=False)
            else:
                rr(c, x - 50, 820, 100, 150, 20); fill_stroke(c, (0.25, 0.25, 0.3), 6); radial(c, x, 1010, 90, (1, 0.6, 0.2), 0.9)
                R.eyes_head(c, x, 790, 55, 'worried', (0, -8), t)
            text(c, lab, x, 1130, 70, col)
        text(c, "OU", 540, 920, 80, WH, glow=0.5)
    else:                                                  # « dis-le en commentaire »
        f15(c, 540, 1100, 0.7, 0.03 * math.sin(t), wing=False)
        rr(c, 160, 480, 760, 260, 40); fill_stroke(c, (0.97, 0.97, 0.98), 8)
        c.new_path(); c.move_to(300, 735); c.line_to(260, 820); c.line_to(380, 735); c.close_path(); fill_stroke(c, (0.97, 0.97, 0.98), 8)
        txt = "J'AURAIS ATTERRI…"[:max(0, int(since * 14))]
        text(c, txt, 540, 640, 80, (0.1, 0.1, 0.15))


def sc_g_options(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    c.set_source_rgb(0.03, 0.04, 0.07); c.paint(); radial(c, 540, 900, 700, (0.3, 0.4, 0.8), 0.15)
    if k == 0:
        stamp(c, "3 OPTIONS", 540, 960, 220, WH, since)
        return
    for j, (lab, name, col) in enumerate((("A", "WINNIPEG", BLUE), ("B", "GIMLI", ORG), ("C", "UN CHAMP", GRN))):
        if j + 1 > k: continue
        sj = t - sg['sent'][j + 1][0]
        a = eout(sj / 0.25); y = 520 + j * 330; dx = (1 - a) * (400 if j % 2 == 0 else -400)
        act = (j + 1 == k)
        c.save(); c.translate(dx, 0)
        rr(c, 90, y, 900, 260, 40); c.set_source_rgba(*col, (0.22 if act else 0.08) * a); c.fill_preserve(); c.set_source_rgba(*col, (1.0 if act else 0.5) * a); c.set_line_width(7 if act else 4); c.stroke()
        text(c, lab, 220, y + 190, 200, col, glow=a if act else 0.2); text(c, name, 620, y + 165, 100, WH)
        c.restore()


def sc_g_end(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    sky(c, (0.03, 0.08, 0.06), (0.01, 0.02, 0.02)); radial(c, 540, 1000, 700, GRN, 0.15)
    if k == 0:
        n = int(69 * ap(p, 0.05, 0.7))
        for i in range(69):
            x = 175 + (i % 10) * 81; y = 720 + (i // 10) * 85
            on = i < n
            c.new_path(); c.arc(x, y, 22, 0, 7); fill_stroke(c, (0.98, 0.98, 0.99) if on else (0.25, 0.3, 0.28), 4)
            if on:
                c.new_path(); c.arc(x, y + 4, 8, 0.2, math.pi - 0.2); c.set_source_rgb(*INK); c.set_line_width(3); c.stroke()
        stamp(c, f"{n} SURVIVANTS", 540, 520, 140, GRN, since, rot=0)
        if p > 0.6: text(c, "0 BLESSÉ GRAVE", 540, 1400, 80, WH)
    elif k == 1:
        for j, (lab, col) in enumerate((("A", BLUE), ("B", ORG), ("C", GRN))):
            x = 240 + j * 300; q = 1 + 0.08 * math.sin(t * 6 + j * 2)
            c.save(); c.translate(x, 900); c.scale(q, q); c.new_path(); c.arc(0, 0, 120, 0, 7); c.set_source_rgba(*col, 0.2); c.fill_preserve(); c.set_source_rgb(*col); c.set_line_width(8); c.stroke()
            text(c, lab, 0, 75, 200, col, glow=0.8); c.restore()
        stamp(c, "ET TOI ?", 540, 520, 170, WH, since)
    else:
        captain(c, 540, 1180, 110, t, (0, -10), 'neutral')
        rr(c, 160, 420, 760, 260, 40); fill_stroke(c, (0.97, 0.97, 0.98), 8)
        c.new_path(); c.move_to(420, 675); c.line_to(400, 760); c.line_to(500, 675); c.close_path(); fill_stroke(c, (0.97, 0.97, 0.98), 8)
        txt = "MOI J'AURAIS DIT B !"[:max(0, int(since * 14))]
        text(c, txt, 540, 580, 80, (0.1, 0.1, 0.15))


SC6 = {k[3:]: v for k, v in globals().items() if k.startswith('sc_') and callable(v)}
