# BlokRaya PRO — PATCH 8D: Fullscreen & Kemudi Analog

Fullscreen diminta langsung dari klik **Mulai Balapan**, dengan fallback viewport responsif ketika browser menolak/tidak mendukung. Analog HP mengatur besar kemudi secara proporsional; tombol klasik, multitouch gas/drift/jump/buff, keyboard dan preferensi lama dipertahankan. Footer persiapan/kuis serta garasi/HUD dirapikan untuk layar pendek.

- [ZIP playable terbaru](blokraya-patch8d-playable.zip) · [HTML mandiri](visual-upgrade/blokraya-patch8d-controls.html) · [ZIP review](blokraya-patch8d-review.zip).
- [Desktop fullscreen](visual-upgrade/patch8d/screenshots/after/fullscreen-1366.png) · [HP portrait](visual-upgrade/patch8d/screenshots/after/race-390.png) · [Analog HP landscape](visual-upgrade/patch8d/screenshots/after/analog-curve-kapuas.png) · [Galeri before–after](visual-upgrade/patch8d/review.html).
- [Sumber dan laporan pengujian](visual-upgrade/patch8d/README.md) · [Metrik](visual-upgrade/patch8d/metrics.json).

HTML **25.003.020 byte** (+17.313; +0,0693%). 359 pemeriksaan bernama lulus: tujuh viewport tanpa overlap dok HUD, fullscreen native masuk/keluar dan fallback, analog/multitouch/reset, wizard/GP, PIN/progres, offline/ekspor. Render 13 world/14 model identik dengan PATCH 8C. HP fisik/Safari dan FPS tidak diklaim diuji; file:// cloud diblokir administrator. Podium PATCH 8C tetap identik. Tidak merge/deployment atau mengubah index.html utama.

# Tahap sebelumnya — PATCH 8C: Podium Tiga Pembalap

Podium kemenangan **2–1–3** memakai karakter dan mobil asli, panggung bertingkat, medali serta perayaan singkat. Bebas memakai urutan finis aktual; GP memakai klasemen akhir dengan tie-break lama. Hasil belajar asli tetap dibuka melalui tombol **Lihat Hasil Belajar**; ronde GP/retry tetap berjalan seperti sebelumnya.

- [ZIP playable terbaru](blokraya-patch8c-playable.zip) · [HTML mandiri](visual-upgrade/blokraya-patch8c-podium.html) · [ZIP review](blokraya-patch8c-review.zip).
- [Desktop](visual-upgrade/patch8c/screenshots/podium-1366x768.png) · [HP portrait](visual-upgrade/patch8c/screenshots/podium-390x844.png) · [HP landscape](visual-upgrade/patch8c/screenshots/podium-844x390.png) · [Galeri](visual-upgrade/patch8c/review.html).
- [Dokumentasi, sumber dan pengujian](visual-upgrade/patch8c/README.md) · [Metrik](visual-upgrade/patch8c/metrics.json).

HTML **24.985.707 byte** (+18.523). 78 kelanjutan AI pada 13 arena mencapai finis tanpa mengubah snapshot siswa/ghost; 56 trio model high/low dan enam layout diuji. 58 pemeriksaan UI peringkat 1–5, 272 pemeriksaan empat GP, offline/ekspor/PIN serta perbandingan piksel 13 world/14 model lolos. Tes GP memakai fixture posisi, bukan balapan manual penuh. Waktu lawan yang belum finis tidak lagi diproyeksikan; dicatat melalui salinan simulasi asli. HP fisik/FPS dan file:// cloud tidak diklaim diuji. Tidak merge/deployment atau mengubah index.html utama.

# Tahap sebelumnya — PATCH 8B: Alur Siswa Ringkas

**Nama/Kelas → Kesulitan → Mode → Arena/Cuaca (Bebas saja) → Garasi → Mulai Balapan.** Grand Prix langsung menuju garasi. Satu carousel arena memakai panah, keyboard, swipe dan daftar ringkas; pengaturan opsional berada dalam accordion. State Bebas/GP terpisah, jumlah soal tetap mengikuti Guru, dan start ganda dicegah.

- [ZIP playable terbaru](blokraya-patch8b-playable.zip) · [HTML mandiri](visual-upgrade/blokraya-patch8b-student-flow.html) · [ZIP review](blokraya-patch8b-review.zip).
- [Galeri setiap tahap + sebelum–sesudah](visual-upgrade/patch8b/review.html) · [Stage HP](visual-upgrade/patch8b/screenshots/390x844-stage-weather.png) · [GP landscape](visual-upgrade/patch8b/screenshots/844x390-mode-grand-prix.png).
- [Dokumentasi, sumber dan laporan pengujian](visual-upgrade/patch8b/README.md) · [Metrik](visual-upgrade/patch8b/metrics.json).

HTML **24.967.184 byte** (+12.865). 61 pemeriksaan navigasi, 42 tampilan enam viewport, 39 kasus metadata carousel dan 235 pemeriksaan transisi empat GP. Offline/ekspor, PIN dan kompatibilitas data diuji; 13 world/14 pasangan model identik secara piksel dengan PATCH 8A. GP memakai fixture posisi untuk pengujian transisi. Landscape pendek mengizinkan scroll lokal terbatas; contoh ekspor guru sekitar 25,003 MB. HP fisik/FPS dan file:// cloud tidak diklaim lulus. Tidak merge/deployment atau mengubah index.html utama.

# Tahap sebelumnya — PATCH 8A: Landmark Kayong Utara & Ketapang

Sail Selat Karimata kini memakai siluet hijau asimetris berlubang, panel batu dan rangka putih berornamen. Ale-Ale mengikuti versi menara jam hijau-kuning pada lampiran; Keraton Matan mempunyai serambi panjang, gable bermahkota dan paviliun sudut. Plaza, taman dan promenade pantai dirapikan; track, physics, obstacle, AI, buff, alur siswa, PIN dan podium tetap dipertahankan.

- [ZIP playable terbaru](blokraya-patch8a-playable.zip) · [HTML mandiri](visual-upgrade/blokraya-patch8a-landmarks.html) · [ZIP review](blokraya-patch8a-review.zip).
- [Sail sebelum–sesudah](visual-upgrade/patch8a/screenshots/comparison-sail-close.jpg) · [Ale-Ale](visual-upgrade/patch8a/screenshots/comparison-ale-close.jpg) · [Keraton Matan](visual-upgrade/patch8a/screenshots/comparison-matan-close.jpg).
- [Dokumentasi, kesesuaian referensi, screenshot dan uji](visual-upgrade/patch8a/README.md) · [Metrik](visual-upgrade/patch8a/metrics.json).

HTML **24.954.319 byte** (+21.557). 18 balapan driver penuh/72 AI finish; 216 sampel renderer, 3.115 sampel lajur dan 192 frame chase, cleanup GPU, kuis/buff/hasil dan offline diuji. 11 world lain serta 14 pasangan GLB identik secara piksel. Foto lampiran menjadi acuan visual; situs sumber diblokir 403 dan foto asli belum dibundel pada lembar review. HP fisik/FPS tidak diklaim diuji. Tidak merge/deployment atau mengganti index.html utama.

# Tahap sebelumnya — Finalisasi 13 Arena (Prompt 7)

Versi final untuk tinjauan melanjutkan HEAD 6J. **13 arena playable**, 14 pasangan karakter/kendaraan dan empat turnamen dipertahankan. Alur siswa kini **Nama dan Kelas → Arena dan Cuaca → Pengaturan Balapan → Karakter → Mulai Game**. Kelas siswa dicatat pada hasil tanpa mengubah bank soal/PIN/data lama.

- [Unduh ZIP playable terbaru](blokraya-pro-final-playable.zip) — ekstrak lalu buka HTML.
- [HTML mandiri](visual-upgrade/blokraya-pro-final.html) · [ZIP review](blokraya-pro-final-review.zip).
- [Dokumentasi, screenshot dan hasil pengujian](visual-upgrade/finalization/README.md) · [Status 13 arena](visual-upgrade/finalization/stage-status.json).
- [Identitas siswa HP](visual-upgrade/finalization/screenshots/identity-390.png) · [13 kartu arena](visual-upgrade/finalization/screenshots/stages-1366.png) · [Pengaturan HP landscape](visual-upgrade/finalization/screenshots/settings-844.png).

HTML **24.932.762 byte** (+5.656 byte). **126 balapan driver referensi** sampai finish, termasuk 42 balapan tiga lap pada semua 14 kendaraan di tiga arena ekstrem; **372 completion AI**. Empat GP lolos 202 pemeriksaan UI/transisi dengan fixture posisi, bukan seluruh GP manual. Semua 13 render arena identik dengan 6J. Offline dan ekspor guru diuji tanpa permintaan aset jaringan. Sebagian AI memakai rescue sah dan tetap finish; HP fisik/FPS dan navigasi file:// cloud tidak diklaim diuji. Tidak merge/deployment atau mengubah index.html utama.

# Tahap sebelumnya — Stage 13 Ketapang: Ale-Ale Chaos Circuit (6J)

Ketapang playable untuk tinjauan: sirkuit kota-pelabuhan fiktif **1.241,93m**, jalan bertingkat19m, jembatan, slalom, ramp/gap dan percabangan. Dua belas zona termasuk kontainer bergeser, palang, rotor, drum, oli dan rangkaian final. Tugu Ale-Ale serta Keraton Matan berada di plaza aman. Langit hangat menjelang sore.

**Seluruh13 arena tersedia.** Kalbar Klasik3 dan Nusantara10 dipertahankan; **Kalbar Extreme Challenge3** dan **Grand Prix Lengkap13 Arena** kini tersedia setelah pengujian transisi/ketuntasan.

- [ZIP playable terbaru](blokraya-stage13-ketapang-playable.zip) — ekstrak, lalu buka HTML di dalamnya.
- [HTML mandiri](visual-upgrade/blokraya-stage13-ketapang.html) · [ZIP review: source, metadata, screenshot dan laporan](blokraya-stage13-ketapang-review.zip).
- [Overview](visual-upgrade/stage13-ketapang/screenshots/overview.png) · [Ale-Ale](visual-upgrade/stage13-ketapang/screenshots/tugu-ale-ale.png) · [Keraton](visual-upgrade/stage13-ketapang/screenshots/keraton-matan.png) · [Jump](visual-upgrade/stage13-ketapang/screenshots/ramp-jump.png).
- [HP landscape](visual-upgrade/stage13-ketapang/screenshots/race-844x390.png) · [Dokumentasi dan hasil uji](visual-upgrade/stage13-ketapang/README.md).

HTML **24.927.106 byte**, bertambah44.827 byte. Lingkungan65.930 segitiga/50 batch warna. Uji18 driver,14 kendaraan,72 completion AI,48 AI rotasi kendaraan, dan3 driver/12 AI tiga lap; collision/rescue/jump/freeze serta offline/ekspor dan kontrol sentuh diuji.28 render lama identik. UI empat turnamen memakai29 ronde sukses+4 gagal/ulang dengan fixture posisi, bukan balapan manual penuh. Landmark belum diverifikasi foto; file:// diblokir cloud dan HP fisik/FPS belum diuji. Tidak merge, deployment, mengganti index.html online atau mengerjakan Prompt7.

# Tahap sebelumnya — Stage 12 Kayong Utara: Coastal Cliff Challenge (6I)

Kayong Utara sudah playable untuk tinjauan: sirkuit pesisir fiktif **1.133,81m**, hairpin/S-curve, elevasi16m, laut turquoise, pantai/kelapa, tebing, bukit tropis dan interpretasi monumen Sail Karimata. Sepuluh zona termasuk batu bolak-balik berperingatan, palang berkala, bridge sempit, kerikil/pasir, gap dan percabangan kiri aman/kanan lompat. Rescue mundur2,4s mempertahankan inventori/token/nilai.

**13 kartu,12 playable; Ketapang tetap Segera Hadir.** Kalbar Klasik3 dan Nusantara10 tetap tersedia; Extreme3/Lengkap13 menunggu Ketapang.

- [ZIP playable terbaru](blokraya-stage12-kayong-utara-playable.zip) — ekstrak, lalu buka HTML di dalamnya.
- [HTML mandiri](visual-upgrade/blokraya-stage12-kayong-utara.html) · [ZIP review: sumber, screenshot, metadata dan laporan](blokraya-stage12-kayong-utara-review.zip).
- [Overview](visual-upgrade/stage12-kayong-utara/screenshots/overview.png) · [Pantai](visual-upgrade/stage12-kayong-utara/screenshots/pulau-datok.png) · [Monumen](visual-upgrade/stage12-kayong-utara/screenshots/sail-karimata.png) · [Jump](visual-upgrade/stage12-kayong-utara/screenshots/bay-jump.png).
- [HP landscape](visual-upgrade/stage12-kayong-utara/screenshots/race-844x390.png) · [Sumber, hasil uji dan keterbatasan](visual-upgrade/stage12-kayong-utara/README.md).

HTML **24.882.279 byte**, bertambah43.311 byte; lingkungan74.130 segitiga dan32 batch warna. Uji18 balapan driver,14 kendaraan,72 completion AI serta3 balapan/12 AI tiga lap lolos; terdapat rescue mundur pada kasus AI, tidak ada warp maju.108 sampel renderer,1.555 titik lajur,96 frame kamera, kuis/PIN/buff/progres/ghost, ekspor offline dan kontrol sentuh emulasi diuji.27 render terlindungi identik dengan baseline Stage11. GP10 UI diuji dengan fixture posisi, bukan balapan manual penuh. Landmark belum diverifikasi foto; file:// diblokir cloud dan HP fisik/FPS belum diuji. Tidak merge, deployment, mengganti index.html online atau membuat Stage13.

# Tahap sebelumnya — Stage 11 Kubu Raya: Mangrove Extreme Run (6H)

Kubu Raya sudah playable: sirkuit papan mangrove **886,86m**, perairan payau, akar bercabang, dermaga/perahu dan mercusuar jauh. Sepuluh zona meliputi tong/pintu bergerak, jembatan sempit, lumpur/genangan, gap bertanda dan dua jalur papan dengan risiko/hadiah berbeda. Rescue mundur ke checkpoint dengan waktu tunggu2,4s, tanpa menghapus inventori/token/nilai.

**13 kartu,11 playable. Kayong Utara dan Ketapang tetap Segera Hadir.** Kalbar Klasik3 dan Nusantara10 tetap; Extreme3 dan Lengkap13 belum aktif.

- [ZIP playable terbaru](blokraya-stage11-kubu-raya-playable.zip) — ekstrak lalu buka `blokraya-stage11-kubu-raya.html`.
- [HTML mandiri](visual-upgrade/blokraya-stage11-kubu-raya.html) · [ZIP review: sumber, screenshot, metadata dan laporan](blokraya-stage11-kubu-raya-review.zip).
- [Mercusuar/mangrove](visual-upgrade/stage11-kubu-raya/screenshots/lighthouse-mangrove.png) · [Lompatan](visual-upgrade/stage11-kubu-raya/screenshots/canal-jump.png) · [Percabangan](visual-upgrade/stage11-kubu-raya/screenshots/fork-routes.png).
- [HP landscape](visual-upgrade/stage11-kubu-raya/screenshots/race-844x390.png) · [Dokumentasi, aturan obstacle/rescue dan pengujian](visual-upgrade/stage11-kubu-raya/README.md).

HTML **24.838.968 byte**, bertambah36.856 byte. Uji collider/jump/rescue,18 balapan driver dan72 completion AI,108 frame render, pause/soal, PIN/progres/ghost/ekspor offline dan sentuh emulasi lolos. Satu AI Santai memakai rescue mundur; tidak ada warp maju. 26 render lama identik. Percabangan memakai koordinat lateral/progres engine, bukan graph rute independen. Landmark merupakan interpretasi belum diverifikasi foto; file:// diblokir browser cloud dan HP fisik/FPS belum diuji. Tidak merge, deployment atau mengubah index.html.

# Tahap sebelumnya — Stage 10 Bromo: Volcano Challenge (6G)

Bromo sudah playable: lintasan vulkanik fiktif **820,41m**, lautan pasir, kawah terbuka beralur, kerucut pendamping, dinding kaldera, kepulan blocky dan horizon pagi. **Seluruh sepuluh arena tersedia; Grand Prix Nusantara dapat dimainkan.** Kalbar Klasik tetap tiga arena awal.

- [ZIP playable terbaru](blokraya-stage10-bromo-playable.zip) — ekstrak lalu buka `blokraya-stage10-bromo.html`.
- [HTML mandiri](visual-upgrade/blokraya-stage10-bromo.html) · [ZIP review: sumber, screenshot dan laporan](blokraya-stage10-bromo-review.zip).
- [Kawah](visual-upgrade/stage10-bromo/screenshots/bromo-crater.png) · [Gameplay](visual-upgrade/stage10-bromo/screenshots/gameplay.png) · [Rekap Nusantara](visual-upgrade/stage10-bromo/screenshots/grand-prix-complete.png).
- HP [portrait](visual-upgrade/stage10-bromo/screenshots/race-390x844.png)/[landscape](visual-upgrade/stage10-bromo/screenshots/race-844x390.png) · menu [sebelum](visual-upgrade/stage10-bromo/screenshots/before-menu.png)/[sesudah](visual-upgrade/stage10-bromo/screenshots/after-menu.png).
- [Sumber, metrik, hasil uji dan keterbatasan](visual-upgrade/stage10-bromo/README.md).

HTML **24.802.112 byte**, naik **37.881 byte**. Lingkungan **15.326 segitiga**, 19 batch warna. Uji balapan/AI, 108 sampel render, UI sepuluh ronde GP beserta gagal/ulang/lolos, kuis/PIN/buff/progres/replay/ekspor offline dan sentuh emulasi lolos. 25 render terlindungi identik. GP browser memakai fixture posisi; bukan sepuluh balapan manual penuh. Landscape adalah interpretasi stylized; referensi web ditolak403. HP fisik/FPS belum diuji; file:// diblokir browser cloud. Tidak merge, deployment atau mengubah index.html.

# Tahap sebelumnya — Stage 9 Bali: Rice Terrace Rush (6F)

Bali sudah playable: lintasan pedesaan fiktif **777,24m**, dua bentang sawah berkontur (enam/empat teras), irigasi, rumpun padi, bukit, kelapa serta bale wisata dan gerbang batu orisinal. Sembilan arena tersedia; Bromo tetap Segera Hadir. Kalbar Klasik tetap tiga arena; Nusantara menunggu Bromo.

- [ZIP playable terbaru](blokraya-stage9-bali-playable.zip) — ekstrak lalu buka `blokraya-stage9-bali.html`.
- [HTML mandiri](visual-upgrade/blokraya-stage9-bali.html) · [ZIP review: sumber, screenshot dan laporan](blokraya-stage9-bali-review.zip).
- [Sawah terasering](visual-upgrade/stage9-bali/screenshots/rice-terraces.png) · [Bale wisata](visual-upgrade/stage9-bali/screenshots/bale-wisata.png) · [Gameplay](visual-upgrade/stage9-bali/screenshots/gameplay.png).
- HP [portrait](visual-upgrade/stage9-bali/screenshots/race-390x844.png)/[landscape](visual-upgrade/stage9-bali/screenshots/race-844x390.png) · menu [sebelum](visual-upgrade/stage9-bali/screenshots/before-menu.png)/[sesudah](visual-upgrade/stage9-bali/screenshots/after-menu.png).
- [Sumber editable, metrik dan laporan uji](visual-upgrade/stage9-bali/README.md).

HTML **24.764.231 byte**, naik **57.329 byte**. Lingkungan **36.988 segitiga**, 22 batch warna. Uji 18 balapan referensi, 18 completion seluruh AI, 108 sampel render, kuis/PIN/buff/progres/replay, ekspor offline dan sentuh emulasi lolos. 24 render terlindungi identik. Referensi web ditolak 403; landscape/arsitektur merupakan interpretasi stylized. HP fisik/FPS belum diuji; file:// diblokir browser cloud. Tidak merge, mengubah index.html, deployment atau mengerjakan6G.

# Tahap sebelumnya — Stage 8 Yogyakarta: Heritage Night Race (6E)

Yogyakarta sudah playable: lintasan kota fiktif **826,23m** pada malam hari, Tugu Pal Putih stylized, taman/plaza, koridor bernuansa Malioboro, lampu hangat, ruko dan gerobak dekoratif. Delapan arena tersedia; Bali dan Bromo tetap Segera Hadir. Kalbar Klasik tetap tiga arena awal; Nusantara menunggu dua world terakhir.

- [ZIP playable terbaru](blokraya-stage8-yogyakarta-playable.zip) — ekstrak lalu buka `blokraya-stage8-yogyakarta.html`.
- [HTML mandiri](visual-upgrade/blokraya-stage8-yogyakarta.html) · [ZIP review: sumber, screenshot dan laporan](blokraya-stage8-yogyakarta-review.zip).
- [Tugu](visual-upgrade/stage8-yogyakarta/screenshots/tugu-pal-putih.png) · [Malioboro](visual-upgrade/stage8-yogyakarta/screenshots/malioboro-corridor.png) · [Gameplay malam](visual-upgrade/stage8-yogyakarta/screenshots/night-boulevard.png).
- HP [portrait](visual-upgrade/stage8-yogyakarta/screenshots/race-390x844.png), [landscape](visual-upgrade/stage8-yogyakarta/screenshots/race-844x390.png) · menu [sebelum](visual-upgrade/stage8-yogyakarta/screenshots/before-menu.png) / [sesudah](visual-upgrade/stage8-yogyakarta/screenshots/after-menu.png).
- [Build, metrik, hasil uji dan batas representasi](visual-upgrade/stage8-yogyakarta/README.md).

HTML **24.706.902 byte**, bertambah **48.630 byte**, tetap di bawah 25 MB desimal. Geometri lingkungan dioptimalkan menjadi **51.508 segitiga**. Uji 18 balapan referensi, 18 completion AI, 108 sampel render, rendering malam/garasi/freeze, kuis/PIN/buff/progres/replay dan ekspor offline lolos. 23 render terlindungi tetap identik. Landmark merupakan interpretasi; referensi web ditolak 403 dan detail belum diverifikasi. HP fisik/FPS belum diuji; file:// diblokir browser cloud. Tidak merge, mengubah index.html, deployment atau mengerjakan 6F.

# Tahap sebelumnya — Stage 7 Bengkayang: Waterfall Adventure (6D)

Bengkayang sudah playable: lintasan fiktif **801,04 m**, air terjun lebar terinspirasi Riam Merasap, kolam/sungai berbatu, dua jembatan, dek pandang dan hutan blocky. Tujuh arena tersedia; Yogyakarta, Bali dan Bromo tetap Segera Hadir. Kalbar Klasik tetap tiga arena awal; Nusantara menunggu tiga world terakhir.

- [ZIP playable terbaru](blokraya-stage7-bengkayang-playable.zip) — ekstrak lalu buka `blokraya-stage7-bengkayang.html`.
- [HTML mandiri](visual-upgrade/blokraya-stage7-bengkayang.html) · [ZIP review: sumber, screenshot dan laporan](blokraya-stage7-bengkayang-review.zip).
- [Air terjun](visual-upgrade/stage7-bengkayang/screenshots/riam-merasap.png) · [Jembatan](visual-upgrade/stage7-bengkayang/screenshots/river-bridge.png) · [Gameplay menuju landmark](visual-upgrade/stage7-bengkayang/screenshots/waterfall-approach.png).
- HP [portrait](visual-upgrade/stage7-bengkayang/screenshots/race-390x844.png), [landscape](visual-upgrade/stage7-bengkayang/screenshots/race-844x390.png) · menu [sebelum](visual-upgrade/stage7-bengkayang/screenshots/before-menu.png) / [sesudah](visual-upgrade/stage7-bengkayang/screenshots/after-menu.png).
- [Build, metrik, hasil uji dan batas representasi](visual-upgrade/stage7-bengkayang/README.md).

HTML **24.658.272 byte**, bertambah **54.786 byte**, tetap di bawah 25 MB desimal. Uji 18 balapan referensi, 18 completion AI, 108 sampel renderer, kuis/PIN/buff/progres/replay dan ekspor offline lolos. Render 14 pasangan dan enam world sebelumnya tetap identik. Landmark merupakan interpretasi stylized; referensi web ditolak 403 dan akurasi geografis belum diverifikasi. HP fisik/FPS belum diuji; `file://` diblokir browser cloud. Tidak merge, mengubah `index.html`, deployment atau mengerjakan 6E.

# Tahap sebelumnya — Stage 6 Kapuas Hulu: Sentarum Lake Circuit (6C)

Arena danau sudah playable: jalur wisata fiktif **836,70 m**, jalan/boardwalk bertiang, pondok pengamatan, dermaga, kano dan hutan rawa blocky. Enam arena tersedia; Stage 7–10 tetap Segera Hadir. Kalbar Klasik tetap tiga arena awal; Nusantara menunggu empat arena lain.

- [ZIP playable terbaru](blokraya-stage6-kapuas-hulu-playable.zip) — ekstrak lalu buka `blokraya-stage6-kapuas-hulu.html`.
- [HTML mandiri](visual-upgrade/blokraya-stage6-kapuas-hulu.html) · [ZIP review: sumber, screenshot dan laporan](blokraya-stage6-kapuas-hulu-review.zip).
- [Danau/pondok](visual-upgrade/stage6-kapuas-hulu/screenshots/sentarum-lake.png) · [Dermaga](visual-upgrade/stage6-kapuas-hulu/screenshots/timber-jetty.png) · [Gameplay](visual-upgrade/stage6-kapuas-hulu/screenshots/gameplay.png).
- HP [portrait](visual-upgrade/stage6-kapuas-hulu/screenshots/race-390x844.png), [landscape](visual-upgrade/stage6-kapuas-hulu/screenshots/race-844x390.png) · menu [sebelum](visual-upgrade/stage6-kapuas-hulu/screenshots/before-menu.png) / [sesudah](visual-upgrade/stage6-kapuas-hulu/screenshots/after-menu.png).
- [Build, metrik, pengujian dan batas representasi](visual-upgrade/stage6-kapuas-hulu/README.md).

HTML **24.603.486 byte**, naik **53.983 byte** dari Sintang, tetap di bawah 25 MB desimal. Uji 18 balapan referensi, 18 completion AI, 108 sampel renderer, item, kuis/PIN/progres/replay serta ekspor offline lolos. Render 14 pasangan dan lima world lama tetap identik. Lanskap adalah interpretasi stylized; akurasi geografis/ekologis belum diverifikasi. HP fisik/FPS belum diuji dan navigasi `file://` diblokir browser cloud. Tidak merge, mengubah `index.html`, deployment atau mengerjakan 6D.

# Tahap sebelumnya — Stage 5 Sintang: Kelam Mountain Run (6B)

Sintang sudah playable: lintasan 905,66 m dengan naik-turun hingga 8 m, hutan tropis blocky, monolit granit terinspirasi Bukit Kelam dan rumah panjang terinspirasi Rumah Betang Ensaid Panjang. Lima arena tersedia; Stage 6–10 tetap Segera Hadir. Kalbar Klasik tetap tiga arena awal; Nusantara masih menunggu lima world lainnya.

- [ZIP playable terbaru](blokraya-stage5-sintang-playable.zip) — ekstrak, lalu buka `blokraya-stage5-sintang.html`.
- [HTML mandiri](visual-upgrade/blokraya-stage5-sintang.html) · [ZIP review: builder, screenshot dan laporan](blokraya-stage5-sintang-review.zip).
- [Monolit](visual-upgrade/stage5-sintang/screenshots/bukit-kelam.png) · [Rumah panjang](visual-upgrade/stage5-sintang/screenshots/betang.png) · [Gameplay](visual-upgrade/stage5-sintang/screenshots/gameplay.png).
- HP [portrait](visual-upgrade/stage5-sintang/screenshots/race-390x844.png), [landscape](visual-upgrade/stage5-sintang/screenshots/race-844x390.png) · [menu stage](visual-upgrade/stage5-sintang/screenshots/menu-desktop.png).
- [Build, metrik, hasil uji dan batas akurasi](visual-upgrade/stage5-sintang/README.md).

HTML **24.549.503 byte**, naik **45.103 byte** dari Sambas, tetap di bawah 25 MB desimal. Uji 18 balapan referensi, 18 completion AI, 108 sampel renderer, permukaan dekorasi, item, kuis, PIN, progres, replay dan ekspor offline lolos. Render 14 pasangan dan empat arena lama tetap identik. Referensi web diblokir; landmark merupakan interpretasi, bukan rekonstruksi terverifikasi. HP fisik/FPS belum diuji dan navigasi `file://` diblokir browser cloud. Tidak merge, mengubah `index.html`, deployment, atau mengerjakan 6C.

# Tahap sebelumnya — Stage 4 Sambas: Royal River Road (6A)

Arena baru Sambas sudah playable: lintasan 687,84 m, kawasan istana Melayu bergaya blocky, jalan tepian sungai, taman/plaza, rumah panggung, promenade, dermaga dan jembatan dekoratif. Empat arena tersedia; Stage 5–10 tetap Segera Hadir. Kalbar Klasik tetap tiga arena, Nusantara menunggu enam world lainnya.

- [ZIP playable terbaru](blokraya-stage4-sambas-playable.zip) — ekstrak, lalu buka `blokraya-stage4-sambas.html`.
- [HTML mandiri](visual-upgrade/blokraya-stage4-sambas.html) · [ZIP review: builder, screenshot dan hasil uji](blokraya-stage4-sambas-review.zip).
- [Istana](visual-upgrade/stage4-sambas/screenshots/palace.png) · [Sungai/promenade](visual-upgrade/stage4-sambas/screenshots/river-promenade.png) · [Kamera gameplay](visual-upgrade/stage4-sambas/screenshots/gameplay.png).
- HP [portrait](visual-upgrade/stage4-sambas/screenshots/race-390x844.png), [landscape](visual-upgrade/stage4-sambas/screenshots/race-844x390.png) · [menu stage](visual-upgrade/stage4-sambas/screenshots/menu-desktop.png).
- [Implementasi, metrik, batas akurasi dan laporan pengujian](visual-upgrade/stage4-sambas/README.md).

HTML **24.504.400 byte**, naik **58.997 byte** dari Prompt 5, tetap di bawah 25 MB desimal. Uji 18 balapan referensi, 18 completion AI, 108 sampel renderer, item, kuis/PIN/progres/replay, ekspor dan jaringan offline lolos. Render 14 pasangan serta tiga world lama tetap identik. Istana merupakan interpretasi blocky; detail historis belum diverifikasi karena akses referensi diblokir 403. HP fisik/FPS belum diuji; navigasi `file://` ditolak kebijakan browser cloud. Tidak merge ke main, mengubah `index.html`, deployment, atau mengerjakan 6B.

# Tahap sebelumnya — PATCH 5: Ten-stage architecture & Grand Prix Nusantara

Distribusi terbaru menyiapkan katalog **10 arena** dengan **3 arena lama playable** dan **7 “Segera Hadir”** yang belum dapat dibuka. Grand Prix **Kalbar Klasik** tetap tiga ronde; **Nusantara** menunggu semua lintasan dan world nyata tersedia. Tidak membangun arena Prompt 6.

- [ZIP playable terbaru](blokraya-patch5-playable.zip) — ekstrak, lalu buka `blokraya-patch5.html`.
- [HTML mandiri](visual-upgrade/blokraya-patch5.html) · [ZIP review, sumber dan bukti uji](blokraya-patch5-review.zip).
- Pemilihan arena [desktop](visual-upgrade/patch5-ten-stages/screenshots/stages-1366x768.png), [HP portrait](visual-upgrade/patch5-ten-stages/screenshots/stages-390x844.png), [HP landscape](visual-upgrade/patch5-ten-stages/screenshots/stages-844x390.png).
- [GP selesai dan rekap ronde](visual-upgrade/patch5-ten-stages/screenshots/grand-prix-complete.png) · [Nusantara belum playable](visual-upgrade/patch5-ten-stages/screenshots/nusantara-blocked.png).
- [Metadata, build, migrasi, laporan pengujian dan rencana distribusi](visual-upgrade/patch5-ten-stages/README.md) · [metrik](visual-upgrade/patch5-ten-stages/release-metrics.json).

HTML **24.445.403 byte**, bertambah **19.452 byte**, masih di bawah 25 MB desimal. ID dan kunci data lama dipertahankan. GP memakai jumlah ronde dinamis; ketuntasan, poin, AI, buff, PIN dan ekspor offline tetap diuji. Render tetap 14 pasangan dan tiga world identik pada pose/kamera tetap. HP fisik/FPS dan navigasi langsung `file://` belum diuji dalam cloud. Tidak merge ke main, mengganti `index.html`, atau deployment.

# Tahap sebelumnya — Mode Siswa & Mode Guru

Distribusi terbaru: poster fullscreen portrait/landscape dengan loading minimum 3 detik, fade 400 ms, pilihan **Mode Siswa** tanpa PIN dan **Mode Guru** dengan PIN lokal. Seluruh gameplay, arena, AI, buff, HUD dan penyimpanan lama dipertahankan.

- [ZIP playable terbaru](blokraya-mode-siswa-guru-playable.zip) — **ekstrak, lalu buka `blokraya-mode-siswa-guru.html`**.
- [HTML mandiri](visual-upgrade/blokraya-mode-siswa-guru.html) · [ZIP review + sumber + screenshot](blokraya-mode-siswa-guru-review.zip).
- Loading [desktop](visual-upgrade/student-teacher-modes/screenshots/loading-1920x1080.png), [HP portrait](visual-upgrade/student-teacher-modes/screenshots/loading-390x844.png), [HP landscape](visual-upgrade/student-teacher-modes/screenshots/loading-844x390.png).
- [Pilih mode](visual-upgrade/student-teacher-modes/screenshots/modes-1366x768.png) · [Buat PIN](visual-upgrade/student-teacher-modes/screenshots/pin-create-phone.png) · [Login PIN](visual-upgrade/student-teacher-modes/screenshots/pin-login-phone.png).
- [Implementasi, pemulihan PIN dan hasil uji](visual-upgrade/student-teacher-modes/README.md) · [metrik](visual-upgrade/student-teacher-modes/release-metrics.json).

Verifier PIN memakai PBKDF2-SHA256 600.000 iterasi dengan salt acak; tidak menyimpan PIN asli, tidak ada PIN bawaan. Login/logout/ganti PIN, cooldown, akses guru, data lama dan ekspor/offline diuji. PIN merupakan pembatas UI lokal, bukan perlindungan terhadap pemilik HTML/storage. HTML **24.425.951 byte**, di bawah 25 MB. HP fisik/FPS belum diuji. Tidak merge ke main, mengganti `index.html`, atau deployment.

# Tahap sebelumnya — Branding BlokRaya

Distribusi terbaru memakai identitas **BlokRaya**, dua poster asli pengguna sesuai orientasi, dan loading **“Memuat...”** yang menunggu kesiapan resource/tampilan. Game tetap offline; seluruh PATCH 1–4.5, 14 pembalap, tiga arena dan perbaikan langit dipertahankan. Kunci penyimpanan lama tetap digunakan.

- [Unduh ZIP playable](blokraya-balap-edukasi-nusantara-playable.zip) — **ekstrak, lalu buka `blokraya-balap-edukasi-nusantara.html`**.
- [HTML mandiri](visual-upgrade/blokraya-balap-edukasi-nusantara.html) · [ZIP review + sumber + poster](blokraya-balap-edukasi-nusantara-review.zip).
- Loading [desktop](visual-upgrade/blokraya-branding/screenshots/loading-1366x768.png), [HP portrait](visual-upgrade/blokraya-branding/screenshots/loading-390x844.png), [HP landscape](visual-upgrade/blokraya-branding/screenshots/loading-844x390.png).
- [Metode/build dan laporan uji](visual-upgrade/blokraya-branding/README.md) · [metrik distribusi](visual-upgrade/blokraya-branding/release-metrics.json).

HTML **24.402.739 byte**, di bawah 25 MB. Poster dioptimalkan tanpa dibuat ulang atau didistorsi. Uji loading, rotasi, kontrol, progres lama, kuis, ekspor guru/offline dan 36 balapan engine berpasangan lolos. HP fisik/FPS belum diuji. Tidak merge ke main, mengganti `index.html` online, atau deployment.

# Tahap sebelumnya — Blocky Sky & Clean Horizon

Distribusi terbaru mempertahankan PATCH 4.5 dan memperbaiki langit ketiga arena: gradient tanpa sambungan, awan blocky berbevel, serta haze yang menyatukan air/daratan jauh dengan horizon. Nuansa Pontianak hangat, Mempawah sejuk, Singkawang cerah. Gameplay, AI, buff, HUD dan model tetap utuh.

- [ZIP playable terbaru](race-quest-pro-sky-horizon-playable.zip) — **ekstrak, lalu buka `race-quest-pro-sky-horizon.html`**.
- [HTML mandiri](visual-upgrade/race-quest-pro-sky-horizon.html) · [ZIP review + sumber + screenshot](race-quest-pro-sky-horizon-review.zip).
- Before–after [Pontianak](visual-upgrade/sky-horizon/screenshots/comparison-pontianak.jpg), [Mempawah](visual-upgrade/sky-horizon/screenshots/comparison-mempawah.jpg), [Singkawang](visual-upgrade/sky-horizon/screenshots/comparison-singkawang.jpg).
- [Metode, hasil uji dan build](visual-upgrade/sky-horizon/README.md) · [metrik](visual-upgrade/sky-horizon/release-metrics.json).

HTML **23.701.999 byte**, naik hanya **2.706 byte**. Langit menggunakan dua draw call, tanpa tekstur baru; awan 3.240/1.800 segitiga high/low. Tes shader, tiga stage, 360 sampel kamera bergerak, kontrol keyboard/touch, kuis, ekspor/offline, serta 36 balapan engine berpasangan lolos. HP fisik/FPS belum diuji. Tidak mengubah `index.html`, merge ke main atau deployment.

# Tahap sebelumnya — PATCH 4.5: Responsive Racing HUD

HUD balapan baru: inventori dua slot di kiri bawah, statistik ringkas di bawah, toolbar seragam dan minimap yang dapat dibuka/ditutup. Area kendaraan tetap bebas. Desktop menyembunyikan kontrol sentuh; HP menampilkan kontrol minimal 44 px, dengan pilihan manual tersimpan melalui Suara/Pause.

- [ZIP playable PATCH 4.5](race-quest-pro-patch4-5-playable.zip) — **ekstrak, lalu buka `race-quest-pro-patch4-5.html`**.
- [HTML mandiri](visual-upgrade/race-quest-pro-patch4-5.html) · [ZIP review + sumber + screenshot](race-quest-pro-patch4-5-review.zip).
- Before–after [desktop](visual-upgrade/patch4-5-responsive-hud/screenshots/comparison-1821x831.jpg), [HP portrait](visual-upgrade/patch4-5-responsive-hud/screenshots/comparison-390x844.jpg), [HP landscape](visual-upgrade/patch4-5-responsive-hud/screenshots/comparison-844x390.jpg).
- [Ringkasan perubahan/build](visual-upgrade/patch4-5-responsive-hud/README.md) · [validasi layout dan interaksi](visual-upgrade/patch4-5-responsive-hud/VALIDATION.md) · [metrik](visual-upgrade/patch4-5-responsive-hud/release-metrics.json).

HTML **23.699.293 byte**, naik **24.626 byte** dari PATCH 4. Matriks 55 kasus layout, kontrol keyboard/touch, kuis, ekspor offline serta 36 balapan engine berpasangan diuji. Smart AI PATCH 4, aturan buff/penilaian, 14 model dan tiga arena tetap dipertahankan. Emulasi HP bukan pengujian perangkat fisik/FPS HP. Tidak mengganti `index.html`, merge ke main, atau deployment.

# Tahap sebelumnya — PATCH 4: Smart Racing AI

Distribusi pengembangan terbaru: empat kepribadian AI, sembilan buff sesuai konteks, inventori terbatas per pos, waktu reaksi, validasi target dan peringatan serangan. Santai tidak menyerang; Sedang dan Menantang memakai serangan/pertahanan dengan cooldown. Batas kecepatan 23 / 31 m/s, tanpa catch-up berdasarkan jarak pemain.

- [ZIP playable PATCH 4](race-quest-pro-patch4-playable.zip) — ekstrak, buka `race-quest-pro-patch4.html`.
- [HTML mandiri](visual-upgrade/race-quest-pro-patch4.html) · [ZIP review + sumber](race-quest-pro-patch4-review.zip).
- [Audit dan tabel keseimbangan](visual-upgrade/patch4-smart-ai/README.md) · [laporan pembanding](visual-upgrade/patch4-smart-ai/BEHAVIOR-REPORT.md) · [grafik](visual-upgrade/patch4-smart-ai/balance-chart.svg).
- HUD [desktop](visual-upgrade/patch4-smart-ai/screenshots/racing-desktop.png) / [HP](visual-upgrade/patch4-smart-ai/screenshots/racing-mobile.png); [peringatan serangan HP](visual-upgrade/patch4-smart-ai/screenshots/warning-mobile.png).

HTML **23.674.667 byte**, naik **19.610 byte** dari PATCH 3, tanpa aset/model/audio baru. Uji 216 balapan engine berpasangan, 108 kasus penyelesaian AI dan 16.000 kesempatan kepribadian terkontrol. Regresi quiz, buff, penyimpanan, Ruang Guru, tiga stage dan ekspor offline lolos. Hasil benchmark bukan win-rate siswa/FPS HP; perangkat fisik belum diuji. Model 14 pembalap dan arena tetap utuh. Tidak merge, mengganti `index.html`, atau deployment.

# Tahap sebelumnya — PATCH 3: Strategic Buff System

Distribusi pengembangan terbaru: **dua slot inventori**, pilihan Ganti/Lewati ketika penuh, **Perisai Pantul, Nitro Ganda, Ban Anti-Selip dan Radar Lintasan**. Cooldown, charge, timer dan kekebalan singkat memakai clock simulasi. Jawaban benar tetap sumber hadiah inventori; skor akademik tetap berdasarkan asesmen.

- [Unduh ZIP playable PATCH 3](race-quest-pro-patch3-playable.zip) — ekstrak, lalu buka `race-quest-pro-patch3.html`.
- [HTML mandiri](visual-upgrade/race-quest-pro-patch3.html) · [ZIP review + sumber + screenshot](race-quest-pro-patch3-review.zip).
- [Audit, tabel durasi/cooldown dan hasil uji](visual-upgrade/patch3-strategic-buffs/README.md).
- HUD desktop: [sebelum](visual-upgrade/patch3-strategic-buffs/screenshots/desktop-before.png) / [sesudah](visual-upgrade/patch3-strategic-buffs/screenshots/desktop-after.png). HP: [sebelum](visual-upgrade/patch3-strategic-buffs/screenshots/mobile-before.png) / [sesudah](visual-upgrade/patch3-strategic-buffs/screenshots/mobile-after.png).
- [Inventori penuh HP](visual-upgrade/patch3-strategic-buffs/screenshots/overflow-mobile.png) · [Radar HP](visual-upgrade/patch3-strategic-buffs/screenshots/radar-mobile.png) · [metrik](visual-upgrade/patch3-strategic-buffs/release-metrics.json).

HTML **23.655.057 byte**, naik **16.497 byte** dari PATCH 2, di bawah 25 MB. Tidak mengubah strategi AI, model 14 pembalap, atau arena. Inventori berlaku per balapan; bank/profil/hasil belajar tersimpan seperti baseline, tanpa fitur save/resume mid-race. Offline diuji dalam browser cloud dengan jaringan dimatikan; HP fisik belum diuji. Tidak mengganti `index.html`, merge ke `main`, atau deployment.

# Tahap sebelumnya — PATCH 2: Audio & VFX

**Distribusi pengembangan terbaru:** audio arcade dinamis, pengaturan Master/Musik/SFX/Mesin/Mute, mode suara ringan dan Reduced Effects. Musik tetap berjalan pelan saat soal; suara balapan dan VFX dunia berhenti. Model, arena, aturan AI dan buff dipertahankan.

- [ZIP playable PATCH 2](race-quest-pro-patch2-playable.zip) — **unduh, ekstrak, buka `race-quest-pro-patch2.html`, lalu klik/sentuh untuk mengaktifkan audio**.
- [HTML mandiri](visual-upgrade/race-quest-pro-patch2.html) · [ZIP review + sumber](race-quest-pro-patch2-review.zip).
- [Preview SFX sintesis](visual-upgrade/patch2-audio-vfx/audio-review/arcade-sfx-preview.ogg) · [audit/daftar audio, ukuran dan hasil uji](visual-upgrade/patch2-audio-vfx/README.md).
- Before–after: [Turbo](visual-upgrade/patch2-audio-vfx/comparisons/comparison-turbo.jpg), [perisai](visual-upgrade/patch2-audio-vfx/comparisons/comparison-shield.jpg), [landing](visual-upgrade/patch2-audio-vfx/comparisons/comparison-landing.jpg).
- Pengaturan: [desktop](visual-upgrade/patch2-audio-vfx/screenshots/audio-desktop.png), [HP](visual-upgrade/patch2-audio-vfx/screenshots/audio-mobile.png).

HTML **23.638.560 byte**, naik 24.802 byte dari PATCH 1. Empat belas berkas OGG lama tetap identik, tanpa berkas audio tambahan di HTML. SFX baru berupa sintesis Web Audio orisinal; belum diuji melalui HP/speaker fisik. Offline penuh, tidak mengganti `index.html` online atau melakukan deployment.

# Tahap sebelumnya — PATCH 1: Garasi & Stage Selection

**Distribusi pengembangan terbaru:** bengkel balap 3D, preview pembalap lebih menonjol, dan kartu arena bergambar dari render game asli. Seluruh 14 pasangan blocky serta arena Pontianak, Mempawah dan Singkawang dipertahankan.

- [ZIP playable PATCH 1](race-quest-pro-patch1-playable.zip) — **unduh, ekstrak, lalu buka `race-quest-pro-patch1.html`**. Semua aset tertanam, playable offline.
- [HTML mandiri](visual-upgrade/race-quest-pro-patch1.html) · [ZIP review + sumber + aset](race-quest-pro-patch1-review.zip).
- Before–after garasi: [desktop](visual-upgrade/patch1-garage-stage/comparisons/comparison-garage-desktop.jpg), [HP](visual-upgrade/patch1-garage-stage/comparisons/comparison-garage-mobile.jpg).
- Pemilihan stage: [sebelum–sesudah](visual-upgrade/patch1-garage-stage/comparisons/comparison-setup-desktop.jpg), [kartu HP](visual-upgrade/patch1-garage-stage/after/stages-mobile.png).
- [Laporan build, pengujian, ukuran dan keterbatasan](visual-upgrade/patch1-garage-stage/README.md). HTML **23.613.758 byte**, di bawah 25 MB. `index.html` online dan `main` tetap utuh; tidak ada deployment.

# Tahap sebelumnya — Singkawang Stage 3

**Distribusi pengembangan terbaru:** Stage 3 bertema pantai Singkawang, Tugu Naga dan ornamen Imlek. Stage 1 Pontianak, Stage 2 Mempawah, serta seluruh 14 pasangan blocky tetap utuh.

- [ZIP playable Singkawang](race-quest-pro-singkawang-stage3-playable.zip) — ekstrak, buka HTML, pilih **Stage Singkawang · Pantai Meriah** pada menu Mulai.
- [HTML mandiri terbaru](visual-upgrade/race-quest-pro-singkawang-stage3.html) · [ZIP review](race-quest-pro-singkawang-stage3-review.zip).
- Before–after: [Tugu Naga](visual-upgrade/stage3-singkawang/comparisons/comparison-naga.jpg), [Imlek](visual-upgrade/stage3-singkawang/comparisons/comparison-imlek.jpg), [pantai](visual-upgrade/stage3-singkawang/comparisons/comparison-beach.jpg).
- [Laporan ukuran, pengujian dan sumber](visual-upgrade/stage3-singkawang/README.md). HTML **23.394.232 byte**. Cuaca tema Stage 3 kini Cerah; pilihan Hujan/Kabut dan seluruh mekanik tetap tersedia. 6.000 langkah physics berpasangan identik dengan baseline.

## Tahap sebelumnya — Mempawah Stage 2

**Hasil Stage 2:** Stage 2 bertema jalanan taman Mempawah, Tugu Pak Tani dan Keraton Mempawah. Stage 1 Pontianak dan seluruh 14 pasangan blocky tetap utuh; Stage 3 belum diubah.

- [ZIP playable Mempawah](race-quest-pro-mempawah-stage2-playable.zip) — ekstrak, buka HTML, pilih **Stage Mempawah · Jalanan Taman** pada menu Mulai.
- [HTML Stage 2](visual-upgrade/race-quest-pro-mempawah-stage2.html) · [ZIP review](race-quest-pro-mempawah-stage2-review.zip).
- Before–after: [Pak Tani](visual-upgrade/stage2-mempawah/comparisons/comparison-pak-tani.jpg), [Keraton](visual-upgrade/stage2-mempawah/comparisons/comparison-keraton.jpg), [taman](visual-upgrade/stage2-mempawah/comparisons/comparison-garden.jpg).
- [Laporan ukuran, pengujian dan sumber](visual-upgrade/stage2-mempawah/README.md). HTML **23.378.794 byte**. Hujan/handling bawaan, ramp, gap, soal, AI dan fitur lain tetap berlaku.

## Tahap sebelumnya — Pontianak Stage 1

**Hasil Stage 1:** Stage 1 bertema jalanan kota Pontianak, Tugu Khatulistiwa dan Tugu Bambu, dengan 14 pasangan blocky Batch 4 tetap utuh.

- [ZIP playable Pontianak](race-quest-pro-pontianak-stage1-playable.zip) — ekstrak dan buka HTML offline.
- [HTML Stage 1](visual-upgrade/race-quest-pro-pontianak-stage1.html) · [ZIP review](race-quest-pro-pontianak-stage1-review.zip).
- Before–after: [Khatulistiwa](visual-upgrade/stage1-pontianak/comparisons/comparison-tugu-khatulistiwa.jpg), [Bambu](visual-upgrade/stage1-pontianak/comparisons/comparison-tugu-bambu.jpg), [kota](visual-upgrade/stage1-pontianak/comparisons/comparison-city.jpg).
- [Laporan ukuran, pengujian dan sumber](visual-upgrade/stage1-pontianak/README.md). HTML 23.362.544 byte. Stage 2–3 dan seluruh aset karakter/kendaraan tetap identik; aturan balapan tidak berubah.

## Arsip — 14 pasangan blocky

**Hasil Batch 4:** Panda–Bamboo, Koala–Eco Pod dan Rakun–Trail Pickup melengkapi seluruh 14 pasangan. Sebelas pasangan sebelumnya dipertahankan utuh dari baseline `ddc28f8`.

- [ZIP playable terbaru](race-quest-pro-batch4-playable.zip) — ekstrak lalu buka HTML.
- [HTML mandiri](visual-upgrade/race-quest-pro-batch4.html) · [paket review](race-quest-pro-batch4-review.zip).
- Paket review memuat enam GLB high/low Batch 4, tiga Blender, builder, enam avatar, screenshot, lineup serta laporan.
- [14 karakter](visual-upgrade/batch4/comparisons/complete-character-lineup.jpg) · [14 kendaraan](visual-upgrade/batch4/comparisons/complete-vehicle-lineup.jpg) · [14 pasangan](visual-upgrade/batch4/comparisons/complete-pair-lineup.jpg).
- Before–after: [Panda](visual-upgrade/batch4/comparisons/panda/comparison-sheet.jpg), [Koala](visual-upgrade/batch4/comparisons/koala/comparison-sheet.jpg), [Rakun](visual-upgrade/batch4/comparisons/rakun/comparison-sheet.jpg).
- [Laporan dan batas pengujian](visual-upgrade/batch4/README.md) · [status 14 karakter](visual-upgrade/batch4/character-status.json) · [katalog metrik lengkap](visual-upgrade/batch4/complete-asset-catalog.json).

HTML **23.349.280 byte (23,35 MB)**, seluruh aset tertanam dan di bawah target 25.000.000 byte. Aturan game, bank soal, data siswa/profil, harga unlock 60 token, AI, Grand Prix, kontrol, progres, ghost, audio, ekspor dan penyimpanan tidak diubah. Panda tersedia pada halaman 2; Koala dan Rakun pada halaman 3 garasi.

`index.html` online dan `main` tetap utuh. Tidak ada deployment. Versi Stage 1 hanya memperbarui visual Stage 1; hasil Mempawah melanjutkan perubahan visual Stage 2, dan hasil Singkawang terbaru memperbarui visual Stage 3.
Riwayat [Batch 3](visual-upgrade/batch3/README.md), [Batch 2](visual-upgrade/batch2/README.md), [Batch 1](visual-upgrade/batch1/README.md) dan [Kucing blocky](visual-upgrade/cat-blocky/README.md) tetap tersedia.
