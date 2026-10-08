"""Série « MINUTE AÉRO · DÉCODÉ » : fiche technique en traits isométriques lumineux, HUD, chrono, sous-titres géants.
Usage : DL=dl/<slug> python3 dc_render.py [stills t1 ...]   (cfg.py : SCENES[type, say, show], END_HOLD ; durs.json)"""
import cairo, json, math, os, re, subprocess, sys, random, importlib.util

W, H, FPS = 1080, 1920, 30
D = os.environ.get('DL', 'dl/dc_oxygene').rstrip('/') + '/'
spec = importlib.util.spec_from_file_location('cfg', D + 'cfg.py'); CFG = importlib.util.module_from_spec(spec); spec.loader.exec_module(CFG)
SCENES = CFG.SCENES
DUR = json.load(open(D + 'durs.json'))
SEG = []; t = 0.0
for i, s in enumerate(SCENES):
    pre = 0.2 if i == 0 else 0.3
    post = 0.35 if i < len(SCENES) - 1 else getattr(CFG, 'END_HOLD', 2.0)
    SEG.append(dict(i=i, k=f's{i}', scene=s['type'], t0=t, vt=t + pre, dur=DUR[f's{i}'], end=t + pre + DUR[f's{i}'] + post, score=(0, 0), p=s))
    t = SEG[-1]['end']
TOTAL = t
json.dump(dict(seg=[{k: v for k, v in x.items() if k != 'p'} for x in SEG], total=TOTAL), open(D + 'timeline.json', 'w'))

BG = (0.024, 0.031, 0.043); AMB = (1.0, 0.62, 0.12); CYA = (0.30, 0.86, 1.0); RED = (1.0, 0.25, 0.22); GRN = (0.30, 0.95, 0.50); WHT = (0.93, 0.95, 0.98); DIM = (0.45, 0.50, 0.58)
PHASE = dict(hook=0, story=0, alarm=0, open=1, chrono=1, heat=1, bag=1, descent=2, helios=2, outro=2)


def ease(u):
    u = min(max(u, 0), 1); return u * u * (3 - 2 * u)


def eo(u):
    u = min(max(u, 0), 1); return 1 - (1 - u) ** 3


def F(c, size, fam='Oswald', bold=True):
    c.select_font_face(fam, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL); c.set_font_size(size)


def txt(c, s, x, y, size, rgba, fam='Oswald', anchor='l', bold=True):
    F(c, size, fam, bold); e = c.text_extents(s)
    xx = x - (e.x_advance if anchor == 'r' else e.x_advance / 2 if anchor == 'c' else 0)
    c.move_to(xx, y); c.set_source_rgba(*rgba); c.show_text(s); c.new_path(); return e.x_advance


# ---------- projection isométrique ----------
class Iso:
    def __init__(self, cx, cy, s): self.cx, self.cy, self.s = cx, cy, s
    def p(self, x, y, z):
        return self.cx + (x - y) * 0.866 * self.s, self.cy + (x + y) * 0.5 * self.s - z * self.s


def glow_path(c, draw, col, a=1.0, w=3.0):
    for lw, al in ((w * 5, 0.10), (w * 2.2, 0.25), (w, 1.0)):
        draw(); c.set_source_rgba(*col, a * al); c.set_line_width(lw); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()


def poly(c, pts, close=True):
    c.move_to(*pts[0])
    for q in pts[1:]: c.line_to(*q)
    if close: c.close_path()


def box(c, I, x0, y0, z0, dx, dy, dz, col, a=1.0, fill=0.06, w=2.4):
    P = I.p
    V = [P(x0 + i * dx, y0 + j * dy, z0 + k * dz) for i in (0, 1) for j in (0, 1) for k in (0, 1)]
    faces = [(1, 3, 7, 5), (2, 3, 7, 6), (4, 5, 7, 6)]
    for f in faces:
        poly(c, [V[q] for q in f]); c.set_source_rgba(*col, fill * a); c.fill()
    E = [(0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3), (2, 6), (3, 7), (4, 5), (4, 6), (5, 7), (6, 7)]
    def d():
        for (u, v) in E: c.move_to(*V[u]); c.line_to(*V[v])
    glow_path(c, d, col, a, w)


def cyl(c, I, x, y, z0, r, h, col, a=1.0, fill=0.06, axis='z', w=2.4, n=40):
    """Cylindre wireframe (axe z ou x)."""
    P = I.p
    def ring(zz):
        if axis == 'z': return [P(x + r * math.cos(k / n * 2 * math.pi), y + r * math.sin(k / n * 2 * math.pi), zz) for k in range(n + 1)]
        return [P(zz, y + r * math.cos(k / n * 2 * math.pi), z0 + r * math.sin(k / n * 2 * math.pi)) for k in range(n + 1)]
    if axis == 'z': A, B = ring(z0), ring(z0 + h)
    else: A, B = ring(x), ring(x + h)
    poly(c, A + B[::-1]); c.set_source_rgba(*col, fill * a); c.fill()
    def d():
        poly(c, A, False); poly(c, B, False)
        for k in (0, n // 4, n // 2, 3 * n // 4): c.move_to(*A[k]); c.line_to(*B[k])
    glow_path(c, d, col, a, w)
    return A, B


def callout(c, x, y, tx, ty, label, col, a):
    if a <= 0: return
    F(c, 30, 'Space Mono'); tw_ = c.text_extents(label).x_advance
    if tx > x and tx + 70 + tw_ > W - 20: tx = x - (tx - x)
    elif tx <= x and tx - 70 - tw_ < 20: tx = x + (x - tx)
    tx = min(max(tx, 20), W - 20)
    def d(): c.move_to(x, y); c.line_to(tx, ty); c.line_to(tx + (60 if tx > x else -60), ty)
    glow_path(c, d, col, a, 1.6)
    c.set_source_rgba(*col, a); c.arc(x, y, 6, 0, 2 * math.pi); c.fill()
    txt(c, label, tx + (70 if tx > x else -70), ty + 10, 30, (*WHT, a), 'Space Mono', 'l' if tx > x else 'r')


def grid(c, t):
    c.save(); c.set_line_width(1)
    for k in range(-40, 41):
        a = 0.06
        c.move_to(W / 2 + k * 60 - 2000 * 0.866, 1100 - 2000 * 0.5 + k * 0); c.line_to(W / 2 + k * 60 + 2000 * 0.866, 1100 + 2000 * 0.5)
        c.move_to(W / 2 + k * 60 + 2000 * 0.866, 1100 - 2000 * 0.5); c.line_to(W / 2 + k * 60 - 2000 * 0.866, 1100 + 2000 * 0.5)
    c.set_source_rgba(*AMB, 0.05); c.stroke(); c.restore()
    g = cairo.RadialGradient(W / 2, 850, 200, W / 2, 900, 1200); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.75)
    c.set_source(g); c.paint()


# ---------- HUD ----------
def hud(c, t, sg, readout):
    c.set_source_rgba(*AMB, 1); c.arc(58, 150, 9, 0, 2 * math.pi); c.fill()
    txt(c, "DÉCODÉ · FICHE 01", 80, 160, 28, (*AMB, 1), 'Space Mono')
    txt(c, "MASQUE À OXYGÈNE", 48, 212, 38, (*WHT, 1), 'Oswald')
    ph = PHASE[sg['scene']]
    for k, lab in enumerate(("01 MENACE", "02 AUTOPSIE", "03 RÉPONSE")):
        txt(c, lab, 48 + k * 250, 262, 24, (*(AMB if k == ph else DIM), 1 if k == ph else 0.6), 'Space Mono')
        if k == ph: c.set_source_rgba(*AMB, 1); c.rectangle(48 + k * 250, 274, 190, 3); c.fill()
    if readout:
        lab, val, col = readout
        txt(c, lab, W - 48, 128, 24, (*DIM, 1), 'Space Mono', 'r')
        txt(c, val, W - 48, 190, 58, (*col, 1), 'Oswald', 'r')


# ---------- sous-titres ----------
KEY = dict(AMB=['oxygène', 'lucidité', 'masque', 'chlorate', 'goupille', 'percuteur', 'amorce', 'bougie', 'pur', 'sac', 'trente', 'trentaine', 'douze', 'vingt', 'trois', 'normal', 'normalement', 'quinze', 'minutes'],
           RED=['bang', 'alarme', 'manuel', 'brûler', 'brûlé', 'degrés', 'morts', 'sèche', '121', '200', 'confondent', 'panne'],
           CYA=['respire', 'respirable', 'air', 'descendent'])


def chunks(show, n=4):
    show = re.sub(r' ([?!:;»])', ' \\1', show)
    w = show.split(); out = []; cur = []
    for x in w:
        cur.append(x)
        if len(cur) >= n or x.endswith(('.', '?', '!', ',', ':')): out.append(' '.join(cur)); cur = []
    if cur: out.append(' '.join(cur))
    return out


CH = []
for sg in SEG:
    cs = chunks(sg['p']['show']); tot = sum(len(x) for x in cs); acc = 0
    for x in cs:
        a = sg['vt'] + sg['dur'] * acc / tot; acc += len(x); CH.append((a, sg['vt'] + sg['dur'] * acc / tot, x))


def word_col(w):
    k = w.lower().strip('.,?!:;«» ')
    for col, lst in (('RED', KEY['RED']), ('CYA', KEY['CYA']), ('AMB', KEY['AMB'])):
        if any(k.startswith(x.lower()) for x in lst): return dict(RED=RED, CYA=CYA, AMB=AMB)[col]
    return WHT


def subtitles(c, t):
    cur = [x for x in CH if x[0] <= t < x[1] + 0.05]
    if not cur: return
    a, b, s = cur[-1]; s = s.upper(); size = 92
    F(c, size); words = s.split(' '); lines = []; line = ''
    for w_ in words:
        tst = (line + ' ' + w_).strip()
        if c.text_extents(tst.replace(' ', ' ')).x_advance > 960 and line: lines.append(line); line = w_
        else: line = tst
    lines.append(line)
    pop = 1 + 0.06 * max(0, 1 - (t - a) / 0.12)
    y = 1560 - (len(lines) - 1) * 52
    for ln in lines:
        F(c, size); wd = c.text_extents(ln.replace(' ', ' ')).x_advance; x = W / 2 - wd * pop / 2
        for w_ in ln.split(' '):
            F(c, size * pop); c.move_to(x, y); c.text_path(w_.replace(' ', ' '))
            c.set_source_rgba(0, 0, 0, 0.85); c.set_line_width(10); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
            c.set_source_rgba(*word_col(w_), 1); c.fill(); c.new_path()
            x += c.text_extents(w_.replace(' ', ' ') + ' ').x_advance
        y += 104


# ---------- éléments ----------
def seat_and_bin(c, I, t, lt, door=0.0, drop=0.0, n_masks=1, fog=0.0):
    box(c, I, -1.2, -1.6, 0, 2.4, 3.2, 0.6, DIM, 0.8, 0.04)                    # assise
    box(c, I, 0.9, -1.6, 0.6, 0.3, 3.2, 2.0, DIM, 0.8, 0.04)                    # dossier
    box(c, I, -1.6, -2.0, 4.6, 3.0, 4.0, 1.0, AMB, 1, 0.05)                     # coffre / PSU
    # porte qui bascule
    P = I.p; ang = door * 1.3
    z = 4.6; pts = [P(-1.6, -1.2, z), P(-1.6, 1.2, z), P(-1.6 + 1.4 * math.cos(ang), 1.2, z - 1.4 * math.sin(ang)), P(-1.6 + 1.4 * math.cos(ang), -1.2, z - 1.4 * math.sin(ang))]
    def d(): poly(c, pts)
    glow_path(c, d, AMB, 1, 2.2)
    for m in range(n_masks):
        yy = -0.6 + 1.2 * m if n_masks > 1 else 0.0
        dz = 2.6 * eo(drop) + 0.12 * math.sin(lt * 5 + m) * drop
        mx, my, mz = -0.8 + 0.15 * math.sin(lt * 3 + m) * drop, yy, 4.6 - dz
        def tube(): c.move_to(*P(-0.8, yy, 4.6)); c.curve_to(*P(-0.9, yy, 4.6 - dz * 0.4), *P(-0.7, yy, 4.6 - dz * 0.7), *P(mx, my, mz + 0.3))
        if drop > 0:
            glow_path(c, tube, WHT, 0.8, 1.5)
            cyl(c, I, mx, my, mz - 0.25, 0.35, 0.3, AMB, 1, 0.25)
    if fog > 0:
        r = random.Random(4)
        for k in range(60):
            x = r.uniform(80, 1000); y = r.uniform(380, 1300) + math.sin(t + k) * 10; rad = r.uniform(30, 110)
            g = cairo.RadialGradient(x, y, 1, x, y, rad); g.add_color_stop_rgba(0, 1, 1, 1, 0.10 * fog); g.add_color_stop_rgba(1, 1, 1, 1, 0)
            c.set_source(g); c.arc(x, y, rad, 0, 2 * math.pi); c.fill()


def jet_side(c, x, y, s, col, a=1.0, ang=0.0):
    pts = [(-1, 0), (0.9, 0), (1.05, 0.05), (0.9, 0.1), (-0.85, 0.1), (-1, 0.42), (-0.86, 0.42), (-0.7, 0.1)]
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    def d(): poly(c, [(px, -py) for px, py in pts])
    c.restore()
    c.save(); c.translate(x, y); c.rotate(ang)
    poly(c, [(px * s, -py * s) for px, py in pts]); c.set_source_rgba(*col, 0.08 * a); c.fill()
    for lw, al in ((14, 0.1), (6, 0.25), (2.5, 1)):
        poly(c, [(px * s, -py * s) for px, py in pts]); c.set_source_rgba(*col, a * al); c.set_line_width(lw); c.stroke()
    c.move_to(-0.1 * s, -0.04 * s); c.line_to(-0.35 * s, 0.22 * s); c.line_to(-0.2 * s, 0.22 * s); c.line_to(0.15 * s, -0.04 * s)
    c.set_source_rgba(*col, a); c.set_line_width(2.5); c.stroke()
    for k in range(10): c.set_source_rgba(*col, 0.7 * a); c.arc((0.7 - k * 0.13) * s, -0.06 * s, 3, 0, 2 * math.pi); c.fill()
    c.restore()


def stamp(c, x, y, s, col, a, k=1.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(-0.05); c.scale(k, k)
    F(c, 44); e = c.text_extents(s); wdt = e.x_advance + 50
    c.rectangle(-wdt / 2, -42, wdt, 64); c.set_source_rgba(*col, 0.15 * a); c.fill()
    c.rectangle(-wdt / 2, -42, wdt, 64); c.set_source_rgba(*col, a); c.set_line_width(4); c.stroke()
    c.move_to(-e.x_advance / 2, 6); c.set_source_rgba(*col, a); c.show_text(s); c.new_path(); c.restore()


def generator(c, I, lt, explode=0.0, burn=-1.0, heat=0.0, labels=0.0, flow=0.0):
    """Générateur chimique (axe x) éclaté le long de l'axe."""
    e = explode
    xs = dict(cord=-3.2 - 1.4 * e, pin=-2.6 - 1.0 * e, striker=-2.2 - 0.6 * e, primer=-1.75 - 0.25 * e, core=-1.5, filt=1.6 + 0.6 * e, out=2.0 + 1.1 * e)
    hc = (1.0, 0.25 + 0.4 * (1 - heat), 0.1 + 0.1 * (1 - heat))
    shell_col = tuple(AMB[i] * (1 - heat) + hc[i] * heat for i in range(3))
    A, B = cyl(c, I, xs['core'] - 0.05, 0, 0, 0.75, 3.1, shell_col, 1, 0.05 + 0.25 * heat, axis='x')
    cyl(c, I, xs['core'] + 0.1, 0, 0, 0.55, 2.8, DIM if burn < 0 else WHT, 0.9, 0.08, axis='x', w=1.6)       # bloc de chlorate
    if burn >= 0:      # front de combustion
        xb = xs['core'] + 0.1 + 2.8 * min(1, burn)
        cyl(c, I, xs['core'] + 0.1, 0, 0, 0.55, max(0.02, 2.8 * min(1, burn)), RED, 0.9, 0.35, axis='x', w=1.6)
        P = I.p; cx_, cy_ = P(xb, 0, 0)
        g = cairo.RadialGradient(cx_, cy_, 2, cx_, cy_, 120); g.add_color_stop_rgba(0, 1, 0.7, 0.2, 0.8); g.add_color_stop_rgba(1, 1, 0.4, 0.1, 0)
        c.set_source(g); c.arc(cx_, cy_, 120, 0, 2 * math.pi); c.fill()
    cyl(c, I, xs['primer'], 0, 0, 0.3, 0.12, AMB, 1, 0.2, axis='x', w=1.8)
    cyl(c, I, xs['striker'], 0, 0, 0.12, 0.45, WHT, 1, 0.2, axis='x', w=1.8)
    cyl(c, I, xs['pin'], 0, 0, 0.06, 0.35, RED, 1, 0.3, axis='x', w=1.8)
    P = I.p
    def cord(): c.move_to(*P(xs['pin'], 0, 0)); c.curve_to(*P(xs['cord'] + 0.3, 0.3, -0.5), *P(xs['cord'], 0.5, -1.2), *P(xs['cord'] - 0.2, 0.6, -2.0))
    glow_path(c, cord, WHT, 0.8, 1.6)
    cyl(c, I, xs['filt'], 0, 0, 0.7, 0.18, CYA, 1, 0.12, axis='x', w=1.8)
    cyl(c, I, xs['out'], 0, 0, 0.12, 0.8, CYA, 1, 0.2, axis='x', w=1.8)
    if flow > 0:
        r = random.Random(9)
        for k in range(40):
            u = (lt * 0.6 + r.random()) % 1; x = xs['filt'] + u * 2.2; yy = r.uniform(-0.1, 0.1); zz = r.uniform(-0.1, 0.1)
            px, py = P(x, yy, zz); c.set_source_rgba(*CYA, flow * (1 - u)); c.arc(px, py, 5, 0, 2 * math.pi); c.fill()
    L = [('cord', -0.0, "CORDON", (60, 260)), ('pin', 0.08, "GOUPILLE", (-40, -230)), ('striker', 0.16, "PERCUTEUR", (-20, 230)),
         ('primer', 0.24, "AMORCE", (40, -330)), ('core', 0.36, "CHLORATE DE SODIUM", (120, 300)), ('filt', 0.5, "FILTRE", (40, -260)), ('out', 0.62, "SORTIE O2", (60, 220))]
    for key, d0, lab, (ox, oy) in L:
        a = ease((labels - d0) / 0.12)
        if a > 0:
            px, py = P(xs[key] + (1.4 if key == 'core' else 0.1), 0, 0.5 if key != 'cord' else -1.6)
            callout(c, px, py, px + ox * 0.6, py + oy * 0.55, lab, AMB if key != 'core' else RED, a)


def gauge(c, x, y, r, val, vmax, lab, unit, col, a=1.0):
    c.set_line_width(14); c.set_source_rgba(1, 1, 1, 0.12 * a); c.arc(x, y, r, math.pi * 0.75, math.pi * 2.25); c.stroke()
    f = min(1, val / vmax); c.set_source_rgba(*col, a); c.arc(x, y, r, math.pi * 0.75, math.pi * (0.75 + 1.5 * f)); c.stroke()
    txt(c, f"{val:.0f}{unit}", x, y + 20, 74, (*col, a), 'Oswald', 'c')
    txt(c, lab, x, y + 80, 26, (*DIM, a), 'Space Mono', 'c')


# ---------- scènes ----------
def sc_hook(c, t, sg, lt, u):
    I = Iso(W / 2 + 40, 1060, 115)
    seat_and_bin(c, I, t, lt, door=ease((lt - 1.2) / 0.4), drop=ease((lt - 1.4) / 0.8), n_masks=1, fog=ease((lt - 1.0) / 0.3) * (1 - 0.6 * ease((lt - 3) / 2)))
    if lt < 1.3:  # carte titre
        a = 1 - ease((lt - 1.0) / 0.3)
        c.set_source_rgba(*BG, 0.85 * a); c.paint()
        txt(c, "MASQUE", W / 2, 820, 190, (*WHT, a), 'Oswald', 'c'); txt(c, "À OXYGÈNE", W / 2, 1010, 150, (*AMB, a), 'Oswald', 'c')
        txt(c, "FICHE 01 · DÉCODÉ", W / 2, 1090, 34, (*DIM, a), 'Space Mono', 'c')
    alt = 8000 + 6500 * ease((lt - 0.8) / 1.0)
    rd = ("ALTITUDE CABINE", f"{alt:,.0f} FT".replace(',', ' '), RED if alt > 14000 else AMB)
    if lt > sg['dur'] * 0.75:
        left = max(0, 30 - (lt - sg['dur'] * 0.75) * 6); rd = ("LUCIDITÉ RESTANTE", f"00:{left:02.0f}", RED)
    return rd


def sc_story(c, t, sg, lt, u):
    jet_side(c, 200 + 680 * u, 1050 - 420 * u, 300, WHT, 1, -0.35)
    stamp(c, W / 2, 470, "HISTOIRE VRAIE · 14 AOÛT 2005", RED, ease(lt / 0.3), 1 + 0.3 * max(0, 1 - lt / 0.2))
    if u > 0.45:     # sélecteur pressurisation
        a = ease((u - 0.45) / 0.1); x0, y0 = 330, 1160
        c.rectangle(x0, y0, 420, 130); c.set_source_rgba(1, 1, 1, 0.05 * a); c.fill()
        c.rectangle(x0, y0, 420, 130); c.set_source_rgba(*DIM, a); c.set_line_width(2); c.stroke()
        txt(c, "PRESSURISATION", x0 + 20, y0 + 40, 26, (*DIM, a), 'Space Mono')
        txt(c, "AUTO", x0 + 40, y0 + 105, 46, (*DIM, 0.5 * a), 'Oswald')
        bl = 1 if int(lt * 3) % 2 else 0.5
        txt(c, "MAN", x0 + 260, y0 + 105, 46, (*RED, a * bl), 'Oswald')
    alt = 2000 + 10000 * u
    return ("ALTITUDE CABINE", f"{alt:,.0f} FT".replace(',', ' '), RED if alt > 10000 else AMB)


def sc_alarm(c, t, sg, lt, u):
    I = Iso(W / 2 + 40, 1000, 85)
    for k in range(3):
        for j in range(2):
            I2 = Iso(W / 2 - 250 + k * 250 + j * 60, 820 + j * 260, 55)
            seat_and_bin(c, I2, t, lt + k, door=ease((lt - 1.5 - 0.1 * k) / 0.3), drop=ease((lt - 1.7 - 0.1 * k) / 0.7))
    pul = (lt * 1.6) % 1
    for r_ in range(3):
        rr = 60 + ((pul + r_ / 3) % 1) * 200
        c.set_source_rgba(*RED, 0.6 * (1 - (pul + r_ / 3) % 1)); c.set_line_width(5); c.arc(W / 2, 470, rr, 0, 2 * math.pi); c.stroke()
    txt(c, "!", W / 2, 510, 120, (*RED, 1), 'Oswald', 'c')
    return ("ALARME", "ALT CABINE", RED)


def sc_open(c, t, sg, lt, u):
    I = Iso(W / 2 + 20, 960, 118)
    lid = ease(lt / 0.8); up = ease((lt - 0.8) / 0.8); ex = ease((lt - 1.6) / 1.4)
    box(c, Iso(W / 2 + 20, 1050, 105), -2.4, -1.2, -1.2, 4.8, 2.4, 0.9, DIM, 1 - 0.7 * up, 0.04)
    c.save(); c.translate(0, -260 * up)
    generator(c, I, lt, explode=ex, labels=(lt - 2.0) / 3.2 if lt > 2.0 else -1)
    c.restore()
    if lt < 1.4:
        stamp(c, W / 2, 470, "PAS DE BOUTEILLE", AMB, ease((lt - 0.2) / 0.3))
    return ("COMPOSANTS", f"{min(7, max(0, int((lt - 2.0) / 3.2 * 11) + 1)) if lt > 2 else 0} / 7", AMB)


def sc_chrono(c, t, sg, lt, u):
    I = Iso(W / 2 + 30, 900, 140)
    burn = max(0, (u - 0.45) / 0.55) * 0.6 if u > 0.45 else -1
    generator(c, I, lt, explode=0.35 * (1 - ease(u / 0.3)), burn=burn, flow=ease((u - 0.55) / 0.1))
    # frise chrono
    x0, x1, y = 90, 990, 1300
    c.set_source_rgba(*DIM, 0.6); c.rectangle(x0, y, x1 - x0, 4); c.fill()
    marks = [(0.12, "0 s", "TU TIRES"), (0.26, "0,1 s", "GOUPILLE"), (0.38, "0,2 s", "AMORCE"), (0.55, "1 s", "O2")]
    for (mu, tl, lab) in marks:
        a = ease((u - mu) / 0.05); x = x0 + (x1 - x0) * (marks.index((mu, tl, lab)) + 0.5) / len(marks)
        c.set_source_rgba(*(AMB if a > 0 else DIM), max(0.3, a)); c.arc(x, y + 2, 12, 0, 2 * math.pi); c.fill()
        txt(c, tl, x, y - 30, 30, (*WHT, max(0.3, a)), 'Space Mono', 'c'); txt(c, lab, x, y + 60, 28, (*AMB, a), 'Space Mono', 'c')
    secs = max(0, (u - 0.12) * 4)
    return ("CHRONO", f"T+{secs:0.1f} s".replace('.', ','), AMB)


def sc_heat(c, t, sg, lt, u):
    I = Iso(W / 2 + 30, 840, 140)
    hv = ease(u / 0.6)
    generator(c, I, lt, burn=0.6 + 0.3 * u, heat=hv, flow=1)
    for k in range(6):
        x = 300 + k * 100; ph = (lt * 0.8 + k * 0.17) % 1
        c.move_to(x, 760 - ph * 200)
        for s_ in range(8): c.line_to(x + 12 * math.sin(s_ + lt * 4 + k), 760 - ph * 200 - s_ * 15)
        c.set_source_rgba(1, 0.5, 0.2, 0.4 * hv * (1 - ph)); c.set_line_width(3); c.stroke()
    gauge(c, W / 2, 1220, 120, 260 * hv, 300, "TEMPÉRATURE DU BOÎTIER", "°C", RED)
    if u > 0.6: stamp(c, W / 2, 470, "ODEUR DE BRÛLÉ = NORMAL", GRN, ease((u - 0.6) / 0.1))
    return ("BOÎTIER", f"{260 * hv:.0f} °C", RED)


def sc_bag(c, t, sg, lt, u):
    cx, cy = W / 2, 900
    # masque (vue de face) + sac : attendu (pointillé) vs réel (à plat)
    for lw, al in ((14, 0.1), (5, 0.3), (2.5, 1)):
        c.set_source_rgba(*AMB, al); c.set_line_width(lw); c.arc(cx, cy - 120, 120, 0, 2 * math.pi); c.stroke()
    c.set_dash([14, 10]); c.set_source_rgba(*DIM, 0.8); c.set_line_width(3)
    c.save(); c.translate(cx, cy + 170); c.scale(1, 1.25); c.arc(0, 0, 140, 0, 2 * math.pi); c.restore(); c.stroke(); c.set_dash([])
    txt(c, "CE QUE TU ATTENDS", cx + 190, cy + 60, 26, (*DIM, 1), 'Space Mono')
    c.save(); c.translate(cx, cy + 120); c.scale(1, 0.25 + 0.05 * math.sin(lt * 2)); c.arc(0, 0, 120, 0, 2 * math.pi); c.restore()
    c.set_source_rgba(*WHT, 0.1); c.fill_preserve(); c.set_source_rgba(*WHT, 1); c.set_line_width(3); c.stroke()
    txt(c, "LA RÉALITÉ", cx + 190, cy + 140, 26, (*WHT, 1), 'Space Mono')
    # flux + indicateur vert
    r = random.Random(3)
    for k in range(30):
        uu = (lt * 0.7 + r.random()) % 1; y = cy + 400 - uu * 380; x = cx + r.uniform(-12, 12)
        c.set_source_rgba(*CYA, 0.9 * (1 - uu)); c.arc(x, y, 5, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(*WHT, 0.6); c.set_line_width(3); c.move_to(cx, cy + 420); c.line_to(cx, cy + 20); c.stroke()
    ind = ease((u - 0.35) / 0.1)
    c.set_source_rgba(*(GRN if ind > 0.5 else DIM), 1); c.rectangle(cx - 30, cy + 300, 60, 40); c.fill()
    txt(c, "INDICATEUR DE DÉBIT", cx - 50, cy + 330, 26, (*(GRN if ind > 0.5 else DIM), 1), 'Space Mono', 'r')
    if u > 0.45: stamp(c, W / 2, 470, "SAC À PLAT ≠ PANNE", GRN, ease((u - 0.45) / 0.1))
    return ("DÉBIT O2", "OK" if ind > 0.5 else "…", GRN)


def sc_descent(c, t, sg, lt, u):
    x0, y0, x1, y1 = 140, 520, 980, 1250
    c.set_source_rgba(*DIM, 0.6); c.set_line_width(2); c.move_to(x0, y0); c.line_to(x0, y1); c.line_to(x1, y1); c.stroke()
    for alt, lab in ((34000, "34 000 FT"), (10000, "10 000 FT")):
        y = y1 - (y1 - y0) * alt / 36000
        c.set_dash([8, 8]); c.set_source_rgba(*DIM, 0.5); c.move_to(x0, y); c.line_to(x1, y); c.stroke(); c.set_dash([])
        txt(c, lab, x0 + 10, y - 12, 26, (*DIM, 1), 'Space Mono')
    p = ease(u / 0.8); n = 60
    def curve():
        for k in range(int(n * p) + 1):
            f = k / n; x = x0 + (x1 - x0) * f; alt = 34000 - 24000 * min(1, f / 0.55)
            y = y1 - (y1 - y0) * alt / 36000
            (c.move_to if k == 0 else c.line_to)(x, y)
    glow_path(c, curve, CYA, 1, 4)
    yair = y1 - (y1 - y0) * 10000 / 36000
    if u > 0.55: txt(c, "AIR RESPIRABLE", x1 - 10, yair + 50, 34, (*GRN, ease((u - 0.55) / 0.1)), 'Oswald', 'r')
    # réserve O2
    left = 1 - 0.75 * p
    c.rectangle(x0, 1310, (x1 - x0), 34); c.set_source_rgba(1, 1, 1, 0.1); c.fill()
    c.rectangle(x0, 1310, (x1 - x0) * left, 34); c.set_source_rgba(*AMB, 1); c.fill()
    txt(c, "RÉSERVE O2 : 12 À 20 MIN", x0, 1390, 28, (*AMB, 1), 'Space Mono')
    return ("ALTITUDE", f"{34000 - 24000 * min(1, p / 0.55 if p < 0.55 else 1):,.0f} FT".replace(',', ' '), CYA)


def sc_helios(c, t, sg, lt, u):
    cx, cy = W / 2, 880
    c.set_source_rgba(*DIM, 0.4); c.set_line_width(2); c.arc(cx, cy, 260, 0, 2 * math.pi); c.stroke()
    c.set_source_rgba(*WHT, 0.9); c.arc(cx, cy, 8, 0, 2 * math.pi); c.fill(); txt(c, "ATHÈNES", cx + 20, cy + 10, 30, (*WHT, 0.9), 'Space Mono')
    a = lt * 1.2
    for k in range(25):
        aa = a - k * 0.06; c.set_source_rgba(*AMB, 0.5 * (1 - k / 25)); c.arc(cx + 260 * math.cos(aa), cy + 260 * math.sin(aa), 5, 0, 2 * math.pi); c.fill()
    px, py = cx + 260 * math.cos(a), cy + 260 * math.sin(a)
    c.save(); c.translate(px, py); c.rotate(a + math.pi / 2); poly(c, [(0, -26), (14, 12), (0, 4), (-14, 12)]); c.set_source_rgba(*AMB, 1); c.fill(); c.restore()
    fuel = max(0, 1 - u * 1.25)
    gauge(c, cx, 1300, 100, fuel * 100, 100, "CARBURANT", " %", RED if fuel < 0.25 else AMB)
    if u > 0.82:
        aa = ease((u - 0.82) / 0.08); c.set_source_rgba(*BG, 0.9 * aa); c.paint()
        txt(c, "121", W / 2, 950, 260, (*WHT, aa), 'Oswald', 'c'); txt(c, "VICTIMES · 14 AOÛT 2005", W / 2, 1030, 34, (*DIM, aa), 'Space Mono', 'c')
    return ("PILOTE AUTO", f"{int(70 * min(1, u * 1.2))} MIN", AMB)


def sc_outro(c, t, sg, lt, u):
    I = Iso(W / 2 + 40, 1060, 115)
    seat_and_bin(c, I, t, lt, door=1, drop=1)
    if u < 0.55:
        stamp(c, W / 2, 470, "TON MASQUE D'ABORD", AMB, ease(lt / 0.3), 1 + 0.3 * max(0, 1 - lt / 0.2))
    else:
        a = ease((u - 0.55) / 0.1)
        c.set_source_rgba(*BG, 0.7 * a); c.paint()
        c.rectangle(140, 620, 800, 360); c.set_source_rgba(1, 1, 1, 0.04 * a); c.fill()
        c.rectangle(140, 620, 800, 360); c.set_source_rgba(*AMB, a); c.set_line_width(3); c.stroke()
        txt(c, "FICHE 02", W / 2, 720, 40, (*DIM, a), 'Space Mono', 'c')
        txt(c, "LES HUBLOTS", W / 2, 840, 110, (*WHT, a), 'Oswald', 'c')
        stamp(c, W / 2, 930, "CLASSÉ", RED, a)
    return ("ABONNE-TOI", "FICHE 02", AMB)


SC = dict(hook=sc_hook, story=sc_story, alarm=sc_alarm, open=sc_open, chrono=sc_chrono, heat=sc_heat, bag=sc_bag, descent=sc_descent, helios=sc_helios, outro=sc_outro)


def frame(t):
    sg = next((x for x in SEG if x['t0'] <= t < x['end']), SEG[-1]); lt = t - sg['t0']
    u = min(1, max(0, (t - sg['vt']) / max(0.1, sg['dur'] + 0.3)))
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    c.set_source_rgb(*BG); c.paint(); grid(c, t)
    k = 1 + 0.03 * ease(lt / max(1, sg['end'] - sg['t0']))       # dérive lente (pas de tremblement)
    c.save(); c.translate(W / 2, 900); c.scale(k, k); c.translate(-W / 2, -900)
    rd = SC[sg['scene']](c, t, sg, lt, u)
    c.restore()
    if sg['i'] > 0 and lt < 0.25:   # transition : balayage lumineux
        y = H * (lt / 0.25); c.set_source_rgba(*AMB, 0.5); c.rectangle(0, y - 3, W, 6); c.fill()
        c.set_source_rgba(*BG, 0.6 * (1 - lt / 0.25)); c.rectangle(0, y, W, H - y); c.fill()
    hud(c, t, sg, rd); subtitles(c, t)
    c.set_source_rgba(*AMB, 1); c.rectangle(0, H - 10, W * t / TOTAL, 10); c.fill()
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
