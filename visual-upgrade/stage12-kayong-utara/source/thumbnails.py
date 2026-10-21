from pathlib import Path
from PIL import Image
import base64,json
B=Path(__file__).resolve().parents[1];assets={}
for key,source in [('kayong_utara-landmark.webp','sail-karimata.png'),('kayong_utara-race.webp','gameplay.png')]:
 im=Image.open(B/'screenshots'/source).convert('RGB').resize((640,400),Image.Resampling.LANCZOS);f=B/'thumbnails'/key;im.save(f,'WEBP',quality=75,method=6);raw=f.read_bytes();assets[key]={'mime':'image/webp','uri':'data:image/webp;base64,'+base64.b64encode(raw).decode(),'width':640,'height':400,'bytes':len(raw),'source':'screenshots/'+source}
(B/'thumbnails/assets.json').write_text(json.dumps(assets,separators=(',',':')));print({k:v['bytes']for k,v in assets.items()})
