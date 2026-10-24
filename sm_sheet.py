import json, subprocess, os, sys
from PIL import Image
os.chdir('/home/claude'); d = sys.argv[1]; out = sys.argv[2]
tl = json.load(open(f'dl/{d}/timeline.json')) if os.path.exists(f'dl/{d}/timeline.json') else None
r = subprocess.run(['python3', 'sm_render2.py', 'stills', '0'], env=dict(os.environ, DL=f'dl/{d}'), capture_output=True, text=True)
if r.returncode: print(r.stderr[-1500:]); sys.exit(1)
tl = json.load(open(f'dl/{d}/timeline.json'))
ts = []
for s in tl['seg']:
    for a, b in s['sent']: ts.append(round(a + 0.55 * (b - a), 2))
ts.append(round(tl['total'] - 2, 2))
r = subprocess.run(['python3', 'sm_render2.py', 'stills'] + [str(x) for x in ts], env=dict(os.environ, DL=f'dl/{d}'), capture_output=True, text=True)
if r.returncode: print(r.stderr[-1500:]); sys.exit(1)
cols = 8; rows = (len(ts) + cols - 1) // cols
im = Image.new('RGB', (180 * cols, 320 * rows))
for i, t in enumerate(ts): im.paste(Image.open(f'dl/{d}/still_{t}.png').resize((180, 320)), ((i % cols) * 180, (i // cols) * 320))
im.save(out); print(len(ts), 'stills', tl['total'])
for f in os.listdir(f'dl/{d}'):
    if f.startswith('still_'): os.remove(f'dl/{d}/{f}')
