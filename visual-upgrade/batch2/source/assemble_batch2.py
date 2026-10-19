"""Incremental build from verified Batch 1. Reuses renderer/engine already embedded.
Run python3 visual-upgrade/batch2/source/assemble_batch2.py [--preview].
--preview permits missing portraits only during direct GLB portrait rendering.
"""
from pathlib import Path
import json,re,base64,hashlib,sys
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parents[2];B=D/'batch2';S=B/'source';IDS=['bebek','ayam','domba','robot']
html=(D/'race-quest-pro-batch1.html').read_text()
assert hashlib.sha256(html.encode()).hexdigest()==json.loads((B/'baseline.json').read_text())['html_sha256']
assets=json.loads(re.search(r'<script id="assetData"[^>]*>(.*?)</script>',html,re.S)[1])
for id in IDS:
 for prefix,suffix,ext,folder,mime in [('kart_','','glb','models','model/gltf-binary'),('kart_','_low','glb','models','model/gltf-binary'),('avatar_','','webp','avatars','image/webp'),('avatar_','_happy','webp','avatars','image/webp')]:
  key=prefix+id+suffix+'.'+ext;file=B/folder/key
  if not file.exists() and '--preview' in sys.argv and prefix=='avatar_':continue
  data=file.read_bytes();assets[key]={'uri':'data:'+mime+';base64,'+base64.b64encode(data).decode(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
html=re.sub(r'(<script id="assetData"[^>]*>).*?(</script>)',lambda m:m[1]+json.dumps(assets,separators=(',',':'))+m[2],html,flags=re.S)
# Extend the shared Batch 1 rigid animation/LOD path, without a second renderer.
old="'kart_sora.glb':'kart_sora_low.glb'"
assert html.count(old)==1
html=html.replace(old,old+','+','.join("'kart_%s.glb':'kart_%s_low.glb'"%(id,id) for id in IDS))
old='[1.39,2.05,2.25]][character]';new='[1.39,2.05,2.25],[1.25,1.75,1.95],[1.28,1.85,2.05],[1.27,1.85,2.05],[1.30,1.85,2.05]][character]'
assert old in html;html=html.replace(old,new)
# Old model phases are byte-for-byte the same; all four new models get an offset.
old="file.includes('bimo')?1.7:2.6";new="file.includes('bimo')?1.7:file.includes('sora')?2.6:file.includes('bebek')?.4:file.includes('ayam')?1.2:file.includes('domba')?2.0:3.1"
assert old in html;html=html.replace(old,new)
# One existing widget/observer, extended to the four new identities.
old=(D/'batch1/source/batch1_preview.js').read_text();new=old.replace('[1,2,3].includes','[1,2,3,4,5,6,7].includes').replace("3:'sora'","3:'sora',4:'bebek',5:'ayam',6:'domba',7:'robot'")
assert html.count(old)==1;html=html.replace(old,new)
(D/'race-quest-pro-batch2.html').write_text(html)
print('Batch 2 HTML:',len(html.encode()),'bytes; embedded keys:',len(assets))
