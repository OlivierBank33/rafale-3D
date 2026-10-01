"""Vidéo technique : comment fonctionne un réacteur (schéma animé)."""
import cairo, json, math, subprocess, sys, re, random
import numpy as np
from PIL import Image
from tech_script import SCENES

W, H, FPS = 1080, 1920, 30
TM = json.load(open('tech/timing.json'))   # starts, durs (parole), total
CYA = (0.35, 0.85, 1.0); YEL = (1.0, 0.84, 0.1); ORA = (1.0, 0.55, 0.15); RED = (1.0, 0.25, 0.2); WHITE = (1, 1, 1)
SEG = []
for i, s in enumerate(SCENES):
    t0 = TM['starts'][i] - (0.0 if i == 0 else 0.25)
    end = TM['starts'][i + 1] - 0.25 if i + 1 < len(SCENES) else TM['total']
    SEG.append(dict(k=f's{i}', step=s['step'], t0=max(0, t0), vt=TM['starts'][i], dur=TM['durs'][i], end=end))
TOTAL = TM['total']


def ease(u):
    u = min(max(u, 0), 1); return u * u * (3 - 2 * u)


def ease_out(u):
    u = min(max(u, 0), 1); return 1 - (1 - u) ** 3


def back_out(u):
    u = min(max(u, 0), 1); c = 1.70158
    return 1 + (c + 1) * (u - 1) ** 3 + c * (u - 1) ** 2


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


def rrect(c, x, y, w, h, r):
    c.new_path()
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2); c.close_path()


def pill(c, txt, cx, cy, size, bg, fg=(0.03, 0.05, 0.1), s=1.0):
    if s <= 0.02: return
    c.save(); c.translate(cx, cy); c.scale(s, s)
    font(c, size); e = c.text_extents(txt); bw = e.x_advance + size * 1.3; bh = size * 1.7
    rrect(c, -bw / 2, -bh / 2, bw, bh, bh / 2); c.set_source_rgba(*bg, 1); c.fill()
    c.set_source_rgb(*fg); c.move_to(-e.x_advance / 2, size * 0.36); c.show_text(txt); c.restore()


# ---------- Géométrie du réacteur ----------
CX, CY = W / 2, 860           # centre du schéma
X0, X1 = 70, 1010              # entrée / sortie
R_OUT = 230                    # rayon nacelle
R_CORE = 120                   # rayon carénage du cœur
SECT = dict(fan=(130, 250), comp=(290, 520), burn=(530, 650), turb=(660, 790), nozz=(800, 1010))


def background(c, t):
    g = cairo.RadialGradient(CX, CY, 50, CX, CY, 1300)
    g.add_color_stop_rgb(0, 0.06, 0.12, 0.24); g.add_color_stop_rgb(1, 0.01, 0.02, 0.05)
    c.set_source(g); c.paint()
    c.set_source_rgba(0.4, 0.7, 1, 0.05); c.set_line_width(1)
    for x in range(0, W, 40):
        c.move_to(x, 0); c.line_to(x, H)
    for y in range(0, H, 40):
        c.move_to(0, y); c.line_to(W, y)
    c.stroke()


def hl_alpha(step, sect):
    """Opacité d'une section selon l'étape (0/7 : tout visible)."""
    focus = {1: 'fan', 2: 'bypass', 3: 'comp', 4: 'burn', 5: 'turb', 6: 'nozz'}.get(step)
    if focus is None: return 1.0
    return 1.0 if focus == sect else 0.35


def engine(c, t, step, u):
    # nacelle (deux coques)
    a = hl_alpha(step, 'bypass') if step == 2 else (1.0 if step in (0, 1, 7) else 0.6)
    for sgn in (-1, 1):
        c.new_path()
        c.move_to(X0, CY + sgn * (R_OUT - 10))
        c.curve_to(X0 + 30, CY + sgn * (R_OUT + 25), 300, CY + sgn * (R_OUT + 30), 520, CY + sgn * (R_OUT + 18))
        c.line_to(870, CY + sgn * (R_OUT - 20))
        c.line_to(870, CY + sgn * (R_OUT - 50))
        c.line_to(520, CY + sgn * (R_OUT - 8))
        c.curve_to(300, CY + sgn * (R_OUT - 2), 120, CY + sgn * (R_OUT - 5), X0 + 15, CY + sgn * (R_OUT - 25))
        c.close_path()
        c.set_source_rgba(0.75, 0.82, 0.9, 0.9 * a); c.fill_preserve()
        c.set_source_rgba(1, 1, 1, a); c.set_line_width(2.5); c.stroke()
    # carénage du cœur
    ac = 1.0 if step in (0, 7) else 0.75
    for sgn in (-1, 1):
        c.new_path()
        c.move_to(270, CY + sgn * 70); c.curve_to(300, CY + sgn * (R_CORE + 10), 360, CY + sgn * (R_CORE + 15), 520, CY + sgn * (R_CORE + 15))
        c.line_to(900, CY + sgn * (R_CORE - 5)); c.line_to(900, CY + sgn * (R_CORE - 25))
        c.line_to(520, CY + sgn * (R_CORE - 5)); c.curve_to(380, CY + sgn * (R_CORE - 8), 320, CY + sgn * 80, 290, CY + sgn * 55)
        c.close_path()
        c.set_source_rgba(0.45, 0.52, 0.62, ac); c.fill_preserve(); c.set_source_rgba(1, 1, 1, 0.8 * ac); c.set_line_width(2); c.stroke()
    # arbre
    c.set_source_rgba(0.85, 0.85, 0.9, 0.9); c.rectangle(170, CY - 8, 640, 16); c.fill()
    # cône d'entrée
    c.new_path(); c.move_to(120, CY); c.curve_to(130, CY - 45, 170, CY - 55, 190, CY - 55); c.line_to(190, CY + 55); c.curve_to(170, CY + 55, 130, CY + 45, 120, CY); c.close_path()
    c.set_source_rgba(0.85, 0.88, 0.95, 1); c.fill()
    # soufflante (pales qui tournent : lignes dont la longueur apparente oscille)
    af = hl_alpha(step, 'fan')
    spin = t * (6 if step in (0, 1, 2, 7) else 3)
    for k in range(14):
        ph = spin + k * 2 * math.pi / 14
        y = CY + (R_OUT - 25) * math.sin(ph)
        if math.cos(ph) < 0: continue
        c.set_source_rgba(0.95, 0.97, 1, 0.9 * af); c.set_line_width(7)
        c.move_to(205, CY + 55 * math.sin(ph)); c.line_to(225, y); c.stroke()
    # compresseur : étages qui rétrécissent
    acp = hl_alpha(step, 'comp')
    for k in range(8):
        x = 300 + k * 28
        h = 95 - k * 6
        col = (0.6 + 0.05 * k, 0.75, 0.95)
        for sgn in (-1, 1):
            c.set_source_rgba(*col, acp); c.set_line_width(6)
            c.move_to(x, CY + sgn * 12); c.line_to(x + 8 * math.sin(t * 20 + k), CY + sgn * h); c.stroke()
    # chambre de combustion + flammes
    ab = hl_alpha(step, 'burn')
    for sgn in (-1, 1):
        rrect(c, 540, CY + (12 if sgn > 0 else -82), 100, 70, 20)
        c.set_source_rgba(0.35, 0.2, 0.15, ab); c.fill_preserve(); c.set_source_rgba(*ORA, ab); c.set_line_width(2); c.stroke()
        for j in range(6):
            fx = 560 + j * 14; fl = 30 + 18 * math.sin(t * 17 + j * 1.7)
            g = cairo.LinearGradient(fx, 0, fx + fl, 0)
            g.add_color_stop_rgba(0, 1, 0.9, 0.4, ab); g.add_color_stop_rgba(1, 1, 0.3, 0.1, 0)
            c.set_source(g); c.set_line_width(9); c.move_to(fx, CY + sgn * 47); c.line_to(fx + fl, CY + sgn * (47 + 6 * math.sin(t * 9 + j))); c.stroke()
    # turbine
    at = hl_alpha(step, 'turb')
    for k in range(4):
        x = 670 + k * 32; h = 80 + k * 6
        for sgn in (-1, 1):
            c.set_source_rgba(1, 0.65 - 0.08 * k, 0.3, at); c.set_line_width(8)
            c.move_to(x, CY + sgn * 12); c.line_to(x - 8 * math.sin(t * 22 + k), CY + sgn * h); c.stroke()
    # cône d'éjection
    an = hl_alpha(step, 'nozz')
    c.new_path(); c.move_to(800, CY - 60); c.line_to(950, CY); c.line_to(800, CY + 60); c.close_path()
    c.set_source_rgba(0.6, 0.6, 0.65, an); c.fill()


# particules d'air
random.seed(7)
PART = [dict(ph=random.random(), lane=random.choice(['by', 'by', 'by', 'core']), off=random.uniform(-1, 1)) for _ in range(150)]


def air(c, t, step):
    show_by = step in (0, 1, 2, 6, 7)
    show_core = step in (0, 1, 3, 4, 5, 6, 7)
    for p in PART:
        if p['lane'] == 'by' and not show_by: continue
        if p['lane'] == 'core' and not show_core: continue
        sp = 0.22 if p['lane'] == 'by' else 0.16
        u = (p['ph'] + t * sp) % 1.0
        x = -60 + u * (W + 260)
        if p['lane'] == 'by':
            r = R_CORE + 40 + (R_OUT - R_CORE - 70) * (0.5 + 0.5 * p['off'])
            if x < X0: r = 40 + (R_OUT - 40) * (0.5 + 0.5 * p['off'])
            y = CY + (r if p['off'] >= 0 else -r) if x >= X0 else CY + r * (1 if p['off'] >= 0 else -1) * 0.95
            col = CYA; L = 26
            if x > 870: col = (0.6, 0.85, 1.0)
        else:
            if x < 250: r = 30 + 160 * abs(p['off'])
            elif x < 520: r = 20 + (90 - 70 * (x - 250) / 270) * abs(p['off'])
            elif x < 800: r = 25 + 40 * abs(p['off'])
            else: r = 15 + 30 * abs(p['off'])
            y = CY + r * (1 if p['off'] >= 0 else -1)
            k = min(1, max(0, (x - 520) / 120))
            col = (0.35 + 0.65 * k, 0.85 - 0.45 * k, 1.0 - 0.85 * k)
            L = 16 if x < 520 else 34
            if 520 <= x < 800 and step == 4: col = (1, 0.45, 0.1)
        if step == 2 and p['lane'] == 'by':
            L *= 1.4
        c.set_source_rgba(*col, 0.85); c.set_line_width(4)
        c.move_to(x - L, y); c.line_to(x, y); c.stroke()


def callouts(c, t, s):
    st = s['step']; lt = t - s['vt']
    u = back_out(lt / 0.4)
    if st == 1:
        pill(c, "SOUFFLANTE", 190, CY - R_OUT - 70, 34, YEL, s=u)
    if st == 2:
        pill(c, "AIR QUI CONTOURNE", W / 2, CY - R_OUT - 70, 34, CYA, s=u)
        v = back_out((lt - 3.0) / 0.4)
        if v > 0:
            pill(c, "= L'ESSENTIEL DE LA POUSSÉE", W / 2, CY + R_OUT + 80, 36, YEL, s=v)
    if st == 3:
        pill(c, "COMPRESSEUR", 410, CY - R_OUT - 70, 34, YEL, s=u)
        v = ease_out((lt - 2.5) / 1.5)
        if v > 0:
            text_c(c, f"× {int(1 + 39 * v)}", W / 2, CY + R_OUT + 130, 130, (*YEL, 1), stroke=10)
            text_c(c, "PRESSION", W / 2, CY + R_OUT + 190, 40, (1, 1, 1, 0.9), stroke=6)
    if st == 4:
        pill(c, "CHAMBRE DE COMBUSTION", 590, CY - R_OUT - 70, 32, ORA, s=u)
        v = ease_out((lt - 2.5) / 1.5)
        if v > 0:
            text_c(c, f"{int(1500 * v):,} °C".replace(',', ' '), W / 2, CY + R_OUT + 130, 120, (*RED, 1), stroke=10)
            text_c(c, "PLUS CHAUD QUE LE MÉTAL NE PEUT LE SUPPORTER", W / 2, CY + R_OUT + 190, 34, (1, 1, 1, 0.9), stroke=6, maxw=980)
    if st == 5:
        pill(c, "TURBINE", 725, CY - R_OUT - 70, 34, ORA, s=u)
        # aube refroidie (zoom)
        v = back_out((lt - 1.0) / 0.4)
        if v > 0.02:
            c.save(); c.translate(W / 2, CY + R_OUT + 230); c.scale(v, v)
            c.new_path(); c.move_to(-60, 120); c.curve_to(-80, 20, -40, -100, 10, -140); c.curve_to(60, -100, 70, 20, 50, 120); c.close_path()
            g = cairo.LinearGradient(0, -140, 0, 120); g.add_color_stop_rgb(0, 1, 0.55, 0.2); g.add_color_stop_rgb(1, 0.8, 0.35, 0.15)
            c.set_source(g); c.fill_preserve(); c.set_source_rgba(1, 1, 1, 0.9); c.set_line_width(3); c.stroke()
            for j in range(7):
                hy = -100 + j * 30; hx = -20 + 8 * math.sin(j)
                c.set_source_rgb(0.1, 0.1, 0.15); c.arc(hx, hy, 6, 0, 2 * math.pi); c.fill()
                fl = (t * 80 + j * 20) % 60
                c.set_source_rgba(*CYA, 0.8 * (1 - fl / 60)); c.set_line_width(3); c.move_to(hx - 6, hy); c.line_to(hx - 6 - fl, hy - 4); c.stroke()
            c.restore()
            text_c(c, "AUBE REFROIDIE DE L'INTÉRIEUR", W / 2, CY + R_OUT + 420, 34, (1, 1, 1, v), stroke=6)
        w = ease_out((t - s['vt'] - s['dur'] * 0.62) / 0.6)
        if w > 0:
            # flèche le long de l'arbre vers la soufflante
            c.set_source_rgba(*YEL, w); c.set_line_width(6)
            c.move_to(720, CY - 24); c.line_to(720 - 500 * w, CY - 24); c.stroke()
            c.move_to(720 - 500 * w, CY - 38); c.line_to(720 - 500 * w - 24, CY - 24); c.line_to(720 - 500 * w, CY - 10); c.close_path(); c.fill()
    if st == 6:
        pill(c, "TUYÈRE", 900, CY - R_OUT - 70, 34, YEL, s=u)
        # panache + flèche de poussée
        for j in range(12):
            fl = (t * 400 + j * 70) % 500
            c.set_source_rgba(1, 0.7, 0.4, 0.5 * (1 - fl / 500)); c.set_line_width(10 - j * 0.5)
            c.move_to(950 + fl * 0.3, CY + (j - 6) * 6); c.line_to(950 + fl * 0.3 + 80, CY + (j - 6) * 8); c.stroke()
        v = back_out((lt - 2.0) / 0.4)
        if v > 0.02:
            c.save(); c.translate(W / 2, CY + R_OUT + 140); c.scale(v, v)
            c.set_source_rgba(*YEL, 1); c.set_line_width(14); c.move_to(200, 0); c.line_to(-160, 0); c.stroke()
            c.move_to(-160, -40); c.line_to(-230, 0); c.line_to(-160, 40); c.close_path(); c.fill()
            c.restore()
            text_c(c, "POUSSÉE", W / 2, CY + R_OUT + 230, 60, (*YEL, v), stroke=8)


STEP_TITLES = {0: ("UN RÉACTEUR", "EN 4 MOTS"), 1: ("1 · ASPIRER", ""), 2: ("L'AIR CONTOURNE", "LE MOTEUR"), 3: ("2 · COMPRIMER", ""),
               4: ("3 · BRÛLER", ""), 5: ("ET ÇA NE FOND PAS ?", ""), 6: ("4 · ÉJECTER", ""), 7: ("ASPIRER · COMPRIMER", "BRÛLER · ÉJECTER")}


def titles(c, t, s):
    a, b = STEP_TITLES[s['step']]
    u = back_out((t - s['t0']) / 0.4)
    text_c(c, a, W / 2, 250, 84 * (0.7 + 0.3 * u), (*(YEL if s['step'] in (1, 3, 4, 6) else WHITE), 1), stroke=10, maxw=1000)
    if b: text_c(c, b, W / 2, 345, 84 * (0.7 + 0.3 * u), (*YEL, 1), stroke=10, maxw=1000)
    # progression 4 étapes
    done = {0: 0, 1: 1, 2: 1, 3: 2, 4: 3, 5: 3, 6: 4, 7: 4}[s['step']]
    for k in range(4):
        x = W / 2 - 150 + k * 100
        rrect(c, x - 35, 120, 70, 12, 6); c.set_source_rgba(*(YEL if k < done else WHITE), 1 if k < done else 0.2); c.fill()


# ---------- Sous-titres ----------
def build_caps():
    caps = []
    for s, sc in zip(SEG, SCENES):
        words = sc['show'].replace('1 500', '1 500').replace('1 500 °C', '1 500 °C').split(' ')
        def wt(w_):
            n = len(re.sub(r'[^\w]', '', w_)) + 3 * sum(ch.isdigit() for ch in w_)
            if w_.endswith(('.', '!', '?', ':')): n += 6
            if '...' in w_: n += 8
            if w_.endswith(','): n += 3
            return max(n, 2) + 2
        ws = [wt(w_) for w_ in words]; tot = sum(ws); t0 = s['vt']; dur = s['dur']
        times = []; acc = 0
        for w_ in ws:
            times.append((t0 + dur * acc / tot, t0 + dur * (acc + w_) / tot)); acc += w_
        grp = []
        for j, w_ in enumerate(words):
            grp.append(j)
            if len(grp) == 3 or w_.endswith(('.', '!', '?', ':', ',')) or j == len(words) - 1 or (len(grp) == 2 and len(''.join(words[q] for q in grp)) > 14):
                caps.append(dict(words=[words[q] for q in grp], times=[times[q] for q in grp], t0=times[grp[0]][0], t1=times[grp[-1]][1])); grp = []
    return caps


CAPS = build_caps()


def captions(c, t):
    cap = None
    for cp in CAPS:
        if cp['t0'] - 0.02 <= t < cp['t1'] + 0.05: cap = cp
    if not cap: return
    size = 70; font(c, size)
    words = [w_.upper() for w_ in cap['words']]
    sp = c.text_extents(' ').x_advance; widths = [c.text_extents(w_).x_advance for w_ in words]
    total = sum(widths) + sp * (len(words) - 1)
    if total > 860:
        size *= 860 / total; font(c, size); widths = [c.text_extents(w_).x_advance for w_ in words]; sp = c.text_extents(' ').x_advance
        total = sum(widths) + sp * (len(words) - 1)
    pop = back_out((t - cap['t0']) / 0.15); y = 1600
    c.save(); c.translate(W / 2, y); c.scale(0.85 + 0.15 * pop, 0.85 + 0.15 * pop); c.translate(-W / 2, -y)
    x = W / 2 - total / 2
    for w_, wd, (a, b) in zip(words, widths, cap['times']):
        c.move_to(x, y); c.text_path(w_)
        c.set_source_rgba(0, 0, 0, 0.9); c.set_line_width(13); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
        c.set_source_rgb(*(YEL if a <= t < b + 0.05 else WHITE)); c.fill(); c.new_path()
        x += wd + sp
    c.restore()


def render(t, surf):
    c = cairo.Context(surf)
    s = SEG[0]
    for x in SEG:
        if t >= x['t0']: s = x
    background(c, t)
    titles(c, t, s)
    # zoom léger selon l'étape
    zoom = {0: 0.95, 7: 0.95}.get(s['step'], 1.0)
    c.save(); c.translate(CX, CY); c.scale(zoom, zoom); c.translate(-CX, -CY)
    air(c, t, s['step'])
    engine(c, t, s['step'], 1)
    c.restore()
    callouts(c, t, s)
    captions(c, t)
    lt = t - s['t0']
    if lt < 0.12 and s['t0'] > 0:
        c.set_source_rgba(1, 1, 1, 0.35 * (1 - lt / 0.12)); c.paint()
    c.set_source_rgba(*YEL, 1); c.rectangle(0, 0, W * t / TOTAL, 6); c.fill()
    if t < 0.2:
        c.set_source_rgba(0, 0, 0, 1 - t / 0.2); c.paint()
    if t > TOTAL - 0.4:
        c.set_source_rgba(0, 0, 0, (t - (TOTAL - 0.4)) / 0.4); c.paint()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        for tt in map(float, sys.argv[2:]):
            sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); render(tt, sf); sf.write_to_png(f'tech/still_{tt:.1f}.png')
        print(round(TOTAL, 1), [(x['step'], round(x['t0'], 1)) for x in SEG]); sys.exit()
    nframes = int(TOTAL * FPS)
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}',
                           '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '22',
                           '-pix_fmt', 'yuv420p', 'tech/video_noaudio.mp4'], stdin=subprocess.PIPE)
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    for f in range(nframes):
        render(f / FPS, sf); sf.flush(); ff.stdin.write(bytes(sf.get_data()))
        if f % 300 == 0: print(f, '/', nframes, flush=True)
    ff.stdin.close(); ff.wait(); print('done', TOTAL)
