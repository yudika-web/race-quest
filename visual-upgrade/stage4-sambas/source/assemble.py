from pathlib import Path
import re,json,hashlib,sys
D=Path(__file__).resolve().parents[2];B=D/'stage4-sambas';base=(D/'blokraya-patch5.html').read_text();h=base;changes=[]
def change(old,new):
 global h
 assert h.count(old)==1,(old[:100],h.count(old));h=h.replace(old,new);changes.append(dict(old=old,new=new,count=1))
meta=json.loads((B/'stages.json').read_text());next(m for m in meta if m['id']=='sambas')['available']=True
old=re.search(r'<script id="patch1StageCatalog"[^>]*>.*?</script>',h,re.S)[0]
new='<script id="stage6aTrack" type="application/json">'+json.dumps(json.loads((B/'track.json').read_text()),separators=(',',':'))+'</script>\n<script id="sambasStageVisuals">'+(B/'source/river.js').read_text()+'</script>\n<script id="patch1StageCatalog" type="application/json">'+json.dumps(meta,ensure_ascii=False,separators=(',',':'))+'</script>'
change(old,new)
assets_path=B/'thumbnails/assets.json'
if assets_path.exists():
 old=re.search(r'<script id="patch1StageAssets"[^>]*>.*?</script>',h,re.S)[0];assets=json.loads(re.search(r'>(.*?)</script>',old,re.S)[1]);new_assets=json.loads(assets_path.read_text());assert not(set(assets)&set(new_assets));assets.update(new_assets);change(old,'<script id="patch1StageAssets" type="application/json">'+json.dumps(assets,separators=(',',':'))+'</script>')
# Scoped sky palette uses the existing shader/clouds and simulation clock unchanged.
# Historical palette is delegated byte-for-byte for all other worlds.
old="const config=JSON.parse(document.getElementById('stage6aTrack').textContent);"
new="const sky=root.RaceRenderer.prototype.skyPalette;root.RaceRenderer.prototype.skyPalette=function(){if(this.track?.id!=='sambas')return sky.call(this);const w=this.weather==='rain'?.55:this.weather==='fog'?.75:0;return{top:[.28,.64,.86].map((v,i)=>v*(1-w)+[.47,.57,.64][i]*w),horizon:[.83,.90,.90].map((v,i)=>v*(1-w)+[.73,.79,.81][i]*w)}};\n"+old
change(old,new)
output=Path('/tmp/blokraya-6a/candidate.html');output.parent.mkdir(parents=True,exist_ok=True);output.write_text(h);(B/'bounded-changes.json').write_text(json.dumps(changes,indent=2));(B/'candidate-metrics.json').write_text(json.dumps({'baseline':'346c915ca0272f6b10732fdd99fe28bcde87fb62','html_bytes':len(h.encode()),'baseline_bytes':len(base.encode()),'growth_bytes':len(h.encode())-len(base.encode()),'html_sha256':hashlib.sha256(h.encode()).hexdigest()},indent=2))
if '--release' in sys.argv:
 for name in ['physics-tests','item-tests','world-tests','browser-tests','offline-tests','unchanged-renders']:
  report=json.loads((B/(name+'.json')).read_text());assert report['status']=='passed',name
 assert assets_path.exists(),'Real rendered thumbnails required'
 (B/'stages.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2));(D/'blokraya-stage4-sambas.html').write_text(h)
print('candidate bytes',len(h.encode()),'growth',len(h.encode())-len(base.encode()),'release','--release' in sys.argv)
