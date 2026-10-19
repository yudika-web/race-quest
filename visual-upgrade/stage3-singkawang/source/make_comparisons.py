from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
B=Path(__file__).resolve().parents[1];font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',23);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
r=json.loads((B/'capture-report.json').read_text())
assert r['status']=='passed'
for name in r['views']:assert r['before'][name]==r['after'][name],name
for ident,title,views in [('naga','Tugu Naga - Singkawang',['tugu-naga','tugu-naga-race']),('imlek','Gapura dan ornamen Imlek',['gapura-imlek','gapura-imlek-race']),('beach','Pantai dan promenade',['beach-road-race','coast-overview']),('detail-gap','Detail naga dan ramp/gap asli',['dragon-face-close','preserved-ramp-gap'])]:
 im=Image.new('RGB',(1600,1128),'#102539');d=ImageDraw.Draw(im);d.text((24,16),'RACE QUEST - '+title,font=font,fill='white');d.text((24,57),'SEBELUM - baseline Mempawah',font=small,fill='#c9dfef');d.text((824,57),'SESUDAH - Stage 3 Singkawang',font=small,fill='#a7e1bd')
 for row,view in enumerate(views):
  for col,mode in enumerate(['before','after']):
   shot=Image.open(B/mode/(view+'.png')).convert('RGB');shot.thumbnail((798,499));im.paste(shot,(col*800,90+row*520))
 d.text((24,1101),'Render engine game asli; kamera, resolusi, pose, waktu dan cuaca Cerah setara.',font=small,fill='white');im.save(B/'comparisons'/('comparison-'+ident+'.jpg'),quality=91)
print('Four matched before-after comparison sheets generated')
