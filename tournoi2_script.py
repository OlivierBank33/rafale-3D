# Tournoi #2 — avions militaires
PLANES = {'b52': 'B-52 Stratofortress', 'c130': 'C-130 Hercules', 'f15': 'F-15 Eagle', 'f16': 'F-16 Falcon',
          'typhoon': 'Eurofighter Typhoon', 'harrier': 'Harrier', 'mig21': 'MiG-21', 'f35': 'F-35 Lightning II'}
SHORT = {'b52': 'B-52', 'c130': 'C-130', 'f15': 'F-15', 'f16': 'F-16', 'typhoon': 'TYPHOON', 'harrier': 'HARRIER', 'mig21': 'MIG-21', 'f35': 'F-35'}
BRACKET = ['b52', 'c130', 'f15', 'f16', 'typhoon', 'harrier', 'mig21', 'f35']
SF_ENT = ['b52', 'f15', 'harrier', 'mig21']
F_ENT = ['b52', 'mig21']
QF_LOSERS = {'c130', 'f16', 'typhoon', 'f35'}
SF_LOSERS = {'f15', 'harrier'}
CHAMP_KEY = 'mig21'; CHAMP_NAME = 'MIG-21'; FINAL_SCORE = 'FINALE GAGNÉE 2 – 1'

INTRO = "Huit avions militaires. Un seul champion. Et le vainqueur va te surprendre. Devine qui passe à chaque duel !"
SEMIS = "Demi-finales !"
FINAL_INTRO = "La grande finale ! Le bé cinquante-deux contre le Migue vingt-et-un. En trois manches."
OUTRO = "Tu l'avais vu venir ? Dis-moi sur qui tu avais parié, en commentaire !"

DUELS = [
    dict(rnd='QUART DE FINALE 1', a='b52', b='c130', crit='LA PLUS GRANDE ENVERGURE ?',
         va=56.4, vb=40.4, la='56,4 m', lb='40,4 m', win='a',
         q="Premier duel : le bé cinquante-deux contre le cé cent trente Hercule. Qui a la plus grande envergure ?",
         r="Le bé cinquante-deux ! Cinquante-six mètres, contre quarante pour l'Hercule."),
    dict(rnd='QUART DE FINALE 2', a='f15', b='f16', crit='QUI EST LE PLUS RAPIDE ?',
         va=2.5, vb=2.0, la='Mach 2,5', lb='Mach 2', win='a',
         q="Le F quinze contre le F seize. Qui est le plus rapide ?",
         r="Le F quinze ! Mach deux virgule cinq, contre Mach deux pour le F seize."),
    dict(rnd='QUART DE FINALE 3', a='typhoon', b='harrier', crit='QUI DÉCOLLE À LA VERTICALE ?',
         va=0, vb=1, la='NON', lb='OUI', win='b',
         q="L'Euro-faïteur Taïfoune contre le Harrieur. Qui peut décoller à la verticale ?",
         r="Le Harrieur ! Ses tuyères pivotent vers le bas. Le Taïfoune, lui, a besoin d'une piste."),
    dict(rnd='QUART DE FINALE 4', a='mig21', b='f35', crit='LE PLUS CONSTRUIT ?',
         va=11000, vb=1000, la='+ de 11 000', lb='+ de 1 000', win='a',
         q="Le Migue vingt-et-un contre le F trente-cinq. Lequel a été construit en plus grand nombre ?",
         r="Le Migue ! Plus de onze mille exemplaires. Le chasseur supersonique le plus produit de l'histoire."),
    dict(rnd='DEMI-FINALE 1', a='b52', b='f15', crit='LE PLUS ANCIEN EN SERVICE ?',
         va=71, vb=50, la='depuis 1955', lb='depuis 1976', win='a',
         q="Le bé cinquante-deux contre le F quinze. Lequel est en service depuis le plus longtemps ?",
         r="Le bé cinquante-deux ! En service depuis mille neuf cent cinquante-cinq. Plus de soixante-dix ans !"),
    dict(rnd='DEMI-FINALE 2', a='harrier', b='mig21', crit='QUI EST LE PLUS RAPIDE ?',
         va=0.95, vb=2.05, la='subsonique', lb='Mach 2', win='b',
         q="Le Harrieur contre le Migue vingt-et-un. Qui est le plus rapide ?",
         r="Le Migue ! Plus de deux fois la vitesse du son. Le Harrieur ne passe pas le mur du son en palier."),
]
FINAL = [
    dict(rnd='FINALE · MANCHE 1', a='b52', b='mig21', crit='ENVERGURE',
         va=56.4, vb=7.2, la='56,4 m', lb='7,2 m', win='a',
         q="Manche un : l'envergure.",
         r="Cinquante-six mètres contre sept. Un zéro pour le bé cinquante-deux !"),
    dict(rnd='FINALE · MANCHE 2', a='b52', b='mig21', crit='VITESSE MAX',
         va=1000, vb=2175, la='1 000 km/h', lb='2 175 km/h', win='b',
         q="Manche deux : la vitesse.",
         r="Plus de deux mille kilomètres heure pour le Migue. Un partout !"),
    dict(rnd='FINALE · MANCHE 3', a='b52', b='mig21', crit='EXEMPLAIRES CONSTRUITS',
         va=744, vb=11000, la='744', lb='+ de 11 000', win='b',
         q="Dernière manche : le nombre d'exemplaires construits. Tout se joue ici.",
         r="Sept cent quarante-quatre bé cinquante-deux, contre plus de onze mille Migue. Le Migue vingt-et-un est champion !"),
]
