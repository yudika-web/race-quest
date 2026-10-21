/* The PATCH 8D fullscreen helper, moved unchanged ahead of startup/assets. */
(function(root){'use strict';
function fullscreenElement(){return document.fullscreenElement||document.webkitFullscreenElement||null}
function requestFullscreen(){const el=document.documentElement,request=el.requestFullscreen||el.webkitRequestFullscreen;if(fullscreenElement()||!request||(el.requestFullscreen?document.fullscreenEnabled:document.webkitFullscreenEnabled)===false||navigator.userActivation?.isActive===false)return Promise.resolve(false);try{return Promise.resolve(request.call(el)).then(()=>!!fullscreenElement(),()=>false)}catch(e){return Promise.resolve(false)}}
function toggleFullscreen(){if(!fullscreenElement())return requestFullscreen();try{return Promise.resolve((document.exitFullscreen||document.webkitExitFullscreen).call(document)).then(()=>false,()=>false)}catch(e){return Promise.resolve(false)}}
root.RaceViewport={fullscreenElement,requestFullscreen,toggleFullscreen};
// Capture the first real poster/CTA interaction even while the HTML is parsing.
let entered=false,complete=false,resolve;const entryReady=new Promise(r=>resolve=r);
document.addEventListener('click',e=>{if(entered||complete||!e.isTrusted||!e.target.closest?.('#loading')||e.target.closest('#brLoadingRetry'))return;root.RaceViewport.requestFullscreen();entered=true;const button=document.getElementById('brEnterButton');if(button){button.disabled=true;button.textContent='Menyiapkan BlokRaya…'}resolve()},true);
root.BlokRayaStartup={entryReady,get entered(){return entered},finish(){complete=true}};
})(globalThis);
