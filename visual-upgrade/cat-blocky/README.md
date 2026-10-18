# Kucing blocky — RACE QUEST

Baseline pembanding: `276792553e913520119038cac5c9512035751d86`, pada branch `dev/race-quest-cat-sport-visual-upgrade`. Revisi ini membangun ulang Kucing mengikuti lembar referensi terbaru: kubus membulat, badan chibi pendek, wajah grafis, dan tabby sederhana. Mobil biru dipertahankan.

## Buka dan tinjau

- [HTML playable offline](../race-quest-visual-upgrade.html). Seluruh model, gambar, suara dan kode tertanam. ZIP HTML di root proyek: `race-quest-playable.zip`; ekstrak lalu buka `RACE-QUEST-Kucing-Blocky.html`.
- [GLB high](../race-quest-cat-sport.glb) / [GLB low](../race-quest-cat-sport-low.glb): Kucing baru + mobil yang sama, dengan pivot yang sama.
- [Sumber Blender](../source/race-quest-cat-sport.blend) / [builder Kucing](../source/refine_cat.py) / [builder dan exporter](../source/build_cat.py).
- [Perbandingan garasi](comparison-garage.jpg), [close-up wajah](comparison-face.jpg), [kamera balapan](comparison-race.jpg), [depan](comparison-front.jpg), [samping](comparison-profile.jpg), [belakang](comparison-rear.jpg).
- [Lembar perbandingan game](cat-blocky-sheet.jpg) / [turnaround Kucing saja](cat-turnaround-sheet.jpg). Render turnaround menyembunyikan mobil agar tubuh dan anggota badan terlihat; pose tetap duduk.
- Close-up aktual: [desktop](after/garage-close-desktop.png) / [HP](after/garage-close-mobile.png). Mode Mobil + Karakter tetap tersedia; geser untuk memutar, scroll/pinch untuk zoom, tombol ↻ untuk rotasi otomatis dan ⟲ untuk reset.

## Perubahan bentuk yang terlihat

Kepala oval, pipi/moncong organik dan mata berlapis diganti kepala kubus dengan bidang datar dan tepi membulat. Bagian krem merupakan warna pada mesh kepala yang sama, tanpa pelat moncong terpisah. Mata berupa persegi panjang hitam dengan highlight persegi; hidung pink kecil dan mulut senyum grafis dengan lidah. Telinga berupa prisma segitiga dengan inset pink.

Tubuh menjadi balok pendek, dengan lengan bertekuk dari balok pendek, paw krem berbentuk kotak, jempol sederhana, paha duduk dan kaki pendek. Ekor memakai penampang kotak berpojok kecil, lengkungan sederhana, loreng lebar dan ujung krem. Loreng kepala mengikuti bagian atas, sisi dan belakang kubus. Bulu tidak memakai rambut/tekstur berat. Ikon pemilih Kucing juga diambil dari render model baru, bukan ilustrasi Kucing lama.

Evaluasi render pertama menemukan mask wajah seperti pelat terpisah, framing close-up HP kurang besar, dan ujung ekor perlu menutup sambungan dengan lebih bersih. Koreksi memakai warna pada mesh kepala, kamera close-up khusus Kucing yang lebih dekat, dan penutup ekor yang cukup menutupi ujung penampang. [Render tahap pertama](evaluation/first-pass/) disimpan sebagai catatan. Kepala kubus dan siluet balok tetap dipertahankan; tidak memakai subdivision/remesh organik.

## Ukuran dan biaya gambar

| Ukuran | Sebelum, commit 2767925 | Kucing blocky |
|---|---:|---:|
| HTML mandiri | 19.796.352 byte | 18.772.016 byte (−5,17%) |
| GLB gabungan high / low | 1.162.168 / 528.680 byte | 643.708 / 285.268 byte |
| Segitiga Kucing high / low | 28.925 / 11.875 | 7.804 / 2.200 |
| Segitiga mobil high / low | 20.931 / 8.678 | 20.931 / 8.678 |
| Segitiga gabungan high / low | 49.856 / 20.553 | 28.735 / 10.878 |
| Draw call model satu pass warna | 44 | 42 |

Pengurangan segitiga Kucing 73,02%; bukti redesign adalah perbedaan bentuk pada render, bukan jumlah poligon. Bevel low memakai satu segmen pada bagian Kucing yang mendukungnya; kepala mempertahankan siluet kubus yang sama. Game tetap memilih LOD low pada kualitas rendah dan model Kucing jauh. [Metrik aset](metrics.json) dan [instrumentasi render](render-metrics.json) disertakan. Waktu `gl.finish` adalah observasi wall-time Chromium cloud, bukan pengukuran GPU/FPS perangkat nyata; GPU timer tidak tersedia.

## Validasi

- [Scope](scope-verification.json): 28 batch mobil di setiap GLB sama persis pada posisi, normal, indeks dan material; semua pivot sama. Core game, UI utama, scenery, renderer/kamera balapan dan kode animasi rigid identik. Aset lain sama, kecuali dua LOD Kucing dan portrait Kucing.
- [Render kompatibilitas](unchanged-renders.json): mobil saja dan 13 karakter lain menghasilkan piksel identik pada kamera, cahaya dan pose uji 256×256 yang sama.
- [Animasi](animation-tests.json): kedip, kedua telinga, ekor, lean, respons jump, kemudi dan putaran roda berjalan; matriks seluruh bagian identik saat waktu simulasi beku. Pusat paw tetap dalam envelope genggaman saat lean/jump (jarak maksimum ke rim sekitar 4,2 cm, ukuran paw sekitar 12,5 cm). Pemeriksaan ini dilengkapi render depan/samping/belakang, bukan solver tabrakan seluruh mesh.
- [Garasi desktop/HP](preview-tests.json): dua mode, drag mouse/sentuhan, wheel/pinch, reset, rotasi otomatis, telinga tidak tertutup toolbar, tombol balapan tidak bertumpuk, kamera balapan tidak terpengaruh.
- [Browser game](../test-results.json): Ruang Guru, 14 model, A kiri/D kanan, jump, jeda, kuis, pemberian/pemakaian buff, lanjut balapan, LOD dan kontrol sentuh. Tidak ada error JavaScript pada pemeriksaan desktop/HP.
- [Core](../core-test-results.json): materi/jumlah soal, JSON persistence, CSV impor/ekspor, stage, AI bertingkat, Grand Prix mastery/retry/completion, drift, jump, kuis, buff, hasil, ghost dan progres.
- [Offline](../offline-test-results.json) dan [ekspor HTML dari Ruang Guru](export-tests.json): browser offline tetap masuk balapan tanpa permintaan HTTP aset dan tanpa error JavaScript.
- [Impor GLB Blender](../glb-validation.json): kedua GLB dapat diimpor kembali; normal unit dan warna vertex dalam rentang sah.
- [Kamera pembanding](camera-verification.json) dan [turnaround](turnaround-cameras.json): matriks view/projection, ukuran canvas, cahaya, skala dan waktu/pose disamakan. Screenshot adalah render game sebenarnya, tanpa retouch bentuk karakter.

Pengujian HP menggunakan emulasi viewport dan sentuhan, bukan HP fisik. Browser cloud melarang membuka `file://`; pengujian offline memasok byte HTML lokal langsung ke browser dengan jaringan dimatikan. Smoke test memperpendek countdown dan memosisikan pemain dekat gerbang soal; tidak menjalankan seluruh Grand Prix secara manual. GLB memakai pivot rigid dan animasi prosedural game, tanpa klip skeletal; sumber Blender tetap dapat diedit. `index.html` online dan `original.html` tidak diubah.

## Reproduksi

Dari root repository:

```sh
blender -b --python-exit-code 1 --python visual-upgrade/source/build_cat.py
python3 visual-upgrade/source/assemble.py
python3 -m http.server 8000 --bind 127.0.0.1
```

Di terminal lain, `node visual-upgrade/source/capture_blocky_avatar.cjs` lalu `python3 visual-upgrade/source/assemble.py` untuk memperbarui portrait jika bentuk diubah lagi. Jalankan `test_core.cjs`, `test_game.cjs`, `test_blocky_preview.cjs`, `test_blocky_animation.cjs`, `test_blocky_export.cjs`, dan `verify_blocky_unchanged.cjs` di folder `visual-upgrade/source`. `capture_blocky.cjs before|after` dan `capture_blocky_turnaround.cjs` mengambil bukti visual; `make_blocky_comparisons.py` menyusunnya. `verify_blocky.py`, `measure_blocky.py`, `measure_blocky_render.cjs`, dan Blender `validate_cat_glb.py` mencatat validasi. Playwright/Chromium memakai lokasi runtime yang tersedia di cloud; sesuaikan lokasinya pada mesin lain.

`python3 visual-upgrade/source/build_release.py` mengemas HTML dan paket lengkap setelah laporan uji lolos. Hash isi disimpan pada `SHA256SUMS.json`. Riwayat revisi organik sebelumnya tetap tersimpan di `cat-redesign/` dan commit baseline, tanpa mengganti game online.
