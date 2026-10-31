import test from 'node:test'
import assert from 'node:assert/strict'
import {readFileSync} from 'node:fs'
import vm from 'node:vm'
import ts from 'typescript'

// Execute the actual module with controllable I/O. No browser, network or
// copied implementation: delayed responses reproduce the startup race.
function deferred(){
 let resolve!:(value?:any)=>void, reject!:(error:Error)=>void
 const promise=new Promise<any>((yes,no)=>{resolve=yes;reject=no})
 return {promise,resolve,reject}
}
function preferencesModule(api:(path:string,init?:any)=>Promise<any>){
 const exports:any={},language={value:'es'}
 const source=readFileSync(new URL('../src/preferences.ts',import.meta.url),'utf8')
 const compiled=ts.transpileModule(source,{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022}}).outputText
 vm.runInNewContext(compiled,{exports,require:(name:string)=>{
  if(name==='vue')return {ref:(value:any)=>({value})}
  if(name==='./i18n')return {language}
  if(name==='./api')return {api,jsonPost:(value:any,method:string)=>({method,body:JSON.stringify(value)})}
  throw Error('Unexpected import '+name)
 }})
 return exports
}
const saved={language:'en',welcome_seen:true,export_format:'jpg',workspace:'creator'}

test('Mode clicks during startup share one GET and retain saved preferences in ordered PUTs',async()=>{
 const read=deferred(),writes:any[]=[];let reads=0
 const prefs=preferencesModule(async(_path,init)=>{
  if(!init){reads++;return read.promise}
  writes.push(JSON.parse(init.body));return {}
 })
 const first=prefs.setWorkspace('pro'),last=prefs.setWorkspace('creator')
 assert.equal(reads,1);assert.equal(writes.length,0)
 read.resolve({json:async()=>saved})
 await Promise.all([first,last])
 assert.deepEqual(writes,[{...saved,workspace:'pro'},saved])
 assert.equal(prefs.preferences.value.workspace,'creator')
})

test('A failed initial load never writes defaults and can be retried',async()=>{
 let reads=0;const writes:any[]=[]
 const prefs=preferencesModule(async(_path,init)=>{
  if(init){writes.push(JSON.parse(init.body));return {}}
  if(++reads===1)throw Error('offline')
  return {json:async()=>saved}
 })
 await assert.rejects(prefs.setWorkspace('pro'),/offline/)
 assert.equal(writes.length,0);assert.equal(prefs.preferences.value.workspace,'creator')
 await prefs.setWorkspace('pro')
 assert.deepEqual(writes,[{...saved,workspace:'pro'}]);assert.equal(reads,2)
})

test('A delayed failed save cannot reorder or cancel the subsequent workspace choice',async()=>{
 const write=deferred(),started=deferred(),writes:any[]=[]
 const prefs=preferencesModule(async(_path,init)=>{
  if(!init)return {json:async()=>saved}
  writes.push(JSON.parse(init.body))
  if(writes.length===1){started.resolve();return write.promise}
  return {}
 })
 await prefs.loadPreferences()
 const first=prefs.setWorkspace('pro');const failed=assert.rejects(first,/save failed/)
 await started.promise
 const last=prefs.setWorkspace('creator')
 assert.equal(writes.length,1)
 write.reject(Error('save failed'))
 await failed;await last
 assert.deepEqual(writes.map(w=>w.workspace),['pro','creator'])
 assert.equal(prefs.preferences.value.workspace,'creator')
})
