"""Package the reviewed current HTML, source, models and actual render comparisons."""
from pathlib import Path
import json,hashlib,zipfile,shutil
D=Path(__file__).resolve().parents[1];ROOT=D.parent
for name in ['test-results.json','core-test-results.json','offline-test-results.json','cat-redesign/scope-verification.json','cat-redesign/preview-tests.json','cat-redesign/animation-tests.json','cat-redesign/unchanged-renders.json','cat-redesign/export-tests.json','cat-redesign/camera-verification.json']:
 assert json.loads((D/name).read_text())['status']=='passed',name
assert all(x['unit_normals_checked']>0 and x['color_vertices_checked']>0 for x in json.loads((D/'glb-validation.json').read_text()))
# Remove generated files from this build, keeping editable .blend and all history.
cache=D/'source/__pycache__'
if cache.exists():shutil.rmtree(cache)
for p in (D/'source').glob('*.blend1'):p.unlink()
html=(D/'race-quest-visual-upgrade.html').read_bytes();assert (ROOT/'index.html').read_bytes()==(D/'original.html').read_bytes()
playable=ROOT/'race-quest-playable.zip'
with zipfile.ZipFile(playable,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 z.writestr('RACE-QUEST-Kucing.html',html)
 z.writestr('README.txt','Ekstrak ZIP lalu buka RACE-QUEST-Kucing.html di browser. Semua aset tertanam. Garasi menyediakan Mobil + Karakter dan Close-up Karakter; geser untuk memutar, scroll atau pinch untuk zoom.\n')
 z.writestr('SHA256.txt',hashlib.sha256(html).hexdigest()+'  RACE-QUEST-Kucing.html\n')
with zipfile.ZipFile(playable) as z:assert z.read('RACE-QUEST-Kucing.html')==html
# Copies outside the repository provide short local filenames as well.
Path('/workspace/RACE-QUEST-Kucing.html').write_bytes(html);shutil.copyfile(playable,'/workspace/RACE-QUEST-Kucing.zip')
checks={str(p.relative_to(D)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(D.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.json'}
(D/'SHA256SUMS.json').write_text(json.dumps(checks,indent=2))
archive=ROOT/'race-quest-visual-upgrade.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(D.rglob('*')):
  if p.is_file():z.write(p,Path('race-quest-visual-upgrade')/p.relative_to(D))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
for name,h in checks.items():assert hashlib.sha256((D/name).read_bytes()).hexdigest()==h,name
print(json.dumps({'verified_artifacts':len(checks),'html_bytes':len(html),'playable_zip_bytes':playable.stat().st_size,'complete_zip_bytes':archive.stat().st_size,'original_unchanged':True}))
