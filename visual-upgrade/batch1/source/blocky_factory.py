"""Small Blender authoring/export toolkit for rigid, vertex-coloured toy models.
Game axes: X right, Y up, Z forward. No subdivision, textures, or external IO.
"""
import bpy, bmesh, math, json, struct
from mathutils import Vector
from collections import defaultdict

def linear(hex):
 c=[int(hex[i:i+2],16)/255 for i in (0,2,4)]
 return [v/12.92 if v<.04045 else ((v+.055)/1.055)**2.4 for v in c]

class Builder:
 def __init__(self,identity,detail=True):
  bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
  for m in list(bpy.data.materials):bpy.data.materials.remove(m)
  self.identity=identity;self.high=detail;self.objects=[];self.materials={}
  self.pivots={identity:(None,(0,0,0)),'chassis':(identity,(0,0,0)),'driver':(identity,(0,0,0)),
   'driver_pose':('driver',(0,.67,-.17)), 'eyes':('driver_pose',(0,.62,.30)), 'eyes_happy':('driver_pose',(0,.62,.30)),
   'ear_l':('driver_pose',(-.23,.83,.01)),'ear_r':('driver_pose',(.23,.83,.01)),
   'tail':('driver_pose',(0,.05,-.20)),'steering':('chassis',(0,.83,.235)),
   'mouth_normal':('driver_pose',(0,.44,.33)),'mouth_happy':('driver_pose',(0,.44,.33)),'mouth_shock':('driver_pose',(0,.44,.33))}
  for side,x in [('l',-.59),('r',.59)]:
   for end,z in [('f',.48),('r',-.56)]:
    key='wheel_'+end+side;self.pivots[key]=(identity,(x,.205,z));self.pivots[key+'_spin']=(key,(0,0,0))
  for name,rough,metal,emit in [('21_Enamel',.39,.18,0),('22_Trim',.80,0,0),('23_Alloy',.35,.58,0),('24_Character',.86,0,0),('25_Rubber',.94,0,0),('26_LED',.36,.02,.12),('27_Smoked_glass',.29,.12,0)]:
   m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
   vc=m.node_tree.nodes.new('ShaderNodeVertexColor');vc.layer_name='ToyColor';m.node_tree.links.new(vc.outputs['Color'],p.inputs['Base Color'])
   if emit:p.inputs['Emission Color'].default_value=(.12,.12,.12,1);p.inputs['Emission Strength'].default_value=1
   self.materials[name[:2]]=(m,{'name':name,'pbrMetallicRoughness':{'baseColorFactor':[1,1,1,1],'roughnessFactor':rough,'metallicFactor':metal},'emissiveFactor':[emit]*3,'doubleSided':name.startswith('27_')})
 def object(self,o,name,color,kind,group,bevel=0):
  o.name=name;o['pivot']=group;o['author_color']=color;o.data.materials.append(self.materials[kind][0]);self.objects.append(o)
  for p in o.data.polygons:p.use_smooth=True
  if bevel:
   m=o.modifiers.new('Toy bevel, no subdivision','BEVEL');m.width=bevel;m.segments=2 if self.high else 1
  m=o.modifiers.new('Weighted planar normals','WEIGHTED_NORMAL');m.keep_sharp=True
  attr=o.data.color_attributes.new(name='ToyColor',type='FLOAT_COLOR',domain='POINT');c=linear(color)
  for item in attr.data:item.color=(*c,1)
  return o
 def box(self,name,c,size,color,kind='24',group='driver_pose',bevel=.02):
  bpy.ops.mesh.primitive_cube_add(size=1,location=c);o=bpy.context.object;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
  return self.object(o,name,color,kind,group,bevel)
 def mesh(self,name,v,f,color,kind='24',group='driver_pose',bevel=0):
  me=bpy.data.meshes.new(name);me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o)
  bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
  return self.object(o,name,color,kind,group,bevel)
 def prism(self,name,outline,z0,z1,color,kind='24',group='driver_pose',bevel=.02):
  n=len(outline);v=[(x,y,z) for z in [z0,z1] for x,y in outline]
  f=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
  return self.mesh(name,v,f,color,kind,group,bevel)
 def beam(self,name,a,b,width,depth,color,kind='24',group='driver_pose',bevel=.015):
  a,b=Vector(a),Vector(b);o=self.box(name,(a+b)/2,(width,(b-a).length,depth),color,kind,group,bevel);o.rotation_euler=(b-a).to_track_quat('Y','Z').to_euler();return o
 def tube(self,name,points,radius,color,kind='22',group='chassis',sides=8):
  v=[];f=[]
  for i,p in enumerate(points):
   t=(Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])).normalized();a=t.cross(Vector((0,1,0)))
   if a.length<.01:a=t.cross(Vector((1,0,0)))
   a.normalize();b=t.cross(a).normalized()
   for j in range(sides):v.append(tuple(Vector(p)+radius*(a*math.cos(math.tau*j/sides)+b*math.sin(math.tau*j/sides))))
  for i in range(len(points)-1):
   for j in range(sides):k=i*sides+j;q=i*sides+(j+1)%sides;f.append((k,q,q+sides,k+sides))
  f += [tuple(reversed(range(sides))),tuple((len(points)-1)*sides+j for j in range(sides))]
  return self.mesh(name,v,f,color,kind,group)
 def cylinder(self,name,c,radius,length,color,kind='23',group='chassis',sides=None,axis='X'):
  sides=sides or (24 if self.high else 12);v=[]
  for h in [-length/2,length/2]:
   for i in range(sides):
    a=i*math.tau/sides;p=(h,radius*math.cos(a),radius*math.sin(a)) if axis=='X' else (radius*math.cos(a),radius*math.sin(a),h)
    v.append(tuple(Vector(c)+Vector(p)))
  f=[tuple(reversed(range(sides))),tuple(range(sides,2*sides))]+[(j,(j+1)%sides,(j+1)%sides+sides,j+sides) for j in range(sides)]
  return self.mesh(name,v,f,color,kind,group)
 def loft(self,name,rows,color,kind='21'):
  # z, half-width, lower and upper height, corner chamfer; closed eight-sided loft.
  v=[]
  for z,w,lo,hi,r in rows:
   for x,y in [(w-r,hi),(w,hi-r),(w,lo+r),(w-r,lo),(-w+r,lo),(-w,lo+r),(-w,hi-r),(-w+r,hi)]:v.append((x,y,z))
  f=[tuple(reversed(range(8))),tuple((len(rows)-1)*8+j for j in range(8))]
  for i in range(len(rows)-1):
   for j in range(8):k=i*8+j;q=i*8+(j+1)%8;f.append((k,q,q+8,k+8))
  return self.mesh(name,v,f,color,kind,'chassis')
 def absolute(self,name):
  p,t=self.pivots[name];return Vector(t)+(self.absolute(p) if p else Vector((0,0,0)))
 def export(self,path,extras):
  deps=bpy.context.evaluated_depsgraph_get();bpy.context.view_layer.update();batches=defaultdict(lambda:[[],[],[],[]])
  for o in self.objects:
   ev=o.evaluated_get(deps);me=ev.to_mesh();me.calc_loop_triangles();origin=self.absolute(o['pivot']);V,N,C,F=batches[(o['pivot'],o.data.materials[0].name[:2])];lookup={};attr=me.color_attributes.get('ToyColor');normal_matrix=o.matrix_world.to_3x3().inverted().transposed()
   for tri in me.loop_triangles:
    for vi,li in zip(tri.vertices,tri.loops):
     pos=o.matrix_world@me.vertices[vi].co-origin;n=(normal_matrix@me.corner_normals[li].vector).normalized();c=tuple(max(0,min(1,x)) for x in attr.data[vi].color[:3]);key=tuple(round(x,7) for x in (*pos,*n,*c))
     if key not in lookup:lookup[key]=len(V);V.append(tuple(pos));N.append(tuple(n));C.append(c)
     F.append(lookup[key])
   ev.to_mesh_clear()
  bin=bytearray();views=[];accs=[];meshes=[];nodes=[];materials=[item[1] for item in self.materials.values()];mi={k:i for i,k in enumerate(self.materials)}
  def acc(data,typ):
   while len(bin)%4:bin.append(0)
   off=len(bin);flat=[x for v in data for x in v] if typ=='VEC3' else data;fmt='f' if typ=='VEC3' else 'H';bin.extend(struct.pack('<'+fmt*len(flat),*flat));views.append({'buffer':0,'byteOffset':off,'byteLength':len(bin)-off});a={'bufferView':len(views)-1,'componentType':5126 if typ=='VEC3' else 5123,'count':len(data),'type':typ}
   if typ=='VEC3':a.update(min=[min(v[i] for v in data) for i in range(3)],max=[max(v[i] for v in data) for i in range(3)])
   accs.append(a);return len(accs)-1
  idx={k:i for i,k in enumerate(self.pivots)}
  for name,(parent,t) in self.pivots.items():
   n={'name':name,'translation':list(t),'children':[]}
   if name in ['eyes_happy','mouth_happy']:n['extras']={'expression':'happy'}
   if name=='eyes':n['extras']={'expression':'eyes'}
   if name=='mouth_normal':n['extras']={'expression':'normal'}
   if name=='mouth_shock':n['extras']={'expression':'shock'}
   # Standard glTF viewers start with normal expression. The game renderer
   # selects expression groups explicitly and uses their authored rigid pose.
   if name in ['eyes_happy','mouth_happy','mouth_shock']:n['scale']=[0,0,0]
   nodes.append(n)
  for name,(parent,t) in self.pivots.items():
   if parent:nodes[idx[parent]]['children'].append(idx[name])
  for (group,kind),(V,N,C,F) in batches.items():
   assert len(V)<65536,(group,len(V));prim={'attributes':{'POSITION':acc(V,'VEC3'),'NORMAL':acc(N,'VEC3'),'COLOR_0':acc(C,'VEC3')},'indices':acc(F,'SCALAR'),'material':mi[kind]};name=group+'_'+kind
   meshes.append({'name':name,'primitives':[prim]});nodes[idx[group]]['children'].append(len(nodes));nodes.append({'name':name,'mesh':len(meshes)-1})
  stats={'triangles':sum(len(b[3])//3 for b in batches.values()),'materialBatches':len(batches),'LOD':'high' if self.high else 'low','axes':'X right Y up Z forward','wheelRadius':.205,**extras}
  nodes[0]['extras']={**extras,'up':'Y','forward':'+Z','units':'meter','collider':{'width':1.6,'height':1.3,'length':1.6},'wheelbase':1.04,'trackWidth':1.18,'steerAxis':'Y','spinAxis':'X'}
  g={'asset':{'version':'2.0','generator':'Blender 4.3 / RACE QUEST blocky factory'},'scene':0,'scenes':[{'nodes':[0]}],'nodes':nodes,'meshes':meshes,'materials':materials,'buffers':[{'byteLength':len(bin)}],'bufferViews':views,'accessors':accs,'extras':stats}
  js=json.dumps(g,separators=(',',':')).encode();js+=b' '*((-len(js))%4);bin+=b'\0'*((-len(bin))%4);total=28+len(js)+len(bin);path.write_bytes(struct.pack('<III',0x46546c67,2,total)+struct.pack('<II',len(js),0x4e4f534a)+js+struct.pack('<II',len(bin),0x004e4942)+bin)
  print('EXPORT',path.name,total,stats['triangles'],'triangles',len(meshes),'batches');return {'bytes':total,**stats}
 def save_source(self,path):
  empties={}
  for name in self.pivots:
   o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o);empties[name]=o
  for name,(parent,t) in self.pivots.items():empties[name].parent=empties.get(parent);empties[name].location=t
  bpy.context.view_layer.update()
  for o in self.objects:
   w=o.matrix_world.copy();o.parent=empties[o['pivot']];o.matrix_world=w
  # Editable source also opens in its clean normal expression. Restore a
  # variant group's scale to 1 and hide the normal group to edit that pose.
  for name in ['eyes_happy','mouth_happy','mouth_shock']:empties[name].scale=(0,0,0)
  empties[self.identity].rotation_euler[0]=math.pi/2;bpy.context.view_layer.update()
  bpy.ops.object.camera_add(location=(2.5,-3.5,2.2));camera=bpy.context.object;camera.name='Review camera';camera.rotation_euler=(Vector((0,0,1))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.lens=50;bpy.context.scene.camera=camera
  for loc,power in [((-3,-4,5),650),((3,-1,3),450),((0,3,4),700)]:
   bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=4;o.rotation_euler=(Vector((0,0,.8))-o.location).to_track_quat('-Z','Y').to_euler()
  scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene.world.color=(.16,.16,.16)
  for area in bpy.context.screen.areas:
   if area.type=='VIEW_3D':area.spaces.active.region_3d.view_distance=3.8;area.spaces.active.region_3d.view_location=(0,0,.9);area.spaces.active.shading.color_type='VERTEX'
  bpy.ops.wm.save_as_mainfile(filepath=str(path))
