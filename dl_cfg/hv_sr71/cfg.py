# HISTOIRE VRAIE : le « ground speed check » du SR-71 (récit de Brian Shul). Source : migflug « 1,842 Knots: The SR-71's famous speed check » [Cessna 90 kt, Twin Beech 125 kt,
# F/A-18 « Dusty 52 » 620 kt, « Aspen 20 » (Shul + Walt) : 1 842 kt sol, ~13 miles d'altitude, Californie du Sud] ; SR-71 en service 1966-1998 ; record absolu de vitesse 3 529,6 km/h (1976)
SERIES = "HISTOIRE VRAIE"; EP = "02"; MODE = "histoire"
SCENES = [
    dict(type='sr_hook', title="VITESSE, S'IL VOUS PLAÎT",
         say="C'est l'échange radio le plus humiliant de l'histoire de l'aviation. Et tout a commencé par une question toute bête : quelle est ma vitesse ?",
         show="C'est l'échange radio le plus humiliant de l'histoire de l'aviation. Et tout a commencé par une question toute bête : quelle est ma vitesse ?"),
    dict(type='sr_intro', title="LE SR-71",
         say="Années quatre-vingts. Un SR-71, l'avion espion américain, traverse la Californie à vingt kilomètres d'altitude. C'est l'avion à réaction le plus rapide jamais mis en service : son record dépasse trois mille cinq cents kilomètres-heure.",
         show="Années 80. Un SR-71, l'avion espion américain, traverse la Californie à 20 kilomètres d'altitude. C'est l'avion à réaction le plus rapide jamais mis en service : son record dépasse 3 500 km/h."),
    dict(type='radio1', title="LE CESSNA", plane="CESSNA", kt=90, kmh=167,
         say="Sur la fréquence, un petit Cessna demande sa vitesse sol au contrôleur de Los Angeles. Réponse : quatre-vingt-dix nœuds. Environ cent soixante-dix kilomètres-heure.",
         show="Sur la fréquence, un petit Cessna demande sa vitesse sol au contrôleur de Los Angeles. Réponse : 90 nœuds. Environ 170 km/h."),
    dict(type='radio1', title="LE BIMOTEUR", plane="TWIN BEECH", kt=125, kmh=232,
         say="Un bimoteur demande la même chose. Cent vingt-cinq nœuds. Puis un chasseur de la Navy, un F dix-huit, en remet une couche, très fier.",
         show="Un bimoteur demande la même chose. 125 nœuds. Puis un chasseur de la Navy, un F-18, en remet une couche, très fier."),
    dict(type='radio1', title="LE F-18", plane="F-18 « DUSTY 52 »", kt=620, kmh=1148,
         say="Six cent vingt nœuds. Plus de mille cent kilomètres-heure. Le pilote du F dix-huit savoure son moment.",
         show="620 nœuds. Plus de 1 100 km/h. Le pilote du F-18 savoure son moment."),
    dict(type='radio1', title="ASPEN 20", plane="SR-71 « ASPEN 20 »", kt=1842, kmh=3411,
         say="Alors l'équipage du SR-71 prend la radio. Aspen vingt, demande vitesse sol. Le contrôleur vérifie. Mille huit cent quarante-deux nœuds. Plus de trois mille quatre cents kilomètres-heure.",
         show="Alors l'équipage du SR-71 prend la radio. « Aspen 20, demande vitesse sol. » Le contrôleur vérifie. 1 842 nœuds. Plus de 3 400 km/h."),
    dict(type='sr_end', title="SILENCE RADIO",
         say="Sur la fréquence, plus personne n'a demandé sa vitesse ce jour-là. Tu connaissais cette histoire ? Dis-le en commentaire.",
         show="Sur la fréquence, plus personne n'a demandé sa vitesse ce jour-là. Tu connaissais cette histoire ? Dis-le en commentaire."),
]
END_HOLD = 9.0
