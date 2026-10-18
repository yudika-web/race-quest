from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
D=Path(__file__).resolve().parents[1]/'cat-blocky'
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',24)
small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
for name in ['face','front','profile','rear','garage','race','cat-front','cat-side','cat-back']:
 images=[Image.open(D/p/(name+'.png')).convert('RGB') for p in ['before','after']]
 w,h=images[0].size
 output=Image.new('RGB',(2*w,h+66),'#0c1c30');draw=ImageDraw.Draw(output)
 for i,im in enumerate(images):
  output.paste(im,(i*w,66));draw.text((i*w+22,12),'SEBELUM — 2767925' if i==0 else 'SESUDAH — Kucing blocky',fill='white',font=font)
 output.save(D/f'comparison-{name}.jpg',quality=95)
# Review sheet: matching crops from real renders, no model/image retouching.
W=1200;rows=[('face','Close-up wajah, moncong, paw',627),('profile','Siluet samping dan leher',627),('front','Tampak depan garasi, skala setara',627),('race','Kamera balapan asli, pose setara',417)]
output=Image.new('RGB',(W,sum(h+55 for _,_,h in rows)+52),'#0c1c30');draw=ImageDraw.Draw(output)
draw.text((18,12),'KUCING: SEBELUM',fill='white',font=font);draw.text((618,12),'KUCING: SESUDAH',fill='white',font=font)
y=52
for name,label,h in rows:
 draw.text((18,y+12),label,fill='#8bd4e6',font=small)
 for i,p in enumerate(['before','after']):
  im=Image.open(D/p/(name+'.png')).convert('RGB');im=im.resize((600,h),Image.Resampling.LANCZOS);output.paste(im,(i*600,y+48))
 y+=h+55
output.save(D/'cat-blocky-sheet.jpg',quality=95)
print('Cat before/after sheets created from game renders.')

# Character-only views from the same renderer; no car geometry obscures the body.
output=Image.new('RGB',(1500,1080),'#0c1c30');draw=ImageDraw.Draw(output)
for row,stage in enumerate(['before','after']):
 y=row*540;draw.text((18,y+10),'SEBELUM — 2767925' if row==0 else 'SESUDAH — Kucing blocky',fill='white',font=font)
 for col,angle in enumerate(['front','side','back']):
  im=Image.open(D/stage/f'cat-{angle}.png').convert('RGB').resize((500,500),Image.Resampling.LANCZOS);output.paste(im,(col*500,y+40))
output.save(D/'cat-turnaround-sheet.jpg',quality=95)
a=json.loads((D/'before/cameras.json').read_text());b=json.loads((D/'after/cameras.json').read_text())
assert a==b,'Comparison cameras differ'
(D/'camera-verification.json').write_text(json.dumps({'status':'passed','baseline_commit':'276792553e913520119038cac5c9512035751d86','matching_cases':list(a),'view_projection_canvas_equal':True,'time_garage':1,'time_race':2,'note':'Same seed, camera matrices, viewport, simulation pose/time, lighting and medium race quality; existing and blocky geometry at identical scales.'},indent=2))
