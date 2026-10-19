"""Append Stage 3 scenery; only its display name and visual default weather change."""
from pathlib import Path
import re,json,hashlib
D=Path(__file__).resolve().parents[2];B=D/'stage3-singkawang';h=(D/'race-quest-pro-mempawah-stage2.html').read_text()
assert hashlib.sha256(h.encode()).hexdigest()==json.loads((B/'baseline.json').read_text())['html_sha256']
old="id:'hutan',name:'Hutan Hujan Kalimantan',seed:8391,weather:'fog'";new="id:'hutan',name:'Singkawang · Pantai Meriah',seed:8391,weather:'clear'";assert h.count(old)==1;h=h.replace(old,new)
m=re.search(r'<script id="mempawahStageVisuals">.*?</script>',h,re.S);assert m;end=m.end();h=h[:end]+'\n<script id="singkawangStageVisuals">\n'+(B/'source/coast.js').read_text()+'\n</script>'+h[end:]
(D/'race-quest-pro-singkawang-stage3.html').write_text(h);print('Standalone bytes',len(h.encode()))
