const {chromium}=require('/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');const path=require('path'),fs=require('fs'),D=path.resolve(__dirname,'..');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox','--enable-unsafe-swiftshader']});try{const p=await b.newPage({viewport:{width:800,height:800}});const errors=[];p.on('pageerror',e=>errors.push(e.message));await p.goto('http://127.0.0.1:8000/visual-upgrade/race-quest-visual-upgrade.html');const report=await p.evaluate(()=>{
 const c=document.createElement('canvas');c.style='width:512px;height:512px';document.body.prepend(c);const r=new RaceRenderer(c,JSON.parse(document.getElementById('assetData').textContent));r.setQuality('high');r.ensureModel('kart_arka.glb');const model=r.models['kart_arka.glb'],names=new Map();for(const [i,ps] of Object.entries(model.primitives))for(const primitive of ps)names.set(primitive,model.doc.nodes[i].name);const original=r.drawPrimitive.bind(r);let record={};r.drawPrimitive=(p,m,...a)=>{const name=names.get(p);if(name)record[name]=Array.from(m);original(p,m,...a)};
 function sample(t,steer=0,lift=0,spin=0){record={};r.clock=t;r.begin([1.3,1.4,1.9],[0,1.12,0],0);r.drawModel('kart_arka.glb',RaceMath.identity(),{fog:0,steer,speed:18,lift,spin});return record}
 const checks=[];function check(ok,s){if(!ok)throw Error(s);checks.push(s)}
 const a=sample(0),b=sample(.4),closed=sample(3.61),turn=sample(0,.42),wheel=sample(0,0,0,1),jump=sample(0,0,2);
 const key=prefix=>Object.keys(a).find(k=>k.startsWith(prefix));const diff=(x,y,k)=>JSON.stringify(x[k])!==JSON.stringify(y[k]);
 check(closed[key('eyes_')][5]<a[key('eyes_')][5]*.15,'Blink squashes the blocky eye surfaces');
 check(diff(a,b,key('ear_l_'))&&diff(a,b,key('ear_r_')),'Both blocky ears retain idle articulation');
 check(diff(a,b,key('tail_')),'Tail animation retained');
 check(diff(a,turn,key('driver_')),'Blocky torso retains steering lean');
 check(diff(a,jump,key('driver_')),'Blocky torso retains jump response');
 check(diff(a,turn,key('wheel_fl_spin_'))&&diff(a,turn,key('wheel_fr_spin_')),'Front wheels retain steering');
 check(diff(a,wheel,key('wheel_rl_spin_')),'Wheel rotation retained');
 check(JSON.stringify(sample(2,.2,0,15))===JSON.stringify(sample(2,.2,0,15)),'All rigid matrices remain identical at frozen simulation time');
 // Contact fixture: transform designed palm centres and the unchanged steering
 // rim through the actual renderer matrices, including worst-case lean/jump.
 const transform=(m,v)=>[0,1,2].map(i=>m[i]*v[0]+m[4+i]*v[1]+m[8+i]*v[2]+m[12+i]);let maxDistance=0;
 for(const steer of [-.42,0,.42])for(const lift of [0,1,2,3]){const pose=sample(2,steer,lift,15);for(const side of [-1,1]){const hand=transform(pose[key('driver_')],[side*.181,.840-.67,.234+.17]);let distance=Infinity;for(let i=0;i<240;i++){const angle=i/240*Math.PI*2,point=transform(pose[key('body_suspension_')],[.18*Math.cos(angle),.83+.18*.88*Math.sin(angle)-.35,.235+.18*.48*Math.sin(angle)]);distance=Math.min(distance,Math.hypot(...hand.map((v,j)=>v-point[j])))}maxDistance=Math.max(maxDistance,distance)}}
 check(maxDistance<.060,'Palm-centre contact fixture stays within grip envelope through steering and jump');
 check(r.gl.getError()===r.gl.NO_ERROR,'Blocky model renders without WebGL errors');
 return {status:'passed',checks,max_palm_centre_to_rim_distance_m:maxDistance,note:'Contact fixture verifies designed centres and actual rigid transforms, supplemented by front/profile/back render inspection. It is not a full mesh collision solver.'}
 });if(errors.length)throw Error(errors.join('\n'));report.errors=errors;fs.writeFileSync(D+'/cat-blocky/animation-tests.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report));}finally{await b.close()}})().catch(e=>{console.error(e);process.exit(1)});
