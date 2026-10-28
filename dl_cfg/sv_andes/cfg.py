# SURVIVRAIS-TU ? : le crash des Andes, vol 571 de la Fuerza Aérea Uruguaya (13/10/1972), l'histoire du film « Le Cercle des neiges » (Netflix, 2023).
# Sources : Wikipedia EN « Uruguayan Air Force Flight 571 » [Fairchild FH-227D T-571 ; Mendoza -> Santiago ; 45 à bord (40 passagers + 5 équipage) dont 19
# joueurs de l'Old Christians Club avec familles et amis ; pilote se croyant après Curicó, descente dans les nuages ; crête : « both wings and the tail cone »
# arrachés ; fuselage glisse 725 m sur le glacier ; site ~3 660 m, Glaciar de las Lágrimas (Argentine) ; pas de vêtements chauds ni équipement ni nourriture ;
# nuits jusqu'à -30 °C ; 11e jour : radio à transistors -> recherches abandonnées ; survivre en se nourrissant des corps des morts ; avalanche vers minuit
# le 29/10, 8 morts ; Parrado et Canessa ~60 km en 10 jours (The Guardian) ; arriero chilien Sergio Catalán ; hélicoptères 22-23/12 ; 29 morts, 16 survivants] ;
# Britannica [45 à bord, 16 survivants]. Avion 3D : FlightGear Fokker 50 (même famille que le F27/FH-227), livrée blanche neutre. Ton respectueux, rien de graphique.
SERIES = "SURVIVRAIS-TU ?"; EP = "08"; MODE = "survie"; STYLE = "cinema"
SCENES = [
    dict(type='aw_hook', title="SURVIVRAIS-TU ?", focus=(540, 900),
         say="Ton avion s'écrase dans les Andes, à plus de trois mille six cents mètres. Personne ne viendra te chercher. Survivrais-tu soixante-douze jours ?",
         show="Ton avion s'écrase dans les Andes, à plus de 3 600 mètres. Personne ne viendra te chercher. Survivrais-tu 72 jours ?"),
    dict(type='aw_real', title="HISTOIRE VRAIE", focus=(540, 900),
         say="C'est l'histoire vraie du film Le Cercle des neiges. Le treize octobre mille neuf cent soixante-douze, un avion uruguayen emmène une équipe de rugby au Chili : quarante-cinq personnes à bord.",
         show="C'est l'histoire vraie du film « Le Cercle des neiges ». Le 13 octobre 1972, un avion uruguayen emmène une équipe de rugby au Chili : 45 personnes à bord."),
    dict(type='aw_crash', title="L'IMPACT", focus=(540, 900),
         say="Dans les nuages, le pilote se croit déjà sorti des montagnes, et descend. L'avion percute une crête, perd ses ailes et sa queue, et le fuselage glisse sur le glacier.",
         show="Dans les nuages, le pilote se croit déjà sorti des montagnes, et descend. L'avion percute une crête, perd ses ailes et sa queue, et le fuselage glisse sur le glacier."),
    dict(type='aw_cold', title="−30 °C", focus=(540, 900),
         say="Les survivants n'ont ni vêtements chauds, ni équipement, ni nourriture. La nuit, il fait jusqu'à moins trente degrés.",
         show="Les survivants n'ont ni vêtements chauds, ni équipement, ni nourriture. La nuit, il fait jusqu'à -30 °C."),
    dict(type='aw_radio', title="JOUR 11", focus=(540, 900),
         say="Le onzième jour, une petite radio leur apprend la pire nouvelle. Les recherches sont abandonnées.",
         show="Le onzième jour, une petite radio leur apprend la pire nouvelle. Les recherches sont abandonnées."),
    dict(type='aw_decide', title="LA DÉCISION", focus=(540, 900),
         say="Pour ne pas mourir de faim, ils prennent une décision terrible : se nourrir des corps de leurs amis disparus.",
         show="Pour ne pas mourir de faim, ils prennent une décision terrible : se nourrir des corps de leurs amis disparus."),
    dict(type='aw_aval', title="29 OCTOBRE", focus=(540, 900),
         say="Le vingt-neuf octobre, il y a cinquante-quatre ans jour pour jour, une avalanche ensevelit l'épave pendant la nuit. Huit personnes meurent.",
         show="Le 29 octobre, il y a 54 ans jour pour jour, une avalanche ensevelit l'épave pendant la nuit. Huit personnes meurent."),
    dict(type='aw_trek', title="10 JOURS DE MARCHE", focus=(540, 900),
         say="Alors deux d'entre eux, Nando Parrado et Roberto Canessa, partent à pied vers le Chili. Après dix jours de marche dans les montagnes, ils croisent un muletier chilien, Sergio Catalán.",
         show="Alors deux d'entre eux, Nando Parrado et Roberto Canessa, partent à pied vers le Chili. Après dix jours de marche dans les montagnes, ils croisent un muletier chilien, Sergio Catalán."),
    dict(type='aw_verdict', title="VERDICT", focus=(540, 900),
         say="Verdict : seize survivants, secourus en hélicoptère après soixante-douze jours. Vingt-neuf personnes n'ont pas survécu. Et toi, tu aurais tenu ?",
         show="Verdict : 16 survivants, secourus en hélicoptère après 72 jours. 29 personnes n'ont pas survécu. Et toi, tu aurais tenu ?"),
]
END_HOLD = 10.0
RECAP_DELAY = 3.0
RECAP = [("3 660 M", "l'altitude de l'épave", (1, 0.85, 0.25)), ("72 JOURS", "dans la neige", (0.55, 0.85, 1.0)), ("16", "survivants", (0.4, 1, 0.6))]
RECAP_NOTE = "En mémoire des 29 victimes du vol 571"
