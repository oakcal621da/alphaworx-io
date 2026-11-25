// DOM-stub test of public/assets/apply.js: the Apply link opens the form, a send posts to /api/apply with the role
// and form token and shows the success view, and without the contact service the form falls back to an email draft.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

class Element {
  constructor(id = '') { this.id=id; this.hidden=false; this.disabled=false; this.textContent=''; this.dataset={}; this.listeners={}; this.attrs={}; }
  addEventListener(type, fn) { (this.listeners[type] ||= []).push(fn); }
  async dispatch(type, event={}) { for (const fn of this.listeners[type] || []) await fn({preventDefault(){},target:this,...event}); }
  querySelectorAll(selector) { return selector==='[data-close-apply]' ? this.closeButtons : []; }
  setAttribute(name,value) { this.attrs[name]=value; }
  removeAttribute(name) { delete this.attrs[name]; }
  showModal() { this.open=true; }
  close() { this.open=false; this.dispatch('close'); }
  getBoundingClientRect() { return {left:0,right:600,top:0,bottom:600}; }
  focus() { this.focused=true; }
  reset() { this.resetCalled=true; }
  reportValidity() { return true; }
}

function run({ enabled }) {
  const ids=['apply-dialog','apply-form','apply-submit','apply-status','apply-delivery-note','apply-dialog-head','apply-success','apply-success-title'];
  const el=Object.fromEntries(ids.map(id=>[id,new Element(id)]));
  el['apply-success'].hidden=true;
  el['apply-dialog'].closeButtons=[new Element('close')];
  el['apply-form'].formData={position:'Account Executive, United States',name:'Avery Stone',email:'avery@example.com',link:'https://www.linkedin.com/in/avery',message:'Ten years selling GRC software.',_gotcha:''};
  const calls=[]; let pageClick=null;
  const location={href:'https://alphaworx.io/careers/account-executive-us.html',origin:'https://alphaworx.io',hash:'',pathname:'/careers/account-executive-us.html'};
  const context={
    document:{getElementById:id=>el[id],addEventListener(type,fn){if(type==='click')pageClick=fn;},body:{classList:{add(){},remove(){}}}},
    window:{ALPHAWORX_CONTACT_CONFIG_URL:'https://alphaworx-contact.onrender.com/api/contact/config'},
    location,URL,AbortController,clearTimeout,setTimeout,Object,JSON,encodeURIComponent,
    FormData:class { constructor(form){return new Map(Object.entries(form.formData));} },
    fetch:async(url,options={})=>{calls.push({url:String(url),options});
      return calls.length===1 ? {ok:true,json:async()=>(enabled?{enabled:true,token:'test-token',endpoint:'/api/contact'}:{enabled:false})}
                              : {ok:true,status:200,json:async()=>({ok:true})};},
  };
  vm.runInNewContext(fs.readFileSync('public/assets/apply.js','utf8'),context);
  return {el,calls,location,click:()=>pageClick({target:{closest:s=>s==='[data-apply]'?{focus(){}}:null},button:0,preventDefault(){}})};
}

(async () => {
  // With the service: the link opens the dialog, the send goes to /api/apply on the service, success replaces the form.
  let t=run({enabled:true});
  t.click();
  assert.equal(t.el['apply-dialog'].open,true);
  await new Promise(r=>setTimeout(r,0));
  assert.equal(t.calls[0].url,'https://alphaworx-contact.onrender.com/api/contact/config');
  assert.equal(t.el['apply-submit'].textContent,'Send application ↗');
  await t.el['apply-form'].dispatch('submit');
  assert.equal(t.calls[1].url,'https://alphaworx-contact.onrender.com/api/apply');
  const sent=JSON.parse(t.calls[1].options.body);
  assert.equal(sent.position,'Account Executive, United States');
  assert.equal(sent.link,'https://www.linkedin.com/in/avery');
  assert.equal(sent.token,'test-token');
  assert.equal(t.el['apply-success'].hidden,false);
  assert.equal(t.el['apply-form'].hidden,true);
  assert.equal(t.el['apply-form'].resetCalled,true);

  // Without the service: the button offers an email draft to jobs@ with the role as the subject; nothing is posted.
  t=run({enabled:false});
  t.click();
  await new Promise(r=>setTimeout(r,0));
  assert.equal(t.el['apply-submit'].textContent,'Continue in email ↗');
  await t.el['apply-form'].dispatch('submit');
  assert.equal(t.calls.length,1);
  assert.match(t.location.href,/^mailto:jobs@alphaworx\.io\?subject=Account%20Executive%2C%20United%20States&body=/);
  assert.match(decodeURIComponent(t.location.href),/linkedin\.com\/in\/avery/);
  console.log('apply form: ok');
})().catch(e=>{console.error(e);process.exit(1);});
