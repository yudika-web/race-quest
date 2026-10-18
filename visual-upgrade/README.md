# RACE QUEST — peningkatan visual Kucing / Sport

Buka **race-quest-visual-upgrade.html**. Semua aset sudah tertanam; tidak membutuhkan CDN, unduhan model, paket JavaScript, atau backend. Untuk server lokal opsional: `python3 -m http.server 8000` dari folder ini. Berkas asli tersimpan sebagai `original.html`; `../index.html` tidak diubah.

## Hasil

- `race-quest-visual-upgrade.html`: game lengkap dengan pasangan Kucing–Sport baru, termasuk garasi dan lintasan. Tiga belas karakter lain dan aset mereka dipertahankan persis.
- `race-quest-cat-sport.glb`: model gabungan detail, dengan hierarki pivot tubuh, pengemudi, mata, telinga, ekor, kemudi roda depan, dan putaran roda.
- `race-quest-cat-sport-low.glb`: geometri ringan untuk kualitas rendah dan Kucing yang berjarak lebih dari 24 unit dari kamera. LOD mengurangi segitiga; jumlah batch material tetap sama.
- `source/race-quest-cat-sport.blend`: sumber Blender 4.3, material dapat diedit, pengelompokan bagian, kamera studio dan lampu untuk render. Scene editor memakai Z-up; ekspor game memakai Y-up.
- `source/build_cat.py`: membangun geometri melalui Blender Python, memanggang modifier dan mengekspor GLB 2.0 sesuai parser game. `source/assemble.py` menanamkan kedua GLB dan perubahan renderer ke salinan HTML asli.
- `comparisons/`: tangkapan WebGL nyata, tanpa retouch model. `comparison-sheet.jpg` memuat empat sudut. `comparison-game-race.jpg` memakai kamera balapan asli dengan posisi dan seed yang disamakan. Tangkapan lain mencatat garasi desktop/HP, balapan, dan soal.

## Desain dan integrasi

Referensi PNG diterjemahkan menjadi bulu jingga dengan pola tabby yang mengikuti permukaan, moncong krem, mata amber berlapis, telinga berongga dan ekor melengkung. Bodi mobil dibuat dari permukaan kap melengkung dan spatbor khusus, dengan warna sian, garis putih, emblem kaki, kokpit terbuka, jok, setir, lampu depan/belakang, intake, splitter, diffuser, knalpot, spoiler, serta ban berprofil dan pelek berjari-jari.

Material membedakan cat, kaca asap, logam, karet, bulu dan lampu. Tambahan pantulan studio dibatasi pada material model baru; kaca tetap opak untuk menghindari persoalan sorting transparansi pada renderer sederhana. Variasi permukaan bulu bersifat ringan, bukan simulasi rambut. Garasi memperoleh latar studio, lantai dan bayangan kontak; sasaran kamera HP disesuaikan agar model tidak tertutup panel keterangan.

Pusat roda tetap **X ±0,59; Y 0,205; Z depan 0,48 / belakang −0,56**, dengan radius ban nominal **0,205**. Titik asal model dan kode tabrakan tetap sama. Tangan diletakkan pada sisi rim setir; ayunan tambahan pengemudi dibatasi agar kontak tidak terlepas. Suspensi, telinga, ekor dan kedipan memakai waktu simulasi, sehingga berhenti bersama permainan. Putaran dan belokan roda memakai jarak serta input kemudi yang sudah ada.

Animasi bersifat prosedural di renderer game. GLB menyimpan geometri dan pivot; tidak berisi klip skeletal/skin. Untuk reproduksi animasi di aplikasi lain diperlukan pengaitan pivot atau baking tersendiri. Source Blender menyediakan bagian yang dapat diedit, bukan rig deformasi produksi penuh.

## Ukuran dan beban

| Ukuran | Asli | Revisi |
|---|---:|---:|
| HTML | 17.997.235 byte | 19.051.488 byte (+5,86%) |
| GLB Kucing–Sport | 348.496 byte | 767.256 byte; LOD 369.692 byte |
| Segitiga model | 15.256 | 37.445; LOD 15.656 |
| Batch gambar model, satu pass warna | 30 | 44 |

Angka batch tidak mencakup arena, partikel, atau pass bayangan. Model dekat lebih mahal daripada model lama; LOD ringan mendekati jumlah segitiga lama. `render-metrics.json` menyimpan hitungan instrumentasi dan waktu wall-time cloud. GPU timer tidak tersedia; angka waktu tersebut hanya observasi pengiriman perintah WebGL dan tidak cukup untuk menyimpulkan biaya GPU atau FPS perangkat nyata. Pengujian HP memakai emulasi viewport dan sentuhan, bukan perangkat fisik.

## Validasi

- Browser Chromium/WebGL: halaman utama, bank soal Ruang Guru, model di garasi, 14 model dapat dimuat, masuk balapan, A ke kiri/D ke kanan, jump, jeda, soal, buff jawaban benar, penggunaan buff, dan kelanjutan permainan.
- Snapshot pemain, AI dan waktu renderer identik selama jeda dan saat soal terbuka setelah frame transisi selesai.
- Desktop 1440×1000 dan HP 390×844: kontrol sentuh kiri bekerja, pratinjau dan tombol garasi tidak bertumpuk; tangkapan disertakan.
- Browser dengan jaringan dimatikan: HTML dipasok langsung dari byte lokal, balapan berjalan tanpa permintaan HTTP aset dan tanpa error JavaScript. Pembukaan `file://` secara langsung diblokir administrator browser cloud, sehingga jalur itu tidak diklaim lolos pengujian.
- Regresi inti: materi/jumlah soal dan JSON round trip, ekspor/impor CSV, tiga stage, konfigurasi AI bertingkat, aturan mastery/retry Grand Prix, drift, jump, pembekuan kuis, buff, hasil, ghost dan progres.
- Logika aturan/UI/scenery serta seluruh aset asli selain GLB Kucing dibandingkan identik dengan sumber asli. Pemeriksaan sintaks JavaScript lolos. Kedua GLB berhasil diimpor kembali oleh Blender.

Smoke browser memperpendek hitungan mundur dan memosisikan pemain mendekati gerbang soal sebagai fixture. Ini menguji event/game/UI sebenarnya, bukan menyelesaikan semua putaran secara manual. Grand Prix dan hasil/ghost/progres diuji pada inti simulasi; tidak semua variasi stage, perangkat, impor file melalui UI, atau seluruh Grand Prix dijalankan manual di browser.

Hasil terperinci: `test-results.json`, `core-test-results.json`, `offline-test-results.json`, `glb-validation.json`, `asset-metrics.json`, dan `render-metrics.json`.

## Reproduksi

1. Blender 4.3+: `blender -b --python source/build_cat.py`.
2. Python 3: `python3 source/assemble.py`.
3. Server statis di folder induk proyek untuk menjalankan skrip browser (URL pengujian memakai `/visual-upgrade/...`).
4. Node: `node source/test_core.cjs`, `node source/test_game.cjs`. Playwright disediakan runtime cloud; sesuaikan lokasi `require` dan executable Chromium bila dijalankan di mesin lain.

Satu pasangan ini menjadi acuan bentuk, palet, material, pivot dan LOD untuk peningkatan 13 karakter berikutnya. Karakter lain belum didesain ulang pada tahap ini.
