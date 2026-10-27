"""Carte en relief (ombrage) Tibet / Sichuan pour sv_sichuan. Hauteurs procédurales : plateau (contour ~3 000 m approché), Himalaya,
Hengduan, bassin du Sichuan bas. Projection partagée avec sm_scenes11.MAPXY. Sortie : pr/relief_sw.png (1080x1920)."""
import numpy as np
from scipy import ndimage
from matplotlib.path import Path
from PIL import Image

W, H = 1080, 1920
def MAPXY(lon, lat): return (lon - 89.5) * 50.0 + 60.0, 900.0 - (lat - 29.8) * 57.7
def INV(x, y): return (x - 60.0) / 50.0 + 89.5, 29.8 - (y - 900.0) / 57.7

PLATEAU = [(78, 35.5), (80, 36.6), (84, 36.4), (88, 36.6), (91, 37.6), (95, 38.6), (99, 38.2), (101.8, 37.2), (103.4, 35.2), (103.0, 32.4),
           (102.6, 30.4), (102.0, 28.6), (101.0, 27.2), (99.2, 26.0), (98.3, 25.6), (97.2, 27.6), (95.4, 28.9), (92.2, 27.9), (89.2, 27.7),
           (86.2, 27.9), (83.0, 29.0), (81.0, 30.0), (79.0, 32.0), (78, 34)]


def noise(shape, scale, seed):
    r = np.random.default_rng(seed)
    g = r.random((shape[0] // scale + 3, shape[1] // scale + 3))
    z = ndimage.zoom(g, scale, order=3)
    z = z[:shape[0], :shape[1]]
    return (z - z.min()) / (z.max() - z.min())


def build(out='/home/claude/pr/relief_sw.png', s=2):
    h, w = H // s, W // s
    ys, xs = np.mgrid[0:h, 0:w] * s
    lon, lat = INV(xs, ys)
    inside = Path(PLATEAU).contains_points(np.c_[lon.ravel(), lat.ravel()]).reshape(h, w)
    din = ndimage.distance_transform_edt(inside) * s / 50.0          # degrés vers l'intérieur
    dout = ndimage.distance_transform_edt(~inside) * s / 50.0
    fr = sum(noise((h, w), sc, sd) * a for sc, sd, a in ((96, 1, 1.0), (40, 2, 0.5), (16, 3, 0.25), (6, 4, 0.08))) / 1.83
    ridge = sum((1 - np.abs(noise((h, w), sc, 20 + sd) * 2 - 1)) ** 2 * a for sd, (sc, a) in enumerate(((48, 1.0), (24, 0.55), (12, 0.25), (6, 0.08))) ) / 1.88
    sig = lambda v, k=3.0: 1 / (1 + np.exp(-v * k))
    plat = np.clip(din / 1.0, 0, 1); plat = plat * plat * (3 - 2 * plat)
    foot = np.exp(-(dout / 0.5) ** 2) * 0.25                          # piémont
    z = 200 + 900 * fr * (0.4 + ridge)
    z += (plat + foot) * (2900 + 500 * fr + 1300 * ridge)
    south = sig(30.4 - lat) * sig(97.8 - lon)
    z += south * np.clip(din / 0.15, 0, 1) * 2400 * np.exp(-((din - 0.35) / 0.4) ** 2) * (0.3 + 1.0 * ridge)      # Himalaya
    heng = sig(lon - 97.5) * sig(103.2 - lon) * sig(33 - lat)
    z += heng * 600 * (0.5 + 0.5 * np.sin((lon - 97.5) * 7.5 + 3.0 * fr)) * plat                                 # Hengduan (crêtes N-S)
    basin = ((lon - 105.6) / 2.4) ** 2 + ((lat - 30.2) / 1.5) ** 2
    z = z * (0.45 + 0.55 * np.clip(basin, 0, 1))
    z = ndimage.gaussian_filter(z, 0.6)
    gy, gx = np.gradient(z / (s * 150.0))
    az, alt = np.radians(315), np.radians(38)
    slope = np.arctan(np.hypot(gx, gy)); aspect = np.arctan2(-gx, gy)
    sh = np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - aspect)
    sh = np.clip(sh, 0, 1)
    stops = [(0, (0.13, 0.21, 0.13)), (1000, (0.19, 0.25, 0.15)), (2500, (0.30, 0.27, 0.18)), (4300, (0.36, 0.30, 0.21)), (5600, (0.42, 0.37, 0.29)), (6500, (0.80, 0.81, 0.85)), (7500, (0.97, 0.97, 1.0))]
    col = np.zeros((h, w, 3))
    for i in range(3):
        col[..., i] = np.interp(z, [a for a, _ in stops], [b[i] for _, b in stops])
    img = col * (0.45 + 0.75 * sh[..., None])
    vy = np.linspace(-1, 1, h)[:, None]; vx = np.linspace(-1, 1, w)[None, :]
    img *= (1 - 0.45 * np.clip(vx ** 2 + (vy * 1.1) ** 2 - 0.15, 0, 1))[..., None]
    img = np.clip(img * 255, 0, 255).astype(np.uint8)
    Image.fromarray(img).resize((W, H), Image.BICUBIC).save(out)


if __name__ == '__main__':
    build()


def build_topo(out='/home/claude/pr/topo_sw.png', s=2):
    """version « carte topographique » : courbes de niveau lumineuses sur fond nuit (plus lisible et plus élégante que l'ombrage)."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    h, w = H // s, W // s
    ys, xs = np.mgrid[0:h, 0:w] * s
    lon, lat = INV(xs, ys)
    inside = Path(PLATEAU).contains_points(np.c_[lon.ravel(), lat.ravel()]).reshape(h, w)
    din = ndimage.distance_transform_edt(inside) * s / 50.0
    dout = ndimage.distance_transform_edt(~inside) * s / 50.0
    fr = sum(noise((h, w), sc, sd) * a for sc, sd, a in ((120, 1, 1.0), (60, 2, 0.5), (30, 3, 0.25))) / 1.75
    ridge = sum((1 - np.abs(noise((h, w), sc, 20 + sd) * 2 - 1)) ** 2 * a for sd, (sc, a) in enumerate(((60, 1.0), (30, 0.5)))) / 1.5
    sig = lambda v, k=3.0: 1 / (1 + np.exp(-v * k))
    plat = np.clip(din / 1.2, 0, 1); plat = plat * plat * (3 - 2 * plat)
    foot = np.exp(-(dout / 0.7) ** 2) * 0.3
    z = 300 + 1400 * fr * (0.3 + ridge)
    z += (plat + foot) * (3000 + 600 * fr + 900 * ridge)
    south = sig(30.4 - lat) * sig(97.8 - lon)
    z += south * np.clip(din / 0.15, 0, 1) * 2600 * np.exp(-((din - 0.4) / 0.45) ** 2) * (0.5 + 0.6 * ridge)
    basin = ((lon - 105.6) / 2.4) ** 2 + ((lat - 30.2) / 1.5) ** 2
    z = z * (0.5 + 0.5 * np.clip(basin, 0, 1))
    z = ndimage.gaussian_filter(z, 2.0)
    cm = LinearSegmentedColormap.from_list('t', [(0.15, 0.45, 0.55), (0.35, 0.7, 0.75), (0.95, 0.82, 0.55), (1.0, 0.97, 0.92)])
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis('off')
    fig.patch.set_alpha(0)
    X, Y = xs + s / 2, ys + s / 2
    ax.contourf(X, Y, z, levels=[2500, 4000, 5500, 9000], colors=[(0.95, 0.75, 0.45, 0.05), (0.95, 0.75, 0.45, 0.09), (1, 0.95, 0.9, 0.14)])
    lv = np.arange(500, 8000, 500)
    ax.contour(X, Y, z, levels=lv, cmap=cm, vmin=300, vmax=7000, linewidths=[1.9 if v % 1500 == 0 else 0.9 for v in lv], alpha=0.85)
    fig.savefig(out, transparent=True); plt.close(fig)
