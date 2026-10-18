"""RACE QUEST hero cat/sport. Run: blender -b --python build_cat.py
Coordinates intentionally use game axes: X right, Y up, Z forward; metres.
Exports renderer-compatible glTF 2 GLB plus editable .blend, high and low LOD.
"""
import bpy, math, json, struct, pathlib, hashlib
from mathutils import Vector
from collections import defaultdict
OUT=pathlib.Path(__file__).resolve().parents[1]
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
MATS={}
def mat(name,hex,rough=.5,metal=0,emit=None):
 c=[int(hex[i:i+2],16)/255 for i in (0,2,4)];c=[v/12.92 if v<.04045 else ((v+.055)/1.055)**2.4 for v in c]
 m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 MATS[name]={'name':name,'pbrMetallicRoughness':{'baseColorFactor':[*c,1],'roughnessFactor':rough,'metallicFactor':metal},'doubleSided':False,'emissiveFactor':emit or [0,0,0]};return m
blue=mat('01_Ceramic_cyan_paint','079ED2',.28,.32);navy=mat('02_Deep_petrol_trim','122B3A',.52,.08);white=mat('03_Pearl_stripe','E6F3E9',.38,.18);rubber=mat('04_Satin_rubber','242A32',.92);metal=mat('05_Machined_titanium','9FAFB8',.3,.72);dark=mat('06_Grille_pupil','08141E',.6);glass=mat('07_Smoked_blue_glass','285D70',.2,.35);lamp=mat('08_Ice_LED','B6EEFF',.22,.1,[.26,.57,.7]);red=mat('09_Coral_tail_LED','F04B41',.3,.1,[.4,.018,.008]);orange=mat('10_Golden_tabby_fur','EA8B30',.84);cream=mat('11_Cream_muzzle','F6DDB0',.86);stripe=mat('12_Burnished_tabby_mark','AC4B1B',.88);pink=mat('13_Rose_ear_nose','E5948B',.78);iris=mat('14_Amber_iris','AD6C23',.38);glint=mat('15_Eye_glint','FFF6DC',.18,0,[.12,.12,.10])
pivots={'root':(None,(0,0,0)),'body_suspension':('root',(0,.35,0)),'driver':('body_suspension',(0,.32,-.17)),'tail':('driver',(0,.04,-.20)),'ear_l':('driver',(-.225,.73,-.02)),'ear_r':('driver',(.225,.73,-.02)),'eyes':('driver',(0,.63,.245))}
for side,x in [('l',-.59),('r',.59)]:
 for end,z in [('f',.48),('r',-.56)]:
  name='wheel_'+end+side;pivots[name]=('root',(x,.205,z));pivots[name+'_spin']=(name,(0,0,0))
GROUP='body_suspension';detail=True

def mesh(name,verts,faces,material,smooth=True,group=None):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.materials.append(material);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o['pivot']=group or GROUP
 for p in me.polygons:p.use_smooth=smooth
 return o

def ell(name,c,s,ma,seg=28,rings=16,group=None):
 seg=seg if detail else max(12,seg//2);rings=rings if detail else max(8,rings//2)
 v=[];f=[]
 for j in range(rings+1):
  t=math.pi*j/rings
  for i in range(seg):
   a=2*math.pi*i/seg;v.append((c[0]+s[0]*math.sin(t)*math.cos(a),c[1]+s[1]*math.cos(t),c[2]+s[2]*math.sin(t)*math.sin(a)))
 for j in range(rings):
  for i in range(seg):a=j*seg+i;b=j*seg+(i+1)%seg;f.append((a,b,b+seg,a+seg))
 return mesh(name,v,f,ma,group=group)

def tube(name,points,radii,ma,sides=10,group=None):
 sides=sides if detail else max(6,sides//2);v=[];f=[]
 for i,p in enumerate(points):
  t=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)]);t.normalize();n=t.cross(Vector((0,1,0)))
  if n.length<.01:n=t.cross(Vector((1,0,0)))
  n.normalize();b=t.cross(n).normalized();r=radii[i] if isinstance(radii,list) else radii
  for k in range(sides):v.append(tuple(Vector(p)+r*(math.cos(k*math.tau/sides)*n+math.sin(k*math.tau/sides)*b)))
 for j in range(len(points)-1):
  for k in range(sides):a=j*sides+k;b=j*sides+(k+1)%sides;f.append((a,b,b+sides,a+sides))
 f.extend([tuple(reversed(range(sides))),tuple((len(points)-1)*sides+k for k in range(sides))]);return mesh(name,v,f,ma,group=group)

def box(name,c,s,ma,bevel=.025,group=None):
 bpy.ops.mesh.primitive_cube_add(size=1,location=c);o=bpy.context.object;o.name=name;o.dimensions=s;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(ma);o['pivot']=group or GROUP
 if bevel:
  mod=o.modifiers.new('Hand-finished edge radii','BEVEL');mod.width=bevel;mod.segments=3 if detail else 2
  mod=o.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL')
 return o

def panel(name,rows,ma):
 # rows: z, center height, half width, edge drop. Transverse sculpted surface.
 v=[];f=[];steps=12 if detail else 8
 for z,y,w,d in rows:
  for i in range(steps+1):
   u=-1+2*i/steps;v.append((w*u,y-d*abs(u)**2.6,z))
 for j in range(len(rows)-1):
  for i in range(steps):a=j*(steps+1)+i;f.append((a,a+1,a+steps+2,a+steps+1))
 # backside faces automatically oriented above via winding +z rows? x increasing, z increasing => -y, reverse
 return mesh(name,v,[tuple(reversed(q)) for q in f],ma)

# Chassis is an authored loft, split around open cockpit; sculpted fenders follow original wheel centres.
box('Carbon flat floor',(0,.235,-.01),(1.06,.12,1.57),navy,.045)
panel('Long flowing bonnet',[(.13,.54,.34,.055),(.28,.53,.43,.06),(.46,.48,.49,.065),(.65,.40,.50,.065),(.83,.32,.47,.045),(.90,.27,.40,.025)],blue)
# reverse rows above to normals correction handled final normals check
for side in [-1,1]:
 for zc in [.48,-.56]:
  v=[];f=[];n=22 if detail else 14
  for j in range(n+1):
   a=math.pi*.06+math.pi*.88*j/n
   for k in range(5):
    x=side*(.36+.33*k/4);rad=.257+(.018*math.sin(k*math.pi/4));v.append((x,.205+rad*math.sin(a),zc+rad*math.cos(a)))
  for j in range(n):
   for k in range(4):i=j*5+k;f.append((i,i+1,i+6,i+5) if side>0 else (i+5,i+6,i+1,i))
  o=mesh('Sculpted wheel arch',v,f,blue);o.data.materials[0]=blue
 # side sills tapered, connected shoulder and sculpted intake
 tube('Sill shoulder',[(side*.45,.28,.72),(side*.51,.29,.3),(side*.52,.31,-.15),(side*.49,.34,-.72)], [.075,.065,.085,.07],blue,12)
 box('Inset side air intake',(side*.516,.36,-.06),(.035,.14,.36),dark,.025)
 for k in range(3):box('Intake gill',(side*.539,.32+k*.035,-.08),(.018,.012,.25),metal,.004)
 tube('Cockpit leather rim',[(side*.34,.53,.19),(side*.37,.57,-.06),(side*.35,.60,-.4),(side*.26,.55,-.68)],.036,navy,12)
 box('Side mirror stalk',(side*.48,.55,.23),(.15,.025,.035),navy,.01)
 ell('Aerodynamic mirror',(side*.56,.57,.23),(.075,.038,.07),blue,20,10)
 box('Mirror glass',(side*.56,.575,.175),(.085,.04,.008),glass,.008)
 # front angled light bezel, luminous nested slash
 tube('Headlamp dark recess',[(side*.40,.37,.78),(side*.35,.405,.67),(side*.30,.445,.59)],.053,dark,12)
 tube('Blade LED',[(side*.40,.420,.81),(side*.355,.455,.70),(side*.31,.495,.625)],.020,lamp,10)
 box('Rear LED',(side*.38,.416,-.82),(.23,.042,.026),red,.012)
 tube('Exhaust titanium',[(side*.31,.27,-.72),(side*.31,.265,-.92)],.055,metal,16)
 tube('Exhaust black bore',[(side*.31,.265,-.925),(side*.31,.265,-.935)],.040,dark,16)
 # spoiler pedestal
 box('Spoiler support',(side*.32,.58,-.73),(.035,.27,.055),navy,.012)
 box('Spoiler end plate',(side*.56,.737,-.76),(.035,.115,.23),blue,.015)
# rear deck, front fascia and spoiler
panel('Engine deck',[(-.85,.39,.44,.04),(-.73,.46,.46,.06),(-.57,.50,.33,.03)],blue)
box('Floating front splitter',(0,.15,.84),(1.06,.045,.20),navy,.02)
box('Deep front radiator',(0,.25,.875),(.61,.13,.035),dark,.025)
for j in range(9):box('Radiator vertical fin',((j-4)*.064,.25,.898),(.008,.10,.008),metal,.002)
for side in [-1,1]:box('Front corner bumper',(side*.46,.23,.83),(.15,.13,.10),blue,.03)
box('Rear diffuser',(0,.19,-.80),(.92,.08,.18),navy,.015)
for x in [-.35,-.17,0,.17,.35]:box('Diffuser vane',(x,.16,-.83),(.02,.09,.17),dark,.005)
box('Airfoil spoiler',(0,.71,-.77),(1.12,.045,.22),blue,.02)
box('Spoiler white inlay',(0,.736,-.77),(.40,.004,.19),white,.002)
# white racing ribbons follow hood surface, thin mesh strips
for side in [-1,1]:
 rows=[(.17,.544),(.28,.534),(.46,.484),(.65,.404),(.83,.324),(.89,.28)]
 vs=[]
 for z,y in rows:
  for x in [side*.074,side*.123]:vs.append((x,y-.002,z))
 mesh('Bonnet ivory racing stripe',vs,[(i,i+2,i+3,i+1) for i in range(0,len(vs)-2,2)],white)
# cockpit wind deflector curved transparent-looking opaque blue glass, no sorting artifacts
panel('Low curved windscreen',[(.14,.54,.32,.018),(.13,.66,.295,.042),(.09,.70,.25,.055)],glass)
box('Seat cushion',(0,.47,-.27),(.43,.115,.43),navy,.065)
box('Seat back',(0,.66,-.48),(.43,.40,.095),navy,.075)
for side in [-1,1]:tube('Seat cyan piping',[(side*.19,.49,-.1),(side*.20,.56,-.42),(side*.18,.79,-.48)],.012,blue,8)
# steering rim faces driver, tilted toward seat. Hands meet left/right rim exactly.
tube('Steering column',[(0,.51,.18),(0,.78,.25)],.022,metal,10)
center=(0,.83,.235);r=.18
rim=[]
for i in range(41):
 a=math.tau*i/40;rim.append((r*math.cos(a),center[1]+r*.88*math.sin(a),center[2]+r*.48*math.sin(a)))
tube('Stitched steering rim',rim,.022,navy,10)
for a in [0,math.pi,math.pi*1.5]:tube('Steering spokes',[center,(r*.85*math.cos(a),center[1]+r*.75*math.sin(a),center[2]+r*.40*math.sin(a))],.014,metal,8)
ell('Steering hub',center,(.045,.04,.025),blue,20,10)
# wheels oriented around X, original radius/axles retained
for side,x in [('l',-.59),('r',.59)]:
 for end,z in [('f',.48),('r',-.56)]:
  GROUP='wheel_'+end+side+'_spin';sg=-1 if x<0 else 1
  # Lathed tire with soft shoulders, carcass and visible circumferential channels
  profile=[(-.105,.139),(-.103,.177),(-.078,.199),(-.046,.205),(-.038,.199),(-.029,.205),(.029,.205),(.038,.199),(.046,.205),(.078,.199),(.103,.177),(.105,.139)]
  v=[];f=[];n=48 if detail else 28
  for xx,rr in profile:
   for k in range(n):a=k*math.tau/n;v.append((x+xx,.205+rr*math.cos(a),z+rr*math.sin(a)))
  for j in range(len(profile)-1):
   for k in range(n):a=j*n+k;b=j*n+(k+1)%n;f.append((a,b,b+n,a+n))
  mesh('Shouldered performance tire',v,f,rubber)
  # V-shaped raised tread dashes stay below maximum .205 contact radius
  if detail:
   for k in range(24):
    a=k*math.tau/24
    for sx in [-1,1]:
     pts=[]
     for t in [0,.5,1]:
      ang=a+.07*t;rr=.2054;pts.append((x+sx*(.052+.025*t),.205+rr*math.cos(ang),z+rr*math.sin(ang)))
     tube('Directional tread',pts,.0035,navy,5)
  face=x+sg*.108
  ell('Alloy outer lip',(face,.205,z),(.010,.153,.153),metal,24,12)
  ell('Brake recess',(face+sg*.008,.205,z),(.012,.125,.125),dark,24,12)
  ell('Ventilated brake rotor',(face+sg*.018,.205,z),(.008,.095,.095),metal,24,12)
  for k in range(5):
   a=math.tau*k/5;pts=[(face+sg*.033,.205+.025*math.cos(a),z+.025*math.sin(a)),(face+sg*.037,.205+.085*math.cos(a+.12),z+.085*math.sin(a+.12)),(face+sg*.029,.205+.139*math.cos(a+.18),z+.139*math.sin(a+.18))];tube('Swept forged spoke',pts,[.016,.013,.011],metal,8)
  ell('Cyan axle cap',(face+sg*.047,.205,z),(.014,.037,.037),blue,16,10)
# Cat-only organic refinement; the sport car above is intentionally unchanged.
exec(compile((OUT/'source/refine_cat.py').read_text(), str(OUT/'source/refine_cat.py'), 'exec'))
# curled tail rises from seat behind body and curls to side, clearly readable from chase camera
GROUP='tail'
pts=[]
for i in range(24):
 t=i/23;pts.append((-.04+.36*math.sin(t*math.pi*1.25),.69+.37*t+.10*math.sin(t*math.pi*2),-.43-.18*math.sin(t*math.pi)))
tube('Single flowing curled tail',pts,[.058*(1-.40*i/23) for i in range(24)],orange,14)
for j in [6,11,16,21]:tube('Tail tabby rings',pts[j:j+2],[.058*(1-.40*j/23)+.001,.058*(1-.40*(j+1)/23)+.001],stripe,14)
# Follow the revised sculpted skull for the fur markings.
refined_markings()
# Cat-only markings conform to the final fused torso.
refined_back_markings()
clean_cat_surfaces()
# Paw emblem on bonnet: cream pad and four toes, integrated shallow relief
GROUP='body_suspension'
ell('Paw badge pad',(0,.455,.55),(.032,.004,.026),white,20,10)
for x,z in [(-.042,.58),(-.016,.600),(.016,.600),(.042,.58)]:ell('Paw badge toe',(x,.441 if z>.59 else .447,z),(.012,.004,.014),white,14,8)

# Correct winding and bake Blender modifiers, group into material batches per rigid pivot.
# Custom glTF writer avoids armature/runtime dependency and preserves fixed rig names.
def export(path,decimate=1):
 deps=bpy.context.evaluated_depsgraph_get();batches=defaultdict(list);triangles=0
 def absolute(name):
  p,t=pivots[name];return Vector(t)+(absolute(p) if p else Vector((0,0,0)))
 for o in list(bpy.context.scene.objects):
  if o.type!='MESH':continue
  if decimate<1:
   mod=o.modifiers.new('Distance LOD','DECIMATE');mod.ratio=decimate
   bpy.context.view_layer.update()
  ev=o.evaluated_get(deps);me=ev.to_mesh();me.calc_loop_triangles();group=o['pivot'];ma=o.data.materials[0];origin=absolute(group)
  # normals orientation from Blender geometry; keep both faces for sculpted thin panels
  V=[];N=[];F=[];lookup={}
  for tri in me.loop_triangles:
   for vi in tri.vertices:
    vert=me.vertices[vi];pos=o.matrix_world@vert.co-origin;n=o.matrix_world.to_3x3()@vert.normal;n.normalize();key=tuple(round(x,7) for x in (*pos,*n))
    if key not in lookup:lookup[key]=len(V);V.append(tuple(pos));N.append(tuple(n))
    F.append(lookup[key])
  batches[(group,ma.name)].append((V,N,F));triangles+=len(F)//3;ev.to_mesh_clear()
  if decimate<1:o.modifiers.remove(mod)
 bin=bytearray();views=[];accs=[];meshes=[];nodes=[];materials=list(MATS.values());mi={m['name']:i for i,m in enumerate(materials)}
 def acc(data,typ,ctype):
  while len(bin)%4:bin.append(0)
  off=len(bin);flat=[x for v in data for x in v] if typ=='VEC3' else data;fmt='f' if ctype==5126 else 'H';bin.extend(struct.pack('<'+fmt*len(flat),*flat));views.append({'buffer':0,'byteOffset':off,'byteLength':len(bin)-off});a={'bufferView':len(views)-1,'componentType':ctype,'count':len(data),'type':typ}
  if typ=='VEC3':a['min']=[min(v[i] for v in data) for i in range(3)];a['max']=[max(v[i] for v in data) for i in range(3)]
  accs.append(a);return len(accs)-1
 idx={name:i for i,name in enumerate(pivots)}
 for name,(parent,t) in pivots.items():nodes.append({'name':name,'translation':list(t),'children':[]})
 for name,(parent,t) in pivots.items():
  if parent:nodes[idx[parent]]['children'].append(idx[name])
 for (group,ma),chunks in batches.items():
  V=[];N=[];F=[]
  for v,n,f in chunks:base=len(V);V+=v;N+=n;F += [i+base for i in f]
  assert len(V)<65536,(group,ma,len(V))
  prim={'attributes':{'POSITION':acc(V,'VEC3',5126),'NORMAL':acc(N,'VEC3',5126)},'indices':acc(F,'SCALAR',5123),'material':mi[ma]};meshes.append({'name':group+'_'+ma,'primitives':[prim]});nodes[idx[group]]['children'].append(len(nodes));nodes.append({'name':group+'_'+ma,'mesh':len(meshes)-1})
 # Thin body lofts are intentionally two-sided; tires and solids remain closed.
 for m in materials:
  if m['name'].startswith(('01_','03_','07_','12_')):m['doubleSided']=True
 g={'asset':{'version':'2.0','generator':'Blender 4.3 / RACE QUEST rigid-pivot exporter'},'scene':0,'scenes':[{'nodes':[0]}],'nodes':nodes,'meshes':meshes,'materials':materials,'buffers':[{'byteLength':len(bin)}],'bufferViews':views,'accessors':accs,'extras':{'author':'RACE QUEST visual upgrade','axes':'X right Y up Z forward','wheelRadius':.205,'triangles':triangles,'materialBatches':len(meshes)}}
 js=json.dumps(g,separators=(',',':')).encode();js+=b' '*((-len(js))%4);bin+=b'\0'*((-len(bin))%4);total=12+8+len(js)+8+len(bin);path.write_bytes(struct.pack('<III',0x46546c67,2,total)+struct.pack('<II',len(js),0x4e4f534a)+js+struct.pack('<II',len(bin),0x004e4942)+bin);print('EXPORT',path,total,triangles,'triangles',len(meshes),'batches')
export(OUT/'race-quest-cat-sport.glb',.68)
export(OUT/'race-quest-cat-sport-low.glb',.28)
# Organize editable source into rigid pivot empties without changing world geometry.
objs=list(bpy.context.scene.objects);empties={}
for name in pivots:
 o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o);empties[name]=o
for name,(parent,t) in pivots.items():
 empties[name].parent=empties.get(parent);empties[name].location=t
bpy.context.view_layer.update()
for o in objs:
 world=o.matrix_world.copy();o.parent=empties[o['pivot']];o.matrix_world=world
# Blender viewport uses Y-up game coordinates. Save a useful orbit and solid-material view.
for area in bpy.context.screen.areas:
 if area.type=='VIEW_3D':
  area.spaces.active.region_3d.view_distance=4;area.spaces.active.region_3d.view_location=(0,.8,0);area.spaces.active.shading.color_type='MATERIAL'
# Convert the editor scene to Blender Z-up after exporting the game Y-up geometry.
empties['root'].rotation_euler[0]=math.pi/2
bpy.context.view_layer.update()
for area in bpy.context.screen.areas:
 if area.type=='VIEW_3D':area.spaces.active.region_3d.view_location=(0,0,.85)
bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=1.55,depth=.06,location=(0,0,-.04))
stage=bpy.context.object;stage.name='STUDIO — excluded from GLB export';stage.data.materials.append(navy)
bpy.ops.object.camera_add(location=(2.8,-3.8,2.2));camera=bpy.context.object;camera.name='Hero review camera';direction=Vector((0,0,.85))-camera.location;camera.rotation_euler=direction.to_track_quat('-Z','Y').to_euler();camera.data.lens=48;bpy.context.scene.camera=camera
for name,loc,power,size in [('Warm softbox',(-3,-4,5),650,4),('Cool fill',(3,-1,3),450,3),('Rim light',(0,3,4),800,3)]:
 bpy.ops.object.light_add(type='AREA',location=loc);light=bpy.context.object;light.name=name;light.data.energy=power;light.data.shape='DISK';light.data.size=size;light.rotation_euler=(Vector((0,0,.8))-light.location).to_track_quat('-Z','Y').to_euler()
bpy.context.scene.render.engine='CYCLES';bpy.context.scene.cycles.samples=32;bpy.context.scene.render.resolution_x=1200;bpy.context.scene.render.resolution_y=1000;bpy.context.scene.world.color=(.16,.16,.16)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source/race-quest-cat-sport.blend'))
