# Vrai ou faux : les géants du ciel (faits : A380 assemblé à Toulouse ; An-225 Mriya détruit à Hostomel en février 2022 ; Beluga transporte des
# tronçons d'Airbus entre les usines ; B-52 toujours en service, modernisé (B-52J) pour voler jusque vers 2050 ; KC-130F posé 21 fois sans crosse
# sur l'USS Forrestal le 30/10/1963 (The Aviationist) ; A400M : les deux hélices de chaque aile tournent en sens inverse, vers l'intérieur)
INTRO = dict(say="Vrai ou faux, spécial géants du ciel ! Six affirmations, trois secondes pour répondre. La dernière piège tout le monde.",
             show="Vrai ou faux : les géants du ciel ! 6 affirmations, 3 secondes. La dernière piège tout le monde.")
OUTRO = dict(say="Alors, combien sur six ? Écris ton score en commentaire !",
             show="Alors, combien sur 6 ? Écris ton score en commentaire !")
Q = [
    dict(img='a380', stmt="L'A380 est assemblé à Toulouse.", answer=0,
         q_say="Numéro un. L'A trois cent quatre-vingts est assemblé à Toulouse.",
         a_say="Vrai ! Son assemblage final se fait à Toulouse, dans une usine géante.",
         a_show="Vrai ! Son assemblage final se fait à Toulouse, dans une usine géante."),
    dict(img='an225', stmt="L'An-225 vole encore aujourd'hui.", answer=1,
         q_say="Numéro deux. L'Antonov deux cent vingt-cinq, le plus gros avion du monde, vole encore aujourd'hui.",
         a_say="Faux ! Il a été détruit au sol en Ukraine, en février deux mille vingt-deux.",
         a_show="Faux ! Il a été détruit au sol en Ukraine, en février 2022."),
    dict(img='beluga', stmt="Le Beluga transporte des morceaux d'avions.", answer=0,
         q_say="Numéro trois. Le Beluga transporte des morceaux d'avions.",
         a_say="Vrai ! Il emporte des tronçons d'Airbus d'une usine à l'autre.",
         a_show="Vrai ! Il emporte des tronçons d'Airbus d'une usine à l'autre."),
    dict(img='b52', stmt="Le B-52 a été retiré du service.", answer=1,
         q_say="Numéro quatre. Le bombardier B cinquante-deux a été retiré du service.",
         a_say="Faux ! Il vole toujours, et il est modernisé pour voler jusque vers deux mille cinquante.",
         a_show="Faux ! Il vole toujours, et il est modernisé pour voler jusque vers 2050."),
    dict(img='c130', stmt="Un C-130 s'est posé sur un porte-avions.", answer=0,
         q_say="Numéro cinq. Un avion cargo C cent trente s'est déjà posé sur un porte-avions.",
         a_say="Vrai ! En mille neuf cent soixante-trois, vingt et une fois, sans crosse d'appontage.",
         a_show="Vrai ! En 1963, 21 fois, sans crosse d'appontage."),
    dict(img='a400m', stmt="Sur chaque aile de l'A400M, les hélices tournent en sens inverse.", answer=0,
         q_say="Numéro six. Sur chaque aile de l'A quatre cents M, les deux hélices tournent en sens inverse.",
         a_say="Vrai ! Elles tournent l'une vers l'autre, pour un avion plus stable.",
         a_show="Vrai ! Elles tournent l'une vers l'autre, pour un avion plus stable."),
]
