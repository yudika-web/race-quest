from pathlib import Path
import json,hashlib,zipfile
D=Path(__file__).resolve().parents[2];B=D/'blokraya-branding';R=D.parent;H=D/'blokraya-balap-edukasi-nusantara.html'
required=['scope-tests','loading-tests','legacy-storage-tests','controls-tests','core-test-results','engine-parity','export-tests','persistence-tests','stage-audio-tests','offline-test-results']
reports={n:json.loads((B/(n+'.json')).read_text())for n in required}
for n,d in reports.items():assert d['status']=='passed',n
raw=H.read_bytes();sha=lambda b:hashlib.sha256(b).hexdigest();scope=reports['scope-tests'];assert scope['html_sha256']==sha(raw)
posters=json.loads((B/'poster-metrics.json').read_text());metrics={**{k:scope[k]for k in ['baseline_commit','html_bytes','baseline_bytes','growth_bytes','html_sha256','under_25_decimal_MB','protected_historical_files']},'poster_original_total_bytes':sum(p['original_bytes']for p in posters),'poster_distribution_total_bytes':sum(p['optimized_bytes']for p in posters),'posters':posters,'new_embedded_images':2,'each_poster_embedded_once':True,'existing_asset_payload_preserved':True,'new_GPU_programs':0,'new_WebGL_draw_calls':0,'new_animation_loops':0,'loading_viewports':len(reports['loading-tests']['viewports']),'paired_complete_races':reports['engine-parity']['cases'],'teacher_export_bytes':reports['export-tests']['export_bytes'],'storage_keys_preserved':True,'physical_phone_tested':False,'FPS_measured':False,'direct_file_scheme_tested':False}
(B/'asset-metrics.json').write_text(json.dumps(metrics,indent=2))
notes='''BLOKRAYA — BALAP EDUKASI NUSANTARA

Ekstrak ZIP, lalu buka blokraya-balap-edukasi-nusantara.html di browser modern dengan WebGL. Semua aset tertanam; game dapat dimainkan offline tanpa CDN. Klik/sentuh tombol untuk mengaktifkan audio.

Dua poster WebP asli pengguna ditampilkan sesuai orientasi layar. Loading “Memuat...” menunggu kesiapan gambar/material dan tampilan. Progress menunjukkan jumlah gambar yang selesai bila tersedia; persiapan renderer memakai indikator tak tentu, bukan persentase unduhan palsu. Loading dapat hilang sangat cepat pada perangkat yang sudah siap.

14 karakter, tiga arena, Smart AI, dua slot buff, HUD, soal, Ruang Guru dan data lama dipertahankan. Penyimpanan memakai kunci lama agar progres tetap terbaca. Agar browser mengakses penyimpanan yang sama, gunakan origin/browser/profil yang sama; browser dapat membatasi storage untuk file lokal sebagaimana sebelumnya.

E/Spasi pakai buff; Q/1/2 pilih slot; A/D kemudi; W/S gas/rem; C drift; Shift loncat; P/Esc jeda. Kontrol sentuh dapat diatur lewat Suara/Pause.

ZIP review memuat sumber, poster asli/optimasi dan laporan. HP diuji melalui emulasi, bukan perangkat fisik; tidak ada klaim FPS HP. Browser cloud memblokir file://; offline diuji dengan jaringan dimatikan dan byte HTML lokal disuplai langsung.
'''
for kind in ['playable','review']:
 dest=R/f'blokraya-balap-edukasi-nusantara-{kind}.zip'
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
  z.write(H,H.name);z.writestr('MULAI.txt',notes)
  if kind=='review':
   for f in sorted(B.rglob('*')):
    if f.is_file()and '__pycache__'not in f.parts and f.name!='release-metrics.json':z.write(f,'blokraya-branding/'+f.relative_to(B).as_posix())
 with zipfile.ZipFile(dest)as z:assert z.testzip()is None;assert z.read(H.name)==raw
 metrics[kind+'_zip']={'file':dest.name,'bytes':dest.stat().st_size,'sha256':sha(dest.read_bytes())}
(B/'release-metrics.json').write_text(json.dumps(metrics,indent=2));print(json.dumps(metrics,indent=2))
