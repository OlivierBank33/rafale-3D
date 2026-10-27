"""Plaques de décor photoréalistes (numpy/PIL) pour le film Concorde premium. python3 pr/plates.py -> pr/p_*.png"""
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
import math, os
OUT = '/home/claude/pr'
rng = np.random.default_rng(7)


def vnoise(h, w, cell, seed=0):
    r = np.random.default_rng(seed)
    gh, gw = h // cell + 3, w // cell + 3
    g = r.random((gh, gw)).astype(np.float32)
    ys = np.arange(h) / cell; xs = np.arange(w) / cell
    y0 = ys.astype(int); x0 = xs.astype(int); fy = ys - y0; fx = xs - x0
    fy = fy * fy * (3 - 2 * fy); fx = fx * fx * (3 - 2 * fx)
    a = g[y0][:, x0]; b = g[y0][:, x0 + 1]; c = g[y0 + 1][:, x0]; d = g[y0 + 1][:, x0 + 1]
    top = a + (b - a) * fx[None, :]; bot = c + (d - c) * fx[None, :]
    return top + (bot - top) * fy[:, None]


def fbm(h, w, cell, oct=5, seed=0, gain=0.5):
    s = np.zeros((h, w), np.float32); amp = 1.0; tot = 0
    for o in range(oct):
        s += amp * vnoise(h, w, max(2, int(cell / 2 ** o)), seed + o * 17); tot += amp; amp *= gain
    return s / tot


def lerp(a, b, t): return a + (b - a) * t


def save(arr, name):
    Image.fromarray(np.clip(arr * 255, 0, 255).astype(np.uint8)).save(f'{OUT}/{name}')


def sky_day(W=1080, H=2400, seed=3, warm=0.35, horizon=0.9, cloud_amt=0.5):
    """Ciel d'été en fin d'après-midi : dégradé + soleil + cumulus doux."""
    y = np.linspace(0, 1, H)[:, None]
    top = np.array([0.14, 0.34, 0.70]); mid = np.array([0.40, 0.60, 0.88]); hor = np.array([0.84, 0.85, 0.86])
    t = np.clip(y / horizon, 0, 1)
    base = lerp(top, mid, np.clip(t * 1.4, 0, 1)[..., None])
    base = lerp(base, hor, (np.clip((t - 0.72) / 0.28, 0, 1) ** 1.4)[..., None])
    base = np.broadcast_to(base, (H, W, 3)).copy()
    # soleil haut à droite + voile chaud
    yy, xx = np.mgrid[0:H, 0:W]
    sx, sy = W * 0.82, H * 0.12
    d = np.sqrt((xx - sx) ** 2 + (yy - sy) ** 2) / W
    glow = np.exp(-d * 5.0)[..., None] * np.array([1.0, 0.92, 0.75]) * 0.55 + np.exp(-d * 28)[..., None] * 0.9
    base = 1 - (1 - base) * (1 - np.clip(glow, 0, 1))
    # cumulus
    n = fbm(H, W, 360, 6, seed)
    n2 = fbm(H, W, 90, 4, seed + 5)
    band = np.exp(-((y - 0.55) / 0.22) ** 2) * 0.9 + 0.25
    c = np.clip((n * 0.75 + n2 * 0.25 - (1 - cloud_amt)) * 3.2, 0, 1) * band
    shade = np.clip(1.0 - (fbm(H, W, 200, 4, seed + 9) - 0.45) * 0.9, 0.78, 1.0)
    ccol = np.stack([shade * 0.98 + 0.02, shade * 0.95 + 0.03, shade * 0.92 + 0.05], -1)
    ccol = lerp(ccol, np.array([1.0, 0.88, 0.7]), warm * 0.4)
    out = lerp(base, ccol, c[..., None] * 0.92)
    # brume au ras de l'horizon
    haze = np.clip((y - horizon + 0.12) / 0.12, 0, 1)[..., None]
    out = lerp(out, np.array([0.88, 0.87, 0.84]), haze * 0.4)
    return out


def strip_far(W=4320, H=520, seed=11):
    """Lisière lointaine : arbres, hangars, tour de contrôle dans la brume (transparent en haut)."""
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    r = np.random.default_rng(seed)
    hz = H - 60
    x = 0
    while x < W:  # bâtiments / hangars
        w = int(r.integers(80, 340)); h = int(r.integers(30, 120))
        if r.random() < 0.35:
            col = tuple(int(v) for v in (r.integers(150, 175), r.integers(158, 182), r.integers(170, 190)))
            d.rectangle((x, hz - h, x + w, hz + 10), fill=col + (255,))
            if r.random() < 0.4:
                d.polygon([(x, hz - h), (x + w // 2, hz - h - 25), (x + w, hz - h)], fill=col + (255,))
        x += w + int(r.integers(10, 120))
    # arbres (couronnes rondes)
    for i in range(900):
        cx = r.random() * W; s = r.integers(14, 40); cy = hz - r.random() * 30 + 8
        g = int(r.integers(95, 125)); col = (g - 20, g + 12, g - 10, 255)
        d.ellipse((cx - s, cy - s, cx + s, cy + s * 0.8), fill=col)
    # tour de contrôle (une fois)
    tx = int(W * 0.62)
    d.rectangle((tx - 14, hz - 300, tx + 14, hz + 5), fill=(150, 156, 168, 255))
    d.polygon([(tx - 46, hz - 300), (tx + 46, hz - 300), (tx + 36, hz - 345), (tx - 36, hz - 345)], fill=(120, 140, 160, 255))
    d.rectangle((tx - 40, hz - 300, tx + 40, hz - 290), fill=(170, 175, 185, 255))
    d.rectangle((0, hz + 5, W, H), fill=(118, 132, 96, 255))
    img = img.filter(ImageFilter.GaussianBlur(2.2))
    a = np.asarray(img).astype(np.float32) / 255
    # brume atmosphérique (vers la couleur d'horizon)
    hazec = np.array([0.88, 0.85, 0.79])
    a[..., :3] = lerp(a[..., :3], hazec, 0.55)
    return a


def runway_strip(W=4320, H=900, seed=21):
    """Bande latérale : herbe lointaine / piste avec marquages / herbe proche (vue de côté rasante). Tuile horizontalement."""
    r = np.random.default_rng(seed)
    y = np.arange(H)[:, None] / H
    out = np.zeros((H, W, 3), np.float32)
    grass = np.array([0.42, 0.52, 0.28]); grass2 = np.array([0.55, 0.6, 0.33])
    n = fbm(H, W, 120, 5, seed)
    gcol = lerp(grass, grass2, n[..., None])
    out[:] = gcol
    # piste entre y0 et y1 (perspective : bande compressée en haut)
    y0, y1 = int(H * 0.30), int(H * 0.56)
    asph = 0.33 + 0.07 * fbm(y1 - y0, W, 40, 5, seed + 3) + 0.03 * vnoise(y1 - y0, W, 3, seed + 4)
    out[y0:y1] = np.stack([asph, asph * 1.0, asph * 1.04], -1)
    # traces de gomme
    tr = np.clip(fbm(y1 - y0, W, 300, 3, seed + 7) - 0.45, 0, 1) * 0.5
    out[y0:y1] *= (1 - tr[..., None] * 0.6)
    img = Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)); d = ImageDraw.Draw(img)
    # bords de piste + axe pointillé (vus de côté : lignes horizontales)
    d.rectangle((0, y0 + 4, W, y0 + 8), fill=(225, 225, 220))
    d.rectangle((0, y1 - 12, W, y1 - 4), fill=(235, 235, 230))
    cy = int((y0 + y1) * 0.5) - 6
    for x in range(0, W, 240):
        d.rectangle((x, cy, x + 130, cy + 6), fill=(230, 230, 222))
    # feux de bord de piste
    for x in range(0, W, 120):
        d.rectangle((x, y1 - 26, x + 8, y1 - 12), fill=(60, 60, 60)); d.ellipse((x - 2, y1 - 34, x + 10, y1 - 24), fill=(250, 240, 200))
    img = img.filter(ImageFilter.GaussianBlur(0.6))
    a = np.asarray(img).astype(np.float32) / 255
    # brume en haut (lointain)
    hz = np.clip(1 - y / 0.35, 0, 1)[..., None] * 0.45
    a = lerp(a, np.array([0.86, 0.84, 0.78]), hz)
    return a


def runway_persp(W=1080, H=1920, seed=31, cam_h=60.0, hy=None, f=900.0, threshold=True):
    """Vue dans l'axe de la piste (point de fuite), herbe, horizon brumeux. Ciel transparent (alpha).
    cam_h : hauteur caméra (m), f : focale (px). Projection : y - hy = f*cam_h/Z ; x - vx = f*X/Z."""
    hy = int(H * 0.43) if hy is None else hy; vx = W / 2
    out = np.zeros((H, W, 4), np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    below = yy > hy
    Z = np.where(below, f * cam_h / np.maximum(yy - hy, 0.5), 1e6)
    X = (xx - vx) * Z / f
    halfw = 30.0
    on_rw = (np.abs(X) < halfw) & below
    g = fbm(H, W, 60, 4, seed)
    grass = np.stack([0.38 + 0.12 * g, 0.48 + 0.1 * g, 0.26 + 0.06 * g], -1)
    asph = 0.32 + 0.06 * fbm(H, W, 20, 3, seed + 2)
    col = np.where(on_rw[..., None], np.stack([asph, asph, asph * 1.03], -1), grass)
    # marquages : bords, axe pointillé, seuil (zébras)
    edge = on_rw & (np.abs(np.abs(X) - halfw + 1.0) < 0.6)
    cl = on_rw & (np.abs(X) < 0.5) & ((Z % 50) < 30)
    thr = on_rw & (Z < 70) & (Z > 10) & ((np.abs(X) % 5) < 2.2) & (np.abs(X) > 2) & threshold
    tdz = on_rw & ((Z % 150) > 135) & (np.abs(np.abs(X) - 11) < 4) & threshold
    mk = edge | cl | thr | tdz
    col = np.where(mk[..., None], np.array([0.9, 0.9, 0.87]), col)
    fog = np.clip(1 - np.exp(-Z / 2600.0), 0, 1)[..., None]
    col = lerp(col, np.array([0.86, 0.83, 0.76]), np.where(below[..., None], fog * 0.9, 0))
    out[..., :3] = col; out[..., 3] = below.astype(np.float32)
    # lisière d'arbres sur l'horizon
    img = Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8), 'RGBA'); d = ImageDraw.Draw(img)
    r = np.random.default_rng(seed)
    for i in range(500):
        cx = r.random() * W; s = r.integers(6, 18)
        d.ellipse((cx - s, hy - s * 1.6, cx + s, hy + 4), fill=(126, 136, 112, 255))
    img = img.filter(ImageFilter.GaussianBlur(1.0))
    return np.asarray(img).astype(np.float32) / 255


def asphalt_macro(W=1400, H=1400, seed=41):
    n = fbm(H, W, 30, 6, seed); n2 = vnoise(H, W, 2, seed + 1)
    v = 0.26 + 0.12 * n + 0.08 * (n2 - 0.5)
    pebbles = (vnoise(H, W, 5, seed + 3) > 0.82).astype(np.float32) * 0.1
    v = v + pebbles
    col = np.stack([v, v * 0.99, v * 1.02], -1)
    return col


def fields(W=4320, H=1100, seed=51):
    """Sol vu de 60 m (côté) : champs, routes, toits — bande défilante avec brume vers le haut."""
    r = np.random.default_rng(seed)
    img = Image.new('RGB', (W, H), (120, 140, 90)); d = ImageDraw.Draw(img)
    y = 0
    rows = [(0, 160), (160, 330), (330, 560), (560, 840), (840, H)]
    pal = [(150, 160, 95), (175, 165, 105), (120, 145, 85), (185, 175, 120), (135, 150, 92), (160, 150, 100)]
    for (a, b) in rows:
        x = 0; hgt = b - a
        while x < W:
            w = int(r.integers(int(hgt * 1.5), int(hgt * 5)))
            d.rectangle((x, a, x + w, b), fill=pal[int(r.integers(0, len(pal)))])
            if r.random() < 0.25:  # maisons
                for k in range(int(r.integers(3, 12))):
                    hx = x + r.random() * w; hy = a + r.random() * hgt * 0.7; s = hgt * 0.12
                    d.rectangle((hx, hy, hx + s * 1.6, hy + s), fill=(190, 170, 160)); d.rectangle((hx, hy - s * 0.5, hx + s * 1.6, hy), fill=(150, 80, 70))
            x += w
        d.rectangle((0, b - 3, W, b + 3), fill=(110, 110, 105))
    img = img.filter(ImageFilter.GaussianBlur(1.2))
    a = np.asarray(img).astype(np.float32) / 255
    a = a * (0.9 + 0.2 * fbm(H, W, 80, 4, seed)[..., None])
    yy = np.arange(H)[:, None] / H
    a = lerp(a, np.array([0.86, 0.83, 0.77]), (np.clip(1 - yy / 0.5, 0, 1) ** 1.5)[..., None] * 0.75)
    return a


if __name__ == '__main__':
    import sys
    want = sys.argv[1:]
    jobs = {'p_sky_day.png': lambda: sky_day(), 'p_sky_warm.png': lambda: sky_day(seed=8, warm=1.0, cloud_amt=0.45),
            'p_far.png': lambda: strip_far(), 'p_runway.png': lambda: runway_strip(), 'p_rw_persp.png': lambda: runway_persp(),
            'p_asphalt.png': lambda: asphalt_macro(), 'p_fields.png': lambda: fields(),
            'p_rw_low.png': lambda: runway_persp(cam_h=6.0, hy=900, seed=33, threshold=False)}
    for k, f in jobs.items():
        if want and k not in want:
            continue
        a = f()
        mode = 'RGBA' if a.shape[-1] == 4 else 'RGB'
        Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8), mode).save(f'{OUT}/{k}'); print(k, a.shape)
