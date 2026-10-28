"""Rendus 3D Cycles d'un modèle .glb (ex. fg/rafale.glb) pour les films cinéma, avec attitude et points projetés (comme pr3d_fg.py).
Usage : python3 pr/pr3d_glb.py shots.json [plan ...]
Plan : glb, drop [...], base_rot (deg autour de Z pour amener le nez vers -X ; Rafale = -90), out, W, H, az, el, dist, lens, samples, pitch, roll, yaw,
sun_el, sun_az, sun_energy, rim_energy, sky_strength, exposure, pts {nom: [x,y,z] repère FG : x arrière, y droite, z haut}, target/tdist.
Sortie : pr/r_<plan>.png (fond transparent) + pr/r_<plan>.json (points projetés)."""
import bpy, sys, os, json, math
from mathutils import Vector, Matrix
sys.path.insert(0, '/home/claude')
import render3d as R
from bpy_extras.object_utils import world_to_camera_view


def shot(cfg):
    W, H = cfg.get('W', 1600), cfg.get('H', 1600)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    R.setup_scene(cfg, W, H)
    sc = bpy.context.scene; sc.cycles.samples = cfg.get('samples', 48)
    bpy.ops.import_scene.gltf(filepath=cfg['glb'])
    for o in list(sc.objects):
        if o.type in ('CAMERA', 'LIGHT') and o.name not in ('sun', 'rim', 'cam'):
            bpy.data.objects.remove(o)
    drop = [k.lower() for k in cfg.get('drop', [])]
    for nm, path in cfg.get('img_override', {}).items():           # texture repeinte (ex. cocardes françaises)
        if nm in bpy.data.images:
            im = bpy.data.images[nm]
            if im.packed_file: im.unpack(method='USE_ORIGINAL') if False else None
            new = bpy.data.images.load(path); im.user_remap(new)
    meshes = [o for o in sc.objects if o.type == 'MESH']
    for o in list(meshes):
        if any(k in o.name.lower() for k in drop):
            meshes.remove(o); bpy.data.objects.remove(o)
    bpy.ops.object.select_all(action='DESELECT')
    for o in meshes: o.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    bpy.ops.object.join()
    ob = bpy.context.view_layer.objects.active
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    # repère FG : nez vers -X, z haut, centré
    vs = [v.co.copy() for v in ob.data.vertices]
    cz = (min(v.z for v in vs) + max(v.z for v in vs)) / 2
    cy = (min(v.y for v in vs) + max(v.y for v in vs)) / 2
    cx = (min(v.x for v in vs) + max(v.x for v in vs)) / 2
    base = Matrix.Rotation(math.radians(cfg.get('base_rot', -90)), 4, 'Z') @ Matrix.Translation((-cx, -cy, -cz))
    ob.data.transform(base); ob.data.update()
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
    vs = [v.co for v in ob.data.vertices]
    xmin = min(v.x for v in vs); xmax = max(v.x for v in vs); zmax = max(v.z for v in vs)
    nose_v = min(vs, key=lambda v: v.x); lw = min(vs, key=lambda v: v.y); rw = max(vs, key=lambda v: v.y)
    aft = [v for v in vs if v.x > xmax - 0.6 and abs(v.z - 0) < 1.2]
    P = {'nose': tuple(nose_v), 'tail': (xmax, 0, zmax), 'lwtip': tuple(lw), 'rwtip': tuple(rw), 'center': ((xmin + xmax) / 2, 0, 0)}
    if aft:
        P['aft'] = (sum(v.x for v in aft) / len(aft), sum(v.y for v in aft) / len(aft), sum(v.z for v in aft) / len(aft))
    P.update({k: tuple(v) for k, v in cfg.get('pts', {}).items()})
    R.frame_camera(ob, cfg, W, H)
    cam = sc.camera.data
    if 'target' in cfg:
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
