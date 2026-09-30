import cairo, json, math, subprocess, sys, re, random
import numpy as np
from PIL import Image, ImageFilter, ImageOps
from tournoi_script import *

W, H, FPS = 1080, 1920, 30
D = json.load(open('tn/durs.json'))
ALL = DUELS + FINAL
YEL = (1.0, 0.84, 0.1); GRN = (0.25, 0.9, 0.45); RED = (1.0, 0.28, 0.3); CYA = (0.35, 0.85, 1.0)
GOLD = (1.0, 0.78, 0.2)


def ease(u):
    u = min(max(u, 0), 1); return u * u * (3 - 2 * u)


def ease_out(u):
    u = min(max(u, 0), 1); return 1 - (1 - u) ** 3


def back_out(u):
    u = min(max(u, 0), 1); c = 1.70158
    return 1 + (c + 1) * (u - 1) ** 3 + c * (u - 1) ** 2


# ---------- Timeline ----------
SEQ = []
t = 0.3
SEQ.append(dict(kind='bracket', stage=0, t0=t, voice='intro', vt=t + 0.2, end=t + 0.2 + D['intro'] + 0.5)); t = SEQ[-1]['end']
for i in range(len(ALL)):
    if i == 4:
        SEQ.append(dict(kind='bracket', stage=1, t0=t, voice='semis', vt=t + 0.5, end=t + 2.3)); t = SEQ[-1]['end']
    if i == 6:
        SEQ.append(dict(kind='bracket', stage=2, t0=t, voice='final', vt=t + 0.3, end=t + 0.3 + D['final'] + 0.4)); t = SEQ[-1]['end']
    susp = 2.0 if i == 8 else 1.5
    q0 = t; qv = q0 + 0.35
    s0 = qv + D[f'q{i}'] + 0.1
    rev = s0 + susp
    rv = rev + 0.25
    end = rv + D[f'r{i}'] + 0.45
    SEQ.append(dict(kind='duel', i=i, t0=q0, voice=f'q{i}', vt=qv, s0=s0, rev=rev, rvoice=f'r{i}', rvt=rv, end=end)); t = end
SEQ.append(dict(kind='champion', t0=t, voice='outro', vt=t + 1.4, end=t + 1.4 + D['outro'] + 1.8)); t = SEQ[-1]['end']
TOTAL = t
json.dump(dict(seq=SEQ, total=TOTAL), open('tn/timeline.json', 'w'))


# ---------- Images ----------
def to_surface(img):
    a = np.array(img.convert('RGBA')).astype(np.float32)
    al = a[..., 3:4] / 255.0; rgb = a[..., :3] * al
    bgra = np.dstack([rgb[..., 2], rgb[..., 1], rgb[..., 0], a[..., 3]]).astype(np.uint8)
    h, w = bgra.shape[:2]
    stride = cairo.ImageSurface.format_stride_for_width(cairo.FORMAT_ARGB32, w)
    buf = np.zeros((h, stride // 4, 4), np.uint8); buf[:, :w] = bgra
    return cairo.ImageSurface.create_for_data(bytearray(buf.tobytes()), cairo.FORMAT_ARGB32, w, h, stride)


def prep(key, bw, bh, pad=30):
    im = Image.open(f"r3d/{key}.png").convert('RGBA'); im = im.crop(im.getbbox())
    sc = min(bw / im.width, bh / im.height)
    im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
    big = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0)); big.alpha_composite(im, (pad, pad))
    al = big.split()[3]
    gray = ImageOps.grayscale(big.convert('RGB')).point(lambda v: int(v * 0.55)).convert('RGBA'); gray.putalpha(al)
    glow = Image.new('RGBA', big.size, (255, 200, 60, 255))
    glow.putalpha(al.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.8)))
    return dict(c=to_surface(big), g=to_surface(gray), glow=to_surface(glow), w=big.width, h=big.height)


BIG = {k: prep(k, 860, 330) for k in PLANES}
THUMB = {k: prep(k, 190, 95, pad=6) for k in PLANES}
CHAMP = prep('sr71', 1000, 560, pad=40)


# ---------- Helpers ----------
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


def text_l(c, txt, x, y, size, rgba=(1, 1, 1, 1), stroke=0):
    font(c, size); c.move_to(x, y); c.text_path(txt)
    if stroke:
        c.set_source_rgba(0, 0, 0, 0.85 * rgba[3]); c.set_line_width(stroke); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
    c.set_source_rgba(*rgba); c.fill(); c.new_path()


def rrect(c, x, y, w, h, r):
    c.new_path()
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2); c.close_path()


def img(c, im, key, cx, cy, s, a):
    if a <= 0: return
    c.save(); c.translate(cx, cy); c.scale(s, s); c.translate(-im['w'] / 2, -im['h'] / 2)
    c.set_source_surface(im[key], 0, 0); c.paint_with_alpha(min(1, a)); c.restore()


def background(c, t, burst=0.0, warm=False):
    g = cairo.RadialGradient(W / 2, 950, 60, W / 2, 950, 1300)
    g.add_color_stop_rgb(0, *((0.3, 0.12, 0.08) if warm else (0.09, 0.14, 0.3))); g.add_color_stop_rgb(1, 0.01, 0.015, 0.04)
    c.set_source(g); c.paint()
    n = 18; rot = t * 0.1
    c.save(); c.translate(W / 2, 950)
    for k in range(n):
        a0 = rot + k * 2 * math.pi / n
        c.move_to(0, 0); c.arc(0, 0, 1600, a0, a0 + math.pi / n * 0.5); c.close_path()
    c.set_source_rgba(1, 1, 1, 0.022 + 0.08 * burst); c.fill(); c.restore()


def fmt_like(label, v):
    m = re.search(r'\d{1,3}(?: \d{3})*(?:,\d+)?', label)
    if not m: return label
    num = m.group(0); dec = len(num.split(',')[1]) if ',' in num else 0
    s = f"{v:,.{dec}f}".replace(',', ' ').replace('.', ',')
    return label[:m.start()] + s + label[m.end():]


def pill(c, txt, cx, y, size, bg, fg=(0.03, 0.05, 0.1)):
    font(c, size); e = c.text_extents(txt); bw = e.x_advance + size * 1.4; bh = size * 1.75
    rrect(c, cx - bw / 2, y, bw, bh, bh / 2); c.set_source_rgba(*bg, 1); c.fill()
    c.set_source_rgb(*fg); c.move_to(cx - e.x_advance / 2, y + bh / 2 + size * 0.36); c.show_text(txt)


# ---------- Duel ----------
def score_at(t):
    """Score de la finale (sr71, an225) au temps t."""
    sa = sb = 0
    for s in SEQ:
        if s['kind'] == 'duel' and s['i'] >= 6 and t >= s['rev'] + 0.3:
            if ALL[s['i']]['win'] == 'a': sa += 1
            else: sb += 1
    return sa, sb


def draw_card(c, t, s, m, side, cy_img, name_y, gauge_y):
    key = m[side]; im = BIG[key]
    lt = t - s['t0']
    enter = ease_out((lt - (0 if side == 'a' else 0.12)) / 0.45)
    dx = (1 - enter) * (W if side == 'a' else -W)
    revealed = t >= s['rev']; ru = t - s['rev']
    win = revealed and m['win'] == side; lose = revealed and not win
    final = s['i'] >= 6
    # nom
    text_l(c, PLANES[key].upper(), 90 + dx, name_y, 48, (1, 1, 1, 1), stroke=7)
    # image
    bob = 6 * math.sin(t * 2 + (0 if side == 'a' else 1.7))
    sc = 1.0
    if win: sc = 1 + 0.06 * math.sin(min(1, ru / 0.35) * math.pi) + 0.03 * ease(ru / 2)
    if win: img(c, im, 'glow', W / 2 + dx, cy_img + bob, sc, min(1, ru / 0.2) * (0.9 if not final else 0.6))
    if lose and not final:
        k = ease(ru / 0.35)
        img(c, im, 'c', W / 2 + dx, cy_img + bob, sc, 1 - k)
        img(c, im, 'g', W / 2 + dx, cy_img + bob, sc, k)
    else:
        img(c, im, 'c', W / 2 + dx, cy_img + bob, sc, 1)
    # jauge
    x0, gw, gh = 90 + dx, 900, 64
    rrect(c, x0, gauge_y, gw, gh, gh / 2); c.set_source_rgba(1, 1, 1, 0.12); c.fill()
    mx = max(m['va'], m['vb']); val = m['va'] if side == 'a' else m['vb']
    if t < s['s0']:
        frac = 0; label = ''
    elif not revealed:
        u = (t - s['s0'])
        frac = 0.45 + 0.28 * math.sin(u * 9 + (0 if side == 'a' else 2.1)) * math.sin(u * 3.3 + 1)
        label = '???'
    else:
        k = ease_out(ru / 0.7)
        frac = max(0.08, val / mx) * k + (0.45) * (1 - k)
        label = fmt_like(m['la'] if side == 'a' else m['lb'], val * k) if k < 0.999 else (m['la'] if side == 'a' else m['lb'])
    if frac > 0:
        col = (GRN if win else RED) if revealed else CYA
        fw = max(gh, gw * min(1, frac))
        rrect(c, x0, gauge_y, fw, gh, gh / 2)
        g = cairo.LinearGradient(x0, 0, x0 + fw, 0)
        g.add_color_stop_rgba(0, col[0] * 0.6, col[1] * 0.6, col[2] * 0.6, 1); g.add_color_stop_rgba(1, *col, 1)
        c.set_source(g); c.fill()
    if label:
        text_l(c, label, x0 + 26, gauge_y + 45, 38, (1, 1, 1, 1), stroke=6)
    # tampon
    if revealed:
        u = back_out((ru - 0.55) / 0.3)
        if u > 0:
            if final:
                txt, col = ('+1', GRN) if win else ('', RED)
            else:
                txt, col = ('QUALIFIÉ', GRN) if win else ('ÉLIMINÉ', RED)
            if txt:
                c.save(); c.translate(W - 230, cy_img - 120); c.rotate(-0.12); c.scale(u * 1.0, u * 1.0)
                font(c, 50); e = c.text_extents(txt); bw = e.x_advance + 50
                rrect(c, -bw / 2, -45, bw, 90, 16); c.set_source_rgba(*col, 0.95); c.fill_preserve()
                c.set_source_rgba(1, 1, 1, 0.9); c.set_line_width(4); c.stroke()
                c.set_source_rgb(1, 1, 1); c.move_to(-e.x_advance / 2, 18); c.show_text(txt)
                c.restore()


def duel_frame(c, t, s):
    m = ALL[s['i']]; lt = t - s['t0']
    revealed = t >= s['rev']; ru = t - s['rev']
    background(c, t, burst=max(0, 1 - ru / 1.0) if revealed else 0.15 * (t > s['s0']), warm=s['i'] >= 6)
    # en-tête
    a = back_out(lt / 0.35)
    c.save(); c.translate(W / 2, 100); c.scale(a, a); c.translate(-W / 2, -100)
    pill(c, m['rnd'], W / 2, 72, 30, GOLD if s['i'] >= 6 else YEL)
    c.restore()
    text_c(c, m['crit'], W / 2, 215, 64 * a, (1, 1, 1, 1), stroke=9, maxw=1000)
    if s['i'] >= 6:
        sa, sb = score_at(t)
        text_c(c, f"SR-71  {sa} – {sb}  AN-225", W / 2, 290, 44, (*GOLD, 1), stroke=7)
    # cartes
    draw_card(c, t, s, m, 'a', 530, 395, 735)
    draw_card(c, t, s, m, 'b', 1150, 1015, 1355)
    # VS / pari
    vy = 885
    pulse = 1 + 0.08 * math.sin(t * 10) if (s['s0'] <= t < s['rev']) else 1
    vu = back_out((lt - 0.3) / 0.35)
    c.save(); c.translate(W / 2, vy); c.scale(vu * pulse, vu * pulse)
    c.new_path(); c.arc(0, 0, 70, 0, 2 * math.pi); c.set_source_rgba(*RED, 1); c.fill_preserve()
    c.set_source_rgba(1, 1, 1, 1); c.set_line_width(5); c.stroke()
    text_c(c, "VS", 0, 22, 62, (1, 1, 1, 1))
    c.restore()
    if s['s0'] <= t < s['rev']:
        u = back_out((t - s['s0']) / 0.3)
        text_l(c, "TON PARI ?", 90, vy + 18, 44 * u, (*YEL, 1), stroke=7)
        text_l(c, "A ou B", W - 250, vy + 18, 44 * u, (*YEL, 1), stroke=7)
    # lettres A/B
    if revealed and ru < 0.2:
        c.set_source_rgba(1, 1, 1, 0.5 * (1 - ru / 0.2)); c.paint()
    if s['end'] - t < 0.18:
        c.set_source_rgba(0.01, 0.015, 0.04, 1 - (s['end'] - t) / 0.18); c.paint()
    if lt < 0.12:
        c.set_source_rgba(0.01, 0.015, 0.04, 1 - lt / 0.12); c.paint()


# ---------- Tableau ----------
QF_Y = [360 + k * 145 for k in range(8)]
SF_Y = [(QF_Y[2 * k] + QF_Y[2 * k + 1]) / 2 for k in range(4)]
F_Y = [(SF_Y[0] + SF_Y[1]) / 2, (SF_Y[2] + SF_Y[3]) / 2]
COLX = [190, 540, 890]
SF_ENT = ['sr71', 'm2000', 'a10', 'an225']
F_ENT = ['sr71', 'an225']
QF_LOSERS = {'concorde', 'f22', 'spitfire', 'b2'}
SF_LOSERS = {'m2000', 'a10'}


def slot(c, key, x, y, state, a=1.0, s=1.0):
    bw, bh = 250, 120
    c.save(); c.translate(x, y); c.scale(s, s)
    rrect(c, -bw / 2, -bh / 2, bw, bh, 18)
    c.set_source_rgba(0.05, 0.08, 0.16, 0.92 * a); c.fill_preserve()
    col = {'win': GOLD, 'lose': (0.5, 0.2, 0.22), 'on': (1, 1, 1), 'empty': (1, 1, 1)}[state]
    c.set_source_rgba(*col, (0.9 if state != 'empty' else 0.25) * a); c.set_line_width(3 if state != 'win' else 5); c.stroke()
    if key:
        th = THUMB[key]
        img(c, th, 'g' if state == 'lose' else 'c', 0, -12, 1, a)
        text_c(c, SHORT[key], 0, 48, 24, (1, 1, 1, (0.45 if state == 'lose' else 1) * a), stroke=4, maxw=230)
        if state == 'lose':
            c.set_source_rgba(*RED, 0.85 * a); c.set_line_width(6)
            c.move_to(-40, -40); c.line_to(40, 30); c.move_to(40, -40); c.line_to(-40, 30); c.stroke()
    else:
        text_c(c, "?", 0, 20, 60, (1, 1, 1, 0.3 * a))
    c.restore()


def lines(c, a):
    c.set_source_rgba(1, 1, 1, 0.25 * a); c.set_line_width(3)
    for k in range(4):
        y1, y2, ym = QF_Y[2 * k], QF_Y[2 * k + 1], SF_Y[k]
        xm = (COLX[0] + COLX[1]) / 2
        c.move_to(COLX[0] + 125, y1); c.line_to(xm, y1); c.line_to(xm, y2); c.line_to(COLX[0] + 125, y2)
        c.move_to(xm, ym); c.line_to(COLX[1] - 125, ym)
    for k in range(2):
        y1, y2, ym = SF_Y[2 * k], SF_Y[2 * k + 1], F_Y[k]
        xm = (COLX[1] + COLX[2]) / 2
        c.move_to(COLX[1] + 125, y1); c.line_to(xm, y1); c.line_to(xm, y2); c.line_to(COLX[1] + 125, y2)
        c.move_to(xm, ym); c.line_to(COLX[2] - 125, ym)
    c.stroke()


def bracket_frame(c, t, s):
    lt = t - s['t0']; st = s['stage']
    background(c, t, burst=0.2)
    a = back_out(lt / 0.4)
    if st == 0:
        text_c(c, "8 AVIONS.", W / 2, 180, 84 * a, (1, 1, 1, 1), stroke=10)
        text_c(c, "1 SEUL CHAMPION.", W / 2, 275, 84 * a, (*GOLD, 1), stroke=10, maxw=1000)
    elif st == 1:
        text_c(c, "DEMI-FINALES", W / 2, 230, 96 * a, (*YEL, 1), stroke=10)
    else:
        text_c(c, "GRANDE FINALE", W / 2, 230, 96 * a, (*GOLD, 1), stroke=10, maxw=1000)
    lines(c, 1)
    for k, key in enumerate(BRACKET):
        u = back_out((lt - 0.05 * k) / 0.3) if st == 0 else 1
        state = 'lose' if (st >= 1 and key in QF_LOSERS) else ('win' if st >= 1 else 'on')
        slot(c, key, COLX[0], QF_Y[k], state, a=min(1, u), s=u)
    for k, key in enumerate(SF_ENT):
        if st >= 1:
            u = back_out((lt - 0.3 - 0.12 * k) / 0.35) if st == 1 else 1
            state = 'lose' if (st >= 2 and key in SF_LOSERS) else ('win' if st >= 2 else 'on')
            slot(c, key, COLX[1], SF_Y[k], state, s=max(0.01, u))
        else:
            slot(c, None, COLX[1], SF_Y[k], 'empty')
    for k, key in enumerate(F_ENT):
        if st >= 2:
            u = back_out((lt - 0.3 - 0.15 * k) / 0.35)
            slot(c, key, COLX[2], F_Y[k], 'on', s=max(0.01, u))
        else:
            slot(c, None, COLX[2], F_Y[k], 'empty')
    if s['end'] - t < 0.18:
        c.set_source_rgba(0.01, 0.015, 0.04, 1 - (s['end'] - t) / 0.18); c.paint()
    if lt < 0.12 and st > 0:
        c.set_source_rgba(0.01, 0.015, 0.04, 1 - lt / 0.12); c.paint()


# ---------- Champion ----------
random.seed(4)
CONF = [dict(x=random.uniform(0, W), y0=random.uniform(-900, -20), v=random.uniform(250, 520), r=random.uniform(0, 6.28),
             w=random.uniform(3, 8), col=random.choice([GOLD, YEL, CYA, RED, GRN, (1, 1, 1)]), sz=random.uniform(10, 20)) for _ in range(140)]


def champion_frame(c, t, s):
    lt = t - s['t0']
    background(c, t, burst=max(0.25, 1 - lt / 1.5), warm=True)
    a = back_out(lt / 0.5)
    text_c(c, "LE CHAMPION", W / 2, 250, 100 * a, (*GOLD, 1), stroke=10)
    img(c, CHAMP, 'glow', W / 2, 760, 1.0 + 0.02 * math.sin(t * 2), min(1, lt / 0.3))
    img(c, CHAMP, 'c', W / 2, 760 + 8 * math.sin(t * 2), 0.7 + 0.3 * back_out(lt / 0.6), min(1, lt / 0.2))
    b = back_out((lt - 0.4) / 0.4)
    text_c(c, "SR-71 BLACKBIRD", W / 2, 1150, 88 * b, (1, 1, 1, 1), stroke=10, maxw=1000)
    text_c(c, "FINALE GAGNÉE 2 – 1", W / 2, 1240, 46 * b, (*GOLD, 1), stroke=7)
    d = back_out((lt - 1.6) / 0.4)
    if d > 0:
        text_c(c, "TU AVAIS PARIÉ SUR QUI ?", W / 2, 1400, 58 * d, (*YEL, 1), stroke=8, maxw=1000)
        yy = 1450 + 12 * math.sin(t * 6)
        c.set_source_rgba(*YEL, 1); c.move_to(W / 2 - 40, yy); c.line_to(W / 2 + 40, yy); c.line_to(W / 2, yy + 50); c.close_path(); c.fill()
    for p in CONF:
        y = p['y0'] + p['v'] * lt
        if y < -30 or y > H: continue
        x = p['x'] + 40 * math.sin(lt * 2 + p['r'])
        c.save(); c.translate(x, y); c.rotate(p['r'] + lt * p['w'])
        c.rectangle(-p['sz'] / 2, -p['sz'] / 4, p['sz'], p['sz'] / 2); c.set_source_rgba(*p['col'], 0.95); c.fill(); c.restore()
    if lt < 0.2:
        c.set_source_rgba(1, 1, 1, 0.7 * (1 - lt / 0.2)); c.paint()


def render(t, surf):
    c = cairo.Context(surf)
    s = SEQ[0]
    for x in SEQ:
        if t >= x['t0']: s = x
    {'bracket': bracket_frame, 'duel': duel_frame, 'champion': champion_frame}[s['kind']](c, t, s)
    if t < 0.2:
        c.set_source_rgba(0, 0, 0, 1 - t / 0.2); c.paint()
    if t > TOTAL - 0.4:
        c.set_source_rgba(0, 0, 0, (t - (TOTAL - 0.4)) / 0.4); c.paint()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        for tt in map(float, sys.argv[2:]):
            sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); render(tt, sf); sf.write_to_png(f'tn/still_{tt:.1f}.png')
        print(round(TOTAL, 1), [(x['kind'], round(x['t0'], 1)) for x in SEQ]); sys.exit()
    nframes = int(TOTAL * FPS)
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}',
                           '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '21',
                           '-pix_fmt', 'yuv420p', 'tn/video_noaudio.mp4'], stdin=subprocess.PIPE)
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    for f in range(nframes):
        render(f / FPS, sf); sf.flush(); ff.stdin.write(bytes(sf.get_data()))
        if f % 300 == 0: print(f, '/', nframes, flush=True)
    ff.stdin.close(); ff.wait(); print('done', TOTAL)
