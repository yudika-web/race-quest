# Stage 1 — Pontianak · Jalanan Kota

Hasil siap ditinjau dari baseline Batch 4 `540accc6b340fc023a403ee0b22443fc6f002be1`. Hanya arena Stage 1 diperbarui. Ini interpretasi landmark dan suasana kota Pontianak secara stylized, bukan rekonstruksi lokasi atau skala geografis.

- [HTML mandiri](../race-quest-pro-pontianak-stage1.html)
- [ZIP playable](../../race-quest-pro-pontianak-stage1-playable.zip) — ekstrak, buka HTML di browser dengan WebGL.
- [ZIP review](../../race-quest-pro-pontianak-stage1-review.zip) — HTML, sumber, render, laporan dan pengujian.
- Perbandingan kamera setara: [Khatulistiwa](comparisons/comparison-tugu-khatulistiwa.jpg), [Bambu](comparisons/comparison-tugu-bambu.jpg), [jalanan dan overview](comparisons/comparison-city.jpg).
- Render game dengan antarmuka: [desktop](smoke/race-desktop.png), [HP emulasi](smoke/race-mobile.png), [soal](smoke/quiz-desktop.png).

Jalan aspal gelap, marka putus-putus, zebra cross, trotoar, kanstin putih/arang, lampu jalan, pohon pangkas dalam planter, serta 42 bangunan pastel menggantikan dekorasi pedesaan Stage 1. Dua plaza bertaman berada di luar lintasan. Tugu Khatulistiwa memakai empat tiang gelap, cincin bumi dan panah; Tugu Bambu memakai sebelas batang beruas dengan ujung runcing merah/emas. Tidak ada mekanik landmark, collision baru, atau animasi lingkungan tambahan.

ID penyimpanan Stage 1 tetap `kampung`; hanya nama tampil berubah. Jalur, tanjakan, ramp, rintangan sungguhan, start gate, collider, item dan AI tetap menggunakan data serta engine asli. Tanjakan dipertahankan dan diberi sisi penahan bergaya kota. Nama/data Stage 2–3 tetap asli. Tidak ada perubahan 14 karakter, mobil, harga unlock, bank soal atau data profil awal. `index.html` dan versi online tidak diganti.

## Ukuran dan biaya rendering

HTML **23.362.544 byte (23,36 MB desimal)**; baseline 23.349.280 byte, bertambah **13.264 byte**. Semua 94 aset lama tetap identik, tidak ada GLB/tekstur besar baru atau permintaan CDN.

Lingkungan kota dibuat sebagai geometri prosedural yang dibatch menurut material: **37.853 segitiga**, **19 submission warna**, **14 submission bayangan**. Tiga tekstur lokal kecil dibuat sekali: noise aspal 128² dan dua papan nama 512×128; total dasar RGBA 589.824 byte sebelum mipmap. Jalan/ground/aktor/fitur engine tidak termasuk hitungan geometri kota ini. Trotoar dan marka menerima bayangan tetapi dikeluarkan dari pass caster untuk menghindari artefak permukaan datar. Detail kota tetap sederhana pada semua kualitas; LOD karakter dan kualitas bayangan engine tetap berlaku.

Pada satu frame tetap (`u=.12`, waktu 2 detik, kamera balapan, high), submission mesh warna turun **375 → 213**, segitiga warna **230.013 → 107.910**; submission mesh depth **44 → 24**, segitiga depth **134.439 → 60.648**. Ini hitungan submission renderer pada fixture tertentu, bukan total API draw call termasuk langit/partikel atau pengukuran FPS. Seluruh sampel/kualitas tersedia di [scene-tests.json](scene-tests.json). Tidak ada klaim FPS atau pengujian HP fisik.

## Bukti pengujian

- [Scope/hash](scope-verification.json): 1.296 file historis dan 94 aset tertanam identik. Setelah menghapus lapisan kota dan membalik satu label nama, isi HTML kembali byte-identik dengan Batch 4. Engine, pemuatan GLB, kamera dan clock animasi tidak diedit.
- [Render karakter terlindungi](unchanged-renders.json): 18 kasus persis sama, mencakup seluruh 14 pasangan, Kucing high/low, kedua mode garasi Kucing dan mobil Kucing saja.
- [Regresi arena](scene-tests.json): 18 render Stage 2–3 identik piksel (dua stage × tiga posisi × high/medium/low). Sembilan render Stage 1 berubah sesuai target. Semua pemeriksaan WebGL dan console lulus. Footprint dekorasi dijaga di luar lintasan. Saat berpindah stage, 59 buffer dan tiga tekstur kota dibebaskan; rebuild tidak menambah resource milik kota.
- [UI desktop/sentuh](test-results.json): bank soal, seluruh model, avatar, A/D kiri/kanan, jump/landing, pause/resume, soal yang membekukan pemain/AI/clock, jawaban benar, penggunaan buff, low LOD, serta preview HP tanpa tumpang tindih lulus.
- [Core](core-test-results.json): persistensi materi/jumlah soal, round trip CSV, AI bertingkat, ketuntasan/retry/tiga ronde Grand Prix secara unit, drift/jump/item/buff, hasil belajar, ghost dan progres lulus.
- [Offline](offline-test-results.json): jaringan browser dinonaktifkan, hanya dokumen utama dipasok dari byte lokal, tanpa permintaan aset HTTP. `file://` langsung diblokir kebijakan browser cloud, sehingga jalur itu belum diverifikasi di lingkungan ini.
- [Ekspor Ruang Guru](export-tests.json): ekspor aktual, hash seluruh payload, muat ulang tanpa jaringan, close-up/ekspresi, mulai balapan serta pembangunan kedua landmark lulus.
- [Kamera pembanding](capture-report.json): tujuh sudut sebelum–sesudah dengan matriks view/projection dan resolusi identik. Render memakai RaceRenderer sebenarnya; kamera hero/overview hanya fixture dokumentasi, kamera balapan distribusi tidak diubah.

Batas: pengujian browser cloud Chromium/SwiftShader dan emulasi sentuh 390×844, bukan perangkat HP fisik. Tidak melakukan seluruh Grand Prix manual. Pengujian lintasan menggunakan posisi/seed terkendali untuk menjangkau fitur secara cepat. Pemeriksaan visual tidak menjamin setiap kombinasi sudut kamera dan lintasan telah dimainkan manual.

## Sumber dan build ulang

Tidak memerlukan Blender atau GLB lingkungan tambahan: geometri blocky dibangun langsung melalui batch renderer yang sudah ada agar HTML tetap ringan dan offline. Sumber editable berada di [source/city.js](source/city.js); assembler menyisipkan satu lapisan visual setelah RaceScenery, tanpa menyalin engine ke sumber baru.

Dari root repository, dengan baseline Batch 4 tersedia:

```sh
python3 visual-upgrade/stage1-pontianak/source/assemble.py
python3 visual-upgrade/stage1-pontianak/source/verify_scope.py
node visual-upgrade/stage1-pontianak/source/test_core.cjs
python3 -m http.server 8000 --bind 127.0.0.1
```

Dengan server berjalan, jalankan `node .../source/test_game.cjs`, `test_scene.cjs`, `test_unchanged_render.cjs`, dan `test_export.cjs`. Pengujian memakai suite Batch 1 melalui adapter kecil; historical suite tidak diedit. Playwright tersedia pada path runtime cloud di skrip; untuk mesin lain sesuaikan resolusi paket dan executable Chromium. Screenshot: `node .../source/capture.cjs`, kemudian `python3 .../source/make_comparisons.py` (Pillow), lalu `python3 .../source/package.py`.

Tahap ini berhenti pada Stage 1 untuk tinjauan. Stage 2–3 belum didesain ulang. Tidak ada merge atau deployment.
