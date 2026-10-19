"""Only append the Stage 2 visual layer and change the displayed name, preserving Stage 1."""
from pathlib import Path
import re,json,hashlib
D=Path(__file__).resolve().parents[2];B=D/'stage2-mempawah';h=(D/'race-quest-pro-pontianak-stage1.html').read_text()
assert hashlib.sha256(h.encode()).hexdigest()==json.loads((B/'baseline.json').read_text())['html_sha256']
old="id:'kapuas',name:'Tepi Sungai Kapuas'";new="id:'kapuas',name:'Mempawah · Jalanan Taman'";assert h.count(old)==1;h=h.replace(old,new)
m=re.search(r'<script id="pontianakStageVisuals">.*?</script>',h,re.S);assert m
end=m.end();h=h[:end]+'\n<script id="mempawahStageVisuals">\n'+(B/'source/garden.js').read_text()+'\n</script>'+h[end:]
(D/'race-quest-pro-mempawah-stage2.html').write_text(h);print('Standalone bytes',len(h.encode()))
