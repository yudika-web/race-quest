from pathlib import Path
import re,json,hashlib,difflib
D=Path(__file__).resolve().parents[1];V=D.parent
old=(V/'blokraya-patch8e-startup.html').read_text();new=(V/'blokraya-patch8f-economy.html').read_text()
script=lambda s:re.findall(r'<script\b([^>]*)>([\s\S]*?)</script>',s)
a,b=script(old),script(new);assert len(a)==len(b)
changed=[];protected=[]
for i,(x,y) in enumerate(zip(a,b)):
 assert x[0]==y[0]
 if x!=y:
  assert 'function normalizeData' in x[1] or 'async function finish()' in x[1];changed.append(i)
 else:protected.append({'index':i,'attributes':x[0],'sha256':hashlib.sha256(x[1].encode()).hexdigest()})
assert len(changed)==2
# Exact reconstruction: no asset, markup or CSS changes other than the new purchase dialog.
rebuilt=old
for i in changed:
 rebuilt=rebuilt.replace(a[i][1],b[i][1],1)
insert=new[new.index('<dialog id="characterPurchaseDialog"'):new.index('</body>')]
assert rebuilt.replace('</body>',insert+'</body>')==new
(D/'scope-results.json').write_text(json.dumps({'passed':True,'changed_scripts':changed,'protected_identical_scripts':protected,'outside_scripts':'Only new purchase dialog; all original markup/styles/embedded assets identical.'},indent=2))
for i,name in zip(changed,['core','application']):
 (D/(name+'-changes.diff')).write_text(''.join(difflib.unified_diff(a[i][1].splitlines(True),b[i][1].splitlines(True),fromfile='8E/'+name,tofile='8F/'+name)))
print('Scope passed:',len(protected),'script payloads unchanged; original markup and styles unchanged.')
