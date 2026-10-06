"""Mascotte minuteaero : pilote de chasse en combinaison de vol, style « sticker ».
draw(ctx, cx, cy, h, expr='smile', mouth=0.0, blink=0.0, look=(0,0), tilt=0.0)
  cx, cy = centre bas du buste ; h = hauteur totale à l'écran (px)
  expr : smile | happy | surprised | wink | think | doubt
  mouth : 0..1 ouverture (parole) ; blink : 0..1 ; look : direction du regard (-1..1)
Le personnage est rendu à 900 px de haut dans un cache (contour blanc + trait sombre), puis mis à l'échelle.
"""
import cairo, math
import numpy as np
from PIL import Image, ImageFilter

BASE_W, BASE_H = 760, 900
SKIN = (0.96, 0.78, 0.62); SKIN_D = (0.86, 0.62, 0.47); SKIN_DD = (0.72, 0.48, 0.36)
SUIT = (0.36, 0.42, 0.27); SUIT_D = (0.27, 0.32, 0.2); SUIT_L = (0.45, 0.52, 0.34)
HELM = (0.93, 0.94, 0.95); HELM_D = (0.74, 0.77, 0.8); HELM_DD = (0.5, 0.54, 0.58)
VISOR = (0.13, 0.15, 0.2); GOLD = (0.95, 0.74, 0.25)
INK = (0.12, 0.11, 0.13)
HAIR = (0.24, 0.16, 0.11)


def rr(c, x, y, w, h, r):
    c.new_sub_path(); c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); c.close_path()


def ell(c, x, y, rx, ry):
    c.save(); c.translate(x, y); c.scale(rx, ry); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()


def fill_stroke(c, col, lw=6, ink=INK):
    c.set_source_rgb(*col); c.fill_preserve(); c.set_source_rgb(*ink); c.set_line_width(lw); c.stroke()


def grad_fill(c, x0, y0, x1, y1, c0, c1, lw=6):
    g = cairo.LinearGradient(x0, y0, x1, y1); g.add_color_stop_rgb(0, *c0); g.add_color_stop_rgb(1, *c1)
    c.set_source(g); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(lw); c.stroke()


# ---------------------------------------------------------------- corps
def body(c):
    # buste (combinaison)
    c.move_to(80, 900); c.curve_to(85, 760, 140, 690, 250, 668); c.line_to(510, 668)
    c.curve_to(620, 690, 675, 760, 680, 900); c.close_path()
    grad_fill(c, 0, 668, 0, 900, SUIT_L, SUIT, 7)
    # coutures d'épaule / plis
    c.set_source_rgba(*SUIT_D, 1); c.set_line_width(5)
    c.move_to(175, 720); c.curve_to(190, 780, 195, 840, 190, 900); c.stroke()
    c.move_to(585, 720); c.curve_to(570, 780, 565, 840, 570, 900); c.stroke()
    # cou
    c.move_to(318, 600); c.line_to(318, 690); c.line_to(442, 690); c.line_to(442, 600); c.close_path()
    fill_stroke(c, SKIN_D, 6)
    # col en V + tee-shirt sombre
    c.move_to(300, 668); c.line_to(380, 790); c.line_to(460, 668); c.close_path(); fill_stroke(c, (0.17, 0.2, 0.15), 6)
    c.move_to(318, 668); c.line_to(380, 760); c.line_to(442, 668); c.close_path(); fill_stroke(c, SKIN_D, 5)
    # cols de la combinaison
    c.move_to(250, 662); c.line_to(300, 662); c.line_to(380, 800); c.line_to(330, 760); c.line_to(262, 706); c.close_path()
    fill_stroke(c, SUIT_L, 6)
    c.move_to(510, 662); c.line_to(460, 662); c.line_to(380, 800); c.line_to(430, 760); c.line_to(498, 706); c.close_path()
    fill_stroke(c, SUIT_L, 6)
    # fermeture éclair
    c.set_source_rgb(*SUIT_D); c.set_line_width(6); c.move_to(380, 800); c.line_to(380, 900); c.stroke()
    c.set_source_rgb(0.75, 0.75, 0.72); rr(c, 372, 812, 16, 26, 4); c.fill()
    # ailes de pilote (poitrine gauche à l'écran = droite du perso)
    c.save(); c.translate(250, 800)
    for s in (-1, 1):
        c.save(); c.scale(s, 1)
        c.move_to(8, -4); c.curve_to(40, -16, 70, -14, 96, -6); c.curve_to(70, 0, 40, 6, 8, 8); c.close_path()
        c.set_source_rgb(*GOLD); c.fill_preserve(); c.set_source_rgb(0.55, 0.4, 0.1); c.set_line_width(3); c.stroke()
        for k in range(3):
            c.move_to(30 + k * 20, -9 + k); c.line_to(24 + k * 20, 5); c.stroke()
        c.restore()
    ell(c, 0, 0, 13, 13); c.set_source_rgb(*GOLD); c.fill_preserve(); c.set_source_rgb(0.55, 0.4, 0.1); c.set_line_width(3); c.stroke()
    c.restore()
    # bande nominative
    rr(c, 440, 784, 150, 40, 6); fill_stroke(c, SUIT_D, 4)
    c.select_font_face('Poppins', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(21)
    t = 'MINUTEAERO'; e = c.text_extents(t); c.set_source_rgb(0.92, 0.9, 0.78); c.move_to(515 - e.x_advance / 2, 812); c.show_text(t)
    # écusson drapeau sur l'épaule droite (à l'écran)
    c.save(); c.translate(598, 744); c.rotate(0.38)
    rr(c, -34, -22, 68, 44, 8); c.set_source_rgb(1, 1, 1); c.fill()
    for k, col in enumerate([(0.0, 0.2, 0.6), (1, 1, 1), (0.88, 0.1, 0.2)]):
        c.rectangle(-30 + k * 20, -18, 20, 36); c.set_source_rgb(*col); c.fill()
    rr(c, -34, -22, 68, 44, 8); c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
    c.restore()


# ---------------------------------------------------------------- tête
def head_base(c):
    # oreilles
    for x, s in ((206, -1), (554, 1)):
        ell(c, x, 420, 30, 44); fill_stroke(c, SKIN, 6)
        c.set_source_rgb(*SKIN_D); ell(c, x + s * 2, 422, 14, 24); c.fill()
    # visage
    c.move_to(380, 175)
    c.curve_to(505, 175, 560, 270, 560, 390)
    c.curve_to(560, 520, 480, 625, 380, 628)
    c.curve_to(280, 625, 200, 520, 200, 390)
    c.curve_to(200, 270, 255, 175, 380, 175); c.close_path()
    g = cairo.RadialGradient(350, 360, 40, 380, 420, 290)
    g.add_color_stop_rgb(0, 0.99, 0.84, 0.69); g.add_color_stop_rgb(0.7, *SKIN); g.add_color_stop_rgb(1, *SKIN_D)
    c.set_source(g); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    # mâchoire ombrée (barbe de 3 jours très légère)
    c.save(); c.move_to(250, 500); c.curve_to(290, 600, 470, 600, 510, 500); c.curve_to(480, 630, 280, 630, 250, 500)
    c.set_source_rgba(*SKIN_DD, 0.18); c.fill(); c.restore()
    # joues
    for x in (275, 485):
        g = cairo.RadialGradient(x, 470, 4, x, 470, 46); g.add_color_stop_rgba(0, 0.95, 0.5, 0.45, 0.35); g.add_color_stop_rgba(1, 0.95, 0.5, 0.45, 0)
        c.set_source(g); ell(c, x, 470, 50, 36); c.fill()
    # mèche de cheveux sous le casque
    c.move_to(262, 268); c.curve_to(300, 300, 340, 290, 360, 262); c.curve_to(390, 296, 450, 300, 498, 268)
    c.line_to(498, 240); c.line_to(262, 240); c.close_path(); fill_stroke(c, HAIR, 5)


def helmet(c):
    # coque
    c.move_to(188, 400)
    c.curve_to(170, 230, 260, 112, 380, 110)
    c.curve_to(500, 112, 590, 230, 572, 400)
    c.line_to(548, 404)
    c.curve_to(548, 330, 530, 270, 498, 262)
    c.curve_to(430, 230, 330, 230, 262, 262)
    c.curve_to(230, 270, 212, 330, 212, 404)
    c.close_path()
    g = cairo.LinearGradient(220, 110, 540, 400); g.add_color_stop_rgb(0, 1, 1, 1); g.add_color_stop_rgb(0.6, *HELM); g.add_color_stop_rgb(1, *HELM_D)
    c.set_source(g); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    # bord gris
    c.move_to(212, 404); c.curve_to(212, 330, 230, 270, 262, 262); c.curve_to(330, 230, 430, 230, 498, 262)
    c.curve_to(530, 270, 548, 330, 548, 404)
    c.set_source_rgb(*HELM_DD); c.set_line_width(14); c.stroke_preserve(); c.set_source_rgb(*INK); c.set_line_width(3); c.stroke()
    # visière relevée (teintée)
    c.move_to(242, 232); c.curve_to(270, 160, 490, 160, 518, 232); c.curve_to(470, 206, 290, 206, 242, 232); c.close_path()
    g = cairo.LinearGradient(0, 160, 0, 232); g.add_color_stop_rgb(0, 0.32, 0.36, 0.46); g.add_color_stop_rgb(1, *VISOR)
    c.set_source(g); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.55); c.set_line_width(6); c.move_to(300, 192); c.curve_to(330, 182, 360, 180, 390, 180); c.stroke()
    # rail central + bande tricolore
    c.set_source_rgb(*HELM_DD); rr(c, 368, 112, 24, 56, 8); c.fill()
    for k, col in enumerate([(0.0, 0.2, 0.6), (1, 1, 1), (0.88, 0.1, 0.2)]):
        c.rectangle(328 + k * 35, 140, 35, 12); c.set_source_rgb(*col); c.fill()
    c.rectangle(328, 140, 105, 12); c.set_source_rgb(*INK); c.set_line_width(3); c.stroke()
    # reflet coque
    c.set_source_rgba(1, 1, 1, 0.7); c.set_line_width(10); c.move_to(250, 190); c.curve_to(265, 160, 290, 140, 320, 128); c.stroke()
    # écouteurs / attaches latérales
    for x in (200, 560):
        ell(c, x, 400, 26, 34); fill_stroke(c, HELM_D, 6)
        ell(c, x, 400, 10, 12); c.set_source_rgb(*HELM_DD); c.fill()


def oxygen_mask(c):
    # masque à oxygène pendant sur la gauche (à l'écran) + tuyau
    c.save(); c.translate(180, 520); c.rotate(0.35)
    c.set_source_rgb(*SUIT_D); c.set_line_width(22); c.move_to(10, 40)
    c.curve_to(10, 120, -40, 160, -20, 240); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(4)
    for k in range(7):
        y = 70 + k * 24; c.move_to(-4 - k * 2, y); c.line_to(22 - k * 3, y + 4); c.stroke()
    c.move_to(-10, -40); c.curve_to(40, -50, 60, 10, 40, 60); c.curve_to(20, 80, -20, 80, -30, 60); c.curve_to(-50, 10, -40, -30, -10, -40)
    c.close_path(); fill_stroke(c, (0.42, 0.47, 0.42), 6)
    ell(c, 6, 20, 14, 16); c.set_source_rgb(0.25, 0.28, 0.26); c.fill()
    c.restore()
    # sangle vers le casque
    c.set_source_rgb(*HELM_DD); c.set_line_width(10); c.move_to(198, 430); c.line_to(186, 486); c.stroke()


# ---------------------------------------------------------------- visage
def eyebrows(c, expr):
    for s in (-1, 1):
        x = 380 + s * 78
        lift = {'surprised': -26, 'happy': -8, 'think': (-16 if s > 0 else 4), 'doubt': (-18 if s < 0 else 6), 'wink': (0 if s < 0 else -6)}.get(expr, -4)
        ang = {'think': 0.1 * s, 'doubt': -0.12 * s}.get(expr, -0.08 * s)
        c.save(); c.translate(x, 318 + lift); c.rotate(ang)
        c.move_to(-42, 8); c.curve_to(-20, -10, 20, -12, 42, -2); c.curve_to(20, 2, -20, 4, -42, 16); c.close_path()
        c.set_source_rgb(*HAIR); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(3); c.stroke()
        c.restore()


def eyes(c, expr, blink, look):
    lx, ly = look
    for s in (-1, 1):
        x, y = 380 + s * 78, 382
        closed = blink
        if expr == 'wink' and s > 0: closed = 1.0
        if expr == 'happy': closed = max(closed, 0.0)
        ry = 40 * (1.12 if expr == 'surprised' else 1.0)
        if closed > 0.85 or (expr == 'happy'):
            # œil fermé / plissé (arc)
            c.set_source_rgb(*INK); c.set_line_width(8); c.set_line_cap(cairo.LINE_CAP_ROUND)
            if expr == 'happy' and closed < 0.85:
                c.move_to(x - 30, y + 8); c.curve_to(x - 14, y - 22, x + 14, y - 22, x + 30, y + 8)
            else:
                c.move_to(x - 30, y + 2); c.curve_to(x - 14, y + 14, x + 14, y + 14, x + 30, y + 2)
            c.stroke(); continue
        h = ry * (1 - closed)
        ell(c, x, y, 33, max(h, 3)); c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
        c.save(); ell(c, x, y, 33, max(h, 3)); c.clip()
        ix, iy = x + lx * 12, y + 4 + ly * 10
        ell(c, ix, iy, 21, 23); c.set_source_rgb(0.33, 0.22, 0.13); c.fill()
        ell(c, ix, iy, 11, 12); c.set_source_rgb(0.05, 0.04, 0.04); c.fill()
        ell(c, ix - 7, iy - 8, 6, 6); c.set_source_rgb(1, 1, 1); c.fill()
        # paupière haute
        c.set_source_rgba(*SKIN_D, 1); c.rectangle(x - 40, y - ry - 2, 80, 8 + ry * closed); c.fill()
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(6); c.move_to(x - 34, y - h * 0.35); c.curve_to(x - 20, y - h - 6, x + 20, y - h - 6, x + 34, y - h * 0.35); c.stroke()


def nose(c):
    c.set_source_rgba(*SKIN_DD, 0.9); c.set_line_width(6); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(372, 400); c.curve_to(366, 440, 360, 456, 372, 466); c.curve_to(384, 474, 398, 468, 402, 460); c.stroke()


def mouth_draw(c, expr, m):
    cx, cy = 380, 530
    if expr == 'surprised' and m < 0.2: m = 0.55
    if expr in ('think', 'doubt') and m < 0.15:
        c.set_source_rgb(*INK); c.set_line_width(7); c.set_line_cap(cairo.LINE_CAP_ROUND)
        if expr == 'think':
            c.move_to(cx - 34, cy + 6); c.curve_to(cx - 10, cy + 2, cx + 14, cy - 6, cx + 34, cy - 10)
        else:
            c.move_to(cx - 36, cy + 4); c.curve_to(cx - 10, cy - 8, cx + 10, cy - 8, cx + 36, cy + 4)
        c.stroke(); return
    if expr == 'surprised':
        w, h = 30 - 6 * m, 24 + 30 * m
        ell(c, cx, cy + 8, w, h); c.set_source_rgb(0.35, 0.08, 0.1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
        ell(c, cx, cy + 8 + h * 0.55, w * 0.6, h * 0.35); c.set_source_rgb(0.9, 0.42, 0.45); c.fill(); return
    wide = 72 if expr in ('happy', 'wink') else 62
    if m < 0.08:
        c.set_source_rgb(*INK); c.set_line_width(7); c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.move_to(cx - wide, cy - 6); c.curve_to(cx - 30, cy + 34, cx + 30, cy + 34, cx + wide, cy - 6); c.stroke()
        for s in (-1, 1):
            c.move_to(cx + s * (wide + 2), cy - 14); c.curve_to(cx + s * (wide + 8), cy - 6, cx + s * (wide + 6), cy + 2, cx + s * wide, cy - 4); c.stroke()
        return
    op = 22 + 64 * m
    c.move_to(cx - wide, cy - 8); c.curve_to(cx - 24, cy - 4, cx + 24, cy - 4, cx + wide, cy - 8)
    c.curve_to(cx + wide * 0.7, cy + op, cx - wide * 0.7, cy + op, cx - wide, cy - 8); c.close_path()
    c.set_source_rgb(0.33, 0.07, 0.1); c.fill_preserve()
    c.save(); c.clip()
    rr(c, cx - wide, cy - 30, wide * 2, 24 + 10 * (1 - m), 6); c.set_source_rgb(1, 1, 1); c.fill()
    ell(c, cx, cy + op * 0.92, wide * 0.55, op * 0.42); c.set_source_rgb(0.92, 0.45, 0.48); c.fill()
    c.restore()
    c.move_to(cx - wide, cy - 8); c.curve_to(cx - 24, cy - 4, cx + 24, cy - 4, cx + wide, cy - 8)
    c.curve_to(cx + wide * 0.7, cy + op, cx - wide * 0.7, cy + op, cx - wide, cy - 8); c.close_path()
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()


def hand_think(c):
    # poing sous le menton + avant-bras (pose « réflexion »)
    c.move_to(470, 900); c.curve_to(480, 800, 470, 720, 430, 668); c.line_to(372, 690); c.curve_to(400, 740, 410, 820, 400, 900); c.close_path()
    fill_stroke(c, SUIT, 6)
    c.save(); c.translate(408, 640); c.rotate(-0.15)
    rr(c, -46, -34, 96, 72, 30); fill_stroke(c, SKIN, 6)
    c.move_to(-40, -30); c.curve_to(-36, -62, -6, -70, 4, -46); c.curve_to(6, -36, 0, -30, -8, -30); c.close_path(); fill_stroke(c, SKIN, 5)
    c.set_source_rgb(*SKIN_DD); c.set_line_width(4); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for k in range(3):
        c.move_to(-10 + k * 20, 6); c.line_to(-10 + k * 20, 30); c.stroke()
    c.restore()


def thumbs_up(c):
    c.save(); c.translate(600, 640); c.rotate(0.15)
    rr(c, -46, 0, 92, 96, 26); fill_stroke(c, SKIN, 6)
    c.move_to(-30, 4); c.curve_to(-34, -50, -10, -80, 6, -76); c.curve_to(22, -72, 18, -40, 12, 4); c.close_path(); fill_stroke(c, SKIN, 6)
    c.set_source_rgb(*SKIN_DD); c.set_line_width(4)
    for k in range(3):
        c.move_to(-20, 30 + k * 22); c.line_to(30, 30 + k * 22); c.stroke()
    # manche
    rr(c, -54, 90, 108, 120, 20); fill_stroke(c, SUIT, 6)
    c.restore()


# ---------------------------------------------------------------- rendu + contour sticker
_cache = {}


def _render_base(expr, mouth, blink, look, pose):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, BASE_W, BASE_H)
    c = cairo.Context(s); c.set_line_join(cairo.LINE_JOIN_ROUND)
    body(c)
    oxygen_mask(c)
    head_base(c)
    helmet(c)
    eyebrows(c, expr); eyes(c, expr, blink, look); nose(c); mouth_draw(c, expr, mouth)
    if pose == 'think': hand_think(c)
    if pose == 'thumb': thumbs_up(c)
    s.flush()
    a = np.ndarray((BASE_H, BASE_W, 4), np.uint8, s.get_data()).copy()
    # contour blanc (dilatation de l'alpha) + ombre portée douce
    al = Image.fromarray(a[:, :, 3])
    border = np.array(al.filter(ImageFilter.MaxFilter(27)).filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32) / 255
    shadow = np.array(al.filter(ImageFilter.MaxFilter(27)).filter(ImageFilter.GaussianBlur(14))).astype(np.float32) / 255
    out = np.zeros((BASE_H + 40, BASE_W + 40, 4), np.float32)
    sh = np.roll(np.roll(np.pad(shadow, 20), 10, 0), 6, 1)
    out[:, :, 3] = sh * 0.35
    b = np.pad(border, 20)
    # blanc par-dessus l'ombre
    out[:, :, :3] = out[:, :, :3] * (1 - b[..., None]) + b[..., None] * 1.0
    out[:, :, 3] = out[:, :, 3] * (1 - b) + b
    src = np.pad(a.astype(np.float32) / 255, ((20, 20), (20, 20), (0, 0)))
    sa = src[:, :, 3:4]
    # cairo stocke en BGRA prémultiplié ; out est en BGRA prémultiplié aussi (blanc = 1,1,1)
    out[:, :, :3] = src[:, :, :3] + out[:, :, :3] * (1 - sa)
    out[:, :, 3] = src[:, :, 3] + out[:, :, 3] * (1 - sa[:, :, 0])
    out8 = np.ascontiguousarray((np.clip(out, 0, 1) * 255).astype(np.uint8))
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, BASE_W + 40, BASE_H + 40)
    np.ndarray((BASE_H + 40, BASE_W + 40, 4), np.uint8, surf.get_data())[:] = out8
    surf.mark_dirty()
    return surf


def get(expr='smile', mouth=0.0, blink=0.0, look=(0.0, 0.0), pose=None):
    key = (expr, round(mouth * 4) / 4, round(blink * 3) / 3, (round(look[0], 1), round(look[1], 1)), pose)
    if key not in _cache: _cache[key] = _render_base(*key)
    return _cache[key]


def draw(c, cx, cy, h, expr='smile', mouth=0.0, blink=0.0, look=(0.0, 0.0), pose=None, tilt=0.0, alpha=1.0):
    s = get(expr, mouth, blink, look, pose)
    k = h / (BASE_H + 40)
    c.save(); c.translate(cx, cy); c.rotate(tilt); c.scale(k, k)
    c.set_source_surface(s, -(BASE_W + 40) / 2, -(BASE_H + 40)); c.paint_with_alpha(alpha)
    c.restore()


def mouth_track(voice_wav, fps=30):
    """Ouverture de bouche par image à partir de l'enveloppe RMS de la voix."""
    import soundfile as sf
    a, sr = sf.read(voice_wav)
    if a.ndim > 1: a = a.mean(1)
    hop = int(sr / fps); n = len(a) // hop
    rms = np.array([np.sqrt(np.mean(a[i * hop:(i + 1) * hop] ** 2)) for i in range(n)])
    ref = np.percentile(rms[rms > 1e-4], 90) if (rms > 1e-4).any() else 1
    m = np.clip((rms / ref - 0.12) * 1.3, 0, 1)
    return m
