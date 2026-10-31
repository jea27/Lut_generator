document.querySelector('#feedback').addEventListener('submit',event=>{
 event.preventDefault();const value=id=>document.getElementById(id).value;
 const data={schema:'color-studio-beta-feedback-v1',code:value('code'),version:value('version'),windows:value('os'),result:value('result'),ease_rating:value('rating')||null,notes:value('notes'),synthetic:value('code')==='QA00',verification:'unverified',counts_as_interview:false};
 const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));
 const a=document.createElement('a');a.href=url;a.download=`beta-feedback-${data.code}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
 document.querySelector('#status').textContent='JSON preparado. Revísalo y compártelo únicamente por el canal privado acordado. No se ha enviado ningún dato.';
});
