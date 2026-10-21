# 6I — Kayong Utara: Coastal Cliff Challenge

Arena **playable untuk tinjauan**, dibangun dari HEAD Stage11 `f2d57c8659a752315c3627e9ed26261cee1583d1`. Seluruh11 world sebelumnya,14 pasangan GLB high/low, avatar, PIN, poster, audio, HUD, buff dan engine asesmen dipertahankan. **Ketapang belum dibuat.** Tidak merge, deployment atau mengganti `index.html` online.

## Isi dan batas representasi

Jalur pesisir **fiktif1133,81m**, elevasi maksimum16m, kemiringan absolut maksimum0,139 (~7,9°). Hairpin dan S-curve membentuk sirkuit tertutup550 segmen dengan marka, guardrail, start/finish dan checkpoint aman. Tidak meniru jalur tiga arena awal. Jembatan memiliki lebar fisik6,5m; jalan utama11m. Pagar diperhitungkan terhadap radius kendaraan0,65m. Permukaan baru hanya memakai konfigurasi/adapter arena ini; physics global tidak diganti.

Laut turquoise, pantai, ombak tipis, kelapa, tebing berundak, bukit tropis dan pulau jauh dibuat dengan geometri prosedural bermaterial bersama. Sky gradient, awan blocky, haze dan pencahayaan lama dipakai ulang. Kamera chase asli tetap: pemeriksaan terrain/lajur dan kamera tidak memerlukan perubahan kamera global.

Pantai dan perbukitan terinspirasi brief Pulau Datok/Sukadana. **Monumen Sail Karimata merupakan interpretasi nautika stylized yang belum diverifikasi foto**, bukan rekonstruksi akurat. Referensi `https://id.wikipedia.org/wiki/Pantai_Pulau_Datok` gagal dengan CONNECT403; tidak ada foto landmark spesifik terlampir. Bentuk layar/warna/proporsi tidak diklaim sebagai ciri bangunan asli. Jalan ekstrem tidak dinyatakan ada di lokasi wisata nyata.

## Zona tantangan

| u / zona | Mekanisme aktual | Jalur aman / mitigasi |
|---|---|---|
| .10 Batu tikungan | Collider parsial, perlambatan benturan | Kanan; papan sebelum tikungan |
| .20 Batu bergerak | Pose periodik bolak-balik, collider dan mesh memakai fungsi sama | Peringatan sebelum melintas; ruang menghindar pada sisi berlawanan |
| .30 Jembatan sempit | Deck27m, rail collider dan pillar | Kurangi kemudi/kecepatan; tetap dapat menyalip secara hati-hati |
| .41 Kerikil | Patch traksi temporer pada sisi kanan | Kiri / Ban Anti-Selip |
| .49 Celah teluk | Road mesh benar-benar putus3,2m, ramp oranye, impuls asli10,5m/s | Gas≥9m/s; rescue mundur bila gagal |
| .59 Palang berkala | Siklus9s, berputar pada pivot kiri, swept collider | Selalu tersedia sisi kanan |
| .68 Tiang | Tiga bollard pendek pada sisi kanan | Kiri; tidak menutup seluruh jalan |
| .77 Batu tepi jalan | Collider parsial, rubble tambahan di luar lajur | Kanan |
| .85 Pasir | Patch traksi ringan pada sisi kiri | Kanan / Ban Anti-Selip |
| .94 Percabangan | Dua dek terpisah dalam koordinat lateral/progres engine | Kiri aman; kanan gap3m berhadiah1 token sesudah mendarat |

Percabangan **bukan graph rute independen**. Memakai kemampuan koordinat lintasan yang sudah ada, collider divider dan dua permukaan jalan. AI Santai memilih kiri; personality `berisiko` pada Sedang/Menantang memilih kanan. Mengemudi aman tanpa drift atau item tetap dapat menyelesaikan balapan; drift/rem/jump asli tersedia.

Papan berada36m sebelum pusat zona (ditambah setengah panjang untuk bridge/fork). Batu bolak-balik kontinu, tanpa reset posisi instan; memiliki waktu peringatan sebelum setiap lintasan. Palang memberi2s peringatan sebelum mulai menutup; indikator tetap merah selama tertutup/membuka. Pose memakai `session.elapsed`, bukan jam dinding. Titik bahaya yang memerlukan jump diberi ramp dan tanda.

Rescue mundur ke checkpoint aman yang sudah benar-benar dilewati, lalu menahan kendaraan2,4s. Tidak memberi keuntungan potong lintasan atau menambah jawaban/checkpoint. Inventori, charge, token dan catatan akademik tetap; buff berdurasi mengikuti waktu simulasi saat menunggu. Pause/soal membekukan semuanya. Area tepi dilindungi guardrail; overshoot dan stall juga mendapat fallback rescue. Tidak ada teleport AI maju.

## Integrasi dan perlindungan

- ID baru playable `kayong_utara`. Semua13 ID tetap;12 world tersedia, `ketapang` tetap Segera Hadir.
- Kalbar Klasik3/Nusantara10 tetap playable; metadata Extreme3/Lengkap13 identik dengan baseline, keduanya belum bisa dimulai karena Ketapang belum tersedia.
- Entry metadata dipisahkan dari builder/track/progres. Kartu memakai thumbnail render aktual, bukan poster generatif.
- `RaceCliff.Session` memperluas Session terakhir, dengan guard ID12. Nama helper berbeda dari Stage11 untuk melindungi virtual dispatch. Item, inventori, asesmen dan kepribadian Smart AI tetap dari parent.
- Builder memakai Garden/CityBatch, utilitas palm/parasol, material batches, sky dan cleanup lama. Tidak menyalin engine atau menanam GLB/avatar duplikat.
- Hash seluruh berkas visual-upgrade historis dan rootindex dibanding baseline; script engine, Stage11 mechanics, seluruh cup, model, poster dan22 thumbnail lama identik. Physics350 langkah setara per11 stage lama dan27 render pixel identik pada pose/waktu/cahaya tetap.
- Tidak menyisipkan data profil/unlock/token QA. Kunci localStorage, PIN dan ghost lama tidak diganti. Ekspor guru mengosongkan PIN dan tidak memuat salt/verifier perangkat.

## Pengujian aktual

Lihat [physics-tests.json](physics-tests.json), [multilap-tests.json](multilap-tests.json), [mechanics-tests.json](mechanics-tests.json), [clearance-tests.json](clearance-tests.json), [world-tests.json](world-tests.json), [browser-tests.json](browser-tests.json), [offline-tests.json](offline-tests.json), [unchanged-renders.json](unchanged-renders.json) dan [grand-prix-browser-tests.json](grand-prix-browser-tests.json).

- 18 balapan reference-driver:3 kesulitan×6 seed; lima jawaban, empat benar, skor80. Ini simulasi input pada Session asli, bukan klaim balapan manual.
- 14 pilihan karakter/kendaraan menyelesaikan rute dengan skor100; tiga balapan tambahan tiga lap (satu tiap kesulitan) menguji hazard/checkpoint berulang.
- 72 completion AI pada18 kasus, ditambah12 AI pada3 kasus tiga lap. Batas perpindahan tiap langkah≤31dt; seluruhnya finis. Jumlah rescue dan collision aktual tercantum per kasus, tidak disembunyikan. AI dapat memakai rescue mundur bila benar-benar gagal jump; tidak diwarp maju.
- Collider tiap zona, palang/rock sharing pose, kontinuitas batu saat batas siklus, grip, radar, risky reward tanpa duplikasi, gagal jump/rescue, wait/freeze, jump9/12/23/31m/s dan Ban Anti-Selip.
- 1.555 sampel lajur terhadap triangle terrain/rock aktual;96 render chase pada12/31m/s memeriksa kamera tidak masuk terrain.108 sampel world (12 posisi×3 kualitas×3 cuaca), cleanupGPU saat berpindah ke seluruh11 world lama; tidak ada JS/WebGL error.
- Desktop1366×768, touch emulation390×844 dan844×390: selection card, actual touch steering, A/D, kuis freeze, buff reward/use, pause, hasil/progres/ghost, replay/reload/PIN, learning export. Screenshot dari UI/renderer sebenarnya.
- GP Nusantara10 UI: ronde benar, gagal ronde10, retry dengan rollback poin, lolos dan rekap juara, ekspor dan reload. **Memakai fixture posisi ke gate/finish; bukan sepuluh balapan manual penuh.**
- Offline dengan network browser dimatikan dan HTML disuplai route harness localhost; nol request aset HTTP/CDN, ekspor guru dimuat dalam konteks offline baru dan memulai race.

`file://` dicoba menggunakan HTML distribusi; hasil/kendala kebijakan browser cloud di [direct-file-tests.json](direct-file-tests.json). Jangan menganggap pengujian origin localhost membuktikan file:// pada seluruh browser. Tidak ada fetch aset lokal atau server wajib ditambahkan. Pengujian HP fisik, FPS, frame time dan penggunaan memori belum dilakukan. Keamanan PIN tetap pembatas UI lokal, bukan proteksi dari pengedit HTML/storage.

## Render dan screenshot

[Overview](screenshots/overview.png) · [Pantai](screenshots/pulau-datok.png) · [Sail Karimata interpretasi](screenshots/sail-karimata.png) · [Hairpin](screenshots/hairpin.png) · [Batu bergerak](screenshots/rolling-rock.png) · [Palang](screenshots/timed-barrier.png) · [Jump aktual](screenshots/bay-jump.png) · [Kamera menurun](screenshots/descent-camera.png) · [Percabangan](screenshots/fork-routes.png).

[Desktop](screenshots/race-desktop.png) · [HP landscape](screenshots/race-844x390.png) · [HP portrait](screenshots/race-390x844.png) · [Sebelum](screenshots/before-unavailable-card.png)/[sesudah](screenshots/after-available-card.png).

Overview dan landmark memakai kamera inspector; overview menonaktifkan fog agar seluruh jalur bisa diperiksa. Gameplay/HP memakai chase camera asli dan fog normal. Screenshot jump berasal dari delapan langkah simulasi sesungguhnya, bukan mengangkat model secara manual. Kayong Utara belum punya world pada baseline; gambar sebelum hanya menunjukkan kartu Segera Hadir, bukan world lama yang diberi nama baru.

## Metrik dan build ulang

Angka final ukuran HTML/ZIP/SHA, pertumbuhan, ekspor guru, segitiga dan draw call aktual ada di [release-metrics.json](release-metrics.json) dan [asset-metrics.json](asset-metrics.json). Lingkungan awal terukur74.130 segitiga,32 batch warna,12 batch shadow,11 tekstur label canvas kecil. Draw call world tidak sama dengan keseluruhan frame; tabel kualitas memuat ukuran frame aktual termasuk karakter, jalan, sky dan efek. Tidak menyatakan FPS perangkat nyata.

Sumber utama: [cliff.js](source/cliff.js), [cliff-physics.js](source/cliff-physics.js), [track.json](track.json), [stages.json](stages.json), [cups.json](cups.json), [assemble.py](source/assemble.py). Source JavaScript prosedural dapat diedit; tidak diperlukan ekspor GLB/Blender baru.

Dari root checkout branch pada baseline Stage11 (Python3/Pillow, Node, Chromium dan Playwright diperlukan untuk validasi):

```bash
python visual-upgrade/stage12-kayong-utara/source/assemble.py
node visual-upgrade/stage12-kayong-utara/source/capture.cjs
python visual-upgrade/stage12-kayong-utara/source/thumbnails.py
python visual-upgrade/stage12-kayong-utara/source/assemble.py
```

Candidate ditulis ke `/tmp/blokraya-6i/candidate.html`. Jalankan server root repository `python -m http.server 8000`. Browser harness mengintersep URL distribusi dengan candidate. Jalankan semua `test_*.cjs` selain `test_file.cjs`/`test_release.cjs` sebelum release; `verify_scope.py` membuktikan reverse assembly dan aset terlindungi. Jangan mengubah candidate ketika pengujian berjalan.

```bash
python visual-upgrade/stage12-kayong-utara/source/assemble.py --release
node visual-upgrade/stage12-kayong-utara/source/test_release.cjs
node visual-upgrade/stage12-kayong-utara/source/test_file.cjs
python visual-upgrade/stage12-kayong-utara/source/package.py
```

`--release` memerlukan laporan lolos serta thumbnail nyata sebelum mengubah metadata source menjadi available. ZIP playable berisi satu HTML dan MULAI.txt; reviewZIP menambahkan source/metadata/screenshot/report. Hash ZIP review lengkap disimpan di repository, bukan hash-diri di dalam ZIP.
