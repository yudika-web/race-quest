# BlokRaya — 6F / Stage 9 Bali: Rice Terrace Rush

Baseline lokal dan remote terverifikasi `6cd35f0a5d005c56754a7167c1efeb36861bd3c1` (Yogyakarta), branch `dev/race-quest-cat-sport-visual-upgrade`. [HTML mandiri](../blokraya-stage9-bali.html). Hanya Bali dibuat; tidak mengubah index.html, merge/deployment atau mengerjakan Bromo/6G.

## Bentuk arena

Jalur pedesaan **fiktif 777,24m**, 16 waypoint, 550 segmen tertutup, tikungan lebar dan pergantian elevasi. Ketinggian jalan maksimum 5,70m, grade maksimum 8,86%, empat batu/kayu obstacle ringan, satu ramp u=0,82 dan tanpa gap. Start/finish, envelope jalan, collider ±6,2m, fisika, AI dan mekanisme balapan lama dipakai tanpa perubahan.

Dua bentang sawah dibangun sebagai ribbon berkontur melengkung dengan **enam dan empat tingkat**. Setiap tingkat mempunyai tanah penahan, pematang, saluran air dan rumpun padi tiga bilah sederhana. Total 784 rumpun dibatch; bukan ratusan draw call terpisah. Bank samping dan apron belakang menutup perbedaan ketinggian. Tiga bukit low-poly, kelapa/pohon tropis, semak dan batu melengkapi landscape. Bale wisata beratap limas, bangku, plaza kecil, tangga dan dua tiang gerbang batu orisinal menjadi arsitektur pendukung.

Evaluasi render awal dilanjutkan pemeriksaan tinggi: pijakan kelapa pada teras kini menggunakan indeks spasial segitiga permukaan yang benar-benar dikirim ke GPU, bukan asumsi bidang datar. Sampel ketinggian dan seluruh akar/anchor diuji terhadap permukaan aktual. Framing thumbnail gameplay dipilih pada ruas yang memperlihatkan sawah dari kamera balapan; kamera balapan game sendiri tidak diubah.

Sky gradient, awan blocky dan haze lama digunakan dengan palet siang hijau-biru. Tidak ada shader langit/point light baru. Air irigasi memakai shader air dan clock simulasi lama; dekorasi lainnya statis. Lookup permukaan CPU, buffer dan tekstur milik Bali dilepas ketika berpindah arena. Transisi Yogyakarta malam → Bali siang menghapus resource malam dan memulihkan piksel siang persis.

Sumber editable: [builder](source/rice-terraces.js), [lintasan](track.json), [metadata](stages.json), [assembler](source/assemble.py). Memakai helper City/Garden/Forest/Sentarum tanpa menyalin engine. Blender tersedia tetapi geometri prosedural JavaScript dipilih untuk reusable mesh ringan; tidak ada GLB atau file Blender environment baru yang diperlukan.

**Batas representasi:** tidak ada foto Bali terlampir; akses referensi web ditolak proxy 403. Sawah, bale dan gerbang adalah interpretasi stylized orisinal, bukan rekonstruksi geografis/arsitektur yang terverifikasi. Tidak menggunakan prasasti, lambang ritual atau nama situs sakral. [Catatan referensi](reference-notes.md).

## Integrasi dan perlindungan

ID `bali` tetap dari katalog Prompt 5. Sembilan arena tersedia; **Bromo tetap Segera Hadir** dan ditolak saat pembuatan Track/Session/start race. Kalbar Klasik tetap tiga arena awal; Nusantara belum aktif hingga Bromo siap. Tidak menambahkan cup sementara sembilan arena.

Terintegrasi ke kartu stage dengan render asli, pengaturan guru, renderer, minimap, empat Smart AI, sembilan buff/dua slot, hasil akademik, `stageProgress.bali`, ghost, replay dan reload. Tidak menyisipkan profil/token/unlock QA ke distribusi. Semua storage key, PIN Guru, bank soal, aturan ketuntasan/nilai dan gameplay tetap.

[Scope](scope-tests.json): assembly dapat dibalik persis ke baseline. **2.373 file historis, 30 payload script dan 16 thumbnail lama** byte-identik. [24 perbandingan piksel](unchanged-renders.json) mencakup 14 pasangan, Cat low, mobil Cat saja serta delapan world lama setelah memasuki/keluar Bali. Hasil lama tidak dibangun ulang.

## Hasil uji

| Pemeriksaan | Hasil |
|---|---|
| [Physics](physics-tests.json) | 18 balapan reference-driver; 18 kasus seluruh empat AI finis, tiga kesulitan × enam seed. Rute tersambung/tidak bersilangan; collision, jump/landing, drift, sembilan buff, freeze, save/ghost |
| [Item/AI](item-tests.json) | 11 pemeriksaan inventori terbatas, target pemain/AI, telegraph, cooldown/charges, perlindungan chain-hit dan clock |
| [Renderer](world-tests.json) | 108 sampel: 12 posisi × 3 kualitas × 3 cuaca; clearance dan cleanup semua transisi lama; tidak ada error GL/JS |
| [Permukaan](surface-tests.json) | Anchor objek dibandingkan dengan segitiga ground/shoulder/teras/bank/bukit yang diunggah, toleransi 12cm |
| [Teras/clock](terrain-tests.json) | 30 tinggi sawah, tingkat naik, freeze piksel pause/soal, transisi malam/siang dan pelepasan shader |
| [Browser](browser-tests.json) | 27 pemeriksaan menu, guru/PIN, balapan, A/D, soal/buff, hasil/ekspor, progres, ghost, replay/reload; sentuh aktual via CDP pada 390×844 dan 844×390 |
| [Offline/ekspor](offline-tests.json) | 28 pemeriksaan dengan jaringan browser dimatikan, tanpa request aset HTTP/CDN; ekspor guru tidak membawa verifier/salt PIN |
| [Smoke rilis](release-smoke.json) | HTML final dibuka dari server lokal, Mode Siswa masuk arena Bali; SHA dicatat |
| [file://](direct-file-tests.json) | Benar-benar dicoba, diblokir administrator browser cloud. Belum terbukti lewat skema ini pada perangkat target |

UI kuis/finish menggunakan fixture posisi untuk mempercepat uji browser; bukan klaim balapan manual penuh. Completion lintasan diuji terpisah melalui driver simulasi dan AI sebenarnya. Tidak mengklaim seluruh Grand Prix manual, FPS/HP fisik, frame time atau benchmark memori.

Screenshot render asli: [overview](screenshots/overview.png), [sawah](screenshots/rice-terraces.png), [bale](screenshots/bale-wisata.png), [gameplay](screenshots/gameplay.png), [tikungan](screenshots/terrace-corner.png), [ramp](screenshots/ramp.png), [desktop](screenshots/race-desktop.png), HP [portrait](screenshots/race-390x844.png)/[landscape](screenshots/race-844x390.png). Menu [sebelum](screenshots/before-menu.png)/[sesudah](screenshots/after-menu.png). Baseline belum mempunyai world Bali playable sehingga tidak ada render before-world palsu; before yang sah adalah kartu Segera Hadir. [Laporan perbandingan](comparison-report.json).

## Ukuran dan rendering

HTML **24.764.231 byte**, naik **57.329 byte**, sisa **235.769 byte** terhadap target 25 MB desimal. Dua thumbnail WebP 640×400 berukuran 12.738 dan 20.922 byte. Sumber pertumbuhan: builder/track/metadata ringkas serta dua thumbnail base64; tidak menggandakan model, poster atau engine lama.

Lingkungan: **36.988 segitiga**, **22 batch warna / 18 batch shadow**, satu tekstur papan kecil; ground dua segitiga. Material bersama per warna, air tidak masuk shadow pass. Seluruh scene termasuk actor, fitur dan HUD terkait dirender dengan culling native: high-clear 102–216 draw warna, 28–72 draw depth; low-clear 88–201 draw warna, tanpa depth shadow. Ini penghitung drawPrimitive aktual pada 12 posisi, bukan FPS atau total biaya GPU. Dua draw gradient/cloud native terpisah dicatat di metrik. LOD actor, quality/shadow/cloud lama dipertahankan; geometri sawah ringan tetap sama pada semua kualitas.

[Metrik aset](asset-metrics.json), [aktivasi](activation.json), [ukuran/hash ZIP final](release-metrics.json). ZIP playable memuat HTML yang sama, tanpa server wajib atau loader fetch aset eksternal. ZIP review memuat sumber, screenshot, thumbnail dan laporan. Hash final ZIP review disimpan di repo; arsip tidak dapat membawa hash final dirinya sendiri.

## Build ulang

Perlu checkout baseline yang memuat HTML Yogyakarta dan helper sebelumnya. Python/Pillow, Node/Playwright/Chromium tersedia di cloud. Sesuaikan path runtime pada browser.cjs untuk mesin lain. Server statis localhost port 8000 hanya harness pengembangan. Paling banyak dua browser WebGL berat bersamaan.

```sh
python visual-upgrade/stage9-bali/source/assemble.py
node visual-upgrade/stage9-bali/source/capture.cjs
python visual-upgrade/stage9-bali/source/thumbnails.py
python visual-upgrade/stage9-bali/source/assemble.py
node visual-upgrade/stage9-bali/source/test_physics.cjs
node visual-upgrade/stage9-bali/source/test_items.cjs
node visual-upgrade/stage9-bali/source/test_world.cjs
node visual-upgrade/stage9-bali/source/test_surfaces.cjs
node visual-upgrade/stage9-bali/source/test_terraces.cjs
node visual-upgrade/stage9-bali/source/test_browser.cjs
node visual-upgrade/stage9-bali/source/test_offline.cjs
node visual-upgrade/stage9-bali/source/test_render_parity.cjs
node visual-upgrade/stage9-bali/source/capture_comparison.cjs
python visual-upgrade/stage9-bali/source/verify_scope.py
python visual-upgrade/stage9-bali/source/assemble.py --release
node visual-upgrade/stage9-bali/source/test_release.cjs
node visual-upgrade/stage9-bali/source/test_file.cjs
python visual-upgrade/stage9-bali/source/package.py
```

Kandidat tinggal di /tmp/blokraya-6f/candidate.html. Assembler `--release` hanya menerbitkan HTML/metadata available setelah laporan wajib lolos; kandidat/rilis byte-identik. Paket review sumber prosedural memerlukan checkout baseline, bukan paket authoring engine mandiri.
