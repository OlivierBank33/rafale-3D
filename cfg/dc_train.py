# Décodé 04 : le train d'atterrissage (sources : Wikipedia JetBlue Flight 292 [21/09/2005, A320 N536JB, Burbank -> JFK, 140 passagers + 6 équipage,
# roue avant tournée à 90°, > 2 h en huit au-dessus de LA pour brûler le carburant, passagers voyant le direct à la TV DirecTV de bord,
# piste 25L LAX, étincelles et flammes, arrêt ~1 000 ft avant la fin de piste, aucun blessé ; NTSB : joints usés + BSCU] ;
# Wikipedia Aircraft tire [pneus de ligne jusqu'à ~200 psi / 14 bar, gonflés à l'azote sec : pression stable, inerte, risque d'inflammation de l'air] ;
# amortisseur oléopneumatique (huile + azote) ; sortie de secours par gravité (FlyByWire A380 docs) ; A380 : 22 roues)
FICHE = "04"; TITLE = "LE TRAIN D'ATTERRISSAGE"; NEXT = "LE SIÈGE ÉJECTABLE"
SCENES = [
    dict(type='lghook', say="Un avion peut-il atterrir avec sa roue avant bloquée en travers ? C'est arrivé. À Los Angeles.",
         show="Un avion peut-il atterrir avec sa roue avant bloquée en travers ? C'est arrivé. À Los Angeles."),
    dict(type='jb292', say="Histoire vraie. Vingt et un septembre deux mille cinq. Un Airbus A trois cent vingt de JetBlue décolle de Burbank, avec cent quarante-six personnes à bord. Le train avant ne rentre pas. Il est tourné à quatre-vingt-dix degrés.",
         show="Histoire vraie. 21 septembre 2005. Un Airbus A320 de JetBlue décolle de Burbank, avec 146 personnes à bord. Le train avant ne rentre pas. Il est tourné à 90 degrés."),
    dict(type='circle', say="Pendant plus de deux heures, l'avion tourne en rond pour vider ses réservoirs. Et à bord, les passagers regardent leur propre avion en direct, à la télé.",
         show="Pendant plus de deux heures, l'avion tourne en rond pour vider ses réservoirs. Et à bord, les passagers regardent leur propre avion en direct, à la télé."),
    dict(type='touch', say="Le pilote pose d'abord les roues arrière, et garde le nez en l'air le plus longtemps possible. Puis la roue avant touche. Étincelles, flammes, le pneu fond. Mais l'avion reste droit, et s'arrête avant la fin de la piste. Aucun blessé.",
         show="Le pilote pose d'abord les roues arrière, et garde le nez en l'air le plus longtemps possible. Puis la roue avant touche. Étincelles, flammes, le pneu fond. Mais l'avion reste droit, et s'arrête avant la fin de la piste. Aucun blessé."),
    dict(type='oleo', say="Pourquoi ça tient ? Chaque jambe de train est un amortisseur géant : de l'huile, et de l'azote sous pression, qui avalent le choc à chaque atterrissage.",
         show="Pourquoi ça tient ? Chaque jambe de train est un amortisseur géant : de l'huile, et de l'azote sous pression, qui avalent le choc à chaque atterrissage."),
    dict(type='tyres', say="Les pneus, eux aussi, sont gonflés à l'azote. Jusqu'à quatorze bars, six fois plus qu'un pneu de voiture. L'azote ne nourrit pas le feu, et sa pression reste stable dans le froid de l'altitude.",
         show="Les pneus, eux aussi, sont gonflés à l'azote. Jusqu'à 14 bars, 6 fois plus qu'un pneu de voiture. L'azote ne nourrit pas le feu, et sa pression reste stable dans le froid de l'altitude."),
    dict(type='gravity', say="Et si l'hydraulique tombe en panne ? Le pilote déverrouille le train, et il descend tout seul, par son propre poids. Pour JetBlue, la cause était bien plus banale : des joints usés.",
         show="Et si l'hydraulique tombe en panne ? Le pilote déverrouille le train, et il descend tout seul, par son propre poids. Pour JetBlue, la cause était bien plus banale : des joints usés."),
    dict(type='lgoutro', say="Toi, à bord de ce vol, tu aurais regardé la télé, ou pas ? Dis-le en commentaire. Prochaine fiche : le siège éjectable.",
         show="Toi, à bord de ce vol, tu aurais regardé la télé, ou pas ? Dis-le en commentaire. Prochaine fiche : le siège éjectable."),
]
END_HOLD = 2.5
