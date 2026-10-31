const slider=document.querySelector('#comparison');
slider.addEventListener('input',()=>{
 const value=Number(slider.value);
 document.querySelector('#after').style.clipPath=`inset(0 ${100-value}% 0 0)`;
 document.querySelector('#divider').style.left=value+'%';
 document.querySelector('#position').textContent=value+'%';
});
