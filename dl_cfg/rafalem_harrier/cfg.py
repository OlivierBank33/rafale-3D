# Duel : Rafale Marine vs Harrier (modèle 3D : Harrier GR1 FlightGear). Sources : migflug.com/aircraft/harrier-jump-jet [GR1 en service RAF le 01/04/1969, 1er avion de combat
# à décollage vertical opérationnel ; GR1/GR3 1 176 km/h au niveau de la mer, AV-8B limité à Mach 0,9 (subsonique) ; dernier vol RAF 15/12/2010] ; Rafale M : Mach 1,8, 13 points d'emport,
# catapulté depuis le Charles de Gaulle (France = seule marine avec les États-Unis à catapulter ses chasseurs) ; Harrier GR1 : 5 points d'emport (4 sous les ailes + 1 ventral) ;
# dispersion de la RAF en Allemagne : Harrier opérant depuis des clairières et des routes
import math
A = dict(name="RAFALE MARINE", short="RAFALE", color=(0.20, 0.50, 1.0), hi=["RAFALE"])
B = dict(name="HARRIER", short="HARRIER", color=(1.0, 0.25, 0.22), hi=["HARRIER"])
FLIP = {}
TOPROT = {"a_top": -math.pi / 2, "b_top": math.pi}
SCENES = [
    dict(type='hook', score=(0, 0), kicker="CATAPULTE OU DÉCOLLAGE VERTICAL ?",
         say="Le Rafale Marine peut-il battre le Harrier, l'avion qui décolle à la verticale ? La catapulte contre l'ascenseur. Cinq rounds, un seul vainqueur.",
         show="Le Rafale Marine peut-il battre le Harrier, l'avion qui décolle à la verticale ? La catapulte contre l'ascenseur. 5 rounds, un seul vainqueur."),
    dict(type='chips', score=(0, 1), round="ROUND 1", title="LE DÉCOLLAGE", side='B',
         chips=["DÉCOLLAGE VERTICAL", "VOL STATIONNAIRE", "EN SERVICE DÈS 1969"], other="BESOIN D'UNE CATAPULTE", other_grey=True,
         say="Round un : le décollage. Le Harrier monte à la verticale et reste immobile en l'air, comme un hélicoptère. Premier avion de combat à le faire en service, dès mille neuf cent soixante-neuf. Point Harrier.",
         show="Round 1 : le décollage. Le Harrier monte à la verticale et reste immobile en l'air, comme un hélicoptère. Premier avion de combat à le faire en service, dès 1969. Point Harrier."),
    dict(type='chips', score=(1, 1), round="ROUND 2", title="LA VITESSE", side='A',
         chips=["MACH 1,8", "SUPERSONIQUE"], other="SUBSONIQUE", other_grey=True,
         say="Round deux : la vitesse. Le Rafale file à Mach un virgule huit. Le Harrier ne passe pas le mur du son en palier. Point Rafale.",
         show="Round 2 : la vitesse. Le Rafale file à Mach 1,8. Le Harrier ne passe pas le mur du son en palier. Point Rafale."),
    dict(type='chips', score=(1, 2), round="ROUND 3", title="LA PISTE", side='B',
         chips=["UN PETIT PONT SUFFIT", "MÊME UNE ROUTE", "OU UNE CLAIRIÈRE"], other="PORTE-AVIONS À CATAPULTES", other_grey=True,
         say="Round trois : la piste. Le Harrier se pose sur un petit pont, une route, et même une clairière en forêt. Le Rafale Marine, lui, a besoin d'un porte-avions à catapultes. Point Harrier.",
         show="Round 3 : la piste. Le Harrier se pose sur un petit pont, une route, et même une clairière en forêt. Le Rafale Marine, lui, a besoin d'un porte-avions à catapultes. Point Harrier."),
    dict(type='bars', score=(2, 2), round="ROUND 4", title="L'ARMEMENT", a=13, b=5, max=15, fmt="{:.0f} POINTS",
         say="Round quatre : l'armement. Le Rafale Marine a treize points d'emport pour ses missiles et ses bombes. Le Harrier d'origine, cinq. Deux partout.",
         show="Round 4 : l'armement. Le Rafale Marine a 13 points d'emport pour ses missiles et ses bombes. Le Harrier d'origine, 5. 2 partout."),
    dict(type='list', score=(3, 2), round="ROUND 5", title="LA CATAPULTE",
         a_items=["CATAPULTÉ EN MER", "FRANCE + USA SEULEMENT"], b_items=["RETIRÉ PAR LA RAF", "EN 2010"],
         say="Dernier round, décisif : la catapulte. Avec les États-Unis, la France est la seule marine au monde à catapulter ses chasseurs. Le Rafale Marine vole toujours. Les Britanniques, eux, ont retiré leurs Harrier en deux mille dix. Point Rafale.",
         show="Dernier round, décisif : la catapulte. Avec les États-Unis, la France est la seule marine au monde à catapulter ses chasseurs. Le Rafale Marine vole toujours. Les Britanniques, eux, ont retiré leurs Harrier en 2010. Point Rafale."),
    dict(type='verdict', score=(3, 2), lines=[("VITESSE, ARMEMENT, CATAPULTE", 'A'), ("VERTICAL, PISTES DE FORTUNE", 'B')],
         say="Verdict : trois à deux pour le Rafale Marine. Plus rapide, mieux armé, et toujours en service. Mais aucun avion n'a jamais égalé le Harrier pour décoller de n'importe où. Et toi, tu mets qui ?",
         show="Verdict : 3 à 2 pour le Rafale Marine. Plus rapide, mieux armé, et toujours en service. Mais aucun avion n'a jamais égalé le Harrier pour décoller de n'importe où. Et toi, tu mets qui ?"),
]
END_HOLD = 10.0
