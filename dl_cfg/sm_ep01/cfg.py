# HISTOIRE INTERACTIVE « TU ES LE PILOTE » — épisode 1 (fiction). Procédures réelles : feu moteur sur bimoteur = réduire, couper l'alimentation (hélice en drapeau),
# tirer la poignée feu, percuter l'extincteur ; vol sur un moteur = plafond réduit, descente lente ; MAYDAY sur 121,5 MHz ; amerrissage de nuit = très risqué.
SERIES = "TU ES LE PILOTE"; EP = "01"
SCENES = [
    dict(type='cockpit', title="MOTEUR EN FEU",
         say="Deux heures du matin. Tu es seul aux commandes de ton bimoteur, au-dessus de l'Atlantique. Tout est calme. Et soudain, une alarme. Ton moteur gauche est en feu.",
         show="2 heures du matin. Tu es seul aux commandes de ton bimoteur, au-dessus de l'Atlantique. Tout est calme. Et soudain, une alarme. Ton moteur gauche est en feu."),
    dict(type='handle', title="RÉFLEXES",
         say="Réflexe. Tu coupes le moteur. Tu tires la poignée feu. L'extincteur se vide. Les flammes s'éteignent.",
         show="Réflexe. Tu coupes le moteur. Tu tires la poignée feu. L'extincteur se vide. Les flammes s'éteignent."),
    dict(type='ocean', title="UN SEUL MOTEUR",
         say="Mais maintenant, tu voles sur un seul moteur. Ton altimètre défile. Trois mille deux cents mètres. Trois mille. Sur un moteur, ton avion ne peut plus tenir cette altitude. Tu descends. Lentement, mais tu descends.",
         show="Mais maintenant, tu voles sur un seul moteur. Ton altimètre défile. 3 200 mètres. 3 000. Sur un moteur, ton avion ne peut plus tenir cette altitude. Tu descends. Lentement, mais tu descends."),
    dict(type='map', title="LE CALCUL",
         say="L'Irlande est à deux cents kilomètres derrière toi. Il te reste environ cinquante minutes de carburant. C'est juste. Très juste.",
         show="L'Irlande est à 200 kilomètres derrière toi. Il te reste environ 50 minutes de carburant. C'est juste. Très juste."),
    dict(type='radio', title="MAYDAY",
         say="Tu lances un Mayday. La radio grésille. Un cargo, à quinze kilomètres. Il peut te repêcher, si tu te poses sur l'eau. De nuit.",
         show="Tu lances un Mayday. La radio grésille. Un cargo, à 15 kilomètres. Il peut te repêcher, si tu te poses sur l'eau. De nuit."),
    dict(type='think', title="RÉFLÉCHIS",
         say="Le demi-tour ? Tu restes en l'air. Mais si le carburant manque, tu tomberas à l'eau quand même, loin de tout secours. Le cargo ? Il est là, maintenant. Mais se poser sur la mer, de nuit, avec des vagues de deux mètres, c'est le moment le plus dangereux de ta vie de pilote.",
         show="Le demi-tour ? Tu restes en l'air. Mais si le carburant manque, tu tomberas à l'eau quand même, loin de tout secours. Le cargo ? Il est là, maintenant. Mais se poser sur la mer, de nuit, avec des vagues de 2 mètres, c'est le moment le plus dangereux de ta vie de pilote."),
    dict(type='choice', title="TU FAIS QUOI ?",
         say="Alors, tu fais quoi ? A : demi-tour vers l'Irlande. B : te poser près du cargo. Écris A ou B en commentaire. La majorité décide de l'épisode deux.",
         show="Alors, tu fais quoi ? A : demi-tour vers l'Irlande. B : te poser près du cargo. Écris A ou B en commentaire. La majorité décide de l'épisode 2."),
]
END_HOLD = 7.0
