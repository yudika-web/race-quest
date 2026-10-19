"""Build a standalone Stage 1 presentation from the immutable final 14-character game."""
from pathlib import Path
import re,json,hashlib
D=Path(__file__).resolve().parents[2];B=D/'stage1-pontianak'
h=(D/'race-quest-pro-batch4.html').read_text()
assert hashlib.sha256(h.encode()).hexdigest()==json.loads((B/'baseline.json').read_text())['html_sha256']
old="id:'kampung',name:'Kampung Hijau'";new="id:'kampung',name:'Pontianak · Jalanan Kota'";assert h.count(old)==1;h=h.replace(old,new)
m=list(re.finditer(r'<script\b[^>]*>.*?</script>',h,re.S));end=m[3].end();h=h[:end]+'\n<script id="pontianakStageVisuals">\n'+(B/'source/city.js').read_text()+'\n</script>'+h[end:]
(D/'race-quest-pro-pontianak-stage1.html').write_text(h);print('Standalone bytes',len(h.encode()))
