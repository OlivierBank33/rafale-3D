# QU'AURAIS-TU FAIT ? : US Airways 1549. Source : migflug « Three minutes to the Hudson » / NTSB [15/01/2009, A320, impact d'oies à 2 818 ft (~860 m), deux moteurs perdus ;
# options : retour LaGuardia (piste 13) ou Teterboro (piste 1) ; amerrissage sur l'Hudson ~3 min après l'impact ; 155 à bord, 155 survivants ; simulateurs NTSB : demi-tour immédiat vers LaGuardia
# réussi 7 fois sur 13, mais avec 35 s de délai de réaction réaliste : crash ; décision de Sullenberger jugée correcte]
SERIES = "QU'AURAIS-TU FAIT ?"; EP = "01"; MODE = "histoire"
SCENES = [
    dict(type='su_hook', title="QU'AURAIS-TU FAIT ?",
         say="Quinze janvier deux mille neuf, New York. Tu viens de décoller de LaGuardia, avec cent cinquante-cinq personnes à bord. À huit cent soixante mètres, des oies. Tes deux moteurs s'arrêtent.",
         show="15 janvier 2009, New York. Tu viens de décoller de LaGuardia, avec 155 personnes à bord. À 860 mètres, des oies. Tes 2 moteurs s'arrêtent."),
    dict(type='su_glide', title="TROIS MINUTES",
         say="Ton avion est devenu un planeur de plus de soixante tonnes, au-dessus de la ville la plus dense d'Amérique. Tu as environ trois minutes avant de toucher quelque chose.",
         show="Ton avion est devenu un planeur de plus de 60 tonnes, au-dessus de la ville la plus dense d'Amérique. Tu as environ 3 minutes avant de toucher quelque chose."),
    dict(type='su_options', title="TROIS CHOIX",
         say="Trois options. A : demi-tour vers LaGuardia, la piste que tu viens de quitter. B : l'aéroport de Teterboro, de l'autre côté du fleuve. C : te poser sur l'Hudson, le fleuve glacé.",
         show="3 options. A : demi-tour vers LaGuardia, la piste que tu viens de quitter. B : l'aéroport de Teterboro, de l'autre côté du fleuve. C : te poser sur l'Hudson, le fleuve glacé."),
    dict(type='su_pause', title="TU FAIS QUOI ?",
         say="Tu as trois secondes. Choisis. A, B ou C ? Trois. Deux. Un.",
         show="Tu as 3 secondes. Choisis. A, B ou C ? 3. 2. 1."),
    dict(type='su_reveal', title="L'HUDSON",
         say="Le commandant Sullenberger a choisi l'Hudson. Trois minutes après les oies, il pose l'Airbus sur le fleuve. Les cent cinquante-cinq personnes à bord survivent.",
         show="Le commandant Sullenberger a choisi l'Hudson. 3 minutes après les oies, il pose l'Airbus sur le fleuve. Les 155 personnes à bord survivent."),
    dict(type='su_sim', title="ET SI ?",
         say="Plus tard, les enquêteurs ont refait le vol au simulateur. En faisant demi-tour immédiatement, des pilotes atteignent LaGuardia sept fois sur treize. Mais avec trente-cinq secondes pour comprendre et décider, comme en vrai : l'avion s'écrase avant la piste.",
         show="Plus tard, les enquêteurs ont refait le vol au simulateur. En faisant demi-tour immédiatement, des pilotes atteignent LaGuardia 7 fois sur 13. Mais avec 35 secondes pour comprendre et décider, comme en vrai : l'avion s'écrase avant la piste."),
    dict(type='su_end', title="LE BON CHOIX",
         say="L'Hudson était le bon choix. Et toi, tu avais choisi quoi ? A, B ou C, en commentaire.",
         show="L'Hudson était le bon choix. Et toi, tu avais choisi quoi ? A, B ou C, en commentaire."),
]
END_HOLD = 9.0
