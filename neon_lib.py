"""Bibliothèque commune du style néon @minuteaero (palette turquoise/orange, polices Bebas Neue + Montserrat, fond étoilé, glow, jauges, karaoké)."""
import cairo, math, os, re, random
W, H, FPS = 1080, 1920, 30

# Palette @minuteaero (style néon, couleurs propres) : turquoise néon + orange néon
BG = (0.012, 0.035, 0.042)                 # #03090B
BLU = (0.0, 0.88, 0.78)                    # turquoise néon #00E0C7 (traits)
CYA = (0.45, 1.0, 0.92)                    # turquoise clair #73FFEB (légendes)
YLW = (1.0, 0.55, 0.0)                     # orange néon #FF8C00 (mots clés, chiffres)
RED = (1.0, 0.18, 0.33)                    # rouge-rose #FF2E55 (alertes)
ORG = (1.0, 0.82, 0.25)                    # ambre (2e couleur d'accent)
WHT = (0.96, 1.0, 0.99)
DIM = (0.40, 0.62, 0.60)
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
        c.set_source_rgba(0.8, 1, 0.96, a * (0.5 + r / 5)); c.arc(x, yy, r, 0, 6.283); c.fill()


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



# ---------- sous-titres karaoké (mot actif en orange) ----------
def chunks(show, n=3):
    show = re.sub(r' ([?!:;»])', '\u00a0\\1', show)
    show = re.sub(r'(\d) (\d{3})', '\\1\u00a0\\2', show)
    w = [x for x in show.split(' ') if x]; out = []; cur = []
    for x in w:
        cur.append(x)
        if len(cur) >= n or x.endswith(('.', '?', '!', ',', ':')): out.append(cur); cur = []
    if cur: out.append(cur)
    return out


def build_chunks(items):
    """items : liste (début_voix, durée, texte_affiché) -> blocs de mots minutés."""
    CHK = []
    for vt, dur, show in items:
        cs = chunks(show); allw = [w for ch in cs for w in ch]
        if not allw: continue
        wt = [len(w) + 2 + (6 if w.endswith(('.', '?', '!')) else 3 if w.endswith((',', ':')) else 0) for w in allw]
        tot = sum(wt); acc = 0; k = 0
        for ch in cs:
            ws = []
            for w in ch:
                a = vt + dur * acc / tot; acc += wt[k]; k += 1
                ws.append((a, vt + dur * acc / tot, w))
            CHK.append(ws)
    return CHK


def subtitles(c, t, CHK, y0=1500, size=86):
    cur = [ch for ch in CHK if ch[0][0] <= t < ch[-1][1] + 0.08]
    if not cur: return
    ch = cur[-1]
    F(c, size); words = [w.upper() for _, _, w in ch]
    sp = size * 0.5
    ws = [c.text_extents(w).x_advance for w in words]
    lines = [[]]; lw = 0
    for i, w in enumerate(ws):
        if lines[-1] and lw + sp + w > 980: lines.append([]); lw = 0
        lines[-1].append(i); lw += (sp if len(lines[-1]) > 1 else 0) + w
    y = y0 - (len(lines) - 1) * 50
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


# ---------- avions 3D -> contours néon ----------
def neon_image(path, col=None, rot=0.0, flip=False, maxdim=900):
    """Transforme un rendu 3D (PNG RGBA) en dessin filaire néon : contours (silhouette + arêtes internes) + halo. Renvoie (surface, w, h)."""
    import numpy as np
    from PIL import Image, ImageFilter, ImageOps
    col = col or BLU
    im = Image.open(path).convert('RGBA')
    if flip: im = ImageOps.mirror(im)
    if rot: im = im.rotate(-math.degrees(rot), expand=True, resample=Image.BICUBIC)
    bb = im.getbbox()
    if bb: im = im.crop(bb)
    k = maxdim / max(im.size)
    if k < 1: im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    pad = 40; big = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad)); big.paste(im, (pad, pad)); im = big
    a = np.asarray(im.split()[3]).astype(np.float32) / 255
    g = np.asarray(im.convert('L').filter(ImageFilter.GaussianBlur(1.0))).astype(np.float32) / 255
    def sob(x):
        gx = np.zeros_like(x); gy = np.zeros_like(x)
        gx[:, 1:-1] = x[:, 2:] - x[:, :-2]; gy[1:-1, :] = x[2:, :] - x[:-2, :]
        return np.hypot(gx, gy)
    e_out = np.clip(sob(a) * 2.2, 0, 1)
    e_in = np.clip((sob(g) - 0.06) * 4.0, 0, 1) * (a > 0.5) * 0.75
    e = np.maximum(e_out, e_in)
    fill = a * 0.07
    E = Image.fromarray((e * 255).astype(np.uint8))
    halo = np.asarray(E.filter(ImageFilter.GaussianBlur(7))).astype(np.float32) / 255 * 1.6
    lum = np.clip(e + halo * 0.6 + fill, 0, 1)
    core = np.clip(e * 1.2, 0, 1)
    r = np.clip(col[0] * lum + core * 0.35, 0, 1); gg = np.clip(col[1] * lum + core * 0.35, 0, 1); b = np.clip(col[2] * lum + core * 0.35, 0, 1)
    alpha = np.clip(np.maximum(lum, e), 0, 1)
    arr = np.zeros((im.height, im.width, 4), np.uint8)   # cairo ARGB32 little-endian = BGRA prémultiplié
    arr[..., 0] = (b * alpha * 255).astype(np.uint8); arr[..., 1] = (gg * alpha * 255).astype(np.uint8)
    arr[..., 2] = (r * alpha * 255).astype(np.uint8); arr[..., 3] = (alpha * 255).astype(np.uint8)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, im.width, im.height)
    stride = surf.get_stride(); buf = surf.get_data()
    np.frombuffer(buf, np.uint8).reshape(im.height, stride)[:, :im.width * 4] = arr.reshape(im.height, -1)
    surf.mark_dirty()
    return surf, im.width, im.height


def draw_surf(c, img, cx, cy, size, a=1.0, rot=0.0):
    surf, w, h = img; k = size / max(w, h)
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(k, k)
    c.set_source_surface(surf, -w / 2, -h / 2); c.paint_with_alpha(max(0, min(1, a))); c.restore()


def sub_button(c, x, y, lt, a=1.0, label="ABONNE-TOI"):
    s = (1 + 0.06 * math.sin(lt * 6)) * a
    if s <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.new_path(); r = 50; w, h = 560, 110
    c.arc(-w / 2 + r, -h / 2 + r, r, math.pi, 1.5 * math.pi); c.arc(w / 2 - r, -h / 2 + r, r, 1.5 * math.pi, 0); c.arc(w / 2 - r, h / 2 - r, r, 0, 0.5 * math.pi); c.arc(-w / 2 + r, h / 2 - r, r, 0.5 * math.pi, math.pi); c.close_path()
    c.set_source_rgba(*YLW, 1); c.fill()
    txt(c, label, 0, 30, 84, (0.02, 0.03, 0.04, 1), BIG, 'c')
    c.restore()


def ffmpeg_out(path):
    import subprocess
    return subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                             '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', path], stdin=subprocess.PIPE)
