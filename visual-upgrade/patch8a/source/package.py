from pathlib import Path
import json,hashlib,zipfile,subprocess,sys
D=Path(__file__).resolve().parents[1];V=D.parent;R=V.parent;H=V/'blokraya-patch8a-landmarks.html'
subprocess.run([sys.executable,str(D/'source/test_scope.py')],check=True)
subprocess.run([sys.executable,str(D/'source/report.py')],check=True,stdout=subprocess.DEVNULL)
m=json.loads((D/'metrics.json').read_text());raw=H.read_bytes();sha=lambda b:hashlib.sha256(b).hexdigest();assert sha(raw)==m['html_sha256']
shared=['finalization/source/harness.cjs','stage11-kubu-raya/source/harness.cjs','stage12-kayong-utara/source/harness.cjs','stage12-kayong-utara/asset-metrics.json','stage13-ketapang/asset-metrics.json']
for kind in ['playable','review']:
 dest=R/f'blokraya-patch8a-{kind}.zip'
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
  z.writestr('MULAI.txt',(D/'MULAI.txt').read_text())
  if kind=='playable':z.write(H,H.name)
  else:
   z.write(H,'visual-upgrade/'+H.name);z.write(V/'blokraya-pro-final.html','visual-upgrade/blokraya-pro-final.html')
   for f in sorted(D.rglob('*')):
    if f.is_file()and '__pycache__'not in f.parts and f.name!='release-metrics.json':z.write(f,'visual-upgrade/patch8a/'+f.relative_to(D).as_posix())
   for p in shared:z.write(V/p,'visual-upgrade/'+p)
   z.writestr('visual-upgrade/patch8a/release-metrics.json',json.dumps({**m,'review_self_hash_omitted':True,'note':'Final archive hashes are recorded in repository release-metrics.json.'},indent=2))
 with zipfile.ZipFile(dest)as z:
  assert z.testzip()is None;assert z.read(H.name if kind=='playable'else'visual-upgrade/'+H.name)==raw
  if kind=='review':
   for f in D.rglob('*'):
    if f.is_file()and '__pycache__'not in f.parts and f.name!='release-metrics.json':assert z.read('visual-upgrade/patch8a/'+f.relative_to(D).as_posix())==f.read_bytes()
 m[kind+'_zip']={'file':dest.name,'bytes':dest.stat().st_size,'sha256':sha(dest.read_bytes()),'CRC_OK':True,'HTML_identical':True,'entries':len(z.namelist())}
(D/'release-metrics.json').write_text(json.dumps(m,indent=2));print(json.dumps({k:m[k]for k in ['html_bytes','growth_bytes','html_sha256','teacher_export_bytes','playable_zip','review_zip']},indent=2))
