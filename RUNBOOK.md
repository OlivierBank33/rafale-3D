# minuteaero — Runbook de production (version du 02/10/2026 au soir — fait foi)

Compte : **@minuteaero** sur TikTok + YouTube Shorts (UCQMD5dRsF3wBsJLOSSkWIKw) + Page Facebook (Reels, 1384175288106569), via Metricool (blogId `7174127`, fuseau `Europe/Paris`, essai Starter jusqu'au ~02/11).
Propriétaire : Olivier (veut rester anonyme : jamais son nom/visage/voix réelle). Langue : **français**. Olivier délègue TOUTES les décisions éditoriales : choisir ce qui a le plus de potentiel, tester, trancher sur les chiffres.

## 0. Règles non négociables
- **3 vidéos par jour** à **10 h 00, 12 h 30, 18 h 00** (pics d'audience Metricool). 1 post par réseau (TikTok, YouTube, Facebook) à la même heure.
- Durée **65–110 s**. Faits vérifiés par recherche web ; préciser à l'écran ce que représente un chiffre (prix catalogue, record, coût programme…).
- `tiktokData.isAigc = false`, `youtubeData.isAiGeneratedContent = false` (demande explicite d'Olivier). `tiktokData.title` obligatoire.
- **Zéro bruit blanc** dans la musique/bruitages : sinus uniquement (`noise_check.py` bloque sinon). Bed à −30 LUFS, filigrane auto (eleven_prep.sh).
- **Pas de tremblement** : aucune secousse ni coup de zoom rythmé (rejeté par Olivier le 06/10) ; seulement une dérive lente.
- Voix principale : **Corentin IHngRooVccHyPqB4uQkG** (la plus rapide ; Olivier trouvait Yariq trop lent). Viser des vidéos de 61-75 s avec un débit rapide plutôt que de longues pauses ; si la voix fait < 58 s, allonger END_HOLD (carton final).
- Voix : **ElevenLabs TTS direct uniquement** (eleven_multilingual_v2, 1 génération). Jamais de voice-changer. Lancer UNIQUEMENT le nœud composition (estimate_only d'abord = 0 crédit) — relancer le nœud voix facture deux fois.
- Jamais de rendu cassé : planche de contrôle avant publication. Jamais deux fois le même sujet (`history.json`).

- **Mascotte pilote** (`mascot.py`, demandée par Olivier le 06/10) : pilote dessiné en code, casque blanc visière relevée, combinaison verte, ailes dorées, bande MINUTEAERO. Expressions smile/happy/surprised/think/doubt/wink, poses think/thumb, bouche synchronisée sur la voix, clignements. ACTIVE avec les 19 stickers Gemini d Olivier (mascot/stickers/, détourés) : neutral + bouche talk/talk_wide + blink collés par masque = lip-sync ; réactions point_up/laugh/celebrate/shocked aux points, skeptical au départ des barres, wink_thumb sur le carton final. Ancienne version vectorielle rejetée (mascot_vector_old.py) ; sous-titres décalés à droite. À ajouter aux vrai/faux et quiz quand la mise en page aura été adaptée (réactions à la révélation).

## 1bis. Méthode « viral » appliquée à TOUTES les vidéos (demande d'Olivier le 06/10)
Analyse de nos chiffres TikTok (au 06/10) : Rafale vs F-22 2 381 · VF avions légendaires 2 098 · VF avions de ligne 1 313 · quiz pilote 1 099 · Rafale vs Typhoon 894 · quiz silhouettes combat 666 (meilleur taux de likes) · prix 273 · duel F-16 vs MiG-21 257.
- **Accroche** : ce qui marche = rivalité tribale avec un camp FRANÇAIS (Rafale vs F-22) ou un jeu où le spectateur se teste (vrai/faux, quiz). Ce qui ne marche pas = contenu passif (prix, top, bio) et duels sans camp français (F-16/MiG-21 : 257). → Prioriser les duels « France vs le monde » (backlog réordonné : Rafale vs F-35, Mirage 2000 vs F-16, Mirage III vs MiG-21, Blériot vs Wright).
- **2 premières secondes** : texte à l'écran = question fermée et clivante (« LE RAFALE PEUT-IL BATTRE LE F-35 ? »), les deux avions visibles, voix qui démarre sans intro ni logo.
- **Structure duel** (rôle de chaque ligne) : accroche/enjeu (0–4 s) → round 1 facile pour l'adversaire (tension) → rounds 2–4 qui alternent (le score ne doit jamais être plié avant le round 5) → round 5 = argument surprise → verdict nuancé et contestable → CTA « Et toi, tu mets qui ? ».
- **Structure vrai/faux/quiz** : annonce du défi + « le dernier piège tout le monde » → items du plus facile au plus dur → un FAUX contre-intuitif tous les 2 items → dernier item = piège → « combien sur 8 ? écris ton score ».
- **Voix de la chaîne** : tutoiement, phrases de 5 à 12 mots, un chiffre précis par phrase, ponctuation de commentateur (« Point Rafale. » « Deux partout. »), jamais de superlatif creux (« incroyable », « dingue »), jamais de jargon non expliqué, aucun emoji dans la voix ; 1-2 emojis max dans la légende.
- **Copiable vs chance** : copiable = rivalité + camp français + score serré + CTA commentaire + format jeu. Non copiable = l'effet F-22 (avion star), le timing du 02/10, l'audience déjà acquise (36,9 k).
- **Lancement** : légende = la question du hook + 4-6 hashtags ; premier commentaire (firstCommentText, YouTube/Facebook) = « Mon pronostic : [X]. Tu valides ou pas ? » pour amorcer les réponses.
- **Ce qui tue la portée** : intro lente, image qui tremble (secousses supprimées le 06/10), vidéo sans camp français, fait contestable (perte de crédibilité en commentaires), > 90 s sans relance, même format 2 jours de suite au même créneau.
- **Tester** : 1 variable à la fois sur 3 vidéos (ex. accroche question vs accroche chiffre choc) et comparer vues 48 h + taux de commentaires.

## 1ter. Veille vidIQ (06/10) — ce qui explose en aviation FR (TikTok/Reels, 3 derniers mois)
- Récits racontés sur images cinématiques (simulateur/3D) : interception d'un A330 par un Rafale en Auvergne 1,5 M (4x la médiane du compte) ; mission DCS « le missile Harpoon » 281 k et 129 k (18x).
- Anecdote radio vraie : la Patrouille de France appelée « Air France » 4,5 M (28x) et 1,5 M.
- Montage cinématique calé sur la musique (F-16) 1,2 M ; cockpit expliqué (737) 2,2 M (accès réel, non copiable).
- → Nos animations de stats sont un bon format « jeu », mais ce qui fait des millions = HISTOIRE VRAIE + IMAGES RÉALISTES + voix dramatique dès la 1re seconde.
- Nouveau format « RÉCIT » (2x/semaine à 12:30) — moteur rc_render.py (DL=dl/<slug>, cfg type hook/story/radio/ask/punch/verdict, mascotte narratrice, ciel haute altitude ; voix via dl_tts.py, musique dl_audio.py, el_sync rc:<slug>) : anecdote vraie et sourcée (SR-71 « ground speed check », F-15 israélien rentré avec une seule aile en 1983, Gimli Glider, Hudson…), plans 3D animés dans Blender (nos modèles), stock Pexels via vidIQ (1 crédit), plan IA ElevenLabs seulement pour l'accroche si besoin (~7 300 crédits / 8 s).
- vidIQ = 150 crédits/mois (plan gratuit, renouvellement le 06/11) : 1 recherche d'outliers par semaine (5 crédits) + mots-clés en hausse ; ne pas utiliser vidiq_compose (1 crédit / 4 s) sauf test.

## 1. Stratégie éditoriale (décidée le 02/10 sur les stats)
Stats semaine 1 (TikTok, 36,9 k abonnés) : vrai/faux 1 968 et 1 240 vues, quiz niveau pilote 1 069, tournoi 731, top vitesse 313, partages ≈ 0.
- **DUEL TOUS LES JOURS à 18:00** (demande d'Olivier le 04/10 : le duel Rafale vs F-22 a été la meilleure vidéo). Moteur générique : écrire `dl/<slug>/cfg.py` (A, B, FLIP, SCENES ; copier dl/rafale_typhoon/cfg.py comme modèle), rendre 4 vues par avion `a_34/a_side/a_front/a_top.png` et `b_*.png` (render3d.py / render_fg.py / render_glb.py, az 215/180|270/270|180/88 selon l'orientation du modèle — contrôler la planche, retirer train/feux via skip), `DL=dl/<slug> python3 dl_tts.py`, `python3 pipe/el_sync.py plan dl:<slug>`, voix ElevenLabs, `el_sync.py apply dl:<slug> <durée>`, `DL=dl/<slug> python3 dl_render.py`, `DL=dl/<slug> python3 dl_audio.py`, `eleven_prep.sh dl/<slug> <nom>`. 5 rounds factuels sourcés, score qui reste serré jusqu'au bout, verdict nuancé + « Et toi, tu mets qui ? ». Choisir dans `history.json > duel_backlog` (rayer après usage).
- **Cœur (1 à 2 vidéos/jour)** : formats « je joue » = vrai ou faux, quiz (silhouette, devine le prix, devine l'année), duels A vs B (rounds + score + verdict). Ce sont ceux qui font commenter.
- **Pari viral (1 vidéo/jour)** : classements visuels à comparaison d'échelle (prix avec piles de billets `px_*`, taille, vitesse, altitude), « et si… ? », crashs qui ont changé l'aviation (sobre, sans voyeurisme).
- **Bio / technique** : max 2 par semaine, seulement si les stats les justifient.
- Accroche : chiffre ou question choc dans les 2 premières secondes, texte à l'écran dès la 1re image.
- Chaque dimanche : relever vues, temps moyen, partages, abonnés gagnés par vidéo (Metricool `getAnalyticsDataByMetrics` TKPO07/08/10/13/15) → ajuster la répartition (doubler le gagnant, couper ce qui fait < 50 % de la médiane deux semaines de suite).
- **Décision au 01/11** : médiane ≥ 3 000 vues/vidéo ou une vidéo ≥ 100 k → on garde Metricool Starter et le rythme ; médiane < 1 500 → 1 vidéo/jour et proposer à Olivier de couper les abonnements.
- **Bilan hebdo du 04/10** (TikTok, 12 vidéos du 30/09 au 02/10 visibles dans Metricool ; médiane ≈ 1 080 vues, abonnés stables ≈ 36,9 k, partages 0–6) : vrai/faux avions légendaires 2 098, duel Rafale vs F-22 1 871, vrai/faux avion de ligne 1 313, quiz pilote 1 099, tournoi militaires 1 092, tech réacteur 881, quiz légendes 627, top vitesse 514, Blériot (version bruitée) 353. → On confirme : **18:00 duel**, **10:00 vrai/faux** (n°1 des formats), **12:30 quiz/prix/tournoi en rotation**. Top vitesse < 50 % de la médiane (1re semaine) : à couper si ça se répète la semaine prochaine. Bio/tech : max 1 par semaine tant qu'elles restent sous la médiane.
- Test des voix : Yariq Ht4OibD14Nq9LzMUT7HK, Kev jGpnMdbhtKgQbVrYezOx, Guillaume 3HZyQcLKlT0a3RDeXVsP, Léa KSyQzmsYhFbuOhqj1Xxv — tourner sur les 3 créneaux, bilan le 11/10 (rétention, vues 48 h).

## 2. Installation
```bash
cd /home/claude && git clone -q --depth 1 -b minuteaero-pipeline https://github.com/OlivierBank33/rafale-3D pipe && cp -r pipe/* /home/claude/ && bash setup.sh
```
Si accès refusé : `add_repo` (OlivierBank33 / rafale-3D, push). Réseau sandbox : GitHub + PyPI seulement (pas de téléchargement des sorties ElevenLabs/Metricool).

## 3. Produire une vidéo
1. Script `<fmt>_script.py` (say = prononcé, nombres en lettres, sigles épelés ; show = affiché) → Kokoro (`*_tts.py`) pour les durées guides.
2. `python3 pipe/el_sync.py plan <fmt>` → `<dir>/el_text.txt` ; ElevenLabs `creative_create_flow` + `creative_generate_speech` (generations_count 1) ; lire `duration_secs` ; `python3 pipe/el_sync.py apply <fmt> <durée>`.
3. Rendu (`*_render.py`) puis audio (`*_audio.py`, sinus uniquement), planche de contrôle.
4. `bash pipe/eleven_prep.sh <dir> <nom>` → `<nom>_bed.mp4` (musique+bruitages+filigrane) ; push sur la branche `minuteaero-media`.
5. `creative_attach_reference_file` (raw GitHub du bed) sur le même flow → nœud `composition` (connect_from [bed, nœud voix]) → estimate_only → run → `master_url` (valide 2 h).
Moteurs : quiz*, vf2/vf3 (vrai/faux), tournoi/tn, mc (et si), top, duel_*, px_* (prix), ea/bio (biographie), tech.
Modèles 3D : `r3d/*.png` + dépôts FGMEMBERS (render_fg.py / render3d.py / render_glb.py).

## 4. Programmer (Metricool)
- TikTok d'abord avec `master_url` → la réponse donne une URL `static.metricool.com` → la réutiliser pour YouTube (`youtubeData` : title finissant par #shorts, type short, public, tags, category EDUCATION, madeForKids false, isAiGeneratedContent false) et Facebook (`facebookData` : type REEL, title).
- `updateScheduledPost` exige le contenu complet (l'id change, l'uuid reste).
- Metricool ne peut pas supprimer une vidéo publiée : en cas de correction, republier et demander à Olivier de supprimer l'ancienne.

## 5. Journal
Mettre à jour `history.json` (sujet, format, voix, uuids, flow) et pousser `minuteaero-pipeline`. Compte rendu court à Olivier (SendUserMessage) : vidéos programmées, enseignement des stats, problèmes, crédits ElevenLabs dépensés.

## 1quater. Innovation (demande d'Olivier le 08/10)
- « Innove, teste des choses, reste pas tunnel sur un truc. » → au moins 1 format nouveau/expérimental par semaine, mesuré à 48 h.
- Pistes : facteurs humains / cerveau du pilote (effet tunnel, hypoxie, désorientation spatiale, voile noir, fatigue, biais de confirmation), toujours lié à un vrai cas aviation sourcé.
- Moteur PIXEL ART : `pa_render.py` (rendu 180x320 agrandi x6 sans lissage, polices pipe/fonts Silkscreen/PressStart2P, tramage, vignette « tunnel », mascotte pixelisée). Scènes codées par type dans le fichier (ajouter un `sc_<type>` par nouveau sujet). Chaîne : cfg dans dl/<slug>, `DL=… dl_tts.py`, `el_sync.py plan pa:<slug>`, voix EL, `apply pa:<slug> <durée>`, `pa_render.py`, `dl_audio.py`, `eleven_prep.sh`.
- Ne pas utiliser le caractère % avec Silkscreen (glyphe illisible).
- Format « ESCALADE » sans voix (bs_render.py / bs_audio.py) : 1 → 5 → 20 → 100 → 1 000, dégâts cumulés, panneau DÉGÂTS, cartes « Le savais-tu ? », chute réelle (fait sourcé). 0 crédit ElevenLabs : mix local + URL raw GitHub dans Metricool. Idées suivantes : grêle vs avion, foudre (1 → 100 éclairs), G (1 G → 12 G sur un pilote), altitude (cabine dépressurisée), glace sur l'aile.
