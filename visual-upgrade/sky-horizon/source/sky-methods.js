 // Sky geometry is camera-relative, static, and never participates in collision.
 skyPalette(){
  const id=this.track?.id;
  const p=id==='kapuas'?{top:[.29,.62,.83],horizon:[.79,.88,.88]}:id==='hutan'?{top:[.22,.64,.89],horizon:[.78,.89,.93]}:{top:[.30,.61,.85],horizon:[.84,.88,.89]};
  const w=this.weather==='rain'?.55:this.weather==='fog'?.75:0;
  return{top:p.top.map((v,i)=>v*(1-w)+[.47,.57,.64][i]*w),horizon:p.horizon.map((v,i)=>v*(1-w)+[.73,.79,.81][i]*w)};
 }
 initSky(shader){
  const gl=this.gl;
  const program=(vs,fs)=>{const p=gl.createProgram();gl.attachShader(p,shader(gl.VERTEX_SHADER,vs));gl.attachShader(p,shader(gl.FRAGMENT_SHADER,fs));gl.linkProgram(p);if(!gl.getProgramParameter(p,gl.LINK_STATUS))throw Error('Sky shader: '+gl.getProgramInfoLog(p));return p};
  this.skyProgram=program(`attribute vec2 aSkyPos;varying vec2 vSkyCoord;void main(){vSkyCoord=aSkyPos;gl_Position=vec4(aSkyPos,.9999,1.0);}`,`precision highp float;varying vec2 vSkyCoord;uniform vec3 uSkyRight,uSkyUp,uSkyForward,uSkyTop,uSkyHorizon;uniform float uSkyAspect,uSkyTan;void main(){vec3 ray=normalize(uSkyForward+uSkyRight*vSkyCoord.x*uSkyAspect*uSkyTan+uSkyUp*vSkyCoord.y*uSkyTan);float h=smoothstep(-.025,.64,ray.y);vec3 c=mix(uSkyHorizon,uSkyTop,h);gl_FragColor=vec4(c,1.0);}`);
  this.KL={aSkyPos:gl.getAttribLocation(this.skyProgram,'aSkyPos')};for(const n of ['uSkyRight','uSkyUp','uSkyForward','uSkyAspect','uSkyTan','uSkyTop','uSkyHorizon'])this.KL[n]=gl.getUniformLocation(this.skyProgram,n);
  this.skyBuffer=this.buffer(new Float32Array([-1,-1,3,-1,-1,3]));
  this.cloudProgram=program(`attribute vec3 aCloudPos;attribute float aCloudShade;uniform mat4 uCloudView,uCloudProjection;varying float vShade,vHeight;void main(){vShade=aCloudShade;vHeight=normalize(aCloudPos).y;gl_Position=uCloudProjection*vec4(mat3(uCloudView)*aCloudPos,1.0);}`,`precision mediump float;varying float vShade,vHeight;uniform vec3 uCloudHorizon;uniform float uCloudWeather;void main(){vec3 c=mix(vec3(.99,.985,.96),vec3(.74,.83,.88),vShade);c=mix(c,uCloudHorizon,(1.0-smoothstep(.02,.22,vHeight))*.75+.08);c=mix(c,c*.84,uCloudWeather);gl_FragColor=vec4(c,1.0);}`);
  this.CL={aCloudPos:gl.getAttribLocation(this.cloudProgram,'aCloudPos'),aCloudShade:gl.getAttribLocation(this.cloudProgram,'aCloudShade')};for(const n of ['uCloudView','uCloudProjection','uCloudHorizon','uCloudWeather'])this.CL[n]=gl.getUniformLocation(this.cloudProgram,n);
  const V=[],I=[],counts=[];
  // Rounded rectangular rings create chamfered cloud blocks: 60 triangles/block.
  const block=(cx,cy,cz,w,h,d,yaw)=>{const start=V.length/4,cs=Math.cos(yaw),sn=Math.sin(yaw),b=Math.min(h*.22,w*.1,d*.16);
   for(const [y,inset,shade]of [[-h/2,b,.78],[-h/2+b,0,.52],[h/2-b,0,.20],[h/2,b,.02]]){
    const x=w/2-inset,z=d/2-inset,k=b*.8;
    for(const [px,pz]of [[-x+k,-z],[x-k,-z],[x,-z+k],[x,z-k],[x-k,z],[-x+k,z],[-x,z-k],[-x,-z+k]])V.push(cx+px*cs+pz*sn,cy+y,cz-px*sn+pz*cs,shade);
   }
   for(let r=0;r<3;r++)for(let k=0;k<8;k++){const a=start+r*8+k,b=start+r*8+(k+1)%8;I.push(a,b,a+8,b,b+8,a+8)}
   for(let k=1;k<7;k++){I.push(start,start+k+1,start+k);I.push(start+24,start+24+k,start+24+k+1)}
  };
  // Golden-angle order keeps every LOD spread across the full 360-degree sky.
  for(let i=0;i<18;i++){
   const a=i*2.39996323,r=230+(i%3)*18,h=35+(i%5)*11,cx=Math.sin(a)*r,cz=Math.cos(a)*r,w=24+(i%4)*5;
   block(cx,h,cz,w,7+(i%3),13,a);block(cx+Math.cos(a)*w*.37,h+4,cz-Math.sin(a)*w*.37,w*.57,10,12,a);block(cx-Math.cos(a)*w*.34,h+2,cz+Math.sin(a)*w*.34,w*.48,8,11,a);
   counts.push(I.length);
  }
  this.cloudVertices=this.buffer(new Float32Array(V));this.cloudIndices=this.buffer(new Uint16Array(I),gl.ELEMENT_ARRAY_BUFFER);this.cloudCounts=counts;
  this.skyStats={groupsHigh:18,groupsLow:10,trianglesHigh:I.length/3,trianglesLow:counts[9]/3,gpuBytes:V.length*4+I.length*2,drawCalls:2,textures:0,animated:false};
 }
 drawSky(eye,target){
  const gl=this.gl,L=this.KL,palette=this.skyPalette(),z=norm(target.map((x,i)=>x-eye[i])),right=norm(cross(z,[0,1,0])),up=cross(right,z);
  gl.disable(gl.DEPTH_TEST);gl.depthMask(false);gl.disable(gl.BLEND);gl.disable(gl.CULL_FACE);
  for(const n of ['aPos','aNormal','aUV','aPaint'])gl.disableVertexAttribArray(this.L[n]);
  gl.useProgram(this.skyProgram);gl.bindBuffer(gl.ARRAY_BUFFER,this.skyBuffer);gl.enableVertexAttribArray(L.aSkyPos);gl.vertexAttribPointer(L.aSkyPos,2,gl.FLOAT,false,0,0);
  gl.uniform3fv(L.uSkyRight,right);gl.uniform3fv(L.uSkyUp,up);gl.uniform3fv(L.uSkyForward,z);gl.uniform3fv(L.uSkyTop,palette.top);gl.uniform3fv(L.uSkyHorizon,palette.horizon);gl.uniform1f(L.uSkyAspect,this.canvas.width/this.canvas.height);gl.uniform1f(L.uSkyTan,Math.tan(this.fov*Math.PI/360));gl.drawArrays(gl.TRIANGLES,0,3);gl.disableVertexAttribArray(L.aSkyPos);
  const C=this.CL;gl.useProgram(this.cloudProgram);gl.bindBuffer(gl.ARRAY_BUFFER,this.cloudVertices);gl.enableVertexAttribArray(C.aCloudPos);gl.vertexAttribPointer(C.aCloudPos,3,gl.FLOAT,false,16,0);gl.enableVertexAttribArray(C.aCloudShade);gl.vertexAttribPointer(C.aCloudShade,1,gl.FLOAT,false,16,12);gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,this.cloudIndices);gl.uniformMatrix4fv(C.uCloudView,false,this.view);gl.uniformMatrix4fv(C.uCloudProjection,false,this.projection);gl.uniform3fv(C.uCloudHorizon,palette.horizon);gl.uniform1f(C.uCloudWeather,this.weather==='clear'?0:1);gl.drawElements(gl.TRIANGLES,this.cloudCounts[this.quality==='low'?9:17],gl.UNSIGNED_SHORT,0);gl.disableVertexAttribArray(C.aCloudPos);gl.disableVertexAttribArray(C.aCloudShade);
  gl.activeTexture(gl.TEXTURE0);gl.depthMask(true);gl.enable(gl.DEPTH_TEST);gl.enable(gl.BLEND);gl.useProgram(this.prog);
 }
