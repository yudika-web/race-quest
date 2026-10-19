from pathlib import Path
import json,hashlib,zipfile
D=Path(__file__).resolve().parents[2];B=D/'stage1-pontianak';R=D.parent;H=D/'race-quest-pro-pontianak-stage1.html';name='race-quest-pro-pontianak-stage1'
reports=['scope-verification.json','core-test-results.json','test-results.json','offline-test-results.json','export-tests.json','scene-tests.json','unchanged-renders.json','capture-report.json']
for f in reports:assert json.loads((B/f).read_text())['status']=='passed',f
scope=json.loads((B/'scope-verification.json').read_text());assert hashlib.sha256(H.read_bytes()).hexdigest()==scope['html_sha256']
scene=json.loads((B/'scene-tests.json').read_text());meta=dict(html_bytes=H.stat().st_size,baseline_bytes=23349280,growth_bytes=H.stat().st_size-23349280,under_25_decimal_MB=H.stat().st_size<25000000,city_triangles=scene['city']['triangles'],city_colour_submissions=scene['city']['colour_draw_calls'],city_shadow_submissions=scene['city']['shadow_draw_calls'],city_owned_textures=3,source_mode='Procedural material batches; no new GLB or network assets',fps_measured=False)
(B/'asset-metrics.json').write_text(json.dumps(meta,indent=2))
notes='RACE QUEST - Pontianak Stage 1\n\nEkstrak ZIP ini, kemudian buka '+name+'.html di Chrome/Edge/Firefox dengan WebGL. Semua aset tertanam; internet tidak diperlukan saat bermain. Hanya visual Stage 1 diperbarui; Stage 2-3 tetap asli. Tidak ada unlock gratis.\n\nLaporan dan sumber lengkap: visual-upgrade/stage1-pontianak/ dalam repository dev/race-quest-cat-sport-visual-upgrade.\n'
for suffix in ['playable','review']:
 dest=R/(name+'-'+suffix+'.zip')
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  z.write(H,H.name);z.writestr('MULAI.txt',notes)
  if suffix=='review':
   for f in sorted(B.rglob('*')):
    if f.is_file() and f.name!='release-metrics.json' and '__pycache__' not in f.parts:z.write(f,'stage1-pontianak/'+f.relative_to(B).as_posix())
 with zipfile.ZipFile(dest) as z:assert z.testzip() is None;assert z.read(H.name)==H.read_bytes()
 meta[suffix+'_zip']={'name':dest.name,'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
(B/'release-metrics.json').write_text(json.dumps(meta,indent=2));print(json.dumps(meta,indent=2))
