<script setup lang="ts">
import { computed, nextTick, onMounted, onBeforeUnmount, reactive, ref, watch } from 'vue'
import { useQuasar } from 'quasar'
type Recipe={version:number;domain:string;method:string;scale:number[];offset:number[];intensity:number;exposure:number;contrast:number;saturation:number;temperature:number}
type Analysis={histograms:number[][];dominant:{hex:string;fraction:number}[];luminance_mean:number;contrast_p95_p05:number}
type ImageAsset={id:string;width:number;height:number;notes:string[];has_alpha:boolean;preview_url:string;analysis:Analysis;name:string}
type Preset={id:string;name:string;recipe:Recipe}
const q=useQuasar()
const neutral=():Recipe=>({version:1,domain:'encoded-sRGB-D65',method:'lab-statistics',scale:[1,1,1],offset:[0,0,0],intensity:1,exposure:0,contrast:1,saturation:1,temperature:0})
const recipe=reactive<Recipe>(neutral()), source=ref<ImageAsset|null>(null), reference=ref<ImageAsset|null>(null)
const online=ref(false),busy=ref(false),previewing=ref(false),error=ref(''),resultUrl=ref(''),split=ref(50),zoom=ref(1)
const presets=ref<Preset[]>([]),presetName=ref(''),timing=ref(0),memory=ref(0),method=ref('lab-statistics')
const history=ref<Recipe[]>([neutral()]),historyIndex=ref(0)
let restoring=false,timer:ReturnType<typeof setTimeout>|undefined,controller:AbortController|undefined,serial=0
const headers={'X-LumaForge-Local':'1'}
const clone=(value:Recipe):Recipe=>JSON.parse(JSON.stringify(value))
async function api(path:string,init:RequestInit={}) {
  const response=await fetch('/api'+path,{...init,headers:{...headers,...init.headers}})
  if(!response.ok) { const body=await response.json().catch(()=>({detail:'No se pudo conectar con el servidor local'})); throw Error(typeof body.detail==='string'?body.detail:'Parámetros de edición no válidos') }
  return response
}
const jsonPost=(value:unknown)=>({method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(value)})
function revoke() { if(resultUrl.value)URL.revokeObjectURL(resultUrl.value);resultUrl.value='' }
async function assignRecipe(value:Recipe,reset=false) {
  restoring=true;Object.assign(recipe,clone(value));await nextTick();restoring=false
  if(reset){history.value=[clone(value)];historyIndex.value=0}
}
async function upload(event:Event,kind:'source'|'reference') {
  const input=event.target as HTMLInputElement,file=input.files?.[0];if(!file)return
  busy.value=true;error.value=''
  try {
    const form=new FormData();form.append('file',file)
    const response=await api('/images',{method:'POST',body:form})
    const asset:ImageAsset={...await response.json(),name:file.name}
    if(kind==='source'){controller?.abort();++serial;clearTimeout(timer);previewing.value=false;revoke();source.value=asset;await assignRecipe(neutral(),true)}else reference.value=asset
    q.notify({message:kind==='source'?'Fotografía lista para editar':'Referencia analizada',color:'dark',icon:'check'})
  }catch(e){error.value=(e as Error).message}finally{busy.value=false;input.value=''}
}
async function match() {
  if(!source.value||!reference.value)return
  busy.value=true;error.value=''
  try {
    const response=await api('/fit',jsonPost({source_id:source.value.id,reference_id:reference.value.id,method:method.value}))
    const data=await response.json();await assignRecipe(data.recipe,true);await renderPreview()
  }catch(e){error.value=(e as Error).message}finally{busy.value=false}
}
async function renderPreview() {
  if(!source.value)return
  controller?.abort();controller=new AbortController();const current=++serial
  previewing.value=true;error.value=''
  try{
    const response=await api('/preview',{...jsonPost({source_id:source.value.id,recipe}),signal:controller.signal})
    const blob=await response.blob();if(current!==serial)return
    revoke();resultUrl.value=URL.createObjectURL(blob)
    timing.value=Number(response.headers.get('X-Processing-Ms'));memory.value=Number(response.headers.get('X-RSS-Peak-MB'))
  }catch(e){if((e as Error).name!=='AbortError')error.value=(e as Error).message}
  finally{if(current===serial)previewing.value=false}
}
watch(recipe,()=>{
  if(!restoring){const value=clone(recipe);if(JSON.stringify(value)!==JSON.stringify(history.value[historyIndex.value])){
    history.value=history.value.slice(0,historyIndex.value+1);history.value.push(value);if(history.value.length>30)history.value.shift();historyIndex.value=history.value.length-1
  }}
  if(source.value)previewing.value=true
  clearTimeout(timer);timer=setTimeout(renderPreview,300)
},{deep:true})
async function undo(delta:number){const index=historyIndex.value+delta;if(index<0||index>=history.value.length)return;historyIndex.value=index;await assignRecipe(history.value[index]!)}
async function download(format:string) {
  if(!source.value)return;busy.value=true;error.value=''
  try{
    const response=await api('/export/'+format,jsonPost({source_id:source.value.id,recipe}))
    const blob=await response.blob(),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='lumaforge.'+format;a.click();setTimeout(()=>URL.revokeObjectURL(url),60000)
    timing.value=Number(response.headers.get('X-Processing-Ms'));memory.value=Number(response.headers.get('X-RSS-Peak-MB'))
    q.notify({message:'Archivo '+format.toUpperCase()+' generado localmente',color:'dark',icon:'download_done'})
  }catch(e){error.value=(e as Error).message}finally{busy.value=false}
}
async function loadPresets(){presets.value=await(await api('/presets')).json()}
async function savePreset(){
  if(!presetName.value.trim())return
  try{await api('/presets',jsonPost({name:presetName.value.trim(),recipe}));presetName.value='';await loadPresets()}catch(e){error.value=(e as Error).message}
}
async function importRecipe(event:Event){
  const input=event.target as HTMLInputElement,file=input.files?.[0];if(!file)return
  try{if(file.size>64000)throw Error('Receta JSON demasiado grande');const value=JSON.parse(await file.text());const valid=await(await api('/presets/validate',jsonPost(value))).json();await assignRecipe(valid)}catch(e){error.value=(e as Error).message}finally{input.value=''}
}
function clearImages(){q.dialog({title:'Eliminar imágenes temporales',message:'Se eliminarán las copias locales de esta sesión. Los originales y presets se conservan.',cancel:true,persistent:true}).onOk(async()=>{
  try{controller?.abort();clearTimeout(timer);++serial;await api('/images',{method:'DELETE'});source.value=null;reference.value=null;revoke();previewing.value=false;await assignRecipe(neutral(),true)}catch(e){error.value=(e as Error).message}
})}
const histogram=computed(()=>reference.value?.analysis??source.value?.analysis)
function histogramPath(channel:number){const data=histogram.value?.histograms[channel]??[],max=Math.max(...data,1);return data.map((x,i)=>`${i?'L':'M'}${i*4},${76-x/max*70}`).join(' ')}
onMounted(async()=>{try{online.value=(await(await api('/health')).json()).offline_processing;await loadPresets()}catch{error.value='Inicia el servidor local con Iniciar-LumaForge.ps1'}})
onBeforeUnmount(()=>{controller?.abort();clearTimeout(timer);revoke()})
</script>

<template>
 <div class="studio">
  <header class="topbar"><div class="brand"><span class="brand-mark">◈</span>Luma<span>Forge</span><small>COLOR STUDIO</small></div>
   <div class="project-title">Sesión de color <span>/</span> {{ source?.name??'Sin título' }}</div>
   <div class="local-status"><i :class="{ready:online}"></i>{{online?'LOCAL · SIN API EXTERNA':'CONECTANDO'}}<span class="version">v0.1</span></div>
  </header>
  <q-linear-progress v-if="busy||previewing" indeterminate color="primary" class="activity"/>
  <div class="workspace">
   <aside class="assets-panel">
    <div class="section-heading">PROYECTO <q-icon name="folder_open" size="17px"/></div>
    <label class="image-import"><span class="asset-label"><span class="asset-number">01</span>Referencia de estilo</span>
     <div class="import-frame" :class="{loaded:reference}"><img v-if="reference" :src="reference.preview_url" alt="Referencia de color importada"><div v-else><q-icon name="add_photo_alternate" size="30px"/><strong>Importar referencia</strong><small>JPG o PNG</small></div></div>
     <input type="file" accept="image/jpeg,image/png" aria-label="Importar referencia" :disabled="busy" @change="upload($event,'reference')">
     <small v-if="reference" class="file-meta">{{reference.width}} × {{reference.height}} · sRGB</small>
    </label>
    <label class="image-import"><span class="asset-label"><span class="asset-number">02</span>Fotografía de destino</span>
     <div class="import-frame" :class="{loaded:source}"><img v-if="source" :src="source.preview_url" alt="Fotografía de destino importada"><div v-else><q-icon name="image" size="30px"/><strong>Importar fotografía</strong><small>Hasta 24 MP · 32 MiB</small></div></div>
     <input type="file" accept="image/jpeg,image/png" aria-label="Importar fotografía de destino" :disabled="busy" @change="upload($event,'source')">
     <small v-if="source" class="file-meta">{{source.width}} × {{source.height}} · {{source.has_alpha?'RGBA':'RGB'}}</small>
    </label>
    <q-select v-model="method" :options="[{label:'Estadísticas Lab',value:'lab-statistics'},{label:'Solo media Lab',value:'mean-only'}]" emit-value map-options dense outlined label="Método clásico" color="primary"/>
    <q-btn class="match-button" unelevated color="primary" text-color="dark" label="Analizar y transferir" icon="tune" :disable="!source||!reference||busy" @click="match"/>
    <div class="section-heading library-heading">MIS PRESETS <span>{{presets.length.toString().padStart(2,'0')}}</span></div>
    <div v-if="!presets.length" class="no-presets">Tu biblioteca empieza con<br>el primer look que guardes.</div>
    <button v-for="preset in presets" :key="preset.id" class="preset-row" @click="assignRecipe(preset.recipe)"><span class="preset-dot"></span>{{preset.name}}<q-icon name="chevron_right"/></button>
    <div class="preset-save"><q-input v-model="presetName" dense outlined label="Nombre del preset" maxlength="80"/><q-btn flat dense icon="add" aria-label="Guardar preset" :disable="!source||!presetName.trim()" @click="savePreset"/></div>
    <label class="import-recipe">Importar receta JSON<input type="file" accept="application/json,.json" aria-label="Importar receta JSON" @change="importRecipe"></label>
    <button class="clear-button" @click="clearImages"><q-icon name="delete_outline"/>Eliminar imágenes temporales</button>
   </aside>
   <main class="main-panel">
    <div class="viewer-toolbar"><div><span class="active-tab">Comparar</span><span class="secondary-tab">{{source?'Previsualización · lado máx. 1280 px':'Espacio de trabajo'}}</span></div>
     <div class="zoom-tools"><q-btn flat round dense icon="remove" aria-label="Reducir zoom" @click="zoom=Math.max(1,zoom-.25)"/><button @click="zoom=1">{{Math.round(zoom*100)}}%</button><q-btn flat round dense icon="add" aria-label="Aumentar zoom" @click="zoom=Math.min(3,zoom+.25)"/></div>
    </div>
    <div class="stage">
     <div v-if="!source" class="empty-stage"><div class="empty-symbol">◈</div><h1>El color empieza con una referencia.</h1><p>Importa dos imágenes. Explora el look.<br>Ajusta hasta hacerlo tuyo.</p><div><span>01 Referencia</span><q-icon name="east"/><span>02 Fotografía</span></div></div>
     <div v-else class="comparison" :style="{aspectRatio:`${source.width}/${source.height}`}">
      <img :src="source.preview_url" alt="Antes: fotografía original" :style="{transform:`scale(${zoom})`}">
      <div v-if="resultUrl" class="after-layer" :style="{clipPath:`inset(0 ${100-split}% 0 0)`}"><img :src="resultUrl" alt="Después: resultado de LumaForge" :style="{transform:`scale(${zoom})`}"></div>
      <template v-if="resultUrl"><div class="split-line" :style="{left:split+'%'}"><span>‹ ›</span></div><span class="image-tag before-tag">DESPUÉS</span><span class="image-tag after-tag">ANTES</span>
       <input v-model.number="split" class="comparison-input" type="range" min="0" max="100" aria-label="Deslizador antes y después">
      </template>
     </div>
     <div v-if="previewing" class="render-badge"><q-spinner size="14px"/> Actualizando vista previa</div>
    </div>
    <div class="under-viewer"><span><q-icon name="swap_horiz"/>{{resultUrl?'Desliza para comparar':'El original permanece intacto'}}</span><span>sRGB · SDR · 8 bits</span></div>
    <div v-if="error" class="error-banner" role="alert"><q-icon name="error_outline"/>{{error}}<button @click="error=''">×</button></div>
    <div class="look-description"><span class="small-kicker">UN LOOK, A TU MEDIDA</span><h2>Una aproximación. Tu criterio.</h2><p>Transferencia global de color con límites conservadores. Ajusta el resultado antes de exportar.</p></div>
    <div v-if="source" class="color-notes"><q-icon name="info_outline"/><span>{{source.notes.join(' · ')}}. JPG con transparencia se compone sobre blanco.</span></div>
   </main>
   <aside class="controls-panel">
    <div class="section-heading">ANÁLISIS <span>{{reference?'REFERENCIA':'IMAGEN'}}</span></div>
    <div class="histogram"><svg viewBox="0 0 252 80" role="img" aria-label="Histograma RGB real de la imagen"><path d="M0 20H252M0 40H252M0 60H252" stroke="#2b3037" fill="none"/><path v-for="(color,c) in ['#cb8177','#8ab78a','#7a9ed1']" :key="c" :d="histogramPath(c)" :stroke="color" fill="none" stroke-width="1.4"/></svg><div class="hist-labels"><span>Sombras</span><span>Altas luces</span></div></div>
    <div class="analysis-numbers"><span>Luminancia <b>{{histogram?(histogram.luminance_mean*100).toFixed(1)+'%':'—'}}</b></span><span>Contraste P95–P05 <b>{{histogram?histogram.contrast_p95_p05.toFixed(3):'—'}}</b></span></div>
    <div class="palette"><span v-for="color in histogram?.dominant??[]" :key="color.hex" :style="{background:color.hex}" :title="color.hex"></span></div>
    <div class="section-heading edit-heading">AJUSTES <div><q-btn flat round dense icon="undo" aria-label="Deshacer ajuste" :disable="historyIndex===0" @click="undo(-1)"/><q-btn flat round dense icon="redo" aria-label="Rehacer ajuste" :disable="historyIndex>=history.length-1" @click="undo(1)"/></div></div>
    <div class="intensity-control"><div class="control-label"><span>Intensidad del look</span><output>{{Math.round(recipe.intensity*100)}}%</output></div><q-slider v-model="recipe.intensity" :min="0" :max="1" :step=".01" color="primary" aria-label="Intensidad del look" :disable="!source"/></div>
    <div v-for="control in [{key:'exposure',label:'Exposición',min:-2,max:2,step:.05},{key:'contrast',label:'Contraste',min:.6,max:1.4,step:.01},{key:'saturation',label:'Saturación',min:0,max:2,step:.01},{key:'temperature',label:'Temperatura',min:-1,max:1,step:.01}]" :key="control.key" class="manual-control">
     <div class="control-label"><span>{{control.label}}</span><output>{{Number(recipe[control.key as keyof Recipe]).toFixed(2)}}</output></div>
     <q-slider :model-value="Number(recipe[control.key as keyof Recipe])" @update:model-value="(v)=>{(recipe as any)[control.key]=v}" :min="control.min" :max="control.max" :step="control.step" color="grey-5" :aria-label="control.label" :disable="!source"/>
    </div>
    <q-btn flat no-caps class="reset-button" label="Restablecer ajustes" icon="restart_alt" :disable="!source" @click="assignRecipe(neutral())"/>
    <div class="domain-note"><q-icon name="verified_user" size="19px"/><span>Procesamiento local.<br>Sin IA generativa ni servicios de imagen.</span></div>
   </aside>
  </div>
  <footer class="export-bar"><div class="process-status"><i :class="{ready:online}"></i><span>{{busy?'Procesando…':previewing?'Previsualizando…':'Listo para crear'}}<small>{{timing?`${timing} ms · RSS pico muestreado ${memory} MB`:'Tus imágenes se quedan en este equipo'}}</small></span></div>
   <div class="export-actions"><q-btn flat no-caps label="Receta JSON" icon="data_object" :disable="!source||busy||previewing" @click="download('json')"/><q-btn outline no-caps label="LUT .cube" icon="grid_on" :disable="!source||busy||previewing" @click="download('cube')"/><q-btn unelevated no-caps color="primary" text-color="dark" label="Exportar PNG" icon="download" :disable="!source||busy||previewing" @click="download('png')"/><q-btn flat no-caps label="JPG" :disable="!source||busy||previewing" @click="download('jpg')"/></div>
  </footer>
 </div>
</template>
