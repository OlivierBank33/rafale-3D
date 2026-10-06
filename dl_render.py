"""Moteur de duel générique A vs B (rounds, score, barres, compteurs, listes, radar, HUD, verdict).
Usage : DL=dl/<slug> python3 dl_render.py [stills t1 t2 ...]
Le dossier contient cfg.py (A, B, SCENES), durs.json (durées Kokoro par scène s0..sN, recalées par el_sync), a_*.png / b_*.png (34, side, front, top).
"""
import cairo, json, math, os, subprocess, sys, re, random, importlib.util
import numpy as np

W, H, FPS = 1080, 1920, 30
D = os.environ.get('DL', 'dl/rafale_typhoon').rstrip('/') + '/'
spec = importlib.util.spec_from_file_location('cfg', D + 'cfg.py'); CFG = importlib.util.module_from_spec(spec); spec.loader.exec_module(CFG)
A, B, SCENES = CFG.A, CFG.B, CFG.SCENES
CA, CB = tuple(A['color']), tuple(B['color'])
YEL = (1.0, 0.84, 0.1); WHITE = (1, 1, 1); GRN = (0.35, 1.0, 0.55); GREY = (0.85, 0.85, 0.9); INK = (0.05, 0.05, 0.08)
DUR = json.load(open(D + 'durs.json'))

# ---------- Timeline ----------
SEG = []; t = 0.0
for i, s in enumerate(SCENES):
    pre = 0.2 if i == 0 else 0.3
    post = 0.35 if i < len(SCENES) - 1 else getattr(CFG, 'END_HOLD', 1.6)
    SEG.append(dict(i=i, k=f's{i}', scene=s['type'], t0=t, vt=t + pre, dur=DUR[f's{i}'], end=t + pre + DUR[f's{i}'] + post, score=tuple(s['score']), p=s))
    t = SEG[-1]['end']
TOTAL = t
json.dump(dict(seg=[{k: v for k, v in x.items() if k != 'p'} for x in SEG], total=TOTAL), open(D + 'timeline.json', 'w'))
ROUNDS = [s for s in SEG if s['scene'] not in ('hook', 'verdict', 'doute')]
random.seed(7)

IM = {}
for side in 'ab':
    for v in ('34', 'side', 'front', 'top'):
        IM[f'{side}_{v}'] = cairo.ImageSurface.create_from_png(D + f'{side}_{v}.png')
FLIP = getattr(CFG, 'FLIP', {})
TOPROT = getattr(CFG, 'TOPROT', {'a_top': -math.pi / 2, 'b_top': math.pi})


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
    c.new_path(); r = min(r, w / 2, h / 2)
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2); c.close_path()


def pill(c, txt, cx, cy, size, bg, fg=(1, 1, 1), s=1.0, alpha=1.0):
    if s <= 0.02 or alpha <= 0.01: return
    c.save(); c.translate(cx, cy); c.scale(s, s)
    font(c, size); e = c.text_extents(txt); bw = e.x_advance + size * 1.3; bh = size * 1.75
    if bw > W - 60:
        k = (W - 60) / bw; c.scale(k, k)
    rrect(c, -bw / 2, -bh / 2, bw, bh, bh / 2); c.set_source_rgba(*bg, 0.95 * alpha); c.fill()
    c.set_source_rgba(*fg, alpha); c.move_to(-e.x_advance / 2, size * 0.36); c.show_text(txt); c.restore()


def plane(c, key, cx, cy, size, alpha=1.0, rot=0.0, glow=None):
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


def background(c, t, tint=None, streak=0.7):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.025, 0.035, 0.07); g.add_color_stop_rgb(0.55, 0.05, 0.07, 0.13); g.add_color_stop_rgb(1, 0.015, 0.02, 0.04)
    c.set_source(g); c.paint()
    for (col, x, y, r, a) in (tint or []):
        rg = cairo.RadialGradient(x, y, 0, x, y, r); rg.add_color_stop_rgba(0, *col, a); rg.add_color_stop_rgba(1, *col, 0)
        c.set_source(rg); c.paint()
    if streak > 0:
        c.set_line_width(3); c.set_line_cap(cairo.LINE_CAP_ROUND)
        for s in STREAKS:
            x = W + 300 - ((t * s['sp'] + s['ph']) % (W + 600))
            c.set_source_rgba(1, 1, 1, 0.10 * streak); c.move_to(x, s['y']); c.line_to(x + s['ln'], s['y']); c.stroke()
    vg = cairo.RadialGradient(W / 2, H / 2, H * 0.3, W / 2, H / 2, H * 0.75)
    vg.add_color_stop_rgba(0, 0, 0, 0, 0); vg.add_color_stop_rgba(1, 0, 0, 0, 0.65)
    c.set_source(vg); c.paint()


def side(k):
    return (A, CA, 'a') if k == 'A' else (B, CB, 'b')


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
    y0 = 158; bw = 680; bh = 104; x0 = W / 2 - bw / 2
    rrect(c, x0, y0, bw, bh, 26); c.set_source_rgba(0.04, 0.05, 0.09, 0.88 * a); c.fill_preserve()
    c.set_source_rgba(1, 1, 1, 0.12 * a); c.set_line_width(2); c.stroke()
    rrect(c, x0, y0, 14, bh, 7); c.set_source_rgba(*CA, a); c.fill()
    rrect(c, x0 + bw - 14, y0, 14, bh, 7); c.set_source_rgba(*CB, a); c.fill()
    text_c(c, A['short'], x0 + 140, y0 + 68, 40, (*CA, a), maxw=220)
    text_c(c, B['short'], x0 + bw - 140, y0 + 68, 40, (*CB, a), maxw=220)
    for val, xx, idx in ((r, W / 2 - 52, 0), (f, W / 2 + 52, 1)):
        pop = 1.0
        if ch and ch[2][idx] != ch[1][idx] and t - ch[0] < 0.45:
            pop = 1 + 0.6 * (1 - ease_out((t - ch[0]) / 0.45))
        c.save(); c.translate(xx, y0 + 52); c.scale(pop, pop); text_c(c, str(val), 0, 26, 76, (1, 1, 1, a)); c.restore()
    text_c(c, "–", W / 2, y0 + 72, 50, (1, 1, 1, 0.5 * a))
    done = sum(1 for x in ROUNDS if x['i'] < s['i'])
    n = len(ROUNDS)
    for k in range(n):
        cx = W / 2 - (n - 1) * 20 + k * 40; on = k < done
        c.arc(cx, y0 + bh + 26, 9, 0, 2 * math.pi)
        c.set_source_rgba(*(YEL if on else (1, 1, 1)), (1 if on else 0.25) * a); c.fill()
    c.restore()


def round_title(c, t, s):
    p = s['p']
    if 'round' not in p: return
    lt = t - s['t0']
    a = ease(lt / 0.3) * (1 - ease((lt - 2.6) / 0.4))
    if a <= 0.01: return
    sc = back_out(lt / 0.35)
    c.save(); c.translate(W / 2, 395); c.scale(0.7 + 0.3 * sc, 0.7 + 0.3 * sc)
    text_c(c, p['round'], 0, 0, 44, (*YEL, a), stroke=8)
    text_c(c, p['title'], 0, 72, 74, (1, 1, 1, a), stroke=10, maxw=900)
    c.restore()


# ---------- Scènes ----------
def sc_hook(c, t, s):
    lt = t - s['t0']
    background(c, t, tint=[(CA, 270, 820, 560, 0.35), (CB, 810, 1120, 560, 0.35)], streak=1.0)
    u = ease_out(0.55 + lt / 1.2); bob = math.sin(t * 2.2) * 8
    plane(c, 'a_34', -380 + u * 720, 820 + bob, 680, glow=CA)
    plane(c, 'b_34', 1460 - u * 720, 1130 - bob, 680, glow=CB)
    na = ease((lt - 0.1) / 0.25)
    text_c(c, A['name'], 300, 600, 64, (*CA, na), stroke=8, maxw=520)
    text_c(c, B['name'], 780, 1370, 64, (*CB, na), stroke=8, maxw=520)
    if lt > 0.05:
        v = back_out((lt - 0.05) / 0.3)
        c.save(); c.translate(W / 2, 1000); c.scale(0.4 + 0.6 * v, 0.4 + 0.6 * v); c.rotate(-0.08)
        text_c(c, "VS", 0, 70, 230, (1, 1, 1, 1), stroke=18); c.restore()
        fl = 1 - ease((lt - 0.05) / 0.2)
        if fl > 0: c.set_source_rgba(1, 1, 1, 0.8 * fl); c.paint()
    text_c(c, s['p'].get('kicker', "LE DUEL"), W / 2, 400, 52, (*YEL, 1.0), stroke=8)
    q = back_out((lt - 0.4) / 0.3)
    if q > 0.02:
        c.save(); c.translate(W / 2, 1470); c.scale(q, q); text_c(c, "QUI GAGNE ?", 0, 0, 80, (*YEL, 1), stroke=12); c.restore()


def bar(c, x, y, w, h, frac, col, label, val, a):
    rrect(c, x, y, w, h, h / 2); c.set_source_rgba(1, 1, 1, 0.10 * a); c.fill()
    if frac > 0.01:
        rrect(c, x, y, max(h, w * frac), h, h / 2); c.set_source_rgba(*col, a); c.fill()
    text_c(c, val, x + w - 150, y - 22, 54, (1, 1, 1, a), stroke=6, maxw=330)
    text_c(c, label, x + 130, y - 22, 40, (*col, a), stroke=6, maxw=260)


def sc_bars(c, t, s):
    """p: a, b (valeurs), max, fmt ('MACH {:.1f}'), dec (virgule), race (bool)."""
    p = s['p']; lt = t - s['t0']; u = (t - s['vt']) / s['dur']
    win = 'A' if p['a'] > p['b'] else 'B'
    wc = CA if win == 'A' else CB
    background(c, t, tint=[(wc, 700, 1150 if win == 'B' else 750, 520, 0.25 * ease((u - 0.75) / 0.1))], streak=2.0 if p.get('race', True) else 0.3)
    shake = 0
    run = ease(u / 0.85)
    fa, fb = (40, 170) if win == 'B' else (170, 40)
    plane(c, 'a_side', 430 + run * fa + shake, 720, 640, glow=CA)
    plane(c, 'b_side', 470 + run * fb - shake, 1110, 640, glow=CB)
    a = ease((lt - 0.6) / 0.4)
    first, second = (('a', 0.12), ('b', 0.45)) if p.get('a_first', False) else (('b', 0.12), ('a', 0.45))
    st = {first[0]: first[1], second[0]: second[1]}
    va = p['a'] * ease((u - st['a']) / 0.3); vb = p['b'] * ease((u - st['b']) / 0.3)
    f = lambda v: p['fmt'].format(v).replace('.', ',')
    bar(c, 140, 930, 800, 30, va / p['max'], CA, A['short'], f(va), a)
    bar(c, 140, 1340, 800, 30, vb / p['max'], CB, B['short'], f(vb), a)
    if p.get('pill'):
        pill(c, p['pill'], W / 2, 1460, 36, GREY, fg=INK, s=back_out((u - 0.7) / 0.1))
    round_title(c, t, s)


def sc_chips(c, t, s):
    """p: side ('A'/'B'), chips [4 max], other ('CHASSE'), other_label optional."""
    p = s['p']; lt = t - s['t0']; u = (t - s['vt']) / s['dur']
    (S, col, k) = side(p['side']); (O, ocol, ok) = side('B' if p['side'] == 'A' else 'A')
    background(c, t, tint=[(col, 540, 760, 600, 0.35)])
    plane(c, f'{k}_34', 560 + math.sin(t) * 8, 720, 760, glow=col)
    pos = [(300, 1010), (780, 1010), (300, 1110), (780, 1110)]
    for j, (txt, (x, y)) in enumerate(zip(p['chips'], pos)):
        pill(c, txt, x, y, 36, col, s=back_out((u - 0.2 - j * 0.08) / 0.1))
    fa = ease((u - 0.62) / 0.12)
    plane(c, f'{ok}_34', 330, 1290, 330, alpha=fa, glow=ocol)
    if p.get('other'):
        pill(c, p['other'], 700, 1290, 38, ocol if not p.get('other_grey') else GREY, fg=WHITE if not p.get('other_grey') else INK, s=back_out((u - 0.66) / 0.1))
    round_title(c, t, s)


def sc_counters(c, t, s):
    """p: a_num, b_num (entiers), a_sub, b_sub, a_pre/b_pre, suffix."""
    p = s['p']; lt = t - s['t0']; u = (t - s['vt']) / s['dur']
    background(c, t, tint=[(CA, 280, 900, 520, 0.28), (CB, 800, 900, 520, 0.28)])
    a = ease((lt - 0.2) / 0.4)
    plane(c, 'a_34', 280, 680, 470, alpha=a, glow=CA)
    plane(c, 'b_34', 800, 680, 470, alpha=a, glow=CB)
    text_c(c, A['short'], 280, 900, 48, (*CA, a), stroke=6, maxw=440)
    text_c(c, B['short'], 800, 900, 48, (*CB, a), stroke=6, maxw=440)
    c.set_source_rgba(1, 1, 1, 0.15 * a); c.rectangle(W / 2 - 1, 560, 2, 820); c.fill()
    for (num, sub, x, col, st) in ((p['a_num'], p['a_sub'], 280, CA, p.get('a_start', 0.15)), (p['b_num'], p['b_sub'], 800, CB, p.get('b_start', 0.45))):
        v = num if p.get('static') else int(round(num * ease_out((u - st) / 0.25)))
        if u > st - 0.02:
            text_c(c, p.get('pre', '') + (str(v) if p.get('static') else f"{v:,}".replace(',', ' ')) + p.get('suffix', ''), x, 1080, 120, (1, 1, 1, a), stroke=10, maxw=480)
            text_c(c, sub, x, 1160, 38, (*col, a * ease((u - st - 0.2) / 0.1)), stroke=6, maxw=480)
    if p.get('pill'):
        pill(c, p['pill'], W / 2, 1300, 36, GREY, fg=INK, s=back_out((u - 0.72) / 0.1))
    round_title(c, t, s)


def sc_list(c, t, s):
    """p: a_items, b_items (pastilles), a_start, b_start."""
    p = s['p']; lt = t - s['t0']; u = (t - s['vt']) / s['dur']
    background(c, t, tint=[(CA, 280, 900, 500, 0.25), (CB, 800, 900, 500, 0.25)])
    a = ease((lt - 0.2) / 0.4)
    plane(c, 'a_top', 280, 640, 380, alpha=a, rot=TOPROT['a_top'])
    plane(c, 'b_top', 800, 640, 380, alpha=a, rot=TOPROT['b_top'])
    text_c(c, A['short'], 280, 860, 50, (*CA, a), stroke=6, maxw=440)
    text_c(c, B['short'], 800, 860, 50, (*CB, a), stroke=6, maxw=440)
    c.set_source_rgba(1, 1, 1, 0.15 * a); c.rectangle(W / 2 - 1, 560, 2, 820); c.fill()
    sa, sb = p.get('a_start', 0.12), p.get('b_start', 0.5)
    for j, txt in enumerate(p['a_items']):
        pill(c, txt, 280, 960 + j * 95, 34, CA, s=back_out((u - sa - j * 0.05) / 0.08))
    for j, txt in enumerate(p['b_items']):
        pill(c, txt, 800, 960 + j * 95, 34, CB, s=back_out((u - sb - j * 0.05) / 0.08))
    round_title(c, t, s)


def sc_radar(c, t, s):
    """p: big ('A'/'B' = le plus visible), small_tag, pill."""
    p = s['p']; lt = t - s['t0']; u = (t - s['vt']) / s['dur']
    background(c, t)
    cx, cy, R = W / 2, 930, 390
    a = ease((lt - 0.2) / 0.5)
    c.set_source_rgba(0.02, 0.10, 0.08, 0.9 * a); c.arc(cx, cy, R, 0, 2 * math.pi); c.fill()
    c.set_line_width(2)
    for rr in (R * 0.33, R * 0.66, R):
        c.set_source_rgba(*GRN, 0.35 * a); c.arc(cx, cy, rr, 0, 2 * math.pi); c.stroke()
    sw = (t * 2.0) % (2 * math.pi)
    for k in range(30):
        ang = sw - k * 0.025
        c.move_to(cx, cy); c.arc(cx, cy, R, ang - 0.025, ang); c.close_path()
        c.set_source_rgba(*GRN, 0.22 * (1 - k / 30) * a); c.fill()

    def blip(ang, r, size, col, base):
        d = (sw - ang) % (2 * math.pi); fade = max(0, 1 - d / 4.5)
        bx, by = cx + r * math.cos(ang), cy + r * math.sin(ang); al = (base + (1 - base) * fade) * a
        g = cairo.RadialGradient(bx, by, 0, bx, by, size * 2.2); g.add_color_stop_rgba(0, *col, al); g.add_color_stop_rgba(1, *col, 0)
        c.set_source(g); c.arc(bx, by, size * 2.2, 0, 2 * math.pi); c.fill()
        c.set_source_rgba(1, 1, 1, al); c.arc(bx, by, size * 0.45, 0, 2 * math.pi); c.fill()
        return bx, by
    big = p.get('big', 'A')
    sa, sb = (34, 7) if big == 'A' else (7, 34)
    rb = blip(math.radians(205), 230, sa, CA, 0.35)
    fb = blip(math.radians(-35), 270, sb, CB, 0.35)
    text_c(c, A['short'], rb[0], rb[1] + 90, 40, (*CA, a), stroke=6)
    text_c(c, B['short'] + (" ?" if big == 'A' else ""), fb[0], fb[1] - 50, 40, (*CB, a), stroke=6)
    if p.get('pill'): pill(c, p['pill'], W / 2, 1385, 40, CB if big == 'A' else CA, s=back_out((u - 0.2) / 0.12), alpha=a)
    round_title(c, t, s)


def sc_verdict(c, t, s):
    """p: lines [(tag, 'A'/'B'), (tag, 'A'/'B')], winner optional."""
    p = s['p']; lt = t - s['t0']; u = (t - s['vt']) / s['dur']
    if u < 0.5:
        (S1, c1, k1) = side(p['lines'][0][1]); (S2, c2, k2) = side(p['lines'][1][1])
        background(c, t, tint=[(c1, 540, 640, 520, 0.35), (c2, 540, 1180, 520, 0.35)])
        a = ease(lt / 0.3)
        text_c(c, "VERDICT", W / 2, 400, 60, (*YEL, a), stroke=8)
        c.set_source_rgba(1, 1, 1, 0.15 * a); c.rectangle(80, 910, W - 160, 2); c.fill()
        plane(c, f'{k1}_34', 650, 660, 520, alpha=a, glow=c1)
        pill(c, p['lines'][0][0], 260, 560, 40, GREY, fg=INK, s=back_out((u - 0.03) / 0.08))
        text_c(c, S1['short'], 260, 680, 74, (*c1, ease((u - 0.08) / 0.08)), stroke=8, maxw=420)
        plane(c, f'{k2}_34', 430, 1180, 520, alpha=ease((u - 0.2) / 0.1), glow=c2)
        pill(c, p['lines'][1][0], 820, 1080, 40, GREY, fg=INK, s=back_out((u - 0.24) / 0.08))
        text_c(c, S2['short'], 820, 1200, 74, (*c2, ease((u - 0.28) / 0.08)), stroke=8, maxw=420)
    else:
        background(c, t, tint=[(CA, 300, 1000, 600, 0.35), (CB, 780, 1000, 600, 0.35)], streak=0.6)
        v = back_out((u - 0.5) / 0.1)
        c.save(); c.translate(W / 2, 640); c.scale(v, v)
        text_c(c, "ET TOI,", 0, 0, 96, (1, 1, 1, 1), stroke=12)
        text_c(c, "QUI GAGNE ?", 0, 110, 110, (*YEL, 1), stroke=12)
        c.restore()
        pp = 1 + 0.05 * math.sin(t * 6)
        pill(c, A['short'], 300, 1000, 60, CA, s=back_out((u - 0.58) / 0.08) * pp)
        pill(c, B['short'], 780, 1000, 60, CB, s=back_out((u - 0.62) / 0.08) * (2 - pp))
        a = ease((u - 0.7) / 0.1)
        text_c(c, "DIS-LE EN COMMENTAIRE", W / 2, 1200, 50, (1, 1, 1, a), stroke=8)
        c.set_source_rgba(*YEL, a); c.set_line_width(8)
        yy = 1250 + 12 * math.sin(t * 6)
        c.move_to(W / 2 - 30, yy); c.line_to(W / 2, yy + 34); c.line_to(W / 2 + 30, yy); c.stroke()
        if t > s['vt'] + s['dur'] + 0.3:
            pill(c, "NOUVEAU DUEL CHAQUE JOUR · ABONNE-TOI", W / 2, 1385, 40, YEL, fg=INK, s=back_out((t - s['vt'] - s['dur'] - 0.3) / 0.3))


SCN = dict(hook=sc_hook, bars=sc_bars, chips=sc_chips, counters=sc_counters, list=sc_list, radar=sc_radar, verdict=sc_verdict)


# ---------- Sous-titres ----------
def build_caps():
    caps = []
    for s in SEG:
        words = s['p']['show'].split(' ')

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
HI_A = [w.upper() for w in A.get('hi', [A['short']])]; HI_B = [w.upper() for w in B.get('hi', [B['short']])]


def captions(c, t):
    cap = None
    for cp in CAPS:
        if cp['t0'] - 0.02 <= t < cp['t1'] + 0.05: cap = cp
    if not cap: return
    size = 68; font(c, size)
    words = [w_.upper() for w_ in cap['words']]
    sp = c.text_extents(' ').x_advance; widths = [c.text_extents(w_).x_advance for w_ in words]
    total = sum(widths) + sp * (len(words) - 1)
    MW = 660 if MASCOT else 880
    if total > MW:
        size *= MW / total; font(c, size); widths = [c.text_extents(w_).x_advance for w_ in words]; sp = c.text_extents(' ').x_advance
        total = sum(widths) + sp * (len(words) - 1)
    pop = back_out((t - cap['t0']) / 0.15); y = 1610
    cxx = CAP_CX if MASCOT else W / 2
    c.save(); c.translate(cxx, y); c.scale(0.85 + 0.15 * pop, 0.85 + 0.15 * pop); c.translate(-cxx, -y)
    x = (CAP_CX if MASCOT else W / 2) - total / 2
    for w_, wd, (a, b) in zip(words, widths, cap['times']):
        c.move_to(x, y); c.text_path(w_)
        c.set_source_rgba(0, 0, 0, 0.9); c.set_line_width(13); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
        hi = YEL
        if any(h in w_ for h in HI_A): hi = tuple(min(1, x_ + 0.25) for x_ in CA)
        if any(h in w_ for h in HI_B): hi = tuple(min(1, x_ + 0.25) for x_ in CB)
        c.set_source_rgb(*(hi if a <= t < b + 0.05 else WHITE)); c.fill(); c.new_path()
        x += wd + sp
    c.restore()


_LAYER = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
CAP_STARTS = sorted(cp['t0'] for cp in CAPS)
SCORE_T = []
_prev = (0, 0)
for _s in SEG:
    if _s['score'] != _prev: SCORE_T.append(_s['vt'] + _s['dur'] * 0.86)
    _prev = _s['score']


# ---------------------------------------------------------------- mascotte (pilote)
MASCOT = getattr(CFG, 'MASCOT', True)
CAP_CX = 680
if MASCOT:
    import mascot as _M
    import soundfile as _sf
    _env = np.zeros(int(TOTAL * FPS) + FPS)
    for _s in SEG:
        try:
            _a, _sr = _sf.read(D + _s['k'] + '.wav')
        except Exception:
            continue
        if _a.ndim > 1: _a = _a.mean(1)
        _hop = _sr / FPS
        for _i in range(int(len(_a) / _hop)):
            _j = int(_s['vt'] * FPS) + _i
            if _j < len(_env): _env[_j] = np.sqrt(np.mean(_a[int(_i * _hop):int((_i + 1) * _hop)] ** 2))
    _ref = np.percentile(_env[_env > 1e-4], 85) if (_env > 1e-4).any() else 1.0
    MOUTH = np.clip((_env / _ref - 0.15) * 1.4, 0, 1)
    MOUTH = np.maximum(MOUTH, np.roll(MOUTH, 1) * 0.6)   # adoucit


def _mascot_state(t, s):
    """(pose, début de la pose) selon le moment du duel."""
    if s['scene'] == 'hook' and t < 1.5: return 'shocked', 0.0
    REACT = ['point_up', 'laugh', 'celebrate', 'shocked', 'point_up', 'laugh']
    for i, ts in enumerate(SCORE_T):
        if 0 <= t - ts < 1.15: return REACT[i % len(REACT)], ts
    if s['scene'] == 'verdict' and t > s['vt'] + s['dur'] + 0.15: return 'wink_thumb', s['vt'] + s['dur'] + 0.15
    if s['scene'] == 'bars' and t - s['t0'] < 1.0: return 'skeptical', s['t0']
    return 'neutral', None


def draw_mascot(c, t, s):
    f = min(len(MOUTH) - 1, int(t * FPS))
    m = float(MOUTH[f])
    pose, t0 = _mascot_state(t, s)
    pop = 0.0
    if t0 is not None: pop = max(0.0, 1 - (t - t0) / 0.28)
    # petit pop aussi au retour en « neutral »
    pp, pt0 = _mascot_state(t - 0.25, s)
    if pose == 'neutral' and pp != 'neutral': pop = max(pop, 0.5 * (1 - min(1, (t % 1e9) * 0)))
    ph = (t + 0.7) % 3.4
    blink = 1 if ph < 0.1 else 0
    enter = ease_out((t - 0.1) / 0.45) if t < 0.6 else 1.0
    bob = 5 * math.sin(t * 2.4) + (1 - enter) * 600
    if pose in ('celebrate', 'panic'): bob += 60
    _M.draw(c, 215, 1942 + bob, 560, pose=pose, mouth=m, blink=blink, pop=pop, tilt=-0.02 + 0.015 * math.sin(t * 1.1))

def camera(t, s):
    """Mouvement de caméra permanent : dérive lente + coup de zoom à chaque groupe de sous-titres + secousse sur les points."""
    lt = t - s['t0']
    drift = 1.0 + 0.03 * min(1.0, lt / max(1.0, s['end'] - s['t0']))
    last = max([c0 for c0 in CAP_STARTS if c0 <= t] or [-9])
    punch = 0.0
    sh = 0.0
    for ts in SCORE_T:
        if 0 <= t - ts < 0.45: sh = 1 - (t - ts) / 0.45
    dx = 0.0; dy = 0.0
    rot = 0.006 * math.sin(t * 0.9)
    return drift, dx, dy, 0.0


def render(t, surf):
    s = SEG[0]
    for x in SEG:
        if t >= x['t0']: s = x
    lc = cairo.Context(_LAYER)
    SCN[s['scene']](lc, t, s)
    _LAYER.flush()
    c = cairo.Context(surf)
    z, dx, dy, rot = camera(t, s)
    c.save(); c.translate(W / 2 + dx, H / 2 + dy); c.rotate(rot); c.scale(z, z); c.translate(-W / 2, -H / 2)
    c.set_source_surface(_LAYER, 0, 0); c.paint(); c.restore()
    scoreboard(c, t, s)
    if MASCOT: draw_mascot(c, t, s)
    captions(c, t)
    lt = t - s['t0']
    if lt < 0.12 and s['t0'] > 0:
        c.set_source_rgba(1, 1, 1, 0.45 * (1 - lt / 0.12)); c.paint()
    c.set_source_rgba(*YEL, 1); c.rectangle(0, 0, W * t / TOTAL, 6); c.fill()
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
