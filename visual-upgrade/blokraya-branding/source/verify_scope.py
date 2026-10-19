from pathlib import Path
import re,json,hashlib,subprocess
D=Path(__file__).resolve().parents[2];B=D/'blokraya-branding';baseline='9bd494aa07b08c2bc58755e9577f9c0237f8df6e';raw=(D/'blokraya-balap-edukasi-nusantara.html').read_bytes();old=(D/'race-quest-pro-sky-horizon.html').read_bytes();h=raw.decode()
for c in reversed(json.loads((B/'bounded-changes.json').read_text())):
 if c['new']:assert h.count(c['new'])==c['count'],c['new'][:80];h=h.replace(c['new'],c['old'],c['count'])
 else:h=h[:c['offset']]+c['old']+h[c['offset']:]
assert h.encode()==old,'Undocumented change beyond branding/loading'
sha=lambda b:hashlib.sha256(b).hexdigest();scripts=lambda b:[m[1]for m in re.finditer(rb'<script\b[^>]*>(.*?)</script>',b,re.S)]
newclean=re.sub(rb'<script id="blokRayaPosters"[^>]*>.*?</script>|<script id="blokRayaLoading"[^>]*>.*?</script>',b'',raw,flags=re.S);a,b=scripts(old),scripts(newclean);assert len(a)==len(b)
# Core changes only its export-format error's brand name; renderer only tracks texture image readiness.
normalizations={2:[(b'Gunakan hasil ekspor BlokRaya atau RACE QUEST.',b'Gunakan hasil ekspor RACE QUEST.')],7:[(b'BlokRayaLoading.trackImage(im);im.src=uri;',b'im.src=uri;')],10:[(b"c.fillText('BlokRaya',512,137)",b"c.fillText('RACE QUEST',512,137)"),(b"c.fillText('BALAP EDUKASI NUSANTARA',512,199)",b"c.fillText('PERFORMANCE GARAGE  /  PIT 01',512,199)")]}
components={}
for i,(x,y)in enumerate(zip(a,b)):
 if i==20:continue # app changes are individually reversed above
 for new,original in normalizations.get(i,[]):y=y.replace(new,original)
 assert x==y,i;components[str(i)]=sha(x)
for key in [b'race_quest_flexible_v1_',b'race_quest_audio_v1',b'race_quest_preferences',b'race_quest_hud_v45']:assert raw.count(key)==old.count(key)
entries=subprocess.check_output(['git','ls-tree','-r','-z',baseline]).split(b'\0');protected={}
for e in entries:
 if not e:continue
 meta,name=e.split(b'\t',1);name=name.decode()
 if name=='index.html'or name.startswith('visual-upgrade/')or name.endswith('.zip'):protected[name]=meta.split()[2].decode()
actual=subprocess.check_output(['git','hash-object','--stdin-paths'],input=('\n'.join(protected)+'\n').encode(),cwd=D.parent).decode().splitlines()
for (name,digest),current in zip(protected.items(),actual):assert digest==current,name
posters=json.loads(re.search(rb'<script id="blokRayaPosters"[^>]*>(.*?)</script>',raw,re.S)[1]);assert set(posters)=={'portrait','landscape'}
for uri in posters.values():assert raw.count(uri.encode())==1,'Duplicated embedded poster'
report=dict(status='passed',baseline_commit=baseline,html_bytes=len(raw),baseline_bytes=len(old),growth_bytes=len(raw)-len(old),html_sha256=sha(raw),under_25_decimal_MB=len(raw)<25000000,reverse_reconstruction_exact=True,protected_historical_files=len(protected),protected_script_sha256=components,storage_keys_preserved=True,each_poster_embedded_once=True,scope='Brand strings, startup/renderer/world loading and texture readiness; gameplay, AI, buffs, HUD, stage geometry and sky shaders unchanged.')
(B/'scope-tests.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
