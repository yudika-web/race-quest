from pathlib import Path
import json,hashlib,zipfile
D=Path(__file__).resolve().parents[2];B=D/'patch1-garage-stage';H=D/'race-quest-pro-patch1.html';R=D.parent;name='race-quest-pro-patch1'
reports=['scope-verification.json','core-test-results.json','test-results.json','offline-test-results.json','export-tests.json','scene-tests.json','unchanged-renders.json','capture-ui-report.json','all-character-tests.json','stage-ui-tests.json','thumbnail-render-report.json','preview-controls-tests.json']
for f in reports:assert json.loads((B/f).read_text())['status']=='passed',f
scope=json.loads((B/'scope-verification.json').read_text());assert hashlib.sha256(H.read_bytes()).hexdigest()==scope['html_sha256']
meta={**{k:scope[k]for k in ['html_bytes','growth_bytes','html_sha256','html_under_25_decimal_MB']},'baseline_bytes':23394232,'workshop':json.loads((B/'workshop-metrics.json').read_text()),'thumbnail_webp_bytes':sum(p.stat().st_size for p in(B/'assets').glob('*.webp')),'fps_measured':False,'physical_phone_tested':False,'teacher_export_bytes':json.loads((B/'export-tests.json').read_text())['export_bytes']}
meta['asset_files']=[{'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in sorted((B/'assets').iterdir())if p.is_file()]
(B/'asset-metrics.json').write_text(json.dumps(meta,indent=2))
notes='RACE QUEST PRO - PATCH 1\n\nEkstrak ZIP lalu buka race-quest-pro-patch1.html di browser desktop/HP yang mendukung WebGL. Jangan hanya membuka halaman preview ZIP. Seluruh aset sudah tertanam; tidak perlu CDN atau internet ketika bermain. Pilih Mulai, klik kartu Pontianak/Mempawah/Singkawang, lanjut ke Garasi, lalu Mulai Balapan. Stage juga dapat diubah melalui tombol arena di footer garasi. Mobil + Karakter dan Close-up Karakter tetap tersedia; geser untuk putar, cubit/scroll untuk zoom. Ruang Guru tetap menggunakan pengaturan stage asli.\n\nTidak mengubah index.html online, model karakter/kendaraan, gameplay atau data profil. Laporan/sumber/screenshot ada pada paket review.\n'
for kind in ['playable','review']:
 dest=R/(name+'-'+kind+'.zip')
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
  z.write(H,H.name);z.writestr('MULAI.txt',notes)
  if kind=='review':
   for p in sorted(B.rglob('*')):
    if p.is_file()and '__pycache__'not in p.parts and p.name not in ['release-metrics.json']and not p.name.endswith('.blend1'):z.write(p,'patch1-garage-stage/'+p.relative_to(B).as_posix())
 with zipfile.ZipFile(dest)as z:assert z.testzip()is None;assert z.read(H.name)==H.read_bytes()
 meta[kind+'_zip']={'name':dest.name,'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
(B/'release-metrics.json').write_text(json.dumps(meta,indent=2));print(json.dumps({k:v for k,v in meta.items()if k!='asset_files'},indent=2))
