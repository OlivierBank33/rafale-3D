"""« Combien d'oiseaux pour abattre un avion ? » — escalade 1 → 5 → 20 → 100 → 1 000, dégâts cumulés sur un A320 (2,5D).
Usage : python3 bs_render.py [stills t1 t2 ...]  -> bs/video_noaudio.mp4 + bs/events.json (pour l'audio)"""
import cairo, json, math, os, random, subprocess, sys
import numpy as np
import mascot as _M

W, H, FPS = 1080, 1920, 30
OUT = 'bs/'; os.makedirs(OUT, exist_ok=True)
WHITE = (1, 1, 1); YEL = (1.0, 0.84, 0.1); RED = (1.0, 0.28, 0.25); ORA = (1.0, 0.55, 0.12); GRN = (0.25, 0.85, 0.4); INK = (0.05, 0.05, 0.08)

# ---------- avion (image Blender) ----------
PL = cairo.ImageSurface.create_from_png('r3d/a320.png')
PCX, PCY = 772, 725            # centre de l'avion dans l'image
S0 = 1.12
# points d'impact (coordonnées image)
Z = dict(nose=(352, 922), wind=(392, 873), eng=(742, 896), wingR=(930, 822), wingL=(470, 735), body=(560, 840), fus2=(700, 790))
ZW = dict(nose=3, wind=3, eng=3, wingR=2, wingL=1.5, body=2, fus2=1.5)

# ---------- chronologie ----------
LEVELS = [  # (n, t0, t1, titre)
    (1, 3.0, 9.0, "1 OISEAU"),
    (5, 13.5, 20.5, "5 OISEAUX"),
    (20, 25.0, 32.0, "20 OISEAUX"),
    (100, 32.5, 40.0, "100 OISEAUX"),
    (1000, 40.5, 49.0, "1 000 OISEAUX"),
]
FACTS = [  # (t0, t1, lignes, pose)
    (9.2, 13.4, ["Le pare-brise est testé", "au CANON À POULETS :", "1,8 kg tiré à la vitesse", "de croisière."], 'shocked'),
    (20.7, 24.9, ["Un réacteur doit pouvoir", "avaler un gros oiseau", "sans exploser…", "mais il a le droit de s'arrêter."], 'skeptical'),
]
T_END_SIM = 50.0
T_HUDSON = 50.5
TOTAL = 66.0

rng = random.Random(7)
BIRDS = []   # dict(t0, th, y0, target or None, x1,y1 (miss end), size, ph)
EVENTS = []  # pour l'audio : (t, kind)
for li, (n, a, b, _) in enumerate(LEVELS):
    span = b - a - 1.5
    for k in range(n):
        if n == 1: th = a + 1.6
        elif n <= 20: th = a + 1.2 + span * (k + rng.random() * 0.6) / n
        else: th = a + 1.0 + span * rng.random()
        hit = (n <= 100) or rng.random() < 0.12
        if n == 1: zone = 'nose'
        elif n == 5 and k == 1: zone = 'eng'
        elif n == 5 and k == 3: zone = 'wind'
        else:
            zs = list(ZW); zone = rng.choices(zs, [ZW[z] for z in zs])[0]
        dur = 0.75 if n <= 20 else 0.55 + rng.random() * 0.4
        y0 = rng.uniform(250, 1500) if n > 20 else rng.uniform(500, 1200)
        BIRDS.append(dict(t0=th - dur, th=th, y0=y0, zone=zone if hit else None, lvl=li, size=(1.0 if n <= 20 else rng.uniform(0.5, 0.9)),
                          ph=rng.random() * 6, my=rng.uniform(150, 1700), jit=(rng.uniform(-18, 18), rng.uniform(-14, 14))))
        if hit: EVENTS.append((th, 'eng' if zone == 'eng' else 'hit', li))
        elif n <= 1000 and k % 8 == 0: EVENTS.append((th, 'pass', li))
EVENTS.sort()
json.dump(dict(events=EVENTS, levels=[(l[1], l[2]) for l in LEVELS], facts=[(f[0], f[1]) for f in FACTS], total=TOTAL, hudson=T_HUDSON), open(OUT + 'events.json', 'w'))

HITS = sorted([bd for bd in BIRDS if bd['zone']], key=lambda b: b['th'])


def hits_until(t, zone=None):
    return [h for h in HITS if h['th'] <= t and (zone is None or h['zone'] == zone)]


def health(t):
    n = len(hits_until(t)); return max(0.0, 1 - 0.05 * n ** 0.62) if t < 46 else max(0, (1 - 0.05 * n ** 0.62) * (1 - (t - 46) / 2))


# ---------- helpers ----------
def ease(u):
    u = min(max(u, 0), 1); return u * u * (3 - 2 * u)


def ease_out(u):
    u = min(max(u, 0), 1); return 1 - (1 - u) ** 3


def font(c, size):
    c.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(size)


def text_c(c, txt, x, y, size, rgba=(1, 1, 1, 1), stroke=0, maxw=None):
    font(c, size); e = c.text_extents(txt)
    if maxw and e.x_advance > maxw:
        size *= maxw / e.x_advance; font(c, size); e = c.text_extents(txt)
    c.move_to(x - e.x_advance / 2, y); c.text_path(txt)
    if stroke:
        c.set_source_rgba(0, 0, 0, 0.85 * rgba[3]); c.set_line_width(stroke); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
    c.set_source_rgba(*rgba); c.fill(); c.new_path()


def text_l(c, txt, x, y, size, rgba=(1, 1, 1, 1)):
    font(c, size); c.move_to(x, y); c.set_source_rgba(*rgba); c.show_text(txt); c.new_path()


def rrect(c, x, y, w, h, r):
    c.new_sub_path(); c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2); c.close_path()


def plane_tf(t):
    """(cx, cy, scale, rot) de l'avion à l'écran — mouvement lent, jamais de tremblement."""
    bob = 8 * math.sin(t * 0.9)
    rot = 0.0; cy = 900 + bob; cx = W / 2; s = S0
    if t > 36: rot -= 0.06 * ease((t - 36) / 6)                       # piqué progressif
    if t > 44: rot -= 0.08 * ease((t - 44) / 5); cy += 120 * ease((t - 44) / 5)
    return cx, cy, s, rot


def to_screen(p, t):
    cx, cy, s, r = plane_tf(t); x, y = (p[0] - PCX) * s, (p[1] - PCY) * s
    return cx + x * math.cos(r) - y * math.sin(r), cy + x * math.sin(r) + y * math.cos(r)


def background(c, t):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, 0.30, 0.32, 0.36); g.add_color_stop_rgb(0.55, 0.20, 0.21, 0.24); g.add_color_stop_rgb(1, 0.10, 0.10, 0.12)
    c.set_source(g); c.paint()
    r = cairo.RadialGradient(W / 2, 900, 50, W / 2, 900, 900); r.add_color_stop_rgba(0, 1, 1, 1, 0.10); r.add_color_stop_rgba(1, 1, 1, 1, 0)
    c.set_source(r); c.paint()
    # ombre au sol
    c.save(); c.translate(W / 2, 1330); c.scale(1, 0.12); c.arc(0, 0, 420, 0, 2 * math.pi); c.restore()
    g2 = cairo.RadialGradient(W / 2, 1330, 10, W / 2, 1330, 420); g2.add_color_stop_rgba(0, 0, 0, 0, 0.35); g2.add_color_stop_rgba(1, 0, 0, 0, 0)
    c.set_source(g2); c.fill()


def bird_path(c, x, y, s, flap, alpha=1.0, col=(0.12, 0.12, 0.14)):
    """Mouette stylisée vue de côté (vole vers la droite)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    w = 26 * flap
    c.move_to(-18, 0); c.curve_to(-8, -6, 10, -6, 20, -1); c.line_to(26, 0); c.line_to(20, 3); c.curve_to(8, 6, -8, 5, -18, 2); c.close_path()
    c.move_to(-4, -2); c.curve_to(-10, -2 - w * 0.6, -22, -2 - w, -30, -4 - w); c.curve_to(-18, -2 - w * 0.3, -10, 0, 4, -1); c.close_path()
    c.set_source_rgba(*col, alpha); c.fill()
    c.restore()


def draw_plane(c, t):
    cx, cy, s, r = plane_tf(t)
    c.save(); c.translate(cx, cy); c.rotate(r); c.scale(s, s); c.translate(-PCX, -PCY)
    c.set_source_surface(PL, 0, 0); c.paint()
    hz = {}
    for h in hits_until(t): hz.setdefault(h['zone'], []).append(h)
    # traces d'impact + bosses
    for h in hits_until(t):
        p = Z[h['zone']]; jx, jy = h['jit']
        age = t - h['th']; a = min(1, age / 0.15)
        x, y = p[0] + jx, p[1] + jy
        g = cairo.RadialGradient(x, y, 1, x, y, 16); g.add_color_stop_rgba(0, 0.25, 0.18, 0.14, 0.75 * a); g.add_color_stop_rgba(1, 0.25, 0.18, 0.14, 0)
        c.set_source(g); c.arc(x, y, 16, 0, 2 * math.pi); c.fill()
        if h['zone'] in ('nose', 'wingR', 'wingL', 'body', 'fus2'):
            c.save(); c.translate(x - 2, y - 2); c.scale(1, 0.6); c.arc(0, 0, 9, 0.3, math.pi - 0.3); c.restore()
            c.set_source_rgba(0, 0, 0, 0.35 * a); c.set_line_width(4); c.stroke()
    # pare-brise fissuré
    nw = len(hz.get('wind', []))
    if nw:
        rr = random.Random(3); x0, y0 = Z['wind']
        c.set_line_width(1.4); c.set_source_rgba(1, 1, 1, 0.85)
        for k in range(min(14, 4 + nw * 3)):
            ang = rr.uniform(0, 2 * math.pi); L = rr.uniform(8, 22 + 4 * nw); x, y = x0, y0; c.move_to(x, y)
            for s_ in range(3):
                ang += rr.uniform(-0.6, 0.6); x += math.cos(ang) * L / 3; y += math.sin(ang) * L / 3; c.line_to(x, y)
            c.stroke()
    c.restore()


def engine_fx(c, t):
    ne = len(hits_until(t, 'eng'))
    if not ne: return
    first = hits_until(t, 'eng')[0]['th']; ex, ey = to_screen((Z['eng'][0] + 60, Z['eng'][1] + 5), t)
    inten = min(1, 0.35 + 0.12 * ne)
    rr = random.Random(11)
    for k in range(int(10 + 30 * inten)):           # fumée qui part vers l'arrière (droite) et monte
        ph = rr.random(); life = 2.4; age = ((t - first) / life + ph) % 1
        if t - first < ph * life: continue
        x = ex + age * 330 + rr.uniform(-10, 10); y = ey - age * 120 + math.sin(age * 6 + k) * 10
        rad = 12 + age * 70; a = (1 - age) * 0.35 * inten
        gr = 0.25 + 0.15 * rr.random() if ne < 6 else 0.12
        g = cairo.RadialGradient(x, y, 1, x, y, rad); g.add_color_stop_rgba(0, gr, gr, gr, a); g.add_color_stop_rgba(1, gr, gr, gr, 0)
        c.set_source(g); c.arc(x, y, rad, 0, 2 * math.pi); c.fill()
    if t > 34.5:                                       # feu
        f = min(1, (t - 34.5) / 1.5)
        for k in range(26):
            age = ((t * 1.7 + k / 26) % 1); x = ex + 10 + age * 120 + math.sin(k * 3.1 + t * 9) * 6; y = ey - age * 50
            rad = (26 - 18 * age) * f
            c.set_source_rgba(1, 0.45 + 0.4 * (1 - age), 0.08, 0.75 * (1 - age) * f); c.arc(x, y, rad, 0, 2 * math.pi); c.fill()
    # étincelles juste après chaque impact moteur
    for h in hits_until(t, 'eng'):
        age = t - h['th']
        if 0 <= age < 0.5:
            r2 = random.Random(int(h['th'] * 100))
            for k in range(14):
                a = r2.uniform(-1.2, 1.2); v = r2.uniform(150, 420) * age; x, y = ex - 40 + math.cos(a) * v, ey + math.sin(a) * v
                c.move_to(x, y); c.line_to(x - math.cos(a) * 14, y - math.sin(a) * 14)
                c.set_source_rgba(1, 0.75, 0.2, 1 - age * 2); c.set_line_width(3); c.stroke()


def feathers(c, t):
    for h in hits_until(t):
        age = t - h['th']
        if age > 1.6: continue
        x0, y0 = to_screen(Z[h['zone']], t); r2 = random.Random(int(h['th'] * 1000) + 1)
        n = 9 if len(HITS) < 200 or h['lvl'] < 4 else 4
        for k in range(n):
            a = r2.uniform(-math.pi, math.pi); v = r2.uniform(80, 260)
            x = x0 + math.cos(a) * v * age; y = y0 + math.sin(a) * v * age + 140 * age * age
            c.save(); c.translate(x, y); c.rotate(a + age * r2.uniform(-6, 6)); c.scale(1, 0.35)
            c.arc(0, 0, r2.uniform(6, 11), 0, 2 * math.pi); c.restore()
            g = r2.uniform(0.75, 0.95); c.set_source_rgba(g, g, g * 0.97, max(0, 1 - age / 1.6)); c.fill()
        if age < 0.12:
            c.set_source_rgba(1, 1, 1, 0.5 * (1 - age / 0.12)); c.arc(x0, y0, 40 + 200 * age, 0, 2 * math.pi); c.fill()


def birds(c, t):
    for bd in BIRDS:
        if not (bd['t0'] <= t <= bd['th'] + (0.9 if not bd['zone'] else 0)): continue
        u = (t - bd['t0']) / (bd['th'] - bd['t0'])
        if bd['zone']:
            tx, ty = to_screen(Z[bd['zone']], t); x = -60 + (tx + 60) * u; y = bd['y0'] + (ty - bd['y0']) * ease(u)
            if t > bd['th']: continue
        else:
            x = -60 + 1200 * u; y = bd['y0'] + (bd['my'] - bd['y0']) * u * 0.3
        flap = math.sin(t * 16 + bd['ph']); s = (2.6 if bd['lvl'] == 0 else (1.9 if bd['lvl'] < 3 else 1.1)) * bd['size']
        bird_path(c, x, y, s, flap, 0.95)


def title(c, t):
    lv = None
    for i, (n, a, b, lab) in enumerate(LEVELS):
        if a - 0.6 <= t: lv = i
    if t < 3.0:
        u = ease_out(t / 0.5)
        text_c(c, "COMBIEN D'OISEAUX", W / 2, 230 - 30 * (1 - u), 82, (1, 1, 1, u), stroke=10, maxw=980)
        text_c(c, "POUR ABATTRE UN AVION ?", W / 2, 330 - 30 * (1 - u), 64, (*YEL, u), stroke=9, maxw=980)
        return
    if lv is None or t > T_HUDSON - 0.3: return
    n, a, b, lab = LEVELS[lv]; age = t - (a - 0.6); k = 1 + 0.35 * max(0, 1 - age / 0.25)
    num, word = lab.split(' ', 1) if not lab.startswith('1 000') else ('1 000', 'OISEAUX')
    c.save(); c.translate(W / 2, 250); c.scale(k, k)
    text_c(c, num, 0, 0, 150, (*YEL, 1), stroke=14)
    c.restore()
    text_c(c, word, W / 2, 335, 70, (1, 1, 1, 1), stroke=9)
    text_c(c, "CONTRE UN AIRBUS A320", W / 2, 400, 38, (0.85, 0.87, 0.92, 0.9), stroke=6)


ROWS = [('nose', "RADÔME"), ('wind', "PARE-BRISE"), ('eng', "MOTEURS"), ('wing', "AILES")]


def zone_state(z, t):
    if z == 'wing': n = len(hits_until(t, 'wingR')) + len(hits_until(t, 'wingL'))
    else: n = len(hits_until(t, z))
    if z == 'eng':
        if t > 46: return "0 / 2 · ARRÊTÉS", RED
        if t > 34.5: return "EN FEU", RED
        if n >= 3: return "1 MOTEUR COUPÉ", ORA
        if n: return "ENDOMMAGÉ", ORA
        return "OK", GRN
    if z == 'wind':
        if n >= 6: return "BRISÉ", RED
        if n: return "FISSURÉ", ORA
        return "OK", GRN
    if n >= 12: return "DÉTRUIT", RED
    if n >= 3: return "TRÈS ABÎMÉ", ORA
    if n: return "CABOSSÉ", ORA
    return "OK", GRN


def panel(c, t):
    if t < 3.0 or t > T_HUDSON - 0.3: return
    if any(f[0] <= t <= f[1] for f in FACTS): return
    x0, y0, w = 50, 1440, 640
    rrect(c, x0, y0, w, 330, 26); c.set_source_rgba(0.04, 0.04, 0.06, 0.72); c.fill()
    text_l(c, "DÉGÂTS", x0 + 30, y0 + 52, 34, (*YEL, 1))
    hp = health(t); bw = 300
    rrect(c, x0 + w - 30 - bw, y0 + 28, bw, 26, 13); c.set_source_rgba(1, 1, 1, 0.15); c.fill()
    col = GRN if hp > 0.6 else (ORA if hp > 0.3 else RED)
    if hp > 0.01: rrect(c, x0 + w - 30 - bw, y0 + 28, bw * hp, 26, 13); c.set_source_rgba(*col, 1); c.fill()
    text_c(c, f"{int(round(hp * 100))} %", x0 + w - 30 - bw / 2, y0 + 50, 22, (1, 1, 1, 1))
    for i, (z, lab) in enumerate(ROWS):
        y = y0 + 110 + i * 58; st, cl = zone_state(z, t)
        text_l(c, lab, x0 + 30, y, 32, (0.9, 0.92, 0.96, 1))
        font(c, 32); e = c.text_extents(st); text_l(c, st, x0 + w - 30 - e.x_advance, y, 32, (*cl, 1))


def fact_card(c, t):
    for (a, b, lines, pose) in FACTS:
        if a <= t <= b:
            u = ease_out((t - a) / 0.35) * (1 - ease((t - (b - 0.3)) / 0.3))
            c.set_source_rgba(0, 0, 0, 0.45 * u); c.paint()
            y0 = 1300 + 60 * (1 - u)
            rrect(c, 40, y0, W - 80, 470, 34); c.set_source_rgba(0.06, 0.07, 0.10, 0.94 * u); c.fill()
            rrect(c, 40, y0, W - 80, 470, 34); c.set_source_rgba(*YEL, 0.9 * u); c.set_line_width(4); c.stroke()
            text_l(c, "LE SAVAIS-TU ?", 360, y0 + 80, 40, (*YEL, u))
            for i, ln in enumerate(lines):
                text_l(c, ln, 360, y0 + 150 + i * 62, 40, (1, 1, 1, u))
            _M.draw(c, 190, y0 + 470, 400, pose=pose, blink=1 if (t % 3.3) < 0.1 else 0, alpha=u)


def hudson(c, t):
    if t < T_HUDSON: return
    lt = t - T_HUDSON; u = ease_out(lt / 0.6)
    c.set_source_rgba(0.02, 0.03, 0.06, 0.985 * u); c.paint()
    # eau + avion qui plane
    g = cairo.LinearGradient(0, 1050, 0, 1350); g.add_color_stop_rgba(0, 0.15, 0.28, 0.40, u); g.add_color_stop_rgba(1, 0.05, 0.10, 0.18, u)
    c.rectangle(0, 1050, W, 300); c.set_source(g); c.fill()
    for k in range(18):
        y = 1070 + k * 15; x = (k * 97 + lt * 60) % (W + 200) - 100
        c.set_source_rgba(0.6, 0.75, 0.9, 0.25 * u); c.rectangle(x, y, 120, 3); c.fill()
    pu = min(1, lt / 9.0); s = 0.42
    px = 160 + 560 * pu; py = 780 + 230 * ease(pu)
    c.save(); c.translate(px, py); c.rotate(0.05); c.scale(-s, s); c.translate(-PCX, -PCY)
    c.set_source_surface(PL, 0, 0); c.paint_with_alpha(u); c.restore()
    text_c(c, "ET DANS LA VRAIE VIE ?", W / 2, 260, 66, (*YEL, u), stroke=9)
    L = [(1.0, "15 janvier 2009, New York."), (3.2, "Quelques bernaches percutent"), (3.2, "un Airbus A320 au décollage."),
         (6.0, "Les 2 moteurs s'arrêtent."), (8.5, "Il se pose sur l'Hudson…")]
    for i, (d, s_) in enumerate(L):
        a = ease_out((lt - d) / 0.4)
        if a > 0: text_c(c, s_, W / 2, 380 + i * 64, 46, (1, 1, 1, a), stroke=6, maxw=980)
    if lt > 10.5:
        a = ease_out((lt - 10.5) / 0.4); k = 1 + 0.3 * max(0, 1 - (lt - 10.5) / 0.25)
        c.save(); c.translate(W / 2, 1480); c.scale(k, k)
        rrect(c, -360, -70, 720, 110, 30); c.set_source_rgba(*GRN, a); c.fill()
        text_c(c, "155 PERSONNES · 0 MORT", 0, 5, 52, (0.02, 0.1, 0.04, a)); c.restore()
    if lt > 12.6:
        a = ease_out((lt - 12.6) / 0.4)
        text_c(c, "Et toi, tu aurais parié combien d'oiseaux ?", W / 2, 1640, 40, (1, 1, 1, a), stroke=6, maxw=960)
        text_c(c, "ABONNE-TOI POUR LA SUITE", W / 2, 1720, 38, (*YEL, a), stroke=6)
    _M.draw(c, 170, 1940, 420, pose='salute' if lt > 10.5 else 'shocked', alpha=u, blink=1 if (t % 3.1) < 0.1 else 0)


def swarm_dark(c, t):
    if 42 < t < 49:
        a = 0.35 * math.sin(math.pi * (t - 42) / 7) ** 2
        c.set_source_rgba(0, 0, 0, a); c.paint()


def mascot_corner(c, t):
    if t < 3.0 or t > T_HUDSON - 0.3 or any(f[0] - 0.2 <= t <= f[1] + 0.2 for f in FACTS): return
    pose = 'neutral'
    for (n, a, b, _) in LEVELS:
        if a <= t <= b: pose = 'skeptical' if n == 1 else ('shocked' if n < 100 else 'panic')
    recent = [h for h in hits_until(t) if t - h['th'] < 0.6]
    if recent and len(HITS) and LEVELS[0][1] <= t < LEVELS[2][1]: pose = 'shocked'
    if t > 46: pose = 'facepalm'
    _M.draw(c, 950, 1900, 400, pose=pose, blink=1 if (t % 3.4) < 0.1 else 0)


def frame(t):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    background(c, t)
    draw_plane(c, t); engine_fx(c, t); feathers(c, t); birds(c, t); swarm_dark(c, t)
    title(c, t); panel(c, t); mascot_corner(c, t); fact_card(c, t); hudson(c, t)
    # barre de progression
    c.set_source_rgba(*YEL, 1); c.rectangle(0, 0, W * t / TOTAL, 8); c.fill()
    return s


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        for x in sys.argv[2:]: frame(float(x)).write_to_png(OUT + f'still_{x}.png')
        sys.exit()
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', OUT + 'video_noaudio.mp4'], stdin=subprocess.PIPE)
    n = int(TOTAL * FPS)
    for i in range(n):
        ff.stdin.write(bytes(frame(i / FPS).get_data()))
        if i % 300 == 0: print(i, '/', n, flush=True)
    ff.stdin.close(); ff.wait(); print('done', TOTAL)
