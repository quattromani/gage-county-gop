import {shareSticker} from './sticker-share.mjs';
import {restoreSelection, canMark} from './selection.mjs';
const storageKey='gage-gop-2026-marks';
const inputs=[...document.querySelectorAll('.candidate input')];
const records=inputs.map(input=>({id:input.value,contest:input.closest('fieldset').dataset.contest,limit:Number(input.closest('fieldset').dataset.limit)}));
const status=document.querySelector('#selection-status'), filter=document.querySelector('#marked-only');
let canStore=true,saved=[];
try {saved=JSON.parse(localStorage.getItem(storageKey)||'[]');localStorage.setItem('gage-card-check','1');localStorage.removeItem('gage-card-check');} catch {canStore=false;}
let selected=restoreSelection(saved,records);
document.querySelectorAll('.js-only').forEach(el=>el.hidden=false);
inputs.forEach(input=>{input.disabled=false;input.checked=selected.has(input.value);});
function persist(){if(canStore)try{localStorage.setItem(storageKey,JSON.stringify([...selected]));}catch{canStore=false;}}
function announce(message){status.textContent=message||`${selected.size} marked. ${canStore?'Saved on this device only.':'Marks last for this session only; device storage is unavailable.'}`;status.classList.toggle('error',Boolean(message));}
function applyFilter(){
 for(const input of inputs)input.closest('label').hidden=filter.checked&&!input.checked;
 for(const office of document.querySelectorAll('.office'))office.hidden=filter.checked&&![...office.querySelectorAll('input')].some(i=>i.checked);
 for(const category of document.querySelectorAll('#candidates .category'))category.hidden=filter.checked&&![...category.querySelectorAll('.office')].some(o=>!o.hidden);
 document.querySelector('#empty-selection').hidden=!(filter.checked&&!selected.size);
}
inputs.forEach((input,index)=>input.addEventListener('change',()=>{
 const row=records[index];
 const office=input.closest("fieldset");
 let notice=office.querySelector(".contest-notice");
 if(!notice){notice=document.createElement("p");notice.className="contest-notice status error";office.append(notice);}
 notice.textContent="";
 if(input.checked&&!canMark(selected,row,records)){input.checked=false;notice.textContent=`You can mark up to ${row.limit}. Unmark a name first.`;announce(`You can mark up to ${row.limit} for ${office.querySelector("legend").textContent}. Unmark a name first.`);return;}
 if(input.checked)selected.add(row.id);else selected.delete(row.id);
 persist();applyFilter();announce();
}));
filter.addEventListener('change',applyFilter);
document.querySelector('#clear').addEventListener('click',()=>{selected.clear();document.querySelectorAll(".contest-notice").forEach(el=>el.textContent="");inputs.forEach(i=>i.checked=false);persist();applyFilter();announce();});
const jump=document.querySelector('#jump');jump.addEventListener('change',()=>{if(!jump.value)return;filter.checked=false;applyFilter();const target=document.getElementById(jump.value);target.scrollIntoView();target.querySelector('h2')?.focus({preventScroll:true});jump.value='';});
persist();announce();
let deferredPrompt;
const install=document.querySelector('#install');
window.addEventListener('beforeinstallprompt',event=>{event.preventDefault();deferredPrompt=event;install.hidden=false;});
install.addEventListener('click',async()=>{if(!deferredPrompt)return;await deferredPrompt.prompt();await deferredPrompt.userChoice;deferredPrompt=null;install.hidden=true;});
window.addEventListener('appinstalled',()=>install.hidden=true);
const offline=document.querySelector('#offline-status'),save=document.querySelector('#offline-save');
const savedLabel=document.querySelector('meta[name="card-version"]').content;
async function askWorker(type){
 const reg=await navigator.serviceWorker.ready;
 return new Promise((resolve,reject)=>{const channel=new MessageChannel();const timer=setTimeout(()=>reject(new Error('Saving took too long. Please try again.')),30000);channel.port1.onmessage=({data})=>{clearTimeout(timer);data.error?reject(new Error(data.error)):resolve(data);};reg.active.postMessage({type},[channel.port2]);});
}
if('serviceWorker' in navigator && window.isSecureContext){
 navigator.serviceWorker.register('./sw.js').then(async()=>{save.disabled=false;const info=await askWorker('STATUS');offline.textContent=info.ready?`Available offline · edition ${savedLabel}.`:'Save a copy for offline reading, including the image, PDFs, and calendar files.';}).catch(()=>{offline.textContent='Offline saving is unavailable here. You can still download the image or PDF.';});
 save.addEventListener('click',async()=>{save.disabled=true;offline.textContent='Saving the card and downloads…';try{await askWorker('SAVE');offline.textContent=`Available offline · edition ${savedLabel}. Your browser may remove saved files if storage is cleared.`;}catch(error){offline.textContent=`Could not finish saving. ${error.message}`;}finally{save.disabled=false;}});
}else offline.textContent='Offline saving needs HTTPS. The image and PDF can still be downloaded.';
window.addEventListener('offline',()=>{offline.textContent='You are offline. Previously saved content is available; external links need a connection.';});
const share=document.querySelector('#share');
share.addEventListener('click',async()=>{const url=new URL('./',location.href).href;try{if(navigator.share)await navigator.share({title:'Gage County GOP · 2026 Candidate Card',url});else{await navigator.clipboard.writeText(url);share.textContent='Link copied';}}catch(error){if(error.name!=='AbortError'){share.textContent='Copy the address from your browser';}}});

// Follow the permanent host automatically once the custom domain is connected.
if(location.protocol==='https:')document.querySelectorAll('[data-webcal]').forEach(link=>{const url=new URL('./calendar/'+link.dataset.webcal,location.href);url.protocol='webcal:';link.href=url.href;});

const stickerPanel=document.querySelector('#sticker-panel');
const revealSticker=document.querySelector('#sticker-reveal');
const stickerShare=document.querySelector('#sticker-share');
const stickerStatus=document.querySelector('#sticker-status');
stickerPanel.hidden=true;
let stickerFile;
revealSticker.addEventListener('click',()=>{
 stickerPanel.hidden=false;revealSticker.setAttribute('aria-expanded','true');revealSticker.hidden=true;
 document.querySelector('#sticker-message').focus({preventScroll:true});
 // Prepare the file before the separate Share tap, preserving iOS user activation.
 stickerShare.disabled=true;
 fetch('./assets/sticker.png').then(response=>{if(!response.ok)throw Error('Image unavailable');return response.blob();}).then(blob=>{
  stickerFile=new File([blob],'gage-county-i-voted-2026.png',{type:'image/png'});
  stickerShare.disabled=false;
 }).catch(()=>{stickerStatus.textContent='Sharing could not load. Open the sticker below to save it, or try again when connected.';});
});
stickerShare.addEventListener('click',async()=>{
 stickerShare.disabled=true;
 const result=await shareSticker(stickerFile,navigator);
 stickerShare.disabled=false;
 stickerStatus.textContent=result==='unsupported'||result==='failed'?'This browser could not share the image. Save it below, then attach it to your Facebook post or message.':result==='handed-off'?'Your phone handled the sharing request.':'Sharing canceled. Your sticker is still ready to save.';
});
