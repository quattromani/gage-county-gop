#!/usr/bin/env python3
"""Render the canonical Republican candidate projection as a continuous phone card."""
from pathlib import Path
from collections import defaultdict
from xml.sax.saxutils import escape
from io import BytesIO
import json
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'src/data/elections/2026'
OUT=ROOT/'output/pdf/gage-county-gop-2026-mobile-card.pdf'
d=json.loads((DATA/'election-directory.json').read_text())
recommendations=json.loads((ROOT/'src/publications/gage-gop-2026/publication.json').read_text())['recommendations']['candidacyIds']
judicial=json.loads((DATA/'judicial-retention.json').read_text())
calendar=json.loads((DATA/'voting-calendar.json').read_text())
candidates={v['candidateId']:v for v in d['candidates']}
affiliations={v['affiliationId']:v for v in d['affiliations']}
offices={v['officeId']:v for v in d['offices']}
groups=defaultdict(list)
for r in d['candidacies']:
    aff=affiliations[r['affiliationId']]
    if r['electionStageGroup']=='current-general-election' and aff['label']=='Republican' and aff['sourceId']:
        groups[r['officeId']].append(r)
for rows in groups.values():
    rows.sort(key=lambda r:(r.get('seat') or '',candidates[r['candidateId']]['displayName']))
fontdir=Path('/System/Library/Fonts/Supplemental')
for name,file in [('Mobile','Arial.ttf'),('MobileBold','Arial Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(fontdir/file)))
pdfmetrics.registerFontFamily('Mobile',normal='Mobile',bold='MobileBold')
NAVY=HexColor('#172C47');RED=HexColor('#AF201B');INK=HexColor('#22262C');GRAY=HexColor('#56606B');LINE=HexColor('#D8DCE1')
WIDTH=360; MARGIN=24; CONTENT=312
ops=[];cursor=0;visited=[];oval_count=0

def gap(n):
    global cursor
    cursor+=n

def rectangle(x,top,w,h,color):ops.append(('rect',x,top,w,h,color))

def para(s,size=13,bold=False,color=INK,x=MARGIN,w=CONTENT,leading=None):
    global cursor
    p=Paragraph(s,ParagraphStyle('mobile',fontName='MobileBold' if bold else 'Mobile',fontSize=size,leading=leading or size*1.3,textColor=color))
    _,h=p.wrap(w,20000)
    ops.append(('para',p,x,cursor,h));cursor+=h

def rule():ops.append(('line',MARGIN,cursor,WIDTH-MARGIN,cursor,LINE))

def section(title):
    global cursor
    gap(19)
    rectangle(MARGIN,cursor,CONTENT,34,NAVY)
    cursor+=7
    para(escape(title.upper()),15,True,white,x=MARGIN+12,w=CONTENT-24,leading=20)
    gap(19)

def office(oid):
    global oval_count
    o=offices[oid]
    label=o['officeName'].replace('Gage County ','').replace('Nebraska ','')
    if oid=='office-nebraska-governor':label='Governor'
    para(escape(label),13,True,NAVY,leading=17)
    rows=groups[oid]
    if o['voteFor']>1 and oid!='office-beatrice-city-council':
        gap(3);para(f"Vote for up to {o['voteFor']}",11,color=GRAY,leading=15)
    gap(7)
    for r in rows:
        name=candidates[r['candidateId']]['displayName']
        if oid=='office-beatrice-city-council':
            para(escape(r['seat']),11,color=GRAY,x=MARGIN+20,w=CONTENT-20,leading=15)
            gap(2)
        ops.append(('oval',MARGIN+1,cursor+5.2,10,6.2))
        oval_count+=1
        para(escape(name + (' (write-in)' if r.get('filingMethod')=='Declared write-in' else '')),15,True,RED,x=MARGIN+20,w=CONTENT-20,leading=20)
        if r.get('filingMethod')=='Declared write-in':
            para('Write this name on the write-in line and mark its oval.',10,color=GRAY,x=MARGIN+20,w=CONTENT-20)
        if affiliations[r['affiliationId']].get('evidenceType')=='reported-affiliation':
            para('Affiliation reported by Voter Information Project.',10,color=GRAY,x=MARGIN+20,w=CONTENT-20)
        visited.append(r['candidacyId'])
        gap(5)
    gap(6);rule();gap(13)

gap(22)
rectangle(MARGIN,cursor,CONTENT,4,RED);gap(12)
ops.append(('image',ROOT/'src/publications/gage-gop-2026/assets/gop-logo.webp',MARGIN,cursor,49,32))
para('GAGE COUNTY GOP',17,True,NAVY,x=83,w=253,leading=21)
para('NEBRASKA',10,True,GRAY,x=84,w=252,leading=14)
gap(15)
para('2026 Republican<br/>candidate card',27,True,NAVY,leading=30)
gap(9)
para('GENERAL ELECTION · NOVEMBER 3',11,True,GRAY,leading=16)
gap(13)
rectangle(MARGIN,cursor,CONTENT,62,RED)
cursor+=10
para('Take this with you to vote for<br/>Republican Party candidates.',14,True,white,x=36,w=288,leading=20)
gap(22)
para('Your address determines your ballot.<br/>Follow its offices, districts, and voting limits.',12,color=INK,leading=17)
para('Filled ovals indicate Gage County GOP recommendations.',11,True,color=NAVY,leading=17)
para('Scroll for candidates and key voting dates.',11,color=GRAY,leading=17)

federal=['office-us-senator','office-us-house-district-3']
state=['office-nebraska-governor','office-nebraska-secretary-of-state','office-nebraska-state-treasurer','office-nebraska-attorney-general','office-nebraska-state-auditor','office-nebraska-legislature-district-30','office-state-board-of-education-district-5']
county=[f'office-gage-county-supervisor-district-{n}' for n in [1,3,5,7]]+['office-gage-county-assessor','office-gage-county-attorney','office-gage-county-clerk','office-gage-county-register-of-deeds','office-gage-county-sheriff','office-gage-county-surveyor','office-gage-county-treasurer']
sections=[('Federal',federal),('State',state),('County',county)]
for title,category in [('School boards','School Boards'),('Cities & villages','Cities & Villages'),('Township boards','Township Boards'),('Other local districts','Other Local Districts')]:
    sections.append((title,sorted(oid for oid in groups if offices[oid]['category']==category)))
for title,ids in sections:
    section(title)
    for oid in ids:office(oid)
section(judicial['copy']['heading'])
para(escape(judicial['copy']['introduction']),12,leading=17);gap(9)
para(escape(judicial['copy']['instructions']),12,True,leading=17);gap(9)
para('Listed for ballot reference. Inclusion does not recommend a Yes or No vote.',11,color=GRAY);gap(12)
for court in judicial['data']['courts']:
    para(escape(court['name']+' - '+court['scope']),14,True,NAVY);gap(10)
    for question in judicial['data']['questions']:
        if question['courtId']!=court['courtId']:continue
        para(escape(question['name']+' - '+question['affiliation']['label']),15,True,NAVY);gap(3)
        para('Reported by Voter Information Project',10,color=GRAY);gap(3)
        para(escape(question['ballotQuestion']),12);gap(3)
        para('Six-year term. Ballot choices: Yes or No.',11,color=GRAY);gap(13)
    rule();gap(15)
para('Resources for evaluating judges',14,True,NAVY);gap(9)
for resource in judicial['data']['voterResources']:
    para('<link href="'+escape(resource['url'])+'">'+escape(resource['title'])+'</link>',11,True,NAVY);gap(4)
    para(escape(resource['description']),11,color=GRAY);gap(10)
retention_source_top=cursor
para('Sources: Nebraska Secretary of State final retention list, August 3, 2026; Nebraska Judicial Branch voter guide. Reviewed October 26, 2026.',10,color=GRAY);gap(10)
retention_source_bottom=cursor
section('Key voting dates')
para('2026 · All times Central',12,True,GRAY,leading=16);gap(16)
dates_top=cursor
for milestone in calendar['milestones']:
    para(milestone['label'],18,True,RED,leading=23);gap(5)
    description=escape(milestone['description']).replace('\n','<br/>')
    description=description.replace(' at the County Election Office.', '<br/>at the County Election Office.')
    para(description,13,color=INK,leading=18)
    gap(13);rule();gap(17)
dates_bottom=cursor
para('Source: Nebraska Secretary of State<br/>2026 Official Election Calendar',10,color=GRAY,leading=14)
gap(26)
rectangle(MARGIN,cursor,CONTENT,3,RED);gap(15)
web_top=cursor
para('gagecountygop.org',22,True,NAVY,leading=28)
para('Provided by Gage County GOP',12,True,NAVY,leading=17)
gap(17)
para('Includes documented Republicans in nonpartisan races.<br/>Unconfirmed affiliations are omitted.<br/>Filled ovals indicate Gage County GOP recommendations.',11,color=GRAY,leading=15)
gap(10)
para('Candidate source: Local Civic Reference. Records reviewed '+d['lastValidated']+'. See partyreveal.com for individual evidence and source dates.',10,color=GRAY,leading=14)
gap(10)
para('Updated October 26, 2026.<br/>This reference is not an official ballot.',10,color=GRAY,leading=14)
gap(24)
HEIGHT=cursor
assert sorted(visited)==sorted(r['candidacyId'] for rows in groups.values() for r in rows)
assert sorted(recommendations)==sorted(visited), 'Recommendation roster requires confirmation'
assert oval_count==len(visited)==83
c=canvas.Canvas(str(OUT),pagesize=(WIDTH,HEIGHT),pageCompression=1)
c.setTitle('Gage County GOP | 2026 Mobile Candidate Card')
c.setAuthor('Gage County GOP')
for op in ops:
    kind=op[0]
    if kind=='para':
        _,p,x,top,h=op;p.drawOn(c,x,HEIGHT-top-h)
    elif kind=='rect':
        _,x,top,w,h,color=op;c.setFillColor(color);c.rect(x,HEIGHT-top-h,w,h,stroke=0,fill=1)
    elif kind=='image':
        _,path,x,top,w,h=op;c.drawImage(ImageReader(str(path)),x,HEIGHT-top-h,width=w,height=h,mask='auto')
    elif kind=='line':
        _,x,y,x2,y2,color=op;c.setStrokeColor(color);c.setLineWidth(.65);c.line(x,HEIGHT-y,x2,HEIGHT-y2)
    elif kind=='oval':
        _,x,top,w,h=op;c.setStrokeColor(INK);c.setFillColor(INK);c.setLineWidth(.85);c.ellipse(x,HEIGHT-top-h,x+w,HEIGHT-top,stroke=1,fill=1)
c.linkURL('https://www.gagecountygop.org/',(24,HEIGHT-web_top-48,336,HEIGHT-web_top),relative=0)
c.linkURL(calendar['source']['url'],(24,HEIGHT-dates_bottom,336,HEIGHT-dates_top),relative=0)
c.linkURL(judicial['data']['questions'][0]['sources'][0]['url'],(24,HEIGHT-retention_source_bottom,336,HEIGHT-retention_source_top),relative=0)
c.showPage();c.save()
r=PdfReader(str(OUT));assert len(r.pages)==1
extracted=' '.join(r.pages[0].extract_text().split())
for rows in groups.values():
    for row in rows:assert candidates[row['candidateId']]['displayName'] in extracted
for question in judicial['data']['questions']:assert question['ballotQuestion'] in extracted
assert 'Anthony M. Landon (write-in)' in extracted
print(f'Validated one continuous page: {WIDTH} x {HEIGHT:.1f} pt; {len(visited)} listings and {oval_count} ovals. PNG target: 1080 x {round(HEIGHT*3)} px.')
