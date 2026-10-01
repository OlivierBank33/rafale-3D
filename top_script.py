# Classement : les 8 avions les plus rapides (vitesse max)
INTRO = dict(say="Les huit avions les plus rapides. Le numéro un traverserait la France en moins de vingt minutes. Reste jusqu'au bout !",
             show="Les 8 avions les plus rapides. Le n°1 traverserait la France en moins de 20 minutes. Reste jusqu'au bout !")
OUTRO = dict(say="Tu t'attendais à ce classement ? Dis-moi en commentaire lequel tu voudrais piloter !",
             show="Tu t'attendais à ce classement ? Dis-moi en commentaire lequel tu voudrais piloter !")
VMAX = 3530
TOP = [  # du n°8 au n°1
    dict(img='spitfire', name='SPITFIRE', kmh=600, lab='≈ 600 km/h', rank=8,
         say="Numéro huit : le Spitfaïeur. Environ six cents kilomètres heure. Une hélice, un moteur à pistons : la référence en mille neuf cent quarante.",
         show="N°8 : le Spitfire. Environ 600 km/h. Une hélice, un moteur à pistons : la référence en 1940."),
    dict(img='b52', name='B-52', kmh=1050, lab='≈ 1 050 km/h', rank=7,
         say="Numéro sept : le bé cinquante-deux. Plus de mille kilomètres heure, avec huit moteurs.",
         show="N°7 : le B-52. Plus de 1 000 km/h, avec huit moteurs."),
    dict(img='harrier', name='HARRIER', kmh=1180, lab='≈ 1 180 km/h', rank=6,
         say="Numéro six : le Harrieur. Environ mille cent quatre-vingts kilomètres heure. Il décolle à la verticale, mais reste sous la vitesse du son.",
         show="N°6 : le Harrier. Environ 1 180 km/h. Il décolle à la verticale, mais reste sous la vitesse du son."),
    dict(img='concorde', name='CONCORDE', kmh=2180, lab='Mach 2,04', rank=5,
         say="Numéro cinq : le Concorde. Plus de deux fois la vitesse du son, avec une centaine de passagers à bord.",
         show="N°5 : le Concorde. Plus de deux fois la vitesse du son, avec une centaine de passagers à bord."),
    dict(img='m2000', name='MIRAGE 2000', kmh=2340, lab='Mach 2,2', rank=4,
         say="Numéro quatre : le Mirage deux mille. Mach deux virgule deux. Le chasseur à aile delta de Dassault.",
         show="N°4 : le Mirage 2000. Mach 2,2. Le chasseur à aile delta de Dassault."),
    dict(img='f22', name='F-22 RAPTOR', kmh=2410, lab='Mach 2,25', rank=3,
         say="Numéro trois : le F vingt-deux Raptor. Furtif, et capable de voler en supersonique sans postcombustion.",
         show="N°3 : le F-22 Raptor. Furtif, et capable de voler en supersonique sans postcombustion."),
    dict(img='f15', name='F-15 EAGLE', kmh=2650, lab='Mach 2,5', rank=2,
         say="Numéro deux : le F quinze Eagle. Mach deux virgule cinq. Un chasseur des années soixante-dix, toujours parmi les plus rapides.",
         show="N°2 : le F-15 Eagle. Mach 2,5. Un chasseur des années 70, toujours parmi les plus rapides."),
    dict(img='sr71', name='SR-71 BLACKBIRD', kmh=3530, lab='3 529 km/h', rank=1,
         say="Et le numéro un... le èss ère soixante et onze Blakbeurde ! Trois mille cinq cent vingt-neuf kilomètres heure, en mille neuf cent soixante-seize. Un record toujours imbattu pour un avion à réacteurs.",
         show="Et le n°1... le SR-71 Blackbird ! 3 529 km/h, en 1976. Un record toujours imbattu pour un avion à réacteurs."),
]
