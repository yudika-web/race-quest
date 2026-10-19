"""PATCH 2 adds presentation hooks only; starts from the committed PATCH 1 HTML."""
from pathlib import Path
import hashlib,json,re
D=Path(__file__).resolve().parents[2];B=D/'patch2-audio-vfx';base=(D/'race-quest-pro-patch1.html').read_text();h=base;changes=[]
meta={'baseline_commit':'7fbb3080ce20ad44e5ca4c32bacbdaec062c400e','html_bytes':len(base.encode()),'html_sha256':hashlib.sha256(base.encode()).hexdigest()};(B/'baseline.json').write_text(json.dumps(meta,indent=2))
def change(old,new):
 global h
 assert h.count(old)==1,(old[:90],h.count(old));h=h.replace(old,new);changes.append({'old':old,'new':new})
scripts=list(re.finditer(r'<script\b[^>]*>(.*?)</script>',h,re.S));app=scripts[12][1];begin=app.index('class AudioSystem{');end=app.index('\nconst sound=new AudioSystem();',begin);change(app[begin:end],'const AudioSystem=RaceArcadeAudio;')
change('const sound=new AudioSystem();', 'const sound=new AudioSystem(uri,AUDIO_STORAGE);RacePatchAV.attach(sound);')
change("document.addEventListener('pointerdown',()=>sound.unlock(),{once:true});document.addEventListener('keydown',()=>sound.unlock(),{once:true});", "document.addEventListener('pointerdown',()=>sound.unlock());document.addEventListener('keydown',()=>sound.unlock());")
start=app.index('function syncAudio(){');end=app.index('\n',start);change(app[start:end],'function syncAudio(){sound.mode(state.screen,state.session)}')
change("sound.fx(item==='turbo'?'sfx_turbo.ogg':'sfx_pickup.ogg');",'sound.item(item);')
change("sound.fx(r.correct?'sfx_correct.ogg':'sfx_retry.ogg');", "sound.fx(r.correct?'sfx_correct.ogg':'sfx_retry.ogg');RacePatchAV.feedback(r.correct);")
change('const award=C.awardProfile(data.profile,r);','const previousAudioLevel=1+Math.floor(data.profile.xp/250);const award=C.awardProfile(data.profile,r);')
change("sound.fx('sfx_finish.ogg');",'sound.finish(r,previousAudioLevel);')
change("function showResults(r){", "function showResults(r){RacePatchAV.results(r);")
change("open('audioDialog')}", "RacePatchAV.settings(sound);open('audioDialog')}")
change("for(let id of ['audioMute','musicVolume','engineVolume','effectsVolume'])", "for(let id of ['audioMute','masterVolume','musicVolume','engineVolume','effectsVolume','reduceAudio','reduceEffects'])")
change("sound.settings={mute:$('audioMute').checked,music:", "sound.settings={...sound.settings,master:Number($('masterVolume').value)/100,reduceAudio:$('reduceAudio').checked,reduceEffects:$('reduceEffects').checked,mute:$('audioMute').checked,music:")
change("if(!['answer','continueRace','useItem'].includes(act)&&state.screen!=='race')sound.fx('sfx_click.ogg');", "if(!['answer','continueRace','useItem'].includes(act)&&state.screen!=='race')sound.ui(button,act);")
change("if(controls.brake&&!state.lastBrake&&s.player.speed>9)sound.fx('sfx_skid.ogg');state.lastBrake=controls.brake;", "state.lastBrake=controls.brake;")
change('const event=s.advance(1/60,','const avSpeed=s.player.speed,avShield=s.buffs.shield,avCooldown=s.collisionCooldown;const event=s.advance(1/60,')
change('accumulator-=1/60;', 'accumulator-=1/60;RacePatchAV.event(sound,state.renderer,s,event,avSpeed,avShield,avCooldown);')
for i,old in enumerate(["sound.fx('sfx_collision.ogg');","sound.fx('sfx_collision.ogg',1.3);","sound.fx('sfx_turbo.ogg');"]):change(old,'/* Actual event audio '+str(i)+' dispatched above. */')
change(' requestAnimationFrame(frame);', ' RacePatchAV.frame(sound,state.renderer,s,state.screen,controls);requestAnimationFrame(frame);')
# Keep existing renderer/geometry intact; reduce the old fast exhaust flicker.
change('pulse=1+.12*Math.sin(session.elapsed*55)', 'pulse=this.patchReduced?1:1+.035*Math.sin(session.elapsed*9)')
change('<label class="toggle"><input id="audioMute" type="checkbox">Matikan seluruh suara</label>', '<label class="toggle"><input id="audioMute" type="checkbox">Matikan seluruh suara</label><label class="field"><span>Volume Master</span><input id="masterVolume" type="range" min="0" max="100" value="85"></label>')
change('<span>Efek suara</span>', '<span>Volume SFX</span>')
change('<input id="effectsVolume" type="range" min="0" max="100" value="55"></label>', '<input id="effectsVolume" type="range" min="0" max="100" value="55"></label><label class="toggle"><input id="reduceAudio" type="checkbox">Kurangi suara intens</label><label class="toggle"><input id="reduceEffects" type="checkbox">Reduced Effects · minim gerak &amp; partikel</label><p id="arcadeAudioStatus" role="status">Sentuh tombol untuk mengaktifkan audio.</p>')
# Remove transient feedback data when exporting a clean teacher package.
change("clone.querySelector('#initialData').textContent=", "clone.querySelector('#activeFeedback').removeAttribute('data-arcade-feedback');clone.querySelector('body').removeAttribute('data-arcade-confetti');\n clone.querySelector('#initialData').textContent=")
# Audio controls lead the dialog on HP; original graphics IDs/settings stay intact.
dialog=h[h.index('<dialog id="audioDialog"'):];dialog=dialog[:dialog.index('</dialog>')+9]
start=dialog.index('<div class="dialog-body stack">');content=start+len('<div class="dialog-body stack">');audio_at=dialog.index('<label class="toggle"><input id="audioMute"');foot=dialog.index('</div><div class="dialog-foot">',audio_at)
visual=dialog[content:audio_at];audio_controls=dialog[audio_at:foot]
change(dialog,dialog[:start]+'<div class="dialog-body arcade-settings"><section aria-label="Pengaturan audio"><h3>Audio Arcade</h3>'+audio_controls+'</section><section aria-label="Pengaturan tampilan"><h3>Tampilan &amp; Akses</h3>'+visual+'</section>'+dialog[foot:])
(B/'bounded-changes.json').write_text(json.dumps(changes,indent=2,ensure_ascii=False))
new_css='\n<style id="patch2Styles">\n'+(B/'source/ui.css').read_text()+'\n</style>\n';h=h.replace('</head>',new_css+'</head>',1)
scripts=list(re.finditer(r'<script\b[^>]*>(.*?)</script>',h,re.S));pos=scripts[11].end();block=''
for id,name in [('patch2Audio','audio.js'),('patch2VFX','vfx.js')]:block+='\n<script id="'+id+'">\n'+(B/'source'/name).read_text()+'\n</script>'
h=h[:pos]+block+h[pos:];out=D/'race-quest-pro-patch2.html';out.write_text(h);print('PATCH 2 bytes',out.stat().st_size)
