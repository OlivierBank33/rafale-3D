"""Scènes 25/10 : train d'atterrissage, F-15 une aile, Gimli. R = module sm_render injecté."""
import cairo, math, random
from sm_lib import *
from sm_scenes2 import ease, ap, blinkh, civ_body, sky, jet, ORG, BLUE, RED, WH, GRN
from sm_scenes4 import fighter
R = None

def wheelwell(c, lt, fold=0.0, cold=0.0, dark=0.0):
    c.set_source_rgb(0.10 - 0.05 * cold, 0.10 - 0.03 * cold, 0.13 + 0.05 * cold); c.paint()
    for k in range(8):  # tuyaux/câbles
        c.move_to(0, 300 + k * 140); c.curve_to(300, 260 + k * 140, 700, 340 + k * 140, W, 300 + k * 140)
        c.set_source_rgb(0.25, 0.26, 0.3); c.set_line_width(14); c.stroke()
    # roue qui remonte
    y = 1900 - 650 * fold
    c.new_path(); c.arc(700, y, 230, 0, 7); fill_stroke(c, (0.08, 0.08, 0.09), 12)
    c.new_path(); c.arc(700, y, 110, 0, 7); fill_stroke(c, (0.55, 0.57, 0.62), 8)
    if cold > 0:
        r = random.Random(3)
        for _ in range(60):
            x = r.random() * W; yy = r.random() * H; c.new_path(); c.arc(x, yy, 3 + 6 * r.random(), 0, 7); c.set_source_rgba(0.8, 0.9, 1, 0.5 * cold); c.fill()
    if dark > 0: c.set_source_rgba(0, 0, 0, dark); c.paint()

def stow(c, x, y, lt, mood='worried', cold=0.0, s=1.0):
    col = (0.25 + 0.3 * cold, 0.45 + 0.3 * cold, 0.75 + 0.2 * cold)
    rr(c, x - 70 * s, y + 60 * s, 140 * s, 150 * s, 50 * s); fill_stroke(c, col, 9)
    limb(c, [(x - 50 * s, y + 90 * s), (x - 10 * s, y + 150 * s)]); limb(c, [(x + 50 * s, y + 90 * s), (x + 10 * s, y + 150 * s)])
    blinkh(c, x, y, 95 * s, mood, (0, 6), lt, False, rim=BLUE if cold > 0.3 else None)

def sc_tw_hide(c, t, sg, lt, u):
    sky(c, (0.35, 0.5, 0.75), (0.75, 0.75, 0.7))
    c.new_path(); c.rectangle(0, 1350, W, H); c.set_source_rgb(0.3, 0.3, 0.33); c.fill()
    k = ap(u, 0.35, 0.9)
    jet(c, 540 + 200 * k, 1150 - 500 * k, -0.18 * k, 1.6)
    if u < 0.35: stow(c, 380, 1180, lt, 'worried', 0, 0.6)
    if u > 0.4: text(c, "DÉCOLLAGE", 540, 520, 120, WH, glow=0.3)

def sc_tw_gear(c, t, sg, lt, u):
    f = ap(u, 0.25, 0.75)
    wheelwell(c, lt, fold=f)
    stow(c, 330, 850, lt, 'worried')
    if f > 0.5: radial(c, 520, 1200, 400, RED, 0.25 * (0.5 + 0.5 * math.sin(lt * 8)))
    text(c, "LE TRAIN REMONTE", 540, 420, 110, RED if f > 0.5 else WH, glow=0.6)

def sc_tw_cold(c, t, sg, lt, u):
    cold = ap(u, 0.1, 0.9)
    wheelwell(c, lt, fold=1, cold=cold)
    stow(c, 330, 850, lt, 'worried', cold)
    temp = int(15 - 65 * cold)
    rr(c, 230, 360, 620, 200, 30); c.set_source_rgba(0, 0, 0, 0.6); c.fill()
    text(c, f"{temp} °C".replace('-', '−'), 540, 510, 150, BLUE if temp < 0 else ORG, glow=0.8)

def sc_tw_oxy(c, t, sg, lt, u):
    wheelwell(c, lt, fold=1, cold=1, dark=0.0)
    k = ap(u, 0.15, 0.6)
    c.save(); c.translate(330, 950); c.rotate(0.5 * k); c.translate(-330, -950); stow(c, 330, 850, lt, 'neutral' if k > 0.5 else 'worried', 1); c.restore()
    if k > 0.5:
        for sx in (-1, 1):
            x0 = 330 + sx * 31; c.move_to(x0 - 14, 850); c.line_to(x0 + 14, 850); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    g = cairo.RadialGradient(W / 2, H * 0.45, W * (0.7 - 0.5 * k), W / 2, H * 0.45, W * 1.0); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.9 * k); c.set_source(g); c.paint()
    text(c, "PLUS D'OXYGÈNE", 540, 430, 120, RED, glow=0.8)

def sc_tw_fall(c, t, sg, lt, u):
    sky(c, (0.4, 0.55, 0.8), (0.8, 0.82, 0.8))
    jet(c, 540, 420, 0.04, 1.4)
    k = ap(u, 0.35, 0.6)
    c.save(); c.translate(560, 470); c.rotate(-0.8 * k); rr(c, -10, 0, 160, 24, 8); fill_stroke(c, (0.6, 0.62, 0.68), 6); c.restore()
    if k > 0.6:
        c.new_path(); c.arc(540, 700, 40, 0, 7); fill_stroke(c, (0.98, 0.98, 0.99), 6)
        c.move_to(540, 760); c.line_to(540, 1300); c.set_source_rgba(1, 1, 1, 0.5); c.set_dash([20, 20]); c.set_line_width(5); c.stroke(); c.set_dash([])
        text(c, "?", 540, 1450, 200, RED, glow=0.8)

def sc_tw_verdict(c, t, sg, lt, u):
    sky(c, (0.08, 0.02, 0.03), (0.02, 0.01, 0.01)); radial(c, 540, 1000, 600, RED, 0.12)
    for i in range(4):
        x = 270 + i * 180; dead = i < 3
        c.new_path(); c.arc(x, 1050, 70, 0, 7); fill_stroke(c, (0.35, 0.35, 0.4) if dead else (0.98, 0.98, 0.99), 7)
        if dead:
            for sx in (-1, 1):
                ex = x + sx * 22; c.move_to(ex - 10, 1040); c.line_to(ex + 10, 1060); c.move_to(ex + 10, 1040); c.line_to(ex - 10, 1060)
            c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    text(c, "PLUS DE 3 SUR 4", 540, 1300, 100, RED, glow=0.8)
    s = 1 + 0.15 * max(0, 1 - lt / 0.3)
    c.save(); c.translate(540, 500); c.rotate(-0.05); c.scale(s, s)
    rr(c, -460, -110, 920, 200, 30); c.set_source_rgba(*RED, 0.15); c.fill_preserve(); c.set_source_rgb(*RED); c.set_line_width(8); c.stroke()
    text(c, "TU NE SURVIS PAS", 0, 50, 130, RED, glow=1.0); c.restore()
    if u > 0.5: text(c, "NE LE TENTE JAMAIS", 540, 760, 70, WH)

# ---------- F-15 ----------
def f15(c, x, y, s=1.0, rot=0.0, wing=True, leak=0.0, lt=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.new_path(); c.move_to(0, -320); c.line_to(40, -200); c.line_to(55, 260); c.line_to(-55, 260); c.line_to(-40, -200); c.close_path(); fill_stroke(c, (0.55, 0.6, 0.66), 8)
    c.new_path(); c.move_to(-50, -40); c.line_to(-300, 120); c.line_to(-300, 170); c.line_to(-50, 140); c.close_path(); fill_stroke(c, (0.5, 0.55, 0.6), 7)
    if wing:
        c.new_path(); c.move_to(50, -40); c.line_to(300, 120); c.line_to(300, 170); c.line_to(50, 140); c.close_path(); fill_stroke(c, (0.5, 0.55, 0.6), 7)
    else:
        c.new_path(); c.move_to(50, -40); c.line_to(90, -10); c.line_to(80, 130); c.line_to(50, 140); c.close_path(); fill_stroke(c, (0.5, 0.55, 0.6), 7)
    for sx in (-1, 1):
        c.new_path(); c.move_to(sx * 45, 200); c.line_to(sx * 160, 290); c.line_to(sx * 160, 320); c.line_to(sx * 45, 300); c.close_path(); fill_stroke(c, (0.5, 0.55, 0.6), 6)
        c.new_path(); c.move_to(sx * 35, 150); c.line_to(sx * 50, 40); c.line_to(sx * 60, 40); c.line_to(sx * 55, 170); c.close_path(); fill_stroke(c, (0.45, 0.5, 0.55), 5)
    c.new_path(); c.save(); c.scale(1, 2.2); c.arc(0, -100, 22, 0, 7); c.restore(); fill_stroke(c, (0.35, 0.75, 1.0), 5)
    if leak > 0:
        r = random.Random(2)
        for k in range(30):
            ph = (lt * 1.5 + k / 30) % 1; c.new_path(); c.arc(80 + 40 * r.random() + ph * 60, 60 + ph * 600, 16 + ph * 40, 0, 7); c.set_source_rgba(0.85, 0.9, 1, 0.5 * leak * (1 - ph)); c.fill()
    c.restore()

def desert(c, lt):
    sky(c, (0.35, 0.6, 0.9), (0.95, 0.85, 0.65))
    c.new_path(); c.move_to(0, 1300); c.curve_to(300, 1250, 700, 1320, W, 1260); c.line_to(W, H); c.line_to(0, H); c.close_path(); c.set_source_rgb(0.85, 0.7, 0.45); c.fill()

def sc_f_hook(c, t, sg, lt, u):
    desert(c, lt)
    f15(c, 540, 800, 1.2, 0.05 * math.sin(lt), wing=u < 0.5, leak=1.0 if u >= 0.5 else 0, lt=lt)
    if u > 0.5: text(c, "1 AILE", 540, 1240, 160, RED, glow=1.0)

def sc_f_train(c, t, sg, lt, u):
    desert(c, lt)
    f15(c, 400 + 60 * math.sin(lt * 0.7), 750, 0.8, 0.3 + 0.1 * math.sin(lt))
    fighter(c, 800, 500 + 40 * math.sin(lt * 0.9), 0.55, 2.7)
    text(c, "F-15  VS  A-4", 540, 1240, 100, WH, glow=0.4)

def sc_f_crash(c, t, sg, lt, u):
    desert(c, lt)
    hit = u > 0.25
    spin = 4 * ap(u, 0.5, 1.0) * lt if u > 0.5 else 0
    f15(c, 540, 800, 1.1, 0.4 * math.sin(spin) if hit else 0, wing=not hit, leak=1.0 if hit else 0, lt=lt)
    if not hit: fighter(c, 1000 - 900 * ap(u, 0, 0.25), 700, 0.55, 3.14)
    else:
        fl = max(0, 1 - (u - 0.25) / 0.06); c.set_source_rgba(1, 1, 1, 0.8 * fl); c.paint()
        for j in range(14):
            r = random.Random(j); a = r.random() * 6.28; d = 500 * ap(u, 0.25, 0.5) * (0.4 + r.random())
            c.save(); c.translate(760 + math.cos(a) * d, 760 + math.sin(a) * d); c.rotate(lt * 6 + j); rr(c, -18, -10, 36, 20, 3); c.set_source_rgb(0.4, 0.42, 0.45); c.fill(); c.restore()
        text(c, "COLLISION", 540, 1240, 130, RED, glow=1.0)

def sc_f_recover(c, t, sg, lt, u):
    desert(c, lt)
    f15(c, 540, 800, 1.1, 0.25 * (1 - ap(u, 0, 0.4)) * math.sin(lt * 3), wing=False, leak=1.0, lt=lt)
    for sx in (-1, 1): radial(c, 540 + sx * 50, 1120, 90, (1, 0.6, 0.2), 0.9)
    if u > 0.2: text(c, "POST-COMBUSTION", 540, 1240, 100, ORG, glow=0.8)

def sc_f_land(c, t, sg, lt, u):
    sky(c, (0.35, 0.6, 0.9), (0.95, 0.85, 0.65))
    c.new_path(); c.move_to(420, 900); c.line_to(660, 900); c.line_to(1000, H); c.line_to(80, H); c.close_path(); fill_stroke(c, (0.3, 0.3, 0.33), 6)
    k = ap(u, 0.0, 0.5)
    f15(c, 540, 300 + 900 * k, 0.4 + 0.5 * k, 0, wing=False, leak=0.5, lt=lt)
    rr(c, 300, 960, 480, 30, 10); fill_stroke(c, ORG, 5)
    text(c, "480 KM/H", 540, 520, 150, RED, glow=0.9)
    if u > 0.7: text(c, "6 M DE LA BARRIÈRE", 540, 680, 66, WH)

def sc_f_reveal(c, t, sg, lt, u):
    desert(c, lt)
    f15(c, 540, 820, 1.25, 0, wing=False)
    for k, x in enumerate((510, 570)):
        c.new_path(); c.arc(x, 820 - 230 + k * 60, 26, 0, 7); fill_stroke(c, (0.98, 0.98, 0.99), 5)
    if u > 0.3:
        rr(c, 640, 720, 220, 200, 20); c.set_source_rgba(1, 0.2, 0.2, 0.15 + 0.1 * math.sin(lt * 5)); c.fill()
        text(c, "!", 760, 870, 160, RED, glow=1.0)
    if u > 0.55: text(c, "PLUS D'AILE DROITE", 540, 1240, 90, RED, glow=0.8)

def sc_f_end(c, t, sg, lt, u):
    desert(c, lt)
    f15(c, 540, 820, 1.25, 0, wing=True)
    text(c, "NOUVELLE AILE", 540, 420, 130, GRN, glow=0.9)
    text(c, "ET RETOUR EN SERVICE", 540, 520, 60, WH)

# ---------- Gimli ----------
def b767(c, x, y, rot=0, s=1.0):
    jet(c, x, y, rot, s)

def sc_g_hook(c, t, sg, lt, u):
    sky(c, (0.15, 0.35, 0.75), (0.65, 0.78, 0.92))
    b767(c, 540, 750, 0.03 * math.sin(lt), 1.3)
    stage = 0 if u < 0.35 else (1 if u < 0.65 else 2)
    labels = ["FUEL LOW", "MOTEUR GAUCHE : OFF", "MOTEUR DROIT : OFF"]
    on = (lt * 2.5) % 1 < 0.55
    rr(c, 160, 1150, 760, 130, 20); fill_stroke(c, RED if on else (0.35, 0.1, 0.1), 7)
    text(c, labels[stage], 540, 1240, 70, WH)
    if u > 0.2: text(c, "12 000 M", 540, 480, 130, WH, glow=0.4)

def sc_g_fuel(c, t, sg, lt, u):
    c.set_source_rgb(0.04, 0.04, 0.07); c.paint()
    for k, (lab, col, x) in enumerate((("LIVRES", ORG, 300), ("KILOS", BLUE, 780))):
        rr(c, x - 200, 600, 400, 300, 40); c.set_source_rgba(*col, 0.12); c.fill_preserve(); c.set_source_rgb(*col); c.set_line_width(6); c.stroke()
        text(c, lab, x, 790, 110, col, glow=0.6)
    text(c, "≠", 540, 800, 200, RED, glow=1.0)
    lvl = 1 - 0.55 * ap(u, 0.3, 0.6)
    rr(c, 140, 1060, 800, 100, 40); c.set_source_rgba(1, 1, 1, 0.08); c.fill_preserve(); c.set_source_rgba(1, 1, 1, 0.6); c.set_line_width(5); c.stroke()
    rr(c, 154, 1074, 772 * lvl, 72, 30); c.set_source_rgb(*(RED if lvl < 0.6 else GRN)); c.fill()
    if u > 0.6: text(c, "MOINS DE LA MOITIÉ", 540, 1300, 80, RED, glow=0.6)

def sc_g_map(c, t, sg, lt, u):
    c.set_source_rgb(0.15, 0.25, 0.15); c.paint()
    c.new_path(); c.move_to(600, 0); c.curve_to(700, 500, 650, 900, 760, 1400); c.line_to(W, 1400); c.line_to(W, 0); c.close_path(); c.set_source_rgb(0.15, 0.3, 0.55); c.fill()
    px, py = 300, 400
    c.save(); c.translate(px, py); c.rotate(1.2); c.new_path(); c.move_to(40, 0); c.line_to(-30, -26); c.line_to(-15, 0); c.line_to(-30, 26); c.close_path(); fill_stroke(c, WH, 5); c.restore()
    c.new_path(); c.arc(380, 1200, 50, 0, 7); fill_stroke(c, RED, 6); text(c, "WINNIPEG", 380, 1310, 54, WH)
    c.move_to(px, py); c.line_to(380, 1150); c.set_source_rgba(*RED, 0.8); c.set_dash([20, 14]); c.set_line_width(6); c.stroke(); c.set_dash([])
    if u > 0.3:
        c.new_path(); c.arc(560, 760, 50, 0, 7); fill_stroke(c, ORG, 6); text(c, "GIMLI", 560, 870, 60, ORG, glow=0.6)
        c.move_to(px, py); c.line_to(560, 710); c.set_source_rgba(*ORG, 0.9); c.set_dash([20, 14]); c.set_line_width(6); c.stroke(); c.set_dash([])
    if u > 0.65:
        for k in range(5): rr(c, 470 + k * 40, 940 + (k % 2) * 30, 30, 18, 6); fill_stroke(c, (RED, BLUE, ORG, GRN, WH)[k], 3)
        text(c, "COURSE AUTO", 560, 1060, 50, WH)

def sc_g_options(c, t, sg, lt, u):
    c.set_source_rgb(0.03, 0.04, 0.07); c.paint()
    for k, (lab, name, col, a0) in enumerate((("A", "WINNIPEG", BLUE, 0.1), ("B", "GIMLI", ORG, 0.38), ("C", "UN CHAMP", GRN, 0.65))):
        a = ap(u, a0, a0 + 0.1)
        if a <= 0: continue
        y = 520 + k * 330
        rr(c, 90, y, 900, 260, 40); c.set_source_rgba(*col, 0.1 * a); c.fill_preserve(); c.set_source_rgba(*col, 0.85 * a); c.set_line_width(5); c.stroke()
        text(c, lab, 220, y + 190, 200, col, glow=a); text(c, name, 620, y + 165, 100, WH)

def sc_g_pause(c, t, sg, lt, u):
    c.set_source_rgb(0.03, 0.04, 0.07); c.paint()
    if len(sg.get('sent', [])) >= 5:                      # v2 : calé sur « Trois. Deux. Un. » de la vraie voix
        marks = [x[0] for x in sg['sent'][2:5]]
        k = sum(1 for m in marks if t >= m - 0.05)
        if k == 0:
            text(c, "?", 540, 1020, 360, WH, glow=0.6); since = lt
        else:
            n = 4 - k; since = t - marks[k - 1]
            s = 1 + 0.35 * (1 - ease(since / 0.25))
            c.save(); c.translate(540, 900); c.scale(s, s); text(c, str(n), 0, 120, 360, (RED, ORG, ORG)[n - 1] if n <= 3 else ORG, glow=1.2); c.restore()
            c.new_path(); c.arc(540, 860, 260 + 120 * ease(since / 0.4), 0, 7); c.set_source_rgba(*ORG, 0.5 * (1 - ease(since / 0.4))); c.set_line_width(10); c.stroke()
    else:
        n = 3 - int(min(2.999, lt * 3 / max(1, sg['end'] - sg['t0'])))
        s = 1 + 0.2 * (1 - (lt % 1))
        c.save(); c.translate(540, 900); c.scale(s, s); text(c, str(n), 0, 120, 360, ORG, glow=1.2); c.restore()
    text(c, "A, B OU C ?", 540, 520, 130, WH, glow=0.6)

def sc_g_reveal(c, t, sg, lt, u):
    sky(c, (0.4, 0.6, 0.88), (0.85, 0.85, 0.8))
    c.new_path(); c.rectangle(0, 1100, W, H); c.set_source_rgb(0.4, 0.55, 0.3); c.fill()
    c.new_path(); c.move_to(420, 1100); c.line_to(660, 1100); c.line_to(1000, H); c.line_to(80, H); c.close_path(); fill_stroke(c, (0.3, 0.3, 0.33), 6)
    for k in range(6): rr(c, 470 + k * 25, 1110, 18, 12, 4); fill_stroke(c, (RED, BLUE, ORG, GRN, WH, RED)[k], 2)
    k = ap(u, 0.0, 0.6)
    slip = 0.35 * math.sin(math.pi * ap(u, 0.1, 0.45))
    b767(c, 540, 450 + 800 * k, slip, 0.6 + 0.9 * k)
    if k >= 1:
        for j in range(12):
            r = random.Random(j); c.new_path(); c.arc(540 + (r.random() - 0.5) * 300, 1450 + (r.random() - 0.5) * 60, 6, 0, 7); c.set_source_rgba(1, 0.8, 0.3, 0.9 * ((lt * 3 + j) % 1)); c.fill()
    if 0.1 < u < 0.5: text(c, "GLISSADE", 540, 400, 110, ORG, glow=0.7)

def sc_g_end(c, t, sg, lt, u):
    sky(c, (0.03, 0.08, 0.06), (0.01, 0.02, 0.02)); radial(c, 540, 1000, 700, GRN, 0.15)
    pilot_body(c, 540, 1180, 1.35)
    limb(c, [(480, 1220), (380, 1120), (360, 1020)]); limb(c, [(600, 1220), (700, 1120), (720, 1020)])
    R.eyes_head(c, 540, 1060, 140, 'determined', (0, -10), lt, rim=GRN)
    text(c, "69 SURVIVANTS", 540, 520, 150, GRN, glow=1.0)
    text(c, "ET TOI : A, B OU C ?", 540, 660, 64, WH)

SC5 = {k[3:]: v for k, v in globals().items() if k.startswith('sc_') and callable(v)}
