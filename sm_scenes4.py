"""Scènes 24/10 : TU ES LE PILOTE ép. 2, SURVIVRAIS-TU éjection, HISTOIRE VRAIE United 232. R = module sm_render injecté (ocean_bg, plane, flames, rain, CFG)."""
import cairo, math, random
from sm_lib import *
from sm_scenes2 import ease, ap, blinkh, civ_body, sky, jet, ORG, BLUE, RED, WH, GRN
from sm_scenes3 import sr71, stars
R = None

# ---------- ép. 2 ----------
def sc_e2_recap(c, t, sg, lt, u):
    R.ocean_bg(c, lt)
    R.plane(c, 540, 720 + 6 * math.sin(lt * 1.3), -0.03, lt, True, 0.3)
    rr(c, 120, 1150, 840, 330, 40); c.set_source_rgba(0, 0, 0, 0.6); c.fill()
    for k, (lab, txt, col) in enumerate((("A", "DEMI-TOUR", BLUE), ("B", "LE CARGO", ORG))):
        y = 1230 + k * 130; win = k == 0 and u > 0.6
        a = 1.0 if (u < 0.6 or win) else 0.25
        c.push_group(); text(c, lab, 220, y + 40, 110, col); text(c, txt, 560, y + 40, 90, WH); c.pop_group_to_source(); c.paint_with_alpha(a)
        if win:
            rr(c, 140, y - 50, 800, 115, 24); c.set_source_rgb(*col); c.set_line_width(6); c.stroke()
    if u > 0.6: text(c, "LE PILOTE A CHOISI", 540, 420, 100, BLUE, glow=1.0)
    else: text(c, "PAS ASSEZ DE VOTES", 540, 420, 90, (0.85, 0.88, 0.95), glow=0.3)

def sc_e2_turn(c, t, sg, lt, u):
    R.ocean_bg(c, lt)
    bank = -0.35 * math.sin(math.pi * ap(u, 0.05, 0.8))
    R.plane(c, 540, 700 + 80 * u, bank, lt, True, 0)
    # cargo qui s'éloigne
    k = ap(u, 0.3, 0.9); x = 860 + 300 * k; s = 1 - 0.6 * k
    c.save(); c.translate(x, 1070); c.scale(s, s)
    c.new_path(); c.move_to(-160, 0); c.line_to(170, 0); c.line_to(140, 40); c.line_to(-130, 40); c.close_path(); fill_stroke(c, (0.12, 0.14, 0.2), 6)
    for j in range(5): c.new_path(); c.arc(-110 + j * 50, 12, 5, 0, 7); c.set_source_rgb(1, 0.85, 0.4); c.fill()
    c.restore()
    alt = int(2500 - 300 * ap(u, 0.1, 0.9))
    rr(c, 260, 1300, 560, 170, 30); c.set_source_rgba(0, 0, 0, 0.5); c.fill()
    text(c, f"{alt:,} M".replace(',', ' '), 540, 1415, 120, ORG, glow=0.5)

def gauge_bar(c, x, y, w, lvl, col, label):
    rr(c, x, y, w, 100, 40); c.set_source_rgba(1, 1, 1, 0.08); c.fill_preserve(); c.set_source_rgba(1, 1, 1, 0.6); c.set_line_width(5); c.stroke()
    rr(c, x + 14, y + 14, max(30, (w - 28) * lvl), 72, 30); c.set_source_rgb(*col); c.fill()
    text(c, label, x + w / 2, y + 170, 42, (0.8, 0.85, 0.95), 'Montserrat')

def sc_e2_fuel(c, t, sg, lt, u):
    c.set_source_rgb(0.03, 0.03, 0.05); c.paint()
    on = (lt * 2.5) % 1 < 0.55 and u > 0.1
    if on: radial(c, 540, 700, 600, RED, 0.35)
    rr(c, 330, 520, 420, 120, 20); fill_stroke(c, RED if on else (0.35, 0.1, 0.1), 7)
    text(c, "LOW FUEL", 540, 605, 80, (1, 0.95, 0.95) if on else (0.6, 0.4, 0.4))
    gauge_bar(c, 140, 820, 800, 0.18 - 0.06 * ap(u, 0.2, 1), RED, "CARBURANT")
    if u > 0.55: text(c, "IRLANDE : 40 KM", 540, 1250, 110, BLUE, glow=0.8)

def sc_e2_coast(c, t, sg, lt, u):
    R.ocean_bg(c, lt, horizon=980)
    a = ap(u, 0.0, 0.3)
    c.new_path(); c.move_to(0, 980); c.curve_to(300, 940, 700, 950, W, 960); c.line_to(W, 1000); c.line_to(0, 1000); c.close_path(); c.set_source_rgba(0.08, 0.12, 0.1, a); c.fill()
    r = random.Random(9)
    for _ in range(40):
        x = r.random() * W; c.new_path(); c.arc(x, 950 + r.random() * 30, 3 + r.random() * 3, 0, 7); c.set_source_rgba(1, 0.85, 0.45, a * (0.6 + 0.4 * math.sin(lt * 3 + x))); c.fill()
    if u > 0.35:
        rr(c, 120, 1180, 840, 140, 30); fill_stroke(c, (0.97, 0.97, 0.98), 7)
        text(c, "SHANNON : PISTE 24", 540, 1275, 70, (0.1, 0.3, 0.7))
    if u > 0.65: text(c, "12 MIN", 540, 600, 200, ORG, glow=1.0)

def sc_e2_cough(c, t, sg, lt, u):
    R.ocean_bg(c, lt, horizon=1000)
    cough = (0.2 < u < 0.3) or (0.42 < u < 0.52)
    jit = 8 * math.sin(lt * 40) if cough else 0
    R.plane(c, 540, 700 + jit, -0.02, lt, True, 0)
    if cough:
        for k in range(5): c.new_path(); c.arc(640 + k * 30, 760 + k * 6, 14 + k * 6, 0, 7); c.set_source_rgba(0.2, 0.2, 0.25, 0.6 - k * 0.1); c.fill()
        text(c, "TEUF… TEUF…", 540, 520, 110, RED, glow=0.8)
    pilot_body(c, 300, 1450, 1.1)
    R.eyes_head(c, 300, 1360, 110, 'worried', (30, -20), lt, rim=RED if cough else (0.6, 0.7, 1))

def sc_e2_think(c, t, sg, lt, u):
    sky(c, (0.04, 0.05, 0.10), (0.01, 0.01, 0.03))
    left = u < 0.5
    for side, (cx, col, lab) in enumerate(((290, BLUE, "LA PLAGE"), (790, ORG, "LA PISTE"))):
        a = ap(u, 0.03 + side * 0.45, 0.12 + side * 0.45)
        if a <= 0: continue
        act = (side == 0) == left; dim = 1.0 if act else 0.45
        c.save(); rr(c, cx - 240, 470, 480, 400, 60); fill_stroke(c, (0.97, 0.97, 0.98), 9, a * dim); rr(c, cx - 240, 470, 480, 400, 60); c.clip()
        c.set_source_rgba(0.04, 0.06, 0.12, a * dim); c.paint()
        if side == 0:
            c.new_path(); c.move_to(cx - 240, 760); c.curve_to(cx - 80, 720, cx + 80, 740, cx + 240, 700); c.line_to(cx + 240, 870); c.line_to(cx - 240, 870); c.close_path(); c.set_source_rgba(0.75, 0.68, 0.5, a * dim); c.fill()
            radial(c, cx + 120, 560, 120, (1, 0.95, 0.8), 0.3 * a * dim)
        else:
            c.new_path(); c.move_to(cx - 40, 870); c.line_to(cx - 10, 650); c.line_to(cx + 10, 650); c.line_to(cx + 40, 870); c.close_path(); c.set_source_rgba(0.3, 0.3, 0.35, a * dim); c.fill()
            for k in range(6): c.new_path(); c.arc(cx - 25 + k * 2, 860 - k * 38, 4, 0, 7); c.arc(cx + 25 - k * 2, 860 - k * 38, 4, 0, 7); c.set_source_rgba(1, 0.85, 0.4, a * dim); c.fill()
        text(c, lab, cx, 560, 70, col, glow=0.6 * dim)
        c.restore()
    by = 4 * math.sin(lt * 2)
    pilot_body(c, W / 2, 1300 + by, 1.3)
    R.eyes_head(c, W / 2, 1180 + by, 140, 'worried', (-30 if left else 30, -20), lt, rim=BLUE if left else ORG)

def sc_e2_choice(c, t, sg, lt, u):
    c.set_source_rgb(0.02, 0.02, 0.04); c.paint()
    N = R.CFG.NEXT
    for side, (col, lab) in enumerate(((BLUE, "A"), (ORG, "B"))):
        sub, l1, l2 = N[lab]
        a = ap(u, 0.12 + side * 0.12, 0.25 + side * 0.12); y0 = 520 + side * 620; dx = (1 - a) * (300 if side == 0 else -300)
        c.save(); c.translate(dx, 0)
        rr(c, 70, y0, 940, 560, 40); c.set_source_rgba(*col, 0.08 * a); c.fill_preserve(); c.set_source_rgba(*col, 0.85 * a); c.set_line_width(5); c.stroke()
        c.save(); rr(c, 70, y0, 940, 560, 40); c.clip(); radial(c, 300, y0 + 280, 500, col, 0.2 * a); c.restore()
        if a > 0.05:
            text(c, lab, 200, y0 + 340, 300, col, glow=a); text(c, sub, 640, y0 + 250, 92, WH)
            text(c, l1, 640, y0 + 320, 36, (0.75, 0.8, 0.9), 'Montserrat'); text(c, l2, 640, y0 + 380, 36, col, 'Montserrat')
        c.restore()
    c.new_path(); c.arc(W / 2, 1080, 120, 0, 7); c.set_source_rgb(0.02, 0.02, 0.04); c.fill()
    lx = -22 if (lt % 2.4) < 1.2 else 22
    R.eyes_head(c, W / 2, 1080, 95, 'worried', (lx * 0.5, -14 if lx < 0 else 14), lt)
    text(c, "TU FAIS QUOI ?", W / 2, 330, 140, WH, glow=0.5)
    if u > 0.6:
        text(c, "ÉCRIS A OU B EN COMMENTAIRE", W / 2, 1790, 46, (0.9, 0.92, 1.0), 'Montserrat')
        text(c, "LA MAJORITÉ DÉCIDE DE L'ÉPISODE 3", W / 2, 1855, 36, ORG, 'Montserrat')

# ---------- éjection ----------
def fighter(c, x, y, s=1.0, rot=0.0, canopy=True):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.new_path(); c.move_to(300, 0); c.line_to(120, -26); c.line_to(-60, -30); c.line_to(-220, -24); c.line_to(-260, -10); c.line_to(-260, 18); c.line_to(-60, 26); c.line_to(120, 22); c.close_path(); fill_stroke(c, (0.55, 0.6, 0.66), 8)
    c.new_path(); c.move_to(-40, 20); c.line_to(-150, 110); c.line_to(-200, 110); c.line_to(-170, 22); c.close_path(); fill_stroke(c, (0.5, 0.55, 0.6), 7)
    c.new_path(); c.move_to(-180, -24); c.line_to(-240, -110); c.line_to(-210, -110); c.line_to(-140, -26); c.close_path(); fill_stroke(c, (0.5, 0.55, 0.6), 7)
    if canopy:
        c.new_path(); c.move_to(160, -24); c.curve_to(120, -70, 40, -70, 20, -28); c.close_path(); fill_stroke(c, (0.35, 0.75, 1.0), 6)
    c.restore()

def sc_ej_cock(c, t, sg, lt, u):
    sky(c, (0.15, 0.30, 0.65), (0.55, 0.70, 0.90))
    for k in range(18):
        ph = (lt * 3 + k / 18) % 1; y = (k * 113) % H; c.move_to(W * (1 - ph), y); c.line_to(W * (1 - ph) - 160, y); c.set_source_rgba(1, 1, 1, 0.35); c.set_line_width(3); c.stroke()
    fighter(c, 540, 650, 1.2, 0.05 * math.sin(lt * 9) * ap(u, 0.3, 0.5))
    on = (lt * 3) % 1 < 0.5 and u > 0.3
    if on: radial(c, 540, 1300, 600, RED, 0.3)
    rr(c, 360, 1050, 360, 120, 20); fill_stroke(c, RED if on else (0.35, 0.1, 0.1), 7); text(c, "MACH 0,95", 540, 1135, 70, WH)
    pull = ap(u, 0.7, 0.85)
    pilot_body(c, 540, 1380, 1.2)
    R.eyes_head(c, 540, 1280, 115, 'worried' if u > 0.3 else 'neutral', (0, 20 * pull), lt)
    hy = 1440 - 40 * pull
    rr(c, 480, hy, 120, 40, 14); fill_stroke(c, (1, 0.85, 0.2), 6)
    limb(c, [(470, 1420), (500, hy + 20)]); limb(c, [(610, 1420), (580, hy + 20)])

def sc_ej_canopy(c, t, sg, lt, u):
    sky(c, (0.15, 0.30, 0.65), (0.55, 0.70, 0.90))
    k = ap(u, 0.15, 0.45)
    fighter(c, 540, 900, 1.6, 0, canopy=k < 0.05)
    if k > 0:
        fl = max(0, 1 - (u - 0.15) / 0.06); c.set_source_rgba(1, 1, 1, 0.7 * fl); c.paint()
        for j in range(16):
            r = random.Random(j); a = r.random() * 6.28; d = 500 * k * (0.5 + r.random())
            c.save(); c.translate(560 + math.cos(a) * d, 840 - abs(math.sin(a)) * d); c.rotate(lt * 5 + j); rr(c, -20, -10, 40, 20, 4); c.set_source_rgba(0.5, 0.8, 1, 0.8 * (1 - k * 0.5)); c.fill(); c.restore()
    if u > 0.75:
        s = ap(u, 0.75, 1.0); y = 820 - 500 * s
        radial(c, 560, y + 120, 160, (1, 0.6, 0.2), 0.8)
        rr(c, 510, y - 60, 100, 160, 20); fill_stroke(c, (0.25, 0.25, 0.3), 7)
        R.eyes_head(c, 560, y - 70, 60, 'worried', (0, -10), lt)

def sc_ej_g(c, t, sg, lt, u):
    sky(c, (0.05, 0.05, 0.10), (0.02, 0.02, 0.04))
    g = 13 * ap(u, 0.05, 0.25) * (1 - 0.9 * ap(u, 0.5, 0.65)) + 1
    from sm_scenes3 import gmeter
    gmeter(c, 540, 600, g, 200)
    sq = min(1, (g - 1) / 13)
    x, y0 = 540, 1050
    for i in range(7):  # vertèbres qui se tassent
        y = y0 + i * (70 - 25 * sq); rr(c, x - 60, y, 120, 50 - 10 * sq, 14); fill_stroke(c, (0.95, 0.93, 0.88), 6)
    radial(c, 540, 1450, 300, (1, 0.6, 0.2), 0.6 * sq)
    if u > 0.7: text(c, "COLONNE COMPRESSÉE", 540, 960, 70, ORG, glow=0.6)

def sc_ej_wind(c, t, sg, lt, u):
    sky(c, (0.15, 0.30, 0.65), (0.55, 0.70, 0.90))
    for k in range(40):
        ph = (lt * 4 + k / 40) % 1; y = 200 + (k * 61) % 1500
        c.move_to(W * (1 - ph) + 300, y); c.line_to(W * (1 - ph) - 100, y); c.set_source_rgba(1, 1, 1, 0.5); c.set_line_width(5); c.stroke()
    rr(c, 420, 760, 200, 300, 30); fill_stroke(c, (0.25, 0.25, 0.3), 8)
    flap = ap(u, 0.55, 0.7) * (0.6 + 0.4 * math.sin(lt * 14))
    limb(c, [(460, 830), (380 - 80 * flap, 880 - 60 * flap)]); limb(c, [(580, 830), (650, 900)])
    R.eyes_head(c, 520, 700, 95, 'worried', (-20, 0), lt)
    text(c, "≈ 39 T / M²", 540, 470, 140, RED, glow=0.9)
    if u > 0.55: text(c, "BRAS COLLÉS AU CORPS", 540, 1300, 70, WH, glow=0.4)

def sc_ej_chute(c, t, sg, lt, u):
    sky(c, (0.35, 0.55, 0.85), (0.85, 0.85, 0.80))
    o = ap(u, 0.2, 0.45)
    cy = 900 + 20 * math.sin(lt * 1.2)
    if o > 0:
        c.save(); c.translate(540, cy - 420); c.scale(o, o)
        c.new_path(); c.arc(0, 0, 300, math.pi, 2 * math.pi); c.close_path(); fill_stroke(c, ORG, 8)
        for k in range(5): c.move_to(-300 + k * 150, 0); c.line_to(0, 400)
        c.set_source_rgb(*INK); c.set_line_width(3); c.stroke(); c.restore()
    pilot_body(c, 540, cy, 1.0)
    R.eyes_head(c, 540, cy - 80, 95, 'neutral' if o > 0.5 else 'worried', (0, -10), lt)
    if u > 0.6: text(c, "< 3 SECONDES", 540, 1300, 130, GRN, glow=0.8)

def sc_ej_verdict(c, t, sg, lt, u):
    sky(c, (0.03, 0.08, 0.06), (0.01, 0.02, 0.02)); radial(c, 540, 1000, 700, GRN, 0.15)
    pilot_body(c, 540, 1180, 1.35)
    limb(c, [(480, 1220), (380, 1120), (360, 1020)]); limb(c, [(600, 1220), (700, 1120), (720, 1020)])
    R.eyes_head(c, 540, 1060, 140, 'determined', (0, -10), lt, rim=GRN)
    s = 1 + 0.15 * max(0, 1 - lt / 0.3)
    c.save(); c.translate(540, 480); c.rotate(-0.06); c.scale(s, s)
    rr(c, -380, -110, 760, 200, 30); c.set_source_rgba(*GRN, 0.15); c.fill_preserve(); c.set_source_rgb(*GRN); c.set_line_width(8); c.stroke()
    text(c, "TU SURVIS", 0, 50, 160, GRN, glow=1.0); c.restore()
    if u > 0.3: text(c, "+ 9 PILOTES SUR 10 SAUVÉS", 540, 700, 64, WH)
    if u > 0.6: text(c, "MAIS BLESSURES FRÉQUENTES", 540, 1420, 60, ORG)

# ---------- United 232 ----------
def dc10(c, x, y, rot=0, s=1.0, tail_dead=False):
    jet(c, x, y, rot, s)
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rr(c, -235, -100, 80, 30, 14); fill_stroke(c, (0.3, 0.3, 0.32) if tail_dead else (0.75, 0.76, 0.8), 6)
    c.restore()

def throttles(c, x, y, l, r, glow=1.0):
    rr(c, x - 200, y, 400, 300, 30); fill_stroke(c, (0.12, 0.13, 0.17), 9)
    for k, v in enumerate((l, r)):
        xx = x - 90 + k * 180; yy = y + 240 - 180 * v
        c.move_to(xx, y + 250); c.line_to(xx, yy); c.set_source_rgb(0.6, 0.62, 0.68); c.set_line_width(14); c.stroke()
        rr(c, xx - 50, yy - 30, 100, 50, 16); fill_stroke(c, ORG if k == 0 else BLUE, 6)
        radial(c, xx, yy, 120, ORG if k == 0 else BLUE, 0.25 * glow)

def sc_h2_hook(c, t, sg, lt, u):
    sky(c, (0.03, 0.04, 0.08), (0.01, 0.01, 0.02))
    throttles(c, 540, 750, 0.5 + 0.3 * math.sin(lt * 1.5), 0.5 - 0.3 * math.sin(lt * 1.5))
    if u > 0.3:
        for k, w in enumerate(("MANCHE", "GOUVERNES")):
            text(c, w, 300 + k * 480, 1250, 70, (0.5, 0.5, 0.55)); c.move_to(160 + k * 480, 1225); c.line_to(440 + k * 480, 1225); c.set_source_rgb(*RED); c.set_line_width(8); c.stroke()
    if u > 0.7: text(c, "1989", 540, 560, 160, ORG, glow=0.8)

def sc_h2_burst(c, t, sg, lt, u):
    sky(c, (0.20, 0.40, 0.75), (0.65, 0.78, 0.92))
    b = u > 0.35
    dc10(c, 540, 760, 0.02, 1.4, tail_dead=b)
    if b:
        fl = max(0, 1 - (u - 0.35) / 0.06); c.set_source_rgba(1, 1, 1, 0.8 * fl); c.paint()
        R.flames(c, 540 - 270, 760 - 150, 0.9, lt, 1 - ap(u, 0.6, 1) * 0.6)
        for j in range(14):
            r = random.Random(j); a = r.random() * 6.28; d = 400 * ap(u, 0.35, 0.6) * (0.4 + r.random())
            c.save(); c.translate(270 + math.cos(a) * d, 610 + math.sin(a) * d); c.rotate(lt * 6 + j); rr(c, -14, -8, 28, 16, 3); c.set_source_rgb(0.3, 0.3, 0.32); c.fill(); c.restore()
    if u > 0.6:
        for k in range(3):
            y = 1200 + k * 110; rr(c, 200, y, 680, 80, 20); c.set_source_rgba(*RED, 0.2); c.fill_preserve(); c.set_source_rgb(*RED); c.set_line_width(4); c.stroke()
            text(c, f"HYDRAULIQUE {k + 1} : 0", 540, y + 60, 54, RED)

def sc_h2_noctl(c, t, sg, lt, u):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, 0.3, 0.5, 0.8); g.add_color_stop_rgb(1, 0.6, 0.75, 0.9); c.set_source(g); c.paint()
    c.save(); c.translate(540, 700); c.rotate(0.35 * ap(u, 0, 0.6) + 0.04 * math.sin(lt * 2))
    c.rectangle(-1400, 300, 2800, 1400); c.set_source_rgb(0.3, 0.45, 0.25); c.fill(); c.restore()
    c.new_path(); c.move_to(0, 1050); c.curve_to(380, 1000, 700, 1000, W, 1050); c.line_to(W, H); c.line_to(0, H); c.close_path(); fill_stroke(c, (0.10, 0.11, 0.14), 10)
    c.new_path(); c.arc(540, 1250, 110, math.pi * 1.1, math.pi * 1.9); c.set_source_rgb(*INK); c.set_line_width(26); c.stroke()
    c.move_to(540, 1250); c.line_to(540, 1450); c.stroke()
    text(c, "COMMANDES : 0", 540, 1380, 80, RED, glow=0.6)
    if u > 0.55: text(c, "296 À BORD", 540, 470, 130, WH, glow=0.4)

def sc_h2_fitch(c, t, sg, lt, u):
    sky(c, (0.12, 0.12, 0.16), (0.06, 0.06, 0.08))
    c.new_path(); c.move_to(0, 400); c.line_to(W, 400); c.line_to(W, 1500); c.line_to(0, 1500); c.close_path(); c.set_source_rgb(0.18, 0.18, 0.24); c.fill()
    for k in range(4): rr(c, 60 + k * 270, 950, 200, 330, 40); fill_stroke(c, (0.28, 0.3, 0.42), 7)
    w = ap(u, 0.3, 0.9); x = 300 + 450 * w; y = 1000 - 120 * ap(u, 0.1, 0.3)
    civ_body(c, x, y + 90, 1.1, (0.85, 0.85, 0.88))
    blinkh(c, x, y, 105, 'determined', (20, 0), lt, False)
    if u > 0.2: text(c, "DENNY FITCH", 540, 560, 110, ORG, glow=0.7)
    if u > 0.45: text(c, "INSTRUCTEUR DC-10", 540, 670, 54, WH)

def sc_h2_thr(c, t, sg, lt, u):
    sky(c, (0.20, 0.40, 0.75), (0.65, 0.78, 0.92))
    ph = math.sin(lt * 1.6)
    dc10(c, 540, 600, 0.25 * ph, 0.9, tail_dead=True)
    throttles(c, 540, 1080, 0.5 + 0.35 * ph, 0.5 - 0.35 * ph)
    text(c, "VIRAGE À DROITE" if ph > 0 else "VIRAGE À GAUCHE", 540, 990, 76, ORG if ph > 0 else BLUE)

def sc_h2_land(c, t, sg, lt, u):
    sky(c, (0.40, 0.60, 0.88), (0.85, 0.85, 0.80))
    c.new_path(); c.move_to(0, 1100); c.line_to(W, 1100); c.line_to(W, H); c.line_to(0, H); c.close_path(); c.set_source_rgb(0.4, 0.55, 0.3); c.fill()
    c.new_path(); c.move_to(420, 1100); c.line_to(660, 1100); c.line_to(1000, H); c.line_to(80, H); c.close_path(); fill_stroke(c, (0.25, 0.26, 0.3), 6)
    k = ap(u, 0.0, 0.4)
    if u < 0.45: dc10(c, 540, 600 + 500 * k, 0.15 * k, 0.6 + 0.8 * k, tail_dead=True)
    else:
        radial(c, 540, 1300, 500, (1, 0.5, 0.1), 0.6); R.flames(c, 540, 1350, 2.0, lt, 0.9)
        for j in range(8): c.new_path(); c.arc(400 + j * 40, 1100 - ((lt * 80 + j * 50) % 500), 40 + j * 4, 0, 7); c.set_source_rgba(0.2, 0.2, 0.22, 0.4); c.fill()
    if u > 0.75:
        rr(c, 140, 300, 800, 200, 34); c.set_source_rgba(0, 0, 0, 0.55); c.fill(); text(c, "+ 180 SURVIVANTS", 540, 440, 110, GRN, glow=0.8)

def sc_h2_end(c, t, sg, lt, u):
    sky(c, (0.04, 0.05, 0.10), (0.01, 0.01, 0.03)); radial(c, 540, 1000, 700, ORG, 0.15)
    for k, x in enumerate((300, 540, 780)):
        pilot_body(c, x, 1180, 1.0); R.eyes_head(c, x, 1090, 100, 'determined', (0, -10), lt + k, rim=ORG)
    text(c, "UN ÉQUIPAGE", 540, 560, 150, ORG, glow=1.0)
    text(c, "44 MINUTES SANS COMMANDES", 540, 680, 56, WH)

SC4 = {k[3:]: v for k, v in globals().items() if k.startswith('sc_') and callable(v)}
