# Duel : Rafale vs F-15 (sources : migflug.com/aircraft/rafale [Mach 1,8 ; ~10,3 t à vide (C) ; Rafale M sur le Charles-de-Gaulle ; en service 2001 Marine] ;
# Wikipedia F-15 Eagle [mise en service 1976 ; Mach 2,5+ ; ~12,7 t à vide (F-15C) ; premier vol 1972 ; 104 victoires aériennes sans perte en combat aérien])
import math
A = dict(name="RAFALE", short="RAFALE", color=(0.20, 0.50, 1.0), hi=["RAFALE"])
B = dict(name="F-15", short="F-15", color=(1.0, 0.25, 0.22), hi=["F-15", "EAGLE"])
FLIP = {"b_side": True}
TOPROT = {"a_top": -math.pi / 2, "b_top": math.pi}
SCENES = [
    dict(type='hook', score=(0, 0), kicker="LE RAFALE PEUT-IL BATTRE L'AIGLE ?",
         say="Le Rafale peut-il battre le F quinze, l'aigle invaincu ? La France contre l'Amérique. Cinq rounds, un seul vainqueur.",
         show="Le Rafale peut-il battre le F-15, l'aigle invaincu ? La France contre l'Amérique. 5 rounds, un seul vainqueur."),
    dict(type='bars', score=(0, 1), round="ROUND 1", title="LA VITESSE", a=1.8, b=2.5, max=2.8, fmt="MACH {:.1f}",
         say="Round un : la vitesse. Le Rafale atteint Mach un virgule huit. Le F quinze dépasse Mach deux virgule cinq. Point F quinze.",
         show="Round 1 : la vitesse. Le Rafale atteint Mach 1,8. Le F-15 dépasse Mach 2,5. Point F-15."),
    dict(type='chips', score=(1, 1), round="ROUND 2", title="LE PORTE-AVIONS", side='A',
         chips=["RAFALE MARINE", "CATAPULTE", "CHARLES-DE-GAULLE"], other="IMPOSSIBLE", other_grey=True,
         say="Round deux : le porte-avions. Le Rafale Marine décolle au catapultage du Charles de Gaulle. Le F quinze, lui, n'a jamais été conçu pour se poser sur un navire. Point Rafale.",
         show="Round 2 : le porte-avions. Le Rafale Marine décolle au catapultage du Charles-de-Gaulle. Le F-15, lui, n'a jamais été conçu pour se poser sur un navire. Point Rafale."),
    dict(type='chips', score=(1, 2), round="ROUND 3", title="LE PALMARÈS", side='B',
         chips=["104 VICTOIRES", "JAMAIS ABATTU EN DUEL"], other="SURTOUT AIR-SOL", other_grey=True,
         say="Round trois : le palmarès. Le F quinze compte plus de cent victoires en combat aérien, sans jamais avoir été abattu par un autre avion. Point F quinze.",
         show="Round 3 : le palmarès. Le F-15 compte plus de 100 victoires en combat aérien, sans jamais avoir été abattu par un autre avion. Point F-15."),
    dict(type='bars', score=(2, 2), round="ROUND 4", title="LA LÉGÈRETÉ", a=10.3, b=12.7, max=14, fmt="{:.1f} T", low_wins=True, race=False, a_first=True,
         say="Round quatre : la légèreté. À vide, le Rafale pèse environ dix tonnes. Le F quinze, presque treize. Avec ses plans canard, le Rafale est plus vif en virage. Deux partout.",
         show="Round 4 : la légèreté. À vide, le Rafale pèse environ 10 tonnes. Le F-15, presque 13. Avec ses plans canard, le Rafale est plus vif en virage. 2 partout."),
    dict(type='list', score=(3, 2), round="ROUND 5", title="LA JEUNESSE",
         a_items=["EN SERVICE EN 2001", "25 ANS PLUS TARD"], b_items=["EN SERVICE EN 1976", "PREMIER VOL EN 1972"],
         say="Dernier round, décisif : la jeunesse. Le F quinze est entré en service en mille neuf cent soixante-seize. Le Rafale, en deux mille un, vingt-cinq ans plus tard, avec une électronique pensée pour le vingt-et-unième siècle. Point Rafale.",
         show="Dernier round, décisif : la jeunesse. Le F-15 est entré en service en 1976. Le Rafale, en 2001, 25 ans plus tard, avec une électronique pensée pour le 21e siècle. Point Rafale."),
    dict(type='verdict', score=(3, 2), lines=[("PORTE-AVIONS, AGILE, MODERNE", 'A'), ("VITESSE, PALMARÈS", 'B')],
         say="Verdict : trois à deux pour le Rafale. Plus jeune, plus agile, et capable d'opérer depuis un porte-avions. Mais l'aigle reste plus rapide, et invaincu en combat aérien. Et toi, tu mets qui ?",
         show="Verdict : 3 à 2 pour le Rafale. Plus jeune, plus agile, et capable d'opérer depuis un porte-avions. Mais l'aigle reste plus rapide, et invaincu en combat aérien. Et toi, tu mets qui ?"),
]
END_HOLD = 9.0
