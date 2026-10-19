# Pengukuran perilaku AI — PATCH 3 vs PATCH 4

216 balapan engine berpasangan: 12 seed × 3 stage × 3 kesulitan × 2 versi. Tambahan 108 kasus penyelesaian AI. Langkah simulasi 0,05 detik. Pembalap referensi memakai controller yang sama, tidak memakai item, menjawab 4/5 soal dengan benar. Ini benchmark deterministik, bukan win-rate siswa atau FPS perangkat.

| Versi | Kesulitan | Posisi rata-rata pemain referensi | Menang referensi | Kontak rintangan / balapan (4 AI) | Buff dipakai / AI-menit | Hit pemain / 36 balapan |
|---|---|---:|---:|---:|---:|---:|
| PATCH 3 | Santai | 1.00 | 100.0% | 4.64 | 0.00 | 0 |
| PATCH 3 | Sedang | 4.42 | 2.8% | 4.00 | 0.54 | 24 |
| PATCH 3 | Menantang | 4.94 | 0.0% | 3.56 | 0.40 | 28 |
| PATCH 4 | Santai | 1.00 | 100.0% | 5.28 | 1.80 | 0 |
| PATCH 4 | Sedang | 3.08 | 13.9% | 3.92 | 3.15 | 8 |
| PATCH 4 | Menantang | 4.33 | 0.0% | 2.47 | 3.74 | 17 |

Baseline hanya Gelembung/Oli; PATCH 4 memakai sembilan buff secara kondisional. Kontak rintangan dihitung dari lintasan dan posisi, karena baseline belum memberi penalti collision rintangan pada AI. Counter kontak bukan jumlah damage yang setara pada dua versi. Hit di tabel adalah collision proyektil/oli primer; pantulan tidak dihitung sebagai proyektil tambahan.

## Distribusi penggunaan alami

| Kesulitan | Turbo | Perisai | Magnet | Gelembung | Oli | Pantul | Nitro | Grip | Radar |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| easy | 33 | 0 | 22 | 0 | 0 | 0 | 61 | 15 | 31 |
| normal | 41 | 7 | 43 | 23 | 21 | 7 | 79 | 19 | 47 |
| hard | 43 | 17 | 46 | 31 | 38 | 13 | 67 | 33 | 60 |

Setiap baris mencakup 36 balapan × 4 AI. Nitro dihitung per charge yang dipakai. Santai tidak mendapat Gelembung/Oli; Perisai/Pantul dapat tersimpan tetapi tidak perlu dipakai jika tidak ada ancaman. Menyimpan item tanpa menggunakannya bukan kegagalan otomatis.

## Penyelesaian dan deadlock

| Kesulitan | Kasus | Rata-rata waktu finis AI | Semua finis | Stall maksimum |
|---|---:|---:|---|---:|
| easy | 36 | 49.02 dtk | Ya | 0.00 dtk |
| normal | 36 | 37.29 dtk | Ya | 0.00 dtk |
| hard | 36 | 35.73 dtk | Ya | 0.00 dtk |

Harness penyelesaian melanjutkan AI secara terpisah dengan mobil referensi 19 m/s. Harness ini tidak memutar ulang collision item penuh, sehingga menguji kelangsungan gerak/finis, bukan akurasi serangan. Balapan berpasangan di tabel pertama menjalankan collision engine sebenarnya. Stall maksimum pada balapan PATCH 4 dengan collision penuh: 0.05 dtk. Jeda quiz tidak dihitung sebagai stall.

## Kepribadian pada kesempatan serangan yang identik

2.000 kesempatan identik per baris, satu item Gelembung, target sah pada posisi yang sama. Persentase adalah pemilihan aksi; target tetap divalidasi ulang sebelum ditembakkan. Ini memisahkan pengaruh kepribadian dari posisi start dan kesempatan berbeda dalam balapan.

| Kesulitan | Kepribadian | Peluang konfigurasi | Terukur |
|---|---|---:|---:|
| normal | agresif | 33.8% | 34.4% |
| normal | defensif | 11.7% | 13.2% |
| normal | berisiko | 27.3% | 28.1% |
| normal | seimbang | 22.1% | 23.1% |
| hard | agresif | 65.0% | 65.2% |
| hard | defensif | 22.5% | 23.8% |
| hard | berisiko | 52.5% | 53.9% |
| hard | seimbang | 42.5% | 43.8% |

Pertahanan pada ancaman identik ETA 1,26 dtk: Defensif dan Seimbang memilih Perisai lebih awal; Agresif dan Berisiko belum menghabiskan Perisai pada jarak itu. Pada ancaman lebih dekat semua dapat bertahan. Peluang di atas bukan peluang mengenai siswa.

## Evaluasi yang dibatasi bukti

Uji pertama menunjukkan kontak rintangan Sedang 5,50 per balapan, lebih buruk daripada baseline 4,00. Kalibrasi memperpanjang jangkauan sensor lokal sesuai waktu reaksi; hasil akhir 3,92. Menantang turun dari 3,56 menjadi 2,47. Santai masih lebih sering menyentuh rintangan (5,28 dibanding 4,64); kemampuan adaptasinya memang rendah dan tidak mengirim serangan. Tidak mengklaim semua perilaku lebih baik pada setiap seed.

Kecerdasan yang diuji mencakup pemilihan target pemain/AI, pembatalan target setelah windup, pertahanan terhadap proyektil, peluang menghindar dan jalur menyalip, sensor Radar yang terbatas, penggunaan item sesuai konteks, serta pasokan/cooldown terbatas. Pace dasar 16,5 / 21,9 / 22,6 dipertahankan. Penyesuaian pace menurut jarak pemain dihapus; AI dibatasi 23 m/s tanpa boost, 31 m/s dengan boost. Gerak longitudinal selalu speed × dt, tanpa teleport.

Data mentah, seed, penggunaan tiap aktor dan tiap balapan berada dalam `simulation-results.json`. Tidak ada pengujian siswa SMP, HP fisik, atau klaim signifikansi statistik/FPS.
