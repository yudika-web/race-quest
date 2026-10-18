"""Embed GLBs and minimal renderer changes into the untouched original game."""
from pathlib import Path
import re,json,base64,hashlib
D=Path(__file__).resolve().parents[1]
s=(D/'original.html').read_text();assets=json.loads(re.search(r'<script id="assetData"[^>]*>(.*?)</script>',s,re.S)[1])
for key,file in [('kart_arka.glb','race-quest-cat-sport.glb'),('kart_arka_low.glb','race-quest-cat-sport-low.glb')]:
 b=(D/file).read_bytes();assets[key]={'uri':'data:model/gltf-binary;base64,'+base64.b64encode(b).decode(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
s=re.sub(r'(<script id="assetData"[^>]*>).*?(</script>)',lambda m:m[1]+json.dumps(assets,separators=(',',':'))+m[2],s,flags=re.S)
renderer=(D/'source/original-script-4.js').read_text()
old="drawModel(file,matrix,{spin=0,steer=0,fog=1}={}){"
new="""drawModel(file,matrix,{spin=0,steer=0,fog=1,speed=0,lift=0}={}){
  const hero=file==='kart_arka.glb';
  if(hero&&(this.quality==='low'||(fog&&this.eye&&Math.hypot(matrix[12]-this.eye[0],matrix[14]-this.eye[2])>24)))file='kart_arka_low.glb';
  const time=this.clock||0,scaleXYZ=(x,y,z)=>{const m=M.identity();m[0]=x;m[5]=y;m[10]=z;return m};
  // All idle, suspension and facial motion uses simulation time, never wall time.
  const blinkPhase=(time+1.17)%4.7,blink=blinkPhase<.16?Math.max(.045,Math.abs(blinkPhase-.08)/.08):1;
  const articulate=(name,world)=>{
   if(!hero)return world;
   if(name==='body_suspension')world=M.mul(world,M.mul(M.trans([0,Math.sin(time*12)*Math.min(.007,speed*.00045)-Math.min(.018,lift*.009),0]),M.rz(-steer*Math.min(1,speed/12)*.045)));
   if(name==='driver')world=M.mul(world,M.mul(M.rz(steer*.018),M.rx(-Math.min(.10,lift*.035))));
   if(name==='eyes')world=M.mul(world,scaleXYZ(1,blink,1));
   if(name==='ear_l'||name==='ear_r')world=M.mul(world,M.rz(Math.sin(time*2.2+(name==='ear_l'?0:1.4))*.035+steer*.025));
   if(name==='tail')world=M.mul(world,M.ry(Math.sin(time*1.9)*.10+steer*.12));
   return world;
  };"""
assert old in renderer;renderer=renderer.replace(old,new)
needle="if(/wheel_.._spin$/.test(n.name))world=M.mul(world,M.rx(spin));"
assert needle in renderer;renderer=renderer.replace(needle,needle+"world=articulate(n.name,world);")
renderer=renderer.replace("{spin:p.s/.205,steer:-(p.steering||0)*.42}","{spin:p.s/.205,steer:-(p.steering||0)*.42,speed:p.speed,lift:p.y||0}")
renderer=renderer.replace("{spin:player.s/.205,steer:-(player.steering||0)*.42}","{spin:player.s/.205,steer:-(player.steering||0)*.42,speed:player.speed,lift:player.y||0}")
renderer=renderer.replace("{spin:a.s/.205,steer:-tr.curvature(a.s)*3}","{spin:a.s/.205,steer:-tr.curvature(a.s)*3,speed:a.speed,lift:a.y||0}")
renderer=renderer.replace("{spin:a.s/.205,steer:-session.track.curvature(a.s)*3}","{spin:a.s/.205,steer:-session.track.curvature(a.s)*3,speed:a.speed,lift:a.y||0}")
# Clear both LODs with a retired hero; retain either only while the hero is in use.
renderer=renderer.replace("for(const f of KARTS)if(this.models[f]&&!keep.has(f))", "if(keep.has('kart_arka.glb'))keep.add('kart_arka_low.glb');for(const f of [...KARTS,'kart_arka_low.glb'])if(this.models[f]&&!keep.has(f))")
# Sun depth pass applies the same animated pivots, so the cat does not cast a detached shadow.
# Garage uses deterministic idle time and a contact shadow; race time remains session.elapsed.
renderer=renderer.replace("this.weather='clear';this.begin([Math.sin(.4+time*.12)","this.clock=time;this.weather='clear';this.begin([Math.sin(.4+time*.12)")
renderer=renderer.replace('this.shadow=this.makeShadow();', '''this.shadow=this.makeShadow();
  const studioV=[[0,-.008,0]],studioF=[];for(let i=0;i<65;i++){const a=i/64*Math.PI*2;studioV.push([Math.cos(a)*1.5,-.008,Math.sin(a)*1.5]);if(i<64)studioF.push([0,i+2,i+1])}
  this.studioFloor=this.mesh(studioV,studioF,[.028,.048,.067],null,null,true);this.studioFloor.material.rough=.82;
''')
renderer=renderer.replace("this.gl.uniform1f(this.L.uSunEnabled,0);this.drawModel(KARTS[character]", "this.gl.uniform1f(this.L.uSunEnabled,0);this.drawPrimitive(this.studioFloor,M.identity(),0);this.drawShadow(M.trans([0,.002,0]));this.drawModel(KARTS[character]")
# Bounded studio reflection for new hero surfaces; retain the existing shader path for all other assets.
renderer=renderer.replace('uSunQuality;uniform vec3', 'uSunQuality,uHero,uFur;uniform vec3')
renderer=renderer.replace("'uPaint'])this.L", "'uPaint','uHero','uFur'])this.L")
renderer=renderer.replace('vec3 c=base*diffuse+specColor*sp+uEmissive*.42;', """vec3 c=base*diffuse+specColor*sp+uEmissive*.42;
 if(uHero>.5){vec3 reflection=reflect(-v,n);float studio=pow(max(0.0,dot(reflection,normalize(vec3(-.4,.85,.3)))),mix(14.0,3.0,rough));
 c+=uHero*(1.0-rough)*mix(vec3(.07,.16,.23),vec3(.42,.55,.64),studio)*(uMetal*.35+.10);
 float furVariation=sin(vWorld.x*73.0+sin(vWorld.y*61.0))*sin(vWorld.z*67.0+vWorld.y*41.0);
 c*=1.0+uFur*furVariation*.017;}
""")
renderer=renderer.replace('double:mat.doubleSided,texture:', "double:mat.doubleSided,hero:/^[0-9][0-9]_/.test(mat.name||'')?1:0,fur:/^(10_|11_)/.test(mat.name||'')?1:0,texture:")
renderer=renderer.replace('gl.uniform3fv(L.uColor,mat.color);', 'gl.uniform1f(L.uHero,mat.hero||0);gl.uniform1f(L.uFur,mat.fur||0);gl.uniform3fv(L.uColor,mat.color);')
renderer=renderer.replace('[0,.95,0],0);this.gl.uniform1f', '[0,this.canvas.clientWidth<600?.70:.85,0],0);this.gl.uniform1f')
s=s.replace((D/'source/original-script-4.js').read_text(),renderer)
# Give the garage a quiet studio backdrop rather than competing scene artwork.
css='''
/* Hero studio: controls and preview occupy separate grid cells. */
body[data-screen=garage] #scene{background:radial-gradient(ellipse at 50% 72%,#31516a 0%,#152c43 54%,#0b182b 100%)}
body[data-screen=garage] .garage-model-note{background:#0b1929d9;border:1px solid #86cde633;border-radius:12px;padding:10px 14px;backdrop-filter:blur(8px)}
body[data-screen=garage] .garage-preview{overflow:hidden}
@media(max-width:700px){body[data-screen=garage] .garage-bottom{gap:8px}body[data-screen=garage] .garage-bottom .btn{padding:10px 13px;font-size:12px}}
'''
s=s.replace('</style>',css+'</style>',1)
(D/'race-quest-visual-upgrade.html').write_text(s)
(D/'source/upgraded-renderer.js').write_text(renderer)
print('HTML bytes',len(s.encode()))
