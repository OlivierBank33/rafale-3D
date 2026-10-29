# MYSTÈRES : la disparition de Saint-Exupéry (31/07/1944). Sources : Parc national des Calanques « L'épave de l'avion de Saint-Exupéry » [départ de Bastia (Borgo),
# P-38 Lightning, 33e groupe de reconnaissance photo, avions non armés, photos pour le futur débarquement de Provence, 44 ans ; dernier écho radar ; gourmette trouvée
# le 7/09/1998 par le pêcheur marseillais Jean-Claude Bianco ; épave à 85 m près de l'archipel de Riou ; pièces identifiées en 2000, numéro de série 2734 L confirmé
# en 2003 ; pièces exposées au musée de l'Air et de l'Espace (Le Bourget) ; gourmette gravée « Antoine de Saint-Exupéry (Consuelo) » ; Horst Rippert (mars 2008, La Provence) affirme avoir abattu un P-38, récit jugé incohérent ; cause inconnue : tir, panne, malaise...].
SERIES = "MYSTÈRES"; EP = "02"; MODE = "histoire"; STYLE = "cinema"
SCENES = [
    dict(type='sx_hook', title="SAINT-EXUPÉRY", focus=(540, 900),
         say="L'auteur du Petit Prince a disparu en plein vol. Pendant cinquante-quatre ans, personne n'a su où. Tu connais la fin de l'histoire ?",
         show="L'auteur du Petit Prince a disparu en plein vol. Pendant 54 ans, personne n'a su où. Tu connais la fin de l'histoire ?"),
    dict(type='sx_takeoff', title="31 JUILLET 1944", focus=(540, 900),
         say="Le trente et un juillet mille neuf cent quarante-quatre, Antoine de Saint-Exupéry, quarante-quatre ans, décolle de Corse aux commandes d'un P trente-huit Lightning, un avion de reconnaissance sans armes. Sa mission : photographier la Provence avant le débarquement.",
         show="Le 31 juillet 1944, Antoine de Saint-Exupéry, 44 ans, décolle de Corse aux commandes d'un P-38 Lightning, un avion de reconnaissance sans armes. Sa mission : photographier la Provence avant le débarquement."),
    dict(type='sx_vanish', title="DISPARU", focus=(540, 900),
         say="Après un dernier écho radar, l'avion disparaît. Aucune trace, aucun message.",
         show="Après un dernier écho radar, l'avion disparaît. Aucune trace, aucun message."),
    dict(type='sx_bracelet', title="1998", focus=(540, 900),
         say="En mille neuf cent quatre-vingt-dix-huit, un pêcheur marseillais remonte dans ses filets une gourmette en argent. Elle porte son nom, et celui de sa femme, Consuelo.",
         show="En 1998, un pêcheur marseillais remonte dans ses filets une gourmette en argent. Elle porte son nom, et celui de sa femme, Consuelo."),
    dict(type='sx_wreck', title="85 MÈTRES", focus=(540, 900),
         say="Des plongeurs retrouvent ensuite l'épave, par quatre-vingt-cinq mètres de fond, près de l'île de Riou, au large de Marseille. En deux mille trois, un numéro de série le confirme : c'est bien son avion. Les débris de l'avion sont aujourd'hui exposés au musée de l'Air et de l'Espace, au Bourget.",
         show="Des plongeurs retrouvent ensuite l'épave, par 85 mètres de fond, près de l'île de Riou, au large de Marseille. En 2003, un numéro de série le confirme : c'est bien son avion. Les débris de l'avion sont aujourd'hui exposés au musée de l'Air et de l'Espace, au Bourget."),
    dict(type='sx_claim', title="2008", focus=(540, 900),
         say="En deux mille huit, un ancien pilote allemand affirme l'avoir abattu ce jour-là. Mais son récit comporte des incohérences.",
         show="En 2008, un ancien pilote allemand affirme l'avoir abattu ce jour-là. Mais son récit comporte des incohérences."),
    dict(type='sx_verdict', title="LE MYSTÈRE", focus=(540, 900),
         say="Abattu, panne, malaise ? Personne ne sait vraiment ce qui s'est passé. Et toi, tu crois qu'il a été abattu ?",
         show="Abattu, panne, malaise ? Personne ne sait vraiment ce qui s'est passé. Et toi, tu crois qu'il a été abattu ?"),
]
END_HOLD = 10.0
RECAP_DELAY = 2.0
RECAP = [("1944", "la disparition", (1, 0.85, 0.25)), ("85 M", "de fond", (0.45, 0.75, 1.0)), ("2734 L", "le numéro de l'épave", (0.92, 0.95, 1.0))]
RECAP_NOTE = "Antoine de Saint-Exupéry (1900-1944)"
