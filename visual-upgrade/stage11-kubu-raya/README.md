# BlokRaya — 6H / Stage 11 Kubu Raya: Mangrove Extreme Run

Baseline lokal dan remote **`7fdbc485a50c851a9e02ab2b675fbc5603bb9c50`**, setelah Yogyakarta/Bali/Bromo selesai dan sepuluh arena terdaftar. Branch `dev/race-quest-cat-sport-visual-upgrade`. [HTML mandiri](../blokraya-stage11-kubu-raya.html). Hanya Stage11 dibuat; tidak mengubah index.html, merge atau deployment.

## Registrasi dan kompatibilitas

[Metadata](stages.json) berisi **13 ID**, mempertahankan sepuluh entri lama persis. `kubu_raya` playable, `kayong_utara` dan `ketapang` **Segera Hadir**, tanpa config/world palsu. Stage12/13 ditolak oleh Track/Session dan menu tidak mengizinkan masuk. [Cup](cups.json) mempertahankan Kalbar Klasik3 dan Nusantara10. Kalbar Extreme Challenge3 serta Grand Prix Lengkap13 Arena hanya metadata, terblokir hingga kedua world yang hilang benar-benar tersedia.

Tidak mengganti storage key, PIN lokal, bank soal, profil, token/unlock, progres lama atau ghost. Normalizer lama menambahkan tiga entri progres kosong tanpa mengubah entri lama. Nilai akademik tetap berasal dari jawaban; hadiah token lintasan bukan buff dan tidak memengaruhi nilai. Semua aturan item, inventori2 slot, audio/VFX, HUD, kontrol, poster/loading dan ketuntasan lama tetap.

Adapter baru memakai subclass Session **hanya untuk ID Kubu Raya**, menambahkan sensing/hazard/rescue tanpa membangun ulang Smart AI. Session pada sepuluh stage lama meneruskan perilaku ke parent tanpa field tambahan. [Scope](scope-tests.json): **2.528 file historis**, **32 payload script** dan **20 thumbnail lama** byte-identik. Core/renderer/scenery dasar, GLB dan aset lama tidak diedit. Satu fungsi metrik kartu mendapat dua ekspresi tambahan untuk menghitung zona/ramp khusus; input stage lama menghasilkan hitungan yang sama. Katalog stage/cup diperluas, tidak mengganti ID lama.

[26 render pembanding](unchanged-renders.json) persis identik: 14 pasangan, Cat low, mobil Cat saja dan sepuluh world lama setelah masuk/keluar Kubu Raya. Physics setiap stage lama dibandingkan dengan baseline selama350 langkah pada seed/input sama; bank/profil/ghost/settings lama tetap setelah normalisasi, hanya tiga progres kosong baru yang ditambahkan.

## Lintasan dan lingkungan

Sirkuit papan tertutup **886,86m**, 17 waypoint/550 segmen, kurva S dan tikungan dermaga, elevasi maksimum3,80m, grade maksimum7,47%. Deck mengikuti tinggi jalan aktual, pagar/pile terhubung, perairan payau hijau-cokelat di bawahnya, bank lumpur, mangrove berakar cabang, dermaga serta perahu nelayan dekoratif. Mercusuar jauh berdiri pada platform dan tidak menjadi obstacle. Sky gradient, awan blocky, haze dan shader air lama dipakai; tanpa shader berat/point light baru.

Percabangan memakai **dua deck terpisah pada koordinat progres/lateral engine**, bukan graph dua rute independen dengan panjang berbeda. Kiri kontinu/aman; kanan melintasi kanal3m. Pembatas tengah terlihat dan mempunyai collision; jalan utama tidak menutup seluruh lebar dengan dua obstacle bersamaan. Tidak ada keuntungan memotong koordinat progres. Landmark dan perahu tidak ditempatkan pada jalur kendaraan.

Sumber editable [mangrove.js](source/mangrove.js), [extreme.js](source/extreme.js), [track.json](track.json), [assembler](source/assemble.py). Builder menggunakan helper Garden/Sentarum yang telah tersedia. Koordinat khusus bridge/fork/gap dimiliki builder dan adapter physics; jika memindahkannya, ubah kedua sumber secara konsisten dan jalankan tes kontrak zona, bukan hanya mengubah JSON. Blender tersedia; geometri prosedural dipilih agar ringan, tanpa GLB/Blender environment besar baru.

**Batas representasi:** mercusuar merupakan interpretasi orisinal terinspirasi brief Tanjung Intan; warna, bentuk dan proporsi belum diverifikasi. Tidak ada foto khusus terlampir, akses web ditolak proxy403. Rute delta bukan rekonstruksi jalur wisata/aktivitas balap sesungguhnya. [Catatan referensi](reference-notes.md).

## Sepuluh zona tantangan

| Posisi lap | Tantangan | Collider dan respons |
|---|---|---|
| 10% | Batang sebagian jalan | Sweep longitudinal + lateral, slowdown45%, cooldown1s; kanan aman |
| 20% | Tong menggelinding | Silinder low-poly, gerak lateral dan putaran dari elapsed; collider memakai pose yang sama |
| 30% | Jembatan sempit27m | Lebar6,5m, pagar terlihat, pusat kendaraan dibatasi±2,6m dengan slowdown65% saat kontak |
| 41% | Lumpur11m | Zona parsial mempertahankan slip singkat0,25s; efek traksi hilang setelah keluar, Grip membatasi efek |
| 49% | Kanal3,2m | Gap benar pada mesh; ramp bertanda dan impuls asli10,5m/s; gagal menyentuh air memicu rescue |
| 59% | Pintu ayun | Pivot/panel kayu, AABB konservatif mengikuti sudut dan kedalaman panel; sisi kanan tetap aman |
| 68% | Bambu | Rumpun parsial dengan collision/speed penalty dan jalan aman kiri |
| 77% | Peti dermaga | Collider mengikuti volume peti; kanan aman, lompatan cukup tinggi dapat menghindari |
| 85% | Genangan10m | Patch dangkal di atas deck, slip0,12s sementara; kanan aman |
| 94% | Fork risiko/hadiah | Kiri aman, kanan gap3m; +1 token setelah berhasil menyeberang di udara dan mendarat, sekali per lap |

Collider parsial menambahkan footprint kendaraan0,65m. Ketinggian clearance disesuaikan dengan batang/peti/bambu/tong/pintu. Pagar menghentikan kemudi pada deck; pada bagian tanpa pagar, jatuh ke air memicu rescue. Warning ditempatkan35m sebelum pusat zona; untuk jembatan/fork sebelum awal zona. Jarak ke awal bahaya sekitar29,5–36m (≥0,95s pada31m/s), dan khusus kanal35m (1,13s) dengan sign/ramp/pole kuning; fork menyebut kiri aman dan kanan+1. HUD memakai antrean notifikasi lama, collision memanggil feedback obstacle native. Radar kini menyertakan zona aktual dalam45m saat buff aktif.

Lompatan memakai gravitasi26 dan impuls native, bukan teleport atau tambahan kecepatan. Uji actual simulation pada9/12/23m/s dan31m/s dengan Turbo legal berhasil melintasi kanal. Minimal9m/s adalah32,4km/jam; jika terlalu lambat, rescue tersedia. AI tetap memakai empat kepribadian, pace/cap23/31, suplai terbatas dan sembilan buff lama. Adapter menambahkan petunjuk jalur lokal pada rintangan, centering jembatan dan launch gap yang diperlukan. Tidak menambah item tak terbatas atau memindahkan AI maju melewati bahaya.

## Rescue dan clock

Checkpoint aman disimpan di luar zona bahaya, ketika grounded dan dekat tengah deck. Rescue selalu **mundur atau tetap**, maksimal ke posisi aman sebelumnya; untuk kanal dipastikan setidaknya18m sebelum awal agar cukup ruang akselerasi. Kendaraan ditahan **2,4s waktu simulasi**, kemudian bisa melaju kembali. Bukan tambahan elapsed instan yang meloncatkan seluruh timer. Inventory/charge, token dan records akademik dipertahankan. Buff berdurasi tetap berjalan mengikuti waktu simulasi selama menunggu, sehingga dapat kedaluwarsa secara normal.

Fallback mencakup gagal gap, jatuh ke air pada sisi terbuka, state tidak valid dan macet>7s saat berusaha melaju. Berhenti normal dengan rem tidak memicu rescue. Tidak menambah checkpoint soal atau menghapus jawaban sebelumnya; sample ghost dapat merekam gerakan mundur, sesuai validator lama yang mengharuskan waktu monoton tetapi tidak memaksa jarak monoton.

Tong/pintu hanya memakai `Session.elapsed` yang sama dengan renderer.clock, bukan Date/performance timer. Pause/soal membekukan gerak, wait rescue, AI, buff dan seluruh event. Lompatan manual maupun ramp otomatis dapat memperoleh hadiah kanan; tanpa jump sukses tidak ada hadiah. Tidak menambah unlock/profil QA ke distribusi.

## Bukti pengujian

| Laporan | Hasil |
|---|---|
| [Physics/AI](physics-tests.json) | 18 balapan referensi, skor asesmen80% persis;18 kasus seluruh4 AI finis (72 penyelesaian),3 kesulitan×6 seed. Setiap langkah maju AI≤31×dt, tidak ada warp maju; satu AI Santai memakai rescue mundur |
| [Obstacle/rescue](mechanics-tests.json) | Delapan kelompok pemeriksaan: seluruh collider, lane aman,4 kecepatan jump, rescue/token/charge/records, water/stuck/idle, fork satu hadiah, manual jump/radar, Grip dan freeze |
| [Rescue browser](rescue-browser-tests.json) | UI asli: rescue mundur, kedua slot/charge/token/records tetap, pause membekukan wait dan AI, kendaraan kembali melaju setelah penalti terbatas |
| [Renderer](world-tests.json) | 108 frame:12 posisi×3 kualitas×3 cuaca; landmark/prop footprint aman, buffer/texture dilepas pada seluruh10 transisi lama dan count stabil saat rebuild; tanpa error GL/JS |
| [Render bergerak](render-mechanics-tests.json) | Pixel pause/soal identik; dua mesh bergerak berubah hanya saat elapsed berubah; night→Kubu Raya memulihkan frame identik |
| [Browser](browser-tests.json) |27 checks:13 kartu/11 aktif, guru/PIN, A/D, quiz/buff, hasil/progres/ghost/replay/reload dan sentuh390×844/844×390 |
| [GP unit](grand-prix-tests.json) | Classic3/Nusantara10 identik baseline untuk order/poin/mastery/retry; dua cup baru terblokir. Sequence13 ronde hanya metadata, tanpa membangun world12/13 palsu |
| [GP browser](grand-prix-browser-tests.json) |81 pemeriksaan regresi UI Nusantara10: semua world lama, kuis/freeze, ronde10 gagal/ulang/lolos, rollback poin, rekap/ekspor/PIN/progres |
| [Item/AI](item-tests.json) |11 checks sembilan buff, finite supply, target pemain, cooldown, collision, protection dan clock lama |
| [Offline/ekspor](offline-tests.json) |28 checks, jaringan browser dimatikan, tidak ada request aset HTTP/CDN; export guru tidak membawa salt/verifier PIN |
| [Smoke rilis](release-smoke.json) | HTML final masuk ke Kubu Raya melalui Mode Siswa; SHA final dicatat |
| [file://](direct-file-tests.json) | Navigasi benar-benar dicoba tetapi diblokir administrator browser cloud; bukan klaim skema tersebut sudah lulus |

Fixture UI menempatkan kendaraan menuju gerbang kuis/finish atau kanal dan menyiapkan inventori/quiz count hanya pada context QA. Bukan klaim balapan GP manual penuh. Route completion diuji terpisah dengan driver/AI sebenarnya. HP fisik, FPS, frame time dan peak memori belum diukur.

Screenshot asli: [overview](screenshots/overview.png), [mercusuar/mangrove](screenshots/lighthouse-mangrove.png), [jembatan](screenshots/extreme-bridge.png), [tong](screenshots/obstacle-barrel.png), [pintu](screenshots/swing-gate.png), [lompatan simulasi nyata](screenshots/canal-jump.png), [fork](screenshots/fork-routes.png), [pemain](screenshots/race-desktop.png), HP [landscape](screenshots/race-844x390.png)/[portrait](screenshots/race-390x844.png), [rescue/pause](screenshots/rescue-pause.png), [kartu](screenshots/after-available-card.png). Overview memakai kamera inspeksi dan fog off; gameplay memakai kamera/fog native. [Before/after katalog](comparison-report.json) membandingkan katalog10 lama dengan13 baru; Stage11 belum ada pada baseline, sehingga tidak ada before-world palsu.

## Ukuran dan distribusi

HTML **24.838.968 byte**, naik **36.856 byte**, sisa161.032 byte terhadap25MB desimal. Ekspor guru terukur **24.874.378 byte**. WebP thumbnail640×400:4.442 dan7.236 byte. Geometri lingkungan48.830 segitiga,31 batch warna/14 batch shadow,10 tekstur label kecil runtime. Dua hazard bergerak memakai mesh lokal tetap dan transform, tanpa alokasi mesh per frame. Material dibagi per warna; landmark, mangrove dan boardwalk dibatch. Tidak menambah GLB, poster duplikat, CDN atau aset gambar besar.

Seluruh scene high-clear:105–215 draw warna /24–68 depth; low-clear93–207 draw warna, tanpa shadow depth. Ini penghitung drawPrimitive pada12 posisi, termasuk actor, bukan FPS/biaya GPU. Dua draw sky/cloud native terpisah. LOD actor dan quality lama tetap, geometri environment ringan memakai mesh sama pada semua kualitas.

[Metrik aset](asset-metrics.json), [aktivasi](activation.json), [status13 stage](stage-status.json), [metrik/hash ZIP](release-metrics.json). ZIP playable berisi HTML identik, bukan server/fetch loader aset lokal. Review ZIP memuat tambahan sumber, screenshot dan laporan; hash final review dicatat di repo karena arsip tidak dapat memuat hash final dirinya sendiri.

## Build

Perlu checkout baseline Bromo beserta helper. Python/Pillow, Node/Playwright/Chromium tersedia di cloud; path browser.cjs dapat disesuaikan. Localhost8000 hanya harness developer, bukan dependensi game. Maksimal dua browser WebGL berat bersamaan.

```sh
python visual-upgrade/stage11-kubu-raya/source/assemble.py
node visual-upgrade/stage11-kubu-raya/source/capture.cjs
python visual-upgrade/stage11-kubu-raya/source/thumbnails.py
python visual-upgrade/stage11-kubu-raya/source/assemble.py
node visual-upgrade/stage11-kubu-raya/source/test_mechanics.cjs
node visual-upgrade/stage11-kubu-raya/source/test_physics.cjs
node visual-upgrade/stage11-kubu-raya/source/test_items.cjs
node visual-upgrade/stage11-kubu-raya/source/test_grand_prix.cjs
node visual-upgrade/stage11-kubu-raya/source/test_world.cjs
node visual-upgrade/stage11-kubu-raya/source/test_render_mechanics.cjs
node visual-upgrade/stage11-kubu-raya/source/test_browser.cjs
node visual-upgrade/stage11-kubu-raya/source/test_rescue_browser.cjs
node visual-upgrade/stage11-kubu-raya/source/test_gp_browser.cjs
node visual-upgrade/stage11-kubu-raya/source/test_offline.cjs
node visual-upgrade/stage11-kubu-raya/source/test_render_parity.cjs
node visual-upgrade/stage11-kubu-raya/source/capture_comparison.cjs
python visual-upgrade/stage11-kubu-raya/source/verify_scope.py
python visual-upgrade/stage11-kubu-raya/source/assemble.py --release
node visual-upgrade/stage11-kubu-raya/source/test_file.cjs
node visual-upgrade/stage11-kubu-raya/source/test_release.cjs
python visual-upgrade/stage11-kubu-raya/source/package.py
```

Kandidat /tmp/blokraya-6h/candidate.html. `--release` hanya menulis HTML dan available setelah seluruh gate termasuk mechanics/rescue/GP lolos; kandidat/rilis byte-identik. Review ZIP membutuhkan checkout baseline untuk rebuild engine yang sudah ada.
