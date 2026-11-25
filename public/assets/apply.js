(() => {
'use strict';
// Application form on each role page (careers/<slug>.html). It posts to the contact service's /api/apply.
// It sends multipart form data so a résumé file (PDF or Word, up to 5 MB) can travel with the details.
// Without the service, or without this script, the Apply links stay plain email links to jobs@alphaworx.io.
const dialog=document.getElementById('apply-dialog');if(!dialog||!dialog.showModal)return;
const form=document.getElementById('apply-form'),resumeInput=document.getElementById('apply-resume'),submit=document.getElementById('apply-submit'),status=document.getElementById('apply-status'),note=document.getElementById('apply-delivery-note'),head=document.getElementById('apply-dialog-head'),success=document.getElementById('apply-success'),successTitle=document.getElementById('apply-success-title');
const configURL=new URL(window.ALPHAWORX_CONTACT_CONFIG_URL||'/api/contact/config',location.href);
let endpoint='',formToken='',opener=null,sending=false,loading=false;
const MAX_RESUME=5*1024*1024,RESUME_TYPES=/\.(pdf|docx?)$/i;
async function loadDelivery(){
 if(loading)return;
 loading=true;submit.disabled=true;submit.textContent='Checking delivery…';
 const controller=new AbortController(),timeout=setTimeout(()=>controller.abort(),5000);
 try{
  const response=await fetch(configURL,{headers:{Accept:'application/json'},cache:'no-store',signal:controller.signal});
  const config=response.ok?await response.json():null;
  if(config?.enabled&&typeof config.token==='string'){endpoint=new URL('/api/apply',configURL).href;formToken=config.token;}
  else{endpoint='';formToken='';}
 }catch(error){endpoint='';formToken='';}
 finally{
  clearTimeout(timeout);loading=false;submit.disabled=false;
  submit.textContent=endpoint?'Send application ↗':'Continue in email ↗';
  note.textContent=endpoint?'':'Your details will open in an email draft to jobs@alphaworx.io. Attach your résumé there and send it from your email app.';
 }
}
function setStatus(message,state='info'){status.textContent=message;status.dataset.state=state;}
function checkResume(){
 const file=resumeInput.files&&resumeInput.files[0];
 if(!file)return '';
 if(!RESUME_TYPES.test(file.name))return 'Please attach your résumé as a PDF or Word document.';
 if(file.size>MAX_RESUME)return 'Your résumé is too large. Please attach a file under 5 MB.';
 return '';
}
resumeInput.addEventListener('change',()=>{const problem=checkResume();setStatus(problem,problem?'error':'info');});
function showSuccess(){head.hidden=true;form.hidden=true;success.hidden=false;dialog.setAttribute('aria-labelledby','apply-success-title');dialog.removeAttribute('aria-describedby');successTitle.focus({preventScroll:true});}
function resetView(){head.hidden=false;form.hidden=false;success.hidden=true;dialog.setAttribute('aria-labelledby','apply-title');dialog.setAttribute('aria-describedby','apply-description');}
function close(){dialog.close();}
dialog.querySelectorAll('[data-close-apply]').forEach(b=>b.addEventListener('click',close));
dialog.addEventListener('close',()=>{document.body.classList.remove('contact-open');resetView();opener?.focus({preventScroll:true});});
dialog.addEventListener('click',event=>{if(event.target!==dialog)return;const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)close();});
document.addEventListener('click',event=>{
 const link=event.target.closest('[data-apply]');if(!link||event.defaultPrevented||event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
 event.preventDefault();opener=link;
 document.body.classList.add('contact-open');dialog.showModal();
 if(!sending&&!formToken)loadDelivery();
});
form.addEventListener('submit',async event=>{
 event.preventDefault();if(sending||loading||!form.reportValidity())return;
 const body=new FormData(form),data=Object.fromEntries(body);
 if(data._gotcha)return;
 const hasFile=!!(resumeInput.files&&resumeInput.files[0]);
 if(!data.name.trim()){setStatus('Please enter your name.','error');return;}
 const problem=checkResume();if(problem){setStatus(problem,'error');return;}
 if(!hasFile&&!data.link.trim()){setStatus('Please attach your résumé or add a link to it or to your LinkedIn profile.','error');return;}
 if(!endpoint){
  const draft=`Name: ${data.name.trim()}\nEmail: ${data.email.trim()}\nLink: ${data.link.trim()||'Not provided'}\n\n${data.message.trim()}`;
  location.href='mailto:jobs@alphaworx.io?subject='+encodeURIComponent(data.position)+'&body='+encodeURIComponent(draft);
  setStatus('Your email app should open with the draft. Attach your résumé there and send it to complete your application; your details remain in this form if you need them.');return;
 }
 sending=true;submit.disabled=true;submit.textContent='Sending…';setStatus('');
 const controller=new AbortController(),timeout=setTimeout(()=>controller.abort(),65000);
 try{
  if(!hasFile)body.delete('resume');
  body.set('token',formToken);
  const response=await fetch(endpoint,{method:'POST',headers:{'Accept':'application/json'},body,signal:controller.signal});
  const result=await response.json().catch(()=>({}));
  if(response.status===403)formToken='';
  if(!response.ok||result.ok!==true)throw new Error(result.error||'We couldn’t confirm delivery. Please try again later or email jobs@alphaworx.io directly.');
  form.reset();formToken='';setStatus('');showSuccess();
 }catch(error){setStatus(error.name==='AbortError'?'Delivery is taking longer than expected. Your details are still here. Please email jobs@alphaworx.io if you need to check delivery.':error instanceof TypeError?'We couldn’t connect to send your application. Your details are still here. Please try again or email jobs@alphaworx.io.':error.message,'error');}
 finally{clearTimeout(timeout);sending=false;submit.disabled=false;submit.textContent='Send application ↗';if(!formToken)loadDelivery();}
});
})();
