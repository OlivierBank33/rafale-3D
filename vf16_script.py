# Vrai ou faux : spécial France (faits : Patrouille de France sur Alpha Jet depuis 1981 ; la France quitte le programme Eurofighter en 1985 et développe seule le Rafale ;
# record New York–Londres du Concorde 2 h 52 min 59 s (7/02/1996) ; 1er avion de ligne à réaction = De Havilland Comet (1949), Caravelle 1er vol 1955 ;
# Blériot traverse la Manche le 25/07/1909 en ~37 min ; Taïwan a reçu 60 Mirage 2000-5 (1997))
THEME = "SPÉCIAL FRANCE"
INTRO = dict(say="Vrai ou faux, spécial aviation française ! Six affirmations, trois secondes pour répondre. Seuls les vrais passionnés font six sur six.",
             show="Vrai ou faux, spécial aviation française ! 6 affirmations, 3 secondes pour répondre. Seuls les vrais passionnés font 6 sur 6.")
OUTRO = dict(say="Alors, combien sur six ? Écris ton score en commentaire !",
             show="Alors, combien sur 6 ? Écris ton score en commentaire !")
Q = [
    dict(img='alphajet', stmt="La Patrouille de France vole sur Alpha Jet.", answer=0,
         q_say="Numéro un. La Patrouille de France vole sur Alpha Jet.", q_show="N°1. La Patrouille de France vole sur Alpha Jet.",
         a_say="Vrai ! Huit Alpha Jet, depuis mille neuf cent quatre-vingt-un.",
         a_show="Vrai ! 8 Alpha Jet, depuis 1981."),
    dict(img='rafale', stmt="Le Rafale a été conçu avec l'Allemagne.", answer=1,
         q_say="Numéro deux. Le Rafale a été conçu avec l'Allemagne.", q_show="N°2. Le Rafale a été conçu avec l'Allemagne.",
         a_say="Faux ! La France a quitté le projet européen en mille neuf cent quatre-vingt-cinq, et a fait le Rafale seule.",
         a_show="Faux ! La France a quitté le projet européen en 1985, et a fait le Rafale seule."),
    dict(img='concorde', stmt="Le Concorde a relié New York à Londres en moins de 3 heures.", answer=0,
         q_say="Numéro trois. Le Concorde a relié New York à Londres en moins de trois heures.", q_show="N°3. Le Concorde a relié New York à Londres en moins de 3 heures.",
         a_say="Vrai ! Deux heures cinquante-deux minutes, en mille neuf cent quatre-vingt-seize. Un record toujours debout.",
         a_show="Vrai ! 2 h 52 min, en 1996. Un record toujours debout."),
    dict(img='caravelle', stmt="La Caravelle a été le 1er avion de ligne à réaction.", answer=1,
         q_say="Numéro quatre. La Caravelle a été le tout premier avion de ligne à réaction.", q_show="N°4. La Caravelle a été le tout premier avion de ligne à réaction.",
         a_say="Faux ! C'est le Comet britannique, dès mille neuf cent quarante-neuf. La Caravelle a volé six ans plus tard.",
         a_show="Faux ! C'est le Comet britannique, dès 1949. La Caravelle a volé 6 ans plus tard."),
    dict(img='bleriot_a', stmt="Blériot a mis plus de 2 heures pour traverser la Manche.", answer=1,
         q_say="Numéro cinq. Blériot a mis plus de deux heures pour traverser la Manche.", q_show="N°5. Blériot a mis plus de 2 heures pour traverser la Manche.",
         a_say="Faux ! Trente-sept minutes environ, le vingt-cinq juillet mille neuf cent neuf.",
         a_show="Faux ! 37 minutes environ, le 25 juillet 1909."),
    dict(img='m2000', stmt="Taïwan vole sur des Mirage 2000 français.", answer=0,
         q_say="Numéro six. Taïwan vole sur des Mirage deux mille français.", q_show="N°6. Taïwan vole sur des Mirage 2000 français.",
         a_say="Vrai ! Soixante Mirage deux mille cinq, livrés à partir de mille neuf cent quatre-vingt-dix-sept.",
         a_show="Vrai ! 60 Mirage 2000-5, livrés à partir de 1997."),
]
