# BlokRaya PRO — PATCH 8A: Kayong Utara dan Ketapang

Baseline: `de6bd8009558d53a5c110644cdd4589e5cf3f731`, branch `dev/race-quest-cat-sport-visual-upgrade`.

[HTML playable](../blokraya-patch8a-landmarks.html) · [ZIP playable](../../blokraya-patch8a-playable.zip) · [ZIP review](../../blokraya-patch8a-review.zip).

## Sumber visual dan batas verifikasi

Prioritas diberikan pada gambar yang terlihat dalam pesan pengguna: Sail Selat Karimata hijau (lampiran kedua), bangunan Keraton Matan kuning-hijau (ketiga), dan Ale-Ale versi menara jam dengan cangkang di samping (keempat). Lampiran pertama menampilkan masjid dan tidak digunakan untuk mengganti landmark target.

Keempat halaman web yang diminta ditolak dari lingkungan cloud: `CONNECT 403 Forbidden`; percobaan browser juga menghasilkan `ERR_TUNNEL_CONNECTION_FAILED`. Tidak mengklaim telah membaca artikel, memverifikasi tanggal pembangunan/renovasi, atau melakukan survei arsitektur. Versi Ale-Ale yang dipilih adalah **versi menara jam pada lampiran**, tanpa menggabungkan pilar/cangkang monumen 2019. URL dan status sumber tercatat di [references/manifest.json](references/manifest.json).

**Batas lembar foto:** gambar referensi dapat dilihat dalam percakapan, tetapi file biner aslinya tidak tersedia sebagai lampiran lokal pada workspace. Tidak membuat ulang/fabrikasi foto. [Lembar FOTO REFERENSI → MODEL LAMA → MODEL BARU](photo-model-review.html) sudah memuat enam render asli dan menyediakan pemilih foto lokal pada kolom pertama; foto asli belum dibundel. Setelah memilih berkas lampiran pada perangkat sendiri, lembar dapat dicetak offline. Gambar yang dipilih tidak diunggah ke server. Lembar before–after dua kolom sudah lengkap tanpa memerlukan foto lokal.

## Perubahan landmark yang terlihat

| Landmark | Unsur gambar yang diterapkan | Detail yang disederhanakan |
|---|---|---|
| Sail Selat Karimata | Satu bidang hijau tinggi asimetris, **lubang bundar benar-benar tembus**, garis putih, panel abu-abu berprofil miring, rangka putih menyapu melengkung, kisi ornamen cokelat, alas silinder putih dan tulisan Sail/2016. Menggantikan dua segitiga jingga/kuning lama. | Motif ukiran disarikan menjadi lengkung geometris; tidak menyalin setiap relief atau tekstur batu. Dimensi merupakan proporsi visual dari satu foto, bukan ukuran bangunan asli. |
| Ale-Ale | Menara hijau berbingkai kuning/emas, bidang jam putih dengan jarum statis, atap Melayu bersilang, bukaan lengkung, dua cangkang beralur pada alas samping, mutiara kecil dan pedestal bertingkat. Menggantikan kipas besar di atas pilar. | Angka jam menjadi tanda sederhana; detail ukiran dan kontur cangkang menggunakan bidang low-poly. Jam dekoratif tidak menjadi fitur waktu baru. |
| Keraton Matan | Fasad kayu kuning, dasar hijau, serambi depan panjang, kolom/rangka kayu, pagar silang, pintu, jendela berdaun penutup, bidang atas berpelana dan mahkota, teras atas, serta paviliun terbuka di sudut kanan. | Relief mahkota, kisi, sambungan kayu dan proporsi belakang disarikan; tidak mengklaim denah atau rekonstruksi sisi yang tidak tampak pada foto. Bentuk dibuat khusus, bukan mengganti istana dengan model Keraton Mempawah. |

Model baru memakai mesh prosedural dan material bersama. Normal bidang Sail dipisahkan per muka agar strip mesh di sekitar lubang tidak menghasilkan garis shading. Atap Ale-Ale dibangun sebagai permukaan silang tunggal agar bidang atap tidak saling menembus. Penerimaan shadow map kasar dinonaktifkan hanya pada grup material landmark baru; pencahayaan arah/ambient dan cast shadow tetap tersedia. State renderer dikembalikan setelah draw.

## Komposisi arena

- **Kayong Utara:** plaza Sail bertingkat, kebun tepi, pohon peneduh/palem, bangku, lampu dan jalur pedestrian. Terrain dekoratif jauh di sekitar plaza serta pantai diselaraskan. Pantai Pulau Datok kini memperlihatkan promenade kayu, gazebo dan fasilitas pantai yang sebelumnya terbenam dalam massa terrain. Kontur bukit di luar area tersebut, laut, langit, track ekstrem dan obstacle tetap digunakan.
- **Ketapang:** taman plaza Ale-Ale, jalur pendekat, halaman istana dengan lawn/pedestrian, pagar rendah, pohon peneduh, bangku, lampu dan beberapa bangunan pengisi tepi. Penataan tambahan bersifat interpretasi kota/pesisir fiktif, tidak diklaim sebagai posisi fasilitas nyata.
- Penataan tetap berada di luar lajur dan tidak membuat collider baru. Perubahan terrain hanya dekorasi jauh; waypoint, panjang/elevasi track dan physics tidak disentuh.

## Bukti visual asli

Kamera, pose, waktu simulasi, kualitas dan pencahayaan pada pasangan before–after dibuat setara. Close-up/overview adalah kamera inspeksi renderer; screenshot bertanda balapan memakai kamera chase asli yang tidak diubah.

- Sail: [sebelum](screenshots/before/sail-close.png), [sesudah](screenshots/after/sail-close.png), [perbandingan](screenshots/comparison-sail-close.jpg), [siluet jauh](screenshots/after/sail-silhouette.png), [plaza](screenshots/after/coastal-plaza.png).
- Pantai: [perbandingan](screenshots/comparison-pulau-datok.jpg), [kamera balapan](screenshots/comparison-kayong-race.jpg).
- Ale-Ale: [perbandingan](screenshots/comparison-ale-close.jpg), [plaza](screenshots/after/ale-plaza.png), [kamera balapan](screenshots/comparison-ketapang-race.jpg).
- Keraton Matan: [perbandingan](screenshots/comparison-matan-close.jpg), [depan](screenshots/after/matan-front.png), [halaman](screenshots/after/matan-courtyard.png), [kamera balapan](screenshots/comparison-matan-race.jpg).
- HUD desktop/HP: [Kayong desktop](screenshots/after/kayong_utara-hud-1366.png), [Kayong landscape](screenshots/after/kayong_utara-hud-844.png), [Ketapang desktop](screenshots/after/ketapang-hud-1366.png), [Ketapang landscape](screenshots/after/ketapang-hud-844.png).
- Empat thumbnail stage diganti dengan render aktual baru; 22 thumbnail lain tetap identik. Gambar model bukan ilustrasi generatif.

## Pengujian

| Pengujian aktual | Hasil |
|---|---|
| Scope dan perlindungan | **51 payload script** identik dengan finalisasi, termasuk seluruh core/track, physics, AI, buff, audio/HUD, mode/PIN, alur siswa, podium/hasil dan konfigurasi GP. Seluruh artefak lama tetap identik, selain README rilis utama. Adapter hanya mengubah dua kelas scenery. Empat thumbnail diganti tanpa duplikasi URI. |
| Simulasi | Seluruh 13 konfigurasi track dan **600 langkah per arena** identik dengan baseline pada input/seed sama. |
| Penyelesaian dua arena | **18 balapan driver referensi penuh dan 72 completion AI**: Kayong/Ketapang × tiga kesulitan × tiga seed; lima jawaban nyata, skor 100%, tidak memindah posisi ke finish pada suite ini. |
| Jalur dan kamera | **3.115 sampel lajur**, **192 frame chase** pada 12/31 m/s: tidak ada geometri dekoratif yang menutupi jalan atau menembus kamera. Permukaan ramp yang memang sengaja naik dikecualikan dari assert "jalan datar bebas"; geometri ramp tidak diubah. |
| Render, kualitas, cuaca | **216 sampel renderer**: dua arena × 12 posisi × high/medium/low × cerah/hujan/kabut. Tidak ada error WebGL. Draw call dan segitiga frame dicatat, bukan estimasi FPS. |
| Cleanup | Buffer/tekstur kedua world dibebaskan saat berpindah ke arena lain; jumlah resource stabil ketika dibangun ulang. State bayangan/siang-malam dipulihkan. |
| Regresi visual | **11 arena lain** dan **14 pasangan GLB** menghasilkan piksel identik dengan baseline setelah masuk/keluar dua world baru. |
| UI, kuis, buff, hasil | **41 pemeriksaan** pada desktop 1366×768 dan HP landscape 844×390: onboarding siswa yang sama, kartu stage, world benar, empat AI, dua slot, buff dari jawaban benar, overflow hadiah, lima kuis, resume dan hasil/kelas tersimpan. Fixture posisi dipakai untuk pemeriksaan UI/hasil, bukan diklaim sebagai balapan manual penuh. |
| Freeze | UI kuis membekukan pemain/AI/buff/clock. Frame render pause/kuis identik pada kedua arena, termasuk obstacle bergerak dan air; piksel berubah ketika clock simulasi diubah. |
| Offline dan Guru | **28 pemeriksaan** jaringan mati: tanpa permintaan aset HTTP/CDN, PIN lokal dapat dibuat, bank guru diekspor, salt/verifier tidak ikut, ekspor dapat memulai balapan di konteks baru. |
| Grand Prix | Empat urutan 3/10/3/13 ronde, ketuntasan dan penyelesaian dinamis lolos unit regression. Konfigurasi dan implementasi GP identik; tidak mengklaim mengulang seluruh GP secara manual. |

Laporan mesin: `*-tests.json`; perbandingan render: [render-parity-tests.json](render-parity-tests.json); detail kamera: [capture-report.json](capture-report.json).

## Ukuran dan rendering

HTML **24.954.319 byte**, bertambah **21.557 byte** dari finalisasi, tetap di bawah 25.000.000 byte. Tidak ada GLB, audio, foto besar atau tekstur unduhan baru. Empat thumbnail memakai WebP 512×320. Label Sail memakai canvas runtime 256×256, menggantikan label lama dengan luas piksel sama; tidak menambah jumlah tekstur world.

| Arena | Segitiga lingkungan lama → baru | Batch warna lama → baru | Batch bayangan baru | Tekstur label runtime |
|---|---:|---:|---:|---:|
| Kayong Utara | 74.130 → 94.596 | 32 → 38 | 16 | 11 |
| Ketapang | 65.930 → 99.670 | 50 → 57 | 21 | 14 |

Angka merupakan seluruh lingkungan, termasuk terrain/road/dekorasi, bukan segitiga landmark saja. Detail objek dibatch berdasarkan material; tidak ada draw call per bangku/jendela. Beban geometri bertambah dan dilaporkan terbuka. Ukuran ZIP, ekspor guru, rentang draw call frame, hash dan metrik lainnya ada di [metrics.json](metrics.json) / [release-metrics.json](release-metrics.json). Tidak ada klaim FPS atau performa HP fisik.

Navigasi langsung `file://` diblokir administrator browser cloud sebagaimana baseline. Offline diuji dengan konteks jaringan mati dan dokumen lokal yang diintersep; direct-file tidak diklaim sudah diuji. Data/PIN memakai kunci lama dan tetap terikat browser/origin yang sama. HTML tidak memerlukan CDN/backend.

## Sumber dan build ulang

[Sumber landmark/komposisi](source/landmarks.js) memakai utilitas batch, material, tekstur label, pohon dan roof yang sudah ada. [Assembler](source/assemble.py) menambahkan satu adapter sebelum aplikasi serta mengganti hanya empat entri thumbnail; engine tidak disalin/refactor.

```sh
python visual-upgrade/patch8a/source/assemble.py
node visual-upgrade/patch8a/source/capture.cjs
python visual-upgrade/patch8a/source/review.py
python visual-upgrade/patch8a/source/thumbnails.py
python visual-upgrade/patch8a/source/assemble.py
node visual-upgrade/patch8a/source/test_physics.cjs
node visual-upgrade/patch8a/source/test_cups.cjs
node visual-upgrade/patch8a/source/kayong_utara-test_world.cjs
node visual-upgrade/patch8a/source/ketapang-test_world.cjs
node visual-upgrade/patch8a/source/kayong_utara-test_clearance.cjs
node visual-upgrade/patch8a/source/ketapang-test_clearance.cjs
node visual-upgrade/patch8a/source/test_render_parity.cjs
node visual-upgrade/patch8a/source/test_browser.cjs
node visual-upgrade/patch8a/source/test_freeze_render.cjs
node visual-upgrade/patch8a/source/test_offline.cjs
python visual-upgrade/patch8a/source/test_scope.py
node visual-upgrade/patch8a/source/test_release.cjs
python visual-upgrade/patch8a/source/package.py
```

Browser tests memakai Chromium/Playwright cloud, server statis root repository pada `127.0.0.1:8000`; maksimal dua proses WebGL berat bersamaan. `test_scope.py` memerlukan checkout Git lengkap. ZIP review memuat baseline HTML dan helper source yang diperlukan untuk rebuild; source arena asli tetap di folder tahap 12/13 pada repository.

Tidak merge, deployment, mengganti index.html online, mengubah alur siswa atau podium, atau mengerjakan patch berikutnya.
