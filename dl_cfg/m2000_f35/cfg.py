# Duel : Mirage 2000 vs F-35. Sources : migflug.com/aircraft/mirage-2000 [Mach 2,2 ; 7 500 kg à vide ; 601 construits ; radar RDY Doppler à balayage mécanique] ;
# airandspaceforces.com/weapons-platforms/f-35 [F-35A Mach 1,6 avec armement interne ; 1er vol 15/12/2006] ; F-35A ≈ 13,2 t à vide ; radar APG-81 à antenne active, capteurs DAS à 360°, fusion de données ;
# plus de 1 000 F-35 livrés (millième en 2024)
import math
A = dict(name="MIRAGE 2000", short="MIRAGE", color=(0.20, 0.50, 1.0), hi=["MIRAGE"])
B = dict(name="F-35", short="F-35", color=(1.0, 0.25, 0.22), hi=["F-35", "LIGHTNING"])
FLIP = {"a_34": True, "a_side": True, "b_side": True}
TOPROT = {"a_top": math.pi, "b_top": math.pi}
SCENES = [
    dict(type='hook', score=(0, 0), kicker="LE MIRAGE 2000 PEUT-IL BATTRE LE F-35 ?",
         say="Le Mirage deux mille peut-il battre le F trente-cinq, le chasseur furtif américain ? La légende française contre le programme militaire le plus cher de l'histoire. Cinq rounds, un seul vainqueur.",
         show="Le Mirage 2000 peut-il battre le F-35, le chasseur furtif américain ? La légende française contre le programme militaire le plus cher de l'histoire. 5 rounds, un seul vainqueur."),
    dict(type='chips', score=(0, 1), round="ROUND 1", title="LA FURTIVITÉ", side='B',
         chips=["QUASI INVISIBLE AU RADAR", "ARMES EN SOUTE"], other="PAS FURTIF", other_grey=True,
         say="Round un : la furtivité. Le F trente-cinq est presque invisible au radar, avec ses armes cachées dans la soute. Le Mirage, lui, n'a pas été conçu pour ça. Point F trente-cinq.",
         show="Round 1 : la furtivité. Le F-35 est presque invisible au radar, avec ses armes cachées dans la soute. Le Mirage, lui, n'a pas été conçu pour ça. Point F-35."),
    dict(type='bars', score=(1, 1), round="ROUND 2", title="LA VITESSE", a=2.2, b=1.6, max=2.6, fmt="MACH {:.1f}",
         say="Round deux : la vitesse. Le Mirage atteint Mach deux virgule deux. Le F trente-cinq, Mach un virgule six. Le vieux Français est bien plus rapide. Point Mirage.",
         show="Round 2 : la vitesse. Le Mirage atteint Mach 2,2. Le F-35, Mach 1,6. Le vieux Français est bien plus rapide. Point Mirage."),
    dict(type='chips', score=(1, 2), round="ROUND 3", title="LES CAPTEURS", side='B',
         chips=["RADAR À ANTENNE ACTIVE", "CAMÉRAS À 360°", "FUSION DE DONNÉES"], other="RADAR À BALAYAGE MÉCANIQUE", other_grey=True,
         say="Round trois : les capteurs. Radar à antenne active, caméras qui voient tout autour de l'avion, et un ordinateur qui fusionne tout. Le Mirage a un radar à antenne mécanique. Point F trente-cinq.",
         show="Round 3 : les capteurs. Radar à antenne active, caméras qui voient tout autour de l'avion, et un ordinateur qui fusionne tout. Le Mirage a un radar à antenne mécanique. Point F-35."),
    dict(type='bars', score=(2, 2), round="ROUND 4", title="LE POIDS", a=7.5, b=13.2, max=15, fmt="{:.1f} T", low_wins=True, race=False, a_first=True,
         say="Round quatre : le poids. À vide, le Mirage pèse sept tonnes et demie. Le F trente-cinq, plus de treize. Plus léger, plus nerveux. Point Mirage. Deux partout.",
         show="Round 4 : le poids. À vide, le Mirage pèse 7,5 tonnes. Le F-35, plus de 13. Plus léger, plus nerveux. Point Mirage. 2 partout."),
    dict(type='counters', score=(2, 3), round="ROUND 5", title="LA PRODUCTION", a_num=601, b_num=1000, a_sub="CONSTRUITS", b_sub="ET PLUS, ET ÇA CONTINUE", pre="", static=True, pill="LE F-35 EST ENCORE EN PRODUCTION",
         say="Dernier round, décisif : la production. Six cent un Mirage deux mille construits. Le F trente-cinq a déjà dépassé les mille exemplaires, et les chaînes tournent encore. Point F trente-cinq.",
         show="Dernier round, décisif : la production. 601 Mirage 2000 construits. Le F-35 a déjà dépassé les 1 000 exemplaires, et les chaînes tournent encore. Point F-35."),
    dict(type='verdict', score=(2, 3), lines=[("VITESSE, LÉGÈRETÉ", 'A'), ("FURTIVITÉ, CAPTEURS, PRODUCTION", 'B')],
         say="Verdict : trois à deux pour le F trente-cinq. Logique, il a près de trente ans de moins. Mais en vitesse pure et en légèreté, le vieux Mirage le bat encore. Et toi, tu mets qui ?",
         show="Verdict : 3 à 2 pour le F-35. Logique, il a près de 30 ans de moins. Mais en vitesse pure et en légèreté, le vieux Mirage le bat encore. Et toi, tu mets qui ?"),
]
END_HOLD = 10.0
