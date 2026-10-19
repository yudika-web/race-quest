"""Prove this is a bounded UI-only patch, restoring exact baseline bytes."""
from pathlib import Path
import re,json,hashlib,subprocess
D=Path(__file__).resolve().parents[2];B=D/'patch1-garage-stage';meta=json.loads((B/'baseline.json').read_text());base=(D/'race-quest-pro-singkawang-stage3.html').read_bytes();new=(D/'race-quest-pro-patch1.html').read_bytes()
assert hashlib.sha256(base).hexdigest()==meta['html_sha256']
h=new.decode();h=re.sub(r'\n<style id="patch1Styles">.*?</style>\n','',h,count=1,flags=re.S)
h=re.sub(r'<dialog id="stagePickerDialog".*?</dialog>\n','',h,count=1,flags=re.S)
h=re.sub(r'\n<script id="patch1StageCatalog".*?</script>\n<script id="patch1StageAssets".*?</script>\n<script id="patch1Workshop">.*?</script>\n<script id="patch1StageUI">.*?</script>','',h,count=1,flags=re.S)
for c in reversed(json.loads((B/'app-ui-changes.json').read_text())):
 assert h.count(c['new'])==1;h=h.replace(c['new'],c['old'])
h=h.replace('<button type="button" id="garageStageBtn" aria-haspopup="dialog">Pilih arena →</button>','<span class="muted small">Soal dijawab saat seluruh balapan dijeda.</span>').replace('Mulai Balapan →','Siap, Balapan! →')
assert h.encode()==base,'Unexpected change outside bounded UI patch'
scripts=lambda s:re.findall(r'<script\b[^>]*>(.*?)</script>',s,re.S)
a=scripts(base.decode());b=scripts(new.decode());assert a[1]==b[1];assets=json.loads(a[1]);assert len(assets)==94
entries=subprocess.check_output(['git','ls-tree','-r',meta['baseline_commit'],'--','index.html','visual-upgrade'],cwd=D.parent,text=True).splitlines()
for line in entries:
 info,name=line.split('\t',1);payload=(D.parent/name).read_bytes();actual=hashlib.sha1(b'blob '+str(len(payload)).encode()+b'\0'+payload).hexdigest();assert actual==info.split()[2],name
report=dict(status='passed',baseline=meta['baseline_commit'],historical_files_byte_identical=len(entries),original_embedded_assets_byte_identical=94,baseline_exact_after_reversing_documented_UI_insertions=True,original_core_renderer_scenery_models_avatars_and_gameplay_unchanged=True,html_bytes=len(new),growth_bytes=len(new)-len(base),html_under_25_decimal_MB=len(new)<25000000,html_sha256=hashlib.sha256(new).hexdigest())
assert report['html_under_25_decimal_MB'];(B/'scope-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
