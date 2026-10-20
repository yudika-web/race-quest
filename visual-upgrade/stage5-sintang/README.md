# BlokRaya — 6B / Stage 5 Sintang: Kelam Mountain Run

Baseline lokal dan remote: `201d60688976d6320c95a6a021472f5b27f12c87` (Sambas), branch `dev/race-quest-cat-sport-visual-upgrade`. Distribusi baru: [`../blokraya-stage5-sintang.html`](../blokraya-stage5-sintang.html). Hanya Sintang dibangun; tidak merge, deployment, mengubah `index.html`, atau mengerjakan 6C.

## Arena baru

Lintasan fiktif **905,66 m**, 17 waypoint dan 550 segmen halus: beberapa tikungan/rangkaian lengkung, naik-turun hingga **8 m**, kemiringan maksimum sekitar **11,56%**, empat obstacle batu/kayu dan satu ramp pada bagian lembah yang datar. Tidak memakai celah jalan. Jalan lengkap tersambung, start/finish, marka, pengaman, minimap, jalur AI dan collision memakai engine lama; konfigurasi rute baru, bukan salinan world lama dengan nama berbeda.

Lingkungan prosedural blocky memakai monolit granit besar terinspirasi Bukit Kelam, hutan tropis berlapis, batu berlumut, semak/pakis, lampu jalur, pagar yang mengikuti elevasi dan area rumah panjang berpanggung terinspirasi Rumah Betang Ensaid Panjang. Rumah panjang memiliki galeri, pintu pusat, tangga terbuka, atap pelana, tiang dan jalur penghubung; papan penunjuk berada di samping jalur. Tidak mengandalkan papan nama sebagai pengganti bentuk landmark.

Terrain baru memakai grid ringan. Tinggi dekorasi pada bagian jauh diinterpolasi dari **segitiga terrain yang benar-benar dirender**, bukan hanya fungsi ketinggian ideal; bagian dekat jalan tetap memakai bahu jalan asli. Akar/basis ditanam sedikit ke tanah. Tebing memakai loft polygonal kontinu; variasi warna menyatu dengan bidang sehingga tidak ada decal yang mengambang. Gradient langit, awan blocky dan haze lama dipertahankan dengan palet Sintang yang sedikit sejuk. Seluruh elemen baru statis; tidak menambahkan clock waktu nyata atau shader baru.

Blender tersedia tetapi tidak diperlukan: sumber editable berupa JavaScript/JSON dan geometri prosedural dengan material batch bersama. Helper bevel, planter, jalur, label dan vegetasi digunakan kembali dari City/Garden. Tidak menyalin keseluruhan script arena lama ke builder baru.

**Akurasi:** landmark adalah interpretasi stylized, **bukan rekonstruksi historis/geologis terverifikasi**. Akses referensi web ditolak 403 dan tidak ada foto Sintang yang dilampirkan. Dimensi/denah/motif/detail belum diverifikasi. Lihat [`reference-notes.md`](reference-notes.md); tidak mengarang lambang atau simbol sakral. Seluruh jalur/tata lingkungan adalah komposisi fiktif permainan.

## Integrasi dan perlindungan

ID tetap `sintang` sesuai Prompt 5. Lima arena tersedia: Pontianak (`kampung`), Mempawah (`kapuas`), Singkawang (`hutan`), Sambas (`sambas`), Sintang (`sintang`). Stage 6–10 tetap Segera Hadir. Kalbar Klasik tetap tiga arena awal; Sintang sudah terdaftar sebagai ronde kelima Nusantara, yang masih dinonaktifkan sampai lima world berikutnya tersedia. Tidak menambahkan turnamen baru atau membuka arena palsu.

Stage terhubung ke kartu/preview bergambar, pengaturan guru, Session/Track, renderer, AI, sembilan buff, inventori dua slot, ghost, hasil belajar dan `stageProgress.sintang`. Semua kunci penyimpanan, profil/token/unlock, bank soal, PIN lokal, audio, HUD dan preferensi lama tetap. Tidak ada data demonstrasi/token/unlock yang disisipkan ke distribusi. Penilaian akademik, ketuntasan, physics, AI, buff dan kontrol tidak diubah.

Core, renderer dasar, world builder lama, audio/VFX, AI, buff, HUD, PIN/mode dan loading/poster tetap byte-identik. Tambahan track/sky/terrain/world diterapkan melalui satu script scoped `sintangStageVisuals`, dengan fallback persis ke fungsi lama untuk arena lain. Verifikasi scope membalik assembly tepat ke baseline; **2.112 file historis, 22 payload script/aset dan delapan thumbnail lama identik**. Model 14 pasangan tetap utuh.

Kandidat HTML diuji terlebih dahulu. `assemble.py --release` memerlukan laporan physics/item/permukaan/world/browser/offline/render terlindungi yang lolos dan thumbnail aktual sebelum menulis distribusi. [`activation.json`](activation.json) mencatat status awal belum tersedia serta kesamaan byte kandidat dan rilis.

## Sumber dan build

- [`track.json`](track.json): waypoint, elevasi, obstacle, ramp, palet dan seed.
- [`stages.json`](stages.json): katalog sepuluh arena; hanya entri Sintang berubah.
- [`source/mountain.js`](source/mountain.js): monolit, rumah panjang, terrain/interpolator, vegetasi, jalur dan adapter world/sky.
- [`source/assemble.py`](source/assemble.py): build terbatas dari HTML Sambas; [`bounded-changes.json`](bounded-changes.json) merekam perubahan.
- [`source/capture.cjs`](source/capture.cjs), [`source/thumbnails.py`](source/thumbnails.py): kamera review dan WebP 640×400 dari renderer sebenarnya.
- [`source/report.py`](source/report.py), [`source/package.py`](source/package.py): metrik, ZIP dan CRC/kesamaan HTML.

Dari root checkout, dengan server statis internal pada port 8000 dan alat Node/Playwright/Chromium/Python/Pillow yang sudah tersedia:

```sh
python visual-upgrade/stage5-sintang/source/assemble.py
node visual-upgrade/stage5-sintang/source/capture.cjs
python visual-upgrade/stage5-sintang/source/thumbnails.py
python visual-upgrade/stage5-sintang/source/assemble.py
node visual-upgrade/stage5-sintang/source/test_physics.cjs
node visual-upgrade/stage5-sintang/source/test_items.cjs
node visual-upgrade/stage5-sintang/source/test_surfaces.cjs
node visual-upgrade/stage5-sintang/source/test_world.cjs
node visual-upgrade/stage5-sintang/source/test_browser.cjs
node visual-upgrade/stage5-sintang/source/test_offline.cjs
node visual-upgrade/stage5-sintang/source/test_render_parity.cjs
python visual-upgrade/stage5-sintang/source/verify_scope.py
python visual-upgrade/stage5-sintang/source/assemble.py --release
node visual-upgrade/stage5-sintang/source/test_file.cjs
python visual-upgrade/stage5-sintang/source/package.py
```

Harness menyuplai kandidat `/tmp/blokraya-6b/candidate.html` pada URL HTML rilis; file rilis identik. Playwright memakai path runtime cloud dalam `browser.cjs`; sesuaikan pada komputer lain. Maksimal dua proses WebGL berat bersamaan. Unit test memakai adapter stub hanya untuk logika; world aktual diuji terpisah di browser. Build memerlukan checkout dengan baseline Sambas; dependensi pengembangan tidak dibutuhkan ketika bermain.

## Hasil pengujian

| Laporan | Hasil |
|---|---|
| [`physics-tests.json`](physics-tests.json) | 7 kelompok: lima track, lima arena diblokir, GP lama, empat konfigurasi/simulasi lama identik, rute tertutup tanpa perpotongan/overlap, 18 balapan penuh driver referensi, 18 completion AI, collision/ramp/drift/landing, sembilan buff, freeze/progres/ghost. |
| [`item-tests.json`](item-tests.json) | 11 kelompok stok terbatas, sembilan buff, target pemain/AI, cooldown/charge, pantulan/grip, projectile/oli, immunity, sensor/radar, freeze dan collision antar-racer. |
| [`surface-tests.json`](surface-tests.json) | 174 titik dekorasi dibandingkan dengan perpotongan vertikal segitiga tanah/bahu jalan aktual; selisih dalam toleransi 12 cm. |
| [`world-tests.json`](world-tests.json) | 108 sampel: 12 posisi × 3 kualitas × 3 cuaca, tanpa error WebGL; struktur aman, buffer/tekstur dilepas ketika berganti ke empat arena lama, jumlah resource stabil saat rebuild. |
| [`browser-tests.json`](browser-tests.json) | 27 pemeriksaan menu/thumbnail/pengaturan guru, loading 3 detik, siswa tanpa PIN, empat AI, A/D, pause/soal, buff, hasil/ekspor/progres/ghost/reload/PIN/replay, desktop dan HP portrait/landscape, termasuk touch press via CDP. |
| [`offline-tests.json`](offline-tests.json) | 28 pemeriksaan jaringan mati: PIN, ekspor guru tanpa salt/verifier, aset tertanam, start Sintang dan HTML ekspor, kuis/buff, lima world, tanpa permintaan HTTP/CDN aset. |
| [`unchanged-renders.json`](unchanged-renders.json) | 20 render identik: 14 pasangan, Cat low, mobil Cat saja dan empat world lama setelah masuk/keluar Sintang, pada kamera/pose/waktu tetap 256×256. |
| [`scope-tests.json`](scope-tests.json) | Assembly persis dapat dibalik; script/aset/file historis dan metadata arena lain tidak berubah. |
| [`direct-file-tests.json`](direct-file-tests.json) | `file://` benar-benar dicoba, ditolak `ERR_BLOCKED_BY_ADMINISTRATOR` oleh browser cloud; bukan hasil yang diklaim lolos. |

Seluruh 18 balapan driver referensi selesai dan tetap memperoleh skor akademik 80% dari empat jawaban benar/lima soal. Semua 72 AI pada 18 kasus completion mencapai finish tanpa stall; rerata simulasi Santai **62,13 s**, Sedang **47,48 s**, Menantang **45,50 s**. Ini bukan waktu balap manusia atau FPS perangkat. Uji completion terpisah menjaga car referensi bergerak agar AI dapat diukur sampai selesai; bukan klaim seluruh interaksi dimainkan manual.

Browser UI memakai fixture posisi ke gate/finish untuk pengujian terarah; penyelesaian lintasan penuh diperiksa oleh simulasi terpisah. Tidak ada error JavaScript/WebGL pada alur yang lolos. GP tidak dimainkan manual ulang seluruhnya karena code/aturan cup tidak berubah; urutan, ketersediaan dan kompatibilitas diuji. HP fisik, waktu/frame dan memori perangkat belum diukur.

## Screenshot dan ukuran

[Overview](screenshots/overview.png) · [Bukit Kelam](screenshots/bukit-kelam.png) · [Rumah panjang](screenshots/betang.png) · [Hutan/perbukitan](screenshots/forest-ridge.png) · [Kamera gameplay](screenshots/gameplay.png) · [Tikungan](screenshots/mountain-corner.png) · [Turunan](screenshots/hill-descent.png) · [Ramp](screenshots/ramp.png).

Menu [desktop](screenshots/menu-desktop.png), [portrait](screenshots/menu-390x844.png), [landscape](screenshots/menu-844x390.png); balapan [desktop](screenshots/race-desktop.png), [HP portrait](screenshots/race-390x844.png), [HP landscape](screenshots/race-844x390.png); [kuis](screenshots/quiz.png), [hasil](screenshots/results.png). Thumbnail [landmark](thumbnails/sintang-landmark.webp) dan [balapan](thumbnails/sintang-race.webp) berasal dari screenshot, bukan ilustrasi generatif.

Overview memakai kamera review atas dan fog geometri dimatikan hanya saat capture agar keseluruhan rute terbaca; screenshot lain memakai atmosfer game biasa. Pengaturan review tersebut tidak mengubah distribusi.

HTML **24.549.503 byte**, baseline Sambas **24.504.400 byte**, pertumbuhan **45.103 byte**, sisa batas 25.000.000 byte **450.497 byte**. Dua thumbnail berjumlah **23.474 byte** sebelum base64. Tidak ada tekstur besar/model/poster duplikat.

Batch lingkungan: **52.462 segitiga**, **21 colour draw calls**, **13 shadow batch calls**, satu tekstur label kecil dari canvas. Terrain terpisah **8.712 segitiga**. Statistik frame termasuk actor/item/fitur lebih besar; rentang per kualitas dan cuaca ada di [`asset-metrics.json`](asset-metrics.json). Counter `drawPrimitive` tidak mencakup dua panggilan langsung gradient/cloud. Batch lingkungan statis tetap pada tiap kualitas; LOD karakter, bayangan, jarak fitur dan awan memakai pengaturan baseline. Tidak mengklaim FPS HP atau benchmark kecepatan.

Distribusi tetap satu HTML mandiri dengan aset tertanam dan ZIP pembungkus. Offline lulus dengan konteks browser jaringan mati dan dokumen lokal disuplai harness pada localhost. Uji buka langsung `file://` diblokir kebijakan cloud; verifikasi browser target masih terbatas. Tidak menambahkan CDN, backend, server wajib baru atau paket `fetch()` aset lokal yang belum teruji. CRC dan kesamaan byte HTML pada kedua ZIP dicatat di [`release-metrics.json`](release-metrics.json).
