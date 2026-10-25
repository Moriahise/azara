import test from 'node:test';
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {readFile} from 'node:fs/promises';
import {RashashTextStore,renderRashashReader,renderRashashPage,searchableHebrew} from '../src/rashash-reader.js';

test('All four Rashash editions retain every source letter, original vowel and all tables',()=>{
 const report=JSON.parse(execFileSync('python3',['scripts/validate-rashash.py'],{encoding:'utf8'}));
 assert.equal(report.reduce((n,v)=>n+v.pages,0),276);assert.equal(report.reduce((n,v)=>n+v.tables,0),690);
 assert.ok(report.every(v=>v.addedMarks>1000&&v.protectedTokens>100));
});
test('Rashash Hebrew search works with or without Niqqud and quote variants',()=>{
 assert.equal(searchableHebrew('שַׁבָּת'),searchableHebrew('שבת'));
 assert.equal(searchableHebrew('רש״ש'),searchableHebrew('רש"ש'));
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
 for(const id of ['21520','21518','21722','21723']){
  const metadata=index.documents.find(d=>d.id===id).transcription;
  const volume=JSON.parse(await readFile(metadata.jsonPath,'utf8'));
  const page=metadata.flags.at(-1).pdfPages.at(-1);
  const html=renderRashashReader({documents:index.documents,id,pageNumber:page,volume,fontSize:32});
  assert.ok(html.includes(metadata.txtPath));assert.ok(html.includes(`data-open-rashash="${id}" data-page="${page}"`));
  assert.ok(html.includes('offene Prüfstelle'));assert.ok(html.includes('redaktionell zu prüfen'));
  assert.ok(html.includes('--reading-size:32px'));assert.ok(!html.includes('speak-section'));
 }
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
