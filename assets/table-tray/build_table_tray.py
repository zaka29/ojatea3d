"""Reference-inspired table and tea tray, built in an isolated Blender process.

Run with Blender --background --factory-startup --python this_file.py, or via
the Blender MCP CLI tool. No existing .blend file is overwritten.
"""
from pathlib import Path
import bpy
import bmesh
import numpy as np
import math
import json
from mathutils import Vector

OUT=Path(__file__).resolve().parent
PROJECT=OUT.parent.parent
BLEND=OUT/'table-tray-reference.blend'
TABLE_GLB=PROJECT/'public/models/table-reference.glb'
TRAY_GLB=PROJECT/'public/models/tray-reference.glb'
if not globals().get('ALLOW_REBUILD',False) and (BLEND.exists() or TABLE_GLB.exists() or TRAY_GLB.exists()):
    raise RuntimeError('Outputs already exist. Choose a new version before rebuilding.')
for folder in ('textures','previews'): (OUT/folder).mkdir(exist_ok=True)

# This reset is local to the disposable background process, never the live UI.
bpy.ops.wm.read_factory_settings(use_empty=True)
table_scene=bpy.data.scenes.new('OjaTea | Rustic table study')
tray_scene=bpy.data.scenes.new('OjaTea | Walnut tea tray study')
room_scene=bpy.data.scenes.new('OjaTea | Table and tray setting')
for scene in (table_scene,tray_scene,room_scene): scene.unit_settings.system='METRIC'
table_col=bpy.data.collections.new('TABLE | Export asset'); table_scene.collection.children.link(table_col)
tray_col=bpy.data.collections.new('TRAY | Export asset'); tray_scene.collection.children.link(tray_col)

def scene_active(scene):
    bpy.context.window.scene=scene

def empty(name,col,loc=(0,0,0),parent=None):
    ob=bpy.data.objects.new(name,None); col.objects.link(ob); ob.parent=parent; ob.location=loc; ob.empty_display_size=.035
    return ob
table_root=empty('table_root',table_col)
tray_root=empty('tray_root',tray_col)
table_root['description']='Rustic aged plank table; leg structure inferred, not visible in references'
tray_root['description']='Rounded walnut slab, pale longitudinal inlay, recessed drain channel and separate pull-out catch pan'
for root in (table_root,tray_root): root['units']='metres; Blender Z up / glTF Y up; base zero'

def linear(rgb):
    rgb=np.asarray(rgb); return np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4)

def material(name,rgb,roughness,metal=0):
    m=bpy.data.materials.new(name); m.use_nodes=True
    rgba=(*linear(rgb),1); m.diffuse_color=rgba
    bs=m.node_tree.nodes.get('Principled BSDF'); bs.inputs['Base Color'].default_value=rgba
    bs.inputs['Roughness'].default_value=roughness; bs.inputs['Metallic'].default_value=metal
    return m

def image(name,rgb,noncolor=False):
    h,w,_=rgb.shape; im=bpy.data.images.new(name,width=w,height=h,alpha=False)
    im.colorspace_settings.name='Non-Color' if noncolor else 'sRGB'
    values=np.ones((h,w,4),dtype=np.float32); values[:,:,:3]=np.clip(rgb,0,1)
    im.pixels.foreach_set(values.ravel()); im.filepath_raw=str(OUT/'textures'/(name+'.png')); im.file_format='PNG'; im.save(); im.pack()
    return im

images=[]
def wood_material(name,base,seed,weathered=False):
    w,h=1536,768; rng=np.random.default_rng(seed)
    y,x=np.mgrid[0:h,0:w]/np.array([h-1,w])[:,None,None]
    # Varying line density and drifting fibres, with elongated knot swirls.
    flow=y+.015*np.sin(x*2*math.pi*1.5)+.006*np.sin(x*2*math.pi*5)
    knots=rng.uniform(-1,1,241); position=np.mod(flow,1)*240
    ix=np.floor(position).astype(int); t=position-ix; t=t*t*(3-2*t)
    fibres=knots[ix]*(1-t)+knots[ix+1]*t
    noise=rng.random((h,w))-.5
    def field(nx,ny):
        grid=rng.uniform(-1,1,(ny+1,nx+1)); gx=x*nx; gy=y*ny
        xi=np.minimum(gx.astype(int),nx-1); yi=np.minimum(gy.astype(int),ny-1)
        a=gx-xi; b=gy-yi; a=a*a*(3-2*a); b=b*b*(3-2*b)
        return grid[yi,xi]*(1-a)*(1-b)+grid[yi,xi+1]*a*(1-b)+grid[yi+1,xi]*(1-a)*b+grid[yi+1,xi+1]*a*b
    cloud=field(4,7)*.65+field(12,24)*.25
    colour=np.empty((h,w,3)); colour[:]=base
    colour+=fibres[:,:,None]*np.array([.025,.020,.014])
    colour+=cloud[:,:,None]*np.array([.10,.085,.060])
    colour+=noise[:,:,None]*.023
    relief=fibres*.015+noise*.004
    for cx,cy,rx,ry in [(.24,.36,.045,.060),(.71,.75,.032,.055),(.88,.19,.02,.04)]:
        rr=np.sqrt(((x-cx)/rx)**2+((y-cy)/ry)**2)
        knot=np.exp(-rr*rr*.5)
        rings=np.sin(rr*15+np.sin(x*17)*.4)
        colour-=knot[:,:,None]*np.array([.07,.06,.04])
        colour+=((knot*rings)[:,:,None])*np.array([.020,.018,.012])
        relief+=knot*rings*.005
    if weathered:
        # Fine dark seasoning checks, a few pale worn patches and open pores.
        for cy,start,end,phase in [(.09,.04,.55,1.0),(.14,.08,.65,1.5),(.32,.18,.76,2),(.53,.36,.92,2.6),(.69,.03,.31,3.4),(.82,.10,.42,4.3),(.93,.58,.96,5.0)]:
            line=cy+.003*np.sin(x*27+phase)+.0015*np.sin(x*67+phase)
            split=np.exp(-((y-line)/.0014)**2)*np.clip((x-start)*70,0,1)*np.clip((end-x)*70,0,1)
            colour-=split[:,:,None]*np.array([.17,.15,.11]); relief-=split*.09
        colour+=np.clip(cloud,0,1)[:,:,None]*np.array([.045,.045,.042])
    dx=(np.roll(relief,-1,1)-np.roll(relief,1,1))*.4
    dy=(np.roll(relief,-1,0)-np.roll(relief,1,0))*.4
    normal=np.stack((-dx,-dy,np.ones_like(dx)),axis=2); normal/=np.linalg.norm(normal,axis=2)[:,:,None]
    slug=name.split(' | ')[0]
    c=image(slug+'_basecolor',colour); n=image(slug+'_normal',normal*.5+.5,True); images.extend([c,n])
    m=material(name,base,.81 if weathered else .40)
    nodes,links=m.node_tree.nodes,m.node_tree.links; bs=nodes.get('Principled BSDF')
    tex=nodes.new('ShaderNodeTexImage'); tex.image=c; tex.location=(-500,150); links.new(tex.outputs['Color'],bs.inputs['Base Color'])
    tex=nodes.new('ShaderNodeTexImage'); tex.image=n; tex.location=(-500,-150)
    nm=nodes.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value=.45; nm.location=(-200,-100)
    links.new(tex.outputs['Color'],nm.inputs['Color']); links.new(nm.outputs['Normal'],bs.inputs['Normal'])
    return m

aged=wood_material('table_aged_oak | weathered warm timber',(.160,.130,.095),184,True)
walnut=wood_material('tray_walnut | dark warm walnut',(.145,.070,.028),841,False)
inlay=material('tray_inlay | pale timber',(.74,.65,.44),.52)
panmat=material('tray_pan | charcoal finish',(.055,.060,.061),.59,.07)
feetmat=material('tray_feet | dark supports',(.045,.040,.031),.9)

def active(ob):
    bpy.ops.object.select_all(action='DESELECT'); ob.select_set(True); bpy.context.view_layer.objects.active=ob

def mesh_object(name,verts,faces,col,parent=None):
    me=bpy.data.meshes.new(name+'_mesh'); me.from_pydata(verts,[],faces); me.update(); me.validate()
    bm=bmesh.new(); bm.from_mesh(me); bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-8)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces)); bm.to_mesh(me); bm.free()
    ob=bpy.data.objects.new(name,me); col.objects.link(ob); ob.parent=parent
    return ob

def box(name,dims,loc,mat,col,parent=None,bevel=.002,uv_scale=None):
    bpy.ops.mesh.primitive_cube_add(size=1)
    ob=bpy.context.object; ob.name=name
    for c in list(ob.users_collection): c.objects.unlink(ob)
    col.objects.link(ob); ob.dimensions=dims; active(ob); bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    ob.parent=parent; ob.location=loc; ob.data.materials.append(mat)
    if bevel:
        mod=ob.modifiers.new('Soft worn edges','BEVEL'); mod.width=bevel; mod.segments=3
    uv_project(ob,uv_scale or dims)
    return ob

def uv_project(ob,scale):
    me=ob.data; uv=me.uv_layers.active or me.uv_layers.new(name='WoodUV')
    for p in me.polygons:
        for li in p.loop_indices:
            co=me.vertices[me.loops[li].vertex_index].co
            # Wood fibres run in the long X direction. Side walls retain grain.
            if abs(p.normal.z)>.5: v=co.y/scale[1]
            else: v=(co.z/scale[2] if abs(p.normal.y)>.5 else co.y/scale[1])
            uv.data[li].uv=(co.x/scale[0]+.5,v+.5)

def outline(w,d,r,segments=12):
    points=[]
    for cx,cy,start in [(w/2-r,d/2-r,0),(-w/2+r,d/2-r,90),(-w/2+r,-d/2+r,180),(w/2-r,-d/2+r,270)]:
        for j in range(segments+1):
            a=math.radians(start+j*90/segments)
            points.append((cx+r*math.cos(a),cy+r*math.sin(a)))
    return points

def rounded_slab(name,w,d,height,r,z,mat,col,parent=None,edge=.002):
    perimeter=outline(w,d,r); n=len(perimeter)
    verts=[(x,y,zz) for zz in (z-height/2,z+height/2) for x,y in perimeter]
    faces=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]
    faces.extend((i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n))
    ob=mesh_object(name,verts,faces,col,parent); ob.data.materials.append(mat)
    if edge:
        mod=ob.modifiers.new('Rounded slab edges','BEVEL'); mod.width=edge; mod.segments=3; mod.limit_method='ANGLE'; mod.angle_limit=.5
    uv_project(ob,(w,d,height))
    return ob

def boolean(ob,other,label):
    active(ob); m=ob.modifiers.new(label,'BOOLEAN'); m.operation='DIFFERENCE'; m.solver='EXACT'; m.object=other
    # Boolean before the retained edge treatment.
    while ob.modifiers.find(m.name)>0: bpy.ops.object.modifier_move_up(modifier=m.name)
    bpy.ops.object.modifier_apply(modifier=m.name); bpy.data.objects.remove(other,do_unlink=True)

scene_active(table_scene)
# Five parallel, seasoned planks. Heights remain level despite surface texture.
for i in range(5):
    p=box('table_top_plank_%02d'%i,(1.6,.1686,.04),(0,(i-2)*.17,.70),aged,table_col,table_root,.0025,(1.6,.85,.04))
    # Each board samples a different portion of the shared texture.
    for datum in p.data.uv_layers.active.data: datum.uv.y+=i*.177; datum.uv.x+=(i%2)*.32
# A small irregular edge loss provides real, localised ageing near the edge,
# away from the central tray placement. The reference shows much deeper wear.
notch=[(-.56,-.45),(-.56,-.42),(-.542,-.414),(-.53,-.397),(-.516,-.414),(-.49,-.408),(-.46,-.43),(-.46,-.45)]
verts=[(x,y,z) for z in (.66,.75) for x,y in notch]; n=len(notch)
faces=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
cutter=mesh_object('_table_temporary_edge_wear',verts,faces,table_col)
boolean(table_col.objects['table_top_plank_00'],cutter,'Local worn edge notch')
for side in (-1,1):
    for front in (-1,1):
        leg=box('table_leg_%s_%s'%(side,front),(.075,.075,.68),(side*.65,front*.30,.34),aged,table_col,table_root,.003,(.075,.075,.68))
        for datum in leg.data.uv_layers.active.data: datum.uv=(datum.uv.y,datum.uv.x)
    box('table_end_apron_%s'%side,(.045,.65,.11),(side*.65,0,.625),aged,table_col,table_root,.002)
for front in (-1,1):
    box('table_long_apron_%s'%front,(1.3,.04,.11),(0,front*.30,.625),aged,table_col,table_root,.002)
    box('table_low_stretcher_%s'%front,(1.3,.035,.05),(0,front*.30,.19),aged,table_col,table_root,.002)
table_anchors={'table_anchor_base':(0,0,0),'table_anchor_surface':(0,0,.72)}
for name,p in table_anchors.items(): empty(name,table_col,p,table_root)

scene_active(tray_scene)
slab=rounded_slab('tray_walnut_slab',.84,.44,.022,.026,.025,walnut,tray_col,tray_root,.0035)
# Narrow, flush pale inlay. Its top plane is identical to the service surface.
strip=box('tray_pale_inlay',(.785,.004,.002),(0,-.122,.035),inlay,tray_col,tray_root,.0003)
inset=box('_tray_temporary_inlay_inset',(.786,.0044,.004),(0,-.122,.035),inlay,tray_col,None,0)
boolean(slab,inset,'Flush inlay seat')
# A recessed channel alongside the inlay. No raised rim is introduced.
cutter=rounded_slab('_tray_temporary_channel',.735,.010,.009,.0049,.035,panmat,tray_col,None,0)
cutter.location.y=-.102
boolean(slab,cutter,'Recessed drainage channel')
for x in (-.31,.31):
    bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=.002,depth=.05,location=(x,-.102,.025))
    cut=bpy.context.object; cut.name='_tray_temporary_drain'
    for c in list(cut.users_collection): c.objects.unlink(cut)
    tray_col.objects.link(cut); boolean(slab,cut,'Channel drain into catch pan')
for x in (-.398,.398):
    for y in (-.196,.196):
        box('tray_support_%s_%s'%(x,y),(.024,.023,.014),(x,y,.007),feetmat,tray_col,tray_root,.002)
for x in (-.376,.376):
    box('tray_pan_guide_%s'%x,(.012,.37,.005),(x,0,.011),feetmat,tray_col,tray_root,.001)

panroot=empty('tray_catch_pan',tray_col,parent=tray_root)
panroot['motion_axis']='local +Y; neutral pose closed; preview extension .20 m'
panprofile=[(.730,.356,.007,.004),(.730,.356,.007,.013),(.726,.352,.005,.013),(.726,.352,.005,.0056)]
verts=[]; loops=[]
for w,d,r,z in panprofile:
    ring=[]
    for x,y in outline(w,d,r): ring.append(len(verts)); verts.append((x,y,z))
    loops.append(ring)
n=len(loops[0]); faces=[tuple(reversed(loops[0])),tuple(loops[-1])]
for lo,hi in zip(loops[:-1],loops[1:]):
    for j in range(n): faces.append((lo[j],lo[(j+1)%n],hi[(j+1)%n],hi[j]))
pan=mesh_object('tray_catch_pan_shell',verts,faces,tray_col,panroot); pan.data.materials.append(panmat)
mod=pan.modifiers.new('Pan softened corners','BEVEL'); mod.width=.0005; mod.segments=2; mod.limit_method='ANGLE'; mod.angle_limit=.5
# A discreet grasping flange remains within the footprint when closed.
box('tray_catch_pan_front',(.736,.006,.011),(0,.180,.0085),panmat,tray_col,panroot,.001)
tray_anchors={'tray_anchor_base':(0,0,0),'tray_anchor_surface':(0,0,.036),
    'tray_anchor_pan_closed':(0,0,0),'tray_anchor_pan_open':(0,.20,0),'tray_anchor_channel':(0,-.102,.0305)}
for name,p in tray_anchors.items(): empty(name,tray_col,p,tray_root)
tray_col.objects['tray_anchor_surface']['usable_bounds_xy']=[-.39,.39,-.075,.195]

def aim(ob,target): ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()
hdr=bpy.data.images.load(str(PROJECT/'public/environment/lebombo_1k.hdr'),check_existing=False); hdr.pack()
def studio_for(scene,prefix):
    col=bpy.data.collections.new(prefix+' | Preview only'); scene.collection.children.link(col)
    ground=mesh_object(prefix+'_floor',[(-20,-20,-.002),(20,-20,-.002),(20,20,-.002),(-20,20,-.002)],[(0,1,2,3)],col)
    ground.data.materials.append(material(prefix+' | warm grey floor',(.30,.29,.26),.94))
    world=bpy.data.worlds.new(prefix+'_world'); world.use_nodes=True
    env=world.node_tree.nodes.new('ShaderNodeTexEnvironment'); env.image=hdr
    world.node_tree.links.new(env.outputs['Color'],world.node_tree.nodes['Background'].inputs['Color'])
    world.node_tree.nodes['Background'].inputs['Strength'].default_value=.24; scene.world=world
    for label,loc,power,size,colour in [('key',(-.8,-1.1,2.4),450,1.5,(1,.86,.69)),('fill',(1.2,-.2,1.7),180,1.2,(.78,.86,1)),('rim',(.4,1.5,2.1),250,1.3,(1,.95,.86))]:
        d=bpy.data.lights.new(prefix+'_'+label,'AREA'); d.energy=power; d.shape='DISK'; d.size=size; d.color=colour
        ob=bpy.data.objects.new(prefix+'_'+label,d); col.objects.link(ob); ob.location=loc; aim(ob,(0,0,.35))
    d=bpy.data.cameras.new(prefix+'_camera'); d.type='ORTHO'; ob=bpy.data.objects.new(prefix+'_camera',d); col.objects.link(ob); scene.camera=ob
    scene.render.engine='CYCLES'; scene.cycles.device='CPU'; scene.cycles.samples=32; scene.cycles.use_denoising=True
    scene.render.resolution_x=1500; scene.render.resolution_y=1150; scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'; scene.view_settings.view_transform='AgX'; scene.view_settings.look='AgX - Medium High Contrast'
    return col
for sc,prefix in [(table_scene,'TABLE_STUDIO'),(tray_scene,'TRAY_STUDIO'),(room_scene,'FURNITURE_STUDIO')]: studio_for(sc,prefix)
table_scene.camera.location=(1.5,-1.45,1.35); aim(table_scene.camera,(0,0,.41)); table_scene.camera.data.ortho_scale=2.05
tray_scene.camera.location=(.60,-.85,.85); aim(tray_scene.camera,(0,0,.02)); tray_scene.camera.data.ortho_scale=1.02
for name,col,loc in [('table',table_col,(0,0,0)),('tray',tray_col,(0,0,.72))]:
    ob=bpy.data.objects.new('FURNITURE_REFERENCE_'+name,None); ob.instance_type='COLLECTION'; ob.instance_collection=col; ob.location=loc; room_scene.collection.objects.link(ob)
room_scene.camera.location=(1.45,-1.6,1.55); aim(room_scene.camera,(0,0,.47)); room_scene.camera.data.ortho_scale=2.05

def validate_collection(col):
    deps=bpy.context.evaluated_depsgraph_get(); checks={}; points=[]
    for ob in col.objects:
        if ob.type!='MESH': continue
        ev=ob.evaluated_get(deps); me=ev.to_mesh(); me.calc_loop_triangles(); bm=bmesh.new(); bm.from_mesh(me)
        checks[ob.name]={'triangles':len(me.loop_triangles),'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges)}
        points.extend(ob.matrix_world@v.co for v in me.vertices)
        bm.free(); ev.to_mesh_clear()
    assert all(v['boundary_edges']==v['nonmanifold_edges']==0 for v in checks.values())
    lo=[min(p[i] for p in points) for i in range(3)]; hi=[max(p[i] for p in points) for i in range(3)]
    return {'mesh_objects':len(checks),'triangles':sum(v['triangles'] for v in checks.values()),'bounds_min':lo,'bounds_max':hi,'geometry_checks':checks}

metadata={'units':'metres','inference':'Dimensions and unseen table legs are inferred from reference photographs.',
    'table':{'surface_z':.72,'dimensions_m':[1.6,.8486,.72],'anchors_blender_z_up':{k:list(v) for k,v in table_anchors.items()}},
    'tray':{'surface_z':.036,'dimensions_m':[.84,.44,.036],'main_usable_bounds_xy':[-.39,.39,-.075,.195],
        'foreground_strip_xy':[-.39,.39,-.19,-.13],'drain_channel_y':-.102,'inlay_y':-.122,'pan_motion_axis':'+Y','pan_open_offset_m':.20,
        'anchors_blender_z_up':{k:list(v) for k,v in tray_anchors.items()}}}
for scene,col,path,key in [(table_scene,table_col,TABLE_GLB,'table'),(tray_scene,tray_col,TRAY_GLB,'tray')]:
    scene_active(scene); bpy.context.view_layer.update(); metadata[key].update(validate_collection(col))
    bpy.ops.object.select_all(action='DESELECT')
    for ob in col.objects: ob.select_set(True)
    bpy.context.view_layer.objects.active=next(o for o in col.objects if o.type=='MESH')
    bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',use_selection=True,use_active_scene=True,
        export_yup=True,export_apply=True,export_extras=True,export_animations=False,export_cameras=False,export_lights=False)
    metadata[key]['glb_bytes']=path.stat().st_size
    metadata[key]['anchors_gltf_y_up']={k:[v[0],v[2],-v[1]] for k,v in metadata[key]['anchors_blender_z_up'].items()}
(OUT/'asset-metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')

# Render through the isolated background process, not the live Blender session.
def render(scene,name):
    scene_active(scene); scene.render.filepath=str(OUT/'previews'/name); bpy.ops.render.render(write_still=True,scene=scene.name)
render(table_scene,'table-hero.png')
render(tray_scene,'tray-closed.png')
panroot.location.y=.20; tray_scene.camera.data.ortho_scale=1.20; aim(tray_scene.camera,(0,.05,.02)); render(tray_scene,'tray-pan-open.png'); panroot.location.y=0
tray_scene.camera.data.ortho_scale=1.02; aim(tray_scene.camera,(0,0,.02))
render(room_scene,'table-and-tray.png')
scene_active(room_scene)
for im in images: im.filepath='//textures/'+Path(im.filepath).name
hdr.filepath='//../../public/environment/lebombo_1k.hdr'
old=bpy.context.preferences.filepaths.save_version; bpy.context.preferences.filepaths.save_version=0
try: bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
finally: bpy.context.preferences.filepaths.save_version=old
result={'blend':str(BLEND),'table_glb':str(TABLE_GLB),'tray_glb':str(TRAY_GLB),'metadata':metadata}
