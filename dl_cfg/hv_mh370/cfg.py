# MYSTÈRE : MH370 (8 mars 2014). Sources : Wikipedia EN « Timeline of Malaysia Airlines Flight 370 » [départ KL 00:42 MYT ; 239 personnes (227 passagers dont 2 bébés, 12 équipage) ;
# « Good night. Malaysian Three Seven Zero » 01:19 ; transpondeur perdu 01:21 ; radar militaire : demi-tour, traversée de la péninsule, détroit de Malacca, dernier contact 02:22 ;
# poignées de main Inmarsat 02:25 -> 08:19 (dernière transmission 00:19:37 UTC) = 7e arc ; flaperon trouvé à La Réunion le 29/07/2015, confirmé par la France le 3/09/2015 ;
# recherche sous-marine 2014-2017 : 120 000 km²] ; PBS / AP mars 2026 [Ocean Infinity 2025-2026 : 28 jours, ~7 571 km², aucun résultat ; 2018 : recherche privée sans résultat].
SERIES = "MYSTÈRES"; EP = "01"; MODE = "histoire"
SCENES = [
    dict(type='mh_hook', title="MH370", focus=(540, 900),
         say="Un Boeing 777, avec deux cent trente-neuf personnes à bord, a disparu en deux mille quatorze. Douze ans plus tard, on ne l'a toujours pas retrouvé. Tu connais le mystère du MH370 ?",
         show="Un Boeing 777, avec 239 personnes à bord, a disparu en 2014. 12 ans plus tard, on ne l'a toujours pas retrouvé. Tu connais le mystère du MH370 ?"),
    dict(type='mh_night', title="8 MARS 2014", focus=(540, 900),
         say="Huit mars deux mille quatorze. Le vol MH370 décolle de Kuala Lumpur pour Pékin, en pleine nuit. À une heure dix-neuf, le commandant salue le contrôle aérien : bonne nuit.",
         show="8 mars 2014. Le vol MH370 décolle de Kuala Lumpur pour Pékin, en pleine nuit. À 1 h 19, le commandant salue le contrôle aérien : bonne nuit."),
    dict(type='mh_dark', title="01:21", focus=(540, 900),
         say="Deux minutes plus tard, son transpondeur s'éteint. L'avion disparaît des écrans des contrôleurs.",
         show="2 minutes plus tard, son transpondeur s'éteint. L'avion disparaît des écrans des contrôleurs."),
    dict(type='mh_turn', title="DEMI-TOUR", focus=(540, 900),
         say="Mais un radar militaire le voit faire demi-tour, retraverser la Malaisie, puis filer au-dessus de la mer. Dernier écho radar : deux heures vingt-deux.",
         show="Mais un radar militaire le voit faire demi-tour, retraverser la Malaisie, puis filer au-dessus de la mer. Dernier écho radar : 2 h 22."),
    dict(type='mh_arcs', title="7E ARC", focus=(540, 900),
         say="Ensuite, plus rien, sauf un satellite. Pendant six heures, l'avion échange avec lui des signaux automatiques. Ces signaux dessinent des arcs. Le dernier, le septième, traverse le sud de l'océan Indien.",
         show="Ensuite, plus rien, sauf un satellite. Pendant 6 heures, l'avion échange avec lui des signaux automatiques. Ces signaux dessinent des arcs. Le dernier, le septième, traverse le sud de l'océan Indien."),
    dict(type='mh_flaperon', title="LA RÉUNION", focus=(540, 900),
         say="En juillet deux mille quinze, un morceau d'aile s'échoue sur l'île de La Réunion. C'est bien un morceau du MH370.",
         show="En juillet 2015, un morceau d'aile s'échoue sur l'île de La Réunion. C'est bien un morceau du MH370."),
    dict(type='mh_search', title="120 000 KM²", focus=(540, 900),
         say="Les recherches ont ratissé plus de cent vingt mille kilomètres carrés de fond marin. Début deux mille vingt-six, une nouvelle mission revient encore les mains vides.",
         show="Les recherches ont ratissé plus de 120 000 km² de fond marin. Début 2026, une nouvelle mission revient encore les mains vides."),
    dict(type='mh_end', title="LE MYSTÈRE", focus=(540, 900),
         say="Aujourd'hui encore, personne ne sait ce qui s'est passé à bord. Toi, tu as une théorie ?",
         show="Aujourd'hui encore, personne ne sait ce qui s'est passé à bord. Toi, tu as une théorie ?"),
]
END_HOLD = 11.0
RECAP_DELAY = 2.5
RECAP = [("239", "personnes à bord", (0.92, 0.95, 1.0)), ("7E ARC", "la dernière trace", (0.2, 0.95, 1.0)), ("12 ANS", "sans épave", (1, 0.85, 0.25))]
RECAP_NOTE = "En mémoire des 239 personnes à bord du MH370"
