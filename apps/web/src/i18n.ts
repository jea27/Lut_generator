import {ref} from 'vue'
export const language=ref<'es'|'en'>('es')
export const tx=(es:string,en:string)=>language.value==='es'?es:en
