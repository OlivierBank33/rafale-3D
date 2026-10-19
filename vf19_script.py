# Vrai ou faux : les dangers du ciel (sources : migflug « Lightning strikes your plane twice a year » [un avion de ligne frappé « roughly once or twice every year », passagers protégés par la carlingue] ;
# sommets des cumulonimbus jusqu'à 15 km et plus, au-dessus de la croisière (~11 km) -> contournement ; US Airways 1549 (A320, 15/01/2009, oies, 2 moteurs perdus, amerrissage sur l'Hudson, 155 survivants) ;
# règle de l'aile propre : dégivrage obligatoire avant décollage ; British Airways 9 (Boeing 747, 24/06/1982, cendres du Galunggung, 4 moteurs éteints, redémarrés) ; turbulences ressenties plus fort à l'arrière, au-dessus des ailes le plus calme)
THEME = "DANGERS DU CIEL"
INTRO = dict(say="Vrai ou faux, spécial dangers du ciel ! Six affirmations, trois secondes pour répondre. La dernière va changer ta façon de choisir ton siège.",
             show="Vrai ou faux, spécial dangers du ciel ! 6 affirmations, 3 secondes pour répondre. La dernière va changer ta façon de choisir ton siège.")
OUTRO = dict(say="Alors, combien sur six ? Écris ton score en commentaire !",
             show="Alors, combien sur 6 ? Écris ton score en commentaire !")
Q = [
    dict(img='b767', stmt="Un avion de ligne est frappé par la foudre environ une fois par an.", answer=0,
         q_say="Numéro un. Un avion de ligne est frappé par la foudre environ une fois par an.", q_show="N°1. Un avion de ligne est frappé par la foudre environ une fois par an.",
         a_say="Vrai ! Une à deux fois par an en moyenne. La carlingue conduit le courant autour des passagers, qui ne sentent presque rien.",
         a_show="Vrai ! 1 à 2 fois par an en moyenne. La carlingue conduit le courant autour des passagers, qui ne sentent presque rien."),
    dict(img='b787', stmt="Un avion de ligne peut toujours passer au-dessus d'un orage.", answer=1,
         q_say="Numéro deux. Un avion de ligne peut toujours passer au-dessus d'un orage.", q_show="N°2. Un avion de ligne peut toujours passer au-dessus d'un orage.",
         a_say="Faux ! Un nuage d'orage peut monter à plus de quinze kilomètres. L'avion vole vers onze. Il doit le contourner.",
         a_show="Faux ! Un nuage d'orage peut monter à plus de 15 km. L'avion vole vers 11. Il doit le contourner."),
    dict(img='a320', stmt="Des oiseaux ont forcé un avion de ligne à se poser sur un fleuve.", answer=0,
         q_say="Numéro trois. Des oiseaux ont déjà forcé un avion de ligne à se poser sur un fleuve.", q_show="N°3. Des oiseaux ont déjà forcé un avion de ligne à se poser sur un fleuve.",
         a_say="Vrai ! New York, deux mille neuf. Des oies coupent les deux moteurs d'un A trois cent vingt. Il se pose sur l'Hudson. Cent cinquante-cinq survivants.",
         a_show="Vrai ! New York, 2009. Des oies coupent les 2 moteurs d'un A320. Il se pose sur l'Hudson. 155 survivants."),
    dict(img='concorde', stmt="On peut décoller avec un peu de givre sur les ailes.", answer=1,
         q_say="Numéro quatre. Un avion de ligne peut décoller avec un peu de givre sur les ailes.", q_show="N°4. Un avion de ligne peut décoller avec un peu de givre sur les ailes.",
         a_say="Faux ! Même une fine couche abîme la portance. Les ailes doivent être propres : c'est pour ça qu'on dégivre les avions l'hiver.",
         a_show="Faux ! Même une fine couche abîme la portance. Les ailes doivent être propres : c'est pour ça qu'on dégivre les avions l'hiver."),
    dict(img='vc25', stmt="Un nuage de cendres a éteint les 4 moteurs d'un Boeing 747.", answer=0,
         q_say="Numéro cinq. Un nuage de cendres volcaniques a éteint les quatre moteurs d'un Boeing sept cent quarante-sept.", q_show="N°5. Un nuage de cendres volcaniques a éteint les 4 moteurs d'un Boeing 747.",
         a_say="Vrai ! British Airways, mille neuf cent quatre-vingt-deux, au-dessus de l'Indonésie. Il a plané, puis les moteurs ont redémarré.",
         a_show="Vrai ! British Airways, 1982, au-dessus de l'Indonésie. Il a plané, puis les moteurs ont redémarré."),
    dict(img='a330', stmt="Les turbulences secouent autant à l'avant qu'à l'arrière.", answer=1,
         q_say="Numéro six, le piège. Les turbulences secouent autant à l'avant qu'à l'arrière de l'avion.", q_show="N°6, le piège. Les turbulences secouent autant à l'avant qu'à l'arrière de l'avion.",
         a_say="Faux ! L'arrière bouge plus, comme le bout d'une balançoire. Pour être tranquille, choisis un siège au niveau des ailes.",
         a_show="Faux ! L'arrière bouge plus, comme le bout d'une balançoire. Pour être tranquille, choisis un siège au niveau des ailes."),
]
