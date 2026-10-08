# Décodé 01 : le masque à oxygène (sources : Wikipedia « Emergency oxygen system » [chlorate de sodium + fer, goupille arrachée en tirant le masque,
# ≥ 15 min, déploiement auto > 14 000 ft, le sac peut ne pas gonfler] ; FAA via migflug [12 à 20 min, boîtier 232-260 °C, odeur de brûlé normale] ;
# Wikipedia Helios 522 [14/08/2005, 737-300 Larnaca-Athènes, pressurisation laissée sur MAN, alarme confondue, O2 passagers ~12 min,
# FL340 en pilote auto ~70 min au-dessus d'Athènes, panne sèche, Grammatiko, 121 morts] ; TUC FL340 ≈ 30 s à 1 min)
SCENES = [
    dict(type='hook', say="Onze mille mètres. Un bang, de la buée partout, et un masque tombe devant ton visage. À partir de maintenant, tu as une trentaine de secondes de lucidité.",
         show="11 000 mètres. Un bang, de la buée partout, et un masque tombe devant ton visage. À partir de maintenant, tu as une trentaine de secondes de lucidité."),
    dict(type='story', say="Histoire vraie. Quatorze août deux mille cinq. Un Boeing 737 décolle de Chypre vers Athènes. Au sol, un mécanicien a laissé la pressurisation en mode manuel. L'avion monte, et l'air de la cabine s'en va.",
         show="Histoire vraie. 14 août 2005. Un Boeing 737 décolle de Chypre vers Athènes. Au sol, un mécanicien a laissé la pressurisation en mode manuel. L'avion monte, et l'air de la cabine s'en va."),
    dict(type='alarm', say="Une alarme sonne. Les pilotes la confondent avec une autre. Au-dessus des passagers, les masques tombent.",
         show="Une alarme sonne. Les pilotes la confondent avec une autre. Au-dessus des passagers, les masques tombent."),
    dict(type='open', say="Alors, on ouvre ce panneau au-dessus de ta tête. Surprise : il n'y a pas de bouteille d'oxygène. Il y a un cylindre de métal, rempli de chlorate de sodium.",
         show="Alors, on ouvre ce panneau au-dessus de ta tête. Surprise : il n'y a pas de bouteille d'oxygène. Il y a un cylindre de métal, rempli de chlorate de sodium."),
    dict(type='chrono', say="Tu tires le masque vers toi. Le cordon arrache une goupille. Un percuteur frappe une amorce, et le bloc se met à brûler, comme une bougie, en libérant de l'oxygène pur. Et ça ne s'arrête plus.",
         show="Tu tires le masque vers toi. Le cordon arrache une goupille. Un percuteur frappe une amorce, et le bloc se met à brûler, comme une bougie, en libérant de l'oxygène pur. Et ça ne s'arrête plus."),
    dict(type='heat', say="Le cylindre dépasse deux cents degrés. Si ça sent le brûlé, c'est normal.",
         show="Le cylindre dépasse 200 degrés. Si ça sent le brûlé, c'est normal."),
    dict(type='bag', say="Et le petit sac ne gonfle pas forcément. Ce n'est pas une panne : l'oxygène passe quand même. Respire normalement.",
         show="Et le petit sac ne gonfle pas forcément. Ce n'est pas une panne : l'oxygène passe quand même. Respire normalement."),
    dict(type='descent', say="Il y en a pour douze à vingt minutes. C'est voulu : pendant ce temps, les pilotes descendent vers trois mille mètres, où l'air se respire à nouveau.",
         show="Il y en a pour 12 à 20 minutes. C'est voulu : pendant ce temps, les pilotes descendent vers 3 000 mètres, où l'air se respire à nouveau."),
    dict(type='helios', say="Sur le vol Helios, personne ne pilotait plus. Les masques se sont vidés au bout d'une douzaine de minutes, et l'avion a tourné en pilote automatique jusqu'à la panne sèche. Cent vingt et un morts.",
         show="Sur le vol Helios, personne ne pilotait plus. Les masques se sont vidés au bout d'une douzaine de minutes, et l'avion a tourné en pilote automatique jusqu'à la panne sèche. 121 morts."),
    dict(type='outro', say="Voilà pourquoi on te dit de mettre ton masque avant d'aider les autres. Tu savais qu'il chauffait autant ? Dis-le en commentaire. Prochaine fiche : pourquoi les hublots sont ronds.",
         show="Voilà pourquoi on te dit de mettre ton masque avant d'aider les autres. Tu savais qu'il chauffait autant ? Dis-le en commentaire. Prochaine fiche : pourquoi les hublots sont ronds."),
]
END_HOLD = 2.5
