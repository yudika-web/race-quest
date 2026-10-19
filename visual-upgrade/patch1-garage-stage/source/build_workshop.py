"""Editable export of actual runtime geometry. Run Blender --background --python thisfile.
Runtime asset remains lightweight shared CityBatch meshes; GLB is a standalone review asset.
"""
import bpy,json
from pathlib import Path
D=Path(__file__).resolve().parents[1];data=json.loads((D/'assets/workshop-geometry.json').read_text())
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
# Game uses Y up, Blender Z up. Keep right-handed conversion (x,-z,y).
materials={}
for key,m in data['materials'].items():
 mat=bpy.data.materials.new(key);mat.use_nodes=True;p=mat.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*m['color'][:3],1);p.inputs['Roughness'].default_value=m['rough'];p.inputs['Metallic'].default_value=m['metal']
 if m['emissive']:
  p.inputs['Emission Color'].default_value=(*m['emissive'],1);p.inputs['Emission Strength'].default_value=.5
 materials[key]=mat
banner=materials['banner'];n=banner.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(D/'assets/workshop-banner.png'));n.image.pack();banner.node_tree.links.new(n.outputs['Color'],banner.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
def mesh(name,g,mat):
 me=bpy.data.meshes.new(name);me.from_pydata([(x,-z,y)for x,y,z in g['V']],[],g['F']);me.update();ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);me.materials.append(mat)
 if len(g.get('UV',[]))==len(g['V']):
  uv=me.uv_layers.new();
  for f in me.polygons:
   for li in f.loop_indices:
    u,v=g['UV'][me.loops[li].vertex_index];uv.data[li].uv=(u,1-v)
 return ob
for key,g in data['groups'].items():mesh('workshop_'+key,g,materials[key])
for i,g in enumerate(data['banners']):mesh('race_quest_banner_'+str(i),g,banner)
bpy.ops.wm.save_as_mainfile(filepath=str(D/'assets/workshop.blend'))
bpy.ops.export_scene.gltf(filepath=str(D/'assets/workshop.glb'),export_format='GLB',export_yup=True)
print('Exported exact runtime workshop meshes:',sum(len(g['F'])for g in data['groups'].values())+4,'triangles')
