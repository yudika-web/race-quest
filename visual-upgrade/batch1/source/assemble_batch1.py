"""Create the Batch 1 single-file game from the accepted blocky-cat baseline.
The baseline HTML, cat GLBs, cat source and main/index.html remain untouched.
"""
from pathlib import Path
import json,re,base64,hashlib,sys
sys.dont_write_bytecode=True
from integrate_batch1 import integrate
D=Path(__file__).resolve().parents[2];B=D/'batch1';S=B/'source'
html=(D/'race-quest-visual-upgrade.html').read_text();assert hashlib.sha256(html.encode()).hexdigest()==json.loads((B/'baseline.json').read_text())['html_sha256'],'Use the accepted blocky cat baseline'
assets=json.loads(re.search(r'<script id="assetData"[^>]*>(.*?)</script>',html,re.S)[1])
for id in ['nara','bimo','sora']:
 for suffix in ['', '_low']:
  key='kart_'+id+suffix+'.glb';data=(B/'models'/key).read_bytes();assets[key]={'uri':'data:model/gltf-binary;base64,'+base64.b64encode(data).decode(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
 for suffix in ['', '_happy']:
  key='avatar_'+id+suffix+'.webp';file=B/'avatars'/key
  if not file.exists():
   if '--preview' in sys.argv:continue
   raise FileNotFoundError('Render actual new avatars before final assembly: '+str(file))
  data=file.read_bytes();assets[key]={'uri':'data:image/webp;base64,'+base64.b64encode(data).decode(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
html=re.sub(r'(<script id="assetData"[^>]*>).*?(</script>)',lambda m:m[1]+json.dumps(assets,separators=(',',':'))+m[2],html,flags=re.S)
original=(D/'source/upgraded-renderer.js').read_text();html,renderer=integrate(html,original,S);html=html.replace(original,renderer)
(D/'race-quest-pro-batch1.html').write_text(html);(S/'batch1-renderer.js').write_text(renderer)
print('Batch 1 HTML:',len(html.encode()),'bytes')
