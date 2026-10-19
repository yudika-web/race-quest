"""Gate/package this stage using the shared Batch 1 artifact validation pipeline."""
from pathlib import Path
s=(Path(__file__).resolve().parents[2]/'batch1/source/build_release.py').read_text()
s=s.replace('batch1','batch3').replace('Batch 1','Batch 3').replace('Batch-1','Batch-3')
s=s.replace("len(reports['unchanged-renders.json']['checks'])==15","len(reports['unchanged-renders.json']['checks'])==22")
s=s.replace("'completed_this_batch':3,'cat_unchanged':True,'pending_pairs':10","'completed_this_batch':3,'batch0_to_2_unchanged':True,'pending_pairs':3")
s=s.replace('Pilih Pinguin, Beruang, atau Kelinci di garasi.','Pilih Anjing, Tikus, atau Rubah di halaman kedua garasi. Unlock tetap 60 token.').replace('template Kucing','template Batch 2')
s=s.replace("'camera-verification.json']","'camera-verification.json','actor-tests.json']")
s=s.replace("(D/'delivery-validation.json').write_text","validation['optional_checks']={'direct_file_offline':json.loads((D/'file-offline-test.json').read_text())}\n(D/'delivery-validation.json').write_text")
# All three actual network-disabled races are a release gate, not just one smoke.
s=s.replace("html=HTML.read_bytes();", "assert len(reports['offline-test-results.json']['cases'])==3\nassert len(reports['actor-tests.json']['cases'])==3\nhtml=HTML.read_bytes();")
exec(compile(s,__file__,'exec'))
