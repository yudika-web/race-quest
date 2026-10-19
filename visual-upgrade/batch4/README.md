# RACE QUEST PRO — Batch 4 final

Baseline lokal dan remote terverifikasi: `ddc28f89d628b877d6e70149b0301df4a8aa24a9`, branch `dev/race-quest-cat-sport-visual-upgrade`. Sumber utama `visual-upgrade/race-quest-pro-batch3.html`. Hanya Panda/Koala/Rakun beserta kendaraan yang diganti; semua file historis, sebelas pasangan sebelumnya, gameplay dan arena dipertahankan.

## Unduh dan mainkan

[ZIP playable](../../race-quest-pro-batch4-playable.zip) · [HTML mandiri](../race-quest-pro-batch4.html) · [ZIP review](../../race-quest-pro-batch4-review.zip).

Ekstrak lalu buka HTML pada browser dengan WebGL. Semua aset tertanam; tidak ada CDN, unduhan model atau server yang diperlukan untuk bermain. **Panda di halaman 2; Koala/Rakun di halaman 3 garasi.** Unlock tetap 60 token. Distribusi tidak berisi token demonstrasi, unlock gratis atau perubahan profil siswa. Pengaturan guru dan impor/ekspor tetap tersedia.

## Bentuk baru

- **Panda / Bamboo:** kepala putih kubus besar, patch mata tipis yang menembus sedikit bidang wajah agar menempel, mata dengan highlight, telinga hitam pendek, muzzle/nose kecil. Torso belly meruncing sedikit gemuk, shoulder saddle dan anggota tubuh gelap, paw proporsional. Bamboo memakai hull hijau, panel kap/side-body beruas dengan node struktural, bumper krem, grille tiga ruas, ban bertapak, fender, arch ringan, spoiler pendek dan emblem daun. Segmen merupakan bagian bodi, bukan batang bambu yang ditempel pada mobil lama.
- **Koala / Eco Pod:** kepala kotak abu lembut, telinga besar kotak membulat berinset pink, nose vertikal besar, mata/cheek ringan, dada krem dan paw pendek. Eco Pod memakai bonnet putih mendatar, muka pod EV tegak, integrated bumper, side battery dengan tiga tick LED, wheel brow ivory dan hub modern. Bentuk kotak tegak/bersih membedakannya dari haluan Kapsul dan pod energi/spoiler Photon.
- **Rakun / Trail Pickup:** rahang kubus abu hangat, topeng mata grafis tunggal yang menyatu, cheek/muzzle krem, telinga segitiga pendek dan paw gelap. Ekor naik di sisi kursi dengan lima segmen loreng; berada di atas bak dan di depan hoop. Trail Pickup memakai kap truck, radiator/grille besar vertikal, fender gelap dengan flare krem, bak terbuka berlantai rendah, bed walls/top rails, tailgate/latch, hoop di bak, bumper protektif, running board dan satu equipment case kecil. Bak tetap terlihat dan tidak memakai mekanik muatan.

Tidak ada sculpt organik, subdivision atau bulu realistis. Material shared tetap membedakan cat, trim, alloy, kaca smoked, karet, LED dan karakter. Sumber Blender per bagian tetap editable.

## Evaluasi dan render sebenarnya

Render awal di `evaluation/first-pass/` dipertahankan. Koreksi terarah memperpanjang sedikit ujung segmen loreng Rakun agar sambungan tertutup saat pivot bergerak; tidak menambah segitiga. Pemeriksaan depan/samping/belakang, pose jump/steer, serta garasi/balapan tidak memperlihatkan clipping besar. Telinga Koala diperiksa pada framing desktop dan HP; ekor Rakun berada di luar bolster dan terpisah dari bed/hoop.

[14-Character Complete Lineup](comparisons/complete-character-lineup.jpg) · [14-Vehicle Lineup](comparisons/complete-vehicle-lineup.jpg) · [14 pasangan lengkap](comparisons/complete-pair-lineup.jpg).

Setiap lineup memakai kamera, pencahayaan, pose dan skala setara, dari **42 capture GLB asli yang dimuat RaceRenderer**. Character lineup mempertahankan pose duduk asli dengan kendaraan disembunyikan, tanpa rescale anggota satu per satu. Vehicle lineup menyembunyikan pengemudi. Tidak ada ilustrasi generatif. `lineup-cameras.json`/`lineup-verification.json` membuktikan matriks, resolusi dan waktu sama per kelompok.

Before–after: [Panda](comparisons/panda/comparison-sheet.jpg), [Koala](comparisons/koala/comparison-sheet.jpg), [Rakun](comparisons/rakun/comparison-sheet.jpg). Setiap folder juga memuat 13 perbandingan terpisah: hero, front/side/back, face, karakter saja, kendaraan saja, garasi dan chase camera. **33 perbandingan model dan enam game** memakai view/projection/resolusi/waktu/seed setara (`camera-verification.json`). PNG UI close-up desktop/HP, ekspresi, grip/jump, hasil menang, AI/ghost serta validasi roster di `after/`. Pillow hanya menata dan menulis label gambar.

## Ukuran, geometri dan resource

HTML **23.349.280 byte**, baseline **22.162.971 byte**, naik **5,35%**. Sisa anggaran **1.650.720 byte** di bawah 25 MB desimal. Tiga GLB utama dan avatar diganti pada key sama; tiga GLB low dan tiga avatar happy ditambahkan. Tidak ada engine/input handler/observer kedua, payload baru yang duplikat, atau penghapusan fitur untuk mengecilkan file.

| Pasangan | GLB high / low (byte) | Segitiga terlihat high / low | Draw call warna | Buffer high+low warna/depth (byte) |
|---|---:|---:|---:|---:|
| Panda / Bamboo | 461.900 / 220.460 | 16.320 / 6.868 | 26 | 918.912 |
| Koala / Eco Pod | 399.208 / 204.420 | 13.892 / 6.336 | 26 | 802.176 |
| Rakun / Trail Pickup | 494.720 / 233.040 | 17.658 / 7.362 | 26 | 986.496 |

Tris/draw call adalah model normal yang benar-benar disubmit pada **satu pass warna**, di luar dunia/UI/AI tambahan/pass bayangan. Stored high termasuk ekspresi tersembunyi: **17.144 / 14.716 / 18.482**. Low mengurangi geometri terlihat sekitar **54–58%**, lewat bevel satu segmen dan sektor roda/rim berkurang. Low tetap dipilih oleh kualitas rendah/jarak lebih dari 24 unit.

Buffer diukur dengan WebGL `BUFFER_SIZE` untuk kedua LOD dan colour/depth geometry. `isBuffer` memverifikasi semua buffer tercatat benar-benar dihapus saat model dipensiunkan. Nilai itu **bukan RAM total browser/VRAM perangkat**; tidak mencakup HTML, JS heap, arena, textures, render target atau overhead driver. Tidak ada klaim FPS fisik. `asset-metrics.json` dan `rig-tests.json` memuat hash, bounds, tris karakter/kendaraan, biaya geometri serta cleanup. **`complete-asset-catalog.json`** merinci ukuran, segitiga terlihat/tersimpan dan draw call high/low aktual seluruh 14 pasangan.

## Integrasi dan sumber

Enam GLB baru di `models/`, tiga `.blend` dan builder/assembler di `source/`, enam avatar WebP normal/happy di `avatars/`. [Instruksi rebuild](source/README.md). Factory, cockpit/wheels, ekspresi dan contact helpers Batch 1–3 digunakan ulang tanpa membangun ulang aset lama. Arsip review memuat tahap ini; untuk rebuild HTML gunakan checkout repository agar helper/template historis tersedia. Blender sumber masing-masing tetap editable sendiri.

Origin, parent/pivot lama, wheelbase, track, radius, steer/spin axis dan collider identik dengan GLB lama. Kontak duduk, footrest dan tangan memakai standar baseline. Pusat paw ke rim maksimum **0,05252 m** dalam fixture lean/jump; pemeriksaan itu dilengkapi render dan bukan solver semua benturan segitiga. Kedip, ears/tail, lean, jump/landing, suspension, steering dan wheel spin memakai clock simulasi asli. Tidak ada wall-clock baru. Wajah normal/happy/shock diseleksi metadata; varian nonaktif default tersembunyi pada viewer GLTF standar. Pemilihan, preview, balapan pemain/AI, ghost dan hasil menang menggunakan aset baru.

## Validasi dan batasnya

Laporan terpisah menyimpan hasil native Blender import enam GLB, validitas indeks/normal/warna, collider/pivot, ekspresi default, rig, LOD, buffer cleanup, serta regresi core. **123 pemeriksaan desktop/HP** menguji tiga karakter pada desktop **1440×1000** dan HP emulasi **390×844**: avatar, telinga/framing, close-up, tiga ekspresi, drag, scroll/pinch, reset/auto, chase camera, steering A/D/sentuh, jump, pause/soal freeze, buff, resume dan hasil menang. AI/ghost dites dengan Session dan ghost tervalidasi, termasuk opacity, surprise, freeze/resume dan low LOD.

**167 pemeriksaan validasi akhir seluruh 14** (`all-character-tests.json`) memakai UI pemilihan/paginasi, pembelian asli untuk karakter terkunci, avatar, close-up, ekspresi yang tersedia, high/low GLB, race Session, submission mesh pemain, dan pause. Semua dilakukan dengan HTML final. Screenshot tiap race di `after/validation/`. Tidak ada unlock gratis di distribusi; test context memasok token sebelum memakai UI beli asli.

Perlindungan (`scope-verification.json`): kode data/gameplay/UI/scenery/input serta renderer bersama identik, kecuali tiga konfigurasi model baru. Semua file historis dan payload sebelas pasangan lama tidak berubah. **25 render terlindungi** (`unchanged-renders.json`) meliputi Cat high/low, dua preview Cat, mobil sport sendiri dan high/low sepuluh pasangan lain, dengan piksel tepat identik terhadap baseline Batch 3.

Core/browser regression mencakup Ruang Guru/bank soal, materi/jumlah, JSON/CSV, penyimpanan, AI/stage/Grand Prix mastery/retry, drift/jump/item/buff/ghost/progres, kontrol, kualitas dan ekspor HTML. Aturan/audio tetap byte-identik. Uji offline mematikan jaringan dan memenuhi **hanya dokumen utama dari byte lokal**, lalu memainkan ketiga pasangan tanpa permintaan aset HTTP. Ekspor HTML Ruang Guru dimuat ulang dan dimainkan offline.

Batas pengujian: Chromium cloud/SwiftShader dan emulasi touch, **bukan HP fisik atau FPS perangkat nyata**. Countdown/gate/finish dipersingkat sebagai fixture; tidak diklaim menjalankan seluruh Grand Prix manual atau uji endurance. Pembukaan langsung `file://` diuji terpisah; kebijakan administrator browser cloud dapat memblokirnya dengan `ERR_BLOCKED_BY_ADMINISTRATOR` dan dicatat sebagai blocked di `file-offline-test.json`, bukan dilabeli lulus. Uji jaringan-mati di atas berhasil; membuka file unduhan pada perangkat pengguna tetap perlu tinjauan.

## Selesai dibuat, menunggu tinjauan

[Status 14 karakter](character-status.json) menandai seluruhnya selesai dibuat dan siap ditinjau. Kucing, Pinguin, Beruang, Kelinci, Bebek, Ayam, Domba, Robot, Anjing, Tikus dan Rubah tidak diubah. Panda, Koala, Rakun melengkapi roster. `index.html` online, `main` dan arena tetap utuh; tidak ada deployment. **Tidak ada pekerjaan arena dimulai. Berhenti untuk tinjauan pengguna.**
