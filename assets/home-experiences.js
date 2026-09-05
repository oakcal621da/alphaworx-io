(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let motionPaused = reduced.matches;
  const motionButton = document.querySelector('.motion-toggle');
  function setMotion(paused) {
    motionPaused = paused;
    document.body.classList.toggle('motion-paused', paused);
    motionButton.textContent = paused ? 'Play motion ▷' : 'Pause motion Ⅱ';
    motionButton.setAttribute('aria-pressed', String(paused));
    document.dispatchEvent(new CustomEvent('alphaworx:motion', { detail: { paused } }));
  }
  motionButton.hidden = false;
  motionButton.addEventListener('click', () => setMotion(!motionPaused));
  reduced.addEventListener('change', event => setMotion(event.matches));
  setMotion(motionPaused);

  const menu = document.querySelector('.menu-toggle');
  const nav = document.getElementById('site-nav');
  menu.hidden = false;
  function closeMenu() { nav.classList.remove('is-open'); menu.setAttribute('aria-expanded', 'false'); menu.textContent = 'Menu ＋'; }
  menu.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    nav.classList.toggle('is-open', open); menu.setAttribute('aria-expanded', String(open)); menu.textContent = open ? 'Close ×' : 'Menu ＋';
  });
  nav.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
  document.addEventListener('keydown', event => { if (event.key === 'Escape' && nav.classList.contains('is-open')) { closeMenu(); menu.focus(); } });

  const priorities = {
    growth: {
      category: 'Commercial teams', scenario: 'Help expertise reach the next customer.',
      description: 'Bring approved research, product knowledge, and customer context into the proposal process, with an accountable commercial owner.',
      value: 'More capacity for relevant, well-informed proposals.',
      decision: 'Which customer segments deserve the investment—and who owns proposal quality?',
      measure: 'Proposal cycle time, qualified conversion, and review rework.',
      flow: ['Customer context', 'Relevant proposal', 'Commercial review'], subject: 'Exploring AI for growth'
    },
    efficiency: {
      category: 'Operations & procurement', scenario: 'Give people more time for the exceptions.',
      description: 'Help teams classify incoming documents, check them against approved records, and route discrepancies to the right person.',
      value: 'Less repetitive handling and more attention on work that needs judgment.',
      decision: 'Which checks can be delegated, and how will released capacity be put to use?',
      measure: 'End-to-end cycle time, exception accuracy, rework, and capacity actually redeployed.',
      flow: ['Incoming documents', 'Match & flag', 'Resolve exceptions'], subject: 'Exploring AI for efficiency'
    },
    experience: {
      category: 'Customer service', scenario: 'Make a useful answer easier to deliver.',
      description: 'Connect a service request to approved knowledge and customer context, then help the team prepare a response they can verify.',
      value: 'More consistent support with less time spent searching across systems.',
      decision: 'What may the AI communicate, and when must a person review or take over?',
      measure: 'Resolution quality, repeat contacts, escalation rates, and customer feedback.',
      flow: ['Customer request', 'Grounded response', 'Review & resolve'], subject: 'Exploring AI for customer experience'
    },
    resilience: {
      category: 'Operational continuity', scenario: 'See a developing issue while there is time to act.',
      description: 'Bring maintenance notes, service history, and operating signals together so a team can investigate potential problems earlier.',
      value: 'Better visibility into emerging issues and more informed response planning.',
      decision: 'Who validates a signal and has authority to intervene when operations may be affected?',
      measure: 'Useful warning time, false alerts, response time, and avoided disruption supported by evidence.',
      flow: ['Operating signals', 'Surface the pattern', 'Validate & act'], subject: 'Exploring AI for resilience'
    }
  };
  const priorityButtons = [...document.querySelectorAll('[data-priority]')];
  function selectPriority(button) {
    const key = button.dataset.priority, item = priorities[key];
    priorityButtons.forEach(other => { other.setAttribute('aria-selected', String(other === button)); other.tabIndex = other === button ? 0 : -1; });
    document.getElementById('opportunity-panel').setAttribute('aria-labelledby', button.id);
    ['category', 'scenario', 'description', 'value', 'decision', 'measure'].forEach(field => { document.getElementById('opportunity-' + field).textContent = item[field]; });
    ['one', 'two', 'three'].forEach((name, index) => { document.getElementById('flow-' + name).textContent = item.flow[index]; });
    document.querySelector('.opportunity-visual').dataset.tone = key;
    document.getElementById('opportunity-cta').href = 'mailto:info@alphaworx.io?subject=' + encodeURIComponent(item.subject);
  }
  priorityButtons.forEach((button, index) => {
    button.addEventListener('click', () => selectPriority(button));
    button.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % priorityButtons.length;
      if (event.key === 'ArrowLeft') next = (index - 1 + priorityButtons.length) % priorityButtons.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = priorityButtons.length - 1;
      if (next !== undefined) { event.preventDefault(); priorityButtons[next].focus(); selectPriority(priorityButtons[next]); }
    });
  });

  const workflow = {
    current: [
      ['Human led', 'Read, classify, and route the request.', 'A team member reads the incoming request, interprets the need, and decides where it belongs. Ambiguous requests may move between queues.'],
      ['Human led', 'Find the right information across systems.', 'A person searches knowledge articles, service records, and previous correspondence. The quality of the result depends on accessible sources and time to investigate.'],
      ['Human led', 'Assemble a response from what was found.', 'The service team drafts an answer and checks it against the request. Repeated tasks compete with unfamiliar or complex cases.'],
      ['Human judgment', 'Check the answer and any commitments.', 'The accountable person verifies accuracy, policy, and any promises to the customer. Uncertainty or exceptions require escalation.'],
      ['Human led', 'Send, record, and carry the learning forward.', 'The team sends the response and updates the case. Patterns in repeated issues may stay scattered across individual records.']
    ],
    assisted: [
      ['Human + AI', 'Start with a well-understood request.', 'AI can suggest a category and summarize the request. A person sets the service policy and owns exceptions and routing rules.'],
      ['AI assists', 'Bring the evidence into the workflow.', 'AI retrieves relevant material from approved sources and presents references. Access rules still apply; missing or conflicting evidence is surfaced for a person.'],
      ['AI assists', 'Prepare an answer that can be checked.', 'AI drafts a response grounded in the retrieved material and flags uncertainty. The draft is assistance, not authorization to make a new commitment.'],
      ['Human judgment', 'Keep the consequential decision with its owner.', 'A person checks the evidence, resolves ambiguity, and approves commitments or escalates exceptions. The review gate remains explicit.'],
      ['Human + AI', 'Close the case and improve the process.', 'After approval, the response is sent and recorded. AI can help summarize recurring issues; the service owner decides which process or knowledge changes to make.']
    ]
  };
  const names = ['Receive', 'Find evidence', 'Prepare', 'Review', 'Resolve & learn'];
  const stepButtons = [...document.querySelectorAll('[data-step]')];
  const modeButtons = [...document.querySelectorAll('[data-workflow-mode]')];
  const play = document.getElementById('workflow-play');
  const status = document.getElementById('workflow-status');
  const detail = document.querySelector('.workflow-detail-copy');
  let mode = 'assisted', step = 0, interval = null;
  function renderWorkflow() {
    const current = workflow[mode][step];
    stepButtons.forEach((button, index) => {
      button.classList.toggle('is-current', index === step); button.setAttribute('aria-pressed', String(index === step));
      button.querySelector('.node-role').textContent = workflow[mode][index][0];
    });
    modeButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.workflowMode === mode)));
    document.getElementById('workflow-step-label').textContent = String(step + 1).padStart(2, '0') + ' / ' + names[step] + ' · ' + (mode === 'assisted' ? 'With AI' : 'Current workflow');
    document.getElementById('workflow-step-title').textContent = current[1];
    document.getElementById('workflow-step-description').textContent = current[2];
  }
  function stopWalkthrough(message = 'Choose any stage to explore.') {
    clearInterval(interval); interval = null; play.textContent = 'Play walkthrough ▷'; play.setAttribute('aria-pressed', 'false'); detail.setAttribute('aria-live', 'polite'); status.textContent = message;
  }
  stepButtons.forEach(button => button.addEventListener('click', () => { stopWalkthrough(); step = Number(button.dataset.step); renderWorkflow(); }));
  modeButtons.forEach(button => button.addEventListener('click', () => { stopWalkthrough(); mode = button.dataset.workflowMode; renderWorkflow(); }));
  play.addEventListener('click', () => {
    if (interval) { stopWalkthrough('Walkthrough paused. Explore at your own pace.'); return; }
    if (motionPaused) { status.textContent = 'Motion is paused. Choose a stage to explore, or enable motion in the header.'; return; }
    if (step === 4) step = 0;
    detail.setAttribute('aria-live', 'off'); renderWorkflow();
    play.textContent = 'Pause walkthrough Ⅱ'; play.setAttribute('aria-pressed', 'true'); status.textContent = 'Following the request through all five stages.';
    interval = setInterval(() => {
      if (step >= 4) { stopWalkthrough('Walkthrough complete. Compare the other workflow or replay.'); return; }
      step += 1; renderWorkflow();
    }, 4800);
  });
  document.addEventListener('alphaworx:motion', event => { if (event.detail.paused) stopWalkthrough('Motion paused. Each stage is still available to explore.'); });
  document.addEventListener('visibilitychange', () => { if (document.hidden) stopWalkthrough(); });
  new IntersectionObserver(entries => { if (!entries[0].isIntersecting && interval) stopWalkthrough('Walkthrough paused. Continue whenever you’re ready.'); }, { threshold: .05 }).observe(document.querySelector('.workflow-surface'));
  renderWorkflow();

  // Preserve the original site's reveal and timeline behavior, with readable no-JS content.
  const reveal = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting) { entry.target.classList.add('in'); reveal.unobserve(entry.target); }
  }), { threshold: .12 });
  document.querySelectorAll('.reveal').forEach(element => reveal.observe(element));
  const progress = document.getElementById('progress');
  function updateProgress() { const el = document.documentElement; progress.style.width = (el.scrollTop / (el.scrollHeight - el.clientHeight || 1) * 100) + '%'; }
  document.addEventListener('scroll', updateProgress, { passive: true }); updateProgress();

  // A soft, low-resolution canvas wash, shared with the original visual direction.
  function mesh(id) {
    const canvas = document.getElementById(id), ctx = canvas?.getContext('2d'); if (!ctx) return;
    let width = 2, height = 2, visible = false, last = 0, time = 0;
    function size() { const rect = canvas.getBoundingClientRect(); width = canvas.width = Math.max(2, Math.round(rect.width * .35)); height = canvas.height = Math.max(2, Math.round(rect.height * .35)); draw(); }
    const colors = ['rgba(100,125,140,.30)', 'rgba(37,70,91,.18)', 'rgba(154,123,73,.12)', 'rgba(149,159,165,.20)'];
    function draw() {
      ctx.clearRect(0, 0, width, height); ctx.fillStyle = '#f5f3ee'; ctx.fillRect(0, 0, width, height);
      colors.forEach((color, i) => {
        const x = width * (.5 + .42 * Math.cos(time * .06 + i * 1.8)), y = height * (.5 + .35 * Math.sin(time * .07 + i));
        const radius = Math.max(width, height) * .5, gradient = ctx.createRadialGradient(x, y, 0, x, y, radius);
        gradient.addColorStop(0, color); gradient.addColorStop(1, 'rgba(255,255,255,0)'); ctx.fillStyle = gradient; ctx.fillRect(0, 0, width, height);
      });
    }
    size(); new ResizeObserver(size).observe(canvas);
    new IntersectionObserver(entries => { visible = entries[0].isIntersecting; }).observe(canvas);
    function frame(now) { if (!motionPaused && visible && !document.hidden && now - last >= 40) { time += Math.min((now - last) / 1000, .08); last = now; draw(); } else if (!visible || motionPaused || document.hidden) last = now; requestAnimationFrame(frame); }
    requestAnimationFrame(frame);
  }
  mesh('mesh'); mesh('mesh2');
  // Keep older inbound links to the value-gap section useful.
  if (location.hash === '#value') document.getElementById('opportunity').scrollIntoView();
})();
