# DEIMOS — the org hero. Mars rises, the moon Deimos crosses, and the mark (a real tetrahedron in a ring) tumbles,
# then locks top-down into the exact flat logo: seen from above, a regular tetrahedron IS the Deimos mark.
#   Blender -b --factory-startup -P hero.py -- OUTDIR [scale%] [samples]
import bpy, math, sys, mathutils
from mathutils import Vector, Euler, Quaternion
argv = sys.argv[sys.argv.index('--') + 1:]
OUT = argv[0]; SCALE = int(argv[1]) if len(argv) > 1 else 100; SAMPLES = int(argv[2]) if len(argv) > 2 else 32
F_END = 216

sc = bpy.context.scene
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
try: sc.render.engine = 'BLENDER_EEVEE'
except TypeError: sc.render.engine = 'BLENDER_EEVEE_NEXT'
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1280, 544, SCALE
sc.render.fps = 24; sc.frame_start, sc.frame_end = 1, F_END
sc.render.image_settings.file_format = 'PNG'
sc.render.filepath = OUT.rstrip('/') + '/f_'
try: sc.eevee.taa_render_samples = SAMPLES
except Exception: pass
sc.view_settings.view_transform = 'AgX'
try: sc.view_settings.look = 'AgX - Punchy'
except Exception: pass

def mat(name, build):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    sock = build(nt)
    nt.links.new(sock, out.inputs['Surface'])
    return m

def emission(col, strength):
    def b(nt):
        e = nt.nodes.new('ShaderNodeEmission'); e.inputs['Color'].default_value = (*col, 1); e.inputs['Strength'].default_value = strength
        return e.outputs[0]
    return b

def key(obj_or_sock, path, frame, value, idx=None):
    setattr(obj_or_sock, path, value) if idx is None else None
    obj_or_sock.keyframe_insert(path, frame=frame) if idx is None else None

# ---------------------------------------------------------------- world: deep space with stars
w = bpy.data.worlds.new('space'); sc.world = w; w.use_nodes = True
nt = w.node_tree; nt.nodes.clear()
out = nt.nodes.new('ShaderNodeOutputWorld'); bg = nt.nodes.new('ShaderNodeBackground')
tc = nt.nodes.new('ShaderNodeTexCoord'); vor = nt.nodes.new('ShaderNodeTexVoronoi'); vor.inputs['Scale'].default_value = 220
nt.links.new(tc.outputs['Generated'], vor.inputs['Vector'])
ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].position = 0.0; ramp.color_ramp.elements[0].color = (1, 1, 1, 1)
ramp.color_ramp.elements[1].position = 0.06; ramp.color_ramp.elements[1].color = (0.0, 0.0, 0.0, 1)
nt.links.new(vor.outputs['Distance'], ramp.inputs['Fac'])
mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.inputs['Factor'].default_value = 1.0
mix.inputs['A'].default_value = (0.004, 0.003, 0.012, 1)
add = nt.nodes.new('ShaderNodeMath'); add.operation = 'MULTIPLY'
# acid nebula: two noise fields coloured violet → magenta → cyan, masked so it drifts in clouds, added to the stars
n1 = nt.nodes.new('ShaderNodeTexNoise'); n1.inputs['Scale'].default_value = 2.6; n1.inputs['Detail'].default_value = 9; n1.inputs['Roughness'].default_value = 0.62
n2 = nt.nodes.new('ShaderNodeTexNoise'); n2.inputs['Scale'].default_value = 3.4; n2.inputs['Detail'].default_value = 6
nt.links.new(tc.outputs['Generated'], n1.inputs['Vector']); nt.links.new(tc.outputs['Generated'], n2.inputs['Vector'])
neb = nt.nodes.new('ShaderNodeValToRGB'); cr = neb.color_ramp
cr.elements[0].position, cr.elements[0].color = 0.38, (0, 0, 0, 1)
cr.elements[1].position, cr.elements[1].color = 0.72, (0.0, 0.75, 0.95, 1)
e1 = cr.elements.new(0.5); e1.color = (0.10, 0.02, 0.26, 1)
e2 = cr.elements.new(0.6); e2.color = (0.75, 0.04, 0.55, 1)
nt.links.new(n1.outputs['Fac'], neb.inputs['Fac'])
mask = nt.nodes.new('ShaderNodeValToRGB'); mask.color_ramp.elements[0].position = 0.47; mask.color_ramp.elements[1].position = 0.74
nt.links.new(n2.outputs['Fac'], mask.inputs['Fac'])
mul = nt.nodes.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'; mul.inputs['Factor'].default_value = 1.0
nt.links.new(neb.outputs['Color'], mul.inputs['A']); nt.links.new(mask.outputs['Color'], mul.inputs['B'])
scl = nt.nodes.new('ShaderNodeVectorMath'); scl.operation = 'SCALE'; scl.inputs['Scale'].default_value = 0.55
nt.links.new(mul.outputs['Result'], scl.inputs[0])
addc = nt.nodes.new('ShaderNodeVectorMath'); addc.operation = 'ADD'
nt.links.new(ramp.outputs['Color'], addc.inputs[0]); nt.links.new(scl.outputs['Vector'], addc.inputs[1])
nt.links.new(addc.outputs['Vector'], bg.inputs['Color']); bg.inputs['Strength'].default_value = 1.4
nt.links.new(bg.outputs[0], out.inputs['Surface'])

# ---------------------------------------------------------------- Mars, lower right, with a rim of atmosphere
bpy.ops.mesh.primitive_uv_sphere_add(segments=128, ring_count=64, radius=22, location=(30, 60, -26))
mars = bpy.context.object; bpy.ops.object.shade_smooth()
def mars_surface(nt):
    tc = nt.nodes.new('ShaderNodeTexCoord'); n = nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = 3.2; n.inputs['Detail'].default_value = 12
    n2 = nt.nodes.new('ShaderNodeTexNoise'); n2.inputs['Scale'].default_value = 18; n2.inputs['Detail'].default_value = 8
    nt.links.new(tc.outputs['Object'], n.inputs['Vector']); nt.links.new(tc.outputs['Object'], n2.inputs['Vector'])
    r = nt.nodes.new('ShaderNodeValToRGB'); cr = r.color_ramp
    cr.elements[0].position, cr.elements[0].color = 0.30, (0.09, 0.02, 0.008, 1)
    cr.elements[1].position, cr.elements[1].color = 0.68, (0.55, 0.09, 0.02, 1)
    e = cr.elements.new(0.52); e.color = (0.33, 0.07, 0.02, 1)
    nt.links.new(n.outputs['Fac'], r.inputs['Fac'])
    p = nt.nodes.new('ShaderNodeBsdfPrincipled'); p.inputs['Roughness'].default_value = 0.95
    nt.links.new(r.outputs['Color'], p.inputs['Base Color'])
    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.8
    nt.links.new(n2.outputs['Fac'], bump.inputs['Height']); nt.links.new(bump.outputs['Normal'], p.inputs['Normal'])
    # atmosphere rim: a facing-based emission added on top
    lw = nt.nodes.new('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.08
    em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = (1.0, 0.42, 0.18, 1); em.inputs['Strength'].default_value = 5.0
    mul = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(lw.outputs['Facing'], mul.inputs['Fac']); nt.links.new(p.outputs[0], mul.inputs[1]); nt.links.new(em.outputs[0], mul.inputs[2])
    return mul.outputs[0]
mars.data.materials.append(mat('mars', mars_surface))
mars.rotation_euler = (0.3, 0, 0)
mars.keyframe_insert('rotation_euler', frame=1); mars.rotation_euler = (0.3, 0, 0.25); mars.keyframe_insert('rotation_euler', frame=F_END)
mars.location = (30, 60, -40); mars.keyframe_insert('location', frame=1)
mars.location = (30, 60, -27); mars.keyframe_insert('location', frame=120)

# ---------------------------------------------------------------- Deimos, the moon: small, lumpy, cratered
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=6, radius=1.0, location=(0, 0, 0))
moon = bpy.context.object; moon.scale = (2.0, 1.56, 1.32); bpy.ops.object.shade_smooth()
tex = bpy.data.textures.new('lumps', 'CLOUDS'); tex.noise_scale = 0.55
d = moon.modifiers.new('lumps', 'DISPLACE'); d.texture = tex; d.strength = 0.28
tex2 = bpy.data.textures.new('grit', 'CLOUDS'); tex2.noise_scale = 0.12
d2 = moon.modifiers.new('grit', 'DISPLACE'); d2.texture = tex2; d2.strength = 0.05
def moon_surface(nt):
    p = nt.nodes.new('ShaderNodeBsdfPrincipled'); p.inputs['Base Color'].default_value = (0.20, 0.17, 0.15, 1); p.inputs['Roughness'].default_value = 1.0
    return p.outputs[0]
moon.data.materials.append(mat('moon', moon_surface))
# it crosses the frame on a slow arc, passing behind the mark
for f, loc in ((1, (-17, 14, 6.5)), (110, (-8, 10, 5.4)), (F_END, (1.5, 9, 7.6))):
    moon.location = loc; moon.keyframe_insert('location', frame=f)
moon.rotation_euler = (0, 0, 0); moon.keyframe_insert('rotation_euler', frame=1)
moon.rotation_euler = (0.6, 1.4, 0.3); moon.keyframe_insert('rotation_euler', frame=F_END)

# ---------------------------------------------------------------- the mark: a regular tetrahedron in a ring
R = 2.4                                   # circumradius of the base triangle = the ring
pivot = bpy.data.objects.new('mark', None); sc.collection.objects.link(pivot)
apex_h = R * math.sqrt(2) * 0.5           # regular tetrahedron height relative to base circumradius R: h = R*sqrt(2)
apex_h = R * math.sqrt(2)
cz = apex_h / 4                           # centroid sits a quarter of the way up
base = [Vector((R * math.cos(math.radians(a)), R * math.sin(math.radians(a)), -cz)) for a in (90, 210, 330)]
apex = Vector((0, 0, apex_h - cz))
glow = mat('glow', emission((0.92, 0.97, 1.0), 14))
node_glow = mat('node', emission((1.0, 1.0, 1.0), 22))
def rod(a, b, r=0.055):
    v = b - a; L = v.length
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=r, depth=L, location=(a + b) / 2)
    o = bpy.context.object; o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(v.normalized())
    o.data.materials.append(glow); o.parent = pivot; return o
def node(p, r):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=r, location=p); o = bpy.context.object
    bpy.ops.object.shade_smooth(); o.data.materials.append(node_glow); o.parent = pivot; return o
for i in range(3): rod(base[i], base[(i + 1) % 3]); rod(base[i], apex, 0.05)
for p in base: node(p, 0.2)
node(apex, 0.27)
# the ring lies in the base plane, through the base vertices
bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=0.045, major_segments=192, minor_segments=16, location=(0, 0, -cz))
ring = bpy.context.object; ring.data.materials.append(mat('ringglow', emission((0.85, 0.92, 1.0), 9))); ring.parent = pivot
# acid accents: two faint coloured halo rings that breathe
for i, (col, rr) in enumerate((((1.0, 0.17, 0.84), R * 1.32), ((0.0, 0.9, 1.0), R * 1.55))):
    bpy.ops.mesh.primitive_torus_add(major_radius=rr, minor_radius=0.02, major_segments=192, minor_segments=8, location=(0, 0, -cz))
    h = bpy.context.object; hm = mat(f'halo{i}', emission(col, 6)); h.data.materials.append(hm); h.parent = pivot
    # acid: the halo rings cycle through the palette, out of phase with each other
    sock = [n for n in hm.node_tree.nodes if n.type == 'EMISSION'][0].inputs['Color']
    acid = [(1.0, 0.17, 0.84), (0.48, 0.36, 1.0), (0.0, 0.9, 1.0), (0.22, 1.0, 0.53), (1.0, 0.95, 0.23), (1.0, 0.48, 0.1)]
    for k in range(F_END // 24 + 2):
        sock.default_value = (*acid[(k + i * 3) % len(acid)], 1); sock.keyframe_insert('default_value', frame=1 + k * 24)

# camera looks along +Y; the logo view = the tetrahedron's apex pointing at the camera (-Y), one base vertex up
cam_d = bpy.data.cameras.new('cam'); cam_d.lens = 50; cam = bpy.data.objects.new('cam', cam_d); sc.collection.objects.link(cam); sc.camera = cam
cam.location = (0, -36, 0.0); cam.rotation_euler = (math.radians(90), 0, 0)
cam.keyframe_insert('location', frame=1); cam.location = (0, -31, 0.0); cam.keyframe_insert('location', frame=F_END)
logo_q = Euler((math.radians(90), 0, 0)).to_quaternion()         # local +Z (apex) -> world -Y (toward camera); local +Y (top vertex) -> world +Z
pivot.rotation_mode = 'QUATERNION'
tumble = [(1, Euler((0.9, 0.4, 0.2))), (40, Euler((1.9, 1.3, 1.2))), (80, Euler((3.0, 2.5, 2.6))), (118, Euler((4.3, 3.1, 4.0)))]
for f, e in tumble:
    pivot.rotation_quaternion = e.to_quaternion(); pivot.keyframe_insert('rotation_quaternion', frame=f)
for f in (150, 196):
    pivot.rotation_quaternion = logo_q; pivot.keyframe_insert('rotation_quaternion', frame=f)
pivot.location = (0, 0, 0.75); pivot.keyframe_insert('location', frame=1)
# lens shift, not a move: the mark stays on the optical axis, so it stays a perfect top-down logo while the frame makes room for the title
cam_d.shift_x = 0; cam_d.keyframe_insert('shift_x', frame=150); cam_d.shift_x = -0.19; cam_d.keyframe_insert('shift_x', frame=178)

# light: a warm sun from the upper left, a cool fill
sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 6.5; sun.color = (1.0, 0.86, 0.72)
so = bpy.data.objects.new('sun', sun); sc.collection.objects.link(so); so.rotation_euler = (math.radians(70), math.radians(-62), math.radians(-20))
fill = bpy.data.lights.new('fill', 'SUN'); fill.energy = 0.35; fill.color = (0.5, 0.65, 1.0)
fo = bpy.data.objects.new('fill', fill); sc.collection.objects.link(fo); fo.rotation_euler = (math.radians(-60), math.radians(40), 0)

# fade from black and back: exposure
sc.view_settings.exposure = -9; sc.view_settings.keyframe_insert('exposure', frame=1)
sc.view_settings.exposure = 0; sc.view_settings.keyframe_insert('exposure', frame=22)
sc.view_settings.keyframe_insert('exposure', frame=F_END - 14)
sc.view_settings.exposure = -9; sc.view_settings.keyframe_insert('exposure', frame=F_END)
for fc in (pivot.animation_data.action.fcurves if hasattr(pivot.animation_data.action, 'fcurves') else []):
    for kp in fc.keyframe_points: kp.interpolation = 'BEZIER'
bpy.ops.render.render(animation=True)
