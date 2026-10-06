"""Aides pour poser la mascotte dans un moteur : enveloppe de voix -> ouverture de bouche, clignement, pop."""
import math, numpy as np, soundfile as sf


def envelope(items, total, fps=30):
    """items = [(chemin_wav, t0)] ; renvoie MOUTH[frame] dans 0..1."""
    env = np.zeros(int(total * fps) + fps)
    for fn, t0 in items:
        try:
            a, sr = sf.read(fn)
        except Exception:
            continue
        if a.ndim > 1: a = a.mean(1)
        hop = sr / fps
        for i in range(int(len(a) / hop)):
            j = int(t0 * fps) + i
            if 0 <= j < len(env): env[j] = np.sqrt(np.mean(a[int(i * hop):int((i + 1) * hop)] ** 2))
    ref = np.percentile(env[env > 1e-4], 85) if (env > 1e-4).any() else 1.0
    m = np.clip((env / ref - 0.15) * 1.4, 0, 1)
    return np.maximum(m, np.roll(m, 1) * 0.6)


def blink(t):
    return 1 if (t + 0.7) % 3.4 < 0.1 else 0


def pop(t, t0, dur=0.28):
    return 0.0 if t0 is None else max(0.0, 1 - (t - t0) / dur)
