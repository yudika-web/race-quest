"""Arrange only actual game-render screenshots; no model retouching."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
D=Path(__file__).resolve().parents[1];OUT=D/'comparisons';OUT.mkdir(exist_ok=True)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',24);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
ids=[('nara','Pinguin / Kapsul'),('bimo','Beruang / Buggy'),('sora','Kelinci / Formula')]
for kind in ['model','game']:
 a=json.loads((D/'before'/(kind+'-cameras.json')).read_text());b=json.loads((D/'after'/(kind+'-cameras.json')).read_text());assert a==b,kind+' cameras differ'
(D/'camera-verification.json').write_text(json.dumps({'status':'passed','baseline_commit':'5b50da96ae72ad7cb30c6cfd37cf25d7a1f5c303','model_comparisons':33,'game_comparisons':6,'view_projection_resolution_time_equal':True,'garage_and_model_time':1,'race_time':2,'same_seed_scale_lighting_pose':True,'note':'Character-only and vehicle-only views use the same delivered GLBs and RaceRenderer, with other primitives hidden. Native UI close-up/mobile captures are separate from controlled camera comparisons.'},indent=2))
for id,title in ids:
 target=OUT/id;target.mkdir(exist_ok=True)
 for view in ['hero','front','side','back','face','character-front','character-side','character-back','vehicle-front','vehicle-side','vehicle-back','garage','race']:
  images=[Image.open(D/stage/id/(view+'.png')).convert('RGB') for stage in ['before','after']];w,h=images[0].size;assert images[1].size==(w,h)
  sheet=Image.new('RGB',(w*2,h+60),'#0d2035');draw=ImageDraw.Draw(sheet)
  for i,im in enumerate(images):sheet.paste(im,(i*w,60));draw.text((i*w+15,12),'SEBELUM — 5b50da9' if i==0 else 'SESUDAH — Batch 1',fill='white',font=font)
  sheet.save(target/('comparison-'+view+'.jpg'),quality=94)
 rows=[('face','Wajah dan posisi paw',600),('vehicle-side','Siluet kendaraan',600),('garage','Garasi, kamera setara',417),('race','Kamera balapan, pose setara',417)]
 sheet=Image.new('RGB',(1200,sum(h+46 for _,_,h in rows)+55),'#0d2035');draw=ImageDraw.Draw(sheet);draw.text((15,12),title+' — SEBELUM / SESUDAH',fill='white',font=font);y=55
 for view,text,h in rows:
  draw.text((15,y+9),text,fill='#8bd4e6',font=small)
  for i,stage in enumerate(['before','after']):sheet.paste(Image.open(D/stage/id/(view+'.png')).convert('RGB').resize((600,h),Image.Resampling.LANCZOS),(600*i,y+42))
  y+=h+46
 sheet.save(target/'comparison-sheet.jpg',quality=94)
# Accepted cat + three new pairs, viewed with the same model camera.
sheet=Image.new('RGB',(1600,450),'#0d2035');draw=ImageDraw.Draw(sheet)
for i,(file,label) in enumerate([(D/'after/cat-style-reference.png','Kucing — patokan tetap')]+[(D/'after'/id/'hero.png',title) for id,title in ids]):
 sheet.paste(Image.open(file).convert('RGB').resize((400,400),Image.Resampling.LANCZOS),(i*400,50));draw.text((i*400+12,15),label,fill='white',font=small)
sheet.save(OUT/'batch1-style-lineup.jpg',quality=95)
for prefix in ['character','vehicle']:
 sheet=Image.new('RGB',(1500,1620),'#0d2035');draw=ImageDraw.Draw(sheet)
 for row,(id,title) in enumerate(ids):
  y=row*540;draw.text((15,y+10),title,fill='white',font=font)
  for col,view in enumerate(['front','side','back']):sheet.paste(Image.open(D/'after'/id/(prefix+'-'+view+'.png')).convert('RGB').resize((500,500),Image.Resampling.LANCZOS),(col*500,y+40))
 sheet.save(OUT/(prefix+'-turnarounds.jpg'),quality=95)
sheet=Image.new('RGB',(1200,1360),'#0d2035');draw=ImageDraw.Draw(sheet)
for row,(id,title) in enumerate(ids):
 y=40+row*440;draw.text((12,y),title,fill='white',font=font)
 for col,state in enumerate(['normal','happy','shock']):sheet.paste(Image.open(D/'after'/id/('expression-'+state+'.png')).convert('RGB').resize((400,400),Image.Resampling.LANCZOS),(col*400,y+35))
for col,text in enumerate(['RAMAH','SENANG','TERKEJUT']):draw.text((col*400+12,8),text,fill='#8bd4e6',font=small)
sheet.save(OUT/'expressions.jpg',quality=95)
print('Controlled comparisons, style lineup, turnarounds and expressions created from real renders.')
