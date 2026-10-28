"""Plaques de décor « Andes » rendues dans Blender/Cycles : terrain fractal (crêtes, glacier), neige + roche selon la pente, ciel Nishita, brume.
Usage : python3 pr/andes_plates.py [plaque ...]  -> pr/p_<plaque>.png (1080x1920 ou plus large pour les panoramiques).
Plaques : andes_day (survol, caméra haute), glacier (fond de vallée, glacier en pente douce au centre, pour l'épave), glacier_dusk, glacier_night,
ridge (crête proche dans les nuages), andes_dawn."""
import bpy, bmesh, sys, math, os
import numpy as np
from mathutils import Vector

OUT = '/home/claude/pr/'


def heightfield(n=480, size=14000.0, seed=3, valley=False, hmax=2000.0, octs=(100, 50, 25, 12, 6, 3)):
    r = np.random.default_rng(seed)
    def noise(sc):
        g = r.random((n // sc + 3, n // sc + 3))
        from scipy import ndimage
        z = ndimage.zoom(g, sc, order=3)[:n, :n]
        return (z - z.min()) / (z.max() - z.min())
    z = np.zeros((n, n))
    amp = 1.0
    for sc in octs:
        rn = 1 - np.abs(noise(sc) * 2 - 1)
        z += (rn ** 2) * amp; amp *= 0.5
    z = z / z.max()
    ys, xs = np.mgrid[0:n, 0:n] / (n - 1)
    h = hmax * z ** 1.25
    if valley:                                   # vallée glaciaire orientée vers la caméra (axe y), fond lisse et incliné
        d = np.abs(xs - 0.5 - 0.06 * np.sin(ys * 5))
        carve = np.exp(-(d / 0.11) ** 2)
        floor = 200 + 700 * ys
        h = h * (1 - carve) + (floor + 80 * z) * carve
        h += 1800 * np.clip(d - 0.1, 0, 1) * 2.2
    return h, size


def build_terrain(h, size, name='terrain'):
    n = h.shape[0]
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    vs = []
    for j in range(n):
        for i in range(n):
            vs.append(bm.verts.new(((i / (n - 1) - 0.5) * size, (j / (n - 1) - 0.5) * size, float(h[j, i]))))
    for j in range(n - 1):
        for i in range(n - 1):
            a = j * n + i
            bm.faces.new((vs[a], vs[a + 1], vs[a + n + 1], vs[a + n]))
    bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    mat = bpy.data.materials.new('snow'); mat.use_nodes = True; nt = mat.node_tree
    bs = nt.nodes['Principled BSDF']
    geo = nt.nodes.new('ShaderNodeNewGeometry'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(geo.outputs['Normal'], sep.inputs[0])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.55; ramp.color_ramp.elements[0].color = (0.10, 0.095, 0.095, 1)
    ramp.color_ramp.elements[1].position = 0.70; ramp.color_ramp.elements[1].color = (0.86, 0.89, 0.95, 1)
    tex = nt.nodes.new('ShaderNodeTexNoise'); tex.inputs['Scale'].default_value = 0.004
    mix = nt.nodes.new('ShaderNodeMath'); mix.operation = 'ADD'
    mul = nt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = 0.12
    nt.links.new(tex.outputs['Fac'], mul.inputs[0])
    nt.links.new(sep.outputs['Z'], mix.inputs[0]); nt.links.new(mul.outputs[0], mix.inputs[1])
    nt.links.new(mix.outputs[0], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bs.inputs['Base Color'])
    bs.inputs['Roughness'].default_value = 0.55
    tc = nt.nodes.new('ShaderNodeTexCoord')
    n1 = nt.nodes.new('ShaderNodeTexNoise'); n1.inputs['Scale'].default_value = 0.35; n1.inputs['Detail'].default_value = 6
    n2 = nt.nodes.new('ShaderNodeTexNoise'); n2.inputs['Scale'].default_value = 0.02; n2.inputs['Detail'].default_value = 4
    nt.links.new(tc.outputs['Object'], n1.inputs['Vector']); nt.links.new(tc.outputs['Object'], n2.inputs['Vector'])
    b1 = nt.nodes.new('ShaderNodeBump'); b1.inputs['Strength'].default_value = 0.25
    b2 = nt.nodes.new('ShaderNodeBump'); b2.inputs['Strength'].default_value = 0.35
    nt.links.new(n1.outputs['Fac'], b1.inputs['Height']); nt.links.new(n2.outputs['Fac'], b2.inputs['Height'])
    nt.links.new(b1.outputs['Normal'], b2.inputs['Normal']); nt.links.new(b2.outputs['Normal'], bs.inputs['Normal'])
    try:
        bs.inputs['Subsurface Weight'].default_value = 0.08
    except Exception:
        pass
    me.materials.append(mat)
    return ob


def scene(W, H, sun_el, sun_az, strength=1.0, exposure=-0.6, samples=32):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = samples; sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = W, H
    sc.render.film_transparent = True
    sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'; sc.view_settings.exposure = exposure
    world = bpy.data.worlds.new('w'); sc.world = world; world.use_nodes = True
    bg = world.node_tree.nodes['Background']
    sky = world.node_tree.nodes.new('ShaderNodeTexSky')
    try:
        sky.sky_type = 'NISHITA'; sky.sun_elevation = math.radians(sun_el); sky.sun_rotation = math.radians(sun_az); sky.altitude = 3600
        try:
            sky.air_density = 0.55; sky.dust_density = 0.4
        except Exception: pass
    except Exception:
        pass
    world.node_tree.links.new(sky.outputs['Color'], bg.inputs['Color']); bg.inputs['Strength'].default_value = strength
    sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 3.5 * max(0.15, math.sin(math.radians(max(sun_el, 2)))); sun.angle = math.radians(1)
    sun.color = (1.0, 0.93, 0.82) if sun_el > 8 else (1.0, 0.62, 0.38)
    so = bpy.data.objects.new('sun', sun); sc.collection.objects.link(so)
    so.rotation_euler = (math.radians(90 - sun_el), 0, math.radians(sun_az + 90))
    return sc


def camera(loc, look, lens=28):
    cam = bpy.data.cameras.new('cam'); cam.lens = lens; cam.clip_end = 200000
    co = bpy.data.objects.new('cam', cam); bpy.context.scene.collection.objects.link(co); bpy.context.scene.camera = co
    co.location = Vector(loc); co.rotation_euler = (Vector(look) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()


def haze_pass(sc, amount):
    """brume atmosphérique via la passe Mist du compositeur (un volume « monde » rend tout noir dans Cycles)."""
    vl = sc.view_layers[0]; vl.use_pass_mist = True
    sc.world.mist_settings.start = 2000; sc.world.mist_settings.depth = 30000; sc.world.mist_settings.falloff = 'QUADRATIC'
    sc.use_nodes = True
    try:
        nt = sc.compositing_node_group if hasattr(sc, 'compositing_node_group') and sc.compositing_node_group else sc.node_tree
    except Exception:
        nt = None
    if nt is None:
        try:
            nt = bpy.data.node_groups.new('comp', 'CompositorNodeTree'); sc.compositing_node_group = nt
        except Exception:
            return
    for n in list(nt.nodes): nt.nodes.remove(n)
    rl = nt.nodes.new('CompositorNodeRLayers')
    mixn = nt.nodes.new('CompositorNodeMixRGB') if hasattr(bpy.types, 'CompositorNodeMixRGB') else None
    try:
        out = nt.nodes.new('CompositorNodeComposite')
    except Exception:
        out = nt.nodes.new('NodeGroupOutput'); nt.interface.new_socket('Image', in_out='OUTPUT', socket_type='NodeSocketColor')
    if mixn is None:
        nt.links.new(rl.outputs['Image'], out.inputs[0]); return
    mixn.inputs[2].default_value = (0.72, 0.8, 0.94, 1)
    mul = nt.nodes.new('CompositorNodeMath'); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = min(1.0, amount * 20000)
    nt.links.new(rl.outputs['Mist'], mul.inputs[0]); nt.links.new(mul.outputs[0], mixn.inputs[0])
    nt.links.new(rl.outputs['Image'], mixn.inputs[1]); nt.links.new(mixn.outputs[0], out.inputs[0])


def mist(sc, density=0.00004, col=(0.75, 0.82, 0.95)):
    w = sc.world; nt = w.node_tree
    vol = nt.nodes.new('ShaderNodeVolumePrincipled'); vol.inputs['Density'].default_value = density
    vol.inputs['Color'].default_value = (*col, 1)
    nt.links.new(vol.outputs[0], nt.nodes['World Output'].inputs['Volume'])


PL = {
    'andes_day': dict(W=1300, H=1920, sun_el=24, sun_az=200, valley=False, seed=3, cam=(0, -9000, 4300), look=(0, 3000, 1300), lens=24, mist=0.0, exposure=-1.4, strength=0.5),
    'ridge': dict(W=1300, H=1920, sun_el=20, sun_az=150, valley=False, seed=8, cam=(0, -6500, 1700), look=(0, 3000, 1500), lens=28, mist=0.0, exposure=-1.4, strength=0.5),
    'glacier': dict(W=1300, H=1920, sun_el=18, sun_az=200, valley=True, seed=5, cam=(0, -6800, 520), look=(0, 2000, 900), lens=30, mist=0.0, exposure=-1.9, strength=0.45),
    'glacier_dusk': dict(W=1300, H=1920, sun_el=3, sun_az=200, valley=True, seed=5, cam=(0, -6800, 520), look=(0, 2000, 900), lens=30, mist=0.00001, exposure=-0.4, strength=0.6),
    'glacier_night': dict(W=1300, H=1920, sun_el=-8, sun_az=200, valley=True, seed=5, cam=(0, -6800, 520), look=(0, 2000, 900), lens=30, mist=0.0, strength=0.5, exposure=0.8, moon=True),
    'andes_dawn': dict(W=1300, H=1920, sun_el=5, sun_az=110, valley=False, seed=3, cam=(0, -9000, 4300), look=(0, 3000, 1300), lens=24, mist=0.00002, exposure=-0.7, strength=0.6),
}


def render(name):
    p = dict(PL[name])
    if os.environ.get('PREVIEW'):
        p['W'] //= 4; p['H'] //= 4; p['samples'] = 8
    sc = scene(p['W'], p['H'], p['sun_el'], p['sun_az'], p.get('strength', 1.0), p.get('exposure', -0.6), p.get('samples', 32))
    h, size = heightfield(seed=p['seed'], valley=p['valley'])
    build_terrain(h, size)
    hf, sf = heightfield(n=160, size=160000.0, seed=p['seed'] + 40, hmax=5200.0, octs=(40, 20, 10, 5))
    nn = hf.shape[0]; yy, xx = (np.mgrid[0:nn, 0:nn] / (nn - 1) - 0.5) * sf; rr_ = np.hypot(xx, yy)
    hf = hf * np.clip((rr_ - 9000) / 8000, 0, 1) - 600.0 * (rr_ < 9000)
    far = build_terrain(hf, sf, 'far')
    camera(p['cam'], p['look'], p['lens'])
    if p.get('mist'): haze_pass(sc, p['mist'])
    if p.get('moon'):
        moon = bpy.data.lights.new('moon', 'SUN'); moon.energy = 0.25; moon.color = (0.6, 0.7, 1.0)
        mo = bpy.data.objects.new('moon', moon); sc.collection.objects.link(mo); mo.rotation_euler = (math.radians(50), 0, math.radians(150))
    sc.render.filepath = OUT + f'p_{name}.png'
    bpy.ops.render.render(write_still=True)
    print('DONE', name, flush=True)


if __name__ == '__main__':
    names = sys.argv[1:] or list(PL)
    for n in names: render(n)
