"""Create the third OjaTea asset study in a new Blender scene via MCP.

Reference dimensions: about 220 mm overall width, 160 mm body diameter,
177 mm height including an upright handle. Existing work is preserved.
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
BLEND = OUT/'kettle-reference.blend'
GLB = PROJECT/'public/models/kettle-reference.glb'
if BLEND.exists() or GLB.exists():
    raise RuntimeError('Kettle output exists. Choose a new version before rebuilding.')
for folder in ('textures','previews'): (OUT/folder).mkdir(exist_ok=True)
scene = bpy.data.scenes.new('OjaTea | Steel kettle study')
bpy.context.window.scene = scene
scene.unit_settings.system = 'METRIC'
model = bpy.data.collections.new('KETTLE | Export asset')
studio = bpy.data.collections.new('KETTLE STUDIO | Preview only')
scene.collection.children.link(model); scene.collection.children.link(studio)

def empty(name,loc=(0,0,0),parent=None):
    ob=bpy.data.objects.new(name,None); model.objects.link(ob)
    ob.location=loc; ob.parent=parent; ob.empty_display_size=.006
    return ob
root=empty('kettle_root')
root['description']='Reference-inspired Japanese kettle; charcoal finish over stainless steel, wood grip/knob'
root['units']='metres; Blender Z up, GLB Y up; spout +X; base zero'
root['integration_status']='Standalone study; application calibration pending'

def linear(c):
    a=np.asarray(c); return np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4)

def material(name,colour,roughness,metallic=0):
    mat=bpy.data.materials.new(name); mat.use_nodes=True
    rgba=(*linear(colour),1); mat.diffuse_color=rgba
    bs=mat.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value=rgba; bs.inputs['Roughness'].default_value=roughness
    bs.inputs['Metallic'].default_value=metallic
    return mat
coat=material('metal.kettle | charcoal exterior finish',(.085,.09,.09),.56,.04)
coat.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=.3
steel=material('metal.kettle | exposed stainless interior',(.65,.67,.69),.25,1)
hardware=material('metal.kettle | hinge hardware',(.14,.15,.16),.4,.65)
wood=material('wood.kettle | honey timber',(.53,.345,.17),.58)

def image(name,rgb,noncolor=False):
    h,w,_=rgb.shape
    im=bpy.data.images.new(name,width=w,height=h,alpha=False)
    im.colorspace_settings.name='Non-Color' if noncolor else 'sRGB'
    rgba=np.ones((h,w,4),dtype=np.float32); rgba[:,:,:3]=rgb
    im.pixels.foreach_set(rgba.ravel()); im.filepath_raw=str(OUT/'textures'/(name+'.png'))
    im.file_format='PNG'; im.save(); im.pack()
    return im

# Generated fine, directional timber grain. No reference-photo pixels are used.
w,h=1024,512
y,x=np.mgrid[0:h,0:w]/np.array([h-1,w])[:,None,None]
rng=np.random.default_rng(188)
warp=.015*np.sin(x*2*math.pi*1.5)+.005*np.sin(x*2*math.pi*6)
knots=rng.uniform(-1,1,145)
position=np.mod(y+warp,1)*144
index=np.floor(position).astype(int); blend=position-index
blend=blend*blend*(3-2*blend)
grain=knots[index]*(1-blend)+knots[index+1]*blend
fine=rng.random((h,w))-.5
for shift in (1,2,4,8,16,32): fine=(fine+np.roll(fine,shift,1)+np.roll(fine,-shift,1))/3
random=rng.random((h,w))
rgb=np.empty((h,w,3)); rgb[:]=(.53,.345,.17)
rgb+=grain[:,:,None]*np.array([.030,.026,.018])
rgb+=fine[:,:,None]*.009+(random-.5)[:,:,None]*.035
rgb+=(.5+.5*np.sin(2*math.pi*(x*2+y)))[:,:,None]*np.array([.045,.035,.02])
woodcolour=image('kettle_wood_basecolor',np.clip(rgb,0,1))
height=grain*.0015+fine*.001+(random-.5)*.002
dx=(np.roll(height,-1,1)-np.roll(height,1,1))*.4
dy=(np.roll(height,-1,0)-np.roll(height,1,0))*.4
norm=np.stack((-dx,-dy,np.ones_like(dx)),axis=2); norm/=np.linalg.norm(norm,axis=2)[:,:,None]
woodnormal=image('kettle_wood_normal',norm*.5+.5,True)
nodes,links=wood.node_tree.nodes,wood.node_tree.links; bs=nodes.get('Principled BSDF')
tex=nodes.new('ShaderNodeTexImage'); tex.image=woodcolour; tex.location=(-500,150)
links.new(tex.outputs['Color'],bs.inputs['Base Color'])
tex=nodes.new('ShaderNodeTexImage'); tex.image=woodnormal; tex.location=(-500,-150)
nm=nodes.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value=.35; nm.location=(-200,-100)
links.new(tex.outputs['Color'],nm.inputs['Color']); links.new(nm.outputs['Normal'],bs.inputs['Normal'])

def mesh_object(name,verts,faces,parent=root,collection=model):
    me=bpy.data.meshes.new(name+'_mesh'); me.from_pydata(verts,[],faces); me.update(); me.validate()
    bm=bmesh.new(); bm.from_mesh(me)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-8)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces)); bm.to_mesh(me); bm.free()
    ob=bpy.data.objects.new(name,me); collection.objects.link(ob); ob.parent=parent
    for p in me.polygons: p.use_smooth=True
    return ob

def active(ob):
    bpy.ops.object.select_all(action='DESELECT'); ob.select_set(True); bpy.context.view_layer.objects.active=ob

def lathe(name,profile,segments=96,parent=root,loc=(0,0,0),inner_start=None,mats=(coat,steel)):
    verts,rings,faces,rows=[],[],[],[]
    for r,z in profile:
        if r==0: rings.append([len(verts)]); verts.append((0,0,z))
        else:
            ring=[]
            for j in range(segments):
                a=2*math.pi*j/segments; ring.append(len(verts)); verts.append((r*math.cos(a),r*math.sin(a),z))
            rings.append(ring)
    for row,(lo,hi) in enumerate(zip(rings[:-1],rings[1:])):
        for j in range(segments):
            k=(j+1)%segments
            if len(lo)==1: f=(lo[0],hi[k],hi[j])
            elif len(hi)==1: f=(lo[j],lo[k],hi[0])
            else: f=(lo[j],lo[k],hi[k],hi[j])
            faces.append(f); rows.append(row)
    ob=mesh_object(name,verts,faces,parent); ob.location=loc
    for m in mats: ob.data.materials.append(m)
    uv=ob.data.uv_layers.new(name='SurfaceUV')
    zmin,zmax=min(z for r,z in profile),max(z for r,z in profile)
    for p,row in zip(ob.data.polygons,rows):
        if inner_start is not None and row>=inner_start: p.material_index=1
        vals=[]
        for li in p.loop_indices:
            co=ob.data.vertices[ob.data.loops[li].vertex_index].co
            vals.append((li,(math.atan2(co.y,co.x)/(2*math.pi))%1,(co.z-zmin)/max(zmax-zmin,.001)))
        seam=max(v[1] for v in vals)-min(v[1] for v in vals)>.5
        for li,u,v in vals:
            u=u+1 if seam and u<.5 else u
            uv.data[li].uv=(v,u) if mats[0]==wood else (u,v)
    return ob

def subdivide(ob):
    active(ob); m=ob.modifiers.new('Soft formed-metal profile','SUBSURF'); m.levels=1
    bpy.ops.object.modifier_apply(modifier=m.name)

def cylinder(name,radius,depth,loc,mat=None,axis=(0,0,1),parent=root):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=radius,depth=depth,location=loc)
    ob=bpy.context.object; ob.name=name
    for col in list(ob.users_collection): col.objects.unlink(ob)
    model.objects.link(ob); ob.parent=parent
    ob.rotation_mode='QUATERNION'; ob.rotation_quaternion=Vector((0,0,1)).rotation_difference(Vector(axis).normalized())
    if mat: ob.data.materials.append(mat)
    for p in ob.data.polygons: p.use_smooth=len(p.vertices)==4
    return ob

def boolean(ob,other,operation,name):
    active(ob); mod=ob.modifiers.new(name,'BOOLEAN'); mod.operation=operation; mod.solver='EXACT'; mod.object=other
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(other,do_unlink=True)

# A closed thin-walled shell with a real floor, stainless interior and rolled rim.
profile=[(0,.0015),(.052,.0015),(.068,.0015),(.073,.002),(.077,.005),
    (.079,.010),(.080,.018),(.080,.029),(.080,.080),(.0798,.090),
    (.078,.096),(.072,.100),(.061,.104),(.052,.107),(.0505,.108),
    (.0495,.108),(.0488,.1075),(.0488,.1055),(.050,.105),
    (.060,.102),(.071,.098),(.0765,.093),(.0785,.087),(.0785,.025),
    (.078,.017),(.076,.011),(.072,.007),(.065,.005),(.044,.0048),
    (.041,.0052),(.039,.0058),(.036,.0059),(.034,.0052),(.031,.0048),(0,.0048)]
body=lathe('kettle_body',profile,96,inner_start=15)
subdivide(body)
# Rebase the smoothed bottom to zero before adding the other parts.
base_offset=min(v.co.z for v in body.data.vertices)
for v in body.data.vertices: v.co.z-=base_offset
body.data.update()

# Swept, hollow spout. The final mouth is obliquely cut and has a steel lip.
path=[(.062,0,.034),(.068,0,.038),(.078,0,.047),(.090,0,.061),
    (.102,0,.078),(.114,0,.094),(.127,0,.106),(.137,0,.111)]
radii=[.019,.019,.017,.0145,.012,.0105,.0095,.0095]
verts,faces,material_ids=[],[],[]; seg=64
centres=[Vector(p) for p in path]
normals=[]
for i,p in enumerate(centres):
    tangent=(centres[min(i+1,len(centres)-1)]-centres[max(i-1,0)]).normalized()
    normals.append(tangent.cross(Vector((0,1,0))).normalized())
# Outer surface, lip, inner surface in reverse, and root closure.
rings=[]
for is_inner in (False,True):
    indices=range(len(path)) if not is_inner else reversed(range(len(path)))
    for i in indices:
        r=radii[i]-(.0011 if is_inner else 0)
        ring=[]
        for j in range(seg):
            a=2*math.pi*j/seg
            ring.append(len(verts)); verts.append(tuple(centres[i]+r*(math.cos(a)*Vector((0,1,0))+math.sin(a)*normals[i])))
        rings.append(ring)
for row in range(len(rings)):
    lo,hi=rings[row],rings[(row+1)%len(rings)]
    for j in range(seg):
        k=(j+1)%seg; faces.append((lo[j],lo[k],hi[k],hi[j]))
        material_ids.append(1 if row>=len(path)-1 else 0)
spout=mesh_object('kettle_spout',verts,faces)
spout.data.materials.append(coat); spout.data.materials.append(steel)
for p,idx in zip(spout.data.polygons,material_ids): p.material_index=idx
boolean(body,spout,'UNION','Join open spout shell')
# Open the receiving body wall where the spout crosses it.
direction=(centres[2]-centres[0]).normalized()
cutter=cylinder('_kettle_temporary_bore',.0145,.032,centres[1],axis=direction)
boolean(body,cutter,'DIFFERENCE','Continuous water passage')
# Slice the mouth on a shallow, downward-facing plane rather than leaving a
# square cut normal to the tube. Keep the lower extremity almost unchanged and
# cut the upper wall back, creating the pointed pouring lip in the annotations.
spout_cut_normal=Vector((.45,0,1)).normalized()
old_lower_lip=centres[-1]-normals[-1]*radii[-1]
spout_cut_plane=old_lower_lip-spout_cut_normal*.0002
bpy.ops.mesh.primitive_cube_add(size=.8)
cutter=bpy.context.object; cutter.name='_kettle_temporary_tip_cut'
for col in list(cutter.users_collection): col.objects.unlink(cutter)
model.objects.link(cutter)
cutter.location=spout_cut_plane+spout_cut_normal*.4
cutter.rotation_mode='QUATERNION'
cutter.rotation_quaternion=Vector((0,0,1)).rotation_difference(spout_cut_normal)
cutter.data.materials.append(coat); cutter.data.materials.append(steel)
for face in cutter.data.polygons: face.material_index=1
boolean(body,cutter,'DIFFERENCE','Angled spout mouth')
cut_vertices=[v.co.copy() for v in body.data.vertices
    if abs(spout_cut_normal.dot(v.co-spout_cut_plane))<1e-6]
spout_tip=max(cut_vertices,key=lambda p:p.x)
bevel=body.modifiers.new('Rounded metal seams','BEVEL'); bevel.width=.00025; bevel.segments=2
bevel.limit_method='ANGLE'; bevel.angle_limit=.7

# Lid hierarchy is independent of body and handle.
lidroot=empty('kettle_lid',(0,0,.106),root)
lid=lathe('kettle_lid_disc',[(0,.001),(.035,.001),(.044,.0005),(.048,0),
    (.049,.0005),(.0495,.0015),(.0485,.0025),(.044,.003),(.034,.005),(0,.006)],
    96,parent=lidroot,inner_start=None)
subdivide(lid)
vent=cylinder('_kettle_temporary_vent',.00135,.020,(.028,-.020,.003),parent=lidroot)
boolean(lid,vent,'DIFFERENCE','Lid pressure vent')
knob=lathe('kettle_wood_knob',[(0,0),(.0075,0),(.008,.001),(.0105,.018),
    (.011,.020),(.010,.021),(.004,.0213),(0,.0213)],64,parent=lidroot,loc=(0,0,.005),mats=(wood,))
subdivide(knob)

def bevel_box(name,dimensions,loc,mat,parent=root,rounding=.001):
    bpy.ops.mesh.primitive_cube_add(size=1)
    ob=bpy.context.object; ob.name=name
    for col in list(ob.users_collection): col.objects.unlink(ob)
    model.objects.link(ob); ob.dimensions=dimensions
    active(ob); bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    ob.parent=parent; ob.location=loc; ob.data.materials.append(mat)
    m=ob.modifiers.new('Soft manufactured edges','BEVEL'); m.width=rounding; m.segments=3
    # Object-space UV projection keeps grain along the long axis of the grip.
    if mat==wood:
        uv=ob.data.uv_layers.active or ob.data.uv_layers.new(name='WoodUV')
        for p in ob.data.polygons:
            for li in p.loop_indices:
                co=ob.data.vertices[ob.data.loops[li].vertex_index].co
                uv.data[li].uv=(co.x/dimensions[0]+.5,
                    co.y/dimensions[1]+.5 if abs(p.normal.z)>.5 else co.z/dimensions[2]+.5)
    return ob

# Hinged bail handle: flattened steel strap, two wood halves, two exposed rivets.
handle=empty('kettle_handle',(0,0,.102),root)
handle['hinge_axis_blender']='local X; upright rest pose; no animation baked'
left=[(-.080,0,.002),(-.080,0,.012),(-.077,0,.025),(-.073,0,.040),
    (-.069,0,.053),(-.065,0,.062),(-.061,0,.066),(-.055,0,.0675)]
strap_path=left+[(-.025,0,.0675),(.025,0,.0675)]+[(-p[0],p[1],p[2]) for p in reversed(left)]
verts,faces=[],[]
# Chamfered rectangular cross-section: 12 mm broad, about 1.5 mm thick.
cross=[(-.00075,-.0056),(-.00035,-.006),(.00035,-.006),(.00075,-.0056),
    (.00075,.0056),(.00035,.006),(-.00035,.006),(-.00075,.0056)]
for i,point in enumerate(strap_path):
    p=Vector(point); t=(Vector(strap_path[min(i+1,len(strap_path)-1)])-Vector(strap_path[max(i-1,0)])).normalized()
    across=t.cross(Vector((0,1,0))).normalized()
    for thickness,width in cross: verts.append(tuple(p+across*thickness+Vector((0,width,0))))
for i in range(len(strap_path)-1):
    for j in range(8):
        k=(j+1)%8; faces.append((i*8+j,i*8+k,(i+1)*8+k,(i+1)*8+j))
faces += [tuple(reversed(range(8))),tuple((len(strap_path)-1)*8+j for j in range(8))]
strap=mesh_object('kettle_handle_strap',verts,faces,parent=handle)
strap.data.materials.append(coat)
upper=bevel_box('kettle_wood_grip_upper',(.104,.020,.007),(0,0,.0715),wood,handle,.0015)
lower=bevel_box('kettle_wood_grip_lower',(.104,.020,.007),(0,0,.0635),wood,handle,.0015)
for i,xpos in enumerate((-.035,.035)):
    rivet=cylinder('kettle_grip_rivet_%d'%i,.0024,.0005,(xpos,0,.07525),steel,parent=handle)
    m=rivet.modifiers.new('Rivet edge','BEVEL'); m.width=.0002; m.segments=2
for side in (-1,1):
    label='left' if side<0 else 'right'
    bracket=bevel_box('kettle_hinge_bracket_'+label,(.004,.017,.014),(side*.079,0,.101),coat,rounding=.001)
    pin=cylinder('kettle_hinge_pin_'+label,.0025,.0075,(side*.080,0,.104),hardware,axis=(1,0,0))
    cap=cylinder('kettle_hinge_cap_'+label,.0035,.001,(side*.084,0,.104),coat,axis=(1,0,0))
# Put the moving group's pivot exactly on the line joining the hinge pins.
handle.location.z=.104
for child in handle.children: child.location.z-=.002

anchors={
    'kettle_anchor_base':(0,0,0),'kettle_anchor_opening':(0,0,.107),
    'kettle_anchor_spout_tip':tuple(spout_tip),'kettle_anchor_grip':(0,0,.1695),
    'kettle_anchor_handle_pivot':(0,0,.104),'kettle_anchor_lid_seat':(0,0,.106),
    'kettle_anchor_pour_pivot':(0,0,.055),'kettle_anchor_liquid_surface':(0,0,.085),
}
for name,p in anchors.items(): empty(name,p,root)
model.objects['kettle_anchor_opening']['radius_m']=.0485
model.objects['kettle_anchor_liquid_surface']['suggested_radius_m']=.077

def aim(ob,target): ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()
def camera_for(sc,col,name,location,target,scale):
    data=bpy.data.cameras.new(name); data.type='ORTHO'; data.ortho_scale=scale
    ob=bpy.data.objects.new(name,data); col.objects.link(ob); ob.location=location; aim(ob,target); sc.camera=ob
    return ob
studio_hdr=bpy.data.images.load(str(PROJECT/'public/environment/lebombo_1k.hdr'),check_existing=False)
studio_hdr.pack()
def studio_for(sc,col,prefix):
    ground=mesh_object(prefix+'_floor',[(-20,-20,-.0003),(20,-20,-.0003),(20,20,-.0003),(-20,20,-.0003)],[(0,1,2,3)],None,col)
    ground.data.materials.append(material(prefix+' | warm grey backdrop',(.35,.36,.365),.9))
    world=bpy.data.worlds.new(prefix+'_world'); world.use_nodes=True
    world.node_tree.nodes['Background'].inputs['Color'].default_value=(.55,.57,.60,1)
    env=world.node_tree.nodes.new('ShaderNodeTexEnvironment'); env.image=studio_hdr
    world.node_tree.links.new(env.outputs['Color'],world.node_tree.nodes['Background'].inputs['Color'])
    world.node_tree.nodes['Background'].inputs['Strength'].default_value=.4; sc.world=world
    for label,location,power,size,colour in [
        ('key',(.04,-.32,.48),13,.30,(1,.96,.90)),
        ('fill',(-.30,-.12,.25),7,.25,(.85,.91,1)),
        ('rim',(.25,.24,.38),17,.22,(1,.97,.92))]:
        data=bpy.data.lights.new(prefix+'_'+label,'AREA'); data.energy=power; data.shape='DISK'; data.size=size; data.color=colour
        ob=bpy.data.objects.new(prefix+'_'+label,data); col.objects.link(ob); ob.location=location; aim(ob,(0,0,.07))
    sc.render.engine='BLENDER_EEVEE'; sc.render.resolution_x=1560; sc.render.resolution_y=1300; sc.render.resolution_percentage=100
    sc.render.image_settings.file_format='PNG'; sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - Medium High Contrast'
studio_for(scene,studio,'KETTLE_STUDIO')
camera=camera_for(scene,studio,'KETTLE_STUDIO_camera',(.28,-.45,.285),(.015,0,.084),.32)
scene.render.filepath=str(OUT/'previews/kettle-hero.png')

# Saved asset collections are linked only into the preview comparison scene.
comparison=bpy.data.scenes.new('OjaTea | Kettle kyusu cup proportions')
comparison.unit_settings.system='METRIC'
comparison_studio=bpy.data.collections.new('KETTLE COMPARISON | Preview only'); comparison.collection.children.link(comparison_studio)
studio_for(comparison,comparison_studio,'KETTLE_COMPARISON')
references=[]
for asset,collection_name,position in [
    ('kyusu','KYUSU | Export asset',(.145,.01,0)),
    ('cup','CUP | Export asset',(.24,-.14,0))]:
    path=PROJECT/'assets'/asset/(asset+'-reference.blend')
    if bpy.data.filepath and Path(bpy.data.filepath).resolve()==path.resolve():
        bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
    with bpy.data.libraries.load(str(path),link=True) as (src,dst):
        if collection_name not in src.collections: raise RuntimeError('Reference collection missing: '+collection_name)
        dst.collections=[collection_name]
    col=dst.collections[0]; col.library.filepath='//../'+asset+'/'+asset+'-reference.blend'
    references.append((asset,col,position))
references.append(('kettle',model,(-.12,.065,0)))
for name,col,loc in references:
    ob=bpy.data.objects.new('KETTLE_REFERENCE_'+name,None); ob.instance_type='COLLECTION'; ob.instance_collection=col; ob.location=loc
    comparison.collection.objects.link(ob)
camera_for(comparison,comparison_studio,'KETTLE_COMPARISON_camera',(.38,-.73,.53),(.07,-.025,.063),.64)
comparison.render.filepath=str(OUT/'previews/kettle-with-teaware.png')

bpy.context.window.scene=scene
bpy.context.view_layer.update()
# Measure/export evaluated geometry, never studio or reference collections.
deps=bpy.context.evaluated_depsgraph_get(); points=[]; checks={}
for ob in model.objects:
    if ob.type!='MESH': continue
    ev=ob.evaluated_get(deps); me=ev.to_mesh(); me.calc_loop_triangles()
    points.extend(ob.matrix_world@v.co for v in me.vertices)
    bm=bmesh.new(); bm.from_mesh(me)
    checks[ob.name]={'triangles':len(me.loop_triangles),'boundary_edges':sum(e.is_boundary for e in bm.edges),
        'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges)}
    bm.free(); ev.to_mesh_clear()
bounds_min=[min(p[i] for p in points) for i in range(3)]; bounds_max=[max(p[i] for p in points) for i in range(3)]
dimensions=[b-a for a,b in zip(bounds_min,bounds_max)]
bpy.ops.object.select_all(action='DESELECT')
for ob in model.objects: ob.select_set(True)
bpy.context.view_layer.objects.active=body
bpy.ops.export_scene.gltf(filepath=str(GLB),export_format='GLB',use_selection=True,use_active_scene=True,
    export_yup=True,export_apply=True,export_extras=True,export_animations=False,export_cameras=False,export_lights=False)
metadata={'units':'metres','reference_dimensions_m':{'overall_width':.22,'body_diameter':.16,'height_with_handle':.177},
    'measured_dimensions_m':{'overall_width_x':dimensions[0],'depth_y':dimensions[1],'height_z':dimensions[2]},
    'bounds_min_blender':bounds_min,'bounds_max_blender':bounds_max,
    'triangles':sum(v['triangles'] for v in checks.values()),'mesh_objects':len(checks),'geometry_checks':checks,
    'glb_bytes':GLB.stat().st_size,'anchors_blender_z_up':{k:list(v) for k,v in anchors.items()},
    'anchors_gltf_y_up':{k:[v[0],v[2],-v[1]] for k,v in anchors.items()},
    'spout_cut':{'plane_normal_blender':list(spout_cut_normal),'plane_point_blender':list(spout_cut_plane),
        'description':'Upper wall cut back to a shallow diagonal mouth; pointed lower pouring lip'},
    'materials':'18-8 stainless reference; dark exterior finish inferred from photos; wood grip and knob',
    'status':'Standalone visual study. Runtime integration and calibration pending.'}
(OUT/'asset-metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
bpy.ops.object.select_all(action='DESELECT'); body.select_set(True); bpy.context.view_layer.objects.active=body
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        area.spaces.active.region_3d.view_location=(.01,0,.08); area.spaces.active.region_3d.view_distance=.39
        area.spaces.active.region_3d.view_rotation=camera.rotation_euler.to_quaternion()
        area.spaces.active.clip_start=.0005; area.spaces.active.overlay.show_extras=False
        area.spaces.active.shading.color_type='MATERIAL'
for im in (woodcolour,woodnormal): im.filepath='//textures/'+Path(im.filepath).name
old=bpy.context.preferences.filepaths.save_version; bpy.context.preferences.filepaths.save_version=0
try: bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
finally: bpy.context.preferences.filepaths.save_version=old
result={'blend':str(BLEND),'glb':str(GLB),'scene':scene.name,'comparison_scene':comparison.name,'metadata':metadata}
