# LA SCIENCE DU VOL 01 : pourquoi les avions de ligne volent à 11 000 m (atmosphère standard OACI : 11 km, -56,5 °C, densité ≈ 0,36 kg/m³ soit ≈ 30 %
# de la densité au sol (1,225) ; traînée ∝ ½ ρ V² ; rendement des réacteurs meilleur en air froid ; tropopause ≈ 11 km aux latitudes moyennes, la plupart
# des nuages en dessous ; « coffin corner » : vitesse de décrochage et vitesse max se rejoignent en altitude ; montée par paliers (step climb) quand l'avion
# s'allège ; altitude cabine max ≈ 8 000 ft (≈ 2 400 m) ; Concorde en croisière vers 18 000 m à Mach 2)
SERIES = "LA SCIENCE DU VOL"; EP = "01"
SCENES = [
    dict(type='hook', top=("11 000 M", "−56 °C"), sub=("altitude de croisière", "température extérieure"),
         say="Onze mille mètres d'altitude, moins cinquante-six degrés, et trois fois moins d'air qu'au sol. Pourtant, c'est exactement là que ton avion consomme le moins.",
         show="11 000 mètres d'altitude, -56 degrés, et 3 fois moins d'air qu'au sol. Pourtant, c'est exactement là que ton avion consomme le moins."),
    dict(type='plan', items=["L'AIR RARE", "LE FROID", "LA MÉTÉO", "LA LIMITE"],
         say="Pourquoi si haut ? Trois raisons. Et une limite, qu'il ne faut surtout pas dépasser.",
         show="Pourquoi si haut ? Trois raisons. Et une limite, qu'il ne faut surtout pas dépasser."),
    dict(type='air', num=1, title="L'AIR RARE",
         say="Un : l'air rare. À onze mille mètres, l'air est environ trois fois moins dense. Or la traînée, la force qui freine l'avion, dépend directement de la densité de l'air. Moins d'air, moins de frein, moins de carburant.",
         show="1 : l'air rare. À 11 000 mètres, l'air est environ 3 fois moins dense. Or la traînée, la force qui freine l'avion, dépend directement de la densité de l'air. Moins d'air, moins de frein, moins de carburant."),
    dict(type='cold', num=2, title="LE FROID",
         say="Deux : le froid. Un réacteur aspire de l'air pour le comprimer et le brûler. Plus l'air entre froid, meilleur est son rendement. Moins cinquante-six degrés, c'est idéal.",
         show="2 : le froid. Un réacteur aspire de l'air pour le comprimer et le brûler. Plus l'air entre froid, meilleur est son rendement. -56 degrés, c'est idéal."),
    dict(type='weather', num=3, title="LA MÉTÉO",
         say="Trois : la météo. Vers onze mille mètres, on atteint la tropopause. La plupart des nuages, et des turbulences, restent en dessous.",
         show="3 : la météo. Vers 11 000 mètres, on atteint la tropopause. La plupart des nuages, et des turbulences, restent en dessous."),
    dict(type='coffin', num=4, title="LA LIMITE",
         say="Alors pourquoi ne pas monter encore plus haut ? Parce que les ailes ont besoin d'air pour porter. Plus on monte, plus la vitesse de décrochage se rapproche de la vitesse maximale. Les pilotes appellent ça le coin du cercueil.",
         show="Alors pourquoi ne pas monter encore plus haut ? Parce que les ailes ont besoin d'air pour porter. Plus on monte, plus la vitesse de décrochage se rapproche de la vitesse maximale. Les pilotes appellent ça le coin du cercueil."),
    dict(type='steps', num=None, title="PAR PALIERS",
         say="Et au décollage, l'avion est trop lourd pour monter si haut. Il grimpe par paliers, au fur et à mesure qu'il brûle son carburant.",
         show="Et au décollage, l'avion est trop lourd pour monter si haut. Il grimpe par paliers, au fur et à mesure qu'il brûle son carburant."),
    dict(type='cabin', num=None, title="ET TOI ?",
         say="Et toi, dans la cabine ? L'avion est pressurisé : tu respires comme si tu étais à environ deux mille quatre cents mètres. Pas à onze mille.",
         show="Et toi, dans la cabine ? L'avion est pressurisé : tu respires comme si tu étais à environ 2 400 mètres. Pas à 11 000."),
    dict(type='concorde', num=None, title="LE CAS CONCORDE",
         say="Le Concorde, lui, volait vers dix-huit mille mètres. Encore plus haut, encore moins d'air, pour tenir Mach deux.",
         show="Le Concorde, lui, volait vers 18 000 mètres. Encore plus haut, encore moins d'air, pour tenir Mach 2."),
    dict(type='outro', num=None, title="ABONNE-TOI",
         say="L'altitude d'un avion n'est jamais un hasard. Abonne-toi pour la suite de la science du vol.",
         show="L'altitude d'un avion n'est jamais un hasard. Abonne-toi pour la suite de la science du vol."),
]
END_HOLD = 2.5
NEXT = "LE MUR DU SON"
