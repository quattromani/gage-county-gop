#!/usr/bin/env python3
"""Generate a source-derived, standalone Gage County GOP candidate flyer."""
from pathlib import Path
from collections import defaultdict
import json
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'src/data/elections/2026/election-directory.json'
OUT = ROOT / 'output/pdf/gage-county-gop-2026-candidate-flyer.pdf'
d = json.loads(DATA.read_text())
calendar = json.loads((DATA.parent / 'voting-calendar.json').read_text())
candidates = {r['candidateId']:r for r in d['candidates']}
affiliations = {r['affiliationId']:r for r in d['affiliations']}
offices = {r['officeId']:r for r in d['offices']}
by_office = defaultdict(list)
selected = []
for r in d['candidacies']:
    a = affiliations[r['affiliationId']]
    if r['electionStageGroup'] == 'current-general-election' and a['label'] == 'Republican' and a['sourceId']:
        by_office[r['officeId']].append(r)
        selected.append(r)
for rows in by_office.values():
    rows.sort(key=lambda r:(r.get('seat') or '', candidates[r['candidateId']]['displayName']))
fontdir = Path('/System/Library/Fonts/Supplemental')
for name, filename in [('Body','Arial Narrow.ttf'),('Bold','Arial Narrow Bold.ttf'),('Wide','Arial Bold.ttf'),('Regular','Arial.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(fontdir/filename)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold')
RED=HexColor('#AF201B'); NAVY=HexColor('#172C47'); INK=HexColor('#22262C'); GRAY=HexColor('#56606B'); LINE=HexColor('#D8DCE1')
OUT.parent.mkdir(parents=True,exist_ok=True)
c=canvas.Canvas(str(OUT),pagesize=(612,792),pageCompression=1)
c.setTitle('2026 Republican Candidates | Gage County GOP')
c.setAuthor('Gage County GOP')
c.setSubject('Source-dated general-election candidate reference from Local Civic Reference')

def text(s,x,y,size=10,font='Body',color=INK):
    c.setFillColor(color);c.setFont(font,size);c.drawString(x,y,s)

def para(s,x,y,w,size=9,font='Body',color=INK,leading=None):
    p=Paragraph(s,ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.12,textColor=color))
    _,h=p.wrap(w,1000);p.drawOn(c,x,y-h);return y-h

# Compact masthead preserves candidate type size and makes room for voting dates.
c.setFillColor(RED);c.rect(24,763,564,4,fill=1,stroke=0)
c.drawImage(ImageReader(str(ROOT/'src/publications/gage-gop-2026/assets/gop-logo.webp')),24,725,width=55,height=35,preserveAspectRatio=True,anchor='c',mask='auto')
text('GAGE COUNTY GOP',89,743,22,'Wide',NAVY)
text('NEBRASKA  /  GENERAL ELECTION  /  NOVEMBER 3, 2026',90,727,9,'Bold',GRAY)
c.linkURL('https://www.gagecountygop.org/',(24,725,588,760),relative=0)
text('2026 REPUBLICAN CANDIDATES',24,703,24,'Wide',NAVY)
c.setFillColor(RED);c.rect(24,673,564,22,fill=1,stroke=0)
text('Take this with you to vote for Republican Party candidates.',33,679,13,'Bold',white)
text('Your address determines your ballot. Follow its offices, districts, and voting limits.',24,661,9.5,'Body',INK)

W=132; TOP=649; OFFICE_GAP=6; visited=[]; oval_count=0

def heading(label,x,y):
    c.setFillColor(NAVY);c.rect(x,y-18,W,18,fill=1,stroke=0)
    text(label,x+5,y-12,10,'Bold',white)
    return y-22

def office(oid,x,y,label=None):
    global oval_count
    rows=by_office[oid]; o=offices[oid]; visited.extend(r['candidacyId'] for r in rows)
    label=label or o['officeName'].replace('Gage County ','').replace('Nebraska ','')
    if label.endswith('Public Schools'):label=label.replace(' Public Schools','')
    label=label.replace(' Township Board','').replace(' Village Board','')
    if o['voteFor']>1 and oid!='office-beatrice-city-council':
        label += f" · Vote up to {o['voteFor']}"
    y=para(escape(label),x,y,W,8.8,'Bold',INK,9.6)
    for r in rows:
        name=candidates[r['candidateId']]['displayName']
        if oid=='office-beatrice-city-council':
            name += ' (' + r['seat'] + ')' 
        c.setStrokeColor(INK);c.setLineWidth(.55)
        c.ellipse(x+.4,y-7.9,x+7.6,y-3.7,stroke=1,fill=0)
        oval_count += 1
        y=para(escape(name),x+11,y,W-11,10,'Wide',RED,11)
    y-=OFFICE_GAP/2
    c.setStrokeColor(LINE);c.setLineWidth(.4);c.line(x,y,x+W,y)
    return y-OFFICE_GAP/2

def section(title,ids,x,y,labels=None):
    y=heading(title,x,y)
    if title=='CITIES & VILLAGES':
        text('Village boards unless otherwise noted',x,y-6.8,7.4,'Body',GRAY)
        y-=13
    for oid in ids:y=office(oid,x,y,(labels or {}).get(oid))
    return y-3

# Office IDs define presentation order only; every candidate value comes from DATA.
x=24;y=TOP
labels={'office-us-senator':'U.S. Senate','office-us-house-district-3':'U.S. House - District 3','office-nebraska-governor':'Governor','office-nebraska-legislature-district-30':'Legislature - District 30','office-state-board-of-education-district-5':'State Board of Education - Dist. 5'}
y=section('FEDERAL', ['office-us-senator','office-us-house-district-3'],x,y,labels)
y=section('STATE', ['office-nebraska-governor','office-nebraska-secretary-of-state','office-nebraska-state-treasurer','office-nebraska-attorney-general','office-nebraska-state-auditor','office-nebraska-legislature-district-30','office-state-board-of-education-district-5'],x,y,labels)
y=section('SCHOOL BOARDS',sorted([oid for oid in by_office if offices[oid]['category']=='School Boards']),x,y)
bottoms=[y]
x=168;y=TOP;OFFICE_GAP=9
y=section('COUNTY', ['office-gage-county-supervisor-district-1','office-gage-county-supervisor-district-3','office-gage-county-supervisor-district-5','office-gage-county-supervisor-district-7','office-gage-county-assessor','office-gage-county-attorney','office-gage-county-clerk','office-gage-county-register-of-deeds','office-gage-county-sheriff','office-gage-county-surveyor','office-gage-county-treasurer'],x,y)
y=section('OTHER LOCAL DISTRICTS',sorted([oid for oid in by_office if offices[oid]['category']=='Other Local Districts']),x,y,{'office-esu-5-district-5':'ESU 5 - District 5','office-esu-5-district-7':'ESU 5 - District 7','office-norris-public-power-district-subdivision-4':'Norris Public Power - Subdiv. 4'})
bottoms.append(y)
x=312;y=TOP;OFFICE_GAP=3
y=section('CITIES & VILLAGES',sorted([oid for oid in by_office if offices[oid]['category']=='Cities & Villages']),x,y)
bottoms.append(y)
x=456;y=TOP;OFFICE_GAP=10
y=section('TOWNSHIP BOARDS',sorted([oid for oid in by_office if offices[oid]['category']=='Township Boards']),x,y)
bottoms.append(y)
print('Column bottoms:',bottoms)
assert min(bottoms)>183, 'Content overlaps footer'
assert sorted(visited)==sorted(r['candidacyId'] for r in selected), 'Missing or duplicate candidate listing'

assert oval_count == len(selected), 'One oval required per listing'
text('KEY VOTING DATES',24,180,9,'Bold',NAVY)
text('2026  /  ALL TIMES CENTRAL',448,180,8,'Bold',GRAY)
c.setFillColor(HexColor('#F1F3F5'));c.rect(24,84,564,89,fill=1,stroke=0)
c.setStrokeColor(RED);c.setLineWidth(1.3);c.line(24,173,588,173)
for i, milestone in enumerate(calendar['milestones']):
    tx=24+i*112.8
    if i:
        c.setStrokeColor(LINE);c.setLineWidth(.6);c.line(tx,91,tx,164)
    text(milestone['label'],tx+7,156,12,'Bold',RED)
    bottom=para(escape(milestone['description']).replace('\n','<br/>'),tx+7,148,98.8,9,'Regular',INK,10.5)
    assert bottom>=88, 'Voting date text exceeds panel'
c.linkURL(calendar['source']['url'],(24,84,588,173),relative=0)
text('gagecountygop.org',24,65,17,'Bold',NAVY)
text('Provided by Gage County GOP',385,67,10,'Bold',NAVY)
c.linkURL('https://www.gagecountygop.org/',(24,60,220,80),relative=0)
para('Includes documented Republicans in nonpartisan races. Unconfirmed affiliations omitted. Listing does not imply endorsement.',24,55,564,8,color=GRAY,leading=8.5)
para('Candidate sources: Local Civic Reference; county filings Aug. 3, state filings July 15; reviewed Aug. 12, 2026.<br/>Voting dates: Nebraska Secretary of State 2026 Election Calendar (linked above). Prepared Sept. 26, 2026. Not an official ballot.',24,43,564,8,color=GRAY,leading=8.5)
c.showPage();c.save()
r=PdfReader(str(OUT));assert len(r.pages)==1
assert tuple(float(v) for v in r.pages[0].mediabox)==(0.,0.,612.,792.)
extracted=' '.join(r.pages[0].extract_text().split())
for row in selected:
    name=candidates[row['candidateId']]['displayName'];assert name in extracted,name
print(f'Validated {len(selected)} listings; {len(set(r["candidateId"] for r in selected))} distinct candidates; {len(by_office)} offices. {OUT}')
