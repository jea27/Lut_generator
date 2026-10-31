import test from 'node:test'
import assert from 'node:assert/strict'
import {creatorSteps,hasProAdjustments,previewIdentity,currentPreview} from '../src/workspace.ts'

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
