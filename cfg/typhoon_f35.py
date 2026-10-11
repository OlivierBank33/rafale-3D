# Duel : Eurofighter Typhoon vs F-35 (sources : leonardo.com Typhoon Mach 2, 2 EJ200 ; Lockheed Martin F-35 Mach 1,6, record 191 livraisons en 2025,
# 1 000e F-35 en 2024 ; euro-sd.com 01/2026 : 769 Eurofighter commandés, 1 M h de vol ; The Aviationist 06/08/2025 : l'Espagne abandonne le F-35,
# 85 % de son plan de défense de 10,5 Md€ en Europe, 25 Eurofighter commandés en déc. 2024)
import math
A = dict(name="TYPHOON", short="TYPHOON", color=(0.20, 0.50, 1.0), hi=["TYPHOON", "EUROFIGHTER", "EUROPE"])
B = dict(name="F-35", short="F-35", color=(1.0, 0.25, 0.22), hi=["F-35", "AMÉRIQUE"])
FLIP = {"a_34": True, "a_side": True, "b_side": True}
TOPROT = {"a_top": math.pi, "b_top": math.pi}
SCENES = [
    dict(type='hook', score=(0, 0), kicker="L'EUROPE PEUT-ELLE BATTRE LE F-35 ?",
         say="L'Europe peut-elle battre le F trente-cinq ? Eurofighter Typhoon contre F trente-cinq. Cinq rounds, un seul vainqueur.",
         show="L'Europe peut-elle battre le F-35 ? Eurofighter Typhoon contre F-35. 5 rounds, un seul vainqueur."),
    dict(type='chips', score=(0, 1), round="ROUND 1", title="LA FURTIVITÉ", side='B',
         chips=["CONÇU FURTIF", "ARMES EN SOUTE"], other="PAS FURTIF", other_grey=True,
         say="Round un : la furtivité. Le F trente-cinq a été dessiné pour échapper aux radars, avec ses armes cachées en soute. Le Typhoon, non. Point F trente-cinq.",
         show="Round 1 : la furtivité. Le F-35 a été dessiné pour échapper aux radars, avec ses armes cachées en soute. Le Typhoon, non. Point F-35."),
    dict(type='bars', score=(1, 1), round="ROUND 2", title="LA VITESSE", a=2.0, b=1.6, max=2.4, fmt="MACH {:.1f}", a_first=True,
         say="Round deux : la vitesse. Le Typhoon pointe à Mach deux. Le F trente-cinq plafonne à Mach un virgule six. Point Typhoon.",
         show="Round 2 : la vitesse. Le Typhoon pointe à Mach 2. Le F-35 plafonne à Mach 1,6. Point Typhoon."),
    dict(type='counters', score=(1, 2), round="ROUND 3", title="LE NOMBRE", a_num=769, b_num=1000, pre="",
         a_sub="TYPHOON COMMANDÉS", b_sub="F-35 LIVRÉS · 191 EN 2025", pill="PLUS DE 1 000 F-35 DÉJÀ LIVRÉS",
         say="Round trois : le nombre. Sept cent soixante-neuf Typhoon commandés. Plus de mille F trente-cinq déjà livrés, dont cent quatre-vingt-onze rien qu'en deux mille vingt-cinq. Point F trente-cinq.",
         show="Round 3 : le nombre. 769 Typhoon commandés. Plus de 1 000 F-35 déjà livrés, dont 191 rien qu'en 2025. Point F-35."),
    dict(type='chips', score=(2, 2), round="ROUND 4", title="LE COMBAT RAPPROCHÉ", side='A',
         chips=["2 RÉACTEURS", "AILE DELTA + CANARDS", "TRÈS MANIABLE"], other="1 RÉACTEUR", other_grey=True,
         say="Round quatre : le combat rapproché. Deux réacteurs, une aile delta, des petits plans canard à l'avant. En virage, le Typhoon est redoutable. Deux partout.",
         show="Round 4 : le combat rapproché. 2 réacteurs, une aile delta, des petits plans canard à l'avant. En virage, le Typhoon est redoutable. 2 partout."),
    dict(type='list', score=(3, 2), round="ROUND 5", title="L'INDÉPENDANCE",
         a_items=["L'ESPAGNE CHOISIT L'EUROPE", "25 TYPHOON COMMANDÉS"], b_items=["F-35 ABANDONNÉ", "PAR L'ESPAGNE EN 2025"],
         say="Dernier round, la surprise : l'indépendance. En deux mille vingt-cinq, l'Espagne renonce au F trente-cinq pour garder son argent en Europe. Elle mise sur le Typhoon. Point Typhoon.",
         show="Dernier round, la surprise : l'indépendance. En 2025, l'Espagne renonce au F-35 pour garder son argent en Europe. Elle mise sur le Typhoon. Point Typhoon."),
    dict(type='verdict', score=(3, 2), lines=[("VITESSE, VIRAGE, EUROPE", 'A'), ("FURTIF, PRODUIT EN MASSE", 'B')],
         say="Verdict : trois à deux pour le Typhoon. Le F trente-cinq est plus furtif et se vend partout. Mais le Typhoon va plus vite, tourne mieux, et reste européen. Et toi, tu mets qui ?",
         show="Verdict : 3 à 2 pour le Typhoon. Le F-35 est plus furtif et se vend partout. Mais le Typhoon va plus vite, tourne mieux, et reste européen. Et toi, tu mets qui ?"),
]
END_HOLD = 9.0
