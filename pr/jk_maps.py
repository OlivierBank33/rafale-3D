"""Cartes « topographiques » nuit du 30/10 (même style que pr/andes_map.py).
build('peru')   : Lima -> Pucallpa, Andes + Amazonie (vol LANSA 508, 1971).
build('canary') : Tenerife / Gran Canaria (Los Rodeos, 1977).
Projection : MAP[nom](lon, lat) -> (x, y) en px 1080x1920."""
import json, math
import numpy as np
from scipy import ndimage

W, H = 1080, 1920
VIEWS = {
    'peru': dict(lon0=-79.5, lon1=-71.5, latc=-10.0, yc=900),
    'canary': dict(lon0=-17.6, lon1=-14.6, latc=28.2, yc=900),
    'med': dict(lon0=3.6, lon1=10.6, latc=42.9, yc=900),
}


def proj(v):
    k = W / (v['lon1'] - v['lon0']); ky = k / math.cos(math.radians(v['latc']))
    return (lambda lon, lat: ((lon - v['lon0']) * k, v['yc'] - (lat - v['latc']) * ky)), (lambda x, y: (x / k + v['lon0'], v['latc'] - (y - v['yc']) / ky))


MAP = {n: proj(v)[0] for n, v in VIEWS.items()}


def noise(shape, scale, seed):
    r = np.random.default_rng(seed)
    g = r.random((shape[0] // scale + 3, shape[1] // scale + 3))
    z = ndimage.zoom(g, scale, order=3)[:shape[0], :shape[1]]
    return (z - z.min()) / (z.max() - z.min())


RIDGE = [(-81.0, -3.5), (-79.2, -6.5), (-77.6, -9.0), (-76.0, -11.5), (-74.3, -13.6), (-71.8, -15.4), (-69.0, -17.5)]
PEAKS = [(-16.64, 28.27, 3718, 0.16), (-15.59, 27.97, 1950, 0.15), (-17.24, 28.11, 1480, 0.08), (-17.86, 28.68, 2400, 0.10),
         (-18.03, 27.75, 1500, 0.08), (-14.05, 28.40, 800, 0.25), (-13.65, 29.03, 670, 0.15), (-16.20, 28.53, 1000, 0.07)]


PEAKS_MED = [(8.95, 42.38, 2700, 0.30), (9.10, 42.05, 2300, 0.30), (9.15, 41.80, 2000, 0.28), (9.25, 42.65, 1500, 0.22), (8.85, 42.15, 1900, 0.22),
             (7.15, 44.15, 3000, 0.45), (6.60, 44.45, 3200, 0.50), (7.60, 44.30, 2600, 0.40), (6.30, 43.95, 1800, 0.40), (5.60, 43.53, 1000, 0.15),
             (5.75, 43.33, 1100, 0.13), (5.30, 43.90, 1200, 0.30), (6.20, 43.25, 700, 0.25), (5.45, 43.22, 500, 0.08)]


def elevation(name, lon, lat):
    sh = lon.shape
    fr = sum(noise(sh, s, sd) * a for s, sd, a in ((90, 1, 1.0), (45, 2, 0.5), (22, 3, 0.25), (11, 4, 0.12))) / 1.87
    rd = sum((1 - np.abs(noise(sh, s, 20 + sd) * 2 - 1)) ** 2 * a for sd, (s, a) in enumerate(((60, 1.0), (30, 0.5), (15, 0.25)))) / 1.75
    if name == 'peru':
        # distance à la ligne de crête (polyligne)
        d = np.full(sh, 1e9)
        for (a0, b0), (a1, b1) in zip(RIDGE, RIDGE[1:]):
            vx, vy = a1 - a0, b1 - b0; L2 = vx * vx + vy * vy
            u = np.clip(((lon - a0) * vx + (lat - b0) * vy) / L2, 0, 1)
            d = np.minimum(d, np.hypot(lon - a0 - u * vx, lat - b0 - u * vy))
        z = 4600 * np.exp(-(d / 1.05) ** 2) * (0.5 + 0.65 * rd) + 1400 * np.exp(-(d / 2.0) ** 2) * fr + 180 * fr
        return z
    z = np.zeros(sh)
    for lo, la, h, s in (PEAKS_MED if name == 'med' else PEAKS):
        dd = np.hypot((lon - lo) * math.cos(math.radians(28.2)), lat - la)
        z += h * np.exp(-(dd / s) ** 1.6)
    return z * (0.75 + 0.45 * rd) + 60


def chaikin(px, n=3):
    for _ in range(n):
        q = 0.75 * px + 0.25 * np.roll(px, -1, 0); r = 0.25 * px + 0.75 * np.roll(px, -1, 0)
        px = np.empty((len(q) * 2, 2)); px[0::2] = q; px[1::2] = r
    return px


def build(name, out=None):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    from matplotlib.path import Path
    v = VIEWS[name]; P, INV = proj(v)
    s = 2; h, w = H // s, W // s
    ys, xs = np.mgrid[0:h, 0:w] * s
    lon, lat = INV(xs, ys)
    z = elevation(name, lon, lat)
    z = ndimage.gaussian_filter(z, 1.4)
    feats = json.load(open('/home/claude/geo/ne50.geojson'))['features']
    land = np.zeros((h, w), bool); polys = []
    for f in feats:
        g = f['geometry']; parts = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        for poly in parts:
            ring = np.array(poly[0])
            if ring[:, 0].max() < v['lon0'] - 6 or ring[:, 0].min() > v['lon1'] + 6: continue
            if ring[:, 1].max() < v['latc'] - 12 or ring[:, 1].min() > v['latc'] + 12: continue
            px = np.c_[P(ring[:, 0], ring[:, 1])]
            if name in ('canary', 'med'): px = chaikin(px, 2 if name == 'med' else 3)
            polys.append((f['properties']['ADMIN'], px))
            land |= Path(px).contains_points(np.c_[xs.ravel() + s / 2, ys.ravel() + s / 2]).reshape(h, w)
    z = np.where(land, z, np.nan)
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis('off')
    fig.patch.set_facecolor((0.02, 0.035, 0.06))
    ax.add_patch(plt.Rectangle((0, 0), W, H, color=(0.02, 0.04, 0.075), zorder=0))
    for nm, px in polys:
        ax.fill(px[:, 0], px[:, 1], color=(0.05, 0.07, 0.085), zorder=1)
    X, Y = xs + s / 2, ys + s / 2
    if name == 'peru':                                                          # Amazonie : basses terres vertes
        rl = np.interp(lat, [q[1] for q in RIDGE[::-1]], [q[0] for q in RIDGE[::-1]])
        east = land & (lon > rl + 0.6) & (z < 900)
        mot = 0.55 + 0.45 * (noise(z.shape, 8, 7) * 0.6 + noise(z.shape, 3, 8) * 0.4)
        img = np.zeros(z.shape + (4,)); img[..., 0] = 0.08 * mot; img[..., 1] = 0.30 * mot; img[..., 2] = 0.14 * mot
        img[..., 3] = np.where(east, 0.75, 0) * np.clip((lon - rl - 0.6) / 0.8, 0, 1)
        ax.imshow(img, extent=(0, W, H, 0), zorder=2, interpolation='bilinear')
        ax.contourf(X, Y, z, levels=[2500, 4000, 9000], colors=[(0.95, 0.85, 0.65, 0.06), (1, 0.97, 0.92, 0.12)], zorder=2)
        lv = np.arange(500, 7000, 500)
    else:
        ax.contourf(X, Y, z, levels=[2000, 9000], colors=[(0.95, 0.85, 0.65, 0.10)], zorder=2)
        lv = np.arange(250, 4000, 250)
        if name == 'med':
            ax.imshow(np.zeros(z.shape + (4,)), extent=(0, W, H, 0), zorder=1)
    cm = LinearSegmentedColormap.from_list('t', [(0.15, 0.45, 0.55), (0.35, 0.7, 0.75), (0.95, 0.85, 0.65), (1.0, 0.98, 0.95)])
    ax.contour(X, Y, z, levels=lv, cmap=cm, vmin=200, vmax=(6000 if name == 'peru' else 3800),
               linewidths=[1.7 if q % (1500 if name == 'peru' else 1000) == 0 else 0.8 for q in lv], alpha=0.85, zorder=3)
    for nm, px in polys:
        ax.plot(px[:, 0], px[:, 1], color=(0.6, 0.75, 0.9), lw=1.3 if name == 'peru' else 2.0, alpha=0.55 if name == 'peru' else 0.8, zorder=4)
    fig.savefig(out or f'/home/claude/pr/map_{name}.png', facecolor=fig.get_facecolor()); plt.close(fig)


if __name__ == '__main__':
    import sys
    for n in (sys.argv[1:] or list(VIEWS)): build(n)
