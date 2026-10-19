# PATCH 4 — Smart Racing AI

Baseline: PATCH 3 `dab093d0c26dd38afdece02b45a8577111b512ab`. Branch: `dev/race-quest-cat-sport-visual-upgrade`. Distribusi: [race-quest-pro-patch4.html](../race-quest-pro-patch4.html). Tidak mengganti `index.html`, merge atau deploy.

## Hasil yang dapat ditinjau

Empat AI memakai racing line/kemudi halus yang dikembangkan dari baseline, sensor lokal, keputusan tertunda, inventori dua slot dan sembilan buff. Ada empat kepribadian: Agresif, Defensif, Cepat Berisiko, Seimbang. Serangan mempertimbangkan pemain maupun AI lain, dengan peringatan sebelum penggunaan. Feed singkat menyebut nama hewan dan buff/efek; cincin warna memperlihatkan efek aktif lawan.

- [Laporan perilaku dan angka pembanding](BEHAVIOR-REPORT.md) · [grafik](balance-chart.svg).
- HUD [desktop](screenshots/racing-desktop.png) / [HP](screenshots/racing-mobile.png).
- Peringatan serangan [desktop](screenshots/warning-desktop.png) / [HP](screenshots/warning-mobile.png).
- Oli [desktop](screenshots/oil-desktop.png) / [HP](screenshots/oil-mobile.png); Perisai [desktop](screenshots/shield-desktop.png) / [HP](screenshots/shield-mobile.png).
- Semua screenshot berasal dari renderer/UI game. Fixture browser menempatkan mobil dan item untuk mencapai keadaan langka; tidak mengubah profil/unlock distribusi. Tidak ada ilustrasi generatif sebagai bukti.

## Audit baseline

`Session.advanceAI` lama menggabungkan racing line `curvature × 75`, tiga kandidat lajur, kemudi eksponensial, akselerasi 6 m/s², grade/kurva, penyesuaian kecepatan menurut jarak pemain, dan generator item berulang. AI mempertimbangkan mobil di depan dan oli/rintangan dalam 12 m. Santai tidak menyalip; Sedang/Menantang mempunyai peluang menghindar dan menyerang. Kepribadian lama memengaruhi kesalahan, kelincahan, peluang Oli atau agresi, tetapi belum memiliki pertahanan aktif atau inventori dua slot.

AI mendapatkan Gelembung/Oli pertama setelah 7–15 dtk, lalu diisi ulang setiap 6–14 dtk, tanpa batas pasokan balapan. Pemilihan target serangan sengaja ditujukan ke pemain; collision proyektil/oli juga bisa mengenai AI lain secara insidental. Santai sudah kebal serangan AI. PATCH 3 memberi semua target kekebalan 1,1 dtk setelah hit/blok.

Temuan lain: skill dan catch-up bisa membuat kecepatan AI tanpa buff melebihi cap biasa pemain (maksimum teramati baseline 27,438 m/s dalam benchmark). Rintangan/celah hanya memengaruhi rencana jalur AI, tanpa pemeriksaan penalti collision seperti pemain; ramp memakai tinggi visual sinus. Karena alasan ini, metode AI monolitik dibungkus ulang dalam subclass khusus, dengan penggunaan ulang Track, racing line, kandidat lajur, percepatan/grade, collision item, renderer, rig dan timer PATCH 3. Mesin permainan tidak disalin atau direfactor.

## Tabel keseimbangan

| Parameter | Santai | Sedang | Menantang |
|---|---:|---:|---:|
| Pace dasar lama, tetap | 16,5 | 21,9 | 22,6 m/s |
| Waktu reaksi | 1,10 | 0,65 | 0,35 dtk |
| Interval evaluasi (±5%) | 0,90 | 0,65 | 0,45 dtk |
| Jangkauan lokal cerah | 22 | 32 | 36 m |
| Peluang dasar rencana menghindar | 28% | 70% | 87% |
| Peluang pilih serangan per kesempatan sah, sebelum kepribadian | 0% | 26% | 50% |
| Peluang memperoleh satu pasokan di pos yang dilewati | 55% | 72% | 82% |
| Jeda global penggunaan per AI | 3,0 | 2,0 | 1,5 dtk |
| Jarak waktu minimal antar-serangan sengaja ke pemain, seluruh AI | Tidak menyerang | 4,5 | 3,5 dtk |

Kepribadian mengalikan peluang serangan: Agresif ×1,30; Defensif ×0,45; Berisiko ×1,05; Seimbang ×0,85. Perisai dipertimbangkan saat ETA ancaman kurang dari 1,2 / 2,4 / 0,8 / 1,7 dtk, sehingga Defensif mempertahankan diri lebih dini. Kepribadian juga mengubah toleransi kesalahan, sedikit bias pace (tetap dibatasi) dan peluang rencana menghindar. Peluang rencana bukan jaminan berhasil, dan peluang memilih serangan bukan peluang mengenai siswa.

Sensor hujan ×0,88, kabut ×0,72; Radar memberi jangkauan 45 m dan +0,10 peluang rencana menghindar. Defensif +0,06, Berisiko −0,10; batas maksimum 0,96. Keputusan memakai informasi lokal posisi/lajur/ketinggian/kecepatan, proyektil, rintangan dan pertahanan yang tampak. Tidak memakai jawaban soal, kunci, inventori pemain atau ranking untuk memacu kecepatan.

## Pasokan dan buff

AI mulai tanpa item. Setiap pos soal publik di sepanjang balapan memberi **maksimal satu kesempatan pasokan untuk setiap AI**, sekali lewat; maksimum jumlah pos sama dengan jumlah soal. Ini pasokan lawan komputer, bukan jawaban atau nilai akademik palsu. Siswa tetap hanya memperoleh hadiah inventori melalui jawaban benar. AI tidak membaca isi/kunci soal. Tidak ada isi ulang berbasis waktu.

Dua slot, tanpa penggantian otomatis saat penuh. Item tidak terpakai kedaluwarsa setelah 28 dtk simulasi. Bag diacak tanpa pengulangan sampai habis; Santai mengecualikan Gelembung/Oli. Nitro membawa dua charge. Maksimal penggunaan total dibatasi dua kali jumlah pasokan yang benar-benar diterima, dan cooldown tetap berlaku meskipun mendapat item sama lagi. Durasi serta cooldown jenis memakai PATCH 3:

| Buff | Durasi / efek | Cooldown jenis | Kondisi keputusan |
|---|---|---:|---|
| Turbo | 4 dtk | 6 dtk | Ada mobil di depan, lintasan lokal aman, cukup cepat dan kurva tidak tajam |
| Perisai | Maks. 8 dtk, satu blok | 10 dtk | Proyektil/oli akan datang; menahan item atau rintangan jalan |
| Magnet | 7 dtk | 9 dtk | Token dekat di luar jangkauan biasa |
| Gelembung | TTL 4 dtk, hit 2,4 dtk | 3 dtk | Target sah 3–27 m di depan, selisih lajur <1,25 m |
| Oli | TTL 10 dtk, slip 2,8 dtk | 4 dtk | Target sah 4–19 m di belakang, lajur sama |
| Perisai Pantul | Maks. 6 dtk, satu blok; pantulan 0,9 dtk | 10 dtk | Pertahanan; penyerang sah dalam 40 m, di tanah, belum finis dan tidak kebal |
| Nitro Ganda | Dua dorongan 1 dtk terpisah | 1,6 dtk | Kesempatan menyalip aman, tidak bersamaan Turbo/Nitro aktif |
| Ban Anti-Selip | 5 dtk; oli maks. 0,7 dtk, cap saat oli 14 m/s | 7 dtk | Terkena oli atau kondisi hujan/kurva licin |
| Radar | 6 dtk, sensor 45 m | 9 dtk | Visibilitas rendah, tikungan atau bahaya yang sedang terlihat |

Target divalidasi ulang setelah waktu reaksi. Tembakan dibatalkan bila target berpindah lajur, menjauh, melompat, sudah kebal/finis, atau jatah serangan ke pemain belum siap. Menantang menghindari membuang serangan ke perisai yang tampak. Proyektil tetap berjalan lurus; oli tetap di lokasi jalan, tanpa homing.

Semua pihak mempertahankan kekebalan hit item 1,1 dtk. Pantulan dapat kembali kepada penyerang pemain atau AI, dengan aturan jarak/ketinggian yang sama. Perisai penerima pantulan dapat menyerapnya; tidak ada pantulan berantai/proyektil baru. Santai tetap melindungi pemain, termasuk dari efek pantulan AI. Buff kecepatan tidak dijumlahkan; batas 23 m/s biasa dan 31 m/s saat boost. Penyesuaian pace menurut gap pemain dihapus.

Rintangan memberi penalti bila benar-benar mengenai AI. Jump/ramp memakai tinggi balistik ringan; percobaan jump manual tidak melempar ulang peluang setiap frame. Gagal melewati celah memperlambat tanpa teleport. Kontak antar-AI memberi perlambatan dan cooldown, tanpa memindahkan posisi secara mendadak. Kontak kart pemain/AI mempertahankan aturan engine sebelumnya.

Magnet AI mengumpulkan counter token pribadinya. Token pemain, wallet/progres siswa dan nilai belajar tidak dikurangi/dialihkan oleh AI. Counter AI tidak menghasilkan pasokan atau kecepatan tambahan, dan tidak masuk perhitungan posisi finis.

## Clock, feedback dan penyimpanan

Waktu reaksi, windup, pasokan, expiry, charge, cooldown, buff, jump dan event memakai clock simulasi. Selama pause/soal/feedback/countdown, tidak ada keputusan atau serangan baru; seluruh state membeku. HUD memberi satu pesan pemakaian/hit/blok dekat (65 m) selama 2,2 dtk simulasi dan satu indikator ancaman pemain. SFX lembut memakai graph/limiter PATCH 2 yang sama, bukan loop/aset baru; menu, musik, mute dan Reduced Effects tetap bekerja. Setiap AI aktif hanya menambah maksimal satu draw ring mesh yang sudah ada (320 segitiga), tanpa mesh/buffer/GLB baru.

Hasil balapan menambahkan `aiSummary` opsional untuk audit; format bank, jawaban dan skor tidak berubah. Akademik tetap benar ÷ jumlah soal ×100. Inventori AI/pemain hanya per balapan, tanpa save/resume mid-race yang memang belum disediakan baseline. Bank, profil, progres, ghost dan hasil belajar tetap tersimpan lokal.

## Pengujian

- `simulation-results.json`: 216 balapan engine berpasangan dan 108 kasus penyelesaian; 12 seed, tiga stage, tiga kesulitan. Memeriksa frekuensi buff, hit pemain/AI, pertahanan, kontak, limit pasokan, cooldown, interval serangan pemain, kecepatan/perpindahan dan stall.
- `personality-tests.json`: 16.000 kesempatan serangan identik serta ancaman pertahanan identik; guard akses inventori pemain dan isi asesmen.
- `ai-tests.json`: sembilan buff kontekstual, supply, windup, pembatalan target, player hit, immunity, pantulan, cooldown, expiry, sensor, token, freeze, cap dan collision kart.
- `smart-ui-tests.json`: renderer/UI nyata desktop/HP, Oli mengenai pemain, Perisai menahan proyektil, clock quiz/resume, feed/warning, layout dan WebGL.
- `buff-tests.json`: regresi PATCH 3 termasuk 81 pasangan buff pemain; `core-test-results.json`: CSV/JSON, jumlah soal, Grand Prix, jump/drift, ghost, skor dan progres.
- `test-results.json`, `ui-tests.json`, `persistence-tests.json`, `stage-audio-tests.json`, `export-tests.json`, `offline-test-results.json`: 14 pembalap, kemudi A/D/sentuh, garasi/close-up, quiz, dua slot/overflow, save/reload hasil aktual, tiga arena, audio dan ekspor guru offline.
- `scope-tests.json`: membalik lima hook hingga HTML asal identik dan memeriksa 1.690 berkas historis. `unchanged-renders.json`: pixel 14 model pada pose/cahaya tetap identik, plus Kucing low dan kendaraan saja. Data GLB/avatar/audio dan ketiga stage tetap utuh.

## Build dan distribusi

Dari root repository:

```sh
python visual-upgrade/patch4-smart-ai/source/assemble.py
node visual-upgrade/patch4-smart-ai/source/test_ai.cjs
node visual-upgrade/patch4-smart-ai/source/test_personalities.cjs
node visual-upgrade/patch4-smart-ai/source/benchmark.cjs
python visual-upgrade/patch4-smart-ai/source/report.py
python visual-upgrade/patch4-smart-ai/source/verify_scope.py
```

Jalankan browser suites di `source/` dengan server root repository port 8000, Chromium `/usr/bin/chromium` dan Playwright seperti path dalam script; lalu `python visual-upgrade/patch4-smart-ai/source/package.py`. Paket hanya dibuat setelah laporan wajib lolos. HTML membaca semua aset tertanam; tidak ada CDN atau file pendukung saat dimainkan. Metrik terukur ada dalam `release-metrics.json`.

## Batas bukti

Benchmark menggunakan controller referensi, bukan siswa SMP; hasil win-rate tidak boleh ditafsirkan sebagai peluang menang manusia. Santai masih lebih sering menyentuh rintangan daripada baseline, Sedang hampir setara, dan Menantang menunjukkan pengurangan kontak. Penyelesaian AI-only tidak memutar ulang collision item penuh; hasil balapan engine sebenarnya disimpan terpisah. AI tetap memakai gerak parametris lintasan, bukan simulasi drift/gamepad penuh seperti pemain.

Offline diuji dengan jaringan browser dimatikan dan HTML lokal dipenuhi sebagai dokumen utama, tanpa permintaan aset jaringan. Cloud memblokir `file://`; membuka ZIP hasil ekstraksi di perangkat fisik belum diuji. Tidak mengklaim FPS, HP/speaker fisik, uji kelas SMP, seluruh Grand Prix manual atau video. Pemilihan model GPT sesi tidak dapat diubah melalui tool repository; tidak mengklaim perpindahan model yang tidak dapat diverifikasi.
