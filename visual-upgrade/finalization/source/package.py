from pathlib import Path
import json,hashlib,zipfile,subprocess,sys
D=Path(__file__).resolve().parents[1];V=D.parent;R=V.parent;H=V/'blokraya-pro-final.html'
subprocess.run([sys.executable,str(D/'source/test_scope.py')],check=True)
subprocess.run([sys.executable,str(D/'source/report.py')],check=True,stdout=subprocess.DEVNULL)
m=json.loads((D/'metrics.json').read_text());raw=H.read_bytes();sha=lambda b:hashlib.sha256(b).hexdigest();assert m['html_sha256']==sha(raw)
# The baseline and small shared helper sources make this review archive rebuildable.
shared=['stage11-kubu-raya/source/harness.cjs','stage11-kubu-raya/source/test_mechanics.cjs','stage12-kayong-utara/source/harness.cjs','stage12-kayong-utara/source/test_mechanics.cjs','stage13-ketapang/source/test_mechanics.cjs','stage13-ketapang/source/test_items.cjs']
for kind in ['playable','review']:
 dest=R/f'blokraya-pro-final-{kind}.zip'
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
  z.writestr('MULAI.txt',(D/'MULAI.txt').read_text())
  if kind=='playable':z.write(H,H.name)
  else:
   z.write(H,'visual-upgrade/'+H.name);z.write(V/'blokraya-stage13-ketapang.html','visual-upgrade/blokraya-stage13-ketapang.html')
   for f in sorted(D.rglob('*')):
    if f.is_file()and '__pycache__'not in f.parts and f.name!='release-metrics.json':z.write(f,'visual-upgrade/finalization/'+f.relative_to(D).as_posix())
   for f in shared:z.write(V/f,'visual-upgrade/'+f)
   z.writestr('visual-upgrade/finalization/release-metrics.json',json.dumps({**m,'review_self_hash_omitted':True,'note':'Final ZIP hashes are recorded in the repository release-metrics.json.'},indent=2))
 with zipfile.ZipFile(dest)as z:
  assert z.testzip()is None;assert z.read(H.name if kind=='playable'else'visual-upgrade/'+H.name)==raw
  if kind=='review':
   for f in D.rglob('*'):
    if f.is_file()and '__pycache__'not in f.parts and f.name!='release-metrics.json':assert z.read('visual-upgrade/finalization/'+f.relative_to(D).as_posix())==f.read_bytes()
 m[kind+'_zip']={'file':dest.name,'bytes':dest.stat().st_size,'sha256':sha(dest.read_bytes()),'CRC_OK':True,'HTML_identical':True,'entries':len(z.namelist())}
(D/'release-metrics.json').write_text(json.dumps(m,indent=2));print(json.dumps({k:m[k]for k in ['html_bytes','growth_bytes','html_sha256','teacher_export_bytes','teacher_export_after_garage_bytes','playable_zip','review_zip']},indent=2))
