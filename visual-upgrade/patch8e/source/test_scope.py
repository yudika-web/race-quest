from pathlib import Path
import re,json,hashlib,subprocess
D=Path(__file__).resolve().parents[1];V=D.parent;R=V.parent;BASE='c34fe8b1da86ca561f5ff49419a88e401185fe28';a=(V/'blokraya-patch8d-controls.html').read_text();b=(V/'blokraya-patch8e-startup.html').read_text();sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
def scripts(s):
 out=[]
 for m in re.finditer(r'<script([^>]*)>(.*?)</script>',s,re.S):
  id=re.search(r'id="([^"]+)"',m[1]);out.append((id[1]if id else'application'if 'const state={screen:'in m[2]else'anonymous',m[2]))
 return out
old=scripts(a);new=scripts(b);early=next(v for k,v in new if k=='startupFullscreen');new=[x for x in new if x[0]!='startupFullscreen'];assert len(old)==len(new);protected=[];changed=[]
for (k,v),(l,w) in zip(old,new):
 assert k==l
 if v==w:protected.append({'id':k,'sha256':sha(v)})
 else:
  changed.append(k);assert k in ['blokRayaLoading','patch8dViewportTouch','application'],k
  if k=='application':assert w.replace("case 'startRace':await startRace();","case 'startRace':RaceViewport.requestFullscreen();await startRace();")==v
  if k=='patch8dViewportTouch':
   restored=w.replace('const {fullscreenElement,requestFullscreen,toggleFullscreen}=root.RaceViewport;\n','')
   for name in ['fullscreenElement','requestFullscreen','toggleFullscreen']:
    oldfn=next(x for x in v.splitlines()if x.startswith('function '+name+'('));assert oldfn in early
    if name=='fullscreenElement':restored=restored.replace('function syncFullscreen()',oldfn+'\nfunction syncFullscreen()')
    elif name=='requestFullscreen':restored=restored.replace('function viewport()',oldfn+'\nfunction viewport()')
    else:restored=restored.replace('function viewport()',oldfn+'\nfunction viewport()')
   assert restored==v,'Joystick/viewport functions must remain byte-identical'
# Reconstruct the entire old distribution to verify no unrelated markup changes.
restored=b
for (k,v),(l,w) in zip(old,new):
 if v!=w:restored=restored.replace(w,v,1)
restored=re.sub(r'<script id="startupFullscreen">.*?</script>\n','',restored,flags=re.S)
restored=re.sub(r'<style id="patch8eStartupStyles">.*?</style>\n','',restored,flags=re.S)
restored=restored.replace('<button id="brEnterButton" type="button" autofocus>Masuk BlokRaya</button>','')
assert restored==a,'Unrelated HTML/markup changed'
styles=lambda s:re.findall(r'<style([^>]*)>(.*?)</style>',s,re.S)
assert styles(a)==[x for x in styles(b)if'id="patch8eStartupStyles"'not in x[0]]
assert [x for x in a.splitlines()if x.rstrip()!=x]==[x for x in b.splitlines()if x.rstrip()!=x]
assert (R/'index.html').read_bytes()==subprocess.check_output(['git','show',BASE+':index.html'],cwd=R)
changes=set(subprocess.check_output(['git','diff','--name-only',BASE],cwd=R).decode().splitlines());oldpaths=subprocess.check_output(['git','ls-tree','-r','--name-only','-z',BASE],cwd=R).decode().split('\0');assert not any(p in changes for p in oldpaths if p and p!='README.md')
r={'status':'passed','baseline_commit':BASE,'baseline_bytes':len(a.encode()),'html_bytes':len(b.encode()),'growth_bytes':len(b.encode())-len(a.encode()),'html_sha256':sha(b),'protected_script_payloads':protected,'changed_scripts':changed,'checks':['Only loader startup gate, fullscreen function location and removal of race-start automatic request change','Original fullscreen helper functions are moved verbatim, not duplicated','Analog/deadzone/multitouch/HUD/viewport functions byte-identical after restoring helper location','Engine/AI/buffs/13 stages/models/posters/audio/auth/PIN/onboarding/podium/assessment payloads unchanged','All existing styles retained; only small CTA style added','Previous distribution and online index.html unchanged','Original overlay gains one CTA only; no new wizard, duplicate loader or unrelated markup changes']}
(D/'scope-tests.json').write_text(json.dumps(r,indent=2));print('PASS',len(protected),'protected payloads;',r['growth_bytes'],'bytes growth')
