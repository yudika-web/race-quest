// Actual RaceRenderer and GLB data. Matched cameras/time; car/character filters
// reveal authored geometry without editing pixels or generating illustrations.
const {chromium}=require('/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path'),D=path.resolve(__dirname,'..'),label=process.argv[2];
if(!['before','after'].includes(label))throw Error('Use before or after');
(async()=>{const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox','--enable-unsafe-swiftshader']});const cameras={},errors=[];try{
 const page=await browser.newPage({viewport:{width:800,height:800}});page.setDefaultTimeout(120000);page.on('pageerror',e=>errors.push(e.message));await page.goto('http://127.0.0.1:8000/visual-upgrade/'+(label==='before'?'race-quest-visual-upgrade.html':'race-quest-pro-batch1.html'));
 await page.evaluate(()=>{const c=document.createElement('canvas');c.id='modelReview';c.style='position:fixed;inset:0;width:800px;height:800px;z-index:999999;background:#142a41';document.body.append(c);window.reviewR=new RaceRenderer(c,JSON.parse(document.getElementById('assetData').textContent));reviewR.setQuality('high');window.drawReviewOriginal=reviewR.drawPrimitive.bind(reviewR)});
 for(const id of ['nara','bimo','sora']){
  const out=D+'/'+label+'/'+id;fs.mkdirSync(out,{recursive:true});cameras[id]={};
  for(const [name,mode,eye,target] of [
   ['hero','all',[2.3,1.8,2.9],[0,1.0,0]],['front','all',[0,1.55,3.10],[0,1.0,0]],['side','all',[3.10,1.55,.02],[0,1.0,0]],['back','all',[-2.2,1.75,-2.8],[0,1.0,0]],
   ['face','all',[1.35,1.50,2.1],[0,1.25,0]],
   ['character-front','character',[0,1.31,2.15],[0,1.24,-.08]],['character-side','character',[2.30,1.31,-.08],[0,1.24,-.08]],['character-back','character',[0,1.31,-2.3],[0,1.24,-.08]],
   ['vehicle-front','vehicle',[0,.9,2.6],[0,.43,0]],['vehicle-side','vehicle',[2.5,.9,.03],[0,.43,0]],['vehicle-back','vehicle',[-1.9,1.1,-2.1],[0,.43,0]]]){
   cameras[id][name]=await page.evaluate(({id,mode,eye,target})=>{
    cancelAnimationFrame(window.reviewRAF);const r=reviewR,file='kart_'+id+'.glb';r.ensureModel(file);const model=r.models[file],keep=new Set();
    for(const [i,ps] of Object.entries(model.primitives)){const char=/^(driver_|driver_pose_|eyes_|ear_[lr]_|tail_|mouth_)/.test(model.doc.nodes[i].name);if(mode==='all'||(mode==='character'?char:!char))ps.forEach(p=>keep.add(p))}
    r.drawPrimitive=(p,...a)=>{if(keep.has(p))drawReviewOriginal(p,...a)};
    const draw=()=>{r.clock=1;r.begin(eye,target,0);r.gl.uniform1f(r.L.uSunEnabled,0);r.drawModel(file,RaceMath.identity(),{fog:0,expression:'normal'});window.reviewRAF=requestAnimationFrame(draw)};draw();return{view:Array.from(r.view),projection:Array.from(r.projection),width:r.canvas.width,height:r.canvas.height,time:r.clock};
   },{id,mode,eye,target});
   await page.locator('#modelReview').screenshot({path:out+'/'+name+'.png'});
  }
  if(label==='after'){
   for(const expression of ['normal','happy','shock']){
    await page.evaluate(({id,expression})=>{cancelAnimationFrame(window.reviewRAF);const r=reviewR,model=r.models['kart_'+id+'.glb'],keep=new Set();for(const [i,ps] of Object.entries(model.primitives))if(/^(driver_|driver_pose_|eyes_|ear_[lr]_|tail_|mouth_)/.test(model.doc.nodes[i].name))ps.forEach(p=>keep.add(p));r.drawPrimitive=(p,...a)=>{if(keep.has(p))drawReviewOriginal(p,...a)};const draw=()=>{r.clock=1;r.begin([.90,1.40,1.75],[0,id==='sora'?1.37:1.22,-.08],0);r.gl.uniform1f(r.L.uSunEnabled,0);r.drawModel('kart_'+id+'.glb',RaceMath.identity(),{fog:0,expression});window.reviewRAF=requestAnimationFrame(draw)};draw()},{id,expression});await page.locator('#modelReview').screenshot({path:out+'/expression-'+expression+'.png'});
   }
  }
  if(label==='after'){
   await page.evaluate(id=>{cancelAnimationFrame(window.reviewRAF);const r=reviewR;r.drawPrimitive=drawReviewOriginal;const draw=()=>{r.clock=1;r.begin([1.35,1.50,2.1],[0,1.25,0],0);r.gl.uniform1f(r.L.uSunEnabled,0);r.drawModel('kart_'+id+'.glb',RaceMath.identity(),{fog:0,steer:.42,speed:18,lift:3,spin:1,expression:'shock'});window.reviewRAF=requestAnimationFrame(draw)};draw()},id);
   await page.locator('#modelReview').screenshot({path:out+'/grip-turn-jump.png'});
  }
  console.log(label,id,'renders captured');
 }
 if(label==='after'){
  await page.evaluate(()=>{cancelAnimationFrame(window.reviewRAF);const r=reviewR;r.drawPrimitive=drawReviewOriginal;const draw=()=>{r.clock=1;r.begin([2.3,1.8,2.9],[0,1.0,0],0);r.gl.uniform1f(r.L.uSunEnabled,0);r.drawModel('kart_arka.glb',RaceMath.identity(),{fog:0});window.reviewRAF=requestAnimationFrame(draw)};draw()});
  await page.locator('#modelReview').screenshot({path:D+'/after/cat-style-reference.png'});
 }
 if(errors.length)throw Error(errors.join('\n'));fs.writeFileSync(D+'/'+label+'/model-cameras.json',JSON.stringify(cameras,null,2));
 }finally{await browser.close()}})().catch(e=>{console.error(e);process.exit(1)});
