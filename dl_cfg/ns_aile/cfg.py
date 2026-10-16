# LA SCIENCE DU VOL 03 : comment une aile porte. Sources : Airbus A380 (masse max au décollage 575 t, surface alaire 845 m² -> ≈ 680 kg/m²) ;
# NASA Glenn « Incorrect Lift Theory » (mythe du temps de transit égal : l'air du dessus arrive avant celui du dessous) ; portance L = ½ ρ V² S Cz (× 4 si V × 2 à incidence égale) ;
# incidence de décrochage typique ≈ 15° pour un profil classique ; volets et becs augmentent la portance à basse vitesse ; vol dos possible avec une incidence adaptée
SERIES = "LA SCIENCE DU VOL"; EP = "03"; NEXT = "POURQUOI LES AVIONS NE VOLENT PAS TOUT DROIT"
SCENES = [
    dict(type='hook', top=("575 T", "845 M²"), sub=("masse max d'un A380", "surface de ses ailes"),
         gauges=[("CHARGE PAR M² D'AILE", "680 KG", 0.68, (0.45, 1.0, 0.92)), ("PORTANCE = POIDS", "575 T", 0.95, (1.0, 0.55, 0.0))],
         say="Cinq cent soixante-quinze tonnes. C'est le poids maximal d'un A trois cent quatre-vingts au décollage. Et ce sont ses ailes, et rien d'autre, qui le portent. Mais comment ?",
         show="575 tonnes. C'est le poids maximal d'un A380 au décollage. Et ce sont ses ailes, et rien d'autre, qui le portent. Mais comment ?"),
    dict(type='plan', items=["L'ANGLE", "LA FORME", "LA VITESSE", "LA LIMITE"],
         say="Quatre idées pour tout comprendre. Et un mythe qu'on apprend encore à l'école.",
         show="4 idées pour tout comprendre. Et un mythe qu'on apprend encore à l'école."),
    dict(type='angle', num=1, title="L'ANGLE",
         say="Un : l'angle. L'aile attaque l'air légèrement inclinée. Elle pousse l'air vers le bas. Et en retour, l'air pousse l'aile vers le haut. C'est l'action et la réaction.",
         show="1 : l'angle. L'aile attaque l'air légèrement inclinée. Elle pousse l'air vers le bas. Et en retour, l'air pousse l'aile vers le haut. C'est l'action et la réaction."),
    dict(type='forme', num=2, title="LA FORME",
         say="Deux : la forme. Le dessus de l'aile est bombé. L'air y accélère, et sa pression baisse. Dessous, elle est plus forte. Résultat : l'aile est aspirée vers le haut.",
         show="2 : la forme. Le dessus de l'aile est bombé. L'air y accélère, et sa pression baisse. Dessous, elle est plus forte. Résultat : l'aile est aspirée vers le haut."),
    dict(type='piege', num=None, title="LE MYTHE",
         say="Et le mythe ? On raconte que l'air du dessus doit aller plus vite pour retrouver l'air du dessous au bout de l'aile. Faux. En réalité, il arrive bien avant. Les deux ne se retrouvent jamais.",
         show="Et le mythe ? On raconte que l'air du dessus doit aller plus vite pour retrouver l'air du dessous au bout de l'aile. Faux. En réalité, il arrive bien avant. Les deux ne se retrouvent jamais."),
    dict(type='vitesse', num=3, title="LA VITESSE",
         say="Trois : la vitesse. La portance dépend du carré de la vitesse. Va deux fois plus vite, et ton aile porte quatre fois plus.",
         show="3 : la vitesse. La portance dépend du carré de la vitesse. Va 2 fois plus vite, et ton aile porte 4 fois plus."),
    dict(type='limite', num=4, title="LA LIMITE",
         say="Quatre : la limite. Si on lève trop le nez, vers quinze degrés pour une aile classique, l'air décroche du dessus de l'aile. La portance s'effondre. C'est le décrochage.",
         show="4 : la limite. Si on lève trop le nez, vers 15 degrés pour une aile classique, l'air décroche du dessus de l'aile. La portance s'effondre. C'est le décrochage."),
    dict(type='astuce', num=None, title="L'ASTUCE",
         say="Pour voler lentement au décollage et à l'atterrissage, les avions de ligne sortent des volets et des becs. L'aile devient plus grande et plus bombée.",
         show="Pour voler lentement au décollage et à l'atterrissage, les avions de ligne sortent des volets et des becs. L'aile devient plus grande et plus bombée."),
    dict(type='dos', num=None, title="LA PREUVE",
         say="La preuve que l'angle compte autant que la forme : un avion de voltige peut voler sur le dos. Il lui suffit de garder le bon angle.",
         show="La preuve que l'angle compte autant que la forme : un avion de voltige peut voler sur le dos. Il lui suffit de garder le bon angle."),
    dict(type='outro', num=None, title="ABONNE-TOI", lines=("UNE AILE ?", "UNE MACHINE À POUSSER L'AIR"),
         say="Une aile, c'est une machine à pousser l'air vers le bas. Abonne-toi pour la suite de la science du vol.",
         show="Une aile, c'est une machine à pousser l'air vers le bas. Abonne-toi pour la suite de la science du vol."),
]
END_HOLD = 2.5
