import test from 'node:test';
import assert from 'node:assert/strict';
import {dayInfo,servicePlan,HDate,isoDate} from '../src/engine.js';
import {arkActionForStep,ritualForStep,parochetPanel,animateParochet} from '../src/ritual.js';

test('The parochet opens before Torah removal, stays open through the reading and closes after return',()=>{
 for(const [date,service] of [['2026-10-26','shacharit'],['2026-10-31','shacharit'],['2026-10-31','mincha']]){
  const plan=servicePlan(dayInfo(date),service),start=plan.findIndex(s=>s.id==='open-ark'),end=plan.findIndex(s=>s.id==='return-torah');
  assert.ok(start>0&&end>start);
  assert.equal(ritualForStep(plan[start],0).opening,0);assert.equal(ritualForStep(plan[start],.5).opening,1);
  for(const step of plan.slice(start+1,end))assert.equal(ritualForStep(step,.5).opening,1,step.id);
  const returning=plan[end];assert.equal(ritualForStep(returning,0).processionZ,0);
  assert.equal(ritualForStep(returning,.75).processionZ,-10);assert.equal(ritualForStep(returning,.75).carrying,false);
  assert.equal(ritualForStep(returning,.75).opening,1);assert.equal(ritualForStep(returning,1).opening,0);
  assert.equal(ritualForStep(plan[end+1],0).opening,0);
 }
});

test('Kol Nidre, weekday Hoshanot and Hakafot open and close; Shabbat Hoshanot do not open the ark',()=>{
 const on=(d,m,y=5787)=>dayInfo(isoDate(new HDate(d,m,y).greg()));
 const cases=[servicePlan(on(10,7),'arvit').find(s=>s.id==='kol-nidre'),servicePlan(on(21,7)).find(s=>s.id==='hoshanot'),servicePlan(on(22,7)).find(s=>s.id==='simchat')];
 for(const step of cases){assert.ok(step);assert.equal(step.arkAction,'open-close');assert.equal(ritualForStep(step,0).opening,0);assert.equal(ritualForStep(step,.5).opening,1);assert.equal(ritualForStep(step,1).opening,0);}
 const shabbat=servicePlan(on(15,7)).find(s=>s.id==='hoshanot');assert.equal(shabbat.pose,'standing');assert.equal(ritualForStep(shabbat,.5).opening,0);
});

test('Neilah and its final Shema keep the parochet open until the final shofar closes it',()=>{
 const i=dayInfo(isoDate(new HDate(10,7,5787).greg()));const plan=servicePlan(i,'neilah');
 assert.equal(ritualForStep(plan[0],.5).opening,1);assert.equal(ritualForStep(plan[1],.5).opening,1);
 assert.equal(ritualForStep(plan[2],0).opening,1);assert.equal(ritualForStep(plan[2],1).opening,0);
 assert.equal(ritualForStep({id:'aleinu'},0).opening,0);
});

test('A generic reading pose never opens the ark or puts an open Torah on the bimah',()=>{
 for(const id of ['megillah','shema','amida','aleinu']){
  const step={id,pose:'reading'};assert.equal(arkActionForStep(step),'closed');assert.equal(ritualForStep(step,.5).bimahReading,false);
 }
 assert.equal(ritualForStep({id:'haftara'},.5).bimahReading,false);
 assert.equal(ritualForStep({id:'torah'},.5).bimahReading,true);
 assert.equal(ritualForStep(null).opening,0);
});

test('Closed curtain panels overlap at the seam; open panels gather at opposite outer edges',()=>{
 const left=parochetPanel(0,-1),right=parochetPanel(0,1);
 assert.ok(left.x+left.width/2>=right.x-right.width/2);
 const a=parochetPanel(1,-1),b=parochetPanel(1,1);
 assert.ok(a.x+a.width/2<-1.6);assert.ok(b.x-b.width/2>1.6);
 assert.equal(a.scaleX,b.scaleX);assert.equal(a.x,-b.x);
 let amount=0;for(let i=0;i<120;i++)amount=animateParochet(amount,1,1/60);assert.equal(amount,1);
 for(let i=0;i<120;i++)amount=animateParochet(amount,0,1/60);assert.equal(amount,0);
 assert.equal(animateParochet(0,1,0,true),1);
});
