import {build} from 'esbuild';
import {mkdir,rm,cp,readFile,writeFile,readdir} from 'node:fs/promises';
import {existsSync} from 'node:fs';
import path from 'node:path';
await rm('dist',{recursive:true,force:true});await mkdir('dist/assets',{recursive:true});
await build({entryPoints:['src/app.js'],bundle:true,minify:true,format:'esm',outfile:'dist/assets/app.js',target:'es2022',legalComments:'eof'});
await cp('public/index.html','dist/index.html');await cp('src/style.css','dist/assets/style.css');
await mkdir('dist/data',{recursive:true});
const txt=await readFile('Shaliehsaboo Edition.txt','utf8');
const re=/<big><b>(.*?)<\/b><\/big>/gs;const matches=[...txt.matchAll(re)];
const sections=matches.map((m,i)=>({id:i,title:m[1].replace(/<[^>]*>/g,'').trim(),html:txt.slice(m.index+m[0].length,matches[i+1]?.index??txt.length).replace(/<\/?(?!b\b|small\b|br\b|big\b|i\b|strong\b)[a-z][^>]*>/gi,'').replace(/<(b|small|br|big|i|strong)\b[^>]*>/gi,'<$1>')}));
await writeFile('dist/data/siddur.json',JSON.stringify(sections));
for(const f of await readdir('data')) if(f.endsWith('.json')) await cp('data/'+f,'dist/data/'+f);
// User supplied recordings and scans remain at their original repository paths.
// The build preserves them verbatim for GitHub Pages. Sparse local checkouts use raw links.
const assets=JSON.parse(await readFile('data/repository-assets.json','utf8'));
for(const a of assets){if(!existsSync(a.path))continue;await mkdir(path.dirname('dist/'+a.path),{recursive:true});await cp(a.path,'dist/'+a.path);}
await cp('docs','dist/docs',{recursive:true});
await writeFile('dist/.nojekyll','');
console.log(`Built Azara: ${sections.length} Siddur sections, ${assets.length} original source assets.`);
