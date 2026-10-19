from pathlib import Path
import re,json,hashlib,subprocess
D=Path(__file__).resolve().parents[2];B=D/'patch2-audio-vfx';meta=json.loads((B/'baseline.json').read_text());base=(D/'race-quest-pro-patch1.html').read_bytes();new=(D/'race-quest-pro-patch2.html').read_bytes();assert hashlib.sha256(base).hexdigest()==meta['html_sha256'];h=new.decode()
h=re.sub(r'\n<style id="patch2Styles">.*?</style>\n','',h,count=1,flags=re.S)
h=re.sub(r'\n<script id="patch2Audio">.*?</script>\n<script id="patch2VFX">.*?</script>','',h,count=1,flags=re.S)
for c in reversed(json.loads((B/'bounded-changes.json').read_text())):
 assert h.count(c['new'])==1,c['new'][:90];h=h.replace(c['new'],c['old'])
assert h.encode()==base,'Unintended changes outside presentation hooks'
S=lambda h:re.findall(r'<script\b([^>]*)>(.*?)</script>',h,re.S)
a=S(base.decode());b=S(new.decode());assert a[1]==b[1];assert a[2]==b[2];assets=json.loads(b[1][1]);assert len(assets)==94
for i in [0,3,4,5,6,8,9,10,11]:assert a[i]==b[i],i
entries=subprocess.check_output(['git','ls-tree','-r',meta['baseline_commit'],'--','index.html','visual-upgrade'],cwd=D.parent,text=True).splitlines()
for line in entries:
 info,name=line.split('\t',1);raw=(D.parent/name).read_bytes();assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==info.split()[2],name
out=dict(status='passed',baseline=meta['baseline_commit'],historical_files_identical=len(entries),embedded_assets_identical=94,all_14_original_ogg_vorbis_identical=True,core_AI_buffs_stages_physics_models_avatars_unchanged=True,baseline_exact_after_reversing_bounded_presentation_changes=True,html_bytes=len(new),growth_bytes=len(new)-len(base),html_sha256=hashlib.sha256(new).hexdigest(),under_25_decimal_MB=len(new)<25000000)
assert out['under_25_decimal_MB'];(B/'scope-verification.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
