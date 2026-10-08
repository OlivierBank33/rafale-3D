# Vrai ou faux : le corps du pilote (faits : temps de conscience utile ~30 s à 1 min vers 11 000 m (FAA) ; désorientation spatiale (oreille interne) ;
# repas différents pilote/copilote (pratique courante des compagnies) ; repos contrôlé en poste autorisé en Europe (EASA, « controlled rest ») ;
# voile gris = perte des couleurs sous facteur de charge, puis voile noir ; SR-71 : combinaison pressurisée David Clark, proche de celles des astronautes)
INTRO = dict(say="Vrai ou faux, spécial corps du pilote ! Six affirmations, trois secondes pour répondre.",
             show="Vrai ou faux : le corps du pilote ! 6 affirmations, 3 secondes pour répondre.")
OUTRO = dict(say="Alors, combien sur six ? Écris ton score en commentaire !",
             show="Alors, combien sur 6 ? Écris ton score en commentaire !")
Q = [
    dict(img='a320', stmt="Sans oxygène à 11 000 m, tu restes conscient plusieurs minutes.", answer=1,
         q_say="Numéro un. Sans oxygène, à onze mille mètres, tu restes conscient plusieurs minutes.",
         a_say="Faux ! Tu as entre trente secondes et une minute pour réagir. C'est pour ça que les masques tombent tout de suite.",
         a_show="Faux ! Tu as entre 30 secondes et 1 minute pour réagir. C'est pour ça que les masques tombent tout de suite."),
    dict(img='c172', stmt="Dans les nuages, tu peux tourner sans le sentir.", answer=0,
         q_say="Numéro deux. Dans les nuages, tu peux tourner sans le sentir.",
         a_say="Vrai ! Ton oreille interne se trompe. C'est pour ça que les pilotes apprennent à croire leurs instruments, pas leurs sensations.",
         a_show="Vrai ! Ton oreille interne se trompe. Les pilotes apprennent à croire leurs instruments, pas leurs sensations."),
    dict(img='a330', stmt="Le pilote et le copilote mangent le même repas.", answer=1,
         q_say="Numéro trois. Le pilote et le copilote mangent le même repas.",
         a_say="Faux ! Souvent, ils prennent des plats différents. Si l'un est malade, l'autre peut encore piloter.",
         a_show="Faux ! Souvent, ils prennent des plats différents. Si l'un est malade, l'autre peut encore piloter."),
    dict(img='b787', stmt="En Europe, un pilote de ligne peut faire une sieste aux commandes.", answer=0,
         q_say="Numéro quatre. En Europe, un pilote de ligne peut faire une sieste aux commandes.",
         a_say="Vrai ! Une courte sieste est autorisée, à condition que l'autre pilote reste bien réveillé.",
         a_show="Vrai ! Une courte sieste est autorisée, à condition que l'autre pilote reste bien réveillé."),
    dict(img='rafale', stmt="En virage serré, un pilote de chasse peut voir en noir et blanc.", answer=0,
         q_say="Numéro cinq. En virage serré, un pilote de chasse peut voir en noir et blanc.",
         a_say="Vrai ! Le sang quitte la tête, la vision perd ses couleurs : c'est le voile gris. Juste après, c'est le voile noir.",
         a_show="Vrai ! Le sang quitte la tête, la vision perd ses couleurs : c'est le voile gris. Juste après, le voile noir."),
    dict(img='sr71', stmt="Les pilotes de SR-71 portaient une combinaison d'astronaute.", answer=0,
         q_say="Numéro six. Les pilotes de SR soixante et onze portaient une combinaison d'astronaute.",
         a_say="Vrai ! À vingt-quatre kilomètres d'altitude, sans combinaison pressurisée, leur sang se serait mis à bouillir.",
         a_show="Vrai ! À 24 km d'altitude, sans combinaison pressurisée, leur sang se serait mis à bouillir."),
]
