# HISTOIRE VRAIE : Roland Garros traverse la Méditerranée (23 sept. 1913). Sources : FAI « Centenary of first flight across Mediterranean Sea by Roland Garros »
# [Fréjus -> Bizerte, 7 h 53, près de 800 km, un peu plus de 200 L au départ, < 10 L à l'arrivée] ; Vikidia [décollage 5 h 47 Fréjus-Saint-Raphaël, arrivée 13 h 40,
# 780 km, Gnome 80 ch, 200 L d'essence, 2 pannes : au large de la Corse et au-dessus de la Sardaigne, 5 L restants] ; This Day in Aviation [Morane-Saulnier G, 756 km,
# essence pour ~8 h, tachymètre + baromètre enregistreur + compas, ~5 L restants] ; Wikipedia EN [1re traversée sans escale, 2 pannes moteur résolues en vol ;
# abattu le 5 oct. 1918 près de Vouziers, la veille de ses 30 ans ; stade Roland-Garros ouvert en 1928].
SERIES = "HISTOIRE VRAIE"; EP = "05"; MODE = "histoire"
SCENES = [
    dict(type='gr_hook', title="ROLAND-GARROS", focus=(540, 900),
         say="Tu savais que Roland-Garros n'était pas un joueur de tennis ? C'était un pilote. Et en mille neuf cent treize, il a tenté ce que personne n'avait jamais réussi.",
         show="Tu savais que Roland-Garros n'était pas un joueur de tennis ? C'était un pilote. Et en 1913, il a tenté ce que personne n'avait jamais réussi."),
    dict(type='gr_takeoff', title="5 H 47", focus=(540, 950),
         say="Vingt-trois septembre, cinq heures quarante-sept. Garros décolle de Fréjus, seul, dans un petit monoplan de bois et de toile. Objectif : traverser la Méditerranée sans escale.",
         show="23 septembre, 5 h 47. Garros décolle de Fréjus, seul, dans un petit monoplan de bois et de toile. Objectif : traverser la Méditerranée sans escale."),
    dict(type='gr_sea', title="800 KM DE MER", focus=(540, 900),
         say="Devant lui, près de huit cents kilomètres de mer, jusqu'à la Tunisie. Pas de radio. Juste une boussole, et de l'essence pour environ huit heures de vol.",
         show="Devant lui, près de 800 kilomètres de mer, jusqu'à la Tunisie. Pas de radio. Juste une boussole, et de l'essence pour environ 8 heures de vol."),
    dict(type='gr_fail', title="PANNES", focus=(540, 900),
         say="Au large de la Corse, premier problème moteur. Garros le règle, en plein vol. Au-dessus de la Sardaigne, deuxième panne. Il s'en sort encore, et il continue.",
         show="Au large de la Corse, premier problème moteur. Garros le règle, en plein vol. Au-dessus de la Sardaigne, deuxième panne. Il s'en sort encore, et il continue."),
    dict(type='gr_land', title="BIZERTE", focus=(540, 950),
         say="Treize heures quarante. La côte tunisienne. Il se pose à Bizerte, après sept heures et cinquante-trois minutes de vol. Dans son réservoir, il ne reste qu'environ cinq litres d'essence.",
         show="13 h 40. La côte tunisienne. Il se pose à Bizerte, après 7 heures et 53 minutes de vol. Dans son réservoir, il ne reste qu'environ 5 litres d'essence."),
    dict(type='gr_end', title="1918", focus=(540, 900),
         say="Cinq ans plus tard, en pleine guerre, Garros est abattu en combat aérien, la veille de ses trente ans. Dix ans après, on donne son nom à un stade de tennis. Tu connaissais son histoire ?",
         show="5 ans plus tard, en pleine guerre, Garros est abattu en combat aérien, la veille de ses 30 ans. 10 ans après, on donne son nom à un stade de tennis. Tu connaissais son histoire ?"),
]
END_HOLD = 13.5
RECAP = [("7 H 53", "de vol, sans escale", (1, 0.85, 0.25)), ("~800 KM", "au-dessus de la mer", (0.35, 0.82, 1.0)), ("5 L", "d'essence à l'arrivée", (1.0, 0.25, 0.25))]
