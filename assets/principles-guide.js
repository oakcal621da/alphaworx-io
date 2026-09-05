(() => {
'use strict';
const principles=JSON.parse(document.getElementById('principle-data').textContent);
const answers=new Map();
const escape=s=>s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const decisions={
 launch:{label:'THE UNRESOLVED COMMITMENT',title:'A working demo has not earned production authority.',text:'A broad rollout would leave the owner, permissions, and passing standard unresolved. In this scenario, the next useful move is to name an accountable owner and define what must pass before customers depend on it.',ids:[2,5,12]},
 wait:{label:'THE COST OF AN UNBOUNDED DELAY',title:'Ask what you need to learn—not just for a bigger plan.',text:'Waiting can be justified when a critical condition is missing. But “more certainty” needs a definition. Identify the evidence that would change the decision, and whether a small, reversible experiment can obtain it safely.',ids:[3,9,11]},
 bound:{label:'A CONDITIONAL PATH FORWARD',title:'Approve the learning. Define the limits.',text:'A bounded pilot is a proposal, not an automatic green light. Name the business owner, use an approved low-risk queue, require human review, define a passing threshold and stop conditions, and set a date to review the next investment.',ids:[1,4,5,12]}
};
document.querySelectorAll('[data-choice]').forEach(button=>button.addEventListener('click',()=>{
 document.querySelectorAll('[data-choice]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
 const d=decisions[button.dataset.choice];
 document.getElementById('decision-response').innerHTML=`<span class="response-icon" aria-hidden="true">↳</span><div><p class="eyebrow">${d.label}</p><h3>${d.title}</h3><p>${d.text}</p><div class="response-links">${d.ids.map(n=>`<a href="#principle-${n}">${String(n).padStart(2,'0')} / ${escape(principles[n-1].title)}</a>`).join('')}</div></div>`;
}));
function selected(){return principles.filter(p=>answers.get(p.n)==='discuss');}
const empty=document.getElementById('agenda-list').innerHTML;
function updateAgenda(){
 const chosen=selected(), clear=[...answers.values()].filter(v=>v==='clear').length;
 document.getElementById('header-count').textContent=chosen.length;
 document.getElementById('discuss-count').textContent=chosen.length;
 document.getElementById('clear-count').textContent=clear;
 document.getElementById('unread-count').textContent=12-answers.size;
 document.getElementById('agenda-list').innerHTML=chosen.length?'<ol>'+chosen.map(p=>`<li><b>${String(p.n).padStart(2,'0')} / ${escape(p.title)}</b><p>${escape(p.q)}</p></li>`).join('')+'</ol>':empty;
 document.querySelectorAll('[data-answer]').forEach(b=>b.setAttribute('aria-pressed',String(answers.get(Number(b.dataset.n))===b.dataset.answer)));
 document.querySelectorAll('[data-map]').forEach(a=>a.dataset.status=answers.get(Number(a.dataset.map))||'');
 document.getElementById('print-agenda').disabled=!chosen.length;
 document.getElementById('download-agenda').disabled=!chosen.length;
 document.getElementById('agenda-status').textContent=answers.size?`${chosen.length} question${chosen.length===1?'':'s'} selected for discussion. ${12-answers.size} principles still unreviewed.`:'';
}
document.querySelectorAll('[data-answer]').forEach(b=>b.addEventListener('click',()=>{
 const n=Number(b.dataset.n);if(answers.get(n)===b.dataset.answer)answers.delete(n);else answers.set(n,b.dataset.answer);updateAgenda();
}));
document.getElementById('reset').addEventListener('click',()=>{answers.clear();updateAgenda();});
document.getElementById('print-agenda').addEventListener('click',()=>window.print());
document.getElementById('download-agenda').addEventListener('click',()=>{
 const text=['ALPHAWORX | Leadership discussion agenda','The twelve first principles of enterprise AI strategy','Personal reflection; not an organizational assessment.','',...selected().flatMap(p=>[String(p.n).padStart(2,'0')+' — '+p.title,p.q,'Owner: ____________________   Next step: ____________________',''])].join('\n');
 const url=URL.createObjectURL(new Blob([text],{type:'text/plain;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download='alphaworx-discussion-agenda.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
 document.getElementById('agenda-status').textContent='Your discussion agenda has been prepared for download.';
});
const chapters=[...document.querySelectorAll('[data-principle]')];let queued=false;
function updateReading(){
 queued=false;
 const full=document.documentElement.scrollHeight-innerHeight;
 document.getElementById('progress').style.width=(full>0?Math.max(0,Math.min(100,scrollY/full*100)):0)+'%';
 let active=null;for(const section of chapters){if(section.getBoundingClientRect().top<=220)active=section.dataset.principle;}
 document.querySelectorAll('[data-rail]').forEach(a=>{if(a.dataset.rail===active)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current');});
}
addEventListener('scroll',()=>{if(!queued){queued=true;requestAnimationFrame(updateReading);}},{passive:true});addEventListener('resize',updateReading);updateReading();
const motion=document.getElementById('motion'),reduced=matchMedia('(prefers-reduced-motion: reduce)');
function setMotion(paused){document.body.classList.toggle('motion-paused',paused);motion.setAttribute('aria-pressed',String(paused));motion.textContent=paused?'Resume motion':'Pause motion';}
setMotion(reduced.matches);motion.addEventListener('click',()=>setMotion(!document.body.classList.contains('motion-paused')));
})();
