# BlokRaya PRO — Finalisasi 13 arena dan onboarding siswa

Baseline: `1b3f9454a780af9f7a53ecebb1a6e599f052cb32` (Stage 13 / 6J), pada branch `dev/race-quest-cat-sport-visual-upgrade`.

Distribusi: [HTML mandiri](../blokraya-pro-final.html), [ZIP playable](../../blokraya-pro-final-playable.zip), [ZIP review](../../blokraya-pro-final-review.zip).

## Perubahan

- Persiapan siswa berurutan: **Nama dan Kelas → Arena dan Cuaca → Pengaturan Balapan → Pilih Karakter → Mulai Game**. Nama dan kelas wajib diisi; tombol kembali mempertahankan isian. Kartu 13 arena, pilihan cuaca, empat turnamen, jumlah soal dari guru dan pilihan balapan yang ada digunakan kembali.
- Hasil belajar memakai kelas yang dimasukkan siswa. `studentClass` menyimpan kelas siswa dan `bankClassName` mempertahankan kelas bank; `className` pada laporan/CSV mengikuti kelas siswa. Hasil lama tetap dibaca tanpa migrasi/destruksi. Bank soal tidak diubah oleh isian siswa.
- Ekspor guru mengembalikan formulir siswa ke bentuk awal, membersihkan identitas pada ringkasan garasi serta kartu avatar runtime yang dapat dibentuk kembali. Ini menghindari identitas siswa dan salinan thumbnail yang tidak diperlukan di paket ekspor.
- Label aksesibilitas katalog dan catatan kesiapan turnamen diperbarui dari sepuluh arena menjadi tiga belas arena / empat turnamen.
- Tidak ada perubahan pada world, mesh/model, track, physics, collision, rescue, AI, buff, aturan akademik, kunci penyimpanan, PIN Guru atau loader. Semua payload script terkait identik dengan 6J. `index.html` utama tetap identik.

## Validasi aktual

| Uji | Hasil dan metode |
|---|---|
| Seluruh 13 arena | **84 balapan mesin penuh**, start hingga finish dengan lima jawaban nyata dan skor 80%; 10 arena pertama pada tiga kesulitan, tiga arena ekstrem pada tiga kesulitan × enam seed. Driver referensi mengirim gas/steer/rem; tidak memindahkan posisi ke finish. |
| AI | **336 aktor AI** menyelesaikan rute tersebut; pilihan karakter AI mencakup seluruh 14 jenis. Kelanjutan AI setelah pemain finish menggunakan mesin AI aktual, tanpa warp maju. |
| Semua kendaraan di arena ekstrem | **42 balapan tiga putaran**: 14 kendaraan × Kubu Raya/Kayong Utara/Ketapang, tingkat kesulitan bergilir, lima jawaban dan skor 100%. Semua finish, tanpa rescue pemain pada driver uji. |
| AI tiga putaran | **36 AI** pada tiga arena × tiga kesulitan, semuanya finish; satu rescue AI Santai di Kayong Utara, kemudian melanjutkan hingga finish. |
| Tantangan ekstrem | Suite per-arena menguji zona/collider, obstacle bergerak dan peringatan, bridge, dua jalur, grip/traksi, gap, jump/landing, rescue mundur dan pembekuan clock. Gap diuji pada 9/12/23/31 m/s dengan impulse asli. Tidak mengklaim setiap pemain selalu lolos tanpa rescue. |
| Sembilan buff | 11 pengujian interaksi Smart AI/item **per arena ekstrem**: suplai terbatas, dua slot, target pemain/AI, telegraph, cooldown/charge Nitro, proteksi chain-hit, reflect/grip, magnet/radar, serta pause/kuis. |
| Grand Prix | **202 pemeriksaan browser** pada Kalbar Klasik (3), Nusantara (10), Kalbar Extreme (3), dan Lengkap 13. 29 ronde sukses + empat percobaan gagal ketuntasan/ulang. Setiap world benar-benar dimuat; posisi kuis/finish memakai fixture untuk uji transisi, bukan 29 balapan manual penuh. Rekap, juara, rollback poin retry, ekspor, progres dan ghost diperiksa. |
| Freeze render | Piksel obstacle, world, air, awan dan aktor berhenti pada pause/kuis di ketiga arena ekstrem; berubah ketika clock simulasi berubah. Uji UI turnamen juga memeriksa objek pemain/AI/clock saat panel kuis benar-benar terbuka. |
| Regresi visual | **13 perbandingan piksel identik** dengan 6J, kamera/seed/waktu tetap. Semua world, model dan aset lama tidak dibangun ulang. |
| Desktop / HP / tablet | Tiga langkah formulir diuji pada 1920×1080, 1366×768, 390×844, 844×390, 768×1024, 1024×768. Bounding rectangles memeriksa header/body/footer, tombol lanjut dan overflow horizontal. UI sampai balapan diuji desktop, HP portrait dan landscape. |
| Data / PIN | PIN salah ditolak, login/logout/reload teruji pada empat turnamen. Fixture data lama mempertahankan bank, kelas bank, jumlah soal, ketuntasan, token, XP, unlock dan progres; onboarding tidak memberikan unlock/token gratis. |
| Offline / ekspor | Browser dengan jaringan dinonaktifkan, dokumen lokal diintersep, **0 permintaan aset HTTP/CDN**. Ekspor dibuka di konteks baru dan dapat masuk ke balapan. Ekspor setelah wizard/garasi juga diuji: identitas kosong, tidak ada ID duplikat, PIN/salt/verifier tidak dibawa. |

Driver referensi memakai pengetahuan konfigurasi kurva untuk merencanakan pengereman, seperti pengujian jalur; ini **bukan perubahan kecerdasan AI**. Sebagian AI mengalami rescue sah selama uji campuran: 8 peristiwa pada 84 balapan, 12 pada 42 balapan tiga putaran, ditambah 1 pada suite AI tiga putaran. Semuanya pulih; bukan teleport maju atau melewati checkpoint. Tidak ada balapan referensi yang gagal finish.

## Status arena

Seluruhnya tersedia dan lulus uji penyelesaian; siap ditinjau pengguna. ID lama dipertahankan:

| No. | ID | Arena |
|---|---|---|
| 1 | kampung | Pontianak — City Road |
| 2 | kapuas | Mempawah — Garden Road |
| 3 | hutan | Singkawang — Coastal Festival |
| 4 | sambas | Sambas — Royal River Road |
| 5 | sintang | Sintang — Kelam Mountain Run |
| 6 | kapuas_hulu | Kapuas Hulu — Sentarum Lake Circuit |
| 7 | bengkayang | Bengkayang — Waterfall Adventure |
| 8 | yogyakarta | Yogyakarta — Heritage Night Race |
| 9 | bali | Bali — Rice Terrace Rush |
| 10 | bromo | Bromo — Volcano Challenge |
| 11 | kubu_raya | Kubu Raya — Mangrove Extreme Run |
| 12 | kayong_utara | Kayong Utara — Coastal Cliff Challenge |
| 13 | ketapang | Ketapang — Ale-Ale Chaos Circuit |

Status dan rentang waktu simulasi per arena: [stage-status.json](stage-status.json). Catatan uji lengkap: berkas `*-tests.json`, `*-mechanics.json`, `*-items.json`; angka distribusi: [metrics.json](metrics.json) dan [release-metrics.json](release-metrics.json).

## Screenshot asli

- Sebelum: [desktop](screenshots/before-setup-1366.png), [HP](screenshots/before-setup-390.png).
- Sesudah: [identitas desktop](screenshots/identity-1366.png), [identitas HP](screenshots/identity-390.png), [13 arena](screenshots/stages-1366.png), [pengaturan HP landscape](screenshots/settings-844.png).
- [Balapan desktop](screenshots/race-1366.png), [HP portrait](screenshots/race-390.png), [HP landscape](screenshots/race-844.png).
- Render arena ekstrem: [Kubu Raya](screenshots/extreme-kubu_raya-mobile.png), [Kayong Utara](screenshots/extreme-kayong_utara-mobile.png), [Ketapang](screenshots/extreme-ketapang-mobile.png). Ini kamera renderer game pada pose uji tetap, bukan ilustrasi.
- Rekap turnamen: [Extreme](screenshots/gp-kalbar-extreme-complete.png), [Lengkap 13](screenshots/gp-lengkap-13-complete.png).

## Ukuran dan keterbatasan

HTML **24.932.762 byte**, bertambah **5.656 byte** dari 6J, tetap di bawah 25 MB desimal. Tidak ada penambahan geometri, material, tekstur atau audio; draw call world tetap karena payload renderer/aset identik. Angka ZIP dan ekspor terukur ada di laporan rilis. Tidak ada klaim FPS, pengukuran HP fisik, benchmark GPU baru atau seluruh GP dimainkan manual.

Navigasi langsung `file://` diblokir administrator browser cloud (keterbatasan yang sudah dicatat pada 6J). Offline diuji dengan konteks jaringan mati dan dokumen lokal yang diintersep, bukan klaim direct-file sudah diuji. Pada perangkat pengguna, ekstrak ZIP dan buka HTML dengan browser modern; Web Crypto dan izin penyimpanan lokal diperlukan untuk PIN. Tidak ada backend/CDN. PIN lokal tetap merupakan pembatas UI, bukan proteksi terhadap pengubah HTML/storage.

## Build dan pengulangan uji

Pada checkout repository lengkap:

```sh
python visual-upgrade/finalization/source/assemble.py
node visual-upgrade/finalization/source/test_completion.cjs
node visual-upgrade/finalization/source/test_extreme_vehicles.cjs
node visual-upgrade/finalization/source/test_extreme.cjs
node visual-upgrade/finalization/source/test_unit.cjs
node visual-upgrade/finalization/source/test_onboarding.cjs
node visual-upgrade/finalization/source/test_layout.cjs
node visual-upgrade/finalization/source/test_gp_browser.cjs
node visual-upgrade/finalization/source/test_offline.cjs
node visual-upgrade/finalization/source/test_compatibility.cjs
node visual-upgrade/finalization/source/test_render.cjs
node visual-upgrade/finalization/source/test_extreme_render.cjs
node visual-upgrade/finalization/source/capture_before.cjs
python visual-upgrade/finalization/source/test_scope.py
node visual-upgrade/finalization/source/test_release.cjs
python visual-upgrade/finalization/source/package.py
```

Browser tests menggunakan Chromium/Playwright yang terpasang di cloud dan origin lokal `127.0.0.1:8000`; jalankan server statis root repository pada port itu. Jalankan paling banyak dua suite WebGL bersamaan. Unit test Node memakai engine asli yang diekstrak dari HTML; stub builder hanya untuk registrasi di VM, sedangkan tes browser memakai builder/world/renderer sebenarnya.

ZIP review memuat HTML final dan baseline 6J serta helper uji bersama yang diperlukan untuk assembler dan suite mekanik. Verifikasi scope memerlukan checkout Git lengkap. Source arena/model sebelumnya tetap di direktori tahap aslinya pada repository. Tidak merge ke main, tidak mengganti index.html, tidak deployment, dan tidak memulai tahap berikutnya.
