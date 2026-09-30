# Tournoi « Quel avion gagne ? » — say = prononcé, show = affiché
PLANES = {
    'concorde': 'Concorde', 'sr71': 'SR-71 Blackbird', 'f22': 'F-22 Raptor', 'm2000': 'Mirage 2000',
    'a10': 'A-10 Thunderbolt II', 'spitfire': 'Spitfire', 'an225': 'An-225 Mriya', 'b2': 'B-2 Spirit',
}
SHORT = {'concorde': 'CONCORDE', 'sr71': 'SR-71', 'f22': 'F-22', 'm2000': 'MIRAGE 2000', 'a10': 'A-10',
         'spitfire': 'SPITFIRE', 'an225': 'AN-225', 'b2': 'B-2'}
BRACKET = ['concorde', 'sr71', 'f22', 'm2000', 'a10', 'spitfire', 'an225', 'b2']

INTRO = "Huit avions légendaires. Un seul champion. À chaque duel, devine qui passe. C'est parti !"
INTRO_SHOW = "8 AVIONS. 1 SEUL CHAMPION."
SEMIS = "Demi-finales !"
FINAL_INTRO = "La grande finale ! Le èss ère soixante et onze contre l'Antonov. En trois manches."
OUTRO = "Tu avais parié sur qui ? Dis-le en commentaire, et abonne-toi pour le prochain tournoi !"

# val = valeur numérique pour la jauge, lab = texte affiché
DUELS = [
    dict(rnd='QUART DE FINALE 1', a='concorde', b='sr71', crit='QUI VOLE LE PLUS HAUT ?',
         va=18300, vb=25900, la='18 300 m', lb='25 900 m', win='b',
         q="Premier duel : le Concorde contre le èss ère soixante et onze. Qui vole le plus haut ?",
         r="Le èss ère soixante et onze ! Vingt-cinq mille neuf cents mètres, contre dix-huit mille pour le Concorde."),
    dict(rnd='QUART DE FINALE 2', a='f22', b='m2000', crit='QUI EST LE PLUS LÉGER ?', lower=True,
         va=19700, vb=7500, la='19,7 t à vide', lb='7,5 t à vide', win='b',
         q="Le F vingt-deux Raptor contre le Mirage deux mille. Qui est le plus léger ?",
         r="Surprise, le Mirage ! Sept tonnes et demie à vide. Le Raptor en pèse presque vingt."),
    dict(rnd='QUART DE FINALE 3', a='a10', b='spitfire', crit='QUI A LE PLUS GROS CANON ?',
         va=30, vb=20, la='30 mm', lb='20 mm', win='a',
         q="Le A dix contre le Spitfaïeur. Qui a le plus gros canon ?",
         r="Le A dix, et de loin ! Trente millimètres, contre vingt pour le Spitfaïeur."),
    dict(rnd='QUART DE FINALE 4', a='an225', b='b2', crit='LA PLUS GRANDE ENVERGURE ?',
         va=88.4, vb=52.4, la='88,4 m', lb='52,4 m', win='a',
         q="L'Antonov deux cent vingt-cinq contre le bé deux Spirite. Qui a la plus grande envergure ?",
         r="L'Antonov ! Quatre-vingt-huit mètres. Le bé deux : cinquante-deux."),
    dict(rnd='DEMI-FINALE 1', a='sr71', b='m2000', crit='QUI EST LE PLUS RAPIDE ?',
         va=3.3, vb=2.2, la='Mach 3,3', lb='Mach 2,2', win='a',
         q="Le èss ère soixante et onze contre le Mirage deux mille. Qui est le plus rapide ?",
         r="Le Blakbeurde, Mach trois virgule trois ! Le Mirage plafonne à Mach deux virgule deux."),
    dict(rnd='DEMI-FINALE 2', a='a10', b='an225', crit='LE PLUS LOURD AU DÉCOLLAGE ?',
         va=23, vb=640, la='23 t', lb='640 t', win='b',
         q="Le A dix contre l'Antonov. Qui est le plus lourd au décollage ?",
         r="L'Antonov, six cent quarante tonnes ! Presque trente fois plus que le A dix."),
]
FINAL = [
    dict(rnd='FINALE · MANCHE 1', a='sr71', b='an225', crit='MASSE AU DÉCOLLAGE',
         va=78, vb=640, la='78 t', lb='640 t', win='b',
         q="Manche un : la masse au décollage.",
         r="Six cent quarante tonnes contre soixante-dix-huit. Un zéro pour l'Antonov !"),
    dict(rnd='FINALE · MANCHE 2', a='sr71', b='an225', crit='VITESSE MAX',
         va=3530, vb=850, la='3 530 km/h', lb='850 km/h', win='a',
         q="Manche deux : la vitesse.",
         r="Trois mille cinq cents kilomètres heure contre huit cent cinquante. Un partout !"),
    dict(rnd='FINALE · MANCHE 3', a='sr71', b='an225', crit='ALTITUDE MAX',
         va=25900, vb=11000, la='25 900 m', lb='11 000 m', win='a',
         q="Dernière manche : l'altitude. Tout se joue ici.",
         r="Vingt-cinq mille neuf cents mètres contre onze mille. Le èss ère soixante et onze est champion !"),
]
