/* Stage 6A / Sambas. New procedural world; shared blocky geometry comes from
 * the accepted City/Garden helpers. Road physics, AI and clocks stay unchanged.
 * Palace is a stylized interpretation, not a verified architectural survey. */
(function(root){'use strict';
const Base=root.RaceScenery,Garden=root.RaceMempawahGarden,TAU=Math.PI*2;
const P={white:[.87,.87,.72],cream:[.78,.69,.43],teal:[.06,.34,.24],glass:[.035,.16,.15],metal:[.09,.18,.16],wood:[.34,.19,.075],roof:[.10,.30,.22],leaf:[.10,.34,.13],lime:[.34,.56,.17],pink:[.85,.18,.28],yellow:[.93,.64,.12],rock:[.39,.44,.38],sand:[.64,.61,.46],black:[.04,.065,.06],orange:[.64,.28,.09],lavender:[.58,.27,.58],water:[.035,.38,.49]};
const local=(p,x,y,z)=>[p.x+Math.cos(p.yaw)*x+Math.sin(p.yaw)*z,p.y+y,p.z-Math.sin(p.yaw)*x+Math.cos(p.yaw)*z];
const bank=z=>149+7*Math.sin(z*.014)+2*Math.sin(z*.039),riverWidth=62;
class RoyalRiver extends Garden{
 upload(batch,noShadow=false){const out=batch.upload(this.r);for(const m of out){m.p.material.color=P[m.key]||P.white;m.p.material.rough=m.key==='water'?.32:m.key==='yellow'?.69:.88;m.p.material.metal=m.key==='yellow'?.10:0;if(noShadow)m.key='shadow'}return out}
 anchor(x,z,yaw,radius,type){const clearance=this.r.clearance(x,z);if(clearance<radius+8.5)throw Error('Sambas: '+type+' terlalu dekat lintasan.');const p={x,z,y:this.r.groundAt(x,z),yaw,radius,type};this.objects.push({...p,clearance});this.landmarks.push(p);return p}
 onLand(p,radius=0){return p.x+radius<bank(p.z)-.5||p.x-radius>bank(p.z)+riverWidth+1}
 locate(u,lat,radius,type){const p=super.locate(u,lat,radius,type);if(p&&!this.onLand(p,radius)){this.objects.pop();return null}return p}
 replaceMesh(name,V,F,color,uv=null){const old=this.r[name];if(old)for(const k of ['pos','normal','uv','index'])if(old[k])this.r.gl.deleteBuffer(old[k]);this.r[name]=this.r.mesh(V,F,color,uv,null,true)}
 riverTerrain(){
  // A continuous bank/bed grid and one ribbon of water; no island edge or terrain holes.
  const V=[],F=[],water=[],wf=[],rows=80,cols=16;
  for(let i=0;i<=rows;i++){const z=-1000+i*25,x=bank(z),xs=[-1200,-400,-160,-80,0,60,95,x-12,x-2,x,x+2,x+riverWidth-2,x+riverWidth,x+riverWidth+3,x+riverWidth+70,1200];
   for(let j=0;j<cols;j++)V.push([xs[j],j===10||j===11?-3.3:j===9||j===12?-.60:-.50,z]);
   water.push([x+.55,-1.05,z],[x+riverWidth-.55,-1.05,z]);if(i){const a=(i-1)*cols;for(let j=0;j<cols-1;j++)F.push([a+j,a+j+cols,a+j+1],[a+j+1,a+j+cols,a+j+cols+1]);const k=i*2;wf.push([k-2,k,k-1],[k-1,k,k+1])}}
  this.replaceMesh('ground',V,F,[.23,.43,.20]);this.replaceMesh('water',water,wf,P.water);this.r.water.material.water=1;this.r.water.material.rough=.30;
 }
 build(){
  const r=this.r,t=this.track,b=this.batch,f=this.pavement,m=this.markings;this.plinth=new b.constructor();
  r.road.material.texture=r.roadTexture;r.road.material.color=[.80,.83,.81];r.road.material.rough=.93;r.shoulders.material.texture=null;r.shoulders.material.color=[.28,.46,.22];r.curbs.forEach((p,i)=>p.material.color=i?P.yellow:P.white);r.static=r.static.filter(x=>x.file==='prop_start_gate.glb');r.staticShadows.count=0;this.riverTerrain();
  const palace=this.anchor(17,67,-Math.PI*.88,25,'istana-alwatzikhoebillah');this.palace(palace);this.connectPromenade(palace,18,62,4.4);
  const dock={x:bank(40)-1,y:-.5,z:40,yaw:Math.PI/2,type:'dermaga-sungai',radius:11};this.landmarks.push(dock);this.dock(dock);
  const bridge={x:bank(-141)+riverWidth/2,y:-.5,z:-141,yaw:Math.PI/2,type:'jembatan-wisata',radius:riverWidth/2+7};this.landmarks.push(bridge);this.bridge(bridge);
  // Sidewalk surface matches the full existing road envelope and road height.
  for(const side of [-1,1]){const V=[],F=[],wall=[],W=[];for(let i=0;i<=550;i++){const p=t.point(i/550*t.length);for(const d of [5.55,7.65])V.push([p.x+p.rightX*side*d,p.y+.15,p.z+p.rightZ*side*d]);const x=p.x+p.rightX*side*7.65,z=p.z+p.rightZ*side*7.65;wall.push([x,r.groundAt(x,z)-.035,z],[x,p.y+.15,z]);if(i){const k=i*2;F.push([k-2,k,k-1],[k-1,k,k+1]);W.push([k-2,k,k-1],[k-1,k,k+1])}}f.geometry('sand',V,F);f.geometry('rock',wall,W)}
  const stripe=(s0,s1,a,c,key='white')=>{const V=[];for(const s of [s0,s1]){const p=t.point(s);for(const d of [a,c])V.push([p.x+p.rightX*d,p.y+.106,p.z+p.rightZ*d])}m.geometry(key,V,[[0,2,1],[1,2,3]])};
  for(let s=6;s<t.length;s+=11)stripe(s,s+4,-.07,.07);for(let s=0;s<t.length;s+=3)for(const side of [-1,1])stripe(s,s+3,side*4.65,side*4.74);
  for(const u of [.025,.34,.59])for(let j=-4;j<=4;j++)stripe(t.length*u-1,t.length*u+1,j*.92-.25,j*.92+.25);
  for(let i=0;i<26;i++){const p=this.locate((i+.4)/26,(i%2?1:-1)*9.8,.55,'lampu-jalan');if(p)this.lantern(p,i%3===0)}
  for(let i=0;i<32;i++){const p=this.locate((i+.3)/32,(i%2?1:-1)*(13.8+i%3),2.3,'pohon-kota');if(p)this.tree(p,.94+i%3*.10)}
  for(let i=0;i<16;i++){const p=this.locate((i+.7)/16,(i%2?-1:1)*22,3.5,'kelapa');if(p)this.palm(p,.90+i%2*.12)}
  for(let i=0;i<23;i++){const p=this.locate((i+.2)/23,(i%2?-1:1)*11.3,1.8,'taman-bunga');if(p)this.bed(p,2.9,1.4,i)}
  for(let i=0;i<13;i++){const p=this.locate((i+.5)/13,(i%2?-1:1)*30,6,'rumah-melayu');if(p&&!this.landmarks.some(l=>Math.hypot(p.x-l.x,p.z-l.z)<l.radius+8))this.house(p,i)}
  this.riverfront();
  for(const u of [.51,.60]){const q=t.point(u*t.length);for(let x=q.x+7.8;x<bank(q.z)-5.4;x+=2.0){const V=[[x,q.z-1.6],[x+2,q.z-1.6],[x+2,q.z+1.6],[x,q.z+1.6]].map(([xx,z])=>[xx,r.groundAt(xx,z)+.17,z]);if(V.every(v=>r.clearance(v[0],v[2])>7.55))f.geometry('sand',V,[[0,2,1],[0,3,2]])}}
  // Warm timber obstacle details remain purely decorative; real features are engine-owned.
  for(const u of [.13,.38,.62,.81]){const p=t.place(u*t.length,8.2);this.guardrail(p,9)}
  this.label({...palace,y:palace.y},'ISTANA ALWATZIKHOEBILLAH\nSAMBAS',7.0,.95,.95,16.8);
  this.batches=[...this.upload(b),...this.upload(f,true),...this.upload(this.plinth,true),...this.upload(m,true),...this.labels];
  this.stats={landmarks:this.landmarks.map(x=>({...x})),objects:this.objects,triangles:this.batches.reduce((n,x)=>n+x.p.count/3,0),colour_draw_calls:this.batches.length,shadow_draw_calls:this.batches.filter(x=>x.key!=='shadow').length,textures:this.textures.length,static_visuals:true,river_mesh_triangles:r.water.count/3,terrain_triangles:r.ground.count/3,palace_verified_reconstruction:false};
 }
 palace(p){
  const b=this.batch,f=this.pavement,box=(k,x,y,z,w,h,d,v=.08)=>b.bevel(k,local(p,x,y,z),[w,h,d],p.yaw,v),beam=(k,a,c,w,d=w)=>b.beam(k,local(p,...a),local(p,...c),w,d);
  f.bevel('sand',local(p,0,.03,1),[40,.20,34],p.yaw,.2);f.bevel('cream',local(p,0,.15,11.0),[24,.12,9],p.yaw,.1);f.bevel('white',local(p,0,.23,12),[5,.04,8],p.yaw,.01);
  // Broad raised timber hall, central projecting entrance, low side wings.
  for(const x of [-13,-8,-3,3,8,13])for(const z of [-5,0,5])box('wood',x,.65,z,.36,1.35,.36,.04);
  box('wood',0,1.35,0,29,.36,13);box('yellow',0,3.40,0,28.2,3.75,12.0,.12);box('cream',0,5.34,0,28.5,.19,12.4,.04);this.hipRoof(p,0,5.45,0,31.5,15,3.8,'roof');
  for(const side of [-1,1]){box('wood',side*17.0,.72,2,7.2,1.45,11);box('yellow',side*17.0,2.77,2,7.0,2.8,10.8);this.hipRoof(p,side*17.0,4.27,2,8.5,12.3,2.2,'roof');for(const z of [-1,3,6]){box('cream',side*20.55,2.85,z,.12,1.8,1.3);box('teal',side*20.63,2.85,z,.045,1.58,1.1)}}
  for(const x of [-11,-7.4,-3.8,3.8,7.4,11]){box('cream',x,3.50,6.06,1.8,2.1,.13);box('teal',x,3.50,6.15,1.54,1.85,.045);for(const dx of [-.34,.34])box('glass',x+dx,3.73,6.184,.48,1.08,.025);box('yellow',x,3.50,6.21,.10,1.85,.025)}
  // Entrance roof has an independent long ridge, not the Mempawah two-tier pediment.
  box('wood',0,1.35,9,10.4,.34,7.4);for(const x of [-4.3,4.3])for(const z of [6.4,11.9]){box('yellow',x,3.13,z,.30,3.3,.30,.04);box('teal',x,1.77,z,.48,.32,.48,.04);box('cream',x,4.66,z,.47,.28,.47,.04)}
  this.hipRoof(p,0,4.88,9,12,8.9,2.45,'roof');box('cream',0,4.68,12.6,9.7,.20,.24,.04);box('teal',0,3.06,6.17,2.5,3.07,.12);box('glass',0,3.22,6.26,2.15,2.72,.05);box('yellow',0,3.15,6.31,.08,2.7,.025);
  for(const side of [-1,1]){for(let i=0;i<6;i++){const x=side*(2.3+i*.34);box('yellow',x,2.0,12,.10,.95,.10,.02)}beam('teal',[side*2.1,2.5,12],[side*4.4,2.5,12],.12);beam('cream',[side*2.1,1.57,12],[side*4.4,1.57,12],.10)}
  for(let i=0;i<6;i++)box(i%2?'cream':'white',0,.10+(6-i)*.11,12.6+i*.47,3.5,(6-i)*.22,.53,.025);
  for(const side of [-1,1]){const q={...p,x:local(p,side*14,.0,12.5)[0],z:local(p,side*14,0,12.5)[2]};this.bed(q,6.5,1.9,side>0?0:2);this.palm({...p,x:local(p,side*22,0,-7)[0],z:local(p,side*22,0,-7)[2]},1.08)}
  for(const side of [-1,1]){const rail={...p,x:local(p,side*12,0,17)[0],z:local(p,side*12,0,17)[2],yaw:p.yaw+Math.PI/2};this.guardrail(rail,14)}
  // Diamond panels are original graphic trim; no unverified royal emblem/calligraphy.
  for(const x of [-8,-5,5,8]){const V=[local(p,x-.25,5.02,6.28),local(p,x,5.28,6.28),local(p,x+.25,5.02,6.28),local(p,x,4.76,6.28)];b.geometry('teal',V,[[0,1,2],[0,2,3]])}
 }
 house(p,i){const b=this.batch,box=(k,x,y,z,w,h,d)=>b.bevel(k,local(p,x,y,z),[w,h,d],p.yaw,.08);for(const x of [-2.6,2.6])for(const z of [-2,2])box('wood',x,.5,z,.22,1.1,.22);box('wood',0,1.12,0,6.4,.22,5.5);box(i%2?'cream':'yellow',0,2.6,0,6.0,2.8,5.0);this.hipRoof(p,0,4.08,0,7.4,6.4,1.8,'roof');for(const x of [-1.8,1.8]){box('white',x,2.65,2.54,1.1,1.4,.1);box('teal',x,2.65,2.61,.91,1.2,.04)}box('teal',0,2.3,2.55,1.1,2.25,.1);for(let j=0;j<3;j++)box('wood',0,.10+(3-j)*.12,3+j*.42,1.5,(3-j)*.24,.46)}
 guardrail(p,length){const b=this.batch;for(const z of [-length/2,0,length/2])b.bevel('rock',local(p,0,.60,z),[.24,1.2,.24],p.yaw,.04);for(const y of [.65,1.12])b.beam('white',local(p,0,y,-length/2),local(p,0,y,length/2),.10);for(const z of [-length/2,length/2])b.box('yellow',local(p,0,1.28,z),[.32,.18,.32],p.yaw)}
 riverfront(){const b=this.batch,f=this.pavement;
  for(let z=-103;z<114;z+=5){const x=bank(z)-3.6,p={x,y:-.5,z,yaw:Math.PI/2};f.bevel('sand',local(p,0,.14,0),[5.0,.25,3.9],p.yaw,.06);for(const dz of [-2.5]){b.box('rock',[x+2.0,.15,z+dz],[.26,1.3,.26]);b.box('yellow',[x+2,.85,z+dz],[.36,.12,.36])}for(const y of [.08,.58])b.beam('teal',[x+2,y,z-2.5],[x+2,y,z+2.5],.10)}
  for(let i=0;i<8;i++){const z=-90+i*27,x=bank(z)-9;this.palm({x,y:-.5,z,yaw:0},.95+i%2*.12);if(i%2)this.lantern({x:x+4,y:-.5,z:z+8,yaw:0},true)}
  for(let i=0;i<10;i++){const z=-190+i*43,x=bank(z)+riverWidth+18+i%3*9;this.tree({x,y:-.5,z,yaw:i*.7},1.2)}
  for(const z of [-55,83])this.boat({x:bank(z)+22,y:-1.05,z,yaw:.18+(z>0?.3:0)});
 }
 dock(p){const b=this.batch;for(let i=0;i<8;i++)b.bevel(i%2?'cream':'wood',local(p,0,.45,1+i*1.7),[5.0,.22,1.66],p.yaw,.03);for(const x of [-2.1,2.1])for(const z of [1,6,12.6])b.box('wood',local(p,x,-.12,z),[.28,2.2,.28],p.yaw);for(const x of [-2.15,2.15])for(const z of [7.9,12.6])b.box('yellow',local(p,x,2.0,z),[.19,3.0,.19],p.yaw);this.hipRoof(p,0,3.55,10.1,6.0,6.2,1.6,'roof');for(const x of [-2.1,2.1])for(const y of [1.0,1.55])b.beam('teal',local(p,x,y,1),local(p,x,y,7.3),.08)}
 bridge(p){const b=this.batch;for(let i=0;i<17;i++){const z=-38+i*4.75,y=.5+1.1*Math.cos(z/38*Math.PI/2);b.bevel(i%2?'wood':'cream',local(p,0,y,z),[4.8,.3,4.78],p.yaw,.04);for(const x of [-2.2,2.2]){b.box('wood',local(p,x,-.25,z),[.33,4.0,.33],p.yaw);b.box('yellow',local(p,x,y+.72,z),[.23,1.55,.23],p.yaw);if(i<16){const zz=z+4.75,yy=.5+1.1*Math.cos(zz/38*Math.PI/2);b.beam('teal',local(p,x,y+1.42,z),local(p,x,yy+1.42,zz),.12)}}}}
 boat(p){const b=this.batch,V=[[-1.1,.15,-3],[1.1,.15,-3],[1.2,.15,2.0],[0,.45,3.7],[-1.2,.15,2.0],[-.55,-.18,-2.5],[.55,-.18,-2.5],[.55,-.18,1.5],[-.55,-.18,1.5]],F=[[0,1,6],[0,6,5],[1,2,7],[1,7,6],[2,3,7],[3,4,8],[3,8,7],[4,0,5],[4,5,8],[5,6,7],[5,7,8]];b.geometry('wood',V.map(v=>local(p,...v)),F);b.bevel('cream',local(p,0,.19,0),[1.7,.16,3.4],p.yaw,.04);b.bevel('yellow',local(p,0,.9,-.6),[1.9,.12,2.3],p.yaw,.05);for(const x of [-.75,.75])for(const z of [-1.5,.3])b.box('wood',local(p,x,.56,z),[.08,.75,.08],p.yaw)}
}
const build=Base.prototype.build,draw=Base.prototype.draw;
Base.prototype.build=function(track){if(this.sambas){this.sambas.release();this.sambas=null}if(track.id!=='sambas')return build.call(this,track);for(const key of ['city','garden','coast'])if(this[key]){this[key].release();this[key]=null}this.dispose();this.wildlife=[];this.ponds=[];this.landmarks=[];this.sambas=new RoyalRiver(this.r,track);this.batches=this.sambas.batches;this.landmarks=this.sambas.landmarks};
Base.prototype.draw=function(time,pos){if(this.sambas){this.sambas.draw();return}return draw.call(this,time,pos)};
root.RaceSambasRiver=RoyalRiver;root.RaceSambasRiver.bankX=bank;
const config=JSON.parse(document.getElementById('stage6aTrack').textContent);if(RaceCore.STAGES.some(x=>x.id===config.id))throw Error('Stage Sambas sudah terdaftar.');RaceCore.STAGES.push(config);
})(globalThis);
