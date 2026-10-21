# PATCH 8G — Tipografi, spacing, dan microcopy

Baseline terverifikasi: `0616727a46b6894d041f3604b1345b7f64d27129` (PATCH 8F). Distribusi: `../blokraya-patch8g-ui-polish.html`.

## Perubahan yang diterapkan

| Area | Sebelum | Sesudah |
| --- | --- | --- |
| Identitas | Nama panggilan | Nama Siswa |
| Identitas | Kelas siswa | Kelas |
| Petunjuk identitas | Nama dan kelas dicatat pada hasil belajar. Konfirmasikan sebelum melanjutkan. | Masukkan nama dan kelas untuk mencatat hasil belajarmu. |
| Validasi nama | Isi nama pembalap. | Nama belum diisi. Masukkan nama untuk melanjutkan. |
| Validasi kelas | Isi kelas siswa. | Kelas belum diisi. Masukkan kelas untuk melanjutkan. |
| Progres wizard | Persiapan … / … · berikutnya: garasi (semua tahap) | Langkah … dari … · Berikutnya: tahap aktual |
| Kartu kesulitan/mode | Huruf kapital penuh | Santai / Sedang / Menantang; Balapan Bebas / Grand Prix |
| Pilihan Mode Siswa | teman AI | lawan komputer |
| Preferensi kontrol | sesuai perangkat/input | sesuai perangkat dan kontrol |

Progres mengikuti `step` dan `setupMode` yang sudah ada: Bebas 1–4, Grand Prix 1–3. Berikutnya adalah Tingkat Kesulitan, Mode Balapan, Arena dan Cuaca (Bebas), lalu Pilih Karakter. Pergantian mode, Kembali, serta kembali dari garasi diuji. Tidak ada wizard/state penyimpanan baru.

## CSS dan audit seluruh permukaan

Satu blok CSS terisolasi, `patch8gTypography`, ditambahkan setelah style yang sudah ada. Tidak ada warna, model, font unduhan, atau aset visual baru.

- **Identitas:** judul 28 px desktop, 24 px portrait kecil, 22 px landscape pendek; line-height 1,2. Label 14 px semibold, input 16 px, padding horizontal 15 px, gap label–input 9 px. Kelompok dan deskripsi berjarak 20 px (18 px vertikal pada landscape pendek). Dua input sejajar pada layar lebar; bertumpuk pada HP portrait. Gutter tetap sama dengan header/footer.
- **Kesulitan/mode/arena/cuaca:** kapitalisasi diperjelas; line-height kartu dan deskripsi ditata. Teks cup 12 px, status 11 px; ringkasan arena 12–13 px, 11 px pada landscape pendek. Cuaca tetap memakai kontrol dan nilai engine lama.
- **Pengaturan Lanjutan:** gap 16 px dan label/input konsisten. Jumlah soal guru tetap read-only. Panel tetap tertutup secara default dan memakai scroll lokal jika perlu.
- **Garasi/pembelian:** status karakter menjadi 10 px (9 px pada landscape pendek), pilihan warna 12 px (11 px pada landscape pendek), ringkasan konfigurasi 11 px/10 px. Dialog pembelian memakai line-height 1,55 dan gap paragraf 16 px. Harga, transaksi dan unlock tidak diubah.
- **Mode/PIN/Ruang Guru:** deskripsi mode diringkas satu istilah; label PIN menjadi 14 px dengan gap 9 px, margin kelompok 20 px. Form guru memakai label 13 px dan input 16 px; keterangan statistik 12 px. Bantuan pemulihan PIN yang bersifat teknis sengaja dipertahankan.
- **HUD/soal/pause:** audit render mempertahankan hierarki HUD kompak, posisi dock, ikon, ukuran angka dan semua perilaku kontrol. Label form pengaturan/pause mengikuti gap 9 px. Teks soal panjang boleh membungkus; teks kontrol diperjelas tanpa mengubah nilai pilihan.
- **Podium/hasil:** line-height judul/konteks dan paragraf hasil dirapikan; teks panjang boleh membungkus. Geometri podium, nama/peringkat aktual, perhitungan hasil dan aksi tetap sama. Gaya cetak tetap tersedia.
- **Splash:** poster, loading minimum tiga detik, fullscreen startup, caption dan tombol masuk sudah sesuai; dipertahankan. Tidak ada timer atau progres pemuatan baru.

Ukuran kecil pada label HUD tertentu tetap dipertahankan karena merupakan informasi sekunder pada dock compact yang sudah diuji. Patch ini tidak memaksakan pembesaran global yang dapat menutupi lintasan.

## Pengujian dan batas interpretasi

`ui-results.json` mencatat pengukuran browser asli pada 1920×1080, 1366×768, 390×844, 844×390, 320×568, 768×1024 dan 1024×768. Before–after lengkap memakai viewport yang sama pada desktop 1366×768 dan HP 390×844: identitas, kesulitan, mode, arena/cuaca, garasi, podium, hasil, mode pengguna, PIN, Ruang Guru, HUD, pause dan soal. Viewport lain memuat screenshot tiap keputusan wizard, Grand Prix dan pengaturan lanjutan.

Pemeriksaan meliputi gap label/input dan kelompok, font/padding, bounding rect/footer, overflow horizontal, scroll lokal, teks terpotong, dan perubahan posisi setelah layout stabil. `maxSettledShift` adalah perbandingan rect selama 120 ms pada tahap yang sama; bukan klaim Core Web Vitals/CLS untuk seluruh permainan. Perubahan tinggi dialog saat berpindah tahap merupakan perubahan yang disengaja. Scroll lokal pada cup, arena, bantuan, guru atau laporan tetap diizinkan untuk aksesibilitas.

Alur Bebas dan Grand Prix diuji dengan Lanjut/Kembali, perubahan mode, lompat pemilihan arena untuk GP, dan pemulihan pilihan arena/cuaca serta identitas dari garasi. Jumlah soal guru tetap read-only. Pemeriksaan regresi mencakup fullscreen native/fallback, PIN, ekspor privasi, analog+gas+drift, kuis/freeze, buff, podium, hasil akademik, replay dan game ekspor dalam konteks browser tanpa jaringan. Uji ekonomi PATCH 8F diulang; profil baru/lamanya, harga dan reward tetap sama.

Untuk screenshot podium/hasil, sesi tes desktop/HP dipercepat setelah mengerjakan satu soal menggunakan handler penyelesaian game yang asli. Ini bukti tampilan render, bukan klaim semua 13 arena diselesaikan manual. Tidak ada fixture, saldo atau unlock pengujian yang ditanam dalam HTML distribusi.

Tidak mengulang benchmark physics/AI seluruh arena karena seluruh script terkait identik. Tidak mengklaim pengujian HP fisik, Safari/iOS atau FPS. Navigasi `file://` diblokir kebijakan browser cloud; pengujian offline menggunakan konteks network-disabled dan pemenuhan dokumen lokal, termasuk HTML hasil ekspor guru.

## Hasil ukur rilis

- **261 pemeriksaan bernama lulus**, termasuk scope: 225 pemeriksaan UI/navigasi, 25 regresi fullscreen/game/ekspor, 7 kelompok ekonomi, 3 layout pembelian, dan 1 pemeriksaan scope.
- **110 screenshot** render asli; before–after desktop/HP dan viewport tambahan tersedia di `review.html`.
- HTML **25.011.586 byte**; pertambahan **4.342 byte** dari PATCH 8F (sekitar 0,0174%). Sedikit di atas sasaran 25 MB; tidak ada aset/font baru dan tidak ada fitur atau kualitas model yang dikurangi.
- 50 pengukuran tahap wizard: tidak ada overflow horizontal; gap label/input 9 px, gap kelompok 20 px dan input 16 px pada ketujuh viewport. Form identitas tidak memerlukan scroll isi pada viewport yang diuji.
- Audit teks aktif tidak menemukan clipping pada permukaan yang diperiksa. Perubahan rect setelah stabil: maksimum 0 px pada sampel 120 ms; ini bukan benchmark CLS/FPS.
- 56 payload script lain identik. Tidak merge/deployment atau perubahan `index.html` utama.

## Rebuild

```sh
python visual-upgrade/patch8g/source/assemble.py
node visual-upgrade/patch8g/source/test_ui.cjs
node visual-upgrade/patch8g/source/test_flow.cjs
node visual-upgrade/patch8g/source/test_economy.cjs
node visual-upgrade/patch8g/source/test_purchase_ui.cjs
python visual-upgrade/patch8g/source/test_scope.py
python visual-upgrade/patch8g/source/package.py
```

Playwright dan Chromium harus tersedia seperti pada runner pengujian. `onboarding.js` adalah sumber wizard aktif yang dapat diedit; `typography.css` berisi semua aturan tambahan; `assemble.py` memuat daftar perubahan markup/microcopy. Builder memverifikasi SHA baseline. `scope-results.json` memverifikasi script lain identik dan logika onboarding sama setelah perubahan presentasi dibalik.
