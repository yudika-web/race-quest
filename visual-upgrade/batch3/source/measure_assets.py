"""Reuse shared measured-bounds / GLTF accounting implementation."""
from pathlib import Path
s=(Path(__file__).resolve().parents[2]/'batch1/source/measure_assets.py').read_text().replace('race-quest-pro-batch1.html','race-quest-pro-batch3.html').replace('race-quest-visual-upgrade.html','race-quest-pro-batch2.html').replace("[('nara','Pinguin','Kapsul'),('bimo','Beruang','Buggy'),('sora','Kelinci','Formula')]","[('anjing','Anjing','Rally'),('tikus','Tikus','Mini Roadster'),('rubah','Rubah','GT')]")
exec(compile(s,__file__,'exec'))
# Real buffer-store measurements from the actual WebGL rig test, not heap estimates.
for row in report['models']:
 row['gpu_high_low_colour_and_depth_buffers_bytes']=rigs[row['id']]['gpu_buffer_bytes_before_cleanup']
 row['retired_gpu_buffer_count']=rigs[row['id']]['retired_gpu_buffer_count']
report['gpu_memory_scope']='Queried BUFFER_SIZE for both LODs, colour/depth geometry only; excludes HTML/JS heap, arena, textures, render targets and driver overhead. isBuffer verifies all recorded buffers are deleted on retirement.'
(D/'asset-metrics.json').write_text(json.dumps(report,indent=2))
