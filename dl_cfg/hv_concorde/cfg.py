# GRANDS CRASHS : Concorde, vol Air France 4590 (25 juillet 2000, Gonesse). Sources : Wikipedia EN « Air France Flight 4590 » (rapport BEA du 16/01/2002) [F-BTSC ;
# 109 à bord (100 passagers, 9 équipage) + 4 au sol = 113 morts ; DC-10 Continental 55 décollé à 16:38 de la même piste, perd une lamelle d'usure en titane (~435 mm) ;
# Concorde à ~300 km/h roule dessus à 16:42 : pneu n° 2 éclaté, fragment ~4,5 kg frappe l'intrados à ~500 km/h ; onde de pression -> rupture du réservoir 5 ; kérosène enflammé ;
# moteurs 1 et 2 perdent de la poussée ; train qui ne remonte pas ; V1 dépassée ; s'écrase sur l'hôtel de Gonesse ~2 min après le décollage ; modifications : Kevlar
# dans les réservoirs, pneus anti-éclatement ; retour en service 7/11/2001 ; arrêt Air France mai 2003, BA oct. 2003 ; justice : Continental condamnée en 2010, relaxée au pénal
# en appel en 2012, responsable civilement à 70 %]. Ton respectueux.
SERIES = "GRANDS CRASHS"; EP = "02"; MODE = "histoire"
SCENES = [
    dict(type='co_hook', title="CONCORDE", focus=(540, 900),
         say="Tu savais qu'une lamelle de métal de quarante-trois centimètres a fait tomber le Concorde ?",
         show="Tu savais qu'une lamelle de métal de 43 centimètres a fait tomber le Concorde ?"),
    dict(type='co_dc10', title="25 JUILLET 2000", focus=(540, 900),
         say="Vingt-cinq juillet deux mille, aéroport de Roissy. Quatre minutes avant le Concorde, un DC-10 décolle de la même piste. Et il perd une lamelle de métal.",
         show="25 juillet 2000, aéroport de Roissy. 4 minutes avant le Concorde, un DC-10 décolle de la même piste. Et il perd une lamelle de métal."),
    dict(type='co_roll', title="300 KM/H", focus=(540, 900),
         say="Le Concorde accélère. À trois cents kilomètres-heure, une de ses roues passe dessus. Le pneu éclate.",
         show="Le Concorde accélère. À 300 km/h, une de ses roues passe dessus. Le pneu éclate."),
    dict(type='co_tank', title="LE RÉSERVOIR", focus=(540, 900),
         say="Un morceau de pneu de quatre kilos et demi frappe l'aile à environ cinq cents kilomètres-heure. L'onde de choc fait céder un réservoir. Le kérosène s'enflamme.",
         show="Un morceau de pneu de 4,5 kg frappe l'aile à environ 500 km/h. L'onde de choc fait céder un réservoir. Le kérosène s'enflamme."),
    dict(type='co_fire', title="EN FEU", focus=(540, 900),
         say="Trop tard pour freiner : l'avion décolle, en feu. Deux moteurs perdent de la puissance. Et le train d'atterrissage refuse de remonter.",
         show="Trop tard pour freiner : l'avion décolle, en feu. Deux moteurs perdent de la puissance. Et le train d'atterrissage refuse de remonter."),
    dict(type='co_crash', title="GONESSE", focus=(540, 900),
         say="Le Concorde ne prend pas assez de vitesse. Environ deux minutes après le décollage, il s'écrase sur un hôtel, à Gonesse. Cent treize morts, dont quatre au sol.",
         show="Le Concorde ne prend pas assez de vitesse. Environ 2 minutes après le décollage, il s'écrase sur un hôtel, à Gonesse. 113 morts, dont 4 au sol."),
    dict(type='co_after', title="LA FIN", focus=(540, 900),
         say="Le Concorde reçoit des réservoirs doublés de Kevlar et des pneus renforcés. Il revole en novembre deux mille un. Mais en deux mille trois, il est retiré pour toujours. Tu te souviens du Concorde ?",
         show="Le Concorde reçoit des réservoirs doublés de Kevlar et des pneus renforcés. Il revole en novembre 2001. Mais en 2003, il est retiré pour toujours. Tu te souviens du Concorde ?"),
]
END_HOLD = 13.5
RECAP_DELAY = 3.0
RECAP = [("43 CM", "la lamelle de métal", (1, 0.85, 0.25)), ("4,5 KG", "le morceau de pneu", (1.0, 0.3, 0.3)), ("113", "victimes", (0.92, 0.95, 1.0))]
RECAP_NOTE = "En mémoire des 113 victimes du vol AF4590"
