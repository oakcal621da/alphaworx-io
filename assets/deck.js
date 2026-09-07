(() => {
'use strict';
const slides = [...document.querySelectorAll('.slide')];
if (!slides.length) return;
const select = document.getElementById('slide-select');
const previous = document.getElementById('previous');
const next = document.getElementById('next');
const count = document.getElementById('slide-count');
const motion = document.getElementById('motion-toggle');
const readingButton = document.getElementById('reading-toggle');
const reduced = matchMedia('(prefers-reduced-motion: reduce)');
let current = 0, reading = false, paused = reduced.matches;
function setMotion(value) {
  paused = value;
  document.body.classList.toggle('motion-paused', paused);
  motion.textContent = paused ? 'Resume motion' : 'Pause motion';
  motion.setAttribute('aria-pressed', String(paused));
  document.dispatchEvent(new CustomEvent('alphaworx:motion', {detail:{paused}}));
}
function indexFromHash() {
  return Math.max(0, slides.findIndex(slide => `#${slide.id}` === location.hash));
}
function show(index, {hash=true, scroll=false}={}) {
  current = Math.max(0, Math.min(slides.length - 1, index));
  slides.forEach((slide,i) => {
    slide.classList.toggle('active', i === current);
    slide.inert = !reading && i !== current;
  });
  select.value = String(current);
  previous.disabled = current === 0;
  next.disabled = current === slides.length - 1;
  count.textContent = `${String(current+1).padStart(2,'0')} / ${slides.length}`;
  document.getElementById('progress').style.width = `${(current+1)/slides.length*100}%`;
  if (hash && location.hash !== `#${slides[current].id}`) history.replaceState(null,'',`#${slides[current].id}`);
  if (scroll) {
    if (reading) slides[current].scrollIntoView({behavior:'instant', block:'start'});
    else window.scrollTo({top:0,behavior:'instant'});
  }
}
document.body.classList.add('js');
document.querySelector('.deck-controls').hidden = false;
setMotion(paused);
show(indexFromHash(), {hash:false});
previous.addEventListener('click', () => show(current-1, {scroll:true}));
next.addEventListener('click', () => show(current+1, {scroll:true}));
select.addEventListener('change', () => show(Number(select.value), {scroll:true}));
motion.addEventListener('click', () => setMotion(!paused));
reduced.addEventListener('change', e => setMotion(e.matches));
readingButton.addEventListener('click', () => {
  reading = !reading;
  document.body.classList.toggle('read-all',reading);
  readingButton.setAttribute('aria-pressed',String(reading));
  readingButton.textContent = reading ? 'Slide view' : 'Read all';
  show(current, {scroll:true});
});
document.getElementById('print-deck').addEventListener('click', () => window.print());
window.addEventListener('hashchange', () => show(indexFromHash(), {hash:false,scroll:true}));
document.addEventListener('keydown', e => {
  if (e.altKey || e.ctrlKey || e.metaKey || e.target.closest('input,textarea,select,button,a,[contenteditable="true"]')) return;
  let index;
  if (e.key === 'ArrowRight' || e.key === 'PageDown' || (e.key === ' ' && !reading)) index = current+1;
  if (e.key === 'ArrowLeft' || e.key === 'PageUp') index = current-1;
  if (e.key === 'Home') index = 0;
  if (e.key === 'End') index = slides.length-1;
  if (index !== undefined) {e.preventDefault(); show(index, {scroll:true});}
});
// Read-all mode keeps the position indicator in sync with the document.
const observer = new IntersectionObserver(entries => {
  if (!reading) return;
  const visible = entries.filter(entry=>entry.isIntersecting).sort((a,b)=>b.intersectionRatio-a.intersectionRatio);
  if (visible.length) show(slides.indexOf(visible[0].target), {hash:false});
}, {threshold:[.25,.5,.75]});
slides.forEach(slide=>observer.observe(slide));
// Fictional worked examples; these controls do not read or score AIOS data.
const passes = {
 initial: {score:2, name:'Emerging', confidence:'provisional', reason:'The initial view relies on the approved human-review process. The AI tool permissions have not yet been independently tested.', change:'Status: provisional assessment; the action boundary remains unverified.'},
 reconciled: {score:1, name:'Ad hoc', confidence:'strong', reason:'E03 reproduces a posting action without required approval. E02 defines a human decision that the tool boundary does not enforce.', change:'Recorded change: 2 → 1 after permission testing. Strong evidence supports a low maturity finding; it does not imply readiness.'}
};
document.querySelectorAll('[data-pass]').forEach(button => button.addEventListener('click', () => {
 const view = passes[button.dataset.pass];
 document.querySelectorAll('[data-pass]').forEach(other => other.setAttribute('aria-pressed', String(other === button)));
 document.getElementById('maturity-score').innerHTML = `${view.score}<span>/5</span>`;
 document.getElementById('maturity-name').textContent = view.name;
 document.getElementById('maturity-confidence').textContent = `Evidence confidence: ${view.confidence}`;
 document.getElementById('maturity-reason').textContent = view.reason;
 document.getElementById('maturity-change').textContent = view.change;
 document.querySelectorAll('.maturity-track i').forEach((segment,i) => segment.classList.toggle('filled', i < view.score));
}));
const costInput = document.getElementById('ai-operating-cost');
const money = value => new Intl.NumberFormat('en-US', {style:'currency',currency:'USD',notation:'compact',maximumFractionDigits:1}).format(value);
function updateAiEconomics() {
 const cost = Number(costInput.value) * 1000;
 const net = 54000000 - cost;
 document.getElementById('ai-cost-output').textContent = money(cost);
 document.getElementById('ai-cost').textContent = money(cost);
 document.getElementById('ai-net').textContent = money(net);
 document.querySelector('#economics .cost-answer>p').textContent = `at ${money(cost)} annual operating cost; cash benefit held constant`;
 costInput.setAttribute('aria-valuetext', `${money(cost)} annual AI operating cost; ${money(net)} cash benefit after operating costs. Staff capacity, forecasts, and duplicate claims are excluded.`);
}
costInput.addEventListener('input', updateAiEconomics);
updateAiEconomics();
})();
