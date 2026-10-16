"""VRAI OU FAUX en style néon @minuteaero. Usage : VF=vf16 python3 nv_render.py [stills t1 ...]
Lit <VF>_script.py (INTRO, OUTRO, Q[img, stmt, answer(0=vrai,1=faux), q_say, a_say, a_show, q_show?], THEME?) et <VF>/durs.json ; images r3d/<img>.png.
Même timeline que vfN_render.py (compatible el_sync / vfN_audio.py) : pour el_sync, <VF>_render.py = wrapper qui importe ce module."""
import cairo, json, math, os, sys, importlib
from neon_lib import *

VF = os.environ.get('VF', 'vf15')
S = importlib.import_module(f'{VF}_script'); INTRO, OUTRO, Q = S.INTRO, S.OUTRO, S.Q
THEME = getattr(S, 'THEME', '')
D = json.load(open(f'{VF}/durs.json')); NQ = len(Q); COUNT = 3.0
T = {}; t = 0.3
T['intro'] = t; t += D['intro'] + 0.45
qs = []
for i in range(NQ):
    q0 = t; cd0 = q0 + 0.15 + D[f'q{i}'] + 0.15; rev = cd0 + COUNT; a0 = rev + 0.2; end = a0 + D[f'a{i}'] + 0.55
    qs.append(dict(q0=q0, cd0=cd0, rev=rev, a0=a0, end=end)); t = end
T['outro'] = t + 0.1
TOTAL = T['outro'] + D['outro'] + 2.2
json.dump(dict(T=T, qs=qs, total=TOTAL), open(f'{VF}/timeline.json', 'w'))
NUM = ["un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit"]
items = [(T['intro'], D['intro'], INTRO['show'])]
for i, q in enumerate(Q):
    items.append((qs[i]['q0'] + 0.15, D[f'q{i}'], q.get('q_show', f"N°{i + 1}. {q['stmt']}")))
    items.append((qs[i]['a0'], D[f'a{i}'], q['a_show']))
items.append((T['outro'], D['outro'], OUTRO['show']))
CHK = build_chunks(items)
IMG = [neon_image(f"r3d/{q['img']}.png", BLU, maxdim=1000) for q in Q]


def wrap(c, s, size, maxw, fam=BIG):
    F(c, size, fam); words = s.split(); lines = []; cur = ''
    for w in words:
        tst = (cur + ' ' + w).strip()
        if c.text_extents(tst).x_advance > maxw and cur: lines.append(cur); cur = w
        else: cur = tst
    lines.append(cur); return lines


def header(c, i):
    txt(c, ("VRAI OU FAUX · " + THEME).strip(' ·').upper(), 54, 150, 30, (*CYA, 0.9), FONT)
    for k in range(NQ):
        on = i is not None and k <= i
        c.new_path(); c.arc(W - 60 - (NQ - 1 - k) * 34, 140, 9, 0, 6.283); c.set_source_rgba(*(YLW if on else DIM), 1 if on else 0.5); c.fill()


def btn(c, y, lab, col, state, a):
    """state : 0 neutre, 1 bonne réponse, -1 éliminée"""
    x0, w, h = 140, 800, 120
    if state == 1:
        c.new_path(); c.rectangle(x0, y, w, h); c.set_source_rgba(*col, 0.35 * a); c.fill()
    glow(c, lambda: (c.new_path(), c.rectangle(x0, y, w, h)), col, a * (0.25 if state == -1 else 1), 4 if state == 1 else 2.5)
    txt(c, lab, W / 2, y + 92, 96, (*(WHT if state != -1 else DIM), a * (0.35 if state == -1 else 1)), BIG, 'c', glow=1 if state == 1 else 0)


def sc_intro(c, t, lt):
    a = ease(lt / 0.3)
    txt(c, "VRAI", W / 2, 430, 190, (*BLU, a), BIG, 'c', glow=1)
    txt(c, "OU FAUX ?", W / 2, 590, 170, (*RED, ease((lt - 0.2) / 0.3)), BIG, 'c', glow=1)
    draw_surf(c, IMG[0], W / 2, 900 + 8 * math.sin(lt * 1.5), 700, ease((lt - 0.4) / 0.4))
    b = ease((lt - 1.2) / 0.3)
    if THEME: txt(c, THEME.upper(), W / 2, 1180, 64, (*YLW, b), BIG, 'c', glow=1)
    txt(c, f"{NQ} AFFIRMATIONS · 3 SECONDES", W / 2, 1250, 40, (*CYA, b), FONT, 'c')


def sc_q(c, t, i):
    q, tm = Q[i], qs[i]; lt = t - tm['q0']; a = ease(lt / 0.3)
    c.new_path(); c.rectangle(54 - 40 * (1 - a), 190, 86, 86); c.set_source_rgba(*YLW, a); c.fill()
    txt(c, str(i + 1), 97 - 40 * (1 - a), 263, 82, (0.02, 0.03, 0.04, a), BIG, 'c')
    txt(c, "AFFIRMATION", 166 - 40 * (1 - a), 262, 80, (*WHT, a), BIG, glow=1)
    lines = wrap(c, q['stmt'].upper(), 74, 960)
    for k, ln in enumerate(lines): txt(c, ln, W / 2, 380 + k * 78, 74, (*WHT, a), BIG, 'c')
    enter = ease(lt / 0.5); bob = 8 * math.sin(lt * 1.4)
    reveal = t >= tm['rev']
    draw_surf(c, IMG[i], W / 2 + (1 - enter) * W * 0.6, 760 + bob, 720, enter)
    st = [0, 0]
    if reveal:
        good = q['answer']; st[good] = 1; st[1 - good] = -1
    btn(c, 1060, "VRAI", BLU, st[0], a); btn(c, 1210, "FAUX", RED, st[1], a)
    if tm['cd0'] <= t < tm['rev']:
        k = t - tm['cd0']; n = 3 - int(k); f = k - int(k)
        r = 95; cx, cy = W - 150, 780
        glow(c, lambda: (c.new_path(), c.arc(cx, cy, r, -math.pi / 2, -math.pi / 2 + 6.283 * (1 - k / COUNT))), YLW, 1, 6)
        s = 1 + 0.3 * (1 - f)
        c.save(); c.translate(cx, cy); c.scale(s, s); txt(c, str(n), 0, 44, 130, (*YLW, 1), BIG, 'c', glow=1); c.restore()
    if reveal:
        b = ease((t - tm['rev']) / 0.2); good = q['answer']; col = BLU if good == 0 else RED
        s = 1 + 0.25 * (1 - b)
        c.save(); c.translate(W / 2, 600); c.rotate(-0.05); c.scale(s, s)
        glow(c, lambda: (c.new_path(), c.rectangle(-330, -95, 660, 140)), col, b, 5)
        txt(c, "C'EST VRAI !" if good == 0 else "C'EST FAUX !", 0, 22, 110, (*col, b), BIG, 'c', glow=1); c.restore()
        sticker(c, 'wink_thumb' if good == 0 else 'shocked', 130, 1730, 200, b, -0.06)


def sc_outro(c, t):
    lt = t - T['outro']; a = ease(lt / 0.3)
    txt(c, "TON SCORE", W / 2, 430, 140, (*WHT, a), BIG, 'c', glow=1)
    txt(c, f"SUR {NQ} ?", W / 2, 560, 120, (*YLW, a), BIG, 'c', glow=1)
    rows = [("0 – 1", "TOURISTE", DIM), ("2 – 3", "PASSAGER", CYA), ("4 – 5", "PILOTE", BLU), (str(NQ), "AS DU MANCHE", YLW)]
    for k, (sc, lab, col) in enumerate(rows):
        b = ease((lt - 0.2 - k * 0.15) / 0.25); y = 680 + k * 120
        panel(c, 140, y, 800, 96, col, b, 0.08)
        txt(c, sc, 180, y + 70, 64, (*col, b), BIG); txt(c, lab, 900, y + 70, 64, (*WHT, b), BIG, 'r')
    b = ease((lt - 1.2) / 0.3)
    txt(c, "ÉCRIS-LE EN COMMENTAIRE", W / 2, 1230, 52, (*CYA, b), BIG, 'c')
    sub_button(c, W / 2 + 70, 1690, lt, ease((lt - D['outro']) / 0.4))
    sticker(c, 'point_right', 190, 1690, 230, ease((lt - D['outro']) / 0.4), -0.05)


def frame(t):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    background(c, t)
    i = next((k for k, q in enumerate(qs) if q['q0'] <= t < q['end']), None)
    if t < qs[0]['q0']: header(c, None); sc_intro(c, t, t - T['intro'])
    elif i is not None: header(c, i); sc_q(c, t, i)
    else: header(c, NQ - 1); sc_outro(c, t)
    starts = [qs[0]['q0']] + [q['q0'] for q in qs[1:]] + [T['outro'] - 0.1]
    for st in starts:
        if 0 <= t - st < 0.22:
            f = (t - st) / 0.22; c.set_source_rgba(*BLU, 0.3 * (1 - f)); c.paint()
            c.set_source_rgba(*CYA, 0.8 * (1 - f)); c.rectangle(W * f - 4, 0, 8, H); c.fill()
    if t < T['outro'] + D['outro']: subtitles(c, t, CHK)
    c.set_source_rgba(*YLW, 1); c.rectangle(0, H - 8, W * t / TOTAL, 8); c.fill()
    if t > TOTAL - 0.4: c.set_source_rgba(0, 0, 0, (t - (TOTAL - 0.4)) / 0.4); c.paint()
    return s


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        for x in sys.argv[2:]: frame(float(x)).write_to_png(f'{VF}/nstill_{x}.png')
        sys.exit()
    ff = ffmpeg_out(f'{VF}/video_noaudio.mp4'); n = int(TOTAL * FPS)
    for k in range(n):
        ff.stdin.write(bytes(frame(k / FPS).get_data()))
        if k % 300 == 0: print(k, '/', n, flush=True)
    ff.stdin.close(); ff.wait(); print('done', TOTAL)
