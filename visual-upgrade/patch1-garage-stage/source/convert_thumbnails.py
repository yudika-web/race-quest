from pathlib import Path
from PIL import Image
D=Path(__file__).resolve().parents[1]
for city in ['pontianak','mempawah','singkawang']:
 for view in ['landmark','race']:
  p=D/'assets'/(city+'-'+view+'.png');Image.open(p).convert('RGB').save(p.with_suffix('.webp'),quality=82,method=6)
