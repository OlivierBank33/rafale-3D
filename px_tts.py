import json, numpy as np, soundfile as sf
from px_script import INTRO, OUTRO, PLANES
from kokoro_onnx import Kokoro
k=Kokoro('tts/kokoro.onnx','tts/voices.bin')
d={}
items=[('intro',INTRO['say'])]+[(f'p{i}',p['say']) for i,p in enumerate(PLANES)]+[('outro',OUTRO['say'])]
for key,txt in items:
    a,sr=k.create(txt,voice='ff_siwis',speed=1.12,lang='fr-fr')
    idx=np.where(np.abs(a)>0.01)[0]; a=a[max(0,idx[0]-400):idx[-1]+1200]
    sf.write(f'px/{key}.wav',a,sr); d[key]=len(a)/sr
json.dump(d,open('px/durs.json','w')); print({k:round(v,1) for k,v in d.items()}, round(sum(d.values()),1))
