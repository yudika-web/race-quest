from pathlib import Path
import re,json,hashlib,sys
D=Path(__file__).resolve().parents[2];B=D/'stage11-kubu-raya';base=(D/'blokraya-stage10-bromo.html').read_text();h=base;changes=[]
def change(old,new):
 global h
 assert h.count(old)==1,(old[:100],h.count(old));h=h.replace(old,new);changes.append(dict(old=old,new=new,count=1))
meta=json.loads((B/'stages.json').read_text());next(m for m in meta if m['id']=='kubu_raya')['available']=True
old=re.search(r'<script id="patch1StageCatalog"[^>]*>.*?</script>',h,re.S)[0]
new='<script id="stage6hTrack" type="application/json">'+json.dumps(json.loads((B/'track.json').read_text()),separators=(',',':'))+'</script>\n<script id="kubuRayaStageVisuals">'+(B/'source/mangrove.js').read_text()+'</script>\n<script id="patch1StageCatalog" type="application/json">'+json.dumps(meta,ensure_ascii=False,separators=(',',':'))+'</script>'
change(old,new)
old=re.search(r'<script id="patch5CupCatalog"[^>]*>.*?</script>',h,re.S)[0]
change(old,'<script id="patch5CupCatalog" type="application/json">'+json.dumps(json.loads((B/'cups.json').read_text()),ensure_ascii=False,separators=(',',':'))+'</script>')
old='gaps=s.gaps.length,obstacles=s.obstacles.length,level=gaps?'
change(old,"gaps=s.gaps.length+(s.extremeZones||[]).filter(z=>['gap','fork'].includes(z.kind)).length,obstacles=s.obstacles.length+(s.extremeZones||[]).filter(z=>!['gap','fork'].includes(z.kind)).length,level=gaps?")
change('ramps:s.ramps.length,gaps,height',"ramps:s.ramps.length+(s.extremeZones||[]).filter(z=>['gap','fork'].includes(z.kind)).length,gaps,height")
change('</body>','<script id="stage11Mechanics">'+(B/'source/extreme.js').read_text()+'</script>\n</body>')
assets_path=B/'thumbnails/assets.json'
if assets_path.exists():
 old=re.search(r'<script id="patch1StageAssets"[^>]*>.*?</script>',h,re.S)[0];assets=json.loads(re.search(r'>(.*?)</script>',old,re.S)[1]);new_assets=json.loads(assets_path.read_text());assert not(set(assets)&set(new_assets));assets.update(new_assets);change(old,'<script id="patch1StageAssets" type="application/json">'+json.dumps(assets,separators=(',',':'))+'</script>')
output=Path('/tmp/blokraya-6h/candidate.html');output.parent.mkdir(parents=True,exist_ok=True);output.write_text(h);(B/'bounded-changes.json').write_text(json.dumps(changes,indent=2));(B/'candidate-metrics.json').write_text(json.dumps({'baseline':'7fdbc485a50c851a9e02ab2b675fbc5603bb9c50','html_bytes':len(h.encode()),'baseline_bytes':len(base.encode()),'growth_bytes':len(h.encode())-len(base.encode()),'html_sha256':hashlib.sha256(h.encode()).hexdigest()},indent=2))
if '--release' in sys.argv:
 for name in ['physics-tests','item-tests','world-tests','browser-tests','offline-tests','unchanged-renders','mechanics-tests','rescue-browser-tests','render-mechanics-tests','grand-prix-tests','grand-prix-browser-tests']:
  report=json.loads((B/(name+'.json')).read_text());assert report['status']=='passed',name
 assert assets_path.exists(),'Real rendered thumbnails required'
 (B/'stages.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2));(D/'blokraya-stage11-kubu-raya.html').write_text(h)
print('candidate bytes',len(h.encode()),'growth',len(h.encode())-len(base.encode()),'release','--release' in sys.argv)
