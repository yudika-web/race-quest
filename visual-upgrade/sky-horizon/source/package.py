from pathlib import Path
import json,hashlib,zipfile
from PIL import Image,ImageDraw,ImageFont
D=Path(__file__).resolve().parents[2];B=D/'sky-horizon';R=D.parent;H=D/'race-quest-pro-sky-horizon.html'
required=['scope-tests','sky-tests','capture-tests','controls-tests','engine-parity','core-test-results','stage-audio-tests','export-tests','offline-test-results','unchanged-renders']
reports={n:json.loads((B/(n+'.json')).read_text())for n in required}
for n,v in reports.items():assert v['status']=='passed',n
raw=H.read_bytes();sha=lambda x:hashlib.sha256(x).hexdigest();scope=reports['scope-tests'];assert sha(raw)==scope['html_sha256']
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22)
for id,name,view in [('kampung','pontianak','normal'),('kapuas','mempawah','normal'),('hutan','singkawang','open')]:
 a=Image.open(B/f'screenshots/before-{id}-{view}.png').convert('RGB');b=Image.open(B/f'screenshots/after-{id}-{view}.png').convert('RGB');assert a.size==b.size
 img=Image.new('RGB',(a.width*2+16,a.height+48),'#112c40');d=ImageDraw.Draw(img);d.text((14,12),name.upper()+' - SEBELUM PATCH 4.5',fill='white',font=font);d.text((a.width+30,12),name.upper()+' - SESUDAH SKY / HORIZON',fill='white',font=font);img.paste(a,(0,48));img.paste(b,(a.width+16,48));img.save(B/f'screenshots/comparison-{name}.jpg',quality=93)
metrics={**{k:scope[k]for k in ['baseline_commit','html_bytes','baseline_bytes','growth_bytes','html_sha256','under_25_decimal_MB','protected_historical_files']},'sky':reports['sky-tests']['metrics']['stats'],'baseline_sky_draw_calls':1,'additional_draw_calls':1,'additional_vertex_index_buffers':2,'additional_shader_programs':1,'new_embedded_assets':0,'sky_textures_uploaded':0,'baseline_sky_textures_uploaded':2,'old_embedded_sky_asset_bytes_preserved':True,'renderer_motion_samples':sum(x['steps']for x in reports['sky-tests']['motion']),'complete_paired_races':reports['engine-parity']['cases'],'unchanged_model_pixel_comparisons':len(reports['unchanged-renders']['checks']),'teacher_export_bytes':reports['export-tests']['export_bytes'],'physical_phone_tested':False,'FPS_measured':False,'GPU_frame_time_measured':False,'direct_file_scheme_tested':False}
(B/'asset-metrics.json').write_text(json.dumps(metrics,indent=2))
notes='''RACE QUEST PRO — BLOCKY SKY & CLEAN HORIZON

Ekstrak ZIP, lalu buka race-quest-pro-sky-horizon.html di browser WebGL. Semua aset tertanam, playable offline, tanpa CDN. Klik/sentuh untuk mengaktifkan audio.

Langit gradient tanpa sambungan, awan blocky berbevel dan haze horizon yang menyatu. Tiga nuansa stage; tidak ada perubahan lintasan, AI, buff, kuis, kontrol atau skor akademik. HUD PATCH 4.5 dipertahankan.

E/Spasi pakai buff; Q/1/2 pilih slot; A/D kemudi; W/S gas/rem; C drift; Shift loncat; P/Esc jeda. Kontrol sentuh dapat diatur Otomatis/Tampilkan/Sembunyikan di Suara/Pause. Gunakan kualitas Low bila perangkat memerlukannya.

ZIP review berisi sumber, screenshot before-after asli dan laporan tes. HP diuji melalui emulasi, bukan perangkat fisik. Tidak ada klaim FPS HP. File:// diblokir browser cloud; offline diuji dengan jaringan dimatikan dan HTML lokal disuplai langsung.
'''
for kind in ['playable','review']:
 dest=R/f'race-quest-pro-sky-horizon-{kind}.zip'
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
  z.write(H,H.name);z.writestr('MULAI.txt',notes)
  if kind=='review':
   for f in sorted(B.rglob('*')):
    if f.is_file()and '__pycache__'not in f.parts and f.name!='release-metrics.json':z.write(f,'sky-horizon/'+f.relative_to(B).as_posix())
 with zipfile.ZipFile(dest)as z:assert z.testzip()is None;assert z.read(H.name)==raw
 metrics[kind+'_zip']={'file':dest.name,'bytes':dest.stat().st_size,'sha256':sha(dest.read_bytes())}
(B/'release-metrics.json').write_text(json.dumps(metrics,indent=2));print(json.dumps(metrics,indent=2))
