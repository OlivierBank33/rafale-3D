# Duel : Rafale vs Eurofighter Typhoon (faits vérifiés le 03/10/2026 — sources dans history.json)
A = dict(name="RAFALE", short="RAFALE", color=(0.20, 0.50, 1.0), hi=["RAFALE"])
B = dict(name="TYPHOON", short="TYPHOON", color=(1.0, 0.42, 0.15), hi=["TYPHOON", "EUROFIGHTER"])
FLIP = {"b_side": True}
SCENES = [
    dict(type='hook', score=(0, 0), kicker="LE DUEL EUROPÉEN",
         say="Rafale contre Eurofighter Typhoon. Le duel européen. Cinq rounds, un seul vainqueur.",
         show="Rafale contre Eurofighter Typhoon. Le duel européen. 5 rounds, un seul vainqueur."),
    dict(type='bars', score=(0, 1), round="ROUND 1", title="LA VITESSE", a=1.8, b=2.0, max=2.4, fmt="MACH {:.1f}",
         say="Round un : la vitesse. Le Typhoon pointe à Mach deux. Le Rafale, Mach un virgule huit. Point Typhoon.",
         show="Round 1 : la vitesse. Le Typhoon pointe à Mach 2. Le Rafale, Mach 1,8. Point Typhoon."),
    dict(type='bars', score=(0, 2), round="ROUND 2", title="LA PUISSANCE", a=75, b=90, max=105, fmt="{:.0f} kN", race=False,
         pill="POUSSÉE PAR MOTEUR, POSTCOMBUSTION",
         say="Round deux : la puissance. Chaque moteur du Typhoon pousse quatre-vingt-dix kilonewtons. Ceux du Rafale, soixante-quinze. Encore le Typhoon.",
         show="Round 2 : la puissance. Chaque moteur du Typhoon pousse 90 kilonewtons. Ceux du Rafale, 75. Encore le Typhoon."),
    dict(type='chips', score=(1, 2), round="ROUND 3", title="LA POLYVALENCE", side='A',
         chips=["PORTE-AVIONS", "NUCLÉAIRE", "FRAPPE AU SOL", "COMBAT AÉRIEN"], other="TOUJOURS À TERRE",
         say="Round trois : la polyvalence. Le Rafale se pose sur un porte-avions et porte l'arme nucléaire française. Le Typhoon, lui, reste à terre. Point Rafale.",
         show="Round 3 : la polyvalence. Le Rafale se pose sur un porte-avions et porte l'arme nucléaire française. Le Typhoon, lui, reste à terre. Point Rafale."),
    dict(type='counters', score=(2, 2), round="ROUND 4", title="L'EXPORT", a_num=320, b_num=170, pre="≈ ",
         a_sub="AVIONS · 8 PAYS", b_sub="AVIONS · 6 PAYS", pill="COMMANDES HORS PAYS CONSTRUCTEURS",
         say="Round quatre : l'export. Le Rafale a convaincu huit pays étrangers, plus de trois cents avions commandés. Le Typhoon : six pays, environ cent soixante-dix. Deux partout.",
         show="Round 4 : l'export. Le Rafale a convaincu 8 pays étrangers, plus de 300 avions commandés. Le Typhoon : 6 pays, environ 170. 2 partout."),
    dict(type='list', score=(3, 2), round="ROUND 5", title="LE COMBAT",
         a_items=["AFGHANISTAN 2007", "LIBYE", "MALI", "IRAK · SYRIE"], b_items=["LIBYE 2011", "IRAK · SYRIE", "YÉMEN"],
         say="Dernier round : le combat. Le Rafale frappe dès deux mille sept en Afghanistan, puis en Libye, au Mali, en Irak et en Syrie. Le Typhoon débute en Libye en deux mille onze. Plus d'expérience : point Rafale.",
         show="Dernier round : le combat. Le Rafale frappe dès 2007 en Afghanistan, puis en Libye, au Mali, en Irak et en Syrie. Le Typhoon débute en Libye en 2011. Plus d'expérience : point Rafale."),
    dict(type='verdict', score=(3, 2), lines=[("PLUS PUISSANT", 'B'), ("PLUS COMPLET", 'A')],
         say="Verdict : le Typhoon est plus rapide et plus puissant. Mais le Rafale fait tout, même depuis un porte-avions. Trois à deux pour le Rafale. Et toi, tu mets qui ? Dis-le en commentaire.",
         show="Verdict : le Typhoon est plus rapide et plus puissant. Mais le Rafale fait tout, même depuis un porte-avions. 3 à 2 pour le Rafale. Et toi, tu mets qui ? Dis-le en commentaire."),
]
