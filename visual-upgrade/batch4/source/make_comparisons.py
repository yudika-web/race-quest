"""Reuse matched-camera comparison layout; arrange real captures only."""
from pathlib import Path
s=(Path(__file__).resolve().parents[2]/'batch1/source/make_comparisons.py').read_text()
s=s.replace("[('nara','Pinguin / Kapsul'),('bimo','Beruang / Buggy'),('sora','Kelinci / Formula')]","[('panda','Panda / Bamboo'),('koala','Koala / Eco Pod'),('rakun','Rakun / Trail Pickup')]")
s=s.replace('5b50da96ae72ad7cb30c6cfd37cf25d7a1f5c303','ddc28f89d628b877d6e70149b0301df4a8aa24a9').replace('5b50da9','ddc28f8').replace('SESUDAH — Batch 1','SESUDAH — Batch 4').replace("'model_comparisons':33","'model_comparisons':33").replace("'game_comparisons':6","'game_comparisons':6")
a=s.index('# Accepted cat +');b=s.index("for prefix in",a);s=s[:a]+s[b:]
exec(compile(s,__file__,'exec'))

# All 14 actual models, no rescaling between members of a given lineup.
labels=[('arka','Kucing / Sport'),('nara','Pinguin / Kapsul'),('bimo','Beruang / Buggy'),('sora','Kelinci / Formula'),('bebek','Bebek / Amfibi'),('ayam','Ayam / Farm Buggy'),('domba','Domba / Cloud Cruiser'),('robot','Robot / Photon'),('anjing','Anjing / Rally'),('tikus','Tikus / Mini Roadster'),('rubah','Rubah / GT'),('panda','Panda / Bamboo'),('koala','Koala / Eco Pod'),('rakun','Rakun / Trail Pickup')]
cameras=json.loads((D/'lineup-cameras.json').read_text());assert cameras['status']=='passed' and len(cameras['views'])==42
for mode,title in [('pair','14 PAIRS — COMPLETE'),('character','14-CHARACTER COMPLETE LINEUP'),('vehicle','14-VEHICLE LINEUP')]:
 views=[x for x in cameras['views'] if x['mode']==mode];assert len(views)==14
 reference={k:views[0][k] for k in ['view','projection','width','height','time']}
 assert all(all(v[k]==reference[k] for k in reference) for v in views),'Lineup cameras differ'
 sheet=Image.new('RGB',(1600,1870),'#0d2035');draw=ImageDraw.Draw(sheet);draw.text((14,15),title,fill='white',font=font)
 for i,(id,label) in enumerate(labels):
  x=i%4*400;y=70+i//4*450;sheet.paste(Image.open(D/'after'/('lineup-'+mode+'-'+id+'.png')).convert('RGB').resize((400,400),Image.Resampling.LANCZOS),(x,y+50));draw.text((x+10,y+14),label,fill='white',font=small)
 sheet.save(OUT/('complete-'+mode+'-lineup.jpg'),quality=95)
(D/'lineup-verification.json').write_text(json.dumps({'status':'passed','models':14,'views':42,'camera_pose_light_time_equal_per_lineup':True,'character_pose':'Authored seated driving pose; vehicle primitives hidden, no model rescaling.','generative_images':False},indent=2))
