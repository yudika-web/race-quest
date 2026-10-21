(function(root){'use strict';
const $=id=>document.getElementById(id),form=$('setupForm'),pristine=form.outerHTML;
let step=0,panels=[],submit,back,progress;
const titles=['Nama dan kelas','Arena dan cuaca','Pengaturan balapan'];
function show(n,focus=true){step=n;panels.forEach((p,i)=>p.hidden=i!==n);progress.querySelectorAll('li').forEach((li,i)=>{li.dataset.current=String(i===n);if(i===n)li.setAttribute('aria-current','step');else li.removeAttribute('aria-current')});$('onboardingTitle').textContent=titles[n];submit.textContent=n===2?'Pilih Karakter →':'Lanjut →';back.hidden=n===0;form.querySelector('.dialog-body').scrollTop=0;if(focus)(n===0?$('playerName'):panels[n].querySelector('button:not([disabled]),select:not([aria-hidden]),input'))?.focus();}
function validIdentity(){for(const id of ['playerName','playerClass']){const input=$(id);input.value=input.value.trim();if(!input.value){input.setCustomValidity(id==='playerName'?'Isi nama pembalap.':'Isi kelas siswa.');input.reportValidity();input.addEventListener('input',()=>input.setCustomValidity(''),{once:true});return false}input.setCustomValidity('')}return true;}
function mount(){
 if(!panels.length){
  const body=form.querySelector('.dialog-body'),head=form.querySelector('.dialog-head');form.noValidate=true;
  head.querySelector('h2').id='onboardingTitle';progress=document.createElement('ol');progress.className='onboarding-progress';progress.setAttribute('aria-label','Persiapan siswa');titles.forEach((t,i)=>{const li=document.createElement('li');li.textContent=(i+1)+'. '+t;progress.append(li)});head.append(progress);
  for(let i=0;i<3;i++){const panel=document.createElement('section');panel.className='onboarding-panel';panel.setAttribute('aria-label',titles[i]);panels.push(panel)}
  panels[0].append($('playerName').closest('label'),$('playerClass').closest('label'));
  const note=document.createElement('p');note.className='muted small';note.textContent='Nama dan kelas dicatat pada hasil belajar balapan ini. Data bank soal guru tetap terpisah.';panels[0].append(note);
  const left=body.querySelector('.patch-setup-left'),right=body.querySelector('.patch-setup-right');
  panels[1].append($('setupStageFields'));
  for(const node of [...left.children])if(node.id!=='setupError')panels[2].append(node);
  panels[2].append($('setupMasteryInfo'));body.append($('setupError'),...panels);left.remove();right.remove();
  back=document.createElement('button');back.type='button';back.className='btn secondary';back.id='onboardingBack';back.textContent='← Kembali';back.onclick=()=>show(Math.max(0,step-1));submit=form.querySelector('button[type=submit]');submit.before(back);
  form.addEventListener('submit',e=>{if(step<2||!validIdentity()){e.preventDefault();e.stopImmediatePropagation();if(step===0){if(validIdentity())show(1)}else if(step===1)show(2);else show(0);}},true);
 }
 panels[2].querySelectorAll('.onboarding-race-mode').forEach(n=>n.remove());
 for(const id of ['setupMode','setupCup']){const label=$(id).closest('label');label.classList.add('onboarding-race-mode');panels[2].prepend(label)}
 show(step,false);
}
root.BlokRayaOnboarding={mount,reset(){show(0)},cleanExport(clone){clone.querySelector('#setupForm').outerHTML=pristine;for(const id of ['garageSetupInfo','characterGrid','paintPicker'])clone.querySelector('#'+id).replaceChildren()}};
})(globalThis);
