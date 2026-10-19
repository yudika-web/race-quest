from pathlib import Path
import re,json,hashlib
D=Path(__file__).resolve().parents[2];B=D/'sky-horizon';base=(D/'race-quest-pro-patch4-5.html').read_text();h=base;changes=[]
def change(old,new):
 global h
 assert h.count(old)==1,(old[:80],h.count(old));offset=h.index(old);h=h.replace(old,new);changes.append(dict(offset=offset,old=old,new=new))
a=h.index(' initSky(shader){');b=h.index(' emitParticle(',a)
change(h[a:b],(B/'source/sky-methods.js').read_text())
old='float fog=clamp((distance(uEye,vWorld)-mix(105.0,23.0,step(1.5,uWeather)))/mix(290.0,85.0,step(1.5,uWeather)),0.0,1.0)*uFog;'
new='''float horizonDistance=length(vWorld.xz-uEye.xz);
 float horizonSlope=abs(vWorld.y-uEye.y)/max(1.0,horizonDistance);
 float atmosphere=smoothstep(65.0,230.0,horizonDistance)*(1.0-smoothstep(.015,.18,horizonSlope));
 float fog=max(clamp((distance(uEye,vWorld)-mix(105.0,23.0,step(1.5,uWeather)))/mix(290.0,85.0,step(1.5,uWeather)),0.0,1.0),atmosphere)*uFog;'''
change(old,new)
old="gl.uniform3fv(this.L.uFogColor,this.stage?.palette.fog||[.43,.70,.78]);if(fog)this.drawSky(eye,target);"
new="const horizon=this.skyPalette().horizon;gl.uniform3fv(this.L.uFogColor,fog?horizon.map(v=>{const l=Math.pow(v,2.2);return l/(1-.24*l)}):(this.stage?.palette.fog||[.43,.70,.78]));if(fog)this.drawSky(eye,target);"
change(old,new)
(D/'race-quest-pro-sky-horizon.html').write_text(h)
(B/'bounded-changes.json').write_text(json.dumps(changes,indent=2));(B/'baseline.json').write_text(json.dumps(dict(commit='b5611f4937c6139024779265f0b8434545b77cbf',bytes=len(base.encode()),sha256=hashlib.sha256(base.encode()).hexdigest()),indent=2));print('HTML bytes',len(h.encode()),'growth',len(h.encode())-len(base.encode()))
