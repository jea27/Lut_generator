/* Pages never authenticates with a token: user posts the copied decision on GitHub. */
(() => {
'use strict';
const esc=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const url=x=>{try{const u=new URL(x);return u.origin==='https://github.com'&&/^\/jea27\/Lut_generator\/(issues\/\d+|pull\/\d+|blob\/|commit\/)/.test(u.pathname)&&!u.username&&!u.password?u.href:null}catch{return null}};
const a=(x,label)=>url(x)?`<a class="external" href="${esc(url(x))}" target="_blank" rel="noopener noreferrer">${esc(label)} ↗</a>`:'';
let filter='pending';
const drafts=new Map();
const all=data=>[...(data?.features||[]),...(data?.review_demo?[data.review_demo]:[])];
const pending=f=>f.implemented&&!f.human_approved;
const state=f=>f.review?.state||'pending';
const names={pending:'Para revisar',approved:'Aprobado',changes_requested:'Correcciones solicitadas',needs_review:'Revisar nueva versión'};
function queue(data){
 if(!data)return '<h1 class="h1">Mis revisiones</h1><p>Sin datos de revisión.</p>';
 let features=data.features.filter(f=>f.implemented);
 const count=features.filter(pending).length;
 features=features.filter(f=>filter==='all'||filter==='pending'&&pending(f)||state(f)===filter);
 return `<div class="eyebrow">ACEPTACIÓN HUMANA · JEa27</div><h1 class="h1">Mis <em>revisiones.</em></h1><p class="intro">${count} capacidades pendientes de aceptación. Prueba cada una, completa sus comprobaciones y publica tu decisión en GitHub.</p><div class="notice notice-amber">Una aprobación se aplica solo a la capacidad y huella revisadas. No cierra tareas históricas ni autoriza distribuir la beta.</div><div class="product-filters">${[['pending','Pendientes'],['changes_requested','Correcciones'],['needs_review','Nueva versión'],['approved','Aprobadas'],['all','Todas']].map(([id,label])=>`<button class="btn ${filter===id?'btn-accent':'btn-outline'}" data-review-filter="${id}" aria-pressed="${filter===id}">${label}</button>`).join('')}</div><div class="product-features">${features.map(f=>`<article class="product-feature"><div class="product-feature-head"><h3>${esc(f.title)}</h3><span class="product-badge ${state(f)==='approved'?'approved':'review'}">${esc(names[state(f)])}</span></div><p>${esc(f.acceptance)}</p><p class="list-muted">${f.technically_verified?'Verificada técnicamente':'Verificación técnica pendiente'} · ${f.human_approved?'Aceptada por jea27':'Aceptación humana pendiente'}</p>${button(f)}</article>`).join('')||'<p>No hay elementos en este filtro.</p>'}</div><section class="panel"><h3>Probar el flujo sin aprobar producto</h3><p class="panel-intro">Demostración sintética independiente de las métricas y funcionalidades reales.</p>${data.review_demo?`<p>Estado QA: ${esc(names[state(data.review_demo)])}</p>${button(data.review_demo)}`:'<p>Sin datos de demostración.</p>'}</section>`;
}
function button(f){return `<button class="btn btn-accent" data-review-feature="${esc(f.id)}" ${f.review?.context?'':'disabled'}>Revisar${f.demo?' demostración':''}</button>${f.review?.context?'':'<small>La versión revisable aún no está disponible; actualiza el dashboard.</small>'}`}
function open(f,data){
 let dialog=document.getElementById('feature-review-dialog');if(dialog)dialog.remove();
 dialog=document.createElement('dialog');dialog.id='feature-review-dialog';dialog.className='review-dialog';
 const c=f.review.context;const d=drafts.get(f.id)||{checked:[],notes:''};
 dialog.innerHTML=`<form method="dialog"><button class="review-close" aria-label="Cerrar revisión">×</button></form><div class="eyebrow">${f.demo?'DEMOSTRACIÓN SINTÉTICA · NO APRUEBA PRODUCTO':'REVISIÓN INDIVIDUAL'}</div><h2>${esc(f.title)}</h2><p>${esc(f.acceptance)}</p><p class="list-muted">Versión ${esc(c.version)} · commit ${esc(c.commit.slice(0,7))}<br>Huella <code>${esc(c.revision.slice(0,16))}</code></p>${data.reviews_active===false?'<p class="notice notice-amber">Workflow pendiente de integración. Esta previsualización no activa aprobaciones reales; la demostración se procesa por separado.</p>':''}<h3>Cómo probarlo</h3><ol>${f.review_steps.map(s=>`<li>${esc(s)}</li>`).join('')}</ol><div class="product-links">${a(f.issue_url,'Issue')}${a(f.pr_url,'PR')}${a(`https://github.com/jea27/Lut_generator/commit/${c.commit}`,'Versión revisada')}${(f.evidence||[]).map(e=>a(e.url,e.label)).join('')}</div><h3>Mis comprobaciones</h3><div class="review-checks">${f.checklist.map(ch=>`<label><input type="checkbox" value="${esc(ch.id)}" ${d.checked.includes(ch.id)?'checked':''}><span>${esc(ch.label)}</span></label>`).join('')}</div><label class="review-notes">Observaciones (obligatorias al pedir cambios)<textarea id="review-observations" maxlength="2000" placeholder="Describe un fallo reproducible sin datos personales ni fotos privadas.">${esc(d.notes)}</textarea></label><p class="list-muted">El comentario será público en GitHub. No añadas datos personales, credenciales ni fotografías. El dashboard conserva un enlace a tus observaciones, sin copiar su texto.</p><div class="review-actions"><button class="btn btn-accent" id="review-approve">Aprobar</button><button class="btn btn-outline" id="review-changes">Pedir cambios</button></div><p id="review-message" role="status"></p><section id="review-export" hidden><h3>Publicar decisión autenticada</h3><p>1. Copia el mensaje y abre la Issue. 2. Pégalo en «Añadir comentario» y publícalo con <b>jea27</b>. Actions comprobará tu cuenta, versión y checklist; después se actualizará la web.</p><textarea id="review-payload" readonly aria-label="Comentario estructurado"></textarea><a class="btn btn-accent" id="review-copy-open" href="${esc(url(f.issue_url)||'#')}#new_comment_field" target="_blank" rel="noopener noreferrer">Copiar y abrir Issue</a><p id="review-copy-status" role="status"></p></section><details><summary>Historial y versiones anteriores (${f.review.history.length})</summary><ul>${f.review.history.map(h=>`<li>${esc(h.at)} · ${esc(h.reviewer)} · ${esc(h.decision)} · ${esc(h.version)} / ${esc(h.commit.slice(0,7))} ${h.source_valid?'':'(comentario retirado/editado)'} ${a(h.url,'Decisión y observaciones')}</li>`).join('')||'<li>Sin decisiones registradas.</li>'}</ul></details>`;
 document.body.appendChild(dialog);dialog.showModal();
 const save=()=>{const draft={checked:Array.from(dialog.querySelectorAll('.review-checks input:checked')).map(c=>c.value),notes:dialog.querySelector('#review-observations').value};drafts.set(f.id,draft);return draft};
 dialog.addEventListener('input',()=>{save();dialog.querySelector('#review-export').hidden=true;dialog.querySelector('#review-message').textContent='Prepara de nuevo la decisión tras cambiar las comprobaciones.'});dialog.addEventListener('close',()=>{save();dialog.remove()});
 function prepare(decision){const draft=save();const msg=dialog.querySelector('#review-message');
  if(decision==='approve'&&draft.checked.length!==f.checklist.length){msg.textContent='Completa todas las comprobaciones para aprobar.';return}
  if(decision==='changes'&&!draft.notes.trim()){msg.textContent='Describe las correcciones que necesitas.';return}
  if(!f.demo&&data.reviews_active===false){msg.textContent='La aprobación real requiere integrar y activar este workflow primero.';return}
  const payload={feature:f.id,revision:c.revision,commit:c.commit,version:c.version,decision,checklist:draft.checked,notes:draft.notes};
  dialog.querySelector('#review-payload').value='LUMAFORGE_REVIEW_V1\n```json\n'+JSON.stringify(payload,null,2)+'\n```';
  dialog.querySelector('#review-export').hidden=false;msg.textContent='Decisión preparada; todavía no se ha enviado ni aprobado nada.';
 }
 dialog.querySelector('#review-approve').onclick=()=>prepare('approve');dialog.querySelector('#review-changes').onclick=()=>prepare('changes');
 dialog.querySelector('#review-copy-open').onclick=()=>{
  const payload=dialog.querySelector('#review-payload');
  if(navigator.clipboard?.writeText)navigator.clipboard.writeText(payload.value).then(()=>{dialog.querySelector('#review-copy-status').textContent='Copiado. Pega y publica en GitHub con jea27.'}).catch(()=>{payload.focus();payload.select();dialog.querySelector('#review-copy-status').textContent='Copia el texto seleccionado y pégalo en GitHub.'});
  else{payload.focus();payload.select();dialog.querySelector('#review-copy-status').textContent='Copia el texto seleccionado y pégalo en GitHub.'}
 };
}
function bind(data,render){document.querySelectorAll('[data-review-filter]').forEach(b=>b.onclick=()=>{filter=b.dataset.reviewFilter;render()});document.querySelectorAll('[data-review-feature]').forEach(b=>b.onclick=()=>{const f=all(data).find(f=>f.id===b.dataset.reviewFeature);if(f?.review?.context)open(f,data)})}
window.LumaForgeReview={queue,button,bind};
})();
