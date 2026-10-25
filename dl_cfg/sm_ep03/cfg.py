# TU ES LE PILOTE — ép. 3 (fiction). Votes ép. 2 (YouTube zFWjdWuBaQ8, lus le 25/10 14h via vidIQ) : A ×3 (« A », « À », « A »), B ×1 -> A la plage (vraie majorité, YouTube seul ;
# TikTok/Facebook non lisibles). Réalisme : sable mouillé compact près de l'eau = plus dur (cf. plage-piste de Barra, Écosse, à marée basse) ; volets sortis en approche ;
# moteur arrêté = planeur, pas de remise des gaz ; tenir la vitesse pour ne pas décrocher ; train dans l'eau = risque de capotage ; passer au-dessus = moins de distance restante.
SERIES = "TU ES LE PILOTE"; EP = "03"
VOTES = dict(A=3, B=1, src="VOTES YOUTUBE")
NEXT = dict(A=("L'EAU", "avant eux, peu profonde", "risque : capoter"), B=("AU-DESSUS", "puis la fin de la plage", "risque : les rochers"))
SCENES = [
    dict(type='e3_recap', title="ÉPISODE 3", focus=(540, 900),
         say="Épisode trois. Plus de carburant, ton dernier moteur tousse. Vous avez voté, et vous avez choisi A : la plage, maintenant.",
         show="Épisode 3. Plus de carburant, ton dernier moteur tousse. Vous avez voté, et vous avez choisi A : la plage, maintenant."),
    dict(type='e3_appr', title="LA PLAGE", focus=(540, 950),
         say="Tu vires vers la côte et tu sors les volets. Tu vises le sable mouillé, au bord de l'eau : il est plus dur, les roues s'y enfoncent moins.",
         show="Tu vires vers la côte et tu sors les volets. Tu vises le sable mouillé, au bord de l'eau : il est plus dur, les roues s'y enfoncent moins."),
    dict(type='e3_quit', title="APPROCHE FINALE", focus=(540, 850),
         say="Trois cents mètres. Et là, ton dernier moteur s'arrête. Plus aucun bruit. Juste le vent. Ton avion est devenu un planeur.",
         show="300 mètres. Et là, ton dernier moteur s'arrête. Plus aucun bruit. Juste le vent. Ton avion est devenu un planeur."),
    dict(type='e3_glide', title="UNE SEULE CHANCE", focus=(540, 900),
         say="Pas de remise des gaz possible : tu n'as qu'une seule tentative. Tu gardes ta vitesse, pour ne pas décrocher.",
         show="Pas de remise des gaz possible : tu n'as qu'une seule tentative. Tu gardes ta vitesse, pour ne pas décrocher."),
    dict(type='e3_light', title="LE PHARE", focus=(540, 1000),
         say="Tu allumes ton phare d'atterrissage. Et tu vois des silhouettes. Un feu de camp. Des gens, au milieu de ta plage.",
         show="Tu allumes ton phare d'atterrissage. Et tu vois des silhouettes. Un feu de camp. Des gens, au milieu de ta plage."),
    dict(type='e3_think', title="RÉFLÉCHIS", focus=(540, 900),
         say="Il te reste quelques secondes. Tu peux te poser avant eux, dans l'eau peu profonde. Mais l'eau peut accrocher le train et retourner l'avion. Ou tu passes au-dessus d'eux, et tu te poses après. Mais il ne restera presque plus de plage avant les rochers.",
         show="Il te reste quelques secondes. Tu peux te poser avant eux, dans l'eau peu profonde. Mais l'eau peut accrocher le train et retourner l'avion. Ou tu passes au-dessus d'eux, et tu te poses après. Mais il ne restera presque plus de plage avant les rochers."),
    dict(type='e3_choice', title="TU FAIS QUOI ?", focus=(540, 900),
         say="Alors, tu fais quoi ? A : l'eau, avant eux. B : au-dessus, puis la fin de la plage. Écris A ou B en commentaire. La majorité décide de l'épisode quatre.",
         show="Alors, tu fais quoi ? A : l'eau, avant eux. B : au-dessus, puis la fin de la plage. Écris A ou B en commentaire. La majorité décide de l'épisode 4."),
]
END_HOLD = 13.5
RECAP = [("A : L'EAU", "risque : capoter", (0.35, 0.65, 1.0)), ("B : AU-DESSUS", "risque : les rochers", (1.0, 0.55, 0.12)), ("ÉPISODE 4", "mercredi, 18 h", (0.92, 0.95, 1.0))]
