# SURVIVRAIS-TU ? : pare-brise qui explose, Sichuan Airlines 3U8633 (14/05/2018). Sources : Aviation Safety Network wikibase 211013 [A319-133 B-6419,
# Chongqing -> Lhassa, croisière 9 800 m (32 100 ft), pare-brise DROIT fissuré à 07:07:05 puis arraché, copilote soufflé de son siège, pilote automatique
# déconnecté, déroutement Chengdu Shuangliu (ILS 02R), arrêt vers 07:41, 128 personnes ; cause probable : joint du pare-brise endommagé -> vapeur d'eau ->
# isolation de l'alimentation (chauffage) dégradée -> arc électrique continu -> rupture du verre double, puis différence de pression] ; CBS News 15/05/2018
# [« halfway out of the window », ceinture attachée, bruit énorme, vibrations « impossible de lire les instruments », atterrissage ~20 min, 128 survivants] ;
# Gulf News [« Everything in the cockpit was floating in the air », radio inaudible, atterrissage manuel, copilote : égratignures + poignet foulé (CAAC),
# 1 membre d'équipage de cabine blessé, 119 passagers]. Température extérieure à 9 800 m ≈ -40 à -50 °C (atmosphère standard) -> « près de -40 ».
# Avion 3D : FlightGear A320-family (A319), livrée neutre blanche (pas de logo de compagnie) pr/A319_white.png.
SERIES = "SURVIVRAIS-TU ?"; EP = "07"; MODE = "survie"; STYLE = "cinema"
SCENES = [
    dict(type='sw_hook', title="SURVIVRAIS-TU ?", focus=(540, 900),
         say="Ton pare-brise explose à près de dix mille mètres. Ton copilote est aspiré à moitié dehors. Survivrais-tu ?",
         show="Ton pare-brise explose à près de 10 000 mètres. Ton copilote est aspiré à moitié dehors. Survivrais-tu ?"),
    dict(type='sw_real', title="HISTOIRE VRAIE", focus=(540, 900),
         say="C'est arrivé pour de vrai, le quatorze mai deux mille dix-huit. Un Airbus A319 chinois, cent vingt-huit personnes à bord, en route vers le Tibet.",
         show="C'est arrivé pour de vrai, le 14 mai 2018. Un Airbus A319 chinois, 128 personnes à bord, en route vers le Tibet."),
    dict(type='sw_crack', title="9 800 M", focus=(540, 900),
         say="En croisière, à neuf mille huit cents mètres, le pare-brise droit se fissure. Puis il cède d'un coup.",
         show="En croisière, à 9 800 mètres, le pare-brise droit se fissure. Puis il cède d'un coup."),
    dict(type='sw_decomp', title="DÉPRESSURISATION", focus=(540, 900),
         say="Le cockpit se dépressurise. Le copilote est aspiré à moitié hors de l'avion. Seule sa ceinture le retient.",
         show="Le cockpit se dépressurise. Le copilote est aspiré à moitié hors de l'avion. Seule sa ceinture le retient."),
    dict(type='sw_cold', title="−40 °C", focus=(540, 900),
         say="Dehors, il fait près de moins quarante degrés. Le bruit est assourdissant, et tout vole dans le cockpit.",
         show="Dehors, il fait près de -40 °C. Le bruit est assourdissant, et tout vole dans le cockpit."),
    dict(type='sw_shake', title="PILOTE AUTO COUPÉ", focus=(540, 900),
         say="Le pilote automatique s'est coupé. L'avion tremble tellement que le commandant ne peut plus lire ses instruments.",
         show="Le pilote automatique s'est coupé. L'avion tremble tellement que le commandant ne peut plus lire ses instruments."),
    dict(type='sw_manual', title="À LA MAIN", focus=(540, 900),
         say="Il pilote à la main, descend, et se dirige vers l'aéroport de Chengdu.",
         show="Il pilote à la main, descend, et se dirige vers l'aéroport de Chengdu."),
    dict(type='sw_land', title="CHENGDU", focus=(540, 900),
         say="Une vingtaine de minutes plus tard, il se pose. Le copilote a pu revenir dans le cockpit : il s'en sort avec des égratignures et un poignet foulé.",
         show="Une vingtaine de minutes plus tard, il se pose. Le copilote a pu revenir dans le cockpit : il s'en sort avec des égratignures et un poignet foulé."),
    dict(type='sw_verdict', title="VERDICT", focus=(540, 900),
         say="Verdict : les cent vingt-huit personnes à bord survivent. En cause : de l'humidité dans le joint du pare-brise, qui a provoqué un arc électrique. Et toi, tu aurais gardé ton sang-froid ?",
         show="Verdict : les 128 personnes à bord survivent. En cause : de l'humidité dans le joint du pare-brise, qui a provoqué un arc électrique. Et toi, tu aurais gardé ton sang-froid ?"),
]
END_HOLD = 10.0
RECAP_DELAY = 1.5
RECAP = [("9 800 M", "l'altitude de croisière", (1, 0.85, 0.25)), ("−40 °C", "dehors", (0.55, 0.85, 1.0)), ("128", "survivants", (0.4, 1, 0.6))]
