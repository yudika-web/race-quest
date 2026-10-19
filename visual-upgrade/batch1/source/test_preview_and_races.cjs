const {chromium}=require('/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path'),D=path.resolve(__dirname,'..');
const specs=[{index:1,id:'nara',eye:.122,z:.151,top:1.535,half:.30,mouth:1.155,mz:.238},{index:2,id:'bimo',eye:.177,z:.180,top:1.670,half:.34,mouth:1.105,mz:.232},{index:3,id:'sora',eye:.145,z:.145,top:1.970,half:.25,mouth:1.122,mz:.157}];
(async()=>{const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox','--enable-unsafe-swiftshader']});const report={status:'running',cases:[],errors:[],consoleErrors:[]};try{
for(const [device,opts] of [['desktop',{viewport:{width:1440,height:1000}}],['mobile',{viewport:{width:390,height:844},hasTouch:true,isMobile:true}]])for(const spec of specs){
 if((process.env.BATCH_QA_DEVICE&&device!==process.env.BATCH_QA_DEVICE)||(process.env.BATCH_QA_ID&&spec.id!==process.env.BATCH_QA_ID))continue;
 const p=await browser.newPage(opts);p.setDefaultTimeout(120000);p.on('pageerror',e=>report.errors.push(e.message));p.on('console',m=>{if(m.type()==='error')report.consoleErrors.push(m.text())});await p.route('**/favicon.ico',r=>r.fulfill({status:204}));
 const checks=[];const check=(ok,s)=>{if(!ok)throw Error(spec.id+' '+device+': '+s);checks.push(s);console.log('PASS',spec.id,device,s)};
 await p.goto('http://127.0.0.1:8000/visual-upgrade/race-quest-pro-batch1.html');
 await p.evaluate(()=>{
  const proto=RaceRenderer.prototype,model=proto.drawModel,draw=proto.drawPrimitive,race=proto.race;
  proto.drawModel=function(f,m,o){const old=this._testBatchActive;this._testBatchActive=/^kart_(nara|bimo|sora)(?:_low)?\.glb$/.test(f);if(this._testBatchActive)window.drawnExpression=o?.expression||'normal';try{return model.call(this,f,m,o)}finally{this._testBatchActive=old}};
  proto.drawPrimitive=function(p,m,...a){if(this._testBatchActive&&window.batchMatrices)batchMatrices.push(Array.from(m));return draw.call(this,p,m,...a)};
  proto.race=function(s,...a){window.batchMatrices=[];window.batchS=s;window.batchR=this;return race.call(this,s,...a)};
 });
 await p.locator('#home [data-act=setup]').click();await p.locator('#playerName').fill('Batch preview QA');await p.locator('#setupForm button[type=submit]').click();await p.locator('#helpDialog').waitFor();await p.locator('#helpDialog [data-close=helpDialog]').first().click();await p.locator('#characterGrid [data-index="'+spec.index+'"]').click();await p.waitForFunction(i=>document.getElementById('world').__garageRenderer.garageCharacter===i,spec.index);
 await p.evaluate(()=>{window.batchR=document.getElementById('world').__garageRenderer;window.projectPoint=v=>{const r=batchR,m=RaceMath.mul(r.projection,r.view),q=[0,1,2,3].map(i=>m[i]*v[0]+m[4+i]*v[1]+m[8+i]*v[2]+m[12+i]),rect=r.canvas.getBoundingClientRect();return{x:rect.x+(q[0]/q[3]+1)*rect.width/2,y:rect.y+(1-q[1]/q[3])*rect.height/2}}});
 await p.locator('[data-garage-auto]').click();const span=await p.evaluate(s=>Math.abs(projectPoint([s.eye,1.286,s.z]).x-projectPoint([-s.eye,1.286,s.z]).x),spec);
 check(await p.locator('#characterGrid [data-index="'+spec.index+'"] img').evaluate(el=>el.complete&&el.naturalWidth===256),'New 256px portrait loads');
 const out=D+'/after/'+spec.id;fs.mkdirSync(out,{recursive:true});await p.screenshot({path:out+'/garage-full-'+device+'.png'});
 await p.locator('[data-garage-view=close]').click();await p.waitForFunction(({s,span})=>Math.abs(projectPoint([s.eye,1.286,s.z]).x-projectPoint([-s.eye,1.286,s.z]).x)>span*1.5,{s:spec,span});
 const close=await p.evaluate(s=>Math.abs(projectPoint([s.eye,1.286,s.z]).x-projectPoint([-s.eye,1.286,s.z]).x),spec);check(close>span*1.5,'Close-up makes the face clearly larger');
 const fit=await p.evaluate(s=>{const bar=document.querySelector('.garage-view-controls').getBoundingClientRect(),exp=document.querySelector('.batch-expression').getBoundingClientRect(),foot=document.querySelector('.garage-bottom').getBoundingClientRect(),preview=document.getElementById('garagePreviewHost').getBoundingClientRect();return{top:Math.min(projectPoint([s.half,s.top,-.1]).y,projectPoint([-s.half,s.top,-.1]).y),toolbarBottom:bar.bottom,mouth:projectPoint([0,s.mouth,s.mz]).y,expressionTop:exp.top,previewBottom:preview.bottom,footerTop:foot.top}},spec);
 console.log('FIT',spec.id,device,JSON.stringify(fit));await p.screenshot({path:out+'/garage-close-'+device+'.png'});
 check(fit.top>fit.toolbarBottom+4,'Head and ears clear the toolbar');check(fit.mouth+8<fit.expressionTop,'Expression control clears the mouth');check(fit.previewBottom<=fit.footerTop+2,'Preview clears race action buttons');
 await p.screenshot({path:out+'/garage-close-'+device+'.png'});
 for(const expression of ['happy','shock','normal']){await p.locator('.batch-expression select').selectOption(expression);await p.waitForFunction(x=>window.drawnExpression===x,expression);check(await p.evaluate(x=>batchR.previewExpression===x,expression),'Expression '+expression+' reaches the renderer')}
 const rect=await p.locator('#world').boundingBox(),x=rect.x+rect.width*.5,y=rect.y+rect.height*.5,yaw=await p.evaluate(()=>batchR.garageOrbit.yaw);
 if(device==='desktop'){
  await p.mouse.move(x,y);await p.mouse.down();await p.mouse.move(x+80,y+15,{steps:6});await p.mouse.up();check(Math.abs(await p.evaluate(()=>batchR.garageOrbit.yaw)-yaw)>.4,'Mouse drag rotates preview');const zoom=await p.evaluate(()=>batchR.garageOrbit.scale);await p.mouse.wheel(0,-170);await p.waitForFunction(z=>batchR.garageOrbit.scale<z,zoom);check(true,'Wheel zoom works');
 }else{
  const cdp=await p.context().newCDPSession(p);await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x,y}]});await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:x+65,y:y+10}]});await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});check(Math.abs(await p.evaluate(()=>batchR.garageOrbit.yaw)-yaw)>.3,'Finger drag rotates preview');const zoom=await p.evaluate(()=>batchR.garageOrbit.scale);await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:x-35,y},{x:x+35,y}]});await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:x-65,y},{x:x+65,y}]});await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});check(await p.evaluate(()=>batchR.garageOrbit.scale)<zoom,'Pinch zoom works');
 }
 check(await p.evaluate(()=>!batchR.garageOrbit.auto),'Manual rotation stops automatic spin');await p.locator('[data-garage-reset]').click();check(await p.evaluate(()=>batchR.garageOrbit.scale===1&&batchR.garageOrbit.auto),'Reset restores scale and automatic spin');await p.locator('[data-garage-auto]').click();const stop=await p.evaluate(()=>batchR.garageOrbit.yaw);await p.locator('[data-garage-auto]').click();await p.waitForFunction(yaw=>batchR.garageOrbit.yaw>yaw+.005,stop);check(true,'Automatic rotation can resume');
 await p.locator('[data-garage-view=full]').click();await p.waitForFunction(()=>batchR.garageView==='full');check(true,'Full vehicle mode remains available');await p.locator('[data-garage-view=close]').click();
 await p.locator('#startRaceBtn').click();await p.waitForFunction(()=>window.batchS);await p.evaluate(()=>batchS.countdown=.01);await p.waitForFunction(()=>batchS.status==='racing');
 const distance=await p.evaluate(()=>{const q=batchS.track.place(batchS.player.s,batchS.player.lateral);return Math.hypot(batchR.eye[0]-q.x,batchR.eye[2]-q.z)});check(Math.abs(distance-6.8)<.12,'Close-up does not change the chase camera');await p.screenshot({path:out+'/race-'+device+'.png'});
 await p.locator('#pauseRaceBtn').click();await p.locator('#pauseDialog').waitFor();
 async function frozenSnapshot(){return p.evaluate(()=>{batchR.race(batchS,0);return JSON.stringify({player:batchS.player,ai:batchS.ai,time:batchS.elapsed,clock:batchR.clock,matrices:batchMatrices,landing:batchR.batchLanding})})}
 const pause=await frozenSnapshot();await p.waitForTimeout(250);check(pause===await frozenSnapshot(),'Pause freezes player, AI, every new-model matrix and reaction timer');
 await p.locator('#pauseDialog [data-act=resumeRace]').click();await p.evaluate(()=>batchS.countdown=.01);await p.waitForFunction(()=>batchS.status==='racing');await p.evaluate(()=>{const s=batchS;s.player.s=s.nextGate-.03;s.player.y=0;s.player.air=false;s.player.speed=12;s.player.error=0;s.player.lateral=0});await p.locator('#questionDialog').waitFor();
 const question=await frozenSnapshot();await p.waitForTimeout(250);check(question===await frozenSnapshot(),'Question freezes player, AI, every new-model matrix and reaction timer');
 const answer=await p.evaluate(()=>batchS.question.correct);await p.locator('#activeAnswerButtons button').nth(answer).click();check(await p.evaluate(()=>!!batchS.slot&&batchS.records.at(-1).correct),'Correct answer grants a buff');await p.locator('#continueRaceBtn').click();await p.evaluate(()=>batchS.countdown=.01);await p.waitForFunction(()=>batchS.status==='racing');check(true,'Race continues after answering');
 if(device==='desktop'){
  // Complete the remaining questions/finish position as a fixture to exercise
  // the actual finish UI and its new winning render, without racing full laps.
  await p.evaluate(()=>{const s=batchS;while(s.records.length<s.count){s.status='question';s.answer(s.question.correct)}s.status='racing';s.player.s=s.total-.01;s.player.y=0;s.player.air=false;s.player.speed=15;s.ai.forEach(a=>{a.s=0;a.finishTime=null})});
  await p.locator('#results').waitFor({state:'visible'});await p.locator('.batch-result-avatar').waitFor();
  check(await p.locator('.batch-result-avatar').evaluate((el,id)=>{const a=JSON.parse(document.getElementById('assetData').textContent);return el.src===a['avatar_'+id+'_happy.webp'].uri},spec.id),'Winning results show the new happy character render');await p.screenshot({path:out+'/results-win.png'});
 }
 check(await p.evaluate(()=>batchR.gl.getError())===0,'No WebGL error');report.cases.push({id:spec.id,device,checks,eye_span_full_px:span,eye_span_close_px:close,enlargement:close/span,fit,chase_distance:distance});await p.close();
}
if(report.errors.length||report.consoleErrors.length)throw Error(JSON.stringify({errors:report.errors,consoleErrors:report.consoleErrors}));report.status='passed';
}catch(e){report.status='failed';report.failure=e.stack;throw e}finally{fs.writeFileSync(D+((process.env.BATCH_QA_DEVICE||process.env.BATCH_QA_ID)?'/debug-preview-race-tests.json':'/preview-race-tests.json'),JSON.stringify(report,null,2));await browser.close()}})().catch(e=>{console.error(e);process.exit(1)});
