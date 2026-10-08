"""Synchronise un format « à timeline » (quiz, vrai-faux, tournoi…) sur une narration ElevenLabs unique.

Étape 1 (plan) : python3 el_sync.py plan <fmt>
    -> lit la timeline Kokoro du format, écrit <dir>/el_text.txt (texte + <break> calés sur les blancs de la timeline)
Étape 2 (apply) : python3 el_sync.py apply <fmt> <duree_el_secondes>
    -> calcule k, réécrit <dir>/durs.json (durées × k, original dans durs_kokoro.json), étire les wav Kokoro (guide/ducking)
Ensuite : relancer le render + l'audio du format, puis eleven_prep.sh.
"""
import json, sys, os, subprocess, importlib, re

os.chdir('/home/claude')
sys.path.insert(0, '/home/claude')

# respellings Kokoro -> texte normal pour ElevenLabs
FIX = [("èss ère soixante et onze", "S R soixante et onze"), ("Spitfaïeur", "Spitfire"), ("bé deux Spirite", "B deux Spirit"),
       ("bé deux", "B deux"), ("Blakbeurde", "Blackbird"), ("Guinemère", "Guynemer"), ("Latam", "Latham"),
       ("F-22", "F vingt-deux"), ("F-35", "F trente-cinq"), ("F-16", "F seize"), ("F-15", "F quinze"), ("A-10", "A dix"),
       ("SR-71", "S R soixante et onze"), ("B-2", "B deux"), ("B-52", "B cinquante-deux")]


def fix(s):
    for a, b in FIX: s = s.replace(a, b)
    s = s.replace('...', ',').replace('…', ',')   # les points de suspension créent des pauses imprévisibles
    return s


def segments(fmt):
    """Renvoie (dossier, [(clé, texte, début)]) depuis la timeline Kokoro du format."""
    if fmt == 'tn':
        S = importlib.import_module('tournoi_script'); ALL = S.DUELS + S.FINAL
        R = importlib.import_module('tournoi_render')
        txt = dict(intro=S.INTRO, semis=S.SEMIS, final=S.FINAL_INTRO, outro=S.OUTRO)
        for i, m in enumerate(ALL): txt[f'q{i}'] = m['q']; txt[f'r{i}'] = m['r']
        seg = []
        for s in R.SEQ:
            seg.append((s['voice'], txt[s['voice']], s['vt']))
            if s['kind'] == 'duel': seg.append((s['rvoice'], txt[s['rvoice']], s['rvt']))
        return 'tn', seg
    if fmt.startswith('vf') or fmt.startswith('qa'):
        mod = {'vf8': ('vf8_script', 'vf8_render', 'vf8'), 'vf7': ('vf7_script', 'vf7_render', 'vf7'), 'qa6': ('quiz6_script', 'quiz6_render', 'qa6'), 'vf6': ('vf6_script', 'vf6_render', 'vf6'), 'qa5': ('quiz5_script', 'quiz5_render', 'qa5'), 'vf5': ('vf5_script', 'vf5_render', 'vf5'), 'qa4': ('quiz4_script', 'quiz4_render', 'qa4'), 'vf4': ('vf4_script', 'vf4_render', 'vf4'), 'vf3': ('vf3_script', 'vf3_render', 'vf3'), 'vf2': ('vf2_script', 'vf2_render', 'vf2')}[fmt]
        S = importlib.import_module(mod[0]); R = importlib.import_module(mod[1])
        seg = [('intro', S.INTRO['say'], R.T['intro'])]
        for i, q in enumerate(S.Q):
            seg.append((f'q{i}', q['q_say'], R.qs[i]['q0'] + 0.15))
            seg.append((f'a{i}', q['a_say'], R.qs[i]['a0']))
        seg.append(('outro', S.OUTRO['say'], R.T['outro']))
        return mod[2], seg
    if fmt in ('ea', 'bio'):
        mod = {'ea': ('ea_script', 'ea_render', 'ea'), 'bio': ('bio_script', 'bio_render', 'bio')}[fmt]
        S = importlib.import_module(mod[0]); R = importlib.import_module(mod[1])
        return mod[2], [(sg['k'], sc['say'], sg['vt']) for sg, sc in zip(R.SEG, S.SCENES)]
    if fmt == 'pol':
        R = importlib.import_module('pol_render').R
        return 'pol', [(sg['k'], sg['p']['say'], sg['vt']) for sg in R.SEG]
    if fmt.startswith('dl:'):
        os.environ['DL'] = 'dl/' + fmt[3:]
        R = importlib.import_module('dl_render')
        return 'dl/' + fmt[3:], [(sg['k'], sg['p']['say'], sg['vt']) for sg in R.SEG]
    if fmt.startswith('dc:'):
        os.environ['DL'] = 'dl/' + fmt[3:]
        R = importlib.import_module('dc_render')
        return 'dl/' + fmt[3:], [(sg['k'], sg['p']['say'], sg['vt']) for sg in R.SEG]
    if fmt.startswith('pa:'):
        os.environ['DL'] = 'dl/' + fmt[3:]
        R = importlib.import_module('pa_render')
        return 'dl/' + fmt[3:], [(sg['k'], sg['p']['say'], sg['vt']) for sg in R.SEG]
    if fmt.startswith('rc:'):
        os.environ['DL'] = 'dl/' + fmt[3:]
        R = importlib.import_module('rc_render')
        return 'dl/' + fmt[3:], [(sg['k'], sg['p']['say'], sg['vt']) for sg in R.SEG]
    if fmt == 'px':
        S = importlib.import_module('px_script'); R = importlib.import_module('px_render')
        txt = dict(intro=S.INTRO['say'], outro=S.OUTRO['say'], **{f'p{i}': p['say'] for i, p in enumerate(S.PLANES)})
        return 'px', [(sg['k'], txt[sg['k']], sg['vt']) for sg in R.SEG]
    raise SystemExit('format inconnu')


def brk(g):
    out = []
    while g > 0.05:
        x = min(3.0, g); out.append(f'<break time="{x:.1f}s" />'); g -= x
    return ' '.join(out)


if __name__ == '__main__':
    cmd, fmt = sys.argv[1], sys.argv[2]
    d, seg = segments(fmt)
    Dk = json.load(open(f'{d}/durs_kokoro.json')) if os.path.exists(f'{d}/durs_kokoro.json') else json.load(open(f'{d}/durs.json'))
    if not os.path.exists(f'{d}/durs_kokoro.json'): json.dump(Dk, open(f'{d}/durs_kokoro.json', 'w'))
    seg.sort(key=lambda x: x[2])
    gaps = [seg[i + 1][2] - (seg[i][2] + Dk[seg[i][0]]) for i in range(len(seg) - 1)]
    lead = seg[0][2]
    if cmd == 'plan':
        parts = [brk(lead)] if lead > 0.05 else []
        for i, (k, t, _) in enumerate(seg):
            parts.append(fix(t))
            if i < len(gaps): parts.append(brk(max(0.15, gaps[i])))
        txt = ' '.join(p for p in parts if p)
        open(f'{d}/el_text.txt', 'w').write(txt)
        print(len(txt), 'car. | parole Kokoro', round(sum(Dk[k] for k, _, _ in seg), 1), 's | blancs', round(sum(max(0.15, g) for g in gaps) + lead, 1), 's')
    elif cmd == 'apply':
        Del = float(sys.argv[3])
        fixed = sum(max(0.15, g) for g in gaps) + lead
        speech = sum(Dk[k] for k, _, _ in seg)
        k = (Del - fixed) / speech
        D2 = dict(Dk)
        for key, _, _ in seg: D2[key] = Dk[key] * k
        json.dump(D2, open(f'{d}/durs.json', 'w'))
        for key, _, _ in seg:
            src = f'{d}/{key}.wav'
            if not os.path.exists(f'{d}/{key}_kokoro.wav'): os.rename(src, f'{d}/{key}_kokoro.wav')
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{d}/{key}_kokoro.wav', '-af', f'atempo={1 / k:.5f}', src], check=True)
        print('k =', round(k, 3))
