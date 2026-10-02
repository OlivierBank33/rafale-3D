"""Les avions les plus chers du monde : alignement gauche -> droite, piles de billets (volume ∝ prix), dézoom progressif."""
import cairo, json, math, subprocess, sys
from px_script import PLANES, INTRO, OUTRO

W, H, FPS = 1080, 1920, 30
D = json.load(open('px/durs.json'))
GY = 1440                      # sol à l'écran
GOLD = (1.0, 0.82, 0.25); GREEN = (0.30, 0.95, 0.55); WHITE = (1, 1, 1)
N = len(PLANES)

# ---------- Timeline ----------
SEG = []; t = 0.0
order = ['intro'] + [f'p{i}' for i in range(N)] + ['outro']
for k in order:
    pre = 0.4 if k == 'intro' else (1.3 if k.startswith('p') else 0.6)
    post = 0.5 if k != 'outro' else 2.4
    SEG.append(dict(k=k, t0=t, vt=t + pre, end=t + pre + D[k] + post)); t = SEG[-1]['end']
TOTAL = t
json.dump(dict(seg=SEG, total=TOTAL), open('px/timeline.json', 'w'))
SEGK = {s['k']: s for s in SEG}

# ---------- Monde (mètres) ----------
IMG = {}
for p in PLANES:
    sf = cairo.ImageSurface.create_from_png(f"px/img_{p['k']}.png"); IMG[p['k']] = sf
    p['h'] = p['L'] * sf.get_height() / sf.get_width()
    p['s'] = 3.6 * p['eur'] ** (1 / 3)          # arête de la pile (m) : volume ∝ prix
x = 0.0
for i, p in enumerate(PLANES):
    p['x'] = x; p['sx'] = x + max(0.15 * p['L'], p['L'] - 0.95 * p['s'])
    x = max(x + p['L'], p['sx'] + p['s'] * 1.3) + 0.08 * max(p['L'], PLANES[i + 1]['L'] if i + 1 < N else 0) + 1.5


def view(i):
    """Vue qui montre tous les avions 0..i (bord gauche fixe)."""
    right = max(PLANES[i]['x'] + PLANES[i]['L'], PLANES[i]['sx'] + PLANES[i]['s'] * 1.3)
    left = -0.04 * right - 0.5; right += 0.04 * (right - left)
    sc = W / (right - left)
    top = max(max(p['h'], p['s'] * 1.25) for p in PLANES[:i + 1])
    sc = min(sc, 760 / top)
    return left, sc


VIEWS = [view(i) for i in range(N)]


def ease(u):
    u = min(max(u, 0), 1); return u * u * (3 - 2 * u)


def ease_out(u):
    u = min(max(u, 0), 1); return 1 - (1 - u) ** 3


def back_out(u):
    u = min(max(u, 0), 1); k = 1.70158; return 1 + (k + 1) * (u - 1) ** 3 + k * (u - 1) ** 2


def lerp(a, b, u): return a + (b - a) * u


def camera(t):
    def mix(v0, v1, u):
        return lerp(v0[0], v1[0], u), math.exp(lerp(math.log(v0[1]), math.log(v1[1]), u))
    intro_v = VIEWS[-1]
    if t < SEGK['p0']['t0']: return intro_v
    cur = intro_v
    for i in range(N):
        s = SEGK[f'p{i}']
        if t < s['t0']: break
        dur = 1.6 if i == 0 else 1.1
        cur = mix(cur, VIEWS[i], ease((t - s['t0']) / dur))
    o = SEGK['outro']
    if t > o['t0']: cur = (cur[0], cur[1] * (1 - 0.04 * ease((t - o['t0']) / 4)))
    return cur


# ---------- Dessin ----------
def font(c, size, bold=True):
    c.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL); c.set_font_size(size)


def text_c(c, txt, x, y, size, rgba=(1, 1, 1, 1), stroke=0, maxw=None, bold=True):
    font(c, size, bold); e = c.text_extents(txt)
    if maxw and e.x_advance > maxw:
        size *= maxw / e.x_advance; font(c, size, bold); e = c.text_extents(txt)
    c.move_to(x - e.x_advance / 2, y); c.text_path(txt)
    if stroke:
        c.set_source_rgba(0, 0, 0, 0.8 * rgba[3]); c.set_line_width(stroke); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
    c.set_source_rgba(*rgba); c.fill(); c.new_path()


def rrect(c, x, y, w, h, r):
    c.new_path(); r = min(r, h / 2, w / 2)
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2); c.close_path()


def pill(c, txt, cx, cy, size, bg, fg=(0, 0, 0), alpha=1.0):
    if alpha <= 0.01: return
    font(c, size); e = c.text_extents(txt); bw = e.x_advance + size * 1.1; bh = size * 1.6
    rrect(c, cx - bw / 2, cy - bh / 2, bw, bh, bh / 2); c.set_source_rgba(*bg, 0.95 * alpha); c.fill()
    c.set_source_rgba(*fg, alpha); c.move_to(cx - e.x_advance / 2, cy + size * 0.36); c.show_text(txt)


def background(c, cam):
    g = cairo.LinearGradient(0, 0, 0, GY)
    g.add_color_stop_rgb(0, 0.02, 0.03, 0.07); g.add_color_stop_rgb(0.7, 0.06, 0.09, 0.17); g.add_color_stop_rgb(1, 0.13, 0.15, 0.24)
    c.set_source(g); c.rectangle(0, 0, W, GY); c.fill()
    hg = cairo.RadialGradient(W / 2, GY, 0, W / 2, GY, 700)
    hg.add_color_stop_rgba(0, 1.0, 0.75, 0.35, 0.16); hg.add_color_stop_rgba(1, 1.0, 0.75, 0.35, 0)
    c.set_source(hg); c.rectangle(0, 0, W, GY); c.fill()
    g2 = cairo.LinearGradient(0, GY, 0, H)
    g2.add_color_stop_rgb(0, 0.10, 0.11, 0.13); g2.add_color_stop_rgb(1, 0.03, 0.03, 0.04)
    c.set_source(g2); c.rectangle(0, GY, W, H - GY); c.fill()
    c.set_source_rgba(1, 0.85, 0.45, 0.55); c.set_line_width(3); c.move_to(0, GY); c.line_to(W, GY); c.stroke()
    # axe de piste (pointillés monde) : pas adapté au zoom
    left, sc = cam
    step = 10 ** math.ceil(math.log10(70 / sc)); dash = step * 0.5
    x0 = math.floor(left / step) * step
    c.set_source_rgba(1, 1, 1, 0.22)
    while (x0 - left) * sc < W:
        c.rectangle((x0 - left) * sc, GY + 70, dash * sc, 8); x0 += step
    c.fill()


def draw_plane(c, p, cam, alpha=1.0, dx=0.0, sil=False, hero=0.0):
    left, sc = cam
    sf = IMG[p['k']]; w = p['L'] * sc
    x = (p['x'] - left) * sc + dx; y = GY - p['h'] * sc
    if hero > 0:   # grande vue au centre -> se pose dans l'alignement
        hw = 780; hx = W / 2 - hw / 2 + dx; hy = 1290 - hw * p['h'] / p['L']
        w = math.exp(lerp(math.log(max(w, 1)), math.log(hw), hero)); x = lerp(x, hx, hero); y = lerp(y, hy, hero)
    s = w / sf.get_width()
    if x > W or x + w < 0 or alpha <= 0.01: return
    # ombre au sol
    c.save(); c.translate(x + w / 2, lerp(GY + 4, 1300, hero)); c.scale(w * 0.45, max(2, w * 0.035))
    rg = cairo.RadialGradient(0, 0, 0, 0, 0, 1); rg.add_color_stop_rgba(0, 0, 0, 0, 0.5 * alpha * (1 - hero)); rg.add_color_stop_rgba(1, 0, 0, 0, 0)
    c.set_source(rg); c.arc(0, 0, 1, 0, 2 * math.pi); c.fill(); c.restore()
    c.save(); c.translate(x, y); c.scale(s, s)
    if sil:
        c.set_source_rgba(0.55, 0.62, 0.8, 0.30 * alpha); c.mask_surface(sf, 0, 0)
    else:
        c.set_source_surface(sf, 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint_with_alpha(alpha)
    c.restore()


def draw_stack(c, p, cam, grow, alpha=1.0):
    """Pile de liasses de billets (isométrique). grow 0..1 = hauteur."""
    if grow <= 0.001 or alpha <= 0.01: return
    left, sc = cam
    w = p['s'] * sc; h = w * grow; x = (p['sx'] - left) * sc; y = GY - h
    if x > W or x + w * 1.3 < 0: return
    dx, dy = 0.30 * w, -0.20 * w
    base = (0.33, 0.62, 0.40)
    c.save()
    # face de dessus
    c.move_to(x, y); c.line_to(x + dx, y + dy); c.line_to(x + w + dx, y + dy); c.line_to(x + w, y); c.close_path()
    c.set_source_rgba(0.55, 0.80, 0.58, alpha); c.fill()
    # côté droit
    c.move_to(x + w, y); c.line_to(x + w + dx, y + dy); c.line_to(x + w + dx, GY + dy); c.line_to(x + w, GY); c.close_path()
    c.set_source_rgba(0.18, 0.40, 0.25, alpha); c.fill()
    # face avant
    c.rectangle(x, y, w, h); c.set_source_rgba(*base, alpha); c.fill()
    if w > 14:
        cols = 3; bundle_h = w / 7.0; rows = max(1, int(round(h / bundle_h)))
        # tranches de papier
        c.set_line_width(max(0.6, w / 260))
        c.set_source_rgba(0.85, 0.95, 0.85, 0.35 * alpha)
        nl = min(int(h / max(2.5, w / 60)), 400)
        for j in range(1, nl):
            yy = GY - j * h / nl; c.move_to(x, yy); c.line_to(x + w, yy)
        c.stroke()
        # séparations de liasses
        c.set_line_width(max(1, w / 120)); c.set_source_rgba(0.08, 0.22, 0.12, 0.9 * alpha)
        for j in range(1, rows):
            yy = GY - j * h / rows; c.move_to(x, yy); c.line_to(x + w, yy)
        for j in range(1, cols):
            xx = x + j * w / cols; c.move_to(xx, y); c.line_to(xx, GY)
        c.stroke()
        # bandes de papier
        c.set_source_rgba(0.96, 0.90, 0.70, 0.95 * alpha)
        for j in range(cols):
            c.rectangle(x + (j + 0.42) * w / cols, y, 0.16 * w / cols, h)
        c.fill()
        # bandes sur le dessus
        for j in range(cols):
            u0 = (j + 0.42) / cols; u1 = (j + 0.58) / cols
            c.move_to(x + u0 * w, y); c.line_to(x + u0 * w + dx, y + dy); c.line_to(x + u1 * w + dx, y + dy); c.line_to(x + u1 * w, y); c.close_path()
        c.fill()
        if w > 60 and grow > 0.6:
            font(c, w * 0.16); e = c.text_extents("€")
            c.set_source_rgba(1, 1, 1, 0.22 * alpha); c.move_to(x + w / 2 - e.x_advance / 2, y + h / 2 + e.height / 2); c.show_text("€")
    c.set_source_rgba(0, 0, 0, 0.35 * alpha); c.set_line_width(1.2)
    c.rectangle(x, y, w, h); c.stroke()
    c.restore()


def fmt_eur(m):
    """m en millions d'euros -> '120 000 000 €' (3 chiffres significatifs)."""
    v = m * 1e6
    if v <= 0: return "0 €"
    e = 10 ** max(0, int(math.floor(math.log10(v))) - 2)
    v = int(round(v / e) * e)
    return f"{v:,}".replace(',', ' ') + " €"


FINAL = {i: "≈ " + fmt_eur(p['eur']) for i, p in enumerate(PLANES)}


def price_now(t, i):
    s = SEGK[f'p{i}']; u = ease_out((t - (s['t0'] + 0.9)) / 2.2)
    prev = PLANES[i - 1]['eur'] if i else 0.01
    return math.exp(lerp(math.log(prev), math.log(PLANES[i]['eur']), u)), u


def hud(c, t, i):
    p = PLANES[i]; s = SEGK[f'p{i}']; a = ease((t - s['t0'] - 0.3) / 0.4)
    if a <= 0: return
    rank = N - i
    pill(c, f"N°{rank}", W / 2, 250, 40, GOLD, (0.05, 0.05, 0.08), a)
    text_c(c, p['name'], W / 2, 375, 92, (1, 1, 1, a), stroke=8, maxw=W - 120)
    v, u = price_now(t, i)
    txt = FINAL[i] if u >= 0.999 else fmt_eur(v)
    pop = 1 + 0.08 * math.sin(math.pi * min(1, max(0, (t - s['t0'] - 3.6) / 0.35)))
    c.save(); c.translate(W / 2, 505); c.scale(pop, pop)
    text_c(c, txt, 0, 0, 84, (*GREEN, a), stroke=8, maxw=W - 90); c.restore()
    text_c(c, p['note'], W / 2, 572, 34, (0.85, 0.88, 0.95, 0.85 * a), bold=False, maxw=W - 120)
    if i >= 2:
        n = p['eur'] / PLANES[0]['eur']; b = ease((t - s['t0'] - 3.7) / 0.4)
        ntxt = f"= {int(round(n, -1 if n > 100 else 0)):,} Cessna 172".replace(',', ' ')
        pill(c, ntxt, W / 2, 655, 38, (0.12, 0.14, 0.22), (1, 0.9, 0.6), b * a)


def labels(c, cam, t, upto, cur):
    left, sc = cam
    for i in range(upto + 1):
        p = PLANES[i]; w = p['L'] * sc
        x = (p['x'] - left) * sc; sx = (p['sx'] - left) * sc; sw = p['s'] * sc
        a = 1.0 if i < cur else ease((t - SEGK[f'p{i}']['t0'] - 3.2) / 0.4)
        if w > 70:
            text_c(c, p['name'], x + w / 2, GY + 52, min(34, max(18, w * 0.09)), (1, 1, 1, 0.75 * a), maxw=max(60, w))
        if sw * 1.3 > 34:
            size = min(34, max(15, sw * 0.22))
            short = p['price'].replace('≈ ', '')
            pill(c, short, sx + sw * 0.65, GY - sw * (1 if i < cur else stack_grow(t, i)) - sw * 0.2 - size * 1.1, size, GOLD, (0.05, 0.05, 0.08), a)


def stack_grow(t, i):
    s = SEGK[f'p{i}']; return back_out((t - s['t0'] - 2.3) / 1.1) if t > s['t0'] + 2.3 else 0.0


def render(t, surf):
    c = cairo.Context(surf)
    cam = camera(t)
    background(c, cam)
    cur = -1
    for i in range(N):
        if t >= SEGK[f'p{i}']['t0']: cur = i
    # intro : silhouettes de tout l'alignement
    if t < SEGK['p0']['t0'] + 1.2:
        fa = 1 - ease((t - SEGK['p0']['t0']) / 1.2)
        for p in PLANES: draw_stack(c, p, cam, 1.0, 0.25 * fa)
        for p in PLANES: draw_plane(c, p, cam, fa, sil=True)
    for i in range(cur + 1):
        draw_stack(c, PLANES[i], cam, stack_grow(t, i))
    for i in range(cur + 1):
        s = SEGK[f'p{i}']
        u = ease_out((t - s['t0'] - 0.25) / 0.9)
        hero = 1 - ease((t - s['t0'] - 1.6) / 0.8)
        if hero > 0.001 and i > 0:   # halo derrière la grande vue
            hx, hy = W / 2, 1120; rg = cairo.RadialGradient(hx, hy, 0, hx, hy, 520)
            rg.add_color_stop_rgba(0, 1, 0.8, 0.4, 0.18 * hero * u); rg.add_color_stop_rgba(1, 1, 0.8, 0.4, 0)
            c.set_source(rg); c.paint()
        draw_plane(c, PLANES[i], cam, alpha=min(1, u * 1.4), dx=(1 - u) * 320, hero=hero if i > 0 else 0)
    if cur >= 0: labels(c, cam, t, cur, cur)
    # HUD
    if t < SEGK['p0']['t0'] + 0.3:
        a = ease(t / 0.5) * (1 - ease((t - SEGK['p0']['t0']) / 0.3))
        text_c(c, "LES AVIONS", W / 2, 330, 104, (1, 1, 1, a), stroke=8)
        text_c(c, "LES PLUS CHERS", W / 2, 445, 104, (*GOLD, a), stroke=8)
        text_c(c, "DU MONDE", W / 2, 560, 104, (1, 1, 1, a), stroke=8)
        b = ease((t - 2.5) / 0.5) * a
        pill(c, "du moins cher au plus cher", W / 2, 670, 40, (0.12, 0.14, 0.22), (1, 0.9, 0.6), b)
    elif t < SEGK['outro']['t0'] + 0.3:
        hud(c, t, cur)
    if t >= SEGK['outro']['t0']:
        a = ease((t - SEGK['outro']['t0'] - 0.2) / 0.5)
        text_c(c, "TU PRENDS", W / 2, 360, 100, (1, 1, 1, a), stroke=8)
        text_c(c, "LEQUEL ?", W / 2, 475, 110, (*GOLD, a), stroke=8)
        pill(c, "Dis-le en commentaire", W / 2, 590, 40, (0.12, 0.14, 0.22), (1, 0.9, 0.6), a)
    # mention
    text_c(c, "Volume des piles proportionnel au prix · ordres de grandeur", W / 2, H - 70, 24, (1, 1, 1, 0.38), bold=False)
    return surf


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        for tt in map(float, sys.argv[2:]):
            sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); render(tt, sf); sf.write_to_png(f'px/still_{tt}.png')
        sys.exit()
    nf = int(TOTAL * FPS)
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', 'px/video_noaudio.mp4'], stdin=subprocess.PIPE)
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    for f in range(nf):
        render(f / FPS, sf); sf.flush(); ff.stdin.write(bytes(sf.get_data()))
        if f % 300 == 0: print(f, '/', nf, flush=True)
    ff.stdin.close(); ff.wait(); print('done', TOTAL)
