# BlokRaya — 6G / Stage 10 Bromo: Volcano Challenge

Baseline lokal/remote terverifikasi **`ce295f302c1dbf4fe4b2189ece95b087b9454b6b`** (Bali), branch `dev/race-quest-cat-sport-visual-upgrade`. [HTML mandiri](../blokraya-stage10-bromo.html). Hanya Bromo dibuat. Tidak mengubah index.html, merge/deployment atau memulai pekerjaan lain.

## Arena baru

Jalan balap **fiktif 820,41m**, 16 waypoint dan 550 segmen tertutup. Tikungan lebar diselingi perubahan arah, elevasi maksimum 5,10m, grade maksimum 8,13%, empat obstacle batu serta satu ramp pada u=0,80; tanpa gap. Envelope jalan dan collider ±6,2m, physics, start/finish, jalur AI dan mekanisme obstacle lama dipertahankan. Tidak memakai ulang konfigurasi lintasan/world lama.

Lautan pasir abu-cokelat mengelilingi kawah terbuka beralur vertikal. Mesh terhubung membentuk kaki lereng, bibir tidak rata, dinding dalam dan lantai cekung, bukan kerucut yang ditutup rata. Kerucut pendamping lebih tinggi dan beralur, dinding kaldera setengah lingkaran, empat bukit pasir, basalt/batu dan sedikit rumput kering membedakannya dari arena sebelumnya. Ada dek pandang kayu kecil dan pagar pada tikungan. Papan hanya penunjuk; bentuk gunung/kawah menjadi landmark utama.

Gradient pagi biru-oranye, haze, awan blocky lama, cakram matahari poligonal dan empat kelompok kepulan blocky statis. Tidak ada efek lava atau klaim erupsi aktual. Tidak menambah program sky, point light dinamis, tekstur besar atau clock waktu nyata. Kepulan statis sengaja sederhana; tidak menggunakan simulasi volumetrik. Air generik dinonaktifkan hanya untuk Bromo.

Evaluasi render awal diikuti koreksi terarah: garis warna lereng dibuat mengikuti alur vertikal agar tidak menyerupai lapisan cincin; kepulan diperjelas; kedua ujung dinding kaldera ditutup. Pijakan diperiksa terhadap triangle permukaan yang benar-benar diunggah. Pengujian memisahkan prefix geometri terrain dari batu dekoratif yang berbagi material, agar puncak batu tidak keliru dianggap tanah.

Sumber editable: [builder prosedural](source/volcano.js), [lintasan](track.json), [metadata](stages.json), [assembler](source/assemble.py). Memakai kembali helper Garden/Forest/Sentarum tanpa menggandakan engine. Blender tersedia; JavaScript prosedural dipilih untuk geometri ringan yang dapat dibangun ulang. Tidak membutuhkan GLB atau file Blender environment baru.

**Batas representasi:** tidak ada foto Bromo terlampir, akses web referensi ditolak proxy403. Siluet/geologi merupakan interpretasi stylized; proporsi, orientasi serta jarak belum diverifikasi dengan foto/topografi. Bukan jalur balap geografis pada kawasan lindung sebenarnya. [Catatan referensi](reference-notes.md).

## Sepuluh arena dan Grand Prix

ID `bromo` tetap dari katalog Prompt 5. Seluruh sepuluh arena kini mempunyai adapter lintasan dan environment nyata. Grand Prix Nusantara menjadi tersedia melalui registry lama setelah Bromo memenuhi gate rilis; tidak mengubah kode poin, ketuntasan atau urutan cup. **Kalbar Klasik tetap tiga arena awal.** Tidak menambah cup sementara atau unlock/token QA.

Kartu memakai thumbnail hasil render. Pengaturan guru, empat Smart AI, sembilan buff/dua slot, hasil akademik, `stageProgress.bromo`, ghost, replay dan reload diuji. Kunci penyimpanan, PIN lokal, bank soal, profil/token/unlock, kontrol, audio/VFX, HUD, poster/loading dan fitur pendidikan tetap.

[Scope](scope-tests.json): assembly dapat dibalik persis menjadi baseline. **2.441 file historis, 32 payload script dan 18 thumbnail lama** byte-identik. [25 render pixel-identik](unchanged-renders.json): seluruh 14 pasangan, Cat low, mobil Cat saja, serta sembilan world lama setelah masuk/keluar Bromo. Aset sebelumnya tidak dibangun ulang.

## Pengujian

| Pemeriksaan | Hasil |
|---|---|
| [Physics](physics-tests.json) | 18 balapan reference-driver + 18 kasus seluruh empat AI finis, tiga kesulitan × enam seed; collision, border, jump/landing, drift, seluruh buff, pause/soal, progres/ghost |
| [Grand Prix unit/integrasi](grand-prix-tests.json) | Sepuluh adapter wajib nyata; penghapusan satu adapter memblokir cup. Classic identik baseline. Sepuluh ronde, retry ketuntasan ronde terakhir, rollback poin, klasemen/juara; driver menyelesaikan lap seluruh sepuluh track |
| [Grand Prix browser](grand-prix-browser-tests.json) | 81 pemeriksaan UI: sepuluh world nyata, soal/freeze/buff di tiap ronde, ronde sepuluh gagal/ulang/lolos, rekap sepuluh ronde, hasil/ekspor/progres/ghost serta PIN setelah reload |
| [Item/AI](item-tests.json) | 11 pemeriksaan suplai terbatas, target pemain, telegraph, cooldown/charges, shield/reflect/grip, collision, perlindungan chain-hit dan clock |
| [World](world-tests.json) | 108 sampel: 12 posisi × 3 kualitas × 3 cuaca; clearance, cleanup/rebuild/transisi sembilan arena lama; tanpa error WebGL/JS |
| [Permukaan](surface-tests.json) | Anchor dibandingkan dengan mesh ground/shoulder/gunung/kaldera/bukit pasir yang benar-benar diunggah; toleransi 12cm |
| [Kawah/clock](terrain-tests.json) | Cekungan >18m di bawah bibir; 90 centroid triangle cocok dengan lookup; piksel pause/soal membeku; sunrise → malam → Bromo memulihkan render identik dan melepas shader malam |
| [Browser](browser-tests.json) | 27 pemeriksaan menu, PIN/guru, balapan, A/D, soal/buff, hasil/ekspor, progres/ghost/replay/reload dan kontrol sentuh CDP 390×844 / 844×390 |
| [Offline/ekspor](offline-tests.json) | 28 pemeriksaan pada context jaringan dimatikan; tidak ada request aset HTTP/CDN. Ekspor guru tidak menyertakan salt/verifier PIN |
| [Smoke rilis](release-smoke.json) | HTML final dibuka dan masuk Bromo melalui Mode Siswa; SHA dicatat |
| [file://](direct-file-tests.json) | Navigasi benar-benar dicoba, diblokir administrator browser cloud; perlu verifikasi browser pengguna |

Uji UI memakai fixture posisi ke gerbang kuis/finish untuk mempercepat transisi. Bukan klaim sepuluh balapan Grand Prix manual penuh. Completion rute diuji terpisah dengan driver simulasi dan Smart AI sebenarnya. Tidak mengklaim FPS/HP fisik, frame time atau benchmark memori.

Screenshot asli: [overview](screenshots/overview.png), [kawah](screenshots/bromo-crater.png), [kaldera](screenshots/caldera-landscape.png), [dek pandang](screenshots/sand-sea-viewpoint.png), [gameplay](screenshots/gameplay.png), [tikungan](screenshots/sand-corner.png), [ramp](screenshots/ramp.png), [desktop](screenshots/race-desktop.png), HP [portrait](screenshots/race-390x844.png)/[landscape](screenshots/race-844x390.png), [rekap Nusantara](screenshots/grand-prix-complete.png). Overview memakai kamera khusus dan fog dimatikan untuk inspeksi struktur; gameplay menggunakan kamera/fog normal.

Menu [sebelum](screenshots/before-menu.png)/[sesudah](screenshots/after-menu.png) membandingkan kartu belum tersedia dengan kartu aktif hasil render. Baseline tidak mempunyai world Bromo playable; tidak membuat render before-world palsu. [Laporan perbandingan](comparison-report.json).

## Ukuran dan rendering

HTML **24.802.112 byte**, bertambah **37.881 byte**, sisa **197.888 byte** terhadap 25 MB desimal. WebP thumbnail 640×400: landmark 3.824 byte, gameplay 15.312 byte. Pertumbuhan hanya builder/track/metadata ringkas dan dua thumbnail base64; tanpa duplikasi GLB, poster atau engine.

Lingkungan **15.326 segitiga**, **19 batch warna / 14 batch shadow**, satu tekstur papan kecil; ground dua segitiga. Material bersama per warna dan geometri batched; kepulan/matahari/paint tidak menambah shadow caster. High-clear seluruh scene termasuk actor: 99–213 draw warna, 24–68 draw depth; low-clear 85–195 draw warna tanpa shadow depth. Ini penghitung drawPrimitive aktual pada 12 posisi, bukan FPS/biaya GPU; dua draw gradient/cloud native terpisah. LOD actor dan pengaturan quality/shadow/cloud lama tetap; terrain ringan memakai geometri sama pada tiap kualitas.

[Metrik aset](asset-metrics.json), [aktivasi](activation.json), [status 10 arena](stage-status.json), [metrik/hash ZIP](release-metrics.json). ZIP playable berisi HTML identik, tanpa server wajib atau fetch aset lokal. ZIP review berisi sumber, screenshot, thumbnail dan laporan. Hash final ZIP review dicatat di repo; arsip tidak dapat memuat hash final dirinya sendiri.

## Build ulang

Perlu checkout baseline Bali beserta helper sebelumnya. Python/Pillow, Node/Playwright/Chromium tersedia di cloud; sesuaikan path runtime pada browser.cjs untuk mesin lain. Server localhost8000 hanya harness pengembangan. Jalankan paling banyak dua browser WebGL berat bersamaan.

```sh
python visual-upgrade/stage10-bromo/source/assemble.py
node visual-upgrade/stage10-bromo/source/capture.cjs
python visual-upgrade/stage10-bromo/source/thumbnails.py
python visual-upgrade/stage10-bromo/source/assemble.py
node visual-upgrade/stage10-bromo/source/test_physics.cjs
node visual-upgrade/stage10-bromo/source/test_items.cjs
node visual-upgrade/stage10-bromo/source/test_grand_prix.cjs
node visual-upgrade/stage10-bromo/source/test_world.cjs
node visual-upgrade/stage10-bromo/source/test_surfaces.cjs
node visual-upgrade/stage10-bromo/source/test_volcano.cjs
node visual-upgrade/stage10-bromo/source/test_browser.cjs
node visual-upgrade/stage10-bromo/source/test_gp_browser.cjs
node visual-upgrade/stage10-bromo/source/test_offline.cjs
node visual-upgrade/stage10-bromo/source/test_render_parity.cjs
node visual-upgrade/stage10-bromo/source/capture_comparison.cjs
python visual-upgrade/stage10-bromo/source/verify_scope.py
python visual-upgrade/stage10-bromo/source/assemble.py --release
node visual-upgrade/stage10-bromo/source/test_release.cjs
node visual-upgrade/stage10-bromo/source/test_file.cjs
python visual-upgrade/stage10-bromo/source/package.py
```

Kandidat berada di /tmp/blokraya-6g/candidate.html. Hanya `--release` menulis distribusi dan metadata available setelah semua gate wajib termasuk uji GP lolos. Kandidat/rilis byte-identik. Review ZIP adalah paket sumber tambahan yang memerlukan checkout baseline, bukan authoring engine mandiri.
