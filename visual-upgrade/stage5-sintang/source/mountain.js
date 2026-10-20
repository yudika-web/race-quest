/* 6B Sintang: original procedural geometry; accepted City/Garden helpers reused.
 * Landmarks are stylized interpretations, not architectural/geological surveys.
 * No simulation, AI, item, assessment or actor code changes. */
(function(root){'use strict';
const Base=root.RaceScenery,Garden=root.RaceMempawahGarden,TAU=Math.PI*2;
const P={white:[.78,.77,.63],cream:[.62,.49,.28],teal:[.075,.28,.23],glass:[.045,.12,.13],metal:[.40,.44,.43],wood:[.28,.14,.06],roof:[.32,.17,.085],leaf:[.075,.29,.12],lime:[.25,.46,.16],pink:[.77,.19,.24],yellow:[.85,.60,.13],rock:[.26,.31,.33],sand:[.45,.38,.24],black:[.20,.26,.28],orange:[.56,.29,.09],lavender:[.48,.28,.58]};
const local=(p,x,y,z)=>[p.x+Math.cos(p.yaw)*x+Math.sin(p.yaw)*z,p.y+y,p.z-Math.sin(p.yaw)*x+Math.cos(p.yaw)*z];
const smooth=x=>{x=Math.max(0,Math.min(1,x));return x*x*(3-2*x)};
const BETANG={x:48,z:34,yaw:-2.12},KELAM={x:-150,z:180,yaw:-.27};
function noise(x,z){return 1.7+1.6*Math.sin(x*.019)*Math.cos(z*.021)+1.0*Math.sin((x+z)*.032)}
function land(r,x,z){const d=r.clearance(x,z),base=noise(x,z),flat=noise(BETANG.x,BETANG.z),blend=smooth((Math.hypot(x-BETANG.x,z-BETANG.z)-29)/14);return -.5+smooth((d-24)/28)*(flat*(1-blend)+base*blend)}
const GRID=[-1200,-600,-300];for(let x=-200;x<=280;x+=8)GRID.push(x);GRID.push(400,600,1200);
function sampledLand(r,x,z){const index=v=>{let a=0,b=GRID.length-1;while(b-a>1){const m=(a+b)>>1;if(GRID[m]>v)b=m;else a=m}return a},i=index(x),j=index(z),x0=GRID[i],x1=GRID[i+1],z0=GRID[j],z1=GRID[j+1],u=Math.max(0,Math.min(1,(x-x0)/(x1-x0))),v=Math.max(0,Math.min(1,(z-z0)/(z1-z0))),a=land(r,x0,z0)-.015,b=land(r,x1,z0)-.015,c=land(r,x0,z1)-.015,d=land(r,x1,z1)-.015;return u+v<=1?a+(b-a)*u+(c-a)*v:d+(c-d)*(1-u)+(b-d)*(1-v)}
class MountainRun extends Garden{
 upload(batch,noShadow=false){const out=batch.upload(this.r);for(const m of out){m.p.material.color=P[m.key]||P.white;m.p.material.rough=.92;m.p.material.metal=0;if(noShadow)m.key='shadow'}return out}
 anchor(p,radius,type){const d=this.r.clearance(p.x,p.z);if(d<radius+8.5)throw Error('Sintang: '+type+' terlalu dekat jalan.');const q={...p,y:this.r.groundAt(p.x,p.z),radius,type};this.objects.push({...q,clearance:d});this.landmarks.push(q);return q}
 terrain(){const V=[],F=[],coords=GRID;const n=coords.length;for(const z of coords)for(const x of coords)V.push([x,land(this.r,x,z)-.015,z]);for(let i=0;i<n-1;i++)for(let j=0;j<n-1;j++){const a=i*n+j;F.push([a,a+n,a+1],[a+1,a+n,a+n+1])}const old=this.r.ground;for(const k of ['pos','normal','uv','index'])if(old[k])this.r.gl.deleteBuffer(old[k]);this.r.ground=this.r.mesh(V,F,[.20,.39,.19],null,null,true)}
 build(){const r=this.r,t=this.track,b=this.batch,f=this.pavement,m=this.markings;this.plinth=new b.constructor();
  r.road.material.texture=r.roadTexture;r.road.material.color=[.78,.81,.76];r.road.material.rough=.94;r.shoulders.material.texture=null;r.shoulders.material.color=[.24,.39,.18];r.curbs.forEach((p,i)=>p.material.color=i?P.yellow:P.white);r.static=r.static.filter(o=>o.file==='prop_start_gate.glb');r.staticShadows.count=0;this.terrain();
  const kelam=this.anchor(KELAM,72,'bukit-kelam'),betang=this.anchor(BETANG,29,'betang-ensaid-panjang');this.monolith(kelam);this.longhouse(betang);this.connectPromenade(betang,13,65,3.3);
  // Terrace paths and embankments stay outside the original ±5m road surface.
  for(const side of [-1,1]){const V=[],F=[],W=[],WF=[];for(let i=0;i<=550;i++){const p=t.point(i/550*t.length);for(const d of [5.55,7.65])V.push([p.x+p.rightX*side*d,p.y+.15,p.z+p.rightZ*side*d]);const x=p.x+p.rightX*side*7.65,z=p.z+p.rightZ*side*7.65;W.push([x,r.groundAt(x,z)-.035,z],[x,p.y+.15,z]);if(i){const k=i*2;F.push([k-2,k,k-1],[k-1,k,k+1]);WF.push([k-2,k,k-1],[k-1,k,k+1])}}f.geometry('sand',V,F);f.geometry('rock',W,WF)}
  const stripe=(s0,s1,a,c)=>{const V=[];for(const s of [s0,s1]){const p=t.point(s);for(const d of [a,c])V.push([p.x+p.rightX*d,p.y+.106,p.z+p.rightZ*d])}m.geometry('white',V,[[0,2,1],[1,2,3]])};
  for(let s=8;s<t.length;s+=12)stripe(s,s+4,-.065,.065);for(let s=0;s<t.length;s+=3)for(const side of [-1,1])stripe(s,s+3,side*4.65,side*4.74);
  for(let i=0;i<64;i++){const p=this.locate((i+.35)/64,(i%2?1:-1)*(13.8+i%3),2.5,'pohon-hutan');if(p)this.forestTree(p,.9+i%4*.12)}
  for(let i=0;i<26;i++){const p=this.locate((i+.72)/26,(i%2?-1:1)*(27+i%3*4),3.2,'pohon-lapis-belakang');if(p)this.forestTree(p,1.10+i%3*.15)}
  for(let i=0;i<18;i++){const p=this.locate((i+.62)/18,(i%2?-1:1)*(46+i%3*5),3.3,'hutan-jauh');if(p)this.forestTree(p,1.1+i%3*.12)}
  for(let i=0;i<22;i++){const p=this.locate((i+.48)/22,(i%2?-1:1)*11.1,1.5,'semak-pakis');if(p)this.fern(p,i)}
  for(let i=0;i<12;i++){const p=this.locate((i+.4)/12,(i%2?-1:1)*9.9,.8,'lampu-jalur');if(p)this.trailLamp(p)}
  for(let i=0;i<18;i++){const p=this.locate((i+.6)/18,(i%2?-1:1)*(13.7+i%3),1.6,'batu-jalur');if(p)this.boulder(p,1.3+i%3*.35)}
  for(const u of [.13,.32,.55,.77])for(const side of [-1,1]){this.railAt(u*t.length,side*8.2,10)}
  for(const x of [-19,19]){const q={...betang,x:local(betang,x,0,11)[0],z:local(betang,x,0,11)[2]};this.bed(q,4.0,1.6,x>0?0:2)}
  const sign={...betang,x:local(betang,9,0,12.6)[0],z:local(betang,9,0,12.6)[2]};b.bevel('wood',local(sign,0,1.02,0),[7.9,1.1,.14],sign.yaw,.06);for(const x of [-2.8,2.8])b.box('wood',local(sign,x,.48,0),[.16,.96,.16],sign.yaw);this.label(sign,'INSPIRASI RUMAH BETANG\nENSAID PANJANG',7.7,.95,1.02,.08);
  this.batches=[...this.upload(b),...this.upload(f,true),...this.upload(this.plinth,true),...this.upload(m,true),...this.labels];this.stats={landmarks:this.landmarks.map(p=>({...p})),objects:this.objects,triangles:this.batches.reduce((n,o)=>n+o.p.count/3,0),colour_draw_calls:this.batches.length,shadow_draw_calls:this.batches.filter(o=>o.key!=='shadow').length,textures:this.textures.length,static_visuals:true,terrain_triangles:r.ground.count/3,historical_accuracy_verified:false};
 }
 forestTree(p,s){const b=this.batch;b.box('wood',local(p,0,2.2*s-.11,0),[.40*s,4.4*s+.22,.40*s],p.yaw);b.beam('wood',local(p,0,2.5*s,0),local(p,1.2*s,4.1*s,.3),.18*s);b.bevel('leaf',local(p,0,4.9*s,0),[4.1*s,2.9*s,3.5*s],p.yaw,.50*s);b.bevel('lime',local(p,-.8*s,6.0*s,.15*s),[2.7*s,1.9*s,2.7*s],p.yaw+.15,.36*s);b.bevel('leaf',local(p,1.25*s,4.75*s,.25),[2.1*s,2.05*s,2.5*s],p.yaw-.1,.30*s)}
 fern(p,i){const b=this.batch;b.bevel(i%2?'leaf':'lime',local(p,0,.28,0),[2.0,.70,1.4],p.yaw,.25);for(let j=0;j<4;j++){const a=j/4*TAU;b.beam('lime',local(p,0,.3,0),local(p,Math.cos(a)*1.2,.78,Math.sin(a)*1.2),.18,.28)}}
 trailLamp(p){const b=this.batch;b.bevel('rock',local(p,0,.08,0),[.6,.32,.6],p.yaw,.07);b.box('wood',local(p,0,1.55,0),[.20,3.1,.20],p.yaw);b.bevel('yellow',local(p,0,3.0,0),[.48,.30,.48],p.yaw,.05);b.bevel('teal',local(p,0,3.22,0),[.64,.16,.64],p.yaw,.04)}
 railAt(s,lat,len){const b=this.batch,points=[-len/2,0,len/2].map(d=>this.track.place(s+d,lat));for(const p of points){b.box('wood',[p.x,p.y+.65,p.z],[.20,1.3,.20],p.yaw);b.box('yellow',[p.x,p.y+1.31,p.z],[.25,.10,.25],p.yaw)}for(const y of [.55,1.06])for(let i=0;i<2;i++)b.beam('cream',[points[i].x,points[i].y+y,points[i].z],[points[i+1].x,points[i+1].y+y,points[i+1].z],.11)}
 boulder(p,s){const b=this.batch;b.bevel('rock',local(p,0,.5*s,0),[1.9*s,1.3*s,1.45*s],p.yaw,.28*s);b.bevel('leaf',local(p,-.25*s,1.03*s,.1*s),[1.15*s,.22*s,.8*s],p.yaw,.07*s)}
 monolith(p){const b=this.batch,n=16,rings=[[-8,1.08],[1,1.02],[18,1.01],[41,.95],[61,.82],[75,.56],[81,.25],[82,.035]],V=[];
  for(let j=0;j<rings.length;j++){const[h,rad]=rings[j];for(let i=0;i<n;i++){const a=i/n*TAU,c=Math.cos(a),s=Math.sin(a),x=Math.sign(c)*Math.pow(Math.abs(c),.67)*54*rad,z=Math.sign(s)*Math.pow(Math.abs(s),.70)*39*rad,y=h+(j>1?1.3*Math.sin(a*3+.4)+.55*Math.cos(a*5):0);V.push(local(p,x,y,z))}}
  // Continuous lofted granite mass: broad steep walls, softened shoulder and dome crown.
  for(let j=0;j<rings.length-1;j++)for(let i=0;i<n;i++){const a=V[j*n+i],c=V[j*n+(i+1)%n],d=V[(j+1)*n+(i+1)%n],e=V[(j+1)*n+i],lerp=(a,b,t)=>a.map((v,k)=>v+(b[k]-v)*t),us=j>0&&j<4&&i%4===1?[0,.76,.84,1]:[0,1];for(let k=0;k<us.length-1;k++){const u=us[k],v=us[k+1],key=us.length>2&&k===1?'black':i%5===1?'metal':'rock';b.geometry(key,[lerp(a,c,u),lerp(a,c,v),lerp(e,d,v),lerp(e,d,u)],[[0,2,1],[0,3,2]])}}
  const top=(rings.length-1)*n;b.geometry('rock',V.slice(top),Array.from({length:n-2},(_,i)=>[0,i+2,i+1]));
  // Surface colour bands follow the loft itself; no floating decal fins.
  for(let i=0;i<12;i++){const a=i*2.399963,q=local(p,Math.cos(a)*74,0,Math.sin(a)*59),d=this.r.clearance(q[0],q[2]);if(d>12.5){const tree={x:q[0],z:q[2],y:this.r.groundAt(q[0],q[2]),yaw:a};this.objects.push({type:'hutan-kaki-kelam',...tree,radius:3.3,clearance:d});this.forestTree(tree,1.15)}}
  for(let i=0;i<11;i++){const a=i*2.399963,q=local(p,Math.cos(a)*(61+3*Math.sin(i*1.3)),0,Math.sin(a)*(46+2*Math.cos(i)));const o={x:q[0],z:q[2],y:this.r.groundAt(q[0],q[2]),yaw:a};this.boulder(o,2.0+i%3*.35);if(i%2)this.fern({...o,x:o.x+2.0,z:o.z+1},i)}
 }
 longhouse(p){const b=this.batch,f=this.pavement,box=(k,x,y,z,w,h,d,bev=.06)=>b.bevel(k,local(p,x,y,z),[w,h,d],p.yaw,bev),beam=(k,a,c,w,d=w)=>b.beam(k,local(p,...a),local(p,...c),w,d);
  f.bevel('sand',local(p,0,.08,1),[53,.20,24],p.yaw,.2);
  // A single long gabled timber house: raised living floor, repeated bays and common gallery.
  for(let i=-5;i<=5;i++)for(const z of [-4.0,0,4.0,7.3])box('wood',i*4.25,1.6,z,.38,3.3,.38,.035);
  box('wood',0,3.3,1.35,46,.30,14.0);box('orange',0,5.35,0,44.0,3.75,9.5,.09);box('wood',0,7.30,0,44.5,.22,10.0,.04);
  for(let i=-5;i<=5;i++){const x=i*3.75;if(i){box('wood',x,5.6,4.81,2.85,2.44,.10,.025);box('glass',x,5.77,4.88,1.7,1.2,.04,.01);box('cream',x,5.77,4.93,.07,1.24,.035,.01);box('wood',x,5.2,7.55,.20,3.65,.20,.025);box('cream',x,4.07,7.55,3.45,.10,.13,.02);for(const dx of [-1.1,0,1.1])box('wood',x+dx,3.82,7.55,.09,.66,.09,.015)}else{box('cream',0,4.95,4.84,2.05,2.9,.12);box('wood',0,4.95,4.94,1.80,2.65,.05);box('yellow',.6,4.95,4.98,.08,.18,.025)}}
  const V=[[-24,7.48,-6.0],[24,7.48,-6.0],[24,11.5,0],[-24,11.5,0],[-24,7.48,8.6],[24,7.48,8.6]],v=V.map(q=>local(p,...q));b.geometry('roof',v,[[0,3,2],[0,2,1],[4,5,2],[4,2,3]]);
  for(const side of [-1,1]){b.geometry('wood',[local(p,side*22.1,7.45,-4.75),local(p,side*22.1,11.2,0),local(p,side*22.1,7.45,4.75)],[[0,1,2]]);for(const z of [-6,8.6])beam('cream',[-24,7.51,z],[24,7.51,z],.10);beam('wood',[side*24,7.48,-6],[side*24,11.5,0],.18);beam('wood',[side*24,11.5,0],[side*24,7.48,8.6],.18)}beam('wood',[-24.2,11.53,0],[24.2,11.53,0],.20);
  // Plain diamond trim only: no invented sacred motifs or royal/regional emblem.
  for(const x of [-15,-7.5,7.5,15]){const v=[[x-.35,4.65,4.94],[x,5.0,4.94],[x+.35,4.65,4.94],[x,4.3,4.94]].map(q=>local(p,...q));b.geometry('white',v,[[0,1,2],[0,2,3]])}
  // Central stair has supported treads and handrails, separate from the gallery balusters.
  for(let i=0;i<12;i++){const z=8.25+i*.34,h=(12-i)*.275;box('wood',0,h/2+.1,z,2.55,h,.37,.025)}for(const side of [-1,1]){beam('cream',[side*1.4,4.18,8.0],[side*1.4,.95,12.25],.11);for(const z of [8.0,10.0,12.25]){const h=4.18-(z-8)*.76;box('wood',side*1.4,h/2,z,.14,h,.14,.02)}}
 }
}
const ground=RaceRenderer.prototype.groundAt;RaceRenderer.prototype.groundAt=function(x,z){if(this.track?.id!=='sintang')return ground.call(this,x,z);return this.clearance(x,z)<=21.45?ground.call(this,x,z):sampledLand(this,x,z)};
const sky=RaceRenderer.prototype.skyPalette;RaceRenderer.prototype.skyPalette=function(){if(this.track?.id!=='sintang')return sky.call(this);const w=this.weather==='rain'?.55:this.weather==='fog'?.75:0;return{top:[.25,.59,.81].map((v,i)=>v*(1-w)+[.47,.57,.64][i]*w),horizon:[.79,.87,.84].map((v,i)=>v*(1-w)+[.73,.79,.81][i]*w)}};
const build=Base.prototype.build,draw=Base.prototype.draw;Base.prototype.build=function(track){if(this.sintang){this.sintang.release();this.sintang=null}if(track.id!=='sintang')return build.call(this,track);for(const key of ['city','garden','coast','sambas'])if(this[key]){this[key].release();this[key]=null}this.dispose();this.wildlife=[];this.ponds=[];this.landmarks=[];this.sintang=new MountainRun(this.r,track);this.batches=this.sintang.batches;this.landmarks=this.sintang.landmarks};Base.prototype.draw=function(time,pos){if(this.sintang){this.sintang.draw();return}return draw.call(this,time,pos)};
root.RaceSintangMountain=MountainRun;root.RaceSintangMountain.landHeight=sampledLand;const config=JSON.parse(document.getElementById('stage6bTrack').textContent);if(RaceCore.STAGES.some(t=>t.id===config.id))throw Error('Stage Sintang sudah terdaftar.');RaceCore.STAGES.push(config);
})(globalThis);
