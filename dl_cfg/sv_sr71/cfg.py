# SURVIVRAIS-TU ? : SR-71 qui se désintègre à Mach 3,2 (25 janv. 1966). Sources : The Aviationist (2015) « Bill Weaver… survived his SR-71 disintegration » [SR-71 n° 952,
# Edwards AFB, Mach 3,2, ~78 000 ft ; virage à 35° ; désamorçage d'entrée d'air -> réacteur droit ; roulis + cabré ; manche à fond sans effet ; 2-3 s jusqu'à la dislocation ;
# Weaver évanoui, se croit mort, séparé de l'avion sans éjection ; combinaison pressurisée gonflée + oxygène (évite l'ébullition du sang) ; parachute auto à 15 000 ft ;
# ranch du Nouveau-Mexique (Albert Mitchell) ; Jim Zwayer tué (nuque brisée) pendant la dislocation] ; limite d'Armstrong ≈ 19 km (fluides corporels qui bouillent).
SERIES = "SURVIVRAIS-TU ?"; EP = "06"; MODE = "survie"
SCENES = [
    dict(type='sb_hook', title="SURVIVRAIS-TU ?", focus=(540, 900),
         say="Ton avion se désintègre à plus de trois fois la vitesse du son, à près de vingt-quatre mille mètres. C'est arrivé pour de vrai, en mille neuf cent soixante-six. Survivrais-tu ?",
         show="Ton avion se désintègre à plus de 3 fois la vitesse du son, à près de 24 000 mètres. C'est arrivé pour de vrai, en 1966. Survivrais-tu ?"),
    dict(type='sb_jet', title="SR-71", focus=(540, 900),
         say="L'avion, c'est le SR-71 Blackbird, l'avion à réaction piloté le plus rapide de l'histoire. Aux commandes, Bill Weaver. Derrière lui, l'ingénieur Jim Zwayer.",
         show="L'avion, c'est le SR-71 Blackbird, l'avion à réaction piloté le plus rapide de l'histoire. Aux commandes, Bill Weaver. Derrière lui, l'ingénieur Jim Zwayer."),
    dict(type='sb_unstart', title="MACH 3,2", focus=(540, 900),
         say="Ils volent à Mach trois virgule deux. En plein virage, une entrée d'air se dérègle, et le réacteur droit s'étouffe. L'avion part en roulis et se cabre.",
         show="Ils volent à Mach 3,2. En plein virage, une entrée d'air se dérègle, et le réacteur droit s'étouffe. L'avion part en roulis et se cabre."),
    dict(type='sb_break', title="2 SECONDES", focus=(540, 900),
         say="Weaver pousse le manche à fond. Rien ne répond. En deux à trois secondes, l'avion se disloque autour de lui.",
         show="Weaver pousse le manche à fond. Rien ne répond. En 2 à 3 secondes, l'avion se disloque autour de lui."),
    dict(type='sb_out', title="DANS LE VIDE", focus=(540, 900),
         say="Il s'évanouit. Quand il revient à lui, il croit être mort. Puis il comprend : il tombe en plein ciel, arraché de l'avion sans s'être éjecté.",
         show="Il s'évanouit. Quand il revient à lui, il croit être mort. Puis il comprend : il tombe en plein ciel, arraché de l'avion sans s'être éjecté."),
    dict(type='sb_suit', title="LA COMBINAISON", focus=(540, 900),
         say="Ce qui le sauve, c'est sa combinaison pressurisée. Elle se gonfle et lui donne de l'oxygène. Sans elle, à cette altitude, son sang se mettrait à bouillir.",
         show="Ce qui le sauve, c'est sa combinaison pressurisée. Elle se gonfle et lui donne de l'oxygène. Sans elle, à cette altitude, son sang se mettrait à bouillir."),
    dict(type='sb_chute', title="4 500 M", focus=(540, 900),
         say="Son parachute s'ouvre tout seul, vers quatre mille cinq cents mètres. Il se pose dans un ranch du Nouveau-Mexique.",
         show="Son parachute s'ouvre tout seul, vers 4 500 mètres. Il se pose dans un ranch du Nouveau-Mexique."),
    dict(type='sb_verdict', title="VERDICT", focus=(540, 900),
         say="Verdict : Bill Weaver survit. Mais Jim Zwayer, lui, n'a pas survécu à la dislocation. Et toi, tu aurais survécu ?",
         show="Verdict : Bill Weaver survit. Mais Jim Zwayer, lui, n'a pas survécu à la dislocation. Et toi, tu aurais survécu ?"),
]
END_HOLD = 10.0
RECAP_DELAY = 1.5
RECAP = [("MACH 3,2", "au moment de l'accident", (1, 0.85, 0.25)), ("2 À 3 S", "pour que l'avion se disloque", (1.0, 0.3, 0.3)), ("24 000 M", "la chute de Bill Weaver", (0.35, 0.82, 1.0))]
RECAP_NOTE = "En mémoire de Jim Zwayer (1966)"
