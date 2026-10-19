/* Garage-only 3D workshop. No GLB, race renderer, model hierarchy or material edits. */
(function(root){'use strict';
const P={white:[.84,.87,.80],cream:[.61,.70,.69],teal:[.08,.24,.29],metal:[.12,.18,.21],wood:[.30,.39,.40],roof:[.065,.13,.18],leaf:[.18,.38,.33],lime:[.25,.50,.42],pink:[.35,.26,.30],yellow:[.94,.58,.12],rock:[.38,.47,.48],sand:[.52,.59,.57],black:[.027,.039,.045],orange:[.85,.29,.065],glass:[.80,.91,.94]};
class Workshop extends root.RacePontianakCity{
 upload(batch){const out=batch.upload(this.r);for(const m of out){m.p.material.color=P[m.key];m.p.material.rough=m.key==='black'?.96:.78;m.p.material.metal=m.key==='metal'?.25:0;if(m.key==='glass')m.p.material.emissive=[.55,.70,.76]}return out}
 tire(x,y,z){const b=this.batch,V=[],F=[],n=12,m=6;for(let i=0;i<n;i++)for(let j=0;j<m;j++){const a=i/n*Math.PI*2,t=j/m*Math.PI*2,rr=.38+.13*Math.cos(t);V.push([x+Math.cos(a)*rr,y+Math.sin(a)*rr,z+.13*Math.sin(t)])}for(let i=0;i<n;i++)for(let j=0;j<m;j++){const a=i*m+j,c=((i+1)%n)*m+j,d=((i+1)%n)*m+(j+1)%m,e=i*m+(j+1)%m;F.push([a,c,d],[a,d,e])}b.geometry('black',V,F)}
 build(){const b=this.batch;b.bevel('rock',[0,-.14,0],[18,.22,18],0,.08);for(let i=-4;i<=4;i++)for(const side of [-1,1]){b.box('wood',[i*2,-.026,0],[.018,.006,17.8]);if(side===1)b.box('wood',[0,-.026,i*2],[17.8,.006,.018])}
  b.cylinder('teal',[0,-.115,0],2.40,.10,48);b.ring('white',[0,-.009,0],2.35,.032,'XZ',64);b.ring('orange',[0,-.008,0],2.12,.022,'XZ',64);
  for(let k=0;k<4;k++){const yaw=k*Math.PI/2,local=(x,y,z)=>[x*Math.cos(yaw)+z*Math.sin(yaw),y,-x*Math.sin(yaw)+z*Math.cos(yaw)],box=(key,x,y,z,w,h,d)=>b.box(key,local(x,y,z),[w,h,d],yaw);
   box('roof',0,2.75,-6.7,13.7,5.55,.24);box('teal',0,.74,-6.54,13.4,1.50,.12);box('white',0,1.55,-6.45,13.3,.10,.045);box('orange',0,1.70,-6.45,13.3,.055,.04);for(const x of [-5.7,-2.8,0,2.8,5.7])box('metal',x,3.6,-6.49,.07,3.5,.08);
   if(k%2===1)for(let x=0;x<8;x++)for(let y=0;y<2;y++)box((x+y)%2?'white':'teal',(x-3.5)*.43,1.98+y*.43,-6.43,.425,.425,.035);
   box('metal',0,5.42,-3.8,5.7,.20,.42);box('glass',0,5.30,-3.8,5.45,.035,.30);box('teal',0,5.33,-6.45,7.2,.055,.045);
  }
  // Back tire rack: six tires on each side, one material batch for all rubber.
  for(const side of [-1,1]){const x=side*4.65;for(const yy of [.30,1.43,2.58])b.bevel('metal',[x,yy,-5.62],[2.85,.12,.75],0,.035);for(const xx of [-1.34,1.34])b.bevel('metal',[x+xx,1.50,-5.81],[.10,2.90,.10],0,.025);for(const yy of [.86,2.0])for(const dx of [-.91,0,.91])this.tire(x+dx,yy,-5.53)}
  // Visible studio softboxes sit outside the camera orbit and keep the kart area clear.
  for(const side of [-1,1]){const x=side*3.7,z=-3.8;b.bevel('metal',[x,1.12,z],[.08,2.24,.08],0,.02);for(const dx of [-.36,.36])b.beam('metal',[x,.40,z],[x+dx,.03,z+.25],.06);b.bevel('metal',[x,2.51,z],[.80,1.12,.18],0,.08);b.bevel('glass',[x,2.51,z+.105],[.67,.98,.045],0,.04)}
  b.bevel('teal',[0,.56,-5.85],[2.85,1.12,.90],0,.10);b.bevel('cream',[0,1.17,-5.85],[3.06,.14,1.03],0,.05);for(let j=0;j<3;j++){b.box('metal',[0,.26+j*.30,-5.384],[2.61,.025,.035]);b.box('white',[0,.39+j*.30,-5.35],[.66,.06,.045])}b.bevel('orange',[.45,1.48,-5.85],[1.15,.47,.62],0,.07);
  // Workbenches and pegboard; low-detail tools read as silhouettes rather than clutter.
  for(const z of [-4.5,4.5]){b.bevel('teal',[5.45,.62,z],[1.65,1.25,2.9],0,.10);b.bevel('cream',[5.45,1.29,z],[1.88,.15,3.05],0,.05);for(let j=0;j<3;j++){b.box('metal',[4.605,.36+j*.34,z],[.035,.025,2.55]);b.box('white',[4.57,.50+j*.34,z],[.06,.065,.60])}}
  b.bevel('cream',[6.44,2.72,-4.1],[.12,2.2,3.7],0,.06);for(let j=0;j<5;j++){const z=-5.45+j*.66;b.beam(j%2?'yellow':'metal',[6.32,1.95,z],[6.32,3.13,z],.12);b.beam('metal',[6.32,3.13,z],[6.32,3.36,z-.16],.09);b.beam('metal',[6.32,3.13,z],[6.32,3.36,z+.16],.09)}
  b.bevel('orange',[-5.55,.49,3.95],[1.30,.98,1.30],0,.13);b.beam('metal',[-5.94,1.03,3.95],[-5.17,1.03,3.95],.10);for(const z of [3.6,4.3])b.box('cream',[-5.55,.50,z],[1.33,.08,.05]);
  // Spare aerodynamic body panel display, safely outside the rotating preview camera.
  b.bevel('teal',[-6.38,2.82,1.0],[.20,1.1,2.35],0,.15);for(const z of [.26,1.74])b.box('white',[-6.25,2.82,z],[.04,1.10,.20]);
  this.bannerCanvas=document.createElement('canvas');this.bannerCanvas.width=1024;this.bannerCanvas.height=256;const c=this.bannerCanvas.getContext('2d');c.fillStyle='#102f43';c.fillRect(0,0,1024,256);c.fillStyle='#f4b447';c.fillRect(0,0,1024,12);c.fillRect(0,244,1024,12);c.textAlign='center';c.fillStyle='#f5f2df';c.font='900 102px sans-serif';c.fillText('RACE QUEST',512,137);c.fillStyle='#8fc7c7';c.font='600 29px sans-serif';c.fillText('PERFORMANCE GARAGE  /  PIT 01',512,199);const tex=this.texture(this.bannerCanvas);this.bannerGeometry=[];for(const side of [-1,1]){const z=side*6.42,cx=side*1.8,V=[[cx-2.3,1.65,z],[cx+2.3,1.65,z],[cx+2.3,2.85,z],[cx-2.3,2.85,z]],F=[[0,1,2],[0,2,3]],UV=side===-1?[[0,1],[1,1],[1,0],[0,0]]:[[1,1],[0,1],[0,0],[1,0]];this.bannerGeometry.push({V,F,UV});this.labels.push({key:'banner',p:this.r.mesh(V,F,[1,1,1],UV,tex,true)})}
  this.batches=[...this.upload(b),...this.labels];this.stats={triangles:this.batches.reduce((n,o)=>n+o.p.count/3,0),colour_draw_calls:this.batches.length,textures:this.textures.length};
 }
 draw(draw){const r=this.r,paint=r.paintMultiplier;r.paintMultiplier=null;try{for(const {p}of this.batches)draw.call(r,p,RaceMath.identity(),0)}finally{r.paintMultiplier=paint}}
 dispose(){for(const {p}of this.batches)for(const k of ['pos','normal','uv','index'])if(p[k])this.r.gl.deleteBuffer(p[k]);this.release();this.batches=[]}
}
const old=RaceRenderer.prototype.garage;
RaceRenderer.prototype.garage=function(character,time){if(!this.patchWorkshop)this.patchWorkshop=new Workshop(this,null);const begin=this.begin,draw=this.drawPrimitive;this.begin=function(eye,target,fog){const aspect=this.canvas.clientWidth/Math.max(1,this.canvas.clientHeight),factor=this.garageView==='close'?1:aspect<.95?.98:.89;eye=eye.map((v,i)=>target[i]+(v-target[i])*factor);begin.call(this,eye,target,fog);this.gl.uniform1f(this.L.uSunEnabled,0);this.patchWorkshop.draw(draw)};this.drawPrimitive=function(p,...a){if(p===this.studioFloor)return;return draw.call(this,p,...a)};try{return old.call(this,character,time)}finally{this.begin=begin;this.drawPrimitive=draw}};
let fade=null;document.getElementById('world').addEventListener('racequest:preview',()=>{if(document.body.dataset.screen!=='garage'||matchMedia('(prefers-reduced-motion: reduce)').matches)return;fade?.cancel();fade=document.getElementById('world').animate([{opacity:.66},{opacity:1}],{duration:210,easing:'ease-out'})});
new MutationObserver(()=>{if(document.body.dataset.screen!=='garage'){fade?.cancel();fade=null}}).observe(document.body,{attributes:true,attributeFilter:['data-screen']});
root.RacePatchWorkshop=Workshop;
})(globalThis);
