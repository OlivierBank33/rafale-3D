# Vrai ou faux : les secrets des avions de ligne (faits : porte « bouchon » plaquée par la pression cabine (plusieurs tonnes) ; toilettes à vide
# vers un réservoir vidé au sol ; biréacteurs certifiés pour voler sur un seul moteur (ETOPS) ; foudre ≈ 1 fois par an par avion de ligne ;
# Concorde Paris–New York en ~3 h 30 ; téléphone non en mode avion = grésillement possible dans les casques pilotes)
INTRO = dict(say="Vrai ou faux, spécial avions de ligne ! Six affirmations, trois secondes pour répondre.",
             show="Vrai ou faux : avions de ligne ! 6 affirmations, 3 secondes pour répondre.")
OUTRO = dict(say="Alors, combien sur six ? Écris ton score en commentaire !",
             show="Alors, combien sur 6 ? Écris ton score en commentaire !")
Q = [
    dict(img='b787', stmt="On peut ouvrir une porte d'avion en plein vol.", answer=1,
         q_say="Numéro un. On peut ouvrir une porte d'avion en plein vol.",
         a_say="Faux ! La pression de la cabine plaque la porte contre l'avion avec plusieurs tonnes. Impossible à la main.",
         a_show="Faux ! La pression de la cabine plaque la porte avec plusieurs tonnes. Impossible à la main."),
    dict(img='a320', stmt="Les toilettes se vident en plein vol.", answer=1,
         q_say="Numéro deux. Les toilettes se vident en plein vol.",
         a_say="Faux ! Tout part dans un réservoir, vidé une fois au sol.",
         a_show="Faux ! Tout part dans un réservoir, vidé une fois au sol."),
    dict(img='a330', stmt="Un biréacteur peut voler avec un seul moteur.", answer=0,
         q_say="Numéro trois. Un biréacteur peut voler avec un seul moteur.",
         a_say="Vrai ! Il est même certifié pour ça, parfois pendant plusieurs heures au-dessus de l'océan.",
         a_show="Vrai ! Il est même certifié pour ça, parfois pendant plusieurs heures au-dessus de l'océan."),
    dict(img='b767', stmt="Un avion de ligne est foudroyé environ une fois par an.", answer=0,
         q_say="Numéro quatre. Un avion de ligne est foudroyé environ une fois par an.",
         a_say="Vrai ! Et la coque en métal fait cage de Faraday : le courant passe autour de toi.",
         a_show="Vrai ! Et la coque fait cage de Faraday : le courant passe autour de toi."),
    dict(img='concorde', stmt="Le Concorde reliait Paris à New York en moins de 4 heures.", answer=0,
         q_say="Numéro cinq. Le Concorde reliait Paris à New York en moins de quatre heures.",
         a_say="Vrai ! Environ trois heures et demie. Avec le décalage horaire, tu arrivais avant d'être parti.",
         a_show="Vrai ! Environ 3 h 30. Avec le décalage horaire, tu arrivais avant d'être parti."),
    dict(img='a320', stmt="Le mode avion de ton téléphone ne sert à rien.", answer=1,
         q_say="Numéro six. Le mode avion de ton téléphone ne sert à rien.",
         a_say="Faux ! Sans lui, ton téléphone peut faire grésiller le casque des pilotes.",
         a_show="Faux ! Sans lui, ton téléphone peut faire grésiller le casque des pilotes."),
]
