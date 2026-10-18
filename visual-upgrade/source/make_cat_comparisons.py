from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
D=Path(__file__).resolve().parents[1]/'cat-refinement'
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',24)
small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
for name in ['face','front','profile','rear','garage','race']:
 images=[Image.open(D/p/(name+'.png')).convert('RGB') for p in ['before','after']]
 w,h=images[0].size
 output=Image.new('RGB',(2*w,h+66),'#0c1c30');draw=ImageDraw.Draw(output)
 for i,im in enumerate(images):
  output.paste(im,(i*w,66));draw.text((i*w+22,12),'SEBELUM — e5d7e07' if i==0 else 'SESUDAH — penyempurnaan Kucing',fill='white',font=font)
 output.save(D/f'comparison-{name}.jpg',quality=95)
# Review sheet: matching crops from real renders, no model/image retouching.
W=1200;rows=[('face','Wajah / moncong / paw',627),('profile','Siluet samping / sambungan lengan',627),('race','Kamera balapan sebenarnya',417)]
output=Image.new('RGB',(W,sum(h+55 for _,_,h in rows)+52),'#0c1c30');draw=ImageDraw.Draw(output)
draw.text((18,12),'KUCING: SEBELUM',fill='white',font=font);draw.text((618,12),'KUCING: SESUDAH',fill='white',font=font)
y=52
for name,label,h in rows:
 draw.text((18,y+12),label,fill='#8bd4e6',font=small)
 for i,p in enumerate(['before','after']):
  im=Image.open(D/p/(name+'.png')).convert('RGB');im=im.resize((600,h),Image.Resampling.LANCZOS);output.paste(im,(i*600,y+48))
 y+=h+55
output.save(D/'cat-refinement-sheet.jpg',quality=95)
print('Cat before/after sheets created from game renders.')
