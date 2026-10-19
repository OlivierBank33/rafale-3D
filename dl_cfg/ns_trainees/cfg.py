# LA SCIENCE DU VOL 06 : les traînées blanches. Sources : planefyi.com « Contrails and Climate Impact » [vapeur chaude et humide des réacteurs + air < −40 °C, cristaux de glace sur les suies,
# critère de Schmidt-Appleman ; la plupart s'évaporent en secondes ou minutes, en air sursaturé en glace elles durent des heures et s'étalent en cirrus ; forçage des cirrus de traînées ≈ 57 mW/m²
# contre ≈ 34 mW/m² pour le CO2 de l'aviation (Lee et al.)] ; combustion du kérosène ≈ 1,2 kg d'eau par kg de carburant ; ~ −50 °C vers 11 km ; traînées des formations de bombardiers 1943-45
SERIES = "LA SCIENCE DU VOL"; EP = "06"; NEXT = "POURQUOI LE RAFALE VOLE SI LENTEMENT"
SCENES = [
    dict(type='hook', top=("−50 °C", "1,2 KG"), sub=("à 11 000 mètres", "d'eau par kg de kérosène"),
         gauges=[("TEMPÉRATURE", "−50 °C", 0.85, (0.45, 1.0, 0.92)), ("EAU REJETÉE", "1,2 KG", 0.6, (1.0, 0.55, 0.0))],
         say="Ces traînées blanches derrière les avions, ce n'est pas de la fumée. Ni des produits chimiques. C'est un nuage, fabriqué en une fraction de seconde. Comment ?",
         show="Ces traînées blanches derrière les avions, ce n'est pas de la fumée. Ni des produits chimiques. C'est un nuage, fabriqué en une fraction de seconde. Comment ?"),
    dict(type='plan', items=["LA VAPEUR", "LE FROID", "L'HUMIDITÉ", "LE CLIMAT"],
         say="Trois ingrédients. Et un effet sur le climat que peu de gens connaissent.",
         show="3 ingrédients. Et un effet sur le climat que peu de gens connaissent."),
    dict(type='vapeur', num=1, title="LA VAPEUR",
         say="Un : la vapeur. En brûlant, le kérosène fabrique de l'eau. Plus d'un kilo d'eau pour chaque kilo de carburant, rejeté en vapeur brûlante par les réacteurs.",
         show="1 : la vapeur. En brûlant, le kérosène fabrique de l'eau. Plus d'un kilo d'eau pour chaque kilo de carburant, rejeté en vapeur brûlante par les réacteurs."),
    dict(type='froid', num=2, title="LE FROID",
         say="Deux : le froid. À onze mille mètres, il fait environ moins cinquante degrés. La vapeur gèle d'un coup en minuscules cristaux de glace. C'est la buée de ton souffle, un matin d'hiver.",
         show="2 : le froid. À 11 000 mètres, il fait environ −50 °C. La vapeur gèle d'un coup en minuscules cristaux de glace. C'est la buée de ton souffle, un matin d'hiver."),
    dict(type='humide', num=3, title="L'HUMIDITÉ",
         say="Trois : l'humidité. Dans un air sec, la traînée disparaît en quelques secondes. Dans un air humide, elle reste des heures, et s'étale en vrais nuages.",
         show="3 : l'humidité. Dans un air sec, la traînée disparaît en quelques secondes. Dans un air humide, elle reste des heures, et s'étale en vrais nuages."),
    dict(type='ww2', num=None, title="1943 : LE PIÈGE",
         say="Pendant la Seconde Guerre mondiale, ces traînées trahissaient les bombardiers. Des centaines de traits blancs dans le ciel : impossible de se cacher des chasseurs ennemis.",
         show="Pendant la Seconde Guerre mondiale, ces traînées trahissaient les bombardiers. Des centaines de traits blancs dans le ciel : impossible de se cacher des chasseurs ennemis."),
    dict(type='climat', num=4, title="LE CLIMAT",
         say="Quatre : le climat. Ces nuages artificiels retiennent la chaleur de la Terre, surtout la nuit. Selon une grande étude de référence, leur effet réchauffant serait même plus fort que celui du CO deux des avions.",
         show="4 : le climat. Ces nuages artificiels retiennent la chaleur de la Terre, surtout la nuit. Selon une grande étude de référence, leur effet réchauffant serait même plus fort que celui du CO2 des avions."),
    dict(type='outro', num=None, title="ABONNE-TOI", lines=("CE N'EST PAS DE LA FUMÉE :", "C'EST UN NUAGE"),
         say="Une traînée d'avion, ce n'est pas de la fumée : c'est un nuage. Abonne-toi pour la suite de la science du vol.",
         show="Une traînée d'avion, ce n'est pas de la fumée : c'est un nuage. Abonne-toi pour la suite de la science du vol."),
]
END_HOLD = 6.5
