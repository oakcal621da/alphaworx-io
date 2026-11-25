// Behavior of the AIOS Cloud workspace tabs (public/assets/site/aios-cloud.js) against a DOM stub.
// It checks the logic only; what the page looks like still needs a real browser.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

class El {
  constructor(props = {}) { this.listeners = {}; this.attrs = {}; this.dataset = {}; this.hidden = false; Object.assign(this, props); }
  addEventListener(type, fn) { (this.listeners[type] ||= []).push(fn); }
  dispatch(type, event = {}) { for (const fn of [...(this.listeners[type] || [])]) fn({ preventDefault() { this.prevented = true; }, ...event }); }
  setAttribute(name, value) { this.attrs[name] = String(value); }
  getAttribute(name) { return name in this.attrs ? this.attrs[name] : null; }
  removeAttribute(name) { delete this.attrs[name]; }
  focus() { El.focused = this; }
  querySelector(selector) { return this.children[selector] || null; }
}

function setup(hash = '') {
  const requested = [];           // every screenshot the script asks for, in order
  class FakeImage extends El {
    constructor() { super(); this.complete = false; requested.push(this); }
    arrive(type = 'load') { this.complete = type === 'load'; this.dispatch(type); }
  }
  const names = ['command-center', 'risk-register', 'policy-workflow'];
  const list = new El();
  const panels = {};
  const tabs = names.map((name, i) => {
    const tab = new El({ id: `heading-${name}`, parentNode: list });
    tab.dataset = { img: `/img/${name}.webp?h=1`, full: `/img/${name}-full.webp?h=2`, alt: `${name} screenshot`, label: name };
    tab.setAttribute('aria-selected', i === 0 ? 'true' : 'false');
    tab.setAttribute('aria-controls', `panel-${name}`);
    panels[`panel-${name}`] = new El({ hidden: i !== 0 });
    return tab;
  });
  const img = new El({ sizes: '90vw', src: tabs[0].dataset.img, alt: tabs[0].dataset.alt });
  const label = new El({ textContent: names[0] });
  const screen = new El({ children: { img, '.ws-label': label } });
  const win = new El();
  const location = { hash };
  vm.runInNewContext(fs.readFileSync('public/assets/site/aios-cloud.js', 'utf8'), {
    document: {
      querySelectorAll: (s) => (s === '.anat-tab' ? tabs : []),
      querySelector: (s) => (s === '.anat-shot .screen' ? screen : null),
      getElementById: (id) => panels[id] || null,
    },
    window: win, location, Image: FakeImage,
  });
  return { tabs, panels, list, img, label, screen, requested, win, location };
}
const selected = (t) => t.tabs.map((tab) => tab.getAttribute('aria-selected')).join(',');

// 1. Loading the page asks for no screenshot.
let t = setup();
assert.equal(t.requested.length, 0);

// 2. Reaching for the tabs fetches the two hidden screenshots, once.
t.list.dispatch('pointerenter');
assert.deepEqual(t.requested.map((im) => im.src), [t.tabs[1].dataset.img, t.tabs[2].dataset.img]);
assert.equal(t.requested[0].srcset, `${t.tabs[1].dataset.img} 1600w, ${t.tabs[1].dataset.full} 2560w`);
assert.equal(t.requested[0].sizes, '90vw');
assert.equal(t.list.listeners.pointerenter.length, 1); // registered with {once:true}; the stub does not remove it
t.tabs[1].dispatch('click'); t.tabs[2].dispatch('click');
assert.equal(t.requested.length, 2, 'a screenshot is requested once, however often its tab is chosen');

// 3. Choosing a tab whose screenshot has not arrived keeps the current one and marks the frame busy.
t = setup();
t.tabs[1].dispatch('click');
assert.equal(selected(t), 'false,true,false');
assert.equal(t.panels['panel-risk-register'].hidden, false);
assert.equal(t.panels['panel-command-center'].hidden, true);
assert.equal(t.label.textContent, 'risk-register');
assert.equal(t.img.src, t.tabs[0].dataset.img, 'the previous screenshot stays until the new one loads');
assert.equal(t.screen.getAttribute('aria-busy'), 'true');
t.requested[0].arrive();
assert.equal(t.img.src, t.tabs[1].dataset.img);
assert.equal(t.img.alt, 'risk-register screenshot');
assert.equal(t.screen.getAttribute('data-full'), t.tabs[1].dataset.full);
assert.equal(t.screen.getAttribute('aria-busy'), null);

// 4. The tab chosen last wins, whichever screenshot arrives first.
t = setup();
t.tabs[1].dispatch('click'); t.tabs[2].dispatch('click');
const [risk, policy] = t.requested;
policy.arrive();
assert.equal(t.img.src, t.tabs[2].dataset.img);
risk.arrive();
assert.equal(t.img.src, t.tabs[2].dataset.img, 'a slower earlier choice must not replace the later one');
assert.equal(selected(t), 'false,false,true');

// 5. A screenshot that fails still clears the busy state and takes the tab's alt text.
t = setup();
t.tabs[1].dispatch('click');
t.requested[0].arrive('error');
assert.equal(t.screen.getAttribute('aria-busy'), null);
assert.equal(t.img.alt, 'risk-register screenshot');

// 6. A screenshot already loaded is shown at once.
t = setup();
t.list.dispatch('focusin');
t.requested.forEach((im) => im.arrive());
t.tabs[2].dispatch('click');
assert.equal(t.img.src, t.tabs[2].dataset.img);
assert.equal(t.screen.getAttribute('aria-busy'), null);

// 7. Arrow keys move the selection and the focus, wrapping at both ends.
t = setup();
const down = { key: 'ArrowDown', prevented: false, preventDefault() { this.prevented = true; } };
t.tabs[0].listeners.keydown[0](down);
assert.equal(down.prevented, true);
assert.equal(selected(t), 'false,true,false');
assert.equal(El.focused, t.tabs[1]);
t.tabs[0].listeners.keydown[0]({ key: 'ArrowUp', preventDefault() {} });
assert.equal(selected(t), 'false,false,true');
t.tabs[0].listeners.keydown[0]({ key: 'Enter', preventDefault() { throw new Error('other keys are left alone'); } });
assert.equal(selected(t), 'false,false,true');

// 8. A link to a tab opens it, on load and when the address changes.
t = setup('#heading-policy-workflow');
assert.equal(selected(t), 'false,false,true');
assert.equal(t.requested.length, 1);
t.location.hash = '#heading-risk-register';
t.win.dispatch('hashchange');
assert.equal(selected(t), 'false,true,false');
t.location.hash = '#not-a-tab';
t.win.dispatch('hashchange');
assert.equal(selected(t), 'false,true,false');

console.log('aios tabs: ok');
