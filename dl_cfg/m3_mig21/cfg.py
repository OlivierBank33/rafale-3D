# Duel : Mirage III vs MiG-21 (sources : migflug Mirage III [1er vol 17/11/1956, ~1 400 Mirage III/5/50, Mach 2,2, 2 canons DEFA 30 mm 125 obus,
# ~21 pays] ; HistoryNet (Mirage III vs MiG-21, Osprey) : pilotes de Shahak revendiquent 23 MiG-21 entre le 14/07/1966 et le 10/06/1967 ;
# Wikipedia MiG-21 [11 496 construits, ~60 pays, Mach 2,05] ; MiG-21F-13 : 1 canon NR-30, MiG-21PF/FL : aucun canon)
import math
A = dict(name="MIRAGE III", short="MIRAGE", color=(0.20, 0.50, 1.0), hi=["MIRAGE"])
B = dict(name="MIG-21", short="MIG-21", color=(1.0, 0.25, 0.22), hi=["MIG-21", "MIG"])
FLIP = {"a_34": True, "a_side": True, "b_side": True}
TOPROT = {"a_top": math.pi, "b_top": math.pi}
SCENES = [
    dict(type='hook', score=(0, 0), kicker="FRANCE CONTRE URSS",
         say="Mirage trois contre MiG vingt et un. La France contre l'URSS, les deux stars de la guerre froide. Cinq rounds, un seul vainqueur.",
         show="Mirage III contre MiG-21. La France contre l'URSS, les deux stars de la guerre froide. 5 rounds, un seul vainqueur."),
    dict(type='bars', score=(1, 0), round="ROUND 1", title="LA VITESSE", a=2.2, b=2.0, max=2.6, fmt="MACH {:.1f}", a_first=True,
         say="Round un : la vitesse. Le Mirage monte à Mach deux virgule deux. Le MiG, un peu plus de Mach deux. Point Mirage.",
         show="Round 1 : la vitesse. Le Mirage monte à Mach 2,2. Le MiG, un peu plus de Mach 2. Point Mirage."),
    dict(type='counters', score=(1, 1), round="ROUND 2", title="LA PRODUCTION", a_num=1400, b_num=11496, pre="",
         a_sub="MIRAGE III ET DÉRIVÉS", b_sub="MIG-21 CONSTRUITS", pill="LE SUPERSONIQUE LE PLUS PRODUIT DE L'HISTOIRE",
         say="Round deux : la production. Environ mille quatre cents Mirage, avec ses dérivés. Plus de onze mille MiG vingt et un. Point MiG.",
         show="Round 2 : la production. Environ 1 400 Mirage, avec ses dérivés. Plus de 11 000 MiG-21. Point MiG."),
    dict(type='chips', score=(2, 1), round="ROUND 3", title="FACE À FACE", side='A',
         chips=["23 MIG-21 REVENDIQUÉS", "1966 – 1967", "GUERRE DES SIX JOURS"], other="BATTU EN 1967", other_grey=True,
         say="Round trois : le face à face. Entre mille neuf cent soixante-six et la guerre des Six Jours, les pilotes israéliens sur Mirage revendiquent vingt-trois MiG vingt et un abattus. Point Mirage.",
         show="Round 3 : le face à face. Entre 1966 et la guerre des Six Jours, les pilotes israéliens sur Mirage revendiquent 23 MiG-21 abattus. Point Mirage."),
    dict(type='list', score=(2, 2), round="ROUND 4", title="L'EXPORT",
         a_items=["ISRAËL", "PAKISTAN", "AFRIQUE DU SUD", "+ 18 AUTRES"], b_items=["INDE", "VIETNAM", "ÉGYPTE", "+ 50 AUTRES"],
         say="Round quatre : l'export. Le Mirage a volé dans une vingtaine de pays. Le MiG, dans une soixantaine. Deux partout.",
         show="Round 4 : l'export. Le Mirage a volé dans une vingtaine de pays. Le MiG, dans une soixantaine. 2 partout."),
    dict(type='chips', score=(3, 2), round="ROUND 5", title="LES CANONS", side='A',
         chips=["2 CANONS DE 30 MM", "125 OBUS CHACUN"], other="1 CANON… OU AUCUN", other_grey=True,
         say="Dernier round : les canons. Le Mirage en a deux, de trente millimètres. Le MiG de mille neuf cent soixante-sept, un seul, et certaines versions aucun. Point Mirage.",
         show="Dernier round : les canons. Le Mirage en a deux, de 30 mm. Le MiG de 1967, un seul, et certaines versions aucun. Point Mirage."),
    dict(type='verdict', score=(3, 2), lines=[("GAGNANT EN FACE À FACE", 'A'), ("LÉGENDE PRODUITE EN MASSE", 'B')],
         say="Verdict : trois à deux pour le Mirage. Le MiG vingt et un reste la légende produite en masse. Mais en face à face, c'est le Mirage qui a marqué l'histoire. Et toi, tu mets qui ?",
         show="Verdict : 3 à 2 pour le Mirage. Le MiG-21 reste la légende produite en masse. Mais en face à face, c'est le Mirage qui a marqué l'histoire. Et toi, tu mets qui ?"),
]
END_HOLD = 10.6
