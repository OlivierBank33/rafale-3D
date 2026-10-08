"""Audio sinus uniquement pour bs_render (aucun bruit blanc) -> bs/mix.wav"""
import json, math
import numpy as np, soundfile as sf
E = json.load(open('bs/events.json')); TOTAL = E['total']; SR = 48000; N = int(TOTAL * SR)
t = np.arange(N) / SR
mus = np.zeros(N); sfx = np.zeros(N)


def env(n, a=0.004, r=0.3):
    e = np.ones(n); na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na); return e * np.exp(-np.arange(n) / (r * SR))


def add(buf, at, sig, g=1.0):
    i = int(at * SR)
    if i >= len(buf) or i < 0: return
    j = min(len(buf), i + len(sig)); buf[i:j] += g * sig[:j - i]


def sweep(f0, f1, d):
    n = int(d * SR); f = np.linspace(f0, f1, n); return np.sin(2 * np.pi * np.cumsum(f) / SR)


HUD = E['hudson']
# drone + accords par niveau
lv = E['levels']; chords = [[55, 82.4, 110], [58.3, 87.3, 116.5], [61.7, 92.5, 123.5], [65.4, 98, 130.8], [69.3, 103.8, 138.6]]
inten = np.full(N, 0.4)
for i, (a, b) in enumerate(lv):
    m = (t >= a - 0.5) & (t < (lv[i + 1][0] - 0.5 if i + 1 < len(lv) else HUD))
    seg = sum(np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t) for f in chords[i])
    mus += 0.05 * seg * m * (0.7 + 0.3 * i / 4)
    inten[m] = 0.5 + 0.12 * i
pre = t < lv[0][0] - 0.5
mus += 0.05 * sum(np.sin(2 * np.pi * f * t) for f in (55, 82.4, 110)) * pre
for (a, b) in E['facts']:
    m = (t >= a) & (t < b); mus[m] *= 0.45
# pulsation qui accélère
bt = 3.0; kick = sweep(90, 40, 0.25) * env(int(0.25 * SR), 0.002, 0.07)
while bt < HUD:
    infact = any(a <= bt < b for a, b in E['facts'])
    if not infact: add(mus, bt, kick, 0.8)
    li = sum(1 for a, b in lv if bt >= a - 0.5) - 1
    bt += [0.75, 0.6, 0.5, 0.4, 0.3][max(0, li)]
# ronronnement moteur (s'arrête vers 46 s)
hum_f = np.where(t < 46, 1.0, np.clip(1 - (t - 46) / 3, 0.25, 1))
ph = np.cumsum(2 * np.pi * 120 * hum_f / SR)
hum = (np.sin(ph) + 0.4 * np.sin(2 * ph) + 0.2 * np.sin(3.01 * ph)) * np.where(t < HUD, 1, 0) * np.clip((49 - t) / 3, 0, 1)
sfx += 0.05 * hum
# impacts
last = -1
for (te, kind, li) in E['events']:
    if kind == 'pass':
        add(sfx, te - 0.3, sweep(300, 900, 0.35) * np.sin(np.linspace(0, np.pi, int(0.35 * SR))) ** 2, 0.08); continue
    if te - last < 0.035: continue
    last = te
    g = 1.0 if li < 2 else (0.7 if li < 4 else 0.45)
    add(sfx, te, sweep(140, 45, 0.35) * env(int(0.35 * SR), 0.001, 0.09), g)
    add(sfx, te, np.sin(2 * np.pi * 420 * np.arange(int(0.08 * SR)) / SR) * env(int(0.08 * SR), 0.001, 0.02), 0.5 * g)
    if kind == 'eng':
        n = int(0.9 * SR); x = np.arange(n) / SR
        ring = (np.sin(2 * np.pi * 1180 * x) + 0.6 * np.sin(2 * np.pi * 1770 * x) + 0.3 * np.sin(2 * np.pi * 2650 * x)) * env(n, 0.001, 0.18)
        add(sfx, te, ring, 0.35)
    if li == 0:
        add(sfx, te - 0.75, sweep(200, 1200, 0.75) * np.linspace(0, 1, int(0.75 * SR)) ** 2, 0.25)
# alarme « master caution »
at = 36.0
while at < 49.5:
    b = np.sin(2 * np.pi * (880 if int(at * 2) % 2 == 0 else 660) * np.arange(int(0.18 * SR)) / SR) * env(int(0.18 * SR), 0.003, 0.12)
    add(sfx, at, b, 0.22); at += 0.5
# Hudson : nappe calme + carillon
m = t >= HUD
pad = sum(np.sin(2 * np.pi * f * t) for f in (130.8, 164.8, 196.0, 246.9)) * np.clip((t - HUD) / 1.5, 0, 1) * m
mus += 0.04 * pad
for k, f in enumerate((523.3, 659.3, 784.0, 1046.5)):
    n = int(1.6 * SR); add(sfx, HUD + 10.5 + k * 0.12, np.sin(2 * np.pi * f * np.arange(n) / SR) * env(n, 0.003, 0.5), 0.25)
mix = 0.55 * mus / (np.abs(mus).max() + 1e-9) + 0.75 * sfx / (np.abs(sfx).max() + 1e-9)
mix *= np.clip(t / 0.3, 0, 1) * np.clip((TOTAL - t) / 1.0, 0, 1)
sf.write('bs/mix.wav', (mix / np.abs(mix).max() * 0.9).astype(np.float32), SR); print('ok')
