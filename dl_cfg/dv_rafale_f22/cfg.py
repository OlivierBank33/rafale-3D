# DUEL « tête d'affiche » en style cinéma 3D : Rafale vs F-22, la revanche (1er duel le 02/10 : 161 k vues YouTube).
# Sources : USAF fact sheet F-22 (af.mil, art. 104506) [« Mach two class with supercruise capability », supercroisière > Mach 1,5 sans postcombustion,
# « air dominance », 183 en service (08/2022)] ; production arrêtée fin 2011 après 195 exemplaires (Air & Space Forces Magazine / Wikipedia) ;
# amendement Obey (1998) : exportation du F-22 interdite par la loi américaine ; Dassault Aviation [Rafale Mach 1,8, omnirôle : air-air, air-sol,
# reconnaissance, dissuasion nucléaire ASMP-A, version marine Rafale M sur porte-avions] ; huit pays étrangers clients : Égypte, Qatar, Inde, Grèce,
# Croatie, Émirats arabes unis, Indonésie, Serbie (Shephard 2026 « operated by eight countries », presse 2024 Serbie). Modèles 3D : rafale.glb, fg/F-22.
SERIES = "DUEL"; EP = "01"; MODE = "duel"; STYLE = "cinema"
A = dict(name="RAFALE", color=(0.25, 0.55, 1.0)); B = dict(name="F-22", color=(1.0, 0.3, 0.25))
SCENES = [
    dict(type='dv_hook', title="RAFALE VS F-22", focus=(540, 900), score=(0, 0),
         say="Le Rafale peut-il battre le F vingt-deux ? Le meilleur avion français contre le chasseur le plus craint du monde. Cinq rounds : c'est la revanche.",
         show="Le Rafale peut-il battre le F-22 ? Le meilleur avion français contre le chasseur le plus craint du monde. 5 rounds : c'est la revanche."),
    dict(type='dv_speed', title="ROUND 1", focus=(540, 900), score=(0, 1),
         say="Round un : la vitesse. Le Rafale atteint Mach un virgule huit. Le F vingt-deux dépasse Mach deux, et vole à plus de Mach un virgule cinq sans postcombustion. Point F vingt-deux.",
         show="Round 1 : la vitesse. Le Rafale atteint Mach 1,8. Le F-22 dépasse Mach 2, et vole à plus de Mach 1,5 sans postcombustion. Point F-22."),
    dict(type='dv_stealth', title="ROUND 2", focus=(540, 900), score=(0, 2),
         say="Round deux : la furtivité. Le F vingt-deux a été dessiné pour échapper aux radars, avec ses missiles cachés en soute. Le Rafale est discret, mais pas furtif. Deux à zéro.",
         show="Round 2 : la furtivité. Le F-22 a été dessiné pour échapper aux radars, avec ses missiles cachés en soute. Le Rafale est discret, mais pas furtif. 2 à 0."),
    dict(type='dv_multi', title="ROUND 3", focus=(540, 900), score=(1, 2),
         say="Round trois : la polyvalence. Le Rafale fait tout : combat aérien, frappe au sol, reconnaissance, dissuasion nucléaire, et même porte-avions. Le F vingt-deux est d'abord un chasseur de supériorité aérienne. Point Rafale.",
         show="Round 3 : la polyvalence. Le Rafale fait tout : combat aérien, frappe au sol, reconnaissance, dissuasion nucléaire, et même porte-avions. Le F-22 est d'abord un chasseur de supériorité aérienne. Point Rafale."),
    dict(type='dv_export', title="ROUND 4", focus=(540, 900), score=(2, 2),
         say="Round quatre : l'export. Huit pays étrangers ont commandé le Rafale. Le F vingt-deux, lui, est interdit à l'export par la loi américaine. Deux partout.",
         show="Round 4 : l'export. 8 pays étrangers ont commandé le Rafale. Le F-22, lui, est interdit à l'export par la loi américaine. 2 partout."),
    dict(type='dv_prod', title="ROUND 5", focus=(540, 900), score=(3, 2),
         say="Dernier round : l'avenir. La production du F vingt-deux s'est arrêtée en deux mille onze, après cent quatre-vingt-quinze exemplaires. Le Rafale, lui, est toujours fabriqué. Point Rafale.",
         show="Dernier round : l'avenir. La production du F-22 s'est arrêtée en 2011, après 195 exemplaires. Le Rafale, lui, est toujours fabriqué. Point Rafale."),
    dict(type='dv_verdict', title="VERDICT", focus=(540, 900), score=(3, 2),
         say="Trois à deux pour le Rafale. Mais en combat aérien pur, le F vingt-deux reste le roi du ciel. Et toi, tu mets qui ?",
         show="3 à 2 pour le Rafale. Mais en combat aérien pur, le F-22 reste le roi du ciel. Et toi, tu mets qui ?"),
]
END_HOLD = 9.0
RECAP_DELAY = 1.5
RECAP = [("MACH 2", "le F-22, plus rapide", (1.0, 0.45, 0.4)), ("8 PAYS", "ont commandé le Rafale", (0.45, 0.7, 1.0)), ("3 - 2", "victoire du Rafale", (1, 0.85, 0.25))]
