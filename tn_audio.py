import numpy as np, soundfile as sf, json
from scipy.signal import lfilter
tl=json.load(open('tn/timeline.json')); SEQ=tl['seq']; TOTAL=tl['total']
vsr=24000; voice=np.zeros(int(TOTAL*vsr)+vsr)
def put(fn,t0):
    a,sr=sf.read(fn); j=int(t0*vsr); voice[j:j+len(a)]+=a
for s in SEQ:
    put(f"tn/{s['voice']}.wav",s['vt'])
    if s['kind']=='duel': put(f"tn/{s['rvoice']}.wav",s['rvt'])
voice/=np.abs(voice).max()*1.05; sf.write('tn/voice.wav',voice.astype(np.float32),vsr)
SR=44100; n=int(TOTAL*SR)+SR; t=np.arange(n)/SR; rng=np.random.default_rng(5)
lp=lambda x,fc:(lambda a:lfilter([1-a],[1,-a],x))(np.exp(-2*np.pi*fc/SR))
f=lambda m:440*2**((m-69)/12)
bpm=124; beat=60/bpm; bar=4*beat
chords=[[57,60,64],[53,57,60],[48,52,55],[55,59,62]]
pad=np.zeros(n); bass=np.zeros(n); drums=np.zeros(n)
for b in range(int(TOTAL/bar)+1):
    ch=chords[b%4]; s0=int(b*bar*SR); s1=min(n,int((b+1)*bar*SR)); tt=np.arange(s1-s0)/SR
    env=np.minimum(1,tt/0.2)*np.minimum(1,(bar-tt)/0.2)
    for m in ch:
        for det in (-0.12,0.12):
            pad[s0:s1]+=sum(np.sin(2*np.pi*f(m+12)*(1+det/100)*k*tt)/k for k in range(1,5))*env*0.06
for k in range(int(TOTAL/(beat/2))):
    b=int(k*(beat/2)/bar); s0=int(k*beat/2*SR); L=int(beat/2*SR*0.9); tt=np.arange(L)/SR
    if s0+L>n: break
    bass[s0:s0+L]+=np.tanh(3*np.sin(2*np.pi*f(chords[b%4][0]-24)*tt))*np.exp(-tt*7)*0.35
for k in range(int(TOTAL/beat)):
    s0=int(k*beat*SR); L=int(0.3*SR); tt=np.arange(L)/SR
    if s0+L>n: break
    ph=2*np.pi*np.cumsum(45+90*np.exp(-tt*30))/SR; drums[s0:s0+L]+=np.sin(ph)*np.exp(-tt*10)*0.65
    if k%2==1:
        L2=int(.18*SR); nz=rng.standard_normal(L2); drums[s0:s0+L2]+=(nz-lp(nz,1500))*np.exp(-np.arange(L2)/SR*25)*0.25
    for h in (0,.5):
        s1=int((k+h)*beat*SR); L2=int(.04*SR)
        if s1+L2<n: nz=rng.standard_normal(L2); drums[s1:s1+L2]+=(nz-lp(nz,7000))*np.exp(-np.arange(L2)/SR*90)*0.1
music=lp(pad,2000)+lp(bass,500)+drums
g=np.ones(n)
for s in SEQ:
    if s['kind']=='duel': g[(t>s['s0'])&(t<s['rev'])]=0.25   # silence tendu pendant le suspense
g=lp(g,10); music*=g*np.clip((TOTAL-t)/2,0,1); music*=0.5/np.abs(music).max()
sfx=np.zeros(n)
def roll(a,b):
    s0=int(a*SR); L=int((b-a)*SR); tt=np.arange(L)/SR
    rate=12+10*tt/(b-a); hits=(np.sin(2*np.pi*np.cumsum(rate)/SR)>0.6).astype(float)
    nz=rng.standard_normal(L); body=nz-lp(nz,300); body=lp(body,3500)
    sfx[s0:s0+L]+=body*hits*(0.25+0.5*tt/(b-a))
def impact(a,g_=1):
    s0=int(a*SR); L=int(1.4*SR); tt=np.arange(L)/SR
    ph=2*np.pi*np.cumsum(35+120*np.exp(-tt*15))/SR
    nz=rng.standard_normal(L)
    sfx[s0:s0+L]+=(np.sin(ph)*np.exp(-tt*3)*0.9+lp(nz,5000)*np.exp(-tt*12)*0.4)*g_
def whoosh(a,dur=.55,gn=.35):
    s0=max(0,int(a*SR)); L=int(dur*SR); tt=np.arange(L)/SR; nz=rng.standard_normal(L)
    sfx[s0:s0+L]+=((1-tt/dur)*lp(nz,700)+(tt/dur)*lp(nz,4000))*np.sin(np.pi*tt/dur)**2*gn
def fanfare(a):
    for k,(m,d) in enumerate([(67,.15),(72,.15),(76,.15),(79,.6)]):
        s0=int((a+k*0.15)*SR); L=int(d*SR+0.3*SR); tt=np.arange(L)/SR
        sfx[s0:s0+L]+=sum(np.sin(2*np.pi*f(m)*h*tt)/h**1.5 for h in range(1,6))*np.exp(-tt*3)*0.3
for s in SEQ:
    whoosh(s['t0']-0.1)
    if s['kind']=='duel':
        roll(s['s0'],s['rev']); impact(s['rev'])
    if s['kind']=='champion': impact(s['t0']); fanfare(s['t0']+0.2)
sfx*=0.75/np.abs(sfx).max()
sf.write('tn/music.wav',music.astype(np.float32),SR); sf.write('tn/sfx.wav',sfx.astype(np.float32),SR)
