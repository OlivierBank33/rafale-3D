"""Scènes « SURVIVRAIS-TU ? » (hublot) et « HISTOIRE VRAIE » (BA 5390) pour sm_render."""
import cairo, math, random
from sm_lib import *
ORG = (1.0, 0.55, 0.12); BLUE = (0.35, 0.82, 1.0); RED = (1.0, 0.25, 0.25); WH = (1, 1, 1); GRN = (0.4, 1, 0.6)
def ease(u): u = min(max(u, 0), 1); return u * u * (3 - 2 * u)
def ap(u, a, b): return ease((u - a) / max(1e-3, b - a))
def blinkh(c, x, y, r, mood, look, t, helmet, rim=None):
    head(c, x, y, r, mood, look, helmet, rim)
    if (t + x * 0.001) % 3.7 < 0.12:
        for sx in (-1, 1):
            ex, ey = x + sx * r * 0.33 + look[0], y + r * 0.02 + look[1]
            c.new_path(); c.arc(ex, ey, r * 0.15, 0, 7); c.set_source_rgb(0.98, 0.98, 0.99); c.fill()
            c.move_to(ex - r * 0.12, ey); c.line_to(ex + r * 0.12, ey); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
def civ_body(c, x, y, s=1.0, col=(0.25, 0.45, 0.75)):
    rr(c, x - 60 * s, y, 120 * s, 180 * s, 50 * s); fill_stroke(c, col, 9)
def crew_body(c, x, y, s=1.0):
    rr(c, x - 60 * s, y, 120 * s, 180 * s, 50 * s); fill_stroke(c, (0.12, 0.16, 0.32), 9)
    c.new_path(); c.move_to(x - 25 * s, y + 5); c.line_to(x, y + 45 * s); c.line_to(x + 25 * s, y + 5); fill_stroke(c, (0.95, 0.95, 0.97), 5)
def sky(c, top, bot):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *top); g.add_color_stop_rgb(1, *bot); c.set_source(g); c.paint()
def fog(c, a, t, seed=2):
    if a <= 0: return
    r = random.Random(seed)
    for _ in range(26):
        x = r.random() * W; y = 300 + r.random() * 1300; rad = 120 + r.random() * 200
        radial(c, x + 40 * math.sin(t * 0.7 + x), y + 30 * math.cos(t * 0.5 + y), rad, (0.85, 0.9, 1.0), 0.18 * a)
def debris(c, t, a, x0, y0, seed=5):
    if a <= 0: return
    r = random.Random(seed)
    for _ in range(18):
        ph = (t * (0.6 + r.random()) + r.random()) % 1; x = x0 + (r.random() - 0.5) * 900 * (1 - ph); y = y0 + (r.random() - 0.5) * 600 * (1 - ph)
        x += (x0 - x) * ph; y += (y0 - y) * ph
        c.save(); c.translate(x, y); c.rotate(t * 6 + r.random() * 6); rr(c, -26, -18, 52, 36, 4); fill_stroke(c, (0.95, 0.95, 0.9), 4, a); c.restore()
def window(c, x, y, w, h, broken, t):
    rr(c, x - w / 2, y - h / 2, w, h, w * 0.45); fill_stroke(c, (0.04, 0.06, 0.14) if not broken else (0.01, 0.01, 0.03), 9)
    if not broken:
        c.save(); rr(c, x - w / 2, y - h / 2, w, h, w * 0.45); c.clip()
        for k in range(12): c.new_path(); c.arc(x - w / 2 + (k * 37) % w, y - h / 2 + (k * 53) % h, 2, 0, 7); c.set_source_rgba(1, 1, 1, 0.6); c.fill()
        c.restore()
    else:
        for k in range(7):
            a = k * 0.9; c.move_to(x, y); c.line_to(x + math.cos(a) * w * 0.7, y + math.sin(a) * h * 0.7)
        c.set_source_rgba(0.8, 0.9, 1, 0.8); c.set_line_width(3); c.stroke()
        for k in range(5):
            ph = (t * 1.5 + k / 5) % 1; c.new_path(); c.arc(x, y, 30 + ph * 200, 0, 7); c.set_source_rgba(0.8, 0.9, 1, 0.5 * (1 - ph)); c.set_line_width(4); c.stroke()

# ---------- SURVIVRAIS-TU ? : hublot ----------
def sc_cabin(c, t, sg, lt, u):
    br = u > 0.42
    sky(c, (0.10, 0.11, 0.16), (0.05, 0.05, 0.08))
    c.new_path(); c.move_to(0, 300); c.curve_to(300, 220, 780, 220, W, 300); c.line_to(W, 1500); c.line_to(0, 1500); c.close_path(); c.set_source_rgb(0.16, 0.17, 0.22); c.fill()
    for k in range(3): window(c, 180 + k * 360, 620, 150, 210, br and k == 2, lt)
    for k in range(3):   # sièges
        rr(c, 80 + k * 360, 900, 200, 360, 40); fill_stroke(c, (0.25, 0.28, 0.40), 8)
    shake = 0
    civ_body(c, 540, 1080, 1.2)
    blinkh(c, 540, 990, 115, 'neutral' if not br else 'worried', (0, 0) if not br else (40, -10), lt, False, rim=(0.8, 0.9, 1) if br else None)
    c.new_path(); c.move_to(470, 1160); c.line_to(610, 1160); c.set_source_rgb(0.9, 0.75, 0.2); c.set_line_width(14); c.stroke()  # ceinture
    if br:
        fl = max(0, 1 - (u - 0.42) / 0.06); c.set_source_rgba(1, 1, 1, 0.8 * fl); c.paint()
        fog(c, ap(u, 0.42, 0.6), lt); debris(c, lt, ap(u, 0.45, 0.55), 900, 620)
        text(c, "BANG", 760, 470, 160, RED, glow=fl)
    c.set_source_rgba(0, 0, 0, 0.2); c.paint()

def sc_press(c, t, sg, lt, u):
    sky(c, (0.03, 0.05, 0.10), (0.01, 0.02, 0.04))
    for k, (lab, val, col, y) in enumerate((("CABINE", "2 400 M", BLUE, 560), ("DEHORS", "11 000 M", RED, 1010))):
        a = ap(u, 0.05 + 0.2 * k, 0.15 + 0.2 * k)
        rr(c, 120, y, 840, 330, 40); c.set_source_rgba(*col, 0.08 * a); c.fill_preserve(); c.set_source_rgba(*col, 0.8 * a); c.set_line_width(5); c.stroke()
        text(c, lab, 540, y + 110, 60, WH if a > 0 else (0, 0, 0)); text(c, val, 540, y + 250, 150, col, glow=0.7 * a)
    f = ap(u, 0.45, 0.6)
    if f > 0:
        for k in range(14):
            ph = (lt * 1.2 + k / 14) % 1; x = 260 + (k * 97) % 560
            c.new_path(); c.move_to(x, 900 + ph * 120); c.line_to(x, 940 + ph * 120); c.set_source_rgba(*BLUE, f * (1 - ph)); c.set_line_width(8); c.set_line_cap(1); c.stroke()
        fog(c, ap(u, 0.6, 0.8), lt, 7)
    c.set_source_rgba(0, 0, 0, 0)

def sc_tuc(c, t, sg, lt, u):
    sky(c, (0.04, 0.02, 0.05), (0.01, 0.01, 0.02))
    run = ap(u, 0.35, 1.0); sec = 30 - 30 * run
    R = 300; x, y = 540, 820
    c.new_path(); c.arc(x, y, R, 0, 7); c.set_source_rgba(1, 1, 1, 0.06); c.fill()
    c.new_path(); c.arc(x, y, R, -math.pi / 2, -math.pi / 2 + 2 * math.pi * (sec / 30)); c.set_source_rgb(*(RED if sec < 15 else ORG)); c.set_line_width(26); c.set_line_cap(1); c.stroke()
    text(c, f"{int(math.ceil(sec))} S", x, y + 70, 220, RED if sec < 15 else ORG, glow=1.0)
    text(c, "TEMPS DE CONSCIENCE UTILE", x, y + R + 110, 52, WH)
    if u > 0.65:  # vision qui se rétrécit
        k = ap(u, 0.65, 1.0); g = cairo.RadialGradient(W / 2, H * 0.45, W * (0.6 - 0.35 * k), W / 2, H * 0.45, W * (1.0 - 0.4 * k))
        g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.9 * k); c.set_source(g); c.paint()

def sc_mask(c, t, sg, lt, u):
    sky(c, (0.12, 0.13, 0.18), (0.05, 0.05, 0.08)); fog(c, 0.5, lt, 4)
    drop = ap(u, 0.05, 0.18); my = 300 + 380 * drop + 12 * math.sin(lt * 5) * drop
    rr(c, 300, 260, 480, 50, 10); fill_stroke(c, (0.2, 0.22, 0.28), 6)
    on = ap(u, 0.45, 0.6)
    hx, hy = 540, 1000
    civ_body(c, hx, hy + 90, 1.2)
    mx = 540 + (0 if on < 1 else 0); myy = my + (hy + 40 - my) * on
    c.move_to(540, 310); c.line_to(mx, myy - 40); c.set_source_rgb(0.85, 0.85, 0.9); c.set_line_width(5); c.stroke()
    blinkh(c, hx, hy, 115, 'worried' if on < 1 else 'determined', (0, -20 if on < 0.5 else 0), lt, False)
    c.new_path(); c.save(); c.translate(mx, myy); c.scale(1.2, 1); c.arc(0, 0, 50, 0, 7); c.restore(); fill_stroke(c, (1, 0.85, 0.2), 7)
    if on > 0.5:
        limb(c, [(hx + 60, hy + 130), (hx + 140, hy + 90), (mx + 40, myy + 10)])
    if u > 0.25: text(c, "LE TIEN D'ABORD", 540, 470, 100, ORG, glow=0.8)
    if on >= 1: radial(c, mx, myy, 200, GRN, 0.25); text(c, "≈ 12 MIN D'OXYGÈNE", 540, 1500, 70, GRN, glow=0.6)

def sc_dive(c, t, sg, lt, u):
    sky(c, (0.04, 0.06, 0.14), (0.10, 0.14, 0.26))
    r = random.Random(8)
    for _ in range(30):
        y = (r.random() * H - lt * 600) % H; x = r.random() * W
        c.new_path(); c.arc(x, y, 70 + r.random() * 90, 0, 7); c.set_source_rgba(0.6, 0.7, 0.9, 0.08); c.fill()
    c.save(); c.translate(540, 760); c.rotate(0.45)
    c.new_path(); c.move_to(-260, -14); c.curve_to(-120, -40, 170, -40, 250, -10); c.curve_to(280, 0, 280, 26, 250, 32); c.curve_to(100, 46, -140, 40, -260, 24); c.close_path(); fill_stroke(c, (0.92, 0.93, 0.96), 9)
    c.new_path(); c.move_to(-230, -14); c.line_to(-280, -120); c.line_to(-235, -120); c.line_to(-180, -22); c.close_path(); fill_stroke(c, (0.2, 0.4, 0.8), 8)
    for i in range(9): rr(c, -150 + i * 40, -20, 22, 16, 6); fill_stroke(c, (1, 0.85, 0.45), 4)
    c.restore()
    alt = int(11000 - 8000 * ap(u, 0.1, 0.8))
    rr(c, 190, 1180, 700, 230, 34); c.set_source_rgba(0, 0, 0, 0.5); c.fill()
    text(c, f"{alt:,} M".replace(',', ' '), 540, 1320, 150, ORG if alt > 3500 else GRN, glow=0.6)
    text(c, "DESCENTE D'URGENCE", 540, 1385, 40, (0.8, 0.85, 0.95), 'Montserrat')
    if u > 0.7: text(c, "−50 °C DEHORS", 540, 400, 90, BLUE, glow=0.8)

def sc_verdict(c, t, sg, lt, u):
    sky(c, (0.03, 0.08, 0.06), (0.01, 0.02, 0.02)); radial(c, 540, 900, 700, GRN, 0.18)
    civ_body(c, 540, 1140, 1.3)
    limb(c, [(480, 1180), (400, 1080), (380, 980)]); limb(c, [(600, 1180), (680, 1080), (700, 980)])
    blinkh(c, 540, 1030, 130, 'neutral', (0, -10), lt, False, rim=GRN)
    s = 1 + 0.15 * max(0, 1 - lt / 0.3)
    c.save(); c.translate(540, 480); c.rotate(-0.06); c.scale(s, s)
    rr(c, -380, -110, 760, 200, 30); c.set_source_rgba(*GRN, 0.15); c.fill_preserve(); c.set_source_rgb(*GRN); c.set_line_width(8); c.stroke()
    text(c, "TU SURVIS", 0, 50, 160, GRN, glow=1.0); c.restore()
    if u > 0.3: text(c, "CEINTURE + MASQUE EN 15 S", 540, 690, 64, WH)

# ---------- HISTOIRE VRAIE : BA 5390 ----------
def jet(c, x, y, rot, s=1.0, wind=None):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.new_path(); c.move_to(-250, -12); c.curve_to(-120, -38, 160, -38, 240, -12); c.curve_to(268, 0, 268, 24, 240, 30); c.curve_to(100, 42, -130, 38, -250, 22); c.close_path(); fill_stroke(c, (0.92, 0.93, 0.96), 9)
    c.new_path(); c.move_to(-210, -14); c.line_to(-250, -130); c.line_to(-200, -130); c.line_to(-150, -24); c.close_path(); fill_stroke(c, (0.1, 0.2, 0.5), 8)
    c.new_path(); c.move_to(-235, -128); c.line_to(-170, -128); c.line_to(-175, -116); c.line_to(-232, -116); c.close_path(); fill_stroke(c, (0.1, 0.2, 0.5), 6)
    rr(c, -200, -30, 70, 26, 12); fill_stroke(c, (0.75, 0.76, 0.8), 6)
    for i in range(8): rr(c, -100 + i * 36, -18, 20, 15, 6); fill_stroke(c, (1, 0.85, 0.45), 4)
    c.new_path(); c.move_to(185, -26); c.curve_to(205, -32, 225, -24, 240, -12); c.line_to(195, -12); c.close_path(); fill_stroke(c, (0.02, 0.02, 0.05) if wind else (0.35, 0.75, 1.0), 5)
    c.new_path(); c.move_to(-30, 14); c.line_to(80, 14); c.line_to(0, 66); c.line_to(-80, 66); c.close_path(); fill_stroke(c, (0.8, 0.81, 0.86), 8)
    c.restore()

def sc_climb(c, t, sg, lt, u):
    sky(c, (0.35, 0.55, 0.85), (0.85, 0.80, 0.70))
    r = random.Random(2)
    for _ in range(14):
        x = (r.random() * W * 1.5 - lt * 60 * (0.5 + r.random())) % (W + 400) - 200; y = 900 + r.random() * 700
        for dx, dy, rad in ((0, 0, 70), (60, 10, 55), (-60, 15, 50)):
            c.new_path(); c.arc(x + dx, y + dy, rad, 0, 7); c.set_source_rgba(1, 1, 1, 0.85); c.fill()
    jet(c, 520 + 20 * math.sin(lt * 0.5), 700 - 40 * u, -0.12, 1.2)
    c.set_source_rgba(0.02, 0.02, 0.05, 0.25); c.paint()
    if u > 0.3: text(c, "10 JUIN 1990", 540, 520, 70, WH, glow=0.3)
    if u > 0.55:
        rr(c, 240, 1250, 600, 170, 30); c.set_source_rgba(0, 0, 0, 0.5); c.fill()
        text(c, "87 À BORD", 540, 1370, 110, ORG, glow=0.6)

def screw(c, x, y, w, L, col, a=1):
    rr(c, x - w * 1.8, y, w * 3.6, 30, 8); fill_stroke(c, col, 6, a)
    rr(c, x - w / 2, y + 30, w, L, 4); fill_stroke(c, col, 6, a)
    for k in range(int(L / 18)):
        c.move_to(x - w / 2, y + 40 + k * 18); c.line_to(x + w / 2, y + 48 + k * 18)
    c.set_source_rgba(*INK, a); c.set_line_width(3); c.stroke()

def sc_screws(c, t, sg, lt, u):
    sky(c, (0.04, 0.05, 0.10), (0.01, 0.01, 0.03)); radial(c, 540, 300, 600, (1, 0.9, 0.6), 0.15)
    a = ap(u, 0.05, 0.2)
    rr(c, 140, 300, 800, 420, 50); fill_stroke(c, (0.3, 0.45, 0.6), 10, a)
    for k in range(18):
        ang = k / 18 * 2 * math.pi; x = 540 + math.cos(ang) * 360; y = 510 + math.sin(ang) * 185
        c.new_path(); c.arc(x, y, 9, 0, 7); c.set_source_rgba(*(RED if u > 0.45 else (0.85, 0.85, 0.9)), a); c.fill()
    text(c, "90 VIS", 540, 530, 110, WH if u < 0.45 else RED, glow=0.6)
    b = ap(u, 0.5, 0.65)
    if b > 0:
        screw(c, 360, 900, 64, 360, (0.6, 0.62, 0.68), b); text(c, "BONNE VIS", 360, 1360, 46, GRN)
        screw(c, 720, 900, 52, 360, (0.6, 0.62, 0.68), b); text(c, "84 VIS POSÉES", 720, 1360, 46, RED)
        if u > 0.75: text(c, "−0,66 MM", 540, 1460, 120, ORG, glow=0.8)

def sc_blowout(c, t, sg, lt, u):
    sky(c, (0.30, 0.45, 0.70), (0.70, 0.75, 0.80))
    c.new_path(); c.move_to(0, 0); c.line_to(W, 0); c.line_to(W, 360); c.curve_to(700, 300, 380, 300, 0, 360); c.close_path(); c.set_source_rgb(0.12, 0.13, 0.17); c.fill()
    c.new_path(); c.move_to(0, 1100); c.curve_to(380, 1040, 700, 1040, W, 1100); c.line_to(W, H); c.line_to(0, H); c.close_path(); fill_stroke(c, (0.12, 0.13, 0.17), 10)
    br = u > 0.35
    c.new_path(); c.move_to(160, 380); c.line_to(920, 380); c.line_to(980, 1060); c.line_to(100, 1060); c.close_path()
    if not br: c.set_source_rgba(0.5, 0.75, 1, 0.25); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(16); c.stroke()
    if br:
        fl = max(0, 1 - (u - 0.35) / 0.06); c.set_source_rgba(1, 1, 1, 0.9 * fl); c.paint()
        k = ap(u, 0.35, 0.55)
        c.save(); c.translate(540 + 300 * k, 700 - 700 * k); c.rotate(k * 4); rr(c, -300, -220, 600, 440, 30); c.set_source_rgba(0.5, 0.75, 1, 0.5 * (1 - k)); c.fill(); c.restore()
        debris(c, lt, 1, 540, 400, 3)
        for kk in range(16):
            ph = (lt * 2 + kk / 16) % 1; y = 1000 - ph * 800; x = 200 + (kk * 53) % 700
            c.move_to(x, y); c.line_to(x, y - 90); c.set_source_rgba(1, 1, 1, 0.35 * (1 - ph)); c.set_line_width(4); c.stroke()
        out = ap(u, 0.55, 0.8)
        # commandant aspiré : vu de dos, glisse vers l'ouverture
        cy = 1250 - 600 * out
        rr(c, 470, cy, 140, 230, 60); fill_stroke(c, (0.95, 0.95, 0.97), 9)
        limb(c, [(500, cy + 40), (380, cy - 80)]); limb(c, [(580, cy + 40), (700, cy - 80)])
        c.new_path(); c.arc(540, cy - 20, 90, 0, 7); fill_stroke(c, (0.98, 0.98, 0.99), 9)
    else:
        rr(c, 440, 1150, 200, 230, 60); fill_stroke(c, (0.95, 0.95, 0.97), 9)
        c.new_path(); c.arc(540, 1120, 95, 0, 7); fill_stroke(c, (0.98, 0.98, 0.99), 9)
        c.new_path(); c.move_to(450, 1080); c.line_to(630, 1080); c.set_source_rgb(0.1, 0.1, 0.15); c.set_line_width(20); c.stroke()  # casquette
    if u > 0.25: text(c, "5 300 M", 540, 280, 90, WH, glow=0.4)

def sc_hold(c, t, sg, lt, u):
    sky(c, (0.30, 0.45, 0.70), (0.70, 0.75, 0.80))
    c.new_path(); c.move_to(0, 0); c.line_to(W, 0); c.line_to(W, 360); c.curve_to(700, 300, 380, 300, 0, 360); c.close_path(); c.set_source_rgb(0.12, 0.13, 0.17); c.fill()
    c.new_path(); c.move_to(160, 380); c.line_to(920, 380); c.line_to(980, 1060); c.line_to(100, 1060); c.close_path(); c.set_source_rgb(*INK); c.set_line_width(16); c.stroke()
    for kk in range(22):
        ph = (lt * 2.4 + kk / 22) % 1; y = 1050 - ph * 760; x = 160 + (kk * 41) % 760
        c.move_to(x, y); c.line_to(x + 10, y - 110); c.set_source_rgba(1, 1, 1, 0.4 * (1 - ph)); c.set_line_width(4); c.stroke()
    # jambes du commandant qui partent dans l'ouverture
    w = 6 * math.sin(lt * 9)
    limb(c, [(500, 1150), (480 + w, 900), (470 + w, 560)], w=34, col=(0.12, 0.13, 0.2)); limb(c, [(580, 1150), (600 - w, 900), (610 - w, 560)], w=34, col=(0.12, 0.13, 0.2))
    rr(c, 450, 1120, 180, 70, 20); fill_stroke(c, (0.12, 0.13, 0.2), 8)
    # steward qui tient la ceinture
    crew_body(c, 300, 1330, 1.2)
    limb(c, [(330, 1360), (440, 1250), (480, 1160)]); limb(c, [(270, 1380), (420, 1300), (500, 1190)])
    blinkh(c, 300, 1250, 110, 'determined', (30, -20), lt, False)
    c.new_path(); c.move_to(240, 1170); c.line_to(360, 1170); c.set_source_rgb(0.1, 0.1, 0.15); c.set_line_width(14); c.stroke()
    if u > 0.55:
        crew_body(c, 800, 1360, 1.1); blinkh(c, 800, 1290, 100, 'worried', (-30, -20), lt, False)
        limb(c, [(760, 1400), (650, 1300), (590, 1220)])
        text(c, "ILS SE RELAIENT", 540, 880, 80, ORG, glow=0.6)

def sc_copilot(c, t, sg, lt, u):
    sky(c, (0.30, 0.45, 0.70), (0.55, 0.62, 0.75))
    for kk in range(16):
        ph = (lt * 1.5 + kk / 16) % 1; c.new_path(); c.arc((kk * 97) % W, 200 + ph * 900, 60, 0, 7); c.set_source_rgba(1, 1, 1, 0.12); c.fill()
    c.new_path(); c.move_to(0, 1000); c.curve_to(380, 950, 700, 950, W, 1000); c.line_to(W, H); c.line_to(0, H); c.close_path(); fill_stroke(c, (0.12, 0.13, 0.17), 10)
    pilot_body(c, 680, 1260, 1.25)
    limb(c, [(640, 1300), (560, 1210), (500, 1160)]); limb(c, [(700, 1300), (620, 1230), (540, 1170)])
    c.new_path(); c.move_to(520, 1300); c.line_to(520, 1150); c.set_source_rgb(*INK); c.set_line_width(18); c.stroke()
    blinkh(c, 680, 1160, 120, 'determined', (-30, -10), lt, True)
    mins = int(20 * ap(u, 0.2, 1.0))
    rr(c, 90, 420, 420, 200, 30); c.set_source_rgba(0, 0, 0, 0.55); c.fill()
    text(c, f"{mins:02d}:00", 300, 560, 120, ORG, glow=0.6)
    if u > 0.25:
        rr(c, 560, 420, 430, 120, 30); fill_stroke(c, (0.97, 0.97, 0.98), 7); text(c, "MAYDAY", 775, 505, 70, (0.85, 0.15, 0.15))
    if u > 0.55: text(c, "CAP SOUTHAMPTON", 540, 800, 80, WH, glow=0.4)

def sc_landing(c, t, sg, lt, u):
    sky(c, (0.40, 0.60, 0.88), (0.85, 0.85, 0.80))
    c.new_path(); c.move_to(0, 1100); c.line_to(W, 1100); c.line_to(W, H); c.line_to(0, H); c.close_path(); c.set_source_rgb(0.35, 0.55, 0.35); c.fill()
    c.new_path(); c.move_to(420, 1100); c.line_to(660, 1100); c.line_to(1000, H); c.line_to(80, H); c.close_path(); fill_stroke(c, (0.25, 0.26, 0.3), 6)
    for k in range(8):
        y = 1130 + k * k * 12; c.new_path(); c.rectangle(530, y, 20, 10 + k * 4); c.set_source_rgb(1, 1, 1); c.fill()
    k = ap(u, 0.0, 0.45)
    jet(c, 540, 600 + 520 * k, 0.05 * (1 - k), 0.6 + 0.9 * k, wind=True)
    if u > 0.5:
        rr(c, 190, 300, 700, 200, 34); c.set_source_rgba(0, 0, 0, 0.5); c.fill()
        text(c, "87 SURVIVANTS", 540, 440, 110, GRN, glow=0.8)

def sc_end(c, t, sg, lt, u):
    sky(c, (0.04, 0.05, 0.10), (0.01, 0.01, 0.03)); radial(c, 540, 1000, 700, ORG, 0.15)
    pilot_body(c, 540, 1180, 1.35)
    limb(c, [(480, 1220), (380, 1120), (360, 1020)]); limb(c, [(600, 1220), (700, 1120), (720, 1020)])
    blinkh(c, 540, 1060, 140, 'determined', (0, -10), lt, True, rim=ORG)
    text(c, "< 5 MOIS", 540, 560, 200, ORG, glow=1.0)
    text(c, "ET DE RETOUR AUX COMMANDES", 540, 660, 54, WH)

def sc_hypox(c, t, sg, lt, u):
    sky(c, (0.06, 0.03, 0.10), (0.02, 0.01, 0.04))
    sw = 0.06 * math.sin(lt * 1.7)
    c.save(); c.translate(540, 1000); c.rotate(sw); c.translate(-540, -1000)
    civ_body(c, 540, 1090, 1.3)
    blinkh(c, 540, 970, 135, 'neutral', (10 * math.sin(lt * 1.3), 0), lt, False)
    c.new_path(); c.arc(540, 1020, 50, 0.2, math.pi - 0.2); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
    c.restore()
    for k in range(5):
        a = lt * 1.5 + k * 1.256; x = 540 + math.cos(a) * 200; y = 790 + math.sin(a) * 50
        c.new_path()
        for j in range(10):
            r = 22 if j % 2 == 0 else 9; aa = j * math.pi / 5 - math.pi / 2
            c.line_to(x + math.cos(aa) * r, y + math.sin(aa) * r)
        c.close_path(); fill_stroke(c, (1, 0.9, 0.3), 4)
    if u > 0.2: text(c, "EUPHORIE", 540, 470, 140, (0.85, 0.5, 1.0), glow=0.9)
    if u > 0.75:
        k = ap(u, 0.75, 1.0); g = cairo.RadialGradient(W / 2, H * 0.5, W * (0.6 - 0.4 * k), W / 2, H * 0.5, W * (1.0 - 0.4 * k))
        g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.95 * k); c.set_source(g); c.paint()

SC2 = dict(hypox=sc_hypox, cabin=sc_cabin, press=sc_press, tuc=sc_tuc, mask=sc_mask, dive=sc_dive, verdict=sc_verdict,
           climb=sc_climb, screws=sc_screws, blowout=sc_blowout, hold=sc_hold, copilot=sc_copilot, landing=sc_landing, end=sc_end)
