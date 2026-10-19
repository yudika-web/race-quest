from pathlib import Path
import re,json,hashlib,subprocess
D=Path(__file__).resolve().parents[2];B=D/'stage2-mempawah';meta=json.loads((B/'baseline.json').read_text());base=(D/'race-quest-pro-pontianak-stage1.html').read_bytes();new=(D/'race-quest-pro-mempawah-stage2.html').read_bytes()
assert hashlib.sha256(base).hexdigest()==meta['html_sha256']
# The only changes are the named visual layer and one display label, with stable stage ID.
rebuilt=re.sub(r'\n<script id="mempawahStageVisuals">.*?</script>', '',new.decode(),count=1,flags=re.S).replace("id:'kapuas',name:'Mempawah · Jalanan Taman'","id:'kapuas',name:'Tepi Sungai Kapuas'")
assert rebuilt.encode()==base
scripts=lambda h:re.findall(r'<script\b[^>]*>(.*?)</script>',h,re.S)
a=scripts(base.decode());b=scripts(new.decode());assets=json.loads(b[1]);assert a[1]==b[1];assert len(assets)==94
protected=subprocess.check_output(['git','ls-tree','-r','--name-only',meta['baseline_commit'],'--','index.html','visual-upgrade'],cwd=D.parent,text=True).splitlines()
# Compare each working file to its committed Git blob SHA, in one streamed pass.
entries=subprocess.check_output(['git','ls-tree','-r',meta['baseline_commit'],'--','index.html','visual-upgrade'],cwd=D.parent,text=True).splitlines()
for line in entries:
 info,name=line.split('\t',1);expected=info.split()[2];payload=(D.parent/name).read_bytes();actual=hashlib.sha1(b'blob '+str(len(payload)).encode()+b'\0'+payload).hexdigest();assert actual==expected,name
report=dict(status='passed',baseline=meta['baseline_commit'],historical_files_byte_identical=len(protected),embedded_assets_byte_identical=94,original_inline_scripts_byte_identical_except_stage_display_name=True,road_physics_AI_UI_loader_animation_code_identical=True,html_bytes=len(new),html_under_25_decimal_MB=len(new)<25000000,html_sha256=hashlib.sha256(new).hexdigest())
assert report['html_under_25_decimal_MB'];(B/'scope-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
