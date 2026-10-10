# Duel : Blériot XI vs Wright Flyer 1903 (sources : Wikipedia Blériot XI [Manche 25/07/1909 en 36,5 min, Anzani 25 ch, 75,6 km/h, 103 commandes
# fin septembre 1909, gauchissement des ailes, usage militaire 1910-1914] ; Wright Flyer 1903 [17/12/1903 Kitty Hawk, 1er vol 12 s, meilleur vol 59 s / 260 m,
# moteur 12 ch, ~48 km/h de vitesse air, un seul exemplaire, contrôle 3 axes par gauchissement])
import math
A = dict(name="BLÉRIOT XI", short="BLÉRIOT", color=(0.20, 0.50, 1.0), hi=["BLÉRIOT"])
B = dict(name="WRIGHT FLYER", short="WRIGHT", color=(1.0, 0.25, 0.22), hi=["WRIGHT", "FLYER"])
FLIP = {"a_34": True, "a_side": True}
TOPROT = {"a_top": math.pi, "b_top": math.pi}
SCENES = [
    dict(type='hook', score=(0, 0), kicker="LES PIONNIERS",
         say="Blériot onze contre Wright Flyer. La France contre l'Amérique, à l'aube de l'aviation. Cinq rounds, un seul vainqueur.",
         show="Blériot XI contre Wright Flyer. La France contre l'Amérique, à l'aube de l'aviation. 5 rounds, un seul vainqueur."),
    dict(type='chips', score=(0, 1), round="ROUND 1", title="LA PREMIÈRE", side='B',
         chips=["17 DÉCEMBRE 1903", "1ER VOL MOTORISÉ CONTRÔLÉ"], other="6 ANS PLUS TARD", other_grey=True,
         say="Round un : la première. Le dix-sept décembre mille neuf cent trois, le Wright Flyer réalise le premier vol motorisé et contrôlé de l'histoire. Point Wright.",
         show="Round 1 : la première. Le 17 décembre 1903, le Wright Flyer réalise le premier vol motorisé et contrôlé de l'histoire. Point Wright."),
    dict(type='bars', score=(1, 1), round="ROUND 2", title="LA VITESSE", a=75, b=48, max=90, fmt="{:.0f} KM/H", a_first=True,
         say="Round deux : la vitesse. Le Blériot file à environ soixante-quinze kilomètres-heure. Le Flyer, autour de quarante-huit. Point Blériot.",
         show="Round 2 : la vitesse. Le Blériot file à environ 75 km/h. Le Flyer, autour de 48. Point Blériot."),
    dict(type='chips', score=(2, 1), round="ROUND 3", title="LA DISTANCE", side='A',
         chips=["LA MANCHE EN 37 MIN", "25 JUILLET 1909"], other="260 M EN 1903", other_grey=True,
         say="Round trois : la distance. Le meilleur vol du Flyer, ce jour-là : deux cent soixante mètres. Le Blériot, lui, traverse la Manche en trente-sept minutes. Point Blériot.",
         show="Round 3 : la distance. Le meilleur vol du Flyer, ce jour-là : 260 mètres. Le Blériot, lui, traverse la Manche en 37 minutes. Point Blériot."),
    dict(type='chips', score=(2, 2), round="ROUND 4", title="LE PILOTAGE", side='B',
         chips=["CONTRÔLE SUR 3 AXES", "AILES QUI SE TORDENT"], other="MÊME IDÉE", other_grey=True,
         say="Round quatre : le pilotage. Les frères Wright inventent le contrôle sur trois axes, en tordant les ailes. Le Blériot utilise d'ailleurs la même idée. Point Wright. Deux partout.",
         show="Round 4 : le pilotage. Les frères Wright inventent le contrôle sur 3 axes, en tordant les ailes. Le Blériot utilise d'ailleurs la même idée. Point Wright. 2 partout."),
    dict(type='chips', score=(3, 2), round="ROUND 5", title="LE SUCCÈS", side='A',
         chips=["103 COMMANDES EN 2 MOIS", "EN SERVICE EN 1914"], other="1 SEUL EXEMPLAIRE", other_grey=True,
         say="Dernier round : le succès. Après la Manche, Blériot reçoit plus de cent commandes en deux mois. Le Flyer de mille neuf cent trois, lui, n'a existé qu'en un seul exemplaire. Point Blériot.",
         show="Dernier round : le succès. Après la Manche, Blériot reçoit plus de 100 commandes en 2 mois. Le Flyer de 1903, lui, n'a existé qu'en un seul exemplaire. Point Blériot."),
    dict(type='verdict', score=(3, 2), lines=[("LA MANCHE, LE SUCCÈS", 'A'), ("LE TOUT PREMIER", 'B')],
         say="Verdict : trois à deux pour le Blériot. Les Wright ont inventé l'avion. Mais c'est Blériot qui a montré au monde à quoi il pouvait servir. Et toi, tu mets qui ?",
         show="Verdict : 3 à 2 pour le Blériot. Les Wright ont inventé l'avion. Mais c'est Blériot qui a montré au monde à quoi il pouvait servir. Et toi, tu mets qui ?"),
]
END_HOLD = 9.0
