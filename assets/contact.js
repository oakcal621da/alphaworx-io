(() => {
'use strict';
const dialog=document.getElementById('contact-dialog');if(!dialog||!dialog.showModal)return;
const form=document.getElementById('contact-form'),submit=document.getElementById('contact-submit'),status=document.getElementById('contact-status'),note=document.getElementById('contact-delivery-note'),topic=document.getElementById('contact-topic'),head=document.getElementById('contact-dialog-head'),success=document.getElementById('contact-success'),successTitle=document.getElementById('contact-success-title');
const configURL=new URL(window.ALPHAWORX_CONTACT_CONFIG_URL||'/api/contact/config',location.href);
let endpoint='',formToken='';
let opener=null,sending=false,topicChosen=false,loading=false;
async function loadDelivery(){
 if(loading)return;
 loading=true;
 submit.disabled=true;submit.textContent='Checking delivery…';
 const controller=new AbortController(),timeout=setTimeout(()=>controller.abort(),5000);
 try{
  const response=await fetch(configURL,{headers:{Accept:'application/json'},cache:'no-store',signal:controller.signal});
  const config=response.ok?await response.json():null;
  if(config?.enabled&&typeof config.token==='string'&&typeof config.endpoint==='string'){
   const target=new URL(config.endpoint,configURL);
   if(target.origin!==configURL.origin)throw new Error('Unexpected endpoint');
   endpoint=target.href;formToken=config.token;
  }else{endpoint='';formToken='';}
 }catch(error){endpoint='';formToken='';}
 finally{
  clearTimeout(timeout);loading=false;submit.disabled=false;
  submit.textContent=endpoint?'Send inquiry ↗':'Continue in email ↗';
  note.textContent=endpoint?'We’ll use these details to respond to your inquiry.':'Your details will open in an email draft to info@alphaworx.io. Send it from your email app.';
 }
}
loadDelivery();
topic.addEventListener('change',()=>{topicChosen=true;});
// A contact link from an article or the deck opens the same form on arrival.
if(location.hash==='#contact'){document.body.classList.add('contact-open');dialog.showModal();}

function setStatus(message,state='info'){status.textContent=message;status.dataset.state=state;}
function showSuccess(){head.hidden=true;form.hidden=true;success.hidden=false;dialog.setAttribute('aria-labelledby','contact-success-title');dialog.removeAttribute('aria-describedby');successTitle.focus({preventScroll:true});}
function resetView(){head.hidden=false;form.hidden=false;success.hidden=true;dialog.setAttribute('aria-labelledby','contact-title');dialog.setAttribute('aria-describedby','contact-description');}
function close(){dialog.close();}
dialog.querySelectorAll('[data-close-contact]').forEach(b=>b.addEventListener('click',close));
dialog.addEventListener('close',()=>{document.body.classList.remove('contact-open');resetView();opener?.focus({preventScroll:true});});
dialog.addEventListener('click',event=>{if(event.target!==dialog)return;const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)close();});
function inferredTopic(subject){
 if(/assessment/i.test(subject))return 'AI strategy assessment';
 if(/growth/i.test(subject))return 'AI for growth';
 if(/efficiency/i.test(subject))return 'AI for efficiency';
 if(/customer experience/i.test(subject))return 'Customer experience';
 if(/resilience/i.test(subject))return 'Operational resilience';
 return 'General conversation';
}
document.addEventListener('click',event=>{
 const link=event.target.closest('a[href]');if(!link||event.defaultPrevented||event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
 const url=new URL(link.href,location.href);
 const email=url.protocol==='mailto:'&&url.pathname.toLowerCase()==='info@alphaworx.io';
 const contact=url.origin===location.origin&&url.pathname===location.pathname&&url.hash==='#contact';
 if(!email&&!contact)return;
 event.preventDefault();opener=link;
 if(!topicChosen)topic.value=inferredTopic(url.searchParams.get('subject')||'');
 document.body.classList.add('contact-open');dialog.showModal();
 if(!sending&&!formToken)loadDelivery();
});
form.addEventListener('submit',async event=>{
 event.preventDefault();if(sending||loading||!form.reportValidity())return;
 const data=Object.fromEntries(new FormData(form));
 if(data._gotcha)return;
 if(!data.name.trim()||!data.message.trim()){setStatus('Please enter your name and a short description of what you’d like to discuss.','error');return;}
 const subject='Alphaworx inquiry: '+data.topic;
 if(!endpoint){
 const body=`Name: ${data.name.trim()}\nWork email: ${data.email.trim()}\nCompany: ${data.company.trim()||'Not provided'}\nRole: ${data.role.trim()||'Not provided'}\nTopic: ${data.topic}\n\n${data.message.trim()}`;
 location.href='mailto:info@alphaworx.io?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(body);
 setStatus('Your email app should open with the draft. Send it there to complete your inquiry; your details remain in this form if you need them.');return;
 }
 sending=true;submit.disabled=true;submit.textContent='Sending…';setStatus('');
 const controller=new AbortController(),timeout=setTimeout(()=>controller.abort(),65000);
 try{
 const response=await fetch(endpoint,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify({...data,token:formToken}),signal:controller.signal});
 const result=await response.json().catch(()=>({}));
 if(response.status===403)formToken='';
 if(!response.ok||result.ok!==true)throw new Error(result.error||'We couldn’t confirm delivery. Please try again later or email info@alphaworx.io directly.');
 form.reset();topicChosen=false;formToken='';setStatus('');showSuccess();
 }catch(error){setStatus(error.name==='AbortError'?'Delivery is taking longer than expected. Your details are still here. Please email info@alphaworx.io if you need to check delivery.':error instanceof TypeError?'We couldn’t connect to send your inquiry. Your details are still here. Please try again or email info@alphaworx.io.':error.message,'error');}
 finally{clearTimeout(timeout);sending=false;submit.disabled=false;submit.textContent='Send inquiry ↗';if(!formToken)loadDelivery();}
});
})();
