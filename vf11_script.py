# Vrai ou faux : Seconde Guerre mondiale (faits : Spitfire britannique ; Me 262 1er chasseur à réaction opérationnel (1944) ;
# A6M2 Zero sans blindage pilote ni réservoirs auto-obturants ; P-51B/D moteur Merlin Rolls-Royce construit par Packard ;
# V1 basculés à l'aile par Spitfire/Tempest ; Avia S-199 = Bf 109G tchèque, 1er chasseur de l'armée de l'air israélienne, mai 1948)
INTRO = dict(say="Vrai ou faux, spécial Seconde Guerre mondiale ! Six affirmations, trois secondes pour répondre. La dernière piège tout le monde.",
             show="Vrai ou faux : la Seconde Guerre mondiale ! 6 affirmations, 3 secondes. La dernière piège tout le monde.")
OUTRO = dict(say="Alors, combien sur six ? Écris ton score en commentaire !",
             show="Alors, combien sur 6 ? Écris ton score en commentaire !")
Q = [
    dict(img='spitfire', stmt="Le Spitfire était un avion américain.", answer=1,
         q_say="Numéro un. Le Spitfire était un avion américain.",
         a_say="Faux ! Il était britannique, et il a défendu l'Angleterre en mille neuf cent quarante.",
         a_show="Faux ! Il était britannique, et il a défendu l'Angleterre en 1940."),
    dict(img='ww_me262', stmt="Le 1er chasseur à réaction en service était allemand.", answer=0,
         q_say="Numéro deux. Le premier chasseur à réaction en service était allemand.",
         a_say="Vrai ! Le Messerschmitt deux cent soixante-deux, engagé dès mille neuf cent quarante-quatre.",
         a_show="Vrai ! Le Messerschmitt Me 262, engagé dès 1944."),
    dict(img='zero', stmt="Le Zero japonais était très blindé.", answer=1,
         q_say="Numéro trois. Le Zero japonais était très blindé.",
         a_say="Faux ! Presque aucun blindage, pour être léger et voler très loin. Son grand point faible.",
         a_show="Faux ! Presque aucun blindage, pour être léger et voler très loin. Son grand point faible."),
    dict(img='ww_p51', stmt="Le Mustang américain avait un moteur britannique.", answer=0,
         q_say="Numéro quatre. Le Mustang américain volait avec un moteur britannique.",
         a_say="Vrai ! Un Merlin, conçu par Rolls-Royce, fabriqué aux États-Unis.",
         a_show="Vrai ! Un Merlin, conçu par Rolls-Royce, fabriqué aux États-Unis."),
    dict(img='spit_34', stmt="Des pilotes renversaient des V1 avec leur aile.", answer=0,
         q_say="Numéro cinq. Des pilotes renversaient des bombes volantes avec le bout de leur aile.",
         a_say="Vrai ! Ils glissaient l'aile sous celle du V un, et la bombe basculait.",
         a_show="Vrai ! Ils glissaient l'aile sous celle du V1, et la bombe basculait."),
    dict(img='bf109_34', stmt="Le 1er chasseur israélien était un Messerschmitt.", answer=0,
         q_say="Numéro six. Le premier chasseur de l'armée de l'air israélienne était un Messerschmitt.",
         a_say="Vrai ! Une version tchèque du Messerschmitt cent neuf, en mille neuf cent quarante-huit.",
         a_show="Vrai ! Une version tchèque du Bf 109, en 1948."),
]
