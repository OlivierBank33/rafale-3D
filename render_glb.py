"""Rendu Cycles d'un modèle .glb. Usage : python3 render_glb.py config.json  (clés comme render3d : glb, az, el, dist, W, H, samples, out, yaw)"""
import bpy, sys, json, math
from mathutils import Vector
sys.path.insert(0, '/home/claude/pipe')
from render3d import setup_scene, frame_camera

if __name__ == '__main__':
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    cfg = json.load(open(argv[0]))
    W, H = cfg.get('W', 1080), cfg.get('H', 1080)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    setup_scene(cfg, W, H)
    bpy.ops.import_scene.gltf(filepath=cfg['glb'])
    meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    for o in bpy.context.scene.objects:
        if o.type in ('CAMERA', 'LIGHT') and o.name not in ('sun', 'rim', 'cam'):
            bpy.data.objects.remove(o)
    drop=[k.lower() for k in cfg.get('drop',[])]
    for o in list(meshes):
        if any(k in o.name.lower() for k in drop):
            meshes.remove(o); bpy.data.objects.remove(o)
    bpy.ops.object.select_all(action='DESELECT')
    for o in meshes: o.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    bpy.ops.object.join()
    ob = bpy.context.view_layer.objects.active
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    ob.rotation_euler[2] = math.radians(cfg.get('yaw', 0))
    bpy.context.view_layer.update()
    mn, mx = frame_camera(ob, cfg, W, H)
    print('BBOX', tuple(round(x, 2) for x in mn), tuple(round(x, 2) for x in mx), 'faces', len(ob.data.polygons))
    bpy.context.scene.render.filepath = cfg['out']
    bpy.ops.render.render(write_still=True)
