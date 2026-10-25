import {getLeyningForParsha, getWeekdayReading, formatAliyahWithBook} from '@hebcal/leyning';
import {normalize} from './audio.js';

const entities={nbsp:' ',thinsp:'\u2009',hairsp:'\u200a',ensp:'\u2002',emsp:'\u2003',lrm:'\u200e',rlm:'\u200f',zwj:'\u200d',zwnj:'\u200c',shy:'\u00ad',amp:'&',quot:'"',apos:"'",lt:'<',gt:'>'};
export const stripHtml=value=>String(value||'').replace(/<br\s*\/?\s*>/gi,'\n').replace(/<[^>]*>/g,'').replace(/&(#x[0-9a-f]+|#\d+|[a-z]+);/gi,(match,name)=>{if(name[0]==='#'){const number=name[1].toLowerCase()==='x'?parseInt(name.slice(2),16):Number(name.slice(1));return number>0&&number<=0x10ffff?String.fromCodePoint(number):'';}return entities[name]??match;});

const hebrew = s => String(s||'').normalize('NFD').replace(/[\u0591-\u05c7]/g,'').replace(/[־–—]/g,' ').replace(/[״׳"':,.;!?]/g,'').replace(/\s+/g,' ').trim();
const aliases = {vayelech:'Vayeilech',haazinu:"Ha'azinu"};
function parsha(name){return getLeyningForParsha(aliases[normalize(name)]||name)}
export function referenceFromDescription(description){
 const text=String(description||'').replace(/[–—]/g,'-');
 const found=text.match(/((?:(?:[123]|I{1,3})\s+)?[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(\d+:\d+(?:\s*-\s*(?:\d+:)?\d+)?(?:\s*[;&]\s*(?:(?:(?:[123]|I{1,3})\s+)?[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+)?\d+:\d+(?:\s*-\s*(?:\d+:)?\d+)?)*)/);
 if(!found)return null;
 const book=found[1].replace(/^1 /,'I ').replace(/^2 /,'II ').replace(/^3 /,'III ');
 return found[2].split(/\s*[;&]\s*/).map(x=>/^\d/.test(x)?book+' '+x:x.replace(/^1 /,'I ').replace(/^2 /,'II ')).join('; ');
}
// Keep vowel marks in the displayed text while finding passages without vowel marks.
export function extractHebrewPassage(html,start,end){
 const plain=stripHtml(html),positions=[];let normalized='';let lastSpace=false;
 for(let i=0;i<plain.length;i++){
  const c=plain[i];if(/[\u0591-\u05c7]/.test(c)||/[״׳"':,.;!?]/.test(c))continue;
  const isSpace=/\s|[־–—]/.test(c);if(isSpace){if(!lastSpace){positions.push(i);normalized+=' ';}lastSpace=true;}else{positions.push(i);normalized+=c;lastSpace=false;}
 }
 const begin=normalized.indexOf(hebrew(start));if(begin<0)return null;const finish=end?normalized.indexOf(hebrew(end),begin+hebrew(start).length):-1;
 return plain.slice(positions[begin],finish<0?plain.length:positions[finish]).trim();
}
function sectionByTitle(siddur,title){return siddur.find(s=>hebrew(s.title)===hebrew(title)&&stripHtml(s.html).trim())}
function fragment(section,start,end,title){if(!section)return null;const text=extractHebrewPassage(section.html,start,end);return text?{type:'siddur',title,sectionId:section.id,text,source:'Edot HaMizrach · Shaliehsaboo Edition',sourceUrl:'https://www.sefaria.org/Siddur_Edot_HaMizrach',note:'Mitlesetext zur Gebetspassage. Aussprache und einzelne Fassungsvarianten können von der Aufnahme abweichen.'}:null}
function siddurSection(section,title=section?.title){return section?{type:'siddur',title,sectionId:section.id,html:section.html,source:'Edot HaMizrach · Shaliehsaboo Edition',sourceUrl:'https://www.sefaria.org/Siddur_Edot_HaMizrach',note:'Die Anweisungen und Varianten der Textausgabe bleiben sichtbar.'}:null}
function bible(ref,title,note=''){return {type:'bible',ref,title,source:'Hebräischer Originaltext · Sefaria',sourceUrl:'https://www.sefaria.org/'+encodeURIComponent(ref),note}}
export function resolveReadAlong(track,{siddur=[],external={},step}={}){
 if(!track)return null;
 if(track.textRef)return bible(track.textRef,track.title||track.canonical||track.textRef,track.textNote||'');
 if(track.sectionId!==undefined)return siddurSection(siddur.find(s=>s.id===track.sectionId));
 // Resolve individual files by their actual URL, including manual starts from the table.
 for(const item of external.torahAliyot||[]){for(const mode of ['shabbat','weekday']){const match=Object.entries(item[mode]||{}).find(([,url])=>url===track.url);if(!match)continue;const reading=parsha(item.canonical);const aliyah=(mode==='weekday'?getWeekdayReading(reading.parsha):reading.fullkriyah)[match[0]];if(aliyah)return bible(formatAliyahWithBook(aliyah),`${item.canonical} · Alija ${match[0]}`,'Textbereich nach dem Lesekalender. Die syrischen Alija-Grenzen der Aufnahme können davon abweichen; keine wortgenauen Zeitmarken.');}}
 if(track.canonical&&track.kind!=='haftarah'){
  try{return bible(parsha(track.canonical).summary,track.canonical,track.kind==='uploaded'?'Parascha-Zuordnung nach dem Dateinamen; Umfang der eigenen Aufnahme nicht geprüft.':'Vollständige Wochenparascha zur Aufnahme.')}catch{}
 }
 if(track.kind==='haftarah'){
  const ref=referenceFromDescription(track.description);return ref?bible(ref,track.title||'Haftara'):null;
 }
 const label=hebrew(track.title||'');const latin=normalize(track.title);
 const get=title=>sectionByTitle(siddur,title);
 if(label==='קריאת שמע')return bible('Deuteronomy 6:4-9; Deuteronomy 11:13-21; Numbers 15:37-41','קריאת שמע · Schma Jisrael','Die drei Schma-Abschnitte; die Aufnahme kann einen Ausschnitt daraus enthalten.');
 if(label==='Full Weekday Amidah'||latin==='fullweekdayamidah')return siddurSection(get('עמידה לשחרית של יום חול'));
 if(label==='פטום הקטרת'||label==='פטום הקטורת')return fragment(get('פטום הקטורת'),'אתה הוא','אביי','פיטום הקטורת · Ketoret')||siddurSection(get('פטום הקטורת'));
 if(label.includes('פתיחת אליהו')||label.includes('פתח אליהו'))return siddurSection(get('פתיחת אליהו'));
 if(label==='אשרי יושבי ביתך')return siddurSection(get('אשרי יושבי ביתך'));
 if(track.key==='havdalah'||latin.startsWith('havdala'))return siddurSection(get('סדר הבדלה'));
 if(track.key==='hallel'||latin.includes('sederhallel'))return siddurSection(get('הלל לראש חודש ולמועדים'));
 if(latin.startsWith('lahaftara')){const h=(external.recordings||[]).find(r=>r.kind==='haftarah'&&normalize(r.canonical)===normalize("Beha'alotcha"));return h?bible(referenceFromDescription(h.description),'הפטרה · Beha’alotcha','Zuordnung nach dem Dateinamen der eigenen Aufnahme.'):null;}
 if(label==='נקדישך'||track.key==='kedusha'||latin.startsWith('nakdishkha'))return fragment(get('עמידה לשחרית של יום חול'),'נקדישך','אתה קדוש','נקדישך · Keduscha');
 if(label==='קדיש'||track.key==='kaddish-pesach'||label.includes('קדיש')||latin.startsWith('kaddish'))return fragment(get('ובא לציון גואל'),'יתגדל','יהא שלמא','קדיש · Kaddisch');
 const pesukei=siddur.find(s=>s.title==='פסוקי דזמרה'&&s.id>50);
 const pieces=[['נשמת','נשמת כל חי','שועת עניים','נשמת כל חי · Nischmat'],['שועת עניים','שועת עניים','אל ההודאות','שועת עניים · Schawat Anijim'],['אל ההודאות','אל ההודאות','ישתבח','אל ההודאות · El HaHodaot'],['כי לה המלוכה','כי ליהוה המלוכה','נשמת כל חי','כי לה׳ המלוכה'],['שמחים','שמחים','מי כמכה','שמחים · Semechim'],['ממצרים','ממצרים','מי כמכה','ממצרים · MiMizrajim']];
 for(const [key,start,end,title] of pieces){if(label!==key)continue;const sections=['שמחים','ממצרים'].includes(key)?siddur.filter(s=>s.title==='ק"ש וברכותיה'): [pesukei];for(const s of sections){const x=fragment(s,start,end,title);if(x)return x;}return null;}
 // Never replace an unidentified recording with the unrelated current day's prayer.
 return null;
}

export function versesFromSefaria(body,reference){
 if(body.error||!body.he)throw new Error('Kein hebräischer Text verfügbar.');
 const start=body.sections||[Number(reference.match(/\d+/)?.[0])||1,1];const result=[];
 const append=(text,chapter,verse)=>{if(typeof text==='string'&&stripHtml(text).trim())result.push({text:stripHtml(text),label:`${chapter}:${verse}`})};
 if(typeof body.he==='string')append(body.he,start[0],start[1]||1);
 else if(Array.isArray(body.he)&&body.he.some(Array.isArray))body.he.forEach((chapter,i)=>{const list=Array.isArray(chapter)?chapter:[chapter];list.forEach((text,j)=>append(text,start[0]+i,(i===0?(start[1]||1):1)+j));});
 else body.he.forEach((text,i)=>append(text,start[0],(start[1]||1)+i));
 if(!result.length)throw new Error('Kein hebräischer Text verfügbar.');return result;
}
export class ReadAlongLoader{
 constructor(fetcher=(...args)=>fetch(...args)){this.fetcher=fetcher;this.cache=new Map();this.generation=0;this.abort=null;}
 cancel(){this.generation++;this.abort?.abort();}
 async load(descriptor){this.cancel();const generation=this.generation;if(!descriptor||descriptor.type!=='bible')return descriptor;const controller=this.abort=new AbortController();
 const timer=setTimeout(()=>controller.abort(),12000);
 try{const passages=[];for(const ref of descriptor.ref.split(/;\s*/)){let verses=this.cache.get(ref);if(!verses){const response=await this.fetcher('https://www.sefaria.org/api/texts/'+encodeURIComponent(ref)+'?context=0&commentary=0',{signal:controller.signal});if(!response.ok)throw new Error('Textquelle momentan nicht erreichbar.');const body=await response.json();verses=versesFromSefaria(body,ref);if(generation!==this.generation)return null;this.cache.set(ref,verses);}passages.push({ref,verses});}
 if(generation!==this.generation)return null;return {...descriptor,passages};
 }finally{clearTimeout(timer);}
 }
}
