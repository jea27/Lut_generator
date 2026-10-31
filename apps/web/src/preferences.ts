import {ref} from 'vue'
import {api,jsonPost} from './api'
import {language} from './i18n'
export type Workspace='creator'|'pro'
export const preferences=ref({language:'es',welcome_seen:false,export_format:'png',workspace:'creator' as Workspace})
let loading:Promise<void>|undefined
let saving=Promise.resolve()
export function loadPreferences(){
 return loading??=api('/preferences').then(r=>r.json()).then(value=>{
  Object.assign(preferences.value,value)
  language.value=preferences.value.language==='en'?'en':'es'
 }).catch(error=>{loading=undefined;throw error})
}
export function savePreferences(){
 preferences.value.language=language.value
 const snapshot={...preferences.value}
 const operation=saving.catch(()=>{}).then(()=>api('/preferences',jsonPost(snapshot,'PUT'))).then(()=>{})
 saving=operation
 return operation
}
