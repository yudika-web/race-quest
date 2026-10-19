# RACE QUEST PRO — Batch 2

Baseline terverifikasi: `60b2edb966e5775c48c8868c105b700eb57718c4`, branch `dev/race-quest-cat-sport-visual-upgrade`. Hanya Bebek, Ayam, Domba, Robot dan kendaraannya yang didesain ulang. Kucing dan Batch 1 beserta HTML historis, seluruh aset, sumber dan laporannya tetap byte-identik. `index.html`/`main`/Pages tidak diganti.

## Mainkan dan tinjau

[ZIP playable](../../race-quest-pro-batch2-playable.zip) · [HTML mandiri](../race-quest-pro-batch2.html) · [paket lengkap](../../race-quest-pro-batch2-review.zip).

Ekstrak ZIP dan buka HTML di browser dengan WebGL. Semua aset tertanam; internet dan server tidak diperlukan untuk bermain. Bebek/Ayam ada di halaman pertama garasi; Domba/Robot di halaman kedua. Unlock tetap memakai aturan asli 60 token. Tidak ada token gratis atau unlock otomatis di file distribusi. Materi/jumlah soal, impor/ekspor dan penyimpanan tetap tersedia melalui Ruang Guru.

## Bentuk yang berubah

- **Bebek / Amfibi:** kepala kuning kubus lebar, paruh pendek dua lapis, sayap terlipat dan kaki berselaput. Kendaraan memiliki lambung mengecil ke haluan, ponton turquoise dengan sabuk kuning dan transom/impeller dekoratif; tetap balapan darat.
- **Ayam / Farm Buggy:** rahang kotak krem, paruh baji, jengger tiga balok, pial merah dan sayap beraksen grafis. Buggy hijau menggunakan grille traktor vertikal, fender krem, ban bertapak, rollbar tinggi, step dan bak kayu kecil. Berbeda dari Buggy Beruang yang tidak diubah.
- **Domba / Cloud Cruiser:** muka abu-krem berbingkai kelompok bulu kubus, telinga kecil, torso pendek dan hoof gelap. Cruiser pastel mempunyai kap empuk lebar, panel awan bertingkat, fender lavender, lampu kotak membulat dan sirip kecil dekoratif. Tetap kendaraan darat.
- **Robot / Photon:** helm kubus, layar gelap, mata cyan, senyum digital, antena dan sendi pendek. Photon mempunyai undertray rendah, dua pod energi depan, side battery, garis cyan dan spoiler berpenopang geometris. Tidak memakai model Formula atau sport Kucing.

Evaluasi awal disimpan di `evaluation/first-pass/`. Koreksi terarah menambah batas bulu pada pipi/flank Domba dan dua pod depan Photon agar lebih mudah dibedakan dari Formula. Ini perubahan bentuk, bukan subdivision. Tidak ada simulasi bulu, tekstur berat, atau perubahan gameplay.

## Bukti visual

Semua gambar berasal dari GLB yang benar-benar dimuat **RaceRenderer di game**, bukan ilustrasi. [Lineup delapan pasangan](comparisons/batch0-2-lineup.jpg) memakai kamera, waktu dan pencahayaan yang sama. [Tampak karakter](comparisons/character-turnarounds.jpg), [kendaraan](comparisons/vehicle-turnarounds.jpg), [ekspresi](comparisons/expressions.jpg).

Before–after: [Bebek](comparisons/bebek/comparison-sheet.jpg), [Ayam](comparisons/ayam/comparison-sheet.jpg), [Domba](comparisons/domba/comparison-sheet.jpg), [Robot](comparisons/robot/comparison-sheet.jpg). Masing-masing folder juga berisi 13 perbandingan terpisah: hero, depan/samping/belakang, wajah, karakter saja, kendaraan saja, garasi, dan balapan. `camera-verification.json` membandingkan matriks view/projection, resolusi dan waktu secara tepat untuk 44 render model dan delapan render game. Gambar garasi close-up desktop/HP di `after/<id>/` menggunakan kamera UI aslinya, terpisah dari kamera perbandingan terkontrol.

## Aset dan efisiensi

HTML **20.742.156 byte**, baseline **19.539.444 byte**, bertambah **6,16%**, tetap di bawah target 25 MB desimal. Hanya empat GLB utama dan avatar yang diganti; empat GLB low dan empat avatar senang ditambahkan. Tidak ada engine kedua, salinan data bank soal, CDN atau aset jaringan. Material berwarna melalui vertex color tanpa tekstur. Mesh digabung per pivot/material.

| Pasangan | GLB high / low (byte) | Segitiga terlihat high / low | Draw call warna |
|---|---:|---:|---:|
| Bebek | 316.740 / 169.956 | 10.716 / 5.136 | 23 |
| Ayam | 444.060 / 210.516 | 15.720 / 6.572 | 24 |
| Domba | 363.968 / 190.660 | 12.524 / 5.864 | 25 |
| Robot | 377.512 / 199.628 | 12.870 / 5.954 | 32 |

Segitiga/draw call di atas adalah model normal yang benar-benar dikirim pada **satu pass warna**, tidak termasuk arena/AI/UI maupun pass bayangan. Jumlah tersimpan termasuk ekspresi alternatif: 11.508 / 16.512 / 13.348 / 13.586 high. LOD low mengurangi segitiga yang terlihat sekitar 52–58%; dipilih saat kualitas rendah atau model balapan berjarak lebih dari 24 unit. `asset-metrics.json` merinci ukuran, hash, tris karakter/kendaraan, bounds, sumber Blender dan perbandingan baseline. Tidak ada klaim FPS HP fisik.

## Rig dan sumber

Delapan GLB di `models/`, empat `.blend` dan builder di `source/`, delapan avatar WebP normal/senang di `avatars/`. [Instruksi rebuild](source/README.md) menjelaskan penggunaan ulang factory, kokpit, roda dan pengujian Batch 1 tanpa mengubah sumber lama. Arsip tinjauan tidak menduplikasi seluruh template Batch 1; untuk rebuild HTML gunakan checkout repository ini.

Origin, parent pivot lama, posisi roda, wheelbase, track dan collider dipertahankan. Pose duduk, seat cushion/back dan rim memakai titik kontak Batch 1. Pemeriksaan matriks mengukur pusat paw ke rim saat steering/jump hingga maksimum 0,05252 m, di dalam envelope mitten; ini bukan solver tabrakan mesh. Tampak samping/depan dan pose belok/jump diperiksa visual untuk clipping besar. Kedip, gerak ekor/telinga/antena, lean, suspensi, roda dan setir memakai clock simulasi yang sama. Tidak ada wall-clock baru yang berjalan saat soal/pause.

GLB default menampilkan wajah normal di viewer standar; grup ekspresi alternatif disembunyikan dengan skala nol. Renderer game memilih grup melalui metadata. Blender sumber memiliki named pieces, bevel terukur, weighted normals, vertex colour dan pivot editable; tidak memakai subdivision tinggi.

## Pengujian dan batasnya

Laporan JSON di folder ini mencatat hasil aktual: native import delapan GLB, validitas normal/warna/index, rig/collider, gameplay core, browser desktop/HP, avatar, seluruh ekspresi, close-up, drag/pinch/zoom/reset, kemudi A/D/sentuh, jump/landing, pause/soal membekukan seluruh matriks, buff/lanjutan/hasil menang, ekspor HTML, dan offline. `scope-verification.json` membuktikan kode game/aturan/data/scenery/input preview dan seluruh file historis tetap identik. `unchanged-renders.json` membandingkan 17 render terlindungi dengan piksel tepat sama.

Pengujian browser memakai Chromium cloud dan SwiftShader; HP diuji pada viewport/touch emulation **390 × 844**, desktop **1440 × 1000**, bukan perangkat HP fisik. Countdown dipercepat serta posisi gate/finish diatur sebagai fixture agar jalur gameplay asli dapat diperiksa; tidak menggantikan uji endurance beberapa balapan manual. Fixture test menyediakan token lalu memakai pembelian/paginasi asli; file distribusi tidak berubah. Mode jaringan browser dinonaktifkan dan hanya dokumen utama dipenuhi dari byte lokal; akses langsung `file://` dibatasi administrator browser cloud, sehingga pembukaan file unduhan di HP fisik masih perlu uji pengguna. Kualitas estetika akhir tetap menunggu tinjauan pengguna dari screenshot dan game.

## Status 14 karakter

Selesai blocky: Kucing, Pinguin, Beruang, Kelinci (baseline tetap), Bebek, Ayam, Domba, Robot (Batch 2 ini). Anjing, Tikus, Rubah, Panda, Koala, Rakun tetap memakai aset lama, belum dikerjakan. Lihat [daftar status](character-status.json). Batch 3–4 tidak dimulai.
