/* Garage-only orbit controls. Race input and camera never read this state. */
(function(){
'use strict';
const canvas=document.getElementById('world'),host=document.getElementById('garagePreviewHost');
const modes=[...host.querySelectorAll('[data-garage-view]')],auto=host.querySelector('[data-garage-auto]'),reset=host.querySelector('[data-garage-reset]');
// Exports clone the live DOM; restore the initial view's accessible state.
for(const b of modes)b.setAttribute('aria-pressed',String(b.dataset.garageView==='full'));auto.setAttribute('aria-pressed','true');
const renderer=()=>canvas.__garageRenderer;
const inGarage=()=>document.body.dataset.screen==='garage';
function sync(){const r=renderer();if(!r)return;for(const b of modes)b.setAttribute('aria-pressed',String(b.dataset.garageView===(r.garageView||'full')));auto.setAttribute('aria-pressed',String(r.garageOrbit?.auto!==false))}
for(const b of modes)b.addEventListener('click',()=>{const r=renderer();if(!r||!inGarage())return;r.garageView=b.dataset.garageView;r.garageOrbit.scale=1;sync()});
auto.addEventListener('click',()=>{const r=renderer();if(!r||!inGarage())return;r.garageOrbit.auto=!r.garageOrbit.auto;sync()});
function restore(){const r=renderer();if(!r)return;r.garageOrbit={yaw:.52,pitch:.318,scale:1,auto:true,dragging:false,lastTime:null};sync()}
reset.addEventListener('click',restore);
canvas.tabIndex=0;canvas.setAttribute('aria-label','Pratinjau 3D: geser untuk memutar, cubit atau gunakan roda mouse untuk zoom');
const points=new Map();let previousDistance=0;
const span=()=>{const p=[...points.values()];return p.length===2?Math.hypot(p[0].x-p[1].x,p[0].y-p[1].y):0};
canvas.addEventListener('pointerdown',e=>{if(!inGarage()||!renderer())return;e.preventDefault();const r=renderer();r.garageOrbit.auto=false;r.garageOrbit.dragging=true;points.set(e.pointerId,{x:e.clientX,y:e.clientY});previousDistance=span();canvas.setPointerCapture(e.pointerId);sync()});
canvas.addEventListener('pointermove',e=>{if(!inGarage()||!points.has(e.pointerId))return;e.preventDefault();const old=points.get(e.pointerId),r=renderer(),o=r.garageOrbit;points.set(e.pointerId,{x:e.clientX,y:e.clientY});if(points.size===1){o.yaw-=(e.clientX-old.x)*.009;o.pitch=Math.max(-.10,Math.min(.82,o.pitch+(e.clientY-old.y)*.006))}else{const distance=span();if(previousDistance>0&&distance>0)o.scale=Math.max(.70,Math.min(1.5,o.scale*previousDistance/distance));previousDistance=distance}});
function release(e){points.delete(e.pointerId);const r=renderer();if(r?.garageOrbit)r.garageOrbit.dragging=points.size>0;previousDistance=span();if(canvas.hasPointerCapture(e.pointerId))canvas.releasePointerCapture(e.pointerId)}
canvas.addEventListener('pointerup',release);canvas.addEventListener('pointercancel',release);canvas.addEventListener('lostpointercapture',e=>{points.delete(e.pointerId);if(renderer()?.garageOrbit)renderer().garageOrbit.dragging=points.size>0});
canvas.addEventListener('wheel',e=>{if(!inGarage()||!renderer())return;e.preventDefault();const o=renderer().garageOrbit;o.scale=Math.max(.70,Math.min(1.5,o.scale*Math.exp(e.deltaY*.001)));},{passive:false});
canvas.addEventListener('keydown',e=>{if(!inGarage()||!renderer())return;const o=renderer().garageOrbit;let handled=true;switch(e.key){case 'ArrowLeft':o.yaw-=.12;break;case 'ArrowRight':o.yaw+=.12;break;case 'ArrowUp':o.pitch=Math.min(.82,o.pitch+.08);break;case 'ArrowDown':o.pitch=Math.max(-.10,o.pitch-.08);break;case '+':case '=':o.scale=Math.max(.70,o.scale*.9);break;case '-':o.scale=Math.min(1.5,o.scale/ .9);break;case '0':restore();return;default:handled=false}if(handled){e.preventDefault();o.auto=false;sync()}});
new MutationObserver(()=>{if(!inGarage()){points.clear();if(renderer()?.garageOrbit)renderer().garageOrbit.dragging=false}}).observe(document.body,{attributes:true,attributeFilter:['data-screen']});
})();
