from pathlib import Path
import re,json,hashlib,subprocess
D=Path(__file__).resolve().parents[1];V=D.parent;R=V.parent;BASE='83c2213f6b6791bfd2ad9f962a356a912bdf5b49'
a=(V/'blokraya-patch8a-landmarks.html').read_text();b=(V/'blokraya-patch8b-student-flow.html').read_text();sha=lambda v:hashlib.sha256(v).hexdigest()
def scripts(s):
 out=[]
 for m in re.finditer(r'<script([^>]*)>(.*?)</script>',s,re.S):
  id=re.search(r'id="([^"]+)"',m[1]);out.append((id[1] if id else ('application' if 'const state={screen:' in m[2] else 'anonymous'),m[2]))
 return out
old=scripts(a);new=scripts(b);assert len(new)==len(old);protected=[];changed=[]
for x,y in zip(old,new):
 assert x[0]==y[0]
 if x[1]!=y[1]:changed.append(x[0]);assert x[0] in ['application','studentOnboarding','patch1StageUI']
 else:protected.append({'id':x[0],'sha256':sha(x[1].encode())})
assert set(changed)=={'application','studentOnboarding','patch1StageUI'}
styles=lambda s:re.findall(r'<style([^>]*)>(.*?)</style>',s,re.S)
for x,y in zip(styles(a),styles(b)):
 assert x[0]==y[0]
 if 'studentOnboardingStyle' not in x[0]:assert x[1]==y[1]
assert (R/'index.html').read_bytes()==subprocess.check_output(['git','show',BASE+':index.html'],cwd=R)
changes=set(subprocess.check_output(['git','diff','--name-only',BASE],cwd=R).decode().splitlines());paths=subprocess.check_output(['git','ls-tree','-r','--name-only','-z',BASE],cwd=R).decode().split('\0');assert not any(p in changes for p in paths if p and p!='README.md')
# Every old whitespace line in generated HTML is retained, including upstream engine whitespace.
assert [x for x in a.splitlines() if x.rstrip()!=x]==[x for x in b.splitlines() if x.rstrip()!=x]
for id in ['patch8aLandmarks','assetData','patch1StageAssets','blokRayaModes','blokRayaLoading','patch5StageRegistry']:
 assert next(x[1]for x in old if x[0]==id)==next(x[1]for x in new if x[0]==id)
r={'status':'passed','baseline_commit':BASE,'baseline_bytes':len(a.encode()),'html_bytes':len(b.encode()),'growth_bytes':len(b.encode())-len(a.encode()),'html_sha256':sha(b.encode()),'changed_script_payloads':changed,'protected_script_payloads':protected,'protected_tracked_files':len([p for p in paths if p and p!='README.md']),'checks':['Same number and order of scripts: replaced original onboarding, no second wizard','All 13 tracks/world builders including PATCH 8A landmarks exactly unchanged','All 14 GLB high/low, avatars, thumbnails and posters byte-identical','Engine/physics/AI/buffs/HUD/audio/quiz/GP/storage/PIN/loading payloads byte-identical','Only student flow CSS changed; teacher and racing styles byte-identical','index.html and prior artifacts unchanged; inherited whitespace retained']}
(D/'scope-tests.json').write_text(json.dumps(r,indent=2));print('PASS',len(protected),'protected payloads;',r['growth_bytes'],'bytes growth')
