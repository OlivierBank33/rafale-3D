"""Rendus 3D d'un avion FlightGear assemblé (XML + sous-modèles) pour les films premium.
Usage : python3 pr/pr3d_fg.py shots.json [plan ...]
Plan : xml, texmap {basename: chemin relatif à fg/}, out, W, H, az, el, dist, lens, samples, pitch, roll, yaw, gear (bool),
gear_words [...], sun_el, sun_az, sun_energy, sun_col, rim_energy, sky_strength, exposure, pts {nom: [x,y,z] FG}, project_only.
Repère FG : x vers l'arrière, y vers la droite, z vers le haut (aile gauche à -y). pitch > 0 = nez haut, roll > 0 = aile gauche basse."""
import bpy, sys, os, json, math
from mathutils import Vector, Matrix
sys.path.insert(0, '/home/claude')
import render3d as R
import render_fg as F
from bpy_extras.object_utils import world_to_camera_view


def shot(cfg):
    W, H = cfg.get('W', 1600), cfg.get('H', 1600)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    R._img_cache.clear()
    R.setup_scene(cfg, W, H)
    sc = bpy.context.scene; sc.cycles.samples = cfg.get('samples', 48)
    parts = []
    excl = F.EXCL + cfg.get('exclude', []) + ([] if cfg.get('gear', False) else cfg.get('gear_words', ['gear', 'nlg', 'mlg']))
    F.collect(os.path.join('/home/claude/fg', cfg['xml']), Matrix.Identity(4), parts, excl)
    cfg2 = dict(cfg); cfg2['skip'] = cfg.get('skip', []) + ['shadow', 'light', 'beam', 'cone', 'halo', 'flare']
    ob = F.build(parts, cfg2)
    rot = (Matrix.Rotation(math.radians(cfg.get('yaw', 0)), 4, 'Z') @ Matrix.Rotation(math.radians(cfg.get('roll', 0)), 4, 'X')
           @ Matrix.Rotation(math.radians(cfg.get('pitch', 0)), 4, 'Y'))
    ob.matrix_world = rot
    bpy.context.view_layer.update()
    for o in sc.objects:
        if o.name == 'sun':
            o.rotation_euler = (math.radians(90 - cfg.get('sun_el', 40)), 0, math.radians(cfg.get('sun_az', 35)))
            o.data.energy = cfg.get('sun_energy', 2.4); o.data.color = cfg.get('sun_col', (1.0, 0.95, 0.88))
        if o.name == 'rim':
            o.data.energy = cfg.get('rim_energy', 1.6)
    sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value = cfg.get('sky_strength', 0.35)
    sc.view_settings.exposure = cfg.get('exposure', -0.25)
    # points auto (repère local) : nez, queue, saumons
    vs = [v.co for v in ob.data.vertices]
    xmin = min(v.x for v in vs); xmax = max(v.x for v in vs); ymin = min(v.y for v in vs); ymax = max(v.y for v in vs)
    zmax = max(v.z for v in vs)
    nose_v = min(vs, key=lambda v: v.x)
    P = {'nose': (nose_v.x, nose_v.y, nose_v.z), 'tail': (xmax, 0, zmax), 'lwtip': (0, ymin, 0), 'rwtip': (0, ymax, 0), 'center': ((xmin + xmax) / 2, 0, 0)}
    lw = min(vs, key=lambda v: v.y); rw = max(vs, key=lambda v: v.y)
    P['lwtip'] = (lw.x, lw.y, lw.z); P['rwtip'] = (rw.x, rw.y, rw.z)
    P.update({k: tuple(v) for k, v in cfg.get('pts', {}).items()})
    R.frame_camera(ob, cfg, W, H)
    cam = sc.camera.data; cam.shift_x = cfg.get('shift_x', 0.0); cam.shift_y = cfg.get('shift_y', 0.0)
    if 'target' in cfg:                                   # plan serré : caméra visée sur un point (repère local FG), à tdist mètres
        tg = ob.matrix_world @ Vector(cfg['target'])
        az = math.radians(cfg.get('az', 35)); el = math.radians(cfg.get('el', 10)); d = cfg.get('tdist', 10.0)
        co = sc.camera
        co.location = tg + Vector((math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el))) * d
        co.rotation_euler = (tg - co.location).to_track_quat('-Z', 'Y').to_euler()
        if cfg.get('lens'): cam.lens = cfg['lens']
    bpy.context.view_layer.update()
    out = {}
    for k, v in P.items():
        co = world_to_camera_view(sc, sc.camera, ob.matrix_world @ Vector(v))
        out[k] = (round(co.x * W, 1), round((1 - co.y) * H, 1))
    print('LOCAL', {k: tuple(round(x, 2) for x in v) for k, v in P.items()})
    json.dump({'W': W, 'H': H, 'pts': out, 'local': P}, open(os.path.splitext(cfg['out'])[0] + '.json', 'w'))
    if cfg.get('project_only'):
        return
    sc.render.filepath = cfg['out']
    bpy.ops.render.render(write_still=True)


if __name__ == '__main__':
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    shots = json.load(open(argv[0])); names = argv[1:]
    for nm, cfg in shots.items():
        if names and nm not in names:
            continue
        cfg.setdefault('out', f'/home/claude/pr/r_{nm}.png')
        shot(cfg)
        print('DONE', nm, flush=True)
