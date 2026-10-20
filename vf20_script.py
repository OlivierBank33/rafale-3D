# Vrai ou faux : secrets de pilotes (sources : Wikipedia « Mayday » [F. S. Mockford, Croydon, 1923, de « m'aider »/« venez m'aider »] ; OACI : anglais obligatoire disponible pour
# l'international mais langue locale autorisée (en France, le contrôle parle français et anglais) ; Flight Deck Friend « Can the pilots eat the same meal » [plus une obligation, mais « some airlines
# still recommend the pilots eat different meals »] ; limite d'âge 65 ans pour le transport commercial de passagers (OACI, EASA, FAA) ; repos équipage : couchettes sur long-courrier ;
# transpondeur 7500 = détournement, 7600 = panne radio, 7700 = urgence)
THEME = "SECRETS DE PILOTES"
INTRO = dict(say="Vrai ou faux, spécial secrets de pilotes ! Six affirmations, trois secondes pour répondre. Le dernier code, presque personne ne le connaît.",
             show="Vrai ou faux, spécial secrets de pilotes ! 6 affirmations, 3 secondes pour répondre. Le dernier code, presque personne ne le connaît.")
OUTRO = dict(say="Alors, combien sur six ? Écris ton score en commentaire !",
             show="Alors, combien sur 6 ? Écris ton score en commentaire !")
Q = [
    dict(img='a320', stmt="« Mayday » vient du français.", answer=0,
         q_say="Numéro un. Le mot Mayday, l'appel de détresse, vient du français.", q_show="N°1. Le mot « Mayday », l'appel de détresse, vient du français.",
         a_say="Vrai ! De « m'aider », comme dans « venez m'aider ». Choisi en Angleterre en mille neuf cent vingt-trois, pour les vols vers Paris.",
         a_show="Vrai ! De « m'aider », comme dans « venez m'aider ». Choisi en Angleterre en 1923, pour les vols vers Paris."),
    dict(img='a330', stmt="Partout dans le monde, les pilotes doivent parler anglais à la tour.", answer=1,
         q_say="Numéro deux. Partout dans le monde, les pilotes sont obligés de parler anglais à la tour de contrôle.", q_show="N°2. Partout dans le monde, les pilotes sont obligés de parler anglais à la tour de contrôle.",
         a_say="Faux ! L'anglais doit toujours être possible, mais la langue du pays est autorisée. En France, un pilote d'Air France peut parler français.",
         a_show="Faux ! L'anglais doit toujours être possible, mais la langue du pays est autorisée. En France, un pilote d'Air France peut parler français."),
    dict(img='b787', stmt="Le commandant et le copilote mangent souvent des plats différents.", answer=0,
         q_say="Numéro trois. Le commandant et le copilote mangent souvent des plats différents.", q_show="N°3. Le commandant et le copilote mangent souvent des plats différents.",
         a_say="Vrai ! Beaucoup de compagnies le conseillent. Si un plat est avarié, un seul pilote tombe malade.",
         a_show="Vrai ! Beaucoup de compagnies le conseillent. Si un plat est avarié, un seul pilote tombe malade."),
    dict(img='caravelle', stmt="Un pilote de ligne peut transporter des passagers jusqu'à 70 ans.", answer=1,
         q_say="Numéro quatre. Un pilote de ligne peut transporter des passagers jusqu'à soixante-dix ans.", q_show="N°4. Un pilote de ligne peut transporter des passagers jusqu'à 70 ans.",
         a_say="Faux ! La limite est de soixante-cinq ans, en Europe comme aux États-Unis.",
         a_show="Faux ! La limite est de 65 ans, en Europe comme aux États-Unis."),
    dict(img='b767', stmt="Sur un long vol, des pilotes dorment dans un lit caché.", answer=0,
         q_say="Numéro cinq. Sur un très long vol, des pilotes dorment dans un lit caché de l'avion.", q_show="N°5. Sur un très long vol, des pilotes dorment dans un lit caché de l'avion.",
         a_say="Vrai ! Un équipage de relève se repose dans des couchettes, souvent au-dessus de la cabine. Les passagers ne les voient jamais.",
         a_show="Vrai ! Un équipage de relève se repose dans des couchettes, souvent au-dessus de la cabine. Les passagers ne les voient jamais."),
    dict(img='concorde', stmt="Le code 7500 veut dire panne radio.", answer=1,
         q_say="Numéro six, le piège. Quand un pilote affiche le code sept mille cinq cents, ça veut dire panne radio.", q_show="N°6, le piège. Quand un pilote affiche le code 7500, ça veut dire « panne radio ».",
         a_say="Faux ! Sept mille cinq cents, c'est un détournement. La panne radio, c'est sept mille six cents. Et l'urgence, sept mille sept cents.",
         a_show="Faux ! 7500, c'est un détournement. La panne radio, c'est 7600. Et l'urgence, 7700."),
]
