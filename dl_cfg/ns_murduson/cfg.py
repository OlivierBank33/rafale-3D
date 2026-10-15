# LA SCIENCE DU VOL 02 : le mur du son. Sources : atmosphère standard (vitesse du son 340 m/s ≈ 1 225 km/h à 15 °C au niveau de la mer ; 295 m/s ≈ 1 062 km/h à 11 km) ;
# Wikipedia « Bell X-1 » (Chuck Yeager, 14 octobre 1947, Mach 1,06) ; « Sonic boom » (bang continu le long de la trajectoire, souvent double) ; « Vapor cone » (condensation, souvent en transsonique, pas une preuve de Mach 1) ;
# « Concorde » (subsonique Mach 0,95 au-dessus des terres, supersonique au-dessus de l'océan ; interdiction FAA des vols civils supersoniques au-dessus du territoire américain, 1973)
SERIES = "LA SCIENCE DU VOL"; EP = "02"; NEXT = "COMMENT UNE AILE PORTE"
SCENES = [
    dict(type='hook', top=("1 225 KM/H", "1 060 KM/H"), sub=("au niveau de la mer", "à 11 000 mètres"),
         gauges=[("VITESSE DU SON · SOL", "340 M/S", 0.85, (0.30, 0.70, 1.0)), ("À 11 000 M", "295 M/S", 0.72, (1.0, 0.86, 0.0))],
         say="Mille deux cent vingt-cinq kilomètres-heure au sol. Mille soixante à onze mille mètres. Le mur du son n'est pas à la même vitesse partout. Alors, c'est quoi, vraiment ?",
         show="1 225 km/h au sol. 1 060 à 11 000 mètres. Le mur du son n'est pas à la même vitesse partout. Alors, c'est quoi, vraiment ?"),
    dict(type='plan', items=["LE SON", "LE CÔNE", "LE BANG", "L'INTERDIT"],
         say="Quatre étapes pour tout comprendre. Et un piège dans lequel presque tout le monde tombe.",
         show="4 étapes pour tout comprendre. Et un piège dans lequel presque tout le monde tombe."),
    dict(type='waves', num=1, title="LE SON",
         say="Un : le son. Un avion pousse l'air devant lui, et crée des ondes de pression qui partent à la vitesse du son. Plus il accélère, plus ces ondes s'entassent devant son nez. À Mach un, elles forment un mur.",
         show="1 : le son. Un avion pousse l'air devant lui, et crée des ondes de pression qui partent à la vitesse du son. Plus il accélère, plus ces ondes s'entassent devant son nez. À Mach 1, elles forment un mur."),
    dict(type='cone', num=2, title="LE CÔNE",
         say="Deux : le cône. Au-delà de Mach un, l'avion dépasse ses propres ondes. Elles se rassemblent derrière lui, en un cône : le cône de Mach.",
         show="2 : le cône. Au-delà de Mach 1, l'avion dépasse ses propres ondes. Elles se rassemblent derrière lui, en un cône : le cône de Mach."),
    dict(type='bang', num=3, title="LE BANG",
         say="Trois : le bang. Quand ce cône balaie le sol, tu entends une détonation, souvent double. Et ce n'est pas un instant unique : l'avion traîne ce bang tout le long de son vol supersonique.",
         show="3 : le bang. Quand ce cône balaie le sol, tu entends une détonation, souvent double. Et ce n'est pas un instant unique : l'avion traîne ce bang tout le long de son vol supersonique."),
    dict(type='yeager', num=None, title="LE PREMIER",
         say="Le premier à passer officiellement le mur du son en vol, c'est Chuck Yeager, le quatorze octobre mille neuf cent quarante-sept, à bord du Bell X un. Mach un virgule zéro six.",
         show="Le premier à passer officiellement le mur du son en vol, c'est Chuck Yeager, le 14 octobre 1947, à bord du Bell X-1. Mach 1,06."),
    dict(type='vapor', num=None, title="LE PIÈGE",
         say="Et ce nuage blanc autour des avions de chasse ? C'est de la vapeur d'eau qui se condense dans une zone de basse pression. Il apparaît souvent juste sous Mach un. Ce n'est donc pas la preuve que l'avion a passé le mur.",
         show="Et ce nuage blanc autour des avions de chasse ? C'est de la vapeur d'eau qui se condense dans une zone de basse pression. Il apparaît souvent juste sous Mach 1. Ce n'est donc pas la preuve que l'avion a passé le mur."),
    dict(type='ban', num=4, title="L'INTERDIT",
         say="Quatre : l'interdit. À cause de ce bang, le Concorde restait sous la vitesse du son au-dessus des terres. Il n'accélérait à Mach deux qu'une fois au-dessus de l'océan.",
         show="4 : l'interdit. À cause de ce bang, le Concorde restait sous la vitesse du son au-dessus des terres. Il n'accélérait à Mach 2 qu'une fois au-dessus de l'océan."),
    dict(type='outro', num=None, title="ABONNE-TOI", lines=("LE MUR DU SON ?", "UN EMBOUTEILLAGE D'ONDES"),
         say="Le mur du son, c'est un embouteillage d'ondes. Abonne-toi pour la suite de la science du vol.",
         show="Le mur du son, c'est un embouteillage d'ondes. Abonne-toi pour la suite de la science du vol."),
]
END_HOLD = 2.5
