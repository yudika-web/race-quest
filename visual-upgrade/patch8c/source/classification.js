/* Result recording only. The live Session, score, clock, ghost and rewards are never advanced here. */
(function(root){'use strict';
function clone(value,track,seen=new Map()){
 if(value===null||typeof value!=='object'||value===track)return value;if(seen.has(value))return seen.get(value);
 const out=value instanceof Set?new Set():value instanceof Map?new Map():ArrayBuffer.isView(value)?new value.constructor(value):Array.isArray(value)?[]:Object.create(Object.getPrototypeOf(value));seen.set(value,out);
 if(value instanceof Set){for(const v of value)out.add(clone(v,track,seen))}else if(value instanceof Map){for(const[k,v]of value)out.set(clone(k,track,seen),clone(v,track,seen))}else if(!ArrayBuffer.isView(value))for(const k of Object.keys(value))out[k]=clone(value[k],track,seen);return out;
}
function forkRandom(owner,copy){if(typeof owner.rng!=='function')return;const source=owner.rng,tape=[];let read=0;owner.rng=()=>read<tape.length?tape[read++]:source();copy.rng=()=>{const v=source();tape.push(v);return v};}
function start(s){
 if(s.status!=='finished')throw Error('Hasil hanya dicatat setelah pemain finis.');
 const result=s.result(),ghost=s.ghostResult(),live=s.ai.every(a=>a.finishTime!==null),tail=live?null:clone(s,s.track),startTime=s.elapsed;
 if(tail){forkRandom(s,tail);s.ai.forEach((a,i)=>forkRandom(a,tail.ai[i]));tail.settings.autoGas=false;tail.status='racing';for(const key of ['extNote','cliffNote','chaosNote'])if(typeof tail[key]==='function'){const note=tail[key];tail[key]=function(a,...args){if(a!==this.player)return note.call(this,a,...args)}}}
 const maxSeconds=Math.max(180,...s.ai.map(a=>Math.max(0,s.total-a.s)/3+120));
 return{s,result,ghost,tail,startTime,steps:0,limit:Math.ceil(maxSeconds*60),done:live,error:null};
}
function advance(job,budget=120){
 if(job.done)return true;const s=job.tail;
 try{for(let i=0;i<budget&&job.steps<job.limit;i++){
   // A finished entrant leaves active road physics on the isolated copy. No AI is repositioned.
   Object.assign(s.player,{s:-s.total-1000,lateral:0,speed:0,error:0,steering:0,y:0,vy:0,air:false,finishTime:job.startTime,hitUntil:Infinity});s.status='racing';s.advance(1/60,{gas:false,brake:true});job.steps++;
   if(s.ai.every(a=>a.finishTime!==null)){job.done=true;break}
  }if(job.steps>=job.limit)job.done=true;
 }catch(e){job.error=e.message;job.done=true}return job.done;
}
function complete(job){
 const{result:r,s}=job,ai=job.tail?.ai||s.ai;
 const racers=[{id:0,name:r.name,character:s.character,finishTime:r.time,distance:s.total,status:'finished'},...ai.map(a=>({id:a.index+1,name:RaceCore.CHARACTERS[a.character].name,character:a.character,finishTime:a.finishTime,distance:a.s,status:a.finishTime===null?'dnf':'finished'}))];
 racers.sort((a,b)=>{if(a.finishTime===null&&b.finishTime===null)return b.distance-a.distance||b.id-a.id;if(a.finishTime===null)return 1;if(b.finishTime===null)return-1;return a.finishTime-b.finishTime||b.id-a.id});
 const order=racers.map(a=>a.id);if(new Set(order).size!==5||order.indexOf(0)+1!==r.position)throw Error('Urutan klasifikasi tidak konsisten dengan posisi pemain.');
 r.finishOrder=order;r.racers=racers;r.classification={version:1,method:'actual-finish-with-ai-continuation',complete:racers.every(a=>a.status==='finished'),steps:job.steps,tailSeconds:job.steps/60,dnf:racers.filter(a=>a.status==='dnf').map(a=>a.id),error:job.error};
 return{result:r,ghost:job.ghost};
}
async function finalize(s,progress=()=>{}){const job=start(s);while(!job.done){const end=performance.now()+6;do{advance(job,12)}while(!job.done&&performance.now()<end);progress((job.tail||s).ai.filter(a=>a.finishTime!==null).length,4);if(!job.done)await new Promise(resolve=>setTimeout(resolve,0))}return complete(job)}
root.BlokRayaClassification={start,advance,complete,finalize};
})(globalThis);
