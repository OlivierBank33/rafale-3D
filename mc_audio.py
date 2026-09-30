import numpy as np, soundfile as sf, json
from scipy.signal import lfilter
tl=json.load(open('mc/timeline.json')); TL=tl['TL']; TOTAL=tl['total']
vsr=24000; voice=np.zeros(int(TOTAL*vsr)+vsr)
for k,v in TL.items():
    a,sr=sf.read(f'mc/v/{k}.wav'); j=int(v['vt']*vsr); voice[j:j+len(a)]+=a
voice/=np.abs(voice).max()*1.05; sf.write('mc/voice.wav',voice.astype(np.float32),vsr)
SR=44100; n=int(TOTAL*SR)+SR; t=np.arange(n)/SR; rng=np.random.default_rng(7)
lp=lambda x,fc:(lambda a:lfilter([1-a],[1,-a],x))(np.exp(-2*np.pi*fc/SR))
f=lambda m:440*2**((m-69)/12)
# nappe cinématique sombre + pulsation
music=np.zeros(n); bar=2.4
chords=[[45,52,57,60],[41,48,53,57],[43,50,55,59],[40,47,52,56]]
for b in range(int(TOTAL/bar)+1):
    ch=chords[b%4]; s0=int(b*bar*SR); s1=min(n,int((b+1)*bar*SR)); tt=np.arange(s1-s0)/SR
    env=np.minimum(1,tt/0.6)*np.minimum(1,(bar-tt)/0.5)
    for m in ch:
        music[s0:s1]+=sum(np.sin(2*np.pi*f(m)*(1+d/100)*tt)*a for d,a in ((-0.15,.5),(0.15,.5)))*env*0.12
    for k in range(8):
        p0=s0+int(k*bar/8*SR); L=int(0.25*SR)
        if p0+L<n:
            tt2=np.arange(L)/SR; music[p0:p0+L]+=np.sin(2*np.pi*f(ch[0]-12)*tt2)*np.exp(-tt2*10)*0.35
music=lp(music,1500)
kick=np.zeros(n); beat=0.6
for k in range(int(TOTAL/beat)):
    s0=int(k*beat*SR); L=int(.3*SR); tt=np.arange(L)/SR
    if s0+L<n and k%2==0:
        kick[s0:s0+L]+=np.sin(2*np.pi*np.cumsum(45+80*np.exp(-tt*30))/SR)*np.exp(-tt*9)*0.5
calm=np.clip((t-TL['g1']['t0'])/1.0,0,1)
music=music+kick*calm*0.8
music*=np.clip((TOTAL-t)/2,0,1); music*=0.5/np.abs(music).max()
sfx=np.zeros(n)
# alarme master warning (bips) + moteurs qui s'éteignent
for k in range(6):
    s0=int((1.0+k*0.33)*SR); L=int(0.18*SR); tt=np.arange(L)/SR
    sfx[s0:s0+L]+=np.sign(np.sin(2*np.pi*(880 if k%2==0 else 660)*tt))*0.18*np.minimum(1,(0.18-tt)/0.02)
L=int(3.5*SR); tt=np.arange(L)/SR; nz=rng.standard_normal(L)
spool=lp(nz,2500)*np.exp(-tt*1.1)*0.5; whine=np.sin(2*np.pi*np.cumsum(3200*np.exp(-tt*0.9)+80)/SR)*np.exp(-tt*1.2)*0.12
eng=np.zeros(n); eng[:int(1.0*SR)]=lp(rng.standard_normal(int(1.0*SR)),2500)*0.5
eng[int(1.0*SR):int(1.0*SR)+L]+=spool+whine; sfx+=eng
# vent pendant le vol plané
wind=lp(rng.standard_normal(n),600)*0.15*(0.6+0.4*np.sin(t*0.7)); m=(t>TL['g1']['t0'])&(t<TL['r']['t0']); sfx+=wind*m
def whoosh(a,dur=.6,g=.4):
    s0=max(0,int(a*SR)); L=int(dur*SR); tt=np.arange(L)/SR; nz=rng.standard_normal(L)
    sfx[s0:s0+L]+=((1-tt/dur)*lp(nz,700)+(tt/dur)*lp(nz,4000))*np.sin(np.pi*tt/dur)**2*g
def hit(a,g=.8):
    s0=int(a*SR); L=int(1.2*SR); tt=np.arange(L)/SR
    sfx[s0:s0+L]+=np.sin(2*np.pi*np.cumsum(38+100*np.exp(-tt*14))/SR)*np.exp(-tt*3.5)*g
for k in ['g1','r','c1','c2','c3','o']: whoosh(TL[k]['t0']-0.3)
for k in ['c1','c2','c3']: hit(TL[k]['t0'])
sfx*=0.7/np.abs(sfx).max()
sf.write('mc/music.wav',music.astype(np.float32),SR); sf.write('mc/sfx.wav',sfx.astype(np.float32),SR)
