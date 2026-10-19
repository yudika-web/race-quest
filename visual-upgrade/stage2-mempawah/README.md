# Stage 2 — Mempawah · Jalanan Taman

Hasil pengembangan dari Stage 1 `8bc787d01fb1a5a96ec177955b8378aea32cd57d`. Hanya visual Stage 2 diperbarui; Stage 1 Pontianak dan Stage 3 tetap utuh.

- **[ZIP playable](../../race-quest-pro-mempawah-stage2-playable.zip)** — ekstrak dan buka `race-quest-pro-mempawah-stage2.html`.
- [HTML mandiri](../race-quest-pro-mempawah-stage2.html) · [ZIP review](../../race-quest-pro-mempawah-stage2-review.zip).
- Pada menu Mulai, pilih **Stage: Mempawah · Jalanan Taman**. Bank bawaan, profil dan unlock tidak dimodifikasi. Versi ini juga memuat Stage 1 Pontianak terbaru.
- Before–after: [Tugu Pak Tani](comparisons/comparison-pak-tani.jpg), [Keraton Mempawah](comparisons/comparison-keraton.jpg), [jalanan dan overview](comparisons/comparison-garden.jpg), [pilihan cerah dan gap asli](comparisons/comparison-weather-gap.jpg).
- Render dengan antarmuka: [desktop](smoke/race-desktop.png), [HP emulasi](smoke/race-mobile.png), [soal](smoke/quiz-desktop.png).

## Desain dan batas perubahan

Bahasa bentuk dari referensi diterjemahkan menjadi balok dengan bevel ringan, warna taman hijau, hamparan bunga, palem, jalur pejalan kaki krem, kanstin merah-putih, lampu taman hijau/emas, pagar rendah dan tiga gazebo. Terdapat 54 penempatan pohon taman, 18 palem di lintasan, 30 kelompok semak, 60 hamparan bunga dan 28 lampu di sepanjang jalan; detail tambahan ditata di dalam area landmark. Geometri memakai batch material bersama dan tekstur lokal kecil.

**Tugu Pak Tani**: patung emas blocky, topi tani, pose memegang cangkul dan hasil panen, alas bertingkat, plaza melingkar, bangku dan bunga. **Keraton Mempawah/Amantubillah**: fasad hijau, trim emas/krem, atap merah bertingkat, sayap samping, pedimen berpola sederhana, jendela/pintu, teras berpagar, tangga depan, palem, taman dan jalur penghubung ke promenade. Keduanya merupakan interpretasi stylized berdasarkan referensi pengguna, bukan rekonstruksi historis atau peta geografis berskala.

ID penyimpanan Stage 2 tetap `kapuas`; hanya nama tampil berubah. Rute, panjang, tanjakan, obstacle, ramp `.675`, gap `.69`, collision dan start gate tetap asli. Marka dan jalur taman tidak menutup celah jalan. Dekorasi desa, bebatuan/pepohonan generik, jembatan dan terowongan dekoratif diganti dengan taman; hazard balapan sungguhan tetap dirender oleh engine yang sama.

**Hujan bawaan dan efek jalan licin tetap berlaku**, karena memengaruhi handling. Mayoritas screenshot memakai hujan bawaan. Satu perbandingan memakai pilihan cuaca Cerah yang memang sudah tersedia, pada kedua versi dengan kamera dan cuaca setara. Tidak ada penggantian cuaca terselubung dalam distribusi. Karakter, kendaraan, AI, ghost, soal, buff, progres, harga unlock, audio dan data profil awal tidak diubah. Tidak ada animasi atau clock lingkungan baru; seluruh gerak masih mengikuti clock simulasi engine.

## Ukuran dan biaya renderer

HTML **23.378.794 byte (23,38 MB desimal)**, bertambah **16.250 byte** dari Stage 1. Tetap di bawah 25.000.000 byte. Semua 94 payload aset lama identik; tidak ada GLB baru, CDN atau unduhan aset saat bermain.

Lapisan taman: **83.250 segitiga**, **26 submission mesh warna**, **12 submission bayangan**. Tiga tekstur yang dibuat lokal sekali: aspal 128², dua papan nama 512×128; data RGBA dasar 589.824 byte sebelum mipmap. Ini hanya lapisan taman, tidak termasuk jalan/terrain/karakter/fitur engine. Permukaan promenade, marka, bunga datar dan alas monumen tidak menjadi caster agar permukaan datar lebih bersih; tetap menerima bayangan dari objek lain. Detail geometri taman tetap sederhana dan sama pada seluruh kualitas; LOD kendaraan/karakter dan kualitas bayangan tetap memakai sistem asli.

Pada satu fixture balapan tetap (`u=.12`, high, waktu 2 detik): submission mesh warna **387 → 220**, segitiga warna **245.505 → 153.031**; submission depth **47 → 22**, segitiga depth **149.741 → 100.791**. Angka ini menghitung submission renderer, bukan semua API draw call termasuk langit/partikel. Seluruh sampel high/medium/low tersedia dalam [scene-tests.json](scene-tests.json). Tidak dilakukan pengukuran FPS atau HP fisik.

## Pengujian

- [Scope dan hash](scope-verification.json): 1.345 file historis di `index.html`/`visual-upgrade` identik dengan baseline; semua 94 payload aset identik. Menghapus script taman baru dan membalik satu label nama menghasilkan HTML baseline yang byte-identik, termasuk seluruh script Stage 1, renderer, UI dan clock animasi.
- [Render terlindungi](scene-tests.json): **18** frame Stage 1/3 identik piksel (dua stage × tiga posisi × high/medium/low). Sembilan frame Stage 2 berubah sesuai target. Tidak ada error JavaScript, console atau WebGL. Jarak horizontal minimum vertex struktur taman dari centerline adalah **8,207 unit**, dibanding lebar jalan setengah 5 dan kanstin sampai 5,5. Landmark serta footprint dekorasi berada di luar envelope balapan.
- Resource cleanup: 80 buffer dan tiga tekstur taman dihapus saat pindah ke Stage 1. Transisi kembali ke taman menghapus resource Stage 1 dengan benar; rebuild memiliki jumlah resource milik taman yang sama. Stage 3 pulih tanpa objek kota/taman.
- [Render semua karakter](unchanged-renders.json): **18 kasus** identik, mencakup seluruh 14 pasangan, Kucing high/low, dua mode garasi Kucing dan mobil Kucing saja.
- [UI desktop dan sentuh](test-results.json): Stage 2 dipilih melalui UI asli; hujan bawaan dan kedua landmark diverifikasi. Bank soal, semua 14 GLB, avatar, A kiri/D kanan, jump/landing, pause/resume, soal yang membekukan pemain/AI/clock, jawaban benar, buff, low LOD dan layout garasi HP lulus. Kontrol sentuh kiri lulus pada emulasi 390×844.
- [Core](core-test-results.json): persistensi materi/jumlah soal, impor/ekspor CSV, AI bertingkat, Grand Prix/retry/ketuntasan tiga ronde secara unit, drift/jump, quiz freeze, buff/item, hasil, ghost dan progres lulus. Kasus balapan core dijalankan pada Stage 2.
- [Offline](offline-test-results.json): jaringan dinonaktifkan, hanya HTML utama disediakan dari byte lokal, Stage 2 mulai balapan dengan dua landmark dan tanpa permintaan aset HTTP.
- [Ekspor guru](export-tests.json): pilihan Stage 2 disimpan melalui Ruang Guru; HTML hasil download aktual mempertahankan bank dengan pengaturan tersebut, seluruh hash aset dan dua lapisan lingkungan. Muat ulang offline, kontrol close-up/ekspresi dan kedua landmark dalam balapan lulus.
- [Bukti screenshot](capture-report.json): delapan sudut before–after dengan matriks view/projection dan resolusi identik. Semuanya berasal dari RaceRenderer sebenarnya. Kamera hero/overview, posisi dekat ramp dan kondisi cuaca cerah hanyalah fixture dokumentasi; kamera balapan dan data distribusi tidak diubah.

Batas pengujian: Chromium/SwiftShader cloud dan HP emulasi, bukan perangkat fisik. `file://` diblokir administrator browser cloud; offline diuji dengan jaringan nonaktif dan byte HTML lokal. Tidak memainkan seluruh Grand Prix secara manual; akses soal, ramp dan posisi kamera menggunakan fixture terkendali. Tidak ada jaminan seluruh sudut/kombinasi balapan telah diperiksa manual.

## Build ulang

Sumber editable: [source/garden.js](source/garden.js). Memakai kembali helper bevel/beam/texture/label Stage 1 melalui subclass, tanpa mengedit berkas Stage 1 atau menggandakan engine. Lingkungan dibangun prosedural saat world dibuat; tidak membutuhkan Blender/GLB terpisah.

Dari root repository dengan hasil Stage 1 tersedia:

```sh
python3 visual-upgrade/stage2-mempawah/source/assemble.py
python3 visual-upgrade/stage2-mempawah/source/verify_scope.py
node visual-upgrade/stage2-mempawah/source/test_core.cjs
python3 -m http.server 8000 --bind 127.0.0.1
```

Dengan server aktif, jalankan `node .../source/test_game.cjs`, `test_scene.cjs`, `test_unchanged_render.cjs`, `test_export.cjs`. Adapter menggunakan suite Batch 1 yang tidak diedit. Skrip mengacu ke Playwright dan Chromium runtime cloud; sesuaikan path pada mesin lain. Screenshot: `node .../source/capture.cjs`, lalu `python3 .../source/make_comparisons.py` (Pillow). Paket: `python3 .../source/package.py`. Sumber dalam ZIP review perlu checkout repository/baseline untuk membangun ulang; HTML dalam kedua ZIP dapat dimainkan mandiri.

Tidak ada merge ke `main`, perubahan `index.html` online atau deployment. Stage 3 belum didesain ulang.
