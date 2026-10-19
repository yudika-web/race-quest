"""Label/compose actual captured game pixels; no illustration or generated artwork."""
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
D=Path(__file__).resolve().parents[1];O=D/'comparisons';O.mkdir(exist_ok=True);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22)
for name in ['drift','turbo','shield','bubble','landing','impact']:
 out=Image.new('RGB',(1310,505),'#102337');draw=ImageDraw.Draw(out)
 for i,side in enumerate(['before','after']):
  im=Image.open(D/'screenshots'/(side+'-'+name+'.png')).convert('RGB');im=ImageOps.contain(im,(640,430));x=i*670;draw.text((x+12,14),side.upper()+' / '+name,font=font,fill='white');out.paste(im,(x,65))
 out.save(O/('comparison-'+name+'.jpg'),quality=91)
