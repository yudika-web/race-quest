/* Stage 2 presentation only. Reuse the accepted Stage 1 batch/texture helpers;
   never modify physics, weather, collision, actor assets, or animation clocks. */
(function(root){'use strict';
const Base=root.RaceScenery,City=root.RacePontianakCity,TAU=Math.PI*2;
const P={white:[.84,.85,.70],cream:[.70,.62,.40],teal:[.12,.49,.37],glass:[.055,.17,.16],metal:[.055,.16,.13],wood:[.30,.17,.065],roof:[.43,.105,.065],leaf:[.105,.34,.12],lime:[.31,.56,.14],pink:[.83,.12,.30],yellow:[.89,.57,.105],rock:[.27,.34,.28],sand:[.60,.56,.40],black:[.045,.065,.05],orange:[.73,.17,.075],lavender:[.56,.23,.62]};
const local=(p,x,y,z)=>[p.x+Math.cos(p.yaw)*x+Math.sin(p.yaw)*z,p.y+y,p.z-Math.sin(p.yaw)*x+Math.cos(p.yaw)*z];
class Garden extends City{
 upload(batch,noShadow=false){const out=batch.upload(this.r);for(const m of out){m.p.material.color=P[m.key]||P.white;m.p.material.rough=m.key==='yellow'?.64:.88;m.p.material.metal=m.key==='yellow'?.22:0;if(noShadow)m.key='shadow'}return out}
 gap(s,margin=0){const u=RaceCore.mod(s,this.track.length)/this.track.length;return this.track.config.gaps.some(g=>Math.abs(u-g.u)*this.track.length<g.length/2+margin)}
 build(){
  const r=this.r,t=this.track,b=this.batch,flat=this.pavement,m=this.markings;
  const asphalt=document.createElement('canvas');asphalt.width=asphalt.height=128;const a=asphalt.getContext('2d');a.fillStyle='#46524e';a.fillRect(0,0,128,128);const rnd=RaceCore.seedRandom(47114);for(let i=0;i<450;i++){a.fillStyle=i%2?'#4b5750':'#424f4b';a.fillRect(rnd()*128,rnd()*128,1,1)}
  r.road.material.texture=this.texture(asphalt);r.road.material.color=[.84,.88,.85];r.road.material.rough=.88;r.ground.material.texture=null;r.ground.material.color=[.18,.39,.17];r.shoulders.material.texture=null;r.shoulders.material.color=[.24,.45,.20];r.curbs.forEach((p,i)=>p.material.color=i?[.72,.13,.075]:[.85,.86,.77]);
  // Generic rural props are decoration only. Actual obstacle/ramp meshes are untouched.
  r.static=r.static.filter(o=>o.file==='prop_start_gate.glb');r.staticShadows.count=0;
  const farmer=this.locate(.16,-24,9.5,'tugu-pak-tani');if(farmer)this.landmarks.push({...farmer,type:'tugu-pak-tani',radius:9.5});
  const palace=this.locate(.425,42,20,'keraton-mempawah');if(palace)this.landmarks.push({...palace,type:'keraton-mempawah',radius:20});
  if(!farmer||!palace)throw Error('Landmark taman tidak mempunyai ruang aman di luar lintasan.');
  // Promenade follows the original elevation; gaps stay visibly open, including markings.
  for(const side of [-1,1]){const v=[],f=[],wall=[],wf=[];for(let i=0;i<=550;i++){const p=t.point(i/550*t.length);for(const d of [5.55,7.95])v.push([p.x+p.rightX*side*d,p.y+.155,p.z+p.rightZ*side*d]);const x=p.x+p.rightX*side*7.95,z=p.z+p.rightZ*side*7.95;wall.push([x,r.groundAt(x,z)-.03,z],[x,p.y+.155,z]);if(i&&!this.gap((i-.5)/550*t.length,t.length/1100)){const k=i*2;f.push([k-2,k,k-1],[k-1,k,k+1]);wf.push([k-2,k,k-1],[k-1,k,k+1])}}flat.geometry('sand',v,f);flat.geometry('rock',wall,wf)}
  const stripe=(s0,s1,d0,d1)=>{if(this.gap((s0+s1)/2,Math.abs(s1-s0)/2))return;const v=[];for(const s of [s0,s1]){const p=t.point(s);for(const d of [d0,d1])v.push([p.x+p.rightX*d,p.y+.104,p.z+p.rightZ*d])}m.geometry('white',v,[[0,2,1],[1,2,3]])};
  for(let s=8;s<t.length;s+=11)stripe(s,s+4,-.065,.065);for(let s=0;s<t.length;s+=2)for(const side of [-1,1])stripe(s,s+2,side*4.68,side*4.76);
  for(const u of [.115,.39,.82])for(let i=-4;i<=4;i++)stripe(u*t.length-1,u*t.length+1,i*.91-.25,i*.91+.25);
  for(let i=0;i<28;i++){const p=this.locate((i+.40)/28,(i%2?1:-1)*9.05,.42,'garden-lantern');if(p)this.lantern(p,i%4===0)}
  for(let i=0;i<54;i++){const p=this.locate((i+.31)/54,(i%2?-1:1)*(12.6+i%3),2.5,'garden-tree');if(p)this.tree(p,1+i%3*.12)}
  for(let i=0;i<18;i++){const p=this.locate((i+.6)/18,(i%2?-1:1)*22,3.8,'palm');if(p)this.palm(p,1+i%2*.13)}
  for(let i=0;i<60;i++){const p=this.locate((i+.74)/60,(i%2?1:-1)*10.8,1.65,'flower-bed');if(p)this.bed(p,2.8,1.4,i)}
  for(let i=0;i<30;i++){const p=this.locate((i+.3)/30,(i%2?-1:1)*18,2.1,'garden-shrub');if(p){b.bevel('leaf',local(p,0,.55,0),[3.4,1.1,1.8],p.yaw,.24);b.bevel('lime',local(p,-.7,.97,0),[1.65,.6,1.4],p.yaw,.20)}}
  for(const [u,side]of [[.055,-1],[.54,-1],[.85,1]]){const p=this.locate(u,side*24,5.1,'gazebo');if(p)this.gazebo(p)}
  // Short white/teal garden fences, never placed on the ramp/gap or in the driving width.
  for(let i=0;i<22;i++){const s=(i+.4)/22*t.length;if(this.gap(s,9)||Math.abs(s/t.length-.675)<.025)continue;const side=i%2?1:-1;for(let j=0;j<4;j++){const q=t.place(s+j*1.6,side*8.35);if(this.landmarks.some(p=>Math.hypot(p.x-q.x,p.z-q.z)<p.radius+1))continue;const p={...q,y:q.y+.15};b.bevel('white',local(p,0,.48,0),[.24,.95,.24],p.yaw,.035);b.bevel('yellow',local(p,0,1.01,0),[.28,.13,.28],p.yaw,.035);if(j<3){const end=t.place(s+(j+1)*1.6,side*8.35);for(const y of [.35,.77])b.beam(y>.5?'teal':'white',local(p,0,y,0),[end.x,end.y+.15+y,end.z],.095,.10)}}}
  this.plinth=new this.batch.constructor();this.farmerPlaza(farmer);this.farmer(farmer);this.connectPromenade(farmer,9.5,28,2.8);this.label(farmer,'TUGU PAK TANI\nMEMPAWAH',4.8,1.0,1.63,2.42);
  this.palace(palace);this.connectPromenade(palace,14.5,46,3.2);const sign={...palace,x:local(palace,-7.6,0,11.75)[0],z:local(palace,-7.6,0,11.75)[2]};this.plinth.bevel('white',local(sign,0,.48,0),[7.6,.96,.28],sign.yaw,.08);this.label(sign,'KERATON MEMPAWAH\nAMANTUBILLAH',7.3,.80,.52,.16);
  this.batches=[...this.upload(b),...this.upload(flat,true),...this.upload(this.plinth,true),...this.upload(m,true),...this.labels];
  this.stats={landmarks:this.landmarks.map(p=>({type:p.type,x:p.x,y:p.y,z:p.z,yaw:p.yaw,radius:p.radius})),objects:this.objects,triangles:this.batches.reduce((n,o)=>n+o.p.count/3,0),colour_draw_calls:this.batches.length,shadow_draw_calls:this.batches.filter(o=>o.key!=='shadow').length,textures:this.textures.length,static_visuals:true,gap_left_open:true};
 }

 connectPromenade(p,start,end,width){
  const f=this.pavement;for(let z=start;z<end;z+=1.6){const v=[];for(const zz of [z,z+1.6])for(const x of [-width/2,width/2]){const q=local(p,x,0,zz);q[1]=this.r.groundAt(q[0],q[2])+.16;v.push(q)}if(v.some(q=>this.r.clearance(q[0],q[2])<8.20))break;f.geometry('sand',v,[[0,2,1],[1,2,3]]);if(Math.round((z-start)/1.6)%3===1)for(const side of [-1,1]){const q=local(p,side*(width/2+1.1),0,z+.8);if(this.r.clearance(q[0],q[2])>11.0)this.bed({...p,x:q[0],y:this.r.groundAt(q[0],q[2]),z:q[2]},1.3,1.0,Math.round(z)%3)}}
 }

 tree(p,s){const b=this.batch;b.bevel('rock',local(p,0,.12,0),[1.0,.24,1.0],p.yaw,.08);b.bevel('wood',local(p,0,1.85*s,0),[.44,3.7*s,.44],p.yaw,.07);b.beam('wood',local(p,0,2.1*s,0),local(p,-1.05*s,3.5*s,.15),.23);b.bevel('leaf',local(p,0,4.15*s,0),[3.7*s,2.8*s,3.2*s],p.yaw,.51);b.bevel('lime',local(p,-.72*s,5.10*s,.1),[2.5*s,1.65*s,2.5*s],p.yaw+.2,.4);b.bevel('leaf',local(p,1.35*s,3.75*s,.2),[1.8*s,1.7*s,2.1*s],p.yaw,.34)}
 palm(p,s){const b=this.batch;b.bevel('wood',local(p,0,3.6*s,0),[.43,7.2*s,.43],p.yaw,.06);for(let i=1;i<7;i++)b.box('cream',local(p,0,i*s,0),[.45,.07,.45],p.yaw);for(let i=0;i<6;i++){const a=i/6*TAU,q=(rad,y)=>local(p,Math.cos(a)*rad*s,y*s,Math.sin(a)*rad*s);b.beam(i%2?'leaf':'lime',q(0,7.1),q(1.05,8.15),.32,.55);b.beam(i%2?'leaf':'lime',q(1.05,8.15),q(2.45,7.95),.35,.64);b.beam(i%2?'leaf':'lime',q(2.45,7.95),q(3.2,6.85),.24,.45)}}
 flower(p,x,y,z,key,scale=1){const b=this.pavement;for(const [dx,dz]of [[-.16,0],[.16,0],[0,-.16],[0,.16]]){const v=[[-.15,-.15],[.15,-.15],[.15,.15],[-.15,.15]].map(([xx,zz])=>local(p,x+(xx+dx)*scale,y,z+(zz+dz)*scale));b.geometry(key,v,[[0,2,1],[0,3,2]])}const v=[[-.09,-.09],[.09,-.09],[.09,.09],[-.09,.09]].map(([xx,zz])=>local(p,x+xx*scale,y+.008,z+zz*scale));b.geometry('yellow',v,[[0,2,1],[0,3,2]])}
 bed(p,w,d,index){const b=this.batch;b.bevel('white',local(p,0,.12,0),[w+.20,.24,d+.20],p.yaw,.10);b.bevel('leaf',local(p,0,.36,0),[w,.44,d],p.yaw,.20);for(let i=0;i<6;i++)this.flower(p,(i%3-1)*w*.30,.61,(Math.floor(i/3)-.5)*d*.48,['pink','white','lavender'][index%3],.88)}
 lantern(p,banner){const b=this.batch;b.bevel('rock',local(p,0,.12,0),[.60,.24,.60],p.yaw,.06);b.bevel('metal',local(p,0,2.05,0),[.14,4.1,.14],p.yaw,.025);b.bevel('yellow',local(p,0,4.0,0),[.30,.16,.30],p.yaw,.035);b.bevel('cream',local(p,0,4.34,0),[.44,.62,.44],p.yaw,.07);for(const x of [-.24,.24])for(const z of [-.24,.24])b.box('metal',local(p,x,4.34,z),[.045,.66,.045],p.yaw);this.hipRoof(p,0,4.70,0,.73,.73,.42,'teal');if(banner){b.beam('metal',local(p,0,3.88,0),local(p,.95,3.88,0),.065);b.box('yellow',local(p,.69,3.17,0),[.60,1.35,.045],p.yaw);b.box('teal',local(p,.69,3.17,.035),[.27,.46,.025],p.yaw)}}
 hipRoof(p,x,y,z,w,d,h,key='roof'){
  const b=this.batch,ridge=w*.24,raw=[[-w/2,0,-d/2],[w/2,0,-d/2],[w/2,0,d/2],[-w/2,0,d/2],[-ridge,h,0],[ridge,h,0]],faces=[[0,4,5,1],[1,5,2],[2,5,4,3],[3,4,0]],v=[],f=[];for(const face of faces){const k=v.length;v.push(...face.map(i=>local(p,x+raw[i][0],y+raw[i][1],z+raw[i][2])));for(let i=1;i<face.length-1;i++)f.push([k,k+i,k+i+1])}b.geometry(key,v,f);
  for(const t of [.02,.32,.64]){const halfW=w/2-(w/2-ridge)*t,halfD=d/2*(1-t),yy=y+h*t+.025;for(const side of [-1,1]){b.beam(t<.1?'yellow':key,local(p,x-halfW,yy,z+side*halfD),local(p,x+halfW,yy,z+side*halfD),.065);b.beam(t<.1?'yellow':key,local(p,x+side*halfW,yy,z-halfD),local(p,x+side*halfW,yy,z+halfD),.065)}}b.beam('yellow',local(p,x-ridge,y+h+.04,z),local(p,x+ridge,y+h+.04,z),.10);
 }
 gazebo(p){const b=this.batch;b.bevel('sand',local(p,0,.2,0),[5.1,.4,5.1],p.yaw,.13);for(const x of [-2.05,2.05])for(const z of [-2.05,2.05]){b.bevel('teal',local(p,x,1.95,z),[.22,3.5,.22],p.yaw,.035);b.box('yellow',local(p,x,.54,z),[.32,.20,.32],p.yaw);b.box('yellow',local(p,x,3.45,z),[.33,.22,.33],p.yaw)}this.hipRoof(p,0,3.65,0,5.8,5.8,1.6);for(const z of [-2.0,1.6])b.bevel('wood',local(p,0,.88,z),[3.5,.20,.65],p.yaw,.06);for(const side of [-1,1]){for(const h of [.88,1.45])b.beam('white',local(p,side*2.05,h,-2.05),local(p,side*2.05,h,2.05),.10);for(const z of [-1.3,0,1.3])b.box('teal',local(p,side*2.05,1.16,z),[.10,.55,.10],p.yaw)}}
 farmerPlaza(p){const b=this.batch,f=this.pavement;b.cylinder('rock',[p.x,p.y+.02,p.z],9.5,.15,32);f.cylinder('sand',[p.x,p.y+.18,p.z],9.15,.08,32);f.ring('white',[p.x,p.y+.268,p.z],8.2,.16,'XZ',40);for(let i=0;i<8;i++){const a=i/8*TAU,q={...p,x:p.x+Math.cos(a)*7.3,z:p.z+Math.sin(a)*7.3,yaw:p.yaw+a};if(i%2)this.bed(q,2.9,1.3,i);else{b.bevel('wood',local(q,0,.63,0),[2.5,.20,.66],q.yaw,.08);for(const x of [-.88,.88])b.box('metal',local(q,x,.35,0),[.12,.55,.42],q.yaw)}}}
 farmer(p){const b=this.batch;const box=(key,x,y,z,w,h,d,bevel=.08)=>(y<3.3?this.plinth:b).bevel(key,local(p,x,y,z),[w,h,d],p.yaw,bevel),beam=(key,a,c,w,d=w)=>b.beam(key,local(p,...a),local(p,...c),w,d);
  box('white',0,.44,0,6.0,.40,5.8);box('teal',0,.78,0,5.2,.28,5.0);box('cream',0,1.84,0,4.4,1.9,4.4);box('teal',0,1.78,2.23,3.8,1.6,.08);box('yellow',0,2.91,0,4.8,.24,4.8);box('orange',0,3.11,0,4.45,.18,4.45);
  for(const side of [-1,1]){box('yellow',side*.93,3.37,.18,.70,.32,1.0);beam('yellow',[side*.93,3.53,0],[side*.64,4.62,0],.50,.60);beam('yellow',[side*.64,4.62,0],[side*.38,5.80,0],.57,.64)}
  box('yellow',0,5.90,0,1.31,.72,.77);box('yellow',0,7.00,0,1.5,1.65,.86,.14);box('wood',0,6.14,0,1.48,.11,.89,.025);box('yellow',0,8.02,0,.39,.47,.43);box('yellow',0,8.70,.02,.97,1.04,.85,.15);box('yellow',0,8.67,.49,.22,.24,.19,.04);
  for(const x of [-.22,.22])box('wood',x,8.86,.451,.085,.07,.018,.01);beam('cream',[-.20,8.40,.46],[.19,8.40,.46],.035);for(const y of [6.55,6.85,7.15])box('cream',.08,y,.45,.06,.06,.04,.01);beam('cream',[0,6.25,.447],[0,7.65,.447],.035);
  b.cylinder('yellow',local(p,0,9.17,0),.93,.13,8);b.cylinder('yellow',local(p,0,9.29,0),.70,.57,8,.10);
  beam('yellow',[-.72,7.62,0],[-1.18,6.94,.02],.45,.50);beam('yellow',[-1.18,6.94,.02],[-1.57,6.63,.29],.38,.43);box('yellow',-1.57,6.59,.3,.44,.42,.45);
  beam('yellow',[.71,7.61,0],[1.09,7.80,0],.44,.48);beam('yellow',[1.09,7.80,0],[1.22,8.96,.10],.37,.42);box('yellow',1.23,9.04,.1,.43,.41,.45);
  beam('wood',[-2.12,3.31,.43],[-1.44,7.23,.28],.12);box('yellow',-1.76,7.27,.38,1.0,.18,.66,.035);
  box('yellow',1.72,8.17,.12,1.12,1.12,.69,.20);box('cream',1.72,8.36,.12,1.16,.10,.72,.025);for(let i=0;i<5;i++){const x=1.36+i*.17;beam('yellow',[1.72,8.32,.12],[x,9.02+(i%2)*.16,.12],.07);box('cream',x,9.03+(i%2)*.16,.12,.15,.28,.16,.04)}
 }
 palace(p){const b=this.batch,f=this.pavement,box=(key,x,y,z,w,h,d,bevel=.08)=>b.bevel(key,local(p,x,y,z),[w,h,d],p.yaw,bevel),beam=(key,a,c,w,d=w)=>b.beam(key,local(p,...a),local(p,...c),w,d);
  f.bevel('sand',local(p,0,.12,2),[30,.24,25],p.yaw,.2);box('rock',0,.66,0,19.0,1.0,11.3);box('white',0,1.29,.75,19.5,.26,13.0);box('teal',0,3.63,0,17.8,4.40,9.6,.12);box('white',0,5.93,0,18.0,.20,9.9);box('cream',0,1.69,4.86,17.7,.30,.13);
  for(const side of [-1,1]){box('rock',side*11.1,.60,-.25,4.8,.90,8.2);box('teal',side*11.1,2.81,-.25,4.8,3.5,8.0);box('white',side*11.1,4.62,-.25,4.95,.16,8.1);this.hipRoof(p,side*11.1,4.74,-.25,5.6,8.9,1.65);for(const z of [-2.3,.8]){box('yellow',side*13.55,2.95,z,.10,1.85,1.3);box('glass',side*13.61,2.95,z,.03,1.57,1.02)}}
  for(const x of [-7.3,-5.0,-2.8,2.8,5.0,7.3]){box('white',x,3.63,4.85,1.33,2.0,.12);box('glass',x,3.63,4.93,1.08,1.73,.045);box('yellow',x,3.63,4.97,.06,1.76,.04);box('yellow',x,3.63,4.97,1.10,.07,.04)}
  box('yellow',0,3.20,4.89,2.20,3.36,.15);box('glass',0,3.20,4.99,1.88,3.08,.05);for(const side of [-1,1]){box('teal',side*.47,3.12,5.03,.78,2.82,.05);box('yellow',side*.18,3.16,5.075,.06,.20,.045)}
  this.hipRoof(p,0,6.06,0,20.2,12.0,3.10);this.hipRoof(p,0,8.58,0,11.7,6.0,1.95);b.cylinder('yellow',local(p,0,10.53,0),.13,.9,8,.035);box('yellow',0,11.43,0,.22,.22,.22,.04);
  for(const x of [-5.4,-2.6,2.6,5.4]){box('teal',x,3.40,6.35,.24,3.95,.24,.04);box('yellow',x,1.72,6.35,.39,.25,.39,.045);box('yellow',x,5.14,6.35,.39,.30,.39,.045)}
  box('yellow',0,5.35,6.25,11.6,.20,.38,.04);
  // Front pediment and pitched veranda roof: gold zigzag trim instead of heavy carving.
  const raw=[[-6.1,5.39,3.6],[6.1,5.39,3.6],[0,8.17,3.6],[-6.1,5.39,7.6],[6.1,5.39,7.6],[0,8.17,7.6]],faces=[[0,3,5,2],[1,2,5,4],[3,4,5]],v=[],ff=[];for(const face of faces){const k=v.length;v.push(...face.map(i=>local(p,...raw[i])));for(let j=1;j<face.length-1;j++)ff.push([k,k+j,k+j+1])}b.geometry('roof',v,ff);
  b.geometry('teal',[local(p,-5.40,5.55,7.63),local(p,5.4,5.55,7.63),local(p,0,7.97,7.63)],[[0,1,2]]);
  for(const side of [-1,1]){beam('yellow',[side*6.1,5.39,7.68],[0,8.17,7.68],.19);for(let i=0;i<6;i++){const x=side*(.5+i*.78),y=7.89-Math.abs(x)*.455;beam('yellow',[x,y,7.72],[x+side*.33,y-.53,7.72],.10);beam('yellow',[x+side*.33,y-.53,7.72],[x+side*.58,y-.28,7.72],.10)}}beam('yellow',[-6.05,5.45,7.68],[6.05,5.45,7.68],.15);
  for(const side of [-1,1])for(let i=0;i<6;i++){const x=side*(2.7+i*1.08);box('white',x,1.98,7.18,.14,1.10,.14,.025);if(i<5){beam('white',[x,2.49,7.18],[x+side*1.08,2.49,7.18],.10);beam('teal',[x,1.53,7.18],[x+side*1.08,2.39,7.18],.065);beam('teal',[x,2.39,7.18],[x+side*1.08,1.53,7.18],.065)}}
  for(let i=0;i<5;i++)box('white',0,.14+(5-i)*.135,7.43+i*.76,4.65,(5-i)*.27,.82,.04);
  for(const side of [-1,1]){const palm={...p,x:local(p,side*15,0,-5)[0],z:local(p,side*15,0,-5)[2]};this.palm(palm,.93);const q={...p,x:local(p,side*6.8,0,9.45)[0],z:local(p,side*6.8,0,9.45)[2]};this.bed(q,5.2,1.55,side>0?0:2)}
  for(const x of [-11.5,11.5])this.bed({...p,x:local(p,x,0,9.35)[0],z:local(p,x,0,9.35)[2]},4.4,1.9,x>0?0:2);
  for(const side of [-1,1]){const q={...p,x:local(p,side*9.0,0,11.0)[0],z:local(p,side*9.0,0,11.0)[2]};this.lantern(q,true)}
 }
}
const build=Base.prototype.build,draw=Base.prototype.draw;
Base.prototype.build=function(track){if(this.garden){this.garden.release();this.garden=null}if(track.id!=='kapuas')return build.call(this,track);if(this.city){this.city.release();this.city=null}this.dispose();this.wildlife=[];this.ponds=[];this.landmarks=[];this.garden=new Garden(this.r,track);this.batches=this.garden.batches;this.landmarks=this.garden.landmarks};
Base.prototype.draw=function(time,pos){if(this.garden){this.garden.draw();return}return draw.call(this,time,pos)};
root.RaceMempawahGarden=Garden;
})(globalThis);
