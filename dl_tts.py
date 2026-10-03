"""Voix guide Kokoro par scène pour un duel : DL=dl/<slug> python3 dl_tts.py -> durs.json + s<i>.wav"""
import json, os, numpy as np, soundfile as sf, importlib.util
from kokoro_onnx import Kokoro
D = os.environ.get('DL', 'dl/rafale_typhoon').rstrip('/') + '/'
spec = importlib.util.spec_from_file_location('cfg', D + 'cfg.py'); CFG = importlib.util.module_from_spec(spec); spec.loader.exec_module(CFG)
k = Kokoro('tts/kokoro.onnx', 'tts/voices.bin'); d = {}
for i, s in enumerate(CFG.SCENES):
    a, sr = k.create(s['say'].replace('Eurofighter', 'Euro-faïteur').replace('Typhoon', 'Taïfoune'), voice='ff_siwis', speed=1.12, lang='fr-fr')
    idx = np.where(np.abs(a) > 0.01)[0]; a = a[max(0, idx[0] - 400):idx[-1] + 1200]
    sf.write(D + f's{i}.wav', a, sr); d[f's{i}'] = len(a) / sr
json.dump(d, open(D + 'durs.json', 'w')); print({k_: round(v, 1) for k_, v in d.items()}, round(sum(d.values()), 1))
