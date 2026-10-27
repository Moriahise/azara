import test from 'node:test';
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {readFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {RashashTextStore,renderRashashReader,renderRashashPage,searchableHebrew,hasRashashTextPage} from '../src/rashash-reader.js';
import {stripHtml} from '../src/readalong.js';

test('All seven Rashash editions retain every source letter, original vowel and all tables',()=>{
 const report=JSON.parse(execFileSync('python3',['scripts/validate-rashash.py'],{encoding:'utf8'}));
 assert.deepEqual(report.map(v=>v.id),['21376','21375','21519','21520','21518','21722','21723']);
 assert.equal(report.reduce((n,v)=>n+v.pages,0),846);assert.equal(report.reduce((n,v)=>n+v.tables,0),1990);
 assert.ok(report.every(v=>(v.importedUnchanged||v.addedMarks>1000)&&v.protectedTokens>100));
});
test('Rashash Hebrew search works with or without Niqqud and quote variants',()=>{
 assert.equal(searchableHebrew('שַׁבָּת'),searchableHebrew('שבת'));
 assert.equal(searchableHebrew('רש״ש'),searchableHebrew('רש"ש'));
});
test('HB21375 reaches the scan end at PDF 323 with all 322 text pages and 86 uncertainties',async()=>{
 const index=JSON.parse(await readFile('data/rashash.json','utf8'));
 const doc=index.documents.find(d=>d.id==='21375'),metadata=doc.transcription;
 const volume=JSON.parse(await readFile(metadata.jsonPath,'utf8'));
 assert.equal(doc.pages,323);assert.equal(metadata.pdfPages,323);
 assert.deepEqual(volume.pages.map(p=>p.pdfPage),[1,...Array.from({length:321},(_,i)=>i+3)]);
 assert.deepEqual(metadata.coverage,{status:'complete',throughPdf:323,scanPages:323,omittedPdfPages:[2]});
 let uncertainties=0,tables=0;
 for(const page of volume.pages){
  for(const block of page.blocks){
   if(block.kind==='table')tables+=1+(block.nestedTables?.length||0);
   for(const item of block.kind==='table'?block.rows:[block]){
    uncertainties+=(item.text.match(/\[\?\]/g)||[]).length;
    if(item.text.includes('[?]'))assert.ok(item.html.includes('rashash-unclear'));
    assert.equal(stripHtml(item.html),item.text);
   }
  }
 }
 assert.equal(uncertainties,86);assert.equal(tables,843);
 const priorPages=volume.pages.filter(p=>p.pdfPage<=50).map(({pdfPage,folio,blocks})=>({pdfPage,folio,blocks}));
 assert.equal(createHash('sha256').update(JSON.stringify(priorPages)).digest('hex'),'eaef15028cff5dc7b58d2f2975b677c92ef4d3e4e145a7437ddbb097a64e616d');
 const prior100=volume.pages.filter(p=>p.pdfPage<=100).map(({pdfPage,folio,blocks})=>({pdfPage,folio,blocks}));
 assert.equal(createHash('sha256').update(JSON.stringify(prior100)).digest('hex'),'e4ea9103e48b793b3f6965d05eca098bddaad4a44914455afd521cd5d69584d4');
 const prior200=volume.pages.filter(p=>p.pdfPage<=200).map(({pdfPage,folio,blocks})=>({pdfPage,folio,blocks}));
 assert.equal(createHash('sha256').update(JSON.stringify(prior200)).digest('hex'),'43ea9483428eadbe1858ee0e4052e37e0ebc47e39b468eb0319919bd7ae850ac');
 assert.equal(metadata.statistics.reused_pages,199);
 assert.deepEqual(metadata.flags.filter(f=>f.kind==='source_uncertainty').map(f=>f.pdfPages[0]),[9,38,39,40,43,44,47,117,130,139,167,168,185,187,190,195,198,217,221,228,229,246,248,251,261,262,263,266,267,289,292,299,300,301,304,305,306,307,308,309,310,312,317,321]);
 const tagged=await readFile(metadata.txtPath,'utf8');
 assert.equal((tagged.match(/<unclear /g)||[]).length,86);
 assert.ok(tagged.includes('<coverage status="complete" through-pdf="323" scan-pages="323"'));
 assert.ok(tagged.includes('engine="Dicta Nakdan" genre="rabbinic"'));
 assert.ok(searchableHebrew(volume.pages.find(p=>p.pdfPage===3).blocks.map(b=>b.text||'').join(' ')).includes('הודו'));
 for(const n of [1,3,50,51,54,100,101,200,201,245,322,323])assert.ok(hasRashashTextPage(metadata,n));
 for(const n of [0,2,324])assert.equal(hasRashashTextPage(metadata,n),false);
 const html=renderRashashReader({documents:index.documents,id:'21375',pageNumber:200,volume});
 assert.ok(!html.includes('Teilfassung ·'));
 const final=renderRashashReader({documents:index.documents,id:'21375',pageNumber:323,volume});
 assert.ok(final.includes('data-open-rashash="21375" data-page="323"'));
 assert.ok(final.includes('<span>PDF 323</span>'));
 assert.ok(final.includes('data-action="rashash-text-next" disabled'));
 assert.ok(!metadata.flags.some(f=>f.kind==='partial_transcription'));
 assert.ok(html.includes('data-open-rashash="21375" data-page="200"'));
 const partialMetadata={...metadata,pdfPages:200,coverage:{status:'partial',throughPdf:200,scanPages:323,omittedPdfPages:[2]}};
 const partialVolume={...volume,...partialMetadata,pages:volume.pages.filter(p=>p.pdfPage<=200)};
 const missing=renderRashashReader({documents:index.documents.map(d=>d.id==='21375'?{...d,transcription:partialMetadata}:d),id:'21375',pageNumber:201,volume:partialVolume});
 assert.ok(missing.includes('PDF 201 ist noch nicht transkribiert'));
 assert.ok(missing.includes('data-open-rashash="21375" data-page="201"'));
 assert.ok(!missing.includes('<span>PDF 1</span>'));
});
test('HB21375 retains nested tables and joined boundaries without losing or duplicating source rows',async()=>{
 const volume=JSON.parse(await readFile('data/rashash-text-21375.json','utf8'));
 const tables=volume.pages.flatMap(p=>p.blocks.filter(b=>b.kind==='table'));
 assert.equal(tables.length,777);
 assert.equal(tables.reduce((n,t)=>n+(t.nestedTables?.length||0),0),66);
 const page245=volume.pages.find(p=>p.pdfPage===245);
 const outer=page245.blocks.find(b=>b.kind==='table'&&b.nestedTables?.length===1);
 assert.ok(outer);
 assert.deepEqual(outer.nestedTables.map(t=>t.startLine),[14037]);
 assert.deepEqual(page245.blocks.filter(b=>b.kind==='table').map(t=>[t.startLine,t.endLine]),[[14032,14056],[14056,14070],[14070,14084],[14084,14098]]);
 const rows=tables.flatMap(t=>t.rows);
 assert.equal(rows.length,11631);
 assert.equal(new Set(rows.map(r=>r.id)).size,rows.length);
 const xml=await readFile(volume.txtPath,'utf8');
 assert.equal((xml.match(/<table /g)||[]).length,843);
});
test('HB21375 preserves diagram names outside tables without vocalizing short ordinary prayers as names',async()=>{
 const volume=JSON.parse(await readFile('data/rashash-text-21375.json','utf8'));
 const items=volume.pages.filter(p=>p.pdfPage>100).flatMap(p=>p.blocks.filter(b=>b.kind!=='table'));
 for(const text of ['צ צב צבא','א אד אדנ אדני','מם כף קץ','פאי','חתך','בם','שקוצית','לל שיד הויה','לל שיד הויה עבד ב׳','ההה ההה']){
  const matches=items.filter(i=>i.text===text);assert.ok(matches.length,text);
  assert.ok(matches.every(i=>i.html.includes('rashash-shem')),text);
 }
 const mixed=items.find(i=>i.text.endsWith(' יד י אן י'));
 assert.ok(mixed);assert.equal((mixed.html.match(/rashash-shem/g)||[]).length,4);
 assert.ok(/[\u05b0-\u05bd]/.test(mixed.text.split(' ')[0]));
 const prayer=items.find(i=>searchableHebrew(i.text)==='מחיה מתים');
 assert.ok(prayer);assert.ok(!prayer.html.includes('rashash-shem'));
 assert.ok(/[\u05b0-\u05bd]/.test(prayer.text));
});
test('HB21376 imports the Scanabgleich upload verbatim with stable IDs, tables and all open readings',async()=>{
 const index=JSON.parse(await readFile('data/rashash.json','utf8'));
 const metadata=index.documents.find(d=>d.id==='21376').transcription;
 const raw=await readFile(metadata.txtPath);
 assert.equal(createHash('sha256').update(raw).digest('hex'),'994f829fd4ddc93220353ae593475a4b9d41a16ea89dff9b40c1fbc303e5d1a6');
 const volume=JSON.parse(await readFile(metadata.jsonPath,'utf8'));
 assert.deepEqual(volume.pages.map(p=>p.pdfPage),[1,...Array.from({length:175},(_,i)=>i+3)]);
 let count=0,tables=0,rows=0;const ids=[];
 for(const page of volume.pages){
  let local=0;
  for(const block of page.blocks){
   if(block.kind==='table'){tables++;rows+=block.rows.length;}
   for(const item of block.kind==='table'?block.rows:[block]){
    ids.push(item.id);local+=(item.text.match(/\[\?\]/g)||[]).length;
    assert.match(item.id,new RegExp(`^HB21376-P${String(page.pdfPage).padStart(3,'0')}-T\\d{3}$`));
    if(item.text.includes('[?]'))assert.ok(item.html.includes('rashash-unclear'));
    assert.ok(!/<(?!\/?span\b)/i.test(item.html));
    assert.equal(stripHtml(item.html),item.text);
   }
  }
  assert.equal(page.flags.reduce((n,f)=>n+f.occurrences,0),local);count+=local;
 }
 assert.equal(new Set(ids).size,6118);assert.equal(ids.length,6118);
 assert.equal(count,143);assert.equal(tables,308);assert.equal(rows,4110);
 assert.equal(volume.provenance.automaticNiqqud.reviewed,'false');
 assert.equal(volume.provenance.contextReview['remaining-markers'],'143');
 const html=renderRashashReader({documents:index.documents,id:'21376',pageNumber:177,volume});
 assert.ok(html.includes('data-open-rashash="21376" data-page="177"'));
 assert.ok(html.includes('143 Lesestellen'));assert.ok(html.includes(metadata.txtPath));
 assert.ok(html.includes('Gelieferte Scanabgleich-TXT mit Niqqud und Tags'));
});
test('Jom Kippur preserves and exposes all 27 uncertain readings on their 19 source pages',async()=>{
 const volume=JSON.parse(await readFile('data/rashash-text-21722.json','utf8'));
 const original=(await readFile(volume.sourcePath,'utf8')).split(/\r?\n/);
 let count=0;const uncertainPages=[];
 for(const page of volume.pages){
  let occurrences=0;
  for(const block of page.blocks)for(const line of block.kind==='table'?block.rows:[block]){
   const matches=[...line.text.matchAll(/\[\?\]/g)];occurrences+=matches.length;
   const wordBeforeMarker=/([א-ת\u0591-\u05c7"'״׳]+)\s*\[\?\]/g;
   assert.deepEqual([...line.text.matchAll(wordBeforeMarker)].map(x=>x[1]),[...original[line.line-1].matchAll(wordBeforeMarker)].map(x=>x[1]));
   if(matches.length)assert.ok(line.html.includes('rashash-unclear'));
  }
  count+=occurrences;
  if(occurrences){uncertainPages.push(page.pdfPage);const flag=page.flags.find(f=>f.kind==='source_uncertainty');assert.equal(flag.occurrences,occurrences);}
 }
 assert.equal(count,27);assert.equal(uncertainPages.length,19);
 assert.equal(volume.pages.length,138);assert.ok(volume.pages.find(p=>p.pdfPage===132).flags.some(f=>f.kind==='service_cross_reference'));
 const xml=await readFile(volume.txtPath,'utf8');assert.equal((xml.match(/<unclear /g)||[]).length,27);
});
test('The checked Jom Kippur prayer distinguishes imperative mecheh from participle mocheh',async()=>{
 const volume=JSON.parse(await readFile('data/rashash-text-21722.json','utf8'));
 const text=volume.pages.find(p=>p.pdfPage===99).blocks.filter(b=>b.text).map(b=>b.text).join(' ');
 assert.ok(text.includes('מְחֵה וְהַעֲבֵר פְשָׁעֵנוּ מִנֶּגֶד עֵינֶיךָ'));
 assert.ok(text.includes('הוּא מֹחֶה'));
});
test('Text edition keeps review flags visible and links the exact TXT and scan page',async()=>{
 const index=JSON.parse(await readFile('data/rashash.json','utf8'));
 for(const id of ['21376','21375','21519','21520','21518','21722','21723']){
  const metadata=index.documents.find(d=>d.id===id).transcription;
  const volume=JSON.parse(await readFile(metadata.jsonPath,'utf8'));
  const page=metadata.flags.at(-1).pdfPages.at(-1);
  const html=renderRashashReader({documents:index.documents,id,pageNumber:page,volume,fontSize:32});
  assert.ok(html.includes(metadata.txtPath));assert.ok(html.includes(`data-open-rashash="${id}" data-page="${page}"`));
  assert.ok(html.includes('offene Prüfstelle'));assert.ok(html.includes('redaktionell zu prüfen'));
  assert.ok(html.includes('--reading-size:32px'));assert.ok(!html.includes('speak-section'));
 }
});
test('HB21519 keeps its own scan, all eight uncertain name pointings and the Shema name lists',async()=>{
 const volume=JSON.parse(await readFile('data/rashash-text-21519.json','utf8'));
 const original=(await readFile(volume.sourcePath,'utf8')).split(/\r?\n/);
 const uncertain=[];let count=0;const protectedLists=[];
 for(const page of volume.pages){
  let occurrences=0;
  for(const block of page.blocks)for(const line of block.kind==='table'?block.rows:[block]){
   occurrences+=(line.text.match(/\[\?\]/g)||[]).length;
   if(line.text.includes('[?]'))assert.ok(line.html.includes('rashash-unclear'));
   if(line.text.includes('שמות ע"ב מעל התיבות:')||line.text.includes('שמות מעל התיבות:')){
    assert.equal(line.text,original[line.line-1]);assert.ok(line.html.includes('rashash-shem'));protectedLists.push(line.text);
   }
   if(original[line.line-1]==='[אני חעם רהע ייז]'){
    assert.equal(line.text,original[line.line-1]);assert.equal((line.html.match(/rashash-shem/g)||[]).length,4);
   }
  }
  count+=occurrences;
  if(occurrences){uncertain.push(page.pdfPage);assert.equal(page.flags.find(f=>f.kind==='source_uncertainty').occurrences,occurrences);}
 }
 assert.equal(count,8);assert.deepEqual(uncertain,[21,23,49,51,63,65,69,71]);assert.equal(protectedLists.length,4);
 assert.equal(volume.pages.length,72);assert.equal(volume.id,'21519');
 const index=JSON.parse(await readFile('data/rashash.json','utf8'));
 const html=renderRashashReader({documents:index.documents,id:'21519',pageNumber:21,volume});
 assert.ok(html.includes('data-open-rashash="21519" data-page="21"'));
 assert.ok(html.includes(volume.txtPath));assert.ok(!html.includes('data-open-rashash="21520"'));
 const app=await readFile('src/app.js','utf8');assert.ok(!app.includes("doc.id==='21519'?'21520':doc.id"));
});
test('HB21519 contextual review distinguishes ordinary prayer words from symbolic names',async()=>{
 const volume=JSON.parse(await readFile('data/rashash-text-21519.json','utf8'));
 const text=n=>volume.pages.find(p=>p.pdfPage===n).blocks.filter(b=>b.text).map(b=>b.text).join(' ');
 assert.ok(text(3).includes('בּוֹאוּ וְנֵצֵא'));
 assert.ok(text(3).includes('בוה זו"ן'));assert.ok(!text(3).includes('בּוֹֽהַּ'));
 assert.ok(text(19).includes('קַבֵּל וּשְׁמַע'));
 assert.ok(text(42).includes('אֹתָם [א] לְאוֹת'));
 assert.ok(text(73).includes('וְגָלָה יְקָרֵנוּ. וְנִטַּל כָּבוֹד'));
});
test('Rashash text loader deduplicates requests, caches only matching volumes and retries failure',async()=>{
 let calls=0,fail=true;const metadata={id:'21520',jsonPath:'data/rashash-text-21520.json'};
 const store=new RashashTextStore(async()=>{calls++;if(fail)throw new Error('offline');return {ok:true,json:async()=>({id:'21520',pages:[{pdfPage:1}]})}});
 await assert.rejects(store.load(metadata),/offline/);fail=false;
 const [a,b]=await Promise.all([store.load(metadata),store.load(metadata)]);assert.equal(a,b);assert.equal(calls,2);
 await store.load(metadata);assert.equal(calls,2);
 const wrong=new RashashTextStore(async()=>({ok:true,json:async()=>({id:'21723',pages:[{}]})}));
 await assert.rejects(wrong.load(metadata),/gültigen/);assert.equal(wrong.get('21520'),undefined);
});
test('Rashash page selection falls back to an available content page, never the omitted scanner notice',async()=>{
 const volume=JSON.parse(await readFile('data/rashash-text-21520.json','utf8'));
 assert.ok(renderRashashPage(volume,2).includes('<span>PDF 1</span>'));
 assert.ok(renderRashashPage(volume,73).includes('<span>PDF 73</span>'));
});
