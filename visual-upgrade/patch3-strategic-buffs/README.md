# PATCH 3 — Strategic Buff System

Baseline: PATCH 2 `c786d88aca6876e7913012f3490fd2f6660898c8`, pada branch `dev/race-quest-cat-sport-visual-upgrade`. Distribusi: [HTML mandiri](../race-quest-pro-patch3.html). Tidak mengganti `index.html`, merge atau deployment.

## Aturan dan audit

Lima ID lama, ikon, durasi dan mekanik proyektil dipertahankan. Sebelumnya inventori hanya satu slot: jawaban benar menimpa item lama, tanpa cooldown item. PATCH 3 menyimpan dua slot, dengan satu slot dipilih. Ketuk slot pada HP, atau Q / 1 / 2; E / Spasi / tombol PAKAI menggunakan slot terpilih. Charge tersisa, status siap/cooldown dan timer aktif terlihat pada HUD.

**Inventori penuh:** hadiah baru menunggu di panel jawaban; pilih Ganti slot 1, Ganti slot 2, atau Lewati hadiah baru sebelum lanjut. Kedua item lama utuh sampai pilihan dibuat. Hadiah tertunda tidak dapat dipakai sebagai slot ketiga. Jawaban salah tidak menawarkan hadiah, tidak menimpa slot dan tidak mengisi charge. Semua sembilan hadiah mempunyai peluang sama pada pengambilan hadiah jawaban benar, memakai satu pengambilan RNG seperti sebelumnya.

| ID | Buff | Durasi / charge | Cooldown per jenis | Target dan batas |
|---|---|---|---|---|
| turbo | Turbo | 4 dtk / 1 | 6 dtk | Pemain; batas kecepatan 31 m/s |
| shield | Perisai | Maks. 8 dtk / 1 benturan | 10 dtk | Perlindungan lama, habis setelah menahan satu benturan/serangan |
| magnet | Magnet | 7 dtk / 1 | 9 dtk | Radius pengambilan token lama: 4 m longitudinal, 8 m lateral |
| bubble | Gelembung | Proyektil 4 dtk; efek 2,4 dtk / 1 | 3 dtk | Menembak lurus, bukan pemilik; batas kecepatan target 3 m/s |
| oil | Oli Licin | Genangan 10 dtk; efek 2,8 dtk / 1 | 4 dtk | Diletakkan di belakang, bukan pemilik; batas kecepatan target 8 m/s |
| reflect | Perisai Pantul | Maks. 6 dtk / 1 serangan | 10 dtk | Menangkis gelembung/oli sekali; pantulan 0,9 dtk hanya ke AI penyerang sah dalam 40 m, di tanah, belum finis dan tidak kebal |
| nitro | Nitro Ganda | 2 × 1 dtk, diaktifkan terpisah | 1,6 dtk antar-charge | Batas 31 m/s yang sama dengan Turbo; tidak menambah kecepatan secara langsung |
| grip | Ban Anti-Selip | 5 dtk / 1 | 7 dtk | Oli dibatasi 0,7 dtk; kecepatan saat oli maks. 14 m/s; goyangan dikurangi 70%; faktor kemudi hujan 0,94 dari 0,78 |
| radar | Radar Lintasan | 6 dtk / 1 | 9 dtk | Maks. 5 batu/batang, celah, oli lawan, gelembung dan pos soal dalam 45 m; tidak membaca isi/kunci soal |

Cooldown global **0,6 dtk** berlaku setelah setiap penggunaan. Cooldown per jenis tetap berlaku jika kemudian memperoleh hadiah sama; item yang masih cooldown tetap tersimpan. Semua waktu adalah **waktu simulasi**, berhenti pada pause, soal, feedback dan countdown untuk melanjutkan.

## Prioritas dan keseimbangan

- Turbo dan Nitro tidak bisa diaktifkan ketika salah satunya masih aktif. Durasi tidak dijumlahkan dan kecepatan tidak melebihi 31 m/s; bonus teknik lama (start/drift/landing/combo benar) tetap bekerja, dengan batas yang sama. Batas jalan luar tetap berlaku.
- Perisai biasa dan Pantul tidak bisa diaktifkan bersamaan. Pantul menangani serangan item; benturan jalan biasa tetap memakai mekanik collision lama. Penyerang tidak diketahui/jauh/di udara/kebal/sudah finis: blok saja, tanpa pantulan. Tidak membuat proyektil balik atau rantai pantulan.
- Setelah serangan item diterima atau ditangkis, target kebal serangan item berikutnya **1,1 dtk**. Batas collision jalan yang lama tetap berlaku. AI tidak memperoleh strategi/item baru; hanya dapat terkena respons defensif pemain dan kekebalan singkat yang sama. Santai tetap kebal serangan AI seperti baseline.
- Gelembung didahulukan daripada efek traksi: Ban Anti-Selip tidak membebaskan gelembung. Grip mengurangi oli, bukan menghapus semua penalti. Tidak melindungi benturan jalan. Radar hanya informasi balapan.
- Maksimal dua item tersimpan (Nitro maksimal dua charge per hadiah), satu reward pending saat quiz; maksimal delapan proyektil dan delapan genangan seperti baseline. Magnet/Grip/Radar aktif tidak bisa ditumpuk/diperpanjang lewat penggunaan item sama.
- Nilai asesmen = jawaban benar / jumlah soal × 100. Buff, rank dan token tidak masuk skor akademik. XP/token profil balapan tetap mengikuti rumus lama. Bonus teknik lama tidak menambah inventori.

## Penyimpanan dan kompatibilitas

Bank, profil, progres, ghost dan hasil belajar memakai format/storage lama. Hasil menambahkan metadata opsional `strategy` dan `rewardAction`; tidak mengubah jawaban/nilai. Inventori, cooldown dan charge adalah **milik balapan berjalan**, tidak disimpan sebagai persediaan lintas balapan. Baseline tidak menyediakan save/resume balapan di tengah jalan; reload memulai menu/race baru tanpa inventori lama. Pause/resume mempertahankan semua slot/charge/timer. Tidak ada profil demo atau unlock gratis pada HTML distribusi.

## Visual/audio

Empat SVG orisinal ringan, cincin Pantul ungu, cincin Grip hijau, trail Nitro amber dan panel radar. Nitro memakai sample Turbo lama dengan pitch/level berbeda; Pantul memakai cue perisai, Grip/Radar memakai sintesis yang sudah tersedia. Tidak menambah file audio atau loop baru. Pool partikel, limiter suara, mute, Reduced Effects dan audio quiz PATCH 2 tetap dipakai. Cincin memanfaatkan mesh yang ada (320 segitiga/satu draw per efek aktif, dihitung dari mesh ring 32 × 5 × 2), radar/slot berupa DOM; tidak membuat GLB, tekstur besar, buffer atau pool GPU baru.

## Sumber dan build

Dari root repository:

```sh
python visual-upgrade/patch3-strategic-buffs/source/icons.py
python visual-upgrade/patch3-strategic-buffs/source/assemble.py
node visual-upgrade/patch3-strategic-buffs/source/test_buffs.cjs
node visual-upgrade/patch3-strategic-buffs/source/test_core.cjs
python visual-upgrade/patch3-strategic-buffs/source/verify_scope.py
```

Builder membaca HTML PATCH 2, menerapkan penggantian terbatas yang dicatat dalam `bounded-changes.json`, lalu menambah lapisan buff/UI. AI, engine scenery, GLB, avatar dan data stage tidak disalin ke sumber baru. `verify_scope.py` membalik seluruh hook hingga identik dengan baseline dan memeriksa hash berkas historis. Browser suite memerlukan server lokal root repository pada port 8000, Chromium `/usr/bin/chromium`, dan Playwright pada path cloud yang dicatat dalam script. Jalankan `test_game.cjs`, `test_ui.cjs`, `test_stages.cjs`, `test_persistence.cjs`, `test_export.cjs`, `test_unchanged_render.cjs`, serta `capture_compare.cjs`; `package.py` menolak rilis jika laporan wajib belum lolos.

## Bukti pengujian dan keterbatasan

Lihat laporan JSON di folder ini: pengujian sembilan buff, 81 pasangan berurutan, overflow/charge/cooldown/target, pause/quiz, finish tanpa item di tiga stage, kesamaan AI seluruh stage/difficulty, penilaian akademik, CSV/JSON, Grand Prix, ghost, keyboard/sentuh, save/reload hasil aktual, ekspor guru dan offline. Screenshot berasal dari UI/renderer game sebenarnya. Fixture browser mengatur posisi/slot untuk mencapai keadaan tertentu; tidak disisipkan ke distribusi. Perbandingan HUD memakai kamera/pose/waktu tetap. Pengujian model membandingkan pixel 14 pasangan lama pada pose/cahaya tetap (ditambah low Kucing dan kendaraan saja).

Offline cloud diuji dengan jaringan browser dimatikan dan HTML lokal dipenuhi langsung sebagai dokumen utama; tidak ada permintaan aset jaringan. Akses `file://` diblokir administrator browser cloud, sehingga unduhan ekstrak-buka pada perangkat pengguna belum diuji langsung. Tidak mengklaim FPS/HP fisik, speaker fisik, semua Grand Prix manual atau pengukuran memori perangkat nyata. Inventori belum memiliki penyimpanan mid-race karena baseline juga tidak memilikinya.
