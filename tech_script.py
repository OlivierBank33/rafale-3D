# Technique : comment fonctionne un réacteur d'avion de ligne
# step : 0 = vue d'ensemble, 1 aspirer, 2 contourner, 3 comprimer, 4 brûler, 5 turbine, 6 éjecter, 7 récap
SCENES = [
    dict(step=0, say="Un réacteur d'avion de ligne tient en quatre mots. Et à l'intérieur, il fait assez chaud pour faire fondre ses propres pièces.",
         show="Un réacteur d'avion de ligne tient en quatre mots. Et à l'intérieur, il fait assez chaud pour faire fondre ses propres pièces."),
    dict(step=1, say="Un : aspirer. À l'avant, une énorme soufflante avale des tonnes d'air chaque minute.",
         show="Un : aspirer. À l'avant, une énorme soufflante avale des tonnes d'air chaque minute."),
    dict(step=2, say="Surprise : la plus grande partie de cet air ne passe pas dans le moteur. Il le contourne... et c'est lui qui produit l'essentiel de la poussée.",
         show="Surprise : la plus grande partie de cet air ne passe pas dans le moteur. Il le contourne... et c'est lui qui produit l'essentiel de la poussée."),
    dict(step=3, say="Deux : comprimer. Le reste de l'air traverse des dizaines de petites aubes, qui le compriment jusqu'à environ quarante fois.",
         show="Deux : comprimer. Le reste de l'air traverse des dizaines de petites aubes, qui le compriment jusqu'à environ 40 fois."),
    dict(step=4, say="Trois : brûler. On injecte du kérosène, et ça s'enflamme. Plus de mille cinq cents degrés. Plus chaud que le point de fusion des métaux qui l'entourent !",
         show="Trois : brûler. On injecte du kérosène, et ça s'enflamme. Plus de 1 500 °C. Plus chaud que le point de fusion des métaux qui l'entourent !"),
    dict(step=5, say="Alors comment ça tient ? Les aubes de la turbine sont refroidies par de l'air qui circule à l'intérieur, par de minuscules trous. Et cette turbine fait tourner la soufflante et le compresseur.",
         show="Alors comment ça tient ? Les aubes de la turbine sont refroidies par de l'air qui circule à l'intérieur, par de minuscules trous. Et cette turbine fait tourner la soufflante et le compresseur."),
    dict(step=6, say="Quatre : éjecter. L'air est rejeté vers l'arrière à grande vitesse... et l'avion est poussé vers l'avant. Action, réaction.",
         show="Quatre : éjecter. L'air est rejeté vers l'arrière à grande vitesse... et l'avion est poussé vers l'avant. Action, réaction."),
    dict(step=7, say="Aspirer, comprimer, brûler, éjecter. Quel sujet technique tu veux que je t'explique ensuite ? Dis-le en commentaire.",
         show="Aspirer, comprimer, brûler, éjecter. Quel sujet technique tu veux que je t'explique ensuite ? Dis-le en commentaire."),
]
