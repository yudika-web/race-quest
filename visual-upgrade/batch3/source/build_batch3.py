"""Batch 3 original blocky designs, shared tested Blender factory/contact rig.
blender -b --python-exit-code 1 --python visual-upgrade/batch3/source/build_batch3.py
Only Batch 3 outputs are written. AST imports definitions without old build loops.
"""
import pathlib,sys,math,json,ast
HERE=pathlib.Path(__file__).resolve().parent;OUT=HERE.parent;SHARED=HERE.parents[1]
sys.path.insert(0,str(SHARED/'batch1/source'));sys.dont_write_bytecode=True
from blocky_factory import Builder
INK='172331';TRIM='203649';WHITE='F5F2DE';STEEL='AABBCB';PINK='ED95B0'
for source,names in [('batch1/source/build_batch1.py',['cockpit','wheels']),('batch2/source/build_batch2.py',['eyes_and_smiles'])]:
 tree=ast.parse((SHARED/source).read_text());exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(SHARED/source),'exec'))
CHARACTERS=[
 dict(id='anjing',name='Anjing',animal='dog',vehicle='Rally',root='race_quest_dog',paint='3D6FA3',accent='F1D398',fur='DDA368',cream='FFE5B9'),
 dict(id='tikus',name='Tikus',animal='mouse',vehicle='Mini Roadster',root='race_quest_mouse',paint='79C9C1',accent='F5B1A0',fur='A7A5BD',cream='DCD4E0'),
 dict(id='rubah',name='Rubah',animal='fox',vehicle='GT',root='race_quest_fox',paint='E86C40',accent='F5E3C5',fur='F3A04C',cream='FFF0CE')]

def seated_body(B,c):
 animal=c['animal'];fur=c['fur'];cream=c['cream'];mouse=animal=='mouse'
 B.box('Short species torso',(0,.744,-.23),(.286 if mouse else .335,.418,.325 if mouse else .34),fur,bevel=.031)
 B.box('Graphic cream belly',(0,.756,-.058),(.203 if mouse else .235,.265,.022),cream,bevel=.021)
 B.box('Short chibi neck',(0,.965,-.18),(.155 if mouse else .18,.113,.17),fur,bevel=.018)
 if animal=='dog':
  B.box('Red toy collar',(0,.967,-.18),(.202,.055,.205),'D96657',bevel=.013)
  B.box('Square brass collar tag',(0,.935,-.066),(.047,.050,.012),'F2BF64','23',bevel=.009)
 for side,label in [(-1,'l'),(1,'r')]:
  width=.111 if mouse else .132
  B.beam('Short upper foreleg',(side*.155,.875,-.17),(side*.231,.790,.015),width,.113,fur,bevel=.021)
  B.beam('Bent foreleg wrist',(side*.231,.790,.015),(side*.181,.840,.214),.105,.107,fur,bevel=.020)
  B.box('Cream mitten '+label,(side*.181,.840,.234),(.125,.126,.115),cream,bevel=.022)
  B.box('Inner wheel thumb '+label,(side*.145,.813,.208),(.051,.057,.063),cream,bevel=.013)
  B.box('Seated thigh',(side*.105,.595,-.032),(.147,.140,.25),fur,bevel=.021)
  B.box('Short chibi paw',(side*.108,.565,.105),(.153,.103,.155),PINK if mouse else cream,bevel=.017)
  if not mouse:
   for x in [-.021,.021]:B.box('Two graphic toe marks',(side*.108+x,.568,.185),(.006,.029,.004),'C89C6A',bevel=.001)

def dog(B,c):
 fur=c['fur'];cream=c['cream'];dark='A16A4E'
 B.prism('Dog broad cube jaw',[(-.269,1.005),(-.315,1.070),(-.315,1.450),(-.267,1.496),(.267,1.496),(.315,1.450),(.315,1.070),(.269,1.005)],-.328,.142,fur,bevel=.039)
 B.prism('Graphic forehead blaze',[(-.083,1.472),(.083,1.472),(.062,1.266),(.098,1.192),(-.098,1.192),(-.062,1.266)],.143,.150,cream,bevel=.007)
 B.box('Short cream square muzzle',(0,1.135,.176),(.257,.169,.063),cream,bevel=.033)
 B.box('Little black dog nose',(0,1.181,.218),(.078,.049,.027),INK,bevel=.013)
 for side,label in [(-1,'l'),(1,'r')]:
  B.pivots['ear_'+label]=('driver_pose',(side*.278,.767,.014))
  o=B.box('Hanging block dog ear',(side*.319,1.342,-.081),(.145,.315,.181),dark,group='ear_'+label,bevel=.026);o.rotation_euler.z=side*.20
  o=B.box('Warm dog ear inset',(side*.324,1.331,.017),(.080,.205,.009),'C58A63',group='ear_'+label,bevel=.014);o.rotation_euler.z=side*.20
  B.box('Small dog cheek freckle',(side*.101,1.146,.212),(.014,.012,.004),dark,bevel=.003)
 eyes_and_smiles(B,c,.161,1.296,.154,1.109,.215,.095,.068)
 B.tube('Short bent dog tail',[(-.145,.729,-.32),(-.259,.756,-.33),(-.295,.830,-.36),(-.272,.891,-.39)],.046,fur,'24','tail',6)
 B.box('Cream dog tail tip',(-.272,.891,-.39),(.076,.079,.075),cream,group='tail',bevel=.019)

def mouse(B,c):
 fur=c['fur'];cream=c['cream']
 B.prism('Small mouse cube cheeks',[(-.191,.994),(-.253,1.074),(-.253,1.387),(-.211,1.434),(.211,1.434),(.253,1.387),(.253,1.074),(.191,.994)],-.284,.118,fur,bevel=.034)
 for side,label in [(-1,'l'),(1,'r')]:
  B.pivots['ear_'+label]=('driver_pose',(side*.214,.767,.048))
  B.box('Oversized round square mouse ear',(side*.228,1.507,-.117),(.264,.287,.139),fur,group='ear_'+label,bevel=.061)
  B.box('Pink round square ear inset',(side*.228,1.511,-.040),(.181,.199,.016),'E9ACBC',group='ear_'+label,bevel=.040)
  B.box('Soft graphic mouse cheek',(side*.163,1.128,.124),(.101,.066,.012),cream,bevel=.017)
  for i in [-1,1]:B.beam('Short graphic whisker',(side*.193,1.149+i*.033,.137),(side*.270,1.149+i*.043,.137),.010,.009,'EEE4DE',bevel=.002)
 B.box('Tiny pink mouse nose',(0,1.181,.139),(.051,.038,.025),PINK,bevel=.011)
 eyes_and_smiles(B,c,.119,1.283,.129,1.123,.129,.077,.055)
 B.pivots['tail']=('driver_pose',(-.26,.08,-.16))
 B.tube('Long block curved mouse tail',[(-.14,.724,-.33),(-.268,.756,-.33),(-.341,.815,-.408),(-.360,.859,-.543),(-.305,.899,-.614)],.024,'E7ACB9','24','tail',4)
 B.box('Mouse tail tiny tip',(-.305,.899,-.614),(.047,.047,.047),PINK,group='tail',bevel=.008)

def fox(B,c):
 fur=c['fur'];cream=c['cream'];dark='794D3C'
 B.prism('Fox tapered cube jaw',[(-.202,1.001),(-.324,1.104),(-.324,1.443),(-.280,1.490),(.280,1.490),(.324,1.443),(.324,1.104),(.202,1.001)],-.328,.141,fur,bevel=.032)
 outline=[(-.182,1.015),(-.263,1.068),(-.296,1.172),(-.213,1.184),(-.112,1.126),(0,1.163),(.112,1.126),(.213,1.184),(.296,1.172),(.263,1.068),(.182,1.015)]
 B.prism('One graphic cream fox cheek bib',outline,.143,.158,cream,bevel=.010)
 B.box('Small fox muzzle',(0,1.144,.173),(.133,.093,.039),cream,bevel=.019)
 B.box('Fox black triangular button nose',(0,1.184,.201),(.063,.037,.026),INK,bevel=.010)
 for side,label in [(-1,'l'),(1,'r')]:
  x=side*.236
  B.prism('Thick triangular fox ear',[(x-side*.101,1.450),(x-side*.080,1.709),(x-side*.022,1.754),(x+side*.111,1.474)],-.239,-.094,fur,group='ear_'+label,bevel=.016)
  B.prism('Dark inner fox ear',[(x-side*.064,1.490),(x-side*.052,1.681),(x-side*.026,1.697),(x+side*.067,1.496)],-.092,-.082,dark,group='ear_'+label,bevel=.010)
  B.box('Fox confident brow',(side*.154,1.370,.151),(.081,.013,.008),dark,bevel=.004)
 eyes_and_smiles(B,c,.155,1.302,.153,1.091,.169,.093,.063)
 # Tail runs OUTSIDE the left seat bolster, above the rear deck, before spoiler.
 B.pivots['tail']=('driver_pose',(-.26,.08,-.15))
 B.beam('Fox tail root',(-.14,.733,-.315),(-.29,.776,-.350),.097,.102,fur,group='tail',bevel=.021)
 B.beam('Large rising block fox tail',(-.302,.793,-.365),(-.359,.969,-.448),.151,.161,fur,group='tail',bevel=.030)
 o=B.box('Big cream fox tail tip',(-.355,1.057,-.485),(.177,.215,.171),cream,group='tail',bevel=.028);o.rotation_euler.x=-.22

def common_details(B,c):
 # Discrete foot rest joins the chassis below the short chibi feet.
 B.box('Footwell pedal plate',(0,.495,.092),(.365,.036,.238),TRIM,'22','chassis',.010)
 B.beam('Footwell support',(0,.286,.155),(0,.480,.125),.042,.040,STEEL,'23','chassis',.006)
 # A short open-cockpit screen stays well below the driver and steering grip.
 v=[(-.228,.565,.320),(.228,.565,.320),(.215,.685,.290),(-.215,.685,.290)]
 B.box('Continuous windscreen mounting plinth',(0,.537,.320),(.478,.060,.045),TRIM,'22','chassis',.011)
 B.mesh('Low smoked windscreen',v,[(0,1,2,3)],'6995A1','27','chassis')
 B.tube('Short windscreen frame',[v[3],v[2]],.010,c['accent'],'21',sides=6)

def rally(B,c):
 p=c['paint'];a=c['accent'];red='E87953'
 B.loft('Rally broad squared bonnet',[(.18,.325,.30,.552,.030),(.45,.398,.27,.522,.028),(.735,.375,.26,.450,.025)],p)
 B.loft('Rally rear hatch shoulder',[(-.785,.305,.30,.49,.026),(-.60,.375,.29,.565,.029),(-.46,.310,.30,.550,.024)],p)
 B.box('Rally inset radiator',(0,.357,.756),(.565,.132,.025),TRIM,'22','chassis',.014)
 for x in [-.21,-.105,0,.105,.21]:B.box('Horizontal rally grille tooth',(x,.356,.773),(.060,.016,.010),STEEL,'23','chassis',.003)
 for side in [-1,1]:
  for z in [.48,-.56]:
   B.box('Broad rally wheel shoulder',(side*.508,.463,z),(.313,.075,.425),p,'21','chassis',.020)
   B.box('Dark rally arch lip',(side*.528,.423,z),(.323,.026,.381),TRIM,'22','chassis',.009)
   B.box('Flexible rear mud flap',(side*.59,.233,z-.220),(.186,.171,.025),TRIM,'25','chassis',.008)
  B.box('Rally squared headlight',(side*.309,.424,.751),(.125,.088,.035),'FFF0C9','26','chassis',.012)
  B.cylinder('Extra round square rally lamp housing',(side*.134,.456,.800),.058,.037,TRIM,'22','chassis',sides=12 if B.high else 8,axis='Z')
  B.cylinder('Extra rally lamp lens',(side*.134,.456,.823),.043,.009,'FFE6A4','26','chassis',sides=12 if B.high else 8,axis='Z')
  B.box('Rally joined middle body panel',(side*.390,.408,-.060),(.130,.175,.590),p,'21','chassis',.018)
  B.box('Cream rally sill',(side*.440,.327,-.08),(.079,.091,.650),a,'21','chassis',.015)
  B.box('Coral side number panel',(side*.483,.371,-.09),(.012,.107,.205),red,'21','chassis',.008)
  B.box('Rally side white number dash',(side*.491,.371,-.09),(.006,.067,.034),WHITE,'21','chassis',.004)
  B.box('Rally rear lamp',(side*.272,.473,-.784),(.136,.060,.026),'F27669','26','chassis',.010)
  B.tube('Rally angled half cage',[(side*.283,.510,-.48),(side*.300,1.026,-.51),(side*.235,1.075,-.54)],.022,TRIM,'22')
  B.box('Rally spoiler pylon',(side*.270,.560,-.717),(.035,.174,.047),TRIM,'22','chassis',.008)
  B.box('Cream hood livery slash',(side*.198,.525,.400),(.042,.012,.213),a,'21','chassis',.005)
 B.tube('Rally cage header',[(-.235,1.075,-.54),(.235,1.075,-.54)],.022,TRIM,'22')
 B.box('Rally rear roof scoop',(0,1.081,-.55),(.215,.069,.147),p,'21','chassis',.014)
 B.box('Rally roof scoop intake',(0,1.089,-.470),(.145,.028,.012),TRIM,'22','chassis',.004)
 B.box('Rally strong front bumper',(0,.257,.815),(.946,.104,.102),STEEL,'23','chassis',.019)
 B.tube('Rally protective front hoop',[(-.39,.295,.831),(-.36,.377,.831),(.36,.377,.831),(.39,.295,.831)],.022,TRIM,'22')
 B.box('Rally rear wing',(0,.653,-.727),(.842,.045,.177),red,'21','chassis',.013)
 B.box('Rally rear skid bar',(0,.245,-.816),(.746,.070,.091),TRIM,'22','chassis',.016)

def roadster(B,c):
 p=c['paint'];a=c['accent']
 B.loft('Mini short round square nose',[(.20,.283,.30,.533,.046),(.37,.357,.27,.513,.044),(.60,.342,.26,.442,.044),(.759,.245,.28,.397,.036)],p)
 B.loft('Mini tidy rounded tail',[(-.755,.245,.29,.393,.032),(-.61,.340,.25,.485,.039),(-.46,.295,.29,.490,.035)],p)
 B.box('Mini smiling dark grille',(0,.347,.776),(.251,.077,.026),TRIM,'22','chassis',.021)
 B.box('Mini slim chrome grille line',(0,.333,.793),(.169,.014,.008),STEEL,'23','chassis',.004)
 for side in [-1,1]:
  # Low chamfered fender strips expose the wheels; no large pontoon/capsule shell.
  for z in [.48,-.56]:B.box('Mini rounded wheel brow',(side*.495,.451,z),(.280,.054,.353),p,'21','chassis',.023)
  B.box('Mini big cream lamp surround',(side*.227,.410,.721),(.151,.122,.069),a,'21','chassis',.028)
  B.box('Mini large headlight',(side*.227,.414,.762),(.105,.080,.019),'FFF5D4','26','chassis',.021)
  B.box('Mini chrome bumper end',(side*.237,.278,.775),(.198,.042,.063),STEEL,'23','chassis',.014)
  B.box('Mini coral rear lamp',(side*.215,.416,-.749),(.124,.050,.032),'ED978E','26','chassis',.013)
  B.box('Mini low sill',(side*.381,.305,-.082),(.098,.079,.531),p,'21','chassis',.022)
  B.box('Mini cream side trim',(side*.435,.336,-.076),(.010,.019,.383),WHITE,'21','chassis',.005)
 B.box('Mini coral nose badge',(0,.474,.502),(.075,.012,.069),a,'21','chassis',.011)
 B.box('Mini low rear lip',(0,.491,-.632),(.530,.031,.098),a,'21','chassis',.012)
 B.tube('Mini low seat hoop',[(-.218,.527,-.529),(-.218,.854,-.529),(-.149,.893,-.529),(.149,.893,-.529),(.218,.854,-.529),(.218,.527,-.529)],.016,STEEL,'23')
 # Small ivory hub covers distinguish the mini from multispoke performance rims.
 for side,x in [('l',-.59),('r',.59)]:
  sign=-1 if x<0 else 1
  for end,z in [('f',.48),('r',-.56)]:
   g='wheel_'+end+side+'_spin'
   B.cylinder('Mini ivory hub cap',(x+sign*.137,.205,z),.091,.008,WHITE,'22',g,sides=16 if B.high else 8)
   B.cylinder('Mini coral centre cap',(x+sign*.144,.205,z),.032,.008,a,'22',g,sides=12 if B.high else 8)

def gt(B,c):
 p=c['paint'];a=c['accent'];black='293744'
 B.loft('GT long wide creased bonnet',[(.175,.307,.30,.548,.028),(.34,.403,.27,.530,.031),(.62,.414,.255,.455,.031),(.826,.325,.27,.383,.025)],p)
 B.loft('GT wide rear haunch deck',[(-.799,.302,.28,.470,.025),(-.635,.424,.265,.527,.030),(-.468,.349,.29,.521,.028)],p)
 B.box('GT wide black grille',(0,.329,.833),(.586,.092,.024),black,'22','chassis',.013)
 for x in [-.22,-.11,0,.11,.22]:B.box('GT vertical grille blade',(x,.329,.850),(.013,.061,.008),STEEL,'23','chassis',.002)
 for side in [-1,1]:
  for z in [.48,-.56]:
   # Long, joined shoulders rather than Formula's isolated wings/open wheels.
   B.box('GT integrated fender shoulder',(side*.473,.442,z),(.301,.090,.461),p,'21','chassis',.023)
   B.box('GT dark arch edge',(side*.537,.399,z),(.237,.022,.377),black,'22','chassis',.008)
  B.prism('GT sharp block lamp',[(side*.349-.077,.443),(side*.349+.077,.418),(side*.349+.070,.387),(side*.349-.077,.409)],.761,.793,'E7F2D7','26','chassis',.006)
  B.box('GT sculpted sill',(side*.412,.296,-.084),(.132,.086,.610),black,'22','chassis',.014)
  B.box('GT continuous sculpted side panel',(side*.400,.403,-.048),(.172,.175,.585),p,'21','chassis',.018)
  B.box('GT side intake',(side*.487,.387,-.057),(.022,.096,.213),black,'22','chassis',.015)
  B.box('GT ivory side flash',(side*.492,.453,-.082),(.012,.028,.278),a,'21','chassis',.004)
  B.box('GT rear narrow lamp',(side*.267,.455,-.800),(.208,.033,.021),'F08473','26','chassis',.007)
  B.box('GT spoiler mount',(side*.258,.547,-.725),(.037,.167,.043),black,'22','chassis',.008)
  B.box('GT wing endplate',(side*.451,.636,-.749),(.025,.113,.176),black,'22','chassis',.008)
  B.cylinder('GT twin exhaust outer',(side*.235,.259,-.824),.041,.067,STEEL,'23','chassis',axis='Z')
  B.cylinder('GT twin exhaust inset',(side*.235,.259,-.861),.027,.007,black,'22','chassis',axis='Z')
 B.box('GT front chin',(0,.236,.814),(.854,.041,.103),black,'22','chassis',.011)
 B.box('GT wide ivory rear wing',(0,.650,-.749),(.920,.039,.174),a,'21','chassis',.012)
 B.box('GT rear diffuser',(0,.230,-.784),(.637,.061,.153),black,'22','chassis',.012)
 for x in [-.19,0,.19]:B.box('GT diffuser vane',(x,.211,-.805),(.018,.060,.139),black,'22','chassis',.004)
 rows=[(.21,.546),(.34,.532),(.62,.457),(.80,.399)]
 for side in [-1,1]:
  v=[(x,y+.002,z) for z,y in rows for x in [side*.064-.018,side*.064+.018]]
  B.mesh('GT double ivory bonnet livery',v,[(i,i+1,i+3,i+2) for i in range(0,len(v)-2,2)],a,'21','chassis')

report=[]
for c in CHARACTERS:
 row={'id':c['id'],'name':c['name'],'vehicle':c['vehicle'],'models':{}}
 for high in [True,False]:
  B=Builder(c['root'],high);cockpit(B,c);common_details(B,c)
  {'dog':rally,'mouse':roadster,'fox':gt}[c['animal']](B,c)
  wheels(B,dict(c,animal='bear' if c['animal']=='dog' else 'rabbit' if c['animal']=='fox' else 'mouse'))
  seated_body(B,c);{'dog':dog,'mouse':mouse,'fox':fox}[c['animal']](B,c)
  file='kart_'+c['id']+('' if high else '_low')+'.glb'
  row['models']['high' if high else 'low']=B.export(OUT/'models'/file,{'animal':c['animal'],'vehicle':c['vehicle'],'identityReference':'avatar_'+c['id']+'.webp','style':'blocky chibi','version':'Batch 3'})
  if high:B.save_source(HERE/('race-quest-'+c['id']+'.blend'))
 report.append(row)
(OUT/'build-metrics.json').write_text(json.dumps(report,indent=2))
