"""Plaques « jungle amazonienne » peintes en 2D (cairo), pour sv_juliane (30/10).
Le rendu Blender (andes_plates.py jungle_*) donnait une canopée « moisie » : on peint ici des houppiers ombrés, en perspective.
  air   : canopée vue d'avion (oblique) avec une rivière en méandres, ciel transparent (peint au rendu)      -> pr/p_jg_air.png  (1300x1920)
  top   : canopée vue de dessus (chute), avec un ruisseau                                                    -> pr/p_jg_top.png  (2400x2400)
  floor : sous-bois (troncs, lianes, fougères), brume                                                      -> pr/p_jg_floor.png (1300x1920)
  river : rivière au ras de l'eau entre deux murs de forêt, reflets, ciel transparent                       -> pr/p_jg_river.png (1300x1920)
Usage : python3 pr/jungle2d.py [air top floor river]"""
import cairo, math, random, sys

PR = '/home/claude/pr/'
GREENS = [(0.17, 0.35, 0.13), (0.21, 0.41, 0.15), (0.13, 0.29, 0.11), (0.27, 0.44, 0.17), (0.19, 0.37, 0.19), (0.24, 0.39, 0.12),
          (0.15, 0.33, 0.16), (0.30, 0.47, 0.20)]
FLOWER = [(0.62, 0.52, 0.18), (0.55, 0.32, 0.38), (0.66, 0.60, 0.30)]


def mix(a, b, f):
    return tuple(x + (y - x) * f for x, y in zip(a, b))


def crown(c, x, y, r, base, rnd, fog=0.0, fogc=(0.75, 0.80, 0.78), light=(-0.55, -0.6), shadow=0.5, detail=True, flat=1.0):
    """houppier : grappe de bulles ombrées (lumière en haut à gauche), ombre portée en bas à droite."""
    lx, ly = light
    if shadow > 0:
        c.save(); c.translate(x - lx * r * 0.35, y - ly * r * 0.35 * flat); c.scale(1, flat)
        g = cairo.RadialGradient(0, 0, r * 0.3, 0, 0, r * 1.2); g.add_color_stop_rgba(0, 0.02, 0.05, 0.02, shadow * (1 - fog)); g.add_color_stop_rgba(1, 0.02, 0.05, 0.02, 0)
        c.new_path(); c.arc(0, 0, r * 1.2, 0, 7); c.set_source(g); c.fill(); c.restore()
    n = rnd.randint(9, 14)
    blobs = [(rnd.uniform(-0.55, 0.55) * r, rnd.uniform(-0.50, 0.42) * r * flat, r * rnd.uniform(0.30, 0.52)) for _ in range(n)]
    blobs.sort(key=lambda b: b[1] - b[0] * 0.3)                                   # les bulles éclairées par-dessus
    hi = mix(tuple(min(1, v * 1.38 + 0.03) for v in base), (0.85, 0.9, 0.45), 0.10)
    lo = tuple(v * 0.40 for v in base)
    hi, mid, lo = mix(hi, fogc, fog), mix(base, fogc, fog), mix(lo, fogc, fog * 0.92)
    for bx, by, br in blobs:
        cx, cy = x + bx, y + by
        g = cairo.RadialGradient(cx + lx * br * 0.45, cy + ly * br * 0.45 * flat, br * 0.05, cx, cy, br)
        g.add_color_stop_rgb(0, *hi); g.add_color_stop_rgb(0.55, *mid); g.add_color_stop_rgb(1, *lo)
        c.save(); c.translate(cx, cy); c.scale(1, flat); c.new_path(); c.arc(0, 0, br, 0, 7); c.restore(); c.set_source(g); c.fill_preserve()
        c.set_source_rgba(*lo, 0.35); c.set_line_width(max(0.5, br * 0.04)); c.stroke()
        if detail and br > 9:                                                     # feuillage : touches claires côté soleil, sombres à l'ombre
            for _ in range(int(br / 1.6)):
                a = rnd.uniform(0, 6.283); d = br * math.sqrt(rnd.random()) * 0.92
                px, py = cx + math.cos(a) * d, cy + math.sin(a) * d * flat
                lit = -(math.cos(a) * lx + math.sin(a) * ly) * d / br
                c.new_path(); c.arc(px, py, br * rnd.uniform(0.05, 0.11), 0, 7)
                if lit > 0.05: c.set_source_rgba(*mix(hi, (1, 1, 0.8), 0.15), 0.25 * lit * (1 - fog))
                else: c.set_source_rgba(*lo, 0.30 * min(1, -lit + 0.3) * (1 - fog))
                c.fill()


# ------------------------------------------------------------------ vue d'avion oblique
def river_x(Z):
    return 160 * math.sin(Z / 900.0) + 55 * math.sin(Z / 210.0 + 0.4) - 40


def build_air(out=PR + 'p_jg_air.png', Wd=1300, Hd=1920, hz=760, h=90.0, R=7.0, hw=26.0, seed=5):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, Wd, Hd); c = cairo.Context(s); cx = Wd / 2
    rnd = random.Random(seed)
    fogc = (0.74, 0.80, 0.80)
    g = cairo.LinearGradient(0, hz, 0, Hd); g.add_color_stop_rgb(0, *fogc); g.add_color_stop_rgb(0.08, 0.20, 0.30, 0.20); g.add_color_stop_rgb(1, 0.03, 0.07, 0.03)
    c.rectangle(0, hz - 2, Wd, Hd); c.set_source(g); c.fill()
    # rivière : polygone (bords à ±hw autour de la ligne centrale), reflets de ciel
    L, Rr = [], []
    y = hz + 1.0
    while y < Hd + 40:
        Z = h * 900 / (y - hz); X = river_x(Z); k = (y - hz) / h
        L.append((cx + (X - hw) * k, y)); Rr.append((cx + (X + hw) * k, y)); y += 2.0
    c.new_path(); c.move_to(*L[0])
    for p in L[1:]: c.line_to(*p)
    for p in Rr[::-1]: c.line_to(*p)
    c.close_path()
    g = cairo.LinearGradient(0, hz, 0, Hd); g.add_color_stop_rgb(0, 0.86, 0.88, 0.86); g.add_color_stop_rgb(0.15, 0.62, 0.58, 0.48); g.add_color_stop_rgb(1, 0.30, 0.22, 0.13)
    c.set_source(g); c.fill_preserve(); c.save(); c.clip()
    for j in range(260):                                                          # rides
        yy = hz + (Hd - hz) * (j / 260) ** 1.6; wv = 2 + 30 * (yy - hz) / (Hd - hz)
        c.rectangle(0, yy, Wd, max(0.6, wv * 0.05)); c.set_source_rgba(1, 1, 1, 0.05 + 0.05 * rnd.random()); c.fill()
    c.restore()
    # houppiers, du lointain vers le premier plan
    y = hz + 2.0
    while y < Hd + 120:
        Z = h * 900 / (y - hz); k = (y - hz) / h
        r = max(1.8, R * k)
        fog = min(1.0, (Z / 5200.0) ** 0.8)
        X0 = river_x(Z)
        x = -r * rnd.random()
        while x < Wd + r:
            Xw = (x - cx) / k
            if abs(Xw - X0) > hw + R * 0.25:
                emerg = rnd.random() < 0.06
                rr_ = r * (rnd.uniform(0.85, 1.15) * (1.5 if emerg else 1.0))
                base = rnd.choice(FLOWER) if rnd.random() < 0.025 else rnd.choice(GREENS)
                if abs(Xw - X0) < hw + R * 1.6: base = mix(base, (0.10, 0.22, 0.08), 0.2)
                crown(c, x + rnd.uniform(-0.3, 0.3) * r, y - (rr_ * 0.5 if emerg else 0) + rnd.uniform(-0.2, 0.2) * r, rr_, base, rnd, fog=fog, fogc=fogc,
                      shadow=0.55, detail=r > 10, flat=0.82)
            x += r * rnd.uniform(1.05, 1.45)
        y += max(1.2, r * 0.42)
    # brume : bandes sur l'horizon et nappes basses
    g = cairo.LinearGradient(0, hz - 30, 0, hz + 220); g.add_color_stop_rgba(0, *fogc, 0.0); g.add_color_stop_rgba(0.2, *fogc, 0.85); g.add_color_stop_rgba(1, *fogc, 0)
    c.rectangle(0, hz - 30, Wd, 250); c.set_source(g); c.fill()
    for j in range(14):
        yy = hz + 40 + (j ** 1.6) * 9; xx = rnd.uniform(0, Wd); rw = 160 + j * 30
        c.save(); c.translate(xx, yy); c.scale(1, 0.12)
        g = cairo.RadialGradient(0, 0, 0, 0, 0, rw); g.add_color_stop_rgba(0, 1, 1, 1, 0.35); g.add_color_stop_rgba(1, 1, 1, 1, 0)
        c.new_path(); c.arc(0, 0, rw, 0, 7); c.set_source(g); c.fill(); c.restore()
    s.write_to_png(out)


# ------------------------------------------------------------------ vue de dessus (chute)
def build_top(out=PR + 'p_jg_top.png', S=2400, seed=8):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, S, S); c = cairo.Context(s); rnd = random.Random(seed)
    c.set_source_rgb(0.03, 0.07, 0.03); c.paint()
    # ruisseau en méandres
    pts = []
    for j in range(0, S + 41, 20):
        x = S * 0.5 + 300 * math.sin(j / 420.0) + 120 * math.sin(j / 150.0 + 2)
        pts.append((x, j - 20))
    c.new_path(); c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    c.set_source_rgb(0.36, 0.28, 0.17); c.set_line_width(60); c.stroke_preserve(); c.set_source_rgba(0.75, 0.75, 0.7, 0.25); c.set_line_width(26); c.stroke()
    def near(x, y):
        return min(abs(x - px) for px, py in pts if abs(py - y) < 40) if True else 99
    crowns = []
    for _ in range(int(S * S / 1500)):
        x, y = rnd.uniform(-60, S + 60), rnd.uniform(-60, S + 60)
        r = rnd.uniform(28, 56) * (1.6 if rnd.random() < 0.05 else 1)
        d = near(x, y)
        if d < 30 + r * 0.6: continue
        crowns.append((r + rnd.random() * 8, x, y, r))
    crowns.sort()
    for _, x, y, r in crowns:
        base = rnd.choice(FLOWER) if rnd.random() < 0.03 else rnd.choice(GREENS)
        crown(c, x, y, r, base, rnd, shadow=0.7, detail=True, light=(-0.6, -0.55))
    s.write_to_png(out)


# ------------------------------------------------------------------ sous-bois
def build_floor(out=PR + 'p_jg_floor.png', Wd=1300, Hd=1920, seed=11):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, Wd, Hd); c = cairo.Context(s); rnd = random.Random(seed)
    g = cairo.LinearGradient(0, 0, 0, Hd); g.add_color_stop_rgb(0, 0.10, 0.22, 0.12); g.add_color_stop_rgb(0.45, 0.36, 0.50, 0.30); g.add_color_stop_rgb(1, 0.06, 0.10, 0.04)
    c.set_source(g); c.paint()
    fogc = (0.46, 0.60, 0.40)
    for layer in range(6):                                                         # troncs, du fond vers l'avant
        dep = 1 - layer / 5.0; n = int(6 + 10 * dep)
        col = mix((0.05, 0.07, 0.04), fogc, 0.85 * dep ** 1.2)
        for _ in range(n):
            x = rnd.uniform(-40, Wd + 40); w = (14 + 70 * (1 - dep)) * rnd.uniform(0.6, 1.3)
            c.new_path(); c.move_to(x - w / 2, Hd); c.curve_to(x - w * 0.45, Hd * 0.6, x - w * 0.3 + rnd.uniform(-20, 20), Hd * 0.3, x - w * 0.32, -10)
            c.line_to(x + w * 0.32, -10); c.curve_to(x + w * 0.3, Hd * 0.3, x + w * 0.45, Hd * 0.6, x + w / 2, Hd); c.close_path()
            c.set_source_rgb(*col); c.fill()
            if layer >= 2:                                                         # mousse éclairée sur le bord gauche
                c.new_path(); c.move_to(x - w / 2 + 3, Hd); c.curve_to(x - w * 0.45 + 3, Hd * 0.6, x - w * 0.3 + 3, Hd * 0.3, x - w * 0.32 + 3, -10)
                c.set_source_rgba(0.35, 0.55, 0.22, 0.35 * (1 - dep)); c.set_line_width(3 + 5 * (1 - dep)); c.stroke()
            if layer >= 3:                                                         # contreforts
                c.new_path(); c.move_to(x - w * 1.6, Hd); c.curve_to(x - w * 0.6, Hd - 60, x - w * 0.5, Hd - 200, x - w * 0.4, Hd - 300); c.line_to(x + w * 0.4, Hd - 300)
                c.curve_to(x + w * 0.5, Hd - 200, x + w * 0.6, Hd - 60, x + w * 1.6, Hd); c.close_path(); c.fill()
        for _ in range(int(3 + 4 * (1 - dep))):                                   # lianes
            x = rnd.uniform(0, Wd); c.new_path(); c.move_to(x, -10)
            c.curve_to(x + rnd.uniform(-120, 120), Hd * 0.3, x + rnd.uniform(-160, 160), Hd * 0.55, x + rnd.uniform(-60, 60), Hd * rnd.uniform(0.5, 0.95))
            c.set_source_rgb(*col); c.set_line_width(2 + 6 * (1 - dep)); c.stroke()
        g = cairo.LinearGradient(0, 0, 0, Hd); g.add_color_stop_rgba(0, *fogc, 0.10); g.add_color_stop_rgba(0.6, *fogc, 0.18); g.add_color_stop_rgba(1, *fogc, 0.02)
        c.rectangle(0, 0, Wd, Hd); c.set_source(g); c.fill()
    # canopée en haut (masse sombre de feuilles)
    for _ in range(120):
        x = rnd.uniform(-50, Wd + 50); y = rnd.uniform(-80, 260); r = rnd.uniform(40, 120)
        c.new_path(); c.arc(x, y, r, 0, 7); c.set_source_rgba(0.03, 0.06, 0.03, 0.85); c.fill()
    # fougères et feuilles au premier plan
    def frond(x, y, L, ang, col, w=1.0):
        c.save(); c.translate(x, y); c.rotate(ang)
        c.new_path(); c.move_to(0, 0); c.curve_to(L * 0.3, -L * 0.15, L * 0.7, -L * 0.12, L, L * 0.08); c.set_source_rgb(*col); c.set_line_width(4 * w); c.stroke()
        for j in range(1, 22):
            u = j / 22; px = L * u; py = -L * 0.16 * math.sin(u * math.pi) + L * 0.08 * u ** 3; ll = L * 0.22 * math.sin(u * math.pi) ** 0.7 * w
            for sgn in (-1, 1):
                c.new_path(); c.move_to(px, py); c.curve_to(px + ll * 0.3, py + sgn * ll * 0.5, px + ll * 0.6, py + sgn * ll * 0.9, px + ll * 0.7, py + sgn * ll)
                c.curve_to(px + ll * 0.5, py + sgn * ll * 0.6, px + ll * 0.2, py + sgn * ll * 0.3, px, py); c.fill()
        c.restore()
    for j in range(16):
        x = rnd.uniform(-100, Wd + 100); y = Hd + rnd.uniform(-60, 40)
        frond(x, y, rnd.uniform(380, 640), -math.pi / 2 + rnd.uniform(-1.0, 1.0), mix((0.02, 0.05, 0.02), (0.10, 0.20, 0.08), rnd.random() * 0.6), 1.2)
    s.write_to_png(out)


# ------------------------------------------------------------------ rivière au ras de l'eau
def build_river(out=PR + 'p_jg_river.png', Wd=1300, Hd=1920, hz=900, seed=21):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, Wd, Hd); c = cairo.Context(s); rnd = random.Random(seed)
    cx = Wd / 2; f = 900.0; h = 1.6; hw = 30.0; top = 32.0
    fogc = (0.78, 0.82, 0.80)
    walls = cairo.ImageSurface(cairo.FORMAT_ARGB32, Wd, Hd); cw = cairo.Context(walls)
    for side in (-1, 1):
        Z = 3000.0
        while Z > 6:
            k = f / Z; xb = cx + side * (hw + 6 * math.sin(Z / 37.0)) * k; yw = hz + h * k; yt = hz - (top - h + 4 * math.sin(Z / 23.0)) * k
            r = max(1.5, 6.5 * k); fog = min(1.0, (Z / 1600.0) ** 0.75)
            # mur : colonne de houppiers entre l'eau et le sommet de la canopée (plus sombre vers l'eau : sous-bois à l'ombre)
            if rnd.random() < 0.18: yt -= r * rnd.uniform(0.8, 2.0)               # arbres émergents
            yy = yt
            while yy < yw - r * 0.3:
                q = (yy - yt) / max(1, yw - yt)
                for m in range(3):
                    xx = xb + side * (r * 0.4 + m * r * 1.2) + rnd.uniform(-0.4, 0.4) * r
                    if -r < xx < Wd + r:
                        base = mix(rnd.choice(FLOWER) if rnd.random() < 0.02 else rnd.choice(GREENS), (0.02, 0.05, 0.02), 0.65 * q ** 1.5)
                        crown(cw, xx, yy, r * rnd.uniform(0.8, 1.2), base, rnd, fog=fog, fogc=fogc, shadow=0.35, detail=r > 9, light=(-0.4 * side - 0.2, -0.7))
                yy += r * 0.75
            Z *= 0.955 if Z > 60 else 0.93
        cw.rectangle(0, 0, 0, 0)
    # eau : ciel réfléchi + reflets inversés des murs, assombris
    g = cairo.LinearGradient(0, hz, 0, Hd); g.add_color_stop_rgb(0, 0.82, 0.84, 0.82); g.add_color_stop_rgb(0.25, 0.48, 0.42, 0.32); g.add_color_stop_rgb(1, 0.20, 0.15, 0.09)
    c.rectangle(0, hz, Wd, Hd - hz); c.set_source(g); c.fill()
    c.save(); c.rectangle(0, hz, Wd, Hd - hz); c.clip(); c.translate(0, 2 * hz); c.scale(1, -1); c.set_source_surface(walls, 0, 0); c.paint_with_alpha(0.55); c.restore()
    c.save(); c.rectangle(0, hz, Wd, Hd - hz); c.clip()
    for j in range(240):                                                          # rides qui cassent le reflet
        yy = hz + (Hd - hz) * (j / 240) ** 1.7; wv = 1 + 26 * (yy - hz) / (Hd - hz)
        c.rectangle(rnd.uniform(-200, Wd), yy, rnd.uniform(200, 900), max(0.6, wv * 0.12)); c.set_source_rgba(0.85, 0.85, 0.8, 0.10 + 0.08 * rnd.random()); c.fill()
        c.rectangle(rnd.uniform(-200, Wd), yy + wv * 0.2, rnd.uniform(200, 900), max(0.6, wv * 0.10)); c.set_source_rgba(0.1, 0.07, 0.04, 0.18); c.fill()
    g = cairo.LinearGradient(0, hz, 0, Hd); g.add_color_stop_rgba(0, 0.30, 0.22, 0.13, 0.0); g.add_color_stop_rgba(1, 0.30, 0.22, 0.13, 0.55)
    c.rectangle(0, hz, Wd, Hd - hz); c.set_source(g); c.fill(); c.restore()
    c.set_source_surface(walls, 0, 0); c.paint()
    g = cairo.LinearGradient(0, hz - 260, 0, hz + 40); g.add_color_stop_rgba(0, *fogc, 0); g.add_color_stop_rgba(0.75, *fogc, 0.75); g.add_color_stop_rgba(1, *fogc, 0.2)
    c.rectangle(0, hz - 260, Wd, 300); c.set_source(g); c.fill()
    s.write_to_png(out)


if __name__ == '__main__':
    B = {'air': build_air, 'top': build_top, 'floor': build_floor, 'river': build_river}
    for n in (sys.argv[1:] or list(B)):
        B[n](); print('DONE', n, flush=True)
