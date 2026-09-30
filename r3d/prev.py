import sys
from PIL import Image
ims=[Image.open(p).convert('RGBA') for p in sys.argv[2:]]
w=sum(i.width for i in ims); h=max(i.height for i in ims)
s=Image.new('RGBA',(w,h),(40,48,64,255)); x=0
for im in ims: s.alpha_composite(im,(x,0)); x+=im.width
s.convert('RGB').save(sys.argv[1])
