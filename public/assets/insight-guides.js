(() => {
'use strict';
const data=JSON.parse(document.getElementById('insight-data').textContent);
const byId=id=>document.getElementById(id);
const buttons=[...document.querySelectorAll('[data-step]')];
function showStep(index){
 const s=data.steps[index];if(!s)return;
 buttons.forEach((b,i)=>b.setAttribute('aria-pressed',String(i===index)));
 byId('step-number').textContent=String(index+1).padStart(2,'0');
 for(const [id,key] of [['step-label','label'],['step-title','title'],['step-text','text'],['step-owner','owner'],['step-evidence','evidence']])byId(id).textContent=s[key];
}
buttons.forEach((b,i)=>{b.addEventListener('click',()=>showStep(i));b.addEventListener('keydown',e=>{let next;if(e.key==='ArrowRight')next=(i+1)%buttons.length;if(e.key==='ArrowLeft')next=(i+buttons.length-1)%buttons.length;if(e.key==='Home')next=0;if(e.key==='End')next=buttons.length-1;if(next!==undefined){e.preventDefault();buttons[next].focus();showStep(next);}});});
const dollars=new Intl.NumberFormat('en-US',{style:'currency',currency:'USD'});
function calculate(){
 const inputs=['tasks','ai-cost','review-minutes','hourly-rate'].map(byId);
 if(inputs.some(i=>!i.value.trim()||!i.checkValidity()||!Number.isFinite(i.valueAsNumber))){byId('cost-validation').textContent='Enter valid values within the limits shown by each field.';byId('total-cost').textContent='—';byId('unit-cost').textContent='Complete all four assumptions.';byId('ai-total').textContent='—';byId('review-total').textContent='—';byId('ai-bar').style.width='0%';byId('review-bar').style.width='0%';return;}
 const [tasks,ai,minutes,rate]=inputs.map(i=>i.valueAsNumber),aiTotal=tasks*ai,reviewTotal=tasks*minutes/60*rate,total=aiTotal+reviewTotal;
 byId('total-cost').textContent=dollars.format(total);byId('unit-cost').textContent=dollars.format(total/tasks)+' per task';byId('ai-total').textContent=dollars.format(aiTotal);byId('review-total').textContent=dollars.format(reviewTotal);
 byId('ai-bar').style.width=(total?aiTotal/total*100:0)+'%';byId('review-bar').style.width=(total?reviewTotal/total*100:0)+'%';byId('cost-validation').textContent='Illustrative processing and review costs. Exclusions are listed below.';
}
if(byId('tasks')){['tasks','ai-cost','review-minutes','hourly-rate'].forEach(id=>byId(id).addEventListener('input',calculate));byId('reset-cost').addEventListener('click',()=>{['tasks','ai-cost','review-minutes','hourly-rate'].forEach((id,i)=>byId(id).value=[1000,.08,2,60][i]);calculate();});calculate();}
const permissions=[...document.querySelectorAll('[data-permission]')];
function updatePermissions(){
 const chosen=permissions.filter(i=>i.checked).map(i=>i.dataset.permission),actions=['Read the approved queue','Prepare a summary'];
 const labels={send:'Send customer email',modify:'Modify customer records',delete:'Delete messages'};chosen.forEach(key=>actions.push(labels[key]));
 byId('permission-title').textContent=chosen.length?'The assistant can now act.':'Read and prepare.';
 byId('permission-description').textContent=chosen.length?'These additional operations exceed the summarization task. Each needs its own resource scope, authorization checks, and decision about human approval.':'The example is limited to reading the approved queue and preparing a summary. A person takes the next consequential action.';
 byId('action-list').replaceChildren(...actions.map(action=>{const li=document.createElement('li');li.textContent=action;return li;}));
}
permissions.forEach(i=>i.addEventListener('change',updatePermissions));
const checks=[...document.querySelectorAll('[data-question]')];
function chosenQuestions(){return checks.filter(i=>i.checked).map(i=>data.questions[Number(i.dataset.question)]);}
function updateQuestions(){
 const qs=chosenQuestions();byId('question-count').textContent=qs.length+' question'+(qs.length===1?'':'s')+' selected';byId('download-notes').disabled=!qs.length;byId('print-notes').disabled=!qs.length;byId('export-status').textContent='';
 const heading=document.createElement('h3');heading.textContent=data.title;const list=document.createElement('ol');qs.forEach(q=>{const li=document.createElement('li');li.textContent=q;const note=document.createElement('small');note.textContent='Owner: ____________________   Next step: ____________________';li.append(note);list.append(li);});byId('print-questions').replaceChildren(heading,list);
}
checks.forEach(i=>i.addEventListener('change',updateQuestions));byId('clear-questions').addEventListener('click',()=>{checks.forEach(i=>i.checked=false);updateQuestions();});
byId('print-notes').addEventListener('click',()=>window.print());
byId('download-notes').addEventListener('click',()=>{const qs=chosenQuestions();if(!qs.length)return;const text=['ALPHAWORX | Discussion notes',data.title,'https://alphaworx.io/blog/'+data.slug+'.html','',...qs.flatMap((q,i)=>[(i+1)+'. '+q,'Owner: ____________________','Next step: ____________________',''])].join('\n');const url=URL.createObjectURL(new Blob([text],{type:'text/plain;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download='alphaworx-'+data.slug+'-notes.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);byId('export-status').textContent='Your discussion notes are ready for download.';});
const motion=byId('guide-motion'),reduced=matchMedia('(prefers-reduced-motion: reduce)');
function setMotion(paused){document.body.classList.toggle('guide-motion-paused',paused);motion.setAttribute('aria-pressed',String(paused));motion.textContent=paused?'Resume motion':'Pause motion';}
setMotion(reduced.matches);motion.addEventListener('click',()=>setMotion(!document.body.classList.contains('guide-motion-paused')));
const chapters=[...document.querySelectorAll('.insight-chapter')];let scheduled=false;
function reading(){scheduled=false;const maximum=document.documentElement.scrollHeight-innerHeight;byId('guide-progress').style.width=(maximum>0?Math.max(0,Math.min(100,scrollY/maximum*100)):0)+'%';let active='';chapters.forEach(c=>{if(c.getBoundingClientRect().top<230)active='#'+c.id;});document.querySelectorAll('.insight-rail a').forEach(a=>{if(a.getAttribute('href')===active)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current');});}
addEventListener('scroll',()=>{if(!scheduled){scheduled=true;requestAnimationFrame(reading);}},{passive:true});addEventListener('resize',reading);reading();updateQuestions();
})();
