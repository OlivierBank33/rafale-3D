"""Audio sinus uniquement pour gz_render -> gz/mix.wav (réacteur qui monte avec les G, cœur qui accélère, alarmes)."""
import json, math, sys
import numpy as np, soundfile as sf
sys.argv = ['x']; import importlib
R = importlib.import_module('gz_render')
SR = 48000; TOTAL = R.TOTAL; N = int(TOTAL * SR); t = np.arange(N) / SR
G = np.interp(t, np.arange(0, TOTAL, 0.02), [R.G_at(x) for x in np.arange(0, TOTAL, 0.02)])
mix = np.zeros(N)
def env(n, a=0.003, r=0.2):
    e = np.ones(n); na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na); return e * np.exp(-np.arange(n) / (r * SR))
def add(at, sig, g=1.0):
    i = int(at * SR)
    if i < 0 or i >= N: return
    j = min(N, i + len(sig)); mix[i:j] += g * sig[:j - i]
def sweep(f0, f1, d):
    n = int(d * SR); f = np.linspace(f0, f1, n); return np.sin(2 * np.pi * np.cumsum(f) / SR)
# réacteur : fondamental qui monte avec G (jusqu'à 9), coupé à l'éjection et pendant le traîneau
gj = np.clip(G, 1, 9); f = 70 + 18 * gj; ph = np.cumsum(2 * np.pi * f / SR)
jet = (np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.25 * np.sin(3.02 * ph) + 0.15 * np.sin(5.01 * ph))
jet_mask = np.where(t < 45.7, 1.0, 0.0) * np.where(t < 62, 1, 0)
mix += 0.10 * jet * jet_mask * (0.6 + 0.05 * gj)
# musique : nappe tendue
for fq, a in ((55, 0.06), (82.4, 0.04), (110, 0.03)):
    mix += a * np.sin(2 * np.pi * fq * t) * (t < 62)
# battements de cœur (accélèrent avec G, s'arrêtent pendant le voile noir)
bt = 3.6
while bt < 62:
    g = R.G_at(bt); bpm = 70 + 14 * min(g, 9)
    if not (31.0 <= bt < 33.6):
        th = sweep(70, 45, 0.16) * env(int(0.16 * SR), 0.002, 0.05)
        add(bt, th, 0.9 if g > 3 else 0.5); add(bt + 0.22, th, 0.6 if g > 3 else 0.35)
    bt += 60 / bpm
# whoosh à chaque palier
for (t0, g, *_x) in R.ST[1:]:
    add(t0 - 0.35, sweep(200, 900, 0.4) * np.sin(np.linspace(0, np.pi, int(0.4 * SR))) ** 2, 0.25)
    n = int(0.5 * SR); add(t0, (np.sin(2 * np.pi * 880 * np.arange(n) / SR) + 0.5 * np.sin(2 * np.pi * 1320 * np.arange(n) / SR)) * env(n, 0.002, 0.12), 0.18)
# alarme G (9 G)
at = 36.5
while at < 44.3:
    add(at, np.sin(2 * np.pi * 1000 * np.arange(int(0.12 * SR)) / SR) * env(int(0.12 * SR), 0.002, 0.08), 0.15); at += 0.35
# acouphène pendant le voile noir (sinus aigu)
m = (t >= 30.8) & (t < 34.0); mix += 0.05 * np.sin(2 * np.pi * 3200 * t) * m * np.clip((t - 30.8) / 0.5, 0, 1)
# éjection : coup sourd + fusée
add(45.4, sweep(160, 35, 0.9) * env(int(0.9 * SR), 0.001, 0.3), 1.4)
n = int(1.6 * SR); x = np.arange(n) / SR; add(45.4, (np.sin(2 * np.pi * 95 * x) + np.sin(2 * np.pi * 142 * x)) * np.exp(-x * 1.5), 0.5)
# traîneau-fusée : grondement + freinage
m = (t >= 50.5) & (t < 61.5); ph2 = np.cumsum(2 * np.pi * (60 + 10 * np.sin(t * 3)) / SR)
mix += 0.18 * (np.sin(ph2) + 0.6 * np.sin(2.01 * ph2) + 0.3 * np.sin(3.03 * ph2)) * m * np.clip((t - 50.5) / 0.5, 0, 1)
add(54.0, sweep(900, 120, 1.4) * env(int(1.4 * SR), 0.002, 0.6), 0.6)
# final : carillon
for k, fq in enumerate((523.3, 659.3, 784.0, 1046.5)):
    n = int(1.8 * SR); add(62.0 + k * 0.12, np.sin(2 * np.pi * fq * np.arange(n) / SR) * env(n, 0.003, 0.6), 0.3)
mix += 0.05 * sum(np.sin(2 * np.pi * fq * t) for fq in (130.8, 164.8, 196.0)) * (t >= 62) * np.clip((t - 62) / 1.0, 0, 1)
mix *= np.clip(t / 0.3, 0, 1) * np.clip((TOTAL - t) / 1.2, 0, 1)
sf.write('gz/mix.wav', (mix / np.abs(mix).max() * 0.9).astype(np.float32), SR); print('ok')
