"""Organic cat refinement, executed by build_cat.py in the shared Blender context.
Only driver / eyes / ears are authored here. Car geometry and material definitions
remain in build_cat.py without modification. All coordinates are game Y-up.
"""

# Smooth cross-sections define a pear-shaped skull, integrated jaw and chin.
# (height, half width, front depth, back depth)
HEAD_SECTIONS=[(.965,0,.035,.035),(.985,.095,.145,-.115),
 (1.025,.184,.218,-.270),(1.085,.267,.237,-.340),
 (1.160,.322,.211,-.373),(1.245,.334,.185,-.381),
 (1.330,.323,.174,-.365),(1.410,.288,.143,-.328),
 (1.485,.220,.085,-.269),(1.545,.126,-.006,-.196),
 (1.578,0,-.101,-.101)]

def catmull(a,b,c,d,t):
 return .5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t)

def head_profile(y):
 for i in range(len(HEAD_SECTIONS)-1):
  b,c=HEAD_SECTIONS[i:i+2]
  if y<=c[0]:
   a=HEAD_SECTIONS[max(0,i-1)];d=HEAD_SECTIONS[min(len(HEAD_SECTIONS)-1,i+2)]
   t=max(0,min(1,(y-b[0])/(c[0]-b[0])))
   return [catmull(a[k],b[k],c[k],d[k],t) for k in range(1,4)]
 return [0,-.101,-.101]

def face_z(x,y):
 w,front,back=head_profile(y)
 return (front+back)*.5+(front-back)*.5*math.sqrt(max(.001,1-(x/max(.001,w))**2))

def smooth_path(points,radii,steps=8):
 pts=[];rs=[]
 for j in range(len(points)-1):
  a=points[max(0,j-1)];b=points[j];c=points[j+1];d=points[min(len(points)-1,j+2)]
  for i in range(steps):
   t=i/steps;pts.append(tuple(catmull(a[k],b[k],c[k],d[k],t) for k in range(3)))
   rs.append(catmull(radii[max(0,j-1)],radii[j],radii[j+1],radii[min(len(points)-1,j+2)],t))
 pts.append(points[-1]);rs.append(radii[-1]);return pts,rs

def curved_tube(name,points,radii,material,sides=20,steps=8,group=None):
 pts,rs=smooth_path(points,radii,steps)
 return tube(name,pts,rs,material,sides,group)

def surface_patch(name,center,radius,material,depth=.0,radial=12,segments=56,group=None,bulge=None):
 # A fitted face patch; the edge follows the actual skull instead of a floating disk.
 v=[];f=[];cx,cy=center;rx,ry=radius
 for j in range(radial+1):
  r=j/radial
  for k in range(segments):
   a=math.tau*k/segments;x=cx+rx*r*math.cos(a);y=cy+ry*r*math.sin(a)
   z=face_z(x,y)+depth+(bulge(x,y,r) if bulge else 0)
   v.append((x,y,z))
 for j in range(radial):
  for k in range(segments):
   a=j*segments+k;b=j*segments+(k+1)%segments;f.append((a,b,b+segments,a+segments))
 # x/y parametrization is front-facing (positive Z).
 return mesh(name,v,[tuple(reversed(q)) for q in f],material,group=group)

GROUP='driver'
# Authored head surface, not intersecting cheek/jaw spheres.
v=[];f=[];rings=72;segments=72
for j in range(rings+1):
 y=HEAD_SECTIONS[0][0]+(HEAD_SECTIONS[-1][0]-HEAD_SECTIONS[0][0])*j/rings
 w,front,back=head_profile(y)
 for k in range(segments):
  a=k*math.tau/segments
  # Soft, shallow cheek flares belong to the same continuous surface.
  flare=.007*math.exp(-((y-1.145)/.055)**2)*abs(math.cos(a))**8
  v.append(((w+flare)*math.cos(a),y,(front+back)*.5+(front-back)*.5*math.sin(a)))
for j in range(rings):
 for k in range(segments):
  a=j*segments+k;b=j*segments+(k+1)%segments;f.append((a,a+segments,b+segments,b))
head=mesh('Cat — continuous sculpted skull and jaw',v,f,orange)

# Continuous seated pear torso, shoulders, elbows, wrists, hips and paws.
# Skin is fused below with a cat-only voxel remesh and curvature smoothing.
skin=[head]
skin.append(ell('Cat — seated pear torso',(0,.752,-.214),(.218,.265,.183),orange,40,28))
skin.append(ell('Cat — soft neck bridge',(0,.969,-.160),(.148,.136,.142),orange,36,24))
skin.append(ell('Cat — seated pelvis',(0,.568,-.171),(.213,.121,.169),orange,36,24))
for side in [-1,1]:
 skin.append(ell('Cat — connected folded thigh',(side*.118,.553,-.103),(.105,.103,.175),orange,32,22))
 skin.append(curved_tube('Cat — continuous shoulder to wrist',
  [(side*.146,.921,-.204),(side*.209,.879,-.165),
   (side*.242,.810,-.060),(side*.225,.807,.092),(side*.180,.839,.231)],
  [.084,.081,.075,.061,.048],orange,24,10))
 skin.append(ell('Cat — rounded gripping palm',(side*.180,.847,.232),(.066,.052,.055),orange,36,24))
 skin.append(curved_tube('Cat — tucked gripping thumb',
  [(side*.146,.850,.210),(side*.137,.827,.228),(side*.151,.812,.245)],
  [.031,.028,.019],orange,20,7))
 # Feet remain under the bonnet and fit the existing seat and floor.
 ell('Cat — fitted racing shoe',(side*.128,.458,.025),(.088,.064,.141),navy,32,20)

# Remove internal intersections and hard shoulder/jaw seams. This operation is
# deliberately scoped to orange cat skin; the car is never remeshed/subdivided.
bpy.ops.object.select_all(action='DESELECT')
for o in skin:o.select_set(True)
bpy.context.view_layer.objects.active=head;bpy.ops.object.join()
head.name='Cat — unified organic skin';head.data.remesh_voxel_size=.009
bpy.ops.object.voxel_remesh()
head['pivot']='driver'
for p in head.data.polygons:p.use_smooth=True
sm=head.modifiers.new('Cat-only curvature relaxation','SMOOTH');sm.factor=1.05;sm.iterations=5
bpy.ops.object.modifier_apply(modifier=sm.name)
# Keep surface normals reliable after the union.
head.data.update()
retopo=head.modifiers.new('Cat-only controlled surface density','DECIMATE');retopo.ratio=.28
bpy.ops.object.modifier_apply(modifier=retopo.name)
for p in head.data.polygons:p.use_smooth=True

# A cream bib follows the torso rather than protruding as a separate belly ball.
v=[];f=[];seg=48;radial=12
for j in range(radial+1):
 r=j/radial
 for k in range(seg):
  a=k*math.tau/seg;x=.133*r*math.cos(a);y=.792+.171*r*math.sin(a)
  z=-.214+.183*math.sqrt(max(.01,1-(x/.218)**2-((y-.752)/.265)**2))+.0035
  v.append((x,y,z))
for j in range(radial):
 for k in range(seg):
  a=j*seg+k;b=j*seg+(k+1)%seg;f.append((a,b,b+seg,a+seg))
mesh('Cat — fitted cream chest marking',v,[tuple(reversed(q)) for q in f],cream)

# Subtle curved paw creases define three toes without sausage-like fingers.
for side in [-1,1]:
 for dx in [-.018,.010]:
  curved_tube('Cat — soft paw crease',
   [(side*.180+dx,.885,.255),(side*.180+dx,.877,.272),(side*.180+dx,.866,.281)],
   [.0006,.0014,.0006],stripe,8,5)

# Recessed, symmetric eye surfaces are projected onto the skull. Orbital skin
# stays part of the head; only eye surfaces use the existing blink pivot.
for side in [-1,1]:
 cx=side*.132;cy=1.302;rx=.106;ry=.128
 def sclera_height(x,y,r):return .028*max(0,1-r*r)**.70
 surface_patch('Cat — fitted sclera',(cx,cy),(rx,ry),cream,.0028,12,56,'eyes',sclera_height)
 def eye_layer(x,y,r):
  rr=((x-cx)/rx)**2+((y-cy)/ry)**2
  return .028*max(0,1-rr)**.70
 # Slightly smaller irises and consistent inset depth avoid the old goggle rim.
 surface_patch('Cat — polished amber iris',(cx,cy+.001),(.068,.096),iris,.005,10,48,'eyes',eye_layer)
 surface_patch('Cat — clean oval pupil',(cx,cy+.003),(.038,.073),dark,.007,10,44,'eyes',eye_layer)
 for dx,dy,sx,sy in [(-.018,.040,.016,.024),(.018,-.027,.0065,.010)]:
  x=cx+dx;y=cy+dy;z=face_z(x,y)+.011+eye_layer(x,y,0)
  ell('Cat — soft corneal glint',(x,y,z),(sx,sy,.004),glint,16,10,group='eyes')
 # Rounded eyelids follow the orbital edge, with soft tapered inner corners.
 for upper in [True,False]:
  pts=[];rs=[]
  for i in range(25):
   a=(math.pi*i/24) if upper else (math.pi+math.pi*i/24)
   x=cx+rx*math.cos(a);y=cy+ry*math.sin(a)
   pts.append((x,y,face_z(x,y)+.004));rs.append(.003+.006*math.sin(math.pi*i/24)**.7)
  tube('Cat — blended upper eyelid' if upper else 'Cat — blended lower eyelid',pts,rs,orange,12)
 # Clean tapered brows, less heavy and angular than the original bars.
 points=[]
 for x,y in [(side*.053,1.443),(side*.127,1.463),(side*.214,1.430)]:points.append((x,y,face_z(x,y)+.005))
 curved_tube('Cat — tapered expressive brow',points,[.004,.010,.002],stripe,12,10)

# One bilobed cream muzzle with a continuous bridge replaces two intersecting
# cheek balls. The perimeter blends flush into the authored cheek surface.
def muzzle_bulge(x,y,r):
 lobes=math.exp(-((x-.073)/.082)**2)+math.exp(-((x+.073)/.082)**2)
 return (.012+.042*lobes)*max(0,1-r*r)**.8
surface_patch('Cat — continuous bilobed muzzle',(0,1.145),(.191,.079),cream,.0025,18,72,bulge=muzzle_bulge)
# A small chin marking extends the same surface flow below the smile.
surface_patch('Cat — soft cream chin',(0,1.015),(.092,.028),cream,.002,8,40)
surface_patch('Cat — inset smiling mouth',(0,1.070),(.084,.058),dark,.005,12,56)
surface_patch('Cat — tongue inside smile',(0,1.042),(.036,.015),pink,.0075,8,36)

# Rounded heart/triangle nose, with a gently narrowing lower half and satin tip.
o=ell('Cat — softly sculpted nose',(0,1.178,.271),(.036,.025,.018),pink,40,24)
for vtx in o.data.vertices:
 ny=(vtx.co.y-1.178)/.025
 vtx.co.x*=.82+.24*(ny+1)/2
# Philtrum is seated on the muzzle; no detached rod between nose and mouth.
curved_tube('Cat — fine philtrum',[(0,1.157,.270),(0,1.139,.264),(0,1.123,.258)],
 [.0028,.0024,.0012],stripe,10,8)
for side in [-1,1]:
 for j in range(3):
  x=side*(.096+j*.021);y=1.144-j*.012;r=math.sqrt((x/.191)**2+((y-1.145)/.079)**2)
  z=face_z(x,y)+.004+muzzle_bulge(x,y,r)
  ell('Cat — tiny whisker follicle',(x,y,z),(.0038,.0035,.002),stripe,16,10)

# Closed rounded ears: a real volume with a softly inset inner ear, replacing
# the thin triangular sheets and angular tube outlines of the prior model.
def rounded_outline(vertices,rounding=.20,steps=10):
 points=[]
 for i,c in enumerate(vertices):
  prev=Vector(vertices[(i-1)%len(vertices)]);c=Vector(c);nxt=Vector(vertices[(i+1)%len(vertices)])
  a=c+(prev-c)*rounding;b=c+(nxt-c)*rounding
  for j in range(steps):
   t=j/steps;points.append(tuple((1-t)**2*a+2*t*(1-t)*c+t*t*b))
 return points
for side,key in [(-1,'ear_l'),(1,'ear_r')]:
 GROUP=key
 outline=rounded_outline([(side*.119,1.421,-.085),(side*.331,1.698,-.111),(side*.348,1.407,-.130)],.19,12)
 area=sum(outline[i][0]*outline[(i+1)%len(outline)][1]-outline[(i+1)%len(outline)][0]*outline[i][1] for i in range(len(outline)))
 if area<0:outline.reverse()
 n=len(outline);center=sum((Vector(p) for p in outline),Vector())/n;v=[];f=[];nr=10
 for back in [False,True]:
  for j in range(nr+1):
   r=j/nr
   for p in outline:
    q=center+(Vector(p)-center)*r
    q.z+=(-.013-.030*(1-r*r)) if back else (.013+.045*(1-r*r))
    v.append(tuple(q))
 count=(nr+1)*n
 for offset in [0,count]:
  for j in range(nr):
   for k in range(n):
    a=offset+j*n+k;b=offset+j*n+(k+1)%n
    face=(a,b,b+n,a+n);f.append(tuple(reversed(face)) if offset==0 else face)
 for k in range(n):
  a=nr*n+k;b=nr*n+(k+1)%n;f.append((a,a+count,b+count,b))
 mesh('Cat — rounded volumetric ear',v,f,orange)
 v=[];f=[]
 for j in range(11):
  r=j/10
  for p in outline:
   q=center+(Vector(p)-center)*r*.71
   q.y+=.008;q.z+=.015+.045*(1-(r*.71)**2)
   v.append(tuple(q))
 for j in range(10):
  for k in range(n):
   a=j*n+k;b=j*n+(k+1)%n;f.append((a,b,b+n,a+n))
 mesh('Cat — inset rose ear bowl',v,[tuple(reversed(q)) for q in f],pink)

# The tail keeps its existing mesh and pivot. All animation remains untouched.
GROUP='driver'
def refined_markings():
 # Surface-following painted strokes; no geometry spikes along the cheek.
 global GROUP
 GROUP='driver'
 for ph in [.55,1.15,1.99,2.59,3.5,4.0,4.7,5.4,5.9]:
  v=[];f=[];steps=24
  for i in range(steps+1):
   t=i/steps;y=1.554-(.158 if math.sin(ph)>0 else .245)*t
   w,front,back=head_profile(y);width=.070*math.sin(math.pi*t)**.7
   for sign in [-1,1]:
    a=ph+sign*width;v.append(((w+.0018)*math.cos(a),y,(front+back)*.5+((front-back)*.5+.0018)*math.sin(a)))
  for i in range(steps):f.append((2*i,2*i+1,2*i+3,2*i+2))
  mesh('Cat — fine tapered crown marking',v,f,stripe)
 # Small side cheek markings stay embedded and do not change the silhouette.
 for side in [-1,1]:
  for y0 in [1.155,1.208]:
   pts=[]
   for i in range(16):
    t=i/15;x=side*(.266-.052*t);y=y0+.009*math.sin(math.pi*t)
    pts.append((x,y,face_z(x,y)+.001))
   tube('Cat — painted cheek accent',pts,[.0008+.0032*math.sin(math.pi*i/15) for i in range(16)],stripe,8)

def refined_back_markings():
 # Project color strokes onto the final fused skin instead of the old ellipsoid.
 from mathutils.bvhtree import BVHTree
 bpy.context.view_layer.update()
 tree=BVHTree.FromObject(head,bpy.context.evaluated_depsgraph_get())
 for y0 in [.69,.79,.89]:
  v=[];f=[]
  for j in range(25):
   t=j/24;x=-.175+.35*t
   for sign in [-1,1]:
    y=y0+.010*math.sin(math.pi*t)+sign*.006*math.sin(math.pi*t)
    hit,normal,index,distance=tree.ray_cast(Vector((x,y,-1)),Vector((0,0,1)))
    assert hit is not None,'Back marking must remain on the skin'
    v.append((x,y,hit.z-.0013))
  for j in range(24):f.append((2*j,2*j+1,2*j+3,2*j+2))
  mesh('Cat — skin-fitted back stripe',v,f,stripe,group='driver')

def clean_cat_surfaces():
 # Weld collapsed patch centres and UV-sphere poles before computing normals.
 # Scope by authored cat object names; wheel/car meshes are intentionally exempt.
 import bmesh
 for o in list(bpy.context.scene.objects):
  if o.type=='MESH' and o.name.startswith('Cat —'):
   bm=bmesh.new();bm.from_mesh(o.data)
   bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.0000005)
   bm.to_mesh(o.data);bm.free();o.data.update()
   for p in o.data.polygons:p.use_smooth=True
