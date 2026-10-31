export function creatorSteps(reference:boolean,source:boolean,matched:boolean,compared:boolean,exported:boolean){
 const active=!reference?0:!source?1:!matched?2:!compared?3:!exported?4:5
 return ['Referencia','Mi imagen','Detectar color','Ajustar','Comparar','Exportar'].map((label,index)=>({label,active:index===active,done:index<active}))
}
export function hasProAdjustments(recipe:{exposure:number;contrast:number;saturation:number;temperature:number}){
 return recipe.exposure!==0||recipe.contrast!==1||recipe.saturation!==1||recipe.temperature!==0
}
export function previewIdentity(source:string|undefined,recipe:unknown){
 return JSON.stringify({source,recipe})
}
export function currentPreview(rendered:string,source:string|undefined,recipe:unknown){
 return !!source&&rendered===previewIdentity(source,recipe)
}
export function recordEdit<T>(entries:T[],index:number,value:T){
 const encoded=JSON.stringify(value)
 if(encoded===JSON.stringify(entries[index]))return {entries,index}
 const next=entries.slice(0,index+1)
 next.push(JSON.parse(encoded))
 if(next.length>30)next.splice(0,next.length-30)
 return {entries:next,index:next.length-1}
}
