# QU'AURAIS-TU FAIT ? : le planeur de Gimli. Source : Wikipedia « Gimli Glider » [23/07/1983, Boeing 767-233 Air Canada, 69 à bord ; jauges en panne + confusion livres/kg -> moins de la moitié
# du carburant ; ennuis à 41 000 ft (~12 500 m), 2 moteurs arrêtés ; dérouté vers Winnipeg, puis Gimli (ancienne base RCAF, piste désaffectée, course automobile en cours, familles) ;
# glissade (forward slip) pour perdre l'altitude ; train avant non verrouillé qui s'effondre, nez qui frotte ; 0 mort, 0 blessé grave, ~10 blessés légers à l'évacuation]
# Le copilote Maurice Quintal, ancien de la RCAF, connaissait Gimli. Commandant : Robert Pearson, planeuriste.
SERIES = "QU'AURAIS-TU FAIT ?"; EP = "02"; MODE = "histoire"
SCENES = [
    dict(type='g_hook', title="QU'AURAIS-TU FAIT ?",
         say="Mille neuf cent quatre-vingt-trois, Canada. Ton Boeing sept six sept tout neuf vole à douze mille mètres. Une alarme carburant sonne. Puis un moteur s'arrête. Puis le second.",
         show="1983, Canada. Ton Boeing 767 tout neuf vole à 12 000 mètres. Une alarme carburant sonne. Puis un moteur s'arrête. Puis le second."),
    dict(type='g_fuel', title="LIVRES OU KILOS ?",
         say="La raison : au moment du plein, on a confondu livres et kilogrammes. L'avion a décollé avec moins de la moitié du carburant nécessaire. Ton avion de ligne est devenu un planeur.",
         show="La raison : au moment du plein, on a confondu livres et kilogrammes. L'avion a décollé avec moins de la moitié du carburant nécessaire. Ton avion de ligne est devenu un planeur."),
    dict(type='g_map', title="TROP LOIN",
         say="Winnipeg est trop loin. Mais ton copilote connaît une ancienne base militaire : Gimli. Problème : la piste est désaffectée, et ce jour-là, il y a une course automobile, avec des familles.",
         show="Winnipeg est trop loin. Mais ton copilote connaît une ancienne base militaire : Gimli. Problème : la piste est désaffectée, et ce jour-là, il y a une course automobile, avec des familles."),
    dict(type='g_options', title="TROIS CHOIX",
         say="Trois options. A : tenter Winnipeg quand même. B : te poser à Gimli, au milieu de la course. C : te poser dans un champ.",
         show="3 options. A : tenter Winnipeg quand même. B : te poser à Gimli, au milieu de la course. C : te poser dans un champ."),
    dict(type='g_pause', title="TU FAIS QUOI ?",
         say="Tu as trois secondes. A, B ou C ? Trois. Deux. Un.",
         show="Tu as 3 secondes. A, B ou C ? 3. 2. 1."),
    dict(type='g_reveal', title="GIMLI",
         say="Le commandant Pearson a choisi Gimli. Trop haut, il fait une glissade, une manœuvre de planeur, pour perdre l'altitude. Le train avant s'effondre, le nez frotte la piste, et l'avion s'arrête avant la foule.",
         show="Le commandant Pearson a choisi Gimli. Trop haut, il fait une glissade, une manœuvre de planeur, pour perdre l'altitude. Le train avant s'effondre, le nez frotte la piste, et l'avion s'arrête avant la foule."),
    dict(type='g_end', title="69 SURVIVANTS",
         say="Les soixante-neuf personnes à bord survivent, sans aucun blessé grave. Et toi, tu avais choisi quoi ? A, B ou C, en commentaire.",
         show="Les 69 personnes à bord survivent, sans aucun blessé grave. Et toi, tu avais choisi quoi ? A, B ou C, en commentaire."),
]
END_HOLD = 12.5
