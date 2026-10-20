from pathlib import Path
import re,json
D=Path(__file__).resolve().parents[2];B=D/'patch5-ten-stages';base=(D/'blokraya-mode-siswa-guru.html').read_text();h=base;changes=[]
def change(old,new,count=1):
 global h
 assert h.count(old)==count,(old[:100],h.count(old));h=h.replace(old,new);changes.append(dict(old=old,new=new,count=count))
# Preserve three legacy track configs; metadata/catalog represents planned as well as actual stages.
old=re.search(r'<script id="patch1StageCatalog"[^>]*>.*?</script>',h,re.S)[0]
new='<script id="patch1StageCatalog" type="application/json">'+json.dumps(json.loads((B/'stages.json').read_text()),ensure_ascii=False,separators=(',',':'))+'</script>\n<script id="patch5CupCatalog" type="application/json">'+json.dumps(json.loads((B/'cups.json').read_text()),ensure_ascii=False,separators=(',',':'))+'</script>\n<script id="patch5StageRegistry">'+(B/'source/registry.js').read_text()+'</script>'
change(old,new)
change('function stageById(id){return STAGES.find(x=>x.id===id)||STAGES[0]}',"function stageById(id){if(root.RaceStages?.get(id))return root.RaceStages.track(id);return STAGES.find(x=>x.id===id)||STAGES[0]}")
change('stage:stageById(settings.stage).id,weather:',"stage:root.RaceStages.normalizeId(settings.stage),gpId:root.RaceStages.normalizeCup(settings.gpId),weather:")
change('profile:normalizeProfile(data.profile||{unlocked:Array.from({length:14},(_,i)=>i)}),ghosts:', 'profile:normalizeProfile(data.profile||{unlocked:Array.from({length:14},(_,i)=>i)}),stageProgress:root.RaceStages.normalizeProgress(data.stageProgress,data.results),ghosts:')
old=re.search(r'class GrandPrix\{.*?\nfunction ghostKey',h,re.S)[0][:-len('\nfunction ghostKey')];change(old,(B/'source/grand-prix.js').read_text().strip())
change('analyzeResults,GrandPrix,ghostKey','analyzeResults,GrandPrix,GrandPrixSequence,ghostKey')
change("constructor(bank,{name='Pembalap',character=0,rng=Math.random}={}){","constructor(bank,{name='Pembalap',character=0,rng=Math.random,stageProgress={}}={}){")
change('this.settings=copy(this.bank.settings);this.rng=rng;', 'this.settings=copy(this.bank.settings);root.RaceStages.requireStage(this.settings.stage,stageProgress);this.rng=rng;')
change('data.profile=C.normalizeProfile(data.profile);data.ghosts=', 'data.stageProgress=RaceStages.normalizeProgress(data.stageProgress,data.results);data.profile=C.normalizeProfile(data.profile);data.ghosts=')
change("new C.Session(snapshot,{name:cfg.name,character:state.character,ghost:", "new C.Session(snapshot,{stageProgress:data.stageProgress,name:cfg.name,character:state.character,ghost:")
change('buildWorld(track){\n',"buildWorld(track){\n  if(RaceStages.track(track.id)!==track.config)throw Error('Track belum terdaftar pada world builder.');\n")
change('this.scenery.build(track);','RaceStages.buildEnvironment(this,track);')
old=re.search(r'<script id="patch1StageUI">.*?</script>',h,re.S)[0];change(old,'<script id="patch1StageUI">'+(B/'source/stage-ui.js').read_text()+'</script>')
change('</head>','<style id="patch5StagesStyles">'+(B/'source/ui.css').read_text()+'</style></head>')
old=re.search(r'function stageFields\(prefix,settings\).*?\nfunction renderAnalysis',h,re.S)[0][:-len('\nfunction renderAnalysis')];change(old,'function stageFields(prefix,settings){return RaceStageUI.fields(prefix,settings)}')
old=re.search(r'function gpPanel\(r\).*?\n\nfunction syncAudio',h,re.S)[0][:-len('\n\nfunction syncAudio')];change(old,(B/'source/gp-panel.js').read_text().strip())
# Teacher/save validation is guarded by existing local PIN handlers.
change("if(!BlokRayaModes.requireTeacher())return;const count=Number($('teacherCount').value);", "if(!BlokRayaModes.requireTeacher())return;try{if($('teacherMode').value==='gp')RaceStages.requireCup($('teacherCup').value,data.stageProgress);else RaceStages.requireStage($('teacherStage').value,data.stageProgress)}catch(err){inputError('settingsError',err.message);return}const count=Number($('teacherCount').value);")
change("b.settings={...b.settings,stage:$('teacherStage').value,", "b.settings={...b.settings,gpId:$('teacherCup').value,stage:$('teacherStage').value,")
change("saved('Pengaturan balapan disimpan.');renderTeacher()};return;", "saved('Pengaturan balapan disimpan.');renderTeacher()};RaceStageUI.bindTeacher();return;")
old="$('setupMasteryInfo').textContent='Grand Prix: Pontianak → Mempawah → Singkawang. Skor kuis minimal '+b.settings.mastery+'% membuka tahap berikutnya.';"
change(old,"$('setupMasteryInfo').textContent='Grand Prix mengikuti urutan turnamen. Skor kuis minimal '+b.settings.mastery+'% membuka tahap berikutnya. Nusantara tersedia setelah semua arena siap.';")
change("state.gp=null;state.config={...b.settings,stage:$('setupStage').value,", "try{if($('setupMode').value==='gp')RaceStages.requireCup($('setupCup').value,data.stageProgress);else RaceStages.requireStage($('setupStage').value,data.stageProgress)}catch(err){inputError('setupError',err.message);return}state.gp=null;state.config={...b.settings,gpId:$('setupCup').value,stage:$('setupStage').value,")
change("if(!continuing)state.gp=cfg.mode==='gp'?new C.GrandPrix(b.settings.mastery):null;", "if(!continuing)state.gp=cfg.mode==='gp'?new C.GrandPrix(b.settings.mastery,cfg.gpId||'kalbar-klasik',data.stageProgress):null;")
change("if(state.gp)cfg.stage=state.gp.stage.id;const snapshot=", "if(state.gp)cfg.stage=state.gp.stage.id;RaceStages.requireStage(cfg.stage,data.stageProgress);const snapshot=")
change("snapshot.settings={...b.settings,stage:cfg.stage,", "snapshot.settings={...b.settings,gpId:cfg.gpId||'kalbar-klasik',stage:cfg.stage,")
change('state.result=null;state.lastStatus=',"if(state.gp)state.session.grandPrix={id:state.gp.cupId,label:state.gp.label,round:state.gp.round+1,totalRounds:state.gp.totalRounds};state.result=null;state.lastStatus=")
change("(state.gp?'GP '+(state.gp.round+1)+'/3 · ':'')", "(state.gp?'GP '+(state.gp.round+1)+'/'+state.gp.totalRounds+' · ':'')")
change("(s.settings.mode==='gp'?'GP '+(C.STAGES.findIndex(x=>x.id===s.track.id)+1)+'/3 · ':'')", "(s.settings.mode==='gp'?'GP '+(s.grandPrix?.round||((RaceStages.cup(s.settings.gpId)||RaceStages.cup()).stageIds.indexOf(s.track.id)+1))+'/'+(s.grandPrix?.totalRounds||(RaceStages.cup(s.settings.gpId)||RaceStages.cup()).stageIds.length)+' · ':'')")
change('const r=s.result();data.results.push(r);','const r=s.result();data.stageProgress=RaceStages.recordProgress(data.stageProgress,r);data.results.push(r);')
change('r.gp={round:state.gp.round+1,blocked:', 'r.gp={id:state.gp.cupId,label:state.gp.label,totalRounds:state.gp.totalRounds,stageIds:state.gp.stageIds.slice(),roundSummaries:state.gp.summary(),champion:state.gp.complete?state.gp.standings()[0].id:null,round:state.gp.round+1,blocked:')
change("BlokRayaModes.bind({student:","RaceStageUI.setProgressProvider(()=>data.stageProgress);BlokRayaModes.bind({student:")
# Future GP selection persists as configuration but cannot launch until cup availability passes.
change("const cfg=state.config,b=data.banks.find(b=>b.id===cfg?.bankId);if(!cfg||!b||!b.questions.length){setup();return}if(!await ensureRenderer())return;", "const cfg=state.config,b=data.banks.find(b=>b.id===cfg?.bankId);if(!cfg||!b||!b.questions.length){setup();return}if(cfg.mode==='gp')RaceStages.requireCup(cfg.gpId||'kalbar-klasik',data.stageProgress);else RaceStages.requireStage(cfg.stage,data.stageProgress);if(!await ensureRenderer())return;")
(D/'blokraya-patch5.html').write_text(h);(B/'bounded-changes.json').write_text(json.dumps(changes,indent=2));print('HTML',len(h.encode()),'growth',len(h.encode())-len(base.encode()))
