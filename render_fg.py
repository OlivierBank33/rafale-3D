"""Assemble un avion FlightGear à partir de son XML (sous-modèles + offsets) puis rend avec Cycles.
Usage : python3 render_fg.py config.json
config : xml, out, W, H, az, el, dist, lens, samples, exclude[], hide_gear
"""
import bpy, bmesh, sys, os, json, math
import xml.etree.ElementTree as ET
from mathutils import Matrix, Vector
sys.path.insert(0, '/home/claude')
import render3d as R

FG = '/home/claude/fg'
EXCL = ['interior', 'flightdeck', 'cockpit', 'cabin', 'light', 'effect', 'pilot', 'panel', 'instrument', 'pushback',
        'marker', 'service', 'operation', 'stair', 'shadow', 'fire', 'smoke', 'contrail', 'fuel-dump', 'wet-runway',
        'tyresmoke', 'chock', 'choke', 'truck', 'catering', 'baggage', 'dualcontrol', 'hud', 'iae', 'pw4000', 'trent',
        'door', 'glass', 'reflect', 'airport']


def resolve(p, base):
    p = p.strip()
    if p.startswith('Aircraft/'):
        return os.path.join(FG, p[len('Aircraft/'):])
    if p.startswith('Models/') and not os.path.exists(os.path.join(base, p)):
        return None
    return os.path.normpath(os.path.join(base, p))


def fmat(off):
    def g(tag):
        e = off.find(tag) if off is not None else None
        return float(e.text) if e is not None and e.text else 0.0
    T = Matrix.Translation((g('x-m'), g('y-m'), g('z-m')))
    Rz = Matrix.Rotation(math.radians(g('heading-deg')), 4, 'Z')
    Ry = Matrix.Rotation(math.radians(g('pitch-deg')), 4, 'Y')
    Rx = Matrix.Rotation(math.radians(g('roll-deg')), 4, 'X')
    return T @ Rz @ Ry @ Rx


def collect(xml_path, M, parts, exclude, depth=0):
    if depth > 6 or not os.path.exists(xml_path):
        return
    try:
        root = ET.parse(xml_path).getroot()
    except ET.ParseError:
        return
    base = os.path.dirname(xml_path)
    top = root.find('path')
    if top is not None and top.text:
        p = resolve(top.text, base)
        if p and p.endswith('.ac') and os.path.exists(p):
            # offsets au niveau racine
            parts.append((p, M @ fmat(root.find('offsets'))))
    for m in root.findall('model'):
        pe = m.find('path'); nm = (m.findtext('name') or '').lower()
        if pe is None or not pe.text:
            continue
        low = pe.text.lower() + ' ' + nm
        if any(k in low for k in exclude):
            continue
        p = resolve(pe.text, base)
        if not p or not os.path.exists(p):
            continue
        Mc = M @ fmat(m.find('offsets'))
        if p.endswith('.xml'):
            collect(p, Mc, parts, exclude, depth + 1)
        elif p.endswith('.ac'):
            parts.append((p, Mc))


MARK = []
AC2FG = Matrix(((1, 0, 0, 0), (0, 0, -1, 0), (0, 1, 0, 0), (0, 0, 0, 1)))


def build(parts, cfg):
    me = bpy.data.meshes.new('plane'); bm = bmesh.new(); uvl = bm.loops.layers.uv.new()
    matlist, matindex = [], {}
    skip = [s.lower() for s in cfg.get('skip', [])] + ['propellerdisk', 'shadow', 'collision', 'light-cone', 'lightcone', 'halo']
    for (acp, M) in parts:
        mats, objs = R.parse_ac(acp)
        acdir = os.path.dirname(acp)
        extra = [os.path.join(acdir, d) for d in cfg.get('texdirs', [])]
        for (name, tex, texrep, texoff, wv, surfs) in objs:
            if any(s in (name or '').lower() for s in skip) or not surfs:
                continue
            bverts = [bm.verts.new(M @ AC2FG @ v) for v in wv]
            if cfg.get('mark') and cfg['mark'] in acp and wv:
                MARK.extend([M @ AC2FG @ v for v in wv])
            tmap = cfg.get('texmap', {})
            if tex and os.path.basename(tex) in tmap:
                texpath = os.path.join(FG, tmap[os.path.basename(tex)])
            else:
                texpath = R.find_tex(acdir, tex, extra) if tex else None
            for (mi, refs, smooth) in surfs:
                mi = max(0, min(mi, len(mats) - 1))
                key = f"{acp}|{mi}|{texpath}"
                if key not in matindex:
                    matindex[key] = len(matlist); matlist.append(R.make_material(mats[mi], texpath, key, cfg))
                try:
                    vs = [bverts[r[0]] for r in refs]
                    if len(set(vs)) < 3: continue
                    f = bm.faces.new(vs)
                except (ValueError, IndexError):
                    continue
                f.material_index = matindex[key]; f.smooth = smooth
                for lp, r in zip(f.loops, refs):
                    lp[uvl].uv = (r[1] * texrep[0] + texoff[0], r[2] * texrep[1] + texoff[1])
    bm.to_mesh(me); bm.free()
    for m in matlist: me.materials.append(m)
    ob = bpy.data.objects.new('plane', me); bpy.context.scene.collection.objects.link(ob)
    return ob


if __name__ == '__main__':
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    cfg = json.load(open(argv[0]))
    W, H = cfg.get('W', 1080), cfg.get('H', 1080)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    R.setup_scene(cfg, W, H)
    parts = []
    collect(cfg['xml'], Matrix.Identity(4), parts, EXCL + cfg.get('exclude', []))
    for extra in cfg.get('extra_ac', []):
        parts.append((extra['ac'], Matrix.Translation(extra.get('off', (0, 0, 0)))))
    print('PARTS', [os.path.relpath(p, FG) for p, _ in parts])
    ob = build(parts, cfg)
    ob.rotation_euler = (math.radians(cfg.get('roll', 0)), math.radians(cfg.get('pitch', 0)), 0)
    bpy.context.view_layer.update()
    mn, mx = R.frame_camera(ob, cfg, W, H)
    print('BBOX', tuple(round(x, 2) for x in mn), tuple(round(x, 2) for x in mx), 'faces', len(ob.data.polygons))
    if MARK:
        from bpy_extras.object_utils import world_to_camera_view
        cen = sum(MARK, Vector()) / len(MARK)
        cen = ob.matrix_world @ cen
        co = world_to_camera_view(bpy.context.scene, bpy.context.scene.camera, cen)
        json.dump(dict(x=co.x * W, y=(1 - co.y) * H), open(cfg['out'] + '.mark.json', 'w'))
        print('MARK', co.x * W, (1 - co.y) * H)
    bpy.context.scene.render.filepath = cfg['out']
    bpy.ops.render.render(write_still=True)
