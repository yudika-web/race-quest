from pathlib import Path
import json,hashlib,zipfile
D=Path(__file__).resolve().parents[2];B=D/'patch2-audio-vfx';R=D.parent;H=D/'race-quest-pro-patch2.html';name='race-quest-pro-patch2'
required=['scope-verification','core-test-results','av-tests','budget-tests','stage-audio-tests','test-results','offline-test-results','export-tests','unchanged-renders','smoke-tests','vfx-capture-report','ui-capture-report','synthesis-metrics']
for n in required:assert json.loads((B/(n+'.json')).read_text())['status']=='passed',n
scope=json.loads((B/'scope-verification.json').read_text());assert hashlib.sha256(H.read_bytes()).hexdigest()==scope['html_sha256']
audit=json.loads((B/'audio-audit.json').read_text());av=json.loads((B/'av-tests.json').read_text());budget=json.loads((B/'budget-tests.json').read_text())
metrics={k:scope[k]for k in ['baseline','html_bytes','growth_bytes','html_sha256','under_25_decimal_MB']};metrics.update(original_embedded_audio_bytes=sum(a['bytes']for a in audit['embedded_audio']),new_embedded_audio_files=0,new_embedded_audio_bytes=0,new_synth_recipes=17,noise_loops=2,transient_voice_cap=8,reduced_voice_cap=5,particle_pool_slots=480,particle_caps={'high':320,'medium':200,'low':80,'reduced':32},shield_triangles=16,shield_draws_when_active=1,measured_audio=[{'device':v['device'],'pcm_rms':v['pcm_rms'],'voice_peak':v['audio']['voicePeak'],'source_peak':v['audio']['sourcePeak'],'pool_peak':v['pool']['peak'],'decode_failures':v['audio']['decodeFailures']}for v in av['devices']],all_assets_decode_fixture_pcm_bytes=sum(d['decoded_pcm_bytes']for d in budget['decoded']),teacher_export_bytes=json.loads((B/'export-tests.json').read_text())['export_bytes'],fps_measured=False,physical_phone_or_speakers_tested=False)
(B/'asset-metrics.json').write_text(json.dumps(metrics,indent=2))
notes='RACE QUEST PRO - PATCH 2 AUDIO & VFX\n\nEkstrak ZIP, lalu buka race-quest-pro-patch2.html di browser WebGL/Web Audio. Klik/sentuh tombol untuk mengaktifkan suara. Semua aset tertanam; tidak perlu internet/CDN. Suara > Audio Arcade menyediakan Master, Musik, SFX, Mesin, Mute, Kurangi suara intens dan Reduced Effects. Data bank/profil serta aturan game tetap dipertahankan.\n\nSFX baru adalah sintesis Web Audio orisinal; audio lama digunakan ulang. Belum diuji pada HP/speaker fisik. Laporan, preview audio, sumber dan screenshot tersedia di ZIP review.\n'
for kind in ['playable','review']:
 dest=R/(name+'-'+kind+'.zip')
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
  z.write(H,H.name);z.writestr('MULAI.txt',notes)
  if kind=='review':
   for f in sorted(B.rglob('*')):
    if f.is_file()and '__pycache__'not in f.parts and f.name!='release-metrics.json':z.write(f,'patch2-audio-vfx/'+f.relative_to(B).as_posix())
 with zipfile.ZipFile(dest)as z:assert z.testzip()is None;assert z.read(H.name)==H.read_bytes()
 metrics[kind+'_zip']={'name':dest.name,'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
(B/'release-metrics.json').write_text(json.dumps(metrics,indent=2));print(json.dumps(metrics,indent=2))
