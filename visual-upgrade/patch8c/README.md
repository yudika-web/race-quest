# BlokRaya PRO — PATCH 8C: Podium Tiga Pembalap

Podium 3D menampilkan **peringkat 2 di kiri, 1 di tengah/tertinggi, 3 di kanan**, lengkap dengan karakter dan kendaraan asli, nama pembalap, serta warna perak/emas/perunggu. Tidak membuat model karakter baru.

Baseline: `659e74b524f674b8a7c9275ab9b1207ba7ebceba` (HEAD PATCH 8B), branch `dev/race-quest-cat-sport-visual-upgrade`.

- [HTML playable mandiri](../blokraya-patch8c-podium.html).
- [ZIP playable](../../blokraya-patch8c-playable.zip) · [ZIP review: sumber, screenshot, laporan](../../blokraya-patch8c-review.zip).
- [Galeri screenshot asli](review.html) · [Desktop](screenshots/podium-1366x768.png) · [HP portrait](screenshots/podium-390x844.png) · [HP landscape](screenshots/podium-844x390.png).
- [Metrik](metrics.json) · [SHA HTML/ZIP](release-metrics.json).

## Pencatatan hasil yang sah

Audit menemukan bahwa `Session.result()` lama memperkirakan waktu lawan yang belum finis menggunakan jarak tersisa dibagi 23. Data ini belum cukup untuk podium tiga finisher.

Adapter hasil baru mengambil snapshot hasil siswa dan ghost tepat saat siswa finis. Lawan yang belum finis dilanjutkan pada **salinan sesi** memakai `Session.advance(1/60)` beserta Smart AI, item, collision, obstacle dan rescue yang sama. Peserta yang sudah finis tidak ikut lagi dalam physics aktif pada salinan. Tidak memindahkan AI ke garis finish dan tidak mengarang waktu AI.

Pemrosesan berlangsung dalam batch dengan anggaran sekitar 6 ms lalu yield, sehingga halaman tetap responsif. Waktu siswa, jawaban, token, posisi dan ghost tidak ditambah durasi penyelesaian AI. Tape RNG menjaga urutan angka acak sesi asli tetap sama apabila dibaca kembali setelah hasil dicatat.

Hasil tersimpan mempertahankan field lama dan menambah:

- `racers`: lima peserta yang benar-benar ikut, ID yang sudah dipakai GP, nama, indeks karakter, jarak dan waktu finis aktual/status DNF.
- `classification`: versi, metode pencatatan, jumlah langkah simulasi lanjutan dan status kelengkapan.
- `finishOrder`: urutan waktu aktual, menggantikan proyeksi untuk hasil baru. Poin GP **25/18/15/12/10** dan aturan tie-break tidak diubah.

Batas simulasi mencegah penantian tanpa akhir. Bila completion tidak lengkap, waktu yang tidak diketahui tetap `null` dengan status **DNF**; tidak diganti waktu perkiraan. Jika belum ada tiga finisher terkonfirmasi, laporan akademik tetap dibuka tanpa podium palsu. Seluruh 78 kasus kelanjutan AI yang diuji mencapai finis lengkap.

## Alur dan tampilan

- **Bebas:** finis → podium → **Lihat Hasil Belajar** → laporan akademik asli.
- **GP ronde biasa atau gagal ketuntasan:** tetap langsung ke laporan dan tombol lanjut/retry lama.
- **GP tuntas:** podium memakai `gp.standings` akhir, termasuk tie-break poin → jumlah kemenangan → ID peserta seperti sebelumnya. Peringkat ronde terakhir tetap terpisah dari klasemen cup dan skor akademik.
- Siswa peringkat 4/5 menerima pesan sesuai posisi dan tidak ditampilkan sebagai juara.
- **Balapan Lagi** dan **Menu Utama** tersedia pada podium serta laporan. Memulai sesi baru membersihkan identitas podium sebelumnya.
- Garasi, alur siswa PATCH 8B, PIN Guru, hasil lama, impor/ekspor, 13 arena, 14 pasangan model, sembilan buff dan dua slot dipertahankan.

Satu renderer/canvas lama dipakai kembali. Model dan rig berasal dari GLB tertanam yang sama, dengan skala presentasi podium dan ekspresi ringan. Panggung prosedural menggunakan delapan batch warna, podium bertingkat, panel kotak dan lampu emissive dekoratif. Tidak menambah lampu/shadow map dinamis atau tekstur. Portrait memakai susunan ruang bertingkat, sementara desktop/landscape horizontal. Kamera menghitung framing dari bounds GLB agar mobil, telinga dan ekor tetap terlihat.

Confetti berakhir setelah sekitar tiga detik; animasi model singkat berhenti setelah enam detik. Reduced Motion/Reduced Effects membekukan pose dan meniadakan confetti. Audio memakai mekanisme kemenangan serta pengaturan mute/volume yang sudah ada, tanpa memulai AudioContext baru secara otomatis.

## Pengujian aktual

| Laporan | Cakupan |
|---|---|
| [Klasifikasi](classification-tests.json) | 78 kelanjutan AI: 13 arena × 3 tingkat × 2 seed; semuanya finis. Snapshot siswa, waktu, skor, token, posisi, ghost dan urutan RNG tetap sama. Termasuk peringkat 1–5, tie waktu, DNF terbatas dan tie-break empat cup |
| [Browser](browser-tests.json) | 58 pemeriksaan: posisi siswa 1–5, model sesuai hasil, pesan jujur, kuis freeze, mute, hasil belajar, print, JSON/CSV, replay/home langsung dari podium, reload serta ekspor HTML setelah podium terpasang |
| [Render/layout](render-tests.json) | 56 trio high/low desktop/portrait mencakup seluruh 14 pasangan GLB. Enam viewport: 1920×1080, 1366×768, 390×844, 844×390, 768×1024, 1024×768; tanpa scroll halaman, overlap panel atau model keluar frame. Buffer panggung dilepas saat ditutup |
| [Tie dan nama panjang](tie-layout-tests.json) | Fixture poin cup melalui kelas GP asli: wins mengalahkan ID, lalu ID menjadi tie-break terakhir. Siswa posisi 4 tidak mendapat pesan juara. Nama panjang/cup 13 ronde juga diuji di 320×568 |
| [Empat Grand Prix](grand-prix-browser-tests.json) | 272 pemeriksaan; 29 ronde tuntas dan empat gagal/ulang. Podium hanya pada akhir cup yang lolos ketuntasan dan mengikuti poin akhir; retry, rekap, progres, ghost dan PIN tetap benar |
| [Offline](offline-tests.json) | 29 pemeriksaan, termasuk podium pada jaringan nonaktif, kuis, buff, kontrol, hasil, PIN dan game hasil ekspor. **0 permintaan aset HTTP/CDN** |
| [Kompatibilitas](compatibility-tests.json) | 13 pemeriksaan: bank, token/XP/unlock, progres lama, PIN, ekspor tanpa identitas siswa/verifier dan tanpa ID wizard ganda |
| [Perlindungan sumber](scope-tests.json) | 51 payload lama identik: engine, physics, AI, buff, stage, loader, rig, aset serta onboarding PATCH 8B. Modul PIN hanya bertambah daftar screen inert/export; fungsi KDF/guard/storage tidak berubah. Laporan akademik, CSV, penilaian dan start balapan identik |
| [Render arena/model lama](render-parity-tests.json) | 13 world setelah meninggalkan podium serta 14 model menghasilkan piksel identik terhadap PATCH 8B; tidak ada error JavaScript/WebGL |
| [HTTP](release-smoke.json) | Dokumen normal dari server lokal memiliki SHA release yang sama dan membuka Mode Siswa dengan benar |

Tes peringkat/GP browser memakai fixture posisi pada gerbang soal/finish untuk memeriksa UI dan hasil; bukan balapan manual seluruh turnamen. Screenshot layout/model juga memakai fixture peserta pada renderer asli. Tes AI melanjutkan physics asli sampai finis dari fixture siswa yang sudah selesai; bukan teleport AI. Tidak memakai ilustrasi generatif.

HP diuji melalui emulasi viewport Chromium. HP fisik, Safari dan FPS perangkat tidak diklaim diuji. Browser cloud menolak `file://` dengan `ERR_BLOCKED_BY_ADMINISTRATOR`; offline diuji melalui konteks jaringan mati dan dokumen lokal yang diintersepsi, serta HTTP biasa. HTML tetap satu file dengan aset tertanam tanpa server/CDN wajib.

## Ukuran dan biaya rendering

- HTML baseline: **24.967.184 byte**.
- HTML PATCH 8C: **24.985.707 byte** (+18.523, sekitar 0,074%). Masih di bawah sasaran 25.000.000 byte.
- Contoh ekspor guru: **25.021.107 byte**; setelah garasi: **25.021.173 byte**; setelah podium/hasil: **25.022.790 byte**. Tambahan bank/markup runtime membuat ekspor sedikit di atas sasaran; tidak ada pengurangan model atau fitur.
- Panggung baru: **1.752 segitiga / 8 batch warna / 0 tekstur baru**. Kontak memakai tiga shadow sederhana yang sudah tersedia.
- Pengukuran submit frame podium penuh termasuk tiga GLB: **83–105 draw call**, **19.006–62.043 segitiga** untuk variasi pasangan/LOD yang diuji.
- Maksimum enam entri model kart (high+low untuk tiga peserta); tidak ditemukan buffer panggung yang masih hidup tanpa pemilik setelah 56 kali keluar podium.
- Waktu CPU persiapan GLB/upload/panggung dan submit pertama pada cloud: sekitar **15,1–75,1 ms**, median **25,8 ms**. Ini bukan waktu GPU steady state atau FPS HP.

## Sumber dan build

- [classification.js](source/classification.js): pencatatan urutan nyata, simulasi copy, RNG tape dan fallback DNF.
- [podium.js](source/podium.js): identitas peserta, panggung batched, framing, render, animasi dan cleanup.
- [podium.html](source/podium.html) / [podium.css](source/podium.css): UI hasil, responsif dan Reduced Motion.
- [assemble.py](source/assemble.py): integrasi minimum pada baseline yang dipastikan SHA-nya. `application.js` merupakan salinan keluaran untuk review; edit modul atau transformasi assembler, lalu build ulang.

Dari root repository:

```sh
python visual-upgrade/patch8c/source/assemble.py
node visual-upgrade/patch8c/source/test_classification.cjs
python -m http.server 8000
```

Pada terminal lain jalankan file browser `test_browser.cjs`, `test_render.cjs`, `test_tie_layout.cjs`, `test_gp_browser.cjs`, `test_offline.cjs`, `test_compatibility.cjs`, `test_render_parity.cjs`, `test_release.cjs`. Helper memakai `/usr/bin/chromium` dan Playwright cloud; `PLAYWRIGHT_MODULE=playwright` dapat digunakan dengan instalasi lokal.

```sh
python visual-upgrade/patch8c/source/test_scope.py
python visual-upgrade/patch8c/source/report.py
python visual-upgrade/patch8c/source/package.py
```

ZIP review menyertakan baseline PATCH 8B dan sumber untuk build ulang. Tes scope Git memerlukan checkout beserta commit baseline. Paket memverifikasi CRC dan kecocokan byte HTML/sumber/screenshot; hash diri ZIP review dicatat di repository, bukan di dalam arsipnya sendiri.

Tidak mengubah `index.html` online, tidak merge ke `main`, tidak deployment, dan tidak redesign arena.
