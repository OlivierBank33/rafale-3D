# SURVIVRAIS-TU ? : Juliane Koepcke, vol LANSA 508 (24/12/1971, Pérou). Sources : Wikipedia EN « LANSA Flight 508 » [Lockheed L-188A Electra, Lima -> Pucallpa -> Iquitos,
# 92 à bord (86 passagers + 6 équipage), foudre sur l'aile droite -> incendie -> rupture en vol ; Juliane 17 ans, chute d'environ 3 km encore attachée à son siège ;
# clavicule cassée, ligament du genou, coupure profonde au bras droit, commotion ; 11 jours dans la forêt ; jusqu'à 14 autres survivants initiaux morts en attendant
# les secours dont sa mère ; 91 morts ; enquête : vol délibéré dans des conditions météo dangereuses] ; Wikipedia EN « Juliane Koepcke » [parents zoologistes ;
# a suivi un ruisseau puis une rivière ; larves dans la plaie du bras ; biologiste, directrice de la station Panguana (fondée par ses parents) depuis 2000 ; campement de bûcherons au 9e jour ; les bûcherons versent de l'essence sur sa plaie (larves), canoë 11 h]. Ton respectueux.
SERIES = "SURVIVRAIS-TU ?"; EP = "09"; MODE = "survie"; STYLE = "cinema"
SCENES = [
    dict(type='jk_hook', title="SURVIVRAIS-TU ?", focus=(540, 900),
         say="Ton avion se brise en plein orage. Tu tombes de trois kilomètres au-dessus de la jungle, attaché à ton siège. Survivrais-tu ?",
         show="Ton avion se brise en plein orage. Tu tombes de 3 kilomètres au-dessus de la jungle, attaché à ton siège. Survivrais-tu ?"),
    dict(type='jk_real', title="HISTOIRE VRAIE", focus=(540, 900),
         say="C'est l'histoire vraie de Juliane Koepcke, dix-sept ans. Le vingt-quatre décembre mille neuf cent soixante et onze, elle survole l'Amazonie péruvienne avec sa mère. Quatre-vingt-douze personnes sont à bord.",
         show="C'est l'histoire vraie de Juliane Koepcke, 17 ans. Le 24 décembre 1971, elle survole l'Amazonie péruvienne avec sa mère. 92 personnes sont à bord."),
    dict(type='jk_storm', title="L'ORAGE", focus=(540, 900),
         say="L'avion traverse un violent orage. La foudre frappe l'aile droite, un incendie se déclare, et l'avion se brise en vol.",
         show="L'avion traverse un violent orage. La foudre frappe l'aile droite, un incendie se déclare, et l'avion se brise en vol."),
    dict(type='jk_fall', title="3 KM", focus=(540, 900),
         say="Juliane tombe d'environ trois kilomètres, toujours attachée à son siège. Elle se réveille au sol, vivante.",
         show="Juliane tombe d'environ 3 kilomètres, toujours attachée à son siège. Elle se réveille au sol, vivante."),
    dict(type='jk_hurt', title="SEULE", focus=(540, 900),
         say="Clavicule cassée, genou blessé, une profonde coupure au bras. Et autour d'elle, personne.",
         show="Clavicule cassée, genou blessé, une profonde coupure au bras. Et autour d'elle, personne."),
    dict(type='jk_river', title="SUIVRE L'EAU", focus=(540, 900),
         say="Fille de zoologistes, elle connaît la forêt. Elle suit un ruisseau, puis une rivière, en marchant dans l'eau.",
         show="Fille de zoologistes, elle connaît la forêt. Elle suit un ruisseau, puis une rivière, en marchant dans l'eau."),
    dict(type='jk_found', title="JOUR 11", focus=(540, 900),
         say="Le neuvième jour, elle trouve un campement de bûcherons. Le onzième jour, ils la découvrent, versent de l'essence sur sa plaie infestée de larves, et l'emmènent en pirogue.",
         show="Le neuvième jour, elle trouve un campement de bûcherons. Le onzième jour, ils la découvrent, versent de l'essence sur sa plaie infestée de larves, et l'emmènent en pirogue."),
    dict(type='jk_later', title="BIOLOGISTE", focus=(540, 900),
         say="Elle est ensuite devenue biologiste, et a pris la direction de la station de recherche fondée par ses parents, en pleine jungle.",
         show="Elle est ensuite devenue biologiste, et a pris la direction de la station de recherche fondée par ses parents, en pleine jungle."),
    dict(type='jk_verdict', title="VERDICT", focus=(540, 900),
         say="Verdict : elle est la seule survivante. Quatre-vingt-onze personnes sont mortes, dont sa mère. Et toi, tu aurais tenu onze jours ?",
         show="Verdict : elle est la seule survivante. 91 personnes sont mortes, dont sa mère. Et toi, tu aurais tenu 11 jours ?"),
]
END_HOLD = 10.0
RECAP_DELAY = 3.0
RECAP = [("3 KM", "de chute", (1, 0.85, 0.25)), ("11 JOURS", "seule dans la jungle", (0.45, 0.9, 0.55)), ("1 SUR 92", "survivante", (0.92, 0.95, 1.0))]
RECAP_NOTE = "En mémoire des 91 victimes du vol LANSA 508"
