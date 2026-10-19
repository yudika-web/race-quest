"""Gate/package this stage using the shared Batch 1 artifact validation pipeline."""
from pathlib import Path
s=(Path(__file__).resolve().parents[2]/'batch1/source/build_release.py').read_text()
s=s.replace('batch1','batch2').replace('Batch 1','Batch 2').replace('Batch-1','Batch-2')
s=s.replace("len(reports['preview-race-tests.json']['cases'])==6","len(reports['preview-race-tests.json']['cases'])==8")
s=s.replace("len(reports['glb-validation.json']['models'])==6","len(reports['glb-validation.json']['models'])==8")
s=s.replace("len(reports['rig-tests.json']['models'])==3","len(reports['rig-tests.json']['models'])==4")
s=s.replace("len(reports['unchanged-renders.json']['checks'])==15","len(reports['unchanged-renders.json']['checks'])==17")
s=s.replace("'completed_this_batch':3,'cat_unchanged':True,'pending_pairs':10","'completed_this_batch':4,'cat_and_batch1_unchanged':True,'pending_pairs':6")
s=s.replace('Pilih Pinguin, Beruang, atau Kelinci di garasi.','Pilih Bebek, Ayam, Domba, atau Robot di garasi. Unlock tetap 60 token; Domba dan Robot ada di halaman kedua.').replace('tiga karakter baru','empat karakter baru').replace('tiga Blender','empat Blender').replace('template Kucing','template Batch 1')
# All four actual network-disabled races are a release gate, not just one smoke.
s=s.replace("html=HTML.read_bytes();", "assert len(reports['offline-test-results.json']['cases'])==4\nhtml=HTML.read_bytes();")
exec(compile(s,__file__,'exec'))
