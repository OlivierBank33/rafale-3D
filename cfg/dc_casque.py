# Décodé 07 : le casque du pilote (sources : New Atlas [casque Gen III du F-35 ≈ 400 000 $, 6 caméras extérieures, vue 360° et à travers l'avion,
# tête scannée en 3D, mousse découpée au laser, ≈ 2,3 kg] ; Air Recognition 03/2021 [viseur de casque Scorpion de Thales pour le Rafale F4,
# écran couleur jour et nuit, informations de pilotage, navigation et mission sur la visière])
FICHE = "07"; TITLE = "LE CASQUE DU PILOTE"; NEXT = "LA VERRIÈRE"
SCENES = [
    dict(type='hehook', say="Un casque de pilote peut-il coûter le prix d'une maison ? Celui du F trente-cinq : environ quatre cent mille dollars.",
         show="Un casque de pilote peut-il coûter le prix d'une maison ? Celui du F-35 : environ 400 000 dollars."),
    dict(type='hexray', say="Son secret : il voit à travers l'avion. Six caméras filment tout autour du F trente-cinq, et la visière assemble les images. Le pilote baisse la tête, et il voit le sol, à travers le plancher.",
         show="Son secret : il voit à travers l'avion. 6 caméras filment tout autour du F-35, et la visière assemble les images. Le pilote baisse la tête, et il voit le sol, à travers le plancher."),
    dict(type='hehud', say="Les informations de vol s'affichent directement dans la visière : vitesse, altitude, cible. Pour viser, le pilote n'a qu'à tourner la tête.",
         show="Les informations de vol s'affichent directement dans la visière : vitesse, altitude, cible. Pour viser, le pilote n'a qu'à tourner la tête."),
    dict(type='hefit', say="Chaque casque est fait sur mesure. On scanne la tête du pilote en trois D, puis la mousse intérieure est découpée au laser. Et le réglage est revérifié tous les quatre mois. Une nouvelle coupe de cheveux peut suffire à tout dérégler.",
         show="Chaque casque est fait sur mesure. On scanne la tête du pilote en 3D, puis la mousse intérieure est découpée au laser. Et le réglage est revérifié tous les quatre mois. Une nouvelle coupe de cheveux peut suffire à tout dérégler."),
    dict(type='heg', say="Il pèse environ deux kilos trois, plus qu'un casque de moto haut de gamme. Mais à neuf G, c'est comme porter plus de vingt kilos, uniquement avec la nuque.",
         show="Il pèse environ 2,3 kilos, plus qu'un casque de moto haut de gamme. Mais à 9 G, c'est comme porter plus de 20 kilos, uniquement avec la nuque."),
    dict(type='herafale', say="Et le Rafale ? Avec le standard F quatre, ses pilotes reçoivent eux aussi un viseur de casque : le Scorpion, de Thales, avec un affichage en couleur, de jour comme de nuit.",
         show="Et le Rafale ? Avec le standard F4, ses pilotes reçoivent eux aussi un viseur de casque : le Scorpion, de Thales, avec un affichage en couleur, de jour comme de nuit."),
    dict(type='heoutro', say="Toi, tu choisis le casque du F trente-cinq, ou celui du Rafale ? Dis-le en commentaire. Prochaine fiche : la verrière.",
         show="Toi, tu choisis le casque du F-35, ou celui du Rafale ? Dis-le en commentaire. Prochaine fiche : la verrière."),
]
END_HOLD = 7.5
