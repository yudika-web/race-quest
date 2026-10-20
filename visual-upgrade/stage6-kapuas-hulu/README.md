# BlokRaya — 6C / Stage 6 Kapuas Hulu: Sentarum Lake Circuit

Baseline HEAD lokal/remote `2055c4d7b441d67b06b485e70b8f960af658152b` (Sintang), branch `dev/race-quest-cat-sport-visual-upgrade`. Distribusi: [HTML mandiri](../blokraya-stage6-kapuas-hulu.html). Hanya Kapuas Hulu dibangun; tidak mengubah `index.html`, merge, deployment atau mengerjakan 6D.

## Arena dan desain

Lintasan wisata **fiktif 836,70 m**, 16 waypoint dan 550 segmen tertutup, elevasi jembatan hingga **3 m**, kemiringan maksimum **5,63%**, empat obstacle batu/kayu dan satu ramp pada u=0,71. Tanpa celah jalan. Lebar jalan, collider, physics, start/finish, jalur AI dan mekanisme balap darat dipertahankan. Bentuk rute berbeda dari lima arena sebelumnya; tidak menambahkan mekanisme berenang.

Perairan biru kehijauan, kelompok pohon rawa blocky dengan akar/tiang ke dasar danau, jalan bertiang dan boardwalk kayu mengikuti elevasi, pondok pengamatan, dermaga terbuka, kano dekoratif dan rumpun tumbuhan air. Siluet pohon jauh menyatu dengan haze; sistem gradient langit dan awan baseline dipertahankan dengan palet sejuk. Semua dekorasi baru statis dan tidak menambah clock waktu nyata, sehingga tidak ada animasi tambahan yang berjalan saat soal/pause.

Evaluasi render awal menemukan bahu jalan hijau terlalu lebar. Bahu tersebut diganti menjadi dek sempit agar air terlihat langsung di samping lintasan; hutan rawa diperkuat dengan kelompok pohon. Pemeriksaan vertex juga menemukan tikungan awal terlalu ketat bagi pagar; waypoint awal diperbaiki, kemudian tes rute, AI dan clearance diulang. Sambungan boardwalk–pondok dihitung dari batas persegi dek agar tidak menggantung dengan celah.

Blender tersedia tetapi tidak dibutuhkan untuk prosedural ini. Sumber editable adalah [lake.js](source/lake.js) dan [track.json](track.json). Builder memakai helper batching/bevel/atap dari City/Garden yang sudah ada, tanpa menyalin mesin game atau membangun ulang GLB lama. Tidak ada tekstur langit/aset eksternal baru; satu label canvas kecil dan dua thumbnail WebP dari renderer.

**Batas akurasi:** lanskap merupakan interpretasi stylized Danau Sentarum, bukan rekonstruksi geografis/ekologis. Referensi web ditolak 403, tanpa foto khusus yang dilampirkan. Pondok/dermaga adalah desain wisata generik; tidak diklaim arsitektur lokal terverifikasi. [Catatan referensi](reference-notes.md).

## Integrasi dan perlindungan

ID baru tetap **`kapuas_hulu`** dari katalog Prompt 5, terpisah dari **`kapuas`** milik Mempawah. Enam arena tersedia: `kampung`, `kapuas`, `hutan`, `sambas`, `sintang`, `kapuas_hulu`. Bengkayang, Yogyakarta, Bali dan Bromo masih Segera Hadir dan ditolak oleh Track/Session/start race. Kalbar Klasik tetap tiga arena awal. Nusantara memuat urutan sepuluh arena, dengan Kapuas Hulu sebagai ronde keenam; belum dapat dijalankan sampai empat arena lain tersedia.

Terhubung ke kartu dan preview render, pengaturan guru, Track/Session/renderer, minimap, AI pemain/lawan, sembilan buff, inventori dua slot, ghost, hasil belajar dan `stageProgress.kapuas_hulu`. Profil, unlock, token, bank soal, hasil, audio, HUD, PIN dan kunci penyimpanan tidak diganti. Data/token/unlock QA tidak disisipkan pada distribusi.

Core, renderer dasar, GLB/aset, builder lama, AI, buff, fisika, kuis/penilaian, audio/VFX, HUD, PIN/mode dan loading/poster tetap byte-identik. Script tambahan `sentarumStageVisuals` menerapkan track, world, groundAt dan sky khusus ID Kapuas Hulu; arena lain mendelegasikan ke fungsi lama. [Scope](scope-tests.json) membuktikan assembly dapat dibalik persis ke baseline: **2.170 file historis**, **24 payload** serta **10 thumbnail lama** tidak berubah. [Render terlindungi](unchanged-renders.json): 21 kasus pixel-identik pada kamera/pose/waktu tetap, mencakup 14 pasangan, Cat low, mobil Cat saja dan kelima world lama setelah masuk/keluar Sentarum.

`assemble.py` membuat kandidat uji; hanya `--release` yang mengaktifkan metadata sumber dan menulis HTML distribusi setelah laporan wajib serta thumbnail aktual tersedia. [Aktivasi](activation.json) mencatat baseline belum tersedia, enam stage rilis dan kesamaan byte kandidat/rilis.

## Build ulang

Dari root checkout yang menyertakan HTML baseline Sintang. Server statis internal port 8000 hanya untuk harness pengembangan; tidak ditambahkan sebagai kebutuhan game. Python/Pillow, Node, Playwright dan Chromium sudah tersedia di lingkungan ini; sesuaikan path Playwright/Chromium di `browser.cjs` pada mesin lain. Jalankan paling banyak dua browser WebGL berat bersamaan.

```sh
python visual-upgrade/stage6-kapuas-hulu/source/assemble.py
node visual-upgrade/stage6-kapuas-hulu/source/capture.cjs
python visual-upgrade/stage6-kapuas-hulu/source/thumbnails.py
python visual-upgrade/stage6-kapuas-hulu/source/assemble.py
node visual-upgrade/stage6-kapuas-hulu/source/test_physics.cjs
node visual-upgrade/stage6-kapuas-hulu/source/test_items.cjs
node visual-upgrade/stage6-kapuas-hulu/source/test_surfaces.cjs
node visual-upgrade/stage6-kapuas-hulu/source/test_world.cjs
node visual-upgrade/stage6-kapuas-hulu/source/test_browser.cjs
node visual-upgrade/stage6-kapuas-hulu/source/test_offline.cjs
node visual-upgrade/stage6-kapuas-hulu/source/test_render_parity.cjs
node visual-upgrade/stage6-kapuas-hulu/source/capture_comparison.cjs
python visual-upgrade/stage6-kapuas-hulu/source/verify_scope.py
python visual-upgrade/stage6-kapuas-hulu/source/assemble.py --release
node visual-upgrade/stage6-kapuas-hulu/source/test_file.cjs
node visual-upgrade/stage6-kapuas-hulu/source/test_release.cjs
python visual-upgrade/stage6-kapuas-hulu/source/package.py
```

[Sumber assembler](source/assemble.py), [metadata](stages.json), [capture](source/capture.cjs), [thumbnail](source/thumbnails.py), [metrik](source/report.py), [paket](source/package.py). Artefak sementara kandidat `/tmp/blokraya-6c/candidate.html` identik dengan rilis yang diuji. Unit harness memakai adapter stub hanya untuk logika; world aktual diuji lewat browser. Distribusi tidak memerlukan dependensi pengembangan.

## Pengujian terarah

| Laporan | Hasil |
|---|---|
| [Physics](physics-tests.json) | 7 kelompok: enam world tersedia, empat diblokir, GP klasik/Nusantara, lima konfigurasi + 350 langkah/session lama identik, rute tertutup tanpa overlap, 18 balapan penuh driver referensi, 18 completion AI, collision/border, drift/jump/landing, sembilan buff, freeze/progres/ghost. |
| [Item](item-tests.json) | 11 kelompok stok terbatas, 9 buff, target pemain/AI, cooldown/charge, refleksi/grip, projectile/oli, immunity, radar, freeze dan collision. |
| [Permukaan](surface-tests.json) | 152 anchor terhadap segitiga dasar danau/bahu aktual, toleransi 12 cm. Vertex kayu memverifikasi basis tiang/akar mencapai dasar -3,5m; ujung beam akar miring boleh tertanam ≤30cm. Kano dekoratif berada pada waterline. |
| [World](world-tests.json) | 108 sampel (12 posisi × 3 kualitas × 3 cuaca), tanpa error WebGL; vertex struktur minimum 7,504m dari centerline, di luar collider ±6,2m; resource dilepas pada transisi ke semua lima arena lama, rebuild stabil. |
| [Browser](browser-tests.json) | 27 cek: loading 3 detik, mode/PIN Guru, kartu/thumbnail, siswa, 4 AI, A/D, pause/soal, hadiah & E, hasil JSON/progres/ghost/reload/replay; desktop 1366×768 dan HP emulasi 390×844/844×390 dengan touch press CDP. |
| [Offline](offline-tests.json) | 28 cek dengan jaringan mati: PIN, ekspor guru tanpa salt/verifier, aset/poster tidak diduplikasi, race/quiz/buff/save, HTML ekspor dibuka kembali pada konteks baru, 6 world, tanpa request HTTP/CDN aset. |
| [Scope](scope-tests.json) dan [render parity](unchanged-renders.json) | File/aset/kode terdahulu terlindungi; 21 kasus render identik. |
| [Perbandingan](comparison-report.json) | Kartu Kapuas Hulu baseline Segera Hadir dibanding kartu tersedia dengan thumbnail aktual, viewport setara. Tidak membuat screenshot world “sebelum” palsu, karena world belum ada pada baseline. |
| [file://](direct-file-tests.json) | Navigasi langsung benar-benar dicoba, ditolak `ERR_BLOCKED_BY_ADMINISTRATOR` oleh browser cloud. Tidak diklaim lolos. |

Semua 18 balapan referensi selesai, dengan skor akademik 80% (empat benar dari lima soal) tanpa pengaruh posisi. Semua 72 AI pada 18 kasus completion mencapai finish, stall maksimum 0 s; rerata waktu simulasi Santai **56,63s**, Sedang **43,23s**, Menantang **42,17s**. Ini hasil simulasi, bukan waktu manusia atau FPS.

Browser UI memakai fixture posisi di gate/finish untuk alur terarah; lintasan penuh dibuktikan oleh simulasi terpisah. GP seluruh ronde tidak dimainkan manual ulang karena aturan dan script tidak berubah; ketersediaan/urutan cup diperiksa. Tidak mengklaim audit ulang seluruh bank soal atau pengujian HP fisik. Tidak ada error JS/WebGL pada alur/sampel yang diuji.

[Smoke rilis final](release-smoke.json) membuka kembali Mode Siswa dan arena Kapuas Hulu pada SHA HTML final. [Pemeriksaan whitespace](final-whitespace-check.json) mencatat penghapusan dua spasi kosong sesudah rangkaian uji; tidak ada perubahan statement/aset.

## Screenshot dan metrik

[Overview](screenshots/overview.png) · [Danau/pondok](screenshots/sentarum-lake.png) · [Dermaga](screenshots/timber-jetty.png) · [Hutan rawa](screenshots/swamp-forest.png) · [Gameplay](screenshots/gameplay.png) · [Tikungan](screenshots/lake-corner.png) · [Boardwalk](screenshots/boardwalk.png) · [Ramp](screenshots/ramp.png).

Menu [sebelum](screenshots/before-menu.png) / [sesudah](screenshots/after-menu.png); [kartu sebelum](screenshots/before-unavailable-card.png) / [sesudah](screenshots/after-available-card.png). Menu HP [portrait](screenshots/menu-390x844.png), [landscape](screenshots/menu-844x390.png). Balapan [desktop](screenshots/race-desktop.png), [HP portrait](screenshots/race-390x844.png), [HP landscape](screenshots/race-844x390.png). [Kuis](screenshots/quiz.png) · [hasil](screenshots/results.png).

Seluruh screenshot berasal dari renderer/UI nyata. Overview memakai kamera atas dan menonaktifkan fog geometri hanya untuk capture agar seluruh rute terbaca; tampilan lain memakai atmosfer game biasa. Tidak mengubah kamera balapan di distribusi.

HTML **24.603.486 byte**, baseline **24.549.503 byte**, pertumbuhan **53.983 byte**, sisa batas 25.000.000 byte **396.514 byte**. Pertumbuhan: script/track/metadata **11.014 byte**, dua thumbnail tertanam **42.969 byte**. Thumbnail WebP mentah total **31.994 byte**. Tidak ada GLB, poster atau audio duplikat.

Batch lingkungan **87.846 segitiga**, **13 colour calls**, **9 shadow batch calls**, satu tekstur label, terrain 2 segitiga. Warna/material bersama; pohon tetap dikelompokkan, bukan per-objek draw. Sampel frame lengkap high: 93–199 colour draws/123.609–172.995 segitiga; low: 79–189 draws/104.858–128.746 segitiga, tanpa depth/shadow pass. Counter ini tidak menghitung dua draw langsung sky gradient/cloud. Rentang lengkap dalam [asset-metrics.json](asset-metrics.json). LOD karakter, bayangan dan awan memakai pengaturan kualitas baseline; batch lingkungan statis sama pada tiap kualitas. FPS, waktu/frame dan konsumsi memori belum diukur.

Distribusi tetap satu HTML dengan semua aset tertanam, dibungkus ZIP playable dan review; [release-metrics.json](release-metrics.json) berisi ukuran/hash/CRC dan kesamaan HTML. Pengujian offline dilakukan dengan jaringan mati dan dokumen lokal disuplai harness di localhost. `file://` diblokir kebijakan cloud; buka langsung pada browser target dan HP fisik masih perlu diverifikasi. Tidak ada CDN, backend, server wajib baru atau paket fetch aset lokal yang diklaim tanpa uji.
