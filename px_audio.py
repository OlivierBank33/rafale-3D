"""Musique + bruitages + voix guide pour « avions les plus chers » (px/). Sinus uniquement, zéro bruit blanc."""
import json, numpy as np, soundfile as sf

SR = 48000
TL = json.load(open('px/timeline.json')); SEG = TL['seg']; TOTAL = TL['total']
N = int(TOTAL * SR) + SR; t = np.arange(N) / SR
f = lambda m: 440 * 2 ** ((m - 69) / 12)


def add(buf, at, sig, g=1.0):
    i = int(at * SR)
    if i < 0: sig = sig[-i:]; i = 0
    if i >= len(buf): return
    j = min(len(buf), i + len(sig)); buf[i:j] += g * sig[:j - i]


# voix guide
voice = np.zeros(N)
for s in SEG:
    v, sr = sf.read(f"px/{s['k']}.wav")
    if v.ndim > 1: v = v.mean(1)
    if sr != SR: v = np.interp(np.arange(int(len(v) * SR / sr)) * sr / SR, np.arange(len(v)), v)
    add(voice, s['vt'], v)

# musique : groove « luxe / argent » qui monte en intensité au fil des avions
music = np.zeros(N); bpm = 100; beat = 60 / bpm
chords = [[57, 60, 64], [53, 57, 60], [55, 59, 62], [52, 55, 59]]
nb = int(TOTAL / beat) + 1
pstarts = [s['t0'] for s in SEG if s['k'].startswith('p')]
def level(tt):      # 0 au début -> 1 au B-2
    return min(1.0, sum(tt >= p for p in pstarts) / 8)
for b in range(nb):
    tb = b * beat; ch = chords[(b // 8) % 4]; lv = level(tb)
    L = int(beat * SR * 1.05); x = np.arange(L) / SR
    env = np.minimum(1, x / 0.01) * np.exp(-x * 2.2)
    if b % 2 == 0:   # basse
        add(music, tb, np.sin(2 * np.pi * f(ch[0] - 24) * x) * np.exp(-x * 3) * 0.55)
    # kick
    if b % 2 == 0 or lv > 0.6:
        kx = np.arange(int(0.28 * SR)) / SR
        add(music, tb, np.sin(2 * np.pi * np.cumsum(45 + 90 * np.exp(-kx * 30)) / SR) * np.exp(-kx * 10) * (0.35 + 0.35 * lv))
    # accord plaqué (piano doux)
    if b % 4 in (0, 3):
        sig = sum(np.sin(2 * np.pi * f(m) * x) + 0.3 * np.sin(4 * np.pi * f(m) * x) * np.exp(-x * 4) for m in ch)
        add(music, tb, sig * env * 0.08)
    # pizz aigu quand ça monte
    if lv > 0.3 and b % 2 == 1:
        m = ch[(b // 2) % 3] + 12; xx = np.arange(int(0.25 * SR)) / SR
        add(music, tb, np.sin(2 * np.pi * f(m) * xx) * np.exp(-xx * 14) * 0.10 * lv)
music *= np.clip((TOTAL - t) / 2.5, 0, 1)

# bruitages
sfx = np.zeros(N)
def sweep(d=0.8, f0=140, f1=650, g=0.3):
    x = np.arange(int(d * SR)) / SR; fr = f0 + (f1 - f0) * (x / d) ** 1.5
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.sin(np.pi * x / d) ** 2 * g
def thump(g=0.6):
    x = np.arange(SR) / SR; fr = 42 + 70 * np.exp(-x * 7)
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-x * 3.5) * g
def coin(at, g=0.18):   # « cha-ching » en sinus
    for k, (m, dt) in enumerate([(88, 0.0), (93, 0.07)]):
        x = np.arange(int(0.5 * SR)) / SR
        add(sfx, at + dt, (np.sin(2 * np.pi * f(m) * x) + 0.4 * np.sin(2 * np.pi * f(m) * 2.76 * x)) * np.exp(-x * 9) * g)
for s in SEG:
    if not s['k'].startswith('p'): continue
    t0 = s['t0']
    add(sfx, t0 + 0.05, sweep())                 # arrivée de l'avion
    add(sfx, t0 + 2.0, sweep(0.6, 600, 160, 0.18))  # il se pose dans l'alignement
    add(sfx, t0 + 2.35, thump(0.55))             # la pile tombe
    nt = 10
    for j in range(nt):                          # tic-tic du compteur
        x = np.arange(int(0.03 * SR)) / SR
        add(sfx, t0 + 0.9 + 2.2 * (j / nt) ** 0.6, np.sin(2 * np.pi * 1500 * x) * np.exp(-x * 120) * 0.10)
    coin(t0 + 3.1)
add(sfx, SEG[-2]['t0'] + 3.1, thump(0.8))         # B-2 : impact final

for name, x in (('voice', voice), ('music', music), ('sfx', sfx)):
    x = x[:int(TOTAL * SR)]
    sf.write(f'px/{name}.wav', (x / (np.abs(x).max() + 1e-9) * 0.9).astype(np.float32), SR)
print('ok', TOTAL)
