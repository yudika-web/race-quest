# BlokRaya — PATCH 5: Ten-stage architecture & Grand Prix Nusantara

Baseline: `07af6fb0a7dfab5cb9f77d8ba32ab0cefc69ce99` pada `dev/race-quest-cat-sport-visual-upgrade`. HEAD lokal dan remote diverifikasi sebelum perubahan. Distribusi baru: [`../blokraya-patch5.html`](../blokraya-patch5.html). Versi lama, `index.html`, seluruh model dan world historis tetap utuh. Tidak merge, deployment, atau pembuatan lingkungan Prompt 6.

## Yang tersedia

| Urutan | Daerah | ID tersimpan | Status |
|---|---|---|---|
| 1 | Pontianak — City Road | `kampung` | Playable; world asli |
| 2 | Mempawah — Garden Road | `kapuas` | Playable; world asli |
| 3 | Singkawang — Coastal Festival | `hutan` | Playable; world asli |
| 4 | Sambas — Royal River Road | `sambas` | Segera Hadir |
| 5 | Sintang — Kelam Mountain Run | `sintang` | Segera Hadir |
| 6 | Kapuas Hulu — Sentarum Lake Circuit | `kapuas_hulu` | Segera Hadir |
| 7 | Bengkayang — Waterfall Adventure | `bengkayang` | Segera Hadir |
| 8 | Yogyakarta — Heritage Night Race | `yogyakarta` | Segera Hadir |
| 9 | Bali — Rice Terrace Rush | `bali` | Segera Hadir |
| 10 | Bromo — Volcano Challenge | `bromo` | Segera Hadir |

**`kapuas` tetap Mempawah**, bukan Kapuas Hulu. Tujuh arena mendatang tidak memiliki trackConfig/world builder, cuaca atau tingkat kesulitan fiktif. Placeholder CSS bertuliskan “Segera Hadir” tidak menggunakan render arena lama. Kartu membedakan status tersedia, terkunci oleh progres, dan belum dibangun. Tidak ada kunci progres baru pada tiga arena lama.

Katalog sepuluh kartu memakai grid bergulir, filter Kalimantan Barat/Nusantara, ringkasan pilihan, preview asli untuk arena aktif, tantangan dari konfigurasi lintasan aktual, dan progres dari hasil tersimpan. Membuka filter tidak mengganti arena yang dipilih. Ruang Guru tetap mengelola stage dan turnamen; pilihan yang belum tersedia dinonaktifkan.

## Struktur dan build ulang

- [`stages.json`](stages.json): metadata tampilan, referensi track/builder, urutan, status, syarat unlock, dan grup turnamen. Data lintasan/mesh tetap pada engine baseline.
- [`cups.json`](cups.json): ID dan urutan arena per turnamen. **Kalbar Klasik** memakai tiga ID lama; **Nusantara** memuat sepuluh ID.
- [`source/registry.js`](source/registry.js): registrasi world aktual, pemeriksaan ketersediaan, syarat progres opsional, serta normalisasi progres. `available: true` saja tidak cukup; konfigurasi lintasan dan adapter nyata wajib terdaftar. Pengamanan berjalan pada UI, penyimpanan pengaturan, Session/Track dan dispatch renderer.
- [`source/grand-prix.js`](source/grand-prix.js): urutan dan perhitungan poin dinamis. `GrandPrixSequence` murni mengelola ronde/asesmen; `GrandPrix` game wajib lolos pemeriksaan ketersediaan semua world.
- [`source/stage-ui.js`](source/stage-ui.js), [`source/ui.css`](source/ui.css), [`source/gp-panel.js`](source/gp-panel.js): picker, pengaturan guru, label HUD jumlah ronde dinamis, klasemen dan rekap per ronde.
- [`source/assemble.py`](source/assemble.py): menerapkan perubahan terbatas pada HTML baseline, tanpa menggandakan mesin ke sumber baru. [`bounded-changes.json`](bounded-changes.json) merekam setiap penggantian agar dapat dibalik dan dibandingkan tepat dengan baseline.

Dari root repository:

```sh
python visual-upgrade/patch5-ten-stages/source/assemble.py
node visual-upgrade/patch5-ten-stages/source/test_units.cjs
python visual-upgrade/patch5-ten-stages/source/verify_scope.py
```

Tes browser menggunakan Playwright pada path runtime cloud yang tercantum di sumber, Chromium `/usr/bin/chromium`, dan server statis root repository pada port 8000. Sesuaikan path runtime Playwright bila dijalankan pada perangkat lain. Dependensi pengembangan tersebut tidak diperlukan saat memainkan HTML.

```sh
node visual-upgrade/patch5-ten-stages/source/test_ui.cjs
node visual-upgrade/patch5-ten-stages/source/test_gp_browser.cjs
node visual-upgrade/patch5-ten-stages/source/test_offline_export.cjs
node visual-upgrade/patch5-ten-stages/source/test_render_parity.cjs
node visual-upgrade/patch5-ten-stages/source/capture_baseline.cjs
python visual-upgrade/patch5-ten-stages/source/package.py
```

Jalankan tes browser berat secara berurutan atau maksimal dua proses bersamaan. File `harness.cjs` memakai stub adapter hanya untuk unit test logika; bukan bukti world baru sudah dibuat dan tidak masuk HTML distribusi.

## Grand Prix dan pembelajaran

Kalbar Klasik tetap Pontianak → Mempawah → Singkawang. Semua label/transisi/penyelesaian memakai `totalRounds` dan urutan cup, bukan indeks akhir `2`. Poin tetap **25 / 18 / 15 / 12 / 10**, tie-break tetap kemenangan lalu ID pembalap. Ambang ketuntasan mengikuti bank soal guru, tanpa perubahan persentase. Posisi dan buff tidak mengubah skor akademik.

Skor di bawah ambang menahan ronde selanjutnya. Ulangi ronde mengembalikan poin percobaan gagal sebelum hasil baru dicatat. Hasil menyimpan ID cup, urutan, jumlah ronde, rekap posisi/skor tiap ronde, klasemen dan juara akhir. Nusantara belum dapat dijalankan, termasuk jika pemilihan dipaksakan melalui formulir. Mesin sepuluh ronde diuji sebagai urutan metadata, bukan sepuluh balapan dunia nyata.

Alur GP aktif tetap berada dalam sesi aplikasi sebagaimana baseline; memuat ulang halaman tidak melanjutkan balapan aktif secara otomatis. Hasil tiap ronde dan progres arena disimpan, termasuk percobaan yang belum tuntas.

## Kompatibilitas dan privasi

Kunci penyimpanan lama tetap: data paket/profil/bank/hasil/ghost, audio, preferensi dan HUD, serta PIN lokal. Tidak ada backend atau autentikasi baru. `gpId` ditambahkan pada pengaturan bank; mode GP lama otomatis memakai Kalbar Klasik. ID arena lama dan format ghost key identik.

`stageProgress` ditambahkan dalam objek data yang sama. Saat data lama belum memilikinya, ringkasan dihitung dari riwayat hasil yang masih tersimpan, tanpa mengganti skor asli. Riwayat lama dibatasi 50 hasil oleh baseline: riwayat yang sudah terbuang tidak dapat direkonstruksi. Setelah migrasi, ringkasan jumlah balapan, kemenangan, skor terbaik dan waktu terbaik tetap bertahan walau daftar riwayat dipangkas.

Mode Siswa tidak memakai PIN; pengelolaan guru tetap membutuhkan PIN lokal. Ekspor HTML/bank tidak memuat PIN, salt, atau verifier perangkat asal. Verifier tetap PBKDF2-SHA256 baseline. Poster fullscreen, minimum loading 3 detik, AI, sembilan buff, dua slot inventori, audio/VFX, langit, karakter dan kontrol dipertahankan.

## Bukti pengujian

| Laporan | Hasil terukur |
|---|---|
| [`unit-tests.json`](unit-tests.json) | 10 kelompok pengujian: metadata, ketersediaan, blokir arena/cup, beda terkunci/belum dibuat, GP lama vs baru, 10 ronde simulasi metadata, panjang/urutan variabel, input invalid, migrasi dan progres. |
| [`ui-tests.json`](ui-tests.json) | 55 pemeriksaan pada 1366×768, 390×844, 844×390, 768×1024: 10 kartu/7 dinonaktifkan, pilihan konsisten, filter, batas formulir, touch target, tidak overflow horizontal atau overlap gambar/teks kartu. |
| [`grand-prix-browser-tests.json`](grand-prix-browser-tests.json) | 37 pemeriksaan game sebenarnya: tiga world, empat AI, pause/kuis membeku, hadiah benar vs salah, penggunaan buff, GP gagal/ulang/lanjut/juara, ekspor hasil, progres/ghost, reload/PIN dan ekspor bank. |
| [`offline-export-tests.json`](offline-export-tests.json) | 28 pemeriksaan jaringan dinonaktifkan: PIN, ekspor guru, aset tertanam, dua slot, kontrol, quiz/buff, start balapan dari HTML ekspor, 10 metadata/3 world, tanpa permintaan aset HTTP/CDN. |
| [`unchanged-renders.json`](unchanged-renders.json) | 19 render: 14 pasangan, Cat low, kendaraan Cat saja, dan tiga world lama. Piksel identik pada pose/waktu/kamera tetap 256×256 sebelum–sesudah. |
| [`scope-tests.json`](scope-tests.json) | Assembly dapat dibalik tepat ke baseline; 2.009 file historis dan 17 payload script/aset terlindungi identik. HUD hanya mengganti label jumlah ronde GP. |

Balapan browser memakai UI/renderer nyata dengan fixture pengujian yang memindahkan kendaraan ke gerbang soal/finis agar transisi dapat diuji terarah. Tidak diklaim sebagai seluruh balapan dimainkan manual. Data demonstrasi hanya ada di konteks browser tes; tidak disisipkan sebagai profil/unlock/token pada distribusi.

Tidak ada error JavaScript/WebGL dalam alur yang diuji. Ini bukan benchmark FPS HP fisik. Offline diuji dengan konteks Chromium `offline: true` dan dokumen lokal dipenuhi oleh harness pada origin localhost untuk Web Crypto; tidak memakai server autentikasi maupun jaringan aset. Harness cloud menolak navigasi `file://`, sehingga pengujian buka langsung file dan HP fisik belum dilakukan pada lingkungan ini.

Screenshot asli: [desktop](screenshots/stages-1366x768.png), [HP portrait](screenshots/stages-390x844.png), [HP landscape](screenshots/stages-844x390.png), [tablet](screenshots/stages-768x1024.png), [arena mendatang](screenshots/coming-1366x768.png), [Nusantara diblokir](screenshots/nusantara-blocked.png), [GP gagal ketuntasan](screenshots/grand-prix-blocked.png), [GP selesai](screenshots/grand-prix-complete.png). Screenshot baseline disimpan dengan awalan `baseline-`; bukan mockup.

## Ukuran dan distribusi selanjutnya

HTML baseline **24.425.951 byte**; PATCH 5 **24.445.403 byte**. Pertumbuhan **19.452 byte** (sekitar 0,080%); sisa batas 25.000.000 byte **554.597 byte**. Tidak ada model, tekstur, atau environment besar baru. Tidak ada draw call/segitiga balapan tambahan; perbandingan render world identik. Waktu/frame dan memori perangkat nyata belum diukur.

**A — Saat ini:** satu HTML mandiri dengan semua aset tertanam, dipaketkan dalam ZIP playable. ZIP review memuat HTML yang sama, metadata, sumber patch, screenshot dan laporan. CRC dan kesamaan byte HTML pada kedua ZIP diperiksa oleh `package.py`; metrik final ada di [`release-metrics.json`](release-metrics.json).

**B — Rencana Prompt 6, belum diimplementasikan:** bila tujuh arena nyata tidak muat, pertahankan versi standalone selama efisien, lalu sediakan ZIP offline berisi HTML dan paket aset JavaScript lokal (`window.BlokRayaAssetPacks`) yang dapat didaftarkan renderer sebelum loading selesai. Hindari `fetch()` GLB lokal karena pembatasan `file://`; jangan menduplikasi aset bersama. Uji ekstraksi/buka `file://` pada browser desktop/Android target, resource cleanup, perpindahan stage dan ekspor guru sebelum menyatakan format tersebut didukung. Tidak ada CDN atau server wajib yang ditambahkan pada patch ini. Sisa sekitar 0,55 MB tidak menjamin tujuh environment mendatang dapat ditanamkan tanpa optimasi tambahan.
