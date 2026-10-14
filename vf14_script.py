# Vrai ou faux : les premières fois de l'aviation (faits : Wright 17/12/1903, 1er vol 12 s / ~37 m ; Roland Garros, Morane-Saulnier L à déflecteurs,
# 3 victoires en avril 1915 en tirant à travers l'hélice ; Earhart 1932 sur Lockheed Vega 5B ; Yeager / Bell X-1 14/10/1947 ;
# Concorde 001 1er vol à Toulouse le 02/03/1969 ; X-15A-2 7 274 km/h (Mach 6,7) le 03/10/1967, Pete Knight — Guinness)
INTRO = dict(say="Vrai ou faux, spécial premières fois de l'aviation ! Six affirmations, trois secondes pour répondre. La dernière piège tout le monde.",
             show="Vrai ou faux : les premières fois de l'aviation ! 6 affirmations, 3 secondes. La dernière piège tout le monde.")
OUTRO = dict(say="Alors, combien sur six ? Écris ton score en commentaire !",
             show="Alors, combien sur 6 ? Écris ton score en commentaire !")
Q = [
    dict(img='wright', stmt="Le 1er vol motorisé a duré plus d'une minute.", answer=1,
         q_say="Numéro un. Le tout premier vol motorisé a duré plus d'une minute.",
         a_say="Faux ! Douze secondes, pour trente-sept mètres, en mille neuf cent trois.",
         a_show="Faux ! 12 secondes, pour 37 mètres, en 1903."),
    dict(img='morane', stmt="Le 1er pilote à abattre des avions en tirant à travers son hélice était français.", answer=0,
         q_say="Numéro deux. Le premier pilote à abattre des avions en tirant à travers son hélice était français.",
         a_say="Vrai ! Roland Garros, en mille neuf cent quinze. Des plaques d'acier sur l'hélice déviaient ses propres balles.",
         a_show="Vrai ! Roland Garros, en 1915. Des plaques d'acier sur l'hélice déviaient ses propres balles."),
    dict(img='vega', stmt="Amelia Earhart a traversé l'Atlantique sur un avion français.", answer=1,
         q_say="Numéro trois. Amelia Earhart a traversé l'Atlantique en solitaire sur un avion français.",
         a_say="Faux ! Elle pilotait un Lockheed Vega américain, en mille neuf cent trente-deux.",
         a_show="Faux ! Elle pilotait un Lockheed Vega américain, en 1932."),
    dict(img='x1', stmt="Le mur du son a été franchi pour la 1re fois en 1960.", answer=1,
         q_say="Numéro quatre. Le mur du son a été franchi pour la première fois en mille neuf cent soixante.",
         a_say="Faux ! Chuck Yeager l'a franchi dès mille neuf cent quarante-sept, à bord du Bell X un.",
         a_show="Faux ! Chuck Yeager l'a franchi dès 1947, à bord du Bell X-1."),
    dict(img='concorde', stmt="Le Concorde a fait son premier vol en France.", answer=0,
         q_say="Numéro cinq. Le Concorde a fait son premier vol en France.",
         a_say="Vrai ! À Toulouse, le deux mars mille neuf cent soixante-neuf.",
         a_show="Vrai ! À Toulouse, le 2 mars 1969."),
    dict(img='x15', stmt="Un avion piloté a déjà dépassé 7 000 km/h.", answer=0,
         q_say="Numéro six. Un avion piloté a déjà dépassé sept mille kilomètres-heure.",
         a_say="Vrai ! Le X quinze, propulsé par une fusée : sept mille deux cent soixante-quatorze kilomètres-heure, en mille neuf cent soixante-sept.",
         a_show="Vrai ! Le X-15, propulsé par une fusée : 7 274 km/h, en 1967."),
]
