"""Build ONLY Batch 1: Pinguin/Kapsul, Beruang/Buggy, Kelinci/Formula.
Run from repository root: blender -b --python-exit-code 1 --python visual-upgrade/batch1/source/build_batch1.py
The accepted cat and all later-batch assets are never read or written here.
"""
import pathlib,sys,math,json
HERE=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(HERE));sys.dont_write_bytecode=True
from blocky_factory import Builder
OUT=HERE.parent
CHARACTERS=[{'id':'nara','name':'Pinguin','animal':'penguin','vehicle':'Kapsul','root':'race_quest_penguin','paint':'25BFC8','accent':'F6C468','fur':'333C54','cream':'FFF3DE'},
 {'id':'bimo','name':'Beruang','animal':'bear','vehicle':'Buggy','root':'race_quest_bear','paint':'ED7550','accent':'EAD9AC','fur':'D18D60','cream':'F2C792'},
 {'id':'sora','name':'Kelinci','animal':'rabbit','vehicle':'Formula','root':'race_quest_rabbit','paint':'9974ED','accent':'FFCFD8','fur':'FFF1E5','cream':'FFF9ED'}]
INK='172331';TRIM='203649';WHITE='F5F2DE';STEEL='AABBCB';PINK='ED95B0'

def driver(B,c):
 animal=c['animal'];fur=c['fur'];cream=c['cream'];penguin=animal=='penguin';bear=animal=='bear';rabbit=animal=='rabbit'
 if penguin:
  B.box('Tall cube penguin head',(0,1.230,-.10),(.60,.60,.46),fur,bevel=.065)
  # A single flat heart/bib outline, with an angular brow notch; no fur sculpt.
  outline=[(-.245,1.08),(-.245,1.37),(-.195,1.430),(-.070,1.430),(0,1.405),(.070,1.430),(.195,1.430),(.245,1.37),(.245,1.08),(.185,1.035),(-.185,1.035)]
  B.prism('White penguin face bib',outline,.128,.143,cream,bevel=.022)
  headfront=.143;eyeX=.122;eyeY=1.286;eyeZ=.151
 else:
  w=.36 if bear else .32;lo= .970 if bear else 1.005;hi=1.515 if bear else 1.505
  B.prism('Wide bear cube jaw' if bear else 'Compact rabbit cube head',[(-w*.87,lo),(-w,lo+.09),(-w,hi-.04),(-w+.04,hi),(w-.04,hi),(w,hi-.04),(w,lo+.09),(w*.87,lo)],-.35 if bear else -.295,.17 if bear else .135,fur,bevel=.042)
  headfront=.17 if bear else .135;eyeX=.177 if bear else .145;eyeY=1.286;eyeZ=headfront+.010
  if bear:
   B.box('Small square cream bear muzzle',(0,1.124,.190),(.245,.167,.052),cream,bevel=.037)
   B.box('Bear button nose',(0,1.169,.226),(.079,.051,.025),INK,bevel=.014)
  else:
   B.box('Rabbit tiny pink nose',(0,1.180,.151),(.053,.034,.025),PINK,bevel=.010)
   for side in [-1,1]:B.box('Soft pink rabbit cheek',(side*.237,1.180,.140),(.060,.036,.010),'F5B0BF',bevel=.010)
 # Short bodies share contact constraints, not identical skulls or anatomy.
 B.box('Short chibi torso',(0,.744,-.23),(.35 if bear else .32,.418,.34),fur,bevel=.038)
 B.box('Cream chest panel',(0,.757,-.052),(.236,.267,.020),cream,bevel=.027)
 B.box('Short neck',(0,.966,-.19),(.19,.11,.19),fur,bevel=.022)
 for side,label in [(-1,'l'),(1,'r')]:
  if penguin:
   # Flattened flipper arms, with a darker outer edge and broad mitten tip.
   B.beam('Block flipper upper',(side*.150,.870,-.16),(side*.224,.790,.015),.123,.095,fur,bevel=.025)
   B.beam('Block flipper forearm',(side*.224,.790,.015),(side*.181,.840,.214),.100,.100,'3C4960',bevel=.020)
   paw='3C4960';foot='F6BB42'
  else:
   B.beam('Short upper arm',(side*.155,.875,-.17),(side*.231,.790,.015),.143 if bear else .123,.128,fur,bevel=.023)
   B.beam('Short bent forearm',(side*.231,.790,.015),(side*.181,.840,.214),.119,.115,fur,bevel=.023)
   paw=cream if bear else fur;foot=cream
  B.box('Steering mitten '+label,(side*.181,.840,.234),(.125,.126,.115),paw,bevel=.024)
  B.box('Grip thumb '+label,(side*.145,.813,.208),(.051,.057,.063),paw,bevel=.014)
  B.box('Short seated thigh',(side*.105,.595,-.032),(.147,.140,.25),fur,bevel=.024)
  B.box('Webbed yellow foot' if penguin else 'Short toy foot',(side*.108,.565,.105),(.153,.103,.155 if not rabbit else .180),foot,bevel=.019)
  if bear:
   B.box('Rounded square bear ear '+label,(side*.245,1.568,-.150),(.179,.200,.146),fur,group='ear_'+label,bevel=.037)
   B.box('Bear ear inset '+label,(side*.245,1.584,-.070),(.104,.114,.013),cream,group='ear_'+label,bevel=.020)
  if rabbit:
   tilt=-side*.12
   o=B.box('Long block rabbit ear '+label,(side*.175,1.713,-.112),(.132,.475,.126),fur,group='ear_'+label,bevel=.029);o.rotation_euler.z=tilt
   o=B.box('Long pink inner ear '+label,(side*.175,1.717,-.043),(.075,.343,.012),PINK,group='ear_'+label,bevel=.017);o.rotation_euler.z=tilt
  B.box('Large readable rectangular eye',(side*eyeX,eyeY,eyeZ),(.071 if bear else .067,.116 if penguin else .110,.015),INK,group='eyes',bevel=.010)
  B.box('Square eye catchlight',(side*eyeX-.009,eyeY+.028,eyeZ+.010),(.024,.030,.004),'FFFAEA',group='eyes',bevel=.003)
  # Happy closed eyes: two short block segments, never dense curves.
  for a,b in [((side*eyeX-.034,eyeY+.003,eyeZ),(side*eyeX,eyeY+.029,eyeZ)),((side*eyeX,eyeY+.029,eyeZ),(side*eyeX+.034,eyeY+.003,eyeZ))]:
   B.beam('Happy chevron eye',a,b,.013,.012,INK,group='eyes_happy',bevel=.004)
 # Distinct facial anatomy, with light rigid expression variants.
 if penguin:
  B.box('Square upper beak',(0,1.185,.181),(.180,.061,.092),'F7BE42',bevel=.015)
  B.box('Square lower beak',(0,1.151,.179),(.156,.032,.080),'ED9D31',bevel=.010)
  mouthY=1.155;mouthZ=.230;mw=.113;mh=.039
 else:mouthY=1.105 if bear else 1.122;mouthZ=.224 if bear else .149;mw=.094;mh=.069
 # Normal friendly smile, an open flat shape with a small tongue.
 for group,scale in [('mouth_normal',.78),('mouth_happy',1.22)]:
  w=mw*scale;h=mh*scale
  outline=[(-w/2,mouthY+h*.40),(-w*.2,mouthY+h*.24),(0,mouthY+h*.35),(w*.2,mouthY+h*.24),(w/2,mouthY+h*.40),(w*.43,mouthY-h*.24),(w*.23,mouthY-h*.48),(-w*.23,mouthY-h*.48),(-w*.43,mouthY-h*.24)]
  B.prism('Friendly smile '+group,outline,mouthZ,mouthZ+.006,INK,group=group,bevel=.002)
  B.box('Pink tongue '+group,(0,mouthY-h*.25,mouthZ+.008),(w*.48,h*.28,.004),PINK,group=group,bevel=.004)
  if rabbit:
   for side in [-1,1]:B.box('Rabbit square front tooth',(side*.012,mouthY+h*.16,mouthZ+.010),(.020,.024,.004),'FFFFF5',group=group,bevel=.002)
 B.box('Surprised square mouth',(0,mouthY,mouthZ+.003),(mw*.68,mh*1.25,.008),INK,group='mouth_shock',bevel=.014)
 B.box('Surprised mouth inset',(0,mouthY-mh*.2,mouthZ+.009),(mw*.35,mh*.38,.004),PINK,group='mouth_shock',bevel=.005)
 if bear:
  B.beam('Bear tail root',(-.14,.695,-.33),(-.230,.695,-.33),.075,.075,fur,group='tail',bevel=.014)
  B.box('Bear stub tail',(-.237,.696,-.33),(.102,.108,.084),fur,group='tail',bevel=.027)
 if rabbit:
  B.beam('Rabbit tail root',(-.13,.70,-.33),(-.23,.70,-.33),.080,.080,cream,group='tail',bevel=.016)
  B.box('Rabbit cube cotton tail',(-.245,.702,-.33),(.145,.147,.110),cream,group='tail',bevel=.039)

def cockpit(B,c):
 if c['animal']=='rabbit':
  B.loft('Formula tapered structural floor',[(-.74,.26,.18,.27,.02),(-.45,.42,.18,.27,.02),(.10,.42,.18,.27,.02),(.40,.21,.18,.26,.015),(.74,.13,.18,.23,.015)],TRIM,'22')
 else:B.box('Low structural floor',(0,.242,-.01),(1.00,.125,1.47),TRIM,'22','chassis',.035)
 B.box('Seat cushion',(0,.470,-.27),(.43,.115,.43),TRIM,'22','chassis',.045)
 B.box('Seat back',(0,.670,-.48),(.43,.405,.095),TRIM,'22','chassis',.052)
 for side in [-1,1]:B.box('Seat colour bolster',(side*.183,.675,-.422),(.034,.31,.035),c['accent'],'22','chassis',.012)
 B.tube('Steering column',[(0,.49,.18),(0,.81,.235)],.018,STEEL,'23')
 rim=[(.18*math.cos(i*math.tau/32),.83+.18*.88*math.sin(i*math.tau/32),.235+.18*.48*math.sin(i*math.tau/32)) for i in range(33)]
 B.tube('Steering rim',rim,.021,TRIM if c['animal']!='penguin' else 'E9DABB','22','steering',8)
 for angle in [0,math.pi,math.pi*1.5]:
  B.tube('Steering spoke',[(0,.83,.235),(.145*math.cos(angle),.83+.145*.88*math.sin(angle),.235+.145*.48*math.sin(angle))],.012,STEEL,'23','steering',6)
 B.box('Steering centre',(0,.83,.245),(.071,.064,.028),c['paint'],'21','steering',.015)

def wheels(B,c):
 animal=c['animal'];n=24 if B.high else 12
 for side,x in [('l',-.59),('r',.59)]:
  sign=-1 if x<0 else 1
  for end,z in [('f',.48),('r',-.56)]:
   group='wheel_'+end+side+'_spin';profile=[(-.101,.143),(-.100,.177),(-.073,.199),(-.043,.205),(.043,.205),(.073,.199),(.100,.177),(.101,.143)]
   if animal=='bear':profile=[(xx,r*.945) for xx,r in profile]
   v=[(x+xx,.205+r*math.cos(i*math.tau/n),z+r*math.sin(i*math.tau/n)) for xx,r in profile for i in range(n)]
   f=[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(len(profile)-1) for i in range(n)]
   B.mesh('Slick tyre' if animal=='rabbit' else 'Capsule tyre' if animal=='penguin' else 'Offroad tyre carcass',v,f,'283443','25',group)
   if animal=='bear':
    for i in range(16 if B.high else 12):
     a=i*math.tau/(16 if B.high else 12);o=B.box('Square offroad tread lug',(x,.205+.195*math.cos(a),z+.195*math.sin(a)),(.170,.020,.039),'303B46','25',group,.004 if B.high else 0);o.rotation_euler.x=a
     if B.high:
      for mod in o.modifiers:
       if mod.type=='BEVEL':mod.segments=1
   face=x+sign*.104
   B.cylinder('Rim inset',(face,.205,z),.141,.014,'192B3D','22',group)
   B.cylinder('Machined rim face',(face+sign*.008,.205,z),.121,.009,STEEL,'23',group)
   B.cylinder('Inset hub disc',(face+sign*.014,.205,z),.089,.008,c['paint'],'23',group)
   count=5 if animal=='rabbit' else 4 if animal=='bear' else 3
   for i in range(count):
    a=i*math.tau/count
    B.beam('Readable wheel spoke',(face+sign*.022,.205+.040*math.cos(a),z+.040*math.sin(a)),(face+sign*.022,.205+.114*math.cos(a),z+.114*math.sin(a)),.023,.016,WHITE if animal=='rabbit' else STEEL,'23',group,.003)
   B.cylinder('Axle cap',(face+sign*.029,.205,z),.031,.013,c['accent'],'23',group,sides=12 if B.high else 8)

def capsule(B,c):
 p=c['paint'];a=c['accent']
 B.loft('Capsule rounded lower monocoque',[(-.83,.12,.24,.34,.035),(-.70,.35,.20,.43,.06),(-.45,.45,.20,.43,.06),(.30,.45,.20,.43,.06),(.65,.37,.21,.40,.06),(.84,.17,.25,.32,.035)],p)
 B.loft('Capsule sculpted nose',[(.16,.31,.34,.59,.055),(.35,.42,.29,.58,.07),(.58,.40,.26,.53,.07),(.76,.31,.26,.46,.055),(.85,.20,.30,.40,.045)],p)
 for side in [-1,1]:
  B.tube('Capsule cockpit coaming',[(side*.31,.47,.22),(side*.36,.54,-.04),(side*.35,.57,-.39),(side*.27,.52,-.64)],.045,WHITE,'21')
  for z in [.48,-.56]:
   verts=[];steps=14 if B.high else 8
   for radius in [.247,.233]:
    for i in range(steps+1):
     t=.16+(math.pi-.32)*i/steps
     for xx in [.48,.704]:verts.append((side*xx,.205+radius*math.sin(t),z+radius*math.cos(t)))
   layer=2*(steps+1);faces=[]
   for i in range(steps):
    k=2*i;faces.extend([(k,k+1,k+3,k+2),(k+layer+2,k+layer+3,k+layer+1,k+layer),(k,k+2,k+2+layer,k+layer),(k+1+layer,k+3+layer,k+3,k+1)])
   faces.extend([(0,layer,layer+1,1),(layer-2,layer-1,2*layer-1,2*layer-2)])
   B.mesh('Solid capsule curved wheel shroud',verts,faces,p,'21','chassis')
  B.box('Capsule headlight',(side*.105,.357,.855),(.145,.035,.020),'E5F5EC','26','chassis',.015)
  B.box('Capsule rear LED',(side*.248,.387,-.752),(.136,.043,.026),'F67F70','26','chassis',.012)
  B.cylinder('Rear pod thruster',(side*.220,.292,-.795),.066,.062,TRIM,'22','chassis',axis='Z')
  B.cylinder('Rear pod glow',(side*.220,.292,-.831),.041,.005,a,'26','chassis',axis='Z')
 B.box('Capsule floating nose bumper',(0,.246,.814),(.58,.075,.095),WHITE,'21','chassis',.030)
 rows=[(.25,.588),(.35,.581),(.58,.531),(.68,.493)]
 v=[(x,y+.001,z) for z,y in rows for x in [-.034,.034]]
 B.mesh('Capsule amber centre flash',v,[(i,i+1,i+3,i+2) for i in range(0,len(v)-2,2)],a,'21','chassis')
 v=[];steps=12 if B.high else 6
 for row in [0,1]:
  for i in range(steps+1):
   u=-1+2*i/steps;v.append((u*.285,.585+row*(.160-.10*u*u),.160-row*.050+.070*(1-u*u)))
 B.mesh('Capsule solid smoked blue windscreen',v,[(i,i+1,i+steps+2,i+steps+1) for i in range(steps)],'438A9C','27','chassis')
 B.tube('Capsule windscreen upper frame',v[steps+1:],.015,WHITE,'21','chassis',8)
 B.loft('Capsule rear pod cover',[(-.75,.26,.34,.50,.03),(-.55,.32,.38,.56,.035),(-.48,.27,.40,.54,.025)],p)

def buggy(B,c):
 p=c['paint'];a=c['accent']
 B.loft('Buggy angular hood',[(.16,.34,.29,.535,.035),(.46,.42,.27,.485,.025),(.73,.405,.26,.415,.025)],p)
 B.box('Buggy rear engine deck',(0,.420,-.615),(.74,.20,.29),p,'21','chassis',.035)
 B.box('Buggy front black grille',(0,.343,.747),(.56,.133,.030),TRIM,'22','chassis',.016)
 for x in [-.21,-.105,0,.105,.21]:B.box('Buggy grille slot',(x,.347,.768),(.026,.080,.012),STEEL,'23','chassis',.003)
 for side in [-1,1]:
  for z in [.48,-.56]:
   B.box('Raised buggy fender',(side*.515,.469,z),(.310,.060,.430),p,'21','chassis',.023)
   B.tube('Visible suspension arm',[(side*.32,.280,z+.06),(side*.52,.205,z)],.018,STEEL,'23')
  B.tube('Buggy side nerf rail',[(side*.47,.285,.48),(side*.49,.300,-.43),(side*.36,.38,-.64)],.033,TRIM,'22')
  B.box('Buggy square headlamp',(side*.333,.392,.753),(.123,.100,.052),'FFE4A2','26','chassis',.018)
  B.box('Buggy rear lamp',(side*.279,.428,-.787),(.140,.044,.026),'F97868','26','chassis',.010)
  B.box('Buggy hood inlay',(side*.222,.507,.254),(.054,.012,.155),a,'21','chassis',.006)
  B.tube('Buggy rear roll upright',[(side*.280,.478,-.51),(side*.285,.988,-.51),(side*.215,1.044,-.51)],.025,TRIM,'22')
  B.tube('Buggy front bumper guard',[(side*.37,.280,.812),(side*.40,.36,.812)],.024,STEEL,'23')
 B.tube('Buggy rear roll crossbar',[(-.215,1.044,-.51),(.215,1.044,-.51)],.025,TRIM,'22')
 B.box('Buggy skid bumper',(0,.235,.815),(.94,.085,.100),STEEL,'23','chassis',.024)
 B.box('Buggy rear impact bar',(0,.238,-.815),(.83,.075,.10),TRIM,'22','chassis',.021)
 for x in [-.20,-.10,0,.10,.20]:B.box('Engine deck vent',(x,.524,-.634),(.055,.008,.155),TRIM,'22','chassis',.005)
 B.box('Buggy hood badge',(0,.467,.540),(.125,.013,.103),a,'21','chassis',.010)

def formula(B,c):
 p=c['paint'];a=c['accent']
 B.loft('Formula tapered central nose',[(.15,.230,.280,.505,.028),(.35,.173,.235,.445,.024),(.62,.135,.207,.330,.020),(.837,.100,.202,.265,.017)],p)
 B.loft('Formula narrow tail spine',[(-.79,.12,.27,.43,.02),(-.60,.29,.27,.53,.03),(-.42,.285,.27,.51,.025)],p)
 for side in [-1,1]:
  B.box('Formula floating sidepod',(side*.352,.346,-.075),(.178,.185,.650),p,'21','chassis',.031)
  B.box('Formula sidepod intake',(side*.352,.360,.257),(.118,.094,.018),TRIM,'22','chassis',.012)
  B.box('Formula sidepod ivory inlay',(side*.449,.375,-.13),(.009,.042,.450),WHITE,'21','chassis',.004)
  B.box('Formula front wing endplate',(side*.532,.250,.765),(.025,.134,.220),p,'21','chassis',.009)
  B.box('Formula rear wing endplate',(side*.492,.657,-.754),(.027,.136,.209),p,'21','chassis',.011)
  B.box('Formula rear wing pillar',(side*.220,.510,-.713),(.027,.260,.049),TRIM,'22','chassis',.009)
  B.tube('Formula front wishbone',[(side*.20,.260,.450),(side*.51,.225,.480)],.016,STEEL,'23')
  B.tube('Formula rear wishbone',[(side*.25,.280,-.49),(side*.51,.225,-.56)],.016,STEEL,'23')
  B.box('Formula narrow headlamp',(side*.120,.307,.701),(.054,.027,.050),'DEF4E9','26','chassis',.009)
 B.box('Formula front wing',(0,.196,.768),(1.090,.040,.190),WHITE,'21','chassis',.012)
 B.box('Formula front wing leading lip',(0,.226,.701),(.94,.016,.038),p,'21','chassis',.006)
 B.box('Formula rear wing',(0,.660,-.754),(.985,.038,.200),p,'21','chassis',.014)
 B.box('Formula rear wing pink livery',(0,.683,-.754),(.425,.008,.175),a,'21','chassis',.004)
 B.box('Formula rear red rain lamp',(0,.421,-.800),(.065,.055,.024),'FF737D','26','chassis',.010)
 # Thin livery panels follow the actual wedge contour.
 rows=[(.19,.493),(.35,.446),(.62,.332),(.81,.276)]
 v=[(x,y+.002,z) for z,y in rows for x in [-.036,.036]]
 B.mesh('Formula central ivory stripe',v,[(i,i+1,i+3,i+2) for i in range(0,len(v)-2,2)],WHITE,'21','chassis')
 B.tube('Formula cockpit rim',[(-.25,.51,.20),(-.29,.55,-.30),(0,.58,-.51),(.29,.55,-.30),(.25,.51,.20)],.025,TRIM,'22')

report=[]
for c in CHARACTERS:
 result={'id':c['id'],'name':c['name'],'vehicle':c['vehicle'],'models':{}}
 for high in [True,False]:
  B=Builder(c['root'],high);cockpit(B,c);{'penguin':capsule,'bear':buggy,'rabbit':formula}[c['animal']](B,c);wheels(B,c);driver(B,c)
  file='kart_'+c['id']+('' if high else '_low')+'.glb';result['models']['high' if high else 'low']=B.export(OUT/'models'/file,{'animal':c['animal'],'vehicle':c['vehicle'],'identityReference':'avatar_'+c['id']+'.webp','style':'blocky chibi','version':'Batch 1'})
  if high:B.save_source(HERE/('race-quest-'+c['id']+'.blend'))
 report.append(result)
(OUT/'build-metrics.json').write_text(json.dumps(report,indent=2))
