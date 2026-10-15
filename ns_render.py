"""Série « LA SCIENCE DU VOL » : motion design néon (fond étoilé noir, bleu néon, jaune, sous-titres karaoké mot à mot).
Usage : DL=dl/<slug> python3 ns_render.py [stills t1 ...]   (cfg.py : SERIES, EP, NEXT, SCENES[type, num, title, say, show, ...], END_HOLD ; durs.json)"""
import cairo, json, math, os, re, subprocess, sys, random, importlib.util

W, H, FPS = 1080, 1920, 30
D = os.environ.get('DL', 'dl/ns_altitude').rstrip('/') + '/'
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

BG = (0.020, 0.027, 0.055)                 # #05070E
BLU = (0.165, 0.46, 1.0)                   # #2A75FF
CYA = (0.30, 0.70, 1.0)                    # #4DB3FF
YLW = (1.0, 0.86, 0.0)                     # #FFDB00
RED = (1.0, 0.23, 0.19)                    # #FF3B30
ORG = (1.0, 0.48, 0.0)
WHT = (0.97, 0.98, 1.0)
DIM = (0.45, 0.55, 0.75)
FONT = 'Montserrat'; BIG = 'Bebas Neue'


def ease(u):
    u = min(max(u, 0), 1); return u * u * (3 - 2 * u)


def ap(u, a, b):
    return ease((u - a) / max(1e-3, b - a))


def F(c, size, fam=FONT, bold=True):
    c.select_font_face(fam, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL); c.set_font_size(size)


def txt(c, s, x, y, size, rgba, fam=FONT, anchor='l', bold=True, outline=0, glow=0):
    F(c, size, fam, bold); e = c.text_extents(s)
    if anchor == 'c': x -= e.x_advance / 2
    elif anchor == 'r': x -= e.x_advance
    if glow:
        for k in (14, 8, 4):
            c.move_to(x, y); c.text_path(s); c.set_source_rgba(rgba[0], rgba[1], rgba[2], rgba[3] * glow * 0.12); c.set_line_width(k); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()
    if outline:
        c.move_to(x, y); c.text_path(s); c.set_source_rgba(0, 0, 0, rgba[3] * 0.9); c.set_line_width(outline); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()
    c.move_to(x, y); c.text_path(s); c.set_source_rgba(*rgba); c.fill()
    return e.x_advance


def glow(c, draw, col, a=1.0, w=3.0):
    for k, al in ((w * 6, 0.07), (w * 3, 0.14), (w * 1.6, 0.30), (w, 1.0)):
        draw(); c.set_source_rgba(*col, a * al); c.set_line_width(k); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()


def poly(c, pts, close=False):
    c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    if close: c.close_path()


# ---------- fond ----------
random.seed(7)
STARS = [(random.random() * W, random.random() * H, random.choice((1, 1, 1, 1.5, 2, 2.6)), random.random() * 6.28, random.random()) for _ in range(260)]


def background(c, t):
    c.set_source_rgb(*BG); c.paint()
    g = cairo.RadialGradient(W / 2, 820, 50, W / 2, 820, 1000); g.add_color_stop_rgba(0, *BLU, 0.10); g.add_color_stop_rgba(1, *BLU, 0)
    c.set_source(g); c.paint()
    for x, y, r, ph, sp in STARS:
        yy = (y + t * (6 + 14 * sp)) % H
        a = 0.25 + 0.55 * (0.5 + 0.5 * math.sin(t * (1 + 2 * sp) + ph))
        c.set_source_rgba(0.8, 0.88, 1, a * (0.5 + r / 5)); c.arc(x, yy, r, 0, 6.283); c.fill()


# ---------- éléments ----------
def plane_side(c, x, y, s, col, a=1.0, w=3.0, fill=0.08):
    """Avion de ligne de profil (nez à droite), longueur ≈ 2s."""
    def body():
        c.new_path(); c.move_to(x - 0.92 * s, y - 0.06 * s)
        c.line_to(x + 0.78 * s, y - 0.09 * s); c.curve_to(x + 0.95 * s, y - 0.09 * s, x + 1.0 * s, y - 0.01 * s, x + 1.0 * s, y + 0.02 * s)
        c.curve_to(x + 0.98 * s, y + 0.08 * s, x + 0.9 * s, y + 0.1 * s, x + 0.78 * s, y + 0.1 * s)
        c.line_to(x - 0.7 * s, y + 0.1 * s); c.line_to(x - 1.0 * s, y - 0.04 * s); c.close_path()
    body(); c.set_source_rgba(*col, a * fill); c.fill()
    glow(c, body, col, a, w)
    glow(c, lambda: poly(c, [(x - 0.72 * s, y - 0.07 * s), (x - 0.95 * s, y - 0.42 * s), (x - 1.05 * s, y - 0.42 * s), (x - 0.98 * s, y - 0.05 * s)]), col, a, w)
    glow(c, lambda: poly(c, [(x - 0.86 * s, y + 0.0 * s), (x - 1.12 * s, y + 0.06 * s), (x - 1.05 * s, y + 0.08 * s), (x - 0.78 * s, y + 0.05 * s)]), col, a, w * 0.8)
    glow(c, lambda: poly(c, [(x + 0.18 * s, y + 0.06 * s), (x - 0.22 * s, y + 0.26 * s), (x - 0.30 * s, y + 0.26 * s), (x - 0.08 * s, y + 0.06 * s)]), col, a, w * 0.8)
    def eng():
        c.new_path(); c.rectangle(x - 0.02 * s, y + 0.13 * s, 0.24 * s, 0.09 * s)
    glow(c, eng, col, a, w * 0.8)
    c.set_source_rgba(*col, a * 0.8)
    for k in range(16): c.arc(x + (-0.6 + k * 0.08) * s, y - 0.02 * s, 0.012 * s, 0, 6.283); c.fill()


def delta_side(c, x, y, s, col, a=1.0, w=3.0):
    """Concorde stylisé de profil (nez à droite)."""
    def body():
        c.new_path(); poly(c, [(x - 1.0 * s, y), (x + 0.85 * s, y - 0.03 * s), (x + 1.12 * s, y + 0.03 * s), (x + 0.85 * s, y + 0.05 * s), (x - 0.95 * s, y + 0.06 * s)], True)
    body(); c.set_source_rgba(*col, a * 0.08); c.fill(); glow(c, body, col, a, w)
    glow(c, lambda: poly(c, [(x - 0.75 * s, y), (x - 0.98 * s, y - 0.33 * s), (x - 1.04 * s, y - 0.33 * s), (x - 0.96 * s, y)]), col, a, w)
    glow(c, lambda: poly(c, [(x + 0.35 * s, y + 0.06 * s), (x - 0.85 * s, y + 0.13 * s), (x - 0.95 * s, y + 0.07 * s)]), col, a, w * 0.8)


def gauge(c, x, y, r, frac, lab, val, col, a=1.0):
    a0, a1 = math.radians(135), math.radians(405)
    glow(c, lambda: (c.new_path(), c.arc(x, y, r, a0, a1)), DIM, a * 0.5, 3)
    glow(c, lambda: (c.new_path(), c.arc(x, y, r, a0, a0 + (a1 - a0) * max(0.001, frac))), col, a, 7)
    for k in range(11):
        an = a0 + (a1 - a0) * k / 10; c.move_to(x + math.cos(an) * (r - 22), y + math.sin(an) * (r - 22)); c.line_to(x + math.cos(an) * (r - 8), y + math.sin(an) * (r - 8))
    c.set_source_rgba(*WHT, a * 0.6); c.set_line_width(3); c.stroke()
    an = a0 + (a1 - a0) * frac
    glow(c, lambda: (c.new_path(), c.move_to(x, y), c.line_to(x + math.cos(an) * (r - 30), y + math.sin(an) * (r - 30))), YLW, a, 4)
    c.set_source_rgba(*YLW, a); c.arc(x, y, 9, 0, 6.283); c.fill()
    txt(c, val, x, y + r * 0.62, r * 0.42, (*WHT, a), BIG, 'c')
    txt(c, lab, x, y + r + 52, 30, (*CYA, a), FONT, 'c')


def arrow(c, x0, y0, x1, y1, col, a=1.0, w=5, head=26):
    an = math.atan2(y1 - y0, x1 - x0)
    glow(c, lambda: (c.new_path(), c.move_to(x0, y0), c.line_to(x1 - math.cos(an) * head * 0.6, y1 - math.sin(an) * head * 0.6)), col, a, w)
    c.move_to(x1, y1); c.line_to(x1 - head * math.cos(an - 0.45), y1 - head * math.sin(an - 0.45)); c.line_to(x1 - head * math.cos(an + 0.45), y1 - head * math.sin(an + 0.45)); c.close_path()
    c.set_source_rgba(*col, a); c.fill()


def tri(c, x, y, s, up, col, a=1.0):
    d = -1 if up else 1
    c.move_to(x - s, y - d * s * 0.5); c.line_to(x + s, y - d * s * 0.5); c.line_to(x, y + d * s * 0.8); c.close_path(); c.set_source_rgba(*col, a); c.fill()


def panel(c, x, y, w, h, col, a=1.0, fill=0.06):
    def p(): c.new_path(); c.rectangle(x, y, w, h)
    p(); c.set_source_rgba(*col, a * fill); c.fill(); glow(c, p, col, a, 2.5)


def cloud(c, x, y, s, a):
    c.new_path()
    for dx, dy, r in ((0, 0, 1), (0.9, 0.15, 0.75), (-0.9, 0.2, 0.7), (0.4, -0.45, 0.7), (-0.4, -0.35, 0.6)):
        c.new_sub_path(); c.arc(x + dx * s, y + dy * s, r * s, 0, 6.283)
    c.set_source_rgba(*CYA, a * 0.10); c.fill_preserve(); c.set_source_rgba(*CYA, a * 0.45); c.set_line_width(2); c.stroke()


def alt_axis(c, x, y0, y1, kmax, a, step=2):
    glow(c, lambda: (c.new_path(), c.move_to(x, y0), c.line_to(x, y1)), BLU, a, 2.5)
    for k in range(0, kmax + 1, step):
        yy = y0 + (y1 - y0) * k / kmax
        c.move_to(x - 14, yy); c.line_to(x, yy); c.set_source_rgba(*CYA, a); c.set_line_width(3); c.stroke()
        txt(c, f"{k} KM", x - 24, yy + 11, 30, (*DIM, a), FONT, 'r')


def sticker(c, name, x, y, size, a=1.0, rot=0.0):
    p = f'pipe/mascot/stickers/{name}.png'
    if not os.path.exists(p): return
    im = STK.get(name) or STK.setdefault(name, cairo.ImageSurface.create_from_png(p))
    k = size / im.get_width(); c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k)
    c.set_source_surface(im, -im.get_width() / 2, -im.get_height() / 2); c.paint_with_alpha(a); c.restore()


STK = {}


# ---------- en-tête ----------
def header(c, t, sg, lt):
    p = sg['p']
    txt(c, f"{getattr(CFG, 'SERIES', 'LA SCIENCE DU VOL')} · ÉP. {getattr(CFG, 'EP', '01')}", 54, 150, 30, (*CYA, 0.9), FONT)
    if p.get('num'):
        a = ease(lt / 0.35); x0 = 54 - 40 * (1 - a)
        c.new_path(); c.rectangle(x0, 182, 96, 96); c.set_source_rgba(*YLW, a); c.fill()
        txt(c, str(p['num']), x0 + 48, 264, 92, (0.02, 0.03, 0.06, a), BIG, 'c')
        txt(c, p['title'], x0 + 124, 262, 90, (*WHT, a), BIG, glow=1)
    elif p['type'] not in ('hook', 'plan', 'outro'):
        a = ease(lt / 0.35)
        txt(c, p['title'], 54, 262, 90, (*YLW, a), BIG, glow=1)


# ---------- sous-titres karaoké ----------
def chunks(show, n=3):
    show = re.sub(r' ([?!:;»])', ' \\1', show)
    w = show.split(); out = []; cur = []
    for x in w:
        cur.append(x)
        if len(cur) >= n or x.endswith(('.', '?', '!', ',', ':')): out.append(cur); cur = []
    if cur: out.append(cur)
    return out


WORDS = []      # (début, fin, mot, id_chunk)
CHK = []
for sg in SEG:
    cs = chunks(sg['p']['show']); allw = [w for ch in cs for w in ch]
    wt = [len(w) + 2 + (6 if w.endswith(('.', '?', '!')) else 3 if w.endswith((',', ':')) else 0) for w in allw]
    tot = sum(wt); acc = 0; k = 0
    for ch in cs:
        cid = len(CHK); ws = []
        for w in ch:
            a = sg['vt'] + sg['dur'] * acc / tot; acc += wt[k]; k += 1
            ws.append((a, sg['vt'] + sg['dur'] * acc / tot, w))
        CHK.append(ws)


def subtitles(c, t):
    cur = [ch for ch in CHK if ch[0][0] <= t < ch[-1][1] + 0.08]
    if not cur: return
    ch = cur[-1]; size = 86
    F(c, size); words = [w.upper() for _, _, w in ch]
    sp = size * 0.5
    ws = [c.text_extents(w).x_advance for w in words]
    lines = [[]]; lw = 0
    for i, w in enumerate(ws):
        if lines[-1] and lw + sp + w > 980: lines.append([]); lw = 0
        lines[-1].append(i); lw += (sp if len(lines[-1]) > 1 else 0) + w
    y = 1500 - (len(lines) - 1) * 50
    pop0 = 1 + 0.08 * max(0, 1 - (t - ch[0][0]) / 0.12)
    for ln in lines:
        tw = sum(ws[i] for i in ln) + sp * (len(ln) - 1); x = W / 2 - tw / 2
        for i in ln:
            a0, a1, _ = ch[i]; act = a0 <= t < a1 or (i == len(ch) - 1 and t >= a0)
            col = YLW if act else WHT
            s = size * ((1.04 * pop0) if act else 1.0)
            F(c, s); dw = c.text_extents(words[i]).x_advance
            xx = x + ws[i] / 2 - dw / 2
            c.move_to(xx, y); c.text_path(words[i]); c.set_source_rgba(0, 0, 0, 0.95); c.set_line_width(12); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()
            c.move_to(xx, y); c.text_path(words[i]); c.set_source_rgba(*col, 1); c.fill()
            x += ws[i] + sp
        y += 100


# ---------- scènes ----------
def sc_hook(c, t, sg, lt, u):
    p = sg['p']; a = ease(lt / 0.25)
    for k in range(2):
        x = W * (0.27 + 0.46 * k); col = YLW if k == 0 else WHT
        s = 1 + 0.05 * max(0, 1 - (lt - 0.15 * k) / 0.2)
        F(c, 150, BIG); fs = 150 * min(1, 440 / max(1, c.text_extents(p['top'][k]).x_advance))
        txt(c, p['top'][k], x, 470, fs * s, (*col, ease((lt - 0.15 * k) / 0.2)), BIG, 'c', glow=1)
        txt(c, p['sub'][k], x, 530, 32, (*CYA, ease((lt - 0.15 * k - 0.2) / 0.2)), FONT, 'c')
    c.set_source_rgba(*BLU, a * 0.8); c.rectangle(W / 2 - 1.5, 360, 3, 190); c.fill()
    b = ap(u, 0.08, 0.25)
    plane_side(c, W / 2 + 60 * (1 - b) - 30 * u, 830 - 8 * math.sin(lt * 1.3), 300, BLU, b, 3.5)
    g = ap(u, 0.45, 0.6)
    if g > 0 and p.get('gauges'):
        for k, (lab, val, fr, col) in enumerate(p['gauges']):
            gauge(c, W * (0.28 + 0.44 * k), 1150, 120, fr * ap(u, 0.45 + 0.15 * k, 0.65 + 0.15 * k), lab, val, col, ap(u, 0.45 + 0.15 * k, 0.55 + 0.15 * k))
    elif g > 0:
        gauge(c, W * 0.28, 1150, 120, 0.30 * g, "DENSITÉ DE L'AIR", f"{int(30 * g)} %", CYA, g)
        gauge(c, W * 0.72, 1150, 120, 1 - 0.75 * ap(u, 0.75, 0.95), "CONSOMMATION", "MIN" if u > 0.8 else "", YLW, g)
        if u > 0.8:
            tri(c, W * 0.72 + 110, 1050, 22, False, YLW, ap(u, 0.8, 0.85))


def sc_plan(c, t, sg, lt, u):
    for k, lab in enumerate(sg['p']['items']):
        a = ap(u, 0.08 + k * 0.14, 0.18 + k * 0.14); y = 470 + k * 190
        x0 = 140 + 60 * (1 - a)
        col = RED if k == 3 else YLW
        panel(c, x0, y, 800, 140, col if k == 3 else BLU, a)
        c.new_path(); c.rectangle(x0, y, 120, 140); c.set_source_rgba(*col, a); c.fill()
        txt(c, str(k + 1), x0 + 60, y + 112, 120, (0.02, 0.03, 0.06, a), BIG, 'c')
        txt(c, lab, x0 + 160, y + 104, 92, (*WHT, a), BIG)


def particles(c, x, y, w, h, n, seed, t, col, a):
    rr = random.Random(seed)
    for _ in range(n):
        px = x + rr.random() * w; py = y + rr.random() * h; ph = rr.random() * 6.28
        px = x + ((px - x + t * 40 * (0.5 + rr.random())) % w)
        c.set_source_rgba(*col, a * (0.6 + 0.4 * math.sin(t * 3 + ph))); c.arc(px, py + 4 * math.sin(t * 2 + ph), 5, 0, 6.283); c.fill()


def sc_air(c, t, sg, lt, u):
    a = ap(u, 0.0, 0.08)
    for k, (lab, n, col, val) in enumerate((("AU SOL", 150, CYA, "1,22 KG/M³"), ("À 11 000 M", 45, YLW, "0,36 KG/M³"))):
        x = 90 + k * 470; aa = a if k == 0 else ap(u, 0.08, 0.16)
        panel(c, x, 360, 430, 420, BLU, aa)
        particles(c, x + 10, 380, 410, 380, n, 3 + k, t, col, aa)
        txt(c, lab, x + 215, 840, 56, (*WHT, aa), BIG, 'c')
        txt(c, val, x + 215, 890, 36, (*col, aa), FONT, 'c')
    b = ap(u, 0.32, 0.42)
    if b > 0:
        c.save(); x0 = 120
        x = x0 + txt(c, "TRAÎNÉE = ½ × ", x0, 1060, 72, (*WHT, b), BIG)
        x += txt(c, "ρ", x, 1060, 80, (*YLW, b), 'DejaVu Sans', glow=1)
        txt(c, " × V² × S × Cx", x, 1060, 72, (*WHT, b), BIG); c.restore()
        xx = 120 + txt(c, "ρ", 120, 1112, 34, (*YLW, b), 'DejaVu Sans'); txt(c, " = DENSITÉ DE L'AIR", xx, 1110, 30, (*YLW, b), FONT)
    d = ap(u, 0.62, 0.8)
    if d > 0:
        plane_side(c, 640, 1250, 130, BLU, d, 2.5)
        L = 300 - 190 * ap(u, 0.72, 0.9)
        arrow(c, 470, 1255, 470 - L, 1255, RED, d, 7)
        txt(c, "FREIN", 470 - L / 2, 1225, 34, (*RED, d), FONT, 'c')
        tri(c, 900, 1230, 26, False, YLW, ap(u, 0.85, 0.92)); txt(c, "CARBURANT", 900, 1300, 30, (*YLW, ap(u, 0.85, 0.92)), FONT, 'c')


def engine(c, x, y, s, a, t):
    def nac(): c.new_path(); poly(c, [(x - s, y - 0.45 * s), (x + s, y - 0.32 * s), (x + 1.1 * s, y), (x + s, y + 0.32 * s), (x - s, y + 0.45 * s)], True)
    nac(); c.set_source_rgba(*BLU, a * 0.08); c.fill(); glow(c, nac, BLU, a, 3)
    for k in range(5):           # aubes de soufflante
        xx = x - 0.75 * s; ph = (t * 8 + k * 0.6) % 3.14
        c.move_to(xx, y - 0.38 * s * math.cos(ph)); c.line_to(xx + 12, y + 0.38 * s * math.cos(ph))
    c.set_source_rgba(*CYA, a); c.set_line_width(3); c.stroke()
    for k, (lab, col) in enumerate((("COMPRESSION", CYA), ("COMBUSTION", ORG), ("TURBINE", YLW))):
        xx = x - 0.45 * s + k * 0.55 * s
        c.new_path(); c.rectangle(xx, y - 0.22 * s, 0.4 * s, 0.44 * s); c.set_source_rgba(*col, a * 0.18); c.fill()
        txt(c, lab, xx + 0.2 * s, y + 0.62 * s + (k % 2) * 44, 28, (*col, a), FONT, 'c')


def sc_cold(c, t, sg, lt, u):
    a = ap(u, 0.0, 0.1)
    engine(c, W / 2 + 40, 640, 330, a, t)
    for k in range(4):
        ph = ((t * 0.9 + k * 0.25) % 1)
        arrow(c, 40 + ph * 140, 560 + k * 55, 120 + ph * 140, 560 + k * 55, CYA, a * (1 - ph), 4, 18)
    b = ap(u, 0.55, 0.65)
    if b > 0:
        x = 230; y0, y1 = 1000, 1270
        glow(c, lambda: (c.new_path(), c.rectangle(x - 22, y0, 44, y1 - y0)), CYA, b, 2.5)
        lvl = y1 - (y1 - y0) * (0.85 - 0.6 * ap(u, 0.65, 0.8))
        c.new_path(); c.rectangle(x - 12, lvl, 24, y1 - lvl); c.set_source_rgba(*CYA, b); c.fill()
        c.arc(x, y1 + 26, 34, 0, 6.283); c.set_source_rgba(*CYA, b); c.fill()
        txt(c, "−56 °C", x + 70, 1150, 110, (*CYA, b), BIG, glow=1)
        g = ap(u, 0.78, 0.88)
        gauge(c, 820, 1130, 110, 0.35 + 0.5 * ap(u, 0.8, 0.95), "RENDEMENT", "", YLW, g)
        if g > 0: tri(c, 820, 1160, 30, True, YLW, g)


def sc_weather(c, t, sg, lt, u):
    a = ap(u, 0.0, 0.1); y0, y1 = 1300, 400        # sol en bas, 14 km en haut
    alt_axis(c, 170, y0, y1, 14, a)
    ky = lambda km: y0 + (y1 - y0) * km / 14
    for k, (x, km, s) in enumerate(((330, 2.0, 50), (560, 3.5, 70), (800, 1.5, 55), (460, 6, 45), (720, 7.5, 60), (900, 5, 40), (620, 9.5, 40))):
        cloud(c, x, ky(km), s, a * ap(u, 0.05 + k * 0.03, 0.15 + k * 0.03))
    b = ap(u, 0.25, 0.4)
    if b > 0:
        y = ky(11)
        for k in range(18):
            c.move_to(190 + k * 50, y); c.line_to(220 + k * 50, y)
        c.set_source_rgba(*YLW, b); c.set_line_width(4); c.stroke()
        txt(c, "TROPOPAUSE ≈ 11 KM", 940, y - 20, 44, (*YLW, b), BIG, 'r', glow=1)
    d = ap(u, 0.5, 0.65)
    if d > 0:
        plane_side(c, 420, ky(12.3) - 4 * math.sin(lt * 1.5), 110, BLU, d, 2.5)
        txt(c, "TURBULENCES", 640, ky(4.5), 36, (*RED, ap(u, 0.75, 0.85)), FONT, 'c')
        txt(c, "EN DESSOUS", 640, ky(4.5) + 44, 36, (*RED, ap(u, 0.75, 0.85)), FONT, 'c')


def sc_coffin(c, t, sg, lt, u):
    a = ap(u, 0.0, 0.1)
    x0, x1, y0, y1 = 170, 960, 1300, 420
    glow(c, lambda: (c.new_path(), c.move_to(x0, y1), c.line_to(x0, y0), c.line_to(x1, y0)), BLU, a, 2.5)
    txt(c, "ALTITUDE", x0 - 10, y1 - 20, 32, (*CYA, a), FONT)
    txt(c, "VITESSE", x1, y0 + 50, 32, (*CYA, a), FONT, 'r')
    b = ap(u, 0.25, 0.55)
    apex = ((x0 + x1) / 2 + 60, y1 + 60)
    def stall(f):  # vitesse de décrochage : monte vers la droite
        pts = []
        for k in range(41):
            s = k / 40 * f; y = y0 + (apex[1] - y0) * s
            x = 300 + (apex[0] - 300) * s ** 2.2; pts.append((x, y))
        return pts
    def vmax(f):
        pts = []
        for k in range(41):
            s = k / 40 * f; y = y0 + (apex[1] - y0) * s
            x = 880 - (880 - apex[0]) * s ** 2.2; pts.append((x, y))
        return pts
    if b > 0:
        glow(c, lambda: poly(c, stall(b)), RED, 1, 4)
        glow(c, lambda: poly(c, vmax(b)), ORG, 1, 4)
        txt(c, "DÉCROCHAGE", 300, y0 - 30, 32, (*RED, b), FONT)
        txt(c, "VITESSE MAX", 880, y0 - 30, 32, (*ORG, b), FONT, 'r')
    d = ap(u, 0.62, 0.72)
    if d > 0:
        r = 70 + 8 * math.sin(lt * 6)
        c.new_path(); c.arc(apex[0], apex[1] + 20, r, 0, 6.283); c.set_source_rgba(*RED, d * 0.18); c.fill()
        glow(c, lambda: (c.new_path(), c.arc(apex[0], apex[1] + 20, r, 0, 6.283)), RED, d, 3)
        txt(c, "COIN DU CERCUEIL", apex[0], apex[1] - 80, 66, (*RED, ap(u, 0.78, 0.86)), BIG, 'c', glow=1)
    e = ap(u, 0.35, 0.75)
    if e > 0:
        s = min(e, 0.85); y = y0 + (apex[1] - y0) * s
        plane_side(c, apex[0] - 20, y + 60, 60, BLU, ap(u, 0.35, 0.42), 2)


def sc_steps(c, t, sg, lt, u):
    a = ap(u, 0.0, 0.1)
    x0, x1, y0, y1 = 140, 960, 1250, 450
    glow(c, lambda: (c.new_path(), c.move_to(x0, y1), c.line_to(x0, y0), c.line_to(x1, y0)), BLU, a, 2.5)
    lv = [(10000, 0.18, 0.42), (11000, 0.42, 0.68), (12000, 0.68, 1.0)]
    ky = lambda m: y0 - (y0 - y1) * (m - 0) / 13000
    b = ap(u, 0.1, 0.85)
    pts = [(x0, y0), (x0 + (x1 - x0) * 0.18, ky(10000))]
    for k, (m, f0, f1) in enumerate(lv):
        pts.append((x0 + (x1 - x0) * f1, ky(m)))
        if k + 1 < len(lv): pts.append((x0 + (x1 - x0) * f1 + 30, ky(lv[k + 1][0])))
    L = [0]
    for i in range(1, len(pts)): L.append(L[-1] + math.dist(pts[i - 1], pts[i]))
    cut = L[-1] * b; vis = [pts[0]]
    for i in range(1, len(pts)):
        if L[i] <= cut: vis.append(pts[i])
        else:
            f = (cut - L[i - 1]) / (L[i] - L[i - 1]); vis.append((pts[i - 1][0] + f * (pts[i][0] - pts[i - 1][0]), pts[i - 1][1] + f * (pts[i][1] - pts[i - 1][1]))); break
    if len(vis) > 1:
        glow(c, lambda: poly(c, vis), YLW, 1, 4)
        plane_side(c, vis[-1][0], vis[-1][1] - 30, 55, BLU, 1, 2)
    for m, f0, f1 in lv:
        if b > f0 * 0.9: txt(c, f"{m // 1000} {m % 1000:03d} M", x0 + (x1 - x0) * (f0 + f1) / 2, ky(m) - 70, 44, (*WHT, ap(u, f0 * 0.85, f0 * 0.85 + 0.06)), BIG, 'c')
    fuel = 1 - 0.7 * b
    panel(c, x0, 1320, 820, 50, ORG, a, 0.0)
    c.new_path(); c.rectangle(x0 + 6, 1326, 808 * fuel, 38); c.set_source_rgba(*ORG, a * 0.8); c.fill()
    txt(c, "CARBURANT", x0, 1310, 30, (*ORG, a), FONT)


def sc_cabin(c, t, sg, lt, u):
    a = ap(u, 0.0, 0.1); cx, cy, R = W / 2, 820, 300
    glow(c, lambda: (c.new_path(), c.arc(cx, cy, R, 0, 6.283)), BLU, a, 4)
    c.new_path(); c.arc(cx, cy, R - 10, 0, 6.283); c.set_source_rgba(*CYA, a * 0.07); c.fill()
    glow(c, lambda: (c.new_path(), c.move_to(cx - R + 30, cy + 120), c.line_to(cx + R - 30, cy + 120)), BLU, a, 2.5)
    for k in range(6):
        x = cx - 200 + k * 80
        c.new_path(); c.rectangle(x - 22, cy + 30, 44, 90); c.set_source_rgba(*CYA, a * 0.5); c.fill()
    b = ap(u, 0.3, 0.45)
    for k in range(12):
        an = k * 6.283 / 12; r0 = R + 110 - 25 * math.sin(t * 4 + k)
        arrow(c, cx + math.cos(an) * r0, cy + math.sin(an) * r0, cx + math.cos(an) * (R + 20), cy + math.sin(an) * (R + 20), YLW, b * 0.8, 3, 16)
    txt(c, "DEHORS : 11 000 M", W / 2, 400, 64, (*RED, ap(u, 0.1, 0.2)), BIG, 'c', glow=1)
    d = ap(u, 0.55, 0.68)
    txt(c, "CABINE ≈ 2 400 M", cx, cy - 60, 86, (*YLW, d), BIG, 'c', glow=1)
    txt(c, "PRESSURISÉE", cx, cy - 6, 34, (*WHT, d), FONT, 'c')


def sc_concorde(c, t, sg, lt, u):
    a = ap(u, 0.0, 0.1); y0, y1 = 1300, 420
    alt_axis(c, 170, y0, y1, 20, a, 4)
    ky = lambda km: y0 + (y1 - y0) * km / 20
    for k, km in enumerate((11, 18)):
        yy = ky(km)
        for j in range(16):
            c.move_to(190 + j * 50, yy); c.line_to(220 + j * 50, yy)
        c.set_source_rgba(*(CYA if k == 0 else YLW), a * (0.5 if k == 0 else ap(u, 0.2, 0.3))); c.set_line_width(3); c.stroke()
    plane_side(c, 560, ky(11) - 50, 110, BLU, a, 2.5)
    txt(c, "AVION DE LIGNE · 11 KM", 940, ky(11) + 50, 34, (*CYA, a), FONT, 'r')
    b = ap(u, 0.15, 0.4)
    delta_side(c, 300 + 400 * b + 40 * u, ky(18) - 40, 140, YLW, b, 3)
    txt(c, "CONCORDE · 18 KM", 940, ky(18) + 50, 34, (*YLW, b), FONT, 'r')
    d = ap(u, 0.7, 0.8)
    txt(c, "MACH 2", W / 2 + 60, ky(15) + 30, 150, (*YLW, d), BIG, 'c', glow=1)


def sc_outro(c, t, sg, lt, u):
    a = ap(u, 0.0, 0.15)
    plane_side(c, W / 2, 560, 260, BLU, a, 3)
    l1, l2 = sg['p'].get('lines', ("L'ALTITUDE N'EST", "JAMAIS UN HASARD"))
    txt(c, l1, W / 2, 820, 92, (*WHT, a), BIG, 'c')
    txt(c, l2, W / 2, 910, 92, (*YLW, a), BIG, 'c', glow=1)
    b = ap(u, 0.45, 0.55)
    if b > 0:
        s = 1 + 0.06 * math.sin(lt * 6)
        c.save(); c.translate(W / 2, 1110); c.scale(s * b, s * b)
        c.new_path(); r = 50; w, h = 560, 110
        c.arc(-w / 2 + r, -h / 2 + r, r, math.pi, 1.5 * math.pi); c.arc(w / 2 - r, -h / 2 + r, r, 1.5 * math.pi, 0); c.arc(w / 2 - r, h / 2 - r, r, 0, 0.5 * math.pi); c.arc(-w / 2 + r, h / 2 - r, r, 0.5 * math.pi, math.pi); c.close_path()
        c.set_source_rgba(*YLW, 1); c.fill()
        txt(c, "ABONNE-TOI", 0, 30, 84, (0.02, 0.03, 0.06, 1), BIG, 'c')
        c.restore()
        sticker(c, 'point_right', 150, 1110, 230, b, -0.05)
    d = ap(u, 0.7, 0.8)
    txt(c, f"ÉP. {int(getattr(CFG, 'EP', '01')) + 1:02d} : {getattr(CFG, 'NEXT', '')}", W / 2, 1270, 44, (*CYA, d), FONT, 'c')


SC = dict(hook=sc_hook, plan=sc_plan, air=sc_air, cold=sc_cold, weather=sc_weather, coffin=sc_coffin, steps=sc_steps, cabin=sc_cabin, concorde=sc_concorde, outro=sc_outro)


# ---------- épisode 02 : le mur du son ----------
def mach_waves(c, lt, m0, m1, T, px, py, cs=170, col=CYA, a=1.0, span=3.2):
    """Ondes émises par l'avion (caméra qui suit l'avion, fixé en px). Mach passe de m0 à m1 en T secondes."""
    M = lambda tau: m0 + (m1 - m0) * min(1, max(0, tau / T))
    X = lambda tau: sum(M(tau * k / 40) for k in range(40)) * tau / 40 * cs
    xn = X(lt)
    te = lt - (lt % 0.22)
    for k in range(int(span / 0.22)):
        e = te - k * 0.22
        if e < 0: break
        r = cs * (lt - e); cx = px - (xn - X(e))
        al = a * max(0, 1 - r / 900)
        if al <= 0: continue
        c.new_path(); c.arc(cx, py, r, 0, 6.283); c.set_source_rgba(*col, al * 0.85); c.set_line_width(3); c.stroke()
    return M(lt)


def sc_waves(c, t, sg, lt, u):
    a = ap(u, 0, 0.08); T = max(1, sg['dur'] * 0.75)
    m = mach_waves(c, lt, 0.45, 1.0, T, 640, 800, a=a)
    plane_side(c, 640 - 90, 800, 90, BLU, a, 2.5)
    txt(c, f"MACH {m:.2f}".replace('.', ','), W / 2, 1230, 120, (*(YLW if m > 0.97 else WHT), a), BIG, 'c', glow=1)
    if m > 0.97:
        b = ap(u, 0.8, 0.88)
        glow(c, lambda: (c.new_path(), c.move_to(645, 560), c.line_to(645, 1040)), RED, b, 6)
        txt(c, "LE MUR", 680, 560, 56, (*RED, b), BIG)


def sc_cone(c, t, sg, lt, u):
    a = ap(u, 0, 0.08)
    m = mach_waves(c, lt + 3, 1.7, 1.7, 1, 820, 780, a=a, span=4.5)
    plane_side(c, 820 - 90, 780, 90, BLU, a, 2.5)
    b = ap(u, 0.3, 0.45); mu = math.asin(1 / 1.7); L = 900
    for sgn in (-1, 1):
        glow(c, lambda sgn=sgn: (c.new_path(), c.move_to(830, 780), c.line_to(830 - L * math.cos(mu), 780 + sgn * L * math.sin(mu))), YLW, b, 4)
    txt(c, "CÔNE DE MACH", 300, 1180, 70, (*YLW, b), BIG, 'c', glow=1)
    txt(c, "MACH 1,7", 820, 600, 60, (*WHT, a), BIG, 'c')


def person(c, x, y, s, col, a):
    c.new_path(); c.arc(x, y - 1.6 * s, 0.25 * s, 0, 6.283); c.set_source_rgba(*col, a); c.fill()
    glow(c, lambda: poly(c, [(x, y - 1.35 * s), (x, y - 0.6 * s), (x - 0.3 * s, y), (x, y - 0.6 * s), (x + 0.3 * s, y), (x, y - 0.6 * s), (x, y - 1.1 * s), (x - 0.35 * s, y - 0.85 * s), (x, y - 1.1 * s), (x + 0.35 * s, y - 0.85 * s)]), col, a, 3)


def sc_bang(c, t, sg, lt, u):
    a = ap(u, 0, 0.08); gy = 1200; py = 560
    glow(c, lambda: (c.new_path(), c.move_to(0, gy), c.line_to(W, gy)), BLU, a, 3)
    for k in range(24):
        c.move_to(k * 50, gy); c.line_to(k * 50 - 25, gy + 25)
    c.set_source_rgba(*BLU, a * 0.4); c.set_line_width(2); c.stroke()
    mu = math.asin(1 / 1.7); dx = (gy - py) / math.tan(mu)
    xs = -300 + 1500 * ap(u, 0.05, 0.95)
    for sgn in (-1, 1):
        glow(c, lambda sgn=sgn: (c.new_path(), c.move_to(xs, py), c.line_to(xs - dx * 1.2, py + sgn * (gy - py) * 1.2)), YLW, a, 4)
    plane_side(c, xs - 80, py, 80, BLU, a, 2.5)
    xg = xs - dx
    c.new_path(); c.arc(xg, gy, 16, 0, 6.283); c.set_source_rgba(*RED, a); c.fill()
    for k, px in enumerate((260, 820)):
        hit = xg >= px; f = min(1, max(0, (xg - px) / 120)) if hit else 0
        person(c, px, gy - 4, 60, WHT if not hit else YLW, a)
        if hit and f < 1:
            sc_ = 1 + 0.4 * f
            txt(c, "BANG !", px, gy - 160 - 40 * f, 90 * sc_, (*RED, 1 - f * 0.6), BIG, 'c', glow=1)
    txt(c, "TOUT LE LONG DU VOL", W / 2, 1330, 54, (*YLW, ap(u, 0.6, 0.7)), BIG, 'c', glow=1)


def x1_side(c, x, y, s, col, a=1.0, w=3.0):
    def body():
        c.new_path(); c.move_to(x + 1.0 * s, y)
        c.curve_to(x + 0.7 * s, y - 0.16 * s, x + 0.2 * s, y - 0.17 * s, x - 0.6 * s, y - 0.12 * s)
        c.line_to(x - 0.95 * s, y - 0.05 * s); c.line_to(x - 0.95 * s, y + 0.05 * s); c.line_to(x - 0.6 * s, y + 0.12 * s)
        c.curve_to(x + 0.2 * s, y + 0.17 * s, x + 0.7 * s, y + 0.16 * s, x + 1.0 * s, y); c.close_path()
    body(); c.set_source_rgba(*col, a * 0.08); c.fill(); glow(c, body, col, a, w)
    glow(c, lambda: poly(c, [(x - 0.55 * s, y - 0.1 * s), (x - 0.8 * s, y - 0.42 * s), (x - 0.92 * s, y - 0.42 * s), (x - 0.85 * s, y - 0.06 * s)]), col, a, w)
    glow(c, lambda: poly(c, [(x + 0.15 * s, y + 0.05 * s), (x - 0.05 * s, y + 0.2 * s), (x - 0.25 * s, y + 0.2 * s), (x - 0.15 * s, y + 0.05 * s)]), col, a, w)
    c.new_path(); c.arc(x + 0.55 * s, y - 0.09 * s, 0.05 * s, 0, 6.283); c.set_source_rgba(*col, a * 0.6); c.fill()


def sc_yeager(c, t, sg, lt, u):
    a = ap(u, 0, 0.1)
    txt(c, "14 OCTOBRE 1947", W / 2, 520, 120, (*YLW, a), BIG, 'c', glow=1)
    b = ap(u, 0.25, 0.4)
    x1_side(c, 200 + 500 * b + 60 * u, 820, 230, BLU, b, 3)
    for k in range(5):
        L = 60 + 40 * k
        glow(c, lambda k=k, L=L: (c.new_path(), c.move_to(200 + 500 * b + 60 * u - 230 * 0.95 - 10, 820 + (k - 2) * 8), c.line_to(200 + 500 * b + 60 * u - 230 * 0.95 - 10 - L * (0.6 + 0.4 * math.sin(lt * 20 + k)), 820 + (k - 2) * 8)), ORG, b * 0.8, 3)
    txt(c, "BELL X-1", W / 2, 1060, 90, (*WHT, ap(u, 0.45, 0.55)), BIG, 'c')
    txt(c, "MACH 1,06", W / 2, 1190, 110, (*CYA, ap(u, 0.6, 0.7)), BIG, 'c', glow=1)


def sc_vapor(c, t, sg, lt, u):
    a = ap(u, 0, 0.08); cx, cy = W / 2, 760
    b = ap(u, 0.15, 0.3)
    for k in range(6):
        rr = 1 + 0.08 * math.sin(lt * 7 + k)
        c.save(); c.translate(cx - 40 + k * 18, cy); c.scale(0.45, 1)
        c.new_path(); c.arc(0, 0, (230 - k * 25) * rr, 0, 6.283); c.restore()
        c.set_source_rgba(0.9, 0.95, 1, b * 0.10); c.fill()
    plane_side(c, cx, cy, 300, BLU, a, 3)
    txt(c, "CONDENSATION", cx, 450, 80, (*CYA, ap(u, 0.35, 0.45)), BIG, 'c', glow=1)
    d = ap(u, 0.62, 0.72)
    if d > 0:
        c.save(); c.translate(cx, 1150); c.rotate(-0.08); s_ = 1 + 0.2 * (1 - d)
        c.scale(s_, s_)
        glow(c, lambda: (c.new_path(), c.rectangle(-380, -70, 760, 120)), RED, d, 5)
        txt(c, "PAS UNE PREUVE DE MACH 1", 0, 20, 60, (*RED, d), BIG, 'c')
        c.restore()


def sc_ban(c, t, sg, lt, u):
    a = ap(u, 0, 0.08); gy = 1100; coast = 560
    c.new_path(); poly(c, [(0, gy), (coast - 40, gy), (coast, gy + 30), (coast - 60, gy + 120), (0, gy + 120)], True)
    c.set_source_rgba(*BLU, a * 0.15); c.fill()
    glow(c, lambda: poly(c, [(0, gy), (coast - 40, gy), (coast, gy + 30), (coast - 60, gy + 120)]), BLU, a, 3)
    for k in range(6):
        y = gy + 20 + k * 18; ph = lt * 2 + k
        c.new_path()
        for j in range(30):
            x = coast + 20 + j * 18; c.line_to(x, y + 6 * math.sin(ph + j * 0.6))
        c.set_source_rgba(*CYA, a * 0.5); c.set_line_width(2); c.stroke()
    txt(c, "TERRE", coast / 2, gy + 190, 60, (*WHT, a), BIG, 'c')
    txt(c, "OCÉAN", (coast + W) / 2, gy + 190, 60, (*CYA, a), BIG, 'c')
    f = ap(u, 0.1, 0.85); x = 120 + 860 * f; sup = x > coast + 40
    if sup:
        mu = math.asin(1 / 2.0)
        for sgn in (-1, 1):
            glow(c, lambda sgn=sgn: (c.new_path(), c.move_to(x + 60, 700), c.line_to(x + 60 - 500 * math.cos(mu), 700 + sgn * 500 * math.sin(mu))), YLW, 0.8, 3)
    delta_side(c, x, 700, 110, YLW if sup else WHT, a, 3)
    txt(c, "MACH 2" if sup else "MACH 0,95", x, 600, 70, (*(YLW if sup else WHT), a), BIG, 'c', glow=1)
    if not sup:
        txt(c, "SUPERSONIQUE INTERDIT", coast / 2 + 60, 470, 56, (*RED, ap(u, 0.2, 0.3)), BIG, 'c', glow=1)


SC.update(waves=sc_waves, cone=sc_cone, bang=sc_bang, yeager=sc_yeager, vapor=sc_vapor, ban=sc_ban)


def frame(t):
    sg = next((x for x in SEG if x['t0'] <= t < x['end']), SEG[-1]); lt = t - sg['t0']
    u = min(1, max(0, (t - sg['vt']) / max(0.1, sg['dur'] + 0.3)))
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    background(c, t)
    k = 1 + 0.035 * ease(lt / max(1, sg['end'] - sg['t0']))       # zoom lent (pas de tremblement)
    c.save(); c.translate(W / 2, 850); c.scale(k, k); c.translate(-W / 2, -850)
    SC[sg['scene']](c, t, sg, lt, u)
    c.restore()
    if sg['i'] > 0 and lt < 0.22:   # transition : flash bleu + balayage
        f = lt / 0.22
        c.set_source_rgba(*BLU, 0.35 * (1 - f)); c.paint()
        x = W * f; c.set_source_rgba(*CYA, 0.8 * (1 - f)); c.rectangle(x - 4, 0, 8, H); c.fill()
    header(c, t, sg, lt); subtitles(c, t)
    c.set_source_rgba(*YLW, 1); c.rectangle(0, H - 8, W * t / TOTAL, 8); c.fill()
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
