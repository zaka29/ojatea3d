"""Reference-led tea caddy study. Execute inside Blender, including background mode.

Creates its own scene/collection and does not modify earlier tea-ware scenes.
Photo dimensions/materials are not known; the scale and finish are interpretations.
"""
from pathlib import Path
import math, json, struct
import bpy, bmesh
import numpy as np
from mathutils import Vector

OUT=Path(__file__).resolve().parent
PROJECT=OUT.parent.parent
BLEND=OUT/'teabox-reference.blend'
GLB=PROJECT/'public/models/teabox-reference.glb'
if BLEND.exists() or GLB.exists():
    raise RuntimeError('Tea-box output already exists; use a new version before rebuilding.')
for part in ('textures','previews'): (OUT/part).mkdir(exist_ok=True)
scene=bpy.data.scenes.new('OjaTea | Charcoal tea box study')
bpy.context.window.scene=scene
scene.unit_settings.system='METRIC'
model=bpy.data.collections.new('TEABOX | Export asset')
studio=bpy.data.collections.new('TEABOX STUDIO | Preview only')
scene.collection.children.link(model); scene.collection.children.link(studio)

def empty(name,loc=(0,0,0),parent=None):
    ob=bpy.data.objects.new(name,None); model.objects.link(ob)
    ob.location=loc; ob.parent=parent; ob.empty_display_size=.005
    return ob
root=empty('teabox_root')
root['description']='Charcoal cylindrical tea caddy, removable loop-grip lid; reference interpretation'
root['units']='metres; Blender Z up, GLB Y up; base at zero'
root['integration_status']='Standalone study; application calibration pending'

def linear(c):
    a=np.asarray(c); return np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4)
def material(name,c,rough):
    m=bpy.data.materials.new(name); m.use_nodes=True
    m.diffuse_color=(*linear(c),1); bs=m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value=m.diffuse_color
    bs.inputs['Roughness'].default_value=rough
    bs.inputs['Specular IOR Level'].default_value=.3
    return m
def image(name,rgb,noncolor=False):
    h,w,_=rgb.shape; im=bpy.data.images.new(name,width=w,height=h,alpha=False)
    im.colorspace_settings.name='Non-Color' if noncolor else 'sRGB'
    data=np.ones((h,w,4),dtype=np.float32); data[:,:,:3]=rgb
    im.pixels.foreach_set(data.ravel()); im.filepath_raw=str(OUT/'textures'/(name+'.png'))
    im.file_format='PNG'; im.save(); im.pack(); return im

rng=np.random.default_rng(6123); n=1024
y,x=np.mgrid[0:n,0:n]/n; noise=rng.random((n,n)); fine=rng.random((n,n))
cloud=.5+.16*np.sin(2*math.pi*(x*3+y))+.08*np.sin(2*math.pi*(x*9-y*2))
rgb=np.empty((n,n,3)); rgb[:]=(.101,.098,.096)
rgb+=(noise-.5)[:,:,None]*.023+(cloud-.5)[:,:,None]*.012
rgb[fine>.989]+=np.array([.029,.026,.022])
colour=image('teabox_charcoal_basecolor',np.clip(rgb,0,1))
height=(noise-.5)*.22
dx=(np.roll(height,-1,1)-np.roll(height,1,1))*.35
dy=(np.roll(height,-1,0)-np.roll(height,1,0))*.35
normal=np.stack((-dx,-dy,np.ones_like(dx)),axis=2); normal/=np.linalg.norm(normal,axis=2)[:,:,None]
normal_image=image('teabox_charcoal_normal',normal*.5+.5,True)
charcoal=material('ceramic.teabox | charcoal granular finish',(.101,.098,.096),.73)
charcoal.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=.18
nodes,links=charcoal.node_tree.nodes,charcoal.node_tree.links; bs=nodes.get('Principled BSDF')
tex=nodes.new('ShaderNodeTexImage'); tex.image=colour; links.new(tex.outputs['Color'],bs.inputs['Base Color'])
texn=nodes.new('ShaderNodeTexImage'); texn.image=normal_image
nm=nodes.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value=.65
links.new(texn.outputs['Color'],nm.inputs['Color']); links.new(nm.outputs['Normal'],bs.inputs['Normal'])
inner=material('ceramic.teabox | brown unglazed interior',(.16,.125,.100),.88)
seal=material('fibre.teabox | pale seal interpretation',(.69,.65,.50),.94)

def mesh_object(name,verts,faces,parent=root,col=model):
    me=bpy.data.meshes.new(name+'_mesh'); me.from_pydata(verts,[],faces); me.update(); me.validate()
    bm=bmesh.new(); bm.from_mesh(me); bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-8)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces)); bm.to_mesh(me); bm.free()
    ob=bpy.data.objects.new(name,me); col.objects.link(ob); ob.parent=parent
    for p in me.polygons: p.use_smooth=True
    return ob
def lathe(name,profile,parent=root,loc=(0,0,0),mats=(charcoal,),brown_from=None):
    verts,rings,faces,rows=[],[],[],[]; seg=96
    for r,z in profile:
        if r==0: rings.append([len(verts)]); verts.append((0,0,z))
        else:
            ring=[]
            for j in range(seg):
                a=j*2*math.pi/seg; rr=r*(1+.0007*math.sin(3*a))
                ring.append(len(verts)); verts.append((rr*math.cos(a),rr*math.sin(a),z))
            rings.append(ring)
    for row,(lo,hi) in enumerate(zip(rings[:-1],rings[1:])):
        for j in range(seg):
            k=(j+1)%seg
            f=(lo[0],hi[k],hi[j]) if len(lo)==1 else ((lo[j],lo[k],hi[0]) if len(hi)==1 else (lo[j],lo[k],hi[k],hi[j]))
            faces.append(f); rows.append(row)
    ob=mesh_object(name,verts,faces,parent); ob.location=loc
    for m in mats: ob.data.materials.append(m)
    uv=ob.data.uv_layers.new(name='SurfaceUV')
    zlo,zhi=min(z for r,z in profile),max(z for r,z in profile)
    for p,row in zip(ob.data.polygons,rows):
        if brown_from is not None and row>=brown_from: p.material_index=1
        values=[]
        for li in p.loop_indices:
            v=ob.data.vertices[ob.data.loops[li].vertex_index].co
            values.append((li,(math.atan2(v.y,v.x)/(2*math.pi))%1,(v.z-zlo)/max(zhi-zlo,.001)))
        seam=max(t[1] for t in values)-min(t[1] for t in values)>.5
        for li,u,v in values: uv.data[li].uv=(u+1 if seam and u<.5 else u,v)
    mod=ob.modifiers.new('Soft handmade profile','SUBSURF'); mod.levels=1; mod.render_levels=1
    return ob

body_profile=[(0,.002),(.033,.002),(.040,.002),(.042,0),(.043,0),(.044,.0015),
 (.045,.005),(.0452,.012),(.0452,.035),(.0451,.070),(.0448,.094),(.0447,.098),
 (.0445,.100),(.0437,.1005),(.0425,.1005),(.0414,.0998),(.0412,.098),
 (.0411,.094),(.0411,.080),(.0412,.060),(.0412,.040),(.041,.020),
 (.040,.009),(.038,.005),(.030,.0045),(0,.0045)]
body=lathe('teabox_body',body_profile,mats=(charcoal,inner),brown_from=12)
bpy.context.view_layer.update(); ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get()); me=ev.to_mesh()
bottom=min(v.co.z for v in me.vertices); ev.to_mesh_clear()
for v in body.data.vertices: v.co.z-=bottom
body.data.update()
lidroot=empty('teabox_lid',(0,0,.1005-bottom),root)
lid=lathe('teabox_lid_disc',[(0,-.003),(.031,-.003),(.039,-.003),(.0408,-.0028),
 (.0435,-.0015),(.0448,-.001),(.045,.0005),(.045,.0025),(.0446,.004),
 (.0435,.0045),(.033,.0048),(0,.005)],parent=lidroot)
insert=lathe('teabox_lid_insert',[(0,-.006),(.035,-.006),(.0394,-.006),(.0402,-.005),
 (.0405,-.0015),(.0395,-.001),(0,-.001)],parent=lidroot,mats=(inner,))
# The pale ring is inferred from the visible lid underside; exact material unknown.
gasket=lathe('teabox_lid_seal',[(.040,-.0055),(.0407,-.0055),(.0412,-.0048),
 (.0412,-.003),(.0406,-.0025),(.040,-.0025),(.040,-.0055)],parent=lidroot,mats=(seal,))

# A real arched loop, not a solid fin; rounded feet meet the lid surface.
verts,faces=[],[]; sections=48; sides=12
for i in range(sections+1):
    t=i*math.pi/sections
    p=Vector((-.013*math.cos(t),0,.004+.018*math.sin(t)))
    tangent=Vector((.013*math.sin(t),0,.018*math.cos(t))).normalized()
    radial=tangent.cross(Vector((0,1,0))).normalized()
    for j in range(sides):
        a=j*2*math.pi/sides; r=.0032
        verts.append(tuple(p+r*(math.cos(a)*Vector((0,1,0))+math.sin(a)*radial)))
for i in range(sections):
    for j in range(sides):
        k=(j+1)%sides; faces.append((i*sides+j,i*sides+k,(i+1)*sides+k,(i+1)*sides+j))
faces.append(tuple(reversed(range(sides)))); faces.append(tuple(sections*sides+j for j in range(sides)))
loop=mesh_object('teabox_lid_loop',verts,faces,lidroot); loop.data.materials.append(charcoal)
uv=loop.data.uv_layers.new(name='SurfaceUV')
for p in loop.data.polygons:
    for li in p.loop_indices:
        v=loop.data.vertices[loop.data.loops[li].vertex_index].co
        uv.data[li].uv=(v.x/.03+.5,v.z/.03)

anchors={'teabox_anchor_base':(0,0,0),'teabox_anchor_opening':(0,0,.100-bottom),
 'teabox_anchor_lid_seat':tuple(lidroot.location),'teabox_anchor_grip':(0,0,.1225-bottom),
 'teabox_anchor_scoop_entry':(0,0,.112-bottom)}
for name,loc in anchors.items(): empty(name,loc,root)
model.objects['teabox_anchor_opening']['radius_m']=.041
model.objects['teabox_anchor_scoop_entry']['clearance_radius_m']=.038

def aim(ob,target): ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()
floor=mesh_object('TEABOX_STUDIO_floor',[(-10,-10,-.0002),(10,-10,-.0002),(10,10,-.0002),(-10,10,-.0002)],[(0,1,2,3)],None,studio)
floor.data.materials.append(material('TEABOX_STUDIO | neutral backdrop',(.40,.405,.41),.9))
world=bpy.data.worlds.new('TEABOX_STUDIO_world'); world.use_nodes=True
world.node_tree.nodes['Background'].inputs['Strength'].default_value=.25
scene.world=world
for suffix,loc,power,size in [('key',(.05,-.27,.36),8,.23),('fill',(-.23,-.03,.22),4,.20),('rim',(.20,.18,.28),7,.18)]:
    data=bpy.data.lights.new('TEABOX_STUDIO_'+suffix,'AREA'); data.energy=power; data.shape='DISK'; data.size=size
    ob=bpy.data.objects.new(data.name,data); studio.objects.link(ob); ob.location=loc; aim(ob,(0,0,.06))
camera_data=bpy.data.cameras.new('TEABOX_STUDIO_camera'); camera=bpy.data.objects.new(camera_data.name,camera_data)
studio.objects.link(camera); camera_data.type='ORTHO'; camera_data.ortho_scale=.20
camera.location=(.16,-.24,.20); aim(camera,(0,0,.060)); scene.camera=camera
scene.render.engine='BLENDER_EEVEE'; scene.render.resolution_x=1400; scene.render.resolution_y=1200; scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'; scene.view_settings.view_transform='AgX'; scene.view_settings.look='AgX - Medium High Contrast'

bpy.context.view_layer.update(); deps=bpy.context.evaluated_depsgraph_get(); checks={}; points=[]
for ob in model.objects:
    if ob.type!='MESH': continue
    ev=ob.evaluated_get(deps); me=ev.to_mesh(); me.calc_loop_triangles(); bm=bmesh.new(); bm.from_mesh(me)
    points.extend(ob.matrix_world@v.co for v in me.vertices)
    checks[ob.name]={'triangles':len(me.loop_triangles),'boundary_edges':sum(e.is_boundary for e in bm.edges),
      'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges)}
    bm.free(); ev.to_mesh_clear()
assert all(c['boundary_edges']==c['nonmanifold_edges']==0 for c in checks.values())
dimensions=[max(p[i] for p in points)-min(p[i] for p in points) for i in range(3)]
bpy.ops.object.select_all(action='DESELECT')
for ob in model.objects: ob.select_set(True)
bpy.context.view_layer.objects.active=body
bpy.ops.export_scene.gltf(filepath=str(GLB),export_format='GLB',use_selection=True,use_active_scene=True,
 export_yup=True,export_apply=True,export_extras=True,export_animations=False,export_lights=False,export_cameras=False)
metadata={'units':'metres','dimensions_xyz_m':dimensions,'body_height_m':.1005-bottom,'opening_radius_m':.041,
 'triangles':sum(c['triangles'] for c in checks.values()),'mesh_objects':len(checks),'geometry_checks':checks,
 'glb_bytes':GLB.stat().st_size,'anchors_blender_z_up':{k:list(v) for k,v in anchors.items()},
 'anchors_gltf_y_up':{k:[v[0],v[2],-v[1]] for k,v in anchors.items()},
 'materials':'Charcoal granular finish and brown interior; pale lid seal interpreted from references, exact material unknown',
 'status':'Standalone visual study; runtime integration and calibration pending.'}
(OUT/'asset-metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
scene.render.filepath=str(OUT/'previews/teabox-closed.png')
bpy.ops.render.render(write_still=True,scene=scene.name)
lidroot.location=(-.084,-.045,.007)
camera.location=(.17,-.25,.28); aim(camera,(-.022,-.008,.045)); camera_data.ortho_scale=.255
scene.render.filepath=str(OUT/'previews/teabox-open.png')
bpy.ops.render.render(write_still=True,scene=scene.name)
lidroot.location=anchors['teabox_anchor_lid_seat']; camera.location=(.16,-.24,.20); aim(camera,(0,0,.060)); camera_data.ortho_scale=.20
scene.render.filepath=str(OUT/'previews/teabox-closed.png')
for im in (colour,normal_image): im.filepath='//textures/'+Path(im.filepath).name
# Write only this new scene and its dependencies, keeping the source compact.
bpy.data.libraries.write(str(BLEND),{scene},path_remap='RELATIVE_ALL',fake_user=True,compress=True)
result={'blend':str(BLEND),'glb':str(GLB),'metadata':metadata}
