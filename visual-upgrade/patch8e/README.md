# BlokRaya PRO — PATCH 8E

Fullscreen dipindahkan dari tombol Mulai Balapan ke interaksi asli pertama pada poster/tombol **Masuk BlokRaya**. Ini patch startup saja, berbasis HEAD PATCH 8D `c34fe8b1da86ca561f5ff49419a88e401185fe28`.

- [HTML playable](../blokraya-patch8e-startup.html) · [ZIP playable](../../blokraya-patch8e-playable.zip) · [ZIP review](../../blokraya-patch8e-review.zip)
- [Galeri screenshot asli](review.html) · [Metrik](metrics.json) · [Metrik arsip](release-metrics.json)

## Perubahan minimum

1. Tiga fungsi fullscreen PATCH 8D dipindahkan **tanpa mengubah isinya** ke script kecil di head. Helper siap sebelum poster/CTA maupun aset engine selesai diparse. Adapter viewport/HUD memanggil helper yang sama melalui alias; tidak ada duplikasi implementasi Fullscreen API.
2. Satu tombol keyboard-accessible ditambahkan pada overlay poster lama. Klik/tap asli pada poster atau tombol memanggil helper langsung, sebelum penyelesaian Promise entry. Klik sintetis diabaikan; interaksi hanya diterima sekali pada pembukaan awal.
3. `bootReady` lama menunggu kesiapan gambar/data, sisa minimum tiga detik sejak paint awal, dan interaksi masuk. Tidak ada timer tiga detik kedua. Jika sudah siap dan pengguna belum mengetuk, poster tetap menampilkan Siap dan tombol masuk. Fade 400 ms dan reduced motion lama dipertahankan.
4. Permintaan fullscreen otomatis di case Mulai Balapan dihapus. Keluar fullscreen tidak menyebabkan menu/garasi/race berikutnya memaksa masuk lagi. Tombol manual HUD tetap memakai helper PATCH 8D.
5. Ekspor Guru mereset tombol entry agar HTML hasil ekspor kembali mulai dari poster. PIN/verifier perangkat asal tetap tidak diekspor.

Poster landscape/portrait, `object-fit:cover`, object-position, fallback gambar, `100dvh`, visualViewport dan safe area lama dipertahankan. Tidak membuat ulang poster, mode, wizard, loading overlay, steering atau podium. Pada rasio layar berbeda, cover memotong tepi sewajarnya tanpa menarik proporsi gambar atau membuat letterbox.

## Perlindungan kode

[Scope test](scope-tests.json) membuktikan 53 payload script lama identik byte demi byte, termasuk engine, physics, AI, buff, 13 arena, model, audio/VFX, PIN, onboarding dan podium. Semua CSS lama identik; hanya style tombol masuk ditambahkan. Setelah posisi tiga helper fullscreen dikembalikan untuk perbandingan, **seluruh kode analog/deadzone/multitouch/viewport PATCH 8D identik**. Aplikasi berubah satu case untuk menghapus request saat Mulai Balapan. Normalisasi perubahan startup merekonstruksi seluruh HTML baseline secara tepat.

`index.html`, seluruh distribusi sebelumnya dan sumber PATCH 8B/8C/8D tidak diubah. Tidak merge/deployment, tidak PWA/service worker, tidak arena/fitur lain.

## Pengujian terarah

116 pemeriksaan bernama lulus dalam lima laporan, ditambah assertion bounding rectangle untuk footer wizard, garasi, kuis, pause dan podium.

| Laporan | Bukti aktual |
|---|---|
| [Startup](startup-tests.json) | Lima kombinasi: desktop 1366×768 native, portrait 390×844 native, landscape 844×390 native, portrait rejected, landscape unsupported. Poster cover tanpa sisi kosong, orientasi aset, tombol dalam viewport, keyboard/poster/button asli, synthetic-click ditolak, waktu minimum, entry terlambat tanpa timer kedua, mode → wizard → garasi → race tanpa request tambahan, GL tanpa error. Fixture decode lambat membuktikan tidak ada progres selesai palsu atau poster hilang sebelum resource siap. |
| [Early entry](early-entry-tests.json) | HTTP streaming menghentikan parser sebelum `initialData`/aset/engine. Ketukan nyata sudah berhasil meminta native fullscreen sebelum `RaceCore` atau adapter input tersedia. Setelah parser dilanjutkan, interaksi diingat dan mode muncul tanpa permintaan ulang. |
| [Flow/offline](flow-tests.json) | PIN Guru → pengaturan → ekspor → logout → Siswa → empat langkah wizard → garasi → Ketapang → analog+gas+drift → kuis/freeze → buff → pause → keluar fullscreen → manual re-entry → podium asli → laporan skor asli → replay non-fullscreen. Ekspor Guru dibuka pada context jaringan dimatikan tanpa Fullscreen API dan bisa memulai balapan. Tidak ada request HTTP aset/CDN atau error JS/WebGL. |
| [Scope](scope-tests.json) | Helper asli dipindah verbatim; tidak ada perubahan analog, model, AI, physics, scoring, PIN, podium atau markup lain. Tidak mengubah artifact/index lama. |
| [Release](release-smoke.json) | Server HTTP biasa menyajikan SHA HTML yang benar; entry mencapai mode tanpa interception dokumen. Navigasi file:// dicoba dan ditolak kebijakan browser cloud. |

Waktu observasi dari first-contentful-paint sampai mode sekitar **3,40–3,48 detik**, termasuk fade. Pada klik setelah status Siap, mode muncul sekitar **485 ms** kemudian. Detail timestamp dan user activation tercatat di JSON; tidak memakai progres palsu atau klik sintetis untuk meminta fullscreen.

## Ukuran dan keterbatasan

- Baseline: **25.003.218 byte**.
- HTML PATCH 8E: **25.005.151 byte**, tambahan **1.933 byte** (sekitar **0,0077%**).
- Melebihi target lunak 25 MB sebesar 5.151 byte. Tidak ada aset/model/tekstur/geometri baru; tidak mengurangi kualitas atau fitur.
- Ukuran ekspor Guru dan kedua ZIP diukur dalam `metrics.json` / `release-metrics.json`.
- Chromium cloud/SwiftShader dan emulasi HP, bukan Android/iOS fisik atau Safari. Fullscreen tidak dapat dijamin pada browser yang tidak mendukung; CSS tidak menyembunyikan toolbar sistem.
- Dalam headless, Escape mencapai handler pause aplikasi, sehingga keluar native diuji dengan `exitFullscreen()` serta re-entry melalui tombol HUD nyata. Tidak mengklaim pengujian tombol Esc browser fisik.
- Fixture gerbang/finish mempercepat uji alur podium/hasil; bukan balapan manual penuh. Physics 13 arena tidak dibenchmark ulang karena identik dan di luar cakupan patch.
- `file://` diblokir `ERR_BLOCKED_BY_ADMINISTRATOR`. Offline diuji melalui context tanpa jaringan, dokumen lokal yang dipenuhi harness, seluruh aset tertanam, dan ekspor yang dimainkan kembali. HTTP biasa juga diuji; tidak menambah server wajib.
- Tidak mengklaim FPS perangkat nyata atau benchmark GPU baru.

## Sumber dan build

```sh
python visual-upgrade/patch8e/source/assemble.py
python visual-upgrade/patch8e/source/test_scope.py
node visual-upgrade/patch8e/source/test_startup.cjs
node visual-upgrade/patch8e/source/test_early_entry.cjs
node visual-upgrade/patch8e/source/test_flow.cjs
node visual-upgrade/patch8e/source/test_release.cjs
python visual-upgrade/patch8e/source/package.py
```

Assembler memverifikasi SHA-256 baseline `visual-upgrade/blokraya-patch8d-controls.html` dan memerlukan file tersebut (disertakan ZIP review). `source/fullscreen.js`, `loading.js`, `startup.css` dan `assemble.py` adalah sumber perubahan yang dapat diedit. Test memerlukan Node, Playwright (`PLAYWRIGHT_MODULE` dapat menunjuk instalasi lain), Chromium dan server root repo pada port 8000 untuk release smoke. Scope test memakai Git repository. Tidak memerlukan Blender atau membangun ulang model.
