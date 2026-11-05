/* Human review UI. GitHub Pages keeps the existing comment workflow; a
   configured same-origin BFF enables GitHub App user-token decisions. */
(() => {
'use strict';
const esc=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const url=x=>{try{const u=new URL(x);return u.origin==='https://github.com'&&/^\/jea27\/Lut_generator\/(issues\/\d+|pull\/\d+|blob\/|commit\/)/.test(u.pathname)&&!u.username&&!u.password?u.href:null}catch{return null}};
const a=(x,label)=>url(x)?`<a class="external" href="${esc(url(x))}" target="_blank" rel="noopener noreferrer">${esc(label)} ↗</a>`:'';
const api=path=>new URL(path,new URL('./',location.href)).href;
let filter='pending';
const drafts=new Map();
let auth={mode:'unknown',csrf:null,error:null};
let authCheckedAt=0;
let authRequest=null;
const all=data=>[...(data?.features||[]),...(data?.review_demo?[data.review_demo]:[])];
const pending=f=>f.implemented&&!f.human_approved;
const state=f=>f.review?.state||'pending';
const names={pending:'Para revisar',approved:'Aprobado',changes_requested:'Correcciones solicitadas',needs_review:'Revisar nueva versión'};
const onPages=()=>location.hostname.endsWith('.github.io')||location.hostname==='localhost'||location.hostname==='127.0.0.1';

async function checkAuth(render,force=false){
 if(authRequest)return authRequest;
 if(!force&&auth.mode!=='unknown'&&Date.now()-authCheckedAt<45000)return auth;
 auth={mode:'checking',csrf:null,error:null};
 authRequest=(async()=>{
  try{
   const response=await fetch(api('api/auth/session'),{credentials:'same-origin',cache:'no-store',headers:{Accept:'application/json'}});
   const type=response.headers.get('Content-Type')||'';
   if(!type.toLowerCase().includes('application/json')){
    auth=onPages()?{mode:'manual',csrf:null,error:null}:{mode:'unavailable',csrf:null,error:'El servicio seguro no respondió.'};
   }else{
    const result=await response.json();
    if(result.enabled===false)auth={mode:'manual',csrf:null,error:null};
    else if(response.status===401)auth={mode:'direct',authenticated:false,csrf:null,error:null};
    else if(!response.ok)auth={mode:'unavailable',csrf:null,error:'No se pudo comprobar la sesión. Vuelve a intentarlo.'};
    else if(result.authenticated===true&&result.login==='jea27'&&typeof result.csrf==='string')auth={mode:'direct',authenticated:true,csrf:result.csrf,error:null};
    else if(result.enabled===true)auth={mode:'direct',authenticated:false,csrf:null,error:null};
    else auth={mode:'unavailable',csrf:null,error:'La configuración segura no está disponible.'};
   }
  }catch{auth=onPages()?{mode:'manual',csrf:null,error:null}:{mode:'unavailable',csrf:null,error:'No se pudo contactar con el servicio seguro.'};}
  authCheckedAt=Date.now();
  return auth;
 })().finally(()=>{authRequest=null;if(typeof render==='function')render()});
 return authRequest;
}

function authPanel(){
 if(auth.mode==='checking'||auth.mode==='unknown')return '<div class="notice">Comprobando el acceso seguro…</div>';
 if(auth.mode==='manual')return '<div class="notice notice-amber">Esta publicación aún usa el método autenticado de GitHub: prepara el comentario y publícalo con tu cuenta.</div>';
 if(auth.mode==='unavailable')return `<div class="notice notice-amber" role="alert">${esc(auth.error||'El servicio seguro no está disponible. No se ha registrado ninguna decisión.')}</div>`;
 if(auth.authenticated)return '<div class="notice">Sesión autenticada como <b>jea27</b>. Las decisiones se publican en GitHub y quedan sujetas a Actions.</div><button class="btn btn-outline" data-review-logout>Cerrar sesión</button>';
 return '<div class="notice">Inicia sesión una vez con GitHub para registrar decisiones desde Project OS.</div><button class="btn btn-accent" data-review-login>Iniciar sesión con GitHub</button>';
}

function queue(data){
 if(!data)return '<h1 class="h1">Mis revisiones</h1><p>Sin datos de revisión.</p>';
 let features=data.features.filter(f=>f.implemented);
 const count=features.filter(pending).length;
 features=features.filter(f=>filter==='all'||filter==='pending'&&pending(f)||state(f)===filter);
 const intro=auth.mode==='direct'?'Revisa la capacidad y su versión; confirma tu decisión en esta página.':'Revisa cada capacidad, completa sus comprobaciones y registra tu decisión.';
 return `<div class="eyebrow">ACEPTACIÓN HUMANA · JEa27</div><h1 class="h1">Mis <em>revisiones.</em></h1><p class="intro"><b>${count}</b> capacidades pendientes de aceptación. ${intro}</p><div class="notice notice-amber">Una aprobación se aplica solo a la capacidad y huella revisadas. No cierra tareas históricas ni autoriza distribuir la beta.</div>${authPanel()}<div class="product-filters" role="group" aria-label="Filtrar revisiones">${[['pending','Pendientes'],['changes_requested','Correcciones'],['needs_review','Nueva versión'],['approved','Aprobadas'],['all','Todas']].map(([id,label])=>`<button class="btn ${filter===id?'btn-accent':'btn-outline'}" data-review-filter="${id}" aria-pressed="${filter===id}">${label}</button>`).join('')}</div><div class="product-features">${features.map(f=>`<article class="product-feature"><div class="product-feature-head"><h3>${esc(f.title)}</h3><span class="product-badge ${state(f)==='approved'?'approved':'review'}">${esc(names[state(f)]||'Para revisar')}</span></div><p>${esc(f.acceptance)}</p><p class="list-muted">${f.technically_verified?'Verificada técnicamente':'Verificación técnica pendiente'} · ${f.human_approved?'Aceptada por jea27':'Aceptación humana pendiente'}</p>${button(f)}</article>`).join('')||'<p>No hay elementos en este filtro.</p>'}</div><section class="panel"><h3>Probar el flujo sin aprobar producto</h3><p class="panel-intro">Demostración sintética independiente de las métricas y funcionalidades reales.</p>${data.review_demo?`<p>Estado QA: ${esc(names[state(data.review_demo)]||'Pendiente')}</p>${button(data.review_demo)}`:'<p>Sin datos de demostración.</p>'}</section>`;
}

function button(f){return `<button class="btn btn-accent" data-review-feature="${esc(f.id)}" ${f.review?.context?'':'disabled'}>Revisar${f.demo?' demostración':''}</button>${f.review?.context?'':'<small>La versión revisable aún no está disponible; actualiza el dashboard.</small>'}`;}

function open(f,data,render){
 let dialog=document.getElementById('feature-review-dialog');if(dialog)dialog.remove();
 dialog=document.createElement('dialog');dialog.id='feature-review-dialog';dialog.className='review-dialog';
 const context=f.review.context;const draft=drafts.get(f.id)||{checked:[],notes:'',idempotencyKey:null};
 const direct=auth.mode==='direct';const manual=auth.mode==='manual';
  dialog.innerHTML=`<form method="dialog"><button class="review-close" aria-label="Cerrar revisión">×</button></form><div class="eyebrow">${f.demo?'DEMOSTRACIÓN SINTÉTICA · NO APRUEBA PRODUCTO':'REVISIÓN INDIVIDUAL'}</div><h2>${esc(f.title)}</h2><p>${esc(f.acceptance)}</p><p class="list-muted">Versión ${esc(context.version)} · commit ${esc(context.commit.slice(0,7))}<br>Huella <code>${esc(context.revision.slice(0,16))}</code></p>${data.reviews_active===false?'<p class="notice notice-amber">Workflow pendiente de integración. Esta vista no activa aprobaciones reales.</p>':''}${direct&&!auth.authenticated?'<button class="btn btn-accent" data-review-login-modal>Iniciar sesión con GitHub</button>':''}<h3>Cómo probarlo</h3><ol>${(f.review_steps||[]).map(step=>`<li>${esc(step)}</li>`).join('')}</ol><div class="product-links">${a(f.issue_url,'Issue')}${a(f.pr_url,'PR')}${a(`https://github.com/jea27/Lut_generator/commit/${context.commit}`,'Versión revisada')}${(f.evidence||[]).map(e=>a(e.url,e.label)).join('')}</div><h3>Mis comprobaciones</h3><div class="review-checks">${(f.checklist||[]).map(check=>`<label><input type="checkbox" value="${esc(check.id)}" ${draft.checked.includes(check.id)?'checked':''}><span>${esc(check.label)}</span></label>`).join('')}</div><label class="review-notes">Observaciones (obligatorias al pedir cambios)<textarea id="review-observations" maxlength="2000" placeholder="Describe un fallo reproducible sin datos personales ni fotos privadas.">${esc(draft.notes)}</textarea></label><p class="list-muted">La decisión y las observaciones se publican en la Issue de GitHub. No añadas datos personales, credenciales ni fotografías.</p><div class="review-actions"><button class="btn btn-accent" id="review-approve">Aprobar</button><button class="btn btn-outline" id="review-changes">Pedir cambios</button></div><p id="review-message" role="status" aria-live="polite"></p><section id="review-export" ${direct?'hidden':''}><h3>Publicar decisión en GitHub</h3><p>1. Copia el mensaje y abre la Issue. 2. Pégalo y publícalo con <b>jea27</b>. Actions comprobará tu cuenta, versión y checklist.</p><textarea id="review-payload" readonly aria-label="Comentario estructurado"></textarea><a class="btn btn-accent" id="review-copy-open" href="${esc(url(f.issue_url)||'#')}#new_comment_field" target="_blank" rel="noopener noreferrer">Copiar y abrir Issue</a><p id="review-copy-status" role="status"></p></section><section id="review-direct-confirm" hidden><h3>Confirmar decisión</h3><p id="review-confirm-summary"></p><p>Se añadirá un comentario público a la Issue. Después, GitHub Actions validará la revisión y actualizará el dashboard.</p><button class="btn btn-accent" id="review-submit">Confirmar y registrar en GitHub</button></section><section id="review-direct-result" hidden><h3>Decisión registrada</h3><p id="review-result-text"></p></section><details><summary>Historial y versiones anteriores (${(f.review.history||[]).length})</summary><ul>${(f.review.history||[]).map(h=>`<li>${esc(h.at)} · ${esc(h.reviewer)} · ${esc(h.decision)} · ${esc(h.version)} / ${esc((h.commit||'').slice(0,7))} ${h.source_valid?'':'(comentario retirado/editado)'} ${a(h.url,'Decisión y observaciones')}</li>`).join('')||'<li>Sin decisiones registradas.</li>'}</ul></details>`;
 document.body.appendChild(dialog);dialog.showModal();
 const save=()=>{const saved={checked:Array.from(dialog.querySelectorAll('.review-checks input:checked')).map(input=>input.value),notes:dialog.querySelector('#review-observations').value,idempotencyKey:drafts.get(f.id)?.idempotencyKey||null};drafts.set(f.id,saved);return saved;};
 dialog.addEventListener('input',()=>{const current=save();current.idempotencyKey=null;drafts.set(f.id,current);dialog.querySelector('#review-export').hidden=true;dialog.querySelector('#review-direct-confirm').hidden=true;dialog.querySelector('#review-direct-result').hidden=true;dialog.querySelector('#review-message').textContent='Prepara de nuevo la decisión tras cambiar las comprobaciones.';});
 dialog.addEventListener('close',()=>{save();dialog.remove();});
 function prepare(decision){
  const current=save();const message=dialog.querySelector('#review-message');
  if(decision==='approve'&&current.checked.length!==(f.checklist||[]).length){message.textContent='Completa todas las comprobaciones para aprobar.';return;}
  if(decision==='changes'&&!current.notes.trim()){message.textContent='Describe las correcciones que necesitas.';return;}
  if(!f.demo&&data.reviews_active===false){message.textContent='La aprobación real requiere activar el workflow integrado.';return;}
  const payload={feature:f.id,revision:context.revision,commit:context.commit,version:context.version,decision,checklist:current.checked,notes:current.notes};
  if(auth.mode==='unavailable'||auth.mode==='checking'||auth.mode==='unknown'){
   message.textContent=auth.error||'No se ha podido comprobar la autenticación. No se registró ninguna decisión.';return;
  }
  if(direct){
   if(!auth.authenticated){message.textContent='Inicia sesión con GitHub antes de enviar la decisión.';return;}
   if(!current.idempotencyKey){current.idempotencyKey=crypto.randomUUID();drafts.set(f.id,current);}
   dialog.querySelector('#review-confirm-summary').textContent=`${decision==='approve'?'Aprobar':'Pedir cambios para'} ${f.title}, versión ${context.version}, commit ${context.commit.slice(0,7)}.`;
   dialog.querySelector('#review-direct-confirm').hidden=false;dialog.querySelector('#review-export').hidden=true;
   message.textContent='Comprueba la capacidad y la versión. El siguiente botón confirma tu decisión.';return;
  }
  if(!manual){message.textContent='El método de decisión no está disponible. No se registró ninguna acción.';return;}
  dialog.querySelector('#review-payload').value='LUMAFORGE_REVIEW_V1\n```json\n'+JSON.stringify(payload,null,2)+'\n```';
  dialog.querySelector('#review-export').hidden=false;message.textContent='Decisión preparada; todavía no se ha enviado ni aprobado nada.';
 }
 async function submit(){
  const current=drafts.get(f.id);const message=dialog.querySelector('#review-message');const submitButton=dialog.querySelector('#review-submit');
  if(!current?.idempotencyKey||!auth.csrf)return;
  submitButton.disabled=true;message.textContent='Enviando decisión autenticada a GitHub…';
  const payload={feature:f.id,revision:context.revision,commit:context.commit,version:context.version,
    decision:dialog.querySelector('#review-confirm-summary').textContent.startsWith('Aprobar')?'approve':'changes',
    checklist:current.checked,notes:current.notes};
  try{
   const response=await fetch(api(`api/reviews/${encodeURIComponent(f.id)}/decision`),{method:'POST',credentials:'same-origin',cache:'no-store',headers:{'Content-Type':'application/json','X-LumaForge-CSRF':auth.csrf,'Idempotency-Key':current.idempotencyKey},body:JSON.stringify(payload)});
   const result=await response.json();
   if(response.status===202){message.textContent='GitHub está terminando de registrar esta petición. Espera unos segundos y confirma de nuevo para consultar el mismo envío seguro.';submitButton.disabled=false;return;}
   if(!response.ok){
    const errors={review_version_changed:'La versión o los criterios cambiaron. Recarga el dashboard y vuelve a revisar.',session_expired:'Tu sesión caducó. Inicia sesión de nuevo.',csrf_rejected:'La sesión de seguridad caducó. Recarga la página.',github_unavailable:'GitHub no está disponible. No se registró una aprobación; puedes reintentar de forma segura.',rate_limited:'Has enviado varias peticiones seguidas. Espera un minuto antes de reintentar.',feature_not_pending:'Esta capacidad ya no está pendiente de revisión.'};
    if(result.error==='session_expired'){auth={mode:'direct',authenticated:false,csrf:null,error:null};}
    message.textContent=errors[result.error]||'No se pudo registrar la decisión. No se ha mostrado como aprobada.';submitButton.disabled=false;return;
   }
   dialog.querySelector('#review-direct-confirm').hidden=true;
   const resultSection=dialog.querySelector('#review-direct-result');resultSection.hidden=false;
   dialog.querySelector('#review-result-text').innerHTML=`${result.decision==='approve'?'Aprobación':'Solicitud de cambios'} registrada para esta capacidad. GitHub Actions y el sincronizador deben validar y publicar el nuevo estado.${result.comment?.url?` ${a(result.comment.url,'Ver registro de auditoría')}`:''}`;
   message.textContent='GitHub recibió tu decisión. El dashboard se actualizará tras terminar Actions y el sincronizador.';
   submitButton.disabled=false;
  }catch{
   message.textContent='No se pudo confirmar la respuesta del servidor. Reintentar con esta misma decisión no duplicará el comentario.';submitButton.disabled=false;
  }
 }
 dialog.querySelector('#review-approve').onclick=()=>prepare('approve');
 dialog.querySelector('#review-changes').onclick=()=>prepare('changes');
 dialog.querySelector('[data-review-login-modal]')?.addEventListener('click',()=>location.assign(api('api/auth/github/start')));
 dialog.querySelector('#review-submit')?.addEventListener('click',submit);
 dialog.querySelector('#review-copy-open')?.addEventListener('click',()=>{
  const payload=dialog.querySelector('#review-payload');
  if(navigator.clipboard?.writeText)navigator.clipboard.writeText(payload.value).then(()=>{dialog.querySelector('#review-copy-status').textContent='Copiado. Pega y publica en GitHub con jea27.'}).catch(()=>{payload.focus();payload.select();dialog.querySelector('#review-copy-status').textContent='Copia el texto seleccionado y pégalo en GitHub.'});
  else{payload.focus();payload.select();dialog.querySelector('#review-copy-status').textContent='Copia el texto seleccionado y pégalo en GitHub.'}
 });
}

function bind(data,render){
 document.querySelectorAll('[data-review-filter]').forEach(button=>button.addEventListener('click',()=>{filter=button.dataset.reviewFilter;render();}));
 document.querySelectorAll('[data-review-feature]').forEach(button=>button.addEventListener('click',async()=>{await checkAuth(render);const feature=all(data).find(item=>item.id===button.dataset.reviewFeature);if(feature?.review?.context)open(feature,data,render);}));
 document.querySelectorAll('[data-review-login]').forEach(button=>button.addEventListener('click',()=>{location.assign(api('api/auth/github/start'));}));
 document.querySelectorAll('[data-review-logout]').forEach(button=>button.addEventListener('click',async()=>{
  button.disabled=true;
  try{
   const response=await fetch(api('api/auth/logout'),{method:'POST',credentials:'same-origin',cache:'no-store',headers:{'X-LumaForge-CSRF':auth.csrf||''}});
   if(!response.ok)throw new Error();
   auth={mode:'direct',authenticated:false,csrf:null,error:null};authCheckedAt=Date.now();render();
  }catch{auth={mode:'unavailable',csrf:null,error:'No se pudo cerrar la sesión de forma segura. Vuelve a intentarlo.'};authCheckedAt=Date.now();render();}
 }));
 if(document.querySelector('[data-review-feature]'))checkAuth(render);
}
window.LumaForgeReview={queue,button,bind};
})();
