"""Reuse the Batch 1 native import, finite/normal/index/rig/collider validator."""
from pathlib import Path
s=(Path(__file__).resolve().parents[2]/'batch1/source/validate_models.py').read_text().replace('assert len(results)==6','assert len(results)==8')
exec(compile(s,__file__,'exec'))
