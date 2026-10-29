# GRANDS CRASHS : Ténérife, 27/03/1977, aéroport de Los Rodeos. Source : Wikipedia EN « Tenerife airport disaster » (rapport CIAIAC) [bombe à l'aéroport de
# Gran Canaria -> déroutements vers Los Rodeos ; KLM 4805 Boeing 747-206B PH-BUF « Rijn », 248 à bord ; Pan Am 1736 Boeing 747-121 N736PA « Clipper Victor »,
# 396 à bord ; brouillard, visibilité < 100 m ; taxiway bloqué -> remontée de la piste ; Pan Am devait sortir en C3 ; KLM décolle sans autorisation (cause
# fondamentale) ; la tour répond « OK » puis « stand by for takeoff », message couvert par une transmission simultanée de Pan Am (sifflement) ; ~140 kt
# (260 km/h) à la rotation, < 100 m du Pan Am ; 583 morts (248 KLM, 335 Pan Am), 61 survivants, tous à l'avant du Pan Am ; phraséologie normalisée
# (« takeoff » réservé à l'autorisation), CRM]. Pas de citation de l'enregistreur de conversations ; seuls les mots publics de la tour. Livrées neutres sans logo.
SERIES = "GRANDS CRASHS"; EP = "03"; MODE = "histoire"; STYLE = "cinema"
SCENES = [
    dict(type='tf_hook', title="TÉNÉRIFE 1977", focus=(540, 900),
         say="Deux Boeing sept cent quarante-sept sur la même piste, dans le brouillard. Aucun ne voit l'autre. Tu connais le pire accident de l'histoire de l'aviation ?",
         show="Deux Boeing 747 sur la même piste, dans le brouillard. Aucun ne voit l'autre. Tu connais le pire accident de l'histoire de l'aviation ?"),
    dict(type='tf_bomb', title="27 MARS 1977", focus=(540, 900),
         say="Le vingt-sept mars mille neuf cent soixante-dix-sept, une bombe explose à l'aéroport de Gran Canaria. Les avions sont déroutés vers le petit aéroport de Tenerife.",
         show="Le 27 mars 1977, une bombe explose à l'aéroport de Gran Canaria. Les avions sont déroutés vers le petit aéroport de Tenerife."),
    dict(type='tf_fog', title="LE BROUILLARD", focus=(540, 900),
         say="Le parking est plein : pour décoller, il faut remonter la piste. Le sept cent quarante-sept de KLM attend en bout de piste. Celui de Pan Am roule encore dessus, dans un brouillard à moins de cent mètres.",
         show="Le parking est plein : pour décoller, il faut remonter la piste. Le 747 de KLM attend en bout de piste. Celui de Pan Am roule encore dessus, dans un brouillard à moins de 100 mètres."),
    dict(type='tf_radio', title="LA RADIO", focus=(540, 900),
         say="KLM annonce à la tour qu'il est prêt. La tour répond OK, puis demande d'attendre. Mais Pan Am parle au même moment, et les deux messages se brouillent.",
         show="KLM annonce à la tour qu'il est prêt. La tour répond « OK », puis demande d'attendre. Mais Pan Am parle au même moment, et les deux messages se brouillent."),
    dict(type='tf_roll', title="SANS AUTORISATION", focus=(540, 900),
         say="Le commandant de KLM lance le décollage sans autorisation. À deux cent soixante kilomètres-heure, le Pan Am surgit du brouillard, droit devant.",
         show="Le commandant de KLM lance le décollage sans autorisation. À 260 km/h, le Pan Am surgit du brouillard, droit devant."),
    dict(type='tf_impact', title="L'IMPACT", focus=(540, 900),
         say="Le KLM décolle trop tôt, percute le dessus du Pan Am, et s'écrase plus loin. Le kérosène s'embrase.",
         show="Le KLM décolle trop tôt, percute le dessus du Pan Am, et s'écrase plus loin. Le kérosène s'embrase."),
    dict(type='tf_toll', title="583", focus=(540, 900),
         say="Cinq cent quatre-vingt-trois morts. Soixante et un survivants, tous à l'avant du Pan Am.",
         show="583 morts. 61 survivants, tous à l'avant du Pan Am."),
    dict(type='tf_after', title="DEPUIS", focus=(540, 900),
         say="Depuis, le mot décollage n'est prononcé que pour autoriser un décollage, et les copilotes apprennent à contredire leur commandant. Tu savais que ce drame avait changé l'aviation ?",
         show="Depuis, le mot « décollage » n'est prononcé que pour autoriser un décollage, et les copilotes apprennent à contredire leur commandant. Tu savais que ce drame avait changé l'aviation ?"),
]
END_HOLD = 10.0
RECAP_DELAY = 3.0
RECAP = [("583", "victimes", (0.92, 0.95, 1.0)), ("61", "survivants", (0.4, 1, 0.6)), ("< 100 M", "de visibilité", (1, 0.85, 0.25))]
RECAP_NOTE = "En mémoire des 583 victimes de Los Rodeos"
