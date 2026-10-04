# Duel : F-16 vs MiG-21 (sources : Wikipedia MiG-21 [11 496 construits, ~60 pays, 1er vol 1955], Lockheed Martin [4 600e F-16 en 2024, ~25-28 pays], retrait indien 26/09/2025, Bekaa 1982 = revendication israélienne)
import math
A = dict(name="F-16", short="F-16", color=(0.25, 0.55, 1.0), hi=["F-16"])
B = dict(name="MIG-21", short="MIG-21", color=(1.0, 0.25, 0.22), hi=["MIG-21", "MIG"])
FLIP = {"a_34": True, "a_side": True, "b_side": True}
TOPROT = {"a_top": math.pi, "b_top": math.pi}
SCENES = [
    dict(type='hook', score=(0, 0), kicker="GUERRE FROIDE",
         say="F-16 contre MiG-21. L'Amérique contre l'URSS. Cinq rounds, un seul vainqueur.",
         show="F-16 contre MiG-21. L'Amérique contre l'URSS. 5 rounds, un seul vainqueur."),
    dict(type='bars', score=(0, 0), round="ROUND 1", title="LA VITESSE", a=2.0, b=2.0, max=2.4, fmt="MACH {:.1f}", a_first=True,
         pill="LES DEUX DÉPASSENT MACH 2",
         say="Round un : la vitesse. Les deux dépassent Mach deux. Égalité parfaite.",
         show="Round 1 : la vitesse. Les deux dépassent Mach 2. Égalité parfaite."),
    dict(type='counters', score=(0, 1), round="ROUND 2", title="LA PRODUCTION", a_num=4600, b_num=11496, pre="",
         a_sub="F-16 CONSTRUITS", b_sub="MIG-21 CONSTRUITS", pill="LE SUPERSONIQUE LE PLUS PRODUIT DE L'HISTOIRE",
         say="Round deux : la production. Plus de quatre mille six cents F-16. Mais plus de onze mille MiG-21 : le supersonique le plus produit de l'histoire. Point MiG.",
         show="Round 2 : la production. Plus de 4 600 F-16. Mais plus de 11 000 MiG-21 : le supersonique le plus produit de l'histoire. Point MiG."),
    dict(type='chips', score=(1, 1), round="ROUND 3", title="LA TECHNOLOGIE", side='A',
         chips=["COMMANDES ÉLECTRIQUES", "MANCHE LATÉRAL", "9 G", "VERRIÈRE BULLE"], other="SIMPLE ET ROBUSTE", other_grey=True,
         say="Round trois : la technologie. Le F-16 a des commandes de vol électriques, un manche sur le côté, et encaisse neuf G. Le MiG mise sur la simplicité. Point F-16.",
         show="Round 3 : la technologie. Le F-16 a des commandes de vol électriques, un manche sur le côté, et encaisse 9 G. Le MiG mise sur la simplicité. Point F-16."),
    dict(type='list', score=(2, 1), round="ROUND 4", title="LE COMBAT",
         a_items=["LIBAN 1982", "IRAK 1991", "BALKANS"], b_items=["VIETNAM", "INDE-PAKISTAN", "PROCHE-ORIENT"],
         say="Round quatre : le combat. En mille neuf cent quatre-vingt-deux, au Liban, les F-15 et F-16 israéliens revendiquent plus de quatre-vingts avions syriens abattus, sans aucune perte en combat aérien. Point F-16.",
         show="Round 4 : le combat. En 1982, au Liban, les F-15 et F-16 israéliens revendiquent plus de 80 avions syriens abattus, sans aucune perte en combat aérien. Point F-16."),
    dict(type='counters', score=(2, 2), round="ROUND 5", title="LA LONGÉVITÉ", a_num=1974, b_num=1955, pre="", static=True,
         a_sub="1ER VOL · TOUJOURS PRODUIT", b_sub="1ER VOL · RETIRÉ PAR L'INDE EN 2025", a_start=0.5, b_start=0.15,
         say="Round cinq : la longévité. Le MiG vole depuis mille neuf cent cinquante-cinq. L'Inde l'a retiré en deux mille vingt-cinq, après soixante-deux ans de service. Deux partout.",
         show="Round 5 : la longévité. Le MiG vole depuis 1955. L'Inde l'a retiré en 2025, après 62 ans de service. 2 partout."),
    dict(type='verdict', score=(2, 2), lines=[("PLUS MODERNE", 'A'), ("PLUS LÉGENDAIRE", 'B')],
         say="Verdict : le F-16 est plus moderne et redoutable au combat. Le MiG-21 est une légende produite en masse. Deux partout. À toi de les départager en commentaire.",
         show="Verdict : le F-16 est plus moderne et redoutable au combat. Le MiG-21 est une légende produite en masse. 2 partout. À toi de les départager en commentaire."),
]
END_HOLD = 7.0
