(function(){
  const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();

  // Curvas de nivel generadas (ruido simple)
  function rnd(seed){let s=seed;return()=>{s=(s*9301+49297)%233280;return s/233280}}
  function field(seed){const r=rnd(seed),bumps=[];for(let i=0;i<6;i++)bumps.push([r(),r(),.08+r()*.22,(r()-.3)*1.4]);
    return (x,y)=>bumps.reduce((a,[bx,by,s,h])=>a+h*Math.exp(-((x-bx)**2+(y-by)**2)/(2*s*s)),0)}
  function draw(cv,seed,levels){
    const dpr=window.devicePixelRatio||1,w=cv.clientWidth,h=cv.clientHeight;if(!w)return;
    cv.width=w*dpr;cv.height=h*dpr;const g=cv.getContext('2d');g.scale(dpr,dpr);
    g.fillStyle=css('--surface');g.fillRect(0,0,w,h);
    const f=field(seed),step=2.5,acc=css('--accent'),con=css('--contour');
    for(let l=0;l<levels;l++){
      const t=-.3+l*(1.4/levels);g.strokeStyle=l%5===0?con:acc;g.globalAlpha=l%5===0?.95:.6;g.lineWidth=l%5===0?2:1.3;g.lineCap='round';g.beginPath();
      for(let x=0;x<w;x+=step)for(let y=0;y<h;y+=step){
        const a=f(x/w,y/h*h/w*1.6)-t,b=f((x+step)/w,y/h*h/w*1.6)-t,c=f(x/w,(y+step)/h*h/w*1.6)-t;
        if(a*b<0){const px=x+step*a/(a-b);g.moveTo(px,y);g.lineTo(px+.4,y+.4)}
        if(a*c<0){const py=y+step*a/(a-c);g.moveTo(x,py);g.lineTo(x+.4,py+.4)}
      }g.stroke()}
    g.globalAlpha=1;
  }
  function drawAll(){draw(document.getElementById('hero'),42,22);document.querySelectorAll('.case canvas').forEach(c=>draw(c,+c.dataset.seed,14))}
  drawAll();addEventListener('resize',drawAll);
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change',drawAll);
  new MutationObserver(drawAll).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});
  document.fonts&&document.fonts.ready.then(drawAll);

  const hero=document.getElementById('hero'),coord=document.getElementById('coord');
  hero.addEventListener('mousemove',e=>{const r=hero.getBoundingClientRect();
    const lat=(4.75-(e.clientY-r.top)/r.height*.08).toFixed(4),lon=(74.11-(e.clientX-r.left)/r.width*.08).toFixed(4);
    coord.textContent=`${lat}° N, ${lon}° O · EPSG:4326`});

  // Índice lateral derecho
  const heads=[...document.querySelectorAll('main h2')],toc=document.getElementById('toc');
  heads.forEach(h=>{const li=document.createElement('li');li.innerHTML=`<a href="#${h.id}">${h.firstChild.textContent.trim()}</a>`;toc.appendChild(li)});
  const tocLinks=[...toc.querySelectorAll('a')],sideLinks=[...document.querySelectorAll('.side a')];
  function spy(){let cur=heads[0];heads.forEach(h=>{if(h.getBoundingClientRect().top<120)cur=h});
    tocLinks.forEach(a=>a.classList.toggle('on',a.getAttribute('href')==='#'+cur.id));
    const top=scrollY<200?'inicio':cur.id;sideLinks.forEach(a=>a.classList.toggle('on',a.getAttribute('href')==='#'+top))}
  addEventListener('scroll',spy,{passive:true});spy();

  // Menú móvil
  const side=document.getElementById('side'),mb=document.getElementById('menuBtn');
  mb.addEventListener('click',()=>{const o=side.classList.toggle('open');mb.setAttribute('aria-expanded',o)});
  side.addEventListener('click',e=>{if(e.target.tagName==='A'){side.classList.remove('open');mb.setAttribute('aria-expanded',false)}});

  // Búsqueda de servicios
  const q=document.getElementById('q'),cards=[...document.querySelectorAll('.svc')],noRes=document.getElementById('noRes');
  const norm=s=>s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'');
  q.addEventListener('input',()=>{const t=norm(q.value.trim());let n=0;
    cards.forEach(c=>{const hit=!t||norm(c.textContent+' '+c.dataset.k).includes(t);c.hidden=!hit;if(hit)n++});
    noRes.hidden=n>0;if(t)document.getElementById('ruta').scrollIntoView()});

})();
