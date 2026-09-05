(() => {
'use strict';
const root=document.getElementById('assessment-app'); if(!root)return;
const units=['Customer service','Commercial','Finance','Operations','Technology'];
const dimensions=['Cost','Data','Vendors','Security','Reliability','Ownership'];
const owners=['Head of Customer Service','Commercial Director','Finance Director','Operations Director','Technology Director'];
const patterns=[
 ['Run cost is hard to attribute.','Usage is billed centrally, so the team cannot connect cost to completed work.','Allocate usage and review cost per completed task.'],
 ['Approved data boundaries need review.','The workflow can include sensitive material; handling and access rules need evidence.','Confirm permitted data and approved tools with the security lead.'],
 ['A supplier dependency needs an exit plan.','The workflow relies on one provider without a documented fallback.','Test a fallback and assign ownership of provider changes.'],
 ['Agent permissions need a named owner.','The example agent uses shared credentials with broader access than its task requires.','Assign an owner, narrow access, and document revocation and review.'],
 ['Exception handling needs testing.','Missing or conflicting evidence can reach the draft without a clear escalation path.','Test failure cases and define the human review gate.'],
 ['The production decision has no clear owner.','Approval is spread across teams, leaving funding and stop decisions ambiguous.','Name the business sponsor and agree decision rights.']
 ];
const scenarios={
 baseline:{label:'Scattered pilots',levels:[[2,2,1,1,1,2],[1,1,1,0,1,1],[0,1,1,0,0,0],[1,1,0,1,2,1],[1,0,2,2,1,1]]},
 agents:{label:'Expanding agent use',levels:[[1,1,1,2,2,2],[1,1,0,2,1,1],[0,1,1,1,1,0],[1,1,0,2,2,1],[2,1,2,2,2,1]]},
 controls:{label:'Core controls established',levels:[[1,1,0,0,1,0],[0,0,1,0,0,0],[0,0,1,0,0,0],[1,0,0,0,1,0],[1,0,1,1,1,0]]}
};
const levels=['Routine','Review','Priority'];
// Dimension-specific discussion prompts, not measured control effectiveness.
const evidencePatterns=[
 ['Tag usage to the workflow and include review and rework within an agreed cost boundary.','Attribution makes spend visible; it does not control demand or prove a cash benefit.','A reconciled sample of usage, reviewer time, accepted outcomes, and the pre-AI baseline.','Finance + business owner','why-ai-pilots-stall'],
 ['Review source permissions and enforce role-appropriate retrieval and approved data handling.','Correct permission enforcement still exposes content allowed by overly broad source permissions.','Allow/deny retrieval tests for representative roles, connected-source inventory, and retention settings.','Data owner + Security','shadow-ai-biggest-exposure'],
 ['Maintain a dependency register, assign change monitoring, and rehearse an alternative route.','An alternative can have different quality, capacity, and contract terms; portability requires testing.','Provider dependencies, notice owner, evaluated fallback, and migration rehearsal.','Technology + Procurement','model-deprecation-reliability-risk'],
 ['Give the agent a scoped identity and minimum tools; check authorization outside the model.','Narrow permissions constrain reachable actions but do not guarantee correct output or remove all attacks.','Permitted operations, downstream authorization tests, approval conditions, and credential revocation test.','Security + workflow owner','excessive-agency-ai-risk-no-attacker'],
 ['Evaluate difficult cases, route exceptions to a person, and exercise a fallback.','A finite test set cannot establish correctness for every future input or provider change.','Representative evaluation cases, reviewed exceptions, escalation thresholds, and fallback exercise.','Operating owner + domain reviewers','model-deprecation-reliability-risk'],
 ['Record who can fund, approve, change, and pause the workflow, with a clear escalation route.','Naming a role is insufficient if it lacks time, evidence, or delegated authority.','Decision record, accepted responsibilities, stop authority, and next review date.','Executive sponsor + AI lead','who-owns-the-ai-decision']
];
const cases=[
 ['Support drafting',78,82,32,'Candidate for a focused pilot','A bounded support workflow with accessible knowledge and a clear review gate.','Head of Customer Service','Validate response quality and repeat contacts before expanding.'],
 ['Contract review',64,68,42,'Validate the review process','Potential value depends on source quality and specialist review capacity.','Legal Operations Lead','Agree an evaluation set and retain legal approval of advice.'],
 ['Demand planning',85,32,50,'Build the foundations','High potential value with data and integration dependencies still unresolved.','Operations Director','Establish a baseline and test forecast quality against current planning.'],
 ['Meeting summaries',32,86,24,'Keep the investment proportionate','Easy to trial, with a smaller direct business outcome to measure.','Business Operations Lead','Confirm adoption, record handling, and the actual time returned.'],
 ['Pricing assistant',76,22,46,'Investigate constraints first','Material commercial consequences make authority and validation central.','Commercial Director','Define permissible recommendations and an accountable approval process.'],
 ['Duplicate chatbot',25,30,28,'Reassess the need','The example overlaps an existing service and has unclear incremental value.','Technology Director','Compare against existing capabilities before further funding.']
];
const economics=[
 ['Customer service',16000,'Head of Customer Service','Cost per resolved request','Track repeat contacts and review effort alongside usage.'],
 ['Technology',12000,'Technology Director','Cost per accepted change','Include evaluation, integration, and rework in the discussion.'],
 ['Operations',9000,'Operations Director','Cost per completed case','Separate routine cases from exceptions requiring specialist review.'],
 ['Commercial',7000,'Commercial Director','Cost per qualified proposal','Measure proposal quality and conversion, with appropriate attribution.'],
 ['Shared / unallocated',4000,'Finance + Technology','Share of cost assigned to owners','Allocate shared costs using a documented method.']
];
const phases=[
 ['Establish the baseline',0,33,'1–30','Agree the problem and the mandate.','Inventory use cases, review evidence, and establish the current cost and outcome baseline.','Executive sponsor','Agreed scope, named owners, and a prioritized assessment.'],
 ['Design the controls',22,39,'21–55','Set the conditions for a useful pilot.','Define access, evaluation, review gates, cost attribution, and provider responsibilities.','Technology + Security','Documented controls and criteria for starting or stopping.'],
 ['Test a bounded workflow',44,39,'41–75','Gather evidence in the actual workflow.','Run a scoped evaluation, review exceptions, and compare results with the baseline.','Business workflow owner','A decision-ready record of quality, cost, and operational fit.'],
 ['Decide and plan forward',77,23,'71–90','Make the next investment explicit.','Review findings and decide whether to expand, revise, or stop; establish the review cadence.','Executive sponsor + Finance','An investment decision and accountable next steps.']
];
root.innerHTML=`<div class="assessment-label"><span>MERIDIAN INDUSTRIAL GROUP · SAMPLE ASSESSMENT</span><strong>Fictional company · illustrative findings and figures</strong></div>
<div class="assessment-tabs" role="tablist" aria-label="Assessment views">${['Exposure heat map','Opportunity portfolio','AI economics','90-day action plan'].map((x,i)=>`<button type="button" role="tab" id="assessment-tab-${i}" aria-controls="assessment-panel" aria-selected="${i===0}" tabindex="${i===0?0:-1}" data-view="${i}"><span>0${i+1}</span>${x}</button>`).join('')}</div>
<div class="assessment-panel" id="assessment-panel" role="tabpanel" aria-labelledby="assessment-tab-0" tabindex="0"><div class="assessment-panel-top"><div><h3 id="assessment-view-title"></h3><p id="assessment-view-description"></p></div><label id="scenario-label">Sample scenario<select id="assessment-scenario" aria-label="Sample scenario">${Object.entries(scenarios).map(([k,v])=>`<option value="${k}">${v.label}</option>`).join('')}</select></label></div><div class="assessment-workspace"><div class="assessment-chart" id="assessment-chart"></div><aside class="assessment-detail" aria-live="polite" aria-atomic="true"><span class="small-label" id="assessment-detail-kicker"></span><h4 id="assessment-detail-title"></h4><p id="assessment-detail-body"></p><dl><dt>Accountable role</dt><dd id="assessment-detail-owner"></dd><dt id="assessment-next-label">Next action</dt><dd id="assessment-detail-next"></dd></dl></aside></div><p class="assessment-footnote" id="assessment-footnote"></p></div>
<div class="assessment-footer"><p>See the priorities. Understand the decisions. Agree the next move.</p><a class="link" href="mailto:info@alphaworx.io?subject=Discuss%20an%20AI%20strategy%20assessment">Discuss an assessment ↗</a></div>`;
const get=id=>document.getElementById(id),chart=get('assessment-chart'),tabs=[...root.querySelectorAll('[data-view]')];
let view=0,scenario='baseline',selectedCell=[0,1];
function detail(kicker,title,body,owner,next,nextLabel='Next action'){
 const evidence=get('assessment-evidence');if(evidence)evidence.hidden=true;
 Object.entries({'kicker':kicker,'title':title,'body':body,'owner':owner,'next':next}).forEach(([key,value])=>get('assessment-detail-'+key).textContent=value);
 get('assessment-next-label').textContent=nextLabel;
}
function selectHeat(r,c){
 selectedCell=[r,c];const severity=scenarios[scenario].levels[r][c];
 chart.querySelectorAll('.heat-cell').forEach(b=>b.setAttribute('aria-pressed',String(+b.dataset.row===r&&+b.dataset.col===c)));
 const [title,body,action]=patterns[c];
 detail(`${units[r]} · ${dimensions[c]} · ${levels[severity]}`,severity===0?'Maintain the established controls.':title,severity===0?'In this sample, an owner and a documented control are in place. Routine review still checks that they work as the workflow changes.':body,owners[r]+(c===1||c===3?' + Security':''),severity===0?'Review evidence at the agreed cadence and after material changes.':action);
 let panel=get('assessment-evidence');
 if(!panel){panel=document.createElement('section');panel.id='assessment-evidence';panel.className='assessment-evidence';panel.setAttribute('aria-label','Control response and evidence');get('assessment-footnote').before(panel);}
 const [response,limit,evidence,reviewers,slug]=evidencePatterns[c];
 panel.hidden=false;
 panel.innerHTML=`<div class="assessment-evidence-heading"><p class="small-label">${units[r]} / ${dimensions[c]} · ILLUSTRATIVE CONTROL REVIEW</p><a class="link" href="/blog/${slug}.html">Explore the guidance ↗</a></div><div class="assessment-evidence-grid"><div><h4>${severity===0?'Response to maintain':'Proposed response'}</h4><p>${response}</p></div><div><h4>Remaining limitation</h4><p>${limit}</p></div><div><h4>Evidence to request</h4><p>${evidence}</p><p class="evidence-reviewers">Review with: ${reviewers}</p></div></div>`;
}
function heat(){
 chart.innerHTML=`<div class="heat-scroll" role="region" aria-label="Exposure heat map, scroll horizontally on small screens" tabindex="0"><table class="heat-table"><caption>Choose a cell to inspect the sample finding.</caption><thead><tr><th scope="col">Business unit</th>${dimensions.map(x=>`<th scope="col">${x}</th>`).join('')}</tr></thead><tbody>${units.map((u,r)=>`<tr><th scope="row">${u}</th>${dimensions.map((d,c)=>{const l=levels[scenarios[scenario].levels[r][c]];return `<td><button class="heat-cell" type="button" data-row="${r}" data-col="${c}" data-level="${l}" aria-pressed="false" aria-label="${u}, ${d}: ${l}">${l}</button></td>`}).join('')}</tr>`).join('')}</tbody></table></div><div class="heat-legend"><span><i style="background:#e3ebf1"></i>Routine · maintain</span><span><i style="background:#526f83"></i>Review · investigate</span><span><i style="background:#25465b"></i>Priority · address first</span></div>`;
 chart.querySelectorAll('.heat-cell').forEach(b=>b.addEventListener('click',()=>selectHeat(+b.dataset.row,+b.dataset.col)));
 selectHeat(...selectedCell);
}
function selectCase(index){
 chart.querySelectorAll('[data-case]').forEach(b=>b.setAttribute('aria-pressed',String(+b.dataset.case===index)));
 const c=cases[index];detail(c[0]+' · illustrative opportunity',c[4],c[5],c[6],c[7]);
}
function portfolio(){
 chart.innerHTML=`<div class="portfolio-plot" role="group" aria-label="Opportunity map. Value increases upward and feasibility increases to the right. Bubble size indicates illustrative relative investment."><span class="plot-quadrant q1">BUILD FOUNDATIONS</span><span class="plot-quadrant q2">PRIORITIZE VALIDATION</span><span class="plot-quadrant q3">REASSESS</span><span class="plot-quadrant q4">LIMIT THE INVESTMENT</span><span class="plot-axis x">FEASIBILITY →</span><span class="plot-axis y">POTENTIAL VALUE →</span>${cases.map((c,i)=>`<button type="button" class="portfolio-point" style="left:${c[2]}%;bottom:${c[1]}%;--bubble:${c[3]}px" data-case="${i}" aria-pressed="false" aria-label="${c[0]}: illustrative value ${c[1]}, feasibility ${c[2]}, on relative scales of 0 to 100">${i+1}</button>`).join('')}</div><div class="portfolio-key">${cases.map((c,i)=>`<button type="button" data-case="${i}" aria-pressed="false"><b>0${i+1}</b>${c[0]}</button>`).join('')}</div>`;
 chart.querySelectorAll('[data-case]').forEach(b=>b.addEventListener('click',()=>selectCase(+b.dataset.case)));selectCase(0);
}
function selectCost(index){
 chart.querySelectorAll('[data-cost]').forEach(b=>b.setAttribute('aria-pressed',String(+b.dataset.cost===index)));
 const c=economics[index];detail(c[0]+' · illustrative monthly cost',c[3],'Connect this spend to a completed business task and its quality. A lower model bill alone does not establish better value.',c[2],c[4]);
}
function costs(){
 const total=economics.reduce((sum,c)=>sum+c[1],0);
 chart.innerHTML=`<div class="economics-total"><strong>$${total.toLocaleString('en-US')}</strong><span>Illustrative monthly operating spend</span></div>${economics.map((c,i)=>`<button type="button" class="cost-item" data-cost="${i}" aria-pressed="false" aria-label="${c[0]}, ${c[1].toLocaleString('en-US')} dollars monthly, ${Math.round(c[1]/total*100)} percent of total"><span>${c[0]}</span><span class="cost-track"><i style="width:${c[1]/total*100}%"></i></span><b>$${(c[1]/1000).toFixed(0)}k</b></button>`).join('')}`;
 chart.querySelectorAll('[data-cost]').forEach(b=>b.addEventListener('click',()=>selectCost(+b.dataset.cost)));selectCost(0);
}
function selectPhase(index){
 chart.querySelectorAll('[data-phase]').forEach(b=>b.setAttribute('aria-pressed',String(+b.dataset.phase===index)));
 const p=phases[index];detail('Illustrative days '+p[3],p[4],p[5],p[6],p[7],'Decision / output');
}
function plan(){
 chart.innerHTML=`<div class="plan-axis"><span>Day 1</span><span>30</span><span>60</span><span>90</span></div>${phases.map((p,i)=>`<button type="button" class="plan-row" data-phase="${i}" aria-pressed="false" aria-label="${p[0]}, illustrative days ${p[3]}"><span>${p[0]}</span><span class="plan-track"><span class="plan-bar" style="--start:${p[1]}%;--duration:${p[2]}%">${p[3]}</span></span></button>`).join('')}`;
 chart.querySelectorAll('[data-phase]').forEach(b=>b.addEventListener('click',()=>selectPhase(+b.dataset.phase)));selectPhase(0);
}
const copy=[
 ['Where does attention belong?','Explore business units and operating dimensions. Each cell connects a priority to an owner and a practical next step.','These are illustrative priority categories, not incident probabilities or validated scores. Sample scenarios are predefined examples; no company systems are scanned.'],
 ['Put the next investment in context.','Compare potential value with feasibility. Select an initiative to explore the decision behind its position.','Positions and relative investment sizes are illustrative. The map informs discussion; funding decisions also consider dependencies, risk, evidence, and strategic fit.'],
 ['Make cost part of the operating conversation.','Explore spending by business unit, then connect each line to an accountable role and a business outcome.','All dollar amounts are fictional. Bars show shares of the $48,000 monthly total. A real assessment defines the cost boundary, including model usage, platform costs, and human effort.'],
 ['Turn findings into accountable action.','Explore a possible sequence from baseline to an evidence-based investment decision.','Illustrative sequencing, subject to scope, access, resources, and findings. Production readiness and delivery dates are established with the client.']
];
function renderView(index){
 view=index;tabs.forEach((b,i)=>{b.setAttribute('aria-selected',String(i===view));b.tabIndex=i===view?0:-1;});
 get('assessment-panel').setAttribute('aria-labelledby','assessment-tab-'+view);
 get('assessment-view-title').textContent=copy[view][0];get('assessment-view-description').textContent=copy[view][1];get('assessment-footnote').textContent=copy[view][2];get('scenario-label').hidden=view!==0;
 [heat,portfolio,costs,plan][view]();
}
tabs.forEach((b,i)=>{b.addEventListener('click',()=>renderView(i));b.addEventListener('keydown',e=>{let next;if(e.key==='ArrowRight')next=(i+1)%4;if(e.key==='ArrowLeft')next=(i+3)%4;if(e.key==='Home')next=0;if(e.key==='End')next=3;if(next!==undefined){e.preventDefault();renderView(next);tabs[next].focus();}});});
get('assessment-scenario').addEventListener('change',e=>{scenario=e.target.value;heat();});renderView(0);
})();
