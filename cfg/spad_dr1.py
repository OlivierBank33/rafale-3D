# Duel : SPAD VII vs Fokker Dr.I (sources : Wikipedia SPAD S.VII [193 km/h, Hispano-Suiza 150-180 ch, ~6 000 construits (estimations 3 825 à 5 600 en France
# + 220 au R.-U. + ~100 en Russie), robuste, piqué sûr jusqu'à 400 km/h, Guynemer, 1 mitrailleuse, peu maniable] ;
# Wikipedia Fokker Dr.I [180 km/h, rotatif Oberursel 110 ch, 320 construits, très maniable, excellente montée initiale, 17 dernières victoires de
# Richthofen sur Dr.I (+2 sur F.I), ruptures d'ailes fin oct. 1917, interdiction de vol du 2 au 28 nov. 1917, plus lent que les chasseurs alliés])
import math
A = dict(name="SPAD VII", short="SPAD", color=(0.20, 0.50, 1.0), hi=["SPAD", "GUYNEMER"])
B = dict(name="FOKKER DR.I", short="FOKKER", color=(1.0, 0.25, 0.22), hi=["FOKKER", "TRIPLAN", "RICHTHOFEN", "BARON"])
FLIP = {"a_34": True, "a_side": True, "b_side": True}
TOPROT = {"a_top": math.pi, "b_top": math.pi}
SCENES = [
    dict(type='hook', score=(0, 0), kicker="LE SPAD BAT-IL LE BARON ROUGE ?",
         say="Le SPAD de Guynemer peut-il battre le triplan du Baron rouge ? SPAD sept contre Fokker D R un. Cinq rounds, un seul vainqueur.",
         show="Le SPAD de Guynemer peut-il battre le triplan du Baron rouge ? SPAD VII contre Fokker Dr.I. 5 rounds, un seul vainqueur."),
    dict(type='chips', score=(0, 1), round="ROUND 1", title="LE VIRAGE", side='B',
         chips=["3 AILES", "TOURNE TRÈS SERRÉ", "MONTÉE EXPLOSIVE"], other="LOURD AUX COMMANDES", other_grey=True,
         say="Round un : le virage. Avec ses trois ailes, le Fokker tourne plus serré que tout le monde, et grimpe comme une flèche. Le SPAD, lui, est lourd aux commandes. Point Fokker.",
         show="Round 1 : le virage. Avec ses 3 ailes, le Fokker tourne plus serré que tout le monde, et grimpe comme une flèche. Le SPAD, lui, est lourd aux commandes. Point Fokker."),
    dict(type='bars', score=(1, 1), round="ROUND 2", title="LA VITESSE", a=193, b=180, max=220, fmt="{:.0f} KM/H", a_first=True,
         say="Round deux : la vitesse. Le SPAD file à cent quatre-vingt-treize kilomètres-heure. Le Fokker, cent quatre-vingts. En piqué, le SPAD le distance encore plus. Point SPAD.",
         show="Round 2 : la vitesse. Le SPAD file à 193 km/h. Le Fokker, 180. En piqué, le SPAD le distance encore plus. Point SPAD."),
    dict(type='chips', score=(1, 2), round="ROUND 3", title="LA LÉGENDE", side='B',
         chips=["LE BARON ROUGE", "80 VICTOIRES", "17 SUR CE TRIPLAN"], other="GUYNEMER : 53", other_grey=True,
         say="Round trois : la légende. Le Baron rouge, quatre-vingts victoires, dont ses dix-sept dernières sur ce triplan. Guynemer en compte cinquante-trois. Point Fokker.",
         show="Round 3 : la légende. Le Baron rouge, 80 victoires, dont ses 17 dernières sur ce triplan. Guynemer en compte 53. Point Fokker."),
    dict(type='counters', score=(2, 2), round="ROUND 4", title="LE NOMBRE", a_num=6000, b_num=320, pre="",
         a_sub="SPAD VII · ENVIRON", b_sub="FOKKER DR.I CONSTRUITS", pill="LE SPAD ÉQUIPE TOUS LES ALLIÉS",
         say="Round quatre : le nombre. Environ six mille SPAD construits, pour les Français, les Anglais, les Russes. Seulement trois cent vingt Fokker. Deux partout.",
         show="Round 4 : le nombre. Environ 6 000 SPAD construits, pour les Français, les Anglais, les Russes. Seulement 320 Fokker. 2 partout."),
    dict(type='list', score=(3, 2), round="ROUND 5", title="LA SOLIDITÉ",
         a_items=["PIQUÉ SÛR À 400 KM/H", "INCASSABLE"], b_items=["AILES QUI CASSENT", "INTERDIT DE VOL EN 1917"],
         say="Dernier round, la surprise : la solidité. En mille neuf cent dix-sept, des ailes de Fokker cassent en plein vol. Tous les triplans sont interdits de vol. Le SPAD, lui, encaisse des piqués à quatre cents kilomètres-heure. Point SPAD.",
         show="Dernier round, la surprise : la solidité. En 1917, des ailes de Fokker cassent en plein vol. Tous les triplans sont interdits de vol. Le SPAD, lui, encaisse des piqués à 400 km/h. Point SPAD."),
    dict(type='verdict', score=(3, 2), lines=[("VITESSE, NOMBRE, SOLIDITÉ", 'A'), ("VIRAGE, LÉGENDE", 'B')],
         say="Verdict : trois à deux pour le SPAD. Le Fokker avait le virage et le Baron rouge. Mais le SPAD était plus rapide, plus solide, et partout dans le ciel. Et toi, tu mets qui ?",
         show="Verdict : 3 à 2 pour le SPAD. Le Fokker avait le virage et le Baron rouge. Mais le SPAD était plus rapide, plus solide, et partout dans le ciel. Et toi, tu mets qui ?"),
]
END_HOLD = 9.0
