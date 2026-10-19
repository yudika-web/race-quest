"""Measure actual file sizes, meshes, bounds and frozen-camera comparison data."""
from pathlib import Path
import json,struct,hashlib
D=Path(__file__).resolve().parents[1];ROOT=D.parent

def model(file):
 b=file.read_bytes();n=struct.unpack_from('<I',b,12)[0];g=json.loads(b[20:20+n]);parents={j:i for i,node in enumerate(g['nodes']) for j in node.get('children',[])}
 def absolute(i):
  own=g['nodes'][i].get('translation',[0,0,0]);p=absolute(parents[i]) if i in parents else [0,0,0];return [own[k]+p[k] for k in range(3)]
 def driver(i):return g['nodes'][i]['name']=='driver' or (i in parents and driver(parents[i]))
 stats={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'stored_triangles':0,'car_triangles':0,'character_triangles':0,'material_batches':len(g['meshes']),'embedded_textures':len(g.get('images',[])),'car_bounds':{'min':[float('inf')]*3,'max':[-float('inf')]*3},'character_bounds':{'min':[float('inf')]*3,'max':[-float('inf')]*3}}
 for i,node in enumerate(g['nodes']):
  if 'mesh' not in node:continue
  char=driver(i);t=absolute(i);target=stats['character_bounds' if char else 'car_bounds']
  for p in g['meshes'][node['mesh']]['primitives']:
   count=g['accessors'][p['indices']]['count']//3;stats['stored_triangles']+=count;stats['character_triangles' if char else 'car_triangles']+=count;a=g['accessors'][p['attributes']['POSITION']]
   for k in range(3):target['min'][k]=min(target['min'][k],a['min'][k]+t[k]);target['max'][k]=max(target['max'][k],a['max'][k]+t[k])
 return stats
rigs={r['id']:r for r in json.loads((D/'rig-tests.json').read_text())['models']}
report={'baseline_commit':json.loads((D/'baseline.json').read_text())['baseline_commit'],'baseline_html_bytes':(ROOT/'race-quest-visual-upgrade.html').stat().st_size,'html_bytes':(ROOT/'race-quest-pro-batch1.html').stat().st_size,'html_target_decimal_bytes':25000000,'models':[]}
for id,name,vehicle in [('nara','Pinguin','Kapsul'),('bimo','Beruang','Buggy'),('sora','Kelinci','Formula')]:
 row={'id':id,'name':name,'vehicle':vehicle,'before':model(D/'before/models'/('kart_'+id+'.glb')),'high':model(D/'models'/('kart_'+id+'.glb')),'low':model(D/'models'/('kart_'+id+'_low.glb')),'blender_bytes':(D/'source'/('race-quest-'+id+'.blend')).stat().st_size,'visible_normal_high_triangles':rigs[id]['visible_high_triangles'],'visible_normal_low_triangles':rigs[id]['visible_low_triangles'],'visible_normal_draw_calls':rigs[id]['visible_high_draw_calls']}
 report['models'].append(row)
report['html_growth_percent']=round((report['html_bytes']/report['baseline_html_bytes']-1)*100,2);report['under_25_MB']=report['html_bytes']<25000000
assert report['under_25_MB'];(D/'asset-metrics.json').write_text(json.dumps(report,indent=2));print(json.dumps({'html_bytes':report['html_bytes'],'under_25_MB':report['under_25_MB'],'models':[{k:r[k] for k in ['id','visible_normal_high_triangles','visible_normal_low_triangles','visible_normal_draw_calls']} for r in report['models']]},indent=2))
