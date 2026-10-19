from pathlib import Path
import json,hashlib,zipfile
D=Path(__file__).resolve().parents[2];B=D/'student-teacher-modes';R=D.parent;H=D/'blokraya-mode-siswa-guru.html'
reports={n:json.loads((B/(n+'.json')).read_text())for n in ['scope-tests','visual-tests','auth-tests','offline-game-tests','fallback-tests']}
for n,d in reports.items():assert d['status']=='passed',n
raw=H.read_bytes();sha=lambda b:hashlib.sha256(b).hexdigest();scope=reports['scope-tests'];assert sha(raw)==scope['html_sha256']
metrics={**{k:scope[k]for k in ['baseline_commit','html_bytes','baseline_bytes','growth_bytes','html_sha256','under_25_decimal_MB','protected_historical_files']},'loading_minimum_ms':3000,'fade_ms':400,'reduced_motion_fade_ms':0,'loading_timings':[{k:c[k]for k in ['viewport','timing']}for c in reports['visual-tests']['cases']],'auth_checks':len(reports['auth-tests']['checks']),'offline_game_checks':len(reports['offline-game-tests']['checks']),'teacher_export_bytes':reports['offline-game-tests']['export_bytes'],'PIN_KDF':'PBKDF2-SHA256','PIN_iterations':600000,'PIN_salt_bits':128,'PIN_verifier_bits':256,'PIN_plaintext_stored':False,'teacher_session_persisted':False,'storage_keys_preserved':True,'new_embedded_images':0,'new_GPU_programs':0,'new_WebGL_draw_calls':0,'physical_phone_tested':False,'FPS_measured':False,'direct_file_scheme_tested':False}
(B/'asset-metrics.json').write_text(json.dumps(metrics,indent=2))
notes='''BLOKRAYA — MODE SISWA / MODE GURU

Ekstrak ZIP lalu buka blokraya-mode-siswa-guru.html pada browser modern dengan WebGL. Semua aset tertanam dan game dapat dimainkan offline, tanpa CDN/backend.

Buka game → poster fullscreen + Memuat (minimum 3 detik, menunggu kesiapan aset) → Pilih Mode. Mode Siswa memulai persiapan balapan tanpa PIN. Mode Guru memerlukan PIN lokal yang Anda buat sendiri, numerik 6–32 digit. Tidak ada PIN bawaan atau master PIN.

Verifier PIN memakai salt acak dan PBKDF2-SHA256 melalui Web Crypto; PIN asli tidak disimpan. Lima kegagalan memicu cooldown dalam sesi. Logout/reload mengunci akses kembali. Kunci data belajar lama tetap dipertahankan; gunakan browser/profil/origin yang sama untuk membaca penyimpanan yang sama.

PIN adalah pembatas UI lokal, bukan perlindungan terhadap pemilik HTML/devtools/browser storage. Jika lupa, pemilik perangkat dapat menghapus hanya entri localStorage blokraya_teacher_pin_v1, lalu reload dan membuat PIN baru. Jangan hapus seluruh data situs: bank, progres dan laporan dapat hilang. Bantuan juga tersedia pada formulir PIN. Pada browser tanpa Web Crypto, Mode Guru ditolak dengan pesan; siswa tetap dapat bermain.

Kontrol balapan lama tetap berfungsi: A/D atau panah, W/S gas/rem, C drift, Shift loncat, E/Spasi pakai buff, Q/1/2 pilih slot, P/Esc jeda. Pilihan sentuh ada di Suara/Pause. Klik/sentuh untuk mengaktifkan audio.

ZIP review berisi sumber, screenshot dan hasil uji. HP diuji lewat emulasi, bukan perangkat fisik/FPS. Browser cloud memblokir file://; offline diuji dengan jaringan mati dan HTML lokal disuplai langsung.
'''
for kind in ['playable','review']:
 dest=R/f'blokraya-mode-siswa-guru-{kind}.zip'
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
  z.write(H,H.name);z.writestr('MULAI.txt',notes)
  if kind=='review':
   for f in sorted(B.rglob('*')):
    if f.is_file()and '__pycache__'not in f.parts and f.name!='release-metrics.json':z.write(f,'student-teacher-modes/'+f.relative_to(B).as_posix())
 with zipfile.ZipFile(dest)as z:assert z.testzip()is None;assert z.read(H.name)==raw
 metrics[kind+'_zip']={'file':dest.name,'bytes':dest.stat().st_size,'sha256':sha(dest.read_bytes())}
(B/'release-metrics.json').write_text(json.dumps(metrics,indent=2));print(json.dumps(metrics,indent=2))
