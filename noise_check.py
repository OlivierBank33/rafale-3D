"""Garde-fou : refuse un bed qui contient du souffle/bruit blanc (planéité spectrale ou aigus anormaux)."""
import sys, numpy as np, soundfile as sf
bad = False
for f in sys.argv[1:]:
    x, sr = sf.read(f); x = x.mean(1) if x.ndim > 1 else x
    for i in range(0, max(1, len(x) - 2 * sr), 2 * sr):
        seg = x[i:i + 2 * sr]
        if np.sqrt(np.mean(seg**2)) < 0.03 * np.abs(x).max(): continue
        S = np.abs(np.fft.rfft(seg)) + 1e-12; fr = np.fft.rfftfreq(len(seg), 1 / sr)
        flat = np.exp(np.mean(np.log(S))) / S.mean(); hf = S[fr > 4000].sum() / S.sum()
        if flat > 0.5 or hf > 0.5:
            print(f'BRUIT {f} t={i/sr:.0f}s planéité={flat:.2f} aigus={hf:.2f}'); bad = True; break
sys.exit(1 if bad else 0)
