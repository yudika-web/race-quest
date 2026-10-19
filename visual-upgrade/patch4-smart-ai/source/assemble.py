from pathlib import Path
import re,json,hashlib
D=Path(__file__).resolve().parents[2];B=D/'patch4-smart-ai';base=(D/'race-quest-pro-patch3.html').read_text();h=base;changes=[]
(B/'baseline.json').write_text(json.dumps({'commit':'dab093d0c26dd38afdece02b45a8577111b512ab','bytes':len(base.encode()),'sha256':hashlib.sha256(base.encode()).hexdigest()},indent=2))
def change(old,new):
 global h
 assert h.count(old)==1,(old[:100],h.count(old));h=h.replace(old,new);changes.append({'old':old,'new':new})
change('...this.batchPose(session,a,kartFiles[a.character],i+1)})}}','...this.batchPose(session,a,kartFiles[a.character],i+1)});if(this.smartAIIndicator)this.smartAIIndicator(a,q)}}')
change('steer:-tr.curvature(a.s)*3','steer:actual.smartSteer??-tr.curvature(a.s)*3')
change('RaceBuffUI.update(s);','RaceBuffUI.update(s);RaceAIUI.update(s);')
change("for(const id of ['strategicSlots','strategyRadar','rewardChoice'])", "for(const id of ['strategicSlots','strategyRadar','rewardChoice','smartAINotice','smartAIWarning'])")
change('Lawan Sedang dan Menantang dapat menyerang dengan gelembung atau oli. Perisai menangkisnya; Santai aman dari serangan AI.', 'Lawan punya dua slot dengan pasokan terbatas saat melintasi pos soal. Santai tidak menembak atau memasang oli; Sedang dan Menantang bereaksi bertahap dengan indikator ancaman. Perisai menangkis serangan. AI tidak membaca soal atau kunci jawaban.')
(B/'bounded-changes.json').write_text(json.dumps(changes,indent=2,ensure_ascii=False))
h=h.replace('</head>','<style id="patch4Styles">'+(B/'source/ui.css').read_text()+'</style></head>',1)
s=list(re.finditer(r'<script\b[^>]*>(.*?)</script>',h,re.S));pos=s[16].end();block=''
for id,file in [('patch4SmartAI','ai.js'),('patch4AIUI','ui.js')]:block+='\n<script id="'+id+'">'+(B/'source'/file).read_text()+'</script>'
h=h[:pos]+block+h[pos:];out=D/'race-quest-pro-patch4.html';out.write_text(h);print('PATCH 4',out.stat().st_size,'bytes')
