# PATCH 4.5 — Responsive Racing HUD

Baseline PATCH 4 terverifikasi: `82c0f778b480d669b236b76517add5cd86e35fb2`, pada branch `dev/race-quest-cat-sport-visual-upgrade`. Distribusi: [HTML mandiri](../race-quest-pro-patch4-5.html). Buka HTML hasil ekstraksi [ZIP playable](../../race-quest-pro-patch4-5-playable.zip). Tidak mengubah `index.html`, merge, atau deployment.

## Audit dan hasil perubahan

HUD lama menggabungkan aturan posisi absolut dari stylesheet dasar, PATCH 3 dan PATCH 4. Inventori besar menempati tengah bawah, petunjuk keyboard panjang permanen, kontrol sentuh tetap mengisi desktop, sedangkan pesan AI, pesan balapan dan status jump mempunyai area terpisah. Perubahan ini mengganti markup area balapan serta dua stylesheet HUD tambahan; engine tetap dipertahankan.

| Kelompok | Tata letak baru |
|---|---|
| Posisi, putaran, waktu | Satu kartu kiri atas dengan waktu berjalan, lap/PB dan stage singkat; mode GP tetap menampilkan nomor putaran stage. |
| Soal | Kartu tengah atas dengan nomor soal dan progress menuju pos berikutnya/finis. Tidak mengubah jadwal atau hasil asesmen. |
| Toolbar | Empat tombol ikon seragam: Suara, Restart, Fullscreen, Pause. Restart memakai konfirmasi asli dengan simulasi dijeda; R tetap mengembalikan kart ke lintasan. |
| Inventori | Dua slot kecil di kiri bawah, charge, siap/aktif/cooldown, tanda pilihan dan PAKAI/E. Deskripsi lengkap di tooltip/Pause. Tidak ada perubahan aturan buff. |
| Kecepatan/token | Kartu kecil tengah bawah, maksimal dua status ringkas; deskripsi status lengkap melalui title/aksesibilitas. |
| Minimap/radar | Satu rail kanan; dapat dibuka/ditutup. Landscape pendek mulai ringkas; rail dapat scroll bila radar dan peta dibuka bersamaan. Peta tidak dihapus. |
| Kontrol | Desktop keyboard/mouse menyembunyikan tombol sentuh tanpa menyisakan ruang kosong. HP memakai arah kiri, gas/rem/drift/jump kanan. Semua tombol balapan minimal 44×44 CSS px. |
| Notifikasi | Satu area atas, maksimal tiga pesan dalam antrean. Ancaman masuk mendapat prioritas, disusul benturan, buff pemain dan penggunaan AI. Deduplikasi dan masa berlaku mengikuti clock simulasi. |
| Bantuan | Petunjuk keyboard lengkap dan deskripsi kedua slot dipindahkan ke Pause. |

Kontrol Sentuh memiliki pilihan **Otomatis / Selalu tampilkan / Sembunyikan** di Suara dan Pause, disimpan pada `race_quest_hud_v45`, terpisah dari data siswa. Mode otomatis membaca pointer utama lalu mengikuti input aktual. Pergantian ke sentuh diselesaikan pada click agar tombol tidak bergeser sebelum tap terproses. Pergantian mode melepaskan input lama untuk mencegah kemudi/gas tersangkut. Laptop layar sentuh dapat memakai pilihan manual.

CSS menggunakan grid untuk bagian atas, flex/grid di dalam kartu, safe-area dan visualViewport untuk tinggi yang tersedia. Di portrait sempit, panel soal berpindah ke baris kedua; inventori diangkat di atas arah. Di 320 px inventori disusun vertikal. Landscape tinggi ≤500 px memakai HUD compact, dan landscape sangat kecil juga menyusun inventori vertikal. Reduced Motion/Reduced Effects menonaktifkan transisi HUD. Tidak menambah animasi dunia, model, tekstur, audio, atau loop render.

## Screenshot asli dan perbandingan

Semua gambar berasal dari Chromium yang menjalankan HTML game sebenarnya. Before–after menggunakan kamera, pose, waktu simulasi, pencahayaan, kecepatan dan kualitas grafis rendah yang setara. Fixture hanya mengatur kondisi pengujian di memori browser; tidak memberikan token/unlock atau mengubah data distribusi. Gambar perbandingan hanya menyandingkan screenshot asli.

- Desktop [1821×831](screenshots/comparison-1821x831.jpg) / [1366×768](screenshots/comparison-1366x768.jpg).
- HP [portrait 390×844](screenshots/comparison-390x844.jpg) / [landscape 844×390](screenshots/comparison-844x390.jpg).
- Inventori [satu slot](screenshots/after-1821x831-one.png), [dua slot](screenshots/after-1821x831-two.png), [aktif/cooldown](screenshots/after-1821x831-active.png).
- [Ancaman AI](screenshots/after-844x390-attack.png), [di udara](screenshots/after-390x844-air.png), [peta diperluas landscape](screenshots/after-844x390-map-expanded.png).
- Interaksi nyata: [jump](screenshots/live-desktop-air.png), [cooldown](screenshots/live-desktop-cooldown.png), [Pause](screenshots/live-desktop-pause.png), [soal](screenshots/live-desktop-quiz.png).
- HP: [Pause portrait](screenshots/pause-390x844.png), [soal portrait](screenshots/quiz-390x844.png), [inventori penuh landscape](screenshots/quiz-overflow-844x390.png).

## Validasi

Lihat [laporan rinci](VALIDATION.md), [metrik distribusi](release-metrics.json) dan JSON pengujian di folder ini. Pengujian utama mencakup bounding rectangle aktif, klik/tap dan keyboard, ekspor guru/offline, penilaian/progres, serta simulasi dan render berpasangan dengan PATCH 4. Pengujian bukan hanya pemeriksaan error JavaScript.

## Sumber dan build ulang

Edit `source/race.html`, `source/hud.css`, `source/hud.js`, lalu jalankan dari root repositori:

```sh
python visual-upgrade/patch4-5-responsive-hud/source/assemble.py
python visual-upgrade/patch4-5-responsive-hud/source/verify_scope.py
python -m http.server 8000
```

Builder membaca **race-quest-pro-patch4.html**, bukan PATCH 3. `bounded-changes.json` mencatat sembilan penggantian terbatas untuk membuktikan baseline dapat direkonstruksi persis. Sumber engine tidak diduplikasi dalam folder patch ini.

Browser tests memakai Chromium `/usr/bin/chromium` dan Playwright yang tersedia pada `/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright`. Jalankan setiap `source/test_*.cjs`; beberapa tes memerlukan server port 8000. `capture_before.cjs` dan `capture_dialogs.cjs` membuat bukti tambahan. Sesudah seluruh laporan lulus, jalankan `python visual-upgrade/patch4-5-responsive-hud/source/package.py` untuk membuat perbandingan dan ZIP dengan pemeriksaan CRC serta hash HTML.

Keterbatasan: HP/tablet, orientasi dan notch diuji melalui emulasi browser cloud, bukan perangkat fisik. Tidak mengklaim FPS perangkat nyata. Browser cloud memblokir `file://`; offline diuji dengan jaringan dimatikan dan byte HTML lokal disuplai langsung. Grand Prix diuji pada engine, bukan seluruh putaran dimainkan manual. Fixture screenshot bukan bukti frekuensi serangan AI; perilaku AI dipastikan melalui tes engine dan kesamaan kode PATCH 4.
