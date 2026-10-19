# RACE QUEST PRO — PATCH 1: Garasi & Pemilihan Stage

[HTML mandiri](../race-quest-pro-patch1.html) · [ZIP playable](../../race-quest-pro-patch1-playable.zip) · [ZIP review](../../race-quest-pro-patch1-review.zip)

Ekstrak ZIP playable, lalu buka `race-quest-pro-patch1.html` di browser dengan WebGL. Seluruh aset tertanam. Tidak memerlukan server, CDN atau unduhan aset ketika bermain. Pilih **Mulai → kartu arena → Lanjut ke Garasi → Mulai Balapan**. Pilihan arena juga tersedia pada footer garasi. Repository viewer GitHub bukan pemutar HTML: gunakan unduhan ZIP, bukan membuka pratinjau kode HTML.

Baseline: `eaf32f667699541def49b2559dc92f387a1a4b57`, file Singkawang Stage 3. Patch ini hanya memperbarui UI garasi dan pemilihan arena. Tidak menyentuh `index.html`, deployment, model GLB lama, avatar, jalan/collision, stage IDs, clock animasi, harga unlock, bank/profil awal, audio, buff atau AI.

## Perubahan yang terlihat

Garasi sekarang memiliki ruang bengkel 3D aktif: lantai ubin dan podium, bayangan kontak lama, panel dinding, rak 12 ban, meja/laci perkakas, pegboard, dua softbox studio, lampu plafon, banner RACE QUEST dan pajangan panel kendaraan. Geometri mengelilingi preview yang tetap dapat diputar; ini bukan gambar latar datar. Warna bengkel tidak mengikuti pilihan cat kendaraan. Kamera komposisi dibuat sedikit lebih dekat; framing close-up semua model tetap memakai aturan lama. Pergantian karakter menggunakan fade 210 ms dan menghormati preferensi reduced motion.

Desktop memberi ruang lebih besar untuk preview. HP menempatkan preview di atas daftar karakter, dengan footer pemilihan arena dan tombol mulai yang tetap terlihat. Daftar 14 pembalap, tiga halaman, harga/unlock, cat, ekspresi, mode close-up/full, drag, pinch/scroll, reset dan auto-rotate dipertahankan. Sidebar HP dapat digulir untuk melihat baris bawah dan navigasi halaman.

Dropdown stage pemain diganti tiga kartu bergambar dengan status pilihan, ringkasan besar, landmark, tantangan lintasan dan cuaca efektif. Tombol **Landmark / Di lintasan** mengganti preview dengan render game asli. Ruang Guru mempertahankan dropdown dan penyimpanan lama. Perubahan stage pemain berlaku pada konfigurasi balapan, tidak menulis ulang default bank guru. Saat kembali ke persiapan, pilihan pemain dipertahankan selama bank, mode dan default guru belum berubah; perubahan default guru kembali menjadi acuan. Grand Prix tetap dimulai di Pontianak, lalu Mempawah dan Singkawang.

## Bukti visual

Semua screenshot berasal dari Chromium/WebGL game asli. Before/after garasi menggunakan karakter Kucing, yaw `.52`, pitch `.318`, clock `1`, viewport dan pose sama. Perubahan jarak kamera komposisi sengaja terlihat karena merupakan bagian patch; close-up memakai framing lama.

- Garasi: [desktop](comparisons/comparison-garage-desktop.jpg), [HP](comparisons/comparison-garage-mobile.jpg).
- Close-up: [desktop](comparisons/comparison-closeup-desktop.jpg), [HP](comparisons/comparison-closeup-mobile.jpg).
- Menu persiapan: [desktop](comparisons/comparison-setup-desktop.jpg), [HP](comparisons/comparison-setup-mobile.jpg).
- Kartu arena di garasi: [desktop](after/stages-desktop.png), [HP](after/stages-mobile.png).
- Transisi balapan: [desktop](after/race-desktop.png), [HP](after/race-mobile.png).
- [Enam thumbnail render arena](comparisons/stage-render-thumbnails.jpg).

Master PNG dan WebP thumbnail tersedia di `assets/`; kamera, cuaca dan ukuran render dicatat pada `thumbnail-render-report.json`. Tidak menggunakan ilustrasi generatif.

## Metadata dan kapasitas menu

`source/stage-catalog.json` memisahkan nama/tema/landmark/thumbnail dari ID persisten. ID tetap `kampung`, `kapuas`, `hutan`. Hanya entri yang benar-benar ada pada `RaceCore.STAGES` yang diaktifkan, sehingga tidak ada arena kosong.

Tantangan dihitung dari data asli `STAGES` dan `Track`: Dasar bila tanpa celah; Menengah bila ada celah; Tinggi bila ada celah serta tinggi maksimum ≥7 m atau ≥4 rintangan. Kartu juga menampilkan cuaca efektif; ringkasan menyebut jumlah rintangan, ramp, celah dan tinggi maksimum lintasan. Ini indikator topologi lintasan, bukan perubahan tingkat AI atau atribut kendaraan. Tingkat AI tetap diatur melalui kontrol bawaan.

Grid desktop dapat membungkus dan digulir; HP memakai strip kartu horizontal. Kapasitas 10 diuji dengan duplikasi kartu **hanya pada DOM pengujian**, tanpa menambahkan metadata/ID/arena ke HTML distribusi. Penambahan stage kelak memerlukan stage nyata di core serta entri presentasi/thumbnail, bukan hanya kartu kosong.

## Ukuran dan biaya rendering

| Komponen | Terukur |
|---|---:|
| HTML baseline | 23.394.232 byte |
| HTML PATCH 1 | 23.613.758 byte |
| Pertumbuhan | 219.526 byte (~0,94%) |
| Anggaran 25 MB desimal | Terpenuhi |
| Ekspor guru pada skenario uji | 23.695.671 byte |
| Geometri bengkel | 5.588 segitiga |
| Submisi warna bengkel | 13 draw call/frame |
| Tekstur milik bengkel | 1 banner 1024×256, dipakai dua panel |

Angka bengkel adalah tambahan pada preview garasi, bukan beban lintasan. Model lama/LOD dan 94 aset tertanam tidak berubah. Thumbnail disimpan sekali dalam JSON terpisah; DOM runtime memakai referensi URI dan dibersihkan ketika ekspor guru agar tidak ikut menanam duplikasi gambar. `workshop.glb` / `.blend` adalah aset review yang diekspor dari geometri runtime; tidak disematkan lagi ke HTML. Ukuran per aset dan ZIP disimpan pada `asset-metrics.json` / `release-metrics.json`. Tidak mengukur atau mengklaim FPS HP fisik.

## Pengujian dan batas bukti

Laporan mesin tersimpan di JSON berikut; paket hanya dibuat bila semua laporan wajib berstatus `passed`.

- `scope-verification.json`: 1.453 file historis dan 94 aset embedded identik; membalik hanya sisipan UI terdokumentasi menghasilkan byte baseline persis. Core, renderer asli, scenery, model, avatar dan aturan gameplay utuh.
- `unchanged-renders.json`: render 14 pasangan, cat low, serta mobil Sport saja identik piksel pada pose/waktu/cahaya tetap.
- `scene-tests.json`: 27 frame identik piksel pada tiga arena × high/medium/low × tiga posisi; tidak ada error WebGL.
- `all-character-tests.json`: pemilihan 14 karakter melalui UI/pembelian 60 token asli, pemuatan high/low, ekspresi, close-up, penggunaan sebagai pemain, serta pause. Saldo 1.000 token adalah fixture browser saja, tidak ada pada distribusi.
- `stage-ui-tests.json`: ketiga kartu pada desktop/HP memuat ID race sebenarnya; sinkronisasi guru/pemain/cuaca/GP, preview, putar/zoom/reset/auto, dan kapasitas layout 10 kartu.
- `test-results.json`: bank soal, ekspor bank, A/D, jump/landing, kontrol sentuh, pause/soal membekukan pemain + AI + clock animasi, jawaban benar, penggunaan buff, resume, LOD.
- `core-test-results.json`: CSV round-trip, materi/jumlah soal/persistensi JSON, AI bertingkat, GP gating/retry/tiga putaran secara deterministik, drift/jump, soal/buff, hasil, ghost dan progres.
- `offline-test-results.json` dan `export-tests.json`: browser offline, HTML dari byte lokal, tanpa request aset HTTP, ekspor guru mempertahankan model/thumbnail dan stage pilihan tetap playable. Tidak ada error JavaScript.
- `preview-controls-tests.json`: pinch dua jari native, reset, reuse buffer/tekstur bengkel pada 14 preview, serta dispose 41 GPU buffer dan satu tekstur banner tanpa error.
- `capture-ui-report.json` / `thumbnail-render-report.json`: hasil tangkapan renderer game asli.

Pengujian dilakukan di Chromium cloud dengan software WebGL; HP adalah viewport/touch emulation 390×844, bukan HP fisik. Pembukaan `file://` langsung diblokir kebijakan browser cloud; bukti offline memakai context tanpa jaringan dengan main HTML dipenuhi dari byte lokal dan request aset lain ditolak. Grand Prix diuji secara deterministik di core, bukan seluruh turnamen manual. Tidak menguji semua browser/perangkat, sesi panjang kebocoran memori, atau FPS nyata. Bengkel berbagi satu set GPU buffer antar pergantian karakter dan menyediakan `dispose()` untuk resource miliknya; engine lama tetap menggunakan satu renderer selama aplikasi hidup.

## Sumber editable dan build ulang

Sumber utama ada di `source/workshop.js` (geometri/material bengkel), `ui.css`, `stage-ui.js`, `stage-catalog.json`, `app_hooks.py`, `assemble.py`. `app-ui-changes.json` mencatat empat hook UI yang dibatasi. Tidak ada salinan mesin permainan baru; assembler membaca HTML Stage 3 yang sudah ada.

```bash
# Dari root repository. Server hanya untuk build/test, bukan untuk memainkan hasil.
python -m http.server 8000 --bind 127.0.0.1
# Terminal lain: opsi regenerasi thumbnail dari baseline dan kamera historis.
node visual-upgrade/patch1-garage-stage/source/capture_stage_assets.cjs
python visual-upgrade/patch1-garage-stage/source/convert_thumbnails.py
# Build distribusi dari sumber dan aset tersimpan:
python visual-upgrade/patch1-garage-stage/source/assemble.py
python visual-upgrade/patch1-garage-stage/source/verify_scope.py
node visual-upgrade/patch1-garage-stage/source/export_workshop.cjs
blender --background --python visual-upgrade/patch1-garage-stage/source/build_workshop.py
node visual-upgrade/patch1-garage-stage/source/capture_ui.cjs
python visual-upgrade/patch1-garage-stage/source/make_comparisons.py
node visual-upgrade/patch1-garage-stage/source/test_core.cjs
node visual-upgrade/patch1-garage-stage/source/test_game.cjs
node visual-upgrade/patch1-garage-stage/source/test_all_characters.cjs
node visual-upgrade/patch1-garage-stage/source/test_stage_ui.cjs
node visual-upgrade/patch1-garage-stage/source/test_scene.cjs
node visual-upgrade/patch1-garage-stage/source/test_unchanged_render.cjs
node visual-upgrade/patch1-garage-stage/source/test_export.cjs
node visual-upgrade/patch1-garage-stage/source/test_preview_controls.cjs
python visual-upgrade/patch1-garage-stage/source/package.py
```

Playwright diakses dari runtime cloud pada path absolut yang tercatat di skrip; lingkungan lain perlu menyesuaikan path modul/executable Chromium. Thumbnail membutuhkan review camera JSON historis Stage 1–3 yang tetap ada di repository. Semua output playable bersifat mandiri; pipeline build saja yang memakai sumber historis tersebut.
