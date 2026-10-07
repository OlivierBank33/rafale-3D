# Duel : Rafale vs F-35 (sources : Dassault/AAE Rafale Mach 1,8 ; F-35 Mach 1,6 ; furtivité F-35 ; coût/heure de vol Rafale ~16-20 k$
# (AAE ~20 k$) vs F-35A ~42 k$ (DoD) — warwingsdaily.com 08/2025 ; 1 000e F-35 en 2024 ; Rafale « quelques centaines » livrés ;
# indépendance : Rafale 100 % français (moteur Safran, électronique Thales), F-35 dépend des USA pour logiciels et maintenance)
import math
A = dict(name="RAFALE", short="RAFALE", color=(0.20, 0.50, 1.0), hi=["RAFALE"])
B = dict(name="F-35", short="F-35", color=(1.0, 0.25, 0.22), hi=["F-35", "LIGHTNING"])
FLIP = {"b_side": True}
TOPROT = {"a_top": -math.pi / 2, "b_top": math.pi}
SCENES = [
    dict(type='hook', score=(0, 0), kicker="FRANCE CONTRE USA",
         say="Le Rafale peut-il battre le F trente-cinq ? La France contre l'Amérique. Cinq rounds, un seul vainqueur.",
         show="Le Rafale peut-il battre le F-35 ? La France contre l'Amérique. 5 rounds, un seul vainqueur."),
    dict(type='bars', score=(1, 0), round="ROUND 1", title="LA VITESSE", a=1.8, b=1.6, max=2.2, fmt="MACH {:.1f}", a_first=True,
         say="Round un : la vitesse. Le Rafale monte à Mach un virgule huit. Le F trente-cinq, Mach un virgule six. Point Rafale.",
         show="Round 1 : la vitesse. Le Rafale monte à Mach 1,8. Le F-35, Mach 1,6. Point Rafale."),
    dict(type='chips', score=(1, 1), round="ROUND 2", title="LA FURTIVITÉ", side='B',
         chips=["QUASI INVISIBLE AU RADAR", "ARMES EN SOUTE", "CONÇU FURTIF"], other="DISCRET, PAS FURTIF", other_grey=True,
         say="Round deux : la furtivité. Le F trente-cinq a été dessiné pour être presque invisible au radar, avec ses armes cachées en soute. Le Rafale est discret, mais pas furtif. Point F trente-cinq.",
         show="Round 2 : la furtivité. Le F-35 a été dessiné pour être presque invisible au radar, avec ses armes cachées en soute. Le Rafale est discret, mais pas furtif. Point F-35."),
    dict(type='chips', score=(2, 1), round="ROUND 3", title="L'INDÉPENDANCE", side='A',
         chips=["MOTEUR FRANÇAIS", "ÉLECTRONIQUE FRANÇAISE", "MISES À JOUR LIBRES"], other="DÉPEND DES USA", other_grey=True,
         say="Round trois : l'indépendance. Le Rafale est cent pour cent français. Le F trente-cinq dépend des États-Unis pour ses logiciels et sa maintenance. Point Rafale.",
         show="Round 3 : l'indépendance. Le Rafale est 100 % français. Le F-35 dépend des États-Unis pour ses logiciels et sa maintenance. Point Rafale."),
    dict(type='counters', score=(2, 2), round="ROUND 4", title="LA PRODUCTION", a_num=300, b_num=1000, pre="",
         a_sub="RAFALE LIVRÉS · ENVIRON", b_sub="F-35 LIVRÉS · PLUS DE", pill="LE F-35 EST CHOISI PAR PRÈS DE 20 PAYS",
         say="Round quatre : la production. Plus de mille F trente-cinq livrés, choisis par près de vingt pays. Le Rafale, quelques centaines. Deux partout.",
         show="Round 4 : la production. Plus de 1 000 F-35 livrés, choisis par près de 20 pays. Le Rafale, quelques centaines. 2 partout."),
    dict(type='bars', score=(3, 2), round="ROUND 5", title="L'HEURE DE VOL", a=20, b=42, max=50, fmt="{:.0f} 000 $", race=False, low_wins=True,
         pill="COÛT ESTIMÉ D'UNE HEURE DE VOL",
         say="Dernier round : le prix d'une heure de vol. Environ vingt mille dollars pour le Rafale. Plus de quarante mille pour le F trente-cinq. Deux fois moins cher : point Rafale.",
         show="Dernier round : le prix d'une heure de vol. Environ 20 000 $ pour le Rafale. Plus de 40 000 $ pour le F-35. Deux fois moins cher : point Rafale."),
    dict(type='verdict', score=(3, 2), lines=[("PLUS LIBRE, MOINS CHER", 'A'), ("PLUS FURTIF, PARTOUT", 'B')],
         say="Verdict : trois à deux pour le Rafale. Le F trente-cinq est plus furtif et partout dans le monde. Le Rafale est plus rapide, plus libre et deux fois moins cher à faire voler. Et toi, tu mets qui ?",
         show="Verdict : 3 à 2 pour le Rafale. Le F-35 est plus furtif et partout dans le monde. Le Rafale est plus rapide, plus libre et deux fois moins cher à faire voler. Et toi, tu mets qui ?"),
]
END_HOLD = 8.2
