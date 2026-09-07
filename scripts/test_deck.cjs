const fs=require('fs'),vm=require('vm'),assert=require('assert');
function el(id){return {id,dataset:{},style:{},value:'',textContent:'',attrs:{},events:{},classList:{items:new Set(),add(x){this.items.add(x)},toggle(x,on){if(on===undefined)on=!this.items.has(x);if(on)this.items.add(x);else this.items.delete(x)}},setAttribute(k,v){this.attrs[k]=v},addEventListener(k,fn){this.events[k]=fn},top:0,getBoundingClientRect(){return {top:this.top}},scrollIntoView(){}}}
const ids=['slide-select','previous','next','slide-count','motion-toggle','reading-toggle','print-deck','progress','maturity-score','maturity-name','maturity-confidence','maturity-reason','maturity-change','ai-operating-cost','ai-cost-output','ai-cost','ai-net','ai-benefit-retention','ai-retention-output','ai-stress-note'];
const nodes=Object.fromEntries(ids.map(x=>[x,el(x)]));nodes['ai-operating-cost'].value='52000';nodes['ai-benefit-retention'].value='100';
const slides=Array.from({length:16},(_,i)=>el('slide-'+i));
const passes=['initial','reconciled'].map(pass=>Object.assign(el(pass),{dataset:{pass}}));
const track=Array.from({length:5},()=>el('bar'));const controls=el('controls');const body=el('body');
const doc={body,getElementById:id=>nodes[id],querySelector:s=>s.includes("cost-answer")?el("cost-description"):controls,querySelectorAll:s=>s==='.slide'?slides:s==='[data-pass]'?passes:track,addEventListener(){},dispatchEvent(){}};
const windowEvents={};
const context={document:doc,matchMedia:()=>({matches:false,addEventListener(){}}),location:{hash:''},history:{replaceState(){}},window:{innerHeight:800,addEventListener(type,fn){windowEvents[type]=fn},scrollTo(){},print(){}},requestAnimationFrame:fn=>fn(),IntersectionObserver:class{observe(){}},CustomEvent:class{},Intl};
vm.runInNewContext(fs.readFileSync('assets/deck.js','utf8'),context);
assert.equal(nodes['ai-cost'].textContent,'$52M');assert.equal(nodes['ai-net'].textContent,'$2M');
for(const [input,expected] of [['44000','$10M'],['60000','-$6M']]){nodes['ai-operating-cost'].value=input;nodes['ai-operating-cost'].events.input();assert.equal(nodes['ai-net'].textContent,expected)}
// The downside can exceed the original margin even with costs unchanged.
nodes['ai-operating-cost'].value='52000';nodes['ai-benefit-retention'].value='90';nodes['ai-benefit-retention'].events.input();
assert.equal(nodes['ai-net'].textContent,'-$3.4M');assert(nodes['ai-stress-note'].textContent.includes('96.3%'));
nodes['ai-operating-cost'].value='44000';nodes['ai-benefit-retention'].value='70';nodes['ai-benefit-retention'].events.input();assert.equal(nodes['ai-net'].textContent,'-$6.2M');
passes[1].events.click();assert.equal(nodes['maturity-name'].textContent,'Ad hoc');assert.equal(nodes['maturity-confidence'].textContent,'Evidence confidence: strong');assert.equal(track.filter(x=>x.classList.items.has('filled')).length,1);
passes[0].events.click();assert.equal(track.filter(x=>x.classList.items.has('filled')).length,2);
nodes['next'].events.click();assert.equal(nodes['slide-count'].textContent,'02 / 16');assert(slides[0].inert);assert(!slides[1].inert);
nodes['reading-toggle'].events.click();assert(slides.every(s=>!s.inert));
// A very tall slide remains current until the next slide reaches the viewport marker.
slides.forEach((slide,i)=>slide.top=i<3?-10000:i===3?-3000:2000+(i-4)*700);
windowEvents.scroll();assert.equal(nodes['slide-count'].textContent,'04 / 16');
slides[4].top=200;windowEvents.scroll();assert.equal(nodes['slide-count'].textContent,'05 / 16');
console.log('Interactions pass: sensitivity endpoints, assessment passes, navigation, and read-all state. DOM-stub validation; browser visual checks are separate.');
