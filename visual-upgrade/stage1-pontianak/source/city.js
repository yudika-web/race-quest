/* Stage 1 visual layer only. All road physics, AI, features and actor rendering
   remain in RaceCore/RaceRenderer. No external asset or animation clock. */
(function(root){'use strict';
const Base=root.RaceScenery,TAU=Math.PI*2;
const C={white:[.75,.80,.77],cream:[.73,.61,.42],teal:[.10,.41,.43],glass:[.10,.25,.31],metal:[.18,.24,.28],wood:[.30,.19,.12],roof:[.45,.24,.17],leaf:[.14,.37,.23],lime:[.35,.55,.27],pink:[.65,.37,.35],yellow:[.83,.63,.19],rock:[.35,.43,.44],sand:[.50,.57,.54],black:[.045,.065,.08],orange:[.72,.23,.16]};
const local=(p,x,y,z)=>[p.x+Math.cos(p.yaw)*x+Math.sin(p.yaw)*z,p.y+y,p.z-Math.sin(p.yaw)*x+Math.cos(p.yaw)*z];
class CityBatch extends Base.Batch{
 // One chamfer segment on major cubes; separate face vertices retain planar normals.
 bevel(key,c,size,yaw=0,d=.12){
  const [w,h,l]=size.map(x=>x/2);d=Math.min(d,w*.45,h*.45,l*.45);const ring=[[-w+d,-l], [w-d,-l],[w,-l+d],[w,l-d],[w-d,l],[-w+d,l],[-w,l-d],[-w,-l+d]],v=[],f=[];
  const rings=[[-h,w-d,l-d],[-h+d,w,l],[h-d,w,l],[h,w-d,l-d]];
  for(const [yy,ww,ll] of rings)for(const [x,z] of ring){const xx=x*ww/w,zz=z*ll/l;v.push([c[0]+Math.cos(yaw)*xx+Math.sin(yaw)*zz,c[1]+yy,c[2]-Math.sin(yaw)*xx+Math.cos(yaw)*zz])}
  const faces=[];for(let j=0;j<3;j++)for(let i=0;i<8;i++)faces.push([j*8+i,j*8+(i+1)%8,(j+1)*8+(i+1)%8,(j+1)*8+i]);faces.push([...Array(8).keys()].reverse(),[...Array(8).keys()].map(i=>24+i));
  // Split face-local vertices so weighted smoothing cannot inflate the flat block sides.
  const out=[];for(const face0 of faces){const face=face0.slice().reverse();const k=out.length;out.push(...face.map(i=>v[i]));for(let i=1;i<face.length-1;i++)f.push([k,k+i,k+i+1])}this.geometry(key,out,f);
 }
 beam(key,a,b,width,depth=width){
  const dy=b.map((x,i)=>x-a[i]),len=Math.hypot(...dy),y=dy.map(x=>x/len),ref=Math.abs(y[1])>.95?[1,0,0]:[0,1,0],cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],x=cross(ref,y),n=Math.hypot(...x);for(let i=0;i<3;i++)x[i]/=n;const z=cross(x,y),v=[];
  for(const p of [a,b])for(const [xx,zz] of [[-1,-1],[1,-1],[1,1],[-1,1]])v.push(p.map((q,i)=>q+x[i]*xx*width/2+z[i]*zz*depth/2));
  this.geometry(key,v,[[0,3,2],[0,2,1],[4,5,6],[4,6,7],[0,1,5],[0,5,4],[1,2,6],[1,6,5],[2,3,7],[2,7,6],[3,0,4],[3,4,7]].map(f=>f.slice().reverse()));
 }
 ring(key,c,r,t,plane='XZ',n=32){
  const v=[],f=[];for(let i=0;i<n;i++){const a=i/n*TAU;for(const rr of [r-t,r+t]){let p=plane==='XZ'?[Math.cos(a)*rr,0,Math.sin(a)*rr]:plane==='XY'?[Math.cos(a)*rr,Math.sin(a)*rr,0]:[0,Math.sin(a)*rr,Math.cos(a)*rr];v.push(p.map((q,k)=>q+c[k]))}}
  for(let i=0;i<n;i++){const a=i*2,b=(i+1)%n*2;f.push([a,b,b+1],[a,b+1,a+1])}this.geometry(key,v,f);
 }
}
class City{
 constructor(renderer,track){this.r=renderer;this.track=track;this.textures=[];this.labels=[];this.objects=[];this.landmarks=[];this.batch=new CityBatch();this.markings=new CityBatch();this.pavement=new CityBatch();this.build()}
 upload(b,noShadow=false){const meshes=b.upload(this.r);for(const m of meshes){m.p.material.color=C[m.key]||C.white;m.p.material.rough=m.key==='glass'?.32:m.key==='metal'?.50:.86;if(noShadow)m.key='shadow'}return meshes}
 texture(canvas){const g=this.r.gl,t=g.createTexture();g.bindTexture(g.TEXTURE_2D,t);g.texImage2D(g.TEXTURE_2D,0,g.RGBA,g.RGBA,g.UNSIGNED_BYTE,canvas);g.generateMipmap(g.TEXTURE_2D);g.texParameteri(g.TEXTURE_2D,g.TEXTURE_MIN_FILTER,g.LINEAR_MIPMAP_LINEAR);g.texParameteri(g.TEXTURE_2D,g.TEXTURE_WRAP_S,g.CLAMP_TO_EDGE);g.texParameteri(g.TEXTURE_2D,g.TEXTURE_WRAP_T,g.CLAMP_TO_EDGE);this.textures.push(t);return t}
 label(p,text,w=6,h=1.2,y=1.8,z=4.2){
  const canvas=document.createElement('canvas');canvas.width=512;canvas.height=128;const c=canvas.getContext('2d');c.fillStyle='#e7d8b5';c.fillRect(0,0,512,128);c.fillStyle='#194652';c.fillRect(0,0,512,10);c.fillRect(0,118,512,10);c.textAlign='center';c.textBaseline='middle';const lines=text.split('\n');c.font='800 '+(lines.length>1?'33':'40')+'px sans-serif';lines.forEach((s,i)=>c.fillText(s,256,lines.length>1?46+i*39:65,486));const v=[local(p,-w/2,y-h/2,z),local(p,w/2,y-h/2,z),local(p,w/2,y+h/2,z),local(p,-w/2,y+h/2,z)];const q=this.r.mesh(v,[[0,1,2],[0,2,3]],[1,1,1],[[0,1],[1,1],[1,0],[0,0]],this.texture(canvas),true);q.material.rough=.9;this.labels.push({key:'shadow',p:q});
 }
 locate(u,lat,radius,type){
  for(const du of [0,.012,-.012,.025,-.025])for(const extra of [0,3,6,9]){const p=this.track.place(this.track.length*(u+du),Math.sign(lat)*(Math.abs(lat)+extra));if(this.r.clearance(p.x,p.z)>radius+8.5&&!this.landmarks.some(q=>Math.hypot(q.x-p.x,q.z-p.z)<q.radius+radius+.6)){p.y=this.r.groundAt(p.x,p.z);p.yaw+=lat>0?-Math.PI/2:Math.PI/2;this.objects.push({type,x:p.x,z:p.z,radius,clearance:this.r.clearance(p.x,p.z)});return p}}return null;
 }
 build(){
  const r=this.r,t=this.track,b=this.batch,m=this.markings;
  // All these materials belong to this new world build, never to a character or other stage.
  const asphalt=document.createElement('canvas');asphalt.width=asphalt.height=128;const ac=asphalt.getContext('2d');ac.fillStyle='#414f5a';ac.fillRect(0,0,128,128);const rng=RaceCore.seedRandom(90281);for(let i=0;i<650;i++){ac.fillStyle=i%2?'#45545e':'#3e4b55';ac.fillRect(Math.floor(rng()*128),Math.floor(rng()*128),1,1)}r.road.material.texture=this.texture(asphalt);r.road.material.color=[.77,.81,.82];r.road.material.rough=.94;r.curbs.forEach((p,i)=>p.material.color=i?[.23,.30,.33]:[.75,.80,.77]);r.shoulders.material.texture=null;r.shoulders.material.color=[.36,.45,.43];r.ground.material.texture=null;r.ground.material.color=[.25,.40,.29];
  // Only decorative generic trees/rocks/bridge/tunnel are replaced. Real hazards stay in features.
  r.static=r.static.filter(o=>o.file==='prop_start_gate.glb');r.staticShadows.count=0;
  const kh=this.locate(.14,-23,9,'tugu-khatulistiwa');if(kh)this.landmarks.push({...kh,type:'tugu-khatulistiwa',radius:9});
  const ba=this.locate(.415,23,8.6,'tugu-bambu');if(ba)this.landmarks.push({...ba,type:'tugu-bambu',radius:8.6});
  const N=550;
  for(const side of [-1,1]){
   const v=[],f=[],wall=[],wf=[];
   for(let i=0;i<=N;i++){const p=t.point(i/N*t.length);for(const d of [5.55,8.15])v.push([p.x+p.rightX*side*d,p.y+.155,p.z+p.rightZ*side*d]);const x=p.x+p.rightX*side*8.15,z=p.z+p.rightZ*side*8.15;wall.push([x,r.groundAt(x,z)-.03,z],[x,p.y+.155,z]);if(i){const k=i*2;f.push([k-2,k,k-1],[k-1,k,k+1]);wf.push([k-2,k,k-1],[k-1,k,k+1])}}
   this.pavement.geometry('sand',v,f);this.pavement.geometry('rock',wall,wf);
  }
  // Lane markings are flat decals; exclude them from the sun pass via the existing shadow key.
  const strip=(s0,s1,a,c,key)=>{const v=[];for(const s of [s0,s1]){const p=t.point(s);for(const d of [a,c])v.push([p.x+p.rightX*d,p.y+.102,p.z+p.rightZ*d])}m.geometry(key,v,[[0,2,1],[1,2,3]])};
  for(let s=8;s<t.length;s+=10)strip(s,s+4,-.065,.065,'white');for(let s=0;s<t.length;s+=2)for(const side of [-1,1])strip(s,s+2,side*4.64,side*4.74,'white');
  for(const u of [.025,.278,.615])for(let k=-4;k<=4;k++)strip(t.length*u-.95,t.length*u+.95,k*.92-.26,k*.92+.26,'white');
  // Streetlights and trimmed city trees. Their footprints stay entirely outside the racing envelope.
  for(let i=0;i<32;i++){const side=i%2?1:-1,p=this.locate((i+.35)/32,side*9.1,.48,'streetlight');if(!p)continue;
   b.bevel('rock',local(p,0,.16,0),[.64,.32,.64],p.yaw,.08);b.box('metal',local(p,0,2.5,0),[.13,4.7,.13],p.yaw);b.beam('metal',local(p,0,4.6,0),local(p,0,4.95,1.0),.12);b.bevel('metal',local(p,0,4.94,1.07),[.54,.16,.95],p.yaw,.045);b.box('yellow',local(p,0,4.844,1.07),[.40,.025,.72],p.yaw);
  }
  for(let i=0;i<27;i++){const side=i%2?-1:1,p=this.locate((i+.8)/27,side*11.3,1.7,'city-tree');if(!p)continue;this.tree(p,1+(i%3)*.09)}
  // Compact shop blocks: broad silhouettes, inset windows, awnings, roof parapets.
  const fronts=['cream','teal','white','pink','cream','teal'];
  for(let i=0;i<42;i++){const side=i%2?1:-1,p=this.locate((i<36?i+.31:i-36+.31)/(i<36?36:6),side*(i<36?17.5+i%3*1.5:33),4.4,'city-building');if(!p||this.landmarks.some(q=>Math.hypot(q.x-p.x,q.z-p.z)<q.radius+6))continue;
   const h=4.4+(i%4)*1.3+(i>=36?2:0),w=5.4+(i%2)*.8,d=4.6;
   b.bevel('rock',local(p,0,.15,0),[w+.9,.4,d+.9],p.yaw,.08);b.bevel(fronts[i%fronts.length],local(p,0,h/2+.28,0),[w,h,d],p.yaw,.10);b.box('white',local(p,0,h+.30,0),[w+.16,.23,d+.16],p.yaw);b.box('metal',local(p,0,.97,d/2+.045),[1.0,1.55,.075],p.yaw);
   for(const x of [-w*.30,w*.30])for(let floor=0;floor<(h>5?2:1);floor++){
    const y=1.8+floor*2.5;b.box('white',local(p,x,y,d/2+.05),[1.45,1.42,.13],p.yaw);b.box('glass',local(p,x,y,d/2+.125),[1.22,1.18,.03],p.yaw);b.box('white',local(p,x,y,d/2+.147),[.045,1.20,.02],p.yaw);
   }
   b.bevel(i%2?'orange':'teal',local(p,0,2.64,d/2+.43),[w*.91,.18,.98],p.yaw,.04);b.box('cream',local(p,0,3.13,d/2+.08),[w*.71,.40,.09],p.yaw);for(let j=0;j<3;j++)b.box('white',local(p,(j-1)*.78,3.13,d/2+.14),[.48,.11,.02],p.yaw);
  }
  // Small planted public square / decorative roundabout, entirely outside the race route.
  if(kh){this.plaza(kh,9);this.khatulistiwa(kh);this.label(kh,'TUGU\nKHATULISTIWA',6.6,1.35,1.15,4.30)}
  if(ba){this.plaza(ba,8.6);this.bambu(ba);this.label(ba,'TUGU BAMBU\nPONTIANAK',6.4,1.3,1.1,4.1)}
  // Retain the elevated driving geometry; add urban supports beneath the old bridge approach.
  for(const u of [.058,.075,.092]){const p=t.point(t.length*u),base=r.groundAt(p.x+p.rightX*6.7,p.z+p.rightZ*6.7);for(const side of [-1,1])b.bevel('rock',[p.x+p.rightX*side*5.9,(base+p.y)/2,p.z+p.rightZ*side*5.9],[.75,Math.max(.35,p.y-base),1.2],p.yaw,.06)}
  this.batches=[...this.upload(b),...this.upload(m,true),...this.upload(this.pavement,true),...this.labels];this.stats={landmarks:this.landmarks.map(p=>({type:p.type,x:p.x,y:p.y,z:p.z,yaw:p.yaw,radius:p.radius})),objects:this.objects,triangles:this.batches.reduce((n,o)=>n+o.p.count/3,0),colour_draw_calls:this.batches.length,shadow_draw_calls:this.batches.filter(o=>o.key!=='shadow').length,textures:this.textures.length,static_visuals:true};
 }
 tree(p,s){const b=this.batch;b.bevel('white',local(p,0,.18,0),[2*s,.36,2*s],p.yaw,.12);b.box('leaf',local(p,0,.38,0),[1.72*s,.10,1.72*s],p.yaw);b.box('wood',local(p,0,1.65,0),[.32,2.8,.32],p.yaw);b.bevel('leaf',local(p,0,3.35,0),[2.65*s,2.05*s,2.5*s],p.yaw,.27);b.bevel('lime',local(p,-.47*s,4.16*s,.09*s),[1.98*s,1.25*s,1.86*s],p.yaw,.23)}
 plaza(p,r){const b=this.batch;b.cylinder('rock',[p.x,p.y+.01,p.z],r,.18,32);b.cylinder('sand',[p.x,p.y+.19,p.z],r-.35,.075,32);b.ring('white',[p.x,p.y+.268,p.z],r-1.1,.14,'XZ',40);b.cylinder('leaf',[p.x,p.y+.27,p.z],r-2.0,.12,28);for(let i=0;i<4;i++){const a=i*Math.PI/2;b.bevel('sand',local(p,Math.cos(a)*(r-1.6),.41,Math.sin(a)*(r-1.6)),[1.8,.40,.65],p.yaw+a,.10);const q={...p,x:p.x+Math.cos(a+.5)*(r-1.8),z:p.z+Math.sin(a+.5)*(r-1.8)};b.bevel(i%2?'lime':'leaf',[q.x,q.y+.75,q.z],[1.4,.78,1.4],p.yaw,.20)}}
 khatulistiwa(p){const b=this.batch;
  b.bevel('white',local(p,0,.65,0),[8.0,.52,7.8],p.yaw,.12);b.bevel('orange',local(p,0,1.05,0),[6.8,.34,6.6],p.yaw,.10);b.bevel('cream',local(p,0,1.46,0),[5.8,.53,5.6],p.yaw,.10);
  for(const x of [-1.05,1.05])for(const z of [-1.02,1.02]){const h=z<0?7.65:6.60;b.bevel('black',local(p,x,1.75+h/2,z),[.43,h,.43],p.yaw,.055);for(const yy of [2.05,1.75+h-.25])b.box('yellow',local(p,x,yy,z),[.50,.20,.50],p.yaw)}
  b.beam('black',local(p,-1.05,9.40,-1.02),local(p,1.05,9.40,-1.02),.35);for(const x of [-1.05,1.05])b.beam('black',local(p,x,8.35,1.02),local(p,x,9.40,-1.02),.27);
  const center=local(p,0,10.85,-1.02);b.ring('yellow',center,1.43,.105,'XY',40);b.ring('black',center,1.43,.10,'YZ',40);b.ring('orange',center,1.43,.095,'XZ',40);
  b.beam('black',local(p,-2.85,12.08,-1.02),local(p,3.05,12.08,-1.02),.17);const v=[local(p,3.75,12.08,-1.02),local(p,2.84,12.45,-1.02),local(p,2.84,11.71,-1.02)];b.geometry('yellow',v,[[0,1,2]]);
 }
 bambu(p){const b=this.batch;b.cylinder('white',[p.x,p.y+.40,p.z],4.05,.45,20);b.cylinder('orange',[p.x,p.y+.85,p.z],3.42,.38,20);b.cylinder('cream',[p.x,p.y+1.23,p.z],2.75,.25,20);
  for(let i=0;i<11;i++){const a=i/11*TAU,rad=i%3===0?.76:1.65,x=Math.cos(a)*rad,z=Math.sin(a)*rad,h=5.1+(i%4)*.78,base=local(p,x,1.48,z);b.cylinder('orange',base,.185,h,8);for(let j=1;j<h;j+=1.22)b.cylinder('yellow',[base[0],base[1]+j,base[2]],.205,.105,8);const v=[],n=8;for(let k=0;k<n;k++){const t=k/n*TAU;v.push([base[0]+Math.cos(t)*.185,base[1]+h,base[2]+Math.sin(t)*.185])}v.push([base[0]+.11,base[1]+h+.74,base[2]+.11]);const f=[];for(let k=0;k<n;k++)f.push([k,(k+1)%n,n]);b.geometry('yellow',v,f)}
 }
 draw(){for(const {p} of this.batches)this.r.drawPrimitive(p,RaceMath.identity())}
 release(){for(const t of this.textures)this.r.gl.deleteTexture(t);this.textures=[]}
}
const build=Base.prototype.build,draw=Base.prototype.draw;
Base.prototype.build=function(track){if(this.city){this.city.release();this.city=null}if(track.id!=='kampung')return build.call(this,track);this.dispose();this.wildlife=[];this.ponds=[];this.landmarks=[];this.city=new City(this.r,track);this.batches=this.city.batches;this.landmarks=this.city.landmarks};
Base.prototype.draw=function(time,pos){if(this.city){this.city.draw();return}return draw.call(this,time,pos)};
root.RacePontianakCity=City;
})(globalThis);
