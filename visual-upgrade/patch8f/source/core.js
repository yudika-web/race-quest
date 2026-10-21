(function(root){'use strict';
const clamp=(x,a,b)=>Math.max(a,Math.min(b,x)),mod=(x,n)=>(x%n+n)%n;
const copy=x=>JSON.parse(JSON.stringify(x));
const CHARACTERS=[
 {name:'Kucing',color:'Sport',file:'avatar_arka.webp',model:'kart_arka.glb'},
 {name:'Pinguin',color:'Kapsul',file:'avatar_nara.webp',model:'kart_nara.glb'},
 {name:'Beruang',color:'Buggy',file:'avatar_bimo.webp',model:'kart_bimo.glb'},
 {name:'Kelinci',color:'Formula',file:'avatar_sora.webp',model:'kart_sora.glb'},
 ...[['Bebek','bebek','Amfibi'],['Ayam','ayam','Farm Buggy'],['Domba','domba','Cloud Cruiser'],['Robot','robot','Photon'],['Anjing','anjing','Rally'],['Tikus','tikus','Mini Roadster'],['Rubah','rubah','GT'],['Panda','panda','Bamboo'],['Koala','koala','Eco Pod'],['Rakun','rakun','Trail Pickup']].map(([name,id,color])=>({name,color,file:'avatar_'+id+'.webp',model:'kart_'+id+'.glb'}))
];
const BUFFS={turbo:{name:'Turbo',duration:4,icon:'icon_turbo.webp',description:'Dorongan kecepatan selama 4 detik.'},shield:{name:'Perisai',duration:8,icon:'icon_shield.webp',description:'Menahan satu benturan, hingga 8 detik.'},magnet:{name:'Magnet',duration:7,icon:'icon_magnet.webp',description:'Menarik token di sekitar mobil selama 7 detik.'},bubble:{name:'Tembakan Gelembung',duration:0,icon:'icon_bubble.svg',description:'Tembak lurus ke depan; lawan yang terkena terkurung 2,4 detik.'},oil:{name:'Oli Licin',duration:0,icon:'icon_oil.svg',description:'Tinggalkan oli di belakang; lawan yang melintas tergelincir 2,8 detik.'}};
function uid(){return 'q_'+Date.now().toString(36)+'_'+Math.random().toString(36).slice(2,9)}
function validateQuestion(q){
 if(!q||typeof q!=='object')throw Error('Format soal tidak valid.');
 const text=String(q.text||'').trim(),options=Array.isArray(q.options)?q.options.map(v=>String(v??'').trim()):[];
 const correct=Number(q.correct);
 if(!text)throw Error('Pertanyaan belum diisi.');
 if(options.length!==4||options.some(v=>!v))throw Error('Isi keempat pilihan A, B, C, dan D.');
 if(q.correct===null||q.correct===''||!Number.isInteger(correct)||correct<0||correct>3)throw Error('Pilih satu kunci jawaban A–D.');
 return {id:String(q.id||uid()),text,options,correct,explanation:String(q.explanation||'').trim(),hint:String(q.hint||'').trim()};
}
function validateBank(b){
 if(!b||typeof b!=='object'||!Array.isArray(b.questions))throw Error('Bank soal tidak memiliki daftar soal.');
 const title=String(b.title||'').trim();if(!title)throw Error('Nama bank soal belum diisi.');
 const qs=b.questions.map(validateQuestion);const used=new Set();for(const q of qs){if(used.has(q.id))q.id=uid();used.add(q.id)}
 const settings=b.settings||{};
 return {id:String(b.id||uid()),title,subject:String(b.subject||'').trim(),material:String(b.material||'').trim(),className:String(b.className||'').trim(),questions:qs,settings:{count:qs.length?clamp(Math.floor(Number(settings.count)||5),1,qs.length):1,laps:clamp(Math.floor(Number(settings.laps)||3),1,5),difficulty:['easy','normal','hard'].includes(settings.difficulty)?settings.difficulty:'normal',shuffle:settings.shuffle!==false,feedback:settings.feedback!==false,autoGas:settings.autoGas!==false,stage:root.RaceStages.normalizeId(settings.stage),gpId:root.RaceStages.normalizeCup(settings.gpId),weather:['stage','clear','rain','fog'].includes(settings.weather)?settings.weather:'stage',mode:settings.mode==='gp'?'gp':'single',mastery:clamp(Number.isFinite(Number(settings.mastery))?Math.round(Number(settings.mastery)):60,0,100)}};
}
function normalizeData(data){
 if(!data||!Array.isArray(data.banks))throw Error('Berkas harus berisi daftar banks. Gunakan hasil ekspor BlokRaya atau RACE QUEST.');
 const banks=data.banks.map(validateBank);const used=new Set();for(const b of banks){if(used.has(b.id))b.id=uid();used.add(b.id)}
 return {version:1,banks,selectedBank:banks.some(b=>b.id===data.selectedBank)?data.selectedBank:(banks[0]?.id||''),profile:normalizeProfile(data.profile||{}),stageProgress:root.RaceStages.normalizeProgress(data.stageProgress,data.results),ghosts:validateGhosts(data.ghosts),results:Array.isArray(data.results)?data.results.filter(x=>x&&Array.isArray(x.records)&&typeof x.name==='string').slice(-50):[]};
}
function parseCSV(text){
 text=String(text).replace(/^\uFEFF/,'');const first=text.split(/\r?\n/)[0];const delimiter=first.includes(';')&&!first.includes(',')?';':',';
 let rows=[],row=[],cell='',quoted=false;
 for(let i=0;i<text.length;i++){
  const c=text[i];if(c==='"'){if(quoted&&text[i+1]==='"'){cell+='"';i++}else if(quoted||cell.length===0)quoted=!quoted;else cell+=c;}
  else if(c===delimiter&&!quoted){row.push(cell);cell=''}
  else if((c==='\n'||c==='\r')&&!quoted){if(c==='\r'&&text[i+1]==='\n')i++;row.push(cell);if(row.some(s=>s.trim()))rows.push(row);row=[];cell=''}
  else cell+=c;
 }
 if(quoted)throw Error('Tanda kutip CSV belum ditutup.');row.push(cell);if(row.some(s=>s.trim()))rows.push(row);
 if(rows.length<2)throw Error('CSV belum berisi soal.');
 const header=rows.shift().map(s=>s.trim().toLowerCase());
 for(const n of ['question','a','b','c','d','answer'])if(!header.includes(n))throw Error('Kolom CSV wajib: question,a,b,c,d,answer,explanation,hint.');
 const get=(r,n)=>r[header.indexOf(n)]||'';
 return rows.map((r,i)=>{let key=get(r,'answer').trim().toUpperCase();if(!/^[ABCD]$/.test(key))throw Error('Kunci pada baris '+(i+2)+' harus A, B, C, atau D.');return validateQuestion({text:get(r,'question'),options:['a','b','c','d'].map(n=>get(r,n)),correct:key.charCodeAt(0)-65,explanation:get(r,'explanation'),hint:get(r,'hint')})});
}
function csvCell(v){return '"'+String(v??'').replace(/"/g,'""')+'"'}
function questionsCSV(qs){return '\uFEFF'+[['question','a','b','c','d','answer','explanation','hint'],...qs.map(q=>[q.text,...q.options,String.fromCharCode(65+q.correct),q.explanation,q.hint])].map(r=>r.map(csvCell).join(',')).join('\r\n')}
function shuffled(items,rng=Math.random){let a=items.slice();for(let i=a.length-1;i>0;i--){let j=Math.floor(rng()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
function seedRandom(seed=109){return ()=>{seed|=0;seed=seed+0x6D2B79F5|0;let t=Math.imul(seed^seed>>>15,1|seed);t=t+Math.imul(t^t>>>7,61|t)^t;return ((t^t>>>14)>>>0)/4294967296}}

class Track{
 constructor(config='kampung'){
  this.config=typeof config==='string'?stageById(config):config;this.id=this.config.id;const pts=this.config.pts;this.obstacles=this.config.obstacles; 
  this.points=[];this.distances=[0];let total=0;
  for(let i=0;i<=550;i++){
   const t=i/550*pts.length,k=Math.floor(t),v=t-k;const get=n=>pts[mod(n,pts.length)];const a=get(k-1),b=get(k),c=get(k+1),d=get(k+2);
   const f=j=>.5*((2*b[j])+(-a[j]+c[j])*v+(2*a[j]-5*b[j]+4*c[j]-d[j])*v*v+(-a[j]+3*b[j]-3*c[j]+d[j])*v*v*v);
   const p={x:f(0),z:f(1),y:0};if(i){const prev=this.points[i-1];total+=Math.hypot(p.x-prev.x,p.z-prev.z);this.distances.push(total)}this.points.push(p);
  }
  this.length=total;
  // Periodic, smooth hills: bridge approach and two longer climbing sections.
  // A raised cosine joins level ground without a sudden change of slope.
  this.points.forEach((p,i)=>{const u=this.distances[i]/total;const hill=(center,width,height,flat=0)=>{const d=Math.max(0,Math.min(Math.abs(u-center),1-Math.abs(u-center))-flat);return d<width?height*.5*(1+Math.cos(Math.PI*d/width)):0};p.y=this.config.hills.reduce((sum,a)=>sum+hill(...a),0)});
  this.points.forEach((p,i)=>{const a=this.points[mod(i-1,550)],b=this.points[(i+1)%550];p.yaw=Math.atan2(b.x-a.x,b.z-a.z)});this.points[550].yaw=this.points[0].yaw;
 }
 point(distance){
  const s=mod(distance,this.length);let lo=0,hi=this.distances.length-1;
  while(hi-lo>1){const mid=(lo+hi)>>1;if(this.distances[mid]>s)hi=mid;else lo=mid}
  const a=this.points[lo],b=this.points[hi],t=(s-this.distances[lo])/(this.distances[hi]-this.distances[lo]||1);
  const yaw=a.yaw+Math.atan2(Math.sin(b.yaw-a.yaw),Math.cos(b.yaw-a.yaw))*t;
  return {x:a.x+(b.x-a.x)*t,y:a.y+(b.y-a.y)*t,z:a.z+(b.z-a.z)*t,yaw,rightX:Math.cos(yaw),rightZ:-Math.sin(yaw)};
 }
 curvature(s){let a=this.point(s-1.5).yaw,b=this.point(s+1.5).yaw;return Math.atan2(Math.sin(b-a),Math.cos(b-a))/3}
 grade(s){return (this.point(s+1).y-this.point(s-1).y)/2}
 place(s,lateral=0){const p=this.point(s);p.x+=p.rightX*lateral;p.z+=p.rightZ*lateral;return p}
}

class BaseSession{
 constructor(bank,{name='Pembalap',character=0,rng=Math.random,stageProgress={}}={}){
  this.bank=validateBank(copy(bank));if(!this.bank.questions.length)throw Error('Tambahkan minimal satu soal sebelum balapan.');
  this.settings=copy(this.bank.settings);root.RaceStages.requireStage(this.settings.stage,stageProgress);this.rng=rng;this.track=new Track(this.settings.stage);this.total=this.track.length*this.settings.laps;
  const all=this.settings.shuffle?shuffled(this.bank.questions,rng):this.bank.questions;
  this.questions=all.slice(0,this.settings.count);this.name=String(name||'Pembalap').trim()||'Pembalap';this.character=clamp(character|0,0,CHARACTERS.length-1);
  this.status='countdown';this.countdown=3;this.elapsed=0;this.player={s:0,lateral:0,speed:0,error:0,steering:0};this.ai=Array.from({length:4},(_,i)=>({s:-3-i*2.8,lateral:i%2?1.8:-1.8,baseLateral:i%2?1.8:-1.8,speed:0,finishTime:null,character:(i+1+this.character)%CHARACTERS.length,index:i,bubble:0,slip:0}));
  this.records=[];this.slot=null;this.buffs={turbo:0,shield:0,magnet:0};this.bubbles=[];this.oils=[];this.impactSerial=0;this.lastImpact=null;this.tokens=0;this.collected=new Set();this.collisionCooldown=0;this.questionHint=false;this.lastEvent=null;
 }
 get count(){return this.questions.length}
 get question(){return this.questions[this.records.length]||null}
 get correct(){return this.records.filter(r=>r.correct).length}
 get score(){return Math.round(this.correct/this.count*100)}
 get nextGate(){return (this.records.length+1)/(this.count+1)*this.total}
 get rank(){if(this.status==='finished')return 1+this.ai.filter(a=>a.finishTime!==null&&a.finishTime<=this.elapsed).length;return 1+this.ai.filter(a=>a.s>this.player.s).length}
 countdownStep(dt){if(this.status!=='countdown')return;this.countdown=Math.max(0,this.countdown-dt);if(!this.countdown)this.status='racing'}
 pause(){if(!['racing','countdown'].includes(this.status))return false;this.previousStatus=this.status;this.status='paused';return true}
 continue(){if(!['paused','feedback'].includes(this.status))return false;this.status='countdown';this.countdown=3;return true}
 useItem(){
  if(this.status!=='racing'||!this.slot||!BUFFS[this.slot])return null;const item=this.slot;this.slot=null;
  if(item==='bubble'){if(this.bubbles.length>=8)this.bubbles.shift();this.bubbles.push({s:this.player.s+.9,lateral:this.player.lateral,speed:Math.max(34,this.player.speed+22),ttl:4})}
  else if(item==='oil'){if(this.oils.length>=8)this.oils.shift();this.oils.push({s:this.player.s-2.2,lateral:this.player.lateral,ttl:10,hits:[]})}
  else this.buffs[item]=BUFFS[item].duration;this.lastEvent={type:'item',item};return item;
 }
 hint(){if(this.status==='question')this.questionHint=true;return this.question?.hint||''}
 answer(selected){
  if(this.status!=='question'||!this.question)return null;if(!Number.isInteger(selected)||selected<0||selected>3)throw Error('Pilihan jawaban tidak valid.');
  const q=this.question,ok=selected===q.correct,keys=Object.keys(BUFFS);const buff=ok?keys[Math.min(keys.length-1,Math.floor(this.rng()*keys.length))]:null;
  const r={questionId:q.id,text:q.text,options:copy(q.options),correctIndex:q.correct,selectedIndex:selected,correct:ok,explanation:q.explanation,hintUsed:this.questionHint,buff};this.records.push(r);this.questionHint=false;
  if(buff)this.slot=buff;this.status='feedback';this.lastEvent={type:'answer',correct:ok,buff};return r;
 }
 advance(dt,input={}){
  if(this.status!=='racing')return null;dt=clamp(dt,0,.05);this.previousPlayer={...this.player};this.previousAI=this.ai.map(a=>({...a}));this.elapsed+=dt;for(let k in this.buffs)this.buffs[k]=Math.max(0,this.buffs[k]-dt);this.collisionCooldown=Math.max(0,this.collisionCooldown-dt);
  const p=this.player,gas=this.settings.autoGas||input.gas,brake=!!input.brake,steer=clamp(Number(input.steer)||0,-1,1);let accel=gas?6.8:-2.2;
  if(brake)accel-=14;const offroad=Math.abs(p.lateral)>5;if(offroad)accel-=5;accel-=8.5*this.track.grade(p.s);
  const max=p.bubble>0?3:p.slip>0?(this.buffs.grip>0?14:8):(this.buffs.turbo>0||this.buffs.nitro>0)?31:23;p.speed=clamp(p.speed+accel*dt,0,max);if(offroad)p.speed=Math.min(p.speed,11);
  p.steering+=(steer-p.steering)*(1-Math.exp(-12*dt));
  // The chase camera looks along +Z: positive world yaw projects left.
  // Positive input means the driver's right, so steering reduces world yaw.
  const turn=-p.steering*(.38+.34*p.speed/23);p.error+=(turn-this.track.curvature(p.s)*p.speed)*dt;if(!steer)p.error*=Math.exp(-1.6*dt);else p.error*=Math.exp(-.45*dt);p.error=clamp(p.error,-.62,.62);
  p.lateral+=Math.sin(p.error)*p.speed*dt;p.s+=Math.cos(p.error)*p.speed*dt;
  let event=null;
  if(Math.abs(p.lateral)>6.2&&this.collisionCooldown===0){p.lateral=clamp(p.lateral,-6.2,6.2);p.error*=-.35;if(this.buffs.shield>0)this.buffs.shield=0;else p.speed*=.55;this.collisionCooldown=.8;event={type:'collision'}}
  const lap=Math.floor(p.s/this.track.length),local=mod(p.s,this.track.length),spacing=this.track.length/22;
  for(let i=0;i<22;i++){
   const pos=(i+.5)*spacing,lateral=i%2?2.4:-2.4,key=lap*22+i;
   if(!this.collected.has(key)&&Math.abs(local-pos)<(this.buffs.magnet>0?4:1.7)&&Math.abs(p.lateral-lateral)<(this.buffs.magnet>0?8:1.5)){this.collected.add(key);this.tokens++;event={type:'token'}}
  }
  if(this.records.length<this.count&&p.s>=this.nextGate){this.status='question';this.questionHint=false;event={type:'question'};}
  else if(p.s>=this.total){p.s=this.total;this.status='finished';event={type:'finish'};}
  this.lastEvent=event;return event;
 }
 result(){return {id:uid(),date:new Date().toISOString(),name:this.name,bankTitle:this.bank.title,subject:this.bank.subject,material:this.bank.material,className:this.bank.className,character:this.character,position:this.rank,time:this.elapsed,score:this.score,correct:this.correct,count:this.count,tokens:this.tokens,records:copy(this.records)}}
}
const AI_LEVELS={easy:{pace:16.5,mistake:.12,slowWhenAhead:.10,catchUp:0,dodge:0,itemUse:0,overtake:false},normal:{pace:21.9,mistake:.05,slowWhenAhead:.04,catchUp:.05,dodge:.5,itemUse:.35,overtake:true},hard:{pace:22.6,mistake:.015,slowWhenAhead:0,catchUp:.10,dodge:.9,itemUse:.8,overtake:true}};
const STAGES=[
{id:'kampung',name:'Pontianak · Jalanan Kota',seed:28106,weather:'clear',pts:[[0,0],[0,65],[32,100],[90,88],[125,40],[108,-15],[130,-75],[85,-118],[20,-110],[-40,-65],[-45,-10]],hills:[[.075,.05,2.2,.018],[.32,.12,7.5],[.77,.115,5.8]],palette:{grass:[.8,1,.8],water:[.035,.32,.48],road:[1,1,1],fog:[.43,.70,.78]},obstacles:[{u:.19,lateral:-2.4,type:'rock'},{u:.43,lateral:1.8,type:'log'},{u:.68,lateral:-1.6,type:'rock'}],ramps:[.54],gaps:[]},
{id:'kapuas',name:'Mempawah · Jalanan Taman',seed:47114,weather:'rain',pts:[[0,0],[-10,65],[26,104],[78,105],[115,62],[85,12],[122,-38],[97,-100],[38,-124],[-23,-90],[-54,-34]],hills:[[.075,.05,2.2,.018],[.29,.09,3.8],[.63,.11,4.6]],palette:{grass:[.55,.83,.65],water:[.065,.29,.30],road:[.77,.84,.88],fog:[.43,.58,.62]},obstacles:[{u:.23,lateral:2,type:'log'},{u:.47,lateral:-2.4,type:'rock'},{u:.81,lateral:0,type:'log'}],ramps:[.675],gaps:[{u:.69,length:5}]},
{id:'hutan',name:'Singkawang · Pantai Meriah',seed:8391,weather:'clear',pts:[[0,0],[18,57],[-18,104],[38,125],[100,95],[119,31],[83,-10],[119,-63],[68,-114],[10,-101],[-49,-63],[-31,-12]],hills:[[.075,.05,2.2,.018],[.36,.10,9],[.48,.045,3,.012],[.73,.10,7]],palette:{grass:[.36,.66,.43],water:[.04,.20,.23],road:[.70,.79,.70],fog:[.35,.49,.44]},obstacles:[{u:.18,lateral:0,type:'log'},{u:.40,lateral:-2,type:'rock'},{u:.60,lateral:2,type:'log'},{u:.85,lateral:0,type:'rock'}],ramps:[.465],gaps:[{u:.48,length:5}]}
];
function stageById(id){if(root.RaceStages?.get(id))return root.RaceStages.track(id);return STAGES.find(x=>x.id===id)||STAGES[0]}
function localDay(){const d=new Date();return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')}
function normalizeProfile(p={}){const n={tokens:0,xp:0,races:0,wins:0,correct:0,unlocked:[0,1,2,3],paints:['original'],paint:'original',achievements:[]};for(const k of ['tokens','xp','races','wins','correct'])n[k]=clamp(Math.floor(Number(p[k])||0),0,1e8);n.unlocked=[...new Set([...n.unlocked,...(Array.isArray(p.unlocked)?p.unlocked.filter(i=>Number.isInteger(i)&&i>=0&&i<14):[])])];n.paints=[...new Set([...n.paints,...(Array.isArray(p.paints)?p.paints.filter(x=>['mint','sunset','violet'].includes(x)):[])])];n.paint=n.paints.includes(p.paint)?p.paint:'original';n.daily={date:localDay(),correct:p.daily?.date===localDay()?clamp(Number(p.daily.correct)||0,0,10000):0,claimed:p.daily?.date===localDay()&&!!p.daily.claimed};n.rewardReceipts=Array.isArray(p.rewardReceipts)?[...new Set(p.rewardReceipts.filter(x=>typeof x==='string'&&x.length<=160))].slice(-256):[];n.achievements=Array.isArray(p.achievements)?p.achievements.filter(x=>['first','scholar','champion','collector'].includes(x)):[];return n}
function awardProfile(profile,r){const p=normalizeProfile(profile);if(r.id&&p.rewardReceipts.includes(r.id))return {profile:p,earned:0,duplicate:true};if(r.id)p.rewardReceipts=[...p.rewardReceipts,r.id].slice(-256);let earned=r.tokens+10+(r.position===1?15:0);p.tokens+=earned;p.xp+=r.correct*15+20+(r.position===1?25:0);p.races++;p.wins+=r.position===1?1:0;p.correct+=r.correct;p.daily.correct+=r.correct;if(p.daily.correct>=10&&!p.daily.claimed){p.daily.claimed=true;p.tokens+=30;p.xp+=50;earned+=30}for(const [id,ok] of [['first',p.races>0],['scholar',p.correct>=50],['champion',p.wins>=5],['collector',p.tokens>=200]])if(ok&&!p.achievements.includes(id))p.achievements.push(id);return {profile:p,earned}}
function purchase(profile,type,id){const p=normalizeProfile(profile),cost=type==='character'?60:40;if(type==='character'){if(!Number.isInteger(id)||id<4||id>=14)throw Error('Karakter tidak valid.');if(p.unlocked.includes(id))return p}else if(type==='paint'){if(!['mint','sunset','violet'].includes(id))throw Error('Warna tidak valid.');if(p.paints.includes(id))return p}else throw Error('Pilihan tidak valid.');if(p.tokens<cost)throw Error('Token belum cukup. Selesaikan balapan untuk mengumpulkannya.');p.tokens-=cost;if(type==='character')p.unlocked.push(id);else p.paints.push(id);return p}
function analyzeResults(results,bankId,className=''){const map=new Map();for(const r of results){if(bankId&&r.bankId!==bankId||className&&r.className!==className)continue;for(const q of r.records||[]){const key=JSON.stringify([q.questionId,q.text,q.options,q.correctIndex]);if(!map.has(key))map.set(key,{id:q.questionId,text:q.text,attempts:0,correct:0,hints:0,choices:[0,0,0,0]});const a=map.get(key);a.attempts++;a.correct+=q.correct?1:0;a.hints+=q.hintUsed?1:0;if(q.selectedIndex>=0&&q.selectedIndex<4)a.choices[q.selectedIndex]++}}return [...map.values()].map(a=>({...a,percent:Math.round(a.correct/a.attempts*100)})).sort((a,b)=>a.percent-b.percent||b.attempts-a.attempts)}
// Pure points/assessment sequence: no world construction or availability override.
class GrandPrixSequence{
 constructor(threshold=60,stageIds){if(!Array.isArray(stageIds)||!stageIds.length||new Set(stageIds).size!==stageIds.length)throw Error('Urutan ronde tidak valid.');this.stageIds=stageIds.slice();this.threshold=clamp(Number(threshold)||0,0,100);this.round=0;this.results=[];this.points=[0,0,0,0,0];this.wins=[0,0,0,0,0];this.blocked=false;this.complete=false}
 get totalRounds(){return this.stageIds.length}
 get stageId(){return this.stageIds[this.round]}
 accept(result){if(this.complete||this.blocked||this.results.length!==this.round)throw Error('Putaran sudah dicatat.');if(!Number.isFinite(result.score)||result.score<0||result.score>100)throw Error('Skor asesmen tidak valid.');if(result.stage&&result.stage!==this.stageId)throw Error('Hasil bukan untuk ronde yang aktif.');const order=result.finishOrder||[0,1,2,3,4];if(order.length!==5||new Set(order).size!==5||order.some(id=>!Number.isInteger(id)||id<0||id>4))throw Error('Urutan finis tidak valid.');order.forEach((id,i)=>{this.points[id]+=[25,18,15,12,10][i];if(i===0)this.wins[id]++});this.results.push(copy(result));this.blocked=result.score<this.threshold;this.complete=this.round===this.totalRounds-1&&!this.blocked}
 next(){if(this.blocked||this.complete||this.results.length!==this.round+1)return false;this.round++;return true}
 retry(){if(!this.blocked)return false;const r=this.results.pop();(r.finishOrder||[0,1,2,3,4]).forEach((id,i)=>{this.points[id]-=[25,18,15,12,10][i];if(i===0)this.wins[id]--});this.blocked=false;return true}
 standings(){return this.points.map((points,id)=>({id,points,wins:this.wins[id]})).sort((a,b)=>b.points-a.points||b.wins-a.wins||a.id-b.id)}
 summary(){return this.results.map((r,i)=>({round:i+1,stage:this.stageIds[i],position:r.position??(r.finishOrder||[0,1,2,3,4]).indexOf(0)+1,score:r.score,finishOrder:r.finishOrder||[0,1,2,3,4]}))}
}
class GrandPrix extends GrandPrixSequence{
 constructor(threshold=60,cupId='kalbar-klasik',progress={}){super(threshold,root.RaceStages.requireCup(cupId,progress));this.cupId=cupId;this.label=root.RaceStages.cup(cupId).displayName}
 get stage(){return stageById(this.stageId)}
}
function ghostKey(s){return [s.stage,s.laps,s.difficulty,s.weather,s.count].join(':')}
function validateGhost(g){if(!g||!Array.isArray(g.samples)||g.samples.length<2||g.samples.length>15000||typeof g.key!=='string'||!Number.isFinite(g.time)||g.time<=0||g.time>1500)return null;let t=-1;for(const a of g.samples){if(!Array.isArray(a)||a.length!==5||a.some(v=>!Number.isFinite(v))||a[0]<=t||a[0]<0||Math.abs(a[2])>7||a[3]<0||a[3]>10)return null;t=a[0]}return {key:g.key,time:g.time,character:clamp(g.character|0,0,13),name:String(g.name||'Ghost').slice(0,60),samples:g.samples}}
function validateGhosts(gs){return (Array.isArray(gs)?gs:[]).map(validateGhost).filter(Boolean).slice(-6)}
function ghostPose(g,t){if(!g||t<0||t>g.time)return null;const a=g.samples;let lo=0,hi=a.length-1;while(hi-lo>1){let m=(lo+hi)>>1;if(a[m][0]>t)hi=m;else lo=m}const x=a[lo],y=a[hi],f=clamp((t-x[0])/(y[0]-x[0]||1),0,1);return {s:x[1]+(y[1]-x[1])*f,lateral:x[2]+(y[2]-x[2])*f,y:x[3]+(y[3]-x[3])*f,error:x[4]+(y[4]-x[4])*f}}
class Session extends BaseSession{
 constructor(bank,options={}){super(bank,options);this.total=this.track.length*this.settings.laps;this.weather=this.settings.weather==='stage'?this.track.config.weather:this.settings.weather;Object.assign(this.player,{lateral:1.8,y:0,vy:0,air:false,bubble:0,slip:0,driftCharge:0,drifting:false});const form=.90+this.rng()*.20;this.ai.forEach((a,i)=>Object.assign(a,{s:4+(3-i)*3,personality:['agresif','stabil','licin','penyalip'][i],skill:form*(.92+this.rng()*.16),think:this.rng()*.3,targetLateral:a.lateral,mistakeTime:0,itemTimer:7+this.rng()*8,item:null,y:0}));this.combo=0;this.jumpHeld=false;this.landingTurboCooldown=0;this.obstacleCooldown=0;this.lapTimes=[];this.lapStarted=0;this.samples=[[0,0,1.8,0,0]];this.sampleNext=.1;this.startGasHeld=false;this.startBoost=false;this.ghost=options.ghost?.key===ghostKey(this.settings)?validateGhost(options.ghost):null}
 countdownStep(dt,input={}){if(this.status!=='countdown')return;if(this.elapsed===0&&input.gas&&!this.startGasHeld&&this.countdown<=.24)this.startBoost=true;this.startGasHeld=!!input.gas;super.countdownStep(dt);if(this.status==='racing'&&this.elapsed===0&&this.startBoost)this.buffs.turbo=1.1}
 useItem(){const k=super.useItem();if(k==='bubble')this.bubbles.at(-1).owner='player';if(k==='oil')this.oils.at(-1).owner='player';return k}
 answer(index){const r=super.answer(index);if(r){this.combo=r.correct?this.combo+1:0;if(this.combo&&this.combo%3===0)this.buffs.turbo=Math.max(this.buffs.turbo,2)}return r}
 reset(){if(this.status!=='racing')return false;Object.assign(this.player,{lateral:0,error:0,steering:0,speed:Math.min(6,this.player.speed),y:0,vy:0,air:false});this.previousPlayer={...this.player};this.collisionCooldown=1;return true}
 launch(v=9.5){if(this.player.air)return false;this.player.air=true;this.player.vy=v;return true}
 spawnItem(item,owner,lateral,s,speed){if(item==='bubble'){if(this.bubbles.length>=8)this.bubbles.shift();this.bubbles.push({owner,s:s+.9,lateral,speed:Math.max(34,speed+22),ttl:4})}else{if(this.oils.length>=8)this.oils.shift();this.oils.push({owner,s:s-2.2,lateral,ttl:10,hits:[]})}}
 hit(target,item){const isPlayer=target===this.player;if(isPlayer&&this.settings.difficulty==='easy')return null;if(isPlayer&&this.buffs.shield>0){this.buffs.shield=0;this.lastImpact={serial:++this.impactSerial,item:'shield',s:target.s,lateral:target.lateral};return {type:'blocked',item,target:'player'}}target[item==='bubble'?'bubble':'slip']=item==='bubble'?2.4:2.8;target.speed=Math.min(target.speed,item==='bubble'?3:8);this.lastImpact={serial:++this.impactSerial,item,s:target.s,lateral:target.lateral};return {type:'attackHit',item,target:isPlayer?'player':target.index}}
 advanceAI(dt){const level=AI_LEVELS[this.settings.difficulty],p=this.player;for(const a of this.ai){if(a.finishTime!==null)continue;for(const k of ['bubble','slip','mistakeTime'])a[k]=Math.max(0,a[k]-dt);a.think-=dt;a.itemTimer-=dt;const curv=this.track.curvature(a.s+7),curve=Math.abs(curv),gap=a.s-p.s;
  if(a.think<=0){const interval=.35+this.rng()*.3;a.think=interval;let lane=level.overtake?clamp(curv*75,-2.5,2.5):a.baseLateral;const ahead=[p,...this.ai.filter(b=>b!==a&&b.finishTime===null)].filter(b=>b.s>a.s&&b.s-a.s<12&&Math.abs(b.lateral-a.lateral)<1.6),hazards=[...this.oils.filter(o=>o.owner!==a.index&&o.s>a.s&&o.s-a.s<12),...this.track.obstacles.map(o=>({s:Math.floor(a.s/this.track.length)*this.track.length+o.u*this.track.length,lateral:o.lateral})).filter(o=>o.s>a.s&&o.s-a.s<12)];if(level.overtake&&ahead.length||hazards.some(o=>Math.abs(o.lateral-a.lateral)<1.8)){if(this.rng()<level.dodge)lane=[-3.2,0,3.2].map(l=>({l,cost:[...ahead,...hazards].reduce((n,b)=>n+(Math.abs(b.lateral-l)<1.7?10:0),0)+Math.abs(l-lane)*.1})).sort((x,y)=>x.cost-y.cost)[0].l;else if(ahead.length)a.blocked=.7}a.targetLateral=lane;if(curve>.013&&this.rng()<level.mistake*interval*(a.personality==='stabil'?.5:1.4))a.mistakeTime=.5}
  a.blocked=Math.max(0,(a.blocked||0)-dt);a.lateral+=(a.targetLateral-a.lateral)*(1-Math.exp(-dt*(a.personality==='licin'?3.2:2.2)));if(a.slip>0)a.lateral=clamp(a.lateral+Math.sin(this.elapsed*11+a.index)*dt*1.8,-4.1,4.1);let target=level.pace*a.skill*(1-Math.min(.14,curve*2.7))-this.track.grade(a.s)*6;if(gap>30)target*=1-level.slowWhenAhead*clamp((gap-30)/90,0,1);else if(gap< -25)target*=1+level.catchUp*clamp((-gap-25)/90,0,1);if(a.blocked>0)target=Math.min(target,p.speed*.96+1);if(a.mistakeTime>0)target*=.60;if(a.bubble>0)target=3;else if(a.slip>0)target=8;a.speed+=clamp(target-a.speed,(a.bubble>0||a.slip>0?-30:-12)*dt,6*dt);a.s+=Math.max(0,a.speed)*dt;
  if(a.itemTimer<=0){a.item=this.rng()<(a.personality==='licin'?.7:.35)?'oil':'bubble';a.itemTimer=6+this.rng()*8}if(a.item&&level.itemUse>0){const ds=p.s-a.s,aligned=Math.abs(p.lateral-a.lateral)<1.5,ready=a.item==='bubble'?ds>2&&ds<28:ds< -2&&ds> -22;if(ready&&aligned&&this.rng()<dt*level.itemUse*(a.personality==='agresif'?1.5:1)){this.spawnItem(a.item,a.index,a.lateral,a.s,a.speed);a.item=null}}a.y=0;for(const ramp of this.track.config.ramps){const d=mod(a.s-ramp*this.track.length,this.track.length);if(d<17&&a.speed>8)a.y=Math.sin(d/17*Math.PI)*1.8}if(a.s>=this.total){a.s=this.total;a.finishTime=this.elapsed}
 }}
 advance(dt,input={}){if(this.status!=='racing')return null;dt=clamp(dt,0,.05);if(!dt)return null;const p=this.player,previous={...p},previousAI=this.ai.map(a=>({...a}));let event=null;this.landingTurboCooldown=Math.max(0,this.landingTurboCooldown-dt);this.obstacleCooldown=Math.max(0,this.obstacleCooldown-dt);if(input.jump&&!this.jumpHeld&&this.launch())event={type:'jump'};this.jumpHeld=!!input.jump;if(p.air){p.vy-=26*dt;p.y+=p.vy*dt;if(p.y<=0){p.y=0;p.vy=0;p.air=false;const smooth=Math.abs(p.error)<.22&&Math.abs(p.lateral)<4.6;if(smooth&&this.landingTurboCooldown===0&&p.speed>8){this.buffs.turbo=Math.max(.7,this.buffs.turbo);this.landingTurboCooldown=2.2}else if(!smooth)p.speed*=.75;event={type:'land',smooth}}}
  for(const k of ['bubble','slip'])p[k]=Math.max(0,p[k]-dt);const cap=p.bubble>0?3:p.slip>0?(this.buffs.grip>0?14:8):Infinity;p.speed=Math.min(p.speed,cap);const drifting=!!input.drift&&!p.air&&p.speed>10&&Math.abs(input.steer||0)>.2;if(drifting)p.driftCharge=Math.min(2,p.driftCharge+dt*Math.abs(input.steer));else if(p.drifting){if(p.driftCharge>=.65){this.buffs.turbo=Math.max(this.buffs.turbo,1.1);event={type:'driftBoost'}}p.driftCharge=0}p.drifting=drifting;
  // Road physics advances once; owned projectiles, AI and hits share this step.
  const ai=this.ai,oldBubbles=this.bubbles.slice();let baseEvent=super.advance(dt,{...input,steer:(Number(input.steer)||0)*(p.air?.35:this.weather==='rain'?(this.buffs.grip>0?.94:.78):1)*(drifting?1.15:1)});this.previousAI=previousAI;for(const b of this.bubbles){b.s+=b.speed*dt;b.ttl-=dt}this.bubbles=this.bubbles.filter(b=>b.ttl>0);for(const o of this.oils)o.ttl-=dt;this.oils=this.oils.filter(o=>o.ttl>0);
  this.previousPlayer=previous;p.speed=Math.min(p.speed,cap);if(p.slip>0)p.error=clamp(p.error+Math.sin(this.elapsed*13)*dt*.9*(this.buffs.grip>0?.3:1),-.62,.62);if(baseEvent)event=baseEvent;if(p.air&&['question','finished'].includes(this.status)){this.status='racing';event=null}
  for(let lap=Math.floor(previous.s/this.track.length);lap<=Math.floor(p.s/this.track.length);lap++){for(const u of this.track.config.ramps){const s=(lap+u)*this.track.length;if(previous.s<s&&p.s>=s&&!p.air&&p.speed>8){this.launch(10.5);event={type:'jump',ramp:true}}}for(const o of this.track.obstacles){const s=(lap+o.u)*this.track.length;if(previous.s<s&&p.s>=s&&Math.abs(p.lateral-o.lateral)<1.5&&p.y<.7&&this.obstacleCooldown===0){p.speed*=.38;this.obstacleCooldown=1;this.collisionCooldown=.7;event={type:'obstacle'}}}for(const g of this.track.config.gaps){const s=(lap+g.u)*this.track.length;if(previous.s<s&&p.s>=s&&p.y<.35&&this.obstacleCooldown===0){p.s=s+g.length/2+1;p.speed=3;p.error=0;this.obstacleCooldown=2;this.collisionCooldown=.8;event={type:'rescue'}}}}
  this.advanceAI(dt);const racers=[{r:p,id:'player',prev:previous},...ai.map((r,i)=>({r,id:i,prev:previousAI[i]}))];for(const b of oldBubbles){const before=b.s-b.speed*dt,hit=racers.filter(x=>x.id!==(b.owner??'player')&&x.r.finishTime==null&&!(x.id==='player'&&this.settings.difficulty==='easy')&&x.r.y<.75&&Math.abs(x.r.lateral-b.lateral)<1.25&&Math.max(before-x.prev.s,b.s-x.r.s)>=-.7&&Math.min(before-x.prev.s,b.s-x.r.s)<=.7).sort((x,y)=>x.r.s-y.r.s)[0];if(hit){event=this.hit(hit.r,'bubble',b.owner)||event;b.ttl=0}}this.bubbles=this.bubbles.filter(b=>b.ttl>0);for(const o of this.oils)for(const x of racers){const r=x.r;if(x.id===(o.owner??'player')||r.finishTime!=null||o.hits.includes(x.id)||x.id==='player'&&this.settings.difficulty==='easy'||r.y>.55||Math.abs(r.lateral-o.lateral)>1.35||x.prev.s>o.s+2.1||r.s<o.s-2.1)continue;o.hits.push(x.id);event=this.hit(r,'oil',o.owner)||event}
  if(this.collisionCooldown===0&&!p.air){const other=ai.find(a=>a.finishTime===null&&Math.abs(a.s-p.s)<1.35&&Math.abs(a.lateral-p.lateral)<1.15);if(other){if(this.buffs.shield>0)this.buffs.shield=0;else p.speed*=.82;other.speed*=.94;p.lateral=clamp(p.lateral+(p.lateral>=other.lateral?.35:-.35),-6.2,6.2);this.collisionCooldown=.65;event={type:'collision'}}}
  while(this.lapTimes.length<this.settings.laps&&p.s>=(this.lapTimes.length+1)*this.track.length){const boundary=(this.lapTimes.length+1)*this.track.length,f=clamp((boundary-previous.s)/(p.s-previous.s||1),0,1),time=this.elapsed-dt+dt*f;this.lapTimes.push(time-this.lapStarted);this.lapStarted=time}if(this.elapsed>=this.sampleNext&&this.samples.length<15000){this.samples.push([+this.elapsed.toFixed(3),+p.s.toFixed(2),+p.lateral.toFixed(3),+p.y.toFixed(3),+p.error.toFixed(3)]);this.sampleNext=this.elapsed+.1}
  if(p.air&&['question','finished'].includes(this.status)){this.status='racing';event=null}if(this.records.length<this.count&&p.s>=this.nextGate&&!p.air){this.status='question';event={type:'question'}}else if(p.s>=this.total&&!p.air&&this.records.length===this.count){p.s=this.total;this.status='finished';const end=[+this.elapsed.toFixed(3),this.total,+p.lateral.toFixed(3),0,+p.error.toFixed(3)];if(this.samples.at(-1)[0]<end[0]&&this.samples.length<15000)this.samples.push(end);else this.samples[this.samples.length-1]=end;event={type:'finish'}}this.lastEvent=event;return event;
 }
 ghostResult(){return this.elapsed>1500?null:{key:ghostKey(this.settings),time:this.elapsed,name:this.name,character:this.character,samples:copy(this.samples)}}
 result(){const r=super.result(),order=this.ai.map(a=>({id:a.index+1,time:a.finishTime??this.elapsed+(this.total-a.s)/23}));order.push({id:0,time:this.elapsed});order.sort((a,b)=>a.time-b.time||b.id-a.id);return {...r,bankId:this.bank.id,stage:this.settings.stage,stageName:this.track.config.name,difficulty:this.settings.difficulty,weather:this.weather,laps:this.settings.laps,lapTimes:copy(this.lapTimes),finishOrder:order.map(x=>x.id)}}
}

function sampleData(){
 const items=[['Hasil 7 × 8 adalah …',['48','54','56','64'],2,'Tujuh kelompok berisi delapan menghasilkan 56.'],['Satu jam sama dengan … menit.',['30','45','60','90'],2,'Satu jam terdiri atas 60 menit.'],['Planet tempat manusia tinggal adalah …',['Mars','Bumi','Venus','Jupiter'],1,'Kita tinggal di planet Bumi.'],['Hasil 144 ÷ 12 adalah …',['10','11','12','14'],2,'12 × 12 = 144.'],['Bilangan genap di antara pilihan berikut adalah …',['13','17','21','24'],3,'Bilangan genap dapat dibagi dua tanpa sisa.'],['Jika waktu mulai 08.00 dan selesai 08.30, durasinya …',['15 menit','20 menit','30 menit','60 menit'],2,'Selisih waktu tersebut adalah 30 menit.'],['Sisi pada sebuah segitiga berjumlah …',['2','3','4','5'],1,'Segitiga memiliki tiga sisi.'],['Hasil penjumlahan 125 + 75 adalah …',['175','190','200','225'],2,'125 + 75 = 200.'],['Kata yang bermakna berlawanan dengan “cepat” adalah …',['Laju','Segera','Lambat','Kencang'],2,'Lambat merupakan lawan kata cepat.'],['Dalam satu minggu terdapat … hari.',['5','6','7','8'],2,'Satu minggu terdiri atas tujuh hari.']];
 const bank=validateBank({id:'sample_bank',title:'Contoh — Pengetahuan Umum',subject:'Latihan',material:'Contoh soal untuk mencoba permainan',className:'SMP',settings:{count:5,laps:3,difficulty:'easy',shuffle:true,feedback:true,autoGas:true},questions:items.map((a,i)=>({id:'sample_'+i,text:a[0],options:a[1],correct:a[2],explanation:a[3],hint:''}))});return {version:1,banks:[bank],selectedBank:bank.id,results:[],profile:normalizeProfile(),ghosts:[]};
}
root.RaceCore={clamp,mod,copy,BUFFS,CHARACTERS,AI_LEVELS,STAGES,stageById,normalizeProfile,awardProfile,purchase,analyzeResults,GrandPrix,GrandPrixSequence,ghostKey,validateGhost,validateGhosts,ghostPose,uid,validateQuestion,validateBank,normalizeData,parseCSV,questionsCSV,csvCell,shuffled,seedRandom,Track,Session,sampleData};
if(typeof module!=='undefined'&&module.exports)module.exports=root.RaceCore;
})(typeof globalThis!=='undefined'?globalThis:this);
