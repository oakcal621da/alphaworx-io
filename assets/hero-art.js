// Original animated ribbon artwork; renders locally without a graphics dependency.
(() => {
'use strict';
const canvas = document.getElementById('hero-sculpture');
const ctx = canvas?.getContext('2d');
if (!ctx) return;
let time = 0, last = 0, width = 1, height = 1, ratio = 1, visible = false;
let paused = document.body.classList.contains('motion-paused');
function rotate(p,a,b){const cy=Math.cos(a),sy=Math.sin(a),cx=Math.cos(b),sx=Math.sin(b);const x=p[0]*cy+p[2]*sy,z=-p[0]*sy+p[2]*cy;return [x,p[1]*cx-z*sx,p[1]*sx+z*cx];}
function point(t,v){const twist=t*1.5;const r=1+v*Math.cos(twist);return [r*Math.cos(t),r*Math.sin(t),v*Math.sin(twist)];}
function project(p,w,h){const f=3.9/(3.9+p[2]);const scale=Math.min(w*.32,h*.32);return [w*.5+p[0]*scale*f,h*.49+p[1]*scale*f];}
function drawRibbon(w,h){
 const a=.32+Math.sin(time*.15)*.3,b=.75+Math.cos(time*.12)*.17;
 const faces=[];const n=116,m=13;
 for(let i=0;i<n;i++){const t=i/n*Math.PI*2;for(let j=0;j<m;j++){
  const v=-.42+j/m*.84;const raw=[point(t,v),point(t+Math.PI*2/n,v),point(t+Math.PI*2/n,v+.84/m),point(t,v+.84/m)];
  const q=raw.map(p=>rotate(p,a,b));const z=q.reduce((s,p)=>s+p[2],0)/4;
  const u=q[1].map((x,k)=>x-q[0][k]),v2=q[3].map((x,k)=>x-q[0][k]);
  const normal=[u[1]*v2[2]-u[2]*v2[1],u[2]*v2[0]-u[0]*v2[2],u[0]*v2[1]-u[1]*v2[0]];
  const norm=Math.hypot(...normal)||1;const light=Math.abs((normal[0]*-.3+normal[1]*-.6+normal[2]*.74)/norm);
  const hue=210;
  faces.push({q:q.map(p=>project(p,w,h)),z,hue,light,j});
 }}
 faces.sort((a,b)=>b.z-a.z);
 for(const f of faces){const lit=24+f.light*48;ctx.beginPath();f.q.forEach((p,k)=>k?ctx.lineTo(...p):ctx.moveTo(...p));ctx.closePath();ctx.fillStyle=`hsl(${f.hue} 24% ${lit}%)`;ctx.fill();ctx.strokeStyle=`hsl(${f.hue} 24% ${lit}%)`;ctx.lineWidth=.65;ctx.stroke();}
}

function draw() {
  ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
  ctx.clearRect(0, 0, width, height);
  ctx.save(); ctx.translate(width * .5, height * .87); ctx.scale(1, .17);
  const shadow = ctx.createRadialGradient(0, 0, 0, 0, 0, width * .3);
  shadow.addColorStop(0, '#172a3a27'); shadow.addColorStop(1, '#172a3a00');
  ctx.fillStyle = shadow; ctx.fillRect(-width/2, -width/2, width, width); ctx.restore();
  drawRibbon(width, height);
}
function resize() {
  const rect = canvas.getBoundingClientRect(); width = rect.width; height = rect.height;
  ratio = Math.min(devicePixelRatio || 1, 2);
  canvas.width = Math.max(1, Math.round(width * ratio)); canvas.height = Math.max(1, Math.round(height * ratio));
  draw();
}
resize();
new ResizeObserver(resize).observe(canvas);
new IntersectionObserver(entries => { visible = entries[0].isIntersecting; }).observe(canvas);
document.addEventListener('alphaworx:motion', event => { paused = event.detail.paused; });
function frame(now) {
  if (!paused && visible && !document.hidden && now - last >= 32) {
    time += Math.min((now - last) / 1000, .08) * .55; last = now; draw();
  } else if (paused || !visible || document.hidden) last = now;
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
})();
