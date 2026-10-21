"""Histoire interactive STICKMAN « TU ES LE PILOTE ». Usage : DL=dl/<slug> python3 sm_render.py [stills t1 ...]
cfg.py : SERIES, EP, SCENES[type, title, say, show], END_HOLD ; durs.json (même timeline que ns_render -> el_sync ns: ou sm:)."""
import cairo, json, math, os, re, subprocess, sys, random, importlib.util
from sm_lib import *
FPS = 30
D = os.environ.get('DL', 'dl/sm_ep01').rstrip('/') + '/'
spec = importlib.util.spec_from_file_location('cfg', D + 'cfg.py'); CFG = importlib.util.module_from_spec(spec); spec.loader.exec_module(CFG)
SCENES = CFG.SCENES; DUR = json.load(open(D + 'durs.json'))
SEG = []; t = 0.0
for i, s in enumerate(SCENES):
    pre = 0.2 if i == 0 else 0.3
    post = 0.35 if i < len(SCENES) - 1 else getattr(CFG, 'END_HOLD', 2.0)
    SEG.append(dict(i=i, k=f's{i}', scene=s['type'], t0=t, vt=t + pre, dur=DUR[f's{i}'], end=t + pre + DUR[f's{i}'] + post, score=(0, 0), p=s))
    t = SEG[-1]['end']
TOTAL = t
json.dump(dict(seg=[{k: v for k, v in x.items() if k != 'p'} for x in SEG], total=TOTAL), open(D + 'timeline.json', 'w'))
ORG = (1.0, 0.55, 0.12); BLUE = (0.35, 0.82, 1.0); RED = (1.0, 0.25, 0.25); WH = (1, 1, 1)


def ease(u): u = min(max(u, 0), 1); return u * u * (3 - 2 * u)
def ap(u, a, b): return ease((u - a) / max(1e-3, b - a))
def blink(t, ph=0.0): return ((t + ph) % 3.7) < 0.12


def eyes_head(c, x, y, r, mood, look, t, rim=None, helmet=True):
    head(c, x, y, r, mood, look, helmet, rim)
    if blink(t, x * 0.001):   # paupières
        for sx in (-1, 1):
            ex, ey = x + sx * r * 0.33 + look[0], y + r * 0.02 + look[1]
            c.new_path(); c.arc(ex, ey, r * 0.15, 0, 7); c.set_source_rgb(0.98, 0.98, 0.99); c.fill()
            c.move_to(ex - r * 0.12, ey); c.line_to(ex + r * 0.12, ey); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()


def sky(c, top, bot):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *top); g.add_color_stop_rgb(1, *bot); c.set_source(g); c.paint()


def rain(c, t, x0, y0, x1, y1, n=110, a=0.18, seed=3):
    r = random.Random(seed)
    for _ in range(n):
        x = x0 + r.random() * (x1 - x0); sp = 900 + 500 * r.random(); L = 50 + r.random() * 70
        y = y0 + ((r.random() * (y1 - y0) + t * sp) % (y1 - y0))
        c.move_to(x, y); c.line_to(x - 12, y + L); c.set_source_rgba(0.6, 0.7, 0.9, a); c.set_line_width(2); c.stroke()


def flames(c, x, y, s, t, a=1.0):
    if a <= 0: return
    radial(c, x, y, 160 * s, (1, 0.45, 0.1), 0.6 * a)
    for k, (col, sc) in enumerate((((1, 0.35, 0.05), 1.0), ((1, 0.65, 0.1), 0.7), ((1, 0.95, 0.6), 0.4))):
        c.new_path(); h = 90 * s * sc * (1 + 0.15 * math.sin(t * 17 + k)); w = 34 * s * sc
        c.move_to(x - w, y); c.curve_to(x - w, y - h * 0.5, x - w * 0.2, y - h * 0.6, x + w * 0.1 * math.sin(t * 11), y - h)
        c.curve_to(x + w * 0.4, y - h * 0.6, x + w, y - h * 0.5, x + w, y); c.close_path()
        c.set_source_rgba(*col, a); c.fill()


# ---------------- scènes ----------------
def sc_cockpit(c, t, sg, lt, u):
    sky(c, (0.03, 0.04, 0.08), (0.01, 0.01, 0.02))
    c.save(); c.new_path(); c.move_to(80, 420); c.line_to(1000, 420); c.line_to(1060, 1000); c.line_to(20, 1000); c.close_path(); c.clip()
    sky(c, (0.07, 0.09, 0.17), (0.12, 0.13, 0.22))
    rain(c, lt, 0, 420, W, 1000)
    fl = max(0, 1 - abs(lt - 1.3) / 0.15) + max(0, 1 - abs(lt - 4.6) / 0.12)
    if fl > 0:
        c.set_source_rgba(0.75, 0.82, 1, 0.5 * fl); c.paint()
        pts = [(720, 420), (690, 560), (735, 575), (680, 760), (760, 600), (715, 590), (750, 420)]
        c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]; c.close_path(); c.set_source_rgba(0.95, 0.97, 1, fl); c.fill()
    for (cx, cy, cr) in ((150, 520, 160), (380, 480, 130), (920, 510, 170), (560, 450, 110)):
        c.new_path(); c.arc(cx + 20 * math.sin(lt * 0.3 + cx), cy, cr, 0, 7); c.set_source_rgba(0.05, 0.06, 0.11, 0.9); c.fill()
    c.restore()
    c.new_path(); c.move_to(530, 420); c.line_to(550, 420); c.line_to(560, 1000); c.line_to(520, 1000); c.close_path(); fill_stroke(c, (0.09, 0.10, 0.13), 8)
    c.new_path(); c.move_to(80, 420); c.line_to(1000, 420); c.line_to(1060, 1000); c.line_to(20, 1000); c.close_path(); c.set_source_rgb(*INK); c.set_line_width(14); c.stroke()
    c.new_path(); c.move_to(0, 960); c.curve_to(300, 920, 780, 920, W, 960); c.line_to(W, H); c.line_to(0, H); c.close_path(); fill_stroke(c, (0.10, 0.11, 0.14), 10)
    for i, (x, y) in enumerate(((200, 1080), (370, 1070), (710, 1070), (880, 1080))):
        c.new_path(); c.arc(x, y, 72, 0, 7); fill_stroke(c, (0.02, 0.03, 0.05), 8)
        c.new_path(); c.arc(x, y, 58, math.pi * 0.8, math.pi * 2.2); c.set_source_rgba(0.3, 1, 0.8, 0.8); c.set_line_width(4); c.stroke()
        a = math.pi * (0.9 + 0.3 * i) + (1.2 if i == 2 else 0) + 0.06 * math.sin(lt * 7 + i)
        if i == 1: a -= 0.25 * ap(u, 0.6, 1)   # couple moteur gauche qui chute
        c.move_to(x, y); c.line_to(x + math.cos(a) * 50, y + math.sin(a) * 50); c.set_source_rgb(1, 0.95, 0.8); c.set_line_width(5); c.stroke()
    on = (lt * 2.5) % 1 < 0.55 and u > 0.6
    if on: radial(c, 540, 1060, 560, (1, 0.1, 0.12), 0.5)
    rr(c, 440, 1020, 200, 80, 14); fill_stroke(c, RED if on else (0.35, 0.1, 0.1), 7)
    text(c, "ENG FIRE", 540, 1078, 52, (1, 0.95, 0.95) if on else (0.6, 0.4, 0.4))
    by = 3 * math.sin(lt * 2)
    pilot_body(c, 330, 1300 + by, 1.25)
    limb(c, [(300, 1340 + by), (390, 1250), (470, 1180)]); limb(c, [(360, 1340 + by), (460, 1290), (520, 1200)])
    look = (28, -6) if u < 0.6 else (40, 8)
    eyes_head(c, 330, 1210 + by, 120, 'worried' if u > 0.6 else 'neutral', look, lt, rim=(1, 0.2, 0.2) if on else (0.6, 0.7, 1))
    if on: c.set_source_rgba(1, 0.1, 0.1, 0.07); c.paint()


def sc_handle(c, t, sg, lt, u):
    sky(c, (0.02, 0.03, 0.06), (0.01, 0.01, 0.02))
    # hublot latéral : aile + moteur
    c.save(); c.translate(W / 2, 640)
    rr(c, -400, -300, 800, 560, 120); c.set_source_rgb(0.05, 0.07, 0.14); c.fill()
    c.save(); rr(c, -400, -300, 800, 560, 120); c.clip()
    rain(c, lt, -400, -300, 400, 260, 60, 0.15)
    c.new_path(); c.move_to(-400, 40); c.line_to(400, -20); c.line_to(400, 60); c.line_to(-400, 140); c.close_path(); fill_stroke(c, (0.75, 0.77, 0.82), 8)
    rr(c, -110, -20, 220, 110, 50); fill_stroke(c, (0.6, 0.62, 0.68), 8)
    fire = 1 - ap(u, 0.62, 0.8)
    feath = ap(u, 0.2, 0.3)
    ang = lt * 40 * (1 - feath) + feath * 0.0
    for k in range(3):
        a = ang + k * 2.094
        c.save(); c.translate(-125, 35); c.scale(0.25 + 0.75 * abs(math.cos(a)), 1)
        rr(c, -10, -120, 20, 120, 8); fill_stroke(c, (0.15, 0.15, 0.18), 5); c.restore()
    flames(c, 30, -20, 1.2, lt, fire)
    ext = ap(u, 0.5, 0.62) * (1 - ap(u, 0.85, 1))
    if ext > 0:
        r = random.Random(4)
        for _ in range(60):
            ph = (lt * 1.5 + r.random()) % 1; x = 30 + r.uniform(-90, 90) * ph; y = -20 - ph * 150
            c.new_path(); c.arc(x, y, 10 + 25 * ph, 0, 7); c.set_source_rgba(0.95, 0.97, 1, 0.5 * ext * (1 - ph)); c.fill()
    c.restore()
    rr(c, -400, -300, 800, 560, 120); c.set_source_rgb(*INK); c.set_line_width(26); c.stroke()
    rr(c, -430, -330, 860, 620, 140); c.set_source_rgb(0.2, 0.22, 0.27); c.set_line_width(30); c.stroke()
    c.restore()
    # premier plan : main qui tire la poignée feu
    pull = ap(u, 0.32, 0.42) * 70
    rr(c, 340, 1150, 400, 300, 30); fill_stroke(c, (0.12, 0.13, 0.17), 9)
    text(c, "FIRE", 540, 1215, 44, (1, 0.6, 0.6))
    c.new_path(); c.rectangle(525, 1250, 30, 120 - pull * 0.2); fill_stroke(c, (0.5, 0.5, 0.55), 6)
    rr(c, 430, 1225 + 120 - pull, 220, 60, 22); fill_stroke(c, RED, 8)
    hy = 1225 + 120 - pull + 30
    limb(c, [(800, 1700), (700, 1520), (590, hy)], w=34)
    c.new_path(); c.arc(590, hy, 46, 0, 7); fill_stroke(c, (0.97, 0.97, 0.98), 9)
    if u > 0.85:
        text(c, "FEU ÉTEINT", W / 2, 1060, 90, (0.4, 1, 0.6), glow=0.8)


PL = None
def plane(c, x, y, rot, lt, dead_prop=True, smoke=0.0, s=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    for k in range(14):
        if smoke <= 0: break
        xx = -60 - k * 34; yy = 40 + k * 4 + 6 * math.sin(lt * 2 + k)
        c.new_path(); c.arc(xx, yy, 14 + k * 5, 0, 7); c.set_source_rgba(0.3, 0.3, 0.35, smoke * (0.5 - k * 0.03)); c.fill()
    c.new_path(); c.move_to(-230, -10); c.curve_to(-120, -38, 150, -40, 230, -14); c.curve_to(260, -4, 262, 22, 232, 30); c.curve_to(100, 44, -120, 40, -230, 22); c.close_path(); fill_stroke(c, (0.92, 0.93, 0.96), 9)
    c.new_path(); c.move_to(-200, -12); c.line_to(-250, -110); c.line_to(-205, -110); c.line_to(-150, -20); c.close_path(); fill_stroke(c, (0.85, 0.2, 0.2), 8)
    for i in range(7): rr(c, -110 + i * 42, -18, 24, 18, 6); fill_stroke(c, (1, 0.85, 0.45), 4)
    c.new_path(); c.move_to(170, -28); c.curve_to(195, -34, 220, -26, 232, -12); c.line_to(185, -12); c.close_path(); fill_stroke(c, (0.35, 0.75, 1.0), 5)
    c.new_path(); c.move_to(-40, 14); c.line_to(80, 14); c.line_to(-10, 70); c.line_to(-90, 70); c.close_path(); fill_stroke(c, (0.8, 0.81, 0.86), 8)
    rr(c, -40, 30, 110, 34, 16); fill_stroke(c, (0.6, 0.62, 0.68), 7)
    # hélice : moteur droit tourne (disque flou), moteur gauche arrêté
    c.new_path(); c.save(); c.translate(76, 47); c.scale(0.25, 1); c.arc(0, 0, 70, 0, 7); c.restore(); c.set_source_rgba(0.8, 0.85, 0.95, 0.25 + 0.1 * math.sin(lt * 40)); c.fill()
    if dead_prop:
        c.move_to(76, -10); c.line_to(76, 100); c.set_source_rgb(*INK); c.set_line_width(9); c.stroke()
    c.restore()


def ocean_bg(c, lt, horizon=1060):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, 0.02, 0.03, 0.08); g.add_color_stop_rgb(horizon / H - 0.001, 0.08, 0.10, 0.22)
    g.add_color_stop_rgb(horizon / H, 0.03, 0.05, 0.10); g.add_color_stop_rgb(1, 0.01, 0.02, 0.04); c.set_source(g); c.paint()
    r = random.Random(5)
    for _ in range(240):
        c.new_path(); c.arc(r.random() * W, r.random() * (horizon - 60), r.choice((1, 1, 1.5, 2.4)), 0, 7); c.set_source_rgba(1, 1, 1, (0.3 + 0.6 * r.random()) * (0.75 + 0.25 * math.sin(lt * 2 + r.random() * 9))); c.fill()
    radial(c, 820, 330, 300, (1, 0.95, 0.8), 0.22); c.new_path(); c.arc(820, 330, 80, 0, 7); c.set_source_rgb(0.98, 0.96, 0.88); c.fill()
    c.new_path(); c.arc(856, 312, 72, 0, 7); c.set_source_rgb(0.03, 0.04, 0.09); c.fill()
    for k in range(18):
        y = horizon + 20 + k * 38; w = 170 - k * 7
        rr(c, 820 - w / 2 + 25 * math.sin(lt * 1.5 + k), y, max(10, w), 6, 3); c.set_source_rgba(1, 0.95, 0.8, max(0, 0.25 - k * 0.012)); c.fill()
    for k in range(40):
        y = horizon + 10 + r.random() * (H - horizon); x = (r.random() * W - lt * 40 * (1 + y / H)) % W
        c.move_to(x, y); c.line_to(x + 40 + r.random() * 80, y); c.set_source_rgba(0.5, 0.6, 0.8, 0.12); c.set_line_width(3); c.stroke()


def sc_ocean(c, t, sg, lt, u):
    ocean_bg(c, lt)
    plane(c, 540 + 30 * math.sin(lt * 0.5), 700 + 60 * u + 8 * math.sin(lt * 1.3), -0.03 + 0.04 * u, lt, True, 0.6 * (1 - u))
    alt = int(3200 - 700 * ap(u, 0.2, 1))
    rr(c, 230, 1250, 620, 200, 30); c.set_source_rgba(0, 0, 0, 0.5); c.fill()
    text(c, f"{alt:,} M".replace(',', '\u00a0'), 540, 1370, 130, ORG, glow=0.6)
    text(c, "ALTITUDE  ▼", 540, 1425, 34, (0.75, 0.8, 0.9), 'Montserrat')


def sc_map(c, t, sg, lt, u):
    sky(c, (0.03, 0.05, 0.10), (0.02, 0.03, 0.06))
    for k in range(30):  # quadrillage
        c.move_to(k * 40, 0); c.line_to(k * 40, H); c.move_to(0, k * 70); c.line_to(W, k * 70)
    c.set_source_rgba(0.3, 0.5, 0.8, 0.06); c.set_line_width(2); c.stroke()
    # Irlande stylisée
    c.save(); c.translate(860, 560); c.scale(1.5, 1.5)
    c.new_path(); pts = [(0, -120), (60, -100), (80, -40), (70, 30), (90, 90), (30, 130), (-40, 110), (-80, 60), (-60, 0), (-90, -50), (-40, -100)]
    c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]; c.close_path(); fill_stroke(c, (0.25, 0.55, 0.35), 6); c.restore()
    text(c, "IRLANDE", 860, 830, 52, WH)
    px, py = 250, 700
    d = ap(u, 0.08, 0.35)
    for k in range(int(26 * d)):
        x = px + (780 - px) * k / 26; y = py + (590 - py) * k / 26
        c.new_path(); c.arc(x, y, 6, 0, 7); c.set_source_rgba(*BLUE, 0.9); c.fill()
    text(c, "200 KM", 515, 610, 90, BLUE, glow=0.7 * d) if d > 0.9 else None
    c.save(); c.translate(px, py); c.rotate(math.pi); c.new_path(); c.move_to(40, 0); c.line_to(-30, -28); c.line_to(-15, 0); c.line_to(-30, 28); c.close_path(); fill_stroke(c, (1, 1, 1), 5); c.restore()
    radial(c, px, py, 90 + 20 * math.sin(lt * 4), RED, 0.3)
    # jauge carburant
    f = ap(u, 0.4, 0.55); lvl = 0.5 - 0.06 * ap(u, 0.55, 1)
    if f > 0:
        rr(c, 140, 1060, 800, 110, 40); c.set_source_rgba(1, 1, 1, 0.08 * f); c.fill_preserve(); c.set_source_rgba(1, 1, 1, 0.6 * f); c.set_line_width(5); c.stroke()
        rr(c, 155, 1075, max(40, 770 * lvl), 80, 32); c.set_source_rgba(*ORG, f); c.fill()
        text(c, "CARBURANT", 540, 1230, 40, (0.8, 0.85, 0.95), 'Montserrat')
        text(c, "≈ 50 MIN", 540, 1360, 140, ORG, glow=0.8)
    if u > 0.8 and (lt * 3) % 1 < 0.6:
        text(c, "TRÈS JUSTE", 540, 1500, 80, RED, glow=1.0)


def sc_radio(c, t, sg, lt, u):
    ocean_bg(c, lt, horizon=900)
    # cargo à l'horizon avec feux + projecteur
    sx = 540
    c.new_path(); c.move_to(sx - 200, 880); c.line_to(sx + 220, 880); c.line_to(sx + 180, 930); c.line_to(sx - 170, 930); c.close_path(); fill_stroke(c, (0.12, 0.14, 0.2), 6)
    rr(c, sx + 80, 820, 80, 60, 8); fill_stroke(c, (0.15, 0.17, 0.24), 6)
    for k in range(6): c.new_path(); c.arc(sx - 150 + k * 50, 890, 5, 0, 7); c.set_source_rgb(1, 0.85, 0.4); c.fill()
    sp = ap(u, 0.3, 0.45)
    if sp > 0:
        a = -1.3 + 0.35 * math.sin(lt * 0.8)
        c.new_path(); c.move_to(sx + 120, 830); c.line_to(sx + 120 + math.cos(a - 0.08) * 900, 830 + math.sin(a - 0.08) * 900); c.line_to(sx + 120 + math.cos(a + 0.08) * 900, 830 + math.sin(a + 0.08) * 900); c.close_path()
        c.set_source_rgba(1, 0.95, 0.7, 0.12 * sp); c.fill()
    # gros plan pilote casque micro, ondes radio
    c.new_path(); c.rectangle(0, 1080, W, H - 1080); c.set_source_rgba(0.02, 0.02, 0.04, 0.85); c.fill()
    pilot_body(c, 300, 1480, 1.3)
    eyes_head(c, 300, 1370, 130, 'worried' if u < 0.5 else 'determined', (20, -8), lt, rim=(0.5, 0.7, 1))
    for k in range(3):
        ph = (lt * 1.2 + k / 3) % 1
        c.new_path(); c.arc(430, 1430, 40 + ph * 220, -0.6, 0.6); c.set_source_rgba(*BLUE, 0.8 * (1 - ph)); c.set_line_width(6); c.stroke()
    bub = ap(u, 0.02, 0.1)
    rr(c, 560, 1180, 450, 130, 30); fill_stroke(c, (0.97, 0.97, 0.98), 7, bub)
    text(c, "MAYDAY MAYDAY", 785, 1268, 64, (0.85, 0.15, 0.15) if bub > 0.5 else (0, 0, 0))
    if u > 0.3:
        text(c, "CARGO · 15 KM", sx, 790, 60, (1, 0.9, 0.5), glow=0.6)


def sc_choice(c, t, sg, lt, u):
    c.set_source_rgb(0.02, 0.02, 0.04); c.paint()
    for side, (col, lab, sub, l1, l2) in enumerate(((BLUE, "A", "DEMI-TOUR", "1 moteur, 200 km, 50 min", "risque : panne sèche"),
                                                   (ORG, "B", "SE POSER EN MER", "de nuit, près du cargo", "risque : couler"))):
        a = ap(u, 0.12 + side * 0.12, 0.25 + side * 0.12); y0 = 520 + side * 620; dx = (1 - a) * (300 if side == 0 else -300)
        c.save(); c.translate(dx, 0)
        hl = 0.5 + 0.5 * math.sin(lt * 3 + side * 3.14) if u > 0.6 else 0.5
        rr(c, 70, y0, 940, 560, 40); c.set_source_rgba(*col, 0.08 * a); c.fill_preserve(); c.set_source_rgba(*col, 0.85 * a); c.set_line_width(5); c.stroke()
        c.save(); rr(c, 70, y0, 940, 560, 40); c.clip(); radial(c, 300, y0 + 280, 500, col, (0.12 + 0.15 * hl) * a); c.restore()
        if a > 0.05:
            text(c, lab, 200, y0 + 340, 300, col, glow=a)
            text(c, sub, 640, y0 + 250, 92, WH)
            text(c, l1, 640, y0 + 320, 36, (0.75, 0.8, 0.9), 'Montserrat'); text(c, l2, 640, y0 + 380, 36, col, 'Montserrat')
        c.restore()
    c.new_path(); c.arc(W / 2, 1080, 120, 0, 7); c.set_source_rgb(0.02, 0.02, 0.04); c.fill()
    lx = 0 if u < 0.3 else (-22 if (lt % 2.4) < 1.2 else 22)
    eyes_head(c, W / 2, 1080, 95, 'worried', (lx * 0.5, -14 if lx <= 0 else 14), lt)
    text(c, "TU FAIS QUOI ?", W / 2, 330, 140, WH, glow=0.5 * ap(u, 0, 0.1))
    b = ap(u, 0.6, 0.7)
    if b > 0:
        text(c, "ÉCRIS A OU B EN COMMENTAIRE", W / 2, 1790, 46, (0.9, 0.92, 1.0), 'Montserrat')
        text(c, "LA MAJORITÉ DÉCIDE DE L'ÉPISODE 2", W / 2, 1855, 36, ORG, 'Montserrat')



def bubble(c, x, y, r, a):
    c.new_path(); c.arc(x, y, r, 0, 7); fill_stroke(c, (0.97, 0.97, 0.98), 8, a)


def sc_think(c, t, sg, lt, u):
    sky(c, (0.04, 0.05, 0.10), (0.01, 0.01, 0.03))
    left = u < 0.47
    for side, (cx, col) in enumerate(((290, BLUE), (790, ORG))):
        act = (side == 0 and left) or (side == 1 and not left)
        a = ap(u, 0.03 + side * 0.44, 0.12 + side * 0.44)
        if a <= 0: continue
        dim = 1.0 if act else 0.45
        for k, (bx, by, br) in enumerate(((W / 2 + (cx - W / 2) * 0.3, 1060, 18), (W / 2 + (cx - W / 2) * 0.55, 950, 30))): bubble(c, bx, by, br, a * dim)
        c.save(); rr(c, cx - 240, 470, 480, 400, 60); fill_stroke(c, (0.97, 0.97, 0.98), 9, a * dim); rr(c, cx - 240, 470, 480, 400, 60); c.clip()
        if side == 0:
            c.set_source_rgba(0.06, 0.08, 0.16, a * dim); c.paint()
            rr(c, cx - 180, 560, 360, 60, 26); c.set_source_rgba(1, 1, 1, 0.2 * a); c.fill()
            lvl = 0.5 - 0.35 * ap(u, 0.15, 0.4) if act else 0.15
            rr(c, cx - 172, 568, max(30, 344 * lvl), 44, 20); c.set_source_rgba(*(RED if lvl < 0.25 else ORG), a * dim); c.fill()
            text(c, "CARBURANT", cx, 680, 44, (0.9, 0.92, 1), 'Montserrat')
            text(c, "200 KM", cx, 810, 110, BLUE, glow=0.6 * dim)
        else:
            c.set_source_rgba(0.04, 0.06, 0.12, a * dim); c.paint()
            for k in range(4):
                c.new_path(); y = 700 + k * 40
                for xx in range(cx - 240, cx + 260, 20): c.line_to(xx, y + 18 * math.sin(xx / 30 + lt * 3 + k))
                c.set_source_rgba(0.4, 0.6, 1, 0.6 * a * dim); c.set_line_width(5); c.stroke()
            c.new_path(); c.move_to(cx - 120, 640); c.line_to(cx + 130, 640); c.line_to(cx + 100, 680); c.line_to(cx - 100, 680); c.close_path(); fill_stroke(c, (0.15, 0.17, 0.24), 6, a * dim)
            text(c, "VAGUES 2 M", cx, 580, 70, ORG, glow=0.6 * dim)
        c.restore()
    by = 4 * math.sin(lt * 2)
    pilot_body(c, W / 2, 1300 + by, 1.3)
    limb(c, [(W / 2 + 60, 1340), (W / 2 + 150, 1270), (W / 2 + 80, 1220)])
    eyes_head(c, W / 2, 1180 + by, 140, 'worried', (-30 if left else 30, -20), lt, rim=BLUE if left else ORG)


SC = dict(cockpit=sc_cockpit, handle=sc_handle, ocean=sc_ocean, map=sc_map, radio=sc_radio, think=sc_think, choice=sc_choice)
from sm_scenes2 import SC2
SC.update(SC2)


# ---------------- sous-titres ----------------
def chunks(show, n=3):
    show = re.sub(r' ([?!:;»])', '\u00a0\\1', show); show = re.sub(r'(\d) (\d{3})', '\\1\u00a0\\2', show)
    w = [x for x in show.split(' ') if x]; out = []; cur = []
    for x in w:
        cur.append(x)
        if len(cur) >= n or x.endswith(('.', '?', '!', ',', ':')): out.append(cur); cur = []
    if cur: out.append(cur)
    return out


CHK = []
for sg in SEG:
    if sg['scene'] == 'choice': continue          # écran de choix déjà très textuel
    cs = chunks(sg['p']['show']); allw = [w for ch in cs for w in ch]
    wt = [len(w) + 2 + (6 if w.endswith(('.', '?', '!')) else 3 if w.endswith((',', ':')) else 0) for w in allw]
    tot = sum(wt); acc = 0; k = 0
    for ch in cs:
        ws = []
        for w in ch:
            a = sg['vt'] + sg['dur'] * acc / tot; acc += wt[k]; k += 1
            ws.append((a, sg['vt'] + sg['dur'] * acc / tot, w))
        CHK.append(ws)


def subtitles(c, t):
    cur = [ch for ch in CHK if ch[0][0] <= t < ch[-1][1] + 0.08]
    if not cur: return
    ch = cur[-1]; size = 84; F(c, size, 'Montserrat'); words = [w.upper() for _, _, w in ch]; sp = size * 0.45
    ws = [c.text_extents(w).x_advance for w in words]; tw = sum(ws) + sp * (len(ws) - 1)
    if tw > 980: size = int(size * 980 / tw); F(c, size, 'Montserrat'); ws = [c.text_extents(w).x_advance for w in words]; tw = sum(ws) + sp * (len(ws) - 1)
    x = W / 2 - tw / 2; y = 1640
    for i, w in enumerate(words):
        a0, a1, _ = ch[i]; act = a0 <= t < a1 or (i == len(ch) - 1 and t >= a0)
        c.move_to(x, y); c.text_path(w); c.set_source_rgba(0, 0, 0, 1); c.set_line_width(14); c.set_line_join(1); c.stroke()
        c.move_to(x, y); c.text_path(w); c.set_source_rgb(*(ORG if act else WH)); c.fill(); x += ws[i] + sp


def title_card(c, sg, lt):
    a = ease(lt / 0.4) * (1 - ease((lt - 2.6) / 0.5))
    if a <= 0 or sg['scene'] == 'choice': return
    if getattr(CFG, 'MODE', 'serie') != 'serie' and sg['i'] > 0: return
    if sg['i'] == 0 and getattr(CFG, 'MODE', 'serie') == 'serie':
        text(c, f"ÉPISODE {int(CFG.EP)}", W / 2, 250, 46, (0.85, 0.88, 0.95), 'Montserrat', track=6)
    c.push_group(); text(c, sg['p']['title'], W / 2, 370, 128, RED if sg['i'] == 0 else (0.92, 0.95, 1), glow=1.0); c.pop_group_to_source(); c.paint_with_alpha(a)


def frame(t):
    sg = next((x for x in SEG if x['t0'] <= t < x['end']), SEG[-1]); lt = t - sg['t0']
    u = min(1, max(0, (t - sg['vt']) / max(0.1, sg['dur'] + 0.3)))
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    k = 1 + 0.05 * ease(lt / max(1, sg['end'] - sg['t0']))       # travelling avant lent
    c.save(); c.translate(W / 2, H * 0.45); c.scale(k, k); c.translate(-W / 2, -H * 0.45)
    SC[sg['scene']](c, t, sg, lt, u); c.restore()
    vignette(c, 0.8); grain(c, int(t * 12) % 6, 6000)
    title_card(c, sg, lt); subtitles(c, t)
    if lt < 0.25 and sg['i'] > 0: c.set_source_rgba(0, 0, 0, 1 - lt / 0.25); c.paint()          # fondu au noir
    if sg['end'] - lt < 0.15 and sg['i'] < len(SEG) - 1: c.set_source_rgba(0, 0, 0, 1 - (sg['end'] - t) / 0.15); c.paint()
    c.set_source_rgba(*ORG, 1); c.rectangle(0, H - 8, W * t / TOTAL, 8); c.fill()
    return s


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        for x in sys.argv[2:]: frame(float(x)).write_to_png(D + f'still_{x}.png')
        sys.exit()
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', D + 'video_noaudio.mp4'], stdin=subprocess.PIPE)
    n = int(TOTAL * FPS)
    for i in range(n):
        ff.stdin.write(bytes(frame(i / FPS).get_data()))
        if i % 300 == 0: print(i, '/', n, flush=True)
    ff.stdin.close(); ff.wait(); print('done', TOTAL)
