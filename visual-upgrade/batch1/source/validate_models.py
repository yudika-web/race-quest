"""Native Blender import and binary/rig validation of six delivered GLBs."""
import bpy,json,struct,math,pathlib
D=pathlib.Path(__file__).resolve().parents[1]
def decode(path):
 b=path.read_bytes();n=struct.unpack_from('<I',b,12)[0];return b,json.loads(b[20:20+n]),28+n

def inspect(path):
 b,g,start=decode(path);result={'file':path.name,'bytes':len(b),'normals':0,'color_vertices':0,'triangles':0}
 for m in g['meshes']:
  for p in m['primitives']:
   for name in ['POSITION','NORMAL','COLOR_0']:
    a=g['accessors'][p['attributes'][name]];v=g['bufferViews'][a['bufferView']];values=struct.unpack_from('<'+'f'*a['count']*3,b,start+v.get('byteOffset',0)+a.get('byteOffset',0));assert all(math.isfinite(x) for x in values),(path.name,m['name'],name)
    if name=='NORMAL':
     assert all(abs(math.sqrt(sum(x*x for x in values[i:i+3]))-1)<.0001 for i in range(0,len(values),3)),(path.name,m['name'],'Non-unit normal');result['normals']+=a['count']
    if name=='COLOR_0':assert all(0<=x<=1 for x in values);result['color_vertices']+=a['count']
   ia=g['accessors'][p['indices']];iv=g['bufferViews'][ia['bufferView']];indices=struct.unpack_from('<'+'H'*ia['count'],b,start+iv.get('byteOffset',0));assert max(indices)<g['accessors'][p['attributes']['POSITION']]['count'];result['triangles']+=len(indices)//3
 # Preserve all original named pivots/translations; newly added facial and pose pivots are additional.
 _,old,_=decode(D/'before/models'/('kart_'+path.name.split('_')[1].split('.')[0]+'.glb'))
 nodes={n['name']:n for n in g['nodes']}
 def parents(doc):return {doc['nodes'][j]['name']:n['name'] for n in doc['nodes'] for j in n.get('children',[])}
 old_parents,new_parents=parents(old),parents(g)
 for node in old['nodes']:
  if 'mesh' not in node:
   assert old_parents.get(node['name'])==new_parents.get(node['name']),('Parent changed',node['name'])
   assert node['name'] in nodes,node['name'];assert node.get('translation',[0,0,0])==nodes[node['name']].get('translation',[0,0,0]),node['name']
 for key in ['collider','wheelbase','trackWidth','steerAxis','spinAxis']:
  assert old['nodes'][0]['extras'][key]==g['nodes'][0]['extras'][key],key
 for node in g['nodes']:
  if node['name'] in ['eyes_happy','mouth_happy','mouth_shock']:assert node.get('scale')==[0,0,0],('Default expression visibility',node['name'])
 result['default_standard_gltf_expression']='normal'
 assert g['extras']['triangles']==result['triangles']
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False);bpy.ops.import_scene.gltf(filepath=str(path))
 variants=[o for o in bpy.context.scene.objects if o.name.startswith(('eyes_happy','mouth_happy','mouth_shock'))]
 assert variants and all(o.matrix_world.to_scale().length<.000001 for o in variants),'Native viewer does not hide inactive expressions'
 result['native_import_hides_inactive_expressions']=True
 result['imported_meshes']=len([o for o in bpy.context.scene.objects if o.type=='MESH']);result['original_rig_pivots_and_collider_preserved']=True
 return result
results=[inspect(p) for p in sorted((D/'models').glob('*.glb'))];assert len(results)==6
(D/'glb-validation.json').write_text(json.dumps({'status':'passed','models':results},indent=2));print(json.dumps(results))
