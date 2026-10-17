# LA SCIENCE DU VOL 04 : pourquoi les avions ne volent pas tout droit. Calculs maison (sphère R = 6 371 km) : CDG–LAX orthodromie ≈ 9 100 km, loxodromie (droite sur carte Mercator) ≈ 10 140 km,
# latitude max de l'orthodromie ≈ 62° N vers 49° O (sud du Groenland) ; jet-stream d'ouest, cœur souvent > 300 km/h ; vols vers l'est plus courts (ex. New York–Paris ≈ 7 h contre ≈ 8 h dans l'autre sens) ;
# North Atlantic Tracks publiés chaque jour selon les vents ; ETOPS : un biréacteur doit rester à un temps de vol limité d'un aéroport de dégagement
SERIES = "LA SCIENCE DU VOL"; EP = "04"; NEXT = "COMMENT UN AVION FREINE"
SCENES = [
    dict(type='hook', top=("10 140 KM", "9 100 KM"), sub=("tout droit sur la carte", "par le Groenland"),
         gauges=[("PARIS → LOS ANGELES", "−1 000 KM", 0.9, (1.0, 0.55, 0.0)), ("LATITUDE MAX", "62° N", 0.69, (0.45, 1.0, 0.92))],
         say="Paris, Los Angeles. Tout droit sur la carte : dix mille kilomètres. Par le Groenland : mille de moins. Alors, pourquoi les avions font-ils ce détour qui n'en est pas un ?",
         show="Paris, Los Angeles. Tout droit sur la carte : 10 000 km. Par le Groenland : 1 000 de moins. Alors, pourquoi les avions font-ils ce détour qui n'en est pas un ?"),
    dict(type='plan', items=["LA CARTE", "LE GLOBE", "LE VENT", "LA SÉCURITÉ"],
         say="Trois raisons. Et une règle de sécurité que peu de passagers connaissent.",
         show="3 raisons. Et une règle de sécurité que peu de passagers connaissent."),
    dict(type='carte', num=1, title="LA CARTE",
         say="Un : la carte ment. Pour étaler une Terre ronde sur du papier, on la déforme. La ligne droite de la carte fait plus de dix mille kilomètres. La vraie route la plus courte, elle, monte vers le nord.",
         show="1 : la carte ment. Pour étaler une Terre ronde sur du papier, on la déforme. La ligne droite de la carte fait plus de 10 000 km. La vraie route la plus courte, elle, monte vers le nord."),
    dict(type='globe', num=2, title="LE GLOBE",
         say="Deux : le globe. Sur une boule, le plus court chemin entre deux villes est un arc de grand cercle. Vu sur un globe, ce détour par le Groenland est une ligne parfaitement droite.",
         show="2 : le globe. Sur une boule, le plus court chemin entre deux villes est un arc de grand cercle. Vu sur un globe, ce détour par le Groenland est une ligne parfaitement droite."),
    dict(type='jet', num=3, title="LE VENT",
         say="Trois : le vent. En altitude, le jet-stream souffle d'ouest en est, parfois à plus de trois cents kilomètres-heure. Vers l'Europe, les avions le prennent dans le dos. Le retour de New York peut durer environ une heure de moins.",
         show="3 : le vent. En altitude, le jet-stream souffle d'ouest en est, parfois à plus de 300 km/h. Vers l'Europe, les avions le prennent dans le dos. Le retour de New York peut durer environ une heure de moins."),
    dict(type='nat', num=None, title="LES AUTOROUTES",
         say="C'est pour ça qu'au-dessus de l'Atlantique, les routes des avions sont redessinées chaque jour, pour suivre ou éviter ce vent.",
         show="C'est pour ça qu'au-dessus de l'Atlantique, les routes des avions sont redessinées chaque jour, pour suivre ou éviter ce vent."),
    dict(type='etops', num=4, title="LA SÉCURITÉ",
         say="Quatre : la sécurité. Un avion à deux moteurs doit toujours rester à un temps de vol limité d'un aéroport de secours. Sa route passe donc près de l'Irlande, de l'Islande ou de Terre-Neuve.",
         show="4 : la sécurité. Un avion à deux moteurs doit toujours rester à un temps de vol limité d'un aéroport de secours. Sa route passe donc près de l'Irlande, de l'Islande ou de Terre-Neuve."),
    dict(type='outro', num=None, title="ABONNE-TOI", lines=("LE DÉTOUR ?", "C'EST LE CHEMIN LE PLUS COURT"),
         say="Le détour, c'est en fait le chemin le plus court. Abonne-toi pour la suite de la science du vol.",
         show="Le détour, c'est en fait le chemin le plus court. Abonne-toi pour la suite de la science du vol."),
]
END_HOLD = 4.5
