from pathlib import Path
import json,hashlib,zipfile,subprocess,sys
D=Path(__file__).resolve().parents[2];B=D/'stage4-sambas';R=D.parent;H=D/'blokraya-stage4-sambas.html'
subprocess.run([sys.executable,str(B/'source/report.py')],check=True)
read=lambda n:json.loads((B/(n+'.json')).read_text());reports={n:read(n)for n in ['physics-tests','item-tests','world-tests','browser-tests','offline-tests','unchanged-renders','scope-tests']}
for n,r in reports.items():assert r['status']=='passed',n
raw=H.read_bytes();sha=lambda x:hashlib.sha256(x).hexdigest();metrics=read('asset-metrics');assert sha(raw)==metrics['html_sha256'];assert raw==Path('/tmp/blokraya-6a/candidate.html').read_bytes()
metrics.update({'under_25_decimal_MB':len(raw)<25000000,'reports':{n:len(r.get('checks',[]))for n,r in reports.items()},'teacher_export_bytes':reports['offline-tests']['export_bytes'],'offline_asset_HTTP_requests':len(reports['offline-tests']['assetRequests']),'direct_file_note':read('direct-file-tests').get('reason'),'release_status':'Ready for visual review; reference accuracy and direct file navigation have documented limitations.'})
notes='''BLOKRAYA — STAGE 4 SAMBAS / ROYAL RIVER ROAD (6A)

Ekstrak ZIP, lalu buka blokraya-stage4-sambas.html pada browser modern yang mendukung WebGL. Semua aset tertanam. Mode Siswa tanpa PIN; Mode Guru memakai PIN lokal. Klik/sentuh untuk audio. Gunakan browser/profil/origin yang sama untuk membaca data lokal lama.

Arena playable: Pontianak, Mempawah, Singkawang dan Sambas. Stage 5–10 tetap Segera Hadir; Nusantara belum dapat dimainkan. Kalbar Klasik tetap tiga arena lama. Hanya Sambas dibuat pada tahap ini.

Lintasan Sambas fiktif sepanjang 687,84 m: kawasan istana Melayu, jalan tepi sungai, promenade, dermaga dan jembatan dekoratif. Istana merupakan interpretasi blocky, bukan rekonstruksi historis terverifikasi; situs referensi tidak dapat diakses (403). Detail perlu tinjauan foto tepercaya. Tidak menggambarkan kegiatan balapan pada situs bersejarah sebenarnya.

Offline lulus pada browser dengan jaringan dinonaktifkan dan dokumen lokal disuplai harness di localhost, tanpa permintaan aset HTTP/CDN. Uji file:// dicoba tetapi ditolak kebijakan administrator browser cloud. Buka langsung file pada browser target dan HP fisik belum terverifikasi; tidak mengklaim FPS perangkat nyata. Tidak ada CDN/backend/server wajib baru atau paket fetch aset lokal.

Kontrol lama: A/D atau panah, W/S gas/rem, C drift, Shift jump, E/Spasi buff, Q/1/2 slot, P/Esc jeda. Sentuh dapat diatur di menu suara/pause. Pengaturan, PIN, profil, bank soal, ghost dan progres memakai kunci penyimpanan lama.

ZIP review berisi folder stage4-sambas: sumber builder/track, metadata, thumbnail, screenshot, laporan pengujian dan metrik aset. Build ulang memerlukan checkout repository berisi baseline Prompt 5, sesuai README. Tidak ada profil/unlock/token QA yang ditanamkan ke HTML.

Tidak merge ke main, tidak mengubah index.html online, tidak deployment atau mengerjakan 6B.
'''
for kind in ['playable','review']:
 dest=R/f'blokraya-stage4-sambas-{kind}.zip'
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
  z.write(H,H.name);z.writestr('MULAI.txt',notes)
  if kind=='review':
   for f in sorted(B.rglob('*')):
    if f.is_file()and '__pycache__'not in f.parts and f.name!='release-metrics.json':z.write(f,'stage4-sambas/'+f.relative_to(B).as_posix())
 with zipfile.ZipFile(dest)as z:assert z.testzip()is None;assert z.read(H.name)==raw;entries=len(z.namelist())
 metrics[kind+'_zip']={'file':dest.name,'bytes':dest.stat().st_size,'sha256':sha(dest.read_bytes()),'crc_ok':True,'html_identical':True,'entries':entries}
(B/'release-metrics.json').write_text(json.dumps(metrics,indent=2));print(json.dumps({k:metrics[k]for k in ['html_bytes','growth_bytes','html_sha256','playable_zip','review_zip']},indent=2))
