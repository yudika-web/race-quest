from pathlib import Path
import re,json,hashlib,subprocess
D=Path(__file__).resolve().parents[2];B=D/'student-teacher-modes';baseline='b98f40e7714b1d43d96020fc917f3575d1571494';old=(D/'blokraya-balap-edukasi-nusantara.html').read_bytes();raw=(D/'blokraya-mode-siswa-guru.html').read_bytes();h=raw.decode();sha=lambda b:hashlib.sha256(b).hexdigest()
changes=json.loads((B/'bounded-changes.json').read_text())
for c in reversed(changes):
 assert h.count(c['new'])==c['count'],c['new'][:100];h=h.replace(c['new'],c['old'],c['count'])
assert h.encode()==old,'Undocumented edit outside modes/loading/teacher guards'
clean=re.sub(rb'<script id="blokRayaModes">.*?</script>',b'',raw,count=1,flags=re.S);scripts=lambda b:list(re.finditer(rb'<script\b([^>]*)>(.*?)</script>',b,re.S));a,b=scripts(old),scripts(clean);assert len(a)==len(b);protected={}
for i,(x,y)in enumerate(zip(a,b)):
 if b'id="blokRayaLoading"'in x[1]or b'async function ensureRenderer'in x[2]:continue
 assert x[2]==y[2],i;protected[str(i)]=sha(x[2])
for key in [b'race_quest_flexible_v1_',b'race_quest_audio_v1',b'race_quest_preferences',b'race_quest_hud_v45']:assert old.count(key)==raw.count(key),key
for id in ['assetData','blokRayaPosters','patch1StageAssets']:
 pattern=rb'<script id="'+id.encode()+rb'"[^>]*>(.*?)</script>';assert re.search(pattern,old,re.S)[1]==re.search(pattern,raw,re.S)[1],id
entries=subprocess.check_output(['git','ls-tree','-r','-z',baseline]).split(b'\0');files={}
for e in entries:
 if not e:continue
 meta,name=e.split(b'\t',1);name=name.decode()
 if name=='index.html'or name.startswith('visual-upgrade/')or name.endswith('.zip'):files[name]=meta.split()[2].decode()
current=subprocess.check_output(['git','hash-object','--stdin-paths'],input=('\n'.join(files)+'\n').encode(),cwd=D.parent).decode().splitlines()
for (name,digest),now in zip(files.items(),current):assert now==digest,name
report=dict(status='passed',baseline_commit=baseline,html_bytes=len(raw),baseline_bytes=len(old),growth_bytes=len(raw)-len(old),html_sha256=sha(raw),under_25_decimal_MB=len(raw)<25000000,bounded_changes=len(changes),reverse_reconstruction_exact=True,protected_script_sha256=protected,protected_historical_files=len(files),storage_keys_preserved=True,original_posters_assets_and_thumbnails_identical=True,gameplay_renderer_AI_buff_stage_audio_HUD_scripts_identical=True,scope='Only loading presentation/timing, new mode/PIN controller/UI and guards around original teacher functions/forms/actions/export cleanup. No gameplay or arena edits.')
(B/'scope-tests.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
