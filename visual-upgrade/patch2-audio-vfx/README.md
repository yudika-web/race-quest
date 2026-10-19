# RACE QUEST PRO — PATCH 2: Audio & VFX

[HTML playable](../race-quest-pro-patch2.html) · [ZIP playable](../../race-quest-pro-patch2-playable.zip) · [ZIP review](../../race-quest-pro-patch2-review.zip)

Unduh ZIP playable, ekstrak, lalu buka `race-quest-pro-patch2.html` di browser yang mendukung WebGL dan Web Audio. Klik/sentuh tombol untuk mengaktifkan audio. Seluruh aset sudah tertanam, tanpa CDN atau unduhan saat bermain. Pengaturan **Suara → Audio Arcade** menyediakan Master, Musik, SFX, trim Mesin, Mute, Kurangi suara intens dan Reduced Effects. Pengaturan dipulihkan dari penyimpanan lokal; profil, bank, harga unlock dan progres tidak diubah.

Baseline: PATCH 1 `7fbb3080ce20ad44e5ca4c32bacbdaec062c400e` pada branch `dev/race-quest-cat-sport-visual-upgrade`. Tidak mengganti `index.html`, merge main atau melakukan deployment.

## Audit dan pemakaian ulang audio

Terdapat **14 berkas OGG/Vorbis** (3 musik + 11 SFX), total **2.233.600 byte**. Semuanya dipertahankan byte-identik di JSON aset yang sama. Durasi, codec, channel, SHA-256 dan keputusan per berkas tersedia pada [audio-audit.json](audio-audit.json).

| Audio lama | Keputusan PATCH 2 |
|---|---|
| `music_menu.ogg` — 60 detik | Dipakai di home, guru, garasi dan hasil. Tidak restart saat berpindah di antara menu tersebut. |
| `music_race.ogg` — 90 detik | Dipakai ketiga stage. Sumber yang sama tetap berjalan saat pause/soal, dengan volume lebih rendah. |
| `music_mission.ogg` — 45 detik | Aset tetap tersedia; tidak lagi mengganti musik setiap soal terbuka. |
| `sfx_engine.ogg` — 3 detik | Loop lama, pitch dan amplitudo mengikuti kecepatan secara halus. Idle terdengar saat balapan pada kecepatan rendah. |
| `sfx_click.ogg` | Tetap untuk navigasi umum. Pilihan karakter/stage mendapat motif singkat tersendiri. |
| `sfx_countdown.ogg` | Tetap untuk 3–2–1. GO memakai resep baru. |
| `sfx_correct.ogg`, `sfx_retry.ogg`, `sfx_mission.ogg` | Tetap untuk jawaban benar, salah dan pembukaan soal. Tidak ada loop yang mengganggu membaca. |
| `sfx_collision.ogg` | Dipakai untuk benturan ringan; benturan berat memakai sintesis berbeda. |
| `sfx_pickup.ogg` | Dipicu pengumpulan token sebenarnya, termasuk ketika magnet aktif. Ada pembatas frekuensi. |
| `sfx_turbo.ogg` | Dipakai pada awal Turbo yang benar-benar aktif. Sustain/akhir memakai sintesis baru. |
| `sfx_finish.ogg` | Dipakai saat juara. Hasil non-juara memakai motif penyelesaian yang lebih tenang. |
| `sfx_skid.ogg` | Tetap tersimpan; pengoperasian drift memakai loop noise terfilter yang lebih mudah dikendalikan. |

Tidak ada berkas audio baru yang disematkan, tidak mengambil sampel dari internet dan tidak menduplikasi berkas lama. Audio baru adalah **sintesis Web Audio sederhana yang dirancang untuk arcade**, bukan rekaman atau produksi studio profesional. Evaluasi perangkat/speaker fisik tetap diperlukan sebelum menilai keseimbangan akhir.

## Audio baru dan perubahan dinamis

[Preview Opus/OGG](audio-review/arcade-sfx-preview.ogg) berisi resep yang sama dengan runtime, berurutan setiap 0,9 detik. Versi WAV dan generator tersedia untuk review; keduanya **tidak** disematkan ke HTML.

| Urutan | Resep | Pemicu |
|---:|---|---|
| 1 | `jump` | Lepas landas lewat jump/ramp. |
| 2 | `land` | Mendarat; intensitas lebih rendah bila mulus. |
| 3 | `heavy` | Rintangan/rescue atau benturan dengan kehilangan kecepatan besar. |
| 4–5 | `bubble_fire`, `bubble_hit` | Item benar-benar dipakai / proyektil benar-benar mengenai target. |
| 6–7 | `oil_drop`, `oil_slip` | Oli benar-benar dipasang / target benar-benar tergelincir. |
| 8–9 | `shield_on`, `shield_block` | Perisai aktif / perisai benar-benar dikonsumsi untuk menangkis. |
| 10 | `magnet_on` | Magnet dipakai. Token tetap menggunakan SFX pickup lama. |
| 11 | `turbo_end` | Durasi Turbo berakhir. |
| 12 | `go` | Countdown beralih ke balapan. |
| 13 | `rank_up` | Peringkat balapan membaik, dengan cooldown. |
| 14 | `level_up` | Level profil hasil award benar-benar naik. |
| 15 | `result` | Selesai balapan tanpa menjadi juara. |
| 16–17 | `character`, `stage` | Pilihan pembalap dan kartu arena. |

Drift memakai loop seeded noise band-pass yang menyesuaikan kecepatan/steering serta berhenti ketika tidak lagi drift/rem/meluncur. Turbo memiliki awal OGG, sustain terfilter mengikuti kecepatan dan akhir pendek. Jump, landing, benturan dan hit diamati dari hasil simulasi. Jika satu hasil event tertimpa event lain pada langkah yang sama, perubahan cooldown benturan atau status air menangkap peristiwa yang benar-benar terjadi; aksi reset tidak dianggap tabrakan. Tidak mengubah `Session.advance`, aturan buff atau AI.

Hit pada lawan di dekat pemain memakai intensitas 38%; hit yang jauh (>45 satuan lintasan) tidak ikut meramaikan audio. Tidak menambahkan mesin untuk setiap lawan.

Routing memakai satu AudioContext, bus musik/mesin/SFX balapan/UI, Master dan compressor. Musik soal/feedback menuju 20% dari volume musik, pause 30%; resume kembali dengan ramp. Loop balapan dan transient balapan dihentikan saat pause/soal, sedangkan cue soal/jawaban tetap dapat dimainkan. Pindah track memakai crossfade singkat dengan maksimum dua sumber musik; request track yang sama tidak membuat ulang loop. Visibility/background menangguhkan context dan mempertahankan posisi musik. Aktivasi dicoba lagi pada interaksi pengguna jika context tertunda oleh browser.

Pengaturan suara lama dimigrasikan dengan default tambahan, tetap pada `race_quest_audio_v1`. Master mengendalikan semua kanal, SFX juga mengendalikan mesin, dan trim Mesin memberi penyesuaian tambahan. **Kurangi suara intens** menurunkan noise/transient keras dan membatasi voice menjadi 5. Mute/Master nol menolak SFX baru serta menghentikan sumber balapan; musik yang sedang berjalan dapat tetap senyap untuk menjaga posisi.

## VFX

- Partikel berbentuk kotak dengan tepi lembut, bukan glow putih besar. Shader tetap memakai batch point yang sama. Blending warna mempertahankan alpha canvas agar partikel/perisai tidak memperlihatkan UI di bawahnya; minimum alpha frame diperiksa pada render hasil patch.
- Jejak ban dan debu mengikuti kondisi rem/drift/off-road; drift yang terisi memberi percikan cyan ringan.
- Trail Turbo dua sisi, burst awal dan perubahan FOV lebih kecil. Frekuensi pulse knalpot lama diturunkan dari 55 ke 9 Hz dengan amplitudo lebih kecil.
- Burst jump/landing dan percikan benturan; warna berbeda untuk hit gelembung/oli/perisai.
- Gelembung meninggalkan partikel ringan. Perisai menambah selubung segi delapan transparan, sambil mempertahankan ring indikator lama. Magnet dan token mendapat aksen ringan.
- Confetti kotak hanya untuk kemenangan baru, satu kali; hasil non-juara dan membuka riwayat tidak memicu confetti kemenangan.
- Jawaban benar/salah mendapat border dan transisi singkat, tanpa partikel menutupi soal.

**Reduced Effects** (juga menghormati `prefers-reduced-motion`) menghilangkan speed lines, jitter kamera, flame pulse dan confetti, mengurangi debu/trail, membatasi partikel ke 32 serta mematikan animasi feedback. Indikator dasar item, proyektil dan perisai tetap terbaca. Ini pengaturan visual, tidak mengubah kecepatan, durasi buff atau hasil jawaban.

Semua partikel dunia memakai `Session.elapsed`. Saat pause/soal, posisi, usia dan animasinya berhenti. Renderer tidak membuat timer dunia baru. Confetti/feedback adalah animasi UI terbatas durasi, bukan simulasi kendaraan.

## Bukti render

Semua gambar diambil dari renderer/UI game asli. State/input untuk perbandingan diberikan melalui fixture pengujian, seed, jumlah langkah dan pose yang setara; bukan mockup. FOV Turbo berubah karena memang bagian efek patch ini.

- Before–after: [drift](comparisons/comparison-drift.jpg), [Turbo](comparisons/comparison-turbo.jpg), [perisai](comparisons/comparison-shield.jpg), [gelembung](comparisons/comparison-bubble.jpg), [landing](comparisons/comparison-landing.jpg), [benturan](comparisons/comparison-impact.jpg).
- Pengaturan: [desktop](screenshots/audio-desktop.png), [HP](screenshots/audio-mobile.png).
- Jawaban: [desktop](screenshots/feedback-desktop.png), [HP](screenshots/feedback-mobile.png); pengujian benar/salah juga disimpan pada `answer-*`.
- Kemenangan dengan confetti: [desktop](screenshots/victory-desktop.png), [HP](screenshots/victory-mobile.png).
- Reduced Effects: [desktop](screenshots/reduced-desktop.png), [HP](screenshots/reduced-mobile.png).

## Anggaran dan ukuran

| Komponen | Terukur / batas |
|---|---:|
| HTML PATCH 1 | 23.613.758 byte |
| HTML PATCH 2 | 23.638.560 byte |
| Pertumbuhan | **24.802 byte (~0,105%)** |
| Audio embedded tambahan | **0 berkas / 0 byte** |
| Resep sintesis baru | 17 + dua loop noise dinamis |
| Transient voice simultan | Maks. 8; mode suara ringan 5 |
| Pool partikel | 480 slot yang digunakan ulang |
| High / medium / low aktif | Maks. 320 / 200 / 80 |
| Reduced Effects aktif | Maks. 32 |
| Buffer CPU atribut partikel lama | 15.360 byte, tetap digunakan |
| Batch partikel | Maks. dua submisi point seperti pipeline lama |
| Selubung perisai baru | 16 segitiga / satu draw tambahan saat aktif; mesh di-cache |

HTML tetap di bawah 25 MB desimal. Ukuran ZIP, SHA dan metrik per screenshot ada di `release-metrics.json` / `vfx-capture-report.json`. Preview audio memakai Opus sebagai aset review saja. Audio runtime memakai decode lazy dan cache berkas lama; tidak mendekode semua musik pada startup. Uji khusus mendekode 14 aset untuk memeriksa kompatibilitas dan mencatat PCM; itu bukan ukuran heap normal permainan. Jumlah sumber aktif puncak yang diamati dilaporkan per perangkat uji, bukan estimasi FPS/performa HP fisik.

## Pengujian

Paket dibuat hanya ketika seluruh laporan wajib `passed`.

- `scope-verification.json`: **1.554 file historis** dan **94 aset embedded** tetap identik; core/AI/buff/stage/model/avatar tidak berubah. Menghapus penambahan presentasi dan membalik hook terdokumentasi menghasilkan baseline persis.
- `av-tests.json`: 69 pemeriksaan desktop/HP mencakup gesture audio, penyimpanan/mute, PCM graph tidak senyap, pitch idle–akselerasi–deselerasi, 3–2–1–GO, jump/landing, drift, kelima item dan hit aktual, perisai, token, akhir Turbo, pause/soal/resume, jawaban benar/salah, reduced effects, cap voice, cleanup, kemenangan serta hasil non-juara. Slot/posisi/countdown untuk mempercepat cakupan adalah fixture browser saja. HP menggunakan touch emulation; keyboard juga dipakai untuk gerakan terkontrol.
- `budget-tests.json`: seluruh 14 Vorbis berhasil di-decode Chromium; cap 5 voice; 100 permintaan efek selesai tanpa voice tertinggal; request musik berulang tidak restart; 2.000 permintaan partikel pada tiap kualitas kembali ke 480 slot bebas; mute dan dispose; fallback HTMLAudio tanpa AudioContext. Parameter bus yang tidak mempunyai sumber aktif tidak dipakai sebagai bukti volume; penghentian sumber diperiksa langsung.
- `stage-audio-tests.json`: ketiga kartu stage memuat arena sebenarnya, musik race/engine aktif, kembali ke menu dengan benar dan pool tetap utuh.
- `test-results.json` / `offline-test-results.json`: regresi bank soal, A/D, jump/landing, touch, kuis/buff/pause/resume, LOD dan gameplay offline tanpa request aset HTTP.
- `core-test-results.json`: CSV/JSON, materi/jumlah soal, AI difficulty, GP gating/retry/tiga putaran deterministik, drift/jump/kuis/buff, hasil, ghost dan progres.
- `export-tests.json`: ekspor guru mempertahankan seluruh model/audio/thumbnail, dapat dimainkan offline, kartu Singkawang benar dan tidak menggandakan thumbnail.
- `unchanged-renders.json`: 14 pasangan, cat low dan mobil Sport saja identik piksel pada pose/cahaya tetap. VFX dunia sengaja berubah; tidak mengklaim seluruh frame balapan identik.
- `synthesis-metrics.json`: 17 resep dirender melalui OfflineAudioContext, RMS >0 dan tidak clipping pada preview. Ini pemeriksaan sinyal, bukan penilaian speaker/manusia.
- `smoke-tests.json`, `vfx-capture-report.json`, `ui-capture-report.json`: shader, WebGL dan screenshot aktual.

Batas pengujian: Chromium cloud / software WebGL, desktop serta viewport/touch HP; **belum diuji pada HP atau speaker/headphone fisik**, Safari/Firefox, atau sesi panjang. Tidak mengklaim FPS perangkat nyata, kualitas produksi audio profesional, atau menyelesaikan Grand Prix manual penuh. Direct `file://` diblokir kebijakan browser cloud; uji offline menggunakan HTML lokal yang dipenuhi langsung ke context tanpa jaringan dan menolak semua request aset. Browser tanpa Web Audio memakai HTMLAudio untuk aset lama; motif sintesis dipetakan ke SFX lama dan loop sintesis tidak tersedia. Browser yang tidak mendukung decode OGG/Vorbis memerlukan uji kompatibilitas audio lebih lanjut; semua berkas berhasil di Chromium pada uji ini.

## Sumber dan build

Sumber utama: `source/audio.js`, `source/vfx.js`, `source/ui.css` dan `source/assemble.py`. Assembler membaca HTML PATCH 1; tidak menyalin engine ke sumber terpisah. `bounded-changes.json` mencatat perubahan UI/audio dan satu ekspresi pulse visual pada renderer lama. Tidak ada aset model baru.

```bash
# Root repository; runtime Node/Playwright, Python/Pillow, ffmpeg dan Chromium tersedia.
python visual-upgrade/patch2-audio-vfx/source/assemble.py
python visual-upgrade/patch2-audio-vfx/source/verify_scope.py
python -m http.server 8000 --bind 127.0.0.1
# Terminal lain ketika server hidup:
node visual-upgrade/patch2-audio-vfx/source/render_audio.cjs
ffmpeg -v error -y -i visual-upgrade/patch2-audio-vfx/audio-review/arcade-sfx-preview.wav -c:a libopus -b:a 80k visual-upgrade/patch2-audio-vfx/audio-review/arcade-sfx-preview.ogg
node visual-upgrade/patch2-audio-vfx/source/test_av.cjs
node visual-upgrade/patch2-audio-vfx/source/test_budgets.cjs
node visual-upgrade/patch2-audio-vfx/source/test_stages.cjs
node visual-upgrade/patch2-audio-vfx/source/test_core.cjs
node visual-upgrade/patch2-audio-vfx/source/test_game.cjs
node visual-upgrade/patch2-audio-vfx/source/test_export.cjs
node visual-upgrade/patch2-audio-vfx/source/test_unchanged_render.cjs
node visual-upgrade/patch2-audio-vfx/source/test_smoke.cjs
node visual-upgrade/patch2-audio-vfx/source/capture_vfx.cjs
node visual-upgrade/patch2-audio-vfx/source/capture_ui.cjs
python visual-upgrade/patch2-audio-vfx/source/make_comparisons.py
python visual-upgrade/patch2-audio-vfx/source/package.py
```

Path absolut Playwright dan executable Chromium di skrip mengikuti runtime cloud ini; sesuaikan bila menggunakan environment lain. Server hanya dibutuhkan pipeline pengembangan/pengujian, bukan untuk memainkan hasil HTML.
