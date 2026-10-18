# Vrai ou faux : 14-18 (sources : Western Front Association / Wikipedia « Aerial combat of 5 October 1914 » [Frantz et Quénault, Voisin III, mitrailleuse Hotchkiss, première victoire aérienne] ;
# migflug « The Red Baron » [la majorité de ses 80 victoires sur Albatros D.III et D.V, le Dr.I seulement quelques mois] ; HistoryNet « Heinecke parachute » [Allemagne 1918 ; « France and America did not allow their pilots to use them during the war »] ;
# WFA « The First World War career of René Fonck » [75 victoires homologuées, meilleur as allié, SPAD XIII] ; Rickenbacker, meilleur as américain (26 victoires), sur SPAD XIII)
THEME = "14-18"
INTRO = dict(say="Vrai ou faux, spécial guerre de quatorze-dix-huit ! Six affirmations, trois secondes pour répondre. La dernière piège presque tout le monde.",
             show="Vrai ou faux, spécial guerre de 14-18 ! 6 affirmations, 3 secondes pour répondre. La dernière piège presque tout le monde.")
OUTRO = dict(say="Alors, combien sur six ? Écris ton score en commentaire !",
             show="Alors, combien sur 6 ? Écris ton score en commentaire !")
Q = [
    dict(img='bleriot_a', stmt="En 1914, les avions partaient sans mitrailleuse.", answer=0,
         q_say="Numéro un. En mille neuf cent quatorze, les avions partaient en mission sans mitrailleuse.", q_show="N°1. En 1914, les avions partaient en mission sans mitrailleuse.",
         a_say="Vrai ! Ils servaient à observer. Les équipages se tiraient dessus au pistolet ou à la carabine.",
         a_show="Vrai ! Ils servaient à observer. Les équipages se tiraient dessus au pistolet ou à la carabine."),
    dict(img='dr1', stmt="Le Baron rouge a eu la plupart de ses victoires sur son triplan.", answer=1,
         q_say="Numéro deux. Le Baron rouge a remporté la plupart de ses quatre-vingts victoires sur son célèbre triplan.", q_show="N°2. Le Baron rouge a remporté la plupart de ses 80 victoires sur son célèbre triplan.",
         a_say="Faux ! Il ne l'a piloté que quelques mois. L'essentiel, il l'a fait sur des biplans Albatros.",
         a_show="Faux ! Il ne l'a piloté que quelques mois. L'essentiel, il l'a fait sur des biplans Albatros."),
    dict(img='morane', stmt="La première victoire aérienne de l'histoire est française.", answer=0,
         q_say="Numéro trois. La première victoire d'un avion contre un autre avion est française.", q_show="N°3. La première victoire d'un avion contre un autre avion est française.",
         a_say="Vrai ! Le cinq octobre mille neuf cent quatorze, près de Reims. Frantz et Quénault abattent un avion allemand à la mitrailleuse.",
         a_show="Vrai ! Le 5 octobre 1914, près de Reims. Frantz et Quénault abattent un avion allemand à la mitrailleuse."),
    dict(img='camel', stmt="Les pilotes français de 14-18 avaient un parachute.", answer=1,
         q_say="Numéro quatre. Les pilotes de chasse français de quatorze-dix-huit avaient un parachute.", q_show="N°4. Les pilotes de chasse français de 14-18 avaient un parachute.",
         a_say="Faux ! La France ne les a jamais autorisés pendant la guerre. Les Allemands, eux, en ont reçu en mille neuf cent dix-huit.",
         a_show="Faux ! La France ne les a jamais autorisés pendant la guerre. Les Allemands, eux, en ont reçu en 1918."),
    dict(img='spad', stmt="Des pilotes américains ont combattu sur des avions français.", answer=0,
         q_say="Numéro cinq. Des pilotes américains ont combattu sur des avions français.", q_show="N°5. Des pilotes américains ont combattu sur des avions français.",
         a_say="Vrai ! Eddie Rickenbacker, le meilleur as américain, volait sur un SPAD treize, construit en France.",
         a_show="Vrai ! Eddie Rickenbacker, le meilleur as américain, volait sur un SPAD XIII, construit en France."),
    dict(img='th_spad', stmt="Le meilleur as allié de la guerre était britannique.", answer=1,
         q_say="Numéro six, le piège. Le meilleur as allié de toute la guerre était britannique.", q_show="N°6, le piège. Le meilleur as allié de toute la guerre était britannique.",
         a_say="Faux ! C'est un Français : René Fonck, soixante-quinze victoires homologuées. Plus que n'importe quel pilote allié.",
         a_show="Faux ! C'est un Français : René Fonck, 75 victoires homologuées. Plus que n'importe quel pilote allié."),
]
