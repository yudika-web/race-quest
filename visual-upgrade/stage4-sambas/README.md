# BlokRaya — 6A / Stage 4 Sambas: Royal River Road

Baseline lokal dan remote diverifikasi: `346c915ca0272f6b10732fdd99fe28bcde87fb62`, branch `dev/race-quest-cat-sport-visual-upgrade`. Distribusi baru: [`../blokraya-stage4-sambas.html`](../blokraya-stage4-sambas.html). Hanya Sambas yang dibangun. Stage 5–10 tetap **Segera Hadir**. Tidak merge, mengubah `index.html`, deployment, atau mengerjakan 6B.

## Arena dan visual

Lintasan fiktif baru sepanjang **687,84 m** berupa loop berlekuk: ruas plaza kerajaan, tikungan kawasan rumah panggung, jalan tepian sungai, elevasi ringan maksimum **2 m**, tiga obstacle dan satu ramp; tanpa celah jalan. Geometri jalan dan physics memakai pipeline lama, dengan titik lintasan/seed baru, bukan salinan world lama yang diganti nama. Lebar jalan, batas collision, kontrol dan aturan balapan tetap.

Lingkungan memakai geometri prosedural blocky: kompleks istana kuning/hijau dengan selasar/tangga, taman dan pendekatan plaza, rumah panggung, pohon/kelapa, lampu, sidewalk/marka, promenade berpagar, sungai berkelok dengan dua tepian, dermaga beratap, perahu, serta jembatan wisata dekoratif. Sungai dan jembatan bukan mekanik berenang atau jalur pintas. Semua dekorasi tetap di luar envelope berkendara.

Gradient langit, awan blocky dan haze memakai shader lama dengan palet Sambas yang hangat. Tidak ada tekstur langit baru, animasi waktu nyata, shader baru, maupun aset karakter/kendaraan yang diubah. Builder mewarisi helper City/Garden untuk bevel, pohon, atap, lampu dan planter, tanpa menyalin seluruh arena lama. Blender tersedia, tetapi tidak diperlukan: sumber editable arena ini adalah JavaScript dan JSON, bukan GLB statis yang berat.

**Batas akurasi landmark:** istana adalah interpretasi artistik blocky, **bukan rekonstruksi historis terverifikasi**. Tidak ada foto Sambas yang disediakan; akses situs referensi dari cloud ditolak 403. Detail denah, jumlah bukaan, warna atap dan ornamen belum divalidasi terhadap foto tepercaya. Tidak membuat lambang/tulisan kerajaan fiktif. Lihat [`reference-notes.md`](reference-notes.md). Siluet dimodelkan sebagai geometri nyata; papan nama kecil hanya penunjuk. Penilaian akurasi landmark masih memerlukan tinjauan referensi, terpisah dari pengujian teknis arena.

## Integrasi dan perlindungan

ID baru tetap `sambas` sesuai metadata Prompt 5. Pengaturan guru, kartu stage, thumbnail/preview asli, Session/Track, minimap, AI, sembilan buff, dua slot inventori, hasil belajar, ghost dan `stageProgress.sambas` memakai alur yang sama. Profil, token, unlock, audio, HUD, PIN dan kunci penyimpanan lama tidak diganti. Tidak ada profil/unlock/token demonstrasi disisipkan dalam distribusi.

Empat arena kini playable: `kampung` (Pontianak), `kapuas` (Mempawah), `hutan` (Singkawang), `sambas`. **Kalbar Klasik tetap tiga arena lama**. Sambas sudah menjadi ronde keempat pada konfigurasi Nusantara, tetapi cup tersebut tetap dinonaktifkan karena enam world lain belum dibuat. Tidak membuat turnamen tambahan atau membuka arena palsu.

Kandidat pengembangan diuji pada HTML sementara sebelum file distribusi dibuat. `assemble.py --release` memerlukan laporan physics, item, world, browser, offline dan render terlindungi berstatus passed serta thumbnail asli. [`activation.json`](activation.json) mencatat aktivasi dari status awal belum tersedia dan kesamaan byte kandidat dengan rilis.

Seluruh script Core, renderer dasar, scenery lama, AI, buff, audio/VFX, HUD, PIN/mode, loading/poster dan ekspor tetap byte-identik. Tambahan track/sky/world didaftarkan melalui satu script baru. Hanya entri Sambas dan dua thumbnail baru yang ditambahkan pada katalog/aset stage. Verifikasi scope dapat membalik assembly tepat ke baseline; **2.056 file historis, 20 payload script/aset dan enam thumbnail lama identik**.

## Sumber dan build

- [`track.json`](track.json): waypoint, elevasi, palette, obstacle, ramp dan seed.
- [`stages.json`](stages.json): katalog sepuluh arena; hanya Sambas berubah.
- [`source/river.js`](source/river.js): builder istana, sungai/terrain, promenade, dermaga, jembatan dan dekorasi. Satu adapter baru ke registry Prompt 5.
- [`source/assemble.py`](source/assemble.py): build dari HTML Prompt 5, penambahan palet langit terisolasi dan payload thumbnail.
- [`source/capture.cjs`](source/capture.cjs): kamera review dan screenshot dari renderer aktual.
- [`source/thumbnails.py`](source/thumbnails.py): dua WebP 640×400 dari screenshot istana dan kamera balapan; tidak memakai ilustrasi generatif.
- [`source/package.py`](source/package.py): ZIP playable/review dan pemeriksaan CRC/kesamaan HTML.

Dari root checkout, memakai Python/Pillow dan Node/Playwright/Chromium yang sudah tersedia:

```sh
python visual-upgrade/stage4-sambas/source/assemble.py
node visual-upgrade/stage4-sambas/source/capture.cjs
python visual-upgrade/stage4-sambas/source/thumbnails.py
python visual-upgrade/stage4-sambas/source/assemble.py
node visual-upgrade/stage4-sambas/source/test_physics.cjs
node visual-upgrade/stage4-sambas/source/test_items.cjs
node visual-upgrade/stage4-sambas/source/test_world.cjs
node visual-upgrade/stage4-sambas/source/test_browser.cjs
node visual-upgrade/stage4-sambas/source/test_offline.cjs
node visual-upgrade/stage4-sambas/source/test_render_parity.cjs
python visual-upgrade/stage4-sambas/source/verify_scope.py
python visual-upgrade/stage4-sambas/source/assemble.py --release
node visual-upgrade/stage4-sambas/source/test_file.cjs
python visual-upgrade/stage4-sambas/source/package.py
```

Jalankan server statis internal dari root repository pada port 8000 untuk tes browser. Harness menyuplai kandidat HTML dari `/tmp/blokraya-6a/candidate.html` pada URL rilis; file rilis identik. Playwright menggunakan path runtime cloud yang tertulis pada `browser.cjs`; sesuaikan untuk komputer lain. Maksimal dua browser WebGL berat bersamaan. Dependensi pengembangan tidak diperlukan saat bermain. Builder memerlukan checkout baseline Prompt 5, bukan hanya ZIP review.

## Pengujian terarah

| Bukti | Hasil |
|---|---|
| [`physics-tests.json`](physics-tests.json) | 7 kelompok: empat track tersedia, enam diblokir, GP lama tetap, physics/progres lama identik, loop tertutup tanpa perpotongan/overlap jalan, 18 balapan driver referensi (3 kesulitan × 6 seed), 18 uji penyelesaian semua AI, collision/ramp/drift/landing, sembilan buff, freeze dan ghost key. |
| [`item-tests.json`](item-tests.json) | 11 kelompok interaksi item/AI pada Sambas: stok terbatas, sembilan buff kontekstual, target pemain/AI, cooldown/charge, pantulan/grip, projectile/oli mengenai target, immunity, sensor/radar, freeze dan contact. |
| [`world-tests.json`](world-tests.json) | 108 sampel nyata: 12 posisi × 3 kualitas × 3 cuaca; tanpa error WebGL. Struktur di luar envelope, teardown buffer/tekstur saat pindah ke tiga arena lama dan rebuild stabil. |
| [`browser-tests.json`](browser-tests.json) | 27 pemeriksaan: menu, thumbnail, konfigurasi guru, student tanpa PIN, loading minimal 3 detik, Sambas nyata/four AI, A/D, pause/quiz freeze, buff benar, hasil/ekspor/progres/ghost/reload/PIN, replay melalui garasi, portrait/landscape serta touch press nyata via CDP. |
| [`offline-tests.json`](offline-tests.json) | 28 pemeriksaan jaringan mati: PIN lokal, ekspor guru, aset tertanam, start Sambas dan HTML ekspor, kuis/buff, empat world, tanpa permintaan HTTP/CDN aset atau kebocoran salt/verifier PIN. |
| [`unchanged-renders.json`](unchanged-renders.json) | 19 perbandingan piksel identik: 14 pasangan, Cat low, mobil Cat saja dan tiga world lama setelah masuk/keluar Sambas; kamera/pose/waktu tetap 256×256. |
| [`scope-tests.json`](scope-tests.json) | Assembly dapat dibalik tepat; sumber engine dan aset historis terlindungi, hanya metadata Sambas aktif. |
| [`direct-file-tests.json`](direct-file-tests.json) | Navigasi `file://` benar-benar dicoba, tetapi browser cloud menolak dengan `ERR_BLOCKED_BY_ADMINISTRATOR`; tidak dilewati menggunakan flag. Tidak diklaim lolos. |

AI menyelesaikan seluruh 72 finish pada 18 kasus completion. Rerata waktu simulasi: Santai **47,57 s**, Sedang **36,48 s**, Menantang **34,65 s**; rencana menyalip teramati pada semua level. Angka ini bukan FPS, waktu balapan manusia, atau benchmark perangkat. Driver referensi menyelesaikan seluruh lintasan dan menghasilkan skor akademik 80% dari 4/5 benar; posisi finis/buff tidak mengubah skor tersebut.

Browser UI memakai fixture posisi ke gate/finis untuk menguji transisi dengan cepat, bukan klaim seluruh lintasan dimainkan manual. Penyelesaian lintasan penuh diuji terpisah oleh simulasi. Screenshot desktop/HP berasal dari game/renderer asli. Tidak ada error JavaScript/WebGL pada alur yang lolos. HP diuji lewat emulasi, **belum perangkat fisik**. Seluruh Grand Prix tidak dimainkan manual ulang karena aturan/code cup tidak berubah; konfigurasi, gating dan physics lama dibandingkan secara terarah.

## Screenshot dan metrik

- [Overview](screenshots/overview.png), [istana](screenshots/palace.png), [promenade/sungai](screenshots/river-promenade.png), [dermaga](screenshots/dock.png), [jembatan](screenshots/bridge.png).
- [Kamera game](screenshots/gameplay.png), [tikungan](screenshots/river-corner.png), [ramp](screenshots/ramp.png), [balapan dengan HUD desktop](screenshots/race-desktop.png).
- HP [portrait](screenshots/race-390x844.png), [landscape](screenshots/race-844x390.png); menu [desktop](screenshots/menu-desktop.png), [portrait](screenshots/menu-390x844.png), [landscape](screenshots/menu-844x390.png).
- [Hasil belajar](screenshots/results.png), [kuis](screenshots/quiz.png), thumbnail [landmark](thumbnails/sambas-landmark.webp) dan [balapan](thumbnails/sambas-race.webp).

Overview adalah kamera review atas dengan fog geometri dimatikan **hanya saat capture** agar keseluruhan rute terbaca. Screenshot lain memakai atmosfer game biasa; konfigurasi ini tidak mengubah gameplay atau langit distribusi.

HTML **24.504.400 byte**; Prompt 5 **24.445.403 byte**. Pertumbuhan **58.997 byte**, sisa target 25.000.000 byte **495.600 byte**. Dua thumbnail asli berjumlah **33.622 byte** sebelum base64. Tidak ada model atau poster duplikat.

Batch lingkungan Sambas: **76.634 segitiga**, **20 colour draw calls**, **11 shadow batch calls**, satu tekstur label kecil hasil canvas. Terrain 2.400 dan sungai 160 segitiga terpisah; jalan/shoulder/curb memakai pipeline bersama. Draw call seluruh frame tentu mencakup model, item dan HUD tambahan. Pada 12 sampel cuaca cerah: high 116–217 colour / 21–65 shadow calls; low 100–202 colour / 0 shadow calls. Penghitungan `drawPrimitive` tersebut tidak mencakup dua panggilan gradient/cloud langsung. Detail lengkap di [`asset-metrics.json`](asset-metrics.json). Tidak mengklaim seluruh lingkungan mempunyai LOD geometri: batch static tetap, sedangkan kualitas mengatur LOD karakter, bayangan, jarak fitur dan awan sebagaimana baseline. Waktu/frame dan memori perangkat belum diukur.

Distribusi tetap satu HTML dengan aset tertanam, dipaketkan dalam ZIP. Tidak ada CDN, backend, atau server wajib baru. Offline diuji dengan jaringan dinonaktifkan dan dokumen lokal disuplai harness pada localhost; pembatasan `file://` berasal dari kebijakan browser cloud. Validasi buka langsung file pada browser target masih perlu dilakukan di luar cloud; tidak membuat paket aset `fetch()` lokal yang belum teruji. CRC/kesamaan byte HTML kedua ZIP dicatat di [`release-metrics.json`](release-metrics.json).
