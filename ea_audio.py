"""Musique + bruitages + voix guide pour la bio Earhart (ea/). Sans bruit blanc : uniquement des sinus."""
import json, numpy as np, soundfile as sf

SR = 48000
TL = json.load(open('ea/timeline.json')); SEG = TL['seg']; TOTAL = TL['total']
N = int(TOTAL * SR) + SR
t = np.arange(N) / SR


def add(buf, at, sig, g=1.0):
    i = int(at * SR)
    if i >= len(buf): return
    j = min(len(buf), i + len(sig)); buf[i:j] += g * sig[:j - i]


def note(f, d=2.5, g=0.2):
    n = int(d * SR); x = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * x) + 0.4 * np.sin(4 * np.pi * f * x) * np.exp(-x * 3) + 0.15 * np.sin(6 * np.pi * f * x) * np.exp(-x * 5)
    a = np.minimum(1, x / 0.006)
    return s * a * np.exp(-x * 1.6) * g


# --- voix guide ---
voice = np.zeros(N)
for s in SEG:
    v, sr = sf.read(f"ea/{s['k']}.wav")
    if v.ndim > 1: v = v.mean(1)
    if sr != SR: v = np.interp(np.arange(int(len(v) * SR / sr)) * sr / SR, np.arange(len(v)), v)
    add(voice, s['vt'], v)

# --- musique : nappe + arpège piano, plus sombre sur carte / mystere ---
CH = {'hook': [110.0, 130.8, 164.8], 'portrait': [130.8, 164.8, 196.0], 'journal': [98.0, 123.5, 146.8], 'avion': [130.8, 164.8, 196.0],
      'carte': [110.0, 130.8, 155.6], 'atterro': [146.8, 185.0, 220.0], 'gloire': [130.8, 164.8, 196.0], 'mystere': [103.8, 123.5, 155.6],
      'outro': [110.0, 130.8, 164.8]}
music = np.zeros(N)
for s in SEG:
    a0, a1 = s['t0'], s['end']; m = (t >= a0) & (t < a1)
    fade = np.clip((t - a0) / 0.6, 0, 1) * np.clip((a1 - t) / 0.6, 0, 1)
    pad = sum(np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t) for f in CH[s['scene']])
    music += 0.05 * pad * fade * m
    arp = [f * 2 for f in CH[s['scene']]] + [CH[s['scene']][1] * 4]
    step = 0.5 if s['scene'] not in ('carte', 'mystere') else 0.75
    tt, i = a0 + 0.2, 0
    while tt < a1 - 0.4:
        add(music, tt, note(arp[i % len(arp)], 2.0, 0.12)); tt += step; i += 1
music += 0.08 * np.sin(2 * np.pi * 55 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * t / 8))

# --- bruitages ---
sfx = np.zeros(N)


def sweep(d=0.7, f0=150, f1=700, g=0.25):
    n = int(d * SR); x = np.arange(n) / SR
    f = f0 + (f1 - f0) * (x / d) ** 1.5
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * x / d) ** 2 * g


for s in SEG[1:]:
    add(sfx, s['t0'] - 0.35, sweep())
# moteur à hélice (sinus modulé) pendant avion + carte
for s in SEG:
    if s['scene'] in ('avion', 'carte'):
        n = int((s['end'] - s['t0']) * SR); x = np.arange(n) / SR
        eng = (np.sin(2 * np.pi * 92 * x) + 0.5 * np.sin(2 * np.pi * 184 * x)) * (0.7 + 0.3 * np.sin(2 * np.pi * 23 * x))
        eng *= np.minimum(1, x / 0.8) * np.minimum(1, (x[-1] - x) / 0.8)
        add(sfx, s['t0'], eng, 0.12)
# impact grave sur le titre et sur le mystère
def thump(g=0.6):
    n = int(1.0 * SR); x = np.arange(n) / SR; f = 45 + 70 * np.exp(-x * 7)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 3) * g
add(sfx, SEG[0]['vt'] - 0.2, thump())
for s in SEG:
    if s['scene'] == 'mystere': add(sfx, s['t0'], thump(0.7))

for name, x in (('voice', voice), ('music', music), ('sfx', sfx)):
    x = x[:int(TOTAL * SR)]
    sf.write(f'ea/{name}.wav', (x / (np.abs(x).max() + 1e-9) * 0.9).astype(np.float32), SR)
print('ok', TOTAL)
