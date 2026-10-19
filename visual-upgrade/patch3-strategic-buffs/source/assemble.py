from pathlib import Path
import re,json,hashlib
D=Path(__file__).resolve().parents[2];B=D/'patch3-strategic-buffs';base=(D/'race-quest-pro-patch2.html').read_text();h=base;changes=[]
(B/'baseline.json').write_text(json.dumps({'commit':'c786d88aca6876e7913012f3490fd2f6660898c8','bytes':len(base.encode()),'sha256':hashlib.sha256(base.encode()).hexdigest()},indent=2))
def change(old,new):
 global h
 assert h.count(old)==1,(old[:120],h.count(old));h=h.replace(old,new);changes.append({'old':old,'new':new})
change('const max=p.bubble>0?3:p.slip>0?8:this.buffs.turbo>0?31:23;', 'const max=p.bubble>0?3:p.slip>0?(this.buffs.grip>0?14:8):(this.buffs.turbo>0||this.buffs.nitro>0)?31:23;')
change('const cap=p.bubble>0?3:p.slip>0?8:Infinity;', 'const cap=p.bubble>0?3:p.slip>0?(this.buffs.grip>0?14:8):Infinity;')
change("this.weather==='rain'?.78:1", "this.weather==='rain'?(this.buffs.grip>0?.94:.78):1")
change('Math.sin(this.elapsed*13)*dt*.9','Math.sin(this.elapsed*13)*dt*.9*(this.buffs.grip>0?.3:1)')
change("this.hit(hit.r,'bubble')", "this.hit(hit.r,'bubble',b.owner)")
change("this.hit(r,'oil')", "this.hit(r,'oil',o.owner)")
change('const ASSETS=JSON.parse($(\'assetData\').textContent)', "const ASSETS=Object.assign(JSON.parse($('assetData').textContent),RaceStrategicBuffs.icons)")
change("+(oldSlot?'<p class=\"small\">Buff di slot sebelumnya telah diganti.</p>':'')", "+'<p class=\"small\">Dua slot tersedia. Jika penuh, pilih item yang diganti atau lewati hadiah.</p>'")
change("$('activeFeedback').innerHTML=feedback;", "$('activeFeedback').innerHTML=feedback;RaceBuffUI.reward(s);")
change("function continueRace(){const s=state.session;if(!s||s.status!=='feedback')return;", "function continueRace(){const s=state.session;if(!s||s.status!=='feedback'||s.pendingReward)return;")
change("$('useItemBtn').disabled=!def||s.status!=='racing';drawMinimap();", "$('useItemBtn').disabled=!def||s.status!=='racing';drawMinimap();RaceBuffUI.update(s);")
change("if((e.key==='e'||e.key==='E'||e.code==='Space')&&!e.repeat)", "if(!e.repeat&&['q','Q','1','2'].includes(e.key)){e.preventDefault();s.selectSlot(e.key==='1'?0:e.key==='2'?1:1-s.selectedSlot);updateHud()}\n if((e.key==='e'||e.key==='E'||e.code==='Space')&&!e.repeat)")
change("clone.querySelector('#initialData').textContent=", "for(const id of ['strategicSlots','strategyRadar','rewardChoice'])clone.querySelector('#'+id)?.remove();clone.querySelector('#continueRaceBtn').disabled=false;\n clone.querySelector('#initialData').textContent=")
change('const p=s.player,turbo=s.buffs.turbo>0;', 'const p=s.player,turbo=s.buffs.turbo>0||s.buffs.nitro>0;')
change("this.sample('sfx_turbo.ogg',{category:'race',level:.65,gap:.45})", "this.sample('sfx_turbo.ogg',{category:'race',level:s.buffs.nitro>0?.5:.65,rate:s.buffs.nitro>0?1.2:1,gap:.45})")
change('const turbo=s.buffs.turbo>0;', 'const turbo=s.buffs.turbo>0||s.buffs.nitro>0,trail=s.buffs.nitro>0?[1,.58,.16]:CYAN;')
change(',.10+(this.patchEmit%3)*.03,.32,CYAN,true', ',.10+(this.patchEmit%3)*.03,.32,trail,true')
change('low?8:16,CYAN,2,.09,.4','low?8:16,trail,2,.09,.4')
change('if(session.buffs.shield>0)this.drawPrimitive(this.ring,transform(pos.x,pos.y+.18,pos.z,session.elapsed,1.05));', 'if(session.buffs.shield>0)this.drawPrimitive(this.ring,transform(pos.x,pos.y+.18,pos.z,session.elapsed,1.05));if(session.buffs.reflect>0){this.ring.material.color=[.64,.32,.95];this.drawPrimitive(this.ring,transform(pos.x,pos.y+.3,pos.z,session.elapsed,1.12));this.ring.material.color=[.04,.65,.85]}if(session.buffs.grip>0){this.ring.material.color=[.20,.76,.47];this.drawPrimitive(this.ring,transform(pos.x,pos.y+.11,pos.z,0,.94));this.ring.material.color=[.04,.65,.85]}')
change('Slot hanya menyimpan satu buff; hadiah baru menggantikan buff yang belum dipakai.', 'Dua slot menyimpan hadiah. Ketuk slot atau tekan Q / 1 / 2 untuk memilih. Saat penuh, pilih slot yang diganti atau lewati hadiah baru. Cooldown terlihat di slot; inventori berlaku selama balapan ini.')
change('Semua efek ikut dijeda saat soal tampil.</p>', 'Perisai Pantul menangkis satu serangan dan dapat memantulkan efek singkat; Nitro Ganda memiliki dua charge; Ban Anti-Selip mengurangi oli; Radar menampilkan ancaman dekat tanpa jawaban soal. Dorongan tidak ditumpuk. Semua efek dan cooldown ikut dijeda saat soal tampil.</p>')
change('const oldSlot=s.slot,r=s.answer(index);', 'const r=s.answer(index);')
# New trails use the existing bounded particle pool; static HUD uses no wall-clock animations.
(B/'bounded-changes.json').write_text(json.dumps(changes,indent=2,ensure_ascii=False))
h=h.replace('</head>','<style id="patch3Styles">'+(B/'source/ui.css').read_text()+'</style></head>',1)
s=list(re.finditer(r'<script\b[^>]*>(.*?)</script>',h,re.S));pos=s[13].end()
block='<script id="patch3BuffIcons" type="application/json">'+(B/'icons/icons.json').read_text()+'</script>'
for id,file in [('patch3BuffSystem','buffs.js'),('patch3BuffUI','ui.js')]:block+='\n<script id="'+id+'">'+(B/'source'/file).read_text()+'</script>'
h=h[:pos]+block+h[pos:];out=D/'race-quest-pro-patch3.html';out.write_text(h);print('PATCH 3',out.stat().st_size,'bytes')
