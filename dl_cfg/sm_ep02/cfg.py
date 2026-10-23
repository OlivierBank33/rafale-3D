# TU ES LE PILOTE — ép. 2 (fiction). Aucun vote lisible (0 commentaire YouTube au 23/10) -> le pilote tranche : A demi-tour. Pas de fausse « majorité ».
# Réalisme : sur un moteur, virage = perte d'altitude ; alarme carburant bas ; Shannon (côte ouest Irlande) ; moteur qui tousse = alimentation qui se désamorce ; posé sur plage de nuit = risque de capotage.
SERIES = "TU ES LE PILOTE"; EP = "02"
NEXT = dict(A=("LA PLAGE", "maintenant, de nuit", "risque : capoter"), B=("LA PISTE", "12 min, 1 moteur qui tousse", "risque : tomber en mer"))
SCENES = [
    dict(type='e2_recap', title="ÉPISODE 2",
         say="Épisode deux. Moteur en feu, au milieu de l'Atlantique. Pas assez de votes pour trancher, alors le pilote a choisi : demi-tour vers l'Irlande.",
         show="Épisode 2. Moteur en feu, au milieu de l'Atlantique. Pas assez de votes pour trancher, alors le pilote a choisi : demi-tour vers l'Irlande."),
    dict(type='e2_turn', title="DEMI-TOUR",
         say="Tu vires lentement. Sur un seul moteur, chaque virage te fait perdre de l'altitude. Le cargo disparaît derrière toi. Plus de retour possible.",
         show="Tu vires lentement. Sur un seul moteur, chaque virage te fait perdre de l'altitude. Le cargo disparaît derrière toi. Plus de retour possible."),
    dict(type='e2_fuel', title="CARBURANT",
         say="Trente minutes plus tard, l'alarme carburant s'allume. La jauge est dans le rouge. Et l'Irlande est encore à quarante kilomètres.",
         show="30 minutes plus tard, l'alarme carburant s'allume. La jauge est dans le rouge. Et l'Irlande est encore à 40 kilomètres."),
    dict(type='e2_coast', title="LA CÔTE",
         say="Et soudain, des lumières. La côte. Le contrôleur de Shannon te donne une piste. Il te faut encore douze minutes.",
         show="Et soudain, des lumières. La côte. Le contrôleur de Shannon te donne une piste. Il te faut encore 12 minutes."),
    dict(type='e2_cough', title="LE MOTEUR TOUSSE",
         say="Puis ton dernier moteur tousse. Une fois. Deux fois. Le carburant n'arrive plus correctement. Le moteur repart, mais pour combien de temps ?",
         show="Puis ton dernier moteur tousse. Une fois. Deux fois. Le carburant n'arrive plus correctement. Le moteur repart, mais pour combien de temps ?"),
    dict(type='e2_think', title="RÉFLÉCHIS",
         say="Sous toi, une longue plage, éclairée par la lune. Tu peux t'y poser maintenant. Mais du sable mou, de nuit, peut retourner l'avion. Ou tu tentes la piste, à douze minutes. Si le moteur s'arrête avant, tu tombes dans la mer.",
         show="Sous toi, une longue plage, éclairée par la lune. Tu peux t'y poser maintenant. Mais du sable mou, de nuit, peut retourner l'avion. Ou tu tentes la piste, à 12 minutes. Si le moteur s'arrête avant, tu tombes dans la mer."),
    dict(type='e2_choice', title="TU FAIS QUOI ?",
         say="Alors, tu fais quoi ? A : la plage, maintenant. B : la piste de Shannon. Écris A ou B en commentaire. La majorité décide de l'épisode trois.",
         show="Alors, tu fais quoi ? A : la plage, maintenant. B : la piste de Shannon. Écris A ou B en commentaire. La majorité décide de l'épisode 3."),
]
END_HOLD = 12.5
