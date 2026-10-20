// Pure points/assessment sequence: no world construction or availability override.
class GrandPrixSequence{
 constructor(threshold=60,stageIds){if(!Array.isArray(stageIds)||!stageIds.length||new Set(stageIds).size!==stageIds.length)throw Error('Urutan ronde tidak valid.');this.stageIds=stageIds.slice();this.threshold=clamp(Number(threshold)||0,0,100);this.round=0;this.results=[];this.points=[0,0,0,0,0];this.wins=[0,0,0,0,0];this.blocked=false;this.complete=false}
 get totalRounds(){return this.stageIds.length}
 get stageId(){return this.stageIds[this.round]}
 accept(result){if(this.complete||this.blocked||this.results.length!==this.round)throw Error('Putaran sudah dicatat.');if(!Number.isFinite(result.score)||result.score<0||result.score>100)throw Error('Skor asesmen tidak valid.');if(result.stage&&result.stage!==this.stageId)throw Error('Hasil bukan untuk ronde yang aktif.');const order=result.finishOrder||[0,1,2,3,4];if(order.length!==5||new Set(order).size!==5||order.some(id=>!Number.isInteger(id)||id<0||id>4))throw Error('Urutan finis tidak valid.');order.forEach((id,i)=>{this.points[id]+=[25,18,15,12,10][i];if(i===0)this.wins[id]++});this.results.push(copy(result));this.blocked=result.score<this.threshold;this.complete=this.round===this.totalRounds-1&&!this.blocked}
 next(){if(this.blocked||this.complete||this.results.length!==this.round+1)return false;this.round++;return true}
 retry(){if(!this.blocked)return false;const r=this.results.pop();(r.finishOrder||[0,1,2,3,4]).forEach((id,i)=>{this.points[id]-=[25,18,15,12,10][i];if(i===0)this.wins[id]--});this.blocked=false;return true}
 standings(){return this.points.map((points,id)=>({id,points,wins:this.wins[id]})).sort((a,b)=>b.points-a.points||b.wins-a.wins||a.id-b.id)}
 summary(){return this.results.map((r,i)=>({round:i+1,stage:this.stageIds[i],position:r.position??(r.finishOrder||[0,1,2,3,4]).indexOf(0)+1,score:r.score,finishOrder:r.finishOrder||[0,1,2,3,4]}))}
}
class GrandPrix extends GrandPrixSequence{
 constructor(threshold=60,cupId='kalbar-klasik',progress={}){super(threshold,root.RaceStages.requireCup(cupId,progress));this.cupId=cupId;this.label=root.RaceStages.cup(cupId).displayName}
 get stage(){return stageById(this.stageId)}
}
