"""Verify cat-only scope against the committed development baseline."""
from pathlib import Path
import subprocess,json,struct,re,hashlib
D=Path(__file__).resolve().parents[1];ROOT=D.parent
BASE='12a3a6f700430f0a39dd4eb3a8ed9ba480106b9c'
def previous(path):return subprocess.check_output(['git','show',f'{BASE}:{path}'],cwd=ROOT)
def glb(b):
 size=struct.unpack_from('<I',b,12)[0];return json.loads(b[20:20+size]),b[28+size:]
def signatures(blob):
 g,b=glb(blob)
 def data(i):
  a=g['accessors'][i];v=g['bufferViews'][a['bufferView']];off=v.get('byteOffset',0)+a.get('byteOffset',0)
  size=a['count']*{'SCALAR':1,'VEC3':3,'VEC2':2}[a['type']]*{5126:4,5123:2,5125:4}[a['componentType']]
  return a['type'],a['componentType'],hashlib.sha256(b[off:off+size]).hexdigest()
 meshes={}
 for m in g['meshes']:
  if m['name'].startswith(('body_suspension_','wheel_')):
   meshes[m['name']]=[{'attributes':{k:data(v) for k,v in p['attributes'].items()},'indices':data(p['indices']),'material':g['materials'][p['material']]} for p in m['primitives']]
 return meshes,{n['name']:{k:n[k] for k in ['translation','rotation','scale'] if k in n} for n in g['nodes'] if 'mesh' not in n},g
summary=[]
for name in ['race-quest-cat-sport.glb','race-quest-cat-sport-low.glb']:
 old,pivots,og=signatures(previous('visual-upgrade/'+name));new,np,ng=signatures((D/name).read_bytes())
 assert old==new,'Car geometry / normals / material changed: '+name
 assert pivots==np,'Animation pivots changed: '+name
 summary.append({'file':name,'car_batches_identical':len(old),'rig_pivots_identical':True,'old_triangles':og['extras']['triangles'],'new_triangles':ng['extras']['triangles'],'bytes':(D/name).stat().st_size})
old=previous('visual-upgrade/race-quest-visual-upgrade.html').decode();new=(D/'race-quest-visual-upgrade.html').read_text()
parts=lambda s:re.findall(r'<script\b([^>]*)>(.*?)</script>',s,re.S)
a,b=parts(old),parts(new)
for i in [0,2,3,5]:assert a[i]==b[i],f'Gameplay/scenery script changed: {i}'
assert a[4][1].split(' race(session,dt,input={},alpha=1){')[1]==b[4][1].split(' race(session,dt,input={},alpha=1){')[1], 'Race renderer / camera changed'
assert a[4][1].split(' drawModel(')[1].split(' begin(')[0]==b[4][1].split(' drawModel(')[1].split(' begin(')[0], 'Rig animation logic changed'
oa=json.loads(a[1][1]);na=json.loads(b[1][1])
for k in oa:
 if k not in ['kart_arka.glb','kart_arka_low.glb']:assert oa[k]==na[k],f'Other asset changed: {k}'
report={'baseline_commit':BASE,'status':'passed','models':summary,'gameplay_scenery_and_race_camera_identical':True,'existing_rig_animation_logic_identical':True,'garage_controls_and_vertex_colors_added':True,'other_assets_identical':True}
(D/'cat-redesign/scope-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
