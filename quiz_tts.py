import sys, json, numpy as np, soundfile as sf
from quiz_script import INTRO, OUTRO, Q
from kokoro_onnx import Kokoro
k=Kokoro('tts/kokoro.onnx','tts/voices.bin')
def gen(text,fn):
    a,sr=k.create(text,voice='ff_siwis',speed=1.15,lang='fr-fr')
    idx=np.where(np.abs(a)>0.01)[0]; a=a[max(0,idx[0]-400):idx[-1]+1200]
    sf.write(fn,a,sr); return len(a)/sr
d={'intro':gen(INTRO['say'],'qa/intro.wav'),'outro':gen(OUTRO['say'],'qa/outro.wav')}
for i,q in enumerate(Q):
    d[f'q{i}']=gen(q['q_say'],f'qa/q{i}.wav'); d[f'a{i}']=gen(q['a_say'],f'qa/a{i}.wav')
json.dump(d,open('qa/durs.json','w'),indent=0); print(d)
