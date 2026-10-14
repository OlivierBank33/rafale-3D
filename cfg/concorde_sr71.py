# Duel : Concorde vs SR-71 (sources : Wikipedia SR-71 [32 construits, 12 perdus en accident, ~3 530 km/h (record 1976), ~25 900 m (record 1976),
# Londres-New York 1 h 54 min 56 s (1974), 2 membres d'équipage en scaphandre, nourriture en tube] ; planefyi « Concorde facts » [20 construits,
# 14 en service commercial, plafond 60 000 ft (~18 300 m), New York-Londres record 2 h 52 min 59 s (1996), 27 ans de service, 2,5 M de passagers,
# 1 accident mortel (AF4590, 25/07/2000)] ; Concorde Mach 2,04, ~100 passagers)
import math
A = dict(name="CONCORDE", short="CONCORDE", color=(0.20, 0.50, 1.0), hi=["CONCORDE"])
B = dict(name="SR-71", short="SR-71", color=(1.0, 0.25, 0.22), hi=["SR-71", "BLACKBIRD"])
FLIP = {"a_34": True, "a_side": True, "b_side": True}
TOPROT = {"a_top": math.pi, "b_top": math.pi}
SCENES = [
    dict(type='hook', score=(0, 0), kicker="LE CONCORDE BAT-IL LE BLACKBIRD ?",
         say="Le Concorde peut-il battre le S R soixante et onze ? Les deux rois de la vitesse. Cinq rounds, un seul vainqueur.",
         show="Le Concorde peut-il battre le SR-71 ? Les deux rois de la vitesse. 5 rounds, un seul vainqueur."),
    dict(type='bars', score=(0, 1), round="ROUND 1", title="LA VITESSE", a=2170, b=3530, max=3900, fmt="{:.0f} KM/H",
         say="Round un : la vitesse. Le Concorde file à Mach deux. Le Blackbird, à plus de trois mille cinq cents kilomètres-heure. Point S R soixante et onze.",
         show="Round 1 : la vitesse. Le Concorde file à Mach 2. Le Blackbird, à plus de 3 500 km/h. Point SR-71."),
    dict(type='counters', score=(1, 1), round="ROUND 2", title="LES PASSAGERS", a_num=100, b_num=2, pre="", static=True,
         a_sub="PASSAGERS ENVIRON", b_sub="PILOTE + OPÉRATEUR", pill="2,5 MILLIONS DE PASSAGERS EN 27 ANS",
         say="Round deux : les passagers. Le Concorde emporte une centaine de passagers. Le Blackbird, seulement deux hommes. Point Concorde.",
         show="Round 2 : les passagers. Le Concorde emporte une centaine de passagers. Le Blackbird, seulement 2 hommes. Point Concorde."),
    dict(type='bars', score=(1, 2), round="ROUND 3", title="L'ALTITUDE", a=18.3, b=25.9, max=28, fmt="{:.1f} KM", race=False,
         say="Round trois : l'altitude. Le Concorde monte à dix-huit kilomètres. Le Blackbird, à près de vingt-six. Point S R soixante et onze.",
         show="Round 3 : l'altitude. Le Concorde monte à 18 kilomètres. Le Blackbird, à près de 26. Point SR-71."),
    dict(type='counters', score=(2, 2), round="ROUND 4", title="LA SÉCURITÉ", a_num=1, b_num=12, pre="", static=True,
         a_sub="ACCIDENT MORTEL · 20 AVIONS", b_sub="PERDUS EN ACCIDENT · 32 AVIONS", pill="",
         say="Round quatre : la sécurité. Un seul accident mortel pour le Concorde, en vingt-sept ans. Le Blackbird, lui, a perdu douze avions sur trente-deux. Deux partout.",
         show="Round 4 : la sécurité. Un seul accident mortel pour le Concorde, en 27 ans. Le Blackbird, lui, a perdu 12 avions sur 32. 2 partout."),
    dict(type='list', score=(3, 2), round="ROUND 5", title="LE CONFORT",
         a_items=["SIÈGE EN CUIR", "REPAS SERVI À MACH 2"], b_items=["SCAPHANDRE", "NOURRITURE EN TUBE"],
         say="Dernier round, la surprise : le confort. Dans le Concorde, on déjeune à Mach deux. Dans le Blackbird, on porte un scaphandre, et on mange dans un tube, à travers le casque. Point Concorde.",
         show="Dernier round, la surprise : le confort. Dans le Concorde, on déjeune à Mach 2. Dans le Blackbird, on porte un scaphandre, et on mange dans un tube, à travers le casque. Point Concorde."),
    dict(type='verdict', score=(3, 2), lines=[("PASSAGERS, SÉCURITÉ, CONFORT", 'A'), ("VITESSE, ALTITUDE", 'B')],
         say="Verdict : trois à deux pour le Concorde. Le Blackbird va plus vite et plus haut. Mais le Concorde a fait voyager des millions de gens au-dessus du son. Et toi, tu mets qui ?",
         show="Verdict : 3 à 2 pour le Concorde. Le Blackbird va plus vite et plus haut. Mais le Concorde a fait voyager des millions de gens au-dessus du son. Et toi, tu mets qui ?"),
]
END_HOLD = 10.5
