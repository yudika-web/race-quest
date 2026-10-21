from pathlib import Path
import hashlib,json,re
D=Path(__file__).resolve().parents[1];V=D.parent;baseline=V/'blokraya-pro-final.html';s=baseline.read_text()
assert hashlib.sha256(baseline.read_bytes()).hexdigest()=='6ec7882aa994377e6de871ee59a4837c758b969acc5ca09c1de5f0b86065d405'
# Prototype adapter is loaded before the application first constructs a world.
needle='<script id="studentOnboarding">';assert s.count(needle)==1
s=s.replace(needle,'<script id="patch8aLandmarks">\n'+(D/'source/landmarks.js').read_text()+'\n</script>\n'+needle)
f=D/'thumbnails/assets.json'
if f.exists():
 m=re.search(r'(<script id="patch1StageAssets"[^>]*>)(.*?)(</script>)',s,re.S);assets=json.loads(m[2]);assets.update(json.loads(f.read_text()));s=s[:m.start(2)]+json.dumps(assets,separators=(',',':'))+s[m.end(2):]
(V/'blokraya-patch8a-landmarks.html').write_text(s);print(len(s.encode()),'bytes; growth',len(s.encode())-baseline.stat().st_size)
