from pathlib import Path
import re,hashlib
D=Path(__file__).resolve().parents[1];V=D.parent;B=V/'blokraya-patch8d-controls.html';s=B.read_text();original=s
assert hashlib.sha256(B.read_bytes()).hexdigest()=='6f311e1c10440bed8c8e6024425bc0ab750584d380f797a4bd3047b5a95740f8'
def replace(a,b,n=1):
 global s
 assert s.count(a)==n,(a[:120],s.count(a));s=s.replace(a,b)
replace('</head>','<script id="startupFullscreen">\n'+(D/'source/fullscreen.js').read_text()+'</script>\n<style id="patch8eStartupStyles">\n'+(D/'source/startup.css').read_text()+'</style>\n</head>')
replace('<p id="brLoadingDetail">Membaca data game…</p>', '<p id="brLoadingDetail">Membaca data game…</p><button id="brEnterButton" type="button" autofocus>Masuk BlokRaya</button>')
s,n=re.subn(r'(<script id="blokRayaLoading">).*?(</script>)',lambda m:m[1]+'\n'+(D/'source/loading.js').read_text()+m[2],s,flags=re.S);assert n==1
# Move the three original fullscreen functions, never the joystick/input code.
v=re.search(r'<script id="patch8dViewportTouch">(.*?)</script>',s,re.S)[1]
for name in ['fullscreenElement','requestFullscreen','toggleFullscreen']:
 line=next(x for x in v.splitlines()if x.startswith('function '+name+'('));v=v.replace(line+'\n','')
v=v.replace("const $=id=>", "const {fullscreenElement,requestFullscreen,toggleFullscreen}=root.RaceViewport;\nconst $=id=>",1)
s,n=re.subn(r'(<script id="patch8dViewportTouch">).*?(</script>)',lambda m:m[1]+v+m[2],s,flags=re.S);assert n==1
replace("case 'startRace':RaceViewport.requestFullscreen();await startRace();", "case 'startRace':await startRace();")
H=V/'blokraya-patch8e-startup.html';H.write_text(s)
print(H.name,len(s.encode()),'bytes; growth',len(s.encode())-len(original.encode()))
