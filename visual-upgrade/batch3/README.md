# RACE QUEST PRO — Batch 3

Baseline lokal/remote terverifikasi: `2527304fb32174f5e07764f1cad84ecac866787f`, branch `dev/race-quest-cat-sport-visual-upgrade`. Template utama `visual-upgrade/race-quest-pro-batch2.html`, bukan `index.html` lama. Hanya Anjing/Tikus/Rubah dan kendaraannya didesain ulang.

## Mainkan

[ZIP playable](../../race-quest-pro-batch3-playable.zip) · [HTML mandiri](../race-quest-pro-batch3.html) · [paket lengkap](../../race-quest-pro-batch3-review.zip).

Ekstrak ZIP lalu buka HTML di browser dengan WebGL. Semua aset tertanam; tidak perlu CDN, unduhan model atau server untuk bermain. Pilih Anjing, Tikus, Rubah pada **halaman kedua** garasi. Status unlock dan harga asli **60 token** dipertahankan. Tidak ada token gratis atau perubahan profil pada distribusi.

## Perubahan bentuk

- **Anjing / Rally:** kepala kubus cokelat madu, moncong krem pendek, blaze grafis, hidung kecil, telinga cokelat jatuh, collar/tag dan paw krem. Ekor pendek bertingkat. Rally biru tua memiliki panel samping tersambung, fender lebar, ban bertapak, bumper/guard, dua lampu reli tambahan, half-cage dengan scoop, spoiler coral, livery, sill dan mud flap. Berbeda dari Buggy Beruang dan bak Farm Buggy.
- **Tikus / Mini Roadster:** kepala lebih kecil berahang kotak, telinga besar kotak membulat berinset pink, pipi ringan, hidung kecil, empat kumis grafis dan ekor pink panjang bersudut lembut. Roadster mint memiliki kap/rear deck pendek, lampu besar, grille kecil, bumper chrome terpisah, fender pendek, kokpit terbuka dengan kaca rendah serta hubcap ivory/coral. Kesan mungil berasal dari bodi, tanpa mengecilkan collider, roda atau wheelbase.
- **Rubah / GT:** rahang kubus meruncing, telinga segitiga tebal, bib pipi krem tunggal, nose kecil, mata dengan brow ringan, tubuh jingga dan paw terang. Ekor blocky besar berujung krem ditempatkan di luar bolster kursi, di atas dek dan di depan spoiler. GT oranye memiliki kap panjang lebar, fender terhubung ke panel samping, lampu tajam, grille lebar, intake, livery dua garis, sayap GT, diffuser dan knalpot ganda. Tidak memakai bodi Sport, Formula atau Photon.

Semua bentuk baru memakai bevel terukur, weighted normals, vertex colour dan material cat/trim/logam/karet/kaca/karakter yang sama dengan renderer baseline. Tidak ada sculpt organik, subdivision atau tekstur berat.

## Evaluasi dan bukti visual

[Lineup 11 pasangan](comparisons/batch0-3-lineup.jpg) berasal dari HTML baru dengan kamera/material/waktu yang sama. [Tampak karakter](comparisons/character-turnarounds.jpg), [tampak kendaraan](comparisons/vehicle-turnarounds.jpg), [ekspresi](comparisons/expressions.jpg).

Before–after: [Anjing](comparisons/anjing/comparison-sheet.jpg), [Tikus](comparisons/tikus/comparison-sheet.jpg), [Rubah](comparisons/rubah/comparison-sheet.jpg). Per folder tersedia 13 pasangan gambar terpisah: hero, depan/samping/belakang, face, karakter saja, kendaraan saja, garasi, dan chase camera. Semua berasal dari GLB yang benar-benar dimuat **RaceRenderer**, bukan mockup atau ilustrasi. Pillow hanya menyusun/menambahkan label gambar.

`camera-verification.json` memastikan matriks view/projection, resolusi dan waktu identik pada **33 perbandingan model dan enam perbandingan game**. Model/garasi memakai waktu 1; balapan memakai waktu 2 dan seed/posisi sama. Close-up desktop/HP tambahan di `after/<id>/` memakai kamera UI sebenarnya dan tidak dicampur dengan perbandingan terkontrol.

Render awal di `evaluation/first-pass/` dipertahankan. Koreksi terarah menyambungkan dudukan kaca depan ke kap, mengisi panel tengah Rally dan panel sisi GT agar detail tidak tampak melayang, serta menyatukan material hubcap Tikus untuk mengurangi empat draw call. Pemeriksaan depan/samping/belakang dan pose steering/jump tidak menunjukkan clipping besar. Sisi ekor Rubah tetap di luar kursi/dek/spoiler; geraknya ringan dan memakai pivot dekat pangkal.

## Ukuran dan rendering

HTML **22.162.971 byte**, baseline **20.742.156 byte**, tumbuh **6,85%**, tetap di bawah target 25 MB desimal. Aset lama tiga pasangan/portrait diganti pada key yang sama; hanya tiga GLB low dan tiga portrait senang ditambahkan. Tidak ada engine kedua atau payload model baru yang duplikat.

| Pasangan | GLB high / low (byte) | Segitiga terlihat high / low | Draw call warna | Buffer GPU kedua LOD (byte) |
|---|---:|---:|---:|---:|
| Anjing / Rally | 500.844 / 239.648 | 17.810 / 7.534 | 28 | 999.504 |
| Tikus / Mini Roadster | 357.332 / 190.164 | 12.186 / 5.782 | 26 | 718.224 |
| Rubah / GT | 432.664 / 219.808 | 15.242 / 6.934 | 26 | 874.896 |

Segitiga/draw call adalah model normal yang benar-benar dikirim pada **satu pass warna**, di luar arena, UI, AI tambahan dan pass bayangan. Segitiga tersimpan high termasuk ekspresi tersembunyi: 18.634 / 13.010 / 16.066. Low mengurangi segitiga terlihat sekitar **53–58%**, melalui bevel satu segmen dan sektor roda/rim lebih sedikit. Low dipilih saat kualitas rendah atau jarak balapan lebih dari 24 unit.

Buffer GPU di atas diukur lewat `getBufferParameter(BUFFER_SIZE)` untuk geometri warna **dan depth**, high+low sekaligus; bukan RAM total browser atau VRAM perangkat. Tidak termasuk HTML, JS heap, arena, tekstur, render target atau overhead driver. `isBuffer` mengonfirmasi seluruh 308/292/292 buffer tercatat telah dihapus setelah model dipensiunkan. `asset-metrics.json` dan `rig-tests.json` merinci batas ukuran, tris karakter/kendaraan, hash serta hasil ini. **Tidak ada klaim FPS perangkat fisik.**

## Rig dan integrasi

Enam GLB di `models/`, tiga `.blend` dan builder di `source/`, enam avatar WebP render normal/senang di `avatars/`. Lihat [rebuild](source/README.md). Sumber Batch 1/2 dipakai ulang tanpa diubah; arsip review tidak menduplikasi seluruh HTML template historis. Gunakan checkout repository untuk rebuild integrasi; Blender sumber masing-masing tetap editable sendiri.

Origin, parent/pivot lama, posisi roda, wheelbase, track, steer/spin axis dan collider tetap identik. Seat, steering dan kontak tangan memakai rig baseline. Pusat paw ke rim terukur maksimum 0,05252 m sepanjang fixture lean/jump, dalam envelope mitten; ini bukan solver benturan semua segitiga. Footrest dan support memberi tumpuan bagi paw bawah. Kaca depan rendah berada di depan kolom kemudi.

Kedip, telinga, ekor, lean, suspensi, jump/landing, steering dan wheel spin memakai clock simulasi yang sama. Tidak ada clock waktu nyata baru. Ekspresi normal/happy/shock tersedia di garasi, reaksi item/benturan dan kemenangan. Grup alternatif default tersembunyi di GLTF viewer standar; renderer game memilih berdasarkan metadata. Avatar pilihan dan hasil menang memakai render baru. Model AI dan ghost transparan juga diverifikasi melalui jalur race renderer asli.

## Pengujian dan keterbatasan

Laporan JSON menyimpan hasil validasi enam GLB melalui native Blender import; finite/unit normals, vertex colour, indeks, metadata rig/collider dan ekspresi default. Tes rig memeriksa semua ekspresi, kedip, gerak khas, steering/wheel spin, lean/jump/landing, freeze, LOD dan penghapusan buffer.

**123 pemeriksaan** browser mencakup tiga karakter pada desktop **1440×1000** dan HP emulasi **390×844**: avatar, framing telinga, close-up, ekspresi, drag, scroll/pinch, reset, auto-rotate, chase camera, pause/soal membekukan seluruh matriks, buff/lanjutan dan hasil menang. Regresi memakai bank soal/Ruang Guru, CSV/JSON, materi/jumlah soal, penyimpanan, AI/stage/Grand Prix, drift/jump/item/ghost/progres, A/D, sentuh, kualitas dan ekspor HTML. `scope-verification.json` membuktikan kode aturan/UI/data/scenery/input/renderer bersama tetap identik kecuali konfigurasi tiga model. `unchanged-renders.json` memeriksa **22 render terlindungi**, termasuk seluruh high/low delapan pasangan selesai, Cat garage dan mobil biru, serta tiga model Batch 4; piksel identik terhadap baseline.

`offline-test-results.json` menguji ketiga pasangan dengan jaringan browser dimatikan: hanya dokumen utama dipenuhi dari byte lokal, tanpa permintaan aset HTTP. Ekspor game Ruang Guru dimuat ulang dan dimainkan dalam kondisi yang sama. **30 pemeriksaan** `actor-tests.json` memaksa AI menggunakan ketiga karakter baru dan ghost masing-masing, menguji opacity, ekspresi, freeze/resume dan low LOD dengan Session serta ghost tervalidasi.

Batas pengujian: Chromium cloud memakai SwiftShader, bukan HP/GPU fisik. Fixture mempercepat countdown dan mendekatkan gate/finish; tidak menggantikan uji endurance beberapa balapan manual. Token fixture hanya untuk pembelian asli dalam konteks uji, tidak masuk distribusi. Pembukaan `file://` telah dicoba ulang dan diblokir kebijakan browser cloud dengan **ERR_BLOCKED_BY_ADMINISTRATOR**, dicatat di `file-offline-test.json`; jalur jaringan-mati di atas berhasil. Membuka HTML unduhan langsung pada browser desktop/HP pengguna tetap perlu tinjauan. Ini batas lingkungan uji, bukan error JavaScript yang disembunyikan.

## Status

**11 blocky:** Kucing, Pinguin, Beruang, Kelinci, Bebek, Ayam, Domba, Robot (delapan baseline tidak berubah), Anjing, Tikus, Rubah (Batch 3). Panda, Koala dan Rakun tetap tersedia dengan aset asli. [Status 14 karakter](character-status.json). Batch 4 tidak dikerjakan. Tidak ada perubahan `index.html`, merge `main` atau deployment Pages.
