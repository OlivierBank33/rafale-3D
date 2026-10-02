"""Vidéo duel : Rafale vs F-22 Raptor (rounds, score, radar, HUD)."""
import cairo, json, math, subprocess, sys, re, random
sys.path.insert(0, '/home/claude/pipe')
from duel_script import SCENES

W, H, FPS = 1080, 1920, 30
D = '/home/claude/r3d/duel/'
TM = json.load(open(D + 'timing.json'))
TOTAL = TM['total']
BLU = (0.20, 0.50, 1.0); RED = (1.0, 0.26, 0.22); YEL = (1.0, 0.84, 0.1); WHITE = (1, 1, 1); GRN = (0.35, 1.0, 0.55)
SEG = []
for i, s in enumerate(SCENES):
    t0 = TM['starts'][i] - (0.0 if i == 0 else 0.3)
    end = TM['starts'][i + 1] - 0.3 if i + 1 < len(SCENES) else TOTAL
    SEG.append(dict(i=i, scene=s['scene'], t0=max(0, t0), vt=TM['starts'][i], dur=TM['durs'][i], end=end, score=s['score']))
random.seed(7)


def img(name):
    return cairo.ImageSurface.create_from_png(D + name + '.png')


IM = {k: img(k) for k in ['r_34', 'r_side', 'r_front', 'r_top', 'f_34', 'f_side', 'f_front', 'f_top']}
FLIP = json.load(open(D + 'flip.json'))   # {"f_side": true, ...} pour orienter les nez


def ease(u):
    u = min(max(u, 0), 1); return u * u * (3 - 2 * u)


def ease_out(u):
    u = min(max(u, 0), 1); return 1 - (1 - u) ** 3


def back_out(u):
    u = min(max(u, 0), 1); k = 1.70158
    return 1 + (k + 1) * (u - 1) ** 3 + k * (u - 1) ** 2


def font(c, size, bold=True):
    c.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL); c.set_font_size(size)


def text_c(c, txt, x, y, size, rgba=(1, 1, 1, 1), stroke=0, maxw=None, bold=True):
    font(c, size, bold); e = c.text_extents(txt)
    if maxw and e.x_advance > maxw:
        size *= maxw / e.x_advance; font(c, size, bold); e = c.text_extents(txt)
    c.move_to(x - e.x_advance / 2, y); c.text_path(txt)
    if stroke:
        c.set_source_rgba(0, 0, 0, 0.85 * rgba[3]); c.set_line_width(stroke); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
    c.set_source_rgba(*rgba); c.fill(); c.new_path()


def rrect(c, x, y, w, h, r):
    c.new_path()
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2); c.close_path()


def pill(c, txt, cx, cy, size, bg, fg=(1, 1, 1), s=1.0, alpha=1.0):
    if s <= 0.02 or alpha <= 0.01: return
    c.save(); c.translate(cx, cy); c.scale(s, s)
    font(c, size); e = c.text_extents(txt); bw = e.x_advance + size * 1.3; bh = size * 1.75
    rrect(c, -bw / 2, -bh / 2, bw, bh, bh / 2); c.set_source_rgba(*bg, 0.95 * alpha); c.fill()
    c.set_source_rgba(*fg, alpha); c.move_to(-e.x_advance / 2, size * 0.36); c.show_text(txt); c.restore()


def plane(c, key, cx, cy, size, alpha=1.0, rot=0.0, glow=None):
    """size = largeur affichée du carré de rendu (px)."""
    if alpha <= 0.01: return
    sf = IM[key]; sw = sf.get_width(); s = size / sw
    c.save(); c.translate(cx, cy); c.rotate(rot)
    if FLIP.get(key): c.scale(-1, 1)
    if glow:
        g = cairo.RadialGradient(0, 0, 0, 0, 0, size * 0.45)
        g.add_color_stop_rgba(0, *glow, 0.35 * alpha); g.add_color_stop_rgba(1, *glow, 0)
        c.set_source(g); c.arc(0, 0, size * 0.45, 0, 2 * math.pi); c.fill()
    c.scale(s, s); c.set_source_surface(sf, -sw / 2, -sw / 2); c.paint_with_alpha(alpha); c.restore()


STREAKS = [dict(y=random.uniform(300, 1500), sp=random.uniform(900, 2200), ph=random.uniform(0, 2000), ln=random.uniform(80, 260)) for _ in range(40)]


def background(c, t, tint=None, streak=0.0):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.025, 0.035, 0.07); g.add_color_stop_rgb(0.55, 0.05, 0.07, 0.13); g.add_color_stop_rgb(1, 0.015, 0.02, 0.04)
    c.set_source(g); c.paint()
    if tint:
        for (col, x, y, r, a) in tint:
            rg = cairo.RadialGradient(x, y, 0, x, y, r); rg.add_color_stop_rgba(0, *col, a); rg.add_color_stop_rgba(1, *col, 0)
            c.set_source(rg); c.paint()
    if streak > 0:
        c.set_line_width(3); c.set_line_cap(cairo.LINE_CAP_ROUND)
        for s in STREAKS:
            x = W + 300 - ((t * s['sp'] + s['ph']) % (W + 600))
            c.set_source_rgba(1, 1, 1, 0.10 * streak); c.move_to(x, s['y']); c.line_to(x + s['ln'], s['y']); c.stroke()
    # vignette
    vg = cairo.RadialGradient(W / 2, H / 2, H * 0.3, W / 2, H / 2, H * 0.75)
    vg.add_color_stop_rgba(0, 0, 0, 0, 0); vg.add_color_stop_rgba(1, 0, 0, 0, 0.65)
    c.set_source(vg); c.paint()


# ---------- Score ----------
def score_at(t):
    sc = (0, 0); ch = None
    for s in SEG:
        tc = s['vt'] + s['dur'] * 0.86
        if t >= tc:
            if s['score'] != sc: ch = (tc, sc, s['score'])
            sc = s['score']
    return sc, ch


def scoreboard(c, t, s):
    a = ease((t - 1.6) / 0.5)
    if a <= 0: return
    (r, f), ch = score_at(t)
    c.save(); c.translate(0, -40 * (1 - a))
    y0 = 158; bw = 640; bh = 104; x0 = W / 2 - bw / 2
    rrect(c, x0, y0, bw, bh, 26); c.set_source_rgba(0.04, 0.05, 0.09, 0.88 * a); c.fill_preserve()
    c.set_source_rgba(1, 1, 1, 0.12 * a); c.set_line_width(2); c.stroke()
    rrect(c, x0, y0, 14, bh, 7); c.set_source_rgba(*BLU, a); c.fill()
    rrect(c, x0 + bw - 14, y0, 14, bh, 7); c.set_source_rgba(*RED, a); c.fill()
    text_c(c, "RAFALE", x0 + 135, y0 + 68, 40, (*BLU, a))
    text_c(c, "F-22", x0 + bw - 115, y0 + 68, 40, (*RED, a))
    for val, xx, col, idx in ((r, W / 2 - 52, BLU, 0), (f, W / 2 + 52, RED, 1)):
        pop = 1.0
        if ch and ch[2][idx] != ch[1][idx]:
            pop = 1 + 0.6 * (1 - ease_out((t - ch[0]) / 0.45)) if t - ch[0] < 0.45 else 1
        c.save(); c.translate(xx, y0 + 52); c.scale(pop, pop)
        text_c(c, str(val), 0, 26, 76, (1, 1, 1, a))
        c.restore()
    text_c(c, "–", W / 2, y0 + 72, 50, (1, 1, 1, 0.5 * a))
    # pastilles des rounds
    rnd = {'hook': 0, 'vitesse': 1, 'furtif': 2, 'poly': 3, 'reel': 4, 'duel': 5, 'doute': 5, 'verdict': 5}[s['scene']]
    for k in range(5):
        cx = W / 2 - 80 + k * 40; on = k < rnd
        c.arc(cx, y0 + bh + 26, 9, 0, 2 * math.pi)
        c.set_source_rgba(*(YEL if on else (1, 1, 1)), (1 if on else 0.25) * a); c.fill()
    c.restore()


def round_title(c, t, s, label, sub):
    lt = t - s['t0']
    a = ease(lt / 0.3) * (1 - ease((lt - 2.6) / 0.4))
    if a <= 0.01: return
    sc = back_out(lt / 0.35)
    c.save(); c.translate(W / 2, 395); c.scale(0.7 + 0.3 * sc, 0.7 + 0.3 * sc)
    text_c(c, label, 0, 0, 44, (*YEL, a), stroke=8)
    text_c(c, sub, 0, 72, 74, (1, 1, 1, a), stroke=10, maxw=900)
    c.restore()


# ---------- Scènes ----------
def sc_hook(c, t, s):
    lt = t - s['t0']
    background(c, t, tint=[(BLU, 270, 820, 560, 0.35), (RED, 810, 1120, 560, 0.35)], streak=1.0)
    u = ease_out(lt / 1.1)
    bob = math.sin(t * 2.2) * 8
    plane(c, 'r_34', -380 + u * 720, 820 + bob, 680, glow=BLU)
    plane(c, 'f_34', 1460 - u * 720, 1130 - bob, 680, glow=RED)
    na = ease((lt - 1.0) / 0.4)
    text_c(c, "RAFALE", 300, 600, 64, (*BLU, na), stroke=8)
    text_c(c, "F-22 RAPTOR", 780, 1370, 64, (*RED, na), stroke=8)
    if lt > 1.1:
        v = back_out((lt - 1.1) / 0.35)
        c.save(); c.translate(W / 2, 1000); c.scale(0.4 + 0.6 * v, 0.4 + 0.6 * v); c.rotate(-0.08)
        text_c(c, "VS", 0, 70, 230, (1, 1, 1, 1), stroke=18)
        c.restore()
        fl = 1 - ease((lt - 1.1) / 0.25)
        if fl > 0: c.set_source_rgba(1, 1, 1, 0.8 * fl); c.paint()
    text_c(c, "LE DUEL", W / 2, 400, 52, (*YEL, ease(lt / 0.5)), stroke=8)


def bar(c, x, y, w, h, frac, col, label, val, a):
    rrect(c, x, y, w, h, h / 2); c.set_source_rgba(1, 1, 1, 0.10 * a); c.fill()
    if frac > 0.01:
        rrect(c, x, y, max(h, w * frac), h, h / 2); c.set_source_rgba(*col, a); c.fill()
    text_c(c, val, x + w - 80, y - 22, 54, (1, 1, 1, a), stroke=6)
    text_c(c, label, x + 120, y - 22, 40, (*col, a), stroke=6)


def sc_vitesse(c, t, s):
    lt = t - s['t0']; u = (t - s['vt']) / s['dur']
    background(c, t, tint=[(RED, 700, 1150, 520, 0.25 * ease((u - 0.75) / 0.1))], streak=2.0)
    shake = math.sin(t * 40) * 3
    run = ease(u / 0.85)
    plane(c, 'r_side', 430 + run * 40 + shake, 720, 640, glow=BLU)
    plane(c, 'f_side', 470 + run * 170 - shake, 1110, 640, glow=RED)
    a = ease((lt - 0.6) / 0.4)
    mr = 1.8 * ease((u - 0.45) / 0.3); mf = 2.2 * ease((u - 0.12) / 0.35)
    bar(c, 140, 930, 800, 30, mr / 2.4, BLU, "RAFALE", f"MACH {mr:.1f}".replace('.', ','), a)
    bar(c, 140, 1340, 800, 30, mf / 2.4, RED, "F-22", f"MACH {mf:.1f}".replace('.', ','), a)
    round_title(c, t, s, "ROUND 1", "LA VITESSE")


def sc_furtif(c, t, s):
    lt = t - s['t0']; u = (t - s['vt']) / s['dur']
    background(c, t)
    cx, cy, R = W / 2, 930, 390
    a = ease((lt - 0.2) / 0.5)
    c.set_source_rgba(0.02, 0.10, 0.08, 0.9 * a); c.arc(cx, cy, R, 0, 2 * math.pi); c.fill()
    c.set_line_width(2)
    for rr in (R * 0.33, R * 0.66, R):
        c.set_source_rgba(*GRN, 0.35 * a); c.arc(cx, cy, rr, 0, 2 * math.pi); c.stroke()
    for k in range(12):
        ang = k * math.pi / 6
        c.move_to(cx, cy); c.line_to(cx + R * math.cos(ang), cy + R * math.sin(ang)); c.set_source_rgba(*GRN, 0.12 * a); c.stroke()
    sw = (t * 2.0) % (2 * math.pi)
    for k in range(30):
        ang = sw - k * 0.025
        c.move_to(cx, cy); c.arc(cx, cy, R, ang - 0.025, ang); c.close_path()
        c.set_source_rgba(*GRN, 0.22 * (1 - k / 30) * a); c.fill()
    c.set_line_width(4); c.move_to(cx, cy); c.line_to(cx + R * math.cos(sw), cy + R * math.sin(sw)); c.set_source_rgba(*GRN, 0.9 * a); c.stroke()

    def blip(ang, r, size, col, base):
        d = (sw - ang) % (2 * math.pi)
        fade = max(0, 1 - d / 4.5)
        bx, by = cx + r * math.cos(ang), cy + r * math.sin(ang)
        al = (base + (1 - base) * fade) * a
        g = cairo.RadialGradient(bx, by, 0, bx, by, size * 2.2); g.add_color_stop_rgba(0, *col, al); g.add_color_stop_rgba(1, *col, 0)
        c.set_source(g); c.arc(bx, by, size * 2.2, 0, 2 * math.pi); c.fill()
        c.set_source_rgba(1, 1, 1, al); c.arc(bx, by, size * 0.45, 0, 2 * math.pi); c.fill()
        return bx, by
    rb = blip(math.radians(205), 230, 34, BLU, 0.35)
    fb = blip(math.radians(-35), 270, 7 if u < 0.95 else 7, RED, 0.04 if u > 0.15 else 0.4)
    text_c(c, "RAFALE", rb[0], rb[1] + 90, 40, (*BLU, a), stroke=6)
    la = ease((u - 0.15) / 0.12)
    text_c(c, "F-22 ?", fb[0], fb[1] - 50, 40, (*RED, la * a), stroke=6)
    pill(c, "LA TAILLE D'UNE BILLE", W / 2, 1385, 40, RED, s=back_out((u - 0.2) / 0.12), alpha=a)
    jam = ease((u - 0.5) / 0.1)
    if jam > 0:
        c.set_line_width(5)
        for k in range(4):
            ph = (t * 1.6 + k / 4) % 1
            c.set_source_rgba(*BLU, 0.6 * (1 - ph) * jam); c.arc(rb[0], rb[1], 40 + ph * 180, 0, 2 * math.pi); c.stroke()
        pill(c, "BROUILLAGE SPECTRA", rb[0] + 60, rb[1] - 110, 34, BLU, s=back_out((u - 0.5) / 0.12))
    round_title(c, t, s, "ROUND 2", "LA FURTIVITÉ")


def sc_poly(c, t, s):
    lt = t - s['t0']; u = (t - s['vt']) / s['dur']
    background(c, t, tint=[(BLU, 540, 760, 600, 0.35)])
    plane(c, 'r_34', 560 + math.sin(t) * 8, 720, 760, glow=BLU)
    chips = ["COMBAT AÉRIEN", "FRAPPE AU SOL", "NUCLÉAIRE", "PORTE-AVIONS"]
    pos = [(300, 1010), (780, 1010), (300, 1110), (780, 1110)]
    for k, (txt, (x, y)) in enumerate(zip(chips, pos)):
        pill(c, txt, x, y, 36, BLU, s=back_out((u - 0.2 - k * 0.08) / 0.1))
    fa = ease((u - 0.62) / 0.12)
    plane(c, 'f_34', 330, 1290, 330, alpha=fa, glow=RED)
    pill(c, "CHASSE", 680, 1290, 40, RED, s=back_out((u - 0.66) / 0.1))
    round_title(c, t, s, "ROUND 3", "LA POLYVALENCE")


def balloon(c, x, y, r, a):
    c.set_source_rgba(0.92, 0.92, 0.95, a); c.arc(x, y, r, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(0.75, 0.75, 0.8, a); c.set_line_width(3)
    c.move_to(x - r * 0.6, y + r * 0.8); c.line_to(x - 12, y + r + 50); c.move_to(x + r * 0.6, y + r * 0.8); c.line_to(x + 12, y + r + 50); c.stroke()
    c.rectangle(x - 22, y + r + 50, 44, 24); c.set_source_rgba(0.85, 0.85, 0.9, a); c.fill()


def sc_reel(c, t, s):
    lt = t - s['t0']; u = (t - s['vt']) / s['dur']
    background(c, t, tint=[(BLU, 280, 900, 500, 0.25), (RED, 800, 900, 500, 0.25)])
    a = ease((lt - 0.2) / 0.4)
    plane(c, 'r_top', 280, 640, 380, alpha=a, rot=-math.pi / 2)
    plane(c, 'f_top', 800, 640, 380, alpha=a, rot=math.pi)
    text_c(c, "RAFALE", 280, 860, 50, (*BLU, a), stroke=6)
    text_c(c, "F-22", 800, 860, 50, (*RED, a), stroke=6)
    c.set_source_rgba(1, 1, 1, 0.15 * a); c.rectangle(W / 2 - 1, 560, 2, 820); c.fill()
    for k, txt in enumerate(["AFGHANISTAN", "LIBYE", "MALI", "SYRIE"]):
        pill(c, txt, 280, 960 + k * 100, 38, BLU, s=back_out((u - 0.12 - k * 0.06) / 0.08))
    pill(c, "SYRIE", 800, 960, 38, RED, s=back_out((u - 0.5) / 0.08))
    ba = ease((u - 0.62) / 0.1)
    if ba > 0:
        balloon(c, 800, 1090 - 10 * math.sin(t * 2), 46, ba)
        pill(c, "BALLON CHINOIS", 800, 1250, 34, RED, s=back_out((u - 0.66) / 0.08))
    round_title(c, t, s, "ROUND 4", "LE COMBAT RÉEL")


def hud(c, t, lock, grey=0.0):
    # ciel du HUD
    g = cairo.LinearGradient(0, 320, 0, 1450)
    g.add_color_stop_rgb(0, 0.10, 0.16, 0.26); g.add_color_stop_rgb(1, 0.30, 0.36, 0.44)
    c.set_source(g); c.rectangle(0, 320, W, 1130); c.fill()
    # cible : F-22 vu de face, petit, qui dérive
    fx = 560 + 70 * math.sin(t * 0.7) * (1 - lock); fy = 860 + 40 * math.sin(t * 1.1) * (1 - lock)
    plane(c, 'f_front', fx, fy, 260)
    col = (*GRN, 0.95)
    c.set_line_width(4); c.set_source_rgba(*col)
    # échelle de tangage
    for k in range(-3, 4):
        y = 880 + k * 150 + 20 * math.sin(t * 0.5)
        if k == 0: continue
        c.move_to(250, y); c.line_to(420, y); c.move_to(660, y); c.line_to(830, y); c.stroke()
    # cap
    font(c, 30)
    for k in range(-4, 5):
        x = W / 2 + k * 90 - (t * 20 % 90)
        c.move_to(x, 380); c.line_to(x, 400); c.stroke()
    # réticule canon qui converge vers la cible
    rx = 540 + (fx - 540) * lock + 120 * (1 - lock) * math.sin(t * 1.7)
    ry = 820 + (fy - 820) * lock + 80 * (1 - lock) * math.cos(t * 1.3)
    c.arc(rx, ry, 120, 0, 2 * math.pi); c.stroke()
    c.arc(rx, ry, 6, 0, 2 * math.pi); c.fill()
    for k in range(8):
        ang = k * math.pi / 4
        c.move_to(rx + 120 * math.cos(ang), ry + 120 * math.sin(ang)); c.line_to(rx + 140 * math.cos(ang), ry + 140 * math.sin(ang)); c.stroke()
    c.move_to(W / 2 - 30, 1250); c.line_to(W / 2, 1220); c.line_to(W / 2 + 30, 1250); c.stroke()
    font(c, 34); c.move_to(120, 1330); c.show_text("GUN"); c.move_to(820, 1330); c.show_text(f"{max(0.4, 1.6 - 1.2 * lock):.1f} NM")
    if lock > 0.95 and grey == 0 and int(t * 4) % 2 == 0:
        text_c(c, "IN RANGE", W / 2, 1120, 56, col)
    if grey > 0:
        c.set_source_rgba(0.1, 0.1, 0.1, 0.55 * grey); c.rectangle(0, 320, W, 1130); c.fill()
    text_c(c, "RECONSTITUTION", W / 2, 1420, 26, (1, 1, 1, 0.45))


def sc_duel(c, t, s):
    lt = t - s['t0']; u = (t - s['vt']) / s['dur']
    background(c, t)
    if u < 0.32:
        a = ease(lt / 0.3)
        sc = back_out(lt / 0.4)
        c.save(); c.translate(W / 2, 880); c.scale(0.6 + 0.4 * sc, 0.6 + 0.4 * sc)
        text_c(c, "DERNIER ROUND", 0, 0, 104, (*YEL, a), stroke=12)
        c.restore()
        pill(c, "2009 · ÉMIRATS ARABES UNIS", W / 2, 1020, 40, (0.85, 0.85, 0.9), fg=(0.05, 0.05, 0.08), s=back_out((u - 0.12) / 0.1))
    else:
        lock = ease((u - 0.45) / 0.45)
        hud(c, t, lock)
        fl = 1 - ease((u - 0.32) / 0.05)
        if fl > 0: c.set_source_rgba(1, 1, 1, 0.7 * fl); c.paint()


def sc_doute(c, t, s):
    lt = t - s['t0']; u = (t - s['vt']) / s['dur']
    background(c, t)
    hud(c, s['t0'], 1.0, grey=ease(lt / 0.5))
    q = back_out((lt - 0.2) / 0.4)
    c.save(); c.translate(W / 2, 760); c.scale(q, q)
    text_c(c, "?", 0, 110, 320, (1, 1, 1, 0.95), stroke=16)
    c.restore()
    pill(c, "JAMAIS CONFIRMÉ PAR L'US AIR FORCE", W / 2, 1060, 34, RED, s=back_out((u - 0.15) / 0.12))
    pill(c, "RÈGLES FIXÉES À L'AVANCE", W / 2, 1160, 34, (0.85, 0.85, 0.9), fg=(0.05, 0.05, 0.08), s=back_out((u - 0.55) / 0.12))


def sc_verdict(c, t, s):
    lt = t - s['t0']; u = (t - s['vt']) / s['dur']
    if u < 0.5:
        background(c, t, tint=[(RED, 540, 640, 520, 0.35), (BLU, 540, 1180, 520, 0.35)])
        a = ease(lt / 0.3)
        text_c(c, "VERDICT", W / 2, 400, 60, (*YEL, a), stroke=8)
        c.set_source_rgba(1, 1, 1, 0.15 * a); c.rectangle(80, 910, W - 160, 2); c.fill()
        plane(c, 'f_34', 650, 660, 520, alpha=a, glow=RED)
        pill(c, "DE LOIN", 260, 560, 40, (0.85, 0.85, 0.9), fg=(0.05, 0.05, 0.08), s=back_out((u - 0.03) / 0.08))
        text_c(c, "F-22", 260, 680, 74, (*RED, ease((u - 0.08) / 0.08)), stroke=8)
        plane(c, 'r_34', 430, 1180, 520, alpha=ease((u - 0.2) / 0.1), glow=BLU)
        pill(c, "DE PRÈS", 820, 1080, 40, (0.85, 0.85, 0.9), fg=(0.05, 0.05, 0.08), s=back_out((u - 0.24) / 0.08))
        text_c(c, "RAFALE", 820, 1200, 74, (*BLU, ease((u - 0.28) / 0.08)), stroke=8)
    else:
        background(c, t, tint=[(BLU, 300, 1000, 600, 0.35), (RED, 780, 1000, 600, 0.35)], streak=0.6)
        v = back_out((u - 0.5) / 0.1)
        c.save(); c.translate(W / 2, 640); c.scale(v, v)
        text_c(c, "ET TOI,", 0, 0, 96, (1, 1, 1, 1), stroke=12)
        text_c(c, "QUI GAGNE ?", 0, 110, 110, (*YEL, 1), stroke=12)
        c.restore()
        p = 1 + 0.05 * math.sin(t * 6)
        pill(c, "RAFALE", 300, 1000, 60, BLU, s=back_out((u - 0.58) / 0.08) * p)
        pill(c, "F-22", 780, 1000, 60, RED, s=back_out((u - 0.62) / 0.08) * (2 - p))
        a = ease((u - 0.7) / 0.1)
        text_c(c, "DIS-LE EN COMMENTAIRE", W / 2, 1200, 50, (1, 1, 1, a), stroke=8)
        c.set_source_rgba(*YEL, a); c.set_line_width(8)
        yy = 1250 + 12 * math.sin(t * 6)
        c.move_to(W / 2 - 30, yy); c.line_to(W / 2, yy + 34); c.line_to(W / 2 + 30, yy); c.stroke()


SCN = dict(hook=sc_hook, vitesse=sc_vitesse, furtif=sc_furtif, poly=sc_poly, reel=sc_reel, duel=sc_duel, doute=sc_doute, verdict=sc_verdict)


# ---------- Sous-titres ----------
def build_caps():
    caps = []
    for s, sc in zip(SEG, SCENES):
        words = sc['show'].split(' ')

        def wt(w_):
            n = len(re.sub(r'[^\w]', '', w_)) + 3 * sum(ch.isdigit() for ch in w_)
            if w_.endswith(('.', '!', '?', ':')): n += 6
            if '…' in w_: n += 8
            if w_.endswith(','): n += 3
            return max(n, 2) + 2
        ws = [wt(w_) for w_ in words]; tot = sum(ws); t0 = s['vt']; dur = s['dur']
        times = []; acc = 0
        for w_ in ws:
            times.append((t0 + dur * acc / tot, t0 + dur * (acc + w_) / tot)); acc += w_
        grp = []
        for j, w_ in enumerate(words):
            grp.append(j)
            if len(grp) == 3 or w_.endswith(('.', '!', '?', ':', ',', '…')) or j == len(words) - 1 or (len(grp) == 2 and len(''.join(words[q] for q in grp)) > 14):
                caps.append(dict(words=[words[q] for q in grp], times=[times[q] for q in grp], t0=times[grp[0]][0], t1=times[grp[-1]][1])); grp = []
    return caps


CAPS = build_caps()


def captions(c, t):
    cap = None
    for cp in CAPS:
        if cp['t0'] - 0.02 <= t < cp['t1'] + 0.05: cap = cp
    if not cap: return
    size = 68; font(c, size)
    words = [w_.upper() for w_ in cap['words']]
    sp = c.text_extents(' ').x_advance; widths = [c.text_extents(w_).x_advance for w_ in words]
    total = sum(widths) + sp * (len(words) - 1)
    if total > 880:
        size *= 880 / total; font(c, size); widths = [c.text_extents(w_).x_advance for w_ in words]; sp = c.text_extents(' ').x_advance
        total = sum(widths) + sp * (len(words) - 1)
    pop = back_out((t - cap['t0']) / 0.15); y = 1610
    c.save(); c.translate(W / 2, y); c.scale(0.85 + 0.15 * pop, 0.85 + 0.15 * pop); c.translate(-W / 2, -y)
    x = W / 2 - total / 2
    for w_, wd, (a, b) in zip(words, widths, cap['times']):
        c.move_to(x, y); c.text_path(w_)
        c.set_source_rgba(0, 0, 0, 0.9); c.set_line_width(13); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
        hi = YEL
        if 'RAFALE' in w_: hi = (0.45, 0.68, 1.0)
        if 'F-22' in w_ or 'RAPTOR' in w_: hi = (1.0, 0.45, 0.4)
        c.set_source_rgb(*(hi if a <= t < b + 0.05 else WHITE)); c.fill(); c.new_path()
        x += wd + sp
    c.restore()


def render(t, surf):
    c = cairo.Context(surf)
    s = SEG[0]
    for x in SEG:
        if t >= x['t0']: s = x
    SCN[s['scene']](c, t, s)
    scoreboard(c, t, s)
    captions(c, t)
    lt = t - s['t0']
    if lt < 0.12 and s['t0'] > 0:
        c.set_source_rgba(1, 1, 1, 0.35 * (1 - lt / 0.12)); c.paint()
    c.set_source_rgba(*YEL, 1); c.rectangle(0, 0, W * t / TOTAL, 6); c.fill()
    if t < 0.15:
        c.set_source_rgba(0, 0, 0, 1 - t / 0.15); c.paint()
    if t > TOTAL - 0.4:
        c.set_source_rgba(0, 0, 0, (t - (TOTAL - 0.4)) / 0.4); c.paint()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        for tt in map(float, sys.argv[2:]):
            sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); render(tt, sf); sf.write_to_png(D + f'still_{tt:.1f}.png')
        print(round(TOTAL, 1), [(x['scene'], round(x['t0'], 1)) for x in SEG]); sys.exit()
    nframes = int(TOTAL * FPS)
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}',
                           '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '21',
                           '-pix_fmt', 'yuv420p', D + 'video_noaudio.mp4'], stdin=subprocess.PIPE)
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    for f in range(nframes):
        render(f / FPS, sf); sf.flush(); ff.stdin.write(bytes(sf.get_data()))
        if f % 300 == 0: print(f, '/', nframes, flush=True)
    ff.stdin.close(); ff.wait(); print('done', TOTAL)
