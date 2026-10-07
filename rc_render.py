"""Moteur « Récit » : histoire vraie racontée, ciel haute altitude, panneau radio, mascotte narratrice.
Usage : DL=dl/<slug> python3 rc_render.py [stills t1 t2 ...]  (cfg.py : SCENES, END_HOLD ; durs.json ; images r3d/ ou dossier)"""
import cairo, json, math, os, re, subprocess, sys, random, importlib.util
import numpy as np
import mascot as _M, mascot_fx as _MF

W, H, FPS = 1080, 1920, 30
D = os.environ.get('DL', 'dl/recit_sr71').rstrip('/') + '/'
spec = importlib.util.spec_from_file_location('cfg', D + 'cfg.py'); CFG = importlib.util.module_from_spec(spec); spec.loader.exec_module(CFG)
SCENES = CFG.SCENES
DUR = json.load(open(D + 'durs.json'))
YEL = (1.0, 0.84, 0.1); WHITE = (1, 1, 1); CYA = (0.35, 0.85, 1.0); RED = (1.0, 0.3, 0.3); INK = (0.05, 0.05, 0.08)

SEG = []; t = 0.0
for i, s in enumerate(SCENES):
    pre = 0.2 if i == 0 else 0.3
    post = 0.35 if i < len(SCENES) - 1 else getattr(CFG, 'END_HOLD', 2.0)
    SEG.append(dict(i=i, k=f's{i}', scene=s['type'], t0=t, vt=t + pre, dur=DUR[f's{i}'], end=t + pre + DUR[f's{i}'] + post, score=(0, 0), p=s))
    t = SEG[-1]['end']
TOTAL = t
json.dump(dict(seg=[{k: v for k, v in x.items() if k != 'p'} for x in SEG], total=TOTAL), open(D + 'timeline.json', 'w'))

_img = {}


def img(name):
    if name not in _img:
        p = D + name + '.png'
        if not os.path.exists(p): p = 'r3d/' + name + '.png'
        _img[name] = cairo.ImageSurface.create_from_png(p)
    return _img[name]


def ease(u):
    u = min(max(u, 0), 1); return u * u * (3 - 2 * u)


def ease_out(u):
    u = min(max(u, 0), 1); return 1 - (1 - u) ** 3


def back_out(u):
    u = min(max(u, 0), 1); k = 1.70158
    return 1 + (k + 1) * (u - 1) ** 3 + k * (u - 1) ** 2


def font(c, size, bold=True):
    c.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL); c.set_font_size(size)


def text_c(c, txt, x, y, size, rgba=(1, 1, 1, 1), stroke=0, maxw=None):
    font(c, size); e = c.text_extents(txt)
    if maxw and e.x_advance > maxw:
        size *= maxw / e.x_advance; font(c, size); e = c.text_extents(txt)
    c.move_to(x - e.x_advance / 2, y); c.text_path(txt)
    if stroke:
        c.set_source_rgba(0, 0, 0, 0.85 * rgba[3]); c.set_line_width(stroke); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
    c.set_source_rgba(*rgba); c.fill(); c.new_path()


def wrap(c, txt, size, maxw):
    font(c, size); out, cur = [], ''
    for w_ in txt.split():
        tr = (cur + ' ' + w_).strip()
        if c.text_extents(tr).x_advance > maxw and cur: out.append(cur); cur = w_
        else: cur = tr
    if cur: out.append(cur)
    return out


def rrect(c, x, y, w, h, r):
    c.new_path(); r = min(r, w / 2, h / 2)
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2); c.close_path()


def sprite(c, name, cx, cy, width, alpha=1.0, flip=False, rot=0.0, halo=True):
    sf = img(name); sw = sf.get_width(); s = width / sw
    if halo:
        g = cairo.RadialGradient(cx, cy, 0, cx, cy, width * 0.42)
        g.add_color_stop_rgba(0, 0.55, 0.75, 1.0, 0.28 * alpha); g.add_color_stop_rgba(1, 0.55, 0.75, 1.0, 0)
        c.set_source(g); c.arc(cx, cy, width * 0.42, 0, 2 * math.pi); c.fill()
    c.save(); c.translate(cx, cy); c.rotate(rot)
    if flip: c.scale(-1, 1)
    c.scale(s, s); c.set_source_surface(sf, -sw / 2, -sf.get_height() / 2); c.paint_with_alpha(alpha); c.restore()


# ---------------------------------------------------------------- ciel haute altitude
random.seed(11)
STARS = [(random.uniform(0, W), random.uniform(0, 1100), random.uniform(0.6, 2.2), random.uniform(0, 6.3)) for _ in range(140)]
CLOUDS = [(random.uniform(0, 1), random.uniform(0, 1), random.uniform(60, 200), random.uniform(0.04, 0.12)) for _ in range(70)]


def sky(c, t, speed=1.0):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.0, 0.0, 0.02); g.add_color_stop_rgb(0.45, 0.02, 0.05, 0.16); g.add_color_stop_rgb(0.68, 0.10, 0.25, 0.55)
    g.add_color_stop_rgb(0.72, 0.55, 0.78, 1.0); g.add_color_stop_rgb(0.75, 0.10, 0.16, 0.28); g.add_color_stop_rgb(1, 0.03, 0.05, 0.09)
    c.set_source(g); c.paint()
    for (x, y, r, ph) in STARS:
        a = 0.35 + 0.35 * math.sin(t * 1.3 + ph)
        c.set_source_rgba(1, 1, 1, a * (1 - y / 1300)); c.arc(x, y, r, 0, 2 * math.pi); c.fill()
    # courbure de la Terre : halo atmosphérique
    cy = 1380 + 2600
    for k, (w_, a) in enumerate(((60, 0.10), (26, 0.22), (8, 0.55))):
        c.set_source_rgba(0.55, 0.85, 1.0, a); c.set_line_width(w_); c.arc(W / 2, cy, 2600, 0, 2 * math.pi); c.stroke()
    # sol sous la courbure, nuages qui défilent (parallaxe = vitesse)
    c.save(); c.arc(W / 2, cy, 2600, 0, 2 * math.pi); c.clip()
    for (u, v, r, a) in CLOUDS:
        y = 1400 + v * 520
        x = (u * (W + 600) - t * 22 * speed * (0.5 + v)) % (W + 600) - 300
        rg = cairo.RadialGradient(x, y, 0, x, y, r * (0.6 + v)); rg.add_color_stop_rgba(0, 0.85, 0.9, 1.0, a); rg.add_color_stop_rgba(1, 0.85, 0.9, 1.0, 0)
        c.set_source(rg); c.save(); c.translate(x, y); c.scale(2.4, 0.6); c.arc(0, 0, r * (0.6 + v), 0, 2 * math.pi); c.restore(); c.fill()
    c.restore()


def contrail(c, x0, y0, x1, y1, a):
    g = cairo.LinearGradient(x0, y0, x1, y1); g.add_color_stop_rgba(0, 1, 1, 1, 0.0); g.add_color_stop_rgba(1, 1, 1, 1, 0.45 * a)
    c.set_source(g); c.set_line_width(14); c.set_line_cap(cairo.LINE_CAP_ROUND); c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()


# ---------------------------------------------------------------- scènes
RADIO = [s for s in SEG if s['scene'] == 'radio']
KMAX = max(s['p']['kt'] for s in RADIO)


def radio_panel(c, t, upto, cur=None, a=1.0, y0=330):
    rows = [s for s in RADIO if s['p']['n'] <= upto]
    h = 130 + 150 * len(rows)
    c.save(); c.translate(0, (1 - a) * -40)
    rrect(c, 60, y0, W - 120, h, 34); c.set_source_rgba(0.02, 0.05, 0.12, 0.82 * a); c.fill_preserve()
    c.set_source_rgba(*CYA, 0.6 * a); c.set_line_width(3); c.stroke()
    c.move_to(110, y0 + 70); c.set_source_rgba(*CYA, a); font(c, 34); c.show_text("LOS ANGELES CENTER · VITESSE SOL")
    for j, s in enumerate(rows):
        p = s['p']; y = y0 + 130 + j * 150
        u = (t - s['vt'] - s['dur'] * 0.55) / 0.9 if s is cur else 1.0
        if s is cur and t < s['vt'] + s['dur'] * 0.55: u = 0
        v = p['kt'] * ease_out(u)
        big = p['kt'] == KMAX
        col = RED if big else WHITE
        font(c, 38); c.set_source_rgba(*(YEL if s is cur else (0.8, 0.85, 0.95)), a); c.move_to(110, y + 10); c.show_text(p['who'])
        txt = f"{int(round(v)):,}".replace(',', ' ') + " KT"
        font(c, 46); e = c.text_extents(txt); c.set_source_rgba(*col, a); c.move_to(W - 110 - e.x_advance, y + 14); c.show_text(txt)
        # barre proportionnelle (échelle linéaire : l'écart saute aux yeux)
        bw = (W - 220) * (v / KMAX)
        rrect(c, 110, y + 40, W - 220, 22, 11); c.set_source_rgba(1, 1, 1, 0.10 * a); c.fill()
        if bw > 4:
            rrect(c, 110, y + 40, max(22, bw), 22, 11); c.set_source_rgba(*(RED if big else CYA), 0.95 * a); c.fill()
    c.restore()


def sc_hook(c, t, s):
    lt = t - s['t0']
    sky(c, t, 3.0)
    x = W + 300 - (lt / 3.2) * (W + 900)
    contrail(c, x + 1400, 815, x + 330, 805, 1)
    sprite(c, 'sr_side', x, 800, 900, flip=True)
    a = back_out((lt - 0.15) / 0.35)
    lines = wrap(c, s['p']['title'], 76, 960)
    for k, ln in enumerate(lines):
        col = YEL if k == len(lines) - 1 else WHITE
        text_c(c, ln, W / 2, 330 + k * 92, 76 * max(a, 0.01), (*col, 1), stroke=10)
    b = back_out((lt - 1.4) / 0.35)
    if b > 0:
        c.save(); c.translate(W / 2, 1190); c.rotate(-0.04); c.scale(b, b)
        rrect(c, -230, -50, 460, 100, 50); c.set_source_rgba(*RED, 1); c.fill()
        text_c(c, "HISTOIRE VRAIE", 0, 18, 46); c.restore()


def sc_story(c, t, s):
    lt = t - s['t0']; u = lt / (s['end'] - s['t0'])
    sky(c, t, 1.5)
    x = W / 2 + 60 - u * 120; y = 860 + 10 * math.sin(t * 1.4)
    if s['p']['img'] == 'sr_side':
        contrail(c, x + 1300, y + 30, x + 0.36 * (980 + 60 * u), y + 15, ease(lt / 0.6))
    sprite(c, s['p']['img'], x, y, 980 + 60 * u, flip=True)
    a = back_out((lt - 0.4) / 0.35)
    if a > 0:
        c.save(); c.translate(W / 2, 360); c.scale(a, a)
        font(c, 40); e = c.text_extents(s['p']['badge']); bw = e.x_advance + 70
        rrect(c, -bw / 2, -45, bw, 90, 45); c.set_source_rgba(0.02, 0.05, 0.12, 0.85); c.fill_preserve(); c.set_source_rgba(*CYA, 1); c.set_line_width(3); c.stroke()
        c.set_source_rgba(*CYA, 1); c.move_to(-e.x_advance / 2, 14); c.show_text(s['p']['badge']); c.restore()


def sc_radio(c, t, s):
    lt = t - s['t0']; p = s['p']
    sky(c, t, 1.0)
    if p.get('img'):
        sprite(c, p['img'], W / 2, 1180 + 8 * math.sin(t * 1.6), 620, alpha=ease(lt / 0.4), flip=(p['img'] != 'sr71'))
    radio_panel(c, t, p['n'], cur=s, a=1.0)


def sc_ask(c, t, s):
    lt = t - s['t0']
    sky(c, t, 2.0)
    sprite(c, s['p']['img'], W / 2, 1050 + 10 * math.sin(t * 1.2), 900 + 40 * lt / 6, flip=True)
    # ondes radio
    for k in range(3):
        r = ((lt * 220 + k * 120) % 360) + 40
        c.set_source_rgba(*CYA, max(0, 0.6 - r / 600)); c.set_line_width(6); c.arc(W / 2, 1000, r, -2.4, -0.7); c.stroke()
    a = back_out((lt - 0.8) / 0.35)
    if a > 0:
        q = "« VOUS AVEZ NOTRE VITESSE SOL ? »"
        c.save(); c.translate(W / 2, 430); c.scale(a, a)
        rrect(c, -480, -110, 960, 200, 40); c.set_source_rgba(1, 1, 1, 0.95); c.fill()
        font(c, 40); c.set_source_rgba(*CYA, 1); c.move_to(-440, -40); c.show_text("ASPEN 20 · SR-71")
        text_c(c, q, 0, 40, 50, (0.05, 0.08, 0.15, 1), maxw=900); c.restore()


def sc_punch(c, t, s):
    lt = t - s['t0']
    sky(c, t, 4.0)
    sprite(c, s['p']['img'], W / 2, 1050 + 6 * math.sin(t * 1.5), 980, flip=True)
    a = back_out((lt - 1.8) / 0.4)
    if a > 0:
        c.save(); c.translate(W / 2, 470); c.rotate(-0.03); c.scale(a, a)
        rrect(c, -490, -150, 980, 290, 44); c.set_source_rgba(*YEL, 1); c.fill()
        text_c(c, "« NOUS, ON L'A", 0, -30, 80, (0.05, 0.05, 0.08, 1), maxw=900)
        text_c(c, "À 1 841. »", 0, 80, 96, (0.05, 0.05, 0.08, 1), maxw=900); c.restore()


def sc_verdict(c, t, s):
    lt = t - s['t0']
    sky(c, t, 5.0)
    radio_panel(c, t, 99, cur=None, a=min(1, max(0, 1 - (lt - 2.2) / 0.4)), y0=330)
    b = back_out((lt - 2.4) / 0.4)
    if b > 0:
        c.save(); c.translate(W / 2, 640); c.scale(b, b)
        text_c(c, "1 842 NŒUDS", 0, 0, 120, (*RED, 1), stroke=12, maxw=980)
        text_c(c, "= 3 412 KM/H", 0, 130, 100, (1, 1, 1, 1), stroke=10, maxw=980); c.restore()
    k = back_out((lt - 3.4) / 0.4)
    if k > 0:
        text_c(c, "Histoire racontée par le pilote Brian Shul", W / 2, 1000, 40 * k, (0.8, 0.85, 0.95, 1), maxw=900)
    e = back_out((t - s['vt'] - s['dur'] - 0.1) / 0.35)
    if e > 0:
        c.save(); c.translate(W / 2, 1300); c.scale(e, e)
        rrect(c, -470, -55, 940, 110, 55); c.set_source_rgba(*YEL, 1); c.fill()
        text_c(c, "ABONNE-TOI · HISTOIRES VRAIES", 0, 18, 48, (0.05, 0.05, 0.08, 1), maxw=860); c.restore()


SCN = dict(hook=sc_hook, story=sc_story, radio=sc_radio, ask=sc_ask, punch=sc_punch, verdict=sc_verdict)

# ---------------------------------------------------------------- sous-titres (mots répartis sur la durée parlée)
CAPS = []
for s in SEG:
    words = re.sub(r' ([?!:;»])', '\u00a0\\1', s['p']['show'].replace('« ', '«')).split(' ')
    n = len(words); per = s['dur'] / max(1, sum(len(w_) + 2 for w_ in words))
    tt = s['vt']; chunk = []
    for w_ in words:
        d = (len(w_) + 2) * per; chunk.append((w_, tt, tt + d)); tt += d
        if len(chunk) >= 3 or w_.endswith(('.', ',', '?', '!', ':', '»')):
            CAPS.append(chunk); chunk = []
    if chunk: CAPS.append(chunk)
CAP_CX = 690


def captions(c, t):
    cur = None
    for ch in CAPS:
        if ch[0][1] - 0.02 <= t < ch[-1][2] + 0.05: cur = ch
    if not cur: return
    words = [w_.upper() for w_, _, _ in cur]
    size = 66; font(c, size)
    sp = c.text_extents(' ').x_advance; ws = [c.text_extents(w_).x_advance for w_ in words]; tot = sum(ws) + sp * (len(ws) - 1)
    if tot > 640:
        size *= 640 / tot; font(c, size); sp = c.text_extents(' ').x_advance; ws = [c.text_extents(w_).x_advance for w_ in words]; tot = sum(ws) + sp * (len(ws) - 1)
    x = CAP_CX - tot / 2; y = 1640
    for w_, wd, (_, a, b) in zip(words, ws, cur):
        c.move_to(x, y); c.text_path(w_)
        c.set_source_rgba(0, 0, 0, 0.9); c.set_line_width(13); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
        c.set_source_rgb(*(YEL if a <= t < b + 0.05 else WHITE)); c.fill(); c.new_path(); x += wd + sp


# ---------------------------------------------------------------- mascotte narratrice
MOUTH = _MF.envelope([(D + s['k'] + '.wav', s['vt']) for s in SEG], TOTAL, FPS)


def m_state(t, s):
    p = s['p']
    if s['scene'] == 'hook' and t < s['t0'] + 1.3: return 'shocked', s['t0']
    if s['scene'] == 'radio' and p['n'] == 2 and t > s['vt'] + s['dur'] * 0.6: return 'skeptical', s['vt'] + s['dur'] * 0.6
    if s['scene'] == 'radio' and p['kt'] == KMAX and t > s['vt'] + s['dur'] * 0.6: return 'shocked', s['vt'] + s['dur'] * 0.6
    if s['scene'] == 'punch' and t > s['t0'] + 1.8: return 'laugh', s['t0'] + 1.8
    if s['scene'] == 'verdict' and t > s['vt'] + s['dur'] + 0.1: return 'wink_thumb', s['vt'] + s['dur'] + 0.1
    return 'neutral', None


def draw_mascot(c, t, s):
    f = min(len(MOUTH) - 1, int(t * FPS)); m = float(MOUTH[f])
    pose, t0 = m_state(t, s)
    if pose != 'neutral': m = 0.0
    enter = ease_out((t - 0.1) / 0.45) if t < 0.6 else 1.0
    bob = 5 * math.sin(t * 2.4) + (1 - enter) * 600
    _M.draw(c, 200, 1968 + bob, 560, pose=pose, mouth=m, blink=_MF.blink(t), pop=_MF.pop(t, t0), tilt=-0.02 + 0.015 * math.sin(t * 1.1))


_LAYER = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)


def render(t, surf):
    s = SEG[0]
    for x in SEG:
        if t >= x['t0']: s = x
    lc = cairo.Context(_LAYER); SCN[s['scene']](lc, t, s); _LAYER.flush()
    c = cairo.Context(surf)
    lt = t - s['t0']; z = 1.0 + 0.03 * min(1.0, lt / max(1.0, s['end'] - s['t0']))
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-W / 2, -H / 2); c.set_source_surface(_LAYER, 0, 0); c.paint(); c.restore()
    draw_mascot(c, t, s)
    captions(c, t)
    if lt < 0.12 and s['t0'] > 0:
        c.set_source_rgba(1, 1, 1, 0.35 * (1 - lt / 0.12)); c.paint()
    c.set_source_rgba(*YEL, 1); c.rectangle(0, 0, W * t / TOTAL, 6); c.fill()
    if t > TOTAL - 0.4:
        c.set_source_rgba(0, 0, 0, (t - (TOTAL - 0.4)) / 0.4); c.paint()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        for tt in map(float, sys.argv[2:]):
            sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); render(tt, sf); sf.write_to_png(D + f'still_{tt:.1f}.png')
        print(round(TOTAL, 1), [(x['scene'], round(x['t0'], 1)) for x in SEG]); sys.exit()
    nframes = int(TOTAL * FPS)
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', D + 'video_noaudio.mp4'], stdin=subprocess.PIPE)
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    for f in range(nframes):
        render(f / FPS, sf); sf.flush(); ff.stdin.write(bytes(sf.get_data()))
        if f % 300 == 0: print(f, '/', nframes, flush=True)
    ff.stdin.close(); ff.wait(); print('done', TOTAL)
