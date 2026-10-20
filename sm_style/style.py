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

# ---------- frame 1 : cockpit de nuit, alarme ----------
def frame_cockpit(t=0.0):
    s=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H); c=cairo.Context(s)
    g=cairo.LinearGradient(0,0,0,H); g.add_color_stop_rgb(0,0.03,0.04,0.08); g.add_color_stop_rgb(1,0.01,0.01,0.02); c.set_source(g); c.paint()
    # pare-brise
    c.save(); c.new_path(); c.move_to(80,420); c.line_to(1000,420); c.line_to(1060,1000); c.line_to(20,1000); c.close_path(); c.clip()
    g=cairo.LinearGradient(0,420,0,1000); g.add_color_stop_rgb(0,0.07,0.09,0.17); g.add_color_stop_rgb(1,0.12,0.13,0.22); c.set_source(g); c.paint()
    r=random.Random(3)
    for _ in range(120):
        x=r.random()*W; y=420+r.random()*580; L=60+r.random()*80
        c.move_to(x,y); c.line_to(x-14,y+L); c.set_source_rgba(0.6,0.7,0.9,0.18); c.set_line_width(2); c.stroke()
    # éclair
    c.new_path(); pts=[(720,420),(690,560),(735,575),(680,760),(760,600),(715,590),(750,420)]
    c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]; c.close_path()
    radial(c,720,560,420,(0.65,0.75,1.0),0.35); c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]; c.close_path(); c.set_source_rgb(0.92,0.95,1); c.fill()
    for (cx,cy,cr) in ((150,520,160),(380,480,130),(920,510,170),(560,450,110)):
        c.new_path(); c.arc(cx,cy,cr,0,2*math.pi); c.set_source_rgba(0.05,0.06,0.11,0.9); c.fill()
    c.restore()
    # montant central + cadre
    for pts in ([(530,420),(550,420),(560,1000),(520,1000)],):
        c.new_path(); c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]; c.close_path(); fill_stroke(c,(0.09,0.10,0.13),8)
    c.new_path(); c.move_to(80,420); c.line_to(1000,420); c.line_to(1060,1000); c.line_to(20,1000); c.close_path(); c.set_source_rgb(*INK); c.set_line_width(14); c.stroke()
    # tableau de bord
    c.new_path(); c.move_to(0,960); c.curve_to(300,920,780,920,W,960); c.line_to(W,H); c.line_to(0,H); c.close_path(); fill_stroke(c,(0.10,0.11,0.14),10)
    for i,(x,y) in enumerate(((200,1080),(370,1070),(710,1070),(880,1080))):
        c.new_path(); c.arc(x,y,72,0,2*math.pi); fill_stroke(c,(0.02,0.03,0.05),8)
        radial(c,x,y,80,(0.2,0.9,0.7),0.12)
        c.new_path(); c.arc(x,y,58,math.pi*0.8,math.pi*2.2); c.set_source_rgba(0.3,1,0.8,0.8); c.set_line_width(4); c.stroke()
        a=math.pi*(0.9+0.3*i)+ (1.2 if i==2 else 0)
        c.move_to(x,y); c.line_to(x+math.cos(a)*50,y+math.sin(a)*50); c.set_source_rgb(1,0.95,0.8); c.set_line_width(5); c.stroke()
    # alarme rouge
    radial(c,540,1060,520,(1,0.1,0.12),0.5)
    rr(c,440,1020,200,80,14); fill_stroke(c,(1,0.15,0.18),7)
    text(c,"ENG FIRE",540,1078,52,(1,0.95,0.95))
    # pilote de dos, 3/4
    pilot_body(c,330,1300,1.25)
    limb(c,[(300,1340),(390,1250),(470,1180)]); limb(c,[(360,1340),(460,1290),(520,1200)])
    head(c,330,1210,120,'worried',look=(28,-6),rim=(1,0.2,0.2))
    # lueur rouge de fill sur tout
    c.set_source_rgba(1,0.1,0.1,0.06); c.paint()
    vignette(c,0.85); grain(c,7)
    text(c,"ÉPISODE 1",W/2,250,46,(0.85,0.88,0.95),'Montserrat',track=6)
    text(c,"MOTEUR EN FEU",W/2,370,128,(1,0.32,0.32),glow=1.0)
    watermark(c); return s

# ---------- frame 2 : avion seul au-dessus de l'océan ----------
def frame_ocean():
    s=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H); c=cairo.Context(s)
    g=cairo.LinearGradient(0,0,0,H); g.add_color_stop_rgb(0,0.02,0.03,0.08); g.add_color_stop_rgb(0.55,0.08,0.10,0.22); g.add_color_stop_rgb(0.56,0.03,0.05,0.10); g.add_color_stop_rgb(1,0.01,0.02,0.04); c.set_source(g); c.paint()
    r=random.Random(5)
    for _ in range(260):
        c.new_path(); c.arc(r.random()*W,r.random()*1000,r.choice((1,1,1.5,2.4)),0,7); c.set_source_rgba(1,1,1,0.3+0.6*r.random()); c.fill()
    radial(c,800,330,300,(1,0.95,0.8),0.25); c.new_path(); c.arc(800,330,90,0,7); c.set_source_rgb(0.98,0.96,0.88); c.fill()
    c.new_path(); c.arc(840,310,80,0,7); c.set_source_rgb(0.03,0.04,0.09); c.fill()
    # reflet lune
    for k in range(18):
        y=1080+k*38; w=180-k*7
        rr(c,800-w/2+r.uniform(-20,20),y,w,6,3); c.set_source_rgba(1,0.95,0.8,0.25-k*0.012); c.fill()
    for k in range(40):
        y=1070+r.random()*850; x=r.random()*W
        c.move_to(x,y); c.line_to(x+40+r.random()*80,y); c.set_source_rgba(0.5,0.6,0.8,0.12); c.set_line_width(3); c.stroke()
    # fumée
    for k in range(14):
        x=430-k*28; y=760+k*16+math.sin(k)*10; rad=22+k*6
        c.new_path(); c.arc(x,y,rad,0,7); c.set_source_rgba(0.25,0.25,0.3,0.55-k*0.03); c.fill()
    # avion (bimoteur de profil, style flat épais)
    c.save(); c.translate(560,720); c.rotate(-0.06)
    c.new_path(); c.move_to(-230,-10); c.curve_to(-120,-38,150,-40,230,-14); c.curve_to(260,-4,262,22,232,30); c.curve_to(100,44,-120,40,-230,22); c.close_path(); fill_stroke(c,(0.92,0.93,0.96),9)
    c.new_path(); c.move_to(-200,-12); c.line_to(-250,-110); c.line_to(-205,-110); c.line_to(-150,-20); c.close_path(); fill_stroke(c,(0.85,0.2,0.2),8)
    for i in range(7): rr(c,-110+i*42,-18,24,18,6); fill_stroke(c,(0.35,0.75,1.0),4)
    c.new_path(); c.move_to(170,-28); c.curve_to(195,-34,220,-26,232,-12); c.line_to(185,-12); c.close_path(); fill_stroke(c,(0.35,0.75,1.0),5)
    c.new_path(); c.move_to(-40,14); c.line_to(80,14); c.line_to(-10,70); c.line_to(-90,70); c.close_path(); fill_stroke(c,(0.8,0.81,0.86),8)
    rr(c,-80,30,90,34,16); fill_stroke(c,(0.6,0.62,0.68),7)
    c.restore()
    radial(c,480,760,140,(1,0.45,0.1),0.7)
    for k,(dx,dy,rad) in enumerate(((0,0,26),(-18,-10,18),(10,-16,14))):
        c.new_path(); c.arc(480+dx,760+dy,rad,0,7); c.set_source_rgb(*((1,0.85,0.3),(1,0.5,0.1),(1,0.95,0.6))[k]); c.fill()
    # carte de distance
    rr(c,90,1240,900,220,30); c.set_source_rgba(0,0,0,0.45); c.fill()
    text(c,"1 200 KM",300,1350,110,(1,1,1)); text(c,"jusqu'à la côte",300,1405,34,(0.7,0.75,0.85),'Montserrat')
    text(c,"40 MIN",780,1350,110,(1,0.55,0.15),glow=0.6); text(c,"de carburant",780,1405,34,(0.7,0.75,0.85),'Montserrat')
    vignette(c,0.8); grain(c,9)
    text(c,"AU MILIEU DE L'ATLANTIQUE",W/2,300,74,(0.9,0.93,1.0),glow=0.4)
    watermark(c); return s

# ---------- frame 3 : le choix ----------
def frame_choice():
    s=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H); c=cairo.Context(s)
    c.set_source_rgb(0.02,0.02,0.04); c.paint()
    for side,(col,lab,sub) in enumerate((((0.2,0.75,1.0),"A","FAIRE DEMI-TOUR"),((1.0,0.5,0.12),"B","POSER SUR L'EAU"))):
        y0=520+side*620
        rr(c,70,y0,940,560,40); c.set_source_rgba(*col,0.08); c.fill_preserve(); c.set_source_rgba(*col,0.85); c.set_line_width(5); c.stroke()
        c.save(); rr(c,70,y0,940,560,40); c.clip(); radial(c,300,y0+280,500,col,0.22); c.restore()
        text(c,lab,200,y0+340,300,col,glow=1.0)
        text(c,sub,640,y0+250,92,(1,1,1))
        text(c,("1 moteur, 1 200 km, 40 min" if side==0 else "de nuit, eau à 12 °C"),640,y0+320,36,(0.75,0.8,0.9),'Montserrat')
        if side==0: text(c,"risque : panne sèche",640,y0+380,36,col,'Montserrat')
        else: text(c,"risque : couler",640,y0+380,36,col,'Montserrat')
    # pilote qui hésite au centre
    c.new_path(); c.arc(W/2,1080,120,0,7); c.set_source_rgb(0.02,0.02,0.04); c.fill()
    head(c,W/2,1080,95,'worried',look=(0,-14))
    text(c,"TU FAIS QUOI ?",W/2,330,140,(1,1,1),glow=0.5)
    text(c,"ÉCRIS A OU B EN COMMENTAIRE",W/2,1800,46,(0.85,0.88,0.95),'Montserrat')
    text(c,"LA MAJORITÉ DÉCIDE DE L'ÉPISODE 2",W/2,1860,34,(1,0.55,0.15),'Montserrat')
    grain(c,11); watermark(c); return s

# ---------- frame 4 : couverture de l'épisode 2 (style « MOST OF YOU SAID ») ----------
def frame_ep2():
    s=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H); c=cairo.Context(s)
    g=cairo.LinearGradient(0,0,0,H); g.add_color_stop_rgb(0,0.04,0.05,0.11); g.add_color_stop_rgb(1,0.01,0.01,0.03); c.set_source(g); c.paint()
    # cockpit éteint, piste éclairée au loin
    radial(c,W/2,900,650,(1,0.75,0.3),0.30)
    for k in range(9):
        y=820+k*k*5; w=8+k*k*3
        c.new_path(); c.arc(W/2-w,y,4+k*0.8,0,7); c.arc(W/2+w,y,4+k*0.8,0,7); c.set_source_rgba(1,0.85,0.4,0.9); c.fill()
    pilot_body(c,W/2,1500,1.4)
    limb(c,[(W/2-70,1540),(W/2-150,1450),(W/2-120,1380)]); limb(c,[(W/2+70,1540),(W/2+150,1450),(W/2+120,1380)])
    head(c,W/2,1390,135,'determined',look=(0,-10),rim=(1,0.75,0.3))
    vignette(c,0.85); grain(c,13)
    text(c,"LA MAJORITÉ A DIT",W/2,300,50,(0.9,0.92,1.0),'Montserrat',track=4)
    text(c,"DEMI-TOUR",W/2,470,190,(0.35,0.85,1.0),glow=1.2)
    text(c,"ÉPISODE 2",W/2,560,44,(1,0.55,0.15),'Montserrat',track=6)
    watermark(c); return s

if __name__=='__main__':
    for n,f in (('1_cockpit',frame_cockpit),('2_ocean',frame_ocean),('3_choix',frame_choice),('4_ep2',frame_ep2)):
        f().write_to_png(f'/home/claude/sm/{n}.png')
