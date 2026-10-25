// Shared by the WebGL room and its Canvas fallback. Ark actions follow the
// named service step, never a worshipper's generic standing/reading pose.
const clamp=value=>Math.max(0,Math.min(1,Number.isFinite(value)?value:0));
const smooth=value=>{const t=clamp(value);return t*t*(3-2*t)};

export function arkActionForStep(step){
 if(!step)return 'closed';
 if(step.id==='open-ark')return 'opening';
 if(['return-torah','shofar-final'].includes(step.id))return 'closing';
 if(['procession','hagbaha','torah','maftir','haftara','neilah','shema-final'].includes(step.id))return 'open';
 if(step.id==='kol-nidre'||step.id==='hoshanot'&&step.pose==='hoshanot'||step.id==='simchat'&&step.pose==='hakafot')return 'open-close';
 return 'closed';
}

export function ritualForStep(step,progress=0){
 const p=clamp(progress),action=step?.arkAction??arkActionForStep(step);
 const opening=action==='opening'?smooth(p/.3):action==='closing'?1-smooth((p-.75)/.25):action==='open'?1:action==='open-close'?smooth(p/.12)*(1-smooth((p-.82)/.18)):0;
 const returning=step?.id==='return-torah';
 const procession=step?.id==='procession'||returning;
 const travel=returning?clamp(p/.75):p;
 return {opening,procession,returning,processionZ:returning?0-10*travel:-10+10*travel,
  carrying:procession&&(!returning||p<.75),
  scrollOut:['procession','hagbaha','torah','maftir','haftara'].includes(step?.id)||returning&&p<.75,
  bimahReading:['torah','maftir'].includes(step?.id),
  label:opening<.01?'Parochet geschlossen':opening>.99?'Parochet offen':action==='closing'||action==='open-close'&&p>.82?'Parochet schließt sich':'Parochet öffnet sich'};
}

// Each half gathers against its own outer jamb, leaving the middle clear.
export function parochetPanel(opening,side){
 const amount=clamp(opening),scaleX=1-.82*amount;
 return {x:Math.sign(side)*(.99+.82*amount),scaleX,width:2*scaleX};
}

export function animateParochet(current,target,dt,reduce=false){
 const goal=clamp(target);
 if(reduce)return goal;
 const next=clamp(current)+(goal-clamp(current))*(1-Math.exp(-Math.max(0,dt)*5));
 return Math.abs(next-goal)<.001?goal:next;
}
