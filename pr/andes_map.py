"""Cartes « topographiques » nuit pour sv_andes (courbes de niveau lumineuses, côtes et frontières Natural Earth 50 m).
build('sa') : Uruguay -> Andes (route Montevideo-Mendoza-Santiago) ; build('zoom') : secteur Curicó / glacier des Larmes.
Projection : MAP[nom](lon, lat) -> (x, y) en px 1080x1920."""
import json, math
import numpy as np
from scipy import ndimage

W, H = 1080, 1920
VIEWS = {
    'sa': dict(lon0=-75.5, lon1=-53.0, latc=-33.5, yc=900),
    'zoom': dict(lon0=-71.9, lon1=-69.1, latc=-34.85, yc=880),
    'trek': dict(lon0=-71.15, lon1=-69.95, latc=-34.82, yc=880),
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


def elevation(lon, lat, zoom):
    ridge = -70.05 + 0.12 * (lat + 33) + 0.25 * np.sin(lat * 2.1)
    w = 0.75
    sh = lon.shape; sc = 1 if zoom else 1
    fr = sum(noise(sh, s, sd) * a for s, sd, a in ((90, 1, 1.0), (45, 2, 0.5), (22, 3, 0.25), (11, 4, 0.12))) / 1.87
    rd = sum((1 - np.abs(noise(sh, s, 20 + sd) * 2 - 1)) ** 2 * a for sd, (s, a) in enumerate(((60, 1.0), (30, 0.5), (15, 0.25)))) / 1.75
    core = np.exp(-((lon - ridge) / w) ** 2)
    z = 4300 * core * (0.55 + 0.6 * rd) + 1200 * np.exp(-((lon - ridge - 0.9) / 1.0) ** 2) * fr
    z += 2500 * np.exp(-((lon + 69.95) ** 2 + (lat + 32.65) ** 2) / 0.05)          # Aconcagua
    z += 900 * np.exp(-((lon + 71.9) / 0.35) ** 2) * fr                            # cordillère côtière
    z += 250 * fr
    return z


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
    z = elevation(lon, lat, name == 'zoom')
    z = ndimage.gaussian_filter(z, 1.2 if name == 'sa' else 1.6)
    feats = json.load(open('/home/claude/geo/ne50.geojson'))['features']
    land = np.zeros((h, w), bool); polys = []
    for f in feats:
        g = f['geometry']; parts = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        for poly in parts:
            ring = np.array(poly[0])
            if ring[:, 0].max() < v['lon0'] - 5 or ring[:, 0].min() > v['lon1'] + 5: continue
            if ring[:, 1].max() < -60 or ring[:, 1].min() > 0: continue
            px = np.c_[P(ring[:, 0], ring[:, 1])]
            polys.append((f['properties']['ADMIN'], px))
            land |= Path(px).contains_points(np.c_[xs.ravel() + s / 2, ys.ravel() + s / 2]).reshape(h, w)
    z = np.where(land, z, np.nan)
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis('off')
    fig.patch.set_facecolor((0.02, 0.035, 0.06))
    ax.add_patch(plt.Rectangle((0, 0), W, H, color=(0.02, 0.04, 0.075), zorder=0))
    for nm, px in polys:
        ax.fill(px[:, 0], px[:, 1], color=(0.05, 0.07, 0.085), zorder=1)
    cm = LinearSegmentedColormap.from_list('t', [(0.15, 0.45, 0.55), (0.35, 0.7, 0.75), (0.95, 0.85, 0.65), (1.0, 0.98, 0.95)])
    X, Y = xs + s / 2, ys + s / 2
    ax.contourf(X, Y, z, levels=[2500, 4000, 9000], colors=[(0.95, 0.85, 0.65, 0.06), (1, 0.97, 0.92, 0.12)], zorder=2)
    lv = np.arange(500, 7000, 500)
    ax.contour(X, Y, z, levels=lv, cmap=cm, vmin=300, vmax=6000, linewidths=[1.7 if q % 1500 == 0 else 0.8 for q in lv], alpha=0.85, zorder=3)
    for nm, px in polys:
        ax.plot(px[:, 0], px[:, 1], color=(0.6, 0.75, 0.9), lw=1.3, alpha=0.55, zorder=4)
    fig.savefig(out or f'/home/claude/pr/map_{name}.png', facecolor=fig.get_facecolor()); plt.close(fig)


if __name__ == '__main__':
    import sys
    for n in (sys.argv[1:] or list(VIEWS)): build(n)
