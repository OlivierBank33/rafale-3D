# LA SCIENCE DU VOL 05 : comment un avion freine. Sources : Air & Space / Smithsonian « How Things Work: Stopping the A380 » [test de décollage interrompu de certification :
# masse max au décollage (1 265 000 lb ≈ 575 t), freins usés à 90 %, décision à 170 kt (≈ 315 km/h), sans inverseurs, arrêt en 6 070 ft (≈ 1 850 m), pneus dégonflés quelques minutes après ;
# inverseurs uniquement sur les 2 moteurs intérieurs (poids, risque d'ingestion de débris) ; freins composites carbone sur 16 des 20 roues du train principal ; 16 spoilers (8 par aile) ;
# antiblocage] ; bouchons fusibles des roues ; piste mouillée : distance d'atterrissage exigée = 115 % de la distance sur piste sèche (règle de préparation du vol)
SERIES = "LA SCIENCE DU VOL"; EP = "05"; NEXT = "LES TRAÎNÉES BLANCHES"
SCENES = [
    dict(type='hook', top=("315 KM/H", "1 850 M"), sub=("A380 lancé à fond", "pour s'arrêter"),
         gauges=[("MASSE", "575 T", 1.0, (1.0, 0.55, 0.0)), ("FREINS USÉS", "90 %", 0.9, (1.0, 0.18, 0.33))],
         say="Cinq cent soixante-quinze tonnes, lancées à trois cent quinze kilomètres-heure. Lors d'un test, cet A trois cent quatre-vingts s'est arrêté en mille huit cent cinquante mètres. Comment freine-t-on un géant pareil ?",
         show="575 tonnes, lancées à 315 km/h. Lors d'un test, cet A380 s'est arrêté en 1 850 mètres. Comment freine-t-on un géant pareil ?"),
    dict(type='plan', items=["LES SPOILERS", "LES INVERSEURS", "LES FREINS", "LA LIMITE"],
         say="Trois systèmes travaillent ensemble. Et il y a une limite que même eux ne peuvent pas battre.",
         show="3 systèmes travaillent ensemble. Et il y a une limite que même eux ne peuvent pas battre."),
    dict(type='spoil', num=1, title="LES SPOILERS",
         say="Un : les spoilers. Au toucher, seize panneaux se dressent sur les ailes. Ils cassent la portance. L'avion arrête de voler, et tout son poids écrase les roues. Sans ça, les freins patineraient.",
         show="1 : les spoilers. Au toucher, 16 panneaux se dressent sur les ailes. Ils cassent la portance. L'avion arrête de voler, et tout son poids écrase les roues. Sans ça, les freins patineraient."),
    dict(type='reverse', num=2, title="LES INVERSEURS",
         say="Deux : les inverseurs. Des volets renvoient le souffle des réacteurs vers l'avant. Sur l'A trois cent quatre-vingts, seuls les deux moteurs intérieurs en ont. Les moteurs extérieurs, eux, dépassent au-dessus du bord de la piste, et pourraient aspirer des débris.",
         show="2 : les inverseurs. Des volets renvoient le souffle des réacteurs vers l'avant. Sur l'A380, seuls les 2 moteurs intérieurs en ont. Les moteurs extérieurs, eux, dépassent au-dessus du bord de la piste, et pourraient aspirer des débris."),
    dict(type='brakes', num=3, title="LES FREINS",
         say="Trois : les freins. Seize roues sur vingt ont des disques en carbone, comme en Formule un. Un antiblocage les relâche par à-coups, comme l'ABS d'une voiture. Ce sont eux qui font l'essentiel du travail.",
         show="3 : les freins. 16 roues sur 20 ont des disques en carbone, comme en Formule 1. Un antiblocage les relâche par à-coups, comme l'ABS d'une voiture. Ce sont eux qui font l'essentiel du travail."),
    dict(type='rto', num=None, title="LE TEST EXTRÊME",
         say="Pour le certifier, Airbus l'a chargé au maximum, avec des freins usés à quatre-vingt-dix pour cent. Décollage interrompu à trois cent quinze kilomètres-heure, sans inverseurs. Arrêt en mille huit cent cinquante mètres. Quelques minutes plus tard, les pneus se dégonflent, comme prévu : des fusibles fondent pour éviter qu'ils explosent.",
         show="Pour le certifier, Airbus l'a chargé au maximum, avec des freins usés à 90 %. Décollage interrompu à 315 km/h, sans inverseurs. Arrêt en 1 850 mètres. Quelques minutes plus tard, les pneus se dégonflent, comme prévu : des fusibles fondent pour éviter qu'ils explosent."),
    dict(type='wet', num=4, title="LA LIMITE",
         say="Quatre : la limite. Sur une piste mouillée, les pneus accrochent moins. La règle impose alors une piste quinze pour cent plus longue qu'au sec.",
         show="4 : la limite. Sur une piste mouillée, les pneus accrochent moins. La règle impose alors une piste 15 % plus longue qu'au sec."),
    dict(type='outro', num=None, title="ABONNE-TOI", lines=("POUR FREINER, UN AVION DOIT", "D'ABORD ARRÊTER DE VOLER"),
         say="Pour freiner, un avion doit d'abord arrêter de voler. Abonne-toi pour la suite de la science du vol.",
         show="Pour freiner, un avion doit d'abord arrêter de voler. Abonne-toi pour la suite de la science du vol."),
]
END_HOLD = 4.5
