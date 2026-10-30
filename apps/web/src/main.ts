import { createApp } from 'vue'
import { Quasar, Dialog, Notify } from 'quasar'
import 'quasar/dist/quasar.css'
import '@quasar/extras/material-icons/material-icons.css'
import App from './App.vue'
import './style.css'
createApp(App).use(Quasar,{plugins:{Dialog,Notify},config:{dark:true,brand:{primary:'#8cddc5',secondary:'#94a6bd'}}}).mount('#app')
