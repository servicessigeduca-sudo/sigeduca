(function(){
  // Índice "En esta página"
  const heads=[...document.querySelectorAll('main h2')],toc=document.getElementById('toc');
  heads.forEach(h=>{const li=document.createElement('li');const a=document.createElement('a');a.href='#'+h.id;a.textContent=h.firstChild.textContent.trim();li.appendChild(a);toc.appendChild(li)});
  // Índice desplegable para pantallas pequeñas
  if(heads.length>2){const d=document.createElement('details');d.className='toc-movil';d.innerHTML='<summary>En esta página</summary>';const ol=document.createElement('ol');
    heads.forEach(h=>{const li=document.createElement('li');const a=document.createElement('a');a.href='#'+h.id;a.textContent=h.firstChild.textContent.trim();a.addEventListener('click',()=>d.open=false);li.appendChild(a);ol.appendChild(li)});
    d.appendChild(ol);heads[0].before(d)}
  const tocLinks=[...toc.querySelectorAll('a')];
  function spy(){if(!heads.length)return;let cur=heads[0];heads.forEach(h=>{if(h.getBoundingClientRect().top<120)cur=h});
    tocLinks.forEach(a=>a.classList.toggle('on',a.getAttribute('href')==='#'+cur.id))}
  addEventListener('scroll',spy,{passive:true});spy();

  // Menú móvil
  const side=document.getElementById('side'),mb=document.getElementById('menuBtn');
  mb.addEventListener('click',()=>{const o=side.classList.toggle('open');mb.setAttribute('aria-expanded',o)});
  document.addEventListener('click',e=>{if(side.classList.contains('open')&&!side.contains(e.target)&&!mb.contains(e.target)){side.classList.remove('open');mb.setAttribute('aria-expanded',false)}});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&side.classList.contains('open')){side.classList.remove('open');mb.setAttribute('aria-expanded',false);mb.focus()}});
  side.addEventListener('click',e=>{if(e.target.tagName==='A'){side.classList.remove('open');mb.setAttribute('aria-expanded',false)}});

  // Buscador: filtra el menú lateral
  const q=document.getElementById('q'),items=[...side.querySelectorAll('li')];
  const norm=s=>s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'');
  q.addEventListener('input',()=>{const t=norm(q.value.trim());items.forEach(li=>{const a=li.querySelector('a');li.hidden=!!t&&!norm(li.textContent+' '+(a&&a.title||'')).includes(t)});if(t)side.querySelectorAll('details').forEach(d=>d.open=true);
    if(t&&innerWidth<=820){side.classList.add('open');mb.setAttribute('aria-expanded',true)}});

  // Botón copiar en cada bloque de código
  document.querySelectorAll('.codebox').forEach(box=>{
    const pre=box.querySelector('pre'),b=document.createElement('button');b.type='button';b.className='copy';b.textContent='Copiar';
    b.addEventListener('click',()=>{const ok=()=>{b.textContent='Copiado';setTimeout(()=>b.textContent='Copiar',1500)};
      const sel=()=>getSelection().selectAllChildren(pre);
      try{navigator.clipboard.writeText(pre.textContent).then(ok,sel)}catch(e){sel()}});
    box.appendChild(b)});
})();
