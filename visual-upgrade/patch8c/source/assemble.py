from pathlib import Path
import hashlib,re
D=Path(__file__).resolve().parents[1];V=D.parent;base=V/'blokraya-patch8b-student-flow.html';s=base.read_text();original=s
assert hashlib.sha256(base.read_bytes()).hexdigest()=='137e69a297c3904d5290e1c34fccfce12bcdf0a8140e979df5188af195c33155'
def replace(a,b,n=1):
 global s
 assert s.count(a)==n,(a,s.count(a));s=s.replace(a,b)
replace('</head>','<style id="podiumStyles">\n'+(D/'source/podium.css').read_text()+'\n</style>\n</head>')
replace('<script id="studentOnboarding">',(D/'source/podium.html').read_text()+'\n<script id="podiumClassification">\n'+(D/'source/classification.js').read_text()+'\n</script>\n<script id="threeRacerPodium">\n'+(D/'source/podium.js').read_text()+'\n</script>\n<script id="studentOnboarding">')
# Only screen visibility/inert lists change in the mode controller; PIN/KDF/guards remain identical.
replace("['home','garage','teacher','race','results'", "['home','garage','teacher','race','results','podium'",4)
replace("state.screen=name;document.body.dataset.screen=name;", "if(state.screen==='podium'&&name!=='podium')RacePodium.leave(state.renderer);state.screen=name;document.body.dataset.screen=name;")
replace("$(name==='garage'?'garagePreviewHost':'raceSceneHost').append($('scene'));", "$(name==='garage'?'garagePreviewHost':name==='podium'?'podiumPreviewHost':'raceSceneHost').append($('scene'));")
replace("function finish(){const s=state.session;if(!s||s.status!=='finished')return;const r=s.result();", "async function finish(){const s=state.session;if(!s||s.status!=='finished'||state.finishing)return;state.finishing=true;clearControls();sound.engineState(false);$('countdown').hidden=true;open('finishWaitDialog');try{const completion=await BlokRayaClassification.finalize(s,(n,total)=>{$('finishWaitStatus').textContent=n+' / '+total+' lawan telah finis';});if(state.session!==s)return;const r=completion.result;")
replace("const ghost=s.ghostResult(),old=", "const ghost=completion.ghost,old=")
replace("sound.finish(r,previousAudioLevel);", "sound.finish(r.gp?.complete?{...r,position:r.gp.standings.findIndex(x=>x.id===0)+1}:r,previousAudioLevel);")
replace("$('countdown').hidden=true;showResults(r)}", "$('countdown').hidden=true;close('finishWaitDialog');if((!r.gp||r.gp.complete)&&RacePodium.entrants(r)){showScreen('podium');RacePodium.show(state.renderer,r,paintColor(data.profile.paint))}else showResults(r)}finally{state.finishing=false;close('finishWaitDialog')}}")
replace("case 'help':open('helpDialog');", "case 'podiumResults':if(state.result)showResults(state.result);break;case 'help':open('helpDialog');")
replace("BlokRayaOnboarding.cleanExport(clone);", "RacePodium.cleanExport(clone);BlokRayaOnboarding.cleanExport(clone);")
replace("else{accumulator=0;$('countdown').hidden=true;if(state.screen==='garage'", "else{accumulator=0;$('countdown').hidden=true;if(state.screen==='podium')RacePodium.frame(state.renderer,now);if(state.screen==='garage'")
replace("$('setupDialog').addEventListener('close'", "$('finishWaitDialog').addEventListener('cancel',e=>e.preventDefault());\n$('setupDialog').addEventListener('close'")
(V/'blokraya-patch8c-podium.html').write_text(s)
app=next(m[2]for m in re.finditer(r'<script([^>]*)>(.*?)</script>',s,re.S)if 'const state={screen:' in m[2]);(D/'source/application.js').write_text(app.strip()+'\n')
print(len(s.encode()),'bytes; growth',len(s.encode())-len(original.encode()))
