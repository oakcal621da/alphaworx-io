const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

class Element {
  constructor(id = '') { this.id=id; this.hidden=false; this.disabled=false; this.textContent=''; this.dataset={}; this.listeners={}; this.value='General conversation'; this.attrs={}; }
  addEventListener(type, fn) { (this.listeners[type] ||= []).push(fn); }
  dispatch(type, event={}) { for (const fn of this.listeners[type] || []) fn({preventDefault(){},target:this,...event}); }
  querySelectorAll(selector) { return selector==='[data-close-contact]' ? this.closeButtons : []; }
  setAttribute(name,value) { this.attrs[name]=value; }
  removeAttribute(name) { delete this.attrs[name]; }
  showModal() { this.open=true; }
  close() { this.open=false; this.dispatch('close'); }
  getBoundingClientRect() { return {left:0,right:600,top:0,bottom:600}; }
  focus() { this.focused=true; }
  reset() { this.resetCalled=true; }
  reportValidity() { return true; }
}

const ids=['contact-dialog','contact-form','contact-submit','contact-status','contact-delivery-note','contact-topic','contact-dialog-head','contact-success','contact-success-title'];
const elements=Object.fromEntries(ids.map(id=>[id,new Element(id)]));
elements['contact-success'].hidden=true;
const closeButton=new Element('success-close');
elements['contact-dialog'].closeButtons=[closeButton];
elements['contact-form'].formData={name:'Avery Stone',email:'avery@example.com',company:'Meridian',role:'COO',topic:'AI strategy assessment',message:'Discuss our AI operating model.',_gotcha:''};

let fetchCount=0;
const context={
  document:{getElementById:id=>elements[id],addEventListener(){},body:{classList:{add(){},remove(){}}}},
  window:{ALPHAWORX_CONTACT_CONFIG_URL:'/api/contact/config'},
  location:{href:'https://alphaworx.io/',hash:'',origin:'https://alphaworx.io',pathname:'/'},
  URL,AbortController,clearTimeout,setTimeout,
  FormData:class { constructor(form){return new Map(Object.entries(form.formData));} },
  Object,JSON,encodeURIComponent,
  fetch:async()=>++fetchCount===1
    ? {ok:true,json:async()=>({enabled:true,token:'test-token',endpoint:'/api/contact'})}
    : {ok:true,status:200,json:async()=>({ok:true})},
};
vm.runInNewContext(fs.readFileSync('assets/contact.js','utf8'),context);

setImmediate(async()=>{
  elements['contact-form'].dispatch('submit');
  await new Promise(resolve=>setImmediate(resolve));
  assert.equal(elements['contact-form'].hidden,true);
  assert.equal(elements['contact-dialog-head'].hidden,true);
  assert.equal(elements['contact-success'].hidden,false);
  assert.equal(elements['contact-success-title'].focused,true);
  assert.equal(elements['contact-dialog'].attrs['aria-labelledby'],'contact-success-title');
  assert.equal(elements['contact-dialog'].attrs['aria-describedby'],undefined);
  assert.equal(elements['contact-form'].resetCalled,true);
  closeButton.dispatch('click');
  assert.equal(elements['contact-form'].hidden,false);
  assert.equal(elements['contact-success'].hidden,true);
  assert.equal(elements['contact-dialog'].attrs['aria-labelledby'],'contact-title');
  console.log('Contact success state verified.');
});
