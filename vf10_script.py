# Vrai ou faux : l'aviation française (faits : Patrouille de France sur Alpha Jet ; Rafale M sur le porte-avions Charles-de-Gaulle ;
# Concorde franco-britannique ; Mirage III Mach 2,2 ; A400M assemblé à Séville (Espagne) ; Caravelle, 1er avion de ligne à réacteurs à l'arrière)
INTRO = dict(say="Vrai ou faux, spécial aviation française ! Six affirmations, trois secondes pour répondre.",
             show="Vrai ou faux : aviation française ! 6 affirmations, 3 secondes pour répondre.")
OUTRO = dict(say="Alors, combien sur six ? Écris ton score en commentaire !",
             show="Alors, combien sur 6 ? Écris ton score en commentaire !")
Q = [
    dict(img='alphajet', stmt="La Patrouille de France vole sur Rafale.", answer=1,
         q_say="Numéro un. La Patrouille de France vole sur Rafale.",
         a_say="Faux ! Elle vole sur Alpha Jet, un avion d'entraînement.",
         a_show="Faux ! Elle vole sur Alpha Jet, un avion d'entraînement."),
    dict(img='rafale', stmt="Le Rafale peut se poser sur un porte-avions.", answer=0,
         q_say="Numéro deux. Le Rafale peut se poser sur un porte-avions.",
         a_say="Vrai ! Sa version Marine se pose sur le Charles-de-Gaulle, accrochée par une crosse.",
         a_show="Vrai ! Sa version Marine se pose sur le Charles-de-Gaulle, accrochée par une crosse."),
    dict(img='concorde', stmt="Le Concorde était 100 % français.", answer=1,
         q_say="Numéro trois. Le Concorde était cent pour cent français.",
         a_say="Faux ! C'était un projet franco-britannique.",
         a_show="Faux ! C'était un projet franco-britannique."),
    dict(img='mirage3', stmt="Le Mirage III dépassait Mach 2.", answer=0,
         q_say="Numéro quatre. Le Mirage trois dépassait Mach deux.",
         a_say="Vrai ! Mach deux virgule deux, dès les années soixante.",
         a_show="Vrai ! Mach 2,2, dès les années 60."),
    dict(img='a400m', stmt="L'Airbus A400M est assemblé en France.", answer=1,
         q_say="Numéro cinq. L'Airbus A quatre cents M est assemblé en France.",
         a_say="Faux ! Son assemblage final se fait à Séville, en Espagne.",
         a_show="Faux ! Son assemblage final se fait à Séville, en Espagne."),
    dict(img='caravelle', stmt="La Caravelle a lancé les réacteurs à l'arrière.", answer=0,
         q_say="Numéro six. La Caravelle a lancé les réacteurs à l'arrière.",
         a_say="Vrai ! C'est le premier avion de ligne avec ses réacteurs à l'arrière, et l'idée a été copiée partout.",
         a_show="Vrai ! Premier avion de ligne avec ses réacteurs à l'arrière, et l'idée a été copiée partout."),
]
