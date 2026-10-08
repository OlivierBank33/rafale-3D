# Duel : Mirage 2000 vs F-16 (sources : Wikipedia Mirage 2000 [1er vol 10/03/1978, 601 construits, ~10 pays] ; Wikipedia F-16 [1er vol 1974,
# 4 604 construits, USA + 25 pays] ; globalmilitary.net : Mirage 2000 Mach 2,2 (2 336 km/h), plafond 18 300 m (17 060 m selon d'autres sources),
# F-16 2 178 km/h (> Mach 2), plafond 15 240 m ; autonomie convoyage F-16 ~4 200 km vs Mirage 2000 ~3 300 km ; Taïwan utilise les deux)
import math
A = dict(name="MIRAGE 2000", short="MIRAGE", color=(0.20, 0.50, 1.0), hi=["MIRAGE"])
B = dict(name="F-16", short="F-16", color=(1.0, 0.25, 0.22), hi=["F-16"])
FLIP = {"a_34": True, "a_side": True}
TOPROT = {"a_top": math.pi, "b_top": math.pi}
SCENES = [
    dict(type='hook', score=(0, 0), kicker="FRANCE CONTRE USA",
         say="Le Mirage deux mille peut-il battre le F-16 ? La France contre l'Amérique. Cinq rounds, un seul vainqueur.",
         show="Le Mirage 2000 peut-il battre le F-16 ? La France contre l'Amérique. 5 rounds, un seul vainqueur."),
    dict(type='bars', score=(1, 0), round="ROUND 1", title="LA VITESSE", a=2.2, b=2.0, max=2.6, fmt="MACH {:.1f}", a_first=True,
         say="Round un : la vitesse. Le Mirage monte à Mach deux virgule deux. Le F-16, un peu plus de Mach deux. Point Mirage.",
         show="Round 1 : la vitesse. Le Mirage monte à Mach 2,2. Le F-16, un peu plus de Mach 2. Point Mirage."),
    dict(type='counters', score=(1, 1), round="ROUND 2", title="LA PRODUCTION", a_num=601, b_num=4604, pre="",
         a_sub="MIRAGE 2000 CONSTRUITS", b_sub="F-16 CONSTRUITS", pill="LE F-16 EST TOUJOURS EN PRODUCTION",
         say="Round deux : la production. Six cents Mirage deux mille. Plus de quatre mille six cents F-16. Point F-16.",
         show="Round 2 : la production. 600 Mirage 2000. Plus de 4 600 F-16. Point F-16."),
    dict(type='bars', score=(2, 1), round="ROUND 3", title="LE PLAFOND", a=17, b=15, max=20, fmt="{:.0f} KM", a_first=True,
         pill="ALTITUDE MAXIMALE",
         say="Round trois : l'altitude. Grâce à son aile delta, le Mirage monte à plus de dix-sept kilomètres. Le F-16, environ quinze. Point Mirage.",
         show="Round 3 : l'altitude. Grâce à son aile delta, le Mirage monte à plus de 17 km. Le F-16, environ 15. Point Mirage."),
    dict(type='list', score=(2, 2), round="ROUND 4", title="L'EXPORT",
         a_items=["INDE", "ÉMIRATS", "TAÏWAN", "GRÈCE"], b_items=["ISRAËL", "TURQUIE", "ÉGYPTE", "+ 22 AUTRES"],
         say="Round quatre : l'export. Le Mirage a convaincu une dizaine de pays. Le F-16, plus de vingt-cinq. Deux partout.",
         show="Round 4 : l'export. Le Mirage a convaincu une dizaine de pays. Le F-16, plus de 25. 2 partout."),
    dict(type='bars', score=(2, 3), round="ROUND 5", title="L'AUTONOMIE", a=3300, b=4200, max=5000, fmt="{:.0f} KM", race=False, a_first=True,
         pill="DISTANCE MAX AVEC RÉSERVOIRS",
         say="Dernier round : l'autonomie. Avec ses réservoirs, le Mirage parcourt environ trois mille trois cents kilomètres. Le F-16, plus de quatre mille. Point F-16.",
         show="Dernier round : l'autonomie. Avec ses réservoirs, le Mirage parcourt environ 3 300 km. Le F-16, plus de 4 000. Point F-16."),
    dict(type='verdict', score=(2, 3), lines=[("PLUS VITE, PLUS HAUT", 'A'), ("PLUS LOIN, PARTOUT", 'B')],
         say="Verdict : trois à deux pour le F-16. Le Mirage va plus vite et plus haut. Le F-16 va plus loin et s'est vendu partout. D'ailleurs, Taïwan vole avec les deux. Et toi, tu mets qui ?",
         show="Verdict : 3 à 2 pour le F-16. Le Mirage va plus vite et plus haut. Le F-16 va plus loin et s'est vendu partout. D'ailleurs, Taïwan vole avec les deux. Et toi, tu mets qui ?"),
]
END_HOLD = 12.6
