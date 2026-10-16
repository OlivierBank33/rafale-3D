"""DUEL en style néon @minuteaero (avions 3D convertis en contours néon, jauges, karaoké).
Même cfg que dl_render.py : DL=dl/<slug> python3 nd_render.py [stills t1 ...]  (A, B, FLIP, TOPROT, SCENES[hook|bars|chips|list|counters|radar|verdict], END_HOLD ; durs.json ; a_*.png / b_*.png)"""
import cairo, json, math, os, sys, importlib.util
from neon_lib import *

D = os.environ.get('DL', 'dl/rafale_f15').rstrip('/') + '/'
spec = importlib.util.spec_from_file_location('cfg', D + 'cfg.py'); CFG = importlib.util.module_from_spec(spec); spec.loader.exec_module(CFG)
A, B, SCENES = CFG.A, CFG.B, CFG.SCENES
CA, CB = BLU, RED                      # France / camp A = turquoise ; camp B = rouge-rose
DUR = json.load(open(D + 'durs.json'))
SEG = []; t = 0.0
for i, s in enumerate(SCENES):
    pre = 0.2 if i == 0 else 0.3
    post = 0.35 if i < len(SCENES) - 1 else getattr(CFG, 'END_HOLD', 1.6)
    SEG.append(dict(i=i, k=f's{i}', scene=s['type'], t0=t, vt=t + pre, dur=DUR[f's{i}'], end=t + pre + DUR[f's{i}'] + post, score=tuple(s['score']), p=s))
    t = SEG[-1]['end']
TOTAL = t
json.dump(dict(seg=[{k: v for k, v in x.items() if k != 'p'} for x in SEG], total=TOTAL), open(D + 'timeline.json', 'w'))
CHK = build_chunks([(s['vt'], s['dur'], s['p']['show']) for s in SEG])
NR = sum(1 for s in SEG if s['scene'] not in ('hook', 'verdict'))

FLIP = getattr(CFG, 'FLIP', {}); TOPROT = getattr(CFG, 'TOPROT', {'a_top': -math.pi / 2, 'b_top': math.pi})
IMG = {}
for sd, col in (('a', CA), ('b', CB)):
    for v in ('34', 'side', 'front', 'top'):
        k = f'{sd}_{v}'
        IMG[k] = neon_image(D + k + '.png', col, rot=TOPROT.get(k, 0) if v == 'top' else 0, flip=bool(FLIP.get(k)))


def side(s):
    return (A, CA, 'a') if s == 'A' else (B, CB, 'b')


def prev_score(sg):
    return SEG[sg['i'] - 1]['score'] if sg['i'] > 0 else (0, 0)


def winner_of(sg):
    p, q = prev_score(sg), sg['score']
    if q[0] > p[0]: return 'A'
    if q[1] > p[1]: return 'B'
    return None


# ---------- HUD ----------
def hud(c, t, sg, lt, u):
    txt(c, "DUEL · MINUTE AÉRO", 54, 150, 30, (*CYA, 0.9), FONT)
    ri = sum(1 for x in SEG[:sg['i'] + 1] if x['scene'] not in ('hook', 'verdict'))
    for k in range(NR):
        on = k < ri
        c.new_path(); c.arc(W - 60 - (NR - 1 - k) * 34, 140, 9, 0, 6.283); c.set_source_rgba(*(YLW if on else DIM), 1 if on else 0.5); c.fill()
    sc = sg['score'] if (u > 0.86 or sg['scene'] in ('hook', 'verdict')) else prev_score(sg)
    if sg['scene'] == 'hook': sc = (0, 0)
    pop = 1.0
    if sg['scene'] not in ('hook', 'verdict') and u > 0.86: pop = 1 + 0.25 * max(0, 1 - (u - 0.86) / 0.05)
    txt(c, A['short'], 300, 262, 72, (*CA, 1), BIG, 'r', glow=1)
    txt(c, B['short'], 780, 262, 72, (*CB, 1), BIG, 'l', glow=1)
    c.save(); c.translate(W / 2, 240); c.scale(pop, pop)
    txt(c, f"{sc[0]} – {sc[1]}", 0, 34, 110, (*YLW, 1), BIG, 'c', glow=1); c.restore()
    p = sg['p']
    if p.get('round'):
        a = ease(lt / 0.35); x0 = 54 - 40 * (1 - a); n = p['round'].split()[-1]
        c.new_path(); c.rectangle(x0, 320, 86, 86); c.set_source_rgba(*YLW, a); c.fill()
        txt(c, n, x0 + 43, 393, 82, (0.02, 0.03, 0.04, a), BIG, 'c')
        F(c, 80, BIG); fs = 80 * min(1, 820 / max(1, c.text_extents(p['title']).x_advance))
        txt(c, p['title'], x0 + 112, 392, fs, (*WHT, a), BIG, glow=1)


def point_stamp(c, sg, u, y=1300):
    w = winner_of(sg)
    a = ap(u, 0.84, 0.9)
    if not w or a <= 0: return
    S, col, _ = side(w)
    s = 1 + 0.3 * (1 - a)
    c.save(); c.translate(W / 2, y); c.scale(s, s)
    glow(c, lambda: (c.new_path(), c.rectangle(-300, -62, 600, 100)), col, a, 4)
    txt(c, f"POINT {S['short']}", 0, 16, 72, (*col, a), BIG, 'c', glow=1); c.restore()


# ---------- scènes ----------
def sc_hook(c, t, sg, lt, u):
    p = sg['p']; a = ease(lt / 0.3)
    F(c, 64, BIG); fs = 64 * min(1, 960 / max(1, c.text_extents(p.get('kicker', '')).x_advance))
    txt(c, p.get('kicker', ''), W / 2, 420, fs, (*YLW, a), BIG, 'c', glow=1)
    ea = ease(lt / 0.9); bob = 10 * math.sin(lt * 1.6)
    draw_surf(c, IMG['a_34'], -300 + ea * 620, 700 + bob, 640, 1)
    draw_surf(c, IMG['b_34'], 1380 - ea * 620, 1110 - bob, 640, 1)
    v = ap(u, 0.2, 0.3); s = 1 + 0.5 * (1 - v)
    c.save(); c.translate(W / 2, 960); c.scale(s, s); txt(c, "VS", 0, 60, 200, (*YLW, v), BIG, 'c', glow=1); c.restore()
    txt(c, A['name'], 120, 560, 56, (*CA, a), BIG, glow=1)
    txt(c, B['name'], W - 120, 1330, 56, (*CB, a), BIG, 'r', glow=1)


def sc_bars(c, t, sg, lt, u):
    p = sg['p']; a = ap(u, 0, 0.08)
    win = 'A' if (p['a'] > p['b']) != bool(p.get('low_wins')) else 'B'
    f = lambda v: p['fmt'].format(v).replace('.', ',')
    first, second = (('a', 0.10), ('b', 0.40)) if p.get('a_first', False) else (('b', 0.10), ('a', 0.40))
    st = dict([first, second])
    for k, (sd, x) in enumerate((('a', W * 0.27), ('b', W * 0.73))):
        col = CA if sd == 'a' else CB
        draw_surf(c, IMG[f'{sd}_side'], x, 580, 470, a)
        g = ap(u, st[sd], st[sd] + 0.2); val = p[sd] * g
        gauge(c, x, 960, 165, min(1, val / p['max']), (A if sd == 'a' else B)['short'], f(val), col, a)
        if u > 0.82 and (win == 'A') == (sd == 'a'):
            r = 200 + 6 * math.sin(lt * 6)
            glow(c, lambda x=x, r=r: (c.new_path(), c.arc(x, 960, r, 0, 6.283)), YLW, ap(u, 0.82, 0.88), 3)
    point_stamp(c, sg, u)


def sc_chips(c, t, sg, lt, u):
    p = sg['p']; S, col, sd = side(p['side']); O, ocol, od = side('B' if p['side'] == 'A' else 'A')
    a = ap(u, 0, 0.1)
    draw_surf(c, IMG[f'{sd}_side'], W / 2 + 40 * (1 - a), 640, 760, a)
    for j, lab in enumerate(p['chips']):
        b = ap(u, 0.15 + j * 0.13, 0.25 + j * 0.13); y = 870 + j * 105
        x0 = 140 + 60 * (1 - b)
        panel(c, x0, y, 800, 88, col, b, 0.10)
        c.new_path(); c.rectangle(x0, y, 14, 88); c.set_source_rgba(*YLW, b); c.fill()
        F(c, 58, BIG); fs = 58 * min(1, 740 / max(1, c.text_extents(lab).x_advance))
        txt(c, lab, x0 + 40, y + 66, fs, (*WHT, b), BIG)
    if p.get('other'):
        b = ap(u, 0.62, 0.72); y = 870 + len(p["chips"]) * 105
        txt(c, f"{O['short']} : {p['other']}", W / 2, y + 50, 46, (*(DIM if p.get('other_grey') else ocol), b), BIG, 'c')
    point_stamp(c, sg, u, 1310)


def sc_list(c, t, sg, lt, u):
    p = sg['p']; a = ap(u, 0, 0.1)
    for sd, x, items, st in (('a', W * 0.27, p['a_items'], p.get('a_start', 0.12)), ('b', W * 0.73, p['b_items'], p.get('b_start', 0.45))):
        col = CA if sd == 'a' else CB
        draw_surf(c, IMG[f'{sd}_front'], x, 640, 380, a)
        for j, it in enumerate(items):
            b = ap(u, st + j * 0.1, st + j * 0.1 + 0.1); y = 900 + j * 120
            panel(c, x - 230, y, 460, 92, col, b, 0.10)
            F(c, 50, BIG); fs = 50 * min(1, 420 / max(1, c.text_extents(it).x_advance))
            txt(c, it, x, y + 64, fs, (*WHT, b), BIG, 'c')
    point_stamp(c, sg, u)


def sc_counters(c, t, sg, lt, u):
    p = sg['p']; a = ap(u, 0, 0.1)
    for sd, x, num, sub, st in (('a', W * 0.27, p['a_num'], p['a_sub'], p.get('a_start', 0.15)), ('b', W * 0.73, p['b_num'], p['b_sub'], p.get('b_start', 0.45))):
        col = CA if sd == 'a' else CB
        draw_surf(c, IMG[f'{sd}_34'], x, 620, 420, a)
        v = num if p.get('static') else int(round(num * ease((u - st) / 0.25)))
        s = (str(v) if p.get('static') else f"{v:,}".replace(',', ' '))
        txt(c, p.get('pre', '') + s + p.get('suffix', ''), x, 1010, 130, (*col, ap(u, st, st + 0.05)), BIG, 'c', glow=1)
        txt(c, sub, x, 1080, 34, (*WHT, ap(u, st, st + 0.05)), FONT, 'c')
    if p.get('pill'): txt(c, p['pill'], W / 2, 1220, 44, (*DIM, ap(u, 0.72, 0.8)), BIG, 'c')
    point_stamp(c, sg, u)


def sc_radar(c, t, sg, lt, u):
    p = sg['p']; a = ap(u, 0, 0.1)
    draw_surf(c, IMG['a_top'], W * 0.28, 760, 460, a); draw_surf(c, IMG['b_top'], W * 0.72, 760, 460, a)
    if p.get('pill'): txt(c, p['pill'], W / 2, 1150, 56, (*YLW, ap(u, 0.2, 0.3)), BIG, 'c', glow=1)
    point_stamp(c, sg, u)


def sc_verdict(c, t, sg, lt, u):
    p = sg['p']; sc = sg['score']; a = ap(u, 0, 0.08)
    w = 'A' if sc[0] > sc[1] else 'B' if sc[1] > sc[0] else None
    if w:
        S, col, sd = side(w)
        draw_surf(c, IMG[f'{sd}_34'], W / 2, 600, 640 + 20 * math.sin(lt), a)
        txt(c, f"VAINQUEUR : {S['name']}", W / 2, 420, 76, (*YLW, a), BIG, 'c', glow=1)
    for j, (lab, s_) in enumerate(p['lines']):
        S, col, _ = side(s_); b = ap(u, 0.08 + j * 0.15, 0.18 + j * 0.15); y = 880 + j * 120
        panel(c, 110, y, 860, 92, col, b, 0.10)
        txt(c, S['short'], 140, y + 64, 50, (*col, b), BIG)
        F(c, 50, BIG); fs = 50 * min(1, 600 / max(1, c.text_extents(lab).x_advance))
        txt(c, lab, 940, y + 64, fs, (*WHT, b), BIG, 'r')
    q = ap(u, 0.62, 0.72)
    txt(c, "ET TOI, QUI GAGNE ?", W / 2, 1200, 90, (*WHT, q), BIG, 'c', glow=1)
    if t > SEG[-1]['vt'] + SEG[-1]['dur'] - 0.5 or u > 0.9:
        b = ease((t - (SEG[-1]['vt'] + SEG[-1]['dur'] - 0.5)) / 0.4)
        sub_button(c, W / 2 + 70, 1680, lt, b)
        sticker(c, 'point_right', 190, 1680, 230, b, -0.05)
        txt(c, "UN DUEL CHAQUE JOUR", W / 2 + 70, 1790, 40, (*CYA, b), FONT, 'c')


SC = dict(hook=sc_hook, bars=sc_bars, chips=sc_chips, list=sc_list, counters=sc_counters, radar=sc_radar, verdict=sc_verdict)


def frame(t):
    sg = next((x for x in SEG if x['t0'] <= t < x['end']), SEG[-1]); lt = t - sg['t0']
    u = min(1, max(0, (t - sg['vt']) / max(0.1, sg['dur'] + 0.3)))
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    background(c, t)
    k = 1 + 0.03 * ease(lt / max(1, sg['end'] - sg['t0']))
    c.save(); c.translate(W / 2, 850); c.scale(k, k); c.translate(-W / 2, -850)
    SC.get(sg['scene'], sc_radar)(c, t, sg, lt, u)
    c.restore()
    if sg['i'] > 0 and lt < 0.22:
        f = lt / 0.22
        c.set_source_rgba(*BLU, 0.30 * (1 - f)); c.paint()
        x = W * f; c.set_source_rgba(*CYA, 0.8 * (1 - f)); c.rectangle(x - 4, 0, 8, H); c.fill()
    hud(c, t, sg, lt, u)
    if sg['scene'] != 'verdict' or t < SEG[-1]['vt'] + SEG[-1]['dur'] - 0.5: subtitles(c, t, CHK)
    c.set_source_rgba(*YLW, 1); c.rectangle(0, H - 8, W * t / TOTAL, 8); c.fill()
    return s


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        for x in sys.argv[2:]: frame(float(x)).write_to_png(D + f'nstill_{x}.png')
        sys.exit()
    ff = ffmpeg_out(D + 'video_noaudio.mp4'); n = int(TOTAL * FPS)
    for i in range(n):
        ff.stdin.write(bytes(frame(i / FPS).get_data()))
        if i % 300 == 0: print(i, '/', n, flush=True)
    ff.stdin.close(); ff.wait(); print('done', TOTAL)
