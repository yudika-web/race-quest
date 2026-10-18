"""Run with Blender Python; re-import both delivered GLBs and check normal data."""
import bpy,json,pathlib,struct,math
D=pathlib.Path(__file__).resolve().parents[1];results=[]
for name in ['race-quest-cat-sport.glb','race-quest-cat-sport-low.glb']:
 b=(D/name).read_bytes();size=struct.unpack_from('<I',b,12)[0];g=json.loads(b[20:20+size]);start=28+size
 normals=0;colors=0
 for m in g['meshes']:
  for p in m['primitives']:
   a=g['accessors'][p['attributes']['NORMAL']];v=g['bufferViews'][a['bufferView']]
   values=struct.unpack_from('<'+'f'*a['count']*3,b,start+v.get('byteOffset',0)+a.get('byteOffset',0))
   for i in range(0,len(values),3):
    length=math.sqrt(sum(x*x for x in values[i:i+3]));assert math.isfinite(length) and abs(length-1)<.0001,(name,m['name'],i,length)
   normals+=a['count']
   if 'COLOR_0' in p['attributes']:
    ca=g['accessors'][p['attributes']['COLOR_0']];cv=g['bufferViews'][ca['bufferView']];values=struct.unpack_from('<'+'f'*ca['count']*3,b,start+cv.get('byteOffset',0));assert all(math.isfinite(x) and 0<=x<=1 for x in values);colors+=ca['count']
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 bpy.ops.import_scene.gltf(filepath=str(D/name))
 results.append({'file':name,'meshes':len([o for o in bpy.context.scene.objects if o.type=='MESH']),'root':any(o.name=='root' for o in bpy.context.scene.objects),'unit_normals_checked':normals,'color_vertices_checked':colors,'bytes':len(b)})
(D/'glb-validation.json').write_text(json.dumps(results,indent=2));print(json.dumps(results))
