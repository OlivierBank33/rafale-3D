# SURVIVRAIS-TU ? : chute libre depuis un avion de ligne, sans parachute. Sources : Popular Mechanics (D. Koeppel, « How to Fall 35,000 Feet and Survive »,
# résumé Gigazine 2016 : perte de connaissance par hypoxie, réveil vers 22 000 ft ≈ 6 700 m, ~2 min restantes, chute totale ≈ 3 min 25 ; neige et marais amortissent,
# l'eau frappe presque comme du béton ; protéger la tête) ; FAA TUC à 35 000 ft = 30 s à 1 min ; vitesse limite à plat ≈ 200 km/h ; T° ISA à 10 000 m ≈ −50 °C ;
# Alan Magee (Wikipedia) : 3 janv. 1943, B-17, ~6 700 m, verrière de la gare de Saint-Nazaire, survit ; Vesna Vulović (Wikipedia) : 26 janv. 1972, JAT 367,
# 10 160 m selon le récit officiel, coincée dans un tronçon de fuselage, pente boisée enneigée, record Guinness ; altitude contestée en 2009 (~800 m selon 2 journalistes).
SERIES = "SURVIVRAIS-TU ?"; EP = "05"; MODE = "survie"
SCENES = [
    dict(type='fl_hook', title="SURVIVRAIS-TU ?", focus=(540, 820),
         say="Tu tombes d'un avion de ligne, à dix mille mètres. Sans parachute. Ça paraît impossible, et pourtant, des gens y ont survécu. Survivrais-tu ?",
         show="Tu tombes d'un avion de ligne, à 10 000 mètres. Sans parachute. Ça paraît impossible, et pourtant, des gens y ont survécu. Survivrais-tu ?"),
    dict(type='fl_air', title="LÀ-HAUT", focus=(540, 900),
         say="Là-haut, il fait environ moins cinquante degrés, et l'air est trop pauvre en oxygène. En moins d'une minute, tu perds connaissance.",
         show="Là-haut, il fait environ −50 °C, et l'air est trop pauvre en oxygène. En moins d'une minute, tu perds connaissance."),
    dict(type='fl_wake', title="RÉVEIL", focus=(540, 900),
         say="Mais tu continues de tomber, et l'air s'épaissit. Vers six mille sept cents mètres, tu reprends connaissance. Il te reste environ deux minutes avant le sol.",
         show="Mais tu continues de tomber, et l'air s'épaissit. Vers 6 700 mètres, tu reprends connaissance. Il te reste environ 2 minutes avant le sol."),
    dict(type='fl_speed', title="200 KM/H", focus=(540, 900),
         say="Tu tombes à environ deux cents kilomètres-heure. Écarte les bras et les jambes, à plat ventre : c'est la position qui te freine le plus.",
         show="Tu tombes à environ 200 km/h. Écarte les bras et les jambes, à plat ventre : c'est la position qui te freine le plus."),
    dict(type='fl_target', title="OÙ TOMBER ?", focus=(480, 880),
         say="Ensuite, choisis où tomber. L'eau ? À cette vitesse, elle frappe presque comme du béton. Vise plutôt la neige, ou un marais. Et au dernier moment : pieds joints, genoux fléchis, tête protégée.",
         show="Ensuite, choisis où tomber. L'eau ? À cette vitesse, elle frappe presque comme du béton. Vise plutôt la neige, ou un marais. Et au dernier moment : pieds joints, genoux fléchis, tête protégée."),
    dict(type='fl_magee', title="1943", focus=(540, 950),
         say="Ça a déjà marché. En mille neuf cent quarante-trois, l'aviateur américain Alan Magee tombe de son bombardier, à six mille sept cents mètres. Il traverse la verrière de la gare de Saint-Nazaire, et il survit.",
         show="Ça a déjà marché. En 1943, l'aviateur américain Alan Magee tombe de son bombardier, à 6 700 mètres. Il traverse la verrière de la gare de Saint-Nazaire, et il survit."),
    dict(type='fl_vesna', title="1972", focus=(540, 950),
         say="En mille neuf cent soixante-douze, l'hôtesse Vesna Vulović tombe de dix mille mètres, coincée dans un morceau d'avion, sur une pente boisée et enneigée. Elle survit. C'est un record du monde, même si cette altitude est aujourd'hui contestée.",
         show="En 1972, l'hôtesse Vesna Vulović tombe de 10 000 mètres, coincée dans un morceau d'avion, sur une pente boisée et enneigée. Elle survit. C'est un record du monde, même si cette altitude est aujourd'hui contestée."),
    dict(type='fl_verdict', title="VERDICT", focus=(540, 900),
         say="Verdict : tu ne survis presque jamais. Les rares survivants avaient tous quelque chose pour amortir le choc. Et toi, tu aurais tenu ?",
         show="Verdict : tu ne survis presque jamais. Les rares survivants avaient tous quelque chose pour amortir le choc. Et toi, tu aurais tenu ?"),
]
END_HOLD = 10.0
RECAP = [("200 KM/H", "vitesse de chute à plat", (1, 0.85, 0.25)), ("2 MIN", "réveillé, avant le sol", (0.35, 0.82, 1.0)), ("6 700 M", "Magee, gare de Saint-Nazaire", (0.4, 1, 0.6))]
