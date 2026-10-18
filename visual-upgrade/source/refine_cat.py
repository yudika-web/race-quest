"""Cat-only blocky/chibi rebuild, executed by build_cat.py.
No organic remesh/subdivision. Rounded rectangular solids, graphic face and
low-cost tabby patches; same seat, steering contact points and rigid pivots.
All positions are game X/Y/Z metres (Y up, Z forward).
"""
import bmesh
pupil=mat('16_Deep_teal_pupil','17212B',.74)
GROUP='driver'

def finish_block(o,bevel):
 o['cat_blocky']=True
 for p in o.data.polygons:p.use_smooth=True
 if bevel:
  m=o.modifiers.new('Small toy edge radius, no subdivision','BEVEL');m.width=bevel;m.segments=3
  m=o.modifiers.new('Planar faces and soft bevel normals','WEIGHTED_NORMAL');m.keep_sharp=True;m.weight=50
 return o

def catbox(name,c,size,material,bevel=.018,group='driver'):
 o=box('Cat — '+name,c,size,material,0,group)
 return finish_block(o,bevel)

def solid(name,verts,faces,material,bevel=.008,group='driver'):
 o=mesh('Cat — '+name,verts,faces,material,False,group)
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
 return finish_block(o,bevel)

def beam(name,a,b,width,depth,material,bevel=.018):
 a,b=Vector(a),Vector(b);o=catbox(name,(a+b)/2,(width,(b-a).length,depth),material,bevel)
 o.rotation_euler=(b-a).to_track_quat('Y','Z').to_euler()
 return o

# Main silhouette: a genuine rounded cube with broad planar front/side/top.
head=catbox('cube head',(0,1.275,-.07),(.74,.56,.53),orange,.060)
catbox('short block neck',(0,.972,-.20),(.20,.10,.20),orange,.025)
catbox('seated chibi torso',(0,.745,-.23),(.34,.42,.34),orange,.042)
catbox('cream chest bib',(0,.762,-.052),(.225,.278,.022),cream,.026)
for side in [-1,1]:
 catbox('short seated thigh',(side*.105,.595,-.035),(.148,.14,.25),orange,.027)
 catbox('cream square foot',(side*.110,.565,.105),(.15,.105,.15),cream,.022)
 beam('short upper arm',(side*.155,.875,-.17),(side*.231,.790,.015),.132,.132,orange,.026)
 beam('short forearm',(side*.231,.790,.015),(side*.181,.840,.214),.116,.116,orange,.024)
 catbox('square steering paw',(side*.181,.840,.234),(.125,.128,.115),cream,.026)
 catbox('small grip thumb',(side*.143,.811,.211),(.055,.062,.065),cream,.015)

# The cream mask is painted into the head's own mesh in clean_cat_surfaces().
# No overlay shell or separate cheek/muzzle solids.
# Graphic eyes; black rounded rectangles and square highlights are rigidly blinkable.
for side in [-1,1]:
 catbox('rectangular eye',(side*.157,1.309,.205),(.090,.139,.020),pupil,.012,'eyes')
 catbox('square eye highlight',(side*.157-.014,1.342,.218),(.030,.038,.005),glint,.004,'eyes')
catbox('small pink nose',(0,1.174,.226),(.064,.045,.026),pink,.010)
# Tiny happy open smile. An extruded flat cartoon shape, deliberately not a muzzle sculpt.
outline=[(-.050,1.132),(-.027,1.121),(0,1.128),(.027,1.121),(.050,1.132),(.046,1.102),(.030,1.078),(0,1.068),(-.030,1.078),(-.046,1.102)]
v=[(x,y,z) for z in [.198,.205] for x,y in outline];n=len(outline)
f=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
solid('happy graphic mouth',v,f,pupil,.003)
catbox('smile tongue',(0,1.087,.207),(.051,.024,.005),pink,.009)
catbox('nose philtrum',(0,1.141,.207),(.009,.019,.006),pupil,.002)
# Simple triangular ears with real depth, softly bevelled perimeter, flat pink inset.
for side,label in [(-1,'l'),(1,'r')]:
 cx=side*.245
 # Slightly outward tip; broad bases are embedded in the cube crown.
 coords=[(cx-.105,1.507),(cx+.105,1.507),(cx+side*.038,1.758)]
 v=[(x,y,z) for z in [-.230,-.058] for x,y in coords]
 solid('triangular ear '+label,v,[(0,2,1),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],orange,.020,'ear_'+label)
 coords=[(cx-.062,1.552),(cx+.062,1.552),(cx+side*.028,1.699)]
 v=[(x,y,z) for z in [-.064,-.052] for x,y in coords]
 solid('pink ear inset '+label,v,[(0,2,1),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],pink,.009,'ear_'+label)

def redesigned_tail():
 # A single continuous square-section curl with chamfered corners. Eight points
 # per ring keep its silhouette blocky; bands sit on the same section, not tubes.
 pts=[(-.06,.724,-.38),(-.20,.735,-.49),(-.35,.790,-.52),(-.435,.940,-.52),(-.435,1.110,-.52),(-.465,1.165,-.51)]
 profile=[(-.039,-.052),(.039,-.052),(.052,-.039),(.052,.039),(.039,.052),(-.039,.052),(-.052,.039),(-.052,-.039)]
 def section(points,material,name,inflate=0):
  verts=[]
  for i,p in enumerate(points):
   t=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)]);t.z=0;t.normalize();a=Vector((-t.y,t.x,0));b=Vector((0,0,1))
   for u,w in profile:verts.append(tuple(Vector(p)+a*u*(1+inflate)+b*w*(1+inflate)))
  faces=[tuple(reversed(range(8))),tuple((len(points)-1)*8+j for j in range(8))]
  for i in range(len(points)-1):
   for j in range(8):k=i*8+j;q=i*8+(j+1)%8;faces.append((k,q,q+8,k+8))
  return solid(name,verts,faces,material,0,'tail')
 section(pts,orange,'square curled tail')
 # Surface bands use complete short ring segments for graphic all-view readability.
 for i,t0,t1 in [(0,.40,.78),(2,.12,.55),(3,.45,.78)]:
  a,b=Vector(pts[i]),Vector(pts[i+1]);section([a.lerp(b,t0),a.lerp(b,t1)],stripe,'tail tabby band',.015)
 catbox('cream tail tip',(-.455,1.151,-.515),(.132,.125,.136),cream,.013,'tail')

def refined_markings():
 # Forehead bars wrap around the actual rounded top/front corner of the cube.
 # Flat patches have no backing volume: no floating cylinders or chunky tufts.
 for x in [-.077,.045]:
  path=[(-.170,1.557),(.135,1.557)] # (z,y): top plane then quarter-circle
  for i in range(1,7):
   a=(math.pi/2)*i/6;path.append((.135+.061*math.sin(a),1.495+.061*math.cos(a)))
  path.append((.197,1.456))
  verts=[(xx,y,z) for z,y in path for xx in [x-.022,x+.022]]
  o=mesh('Cat — graphic crown stripe',verts,[(i,i+1,i+3,i+2) for i in range(0,len(verts)-2,2)],stripe,False,'driver');o['cat_blocky']=True
 for side in [-1,1]:
  # front cheek bars + side bars, with no extra facial bulk
  for y in [1.225,1.131]:
   verts=[(side*x,yy,.1970) for yy in [y-.017,y+.017] for x in [.258,.310]]
   faces=[(0,1,3,2)]
   if side<0:faces=[tuple(reversed(f)) for f in faces]
   o=mesh('Cat — flat graphic cheek stripe',verts,faces,stripe,False,'driver');o['cat_blocky']=True
  for y in [1.160,1.294,1.428]:
   catbox('graphic side stripe',(side*.372,y,-.075),(.008,.043,.230),stripe,.007)

def refined_back_markings():
 for y in [1.16,1.292,1.424]:catbox('graphic back head stripe',(0,y,-.338),(.435,.044,.008),stripe,.007)
 for y in [.703,.817]:catbox('graphic back torso stripe',(0,y,-.402),(.235,.033,.006),stripe,.005)

def color_hex(s):
 rgb=[int(s[i:i+2],16)/255 for i in [0,2,4]]
 return [v/12.92 if v<.04045 else ((v+.055)/1.055)**2.4 for v in rgb]

def clean_cat_surfaces():
 # Bake only the cube head bevel, then divide its surface at the mask edges.
 # Corner colours create a crisp painted boundary on ONE continuous solid;
 # there is no z fighting, raised face plate or extra material draw call.
 bpy.context.view_layer.objects.active=head;head.select_set(True)
 for m in list(head.modifiers):
  if m.type=='BEVEL':bpy.ops.object.modifier_apply(modifier=m.name)
 bm=bmesh.new();bm.from_mesh(head.data)
 for point,normal in [((0,1.20,0),(0,1,0)),((0,0,.080),(0,0,1))]:
  bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=.0000001,plane_co=head.matrix_world.inverted()@Vector(point),plane_no=normal,clear_inner=False,clear_outer=False)
 bm.to_mesh(head.data);bm.free();head.data.update()
 palette={10:'FFA957',11:'FFE7BE',12:'BF611F',13:'F18DA9',14:'AD6C23',15:'FFF9E9',16:'17212B'}
 for o in bpy.context.scene.objects:
  if o.type!='MESH' or not o.get('cat_blocky'):continue
  material=o.data.materials[0];kind=int(material.name[:2]);base=color_hex(palette[kind])
  attr=o.data.color_attributes.new(name='CatGradient',type='FLOAT_COLOR',domain='CORNER' if o==head else 'POINT')
  for i,v in enumerate(o.data.vertices) if o!=head else []:
   # Very subtle warm variation; graphic tabby boundaries stay crisp.
   pos=o.matrix_world@v.co;shade=1 if kind!=10 else .975+.025*max(0,min(1,(pos.y-.55)/1.2))
   attr.data[i].color=(*(x*shade for x in base),1)
  if o==head:
   for poly in o.data.polygons:
    center=sum((o.data.vertices[i].co for i in poly.vertices),Vector())/len(poly.vertices)
    center=o.matrix_world@center
    color=color_hex(palette[11]) if center.y<1.200001 and center.z>.079999 else base
    for li in poly.loop_indices:attr.data[li].color=(*color,1)
  nodes=material.node_tree.nodes;shader=nodes.get('Principled BSDF');vc=nodes.get('CatGradient') or nodes.new('ShaderNodeVertexColor');vc.name='CatGradient';vc.layer_name='CatGradient';material.node_tree.links.new(vc.outputs['Color'],shader.inputs['Base Color'])
