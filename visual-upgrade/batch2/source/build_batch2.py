"""Four original blocky racers. Shared Batch 1 factory, cockpit and wheel functions.
blender -b --python-exit-code 1 --python visual-upgrade/batch2/source/build_batch2.py
Only Batch 2 outputs are written. AST imports selected functions, never Batch 1's build loop.
"""
import pathlib,sys,math,json,ast
HERE=pathlib.Path(__file__).resolve().parent;OUT=HERE.parent;SHARED=HERE.parents[1]/'batch1/source'
sys.path.insert(0,str(SHARED));sys.dont_write_bytecode=True
from blocky_factory import Builder
INK='172331';TRIM='203649';WHITE='F5F2DE';STEEL='AABBCB';PINK='ED95B0'
_tree=ast.parse((SHARED/'build_batch1.py').read_text())
exec(compile(ast.Module(body=[n for n in _tree.body if isinstance(n,ast.FunctionDef) and n.name in ['cockpit','wheels']],type_ignores=[]),str(SHARED/'build_batch1.py'),'exec'))
CHARACTERS=[
 dict(id='bebek',name='Bebek',animal='duck',vehicle='Amfibi',root='race_quest_duck',paint='25B5C7',accent='FFD15A',fur='FFCD4A',cream='FFE694'),
 dict(id='ayam',name='Ayam',animal='chicken',vehicle='Farm Buggy',root='race_quest_chicken',paint='65A65A',accent='F6D187',fur='FFF2DA',cream='FFE5B8'),
 dict(id='domba',name='Domba',animal='sheep',vehicle='Cloud Cruiser',root='race_quest_sheep',paint='A7CDEB',accent='C6ABE7',fur='FFF1DA',cream='9E8F9B'),
 dict(id='robot',name='Robot',animal='robot',vehicle='Photon',root='race_quest_robot',paint='D6E5F1',accent='46DCE9',fur='D8E6F1',cream='344A64')]

def eyes_and_smiles(B,c,x,y,z,my,mz,mw=.09,mh=.061):
 robot=c['animal']=='robot';eye='56E6EF' if robot else INK
 for side in [-1,1]:
  B.box('Readable square eye',(side*x,y,z),(.064 if not robot else .070,.105,.016),eye,'24' if not robot else '26','eyes',.009)
  if not robot:B.box('Tiny square highlight',(side*x-.009,y+.027,z+.011),(.022,.028,.005),'FFF9EA','24','eyes',.003)
  for a,b in [((side*x-.031,y,z),(side*x,y+.029,z)),((side*x,y+.029,z),(side*x+.031,y,z))]:B.beam('Happy pixel eye',a,b,.014,.014,eye,'24' if not robot else '26','eyes_happy',.003)
 for group,s in [('mouth_normal',.78),('mouth_happy',1.20)]:
  w=mw*s;h=mh*s
  outline=[(-w/2,my+h*.42),(0,my+h*.27),(w/2,my+h*.42),(w*.43,my-h*.22),(w*.20,my-h*.49),(-w*.20,my-h*.49),(-w*.43,my-h*.22)]
  B.prism('Friendly toy smile',outline,mz,mz+.007,eye,'24' if not robot else '26',group,.003)
  if not robot:B.box('Little pink tongue',(0,my-h*.23,mz+.009),(w*.48,h*.28,.004),PINK,group=group,bevel=.003)
 B.box('Surprised pixel mouth',(0,my,mz+.004),(mw*.62,mh*1.2,.010),eye,'24' if not robot else '26','mouth_shock',.012)

def bird(B,c):
 duck=c['animal']=='duck';fur=c['fur'];beak='F3A32C' if duck else 'FFC052';red='DF5260'
 if duck:
  B.box('Broad duck cube head',(0,1.245,-.095),(.625,.536,.467),fur,bevel=.051)
  B.box('Short duck beak upper',(0,1.177,.194),(.214,.066,.130),beak,bevel=.017)
  B.box('Short duck beak lower',(0,1.133,.190),(.184,.031,.109),'E58B2B',bevel=.009)
  body=(.36,.408,.34);eyeX=.159;eyeZ=.147
 else:
  B.prism('Chicken cube jaw',[(-.265,.989),(-.306,1.060),(-.306,1.435),(-.254,1.495),(.254,1.495),(.306,1.435),(.306,1.060),(.265,.989)],-.325,.137,fur,bevel=.037)
  B.prism('Small wedge chicken beak',[(-.094,1.195),(0,1.231),(.094,1.195),(.070,1.148),(-.070,1.148)],.140,.245,beak,bevel=.009)
  B.box('Small chicken wattle',(0,1.080,.150),(.054,.108,.031),red,bevel=.018)
  for i,(y,z) in enumerate([(1.531,.01),(1.607,-.08),(1.557,-.19)]):B.box('Three block red comb '+str(i),(0,y,z),(.102,.173,.120),red,group='ear_l',bevel=.017)
  body=(.335,.401,.33);eyeX=.151;eyeZ=.148
 B.box('Short bird body',(0,.745,-.23),body,fur,bevel=.037)
 B.box('Warm belly bib',(0,.755,-.054),(.230,.264,.017),c['cream'],bevel=.025)
 B.box('Short bird neck',(0,.963,-.17),(.185,.107,.18),fur,bevel=.018)
 for side,label in [(-1,'l'),(1,'r')]:
  B.beam('Folded block wing',(side*.156,.863,-.162),(side*.228,.785,.014),.139,.098,fur,bevel=.022)
  B.beam('Wing wrist',(side*.228,.785,.014),(side*.181,.840,.214),.107,.096,fur,bevel=.020)
  B.box('Wing mitten on wheel',(side*.181,.840,.234),(.125,.126,.115),fur,bevel=.021)
  B.box('Wing inner grip',(side*.145,.813,.208),(.051,.057,.063),fur,bevel=.012)
  B.box('Seated short bird thigh',(side*.105,.595,-.032),(.147,.140,.25),fur,bevel=.020)
  B.box('Webbed orange foot',(side*.108,.565,.110),(.153,.103,.175),'EFA13B',bevel=.015)
  B.box('Graphic pink cheek',(side*.230,1.187,.142),(.060,.035,.008),'F5AA86' if duck else 'F2A6A6',bevel=.008)
  if not duck:
   for i in range(2):B.box('Graphic folded feather',(side*.242,.809-i*.035,-.007),(.012,.018,.103),'EAD5B3',bevel=.005)
 B.beam('Offset tail root',(-.14,.724,-.33),(-.23,.73,-.33),.07,.07,fur,group='tail',bevel=.012)
 if duck:B.prism('Duck upward square tail',[(-.28,.70),(-.20,.71),(-.20,.79),(-.30,.82)],-.38,-.29,fur,group='tail',bevel=.012)
 else:
  for i in range(2):
   o=B.box('Block chicken tail plume',(-.24-i*.028,.76+i*.045,-.32),(.07,.15,.085),c['cream'],group='tail',bevel=.015);o.rotation_euler.z=-.30
 eyes_and_smiles(B,c,eyeX,1.301,eyeZ,1.142 if duck else 1.182,.263 if duck else .254,.110 if duck else .094,.042 if duck else .036)

def sheep(B,c):
 wool=c['fur'];face=c['cream']
 B.box('Squat wool body',(0,.751,-.23),(.368,.42,.35),wool,bevel=.048)
 B.box('Dark short sheep neck',(0,.968,-.18),(.18,.12,.17),face,bevel=.020)
 B.box('Square soft sheep face',(0,1.236,-.080),(.472,.425,.424),face,bevel=.050)
 # Sparse, arranged cube fleece: a crown and side border, not a sphere pile.
 for x,y,z,s in [(-.245,1.403,-.12,.182),(0,1.478,-.12,.215),(.245,1.403,-.12,.182),(-.135,1.486,-.12,.185),(.135,1.486,-.12,.185),(-.265,1.215,-.16,.148),(.265,1.215,-.16,.148),(-.17,1.351,-.30,.18),(.17,1.351,-.30,.18)]:
  B.box('Ordered cube fleece',(x,y,z),(s,s,.20),wool,bevel=.045)
 for side in [-1,1]:
  B.box('Lower wool cheek border',(side*.247,1.065,-.130),(.135,.147,.199),wool,bevel=.036)
  for y,z in [(.865,-.255),(.710,-.255),(.629,-.22)]:B.box('Sparse flank wool block',(side*.169,y,z),(.102,.145,.215),wool,bevel=.032)
 for side,label in [(-1,'l'),(1,'r')]:
  o=B.box('Small floppy sheep ear',(side*.304,1.283,-.051),(.183,.101,.120),face,group='ear_'+label,bevel=.029);o.rotation_euler.z=-side*.24
  o=B.box('Pink inset sheep ear',(side*.313,1.286,.015),(.106,.051,.009),'DDB1B4',group='ear_'+label,bevel=.014);o.rotation_euler.z=-side*.24
  B.beam('Wool shoulder',(side*.154,.868,-.16),(side*.23,.790,.015),.145,.128,wool,bevel=.032)
  B.beam('Short sheep foreleg',(side*.23,.790,.015),(side*.181,.840,.214),.111,.110,face,bevel=.023)
  B.box('Soft hoof steering grip',(side*.181,.840,.234),(.125,.126,.115),'756979',bevel=.025)
  B.box('Hoof inner grip',(side*.145,.813,.208),(.051,.057,.063),'756979',bevel=.012)
  B.box('Seated wool thigh',(side*.105,.595,-.032),(.147,.140,.25),wool,bevel=.025)
  B.box('Short sheep hoof',(side*.108,.565,.105),(.153,.103,.155),'756979',bevel=.018)
 B.box('Tiny square sheep nose',(0,1.186,.139),(.056,.034,.025),'665767',bevel=.010)
 B.box('Sparse side fleece tail',(-.251,.729,-.325),(.146,.134,.101),wool,group='tail',bevel=.037)
 eyes_and_smiles(B,c,.129,1.289,.141,1.133,.142,.090,.060)

def robot(B,c):
 p=c['fur'];dark=c['cream'];cyan=c['accent']
 B.box('Robot helmet cube',(0,1.255,-.105),(.584,.493,.443),p,'21',bevel=.044)
 B.box('Inset dark digital face',(0,1.251,.124),(.480,.349,.026),dark,'22',bevel=.038)
 B.box('Short robot neck',(0,.983,-.18),(.134,.115,.134),dark,'23',bevel=.012)
 B.box('Robot compact torso',(0,.748,-.23),(.325,.412,.34),p,'21',bevel=.029)
 B.box('Inset chest socket',(0,.780,-.052),(.210,.151,.019),dark,'22',bevel=.014)
 B.box('Cyan battery badge',(0,.780,-.039),(.137,.086,.011),cyan,'26',bevel=.010)
 B.box('Short antenna stem',(0,1.548,-.12),(.038,.130,.038),dark,'23','ear_l',.007)
 B.box('Antenna beacon',(0,1.628,-.12),(.107,.101,.087),cyan,'26','ear_l',.018)
 for side,label in [(-1,'l'),(1,'r')]:
  B.box('Square headphone',(side*.307,1.269,-.090),(.074,.182,.199),cyan,'21','ear_'+label,.020)
  B.box('Headphone inset',(side*.350,1.269,-.090),(.013,.100,.113),dark,'22','ear_'+label,.015)
  B.beam('Mechanical upper arm',(side*.155,.875,-.17),(side*.231,.790,.015),.122,.112,p,'21',bevel=.018)
  B.box('Square elbow joint',(side*.23,.79,.015),(.119,.102,.098),dark,'23',bevel=.016)
  B.beam('Short mechanical wrist',(side*.231,.790,.015),(side*.181,.840,.214),.096,.095,p,'21',bevel=.016)
  B.box('Robot mitten wheel grip',(side*.181,.840,.234),(.125,.126,.115),dark,bevel=.019)
  B.box('Robot inner thumb',(side*.145,.813,.208),(.051,.057,.063),dark,bevel=.010)
  B.box('Seated robot thigh',(side*.105,.595,-.032),(.147,.140,.25),p,'21',bevel=.017)
  B.box('Robot short boot',(side*.108,.565,.105),(.153,.103,.155),dark,'22',bevel=.016)
  B.box('Cyan boot sole',(side*.108,.529,.105),(.151,.025,.149),cyan,'26',bevel=.006)
 eyes_and_smiles(B,c,.127,1.294,.148,1.178,.148,.093,.060)

def amphibian(B,c):
 p=c['paint'];a=c['accent']
 B.loft('Faceted boat hull',[(-.81,.19,.25,.38,.035),(-.66,.36,.18,.46,.045),(-.35,.43,.18,.46,.055),(.25,.43,.19,.46,.055),(.60,.32,.24,.45,.045),(.86,.08,.32,.40,.025)],'247892')
 B.loft('Raised boat bow',[(.19,.32,.35,.570,.035),(.41,.38,.32,.555,.045),(.67,.27,.33,.50,.04),(.87,.07,.35,.43,.015)],p)
 for side in [-1,1]:
  # Pontoon hulls are outside the cockpit, not wheel shrouds copied from Kapsul.
  B.box('Sealed side pontoon',(side*.408,.368,-.065),(.177,.203,.640),p,'21','chassis',.045)
  B.box('Yellow flotation belt',(side*.503,.395,-.065),(.020,.064,.500),a,'21','chassis',.010)
  for z in [.48,-.56]:
   B.box('Amphibian wheel arch',(side*.530,.457,z),(.278,.048,.360),'247892','21','chassis',.016)
  B.box('Boat bow amber headlamp',(side*.163,.452,.716),(.106,.058,.050),'FFF1BE','26','chassis',.016)
  B.box('Boat transom rear lamp',(side*.230,.410,-.724),(.108,.040,.030),'F47468','26','chassis',.010)
  B.tube('Boat cockpit yellow edging',[(side*.285,.485,.16),(side*.315,.520,-.15),(side*.29,.520,-.51)],.022,a,'21')
  B.box('Deck anti slip strip',(side*.23,.565,.290),(.045,.011,.132),'267E91','22','chassis',.005)
 B.box('Boat nose rubbing rail',(0,.306,.797),(.58,.060,.108),a,'21','chassis',.020)
 B.box('Amphibian transom',(0,.40,-.688),(.670,.146,.133),p,'21','chassis',.023)
 B.cylinder('Decorative rear impeller housing',(0,.315,-.796),.105,.052,TRIM,'22','chassis',axis='Z')
 B.cylinder('Impeller alloy inset',(0,.315,-.826),.073,.008,STEEL,'23','chassis',axis='Z')
 for side in [-1,1]:B.beam('Impeller diagonal grille',(side*.047,.268,-.834),(-side*.047,.362,-.834),.013,.010,TRIM,'22','chassis',.003)
 B.box('Bow cream centre mark',(0,.510,.574),(.055,.010,.125),WHITE,'21','chassis',.005)

def farm(B,c):
 p=c['paint'];a=c['accent'];wood='B98C5D'
 B.loft('Short tractor hood',[(.20,.275,.29,.573,.025),(.48,.310,.27,.550,.025),(.70,.310,.26,.490,.025)],p)
 B.box('Cream tractor radiator surround',(0,.383,.722),(.643,.244,.058),a,'21','chassis',.027)
 B.box('Dark tractor radiator grille',(0,.382,.758),(.364,.150,.016),TRIM,'22','chassis',.010)
 for x in [-.135,-.0675,0,.0675,.135]:B.box('Vertical radiator bar',(x,.382,.771),(.016,.128,.009),STEEL,'23','chassis',.003)
 B.box('Farm squared front bumper',(0,.230,.810),(.875,.092,.101),TRIM,'22','chassis',.019)
 # Small functional-looking open utility bed makes this unlike the Bear's racer.
 B.box('Pickup flatbed floor',(0,.401,-.619),(.74,.076,.294),wood,'22','chassis',.014)
 B.box('Green tailgate',(0,.518,-.772),(.77,.198,.042),p,'21','chassis',.019)
 for side in [-1,1]:
  B.box('Timber cargo bed side',(side*.365,.511,-.615),(.035,.167,.285),wood,'22','chassis',.009)
  for z in [-.71,-.52]:B.box('Cream bed bracket',(side*.387,.514,z),(.012,.147,.020),a,'23','chassis',.004)
  B.box('Large rear mudguard',(side*.526,.486,-.56),(.320,.071,.445),p,'21','chassis',.020)
  B.box('Cream front mudguard',(side*.532,.455,.48),(.303,.050,.400),a,'21','chassis',.018)
  B.box('Tractor square headlight',(side*.254,.422,.768),(.109,.103,.041),'FFF0BC','26','chassis',.016)
  B.box('Farm tail light',(side*.282,.522,-.800),(.095,.058,.020),'F57E68','26','chassis',.011)
  B.tube('Farm tall rollbar',[(side*.333,.490,-.480),(side*.333,1.095,-.480),(side*.245,1.160,-.480)],.023,TRIM,'22')
  B.box('Farm running step',(side*.465,.288,-.05),(.105,.050,.310),STEEL,'23','chassis',.011)
 B.tube('Farm rollbar top',[(-.245,1.16,-.48),(.245,1.16,-.48)],.023,TRIM,'22')
 B.box('Farm cream roof brow',(0,1.171,-.48),(.73,.036,.180),a,'21','chassis',.013)
 B.tube('Small farm exhaust stack',[(.239,.555,.270),(.239,.782,.270),(.239,.807,.220)],.019,TRIM,'22')
 B.box('Green raised bonnet stripe',(0,.554,.459),(.081,.012,.180),a,'21','chassis',.005)

def cloud(B,c):
 p=c['paint'];a=c['accent']
 B.loft('Cloud short rounded tub',[(-.79,.17,.28,.38,.035),(-.62,.36,.22,.49,.045),(-.20,.415,.22,.50,.050),(.35,.415,.23,.49,.050),(.69,.30,.28,.43,.04),(.82,.13,.30,.38,.025)],p)
 B.loft('Cloud broad cushion nose',[(.20,.31,.34,.562,.045),(.46,.37,.32,.540,.045),(.70,.29,.30,.463,.04),(.80,.18,.31,.425,.025)],'DDEBEA')
 for side in [-1,1]:
  # Each side has one authored stepped cloud profile, not dozens of ornaments.
  outline=[(-.73,.32),(-.73,.43),(-.64,.43),(-.64,.48),(-.50,.48),(-.50,.53),(-.32,.53),(-.32,.48),(-.15,.48),(-.15,.43),(-.02,.43),(-.02,.32)]
  # profile is in Z/Y; map the prism to X thickness through a custom solid.
  v=[(side*x,y,z) for x in [.402,.453] for z,y in outline];n=len(outline);f=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
  B.mesh('Stepped cloud side relief',v,f,'F6EDDE','21','chassis',.014)
  for z in [.48,-.56]:B.box('Lavender cloud fender',(side*.521,.462,z),(.289,.059,.387),a,'21','chassis',.023)
  B.box('Cloud lamp surround',(side*.235,.414,.709),(.163,.132,.059),a,'21','chassis',.029)
  B.box('Cream square round headlight',(side*.235,.417,.745),(.111,.084,.023),'FFF2CF','26','chassis',.021)
  B.box('Cloud pink rear light',(side*.239,.420,-.731),(.135,.050,.029),'F49CAA','26','chassis',.013)
  B.box('Cloud decorative tiny wing',(side*.410,.559,-.481),(.207,.037,.216),'DDEBEA','21','chassis',.014)
  B.tube('Cloud cockpit piping',[(side*.280,.493,.18),(side*.31,.535,-.08),(side*.29,.542,-.46)],.024,a,'21')
 B.box('Cloud soft bumper',(0,.272,.780),(.688,.082,.112),a,'21','chassis',.028)
 B.box('Cloud rear cushion deck',(0,.461,-.643),(.622,.137,.201),'DDEBEA','21','chassis',.029)
 B.box('Cloud hood lavender badge',(0,.538,.479),(.109,.010,.092),a,'21','chassis',.014)

def photon(B,c):
 p=c['paint'];a=c['accent'];blue='3D83D9'
 B.loft('Photon dark continuous undertray',[(-.81,.29,.20,.29,.024),(-.55,.43,.19,.29,.026),(.44,.43,.19,.28,.026),(.82,.24,.21,.27,.021)],TRIM,'22')
 B.loft('Photon split wedge central bonnet',[(.19,.24,.30,.539,.024),(.43,.31,.26,.485,.027),(.68,.28,.23,.371,.023),(.83,.18,.23,.309,.018)],p)
 B.loft('Photon compact power bay',[(-.80,.23,.29,.43,.025),(-.63,.34,.29,.53,.030),(-.46,.29,.29,.51,.028)],blue)
 for side in [-1,1]:
  B.box('Photon angular side battery',(side*.367,.351,-.065),(.170,.170,.608),blue,'21','chassis',.018)
  B.box('Cyan side energy rail',(side*.458,.354,-.065),(.011,.035,.446),a,'26','chassis',.006)
  B.box('Photon side intake',(side*.367,.364,.248),(.116,.090,.016),TRIM,'22','chassis',.012)
  for z in [.48,-.56]:B.box('Photon bevel armour fender',(side*.519,.452,z),(.289,.045,.330),p,'21','chassis',.011)
  B.box('Photon forward twin energy pod',(side*.338,.350,.493),(.132,.158,.426),blue,'21','chassis',.019)
  B.box('Photon pod ivory armour',(side*.338,.434,.493),(.131,.026,.330),p,'21','chassis',.010)
  B.box('Photon pod cyan eye',(side*.338,.352,.712),(.082,.068,.014),a,'26','chassis',.009)
  B.box('Photon front vertical light',(side*.303,.313,.746),(.042,.114,.031),a,'26','chassis',.008)
  B.box('Photon rear energy light',(side*.244,.385,-.789),(.128,.026,.012),'FF7B9B','26','chassis',.006)
  B.beam('Photon buttress', (side*.269,.48,-.52),(side*.300,.671,-.721),.040,.044,p,'21','chassis',.008)
  B.box('Photon rear spoiler endplate',(side*.419,.646,-.728),(.026,.113,.180),blue,'21','chassis',.009)
  B.box('Photon cockpit sill',(side*.275,.501,-.117),(.037,.058,.586),p,'21','chassis',.013)
 B.box('Photon layered front splitter',(0,.214,.795),(.690,.033,.077),TRIM,'22','chassis',.009)
 B.box('Photon cyan front bar',(0,.238,.823),(.602,.019,.020),a,'26','chassis',.004)
 B.box('Photon geometric rear spoiler',(0,.664,-.729),(.861,.035,.178),p,'21','chassis',.011)
 B.box('Photon cyan spoiler inset',(0,.686,-.729),(.547,.010,.125),a,'26','chassis',.005)
 rows=[(.21,.539),(.43,.487),(.68,.373),(.81,.323)];v=[(x,y+.002,z) for z,y in rows for x in [-.027,.027]]
 B.mesh('Photon bonnet cyan energy seam',v,[(i,i+1,i+3,i+2) for i in range(0,len(v)-2,2)],a,'26','chassis')

report=[]
for c in CHARACTERS:
 row={'id':c['id'],'name':c['name'],'vehicle':c['vehicle'],'models':{}}
 for high in [True,False]:
  B=Builder(c['root'],high);cockpit(B,c)
  {'duck':amphibian,'chicken':farm,'sheep':cloud,'robot':photon}[c['animal']](B,c)
  wc=dict(c,animal='bear' if c['id']=='ayam' else 'rabbit' if c['id']=='robot' else c['animal']);wheels(B,wc)
  {'duck':bird,'chicken':bird,'sheep':sheep,'robot':robot}[c['animal']](B,c)
  file='kart_'+c['id']+('' if high else '_low')+'.glb'
  row['models']['high' if high else 'low']=B.export(OUT/'models'/file,{'animal':c['animal'],'vehicle':c['vehicle'],'identityReference':'avatar_'+c['id']+'.webp','style':'blocky chibi','version':'Batch 2'})
  if high:B.save_source(HERE/('race-quest-'+c['id']+'.blend'))
 report.append(row)
(OUT/'build-metrics.json').write_text(json.dumps(report,indent=2))
