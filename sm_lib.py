"""Bibliothèque du style STICKMAN (histoires interactives) : traits noirs épais, aplats, éclairages, grain."""
import cairo, math, random
W,H=1080,1920
INK=(0.04,0.04,0.06)
def rr(c,x,y,w,h,r):
    c.new_path(); c.arc(x+w-r,y+r,r,-math.pi/2,0); c.arc(x+w-r,y+h-r,r,0,math.pi/2); c.arc(x+r,y+h-r,r,math.pi/2,math.pi); c.arc(x+r,y+r,r,math.pi,1.5*math.pi); c.close_path()
def fill_stroke(c,col,lw=7,a=1):
    c.set_source_rgba(*col,a); c.fill_preserve(); c.set_source_rgba(*INK,a); c.set_line_width(lw); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()
def F(c,s,fam='Bebas Neue'): c.select_font_face(fam,0,1); c.set_font_size(s)
def text(c,s,x,y,size,col,fam='Bebas Neue',glow=0,anchor='c',track=0):
    F(c,size,fam); w=c.text_extents(s).x_advance+track*(len(s)-1)
    x0=x-w/2 if anchor=='c' else x
    def path():
        c.new_path(); xx=x0
        for ch in s:
            c.move_to(xx,y); c.text_path(ch); xx+=c.text_extents(ch).x_advance+track
    if glow:
        for k,a in ((40,.05),(24,.09),(12,.16),(5,.35)):
            path(); c.set_source_rgba(*col,a*glow); c.set_line_width(k); c.set_line_join(1); c.stroke()
    path(); c.set_source_rgba(*col,1); c.fill()
def radial(c,x,y,r,col,a):
    g=cairo.RadialGradient(x,y,0,x,y,r); g.add_color_stop_rgba(0,*col,a); g.add_color_stop_rgba(1,*col,0); c.set_source(g); c.paint()
def vignette(c,s=0.75):
    g=cairo.RadialGradient(W/2,H*0.45,W*0.35,W/2,H*0.45,H*0.75); g.add_color_stop_rgba(0,0,0,0,0); g.add_color_stop_rgba(1,0,0,0,s); c.set_source(g); c.paint()
def grain(c,seed=1,n=9000):
    r=random.Random(seed)
    for _ in range(n):
        c.rectangle(r.random()*W,r.random()*H,2,2); v=r.random(); c.set_source_rgba(v,v,v,0.035); c.fill()
def watermark(c):
    text(c,"@minuteaero",W-60,110,30,(0.75,0.78,0.85),'Montserrat',anchor='l') if False else None
    F(c,28,'Montserrat'); s="@minuteaero"; w=c.text_extents(s).x_advance
    c.move_to(W-50-w,110); c.text_path(s); c.set_source_rgba(0.8,0.82,0.9,0.75); c.fill()

# --- personnage : pilote stickman ---
def limb(c,pts,w=26,col=(0.97,0.97,0.98)):
    for lw,cc in ((w+14,INK),(w,col)):
        c.new_path(); c.move_to(*pts[0])
        for p in pts[1:]: c.line_to(*p)
        c.set_source_rgb(*cc); c.set_line_width(lw); c.set_line_cap(1); c.set_line_join(1); c.stroke()
def head(c,x,y,r,mood='worried',look=(0,0),helmet=True,rim=None):
    c.new_path(); c.arc(x,y,r,0,2*math.pi); fill_stroke(c,(0.98,0.98,0.99),9)
    if rim:  # lumière de bord
        c.save(); c.arc(x,y,r-5,0,2*math.pi); c.clip()
        g=cairo.LinearGradient(x+r,y,x-r*0.2,y); g.add_color_stop_rgba(0,*rim,0.55); g.add_color_stop_rgba(1,*rim,0); c.set_source(g); c.paint(); c.restore()
    c.save(); c.arc(x,y,r-5,0,2*math.pi); c.clip()
    g=cairo.LinearGradient(x,y-r,x,y+r); g.add_color_stop_rgba(0.55,0,0,0,0); g.add_color_stop_rgba(1,0.2,0.25,0.4,0.25); c.set_source(g); c.paint(); c.restore()
    if helmet:
        c.new_path(); c.arc(x,y-r*0.05,r*1.06,math.pi*1.02,math.pi*1.98); c.close_path(); fill_stroke(c,(0.30,0.36,0.30),9)
        rr(c,x-r*0.95,y-r*0.42,r*1.9,r*0.2,8); fill_stroke(c,(0.85,0.7,0.25),6)
        c.new_path(); c.arc(x+r*0.98,y+r*0.1,r*0.22,0,2*math.pi); fill_stroke(c,(0.3,0.36,0.3),6)
        c.new_path(); c.arc(x+r*0.98,y+r*0.1,r*0.22,math.pi*0.3,math.pi*0.9); c.set_line_width(5); c.set_source_rgb(*INK); c.stroke()
        c.new_path(); c.move_to(x+r*0.85,y+r*0.3); c.curve_to(x+r*0.7,y+r*0.75,x+r*0.35,y+r*0.75,x+r*0.15,y+r*0.62); c.set_line_width(6); c.stroke()
    lx,ly=look
    for sx in (-1,1):
        ex,ey=x+sx*r*0.33+lx,y+r*0.02+ly
        c.new_path(); c.save(); c.translate(ex,ey); c.scale(1,1.25); c.arc(0,0,r*0.11,0,2*math.pi); c.restore(); c.set_source_rgb(*INK); c.fill()
        c.new_path(); c.arc(ex+r*0.03,ey-r*0.05,r*0.035,0,2*math.pi); c.set_source_rgb(1,1,1); c.fill()
        c.new_path()
        if mood=='worried': c.move_to(ex-sx*r*0.18,ey-r*0.2); c.line_to(ex+sx*r*0.12,ey-r*0.3)
        elif mood=='determined': c.move_to(ex-sx*r*0.18,ey-r*0.32); c.line_to(ex+sx*r*0.14,ey-r*0.2)
        else: c.move_to(ex-r*0.15,ey-r*0.26); c.line_to(ex+r*0.15,ey-r*0.26)
        c.set_source_rgb(*INK); c.set_line_width(8); c.set_line_cap(1); c.stroke()
    c.new_path()
    if mood=='worried': c.move_to(x-r*0.18+lx,y+r*0.45); c.curve_to(x-r*0.05,y+r*0.36,x+r*0.08,y+r*0.5,x+r*0.2+lx,y+r*0.42)
    elif mood=='determined': c.move_to(x-r*0.16+lx,y+r*0.44); c.line_to(x+r*0.16+lx,y+r*0.4)
    else: c.move_to(x-r*0.12,y+r*0.42); c.curve_to(x,y+r*0.5,x,y+r*0.5,x+r*0.12,y+r*0.42)
    c.set_line_width(7); c.stroke()
    c.new_path(); c.arc(x-r*0.62,y-r*0.15,r*0.05,0,2*math.pi)  # sueur
    if mood=='worried':
        c.new_path(); c.move_to(x-r*0.7,y-r*0.35); c.curve_to(x-r*0.82,y-r*0.15,x-r*0.78,y-r*0.05,x-r*0.7,y-r*0.05); c.curve_to(x-r*0.62,y-r*0.05,x-r*0.58,y-r*0.15,x-r*0.7,y-r*0.35)
        fill_stroke(c,(0.6,0.85,1.0),4)
def pilot_body(c,x,y,s=1.0,arms='yoke'):
    rr(c,x-60*s,y,120*s,190*s,50*s); fill_stroke(c,(0.30,0.36,0.30),9)   # combinaison
    rr(c,x-30*s,y+30*s,60*s,30*s,6); fill_stroke(c,(0.85,0.7,0.25),5)     # écusson
    c.new_path(); c.move_to(x,y+20*s); c.line_to(x,y+180*s); c.set_source_rgba(*INK,.6); c.set_line_width(4); c.stroke()

