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
