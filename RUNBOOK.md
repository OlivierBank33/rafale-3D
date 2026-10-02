# minuteaero — Runbook de production (version du 02/10/2026 au soir — fait foi)

Compte : **@minuteaero** sur TikTok + YouTube Shorts (UCQMD5dRsF3wBsJLOSSkWIKw) + Page Facebook (Reels, 1384175288106569), via Metricool (blogId `7174127`, fuseau `Europe/Paris`, essai Starter jusqu'au ~02/11).
Propriétaire : Olivier (veut rester anonyme : jamais son nom/visage/voix réelle). Langue : **français**. Olivier délègue TOUTES les décisions éditoriales : choisir ce qui a le plus de potentiel, tester, trancher sur les chiffres.

## 0. Règles non négociables
- **3 vidéos par jour** à **10 h 00, 12 h 30, 18 h 00** (pics d'audience Metricool). 1 post par réseau (TikTok, YouTube, Facebook) à la même heure.
- Durée **65–110 s**. Faits vérifiés par recherche web ; préciser à l'écran ce que représente un chiffre (prix catalogue, record, coût programme…).
- `tiktokData.isAigc = false`, `youtubeData.isAiGeneratedContent = false` (demande explicite d'Olivier). `tiktokData.title` obligatoire.
- **Zéro bruit blanc** dans la musique/bruitages : sinus uniquement (`noise_check.py` bloque sinon). Bed à −30 LUFS, filigrane auto (eleven_prep.sh).
- Voix : **ElevenLabs TTS direct uniquement** (eleven_multilingual_v2, 1 génération). Jamais de voice-changer. Lancer UNIQUEMENT le nœud composition (estimate_only d'abord = 0 crédit) — relancer le nœud voix facture deux fois.
- Jamais de rendu cassé : planche de contrôle avant publication. Jamais deux fois le même sujet (`history.json`).

## 1. Stratégie éditoriale (décidée le 02/10 sur les stats)
Stats semaine 1 (TikTok, 36,9 k abonnés) : vrai/faux 1 968 et 1 240 vues, quiz niveau pilote 1 069, tournoi 731, top vitesse 313, partages ≈ 0.
- **Cœur (2 vidéos/jour)** : formats « je joue » = vrai ou faux, quiz (silhouette, devine le prix, devine l'année), duels A vs B (rounds + score + verdict). Ce sont ceux qui font commenter.
- **Pari viral (1 vidéo/jour)** : classements visuels à comparaison d'échelle (prix avec piles de billets `px_*`, taille, vitesse, altitude), « et si… ? », crashs qui ont changé l'aviation (sobre, sans voyeurisme).
- **Bio / technique** : max 2 par semaine, seulement si les stats les justifient.
- Accroche : chiffre ou question choc dans les 2 premières secondes, texte à l'écran dès la 1re image.
- Chaque dimanche : relever vues, temps moyen, partages, abonnés gagnés par vidéo (Metricool `getAnalyticsDataByMetrics` TKPO07/08/10/13/15) → ajuster la répartition (doubler le gagnant, couper ce qui fait < 50 % de la médiane deux semaines de suite).
- **Décision au 01/11** : médiane ≥ 3 000 vues/vidéo ou une vidéo ≥ 100 k → on garde Metricool Starter et le rythme ; médiane < 1 500 → 1 vidéo/jour et proposer à Olivier de couper les abonnements.
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
