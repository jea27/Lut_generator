<script setup lang="ts">
import {computed,ref,watch} from 'vue'
import {useQuasar} from 'quasar'
import {api,jsonPost} from './api'
import {tx} from './i18n'
const props=defineProps<{referenceId:string|null;referenceUrl:string;recipe:unknown}>()
const emit=defineEmits(['back'])
const q=useQuasar()
type Node={id:string;label:string;x:number;y:number;enabled:boolean}
type Plan={schema:string;setup:unknown;diagram:{nodes:Node[]};sections:Record<string,{kind:string;title:string;detail:string;source_ids:string[];uncertainty:string|null}[]>;equipment:Record<string,string[]>;checklist:{id:string;text:string;checked:boolean}[];sources:{id:string;title:string;url:string;verified_on:string}[];limits:string[];recipe:unknown}
const setup=ref({shot:'medium',key_side:'left',softness:'soft',contrast:'medium',sensor_width_mm:36,focal_mm:null as number|null,aperture:4,fps:25,shutter_angle:180,white_balance_k:5600,camera_height_m:1.5,movement:'locked'})
const report=ref<Plan|null>(null),busy=ref(false),error=ref(''),selected=ref('key'),stale=ref(false),elapsed=ref(0)
const selectedNode=computed(()=>report.value?.diagram.nodes.find(n=>n.id===selected.value))
const editsKey=()=>JSON.stringify({diagram:report.value?.diagram,checklist:report.value?.checklist})
let initialEdits=''
const kindLabel:Record<string,string>={observation:'Observación medida',estimate:'Estimación / sin confirmar',recommendation:'Recomendación de LumaForge',source_confirmed:'Cálculo con fuente técnica'}
const sectionLabel:Record<string,string>={composition:'Composición',lighting:'Iluminación',camera:'Cámara',postproduction:'Postproducción'}
const position=(v:number)=>250+v*40
async function generate(){
 if(busy.value||!props.referenceId)return
 if(report.value&&initialEdits!==editsKey()){
  q.dialog({title:tx('¿Regenerar la propuesta?','Regenerate proposal?'),message:tx('Se reiniciarán tus cambios del diagrama y la checklist. Cancela para guardar el plan JSON antes de continuar.','Your diagram and checklist edits will be reset. Cancel to save the plan JSON before continuing.'),cancel:true,persistent:true}).onOk(()=>generateConfirmed())
  return
 }
 await generateConfirmed()
}
async function generateConfirmed(){
 if(busy.value||!props.referenceId)return
 const key=JSON.stringify({reference:props.referenceId,setup:setup.value,recipe:props.recipe})
 busy.value=true;error.value=''
 try{const response=await(await api('/planner',jsonPost({reference_id:props.referenceId,setup:setup.value,recipe:props.recipe}))).json();report.value=response.plan;initialEdits=editsKey();elapsed.value=response.metrics.wall_ms;stale.value=key!==JSON.stringify({reference:props.referenceId,setup:setup.value,recipe:props.recipe})}
 catch(e){error.value=(e as Error).message}finally{busy.value=false}
}
function download(){
 if(!report.value||stale.value)return
 const blob=new Blob([JSON.stringify(report.value,null,2)],{type:'application/json'})
 const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='lumaforge-shot-plan.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),60000)
}
watch(()=>props.referenceId,()=>{report.value=null;stale.value=false})
watch([setup,()=>props.recipe],()=>{if(report.value)stale.value=true},{deep:true})
</script>
<template>
 <main class="shot-planner">
  <header class="planner-header"><div><span class="small-kicker">PRO · EXPERIMENTAL · LOCAL</span><h1>Cinematic Shot Planner</h1><p>{{tx('Una propuesta de rodaje, con límites visibles.','A shooting proposal with visible limits.')}}</p></div><q-btn flat :label="tx('Volver al color','Back to colour')" icon="arrow_back" @click="emit('back')"/></header>
  <q-banner class="planner-limit">{{tx('La foto no revela con certeza la cámara, óptica, luces ni exposición originales. Esta versión mide píxeles y propone un montaje según tus elecciones; no reconoce automáticamente sujetos o luces.','A photograph does not reveal the original camera, lens, lighting or exposure with certainty. This version measures pixels and proposes a setup from your choices; it does not automatically recognize subjects or lights.')}}</q-banner>
  <div v-if="!referenceId" class="planner-empty"><p>{{tx('Importa una referencia JPG/PNG en el editor o usa la demo CC0.','Import a JPG/PNG reference in the editor or use the CC0 demo.')}}</p><q-btn color="primary" text-color="dark" :label="tx('Importar en el editor','Import in editor')" @click="emit('back')"/></div>
  <div v-else class="planner-grid">
   <section class="planner-settings"><img :src="referenceUrl" :alt="tx('Referencia local para la propuesta','Local planning reference')"><h2>{{tx('Tus elecciones de rodaje','Your shooting choices')}}</h2><p>{{tx('Son propuestas editables, no valores detectados en la referencia.','Editable proposals, not values detected in the reference.')}}</p>
    <label>{{tx('Escala de plano','Shot scale')}}<select v-model="setup.shot"><option value="wide">General / Wide</option><option value="medium">Medio / Medium</option><option value="close">Primer plano / Close</option></select></label>
    <label>{{tx('Lado de key propuesto','Proposed key side')}}<select v-model="setup.key_side"><option value="left">Izquierda / Left</option><option value="right">Derecha / Right</option><option value="back">Contraluz / Back</option><option value="front">Frontal / Front</option></select></label>
    <label>{{tx('Calidad de luz propuesta','Proposed light quality')}}<select v-model="setup.softness"><option value="soft">Suave / Soft</option><option value="hard">Dura / Hard</option></select></label>
    <label>{{tx('Contraste deseado','Desired contrast')}}<select v-model="setup.contrast"><option value="low">Bajo / Low</option><option value="medium">Medio / Medium</option><option value="high">Alto / High</option></select></label>
    <label>{{tx('Ancho de sensor propuesto (mm)','Proposed sensor width (mm)')}}<input type="number" v-model.number="setup.sensor_width_mm" min="6" max="70" step=".1"></label>
    <label>{{tx('Focal disponible (mm), opcional','Available lens (mm), optional')}}<input type="number" :value="setup.focal_mm??''" @input="setup.focal_mm=($event.target as HTMLInputElement).value===''?null:Number(($event.target as HTMLInputElement).value)" min="4" max="300" :placeholder="tx('Sin datos','No data')"></label>
    <label>{{tx('Apertura de partida','Starting aperture')}}<input type="number" v-model.number="setup.aperture" min="1" max="22" step=".1"></label>
    <div class="planner-pair"><label>FPS<input type="number" v-model.number="setup.fps" min="1" max="120" step=".001"></label><label>Shutter °<input type="number" v-model.number="setup.shutter_angle" min="1" max="360"></label></div>
    <label>{{tx('WB de partida (K)','Starting WB (K)')}}<input type="number" v-model.number="setup.white_balance_k" min="2000" max="12000" step="100"></label>
    <label>{{tx('Altura de cámara propuesta (m)','Proposed camera height (m)')}}<input type="number" v-model.number="setup.camera_height_m" min=".1" max="3" step=".1"></label>
    <label>{{tx('Movimiento elegido','Chosen movement')}}<select v-model="setup.movement"><option value="locked">Fijo / Locked</option><option value="handheld">Mano / Handheld</option><option value="slow-move">Lento / Slow move</option></select></label>
    <q-btn unelevated color="primary" text-color="dark" :loading="busy" :label="tx('Preparar propuesta local','Prepare local proposal')" @click="generate"/>
    <p v-if="report">{{elapsed}} ms · {{tx('análisis local muestreado a 512 px','local analysis sampled at 512 px')}}</p><p v-if="error" class="planner-error" role="alert">{{error}}</p>
   </section>
   <section v-if="!report" class="planner-start"><h2>{{tx('Del encuadre al montaje','From frame to setup')}}</h2><p>{{tx('Elige cómo quieres rodarlo y prepara un esquema cenital editable, checklist, alternativas de equipo y referencias técnicas. La imagen se queda en este equipo.','Choose how to shoot it and prepare an editable overhead layout, checklist, equipment alternatives and technical references. Your image stays on this computer.')}}</p></section>
   <section v-else class="planner-report">
    <q-banner v-if="stale" class="planner-stale">{{tx('Han cambiado la referencia, receta o elecciones. Regenera la propuesta antes de exportar; esto reinicia las ediciones del diagrama.','Reference, recipe or choices changed. Regenerate before exporting; this resets diagram edits.')}}</q-banner>
    <section class="planner-diagram"><h2>{{tx('Montaje cenital propuesto','Proposed overhead layout')}}</h2><p>{{tx('Selecciona un elemento y mueve X/Y. Metros de propuesta, sin escala recuperada de la foto. Rim y práctica son opcionales.','Select an element and move X/Y. Proposed metres, not scale recovered from the photograph. Rim and practical are optional.')}}</p>
     <svg viewBox="0 0 500 500" role="img" :aria-label="tx('Diagrama de sujeto, cámara y luces propuestos','Proposed subject, camera and lighting diagram')"><defs><pattern id="planner-grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#303d47"/></pattern></defs><rect width="500" height="500" fill="url(#planner-grid)"/><g v-for="node in report.diagram.nodes" :key="node.id" :opacity="node.enabled?1:.3"><line v-if="node.id!=='subject'" :x1="position(node.x)" :y1="position(-node.y)" :x2="position(report.diagram.nodes[0]!.x)" :y2="position(-report.diagram.nodes[0]!.y)" stroke="#7e99a5" stroke-dasharray="5 5"/><circle :cx="position(node.x)" :cy="position(-node.y)" r="16" :fill="node.id==='subject'?'#c0ccdf':node.id==='camera'?'#91c9c1':'#e9c68b'" :stroke="selected===node.id?'#fff':'#172028'" stroke-width="2"/><text :x="position(node.x)" :y="position(-node.y)+32" text-anchor="middle" fill="#e4eaf0" font-size="14">{{node.label}}</text></g><text x="12" y="20" fill="#97a9b9" font-size="12">+Y · Fondo / Background</text></svg>
     <label>{{tx('Elemento','Element')}}<select v-model="selected"><option v-for="node in report.diagram.nodes" :value="node.id" :key="node.id">{{node.label}}</option></select></label>
     <div v-if="selectedNode" class="diagram-controls"><label>X: {{selectedNode.x}} m<input type="range" v-model.number="selectedNode.x" min="-5" max="5" step=".1"></label><label>Y: {{selectedNode.y}} m<input type="range" v-model.number="selectedNode.y" min="-5" max="5" step=".1"></label><label v-if="['rim','practical'].includes(selectedNode.id)"><input type="checkbox" v-model="selectedNode.enabled">{{tx('Incluir en el montaje','Include in setup')}}</label></div>
    </section>
    <section v-for="(items,key) in report.sections" :key="key" class="planner-section"><h2>{{tx(sectionLabel[key]??key,key)}}</h2><article v-for="(item,index) in items" :key="index"><span class="evidence-kind" :class="item.kind">{{tx(kindLabel[item.kind]??item.kind,item.kind)}}</span><h3>{{item.title}}</h3><p>{{item.detail}}</p><p v-if="item.uncertainty" class="uncertainty">{{item.uncertainty}}</p><span v-for="id in item.source_ids" :key="id" class="planner-source-tag">{{id}}</span></article></section>
    <section class="planner-section"><h2>{{tx('Equipo: alternativas','Equipment alternatives')}}</h2><div class="equipment-grid"><article v-for="(list,key) in report.equipment" :key="key"><h3>{{key==='low_budget'?tx('Bajo presupuesto','Low budget'):tx('Profesional','Professional')}}</h3><ul><li v-for="value in list" :key="value">{{value}}</li></ul></article></div></section>
    <section class="planner-checklist"><h2>{{tx('Antes de rodar','Before shooting')}}</h2><label v-for="check in report.checklist" :key="check.id"><input type="checkbox" v-model="check.checked">{{check.text}}</label></section>
    <section class="planner-sources"><h2>{{tx('Fuentes y límites','Sources and limits')}}</h2><p v-for="source in report.sources" :key="source.id"><a :href="source.url" target="_blank" rel="noopener noreferrer">{{source.title}} ↗</a><small>{{source.id}} · {{tx('consultada','checked')}} {{source.verified_on}}</small></p><p v-for="limit in report.limits" :key="limit">{{limit}}</p><q-btn color="primary" text-color="dark" icon="download" :disable="stale" :label="tx('Guardar plan JSON local','Save local plan JSON')" @click="download"/><p>{{tx('El JSON conserva diagrama, checklist y receta; no incluye fotografía, EXIF, nombre de archivo ni ruta local. No acredita validación humana.','JSON retains diagram, checklist and recipe, without photograph, EXIF, filename or local path. It does not certify human validation.')}}</p></section>
   </section>
  </div>
 </main>
</template>
<style scoped>
.shot-planner{padding:28px;overflow-y:auto;flex:1;min-height:0;color:#d5e0e7}.planner-header{display:flex;justify-content:space-between;gap:20px;align-items:center}.planner-header h1{font-size:30px;line-height:1.2;margin:12px 0}.planner-header p,.shot-planner p{font-size:12px;line-height:1.7;color:#a4b5c1}.planner-limit{background:#303024;color:#e1d5b3;margin:18px 0;border:1px solid #6a6040;border-radius:8px;font-size:12px}.planner-grid{display:grid;grid-template-columns:280px minmax(0,1fr);gap:24px}.planner-settings,.planner-report section,.planner-start{border:1px solid #35434d;background:#1b222a;border-radius:10px;padding:20px;min-width:0}.planner-settings{align-self:start}.planner-settings img{width:100%;max-height:220px;object-fit:contain;border-radius:5px;background:#10161b}.shot-planner h2{font-size:18px;line-height:1.5;margin:12px 0}.shot-planner h3{font-size:14px;line-height:1.6;margin:8px 0}.shot-planner label{display:block;font-size:12px;line-height:1.6;margin:12px 0;color:#c7d4db}.shot-planner select,.shot-planner input[type=number]{display:block;width:100%;background:#101820;color:#e5edf1;border:1px solid #455561;border-radius:5px;padding:10px;min-height:44px;margin-top:5px;font:inherit}.planner-pair,.equipment-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}.planner-report{display:grid;gap:18px}.planner-diagram svg{display:block;width:100%;max-width:500px;margin:auto;background:#111a23;border-radius:8px}.diagram-controls input[type=range]{display:block;width:100%;min-height:44px;accent-color:#8cddc5}.diagram-controls input[type=checkbox],.planner-checklist input{margin-right:10px;accent-color:#8cddc5;min-width:20px;min-height:20px}.planner-report article{padding:12px 0;border-bottom:1px solid #35434d}.evidence-kind{font-size:9px;text-transform:uppercase;letter-spacing:1px;color:#9fcfc6}.evidence-kind.estimate{color:#ebc67b}.evidence-kind.source_confirmed{color:#acbfe5}.uncertainty{border-left:2px solid #c2a76b;padding-left:12px}.planner-source-tag{font-size:10px;color:#95b7ce;margin-right:12px}.planner-checklist label{display:flex;align-items:flex-start;min-height:44px;gap:8px}.planner-sources a{color:#a4dfce;font-size:12px}.planner-sources small{display:block;color:#8198ac;font-size:10px}.planner-error{color:#ffc5af!important}.planner-stale{background:#493b24;color:#ffe4b1}.planner-empty{padding:40px 0}.equipment-grid li{font-size:12px;line-height:1.8}.planner-start{min-height:200px;align-self:start}@media(max-width:1000px){.planner-grid{grid-template-columns:240px minmax(0,1fr)}.equipment-grid{grid-template-columns:1fr}}@media(max-width:700px){.shot-planner{padding:16px}.planner-grid{grid-template-columns:1fr}.planner-header{flex-direction:column;align-items:flex-start}.planner-header h1{font-size:25px}.planner-settings,.planner-report section{padding:16px}}
</style>
