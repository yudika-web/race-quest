"""Ensure this stage changes exactly the three requested pairs and presentation."""
from pathlib import Path
import re,json,base64,hashlib,subprocess,struct
D=Path(__file__).resolve().parents[2];B=D/'batch1';BASE='5b50da96ae72ad7cb30c6cfd37cf25d7a1f5c303'
def old(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=D.parent)
def scripts(s):return re.findall(r'<script\b([^>]*)>(.*?)</script>',s,re.S)
baseline=(D/'race-quest-visual-upgrade.html').read_bytes();assert baseline==old('visual-upgrade/race-quest-visual-upgrade.html')
a=scripts(baseline.decode());new=(D/'race-quest-pro-batch1.html').read_bytes();b=scripts(new.decode())
for i in [0,2,3,5]:assert a[i]==b[i],('Gameplay/UI/data/scenery changed',i)
oa=json.loads(a[1][1]);na=json.loads(b[1][1]);replaced={p+id+ext for id in ['nara','bimo','sora'] for p,ext in [('kart_','.glb'),('avatar_','.webp')]}
for key in oa:
 if key not in replaced:assert oa[key]==na[key],key
extras={p+id+suffix+ext for id in ['nara','bimo','sora'] for p,suffix,ext in [('kart_','_low','.glb'),('avatar_','_happy','.webp')]};assert set(na)-set(oa)==extras
for key in replaced|extras:
 data=base64.b64decode(na[key]['uri'].split(',')[1]);file=B/('models' if key.endswith('.glb') else 'avatars')/key
 assert data==file.read_bytes();assert len(data)==na[key]['bytes'];assert hashlib.sha256(data).hexdigest()==na[key]['sha256']
assert len({na[k]['uri'] for k in replaced|extras})==len(replaced|extras),'Duplicate newly embedded asset'
protected=['index.html','visual-upgrade/race-quest-cat-sport.glb','visual-upgrade/race-quest-cat-sport-low.glb','visual-upgrade/source/refine_cat.py','visual-upgrade/source/build_cat.py','visual-upgrade/source/race-quest-cat-sport.blend']
for name in protected:assert (D.parent/name).read_bytes()==old(name),name
# Permit only model-facing calls in the existing race/depth renderers.
def remove_options(s):return re.sub(r',\.\.\.this\.batchPose\(session,(?:a|p|player),(?:kartFiles|files)\[(?:a|session)\.character\],(?:i\+1|0)\)','',s).replace('\n  this.batchSession=session;','')
for start,end in [(' race(session,',None),(' renderSunShadows(',' initParticles(')]:
 before=a[4][1].split(start,1)[1];after=b[4][1].split(start,1)[1]
 if end:before=before.split(end,1)[0];after=after.split(end,1)[0]
 assert before==remove_options(after),('Race camera/world rendering changed',start)
# GPU programs, materials, loader and drawPrimitive stay as in the accepted cat version.
for start,end in [(' constructor(',' ensureModel('),(' loadModel(',' mesh('),(' drawPrimitive(',' drawModel(')]:
 before=a[4][1].split(start,1)[1].split(end,1)[0]
 after=b[4][1].split(start,1)[1].split(' batchPose(' if start==' drawPrimitive(' else end,1)[0]
 assert before==after,('Shared lighting/loader/draw changed',start)
report={'status':'passed','baseline_commit':BASE,'gameplay_ui_scenery_initial_data_identical':True,'race_camera_world_and_non_batch_calls_identical':True,'gpu_programs_and_shared_material_rendering_identical':True,'cat_html_models_and_source_byte_identical':True,'unchanged_original_asset_count':len(oa)-len(replaced),'only_replaced_assets':sorted(replaced),'only_new_assets':sorted(extras),'no_duplicate_new_asset_payloads':True,'html_bytes':len(new),'html_under_25_decimal_MB':len(new)<25000000,'html_sha256':hashlib.sha256(new).hexdigest()}
assert report['html_under_25_decimal_MB']
(B/'scope-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
