# Décodé 02 : les hublots ronds (sources : FAA Lessons Learned G-ALYV/Comet [G-ALYP Elbe 10/01/1954 35 morts ; G-ALYY Naples 08/04/1954 21 morts ;
# essai en cuve G-ALYU : ~3 060 cycles (1 230 vols + ~1 830 en cuve), fissure au coin d'une fenêtre presque carrée, contraintes aux coins bien
# supérieures aux calculs] ; migflug « The hole in your aircraft window » [3 vitres, l'extérieure encaisse, trou de respiration dans la vitre du milieu,
# celle-ci sert de secours] ; différentiel de pression ~0,55 bar ≈ 5,6 t par m²)
FICHE = "02"; TITLE = "LES HUBLOTS"; NEXT = "LA BOÎTE NOIRE"
SCENES = [
    dict(type='window', say="Dix mille mètres. Entre toi et le vide, il y a juste ce hublot. Et chaque mètre carré de l'avion est poussé vers l'extérieur avec plus de cinq tonnes.",
         show="10 000 mètres. Entre toi et le vide, il y a juste ce hublot. Et chaque mètre carré de l'avion est poussé vers l'extérieur avec plus de 5 tonnes."),
    dict(type='comet', say="Histoire vraie. Mille neuf cent cinquante-quatre. Le Comet est le premier avion de ligne à réaction de l'histoire. Et en trois mois, deux Comet se désintègrent en plein vol, au-dessus de la Méditerranée.",
         show="Histoire vraie. 1954. Le Comet est le premier avion de ligne à réaction de l'histoire. Et en trois mois, deux Comet se désintègrent en plein vol, au-dessus de la Méditerranée."),
    dict(type='tank', say="Pour comprendre, les ingénieurs plongent un Comet entier dans une cuve d'eau géante. Ils le gonflent, puis le dégonflent, comme à chaque vol. Encore. Et encore.",
         show="Pour comprendre, les ingénieurs plongent un Comet entier dans une cuve d'eau géante. Ils le gonflent, puis le dégonflent, comme à chaque vol. Encore. Et encore."),
    dict(type='crack', say="Au bout d'environ trois mille cycles, le métal cède. La fissure part du coin d'une fenêtre presque carrée.",
         show="Au bout d'environ 3 000 cycles, le métal cède. La fissure part du coin d'une fenêtre presque carrée."),
    dict(type='stress', say="Alors, on ouvre. Ton avion, c'est un ballon qu'on gonfle à chaque vol. Dans un coin, toute la force se concentre sur un seul point. Dans un cercle, elle glisse tout autour.",
         show="Alors, on ouvre. Ton avion, c'est un ballon qu'on gonfle à chaque vol. Dans un coin, toute la force se concentre sur un seul point. Dans un cercle, elle glisse tout autour."),
    dict(type='panes', say="Et regarde bien ton hublot : il y a un petit trou. Ce n'est pas un défaut. Il y a trois vitres, et ce trou laisse passer l'air, pour que la vitre extérieure encaisse tout. Celle du milieu, c'est la roue de secours.",
         show="Et regarde bien ton hublot : il y a un petit trou. Ce n'est pas un défaut. Il y a trois vitres, et ce trou laisse passer l'air, pour que la vitre extérieure encaisse tout. Celle du milieu, c'est la roue de secours."),
    dict(type='round', say="Depuis le Comet, tous les hublots sont arrondis. Et pour chaque nouveau modèle, un exemplaire est gonflé et dégonflé des dizaines de milliers de fois avant le premier passager.",
         show="Depuis le Comet, tous les hublots sont arrondis. Et pour chaque nouveau modèle, un exemplaire est gonflé et dégonflé des dizaines de milliers de fois avant le premier passager."),
    dict(type='outro2', say="Alors au prochain vol, cherche le petit trou. Tu l'avais déjà remarqué ? Dis-le en commentaire. Prochaine fiche : la boîte noire.",
         show="Alors au prochain vol, cherche le petit trou. Tu l'avais déjà remarqué ? Dis-le en commentaire. Prochaine fiche : la boîte noire."),
]
END_HOLD = 2.5
