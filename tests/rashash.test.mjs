import test from 'node:test';
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {readFile} from 'node:fs/promises';
import {RashashTextStore,renderRashashReader,renderRashashPage,searchableHebrew} from '../src/rashash-reader.js';

test('All 138 Rashash pages retain every source letter, original vowel and all 274 tables',()=>{
 const report=JSON.parse(execFileSync('python3',['scripts/validate-rashash.py'],{encoding:'utf8'}));
 assert.equal(report.reduce((n,v)=>n+v.pages,0),138);assert.equal(report.reduce((n,v)=>n+v.tables,0),274);
 assert.ok(report.every(v=>v.addedMarks>1000&&v.protectedTokens>100));
});
test('Rashash Hebrew search works with or without Niqqud and quote variants',()=>{
 assert.equal(searchableHebrew('שַׁבָּת'),searchableHebrew('שבת'));
 assert.equal(searchableHebrew('רש״ש'),searchableHebrew('רש"ש'));
});
test('Text edition keeps review flags visible and links the exact TXT and scan page',async()=>{
 const index=JSON.parse(await readFile('data/rashash.json','utf8'));
 for(const id of ['21520','21518','21723']){
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
