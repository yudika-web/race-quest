(function(root){'use strict';
const clone=v=>JSON.parse(JSON.stringify(v)),finite=(v,min=0,max=1e8)=>Math.max(min,Math.min(max,Number(v)||0));
class StageRegistry{
 constructor(catalog,cups){this.catalog=Object.freeze(catalog.map(v=>Object.freeze(clone(v))));this.cups=Object.freeze(cups.map(v=>Object.freeze(clone(v))));this.runtime=new Map();if(new Set(catalog.map(x=>x.id)).size!==catalog.length||new Set(cups.map(x=>x.id)).size!==cups.length)throw Error('ID katalog harus unik.');for(const c of cups)if(!c.stageIds.length||new Set(c.stageIds).size!==c.stageIds.length||c.stageIds.some(id=>!this.get(id)))throw Error('Urutan Grand Prix tidak valid.')}
 get(id){return this.catalog.find(x=>x.id===id)||null}
 normalizeId(id){return this.get(id)?.id||this.catalog[0].id}
 cup(id='kalbar-klasik'){return this.cups.find(x=>x.id===id)||null}
 normalizeCup(id){return this.cup(id)?.id||this.cups[0].id}
 register(id,trackConfig,environmentBuilder){const m=this.get(id);if(!m||trackConfig?.id!==id||typeof environmentBuilder!=='function')throw Error('Adapter stage tidak valid.');this.runtime.set(id,{trackConfig,environmentBuilder})}
 ready(id){const m=this.get(id),r=this.runtime.get(id);return !!(m?.available&&m.trackConfig&&m.environmentBuilder&&r?.trackConfig&&r?.environmentBuilder)}
 status(id,progress={}){const m=this.get(id);if(!m||!this.ready(id))return{code:'coming',label:'Segera Hadir',reason:'Lintasan dan environment belum tersedia.'};const q=m.unlockRequirement;if(q){const target=progress[q.stageId];if(q.type!=='stageScore'||!target||target.bestScore<q.minimumScore)return{code:'locked',label:'Terkunci',reason:q.type==='stageScore'?'Perlu skor '+q.minimumScore+'% di '+(this.get(q.stageId)?.city||q.stageId):'Syarat pembukaan belum dikonfigurasi.'}}return{code:'available',label:'Tersedia',reason:''}}
 track(id){if(!this.ready(id))throw Error((this.get(id)?.city||id)+' · Segera Hadir. Lintasan dan environment belum tersedia.');return this.runtime.get(id).trackConfig}
 requireStage(id,progress={}){const s=this.status(id,progress);if(s.code!=='available')throw Error((this.get(id)?.city||id)+' · '+s.label+'. '+s.reason);return this.runtime.get(id).trackConfig}
 cupStatus(id,progress={}){const c=this.cup(id);if(!c)return{available:false,missing:[],label:'Grand Prix tidak dikenal'};const missing=c.stageIds.filter(s=>this.status(s,progress).code!=='available');return{available:!missing.length,missing,label:missing.length?'Menunggu '+missing.length+' arena':'Tersedia'}}
 requireCup(id='kalbar-klasik',progress={}){const c=this.cup(id),s=this.cupStatus(id,progress);if(!c||!s.available)throw Error((c?.displayName||id)+' belum dapat dimainkan. '+s.label+'.');return c.stageIds.slice()}
 buildEnvironment(renderer,track){const config=this.track(track.id);if(track.config!==config)throw Error('Konfigurasi world tidak cocok dengan registry.');return this.runtime.get(track.id).environmentBuilder(renderer,track)}
 normalizeProgress(stored,results=[]){results=Array.isArray(results)?results:[];const out={};for(const m of this.catalog){const saved=stored?.[m.id];if(saved&&typeof saved==='object'){out[m.id]={races:Math.floor(finite(saved.races)),wins:Math.floor(finite(saved.wins)),bestScore:finite(saved.bestScore,0,100),bestTime:Number.isFinite(saved.bestTime)&&saved.bestTime>0?saved.bestTime:null,lastResultId:String(saved.lastResultId||'').slice(0,160)};continue}let p={races:0,wins:0,bestScore:0,bestTime:null,lastResultId:''};const seen=new Set();for(const r of results)if(r&&r.stage===m.id&&Array.isArray(r.records)&&(!r.id||!seen.has(r.id))){if(r.id)seen.add(r.id);p=this.applyProgress(p,r)}out[m.id]=p}return out}
 applyProgress(p,r){if(r.id&&p.lastResultId===r.id)return p;return{races:p.races+1,wins:p.wins+(r.position===1?1:0),bestScore:Math.max(p.bestScore,finite(r.score,0,100)),bestTime:Number.isFinite(r.time)&&r.time>0?Math.min(p.bestTime||Infinity,r.time):p.bestTime,lastResultId:String(r.id||'').slice(0,160)}}
 recordProgress(stored,result){const out=this.normalizeProgress(stored);if(this.get(result.stage))out[result.stage]=this.applyProgress(out[result.stage],result);return out}
}
const catalog=JSON.parse(document.getElementById('patch1StageCatalog').textContent),cups=JSON.parse(document.getElementById('patch5CupCatalog').textContent),registry=new StageRegistry(catalog,cups);registry.Registry=StageRegistry;root.RaceStages=registry;
})(globalThis);
// Existing environments keep their accepted composition/geometry; only dispatch is registered.
for(const m of RaceStages.catalog){const track=RaceCore.STAGES.find(t=>t.id===m.trackConfig);if(m.available&&track&&typeof globalThis[m.environmentBuilder]==='function')RaceStages.register(m.id,track,(renderer,t)=>renderer.scenery.build(t))}
