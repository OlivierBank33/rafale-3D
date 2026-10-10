# Décodé 03 : la boîte noire (sources : BST/TSB Canada « Backgrounder: Flight recorders » [FDR + CVR, orange, 3 400 g, 1 100 °C 1 h, 260 °C 10 h,
# pression ~20 000 ft d'eau, balise 90 jours, CVR 2 h, A380 > 2 800 paramètres] ; AF447 : 01/06/2009 Rio-Paris, 228 personnes, enregistreurs
# remontés début mai 2011 vers 3 900 m ; BEA : sondes Pitot givrées, décrochage non identifié par l'équipage ; balise : 1 impulsion/seconde)
FICHE = "03"; TITLE = "LA BOÎTE NOIRE"; NEXT = "LE TRAIN D'ATTERRISSAGE"
SCENES = [
    dict(type='bbhook', say="Ton avion repose au fond de l'océan. Quatre mille mètres sous l'eau, dans le noir total. Une seule chose sait ce qui s'est passé.",
         show="Ton avion repose au fond de l'océan. 4 000 mètres sous l'eau, dans le noir total. Une seule chose sait ce qui s'est passé."),
    dict(type='af447', say="Histoire vraie. Premier juin deux mille neuf. Le vol Air France 447, entre Rio et Paris, disparaît au-dessus de l'Atlantique. Deux cent vingt-huit personnes à bord.",
         show="Histoire vraie. 1er juin 2009. Le vol Air France 447, entre Rio et Paris, disparaît au-dessus de l'Atlantique. 228 personnes à bord."),
    dict(type='search', say="Pendant près de deux ans, on cherche. Des robots fouillent les fonds marins. Et en mai deux mille onze, à près de quatre mille mètres, on remonte les enregistreurs. Ils fonctionnent encore.",
         show="Pendant près de deux ans, on cherche. Des robots fouillent les fonds marins. Et en mai 2011, à près de 4 000 mètres, on remonte les enregistreurs. Ils fonctionnent encore."),
    dict(type='bbopen', say="Alors, on ouvre. Surprise : la boîte noire est orange. Et il y en a deux. L'une enregistre les voix du cockpit. L'autre, des milliers de paramètres de vol.",
         show="Alors, on ouvre. Surprise : la boîte noire est orange. Et il y en a deux. L'une enregistre les voix du cockpit. L'autre, des milliers de paramètres de vol."),
    dict(type='armor', say="Leur mémoire est enfermée dans un blindage testé pour encaisser trois mille quatre cents G, une heure de feu à mille cent degrés, et la pression des grands fonds.",
         show="Leur mémoire est enfermée dans un blindage testé pour encaisser 3 400 G, une heure de feu à 1 100 degrés, et la pression des grands fonds."),
    dict(type='beacon', say="Et dès qu'elle touche l'eau, une balise se réveille. Un bip par seconde, pendant quatre-vingt-dix jours.",
         show="Et dès qu'elle touche l'eau, une balise se réveille. Un bip par seconde, pendant 90 jours."),
    dict(type='pitot', say="Pour le vol 447, les enregistreurs ont tout expliqué : des sondes de vitesse bouchées par la glace, puis un décrochage que l'équipage n'a pas compris. Depuis, les sondes ont été changées, et la formation des pilotes aussi.",
         show="Pour le vol 447, les enregistreurs ont tout expliqué : des sondes de vitesse bouchées par la glace, puis un décrochage que l'équipage n'a pas compris. Depuis, les sondes ont été changées, et la formation des pilotes aussi."),
    dict(type='bboutro', say="Voilà pourquoi chaque avion emporte ses deux boîtes orange. Tu savais qu'elles n'étaient pas noires ? Dis-le en commentaire. Prochaine fiche : le train d'atterrissage.",
         show="Voilà pourquoi chaque avion emporte ses deux boîtes orange. Tu savais qu'elles n'étaient pas noires ? Dis-le en commentaire. Prochaine fiche : le train d'atterrissage."),
]
END_HOLD = 2.5
