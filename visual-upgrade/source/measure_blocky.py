"""Measure the delivered assets against the exact previous development commit."""
from pathlib import Path
import json,struct,subprocess,hashlib
D=Path(__file__).resolve().parents[1];BASE='276792553e913520119038cac5c9512035751d86'
def previous(name):return subprocess.check_output(['git','show',BASE+':visual-upgrade/'+name],cwd=D.parent)
def model(blob):
 n=struct.unpack_from('<I',blob,12)[0];g=json.loads(blob[20:20+n]);counts={'car_triangles':0,'cat_triangles':0}
 for m in g['meshes']:
  k='car_triangles' if m['name'].startswith(('body_suspension_','wheel_')) else 'cat_triangles'
  counts[k]+=sum(g['accessors'][p['indices']]['count']//3 for p in m['primitives'])
 return {'bytes':len(blob),'total_triangles':sum(counts.values()),'material_batches':len(g['meshes']),**counts}
report={'baseline_commit':BASE,'before':{},'after':{}}
for key,name in [('high','race-quest-cat-sport.glb'),('low','race-quest-cat-sport-low.glb')]:
 report['before'][key]=model(previous(name));report['after'][key]=model((D/name).read_bytes())
for stage,data in [('before',previous('race-quest-visual-upgrade.html')),('after',(D/'race-quest-visual-upgrade.html').read_bytes())]:report[stage]['html_bytes']=len(data)
report['html_change_percent']=round((report['after']['html_bytes']/report['before']['html_bytes']-1)*100,2)
report['cat_triangle_reduction_percent']=round((1-report['after']['high']['cat_triangles']/report['before']['high']['cat_triangles'])*100,2)
report['html_sha256']=hashlib.sha256((D/'race-quest-visual-upgrade.html').read_bytes()).hexdigest()
(D/'cat-blocky/metrics.json').write_text(json.dumps(report,indent=2))
metrics=json.loads((D/'asset-metrics.json').read_text());metrics['previous_organic_redesign_stage']={k:metrics[k] for k in ['revised_html_bytes','new_high_glb_bytes','new_low_glb_bytes','new_high_triangles','new_low_triangles','refined_cat_high_triangles','refined_cat_low_triangles','new_draw_batches']}
metrics.update(revised_html_bytes=report['after']['html_bytes'],growth_percent=round((report['after']['html_bytes']/metrics['original_html_bytes']-1)*100,2),new_high_glb_bytes=report['after']['high']['bytes'],new_low_glb_bytes=report['after']['low']['bytes'],new_high_triangles=report['after']['high']['total_triangles'],new_low_triangles=report['after']['low']['total_triangles'],new_draw_batches=report['after']['high']['material_batches'],refined_cat_high_triangles=report['after']['high']['cat_triangles'],refined_cat_low_triangles=report['after']['low']['cat_triangles'],current_stage='blocky chibi rebuild',blocky_baseline_commit=BASE,blocky_html_change_percent=report['html_change_percent'],blocky_cat_triangle_reduction_percent=report['cat_triangle_reduction_percent'])
# Preserve the original historical measurements across repeated measurement.
old=json.loads(subprocess.check_output(['git','show',BASE+':visual-upgrade/asset-metrics.json'],cwd=D.parent))
metrics['previous_organic_redesign_stage']={k:old[k] for k in metrics['previous_organic_redesign_stage']}
(D/'asset-metrics.json').write_text(json.dumps(metrics,indent=2));print(json.dumps(report,indent=2))
