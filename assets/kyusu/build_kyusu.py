"""Build the reference-inspired kyusu in a NEW Blender scene. Run through Blender MCP.

Source photographs are visual references only; no photograph is used as a texture.
All dimensions are inferred, in metres. Existing scenes/objects are preserved.
"""
from pathlib import Path
import math
import json
import bpy
import bmesh
import numpy as np
from mathutils import Vector

OUT = Path(__file__).resolve().parent
PROJECT = OUT.parent.parent
if (OUT / 'kyusu-reference.blend').exists():
    raise RuntimeError('Output already exists; choose a new output name before rebuilding.')

scene = bpy.data.scenes.new('OjaTea | Kyusu reference study')
bpy.context.window.scene = scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1
model = bpy.data.collections.new('KYUSU | Export asset')
studio = bpy.data.collections.new('STUDIO | Preview only')
scene.collection.children.link(model)
scene.collection.children.link(studio)

def empty(name, loc=(0, 0, 0), parent=None):
    ob = bpy.data.objects.new(name, None)
    model.objects.link(ob)
    ob.location = loc
    ob.parent = parent
    ob.empty_display_size = .008
    ob.empty_display_type = 'PLAIN_AXES'
    return ob

root = empty('kyusu_root')
root['description'] = 'Reference-inspired rustic clay kyusu; inferred scale, not a scan'
root['blender_axes'] = 'Z up; spout +X; handle -Y; base Z=0'
root['gltf_axes'] = 'Y up; spout +X; handle +Z; base Y=0'
root['integration_status'] = 'Standalone asset; application calibration still required'

def mesh_object(name, verts, faces, collection=model, parent=root):
    data = bpy.data.meshes.new(name + '_mesh')
    data.from_pydata(verts, [], faces)
    data.update()
    data.validate()
    ob = bpy.data.objects.new(name, data)
    collection.objects.link(ob)
    ob.parent = parent
    for p in data.polygons:
        p.use_smooth = True
    bm = bmesh.new()
    bm.from_mesh(data)
    bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-8)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bm.to_mesh(data)
    bm.free()
    return ob

def lathe(name, profile, segments=96, parent=root, origin=(0, 0, 0), axis=(0, 0, 1), handmade=0):
    verts, rings, faces = [], [], []
    for r, z in profile:
        if r == 0:
            rings.append([len(verts)])
            verts.append((0, 0, z))
        else:
            ring = []
            for j in range(segments):
                a = 2 * math.pi * j / segments
                rr = r * (1 + handmade * (.6 * math.sin(3*a + z*20) + .4 * math.sin(7*a - z*30)))
                ring.append(len(verts))
                verts.append((rr * math.cos(a), rr * math.sin(a), z))
            rings.append(ring)
    for lo, hi in zip(rings[:-1], rings[1:]):
        for j in range(segments):
            k = (j + 1) % segments
            if len(lo) == 1:
                faces.append((lo[0], hi[k], hi[j]))
            elif len(hi) == 1:
                faces.append((lo[j], lo[k], hi[0]))
            else:
                faces.append((lo[j], lo[k], hi[k], hi[j]))
    ob = mesh_object(name, verts, faces, parent=parent)
    ob.location = origin
    ob.rotation_mode = 'QUATERNION'
    ob.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(Vector(axis).normalized())
    uv = ob.data.uv_layers.new(name='SurfaceUV')
    for poly in ob.data.polygons:
        values = []
        for li in poly.loop_indices:
            co = ob.data.vertices[ob.data.loops[li].vertex_index].co
            u = (math.atan2(co.y, co.x) / (2*math.pi)) % 1
            values.append((li, u, co.z))
        seam = max(v[1] for v in values) - min(v[1] for v in values) > .5
        zmin, zmax = min(p[1] for p in profile), max(p[1] for p in profile)
        for li, u, z in values:
            if seam and u < .5:
                u += 1
            uv.data[li].uv = (u, (z-zmin) / max(.001, zmax-zmin))
    return ob

def active(ob):
    bpy.ops.object.select_all(action='DESELECT')
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob

def subdivide(ob, levels=1):
    active(ob)
    m = ob.modifiers.new('Soft wheel-thrown profile', 'SUBSURF')
    m.levels = levels
    bpy.ops.object.modifier_apply(modifier=m.name)

def cylinder(name, radius, depth, centre, direction=(0, 0, 1)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=radius, depth=depth, location=centre)
    ob = bpy.context.object
    ob.name = name
    for c in list(ob.users_collection):
        c.objects.unlink(ob)
    model.objects.link(ob)
    ob.rotation_mode = 'QUATERNION'
    ob.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(Vector(direction).normalized())
    return ob

def cut(ob, cutter, name):
    active(ob)
    m = ob.modifiers.new(name, 'BOOLEAN')
    m.operation = 'DIFFERENCE'
    m.solver = 'EXACT'
    m.object = cutter
    bpy.ops.object.modifier_apply(modifier=m.name)
    # Only remove this temporary object created by this build.
    bpy.data.objects.remove(cutter, do_unlink=True)

def make_image(name, pixels, noncolor=False):
    n = pixels.shape[0]
    im = bpy.data.images.new(name, width=n, height=n, alpha=False)
    im.colorspace_settings.name = 'Non-Color' if noncolor else 'sRGB'
    rgba = np.ones((n, n, 4), dtype=np.float32)
    rgba[:, :, :3] = pixels
    im.pixels.foreach_set(rgba.ravel())
    im.filepath_raw = str(OUT / 'textures' / (name + '.png'))
    im.file_format = 'PNG'
    im.save()
    im.pack()
    return im

def linear(rgb):
    a = np.asarray(rgb)
    return np.where(a <= .04045, a/12.92, ((a+.055)/1.055)**2.4)

(OUT / 'textures').mkdir(exist_ok=True)
(OUT / 'previews').mkdir(exist_ok=True)
rng = np.random.default_rng(319)
n = 1024
y, x = np.mgrid[0:n, 0:n] / n
grain = rng.random((n,n))
flecks = rng.random((n,n))
cloud = .5 + .19*np.sin(2*math.pi*(2*x+y)) + .12*np.sin(2*math.pi*(5*x-3*y)) + .09*np.sin(2*math.pi*(11*x+7*y))
wheel = np.sin(2*math.pi*(y*67 + .12*np.sin(2*math.pi*x)))
rgb = np.zeros((n,n,3))
rgb[:] = (.36, .235, .18)
rgb += (cloud-.5)[:,:,None] * np.array([.09,.07,.05])
rgb += (grain-.5)[:,:,None] * np.array([.16,.12,.09])
rgb += (flecks>.985)[:,:,None] * np.array([.13,.105,.065])
rgb -= (flecks<.025)[:,:,None] * .065
rgb += wheel[:,:,None] * .003
base = make_image('clay_basecolor', linear(np.clip(rgb,0,1)))
height = grain*.5 + wheel*.06
dx = (np.roll(height,-1,1)-np.roll(height,1,1))*.23
dy = (np.roll(height,-1,0)-np.roll(height,1,0))*.23
norm = np.stack((-dx,-dy,np.ones_like(dx)),axis=2)
norm /= np.linalg.norm(norm,axis=2)[:,:,None]
normal = make_image('clay_normal', norm*.5+.5, True)

def material(name, colour, roughness):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.diffuse_color = (*linear(colour), 1)
    bs = mat.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value = (*linear(colour), 1)
    bs.inputs['Roughness'].default_value = roughness
    return mat

clay = material('ceramic.body | iron-rich matte clay', (.43,.285,.22), .88)
nodes, links = clay.node_tree.nodes, clay.node_tree.links
bs = nodes.get('Principled BSDF')
tex = nodes.new('ShaderNodeTexImage'); tex.image=base; tex.location=(-500,150)
links.new(tex.outputs['Color'],bs.inputs['Base Color'])
texn = nodes.new('ShaderNodeTexImage'); texn.image=normal; texn.location=(-500,-140)
nm = nodes.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value=.65; nm.location=(-220,-100)
links.new(texn.outputs['Color'],nm.inputs['Color']); links.new(nm.outputs['Normal'],bs.inputs['Normal'])
cordmat = material('fibre.handle | natural straw cord', (.70,.61,.43), .94)
darkclay = material('ceramic.handle | burnished end', (.31,.20,.16), .72)

# Closed cross section: underside -> foot -> exterior -> rim -> inner wall -> floor.
body_profile = [(0,.003),(.022,.003),(.029,.002),(.032,0),(.035,0),(.038,.002),
    (.045,.006),(.053,.012),(.061,.023),(.066,.034),(.068,.045),(.067,.053),
    (.063,.063),(.055,.071),(.046,.077),(.040,.080),(.0375,.0805),
    (.0365,.0795),(.0365,.077),(.038,.075),(.042,.074),(.050,.069),
    (.058,.061),(.062,.051),(.063,.041),(.060,.029),(.053,.019),
    (.043,.012),(.029,.008),(.012,.007),(0,.007)]
body = lathe('kyusu_body', body_profile, handmade=.002)
body.data.materials.append(clay)
subdivide(body)

# Spout: a continuous hollow tapered tube; bore also cuts the body's wall.
start=Vector((.050,0,.043)); end=Vector((.105,0,.075))
axis=(end-start).normalized()
length=(end-start).length
spout_profile=[(.017,0),(.017,.004),(.014,.017),(.010,.033),(.0078,length-.003),
    (.0079,length),(.0073,length+.0008),(.0058,length+.0006),(.0054,length-.001),
    (.0056,length-.005),(.0075,.033),(.011,.017),(.0138,.004),(.0138,0),(.017,0)]
spout = lathe('kyusu_spout',spout_profile,64,origin=start,axis=axis)
spout.data.materials.append(clay)
subdivide(spout)
cutter=cylinder('_temporary_spout_bore',.0105,.052,start+axis*.006,axis)
cut(body,cutter,'Open passage into spout')
active(body)
union = body.modifiers.new('Blend spout into body', 'BOOLEAN')
union.operation = 'UNION'; union.solver = 'EXACT'; union.object = spout
bpy.ops.object.modifier_apply(modifier=union.name)
bpy.data.objects.remove(spout, do_unlink=True)
join_bevel = body.modifiers.new('Soft ceramic joins', 'BEVEL')
join_bevel.width = .0008; join_bevel.segments = 3; join_bevel.limit_method = 'ANGLE'

# Side handle, perpendicular to spout; terminal flare matches reference silhouette.
hstart=Vector((0,-.058,.047))
haxis=Vector((0,-1,.12)).normalized()
handle_profile=[(0,0),(.014,0),(.014,.003),(.012,.010),(.010,.016),(.009,.025),
    (.0095,.037),(.011,.048),(.014,.055),(.019,.060),(.021,.063),
    (.021,.065),(.019,.067),(.015,.0675),(.006,.0675),(0,.0675)]
handle=lathe('kyusu_side_handle',handle_profile,64,origin=hstart,axis=haxis)
handle.data.materials.append(darkclay)
subdivide(handle)

# Continuous twisted cord: three fine strands winding around a common helix.
q=Vector((0,0,1)).rotation_difference(haxis)
def cord_radius(t):
    return .0097 + .0018*(abs((t-.030)/.018)**1.5)
verts, faces=[],[]
steps=1100
turns=14
for strand in range(3):
    offset=len(verts)
    for i in range(steps+1):
        f=i/steps; t=.012+f*.038; a=f*turns*2*math.pi
        rr=cord_radius(t)
        theta=a+math.pi/2
        twist=a*5+strand*2*math.pi/3
        centre=Vector((rr*math.cos(a),rr*math.sin(a),t))
        radial=Vector((math.cos(a),math.sin(a),0))
        tangent=Vector((-math.sin(a),math.cos(a),.038/(turns*2*math.pi*rr))).normalized()
        across=tangent.cross(radial).normalized()
        centre += .00053*(math.cos(twist)*radial+math.sin(twist)*across)
        for j in range(5):
            b=j*2*math.pi/5
            p=centre+.00048*(math.cos(b)*radial+math.sin(b)*across)
            verts.append(tuple(hstart+q@p))
    for i in range(steps):
        for j in range(5):
            k=(j+1)%5
            faces.append((offset+i*5+j,offset+i*5+k,offset+(i+1)*5+k,offset+(i+1)*5+j))
    faces.append(tuple(offset+j for j in reversed(range(5))))
    faces.append(tuple(offset+steps*5+j for j in range(5)))
wrap=mesh_object('kyusu_handle_cord',verts,faces)
wrap.data.materials.append(cordmat)
cord_lod = wrap.modifiers.new('Export cord simplification', 'DECIMATE')
cord_lod.ratio = .28

# Separate lid hierarchy; origin is its seated pivot, not the bottom of the pot.
lidroot=empty('kyusu_lid',(0,0,.0785),root)
lidprofile=[(0,-.0025),(.020,-.0025),(.031,-.003),(.034,-.004),(.035,-.003),
    (.0355,-.001),(.0355,.001),(.0345,.0025),(.032,.003),
    (.028,.0012),(.022,-.0002),(.017,-.0005),(.013,0),(.009,.0007),(0,.001)]
lid=lathe('kyusu_lid_disc',lidprofile,96,parent=lidroot,handmade=.001)
lid.data.materials.append(clay)
subdivide(lid)
# Small pressure vent through the lid.
vent=cylinder('_temporary_lid_vent',.00095,.014,(.017,-.010,.0785))
cut(lid,vent,'Lid steam vent')
knob=lathe('kyusu_lid_knob',[(0,0),(.0048,0),(.005,.001),(.004,.003),
    (.0035,.010),(.0034,.013),(.0025,.014),(0,.014)],48,parent=lidroot,origin=(0,0,.001))
knob.data.materials.append(clay)
subdivide(knob)
# Concentric throwing marks near knob, subtle geometry that survives export.
for i,r in enumerate([.007,.009,.011,.013,.015]):
    ridge=lathe('kyusu_lid_throwing_ring_%02d'%i,[(r-.0003,.0005),(r-.0003,.0007),(r,.0010),(r+.0003,.0007),(r+.0003,.0005),(r-.0003,.0005)],64,parent=lidroot)
    ridge.data.materials.append(clay)

anchors={
    'anchor_base':(0,0,0), 'anchor_opening':(0,0,.079),
    'anchor_spout_tip':tuple(start+axis*(length-.0003)),
    'anchor_grip':tuple(hstart+haxis*.032),
    'anchor_lid_seat':(0,0,.0785), 'anchor_liquid_surface':(0,0,.050),
    'anchor_pour_pivot':(0,0,.040),
}
for name,loc in anchors.items():
    ob=empty(name,loc,root)
    if name=='anchor_opening': ob['radius_m']=.036
    if name=='anchor_liquid_surface': ob['suggested_radius_m']=.060

# Preview studio is not included in the GLB.
groundmat=material('STUDIO | charcoal taupe',(.19,.185,.17),.96)
ground=mesh_object('STUDIO_ground',[(-200,-200,-.0008),(200,-200,-.0008),(200,200,-.0008),(-200,200,-.0008)],[(0,1,2,3)],studio,None)
ground.data.materials.append(groundmat)
world=bpy.data.worlds.new('STUDIO | soft neutral world'); world.use_nodes=True
world.node_tree.nodes['Background'].inputs['Color'].default_value=(.40,.42,.46,1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=.32
scene.world=world

def aim(ob,target):
    ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()

def light(name,loc,power,size,colour):
    data=bpy.data.lights.new(name,'AREA'); data.energy=power; data.shape='DISK'; data.size=size; data.color=colour
    ob=bpy.data.objects.new(name,data); studio.objects.link(ob); ob.location=loc; aim(ob,(0,0,.04))

light('STUDIO_key',(.02,-.22,.36),7,.23,(1,.86,.74))
light('STUDIO_fill',(-.22,-.01,.17),3,.20,(.77,.85,1))
light('STUDIO_rim',(.16,.20,.27),6,.18,(1,.94,.82))
camera_data=bpy.data.cameras.new('STUDIO_camera'); camera=bpy.data.objects.new('STUDIO_camera',camera_data)
studio.objects.link(camera); camera.location=(.235,-.31,.235); camera_data.type='ORTHO'; camera_data.ortho_scale=.275
aim(camera,(.011,-.013,.042)); scene.camera=camera
scene.render.engine='BLENDER_EEVEE'
scene.render.resolution_x=1500; scene.render.resolution_y=1200; scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.view_settings.view_transform='AgX'
scene.view_settings.look='AgX - Medium High Contrast'
scene.view_settings.exposure=0
scene.render.film_transparent=False

# Frame the new scene in the existing Layout viewport without modifying old objects.
bpy.context.view_layer.update()
active(body)
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            area.spaces.active.region_3d.view_distance=.34
            area.spaces.active.region_3d.view_location=(0,-.01,.04)
            area.spaces.active.region_3d.view_rotation=camera.rotation_euler.to_quaternion()
            area.spaces.active.clip_start=.001
            area.spaces.active.clip_end=100
            area.spaces.active.shading.color_type='MATERIAL'
            area.spaces.active.overlay.show_extras=False

# Export only the asset hierarchy, including semantic anchors, with PBR textures.
bpy.ops.object.select_all(action='DESELECT')
for ob in model.objects: ob.select_set(True)
bpy.context.view_layer.objects.active=body
glb=PROJECT/'public/models/kyusu-reference.glb'
bpy.ops.export_scene.gltf(filepath=str(glb),export_format='GLB',use_selection=True,use_active_scene=True,
    export_yup=True,export_apply=True,export_extras=True,export_animations=False,
    export_cameras=False,export_lights=False)

deps=bpy.context.evaluated_depsgraph_get()
triangles=0
for ob in model.objects:
    if ob.type=='MESH':
        me=ob.evaluated_get(deps).to_mesh(); me.calc_loop_triangles(); triangles+=len(me.loop_triangles)
        ob.evaluated_get(deps).to_mesh_clear()
metadata={'units':'metres','body_diameter_approx':.136,'body_rim_height':.0805,
    'lid_knob_top_approx':.0945,'triangles':triangles,
    'anchors_blender_z_up':{k:list(v) for k,v in anchors.items()},
    'anchors_gltf_y_up':{k:[v[0],v[2],-v[1]] for k,v in anchors.items()},
    'opening_radius':.036,'glb_bytes':glb.stat().st_size,
    'status':'Visual study. Needs in-app scale/pose/clearance calibration.'}
(OUT/'asset-metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
scene.render.filepath=str(OUT/'previews/kyusu-closed.png')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'kyusu-reference.blend'))
result={'scene':scene.name,'blend':bpy.data.filepath,'glb':str(glb),'metadata':metadata}
