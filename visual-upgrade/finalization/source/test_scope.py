from pathlib import Path
import re,json,hashlib,subprocess
D=Path(__file__).resolve().parents[1];V=D.parent;R=V.parent
sha=lambda b:hashlib.sha256(b).hexdigest()
a=(V/'blokraya-stage13-ketapang.html').read_text();b=(V/'blokraya-pro-final.html').read_text()
def scripts(s):
 out=[]
 for m in re.finditer(r'<script([^>]*)>(.*?)</script>',s,re.S):
  attrs,text=m.groups();id=re.search(r'id="([^"]+)"',attrs)
  out.append((id.group(1) if id else 'anonymous',text))
 return out
old=scripts(a);new=scripts(b);assert len(new)==len(old)+1
new=[x for x in new if x[0]!='studentOnboarding'];changes=[];protected=[]
for i,(x,y)in enumerate(zip(old,new)):
 assert x[0]==y[0]
 if x[1]!=y[1]:
  assert x[0]=='patch1StageUI' or 'const state={screen:' in x[1],x[0]
  changes.append(x[0])
 else:protected.append({'script':x[0],'sha256':sha(x[1].encode())})
assert len(changes)==2
assert (R/'index.html').read_bytes()==subprocess.check_output(['git','show','1b3f9454a780af9f7a53ecebb1a6e599f052cb32:index.html'],cwd=R)
# All pre-existing tracked source/model/media artifacts remain byte-identical.
BASE='1b3f9454a780af9f7a53ecebb1a6e599f052cb32'
paths=subprocess.check_output(['git','ls-tree','-r','--name-only','-z',BASE],cwd=R).split(b'\0');files=[]
changed=set(subprocess.check_output(['git','diff','--name-only',BASE],cwd=R).decode().splitlines());assert changed<=set(['README.md','visual-upgrade/blokraya-pro-final.html'])|{p for p in changed if p.startswith('visual-upgrade/finalization/')}|{'blokraya-pro-final-playable.zip','blokraya-pro-final-review.zip'}
for raw in paths:
 if not raw:continue
 p=raw.decode()
 if p=='README.md':continue
 assert p not in changed,p
 files.append(p)
r={'status':'passed','checks':['All existing tracked files unchanged','Root index.html unchanged','Only app orchestration and stage UI text changed; all core, physics, AI, buffs, modes/PIN, loader, world builders, track data, model/poster/thumbnail payloads identical'],'protected_script_payloads':protected,'changed_scripts':changes,'protected_files':len(files),'baseline_sha256':sha(a.encode()),'html_sha256':sha(b.encode()),'html_bytes':len(b.encode()),'growth_bytes':len(b.encode())-len(a.encode())}
(D/'scope-tests.json').write_text(json.dumps(r,indent=2));print('PASS',len(files),'existing files and',len(protected),'script payloads unchanged')
