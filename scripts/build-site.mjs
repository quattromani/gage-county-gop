import fs from 'node:fs';
import path from 'node:path';
const root=path.resolve(import.meta.dirname,'..');
const out=path.join(root,'public');
// public/ is generated; rebuild it so obsolete files cannot leak into releases.
fs.rmSync(out,{recursive:true,force:true});
await import('./build-gop-web-card.mjs');
fs.copyFileSync(path.join(root,'src/site/index.html'),path.join(out,'index.html'));
fs.copyFileSync(path.join(root,'src/site/sw.js'),path.join(out,'sw.js'));
// Preserve already-shared downloads and existing calendar subscriptions.
for(const dir of ['calendar','assets'])fs.cpSync(path.join(out,'vote-2026',dir),path.join(out,dir),{recursive:true});
