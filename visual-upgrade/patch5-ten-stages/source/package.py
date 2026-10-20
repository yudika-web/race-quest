from pathlib import Path
import json,hashlib,zipfile
D=Path(__file__).resolve().parents[2];B=D/'patch5-ten-stages';R=D.parent;H=D/'blokraya-patch5.html'
reports={n:json.loads((B/(n+'.json')).read_text())for n in ['unit-tests','ui-tests','grand-prix-browser-tests','offline-export-tests','unchanged-renders','scope-tests']}
for n,d in reports.items():assert d['status']=='passed',n
raw=H.read_bytes();sha=lambda b:hashlib.sha256(b).hexdigest();scope=reports['scope-tests'];assert sha(raw)==scope['html_sha256']
metrics={k:scope[k]for k in ['baseline','html_bytes','baseline_bytes','growth_bytes','html_sha256','remaining_bytes','budget_bytes','historical_files_unchanged']}
metrics.update({'under_25_decimal_MB':len(raw)<25000000,'metadata_stages':10,'playable_stages':['kampung','kapuas','hutan'],'coming_soon_stages':['sambas','sintang','kapuas_hulu','bengkayang','yogyakarta','bali','bromo'],'playable_cups':['kalbar-klasik'],'unavailable_cups':['nusantara'],'unit_check_groups':len(reports['unit-tests']['checks']),'responsive_ui_checks':len(reports['ui-tests']['checks']),'grand_prix_browser_checks':len(reports['grand-prix-browser-tests']['checks']),'offline_export_checks':len(reports['offline-export-tests']['checks']),'protected_render_cases':len(reports['unchanged-renders']['checks']),'protected_named_script_payloads':len(scope['protected_script_payloads']),'teacher_export_bytes':reports['offline-export-tests']['export_bytes'],'new_environment_assets':0,'new_textures':0,'new_GPU_programs':0,'new_race_draw_calls':0,'new_race_triangles':0,'storage_keys_preserved':True,'physical_phone_tested':False,'FPS_measured':False,'memory_benchmarked':False,'direct_file_scheme_tested':False,'offline_test_method':'Chromium context offline:true; local document fulfilled by harness on localhost; zero asset HTTP/CDN requests.'})
(B/'asset-metrics.json').write_text(json.dumps(metrics,indent=2))
notes='''BLOKRAYA — PATCH 5: TEN-STAGE ARCHITECTURE

Ekstrak ZIP lalu buka blokraya-patch5.html pada browser modern dengan WebGL. Semua aset tertanam, tanpa CDN/backend. Browser cloud memblokir file://, sehingga pengujian offline dilakukan dengan jaringan dimatikan dan dokumen lokal disuplai harness pada localhost. HP fisik dan FPS belum diuji.

PLAYABLE: Pontianak, Mempawah, Singkawang. Kalbar Klasik tetap tiga arena.
SEGERA HADIR: Sambas, Sintang, Kapuas Hulu, Bengkayang, Yogyakarta, Bali, Bromo. Belum ada world/lintasan untuk tujuh arena ini. Grand Prix Nusantara belum dapat dimainkan sampai seluruh world tersedia. Tes sepuluh ronde hanya memeriksa urutan/poin/ketuntasan menggunakan metadata.

Pilih Mode Siswa untuk bermain tanpa PIN. Mode Guru memakai PIN lokal yang Anda buat sendiri. Loading minimum 3 detik dan kedua poster tetap ada. Profil, bank soal, progres, ghost, audio/HUD dan PIN lama memakai kunci penyimpanan asli. Gunakan browser/profil/origin yang sama untuk mengakses data lama. Mengubah origin browser dapat memberi ruang penyimpanan berbeda.

Kontrol: A/D atau panah, W/S gas/rem, C drift, Shift jump, E/Spasi buff, Q/1/2 pilih slot, P/Esc jeda. Kontrol sentuh tersedia melalui pengaturan. Klik/sentuh untuk mengaktifkan audio.

ZIP review menyertakan patch5-ten-stages/: README, metadata, sumber patch, screenshot asli dan laporan tes/asset-metrics.json. Build ulang memakai baseline HTML dari checkout repository seperti petunjuk README. Tidak ada unlock/token/profil demonstrasi disisipkan dalam distribusi.

Tidak mengubah index.html online, merge ke main, deployment, atau membangun arena Prompt 6.
'''
for kind in ['playable','review']:
 dest=R/f'blokraya-patch5-{kind}.zip'
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
  z.write(H,H.name);z.writestr('MULAI.txt',notes)
  if kind=='review':
   for f in sorted(B.rglob('*')):
    if f.is_file()and '__pycache__'not in f.parts and f.name!='release-metrics.json':z.write(f,'patch5-ten-stages/'+f.relative_to(B).as_posix())
 with zipfile.ZipFile(dest)as z:
  assert z.testzip()is None;assert z.read(H.name)==raw
  metrics[kind+'_zip']={'file':dest.name,'bytes':dest.stat().st_size,'sha256':sha(dest.read_bytes()),'crc_ok':True,'html_identical':True,'entries':len(z.namelist())}
(B/'release-metrics.json').write_text(json.dumps(metrics,indent=2));print(json.dumps(metrics,indent=2))
