# SURVIVRAIS-TU ? : caché dans le train d'atterrissage. Sources : FAA via CBS Miami [128 cas recensés 1947-2020, > 75 % de morts ; causes : hypothermie, manque d'oxygène, écrasement par le train ;
# case non chauffée, non pressurisée, croisière ~38 000 ft] ; T° extérieure en croisière ~ −50 °C. Message clair : ne jamais le tenter.
SERIES = "SURVIVRAIS-TU ?"; EP = "04"; MODE = "survie"
SCENES = [
    dict(type='tw_hide', title="SURVIVRAIS-TU ?",
         say="Tu te caches dans la case du train d'atterrissage d'un avion de ligne. L'avion décolle. Ça paraît fou, mais depuis des décennies, des gens le tentent vraiment. Survivrais-tu jusqu'à l'arrivée ?",
         show="Tu te caches dans la case du train d'atterrissage d'un avion de ligne. L'avion décolle. Ça paraît fou, mais depuis des décennies, des gens le tentent vraiment. Survivrais-tu jusqu'à l'arrivée ?"),
    dict(type='tw_gear', title="LE TRAIN SE REPLIE",
         say="Premier danger, juste après le décollage : le train se replie. Les roues remontent dans la case, exactement là où tu es. S'il n'y a pas assez de place, tu es écrasé.",
         show="Premier danger, juste après le décollage : le train se replie. Les roues remontent dans la case, exactement là où tu es. S'il n'y a pas assez de place, tu es écrasé."),
    dict(type='tw_cold', title="LE FROID",
         say="Puis l'avion monte. La case du train n'est ni chauffée, ni pressurisée. Dehors, à onze mille mètres, il fait autour de moins cinquante degrés.",
         show="Puis l'avion monte. La case du train n'est ni chauffée, ni pressurisée. Dehors, à 11 000 mètres, il fait autour de −50 °C."),
    dict(type='tw_oxy', title="L'OXYGÈNE",
         say="Et l'air devient trop pauvre en oxygène. Sans masque, tu perds connaissance. Pendant des heures, ton corps se refroidit, sans que tu puisses bouger.",
         show="Et l'air devient trop pauvre en oxygène. Sans masque, tu perds connaissance. Pendant des heures, ton corps se refroidit, sans que tu puisses bouger."),
    dict(type='tw_fall', title="L'ARRIVÉE",
         say="À l'approche, le train redescend. La trappe s'ouvre sous toi. Si tu es inconscient, rien ne te retient : tu tombes, parfois de plusieurs centaines de mètres.",
         show="À l'approche, le train redescend. La trappe s'ouvre sous toi. Si tu es inconscient, rien ne te retient : tu tombes, parfois de plusieurs centaines de mètres."),
    dict(type='tw_verdict', title="VERDICT",
         say="Verdict : tu ne survis probablement pas. Sur cent vingt-huit cas recensés par l'aviation américaine depuis mille neuf cent quarante-sept, plus de trois sur quatre sont morts. Ne le tente jamais. Tu savais que c'était aussi dangereux ?",
         show="Verdict : tu ne survis probablement pas. Sur 128 cas recensés par l'aviation américaine depuis 1947, plus de 3 sur 4 sont morts. Ne le tente jamais. Tu savais que c'était aussi dangereux ?"),
]
END_HOLD = 14.0

RECAP = [("128 CAS", "recensés depuis 1947 (FAA)", (1, 0.85, 0.25)), ("−50 °C", "dehors, à 11 000 m", (0.35, 0.82, 1.0)), ("3 SUR 4", "n'ont pas survécu", (1.0, 0.25, 0.25))]
