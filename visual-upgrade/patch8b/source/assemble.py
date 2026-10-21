from pathlib import Path
import re,hashlib
D=Path(__file__).resolve().parents[1];V=D.parent
base=V/'blokraya-patch8a-landmarks.html';s=base.read_text();original=s
assert hashlib.sha256(base.read_bytes()).hexdigest()=='8413c27e2b9e3e98ef0dc63b7147c37db1072b8cd56402ad6240ac84a3a166fb'
def replace(a,b):
 global s
 assert s.count(a)==1,(a,s.count(a));s=s.replace(a,b)
def payload(id,source,tag='script'):
 global s
 pattern=r'(<'+tag+r'[^>]*id="'+id+r'"[^>]*>)(.*?)(</'+tag+'>)'
 m=re.search(pattern,s,re.S);assert m,id;s=s[:m.start(2)]+'\n'+source+'\n'+s[m.end(2):]
# Reuse the original Stage UI registry/metrics and teacher fields; replace only student routing.
m=re.search(r'<script id="patch1StageUI">(.*?)</script>',s,re.S);ui=m[1]
a=ui.index('function mountSetup(');b=ui.index('function bindTeacher(',a)
ui=ui[:a]+'''function mountSetup(bank){BlokRayaOnboarding.mount(bank)}
function mountGarage(config,bank){garageConfig=config;BlokRayaOnboarding.summary(config,bank);const gp=config.mode==='gp';document.getElementById('startRaceBtn').disabled=S.status(config.stage,progressProvider()).code!=='available'||(gp&&!S.cupStatus(config.gpId,progressProvider()).available)}
'''+ui[b:]
# The old grid/hero picker is no longer reachable from student preparation or garage.
# Remove its code and its second parsed copy of thumbnail assets, retaining teacher fields.
a=ui.index('function picker(');b=ui.index('function mountSetup(',a);ui=ui[:a]+ui[b:]
a=ui.index('const el=');b=ui.index('function metrics(',a);ui=ui[:a]+ui[b:]
ui=ui.replace("const C=RaceCore,S=RaceStages,entries=S.catalog,assets=JSON.parse(document.getElementById('patch1StageAssets').textContent),teacherDefaults=new Map();let garageConfig=null,progressProvider=()=>({});", "const C=RaceCore,S=RaceStages,entries=S.catalog;let progressProvider=()=>({});")
ui=ui.replace('garageConfig=config;','')
ui=ui.replace('root.RaceStageUI={mountSetup','root.RaceStageUI={progress:()=>progressProvider(),mountSetup')
(D/'source/stage-ui.js').write_text(ui.strip()+'\n');payload('patch1StageUI',ui.strip())
payload('studentOnboarding',(D/'source/onboarding.js').read_text());payload('studentOnboardingStyle',(D/'source/onboarding.css').read_text(),'style')
replace('function setup(){\n const available=',"function setup(){\n const returning=state.screen==='garage';BlokRayaOnboarding.begin(state.config);const available=")
replace("open('setupDialog');BlokRayaOnboarding.reset()}","open('setupDialog');BlokRayaOnboarding.reset(returning)}")
replace("RaceStageUI.mountSetup(b);BlokRayaOnboarding.mount()}","RaceStageUI.mountSetup(b)}")
replace("$('setupBank').onchange=fillSetupBank;","$('setupBank').onchange=()=>{BlokRayaOnboarding.capture();fillSetupBank()};")
# Original submit handler still creates the config, saves selected bank and opens the existing garage.
replace("if(!preferences.tutorialSeen){preferences.tutorialSeen=true;persistPreferences();open('helpDialog')}","if(!preferences.tutorialSeen){preferences.tutorialSeen=true;persistPreferences()}")
replace("async function startRace(continuing=false){",'''async function startRace(continuing=false){
 if(state.startingRace)return;state.startingRace=true;$('startRaceBtn').disabled=true;
 try{const cfg=state.config,b=data.banks.find(b=>b.id===cfg?.bankId);try{BlokRayaOnboarding.validateConfig(cfg,b,data.stageProgress);if(!data.profile.unlocked.includes(state.character))throw Error('Pilih pembalap yang sudah terbuka.')}catch(e){setup();inputError('setupError',e.message);return}await startRacePrepared(continuing)}finally{state.startingRace=false;if(state.screen==='garage'&&$('webglError').hidden)$('startRaceBtn').disabled=false}
}
async function startRacePrepared(continuing=false){''')
replace('<button class="btn ghost" data-act="setup">Ubah persiapan</button>','<button class="btn ghost" data-act="setup">← Kembali ke Persiapan</button>')
replace('<nav class="app-nav"><button data-act="home">Menu utama</button><button data-act="audio">Suara</button></nav></header><div class="garage-layout">','<nav class="app-nav"><button data-act="home">Menu utama</button><button data-act="help">Bantuan</button><button data-act="audio">Suara</button></nav></header><div class="garage-layout">')
# Keep an editable exact copy of the minimal application integration for review.
app=next(m[2] for m in re.finditer(r'<script([^>]*)>(.*?)</script>',s,re.S) if 'const state={screen:' in m[2]);(D/'source/application.js').write_text(app.strip()+'\n')
(V/'blokraya-patch8b-student-flow.html').write_text(s)
print(len(s.encode()),'bytes; growth',len(s.encode())-len(original.encode()))
