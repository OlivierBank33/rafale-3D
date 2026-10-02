import numpy as np, soundfile as sf, json
tl=json.load(open('timeline.json')); starts=tl['starts']; TOTAL=tl['total']; arrive={int(k):v for k,v in tl['arrive'].items()}
# ---- voix (24 kHz)
vsr=24000; voice=np.zeros(int(TOTAL*vsr)+vsr)
for i,t0 in enumerate(starts):
    a,sr=sf.read(f'seg{i}.wav'); assert sr==vsr
    j=int(t0*vsr); voice[j:j+len(a)]+=a
voice/=np.abs(voice).max()*1.05
sf.write('voice.wav',voice.astype(np.float32),vsr)
# ---- musique + effets (44.1 kHz)
SR=44100; n=int(TOTAL*SR)+SR; t=np.arange(n)/SR
rng=np.random.default_rng(1)
def lp(x,fc):
    a=np.exp(-2*np.pi*fc/SR); y=np.empty_like(x); acc=0.
    # filtre 1 pôle vectorisé par scipy si dispo
    try:
        from scipy.signal import lfilter; return lfilter([1-a],[1,-a],x)
    except ImportError:
        for i,v in enumerate(x): acc=(1-a)*v+a*acc; y[i]=acc
        return y
bpm=100; beat=60/bpm; bar=4*beat
chords=[[57,60,64],[53,57,60],[48,52,55],[55,59,62]]  # Am F C G
f=lambda m:440*2**((m-69)/12)
music=np.zeros(n)
# pad
pad=np.zeros(n)
for b in range(int(TOTAL/bar)+2):
    ch=chords[b%4]; s0=int(b*bar*SR); s1=min(n,int((b+1)*bar*SR)); tt=np.arange(s1-s0)/SR
    if s1<=s0: break
    env=np.minimum(1,tt/0.4)*np.minimum(1,(bar-tt)/0.3)
    for m in ch:
        for det in (-0.12,0.12):
            fr=f(m+12)*(1+det/100)
            wave=sum(np.sin(2*np.pi*fr*k*tt)/k for k in range(1,6))
            pad[s0:s1]+=wave*env*0.08
pad=lp(pad,1800)
# basse en croches
bass=np.zeros(n)
for k in range(int(TOTAL/(beat/2))):
    b=int(k*(beat/2)/bar); root=chords[b%4][0]-24
    s0=int(k*beat/2*SR); L=int(beat/2*SR*0.9); tt=np.arange(L)/SR
    if s0+L>n: break
    env=np.exp(-tt*9)
    bass[s0:s0+L]+=np.tanh(2*np.sin(2*np.pi*f(root)*tt))*env*0.35
bass=lp(bass,500)
# kick + charley
drums=np.zeros(n)
for k in range(int(TOTAL/beat)):
    s0=int(k*beat*SR); L=int(0.35*SR); tt=np.arange(L)/SR
    if s0+L>n: break
    if k%2==0:
        ph=2*np.pi*np.cumsum(45+80*np.exp(-tt*30))/SR
        drums[s0:s0+L]+=np.sin(ph)*np.exp(-tt*9)*0.7
    for h in (0,0.5):
        s1=int((k+h)*beat*SR); L2=int(0.05*SR)
        if s1+L2<n:
            pass  # charleston au bruit blanc supprimé
music=pad+bass+drums
# intro plus calme : pas de batterie pendant l'accroche
calm=np.clip((t-3.6)/1.5,0,1); music=pad+bass*(0.5+0.5*calm)+drums*calm
# fin
fade=np.clip((TOTAL-t)/1.8,0,1); music*=fade
music*=0.5/np.abs(music).max()
# effets : whoosh + boom à chaque arrivée
sfx=np.zeros(n)
def whoosh(at,dur=0.9,g=0.5):
    s0=int((at-0.45)*SR); L=int(dur*SR)
    if s0<0: s0=0
    nz=rng.standard_normal(L); tt=np.arange(L)/SR
    env=np.sin(np.pi*tt/dur)**2
    # balayage : mélange de filtres
    mix=np.sin(2*np.pi*np.cumsum(150+550*(tt/dur)**1.5)/SR)*0.5
    sfx[s0:s0+L]+=mix*env*g
def boom(at,g=0.8):
    s0=int(at*SR); L=int(1.2*SR); tt=np.arange(L)/SR
    ph=2*np.pi*np.cumsum(38+60*np.exp(-tt*12))/SR
    sfx[s0:s0+L]+=np.sin(ph)*np.exp(-tt*3.5)*g
for pid,at in arrive.items():
    if pid==0: continue
    whoosh(at+0.3, g=0.35+0.03*pid)
    if pid>=5: boom(at+0.55, g=0.25+0.06*(pid-5))
whoosh(starts[0]+4.3,dur=2.0,g=0.5)  # zoom de l'intro
sfx*=0.6/max(1e-9,np.abs(sfx).max())
sf.write('music.wav',(music).astype(np.float32),SR)
sf.write('sfx.wav',(sfx).astype(np.float32),SR)
print('ok',TOTAL)
