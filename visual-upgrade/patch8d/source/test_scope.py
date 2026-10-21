from pathlib import Path
import re,json,hashlib,subprocess
D=Path(__file__).resolve().parents[1];V=D.parent;R=V.parent;BASE='18fce7045518dc7f4b8569ce3010a73f267056d2'
a=(V/'blokraya-patch8c-podium.html').read_text();b=(V/'blokraya-patch8d-controls.html').read_text();sha=lambda v:hashlib.sha256(v).hexdigest()
def scripts(s):
 out=[]
 for m in re.finditer(r'<script([^>]*)>(.*?)</script>',s,re.S):
  id=re.search(r'id="([^"]+)"',m[1]);out.append((id[1]if id else'application'if 'const state={screen:' in m[2]else'anonymous',m[2]))
 return out
old=scripts(a);new=scripts(b);added=[x for x in new if x[0]=='patch8dViewportTouch'];assert len(added)==1;new=[x for x in new if x[0]!='patch8dViewportTouch'];assert len(old)==len(new);protected=[];changed=[]
for x,y in zip(old,new):
 assert x[0]==y[0]
 if x[1]==y[1]:protected.append({'id':x[0],'sha256':sha(x[1].encode())})
 else:changed.append(x[0]);assert x[0]in ['application','patch45HUD']
assert set(changed)=={'application','patch45HUD'}
styles=lambda s:re.findall(r'<style([^>]*)>(.*?)</style>',s,re.S)
assert styles(a)==[x for x in styles(b)if'id="patch8dViewportStyles"'not in x[0]]
oldApp=next(v for k,v in old if k=='application');newApp=next(v for k,v in new if k=='application')
for start,end in [('function reviewCards','function openAudio'),('function exportHistory','function exportGame'),('function answer','function continueRace'),('async function startRace','function formatTime'),('function showQuestion','function continueRace'),('function pauseRace','function finish')]:
 assert oldApp[oldApp.index(start):oldApp.index(end)]==newApp[newApp.index(start):newApp.index(end)],start
assert oldApp[oldApp.index('async function finish'):oldApp.index('function showResults')]==newApp[newApp.index('async function finish'):newApp.index('function showResults')]
assert [x for x in a.splitlines()if x.rstrip()!=x]==[x for x in b.splitlines()if x.rstrip()!=x]
assert (R/'index.html').read_bytes()==subprocess.check_output(['git','show',BASE+':index.html'],cwd=R)
changes=set(subprocess.check_output(['git','diff','--name-only',BASE],cwd=R).decode().splitlines());paths=subprocess.check_output(['git','ls-tree','-r','--name-only','-z',BASE],cwd=R).decode().split('\0');assert not any(p in changes for p in paths if p and p!='README.md')
# The follow-up starts at the already-pushed PATCH 8D HEAD. Only its joystick
# input module may differ in the distribution; existing HUD/onboarding are retained.
FOLLOW_UP='d12401fc337b0a5869b2b9fdd8be9a4757c29fcb'
head_html=subprocess.check_output(['git','show',FOLLOW_UP+':visual-upgrade/blokraya-patch8d-controls.html'],cwd=R).decode()
module=lambda value:re.search(r'(<script id="patch8dViewportTouch">)(.*?)(</script>)',value,re.S)
before=module(head_html);after=module(b);assert before and after
assert b[:after.start(2)]+before[2]+b[after.end(2):]==head_html
r={'status':'passed','baseline_commit':BASE,'follow_up_baseline_commit':FOLLOW_UP,'follow_up_growth_bytes':len(b.encode())-len(head_html.encode()),'baseline_bytes':len(a.encode()),'html_bytes':len(b.encode()),'growth_bytes':len(b.encode())-len(a.encode()),'html_sha256':sha(b.encode()),'protected_script_payloads':protected,'changed_old_scripts':changed,'protected_tracked_files':len([p for p in paths if p and p!='README.md']),'checks':['Engine/physics/AI/buff/stage/GP data/loader/rig payloads byte-identical','Fourteen model pairs, avatars, posters and stage thumbnails byte-identical','PATCH 8B onboarding/stage UI, PIN auth and PATCH 8C podium/classification byte-identical','Academic grading, report, start validation/loading, finish and export results unchanged','Existing CSS retained; scoped viewport/control overrides added','All prior tracked artifacts and online index.html unchanged except root release README','Compared with pushed PATCH 8D HEAD, HTML changes only the joystick boundary input module']}
(D/'scope-tests.json').write_text(json.dumps(r,indent=2));print('PASS',len(protected),'protected payloads;',r['growth_bytes'],'bytes growth')
