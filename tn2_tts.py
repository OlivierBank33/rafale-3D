import json, numpy as np, soundfile as sf
from tournoi2_script import *
from kokoro_onnx import Kokoro
k=Kokoro('tts/kokoro.onnx','tts/voices.bin')
def gen(text,fn):
    a,sr=k.create(text,voice='ff_siwis',speed=1.24,lang='fr-fr')
    idx=np.where(np.abs(a)>0.01)[0]; a=a[max(0,idx[0]-400):idx[-1]+1200]
    sf.write(fn,a,sr); return len(a)/sr
d={'intro':gen(INTRO,'tn2/intro.wav'),'semis':gen(SEMIS,'tn2/semis.wav'),'final':gen(FINAL_INTRO,'tn2/final.wav'),'outro':gen(OUTRO,'tn2/outro.wav')}
for i,m in enumerate(DUELS+FINAL):
    d[f'q{i}']=gen(m['q'],f'tn2/q{i}.wav'); d[f'r{i}']=gen(m['r'],f'tn2/r{i}.wav')
json.dump(d,open('tn2/durs.json','w')); print({k:round(v,1) for k,v in d.items()}, round(sum(d.values()),1))
