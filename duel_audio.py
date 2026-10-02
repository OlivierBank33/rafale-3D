"""Musique + bruitages du duel (numpy) -> /home/claude/r3d/duel/bed.wav (sans voix, ducking sur la timeline)."""
import json, math, sys
import numpy as np
import soundfile as sf
sys.path.insert(0, '/home/claude/pipe')
from duel_script import SCENES

D = '/home/claude/r3d/duel/'
TM = json.load(open(D + 'timing.json'))
SR = 48000; TOTAL = TM['total']; N = int(TOTAL * SR) + SR
t = np.arange(N) / SR
rng = np.random.default_rng(3)
starts, durs = TM['starts'], TM['durs']
sc = {s['scene']: i for i, s in enumerate(SCENES)}
T = lambda name: starts[sc[name]]
U = lambda name, u: starts[sc[name]] + durs[sc[name]] * u


def env(n, a=0.005, r=0.3):
    e = np.ones(n); na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na)
    e *= np.exp(-np.arange(n) / (r * SR)); return e


def add(buf, at, sig, g=1.0):
    i = int(at * SR)
    if i >= len(buf): return
    j = min(len(buf), i + len(sig)); buf[i:j] += g * sig[:j - i]


def lp(x, k):
    return np.convolve(x, np.ones(k) / k, mode='same')


music = np.zeros(N); sfx = np.zeros(N)
# --- drone + pad ---
swell = 0.6 + 0.4 * np.sin(2 * np.pi * t / 9)
music += 0.30 * np.sin(2 * np.pi * 41.2 * t) * swell + 0.18 * np.sin(2 * np.pi * 61.7 * t) * swell
music += 0.10 * np.sin(2 * np.pi * 30.9 * t) * swell  # sub propre (plus de bruit blanc)
chords = {'hook': [82.4, 98.0, 123.5], 'vitesse': [65.4, 82.4, 98.0], 'furtif': [73.4, 87.3, 110.0], 'poly': [82.4, 98.0, 123.5],
          'reel': [65.4, 82.4, 98.0], 'duel': [77.8, 92.5, 116.5], 'doute': [77.8, 92.5, 116.5], 'verdict': [82.4, 103.8, 123.5]}
for i, s in enumerate(SCENES):
    a0 = starts[i] - 0.3; a1 = starts[i + 1] - 0.3 if i + 1 < len(SCENES) else TOTAL
    m = (t >= a0) & (t < a1)
    seg = np.zeros(N)
    for f in chords[s['scene']]:
        ph = 2 * np.pi * f * t
        seg += np.sin(ph) + 0.35 * np.sin(2 * ph) + 0.15 * np.sin(3 * ph)
    fade = np.clip((t - a0) / 0.4, 0, 1) * np.clip((a1 - t) / 0.4, 0, 1)
    music += 0.06 * seg * fade * m
# --- pulsation (s'arrête pendant le doute, double pendant le duel HUD) ---
kick = np.sin(2 * np.pi * (55 * np.arange(int(0.3 * SR)) / SR)) * env(int(0.3 * SR), 0.002, 0.09)
bt = 1.25
while bt < TOTAL - 1:
    if T('doute') - 0.3 <= bt < T('verdict') - 0.3:
        bt += 0.625; continue
    add(music, bt, kick, 0.9)
    bt += 0.3125 if U('duel', 0.35) <= bt < T('doute') - 0.3 else 0.625
# --- montée avant le VS et avant le dernier round ---
for (a, b) in [(0.0, 1.2), (T('duel') - 1.6, T('duel') - 0.3)]:
    n = int((b - a) * SR); x = np.arange(n) / SR
    f = 200 + 1600 * (x / (b - a)) ** 2
    rise = np.sin(2 * np.pi * np.cumsum(f) / SR) * (x / (b - a)) ** 2 * 0.25
    add(sfx, a, rise)


def boom(g=1.0):
    n = int(1.2 * SR); x = np.arange(n) / SR
    f = 40 + 80 * np.exp(-x * 6)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 2.5)
    s += np.sin(2 * np.pi * np.cumsum(f * 2.01) / SR) * np.exp(-x * 9) * 0.3
    return s * g


def whoosh(d=0.6, g=0.5):
    """balayage sinusoïdal grave->aigu, sans bruit"""
    n = int(d * SR); x = np.arange(n) / SR
    f = 120 + 500 * (x / d) ** 1.5
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * x / d) ** 2 * g * 0.5


def blip(f, d=0.12, g=0.4):
    n = int(d * SR); x = np.arange(n) / SR
    return np.sin(2 * np.pi * f * x) * env(n, 0.002, d / 3) * g


add(sfx, 1.2, boom(1.0))
for i in range(1, len(SCENES)):
    add(sfx, starts[i] - 0.45, whoosh())
# changements de score
prev = (0, 0)
for i, s in enumerate(SCENES):
    if s['score'] != prev:
        tc = starts[i] + durs[i] * 0.86
        add(sfx, tc, boom(0.55)); add(sfx, tc, blip(1320, 0.5, 0.25)); add(sfx, tc + 0.08, blip(1760, 0.5, 0.2))
    prev = s['score']
# radar : ping à chaque passage du balayage sur le Rafale
a0, a1 = T('furtif') - 0.3, T('poly') - 0.3
tt = a0
while tt < a1:
    sw = (tt * 2.0) % (2 * math.pi)
    tgt = math.radians(205)
    dt = ((tgt - sw) % (2 * math.pi)) / 2.0
    tt += dt
    if tt < a1: add(sfx, tt, blip(980, 0.35, 0.35))
    tt += 0.05
# pastilles qui apparaissent
for name, us in [('poly', [0.2, 0.28, 0.36, 0.44, 0.66]), ('reel', [0.12, 0.18, 0.24, 0.30, 0.5, 0.66]), ('furtif', [0.2, 0.5])]:
    for u in us:
        add(sfx, U(name, u), blip(2400, 0.05, 0.3)); add(sfx, U(name, u), kick[:4000], 0.4)
# verrouillage HUD
lt = U('duel', 0.45); end = U('duel', 0.9)
while lt < end:
    p = (lt - U('duel', 0.45)) / (end - U('duel', 0.45))
    add(sfx, lt, blip(1600, 0.06, 0.28)); lt += 0.45 - 0.37 * p
n = int((T('doute') - 0.3 - end) * SR)
if n > 0: add(sfx, end, np.sin(2 * np.pi * 1600 * np.arange(n) / SR) * 0.18)
add(sfx, U('duel', 0.32), boom(0.6))
add(sfx, T('doute') - 0.3, boom(0.7))
add(sfx, U('verdict', 0.5), boom(0.9))

# --- ducking sur la voix (intervalles de parole) ---
duck = np.ones(N)
for s0, d in zip(starts, durs):
    duck[(t > s0 - 0.12) & (t < s0 + d + 0.2)] = 0.35
k = int(0.12 * SR); duck = np.convolve(duck, np.ones(k) / k, mode='same')
bed = music * duck + sfx * (0.55 + 0.45 * duck)
bed = bed[:int(TOTAL * SR)]
bed = bed / (np.abs(bed).max() + 1e-9) * 0.9
sf.write(D + 'bed_raw.wav', bed.astype(np.float32), SR)
print('ok', len(bed) / SR)
