# Les avions les plus chers du monde — du moins cher au plus cher, piles de billets (volume ∝ prix)
INTRO = dict(say="Huit avions, du moins cher au plus cher. À côté de chacun, une pile de billets de la taille de son prix. Le dernier va te faire mal à la tête.")
OUTRO = dict(say="Alors, avec ton gain au Loto, tu prends lequel ? Dis-le en commentaire.")
# eur : valeur en millions d'euros utilisée pour la pile ; L : taille d'affichage (m) ; flip : nez à gauche
PLANES = [
    dict(k='c172', name="CESSNA 172", eur=0.45, price="≈ 450 000 €", note="prix neuf · avion d'aéroclub", L=11.0,
         say="On commence avec le Cessna cent soixante-douze, l'avion des aéroclubs. Neuf, environ cinq cent mille dollars. Le prix d'une belle maison."),
    dict(k='spitfire', name="SPITFIRE", eur=3.6, price="3,6 M€", note="record aux enchères · Christie's 2015", L=11.2,
         say="Un Spitfire de la Seconde Guerre mondiale, en état de vol. Record aux enchères : plus de trois millions et demi d'euros."),
    dict(k='f35', name="F-35A", eur=79, price="≈ 79 M€", note="prix unitaire · contrat 2025", L=15.7,
         say="Le F-35 américain. Environ quatre-vingts millions d'euros pièce. Et ça, c'est sans les missiles."),
    dict(k='rafale', name="RAFALE", eur=120, price="≈ 120 M€", note="commande France 2024 · 42 avions pour 5 Md€", L=15.3, flip=True,
         say="Le Rafale. Pour l'armée française, environ cent vingt millions d'euros l'avion. À l'export, avec les armes et la formation, la facture peut doubler."),
    dict(k='f22', name="F-22 RAPTOR", eur=170, price="≈ 170 M€", note="coût de fabrication · en euros actuels", L=18.9,
         say="Le F-22 Raptor. Environ cent soixante-dix millions d'euros à fabriquer. Et les États-Unis refusent de le vendre à qui que ce soit."),
    dict(k='b787', name="BOEING 787", eur=252, price="≈ 252 M€", note="prix catalogue 787-9 · remises fréquentes", L=62.8,
         say="Le Boeing sept cent quatre-vingt-sept Dreamliner. Prix catalogue : deux cent cinquante millions d'euros. Mais les compagnies obtiennent de grosses remises."),
    dict(k='vc25', name="AIR FORCE ONE", eur=1680, price="≈ 1,7 Md€", note="VC-25B · 3,9 Md$ les deux avions", L=76.3,
         say="Air Force One, le nouvel avion du président américain. Un Boeing sept cent quarante-sept transformé. Près d'un milliard sept cents millions d'euros chacun."),
    dict(k='b2', name="B-2 SPIRIT", eur=3300, price="≈ 3,3 Md€", note="coût par avion · 2,1 Md$ de 1997", L=52.4,
         say="Et le plus cher de tous : le bombardier furtif B-2 Spirit. Plus de deux milliards de dollars pièce en mille neuf cent quatre-vingt-dix-sept. Aujourd'hui, plus de trois milliards d'euros. Seulement vingt et un ont été construits."),
]
