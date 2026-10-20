from pathlib import Path
import json,hashlib,zipfile,subprocess,sys
D=Path(__file__).resolve().parents[2];B=D/'stage5-sintang';R=D.parent;H=D/'blokraya-stage5-sintang.html'
subprocess.run([sys.executable,str(B/'source/report.py')],check=True)
read=lambda n:json.loads((B/(n+'.json')).read_text());reports={n:read(n)for n in ['physics-tests','item-tests','surface-tests','world-tests','browser-tests','offline-tests','unchanged-renders','scope-tests']}
for n,r in reports.items():assert r['status']=='passed',n
raw=H.read_bytes();sha=lambda x:hashlib.sha256(x).hexdigest();metrics=read('asset-metrics');assert sha(raw)==metrics['html_sha256'];assert raw==Path('/tmp/blokraya-6b/candidate.html').read_bytes()
metrics.update({'under_25_decimal_MB':len(raw)<25000000,'reports':{n:len(r.get('checks',[]))for n,r in reports.items()},'teacher_export_bytes':reports['offline-tests']['export_bytes'],'offline_asset_HTTP_requests':len(reports['offline-tests']['assetRequests']),'direct_file_note':read('direct-file-tests').get('reason'),'release_status':'Ready for visual review; reference accuracy and direct file navigation have documented limitations.'})
notes='BLOKRAYA — STAGE 5 SINTANG / KELAM MOUNTAIN RUN (6B)\n\nEkstrak ZIP lalu buka blokraya-stage5-sintang.html pada browser modern dengan WebGL. Seluruh aset tertanam; tidak menambahkan CDN/backend. Gunakan browser/profil/origin sama untuk membaca data lokal lama. Mode Siswa tanpa PIN; Mode Guru menggunakan PIN lokal. Klik/sentuh untuk audio.\n\nPLAYABLE: Pontianak, Mempawah, Singkawang, Sambas dan Sintang. Stage 6–10 tetap Segera Hadir; Nusantara menunggu lima world lainnya. Kalbar Klasik tetap tiga arena lama. Hanya Sintang dibangun pada tahap ini.\n\nLintasan Sintang fiktif sepanjang 905,66 m melalui perbukitan dan hutan tropis, monolit granit terinspirasi Bukit Kelam serta rumah panjang berpanggung terinspirasi Rumah Betang Ensaid Panjang. Tidak menggambarkan aktivitas balap sebenarnya di kawasan budaya/alami. Referensi web diblokir 403; detail landmark merupakan interpretasi, bukan rekonstruksi terverifikasi.\n\nPengujian offline dengan jaringan mati dan dokumen lokal pada localhost lolos, tanpa permintaan HTTP/CDN aset. Navigasi file:// dicoba tetapi diblokir administrator browser cloud. Buka langsung file di browser target serta HP fisik/FPS belum terverifikasi. Tidak ada server wajib baru atau paket fetch aset lokal yang ditambahkan.\n\nKontrol: A/D/panah, W/S gas/rem, C drift, Shift jump, E/Spasi buff, Q/1/2 slot, P/Esc jeda. Sentuh tersedia melalui pengaturan suara/pause. Kunci data bank soal, progres, profil, ghost, PIN, audio dan HUD tetap.\n\nZIP review memuat sumber builder/track, metadata, thumbnail, screenshot serta hasil uji. Build ulang memerlukan checkout repository berisi HTML baseline Sambas; lihat README. Profil/token/unlock QA tidak disisipkan ke distribusi.\n\nTidak merge ke main, mengubah index.html, deployment atau mengerjakan 6C.\n'
for kind in ['playable','review']:
 dest=R/f'blokraya-stage5-sintang-{kind}.zip'
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
  z.write(H,H.name);z.writestr('MULAI.txt',notes)
  if kind=='review':
   for f in sorted(B.rglob('*')):
    if f.is_file()and '__pycache__'not in f.parts and f.name!='release-metrics.json':z.write(f,'stage5-sintang/'+f.relative_to(B).as_posix())
 with zipfile.ZipFile(dest)as z:assert z.testzip()is None;assert z.read(H.name)==raw;entries=len(z.namelist())
 metrics[kind+'_zip']={'file':dest.name,'bytes':dest.stat().st_size,'sha256':sha(dest.read_bytes()),'crc_ok':True,'html_identical':True,'entries':entries}
(B/'release-metrics.json').write_text(json.dumps(metrics,indent=2));print(json.dumps({k:metrics[k]for k in ['html_bytes','growth_bytes','html_sha256','playable_zip','review_zip']},indent=2))
