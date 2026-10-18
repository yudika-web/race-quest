# Tabby kitten redesign + interactive garage

Baseline: commit `12a3a6f700430f0a39dd4eb3a8ed9ba480106b9c`, branch `dev/race-quest-cat-sport-visual-upgrade`. Model, material and source continue from the previous work. The sport car and all other characters have been retained.

## Perubahan bentuk yang dapat dibandingkan

- Kepala berganti dari bentuk tinggi dengan mata oval tegak menjadi bentuk lebih lebar pada pipi, menyempit ke rahang/dagu, dengan mahkota dahi membulat. Volume moncong dan jembatan hidung dibentuk pada permukaan tengkorak.
- Mata berganti menjadi almond besar yang sedikit miring ke luar, dengan kelopak yang mengikuti socket, iris madu bergradasi, pupil gelap dan catchlight. Ini mengubah susunan wajah, bukan hanya kepadatan mesh.
- Moncong mengikuti pipi; hidung menjadi bentuk hati/segitiga kecil; senyum lebih lebar dengan sudut naik, lidah dan dua gigi kecil.
- Telinga menyapu keluar, memiliki ketebalan, bagian dalam cekung serta rim membulat. Pangkal ditanam ke volume kepala untuk menghindari lapisan yang tampak menempel pada pelipis.
- Tubuh lebih ringkas dan leher lebih pendek. Lengan meruncing melalui siku/pergelangan ke palm, dengan tiga digit melengkung dan thumb yang berlawanan pada setir.
- Ekor berganti dari kurva mendatar menjadi kurva S yang mengecil ke ujung dan berada di samping kepala. Pola tabby tetap mengikuti permukaan kepala, punggung, dan ekor.

Gradasi jingga–keemasan pada dahi/pipi, krem pada moncong/paw, dan rose pada telinga memakai `COLOR_0` per vertex. Tidak ada tekstur bulu tambahan, CDN, atau unduhan aset. Renderer ditambah pembacaan warna vertex; material tanpa warna vertex memakai putih netral sehingga perilaku aset lama tetap sama.

## Bukti render dan evaluasi

[Perbandingan empat sudut](cat-redesign-sheet.jpg) memuat close-up wajah, profil samping, depan garasi, dan kamera balapan. Berkas individual: [wajah](comparison-face.jpg), [profil](comparison-profile.jpg), [depan](comparison-front.jpg), [balapan](comparison-race.jpg), dan [ukuran garasi sebenarnya](comparison-garage.jpg).

`before/` direkam dari HTML baseline Git di atas tanpa mengubah checkout branch pengembangan. `after/` memakai model baru. Close-up/profil/depan memakai posisi kamera dan target yang sama; viewport, FOV, pencahayaan, waktu idle, seed dan pose balapan disamakan. Kamera balapan memakai fungsi renderer balapan asli yang byte-identik. `camera-verification.json` memeriksa matriks view/projection dan dimensi canvas dari enam kasus perbandingan. Gambar adalah screenshot game sebenarnya, tanpa retouch karakter. Perbandingan wajah pada skala yang sama memperlihatkan perubahan lebar pipi, bentuk mata, hidung/senyum, telinga dan grip; kamera balapan memperlihatkan bentuk kepala dan ekor yang berbeda.

Satu tahap redesign bentuk diikuti evaluasi render. Snapshot tahap pertama disimpan di `evaluation/first-pass/`. Koreksi terarah mencakup telinga yang terlalu tinggi/berbidang, kesinambungan kurva dahi, pemasangan pangkal telinga, kemiringan mata, dan ujung ekor yang bertumpuk dengan kepala. Tidak dilakukan tahap subdivision berulang. Target penilaian adalah gambar pada kamera yang setara; jumlah segitiga dan tes kode bukan pengganti penilaian visual.

## Dua mode garasi

- **Mobil + Karakter**: komposisi seluruh mobil dan pengemudi.
- **Close-up Karakter**: kepala dan tubuh diperbesar. [Desktop](after/garage-close-desktop.png) / [HP](after/garage-close-mobile.png).

Geser mouse atau jari untuk memutar; scroll atau pinch untuk zoom. Rotasi otomatis dapat dijeda/dilanjutkan dan tampilan dapat direset. Panah pada canvas yang mendapat fokus mengubah orbit; `+`/`-` untuk zoom dan `0` untuk reset. Kontrol hanya aktif saat garasi. Kamera/input balapan tidak membaca keadaan orbit garasi.

Pada pengujian, jarak mata dalam pixel bertambah sekitar **2,07× desktop** dan **1,84× HP** pada mode close-up. Telinga tidak tertutup toolbar pada posisi awal; panel tidak bertumpuk dengan tombol balapan. Crop saat pengguna memperbesar atau mengubah sudut secara manual merupakan bagian dari zoom yang dapat direset.

## Geometri dan ukuran

| Komponen | Baseline | Redesign |
|---|---:|---:|
| Kucing high | 37.458 segitiga | 28.925 segitiga (−22,78%) |
| Mobil high | 20.931 | **20.931 identik** |
| Pasangan high | 58.389 | 49.856 |
| Kucing low | 15.405 | 11.875 (−22,91%) |
| Mobil low | 8.678 | **8.678 identik** |
| Pasangan low | 24.083 | 20.553 |
| Batch per pass warna | 44 | 44 |
| HTML mandiri | 19.736.629 byte | 19.796.352 byte |

GLB high 1.162.168 byte; low 528.680 byte. Data warna vertex menambah sedikit ukuran meskipun geometri berkurang. LOD, kualitas grafis dan jarak pemilihan model tetap memakai sistem lama. Tidak ada klaim FPS perangkat nyata; GPU timer cloud tidak tersedia. `metrics.json` menyimpan angka model terukur dan `../render-metrics.json` menyimpan instrumentasi model saja.

## Validasi

- **Scope/data** (`scope-verification.json`): seluruh 28 batch mobil mempunyai posisi, normal, indeks, dan material yang identik dengan baseline; seluruh pivot identik. Script gameplay, UI utama, scenery, metode animasi rig dan metode renderer/kamera balapan identik. Seluruh aset selain kedua GLB Kucing identik.
- **Render kompatibilitas** (`unchanged-renders.json`): mobil saja dan 13 karakter lainnya menghasilkan pixel identik dengan baseline pada 256×256, kamera/cahaya/pose yang sama. Ini memeriksa jalur default putih ketika aset tidak memiliki warna vertex.
- **Garasi** (`preview-tests.json`): 25 pemeriksaan lulus untuk dua mode, ukuran close-up, posisi toolbar/tombol, drag mouse/jari, scroll/pinch, stop/resume otomatis, reset, dan transisi ke kamera balapan. Desktop 1440×1000; HP emulasi 390×844.
- **Animasi dan kontak** (`animation-tests.json`): 10 pemeriksaan lulus untuk blink, kedua telinga, ekor, lean/jump, roda, pembekuan matriks pada waktu tetap, grip dan error WebGL. Fixture pusat palm terhadap rim maksimal sekitar 0,0421 m dalam rentang pose uji; ini bukan solver tabrakan seluruh mesh. Render depan/samping/belakang melengkapi fixture tersebut.
- **Gameplay/offline**: 16 pemeriksaan browser pada JSON tingkat atas lulus — bank soal, A/D, jump, pause, pemain/AI/waktu animasi membeku pada soal, buff dan kelanjutan, sentuhan, LOD dan balapan tanpa jaringan. Tujuh regresi inti juga lulus: JSON/CSV, stage/AI, Grand Prix, drift/jump, buff, hasil, ghost dan progres.
- **Ekspor HTML guru** (`export-tests.json`): empat pemeriksaan lulus. Ekspor menyertakan model berwarna dan kontrol, memulihkan state awal pratinjau, dan dapat masuk balapan/close-up ketika jaringan browser dimatikan.
- **GLB** (`../glb-validation.json`): kedua model diimpor kembali oleh Blender; normal hingga/berpanjang satuan, serta komponen warna vertex dalam rentang [0,1].

Tidak ada error JavaScript pada pemeriksaan di atas. HP adalah emulasi viewport/sentuhan, bukan perangkat fisik. `file://` diblokir administrator browser cloud; pengujian offline memakai browser tanpa jaringan dengan HTML dipasok langsung dari byte lokal. Fixture browser memperpendek countdown dan mendekatkan pemain ke gerbang kuis; tidak mengklaim semua putaran Grand Prix dimainkan manual. Seluruh perubahan gameplay dicegah oleh pemeriksaan kesamaan sumber.

## Berkas dan reproduksi

- [HTML terbaru](../race-quest-visual-upgrade.html)
- [GLB high](../race-quest-cat-sport.glb) / [GLB low](../race-quest-cat-sport-low.glb)
- [Blender editable](../source/race-quest-cat-sport.blend), dengan node warna vertex.
- Pemodelan: `source/refine_cat.py`, dipanggil oleh `source/build_cat.py`.
- Integrasi: `source/redesign_integration.py`; kontrol inline: `source/garage_preview.js`.

Dari `visual-upgrade/`: `blender -b --python-exit-code 1 --python source/build_cat.py`, kemudian `python3 source/assemble.py`. Server statis dari root repositori pada port 8000 diperlukan untuk skrip browser. `python3 visual-upgrade/source/verify_redesign.py` memeriksa batas scope; `node visual-upgrade/source/test_garage_preview.cjs` menguji kontrol; `node visual-upgrade/source/test_redesign_animation.cjs` menguji rig; `node visual-upgrade/source/verify_unchanged_render.cjs` memeriksa render kompatibilitas. Playwright dan Chromium memakai runtime cloud; sesuaikan lokasi require/executable untuk mesin lain.

Riwayat hasil dua tahap sebelumnya tetap tersedia di folder `cat-refinement/`, `comparisons/` dan commit Git sebelumnya. Entry point `index.html` tidak diubah dan tidak ada konfigurasi deployment yang ditambahkan.
