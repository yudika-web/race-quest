"""Check only the three requested pairs and bounded presentation changes differ."""
from pathlib import Path
import re,json,base64,hashlib,subprocess
D=Path(__file__).resolve().parents[2];B=D/'batch4';BASE='ddc28f89d628b877d6e70149b0301df4a8aa24a9'
def gitfile(n):return subprocess.check_output(['git','show',BASE+':'+n],cwd=D.parent)
def scripts(h):return re.findall(r'<script\b([^>]*)>(.*?)</script>',h,re.S)
baseline=(D/'race-quest-pro-batch3.html').read_bytes();assert baseline==gitfile('visual-upgrade/race-quest-pro-batch3.html')
new=(D/'race-quest-pro-batch4.html').read_bytes();a=scripts(baseline.decode());b=scripts(new.decode())
assert len(a)==len(b)==8
for i in [0,2,3,5,6]:assert a[i]==b[i],('Protected app/core/data/world/preview-input changed',i)
oa=json.loads(a[1][1]);na=json.loads(b[1][1]);ids=['panda','koala','rakun']
replaced={p+id+ext for id in ids for p,ext in [('kart_','.glb'),('avatar_','.webp')]}
extras={p+id+ext for id in ids for p,ext in [('kart_','_low.glb'),('avatar_','_happy.webp')]}
assert set(na)-set(oa)==extras
for k in oa:
 if k not in replaced:assert oa[k]==na[k],k
for k in replaced|extras:
 data=base64.b64decode(na[k]['uri'].split(',')[1]);assert data==(B/('models' if k.endswith('.glb') else 'avatars')/k).read_bytes();assert len(data)==na[k]['bytes'];assert hashlib.sha256(data).hexdigest()==na[k]['sha256']
assert len({na[k]['uri'] for k in replaced|extras})==12
# Reverse only the exact, bounded three-model configuration additions.
r=b[4][1]
r=r.replace(','+','.join("'kart_%s.glb':'kart_%s_low.glb'"%(id,id) for id in ids),'')
r=r.replace('[1.34,1.95,2.15],[1.27,1.85,2.05],[1.27,2.05,2.25],[1.30,1.90,2.10]][character]','[1.34,1.95,2.15]][character]')
r=r.replace("file.includes('tikus')?1.6:file.includes('rubah')?2.9:file.includes('panda')?.6:file.includes('koala')?1.5:2.8","file.includes('tikus')?1.6:2.9")
assert r==a[4][1],'Other renderer/lighting/physics/timing/camera changes'
r=b[7][1].replace('[1,2,3,4,5,6,7,8,9,10,11,12,13].includes','[1,2,3,4,5,6,7,8,9,10].includes').replace("10:'rubah',11:'panda',12:'koala',13:'rakun'","10:'rubah'")
assert r==a[7][1],'Other results/expression changes'
# Every tracked historical asset/source/report is byte-identical, including both snapshots.
protected=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'--','index.html','visual-upgrade'],cwd=D.parent,text=True).splitlines()
for name in protected:assert (D.parent/name).read_bytes()==gitfile(name),name
# Inherited core whitespace is intentionally kept to prove byte-identical game logic.
trailing=lambda h:[line for line in h.splitlines() if line.rstrip()!=line]
assert all(line in trailing(baseline.decode()) for line in trailing(new.decode()))
report={'status':'passed','baseline_commit':BASE,'html_bytes':len(new),'html_sha256':hashlib.sha256(new).hexdigest(),'html_under_25_decimal_MB':len(new)<25000000,'gameplay_ui_scenery_initial_data_identical':True,'race_camera_world_and_animation_timing_identical':True,'shared_renderer_lighting_loader_identical_except_three_model_configuration_entries':True,'historical_files_byte_identical':len(protected),'unchanged_original_asset_count':len(oa)-len(replaced),'only_replaced_assets':sorted(replaced),'only_new_assets':sorted(extras),'new_asset_payloads_unique':True}
assert report['html_under_25_decimal_MB'];(B/'scope-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
