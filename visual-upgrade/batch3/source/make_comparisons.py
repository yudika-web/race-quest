"""Reuse matched-camera comparison layout; arrange real captures only."""
from pathlib import Path
s=(Path(__file__).resolve().parents[2]/'batch1/source/make_comparisons.py').read_text()
s=s.replace("[('nara','Pinguin / Kapsul'),('bimo','Beruang / Buggy'),('sora','Kelinci / Formula')]","[('anjing','Anjing / Rally'),('tikus','Tikus / Mini Roadster'),('rubah','Rubah / GT')]")
s=s.replace('5b50da96ae72ad7cb30c6cfd37cf25d7a1f5c303','2527304fb32174f5e07764f1cad84ecac866787f').replace('5b50da9','2527304').replace('SESUDAH — Batch 1','SESUDAH — Batch 3').replace("'model_comparisons':33","'model_comparisons':33").replace("'game_comparisons':6","'game_comparisons':6")
a=s.index('# Accepted cat +');b=s.index("for prefix in",a);s=s[:a]+s[b:]
exec(compile(s,__file__,'exec'))

# Eleven actual pairs, four columns; empty final cell intentionally blank.
sheet=Image.new('RGB',(1600,1350),'#0d2035');draw=ImageDraw.Draw(sheet)
labels=[('arka','Kucing — tetap'),('nara','Pinguin — tetap'),('bimo','Beruang — tetap'),('sora','Kelinci — tetap'),('bebek','Bebek — tetap'),('ayam','Ayam — tetap'),('domba','Domba — tetap'),('robot','Robot — tetap'),('anjing','Anjing / Rally'),('tikus','Tikus / Mini Roadster'),('rubah','Rubah / GT')]
for i,(id,label) in enumerate(labels):
 x=i%4*400;y=i//4*450;sheet.paste(Image.open(D/'after'/('style-'+id+'.png')).convert('RGB').resize((400,400),Image.Resampling.LANCZOS),(x,y+50));draw.text((x+12,y+15),label,fill='white',font=small)
sheet.save(OUT/'batch0-3-lineup.jpg',quality=95)
