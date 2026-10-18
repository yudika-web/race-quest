(function(root){'use strict';
// Original code-built geometry. Static pieces share material batches; wildlife
// reuses small meshes. No network assets or additional loading steps.
const TAU=Math.PI*2;
const palette={cream:[.75,.63,.43],white:[.86,.91,.88],wood:[.22,.105,.045],roof:[.48,.12,.045],teal:[.025,.32,.34],glass:[.025,.16,.23],metal:[.13,.18,.21],leaf:[.06,.28,.075],lime:[.25,.48,.09],pink:[.85,.17,.32],yellow:[1,.63,.06],lavender:[.38,.18,.66],rock:[.34,.39,.34],sand:[.57,.42,.23],water:[.02,.31,.40],shadow:[.02,.03,.04],orange:[.92,.32,.025],black:[.012,.02,.025]};
class Batch{
 constructor(){this.groups={}}
 geometry(key,V,F,uv=null){const g=this.groups[key]||(this.groups[key]={V:[],F:[],UV:[]});const base=g.V.length;g.V.push(...V);for(const f of F)g.F.push(f.map(i=>i+base));if(uv)g.UV.push(...uv)}
 box(key,c,size,yaw=0){let V=[],F=[];const sn=Math.sin(yaw),cs=Math.cos(yaw);for(let x of [-1,1])for(let y of [-1,1])for(let z of [-1,1])V.push([c[0]+cs*x*size[0]/2+sn*z*size[2]/2,c[1]+y*size[1]/2,c[2]-sn*x*size[0]/2+cs*z*size[2]/2]);
  for(const face of [[0,1,3,2],[4,6,7,5],[0,4,5,1],[2,3,7,6],[0,2,6,4],[1,5,7,3]]){let a=V.length;V.push(...face.map(i=>V[i]));F.push([a,a+1,a+2],[a,a+2,a+3])}this.geometry(key,V,F)}
 ell(key,c,r,nu=16,nv=9){let V=[],F=[];for(let i=0;i<=nu;i++)for(let j=0;j<=nv;j++){const a=i/nu*TAU,b=j/nv*Math.PI;V.push([c[0]+r[0]*Math.sin(b)*Math.cos(a),c[1]+r[1]*Math.cos(b),c[2]+r[2]*Math.sin(b)*Math.sin(a)])}for(let i=0;i<nu;i++)for(let j=0;j<nv;j++){const a=i*(nv+1)+j,b=a+nv+1;if(j)F.push([a,b,a+1]);if(j<nv-1)F.push([a+1,b,b+1])}this.geometry(key,V,F)}
 cylinder(key,c,r,h,segments=16,topRadius=r){let V=[],F=[];for(let j=0;j<2;j++)for(let i=0;i<=segments;i++){const a=i/segments*TAU,rr=j?topRadius:r;V.push([c[0]+Math.cos(a)*rr,c[1]+j*h,c[2]+Math.sin(a)*rr])}const n=segments+1;V.push([c[0],c[1],c[2]],[c[0],c[1]+h,c[2]]);for(let i=0;i<segments;i++){F.push([i,n+i,i+1],[i+1,n+i,n+i+1],[2*n,i,i+1]);if(topRadius)F.push([2*n+1,n+i+1,n+i])}this.geometry(key,V,F)}
 roof(c,w,h,d,yaw){let V=[[-w/2,0,-d/2],[w/2,0,-d/2],[0,h,-d/2],[-w/2,0,d/2],[w/2,0,d/2],[0,h,d/2]],F=[[0,2,1],[3,4,5],[0,3,5],[0,5,2],[1,2,5],[1,5,4]],out=[];const sn=Math.sin(yaw),cs=Math.cos(yaw);for(const f of F){let k=out.length;out.push(...f.map(i=>{const p=V[i];return[c[0]+p[0]*cs+p[2]*sn,c[1]+p[1],c[2]-p[0]*sn+p[2]*cs]}));}this.geometry('roof',out,F.map((_,i)=>[i*3,i*3+1,i*3+2]))}
 ellipse(key,x,y,z,rx,rz,segments=48){let V=[[x,y,z]],UV=[[.5,.5]],F=[];for(let i=0;i<=segments;i++){const a=i/segments*TAU;V.push([x+Math.cos(a)*rx,y,z+Math.sin(a)*rz]);UV.push([.5+.5*Math.cos(a),.5+.5*Math.sin(a)])}for(let i=0;i<segments;i++)F.push([0,i+2,i+1]);this.geometry(key,V,F,UV)}
 softShadow(x,y,z,rx,rz){this.geometry('shadow',[[x-rx,y,z-rz],[x+rx,y,z-rz],[x+rx,y,z+rz],[x-rx,y,z+rz]],[[0,2,1],[0,3,2]],[[0,0],[1,0],[1,1],[0,1]])}
 upload(r){const out=[];for(const [key,g] of Object.entries(this.groups)){let V=[],F=[],UV=[],map=new Map();const hasUV=g.UV.length===g.V.length,flush=()=>{if(!F.length)return;const p=r.mesh(V,F,palette[key],hasUV?UV:null,null,true);if(key==='water'){p.material.water=1;p.material.rough=.2;p.material.color=r.track?.config.palette.water||palette.water}if(key==='shadow'){p.material.shadow=1;p.material.alpha=.30}out.push({key,p});V=[];F=[];UV=[];map=new Map()};for(const face of g.F){if(V.length+face.filter(i=>!map.has(i)).length>65532)flush();F.push(face.map(i=>{if(!map.has(i)){map.set(i,V.length);V.push(g.V[i]);if(hasUV)UV.push(g.UV[i])}return map.get(i)}))}flush()}return out}

}
class Scenery{
 constructor(renderer){this.r=renderer;this.batches=[];this.wildlife=[];this.ponds=[];this.landmarks=[];this.meshes={};this.makeWildlife()}
 makeWildlife(){
  const r=this.r,make=(name,fn)=>{const b=new Batch();fn(b);this.meshes[name]=b.upload(r)};
  make('butterflyBody',b=>{b.ell('black',[0,0,0],[.035,.035,.20],12,6)});
  for(const [name,color] of [['wingBlue','teal'],['wingGold','yellow'],['wingPink','pink']])make(name,b=>{b.ell(color,[.27,0,.06],[.29,.018,.23]);b.ell(color,[.21,0,-.20],[.21,.016,.17]);b.ell('white',[.36,.019,.11],[.06,.008,.065],12,6);b.ell('black',[.46,.015,.05],[.03,.008,.04],10,5)});
  make('duck',b=>{b.ell('white',[0,.28,0],[.28,.23,.40]);b.ell('white',[0,.60,.23],[.18,.19,.18]);b.ell('orange',[0,.56,.43],[.115,.045,.13]);b.ell('cream',[.22,.30,-.02],[.065,.14,.23]);b.ell('cream',[-.22,.30,-.02],[.065,.14,.23]);for(const x of [-.12,.12])b.ell('black',[x,.65,.35],[.026,.029,.018],10,6)});
  make('turtle',b=>{b.ell('leaf',[0,.22,0],[.40,.24,.48],24,14);b.ell('lime',[0,.40,0],[.23,.07,.30]);b.ell('lime',[0,.18,.48],[.14,.13,.18]);for(const x of [-.28,.28])for(const z of [-.28,.25])b.ell('lime',[x,.08,z],[.14,.07,.17]);for(const x of [-.08,.08])b.ell('black',[x,.23,.61],[.018,.021,.012],10,6)});
  make('rabbit',b=>{b.ell('cream',[0,.28,0],[.19,.24,.30]);b.ell('white',[0,.51,.20],[.19,.18,.17]);for(const x of [-.085,.085]){b.ell('white',[x,.77,.17],[.06,.23,.055]);b.ell('pink',[x,.78,.218],[.025,.16,.008]);b.ell('black',[x,.54,.347],[.022,.03,.01],10,6);b.ell('cream',[x,.07,.18],[.08,.065,.16])}b.ell('pink',[0,.48,.371],[.022,.017,.014],10,6);b.ell('white',[0,.28,-.31],[.11,.11,.10])});
 }
 dispose(){for(const {p} of this.batches)for(const b of [p.pos,p.normal,p.uv,p.index])if(b)this.r.gl.deleteBuffer(b);this.batches=[]}
 build(track){
  this.dispose();this.wildlife=[];this.ponds=[];this.landmarks=[];const b=new Batch(),r=this.r,rng=RaceCore.seedRandom(track.config.seed),rnd=(a,c)=>a+rng()*(c-a);
  const place=(u,lat,radius)=>{const p=track.place(track.length*u,lat);return r.clearance(p.x,p.z)>radius+6.6?{...p,y:r.groundAt(p.x,p.z)}:null};
  const local=(p,x,y,z)=>[p.x+Math.cos(p.yaw)*x+Math.sin(p.yaw)*z,p.y+y,p.z-Math.sin(p.yaw)*x+Math.cos(p.yaw)*z];
  // Villages: pitched roofs, porches, raised foundations and inset windows.
  for(let i=0;i<(track.id==='hutan'?3:track.id==='kapuas'?7:10);i++){const u=(i+.28)/10,p=place(u,(i%2?1:-1)*17,4.4);if(!p)continue;p.yaw+=i%2?-Math.PI/2:Math.PI/2;this.landmarks.push({type:'building',x:p.x,z:p.z});const yaw=p.yaw;if(track.id==='kapuas'){for(const x of [-2.3,2.3])for(const z of [-1.8,1.8])b.cylinder('wood',local(p,x,0,z),.14,1.5,8);p.y+=1.1}
   b.box('sand',local(p,0,.12,0),[7,.38,6.2],yaw);b.box(i%2?'teal':'cream',local(p,0,1.65,0),[5.6,3.0,4.4],yaw);b.roof(local(p,0,3.15,0),6.8,1.8,5.5,yaw);
   b.box('wood',local(p,0,1.1,2.23),[1.1,2.0,.10],yaw);b.box('metal',local(p,.35,1.05,2.31),[.08,.08,.06],yaw);
   for(const x of [-1.7,1.7]){b.box('white',local(p,x,1.9,2.25),[1.25,1.2,.12],yaw);b.box('glass',local(p,x,1.9,2.33),[1.05,1.0,.06],yaw);b.box('white',local(p,x,1.9,2.38),[.07,1.06,.03],yaw);b.box('white',local(p,x,1.9,2.38),[1.06,.07,.03],yaw)}
   for(const x of [-2.6,2.6])b.cylinder('wood',local(p,x,.3,3),.09,2.6,10);
   b.box('wood',local(p,0,2.9,2.85),[6.3,.15,2],yaw);b.box('cream',local(p,0,.38,2.9),[6.2,.2,2],yaw);
   b.softShadow(p.x+1,p.y+.025,p.z-1,4.6,4.4);
  }
  if(track.id==='kapuas'){const V=[],F=[];for(let i=0;i<=90;i++){const u=.12+i/90*.72,p=track.place(u*track.length,-28);for(const d of [-7,7])V.push([p.x+p.rightX*d,-.43,p.z+p.rightZ*d]);if(i){const k=i*2;if([V[k-2],V[k-1],V[k],V[k+1]].every(v=>r.clearance(v[0],v[2])>9))F.push([k-2,k,k-1],[k-1,k,k+1])}if(i%3===0&&r.clearance(p.x,p.z)>15)for(const d of [-8,8])for(let j=0;j<3;j++)b.cylinder('leaf',[p.x+p.rightX*d+j*.18,-.4,p.z+p.rightZ*d],.03,.9+j*.22,6)}b.geometry('water',V,F)}
  if(track.id==='hutan')for(let i=0;i<30;i++){const p=place((i+.3)/30,(i%2?1:-1)*12,2);if(!p)continue;for(let j=0;j<3;j++){const a=j*2.1;b.box('wood',local(p,Math.cos(a),.12,Math.sin(a)),[2.2,.20,.23],p.yaw+a)}b.ell('leaf',local(p,0,.4,0),[1.1,.55,1.1],12,7)}
  // Shallow garden ponds: layered banks, rocks, reeds, lily pads and ducks.
  for(const [u,lat] of [[.18,-24],[.48,25],[.89,-24]]){const p=place(u,lat,8);if(!p)continue;this.ponds.push(p);b.ellipse('sand',p.x,p.y+.025,p.z,8.3,6.0);b.ellipse('rock',p.x,p.y+.045,p.z,7.7,5.5);b.ellipse('water',p.x,p.y+.07,p.z,7.15,5.0,64);
   for(let j=0;j<22;j++){let a=j/22*TAU,x=p.x+Math.cos(a)*7.5,z=p.z+Math.sin(a)*5.25;b.ell('rock',[x,p.y+.15,z],[rnd(.25,.6),rnd(.18,.4),rnd(.2,.45)],12,7)}
   for(let j=0;j<10;j++){const a=rnd(0,TAU),x=p.x+Math.cos(a)*7.7,z=p.z+Math.sin(a)*5.5;for(let k=0;k<3;k++){b.cylinder('leaf',[x+k*.12,p.y+.15,z],.025,.65+k*.18,6);b.ell('wood',[x+k*.12,p.y+.90+k*.18,z],[.055,.17,.055],10,6)}}
   for(let j=0;j<5;j++){const x=p.x+rnd(-4,4),z=p.z+rnd(-3,3);b.ellipse('leaf',x,p.y+.09,z,rnd(.3,.55),.35,16);b.ell('pink',[x,p.y+.16,z],[.14,.09,.14],12,7)}
   for(let j=0;j<3;j++)this.wildlife.push({type:'duck',x:p.x,y:p.y+.07,z:p.z,radius:2+j*.65,phase:j*2.1,speed:.14+j*.02});
   this.wildlife.push({type:'turtle',x:p.x+8.5,y:r.groundAt(p.x+8.5,p.z+2),z:p.z+2,phase:rnd(0,TAU),radius:.6,speed:.18});
  }
  // Flower islands, shrubs, benches, fences and trackside flags.
  for(let i=0;i<42;i++){const u=(i+.4)/42,p=place(u,(i%2?1:-1)*rnd(10,15),1.8);if(!p)continue;
   b.ell(i%2?'leaf':'lime',[p.x,p.y+.45,p.z],[1.2,.65,.95]);b.softShadow(p.x+.2,p.y+.025,p.z-.2,1.65,1.25);
   for(let j=0;j<5;j++){const x=p.x+rnd(-1.5,1.5),z=p.z+rnd(-1.3,1.3),y=r.groundAt(x,z);b.cylinder('leaf',[x,y,z],.02,.42,5);b.ell(['pink','yellow','lavender'][i%3],[x,y+.48,z],[.14,.09,.14],10,6);b.ell('yellow',[x,y+.55,z],[.045,.025,.045],8,4)}
   if(i%3===0)for(let j=0;j<2;j++)this.wildlife.push({type:'butterfly',wing:['wingBlue','wingGold','wingPink'][Math.floor(i/3)%3],x:p.x,y:p.y+1.4,z:p.z,radius:.8+j*.6,phase:rnd(0,TAU),speed:.5+rnd(0,.25)});
   if(i%7===0)this.wildlife.push({type:'rabbit',x:p.x+1.7,y:r.groundAt(p.x+1.7,p.z),z:p.z,radius:.5,phase:rnd(0,TAU),speed:.4});
  }
  for(let i=0;i<16;i++){const p=place((i+.7)/16,(i%2?1:-1)*10.8,1);if(!p)continue;const yaw=p.yaw;
   b.cylinder('wood',local(p,0,0,0),.07,3.2,10);b.box(i%2?'orange':'teal',local(p,.52,2.7,0),[1.0,.72,.035],yaw);b.softShadow(p.x+.55,p.y+.025,p.z-.55,1.2,.5);
   if(i%2===0){b.box('wood',local(p,0,.52,1.9),[2.4,.13,.65],yaw);b.box('wood',local(p,0,.95,2.16),[2.4,.65,.09],yaw);for(const x of [-.85,.85])b.box('metal',local(p,x,.25,1.9),[.10,.5,.48],yaw)}
  }
  for(let i=0;i<12;i++){const p=place((i+.5)/12,(i%2?1:-1)*12.4,3);if(!p)continue;for(const x of [-2,0,2])b.box('white',local(p,x,.6,0),[.12,1.2,.14],p.yaw);for(const y of [.35,.85])b.box('white',local(p,0,y,0),[4.3,.12,.10],p.yaw)}
  this.batches=b.upload(r);
 }
 wildlifePose(a,time){
  const t=time*a.speed+a.phase,fly=a.type==='butterfly',hop=a.type==='rabbit'?Math.pow(Math.max(0,Math.sin(t*3)),3)*.17:0;
  const x=a.x+Math.cos(t)*a.radius,z=a.z+Math.sin(t)*a.radius;
  return {x,y:fly?a.y+Math.sin(t*2)*.25:a.type==='duck'?a.y+Math.sin(t*4)*.025:this.r.groundAt(x,z)+hop,z,yaw:-t,flap:Math.sin(time*12+a.phase)*1.05};
 }
 draw(time,pos){
  const r=this.r,M=RaceMath,identity=M.identity(),tr=(x,y,z,yaw=0,scale=1)=>M.mul(M.trans([x,y,z]),M.mul(M.ry(yaw),M.scale(scale)));
  r.gl.depthMask(false);for(const {key,p} of this.batches)if(key==='shadow')r.drawPrimitive(p,identity);r.gl.depthMask(true);
  for(const {key,p} of this.batches)if(key!=='shadow')r.drawPrimitive(p,identity);
  const draw=(name,m)=>{for(const {p} of this.meshes[name])r.drawPrimitive(p,m)};
  for(const a of this.wildlife){if(Math.hypot(a.x-pos.x,a.z-pos.z)>95)continue;const q=this.wildlifePose(a,time),matrix=tr(q.x,q.y,q.z,q.yaw,a.type==='butterfly'?.85:1);
   if(a.type==='butterfly'){draw('butterflyBody',matrix);draw(a.wing,M.mul(matrix,M.rz(q.flap)));const flip=M.identity();flip[0]=-1;draw(a.wing,M.mul(matrix,M.mul(flip,M.rz(q.flap))))}
   else{r.drawShadow(M.mul(tr(q.x,this.r.groundAt(q.x,q.z)+.03,q.z,q.yaw),M.scale(.4)));draw(a.type,matrix)}
  }
 }
}
root.RaceScenery=Scenery;root.RaceScenery.Batch=Batch;
})(typeof globalThis!=='undefined'?globalThis:this);
