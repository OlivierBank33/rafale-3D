# Vrai ou faux : avions de ligne (faits : An-225 640 t > A380 575 t ; Boeing 787 ≈ 50 % de composites en masse ; A320 piloté au mini-manche latéral ;
# Concorde en croisière jusqu'à ~18 000 m ; Air Transat 236 (A330, 24/08/2001) a plané ~19 min jusqu'aux Açores ; « Gimli Glider » (Air Canada 143, Boeing 767, 1983) : panne sèche due à une erreur de conversion livres/kilos)
THEME = "AVIONS DE LIGNE"
INTRO = dict(say="Vrai ou faux, spécial avions de ligne ! Six affirmations, trois secondes pour répondre. Les deux dernières sont des histoires vraies incroyables.",
             show="Vrai ou faux, spécial avions de ligne ! 6 affirmations, 3 secondes pour répondre. Les 2 dernières sont des histoires vraies incroyables.")
OUTRO = dict(say="Alors, combien sur six ? Écris ton score en commentaire !",
             show="Alors, combien sur 6 ? Écris ton score en commentaire !")
Q = [
    dict(img='an225', stmt="L'Antonov 225 était plus lourd qu'un A380.", answer=0,
         q_say="Numéro un. L'Antonov deux cent vingt-cinq était plus lourd qu'un A trois cent quatre-vingts.", q_show="N°1. L'Antonov 225 était plus lourd qu'un A380.",
         a_say="Vrai ! Six cent quarante tonnes au décollage, contre cinq cent soixante-quinze pour l'A trois cent quatre-vingts. Le plus lourd de l'histoire.",
         a_show="Vrai ! 640 tonnes au décollage, contre 575 pour l'A380. Le plus lourd de l'histoire."),
    dict(img='b787', stmt="Le Boeing 787 est fait à moitié de matériaux composites.", answer=0,
         q_say="Numéro deux. Le Boeing sept cent quatre-vingt-sept est fait à moitié de matériaux composites.", q_show="N°2. Le Boeing 787 est fait à moitié de matériaux composites.",
         a_say="Vrai ! Environ cinquante pour cent de sa masse. Plus léger que l'aluminium, et il ne rouille pas.",
         a_show="Vrai ! Environ 50 % de sa masse. Plus léger que l'aluminium, et il ne rouille pas."),
    dict(img='a320', stmt="Dans un A320, le pilote a un grand manche entre les jambes.", answer=1,
         q_say="Numéro trois. Dans un A trois cent vingt, le pilote a un grand manche entre les jambes.", q_show="N°3. Dans un A320, le pilote a un grand manche entre les jambes.",
         a_say="Faux ! Il pilote avec un mini-manche, sur le côté, comme une manette.",
         a_show="Faux ! Il pilote avec un mini-manche, sur le côté, comme une manette."),
    dict(img='concorde', stmt="Le Concorde volait à plus de 15 000 mètres.", answer=0,
         q_say="Numéro quatre. Le Concorde volait à plus de quinze mille mètres d'altitude.", q_show="N°4. Le Concorde volait à plus de 15 000 mètres d'altitude.",
         a_say="Vrai ! Jusqu'à dix-huit mille mètres. Les passagers voyaient la courbure de la Terre.",
         a_show="Vrai ! Jusqu'à 18 000 mètres. Les passagers voyaient la courbure de la Terre."),
    dict(img='a330', stmt="Un A330 a plané près de 20 minutes sans moteurs.", answer=0,
         q_say="Numéro cinq. Un A trois cent trente a plané près de vingt minutes, sans aucun moteur.", q_show="N°5. Un A330 a plané près de 20 minutes, sans aucun moteur.",
         a_say="Vrai ! Vol Air Transat deux cent trente-six, en deux mille un. Il s'est posé aux Açores, sans un seul mort.",
         a_show="Vrai ! Vol Air Transat 236, en 2001. Il s'est posé aux Açores, sans un seul mort."),
    dict(img='b767', stmt="Un Boeing 767 est tombé en panne sèche à cause d'une fuite.", answer=1,
         q_say="Numéro six. Un Boeing sept cent soixante-sept est tombé en panne sèche à cause d'une fuite.", q_show="N°6. Un Boeing 767 est tombé en panne sèche à cause d'une fuite.",
         a_say="Faux ! C'était une erreur de calcul : des livres confondues avec des kilos. Il a plané jusqu'à Gimli, en mille neuf cent quatre-vingt-trois.",
         a_show="Faux ! C'était une erreur de calcul : des livres confondues avec des kilos. Il a plané jusqu'à Gimli, en 1983."),
]
