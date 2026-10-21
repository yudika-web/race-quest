from pathlib import Path
from PIL import Image
import base64,json
D=Path(__file__).resolve().parents[1];assets={}
for key,name in [('kayong_utara-landmark.webp','sail-close'),('kayong_utara-race.webp','kayong-race'),('ketapang-landmark.webp','ale-close'),('ketapang-race.webp','ketapang-race')]:
 p=D/'screenshots/after'/(name+'.png');im=Image.open(p).convert('RGB').resize((512,320),Image.Resampling.LANCZOS);f=D/'thumbnails'/key;im.save(f,'WEBP',quality=70,method=6);raw=f.read_bytes();assets[key]={'mime':'image/webp','uri':'data:image/webp;base64,'+base64.b64encode(raw).decode(),'width':512,'height':320,'bytes':len(raw),'source':'screenshots/after/'+name+'.png'}
(D/'thumbnails/assets.json').write_text(json.dumps(assets,separators=(',',':')));print({k:v['bytes']for k,v in assets.items()})
