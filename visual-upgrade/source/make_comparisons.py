from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
D=Path(__file__).resolve().parents[1]/'comparisons'
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22)
small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
sheet=Image.new('RGB',(1200,2110),'#0c1c30');draw=ImageDraw.Draw(sheet)
draw.text((24,18),'RACE QUEST — Kucing / Sport',font=font,fill='white')
for j,(angle,label) in enumerate([('front','DEPAN'),('rear','BELAKANG'),('side','SAMPING'),('race','SUDUT KAMERA BALAPAN')]):
 y=60+j*510;draw.text((20,y),label,font=small,fill='#84cfe5')
 for i,prefix in enumerate(['before','after']):
  im=Image.open(D/f'{prefix}-{angle}.png').convert('RGB').resize((600,480),Image.Resampling.LANCZOS);sheet.paste(im,(i*600,y+24));draw.text((i*600+24,y+40),'SEBELUM' if i==0 else 'SESUDAH',font=font,fill='#ffffff')
sheet.save(D/'comparison-sheet.jpg',quality=94)
for angle in ['front','rear','side','race','game-race']:
 ims=[Image.open(D/f'{p}-{angle}.png').convert('RGB') for p in ['before','after']];w,h=ims[0].size;out=Image.new('RGB',(w*2,h+48),'#0c1c30');dr=ImageDraw.Draw(out)
 for i,im in enumerate(ims):out.paste(im,(i*w,48));dr.text((i*w+24,12),'SEBELUM' if i==0 else 'SESUDAH',font=font,fill='white')
 out.save(D/f'comparison-{angle}.jpg',quality=94)
print('Comparison sheets assembled from actual, unretouched WebGL screenshots.')
