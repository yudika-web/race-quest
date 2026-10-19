"""All 14 actual loaded high/low pairs; measured colour submissions, not FPS."""
from pathlib import Path
import json
D=Path(__file__).resolve().parents[1];r=json.loads((D/'all-character-tests.json').read_text());assert r['status']=='passed' and len(r['cases'])==14
catalog={'status':'passed','models':[{k:c[k] for k in ['index','name','vehicle','file','low','avatar','renderer_stats']} for c in r['cases']],'measurement':'Actual RaceRenderer high/low normal-expression draw submissions, time 1, one colour pass. Excludes world/UI/AI and shadow passes. No physical-device FPS measurement.'}
(D/'complete-asset-catalog.json').write_text(json.dumps(catalog,indent=2))
