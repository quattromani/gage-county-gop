import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import {restoreSelection,canMark} from '../src/publications/gage-gop-2026/web/selection.mjs';
const root=path.resolve(import.meta.dirname,'..'),out=path.join(root,'public/vote-2026');
const rows=[{id:'a',contest:'ward-1',limit:1},{id:'b',contest:'ward-1',limit:1},{id:'c',contest:'ward-2',limit:1},{id:'d',contest:'school',limit:2},{id:'e',contest:'school',limit:2},{id:'f',contest:'school',limit:2}];
test('single-seat limits are independent by ward, while multi-seat races respect their limit',()=>{let marked=new Set(['a','d']);assert.equal(canMark(marked,rows[1],rows),false);assert.equal(canMark(marked,rows[2],rows),true);assert.equal(canMark(marked,rows[4],rows),true);marked.add('e');assert.equal(canMark(marked,rows[5],rows),false);marked.delete('a');assert.equal(canMark(marked,rows[1],rows),true);});
test('restoration removes obsolete IDs, duplicates and over-limit marks; malformed storage is harmless',()=>{assert.deepEqual([...restoreSelection(['a','a','b','c','d','e','f','obsolete'],rows)],['a','c','d','e']);assert.equal(restoreSelection({bad:true},rows).size,0);});
const html=fs.readFileSync(path.join(out,'index.html'),'utf8');
test('publication contains exactly the source-derived Republican general-election inclusion set',()=>{const data=JSON.parse(fs.readFileSync(path.join(root,'src/data/elections/2026/election-directory.json')));const aff=new Map(data.affiliations.map(r=>[r.affiliationId,r]));const expected=data.candidacies.filter(r=>r.electionStageGroup==='current-general-election'&&aff.get(r.affiliationId).label==='Republican'&&aff.get(r.affiliationId).sourceId).map(r=>r.candidacyId).sort();const actual=[...html.matchAll(/type="checkbox" value="([^"]+)"/g)].map(m=>m[1]).sort();assert.deepEqual(actual,expected);assert.ok(!html.includes('COUNTY / CONTINUED'));assert.equal([...html.matchAll(/data-contest="office-beatrice-city-council:Ward [123]" data-limit="1"/g)].length,3);assert.ok(!html.includes('verificationDate'));});
test('download/manifest links are relative and reference real files; ICS includes all 5 dates with CRLF folding',()=>{for(const m of html.matchAll(/(?:href|src)="(\.\/[^"#]+)"/g))assert.ok(fs.existsSync(path.join(out,m[1])),m[1]);const manifest=JSON.parse(fs.readFileSync(path.join(out,'manifest.webmanifest')));assert.equal(manifest.scope,'./');assert.equal(manifest.start_url,'./');const ics=fs.readFileSync(path.join(out,'calendar/all-dates.ics'),'utf8');assert.equal((ics.match(/BEGIN:VEVENT/g)||[]).length,5);assert.equal((ics.match(/BEGIN:VALARM/g)||[]).length,5);assert.ok(ics.includes('DTSTART;VALUE=DATE:20261023'));assert.ok(ics.includes('DTEND;VALUE=DATE:20261024'));assert.ok(!ics.replaceAll('\r\n','').includes('\n'));for(const line of ics.split('\r\n'))assert.ok(Buffer.byteLength(line)<=75);});
function workerHarness(){const handlers={},store=new Map();let online=true,failSave=false;const scope='https://example.org/reference/gop-card/';const norm=k=>typeof k==='string'?k:k.url;const caches={async keys(){return [...store.keys()]},async delete(k){return store.delete(k)},async open(name){if(!store.has(name))store.set(name,new Map());const entries=store.get(name);return {async match(key){const r=entries.get(norm(key));return r?.clone();},async addAll(requests){if(failSave)throw Error('network failure');for(const req of requests)entries.set(req.url,new Response('saved:'+req.url));}}}};const self={registration:{scope},clients:{claim:async()=>{}},skipWaiting(){},addEventListener:(name,cb)=>handlers[name]=cb};vm.runInNewContext(fs.readFileSync(path.join(out,'sw.js'),'utf8'),{self,caches,URL,Request,Response,fetch:async req=>{if(!online)throw Error('offline');return new Response('network');}});return {store,async message(type){let promise,result;handlers.message({data:{type},ports:[{postMessage:r=>result=r}],waitUntil:p=>promise=p});await promise;return result;},async get(url,navigation=false){let response;handlers.fetch({request:{url,method:'GET',mode:navigation?'navigate':'cors'},respondWith:p=>response=p});return response?await response:null;},offline(){online=false;},failSave(){failSave=true;}};}
test('offline saving confirms only complete caches, supports subpaths and returns downloads offline',async()=>{const w=workerHarness();assert.equal((await w.message('STATUS')).ready,false);assert.equal((await w.message('SAVE')).ready,true);w.offline();const page=await w.get('https://example.org/reference/gop-card/',true);assert.equal(page.status,200);assert.match(await page.text(),/saved:/);const image=await w.get('https://example.org/reference/gop-card/assets/candidate-card.png');assert.equal(image.status,200);const absent=await w.get('https://example.org/reference/gop-card/absent');assert.equal(absent.status,503);assert.equal(await w.get('https://other.example/'),null);});
test('failed cache saving reports an error rather than false offline readiness',async()=>{const w=workerHarness();w.failSave();assert.match((await w.message('SAVE')).error,/failure/);assert.equal((await w.message('STATUS')).ready,false);});

test('saving a card preserves caches belonging to other publication locations',async()=>{const w=workerHarness();w.store.set('gage-gop-card-other-location',new Map());await w.message('SAVE');assert.ok(w.store.has('gage-gop-card-other-location'));});

test('calendar controls distinguish Apple subscription, Google creation and downloads',()=>{assert.match(html,/href="webcal:\/\/[^"]+all-dates\.ics"/);assert.ok(!html.includes('download>Add all dates to calendar'));const links=[...html.matchAll(/href="(https:\/\/calendar\.google\.com\/calendar\/render\?[^"]+)"/g)];assert.equal(links.length,5);const url=new URL(links[4][1].replaceAll('&amp;','&'));assert.equal(url.searchParams.get('dates'),'20261103/20261104');assert.equal(url.searchParams.get('ctz'),'America/Chicago');assert.match(url.searchParams.get('details'),/8 AM to 8 PM/);});

test('individual Apple events open inline instead of requesting a download',()=>{assert.equal([...html.matchAll(/href="\.\/calendar\/2026-[0-9-]+\.ics" aria-label="Open/g)].length,5);const headers=fs.readFileSync(path.join(out,'_headers'),'utf8');assert.match(headers,/Content-Type: text\/calendar/);assert.match(headers,/Content-Disposition: inline/);});

test('sticker download and offline copy are included after the footer',()=>{assert.ok(html.indexOf('id="voted"')>html.indexOf('</footer>'));assert.match(html,/download="gage-county-i-voted-2026.png"/);assert.ok(JSON.parse(fs.readFileSync(path.join(out,'build-info.json'))).assets.includes('./assets/sticker.png'));});
test('native sticker sharing sends the image only and handles cancellation and unsupported browsers',async()=>{const {shareSticker}=await import('../src/publications/gage-gop-2026/web/sticker-share.mjs');const file=new File(['image'],'sticker.png',{type:'image/png'});let payload;assert.equal(await shareSticker(file,{canShare:()=>true,share:async data=>{payload=data}}),'handed-off');assert.deepEqual(payload,{files:[file]});assert.equal(await shareSticker(file,{}),'unsupported');assert.equal(await shareSticker(file,{canShare:()=>true,share:async()=>{throw Object.assign(Error(),{name:'AbortError'})}}),'cancelled');});

test('parent links to the project and legacy subscriptions/downloads remain intact',()=>{
 const parent=path.dirname(out);
 const home=fs.readFileSync(path.join(parent,'index.html'),'utf8');
 assert.match(home,/href="\.\/vote-2026\/"/);
 assert.ok(!home.includes('data-contest='));
 assert.match(html,/webcal:\/\/quattromani\.github\.io\/gage-county-gop\/vote-2026\/calendar\/all-dates\.ics/);
 for(const dir of ['calendar','assets'])for(const file of fs.readdirSync(path.join(out,dir)))assert.deepEqual(fs.readFileSync(path.join(parent,dir,file)),fs.readFileSync(path.join(out,dir,file)));
 assert.match(fs.readFileSync(path.join(parent,'sw.js'),'utf8'),/registration\.unregister/);
});

test('social preview is crawlable static metadata with correct PNG dimensions',()=>{
 const image=html.match(/property="og:image" content="([^"]+)"/)[1];
 const url=new URL(image);
 assert.equal(url.origin,'https://quattromani.github.io');
 assert.equal(url.pathname,'/gage-county-gop/vote-2026/assets/facebook-preview.png');
 assert.match(html,/property="og:image:width" content="1200"/);
 assert.match(html,/property="og:image:height" content="630"/);
 for(const [file,w,h] of [['facebook-preview.png',1200,630],['facebook-post-square.png',1080,1080]]){
  const png=fs.readFileSync(path.join(out,'assets',file));
  assert.equal(png.toString('hex',0,8),'89504e470d0a1a0a');
  assert.equal(png.readUInt32BE(16),w);assert.equal(png.readUInt32BE(20),h);
  assert.ok(png.length<8000000);
 }
});

test('calendar defaults cover Apple and Android while unknown devices retain a chooser',async()=>{
 const {calendarChoice}=await import('../src/publications/gage-gop-2026/web/calendar-choice.mjs');
 for(const ua of ['iPhone','iPad','Macintosh'])assert.equal(calendarChoice(ua),'apple');
 assert.equal(calendarChoice('Linux Android 16'),'google');
 for(const ua of ['', 'Windows NT 10.0','Linux x86_64'])assert.equal(calendarChoice(ua),null);
 assert.equal((html.match(/class="calendar-choice"/g)||[]).length,5);
 assert.equal((html.match(/Add to calendar<span/g)||[]).length,5);
});
