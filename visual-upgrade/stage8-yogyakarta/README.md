# BlokRaya — 6E / Stage 8 Yogyakarta: Heritage Night Race

Baseline lokal/remote terverifikasi **`a7355609e4f9eb6dc255a9951fc9f7419da4ec2e`** (Bengkayang), branch `dev/race-quest-cat-sport-visual-upgrade`. Distribusi [HTML mandiri](../blokraya-stage8-yogyakarta.html). Hanya Yogyakarta dibuat; tidak merge, deployment, mengubah `index.html` atau mengerjakan 6F.

## Arena dan suasana malam

Lintasan kota **fiktif 826,23 m**, 17 waypoint dan 550 segmen tertutup, ruas lurus, tikungan dan chicane urban. Elevasi maksimum **1,50m**, grade maksimum **3,17%**, empat obstacle batu/kayu sebagai hambatan konstruksi ringan, satu ramp u=0,71 dan tanpa gap. Lebar jalan, collider ±6,2m, start/finish, jalur AI, collision dan fisika lama tetap. Tidak memakai ulang rute/world lama.

Tugu Pal Putih stylized putih-emas menjadi landmark utama: alas persegi bertingkat, pedestal dengan panel, shaft empat sisi yang mengecil, lis emas dan puncak meruncing. Plaza/taman kecil, jalur penghubung dan planter mengelilingi monumen. Koridor terinspirasi Malioboro mempunyai ruko dua lantai dengan teras/arcade, atap sederhana, jendela hangat, lampu hijau tua, bangku, pohon kota, bollard dan gerobak dekoratif. Tidak mengandalkan papan nama sebagai pengganti bentuk monumen.

Night rendering hanya aktif saat `RaceRenderer.race()` merender ID `yogyakarta`. Material actor diberi tint dingin sementara lalu **dipulihkan pada frame yang sama**, sehingga data GLB tidak berubah. Material milik arena memakai palet malam, jendela/lentera memakai emissive ringan. Tiga lapis decal transparan memberi cahaya dekoratif hangat pada permukaan jalan dan mengikuti tinggi jalan; tidak menambahkan point light dinamis, bloom, framebuffer postprocess atau shader pencahayaan mahal.

Gradient/horizon lama memakai palet malam. Awan memakai satu fragment program khusus Yogyakarta, dengan vertex shader/buffer cloud baseline digunakan bersama. Bulan poligonal dan bintang dibatch menjadi **172 segitiga dan satu draw tambahan**, tanpa tekstur. Tidak menambah clock waktu nyata; seluruh dekorasi statis dan pergerakan lama tetap mengikuti clock simulasi. Program, fragment dan buffer malam dilepas saat keluar arena. Tabel tinggi CPU Bengkayang juga dibersihkan ketika masuk Yogyakarta.

Evaluasi awal memperbaiki blending decal cahaya agar tidak saling menutup, menambah plaza sekitar tugu serta merapikan roda gerobak/jendela belakang. Pengukuran awal lingkungan **150.076 segitiga**; panel tipis ruko kemudian diubah menjadi quad dan trim kecil menjadi box, sambil mempertahankan bevel pada massa/siluet utama. Hasil **51.508 segitiga**, turun **65,7%**; [catatan optimasi](optimization.json). Tidak menurunkan model karakter/kendaraan atau aset arena lama.

Sumber editable [night-city.js](source/night-city.js), [track.json](track.json) dan [stages.json](stages.json). Builder memakai helper City/Garden/Sentarum, tanpa menyalin seluruh engine. Blender tersedia tetapi prosedural JavaScript lebih sesuai di sini; tidak membutuhkan GLB/tekstur environment besar baru.

**Batas representasi:** referensi web ditolak 403 dan tidak ada foto khusus Tugu terlampir. Proporsi/detail/denah belum diverifikasi; monumen dan koridor adalah interpretasi stylized, bukan rekonstruksi geografis, arsitektural atau historis. Tidak mengarang prasasti/lambang yang diklaim autentik. [Catatan referensi](reference-notes.md).

## Integrasi dan perlindungan

ID **`yogyakarta`** tetap dari katalog Prompt 5. Delapan arena tersedia: `kampung`, `kapuas`, `hutan`, `sambas`, `sintang`, `kapuas_hulu`, `bengkayang`, `yogyakarta`. Bali dan Bromo tetap Segera Hadir, ditolak saat membuat Track/Session/start race. Kalbar Klasik tetap tiga arena awal. Nusantara memuat Yogyakarta sebagai ronde kedelapan tetapi belum aktif sampai dua world terakhir tersedia.

Terhubung ke kartu/thumbnail, pengaturan guru, minimap, Session/Track, renderer, Smart AI, 9 buff, 2 slot, hasil belajar, `stageProgress.yogyakarta`, ghost, reload dan replay. Profil, bank soal, token, unlock, audio, HUD, PIN Guru dan semua kunci penyimpanan tetap. Tidak menyisipkan profil/token/unlock QA ke HTML distribusi. Penilaian/ketuntasan, physics, AI, aturan buff dan kontrol tidak diubah.

Tambahan hanya script scoped `yogyakartaStageVisuals`, track, metadata target dan dua thumbnail. Script core/renderer dasar, GLB, audio/VFX, HUD, mode/PIN, poster/loading dan builder lama tetap byte-identik. [Scope](scope-tests.json) membuktikan assembly dapat dibalik persis ke baseline: **2.304 file historis**, **28 payload** dan **14 thumbnail lama** terlindungi. [23 render pixel-identik](unchanged-renders.json) mencakup 14 pasangan, Cat low, mobil Cat saja, serta tujuh world lama setelah masuk/keluar Yogyakarta. [Uji malam](night-tests.json) membuktikan material dan garasi tidak terkena perubahan permanen.

`assemble.py` membuat kandidat uji; hanya `--release` menulis distribusi/metadata tersedia setelah semua laporan wajib termasuk night-tests lolos. [Aktivasi](activation.json) mencatat baseline belum tersedia, delapan arena rilis dan byte kandidat/rilis identik. [Smoke rilis](release-smoke.json) membuka Mode Siswa serta arena baru pada SHA HTML final.

## Build ulang

Dari root checkout yang memuat HTML baseline Bengkayang. Python/Pillow, Node/Playwright/Chromium sudah tersedia di cloud; sesuaikan path runtime pada `browser.cjs` di komputer lain. Server statis internal port 8000 hanya untuk harness pengembangan; bukan kebutuhan baru game. Jalankan paling banyak dua browser WebGL berat bersamaan.

```sh
python visual-upgrade/stage8-yogyakarta/source/assemble.py
node visual-upgrade/stage8-yogyakarta/source/capture.cjs
python visual-upgrade/stage8-yogyakarta/source/thumbnails.py
python visual-upgrade/stage8-yogyakarta/source/assemble.py
node visual-upgrade/stage8-yogyakarta/source/test_physics.cjs
node visual-upgrade/stage8-yogyakarta/source/test_items.cjs
node visual-upgrade/stage8-yogyakarta/source/test_surfaces.cjs
node visual-upgrade/stage8-yogyakarta/source/test_world.cjs
node visual-upgrade/stage8-yogyakarta/source/test_night.cjs
node visual-upgrade/stage8-yogyakarta/source/test_browser.cjs
node visual-upgrade/stage8-yogyakarta/source/test_offline.cjs
node visual-upgrade/stage8-yogyakarta/source/test_render_parity.cjs
node visual-upgrade/stage8-yogyakarta/source/capture_comparison.cjs
python visual-upgrade/stage8-yogyakarta/source/verify_scope.py
python visual-upgrade/stage8-yogyakarta/source/assemble.py --release
node visual-upgrade/stage8-yogyakarta/source/test_file.cjs
node visual-upgrade/stage8-yogyakarta/source/test_release.cjs
python visual-upgrade/stage8-yogyakarta/source/package.py
```

[Assembler](source/assemble.py) · [capture](source/capture.cjs) · [thumbnail](source/thumbnails.py) · [metrik](source/report.py) · [paket](source/package.py). Kandidat `/tmp/blokraya-6e/candidate.html` identik dengan rilis. Unit harness memakai stub adapter hanya untuk logika; renderer/world aktual diuji lewat browser. Dependensi build tidak diperlukan ketika bermain.

## Pengujian

| Laporan | Hasil |
|---|---|
| [Physics](physics-tests.json) | 7 kelompok: 8 stage tersedia/2 diblokir, GP klasik/Nusantara, tujuh konfigurasi/simulasi lama identik selama 350 langkah/session, rute tertutup tanpa overlap, 18 balapan referensi, 18 completion AI, collision/border/drift/jump/landing, 9 buff dan freeze/progres/ghost. |
| [Item](item-tests.json) | 11 kelompok stok terbatas, semua buff, target pemain/AI, cooldown/charge, refleksi/grip, projectile/oli, immunity, radar, freeze dan collision. |
| [Permukaan](surface-tests.json) | 138 anchor dibandingkan perpotongan segitiga terrain/bahu aktual, toleransi 12cm. |
| [World](world-tests.json) | 108 sampel (12 posisi × 3 kualitas × 3 cuaca) tanpa error WebGL; vertex struktur minimum 7,739m dari centerline, di luar collider. Buffer/tekstur/program malam dilepas pada transisi ke tujuh arena lama; rebuild stabil; lookup CPU lama dibersihkan. |
| [Night](night-tests.json) | 5 cek: material cache GLB dipulihkan; binding cloud/flag frame kembali; piksel paused/question identik pada waktu simulasi tetap; piksel garasi setelah malam sama dengan setelah world siang; tanpa error JS/WebGL. |
| [Browser](browser-tests.json) | 27 cek loading 3 detik, PIN/mode/konfigurasi guru, kartu/thumbnail, siswa/4 AI, A/D, pause/soal/buff/E, hasil JSON/progres/ghost/reload/replay; desktop 1366×768 serta HP emulasi 390×844/844×390 dengan touch press CDP. |
| [Offline](offline-tests.json) | 28 cek jaringan mati: PIN, ekspor guru tanpa salt/verifier, aset/poster tidak diduplikasi, race/quiz/buff/save, HTML ekspor pada konteks baru, 8 world dan tanpa request HTTP/CDN aset. |
| [Parity](unchanged-renders.json) / [scope](scope-tests.json) | 23 render dan seluruh payload/aset/file lama tetap identik. |
| [Before–after kartu](comparison-report.json) | Kartu baseline Segera Hadir dibanding kartu tersedia dengan thumbnail render, viewport setara. World baru tidak mempunyai render “sebelum”; tidak membuat world lama palsu. |
| [file://](direct-file-tests.json) | Dicoba langsung dan ditolak `ERR_BLOCKED_BY_ADMINISTRATOR` oleh browser cloud; tidak diklaim lolos. |

Semua 18 balapan driver referensi selesai dengan skor akademik tetap 80% dari 4 benar/5 soal. Semua 72 AI pada 18 kasus completion mencapai finish; stall maksimum 0s. Rerata waktu simulasi Santai **55,28s**, Sedang **43,31s**, Menantang **41,96s**. Ini bukan waktu manusia/FPS. Browser UI memakai fixture gate/finish untuk alur terarah; rute penuh dibuktikan oleh simulasi terpisah. GP seluruh ronde tidak dimainkan manual ulang; urutan/ketersediaan dan kode lama diperiksa. HP fisik, frame time dan konsumsi memori belum diukur.

## Screenshot dan metrik

[Overview malam](screenshots/overview.png) · [Tugu Pal Putih](screenshots/tugu-pal-putih.png) · [Koridor Malioboro](screenshots/malioboro-corridor.png) · [Boulevard/bulan](screenshots/night-boulevard.png) · [Menuju tugu](screenshots/tugu-approach.png) · [Gameplay](screenshots/gameplay.png) · [Tikungan](screenshots/city-corner.png) · [Ruko](screenshots/shopfronts.png) · [Ramp](screenshots/ramp.png).

Menu [sebelum](screenshots/before-menu.png) / [sesudah](screenshots/after-menu.png), kartu [sebelum](screenshots/before-unavailable-card.png) / [sesudah](screenshots/after-available-card.png). Menu HP [portrait](screenshots/menu-390x844.png), [landscape](screenshots/menu-844x390.png). Race [desktop](screenshots/race-desktop.png), [portrait](screenshots/race-390x844.png), [landscape](screenshots/race-844x390.png); [kuis](screenshots/quiz.png), [hasil](screenshots/results.png).

Semua gambar adalah screenshot renderer/UI sebenarnya. Overview memakai kamera review atas dengan fog geometri dimatikan hanya saat capture; landmark/koridor memakai kamera review eksplisit. Screenshot gameplay memakai kamera balapan. Kamera distribusi tidak diubah.

HTML **24.706.902 byte**, baseline **24.658.272 byte**, pertumbuhan **48.630 byte**, sisa batas 25.000.000 byte **293.098 byte**. WebP mentah total **23.310 byte**; script/track/metadata dan thumbnail embedded dicatat per komponen dalam [asset-metrics.json](asset-metrics.json). Tidak menggandakan model/audio/poster atau menambah tekstur langit besar.

Lingkungan **51.508 segitiga**, **23 colour batch calls**, **16 shadow batch calls**, satu tekstur label. Terrain 2 segitiga; bulan/bintang 172 segitiga. Gradient/cloud memakai dua draw baseline; bulan/bintang menambah satu drawPrimitive yang sudah masuk counter frame. Cloud memakai satu program fragment baru dan buffer lama, tanpa point light dinamis. Counter frame lengkap high: 104–210 colour calls / 95.141–144.527 segitiga; low: 90–200 calls / 76.390–100.278 segitiga, tanpa depth/shadow pass. Counter drawPrimitive tidak mencakup dua draw langsung gradient/cloud. LOD karakter, bayangan dan cloud mengikuti baseline; tidak mengklaim FPS perangkat.

Distribusi tetap satu HTML offline dengan aset tertanam, dibungkus ZIP playable/review. [release-metrics.json](release-metrics.json) memuat ukuran/hash/CRC dan kesamaan HTML. Salinan metrik di dalam ZIP review tidak memuat hash ZIP dirinya sendiri; hash lengkap ada di repository. Offline lulus dengan jaringan mati dan dokumen lokal disuplai harness pada localhost; file:// diblokir kebijakan cloud dan perlu verifikasi di browser target. Tidak menambahkan server wajib, backend, CDN atau loader fetch aset lokal.
