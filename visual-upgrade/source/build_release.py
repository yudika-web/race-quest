"""Package the reviewed current HTML, source, models and actual render comparisons."""
from pathlib import Path
import json,hashlib,zipfile,shutil,subprocess,datetime
D=Path(__file__).resolve().parents[1];ROOT=D.parent
required=['test-results.json','core-test-results.json','offline-test-results.json','cat-blocky/scope-verification.json','cat-blocky/preview-tests.json','cat-blocky/animation-tests.json','cat-blocky/unchanged-renders.json','cat-blocky/export-tests.json','cat-blocky/camera-verification.json','cat-blocky/turnaround-cameras.json']
for name in required:
 assert json.loads((D/name).read_text())['status']=='passed',name
assert all(x['unit_normals_checked']>0 and x['color_vertices_checked']>0 for x in json.loads((D/'glb-validation.json').read_text()))
# Remove generated files from this build, keeping editable .blend and all history.
cache=D/'source/__pycache__'
if cache.exists():shutil.rmtree(cache)
for p in (D/'source').glob('*.blend1'):p.unlink()
html=(D/'race-quest-visual-upgrade.html').read_bytes();assert (ROOT/'index.html').read_bytes()==(D/'original.html').read_bytes()
assert (ROOT/'index.html').read_bytes()==subprocess.check_output(['git','show','b38224e148b7427011ed02a4b8f6a2234be7c0cf:index.html'],cwd=ROOT)
validation={'status':'passed','validated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'html_sha256':hashlib.sha256(html).hexdigest(),'original_main_index_unchanged':True,'artifacts':{},'checks':{}}
for name in ['race-quest-visual-upgrade.html','race-quest-cat-sport.glb','race-quest-cat-sport-low.glb','source/race-quest-cat-sport.blend','cat-blocky/avatar.webp']:
 data=(D/name).read_bytes();validation['artifacts'][name]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
for name in required:
 report=json.loads((D/name).read_text());validation['checks'][name]={'status':report['status'],'check_count':len(report.get('checks',[]))}
for item in json.loads((D/'glb-validation.json').read_text()):assert item['bytes']==(D/item['file']).stat().st_size
(D/'cat-blocky/delivery-validation.json').write_text(json.dumps(validation,indent=2))
playable=ROOT/'race-quest-playable.zip'
with zipfile.ZipFile(playable,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 z.writestr('RACE-QUEST-Kucing-Blocky.html',html)
 z.writestr('README.txt','Ekstrak ZIP lalu buka RACE-QUEST-Kucing-Blocky.html di browser. Semua aset tertanam. Garasi menyediakan Mobil + Karakter dan Close-up Karakter; geser untuk memutar, scroll atau pinch untuk zoom.\n')
 z.writestr('SHA256.txt',hashlib.sha256(html).hexdigest()+'  RACE-QUEST-Kucing-Blocky.html\n')
with zipfile.ZipFile(playable) as z:assert z.read('RACE-QUEST-Kucing-Blocky.html')==html
# Copies outside the repository provide short local filenames as well.
Path('/workspace/RACE-QUEST-Kucing-Blocky.html').write_bytes(html);shutil.copyfile(playable,'/workspace/RACE-QUEST-Kucing.zip')
checks={str(p.relative_to(D)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(D.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.json'}
(D/'SHA256SUMS.json').write_text(json.dumps(checks,indent=2))
archive=ROOT/'race-quest-visual-upgrade.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(D.rglob('*')):
  if p.is_file():z.write(p,Path('race-quest-visual-upgrade')/p.relative_to(D))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
for name,h in checks.items():assert hashlib.sha256((D/name).read_bytes()).hexdigest()==h,name
print(json.dumps({'verified_artifacts':len(checks),'html_bytes':len(html),'playable_zip_bytes':playable.stat().st_size,'complete_zip_bytes':archive.stat().st_size,'original_unchanged':True}))
