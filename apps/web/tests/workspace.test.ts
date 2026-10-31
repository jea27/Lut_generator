import test from 'node:test'
import assert from 'node:assert/strict'
import {creatorSteps,hasProAdjustments,previewIdentity,currentPreview,recordEdit} from '../src/workspace.ts'

test('Creator guides actual state without inventing successful export',()=>{
 assert.equal(creatorSteps(false,false,false,false,false).findIndex(s=>s.active),0)
 assert.equal(creatorSteps(true,false,false,false,false).findIndex(s=>s.active),1)
 assert.equal(creatorSteps(true,true,false,false,false).findIndex(s=>s.active),2)
 assert.equal(creatorSteps(true,true,true,false,false).filter(s=>s.done).length,3)
 assert.equal(creatorSteps(true,true,true,true,true).at(-1)?.active,true)
})
test('Exports require the exact source and colour/optical recipe already previewed',()=>{
 const recipe={intensity:.8,look:{enabled:true,glow:.2}}
 const key=previewIdentity('source-a',recipe)
 assert.equal(currentPreview(key,'source-a',recipe),true)
 assert.equal(currentPreview(key,'source-b',recipe),false)
 assert.equal(currentPreview(key,undefined,recipe),false)
 assert.equal(currentPreview('', 'source-a',recipe),false)
 assert.equal(currentPreview(key,'source-a',{...recipe,intensity:.5}),false)
 assert.equal(currentPreview(key,'source-a',{...recipe,look:{...recipe.look,glow:.4}}),false)
})
test('Switching workspace does not normalize away meaningful Pro adjustments',()=>{
 const recipe={exposure:0,contrast:1,saturation:1,temperature:0}
 assert.equal(hasProAdjustments(recipe),false)
 const original=JSON.stringify(recipe)
 hasProAdjustments(recipe)
 assert.equal(JSON.stringify(recipe),original)
 for(const key of Object.keys(recipe))assert.equal(hasProAdjustments({...recipe,[key]:recipe[key as keyof typeof recipe]+.1}),true)
})

test('Recipe history retains preset/import/reset edits, truncates redo on new edits and bounds snapshots',()=>{
 const neutral={exposure:0,look:{glow:0}}
 let state={entries:[neutral],index:0}
 const preset={exposure:.5,look:{glow:.2}}
 state=recordEdit(state.entries,state.index,preset)
 preset.look.glow=.8
 assert.equal(state.entries[1]?.look.glow,.2,'Keep snapshot separate from live preset')
 state=recordEdit(state.entries,state.index,neutral)
 assert.equal(state.entries[state.index-1]?.exposure,.5,'Reset is undoable')
 state.index-- // undo, then importing another recipe discards the old redo
 state=recordEdit(state.entries,state.index,{exposure:.7,look:{glow:.3}})
 assert.deepEqual(state.entries.map(r=>r.exposure),[0,.5,.7])
 assert.equal(recordEdit(state.entries,state.index,state.entries[state.index]!).entries,state.entries)
 for(let i=1;i<=40;i++)state=recordEdit(state.entries,state.index,{exposure:i,look:{glow:0}})
 assert.equal(state.entries.length,30);assert.equal(state.index,29)
 assert.equal(state.entries[0]?.exposure,11);assert.equal(neutral.exposure,0)
})
