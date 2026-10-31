<script setup lang="ts">
import {tx} from './i18n'
export type Look={enabled:boolean;strength:number;glow:number;diffusion:number;fade:number;radius:number;threshold:number}
defineProps<{modelValue:Look;disabled:boolean}>()
const controls=[['strength','Intensidad del acabado','Finish strength'],['glow','Glow de altas luces','Highlight glow'],['diffusion','Difusión suave','Soft diffusion'],['fade','Fade','Fade']] as const
</script>
<template>
 <section class="look-panel">
  <div class="section-heading">{{tx('ACABADO MANUAL','MANUAL FINISH')}} <q-toggle v-model="modelValue.enabled" :disable="disabled" :aria-label="tx('Activar acabado','Enable finish')"/></div>
  <p>{{tx('Acabado manual experimental. La extracción automática del look de una referencia está pendiente.','Experimental manual finishing. Automatic extraction of a reference look is pending.')}}</p>
  <div v-for="control in controls" :key="control[0]" class="manual-control">
   <div class="control-label"><span>{{tx(control[1],control[2])}}</span><output>{{Math.round(modelValue[control[0]]*100)}}%</output></div>
   <q-slider v-model="modelValue[control[0]]" :min="0" :max="1" :step=".01" :disable="disabled||!modelValue.enabled" :aria-label="tx(control[1],control[2])" color="primary"/>
  </div>
  <p>{{tx('PNG/JPG y receta JSON conservan el acabado. La LUT .cube exporta solo Color Match; no incluye glow, difusión ni fade.','PNG/JPG and recipe JSON retain the finish. The .cube LUT exports Color Match only; glow, diffusion and fade are excluded.')}}</p>
 </section>
</template>
<style scoped>.look-panel{border-top:1px solid #38413f;margin-top:22px;padding-top:20px}.look-panel p{font-size:11px;color:#abb7b3;line-height:1.6}</style>
