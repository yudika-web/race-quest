"""Reuse matched-camera comparison layout; arrange real captures only."""
from pathlib import Path
s=(Path(__file__).resolve().parents[2]/'batch1/source/make_comparisons.py').read_text()
s=s.replace("[('nara','Pinguin / Kapsul'),('bimo','Beruang / Buggy'),('sora','Kelinci / Formula')]","[('bebek','Bebek / Amfibi'),('ayam','Ayam / Farm Buggy'),('domba','Domba / Cloud Cruiser'),('robot','Robot / Photon')]")
s=s.replace('5b50da96ae72ad7cb30c6cfd37cf25d7a1f5c303','60b2edb966e5775c48c8868c105b700eb57718c4').replace('5b50da9','60b2edb').replace('SESUDAH — Batch 1','SESUDAH — Batch 2').replace("'model_comparisons':33","'model_comparisons':44").replace("'game_comparisons':6","'game_comparisons':8")
a=s.index('# Accepted cat +');b=s.index("for prefix in",a);s=s[:a]+s[b:];s=s.replace('(1500,1620)','(1500,2160)').replace('(1200,1360)','(1200,1800)')
exec(compile(s,__file__,'exec'))
# Both the accepted quartet and new quartet rendered from this same HTML.
sheet=Image.new('RGB',(1600,900),'#0d2035');draw=ImageDraw.Draw(sheet)
for i,(id,label) in enumerate([('arka','Kucing — tetap'),('nara','Pinguin — tetap'),('bimo','Beruang — tetap'),('sora','Kelinci — tetap'),('bebek','Bebek / Amfibi'),('ayam','Ayam / Farm Buggy'),('domba','Domba / Cloud Cruiser'),('robot','Robot / Photon')]):
 x=i%4*400;y=i//4*450;sheet.paste(Image.open(D/'after'/('style-'+id+'.png')).convert('RGB').resize((400,400),Image.Resampling.LANCZOS),(x,y+50));draw.text((x+12,y+15),label,fill='white',font=small)
sheet.save(OUT/'batch0-2-lineup.jpg',quality=95)
