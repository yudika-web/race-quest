/* 6D Bengkayang. Fictional forest route and original procedural landscape inspired
 * by the broad Riam Merasap cascade, not a geographic reconstruction. */
(function(root){'use strict';
const Base=root.RaceScenery,Forest=root.RaceSintangMountain,TAU=Math.PI*2,WATER=-1.05;
const P={white:[.86,.91,.87],cream:[.65,.64,.45],teal:[.075,.36,.32],glass:[.06,.17,.19],metal:[.36,.43,.42],wood:[.29,.17,.08],roof:[.25,.17,.10],leaf:[.065,.27,.13],lime:[.24,.44,.19],pink:[.67,.24,.32],yellow:[.86,.65,.18],rock:[.31,.37,.37],sand:[.46,.42,.29],black:[.19,.27,.28],orange:[.62,.32,.12],cascadeWhite:[.90,.95,.94],fall:[.58,.80,.82],rocklight:[.37,.42,.40],rockdark:[.25,.31,.31]};
const local=(p,x,y,z)=>[p.x+Math.cos(p.yaw)*x+Math.sin(p.yaw)*z,p.y+y,p.z-Math.sin(p.yaw)*x+Math.cos(p.yaw)*z],smooth=x=>{x=Math.max(0,Math.min(1,x));return x*x*(3-2*x)};
const centre=z=>45+5*Math.sin((z-110)*.02),width=z=>12+14*Math.exp(-Math.pow((z-105)/23,2));
const bridge=p=>p.z<117&&Math.abs(p.x-centre(p.z))<32;
function land(x,z){const upland=25.5*smooth((z-129)/11)*smooth((97-Math.abs(x-45))/25),d=Math.abs(x-centre(z)),cut=z<126?(1-smooth((d-width(z))/8))*3.0:0;return -.5+upland-cut}
const GRID=[-1600,-600,-300];for(let x=-240;x<=300;x+=6)GRID.push(x);GRID.push(500,800,1600);
function sampled(x,z){const index=v=>{let a=0,b=GRID.length-1;while(b-a>1){const m=(a+b)>>1;if(GRID[m]>v)b=m;else a=m}return a},i=index(x),j=index(z),x0=GRID[i],x1=GRID[i+1],z0=GRID[j],z1=GRID[j+1],u=Math.max(0,Math.min(1,(x-x0)/(x1-x0))),v=Math.max(0,Math.min(1,(z-z0)/(z1-z0))),a=land(x0,z0),b=land(x1,z0),c=land(x0,z1),d=land(x1,z1);return u+v<=1?a+(b-a)*u+(c-a)*v:d+(c-d)*(1-u)+(b-d)*(1-v)}
function nearest(r,x,z){let d=Infinity,p=null;for(const q of r.track.points){const n=Math.hypot(q.x-x,q.z-z);if(n<d){d=n;p=q}}return{d,p}}
class WaterfallAdventure extends Forest{
 upload(batch,noShadow=false){const out=batch.upload(this.r);for(const m of out){m.p.material.color=P[m.key]||P.white;m.p.material.rough=m.key==='fall'?.65:.93;m.p.material.metal=0;if(m.key==='cascadeWhite'||m.key==='fall'){m.p.material.emissive=[.10,.12,.12];m.key='shadow'}if(noShadow)m.key='shadow'}return out}
 replace(...a){return root.RaceSentarumLake.prototype.replace.apply(this,a)}
 anchor(p,radius,type){const d=this.r.clearance(p.x,p.z);if(d<radius+8.5)throw Error('Bengkayang landmark too close: '+type);const q={...p,y:p.y??this.r.groundAt(p.x,p.z),radius,type};this.landmarks.push(q);this.objects.push({...q,clearance:d});return q}
 terrain(){const V=[],F=[],n=GRID.length;for(const z of GRID)for(const x of GRID)V.push([x,land(x,z),z]);for(let j=0;j<n-1;j++)for(let i=0;i<n-1;i++){const a=j*n+i;F.push([a,a+n,a+1],[a+1,a+n,a+n+1])}this.replace('ground',V,F,[.18,.36,.20]);
  const wV=[],wF=[];for(let i=0;i<=180;i++){const z=-1500+i/180*1626,c=centre(z),w=width(z)+11;wV.push([c-w,WATER,z],[c+w,WATER,z]);if(i){const k=i*2;wF.push([k-2,k,k-1],[k-1,k,k+1])}}this.replace('water',wV,wF,[.055,.35,.38]);this.r.water.material.water=1;
  // Preserve broad earthen shoulders on land, but open the river under both bridges.
  const SV=[],SF=[];for(const side of [-1,1])for(let i=0;i<550;i++){const V=[];for(const j of [i,i+1]){const p=this.track.point(j/550*this.track.length),end=bridge(p)?7.65:21.45;for(const d of [5.45,end])V.push([p.x+p.rightX*side*d,(1-(d-5.45)/16)*(p.y+.02)+(d-5.45)/16*(-.49),p.z+p.rightZ*side*d])}const k=SV.length;SV.push(...V);SF.push([k,k+2,k+1],[k+1,k+2,k+3])}this.replace('shoulders',SV,SF,[.27,.40,.22]);
  // Spatially indexed triangle heights avoid floating props at bridge/earth transitions.
  const bins=new Map();for(const face of SF){const v=face.map(i=>SV[i]),xs=v.map(q=>q[0]),zs=v.map(q=>q[2]);for(let x=Math.floor(Math.min(...xs)/16);x<=Math.floor(Math.max(...xs)/16);x++)for(let z=Math.floor(Math.min(...zs)/16);z<=Math.floor(Math.max(...zs)/16);z++){const key=x+','+z;if(!bins.has(key))bins.set(key,[]);bins.get(key).push(v)}}
  this.r._bengkayangSurface=(x,z)=>{let h=sampled(x,z);for(const[a,b,c]of bins.get(Math.floor(x/16)+','+Math.floor(z/16))||[]){const den=(b[2]-c[2])*(a[0]-c[0])+(c[0]-b[0])*(a[2]-c[2]);if(Math.abs(den)<1e-9)continue;const l=((b[2]-c[2])*(x-c[0])+(c[0]-b[0])*(z-c[2]))/den,m=((c[2]-a[2])*(x-c[0])+(a[0]-c[0])*(z-c[2]))/den,n=1-l-m;if(l>=-1e-7&&m>=-1e-7&&n>=-1e-7)h=Math.max(h,l*a[1]+m*b[1]+n*c[1])}return h}

 }
 build(){const r=this.r,t=this.track,b=this.batch,f=this.pavement,m=this.markings;
  r.road.material.texture=r.roadTexture;r.road.material.color=[.81,.84,.79];r.road.material.rough=.95;r.curbs.forEach((p,i)=>p.material.color=i?P.yellow:P.white);r.static=r.static.filter(o=>o.file==='prop_start_gate.glb');r.staticShadows.count=0;this.terrain();
  const fall=this.anchor({x:45,z:142,y:-.5,yaw:0},42,'riam-merasap-inspired-cascade'),deck=this.anchor({x:-12,z:106,yaw:Math.PI},7.2,'forest-overlook');this.cascade(fall);this.overlook(deck);
  for(const side of [-1,1]){const V=[],F=[];for(let i=0;i<=550;i++){const p=t.point(i/550*t.length);for(const d of [5.55,7.65])V.push([p.x+p.rightX*side*d,p.y+.14,p.z+p.rightZ*side*d]);if(i){const k=i*2;F.push([k-2,k,k-1],[k-1,k,k+1])}}f.geometry('sand',V,F)}
  for(let s=0;s<t.length;s+=5){const p=t.point(s);if(!bridge(p))continue;for(const side of [-1,1]){const q=t.place(s,side*7.8),next=t.place(s+5,side*7.8),bed=sampled(q.x,q.z);b.box('rock',[q.x,(bed+q.y)/2,q.z],[.45,q.y-bed,.45],q.yaw);b.box('wood',[q.x,q.y+.65,q.z],[.17,1.30,.17],q.yaw);for(const h of [.52,1.16])b.beam('wood',[q.x,q.y+h,q.z],[next.x,next.y+h,next.z],.13,.13)}}
  const stripe=(s0,s1,a,c)=>{const V=[];for(const s of [s0,s1]){const p=t.point(s);for(const d of [a,c])V.push([p.x+p.rightX*d,p.y+.106,p.z+p.rightZ*d])}m.geometry('white',V,[[0,2,1],[1,2,3]])};for(let s=8;s<t.length;s+=12)stripe(s,s+4,-.065,.065);for(let s=0;s<t.length;s+=3)for(const side of [-1,1])stripe(s,s+3,side*4.65,side*4.74);
  for(let i=0;i<78;i++){const p=this.locate((i+.35)/78,(i%2?-1:1)*(15+i%4*2.5),2.7,'rainforest-tree');if(p&&Math.abs(p.x-centre(p.z))>width(p.z)+9)this.forestTree(p,.95+i%4*.14)}
  for(let i=0;i<38;i++){const p=this.locate((i+.72)/38,(i%2?1:-1)*(38+i%4*9),3.4,'forest-backdrop');if(p&&Math.abs(p.x-centre(p.z))>width(p.z)+9)this.forestTree(p,1.25+i%3*.15)}
  for(let i=0;i<28;i++){const c=this.locate((i+.66)/28,(i%2?-1:1)*(64+i%4*15),10,'rainforest-grove');if(c)for(let j=0;j<4;j++){const a=j*2.4,x=c.x+Math.cos(a)*6,z=c.z+Math.sin(a)*6;if(r.clearance(x,z)>26&&Math.abs(x-centre(z))>width(z)+9&&this.landmarks.every(l=>Math.hypot(x-l.x,z-l.z)>l.radius+5)){const p={x,z,y:r.groundAt(x,z),yaw:a};this.forestTree(p,1.1+j*.1)}}}
  for(let i=0;i<24;i++){const p=this.locate((i+.4)/24,(i%2?-1:1)*11.9,1.5,'forest-fern');if(p)this.fern(p,i)}
  for(let i=0;i<18;i++){const p=this.locate((i+.6)/18,(i%2?1:-1)*13.7,1.8,'moss-rock');if(p)this.boulder(p,1.25+i%3*.3)}
  for(let i=0;i<10;i++){const p=this.locate((i+.45)/10,(i%2?-1:1)*10.4,.8,'trail-lamp');if(p&&Math.abs(p.x-centre(p.z))>width(p.z)+8)this.trailLamp(p)}
  for(let i=0;i<18;i++){const z=-160+i*15,x=centre(z)+(i%2?-1:1)*(width(z)-3),d=r.clearance(x,z);if(d>12.5&&z<90)b.bevel('rock',[x,-1.90,z],[2.7,3.2,2.15],i*.7,.32)}
  // Forest rim follows the raised river source, with low distant silhouettes in haze.
  for(let i=0;i<28;i++){const x=-75+i*9,z=158+(i%3)*13,p={x,z,y:r.groundAt(x,z),yaw:i*.6};if(r.clearance(x,z)>18)this.forestTree(p,1.15+i%3*.2)}
  this.batches=[...this.upload(b),...this.upload(f,true),...this.upload(m,true),...this.labels];this.stats={landmarks:this.landmarks,objects:this.objects,triangles:this.batches.reduce((n,o)=>n+o.p.count/3,0),colour_draw_calls:this.batches.length,shadow_draw_calls:this.batches.filter(o=>o.key!=='shadow').length,textures:this.textures.length,terrain_triangles:r.ground.count/3,static_visuals:true,landmark_accuracy_verified:false,waterfall_height:26.0,river_waterline:WATER,bridge_segments:this.bridgeCount()};
 }
 bridgeCount(){let n=0;for(let i=0;i<550;i++)if(bridge(this.track.point(i/550*this.track.length)))n++;return n}
 cascade(p){const b=this.batch;
  // Broad rock ledge and continuous curtain, not a thin tower or a named generic prop.
  const V=[],rings=[[0,42,-21,13],[12,38,-19,12],[26,34,-17,10]];for(const [y,w,front,back]of rings)for(const [x,z]of [[-w,front],[w,front],[w,back],[-w,back]])V.push(local(p,x,y,z));const F=[];for(let j=0;j<2;j++)for(let i=1;i<4;i++){const a=j*4+i,c=j*4+(i+1)%4,d=(j+1)*4+(i+1)%4,e=(j+1)*4+i;F.push([a,e,d],[a,d,c])}F.push([8,11,10],[8,10,9]);b.geometry('rock',V,F);
  for(let j=0;j<2;j++)for(let i=0;i<12;i++){const v=[];for(const k of [j,j+1])for(const a of [i/12,(i+1)/12]){const [y,w,front]=rings[k],z=front+.65*Math.sin(a*Math.PI)*Math.sin(a*8.0+k);v.push(local(p,-w+a*w*2,y,z))}b.geometry((i+j)%5===0?'rockdark':(i+j)%3===0?'rocklight':'rock',v,[[0,2,1],[1,2,3]])}
  for(const side of [-1,1]){for(const y of [7,15,22]){const w=side*(y>15?29:34),z=-21+y*4/26-.12;b.geometry('leaf',[local(p,w-3,y-.4,z),local(p,w+3,y+.5,z),local(p,w+2,y+2.2,z+.1),local(p,w-2,y+1.6,z+.1)],[[0,2,1],[0,3,2]])}this.boulder({x:p.x+side*28,y:25,z:130,yaw:side*.4},2.0)}
  const rows=[[-.42,-22.5],[7,-21.3],[17,-19.7],[26.08,-18.35]];
  for(let i=0;i<14;i++){const x=-16+i*32/14,x1=-16+(i+1)*32/14,V=[];for(const[y,z]of rows){V.push(local(p,x,y,z+.18*Math.sin(i)),local(p,x1,y,z+.18*Math.sin(i+1)))}const F=[];for(let j=0;j<3;j++)F.push([j*2,j*2+2,j*2+1],[j*2+1,j*2+2,j*2+3]);b.geometry(i%5===0?'fall':'cascadeWhite',V,F)}
  for(let i=0;i<9;i++){const x=-14+i*3.5,w=.22+(i%3)*.16,V=rows.map(([y,z])=>[local(p,x-w,y,z-.12),local(p,x+w,y,z-.12)]).flat(),F=[];for(let j=0;j<3;j++)F.push([j*2,j*2+2,j*2+1],[j*2+1,j*2+2,j*2+3]);b.geometry('cascadeWhite',V,F)}
  const WV=[local(p,-16,26.10,-18.35),local(p,16,26.10,-18.35),local(p,-14,26.10,28),local(p,14,26.10,28)];b.geometry('fall',WV,[[0,2,1],[1,2,3]]);
  // Foam patches lie on the plunge-pool surface; all are static and colour-batched.
  const foam=[local(p,0,-.48,-23)];for(let i=0;i<24;i++){const a=i/24*TAU,rad=1+.06*Math.sin(i*2.4);foam.push(local(p,Math.cos(a)*20*rad,-.48,-23+Math.sin(a)*4.2*rad))}this.pavement.geometry('white',foam,Array.from({length:24},(_,i)=>[0,(i+1)%24+1,i+1]));
  for(let i=0;i<7;i++)this.pavement.bevel('white',local(p,-15+i*5,-.30,-22-(i%2)*1.3),[.8,.35,.7],i*.5,.12);

  for(const side of [-1,1])for(let j=0;j<4;j++){const q={x:p.x+side*(28+j*4.0),z:p.z-18-j*2,y:rHeight(this.r,p.x+side*(28+j*4.0),p.z-18-j*2),yaw:j*.8};this.boulder(q,2.7+j*.3)}
 }
 overlook(p){const b=this.batch,box=(k,x,y,z,w,h,d)=>b.bevel(k,local(p,x,y,z),[w,h,d],p.yaw,.06);box('rock',0,.14,0,11,.30,9);box('wood',0,.34,0,10.3,.14,8.3);for(const x of [-5,5])for(const z of [-4,0,4])box('wood',x,.96,z,.20,1.25,.20);for(const x of [-5,5])for(const y of [.75,1.5])box('wood',x,y,0,.13,.13,8);for(const z of [-2,2]){box('wood',0,.90,z,4.8,.18,.7);for(const x of [-1.8,1.8])box('rock',x,.58,z,.25,.6,.4)}for(const x of [-2.7,2.7])box('wood',x,1,-3.7,.16,2,.16);box('wood',0,1.9,-3.7,6.5,1,.13);this.label(p,'RIAM MERASAP',6.2,.80,1.9,-3.61);this.pathToRoad(p)}
 pathToRoad(p){const q=nearest(this.r,p.x,p.z),dx=(q.p.x-p.x)/q.d,dz=(q.p.z-p.z)/q.d,len=q.d-7.8;if(len<5)return;const V=[],F=[];for(let i=0;i<=12;i++){const d=4.2+(len-4.2)*i/12;for(const side of [-1,1]){const x=p.x+dx*d+dz*side*1.35,z=p.z+dz*d-dx*side*1.35;V.push([x,this.r.groundAt(x,z)+.035,z])}if(i){const k=i*2;F.push([k-2,k,k-1],[k-1,k,k+1])}}this.pavement.geometry('sand',V,F)}
}
const rHeight=(r,x,z)=>r.groundAt(x,z);
const ground=RaceRenderer.prototype.groundAt;RaceRenderer.prototype.groundAt=function(x,z){if(this.track?.id!=='bengkayang')return ground.call(this,x,z);return this._bengkayangSurface?this._bengkayangSurface(x,z):sampled(x,z)};
const sky=RaceRenderer.prototype.skyPalette;RaceRenderer.prototype.skyPalette=function(){if(this.track?.id!=='bengkayang')return sky.call(this);const w=this.weather==='rain'?.55:this.weather==='fog'?.75:0;return{top:[.28,.61,.78].map((v,i)=>v*(1-w)+[.47,.58,.62][i]*w),horizon:[.76,.85,.80].map((v,i)=>v*(1-w)+[.72,.79,.78][i]*w)}};
const build=Base.prototype.build,draw=Base.prototype.draw;Base.prototype.build=function(track){if(this.bengkayang){this.bengkayang.release();this.bengkayang=null}this.r._bengkayangSurface=null;if(track.id!=='bengkayang')return build.call(this,track);for(const key of ['city','garden','coast','sambas','sintang','sentarum'])if(this[key]){this[key].release();this[key]=null}this.dispose();this.wildlife=[];this.ponds=[];this.landmarks=[];this.bengkayang=new WaterfallAdventure(this.r,track);this.batches=this.bengkayang.batches;this.landmarks=this.bengkayang.landmarks};Base.prototype.draw=function(time,pos){if(this.bengkayang){this.bengkayang.draw();return}return draw.call(this,time,pos)};
root.RaceBengkayangWaterfall=WaterfallAdventure;root.RaceBengkayangWaterfall.sampledLand=sampled;const config=JSON.parse(document.getElementById('stage6dTrack').textContent);if(RaceCore.STAGES.some(t=>t.id===config.id))throw Error('Stage Bengkayang already registered');RaceCore.STAGES.push(config);
})(globalThis);
