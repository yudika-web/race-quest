from pathlib import Path
import re,json,hashlib,subprocess
D=Path(__file__).resolve().parents[2];B=D/'patch5-ten-stages';baseline='07af6fb0a7dfab5cb9f77d8ba32ab0cefc69ce99'
old=subprocess.check_output(['git','show',baseline+':visual-upgrade/blokraya-mode-siswa-guru.html'],cwd=D.parent).decode();new=(D/'blokraya-patch5.html').read_text();changes=json.loads((B/'bounded-changes.json').read_text());restored=new
for c in reversed(changes):
 assert restored.count(c['new'])==c['count'],c['new'][:60]
 restored=restored.replace(c['new'],c['old'])
assert restored==old,'Unexpected changes outside bounded assembly'
def blocks(s):return {m[0]:m[1] for m in re.findall(r'<script id="([^"]+)"[^>]*>(.*?)</script>',s,re.S)}
a,b=blocks(old),blocks(new);changed={'patch1StageCatalog','patch1StageUI','patch45HUD'}
protected=[]
for key in a:
 if key not in changed:
  assert a[key]==b[key],key
  protected.append({'id':key,'sha256':hashlib.sha256(a[key].encode()).hexdigest()})
# Historical accepted files/index.html remain identical to HEAD. New distributable is additive.
tracked=subprocess.check_output(['git','ls-files','visual-upgrade','index.html'],cwd=D.parent).decode().splitlines()
for file in tracked:
 p=D.parent/file
 assert p.exists() and hashlib.sha256(p.read_bytes()).digest()==hashlib.sha256(subprocess.check_output(['git','show',baseline+':'+file],cwd=D.parent)).digest(),file
assert len(new.encode())<25_000_000
report={'status':'passed','baseline':baseline,'bounded_change_count':len(changes),'reverse_assembly_matches_baseline':True,'historical_files_unchanged':len(tracked),'protected_script_payloads':protected,'baseline_bytes':len(old.encode()),'html_bytes':len(new.encode()),'html_sha256':hashlib.sha256(new.encode()).hexdigest(),'growth_bytes':len(new.encode())-len(old.encode()),'budget_bytes':25000000,'remaining_bytes':25000000-len(new.encode()),'notes':['Core/app/renderer changes are precisely recorded in bounded-changes.json. Named scripts not targeted by assembly are byte-identical, including audio, buff, AI, posters, PIN modes and boot loading.','HUD changes only its GP round label to use configured round count. No main/index.html, original distribution, historical source or environment/model asset edits.']}
(B/'scope-tests.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='protected_script_payloads'},indent=2))
