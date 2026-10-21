from pathlib import Path
import json,hashlib,zipfile,subprocess,sys
D=Path(__file__).resolve().parents[2];B=D/'stage12-kayong-utara';R=D.parent;H=D/'blokraya-stage12-kayong-utara.html'
subprocess.run([sys.executable,str(B/'source/report.py')],check=True)
read=lambda n:json.loads((B/(n+'.json')).read_text());reports={n:read(n)for n in ['multilap-tests','clearance-tests','physics-tests','item-tests','world-tests','browser-tests','offline-tests','unchanged-renders','scope-tests','comparison-report','release-smoke','render-mechanics-tests','mechanics-tests','rescue-browser-tests','grand-prix-tests','grand-prix-browser-tests']}
for n,r in reports.items():assert r['status']=='passed',n
raw=H.read_bytes();sha=lambda x:hashlib.sha256(x).hexdigest();metrics=read('asset-metrics');assert sha(raw)==metrics['html_sha256'];assert reports['release-smoke']['html_sha256']==sha(raw);assert raw==Path('/tmp/blokraya-6i/candidate.html').read_bytes()
metrics.update({'under_25_decimal_MB':len(raw)<25000000,'reports':{n:len(r.get('checks',[]))for n,r in reports.items()},'teacher_export_bytes':reports['offline-tests']['export_bytes'],'offline_asset_HTTP_requests':len(reports['offline-tests']['assetRequests']),'direct_file_note':read('direct-file-tests').get('reason'),'release_status':'Ready for visual review; reference accuracy and direct file navigation have documented limitations.'})
notes=(B/'MULAI.txt').read_text()

for kind in ['playable','review']:
 dest=R/f'blokraya-stage12-kayong-utara-{kind}.zip'
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
  z.write(H,H.name);z.writestr('MULAI.txt',notes)
  if kind=='review':
   for f in sorted(B.rglob('*')):
    if f.is_file()and '__pycache__'not in f.parts and f.name!='release-metrics.json':z.write(f,'stage12-kayong-utara/'+f.relative_to(B).as_posix())
   z.writestr('stage12-kayong-utara/release-metrics.json',json.dumps({**metrics,'review_self_hash_omitted':True,'review_self_hash_note':'The full review ZIP hash lives in the repository release-metrics.json; an archive cannot contain its own final hash.'},indent=2))
 with zipfile.ZipFile(dest)as z:assert z.testzip()is None;assert z.read(H.name)==raw;entries=len(z.namelist())
 metrics[kind+'_zip']={'file':dest.name,'bytes':dest.stat().st_size,'sha256':sha(dest.read_bytes()),'crc_ok':True,'html_identical':True,'entries':entries}
(B/'release-metrics.json').write_text(json.dumps(metrics,indent=2));print(json.dumps({k:metrics[k]for k in ['html_bytes','growth_bytes','html_sha256','playable_zip','review_zip']},indent=2))
