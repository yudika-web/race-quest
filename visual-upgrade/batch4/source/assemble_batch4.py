"""Incremental standalone build from verified Batch 3; no second engine."""
from pathlib import Path
import json,re,base64,hashlib,sys
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parents[2];B=D/'batch4';IDS=['panda','koala','rakun']
html=(D/'race-quest-pro-batch3.html').read_text();assert hashlib.sha256(html.encode()).hexdigest()==json.loads((B/'baseline.json').read_text())['html_sha256']
assets=json.loads(re.search(r'<script id="assetData"[^>]*>(.*?)</script>',html,re.S)[1])
for id in IDS:
 for prefix,suffix,ext,folder,mime in [('kart_','','glb','models','model/gltf-binary'),('kart_','_low','glb','models','model/gltf-binary'),('avatar_','','webp','avatars','image/webp'),('avatar_','_happy','webp','avatars','image/webp')]:
  key=prefix+id+suffix+'.'+ext;f=B/folder/key
  if not f.exists() and '--preview' in sys.argv and prefix=='avatar_':continue
  data=f.read_bytes();assets[key]={'uri':'data:'+mime+';base64,'+base64.b64encode(data).decode(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
html=re.sub(r'(<script id="assetData"[^>]*>).*?(</script>)',lambda m:m[1]+json.dumps(assets,separators=(',',':'))+m[2],html,flags=re.S)
old="'kart_rubah.glb':'kart_rubah_low.glb'";assert html.count(old)==1
html=html.replace(old,old+','+','.join("'kart_%s.glb':'kart_%s_low.glb'"%(id,id) for id in IDS))
old='[1.34,1.95,2.15]][character]';new='[1.34,1.95,2.15],[1.27,1.85,2.05],[1.27,2.05,2.25],[1.30,1.90,2.10]][character]';assert old in html;html=html.replace(old,new)
old="file.includes('tikus')?1.6:2.9";new="file.includes('tikus')?1.6:file.includes('rubah')?2.9:file.includes('panda')?.6:file.includes('koala')?1.5:2.8";assert old in html;html=html.replace(old,new)
old='[1,2,3,4,5,6,7,8,9,10].includes';assert old in html;html=html.replace(old,'[1,2,3,4,5,6,7,8,9,10,11,12,13].includes')
old="10:'rubah'";assert old in html;html=html.replace(old,"10:'rubah',11:'panda',12:'koala',13:'rakun'")
(D/'race-quest-pro-batch4.html').write_text(html);print('Batch 4 HTML:',len(html.encode()),'bytes;',len(assets),'asset keys')
