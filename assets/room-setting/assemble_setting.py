"""Stage the independently authored room furnishings and tea ware in Blender.

Run in an isolated background Blender process after all asset studies exist.
This creates a NEW scene, saves only that
scene and its dependencies, and does not change original model transforms.
This is a visual composition study, not an application layout implementation.
"""
from pathlib import Path
import json
import math
import bpy
from mathutils import Vector,Matrix,Quaternion

OUT=Path(__file__).resolve().parent
PROJECT=OUT.parent.parent
OUTPUT=OUT/'room-setting-study.blend'
if OUTPUT.exists():
    raise RuntimeError('Setting output exists; use a new version before rebuilding.')
if not bpy.app.background:
    raise RuntimeError('Run this composition script in isolated background Blender, not the live UI.')
# Discard only this isolated process's seed file so every source can be linked
# externally, including whichever asset the CLI tool used to launch Blender.
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.data.scenes.new('OjaTea | Shared furnishing study')
scene.unit_settings.system='METRIC'
assets=bpy.data.collections.new('ROOM SETTING | Asset instances')
studio=bpy.data.collections.new('ROOM SETTING | Preview studio')
scene.collection.children.link(assets); scene.collection.children.link(studio)

def collection_from(relative_path,name):
    path=PROJECT/relative_path
    if bpy.data.filepath and Path(bpy.data.filepath).resolve()==path.resolve():
        col=bpy.data.collections.get(name)
        if col is None: raise RuntimeError('Collection not present in loaded file: '+name)
        return col
    with bpy.data.libraries.load(str(path),link=True) as (source,target):
        if name not in source.collections: raise RuntimeError('Missing export collection: '+name)
        target.collections=[name]
    col=target.collections[0]
    col.library.filepath='//../'+str(Path(relative_path).relative_to('assets'))
    return col

table=collection_from('assets/table-tray/table-tray-reference.blend','TABLE | Export asset')
tray=collection_from('assets/table-tray/table-tray-reference.blend','TRAY | Export asset')
box=collection_from('assets/teabox/teabox-reference.blend','TEABOX | Export asset')
pot=collection_from('assets/kyusu/kyusu-reference.blend','KYUSU | Export asset')
cup=collection_from('assets/cup/cup-reference.blend','CUP | Export asset')
kettle=collection_from('assets/kettle/kettle-reference.blend','KETTLE | Export asset')

def source_matrix(ob):
    # Linked collections are not direct members of the active view layer yet;
    # their cached matrix_world may still be identity. Compose authored local
    # transforms explicitly for these static, unconstrained asset hierarchies.
    if ob.rotation_mode=='QUATERNION': rotation=ob.rotation_quaternion
    elif ob.rotation_mode=='AXIS_ANGLE': rotation=Quaternion(Vector(ob.rotation_axis_angle[1:]),ob.rotation_axis_angle[0])
    else: rotation=ob.rotation_euler.to_quaternion()
    matrix=Matrix.LocRotScale(ob.location,rotation,ob.scale)
    return source_matrix(ob.parent)@ob.matrix_parent_inverse@matrix if ob.parent else matrix

def anchor_height(col,candidates):
    for name in candidates:
        ob=next((o for o in col.all_objects if o.name.split('.')[0]==name),None)
        if ob is not None: return float(source_matrix(ob).translation.z)
    raise RuntimeError('No surface anchor found: '+', '.join(candidates))

tabletop=anchor_height(table,['table_anchor_surface','anchor_table_surface','table_surface'])
traytop=anchor_height(tray,['tray_anchor_surface','anchor_tray_surface','tray_surface'])
tray_offset=(0,-.025,tabletop)
service_z=tabletop+traytop
# The final positions may be adjusted after inspecting the tray's actual
# drainage channel and usable zones. All models retain their real metre scale.
placements=[
    ('table',table,(0,0,0)),('tray',tray,tray_offset),
    ('kettle',kettle,(-.245,.080+tray_offset[1],service_z)),
    ('teabox',box,(-.030,.130+tray_offset[1],service_z)),
    ('kyusu',pot,(.120,.065+tray_offset[1],service_z)),
    ('cup',cup,(.310,.110+tray_offset[1],service_z)),
]
instances={}
for name,col,position in placements:
    ob=bpy.data.objects.new('SETTING_'+name,None)
    ob.instance_type='COLLECTION'; ob.instance_collection=col; ob.location=position
    assets.objects.link(ob); instances[name]=ob

# Check the staged footprints rather than claiming ceremony clearance from a
# render. This only checks static bounds/support; guided motion is later work.
def bounds_of(col,offset):
    points=[Vector(offset)+(source_matrix(ob)@Vector(corner))
        for ob in col.all_objects if ob.type=='MESH' for corner in ob.bound_box]
    return {'min':[min(p[i] for p in points) for i in range(3)],
        'max':[max(p[i] for p in points) for i in range(3)]}

bounds={name:bounds_of(col,pos) for name,col,pos in placements}
static_checks={}
for name in ('kettle','teabox','kyusu','cup'):
    bb=bounds[name]
    on_surface=abs(bb['min'][2]-service_z)<.002
    within_tray=all(bb['min'][i]>=bounds['tray']['min'][i]-.001 and
        bb['max'][i]<=bounds['tray']['max'][i]+.001 for i in (0,1))
    clear_of_channel=bb['min'][1]>=tray_offset[1]-.075 and bb['max'][1]<=tray_offset[1]+.195
    static_checks[name]={'base_near_surface':on_surface,'footprint_within_tray_outer_bounds':within_tray,
        'within_main_service_zone':clear_of_channel}
    if not clear_of_channel:
        raise RuntimeError('Asset footprint crosses drainage channel or service-zone edge: '+name)
    if not on_surface or not within_tray:
        raise RuntimeError('Staging requires adjustment for '+name+': '+str(static_checks[name]))

def linear(c):
    return [v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in c]

def mat(name,c,roughness):
    m=bpy.data.materials.new(name); m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value=(*linear(c),1)
    bs.inputs['Roughness'].default_value=roughness
    return m

mesh=bpy.data.meshes.new('SETTING_STUDIO_floor_mesh')
mesh.from_pydata([(-20,-20,-.001),(20,-20,-.001),(20,20,-.001),(-20,20,-.001)],[],[(0,1,2,3)])
ground=bpy.data.objects.new('SETTING_STUDIO_floor',mesh); studio.objects.link(ground)
ground.data.materials.append(mat('SETTING_STUDIO | quiet warm floor',(.27,.275,.265),.95))

def aim(ob,target):
    ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()

for name,loc,power,size,colour in [
    ('key',(-1,-1.1,2.2),200,1.2,(1,.90,.78)),
    ('fill',(1.0,-.5,1.65),80,1.0,(.80,.88,1)),
    ('rim',(.2,1.2,1.8),170,1.0,(1,.96,.88)),
]:
    data=bpy.data.lights.new('SETTING_STUDIO_'+name,'AREA')
    data.energy=power; data.shape='DISK'; data.size=size; data.color=colour
    ob=bpy.data.objects.new(data.name,data); studio.objects.link(ob); ob.location=loc
    aim(ob,(0,0,service_z))
world=bpy.data.worlds.new('SETTING_STUDIO_world'); world.use_nodes=True; scene.world=world
hdr=bpy.data.images.load(str(PROJECT/'public/environment/lebombo_1k.hdr'),check_existing=False)
hdr.pack(); hdr.filepath='//../../public/environment/lebombo_1k.hdr'
env=world.node_tree.nodes.new('ShaderNodeTexEnvironment'); env.image=hdr
world.node_tree.links.new(env.outputs['Color'],world.node_tree.nodes['Background'].inputs['Color'])
world.node_tree.nodes['Background'].inputs['Strength'].default_value=.25

data=bpy.data.cameras.new('SETTING_STUDIO_camera'); data.type='ORTHO'
camera=bpy.data.objects.new(data.name,data); studio.objects.link(camera); scene.camera=camera
scene.render.engine='CYCLES'
scene.cycles.device='CPU'; scene.cycles.samples=32; scene.cycles.use_denoising=True
scene.render.threads_mode='FIXED'; scene.render.threads=8
scene.render.resolution_x=1800; scene.render.resolution_y=1280; scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.view_settings.view_transform='AgX'; scene.view_settings.look='AgX - Medium High Contrast'

def render(name,location,target,scale):
    camera.location=location; data.ortho_scale=scale; aim(camera,target)
    scene.render.filepath=str(OUT/'previews'/name)
    bpy.ops.render.render(write_still=True,scene=scene.name)

render('room-setting-wide.png',(1.30,-1.80,1.45),(0,0,.55),2.18)
render('room-setting-tabletop.png',(.70,-1.0,1.40),(0,-.025,service_z+.055),1.12)
# Save in the tabletop composition. Only this scene/dependencies are written;
# previously loaded scenes remain untouched in their original source files.
bpy.data.libraries.write(str(OUTPUT),{scene},path_remap='RELATIVE_ALL',fake_user=True,compress=True)
metadata={'units':'metres','table_surface_world_z':tabletop,'tray_surface_local_z':traytop,
    'service_surface_world_z':service_z,
    'placements':{name:list(pos) for name,col,pos in placements},
    'world_bounds':bounds,'static_checks':static_checks,
    'reserved_lid_rest_centres_tray_xy':{'teabox':[-.110,-.025],'kyusu':[.320,-.025]},
    'status':'Visual scale/composition study; not room architecture or runtime integration.'}
(OUT/'setting-metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
result={'blend':str(OUTPUT),'previews':[str(OUT/'previews'/n) for n in ['room-setting-wide.png','room-setting-tabletop.png']],
    'metadata':metadata}
