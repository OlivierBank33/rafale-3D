"""Son v2 « qualité max » (sinus uniquement) calé sur la timeline au mot (timeline.json v2 + align.json) :
musique (pad + basse + arpège, progression i-VI-III-VII), risers et whooshes aux changements de scène, ticks aux cuts,
SFX d'événements calés sur les phrases, récap, et piste « voix » synthétique (enveloppe des phrases) pour le ducking.
Usage : DL=dl/<slug> python3 sm_audio2.py -> music.wav, sfx.wav, voice.wav"""
import json, os, importlib.util, numpy as np, soundfile as sf
D = os.environ.get('DL').rstrip('/') + '/'
TM = json.load(open(D + 'timeline.json')); SEGS = TM['seg']; TOTAL = TM['total']; AL = json.load(open(D + 'align.json'))
spec = importlib.util.spec_from_file_location('cfg', D + 'cfg.py'); CFG = importlib.util.module_from_spec(spec); spec.loader.exec_module(CFG)
SR = 48000; N = int(TOTAL * SR) + SR; T = np.arange(N) / SR
rng = np.random.default_rng(7)


def env(n, a=0.005, r=0.1):
    e = np.ones(n); na = max(1, min(n // 2, int(a * SR))); nr = max(1, min(n // 2, int(r * SR))); e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr); return e
def add(buf, at, sig, g=1.0):
    i = int(at * SR)
    if i < 0: sig = sig[-i:]; i = 0
    j = min(len(buf), i + len(sig))
    if i < len(buf) and j > i: buf[i:j] += sig[:j - i] * g
def tone(f, d, g=0.3, a=0.005, r=0.1, harm=0.0):
    n = int(d * SR); x = np.arange(n) / SR; s = np.sin(2 * np.pi * f * x) + harm * np.sin(4 * np.pi * f * x); return s * env(n, a, r) * g
def pluck(f, d=0.35, g=0.2):
    n = int(d * SR); x = np.arange(n) / SR; return (np.sin(2 * np.pi * f * x) + 0.3 * np.sin(4 * np.pi * f * x)) * np.exp(-x * 9) * env(n, 0.002, 0.05) * g
def gliss(f0, f1, d, g=0.2, a=0.01, r=0.1, curve=1.0):
    n = int(d * SR); x = np.linspace(0, 1, n) ** curve; f = f0 + (f1 - f0) * x; return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, a, r) * g
def impact(g=1.0, d=1.6):
    n = int(d * SR); x = np.arange(n) / SR; f = 90 * np.exp(-x * 3) + 34
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 2.6) + 0.25 * np.sin(2 * np.pi * 1800 * x) * np.exp(-x * 60)) * g
def whoosh(g=0.25):
    return gliss(2200, 220, 0.32, g, 0.04, 0.2, 0.6) + gliss(1700, 160, 0.32, g * 0.6, 0.06, 0.2, 0.7)
def riser(d=1.0, g=0.12):
    n = int(d * SR); x = np.linspace(0, 1, n); f = 260 + 1300 * x ** 2
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.5 * np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR)) * x ** 2 * g
def rumble(d, f=55, g=0.25):                       # moteurs / vent : sinus battants
    n = int(d * SR); x = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * (f * m + 0.7 * k) * x + k) / m for k in range(4) for m in (1, 2, 3))
    return s / 12 * env(n, 0.3, 0.4) * g
def spool(f0, f1, d, g=0.25):
    n = int(d * SR); x = np.linspace(0, 1, n); f = f0 + (f1 - f0) * x
    s = sum(np.sin(2 * np.pi * np.cumsum(f * m) / SR) / m for m in (1, 2, 3.01, 4.02))
    return s / 2 * env(n, 0.05, 0.3) * g
def stinger(root=110, g=0.4):
    return sum(tone(root * r, 2.2, g / 3, 0.003, 1.8) for r in (1, 1.189, 1.498, 2))
def heartbeat(t0, t1, bpm=72, g=0.6):
    tt = t0
    while tt < t1 - 0.3:
        add(sfx, tt, tone(52, 0.16, g, 0.002, 0.14)); add(sfx, tt + 0.21, tone(47, 0.14, g * 0.7, 0.002, 0.13)); tt += 60 / bpm


# ---------------- musique ----------------
MODE = getattr(CFG, 'MODE', 'serie'); ROOT = {'survie': 110.0, 'histoire': 146.83, 'serie': 98.0}.get(MODE, 110.0)
if 'AURAIS' in getattr(CFG, 'SERIES', ''): ROOT = 82.41
BPM = 92; BEAT = 60 / BPM; BAR = 4 * BEAT
PROG = [(0, (0, 3, 7)), (8, (0, 4, 7)), (3, (0, 4, 7)), (10, (0, 4, 7))]   # i - VI - III - VII (demi-tons depuis la tonique)
music = np.zeros(N); sfx = np.zeros(N)
ve = AL['voice_end']; mend = TOTAL
nbars = int(mend / BAR) + 2
for b in range(nbars):
    t0 = b * BAR
    if t0 > mend: break
    deg, tri = PROG[(b // 2) % 4]
    rootf = ROOT * 2 ** (deg / 12)
    for iv in tri:                                        # pad
        f = rootf * 2 ** (iv / 12)
        add(music, t0, tone(f, BAR + 0.3, 0.10, 0.5, 0.6)); add(music, t0, tone(f * 2.003, BAR + 0.3, 0.035, 0.6, 0.6))
    for k in (0, 2):                                      # basse
        add(music, t0 + k * BEAT, tone(rootf / 2, BEAT * 1.6, 0.30, 0.004, 0.5))
    notes = [rootf * 2 ** (iv / 12) * 2 for iv in tri] + [rootf * 4]
    for e in range(8):                                    # arpège croches
        add(music, t0 + e * BEAT / 2, pluck(notes[(e * 3 + b) % 4], 0.4, 0.09 if b > 0 else 0.0))
# respiration musicale : légère montée d'intensité sur la dernière scène parlée, fondu final
fade = np.ones(N); i0 = int((mend - 2.0) * SR); fade[i0:] = np.linspace(1, 0, N - i0) if i0 < N else 1
music *= fade

MUTE = []
def crackle(t0, d, g=0.04, n=40):
    for j in range(n): add(sfx, t0 + d * rng.random(), tone(rng.uniform(900, 2600), 0.025, g))
def sputter(t0, d, g=0.55, step=0.26):
    tt = t0
    while tt < t0 + d: add(sfx, tt, tone(68, 0.12, g, 0.003, 0.08)); add(sfx, tt + 0.05, tone(140, 0.06, g * 0.4)); tt += step * rng.uniform(0.8, 1.3)
def cues7(sc, s, S, at):
    end = s['end']
    if sc == 'fl_hook':
        add(sfx, at(0), rumble(2.4, 260, 0.1)); add(sfx, at(1), impact(0.5)); add(sfx, at(2, 0.45), tone(1320, 0.12, 0.1)); add(sfx, at(2, 0.55), stinger(ROOT * 2, 0.25)); add(sfx, at(3), stinger(ROOT, 0.4))
    if sc == 'fl_air':
        add(sfx, at(0), rumble(S[0][1] - S[0][0] + 0.5, 320, 0.1)); heartbeat(at(1), at(1, 0.5), 100, 0.45); heartbeat(at(1, 0.5), end, 50, 0.3)
    if sc == 'fl_wake':
        add(sfx, at(0), rumble(S[0][1] - S[0][0] + 0.4, 200, 0.12)); add(sfx, at(1), impact(0.6)); add(sfx, at(1), gliss(300, 1200, 0.4, 0.12))
        tt = at(2)
        while tt < end - 0.1: add(sfx, tt, tone(2000, 0.03, 0.12, 0.001, 0.02)); tt += 1.0
    if sc == 'fl_speed':
        add(sfx, at(0), spool(80, 300, 1.6, 0.2)); add(sfx, at(0), rumble(3.0, 380, 0.08)); add(sfx, at(1, 0.1), gliss(900, 500, 1.2, 0.08))
    if sc == 'fl_target':
        add(sfx, at(1), tone(660, 0.2, 0.15)); add(sfx, at(2, 0.4), impact(0.9)); add(sfx, at(3), pluck(1320, 0.4, 0.18)); add(sfx, at(3, 0.5), pluck(1568, 0.4, 0.18))
        for f in (0.25, 0.52, 0.79): add(sfx, at(4, f), pluck(1046, 0.3, 0.16))
    if sc == 'fl_magee':
        add(sfx, at(0), stinger(ROOT * 1.5, 0.25)); add(sfx, at(1), rumble(S[1][1] - S[1][0] + 0.5, 50, 0.4))
        for f in (0.15, 0.4, 0.7): add(sfx, at(1, f), impact(0.3, 0.8))
        add(sfx, at(2, 0.42), impact(0.7)); crackle(at(2, 0.42), 0.6, 0.06, 70); add(sfx, at(2, 0.74), stinger(ROOT * 2, 0.3))
    if sc == 'fl_vesna':
        add(sfx, at(0), gliss(700, 200, (S[0][1] - S[0][0]) * 0.66, 0.08)); add(sfx, at(0, 0.66), impact(0.8))
        for j in range(3): add(sfx, at(1) + j * 0.55, tone(1000, 0.08, 0.15))
        add(sfx, at(2), tone(1568, 0.5, 0.1, 0.002, 0.4)); add(sfx, at(2, 0.42), impact(0.7))
    if sc == 'fl_verdict':
        add(sfx, at(0), stinger(ROOT / 2, 0.5)); add(sfx, at(0, 0.3), impact(0.8)); add(sfx, at(1, 0.1), pluck(880, 0.4, 0.15)); add(sfx, at(1, 0.35), pluck(1100, 0.4, 0.15)); add(sfx, at(2), stinger(ROOT, 0.3))
    if sc == 'gr_hook':
        tt = at(0)
        while tt < at(1): add(sfx, tt, pluck(330, 0.15, 0.2)); tt += 0.83
        add(sfx, at(1), spool(60, 180, 1.4, 0.25)); add(sfx, at(2), stinger(ROOT, 0.3))
    if sc == 'gr_takeoff':
        tt = at(0)
        while tt < at(1) - 0.1: add(sfx, tt, tone(1800, 0.03, 0.12, 0.001, 0.02)); tt += 0.5
        add(sfx, at(1), rumble(S[1][1] - S[1][0] + 0.6, 45, 0.35)); add(sfx, at(1), spool(40, 140, 2.5, 0.2))
        for j in range(6): add(sfx, at(2, j / 6), pluck(660 * 2 ** (j / 12 * 2), 0.3, 0.1))
    if sc == 'gr_sea':
        for j in range(16): add(sfx, at(0, 0.05 + 0.05 * j), tone(1500, 0.02, 0.06, 0.001, 0.01))
        add(sfx, at(1), impact(0.5)); add(sfx, at(2), gliss(500, 700, 1.0, 0.05)); add(sfx, at(2, 0.4), pluck(880, 0.3, 0.12))
    if sc == 'gr_fail':
        sputter(at(0), S[0][1] - S[0][0]); add(sfx, at(1), spool(50, 190, 1.4, 0.3)); add(sfx, at(1, 0.3), stinger(ROOT * 2, 0.2))
        sputter(at(2), S[2][1] - S[2][0]); add(sfx, at(3), rumble(S[3][1] - S[3][0] + 0.5, 45, 0.3)); add(sfx, at(3), stinger(ROOT, 0.25))
    if sc == 'gr_land':
        add(sfx, at(0), tone(880, 0.6, 0.12, 0.002, 0.5)); add(sfx, at(0, 0.3), tone(660, 0.8, 0.12, 0.002, 0.6)); add(sfx, at(1), stinger(ROOT * 2, 0.3))
        add(sfx, at(2), rumble(2.0, 45, 0.25)); add(sfx, at(2, 0.6), impact(0.45))
        for j in range(4): add(sfx, at(3, 0.1) + j * 0.4, tone(1500 - 100 * j, 0.06, 0.12))
        add(sfx, at(3, 0.2), stinger(ROOT / 2, 0.3))
    if sc == 'gr_end':
        add(sfx, at(0), rumble(S[0][1] - S[0][0], 52, 0.2)); add(sfx, at(0, 0.55), gliss(800, 200, 2.0, 0.08)); add(sfx, at(1), stinger(ROOT * 1.5, 0.25)); add(sfx, at(2), stinger(ROOT, 0.3))
    if sc == 'e3_recap':
        for f in (0.2, 0.5): add(sfx, at(1, f), tone(70, 0.14, 0.6, 0.003, 0.1))
        add(sfx, at(2, 0.1), pluck(660, 0.3, 0.15)); add(sfx, at(2, 0.25), pluck(880, 0.3, 0.15)); add(sfx, at(2, 0.57), stinger(ROOT * 2, 0.3))
    if sc == 'e3_appr':
        add(sfx, at(0), rumble(S[0][1] - S[0][0] + 0.5, 55, 0.3)); add(sfx, at(0, 0.45), gliss(300, 500, 1.0, 0.06)); add(sfx, at(1, 0.2), pluck(1320, 0.4, 0.15))
    if sc == 'e3_quit':
        add(sfx, at(0), rumble(S[1][1] - S[0][0], 55, 0.3)); add(sfx, at(1, 0.45), spool(130, 18, 1.6, 0.4)); add(sfx, at(1, 0.6), impact(0.6))
        MUTE.append((at(2) - 0.1, at(4) - 0.1)); add(sfx, at(3), rumble(S[3][1] - S[3][0] + 1.0, 330, 0.12)); add(sfx, at(4), stinger(ROOT, 0.3))
    if sc == 'e3_glide':
        add(sfx, at(0, 0.1), impact(0.3, 0.6)); add(sfx, at(0, 0.2), impact(0.3, 0.6)); add(sfx, at(0, 0.35), tone(110, 0.45, 0.3, 0.005, 0.2)); heartbeat(at(1), end, 110, 0.45)
    if sc == 'e3_light':
        add(sfx, at(0, 0.35), tone(3000, 0.03, 0.2)); add(sfx, at(0, 0.35), tone(220, 1.5, 0.08, 0.3, 0.6)); add(sfx, at(1), pluck(990, 0.3, 0.12))
        crackle(at(2), end - at(2), 0.03, 60); add(sfx, at(3), stinger(ROOT, 0.45)); add(sfx, at(3), impact(0.6))
    if sc == 'e3_think':
        heartbeat(at(0), end, 120, 0.45)
        for j in range(5): add(sfx, at(0) + j / 2.2, tone(1000, 0.05, 0.12))
        add(sfx, at(1), pluck(660, 0.3, 0.15)); add(sfx, at(2, 0.2), impact(0.5)); add(sfx, at(3), pluck(880, 0.3, 0.15)); add(sfx, at(4, 0.2), tone(140, 0.3, 0.3))
    if sc == 'e3_choice':
        for k in (1, 2): add(sfx, at(k), tone(660 + 220 * k, 0.3, 0.14, 0.002, 0.25))


# ---------------- montage sonore ----------------
add(sfx, 0.04, impact(1.0)); add(sfx, 0.04, gliss(3000, 1200, 0.5, 0.08, 0.002, 0.4))            # titre « slam »
for i, s in enumerate(SEGS):
    if i > 0:
        add(sfx, s['t0'] - 1.0, riser(1.0, 0.07 if i < len(SEGS) - 2 else 0.12))
        add(sfx, s['t0'] - 0.05, whoosh(0.22)); add(sfx, s['t0'], impact(0.45, 1.0))
    for c0 in s['shots'][1:]:
        add(sfx, c0, tone(2900, 0.03, 0.05, 0.001, 0.02)); add(sfx, c0, tone(880, 0.07, 0.05, 0.002, 0.05))
    S = s['sent']; sc = s['scene']
    def at(k, frac=0.0, plus=0.0):
        k = min(k, len(S) - 1); a, b = S[k]; return a + (b - a) * frac + plus
    # --- cues par scène ---
    if sc == 'tw_hide':
        heartbeat(S[0][0], S[0][1], 84, 0.45)
        add(sfx, at(1), spool(70, 200, 3.0, 0.35)); add(sfx, at(1, 0.2), rumble(3.2, 48, 0.4))
        for j in range(12): add(sfx, at(2, j / 12), pluck(1760, 0.1, 0.06))
        add(sfx, at(3), stinger(ROOT, 0.35))
    if sc == 'tw_gear':
        add(sfx, at(0, 0.6), tone(110, 0.15, 0.6, 0.002, 0.1)); add(sfx, at(0, 0.6), tone(2200, 0.02, 0.2))
        heartbeat(at(1), at(2), 110, 0.5); add(sfx, at(2), impact(1.0))
    if sc == 'tw_cold':
        add(sfx, at(0), rumble(S[0][1] - S[0][0] + 0.6, 60, 0.3)); add(sfx, at(1), rumble(6.0, 300, 0.08))
        for j in range(5): add(sfx, at(2, j / 5), tone(2400 + 300 * j, 0.25, 0.04, 0.05, 0.2))
    if sc == 'tw_oxy':
        heartbeat(at(0), at(1, 0.5), 96, 0.5); heartbeat(at(1, 0.5), s['end'], 52, 0.35)
    if sc == 'tw_fall':
        add(sfx, at(0, 0.4), tone(140, 0.3, 0.4, 0.01, 0.2)); add(sfx, at(1, 0.1), tone(90, 0.4, 0.6, 0.005, 0.3)); add(sfx, at(1, 0.1), rumble(3, 220, 0.12))
        add(sfx, at(2, 0.1), gliss(1400, 300, 2.2, 0.12, 0.05, 0.4))
    if sc == 'tw_verdict':
        add(sfx, at(0), stinger(ROOT / 2, 0.5)); add(sfx, at(2), impact(0.8)); add(sfx, at(2, 0.3), impact(0.6))
    if sc == 'f_crash':
        add(sfx, at(0), impact(1.2)); add(sfx, at(0, 0.05), gliss(2500, 400, 0.6, 0.15, 0.002, 0.4))
        for j in range(8): add(sfx, at(2, j / 10), tone(300 + 150 * j, 0.08, 0.08))
        add(sfx, at(3), spool(400, 150, S[3][1] - S[3][0] + 0.5, 0.25))
    if sc == 'f_recover':
        add(sfx, at(1), rumble(4.0, 40, 0.5)); add(sfx, at(1), spool(90, 220, 2.5, 0.3))
    if sc == 'f_land':
        add(sfx, at(0), rumble(3.5, 45, 0.35)); add(sfx, at(1, 0.4), gliss(420, 380, 0.8, 0.3, 0.002, 0.6)); add(sfx, at(1, 0.48), tone(3000, 0.04, 0.3))
        for j in range(16): add(sfx, at(1, 0.48 + j * 0.02), tone(1500 + 400 * (j % 3), 0.03, 0.06))
        add(sfx, at(2, 0.1), impact(0.7))
    if sc == 'f_reveal':
        add(sfx, at(1), stinger(ROOT, 0.45)); add(sfx, at(1), impact(0.7))
    if sc == 'f_end':
        add(sfx, at(0, 0.5), tone(1320, 0.6, 0.12, 0.002, 0.5)); add(sfx, at(0, 0.55), tone(1760, 0.8, 0.1, 0.002, 0.6))
    if sc == 'g_hook':
        tt = at(2)
        while tt < s['end'] - 0.2: add(sfx, tt, tone(880, 0.16, 0.12)); add(sfx, tt + 0.2, tone(660, 0.16, 0.12)); tt += 0.8
        add(sfx, at(3), spool(260, 35, 2.0, 0.3)); add(sfx, at(4), spool(240, 30, 2.0, 0.3)); add(sfx, at(4, 0.6), tone(70, 0.6, 0.4, 0.005, 0.4))
    if sc == 'g_fuel':
        add(sfx, at(0, 0.5), impact(0.5)); add(sfx, at(1, 0.4), gliss(600, 200, 1.2, 0.12))
    if sc == 'g_options':
        for k in range(1, len(S)): add(sfx, at(k), tone(660 + 220 * k, 0.3, 0.14, 0.002, 0.25))
    if sc == 'g_pause':
        for k, f in ((2, 1000), (3, 1000), (4, 1500)): add(sfx, at(k), tone(f, 0.18, 0.25, 0.002, 0.1))
        heartbeat(at(0), s['end'], 120, 0.55)
    if sc == 'g_reveal':
        add(sfx, at(1), rumble(3.0, 260, 0.1))
        for j in range(60): add(sfx, at(2, 0.15 + j * 0.01), tone(rng.uniform(900, 2600), 0.03, 0.05))
        add(sfx, at(2, 0.15), impact(0.8)); add(sfx, at(2, 0.78), stinger(ROOT * 2, 0.3))
    if sc == 'g_end':
        add(sfx, at(0), stinger(ROOT * 2 * 1.26, 0.25))
    cues7(sc, s, S, at)
for a_, b_ in MUTE:                                          # silence musical (« plus aucun bruit »)
    gm = np.ones(N); i0, i1 = int(a_ * SR), int(b_ * SR); r_ = int(0.25 * SR)
    gm[i0:i1] = 0.06; gm[max(0, i0 - r_):i0] = np.linspace(1, 0.06, i0 - max(0, i0 - r_)); gm[i1:i1 + r_] = np.linspace(0.06, 1, len(gm[i1:i1 + r_]))
    music *= gm
# récap final + appel à s'abonner
if getattr(CFG, 'RECAP', None):
    t0 = ve + 0.9
    add(sfx, t0, whoosh(0.2))
    for j in range(3): add(sfx, t0 + 0.5 + j * 1.6, impact(0.35, 0.8)); add(sfx, t0 + 0.5 + j * 1.6, tone(1320, 0.2, 0.1, 0.002, 0.15))
    tc = t0 + 0.5 + 3 * 1.6 + 0.4; add(sfx, tc, tone(1568, 0.5, 0.12, 0.002, 0.4)); add(sfx, tc + 0.12, tone(2093, 0.7, 0.12, 0.002, 0.5))

# ---------------- « voix » pour le ducking : enveloppe des phrases ----------------
voice = np.zeros(N)
for s in SEGS:
    for a, b in s['sent']:
        n = int((b - a + 0.1) * SR); add(voice, a - 0.05, np.sin(2 * np.pi * 200 * np.arange(n) / SR) * env(n, 0.03, 0.06) * 0.9)

for name, x in (('voice', voice), ('music', music), ('sfx', sfx)):
    x = x[:int(TOTAL * SR)]; sf.write(D + name + '.wav', (x / (np.abs(x).max() + 1e-9) * 0.9).astype(np.float32), SR)
print('ok', round(TOTAL, 2))
