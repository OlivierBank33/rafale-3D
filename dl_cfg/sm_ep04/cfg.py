# TU ES LE PILOTE — ép. 4 = FINALE (fiction). Votes ép. 3 (YouTube V-AXin5fEm0, lus le 27/10 ~14 h via vidIQ) : A ×5 (« A » ×4, « L'eau »), B ×3,
# 2 commentaires « C sur eux » (blague, hors vote) -> A : l'eau, avant eux (vraie majorité YouTube ; TikTok/Facebook non lisibles).
# Réalisme amerrissage : train rentré (roues dans l'eau = capotage), porte déverrouillée avant l'impact (évite qu'elle se coince), toucher parallèle
# au rivage, au ras de l'eau, le plus lentement possible (arrondi), décélération brutale, harnais.
SERIES = "TU ES LE PILOTE"; EP = "04"; MODE = "serie"
VOTES = dict(A=5, B=3, src="VOTES YOUTUBE")
SCENES = [
    dict(type='e4_recap', title="ÉPISODE 4 · FINAL", focus=(540, 900),
         say="Épisode quatre, le final. Moteur coupé, des gens sur ta plage. Vous avez voté A, à cinq voix contre trois : l'eau, avant eux.",
         show="Épisode 4, le final. Moteur coupé, des gens sur ta plage. Vous avez voté A, à 5 voix contre 3 : l'eau, avant eux."),
    dict(type='e4_gear', title="LE TRAIN", focus=(540, 900),
         say="Tu rentres le train : dans l'eau, des roues sorties peuvent accrocher et retourner l'avion. Et tu déverrouilles ta porte, pour qu'elle ne se coince pas à l'impact.",
         show="Tu rentres le train : dans l'eau, des roues sorties peuvent accrocher et retourner l'avion. Et tu déverrouilles ta porte, pour qu'elle ne se coince pas à l'impact."),
    dict(type='e4_flare', title="AU RAS DE L'EAU", focus=(540, 900),
         say="Tu longes la plage, au ras des vagues. Juste avant de toucher, tu cabres doucement : il faut toucher l'eau le plus lentement possible.",
         show="Tu longes la plage, au ras des vagues. Juste avant de toucher, tu cabres doucement : il faut toucher l'eau le plus lentement possible."),
    dict(type='e4_touch', title="CONTACT", focus=(540, 900),
         say="Premier contact. L'eau freine d'un coup, comme un mur. Ta ceinture te retient.",
         show="Premier contact. L'eau freine d'un coup, comme un mur. Ta ceinture te retient."),
    dict(type='e4_stop', title="ARRÊT", focus=(540, 900),
         say="L'avion glisse, ralentit, et s'arrête à quelques dizaines de mètres des gens. Il ne s'est pas retourné.",
         show="L'avion glisse, ralentit, et s'arrête à quelques dizaines de mètres des gens. Il ne s'est pas retourné."),
    dict(type='e4_out', title="DEHORS", focus=(540, 900),
         say="Tu ouvres la porte, et tu sors, de l'eau jusqu'à la taille. Sur la plage, les gens courent vers toi.",
         show="Tu ouvres la porte, et tu sors, de l'eau jusqu'à la taille. Sur la plage, les gens courent vers toi."),
    dict(type='e4_end', title="FIN", focus=(540, 900),
         say="Tu as survécu, et personne n'a été blessé. C'était le dernier épisode de Tu es le pilote. Merci d'avoir piloté avec nous ! Et toi, tu aurais choisi l'eau aussi ?",
         show="Tu as survécu, et personne n'a été blessé. C'était le dernier épisode de « Tu es le pilote ». Merci d'avoir piloté avec nous ! Et toi, tu aurais choisi l'eau aussi ?"),
]
END_HOLD = 19.5
RECAP_DELAY = 6.0
RECAP = [("TRAIN RENTRÉ", "pour ne pas capoter", (0.35, 0.65, 1.0)), ("PORTE OUVERTE", "avant l'impact", (1.0, 0.55, 0.12)), ("0 BLESSÉ", "fin de la série", (0.4, 1, 0.6))]
