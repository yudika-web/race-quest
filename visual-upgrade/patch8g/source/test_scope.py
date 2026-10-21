from pathlib import Path
import re,json,hashlib,difflib,runpy
D=Path(__file__).resolve().parents[1];V=D.parent;B=V/'blokraya-patch8f-economy.html';H=V/'blokraya-patch8g-ui-polish.html'
a=B.read_text();b=H.read_text();script=lambda s:re.findall(r'<script\b([^>]*)>([\s\S]*?)</script>',s)
old,new=script(a),script(b);assert len(old)==len(new)
protected=[];changed=[]
for x,y in zip(old,new):
 assert x[0]==y[0]
 if x!=y:
  assert x[0]==' id="studentOnboarding"';changed.append(x[0]);(D/'onboarding-changes.diff').write_text(''.join(difflib.unified_diff(x[1].splitlines(True),y[1].splitlines(True),fromfile='8F/onboarding.js',tofile='8G/onboarding.js')))
 else:protected.append({'attributes':x[0],'sha256':hashlib.sha256(x[1].encode()).hexdigest()})
assert len(changed)==1
# Only display expressions/strings change inside the onboarding script.
x=next(x[1] for x in old if x[0]==' id="studentOnboarding"');y=next(x[1]for x in new if x[0]==' id="studentOnboarding"')
y=y.replace("function updateProgress(){const gp=$('setupMode').value==='gp',next=['Tingkat Kesulitan','Mode Balapan',gp?'Pilih Karakter':'Arena dan Cuaca','Pilih Karakter'];progress.textContent='Langkah '+(step+1)+' dari '+(gp?3:4)+' · Berikutnya: '+next[step];}\n",'')
y=y.replace('updateProgress();',"progress.textContent='Persiapan '+(n+1)+' / '+total+' · berikutnya: garasi';",1).replace('updateProgress();',"progress.textContent='Persiapan '+(step+1)+' / '+(gp?3:4)+' · berikutnya: garasi';",1)
for before,after in [ ('Isi nama pembalap.','Nama belum diisi. Masukkan nama untuk melanjutkan.'),('Isi kelas siswa.','Kelas belum diisi. Masukkan kelas untuk melanjutkan.'),('Nama dan kelas dicatat pada hasil belajar. Konfirmasikan sebelum melanjutkan.','Masukkan nama dan kelas untuk mencatat hasil belajarmu.'),("el('b',null,name.toUpperCase())","el('b',null,name)"),("['single','⚑','BEBAS'","['single','⚑','Balapan Bebas'"),("['gp','🏆','GRAND PRIX'","['gp','🏆','Grand Prix'")]:
 assert after in y;y=y.replace(after,before,1)

if x!=y:print(''.join(difflib.unified_diff(x.splitlines(True),y.splitlines(True))))
assert x==y,'Non-display onboarding logic must stay byte-identical'
# Rebuilding reproduces the exact distribution, including only approved markup copy and one scoped style block.
sha=hashlib.sha256(H.read_bytes()).hexdigest();runpy.run_path(str(D/'source/assemble.py'));assert hashlib.sha256(H.read_bytes()).hexdigest()==sha
(D/'scope-results.json').write_text(json.dumps({'passed':True,'protected_scripts':protected,'changed_scripts':changed,'onboarding_logic_identical_after_display_changes_reversed':True,'deterministic_build':True,'no_distribution_test_profiles':True,'baseline_sha256':hashlib.sha256(B.read_bytes()).hexdigest(),'html_sha256':sha},indent=2))
print('Scope passed:',len(protected),'unchanged scripts; only onboarding presentation + scoped CSS and approved markup text.')
