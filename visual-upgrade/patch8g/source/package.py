from pathlib import Path
import json,hashlib,zipfile,html
D=Path(__file__).resolve().parents[1];V=D.parent;R=V.parent;H=V/'blokraya-patch8g-ui-polish.html';B=V/'blokraya-patch8f-economy.html';sha=lambda b:hashlib.sha256(b).hexdigest()
checks={}
for file in ['unit-results.json','ui-results.json','flow-tests.json','purchase-ui-results.json']:
 r=json.loads((D/file).read_text());assert r.get('status','passed')=='passed';checks[file]=r.get('passed',len(r.get('checks',[])))
assert json.loads((D/'scope-results.json').read_text())['passed']
u=json.loads((D/'ui-results.json').read_text());assert not any(x['clipped'] for x in u['textAudits']);assert all(x['bodyHorizontal']<=1 and x['pageHorizontal']<=1 and x['maxSettledShift']<1 for x in u['measurements']);m={'baseline_commit':'0616727a46b6894d041f3604b1345b7f64d27129','html_bytes':H.stat().st_size,'growth_bytes':H.stat().st_size-B.stat().st_size,'growth_percent':round((H.stat().st_size/B.stat().st_size-1)*100,5),'html_sha256':sha(H.read_bytes()),'named_checks':sum(checks.values())+1,'checks':checks,'scope_passed':True,'protected_scripts':56,'screenshots':len(list((D/'screenshots').glob('*.png'))),'viewports':[[1920,1080],[1366,768],[390,844],[844,390],[320,568],[768,1024],[1024,768]],'max_settled_rect_shift_px':max(x.get('maxSettledShift',0) for x in u['measurements']),'clipped_text_surfaces':0,'horizontal_overflow_in_measured_wizard_phases':False,'new_external_assets':0,'physical_mobile_tested':False,'FPS_measured':False}
(D/'metrics.json').write_text(json.dumps(m,indent=2))
phases=['identity','difficulty','race-mode','stage-weather','garage','podium','results','teacher','teacher-settings','pin','modes','hud','quiz','pause']
items=[]
for size in ['1366x768','390x844']:
 for phase in phases:
  items.append('<section><h2>'+html.escape(size+' · '+phase)+'</h2><div class="pair">'+''.join('<figure><figcaption>'+label+'</figcaption><a href="screenshots/'+mode+'-'+size+'-'+phase+'.png"><img loading="lazy" src="screenshots/'+mode+'-'+size+'-'+phase+'.png"></a></figure>' for mode,label in [('before','Sebelum · PATCH 8F'),('after','Sesudah · PATCH 8G')])+'</div></section>')
others=''.join('<a href="screenshots/'+p.name+'">'+html.escape(p.stem)+'</a><br>'for p in sorted((D/'screenshots').glob('*.png')) if not any(p.name.startswith(x+'-'+y+'-'+z+'.')for x in ['before','after']for y in ['1366x768','390x844']for z in phases))
(D/'review.html').write_text('<!doctype html><html lang="id"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BlokRaya PATCH 8G · Before–After</title><style>body{background:#102036;color:#fff;font:16px/1.5 system-ui;margin:24px}section{margin:32px 0}h1{font-size:28px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:16px}figure{margin:0;min-width:0}img{display:block;width:100%;height:440px;object-fit:contain;background:#081320}a{color:#70d9ff}@media(max-width:700px){.pair{grid-template-columns:1fr}body{margin:14px}}</style><h1>PATCH 8G — Tipografi dan Spacing</h1><p>Render asli game pada viewport yang sama. <a href="README.md">Laporan</a> · <a href="metrics.json">Metrik</a></p>'+''.join(items)+'<h2>Viewport dan pengujian lainnya</h2>'+others+'</html>')
for kind in ['playable','review']:
 dest=R/f'blokraya-patch8g-{kind}.zip'
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
  z.write(D/'MULAI.txt','MULAI.txt');z.write(H,H.name if kind=='playable'else'visual-upgrade/'+H.name)
  if kind=='review':
   z.write(B,'visual-upgrade/'+B.name)
   for f in sorted(D.rglob('*')):
    if f.is_file()and '__pycache__'not in f.parts and f.name!='release-metrics.json':z.write(f,'visual-upgrade/patch8g/'+f.relative_to(D).as_posix())
 with zipfile.ZipFile(dest)as z:assert z.testzip()is None;assert z.read(H.name if kind=='playable'else'visual-upgrade/'+H.name)==H.read_bytes()
 m[kind+'_zip']={'file':dest.name,'bytes':dest.stat().st_size,'sha256':sha(dest.read_bytes()),'CRC_OK':True}
(D/'release-metrics.json').write_text(json.dumps(m,indent=2));print(json.dumps(m,indent=2))
