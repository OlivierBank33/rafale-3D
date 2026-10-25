"""Planche de contrôle détaillée : python3 pipe/sm_sheet2.py <slug> <prefix_png> [par_planche=12] -> <prefix>_1.png, _2.png… (stills 300x533, horodatés)"""
import json, subprocess, os, sys
from PIL import Image, ImageDraw
os.chdir('/home/claude'); d = sys.argv[1]; out = sys.argv[2]; per = int(sys.argv[3]) if len(sys.argv) > 3 else 12
r = subprocess.run(['python3', 'sm_render2.py', 'stills', '0'], env=dict(os.environ, DL=f'dl/{d}'), capture_output=True, text=True)
if r.returncode: print(r.stderr[-1500:]); sys.exit(1)
tl = json.load(open(f'dl/{d}/timeline.json')); ts = []
for s in tl['seg']:
    for a, b in s['sent']: ts.append(round(a + 0.55 * (b - a), 2))
ts += [round(tl['total'] - 6, 2), round(tl['total'] - 1, 2)]
r = subprocess.run(['python3', 'sm_render2.py', 'stills'] + [str(x) for x in ts], env=dict(os.environ, DL=f'dl/{d}'), capture_output=True, text=True)
if r.returncode: print(r.stderr[-1500:]); sys.exit(1)
cols = 4; w, h = 300, 533
for n, i0 in enumerate(range(0, len(ts), per)):
    part = ts[i0:i0 + per]; rows = (len(part) + cols - 1) // cols
    im = Image.new('RGB', (w * cols, h * rows), (40, 40, 40)); dr = ImageDraw.Draw(im)
    for i, t in enumerate(part):
        x, y = (i % cols) * w, (i // cols) * h
        im.paste(Image.open(f'dl/{d}/still_{t}.png').resize((w, h)), (x, y)); dr.text((x + 6, y + 6), f'{i0 + i}  t={t}', fill=(255, 255, 0))
    im.save(f'{out}_{n + 1}.png')
print(len(ts), 'stills', tl['total'])
for f in os.listdir(f'dl/{d}'):
    if f.startswith('still_'): os.remove(f'dl/{d}/{f}')
