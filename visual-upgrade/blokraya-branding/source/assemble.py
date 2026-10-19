from pathlib import Path
import re,json,hashlib,base64
from PIL import Image,ImageOps
D=Path(__file__).resolve().parents[2];B=D/'blokraya-branding'
posters={};metrics=[]
for orientation,limit in [('landscape',1440),('portrait',900)]:
 original=B/'assets'/('poster-'+orientation+'-original.webp')
 if not original.exists():
  raise SystemExit('Original user attachment required: '+str(original)+'; no replacement poster will be generated.')
 im=ImageOps.exif_transpose(Image.open(original)).convert('RGB');w,h=im.size
 assert(w>h)==(orientation=='landscape'),orientation+' orientation mismatch'
 if w>limit:im=im.resize((limit,round(h*limit/w)),Image.Resampling.LANCZOS)
 dest=B/'assets'/('poster-'+orientation+'.webp');im.save(dest,'WEBP',quality=82,method=6)
 content=dest.read_bytes();posters[orientation]='data:image/webp;base64,'+base64.b64encode(content).decode();metrics.append(dict(orientation=orientation,original_bytes=original.stat().st_size,original_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),optimized_bytes=len(content),size=im.size,sha256=hashlib.sha256(content).hexdigest()))
base=(D/'race-quest-pro-sky-horizon.html').read_text();h=base;changes=[]
def change(old,new,count=1):
 global h
 assert h.count(old)==count,(old[:80],h.count(old));offset=h.index(old);h=h.replace(old,new);changes.append(dict(offset=offset,old=old,new=new,count=count))
change('<title>RACE QUEST — Balapan &amp; Belajar</title>','<title>BlokRaya — Balap Edukasi Nusantara</title>') if '<title>RACE QUEST — Balapan &amp; Belajar</title>'in h else change('<title>RACE QUEST — Balapan & Belajar</title>','<title>BlokRaya — Balap Edukasi Nusantara</title>')
change('<div class="brand">RACE <em>QUEST</em></div>','<div class="brand" aria-label="BlokRaya — Balap Edukasi Nusantara">Blok<em>Raya</em><small class="br-subtitle">Balap Edukasi Nusantara</small></div>',4)
change("c.fillText('RACE QUEST',512,137)","c.fillText('BlokRaya',512,137)")
change("c.fillText('PERFORMANCE GARAGE  /  PIT 01',512,199)","c.fillText('BALAP EDUKASI NUSANTARA',512,199)")
change('Gunakan hasil ekspor RACE QUEST.','Gunakan hasil ekspor BlokRaya atau RACE QUEST.')
change('RACE QUEST — HASIL BALAPAN DAN JAWABAN','BLOKRAYA — HASIL BALAPAN DAN JAWABAN')
# Runtime storage keys intentionally remain race_quest_* for backward compatibility.
for old,new in [("download('race_quest_","download('blokraya_"),("download('template_soal_race_quest.csv'","download('template_soal_blokraya.csv'")]:
 if old in h:change(old,new,h.count(old))
old=re.search(r'<div class="loading-screen" id="loading".*?</div></div>',h,re.S)[0];change(old,'')
# Boot overlay precedes the large embedded assets/scripts, rather than opening only at garage entry.
boot=(B/'source/loading.html').read_text()+'\n<script id="blokRayaPosters" type="application/json">'+json.dumps(posters,separators=(',',':'))+'</script>\n<script id="blokRayaLoading">'+(B/'source/loading.js').read_text()+'</script>\n'
body=re.search(r'<body[^>]*>',h)[0];change(body,body+'\n'+boot)
change('</head>','<style id="blokRayaBranding">'+(B/'source/branding.css').read_text()+'</style></head>')
# Existing data-URI texture lifecycle now exposes actual readiness to the loading UI.
change('im.src=uri;this.textureList.push(t);return t','BlokRayaLoading.trackImage(im);im.src=uri;this.textureList.push(t);return t')
old=re.search(r'async function ensureRenderer\(\).*?\nasync function garage',h,re.S)[0][:-len('\nasync function garage')]
new="""async function ensureRenderer(){if(state.renderer)return true;const token=BlokRayaLoading.begin('Menyiapkan tampilan 3D…');await BlokRayaLoading.paint();try{state.renderer=new RaceRenderer($('world'),ASSETS);state.renderer.setQuality(preferences.quality);state.renderer.garage(state.character,0);await BlokRayaLoading.waitImages('Memuat material dan pembalap…');await BlokRayaLoading.finish(token,()=>state.renderer.garage(state.character,0));return true}catch(e){await BlokRayaLoading.finish(token);$('webglError').textContent=e.message;$('webglError').hidden=false;$('startRaceBtn').disabled=true;toast(e.message);return false}}"""
change(old,new)
old="$('loading').hidden=false;await new Promise(r=>setTimeout(r,35));state.renderer.buildWorld(state.session.track);$('loading').hidden=true;"
new="const loadingToken=BlokRayaLoading.begin('Menyiapkan arena…');await BlokRayaLoading.paint();try{state.renderer.buildWorld(state.session.track);state.renderer.race(state.session,0);await BlokRayaLoading.waitImages('Memuat material arena…');await BlokRayaLoading.finish(loadingToken)}catch(e){await BlokRayaLoading.finish(loadingToken);throw e};"
change(old,new)
change("showScreen('race');clearControls();drawMinimap();syncAudio();","showScreen('race');state.renderer.race(state.session,0);clearControls();drawMinimap();syncAudio();")
change("RaceHUD.cleanExport(clone);clone.querySelector('#initialData')","RaceHUD.cleanExport(clone);BlokRayaLoading.cleanExport(clone);clone.querySelector('#initialData')")
change("showScreen('home');if(loadError)","showScreen('home');BlokRayaLoading.bootReady();if(loadError)")
dest=D/'blokraya-balap-edukasi-nusantara.html';dest.write_text(h);(B/'bounded-changes.json').write_text(json.dumps(changes,indent=2));(B/'poster-metrics.json').write_text(json.dumps(metrics,indent=2));print('HTML',dest.stat().st_size,'bytes; growth',len(h.encode())-len(base.encode()))
