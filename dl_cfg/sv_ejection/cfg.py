# SURVIVRAIS-TU ? : éjection à la vitesse du son. Source : migflug « What happens inside an ejection seat » [12-14 G ~0,25 s ; < 2,5 s de la poignée au parachute ;
# vent à 500 kt > 8 000 lb/ft² (~39 t/m²) ; verrière éjectée ou cordeau détonant ; zéro-zéro ; Martin-Baker > 90 % de réussite, > 7 700 vies ; certaines armées limitent le nombre d'éjections]
SERIES = "SURVIVRAIS-TU ?"; EP = "03"; MODE = "survie"
SCENES = [
    dict(type='ej_cock', title="SURVIVRAIS-TU ?",
         say="Tu voles en avion de chasse, presque à la vitesse du son. Ton avion ne répond plus. Tu tires la poignée d'éjection. Survivrais-tu aux trois secondes qui suivent ?",
         show="Tu voles en avion de chasse, presque à la vitesse du son. Ton avion ne répond plus. Tu tires la poignée d'éjection. Survivrais-tu aux 3 secondes qui suivent ?"),
    dict(type='ej_canopy', title="LA VERRIÈRE",
         say="D'abord, la verrière. Elle est éjectée, ou pulvérisée par un cordon explosif collé dans le plexiglas. Et une fraction de seconde plus tard, ton siège part.",
         show="D'abord, la verrière. Elle est éjectée, ou pulvérisée par un cordon explosif collé dans le plexiglas. Et une fraction de seconde plus tard, ton siège part."),
    dict(type='ej_g', title="14 G",
         say="La catapulte, puis une fusée sous ton siège. Tu encaisses douze à quatorze G, pendant un quart de seconde. Ta colonne vertébrale se tasse. Certaines armées limitent le nombre d'éjections dans une carrière.",
         show="La catapulte, puis une fusée sous ton siège. Tu encaisses 12 à 14 G, pendant un quart de seconde. Ta colonne vertébrale se tasse. Certaines armées limitent le nombre d'éjections dans une carrière."),
    dict(type='ej_wind', title="LE MUR D'AIR",
         say="Puis le vent. À plus de neuf cents kilomètres-heure, l'air te frappe comme un mur : des dizaines de tonnes par mètre carré. Si tes bras ne sont pas collés au corps, ils peuvent être arrachés de leur position.",
         show="Puis le vent. À plus de 900 km/h, l'air te frappe comme un mur : des dizaines de tonnes par mètre carré. Si tes bras ne sont pas collés au corps, ils peuvent être arrachés de leur position."),
    dict(type='ej_chute', title="LE PARACHUTE",
         say="Le siège se stabilise, puis te largue. Ton parachute s'ouvre. Entre la poignée et le parachute, moins de trois secondes.",
         show="Le siège se stabilise, puis te largue. Ton parachute s'ouvre. Entre la poignée et le parachute, moins de 3 secondes."),
    dict(type='ej_verdict', title="VERDICT",
         say="Verdict : tu survis, très probablement. Les sièges modernes sauvent plus de neuf pilotes sur dix. Mais à très grande vitesse, le risque de blessure grave est bien plus élevé. Et toi, tu aurais tiré la poignée ?",
         show="Verdict : tu survis, très probablement. Les sièges modernes sauvent plus de 9 pilotes sur 10. Mais à très grande vitesse, le risque de blessure grave est bien plus élevé. Et toi, tu aurais tiré la poignée ?"),
]
END_HOLD = 12.5
