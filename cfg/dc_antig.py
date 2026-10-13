# Décodé 06 : la combinaison anti-G (sources : The Aviationist 13/09/2016 [élève pilote F-16 Arizona ANG, G-LOC jusqu'à 8,4 G, piqué 55°, plein PC,
# > 600 kt (≈ 1 110 km/h), descente de 17 000 ft à 8 700 ft (≈ 2 650 m) où l'Auto-GCAS redresse l'avion, 4e sauvetage confirmé depuis 2014] ;
# Wikipedia G-suit [poches gonflées sur ventre et jambes via valve sensible aux G, ~ +1 G de tolérance (3-5 G au repos), voile gris -> tunnel -> voile noir -> G-LOC ;
# manœuvre de contraction AGSM toujours nécessaire])
FICHE = "06"; TITLE = "LA COMBINAISON ANTI-G"; NEXT = "LE CASQUE DU PILOTE"
SCENES = [
    dict(type='aghook', say="Un pilote de chasse peut-il s'évanouir en plein vol ? Oui. Et son avion part en piqué.",
         show="Un pilote de chasse peut-il s'évanouir en plein vol ? Oui. Et son avion part en piqué."),
    dict(type='agturn', say="Histoire vraie. Deux mille seize, aux États-Unis. Un élève pilote de F seize enchaîne les virages serrés. Plus de huit G, huit fois son poids. Et soudain, il perd connaissance.",
         show="Histoire vraie. 2016, aux États-Unis. Un élève pilote de F-16 enchaîne les virages serrés. Plus de 8 G, 8 fois son poids. Et soudain, il perd connaissance."),
    dict(type='agdive', say="Son avion pique vers le sol, à cinquante-cinq degrés, plein gaz, à plus de mille cent kilomètres-heure. Il perd plus de deux mille cinq cents mètres.",
         show="Son avion pique vers le sol, à 55 degrés, plein gaz, à plus de 1100 km/h. Il perd plus de 2500 mètres."),
    dict(type='aggcas', say="Et là, l'ordinateur prend la main. Le système anti-collision du F seize redresse l'avion tout seul, vers deux mille six cents mètres. Le pilote se réveille. Vivant.",
         show="Et là, l'ordinateur prend la main. Le système anti-collision du F-16 redresse l'avion tout seul, vers 2600 mètres. Le pilote se réveille. Vivant."),
    dict(type='agblood', say="Pourquoi il s'est évanoui ? Sous les G, le sang descend vers les jambes, et le cerveau en manque. La vision devient grise, puis un tunnel, puis le noir. Puis plus rien.",
         show="Pourquoi il s'est évanoui ? Sous les G, le sang descend vers les jambes, et le cerveau en manque. La vision devient grise, puis un tunnel, puis le noir. Puis plus rien."),
    dict(type='agsuit', say="C'est là qu'intervient la combinaison anti-G. Des poches d'air se gonflent sur le ventre et les jambes, et serrent pour retenir le sang.",
         show="C'est là qu'intervient la combinaison anti-G. Des poches d'air se gonflent sur le ventre et les jambes, et serrent pour retenir le sang."),
    dict(type='agstrain', say="Au repos, un humain tient entre trois et cinq G. La combinaison n'ajoute qu'environ un G. Le reste, c'est le pilote : il contracte tous ses muscles, et contrôle sa respiration, à chaque virage.",
         show="Au repos, un humain tient entre 3 et 5 G. La combinaison n'ajoute qu'environ 1 G. Le reste, c'est le pilote : il contracte tous ses muscles, et contrôle sa respiration, à chaque virage."),
    dict(type='agoutro', say="Toi, tu tiendrais combien de G ? Dis-le en commentaire. Prochaine fiche : le casque du pilote.",
         show="Toi, tu tiendrais combien de G ? Dis-le en commentaire. Prochaine fiche : le casque du pilote."),
]
END_HOLD = 5.5
