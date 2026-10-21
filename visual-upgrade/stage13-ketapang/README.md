# 6J — Ketapang: Ale-Ale Chaos Circuit

Arena final **playable untuk tinjauan**, dibangun dari HEAD Stage12 `c5c717e23cd020b1d0d464ed0923f3b5cb504089`. Seluruh13 world tersedia setelah validasi; tidak ada penggantian ID lama atau arena palsu bernama baru. Tidak merge/deployment/mengubah `index.html` online. Prompt7 tidak dikerjakan.

## Arena dan batas representasi

Sirkuit kota-pelabuhan **fiktif1241,93m**,550 segmen tertutup, maksimum elevasi19m dan kemiringan0,200 (~11,3°). Bentuk baru mencakup jalan bertingkat dengan pilar, hairpin/S-curve, jembatan sempit6,7m, turunan ke dermaga, slalom, dua tingkat ramp dan percabangan. Jalan utama11m; origin/collider kendaraan, physics global dan kamera chase tidak diubah.

Kota blocky, keraton/plaza, Tugu Ale-Ale bertema kerang, toko, kelapa, quay, crane generik, perahu dan kontainer warna-warni dibuat prosedural. Langit hangat, awan dan haze memakai sistem lama. Geometri datar kota/quay dipisah dari caster shadow agar tidak menimbulkan pola self-shadow pada bidang sangat luas; soft contact shadows tetap dipakai pada bangunan. Perbaikan hanya pada builder Ketapang.

**Landmark adalah interpretasi stylized yang belum diverifikasi foto**, bukan rekonstruksi akurat. `https://id.wikipedia.org/wiki/Keraton_Matan` gagal dengan CONNECT403; tidak ada foto spesifik terlampir. Bentuk atap, susunan fasad, monumen, warna dan proporsi tidak diklaim akurat. Pelabuhan, jalan bertingkat dan obstacle adalah rekaan permainan. Keraton berada jauh di plaza aman, tidak mempunyai collider/destruction di jalur balapan.

## Dua belas zona nyata

| u / zona | Mekanisme | Mitigasi / sisi aman |
|---|---|---|
| .08 Kontainer bergeser | Translasi terbatas, berhenti/mulai pada siklus12s | Kanan; lampu mendahului gerakan |
| .17 Palang | Buka/tutup siklus9s, posisi pivot dan AABB tersinkron | Kanan selalu tersedia |
| .255 Rotor | Batang berputar kontinu pada area kiri | Kanan; lampu bahaya tetap, putaran terlihat |
| .34 Bridge | Deck28m, rail collider, lebar6,7m | Rem, tetap di tengah |
| .43 Drum | Bolak-balik teratur dengan waktu peringatan | Sisi yang sedang bebas; jump jika tepat |
| .52 Peti | Collider solid dan penalti laju | Kanan |
| .605 Slalom | Tiga barrier kiri/kanan/kiri berjarak24m | Kendalikan laju dan kemudi |
| .69 Oli | Patch traksi sementara di kanan | Kiri atau Ban Anti-Selip |
| .755 Ramp/gap | Dua bidang ramp visual, satu takeoff native10,5m/s, gap3,2m | Gas≥9m/s; rescue mundur bila gagal |
| .85 Percabangan | Dua dek, divider, gap3m pada kanan | Kiri aman; kanan hadiah1 token sesudah mendarat |
| .925 Penghalang final | Blok bergerak di kanan, pola periodik | Kiri dan perhatikan lampu |
| .977 Rangkaian final | Dua barrier kiri setelah tikungan/zona timing | Geser ke kanan sampai finis |

Papan36m sebelum pusat zona; slalom/bridge/fork/sequence ditambah setengah panjang. Terdapat area pemulihan antar kelompok, tidak semua obstacle ditumpuk di satu segmen. Tidak ada dua obstacle menutup seluruh jalan sekaligus.

`RaceChaos.pose/parts/hazards` menjadi sumber posisi visual dan collider. Slider/drum bergerak kontinu tanpa teleport saat reset siklus. Palang memperingatkan2s sebelum menutup dan tetap merah selama tertutup/membuka. Rotor terus bergerak dengan indikator bahaya konstan. Semua memakai `session.elapsed`; tidak ada wall clock/timer baru. AI membaca posisi **saat ini** dalam jangkauan persepsi, bukan posisi masa depan atau jawaban soal.

Solid collision selalu menyelesaikan overlap, terpisah dari cooldown damage: lateral ke sisi aman terdekat, atau mundur jika tidak ada sisi, tidak pernah maju. Penalti laju, notifikasi singkat dan event obstacle memakai SFX/VFX lama. Tidak menambahkan buff atau mengubah aturan buff. Perisai tetap pertahanan combat sesuai aturan lama, bukan izin menembus kontainer. Radar/Grip dan pilihan waktu Turbo/Nitro tetap berguna.

Dua jalur memakai koordinat progres/lateral engine, **bukan graph rute independen**. AI Santai memilih kiri; personality `berisiko` pada Sedang/Menantang bisa mengambil kanan. Hadiah lintasan hanya1 token setelah crossing airborne yang sah dan landing, sekali per lap; bukan buff akademik.

Rescue hanya ke checkpoint aman yang sudah dilewati (minimum mundur sebelum hazard) dengan tunggu2,4s pada clock simulasi. Inventori/charge/token/jawaban tidak dihapus. Tidak ada shortcut longitudinal; progres tetap sepanjang centerline. Buff berdurasi berjalan saat race clock berjalan selama menunggu, dan membeku bersama obstacle/AI saat pause/soal.

## Empat turnamen

| ID tetap | Turnamen | Ronde |
|---|---|---:|
| `kalbar-klasik` | Kalbar Klasik | 3 |
| `nusantara` | Nusantara | 10 |
| `kalbar-extreme` | Kalbar Extreme Challenge: Kubu Raya → Kayong Utara → Ketapang | 3 |
| `lengkap-13` | Grand Prix Lengkap13 Arena | 13 |

Metadata cup identik dengan Stage12. Dua cup terakhir menjadi tersedia karena registry benar-benar mempunyai13 world, bukan mengganti aturan availability. Release digate oleh pengujian seluruh transisi. Tidak ada perubahan poin, ketuntasan60 pada fixture, retry, skor akademik atau jumlah soal yang ditentukan guru.

[Unit semua cup](grand-prix-tests.json) dan [uji UI empat cup](grand-prix-browser-tests.json) mencakup29 ronde sukses ditambah satu gagal/ulang pada akhir setiap cup, hasil/juara, rekap, point rollback, ekspor, ghost/progres, reload dan PIN. **UI memakai fixture posisi ke gate/finish, bukan29 balapan manual penuh.** Dunia asli dan UI asli tetap dimuat pada setiap ronde.

## Validasi aktual

- [Physics](physics-tests.json):18 reference races,3 kesulitan×6 seed, lima jawaban (empat benar), skor80;14 pilihan kendaraan masing-masing menyelesaikan rute dengan skor100. Driver benar-benar mengirim gas/rem/steer/jump ke Session, tidak memindahkan posisi sepanjang rute.
- [Tiga lap](multilap-tests.json):3 driver dan12 AI menguji checkpoint/hazard/reward lintas garis finis.
- Completion AI utama72, ditambah [48 AI dengan rotasi kendaraan](ai-collision-tests.json) yang mencakup semua14 identitas pada tiga kesulitan. Setiap langkah memeriksa laju≤31m/s, tidak ada loncatan maju, tidak ada sisa penetrasi collider solid. Ini simulasi engine, bukan tes perangkat fisik.
- [Mekanik](mechanics-tests.json):12 kelompok/12 collider parsial expanded, swept collision, kontinuitas/indikator, bridge/divider, jump9/12/23/31, rescue, Grip/oil, Radar, reward hanya crossing sah, dan freeze seluruh clock.
- [Buff/AI](item-tests.json):sembilan item, dua slot, supplies terbatas, cooldown, windup, target pemain/AI, chain-hit immunity, reflect/shield, anti-rubberband dan pause.
- [Renderer](world-tests.json):108 frame12 posisi×3 kualitas×3 cuaca, cleanup buffer/texture saat pindah ke seluruh12 world sebelumnya, stabil saat rebuild.
- [Clearance](clearance-tests.json):sampling lajur terhadap seluruh kelompok geometri statis dan96 chase frames12/31m/s. Pendekatan ramp yang disengaja dikecualikan secara eksplisit dari pemeriksaan “terrain menutupi jalan”; collider/ramp diuji terpisah. Kamera tidak menembus tanah/bangunan.
- [Render freeze](render-mechanics-tests.json):kelima mekanisme, water/cloud/actor freeze pada pause/question, bergerak hanya saat waktu simulasi berubah, night→day restore.
- [UI](browser-tests.json):desktop1366×768, sentuh390×844/844×390,13 kartu aktif, guru/PIN, siswa, A/D/touch, kuis/buff, pause, hasil/ghost/progres/replay/reload/ekspor.
- [Offline/ekspor](offline-tests.json):network disabled, nol request aset HTTP/CDN, Web Crypto lokal, ekspor tidak membawa verifier/salt/PIN, hasil ekspor bisa memulai race pada konteks offline baru.
- [Hash](scope-tests.json) dan [28 render pixel](unchanged-renders.json):14 pasangan GLB, cat low/car-only dan12 world lama terlindungi. Renderer lama diuji setelah membangun/merender Ketapang dan beralih kembali. Physics350 langkah per12 stage lama identik; seluruh berkas historis visual-upgrade/rootindex tidak berubah.

Benturan AI bukan kegagalan tes jika menghasilkan penalti dan respons sah. AI Menantang masih bisa salah/terkena obstacle; laporan memuat collision dan overtake **plans**, bukan klaim sempurna atau klaim jumlah menyalip aktual. Kesulitan tidak diukur dari pace saja: ada lebih banyak mekanisme bergerak, slalom, jalur risiko, braking input, sensor, supplies dan keputusan item. Parameter laju global lama tidak dinaikkan.

## Screenshot sebenarnya

[Overview](screenshots/overview.png) · [Tugu Ale-Ale](screenshots/tugu-ale-ale.png) · [Keraton](screenshots/keraton-matan.png) · [Kontainer](screenshots/sliding-container.png) · [Rotor](screenshots/rotating-barrier.png) · [Drum](screenshots/rolling-drum.png) · [Jalan bertingkat](screenshots/elevated-road.png) · [Slalom](screenshots/slalom.png) · [Jump](screenshots/ramp-jump.png) · [Percabangan](screenshots/fork-routes.png) · [Zona final](screenshots/final-challenge.png).

[Desktop](screenshots/race-desktop.png) · [HP landscape](screenshots/race-844x390.png) · [HP portrait](screenshots/race-390x844.png) · kartu [sebelum](screenshots/before-unavailable-card.png)/[sesudah](screenshots/after-available-card.png).

Overview/landmark memakai kamera inspector, fog dimatikan hanya pada overview agar jalur utuh terlihat. Gameplay memakai chase camera dan fog biasa. Jump berasal dari delapan langkah simulasi asli. Baseline belum memiliki world Ketapang; tidak membuat before-world palsu atau ilustrasi generatif.

## Metrik, batas dan distribusi

HTML **24.927.106 byte** (+44.827 dari Stage12); tetap di bawah25.000.000 byte. Lingkungan65.930 segitiga,50 batch warna termasuk14 label canvas dan lima mekanisme,15 batch shadow. Tidak sama dengan draw call keseluruhan frame; rincian kualitas/segitiga/frame aktual pada [asset-metrics.json](asset-metrics.json) dan [release-metrics.json](release-metrics.json). Tidak mengklaim FPS, frame time, HP fisik atau benchmark memori.

HTML tunggal tetap efisien sehingga ZIP playable berisi HTML+MULAI.txt; reviewZIP menambahkan sumber/screenshot/report. Alternatif aset lokal terpisah belum diperlukan/dibangun dan tidak diklaim lolos file://. Direct `file://` dicoba pada distribusi, hasilnya di [direct-file-tests.json](direct-file-tests.json); browser cloud memblokir melalui kebijakan administrator. Offline yang lolos memakai dokumen disuplai harness localhost dengan jaringan dimatikan. Tidak menambahkan server wajib/fetch aset lokal. Perlu uji file:// di browser target.

## Source dan build

[harbor.js](source/harbor.js) · [chaos-physics.js](source/chaos-physics.js) · [track.json](track.json) · [stages.json](stages.json) · [cups.json](cups.json) · [assemble.py](source/assemble.py). Geometri prosedural JavaScript editable; tidak ada GLB/Blender baru. Memakai utilitas Garden/CityBatch, label, palm, canoe, sky dan GPU cleanup lama. Engine tidak diduplikasi.

Dari checkout baseline Stage12, Python3/Pillow, Node, Chromium dan Playwright:

```bash
python visual-upgrade/stage13-ketapang/source/assemble.py
node visual-upgrade/stage13-ketapang/source/capture.cjs
python visual-upgrade/stage13-ketapang/source/thumbnails.py
python visual-upgrade/stage13-ketapang/source/assemble.py
```

Candidate: `/tmp/blokraya-6j/candidate.html`. Jalankan server root `python -m http.server 8000`; browser harness mengintersep URL distribusi dengan candidate. Jalankan seluruh test_*.cjs kecuali test_release/test_file, serta verify_scope.py. Jangan mengubah candidate ketika tes berjalan. Release hanya jika laporan diwajibkan passed dan thumbnail render nyata tersedia.

```bash
python visual-upgrade/stage13-ketapang/source/assemble.py --release
node visual-upgrade/stage13-ketapang/source/test_release.cjs
node visual-upgrade/stage13-ketapang/source/test_file.cjs
python visual-upgrade/stage13-ketapang/source/package.py
```

PIN/progres/bank lama tidak dipindahkan atau ditanam sebagai QA. Hash ZIP lengkap berada di repository release-metrics.json; ZIP review tidak memuat hash dirinya sendiri.
