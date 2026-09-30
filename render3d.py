"""Chargeur AC3D (FlightGear) + rendu Cycles. Usage : python3 render3d.py config.json"""
import bpy, bmesh, sys, os, json, math
from mathutils import Matrix, Vector


def parse_ac(path):
    with open(path, 'r', errors='ignore') as f:
        lines = f.read().split('\n')
    i = 0
    mats = []
    objs = []  # (name, texture, texrep, texoff, verts_world, surfs)

    def tok(l):
        out, cur, q = [], '', False
        for ch in l:
            if ch == '"':
                q = not q; continue
            if ch.isspace() and not q:
                if cur: out.append(cur); cur = ''
            else:
                cur += ch
        if cur: out.append(cur)
        return out

    def read_obj(parent_m):
        nonlocal i
        name, tex, texrep, texoff = '', None, (1, 1), (0, 0)
        rot = Matrix.Identity(3); loc = Vector((0, 0, 0))
        verts, surfs = [], []
        while i < len(lines):
            t = tok(lines[i]); i += 1
            if not t:
                continue
            k = t[0]
            if k == 'name': name = t[1] if len(t) > 1 else ''
            elif k == 'data':
                n = int(t[1]); consumed = 0
                while consumed < n and i < len(lines):
                    consumed += len(lines[i]) + 1; i += 1
            elif k == 'texture': tex = t[1]
            elif k == 'texrep': texrep = (float(t[1]), float(t[2]))
            elif k == 'texoff': texoff = (float(t[1]), float(t[2]))
            elif k == 'rot':
                v = list(map(float, t[1:10])); rot = Matrix((v[0:3], v[3:6], v[6:9])).transposed()
            elif k == 'loc': loc = Vector(map(float, t[1:4]))
            elif k == 'numvert':
                n = int(t[1])
                for _ in range(n):
                    verts.append(Vector(map(float, lines[i].split()[:3]))); i += 1
            elif k == 'numsurf':
                n = int(t[1])
                for _ in range(n):
                    flags = mat = 0; refs = []
                    while True:
                        tt = lines[i].split(); i += 1
                        if not tt: continue
                        if tt[0] == 'SURF': flags = int(tt[1], 16)
                        elif tt[0] == 'mat': mat = int(tt[1])
                        elif tt[0] == 'refs':
                            m = int(tt[1])
                            for _ in range(m):
                                r = lines[i].split(); i += 1
                                refs.append((int(r[0]), float(r[1]) if len(r) > 1 else 0, float(r[2]) if len(r) > 2 else 0))
                            break
                    if (flags & 0x0F) == 0 and len(refs) >= 3:
                        surfs.append((mat, refs, bool(flags & 0x10)))
            elif k == 'kids':
                m = Matrix.Translation(loc) @ rot.to_4x4()
                world = parent_m @ m
                wv = [world @ v for v in verts]
                objs.append((name, tex, texrep, texoff, wv, surfs))
                for _ in range(int(t[1])):
                    # attendre la ligne OBJECT
                    while i < len(lines) and not lines[i].startswith('OBJECT'):
                        i += 1
                    i += 1
                    read_obj(world)
                return

    while i < len(lines):
        l = lines[i]
        if l.startswith('MATERIAL'):
            t = tok(l)
            d = {t[j]: t[j + 1:j + 4] for j in range(len(t)) if t[j] in ('rgb', 'amb', 'emis', 'spec')}
            tr = float(t[t.index('trans') + 1]) if 'trans' in t else 0
            shi = float(t[t.index('shi') + 1]) if 'shi' in t else 10
            mats.append(dict(rgb=tuple(map(float, d.get('rgb', [0.8] * 3))), trans=tr, shi=shi, name=t[1] if len(t) > 1 else ''))
            i += 1
        elif l.startswith('OBJECT'):
            i += 1
            read_obj(Matrix.Identity(4))
        else:
            i += 1
    return mats, objs


_img_cache = {}


def find_tex(acdir, tex, extra_dirs):
    cands = [os.path.join(acdir, tex)] + [os.path.join(d, os.path.basename(tex)) for d in extra_dirs]
    base, _ = os.path.splitext(tex)
    for c in list(cands):
        for ext in ('.png', '.rgb', '.jpg', '.dds', '.sgi', '.bmp'):
            cands.append(os.path.splitext(c)[0] + ext)
    for c in cands:
        if os.path.exists(c):
            return c
    return None


def make_material(m, texpath, key, cfg):
    if key in _img_cache:
        return _img_cache[key]
    mat = bpy.data.materials.new(name=key[:60])
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes['Principled BSDF']
    r, g, b = m['rgb']
    bsdf.inputs['Base Color'].default_value = (r, g, b, 1)
    bsdf.inputs['Roughness'].default_value = cfg.get('roughness', 0.38)
    bsdf.inputs['Metallic'].default_value = cfg.get('metallic', 0.15)
    if texpath:
        try:
            img = bpy.data.images.load(texpath, check_existing=True)
            tn = nt.nodes.new('ShaderNodeTexImage'); tn.image = img
            mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.blend_type = 'MULTIPLY'
            mix.inputs['Factor'].default_value = cfg.get('tint', 0.0)
            nt.links.new(tn.outputs['Color'], mix.inputs['A'])
            mix.inputs['B'].default_value = (r, g, b, 1)
            nt.links.new(mix.outputs['Result'], bsdf.inputs['Base Color'])
            if img.depth in (32, 64, 128) or img.channels == 4:
                nt.links.new(tn.outputs['Alpha'], bsdf.inputs['Alpha'])
        except Exception as e:
            print('tex fail', texpath, e)
    if m['trans'] > 0.05:
        bsdf.inputs['Alpha'].default_value = max(0.12, 1 - m['trans'])
        bsdf.inputs['Roughness'].default_value = 0.05
        bsdf.inputs['Base Color'].default_value = (0.05, 0.07, 0.1, 1)
    _img_cache[key] = mat
    return mat


def load_model(path, cfg):
    mats, objs = parse_ac(path)
    acdir = os.path.dirname(path)
    extra = [os.path.join(os.path.dirname(path), d) for d in cfg.get('texdirs', [])]
    skip = [s.lower() for s in cfg.get('skip', [])] + ['propellerdisk', 'disk', 'shadow', 'collision', 'lightcone', 'light-cone', 'light_cone', 'halo']
    me = bpy.data.meshes.new('plane')
    bm = bmesh.new()
    uvl = bm.loops.layers.uv.new()
    matlist = []
    matindex = {}
    for (name, tex, texrep, texoff, wv, surfs) in objs:
        if any(s in (name or '').lower() for s in skip):
            continue
        if not surfs:
            continue
        bverts = [bm.verts.new(v) for v in wv]
        texpath = find_tex(acdir, tex, extra) if tex else None
        for (mi, refs, smooth) in surfs:
            mi = min(mi, len(mats) - 1)
            key = f"{mi}|{texpath}"
            if key not in matindex:
                matindex[key] = len(matlist)
                matlist.append(make_material(mats[mi], texpath, key, cfg))
            try:
                vs = [bverts[r[0]] for r in refs]
                if len(set(vs)) < 3:
                    continue
                f = bm.faces.new(vs)
            except (ValueError, IndexError):
                continue
            f.material_index = matindex[key]
            f.smooth = smooth
            for lp, r in zip(f.loops, refs):
                lp[uvl].uv = (r[1] * texrep[0] + texoff[0], r[2] * texrep[1] + texoff[1])
    bm.to_mesh(me); bm.free()
    for m in matlist:
        me.materials.append(m)
    ob = bpy.data.objects.new('plane', me)
    bpy.context.scene.collection.objects.link(ob)
    # AC : y vers le haut -> Blender z vers le haut
    ob.rotation_euler = (math.radians(90), 0, 0)
    bpy.context.view_layer.update()
    try:
        me.set_sharp_from_angle(angle=math.radians(40))
    except Exception:
        pass
    return ob


def setup_scene(cfg, W, H):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'CPU'
    sc.cycles.samples = cfg.get('samples', 48)
    sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = W, H
    sc.render.film_transparent = True
    sc.view_settings.view_transform = 'AgX'
    sc.view_settings.look = 'AgX - Medium High Contrast'
    sc.view_settings.exposure = cfg.get('exposure', -0.35)
    world = bpy.data.worlds.new('w'); sc.world = world; world.use_nodes = True
    bg = world.node_tree.nodes['Background']
    sky = world.node_tree.nodes.new('ShaderNodeTexSky')
    try:
        sky.sky_type = 'NISHITA'; sky.sun_elevation = math.radians(35); sky.sun_rotation = math.radians(40)
    except Exception:
        pass
    world.node_tree.links.new(sky.outputs['Color'], bg.inputs['Color'])
    bg.inputs['Strength'].default_value = 0.35
    sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = cfg.get('sun', 2.2); sun.angle = math.radians(2)
    so = bpy.data.objects.new('sun', sun); sc.collection.objects.link(so)
    so.rotation_euler = (math.radians(40), math.radians(-15), math.radians(35))
    rim = bpy.data.lights.new('rim', 'SUN'); rim.energy = 2.0; rim.color = (0.6, 0.75, 1.0)
    ro = bpy.data.objects.new('rim', rim); sc.collection.objects.link(ro)
    ro.rotation_euler = (math.radians(-60), 0, math.radians(200))


def frame_camera(ob, cfg, W, H):
    sc = bpy.context.scene
    bb = [ob.matrix_world @ Vector(c) for c in ob.bound_box]
    mn = Vector((min(v[k] for v in bb) for k in range(3)))
    mx = Vector((max(v[k] for v in bb) for k in range(3)))
    center = (mn + mx) / 2
    size = (mx - mn).length
    cam = bpy.data.cameras.new('cam'); cam.lens = cfg.get('lens', 50)
    co = bpy.data.objects.new('cam', cam); sc.collection.objects.link(co); sc.camera = co
    az = math.radians(cfg.get('az', 35)); el = math.radians(cfg.get('el', 18))
    d = size * cfg.get('dist', 1.0)
    co.location = center + Vector((math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el))) * d
    direction = center - co.location
    co.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    if cfg.get('roll'):
        co.rotation_euler.rotate_axis('Z', math.radians(cfg['roll']))
    return mn, mx


if __name__ == '__main__':
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    cfg = json.load(open(argv[0]))
    W, H = cfg.get('W', 1080), cfg.get('H', 1080)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    setup_scene(cfg, W, H)
    ob = load_model(cfg['ac'], cfg)
    if cfg.get('flip'):
        ob.rotation_euler[2] = math.radians(180)
    bpy.context.view_layer.update()
    mn, mx = frame_camera(ob, cfg, W, H)
    print('BBOX', tuple(round(x, 2) for x in mn), tuple(round(x, 2) for x in mx), 'faces', len(ob.data.polygons))
    bpy.context.scene.render.filepath = cfg['out']
    bpy.ops.render.render(write_still=True)
