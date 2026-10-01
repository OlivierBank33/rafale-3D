import numpy as np, soundfile as sf, json
from scipy.signal import lfilter
tl=json.load(open('qa2/timeline.json')); T=tl['T']; qs=tl['qs']; TOTAL=tl['total']
D=json.load(open('qa2/durs.json'))
vsr=24000; voice=np.zeros(int(TOTAL*vsr)+vsr)
def put(fn,t0):
    a,sr=sf.read(fn); j=int(t0*vsr); voice[j:j+len(a)]+=a
put('qa2/intro.wav',T['intro']); put('qa2/outro.wav',T['outro'])
for i,q in enumerate(qs):
    put(f'qa2/q{i}.wav',q['q0']+0.15); put(f'qa2/a{i}.wav',q['a0'])
voice/=np.abs(voice).max()*1.05; sf.write('qa2/voice.wav',voice.astype(np.float32),vsr)
SR=44100; n=int(TOTAL*SR)+SR; rng=np.random.default_rng(3)
lp=lambda x,fc:(lambda a:lfilter([1-a],[1,-a],x))(np.exp(-2*np.pi*fc/SR))
f=lambda m:440*2**((m-69)/12)
bpm=118; beat=60/bpm; bar=4*beat
chords=[[57,60,64],[53,57,60],[55,59,62],[52,56,59]]  # Am F G E : tension
pad=np.zeros(n); bass=np.zeros(n); drums=np.zeros(n)
for b in range(int(TOTAL/bar)+1):
    ch=chords[b%4]; s0=int(b*bar*SR); s1=min(n,int((b+1)*bar*SR)); tt=np.arange(s1-s0)/SR
    env=np.minimum(1,tt/0.3)*np.minimum(1,(bar-tt)/0.2)
    for m in ch:
        for det in (-0.1,0.1):
            pad[s0:s1]+=sum(np.sin(2*np.pi*f(m+12)*(1+det/100)*k*tt)/k for k in range(1,5))*env*0.07
for k in range(int(TOTAL/(beat/2))):
    b=int(k*(beat/2)/bar); s0=int(k*beat/2*SR); L=int(beat/2*SR*0.9); tt=np.arange(L)/SR
    if s0+L>n: break
    bass[s0:s0+L]+=np.tanh(2.5*np.sin(2*np.pi*f(chords[b%4][0]-24)*tt))*np.exp(-tt*8)*0.35
for k in range(int(TOTAL/beat)):
    s0=int(k*beat*SR); L=int(0.3*SR); tt=np.arange(L)/SR
    if s0+L>n: break
    ph=2*np.pi*np.cumsum(45+90*np.exp(-tt*30))/SR; drums[s0:s0+L]+=np.sin(ph)*np.exp(-tt*10)*0.6
    for h in (0,.5):
        s1=int((k+h)*beat*SR); L2=int(.04*SR)
        if s1+L2<n: nz=rng.standard_normal(L2); drums[s1:s1+L2]+=(nz-lp(nz,7000))*np.exp(-np.arange(L2)/SR*90)*0.1
music=lp(pad,1800)+lp(bass,500)+drums
t=np.arange(n)/SR
# pendant les comptes à rebours : musique plus basse (tension)
g=np.ones(n)
for q in qs:
    m=(t>q['cd0'])&(t<q['rev']); g[m]=0.45
g=lp(g,8); music*=g*np.clip((TOTAL-t)/2,0,1); music*=0.5/np.abs(music).max()
sfx=np.zeros(n)
def tick(at,hi):
    s0=int(at*SR); L=int(.08*SR); tt=np.arange(L)/SR
    sfx[s0:s0+L]+=np.sin(2*np.pi*(1800 if hi else 1200)*tt)*np.exp(-tt*60)*0.5
def ding(at):
    s0=int(at*SR); L=int(1.2*SR); tt=np.arange(L)/SR
    for fr,a in ((f(76),.35),(f(79),.3),(f(84),.3)):
        sfx[s0:s0+L]+=np.sin(2*np.pi*fr*tt)*np.exp(-tt*3)*a
def whoosh(at,dur=.6,gn=.35):
    s0=max(0,int(at*SR)); L=int(dur*SR); tt=np.arange(L)/SR; nz=rng.standard_normal(L)
    sfx[s0:s0+L]+=((1-tt/dur)*lp(nz,700)+(tt/dur)*lp(nz,4000))*np.sin(np.pi*tt/dur)**2*gn
for q in qs:
    whoosh(q['q0']-0.1)
    for s in range(3): tick(q['cd0']+s, s==2)
    ding(q['rev'])
sfx*=0.7/np.abs(sfx).max()
sf.write('qa2/music.wav',music.astype(np.float32),SR); sf.write('qa2/sfx.wav',sfx.astype(np.float32),SR)
