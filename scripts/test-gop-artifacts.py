"""Check regenerated cross-format content; requires the publication Python dependencies."""
from pathlib import Path
import json
from pypdf import PdfReader
from PIL import Image
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'src/data/elections/2026/election-directory.json').read_text())
j=json.loads((root/'src/data/elections/2026/judicial-retention.json').read_text())
flyer=PdfReader(root/'output/pdf/gage-county-gop-2026-candidate-flyer.pdf')
mobile=PdfReader(root/'output/pdf/gage-county-gop-2026-mobile-card.pdf')
assert len(flyer.pages)==2 and len(mobile.pages)==1
normalize=lambda s:' '.join(s.split())
f=normalize(flyer.pages[0].extract_text()); m=normalize(mobile.pages[0].extract_text()); retention=normalize(flyer.pages[1].extract_text())
for candidate in d['candidates']:
 assert candidate['displayName'] in f,candidate['displayName']
 assert candidate['displayName'] in m,candidate['displayName']
for question in j['data']['questions']:
 assert question['ballotQuestion'] in retention,question['name']
 assert question['ballotQuestion'] in m,question['name']
for text in [f,m]:
 assert 'Anthony M. Landon (write-in)' in text
 assert 'Mary D. Benes' not in text
assert 'Inclusion does not recommend a Yes or No vote.' in retention
assert 'Inclusion does not recommend a Yes or No vote.' in m
im=Image.open(root/'output/pdf/gage-county-gop-2026-mobile-card.png')
assert im.width==1080 and abs(im.height-float(mobile.pages[0].mediabox.height)*3)<=1
print(f'Artifacts passed: {len(d["candidacies"])} listings, {len(d["candidates"])} people, six exact retention questions; 2-page flyer, continuous mobile PDF, {im.width} x {im.height} PNG.')
