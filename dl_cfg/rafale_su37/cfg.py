# Duel : Rafale vs Su-35 (modèle 3D : Su-37 / Su-27M à plans canard, famille « Flanker »). Sources : migflug.com/aircraft/su-35-flanker-e [Su-35S : Mach 2,25 ; ~19 t à vide ;
# radar Irbis-E PESA (pas AESA) ; tuyères orientables AL-41F1S ; seul client export confirmé : la Chine, 24 avions 2016-2018] ; migflug.com/aircraft/rafale [Mach 1,8 ; ~10,3 t à vide ;
# 8 clients export : Égypte, Qatar, Inde, Grèce, Croatie, Indonésie, Émirats, Serbie] ; radar RBE2 à antenne active (AESA) en service depuis 2013
import math
A = dict(name="RAFALE", short="RAFALE", color=(0.20, 0.50, 1.0), hi=["RAFALE"])
B = dict(name="SU-35", short="SU-35", color=(1.0, 0.25, 0.22), hi=["SU-35", "FLANKER"])
FLIP = {}
TOPROT = {"a_top": -math.pi / 2, "b_top": math.pi}
SCENES = [
    dict(type='hook', score=(0, 0), kicker="LE RAFALE PEUT-IL BATTRE LE FLANKER ?",
         say="Le Rafale peut-il battre le Soukhoï trente-cinq, le chasseur vedette de la Russie ? La France contre la Russie. Cinq rounds, un seul vainqueur.",
         show="Le Rafale peut-il battre le Soukhoï 35, le chasseur vedette de la Russie ? La France contre la Russie. 5 rounds, un seul vainqueur."),
    dict(type='bars', score=(0, 1), round="ROUND 1", title="LA VITESSE", a=1.8, b=2.25, max=2.6, fmt="MACH {:.2f}",
         say="Round un : la vitesse. Le Rafale atteint Mach un virgule huit. Le Soukhoï, Mach deux virgule vingt-cinq. Point Soukhoï.",
         show="Round 1 : la vitesse. Le Rafale atteint Mach 1,8. Le Soukhoï, Mach 2,25. Point Soukhoï."),
    dict(type='chips', score=(0, 2), round="ROUND 2", title="LA VOLTIGE", side='B',
         chips=["TUYÈRES ORIENTABLES", "POUSSÉE VECTORIELLE", "FIGURES IMPOSSIBLES"], other="PAS DE POUSSÉE VECTORIELLE", other_grey=True,
         say="Round deux : la voltige. Les tuyères du Soukhoï s'orientent, et lui permettent des figures que presque aucun autre chasseur ne peut faire. Point Soukhoï.",
         show="Round 2 : la voltige. Les tuyères du Soukhoï s'orientent, et lui permettent des figures que presque aucun autre chasseur ne peut faire. Point Soukhoï."),
    dict(type='chips', score=(1, 2), round="ROUND 3", title="LE RADAR", side='A',
         chips=["RBE2 À ANTENNE ACTIVE", "EN SERVICE DEPUIS 2013"], other="ANTENNE PASSIVE", other_grey=True,
         say="Round trois : le radar. Le Rafale vole avec un radar à antenne active, la technologie la plus moderne. Celui du Soukhoï est encore à antenne passive. Point Rafale.",
         show="Round 3 : le radar. Le Rafale vole avec un radar à antenne active, la technologie la plus moderne. Celui du Soukhoï est encore à antenne passive. Point Rafale."),
    dict(type='bars', score=(2, 2), round="ROUND 4", title="LA TAILLE", a=10.3, b=19.0, max=21, fmt="{:.1f} T", low_wins=True, race=False, a_first=True,
         say="Round quatre : la taille. À vide, le Rafale pèse environ dix tonnes. Le Soukhoï, dix-neuf. Plus petit, le Rafale est bien plus difficile à repérer. Deux partout.",
         show="Round 4 : la taille. À vide, le Rafale pèse environ 10 tonnes. Le Soukhoï, 19. Plus petit, le Rafale est bien plus difficile à repérer. 2 partout."),
    dict(type='list', score=(3, 2), round="ROUND 5", title="L'EXPORT",
         a_items=["8 PAYS CLIENTS", "INDE, ÉMIRATS, GRÈCE…"], b_items=["1 CLIENT CONFIRMÉ", "LA CHINE"],
         say="Dernier round, décisif : l'export. Le Rafale a convaincu huit pays, de l'Inde aux Émirats. Le Soukhoï trente-cinq n'a qu'un seul client étranger confirmé : la Chine. Point Rafale.",
         show="Dernier round, décisif : l'export. Le Rafale a convaincu 8 pays, de l'Inde aux Émirats. Le Soukhoï 35 n'a qu'un seul client étranger confirmé : la Chine. Point Rafale."),
    dict(type='verdict', score=(3, 2), lines=[("RADAR, DISCRÉTION, EXPORT", 'A'), ("VITESSE, VOLTIGE", 'B')],
         say="Verdict : trois à deux pour le Rafale. Plus moderne, plus discret, et choisi par huit pays. Mais en vitesse et en voltige pure, le Soukhoï reste un monstre. Et toi, tu mets qui ?",
         show="Verdict : 3 à 2 pour le Rafale. Plus moderne, plus discret, et choisi par huit pays. Mais en vitesse et en voltige pure, le Soukhoï reste un monstre. Et toi, tu mets qui ?"),
]
END_HOLD = 10.0
