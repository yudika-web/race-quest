from pathlib import Path
import re,json,hashlib,subprocess
D=Path(__file__).resolve().parents[2];B=D/'stage4-sambas';baseline='346c915ca0272f6b10732fdd99fe28bcde87fb62';old=(D/'blokraya-patch5.html').read_text();new=Path('/tmp/blokraya-6a/candidate.html').read_text();changes=json.loads((B/'bounded-changes.json').read_text());restore=new
for c in reversed(changes):
 assert restore.count(c['new'])==c['count'];restore=restore.replace(c['new'],c['old'])
assert restore==old
blocks=lambda s:{m[0]:m[1] for m in re.findall(r'<script id="([^"]+)"[^>]*>(.*?)</script>',s,re.S)}
a,b=blocks(old),blocks(new);hashes=[]
for key in a:
 if key in ['patch1StageCatalog','patch1StageAssets']:continue
 assert a[key]==b[key],key;hashes.append({'id':key,'sha256':hashlib.sha256(a[key].encode()).hexdigest()})
oldmeta=json.loads(a['patch1StageCatalog']);meta=json.loads(b['patch1StageCatalog']);assert all(x==y for x,y in zip(oldmeta,meta)if x['id']!='sambas');assert sum(x['available']for x in meta)==4
oldassets=json.loads(a['patch1StageAssets']);assets=json.loads(b['patch1StageAssets']);assert all(assets[k]==v for k,v in oldassets.items());assert len(assets)==len(oldassets)+2
tracked=subprocess.check_output(['git','ls-tree','-r','--name-only',baseline,'--','visual-upgrade','index.html'],cwd=D.parent).decode().splitlines()
for file in tracked:
 p=D.parent/file;assert p.read_bytes()==subprocess.check_output(['git','show',baseline+':'+file],cwd=D.parent),file
report={'status':'passed','baseline':baseline,'baseline_bytes':len(old.encode()),'html_bytes':len(new.encode()),'growth_bytes':len(new.encode())-len(old.encode()),'html_sha256':hashlib.sha256(new.encode()).hexdigest(),'remaining_to_25M':25000000-len(new.encode()),'reverse_assembly_exact':True,'historical_files_unchanged':len(tracked),'protected_script_payloads':hashes,'protected_old_thumbnails':len(oldassets),'new_rendered_thumbnails':2,'original_core_renderer_scenery_source_unchanged':True,'other_stage_metadata_identical':True,'new_runtime_track_id':'sambas'}
assert report['remaining_to_25M']>0
(B/'scope-tests.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items()if k!='protected_script_payloads'},indent=2))
