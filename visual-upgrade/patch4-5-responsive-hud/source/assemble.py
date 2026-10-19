from pathlib import Path
import re,json,hashlib
D=Path(__file__).resolve().parents[2];B=D/'patch4-5-responsive-hud';base=(D/'race-quest-pro-patch4.html').read_text();h=base;changes=[]
(B/'baseline.json').write_text(json.dumps({'commit':'82c0f778b480d669b236b76517add5cd86e35fb2','bytes':len(base.encode()),'sha256':hashlib.sha256(base.encode()).hexdigest()},indent=2))
def change(old,new):
 global h
 assert h.count(old)==1,(old[:100],h.count(old));offset=h.index(old);h=h.replace(old,new);changes.append({'offset':offset,'old':old,'new':new})
for id in ['patch3Styles','patch4Styles']:
 m=re.search(r'<style id="'+id+r'"[^>]*>.*?</style>',h,re.S);assert m;change(m[0],'')
m=re.search(r'<section id="race"[^>]*>.*?</section>',h,re.S)
change(m[0],(B/'source/race.html').read_text().strip())
change('RaceBuffUI.update(s);RaceAIUI.update(s);','RaceBuffUI.update(s);RaceAIUI.update(s);RaceHUD.update(s);')
old="function raceNotice(text,duration=2400){$('raceNotice').textContent=text;$('raceNotice').hidden=false;clearTimeout(state.noticeTimer);state.noticeTimer=setTimeout(()=>$('raceNotice').hidden=true,duration)}"
change(old,'function raceNotice(text,duration=2400){RaceHUD.notify(text,duration,state.session)}')
old="function clearControls(){for(let k in controls)controls[k]=false;document.querySelectorAll('.touch-btn').forEach(b=>b.classList.remove('down'))}"
change(old,old+'RaceHUD.bind(clearControls);')
change("clone.querySelector('#initialData').textContent=", "RaceHUD.cleanExport(clone);clone.querySelector('#initialData').textContent=")
control=lambda id:'<label class="field hud-control-choice"><span>Kontrol sentuh</span><select id="'+id+'"><option value="auto">Otomatis · sesuai perangkat/input</option><option value="show">Selalu tampilkan</option><option value="hide">Sembunyikan · pakai keyboard</option></select></label>'
help='<details class="hud-help"><summary>Kontrol dan bantuan buff</summary><p>WASD / panah: kemudi, gas, rem · C: drift · Shift: loncat · Q / 1 / 2: pilih slot · E / Spasi: pakai · R: kembali ke jalur · P / Esc: jeda. Gamepad: stik kiri, RT/LT gas/rem, A loncat, B drift, X item. Minimap dapat dibuka/ditutup melalui tombol PETA.</p><div id="buffDetails"></div><p>Jawaban benar memberi hadiah. Jika dua slot penuh, pilih item yang diganti atau lewati hadiah baru. Seluruh simulasi berhenti ketika soal atau jeda terbuka.</p></details>'
change('<h3>Tampilan &amp; Akses</h3>','<h3>Tampilan &amp; Akses</h3>'+control('hudTouchMode')+'<p class="small muted" id="hudControlStatus">Pilihan HUD disimpan pada perangkat ini.</p>')
pause=re.search(r'<dialog id="pauseDialog"[^>]*>.*?</dialog>',h,re.S)[0]
change(pause,pause.replace('</div></div></dialog>','</div>'+control('pauseTouchMode')+help+'</div></dialog>'))
(B/'bounded-changes.json').write_text(json.dumps(changes,indent=2,ensure_ascii=False))
h=h.replace('</head>','<style id="patch45HUDStyles">'+(B/'source/hud.css').read_text()+'</style></head>',1)
s=list(re.finditer(r'<script\b[^>]*>(.*?)</script>',h,re.S));pos=s[18].end();block='\n<script id="patch45HUD">'+(B/'source/hud.js').read_text()+'</script>'
h=h[:pos]+block+h[pos:];out=D/'race-quest-pro-patch4-5.html';out.write_text(h);print('PATCH 4.5',out.stat().st_size,'bytes')
