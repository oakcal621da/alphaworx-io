// Scheduler: a slow response for an earlier day must never fill the list for the day now selected.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

function el(id) {
  return {
    id, hidden: false, disabled: false, textContent: '', innerHTML: '', value: '', min: '', max: '', dataset: {},
    children: [], listeners: {}, elements: { name: { focus() {} } }, classList: { toggle() {} },
    addEventListener(type, fn) { this.listeners[type] = fn; },
    setAttribute() {}, focus() {}, reportValidity() { return true; },
    replaceChildren(...nodes) { this.children = nodes; },
    append(...nodes) { this.children.push(...nodes); },
    querySelectorAll() { return []; },
  };
}
const ids = ['schedule-booker', 'booker-status', 'time-step', 'details-step', 'booking-success', 'booking-fallback',
  'schedule-date', 'time-options', 'schedule-time-zone', 'selected-time', 'confirmation-time', 'book-submit', 'booker-back'];
const nodes = Object.fromEntries(ids.map(id => [id, el(id)]));
const pending = {};
function json(body, ok = true) { return { ok, json: async () => body }; }
async function fetchStub(url) {
  url = new URL(url);
  if (url.pathname === '/api/schedule/config') {
    return json({ enabled: true, token: 't', availabilityEndpoint: '/api/schedule/availability', bookingEndpoint: '/api/schedule/book' });
  }
  // Availability: resolved by the test, in whatever order it chooses. The abort signal is ignored on purpose,
  // so the guard has to hold even when an old response still arrives.
  return new Promise(resolve => { pending[url.searchParams.get('date')] = slots => resolve(json({ slots })); });
}
const context = {
  document: { getElementById: id => nodes[id], createElement: () => el('') },
  window: {}, location: { origin: 'https://alphaworx.io' }, fetch: fetchStub, URL, Intl, Date, FormData: class {},
  AbortController, setTimeout, clearTimeout, console,
};
vm.runInNewContext(fs.readFileSync('public/assets/schedule.js', 'utf8'), context);
const tick = () => new Promise(resolve => setImmediate(resolve));

(async () => {
  await tick(); await tick();
  const date = nodes['schedule-date'], times = nodes['time-options'], status = nodes['booker-status'];
  pending[date.value](['2026-12-01T15:00:00Z']);           // the first day loads normally
  await tick(); await tick();
  assert.equal(times.children.length, 1);

  date.value = '2026-12-02'; date.listeners.change();      // visitor picks day A …
  await tick();
  date.value = '2026-12-03'; date.listeners.change();      // … then day B before A answers
  await tick();
  pending['2026-12-03'](['2026-12-03T16:00:00Z']);         // B answers first
  await tick(); await tick();
  pending['2026-12-02'](['2026-12-02T15:00:00Z', '2026-12-02T17:00:00Z']); // A answers late
  await tick(); await tick();

  assert.equal(times.children.length, 1, 'only the selected day’s times are shown');
  assert.equal(status.textContent, '1 times available');
  console.log('Scheduler keeps only the selected day’s times when responses arrive out of order.');
})().catch(error => { console.error(error); process.exit(1); });
