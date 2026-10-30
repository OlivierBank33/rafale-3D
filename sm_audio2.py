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
CINEMA = getattr(CFG, 'STYLE', '') == 'cinema'
INTEN = {'cc_hook': 0.6, 'cc_legend': 0.35, 'cc_flight': 0.3, 'cc_dc10': 0.5, 'cc_roll': 0.8, 'cc_burst': 0.95, 'cc_tank': 0.9, 'cc_fire': 1.0,
         'cc_engines': 1.0, 'cc_struggle': 1.0, 'cc_crash': 0.0, 'cc_after': 0.35, 'cc_justice': 0.3, 'cc_end': 0.5,
         'sw_hook': 0.8, 'sw_real': 0.35, 'sw_crack': 0.7, 'sw_decomp': 0.95, 'sw_cold': 0.9, 'sw_shake': 0.95, 'sw_manual': 0.8, 'sw_land': 0.5, 'sw_verdict': 0.4,
         'aw_hook': 0.7, 'aw_real': 0.3, 'aw_crash': 0.9, 'aw_cold': 0.6, 'aw_radio': 0.5, 'aw_decide': 0.35, 'aw_aval': 0.85, 'aw_trek': 0.75, 'aw_verdict': 0.4,
         'dv_hook': 0.8, 'dv_speed': 0.9, 'dv_stealth': 0.75, 'dv_multi': 0.8, 'dv_export': 0.6, 'dv_prod': 0.7, 'dv_verdict': 0.85,
         'jk_hook': 0.75, 'jk_real': 0.3, 'jk_storm': 0.85, 'jk_fall': 0.8, 'jk_hurt': 0.45, 'jk_river': 0.5, 'jk_found': 0.55, 'jk_later': 0.45, 'jk_verdict': 0.35,
         'tf_hook': 0.6, 'tf_bomb': 0.55, 'tf_fog': 0.5, 'tf_radio': 0.6, 'tf_roll': 0.85, 'tf_impact': 0.95, 'tf_toll': 0.2, 'tf_after': 0.4,
         'sx_hook': 0.55, 'sx_takeoff': 0.5, 'sx_vanish': 0.7, 'sx_bracelet': 0.4, 'sx_wreck': 0.55, 'sx_claim': 0.6, 'sx_verdict': 0.45}
def inten_at(tt):
    for sgx in SEGS:
        if sgx['t0'] <= tt < sgx['end']: return INTEN.get(sgx['scene'], 0.5)
    return 0.4
if CINEMA:                                               # partition de film : nappes lentes, piano rare, ostinato grave selon la tension
    ROOT = 110.0; BPM = 72; BEAT = 60 / BPM; BAR = 4 * BEAT
    PROGC = [(0, (0, 3, 7)), (8, (0, 4, 7)), (5, (0, 3, 7)), (7, (0, 4, 7))]   # i - VI - iv - V
    nb = int(mend / BAR) + 2
    for b in range(nb):
        t0 = b * BAR
        if t0 > mend: break
        deg, tri = PROGC[b % 4]; rootf = ROOT * 2 ** (deg / 12); it = inten_at(t0 + 0.1)
        for iv in tri:
            f = rootf * 2 ** (iv / 12)
            for det, g in ((1.0, 0.07), (1.004, 0.05), (2.0, 0.025), (0.5, 0.05)):
                add(music, t0, tone(f * det, BAR + 0.6, g * (0.7 + 0.5 * it), 1.4, 1.2))
        add(music, t0, pluck(rootf * 4 * 2 ** (tri[1] / 12), 1.6, 0.05)); add(music, t0 + 2 * BEAT, pluck(rootf * 4 * 2 ** (tri[2] / 12), 1.4, 0.04))
        if it >= 0.75:                                    # ostinato grave en croches
            for e in range(8):
                add(music, t0 + e * BEAT / 2, tone(rootf / 2, BEAT * 0.45, 0.16 * it, 0.004, 0.2))
                if e % 2 == 0: add(music, t0 + e * BEAT / 2, tone(rootf, BEAT * 0.3, 0.06 * it, 0.004, 0.15))
nbars = 0 if CINEMA else int(mend / BAR) + 2
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
    # ---- AF447 (sm_scenes8) ----
    def cricket(t0, d, g=0.12):
        tt = t0
        while tt < t0 + d: add(sfx, tt, tone(2900, 0.035, g, 0.002, 0.01)); add(sfx, tt + 0.012, tone(3300, 0.03, g * 0.7, 0.002, 0.01)); tt += 0.066
    if sc == 'af_hook':
        add(sfx, at(0), rumble(S[1][1] - S[0][0] + 0.5, 70, 0.25)); add(sfx, at(1, 0.2), pluck(1320, 0.4, 0.12))
        add(sfx, at(2, 0.05), gliss(1100, 140, (S[2][1] - S[2][0]) * 0.9, 0.12)); add(sfx, at(2, 0.95), impact(0.6)); add(sfx, at(3), stinger(ROOT / 2, 0.45))
    if sc == 'af_night':
        for j in range(5): add(sfx, at(0, 0.1 + 0.15 * j), pluck(440 * 2 ** (j * 3 / 12), 0.5, 0.08))
        for j in range(20): add(sfx, at(1, 0.1 + 0.035 * j), tone(1800, 0.02, 0.05, 0.001, 0.01))
        add(sfx, at(2, 0.6), tone(300, 0.06, 0.25)); add(sfx, at(2, 0.62), tone(150, 0.1, 0.3))
    if sc == 'af_storm':
        tt = at(0)
        while tt < at(1): add(sfx, tt, tone(1200, 0.06, 0.08)); tt += 0.83
        add(sfx, at(1), rumble(S[1][1] - S[1][0] + 0.8, 40, 0.35))
        for f in (0.15, 0.55, 0.9): add(sfx, at(1, f), impact(0.55, 1.4))
    if sc == 'af_pitot':
        for j in range(50): add(sfx, at(0, 0.35 + 0.6 * j / 50), tone(rng.uniform(3000, 5200), 0.03, 0.03))
        for j in range(12): add(sfx, at(1, 0.2 + 0.06 * j), tone(rng.uniform(200, 900), 0.05, 0.08))
        for rep in range(2):                                   # « cavalry charge » (sinus)
            for j, f in enumerate((523, 659, 784, 1046, 784, 1046)): add(sfx, at(2, 0.05) + rep * 0.75 + j * 0.11, tone(f, 0.1, 0.18, 0.003, 0.03))
    if sc == 'af_climb':
        add(sfx, at(0, 0.15), gliss(180, 320, 0.5, 0.15)); add(sfx, at(1), gliss(200, 520, S[1][1] - S[1][0], 0.07))
    if sc == 'af_stall':
        tt = at(0)
        while tt < end - 0.3: cricket(tt, 0.45, 0.11 if tt < at(1) else 0.06); tt += 1.0
        add(sfx, at(1), rumble(S[1][1] - S[1][0] + 0.5, 60, 0.3)); add(sfx, at(3), stinger(ROOT / 2, 0.35))
    if sc == 'af_captain':
        add(sfx, at(0, 0.1), tone(300, 0.06, 0.25))
        tt = at(1)
        while tt < end - 0.2: add(sfx, tt, tone(1050, 0.18, 0.1, 0.005, 0.05)); add(sfx, tt + 0.22, tone(840, 0.18, 0.1, 0.005, 0.05)); tt += 0.5
        cricket(at(0), 0.45, 0.06)
    if sc == 'af_fall':
        add(sfx, at(0), rumble(S[0][1] - S[0][0] + 0.5, 330, 0.12)); add(sfx, at(0), rumble(S[1][1] - S[0][0], 45, 0.35))
        for j in range(int(S[1][1] - S[1][0])): add(sfx, at(1) + j, tone(1600, 0.03, 0.08, 0.001, 0.02))
        MUTE.append((at(2) - 0.15, end + 0.4)); add(sfx, at(2), tone(73.4, 3.0, 0.2, 0.3, 2.0))
    if sc == 'af_search':
        tt = at(0, 0.35)
        while tt < end - 0.3: add(sfx, tt, tone(1480, 0.5, 0.12, 0.002, 0.45)); add(sfx, tt + 0.5, tone(1480, 0.4, 0.04, 0.002, 0.35)); tt += 1.6
        add(sfx, at(0, 0.62), stinger(ROOT, 0.25))
    if sc == 'af_after':
        for f in (0.0, 0.05): add(sfx, at(1, f), impact(0.35, 0.6))
        for j in range(6): add(sfx, at(2, 0.05 + 0.12 * j), pluck(880 * 2 ** ([0, 4, 7, 12, 7, 4][j] / 12), 0.8, 0.07))

    # ---- SR-71 (sm_scenes9) ----
    def alarm2(t0, t1, f0=1050, f1=840, g=0.1, step=0.5):
        tt = t0
        while tt < t1 - 0.2: add(sfx, tt, tone(f0, 0.18, g, 0.005, 0.05)); add(sfx, tt + 0.22, tone(f1, 0.18, g, 0.005, 0.05)); tt += step
    if sc == 'sb_hook':
        add(sfx, at(0), rumble(S[0][1] - S[0][0], 330, 0.1)); add(sfx, at(0, 0.66), impact(0.9)); add(sfx, at(0, 0.66), gliss(900, 120, 1.0, 0.1)); crackle(at(0, 0.66), 0.8, 0.05, 50)
        for j in range(6): add(sfx, at(1) + j * 0.12, tone(1400, 0.02, 0.05, 0.001, 0.01))
        add(sfx, at(1, 0.3), stinger(ROOT * 1.5, 0.25)); add(sfx, at(2), stinger(ROOT, 0.35))
    if sc == 'sb_jet':
        add(sfx, at(0), rumble(S[0][1] - S[0][0] + 0.4, 70, 0.25)); add(sfx, at(0), spool(60, 200, 1.5, 0.15))
        add(sfx, at(1, 0.05), pluck(880, 0.4, 0.15)); add(sfx, at(2, 0.05), pluck(1100, 0.4, 0.15))
    if sc == 'sb_unstart':
        add(sfx, at(0), gliss(200, 700, (S[0][1] - S[0][0]) * 0.7, 0.07))
        add(sfx, at(1, 0.48), impact(1.0)); add(sfx, at(1, 0.48), tone(60, 0.5, 0.35, 0.002, 0.4)); sputter(at(1, 0.6), (S[1][1] - S[1][0]) * 0.4)
        add(sfx, at(2), rumble(S[2][1] - S[2][0] + 0.4, 50, 0.3)); add(sfx, at(2, 0.2), gliss(500, 250, 1.4, 0.08))
    if sc == 'sb_break':
        add(sfx, at(0, 0.15), gliss(120, 90, 0.8, 0.15)); alarm2(at(1), at(2), 1200, 900, 0.1, 0.45)
        add(sfx, at(2, 0.05), impact(1.0)); add(sfx, at(2, 0.05), rumble(S[2][1] - S[2][0] + 0.6, 45, 0.4)); crackle(at(2, 0.05), S[2][1] - S[2][0], 0.06, 90)
    if sc == 'sb_out':
        MUTE.append((at(0) - 0.1, at(2) - 0.1)); heartbeat(at(0), at(2) - 0.1, 48, 0.4)
        add(sfx, at(1), tone(220, 1.6, 0.06, 0.4, 1.0)); add(sfx, at(2), rumble(S[2][1] - S[2][0] + 0.5, 330, 0.12)); add(sfx, at(2), whoosh(0.3))
    if sc == 'sb_suit':
        add(sfx, at(0, 0.1), gliss(300, 520, 1.6, 0.05)); add(sfx, at(0, 0.3), pluck(880, 0.3, 0.12))
        tt = at(1)
        while tt < at(2) - 0.3: add(sfx, tt, tone(140, 0.7, 0.06, 0.3, 0.3)); tt += 1.4
        add(sfx, at(2), stinger(ROOT * 2, 0.3)); add(sfx, at(2, 0.1), tone(70, 0.4, 0.4, 0.003, 0.3))
        for j in range(8): add(sfx, at(2, 0.2) + j * 0.2, tone(rng.uniform(600, 1200), 0.05, 0.05))
    if sc == 'sb_chute':
        add(sfx, at(0), rumble((S[0][1] - S[0][0]) * 0.7, 330, 0.12)); add(sfx, at(0, 0.72), impact(0.7)); add(sfx, at(0, 0.72), gliss(500, 200, 0.4, 0.12))
        add(sfx, at(0, 0.8), pluck(660, 0.4, 0.12)); add(sfx, at(0, 0.9), pluck(990, 0.5, 0.12))
        tt = at(1)
        while tt < end - 0.3: add(sfx, tt, tone(85, 0.05, 0.12, 0.002, 0.03)); tt += 0.085
    if sc == 'sb_verdict':
        for j, f in enumerate((660, 880, 1100)): add(sfx, at(0, 0.1) + j * 0.14, pluck(f, 0.5, 0.15))
        MUTE.append((at(1) - 0.1, at(2) - 0.1)); add(sfx, at(1), tone(73.4, 2.5, 0.18, 0.3, 1.8))
        add(sfx, at(2), stinger(ROOT, 0.35))
    # ---- Concorde (sm_scenes9) ----
    if sc == 'co_hook':
        for j in range(4): add(sfx, at(0, 0.1) + j * 1.25, tone(2600, 0.12, 0.05, 0.003, 0.1))
        add(sfx, at(0, 0.5), rumble(2.6, 60, 0.25)); add(sfx, at(0, 0.5), whoosh(0.3))
    if sc == 'co_dc10':
        tt = at(0)
        while tt < at(1) - 0.1: add(sfx, tt, tone(1800, 0.03, 0.12, 0.001, 0.02)); tt += 0.5
        add(sfx, at(1), rumble(S[1][1] - S[1][0] + 0.4, 55, 0.3)); add(sfx, at(1), spool(50, 160, 2.0, 0.15))
        for j in range(5): add(sfx, at(2, 0.1 + 0.08 * j), tone(2400 - 200 * j, 0.04, 0.1))
        add(sfx, at(2, 0.6), impact(0.35, 0.6)); add(sfx, at(2, 0.6), tone(3100, 0.25, 0.06, 0.002, 0.2))
    if sc == 'co_roll':
        add(sfx, at(0), rumble(S[1][1] - S[0][0] + 0.3, 50, 0.35)); add(sfx, at(0), spool(50, 220, S[0][1] - S[0][0], 0.15))
        add(sfx, at(1, 0.3), pluck(1320, 0.3, 0.1))
        add(sfx, at(2), impact(1.0)); add(sfx, at(2), tone(55, 0.6, 0.4, 0.002, 0.5)); crackle(at(2), 0.7, 0.07, 60)
    if sc == 'co_tank':
        add(sfx, at(0, 0.2), gliss(1400, 400, 1.2, 0.08)); add(sfx, at(0, 0.88), impact(0.7))
        for j in range(5): add(sfx, at(1) + j * 0.5, tone(48, 0.4, 0.3, 0.003, 0.35)); add(sfx, at(1) + j * 0.5, tone(96, 0.2, 0.08))
        add(sfx, at(2, 0.3), impact(0.8)); add(sfx, at(2, 0.3), rumble(S[2][1] - S[2][0], 35, 0.3)); crackle(at(2, 0.3), (S[2][1] - S[2][0]) * 0.8, 0.05, 80)
    if sc == 'co_fire':
        add(sfx, at(0), rumble(end - at(0), 55, 0.25)); crackle(at(0), S[0][1] - S[0][0], 0.04, 60)
        tt = at(1)
        while tt < at(2) - 0.15: add(sfx, tt, tone(1000, 0.09, 0.08, 0.002, 0.03)); tt += 0.18
        add(sfx, at(1, 0.3), spool(140, 60, 1.2, 0.2))
        for f in (0.25, 0.55): add(sfx, at(2, f), impact(0.3, 0.5)); add(sfx, at(2, f), tone(1600, 0.06, 0.06))
    if sc == 'co_crash':
        add(sfx, at(0), gliss(160, 110, S[0][1] - S[0][0], 0.1))
        add(sfx, at(1), tone(220, 0.5, 0.06, 0.1, 0.4)); add(sfx, at(1, 0.4), gliss(400, 150, 1.5, 0.05))
        MUTE.append((at(2) - 0.15, end + 0.3)); add(sfx, at(2), tone(73.4, 3.0, 0.18, 0.3, 2.0))
    if sc == 'co_after':
        add(sfx, at(0, 0.2), pluck(660, 0.4, 0.1))
        for j in range(4): add(sfx, at(1, 0.05 + 0.1 * j), pluck(523 * 2 ** ([0, 4, 7, 12][j] / 12), 0.6, 0.1))
        add(sfx, at(2), stinger(ROOT / 2, 0.3))
        for j in range(6): add(sfx, at(3, 0.05 + 0.12 * j), pluck(880 * 2 ** ([0, 4, 7, 12, 7, 4][j] / 12), 0.8, 0.07))
    # ---- MH370 (sm_scenes9) ----
    def ping(t0, f=1480, g=0.11): add(sfx, t0, tone(f, 0.5, g, 0.002, 0.45)); add(sfx, t0 + 0.5, tone(f, 0.4, g * 0.33, 0.002, 0.35))
    if sc == 'mh_hook':
        add(sfx, at(0), rumble(S[1][1] - S[0][0], 70, 0.22))
        for j in range(8): add(sfx, at(0, 0.2 + 0.06 * j), tone(1800, 0.02, 0.06, 0.001, 0.01))
        add(sfx, at(1), gliss(600, 150, (S[1][1] - S[1][0]) * 0.7, 0.08)); ping(at(2), 1180); add(sfx, at(2), stinger(ROOT, 0.35))
    if sc == 'mh_night':
        for j in range(4): add(sfx, at(0, 0.1 + 0.15 * j), pluck(440 * 2 ** ([0, 3, 7, 10][j] / 12), 0.5, 0.08))
        add(sfx, at(1), rumble(S[1][1] - S[1][0] + 0.3, 70, 0.15))
        tt = at(2)
        while tt < end - 0.4: ping(tt, 1700, 0.05); tt += 1.6
        add(sfx, at(2, 0.25), tone(300, 0.06, 0.25)); add(sfx, at(2, 0.27), tone(150, 0.1, 0.3))
    if sc == 'mh_dark':
        add(sfx, at(0, 0.48), tone(880, 0.12, 0.15)); add(sfx, at(0, 0.5), gliss(880, 110, 0.6, 0.1))
        MUTE.append((at(0, 0.5), end - 0.1)); add(sfx, at(1), tone(55, 2.5, 0.18, 0.5, 1.5))
    if sc == 'mh_turn':
        tt = at(0)
        while tt < end - 0.3: add(sfx, tt, tone(520, 0.12, 0.1, 0.002, 0.1)); tt += 1.2
        add(sfx, at(1, 0.1), stinger(ROOT / 2, 0.3))
    if sc == 'mh_arcs':
        add(sfx, at(0), pluck(1320, 0.4, 0.12))
        tt = at(1)
        while tt < at(2) - 0.2: add(sfx, tt, tone(1760, 0.06, 0.08)); add(sfx, tt + 0.08, tone(2350, 0.05, 0.06)); tt += 0.9
        for j in range(7): add(sfx, at(2) + (S[2][1] - S[2][0]) * j / 7, pluck(440 * 2 ** (j * 2 / 12), 0.4, 0.12))
        add(sfx, at(3), stinger(ROOT * 2, 0.3)); add(sfx, at(3, 0.3), tone(1320, 0.8, 0.08, 0.002, 0.7))
    if sc == 'mh_flaperon':
        add(sfx, at(0), rumble(S[0][1] - S[0][0], 40, 0.12)); add(sfx, at(0, 0.85), pluck(990, 0.5, 0.12))
        add(sfx, at(1), rumble(end - at(1), 90, 0.08)); add(sfx, at(1, 0.15), stinger(ROOT * 1.5, 0.25))
    if sc == 'mh_search':
        tt = at(0, 0.1)
        while tt < at(1) - 0.3: ping(tt); tt += 1.6
        add(sfx, at(1), stinger(ROOT / 2, 0.35))
    if sc == 'mh_end':
        for j in range(6): add(sfx, at(0, 0.05 + 0.12 * j), pluck(660 * 2 ** ([0, 3, 7, 10, 7, 3][j] / 12), 0.8, 0.06))
        add(sfx, at(1), stinger(ROOT, 0.3))

    # ---- Concorde premium (sm_scenes10) ----
    def roar(t0, d, g=0.3, f=42):
        add(sfx, t0, rumble(d, f, g)); add(sfx, t0, rumble(d, f * 1.51, g * 0.5)); add(sfx, t0, rumble(d, 330, g * 0.12))
    def bell(t0, t1, g=0.09):
        tt = t0
        while tt < t1 - 0.1: add(sfx, tt, tone(980, 0.09, g, 0.002, 0.06)); add(sfx, tt + 0.1, tone(980, 0.09, g * 0.8, 0.002, 0.06)); tt += 0.5
    if sc == 'cc_hook':
        roar(at(0), S[0][1] - S[0][0] + 0.3, 0.22, 38); crackle(at(0), S[0][1] - S[0][0], 0.03, 50)
        add(sfx, at(1, 0.05), tone(2600, 1.2, 0.07, 0.002, 1.1)); add(sfx, at(1, 0.05), tone(3480, 0.9, 0.04, 0.002, 0.8))
        add(sfx, at(2), spool(35, 110, S[2][1] - S[2][0] + 0.6, 0.18)); add(sfx, at(2, 0.9), stinger(ROOT / 2, 0.35))
    if sc == 'cc_legend':
        add(sfx, at(0), tone(880, S[0][1] - S[0][0], 0.03, 0.8, 0.8)); add(sfx, at(0), whoosh(0.18))
        for j, f in enumerate((660, 880, 990, 1320)): add(sfx, at(1, 0.1) + j * 0.22, pluck(f, 0.9, 0.06))
    if sc == 'cc_flight':
        for j in range(60): add(sfx, at(0, 0.03) + j * 0.028, tone(rng.uniform(1500, 2400), 0.012, 0.05, 0.001, 0.008))
        for j in range(25): add(sfx, at(1, 0.05) + j * (S[1][1] - S[1][0]) * 0.8 / 25, tone(1760, 0.03, 0.03, 0.002, 0.02))
        add(sfx, at(2), gliss(300, 520, 1.6, 0.04))
    if sc == 'cc_dc10':
        roar(at(0), S[0][1] - S[0][0] + 0.5, 0.16, 55); add(sfx, at(0, 0.3), spool(60, 160, 2.2, 0.12))
        add(sfx, at(1), gliss(1800, 600, (S[1][1] - S[1][0]) * 0.55, 0.05))
        for f, g in ((2400, 0.12), (3150, 0.08), (4100, 0.05)): add(sfx, at(1, 0.55), tone(f, 0.5, g, 0.001, 0.45))
        add(sfx, at(1, 0.72), tone(2700, 0.3, 0.06, 0.001, 0.28))
    if sc == 'cc_roll':
        add(sfx, at(0, 0.1), tone(70, 0.5, 0.35, 0.003, 0.4)); add(sfx, at(0, 0.1), tone(1200, 0.05, 0.06))
        roar(at(1), s['end'] - at(1) + 0.4, 0.42, 36); add(sfx, at(1), spool(28, 95, S[1][1] - S[1][0], 0.25))
        add(sfx, at(2), gliss(180, 420, S[2][1] - S[2][0] + 0.4, 0.06))
    if sc == 'cc_burst':
        roar(at(0), S[0][1] - S[0][0] + 0.1, 0.4, 36); add(sfx, at(0), gliss(300, 520, S[0][1] - S[0][0], 0.05))
        add(sfx, at(1), impact(1.3)); add(sfx, at(1), tone(48, 1.2, 0.5, 0.002, 1.0)); add(sfx, at(1), gliss(2400, 200, 0.7, 0.1))
        MUTE.append((at(1) - 0.02, at(2) + 0.2)); heartbeat(at(1, 0.3), at(2, 0.2), 54, 0.35)
        add(sfx, at(2), whoosh(0.25)); add(sfx, at(2, 0.45), impact(0.8, 1.2)); add(sfx, at(2, 0.45), tone(95, 0.4, 0.35, 0.003, 0.35))
    if sc == 'cc_tank':
        add(sfx, at(0), tone(120, S[0][1] - S[0][0] + 0.3, 0.05, 0.2, 0.3)); add(sfx, at(0, 0.5), pluck(1320, 0.5, 0.06))
        for j in range(5): add(sfx, at(1, 0.15) + j * 0.55, tone(44, 0.45, 0.4, 0.003, 0.4)); add(sfx, at(1, 0.15) + j * 0.55, tone(88, 0.2, 0.1))
        add(sfx, at(2), impact(0.9)); add(sfx, at(2), gliss(2600, 900, 0.5, 0.08)); crackle(at(2), 0.6, 0.05, 30)
        for j in range(70): add(sfx, at(3) + rng.random() * (S[3][1] - S[3][0]), tone(rng.uniform(250, 700), 0.05, 0.03, 0.005, 0.04))
        add(sfx, at(3, 0.8), gliss(70, 220, 0.6, 0.35)); roar(at(3, 0.8), s['end'] - at(3, 0.8) + 0.4, 0.35, 34)
    if sc == 'cc_fire':
        roar(at(0), S[0][1] - S[0][0] + 0.3, 0.45, 32); crackle(at(0), S[0][1] - S[0][0], 0.05, 80)
        for j in range(2): add(sfx, at(1, 0.05) + j * 0.35, tone(1050, 0.12, 0.08, 0.003, 0.05))
        bell(at(2), at(3), 0.08)
        roar(at(3), s['end'] - at(3) + 0.5, 0.4, 36); add(sfx, at(3), gliss(160, 260, 1.0, 0.1))
    if sc == 'cc_engines':
        bell(at(0), at(2), 0.06); add(sfx, at(0, 0.2), spool(130, 45, 1.6, 0.3)); roar(at(0), s['end'] - at(0), 0.25, 40)
        add(sfx, at(1, 0.15), impact(0.5, 0.8)); add(sfx, at(1, 0.2), spool(60, 18, 1.0, 0.3))
        add(sfx, at(2, 0.1), impact(0.45, 0.7)); add(sfx, at(2, 0.14), tone(180, 0.12, 0.3)); add(sfx, at(2, 0.4), tone(180, 0.12, 0.25))
    if sc == 'cc_struggle':
        roar(at(0), S[0][1] - S[0][0] + 0.4, 0.4, 38); heartbeat(at(0), s['end'], 104, 0.4)
        for j in range(3): add(sfx, at(1, 0.2 + 0.25 * j), tone(880, 0.25, 0.05, 0.003, 0.2))
    if sc == 'cc_crash':
        roar(at(0), (S[0][1] - S[0][0]) * 0.85, 0.32, 38)
        MUTE.append((at(0, 0.85), s['end'] + 0.6)); add(sfx, at(0, 0.88), tone(55, 4.0, 0.22, 0.6, 3.0))
        add(sfx, at(2, 0.1), tone(73.4, 3.0, 0.12, 0.6, 2.0))
        for j, f in enumerate((440, 554, 659)): add(sfx, at(2, 0.3) + j * 0.7, pluck(f, 1.6, 0.035))
    if sc == 'cc_after':
        for j in range(5): add(sfx, at(0, 0.05) + j * 0.3, pluck(660 * 2 ** (j * 2 / 12), 0.4, 0.06)); add(sfx, at(0, 0.05) + j * 0.3, tone(2800, 0.03, 0.03))
        add(sfx, at(1, 0.1), pluck(990, 0.6, 0.06))
        for j, f in enumerate((523, 659, 784, 1046)): add(sfx, at(2, 0.05) + j * 0.15, pluck(f, 0.8, 0.07))
    if sc == 'cc_justice':
        for j in range(2): add(sfx, at(0, 0.25) + j * 0.32, impact(0.55, 0.6)); add(sfx, at(0, 0.25) + j * 0.32, tone(140, 0.12, 0.3))
        add(sfx, at(1, 0.2), pluck(660, 0.6, 0.06)); add(sfx, at(1, 0.5), pluck(440, 0.8, 0.06))
    if sc == 'cc_end':
        add(sfx, at(0), tone(220, S[0][1] - S[0][0] + 1.0, 0.04, 1.0, 1.0))
        add(sfx, at(1, 0.2), pluck(880, 0.5, 0.06)); add(sfx, at(1, 0.45), pluck(587, 0.6, 0.06))
        add(sfx, at(2), stinger(ROOT, 0.3)); add(sfx, at(2, 0.2), pluck(880, 1.2, 0.06))

    # ---- Sichuan 3U8633 (sm_scenes11) ----
    def wind(t0, d, g=0.2): add(sfx, t0, rumble(d, 330, g * 0.5)); add(sfx, t0, rumble(d, 62, g)); add(sfx, t0, rumble(d, 520, g * 0.18))
    def creak(t0, n=4, g=0.06):
        for j in range(n): add(sfx, t0 + j * 0.16 + 0.05 * rng.random(), tone(rng.uniform(2200, 3400), 0.05, g, 0.001, 0.04))
    if sc == 'sw_hook':
        add(sfx, at(0), rumble(S[0][1] - S[0][0], 90, 0.06)); creak(at(0, 0.15), 3); creak(at(0, 0.5), 4, 0.08)
        tb = S[0][0] + 0.7 * (S[1][0] - S[0][0])
        add(sfx, tb, impact(1.4)); add(sfx, tb, gliss(2600, 180, 0.6, 0.1)); crackle(tb, 0.5, 0.06, 60); wind(tb, at(2) - tb + 0.3, 0.3)
        add(sfx, at(2), stinger(ROOT, 0.35))
    if sc == 'sw_real':
        add(sfx, at(0), rumble(end - at(0), 95, 0.05)); add(sfx, at(0, 0.1), pluck(880, 0.6, 0.06))
        for j in range(4): add(sfx, at(1, 0.1) + j * 0.5, pluck(660 * 2 ** ([0, 3, 7, 12][j] / 12), 0.5, 0.05))
    if sc == 'sw_crack':
        add(sfx, at(0), rumble(S[0][1] - S[0][0], 95, 0.05)); creak(at(0, 0.45), 3, 0.07); creak(at(0, 0.75), 5, 0.09)
        add(sfx, at(1), impact(1.4)); add(sfx, at(1), gliss(2400, 200, 0.6, 0.1)); crackle(at(1), 0.5, 0.06, 60); wind(at(1), end - at(1) + 0.3, 0.32)
    if sc == 'sw_decomp':
        add(sfx, at(0), whoosh(0.3)); wind(at(0), end - at(0), 0.28)
        tt = at(0, 0.4)
        while tt < at(1) - 0.1: add(sfx, tt, tone(1000, 0.18, 0.07, 0.003, 0.1)); add(sfx, tt + 0.25, tone(1000, 0.18, 0.07, 0.003, 0.1)); tt += 1.0
        heartbeat(at(2), end, 112, 0.4); add(sfx, at(2, 0.2), tone(140, 0.25, 0.3, 0.003, 0.2))
    if sc == 'sw_cold':
        wind(at(0), end - at(0), 0.3)
        for j in range(30): add(sfx, at(0) + rng.random() * (S[0][1] - S[0][0]), tone(rng.uniform(3000, 4200), 0.04, 0.025, 0.001, 0.03))
        add(sfx, at(0, 0.6), tone(2093, 1.2, 0.04, 0.01, 1.1)); add(sfx, at(1), rumble(end - at(1), 48, 0.3))
    if sc == 'sw_shake':
        for j in range(3):
            for f in (1480, 1760, 1480): add(sfx, at(0, 0.05) + j * 0.55 + (f == 1760) * 0.12, tone(f, 0.1, 0.06, 0.002, 0.06))
        wind(at(0), end - at(0), 0.22); add(sfx, at(1), rumble(end - at(1), 28, 0.35)); heartbeat(at(1), end, 120, 0.35)
    if sc == 'sw_manual':
        wind(at(0), end - at(0), 0.2); heartbeat(at(0), end, 96, 0.35); add(sfx, at(0, 0.6), stinger(ROOT * 1.5, 0.2))
    if sc == 'sw_land':
        add(sfx, at(0), rumble(S[0][1] - S[0][0], 80, 0.18)); add(sfx, at(0, 0.8), impact(0.5)); add(sfx, at(0, 0.8), tone(1700, 0.3, 0.04, 0.005, 0.25))
        add(sfx, at(0, 0.8), rumble(1.8, 55, 0.25)); add(sfx, at(1), stinger(ROOT * 2, 0.25))
        for j in range(3): add(sfx, at(1, 0.3) + j * 0.4, pluck(880 * 2 ** ([0, 4, 7][j] / 12), 0.6, 0.06))
    if sc == 'sw_verdict':
        add(sfx, at(0), stinger(ROOT * 2, 0.3)); add(sfx, at(0, 0.1), gliss(400, 900, 1.2, 0.04))
        add(sfx, at(1, 0.15), tone(120, 0.6, 0.06)); add(sfx, at(1, 0.4), gliss(3000, 1200, 0.3, 0.06)); crackle(at(1, 0.4), 0.5, 0.05, 50)
        add(sfx, at(2), stinger(ROOT, 0.35))
    # ---- TU ES LE PILOTE ép. 4 (sm_scenes11) ----
    def splash(t0, d=0.8, g=0.05, n=80):
        for j in range(n): add(sfx, t0 + d * rng.random() ** 1.6, tone(rng.uniform(600, 3200), 0.06, g, 0.002, 0.05))
    if sc == 'e4_recap':
        add(sfx, at(0), rumble(S[0][1] - S[0][0], 300, 0.08)); add(sfx, at(0, 0.3), stinger(ROOT, 0.3))
        for f in (0.2, 0.5): add(sfx, at(1, f), tone(70, 0.14, 0.5, 0.003, 0.1))
        add(sfx, at(2, 0.1), pluck(660, 0.3, 0.15)); add(sfx, at(2, 0.25), pluck(880, 0.3, 0.15)); add(sfx, at(2, 0.62), stinger(ROOT * 2, 0.3))
    if sc == 'e4_gear':
        add(sfx, at(0, 0.05), spool(220, 120, 1.1, 0.12)); add(sfx, at(0, 0.38), tone(90, 0.2, 0.4, 0.002, 0.18))
        add(sfx, at(0, 0.7), tone(60, 0.4, 0.3, 0.003, 0.3)); splash(at(0, 0.72), 0.6, 0.04, 40)
        add(sfx, at(1, 0.15), tone(150, 0.1, 0.35, 0.002, 0.08)); add(sfx, at(1, 0.22), tone(110, 0.14, 0.3, 0.002, 0.1)); add(sfx, at(1, 0.45), pluck(990, 0.4, 0.12))
    if sc == 'e4_flare':
        add(sfx, at(0), rumble(end - at(0), 300, 0.1)); add(sfx, at(0), rumble(end - at(0), 70, 0.08))
        heartbeat(at(1), end, 118, 0.4); add(sfx, at(1, 0.3), gliss(700, 400, 1.5, 0.05))
    if sc == 'e4_touch':
        add(sfx, at(0, 0.05), impact(1.1)); splash(at(0, 0.05), 1.2, 0.06, 120)
        add(sfx, at(1), impact(1.2, 1.2)); splash(at(1), 1.0, 0.07, 120); add(sfx, at(1), rumble(S[1][1] - S[1][0], 60, 0.3))
        add(sfx, at(2), tone(90, 0.3, 0.4, 0.003, 0.25)); heartbeat(at(2, 0.2), end, 104, 0.35)
    if sc == 'e4_stop':
        add(sfx, at(0), rumble(S[0][1] - S[0][0], 80, 0.22)); splash(at(0), S[0][1] - S[0][0], 0.03, 60)
        add(sfx, at(1, 0.1), stinger(ROOT * 2, 0.3)); add(sfx, at(1, 0.3), pluck(1320, 0.5, 0.12))
    if sc == 'e4_out':
        for j in range(4): splash(at(0, 0.2) + j * 0.6, 0.25, 0.04, 20)
        for j in range(6): add(sfx, at(1, 0.05) + j * 0.22, tone(rng.uniform(300, 500), 0.12, 0.04, 0.01, 0.08))
        add(sfx, at(1, 0.4), pluck(880, 0.6, 0.1))
    if sc == 'e4_end':
        add(sfx, at(0), stinger(ROOT * 2, 0.35)); add(sfx, at(0, 0.2), gliss(400, 900, 1.0, 0.05))
        for j in range(4): add(sfx, at(1) + 0.15 * j, pluck(660 * 2 ** ([0, 4, 7, 12][j] / 12), 0.5, 0.12))
        add(sfx, at(2), stinger(ROOT * 1.5, 0.3)); add(sfx, at(3), stinger(ROOT, 0.35))


    # ---- Andes 1972 (sm_scenes12) ----
    def gust(t0, d, g=0.14): add(sfx, t0, rumble(d, 230, g * 0.6)); add(sfx, t0, rumble(d, 75, g)); add(sfx, t0, gliss(300, 520, d, g * 0.12, 0.6, 0.6))
    if sc == 'aw_hook':
        add(sfx, at(0), rumble(S[0][1] - S[0][0] + 0.3, 95, 0.12)); add(sfx, at(0), rumble(S[0][1] - S[0][0], 190, 0.05))
        gust(at(1), S[1][1] - S[1][0] + 0.4, 0.16); add(sfx, at(2), stinger(ROOT, 0.35)); gust(at(2), end - at(2), 0.12)
    if sc == 'aw_real':
        add(sfx, at(0), tone(220, S[0][1] - S[0][0] + 0.5, 0.04, 0.6, 0.6)); add(sfx, at(0, 0.6), pluck(880, 0.8, 0.06))
        for j in range(4): add(sfx, at(1, 0.05) + j * 0.5, pluck(660 * 2 ** ([0, 3, 7, 12][j] / 12), 0.5, 0.05))
    if sc == 'aw_crash':
        add(sfx, at(0), rumble(S[0][1] - S[0][0], 95, 0.1)); add(sfx, at(0, 0.5), tone(1200, 0.12, 0.05)); add(sfx, at(0, 0.55), tone(1200, 0.12, 0.05))
        ti = S[1][0] + 0.30 * (S[1][1] - S[1][0])
        add(sfx, S[1][0], rumble(ti - S[1][0], 95, 0.18)); add(sfx, ti, impact(1.4)); add(sfx, ti, tone(42, 1.4, 0.5, 0.002, 1.2))
        crackle(ti, 1.2, 0.05, 80); add(sfx, ti + 0.1, rumble(end - ti, 160, 0.12)); add(sfx, ti + 0.1, gliss(400, 120, end - ti, 0.06))
    if sc == 'aw_cold':
        gust(at(0), end - at(0), 0.16)
        for j in range(3): add(sfx, at(0) + 0.5 + j * 0.8, tone(140, 0.2, 0.25, 0.003, 0.15))
        for j in range(25): add(sfx, at(1) + rng.random() * (S[1][1] - S[1][0]), tone(rng.uniform(3000, 4200), 0.04, 0.02, 0.001, 0.03))
    if sc == 'aw_radio':
        crackle(at(0, 0.2), S[0][1] - S[0][0], 0.03, 120); add(sfx, at(0, 0.3), tone(1000, 0.6, 0.03, 0.05, 0.4))
        add(sfx, at(1), stinger(ROOT / 2, 0.45)); add(sfx, at(1), impact(0.7)); add(sfx, at(1, 0.4), impact(0.5, 1.2))
    if sc == 'aw_decide':
        MUTE.append((at(0) - 0.1, end)); add(sfx, at(0), tone(55, end - at(0), 0.16, 0.8, 1.0)); add(sfx, at(0, 0.6), tone(82.4, 2.0, 0.06, 0.6, 1.2))
    if sc == 'aw_aval':
        add(sfx, at(0), pluck(660, 0.8, 0.06)); add(sfx, at(0, 0.38), rumble(2.6, 38, 0.45)); add(sfx, at(0, 0.38), rumble(2.6, 70, 0.25))
        add(sfx, at(0, 0.5), gliss(90, 40, 2.0, 0.3)); crackle(at(0, 0.45), 2.0, 0.05, 90)
        MUTE.append((at(1) - 0.1, end + 0.3)); add(sfx, at(1), tone(55, end - at(1) + 0.8, 0.14, 0.5, 1.0))
    if sc == 'aw_trek':
        gust(at(0), S[0][1] - S[0][0], 0.12)
        tt = at(0)
        while tt < at(1) - 0.2: add(sfx, tt, tone(70, 0.12, 0.25, 0.004, 0.1)); tt += 0.62
        for j in range(10): add(sfx, at(1) + j * (S[1][1] - S[1][0]) * 0.8 / 10, pluck(440 * 2 ** (j * 2 / 12), 0.4, 0.06))
        add(sfx, at(1, 0.85), stinger(ROOT * 1.5, 0.25))
    if sc == 'aw_verdict':
        tt = at(0)
        while tt < at(1) - 0.1: add(sfx, tt, tone(48, 0.07, 0.35, 0.002, 0.05)); tt += 0.075
        add(sfx, at(0, 0.1), stinger(ROOT * 2, 0.3))
        MUTE.append((at(1) - 0.1, at(2) - 0.1)); add(sfx, at(1), tone(110, S[1][1] - S[1][0] + 0.6, 0.05, 0.5, 0.8))
        add(sfx, at(2), stinger(ROOT, 0.35))
    # ---- Duel Rafale vs F-22 (sm_scenes12) ----
    def jetroar(t0, d, g=0.25): add(sfx, t0, rumble(d, 60, g)); add(sfx, t0, rumble(d, 125, g * 0.5)); add(sfx, t0, rumble(d, 410, g * 0.1))
    def point(t0, hi=True):
        add(sfx, t0, impact(0.8)); add(sfx, t0, stinger(ROOT * (2 if hi else 1.5), 0.32))
        for j in range(3): add(sfx, t0 + 0.08 * j, pluck(880 * 2 ** ([0, 4, 7][j] / 12), 0.4, 0.08))
    if sc.startswith('dv_') and sc not in ('dv_hook', 'dv_verdict'):
        add(sfx, at(0), whoosh(0.3)); add(sfx, at(0, 0.1), impact(0.9)); add(sfx, at(0, 0.15), tone(1320, 0.4, 0.06, 0.002, 0.35))
        point(at(3))
    if sc == 'dv_hook':
        jetroar(at(0), S[0][1] - S[0][0] + 0.5, 0.22); add(sfx, at(0, 0.6), impact(1.1)); add(sfx, at(0, 0.62), stinger(ROOT, 0.35))
        add(sfx, at(2), impact(0.9)); add(sfx, at(2), stinger(ROOT * 1.5, 0.3))
    if sc == 'dv_speed':
        jetroar(at(1), S[1][1] - S[1][0] + 0.3, 0.3); add(sfx, at(1), gliss(200, 600, 1.2, 0.05))
        jetroar(at(2), S[2][1] - S[2][0], 0.34); add(sfx, at(2), whoosh(0.35)); add(sfx, at(2, 0.1), gliss(150, 700, 1.6, 0.06))
    if sc == 'dv_stealth':
        tt = at(1)
        while tt < at(3) - 0.2: add(sfx, tt, tone(1480, 0.18, 0.06, 0.002, 0.16)); tt += 1.4
        add(sfx, at(1, 0.5), tone(2100, 0.05, 0.02)); add(sfx, at(2, 0.3), tone(1760, 0.25, 0.12, 0.002, 0.2)); add(sfx, at(2, 0.3), tone(880, 0.25, 0.08, 0.002, 0.2))
    if sc == 'dv_multi':
        for t0 in (28.0, 28.8, 29.57, 30.31, 31.67): add(sfx, t0, pluck(988, 0.3, 0.1)); add(sfx, t0, tone(140, 0.12, 0.2))
        jetroar(at(2), S[2][1] - S[2][0], 0.18)
    if sc == 'dv_export':
        for j in range(8): add(sfx, at(1) + 0.25 * j + 0.25, pluck(660 * 2 ** (j * 2 / 12), 0.35, 0.08))
        add(sfx, at(2, 0.1), tone(110, 0.3, 0.4, 0.002, 0.25)); add(sfx, at(2, 0.12), tone(2400, 0.06, 0.08)); add(sfx, at(2, 0.4), impact(0.8))
    if sc == 'dv_prod':
        for j in range(14): add(sfx, at(1) + j * 2.6 / 14, tone(700 + 30 * j, 0.05, 0.05, 0.002, 0.04))
        add(sfx, at(1) + 2.6, impact(1.0)); add(sfx, at(1) + 2.6, tone(90, 0.5, 0.3, 0.002, 0.4))
        add(sfx, at(2), gliss(300, 900, 1.6, 0.05))
    if sc == 'dv_verdict':
        add(sfx, at(0), impact(1.0)); add(sfx, at(0), stinger(ROOT * 2, 0.4)); jetroar(at(0), end - at(0), 0.16)
        add(sfx, at(1, 0.45), impact(0.8)); add(sfx, at(1, 0.45), stinger(ROOT * 1.5, 0.3)); add(sfx, at(2), stinger(ROOT, 0.35))
    # ---- Juliane Koepcke, LANSA 508 (sm_scenes13) ----
    def thunder(t0, g=1.0): add(sfx, t0, impact(1.1 * g)); add(sfx, t0, tone(38, 1.8, 0.5 * g, 0.004, 1.6)); add(sfx, t0 + 0.05, rumble(2.2, 52, 0.3 * g)); crackle(t0, 0.25, 0.05 * g, 30)
    def birds(t0, d, n=10, g=0.05):
        for j in range(n):
            tb = t0 + d * rng.random(); f = rng.uniform(2300, 3600)
            for m in range(int(rng.integers(2, 5))): add(sfx, tb + m * 0.09, gliss(f, f * rng.uniform(1.1, 1.3), 0.07, g, 0.004, 0.05))
    def insects(t0, d, g=0.012): add(sfx, t0, rumble(d, 4200, g)); add(sfx, t0, rumble(d, 3900, g * 0.7))
    if sc == 'jk_hook':
        add(sfx, at(0), rumble(S[0][1] - S[0][0] + 0.3, 70, 0.15)); thunder(at(0) + 0.25); add(sfx, at(0) + 0.9, impact(1.3)); add(sfx, at(0) + 0.9, gliss(2400, 160, 0.7, 0.1)); crackle(at(0) + 0.9, 0.6, 0.06, 60)
        wind(at(1), S[1][1] - S[1][0] + 0.2, 0.3); add(sfx, at(1), gliss(900, 260, S[1][1] - S[1][0], 0.06))
        add(sfx, at(2), stinger(ROOT, 0.35)); insects(at(2), end - at(2)); birds(at(2, 0.2), end - at(2), 4)
    if sc == 'jk_real':
        add(sfx, at(0), tone(220, S[0][1] - S[0][0] + 0.5, 0.04, 0.6, 0.6)); add(sfx, at(0, 0.6), pluck(880, 0.8, 0.06))
        for j in range(4): add(sfx, at(1, 0.1) + j * 0.55, pluck(660 * 2 ** ([0, 3, 7, 12][j] / 12), 0.5, 0.05))
        add(sfx, at(2), rumble(end - at(2), 140, 0.08)); add(sfx, at(2, 0.05), pluck(1046, 0.5, 0.06))
    if sc == 'jk_storm':
        add(sfx, at(0), rumble(end - at(0), 72, 0.16)); add(sfx, at(0), rumble(end - at(0), 145, 0.06)); thunder(at(0) + 0.4, 0.8); thunder(at(0) + 1.2, 0.6)
        L1 = S[1][1] - S[1][0]
        thunder(S[1][0] + 0.05, 1.3); crackle(S[1][0] + 0.30 * L1, end - S[1][0] - 0.30 * L1, 0.04, 90)
        tb = S[1][0] + 0.62 * L1; add(sfx, tb, impact(1.4)); add(sfx, tb, gliss(2600, 150, 0.8, 0.1)); wind(tb, end - tb + 0.4, 0.32)
    if sc == 'jk_fall':
        wind(at(0) - 0.1, S[0][1] - S[0][0] + 0.3, 0.36); add(sfx, at(0), gliss(1200, 300, S[0][1] - S[0][0], 0.05))
        for j in range(6): add(sfx, at(0) + j * (S[0][1] - S[0][0]) / 6, tone(1500 - 120 * j, 0.05, 0.05, 0.002, 0.04))
        add(sfx, S[0][1] + 0.05, impact(1.2)); crackle(S[0][1] + 0.05, 0.5, 0.06, 70)
        MUTE.append((at(1) - 0.05, at(1, 0.5))); heartbeat(at(1, 0.1), end, 62, 0.4); insects(at(1), end - at(1)); birds(at(1, 0.3), end - at(1), 5)
        add(sfx, at(1, 0.45), stinger(ROOT * 2, 0.25))
    if sc == 'jk_hurt':
        L0 = S[0][1] - S[0][0]
        for j in range(3): add(sfx, at(0) + j * L0 * 0.3 + 0.05, tone(140, 0.25, 0.3, 0.003, 0.2)); add(sfx, at(0) + j * L0 * 0.3 + 0.05, tone(1760, 0.12, 0.04, 0.002, 0.1))
        insects(at(1), end - at(1), 0.01); add(sfx, at(1), tone(55, end - at(1) + 0.5, 0.12, 0.4, 0.8))
        tt = at(1)
        while tt < end: add(sfx, tt, tone(990, 0.25, 0.04, 0.003, 0.22)); tt += 1 / 0.35 / 4
    if sc == 'jk_river':
        insects(at(0), end - at(0)); birds(at(0), end - at(0), 14)
        add(sfx, at(1), rumble(end - at(1), 300, 0.05))
        tt = at(1, 0.42)
        while tt < end: splash(tt, 0.2, 0.025, 14); tt += 0.62
    if sc == 'jk_found':
        insects(at(0), end - at(0)); birds(at(0), S[0][1] - S[0][0], 5)
        add(sfx, at(0, 0.05), pluck(660, 0.6, 0.06)); add(sfx, at(0, 0.3), stinger(ROOT * 1.5, 0.22))
        add(sfx, at(1), stinger(ROOT * 2, 0.3)); add(sfx, at(1, 0.3), tone(330, 0.5, 0.05, 0.01, 0.4))
        tt = at(1, 0.62)
        while tt < end: splash(tt, 0.25, 0.03, 18); tt += 0.8
    if sc == 'jk_later':
        for j in range(6): add(sfx, at(0, 0.05) + j * 0.4, pluck(523 * 2 ** ([0, 4, 7, 12, 7, 16][j] / 12), 0.6, 0.06))
        add(sfx, at(0, 0.55), stinger(ROOT * 2, 0.25)); birds(at(0), end - at(0), 6, 0.03)
    if sc == 'jk_verdict':
        add(sfx, at(0), stinger(ROOT * 2, 0.3)); add(sfx, at(0, 0.1), pluck(1320, 0.8, 0.06))
        MUTE.append((at(1) - 0.1, at(2) - 0.1)); add(sfx, at(1), tone(110, S[1][1] - S[1][0] + 0.6, 0.05, 0.5, 0.8))
        add(sfx, at(2), stinger(ROOT, 0.35))
    # ---- Ténérife 1977 (sm_scenes13) ----
    def idle(t0, d, g=0.1): add(sfx, t0, rumble(d, 118, g)); add(sfx, t0, rumble(d, 236, g * 0.35)); add(sfx, t0, tone(1900, d, g * 0.06, 0.4, 0.4))
    if sc == 'tf_hook':
        idle(at(0), end - at(0), 0.1); add(sfx, at(0), tone(73.4, end - at(0), 0.08, 1.0, 1.0))
        add(sfx, at(1), tone(1480, 0.5, 0.05, 0.01, 0.4)); add(sfx, at(1, 0.2), gliss(600, 900, 0.6, 0.04))
        add(sfx, at(2), impact(0.9)); add(sfx, at(2), stinger(ROOT, 0.35))
    if sc == 'tf_bomb':
        add(sfx, at(0, 0.05), pluck(880, 0.6, 0.06)); te = S[0][0] + 0.45 * (S[0][1] - S[0][0])
        add(sfx, te, impact(1.3)); add(sfx, te, tone(40, 1.6, 0.5, 0.002, 1.4)); crackle(te, 0.6, 0.05, 60)
        for j in range(5): add(sfx, at(1) + 0.5 + j * 0.5, gliss(500, 380, 0.5, 0.03)); add(sfx, at(1) + 0.5 + j * 0.5, pluck(660, 0.3, 0.04))
    if sc == 'tf_fog':
        for j in range(8): add(sfx, at(0, 0.1) + j * 0.3, tone(1320, 0.04, 0.05, 0.002, 0.03))
        idle(at(1), end - at(1), 0.12); add(sfx, at(2), tone(61.7, end - at(2), 0.1, 0.8, 0.8)); heartbeat(at(2, 0.3), end, 66, 0.3)
    if sc == 'tf_radio':
        def squelch(t0): crackle(t0, 0.25, 0.03, 25); add(sfx, t0, tone(1000, 0.08, 0.04, 0.002, 0.05))
        squelch(at(0)); crackle(at(0, 0.1), S[0][1] - S[0][0], 0.015, 40)
        squelch(at(1)); add(sfx, at(1, 0.1), pluck(1046, 0.4, 0.08)); add(sfx, S[1][0] + 0.40 * (S[1][1] - S[1][0]), tone(660, 0.3, 0.06, 0.005, 0.25))
        squelch(at(2)); tb = at(2) + 0.3
        add(sfx, tb, tone(2800, 3.0, 0.05, 0.05, 0.4)); add(sfx, tb, tone(2836, 3.0, 0.05, 0.05, 0.4)); crackle(tb, 3.0, 0.03, 120)
    if sc == 'tf_roll':
        add(sfx, at(0), spool(110, 260, S[0][1] - S[0][0], 0.22)); add(sfx, at(0), rumble(end - at(0), 60, 0.2)); add(sfx, at(0, 0.5), stinger(ROOT / 2, 0.35))
        add(sfx, at(1), spool(260, 330, S[1][1] - S[1][0], 0.22)); heartbeat(at(1), end, 132, 0.4)
        tm = S[1][0] + 0.45 * (S[1][1] - S[1][0]); add(sfx, tm, impact(0.9)); add(sfx, tm, gliss(400, 1400, 1.2, 0.07))
    if sc == 'tf_impact':
        L0 = S[0][1] - S[0][0]; th = S[0][0] + 0.45 * L0
        add(sfx, at(0), rumble(th - at(0), 60, 0.3)); crackle(S[0][0] + 0.2 * L0, 0.16 * L0, 0.05, 50)
        add(sfx, th, impact(1.6)); add(sfx, th, tone(36, 2.2, 0.6, 0.002, 2.0)); crackle(th, 1.0, 0.07, 120)
        add(sfx, S[0][0] + 0.75 * L0, impact(1.1, 1.4)); add(sfx, at(1), rumble(end - at(1) + 0.5, 90, 0.2)); crackle(at(1), end - at(1), 0.05, 90)
    if sc == 'tf_toll':
        MUTE.append((at(0) - 0.15, end + 0.2)); add(sfx, at(0), tone(55, end - at(0) + 0.8, 0.14, 0.5, 1.0)); add(sfx, at(1, 0.1), tone(110, 1.5, 0.04, 0.4, 1.0))
    if sc == 'tf_after':
        for j in range(4): add(sfx, at(0, 0.1) + j * 0.45, pluck(523 * 2 ** ([0, 4, 7, 12][j] / 12), 0.5, 0.05))
        add(sfx, S[0][0] + 0.5 * (S[0][1] - S[0][0]), tone(660, 0.4, 0.05)); add(sfx, at(1), stinger(ROOT, 0.35))
    # ---- Saint-Exupéry (sm_scenes14) ----
    def prop(t0, d, g=0.1): add(sfx, t0, rumble(d, 96, g)); add(sfx, t0, rumble(d, 192, g * 0.4))
    if sc == 'sx_hook':
        prop(at(0), S[0][1] - S[0][0] + 0.3, 0.1); add(sfx, at(0, 0.7), gliss(500, 300, 1.2, 0.04))
        for j in range(8): add(sfx, at(1) + j * (S[1][1] - S[1][0]) / 8, tone(1320, 0.04, 0.04, 0.002, 0.03))
        add(sfx, at(2), stinger(ROOT, 0.35))
    if sc == 'sx_takeoff':
        prop(at(0), S[0][1] - S[0][0], 0.09); add(sfx, at(0, 0.55), gliss(300, 1500, 1.4, 0.04))
        for j in range(4): t0 = S[1][0] + 0.15 * (S[1][1] - S[1][0]) + j * 0.7; add(sfx, t0, tone(2600, 0.03, 0.12, 0.001, 0.02)); add(sfx, t0 + 0.05, tone(1800, 0.05, 0.08, 0.001, 0.04))
    if sc == 'sx_vanish':
        tt = at(0)
        while tt < end: add(sfx, tt, tone(1000 if tt < at(0) + 1.2 else 700, 0.12, 0.08, 0.002, 0.1)); tt += 3.93
        MUTE.append((at(1) - 0.1, end)); add(sfx, at(1), tone(55, end - at(1) + 0.6, 0.12, 0.4, 0.8))
    if sc == 'sx_bracelet':
        add(sfx, at(0), rumble(S[0][1] - S[0][0], 300, 0.04)); add(sfx, at(0, 0.6), pluck(1568, 0.6, 0.08))
        add(sfx, at(1, 0.1), gliss(2400, 3600, 1.5, 0.03)); add(sfx, at(1, 0.4), pluck(1760, 1.0, 0.06)); add(sfx, at(1, 0.5), stinger(ROOT * 2, 0.22))
    if sc == 'sx_wreck':
        add(sfx, at(0), rumble(S[0][1] - S[0][0] + 0.3, 70, 0.14)); add(sfx, at(0), gliss(300, 90, S[0][1] - S[0][0], 0.05))
        for j in range(10): add(sfx, at(0) + rng.random() * (S[0][1] - S[0][0]), tone(rng.uniform(500, 900), 0.08, 0.03, 0.005, 0.06))
        add(sfx, at(1, 0.6), stinger(ROOT * 1.5, 0.3)); add(sfx, at(1, 0.6), impact(0.6))
        for j in range(3): add(sfx, at(2, 0.1) + j * 0.4, pluck(523 * 2 ** ([0, 4, 7][j] / 12), 0.6, 0.05))
    if sc == 'sx_claim':
        add(sfx, at(0), rumble(S[0][1] - S[0][0], 140, 0.1)); add(sfx, at(0, 0.1), stinger(ROOT / 2, 0.3))
        for j in range(5): add(sfx, at(1) + 0.2 + j * 0.3, tone(220 - 15 * j, 0.15, 0.08, 0.003, 0.12))
        add(sfx, at(1, 0.3), impact(0.7))
    if sc == 'sx_verdict':
        L0 = S[0][1] - S[0][0]
        for j in range(3): add(sfx, at(0) + j * L0 * 0.3, impact(0.5)); add(sfx, at(0) + j * L0 * 0.3, tone(660 + 110 * j, 0.3, 0.06, 0.002, 0.25))
        prop(at(1), S[1][1] - S[1][0], 0.06); add(sfx, at(2), stinger(ROOT, 0.35))


# ---------------- montage sonore ----------------
add(sfx, 0.04, impact(1.0)); add(sfx, 0.04, gliss(3000, 1200, 0.5, 0.08, 0.002, 0.4))            # titre « slam »
for i, s in enumerate(SEGS):
    if i > 0 and not CINEMA:
        add(sfx, s['t0'] - 1.0, riser(1.0, 0.07 if i < len(SEGS) - 2 else 0.12))
        add(sfx, s['t0'] - 0.05, whoosh(0.22)); add(sfx, s['t0'], impact(0.45, 1.0))
    elif i > 0:
        add(sfx, s['t0'] - 0.6, riser(0.6, 0.035)); add(sfx, s['t0'], impact(0.25, 1.4))
    for c0 in s['shots'][1:]:
        if CINEMA: continue
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
    t0 = ve + getattr(CFG, 'RECAP_DELAY', 0.9)
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
