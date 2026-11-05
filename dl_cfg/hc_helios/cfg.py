# GRANDS CRASHS : Helios Airways 522, « l'avion fantôme » (14/08/2005). Sources vérifiées le 05/11 : Wikipedia EN « Helios Airways Flight 522 » (rapport final AAIASB, Grèce) :
# Boeing 737-300 5B-DBY, Larnaca -> Athènes -> Prague, 121 à bord (115 passagers + 6 équipage), tous tués ; sélecteur de pressurisation laissé sur « manual » après un test
# de fuite au sol ; alarme d'altitude cabine (12 040 ft) prise pour l'alarme de configuration décollage ; masques passagers à ~18 000 ft ; contact perdu ~09:20,
# attente au-dessus de KEA (Athènes) ~70 min en pilote automatique ; F-16 ~11:24 : copilote effondré, siège du commandant vide, masques pendants ; ~11:49 une personne
# tente de reprendre le contrôle : le steward Andreas Prodromou (licence de pilote commercial britannique, pas qualifié 737) ; moteurs arrêtés faute de carburant
# (11:49:50 et 11:59:47) ; crash vers 12:03 près de Grammatiko, à ~40 km d'Athènes. vidIQ : helios 522 ~19k/mois (+450 %), ghost plane +246 %.
SERIES = "GRANDS CRASHS"; EP = "04"; MODE = "histoire"; STYLE = "cinema"
SCENES = [
    dict(type='hl_hook', title="L'AVION FANTÔME", focus=(540, 900),
         say="Un avion de ligne vole seul pendant plus d'une heure au-dessus de la Grèce. À bord, personne ne répond. Tu connais l'histoire de l'avion fantôme ?",
         show="Un avion de ligne vole seul pendant plus d'une heure au-dessus de la Grèce. À bord, personne ne répond. Tu connais l'histoire de l'avion fantôme ?"),
    dict(type='hl_switch', title="14 AOÛT 2005", focus=(540, 900),
         say="Le quatorze août deux mille cinq, un Boeing sept cent trente-sept d'Helios décolle de Chypre. Après une maintenance, un bouton de pressurisation est resté sur manuel.",
         show="Le 14 août 2005, un Boeing 737 d'Helios décolle de Chypre. Après une maintenance, un bouton de pressurisation est resté sur « manuel »."),
    dict(type='hl_alarm', title="L'ALARME", focus=(540, 900),
         say="L'avion monte, l'air se raréfie. Une alarme retentit, mais l'équipage croit à une autre panne.",
         show="L'avion monte, l'air se raréfie. Une alarme retentit, mais l'équipage croit à une autre panne."),
    dict(type='hl_hypoxia', title="HYPOXIE", focus=(540, 900),
         say="Les masques tombent en cabine. Dans le cockpit, les pilotes perdent connaissance. Le pilote automatique continue jusqu'à Athènes, et tourne en rond.",
         show="Les masques tombent en cabine. Dans le cockpit, les pilotes perdent connaissance. Le pilote automatique continue jusqu'à Athènes, et tourne en rond."),
    dict(type='hl_f16', title="LES F-16", focus=(540, 900),
         say="Deux F-16 décollent pour l'intercepter. Ils voient le copilote effondré, le siège du commandant vide, et les masques qui pendent dans la cabine.",
         show="Deux F-16 décollent pour l'intercepter. Ils voient le copilote effondré, le siège du commandant vide, et les masques qui pendent dans la cabine."),
    dict(type='hl_steward', title="UN STEWARD", focus=(540, 900),
         say="Soudain, quelqu'un entre dans le cockpit : un steward, qui a une licence de pilote. Il tente de reprendre l'avion.",
         show="Soudain, quelqu'un entre dans le cockpit : un steward, qui a une licence de pilote. Il tente de reprendre l'avion."),
    dict(type='hl_crash', title="121", focus=(540, 900),
         say="Mais les réservoirs sont vides. Un moteur s'arrête, puis l'autre, dix minutes plus tard. L'avion s'écrase près d'Athènes. Les cent vingt et une personnes à bord meurent.",
         show="Mais les réservoirs sont vides. Un moteur s'arrête, puis l'autre, 10 minutes plus tard. L'avion s'écrase près d'Athènes. Les 121 personnes à bord meurent."),
    dict(type='hl_after', title="UN BOUTON", focus=(540, 900),
         say="Tout est parti d'un bouton mal réglé. Tu aurais compris l'alarme à temps ?",
         show="Tout est parti d'un bouton mal réglé. Tu aurais compris l'alarme à temps ?"),
]
END_HOLD = 12.0
RECAP_DELAY = 3.0
RECAP = [("121", "victimes", (0.92, 0.95, 1.0)), ("1 BOUTON", "sur manuel", (1, 0.85, 0.25)), ("2 F-16", "en interception", (0.45, 0.75, 1.0))]
RECAP_NOTE = "En mémoire des 121 victimes du vol Helios 522"
