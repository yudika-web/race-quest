"""Gate and package the reviewable Batch 1 without touching the cat release."""
from pathlib import Path
import json,hashlib,zipfile,shutil,datetime
D=Path(__file__).resolve().parents[1];ROOT=D.parents[1];HTML=D.parent/'race-quest-pro-batch1.html'
required=['scope-verification.json','glb-validation.json','core-test-results.json','test-results.json','offline-test-results.json','rig-tests.json','preview-race-tests.json','export-tests.json','unchanged-renders.json','camera-verification.json']
reports={name:json.loads((D/name).read_text()) for name in required}
for name,r in reports.items():assert r['status']=='passed',name
assert len(reports['preview-race-tests.json']['cases'])==6
assert len(reports['glb-validation.json']['models'])==6
assert len(reports['rig-tests.json']['models'])==3
assert len(reports['unchanged-renders.json']['checks'])==15
assert all(r['exact'] for r in reports['unchanged-renders.json']['checks'])
assert not reports['preview-race-tests.json']['errors'] and not reports['preview-race-tests.json']['consoleErrors']
assert reports['offline-test-results.json']['offline'] and not reports['offline-test-results.json']['assetHttpRequests']
html=HTML.read_bytes();digest=hashlib.sha256(html).hexdigest();assert len(html)<25000000
assert reports['scope-verification.json']['html_sha256']==digest
metrics=json.loads((D/'asset-metrics.json').read_text());assert metrics['html_bytes']==len(html)
for r in reports['glb-validation.json']['models']:assert r['bytes']==(D/'models'/r['file']).stat().st_size
# Delete only generated backups/caches from this stage, never user source files.
for p in (D/'source').glob('*.blend1'):p.unlink()
cache=D/'source/__pycache__'
if cache.exists():shutil.rmtree(cache)
validation={'status':'passed','validated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline_commit':reports['scope-verification.json']['baseline_commit'],'branch':'dev/race-quest-cat-sport-visual-upgrade','html_bytes':len(html),'html_sha256':digest,'completed_this_batch':3,'cat_unchanged':True,'pending_pairs':10,'checks':{name:{'status':r['status'],'case_count':len(r.get('cases',[])),'check_count':len(r.get('checks',[]))} for name,r in reports.items()},'artifacts':{}}
for p in [HTML,*sorted((D/'models').glob('*.glb')),*sorted((D/'source').glob('*.blend'))]:validation['artifacts'][str(p.relative_to(ROOT))]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(D/'delivery-validation.json').write_text(json.dumps(validation,indent=2))
checks={str(HTML.relative_to(ROOT)):digest}
for p in sorted(D.rglob('*')):
 if p.is_file() and p.name!='SHA256SUMS.json':checks[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
(D/'SHA256SUMS.json').write_text(json.dumps(checks,indent=2))
playable=ROOT/'race-quest-pro-batch1-playable.zip'
with zipfile.ZipFile(playable,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 z.writestr('RACE-QUEST-PRO-Batch-1.html',html)
 z.writestr('README.txt','Ekstrak ZIP lalu buka RACE-QUEST-PRO-Batch-1.html. Semua aset tertanam; tidak memerlukan internet. Pilih Pinguin, Beruang, atau Kelinci di garasi. Mobil + Karakter / Close-up tersedia, geser untuk rotasi dan scroll/pinch untuk zoom. Ekspresi Ramah/Senang/Terkejut tersedia untuk tiga karakter baru.\n')
 z.writestr('SHA256.txt',digest+'  RACE-QUEST-PRO-Batch-1.html\n')
with zipfile.ZipFile(playable) as z:assert z.read('RACE-QUEST-PRO-Batch-1.html')==html;assert z.testzip() is None
archive=ROOT/'race-quest-pro-batch1-review.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 z.write(HTML,HTML.relative_to(ROOT))
 for p in sorted(D.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(ROOT))
 z.writestr('README.txt','Buka visual-upgrade/race-quest-pro-batch1.html untuk bermain offline. Model GLB, tiga Blender, script modular dan screenshot berada di visual-upgrade/batch1/. Lihat README.md di folder itu untuk data uji dan batas pengujian. Untuk rebuild/integrasi HTML gunakan checkout repository yudika-web/race-quest agar template Kucing dan riwayat baseline tersedia; arsip ini tidak menggandakan HTML template lama. Tidak ada merge main atau deployment Pages.\n')
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
assert archive.stat().st_size<100000000,'Review archive exceeds GitHub single-file limit'
for name,h in checks.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h,name
print(json.dumps({'status':'passed','verified_files':len(checks),'html_bytes':len(html),'playable_zip_bytes':playable.stat().st_size,'review_zip_bytes':archive.stat().st_size,'html_sha256':digest,'baseline_cat_release_untouched':True}))
