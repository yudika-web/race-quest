# BlokRaya PRO — PATCH 8D

Fullscreen dari klik Mulai Balapan, kemudi analog proporsional dan perbaikan viewport. Baseline HEAD PATCH 8C `18fce7045518dc7f4b8569ce3010a73f267056d2`, penerus PATCH 8B. Podium yang sudah ada dipertahankan tanpa perubahan.

- [HTML playable mandiri](../blokraya-patch8d-controls.html)
- [ZIP playable](../../blokraya-patch8d-playable.zip) · [ZIP review](../../blokraya-patch8d-review.zip)
- [Galeri before–after, fullscreen, wizard dan HP](review.html)
- [Metrik terukur](metrics.json) · [Metrik paket](release-metrics.json)

## Implementasi

`source/assemble.py` memverifikasi SHA-256 HTML PATCH 8C, menambah adapter viewport/input dan CSS terpisah, serta mengubah hook aplikasi minimum. Seluruh renderer, model, environment, physics, AI, buff, PIN, registry, onboarding PATCH 8B dan podium PATCH 8C tetap memakai sumber sebelumnya.

- **Fullscreen:** helper tunggal dipakai klik Mulai Balapan dan tombol HUD manual. Permintaan native dilakukan sinkron dalam user activation, sebelum await/loading world. Tidak meminta fullscreen pada boot, pergantian menu, GP-next atau retry otomatis. Penolakan, exception dan API yang tidak tersedia tidak menghambat balapan. Tidak memakai klik sintetis/timer untuk meminta fullscreen dan tidak mengunci orientasi/navigasi browser.
- **Viewport:** `visualViewport` height/width/offset, `100dvh` fallback, safe area dan perubahan orientasi/fullscreen memperbarui layout. Canvas race mengikuti ruang yang tersedia; paused renderer mendapat satu redraw ketika viewport berubah. Footer wizard/kuis dibatasi dalam layar; konten panjang dapat digulir lokal. Garasi portrait kecil kembali menjadi satu kolom, preview tetap terlihat dan pager karakter tetap dapat dicapai. Home/hasil memakai scroll konten lokal; aturan cetak hasil tetap terlindungi.
- **Analog:** CSS tanpa aset gambar. Base 94–116 CSS px, deadzone horizontal 10%, nilai kontinu `-1..+1`. Input ditambahkan pada adapter `Session.advance` yang sudah menerima analog, dengan clamp asli. Keyboard, gamepad, tilt dan rumus physics tidak diganti. Knob mengikuti pointer capture hingga jari keluar base; lepaskan untuk netral. Tidak ada loop animasi baru.
- **Multitouch:** pointer joystick terpisah dari set pointer setiap pedal/aksi. Buff dan pemilihan slot memakai handler game asli melalui tap adapter, termasuk jari nonprimer; klik native susulan dideduplikasi agar satu tap tidak memakai dua charge. Melepas analog tidak melepaskan gas yang masih ditahan jari lain.
- **Keamanan input:** netral saat up/cancel/lost-capture, blur, visibility hidden, resize/orientasi/fullscreen, pause, soal, finish dan pindah menu. Pelepasan sentuhan yang dibatalkan tidak boleh menjadi klik tembus pada tombol kuis/menu. Koleksi pointer dibatasi dan dibersihkan. `touch-action:none` hanya pada canvas/kontrol race terkait; UI persiapan tetap dapat digulir/di-zoom.
- **Preferensi:** tambah `steering: analog|buttons` pada `race_quest_hud_v45`; analog default. `touch: auto|show|hide`, minimap dan field preferensi lama/tidak dikenal dipertahankan. Desktop menyembunyikan kontrol sentuh secara otomatis; laptop sentuh tetap bisa memilih Selalu Tampilkan.
- **HUD:** inventori di atas kemudi kiri, gas/rem/drift/jump kanan bawah, kecepatan/token bawah tengah, map kanan dengan expand/collapse dan scroll lokal. Tidak mengubah dua slot, charge/cooldown, aturan hadiah atau notifikasi Smart AI.

## Bukti pengujian

359 pemeriksaan bernama dalam 11 laporan, ditambah assertion geometri footer wizard dari helper. Semua lulus pada artifact yang SHA-nya tercatat dalam `metrics.json`.

| Laporan | Bukti aktual |
|---|---|
| [Responsive](responsive-tests.json) | 7 viewport: 1920×1080, 1366×768, 768×1024, 1024×768, 390×844, 844×390, 320×568. Footer tiap tahap wizard/garasi/kuis, bounding rectangle HUD, nol overlap antardok, canvas, native fullscreen masuk/keluar melalui HUD pada semua viewport. |
| [Input](input-tests.json) | Pusat, sedikit/penuh kiri/kanan, kontinuitas ke `Session.advance`, capture di luar base, native cancel, 2/3 jari analog+gas+drift/jump, analog+buff+slot kedua, satu charge per tap, pelepasan terpisah, pause/kuis/freeze, anti klik tembus, resize, blur, klasik, A/D, show/hide, finish/menu. Memakai native CDP touch contacts, bukan hanya dispatch boolean tombol. |
| [Fullscreen](fullscreen-tests.json) | Native Chromium pada desktop dan emulasi touch; user activation dan urutan request sebelum world build dicatat. Exit manual memperbarui canvas/aria. API unavailable/rejected adalah fixture eksplisit; game tetap berjalan. |
| [Viewport pendek/PIN](short-viewport-tests.json) | Fixture visualViewport tinggi 300 px + offset 70 px, footer lokal; PIN create, salah/benar, logout pada landscape 844×390. |
| [Input lintas arena](stage-controls-tests.json) | Pontianak, Mempawah dan Kayong Utara di posisi tikungan; analog diterima engine asli, AI/clock bergerak, release netral, tanpa error GL. Ketapang dipakai pengujian multitouch/soal/buff/finish. Posisi dekat tikungan memakai fixture, bukan klaim balapan manual penuh. |
| [Navigasi](navigation-tests.json) | Alur Bebas/GP PATCH 8B, 13 arena, empat cup, stage/weather/AI/laps/autogas, kembali, pagination 14 karakter, validasi cup unavailable, double-start hanya membangun satu world. |
| [Offline](offline-tests.json) | Konteks browser jaringan dimatikan; buat PIN, Ruang Guru/ekspor, siswa/kuis/buff/pause, finish/podium asli/hasil akademik, ekspor dimainkan kembali. Nol request HTTP aset/CDN; favicon browser dipisahkan. |
| [Kompatibilitas](compatibility-tests.json) | Bank soal, profil/token/unlock/progres/PIN lama identik; preferensi HUD lama/field tambahan tetap ada; reload mengunci Guru; ekspor membersihkan identitas/PIN dan dapat dibuka lagi. |
| [Render parity](render-parity-tests.json) | 13 world dan 14 model terlindungi menghasilkan piksel identik dibanding PATCH 8C, termasuk setelah berpindah dari podium. Tidak ada error JavaScript/WebGL. |
| [Scope](scope-tests.json) | 53 payload script lama identik byte demi byte. Hanya aplikasi dan adapter HUD lama berubah; module viewport baru. Semua CSS/aset lama dipertahankan, `index.html` dan artifact terdahulu tidak diubah. |
| [Release](release-smoke.json) | Navigasi HTTP biasa menyajikan SHA HTML yang sama, loader → mode → wizard. File lokal dicoba tetapi diblokir kebijakan administrator browser cloud. |

Screenshot before–after memakai viewport, identitas, kamera/pose dan kualitas rendah yang setara. Simulasi dihentikan sesaat agar komposisi HUD konsisten; tidak ada manipulasi gambar/generatif. Screenshot interaksi lain berasal dari sesi dan fixture yang dijelaskan di atas. Pada layar sempit/pendek, scroll lokal tetap diperbolehkan agar isi tidak dipotong. FPS perangkat fisik tidak diklaim.

## Ukuran dan rendering

- HTML baseline: **24.985.707 byte**.
- HTML baru: **25.003.020 byte**; tambahan **17.313 byte**, sekitar **0,0693%**.
- Melebihi sasaran lunak 25 MB sebesar **3.020 byte**. Tidak ada model, fitur, landmark atau kualitas yang dihapus untuk mengejar angka tersebut.
- Tidak ada GLB, tekstur, lampu, shadow map maupun geometri 3D baru. Aset lama identik; joystick adalah DOM/CSS kecil. Biaya komposit UI/FPS hardware tidak dibenchmark; tidak ada klaim FPS HP.
- Ukuran ekspor Guru dan arsip ZIP aktual ada pada `metrics.json` / `release-metrics.json`; ekspor dapat lebih besar karena bank/pengaturan/markup saat ekspor.

## Browser dan keterbatasan

Native fullscreen terbukti pada Chromium cloud desktop dan emulasi mobile. Ini bukan bukti Chrome Android fisik atau Safari iOS. Browser yang menolak/tidak menyediakan API mendapat layout viewport responsif; CSS tidak dapat menyembunyikan toolbar sistem iOS. Keyboard virtual/notch fisik belum diuji, hanya kontrak visualViewport dan safe-area CSS. Tidak mengharuskan PWA.

`file://` ditolak `ERR_BLOCKED_BY_ADMINISTRATOR` dalam browser cloud, sehingga tidak diklaim lulus di konteks itu. Offline diuji dengan network-disabled context, dokumen lokal yang dipenuhi harness, semua aset tertanam, dan ekspor yang dijalankan ulang; HTTP lokal biasa juga diuji. Tidak ada backend/CDN baru.

Tidak mengulang benchmark seluruh engine atau seluruh GP secara manual. Aturan GP/physics/AI/penilaian/PIN dan podium identik; regresi yang dijalankan fokus pada permukaan input, navigasi, freeze, hasil/ekspor serta render terlindungi.

## Build ulang

Jalankan dari root repository:

```sh
python visual-upgrade/patch8d/source/assemble.py
python visual-upgrade/patch8d/source/test_scope.py
node visual-upgrade/patch8d/source/test_input.cjs
node visual-upgrade/patch8d/source/test_responsive.cjs
python visual-upgrade/patch8d/source/package.py
```

Assembler memerlukan baseline `visual-upgrade/blokraya-patch8c-podium.html` identik (disertakan ZIP review). Test memerlukan Node, Playwright dan Chromium; `PLAYWRIGHT_MODULE` dapat menunjuk modul Playwright. Jalankan server lokal root repository pada port 8000 untuk release smoke. Browser test lain memenuhi dokumen lokal melalui harness. Semua sumber UI yang diubah tersimpan di `source/`; tidak perlu Blender atau membangun ulang GLB.

Tidak merge, tidak deployment, tidak mengganti `index.html` online, tidak menambah podium baru.
