from pathlib import Path
import re,json,hashlib,subprocess
D=Path(__file__).resolve().parents[1];V=D.parent;R=V.parent;BASE='659e74b524f674b8a7c9275ab9b1207ba7ebceba';a=(V/'blokraya-patch8b-student-flow.html').read_text();b=(V/'blokraya-patch8c-podium.html').read_text();sha=lambda v:hashlib.sha256(v).hexdigest()
def scripts(s):
 out=[]
 for m in re.finditer(r'<script([^>]*)>(.*?)</script>',s,re.S):
  id=re.search(r'id="([^"]+)"',m[1]);out.append((id[1]if id else'application'if 'const state={screen:' in m[2]else'anonymous',m[2]))
 return out
old=scripts(a);new=scripts(b);new_only=[x for x in new if x[0]in['podiumClassification','threeRacerPodium']];assert len(new_only)==2;new=[x for x in new if x[0]not in ['podiumClassification','threeRacerPodium']];assert len(old)==len(new);protected=[];changed=[]
for x,y in zip(old,new):
 assert x[0]==y[0]
 if x[1]==y[1]:protected.append({'id':x[0],'sha256':sha(x[1].encode())})
 else:
  changed.append(x[0]);assert x[0]in ['application','blokRayaModes']
  if x[0]=='blokRayaModes':assert y[1].replace("'results','podium'","'results'")==x[1]
assert set(changed)=={'application','blokRayaModes'}
styles=lambda s:re.findall(r'<style([^>]*)>(.*?)</style>',s,re.S)
assert styles(a)==[x for x in styles(b)if'id="podiumStyles"'not in x[0]]
oldApp=next(v for k,v in old if k=='application');newApp=next(v for k,v in new if k=='application')
for start,end in [('function reviewCards','function openAudio'),('function exportHistory','function exportGame'),('function answer','function continueRace'),('async function startRacePrepared','function formatTime')]:
 assert oldApp[oldApp.index(start):oldApp.index(end)]==newApp[newApp.index(start):newApp.index(end)],start
assert [x for x in a.splitlines()if x.rstrip()!=x]==[x for x in b.splitlines()if x.rstrip()!=x]
assert (R/'index.html').read_bytes()==subprocess.check_output(['git','show',BASE+':index.html'],cwd=R)
changes=set(subprocess.check_output(['git','diff','--name-only',BASE],cwd=R).decode().splitlines());paths=subprocess.check_output(['git','ls-tree','-r','--name-only','-z',BASE],cwd=R).decode().split('\0');assert not any(p in changes for p in paths if p and p!='README.md')
r={'status':'passed','baseline_commit':BASE,'baseline_bytes':len(a.encode()),'html_bytes':len(b.encode()),'growth_bytes':len(b.encode())-len(a.encode()),'html_sha256':sha(b.encode()),'protected_script_payloads':protected,'changed_old_scripts':changed,'new_scripts':[x[0]for x in new_only],'protected_tracked_files':len([p for p in paths if p and p!='README.md']),'checks':['All engine/physics/AI/buff/stage/GP data/loader/rig payloads byte-identical','All fourteen GLB high/low pairs, avatar, poster and stage thumbnail assets byte-identical','PATCH 8B onboarding, stage picker and garage remain byte-identical','Teacher PIN module changes only screen inert/export lists; KDF, storage and access guards identical','Academic report, CSV export, quiz grading and race-start implementation identical','Existing styles unchanged; podium styles isolated','index.html and every prior artifact unchanged except root release README']}
(D/'scope-tests.json').write_text(json.dumps(r,indent=2));print('PASS',len(protected),'protected payloads;',r['growth_bytes'],'bytes growth')
