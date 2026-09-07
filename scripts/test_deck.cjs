const fs=require('fs'),vm=require('vm'),assert=require('assert');
function el(id){return {id,dataset:{},style:{},value:'',textContent:'',attrs:{},events:{},classList:{items:new Set(),add(x){this.items.add(x)},toggle(x,on){if(on===undefined)on=!this.items.has(x);if(on)this.items.add(x);else this.items.delete(x)}},setAttribute(k,v){this.attrs[k]=v},addEventListener(k,fn){this.events[k]=fn},scrollIntoView(){}}}
const ids=['slide-select','previous','next','slide-count','motion-toggle','reading-toggle','print-deck','progress','maturity-score','maturity-name','maturity-confidence','maturity-reason','maturity-change','ai-operating-cost','ai-cost-output','ai-cost','ai-net'];
const nodes=Object.fromEntries(ids.map(x=>[x,el(x)]));nodes['ai-operating-cost'].value='52000';
const slides=Array.from({length:16},(_,i)=>el('slide-'+i));
const passes=['initial','reconciled'].map(pass=>Object.assign(el(pass),{dataset:{pass}}));
const track=Array.from({length:5},()=>el('bar'));const controls=el('controls');const body=el('body');
const doc={body,getElementById:id=>nodes[id],querySelector:s=>s.includes("cost-answer")?el("cost-description"):controls,querySelectorAll:s=>s==='.slide'?slides:s==='[data-pass]'?passes:track,addEventListener(){},dispatchEvent(){}};
const context={document:doc,matchMedia:()=>({matches:false,addEventListener(){}}),location:{hash:''},history:{replaceState(){}},window:{addEventListener(){},scrollTo(){},print(){}},IntersectionObserver:class{observe(){}},CustomEvent:class{},Intl};
vm.runInNewContext(fs.readFileSync('assets/deck.js','utf8'),context);
assert.equal(nodes['ai-cost'].textContent,'$52M');assert.equal(nodes['ai-net'].textContent,'$2M');
for(const [input,expected] of [['44000','$10M'],['60000','-$6M']]){nodes['ai-operating-cost'].value=input;nodes['ai-operating-cost'].events.input();assert.equal(nodes['ai-net'].textContent,expected)}
passes[1].events.click();assert.equal(nodes['maturity-name'].textContent,'Ad hoc');assert.equal(nodes['maturity-confidence'].textContent,'Evidence confidence: strong');assert.equal(track.filter(x=>x.classList.items.has('filled')).length,1);
passes[0].events.click();assert.equal(track.filter(x=>x.classList.items.has('filled')).length,2);
nodes['next'].events.click();assert.equal(nodes['slide-count'].textContent,'02 / 16');assert(slides[0].inert);assert(!slides[1].inert);
nodes['reading-toggle'].events.click();assert(slides.every(s=>!s.inert));
console.log('Interactions pass: sensitivity endpoints, assessment passes, navigation, and read-all state. DOM-stub validation; browser visual checks are separate.');
