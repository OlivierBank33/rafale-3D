"""Rendus 3D du Concorde F-BTSC (livrée Air France) pour le film premium.
Usage : python3 pr/pr3d.py shots.json [nom1 nom2 ...]
Chaque plan : out, W, H, az, el, dist, lens, samples, pitch, roll, yaw, gear (bool), sun_el, sun_az, sun_energy, sun_col, exposure,
sky_strength, shift_x, shift_y, list_objects
"""
import bpy, sys, os, json, math
from mathutils import Vector, Matrix
sys.path.insert(0, '/home/claude')
import render3d as R
from bpy_extras.object_utils import world_to_camera_view

AC = '/home/claude/fg/Concorde/Models/concorde.ac'
TEX = {'concorde.png': '/home/claude/pr/AF_FBTSC.png'}
_orig_find = R.find_tex


def find_tex(acdir, tex, extra):
    b = os.path.basename(tex)
    if b in TEX:
        return TEX[b]
    return _orig_find(acdir, tex, extra)


R.find_tex = find_tex
ALWAYS_SKIP = ['reheat', 'innerflame', 'outerflame', 'fx', 'hullinside', 'cabin', 'mainpanel', 'pillar']
GEAR = ['lmain', 'rmain', 'fwheels', 'fstrut', 'fhub', 'fram', 'tailwheels', 'tailstrut', 'tailram', 'taildoorfront',
        'lactuating', 'ractuating', 'lpiston', 'rpiston', 'ofl', 'ofr', 'oli', 'olo', 'ori', 'oro', 'littledoor', 'wheel']
CLOSED = ['closed']


def shot(cfg):
    W, H = cfg.get('W', 1600), cfg.get('H', 1600)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    R._img_cache.clear() if hasattr(R, '_img_cache') else None
    R.setup_scene(cfg, W, H)
    sc = bpy.context.scene
    sc.cycles.samples = cfg.get('samples', 48)
    try:
        sc.cycles.use_adaptive_sampling = True
    except Exception:
        pass
    skip = list(ALWAYS_SKIP) + (CLOSED if cfg.get('gear', False) else GEAR) + cfg.get('skip', [])
    cfg2 = dict(cfg); cfg2['skip'] = skip
    ob = R.load_model(AC, cfg2)
    if cfg.get('list_objects'):
        mats, objs = R.parse_ac(AC)
        print('OBJS', sorted(set(o[0] for o in objs if o[0])))
    # orientation de l'avion : yaw/pitch/roll en degrés (après la conversion AC->Blender)
    base = ob.rotation_euler.to_matrix().to_4x4()
    rot = (Matrix.Rotation(math.radians(cfg.get('yaw', 0)), 4, 'Z') @ Matrix.Rotation(math.radians(cfg.get('roll', 0)), 4, 'X')
           @ Matrix.Rotation(math.radians(cfg.get('pitch', 0)), 4, 'Y'))
    ob.matrix_world = rot @ base
    bpy.context.view_layer.update()
    # soleil
    for o in sc.objects:
        if o.name == 'sun':
            o.rotation_euler = (math.radians(90 - cfg.get('sun_el', 40)), 0, math.radians(cfg.get('sun_az', 35)))
            o.data.energy = cfg.get('sun_energy', 2.4); o.data.color = cfg.get('sun_col', (1.0, 0.95, 0.88))
        if o.name == 'rim':
            o.data.energy = cfg.get('rim_energy', 1.6)
    w = sc.world.node_tree.nodes['Background']; w.inputs['Strength'].default_value = cfg.get('sky_strength', 0.35)
    sc.view_settings.exposure = cfg.get('exposure', -0.25)
    bb = [ob.matrix_world @ Vector(c) for c in ob.bound_box]
    mn = Vector((min(v[k] for v in bb) for k in range(3))); mx = Vector((max(v[k] for v in bb) for k in range(3)))
    R.frame_camera(ob, cfg, W, H)
    cam = sc.camera.data; cam.shift_x = cfg.get('shift_x', 0.0); cam.shift_y = cfg.get('shift_y', 0.0)
    print('BBOX', tuple(round(x, 2) for x in mn), tuple(round(x, 2) for x in mx))
    P = {'nose': (-31.4, 0, 0), 'tail': (24.4, 7.4, 0), 'lgear': (4.49, -3.9, 3.73), 'lgear_top': (5.4, -0.9, 3.7), 'rgear': (4.49, -3.9, -3.74),
         'fgear': (-12.1, -4.0, 0), 'noz1': (15.4, -0.9, 6.12), 'noz2': (15.4, -0.9, 4.78), 'noz3': (15.4, -0.9, -4.77), 'noz4': (15.4, -0.9, -6.11),
         'impact': (3.0, -1.0, 4.4), 'tank5': (1.5, -0.6, 4.0), 'leak': (4.0, -1.1, 4.3), 'lwtip': (15.0, -0.8, 12.3), 'rwtip': (15.0, -0.8, -12.3),
         'wing_le_l': (-5.0, -0.5, 4.5), 'cockpit': (-24.5, 1.4, 0), 'center': (0, 0, 0)}
    bpy.context.view_layer.update()
    out = {}
    for k, v in P.items():
        co = world_to_camera_view(sc, sc.camera, ob.matrix_world @ Vector(v))
        out[k] = (round(co.x * W, 1), round((1 - co.y) * H, 1))
    json.dump({'W': W, 'H': H, 'pts': out}, open(os.path.splitext(cfg['out'])[0] + '.json', 'w'))
    if cfg.get('project_only'):
        return
    sc.render.filepath = cfg['out']
    bpy.ops.render.render(write_still=True)


if __name__ == '__main__':
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    shots = json.load(open(argv[0]))
    names = argv[1:]
    for nm, cfg in shots.items():
        if names and nm not in names:
            continue
        cfg.setdefault('out', f'/home/claude/pr/r_{nm}.png')
        shot(cfg)
        print('DONE', nm, flush=True)
