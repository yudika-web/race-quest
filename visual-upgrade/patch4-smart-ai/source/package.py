from pathlib import Path
import json,hashlib,zipfile,re
D=Path(__file__).resolve().parents[2];B=D/'patch4-smart-ai';H=D/'race-quest-pro-patch4.html';R=D.parent
required=['scope-tests','ai-tests','personality-tests','simulation-results','smart-ui-tests','buff-tests','core-test-results','ui-tests','test-results','offline-test-results','persistence-tests','export-tests','stage-audio-tests','unchanged-renders']
for n in required:assert json.loads((B/(n+'.json')).read_text())['status']=='passed',n
raw=H.read_bytes();old=(D/'race-quest-pro-patch3.html').read_bytes();sha=lambda x:hashlib.sha256(x).hexdigest()
# Exact embedded assets/scenery/audio and academic code are also checked by reverse reconstruction.
for id in ['assetData','patch1StageAssets','patch3BuffIcons','initialData']:
 pattern=rb'<script id="'+id.encode()+rb'"[^>]*>(.*?)</script>';assert re.search(pattern,raw,re.S)[1]==re.search(pattern,old,re.S)[1],id
sims=json.loads((B/'simulation-results.json').read_text());metrics={'baseline':'dab093d0c26dd38afdece02b45a8577111b512ab','html_bytes':len(raw),'baseline_bytes':len(old),'growth_bytes':len(raw)-len(old),'html_sha256':sha(raw),'under_25_decimal_MB':len(raw)<25000000,'new_embedded_assets':0,'new_GPU_buffers':0,'additional_AI_indicator_max_draws':4,'additional_AI_indicator_max_triangles':1280,'particle_pool_slots_unchanged':480,'AI_inventory_slots_each':2,'AI_log_capacity':240,'AI_HUD_event_capacity':24,'AI_supply_max_per_actor':'Question count, one opportunity per physical public gate; probability and two-slot capacity apply. No timer refill.','unboosted_AI_speed_cap_mps':23,'boosted_AI_speed_cap_mps':31,'paired_races':sims['paired_races'],'standalone_completion_cases':sims['standalone_cases'],'seeds':len(sims['seeds']),'controlled_personality_opportunities':16000,'teacher_export_bytes':json.loads((B/'export-tests.json').read_text())['export_bytes'],'protected_files':json.loads((B/'scope-tests.json').read_text())['protected_files'],'fps_measured':False,'physical_phone_tested':False,'human_student_win_rate_measured':False,'mid_race_save_supported':False}
(B/'asset-metrics.json').write_text(json.dumps(metrics,indent=2))
notes='RACE QUEST PRO — PATCH 4 SMART RACING AI\n\nEkstrak ZIP, buka race-quest-pro-patch4.html pada browser WebGL. Semua aset tertanam tanpa CDN/internet. Klik/sentuh tombol untuk audio.\n\nEmpat kepribadian AI, sembilan buff kontekstual, dua slot dengan pasokan terbatas per pos balapan. Santai tidak menyerang; Sedang dan Menantang menggunakan target lokal, waktu reaksi, cooldown dan peringatan. AI tidak membaca jawaban atau inventori siswa.\n\nHadiah buff pemain tetap dari jawaban benar. Soal/pause membekukan seluruh simulasi. Bank, profil, progres, hasil belajar, 14 karakter dan tiga arena tetap tersedia. Inventori berlaku per balapan tanpa fitur save/resume mid-race.\n\nLaporan perilaku, tabel keseimbangan, seed, screenshot dan sumber ada di ZIP review. Benchmark cloud bukan win-rate siswa atau FPS HP. HP fisik dan file:// di cloud belum diuji.\n'
for kind in ['playable','review']:
 dest=R/('race-quest-pro-patch4-'+kind+'.zip')
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
  z.write(H,H.name);z.writestr('MULAI.txt',notes)
  if kind=='review':
   for f in sorted(B.rglob('*')):
    if f.is_file()and '__pycache__'not in f.parts and f.name!='release-metrics.json':z.write(f,'patch4-smart-ai/'+f.relative_to(B).as_posix())
 with zipfile.ZipFile(dest)as z:assert z.testzip()is None;assert z.read(H.name)==raw
 metrics[kind+'_zip']={'file':dest.name,'bytes':dest.stat().st_size,'sha256':sha(dest.read_bytes())}
(B/'release-metrics.json').write_text(json.dumps(metrics,indent=2));print(json.dumps(metrics,indent=2))
