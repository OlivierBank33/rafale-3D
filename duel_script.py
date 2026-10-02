# Duel : Rafale vs F-22 Raptor
# scene = type de plan ; say = texte lu (TTS) ; show = sous-titres ; score = (rafale, f22) après la scène
SCENES = [
    dict(scene='hook', score=(0, 0),
         say="Rafale contre F-22 Raptor. Cinq rounds. Un seul vainqueur.",
         show="Rafale contre F-22 Raptor. 5 rounds. Un seul vainqueur."),
    dict(scene='vitesse', score=(0, 1),
         say="Round un : la vitesse. Le Raptor monte à Mach deux virgule deux. Le Rafale plafonne à Mach un virgule huit. Point F-22.",
         show="Round 1 : la vitesse. Le Raptor monte à Mach 2,2. Le Rafale plafonne à Mach 1,8. Point F-22."),
    dict(scene='furtif', score=(0, 2),
         say="Round deux : la furtivité. Sur un radar, le F-22 aurait la taille d'une bille. Le Rafale n'est pas furtif... mais il brouille les radars ennemis. Encore le F-22.",
         show="Round 2 : la furtivité. Sur un radar, le F-22 aurait la taille d'une bille. Le Rafale n'est pas furtif… mais il brouille les radars ennemis. Encore le F-22."),
    dict(scene='poly', score=(1, 2),
         say="Round trois : la polyvalence. Le Rafale fait tout : combat aérien, frappe au sol, nucléaire, porte-avions. Le F-22 est d'abord un chasseur. Point Rafale.",
         show="Round 3 : la polyvalence. Le Rafale fait tout : combat aérien, frappe au sol, nucléaire, porte-avions. Le F-22 est d'abord un chasseur. Point Rafale."),
    dict(scene='reel', score=(2, 2),
         say="Round quatre : le combat réel. Afghanistan, Libye, Mali, Syrie pour le Rafale. Le Raptor ? Quelques frappes en Syrie... et un ballon chinois. Deux partout.",
         show="Round 4 : le combat réel. Afghanistan, Libye, Mali, Syrie pour le Rafale. Le Raptor ? Quelques frappes en Syrie… et un ballon chinois. 2 partout."),
    dict(scene='duel', score=(2, 2),
         say="Dernier round. Deux mille neuf, aux Émirats. Pendant un exercice, une image fait le tour du monde : un F-22... dans le viseur d'un Rafale.",
         show="Dernier round. 2009, aux Émirats. Pendant un exercice, une image fait le tour du monde : un F-22… dans le viseur d'un Rafale."),
    dict(scene='doute', score=(2, 2),
         say="Mais l'US Air Force n'a jamais confirmé... et les règles étaient fixées à l'avance.",
         show="Mais l'US Air Force n'a jamais confirmé… et les règles étaient fixées à l'avance."),
    dict(scene='verdict', score=(2, 2),
         say="Verdict : de loin, le F-22 tire avant d'être vu. De près, le Rafale peut gagner. Et toi, tu mets qui ? Dis-le en commentaire.",
         show="Verdict : de loin, le F-22 tire avant d'être vu. De près, le Rafale peut gagner. Et toi, tu mets qui ? Dis-le en commentaire."),
]
BREAK = 0.6
