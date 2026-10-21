from pathlib import Path
import re,hashlib,json
D=Path(__file__).resolve().parents[1]; V=D.parent
base=V/'blokraya-stage13-ketapang.html'; s=base.read_text();original=s
assert hashlib.sha256(base.read_bytes()).hexdigest()=='3a5e2e4270b3a4843f3114b7b57e86cac48104449301382b9c491e71ddbaa645'
def replace(a,b):
 global s
 assert s.count(a)==1,(a,s.count(a));s=s.replace(a,b)
replace('<label class="field"><span>Bank soal</span><select id="setupBank"','<label class="field"><span>Kelas siswa</span><input id="playerClass" required maxlength="40" placeholder="Contoh: VIII A" autocomplete="off"></label><label class="field"><span>Bank soal</span><select id="setupBank"')
replace("function layoutSetup(){const form=", "function layoutSetup(){if(document.getElementById('onboardingTitle'))return;const form=")
replace("RaceStageUI.mountSetup(b)}","RaceStageUI.mountSetup(b);BlokRayaOnboarding.mount()}")
replace("fillSetupBank();open('setupDialog')}","$('playerClass').value=state.config?.studentClass||'';fillSetupBank();open('setupDialog');BlokRayaOnboarding.reset()}")
replace("name:$('playerName').value.trim()||'Pembalap',count", "name:$('playerName').value.trim()||'Pembalap',studentClass:$('playerClass').value.trim(),count")
replace("const r=s.result();data.stageProgress", "const r=s.result();r.bankClassName=r.className;r.studentClass=state.config?.studentClass||'';if(r.studentClass)r.className=r.studentClass;data.stageProgress")
replace("bankId:target.id,name:r?.name||'Pembalap',...target.settings", "bankId:target.id,name:r?.name||'Pembalap',studentClass:r?.studentClass||'',...target.settings")
replace("RaceHUD.cleanExport(clone);", "BlokRayaOnboarding.cleanExport(clone);RaceHUD.cleanExport(clone);")
replace('Pilihan sepuluh arena','Pilihan tiga belas arena');replace('Daftar sepuluh arena','Daftar tiga belas arena')
replace('Kalbar Klasik tersedia. Nusantara menunggu seluruh arena.','Empat turnamen tersedia; jumlah ronde mengikuti urutan arena masing-masing.')
replace('Nusantara tersedia setelah semua arena siap.','Keempat turnamen menggunakan arena yang sudah tersedia.')
# Load the UI adapter after markup and before the application script.
app=re.search(r'<script>\s*\(function\(\)\{\s*\x27use strict\x27;\s*const C=RaceCore',s)
if not app:
 app=next(m for m in re.finditer(r'<script[^>]*>',s) if 'const state={screen:' in s[m.end():m.end()+2000])
s=s[:app.start()]+'<script id="studentOnboarding">\n'+(D/'source/onboarding.js').read_text()+'\n</script>\n'+s[app.start():]
s=s.replace('</head>','<style id="studentOnboardingStyle">\n'+(D/'source/onboarding.css').read_text()+'\n</style>\n</head>')
(V/'blokraya-pro-final.html').write_text(s)
print(len(s.encode()),'bytes; growth',len(s.encode())-len(original.encode()))
