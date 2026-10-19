"""Bounded presentation hooks into the existing UI closure. Gameplay functions are untouched."""
def patch_app(s):
 changes=[]
 def replace(old,new):
  nonlocal s
  assert s.count(old)==1,old[:100]
  s=s.replace(old,new);changes.append({'old':old,'new':new})
 start=s.index('function fillSetupBank(){');end=s.index("\n$('setupBank').onchange",start);old=s[start:end];replace(old,old.rsplit('}',1)[0]+';RaceStageUI.mountSetup(b)}')
 replace('await ensureRenderer();if(!preferences.tutorialSeen)','await ensureRenderer();RaceStageUI.mountGarage(state.config,b);if(!preferences.tutorialSeen)')
 replace('Grand Prix: Kampung → Kapuas → Hutan.','Grand Prix: Pontianak → Mempawah → Singkawang.')
 replace("clone.querySelector('#initialData').textContent=", "for(const n of clone.querySelectorAll('.patch-stage-picker'))n.remove();clone.querySelector('#garageStagePicker').replaceChildren();\n clone.querySelector('#initialData').textContent=")
 return s,changes
