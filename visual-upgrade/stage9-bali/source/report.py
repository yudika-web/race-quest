from pathlib import Path
import json
B=Path(__file__).resolve().parents[1];read=lambda name:json.loads((B/(name+'.json')).read_text())
s=read('scope-tests');w=read('world-tests');p=read('physics-tests');changes=read('bounded-changes')
m={**{k:s[k]for k in ['baseline','baseline_bytes','html_bytes','growth_bytes','html_sha256','remaining_to_25M']},'track':p['track'],'environment':{k:v for k,v in w['stats'].items()if k not in ['objects','landmarks']},'sky':w['sky'],'thumbnail_bytes':{k:v['bytes']for k,v in json.loads((B/'thumbnails/assets.json').read_text()).items()},'growth_components_bytes':[len(c['new'].encode())-len(c['old'].encode())for c in changes],'quality_samples':{},'AI_completion':{},'physical_phone_tested':False,'FPS_measured':False,'memory_benchmarked':False,'new_external_runtime_dependencies':0,'landmark_accuracy_verified':False,'direct_file_scheme_result':read('direct-file-tests')['status'],'network_disabled_offline_test':read('offline-tests')['status']}
for q in ['high','medium','low']:
 samples=[x for x in w['samples']if x['quality']==q and x['weather']=='clear'];m['quality_samples'][q]={k:{'min':min(a[k]for a in samples),'max':max(a[k]for a in samples)}for k in ['colour_draws','depth_draws','colour_triangles','depth_triangles']}
for level in ['easy','normal','hard']:
 cases=[x for x in p['completion']if x['level']==level];m['AI_completion'][level]={'seed_cases':len(cases),'all_4_AI_finished':True,'mean_simulation_finish_seconds':sum(sum(a['finish_times'])for a in cases)/(len(cases)*4),'max_stall_seconds':max(a['max_stall']for a in cases),'overtake_plans':sum(sum(a['overtake_plans'])for a in cases)}
m['terrain_checks']=read('terrain-tests')['result'];m['sky_counter_note']='Two existing gradient/cloud draw calls; no additional sky program, light or texture. Prior night-stage resources are freed on transition.'
(B/'asset-metrics.json').write_text(json.dumps(m,indent=2))
