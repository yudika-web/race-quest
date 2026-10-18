# Penyempurnaan Kucing — mobil sport dipertahankan

Revisi ini melanjutkan commit `e5d7e07313751b5d168e77f7ac457f2139ceb80c` pada branch `dev/race-quest-cat-sport-visual-upgrade`. Hanya geometri Kucing dalam dua GLB tertanam yang diganti. Pemeriksaan data membuktikan posisi/normal/indeks/material **seluruh 28 batch mobil identik**, seluruh pivot identik, runtime dan HTML di luar data aset identik, serta 13 karakter lain tidak berubah.

## Bagian yang diperhalus

- **Kepala, pipi, rahang, dagu dan badan:** kepala dibentuk dari penampang melengkung yang dirancang khusus. Kulit kepala–leher–torso–bahu–lengan–pangkal paw–paha disatukan, dihaluskan, lalu kepadatan mesh dibatasi khusus pada Kucing. Pipi tidak lagi berupa tonjolan terpisah.
- **Moncong dan wajah:** satu permukaan moncong dua lobus dengan tepi mengikuti pipi; hidung mengecil dan membulat, area mulut/lidah lebih rapi, serta dagu menyatu dengan siluet rahang. Pola tabby mengikuti bentuk kepala dan diproyeksikan ke permukaan punggung baru.
- **Mata dan telinga:** mata simetris berupa permukaan melengkung yang mengikuti kepala, dengan iris/pupil/highlight yang lebih bersih dan kelopak membulat. Telinga menjadi volume tertutup dengan tepian lembut dan bagian dalam merah muda yang terpasang ke permukaan telinga.
- **Lengan dan paw:** kurva bahu–siku–pergelangan diperhalus; palm dan ibu jari dibuat menyatu, dengan penanda jari tipis. Tangan tetap pada setir, paha duduk pada kursi dan sepatu berada di bawah kap yang tidak diubah.

Tidak ada tekstur baru atau tambahan batch gambar. Warna jingga, identitas tabby, proporsi umum, pose duduk dan pivot animasi dipertahankan. Sistem gameplay dan animasi prosedural tidak diubah.

## Berkas

- [HTML playable terbaru](../race-quest-visual-upgrade.html)
- [GLB detail](../race-quest-cat-sport.glb) / [GLB ringan](../race-quest-cat-sport-low.glb), masing-masing berisi Kucing baru dan mobil yang identik dengan baseline.
- [Sumber Blender](../source/race-quest-cat-sport.blend); [pemodelan Kucing](../source/refine_cat.py), dipanggil oleh [generator utama](../source/build_cat.py).
- [Lembar perbandingan Kucing](cat-refinement-sheet.jpg), [wajah](comparison-face.jpg), [siluet samping](comparison-profile.jpg), [garasi utuh](comparison-garage.jpg), dan [kamera balapan](comparison-race.jpg).

Folder `before/` direkam dari game pada commit baseline sebelum model diganti. Folder `after/` direkam dari revisi ini. Kamera, viewport, posisi balapan, seed dan waktu idle disamakan; gambar berasal dari renderer game sebenarnya. Tidak ada retouch karakter. Perbandingan tahap awal di `../comparisons/` tetap disimpan sebagai riwayat; beberapa tangkapan smoke test di folder itu diperbarui oleh pengujian terbaru.

## Kepadatan dan ukuran

| Komponen | Sebelum | Revisi |
|---|---:|---:|
| Segitiga Kucing detail | 16.514 | 37.458 |
| Segitiga mobil detail | 20.931 | **20.931 identik** |
| Total pasangan detail | 37.445 | 58.389 |
| Segitiga Kucing ringan | 6.978 | 15.405 |
| Segitiga mobil ringan | 8.678 | **8.678 identik** |
| Total pasangan ringan | 15.656 | 24.083 |
| Batch gambar pasangan per pass warna | 44 | 44 |
| HTML mandiri | 19.051.488 byte | 19.736.629 byte (+3,60%) |

GLB detail 1.137.120 byte; versi ringan 513.684 byte. Tambahan geometri hanya pada Kucing; LOD/kualitas grafis dan pemilihan model berdasarkan jarak tetap memakai sistem sebelumnya. GPU timer tidak tersedia, sehingga tidak ada klaim FPS atau performa perangkat fisik.

## Pemeriksaan

- `scope-verification.json`: geometri/material mobil, pivot, renderer/gameplay, HTML selain aset Kucing, dan aset karakter lain identik dengan baseline.
- `animation-tests.json`: 10 pemeriksaan khusus model — kedip, kedua telinga, ekor, lean, jump, kemudi/putaran roda, matriks animasi saat waktu membeku, fixture kontak paw, dan tidak ada error WebGL.
- Fixture kontak memakai pusat palm dan transformasi renderer sebenarnya pada kemudi ±0,42 radian dan jump 0–3 unit. Jarak pusat paw ke rim maksimal 0,0476 m, masih dalam envelope grip yang diuji; ini dilengkapi pemeriksaan render depan, samping dan belakang, bukan solver tabrakan mesh lengkap.
- Smoke browser terbaru: 16 pemeriksaan lulus termasuk A/D, jump, kontrol sentuh, soal, buff, kelanjutan, jeda pemain/AI/waktu animasi, serta offline. Tidak ada error JavaScript.
- Regresi inti: 7 pemeriksaan lulus untuk aturan/UI/scenery, bank soal JSON/CSV, stage/AI, Grand Prix, drift/jump, buff, hasil, ghost dan progres.
- Kedua GLB diimpor kembali dengan Blender dan data normal diperiksa bernilai hingga serta panjang satuan.
- Pengujian visual desktop 1440×1000 dan HP emulasi 390×844; tidak ditemukan clipping terbuka atau tangan lepas pada pose yang direkam. Pengujian HP bukan pengujian perangkat fisik. Browser cloud memblokir `file://`; offline dibuktikan dengan jaringan browser dimatikan dan HTML dipasok dari byte lokal.

Hasil smoke/regresi/offline lengkap berada di JSON tingkat folder `visual-upgrade/`. Pemeriksaan kuis memakai fixture posisi dekat gerbang dan hitungan mundur diperpendek; ini bukan klaim telah menyelesaikan seluruh Grand Prix secara manual.

## Reproduksi

Dari folder `visual-upgrade/`: jalankan `blender -b --python-exit-code 1 --python source/build_cat.py`, lalu `python3 source/assemble.py`. Dari root repositori, jalankan server statis port 8000 untuk skrip browser. Pemeriksaan scope: `python3 visual-upgrade/source/verify_cat_refinement.py`; pengujian model: `node visual-upgrade/source/test_cat_animation.cjs`. GLB: `blender -b --python-exit-code 1 --python visual-upgrade/source/validate_cat_glb.py`.
