from pathlib import Path
import re,json,hashlib,subprocess
D=Path(__file__).resolve().parents[2];B=D/'patch3-strategic-buffs';baseline='c786d88aca6876e7913012f3490fd2f6660898c8';h=(D/'race-quest-pro-patch3.html').read_text();original=(D/'race-quest-pro-patch2.html').read_text();sha=lambda x:hashlib.sha256(x).hexdigest()
for id in ['patch3Styles','patch3BuffIcons','patch3BuffSystem','patch3BuffUI']:
 tag='style' if id.endswith('Styles') else 'script'
 h,n=re.subn(r'<'+tag+r' id="'+id+r'"[^>]*>.*?</'+tag+'>','',h,flags=re.S);assert n==1
# inserted scripts have two separator newlines; remove exactly at insertion boundary.
scripts=list(re.finditer(r'<script\b[^>]*>.*?</script>',h,re.S));pos=scripts[13].end();assert h[pos:pos+2]=='\n\n';h=h[:pos]+h[pos+2:]
changes=json.loads((B/'bounded-changes.json').read_text())
for change in reversed(changes):
 assert h.count(change['new'])==1,change['new'][:80]
 h=h.replace(change['new'],change['old'])
assert h==original,'Unbounded difference outside approved hooks'
files=subprocess.check_output(['git','ls-tree','-r','--name-only',baseline],text=True).splitlines();protected=[]
for file in files:
 if file=='index.html' or file.startswith('visual-upgrade/'):
  expected=subprocess.check_output(['git','rev-parse',baseline+':'+file],text=True).strip()
  current=subprocess.check_output(['git','hash-object',file],text=True).strip()
  assert expected==current,file
  protected.append(file)
report={'status':'passed','baseline':baseline,'baseline_html_sha256':sha(original.encode()),'current_html_bytes':(D/'race-quest-pro-patch3.html').stat().st_size,'bounded_hooks':len(changes),'reverse_reconstruction_exact':True,'protected_files':len(protected),'protected_engine_scope':'AI decision method, stage definitions, character GLB/avatar data, teacher/bank/progress/academic scoring unchanged. Only logged item mechanics, presentation and inventory hooks differ.'}
(B/'scope-tests.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
