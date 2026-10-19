/* Model-only presentation. Input, physics, questions, rewards and storage stay in the original app. */
(function(){
'use strict';
const canvas=document.getElementById('world'),host=document.getElementById('garagePreviewHost');
// HTML exports clone live DOM. Remove a cloned control/avatar before binding anew.
host.querySelector('.batch-expression')?.remove();document.querySelectorAll('.batch-result-avatar').forEach(x=>x.remove());
const label=document.createElement('label');label.className='batch-expression';label.hidden=true;label.append('Ekspresi ');
const select=document.createElement('select');select.setAttribute('aria-label','Ekspresi karakter');for(const [value,text] of [['normal','Ramah'],['happy','Senang'],['shock','Terkejut']]){const o=document.createElement('option');o.value=value;o.textContent=text;select.append(o)}label.append(select);host.append(label);
const hint=document.querySelector('.garage-model-note span'),fullHint='Geser untuk memutar · cubit atau scroll untuk zoom';
function updateHint(){if(hint)hint.textContent=host.dataset.batchModel==='true'&&innerWidth<700?'Geser · cubit untuk zoom':fullHint}
window.addEventListener('resize',updateHint);
canvas.addEventListener('racequest:preview',e=>{const batch=[1,2,3].includes(e.detail);host.dataset.batchModel=String(batch);label.hidden=!batch;select.value='normal';updateHint()});
select.addEventListener('change',()=>{if(document.body.dataset.screen==='garage'&&canvas.__garageRenderer)canvas.__garageRenderer.previewExpression=select.value});
// The existing results screen uses a trophy, not a 3D model. Add a small actual
// character render beside the result text; the trophy and scoring are preserved.
let previousScreen=document.body.dataset.screen;
new MutationObserver(()=>{
 const screen=document.body.dataset.screen,fromRace=previousScreen==='race';previousScreen=screen;
 if(screen!=='results'||!fromRace)return;
 const r=canvas.__garageRenderer,s=r?.batchSession,ids={1:'nara',2:'bimo',3:'sora'};
 if(!s||!ids[s.character])return;
 const hero=document.querySelector('#resultsContent .result-hero>div');if(!hero||hero.querySelector('.batch-result-avatar'))return;
 const rank=document.querySelector('#resultsContent .result-metrics .metric:nth-child(3) b')?.textContent;
 const key='avatar_'+ids[s.character]+(rank==='#1'?'_happy':'')+'.webp',assets=r.assets;
 if(!assets[key])return;
 const image=document.createElement('img');image.className='batch-result-avatar';image.src=assets[key].uri;image.alt=RaceCore.CHARACTERS[s.character].name+(rank==='#1'?' senang menang':' selesai balapan');hero.append(image);
}).observe(document.body,{attributes:true,attributeFilter:['data-screen']});
})();
