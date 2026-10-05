# Duel : Spitfire vs Bf 109 (sources : battleofbritain1940.com Bf 109E [560 km/h, 2 MG FF 20 mm sur E-3, rayon de virage plus large, injection = piqué en G négatif] ;
# Wikipedia Spitfire variants [Mk I 362 mph = 582 km/h, 8 Browning .303] ; production ~34 000 Bf 109 / 20 351 Spitfire ; Seelöwe reporté sept. 1940)
import math
A = dict(name="SPITFIRE", short="SPITFIRE", color=(0.25, 0.55, 1.0), hi=["SPITFIRE"])
B = dict(name="BF 109", short="BF 109", color=(1.0, 0.25, 0.22), hi=["BF 109", "MESSERSCHMITT"])
FLIP = {"a_34": True, "a_side": True, "b_side": True}
TOPROT = {"a_top": math.pi, "b_top": math.pi}
SCENES = [
    dict(type='hook', score=(0, 0), kicker="BATAILLE D'ANGLETERRE · 1940",
         say="Spitfire contre Messerschmitt cent neuf. Été mille neuf cent quarante, le ciel anglais. Cinq rounds, un seul vainqueur.",
         show="Spitfire contre Messerschmitt Bf 109. Été 1940, le ciel anglais. 5 rounds, un seul vainqueur."),
    dict(type='bars', score=(1, 0), round="ROUND 1", title="LA VITESSE", a=582, b=560, max=650, fmt="{:.0f} KM/H", a_first=True,
         pill="SPITFIRE MK I VS BF 109 E, EN 1940",
         say="Round un : la vitesse. Le Spitfire atteint cinq cent quatre-vingt-deux kilomètres heure. Le cent neuf, cinq cent soixante. Point Spitfire, de justesse.",
         show="Round 1 : la vitesse. Le Spitfire atteint 582 km/h. Le Bf 109, 560. Point Spitfire, de justesse."),
    dict(type='counters', score=(1, 1), round="ROUND 2", title="LA PRODUCTION", a_num=20351, b_num=34000, pre="",
         a_sub="SPITFIRE CONSTRUITS", b_sub="BF 109 CONSTRUITS", pill="LE CHASSEUR LE PLUS PRODUIT DE L'HISTOIRE",
         say="Round deux : la production. Plus de vingt mille Spitfire. Mais près de trente-quatre mille Messerschmitt : le chasseur le plus produit de l'histoire. Point cent neuf.",
         show="Round 2 : la production. Plus de 20 000 Spitfire. Mais près de 34 000 Messerschmitt : le chasseur le plus produit de l'histoire. Point Bf 109."),
    dict(type='list', score=(1, 2), round="ROUND 3", title="LA PUISSANCE DE FEU",
         a_items=["8 MITRAILLEUSES", "CALIBRE 7,7 MM"], b_items=["2 CANONS 20 MM", "2 MITRAILLEUSES"],
         say="Round trois : la puissance de feu. Le Spitfire aligne huit mitrailleuses légères. Le cent neuf a deux canons de vingt millimètres. Un seul obus peut suffire. Point cent neuf.",
         show="Round 3 : la puissance de feu. Le Spitfire aligne 8 mitrailleuses légères. Le Bf 109 a 2 canons de 20 mm. Un seul obus peut suffire. Point Bf 109."),
    dict(type='chips', score=(2, 2), round="ROUND 4", title="LE COMBAT TOURNOYANT", side='A',
         chips=["VIRAGE PLUS SERRÉ", "AILE ELLIPTIQUE", "TRÈS MANIABLE"], other="PIQUE PLUS FORT",
         say="Round quatre : le combat tournoyant. Le Messerschmitt pique mieux, grâce à son moteur à injection. Mais en virage, le Spitfire tourne plus serré et finit dans sa queue. Point Spitfire.",
         show="Round 4 : le combat tournoyant. Le Messerschmitt pique mieux, grâce à son moteur à injection. Mais en virage, le Spitfire tourne plus serré et finit dans sa queue. Point Spitfire."),
    dict(type='chips', score=(3, 2), round="ROUND 5", title="LA BATAILLE", side='A',
         chips=["CIEL ANGLAIS DÉFENDU", "INVASION REPORTÉE"], other="SUPÉRIORITÉ AÉRIENNE RATÉE", other_grey=True,
         say="Round cinq : la bataille d'Angleterre. La Luftwaffe n'obtient jamais la maîtrise du ciel, et Hitler reporte l'invasion. Avec l'Hurricane, le Spitfire a gagné. Point Spitfire.",
         show="Round 5 : la bataille d'Angleterre. La Luftwaffe n'obtient jamais la maîtrise du ciel, et Hitler reporte l'invasion. Avec le Hurricane, le Spitfire a gagné. Point Spitfire."),
    dict(type='verdict', score=(3, 2), lines=[("A GAGNÉ LA BATAILLE", 'A'), ("PLUS PRODUIT, MIEUX ARMÉ", 'B')],
         say="Verdict : trois à deux pour le Spitfire. Le cent neuf était plus nombreux et mieux armé, mais le Spitfire a gagné la bataille qui comptait. Et toi, tu mets qui ?",
         show="Verdict : 3 à 2 pour le Spitfire. Le Bf 109 était plus nombreux et mieux armé, mais le Spitfire a gagné la bataille qui comptait. Et toi, tu mets qui ?"),
]
END_HOLD = 6.3
