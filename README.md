# RACE QUEST PRO — PATCH 4.5: Responsive Racing HUD

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
