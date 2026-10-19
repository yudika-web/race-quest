"""Measured renderer additions for the three new models; cat path is retained."""
from pathlib import Path

def integrate(html,renderer,source):
 renderer=renderer.replace('const KARTS=RaceCore.CHARACTERS.map(c=>c.model);',"const KARTS=RaceCore.CHARACTERS.map(c=>c.model);\nconst BATCH_MODELS={'kart_nara.glb':'kart_nara_low.glb','kart_bimo.glb':'kart_bimo_low.glb','kart_sora.glb':'kart_sora_low.glb'};")
 # Keep and retire both LODs using the existing GPU-buffer disposal path.
 renderer=renderer.replace("for(const f of files)this.ensureModel(f);", "for(const f of files){this.ensureModel(f);if(BATCH_MODELS[f])keep.add(BATCH_MODELS[f])}")
 renderer=renderer.replace("[...KARTS,'kart_arka_low.glb']", "[...KARTS,'kart_arka_low.glb',...Object.values(BATCH_MODELS)]")
 renderer=renderer.replace('speed=0,lift=0}={}){','speed=0,lift=0,expression=\'normal\',landing=0}={}){')
 renderer=renderer.replace("  const hero=file==='kart_arka.glb';", "  const batch=BATCH_MODELS[file],hero=file==='kart_arka.glb';\n  if(batch&&(this.quality==='low'||(fog&&this.eye&&Math.hypot(matrix[12]-this.eye[0],matrix[14]-this.eye[2])>24)))file=batch;")
 body="""   if(batch){
    if(name==='chassis'||name==='driver')world=M.mul(world,M.mul(M.trans([0,Math.sin(time*12)*Math.min(.006,speed*.0004)-Math.min(.016,lift*.008)-landing,0]),M.rz(-steer*Math.min(1,speed/12)*.035)));
    if(name==='driver_pose')world=M.mul(world,M.mul(M.rz(steer*.018),M.rx(-Math.min(.10,lift*.035))));
    if(name==='steering')world=M.mul(world,M.rz(-steer*.30));
    if(name==='eyes'){const phase=(time+(file.includes('nara')?.8:file.includes('bimo')?1.7:2.6))%4.7,b=phase<.16?Math.max(.05,Math.abs(phase-.08)/.08):1;world=M.mul(world,scaleXYZ(expression==='shock'?1.12:1,b*(expression==='shock'?1.1:1),1))}
    if(name==='ear_l'||name==='ear_r')world=M.mul(world,M.rz(Math.sin(time*2.1+(name==='ear_l'?0:1.4))*.024+steer*.02));
    if(name==='tail')world=M.mul(world,M.ry(Math.sin(time*1.9)*.07+steer*.09));
    return world;
   }
"""
 renderer=renderer.replace('   if(!hero)return world;',body+'   if(!hero)return world;')
 renderer=renderer.replace('const n=model.doc.nodes[i];let world=',"const n=model.doc.nodes[i];if(batch&&n.extras?.expression){const e=n.extras.expression;if(e==='eyes'?expression==='happy':e!==expression)return}let world=")
 # Visual reactions use only existing simulation fields. No gameplay state is set.
 method=""" batchPose(session,actor,file,key=0){
  if(!BATCH_MODELS[file])return {};
  if(this.batchPoseSession!==session){this.batchPoseSession=session;this.batchLanding={}}
  const t=session.elapsed,lift=actor.y||0,record=this.batchLanding[key]||(this.batchLanding[key]={time:null,air:!!actor.air||lift>.0001,land:-10});
  if(record.time!==t){const air=!!actor.air||lift>.0001;if(record.air&&!air)record.land=t;record.air=air;record.time=t}
  const age=t-record.land,landing=age>=0&&age<.32?Math.sin(age/.32*Math.PI)*.018:0;
  const hit=actor.bubble>0||actor.slip>0||(key===0&&session.collisionCooldown>.1);
  const won=key===0&&session.status==='finished'&&session.ai.every(a=>a.finishTime===null||a.finishTime>t);
  return {expression:won?'happy':hit?'shock':'normal',landing};
 }
"""
 renderer=renderer.replace(' drawModel(file,matrix,',method+' drawModel(file,matrix,',1)
 # These exact call sites exist in the colour and depth passes.
 for actor,key,files in [('a','i+1','files'),('player','0','files'),('a','i+1','kartFiles'),('p','0','kartFiles')]:
  target=("lift:"+actor+".y||0}")
  # a occurs in both passes, so replace its sites according to the files in scope.
  if actor=='a':continue
  replacement="lift:"+actor+".y||0,...this.batchPose(session,"+actor+","+files+"[session.character],"+key+")}"
  renderer=renderer.replace(target,replacement)
 # AI in the depth pass has files[], colour pass has kartFiles[].
 marker=' renderSunShadows(';a=renderer.index(marker);b=renderer.index(' initParticles(',a)
 part=renderer[a:b].replace('lift:a.y||0}', 'lift:a.y||0,...this.batchPose(session,a,files[a.character],i+1)}');renderer=renderer[:a]+part+renderer[b:]
 a=renderer.index(' race(session,');part=renderer[a:].replace('lift:a.y||0}', 'lift:a.y||0,...this.batchPose(session,a,kartFiles[a.character],i+1)}');renderer=renderer[:a]+part
 renderer=renderer.replace(" race(session,dt,input={},alpha=1){", " race(session,dt,input={},alpha=1){\n  this.batchSession=session;")
 renderer=renderer.replace("this.garageCharacter=character}","this.garageCharacter=character;this.previewExpression='normal';this.canvas.dispatchEvent(new CustomEvent('racequest:preview',{detail:character}))}")
 old="const target=[0,close?(cat?1.32:1.19):(narrow?.70:.85),close?.015:0],radius=(close?(cat?(narrow?1.85:1.75):(narrow?2.15:1.95)):4.0)*orbit.scale;"
 new="const framing=[[1.32,1.75,1.85],[1.22,1.75,1.90],[1.25,1.85,2.00],[1.39,2.05,2.25]][character]||[1.19,1.95,2.15];\n  const target=[0,close?framing[0]:(narrow?.70:.85),close?.015:0],radius=(close?(narrow?framing[2]:framing[1]):4.0)*orbit.scale;"
 assert old in renderer;renderer=renderer.replace(old,new)
 renderer=renderer.replace("this.drawModel(KARTS[character],M.identity(),{fog:0});","this.drawModel(KARTS[character],M.identity(),{fog:0,...(BATCH_MODELS[KARTS[character]]?{expression:this.previewExpression||'normal'}:{})});")
 html=html.replace('</body>', '<script>\n'+(source/'batch1_preview.js').read_text()+'\n</script>\n</body>')
 html=html.replace('</style>', '''
.batch-expression{position:absolute;z-index:7;right:14px;left:auto;bottom:17px;margin:0;display:flex;align-items:center;gap:6px;padding:5px 8px;border:1px solid #86cde644;border-radius:9px;background:#10233ce8;color:#d6e5f4;font-size:11px}
.batch-expression[hidden]{display:none}.batch-expression select{font:inherit;width:88px;height:28px;min-height:0;line-height:1;color:#edf6ff;background:#19324a;border:1px solid #8cb5cf55;border-radius:5px;padding:3px}
#garagePreviewHost[data-batch-model=true] .garage-model-note{text-align:left;padding-right:166px;min-height:51px}
.batch-result-avatar{width:96px;height:96px;object-fit:contain;display:block;margin-top:8px}
@media(max-width:700px){.batch-expression{bottom:17px;right:13px;left:auto}.batch-result-avatar{width:72px;height:72px}}
</style>''',1)
 return html,renderer
