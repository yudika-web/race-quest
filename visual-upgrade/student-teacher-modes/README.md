# BlokRaya — Mode Siswa, Mode Guru dan fullscreen loading

Baseline terverifikasi: `b98f40e7714b1d43d96020fc917f3575d1571494`, branch `dev/race-quest-cat-sport-visual-upgrade`.

- [HTML playable mandiri](../blokraya-mode-siswa-guru.html)
- [ZIP playable](../../blokraya-mode-siswa-guru-playable.zip): ekstrak, lalu buka HTML.
- [ZIP review: sumber, screenshot dan laporan](../../blokraya-mode-siswa-guru-review.zip)

## Alur

**Buka game → poster + “Memuat...” minimal 3 detik → fade 400 ms → Pilih Mode Pengguna.** Mode Siswa membuka persiapan balapan asli tanpa PIN. Mode Guru membuka pembuatan atau verifikasi PIN, lalu Ruang Guru asli. Kembali ke pilihan mode dapat dilakukan melalui tombol **Ganti Mode Pengguna** pada menu utama. Guru memiliki **Ganti PIN** dan **Keluar Mode Guru** pada header Ruang Guru.

## Loading dan poster fullscreen

Poster dalam lampiran `BlokRaya_Poster_WebP.zip` identik byte demi byte dengan sumber branding sebelumnya. Nama berkas ZIP adalah `BlokRaya_Landscape.webp` dan `BlokRaya_Portrait.webp`; keduanya memenuhi peran poster 16:9/9:16 yang diminta. File asli dan salinan optimal tetap tersedia di `../blokraya-branding/assets/`. Patch ini memakai payload poster yang sudah tertanam tanpa membuat ulang atau menyematkan salinan tambahan.

`<picture>` mengikuti orientasi. Elemen gambar fixed/full viewport menggunakan `object-fit:cover`, bukan contain. Safe-area hanya menggeser panel indikator; gambar tetap menutupi semua sisi. Pada rasio berbeda, tepi memang dipotong secara proporsional. Titik fokus portrait tinggi digeser agar tulisan BlokRaya dan wajah Kucing terbaca; landscape pendek memindahkan panel ke kiri bawah sehingga tidak melintangi wajah pengemudi utama. Pada rasio ekstrem sebagian kendaraan/landmark tepi dapat terpotong, tanpa stretching atau letterbox.

Durasi minimum memakai `performance.now()` setelah kesempatan paint awal dan Promise/setTimeout nonblocking. Readiness gambar/material tetap memakai tracker event load/error dari patch sebelumnya. Jika komponen belum siap setelah tiga detik, overlay tetap menunggu; tidak ada persentase download palsu. Ketika resource selesai tetapi minimum belum tercapai, indikator tetap indeterminate. Persiapan renderer dan lintasan mempertahankan jalur loading yang ada tanpa memberlakukan tiga detik untuk navigasi menu biasa.

Pemilihan mode dan permukaan game dibuat inert sampai overlay/fade selesai. Tidak ada menu interaktif sebelum loading berakhir. Reduced Motion atau Reduced Effects menghapus fade, tetapi durasi minimum tetap berlaku. Poster gagal memakai gradient bermerek sebagai fallback full viewport; tidak menampilkan ruang hitam/putih atau menunggu tanpa akhir. Error startup kritis tetap menyediakan tombol Muat ulang.

## PIN Guru lokal

| Aspek | Implementasi |
|---|---|
| PIN | Numerik 6–32 digit, konfirmasi saat pembuatan/perubahan; tidak ada PIN bawaan. |
| Verifier | PBKDF2 SHA-256, **600.000 iterasi**, output 256 bit. |
| Salt | 128 bit acak dari `crypto.getRandomValues`, baru untuk setiap pembuatan/perubahan. |
| Penyimpanan | Hanya versi/KDF/iterasi/salt/verifier pada `blokraya_teacher_pin_v1`. PIN asli tidak disimpan. |
| Sesi | Autentikasi berada di memori; reload tidak mempertahankan sesi Guru. |
| Percobaan | Lima kegagalan menghasilkan cooldown 30 detik; kelompok berikutnya 60/120/240 hingga maksimum 300 detik. Pembatasan berlaku dalam sesi aplikasi. |
| Tanpa Web Crypto | Akses Guru ditolak dengan pesan jelas, tanpa fallback plaintext. Mode Siswa tetap tersedia. |
| Tanpa storage/verifier rusak | Gagal tertutup dengan pesan, tanpa membuat PIN sementara atau menghapus data. |
| Ganti PIN | Memerlukan sesi Guru dan PIN lama yang benar; salt diganti. |
| Logout | Mengunci sesi, membersihkan formulir/konten guru, kembali ke pilihan mode. |
| Perubahan antartab | Perubahan kunci PIN mencabut sesi Guru; balapan siswa tidak dihentikan. |

Pemeriksaan dilakukan pada capture navigasi, dispatch aksi guru, fungsi layar/render/pengelolaan guru, form bank/soal/pengaturan dan impor file. Impor mengecek ulang autentikasi sebelum mutasi setelah proses asynchronous; konfirmasi penghapusan juga mengecek sesi. Ekspor guru memerlukan autentikasi, menghapus state/input PIN dari clone dan tidak menyalin verifier/salt atau sesi. Browser/origin lain menyiapkan PIN-nya sendiri.

**Batas keamanan:** PIN adalah pembatas akses antarmuka lokal, bukan enkripsi bank soal atau perlindungan kuat terhadap pemilik HTML/devtools/storage. Sesi/cooldown dapat direset dengan membuka ulang aplikasi; tidak ada klaim perlindungan server. Penyiapan pertama pada perangkat bersama sebaiknya dilakukan oleh guru/pemilik perangkat.

## Lupa PIN dan pemulihan

Tidak ada master PIN atau PIN rahasia. Pemilik perangkat dapat membuka alat pengembang browser → penyimpanan lokal untuk origin game → menghapus **hanya** `blokraya_teacher_pin_v1`, lalu reload dan membuat PIN baru. Ini menghapus pembatas lokal, bukan data belajar. Pada perangkat sekolah, libatkan administrator/pemilik perangkat. Jangan memilih hapus seluruh data situs karena bank soal, progres, hasil dan ghost dapat ikut terhapus. Penjelasan yang sama tersedia pada formulir PIN.

## Data dan gameplay lama

Seluruh kunci `race_quest_flexible_v1_*`, `race_quest_audio_v1`, `race_quest_preferences` dan `race_quest_hud_v45` dipertahankan. Tidak ada migrasi/reset profil atau pemberian token/unlock. Verifier disimpan terpisah. Format bank/impor/ekspor, skor akademik, tiga ID stage dan 14 pembalap tidak diubah.

Renderer/model, AI Smart Racing, buff/inventori, HUD, suara/VFX dan shader langit tidak diubah. Hanya loading, UI mode dan pemeriksaan akses di sekitar handler guru yang ditambahkan. Tidak membangun ulang model atau arena dan tidak mengulangi benchmark engine penuh.

## Screenshot renderer/UI sebenarnya

| Kondisi | Screenshot |
|---|---|
| Loading desktop | [1920×1080](screenshots/loading-1920x1080.png), [1366×768](screenshots/loading-1366x768.png) |
| Loading HP | [390×844 portrait](screenshots/loading-390x844.png), [844×390 landscape](screenshots/loading-844x390.png) |
| Loading tablet | [768×1024](screenshots/loading-768x1024.png), [1024×768](screenshots/loading-1024x768.png) |
| Pilih mode | [desktop](screenshots/modes-1366x768.png), [HP portrait](screenshots/modes-390x844.png), [HP landscape](screenshots/modes-844x390.png) |
| Buat PIN | [desktop](screenshots/pin-create-desktop.png), [HP](screenshots/pin-create-phone.png) |
| Login PIN | [desktop](screenshots/pin-login-desktop.png), [HP](screenshots/pin-login-phone.png) |
| Guru dan cooldown | [akses guru](screenshots/teacher-authorized.png), [pembatasan percobaan](screenshots/pin-cooldown.png) |
| Fallback dan kuis | [poster gagal](screenshots/poster-fallback.png), [kuis siswa](screenshots/student-quiz.png) |

Screenshot tidak menahan atau memalsukan durasi loading. Fallback memakai fixture sumber gambar rusak hanya di browser pengujian. Data QA dibuat di konteks browser terisolasi, bukan di HTML distribusi. Tidak ada PIN pribadi yang dicantumkan pada screenshot/laporan.

## Hasil pengujian terarah

- [visual-tests.json](visual-tests.json): enam viewport di atas, sumber poster yang benar, bounding rectangle gambar tepat memenuhi viewport, `cover`, tanpa overflow, target mode ≥44 px, durasi minimum dan fade. Terukur sekitar **3,07–3,09 detik sebelum fade**, kemudian **400 ms fade**. Mode tetap inert selama fade. Resource tertahan sungguhan membuat loading menunggu melewati tiga detik; Reduced Motion menghilangkan transisi.
- [auth-tests.json](auth-tests.json): **43 pemeriksaan**, termasuk siswa tanpa PIN, data lama tetap identik saat boot, navigasi/form/file guru ditolak saat tidak autentik, konfirmasi PIN, verifier, benar/salah, ganti PIN lama/baru, logout, reload, cooldown, perubahan antartab, Web Crypto hilang, storage gagal dan verifier rusak. Ketiga kondisi gagal tetap mengizinkan siswa.
- [offline-game-tests.json](offline-game-tests.json): **26 pemeriksaan**, pembuatan/verifikasi PIN sepenuhnya offline, pengaturan guru dan ekspor; verifier/salt tidak masuk ekspor, aset/poster/thumbnail dipertahankan dan poster tidak diduplikasi. Siswa memulai balapan asli, mengemudi, Pause, menjawab kuis dengan simulasi beku, memperoleh/memakai buff dan menyimpan skor 100 melalui kunci lama. Ekspor membuka pilihan mode dan meminta PIN baru pada konteks browser baru; siswa tetap bisa bermain offline. Tidak ada HTTP/CDN aset baru dan error JavaScript/WebGL.
- [fallback-tests.json](fallback-tests.json): poster gagal menampilkan fallback bermerek fullscreen, loading tetap selesai, tanpa error JavaScript.
- [scope-tests.json](scope-tests.json): membalik 28 perubahan terbatas menghasilkan baseline persis; **23 payload script lama** tetap identik, termasuk gameplay, renderer, AI, buff, HUD, stage, audio dan sky. **1.998 berkas historis**, termasuk `index.html` dan seluruh aset, tetap identik.

HP/tablet diuji melalui emulasi Chromium, bukan perangkat fisik. Tidak mengklaim FPS atau benchmark perangkat. `file://` diblokir administrator browser cloud; offline diuji dengan jaringan dimatikan dan byte HTML lokal disuplai langsung pada origin localhost yang mendukung Web Crypto. Pada browser/konteks tanpa Web Crypto, Guru ditolak secara eksplisit. Penyimpanan lama dapat dibaca bila browser/profil/origin tetap sama, sebagaimana baseline.

HTML **24.425.951 byte**, naik **23.212 byte** dari baseline, di bawah 25.000.000 byte. Tidak ada gambar/model/audio baru, CDN, backend atau program GPU tambahan. Sumber poster yang diterima tetap dipakai. Ukuran/hash HTML, ekspor dan ZIP tersedia di [release-metrics.json](release-metrics.json).

## Build ulang

`source/assemble.py` membaca HTML branding terbaru sebagai baseline, mempertahankan data poster dan menyisipkan `modes.html`, `modes.css`, `modes.js`, serta revisi `loading.js`. `bounded-changes.json` mencatat setiap hook. Sumber engine tidak diduplikasi dalam folder patch ini.

```sh
python visual-upgrade/student-teacher-modes/source/assemble.py
python visual-upgrade/student-teacher-modes/source/verify_scope.py
python -m http.server 8000
```

Dengan server port 8000 berjalan, jalankan masing-masing `source/test_visual.cjs`, `test_auth.cjs`, `test_offline_game.cjs` dan `test_fallback.cjs` melalui Node. Playwright/Chromium memakai lingkungan yang sama dengan patch sebelumnya. `source/package.py` memeriksa laporan, membuat ZIP playable/review, memeriksa CRC dan memastikan byte HTML sama.

Tidak merge ke main, tidak mengganti website/index.html online, tidak deployment, tidak Prompt 5 atau arena baru.
