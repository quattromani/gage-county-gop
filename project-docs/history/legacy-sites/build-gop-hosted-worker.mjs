// Hosting adapter only: every response is generated from the canonical publication.
import fs from 'node:fs';
import path from 'node:path';
const root=path.resolve(import.meta.dirname,'..');
const input=path.join(root,'output/web/gop-card');
const dest=path.resolve(process.argv[2]||'output/web/hosted-server');
const types={'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.mjs':'text/javascript; charset=utf-8','.ics':'text/calendar; charset=utf-8','.json':'application/json','.webmanifest':'application/manifest+json','.png':'image/png','.webp':'image/webp','.pdf':'application/pdf'};
const files={};
function walk(dir){for(const entry of fs.readdirSync(dir,{withFileTypes:true})){const file=path.join(dir,entry.name);if(entry.isDirectory())walk(file);else if(entry.name!=='_headers'){const key='/'+path.relative(input,file).split(path.sep).join('/');files[key]={type:types[path.extname(file)]||'application/octet-stream',body:fs.readFileSync(file).toString('base64')};}}}walk(input);
fs.mkdirSync(dest,{recursive:true});
fs.writeFileSync(path.join(dest,'index.js'),`const files=${JSON.stringify(files)};\nexport default {fetch(request){const url=new URL(request.url);const key=url.pathname==='/'?'/index.html':url.pathname;const item=files[key];if(!item)return new Response('Not found',{status:404});if(!['GET','HEAD'].includes(request.method))return new Response('Method not allowed',{status:405,headers:{Allow:'GET, HEAD'}});const headers={'Content-Type':item.type,'Cache-Control':'public, max-age=0, must-revalidate'};if(key.endsWith('.ics'))headers['Content-Disposition']='inline; filename="'+key.split('/').pop()+'"';const body=request.method==='HEAD'?null:Uint8Array.from(atob(item.body),c=>c.charCodeAt(0));return new Response(body,{headers});}};\n`);
console.log('Built publication hosting adapter');
