# SURVIVRAIS-TU ? : 9 G dans un Rafale. Source : migflug « What pulling 9G does to your body » [non entraîné : perte de connaissance entre 4 et 6 G ; vision tunnel, voile gris, voile noir, G-LOC ;
# combinaison anti-G ≈ +1 G ; manœuvre de contraction (expiration forcée glotte fermée toutes les 3 s, jambes/abdos contractés) ≈ +4 G ; 80 kg -> 720 kg à 9 G] ; Rafale limité à +9 G
SERIES = "SURVIVRAIS-TU ?"; EP = "02"; MODE = "survie"
SCENES = [
    dict(type='gcock', title="SURVIVRAIS-TU ?",
         say="Tu es assis à l'arrière d'un Rafale. Le pilote tire sur le manche. Trois G. Six G. Neuf G. Survivrais-tu à neuf fois ton propre poids ?",
         show="Tu es assis à l'arrière d'un Rafale. Le pilote tire sur le manche. 3 G. 6 G. 9 G. Survivrais-tu à 9 fois ton propre poids ?"),
    dict(type='gweight', title="NEUF FOIS TON POIDS",
         say="À neuf G, tout pèse neuf fois plus lourd. Si tu fais quatre-vingts kilos, ton corps en pèse maintenant sept cent vingt. Ta tête et ton casque pèsent plus de cinquante kilos. Lever le bras devient un exploit.",
         show="À 9 G, tout pèse 9 fois plus lourd. Si tu fais 80 kilos, ton corps en pèse maintenant 720. Ta tête et ton casque pèsent plus de 50 kilos. Lever le bras devient un exploit."),
    dict(type='gblood', title="LE SANG",
         say="Et ton sang aussi pèse neuf fois plus. Il quitte ta tête et descend dans tes jambes. Ton cœur n'arrive plus à le remonter jusqu'au cerveau.",
         show="Et ton sang aussi pèse 9 fois plus. Il quitte ta tête et descend dans tes jambes. Ton cœur n'arrive plus à le remonter jusqu'au cerveau."),
    dict(type='gvision', title="LA VISION",
         say="D'abord, ta vision se rétrécit, comme dans un tunnel. Puis les couleurs disparaissent. Puis le noir complet. Et enfin, tu perds connaissance.",
         show="D'abord, ta vision se rétrécit, comme dans un tunnel. Puis les couleurs disparaissent. Puis le noir complet. Et enfin, tu perds connaissance."),
    dict(type='gsuit', title="LA COMBINAISON",
         say="Alors comment tient le pilote ? Un : sa combinaison anti-G. Des poches d'air se gonflent sur ses jambes et son ventre, et empêchent le sang de descendre.",
         show="Alors comment tient le pilote ? 1 : sa combinaison anti-G. Des poches d'air se gonflent sur ses jambes et son ventre, et empêchent le sang de descendre."),
    dict(type='gstrain', title="LA RESPIRATION",
         say="Deux : il contracte les jambes, le ventre, et force sa respiration toutes les trois secondes. Cette technique lui fait gagner environ quatre G.",
         show="2 : il contracte les jambes, le ventre, et force sa respiration toutes les 3 secondes. Cette technique lui fait gagner environ 4 G."),
    dict(type='gverdict', title="VERDICT",
         say="Verdict : sans entraînement, un humain s'évanouit en général entre quatre et six G. Toi, tu t'éteins. Le pilote, lui, reste conscient : il s'entraîne pour ça en centrifugeuse. Et toi, tu aurais tenu combien de G ?",
         show="Verdict : sans entraînement, un humain s'évanouit en général entre 4 et 6 G. Toi, tu t'éteins. Le pilote, lui, reste conscient : il s'entraîne pour ça en centrifugeuse. Et toi, tu aurais tenu combien de G ?"),
]
END_HOLD = 9.0
