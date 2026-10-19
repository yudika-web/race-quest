"""Final three original blocky racers, using protected shared Blender toolkit.
blender -b --python-exit-code 1 --python visual-upgrade/batch4/source/build_batch4.py
Only Batch 4 models/sources are generated. No historical build loop is executed.
"""
import pathlib,sys,math,json,ast
HERE=pathlib.Path(__file__).resolve().parent;OUT=HERE.parent;SHARED=HERE.parents[1]
sys.path.insert(0,str(SHARED/'batch1/source'));sys.dont_write_bytecode=True
from blocky_factory import Builder
INK='172331';TRIM='203649';WHITE='F5F2DE';STEEL='AABBCB';PINK='ED95B0'
for source,names in [('batch1/source/build_batch1.py',['cockpit','wheels']),('batch2/source/build_batch2.py',['eyes_and_smiles']),('batch3/source/build_batch3.py',['common_details'])]:
 tree=ast.parse((SHARED/source).read_text());exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(SHARED/source),'exec'))
CHARACTERS=[
 dict(id='panda',name='Panda',animal='panda',vehicle='Bamboo',root='race_quest_panda',paint='65A965',accent='E8D8A3',fur='FFF0DB',cream='F8E7CE'),
 dict(id='koala',name='Koala',animal='koala',vehicle='Eco Pod',root='race_quest_koala',paint='90D5C5',accent='EBF0DE',fur='AFADBB',cream='E9DACB'),
 dict(id='rakun',name='Rakun',animal='raccoon',vehicle='Trail Pickup',root='race_quest_raccoon',paint='466F80',accent='E3C394',fur='A8A0A2',cream='F3DFCB')]

def body(B,c):
 fur=c['fur'];cream=c['cream'];panda=c['animal']=='panda';dark='3F404E' if panda else '777381'
 if panda:
  B.prism('Panda plump tapered belly',[(-.142,.536),(-.185,.590),(-.185,.818),(-.150,.945),(.150,.945),(.185,.818),(.185,.590),(.142,.536)],-.401,-.060,fur,bevel=.030)
  B.box('Panda shoulder saddle',(0,.902,-.235),(.337,.103,.320),dark,bevel=.026)
 else:B.box('Short species torso',(0,.744,-.23),(.327,.418,.34),fur,bevel=.032)
 if not panda:B.box('Warm chest graphic',(0,.757,-.052),(.225,.268,.020),cream,bevel=.023)
 B.box('Short chibi neck',(0,.970,-.18),(.178,.11,.178),dark if panda else fur,bevel=.018)
 for side,label in [(-1,'l'),(1,'r')]:
  arm=dark if panda else fur;paw=dark if c['animal'] in ['panda','raccoon'] else '85818F'
  B.beam('Short upper foreleg',(side*.155,.875,-.17),(side*.231,.790,.015),.135,.117,arm,bevel=.021)
  B.beam('Short bent wrist',(side*.231,.790,.015),(side*.181,.840,.214),.111,.110,arm,bevel=.020)
  B.box('Steering mitten '+label,(side*.181,.840,.234),(.125,.126,.115),paw,bevel=.023)
  B.box('Inner wheel thumb '+label,(side*.145,.813,.208),(.051,.057,.063),paw,bevel=.013)
  B.box('Seated short thigh',(side*.105,.595,-.032),(.147,.140,.25),dark if panda else fur,bevel=.021)
  B.box('Short chibi foot',(side*.108,.565,.105),(.153,.103,.155),paw,bevel=.018)
  for dx in [-.021,.021]:B.box('Subtle graphic toe mark',(side*.108+dx,.570,.185),(.006,.026,.004),'9B9298',bevel=.001)

def panda(B,c):
 fur=c['fur'];dark='3F404E'
 B.box('Panda large soft cube head',(0,1.248,-.100),(.650,.526,.470),fur,bevel=.052)
 for side,label in [(-1,'l'),(1,'r')]:
  B.box('Short black panda ear',(side*.247,1.551,-.124),(.180,.184,.145),dark,group='ear_'+label,bevel=.036)
  B.box('Dark grey ear inset',(side*.247,1.560,-.047),(.096,.092,.010),'57525F',group='ear_'+label,bevel=.018)
  o=B.box('Flush graphic panda eye patch',(side*.154,1.290,.136),(.130,.172,.013),'57525F',bevel=.024);o.rotation_euler.z=-side*.16
 B.box('Tiny cream panda muzzle',(0,1.133,.155),(.150,.108,.035),c['cream'],bevel=.021)
 B.box('Small panda nose',(0,1.171,.181),(.062,.041,.025),INK,bevel=.010)
 eyes_and_smiles(B,c,.154,1.297,.151,1.105,.178,.085,.061)
 B.beam('Panda tail root',(-.14,.719,-.325),(-.232,.731,-.330),.073,.072,fur,group='tail',bevel=.014)
 B.box('Panda small square tail',(-.244,.738,-.33),(.097,.098,.088),fur,group='tail',bevel=.024)

def koala(B,c):
 fur=c['fur'];cream=c['cream']
 B.prism('Koala broad cube chin',[(-.248,1.005),(-.305,1.070),(-.305,1.434),(-.265,1.478),(.265,1.478),(.305,1.434),(.305,1.070),(.248,1.005)],-.326,.137,fur,bevel=.039)
 for side,label in [(-1,'l'),(1,'r')]:
  B.pivots['ear_'+label]=('driver_pose',(side*.285,.690,.070))
  B.box('Large round square koala ear',(side*.337,1.326,-.105),(.247,.306,.162),fur,group='ear_'+label,bevel=.050)
  B.box('Warm koala ear inset',(side*.350,1.329,-.016),(.165,.218,.017),'E9C7CE',group='ear_'+label,bevel=.035)
  B.box('Soft koala cheek',(side*.207,1.167,.141),(.070,.035,.009),'C8B7C0',bevel=.009)
 B.box('Big vertical koala nose',(0,1.226,.169),(.108,.148,.047),'3E3F4D',bevel=.025)
 eyes_and_smiles(B,c,.145,1.293,.150,1.111,.149,.077,.054)
 B.beam('Koala stub tail root',(-.14,.728,-.325),(-.230,.736,-.329),.067,.066,fur,group='tail',bevel=.013)
 B.box('Koala tiny tail',(-.242,.742,-.329),(.086,.090,.080),fur,group='tail',bevel=.023)

def raccoon(B,c):
 fur=c['fur'];cream=c['cream'];dark='53515E'
 B.prism('Raccoon angular cube jaw',[(-.237,1.003),(-.313,1.076),(-.313,1.431),(-.266,1.481),(.266,1.481),(.313,1.431),(.313,1.076),(.237,1.003)],-.329,.140,fur,bevel=.036)
 mask=[(-.290,1.220),(-.290,1.340),(-.213,1.378),(-.105,1.334),(0,1.302),(.105,1.334),(.213,1.378),(.290,1.340),(.290,1.220),(.133,1.202),(0,1.246),(-.133,1.202)]
 B.prism('Flush continuous raccoon eye mask',mask,.136,.148,dark,bevel=.009)
 B.prism('Graphic cream jaw',[(-.205,1.018),(-.278,1.086),(-.230,1.158),(0,1.133),(.230,1.158),(.278,1.086),(.205,1.018)],.140,.151,cream,bevel=.012)
 B.box('Short raccoon muzzle',(0,1.139,.176),(.202,.129,.053),cream,bevel=.025)
 B.box('Raccoon small black nose',(0,1.182,.212),(.066,.042,.025),INK,bevel=.011)
 for side,label in [(-1,'l'),(1,'r')]:
  x=side*.226
  B.prism('Short thick raccoon ear',[(x-side*.092,1.429),(x-side*.067,1.644),(x+side*.006,1.671),(x+side*.112,1.458)],-.239,-.097,fur,group='ear_'+label,bevel=.020)
  B.prism('Raccoon dark inner ear',[(x-side*.052,1.478),(x-side*.031,1.604),(x+side*.006,1.617),(x+side*.065,1.490)],-.094,-.082,dark,group='ear_'+label,bevel=.011)
 eyes_and_smiles(B,c,.156,1.293,.159,1.108,.207,.092,.064)
 B.pivots['tail']=('driver_pose',(-.265,.08,-.15))
 B.beam('Raccoon tail root',(-.14,.733,-.315),(-.279,.775,-.347),.091,.091,fur,group='tail',bevel=.018)
 points=[(-.280,.770,-.350),(-.325,.827,-.380),(-.345,.887,-.408),(-.350,.952,-.434),(-.335,1.017,-.455),(-.307,1.075,-.468)]
 for i,(a,b) in enumerate(zip(points,points[1:])):
  # Slightly overlapping solids retain clean joints while colours describe rings.
  w=[.132,.144,.152,.146,.125][i]
  direction=[b[k]-a[k] for k in range(3)];length=math.sqrt(sum(v*v for v in direction));aa=tuple(a[k]-.006*direction[k]/length for k in range(3));bb=tuple(b[k]+.006*direction[k]/length for k in range(3))
  B.beam('Banded block tail segment '+str(i),aa,bb,w,.145,dark if i%2==0 else 'B9B0B1',group='tail',bevel=.014)

def leaf_badge(B,name,c,color,kind='21',group='chassis',size=.08,slope=0):
 x,y,z=c
 v=[(x-size*.48,y-slope*size*.5,z-size*.5),(x+size*.45,y,z),(x+size*.18,y+slope*size*.46,z+size*.46),(x-size*.38,y+slope*size*.35,z+size*.35)]
 B.mesh(name,v,[(3,2,1,0)],color,kind,group)

def bamboo(B,c):
 p=c['paint'];a=c['accent'];light='99C979';deep='3C7454'
 B.loft('Bamboo stepped structural hull',[(-.79,.23,.25,.40,.035),(-.61,.355,.22,.48,.040),(-.38,.405,.22,.49,.040),(.30,.405,.23,.49,.040),(.67,.330,.26,.44,.035),(.80,.21,.29,.39,.025)],deep)
 B.loft('Bamboo segmented broad bonnet',[(.18,.295,.34,.553,.035),(.40,.375,.29,.529,.040),(.65,.340,.27,.468,.035),(.79,.245,.29,.415,.025)],p)
 for z,y,w in [(.280,.548,.325),(.458,.516,.363),(.630,.475,.345)]:
  B.box('Bamboo raised structural node',(0,y,z),(w*2,.025,.035),light,'21','chassis',.009)
 for side in [-1,1]:
  for i,z in enumerate([-.286,-.073,.140]):
   B.box('Segmented bamboo side body',(side*.401,.364,z),(.147,.187,.213),p if i%2 else light,'21','chassis',.025)
   B.box('Bamboo side joint band',(side*.410,.365,z+.089),(.157,.198,.024),deep,'21','chassis',.007)
  for z in [.48,-.56]:B.box('Bamboo broad node fender',(side*.521,.459,z),(.301,.067,.400),p,'21','chassis',.022)
  B.box('Bamboo square cream headlight',(side*.264,.431,.743),(.126,.073,.047),'FFF0BD','26','chassis',.016)
  B.box('Bamboo rear amber lamp',(side*.237,.414,-.757),(.132,.043,.027),'EBAE6D','26','chassis',.010)
  B.tube('Bamboo light rear arch',[(side*.265,.51,-.505),(side*.268,.936,-.535),(side*.211,.984,-.535)],.019,deep,'22')
 B.tube('Bamboo arch top',[(-.211,.984,-.535),(.211,.984,-.535)],.019,deep,'22')
 B.box('Bamboo compact dark grille',(0,.343,.801),(.350,.098,.024),TRIM,'22','chassis',.018)
 for x in [-.118,0,.118]:B.box('Bamboo grille node',(x,.344,.817),(.025,.072,.010),a,'21','chassis',.006)
 B.box('Bamboo cream chin bumper',(0,.250,.795),(.796,.089,.098),a,'21','chassis',.026)
 B.box('Bamboo rear segmented cowl',(0,.442,-.636),(.631,.139,.212),p,'21','chassis',.027)
 B.box('Bamboo low rear spoiler',(0,.555,-.694),(.709,.035,.140),light,'21','chassis',.013)
 leaf_badge(B,'Bamboo original hood leaf emblem',(0,.493,.570),a,size=.075,slope=-.24)

def ecopod(B,c):
 p=c['paint'];a=c['accent'];teal='369C9D';cyan='73E1DB'
 B.loft('Eco compact chamfered lower pod',[(-.783,.240,.25,.38,.035),(-.61,.377,.22,.445,.043),(.43,.377,.23,.45,.043),(.760,.282,.26,.406,.035)],teal)
 B.box('Eco square upright front pod',(0,.434,.542),(.688,.221,.410),p,'21','chassis',.044)
 B.box('Eco broad ivory bonnet',(0,.555,.463),(.604,.035,.333),a,'21','chassis',.014)
 for side in [-1,1]:
  B.box('Eco continuous battery side',(side*.390,.380,-.080),(.157,.218,.639),p,'21','chassis',.030)
  B.box('Eco side battery socket',(side*.474,.386,-.100),(.018,.109,.210),teal,'22','chassis',.017)
  for z in [-.161,-.104,-.047]:B.box('Eco battery energy tick',(side*.486,.386,z),(.008,.061,.032),cyan,'26','chassis',.005)
  for z in [.48,-.56]:B.box('Eco ivory wheel brow',(side*.515,.464,z),(.290,.061,.373),a,'21','chassis',.023)
  B.box('Eco front corner LED',(side*.252,.436,.756),(.060,.102,.020),cyan,'26','chassis',.012)
  B.box('Eco integrated rear corner',(side*.257,.406,-.702),(.161,.145,.123),a,'21','chassis',.024)
  B.box('Eco rear vertical light',(side*.258,.415,-.772),(.034,.074,.018),'E9929F','26','chassis',.007)
 B.box('Eco front continuous LED',(0,.469,.757),(.357,.032,.018),cyan,'26','chassis',.008)
 B.box('Eco integrated front bumper',(0,.290,.754),(.639,.084,.086),a,'21','chassis',.026)
 B.box('Eco flat clean rear deck',(0,.480,-.621),(.649,.080,.238),a,'21','chassis',.027)
 B.box('Eco rear charge socket',(0,.380,-.752),(.130,.070,.027),teal,'22','chassis',.013)
 leaf_badge(B,'Eco original two tone leaf',(0,.577,.459),'55A784',size=.105)
 for side,x in [('l',-.59),('r',.59)]:
  sign=-1 if x<0 else 1
  for end,z in [('f',.48),('r',-.56)]:
   g='wheel_'+end+side+'_spin'
   B.cylinder('Eco flush hub cover',(x+sign*.137,.205,z),.105,.008,a,'22',g,sides=16 if B.high else 8)
   for i in range(3):
    t=i*math.tau/3
    B.beam('Eco radial teal hub mark',(x+sign*.144,.205+.039*math.cos(t),z+.039*math.sin(t)),(x+sign*.144,.205+.085*math.cos(t),z+.085*math.sin(t)),.018,.012,teal,'23',g,.003)

def pickup(B,c):
 p=c['paint'];a=c['accent'];dark='293E4A';orange='D78C56'
 B.loft('Trail raised square truck hood',[(.18,.305,.31,.580,.028),(.43,.354,.28,.568,.028),(.726,.349,.275,.505,.026)],p)
 B.box('Trail deep radiator surround',(0,.393,.739),(.724,.225,.052),dark,'22','chassis',.022)
 B.box('Trail broad truck grille',(0,.392,.773),(.427,.141,.019),STEEL,'23','chassis',.010)
 for x in [-.158,-.079,0,.079,.158]:B.box('Trail dark radiator slot',(x,.392,.786),(.035,.103,.011),dark,'22','chassis',.005)
 # Clearly open bed: inner floor, side walls and tailgate, not a covered hatch.
 B.box('Trail open bed floor',(0,.394,-.625),(.738,.057,.343),dark,'22','chassis',.011)
 B.box('Trail pickup tailgate',(0,.506,-.790),(.776,.205,.042),p,'21','chassis',.018)
 B.box('Trail tailgate stamped panel',(0,.520,-.815),(.420,.079,.010),dark,'22','chassis',.012)
 B.box('Trail tailgate latch',(0,.553,-.825),(.096,.019,.009),STEEL,'23','chassis',.004)
 for side in [-1,1]:
  B.box('Trail deep bed wall',(side*.368,.512,-.624),(.044,.220,.345),p,'21','chassis',.016)
  B.box('Trail grey bed top rail',(side*.368,.630,-.624),(.061,.022,.348),STEEL,'23','chassis',.007)
  for z in [.48,-.56]:
   B.box('Trail chunky dark mudguard',(side*.521,.470,z),(.319,.073,.432),dark,'22','chassis',.020)
   B.box('Trail ivory fender flare',(side*.556,.490,z),(.260,.024,.380),a,'21','chassis',.009)
  B.box('Trail truck headlamp',(side*.281,.442,.780),(.119,.107,.029),'FFF0C8','26','chassis',.014)
  B.box('Trail tall rear light',(side*.302,.523,-.821),(.058,.104,.018),'F18773','26','chassis',.010)
  B.box('Trail middle cab rocker',(side*.388,.388,-.073),(.137,.169,.554),p,'21','chassis',.018)
  B.box('Trail running board',(side*.461,.296,-.067),(.107,.048,.425),STEEL,'23','chassis',.010)
  B.tube('Trail bed mounted adventure hoop',[(side*.266,.438,-.635),(side*.266,.954,-.635),(side*.207,1.010,-.635)],.022,dark,'22')
 B.tube('Trail adventure hoop header',[(-.207,1.010,-.635),(.207,1.010,-.635)],.022,dark,'22')
 B.box('Trail small roof accessory',(0,1.031,-.635),(.229,.057,.111),orange,'21','chassis',.012)
 B.box('Trail strong front bumper',(0,.251,.813),(.948,.113,.103),STEEL,'23','chassis',.021)
 B.box('Trail rear protective bumper',(0,.260,-.829),(.868,.078,.083),dark,'22','chassis',.018)
 B.box('Trail hood cream badge',(0,.557,.486),(.115,.012,.090),a,'21','chassis',.010)
 B.box('Trail small right bed equipment case',(.165,.464,-.629),(.184,.098,.166),orange,'22','chassis',.013)
 B.box('Trail case latch',(.165,.519,-.629),(.034,.014,.070),STEEL,'23','chassis',.004)

report=[]
for c in CHARACTERS:
 row={'id':c['id'],'name':c['name'],'vehicle':c['vehicle'],'models':{}}
 for high in [True,False]:
  B=Builder(c['root'],high);cockpit(B,c);common_details(B,c)
  {'panda':bamboo,'koala':ecopod,'raccoon':pickup}[c['animal']](B,c)
  wheels(B,dict(c,animal='mouse' if c['animal']=='koala' else 'bear'))
  body(B,c);{'panda':panda,'koala':koala,'raccoon':raccoon}[c['animal']](B,c)
  file='kart_'+c['id']+('' if high else '_low')+'.glb'
  row['models']['high' if high else 'low']=B.export(OUT/'models'/file,{'animal':c['animal'],'vehicle':c['vehicle'],'identityReference':'avatar_'+c['id']+'.webp','style':'blocky chibi','version':'Batch 4 final'})
  if high:B.save_source(HERE/('race-quest-'+c['id']+'.blend'))
 report.append(row)
(OUT/'build-metrics.json').write_text(json.dumps(report,indent=2))
