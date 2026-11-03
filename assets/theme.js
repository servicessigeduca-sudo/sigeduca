// Modo claro / oscuro: se aplica antes de pintar y se recuerda en el navegador
(function(){
  const root=document.documentElement;
  let saved=null;try{saved=localStorage.getItem('tema')}catch(e){}
  if(saved==='light'||saved==='dark')root.setAttribute('data-theme',saved);
  const isDark=()=>root.getAttribute('data-theme')?root.getAttribute('data-theme')==='dark':matchMedia('(prefers-color-scheme: dark)').matches;
  function sync(btn){const d=isDark();btn.setAttribute('aria-checked',d);btn.title=d?'Cambiar a modo claro':'Cambiar a modo oscuro'}
  document.addEventListener('DOMContentLoaded',()=>{
    const btn=document.getElementById('themeBtn');if(!btn)return;sync(btn);
    btn.addEventListener('click',()=>{const next=isDark()?'light':'dark';root.setAttribute('data-theme',next);
      try{localStorage.setItem('tema',next)}catch(e){}sync(btn)});
    matchMedia('(prefers-color-scheme: dark)').addEventListener('change',()=>sync(btn));
  });
})();
