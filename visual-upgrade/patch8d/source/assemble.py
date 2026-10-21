from pathlib import Path
import re,hashlib
D=Path(__file__).resolve().parents[1];V=D.parent
baseline=V/'blokraya-patch8c-podium.html';s=baseline.read_text();original=s
assert hashlib.sha256(baseline.read_bytes()).hexdigest()=='b8239755f5968532a9127815cf5d15827b76b75abddacdf54541b8cd8afbbac9'
def replace(a,b,n=1):
 global s
 assert s.count(a)==n,(a[:150],s.count(a),n)
 s=s.replace(a,b)
def script(id,source):
 global s
 s,n=re.subn(r'(<script id="'+id+r'"[^>]*>).*?(</script>)',lambda m:m[1]+'\n'+(D/'source'/source).read_text().strip()+'\n'+m[2],s,flags=re.S)
 assert n==1
replace('</head>','<style id="patch8dViewportStyles">\n'+(D/'source/viewport.css').read_text()+'</style>\n</head>')
replace('<div class="rq-directions rq-controls"',(D/'source/joystick.html').read_text()+'<div class="rq-directions rq-controls"')
for prefix in ['hud','pause']:
 anchor='<select id="'+prefix+'TouchMode"><option value="auto">Otomatis · sesuai perangkat/input</option><option value="show">Selalu tampilkan</option><option value="hide">Sembunyikan · pakai keyboard</option></select></label>'
 replace(anchor,anchor+'<label class="field steering-choice"><span>Model kemudi sentuh</span><select id="'+prefix+'SteeringMode"><option value="analog">Analog · kemudi proporsional</option><option value="buttons">Tombol Kiri/Kanan · klasik</option></select></label>')
replace('WASD / panah: kemudi, gas, rem · C:', 'Analog: geser sedikit untuk belok perlahan, lepaskan untuk netral. Tangan kanan tetap dapat memakai gas, drift, loncat dan buff bersamaan. Pilih tombol klasik di Model kemudi sentuh. WASD / panah: kemudi, gas, rem · C:')
script('patch45HUD','hud.js')
replace('<script id="blokRayaModes">','<script id="patch8dViewportTouch">\n'+(D/'source/viewport-touch.js').read_text()+'</script>\n<script id="blokRayaModes">')
replace("function clearControls(){for(let k in controls)controls[k]=false;", "function clearControls(){RaceViewport.reset();for(let k in controls)controls[k]=false;")
replace('RaceHUD.bind(clearControls);',"RaceHUD.bind(clearControls);RaceViewport.bind(controls,()=>state.screen==='race'&&['racing','countdown'].includes(state.session?.status),clearControls);")
replace("case 'startRace':await startRace();", "case 'startRace':RaceViewport.requestFullscreen();await startRace();")
replace("case 'fullscreen':if(document.fullscreenElement)await document.exitFullscreen();else if(document.documentElement.requestFullscreen)await document.documentElement.requestFullscreen();else toast('Gunakan fitur layar penuh pada browser perangkat ini.');break;", "case 'fullscreen':await RaceViewport.toggleFullscreen();break;")
start=s.index("document.querySelectorAll('[data-control]').forEach(b=>{");end=s.index('\nconst keymap=',start)
s=s[:start]+'/* Pointer ownership is bound once by RaceViewport; keyboard handlers remain unchanged. */'+s[end:]
replace('Number(controls.left)+hardware.steer','Number(controls.left)+hardware.steer+RaceViewport.steer')
replace("now-state.lastScene>500)","now-state.lastScene>500||RaceViewport.dirty)")
replace('state.lastScene=now}\n  }','state.lastScene=now;RaceViewport.painted()}\n  }')
replace('RacePodium.cleanExport(clone);','RaceViewport.cleanExport(clone);RacePodium.cleanExport(clone);')
(V/'blokraya-patch8d-controls.html').write_text(s)
app=next(m[2] for m in re.finditer(r'<script([^>]*)>(.*?)</script>',s,re.S) if 'const state={screen:' in m[2]);(D/'source/application.js').write_text(app.strip()+'\n')
print(len(s.encode()),'bytes; growth',len(s.encode())-len(original.encode()))
