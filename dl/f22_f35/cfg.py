# Duel : F-22 vs F-35 (sources : Wikipedia F-22 [195 construits, Mach 2,25, supercroisière, export interdit — amendement Obey 1998] ;
# Lockheed Martin [1 000e F-35 en 2024, F-35 Mach 1,6, versions A/B/C] ; ~20 pays utilisateurs/clients du F-35)
import math
A = dict(name="F-22", short="F-22", color=(0.25, 0.55, 1.0), hi=["F-22", "RAPTOR"])
B = dict(name="F-35", short="F-35", color=(1.0, 0.25, 0.22), hi=["F-35", "LIGHTNING"])
FLIP = {"a_34": True, "a_side": True, "b_side": True}
TOPROT = {"a_top": math.pi, "b_top": math.pi}
SCENES = [
    dict(type='hook', score=(0, 0), kicker="LES DEUX FURTIFS AMÉRICAINS",
         say="F vingt-deux contre F trente-cinq. Les deux chasseurs furtifs américains. Cinq rounds, un seul vainqueur.",
         show="F-22 contre F-35. Les deux chasseurs furtifs américains. 5 rounds, un seul vainqueur."),
    dict(type='bars', score=(1, 0), round="ROUND 1", title="LA VITESSE", a=2.25, b=1.6, max=2.6, fmt="MACH {:.2f}", a_first=True,
         say="Round un : la vitesse. Le F vingt-deux dépasse Mach deux. Le F trente-cinq plafonne à Mach un virgule six. Point F vingt-deux.",
         show="Round 1 : la vitesse. Le F-22 dépasse Mach 2. Le F-35 plafonne à Mach 1,6. Point F-22."),
    dict(type='chips', score=(2, 0), round="ROUND 2", title="LE COMBAT AÉRIEN", side='A',
         chips=["SUPERCROISIÈRE", "POUSSÉE VECTORIELLE", "2 MOTEURS"], other="1 MOTEUR", other_grey=True,
         say="Round deux : le combat aérien. Le F vingt-deux vole en supersonique sans postcombustion, et ses tuyères orientables le rendent ultra maniable. Encore le F vingt-deux.",
         show="Round 2 : le combat aérien. Le F-22 vole en supersonique sans postcombustion, et ses tuyères orientables le rendent ultra maniable. Encore le F-22."),
    dict(type='counters', score=(2, 1), round="ROUND 3", title="LA PRODUCTION", a_num=195, b_num=1000, pre="",
         a_sub="F-22 CONSTRUITS · FIN EN 2011", b_sub="F-35 LIVRÉS · ET ÇA CONTINUE", pill="LE F-35 EST TOUJOURS EN PRODUCTION",
         say="Round trois : la production. Seulement cent quatre-vingt-quinze F vingt-deux, chaîne fermée en deux mille onze. Plus de mille F trente-cinq, et ça continue. Point F trente-cinq.",
         show="Round 3 : la production. Seulement 195 F-22, chaîne fermée en 2011. Plus de 1 000 F-35, et ça continue. Point F-35."),
    dict(type='chips', score=(2, 2), round="ROUND 4", title="LA POLYVALENCE", side='B',
         chips=["3 VERSIONS", "DÉCOLLAGE COURT", "PORTE-AVIONS", "FUSION DE CAPTEURS"], other="SUPÉRIORITÉ AÉRIENNE", other_grey=True,
         say="Round quatre : la polyvalence. Le F trente-cinq existe en trois versions, dont une à décollage court et une pour porte-avions. Ses capteurs voient tout autour de lui. Deux partout.",
         show="Round 4 : la polyvalence. Le F-35 existe en 3 versions, dont une à décollage court et une pour porte-avions. Ses capteurs voient tout autour de lui. 2 partout."),
    dict(type='list', score=(2, 3), round="ROUND 5", title="L'EXPORT",
         a_items=["EXPORT INTERDIT", "USA SEULEMENT"], b_items=["ROYAUME-UNI", "JAPON", "ISRAËL", "+ 16 AUTRES"],
         say="Dernier round : l'export. Le Congrès américain interdit de vendre le F vingt-deux, même aux alliés. Le F trente-cinq, lui, a été choisi par près de vingt pays. Point F trente-cinq.",
         show="Dernier round : l'export. Le Congrès américain interdit de vendre le F-22, même aux alliés. Le F-35, lui, a été choisi par près de 20 pays. Point F-35."),
    dict(type='verdict', score=(2, 3), lines=[("ROI DU COMBAT AÉRIEN", 'A'), ("PARTOUT DANS LE MONDE", 'B')],
         say="Verdict : trois à deux pour le F trente-cinq. Le F vingt-deux reste le roi du combat aérien, mais le F trente-cinq est partout. Et toi, tu mets qui ?",
         show="Verdict : 3 à 2 pour le F-35. Le F-22 reste le roi du combat aérien, mais le F-35 est partout. Et toi, tu mets qui ?"),
]
END_HOLD = 6.0
