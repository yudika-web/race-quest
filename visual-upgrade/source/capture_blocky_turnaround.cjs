// Actual game renderer + delivered GLBs. Only car primitives are hidden for
// the character turnaround; before/after share camera, canvas, light and time.
const {chromium}=require('/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path'),cp=require('child_process');
const D=path.resolve(__dirname,'..'),BASE='276792553e913520119038cac5c9512035751d86';
(async()=>{const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox','--enable-unsafe-swiftshader']});const cameras={};try{
 for(const label of ['before','after']){
  const page=await browser.newPage({viewport:{width:800,height:800}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
  if(label==='before'){const html=cp.execFileSync('git',['show',BASE+':visual-upgrade/race-quest-visual-upgrade.html'],{cwd:D,maxBuffer:32*1024*1024});await page.route('**/turnaround-baseline.html',r=>r.fulfill({status:200,contentType:'text/html',body:html}))}
  await page.goto('http://127.0.0.1:8000/'+(label==='before'?'turnaround-baseline.html':'visual-upgrade/race-quest-visual-upgrade.html'));
  await page.evaluate(()=>{
   const c=document.createElement('canvas');c.id='catTurnaround';c.style='position:fixed;inset:0;width:800px;height:800px;z-index:999999;background:#132940';document.body.append(c);
   const r=window.turnaroundR=new RaceRenderer(c,JSON.parse(document.getElementById('assetData').textContent));r.setQuality('high');r.ensureModel('kart_arka.glb');const model=r.models['kart_arka.glb'];
   const selected=new Set();for(const [i,ps] of Object.entries(model.primitives))if(/^(driver_|eyes_|ear_[lr]_|tail_)/.test(model.doc.nodes[i].name))ps.forEach(p=>selected.add(p));
   const draw=r.drawPrimitive.bind(r);r.drawPrimitive=(p,...args)=>{if(selected.has(p))draw(p,...args)};
  });cameras[label]={};
  for(const [angle,eye] of Object.entries({front:[0,1.23,2.05],side:[2.1,1.23,-.07],back:[0,1.23,-2.25]})){
   cameras[label][angle]=await page.evaluate(eye=>{const r=turnaroundR;cancelAnimationFrame(window.turnRAF);const render=()=>{r.clock=1;r.begin(eye,[0,1.12,-.08],0);r.gl.uniform1f(r.L.uSunEnabled,0);r.drawModel('kart_arka.glb',RaceMath.identity(),{fog:0});window.turnRAF=requestAnimationFrame(render)};render();return {view:Array.from(r.view),projection:Array.from(r.projection),time:r.clock}},eye);
   await page.locator('#catTurnaround').screenshot({path:D+'/cat-blocky/'+label+'/cat-'+angle+'.png'});
  }
  if(errors.length)throw Error(errors.join('\n'));await page.close();
 }
 if(JSON.stringify(cameras.before)!==JSON.stringify(cameras.after))throw Error('Turnaround cameras differ');
 fs.writeFileSync(D+'/cat-blocky/turnaround-cameras.json',JSON.stringify({status:'passed',cameras,baseline:BASE},null,2));console.log('Six character-only turnaround renders captured with identical cameras');
 }finally{await browser.close()}})().catch(e=>{console.error(e);process.exit(1)});
