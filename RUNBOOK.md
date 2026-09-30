# minuteaero — Runbook de la production quotidienne (3 vidéos / jour)

Compte TikTok : **@minuteaero** (Metricool, blogId `7174127`, fuseau `Europe/Paris`).
Propriétaire : Olivier. Langue : **français**. Objectif : croissance puis monétisation (Creator Rewards : vidéos ≥ 60 s, originales).

## 0. Principes non négociables
- **3 vidéos par jour**, créneaux **12 h 30, 19 h 00, 21 h 30** (heure de Paris). Ne remplir que les créneaux vides (vérifier `getScheduledPosts`).
- Durée **65–110 s** chacune (≥ 60 s obligatoire).
- **Faits vérifiés** : chaque chiffre/date/nom affiché ou prononcé doit être vérifié par recherche web si tu n'en es pas certain. En cas de doute, retire le fait. Jamais de statistique inventée.
- **Jamais deux fois le même sujet** : lire et mettre à jour `history.json`.
- `tiktokData.isAigc = true` (voix de synthèse) — obligatoire. `tiktokData.title` est obligatoire.
- Pas de marque déposée mise en avant, pas de personnes réelles identifiables, pas de politique, pas de contenu militaire sensible (seulement des infos publiques grand public).
- Qualité avant tout : **vérifier visuellement** chaque vidéo (planche de 6–8 images extraites) avant de programmer. Si c'est raté, corriger ou remplacer ; ne jamais publier un rendu cassé.

## 1. Installation (≈ 5 min)
```bash
cd /home/claude
git clone -q --depth 1 -b minuteaero-pipeline https://github.com/OlivierBank33/rafale-3d pipe
cp -r pipe/* /home/claude/
bash setup.sh
```
`setup.sh` installe bpy, kokoro-onnx, pycairo, scipy, soundfile, télécharge la voix (GitHub releases) et clone les modèles 3D FlightGear déjà utilisés dans `fg/`.
Si le dépôt n'est pas accessible, appelle `add_repo` (owner `OlivierBank33`, repo `rafale-3D`, access `push`) puis reclone.

## 2. Choisir les 3 sujets du jour
1. Lire `history.json` (sujets déjà faits + stats).
2. Analyser les performances : `getAnalyticsAvailableMetrics` puis `getAnalyticsDataByMetrics` sur TikTok (vues, taux de visionnage complet, partages, commentaires) pour les 14 derniers jours. Noter dans `history.json` les stats de chaque vidéo publiée.
3. Répartition : doubler le format qui marche le mieux ; garder au moins 2 formats différents par jour.
4. Formats disponibles (moteurs dans ce dépôt) :
   - **Quiz silhouette** (`quiz_script.py`, `quiz_tts.py`, `quiz_render.py`, `quiz_audio.py`) — 10 avions, 3 réponses, compte à rebours 3 s. Varier les thèmes : chasseurs, avions de ligne, avions historiques, avions français, « niveau expert »…
   - **Tournoi** (`tournoi_script.py`, `tn_tts.py`, `tournoi_render.py`, `tn_audio.py`) — 8 avions, critères chiffrés vérifiés, finale en 3 manches.
   - **« Et si… ? »** (`mc_script.py`, `mc_render.py`, `mc_audio.py`) — scénario catastrophe expliqué + cas réels. Idées : porte ouverte en vol, pilotes inconscients, foudre, dépressurisation, oiseau dans le moteur, atterrissage sans train, turbulences extrêmes.
   - **Vrai ou faux** — adapter le moteur quiz : 2 réponses (VRAI/FAUX), affirmation surprenante + image de l'avion concerné.
   - Tu peux créer de nouveaux formats si les stats montrent une lassitude.
5. Avions 3D disponibles : `r3d/*.png` (Concorde, Spitfire, B-2, Beluga, SR-71, F-22, A-10, Mirage 2000, F-117, An-225) et `mc/*.png` (A320, A330, 767). Pour d'autres avions : dépôts `https://github.com/FGMEMBERS/<Nom>` (ex. Eurofighter, F-15C, f16, F-35B, 787-8, 777, 707, 737-800, A400M, c130, Caravelle, MiG-21bis, Su-37, Harrier-GR1, B-52F, Alphajet, pc7, DR400, ASK21, An-124, 747-8i, A300-600ST, Extra-500). Rendu : `render3d.py` (un seul .ac) ou `render_fg.py` (assemblage via le XML FlightGear). Vérifier chaque rendu (vue d'ensemble), éviter les livrées de compagnies réelles si possible (textures neutres : `texmap`).

## 3. Produire chaque vidéo
- Écrire le script (say = prononcé avec noms anglais transcrits phonétiquement ; show = affiché). Vérifier la prononciation avec `k.tokenizer.phonemize(texte, 'fr-fr')` : aucun marqueur `(en)` ne doit rester.
- Voix : Kokoro `ff_siwis`, vitesse 1.15–1.26.
- Rendu vidéo 1080×1920, 30 i/s ; audio mixé à −14 LUFS (voir les scripts *_audio.py + commande ffmpeg dans l'historique des scripts).
- Nommer : `AAAA-MM-JJ_<creneau>_<format>_<slug>.mp4`, taille < 30 Mo (sinon ré-encoder crf 23–24).
- Contrôle : extraire 6–8 images (ffmpeg `-ss`) en planche, la regarder, corriger si texte coupé, image vide, chevauchement.

## 4. Héberger et programmer
```bash
cd /home/claude && rm -rf media_push && git clone -q --depth 1 -b minuteaero-media https://github.com/OlivierBank33/rafale-3d media_push
cp <videos>.mp4 media_push/ && cd media_push && git add *.mp4 && git -c user.name=Claude -c user.email=noreply@anthropic.com commit -qm "Médias du <date>" && git push -q origin minuteaero-media
```
URL publique : `https://raw.githubusercontent.com/OlivierBank33/rafale-3D/minuteaero-media/<fichier>.mp4` (vérifier avec `curl -r 0-100`).
Puis `createScheduledPost` (blogId `7174127`) :
- `providers: [{"network":"tiktok"}]`, `autoPublish: true`, `draft: false`
- `publicationDate: {dateTime, timezone:"Europe/Paris"}` + `date` ISO avec +02:00 (été) / +01:00 (hiver)
- `text` : accroche courte + appel au commentaire + 5–6 hashtags (#avion #aviation #avgeek #pilote #minuteaero + 1 spécifique)
- `tiktokData: {title, privacyOption:"PUBLIC_TO_EVERYONE", isAigc:true, autoAddMusic:false}`
Programmer pour **le lendemain** (ou le jour même si les créneaux sont encore à venir de > 1 h).
Ménage : supprimer du dépôt média les vidéos déjà publiées depuis > 3 jours (Metricool garde sa copie) pour garder le dépôt léger.

## 5. Journal
Mettre à jour `history.json` (sujet, format, fichier, date, créneau, id Metricool, stats quand dispo) et pousser sur la branche `minuteaero-pipeline` avec les scripts nouveaux ou modifiés. Terminer par un court compte rendu (SendUserMessage) : 3 vidéos programmées, créneaux, 1 enseignement tiré des stats.
