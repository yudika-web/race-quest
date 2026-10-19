from pathlib import Path
import json,hashlib,zipfile
D=Path(__file__).resolve().parents[2];B=D/'stage3-singkawang';R=D.parent;H=D/'race-quest-pro-singkawang-stage3.html';name='race-quest-pro-singkawang-stage3'
reports=['scope-verification.json','core-test-results.json','physics-comparison.json','test-results.json','offline-test-results.json','export-tests.json','scene-tests.json','unchanged-renders.json','capture-report.json']
for f in reports:assert json.loads((B/f).read_text())['status']=='passed',f
scope=json.loads((B/'scope-verification.json').read_text());assert hashlib.sha256(H.read_bytes()).hexdigest()==scope['html_sha256']
scene=json.loads((B/'scene-tests.json').read_text());meta=dict(html_bytes=H.stat().st_size,baseline_bytes=23378794,growth_bytes=H.stat().st_size-23378794,under_25_decimal_MB=H.stat().st_size<25000000,coast_triangles=scene['coast']['triangles'],terrain_triangles=scene['coast']['terrain_triangles'],coast_colour_submissions=scene['coast']['colour_draw_calls'],coast_shadow_submissions=scene['coast']['shadow_draw_calls'],coast_owned_textures=3,source_mode='Procedural material batches; no new GLB or network assets',fps_measured=False)
(B/'asset-metrics.json').write_text(json.dumps(meta,indent=2))
notes='RACE QUEST - Singkawang Stage 3\n\nEkstrak ZIP, kemudian buka '+name+'.html di Chrome/Edge/Firefox dengan WebGL. Pada menu Mulai, pilih Stage Singkawang - Pantai Meriah dan Cuaca Sesuai Tema/Cerah. Semua aset tertanam; internet tidak diperlukan saat bermain. Stage 1 Pontianak dan Stage 2 Mempawah tetap tersedia tanpa perubahan. Pilihan Hujan/Kabut tetap ada. Tidak ada unlock gratis atau perubahan profil/bank bawaan.\n\nLaporan, sumber dan screenshot: visual-upgrade/stage3-singkawang/ pada branch dev/race-quest-cat-sport-visual-upgrade.\n'

for suffix in ['playable','review']:
 dest=R/(name+'-'+suffix+'.zip')
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  z.write(H,H.name);z.writestr('MULAI.txt',notes)
  if suffix=='review':
   for f in sorted(B.rglob('*')):
    if f.is_file() and f.name!='release-metrics.json' and '__pycache__' not in f.parts:z.write(f,'stage3-singkawang/'+f.relative_to(B).as_posix())
 with zipfile.ZipFile(dest) as z:assert z.testzip() is None;assert z.read(H.name)==H.read_bytes()
 meta[suffix+'_zip']={'name':dest.name,'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
(B/'release-metrics.json').write_text(json.dumps(meta,indent=2));print(json.dumps(meta,indent=2))
