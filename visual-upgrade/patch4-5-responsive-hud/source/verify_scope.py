from pathlib import Path
import re,json,hashlib,subprocess
D=Path(__file__).resolve().parents[2];B=D/'patch4-5-responsive-hud';baseline='82c0f778b480d669b236b76517add5cd86e35fb2';raw=(D/'race-quest-pro-patch4-5.html').read_bytes();h=raw.decode();original=(D/'race-quest-pro-patch4.html').read_text();sha=lambda x:hashlib.sha256(x.encode()if isinstance(x,str)else x).hexdigest()
for tag,id in [('style','patch45HUDStyles'),('script','patch45HUD')]:
 h,n=re.subn(r'<'+tag+r' id="'+id+r'"[^>]*>.*?</'+tag+'>','',h,flags=re.S);assert n==1
s=list(re.finditer(r'<script\b[^>]*>.*?</script>',h,re.S));pos=s[18].end();assert h[pos]=='\n';h=h[:pos]+h[pos+1:]
changes=json.loads((B/'bounded-changes.json').read_text())
for c in reversed(changes):
 i=c['offset'];assert h[i:i+len(c['new'])]==c['new'],c['old'][:70];h=h[:i]+c['old']+h[i+len(c['new']):]
assert h==original,'Unbounded edit outside documented presentation hooks'
ss=lambda x:list(re.finditer(r'<script\b[^>]*>(.*?)</script>',x,re.S));old=ss(original);new=ss(raw.decode());components={}
for index,name in [(2,'RaceCore / physics / assessment'),(3,'Scenery'),(4,'Pontianak'),(5,'Mempawah'),(6,'Singkawang'),(7,'Renderer / models'),(10,'Garage workshop'),(11,'Stage selection'),(12,'Audio'),(13,'VFX'),(15,'Strategic buff system'),(16,'Original buff reward callbacks'),(17,'Smart Racing AI'),(18,'AI indicator/audio layer')]:
 assert old[index][1]==new[index][1],name;components[name]=sha(old[index][1])
entries=subprocess.check_output(['git','ls-tree','-r','-z',baseline]).split(b'\0');protected={}
for row in entries:
 if not row:continue
 meta,path=row.split(b'\t',1);path=path.decode()
 if path=='index.html' or path.startswith('visual-upgrade/'):protected[path]=meta.decode().split()[2]
paths=list(protected);hashes=subprocess.check_output(['git','hash-object','--stdin-paths'],input='\n'.join(paths)+'\n',text=True).splitlines();assert len(hashes)==len(paths)
for path,digest in zip(paths,hashes):assert protected[path]==digest,path
report={'status':'passed','baseline':baseline,'baseline_html_sha256':sha(original),'html_sha256':sha(raw),'html_bytes':len(raw),'growth_bytes':len(raw)-len(original.encode()),'under_25_decimal_MB':len(raw)<25000000,'bounded_changes':len(changes),'reverse_reconstruction_exact':True,'protected_historical_files':len(paths),'component_sha256_unchanged':components,'scope':'New HUD markup/styles/presentation plus routing restart through existing Pause and controls release on input mode changes. Core/AI/buff/physics/assessment/audio/VFX files remain identical.'}
(B/'scope-tests.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
