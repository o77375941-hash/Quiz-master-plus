# Quiz Master Plus (Gradio) — Starter

## Objectif (MVP)
Construire une app Gradio "Quiz Master Plus" avec :
- Choix **Catégorie** (Culture / Maths / Python)
- Choix **Difficulté** (Facile / Moyen / Difficile)
- Boutons : Start / Valider / Skip / Restart
- Affichage : **Question X/Y** + **Score : s** (pendant le quiz)
- Fin : Score + Badge

## Lancer l'app
1) Installer les dépendances :
   - `pip install -r requirements.txt`
2) Lancer :
   - `python app.py`
3) Ouvrir le lien affiché dans le terminal (ex: http://127.0.0.1:7860)

## Fichiers
- `app.py` : interface Gradio
- `utils.py` : logique du quiz (state, questions, vérification, badge)

## Consigne importante
Ce starter contient une **structure** et des **TODO**.
Votre mission est d'implémenter la logique étape par étape (avec Copilot si vous voulez),
en comprenant ce que vous faites.
