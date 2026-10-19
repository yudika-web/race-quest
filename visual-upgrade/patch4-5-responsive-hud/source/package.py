from pathlib import Path
import json,hashlib,zipfile
from PIL import Image,ImageDraw,ImageFont
D=Path(__file__).resolve().parents[2];B=D/'patch4-5-responsive-hud';R=D.parent;H=D/'race-quest-pro-patch4-5.html'
required=['scope-tests','layout-tests','controls-tests','input-edge-tests','dialog-tests','before-captures','engine-parity','core-test-results','ai-tests','personality-tests','stage-audio-tests','export-tests','offline-test-results','persistence-tests','unchanged-renders']
reports={n:json.loads((B/(n+'.json')).read_text()) for n in required}
for n,d in reports.items():assert d['status']=='passed',n
raw=H.read_bytes();sha=lambda x:hashlib.sha256(x).hexdigest();scope=reports['scope-tests'];assert scope['html_sha256']==sha(raw)
# Side-by-side composites use only original browser screenshots, unretouched.
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20)
for size in ['1821x831','1366x768','390x844','844x390']:
 a=Image.open(B/f'screenshots/before-{size}-active.png').convert('RGB');b=Image.open(B/f'screenshots/after-{size}-active.png').convert('RGB');assert a.size==b.size
 canvas=Image.new('RGB',(a.width*2+16,a.height+44),'#102739');draw=ImageDraw.Draw(canvas);draw.text((12,10),'SEBELUM - PATCH 4',fill='white',font=font);draw.text((a.width+28,10),'SESUDAH - PATCH 4.5',fill='white',font=font);canvas.paste(a,(0,44));canvas.paste(b,(a.width+16,44));canvas.save(B/f'screenshots/comparison-{size}.jpg',quality=92)
perf=reports['input-edge-tests']['performance'];metrics={**{k:scope[k] for k in ['baseline','html_sha256','html_bytes','growth_bytes','under_25_decimal_MB','protected_historical_files']},'baseline_bytes':json.loads((B/'baseline.json').read_text())['bytes'],'new_embedded_assets':0,'new_GPU_buffers':0,'additional_WebGL_draw_calls':0,'layout_cases':len(reports['layout-tests']['cases']),'viewport_sizes':9,'minimum_racing_button_css_px':44,'paired_complete_races':reports['engine-parity']['cases'],'unchanged_render_cases':len(reports['unchanged-renders']['checks']),'teacher_export_bytes':reports['export-tests']['export_bytes'],'HUD_JS_microbenchmark':{**perf,'mean_js_ms':perf['total_js_ms']/perf['calls']},'FPS_measured':False,'physical_phone_tested':False,'direct_file_scheme_tested':False}
(B/'asset-metrics.json').write_text(json.dumps(metrics,indent=2))
notes='''RACE QUEST PRO — PATCH 4.5 RESPONSIVE HUD

Ekstrak ZIP, lalu buka race-quest-pro-patch4-5.html di browser modern dengan WebGL. Semua aset tertanam; tidak membutuhkan CDN/internet. Klik/sentuh untuk mengaktifkan audio.

Inventori dua slot di kiri bawah; E / Spasi untuk memakai, Q / 1 / 2 untuk memilih. A/D atau panah untuk kemudi, W/S gas/rem, C drift, Shift loncat, P/Esc jeda. R mengembalikan kart ke jalur. Tombol restart pada toolbar mengulang balapan setelah konfirmasi.

Desktop menyembunyikan tombol sentuh. HP menampilkannya. Ubah Kontrol Sentuh: Otomatis / Selalu tampilkan / Sembunyikan melalui Suara atau Pause. Pilihan disimpan lokal. Tombol PETA membuka/menutup minimap; landscape pendek mulai dengan peta ringkas. Daftar kontrol dan deskripsi buff berada di Pause.

PATCH 4 Smart Racing AI, seluruh aturan buff, soal, penilaian, 14 model, 3 arena dan progres dipertahankan. Soal dan Pause membekukan simulasi. Pilihan HUD terpisah dari data belajar.

Bukti pengujian dan screenshot asli tersedia di ZIP review. Pengujian HP berupa emulasi; bukan pengujian perangkat fisik atau FPS HP. Browser cloud memblokir file://; offline diuji dengan jaringan dimatikan dan HTML lokal disuplai langsung ke browser.
'''
for kind in ['playable','review']:
 dest=R/f'race-quest-pro-patch4-5-{kind}.zip'
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
  z.write(H,H.name);z.writestr('MULAI.txt',notes)
  if kind=='review':
   for f in sorted(B.rglob('*')):
    if f.is_file()and '__pycache__'not in f.parts and f.name!='release-metrics.json':z.write(f,'patch4-5-responsive-hud/'+f.relative_to(B).as_posix())
 with zipfile.ZipFile(dest)as z:assert z.testzip()is None;assert z.read(H.name)==raw
 metrics[kind+'_zip']={'file':dest.name,'bytes':dest.stat().st_size,'sha256':sha(dest.read_bytes())}
(B/'release-metrics.json').write_text(json.dumps(metrics,indent=2));print(json.dumps(metrics,indent=2))
