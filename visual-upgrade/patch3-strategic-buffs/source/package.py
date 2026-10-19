from pathlib import Path
import json,hashlib,zipfile
D=Path(__file__).resolve().parents[2];B=D/'patch3-strategic-buffs';H=D/'race-quest-pro-patch3.html';R=D.parent
required=['scope-tests','buff-tests','core-test-results','ui-tests','test-results','offline-test-results','persistence-tests','export-tests','stage-audio-tests','unchanged-renders','comparison-tests']
for n in required:assert json.loads((B/(n+'.json')).read_text())['status']=='passed',n
raw=H.read_bytes();old=(D/'race-quest-pro-patch2.html').read_bytes();sha=lambda x:hashlib.sha256(x).hexdigest();icons=json.loads((B/'icons/icons.json').read_text())
metrics={'baseline':'c786d88aca6876e7913012f3490fd2f6660898c8','html_bytes':len(raw),'baseline_bytes':len(old),'growth_bytes':len(raw)-len(old),'html_sha256':sha(raw),'under_25_decimal_MB':len(raw)<25000000,'new_icons':4,'new_icon_svg_bytes':sum(v['bytes'] for v in icons.values()),'new_audio_files':0,'new_models':0,'new_GPU_buffers':0,'additional_active_effects':{'reflect':{'draw_calls':1,'triangles':320},'grip':{'draw_calls':1,'triangles':320},'radar':'DOM, no WebGL draws','nitro':'Existing bounded particle pool, no new pool'},'unchanged_particle_pool_slots':480,'inventory_slots':2,'max_nitro_charges_per_reward':2,'global_item_cooldown_seconds':.6,'immunity_seconds':1.1,'tested_ordered_buff_pairs':81,'protected_historical_files':json.loads((B/'scope-tests.json').read_text())['protected_files'],'teacher_export_bytes':json.loads((B/'export-tests.json').read_text())['export_bytes'],'browser':'Cloud Chromium WebGL/software GPU; desktop and touch emulation','fps_measured':False,'physical_phone_tested':False,'mid_race_save_supported':False}
(B/'asset-metrics.json').write_text(json.dumps(metrics,indent=2))
notes='RACE QUEST PRO — PATCH 3 STRATEGIC BUFFS\n\nEkstrak ZIP, lalu buka race-quest-pro-patch3.html pada browser WebGL. Semua aset tertanam, tanpa CDN/internet. Klik/sentuh untuk mengaktifkan audio.\n\nJawab benar untuk hadiah buff. Dua slot: ketuk slot / Q / 1 / 2; E atau PAKAI untuk menggunakan. Slot penuh: pilih Ganti slot 1/2 atau Lewati hadiah sebelum melanjutkan. Empat hadiah baru: Perisai Pantul, Nitro Ganda (2 charge), Ban Anti-Selip, Radar Lintasan.\n\nInventori/cooldown berlaku per balapan, tidak disimpan untuk race berikutnya. Bank soal, profil, progres dan hasil belajar tetap tersimpan lokal. Pause/soal membekukan simulasi dan timer. Skor akademik tetap berdasarkan jawaban soal.\n\nBelum diuji HP/speaker fisik atau file:// pada browser cloud yang memblokirnya. Lihat ZIP review untuk laporan JSON, screenshot nyata, dokumentasi durasi/cooldown dan sumber editable.\n'
for kind in ['playable','review']:
 dest=R/('race-quest-pro-patch3-'+kind+'.zip')
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
  z.write(H,H.name);z.writestr('MULAI.txt',notes)
  if kind=='review':
   for f in sorted(B.rglob('*')):
    if f.is_file()and '__pycache__'not in f.parts and f.name!='release-metrics.json':z.write(f,'patch3-strategic-buffs/'+f.relative_to(B).as_posix())
 with zipfile.ZipFile(dest)as z:assert z.testzip()is None;assert z.read(H.name)==raw
 metrics[kind+'_zip']={'file':dest.name,'bytes':dest.stat().st_size,'sha256':sha(dest.read_bytes())}
(B/'release-metrics.json').write_text(json.dumps(metrics,indent=2));print(json.dumps(metrics,indent=2))
