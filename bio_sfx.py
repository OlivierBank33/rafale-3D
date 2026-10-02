"""Bruitages propres (sinus uniquement, zéro bruit blanc) pour une bio : python3 bio_sfx.py <dossier> [scènes_moteur,...]"""
import json, sys, numpy as np, soundfile as sf
D = sys.argv[1]; ENG = sys.argv[2].split(',') if len(sys.argv) > 2 else ['avion', 'carte']
SR = 48000; TL = json.load(open(f'{D}/timeline.json')); SEG = TL['seg']; TOTAL = TL['total']
N = int(TOTAL * SR) + SR; sfx = np.zeros(N)
def add(at, sig, g=1.0):
    i = int(at * SR); j = min(N, i + len(sig))
    if i < N: sfx[i:j] += g * sig[:j - i]
def sweep(d=0.7, f0=150, f1=700, g=0.25):
    x = np.arange(int(d * SR)) / SR; f = f0 + (f1 - f0) * (x / d) ** 1.5
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * x / d) ** 2 * g
def thump(g=0.6):
    x = np.arange(SR) / SR; f = 45 + 70 * np.exp(-x * 7)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 3) * g
for s in SEG[1:]: add(s['t0'] - 0.35, sweep())
for s in SEG:
    if s['scene'] in ENG:
        x = np.arange(int((s['end'] - s['t0']) * SR)) / SR
        e = (np.sin(2 * np.pi * 92 * x) + 0.5 * np.sin(2 * np.pi * 184 * x)) * (0.7 + 0.3 * np.sin(2 * np.pi * 23 * x))
        add(s['t0'], e * np.minimum(1, x / 0.8) * np.minimum(1, (x[-1] - x) / 0.8), 0.12)
add(SEG[0]['vt'] - 0.2, thump())
sfx = sfx[:int(TOTAL * SR)]
sf.write(f'{D}/sfx.wav', (sfx / np.abs(sfx).max() * 0.9).astype(np.float32), SR); print('ok', TOTAL)
