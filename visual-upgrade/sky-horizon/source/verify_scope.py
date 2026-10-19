from pathlib import Path
import re,json,hashlib,subprocess
D=Path(__file__).resolve().parents[2];B=D/'sky-horizon';baseline='b5611f4937c6139024779265f0b8434545b77cbf';old=(D/'race-quest-pro-patch4-5.html').read_bytes();raw=(D/'race-quest-pro-sky-horizon.html').read_bytes();h=raw.decode();sha=lambda v:hashlib.sha256(v).hexdigest()
changes=json.loads((B/'bounded-changes.json').read_text())
for c in reversed(changes):
 i=c['offset'];assert h[i:i+len(c['new'])]==c['new'];h=h[:i]+c['old']+h[i+len(c['new']):]
assert h.encode()==old
scripts=lambda v:list(re.finditer(rb'<script\b[^>]*>(.*?)</script>',v,re.S));a,b=scripts(old),scripts(raw);assert len(a)==len(b);hashes={}
for i,(x,y)in enumerate(zip(a,b)):
 if i!=7:assert x[1]==y[1];hashes[str(i)]=sha(y[1])
# Historical assets, HTML, sources and archives must not change.
entries=subprocess.check_output(['git','ls-tree','-r','-z',baseline]).split(b'\0');protected={}
for entry in entries:
 if not entry:continue
 meta,name=entry.split(b'\t',1);name=name.decode()
 if name=='index.html'or name.startswith('visual-upgrade/')or name.endswith('.zip'):protected[name]=meta.split()[2].decode()
paths=list(protected);actual=subprocess.check_output(['git','hash-object','--stdin-paths'],input=('\n'.join(paths)+'\n').encode(),cwd=D.parent).decode().splitlines()
for name,digest in zip(paths,actual):assert digest==protected[name],name
report=dict(status='passed',baseline_commit=baseline,html_bytes=len(raw),baseline_bytes=len(old),growth_bytes=len(raw)-len(old),under_25_decimal_MB=len(raw)<25000000,html_sha256=sha(raw),reverse_reconstruction_exact=True,renderer_only_changes=len(changes),unchanged_script_sha256=hashes,protected_historical_files=len(protected),scope='Only sky init/draw/palette, distant geometry haze and fog color. No race camera, material lighting, models, gameplay, controls, UI or world layout edits.')
(B/'scope-tests.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
