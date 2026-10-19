# Stage 3 — Singkawang · Pantai Meriah

Hasil dari baseline Mempawah `53d677c02228118b9933e3aa712b6dc66ce4be4c`. Hanya visual Stage 3, nama tampilnya dan cuaca tema bawaannya diperbarui. Stage 1 Pontianak, Stage 2 Mempawah dan seluruh pasangan karakter/kendaraan tetap utuh.

- **[ZIP playable](../../race-quest-pro-singkawang-stage3-playable.zip)** — ekstrak lalu buka `race-quest-pro-singkawang-stage3.html`.
- [HTML mandiri](../race-quest-pro-singkawang-stage3.html) · [ZIP review](../../race-quest-pro-singkawang-stage3-review.zip).
- Pada menu Mulai, pilih **Singkawang · Pantai Meriah**. Pilih cuaca **Sesuai tema** atau **Cerah** untuk suasana pantai cerah. Pilihan Hujan dan Kabut tetap tersedia.
- Before–after: [Tugu Naga](comparisons/comparison-naga.jpg), [Imlek](comparisons/comparison-imlek.jpg), [pantai](comparisons/comparison-beach.jpg), [detail naga dan gap](comparisons/comparison-detail-gap.jpg).
- Balapan dengan UI: [desktop](smoke/race-desktop.png), [HP emulasi](smoke/race-mobile.png), [panel soal](smoke/quiz-desktop.png).

## Perubahan visual

Jalan beraspal dengan kanstin merah-putih, pasir, laut turquoise dengan tepian buih, promenade, pagar rendah, bangku, kelapa dengan buah, payung/kursi pantai dan kios wisata menggantikan dekorasi hutan Stage 3. Terrain visual baru mengikuti envelope rute asli sebagai pantai dengan teluk/laguna, tanpa menjadi collider baru. Elevasi jalan dan lereng penghubung lintasan tetap asli.

**Tugu Naga**: monumen merah–emas dengan alas bertingkat, tubuh naga berpenampang oktagonal yang melilit pilar, ekor mengecil, sisik grafis, punggung merah, empat kaki/cakar, kepala ekspresif, moncong, mata/highlight, rahang, gigi, tanduk bercabang, kumis, janggut dan aksen awan. Setelah render awal, lilitan dan bentuk kepala dikoreksi agar lebih terbaca; posisi mata serta papan nama diperbaiki melalui inspeksi close-up.

**Ornamen Imlek**: gapura pedestrian bertingkat dengan ujung atap terangkat, papan selamat datang, lampion dan dekor merah–emas. Gapura berada di luar lintasan, bukan rintangan tambahan. Lampion digunakan pada 28 tiang tepi promenade, gapura, kios dan plaza, tanpa efek lampu dinamis berat. Ada 38 penempatan kelapa, 10 payung/kursi pantai, empat kios dan 14 bangku promenade. Seluruh desain adalah interpretasi stylized dari referensi pengguna, bukan rekonstruksi geografis/historis berskala.

## Gameplay dan cuaca

ID stage tetap `hutan`, sehingga pemilihan, penyimpanan, progres dan ghost tetap menggunakan ID yang sama. Seluruh titik rute, panjang, elevasi/tanjakan, obstacle, ramp `.465` dan gap `.48` tetap identik. Promenade dan marka tidak menutup gap. Dekorasi forest/bridge/tunnel generik diganti; hazard, ramp dan start gate sungguhan tetap menggunakan engine asli.

**Cuaca tema Stage 3 berubah dari Kabut ke Cerah** untuk memenuhi arahan pantai cerah. Pengaturan guru yang memilih Hujan atau Kabut secara eksplisit tetap dihormati. Kode handling/cuaca tidak diubah. Pengujian berpasangan membuktikan kondisi Cerah dan Kabut memiliki physics yang sama dalam engine ini; Hujan tetap memakai handling licin asli. Metadata cuaca hasil balapan secara wajar mencatat cuaca yang digunakan.

Tidak ada perubahan bank soal, profil awal, harga unlock, AI, item/buff, drift, jump, Grand Prix, hasil belajar, ghost, audio, renderer karakter, kontrol atau ekspor. Air laut memakai clock simulasi asli; tidak ada clock waktu nyata atau animasi lingkungan baru yang berjalan saat pause/soal.

## Ukuran dan biaya renderer

HTML **23.394.232 byte (23,39 MB desimal)**, bertambah **15.438 byte** dari Mempawah. Tetap di bawah 25.000.000 byte. Semua 94 payload aset lama identik; tanpa CDN, GLB/tekstur besar baru atau permintaan aset jaringan.

Lapisan dekor pantai: **64.076 segitiga**, **26 submission mesh warna**, **13 submission bayangan**. Terrain pantai baru **11.520 segitiga** dan satu submission warna, menggantikan ground lama. Laut memakai satu primitive dan shader air yang sudah tersedia. Tiga tekstur lokal kecil dibuat sekali: aspal 128² serta dua papan nama 512×128; data RGBA dasar 589.824 byte sebelum mipmap. Detail lingkungan tetap sama pada semua kualitas, sementara LOD karakter/kendaraan serta kualitas bayangan tetap memakai sistem asli.

Pada fixture balapan tetap (`u=.12`, high, waktu 2 detik), submission warna **413 → 216**, segitiga warna **262.939 → 143.343**; submission depth **58 → 23**, segitiga depth **171.573 → 84.297**. Perbandingan biaya ini memakai cuaca bawaan masing-masing versi, Kabut/Cerah. Ini hitungan submission mesh renderer, bukan seluruh API draw call termasuk langit/partikel atau pengukuran FPS. Semua sampel/kualitas tersedia di [scene-tests.json](scene-tests.json).

## Bukti pengujian

- [Scope/hash](scope-verification.json): **1.397** file historis dalam `index.html`/`visual-upgrade` identik dengan baseline; seluruh **94 aset** tertanam identik. Menghapus lapisan Stage 3 baru dan membalik hanya nama/cuaca tema Stage 3 menghasilkan HTML baseline byte-identik. Script Stage 1–2, engine, UI, loader GLB, kamera dan clock animasi tidak diedit.
- [Physics berpasangan](physics-comparison.json): **6.000** langkah simulasi baseline/revisi identik pada empat pilihan cuaca (`stage`, `clear`, `fog`, `rain`), termasuk pemain, AI, buff, item, waktu dan catatan. Default lama Kabut dibandingkan default baru Cerah; physics tetap identik. Ramp otomatis dan rescue gap diuji pada keempat pilihan; titik track, hills, obstacle, ramp dan gap juga identik.
- [Render arena](scene-tests.json): **18** frame Stage 1–2 identik piksel (dua stage × tiga posisi × high/medium/low), termasuk setelah berganti dari Stage 3. Sembilan frame Stage 3 berubah sesuai target. Pilihan cuaca Cerah/Hujan/Kabut dirender tanpa error WebGL. Jarak minimum vertex struktur dekorasi dari centerline **8,346 unit**, dibanding jalan setengah 5 dan kanstin sampai 5,5.
- Cleanup GPU: **80 buffer dan tiga tekstur dekor pantai**, serta **enam buffer ground/laut**, dibebaskan saat pindah stage. Stage 1 dan Stage 2 pulih; resource kedua stage juga dibebaskan saat kembali ke pantai. Rebuild memiliki jumlah resource dekor pantai yang sama.
- [Model terlindungi](unchanged-renders.json): **18 kasus** identik, mencakup seluruh 14 pasangan, Kucing high/low, dua mode garasi Kucing dan mobil Kucing saja.
- [UI/gameplay](test-results.json): pemilihan Stage 3 dari UI asli, default Cerah, dua landmark, semua model/avatar, A kiri/D kanan, jump/landing, pause/resume, soal yang membekukan pemain/AI/clock, jawaban benar, penggunaan buff, low LOD, serta layout garasi HP lulus. Kontrol sentuh kiri lulus pada emulasi 390×844. Tidak ada error JavaScript.
- [Core](core-test-results.json): persistensi materi/jumlah soal, CSV round trip, AI bertingkat, Grand Prix/retry/ketuntasan tiga ronde secara unit, drift/jump, soal/buff/item, hasil, ghost dan progres lulus pada target Stage 3.
- [Offline](offline-test-results.json): browser berjaringan nonaktif, hanya HTML utama dipasok dari byte lokal; balapan Stage 3 memuat kedua landmark tanpa permintaan aset HTTP.
- [Ekspor guru](export-tests.json): Stage 3 disimpan melalui Ruang Guru, diekspor melalui download HTML aktual, semua hash aset dan tiga lapisan lingkungan dipertahankan; muat ulang offline, ekspresi/close-up dan kedua landmark dalam balapan lulus.
- [Screenshot](capture-report.json): sembilan pasangan kamera before–after identik matriks view/projection/resolusi. Delapan memakai **Cerah pada kedua versi** untuk membandingkan desain secara adil; satu pasangan tambahan memakai Kabut pada kedua versi. Semua gambar berasal dari RaceRenderer sebenarnya, bukan ilustrasi generatif. Hero/close-up/overview dan posisi dekat gap merupakan fixture dokumentasi; kamera balapan distribusi tidak diedit.

Batas: pengujian Chromium/SwiftShader cloud dan HP emulasi, bukan perangkat fisik. Tidak ada pengukuran FPS atau seluruh Grand Prix manual. `file://` diblokir administrator browser cloud; offline diuji dengan jaringan nonaktif dan byte HTML lokal. Posisi/seed terkontrol digunakan untuk menjangkau kuis/ramp/gap, bukan klaim seluruh kombinasi lintasan dimainkan manual.

## Sumber dan build

Sumber editable: [source/coast.js](source/coast.js). Menggunakan helper geometri/material/palm/roof yang sudah diterima melalui subclass, tanpa mengubah sumber Stage 1 atau Stage 2. Terrain, tubuh naga dan ornamen dibangun prosedural ketika world dibuat; tidak memerlukan Blender atau GLB tambahan.

Dari root checkout dengan hasil Mempawah tersedia:

```sh
python3 visual-upgrade/stage3-singkawang/source/assemble.py
python3 visual-upgrade/stage3-singkawang/source/verify_scope.py
node visual-upgrade/stage3-singkawang/source/test_core.cjs
node visual-upgrade/stage3-singkawang/source/test_physics.cjs
python3 -m http.server 8000 --bind 127.0.0.1
```

Dengan server aktif, jalankan `node .../source/test_game.cjs`, `test_scene.cjs`, `test_unchanged_render.cjs`, `test_export.cjs`. Adapter menggunakan suite Batch 1 yang tidak diedit. Path Playwright/Chromium mengacu pada runtime cloud; sesuaikan pada mesin lain. Screenshot: `node .../source/capture.cjs`, lalu `python3 .../source/make_comparisons.py` (Pillow). Paket: `python3 .../source/package.py`. Sumber dalam ZIP review membutuhkan checkout/baseline untuk build ulang; HTML dalam ZIP playable/review mandiri.

Tidak ada perubahan `index.html` online, merge ke `main` atau deployment.
