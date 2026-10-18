"""Tabby kitten redesign, game Y-up. Executed in the Blender builder context.
Shape language: wide cheek apples, tapered heart jaw, canted almond eyes,
cupped outward ears, compact torso, curled digits and a tapering S-tail.
"""
HEAD_SECTIONS=[(.963,0,.132,.132),(.987,.108,.236,-.070),
 (1.030,.233,.279,-.203),(1.095,.344,.277,-.307),
 (1.175,.387,.244,-.354),(1.275,.373,.220,-.374),
 (1.390,.326,.194,-.352),(1.500,.263,.123,-.294),
 (1.590,.148,-.008,-.207),(1.628,0,-.109,-.109)]

def catmull(a,b,c,d,t):
 return .5*(2*b+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t)

def head_profile(y):
 base=[0,-.109,-.109]
 for i in range(len(HEAD_SECTIONS)-1):
  b,c=HEAD_SECTIONS[i:i+2]
  if y<=c[0]:
   a=HEAD_SECTIONS[max(0,i-1)];d=HEAD_SECTIONS[min(len(HEAD_SECTIONS)-1,i+2)];t=max(0,min(1,(y-b[0])/(c[0]-b[0])))
   base=[catmull(a[k],b[k],c[k],d[k],t) for k in range(1,4)];break
 if y>1.32:
  factor=math.sqrt(max(0,1-((y-1.40)/.228)**2))
  cap=[.322*factor,-.080+.267*factor,-.080-.267*factor]
  t=max(0,min(1,(y-1.32)/.20));t=t*t*(3-2*t)
  return [a*(1-t)+b*t for a,b in zip(base,cap)]
 return base

def gauss(x,c,w):return math.exp(-((x-c)/w)**2)
def facial_volume(x,y):
 # Muzzle and brow volumes belong to the skull itself, not attached balls.
 cheeks=.038*(gauss(x,-.113,.115)+gauss(x,.113,.115))*gauss(y,1.145,.085)
 bridge=.026*gauss(x,0,.052)*gauss(y,1.255,.105)
 orbit=-.012*(gauss(x,-.160,.117)+gauss(x,.160,.117))*gauss(y,1.323,.104)
 return cheeks+bridge+orbit

def face_z(x,y):
 w,front,back=head_profile(y);s=math.sqrt(max(.001,1-(x/max(.001,w))**2))
 return (front+back)/2+(front-back)/2*s+facial_volume(x,y)*s**4

def smooth_path(points,radii,steps=7):
 pts=[];rs=[]
 for j in range(len(points)-1):
  a,b,c,d=points[max(0,j-1)],points[j],points[j+1],points[min(len(points)-1,j+2)]
  for i in range(steps):
   t=i/steps;pts.append(tuple(catmull(a[k],b[k],c[k],d[k],t) for k in range(3)))
   rs.append(catmull(radii[max(0,j-1)],radii[j],radii[j+1],radii[min(len(points)-1,j+2)],t))
 return pts+[points[-1]],rs+[radii[-1]]

def curved_tube(name,points,radii,material,sides=16,steps=7,group=None):
 p,r=smooth_path(points,radii,steps);return tube(name,p,r,material,sides,group)

def patch(name,coords,material,group='driver',rings=10,segments=48):
 v=[];f=[]
 for j in range(rings+1):
  r=j/rings
  for i in range(segments):
   a=math.tau*i/segments;v.append(coords(r*math.cos(a),r*math.sin(a),r))
 for j in range(rings):
  for i in range(segments):
   a=j*segments+i;b=j*segments+(i+1)%segments;f.append((a,a+segments,b+segments,b))
 # Winding is corrected per connected patch, including mirrored eye patches.
 o=mesh(name,v,f,material,group=group)
 if sum(p.normal.z for p in o.data.polygons)<0:
  import bmesh
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.reverse_faces(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update()
 return o

GROUP='driver'
# Analytic skull: actual cheek projection, tapered lower jaw, shorter chin.
v=[];f=[];rings=44;segments=64
for j in range(rings+1):
 y=.963+(1.628-.963)*j/rings;w,front,back=head_profile(y)
 for k in range(segments):
  a=k*math.tau/segments;x=w*math.cos(a)
  flare=.012*gauss(y,1.145,.060)*abs(math.cos(a))**8
  x+=math.copysign(flare,x)
  z=(front+back)/2+(front-back)/2*math.sin(a)+facial_volume(x,y)*max(0,math.sin(a))**4
  v.append((x,y,z))
for j in range(rings):
 for k in range(segments):
  a=j*segments+k;b=j*segments+(k+1)%segments;f.append((a,a+segments,b+segments,b))
head=mesh('Cat — heart-shaped cheek and jaw sculpt',v,f,orange)
# Compact torso and tapered arms. The head retains its analytic topology;
# only the smaller torso/limb volume is fused, at a bounded resolution.
skin=[ell('Cat — compact seated ribcage',(0,.739,-.193),(.186,.223,.155),orange,32,20),
 ell('Cat — short soft neck',(0,.936,-.128),(.126,.105,.123),orange,28,18),
 ell('Cat — seated haunches',(0,.562,-.168),(.202,.112,.155),orange,28,18)]
for side in [-1,1]:
 skin.append(ell('Cat — folded thigh',(side*.121,.548,-.097),(.098,.091,.160),orange,24,16))
 skin.append(curved_tube('Cat — shoulder elbow wrist sweep',[(side*.137,.887,-.151),(side*.201,.858,-.133),(side*.247,.791,-.028),(side*.224,.809,.109),(side*.180,.835,.225)],[.073,.071,.062,.052,.039],orange,20,7))
 skin.append(ell('Cat — grip palm',(side*.181,.840,.234),(.056,.044,.052),orange,28,18))
 for dx in [-.024,0,.024]:
  x=side*.180+dx
  skin.append(curved_tube('Cat — curled grip digit',[(x,.863,.247),(x,.852,.274),(x,.829,.278),(x,.817,.258)],[.016,.017,.014,.010],orange,12,5))
 skin.append(curved_tube('Cat — opposed thumb',[(side*.148,.846,.213),(side*.137,.826,.233),(side*.154,.812,.257)],[.025,.022,.014],orange,14,6))
 ell('Cat — small fitted shoe',(side*.126,.452,.025),(.083,.059,.133),navy,24,16)
bpy.ops.object.select_all(action='DESELECT')
for o in skin:o.select_set(True)
bpy.context.view_layer.objects.active=skin[0];bpy.ops.object.join();body=bpy.context.object
body.name='Cat — fused compact body and articulated grip';body['pivot']='driver';body.data.remesh_voxel_size=.0105
bpy.ops.object.voxel_remesh()
sm=body.modifiers.new('Relax joins only','SMOOTH');sm.factor=.8;sm.iterations=3;bpy.ops.object.modifier_apply(modifier=sm.name)
de=body.modifiers.new('Bounded body topology','DECIMATE');de.ratio=.36;bpy.ops.object.modifier_apply(modifier=de.name)
for p in body.data.polygons:p.use_smooth=True
# Fitted chest bib, broader at its base, not an extra belly volume.
def chest(u,v,r):
 x=.111*u;y=.774+.139*v;z=-.193+.155*math.sqrt(max(.01,1-(x/.186)**2-((y-.739)/.223)**2))+.003
 return x,y,z
patch('Cat — cream chest bib',chest,cream,rings=10,segments=40)
# Eye anatomy: outward-canted almond openings, less exposed sclera, deep iris.
pupil=mat('16_Deep_teal_pupil','15292A',.24)
def eye_xy(side,u,v):return side*(.158+.126*u),1.322+.106*v*(.95-.09*abs(u))+.012*u

def eye_z(x,y,side,offset=0):
 u=(side*x-.158)/.126;v=(y-1.322-.012*u)/(.106*(.95-.09*abs(u)))
 return face_z(x,y)+.004+.032*max(0,1-u*u-v*v)**.7+offset
for side in [-1,1]:
 def eye_surface(u,v,r,side=side):
  x,y=eye_xy(side,u,v);return x,y,eye_z(x,y,side)
 patch('Cat — almond sclera',eye_surface,cream,'eyes',12,56)
 def iris_surface(u,v,r,side=side):
  x,y=eye_xy(side,-.04+.61*u,.01+.82*v);return x,y,eye_z(x,y,side,.0025)
 patch('Cat — honey iris',iris_surface,iris,'eyes',10,48)
 def pupil_surface(u,v,r,side=side):
  x,y=eye_xy(side,-.04+.315*u,.015+.66*v);return x,y,eye_z(x,y,side,.0045)
 patch('Cat — deep living pupil',pupil_surface,pupil,'eyes',10,40)
 for dx,dy,sx,sy in [(-.020,.031,.014,.021),(.016,-.029,.005,.008)]:
  x=side*(.158-.04*.126)+dx;y=1.322+dy
  ell('Cat — eye catchlight',(x,y,eye_z(x,y,side,.009)),(sx,sy,.0035),glint,16,10,group='eyes')
 for upper in [True,False]:
  points=[];radii=[]
  for j in range(29):
   a=(0 if upper else math.pi)+math.pi*j/28;x,y=eye_xy(side,math.cos(a),math.sin(a))
   points.append((x,y,face_z(x,y)+.005));radii.append((.004 if upper else .002)+(.009 if upper else .005)*math.sin(math.pi*j/28)**.7)
  tube('Cat — sculpted eyelid',points,radii,orange,12)
 # Friendly raised inner brow, no heavy angular moustache over the eyes.
 points=[]
 for x,y in [(side*.064,1.443),(side*.145,1.477),(side*.247,1.456)]:points.append((x,y,face_z(x,y)+.004))
 curved_tube('Cat — expressive brow',points,[.003,.008,.001],stripe,10,7)
# A heart-like cream mask traces the actual cheek/muzzle volumes of the skull.
def muzzle_surface(u,v,r):
 x=.226*u;y=1.153+.080*v+.008*gauss(abs(x),.110,.070)
 return x,y,face_z(x,y)+.0035
patch('Cat — sculpted whisker muzzle',muzzle_surface,cream,rings=15,segments=64)
# Radial polygon patch, using a smooth closed contour and a domed surface.
def outline_patch(name,points,material,offset=.006,dome=0,group='driver',rings=10):
 center=sum((Vector((x,y)) for x,y in points),Vector((0,0)))/len(points)
 boundary=[]
 for j in range(len(points)):
  a,b,c,d=points[(j-1)%len(points)],points[j],points[(j+1)%len(points)],points[(j+2)%len(points)]
  for k in range(5):boundary.append(tuple(catmull(a[i],b[i],c[i],d[i],k/5) for i in range(2)))
 v=[];f=[];n=len(boundary)
 for j in range(rings+1):
  r=j/rings
  for xy in boundary:
   q=center+(Vector(xy)-center)*r;x,y=q
   v.append((x,y,face_z(x,y)+offset+dome*(1-r*r)))
 for j in range(rings):
  for k in range(n):
   a=j*n+k;b=j*n+(k+1)%n;f.append((a,a+n,b+n,b))
 o=mesh(name,v,f,material,group=group)
 if sum(p.normal.z for p in o.data.polygons)<0:
  import bmesh
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.reverse_faces(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update()
 return o
outline_patch('Cat — upward smiling mouth',[(-.143,1.105),(-.089,1.083),(0,1.080),(.089,1.083),(.143,1.105),(.101,1.045),(.043,1.016),(0,1.010),(-.043,1.016),(-.101,1.045)],pupil,.008)
patch('Cat — tongue in smile',lambda u,v,r:(.040*u,1.037+.016*v,face_z(.040*u,1.037+.016*v)+.011),pink,rings=8,segments=32)
# Two small incisors catch the upper lip; they are rounded shallow relief.
for side in [-1,1]:
 patch('Cat — tiny smile tooth',lambda u,v,r,side=side:(side*.023+.018*u,1.073+.010*v,face_z(side*.023+.018*u,1.073+.010*v)+.012),cream,rings=6,segments=24)
outline_patch('Cat — heart triangle nose',[(-.037,1.210),(-.015,1.215),(0,1.209),(.015,1.215),(.037,1.210),(.027,1.190),(0,1.171),(-.027,1.190)],pink,.009,.018,rings=8)
curved_tube('Cat — philtrum',[(0,1.176,face_z(0,1.176)+.008),(0,1.152,face_z(0,1.152)+.007),(0,1.127,face_z(0,1.127)+.006)],[.0025,.002,.0008],stripe,8,6)
for side in [-1,1]:
 for j in range(3):
  x=side*(.123+j*.024);y=1.154-j*.015
  ell('Cat — whisker freckles',(x,y,face_z(x,y)+.006),(.0035,.003,.0015),stripe,12,8)
# Closed cupped ears with outward sweeping tips and a rolled rim. Not a flat triangle.
for side,key in [(-1,'ear_l'),(1,'ear_r')]:
 boundary2=[(.125,1.457),(.201,1.574),(.385,1.809),(.424,1.824),(.435,1.767),(.422,1.588),(.401,1.453),(.316,1.432)]
 points=[]
 for j in range(len(boundary2)):
  a,b,c,d=boundary2[(j-1)%len(boundary2)],boundary2[j],boundary2[(j+1)%len(boundary2)],boundary2[(j+2)%len(boundary2)]
  for i in range(5):points.append((side*catmull(a[0],b[0],c[0],d[0],i/5),catmull(a[1],b[1],c[1],d[1],i/5)))
 points=[(x*.96,1.46+(y-1.46)*.82) for x,y in points]
 if sum(points[i][0]*points[(i+1)%len(points)][1]-points[(i+1)%len(points)][0]*points[i][1] for i in range(len(points)))<0:points.reverse()
 center=sum((Vector(q) for q in points),Vector((0,0)))/len(points);n=len(points);nr=9;v=[];f=[]
 def ear_z(x,y):return -.065-.105*(y-1.46)/.30+.026*gauss(y,1.73,.07)-.075*gauss(y,1.455,.11)
 for back in [False,True]:
  for j in range(nr+1):
   r=j/nr
   for q in points:
    x,y=center+(Vector(q)-center)*r
    z=ear_z(x,y)+(-.028-.034*(1-r*r) if back else .018+.035*r*r)
    v.append((x,y,z))
 count=(nr+1)*n
 for off in [0,count]:
  for j in range(nr):
   for k in range(n):
    a=off+j*n+k;b=off+j*n+(k+1)%n;face=(a,a+n,b+n,b);f.append(face if not off else tuple(reversed(face)))
 for k in range(n):a=nr*n+k;b=nr*n+(k+1)%n;f.append((a,b,b+count,a+count))
 mesh('Cat — swept cupped ear',v,f,orange,group=key)
 v=[];f=[]
 for j in range(nr+1):
  r=j/nr
  for q in points:
   x,y=center+(Vector(q)-center)*r*.73
   z=ear_z(x,y)+.020+.035*(r*.73)**2
   v.append((x,y,z))
 for j in range(nr):
  for k in range(n):a=j*n+k;b=j*n+(k+1)%n;f.append((a,a+n,b+n,b))
 mesh('Cat — velvet ear concha',v,f,pink,group=key)

def redesigned_tail():
 p,r=smooth_path([(0,.659,-.383),(-.14,.705,-.50),(-.37,.830,-.65),(-.50,1.020,-.66),(-.52,1.190,-.60),(-.475,1.285,-.53),(-.43,1.250,-.52)], [.057,.056,.052,.047,.038,.027,.010],7)
 tube('Cat — tapering S tail',p,r,orange,18,group='tail')
 # Color bands are fitted to the same swept surface and taper with the tail.
 for a,b in [(10,13),(23,26),(35,38)]:tube('Cat — tail tabby band',p[a:b+1],[x+.0009 for x in r[a:b+1]],stripe,18,group='tail')

def refined_markings():
 for side in [-1,1]:
  for index in range(3):
   ph=(.88+index*.43) if side==1 else (math.pi-.88-index*.43)
   v=[];f=[]
   for i in range(21):
    t=i/20;y=1.594-(.137+index*.009)*t;w,front,back=head_profile(y)
    for s in [-1,1]:
     a=ph+s*.072*math.sin(math.pi*t)**.65;x=(w+.0016)*math.cos(a);z=(front+back)/2+((front-back)/2+.0016)*math.sin(a)+facial_volume(x,y)*max(0,math.sin(a))**4
     v.append((x,y,z))
   for i in range(20):f.append((2*i,2*i+1,2*i+3,2*i+2))
   mesh('Cat — forehead tabby M stroke',v,f,stripe,group='driver')
 # Rear crown stripes keep the kitten readable from the chase camera.
 for ph in [3.65,4.15,4.7,5.25,5.75]:
  v=[];f=[]
  for i in range(21):
   t=i/20;y=1.592-.293*t;w,front,back=head_profile(y)
   for s in [-1,1]:
    a=ph+s*.055*math.sin(math.pi*t)**.7;v.append(((w+.0015)*math.cos(a),y,(front+back)/2+((front-back)/2+.0015)*math.sin(a)))
  for i in range(20):f.append((2*i,2*i+1,2*i+3,2*i+2))
  mesh('Cat — tapered rear crown tabby',v,f,stripe,group='driver')
 for side in [-1,1]:
  for yy in [1.159,1.218]:
   pts=[]
   for j in range(17):
    t=j/16;x=side*(.328-.089*t);y=yy+.013*math.sin(math.pi*t);pts.append((x,y,face_z(x,y)+.002))
   tube('Cat — cheek tabby sweep',pts,[.0005+.006*math.sin(math.pi*j/16) for j in range(17)],stripe,8,group='driver')

def refined_back_markings():
 from mathutils.bvhtree import BVHTree
 bpy.context.view_layer.update();tree=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get())
 for yy in [.673,.762,.844]:
  v=[];f=[]
  for j in range(21):
   t=j/20;x=-.145+.29*t
   for side in [-1,1]:
    y=yy+.011*math.sin(math.pi*t)+side*.007*math.sin(math.pi*t);hit,*_=tree.ray_cast(Vector((x,y,-1)),Vector((0,0,1)))
    assert hit is not None;v.append((x,y,hit.z-.001))
  for j in range(20):f.append((2*j,2*j+1,2*j+3,2*j+2))
  mesh('Cat — fitted back tabby',v,f,stripe,group='driver')

def linear_hex(h):
 vals=[int(h[i:i+2],16)/255 for i in (0,2,4)]
 return [v/12.92 if v<.04045 else ((v+.055)/1.055)**2.4 for v in vals]
def blend(a,b,t):return [x*(1-t)+y*t for x,y in zip(a,b)]
def cat_color(o,p):
 x,y,z=p;name=o.data.materials[0].name;kind=int(name[:2]);original=MATS[name]['pbrMetallicRoughness']['baseColorFactor'][:3]
 if kind==10:
  color=linear_hex('E7973D');crown=gauss(y,1.56,.18);color=blend(color,linear_hex('D47726'),crown*.65)
  cheek=gauss(y,1.15,.13)*max(0,min(1,(z+.05)/.3));color=blend(color,linear_hex('F6BC76'),cheek*.67)
  paw=gauss(y,.850,.048)*gauss(z,.261,.065);color=blend(color,linear_hex('F1C480'),paw*.72)
  return color
 if kind==11:
  color=linear_hex('FFF0D2');edge=0
  if 'muzzle' in o.name:
   rr=math.sqrt((x/.226)**2+((y-1.153)/.080)**2);edge=max(0,min(1,(rr-.68)/.32))*.5
  return blend(color,linear_hex('EDB56F'),edge)
 if kind==12:return linear_hex('965020')
 if kind==13:
  if 'ear' in o.name:return blend(linear_hex('B96D70'),linear_hex('F3BEAC'),max(0,min(1,(y-1.50)/.28)))
  return linear_hex('CB8586')
 if kind==14:
  return blend(linear_hex('875020'),linear_hex('EFBE46'),max(0,min(1,(1.38-y)/.13)))
 if kind==16:return linear_hex('12292B')
 return original

def clean_cat_surfaces():
 import bmesh
 for o in list(bpy.context.scene.objects):
  if o.type=='MESH' and o.name.startswith('Cat —'):
   bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.0000005);bm.to_mesh(o.data);bm.free();o.data.update()
   for p in o.data.polygons:p.use_smooth=True
   material=o.data.materials[0]
   if int(material.name[:2])>=10:
    attr=o.data.color_attributes.new(name='CatGradient',type='FLOAT_COLOR',domain='POINT')
    for i,v in enumerate(o.data.vertices):attr.data[i].color=(*cat_color(o,tuple(o.matrix_world@v.co)),1)
    material.use_nodes=True;nodes=material.node_tree.nodes;shader=nodes.get('Principled BSDF');vc=nodes.get('CatGradient') or nodes.new('ShaderNodeVertexColor');vc.name='CatGradient';vc.layer_name='CatGradient';material.node_tree.links.new(vc.outputs['Color'],shader.inputs['Base Color'])
