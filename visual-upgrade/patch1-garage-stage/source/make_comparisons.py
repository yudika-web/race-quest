"""Compose unmodified real UI captures; labels and scaling only, no generated imagery."""
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
D=Path(__file__).resolve().parents[1];font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22)
for view in ['garage','closeup','setup']:
 for device in ['desktop','mobile']:
  imgs=[Image.open(D/side/(view+'-'+device+'.png')).convert('RGB')for side in ['before','after']];w=850 if device=='desktop' else 390;thumbs=[ImageOps.contain(im,(w,1300))for im in imgs];h=max(im.height for im in thumbs);out=Image.new('RGB',(w*2+30,h+90),'#102337');draw=ImageDraw.Draw(out)
  for i,(label,im)in enumerate(zip(['BEFORE - Stage 3 baseline','AFTER - PATCH 1'],thumbs)):
   x=i*(w+30);draw.text((x+12,15),label,font=font,fill='white');out.paste(im,(x,65))
  out.save(D/'comparisons'/('comparison-'+view+'-'+device+'.jpg'),quality=92)
# Stage thumbnail contact sheet, exact game render source masters.
W,H=1200,840;out=Image.new('RGB',(W,H),'#102337');draw=ImageDraw.Draw(out)
for i,city in enumerate(['pontianak','mempawah','singkawang']):
 for j,mode in enumerate(['landmark','race']):
  im=Image.open(D/'assets'/(city+'-'+mode+'.png')).convert('RGB');im=ImageOps.contain(im,(390,300));x=i*400;y=j*420;draw.text((x+12,y+18),city.title()+' / '+mode,font=font,fill='white');out.paste(im,(x+5,y+65))
out.save(D/'comparisons'/'stage-render-thumbnails.jpg',quality=92)
