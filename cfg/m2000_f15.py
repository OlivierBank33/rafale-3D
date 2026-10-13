# Duel : Mirage 2000 vs F-15 (sources : Wikipedia Mirage 2000 [Mach 2,2, 601 construits, ~7,5 t à vide, monoréacteur, aile delta + commandes de vol électriques] ;
# Wikipedia F-15 Eagle [Mach 2,5+, ~12,7 t à vide (F-15C), biréacteur, 104 victoires aériennes pour 0 perte en combat aérien, F-15EX toujours produit])
import math
A = dict(name="MIRAGE 2000", short="MIRAGE", color=(0.20, 0.50, 1.0), hi=["MIRAGE"])
B = dict(name="F-15", short="F-15", color=(1.0, 0.25, 0.22), hi=["F-15", "EAGLE"])
FLIP = {"a_34": True, "a_side": True, "b_side": True}
TOPROT = {"a_top": math.pi, "b_top": math.pi}
SCENES = [
    dict(type='hook', score=(0, 0), kicker="LE MIRAGE PEUT-IL BATTRE L'AIGLE ?",
         say="Le Mirage deux mille peut-il battre le F quinze ? La France contre l'Amérique. Cinq rounds, un seul vainqueur.",
         show="Le Mirage 2000 peut-il battre le F-15 ? La France contre l'Amérique. 5 rounds, un seul vainqueur."),
    dict(type='bars', score=(0, 1), round="ROUND 1", title="LA VITESSE", a=2.2, b=2.5, max=2.8, fmt="MACH {:.1f}",
         say="Round un : la vitesse. Le Mirage pointe à Mach deux virgule deux. Le F quinze dépasse Mach deux virgule cinq. Point F quinze.",
         show="Round 1 : la vitesse. Le Mirage pointe à Mach 2,2. Le F-15 dépasse Mach 2,5. Point F-15."),
    dict(type='chips', score=(1, 1), round="ROUND 2", title="LE VIRAGE", side='A',
         chips=["AILE DELTA", "COMMANDES ÉLECTRIQUES", "TRÈS AGILE"], other="PLUS LOURD", other_grey=True,
         say="Round deux : le virage. Aile delta, commandes de vol électriques : le Mirage est un des chasseurs les plus agiles de sa génération. Point Mirage.",
         show="Round 2 : le virage. Aile delta, commandes de vol électriques : le Mirage est un des chasseurs les plus agiles de sa génération. Point Mirage."),
    dict(type='chips', score=(1, 2), round="ROUND 3", title="LE PALMARÈS", side='B',
         chips=["104 VICTOIRES", "JAMAIS ABATTU EN DUEL"], other="PALMARÈS PLUS MODESTE", other_grey=True,
         say="Round trois : le palmarès. Le F quinze compte plus de cent victoires en combat aérien, sans jamais avoir été abattu par un autre avion. Point F quinze.",
         show="Round 3 : le palmarès. Le F-15 compte plus de 100 victoires en combat aérien, sans jamais avoir été abattu par un autre avion. Point F-15."),
    dict(type='bars', score=(2, 2), round="ROUND 4", title="LA DISCRÉTION", a=7.5, b=12.7, max=14, fmt="{:.1f} T", low_wins=True, race=False, a_first=True,
         say="Round quatre : la discrétion. À vide, le Mirage pèse sept tonnes et demie. Le F quinze, presque treize. Plus petit, le Mirage est bien plus dur à repérer à l'œil. Deux partout.",
         show="Round 4 : la discrétion. À vide, le Mirage pèse 7,5 tonnes. Le F-15, presque 13. Plus petit, le Mirage est bien plus dur à repérer à l'œil. 2 partout."),
    dict(type='list', score=(2, 3), round="ROUND 5", title="L'AVENIR",
         a_items=["PRODUCTION ARRÊTÉE", "601 CONSTRUITS"], b_items=["F-15EX", "TOUJOURS PRODUIT"],
         say="Dernier round, la surprise : l'avenir. La chaîne du Mirage s'est arrêtée, après six cent un avions. Le F quinze, lui, est encore fabriqué aujourd'hui, en version EX. Point F quinze.",
         show="Dernier round, la surprise : l'avenir. La chaîne du Mirage s'est arrêtée, après 601 avions. Le F-15, lui, est encore fabriqué aujourd'hui, en version EX. Point F-15."),
    dict(type='verdict', score=(2, 3), lines=[("AGILE, LÉGER, DISCRET", 'A'), ("VITESSE, PALMARÈS, AVENIR", 'B')],
         say="Verdict : trois à deux pour le F quinze. Il est plus rapide, invaincu, et toujours produit. Mais en combat tournoyant, le petit Mirage reste un cauchemar. Et toi, tu mets qui ?",
         show="Verdict : 3 à 2 pour le F-15. Il est plus rapide, invaincu, et toujours produit. Mais en combat tournoyant, le petit Mirage reste un cauchemar. Et toi, tu mets qui ?"),
]
END_HOLD = 9.0
