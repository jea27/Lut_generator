export function creatorSteps(reference:boolean,source:boolean,result:boolean,compared:boolean,exported:boolean){
 const active=!reference?0:!source?1:!result?2:!compared?3:!exported?4:5
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
