"""Construct an oatmeal ceramic cup in a new Blender scene via Blender MCP.

Metres, Z up, base at zero. No existing scenes or objects are changed.
Photographs guide the design; generated textures contain no photo pixels.
"""
from pathlib import Path
import math
import json
import bpy
import bmesh
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

OUT = Path(__file__).resolve().parent
PROJECT = OUT.parent.parent
BLEND = OUT / 'cup-reference.blend'
GLB = PROJECT / 'public/models/cup-reference.glb'
if BLEND.exists() or GLB.exists():
    raise RuntimeError('Cup output already exists; choose a new output/version before rebuilding.')
for folder in ('textures', 'previews'):
    (OUT / folder).mkdir(exist_ok=True)

scene = bpy.data.scenes.new('OjaTea | Oatmeal cup study')
bpy.context.window.scene = scene
scene.unit_settings.system = 'METRIC'
model = bpy.data.collections.new('CUP | Export asset')
studio = bpy.data.collections.new('CUP STUDIO | Preview only')
scene.collection.children.link(model)
scene.collection.children.link(studio)

def empty(name, location=(0,0,0), parent=None):
    ob = bpy.data.objects.new(name, None)
    model.objects.link(ob)
    ob.location = location
    ob.parent = parent
    ob.empty_display_size = .005
    return ob

root = empty('cup_root')
root['description'] = 'Rounded oatmeal glazed ceramic cup; 60 mm tall, approximately 180 ml brim capacity'
root['units'] = 'metres; Blender Z up, GLB Y up; base at zero'
root['integration_status'] = 'Standalone study; requires app calibration'

def srgb_to_linear(c):
    c = np.asarray(c)
    return np.where(c <= .04045, c / 12.92, ((c + .055)/1.055)**2.4)

def image(name, rgb, noncolor=False):
    h,w,_ = rgb.shape
    im = bpy.data.images.new(name, width=w, height=h, alpha=False)
    im.colorspace_settings.name = 'Non-Color' if noncolor else 'sRGB'
    rgba = np.ones((h,w,4),dtype=np.float32)
    # Image buffers store the encoded values; shader colour-space conversion is
    # performed by the image node. Normal maps use linear data values.
    rgba[:,:,:3] = rgb
    im.pixels.foreach_set(rgba.ravel())
    im.filepath_raw = str(OUT / 'textures' / (name + '.png'))
    im.file_format = 'PNG'
    im.save()
    im.pack()
    return im

def material(name, colour, roughness):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    rgba = (*srgb_to_linear(colour),1)
    mat.diffuse_color = rgba
    bs = mat.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value = rgba
    bs.inputs['Roughness'].default_value = roughness
    return mat

# The rectangular image matches the circumference/height aspect ratio, keeping
# the mineral flecks close to circular on the broad wall rather than stretched.
w,h = 2048,512
y,x = np.mgrid[0:h,0:w] / np.array([h-1,w])[:,None,None]
rng = np.random.default_rng(5212)
grain = rng.random((h,w))
random_flecks = rng.random((h,w))
cloud = .5 + .18*np.sin(2*math.pi*(3*x+y)) + .10*np.sin(2*math.pi*(9*x-2*y))
rgb = np.zeros((h,w,3))
rgb[:] = (.90,.875,.79)
rgb += (cloud-.5)[:,:,None] * np.array([.065,.062,.045])
rgb += (grain-.5)[:,:,None] * .022
specks = random_flecks > .996
rgb[specks] = np.array([.40,.29,.16]) + grain[specks,None]*.12
fine = (random_flecks > .985) & ~specks
rgb[fine] -= np.array([.13,.12,.095])
# Thin iron-brown lip with an irregular, freckled transition into the glaze.
rim_start = .973 + .003*np.sin(2*math.pi*x*17) + .005*(grain-.5)
rim = np.clip((y-rim_start)/.023,0,1)
rim_colour = np.stack((.39+.07*grain,.26+.055*grain,.13+.035*grain),axis=2)
rgb = rgb*(1-rim[:,:,None]) + rim_colour*rim[:,:,None]
fallout = (y>.935) & (random_flecks > (.998 - .14*np.clip((y-.935)/.06,0,1)))
rgb[fallout] = rgb[fallout]*.74 + rim_colour[fallout]*.26
base_image = image('cup_oatmeal_basecolor', np.clip(rgb,0,1))
micro = grain*.02 + specks*.015
dx = (np.roll(micro,-1,1)-np.roll(micro,1,1))*.45
dy = (np.roll(micro,-1,0)-np.roll(micro,1,0))*.45
normal = np.stack((-dx,-dy,np.ones_like(dx)),axis=2)
normal /= np.linalg.norm(normal,axis=2)[:,:,None]
normal_image = image('cup_oatmeal_normal',normal*.5+.5,True)
glaze = material('ceramic.cup | oatmeal glaze',(.90,.875,.79),.29)
nodes,links = glaze.node_tree.nodes,glaze.node_tree.links
bs = nodes.get('Principled BSDF')
bs.inputs['Coat Weight'].default_value = .14
bs.inputs['Coat Roughness'].default_value = .22
colour_node = nodes.new('ShaderNodeTexImage'); colour_node.image=base_image; colour_node.location=(-500,160)
links.new(colour_node.outputs['Color'],bs.inputs['Base Color'])
normal_node = nodes.new('ShaderNodeTexImage'); normal_node.image=normal_image; normal_node.location=(-500,-150)
nm = nodes.new('ShaderNodeNormalMap'); nm.location=(-200,-100); nm.inputs['Strength'].default_value=.32
links.new(normal_node.outputs['Color'],nm.inputs['Color']); links.new(nm.outputs['Normal'],bs.inputs['Normal'])
footmat = material('ceramic.cup | exposed clay foot',(.36,.255,.17),.86)

# Inner profile is sized to the requested approximate brim volume; the final
# smoothed geometry is measured independently by ray-sampling the inner wall.
inner = [(0,.0055),(.014,.0055),(.024,.007),(.030,.012),(.0345,.020),
    (.037,.030),(.0375,.039),(.0365,.048),(.035,.056),(.035,.0597)]
profile_volume = sum(math.pi*(b[1]-a[1])*(a[0]**2+a[0]*b[0]+b[0]**2)/3
    for a,b in zip(inner,inner[1:]))
radial_scale = math.sqrt(.000180/profile_volume)
outer = [(0,.0022),(.014,.0022),(.020,.0022),(.021,0),(.023,0),(.0245,.0012),
    (.026,.0023),(.030,.005),(.034,.010),(.038,.017),(.0408,.025),
    (.0418,.033),(.0415,.040),(.040,.048),(.0385,.054),(.0372,.058),
    (.0369,.0594),(.0365,.060),(.036,.060)]
profile = [(r*radial_scale,z) for r,z in outer + list(reversed(inner))]
segments=128
verts,rings,faces=[],[],[]
for r,z in profile:
    if r==0:
        rings.append([len(verts)]); verts.append((0,0,z))
    else:
        ring=[]
        for j in range(segments):
            a=2*math.pi*j/segments
            handmade=1+.0008*math.sin(3*a+z*10)+.0005*math.sin(7*a-z*17)
            ring.append(len(verts)); verts.append((r*handmade*math.cos(a),r*handmade*math.sin(a),z))
        rings.append(ring)
for lo,hi in zip(rings[:-1],rings[1:]):
    for j in range(segments):
        k=(j+1)%segments
        if len(lo)==1: faces.append((lo[0],hi[k],hi[j]))
        elif len(hi)==1: faces.append((lo[j],lo[k],hi[0]))
        else: faces.append((lo[j],lo[k],hi[k],hi[j]))
mesh=bpy.data.meshes.new('cup_body_mesh'); mesh.from_pydata(verts,[],faces); mesh.update(); mesh.validate()
cup=bpy.data.objects.new('cup_body',mesh); model.objects.link(cup); cup.parent=root
bm=bmesh.new(); bm.from_mesh(mesh); bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces)); bm.to_mesh(mesh); bm.free()
mesh.materials.append(glaze); mesh.materials.append(footmat)
uv=mesh.uv_layers.new(name='SurfaceUV')
for poly in mesh.polygons:
    poly.use_smooth=True
    centre=poly.center
    if centre.z < .0016 or (centre.z<.0026 and math.hypot(centre.x,centre.y)<.021*radial_scale): poly.material_index=1
    values=[]
    for li in poly.loop_indices:
        co=mesh.vertices[mesh.loops[li].vertex_index].co
        values.append((li,(math.atan2(co.y,co.x)/(2*math.pi))%1,co.z/.060))
    seam=max(v[1] for v in values)-min(v[1] for v in values)>.5
    for li,u,v in values: uv.data[li].uv=(u+1 if seam and u<.5 else u,v)
modifier=cup.modifiers.new('Soft ceramic profile','SUBSURF'); modifier.levels=1; modifier.render_levels=1
# Subdivision gently lifts the raw foot. Rebase the evaluated contact point to
# zero so the semantic base anchor really rests on the table.
bpy.context.view_layer.update()
ev=cup.evaluated_get(bpy.context.evaluated_depsgraph_get()); evaluated_mesh=ev.to_mesh()
base_offset=min(v.co.z for v in evaluated_mesh.vertices); ev.to_mesh_clear()
for vertex in mesh.vertices: vertex.co.z-=base_offset
mesh.update()

anchors={
    'cup_anchor_base':(0,0,0),'cup_anchor_opening':(0,0,.0598),
    'cup_anchor_liquid_surface':(0,0,.052),'cup_anchor_sip_edge':(.035*radial_scale,0,.0597),
    'cup_anchor_grip':(0,0,.030),
}
for name,loc in anchors.items(): empty(name,loc,root)
for name in anchors:
    if name!='cup_anchor_base': model.objects[name].location.z-=base_offset
anchors={name:tuple(model.objects[name].location) for name in anchors}
model.objects['cup_anchor_opening']['radius_m']=.035*radial_scale
model.objects['cup_anchor_liquid_surface']['suggested_radius_m']=.0357*radial_scale

# Shared neutral studio setup; the material controls warmth rather than a strong
# coloured light, so the oatmeal cup remains distinct from the dark clay pot.
def aim(ob,target): ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()
def camera_for(sc,col,name,loc,target,scale):
    data=bpy.data.cameras.new(name); data.type='ORTHO'; data.ortho_scale=scale
    ob=bpy.data.objects.new(name,data); col.objects.link(ob); ob.location=loc; aim(ob,target); sc.camera=ob
    return ob
def studio_for(sc,col,prefix):
    groundmesh=bpy.data.meshes.new(prefix+'_floor_mesh')
    groundmesh.from_pydata([(-20,-20,-.0002),(20,-20,-.0002),(20,20,-.0002),(-20,20,-.0002)],[],[(0,1,2,3)])
    ground=bpy.data.objects.new(prefix+'_floor',groundmesh); col.objects.link(ground)
    ground.data.materials.append(material(prefix+' | backdrop',(.27,.285,.29),.93))
    for suffix,loc,power,size,colour in [
        ('key',(.04,-.24,.35),9,.23,(1,.965,.91)),
        ('fill',(-.22,-.02,.20),4,.20,(.88,.93,1)),
        ('rim',(.20,.16,.28),7,.17,(1,.98,.94))]:
        data=bpy.data.lights.new(prefix+'_'+suffix,'AREA'); data.energy=power; data.shape='DISK'; data.size=size; data.color=colour
        ob=bpy.data.objects.new(prefix+'_'+suffix,data); col.objects.link(ob); ob.location=loc; aim(ob,(0,0,.035))
    world=bpy.data.worlds.new(prefix+'_world'); world.use_nodes=True
    world.node_tree.nodes['Background'].inputs['Color'].default_value=(.5,.5,.5,1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value=.25; sc.world=world
    sc.render.engine='BLENDER_EEVEE'; sc.render.resolution_x=1440; sc.render.resolution_y=1200; sc.render.resolution_percentage=100
    sc.render.image_settings.file_format='PNG'; sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - Medium High Contrast'

studio_for(scene,studio,'CUP_STUDIO')
camera=camera_for(scene,studio,'CUP_STUDIO_camera',(.13,-.18,.145),(0,0,.028),.128)
scene.render.filepath=str(OUT/'previews/cup-hero.png')

# Compare against the SAVED kyusu asset, preserving any unsaved work in its live scene.
comparison=bpy.data.scenes.new('OjaTea | Cup and kyusu proportions')
comparison.unit_settings.system='METRIC'
comparison_studio=bpy.data.collections.new('CUP COMPARISON | Preview only'); comparison.collection.children.link(comparison_studio)
studio_for(comparison,comparison_studio,'CUP_COMPARISON')
# Blender cannot link from its current file. Save this new study first when the
# connected session is still editing the kyusu file; its original stays intact.
if Path(bpy.data.filepath).resolve() == (PROJECT/'assets/kyusu/kyusu-reference.blend').resolve():
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
with bpy.data.libraries.load(str(PROJECT/'assets/kyusu/kyusu-reference.blend'),link=True) as (src,dst):
    matches=[n for n in src.collections if n=='KYUSU | Export asset']
    if not matches: raise RuntimeError('Saved kyusu export collection not found.')
    dst.collections=matches
pot_collection=dst.collections[0]
pot_collection.library.filepath='//../kyusu/kyusu-reference.blend'
for name,col,loc in [('REFERENCE_kyusu',pot_collection,(-.065,.025,0)),('REFERENCE_cup',model,(.115,-.022,0))]:
    ob=bpy.data.objects.new(name,None); ob.instance_type='COLLECTION'; ob.instance_collection=col; ob.location=loc
    comparison.collection.objects.link(ob)
camera_for(comparison,comparison_studio,'CUP_COMPARISON_camera',(.20,-.43,.29),(.017,-.006,.038),.37)
comparison.render.filepath=str(OUT/'previews/cup-with-kyusu.png')

bpy.context.window.scene=scene
bpy.ops.object.select_all(action='DESELECT')
for ob in model.objects: ob.select_set(True)
bpy.context.view_layer.objects.active=cup
bpy.ops.export_scene.gltf(filepath=str(GLB),export_format='GLB',use_selection=True,use_active_scene=True,
    export_yup=True,export_apply=True,export_extras=True,export_animations=False,export_lights=False,export_cameras=False)

# Independent measurements of the evaluated mesh, including its real cavity.
bpy.context.view_layer.update(); deps=bpy.context.evaluated_depsgraph_get(); evaluated=cup.evaluated_get(deps); me=evaluated.to_mesh()
me.calc_loop_triangles(); bm=bmesh.new(); bm.from_mesh(me)
checks={'triangles':len(me.loop_triangles),'boundary_edges':sum(e.is_boundary for e in bm.edges),
    'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges)}
bvh=BVHTree.FromBMesh(bm)
def capacity_at(fill_z):
    zs=np.linspace(.00551-base_offset,fill_z,600); rs=[]
    for z in zs:
        hit=bvh.ray_cast(Vector((0,0,float(z))),Vector((1,0,0)),.08)
        rs.append(hit[0].x if hit[0] else 0)
    return float(np.trapezoid(math.pi*np.asarray(rs)**2,zs)*1e6)
capacity=capacity_at(.0597-base_offset); serving=capacity_at(.052-base_offset)
dimensions=[max(v.co[i] for v in me.vertices)-min(v.co[i] for v in me.vertices) for i in range(3)]
bm.free(); evaluated.to_mesh_clear()
metadata={'units':'metres','height_m':dimensions[2],'max_diameter_m':max(dimensions[:2]),
    'requested_capacity_ml':180,'estimated_brim_capacity_ml':capacity,'estimated_capacity_at_liquid_anchor_ml':serving,
    'capacity_method':'600 horizontal ray samples of evaluated inner wall, integrated as circular cross sections; approximate',
    'material':'oatmeal glazed ceramic with iron-brown rim and exposed clay foot','geometry_checks':checks,
    'opening_radius_m':.035*radial_scale,'glb_bytes':GLB.stat().st_size,
    'anchors_blender_z_up':{k:list(v) for k,v in anchors.items()},
    'anchors_gltf_y_up':{k:[v[0],v[2],-v[1]] for k,v in anchors.items()},
    'status':'Standalone visual study. In-app calibration and integration pending.'}
(OUT/'asset-metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
bpy.ops.object.select_all(action='DESELECT'); cup.select_set(True); bpy.context.view_layer.objects.active=cup
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        area.spaces.active.region_3d.view_location=(0,0,.03)
        area.spaces.active.region_3d.view_distance=.16
        area.spaces.active.region_3d.view_rotation=camera.rotation_euler.to_quaternion()
        area.spaces.active.clip_start=.0005
        area.spaces.active.overlay.show_extras=False
        area.spaces.active.shading.color_type='MATERIAL'

# Save to a new file; the existing kyusu file and all live scenes are preserved.
backup_setting=bpy.context.preferences.filepaths.save_version
bpy.context.preferences.filepaths.save_version=0
try:
    for im in (base_image,normal_image): im.filepath='//textures/'+Path(im.filepath).name
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
finally:
    bpy.context.preferences.filepaths.save_version=backup_setting
result={'blend':str(BLEND),'glb':str(GLB),'scene':scene.name,'comparison_scene':comparison.name,'metadata':metadata}
