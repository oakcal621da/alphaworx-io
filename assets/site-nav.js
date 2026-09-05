(() => {
  const button=document.querySelector('.menu-toggle'),nav=document.getElementById('site-nav');
  if(!button||!nav)return;
  document.documentElement.classList.add('js');button.hidden=false;
  const close=()=>{nav.classList.remove('is-open');button.setAttribute('aria-expanded','false');button.textContent='Menu ＋';};
  button.addEventListener('click',()=>{const open=button.getAttribute('aria-expanded')!=='true';nav.classList.toggle('is-open',open);button.setAttribute('aria-expanded',String(open));button.textContent=open?'Close ×':'Menu ＋';});
  nav.addEventListener('click',e=>{if(e.target.closest('a'))close();});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&nav.classList.contains('is-open')){close();button.focus();}});
})();
