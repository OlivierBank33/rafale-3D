"""STICKMAN v2 — rendu « qualité max ». Usage : DL=dl/<slug> python3 sm_render2.py [stills t1 ...]
Différences avec v1 (sm_render.py, dont on réutilise toutes les scènes) :
- timeline calée AU MOT sur la vraie voix ElevenLabs (dl/<slug>/align.json, issu de creative_transcribe_audio, 0 crédit) ;
- montage : un plan par phrase (cut toutes les 1,5-3,5 s) avec punch-in alterné, dérive lente de caméra, whip-pan entre scènes ;
- titre d'accroche « slam » + onde de choc, sous-titres karaoké mot à mot (pop du mot actif, chiffres en jaune) ;
- poussière en premier plan, étalonnage, grain, barre de progression ;
- écrit timeline.json (avec shots) pour sm_audio2.py (son calé sur les mêmes instants).
"""
import cairo, json, math, os, re, subprocess, sys, random
import sm_render as R1                       # charge cfg, scènes, helpers (le rendu v1 n'est PAS lancé)
from sm_lib import *
CFG = R1.CFG; SC = R1.SC; D = R1.D; FPS = 30
import sm_scenes6
sm_scenes6.R = R1
SC.update(sm_scenes6.SC6)
ORG, BLUE, RED, WH = R1.ORG, R1.BLUE, R1.RED, R1.WH
YEL = (1.0, 0.85, 0.25)
AL = json.load(open(D + 'align.json'))
SCN = CFG.SCENES; END_HOLD = getattr(CFG, 'END_HOLD', 8.0)
LEAD = 0.22                                   # le plan change juste avant le premier mot


def ease(u): u = min(max(u, 0), 1); return u * u * (3 - 2 * u)
def eout(u): u = min(max(u, 0), 1); return 1 - (1 - u) ** 3
def back(u, s=1.7):
    u = min(max(u, 0), 1) - 1; return 1 + u * u * ((s + 1) * u + s)


# ---------------- timeline au mot ----------------
SEG = []
for i, (s, sents) in enumerate(zip(SCN, AL['scenes'])):
    vs, ve = sents[0][0], sents[-1][1]
    t0 = 0.0 if i == 0 else vs - LEAD
    SEG.append(dict(i=i, k=f's{i}', scene=s['type'], t0=t0, vt=vs, dur=ve - vs, sent=sents, score=(0, 0), p=s))
for i, sg in enumerate(SEG):
    sg['end'] = SEG[i + 1]['t0'] if i + 1 < len(SEG) else AL['voice_end'] + END_HOLD
TOTAL = SEG[-1]['end']
# plans : un par phrase ; un plan trop court (< 1,1 s) est fusionné avec le précédent
for sg in SEG:
    cuts = [sg['t0']] + [a - 0.08 for a, _ in sg['sent'][1:]]
    sh = []
    for c0 in cuts:
        if sh and c0 - sh[-1] < 1.1: continue
        sh.append(c0)
    sg['shots'] = sh
json.dump(dict(seg=[{k: v for k, v in x.items() if k != 'p'} for x in SEG], total=TOTAL, v=2), open(D + 'timeline.json', 'w'))


# ---------------- caméra ----------------
def focus_of(sg):
    return sg['p'].get('focus', (540, 900))


def camera(sg, t):
    """(zoom, cx, cy) : plan pair = large, plan impair = punch-in 1,12 sur le point d'intérêt ; dérive lente ; arrivée en 'settle'."""
    j = max(k for k, c0 in enumerate(sg['shots']) if c0 <= t + 1e-6) if any(c0 <= t + 1e-6 for c0 in sg['shots']) else 0
    a = sg['shots'][j]; b = sg['shots'][j + 1] if j + 1 < len(sg['shots']) else sg['end']
    p = (t - a) / max(0.5, b - a)
    fx, fy = focus_of(sg)
    if j % 2 == 0: z, cx, cy = 1.0, W / 2, H / 2
    else: z, cx, cy = 1.12, fx, fy
    z *= 1 + 0.03 * ease(p)                                  # push-in continu
    if j == 0: z *= 1 + 0.07 * (1 - eout((t - a) / 0.45))     # « settle » à l'entrée de scène
    cx += 14 * math.sin(t * 0.37 + sg['i']); cy += 10 * math.sin(t * 0.29 + 2 * sg['i'])   # dérive douce (pas de shake)
    hw, hh = W / (2 * z), H / (2 * z)
    cx = min(max(cx, hw), W - hw); cy = min(max(cy, hh), H - hh)
    return z, cx, cy, j


# ---------------- sous-titres karaoké ----------------
def spoken_len(w):
    w2 = w.strip('.,?!:;«»"\'\u00a0')
    if re.search(r'\d', w2): return 5 * len(re.sub(r'\D', '', w2)) + 3
    return {'km/h': 16, '°C': 7, '%': 9}.get(w2, len(w2)) + 1


def chunks(words, n=3, maxc=17):
    out, cur = [], []
    for x in words:
        if cur and sum(len(w) for w in cur) + len(x) + len(cur) > maxc: out.append(cur); cur = []
        cur.append(x)
        if len(cur) >= n or x.endswith(('.', '?', '!', ',', ':')): out.append(cur); cur = []
    if cur: out.append(cur)
    return out


CHK = []
for sg in SEG:
    if sg['scene'] in ('choice', 'e2_choice'): continue
    show = re.sub(r' ([?!:;»])', '\u00a0\\1', sg['p']['show']); show = re.sub(r'(\d) (\d{3})', '\\1\u00a0\\2', show)
    sents = [x for x in re.split(r'(?<=[.?!])\s+', show.strip()) if x]
    if len(sents) != len(sg['sent']): sents = [show]; spans = [(sg['vt'], sg['vt'] + sg['dur'])]
    else: spans = sg['sent']
    for stext, (a, b) in zip(sents, spans):
        ws = [x for x in stext.split(' ') if x]; wt = [spoken_len(x) for x in ws]; tot = sum(wt); acc = 0; timed = []
        for x, k in zip(ws, wt):
            s0 = a + (b - a) * acc / tot; acc += k; timed.append((s0, a + (b - a) * acc / tot, x))
        i = 0
        for ch in chunks(ws):
            CHK.append(timed[i:i + len(ch)]); i += len(ch)


def subtitles(c, t):
    cur = [ch for ch in CHK if ch[0][0] - 0.05 <= t < ch[-1][1] + 0.12]
    if not cur: return
    ch = cur[-1]; size = 90; F(c, size, 'Montserrat'); words = [w.upper() for _, _, w in ch]; sp = size * 0.42
    ws = [c.text_extents(w).x_advance for w in words]; tw = sum(ws) + sp * (len(ws) - 1)
    if tw > 960: size = int(size * 960 / tw); F(c, size, 'Montserrat'); ws = [c.text_extents(w).x_advance for w in words]; tw = sum(ws) + sp * (len(ws) - 1)
    pop = back((t - ch[0][0] + 0.05) / 0.16, 2.2); y = 1600; x = W / 2 - tw / 2
    c.save(); c.translate(W / 2, y - size * 0.35); c.scale(0.8 + 0.2 * pop, 0.8 + 0.2 * pop); c.translate(-W / 2, -(y - size * 0.35))
    for i, w in enumerate(words):
        a0, a1, _ = ch[i]; act = a0 <= t < a1 or (i == len(ch) - 1 and t >= a0); said = t >= a0
        col = ORG if act else (YEL if re.search(r'\d', w) else WH)
        s = 1.0 + (0.14 * (1 - eout((t - a0) / 0.18)) if act else 0)
        cxw = x + ws[i] / 2
        c.save(); c.translate(cxw, y - size * 0.35); c.scale(s, s); c.translate(-cxw, -(y - size * 0.35))
        c.move_to(x + 5, y + 7); c.text_path(w); c.set_source_rgba(0, 0, 0, 0.45); c.fill()               # ombre portée
        c.move_to(x, y); c.text_path(w); c.set_source_rgba(0, 0, 0, 1); c.set_line_width(16); c.set_line_join(1); c.stroke()
        c.move_to(x, y); c.text_path(w); c.set_source_rgba(*col, 1.0 if said else 0.55); c.fill()
        c.restore(); x += ws[i] + sp
    c.restore()


# ---------------- titre « slam » ----------------
def title_card(c, sg, lt):
    if sg['scene'] in ('choice', 'e2_choice', 'e2_recap'): return
    mode = getattr(CFG, 'MODE', 'serie')
    if mode != 'serie' and sg['i'] > 0: return
    a = 1 - ease((lt - 2.7) / 0.45)
    if a <= 0: return
    k = back(lt / 0.28, 2.0); s = 1.9 - 0.9 * k
    y = 370
    if sg['i'] == 0 and mode == 'serie':
        text(c, f"ÉPISODE {int(CFG.EP)}", W / 2, 250, 46, (0.85, 0.88, 0.95), 'Montserrat', track=6)
    if sg['i'] == 0 and lt < 0.6:                       # onde de choc
        q = eout(lt / 0.6); c.new_path(); c.arc(W / 2, y - 45, 120 + 520 * q, 0, 7)
        c.set_source_rgba(1, 1, 1, 0.5 * (1 - q)); c.set_line_width(14 * (1 - q) + 2); c.stroke()
    c.push_group(); c.translate(W / 2, y - 45); c.scale(s, s); c.translate(-W / 2, -(y - 45))
    text(c, sg['p']['title'], W / 2, y, 128, RED if sg['i'] == 0 else (0.92, 0.95, 1), glow=1.0)
    c.pop_group_to_source(); c.paint_with_alpha(min(1, lt / 0.08) * a)


# ---------------- poussière / étalonnage ----------------
DUST = [(random.Random(7 + k).random() * W, random.Random(70 + k).random() * H, 2 + 5 * random.Random(700 + k).random(), random.Random(7000 + k).random()) for k in range(34)]
def dust(c, t, z, cx, cy):
    for (x, y, r, ph) in DUST:
        xx = (x + t * (8 + 14 * ph) - (cx - W / 2) * 0.25) % W; yy = (y - t * (5 + 9 * ph) - (cy - H / 2) * 0.25) % H
        a = 0.10 + 0.10 * math.sin(t * 1.3 + ph * 9)
        c.new_path(); c.arc(xx, yy, r * (0.8 + 0.4 * z), 0, 7); c.set_source_rgba(1, 0.97, 0.9, a); c.fill()


RECAP = getattr(CFG, 'RECAP', None)
def recap(c, t):
    """Maintien final : récap de 3 chiffres-clés + appel à s'abonner (pas d'écran figé)."""
    t0 = AL['voice_end'] + 0.9
    if not RECAP or t < t0: return
    a = ease((t - t0) / 0.4); c.set_source_rgba(0.02, 0.02, 0.05, a); c.paint()
    radial(c, W / 2, 900, 700, (0.25, 0.3, 0.6), 0.25 * a); dust(c, t, 1.0, W / 2, H / 2)
    text(c, "À RETENIR", W / 2, 430, 90, (0.85, 0.88, 0.95), 'Montserrat', track=6)
    for j, (big, small, col) in enumerate(RECAP):
        sj = t - t0 - 0.5 - j * 1.6
        if sj <= 0: continue
        k = back(sj / 0.25, 2.2); y = 640 + j * 300
        c.save(); c.translate(W / 2, y); c.scale(1.5 - 0.5 * k, 1.5 - 0.5 * k)
        c.push_group(); text(c, big, 0, 40, 150, col, glow=0.9); text(c, small, 0, 110, 46, WH, 'Montserrat'); c.pop_group_to_source(); c.paint_with_alpha(min(1, sj / 0.08)); c.restore()
    sc = t - t0 - 0.5 - 3 * 1.6 - 0.4
    if sc > 0:
        q = back(sc / 0.3, 2.0) * (1 + 0.05 * math.sin(t * 6))
        c.save(); c.translate(W / 2, 1440); c.scale(q, q)
        rr(c, -300, -70, 600, 140, 70); c.set_source_rgb(*ORG); c.fill()
        text(c, "ABONNE-TOI", 0, 30, 90, (0.05, 0.05, 0.08)); c.restore()


def draw_scene(c, sg, t, extra_z=1.0, dx=0.0):
    lt = t - sg['t0']; u = min(1, max(0, (t - sg['vt']) / max(0.1, sg['dur'] + 0.3)))
    z, cx, cy, j = camera(sg, t); z *= extra_z
    c.save(); c.translate(W / 2 + dx, H / 2); c.scale(z, z); c.translate(-cx, -cy)
    SC[sg['scene']](c, t, sg, lt, u); c.restore()
    return z, cx, cy


WHIP = 0.16
def frame(t):
    i = next((k for k, x in enumerate(SEG) if x['t0'] <= t < x['end']), len(SEG) - 1); sg = SEG[i]; lt = t - sg['t0']
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    out_k = 0.0
    if i + 1 < len(SEG) and sg['end'] - t < 0.12: out_k = ease(1 - (sg['end'] - t) / 0.12)       # sortie : accélération
    in_k = 1 - eout(lt / WHIP) if i > 0 else 0.0                                                 # entrée : glisse
    z, cx, cy = draw_scene(c, sg, t, 1 + 0.18 * out_k, -260 * out_k + 300 * in_k)
    k = max(out_k, in_k)
    if k > 0.02:                                                                                 # traînées du whip
        r = random.Random(int(t * 60))
        for _ in range(26):
            y = r.random() * H; L = 200 + 500 * r.random(); x = r.random() * W
            c.move_to(x, y); c.line_to(x + L, y); c.set_source_rgba(1, 1, 1, 0.22 * k); c.set_line_width(2 + 6 * r.random()); c.stroke()
        c.set_source_rgba(1, 1, 1, 0.22 * in_k); c.paint()
    dust(c, t, z, cx, cy)
    vignette(c, 0.82); grain(c, int(t * 12) % 6, 6000)
    title_card(c, sg, lt); subtitles(c, t); recap(c, t)
    c.set_source_rgba(*ORG, 1); c.rectangle(0, H - 8, W * t / TOTAL, 8); c.fill()
    return s


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        for x in sys.argv[2:]: frame(float(x)).write_to_png(D + f'still_{x}.png')
        sys.exit()
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', D + 'video_noaudio.mp4'], stdin=subprocess.PIPE)
    n = int(TOTAL * FPS)
    for k in range(n):
        ff.stdin.write(bytes(frame(k / FPS).get_data()))
        if k % 300 == 0: print(k, '/', n, flush=True)
    ff.stdin.close(); ff.wait(); print('done', TOTAL)
