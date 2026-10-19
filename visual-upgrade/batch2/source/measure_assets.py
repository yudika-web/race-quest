"""Reuse shared measured-bounds / GLTF accounting implementation."""
from pathlib import Path
s=(Path(__file__).resolve().parents[2]/'batch1/source/measure_assets.py').read_text().replace('race-quest-pro-batch1.html','race-quest-pro-batch2.html').replace('race-quest-visual-upgrade.html','race-quest-pro-batch1.html').replace("[('nara','Pinguin','Kapsul'),('bimo','Beruang','Buggy'),('sora','Kelinci','Formula')]","[('bebek','Bebek','Amfibi'),('ayam','Ayam','Farm Buggy'),('domba','Domba','Cloud Cruiser'),('robot','Robot','Photon')]")
exec(compile(s,__file__,'exec'))
