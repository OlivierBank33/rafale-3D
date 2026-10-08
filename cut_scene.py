"""« N coupes » sur un Rafale (Blender Workbench, rendu rapide).
Usage : python3 cut_scene.py test            -> une image de test
        python3 cut_scene.py render A B      -> frames A..B-1 dans cut/f_XXXX.png
Chronologie : LEVELS (n coupes, début, durée). Couper = bisect + rebouchage (faces de coupe colorées)."""
import bpy, bmesh, math, sys, os, json, random
from mathutils import Vector, Matrix, Euler

FPS = 30
OUT = '/home/claude/cut/'
os.makedirs(OUT, exist_ok=True)
SKIP = ["door", "strut", "hub", "wheel", "gearbox", "lights", "hook", "damocles", "exocet", "gbu", "meteor", "mica", "fueltank", "pylon", "seat", "cockpittub", "camera"]
LEVELS = [(1, 0.0, 9.0), (2, 9.0, 9.0), (3, 18.0, 9.5), (5, 27.5, 10.0), (7, 37.5, 10.5), (12, 48.0, 12.0)]
TOTAL = 64.0
KNIFE_T = 1.2        # 1re coupe à t0 + 1.2 s
GAP = 0.32           # entre deux coupes
CUT_COL = (0.92, 0.28, 0.12, 1)


def planes_for(n, seed):
    """Plans de coupe : d'abord des tranches transversales, puis des coupes en biais."""
    r = random.Random(seed); P = []
    base = [(Vector((0, 0, 0.6)), Vector((0, 1, 0.18)))]
    trans = [-0.33, 0.33, -0.66, 0.66, 0.0]
    for k in range(n):
        if k == 0: co, no = Vector((0, 0.05, 0.6)), Vector((0.05, 1, 0.2))
        elif k < 5:
            y = trans[(k - 1) % 5] * 6.5; co = Vector((0, y, 0.6)); no = Vector((r.uniform(-0.25, 0.25), 1, r.uniform(-0.3, 0.3)))
        else:
            co = Vector((r.uniform(-1.5, 1.5), r.uniform(-4, 4), 0.6)); no = Vector((r.uniform(-1, 1), r.uniform(-0.5, 0.5), r.uniform(-0.2, 0.6)))
            if k % 2: no = Vector((1, r.uniform(-0.3, 0.3), r.uniform(-0.2, 0.2)))
        P.append((co, no.normalized()))
    return P


def build_base():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath='/home/claude/fg/rafale.glb')
    for o in list(bpy.data.objects):
        if o.type != 'MESH' or any(s in o.name.lower() for s in SKIP): bpy.data.objects.remove(o, do_unlink=True)
    meshes = [o for o in bpy.data.objects if o.type == 'MESH']
    for o in meshes: o.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.join()
    base = bpy.context.view_layer.objects.active; base.name = 'RAF'
    for o in list(bpy.data.objects):
        if o.type != 'MESH': bpy.data.objects.remove(o, do_unlink=True)
    # centrer, mettre à l'échelle (longueur ~ 8 u), poser à z ~ 0.6
    bb = [base.matrix_world @ Vector(c) for c in base.bound_box]
    mn = Vector((min(v.x for v in bb), min(v.y for v in bb), min(v.z for v in bb))); mx = Vector((max(v.x for v in bb), max(v.y for v in bb), max(v.z for v in bb)))
    ctr = (mn + mx) / 2; s = 8.0 / (mx.y - mn.y)
    me = base.data
    bm0 = bmesh.new(); bm0.from_mesh(me); bmesh.ops.remove_doubles(bm0, verts=bm0.verts, dist=1e-3); bm0.to_mesh(me); bm0.free()
    me.transform(Matrix.Translation(-ctr)); me.transform(Matrix.Scale(s, 4)); me.transform(Matrix.Translation((0, 0, 1.2)))
    cm = bpy.data.materials.new('CUT'); cm.diffuse_color = CUT_COL; cm.roughness = 0.6
    me.materials.append(cm)
    return base, len(me.materials) - 1


def cut_pieces(base, cut_mi, planes):
    pieces = [base.data.copy()]
    for (co, no) in planes:
        co = co + Vector((0, 0, 0.6))
        new = []
        for me in pieces:
            for side in (1, -1):
                bm = bmesh.new(); bm.from_mesh(me)
                geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
                res = bmesh.ops.bisect_plane(bm, geom=geom, plane_co=co, plane_no=no * side, clear_inner=False, clear_outer=True, dist=1e-5)
                cut_edges = [e for e in res['geom_cut'] if isinstance(e, bmesh.types.BMEdge)]
                if not bm.faces: bm.free(); continue
                bnd = [e for e in cut_edges if e.is_valid and e.is_boundary]
                if bnd:
                    try:
                        r2 = bmesh.ops.holes_fill(bm, edges=bnd, sides=0)
                        for f in r2['faces']: f.material_index = cut_mi
                    except Exception:
                        pass
                m2 = bpy.data.meshes.new('pc'); bm.to_mesh(m2); bm.free()
                for mat in me.materials: m2.materials.append(mat)
                if len(m2.polygons) > 20: new.append(m2)
        pieces = new
    for me in pieces:   # coque intérieure : copie retournée, couleur de coupe (visible de l'intérieur grâce au backface culling)
        bm = bmesh.new(); bm.from_mesh(me)
        dup = bmesh.ops.duplicate(bm, geom=bm.faces[:])
        nf = [g for g in dup['geom'] if isinstance(g, bmesh.types.BMFace)]
        bmesh.ops.reverse_faces(bm, faces=nf)
        for f in nf: f.material_index = cut_mi
        bm.to_mesh(me); bm.free()
    return pieces


def setup_world():
    sc = bpy.context.scene
    sc.render.engine = 'BLENDER_WORKBENCH'
    sh = sc.display.shading
    sh.light = 'STUDIO'; sh.color_type = 'TEXTURE'; sh.show_shadows = True; sh.shadow_intensity = 0.55
    sh.show_cavity = True; sh.cavity_type = 'BOTH'; sh.curvature_ridge_factor = 0.6; sh.curvature_valley_factor = 0.8
    sh.show_specular_highlight = True; sh.show_backface_culling = True; sh.background_type = 'VIEWPORT'
    sh.background_color = (0.30, 0.31, 0.34) if hasattr(sh, 'background_color') else None
    sc.display.shading.single_color = (0.6, 0.6, 0.6)
    sc.render.film_transparent = True
    sc.display.render_aa = '5'
    sc.render.resolution_x = 720; sc.render.resolution_y = 1280
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.exposure = 1.1
    # sol (planche) + ombre
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -1.05)); board = bpy.context.object; board.scale = (3.2, 7.2, 0.18)
    bm_ = bpy.data.materials.new('wood'); bm_.diffuse_color = (0.72, 0.52, 0.33, 1); board.data.materials.append(bm_)
    bpy.ops.mesh.primitive_plane_add(size=600, location=(0, 0, -1.15)); fl = bpy.context.object
    fm = bpy.data.materials.new('floor'); fm.diffuse_color = (0.33, 0.34, 0.37, 1); fl.data.materials.append(fm)
    cam = bpy.data.cameras.new('cam'); cam.lens = 50; co = bpy.data.objects.new('cam', cam); sc.collection.objects.link(co); sc.camera = co
    return co


def knife():
    bm = bmesh.new()
    # lame : triangle allongé épais 0.03 (plan local XZ, épaisseur Y)
    pts = [(-0.15, 0, 0), (3.6, 0, 0.08), (4.0, 0, 0.6), (-0.15, 0, 0.95)]
    vs1 = [bm.verts.new((x, -0.015, z)) for x, _, z in pts]; vs2 = [bm.verts.new((x, 0.015, z)) for x, _, z in pts]
    bm.faces.new(vs1); bm.faces.new(vs2[::-1])
    for i in range(4): bm.faces.new((vs1[i], vs1[(i + 1) % 4], vs2[(i + 1) % 4], vs2[i]))
    me = bpy.data.meshes.new('knife'); bm.to_mesh(me); bm.free()
    k = bpy.data.objects.new('knife', me); bpy.context.scene.collection.objects.link(k)
    mt = bpy.data.materials.new('steel'); mt.diffuse_color = (0.95, 0.96, 0.98, 1); mt.metallic = 0.0; mt.roughness = 0.2; me.materials.append(mt)
    bpy.ops.mesh.primitive_cube_add(size=1); h = bpy.context.object; h.scale = (1.1, 0.09, 0.42); h.location = (-0.7, 0, 0.27); h.parent = k
    hm = bpy.data.materials.new('handle'); hm.diffuse_color = (0.35, 0.2, 0.1, 1); h.data.materials.append(hm)
    return k


def ease(u):
    u = min(max(u, 0), 1); return u * u * (3 - 2 * u)


def main(mode, a=0, b=0):
    base, cut_mi = build_base()
    cam = setup_world()
    K = knife()
    lv_objs = []
    for li, (n, t0, dur) in enumerate(LEVELS):
        P = planes_for(n, 11 + li)
        meshes = cut_pieces(base, cut_mi, P)
        objs = []
        for m in meshes:
            o = bpy.data.objects.new('p', m); bpy.context.scene.collection.objects.link(o)
            # direction d'éclatement : centre de la pièce
            c = sum((v.co for v in m.vertices), Vector()) / max(1, len(m.vertices))
            d = c - Vector((0, 0, 1.2)); d.z *= 0.5
            if d.length < 1e-3: d = Vector((0, 0, 1))
            o['dx'], o['dy'], o['dz'] = d.normalized() * (0.5 + 0.06 * n)
            o['cx'], o['cy'], o['cz'] = c
            o['rs'] = random.Random(len(objs) + li * 100).uniform(-1, 1)
            o.hide_render = True; objs.append(o)
        lv_objs.append((P, objs))
        print('level', n, 'pieces', len(objs), flush=True)
    base.hide_render = True

    def place(t):
        li = max(i for i, l in enumerate(LEVELS) if l[1] <= t) if t >= 0 else 0
        n, t0, dur = LEVELS[li]; lt = t - t0
        P, objs = lv_objs[li]
        t_burst = KNIFE_T + GAP * (n - 1) + 0.25
        for j, (P2, ob2) in enumerate(lv_objs):
            for o in ob2: o.hide_render = True
        if lt < t_burst:
            base.hide_render = False
            base.location = (0, 0, 0.05 * math.sin(lt * 1.3))
        else:
            base.hide_render = True
            u = ease((lt - t_burst) / 2.2) + 0.08 * max(0, lt - t_burst - 2.2)
            for o in objs:
                o.hide_render = False
                d = Vector((o['dx'], o['dy'], o['dz']))
                o.location = d * u
                ang = o['rs'] * 0.35 * u
                c = Vector((o['cx'], o['cy'], o['cz']))
                R = Matrix.Translation(c) @ Euler((ang * 0.6, ang * 0.3, ang), 'XYZ').to_matrix().to_4x4() @ Matrix.Translation(-c)
                o.matrix_world = Matrix.Translation(d * u) @ R
        # couteau : passe k-ième dans le plan k
        K.hide_render = True; K.children[0].hide_render = True
        for k, (co, no) in enumerate(P):
            tk = KNIFE_T + GAP * k
            if tk - 0.12 <= lt <= tk + 0.16:
                v = (lt - (tk - 0.12)) / 0.28
                co2 = co + Vector((0, 0, 0.6))
                up = Vector((0, 0, 1)); dv = (up - no * up.dot(no)).normalized() if abs(no.z) < 0.95 else Vector((1, 0, 0))
                side = no.cross(dv).normalized()
                pos = co2 + dv * (3.4 - 7.2 * v) - side * 1.3
                M = Matrix((side, dv, no)).transposed()      # colonnes : x=side, y=dv(?), z=no
                rot = Matrix((side, no, dv)).transposed().to_4x4()
                K.matrix_world = Matrix.Translation(pos) @ rot
                K.hide_render = False; K.children[0].hide_render = False
        # caméra : orbite lente
        az = math.radians(238 + 8 * math.sin(t * 0.12)); el = math.radians(24); R_ = 17.5
        cam.location = (R_ * math.cos(el) * math.cos(az), R_ * math.cos(el) * math.sin(az), 1.0 + R_ * math.sin(el))
        tgt = Vector((0, 0, 0.7)); dirv = tgt - cam.location
        cam.rotation_euler = dirv.to_track_quat('-Z', 'Y').to_euler()

    if mode == 'test':
        for tt in (4.0, 15.0, 33.0, 58.0):
            place(tt); bpy.context.scene.render.filepath = OUT + f'test_{tt}.png'; bpy.ops.render.render(write_still=True)
        return
    rng_ = range(a, b) if a >= 0 else [int(x) for x in open('/tmp/claude-0/kframes.txt').read().split()[b::2]]
    for f in rng_:
        t = f / FPS; place(t)
        bpy.context.scene.render.filepath = OUT + f'f_{f:04d}.png'; bpy.ops.render.render(write_still=True)


if __name__ == '__main__':
    args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    if args[0] == 'test': main('test')
    else: main('render', int(args[1]), int(args[2]))
