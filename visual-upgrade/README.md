# RACE QUEST — Kucing blocky dan Sport biru

Kucing terbaru dibangun ulang menjadi karakter chibi blocky mengikuti lembar referensi: kepala kubus membulat, mata persegi, wajah krem sederhana, telinga segitiga, lengan/paw pendek dan ekor kotak melengkung. Mobil biru dipertahankan. [Lihat hasil dan pengujian lengkap](cat-blocky/README.md), [perbandingan game](cat-blocky/cat-blocky-sheet.jpg), [depan/samping/belakang Kucing](cat-blocky/cat-turnaround-sheet.jpg), dan [close-up HP](cat-blocky/after/garage-close-mobile.png).

Buka **race-quest-visual-upgrade.html**, atau ekstrak `../race-quest-playable.zip` lalu buka **RACE-QUEST-Kucing-Blocky.html**. Semua aset tertanam dan tidak membutuhkan CDN atau backend. `../index.html` dan salinan asli `original.html` tidak diubah.

## Hasil terbaru

- [HTML playable mandiri](race-quest-visual-upgrade.html).
- [GLB high](race-quest-cat-sport.glb) dan [GLB low](race-quest-cat-sport-low.glb), termasuk mobil, Kucing dan pivot animasi.
- [Sumber Blender 4.3](source/race-quest-cat-sport.blend), [builder Kucing](source/refine_cat.py), [builder/exporter gabungan](source/build_cat.py), dan [assembler HTML](source/assemble.py).
- [Perbandingan garasi](cat-blocky/comparison-garage.jpg), [wajah](cat-blocky/comparison-face.jpg), [balapan](cat-blocky/comparison-race.jpg), [depan](cat-blocky/comparison-front.jpg), [samping](cat-blocky/comparison-profile.jpg), [belakang](cat-blocky/comparison-rear.jpg).
- Garasi menyediakan **Mobil + Karakter** dan **Close-up Karakter**. Geser untuk memutar, scroll/pinch untuk zoom; rotasi otomatis dapat dihentikan atau dilanjutkan. Close-up Kucing dibesarkan tanpa mengubah kamera balapan atau framing karakter lain.
- `../race-quest-visual-upgrade.zip` berisi HTML, model, sumber, hasil uji dan gambar. `cat-redesign/`, `cat-refinement/` dan `comparisons/` menyimpan riwayat sebelumnya; bukti terbaru berada di `cat-blocky/`.

## Perubahan dan integrasi

Kucing organik diganti volume kubus dengan bidang datar dan tepi membulat kecil. Warna krem wajah berada pada mesh kepala yang sama; tidak ada bola pipi/moncong atau pelat wajah. Mata kotak dan mulut senyum grafis terbaca pada ukuran kecil. Tabby berupa garis lebar pada kepala/tubuh/ekor, dengan warna vertex ringan dan tanpa bulu berat. Portrait pemilih Kucing dirender dari GLB baru.

Seluruh geometri/material mobil high dan low sama dengan baseline `2767925`. Mobil tetap mempunyai kap/spatbor melengkung, cat sian, garis putih, kokpit, jok, setir, lampu, intake, splitter, diffuser, knalpot, spoiler, ban berprofil dan pelek. Kaca opak menghindari masalah sorting transparansi renderer.

Pusat roda tetap **X ±0,59; Y 0,205; Z depan 0,48 / belakang −0,56**, radius **0,205**, beserta origin dan pivot driver/mata/telinga/ekor. Paw duduk di sisi rim setir dan paha menyentuh jok. Kedip, gerak telinga/ekor, lean, suspensi dan respons jump memakai waktu simulasi sehingga membeku saat jeda/soal. Animasi prosedural berada di renderer; GLB tidak menyimpan klip skeletal. Sumber Blender memakai Z-up, ekspor game memakai Y-up.

## Ukuran dibanding revisi sebelumnya

| Ukuran | Sebelum (2767925) | Blocky |
|---|---:|---:|
| HTML | 19.796.352 byte | 18.772.016 byte |
| GLB high / low | 1.162.168 / 528.680 byte | 643.708 / 285.268 byte |
| Segitiga Kucing high / low | 28.925 / 11.875 | 7.804 / 2.200 |
| Segitiga gabungan high / low | 49.856 / 20.553 | 28.735 / 10.878 |
| Batch satu pass warna model | 44 | 42 |

HTML berkurang 5,17%; segitiga Kucing berkurang 73,02%. Segitiga mobil tetap 20.931 / 8.678. LOD dipilih pada kualitas rendah atau Kucing jauh. Hitungan tidak mencakup arena/pass bayangan/partikel. [Metrik baseline terbaru](cat-blocky/metrics.json) dan [instrumentasi render](cat-blocky/render-metrics.json) tersedia. `render-metrics.json` di root membandingkan game asli tahap awal. Wall-time Chromium cloud bukan FPS perangkat nyata; GPU timer tidak tersedia.

## Validasi dan batas pengujian

Pengujian browser mencakup Ruang Guru, 14 model, A kiri/D kanan, sentuhan, jump, pause, kuis, buff benar, pemakaian buff dan lanjut balapan. Pemain, AI dan waktu animasi membeku saat pause/soal. Core mencakup PG, materi/jumlah soal, persistence, CSV, stage, AI, Grand Prix, drift, ghost, progres dan hasil. Kode aturan/UI/scenery, renderer balapan dan animasi rigid tidak berubah. Aset selain dua GLB Kucing dan portrait Kucing identik. Render mobil dan 13 karakter lain identik pada kamera uji.

Dua mode garasi diuji pada desktop 1440×1000 dan HP emulasi 390×844, termasuk mouse, drag sentuh, wheel/pinch, reset dan rotasi. Tidak ada error JavaScript/WebGL pada pemeriksaan ini. HTML dan hasil ekspor Ruang Guru berjalan dengan jaringan dimatikan, tanpa unduhan aset. Browser cloud melarang `file://`, sehingga pengujian offline memasok byte lokal langsung ke browser. HP fisik/FPS nyata dan seluruh Grand Prix manual belum diuji; browser smoke memakai fixture countdown/gerbang, sementara aturan Grand Prix diuji pada core.

Laporan terbaru: [cat-blocky/README.md](cat-blocky/README.md), `test-results.json`, `core-test-results.json`, `offline-test-results.json`, dan `glb-validation.json`. Normal GLB dan warna vertex diperiksa, kedua GLB diimpor ulang dengan Blender. Perbandingan lama–baru memakai kamera, ukuran canvas, skala, pencahayaan dan pose setara.

Petunjuk build/test ada pada [cat-blocky/README.md](cat-blocky/README.md#reproduksi). Pasangan ini menjadi acuan gaya blocky; 13 karakter lain belum didesain ulang.
