"""Gate/package this stage using the shared Batch 1 artifact validation pipeline."""
from pathlib import Path
s=(Path(__file__).resolve().parents[2]/'batch1/source/build_release.py').read_text()
s=s.replace('batch1','batch4').replace('Batch 1','Batch 4').replace('Batch-1','Batch-4')
s=s.replace("len(reports['unchanged-renders.json']['checks'])==15","len(reports['unchanged-renders.json']['checks'])==25")
s=s.replace("'completed_this_batch':3,'cat_unchanged':True,'pending_pairs':10","'completed_this_batch':3,'batch0_to_3_unchanged':True,'pending_pairs':0,'completed_total_pairs':14,'arena_work_started':False")
s=s.replace('Pilih Pinguin, Beruang, atau Kelinci di garasi.','Pilih Panda, Koala, atau Rakun melalui halaman 2/3 garasi. Unlock tetap 60 token.').replace('template Kucing','template Batch 3')
s=s.replace("'camera-verification.json']","'camera-verification.json','actor-tests.json','all-character-tests.json','lineup-verification.json','complete-asset-catalog.json']")
s=s.replace("(D/'delivery-validation.json').write_text","validation['optional_checks']={'direct_file_offline':json.loads((D/'file-offline-test.json').read_text())}\n(D/'delivery-validation.json').write_text")
# All three actual network-disabled races are a release gate, not just one smoke.
s=s.replace("html=HTML.read_bytes();", "assert len(reports['offline-test-results.json']['cases'])==3\nassert len(reports['actor-tests.json']['cases'])==3\nassert len(reports['all-character-tests.json']['cases'])==14\nassert reports['lineup-verification.json']['views']==42\nassert len(reports['complete-asset-catalog.json']['models'])==14\nhtml=HTML.read_bytes();")
exec(compile(s,__file__,'exec'))
