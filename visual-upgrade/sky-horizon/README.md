# Langit blocky dan horizon yang menyatu

Baseline: PATCH 4.5 `b5611f4937c6139024779265f0b8434545b77cbf`, branch `dev/race-quest-cat-sport-visual-upgrade`. Distribusi baru: [race-quest-pro-sky-horizon.html](../race-quest-pro-sky-horizon.html). [ZIP playable](../../race-quest-pro-sky-horizon-playable.zip): ekstrak lalu buka HTML pada browser modern dengan WebGL.

## Perubahan visual

Langit lama menggunakan panorama bitmap dan lapisan awan fotografis. Sambungan panorama tampak sebagai garis vertikal, sedangkan pertemuan langit dan air mempunyai pita warna datar yang berbeda dari warna fog geometri. Bagian jauh akhirnya terlihat seperti batas map.

Langit baru memakai **gradient berbasis arah pandang**, tanpa UV panorama atau tepi dome. Warna zenith bertransisi lembut ke warna horizon. Palet Pontianak sedikit hangat, Mempawah lebih sejuk dan Singkawang lebih segar. Opsi hujan/kabut tetap memakai cuaca lama; hanya warna atmosfer yang menyesuaikan. Tidak ada sistem cuaca baru.

**Awan blocky berbevel** dibangun dari geometri ringan, tiga balok per kelompok. Seluruh kelompok digabung menjadi satu vertex/index batch, dengan shading bagian atas dan bawah yang sederhana. Posisi mengikuti orientasi kamera seperti objek jauh di langit, tanpa translasi/parallax palsu dan tanpa animasi waktu nyata. Awan berada di atas horizon dan digambar sebelum dunia sehingga tidak menutupi jalan, kendaraan atau landmark di depannya. LOD rendah menyebarkan sepuluh kelompok ke seluruh azimuth, bukan memotong satu sisi langit.

**Horizon blending** memakai haze tambahan pada geometri jauh yang dekat arah horizon. Efek mulai pada jarak horizontal 65 m dan mencapai penuh pada 230 m; objek dekat tetap memakai shading lama. Warna fog disetarakan dengan warna gradient melalui konversi balik gamma/tone mapping renderer. Air dan daratan jauh menghilang secara lembut ke warna yang sama. Radius dunia, pantai, jalan, collider, kamera balapan dan landmark tidak diubah. Haze tidak menambah jarak pandang atau mengubah data yang diketahui AI.

## Screenshot render asli

Kamera, posisi, waktu simulasi, pencahayaan, kualitas high dan pose sama antara baseline dan revisi. Gambar bukan ilustrasi generatif. Komposit hanya menyandingkan dua screenshot asli.

| Stage | Perbandingan utama | Sudut tambahan sesudah |
|---|---|---|
| Pontianak | [Sebelum–sesudah](screenshots/comparison-pontianak.jpg) | [Tikungan](screenshots/after-kampung-turn.png), [area terbuka](screenshots/after-kampung-open.png), [kecepatan tinggi](screenshots/after-kampung-fast.png) |
| Mempawah | [Sebelum–sesudah](screenshots/comparison-mempawah.jpg) | [Tikungan](screenshots/after-kapuas-turn.png), [area terbuka](screenshots/after-kapuas-open.png), [kecepatan tinggi](screenshots/after-kapuas-fast.png) |
| Singkawang | [Sebelum–sesudah](screenshots/comparison-singkawang.jpg) | [Tikungan](screenshots/after-hutan-turn.png), [area terbuka](screenshots/after-hutan-open.png), [kecepatan tinggi](screenshots/after-hutan-fast.png) |

[HP portrait](screenshots/live-mobile-390x844.png) dan [landscape](screenshots/live-mobile-844x390.png) berasal dari game dengan HUD aktif. Folder screenshot juga menyimpan normal/turn/open/fast sebelum dan sesudah ketiga stage, kualitas low serta opsi rain/fog. Foto HP merupakan emulasi browser, bukan perangkat fisik.

## Ukuran dan biaya rendering

HTML **23.701.999 byte**, baseline **23.699.293 byte**, naik **2.706 byte** (0,0114%), di bawah 25.000.000 byte. Tidak ada aset gambar/audio/GLB baru, CDN, atau unduhan saat dimainkan. Aset panorama lama tetap ada dalam paket data untuk menjaga kompatibilitas arsip/ekspor; renderer tidak lagi mengunggah dua bitmap langit tersebut ke GPU.

| Metrik langit | High / auto | Low |
|---|---:|---:|
| Kelompok awan | 18 | 10 |
| Segitiga awan | 3.240 | 1.800 |
| Draw call langit total | 2 | 2 |
| Draw call tambahan terhadap baseline | 1 | 1 |
| Tekstur langit aktif | 0 | 0 |

Buffer awan dibangun sekali per instance renderer, **47.088 byte**, tidak dibangun ulang saat stage berganti. Gradient tetap memakai satu segitiga fullscreen; awan menambah dua buffer dan satu program shader. Angka tersebut adalah biaya geometri/buffer, bukan seluruh penggunaan VRAM. Shader gradient tidak melakukan texture sampling; cloud shader tidak memakai shadow map atau efek berat. Tidak ada loop animasi/RAF tambahan. Pengujian cloud bukan bukti FPS HP nyata; performa GPU pada perangkat fisik belum diukur.

## Pengujian

Lihat laporan JSON: [scope](scope-tests.json), [sky/WebGL](sky-tests.json), [capture](capture-tests.json), [kontrol](controls-tests.json), [simulasi berpasangan](engine-parity.json), [regresi core](core-test-results.json), [stage/audio](stage-audio-tests.json), [ekspor guru](export-tests.json), [offline](offline-test-results.json), [model](unchanged-renders.json).

- Screenshot dua versi ×3 stage ×4 sudut; tambahan low/rain/fog. Hasil ditinjau langsung untuk horizon, siluet awan, warna dan keterbacaan jalan.
- Uji shader: dua draw call per stage, translasi kamera tidak menggeser langit, kontinuitas pada arah sambungan panorama, pita horizon air tanpa lonjakan warna kasar, LOD menurunkan geometri.
- Pergerakan kamera: 120 sampel berurutan per stage pada state kecepatan 31 m/s, melewati tikungan; buffer awan tetap identik dan tidak ada error WebGL. Ini pengujian renderer dengan fixture, bukan klaim 360 frame gameplay fisik atau FPS.
- Render pause berulang identik; awan statis tidak mempunyai jam animasi terpisah. Kontrol asli, item, audio, Pause/kuis, jawaban benar/salah dan hasil/progres diuji lewat UI aktual. Soal tetap membekukan simulasi.
- 36 balapan engine lengkap berpasangan (3 stage ×3 kesulitan ×4 seed) identik setiap langkah dengan baseline, termasuk AI, buff, inventori, soal, penilaian, token dan ghost.
- Render terisolasi 14 pasangan plus cat low dan vehicle-only: 16 perbandingan piksel identik. Tidak membangun ulang atau mengubah model.
- Ruang Guru/ekspor diuji kembali. HTML ekspor mempertahankan aset, HUD, Smart AI, tiga pilihan stage, dan dapat memulai balapan dengan jaringan dimatikan. Tidak ada permintaan aset HTTP.
- Verifikasi scope membalik tiga penggantian renderer dan menghasilkan baseline persis. Semua script selain renderer, markup HUD/CSS, aset, struktur arena, serta berkas historis tetap identik.

Batas pengujian: perangkat HP fisik belum diuji, tidak mengklaim FPS atau seluruh Grand Prix manual. `file://` diblokir administrator browser cloud; pengujian offline menyuplai byte HTML lokal ke konteks dengan jaringan dimatikan. HTML tetap mandiri dan seluruh dependensi tertanam. Gambar thumbnail menu lama dipertahankan karena patch hanya mengubah langit saat render; tidak mengubah katalog stage/HUD atau membuat arena baru.

## Sumber yang dapat diedit

`source/sky-methods.js` berisi palet, generator awan, shader dan draw langit. `source/assemble.py` memasukkan metode tersebut serta dua perubahan fog terbatas ke baseline PATCH 4.5. `bounded-changes.json` mencatat penggantian yang dapat dibalik. Tes regresi memakai ulang sumber tes PATCH 4.5 melalui `source/reuse.cjs`, tanpa menyalin engine.

Dari root repositori:

```sh
python visual-upgrade/sky-horizon/source/assemble.py
python visual-upgrade/sky-horizon/source/verify_scope.py
python -m http.server 8000
```

Dengan server port 8000 berjalan, jalankan `node visual-upgrade/sky-horizon/source/capture.cjs`, lalu `test_sky.cjs`, `test_controls.cjs`, `test_stages.cjs`, `test_export.cjs`, `test_offline.cjs`, `test_unchanged_render.cjs`, `test_core.cjs` dan `test_engine_parity.cjs`. Chromium/Playwright memakai lingkungan yang sama dengan PATCH 4.5. Setelah seluruh laporan lulus, `python visual-upgrade/sky-horizon/source/package.py` membuat komposit before–after, metrik, ZIP playable dan ZIP review dengan CRC serta verifikasi byte HTML.

Tidak merge ke main, tidak mengganti `index.html`, tidak deployment, dan tidak mengerjakan Prompt 5/10 stage.
