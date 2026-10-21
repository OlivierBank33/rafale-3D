# SURVIVRAIS-TU ? : un hublot casse à 11 000 m. Sources : Wikipedia « Time of useful consciousness » [35 000 ft (~10 700 m) : 30-60 s en montée normale, 15-30 s en décompression rapide ;
# 40 000 ft : 7-10 s] ; altitude cabine max certifiée 8 000 ft (~2 400 m) ; masques passagers à générateur chimique (~12 min ou plus) ; descente d'urgence vers 10 000 ft (~3 000 m) ;
# température extérieure ~ −50 °C vers 11 km ; brouillard soudain = condensation due à la détente de l'air
SERIES = "SURVIVRAIS-TU ?"; EP = "01"; MODE = "survie"
SCENES = [
    dict(type='cabin', title="SURVIVRAIS-TU ?",
         say="Tu es assis dans un avion de ligne, à onze mille mètres. Et d'un coup, un bruit énorme. Un hublot vient de casser. Survivrais-tu aux trente secondes qui suivent ?",
         show="Tu es assis dans un avion de ligne, à 11 000 mètres. Et d'un coup, un bruit énorme. Un hublot vient de casser. Survivrais-tu aux 30 secondes qui suivent ?"),
    dict(type='press', title="LA DÉCOMPRESSION",
         say="Dans la cabine, l'air est pressurisé comme à deux mille quatre cents mètres. Dehors, c'est onze mille. L'air s'échappe d'un coup. La cabine se remplit de brouillard, et tes oreilles claquent.",
         show="Dans la cabine, l'air est pressurisé comme à 2 400 mètres. Dehors, c'est 11 000. L'air s'échappe d'un coup. La cabine se remplit de brouillard, et tes oreilles claquent."),
    dict(type='tuc', title="LE CHRONO",
         say="Le vrai danger, ce n'est pas d'être aspiré. C'est l'oxygène. À cette altitude, après une décompression, tu as entre quinze et trente secondes avant de perdre tes moyens. Et tu ne sentiras rien venir.",
         show="Le vrai danger, ce n'est pas d'être aspiré. C'est l'oxygène. À cette altitude, après une décompression, tu as entre 15 et 30 secondes avant de perdre tes moyens. Et tu ne sentiras rien venir."),
    dict(type='hypox', title="LE PIÈGE",
         say="Le piège, c'est l'hypoxie. Ton cerveau manque d'oxygène, mais tu te sens bien. Parfois même euphorique. Tu crois avoir tout ton temps. Et tu t'éteins, sans t'en rendre compte.",
         show="Le piège, c'est l'hypoxie. Ton cerveau manque d'oxygène, mais tu te sens bien. Parfois même euphorique. Tu crois avoir tout ton temps. Et tu t'éteins, sans t'en rendre compte."),
    dict(type='mask', title="LE MASQUE",
         say="Les masques tombent. Règle d'or : tu mets le tien d'abord, avant d'aider qui que ce soit. Tu tires dessus, l'oxygène arrive. Tu as maintenant une bonne dizaine de minutes.",
         show="Les masques tombent. Règle d'or : tu mets le tien d'abord, avant d'aider qui que ce soit. Tu tires dessus, l'oxygène arrive. Tu as maintenant une bonne dizaine de minutes."),
    dict(type='dive', title="LA DESCENTE",
         say="Dans le cockpit, les pilotes plongent. Descente d'urgence vers trois mille mètres, où l'on respire sans masque. Dehors, il fait moins cinquante degrés.",
         show="Dans le cockpit, les pilotes plongent. Descente d'urgence vers 3 000 mètres, où l'on respire sans masque. Dehors, il fait −50 °C."),
    dict(type='verdict', title="VERDICT",
         say="Verdict : tu survis. Si ta ceinture est attachée, et si ton masque est sur ton visage dans les quinze premières secondes. Et toi, tu aurais tenu ?",
         show="Verdict : tu survis. Si ta ceinture est attachée, et si ton masque est sur ton visage dans les 15 premières secondes. Et toi, tu aurais tenu ?"),
]
END_HOLD = 6.0
