# HISTOIRE VRAIE : le F-15 israélien rentré avec une seule aile. Source : Sandboxx « That time an F-15 landed without a wing » [1er mai 1983, Néguev, F-15D « Baz 957 » piloté par Ziv Nedivi
# avec l'instructeur Yehoar Gal ; collision avec un A-4N, pilote du Skyhawk éjecté ; aile droite arrachée à ~60 cm de l'emplanture ; posé à ~260 kt (~480 km/h), env. 2× la normale ;
# crosse arrachée, arrêt à ~6 m de la barrière ; Nedivi ne mesure les dégâts qu'en se retournant ; avion réparé (nouvelle aile), remis en service]
SERIES = "HISTOIRE VRAIE"; EP = "04"; MODE = "histoire"
SCENES = [
    dict(type='f_hook', title="SANS AILE ?",
         say="Un avion de chasse peut-il voler avec une seule aile ? En mille neuf cent quatre-vingt-trois, un pilote israélien a eu la réponse. Sans le vouloir.",
         show="Un avion de chasse peut-il voler avec une seule aile ? En 1983, un pilote israélien a eu la réponse. Sans le vouloir."),
    dict(type='f_train', title="1ER MAI 1983",
         say="Premier mai, au-dessus du désert du Néguev. Un F quinze biplace s'entraîne au combat aérien contre des A quatre Skyhawk.",
         show="1er mai, au-dessus du désert du Néguev. Un F-15 biplace s'entraîne au combat aérien contre des A-4 Skyhawk."),
    dict(type='f_crash', title="COLLISION",
         say="Collision. Un Skyhawk percute l'aile droite du F quinze. Le Skyhawk se disloque, son pilote s'éjecte. Le F quinze part en vrille, dans un nuage de carburant.",
         show="Collision. Un Skyhawk percute l'aile droite du F-15. Le Skyhawk se disloque, son pilote s'éjecte. Le F-15 part en vrille, dans un nuage de carburant."),
    dict(type='f_recover', title="PLEINS GAZ",
         say="Le pilote, Ziv Nedivi, met la post-combustion. Avec la vitesse, il reprend le contrôle. Il ne mesure pas les dégâts : le carburant qui s'échappe lui cache son aile.",
         show="Le pilote, Ziv Nedivi, met la post-combustion. Avec la vitesse, il reprend le contrôle. Il ne mesure pas les dégâts : le carburant qui s'échappe lui cache son aile."),
    dict(type='f_land', title="480 KM/H",
         say="Il se pose à près de quatre cent quatre-vingts kilomètres-heure, deux fois la vitesse normale. La crosse accroche le câble, et se fait arracher. L'avion s'arrête à six mètres de la barrière.",
         show="Il se pose à près de 480 km/h, deux fois la vitesse normale. La crosse accroche le câble, et se fait arracher. L'avion s'arrête à 6 mètres de la barrière."),
    dict(type='f_reveal', title="L'AILE ?",
         say="Il se retourne pour serrer la main de son instructeur. Et là, il voit enfin : son aile droite a disparu. Le fuselage, très large, portait l'avion grâce à la vitesse.",
         show="Il se retourne pour serrer la main de son instructeur. Et là, il voit enfin : son aile droite a disparu. Le fuselage, très large, portait l'avion grâce à la vitesse."),
    dict(type='f_end', title="RÉPARÉ",
         say="L'avion a reçu une nouvelle aile, et a repris du service. Tu aurais tenté l'atterrissage, ou tu te serais éjecté ? Dis-le en commentaire.",
         show="L'avion a reçu une nouvelle aile, et a repris du service. Tu aurais tenté l'atterrissage, ou tu te serais éjecté ? Dis-le en commentaire."),
]
END_HOLD = 12.5
