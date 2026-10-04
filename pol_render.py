"""« L'avion pollue-t-il vraiment plus que le reste ? » — scènes de comparaison chiffrée. Réutilise les outils de dl_render.
Usage : python3 pol_render.py [stills t ...]"""
import os, sys, math, subprocess, cairo
os.environ['DL'] = 'pol'
sys.argv_saved = sys.argv; sys.argv = [sys.argv[0]]
import dl_render as R
sys.argv = sys.argv_saved
from dl_render import (W, H, FPS, ease, ease_out, back_out, text_c, pill, rrect, background, font, YEL, GREY, INK)

BLUE = (0.25, 0.62, 1.0); RED = (1.0, 0.33, 0.25); GRN = (0.35, 0.95, 0.55); ORG = (1.0, 0.62, 0.2)
IMG = {k: cairo.ImageSurface.create_from_png(f'r3d/{k}.png') for k in ('a320', 'b787', 'a330', 'concorde')}


def plane(c, key, cx, cy, size, alpha=1.0, flip=False):
    sf = IMG[key]; sw = sf.get_width(); s = size / sw
    c.save(); c.translate(cx, cy)
    if flip: c.scale(-1, 1)
    c.scale(s, s); c.set_source_surface(sf, -sw / 2, -sf.get_height() / 2); c.paint_with_alpha(alpha); c.restore()


def U(t, s): return (t - s['vt']) / s['dur']


def title(c, t, s, txt, sub=None, y=330):
    a = ease((t - s['t0']) / 0.3)
    text_c(c, txt, W / 2, y, 64, (1, 1, 1, a), stroke=10, maxw=980)
    if sub: text_c(c, sub, W / 2, y + 60, 32, (0.8, 0.85, 0.95, a), maxw=980, bold=False)


def hbar(c, y, label, val, vmax, col, a, txt, hi=False, x0=330, wmax=540):
    if a <= 0.01: return
    font(c, 40); e = c.text_extents(label)
    c.set_source_rgba(1, 1, 1, a); c.move_to(x0 - 24 - e.x_advance, y + 30); c.show_text(label)
    w = max(10, wmax * val / vmax)
    rrect(c, x0, y, w, 44, 12); c.set_source_rgba(*col, a); c.fill()
    if hi:
        c.set_line_width(5); rrect(c, x0 - 6, y - 6, w + 12, 56, 16); c.set_source_rgba(*YEL, a); c.stroke()
    text_c(c, txt, x0 + w + 80, y + 32, 40, (1, 1, 1, a), stroke=6)


def sc_hook(c, t, s):
    lt = t - s['t0']
    background(c, t, tint=[(RED, 540, 900, 600, 0.35)], streak=1.0)
    plane(c, 'a320', W / 2 + 40 * math.sin(t), 900, 900 * (1 + 0.05 * ease(lt / 3)), alpha=ease(lt / 0.4))
    a = ease((lt - 0.2) / 0.3)
    text_c(c, "L'AVION,", W / 2, 470, 96, (1, 1, 1, a), stroke=12)
    text_c(c, "ENNEMI N°1", W / 2, 1300, 110, (*RED, ease((lt - 0.6) / 0.3)), stroke=12)
    text_c(c, "DU CLIMAT ?", W / 2, 1420, 110, (*RED, ease((lt - 0.8) / 0.3)), stroke=12)


SECT = [("Route", 11.9, (0.6, 0.6, 0.65)), ("Acier", 7.2, (0.6, 0.6, 0.65)), ("Élevage", 5.8, (0.6, 0.6, 0.65)),
        ("Ciment", 3.0, (0.6, 0.6, 0.65)), ("Aviation", 1.9, BLUE), ("Maritime", 1.7, (0.6, 0.6, 0.65))]


def sc_sectors(c, t, s):
    u = U(t, s)
    background(c, t, tint=[(BLUE, 540, 1150, 500, 0.25 * ease((u - 0.6) / 0.1))])
    title(c, t, s, "PART DES ÉMISSIONS MONDIALES", "gaz à effet de serre par secteur · Our World in Data (2016)")
    starts = [0.18, 0.30, 0.40, 0.50, 0.62, 0.82]
    for k, ((lab, v, col), st) in enumerate(zip(SECT, starts)):
        g = ease_out((u - st) / 0.08)
        hbar(c, 540 + k * 150, lab, v * g, 12, col, ease((u - st) / 0.05), f"{v * g:.1f} %".replace('.', ','), hi=(lab == "Aviation" and u > 0.7))
    if u > 0.72:
        pill(c, "MOINS QUE LE CIMENT", W / 2, 1470, 44, YEL, fg=INK, s=back_out((u - 0.72) / 0.08))


def sc_digital(c, t, s):
    u = U(t, s)
    background(c, t, tint=[(ORG, 540, 900, 500, 0.25)])
    title(c, t, s, "ET LE NUMÉRIQUE ?", "data centers, réseaux, écrans · estimations 2020-2024")
    a = ease((t - s['t0']) / 0.3)
    hbar(c, 700, "Aviation", 1.9, 4.5, BLUE, a, "1,9 %")
    g = ease_out((u - 0.15) / 0.2)
    x0, wmax = 330, 540
    font(c, 40); e = c.text_extents("Numérique"); c.set_source_rgba(1, 1, 1, a); c.move_to(x0 - 24 - e.x_advance, 900 + 30); c.show_text("Numérique")
    w2 = wmax * 2 / 4.5 * g; w4 = wmax * 4 / 4.5 * g
    rrect(c, x0, 900, max(10, w4), 44, 12); c.set_source_rgba(*ORG, 0.35 * a); c.fill()
    rrect(c, x0, 900, max(10, w2), 44, 12); c.set_source_rgba(*ORG, a); c.fill()
    if g > 0.5: text_c(c, "2 à 4 %", x0 + w4 + 90, 932, 40, (1, 1, 1, a), stroke=6)
    if u > 0.55: pill(c, "AUTANT, VOIRE PLUS", W / 2, 1150, 44, YEL, fg=INK, s=back_out((u - 0.55) / 0.08))


def sc_eff(c, t, s):
    u = U(t, s)
    background(c, t, tint=[(GRN, 540, 900, 520, 0.25)])
    title(c, t, s, "CO2 PAR PASSAGER ET PAR KM", "moyenne mondiale · Our World in Data")
    a = ease((t - s['t0']) / 0.3)
    plane(c, 'b787', W / 2, 640, 640, alpha=a)
    v = 357 - (357 - 157) * ease((u - 0.3) / 0.35)
    yr = int(1990 + 29 * ease((u - 0.3) / 0.35))
    text_c(c, f"{yr}", W / 2, 920, 60, (*YEL, a), stroke=8)
    text_c(c, f"{v:.0f} g", W / 2, 1090, 170, (1, 1, 1, a), stroke=14)
    if u > 0.68:
        pill(c, "÷ 2 DEPUIS 1990", W / 2, 1260, 50, GRN, fg=INK, s=back_out((u - 0.68) / 0.08))


TRIP = [("Voiture seul", 200, RED, 0.18), ("Avion", 155, BLUE, 0.36), ("TGV", 2.7, GRN, 0.64)]


def sc_trip(c, t, s):
    u = U(t, s)
    background(c, t)
    title(c, t, s, "PARIS – NICE", "kg CO2e par personne · ADEME (impactco2.fr)")
    for k, (lab, v, col, st) in enumerate(TRIP):
        g = ease_out((u - st) / 0.1)
        hbar(c, 640 + k * 190, lab, v * g, 210, col, ease((u - st) / 0.05), (f"{v * g:.0f} kg" if v > 10 else f"{v * g:.1f} kg".replace('.', ',')))
    if u > 0.36: text_c(c, "traînées comprises", 330 + 540 * 155 / 210 / 2, 900, 26, (1, 1, 1, 0.7), bold=False)
    if u > 0.8: pill(c, "LE TGV : IMBATTABLE", W / 2, 1300, 44, GRN, fg=INK, s=back_out((u - 0.8) / 0.08))


def sc_caveat(c, t, s):
    u = U(t, s)
    background(c, t, tint=[(ORG, 540, 900, 520, 0.3)])
    title(c, t, s, "SOYONS HONNÊTES", "Lee et al. 2021 · forçage radiatif, effets non-CO2 compris")
    a = ease((t - s['t0']) / 0.3)
    plane(c, 'a330', W / 2, 650, 700, alpha=a)
    # traînées : lignes blanches derrière l'avion
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    for k in (-1, 1):
        c.set_source_rgba(1, 1, 1, 0.35 * a); c.set_line_width(14); c.move_to(W / 2 + 180, 640 + k * 30); c.line_to(W + 80, 560 + k * 60); c.stroke()
    v = 3.5 * ease_out((u - 0.25) / 0.25)
    text_c(c, f"≈ {v:.1f} %".replace('.', ','), W / 2, 1060, 170, (*ORG, a), stroke=14)
    text_c(c, "DU RÉCHAUFFEMENT", W / 2, 1150, 50, (1, 1, 1, a), stroke=8)
    if u > 0.7: pill(c, "ET LE TRAFIC AUGMENTE", W / 2, 1300, 44, RED, s=back_out((u - 0.7) / 0.08))


def sc_future(c, t, s):
    u = U(t, s)
    background(c, t, tint=[(GRN, 540, 900, 560, 0.3)], streak=0.6)
    title(c, t, s, "OBJECTIF 2050", "zéro émission nette de CO2 · OACI / secteur aérien")
    pts = [(2025, "2 %"), (2030, "6 %"), (2035, "20 %"), (2050, "70 %")]
    x0, x1, y = 150, 930, 820
    a = ease((t - s['t0']) / 0.3)
    c.set_source_rgba(1, 1, 1, 0.3 * a); c.set_line_width(6); c.move_to(x0, y); c.line_to(x1, y); c.stroke()
    p = ease((u - 0.1) / 0.6)
    c.set_source_rgba(*GRN, a); c.move_to(x0, y); c.line_to(x0 + (x1 - x0) * p, y); c.stroke()
    for k, (yr, pc) in enumerate(pts):
        x = x0 + (x1 - x0) * (yr - 2025) / 25; on = (yr - 2025) / 25 <= p + 1e-3
        c.arc(x, y, 16, 0, 2 * math.pi); c.set_source_rgba(*(GRN if on else (0.5, 0.5, 0.5)), a); c.fill()
        text_c(c, str(yr), x, y + 70, 36, (1, 1, 1, a))
        if on: text_c(c, pc, x, y - 40, 46, (*GRN, a), stroke=6)
    text_c(c, "carburants durables obligatoires en Europe (ReFuelEU)", W / 2, y + 150, 30, (1, 1, 1, 0.8 * a), bold=False)
    if u > 0.6:
        plane(c, 'a320', W / 2, 1240, 560, alpha=ease((u - 0.6) / 0.1))
        pill(c, "AVIONS NEUFS : −20 % DE CARBURANT", W / 2, 1460, 36, GREY, fg=INK, s=back_out((u - 0.66) / 0.08))


def sc_outro(c, t, s):
    u = U(t, s)
    background(c, t, tint=[(RED, 300, 1000, 500, 0.3), (GRN, 780, 1000, 500, 0.3)], streak=0.5)
    v = back_out((t - s['t0']) / 0.4)
    c.save(); c.translate(W / 2, 640); c.scale(v, v)
    text_c(c, "L'AVION :", 0, 0, 96, (1, 1, 1, 1), stroke=12)
    c.restore()
    pp = 1 + 0.05 * math.sin(t * 6)
    pill(c, "COUPABLE", 300, 900, 60, RED, s=back_out((u - 0.05) / 0.1) * pp)
    pill(c, "BOUC ÉMISSAIRE", 760, 1050, 54, GRN, fg=INK, s=back_out((u - 0.15) / 0.1) * (2 - pp))
    a = ease((u - 0.4) / 0.1)
    text_c(c, "DIS-LE EN COMMENTAIRE", W / 2, 1250, 50, (1, 1, 1, a), stroke=8)


R.SCN.update(hook=sc_hook, sectors=sc_sectors, digital=sc_digital, eff=sc_eff, trip=sc_trip, caveat=sc_caveat, future=sc_future, outro=sc_outro)
R.scoreboard = lambda c, t, s: None
R.HI_A = ["AVION", "AVIATION"]; R.HI_B = ["TGV"]

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        for tt in map(float, sys.argv[2:]):
            sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); R.render(tt, sf); sf.write_to_png(f'pol/still_{tt:.1f}.png')
        print(round(R.TOTAL, 1), [(x['scene'], round(x['t0'], 1)) for x in R.SEG]); sys.exit()
    nf = int(R.TOTAL * FPS)
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '21', '-pix_fmt', 'yuv420p', 'pol/video_noaudio.mp4'], stdin=subprocess.PIPE)
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    for f in range(nf):
        R.render(f / FPS, sf); sf.flush(); ff.stdin.write(bytes(sf.get_data()))
        if f % 300 == 0: print(f, '/', nf, flush=True)
    ff.stdin.close(); ff.wait(); print('done', R.TOTAL)
