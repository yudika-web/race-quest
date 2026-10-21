# BlokRaya PRO — PATCH 8B

Alur siswa: **Nama/Kelas → Kesulitan → Mode → Arena/Cuaca (Bebas saja) → Garasi → Mulai Balapan**. Grand Prix langsung menuju garasi setelah memilih cup. Wizard tiga tahap lama diganti pada sumber yang sama; tidak ditumpuk dengan wizard tambahan.

Baseline terverifikasi: `83c2213f6b6791bfd2ad9f962a356a912bdf5b49` (PATCH 8A), pada branch `dev/race-quest-cat-sport-visual-upgrade`.

- [HTML mandiri](../blokraya-patch8b-student-flow.html).
- [ZIP playable](../../blokraya-patch8b-playable.zip) · [ZIP review + sumber + screenshot](../../blokraya-patch8b-review.zip).
- [Galeri screenshot per tahap dan sebelum–sesudah](review.html). Buka galeri dari ZIP review untuk tampilan HTML lokal; gambar juga tersedia langsung di [screenshots](screenshots/).
- [Metrik](metrics.json) · [Hash HTML dan ZIP](release-metrics.json).

## Perubahan

- Nama dan kelas wajib, dipangkas dari spasi, serta dikonfirmasi satu kali. Navigasi Kembali mempertahankan isian.
- Kartu kesulitan menggunakan nilai engine `easy`, `normal`, `hard`. Tidak ada perubahan parameter AI.
- Kartu Bebas/Grand Prix dan empat cup memakai status serta urutan registry yang sama. Cup yang belum memenuhi status tidak dapat dipilih.
- Arena memakai satu preview render aktual, panah melingkar, daftar ringkas 13 arena, indikator posisi, keyboard saat carousel fokus, serta swipe sentuh. Panah berada di luar gambar landmark. Kesulitan arena dihitung dari track aktual menggunakan helper lama.
- Empat pilihan cuaca memakai nilai engine `stage`, `clear`, `rain`, `fog`. State arena/cuaca Bebas disimpan terpisah dari cup. Grand Prix mengambil arena pertama cup dan cuaca guru/default, termasuk ketika sebelumnya memilih Hujan pada arena lain.
- Bank soal, putaran dan gas otomatis tetap tersedia di **Pengaturan Lanjutan**, tertutup secara default. Jumlah soal tetap read-only dan konfigurasi final menggunakan jumlah soal guru.
- Garasi tetap menggunakan 14 model, warna, unlock, studio, rotasi/zoom, serta preview penuh/close-up. Enam karakter per halaman ditata tiga kolom; panah tidak perlu dicari melalui scroll. Ringkasan identitas dan konfigurasi berada pada caption preview. Kembali membuka keputusan terakhir yang relevan.
- Bantuan tetap tersedia melalui tombol **Bantuan**, tanpa popup otomatis ketika pertama masuk garasi. Validasi dilakukan lagi sebelum balapan; guard menolak start ganda.

State wizard hanya sementara dalam sesi aplikasi. Tidak ada kunci penyimpanan baru atau migrasi data. Memuat ulang kembali meminta konfirmasi identitas; bank soal, hasil, progres, unlock, ghost dan PIN lama tetap disimpan oleh mekanisme semula.

## Hasil uji

| Laporan | Hasil aktual |
|---|---|
| [Navigasi](navigation-tests.json) | 61 pemeriksaan: kedua alur sampai balapan, validasi, Back, state Bebas/GP, seluruh panah arena, empat cup, status tidak tersedia melalui fixture registry, pagination karakter dan start ganda |
| [Layout](layout-tests.json) | 42 pemeriksaan tampilan pada 1920×1080, 1366×768, 390×844, 844×390, 768×1024, 1024×768; footer tetap terlihat, satu panel/modal aktif, tanpa overflow horizontal atau overlap head/body/footer |
| [Semua metadata carousel](carousel-layout-tests.json) | 39 kasus: 13 arena pada desktop, portrait dan landscape pendek; judul/landmark berada di dalam kartu, panah di luar gambar, tanpa scroll horizontal |
| [Grand Prix](grand-prix-browser-tests.json) | 235 pemeriksaan; 29 ronde tuntas dan empat percobaan gagal/ulang pada empat cup. Termasuk cuaca guru Kabut, default per stage, ketuntasan, rollback poin retry, rekap, hasil JSON, progres/ghost, reload dan login PIN |
| [Offline/ekspor](offline-tests.json) | 28 pemeriksaan dalam konteks jaringan dinonaktifkan; PIN, ekspor guru, game hasil ekspor, kontrol A, pause, freeze kuis, hadiah buff, E, hasil akademik; **0 permintaan aset HTTP/CDN** |
| [Kompatibilitas](compatibility-tests.json) | 13 pemeriksaan: token/XP/unlock, bank soal dan kelas bank, progres lama, PIN, ekspor setelah wizard/garasi terpasang, tidak ada identitas siswa/PIN atau ID wizard ganda dalam ekspor |
| [Perlindungan sumber](scope-tests.json) | 50 payload script/data tetap identik; engine/AI/buff/physics/HUD/audio/PIN/loading, track, world, GP dan aset lama tidak berubah |
| [Render](render-parity-tests.json) | Perbandingan piksel tepat seluruh 13 world dan 14 pasangan model dengan PATCH 8A; tanpa error JavaScript/WebGL |
| [HTTP biasa](release-smoke.json) | Server lokal menyajikan HTML dengan SHA yang sama, lalu Mode Siswa membuka wizard tunggal tanpa intersepsi dokumen |

Pengujian GP memakai fixture posisi pada gerbang soal dan garis finish untuk menguji transisi UI, bukan balapan manual seluruh turnamen. Tidak ada benchmark physics/AI baru karena payload tersebut tidak berubah. Tes offline tetap menjalankan renderer dan alur permainan sebenarnya.

Pada alur utama Bebas dan garasi tidak diperlukan scroll pada enam viewport yang diuji. GP portrait memiliki kelebihan pembulatan 1 px; GP landscape 844×390 menggunakan **49 px scroll lokal**. Accordion lanjutan yang sengaja dibuka dapat memerlukan scroll lokal sampai 269 px pada landscape pendek. Tombol Kembali/Lanjut tetap berada di footer di luar area scroll. Seluruh 39 kasus carousel tidak memerlukan scroll lokal.

HP diuji melalui emulasi viewport/sentuh Chromium, termasuk input swipe CDP. HP fisik, Safari dan FPS perangkat tidak diklaim diuji. Navigasi `file://` ditolak browser cloud dengan `ERR_BLOCKED_BY_ADMINISTRATOR`; pengujian offline memakai konteks jaringan mati dan dokumen lokal yang diintersepsi. HTML tidak memakai fetch aset lokal maupun CDN, dan distribusi tetap satu HTML seperti sebelumnya.

## Ukuran dan performa

- HTML baseline: **24.954.319 byte**.
- HTML PATCH 8B: **24.967.184 byte** (+12.865 byte, sekitar 0,052%). Masih di bawah sasaran 25.000.000 byte.
- Contoh ekspor guru: **25.002.581 byte**; setelah wizard/garasi pernah dipasang: **25.002.647 byte**. Tambahan konfigurasi bank membuat contoh ekspor sekitar 2,6 KB di atas sasaran, tanpa mengurangi aset/fitur.
- Tidak menambah model, tekstur, segitiga, material atau draw call 3D. Aset poster, GLB high/low, avatar dan thumbnail identik.
- Picker grid lama yang tidak lagi digunakan dihapus dari adapter, sehingga thumbnail tidak perlu di-parse dua kali. Form ekspor dikembalikan ke markup awal agar tidak menggandakan avatar atau menyertakan identitas sesi.
- Tidak ada klaim kenaikan FPS atau hasil benchmark HP. Ukuran ZIP dan SHA tercatat di `release-metrics.json`.

## Sumber dan build

- [onboarding.js](source/onboarding.js): state, validasi, kartu, carousel/swipe, ekspor bersih dan ringkasan garasi.
- [onboarding.css](source/onboarding.css): layout responsif, footer tetap dan fallback scroll lokal.
- [assemble.py](source/assemble.py): mengganti adapter lama dan menerapkan integrasi minimum ke aplikasi baseline.
- `stage-ui.js` dan `application.js` dihasilkan assembler untuk review. Edit sumber onboarding/CSS atau transformasi integrasi dalam assembler, lalu build ulang; kedua file keluaran ini bukan input build.

Dari root repository:

```sh
python visual-upgrade/patch8b/source/assemble.py
python -m http.server 8000
```

Pada terminal lain jalankan `node visual-upgrade/patch8b/source/test_navigation.cjs`, lalu `test_layout.cjs`, `test_carousel_layout.cjs`, `test_gp_browser.cjs`, `test_offline.cjs`, `test_compatibility.cjs`, `test_render_parity.cjs`, dan `test_release.cjs`. Browser helper menggunakan Chromium `/usr/bin/chromium` dan Playwright yang tersedia di cloud; `PLAYWRIGHT_MODULE=playwright` dapat digunakan untuk instalasi lokal.

```sh
python visual-upgrade/patch8b/source/test_scope.py
python visual-upgrade/patch8b/source/report.py
python visual-upgrade/patch8b/source/package.py
```

ZIP review menyertakan HTML baseline yang dibutuhkan assembler, sehingga build dapat diulang setelah ekstraksi. Tes perlindungan Git membutuhkan checkout repository beserta commit baseline. Package memverifikasi CRC dan kecocokan byte HTML/sumber dalam ZIP. Hash ZIP final dicatat di repository; hash diri ZIP review tidak dimasukkan ke dalam arsip itu sendiri.

Tidak mengubah `index.html` online, tidak merge ke `main`, tidak deployment, dan tidak membuat podium.
