from pathlib import Path
import re,json
D=Path(__file__).resolve().parents[2];B=D/'student-teacher-modes';base=(D/'blokraya-balap-edukasi-nusantara.html').read_text();h=base;changes=[]
def change(old,new,count=1):
 global h
 assert h.count(old)==count,(old[:100],h.count(old));offset=h.index(old);h=h.replace(old,new);changes.append(dict(old=old,new=new,count=count,offset=offset))
change('<picture id="brPoster">','<div id="brPosterFallback" class="br-poster-fallback"><strong>BlokRaya</strong><p>Balap Edukasi Nusantara</p></div><picture id="brPoster">')
# Fallback sits beneath the real poster; it remains visible if the image fails.
change('</head>','<style id="blokRayaModesStyles">'+(B/'source/modes.css').read_text()+'</style></head>')
old=re.search(r'<script id="blokRayaLoading">.*?</script>',h,re.S)[0];change(old,'<script id="blokRayaLoading">'+(B/'source/loading.js').read_text()+'</script>')
body=re.search(r'<body[^>]*>',h)[0];change(body,body+'\n'+(B/'source/modes.html').read_text())
# Main application remains last; mode controller binds to existing screen/teacher functions.
needle="(function(){'use strict';";scripts=list(re.finditer(r'<script\b[^>]*>(.*?)</script>',h,re.S));main=next(s for s in scripts if 'async function ensureRenderer' in s[1]);pos=main.start();change(main[0],'<script id="blokRayaModes">'+(B/'source/modes.js').read_text()+'</script>\n'+main[0])
change("function showScreen(name){state.screen=name;","function showScreen(name){if(name==='teacher'&&!BlokRayaModes.requireTeacher())return;state.screen=name;")
for name,params in [('renderTeacher',''),('renderAnalysis',''),('exportAnalysis',''),('editBank','id'),('editQuestion','id'),('exportHistory',''),('exportGame','')]:
 old='function '+name+'('+params+'){';change(old,old+'if(!BlokRayaModes.requireTeacher())return;')
for form in ['settingsForm','bankForm','questionForm']:
 old="$('%s').onsubmit=e=>{e.preventDefault();"%form;change(old,old+'if(!BlokRayaModes.requireTeacher())return;')
for field in ['importJsonFile','importCsvFile']:
 old="$('%s').onchange=async e=>{"%field;change(old,old+'if(!BlokRayaModes.requireTeacher()){e.target.value=\'\';return;}')
# Also recheck after asynchronous import reading/confirmation before committing data.
change("incoming.banks.forEach(b=>b.id=C.uid());","if(!BlokRayaModes.requireTeacher())return;incoming.banks.forEach(b=>b.id=C.uid());")
change("return;b.questions.push(...qs);","return;if(!BlokRayaModes.requireTeacher())return;b.questions.push(...qs);")
change("const act=button.dataset.act,b=bank(),id=button.dataset.id;","const act=button.dataset.act,b=bank(),id=button.dataset.id;if(BlokRayaModes.isTeacherAction(act)&&!BlokRayaModes.requireTeacher())return;")
# A canceled/revoked teacher session cannot approve a pending destructive confirmation.
for old in ["'Hapus bank')){data.banks=","'Hapus soal')){b.questions=","'Hapus riwayat')){data.results="]:
 change(old,old.replace(')){',')&&BlokRayaModes.authenticated){'))
change('RaceHUD.cleanExport(clone);BlokRayaLoading.cleanExport(clone);','RaceHUD.cleanExport(clone);BlokRayaLoading.cleanExport(clone);BlokRayaModes.cleanExport(clone);')
change("showScreen('home');BlokRayaLoading.bootReady();", "BlokRayaModes.bind({student:()=>{closeAll();showScreen('home');setup()},teacher:()=>{closeAll();state.teacherTab='banks';showScreen('teacher')},locked:()=>{closeAll();$('teacherContent').replaceChildren();showScreen('home')}});showScreen('home');BlokRayaLoading.bootReady();")
# Keep mode switching in the home footer; do not expand the crowded mobile header.
change('KENDALIKAN • PIKIRKAN • MELAJU LEBIH JAUH</div>','KENDALIKAN • PIKIRKAN • MELAJU LEBIH JAUH<br><button class="br-mode-switch" type="button" onclick="BlokRayaModes.showChooser()">Ganti Mode Pengguna</button></div>')
old=re.search(r'<section id="teacher".*?</header>',h,re.S)[0];new=old.replace('</nav>','<button type="button" id="changeTeacherPinBtn" onclick="BlokRayaModes.changePin()">Ganti PIN</button><button type="button" id="teacherLogoutBtn" onclick="BlokRayaModes.logout()">Keluar Mode Guru</button></nav>');change(old,new)
# Screen initially remains non-interactive behind the loading overlay and chooser.
(D/'blokraya-mode-siswa-guru.html').write_text(h);(B/'bounded-changes.json').write_text(json.dumps(changes,indent=2));print('HTML',len(h.encode()),'growth',len(h.encode())-len(base.encode()))
