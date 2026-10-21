from pathlib import Path
import json,hashlib,zipfile,html
D=Path(__file__).resolve().parents[1];V=D.parent;R=V.parent;H=V/'blokraya-patch8f-economy.html';B=V/'blokraya-patch8e-startup.html'
sha=lambda b:hashlib.sha256(b).hexdigest()
checks={}
for file in ['unit-results.json','browser-results.json','edge-results.json','visual-results.json','flow-tests.json']:
 r=json.loads((D/file).read_text());assert r.get('status','passed')=='passed';checks[file]=r.get('passed',len(r.get('checks',[])))
assert json.loads((D/'scope-results.json').read_text())['passed']
m={'baseline_commit':'34b9defab52e2b992235f24ce8162e411f6833cd','html_bytes':H.stat().st_size,'growth_bytes':H.stat().st_size-B.stat().st_size,'html_sha256':sha(H.read_bytes()),'named_test_groups':sum(checks.values())+1,'test_groups':checks,'scope_passed':True,'screenshots':len(list((D/'screenshots').glob('*.png'))),'new_external_assets':0,'physical_mobile_tested':False,'full_stage_benchmark_repeated':False}
(D/'metrics.json').write_text(json.dumps(m,indent=2))
images=''.join('<figure><a href="screenshots/'+p.name+'"><img loading="lazy" src="screenshots/'+p.name+'"></a><figcaption>'+html.escape(p.stem)+'</figcaption></figure>'for p in sorted((D/'screenshots').glob('*.png')))
(D/'review.html').write_text('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BlokRaya PATCH 8F review</title><style>body{background:#102036;color:#fff;font:16px system-ui;margin:24px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}figure{margin:0}img{width:100%;height:310px;object-fit:contain;background:#081320}a{color:#70d9ff}</style><h1>PATCH 8F — Token dan unlock</h1><p>Screenshot asli browser/game. Fixture pengujian tidak ditanam dalam HTML distribusi. <a href="README.md">Laporan</a></p><main>'+images+'</main>')
for kind in ['playable','review']:
 dest=R/f'blokraya-patch8f-{kind}.zip'
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
  z.write(D/'MULAI.txt','MULAI.txt');z.write(H,H.name if kind=='playable'else 'visual-upgrade/'+H.name)
  if kind=='review':
   z.write(B,'visual-upgrade/'+B.name)
   for f in sorted(D.rglob('*')):
    if f.is_file()and '__pycache__'not in f.parts and f.name!='release-metrics.json':z.write(f,'visual-upgrade/patch8f/'+f.relative_to(D).as_posix())
 with zipfile.ZipFile(dest)as z:assert z.testzip()is None;assert z.read(H.name if kind=='playable'else'visual-upgrade/'+H.name)==H.read_bytes()
 m[kind+'_zip']={'file':dest.name,'bytes':dest.stat().st_size,'sha256':sha(dest.read_bytes()),'CRC_OK':True}
(D/'release-metrics.json').write_text(json.dumps(m,indent=2));print(json.dumps(m,indent=2))
