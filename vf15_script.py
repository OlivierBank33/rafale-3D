# Vrai ou faux : avions mythiques (faits : F-117 abattu au-dessus de la Serbie le 27/03/1999 ; B-2 ≈ 2,1 Md$ pièce développement compris (1997) ;
# A-10 conçu autour du canon GAU-8 Avenger 30 mm ; poussée vectorielle du Harrier : brevets de l'ingénieur français Michel Wibault (1954-1957, Gyropter → Pegasus) ;
# Mirage IIICJ israéliens pendant la guerre des Six Jours (1967) ; SR-71 : selon l'US Air Force plus de 4 000 missiles tirés, aucun avion perdu par action ennemie)
INTRO = dict(say="Vrai ou faux, spécial avions mythiques ! Six affirmations, trois secondes pour répondre. La quatrième va surprendre beaucoup de monde.",
             show="Vrai ou faux : avions mythiques ! 6 affirmations, 3 secondes. La 4e va surprendre beaucoup de monde.")
OUTRO = dict(say="Alors, combien sur six ? Écris ton score en commentaire !",
             show="Alors, combien sur 6 ? Écris ton score en commentaire !")
Q = [
    dict(img='f117', stmt="Le F-117 furtif n'a jamais été abattu.", answer=1,
         q_say="Numéro un. Le F cent dix-sept, l'avion furtif, n'a jamais été abattu.",
         a_say="Faux ! Un F cent dix-sept a été abattu au-dessus de la Serbie, en mille neuf cent quatre-vingt-dix-neuf.",
         a_show="Faux ! Un F-117 a été abattu au-dessus de la Serbie, en 1999."),
    dict(img='b2', stmt="Un bombardier B-2 coûte environ 2 milliards de dollars.", answer=0,
         q_say="Numéro deux. Un bombardier B deux coûte environ deux milliards de dollars.",
         a_say="Vrai ! Environ deux virgule un milliards pièce, développement compris.",
         a_show="Vrai ! Environ 2,1 milliards pièce, développement compris."),
    dict(img='a10', stmt="L'A-10 a été conçu autour d'un missile.", answer=1,
         q_say="Numéro trois. L'A dix a été conçu autour d'un missile.",
         a_say="Faux ! Il a été conçu autour de son énorme canon de trente millimètres, le GAU huit.",
         a_show="Faux ! Il a été conçu autour de son énorme canon de 30 mm, le GAU-8."),
    dict(img='harrier', stmt="L'idée du Harrier vient d'un ingénieur français.", answer=0,
         q_say="Numéro quatre. L'idée du Harrier, l'avion qui décolle à la verticale, vient d'un ingénieur français.",
         a_say="Vrai ! Michel Wibault a breveté les tuyères orientables dans les années cinquante. Les Britanniques en ont fait le Harrier.",
         a_show="Vrai ! Michel Wibault a breveté les tuyères orientables dans les années 1950. Les Britanniques en ont fait le Harrier."),
    dict(img='mirage3', stmt="Le Mirage III n'a jamais combattu.", answer=1,
         q_say="Numéro cinq. Le Mirage trois n'a jamais combattu.",
         a_say="Faux ! Les Mirage trois israéliens ont dominé le ciel pendant la guerre des Six Jours, en mille neuf cent soixante-sept.",
         a_show="Faux ! Les Mirage III israéliens ont dominé le ciel pendant la guerre des Six Jours, en 1967."),
    dict(img='sr71', stmt="Plus de 4 000 missiles ont été tirés sur le SR-71.", answer=0,
         q_say="Numéro six. Plus de quatre mille missiles ont été tirés sur le SR soixante et onze.",
         a_say="Vrai ! Selon l'US Air Force. Et aucun ne l'a jamais touché : il accélérait, tout simplement.",
         a_show="Vrai ! Selon l'US Air Force. Et aucun ne l'a jamais touché : il accélérait, tout simplement."),
]
