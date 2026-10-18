(function(root){'use strict';
const M={identity:()=>new Float32Array([1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]),
 mul:(a,b)=>{let o=new Float32Array(16);for(let c=0;c<4;c++)for(let r=0;r<4;r++)for(let k=0;k<4;k++)o[c*4+r]+=a[k*4+r]*b[c*4+k];return o},
 trans:t=>{let m=M.identity();m[12]=t[0];m[13]=t[1];m[14]=t[2];return m},
 scale:s=>{let m=M.identity();m[0]=s;m[5]=s;m[10]=s;return m},
 ry:t=>{let m=M.identity(),c=Math.cos(t),s=Math.sin(t);m[0]=c;m[2]=-s;m[8]=s;m[10]=c;return m},
 rx:t=>{let m=M.identity(),c=Math.cos(t),s=Math.sin(t);m[5]=c;m[6]=s;m[9]=-s;m[10]=c;return m},
 rz:t=>{let m=M.identity(),c=Math.cos(t),s=Math.sin(t);m[0]=c;m[1]=s;m[4]=-s;m[5]=c;return m}};
const norm=a=>{const n=Math.hypot(...a)||1;return a.map(v=>v/n)},cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0);
function look(eye,target){const z=norm(eye.map((v,i)=>v-target[i])),x=norm(cross([0,1,0],z)),y=cross(z,x);return new Float32Array([x[0],y[0],z[0],0,x[1],y[1],z[1],0,x[2],y[2],z[2],0,-dot(x,eye),-dot(y,eye),-dot(z,eye),1])}
function perspective(aspect,fov=60){const f=1/Math.tan(fov*Math.PI/360),n=.08,far=800;return new Float32Array([f/aspect,0,0,0,0,f,0,0,0,0,(far+n)/(n-far),-1,0,0,2*far*n/(n-far),0])}
function orthographic(radius,near,far){const m=M.identity();m[0]=m[5]=1/radius;m[10]=-2/(far-near);m[14]=-(far+near)/(far-near);return m}
const transform=(x,y,z,yaw=0,scale=1)=>M.mul(M.trans([x,y,z]),M.mul(M.ry(yaw),M.scale(scale)));
const KARTS=RaceCore.CHARACTERS.map(c=>c.model);
const colors={road:[.15,.20,.27],grass:[.17,.42,.20],sand:[.72,.57,.34],water:[.035,.32,.48],orange:[1,.30,.045],white:[.85,.91,.94]};
class Renderer{
 constructor(canvas,assets){
  this.canvas=canvas;this.assets=assets;this.gl=canvas.getContext('webgl',{antialias:true,alpha:true,powerPreference:'high-performance'});if(!this.gl)throw Error('Perangkat ini belum mendukung WebGL. Coba Chrome/Edge dengan akselerasi grafis aktif.');
  const gl=this.gl;this.models={};this.textureList=[];this.eye=null;this.mode='none';
  const vs=`attribute vec3 aPos,aNormal;attribute vec2 aUV;uniform mat4 uModel,uView,uProjection,uLightMatrix;uniform float uFoliage,uTime;varying vec3 vNormal,vWorld;varying vec2 vUV;varying vec4 vLight;void main(){vec4 w=uModel*vec4(aPos,1.0);w.x+=uFoliage*.045*sin(w.z*.7+uTime*.65)*smoothstep(1.7,4.0,aPos.y);vWorld=w.xyz;vNormal=mat3(uModel)*aNormal;vUV=aUV;vLight=uLightMatrix*w;gl_Position=uProjection*uView*w;}`;
  const fs=`precision highp float;
varying vec3 vNormal,vWorld;varying vec2 vUV;varying vec4 vLight;
uniform vec3 uColor,uEye,uEmissive;uniform float uRough,uMetal,uHasTexture,uFog,uAlpha,uShadow,uWater,uTime,uFoliage,uSunEnabled,uBubble,uOil,uWeather,uOpacity,uSunQuality;uniform vec3 uFogColor,uPaint;uniform sampler2D uTexture;uniform highp sampler2D uSunMap;uniform vec2 uSunTexel;
float sunlight(vec3 n,vec3 l){
 if(uSunEnabled<.5)return 1.0;vec3 q=vLight.xyz/vLight.w*.5+.5;
 if(q.x<=.0||q.x>=1.0||q.y<=.0||q.y>=1.0||q.z<=.0||q.z>=1.0)return 1.0;
 float bias=.00035+.0007*(1.0-max(dot(n,l),0.0)),lit=0.0,taps=0.0;
 for(int x=-1;x<=1;x++){for(int y=-1;y<=1;y++){if(uSunQuality<.5&&(x==0||y==0))continue;taps+=1.0;vec4 packedDepth=texture2D(uSunMap,q.xy+vec2(float(x),float(y))*uSunTexel*1.6);float d=dot(packedDepth,vec4(.000000059604645,.000015258789,.00390625,1.0))*.99609375;lit+=step(q.z-bias,d);}}
 float fade=1.0-smoothstep(.78,.98,max(abs(q.x*2.0-1.0),abs(q.y*2.0-1.0)));return mix(1.0,.22+.78*lit/max(1.0,taps),fade);
}
void main(){
 float fog=clamp((distance(uEye,vWorld)-mix(105.0,23.0,step(1.5,uWeather)))/mix(290.0,85.0,step(1.5,uWeather)),0.0,1.0)*uFog;
 if(uShadow>.5){float r=length((vUV-.5)*2.0);float a=(1.0-smoothstep(.12,1.0,r))*uAlpha*(1.0-fog);gl_FragColor=vec4(.025,.042,.060,a);return;}
 vec3 n=normalize(vNormal);if(!gl_FrontFacing)n=-n;
 vec3 base=uColor*uPaint;if(uHasTexture>.5)base*=pow(texture2D(uTexture,vUV).rgb,vec3(2.2));
 if(uWater>.5){vec2 q=vWorld.xz;n=normalize(vec3(.055*cos(q.x*1.2+uTime),1.0,.045*sin(q.y*1.6-uTime*.7)));float wave=.5+.5*sin(q.x*2.2+q.y*.7+uTime*.8);base*=.9+.15*wave;}
 vec3 l=normalize(vec3(-1.0,2.0,1.0)),v=normalize(uEye-vWorld),h=normalize(l+v);float sun=sunlight(n,l);
 float hemi=clamp(n.y*.5+.5,0.0,1.0);vec3 ambient=mix(vec3(.18,.17,.125),vec3(.34,.45,.56),hemi);
 float diffuseSun=max(dot(n,l),0.0);vec3 diffuse=ambient+vec3(.95,.83,.64)*diffuseSun*sun+vec3(.055,.08,.12)*max(dot(n,normalize(vec3(1.0,.5,-1.0))),0.0);
 float rough=clamp(uRough,.12,1.0),fresnel=pow(1.0-max(dot(n,v),0.0),5.0);vec3 f0=mix(vec3(.035),base,uMetal);vec3 specColor=mix(f0,vec3(1.0),fresnel);
 float sp=pow(max(dot(n,h),0.0),mix(110.0,10.0,rough))*(.55+.65*uMetal)*sun;
 vec3 c=base*diffuse+specColor*sp+uEmissive*.42;
 c+=vec3(.14,.21,.26)*fresnel*(.12+.25*uMetal)*(hemi*.7+.3);
 c+=base*uFoliage*vec3(.08,.13,.035)*pow(max(dot(-l,v),0.0),2.0)*sun;
 if(uWater>.5)c=mix(c,vec3(.28,.53,.63),.17+.40*fresnel);
 if(uOil>.5){float band=.5+.5*sin(vUV.x*22.0+vUV.y*17.0+uTime*.4);c=mix(vec3(.009,.012,.025),vec3(.13,.045,.22),band*.6)+vec3(.02,.05,.065)*fresnel;}
 if(uBubble>.5){float edge=pow(1.0-abs(dot(n,v)),2.0);vec3 iridescent=.5+.5*cos(vec3(0.0,2.0,4.0)+vNormal.y*4.0+uTime*.8);c=mix(vec3(.20,.68,.85),iridescent,.35)+edge*.55;gl_FragColor=vec4(c,.10+edge*.48);return;}
 c*=mix(1.0,.74,step(.5,uWeather));c=mix(c,uFogColor,fog);c=c/(vec3(1.0)+c*.24);gl_FragColor=vec4(pow(max(c,vec3(0.0)),vec3(1.0/2.2)),uAlpha*uOpacity);
}`;
  const shader=(t,s)=>{let o=gl.createShader(t);gl.shaderSource(o,s);gl.compileShader(o);if(!gl.getShaderParameter(o,gl.COMPILE_STATUS))throw Error('Shader: '+gl.getShaderInfoLog(o));return o};
  this.prog=gl.createProgram();gl.attachShader(this.prog,shader(gl.VERTEX_SHADER,vs));gl.attachShader(this.prog,shader(gl.FRAGMENT_SHADER,fs));gl.linkProgram(this.prog);if(!gl.getProgramParameter(this.prog,gl.LINK_STATUS))throw Error('Tampilan 3D belum dapat dimuat.');gl.useProgram(this.prog);
  this.L={};for(let a of ['aPos','aNormal','aUV'])this.L[a]=gl.getAttribLocation(this.prog,a);for(let u of ['uModel','uView','uProjection','uColor','uEye','uEmissive','uRough','uMetal','uHasTexture','uTexture','uFog','uAlpha','uShadow','uWater','uTime','uFoliage','uLightMatrix','uSunEnabled','uSunMap','uSunTexel','uBubble','uOil','uWeather','uOpacity','uSunQuality','uFogColor','uPaint'])this.L[u]=gl.getUniformLocation(this.prog,u);
  gl.enable(gl.DEPTH_TEST);gl.enable(gl.CULL_FACE);gl.enable(gl.BLEND);gl.blendFunc(gl.SRC_ALPHA,gl.ONE_MINUS_SRC_ALPHA);
  this.quality='auto';this.pixelScale=.9;this.maxParticles=300;this.viewDistance=105;this.frameWindow=[];this.adaptCooldown=0;
  this.roadTexture=this.textureURI(assets['texture_road.webp'].uri);this.grassTexture=this.textureURI(assets['texture_grass.webp'].uri);
  this.tireMark=this.mesh([[-.055,0,-.22],[.055,0,-.22],[.055,0,.22],[-.055,0,.22]],[[0,2,1],[0,3,2]],[.018,.022,.026],null,null,true);this.tireMark.material.alpha=.35;this.skidMarks=[];this.markCarry=0;this.ring=this.makeRing();this.flame=this.makeFlame();this.shadow=this.makeShadow();this.bubbleMesh=this.makeBubble();this.oilMesh=this.makeOil();this.initParticles(shader);this.scenery=new RaceScenery(this);this.clock=0;this.cameraTime=0;this.cameraTarget=null;this.initSunShadows(shader);this.initSky(shader);this.setQuality('auto');
 }
 ensureModel(file){if(!this.models[file])this.loadModel(file)}
 prepareModels(files){const keep=new Set(files);for(const f of files)this.ensureModel(f);for(const f of KARTS)if(this.models[f]&&!keep.has(f)){const m=this.models[f];for(const group of [m.primitives,m.depthPrimitives])for(const ps of Object.values(group))for(const p of ps)for(const b of [p.pos,p.normal,p.uv,p.index])if(b)this.gl.deleteBuffer(b);delete this.models[f]}}
 setQuality(value){this.quality=['low','medium','high','auto'].includes(value)?value:'auto';const q=this.quality;this.pixelScale=q==='low'?.65:q==='high'?1.4:.9;this.maxParticles=q==='low'?120:q==='high'?480:300;this.viewDistance=q==='low'?78:q==='high'?125:105;const size=q==='high'?1024:512;if(size!==this.sunSize&&this.sunTexture){const gl=this.gl;this.sunSize=size;gl.bindTexture(gl.TEXTURE_2D,this.sunTexture);gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,size,size,0,gl.RGBA,gl.UNSIGNED_BYTE,null);gl.bindRenderbuffer(gl.RENDERBUFFER,this.sunDepth);gl.renderbufferStorage(gl.RENDERBUFFER,gl.DEPTH_COMPONENT16,size,size);gl.bindRenderbuffer(gl.RENDERBUFFER,null)}this.frameWindow=[];this.adaptCooldown=0}
 observeFrame(dt){if(this.quality!=='auto'||dt<=0||dt>.25)return;this.adaptCooldown=Math.max(0,this.adaptCooldown-dt);this.frameWindow.push(dt);const span=this.frameWindow.reduce((a,b)=>a+b,0);if(span<2)return;const fps=this.frameWindow.length/span;this.frameWindow=[];if(!this.adaptCooldown&&fps<32&&this.pixelScale>.55){this.pixelScale=Math.max(.55,this.pixelScale-.1);this.adaptCooldown=4}else if(!this.adaptCooldown&&fps>55&&this.pixelScale<.9){this.pixelScale=Math.min(.9,this.pixelScale+.05);this.adaptCooldown=10}}
 initSunShadows(shader){
  const gl=this.gl;this.sunSize=1024;this.lightMatrix=M.identity();this.depthPass=false;this.sunEnabled=false;
  this.sunProgram=gl.createProgram();
  gl.attachShader(this.sunProgram,shader(gl.VERTEX_SHADER,`attribute vec3 aPos;uniform mat4 uModel,uLightMatrix;uniform float uFoliage,uTime;varying highp float vSunDepth;void main(){vec4 w=uModel*vec4(aPos,1.0);w.x+=uFoliage*.045*sin(w.z*.7+uTime*.65)*smoothstep(1.7,4.0,aPos.y);gl_Position=uLightMatrix*w;vSunDepth=gl_Position.z/gl_Position.w*.5+.5;}`));
  gl.attachShader(this.sunProgram,shader(gl.FRAGMENT_SHADER,`precision highp float;varying highp float vSunDepth;void main(){vec4 p=fract(min(vSunDepth,.999999)*vec4(16777216.0,65536.0,256.0,1.0));p-=p.xxyz*vec4(0.0,.00390625,.00390625,.00390625);gl_FragColor=p*1.00392156862745;}`));
  gl.linkProgram(this.sunProgram);if(!gl.getProgramParameter(this.sunProgram,gl.LINK_STATUS))return;
  this.SL={aPos:gl.getAttribLocation(this.sunProgram,'aPos')};for(const n of ['uModel','uLightMatrix','uFoliage','uTime'])this.SL[n]=gl.getUniformLocation(this.sunProgram,n);
  this.sunTexture=gl.createTexture();gl.bindTexture(gl.TEXTURE_2D,this.sunTexture);gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,this.sunSize,this.sunSize,0,gl.RGBA,gl.UNSIGNED_BYTE,null);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.NEAREST);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.NEAREST);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);
  this.sunFramebuffer=gl.createFramebuffer();gl.bindFramebuffer(gl.FRAMEBUFFER,this.sunFramebuffer);gl.framebufferTexture2D(gl.FRAMEBUFFER,gl.COLOR_ATTACHMENT0,gl.TEXTURE_2D,this.sunTexture,0);
  this.sunDepth=gl.createRenderbuffer();gl.bindRenderbuffer(gl.RENDERBUFFER,this.sunDepth);gl.renderbufferStorage(gl.RENDERBUFFER,gl.DEPTH_COMPONENT16,this.sunSize,this.sunSize);gl.framebufferRenderbuffer(gl.FRAMEBUFFER,gl.DEPTH_ATTACHMENT,gl.RENDERBUFFER,this.sunDepth);
  this.sunEnabled=gl.checkFramebufferStatus(gl.FRAMEBUFFER)===gl.FRAMEBUFFER_COMPLETE;gl.bindFramebuffer(gl.FRAMEBUFFER,null);gl.bindRenderbuffer(gl.RENDERBUFFER,null);gl.bindTexture(gl.TEXTURE_2D,null);gl.useProgram(this.prog);
 }
 renderSunShadows(session,pos,player,yaw,blend,slope){
  const gl=this.gl;if(!this.sunEnabled||this.quality==='low'){gl.uniform1f(this.L.uSunEnabled,0);return}
  const center=[pos.x,pos.y+2,pos.z],eye=[center[0]-42,center[1]+84,center[2]+42];this.lightMatrix=M.mul(orthographic(45,1,180),look(eye,center));
  // Snap the light projection to texels to suppress shimmering while driving.
  for(const i of [12,13])this.lightMatrix[i]=Math.round(this.lightMatrix[i]*this.sunSize*.5)/(this.sunSize*.5);
  gl.bindFramebuffer(gl.FRAMEBUFFER,this.sunFramebuffer);gl.viewport(0,0,this.sunSize,this.sunSize);gl.clearColor(1,1,1,1);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);gl.disable(gl.BLEND);gl.disable(gl.DITHER);gl.depthMask(true);gl.disable(gl.CULL_FACE);gl.useProgram(this.sunProgram);for(const n of ['aPos','aNormal','aUV'])if(this.L[n]!==this.SL.aPos)gl.disableVertexAttribArray(this.L[n]);gl.uniformMatrix4fv(this.SL.uLightMatrix,false,this.lightMatrix);gl.uniform1f(this.SL.uTime,this.clock);this.depthPass=true;
  for(const o of this.static){const x=o.matrix[12],z=o.matrix[14];if(Math.hypot(x-pos.x,z-pos.z)<68)this.drawModel(o.file,o.matrix)}
  for(const {key,p} of this.scenery.batches)if(key!=='shadow'&&key!=='water')this.drawPrimitive(p,M.identity());
  const files=KARTS;
  for(const [i,actual] of session.ai.entries()){const a=blend(actual,session.previousAI?.[i]),p=session.track.place(a.s,a.lateral);if(Math.hypot(p.x-pos.x,p.z-pos.z)<55)this.drawModel(files[a.character],M.mul(transform(p.x,p.y+.09+(a.y||0),p.z,p.yaw+(a.slip>0?Math.sin(this.clock*12)*.28:0)),M.rx(slope(a.s))),{spin:a.s/.205,steer:-session.track.curvature(a.s)*3})}
  this.drawModel(files[session.character],M.mul(M.mul(transform(pos.x,pos.y+.09+(player.y||0),pos.z,yaw),M.rx(slope(player.s))),M.rz((player.steering||0)*Math.min(1,player.speed/23)*.035)),{spin:player.s/.205,steer:-(player.steering||0)*.42});
  this.depthPass=false;gl.enable(gl.DITHER);gl.bindFramebuffer(gl.FRAMEBUFFER,null);gl.viewport(0,0,this.canvas.width,this.canvas.height);gl.clearColor(0,0,0,0);gl.enable(gl.BLEND);gl.blendFunc(gl.SRC_ALPHA,gl.ONE_MINUS_SRC_ALPHA);gl.useProgram(this.prog);gl.uniformMatrix4fv(this.L.uLightMatrix,false,this.lightMatrix);gl.uniform1f(this.L.uSunEnabled,1);gl.uniform1f(this.L.uSunQuality,this.quality==='high'?1:0);gl.uniform2f(this.L.uSunTexel,1/this.sunSize,1/this.sunSize);gl.activeTexture(gl.TEXTURE1);gl.bindTexture(gl.TEXTURE_2D,this.sunTexture);gl.uniform1i(this.L.uSunMap,1);gl.activeTexture(gl.TEXTURE0);
 }
 initParticles(shader){
  const gl=this.gl;this.particleProgram=gl.createProgram();
  gl.attachShader(this.particleProgram,shader(gl.VERTEX_SHADER,`attribute vec3 aParticle;attribute vec4 aTint;attribute float aSize;uniform mat4 uView,uProjection;uniform float uHeight;varying vec4 vTint;void main(){vec4 p=uView*vec4(aParticle,1.0);gl_Position=uProjection*p;gl_PointSize=clamp(aSize*uHeight*uProjection[1][1]/max(.2,-p.z),1.0,96.0);vTint=aTint;}`));
  gl.attachShader(this.particleProgram,shader(gl.FRAGMENT_SHADER,`precision mediump float;varying vec4 vTint;uniform float uEnergy;void main(){vec2 p=gl_PointCoord*2.0-1.0;float r=dot(p,p);if(r>1.0)discard;float a=(1.0-smoothstep(.0,1.0,r))*vTint.a;vec3 c=vTint.rgb+uEnergy*pow(max(0.0,1.0-r),6.0)*.55;gl_FragColor=vec4(c,a);}`));
  gl.linkProgram(this.particleProgram);if(!gl.getProgramParameter(this.particleProgram,gl.LINK_STATUS))throw Error('Shader efek belum dapat dimuat.');
  this.PL={};for(const a of ['aParticle','aTint','aSize'])this.PL[a]=gl.getAttribLocation(this.particleProgram,a);for(const u of ['uView','uProjection','uHeight','uEnergy'])this.PL[u]=gl.getUniformLocation(this.particleProgram,u);
  this.particleBuffer=gl.createBuffer();this.particleData=new Float32Array(480*8);this.particles=[];this.fxTime=0;this.dustCarry=0;this.nitroCarry=0;this.fxCooldown=0;this.fxTokens=0;this.fov=60;
 }
 initSky(shader){
  const gl=this.gl;this.skyProgram=gl.createProgram();
  gl.attachShader(this.skyProgram,shader(gl.VERTEX_SHADER,`attribute vec2 aSkyPos;varying vec2 vSkyCoord;void main(){vSkyCoord=aSkyPos;gl_Position=vec4(aSkyPos,.9999,1.0);}`));
  gl.attachShader(this.skyProgram,shader(gl.FRAGMENT_SHADER,`precision highp float;varying vec2 vSkyCoord;uniform vec3 uSkyRight,uSkyUp,uSkyForward,uSkyEye;uniform float uSkyAspect,uSkyTan,uSkyTime,uSkyWeather;uniform sampler2D uSkyImage,uCloudImage;void main(){vec3 ray=normalize(uSkyForward+uSkyRight*vSkyCoord.x*uSkyAspect*uSkyTan+uSkyUp*vSkyCoord.y*uSkyTan);float u=atan(ray.x,ray.z)/6.2831853+.5,h=clamp(atan(ray.y,length(ray.xz))/1.5707963,0.0,1.0);vec2 uv=vec2(fract(u+uSkyEye.x*.000025),1.0-h);vec3 sky=texture2D(uSkyImage,uv).rgb;float seam=1.0-smoothstep(.0,.035,min(uv.x,1.0-uv.x));vec3 edge=(texture2D(uSkyImage,vec2(.02,uv.y)).rgb+texture2D(uSkyImage,vec2(.98,uv.y)).rgb)*.5;sky=mix(sky,edge,seam);vec2 cloudUV=vec2(fract(u*2.5+uSkyEye.x*.0007+uSkyTime*.0008),.86-h*1.7+uSkyEye.z*.00015);vec4 cloud=texture2D(uCloudImage,clamp(cloudUV,vec2(0.0),vec2(1.0)));float valid=step(.0,cloudUV.y)*step(cloudUV.y,1.0)*smoothstep(.01,.16,h);sky=mix(sky,cloud.rgb,cloud.a*.48*valid);sky=mix(vec3(.67,.82,.87),sky,smoothstep(-.10,.06,ray.y));float gray=dot(sky,vec3(.3,.59,.11));sky=mix(sky,vec3(gray)*vec3(.66,.75,.79),uSkyWeather*.65);gl_FragColor=vec4(sky,1.0);}`));
  gl.linkProgram(this.skyProgram);if(!gl.getProgramParameter(this.skyProgram,gl.LINK_STATUS))throw Error('Langit belum dapat dimuat.');this.KL={aSkyPos:gl.getAttribLocation(this.skyProgram,'aSkyPos')};for(const n of ['uSkyRight','uSkyUp','uSkyForward','uSkyEye','uSkyAspect','uSkyTan','uSkyTime','uSkyWeather','uSkyImage','uCloudImage'])this.KL[n]=gl.getUniformLocation(this.skyProgram,n);
  this.skyBuffer=this.buffer(new Float32Array([-1,-1,3,-1,-1,3]));this.skyTexture=this.textureURI(this.assets['sky_panorama.webp'].uri);this.cloudTexture=this.textureURI(this.assets['cloud_layer.webp'].uri,true);
 }
 drawSky(eye,target){
  const gl=this.gl,L=this.KL,z=norm(target.map((x,i)=>x-eye[i])),right=norm(cross(z,[0,1,0])),up=cross(right,z);gl.useProgram(this.skyProgram);gl.disable(gl.DEPTH_TEST);gl.depthMask(false);gl.disable(gl.BLEND);gl.disable(gl.CULL_FACE);
  for(const n of ['aPos','aNormal','aUV'])if(this.L[n]!==L.aSkyPos)gl.disableVertexAttribArray(this.L[n]);gl.bindBuffer(gl.ARRAY_BUFFER,this.skyBuffer);gl.enableVertexAttribArray(L.aSkyPos);gl.vertexAttribPointer(L.aSkyPos,2,gl.FLOAT,false,0,0);
  gl.uniform3fv(L.uSkyRight,right);gl.uniform3fv(L.uSkyUp,up);gl.uniform3fv(L.uSkyForward,z);gl.uniform3fv(L.uSkyEye,eye);gl.uniform1f(L.uSkyAspect,this.canvas.width/this.canvas.height);gl.uniform1f(L.uSkyTan,Math.tan(this.fov*Math.PI/360));gl.uniform1f(L.uSkyTime,this.clock);gl.uniform1f(L.uSkyWeather,this.weather==='clear'?0:1);
  gl.activeTexture(gl.TEXTURE0);gl.bindTexture(gl.TEXTURE_2D,this.skyTexture);gl.uniform1i(L.uSkyImage,0);gl.activeTexture(gl.TEXTURE1);gl.bindTexture(gl.TEXTURE_2D,this.cloudTexture);gl.uniform1i(L.uCloudImage,1);gl.drawArrays(gl.TRIANGLES,0,3);gl.disableVertexAttribArray(L.aSkyPos);gl.activeTexture(gl.TEXTURE0);gl.depthMask(true);gl.enable(gl.DEPTH_TEST);gl.enable(gl.BLEND);gl.useProgram(this.prog);
 }
 emitParticle(x,y,z,vx,vy,vz,size,life,color,energy=false){
  if(this.particles.length>=this.maxParticles)return;this.particles.push({x,y,z,vx,vy,vz,size,life,ttl:life,color,energy});
 }
 updateVFX(s,input={}){
  // Use simulation time: particles freeze together with AI, timers and buffs.
  const dt=Math.max(0,Math.min(.05,s.elapsed-this.fxTime));this.fxTime=s.elapsed;if(!dt)return;
  const p=s.player,q=s.track.place(p.s,p.lateral),yaw=q.yaw+p.error,sn=Math.sin(yaw),cs=Math.cos(yaw),rnd=()=>Math.random()-.5;q.y+=p.y||0;
  for(let i=this.particles.length-1;i>=0;i--){let v=this.particles[i];v.life-=dt;if(v.life<=0){this.particles.splice(i,1);continue}v.x+=v.vx*dt;v.y+=v.vy*dt;v.z+=v.vz*dt;v.vx*=Math.exp(-dt*1.2);v.vz*=Math.exp(-dt*1.2);v.vy+=(v.energy?-.8:.35)*dt;}
  const off=Math.abs(p.lateral)>4.8,skid=!!input.brake||!!p.drifting||Math.abs(p.error)>.25;this.skidMarks=this.skidMarks.filter(m=>s.elapsed-m.t<8);if(skid&&!p.air&&p.speed>8){this.markCarry+=dt;if(this.markCarry>.08){this.markCarry=0;for(const side of [-.6,.6])this.skidMarks.push({x:q.x+cs*side,y:q.y+.121,z:q.z-sn*side,yaw,s:p.s,t:s.elapsed});this.skidMarks=this.skidMarks.slice(-(this.quality==='low'?32:96))}}
  if(p.speed>2&&!p.air){
   this.dustCarry+=dt*(off?65:skid?42:12)*Math.min(1,p.speed/12);
   while(this.dustCarry>=1){this.dustCarry--;const side=Math.random()<.5?-.59:.59,back=-.57;
    this.emitParticle(q.x+cs*side+sn*back,q.y+.18,q.z-sn*side+cs*back,-sn*p.speed*.12+rnd()*1.8,.35+Math.random()*.8,-cs*p.speed*.12+rnd()*1.8,off?.55:.34,.55+Math.random()*.55,off?[.72,.57,.36]:[.71,.77,.79]);
   }
  }
  if(s.buffs.turbo>0&&p.speed>1){
   this.nitroCarry+=dt*100;
   while(this.nitroCarry>=1){this.nitroCarry--;const side=Math.random()<.5?-.31:.31,back=-.9-Math.random()*.35;
    this.emitParticle(q.x+cs*side+sn*back,q.y+.38+rnd()*.08,q.z-sn*side+cs*back,-sn*(3+Math.random()*5)+rnd()*.8,rnd()*.6,-cs*(3+Math.random()*5)+rnd()*.8,.11+Math.random()*.14,.17+Math.random()*.20,Math.random()<.25?[.9,.97,1]:[.12,.65,1],true);
   }
  }
  if(s.collisionCooldown>this.fxCooldown+.05){for(let i=0;i<28;i++){let a=Math.random()*Math.PI*2,v=1+Math.random()*4;this.emitParticle(q.x+sn*.65,q.y+.4,q.z+cs*.65,Math.sin(a)*v,1+Math.random()*2,Math.cos(a)*v,.055+Math.random()*.05,.25+Math.random()*.4,[1,.64,.18],true)}}
  if(s.tokens>this.fxTokens){for(let i=0;i<16;i++){let a=i/16*Math.PI*2;this.emitParticle(q.x,q.y+.9,q.z,Math.sin(a)*1.7,Math.random()*2,Math.cos(a)*1.7,.09,.5,[1,.83,.25],true)}}
  if(s.weather==='rain')for(let i=0;i<(this.quality==='low'?1:4);i++)this.emitParticle(q.x+rnd()*28,q.y+7+Math.random()*6,q.z+rnd()*28,-1,-19,1,.035,.65,[.65,.79,.85]);this.fxCooldown=s.collisionCooldown;this.fxTokens=s.tokens;this.fov+=((s.buffs.turbo>0?69:60)-this.fov)*(1-Math.exp(-dt*4));
  if(s.lastImpact&&s.lastImpact.serial!==this.fxImpact){const hit=s.track.place(s.lastImpact.s,s.lastImpact.lateral);for(let i=0;i<22;i++){const a=i/22*Math.PI*2;this.emitParticle(hit.x,hit.y+.7,hit.z,Math.sin(a)*2.5,Math.random()*2,Math.cos(a)*2.5,.1,.55,s.lastImpact.item==='bubble'?[.35,.85,1]:[.6,.35,.8],true)}this.fxImpact=s.lastImpact.serial}
 }
 drawParticles(){
  const gl=this.gl,L=this.PL;gl.useProgram(this.particleProgram);gl.uniformMatrix4fv(L.uView,false,this.view);gl.uniformMatrix4fv(L.uProjection,false,this.projection);gl.uniform1f(L.uHeight,this.canvas.height);gl.disable(gl.CULL_FACE);gl.depthMask(false);
  for(const energy of [false,true]){let n=0;for(const p of this.particles){if(p.energy!==energy)continue;const age=1-p.life/p.ttl,alpha=(energy?.85:.26)*Math.min(1,age*7)*(1-age);
    this.particleData.set([p.x,p.y,p.z,...p.color,alpha,p.size*(energy?1:1+age*2.5)],n*8);n++;
   }if(!n)continue;
   gl.blendFunc(gl.SRC_ALPHA,energy?gl.ONE:gl.ONE_MINUS_SRC_ALPHA);gl.uniform1f(L.uEnergy,energy?1:0);gl.bindBuffer(gl.ARRAY_BUFFER,this.particleBuffer);gl.bufferData(gl.ARRAY_BUFFER,this.particleData.subarray(0,n*8),gl.DYNAMIC_DRAW);
   for(const [name,size,offset] of [['aParticle',3,0],['aTint',4,12],['aSize',1,28]]){gl.enableVertexAttribArray(L[name]);gl.vertexAttribPointer(L[name],size,gl.FLOAT,false,32,offset)}gl.drawArrays(gl.POINTS,0,n);
  }
  for(const a of ['aParticle','aTint','aSize'])gl.disableVertexAttribArray(L[a]);gl.depthMask(true);gl.blendFunc(gl.SRC_ALPHA,gl.ONE_MINUS_SRC_ALPHA);gl.useProgram(this.prog);
 }
 buffer(data,target){const g=this.gl,b=g.createBuffer();g.bindBuffer(target||g.ARRAY_BUFFER,b);g.bufferData(target||g.ARRAY_BUFFER,data,g.STATIC_DRAW);return b}
 textureURI(uri,alpha=false){const gl=this.gl,format=alpha?gl.RGBA:gl.RGB,t=gl.createTexture();gl.bindTexture(gl.TEXTURE_2D,t);gl.texImage2D(gl.TEXTURE_2D,0,format,1,1,0,format,gl.UNSIGNED_BYTE,new Uint8Array(alpha?[255,255,255,0]:[150,155,160]));gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR);const im=new Image();im.onload=()=>{gl.bindTexture(gl.TEXTURE_2D,t);gl.texImage2D(gl.TEXTURE_2D,0,format,format,gl.UNSIGNED_BYTE,im);gl.generateMipmap(gl.TEXTURE_2D);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR_MIPMAP_LINEAR);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.REPEAT);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.REPEAT)};im.src=uri;this.textureList.push(t);return t}
 loadModel(file){
  if(this.models[file])return;
  const uri=this.assets[file]?.uri;if(!uri)throw Error('Aset tidak ditemukan: '+file);
  const bytes=Uint8Array.from(atob(uri.split(',')[1]),c=>c.charCodeAt(0)),v=new DataView(bytes.buffer),len=v.getUint32(12,true),doc=JSON.parse(new TextDecoder().decode(bytes.slice(20,20+len))),start=28+len,gl=this.gl,textures=[];
  const acc=i=>{const a=doc.accessors[i],b=doc.bufferViews[a.bufferView],k={VEC3:3,VEC2:2,SCALAR:1}[a.type],T={5126:Float32Array,5123:Uint16Array,5125:Uint32Array}[a.componentType];return new T(bytes.buffer,start+(b.byteOffset||0)+(a.byteOffset||0),a.count*k)};
  for(let image of doc.images||[]){const b=doc.bufferViews[image.bufferView],raw=bytes.slice(start+b.byteOffset,start+b.byteOffset+b.byteLength);let str='';for(let i=0;i<raw.length;i+=8192)str+=String.fromCharCode(...raw.subarray(i,i+8192));textures.push(this.textureURI('data:'+image.mimeType+';base64,'+btoa(str)))}
  const primitives={};doc.nodes.forEach((n,i)=>{if(n.mesh===undefined)return;primitives[i]=doc.meshes[n.mesh].primitives.map(p=>{const pos=acc(p.attributes.POSITION),normal=acc(p.attributes.NORMAL),indices=acc(p.indices),uv=p.attributes.TEXCOORD_0===undefined?null:acc(p.attributes.TEXCOORD_0);let mat=doc.materials[p.material],pbr=mat.pbrMetallicRoughness;return {pos:this.buffer(pos),normal:this.buffer(normal),uv:uv?this.buffer(uv):null,index:this.buffer(indices,gl.ELEMENT_ARRAY_BUFFER),count:indices.length,type:indices instanceof Uint16Array?gl.UNSIGNED_SHORT:gl.UNSIGNED_INT,material:{color:pbr.baseColorFactor.slice(0,3),rough:pbr.roughnessFactor,metal:pbr.metallicFactor,emissive:mat.emissiveFactor||[0,0,0],foliage:/foliage/.test(mat.name||'')?1:0,double:mat.doubleSided,texture:pbr.baseColorTexture?textures[doc.textures[pbr.baseColorTexture.index].source]:null}}})});
  // The sun pass does not need material colours or textures. Merge opaque
  // pieces at each rig pivot to avoid redrawing every material separately.
  const depthPrimitives={};doc.nodes.forEach((parent,i)=>{const groups={};for(const child of parent.children||[]){const n=doc.nodes[child];if(n.mesh===undefined)continue;for(const p of doc.meshes[n.mesh].primitives){const foliage=/foliage/.test(doc.materials[p.material].name||'')?1:0,g=groups[foliage]||(groups[foliage]={V:[],F:[],foliage}),positions=acc(p.attributes.POSITION),indices=acc(p.indices),base=g.V.length/3,t=n.translation||[0,0,0];for(let j=0;j<positions.length;j++)g.V.push(positions[j]+t[j%3]);for(const index of indices)g.F.push(index+base)}}
   depthPrimitives[i]=Object.values(groups).map(g=>{if(g.V.length/3>=65536)throw Error('Model bayangan terlalu besar: '+file);const indices=new Uint16Array(g.F);return {pos:this.buffer(new Float32Array(g.V)),index:this.buffer(indices,gl.ELEMENT_ARRAY_BUFFER),count:indices.length,type:gl.UNSIGNED_SHORT,material:{foliage:g.foliage}}});
  });this.models[file]={doc,primitives,depthPrimitives};
 }
 mesh(vertices,faces,color,uv=null,texture=null,double=false){
  const gl=this.gl,V=new Float32Array(vertices.flat()),F=new Uint16Array(faces.flat()),N=new Float32Array(V.length);
  for(let k=0;k<F.length;k+=3){let a=F[k]*3,b=F[k+1]*3,c=F[k+2]*3;const ab=[V[b]-V[a],V[b+1]-V[a+1],V[b+2]-V[a+2]],ac=[V[c]-V[a],V[c+1]-V[a+1],V[c+2]-V[a+2]],n=cross(ab,ac);for(let j of [a,b,c])for(let q=0;q<3;q++)N[j+q]+=n[q]}
  for(let k=0;k<N.length;k+=3){let n=norm([N[k],N[k+1],N[k+2]]);N.set(n,k)}
  return {pos:this.buffer(V),normal:this.buffer(N),uv:uv?this.buffer(new Float32Array(uv.flat())):null,index:this.buffer(F,gl.ELEMENT_ARRAY_BUFFER),count:F.length,type:gl.UNSIGNED_SHORT,material:{color,texture,rough:.8,metal:0,emissive:[0,0,0],double}};
 }
 makeRing(){let V=[],F=[];for(let i=0;i<=32;i++)for(let j=0;j<=5;j++){const a=i/32*Math.PI*2,b=j/5*Math.PI*2,r=1+.035*Math.cos(b);V.push([Math.cos(a)*r,.035*Math.sin(b),Math.sin(a)*r])}for(let i=0;i<32;i++)for(let j=0;j<5;j++){let a=i*6+j,b=a+6;F.push([a,a+1,b],[a+1,b+1,b])}return this.mesh(V,F,[.04,.65,.85],null,null,true)}
 makeFlame(){let V=[[0,0,-.65]],F=[];for(let i=0;i<8;i++)V.push([.09*Math.cos(i*Math.PI/4),.09*Math.sin(i*Math.PI/4),0]);for(let i=0;i<8;i++)F.push([0,i+1,(i+1)%8+1]);const mesh=this.mesh(V,F,[1,.29,.02],null,null,true);mesh.material.emissive=[.9,.2,0];return mesh}
 makeShadow(){const p=this.mesh([[-.9,0,-1.15],[.9,0,-1.15],[.9,0,1.15],[-.9,0,1.15]],[[0,2,1],[0,3,2]],[.01,.02,.03],[[0,0],[1,0],[1,1],[0,1]],null,true);p.material.alpha=.38;p.material.shadow=1;return p}
 makeBubble(){const V=[],F=[];for(let i=0;i<=24;i++)for(let j=0;j<=14;j++){const a=i/24*Math.PI*2,b=j/14*Math.PI;V.push([Math.cos(a)*Math.sin(b),Math.cos(b),Math.sin(a)*Math.sin(b)])}for(let i=0;i<24;i++)for(let j=0;j<14;j++){const a=i*15+j,b=a+15;if(j)F.push([a,b,a+1]);if(j<13)F.push([a+1,b,b+1])}const p=this.mesh(V,F,[.14,.65,.85],null,null,true);p.material.bubble=1;p.material.alpha=.38;p.material.rough=.12;p.material.emissive=[.03,.12,.16];return p}
 makeOil(){const V=[[0,0,0]],F=[],UV=[[.5,.5]];for(let i=0;i<=48;i++){const a=i/48*Math.PI*2,r=1+.08*Math.sin(a*5);V.push([Math.cos(a)*1.3*r,0,Math.sin(a)*2.1*r]);UV.push([.5+.5*Math.cos(a),.5+.5*Math.sin(a)])}for(let i=0;i<48;i++)F.push([0,i+2,i+1]);const p=this.mesh(V,F,[.012,.015,.035],UV,null,true);p.material.oil=1;p.material.rough=.18;p.material.metal=.8;return p}
 drawShadow(matrix){this.gl.depthMask(false);this.drawPrimitive(this.shadow,matrix);this.gl.depthMask(true)}
 clearance(x,z){let d=Infinity;for(const p of this.track.points)d=Math.min(d,(p.x-x)**2+(p.z-z)**2);return Math.sqrt(d)}
 groundAt(x,z){let d=Infinity,y=0;for(const p of this.track.points){const q=(p.x-x)**2+(p.z-z)**2;if(q<d){d=q;y=p.y}}const t=Math.max(0,Math.min(1,(Math.sqrt(d)-5.45)/16));return (1-t)*(y+.02)+t*(-.49)}
 buildWorld(track){
  for(const mesh of [this.road,this.ground,this.shoulders,this.water,this.staticShadows,...(this.curbs||[]),...(this.featureMeshes||[])])if(mesh)for(const buffer of [mesh.pos,mesh.normal,mesh.uv,mesh.index])if(buffer)this.gl.deleteBuffer(buffer);
  this.track=track;this.stage=track.config;this.static=[];for(const file of ['prop_tree.glb','prop_rock.glb','prop_start_gate.glb','prop_tunnel.glb','prop_bridge.glb','item_box.glb','token.glb'])this.ensureModel(file);const N=550,V=[],UV=[],F=[],curbV=[[],[]],curbF=[[],[]];
  for(let i=0;i<=N;i++){const s=i/N*track.length,p=track.point(s);for(let side of [-1,1]){V.push([p.x+p.rightX*side*5,p.y+.09,p.z+p.rightZ*side*5]);UV.push([side<0?0:2,s/4])}}
  for(let i=0;i<N;i++){const a=i*2,b=a+2,u=(i+.5)/N;if(!track.config.gaps.some(g=>Math.abs(u-g.u)*track.length<g.length/2))F.push([a,b,a+1],[a+1,b,b+1]);
   for(let side of [-1,1]){const a=track.point(i/N*track.length),b=track.point((i+1)/N*track.length),color=Math.floor(i/3)%2,verts=curbV[color],faces=curbF[color],k=verts.length;
    for(let [p,d] of [[a,5],[b,5],[a,5.5],[b,5.5]])verts.push([p.x+p.rightX*side*d,p.y+.105,p.z+p.rightZ*side*d]);faces.push([k,k+1,k+2],[k+2,k+1,k+3])}}
  this.road=this.mesh(V,F,track.config.palette.road,UV,this.roadTexture,true);this.curbs=curbV.map((v,i)=>this.mesh(v,curbF[i],i?colors.orange:colors.white,null,null,true));
  let gv=[],guv=[],gf=[];const cx=40,cz=-10,segments=80,rings=10;
  for(let ring=0;ring<=rings;ring++)for(let i=0;i<=segments;i++){
   const ang=i/segments*Math.PI*2,r=ring/rings*185*(1+.04*Math.sin(5*ang)+.03*Math.cos(9*ang)),x=cx+Math.cos(ang)*r,z=cz+Math.sin(ang)*r;
   let y=-.5;if(ring>8)y-=Math.pow((ring-8)/2,2)*5;gv.push([x,y,z]);guv.push([x*.22,z*.22]);
  }
  for(let j=0;j<rings;j++)for(let i=0;i<segments;i++){let a=j*(segments+1)+i,b=a+segments+1;gf.push([a,a+1,b],[a+1,b+1,b])}
  this.ground=this.mesh(gv,gf,track.config.palette.grass,guv,this.grassTexture,true);this.water=this.mesh([[-1200,-4.5,-1200],[1200,-4.5,-1200],[1200,-4.5,1200],[-1200,-4.5,1200]],[[0,2,1],[0,3,2]],track.config.palette.water,null,null,true);this.water.material.water=1;
  // Road-following embankments keep the elevated road supported and prevent
  // a coarse island mesh from intersecting the climbing sections.
  let sv=[],su=[],sf=[];for(const side of [-1,1]){const base=sv.length;for(let i=0;i<=N;i++){const p=track.point(i/N*track.length);for(let j=0;j<=4;j++){const t=j/4,d=5.45+16*t,x=p.x+p.rightX*side*d,z=p.z+p.rightZ*side*d;sv.push([x,(1-t)*(p.y+.02)+t*(-.49),z]);su.push([x*.22,z*.22])}}for(let i=0;i<N;i++)for(let j=0;j<4;j++){let a=base+i*5+j,b=a+5;sf.push([a,b,a+1],[a+1,b,b+1])}}
  this.shoulders=this.mesh(sv,sf,track.config.palette.grass,su,this.grassTexture,true);
  const shadowV=[],shadowUV=[],shadowF=[];
  const add=(file,s,lat,scale=1,yoff=0)=>{const p=track.place(s,lat),y=Math.abs(lat)>5.5?this.groundAt(p.x,p.z):p.y;this.static.push({file,matrix:transform(p.x,y+yoff,p.z,p.yaw,scale),s});
   if(Math.abs(lat)>5.5){const rx=(file==='prop_tree.glb'?3.0:1.3)*scale,rz=(file==='prop_tree.glb'?3.3:1.3)*scale,base=shadowV.length,x=p.x+.4*scale,z=p.z-.6*scale;
    for(const [dx,dz,u,v] of [[-rx,-rz,0,0],[rx,-rz,1,0],[rx,rz,1,1],[-rx,rz,0,1]]){shadowV.push([x+dx,this.groundAt(x+dx,z+dz)+.035,z+dz]);shadowUV.push([u,v])}shadowF.push([base,base+2,base+1],[base,base+3,base+2]);}
  };
  add('prop_start_gate.glb',0,0,1,0);add('prop_bridge.glb',track.length*.075,0,1,-.015);add('prop_tunnel.glb',track.length*.57,0,1,.1);
  const treeCount=track.id==='hutan'?46:track.id==='kapuas'?32:26;for(let i=0;i<treeCount;i++)add('prop_tree.glb',(i+.35)/treeCount*track.length,(i%2?1:-1)*(11+i%3*2),.85+(i%4)*.15,-.1);
  for(let i=0;i<40;i++)add('prop_rock.glb',(i+.7)/40*track.length,(i%2?1:-1)*(8.8+i%5*1.8),.55+(i%5)*.28,-.1);
  this.staticShadows=this.mesh(shadowV,shadowF,[.02,.03,.04],shadowUV,null,true);this.staticShadows.material.shadow=1;this.staticShadows.material.alpha=.18;
  this.makeTrackFeatures(track);this.scenery.build(track);this.shake=0;this.shakeCooldown=0;this.skidMarks=[];this.markCarry=0;this.eye=null;this.cameraTarget=null;this.cameraTime=0;this.clock=0;this.particles.length=0;this.fxTime=0;this.fxCooldown=0;this.fxTokens=0;this.fxImpact=0;this.dustCarry=0;this.nitroCarry=0;this.fov=60;
 }
 makeTrackFeatures(track){this.featureMeshes=[];this.features=[];const ramp=this.mesh([[-4,0,-2.5],[4,0,-2.5],[-4,.72,2.5],[4,.72,2.5],[-4,0,2.5],[4,0,2.5]],[[0,2,1],[1,2,3],[2,4,3],[3,4,5]],[.90,.59,.12],null,null,true),log=this.mesh([[-1.4,0,-.28],[1.4,0,-.28],[-1.4,.65,-.28],[1.4,.65,-.28],[-1.4,0,.28],[1.4,0,.28],[-1.4,.65,.28],[1.4,.65,.28]],[[0,2,1],[1,2,3],[4,5,6],[5,7,6],[2,6,3],[3,6,7],[0,4,2],[2,4,6],[1,3,5],[3,7,5]],[.27,.12,.035],null,null,true),grid=this.mesh([[-.8,0,-.6],[.8,0,-.6],[.8,0,.6],[-.8,0,.6]],[[0,2,1],[0,3,2]],[.96,.91,.69],null,null,true),chevron=this.mesh([[-1,0,-1],[0,0,0],[1,0,-1],[1,0,-.45],[0,0,.55],[-1,0,-.45]],[[0,1,5],[1,4,5],[1,2,3],[1,3,4]],[1,.87,.19],null,null,true);this.featureMeshes.push(ramp,log,grid,chevron);const add=(s,lat,mesh,file=null,scale=1)=>{const q=track.place(s,lat);this.features.push({s,mesh,file,matrix:transform(q.x,q.y+.12,q.z,q.yaw,scale)})};for(const o of track.obstacles){add(o.u*track.length,o.lateral,o.type==='log'?log:null,o.type==='rock'?'prop_rock.glb':null,o.type==='rock'?.55:1);add(o.u*track.length-9,o.lateral,chevron)}for(const u of track.config.ramps){add(u*track.length,0,ramp);for(let d=4;d<=10;d+=3)add(u*track.length-d,0,chevron)}for(let i=0;i<5;i++)add(i===4?0:4+(3-i)*3,i===4?1.8:i%2?1.8:-1.8,grid)}
 drawPrimitive(p,matrix,fog=1){
  if(this.depthPass){const gl=this.gl,L=this.SL;gl.uniformMatrix4fv(L.uModel,false,matrix);gl.uniform1f(L.uFoliage,p.material.foliage||0);gl.bindBuffer(gl.ARRAY_BUFFER,p.pos);gl.enableVertexAttribArray(L.aPos);gl.vertexAttribPointer(L.aPos,3,gl.FLOAT,false,0,0);gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,p.index);gl.drawElements(gl.TRIANGLES,p.count,p.type,0);return}
  const gl=this.gl,L=this.L,mat=p.material;gl.uniformMatrix4fv(L.uModel,false,matrix);
  for(const [name,b,n] of [['aPos',p.pos,3],['aNormal',p.normal,3],['aUV',p.uv,2]]){if(b){gl.bindBuffer(gl.ARRAY_BUFFER,b);gl.enableVertexAttribArray(L[name]);gl.vertexAttribPointer(L[name],n,gl.FLOAT,false,0,0)}else{gl.disableVertexAttribArray(L[name]);gl.vertexAttrib2f(L[name],0,0)}}
  gl.uniform3fv(L.uColor,mat.color);gl.uniform3fv(L.uPaint,this.paintMultiplier&&mat.metal>.1?this.paintMultiplier:[1,1,1]);gl.uniform1f(L.uOpacity,this.opacity??1);gl.uniform3fv(L.uEmissive,mat.emissive||[0,0,0]);gl.uniform1f(L.uRough,mat.rough??.5);gl.uniform1f(L.uMetal,mat.metal||0);gl.uniform1f(L.uFog,fog);gl.uniform1f(L.uAlpha,mat.alpha??1);gl.uniform1f(L.uHasTexture,mat.texture?1:0);gl.uniform1f(L.uShadow,mat.shadow||0);gl.uniform1f(L.uWater,mat.water||0);gl.uniform1f(L.uTime,this.clock||0);
  gl.uniform1f(L.uFoliage,mat.foliage||0);gl.uniform1f(L.uBubble,mat.bubble||0);gl.uniform1f(L.uOil,mat.oil||0);if(mat.texture){gl.activeTexture(gl.TEXTURE0);gl.bindTexture(gl.TEXTURE_2D,mat.texture);gl.uniform1i(L.uTexture,0)}if(mat.double)gl.disable(gl.CULL_FACE);else gl.enable(gl.CULL_FACE);gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,p.index);gl.drawElements(gl.TRIANGLES,p.count,p.type,0);
 }
 drawModel(file,matrix,{spin=0,steer=0,fog=1}={}){
  this.ensureModel(file);const model=this.models[file];
  const visit=(i,parent)=>{const n=model.doc.nodes[i];let world=M.mul(parent,M.trans(n.translation||[0,0,0]));if(/^wheel_f[lr]$/.test(n.name))world=M.mul(world,M.ry(steer));if(/wheel_.._spin$/.test(n.name))world=M.mul(world,M.rx(spin));for(const p of (this.depthPass?model.depthPrimitives:model.primitives)[i]||[])this.drawPrimitive(p,world,fog);for(const c of n.children||[])visit(c,world)};visit(0,matrix);
 }
 begin(eye,target,fog=1){
  const gl=this.gl,c=this.canvas;const dpr=Math.min(window.devicePixelRatio||1,this.pixelScale),w=Math.max(1,Math.round(c.clientWidth*dpr)),h=Math.max(1,Math.round(c.clientHeight*dpr));if(c.width!==w||c.height!==h){c.width=w;c.height=h}gl.viewport(0,0,w,h);gl.clearColor(0,0,0,0);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);gl.useProgram(this.prog);this.view=look(eye,target);this.projection=perspective(w/h,fog?this.fov:52);gl.uniformMatrix4fv(this.L.uLightMatrix,false,this.lightMatrix||M.identity());gl.uniformMatrix4fv(this.L.uView,false,this.view);gl.uniformMatrix4fv(this.L.uProjection,false,this.projection);gl.uniform3fv(this.L.uEye,eye);gl.uniform1f(this.L.uWeather,this.weather==='rain'?1:this.weather==='fog'?2:0);gl.uniform3fv(this.L.uFogColor,this.stage?.palette.fog||[.43,.70,.78]);if(fog)this.drawSky(eye,target);
 }
 garage(character,time){if(this.garageCharacter!==character){this.prepareModels([KARTS[character]]);this.garageCharacter=character}this.weather='clear';this.begin([Math.sin(.4+time*.12)*3.8,2.1,Math.cos(.4+time*.12)*3.8],[0,.95,0],0);this.gl.uniform1f(this.L.uSunEnabled,0);this.drawModel(KARTS[character],M.identity(),{fog:0})}
 race(session,dt,input={},alpha=1){
  if(this.preparedSession!==session){this.prepareModels([KARTS[session.character],...session.ai.map(a=>KARTS[a.character]),...(session.ghost?[KARTS[session.ghost.character]]:[])]);this.preparedSession=session;this.garageCharacter=null}this.paintMultiplier=null;this.weather=session.weather;this.updateVFX(session,input);
  this.clock=session.elapsed;const visualDt=session.status==='racing'?Math.max(0,Math.min(.05,dt)):Math.max(0,Math.min(.05,session.elapsed-this.cameraTime));this.cameraTime=session.elapsed;
  const blend=(now,prev)=>{if(session.status!=='racing'||!prev)return now;const a=Math.max(0,Math.min(1,alpha));return {...now,s:prev.s+(now.s-prev.s)*a,lateral:prev.lateral+(now.lateral-prev.lateral)*a,y:(prev.y||0)+((now.y||0)-(prev.y||0))*a,error:(prev.error||0)+((now.error||0)-(prev.error||0))*a,steering:(prev.steering||0)+((now.steering||0)-(prev.steering||0))*a}};
  const tr=session.track,p=blend(session.player,session.previousPlayer),pos=tr.place(p.s,p.lateral),yaw=pos.yaw+p.error;
  const desired=[pos.x-Math.sin(yaw)*6.8,pos.y+3.4,pos.z-Math.cos(yaw)*6.8],target=[pos.x+Math.sin(yaw)*5,pos.y+1.0,pos.z+Math.cos(yaw)*5];if(!this.eye)this.eye=desired.slice();if(!this.cameraTarget)this.cameraTarget=target.slice();let smooth=1-Math.exp(-8*visualDt);this.eye=this.eye.map((v,i)=>v+(desired[i]-v)*smooth);this.cameraTarget=this.cameraTarget.map((v,i)=>v+(target[i]-v)*(1-Math.exp(-10*visualDt)));
  if(visualDt>0){if(session.collisionCooldown>this.shakeCooldown+.05)this.shake=.18;else if(session.lastEvent?.type==='land')this.shake=Math.max(this.shake,.07);this.shakeCooldown=session.collisionCooldown;this.shake*=Math.exp(-visualDt*9)}const jitter=(this.shake||0)+(session.buffs.turbo>0?.012:0);this.begin(this.eye.map((v,i)=>v+Math.sin(session.elapsed*(i?67:83))*jitter),this.cameraTarget);
  const slope=s=>-Math.atan2(tr.point(s+.75).y-tr.point(s-.75).y,1.5);this.renderSunShadows(session,pos,p,yaw,blend,slope);
  this.drawPrimitive(this.water,M.identity());this.drawPrimitive(this.ground,M.identity());this.drawPrimitive(this.shoulders,M.identity());this.drawPrimitive(this.road,M.identity());for(let mesh of this.curbs)this.drawPrimitive(mesh,M.identity());
  this.gl.depthMask(false);for(const m of this.skidMarks)if(Math.hypot(m.x-pos.x,m.z-pos.z)<55){this.tireMark.material.alpha=.35*Math.max(0,1-(session.elapsed-m.t)/8);this.drawPrimitive(this.tireMark,M.mul(transform(m.x,m.y,m.z,m.yaw),M.rx(slope(m.s))))}this.drawPrimitive(this.staticShadows,M.identity());this.gl.depthMask(true);this.scenery.draw(session.elapsed,pos);
  const local=RaceCore.mod(p.s,tr.length);const near=s=>{let d=Math.abs(s-local);return Math.min(d,tr.length-d)<this.viewDistance};
  for(const o of session.oils||[]){const q=tr.place(o.s,o.lateral);if(near(RaceCore.mod(o.s,tr.length)))this.drawPrimitive(this.oilMesh,M.mul(transform(q.x,q.y+.112,q.z,q.yaw),M.rx(slope(o.s))))}
  for(const o of this.features||[])if(near(o.s)){if(o.mesh)this.drawPrimitive(o.mesh,o.matrix);else this.drawModel(o.file,o.matrix)}
  for(const o of this.static)if(near(o.s))this.drawModel(o.file,o.matrix);
  const kartFiles=KARTS;
  for(const [i,actual] of session.ai.entries()){const a=blend(actual,session.previousAI?.[i]),q=tr.place(a.s,a.lateral);if(Math.hypot(q.x-pos.x,q.z-pos.z)<130){this.drawShadow(M.mul(transform(q.x,q.y+.105,q.z,q.yaw),M.rx(slope(a.s))));this.drawModel(kartFiles[a.character],M.mul(transform(q.x,q.y+.09+(a.y||0),q.z,q.yaw+(a.slip>0?Math.sin(this.clock*12)*.28:0)),M.rx(slope(a.s))),{spin:a.s/.205,steer:-tr.curvature(a.s)*3})}}
  if(session.ghost){const g=RaceCore.ghostPose(session.ghost,session.elapsed);if(g){const q=tr.place(g.s,g.lateral);this.opacity=.24;this.gl.depthMask(false);this.drawModel(KARTS[session.ghost.character],transform(q.x,q.y+.12+g.y,q.z,q.yaw+g.error));this.gl.depthMask(true);this.opacity=1}}
  this.drawShadow(M.mul(transform(pos.x,pos.y+.105,pos.z,yaw),M.rx(slope(p.s))));
  this.paintMultiplier=this.selectedPaint;this.drawModel(kartFiles[session.character],M.mul(M.mul(transform(pos.x,pos.y+.09+(p.y||0),pos.z,yaw),M.rx(slope(p.s))),M.rz((p.steering||0)*Math.min(1,p.speed/23)*(p.drifting?.10:.035))),{spin:p.s/.205,steer:-(p.steering||0)*.42});
  this.paintMultiplier=null;
  if(session.records.length<session.count){const gate=session.nextGate,gp=tr.point(gate);if(gate-p.s<100&&gate-p.s>-3)for(const lat of [-2.8,0,2.8]){const q=tr.place(gate,lat);this.drawModel('item_box.glb',transform(q.x,q.y+.65+Math.sin(session.elapsed*2)*.10,q.z,session.elapsed,1.15));}}
  const lap=Math.floor(p.s/tr.length),spacing=tr.length/22;for(let i=0;i<22;i++){const s=(i+.5)*spacing;if(!near(s)||session.collected.has(lap*22+i))continue;const q=tr.place(s,i%2?2.4:-2.4);this.drawModel('token.glb',transform(q.x,q.y+.7,q.z,session.elapsed*2,1.6))}
  if(p.bubble>0){this.gl.depthMask(false);this.drawPrimitive(this.bubbleMesh,transform(pos.x,pos.y+1+(p.y||0),pos.z,session.elapsed,1.2));this.gl.depthMask(true)}
  if(session.buffs.shield>0)this.drawPrimitive(this.ring,transform(pos.x,pos.y+.18,pos.z,session.elapsed,1.05));
  if(session.buffs.magnet>0){this.ring.material.color=[.50,.10,.65];this.drawPrimitive(this.ring,transform(pos.x,pos.y+.12,pos.z,session.elapsed,1.35));this.ring.material.color=[.04,.65,.85]}
  if(session.buffs.turbo>0&&p.speed>1){const gl=this.gl,pulse=1+.12*Math.sin(session.elapsed*55);gl.depthMask(false);gl.blendFunc(gl.SRC_ALPHA,gl.ONE);for(const side of [-1,1]){const q=M.mul(transform(pos.x,pos.y+.43,pos.z,yaw),M.trans([side*.31,0,-.80]));this.flame.material.color=[.02,.3,1];this.flame.material.emissive=[.08,.55,1];this.drawPrimitive(this.flame,M.mul(q,M.scale(pulse)));this.flame.material.color=[.7,.95,1];this.flame.material.emissive=[.7,.95,1];this.drawPrimitive(this.flame,M.mul(q,M.scale(.58*pulse)))}gl.depthMask(true);gl.blendFunc(gl.SRC_ALPHA,gl.ONE_MINUS_SRC_ALPHA)}
  this.gl.depthMask(false);for(const b of session.bubbles||[]){const q=tr.place(b.s,b.lateral);this.drawPrimitive(this.bubbleMesh,transform(q.x,q.y+.75,q.z,session.elapsed,.5))}for(const a of session.ai)if(a.bubble>0){const q=tr.place(a.s,a.lateral);this.drawPrimitive(this.bubbleMesh,transform(q.x,q.y+.95,q.z,session.elapsed,1.2))}this.gl.depthMask(true);this.drawParticles();
 }
}
root.RaceRenderer=Renderer;root.RaceMath=M;
})(typeof globalThis!=='undefined'?globalThis:this);
