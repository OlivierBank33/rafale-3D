# HISTOIRE VRAIE / GRANDS CRASHS : vol Air France 447 Rio-Paris (1er juin 2009). Sources : BEA rapport final (5 juil. 2012) via Wikipedia EN « Air France Flight 447 »
# [A330-203 F-GZCP, 228 personnes (216 passagers, 12 équipage) ; décollage Rio 31/05 22:29 UTC ; commandant au repos 02:01:46 ; déconnexion AP 02:10:05 après vitesses
# incohérentes (obstruction probable des sondes Pitot par des cristaux de glace) ; entrées à cabrer du PF ; ~38 000 ft max à 02:11:10 ; alarme de décrochage (continue 54 s) ;
# commandant de retour ~02:11:40 ; incidence > 35° jusqu'à l'impact ; fin des données 02:14:28 ; Vz ≈ -10 912 ft/min (≈ 200 km/h) ; assiette +16° à l'impact ; épave localisée
# le 3 avril 2011 à 3 980 m ; enregistreurs remontés les 1er-3 mai 2011 ; sondes remplacées, formation renforcée] ; Vikidia (vitesse verticale « près de 200 km/h », +16°) ;
# TourMaG / Reuters 21 mai 2026 : Air France et Airbus condamnés en appel pour homicides involontaires (225 000 € chacun) ; Airbus s'est pourvu en cassation.
# Ton : factuel et respectueux (228 victimes) ; pas de citation du CVR ; pas de jugement au-delà du BEA et de la cour d'appel.
SERIES = "HISTOIRE VRAIE"; EP = "06"; MODE = "histoire"
SCENES = [
    dict(type='af_hook', title="RIO – PARIS", focus=(540, 900),
         say="Ses deux moteurs fonctionnaient. Ses ailes étaient intactes. Pourtant, en quatre minutes, l'Airbus du Rio-Paris est tombé dans l'océan. Tu sais pourquoi ?",
         show="Ses deux moteurs fonctionnaient. Ses ailes étaient intactes. Pourtant, en 4 minutes, l'Airbus du Rio-Paris est tombé dans l'océan. Tu sais pourquoi ?"),
    dict(type='af_night', title="1ER JUIN 2009", focus=(540, 900),
         say="Premier juin deux mille neuf, deux heures du matin. Le vol Air France quatre cent quarante-sept traverse l'Atlantique avec deux cent vingt-huit personnes à bord. Le commandant est parti se reposer. Deux copilotes sont aux commandes.",
         show="1er juin 2009, 2 heures du matin. Le vol Air France 447 traverse l'Atlantique avec 228 personnes à bord. Le commandant est parti se reposer. Deux copilotes sont aux commandes."),
    dict(type='af_storm', title="L'ORAGE", focus=(540, 900),
         say="Devant eux, une zone orageuse. L'avion traverse des nuages chargés de cristaux de glace.",
         show="Devant eux, une zone orageuse. L'avion traverse des nuages chargés de cristaux de glace."),
    dict(type='af_pitot', title="LES SONDES", focus=(540, 900),
         say="Les sondes Pitot, ces petits tubes qui mesurent la vitesse, se bouchent, sans doute à cause de la glace. Les vitesses affichées deviennent fausses. Le pilote automatique se déconnecte.",
         show="Les sondes Pitot, ces petits tubes qui mesurent la vitesse, se bouchent, sans doute à cause de la glace. Les vitesses affichées deviennent fausses. Le pilote automatique se déconnecte."),
    dict(type='af_climb', title="À CABRER", focus=(540, 900),
         say="Le copilote aux commandes tire sur le manche. L'avion monte, monte, et perd de la vitesse.",
         show="Le copilote aux commandes tire sur le manche. L'avion monte, monte, et perd de la vitesse."),
    dict(type='af_stall', title="DÉCROCHAGE", focus=(540, 900),
         say="L'alarme retentit : décrochage. L'aile ne porte plus. Il faudrait pousser sur le manche. Mais il continue, presque tout le temps, de tirer.",
         show="L'alarme retentit : décrochage. L'aile ne porte plus. Il faudrait pousser sur le manche. Mais il continue, presque tout le temps, de tirer."),
    dict(type='af_captain', title="LE COMMANDANT", focus=(540, 900),
         say="Une minute et demie plus tard, le commandant revient. Les alarmes s'enchaînent. Personne ne comprend que l'avion a décroché.",
         show="Une minute et demie plus tard, le commandant revient. Les alarmes s'enchaînent. Personne ne comprend que l'avion a décroché."),
    dict(type='af_fall', title="4 MIN 23", focus=(540, 900),
         say="L'avion tombe, nez vers le haut, à près de deux cents kilomètres-heure vers le bas. Il touche l'océan quatre minutes et vingt-trois secondes après la déconnexion du pilote automatique. Aucun survivant.",
         show="L'avion tombe, nez vers le haut, à près de 200 km/h vers le bas. Il touche l'océan 4 minutes et 23 secondes après la déconnexion du pilote automatique. Aucun survivant."),
    dict(type='af_search', title="3 980 M", focus=(540, 900),
         say="Il faudra près de deux ans pour retrouver l'épave, à près de quatre mille mètres de fond, et les boîtes noires.",
         show="Il faudra près de 2 ans pour retrouver l'épave, à près de 4 000 mètres de fond, et les boîtes noires."),
    dict(type='af_after', title="APRÈS", focus=(540, 900),
         say="Depuis, les sondes ont été remplacées et la formation des pilotes au décrochage renforcée. En mai deux mille vingt-six, Air France et Airbus ont été condamnés en appel pour homicides involontaires. Tu connaissais cette histoire ?",
         show="Depuis, les sondes ont été remplacées et la formation des pilotes au décrochage renforcée. En mai 2026, Air France et Airbus ont été condamnés en appel pour homicides involontaires. Tu connaissais cette histoire ?"),
]
END_HOLD = 11.5
RECAP_DELAY = 3.2
RECAP = [("4 MIN 23", "de la déconnexion à l'océan", (1.0, 0.3, 0.3)), ("228", "personnes à bord", (0.92, 0.95, 1.0)), ("3 980 M", "profondeur de l'épave", (0.35, 0.75, 1.0))]
RECAP_NOTE = "En mémoire des 228 victimes du vol AF447"
