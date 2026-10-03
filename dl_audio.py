"""Musique + bruitages d'un duel générique (sinus uniquement) : DL=dl/<slug> python3 dl_audio.py -> music.wav, sfx.wav, voice.wav (guide)."""
import json, math, sys
import numpy as np
import soundfile as sf
import os
D = os.environ.get('DL', 'dl/rafale_typhoon').rstrip('/') + '/'
TM = json.load(open(D + 'timeline.json')); SEGS = TM['seg']
SR = 48000; TOTAL = TM['total']; N = int(TOTAL * SR) + SR
t = np.arange(N) / SR
starts = [x['vt'] for x in SEGS]; durs = [x['dur'] for x in SEGS]
SCENES = [dict(scene=x['scene'], score=tuple(x['score'])) for x in SEGS]
LASTR = max(i for i, x in enumerate(SEGS) if x['scene'] not in ('hook', 'verdict'))


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
CH = [[82.4, 98.0, 123.5], [65.4, 82.4, 98.0], [73.4, 87.3, 110.0], [82.4, 98.0, 123.5], [65.4, 82.4, 98.0], [77.8, 92.5, 116.5], [82.4, 103.8, 123.5]]
for i, s in enumerate(SEGS):
    a0 = s['t0'] - 0.3 if i else 0; a1 = s['end'] - 0.3 if i + 1 < len(SEGS) else TOTAL
    m = (t >= a0) & (t < a1); seg = np.zeros(N)
    ch = CH[-1] if s['scene'] == 'verdict' else CH[i % (len(CH) - 1)]
    for f in ch:
        ph = 2 * np.pi * f * t; seg += np.sin(ph) + 0.35 * np.sin(2 * ph) + 0.15 * np.sin(3 * ph)
    fade = np.clip((t - a0) / 0.4, 0, 1) * np.clip((a1 - t) / 0.4, 0, 1)
    music += 0.06 * seg * fade * m
# pulsation : double tempo pendant le dernier round
kick = np.sin(2 * np.pi * (55 * np.arange(int(0.3 * SR)) / SR)) * env(int(0.3 * SR), 0.002, 0.09)
lr0, lr1 = SEGS[LASTR]['t0'], SEGS[LASTR]['end']
bt = 1.25
while bt < TOTAL - 1:
    add(music, bt, kick, 0.9)
    bt += 0.3125 if lr0 + 1.0 <= bt < lr1 - 0.3 else 0.625
# montées (sinus) avant le VS et avant le dernier round
for (a, b) in [(0.0, 1.2), (lr0 - 1.4, lr0 - 0.1)]:
    n = int((b - a) * SR); x = np.arange(n) / SR
    f = 200 + 1600 * (x / (b - a)) ** 2
    add(sfx, a, np.sin(2 * np.pi * np.cumsum(f) / SR) * (x / (b - a)) ** 2 * 0.25)


def boom(g=1.0):
    n = int(1.2 * SR); x = np.arange(n) / SR
    f = 40 + 80 * np.exp(-x * 6)
    s_ = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 2.5)
    s_ += np.sin(2 * np.pi * np.cumsum(f * 2.01) / SR) * np.exp(-x * 9) * 0.3
    return s_ * g


def whoosh(d=0.6, g=0.5):
    n = int(d * SR); x = np.arange(n) / SR
    f = 120 + 500 * (x / d) ** 1.5
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * x / d) ** 2 * g * 0.5


def blip(f, d=0.12, g=0.4):
    n = int(d * SR); x = np.arange(n) / SR
    return np.sin(2 * np.pi * f * x) * env(n, 0.002, d / 3) * g


add(sfx, 1.2, boom(1.0))
for s in SEGS[1:]:
    add(sfx, s['t0'] - 0.45, whoosh())
prev = (0, 0)
for s in SEGS:
    if tuple(s['score']) != prev:
        tc = s['vt'] + s['dur'] * 0.86
        add(sfx, tc, boom(0.55)); add(sfx, tc, blip(1320, 0.5, 0.25)); add(sfx, tc + 0.08, blip(1760, 0.5, 0.2))
    prev = tuple(s['score'])
    if s['scene'] in ('chips', 'list', 'counters'):
        for u in (0.2, 0.3, 0.4, 0.5, 0.62):
            add(sfx, s['vt'] + s['dur'] * u, blip(2400, 0.05, 0.25))
    if s['scene'] == 'radar':
        tt = s['t0']
        while tt < s['end']:
            add(sfx, tt, blip(980, 0.35, 0.3)); tt += np.pi
add(sfx, SEGS[-1]['vt'] + SEGS[-1]['dur'] * 0.5, boom(0.9))

# voix guide (Kokoro recalé)
voice = np.zeros(N)
for s in SEGS:
    v, sr_ = sf.read(D + s['k'] + '.wav')
    if v.ndim > 1: v = v.mean(1)
    if sr_ != SR: v = np.interp(np.arange(int(len(v) * SR / sr_)) * sr_ / SR, np.arange(len(v)), v)
    add(voice, s['vt'], v)
for name, x in (('voice', voice), ('music', music), ('sfx', sfx)):
    x = x[:int(TOTAL * SR)]
    sf.write(D + name + '.wav', (x / (np.abs(x).max() + 1e-9) * 0.9).astype(np.float32), SR)
print('ok', TOTAL)
