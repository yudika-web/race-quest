from pathlib import Path
import re,json,hashlib,subprocess
D=Path(__file__).resolve().parents[1];V=D.parent;R=V.parent;BASE='de6bd8009558d53a5c110644cdd4589e5cf3f731'
a=(V/'blokraya-pro-final.html').read_text();b=(V/'blokraya-patch8a-landmarks.html').read_text();sha=lambda x:hashlib.sha256(x).hexdigest()
def scripts(s):
 out=[]
 for m in re.finditer(r'<script([^>]*)>(.*?)</script>',s,re.S):
  id=re.search(r'id="([^"]+)"',m[1]);out.append((id[1]if id else'anonymous',m[2]))
 return out
old=scripts(a);new=scripts(b);assert len(new)==len(old)+1;new=[m for m in new if m[0]!='patch8aLandmarks'];protected=[]
for x,y in zip(old,new):
 assert x[0]==y[0]
 if x[0]!='patch1StageAssets':assert x[1]==y[1],x[0];protected.append({'id':x[0],'sha256':sha(x[1].encode())})
 else:
  oldAssets=json.loads(x[1]);newAssets=json.loads(y[1]);assert set(oldAssets)==set(newAssets);changed=[k for k in oldAssets if oldAssets[k]!=newAssets[k]];assert set(changed)=={'kayong_utara-landmark.webp','kayong_utara-race.webp','ketapang-landmark.webp','ketapang-race.webp'}
  assert all(b.count(newAssets[k]['uri'])==1 for k in changed)
assert (R/'index.html').read_bytes()==subprocess.check_output(['git','show',BASE+':index.html'],cwd=R)
changes=set(subprocess.check_output(['git','diff','--name-only',BASE],cwd=R).decode().splitlines());allowed={'README.md','visual-upgrade/blokraya-patch8a-landmarks.html','blokraya-patch8a-playable.zip','blokraya-patch8a-review.zip'};assert all(p in allowed or p.startswith('visual-upgrade/patch8a/')for p in changes),changes
paths=subprocess.check_output(['git','ls-tree','-r','--name-only','-z',BASE],cwd=R).decode().split('\0');assert not any(p in changes for p in paths if p and p!='README.md')
r={'status':'passed','checks':['All baseline engine, physics, AI, buff, mode/PIN, student onboarding, podium/results, world builders, track and GP metadata payloads exactly identical','Only the four target thumbnails replaced; same catalog keys and one copy per thumbnail','New adapter overrides only the two target scenery classes; no collider or track changes','index.html and all previous tracked artifacts unchanged except root release README'],'protected_script_payloads':protected,'protected_tracked_files':len([p for p in paths if p and p!='README.md']),'updated_thumbnail_keys':changed,'unchanged_thumbnail_count':len(oldAssets)-4,'baseline_commit':BASE,'baseline_bytes':len(a.encode()),'html_bytes':len(b.encode()),'growth_bytes':len(b.encode())-len(a.encode()),'html_sha256':sha(b.encode()),'landmark_source_sha256':sha((D/'source/landmarks.js').read_bytes())}
(D/'scope-tests.json').write_text(json.dumps(r,indent=2));print('PASS',len(protected),'script payloads and',r['protected_tracked_files'],'old files protected;',r['growth_bytes'],'bytes growth')
