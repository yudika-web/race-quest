# RACE QUEST PRO — Batch 1

Tahap ini mencakup **Pinguin + Kapsul, Beruang + Buggy, Kelinci + Formula**. Ketiganya siap ditinjau. Kucing yang dijadikan standar adalah versi blocky commit `5b50da96ae72ad7cb30c6cfd37cf25d7a1f5c303`, bukan revisi organik. Sepuluh pasangan Batch 2–4 masih memakai aset asli dan belum didesain ulang.

## Unduh dan buka

- [HTML playable](../race-quest-pro-batch1.html), atau ekstrak `../../race-quest-pro-batch1-playable.zip` lalu buka **RACE-QUEST-PRO-Batch-1.html**. Game tetap satu HTML mandiri dengan aset tertanam dan dapat dimainkan tanpa mengunduh model/gambar/suara saat berjalan.
- `../../race-quest-pro-batch1-review.zip` berisi HTML, seluruh berkas tahap ini, screenshot, GLB, Blender, builder dan hasil uji. Build/integrasi ulang memakai template Kucing yang tetap tersedia dalam repository; arsip tinjauan tidak menggandakan template HTML lama.
- [Model high/low](models/) · [sumber Blender/script](source/) · [status 14 karakter](character-status.json).

| Pasangan | High | Low | Blender |
|---|---|---|---|
| Pinguin–Kapsul | [kart_nara.glb](models/kart_nara.glb) | [kart_nara_low.glb](models/kart_nara_low.glb) | [race-quest-nara.blend](source/race-quest-nara.blend) |
| Beruang–Buggy | [kart_bimo.glb](models/kart_bimo.glb) | [kart_bimo_low.glb](models/kart_bimo_low.glb) | [race-quest-bimo.blend](source/race-quest-bimo.blend) |
| Kelinci–Formula | [kart_sora.glb](models/kart_sora.glb) | [kart_sora_low.glb](models/kart_sora_low.glb) | [race-quest-sora.blend](source/race-quest-sora.blend) |

## Bentuk dan identitas

**Pinguin** memiliki kepala kubus tinggi berwarna navy gelap, bib wajah putih dengan lekuk grafis, paruh kotak kuning, flipper pendek yang memegang kemudi, dan kaki kuning. **Kapsul** memakai monocoque turquoise membulat, hidung bulb pendek, pelindung roda melengkung dengan ketebalan nyata, kaca asap opak, coaming krem dan pod pendorong belakang.

**Beruang** memiliki kepala lebar dengan rahang sedikit menyempit, telinga kotak pendek, muzzle krem kecil, hidung kotak dan lengan/paw lebih kokoh. **Buggy** memakai kap bersudut, grille, bumper pelindung, fender lebar, roll hoop belakang, suspensi terlihat dan ban dengan lug kotak. Warna tembaga/coral berbeda dari dua kendaraan lainnya.

**Kelinci** memiliki kepala kubus lebih ringkas, telinga panjang berujung balok, inset pink, pipi grafis, gigi depan kecil dan ekor kubus krem di sisi belakang agar tidak masuk ke sandaran kursi. **Formula** memakai lantai dan hidung meruncing, roda terbuka, sidepod, wishbone serta sayap depan/belakang. Livery violet, ivory dan pink membedakannya dari Kapsul dan Buggy.

Ketiganya dibangun ulang melalui Blender Python, tanpa subdivision/remesh organik atau bulu realistis. Builder berbagi alat dan kelas material, tetapi memakai volume kepala, anatomi dan struktur kendaraan yang berbeda. Material memakai warna vertex dengan kelas cat, trim, logam, karakter, karet, lampu dan kaca. Tidak ada tekstur model baru yang berat. Kaca opak dipilih agar cocok dengan renderer yang ada tanpa menambah sorting transparansi.

## Bukti visual

Semua gambar berasal dari **RaceRenderer game dan GLB sebenarnya**, tanpa ilustrasi generatif atau retouch bentuk model. Gambar gabungan hanya disusun/diubah ukurannya untuk perbandingan; PNG asli dipertahankan.

- [Acuan Kucing + tiga pasangan baru](comparisons/batch1-style-lineup.jpg).
- Before–after: [Pinguin](comparisons/nara/comparison-sheet.jpg), [Beruang](comparisons/bimo/comparison-sheet.jpg), [Kelinci](comparisons/sora/comparison-sheet.jpg).
- [Depan/samping/belakang karakter](comparisons/character-turnarounds.jpg) · [depan/samping/belakang kendaraan](comparisons/vehicle-turnarounds.jpg) · [tiga ekspresi](comparisons/expressions.jpg).
- Untuk setiap ID `nara`, `bimo`, `sora`, `before/<id>/` dan `after/<id>/` menyimpan hero, depan/samping/belakang, face, karakter saja, kendaraan saja, garasi dan kamera balapan. Filter karakter/kendaraan menyembunyikan primitive lain pada GLB yang sama, bukan mengganti model.
- `after/<id>/garage-close-desktop.png`, `garage-close-mobile.png`, `race-desktop.png`, `race-mobile.png` dan `results-win.png` memperlihatkan UI game sebenarnya. `grip-turn-jump.png` memperlihatkan pose kemudi maksimum/jump sebagai pemeriksaan kontak paw.
- [Kamera pembanding](camera-verification.json) memverifikasi 33 sudut model dan 6 sudut garasi/balapan dengan matriks view/projection, ukuran canvas, skala, cahaya dan waktu/pose setara. Pengambilan UI native close-up/HP tersimpan terpisah karena framing disesuaikan untuk jenis karakter.

Evaluasi render awal mengarahkan koreksi pada hidung Kapsul yang lebih membulat, shroud roda yang tertutup/berketebalan, lantai Formula yang meruncing, dukungan fender Buggy, posisi ekor di luar sandaran, dan tombol ekspresi yang dipindahkan ke panel keterangan agar tidak mendekati mulut pada HP. Rekaman tahap awal disimpan pada `evaluation/first-pass/`.

## Integrasi, pose dan ekspresi

Nama karakter/kendaraan, ID file asli, status unlock dan atribut gameplay tidak berubah. AssetData mengganti tiga GLB/avatar lama, menambahkan tiga LOD low dan tiga avatar senang. Model yang sama dipakai ulang oleh garasi, pemain, AI dan ghost; payload model baru tidak diduplikasi di HTML.

Pusat roda tetap **X ±0,59; Y 0,205; Z depan 0,48 / belakang −0,56**, wheelbase **1,04**, track width **1,18**, radius nominal **0,205**, origin dan collider metadata **1,6 × 1,3 × 1,6**. Pivot serta hubungan parent rig asli dipertahankan; `driver_pose`, bagian wajah dan `steering` adalah tambahan. Bentuk bodi/pelek berubah dalam envelope kart yang dicatat pada `asset-metrics.json`; bounds visual tidak diklaim identik. Kode collision dan ukuran lintasan tetap sama.

Kursi, paha, posisi kedua paw dan kemudi menggunakan titik kontak tetap. Roda depan mengikuti steering, roda berputar mengikuti laju, badan melakukan lean serta respons jump/landing ringan. Reaksi memakai data simulasi yang sudah ada, tanpa mengubahnya. Kedip, telinga, ekor, body/suspensi, reaksi benturan dan timer landing memakai waktu simulasi, sehingga seluruh animasi membeku saat pause/soal.

Garasi memiliki Mobil + Karakter / Close-up Karakter, drag, wheel/pinch, reset, auto-rotate dan pilihan Ramah/Senang/Terkejut untuk tiga model baru. Close-up Kelinci mempertahankan telinga panjang; pengguna dapat pinch/scroll lebih dekat ke wajah. Kamera balapan tetap memakai jarak/rumus yang sama. Benturan/bubble/slip memicu ekspresi terkejut; kemenangan memilih senang. Layar hasil asli memakai piala, sehingga render avatar senang ditambahkan saat kemenangan baru; piala dan penilaian tetap dipertahankan.

GLB/Blender dibuka pada ekspresi normal. Tiga grup varian nonaktif memakai skala default nol agar tidak menumpuk pada viewer glTF standar. Renderer rigid game memilih varian melalui `extras.expression` dan memakai pose geometri yang sudah dibake. Grup yang tidak aktif dilewati sebelum draw call. Untuk mengedit varian di Blender, pulihkan skala grup varian menjadi 1 dan nonaktifkan grup normal yang terkait. Pipeline ekspor kompatibel berada di builder; GLB tidak berisi klip skeletal atau rig deformasi produksi. Scene Blender memakai Z-up; file GLB/game memakai Y-up.

## Ukuran dan beban terukur

HTML final **19.539.444 byte (19,54 MB desimal)**, di bawah target **25.000.000 byte**. Baseline Kucing 18.772.016 byte; pertumbuhan sekitar 4,09%. Seluruh enam GLB memiliki nol tekstur tertanam dan memakai warna vertex.

| Pasangan | GLB high / low, byte | Segitiga tersimpan high / low | Segitiga benar-benar digambar pada ekspresi normal, high / low | Draw call warna normal |
|---|---:|---:|---:|---:|
| Pinguin–Kapsul | 303.996 / 169.568 | 10.966 / 5.450 | 10.042 / 5.058 | 23 |
| Beruang–Buggy | 432.968 / 209.392 | 16.008 / 6.816 | 15.004 / 6.404 | 25 |
| Kelinci–Formula | 364.732 / 192.980 | 13.366 / 6.286 | 12.146 / 5.786 | 25 |

Segitiga tersimpan mencakup semua varian ekspresi; kolom draw aktual mengecualikan grup nonaktif. Angka draw call adalah model terisolasi, satu pass warna, tidak termasuk arena, bayangan atau partikel. Sebelum redesign, GLB high Pinguin/Beruang/Kelinci masing-masing 15.630/16.684/15.334 segitiga. Buggy tetap memiliki lebih banyak detail kendaraan untuk tread/fender/cage; LOD menurunkan biaya saat kualitas rendah atau jarak lebih dari 24 unit. Kedua LOD GPU dibuang ketika karakter tidak diperlukan lagi.

[Metrik file/bounds](asset-metrics.json) dan [hitungan draw/rig aktual](rig-tests.json) disertakan. Tidak ada klaim FPS/GPU perangkat nyata. Pengujian menggunakan Chromium cloud; HP adalah emulasi viewport/sentuhan, bukan perangkat fisik.

## Hasil uji

- [Scope](scope-verification.json): core, initial data, UI utama dan scenery identik; kode kamera/dunia balapan identik setelah mengecualikan tambahan parameter model. Shader GPU, loader dan jalur material bersama tetap sama. Kucing HTML/GLB/sumber serta `index.html` identik dengan baseline. Sebanyak 62 aset lama tetap persis; hanya enam asset lama Batch 1 diganti dan enam varian baru ditambahkan.
- [Render terlindungi](unchanged-renders.json): 15 perbandingan menghasilkan piksel identik, termasuk Kucing high/low, dua mode garasinya, mobil sport saja, dan sepuluh karakter Batch 2–4.
- [Core](core-test-results.json): tujuh kelompok pemeriksaan PG, materi/jumlah soal, JSON persistence, CSV round trip, stage/AI, Grand Prix mastery/retry/completion, drift, jump, kuis, buff, ghost, progres dan hasil.
- [Browser game](test-results.json): 17 pemeriksaan Ruang Guru, 14 model, keyboard A/D, jump, pause/soal, buff benar dan pemakaiannya, kelanjutan balapan, LOD, sentuhan dan offline.
- [Garasi + balapan](preview-race-tests.json): enam kasus, yaitu tiga karakter pada desktop 1440×1000 dan HP 390×844. Memeriksa avatar, framing wajah/telinga, toolbar/footer, tiga ekspresi, drag/zoom/reset/auto, kamera balapan, pause/soal yang membekukan semua matriks model baru, buff, lanjut balapan dan avatar kemenangan. Tidak ada error JavaScript, console error atau WebGL pada enam kasus ini.
- [Rig/LOD](rig-tests.json): animasi setiap pasangan, pilihan grup ekspresi, landing termasuk transisi ketinggian kecil, prioritas senang saat menang, seleksi LOD jarak/kualitas dan pelepasan buffer. Pusat paw berada dalam envelope genggaman saat steer ±0,42 dan jump 0–3; jarak maksimum ke rim sekitar 5,25 cm untuk paw selebar 12,5 cm. Ini fixture titik kontak ditambah inspeksi gambar, bukan solver clipping seluruh mesh.
- [Ekspor Ruang Guru](export-tests.json): 13 pemeriksaan, termasuk keenam GLB cocok dengan hasil builder, reset kontrol yang ikut terkloning, ekspresi/close-up dan masuk balapan pada browser offline tanpa permintaan aset HTTP.
- [Offline](offline-test-results.json): jaringan browser dimatikan, byte HTML lokal dipasok langsung, balapan berjalan tanpa unduhan aset. Browser cloud membatasi pembukaan `file://`, sehingga jalur itu tidak diklaim teruji langsung.
- [GLB](glb-validation.json): enam GLB berhasil diimpor ulang oleh Blender; posisi/normal/warna/index diperiksa, original pivot/parent/collider dipertahankan, dan varian nonaktif benar-benar tersembunyi pada impor standar.

Smoke browser memperpendek countdown, menempatkan pemain dekat gerbang soal, serta memakai fixture jawaban/garis finis untuk menguji UI hasil. Ini bukan penyelesaian semua lap/Grand Prix secara manual. Impor/ekspor CSV/JSON, ghost dan progres diuji pada core; tidak semua variasi perangkat, bank soal atau seluruh Grand Prix dijalankan manual. Kebutuhan persetujuan batch berikutnya tidak dilewati.

## Reproduksi di repository

Dari root checkout, dengan Blender 4.3+, Python 3, Node, Playwright dan Chromium:

```sh
blender -b --python-exit-code 1 --python visual-upgrade/batch1/source/build_batch1.py
python3 visual-upgrade/batch1/source/assemble_batch1.py --preview
python3 -m http.server 8000 --bind 127.0.0.1 --directory .
```

Di terminal lain:

```sh
node visual-upgrade/batch1/source/capture_avatars.cjs
python3 visual-upgrade/batch1/source/assemble_batch1.py
blender -b --python-exit-code 1 --python visual-upgrade/batch1/source/validate_models.py
python3 visual-upgrade/batch1/source/verify_scope.py
node visual-upgrade/batch1/source/test_core.cjs
node visual-upgrade/batch1/source/test_game.cjs
node visual-upgrade/batch1/source/test_rigs.cjs
node visual-upgrade/batch1/source/test_preview_and_races.cjs
node visual-upgrade/batch1/source/test_export.cjs
node visual-upgrade/batch1/source/test_unchanged_render.cjs
```

`capture_models.cjs before|after` dan `capture_game.cjs before|after` membuat gambar nyata. `make_comparisons.py` memverifikasi kamera dan menyusun perbandingan; `measure_assets.py` mencatat ukuran/bounds. `build_release.py` memeriksa laporan dan checksum sebelum membuat ZIP. Skrip browser memakai lokasi Playwright `/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright` dan Chromium `/usr/bin/chromium` yang tersedia di cloud; sesuaikan pada mesin lain.

Baseline lama tersimpan di Git serta `before/models/`. Nama branch tetap `dev/race-quest-cat-sport-visual-upgrade`. Tidak ada merge ke `main`, perubahan `index.html`, atau deployment Pages.
