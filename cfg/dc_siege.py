# Décodé 05 : le siège éjectable (sources : migflug.com « Anatoly Kvochur » [Le Bourget 1989, oiseau aspiré dans le moteur droit, ~180 km/h,
# avion écarté de la foule, éjection K-36D 2,5 s avant l'impact, pilote posé à ~30 m de l'épave] ; Wikipedia NPP Zvezda K-36 [zéro-zéro] ;
# migflug.com « What happens inside an ejection seat » [verrière, catapulte 12-14 G, fusée, < 2,5 s jusqu'au parachute] ;
# migflug.com « two centimetres shorter » [pic ~14-25 G, perte de 1 à 3 cm] ; Wikipedia Martin-Baker Mk.1 [1er essai en vol, Bernard Lynch, 24/07/1946] ;
# EurAsian Times 25/08/2026 [7 827 vies sauvées par Martin-Baker])
FICHE = "05"; TITLE = "LE SIÈGE ÉJECTABLE"; NEXT = "LA COMBINAISON ANTI-G"
SCENES = [
    dict(type='ejhook', say="Un pilote peut-il survivre à une éjection à quelques mètres du sol ? C'est arrivé. Au salon du Bourget.",
         show="Un pilote peut-il survivre à une éjection à quelques mètres du sol ? C'est arrivé. Au salon du Bourget."),
    dict(type='bourget', say="Histoire vraie. Juin mille neuf cent quatre-vingt-neuf. Un MiG vingt-neuf vole très lentement, nez haut, devant la foule. Un oiseau est aspiré dans le moteur droit. Le moteur prend feu.",
         show="Histoire vraie. Juin 1989. Un MiG-29 vole très lentement, nez haut, devant la foule. Un oiseau est aspiré dans le moteur droit. Le moteur prend feu."),
    dict(type='ejdive', say="L'avion bascule vers le sol. Le pilote, Anatoli Kvotchour, l'écarte de la foule. Puis il tire la poignée. Deux secondes et demie avant l'impact.",
         show="L'avion bascule vers le sol. Le pilote, Anatoli Kvotchour, l'écarte de la foule. Puis il tire la poignée. 2,5 secondes avant l'impact."),
    dict(type='ejseq', say="Tout va très vite. La verrière saute. Une charge explosive pousse le siège sur ses rails. Puis une fusée, sous le siège, l'envoie encore plus haut.",
         show="Tout va très vite. La verrière saute. Une charge explosive pousse le siège sur ses rails. Puis une fusée, sous le siège, l'envoie encore plus haut."),
    dict(type='ejg', say="Le pilote encaisse plus de quinze G. Sa colonne vertébrale se tasse : beaucoup de pilotes perdent un à trois centimètres, parfois pour toujours.",
         show="Le pilote encaisse plus de 15 G. Sa colonne vertébrale se tasse : beaucoup de pilotes perdent 1 à 3 centimètres, parfois pour toujours."),
    dict(type='ejzero', say="Son siège est dit zéro-zéro : il peut sauver un pilote même à l'arrêt, sur la piste. Au Bourget, le parachute s'ouvre juste à temps. Kvotchour se pose à une trentaine de mètres de son avion en feu. Vivant.",
         show="Son siège est dit zéro-zéro : il peut sauver un pilote même à l'arrêt, sur la piste. Au Bourget, le parachute s'ouvre juste à temps. Kvotchour se pose à une trentaine de mètres de son avion en feu. Vivant."),
    dict(type='ejsaved', say="Depuis le premier essai en vol, en mille neuf cent quarante-six, les sièges du britannique Martin-Baker ont sauvé plus de sept mille huit cents pilotes.",
         show="Depuis le premier essai en vol, en 1946, les sièges du britannique Martin-Baker ont sauvé plus de 7 800 pilotes."),
    dict(type='ejoutro', say="Toi, tu aurais tiré la poignée aussi tard ? Dis-le en commentaire. Prochaine fiche : la combinaison anti-G.",
         show="Toi, tu aurais tiré la poignée aussi tard ? Dis-le en commentaire. Prochaine fiche : la combinaison anti-G."),
]
END_HOLD = 4.0
