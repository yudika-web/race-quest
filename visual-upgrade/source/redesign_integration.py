"""Small renderer extension for glTF vertex colors and garage-only orbit modes."""
def integrate(s,renderer,D):
 renderer=renderer.replace('attribute vec3 aPos,aNormal;', 'attribute vec3 aPos,aNormal,aPaint;')
 renderer=renderer.replace('varying vec3 vNormal,vWorld;', 'varying vec3 vNormal,vWorld,vPaint;')
 renderer=renderer.replace('vWorld=w.xyz;vNormal=', 'vWorld=w.xyz;vPaint=aPaint;vNormal=')
 renderer=renderer.replace('vec3 base=uColor*uPaint;', 'vec3 base=uColor*uPaint*vPaint;')
 renderer=renderer.replace("['aPos','aNormal','aUV']", "['aPos','aNormal','aUV','aPaint']")
 renderer=renderer.replace('const primitives={};', 'const primitives={};')
 renderer=renderer.replace("normal:this.buffer(normal),uv:","normal:this.buffer(normal),paint:p.attributes.COLOR_0===undefined?null:this.buffer(acc(p.attributes.COLOR_0)),uv:")
 renderer=renderer.replace('[p.pos,p.normal,p.uv,p.index]', '[p.pos,p.normal,p.uv,p.paint,p.index]')
 renderer=renderer.replace("gl.uniform1f(L.uHero,mat.hero||0);", "if(p.paint){gl.bindBuffer(gl.ARRAY_BUFFER,p.paint);gl.enableVertexAttribArray(L.aPaint);gl.vertexAttribPointer(L.aPaint,3,gl.FLOAT,false,0,0)}else{gl.disableVertexAttribArray(L.aPaint);gl.vertexAttrib3f(L.aPaint,1,1,1)}\n  gl.uniform1f(L.uHero,mat.hero||0);")
 renderer=renderer.replace('const gl=this.gl,L=this.PL;gl.useProgram', 'const gl=this.gl,L=this.PL;gl.disableVertexAttribArray(this.L.aPaint);gl.useProgram')
 # Replace only the garage method. The race method below remains byte-identical.
 old=next(line for line in renderer.splitlines() if line.startswith(' garage(character,time)'))
 new=''' garage(character,time){
  if(this.garageCharacter!==character){this.prepareModels([KARTS[character]]);this.garageCharacter=character}
  this.canvas.__garageRenderer=this;
  if(!this.garageOrbit)this.garageOrbit={yaw:.52,pitch:.318,scale:1,auto:true,dragging:false,lastTime:null};
  const orbit=this.garageOrbit,dt=orbit.lastTime===null?0:Math.max(0,Math.min(.05,time-orbit.lastTime));orbit.lastTime=time;
  if(orbit.auto&&!orbit.dragging)orbit.yaw+=dt*.12;
  const close=this.garageView==='close',narrow=this.canvas.clientWidth<600,cat=character===0;
  const target=[0,close?(cat?1.32:1.19):(narrow?.70:.85),close?.015:0],radius=(close?(cat?(narrow?1.85:1.75):(narrow?2.15:1.95)):4.0)*orbit.scale;
  const eye=[Math.sin(orbit.yaw)*radius*Math.cos(orbit.pitch),target[1]+radius*Math.sin(orbit.pitch),Math.cos(orbit.yaw)*radius*Math.cos(orbit.pitch)];
  this.clock=time;this.weather='clear';this.begin(eye,target,0);this.gl.uniform1f(this.L.uSunEnabled,0);
  this.drawPrimitive(this.studioFloor,M.identity(),0);this.drawShadow(M.trans([0,.002,0]));this.drawModel(KARTS[character],M.identity(),{fog:0});
 }'''
 renderer=renderer.replace(old,new)
 controls='''<div class="garage-view-controls" role="toolbar" aria-label="Pratinjau model"><button type="button" data-garage-view="full" aria-pressed="true">Mobil + Karakter</button><button type="button" data-garage-view="close" aria-pressed="false">Close-up Karakter</button><button type="button" data-garage-auto aria-pressed="true" aria-label="Rotasi otomatis" title="Rotasi otomatis">↻</button><button type="button" data-garage-reset aria-label="Atur ulang pratinjau" title="Atur ulang pratinjau">⟲</button></div>'''
 s=s.replace('<div class="garage-preview" id="garagePreviewHost">','<div class="garage-preview" id="garagePreviewHost">'+controls)
 s=s.replace('Pratinjau 3D berputar','Geser untuk memutar · cubit atau scroll untuk zoom')
 css='''
#garagePreviewHost{position:relative}
.garage-view-controls{position:absolute;z-index:5;left:12px;right:12px;top:12px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr) 34px 34px;gap:5px;max-width:500px;pointer-events:auto}
.garage-view-controls button{min-height:36px;padding:7px 8px;border:1px solid #8cb5cf55;border-radius:10px;background:#10233ce8;color:#d6e5f4;font-size:11px;font-weight:700;white-space:nowrap;backdrop-filter:blur(8px)}
.garage-view-controls button[aria-pressed=true]{background:#ffc078;color:#182c42;border-color:#ffc078}
body[data-screen=garage] #world{cursor:grab;touch-action:none}
body[data-screen=garage] #world:active{cursor:grabbing}
@media(max-width:720px){.garage-view-controls{left:9px;right:9px;top:9px;gap:4px;grid-template-columns:minmax(0,1fr) minmax(0,1fr) 28px 28px}.garage-view-controls button{font-size:10px;padding:6px 4px;min-height:32px}}
'''
 s=s.replace('</style>',css+'</style>',1)
 # Inline controller is included in exported games, with no fetch/CDN dependency.
 s=s.replace('</body>', '<script>'+ (D/'source/garage_preview.js').read_text()+'</script>\n</body>')
 return s,renderer
