# Validasi PATCH 4.5

## Layout dan komposisi

`layout-tests.json` merekam bounding rectangle komponen aktif, ukuran target, hit-test pada pusat tombol, overflow teks, area tengah dan mode input. Matriks mencakup:

| Perangkat/emulasi | Viewport CSS px |
|---|---|
| Desktop fine pointer | 1920×1080, 1821×831, 1366×768 |
| Tablet touch | 768×1024, 1024×768 |
| HP touch portrait | 390×844, 320×568 |
| HP touch landscape | 844×390, 640×320 |

Enam kondisi per ukuran: normal, satu slot, dua slot, aktif/cooldown dengan radar, ancaman AI, di udara. Ditambah manual-touch desktop: **55 kasus**. Pemeriksaan juga mencakup bidang internal posisi/waktu/nama stage agar kartu gabungan tidak saling menimpa. Peta diperluas diuji pada kedua landscape pendek. Target tombol balapan minimal **44×44 CSS px**, pusat tombol dapat diklik kecuali memang disabled oleh cooldown/status.

Kriteria otomatis: tidak ada overlap antarkelompok permanen; tidak keluar viewport; tidak ada overflow horizontal atau teks penting; panel permanen di luar area 32–68% horizontal ×25–80% vertikal; notifikasi tidak menutupi fokus kendaraan 40–60% ×45–80%. Area panel kuis/Pause adalah dialog modal dan sengaja menutupi permainan yang dijeda. Bukti desktop/HP tersedia di folder screenshot.

Percobaan awal menemukan overlap kecil antara inventori portrait dan panel kecepatan serta inventori terlalu lebar pada 320 px. Perbaikan mengangkat inventori portrait di atas tinggi penuh panel statistik dan menyusun slot vertikal pada layar sangat sempit. Laporan final memeriksa hasil perbaikan. Error 404 awal berasal dari favicon server pengujian; harness menyuplai respons 204 untuk favicon, sambil tetap mencatat seluruh error JavaScript/console lainnya.

## Interaksi aktual

`controls-tests.json`: A/D, rem, loncat, drift, Q/1/2, E, dua slot dan charge/cooldown; kecepatan/token/minimap berubah; tombol Suara dan penyimpanan audio, Pause/resume, fullscreen enter/exit dan restart konfirmasi/cancel. Restart membuka jalur Pause asli sebelum konfirmasi sehingga waktu tidak berjalan di belakang prompt. Input keyboard tetap memakai handler asli.

Touch diuji melalui input CDP asli: arah, gas/rem, loncat, pemilihan/pemakaian slot. Pergantian input keyboard → sentuh tidak kehilangan tap pertama. Manual-show tetap aktif saat keyboard digunakan; manual-hide meniadakan tombol. `input-edge-tests.json` menambahkan touch steering + drift bersamaan, Space, orientasi, map expand/collapse dan persistensi, emulasi inset notch, Reduced Motion, antrean prioritas dan kedaluwarsa pesan menurut waktu simulasi.

Kuis nyata diuji benar/salah, dua slot penuh, Ganti/Lewati, resume, Pause, hasil dan nilai akademik. Jawaban salah tidak memberi buff. Pause/soal membekukan waktu dan status dunia. Dialog portrait/landscape direkam pada `dialog-tests.json` dan screenshot. `persistence-tests.json` menguji pengaturan guru, penyimpanan hasil asesmen, strategi, progres/profil/ghost dan pemulihan setelah reload. Tidak ada unlock/token demonstrasi di HTML distribusi.

## Perlindungan gameplay dan aset

- `scope-tests.json`: membalik sembilan perubahan terbatas beserta blok HUD baru menghasilkan PATCH 4 **persis**. Hash 14 komponen penting identik, mencakup Smart Racing AI, callback reward, fisika, asesmen, renderer, tiga stage, audio/VFX, garasi dan stage selection. **1.755 berkas historis** dipertahankan identik dengan baseline.
- `engine-parity.json`: **36 balapan lengkap berpasangan**, 3 stage ×3 kesulitan ×4 seed. Setiap langkah pemain/AI, stok, cooldown, proyektil, soal, nilai, token, ghost dan waktu putaran identik antara PATCH 4 dan 4.5.
- `ai-tests.json`, `personality-tests.json`: 11 pemeriksaan AI dan 16.000 kesempatan kepribadian terkontrol, termasuk batas informasi/target, cooldown dan pertahanan. Tidak mengubah AI untuk memperbaiki layout.
- `core-test-results.json`: regresi bank/CSV/JSON, pengaturan jumlah soal, tiga stage, tingkat kesulitan, GP gating/retry/penyelesaian tiga ronde, jump/drift, buff, kuis dan hasil/progres.
- `stage-audio-tests.json`: ketiga arena, audio, pool VFX dan WebGL.
- `unchanged-renders.json`: 16 render berpasangan (14 pasangan + cat low + vehicle-only) identik per kanal RGBA pada kamera/pencahayaan tetap. Seluruh model dilindungi tanpa pembangunan ulang.

## Offline dan ekspor guru

`offline-test-results.json` memuat game dan memulai balapan dengan jaringan browser dimatikan, tanpa permintaan aset HTTP. `export-tests.json` mengekspor HTML melalui Ruang Guru lalu mengujinya offline: 94 aset model/avatar/audio dan enam thumbnail tetap utuh; tiga kartu stage, pemilihan Singkawang, sembilan buff, dua slot, Smart AI dan satu HUD baru tetap tersedia. Kontrol preview ekspor tidak terduplikasi.

Browser cloud melarang `file://`; pengujian menyuplai byte HTML lokal sebagai dokumen utama ke konteks offline. Pengguna tetap memperoleh HTML mandiri yang seluruh dependensinya tertanam, tanpa CDN. ZIP diverifikasi melalui CRC dan kesamaan byte HTML dengan distribusi.

## Ukuran dan biaya tambahan

HTML **23.699.293 byte**, baseline PATCH 4 **23.674.667 byte**, pertumbuhan **24.626 byte** (sekitar 0,10%); di bawah **25.000.000 byte**. Ekspor guru pengujian **23.781.360 byte**. Lihat `release-metrics.json` untuk hash, ukuran ZIP dan pengukuran final.

HUD baru tidak menambah model, tekstur, audio, buffer GPU, atau draw call WebGL. Pembaruan mengikuti siklus UI yang sudah ada, tanpa loop requestAnimationFrame baru. Pengukuran terisolasi 200 pemanggilan JavaScript HUD pada browser cloud: **26,9 ms total /0,1345 ms per pemanggilan**, 108 node dalam area balapan. Pengukuran berupa penulisan DOM berkelompok tanpa flush layout/render; **bukan biaya frame lengkap, FPS, atau benchmark HP nyata**. Tidak ada klaim peningkatan FPS dibanding baseline.

## Batas pengujian

HP/tablet, pointer dan notch diuji lewat emulasi; perangkat fisik/laptop hybrid belum diuji. Fullscreen diuji pada Chromium cloud; dukungan browser HP tetap mengikuti browser. Grand Prix diuji di engine, bukan seluruh balapan dimainkan manual. Screenshot state terkontrol menguji tampilan, sedangkan tes interaksi dan simulasi menguji perilaku. Tidak dilakukan redesign model/arena, perubahan aturan buff, atau pekerjaan PATCH 5.
