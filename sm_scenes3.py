"""Scènes 23/10 : SURVIVRAIS-TU ? 9 G, HISTOIRE VRAIE SR-71, QU'AURAIS-TU FAIT ? Hudson."""
import cairo, math, random
from sm_lib import *
from sm_scenes2 import ease, ap, blinkh, civ_body, sky, jet, ORG, BLUE, RED, WH, GRN

def stars(c, t, n=200, seed=1, ymax=H):
    r = random.Random(seed)
    for _ in range(n):
        c.new_path(); c.arc(r.random() * W, r.random() * ymax, r.choice((1, 1, 1.6, 2.4)), 0, 7); c.set_source_rgba(1, 1, 1, (0.3 + 0.6 * r.random()) * (0.75 + 0.25 * math.sin(t * 2 + r.random() * 9))); c.fill()

def gmeter(c, x, y, g, R=150):
    c.new_path(); c.arc(x, y, R, 0, 7); fill_stroke(c, (0.05, 0.06, 0.09), 8)
    a0, a1 = math.pi * 0.75, math.pi * 2.25
    c.new_path(); c.arc(x, y, R - 22, a0, a0 + (a1 - a0) * min(1, g / 10)); c.set_source_rgb(*(RED if g > 6 else ORG if g > 3 else GRN)); c.set_line_width(16); c.set_line_cap(1); c.stroke()
    text(c, f"{g:.1f} G".replace('.', ','), x, y + 30, 90, WH)

def sc_gcock(c, t, sg, lt, u):
    g = 1 + 8 * ap(u, 0.25, 0.85)
    bank = -0.9 * ap(u, 0.15, 0.4)
    c.save(); c.translate(W / 2, 700); c.rotate(bank)
    g1 = cairo.LinearGradient(0, -1400, 0, 1400); g1.add_color_stop_rgb(0, 0.15, 0.35, 0.75); g1.add_color_stop_rgb(0.5, 0.6, 0.78, 0.95); g1.add_color_stop_rgb(0.5, 0.25, 0.4, 0.3); g1.add_color_stop_rgb(1, 0.12, 0.2, 0.15)
    c.rectangle(-1600, -1600, 3200, 3200); c.set_source(g1); c.fill()
    r = random.Random(4)
    for _ in range(14):
        x = (r.random() * 2400 - lt * 300) % 2400 - 1200; y = -900 + r.random() * 800
        for dx, rad in ((0, 60), (55, 45), (-55, 40)): c.new_path(); c.arc(x + dx, y, rad, 0, 7); c.set_source_rgba(1, 1, 1, 0.8); c.fill()
    c.restore()
    # verrière + tableau de bord
    c.new_path(); c.move_to(0, 0); c.line_to(W, 0); c.line_to(W, 260); c.curve_to(700, 160, 380, 160, 0, 260); c.close_path(); c.set_source_rgb(0.08, 0.09, 0.12); c.fill()
    c.new_path(); c.move_to(0, 1050); c.curve_to(380, 1000, 700, 1000, W, 1050); c.line_to(W, H); c.line_to(0, H); c.close_path(); fill_stroke(c, (0.10, 0.11, 0.14), 10)
    gmeter(c, 820, 1230, g)
    # passager arrière (toi) écrasé par les G
    sq = (g - 1) / 8
    rr(c, 230, 1280 + 40 * sq, 220, 260 - 40 * sq, 70); fill_stroke(c, (0.30, 0.36, 0.30), 9)
    blinkh(c, 340, 1190 + 60 * sq, 125, 'worried' if g > 3 else 'neutral', (0, 10 * sq), lt, True)
    if g > 5:
        k = ap(g, 5, 9); gg = cairo.RadialGradient(W / 2, H * 0.45, W * (0.7 - 0.3 * k), W / 2, H * 0.45, W * 1.05)
        gg.add_color_stop_rgba(0, 0, 0, 0, 0); gg.add_color_stop_rgba(1, 0, 0, 0, 0.8 * k); c.set_source(gg); c.paint()

def sc_gweight(c, t, sg, lt, u):
    sky(c, (0.05, 0.05, 0.10), (0.02, 0.02, 0.04))
    k = ap(u, 0.15, 0.5); kg = int(80 + 640 * k)
    c.new_path(); c.move_to(240, 1400); c.line_to(840, 1400); c.line_to(800, 1460); c.line_to(280, 1460); c.close_path(); fill_stroke(c, (0.6, 0.62, 0.68), 8)
    rr(c, 330, 1460, 420, 120, 20); fill_stroke(c, (0.15, 0.16, 0.2), 8)
    text(c, f"{kg} KG", 540, 1550, 100, RED if kg > 400 else GRN, glow=0.6)
    sq = k
    rr(c, 440 - 40 * sq, 1110 + 120 * sq, 200 + 80 * sq, 290 - 120 * sq, 70); fill_stroke(c, (0.25, 0.45, 0.75), 9)
    blinkh(c, 540, 1010 + 150 * sq, 120, 'worried' if k > 0.3 else 'neutral', (0, 10 * sq), lt, False)
    if u > 0.55:
        arm = ap(u, 0.55, 0.9); limb(c, [(620, 1180 + 120 * sq), (700, 1150 + 90 * sq - 60 * arm * (1 - 0.8 * math.sin(lt * 9) ** 2))])
    text(c, "× 9", 540, 500, 220, ORG, glow=1.0)

def _rr(c, x, y, w, h, r):
    c.new_sub_path(); c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2); c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); c.close_path()
def silhouette(c, x, y, s=1.0):
    c.new_path(); c.arc(x, y, 80 * s, 0, 7); c.close_path()
    _rr(c, x - 90 * s, y + 100 * s, 180 * s, 330 * s, 60 * s)
    _rr(c, x - 85 * s, y + 420 * s, 70 * s, 330 * s, 30 * s); _rr(c, x + 15 * s, y + 420 * s, 70 * s, 330 * s, 30 * s)

def sc_gblood(c, t, sg, lt, u):
    sky(c, (0.04, 0.03, 0.06), (0.02, 0.01, 0.03))
    x, y = 540, 470; d = ap(u, 0.15, 0.7)
    silhouette(c, x, y); c.set_source_rgba(1, 1, 1, 0.06); c.fill_preserve(); c.set_source_rgb(0.9, 0.92, 1); c.set_line_width(6); c.stroke()
    c.save(); silhouette(c, x, y); c.clip()
    top = 390 + 700 * d                         # niveau du sang qui descend
    g = cairo.LinearGradient(0, top - 120, 0, top + 120); g.add_color_stop_rgba(0, 0.9, 0.1, 0.15, 0); g.add_color_stop_rgba(1, 0.9, 0.1, 0.15, 0.75)
    c.rectangle(0, top - 120, W, H); c.set_source(g); c.fill(); c.restore()
    hb = 1 + 0.12 * max(0, math.sin(lt * 7))
    c.save(); c.translate(x, 660); c.scale(hb, hb)
    c.new_path(); c.move_to(0, 30); c.curve_to(-60, -10, -40, -60, 0, -30); c.curve_to(40, -60, 60, -10, 0, 30); fill_stroke(c, RED, 5); c.restore()
    for k in range(8):
        ph = (lt * 1.2 + k / 8) % 1; yy = 520 + ph * 650
        c.new_path(); c.arc(x - 30 + (k % 3) * 30, yy, 9, 0, 7); c.set_source_rgba(1, 0.2, 0.2, (1 - ph) * d); c.fill()
    if u > 0.55: text(c, "CERVEAU : PLUS ASSEZ DE SANG", 540, 1400, 66, RED, glow=0.7)

def sc_gvision(c, t, sg, lt, u):
    sky(c, (0.15, 0.35, 0.75), (0.6, 0.78, 0.95))
    r = random.Random(6)
    for _ in range(10):
        x = (r.random() * W * 1.5 - lt * 200) % (W + 300) - 150; y = 300 + r.random() * 1200
        for dx, rad in ((0, 70), (60, 50), (-60, 45)): c.new_path(); c.arc(x + dx, y, rad, 0, 7); c.set_source_rgba(1, 1, 1, 0.85); c.fill()
    jet(c, 540, 900, -0.1, 1.0)
    stages = [("VISION TUNNEL", 0.0), ("VOILE GRIS", 0.3), ("VOILE NOIR", 0.55), ("G-LOC", 0.8)]
    st = max([i for i, (_, a) in enumerate(stages) if u >= a] or [0])
    if st >= 1:
        g = 0.5 if st == 1 else 0.8; c.set_source_rgba(0.5, 0.5, 0.5, g); c.set_operator(cairo.OPERATOR_HSL_SATURATION); c.paint(); c.set_operator(cairo.OPERATOR_OVER)
    k = [0.25, 0.45, 0.85, 1.0][st] * (0.9 + 0.1 * math.sin(lt * 3))
    gg = cairo.RadialGradient(W / 2, H * 0.47, W * max(0.02, 0.7 - 0.65 * k), W / 2, H * 0.47, W * max(0.1, 1.1 - 0.75 * k))
    gg.add_color_stop_rgba(0, 0, 0, 0, 0); gg.add_color_stop_rgba(1, 0, 0, 0, 1); c.set_source(gg); c.paint()
    if st == 3: c.set_source_rgba(0, 0, 0, 0.92); c.paint()
    text(c, stages[st][0], 540, 420, 120, RED if st >= 2 else ORG, glow=1.0)
    for i in range(4):
        c.new_path(); c.arc(330 + i * 140, 540, 16, 0, 7); c.set_source_rgba(*(ORG if i <= st else (0.4, 0.4, 0.45))); c.fill()

def gsuit_fig(c, x, y, inflate, lt):
    rr(c, x - 90, y, 180, 330, 60); fill_stroke(c, (0.30, 0.36, 0.30), 9)
    for k, (bx, by, bw, bh) in enumerate(((x - 75, y + 200, 150, 90), (x - 85, y + 420, 70, 150), (x + 15, y + 420, 70, 150), (x - 85, y + 600, 70, 120), (x + 15, y + 600, 70, 120))):
        p = 1 + 0.18 * inflate * (0.8 + 0.2 * math.sin(lt * 5 + k))
        rr(c, bx - bw * (p - 1) / 2, by - bh * (p - 1) / 2, bw * p, bh * p, 24); fill_stroke(c, (0.55, 0.6, 0.35) if inflate < 0.5 else ORG, 6)
    rr(c, x - 85, y + 330, 70, 420, 30); rr(c, x + 15, y + 330, 70, 420, 30); c.set_source_rgba(0.3, 0.36, 0.3, 0.0); c.fill()

def sc_gsuit(c, t, sg, lt, u):
    sky(c, (0.04, 0.05, 0.10), (0.02, 0.02, 0.04))
    inf = ap(u, 0.35, 0.55)
    gsuit_fig(c, 540, 820, inf, lt)
    blinkh(c, 540, 730, 120, 'determined', (0, 0), lt, True)
    if inf > 0.2:
        for k in range(6):
            ph = (lt * 1.5 + k / 6) % 1; c.new_path(); c.arc(540, 1250 - ph * 500, 10, 0, 7); c.set_source_rgba(1, 0.25, 0.25, 1 - ph); c.fill()
    if u > 0.3: text(c, "COMBINAISON ANTI-G", 540, 430, 90, WH, glow=0.4)
    if u > 0.6: text(c, "+1 G", 820, 1000, 140, GRN, glow=1.0)

def sc_gstrain(c, t, sg, lt, u):
    sky(c, (0.04, 0.05, 0.10), (0.02, 0.02, 0.04))
    cyc = (lt % 3) / 3; push = 1 if cyc < 0.15 else 0
    gsuit_fig(c, 540, 820, 1, lt)
    blinkh(c, 540, 730 - 6 * push, 120, 'determined', (0, 0), lt, True)
    if push:
        for k in range(3): c.new_path(); c.arc(640 + k * 40, 760, 10 + k * 8, 0, 7); c.set_source_rgba(1, 1, 1, 0.6 - k * 0.15); c.fill()
    c.new_path(); c.arc(540, 560, 60, -math.pi / 2, -math.pi / 2 + 2 * math.pi * cyc); c.set_source_rgb(*ORG); c.set_line_width(12); c.stroke()
    text(c, "3 S", 540, 585, 60, WH)
    if u > 0.2: text(c, "CONTRACTE + EXPIRE", 540, 430, 90, WH, glow=0.4)
    if u > 0.55: text(c, "+4 G", 820, 1000, 140, GRN, glow=1.0)

def sc_gverdict(c, t, sg, lt, u):
    sky(c, (0.08, 0.02, 0.03), (0.02, 0.01, 0.01)); radial(c, 300, 1000, 500, RED, 0.15); radial(c, 780, 1000, 500, GRN, 0.12 * ap(u, 0.5, 0.6))
    rr(c, 190, 1130, 220, 230, 70); fill_stroke(c, (0.25, 0.45, 0.75), 9)
    c.save(); c.translate(300, 1060); c.rotate(0.5); blinkh(c, 0, 0, 105, 'neutral', (0, 20), 99, False); c.restore()
    for sx in (-1, 1):
        c.move_to(300 + sx * 25 - 15, 1050 - 10); c.line_to(300 + sx * 25 + 15, 1050 + 10); c.move_to(300 + sx * 25 + 15, 1050 - 10); c.line_to(300 + sx * 25 - 15, 1050 + 10)
    c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    text(c, "TOI : 4-6 G", 300, 1480, 66, RED)
    if u > 0.5:
        pilot_body(c, 780, 1130, 1.1); blinkh(c, 780, 1040, 110, 'determined', (0, 0), lt, True)
        text(c, "PILOTE : 9 G", 780, 1480, 66, GRN)
    s = 1 + 0.15 * max(0, 1 - lt / 0.3)
    c.save(); c.translate(540, 480); c.rotate(-0.06); c.scale(s, s)
    rr(c, -440, -110, 880, 200, 30); c.set_source_rgba(*RED, 0.15); c.fill_preserve(); c.set_source_rgb(*RED); c.set_line_width(8); c.stroke()
    text(c, "TU T'ÉVANOUIS", 0, 50, 150, RED, glow=1.0); c.restore()

# ---------- SR-71 ----------
def sr71(c, x, y, s=1.0, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.new_path(); c.move_to(320, 0); c.curve_to(200, -14, 60, -22, -40, -30); c.line_to(-230, -150); c.line_to(-280, -150); c.line_to(-210, -30); c.line_to(-300, -14)
    c.line_to(-300, 14); c.line_to(-210, 30); c.line_to(-280, 150); c.line_to(-230, 150); c.line_to(-40, 30); c.curve_to(60, 22, 200, 14, 320, 0); c.close_path(); fill_stroke(c, (0.24, 0.26, 0.32), 8)
    for sy in (-1, 1):
        rr(c, -250, sy * 70 - 18, 230, 36, 18); fill_stroke(c, (0.30, 0.32, 0.38), 6)
        c.new_path(); c.move_to(-170, sy * 70); c.line_to(-150, sy * 150); c.line_to(-120, sy * 150); c.line_to(-130, sy * 70); c.close_path(); fill_stroke(c, (0.30, 0.32, 0.38), 5)
    c.restore()

def earth_curve(c, t, y=1250):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, 0.0, 0.0, 0.02); g.add_color_stop_rgb(0.55, 0.02, 0.04, 0.12); g.add_color_stop_rgb(1, 0.05, 0.12, 0.3); c.set_source(g); c.paint()
    stars(c, t, 220, 3, y)
    c.new_path(); c.arc(W / 2, y + 2600, 2600, 0, 7); c.set_source_rgb(0.08, 0.18, 0.35); c.fill()
    c.new_path(); c.arc(W / 2, y + 2600, 2600, math.pi * 1.2, math.pi * 1.8); c.set_source_rgba(0.4, 0.75, 1, 0.8); c.set_line_width(10); c.stroke()
    radial(c, W / 2, y, 700, (0.4, 0.75, 1), 0.2)

def sc_sr_hook(c, t, sg, lt, u):
    sky(c, (0.03, 0.04, 0.08), (0.01, 0.01, 0.02))
    rr(c, 190, 780, 700, 360, 50); fill_stroke(c, (0.12, 0.13, 0.17), 10)
    for k in range(12):
        a = 0.5 + 0.5 * math.sin(lt * 9 + k)
        rr(c, 260 + k * 48, 1000 - 120 * a, 24, 120 * a + 4, 6); c.set_source_rgba(*GRN, 0.9); c.fill()
    text(c, "« QUELLE EST", 540, 880, 70, WH); text(c, "MA VITESSE ? »", 540, 960, 70, ORG, glow=0.6)
    for k in range(3):
        ph = (lt * 1.1 + k / 3) % 1; c.new_path(); c.arc(540, 700, 40 + ph * 260, math.pi * 1.15, math.pi * 1.85); c.set_source_rgba(*BLUE, 1 - ph); c.set_line_width(6); c.stroke()

def sc_sr_intro(c, t, sg, lt, u):
    earth_curve(c, lt)
    sr71(c, 540 + 40 * math.sin(lt * 0.4), 760, 1.3)
    radial(c, 120, 760, 160, (1, 0.6, 0.2), 0.5 + 0.2 * math.sin(lt * 20))
    if u > 0.3: text(c, "20 KM D'ALTITUDE", 540, 470, 80, WH, glow=0.4)
    if u > 0.6:
        rr(c, 140, 1120, 800, 200, 34); c.set_source_rgba(0, 0, 0, 0.5); c.fill()
        text(c, "LE JET LE PLUS RAPIDE", 540, 1200, 64, ORG, glow=0.5); text(c, "JAMAIS MIS EN SERVICE", 540, 1280, 54, WH)

SPEEDS = []
def sc_radio1(c, t, sg, lt, u):
    p = sg['p']
    sky(c, (0.03, 0.05, 0.10), (0.01, 0.02, 0.04))
    # tour de contrôle
    rr(c, 70, 340, 300, 140, 26); fill_stroke(c, (0.15, 0.16, 0.22), 8); text(c, "L.A. CENTER", 220, 430, 50, BLUE)
    for k in range(3):
        ph = (lt * 1.3 + k / 3) % 1; c.new_path(); c.arc(370, 410, 30 + ph * 140, -0.6, 0.6); c.set_source_rgba(*BLUE, 1 - ph); c.set_line_width(5); c.stroke()
    text(c, p['plane'], 540, 640, 80 if len(p['plane']) < 14 else 64, WH, glow=0.4)
    # barres des vitesses (cumulées d'une scène à l'autre)
    allp = [(90, "CESSNA"), (125, "BIMOTEUR"), (620, "F-18"), (1842, "SR-71")]
    idx = [k for k, _ in allp].index(p['kt'])
    maxv = 1842 if idx == 3 else 700
    for i in range(idx + 1):
        kt, lab = allp[i]; y = 740 + i * 170
        grow = 1 if i < idx else ap(u, 0.35, 0.6)
        if i == 3: grow = ap(u, 0.5, 0.75)
        w = 740 * min(1, kt / maxv) * grow
        col = RED if i == 3 else ORG if i == idx else (0.5, 0.55, 0.65)
        text(c, lab, 60, y + 82, 50, WH, anchor='l')
        rr(c, 290, y + 20, max(10, w), 100, 24); c.set_source_rgb(*col); c.fill()
        if grow > 0.9: text(c, f"{kt} KT", (310 + w) if w < 560 else (290 + w / 2), y + 92, 64, WH if w >= 560 else col, anchor='l' if w < 560 else 'c')
    if u > 0.6:
        text(c, f"{p['kmh']:,} KM/H".replace(',', ' '), 540, 1500, 130 if idx == 3 else 100, RED if idx == 3 else ORG, glow=1.0 if idx == 3 else 0.5)
    if idx == 3:
        sr71(c, 1200 - (lt * 900) % 1800, 560, 0.5)

def sc_sr_end(c, t, sg, lt, u):
    earth_curve(c, lt, 1350)
    sr71(c, -300 + ((lt * 380) % (W + 700)), 700, 0.9)
    text(c, "SILENCE RADIO", 540, 470, 130, WH, glow=0.6)
    text(c, "1 842 KT", 540, 1050, 160, RED, glow=1.0)

# ---------- Hudson ----------
def skyline(c, y, col=(0.10, 0.12, 0.18), seed=2):
    r = random.Random(seed); x = 0
    while x < W:
        w = 50 + r.random() * 70; h = 120 + r.random() * 330
        c.new_path(); c.rectangle(x, y - h, w, h); c.set_source_rgb(*col); c.fill()
        for k in range(int(h / 40)):
            for j in range(int(w / 25)):
                if r.random() < 0.4: c.new_path(); c.rectangle(x + 6 + j * 22, y - h + 12 + k * 38, 8, 12); c.set_source_rgba(1, 0.85, 0.45, 0.6); c.fill()
        x += w + 6

def bird(c, x, y, s, t):
    f = math.sin(t * 12) * 0.5
    c.move_to(x - 30 * s, y - 10 * s * f); c.curve_to(x - 15 * s, y - 20 * s, x - 5 * s, y - 5 * s, x, y); c.curve_to(x + 5 * s, y - 5 * s, x + 15 * s, y - 20 * s, x + 30 * s, y - 10 * s * f)
    c.set_source_rgb(*INK); c.set_line_width(5); c.set_line_cap(1); c.stroke()

def sc_su_hook(c, t, sg, lt, u):
    sky(c, (0.45, 0.62, 0.85), (0.85, 0.88, 0.92))
    skyline(c, 1500); c.new_path(); c.rectangle(0, 1500, W, H); c.set_source_rgb(0.15, 0.2, 0.28); c.fill()
    hit = u > 0.7
    jet(c, 540, 800 - 80 * ap(u, 0, 0.7), -0.15 + 0.15 * ap(u, 0.7, 1), 1.1)
    for k in range(9):
        bx = 1150 - ap(u, 0.45, 0.72) * 700 + (k % 3) * 60; by = 700 + (k // 3) * 40 + 20 * math.sin(lt * 3 + k)
        if not hit: bird(c, bx, by, 0.9, lt + k)
    if hit:
        fl = max(0, 1 - (u - 0.7) / 0.05); c.set_source_rgba(1, 1, 1, 0.8 * fl); c.paint()
        for sx in (-1, 1):
            for k in range(6):
                ph = (lt * 1.5 + k / 6) % 1; c.new_path(); c.arc(520 - ph * 250 + sx * 30, 830 + 20 * sx + ph * 40, 12 + ph * 25, 0, 7); c.set_source_rgba(0.3, 0.3, 0.35, 0.6 * (1 - ph)); c.fill()
        text(c, "2 MOTEURS PERDUS", 540, 520, 100, RED, glow=1.0)
    elif u > 0.3: text(c, "860 M", 540, 520, 120, WH, glow=0.4)

def sc_su_glide(c, t, sg, lt, u):
    sky(c, (0.45, 0.62, 0.85), (0.85, 0.88, 0.92))
    skyline(c, 1500); c.new_path(); c.rectangle(0, 1500, W, H); c.set_source_rgb(0.15, 0.2, 0.28); c.fill()
    jet(c, 540, 760 + 120 * u, 0.06, 1.1)
    sec = int(180 - 30 * u)
    rr(c, 300, 1150, 480, 220, 34); c.set_source_rgba(0, 0, 0, 0.55); c.fill()
    text(c, f"{sec // 60}:{sec % 60:02d}", 540, 1310, 150, RED, glow=0.8)
    if u > 0.2: text(c, "PLANEUR DE 60+ TONNES", 540, 520, 80, WH, glow=0.4)

def nyc_map(c, a=1.0):
    c.set_source_rgb(0.12, 0.16, 0.12); c.paint()
    c.new_path(); c.move_to(420, 0); c.curve_to(470, 500, 400, 1100, 470, H); c.line_to(600, H); c.curve_to(530, 1100, 600, 500, 560, 0); c.close_path(); c.set_source_rgb(0.15, 0.3, 0.55); c.fill()
    c.new_path(); c.move_to(600, 1450); c.curve_to(800, 1300, 900, 1250, W, 1200); c.line_to(W, 1320); c.curve_to(900, 1380, 800, 1430, 620, 1560); c.close_path(); c.set_source_rgb(0.15, 0.3, 0.55); c.fill()
def sc_su_options(c, t, sg, lt, u):
    nyc_map(c)
    pts = dict(P=(640, 1080), A=(900, 1290), B=(250, 600), C=(500, 860))
    c.save(); c.translate(*pts['P']); c.rotate(-2.6); c.new_path(); c.move_to(40, 0); c.line_to(-30, -26); c.line_to(-15, 0); c.line_to(-30, 26); c.close_path(); fill_stroke(c, WH, 5); c.restore()
    for k, (lab, name, col, a0) in enumerate((("A", "LAGUARDIA", BLUE, 0.1), ("B", "TETERBORO", ORG, 0.38), ("C", "L'HUDSON", GRN, 0.65))):
        a = ap(u, a0, a0 + 0.1)
        if a <= 0: continue
        x, y = pts[lab]
        c.new_path(); c.move_to(*pts['P']); c.curve_to(pts['P'][0], (pts['P'][1] + y) / 2, (pts['P'][0] + x) / 2, y, x, y); c.set_source_rgba(*col, a); c.set_line_width(7); c.set_dash([20, 14]); c.stroke(); c.set_dash([])
        c.new_path(); c.arc(x, y, 60, 0, 7); fill_stroke(c, col, 7, a); text(c, lab, x, y + 30, 90, (0.02, 0.02, 0.04))
        text(c, name, x, y + 120 if y < 1300 else y - 80, 52, WH)

def sc_su_pause(c, t, sg, lt, u):
    nyc_map(c); c.set_source_rgba(0, 0, 0, 0.65); c.paint()
    n = 3 - int(min(2.999, lt * 3 / max(1, sg['end'] - sg['t0'])))
    s = 1 + 0.2 * (1 - (lt % 1))
    c.save(); c.translate(540, 900); c.scale(s, s); text(c, str(n), 0, 120, 360, ORG, glow=1.2); c.restore()
    text(c, "A, B OU C ?", 540, 520, 130, WH, glow=0.6)

def sc_su_reveal(c, t, sg, lt, u):
    sky(c, (0.55, 0.65, 0.80), (0.75, 0.80, 0.85))
    skyline(c, 1000, (0.25, 0.28, 0.35), 5)
    c.new_path(); c.rectangle(0, 1000, W, H); c.set_source_rgb(0.2, 0.32, 0.45); c.fill()
    for k in range(20):
        y = 1040 + k * 45; c.move_to((k * 131 + lt * 40) % W, y); c.line_to((k * 131 + lt * 40) % W + 90, y); c.set_source_rgba(1, 1, 1, 0.25); c.set_line_width(3); c.stroke()
    k = ap(u, 0.0, 0.4)
    jet(c, 540, 700 + 420 * k, 0.08 * (1 - k), 1.0 + 0.3 * k, wind=True)
    if k >= 1:
        for j in range(5):
            ph = (lt + j / 5) % 1; c.new_path(); c.save(); c.translate(540, 1150); c.scale(1, 0.25); c.arc(0, 0, 200 + ph * 300, 0, 7); c.restore(); c.set_source_rgba(1, 1, 1, 0.4 * (1 - ph)); c.set_line_width(4); c.stroke()
    if u > 0.5:
        rr(c, 190, 300, 700, 200, 34); c.set_source_rgba(0, 0, 0, 0.5); c.fill(); text(c, "155 SURVIVANTS", 540, 440, 110, GRN, glow=0.8)

def sc_su_sim(c, t, sg, lt, u):
    sky(c, (0.03, 0.04, 0.08), (0.01, 0.01, 0.02))
    text(c, "SIMULATEUR", 540, 420, 90, WH, glow=0.3)
    a = ap(u, 0.1, 0.25)
    rr(c, 90, 560, 900, 360, 40); c.set_source_rgba(*GRN, 0.08 * a); c.fill_preserve(); c.set_source_rgba(*GRN, 0.8 * a); c.set_line_width(5); c.stroke()
    if a > 0:
        text(c, "DEMI-TOUR IMMÉDIAT", 540, 650, 56, WH)
        for i in range(13):
            ok = i < 7; x = 160 + i * 63; col = GRN if ok else RED
            if ap(u, 0.15 + i * 0.015, 0.2 + i * 0.015) > 0: c.new_path(); c.arc(x, 780, 24, 0, 7); c.set_source_rgb(*col); c.fill()
        text(c, "7 / 13 RÉUSSIS", 540, 880, 60, GRN)
    b = ap(u, 0.55, 0.7)
    if b > 0:
        rr(c, 90, 1000, 900, 360, 40); c.set_source_rgba(*RED, 0.1 * b); c.fill_preserve(); c.set_source_rgba(*RED, 0.85 * b); c.set_line_width(5); c.stroke()
        text(c, "+ 35 S POUR DÉCIDER", 540, 1100, 60, WH); text(c, "CRASH", 540, 1290, 160, RED, glow=1.0)

def sc_su_end(c, t, sg, lt, u):
    sky(c, (0.03, 0.08, 0.06), (0.01, 0.02, 0.02)); radial(c, 540, 1000, 700, GRN, 0.15)
    pilot_body(c, 540, 1180, 1.35)
    limb(c, [(480, 1220), (380, 1120), (360, 1020)]); limb(c, [(600, 1220), (700, 1120), (720, 1020)])
    blinkh(c, 540, 1060, 140, 'determined', (0, -10), lt, False, rim=GRN)
    text(c, "LE BON CHOIX", 540, 520, 150, GRN, glow=1.0)
    text(c, "ET TOI : A, B OU C ?", 540, 660, 64, WH)

SC3 = dict(gcock=sc_gcock, gweight=sc_gweight, gblood=sc_gblood, gvision=sc_gvision, gsuit=sc_gsuit, gstrain=sc_gstrain, gverdict=sc_gverdict,
           sr_hook=sc_sr_hook, sr_intro=sc_sr_intro, radio1=sc_radio1, sr_end=sc_sr_end,
           su_hook=sc_su_hook, su_glide=sc_su_glide, su_options=sc_su_options, su_pause=sc_su_pause, su_reveal=sc_su_reveal, su_sim=sc_su_sim, su_end=sc_su_end)
