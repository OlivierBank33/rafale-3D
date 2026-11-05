"""05/11 : GRANDS CRASHS ép. 04 « Helios 522, l'avion fantôme » (14/08/2005) en style cinéma (hl_*).
Boeing 737-300 FlightGear (pr/r_hl_*, dérive bleu nuit sans logo), carte topo pr/map_egee.png (jk_maps 'egee').
Signatures : avion « fantôme » qui clignote en radiographie, sélecteur de pressurisation bloqué sur MAN (macro), double carte « ce que dit
l'alarme / ce que croit l'équipage », hippodrome d'attente au-dessus de Kéa, vue du chasseur (sièges vides, masques pendants), jauges carburant et N1 qui tombent."""
import cairo, math, random
from sm_lib import *
from sm_scenes2 import ease, ap, ORG, BLUE, RED, WH, GRN
from sm_scenes6 import si, stamp, eout, YEL
from sm_scenes7 import tag, label, check, cross
import sm_scenes10 as P10
from sm_scenes10 import plane, glow, letter, panel, counter
from sm_scenes11 import cabin_masks
from sm_scenes12 import sky_paint, plane_icon
from sm_scenes13 import route, curve_pts, mixc, CY
from sm_scenes14 import sea, clouds
import pr.jk_maps as JM
R = None
NAVY = (0.08, 0.16, 0.42)


def map_egee(c, sc=1.0, cx=540, cy=900, fx=540, fy=900):
    s, _ = P10.plate('map_egee.png')
    c.save(); c.translate(cx, cy); c.scale(sc, sc); c.translate(-fx, -fy); c.set_source_surface(s, 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint(); c.restore()
    M0 = JM.MAP['egee']
    return lambda lo, la: ((M0(lo, la)[0] - fx) * sc + cx, (M0(lo, la)[1] - fy) * sc + cy)


def ghost(c, name, x, y, sc, t, a=1.0, rot=0.0):
    """l'avion « fantôme » : rendu normal qui laisse passer par instants sa radiographie."""
    fl = 0.5 + 0.5 * math.sin(t * 3.1) * math.sin(t * 1.7 + 1)
    plane(c, name, x, y, sc, rot=rot, alpha=a * (0.85 - 0.35 * fl))
    c.push_group(); plane(c, name, x, y, sc, rot=rot, xray=True); c.pop_group_to_source(); c.paint_with_alpha(a * (0.15 + 0.6 * fl))


def selector(c, x, y, r, pos, t, a=1.0, hot=1.0):
    """sélecteur de mode de pressurisation (panneau plafond) : AUTO / ALTN / MAN ; pos en degrés (-50 AUTO, 0 ALTN, +50 MAN)."""
    rr(c, x - r * 2.1, y - r * 2.45, r * 4.2, r * 4.15, r * 0.2); c.set_source_rgba(0.16, 0.17, 0.18, a); c.fill()
    for j in range(40):                                                         # grain du panneau
        rnd = random.Random(j); c.new_path(); c.arc(x + rnd.uniform(-2, 2) * r, y + rnd.uniform(-1.9, 1.6) * r, 1.5, 0, 7); c.set_source_rgba(1, 1, 1, 0.04 * a); c.fill()
    letter(c, "PRESSURISATION", x, y - r * 2.05, r * 0.26, (0.85, 0.85, 0.8), a, 'Montserrat')
    for lab, ang in (("AUTO", -50), ("ALTN", 0), ("MAN", 50)):
        an = math.radians(ang - 90)
        col = RED if lab == "MAN" and hot > 0 else (0.9, 0.9, 0.85)
        letter(c, lab, x + math.cos(an) * r * 1.45, y + math.sin(an) * r * 1.45 + r * 0.12, r * 0.36, col, a)
        c.move_to(x + math.cos(an) * r * 1.02, y + math.sin(an) * r * 1.02); c.line_to(x + math.cos(an) * r * 1.18, y + math.sin(an) * r * 1.18)
        c.set_source_rgba(0.9, 0.9, 0.85, a); c.set_line_width(r * 0.06); c.stroke()
    g = cairo.RadialGradient(x - r * 0.3, y - r * 0.3, r * 0.1, x, y, r)
    g.add_color_stop_rgb(0, 0.30, 0.30, 0.32); g.add_color_stop_rgb(1, 0.05, 0.05, 0.06)
    c.new_path(); c.arc(x, y, r, 0, 7); c.set_source(g); c.fill()
    an = math.radians(pos - 90)
    c.save(); c.translate(x, y); c.rotate(an + math.pi / 2)
    rr(c, -r * 0.22, -r * 0.95, r * 0.44, r * 1.9, r * 0.2); c.set_source_rgba(0.12, 0.12, 0.13, a); c.fill()
    c.move_to(0, -r * 0.9); c.line_to(0, -r * 0.35); c.set_source_rgba(1, 1, 1, a); c.set_line_width(r * 0.1); c.set_line_cap(1); c.stroke()
    c.restore()
    if hot > 0:
        ph = (t * 1.2) % 1
        c.new_path(); c.arc(x, y, r * (1.25 + 0.6 * ph), 0, 7); c.set_source_rgba(*RED, hot * (1 - ph) * 0.8); c.set_line_width(5); c.stroke()


def dial(c, x, y, r, v, lab, unit, t, col=YEL, a=1.0, warn=None):
    """cadran rond 0..1 (aiguille), libellé."""
    c.new_path(); c.arc(x, y, r, 0, 7); c.set_source_rgba(0.03, 0.04, 0.06, 0.85 * a); c.fill_preserve(); c.set_source_rgba(0.7, 0.75, 0.8, 0.8 * a); c.set_line_width(4); c.stroke()
    for m in range(11):
        an = math.radians(135 + 27 * m)
        c.move_to(x + r * 0.78 * math.cos(an), y + r * 0.78 * math.sin(an)); c.line_to(x + r * 0.9 * math.cos(an), y + r * 0.9 * math.sin(an))
        c.set_source_rgba(0.85, 0.85, 0.85, a); c.set_line_width(3); c.stroke()
    if warn is not None:
        c.new_path(); c.arc(x, y, r * 0.84, math.radians(135 + 270 * warn), math.radians(405)); c.set_source_rgba(*RED, 0.8 * a); c.set_line_width(8); c.stroke()
    an = math.radians(135 + 270 * max(0, min(1, v)))
    c.move_to(x, y); c.line_to(x + r * 0.75 * math.cos(an), y + r * 0.75 * math.sin(an)); c.set_source_rgba(*col, a); c.set_line_width(7); c.set_line_cap(1); c.stroke()
    c.new_path(); c.arc(x, y, r * 0.08, 0, 7); c.set_source_rgba(0.9, 0.9, 0.9, a); c.fill()
    letter(c, lab, x, y + r * 0.45, r * 0.22, WH, a)
    letter(c, unit, x, y + r * 1.32, r * 0.2, (0.8, 0.85, 0.9), a, 'Montserrat')


def f16_top(c, x, y, s, ang, a=1.0, col=(0.20, 0.22, 0.26)):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.new_path(); c.move_to(80, 0); c.line_to(40, -6); c.line_to(10, -8); c.line_to(-10, -48); c.line_to(-26, -48); c.line_to(-22, -10); c.line_to(-55, -10)
    c.line_to(-70, -30); c.line_to(-80, -30); c.line_to(-76, -6); c.line_to(-80, 0)
    c.line_to(-76, 6); c.line_to(-80, 30); c.line_to(-70, 30); c.line_to(-55, 10); c.line_to(-22, 10); c.line_to(-26, 48); c.line_to(-10, 48); c.line_to(10, 8); c.line_to(40, 6); c.close_path()
    c.set_source_rgba(*col, a); c.fill_preserve(); c.set_source_rgba(0.8, 0.85, 0.9, 0.6 * a); c.set_line_width(1.5 / s); c.stroke()
    c.restore()


def cockpit_view(c, t, slump=1.0, empty_left=1.0, intruder=0.0, masks=0.0, a=1.0):
    """vue du chasseur à travers la vitre latérale du poste (2D) : sièges, copilote affalé, siège gauche vide, masques en cabine."""
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, 0.30, 0.50, 0.80); g.add_color_stop_rgb(1, 0.75, 0.84, 0.95); c.set_source(g); c.paint()
    # flanc de l'avion (blanc) + fenêtres du poste
    c.new_path(); c.move_to(-50, 420); c.curve_to(300, 330, 700, 320, 1130, 330); c.line_to(1130, 1350); c.curve_to(700, 1360, 300, 1360, -50, 1300); c.close_path()
    c.set_source_rgb(0.93, 0.94, 0.96); c.fill()
    wins = [(90, 560, 300, 330), (430, 545, 300, 340)]
    for j, (wx, wy, ww, wh) in enumerate(wins):
        c.save(); rr(c, wx, wy, ww, wh, 40); c.clip()
        c.set_source_rgb(0.10, 0.12, 0.15); c.paint()
        # siège
        cx_ = wx + ww / 2
        rr(c, cx_ - 70, wy + 80, 140, 260, 30); c.set_source_rgb(0.16, 0.17, 0.20); c.fill()
        if j == 0:
            if empty_left > 0 and intruder <= 0:
                c.set_dash([10, 8]); rr(c, cx_ - 50, wy + 40, 100, 120, 40); c.set_source_rgba(1, 1, 1, 0.5 * empty_left); c.set_line_width(3); c.stroke(); c.set_dash([])
            if intruder > 0:
                xx = cx_ - 160 * (1 - intruder)
                c.new_path(); c.arc(xx, wy + 95, 34, 0, 7); c.set_source_rgb(0.03, 0.03, 0.04); c.fill()
                rr(c, xx - 55, wy + 130, 110, 200, 40); c.fill()
        else:
            hx = cx_ + 30 * slump; hy = wy + 110 + 60 * slump
            c.new_path(); c.arc(hx, hy, 34, 0, 7); c.set_source_rgb(0.03, 0.03, 0.04); c.fill()
            c.save(); c.translate(cx_, wy + 160); c.rotate(0.5 * slump); rr(c, -55, 0, 110, 190, 40); c.restore(); c.fill()
        c.restore()
        rr(c, wx, wy, ww, wh, 40); c.set_source_rgb(0.25, 0.27, 0.30); c.set_line_width(10); c.stroke()
        glow(c, wx + ww * 0.3, wy + wh * 0.2, ww * 0.5, (1, 1, 1), 0.10)
    # hublots cabine avec masques jaunes qui pendent
    for j in range(4):
        hx = 765 + j * 62; hy = 640
        rr(c, hx, hy, 50, 70, 22); c.set_source_rgb(0.12, 0.14, 0.18); c.fill()
        if masks > 0:
            sw = math.sin(t * 2 + j) * 6
            c.move_to(hx + 25, hy + 8); c.line_to(hx + 25 + sw, hy + 40); c.set_source_rgba(1, 1, 1, 0.8 * masks); c.set_line_width(2); c.stroke()
            c.new_path(); c.arc(hx + 25 + sw, hy + 48, 9, 0, 7); c.set_source_rgba(1.0, 0.82, 0.1, masks); c.fill()
    # vignette ronde « jumelles »
    g = cairo.RadialGradient(540, 760, 380, 540, 760, 900); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.85)
    c.set_source(g); c.paint()


def vision_tunnel(c, k):
    if k <= 0: return
    g = cairo.RadialGradient(540, 820, 700 * (1 - k) + 60, 540, 820, 900 * (1 - k) + 300)
    g.add_color_stop_rgba(0, 0, 0, 0.02, 0); g.add_color_stop_rgba(1, 0, 0, 0.02, min(1, 0.4 + k))
    c.set_source(g); c.paint()


# =============================================================== scènes
def sc_hl_hook(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        sea(c, t, 'dawn', 1050, (760, 1040))
        ghost(c, 'hl_hero', 560 - 60 * p, 700, 0.40, t)
        tag(c, "AU-DESSUS DE LA GRÈCE", 540, 1285, WH, ap(p, 0.3, 0.45), 52)
    elif k == 1:
        sea(c, t, 'dawn', 1050, (760, 1040))
        c.set_source_rgba(0, 0, 0, 0.45); c.paint()
        ghost(c, 'hl_hero', 520, 960, 0.26, t, 0.6)
        panel(c, 120, 340, 840, 360, 0.75)
        b = sg['sent'][1]
        for j in range(3):
            a = ap(t, b[0] + j * 0.35, b[0] + j * 0.35 + 0.2)
            letter(c, "« HELIOS 522, VOUS M'ENTENDEZ ? »", 540, 420 + j * 70, 40, YEL, a * (1 - 0.3 * j), 'Montserrat')
        c.move_to(170, 640); c.line_to(910, 640); c.set_source_rgba(0.4, 1, 0.5, 0.8); c.set_line_width(3); c.stroke()
        letter(c, "AUCUNE RÉPONSE", 540, 690, 48, RED, ap(p, 0.4, 0.6))
    else:
        sea(c, t, 'dawn', 1050, (760, 1040))
        c.set_source_rgba(0, 0, 0, 0.35); c.paint()
        ghost(c, 'hl_hero', 540, 820, 0.36, t * 1.5)
        stamp(c, "HELIOS 522", 540, 520, 150, CY, since, glow=1.0)


def sc_hl_switch(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        M = map_egee(c)
        lca, ath = M(33.63, 34.88), M(23.73, 37.98)
        xy = curve_pts(lca, ath, -0.08)
        hx, hy = route(c, xy, ap(p, 0.15, 0.95))
        if p > 0.15:
            i = max(1, int(len(xy) * ap(p, 0.15, 0.95)) - 1); plane_icon(c, hx, hy, math.atan2(xy[i][1] - xy[i - 1][1], xy[i][0] - xy[i - 1][0]), 1.5)
        for nm, (x, y), anc, dx in (("LARNACA (CHYPRE)", lca, 'r', -20), ("ATHÈNES", ath, 'l', 20)):
            c.new_path(); c.arc(x, y, 10, 0, 7); c.set_source_rgb(1, 1, 1); c.fill()
            letter(c, nm, x + dx, y + 55, 38, WH, 1.0, anchor=anc)
        panel(c, 260, 380, 560, 150, 0.55)
        letter(c, "14 AOÛT 2005", 540, 485, 96, YEL, ap(p, 0.0, 0.12))
        tag(c, "HELIOS 522 · BOEING 737 · 121 À BORD", 540, 1285, WH, ap(p, 0.35, 0.5), 44)
    else:
        c.set_source_rgb(0.04, 0.04, 0.05); c.paint()
        b = sg['sent'][1]
        pos = -50 + 100 * ap(t, b[0] + 0.2, b[0] + 1.0)                                # le bouton passe sur MAN… et y reste
        selector(c, 540, 820, 150, pos, t, 1.0, ap(t, b[0] + 1.0, b[0] + 1.3))
        letter(c, "APRÈS UNE MAINTENANCE", 540, 390, 56, WH, ap(p, 0.0, 0.2), 'Montserrat')
        tag(c, "RESTÉ SUR « MANUEL »", 540, 1285, RED, ap(p, 0.55, 0.7), 56)


def sc_hl_alarm(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        P10.sky_bg(c, t, oy=300)
        q = ap(t, sg['sent'][0][0], sg['sent'][0][1] + 0.3)
        plane(c, 'hl_side', 520, 900 - 120 * q, 0.34, rot=-0.10)
        r = random.Random(4)
        for j in range(140):                                                     # molécules d'oxygène qui se raréfient
            if r.random() < q * 0.85: continue
            x = (r.random() * W + t * 40) % W; y = r.random() * 1300 + 100
            c.new_path(); c.arc(x, y, 5, 0, 7); c.set_source_rgba(0.6, 0.85, 1, 0.55); c.fill()
        alt = int(10000 + 24000 * q)
        panel(c, 300, 1100, 480, 180, 0.6)
        counter(c, f"{alt:,} FT".replace(',', ' '), "L'AIR SE RARÉFIE", 540, 1200, YEL, 100)
    else:
        c.set_source_rgb(0.03, 0.03, 0.05); c.paint()
        b = sg['sent'][1]; q = ap(t, b[0], b[1])
        c.new_path()                                                              # klaxon d'alarme (forme d'onde)
        for i in range(0, 861, 3):
            v = 60 * math.sin(i * 0.25 + t * 30) * (1 if (t * 3) % 1 < 0.6 else 0.15)
            (c.move_to if i == 0 else c.line_to)(110 + i, 420 + v)
        c.set_source_rgba(*RED, 0.9); c.set_line_width(4); c.stroke()
        rr(c, 110, 560, 860, 230, 26); c.set_source_rgba(*RED, 0.18); c.fill_preserve(); c.set_source_rgba(*RED, 1); c.set_line_width(4); c.stroke()
        letter(c, "CE QUE DIT L'ALARME", 540, 630, 40, (1, 0.7, 0.7), 1.0, 'Montserrat')
        letter(c, "ALTITUDE CABINE", 540, 730, 84, RED, 1.0)
        a = ap(q, 0.3, 0.45)
        rr(c, 110, 860, 860, 230, 26); c.set_source_rgba(1, 1, 1, 0.08 * a); c.fill_preserve(); c.set_source_rgba(0.8, 0.8, 0.8, a); c.set_line_width(4); c.stroke()
        letter(c, "CE QUE CROIT L'ÉQUIPAGE", 540, 930, 40, WH, a, 'Montserrat')
        letter(c, "CONFIGURATION DÉCOLLAGE ?", 540, 1030, 70, WH, a)
        if q > 0.55: cross(c, 900, 1010, 0.9, RED, ap(q, 0.55, 0.65))


def sc_hl_hypoxia(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        cabin_masks(c, t, ap(p, 0.0, 0.7))
        tag(c, "LES MASQUES TOMBENT", 540, 1285, YEL, ap(p, 0.2, 0.35), 54)
    elif k == 1:
        c.set_source_rgb(0.05, 0.07, 0.12); c.paint()
        for j, x in enumerate((360, 720)):                                       # deux pilotes (pictogrammes) qui s'affaissent
            sl = ap(p, 0.25 + 0.15 * j, 0.7 + 0.15 * j)
            c.save(); c.translate(x, 900); c.rotate((0.35 if j else -0.35) * sl)
            rr(c, -80, -40, 160, 260, 60); c.set_source_rgb(0.20, 0.26, 0.40); c.fill()
            c.new_path(); c.arc(0, -110 + 30 * sl, 60, 0, 7); c.set_source_rgb(0.85, 0.75, 0.65); c.fill()
            c.restore()
        vision_tunnel(c, ap(p, 0.1, 0.9))
        stamp(c, "HYPOXIE", 540, 520, 140, CY, since - 0.4, glow=1.0)
    else:
        M = map_egee(c, 7.0, 540, 840, *JM.MAP['egee'](24.0, 37.8))
        kea, ath = M(24.32, 37.62), M(23.73, 37.98)
        b = sg['sent'][2]; q = ap(t, b[0], b[1] + 0.3)
        c.new_path(); c.arc(*ath, 12, 0, 7); c.set_source_rgb(1, 1, 1); c.fill(); letter(c, "ATHÈNES", ath[0] + 20, ath[1] - 20, 40, WH, 1.0, anchor='l')
        # hippodrome d'attente autour de Kéa
        L, Rr = 160, 90
        def race(u_):
            per = 2 * L + 2 * math.pi * Rr; d = (u_ % 1) * per
            if d < L: return kea[0] - L / 2 + d, kea[1] - Rr, 0.0
            d -= L
            if d < math.pi * Rr: an = -math.pi / 2 + d / Rr; return kea[0] + L / 2 + Rr * math.cos(an), kea[1] + Rr * math.sin(an), an + math.pi / 2
            d -= math.pi * Rr
            if d < L: return kea[0] + L / 2 - d, kea[1] + Rr, math.pi
            d -= L; an = math.pi / 2 + d / Rr; return kea[0] - L / 2 + Rr * math.cos(an), kea[1] + Rr * math.sin(an), an + math.pi / 2
        n = 160; turns = 1.6 * q
        c.new_path()
        for i in range(n + 1):
            x, y, _ = race(turns * i / n); (c.move_to if i == 0 else c.line_to)(x, y)
        c.set_source_rgba(*YEL, 0.85); c.set_line_width(5); c.set_dash([12, 8]); c.stroke(); c.set_dash([])
        x, y, an = race(turns); plane_icon(c, x, y, an, 1.6, (1, 1, 1), 1.0); glow(c, x, y, 40, YEL, 0.6)
        letter(c, "KÉA", kea[0], kea[1] + 15, 40, (0.6, 0.72, 0.85), 0.9)
        panel(c, 300, 380, 480, 170, 0.6)
        counter(c, "70 MIN", "EN ATTENTE, EN PILOTE AUTOMATIQUE", 540, 480, YEL, 100, ap(q, 0.1, 0.3))


def sc_hl_f16(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        P10.sky_bg(c, t, oy=380)
        clouds(c, t, 0.6, 1050, 1400, (1, 1, 1), 160, seed=5)
        plane(c, 'hl_bank', 560, 760, 0.30)
        q = ap(p, 0.0, 1.0)
        for j in range(2):
            x = -150 + 820 * q + j * 120; y = 1000 - 180 * q + j * 90
            f16_top(c, x, y, 1.6, -0.3, 1.0)
        tag(c, "2 F-16 GRECS EN INTERCEPTION", 540, 1285, WH, ap(p, 0.2, 0.35), 48)
    else:
        b = sg['sent'][1]; L = b[1] - b[0]
        cockpit_view(c, t, slump=1.0, masks=ap(t, b[0] + 0.66 * L, b[0] + 0.72 * L))
        for j, (txt, x, y, col) in enumerate((("COPILOTE EFFONDRÉ", 580, 1000, RED), ("SIÈGE VIDE", 240, 1000, WH), ("MASQUES QUI PENDENT", 870, 820, YEL))):
            tag(c, txt, x, y, col, ap(t, b[0] + j * 0.3 * L + 0.2, b[0] + j * 0.3 * L + 0.4), 38)


def sc_hl_steward(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        b = sg['sent'][0]
        cockpit_view(c, t, slump=1.0, intruder=ap(t, b[0] + 0.3, b[0] + 1.6), masks=1.0)
        tag(c, "UN STEWARD, LICENCE DE PILOTE", 540, 1285, GRN, ap(p, 0.5, 0.65), 46)
    else:
        P10.sky_bg(c, t, oy=380)
        plane(c, 'hl_bank', 540, 780, 0.32, rot=0.08 * math.sin(t * 0.8))
        stamp(c, "IL TENTE DE REPRENDRE L'AVION", 540, 1285, 70, GRN, since, glow=1.0)


def hills(c, t, y0=1150, col=(0.10, 0.09, 0.08)):
    r = random.Random(9)
    for layer, (yy, cc) in enumerate(((y0 - 120, (0.30, 0.26, 0.24)), (y0 - 40, (0.18, 0.15, 0.13)), (y0 + 40, col))):
        c.new_path(); c.move_to(-20, H)
        for i in range(0, W + 61, 60): c.line_to(i, yy - 60 * math.sin(i / 180.0 + layer * 2) - r.uniform(0, 40))
        c.line_to(W + 20, H); c.close_path(); c.set_source_rgb(*cc); c.fill()


def sc_hl_crash(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    if k == 0:
        c.set_source_rgb(0.03, 0.03, 0.05); c.paint()
        for j, x in enumerate((330, 750)):
            dial(c, x, 820, 170, 0.35 * (1 - ap(p, 0.0, 0.8)), "CARBURANT", "RÉSERVOIR " + ("GAUCHE" if j == 0 else "DROIT"), t, RED, 1.0, warn=0.12)
        stamp(c, "RÉSERVOIRS VIDES", 540, 1285, 96, RED, since - 0.3, glow=1.0)
    elif k == 1:
        c.set_source_rgb(0.03, 0.03, 0.05); c.paint()
        b = sg['sent'][1]; L = b[1] - b[0]
        nL = 0.85 * (1 - ap(t, b[0] + 0.1, b[0] + 0.45 * L)); nR = 0.85 * (1 - ap(t, b[0] + 0.55 * L, b[1]))
        dial(c, 330, 820, 170, nL, "N1 GAUCHE", "11:49", t, YEL if nL > 0.1 else RED)
        dial(c, 750, 820, 170, nR, "N1 DROIT", "11:59", t, YEL if nR > 0.1 else RED)
        letter(c, "10 MINUTES D'ÉCART", 540, 470, 70, WH, ap(p, 0.4, 0.6))
    elif k == 2:
        g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, 0.35, 0.45, 0.62); g.add_color_stop_rgb(1, 0.85, 0.75, 0.62); c.set_source(g); c.paint()
        b = sg['sent'][2]; q = ap(t, b[0] - 0.2, b[1] + 0.2)
        hills(c, t)
        plane(c, 'hl_bank', 700 - 340 * q, 500 + 440 * q, 0.30 - 0.06 * q, rot=-0.15 - 0.2 * q, alpha=1 - ap(q, 0.85, 1.0))
        c.set_source_rgba(0, 0, 0, 0.6 * ap(q, 0.8, 1.0)); c.paint()
        tag(c, "PRÈS DE GRAMMATIKO, À 40 KM D'ATHÈNES", 540, 1285, WH, ap(q, 0.1, 0.25), 42)
    else:
        c.set_source_rgb(0.01, 0.012, 0.02); c.paint()
        b = sg['sent'][3]
        for j in range(121):                                                     # 121 lumières
            row, col = j // 11, j % 11
            x = 140 + col * 80; y = 420 + row * 62
            a = ap(t, b[0] + j * 0.008, b[0] + j * 0.008 + 0.35); fl = 0.85 + 0.15 * math.sin(t * 7 + j)
            glow(c, x, y, 24, (1.0, 0.75, 0.4), 0.45 * a * fl)
            c.new_path(); c.arc(x, y, 5, 0, 7); c.set_source_rgba(1, 0.95, 0.8, a); c.fill()
        letter(c, "121 VICTIMES", 540, 1210, 110, WH, ap(since, 0.0, 0.3))


def sc_hl_after(c, t, sg, lt, u):
    k, p, since = si(sg, t)
    c.set_source_rgb(0.04, 0.04, 0.05); c.paint()
    if k == 0:
        b = sg['sent'][0]
        pos = 50 - 100 * ap(t, b[0] + 0.6, b[0] + 1.2)                             # ce qu'il aurait fallu : AUTO
        selector(c, 540, 820, 150, pos, t, 1.0, 1 - ap(t, b[0] + 0.6, b[0] + 0.9))
        letter(c, "UN SEUL BOUTON", 540, 400, 90, YEL, ap(p, 0.0, 0.2))
    else:
        selector(c, 540, 960, 110, 50, t, 0.4, 0.6)
        stamp(c, "ET TOI ?", 540, 560, 160, ORG, since, glow=1.0)
        letter(c, "TU AURAIS COMPRIS L'ALARME ?", 540, 680, 46, WH, ap(since, 0.3, 0.6), 'Montserrat')


SC15 = {k[3:]: v for k, v in globals().items() if k.startswith('sc_') and callable(v)}
