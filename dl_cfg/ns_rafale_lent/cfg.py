# LA SCIENCE DU VOL 07 : pourquoi le Rafale vole si lentement. Sources : globalsecurity.org « Rafale design » [travaux sur le canard pour réduire la vitesse d'approche élevée du Mirage III (180 kt ≈ 333 km/h) ;
# configuration longitudinalement instable, marge statique négative, commandes de vol électriques « quadruple redundant with three digital channels and one separately designed analog channel », sans secours mécanique ;
# pilotage limité automatiquement selon l'angle d'attaque] ; migflug.com/aircraft/rafale [approche « 222 km/h, under 120 kn » grâce aux canards ; tourbillons des canards qui énergisent l'écoulement sur l'aile ; roulage 450 m]
SERIES = "LA SCIENCE DU VOL"; EP = "07"; NEXT = "LE PILOTE AUTOMATIQUE"
SCENES = [
    dict(type='hook', top=("333 KM/H", "222 KM/H"), sub=("Mirage III à l'approche", "Rafale à l'approche"),
         gauges=[("ÉCART", "−110 KM/H", 0.66, (1.0, 0.55, 0.0)), ("ATTERRISSAGE", "450 M", 0.45, (0.45, 1.0, 0.92))],
         say="Le Mirage trois arrivait sur la piste à plus de trois cents kilomètres-heure. Le Rafale, à environ deux cent vingt. Même famille, même aile en triangle. Alors, comment le Rafale fait-il pour voler si lentement ?",
         show="Le Mirage III arrivait sur la piste à plus de 300 km/h. Le Rafale, à environ 220. Même famille, même aile en triangle. Alors, comment le Rafale fait-il pour voler si lentement ?"),
    dict(type='plan', items=["LE DELTA", "LES CANARDS", "L'INSTABILITÉ", "LA LIMITE"],
         say="Trois secrets de conception. Et une limite que l'ordinateur surveille sans arrêt.",
         show="3 secrets de conception. Et une limite que l'ordinateur surveille sans arrêt."),
    dict(type='delta', num=1, title="LE DELTA",
         say="Un : le problème du delta. Une aile en triangle est parfaite pour la vitesse. Mais à basse vitesse, elle doit se cabrer très fort pour porter. Résultat : le Mirage trois atterrissait vite, le nez en l'air.",
         show="1 : le problème du delta. Une aile en triangle est parfaite pour la vitesse. Mais à basse vitesse, elle doit se cabrer très fort pour porter. Résultat : le Mirage III atterrissait vite, le nez en l'air."),
    dict(type='canard', num=2, title="LES CANARDS",
         say="Deux : les canards. Ces petites ailes à l'avant créent des tourbillons qui glissent sur l'aile principale. Ils accélèrent l'air au-dessus, et la font porter bien plus à basse vitesse.",
         show="2 : les canards. Ces petites ailes à l'avant créent des tourbillons qui glissent sur l'aile principale. Ils accélèrent l'air au-dessus, et la font porter bien plus à basse vitesse."),
    dict(type='instab', num=3, title="L'INSTABILITÉ",
         say="Trois : l'instabilité. Le Rafale est volontairement instable, comme un crayon en équilibre sur le doigt. Sans ordinateur, impossible à piloter. Mais c'est ce qui le rend si agile.",
         show="3 : l'instabilité. Le Rafale est volontairement instable, comme un crayon en équilibre sur le doigt. Sans ordinateur, impossible à piloter. Mais c'est ce qui le rend si agile."),
    dict(type='fbw', num=None, title="LE CERVEAU",
         say="Ses commandes de vol électriques le corrigent en permanence. Quatre chaînes en parallèle : trois numériques, et une analogique en secours. Aucun câble ne relie le manche aux gouvernes.",
         show="Ses commandes de vol électriques le corrigent en permanence. 4 chaînes en parallèle : 3 numériques, et une analogique en secours. Aucun câble ne relie le manche aux gouvernes."),
    dict(type='aoa', num=4, title="LA LIMITE",
         say="Quatre : la limite. Trop cabrée, une aile décroche : l'air ne colle plus et elle ne porte plus. Alors le calculateur bride automatiquement l'angle du Rafale. Le pilote peut tirer à fond, sans jamais décrocher.",
         show="4 : la limite. Trop cabrée, une aile décroche : l'air ne colle plus et elle ne porte plus. Alors le calculateur bride automatiquement l'angle du Rafale. Le pilote peut tirer à fond, sans jamais décrocher."),
    dict(type='outro', num=None, title="ABONNE-TOI", lines=("UN AVION INSTABLE,", "TENU PAR UN ORDINATEUR"),
         say="Le secret du Rafale : un avion instable, tenu en l'air par un ordinateur. Abonne-toi pour la suite de la science du vol.",
         show="Le secret du Rafale : un avion instable, tenu en l'air par un ordinateur. Abonne-toi pour la suite de la science du vol."),
]
END_HOLD = 4.5
