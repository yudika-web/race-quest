from pathlib import Path
import re,json,hashlib,base64
from app_hooks import patch_app
D=Path(__file__).resolve().parents[2];B=D/'patch1-garage-stage';h=(D/'race-quest-pro-singkawang-stage3.html').read_text();meta=json.loads((B/'baseline.json').read_text());assert hashlib.sha256(h.encode()).hexdigest()==meta['html_sha256']
assets={}
for p in sorted((B/'assets').glob('*.webp')):
 data=p.read_bytes();assets[p.name]={'uri':'data:image/webp;base64,'+base64.b64encode(data).decode(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
assert len(assets)==6
scripts=list(re.finditer(r'<script\b[^>]*>(.*?)</script>',h,re.S));m=scripts[8];app,changes=patch_app(m[1]);h=h[:m.start(1)]+app+h[m.end(1):]
(B/'app-ui-changes.json').write_text(json.dumps(changes,indent=2,ensure_ascii=False))
css='\n<style id="patch1Styles">\n'+(B/'source/ui.css').read_text()+'\n</style>\n';h=h.replace('</head>',css+'</head>',1)
old='<span class="muted small">Soal dijawab saat seluruh balapan dijeda.</span>';new='<button type="button" id="garageStageBtn" aria-haspopup="dialog">Pilih arena →</button>';assert h.count(old)==1;h=h.replace(old,new)
assert h.count('Siap, Balapan! →')==1;h=h.replace('Siap, Balapan! →','Mulai Balapan →')
dialog='<dialog id="stagePickerDialog" aria-labelledby="stagePickerTitle"><form method="dialog"><div class="dialog-head"><div class="row"><span class="eyebrow">JELAJAH KALIMANTAN BARAT</span><button type="button" class="dialog-close" data-close="stagePickerDialog" aria-label="Tutup">✕</button></div><h2 id="stagePickerTitle">Pilih perjalananmu.</h2></div><div class="dialog-body" id="garageStagePicker"></div><div class="dialog-foot"><button type="button" class="btn ghost" data-close="stagePickerDialog">Kembali ke Garasi</button><button type="button" class="btn" id="stagePickerRaceBtn">Mulai Balapan →</button></div></form></dialog>\n'
pos=h.index('<script id="initialData"');h=h[:pos]+dialog+h[pos:]
scripts=list(re.finditer(r'<script\b[^>]*>(.*?)</script>',h,re.S));end=scripts[7].end()
new_scripts='\n<script id="patch1StageCatalog" type="application/json">'+(B/'source/stage-catalog.json').read_text().strip()+'</script>\n<script id="patch1StageAssets" type="application/json">'+json.dumps(assets,separators=(',',':'))+'</script>\n<script id="patch1Workshop">\n'+(B/'source/workshop.js').read_text()+'\n</script>\n<script id="patch1StageUI">\n'+(B/'source/stage-ui.js').read_text()+'\n</script>'
h=h[:end]+new_scripts+h[end:];out=D/'race-quest-pro-patch1.html';out.write_text(h);print('Playable bytes',out.stat().st_size)
