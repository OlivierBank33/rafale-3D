# Duel : Rafale vs F-16 (sources : migflug.com/aircraft/rafale [Mach 1,8 ; biréacteur M88] ; dassault-aviation.com « Adapt and deliver » [plus de 9 t de charge externe, 14 points d'emport] ;
# Wikipedia F-16 [chasseur le plus nombreux en service (Flight Global World Air Forces) ; Mach 2+ (2 178 km/h), monoréacteur, ~7 700 kg d'emport, plus de 4 600 construits] ; Rafale Marine sur le Charles-de-Gaulle ; le F-16 n'est pas embarqué)
import math
A = dict(name="RAFALE", short="RAFALE", color=(0.20, 0.50, 1.0), hi=["RAFALE"])
B = dict(name="F-16", short="F-16", color=(1.0, 0.25, 0.22), hi=["F-16"])
FLIP = {}
TOPROT = {"a_top": -math.pi / 2, "b_top": math.pi}
SCENES = [
    dict(type='hook', score=(0, 0), kicker="LE RAFALE PEUT-IL BATTRE LE F-16 ?",
         say="Le Rafale peut-il battre le F seize, le chasseur le plus répandu de la planète ? La France contre l'Amérique. Cinq rounds, un seul vainqueur.",
         show="Le Rafale peut-il battre le F-16, le chasseur le plus répandu de la planète ? La France contre l'Amérique. 5 rounds, un seul vainqueur."),
    dict(type='bars', score=(0, 1), round="ROUND 1", title="LA VITESSE", a=1.8, b=2.0, max=2.4, fmt="MACH {:.1f}",
         say="Round un : la vitesse. Le Rafale atteint Mach un virgule huit. Le F seize dépasse Mach deux. Point F seize.",
         show="Round 1 : la vitesse. Le Rafale atteint Mach 1,8. Le F-16 dépasse Mach 2. Point F-16."),
    dict(type='chips', score=(1, 1), round="ROUND 2", title="LES MOTEURS", side='A',
         chips=["DEUX RÉACTEURS M88", "UN PEUT LÂCHER", "IL RENTRE QUAND MÊME"], other="UN SEUL RÉACTEUR", other_grey=True,
         say="Round deux : les moteurs. Le Rafale a deux réacteurs : si l'un tombe en panne, il peut rentrer sur l'autre. Le F seize n'en a qu'un seul. Point Rafale.",
         show="Round 2 : les moteurs. Le Rafale a deux réacteurs : si l'un tombe en panne, il peut rentrer sur l'autre. Le F-16 n'en a qu'un seul. Point Rafale."),
    dict(type='chips', score=(1, 2), round="ROUND 3", title="LES VENTES", side='B',
         chips=["PLUS DE 4 600 CONSTRUITS", "LE PLUS NOMBREUX EN SERVICE"], other="BEAUCOUP MOINS", other_grey=True,
         say="Round trois : les ventes. Plus de quatre mille six cents F seize ont été construits. C'est le chasseur le plus nombreux en service dans le monde. Point F seize.",
         show="Round 3 : les ventes. Plus de 4 600 F-16 ont été construits. C'est le chasseur le plus nombreux en service dans le monde. Point F-16."),
    dict(type='bars', score=(2, 2), round="ROUND 4", title="LA CHARGE", a=9.0, b=7.7, max=10, fmt="{:.1f} T", race=False, a_first=True,
         say="Round quatre : la charge. Le Rafale emporte plus de neuf tonnes d'armes et de carburant sous ses ailes. Le F seize, environ sept virgule sept. Deux partout.",
         show="Round 4 : la charge. Le Rafale emporte plus de 9 tonnes d'armes et de carburant sous ses ailes. Le F-16, environ 7,7. 2 partout."),
    dict(type='chips', score=(3, 2), round="ROUND 5", title="LE PORTE-AVIONS", side='A',
         chips=["RAFALE MARINE", "CATAPULTE", "CHARLES-DE-GAULLE"], other="JAMAIS EMBARQUÉ", other_grey=True,
         say="Dernier round, décisif : le porte-avions. Le Rafale Marine décolle du Charles de Gaulle. Le F seize, lui, n'a jamais été embarqué. Point Rafale.",
         show="Dernier round, décisif : le porte-avions. Le Rafale Marine décolle du Charles-de-Gaulle. Le F-16, lui, n'a jamais été embarqué. Point Rafale."),
    dict(type='verdict', score=(3, 2), lines=[("BIMOTEUR, CHARGE, PORTE-AVIONS", 'A'), ("VITESSE, VENTES", 'B')],
         say="Verdict : trois à deux pour le Rafale. Plus sûr, plus chargé, et capable d'opérer en mer. Mais le F seize reste plus rapide, et c'est le plus répandu de la planète. Et toi, tu mets qui ?",
         show="Verdict : 3 à 2 pour le Rafale. Plus sûr, plus chargé, et capable d'opérer en mer. Mais le F-16 reste plus rapide, et c'est le plus répandu de la planète. Et toi, tu mets qui ?"),
]
END_HOLD = 10.5
