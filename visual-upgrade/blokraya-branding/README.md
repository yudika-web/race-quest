# BlokRaya — Balap Edukasi Nusantara

Rebranding dan loading screen dari baseline terbaru `9bd494aa07b08c2bc58755e9577f9c0237f8df6e` (PATCH 4.5 + langit blocky), pada branch `dev/race-quest-cat-sport-visual-upgrade`.

- [HTML offline mandiri](../blokraya-balap-edukasi-nusantara.html)
- [ZIP playable](../../blokraya-balap-edukasi-nusantara-playable.zip): ekstrak, lalu buka HTML.
- [ZIP review: sumber, poster dan bukti pengujian](../../blokraya-balap-edukasi-nusantara-review.zip)

## Branding

Nama dokumen dan empat header menu menjadi **BlokRaya**, dengan subjudul **Balap Edukasi Nusantara**. Banner bengkel 3D dan judul hasil cetak memakai identitas baru. Nama file ekspor guru/hasil/ghost mengikuti BlokRaya; format file tetap kompatibel. Pesan validasi impor menyebut BlokRaya dan RACE QUEST untuk berkas lama. Menu memakai poster pengguna sebagai latar dengan lapisan gelap agar teks/tombol terbaca.

Tidak mengganti ID stage, nama karakter, aturan pembelajaran, identitas bank atau kunci localStorage. `race_quest_flexible_v1_*`, `race_quest_preferences`, `race_quest_hud_v45` dan `race_quest_audio_v1` dipertahankan. Bank, profil, token, unlock, paint, hasil belajar, ghost dan pilihan HUD lama tetap terbaca. File ekspor guru tetap memakai namespace paket baru sebagaimana baseline; rebranding tidak membuat migrasi/reset penyimpanan.

## Poster asli dan optimasi

Dua WebP berasal dari `BlokRaya_Poster_WebP.zip` yang diunggah pengguna. Tidak dibuat ulang, digambar ulang atau diganti. `assets/*-original.webp` menyimpan byte asli; hash dan ukuran tersedia di [poster-metrics.json](poster-metrics.json).

| Orientasi | Asli | Distribusi | Ukuran distribusi |
|---|---|---|---:|
| Landscape | 1672×941 · 368.694 byte | 1440×810 | 262.388 byte |
| Portrait | 941×1672 · 317.504 byte | 900×1599 | 257.380 byte |

Optimasi hanya resize proporsional dan encoding WebP quality 82; selisih rasio paling besar kurang dari satu pixel akibat pembulatan. Total poster distribusi **519.768 byte**, turun dari **686.198 byte**. Masing-masing disematkan sekali di JSON; menu dan loading memakai URI yang sama. Ekspor guru membersihkan URL dinamis di DOM/CSS sehingga payload poster tidak terduplikasi.

## Loading “Memuat...”

Overlay berada sebelum payload aset dan script game. `<picture>` memilih portrait untuk orientasi vertikal dan landscape untuk horizontal; pergantian orientasi tetap bekerja saat loading. `object-fit:contain` menjaga seluruh komposisi poster, tanpa stretching atau crop. Letterbox navy disengaja pada rasio layar berbeda. Indikator berada pada panel terpisah di bawah poster, termasuk safe-area.

- Saat parsing data atau menyiapkan shader/model/world secara sinkron, progress **indeterminate**. Tidak menampilkan persentase unduhan palsu.
- Bila gambar/material masih dimuat, indikator menghitung **gambar selesai / gambar yang sedang ditunggu**, berdasarkan event load/error nyata. Ini jumlah resource, bukan persentase byte atau estimasi seluruh pekerjaan CPU.
- Lifecycle gambar data-URI renderer dihubungkan ke readiness tracker. Loading garasi menunggu pembalap/material dan frame pratinjau; loading arena membangun world, menyiapkan model melalui render pertama, menunggu gambar lalu menampilkan balapan.
- Overlay hilang setelah resource selesai dan kesempatan paint tersedia. Tidak ada durasi minimum atau countdown loading buatan. Mesin balapan tidak berjalan di belakang persiapan arena karena layar masih garasi sampai readiness selesai.
- Gambar dekoratif gagal memakai fallback tekstur yang sudah ada dan tidak membuat infinite loading. Error startup fatal menampilkan tombol **Muat ulang**. Error WebGL tetap memakai pesan/perlindungan tombol Mulai asli.
- Tidak menambah loop animasi, GPU program atau audio. Tracker memakai WeakMap/Set dan melepas promise serta listener setelah load/error. Penanganan ini tidak mengubah simulasi, cooldown atau penilaian.

## Screenshot game sebenarnya

- Loading [desktop 1366×768](screenshots/loading-1366x768.png), [HP portrait 390×844](screenshots/loading-390x844.png), [HP landscape 844×390](screenshots/loading-844x390.png), [tablet portrait](screenshots/loading-768x1024.png).
- Menu [desktop](screenshots/menu-1366x768.png), [HP portrait](screenshots/menu-390x844.png), [HP landscape](screenshots/menu-844x390.png).
- Gameplay [jump](screenshots/live-desktop-air.png), [buff/cooldown](screenshots/live-desktop-cooldown.png), [Pause](screenshots/live-desktop-pause.png), [soal](screenshots/live-desktop-quiz.png).

Untuk memotret overlay startup yang dapat selesai sangat cepat, harness menahan callback boot-ready **hanya dalam browser pengujian**. Poster adalah gambar asli yang dirender UI final; build distribusi tidak memiliki penundaan tersebut.

## Hasil pengujian

[loading-tests.json](loading-tests.json): empat viewport, pilihan poster, rotasi portrait→landscape, object-fit, panel terpisah, overflow, dismiss saat siap, gambar unresolved/resolved dan error, tombol recovery. Semua lulus, tanpa error JavaScript.

[legacy-storage-tests.json](legacy-storage-tests.json): data dibuat menggunakan baseline lama, kemudian dibuka lewat HTML BlokRaya pada origin yang sama. Bank/profil tersimpan tidak ditulis ulang saat menu dibuka; token/XP/progres, pengaturan jumlah soal, unlock, paint dan pilihan HUD dipertahankan.

[controls-tests.json](controls-tests.json): keyboard/touch, dua slot, buff/charge/cooldown, Smart AI, HUD, jump/drift, Pause/soal freeze, jawaban benar/salah, hasil belajar, restart/fullscreen/audio dan penyimpanan. [persistence-tests.json](persistence-tests.json) memeriksa penyimpanan hasil dan pemulihan setelah reload. [stage-audio-tests.json](stage-audio-tests.json) memuat tiga arena dengan renderer/audio dan tanpa error WebGL.

[export-tests.json](export-tests.json): ekspor guru mempertahankan 94 aset lama, enam thumbnail, dua poster baru, sembilan buff, Smart AI dan HUD; setiap poster hanya muncul sekali. HTML ekspor memakai nama BlokRaya dan loading menutup otomatis; dapat memulai Singkawang dalam konteks offline. [offline-test-results.json](offline-test-results.json) memeriksa game distribusi dengan jaringan dimatikan, tanpa permintaan aset HTTP.

[core-test-results.json](core-test-results.json): bank CSV/JSON, tiga stage, GP gating/retry/penyelesaian tiga ronde, asesmen, buff, ghost dan progres. [engine-parity.json](engine-parity.json): **36 balapan lengkap berpasangan**, 3 stage ×3 kesulitan ×4 seed, dibanding baseline langit terbaru. Setiap langkah pemain/AI, inventori, cooldown, proyektil, soal, nilai dan token identik.

[scope-tests.json](scope-tests.json): semua perubahan dibatasi dan dapat dibalik menjadi baseline persis. Shader langit, layout HUD, AI, buff, stage dan material/model dipertahankan; renderer hanya menambahkan pelacakan readiness gambar. Kode core hanya mengganti nama pada pesan validasi ekspor. `index.html`, distribusi lama dan 1.945 berkas historis tetap utuh.

## Ukuran dan batas pengujian

HTML **24.402.739 byte**, naik **700.740 byte** dari baseline. Di bawah **25.000.000 byte**. Pertumbuhan didominasi dua poster yang disematkan sebagai base64; tidak menambahkan CDN atau unduhan aset. Ukuran/hash final serta ZIP dicatat di [release-metrics.json](release-metrics.json).

HP/tablet diuji melalui emulasi Chromium, bukan perangkat fisik. Tidak mengklaim FPS/performa GPU HP. Browser cloud memblokir `file://`; offline diuji dengan byte HTML lokal yang disuplai langsung ke konteks jaringan nonaktif. Grand Prix diuji di engine, bukan seluruh balapan manual. Tidak merge ke main, tidak mengganti `index.html` dan tidak deployment.

## Sumber/build

`source/assemble.py` membaca `race-quest-pro-sky-horizon.html`; tidak menggunakan baseline lama. `loading.html`, `loading.js` dan `branding.css` dapat diedit. Loader dipasang melalui hook terbatas pada startup, renderer dan world preparation. `bounded-changes.json` merekam setiap penggantian. Dua file WebP asli wajib tersedia, builder tidak membuat poster pengganti.

```sh
python visual-upgrade/blokraya-branding/source/assemble.py
python visual-upgrade/blokraya-branding/source/verify_scope.py
python -m http.server 8000
```

Jalankan `node visual-upgrade/blokraya-branding/source/test_loading.cjs`, `test_legacy_storage.cjs`, `test_controls.cjs`, `test_export.cjs`, `test_persistence.cjs`, `test_stages.cjs`, `test_offline.cjs`, `test_core.cjs` dan `test_engine_parity.cjs`. Playwright/Chromium memakai lingkungan sama dengan patch sebelumnya. Tes regresi memakai ulang source PATCH 4.5 melalui `reuse.cjs`; engine tidak diduplikasi. Setelah semua laporan lulus, `python visual-upgrade/blokraya-branding/source/package.py` membuat ZIP dan memverifikasi CRC/hash HTML.
