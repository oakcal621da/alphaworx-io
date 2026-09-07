from pathlib import Path
from bs4 import BeautifulSoup
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
ROOT=Path(__file__).resolve().parents[1]
from tempfile import gettempdir
FONT_CACHE=Path(gettempdir())/'alphaworx-deck-fonts'
FONT_CACHE.mkdir(exist_ok=True)
if not (FONT_CACHE/'plex-600.ttf').exists():
 from urllib.request import urlretrieve
 from fontTools.ttLib import TTFont as FontFile
 from fontTools.varLib.instancer import instantiateVariableFont
 urlretrieve('https://raw.githubusercontent.com/google/fonts/main/ofl/ibmplexsans/IBMPlexSans%5Bwdth,wght%5D.ttf',FONT_CACHE/'plex-variable.ttf')
 font=FontFile(FONT_CACHE/'plex-variable.ttf')
 for weight in [400,500,600]:
  instantiateVariableFont(font,{'wght':weight,'wdth':100},inplace=False).save(FONT_CACHE/f'plex-{weight}.ttf')
for weight in [400,500,600]: pdfmetrics.registerFont(TTFont(f'Plex{weight}',str(FONT_CACHE/f'plex-{weight}.ttf')))
W,H=1200,675
INK='#172a3a'; MUTED='#526775'; NAVY='#25465b'; SLATE='#647d8c'; LINE='#ccd5db'; PAPER='#f5f3ee'; BLUE='#e0e8ee'
soup=BeautifulSoup((ROOT/'deck.html').read_text(),'html.parser')
slide_total=len(soup.select('.slide'))
out=ROOT/'output/pdf/alphaworx-enterprise-ai-assessment.pdf'
out.parent.mkdir(parents=True,exist_ok=True)
c=canvas.Canvas(str(out),pagesize=(W,H));c.setTitle('Meridian AI Assessment Walkthrough - Alphaworx');c.setAuthor('Alphaworx')
issues=[]
def text(el): return el.get_text(' ',strip=True) if el else ''
def rect(x,y,w,h,color,stroke=None):
 c.setFillColor(HexColor(color));c.setStrokeColor(HexColor(stroke or color));c.rect(x,H-y-h,w,h,fill=1,stroke=bool(stroke))
def para(txt,x,y,w,size=17,color=MUTED,weight=400,leading=None):
 style=ParagraphStyle('body',fontName=f'Plex{weight}',fontSize=size,leading=leading or size*1.35,textColor=HexColor(color))
 p=Paragraph(escape(txt),style);pw,ph=p.wrap(w,H)
 p.drawOn(c,x,H-y-ph)
 if y+ph>611: issues.append((page,txt[:45],y+ph))
 return y+ph

def block(el,x,y,w,title_size=24):
 lab=el.select_one('.case-code') or el.find('span',recursive=False)
 if lab: y=para(text(lab),x,y,w,11,SLATE,500)+12
 title=el.find(['h3','blockquote'])
 if title: y=para(text(title),x,y,w,title_size,INK,500)+13
 for p in el.find_all('p',recursive=False):
  if p!=lab: y=para(text(p),x,y,w,16)+10
 return y

def dl(el,x,y,w):
 for dt,dd in zip(el.find_all('dt'),el.find_all('dd')):
  y=para(text(dt).upper(),x,y,w,10,NAVY,500)+5
  y=para(text(dd),x,y,w,15)+13
 return y

def strip(el,y=495):
 rect(55,y,1090,78,BLUE);rect(55,y,3,78,NAVY)
 yy=para(text(el.find('strong')),76,y+13,1048,19,INK,500)+7
 para(text(el.find('span')),76,yy,1048,14)

for page,s in enumerate(soup.select('.slide'),1):
 id=s['id'];rect(0,0,W,H,PAPER if id in ('assessment','conversation') else '#fdfdfb')
 c.setFillColor(HexColor(NAVY));c.setFont('Plex600',12);c.drawString(55,H-34,'ALPHAWORX.IO')
 c.setFillColor(HexColor(SLATE));c.setFont('Plex400',10);c.drawRightString(1145,H-34,'FICTIONAL ENTERPRISE ASSESSMENT')
 para(text(s.select_one('.eyebrow')).upper(),55,65,1090,11,SLATE,500)
 title=text(s.find(['h1','h2']))
 titlebottom=para(title,55,91,1090 if page!=1 else 620,39 if page!=1 else 59,INK,500,44 if page!=1 else 61)
 y=max(182,titlebottom+28)
 content=s.select_one('.slide-content')
 if id=='assessment':
  para(text(content.select_one('.lede')),55,275,560,25,MUTED)
  # A code-native process graphic, summarizing the story.
  for i,(lab,sub) in enumerate([('AI USAGE','What does AI do in the process?'),('BUSINESS IMPACT','Does the completed work improve?'),('ACCOUNTABILITY','What should continue, change, or stop?')]):
   yy=180+i*120;rect(720,yy,425,91,BLUE if i!=1 else NAVY)
   para(lab,742,yy+15,380,13,'#ffffff' if i==1 else NAVY,600)
   para(sub,742,yy+42,380,18,'#dfe8ef' if i==1 else INK,500)
   if i<2: rect(927,yy+91,2,29,SLATE)
  para(f'{slide_total} slides / Meridian: $6.5bn annual revenue',55,485,580,14,SLATE,500)
 elif id in ('charter','finding','engagement'):
  left,right=content.select_one('.case-split').find_all('div',recursive=False)
  if id=='engagement':
   para(text(left.select_one('.lede')),55,y,485,24)
   st=left.select_one('.case-strip');yy=para(text(st.find('strong')),55,y+145,480,22,INK,500)+13
   para(text(st.find('span')),55,yy,480,17)
  else:
   end=block(left,55,y,495,31)
   if id=='finding':
    para(text(left.select_one('.trace-line')),55,end+16,490,15,NAVY,500)
  rect(605,y,540,385,'#edf1f3');dl(right,629,y+22,492)
 elif id in ('people','proof'):
  for i,a in enumerate(content.select('.case-cards article')):
   xx=55+(i%2)*562;yy=y+(i//2)*162
   rect(xx,yy,527,2,SLATE);block(a,xx,yy+16,512,24)
  st=content.select_one('.case-strip')
  if st: strip(st,527)
  else: para(text(content.select_one('.case-note')),55,540,1090,13)
 elif id in ('evidence','handoff','spend','tradeoffs'):
  t=content.select_one('table'); data=[]
  for r,row in enumerate(t.select('tr')):
   vals=[]
   for cell in row.find_all(['th','td']):
    style=ParagraphStyle('t',fontName='Plex500' if r==0 else 'Plex400',fontSize=12 if r==0 else 15,leading=19,textColor=HexColor(NAVY if r==0 else MUTED))
    vals.append(Paragraph(escape(text(cell)),style))
   data.append(vals)
  widths=[505,130,455] if len(data[0])==3 else ([260,155,260,415] if id=='tradeoffs' else [170,350,220,350])
  tt=Table(data,colWidths=widths);tt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor(BLUE)),('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),14),('TOPPADDING',(0,0),(-1,-1),14),('LEFTPADDING',(0,0),(-1,-1),13),('RIGHTPADDING',(0,0),(-1,-1),13),('LINEBELOW',(0,0),(-1,-1),.5,HexColor(LINE))]));ww,hh=tt.wrap(1090,500);tt.drawOn(c,55,H-y-hh)
  para(text(content.select_one('.case-note')),55,y+hh+19,1090,13)
 elif id=='contradiction':
  for i,node in enumerate(content.select('.claim-node')):
   xx=55+i*595;rect(xx,y,495,260,'#edf1f3' if i==0 else BLUE);block(node,xx+25,y+25,445,29)
  para('≠',573,y+82,60,54,SLATE)
  strip(content.select_one('.case-strip'),y+288)
 elif id=='reconcile':
  for i,(label,score,name,confidence,reason) in enumerate([
    ('01 / INITIAL VIEW','2','Emerging','Provisional','Approved process requires a human decision. Actual AI tool permissions have not yet been tested.'),
    ('02 / RECONCILED VIEW','1','Ad hoc','Strong','E03 reproduces credit posting without required approval. The AI tool boundary does not enforce the process.')]):
   xx=55+i*563;rect(xx,y,527,281,'#edf1f3');para(label,xx+25,y+21,477,11,SLATE,500)
   para(score+'/5',xx+25,y+55,150,64,INK,500);para(name,xx+190,y+69,300,28,INK,500);para('Evidence confidence: '+confidence,xx+190,y+111,300,13,NAVY)
   para(reason,xx+25,y+169,477,18)
  para('Risk & Governance / assessed credit workflow only',55,y+300,1090,15,NAVY,500)
  para('Recorded change: 2 → 1 after permission testing. Strong evidence can support a low maturity finding. Missing evidence is not a score of zero.',55,y+330,1090,18)
 elif id=='tradeoffs':
  for i,a in enumerate(content.select('.choice-stack article')):
   yy=y+i*124;rect(55,yy,1090,108,BLUE if i==1 else '#edf1f3')
   para(text(a.select_one('.status-tag')),75,yy+23,175,12,NAVY,600)
   para(text(a.find('h3')),263,yy+16,855,24,INK,500);para(text(a.find('p')),263,yy+52,855,16)
 elif id=='economics':
  for i,(label,value) in enumerate([('Finance-accepted cash cost reductions','$54m'),('Modeled staff capacity - not cash','$36m'),('Forecasts - not yet evidenced','$12m'),('Duplicate claims removed','$8m')]):
   yy=y+i*54;para(label,55,yy+7,431,17);para(value,503,yy,100,29,NAVY,500);rect(55,yy+43,550,.5,LINE)
  para('Divisional headline: $110m. Only $54m enters the cash comparison; the remaining categories are separate.',55,y+228,555,17)
  para('Assessed annual AI cost: $52m',55,y+308,580,21,INK,500)
  rect(665,y,480,350,BLUE);para('BENEFIT LESS ALLOCATED ANNUAL AI COST',695,y+25,420,12,NAVY,500)
  para('$2m',695,y+66,420,76,INK,500)
  para('at the assessed $52m annual AI cost',695,y+162,420,20)
  para('A 10% benefit shortfall turns $2m into −$3.4m at the same cost. Break-even requires 96.3% of the assessed $54m benefit.',695,y+215,420,17)
  para('The web version varies cost and benefit retention. This is not project ROI; additional investment and transition costs are excluded.',55,y+368,1090,13,SLATE)
 elif id=='decision':
  rect(55,y,1090,373,'#edf1f3');para('MERIDIAN / BOARD INVESTMENT DECISION',80,y+20,690,12,SLATE,500)
  para('EVIDENCE-GATED FUNDING',830,y+20,270,12,NAVY,600)
  for i,b in enumerate(content.select('.memo-grid>div')): block(b,80+i*553,y+64,503,26)
  for i,p in enumerate(content.select('.memo-bottom p')): para(text(p),80+(i%2)*553,y+252+(i//2)*49,503,15)
 elif id=='deliverables':
  for i,a in enumerate(content.select('.document-grid article')):
   xx=55+(i%2)*563;yy=y+(i//2)*190;rect(xx,yy,527,168,'#edf1f3');rect(xx,yy,3,168,SLATE);block(a,xx+23,yy+21,481,24)
 elif id=='conversation':
  para(text(content.select_one('.lede')),55,y,860,26)
  rect(55,y+109,420,56,NAVY);para('Discuss an assessment ↗',77,y+121,375,23,'#ffffff',500)
  c.linkURL('https://alphaworx.io/#contact',(55,H-y-165,475,H-y-109),relative=0)
  para('alphaworx.io  /  info@alphaworx.io',55,y+187,1000,20,NAVY)
  para(text(content.select_one('.method-note .case-code')),55,y+264,1090,11,SLATE,500)
  para(text(content.select_one('.method-note p')),55,y+287,1040,16)
 rect(55,623,1090,.7,LINE)
 # Footers intentionally outside content bounds.
 foot=text(s.select_one('.slide-foot p'));style=ParagraphStyle('foot',fontName='Plex400',fontSize=9,leading=12,textColor=HexColor(SLATE))
 pp=Paragraph(escape(foot),style);_,ph=pp.wrap(1010,50);pp.drawOn(c,55,H-635-ph)
 c.setFont('Plex500',11);c.setFillColor(HexColor(NAVY));c.drawRightString(1145,25,f'{page:02} / {slide_total}')
 c.showPage()
c.save();print(out);print('Overflow checks:',issues)
