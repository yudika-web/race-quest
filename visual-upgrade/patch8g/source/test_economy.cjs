const assert=require('assert'),{load}=require('./harness.cjs'),{C}=load();let checks=[];
function test(name,fn){fn();checks.push(name)}
const sample=C.sampleData(),blank={...sample};delete blank.profile;
test('fresh profile: zero tokens, exactly four free',()=>{assert.equal(sample.profile.tokens,0);assert.deepEqual([...sample.profile.unlocked],[0,1,2,3])});
test('missing profile import and null profile cannot unlock all',()=>{for(const data of [blank,{...blank,profile:null}])assert.deepEqual([...C.normalizeData(data).profile.unlocked],[0,1,2,3])});
const legacy={...C.normalizeProfile(),tokens:180,xp:760,unlocked:Array.from({length:14},(_,i)=>i),paints:['original','mint']};
test('valid legacy all-unlocked profile retains progression',()=>{const p=C.normalizeData({...sample,profile:legacy}).profile;for(const k of ['tokens','xp','unlocked','paints'])assert.deepEqual(JSON.parse(JSON.stringify(p[k])),legacy[k])});
test('insufficient purchase rejects without mutation',()=>{assert.throws(()=>C.purchase(sample.profile,'character',4));assert.equal(sample.profile.tokens,0)});
let paid;
test('60 charged once, duplicate purchase no charge, reload retains',()=>{paid=C.purchase({...sample.profile,tokens:120},'character',13);assert.equal(paid.tokens,60);paid=C.purchase(paid,'character',13);assert.equal(paid.tokens,60);assert(C.normalizeData(JSON.parse(JSON.stringify({...sample,profile:paid}))).profile.unlocked.includes(13))});
test('all ten premium characters cost 60; paints remain 40',()=>{for(let i=4;i<14;i++){const p=C.purchase({...sample.profile,tokens:60},'character',i);assert.equal(p.tokens,0);assert(p.unlocked.includes(i))}assert.equal(C.purchase({...sample.profile,tokens:60},'paint','mint').tokens,20)});
test('existing rewards unchanged; same result once after save/reload',()=>{let p=C.normalizeProfile();const r={id:'fixture-race-1',tokens:7,position:1,correct:10};const a=C.awardProfile(p,r);assert.equal(a.earned,62);assert.equal(a.profile.xp,245);p=C.normalizeData({...sample,profile:a.profile}).profile;const again=C.awardProfile(p,r);assert.equal(again.earned,0);assert.equal(again.profile.tokens,62);assert.equal(again.profile.races,1);const b=C.awardProfile(p,{...r,id:'fixture-race-2',position:3,correct:0});assert.equal(b.earned,17);assert.equal(b.profile.tokens,79)});
console.log(JSON.stringify({checks,passed:checks.length},null,2));require('fs').writeFileSync(require('path').resolve(__dirname,'../unit-results.json'),JSON.stringify({checks,passed:checks.length},null,2));
