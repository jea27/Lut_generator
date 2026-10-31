let token=''
async function bootstrap(){
  const response=await fetch('/api/session',{cache:'no-store'})
  if(!response.ok)throw Error('Local session unavailable')
  token=(await response.json()).csrf
}
export async function api(path:string,init:RequestInit={},retry=true):Promise<Response>{
  if(!token)await bootstrap()
  const response=await fetch('/api'+path,{...init,headers:{'X-LumaForge-Local':'1','X-Color-Studio-Token':token,...init.headers}})
  if(!response.ok){
    const body=await response.json().catch(()=>({detail:'Local server unavailable'}))
    if(response.status===403&&body.detail==='LOCAL_SESSION_REQUIRED'&&retry){token='';return api(path,init,false)}
    throw Error(typeof body.detail==='string'?body.detail:'Invalid editing parameters')
  }
  return response
}
export const jsonPost=(value:unknown,method='POST')=>({method,headers:{'Content-Type':'application/json'},body:JSON.stringify(value)})
