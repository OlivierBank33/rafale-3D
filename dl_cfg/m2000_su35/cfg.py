# Duel : Mirage 2000 vs Su-35 (modèle 3D : Su-37 / Su-27M, famille « Flanker »). Sources : migflug.com/aircraft/mirage-2000 [Mach 2,2 ; 7 500 kg à vide ; 601 exemplaires 1978-2007 ;
# 1er vol 10/03/1978 ; utilisateurs export : Inde, Émirats, Taïwan, Grèce, Égypte, Pérou, Ukraine, anciens : Qatar, Brésil] ; migflug.com/aircraft/su-35-flanker-e [Su-35S : Mach 2,25 ; ~19 t à vide ;
# tuyères orientables ; 1er vol du Su-35S en 2008 ; seul client export confirmé : la Chine]
import math
A = dict(name="MIRAGE 2000", short="MIRAGE", color=(0.20, 0.50, 1.0), hi=["MIRAGE"])
B = dict(name="SU-35", short="SU-35", color=(1.0, 0.25, 0.22), hi=["SU-35", "FLANKER"])
FLIP = {"a_34": True, "a_side": True}
TOPROT = {"a_top": math.pi, "b_top": math.pi}
SCENES = [
    dict(type='hook', score=(0, 0), kicker="LE MIRAGE 2000 PEUT-IL BATTRE LE SU-35 ?",
         say="Le Mirage deux mille peut-il battre le Soukhoï trente-cinq ? Le petit delta français contre le Flanker russe, trente ans plus jeune. Cinq rounds, un seul vainqueur.",
         show="Le Mirage 2000 peut-il battre le Soukhoï 35 ? Le petit delta français contre le Flanker russe, 30 ans plus jeune. 5 rounds, un seul vainqueur."),
    dict(type='bars', score=(0, 1), round="ROUND 1", title="LA VITESSE", a=2.2, b=2.25, max=2.6, fmt="MACH {:.2f}",
         say="Round un : la vitesse. Le Mirage atteint Mach deux virgule deux. Le Soukhoï, Mach deux virgule vingt-cinq. À peine cinquante kilomètres-heure d'écart. Point Soukhoï, de justesse.",
         show="Round 1 : la vitesse. Le Mirage atteint Mach 2,2. Le Soukhoï, Mach 2,25. À peine 50 km/h d'écart. Point Soukhoï, de justesse."),
    dict(type='chips', score=(0, 2), round="ROUND 2", title="LA VOLTIGE", side='B',
         chips=["TUYÈRES ORIENTABLES", "POUSSÉE VECTORIELLE", "FIGURES IMPOSSIBLES"], other="PAS DE POUSSÉE VECTORIELLE", other_grey=True,
         say="Round deux : la voltige. Les tuyères du Soukhoï s'orientent. Il peut presque s'arrêter en l'air et pivoter sur lui-même. Point Soukhoï.",
         show="Round 2 : la voltige. Les tuyères du Soukhoï s'orientent. Il peut presque s'arrêter en l'air et pivoter sur lui-même. Point Soukhoï."),
    dict(type='bars', score=(1, 2), round="ROUND 3", title="LE POIDS", a=7.5, b=19.0, max=21, fmt="{:.1f} T", low_wins=True, race=False, a_first=True,
         say="Round trois : le poids. À vide, le Mirage pèse sept tonnes et demie. Le Soukhoï, dix-neuf. Deux fois et demie plus léger, et bien plus dur à repérer. Point Mirage.",
         show="Round 3 : le poids. À vide, le Mirage pèse 7,5 tonnes. Le Soukhoï, 19. 2,5 fois plus léger, et bien plus dur à repérer. Point Mirage."),
    dict(type='list', score=(2, 2), round="ROUND 4", title="L'EXPORT",
         a_items=["601 CONSTRUITS", "INDE, GRÈCE, ÉGYPTE…"], b_items=["1 CLIENT CONFIRMÉ", "LA CHINE"],
         say="Round quatre : l'export. Six cent un Mirage deux mille construits, vendus de l'Inde à la Grèce, en passant par l'Égypte et le Pérou. Le Soukhoï trente-cinq n'a qu'un client étranger confirmé : la Chine. Deux partout.",
         show="Round 4 : l'export. 601 Mirage 2000 construits, vendus de l'Inde à la Grèce, en passant par l'Égypte et le Pérou. Le Soukhoï 35 n'a qu'un client étranger confirmé : la Chine. 2 partout."),
    dict(type='counters', score=(2, 3), round="ROUND 5", title="L'ÂGE", a_num=1978, b_num=2008, a_sub="PREMIER VOL", b_sub="PREMIER VOL (SU-35S)", pre="", static=True, pill="30 ANS D'ÉCART",
         say="Dernier round, décisif : l'âge. Le Mirage deux mille a volé pour la première fois en mille neuf cent soixante-dix-huit. Le Soukhoï trente-cinq moderne, en deux mille huit. Trente ans d'écart. Point Soukhoï.",
         show="Dernier round, décisif : l'âge. Le Mirage 2000 a volé pour la première fois en 1978. Le Soukhoï 35 moderne, en 2008. 30 ans d'écart. Point Soukhoï."),
    dict(type='verdict', score=(2, 3), lines=[("LÉGÈRETÉ, EXPORT", 'A'), ("VITESSE, VOLTIGE, MODERNITÉ", 'B')],
         say="Verdict : trois à deux pour le Soukhoï. Logique, il a trente ans de moins. Mais le petit Mirage, deux fois et demie plus léger et vendu dans le monde entier, lui tient tête jusqu'au dernier round. Et toi, tu mets qui ?",
         show="Verdict : 3 à 2 pour le Soukhoï. Logique, il a 30 ans de moins. Mais le petit Mirage, 2,5 fois plus léger et vendu dans le monde entier, lui tient tête jusqu'au dernier round. Et toi, tu mets qui ?"),
]
END_HOLD = 10.0
