"""Archive generator for the retired badge; does not overwrite the active courthouse sticker."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math
root=Path(__file__).resolve().parents[1]
scale=2
im=Image.new('RGB',(1080*scale,1080*scale),'#f4f1ea')
d=ImageDraw.Draw(im)
navy='#172c47'; red='#af201b'
def ellipse(box,fill,outline=None,width=1):d.ellipse(tuple(v*scale for v in box),fill=fill,outline=outline,width=width*scale)
def text(value,y,size,color,bold=True):
 font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf' if bold else '/System/Library/Fonts/Supplemental/Arial.ttf',size*scale)
 d.text((540*scale,y*scale),value,font=font,fill=color,anchor='mt')
def star(x,y,r,color):
 pts=[]
 for i in range(10):
  a=-math.pi/2+i*math.pi/5;rr=r if i%2==0 else r*.42;pts.append(((x+math.cos(a)*rr)*scale,(y+math.sin(a)*rr)*scale))
 d.polygon(pts,fill=color)
ellipse((77,92,1003,1018),'#dfdcd6')
ellipse((72,72,1008,1008),'white',navy,7)
ellipse((91,91,989,989),'white',red,3)
for x,y,r in [(400,225,23),(470,210,28),(540,200,34),(610,210,28),(680,225,23)]:star(x,y,r,navy)
text('I',282,138,navy)
text('VOTED!',425,165,red)
d.rounded_rectangle((253*scale,632*scale,827*scale,707*scale),radius=4*scale,fill=navy)
text('GAGE COUNTY',646,43,'white')
text('NEBRASKA',745,28,navy)
text('2026',804,54,navy)
star(420,840,11,red);star(660,840,11,red)
out=root/'src/publications/gage-gop-2026/assets/sticker-retired-badge.png'
im.resize((1080,1080),Image.Resampling.LANCZOS).save(out,optimize=True)
print(out)
