# Vrai ou faux : spécial Rafale (faits : Dassault Aviation, assemblage final à Mérignac ; Rafale B biplace pilote + officier systèmes d'armes ;
# 2 réacteurs Safran M88 ; ASMP-A des Forces aériennes stratégiques ; combat en Afghanistan dès mars 2007 (AIN 18/06/2007), puis Libye, Mali, Irak, Syrie ;
# essai nacelle NARANG : un Rafale M ravitaille un A400M en vol (The Aviationist 27/11/2024))
INTRO = dict(say="Vrai ou faux, spécial Rafale ! Six affirmations, trois secondes pour répondre. La dernière piège tout le monde.",
             show="Vrai ou faux : spécial Rafale ! 6 affirmations, 3 secondes. La dernière piège tout le monde.")
OUTRO = dict(say="Alors, combien sur six ? Écris ton score en commentaire !",
             show="Alors, combien sur 6 ? Écris ton score en commentaire !")
Q = [
    dict(img='rafale', stmt="Le Rafale est fabriqué par Airbus.", answer=1,
         q_say="Numéro un. Le Rafale est fabriqué par Airbus.",
         a_say="Faux ! C'est un avion Dassault, assemblé à Mérignac, près de Bordeaux.",
         a_show="Faux ! C'est un avion Dassault, assemblé à Mérignac, près de Bordeaux."),
    dict(img='rafale_34', stmt="Le Rafale existe en version deux places.", answer=0,
         q_say="Numéro deux. Le Rafale existe en version deux places.",
         a_say="Vrai ! Le Rafale B, avec un pilote et un officier systèmes d'armes.",
         a_show="Vrai ! Le Rafale B, avec un pilote et un officier systèmes d'armes."),
    dict(img='rafale_front', stmt="Le Rafale n'a qu'un seul réacteur.", answer=1,
         q_say="Numéro trois. Le Rafale n'a qu'un seul réacteur.",
         a_say="Faux ! Il en a deux, des M quatre-vingt-huit fabriqués par Safran.",
         a_show="Faux ! Il en a deux, des M88 fabriqués par Safran."),
    dict(img='rafale_side', stmt="Le Rafale peut emporter l'arme nucléaire.", answer=0,
         q_say="Numéro quatre. Le Rafale peut emporter l'arme nucléaire.",
         a_say="Vrai ! Il porte le missile A S M P A, celui des Forces aériennes stratégiques.",
         a_show="Vrai ! Il porte le missile ASMP-A, celui des Forces aériennes stratégiques."),
    dict(img='rafale_top', stmt="Le Rafale n'a jamais fait la guerre.", answer=1,
         q_say="Numéro cinq. Le Rafale n'a jamais fait la guerre.",
         a_say="Faux ! En Afghanistan dès deux mille sept, puis en Libye, au Mali, en Irak et en Syrie.",
         a_show="Faux ! En Afghanistan dès 2007, puis en Libye, au Mali, en Irak et en Syrie."),
    dict(img='rafale', stmt="Un Rafale a déjà ravitaillé un avion de transport.", answer=0,
         q_say="Numéro six. Un Rafale a déjà fait le plein, en vol, d'un gros avion de transport.",
         a_say="Vrai ! Lors d'un essai, un Rafale Marine a donné du carburant à un A quatre cents M.",
         a_show="Vrai ! Lors d'un essai, un Rafale Marine a donné du carburant à un A400M."),
]
