"""Moteur « Pixel » : vidéo en pixel art (rendu 180x320, agrandi x6 sans lissage).
Usage : DL=dl/<slug> python3 pa_render.py [stills t1 t2 ...]   (cfg.py : SCENES[type,title,say,show], END_HOLD ; durs.json)
Types : hook gorilla tunnel night bulb descent alarm crash cause fix verdict"""
import json, math, os, re, subprocess, sys, random, importlib.util
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import mascot_fx as _MF

W, H, S, FPS = 180, 320, 6, 30
D = os.environ.get('DL', 'dl/pa_tunnel').rstrip('/') + '/'
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

FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pipe', 'fonts')
_f = {}


def F(sz, kind='sk'):
    k = (sz, kind)
    if k not in _f: _f[k] = ImageFont.truetype(os.path.join(FD, 'Silkscreen-Bold.ttf' if kind == 'sk' else 'PressStart2P.ttf'), sz)
    return _f[k]


BG = (3, 3, 12); WHITE = (236, 236, 244); RED = (232, 62, 48); RED_D = (100, 14, 10); BLUE = (100, 145, 255); BLUE_D = (15, 25, 90)
YEL = (238, 206, 92); YEL_D = (150, 115, 30); GREEN = (70, 220, 90); GREEN_D = (10, 70, 20); GREY = (70, 70, 92); AMBER = (255, 160, 30)


def txt(d, x, y, s, sz, col, sh=(0, 0, 0), kind='sk', anchor='la'):
    f = F(sz, kind)
    d.text((x + 1, y + 1), s, font=f, fill=sh, anchor=anchor); d.text((x, y), s, font=f, fill=col, anchor=anchor)


def tw(s, sz, kind='sk'):
    return F(sz, kind).getlength(s)


def ease(u):
    u = min(max(u, 0), 1); return u * u * (3 - 2 * u)


def ease_out(u):
    u = min(max(u, 0), 1); return 1 - (1 - u) ** 3


# ---------- sprites ----------
def pixelize(im, h, cols=14, thr=110):
    im = im.convert('RGBA'); w = max(1, round(im.width * h / im.height))
    s = im.resize((w, h), Image.LANCZOS); a = s.split()[3].point(lambda v: 255 if v > thr else 0)
    q = s.convert('RGB').quantize(cols, method=Image.Quantize.MEDIANCUT).convert('RGB'); q.putalpha(a)
    # contour sombre 1 px
    m = np.array(a) > 0; o = np.zeros_like(m)
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)): o |= np.roll(np.roll(m, dy, 0), dx, 1)
    o &= ~m; arr = np.array(q); arr[o] = (8, 8, 20, 255); return Image.fromarray(arr)


_MS = {}
MDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mascot', 'stickers')


def mascot(pose, h=66):
    k = (pose, h)
    if k not in _MS: _MS[k] = pixelize(Image.open(os.path.join(MDIR, pose + '.png')), h, 20)
    return _MS[k]


def stars(d, t, n=60, seed=7, col=((30, 40, 110), (50, 60, 150), (90, 100, 190))):
    r = random.Random(seed)
    for i in range(n):
        x, y = r.randrange(W), r.randrange(H); ph = r.random() * 6
        c = col[int((math.sin(t * 2 + ph) * 0.5 + 0.5) * (len(col) - 0.01))]
        d.point((x, y), fill=c)


def dither_rect(d, x0, y0, x1, y1, pal, vertical=True):
    for yy in range(int(y0), int(y1)):
        tt = 1 - (yy - y0) / max(1, (y1 - y0))
        for xx in range(int(x0), int(x1)):
            v = tt * (len(pal) - 1) + ((xx + yy) % 2) * 0.5
            d.point((xx, yy), fill=pal[min(len(pal) - 1, int(v))])


def stamp(d, cx, y, s, u, col=YEL, dark=YEL_D, ink=(16, 16, 22), sz=16):
    if u <= 0: return
    w = tw(s, sz) + 14; k = 1 + 0.6 * max(0, 1 - u * 5)
    w2 = w * k; h2 = (sz + 10) * k
    d.rectangle([cx - w2 / 2, y, cx + w2 / 2, y + h2], fill=col); d.rectangle([cx - w2 / 2, y + h2 - 2, cx + w2 / 2, y + h2], fill=dark)
    if k < 1.05: txt(d, cx, y + 4, s, sz, ink, dark, anchor='ma')


def vignette(img, cx, cy, r, soft=6):
    """Effet tunnel : noir hors d'un cercle, bord tramé."""
    a = np.array(img).astype(np.int16)
    yy, xx = np.mgrid[0:H, 0:W]; dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    bay = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0
    th = bay[yy % 4, xx % 4]
    m = (dist - r) / soft > th
    a[m] = (2, 2, 6); return Image.fromarray(a.astype(np.uint8))


def airliner(d, x, y, k=1.0, ang=0.0, lights=True, t=0.0):
    """TriStar en pixel (vue de profil, nez à droite)."""
    pts = []
    def P(px, py):
        ca, sa = math.cos(ang), math.sin(ang); return (x + (px * ca - py * sa) * k, y + (px * sa + py * ca) * k)
    body = [P(-30, -3), P(24, -3), P(30, 0), P(24, 3), P(-30, 3), P(-34, 0)]
    d.polygon(body, fill=(200, 205, 215)); d.line([P(-30, 1), P(26, 1)], fill=(40, 80, 190))
    d.polygon([P(-30, -3), P(-36, -14), P(-30, -14), P(-22, -3)], fill=(190, 195, 205))  # dérive
    d.polygon([P(-31, -6), P(-24, -6), P(-24, -3), P(-31, -3)], fill=(120, 125, 140))  # réacteur central (S-duct)
    d.polygon([P(-8, 2), P(4, 2), P(-12, 9), P(-18, 9)], fill=(160, 165, 178))  # aile
    d.rectangle([P(-6, 4)[0] - 3, P(-6, 4)[1], P(-6, 4)[0] + 4, P(-6, 4)[1] + 2], fill=(110, 115, 130))
    for i in range(-24, 20, 4): d.point(P(i, -1), fill=(255, 230, 140))
    if lights and int(t * 2.2) % 2 == 0: d.point(P(-36, -14), fill=(255, 60, 60)); d.point(P(30, 0), fill=(255, 255, 255))


def pilot_back(d, x, y, col=(40, 40, 60)):
    col = tuple(min(255, c + 30) for c in col)
    d.ellipse([x - 5, y - 12, x + 5, y - 2], fill=(70, 50, 40)); d.arc([x - 5, y - 13, x + 5, y - 3], 180, 360, fill=(20, 20, 25)); d.rectangle([x - 8, y - 2, x + 8, y + 12], fill=col)


def ball(d, x, y, col=(230, 120, 40)):
    d.rectangle([x - 1, y - 1, x + 1, y + 1], fill=col)


def player(d, x, y, col, t, ph):
    leg = int(math.sin(t * 9 + ph) * 2)
    d.rectangle([x - 2, y - 11, x + 2, y - 8], fill=(230, 180, 140)); d.rectangle([x - 3, y - 7, x + 3, y], fill=col)
    d.line([x - 2, y, x - 2 + leg, y + 5], fill=col); d.line([x + 2, y, x + 2 - leg, y + 5], fill=col)


def gorilla_big(img, x, y, t, beat=False, k=2):
    g = Image.new('RGBA', (40, 40), (0, 0, 0, 0)); gorilla(ImageDraw.Draw(g), 20, 30, t, beat, (34, 34, 40), (90, 90, 100))
    g = g.resize((40 * k, 40 * k), Image.NEAREST); img.paste(g, (int(x - 20 * k), int(y - 30 * k)), g)


def gorilla(d, x, y, t, beat=False, G=(20, 20, 26), G2=(60, 60, 70)):
    leg = int(math.sin(t * 6) * 2)
    d.ellipse([x - 5, y - 22, x + 5, y - 13], fill=G); d.rectangle([x - 3, y - 18, x + 3, y - 15], fill=G2)
    d.ellipse([x - 9, y - 15, x + 9, y + 2], fill=G)
    if beat:
        d.line([x - 9, y - 10, x - 3, y - 7], fill=G2, width=2); d.line([x + 9, y - 10, x + 3, y - 7], fill=G2, width=2)
    else:
        d.line([x - 9, y - 10, x - 11, y + 2], fill=G, width=3); d.line([x + 9, y - 10, x + 11, y + 2], fill=G, width=3)
    d.line([x - 4, y, x - 4 + leg, y + 7], fill=G, width=3); d.line([x + 4, y, x + 4 - leg, y + 7], fill=G, width=3)


def bulb_icon(d, cx, cy, on, broken=False, r=10):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 235, 120) if on else (60, 60, 75), outline=(10, 10, 20))
    d.rectangle([cx - r // 2, cy + r - 2, cx + r // 2, cy + r + 6], fill=(150, 150, 165)); d.line([cx - r // 2, cy + r + 2, cx + r // 2, cy + r + 2], fill=(90, 90, 100))
    if broken:
        d.line([cx - 4, cy + 2, cx - 1, cy - 3], fill=(20, 20, 30)); d.line([cx + 1, cy - 3, cx + 4, cy + 3], fill=(20, 20, 30))
    elif on:
        for a in range(0, 360, 45):
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            d.line([cx + ca * (r + 3), cy + sa * (r + 3), cx + ca * (r + 7), cy + sa * (r + 7)], fill=(255, 235, 120))


def gear_panel(d, x, y, nose_on, u_pulse):
    d.rectangle([x, y, x + 74, y + 40], fill=(28, 30, 40), outline=(70, 75, 95))
    txt(d, x + 37, y + 3, "GEAR", 8, (170, 175, 195), (0, 0, 0), anchor='ma')
    for i, (lx, on) in enumerate(((x + 14, True), (x + 37, nose_on), (x + 60, True))):
        c = GREEN if on else ((70, 30, 30) if u_pulse else (45, 45, 55))
        d.rectangle([lx - 6, y + 16, lx + 6, y + 28], fill=c, outline=(10, 10, 15))
        if on: d.rectangle([lx - 4, y + 18, lx - 1, y + 20], fill=(180, 255, 180))
    txt(d, x + 37, y + 31, "NOSE", 8, (120, 125, 145), (0, 0, 0), anchor='ma')


def altimeter(d, x, y, ft, warn=False, blink=False):
    d.rectangle([x, y, x + 64, y + 30], fill=(10, 12, 18), outline=(200, 120, 30) if (warn and blink) else (70, 75, 95))
    txt(d, x + 4, y + 3, "ALT FT", 8, (130, 135, 155), (0, 0, 0))
    txt(d, x + 60, y + 13, f"{max(0, int(ft)):04d}", 16, AMBER if warn else GREEN, (0, 0, 0), kind='sk', anchor='ra')


# ---------- légendes ----------
def chunks(show, n=4):
    show = re.sub(r' ([?!:;»])', '\u00a0\\1', show); show = re.sub(r'(«) ', '\\1\u00a0', show)
    w = show.split(); out = []; cur = []
    for x in w:
        cur.append(x)
        if len(cur) >= n or x.endswith(('.', '?', '!', ',')): out.append(' '.join(cur)); cur = []
    if cur: out.append(' '.join(cur))
    return out


CH = []
for sg in SEG:
    cs = chunks(sg['p']['show']); tot = sum(len(c) for c in cs); acc = 0
    for c in cs:
        a = sg['vt'] + sg['dur'] * acc / tot; acc += len(c); CH.append((a, sg['vt'] + sg['dur'] * acc / tot, c))


def wrap(s, sz, maxw):
    words = s.replace('\u00a0', '\x00').split(); lines = []; cur = ''
    for w_ in words:
        t2 = (cur + ' ' + w_).strip()
        if tw(t2.replace('\x00', ' '), sz) > maxw and cur: lines.append(cur); cur = w_
        else: cur = t2
    lines.append(cur); return [l.replace('\x00', ' ') for l in lines]


HI = {'tunnel', 'gorille', 'aveugle', 'tuer', 'moitié', 'stress', 'ampoule', 'ampoule.', 'grillée.', 'alarme', '101', 'règle', 'vole,', 'panne.', 'gorille ?', 'altitude.', 'TriStar', '176', '1972.', '1999,'}


def captions(d, t, cx=112, y=258, maxw=128):
    cur = [c for c in CH if c[0] <= t < c[1] + 0.05]
    if not cur: return
    a, b, s = cur[-1]; lines = wrap(s.upper(), 8, maxw)
    yy = y - (len(lines) - 1) * 6
    for ln in lines:
        x = cx - tw(ln, 8) / 2
        for w_ in ln.split(' '):
            col = YEL if w_.lower().strip('.,?!') in {h.strip('.,?!').lower() for h in HI} else WHITE
            txt(d, x, yy, w_, 8, col, (0, 0, 0)); x += tw(w_ + ' ', 8)
        yy += 12


# ---------- mascotte ----------
MOUTH = _MF.envelope([(D + f"s{sg['i']}.wav", sg['vt']) for sg in SEG], TOTAL, FPS)
POSE = dict(hook='shocked', gorilla='point_up', tunnel='skeptical', night=None, bulb=None, descent=None, alarm=None, crash=None, cause=None, fix='point_up', verdict='wink_thumb')


def draw_mascot(img, t, sg, u):
    if sg['scene'] in ('crash',): return
    pose = POSE.get(sg['scene'])
    if sg['scene'] == 'gorilla' and u > 0.78: pose = 'shocked'
    if pose is None or (t - sg['vt']) > 1.6 and sg['scene'] not in ('verdict', 'hook'):
        m = MOUTH[min(len(MOUTH) - 1, int(t * FPS))]
        pose = 'blink' if _MF.blink(t) else ('talk_wide' if m > 0.55 else ('talk' if m > 0.18 else 'neutral'))
    sp = mascot(pose); bob = 1 if int(t * 2) % 2 else 0
    img.paste(sp, (0, H - sp.height + 4 + bob), sp)


# ---------- scènes ----------
def title(d, s, t0, t, col=RED, sh=RED_D, y=26):
    if not s: return
    u = ease_out((t - t0) / 0.35); n = int(len(s) * min(1, (t - t0) / 0.5) + 0.999)
    lines = wrap(s, 16, 168); k = 0
    for j, ln in enumerate(lines):
        vis = ln[:max(0, n - k)]; k += len(ln) + 1
        txt(d, W // 2, y - int((1 - u) * 6) + j * 18, vis, 16, col, sh, anchor='ma')


def sc_hook(img, d, t, u, sg):
    stars(d, t)
    cx, cy = 90, 130; open_ = min(1, (t - sg['t0']) / 0.4)
    ry = int(26 * open_); d.ellipse([cx - 52, cy - ry, cx + 52, cy + ry], fill=(235, 235, 240), outline=(10, 10, 20))
    if ry > 6:
        ix = cx + int(math.sin(t * 1.3) * 10); d.ellipse([ix - 20, cy - 20, ix + 20, cy + 20], fill=(40, 90, 200)); d.ellipse([ix - 10, cy - 10, ix + 10, cy + 10], fill=(5, 5, 10))
        d.rectangle([ix - 7, cy - 9, ix - 3, cy - 5], fill=(255, 255, 255))
        img = vignette(img, cx, cy, 160 - 115 * ease(u * 1.2), 10); d = ImageDraw.Draw(img)
    title(d, sg['p']['title'], sg['t0'] + 0.3, t)
    return img, d


def sc_gorilla(img, d, t, u, sg):
    d.rectangle([8, 60, 172, 200], fill=(150, 95, 50)); d.rectangle([8, 60, 172, 200], outline=(230, 220, 200))
    d.ellipse([60, 105, 120, 155], outline=(230, 220, 200)); d.line([90, 60, 90, 200], fill=(230, 220, 200))
    P = [(40, 100, (245, 245, 250)), (130, 95, (245, 245, 250)), (85, 175, (245, 245, 250)), (60, 150, (20, 20, 28)), (120, 140, (20, 20, 28)), (100, 85, (20, 20, 28))]
    for i, (x, y, c) in enumerate(P):
        player(d, x + int(math.sin(t * 1.5 + i) * 8), y + int(math.cos(t * 1.2 + i * 2) * 5), c, t, i)
    k = int((t - sg['t0']) / 0.9); a = P[k % 3]; b = P[(k + 1) % 3]; f = ((t - sg['t0']) / 0.9) % 1
    ball(d, a[0] + (b[0] - a[0]) * f, a[1] - 6 + (b[1] - a[1]) * f - math.sin(f * math.pi) * 14)
    txt(d, 14, 205, f"PASSES : {min(k, 15)}", 8, WHITE, (0, 0, 0), kind='ps')
    gu = (u - 0.42) / 0.33
    pass
    if 0 < gu < 1: gorilla_big(img, int(-10 + 200 * gu), 150, t, beat=0.45 < gu < 0.6, k=2); d = ImageDraw.Draw(img)
    title(d, sg['p']['title'], sg['t0'] + 0.2, t, y=10)
    if u > 0.8: stamp(d, 90, 216, "1 SUR 2 NE L'A PAS VU", (u - 0.8) * 4, sz=8)
    return img, d


def sc_tunnel(img, d, t, u, sg):
    stars(d, t)
    icons = [(30, 80, 'cloud'), (150, 90, 'alarm'), (30, 200, 'plane'), (150, 205, 'alt'), (90, 70, 'radio'), (88, 220, 'fuel')]
    for x, y, k in icons:
        if k == 'cloud': d.ellipse([x - 12, y - 6, x + 12, y + 6], fill=(140, 150, 180))
        elif k == 'alarm': d.rectangle([x - 10, y - 8, x + 10, y + 8], fill=AMBER if int(t * 3) % 2 else (120, 70, 10)); txt(d, x, y - 4, "!", 8, (0, 0, 0), AMBER, anchor='ma')
        elif k == 'plane': airliner(d, x, y, 0.5, 0, False)
        elif k == 'alt': altimeter(d, x - 32, y - 15, 2000 - 400 * u)
        elif k == 'radio': d.rectangle([x - 9, y - 6, x + 9, y + 6], fill=(60, 140, 200)); txt(d, x, y - 4, "ATC", 8, (0, 0, 0), (60, 140, 200), anchor='ma')
        else: d.rectangle([x - 8, y - 6, x + 8, y + 6], fill=(90, 200, 90)); txt(d, x, y - 4, "F", 8, (0, 0, 0), (90, 200, 90), anchor='ma')
    bulb_icon(d, 90, 142, True)
    r = 140 - 112 * ease(u * 1.15)
    img = vignette(img, 90, 145, r, 8); d = ImageDraw.Draw(img)
    title(d, sg['p']['title'], sg['t0'] + 0.2, t)
    if u > 0.62:
        txt(d, 90, 205, "STRESS", 8, RED, RED_D, anchor='ma'); txt(d, 90, 216, "= TUNNEL PLUS ÉTROIT", 8, WHITE, (0, 0, 0), anchor='ma')
    return img, d


def ground_lights(d, t, y0=230, seed=3):
    r = random.Random(seed)
    for i in range(70):
        x = r.randrange(W); y = y0 + int(r.random() ** 2 * 40); c = r.choice([(255, 200, 90), (255, 230, 160), (200, 160, 80)])
        if (i + int(t * 3)) % 9: d.point((x, y), fill=c)


def sc_night(img, d, t, u, sg):
    stars(d, t, 80)
    d.rectangle([0, 228, W, H], fill=(6, 8, 14)); ground_lights(d, t)
    airliner(d, 30 + 130 * u, 130 + 20 * u, 1.3, 0.05, True, t)
    title(d, sg['p']['title'], sg['t0'] + 0.2, t)
    if u > 0.45: txt(d, 90, 60, "NEW YORK > MIAMI", 8, BLUE, BLUE_D, anchor='ma')
    if u > 0.65: txt(d, 90, 74, "176 À BORD", 8, WHITE, (0, 0, 0), anchor='ma')
    return img, d


def cockpit(d, t, nose_on, pulse):
    d.rectangle([0, 50, W, 230], fill=(12, 14, 22))
    d.polygon([(0, 50), (60, 50), (40, 95), (0, 95)], fill=(8, 10, 30)); d.polygon([(180, 50), (120, 50), (140, 95), (180, 95)], fill=(8, 10, 30))
    d.polygon([(62, 50), (118, 50), (136, 95), (44, 95)], fill=(10, 14, 36))
    for i in range(12): d.point(((i * 37) % 180, 60 + (i * 13) % 30), fill=(60, 70, 140))
    d.rectangle([0, 95, W, 230], fill=(26, 28, 38))
    gear_panel(d, 53, 112, nose_on, pulse)


def sc_bulb(img, d, t, u, sg):
    cockpit(d, t, False, int(t * 3) % 2)
    if u > 0.45:
        k = ease((u - 0.45) / 0.3)
        for i, x in enumerate((40, 90, 140)):
            px = x + (90 - x) * 0.35 * k; pilot_back(d, int(px), int(220 - 8 * k), (34, 36, 52))
    title(d, sg['p']['title'], sg['t0'] + 0.2, t)
    return img, d


def sc_descent(img, d, t, u, sg):
    cockpit(d, t, False, int(t * 3) % 2)
    ap_on = u < 0.4
    d.rectangle([12, 162, 62, 180], fill=GREEN_D if ap_on else (30, 30, 36), outline=GREEN if ap_on else GREY)
    txt(d, 37, 166, "ALT HOLD", 8, GREEN if ap_on else GREY, (0, 0, 0), anchor='ma')
    ft = 2000 if u < 0.4 else 2000 - 450 * (u - 0.4) / 0.6
    altimeter(d, 108, 158, ft)
    for i, x in enumerate((60, 90, 120)): pilot_back(d, x, 214, (34, 36, 52))
    if u > 0.4 and int(t * 2) % 2: txt(d, 140, 192, "▼", 8, AMBER, (0, 0, 0), kind='ps', anchor='ma')
    title(d, sg['p']['title'], sg['t0'] + 0.2, t)
    return img, d


def sc_alarm(img, d, t, u, sg):
    cockpit(d, t, False, int(t * 3) % 2)
    ft = 1550 - 400 * u; bl = int(t * 4) % 2
    altimeter(d, 108, 158, ft, True, bl)
    if bl: d.rectangle([12, 160, 62, 178], fill=AMBER); txt(d, 37, 164, "ALT", 8, (0, 0, 0), AMBER, anchor='ma')
    for i, x in enumerate((60, 90, 120)): pilot_back(d, x, 214, (34, 36, 52))
    k = ease(u / 0.5); img = vignette(img, 90, 134, 150 - 118 * k, 6); d = ImageDraw.Draw(img)
    for j in range(3):
        ph = (t * 1.3 + j / 3) % 1
        txt(d, int(20 + ph * 10), int(200 - ph * 40), "♪", 8, (255, 190, 80), (0, 0, 0), kind='ps')
    title(d, sg['p']['title'], sg['t0'] + 0.2, t, AMBER, (110, 60, 0))
    return img, d


def sc_crash(img, d, t, u, sg):
    if u < 0.5:
        cockpit(d, t, False, 1)
        ft = 1100 * (1 - u / 0.5) ** 1.3
        altimeter(d, 58, 150, ft, True, int(t * 6) % 2)
        txt(d, 90, 70, f"{max(0, 10 - int(u / 0.5 * 10))} S", 16, RED, RED_D, anchor='ma')
    else:
        a = min(1, (u - 0.6) / 0.15)
        if a > 0:
            c = tuple(int(v * a) for v in WHITE); txt(d, 90, 130, "101", 16, c, (0, 0, 0), kind='ps', anchor='ma')
            txt(d, 90, 152, "MORTS", 8, c, (0, 0, 0), kind='ps', anchor='ma')
            txt(d, 90, 170, "EVERGLADES · 1972", 8, tuple(int(v * a * 0.6) for v in WHITE), (0, 0, 0), anchor='ma')
    return img, d


def sc_cause(img, d, t, u, sg):
    stars(d, t, 40)
    bulb_icon(d, 90, 120, False, True, 24)
    title(d, sg['p']['title'], sg['t0'] + 0.2, t)
    if u > 0.1: txt(d, 90, 168, "TRAIN SORTI ✓", 8, GREEN, GREEN_D, anchor='ma')
    if u > 0.45: stamp(d, 90, 186, "AMPOULE GRILLÉE", (u - 0.45) * 4, RED, RED_D, WHITE, 8)
    return img, d


def sc_fix(img, d, t, u, sg):
    stars(d, t, 40)
    for i, (x, lab, col) in enumerate(((50, "PILOTE", BLUE), (130, "PANNE", AMBER))):
        if u > 0.25 + 0.2 * i:
            d.rectangle([x - 30, 80, x + 30, 170], fill=(18, 20, 32), outline=col)
            pilot_back(d, x, 128, col)
            if i == 0:
                d.rectangle([x - 12, 140, x + 12, 144], fill=(200, 200, 210)); d.rectangle([x - 2, 144, x + 2, 156], fill=(200, 200, 210))
            else:
                d.rectangle([x - 9, 136, x + 9, 160], fill=(230, 230, 220))
                for k in range(4): d.line([x - 6, 140 + k * 5, x + 6, 140 + k * 5], fill=(80, 80, 90))
            txt(d, x, 174, lab, 8, col, (0, 0, 0), anchor='ma')
    title(d, sg['p']['title'], sg['t0'] + 0.2, t, BLUE, BLUE_D)
    if u > 0.75: txt(d, 90, 200, "CRM", 16, WHITE, (0, 0, 0), kind='ps', anchor='ma')
    return img, d


def sc_verdict(img, d, t, u, sg):
    stars(d, t)
    gy = 200 - int(ease((t - sg['t0']) / 0.8) * 40)
    gorilla_big(img, 128, gy, t, beat=int(t * 2) % 2 == 0, k=3); d = ImageDraw.Draw(img)
    d.rectangle([0, 196, W, H], fill=BG)
    title(d, sg['p']['title'], sg['t0'] + 0.2, t, YEL, YEL_D, 50)
    txt(d, 60, 90, "TU L'AURAIS", 8, WHITE, (0, 0, 0), anchor='ma'); txt(d, 60, 102, "VU ?", 16, WHITE, (0, 0, 0), anchor='ma')
    if t > sg['vt'] + sg['dur'] * 0.5:
        stamp(d, 90, 206, "ABONNE-TOI", (t - sg['vt'] - sg['dur'] * 0.5) * 3, RED, RED_D, WHITE, 16)
        txt(d, 90, 236, "@MINUTEAERO", 8, (150, 155, 180), (0, 0, 0), anchor='ma')
    return img, d


SC = dict(hook=sc_hook, gorilla=sc_gorilla, tunnel=sc_tunnel, night=sc_night, bulb=sc_bulb, descent=sc_descent, alarm=sc_alarm,
          crash=sc_crash, cause=sc_cause, fix=sc_fix, verdict=sc_verdict)


def frame(t):
    sg = next((s for s in SEG if s['t0'] <= t < s['end']), SEG[-1])
    u = min(1, max(0, (t - sg['vt']) / max(0.1, sg['dur'] + 0.3)))
    img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img)
    img, d = SC[sg['scene']](img, d, t, u, sg)
    # transition : dissolution en blocs
    tt = t - sg['t0']
    if sg['i'] > 0 and tt < 0.3:
        r = random.Random(int(t * FPS)); k = 1 - tt / 0.3
        for by in range(0, H, 10):
            for bx in range(0, W, 10):
                if r.random() < k: d.rectangle([bx, by, bx + 9, by + 9], fill=BG)
    if sg['scene'] not in ('verdict',) or t < sg['vt'] + sg['dur'] * 0.5: captions(d, t)
    draw_mascot(img, t, sg, u)
    # barre de progression
    d.rectangle([0, 0, int(W * t / TOTAL), 1], fill=YEL)
    return img.resize((W * S, H * S), Image.NEAREST)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        for x in sys.argv[2:]: frame(float(x)).save(D + f'still_{x}.png')
        sys.exit()
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W * S}x{H * S}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', D + 'video_noaudio.mp4'], stdin=subprocess.PIPE)
    n = int(TOTAL * FPS)
    for i in range(n):
        ff.stdin.write(frame(i / FPS).tobytes())
        if i % 300 == 0: print(i, '/', n, flush=True)
    ff.stdin.close(); ff.wait(); print('done', TOTAL)
