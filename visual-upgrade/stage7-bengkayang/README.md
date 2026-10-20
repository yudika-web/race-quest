# BlokRaya — 6D / Stage 7 Bengkayang: Waterfall Adventure

Baseline terverifikasi lokal/remote **`d95fb920c781b408f04b95ee479c616cb58c4f4b`** (Sentarum), branch `dev/race-quest-cat-sport-visual-upgrade`. Distribusi [HTML mandiri](../blokraya-stage7-bengkayang.html). Hanya Bengkayang dibangun; tidak merge, deployment, mengubah `index.html` atau mengerjakan 6E.

## Arena baru

Rute wisata **fiktif 801,04 m**, 16 waypoint dan 550 segmen tertutup, variasi tikungan, elevasi hingga **5,20 m**, kemiringan maksimum **10,19%**, empat obstacle batu/kayu, satu ramp u=0,74 dan tanpa gap jalan. Jalan, collider ±6,2m, ruang lajur dan physics memakai engine lama. Tidak memakai ulang rute Sentarum atau menyamarkan world lama dengan nama baru.

Air terjun lebar terinspirasi Riam Merasap menjadi landmark utama: tebing berbidang batu, tirai air terang sekitar 26 unit game (bukan ukuran landmark nyata), aliran hulu, kolam buih, sungai berbatu dan dua penyeberangan jalan dengan tiang serta pagar jembatan. Dek pandang dengan bangku dan jalur pendek menjadi landmark pendukung generik. Hutan blocky berkelompok, pakis, batu berlumut, lampu jalur dan plateau berhutan melengkapi rute. Gradient langit, awan blocky dan haze lama dipertahankan dengan palet Bengkayang yang sejuk.

Evaluasi render menemukan elevasi dasar landmark mengikuti puncak plateau; basis tebing/air diperbaiki agar tersambung ke kolam. Facet batu dan aliran air kemudian disesuaikan agar batu tidak menembus tirai. Pemeriksaan permukaan menemukan satu pohon mengambang di transisi tanah–jembatan; anchor dekorasi kini memakai perpotongan segitiga bahu yang benar-benar dirender melalui indeks spasial, ditambah interpolasi terrain aktual. Tabel CPU ini dilepas ketika keluar arena. Tidak mengubah fisika kendaraan.

Tirai air, foam dan dekorasi statis; gelombang sungai memakai shader ringan dan clock simulasi yang sudah ada. Tidak menambahkan timer waktu nyata, sistem cuaca, partikel tak terbatas atau shader baru. Blender tersedia, tetapi builder prosedural JavaScript lebih sesuai untuk komponen ini. Sumber editable [waterfall.js](source/waterfall.js) dan [track.json](track.json) memakai ulang helper batching/bevel/atap dan vegetasi City/Garden/Sintang serta penggantian mesh Sentarum. GLB lama tidak dibangun ulang.

**Batas akurasi:** hanya interpretasi stylized, bukan rekonstruksi geografis/geologis/ekologis. Referensi web ditolak 403, tanpa foto Riam Merasap terlampir. Bangunan, spesies tanaman dan dimensi tidak diklaim akurat. [Catatan referensi](reference-notes.md).

## Integrasi dan perlindungan

ID **`bengkayang`** sesuai katalog Prompt 5. Tujuh arena tersedia: `kampung`, `kapuas`, `hutan`, `sambas`, `sintang`, `kapuas_hulu`, `bengkayang`. Yogyakarta, Bali dan Bromo tetap Segera Hadir dan tidak dapat dibuka. Kalbar Klasik tetap tiga arena awal; Nusantara menyertakan Bengkayang sebagai ronde ketujuh, tetapi belum aktif sampai tiga world lain tersedia.

Kartu/thumbnail render, pengaturan guru, Track/Session, renderer, AI, buff, inventori, minimap, hasil belajar, progres `stageProgress.bengkayang` dan ghost terhubung ke arena baru. Tidak mengubah nilai akademik, persentase ketuntasan, aturan item/AI, kontrol, audio/VFX atau skema penyimpanan. Profil, token, unlock, bank soal, PIN Guru, poster/loading 3 detik, HUD dan preferensi lama dipertahankan. Tidak ada data/token/unlock QA dalam HTML distribusi.

Penambahan hanya script scoped `waterfallStageVisuals`, track JSON, entri metadata Bengkayang dan dua thumbnail. Arena lain mendelegasikan world/sky/groundAt ke implementasi lama. [Scope](scope-tests.json) membuktikan assembly dapat dibalik persis ke baseline: **2.237 file historis**, **26 payload** dan **12 thumbnail lama** tetap identik. [Perbandingan render](unchanged-renders.json) menunjukkan **22 kasus pixel-identik** pada kamera/pose/waktu tetap: 14 pasangan, Cat low, mobil Cat saja serta enam world lama setelah masuk/keluar Bengkayang.

Kandidat diuji terlebih dahulu. `assemble.py --release` baru menulis HTML distribusi dan metadata tersedia setelah laporan wajib lolos serta thumbnail aktual ada. [Aktivasi](activation.json) mencatat status awal belum tersedia, tujuh arena rilis, dan byte kandidat/rilis identik. [Smoke final](release-smoke.json) membuka lagi Mode Siswa serta world Bengkayang dan mencatat SHA HTML yang dipaketkan.

## Build dan sumber

Dari root checkout yang memuat HTML baseline Sentarum. Server statis internal port 8000 hanya untuk harness pengembangan. Node/Playwright/Chromium serta Python/Pillow sudah tersedia di cloud; sesuaikan path runtime pada `browser.cjs` untuk mesin lain. Maksimal dua browser WebGL berat bersamaan.

```sh
python visual-upgrade/stage7-bengkayang/source/assemble.py
node visual-upgrade/stage7-bengkayang/source/capture.cjs
python visual-upgrade/stage7-bengkayang/source/thumbnails.py
python visual-upgrade/stage7-bengkayang/source/assemble.py
node visual-upgrade/stage7-bengkayang/source/test_physics.cjs
node visual-upgrade/stage7-bengkayang/source/test_items.cjs
node visual-upgrade/stage7-bengkayang/source/test_surfaces.cjs
node visual-upgrade/stage7-bengkayang/source/test_world.cjs
node visual-upgrade/stage7-bengkayang/source/test_browser.cjs
node visual-upgrade/stage7-bengkayang/source/test_offline.cjs
node visual-upgrade/stage7-bengkayang/source/test_render_parity.cjs
node visual-upgrade/stage7-bengkayang/source/capture_comparison.cjs
python visual-upgrade/stage7-bengkayang/source/verify_scope.py
python visual-upgrade/stage7-bengkayang/source/assemble.py --release
node visual-upgrade/stage7-bengkayang/source/test_file.cjs
node visual-upgrade/stage7-bengkayang/source/test_release.cjs
python visual-upgrade/stage7-bengkayang/source/package.py
```

[Builder](source/waterfall.js) · [track](track.json) · [metadata sepuluh arena](stages.json) · [assembler](source/assemble.py) · [capture](source/capture.cjs) · [thumbnail](source/thumbnails.py) · [metrik](source/report.py) · [paket](source/package.py). Kandidat sementara `/tmp/blokraya-6d/candidate.html` identik dengan rilis. Unit test memakai stub adapter hanya untuk logika; world sebenarnya diuji di browser. Tidak menduplikasi keseluruhan mesin; dependensi build tidak diperlukan saat bermain.

## Pengujian

| Laporan | Hasil |
|---|---|
| [Physics](physics-tests.json) | 7 kelompok: 7 stage tersedia/3 diblokir, GP klasik dan Nusantara, enam konfigurasi/simulasi lama identik selama 350 langkah/session, rute tertutup tanpa overlap, 18 balapan driver referensi dan 18 completion AI, collision/border, drift/jump/landing, 9 buff, freeze/progres/ghost. |
| [Item](item-tests.json) | 11 kelompok stok terbatas, semua buff, target pemain/AI, cooldown/charge, refleksi/grip, projectile/oli, immunity, radar, freeze dan collision. |
| [Permukaan](surface-tests.json) | 194 anchor terhadap perpotongan vertikal segitiga terrain/bahu aktual, toleransi 12 cm; indeks tinggi baru mengatasi transisi jembatan. |
| [World](world-tests.json) | 108 sampel (12 posisi × 3 kualitas × 3 cuaca), tanpa error WebGL. Vertex struktur minimum 7,573m dari centerline; buffer/tekstur dilepas pada transisi ke enam arena lama; lookup CPU dilepas; rebuild stabil. |
| [Browser](browser-tests.json) | 27 cek loading, mode/PIN, kartu/thumbnail/konfigurasi guru, siswa dan 4 AI, A/D, pause/soal, hadiah/E, hasil JSON/progres/ghost/reload/replay. Desktop 1366×768, HP emulasi 390×844 dan 844×390; touch press via CDP. |
| [Offline](offline-tests.json) | 28 cek jaringan mati: PIN, ekspor guru tanpa salt/verifier, aset/poster tidak diduplikasi, start/quiz/buff/save, HTML ekspor pada konteks baru, 7 world tersedia dan tanpa request HTTP/CDN aset. |
| [Render parity](unchanged-renders.json) / [scope](scope-tests.json) | 22 render dan seluruh payload/aset/file historis terlindungi. |
| [Perbandingan kartu](comparison-report.json) | Kartu baseline Segera Hadir dibanding kartu tersedia ber-thumbnail render, viewport setara. Tidak membuat world “sebelum” palsu karena world belum ada pada baseline. |
| [file://](direct-file-tests.json) | Navigasi langsung benar-benar dicoba; ditolak `ERR_BLOCKED_BY_ADMINISTRATOR` oleh browser cloud. Tidak diklaim lolos. |

Semua 18 balapan referensi selesai dengan skor akademik tetap 80% dari 4 benar/5 soal. Semua 72 AI pada 18 kasus completion mencapai finish, stall maksimum 0 s. Rerata waktu simulasi Santai **54,00s**, Sedang **41,66s**, Menantang **39,81s**; ini bukan waktu pemain manusia atau FPS. Pengujian UI memakai fixture gate/finish untuk alur terarah; lintasan penuh diuji oleh simulasi terpisah. Seluruh GP tidak dimainkan manual ulang; urutan/ketersediaan dan script terlindungi diperiksa. HP fisik, frame time dan konsumsi memori belum diukur.

## Screenshot dan ukuran

[Overview](screenshots/overview.png) · [Riam Merasap stylized](screenshots/riam-merasap.png) · [Dek pandang](screenshots/forest-overlook.png) · [Jembatan sungai](screenshots/river-bridge.png) · [Gameplay menuju air terjun](screenshots/waterfall-approach.png) · [Gameplay jembatan](screenshots/gameplay.png) · [Tikungan](screenshots/forest-corner.png) · [Ramp](screenshots/ramp.png).

Menu [sebelum](screenshots/before-menu.png) / [sesudah](screenshots/after-menu.png); kartu [sebelum](screenshots/before-unavailable-card.png) / [sesudah](screenshots/after-available-card.png). HP menu [portrait](screenshots/menu-390x844.png), [landscape](screenshots/menu-844x390.png). Balapan [desktop](screenshots/race-desktop.png), [portrait](screenshots/race-390x844.png), [landscape](screenshots/race-844x390.png); [kuis](screenshots/quiz.png) dan [hasil](screenshots/results.png).

Semua screenshot adalah render game/UI asli. Overview menggunakan kamera review atas dengan fog geometri dimatikan hanya saat capture agar rute terbaca; screenshot lain memakai atmosfer dan kamera biasa kecuali close-up landmark/dek/jembatan yang memakai kamera review eksplisit. Tidak mengubah kamera balapan distribusi.

HTML **24.658.272 byte**, baseline **24.603.486 byte**, pertumbuhan **54.786 byte**, sisa batas 25.000.000 byte **341.728 byte**. Script/track/metadata menambah **13.851 byte**, thumbnail tertanam **40.935 byte**; WebP mentah total **30.464 byte**. Tidak menambah GLB, audio/poster duplikat, tekstur resolusi besar atau CDN.

Batch lingkungan **60.586 segitiga**, **14 colour calls**, **8 shadow batch calls**, satu tekstur label. Terrain terpisah **18.432 segitiga**. Counter frame lengkap high: 94–204 colour calls/116.669–165.623 segitiga; low: 80–191 calls/97.486–121.376 segitiga, tanpa depth/shadow pass. Counter ini tidak mencakup dua panggilan langsung sky/cloud. Rentang lengkap ada dalam [asset-metrics.json](asset-metrics.json). Batch lingkungan statis sama per kualitas; LOD karakter, bayangan dan awan mengikuti baseline. Tidak mengklaim FPS atau pengujian HP fisik.

[release-metrics.json](release-metrics.json) mencatat ukuran/hash ZIP, CRC dan kesamaan HTML. Distribusi satu HTML mandiri, dibungkus ZIP playable/review. Offline lulus dengan jaringan mati dan dokumen lokal disuplai harness pada localhost. Uji langsung file:// diblokir kebijakan cloud; verifikasi browser target masih diperlukan. Tidak menambahkan server wajib, backend, layanan online atau loader fetch aset lokal.
