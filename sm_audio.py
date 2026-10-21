"""Ambiance des histoires STICKMAN (sinus uniquement) : DL=dl/<slug> python3 sm_audio.py -> music.wav, sfx.wav, voice.wav (guide)."""
import json, os, numpy as np, soundfile as sf
D = os.environ.get('DL', 'dl/sm_ep01').rstrip('/') + '/'
TM = json.load(open(D + 'timeline.json')); SEGS = TM['seg']; SR = 48000; TOTAL = TM['total']; N = int(TOTAL * SR) + SR
t = np.arange(N) / SR
def env(n, a=0.01, r=0.3):
    e = np.ones(n); na = max(1, min(n // 2, int(a * SR))); nr = max(1, min(n // 2, int(r * SR))); e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr); return e
def add(buf, at, sig, g=1.0):
    i = int(at * SR); j = min(len(buf), i + len(sig))
    if i < len(buf) and j > i: buf[i:j] += sig[:j - i] * g
def tone(f, d, g=0.3, a=0.005, r=0.1):
    n = int(d * SR); x = np.arange(n) / SR; return np.sin(2 * np.pi * f * x) * env(n, a, r) * g
def hit(g=1.0):
    n = int(1.6 * SR); x = np.arange(n) / SR; f = 70 * np.exp(-x * 2.5) + 38
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 2.8) * g
MOOD = dict(cockpit=(55, 65.4, 82.4), handle=(49, 58.3, 73.4), ocean=(43.7, 55, 65.4), map=(46.2, 55, 69.3), radio=(49, 61.7, 73.4), think=(41.2, 49, 61.7), choice=(55, 65.4, 82.4))
music = np.zeros(N)
for s in SEGS:
    i0 = int(s['t0'] * SR); i1 = min(N, int(s['end'] * SR)); n = i1 - i0; x = t[i0:i1]
    sig = np.zeros(n)
    for k, f in enumerate(MOOD.get(s['scene'], (55, 65.4, 82.4))):
        sig += np.sin(2 * np.pi * f * x + k) * (0.5 / (k + 1)) * (1 + 0.25 * np.sin(2 * np.pi * 0.13 * x + k))
        sig += np.sin(2 * np.pi * f * 2.003 * x) * 0.08
    music[i0:i1] += sig * env(n, 0.4, 0.4)
    # pulsation « cœur » sur les scènes de tension
    if s['scene'] in ('cockpit', 'map', 'think', 'choice', 'tuc', 'hypox', 'hold', 'copilot'):
        bpm = 70 if s['scene'] != 'choice' else 84; tt = s['vt']
        while tt < s['end'] - 0.3:
            add(music, tt, tone(48, 0.18, 0.55, 0.002, 0.15)); add(music, tt + 0.22, tone(44, 0.16, 0.4, 0.002, 0.14)); tt += 60 / bpm
sfx = np.zeros(N)
for s in SEGS[1:]: add(sfx, s['t0'], hit(0.7))
c0 = SEGS[0]; tt = c0['vt'] + c0['dur'] * 0.6
while c0['scene'] == 'cockpit' and tt < c0['end']:
    add(sfx, tt, tone(880, 0.18, 0.25)); add(sfx, tt + 0.2, tone(660, 0.18, 0.25)); tt += 0.4
for s in SEGS:
    if s['scene'] == 'handle':
        add(sfx, s['vt'] + s['dur'] * 0.36, hit(0.5)); add(sfx, s['vt'] + s['dur'] * 0.55, tone(180, 1.2, 0.2, 0.05, 0.8))
    if s['scene'] in ('cabin', 'blowout'):
        add(sfx, s['vt'] + (s['dur'] + 0.3) * (0.42 if s['scene'] == 'cabin' else 0.35), hit(1.0))
        add(sfx, s['vt'] + (s['dur'] + 0.3) * (0.42 if s['scene'] == 'cabin' else 0.35) + 0.05, tone(90, 1.5, 0.4, 0.002, 1.2))
    if s['scene'] == 'tuc':
        tt = s['vt'] + (s['dur'] + 0.3) * 0.35
        while tt < s['end'] - 0.2: add(sfx, tt, tone(1000, 0.06, 0.18)); tt += 0.5
    if s['scene'] == 'verdict': add(sfx, s['t0'] + 0.1, tone(880, 0.6, 0.2)); add(sfx, s['t0'] + 0.25, tone(1320, 0.8, 0.2))
    if s['scene'] == 'radio':
        for k in range(10): add(sfx, s['vt'] + 0.1 + k * 0.07, tone(1400 + 300 * (k % 3), 0.05, 0.12))
    if s['scene'] == 'choice':
        for k in range(2): add(sfx, s['vt'] + s['dur'] * (0.12 + 0.12 * k), tone(1320 + 440 * k, 0.4, 0.2, 0.002, 0.35))
voice = np.zeros(N)
for s in SEGS:
    v, sr_ = sf.read(D + s['k'] + '.wav')
    if v.ndim > 1: v = v.mean(1)
    if sr_ != SR: v = np.interp(np.arange(int(len(v) * SR / sr_)) * sr_ / SR, np.arange(len(v)), v)
    add(voice, s['vt'], v)
for name, x in (('voice', voice), ('music', music), ('sfx', sfx)):
    x = x[:int(TOTAL * SR)]; sf.write(D + name + '.wav', (x / (np.abs(x).max() + 1e-9) * 0.9).astype(np.float32), SR)
print('ok', TOTAL)
