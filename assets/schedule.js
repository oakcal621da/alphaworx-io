(() => {
'use strict';
const root=document.getElementById('schedule-booker');if(!root)return;
const status=document.getElementById('booker-status'),timeStep=document.getElementById('time-step'),details=document.getElementById('details-step'),success=document.getElementById('booking-success'),fallback=document.getElementById('booking-fallback'),dateInput=document.getElementById('schedule-date'),times=document.getElementById('time-options'),zoneLabel=document.getElementById('schedule-time-zone'),selectedLabel=document.getElementById('selected-time'),confirmLabel=document.getElementById('confirmation-time'),submit=document.getElementById('book-submit'),back=document.getElementById('booker-back'),progress=[...root.querySelectorAll('.booker-progress span')];
const apiBase=new URL(window.ALPHAWORX_SCHEDULER_API_BASE||location.origin);let token='',availabilityEndpoint='',bookingEndpoint='',selectedStart='';
const browserZone=Intl.DateTimeFormat().resolvedOptions().timeZone||'your local time';
function setStatus(message,state='info'){status.textContent=message;status.dataset.state=state;}
function partsInChicago(date=new Date()){const p=Object.fromEntries(new Intl.DateTimeFormat('en-US',{timeZone:'America/Chicago',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(date).filter(x=>x.type!=='literal').map(x=>[x.type,x.value]));return `${p.year}-${p.month}-${p.day}`;}
function nextWeekday(value){const d=new Date(`${value}T12:00:00`);while(d.getDay()===0||d.getDay()===6)d.setDate(d.getDate()+1);return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;}
function formatSlot(value){return new Intl.DateTimeFormat(undefined,{weekday:'long',month:'long',day:'numeric',hour:'numeric',minute:'2-digit',timeZoneName:'short'}).format(new Date(value));}
function setProgress(index){progress.forEach((item,i)=>item.classList.toggle('active',i===index));}
async function init(){
 setStatus('Connecting to the calendar…');
 try{const response=await fetch(new URL('/api/schedule/config',apiBase),{headers:{Accept:'application/json'},cache:'no-store'}),config=response.ok?await response.json():null;if(!config?.enabled)throw new Error();token=config.token;availabilityEndpoint=new URL(config.availabilityEndpoint,apiBase);bookingEndpoint=new URL(config.bookingEndpoint,apiBase);const today=partsInChicago();dateInput.min=today;const max=new Date(`${today}T12:00:00`);max.setDate(max.getDate()+30);dateInput.max=`${max.getFullYear()}-${String(max.getMonth()+1).padStart(2,'0')}-${String(max.getDate()).padStart(2,'0')}`;const initial=new Date(`${today}T12:00:00`);initial.setDate(initial.getDate()+1);dateInput.value=nextWeekday(`${initial.getFullYear()}-${String(initial.getMonth()+1).padStart(2,'0')}-${String(initial.getDate()).padStart(2,'0')}`);zoneLabel.textContent=`Times shown in ${browserZone}`;timeStep.hidden=false;fallback.hidden=true;await loadTimes();}
 catch{setStatus('');timeStep.hidden=true;fallback.hidden=false;}
}
async function loadTimes(){
 if(!dateInput.value||!token)return;times.replaceChildren();setStatus('Checking availability…');
 try{const url=new URL(availabilityEndpoint);url.searchParams.set('date',dateInput.value);const response=await fetch(url,{headers:{Accept:'application/json','X-Schedule-Token':token},cache:'no-store'}),result=await response.json().catch(()=>({}));if(!response.ok)throw new Error(result.error||'Availability could not be loaded.');if(!result.slots.length){const empty=document.createElement('p');empty.className='empty-times';empty.textContent='No open times on this day. Try another weekday.';times.append(empty);}else result.slots.forEach(value=>{const button=document.createElement('button');button.type='button';button.className='time-option';button.textContent=new Intl.DateTimeFormat(undefined,{hour:'numeric',minute:'2-digit'}).format(new Date(value));button.setAttribute('aria-label',formatSlot(value));button.addEventListener('click',()=>choose(value));times.append(button);});setStatus(result.slots.length?`${result.slots.length} times available`:'');}
 catch(error){setStatus(error.message||'Availability could not be loaded.','error');}
}
function choose(value){selectedStart=value;selectedLabel.textContent=formatSlot(value);timeStep.hidden=true;details.hidden=false;setProgress(1);setStatus('');details.elements.name.focus();}
back.addEventListener('click',()=>{selectedStart='';details.hidden=true;timeStep.hidden=false;setProgress(0);setStatus('');});
dateInput.addEventListener('change',loadTimes);
details.addEventListener('submit',async event=>{
 event.preventDefault();if(!selectedStart||!details.reportValidity()||submit.disabled)return;const data=Object.fromEntries(new FormData(details));if(data._gotcha)return;submit.disabled=true;submit.textContent='Confirming…';setStatus('Creating your meeting…');
 try{const response=await fetch(bookingEndpoint,{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify({...data,start:selectedStart,token})}),result=await response.json().catch(()=>({}));if(!response.ok||result.ok!==true)throw new Error(result.error||'The booking could not be confirmed.');details.hidden=true;success.hidden=false;confirmLabel.textContent=formatSlot(result.start);setProgress(2);setStatus('');success.focus({preventScroll:true});}
 catch(error){setStatus(error.message||'The booking could not be confirmed.','error');if(/refresh|taken|available/i.test(error.message||'')){await init();details.hidden=true;timeStep.hidden=false;setProgress(0);}}
 finally{submit.disabled=false;submit.innerHTML='Confirm conversation <span>↗</span>';}
});
init();
})();
