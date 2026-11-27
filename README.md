# Interface Pari Demo — projet indépendant

Déploiement Render avec Flask. Ce dépôt ne dépend pas de Golsinyali AI.

## Déployer
1. Crée un nouveau dépôt Git et ajoute tous les fichiers de ce dossier.
2. Sur Render : **New + > Blueprint**, puis connecte le dépôt.
3. Render détecte `render.yaml`.
4. Dans les variables d'environnement, renseigne `SPORTS_API_KEY` avec ta clé.
5. Déploie et ouvre l'URL Render.

## Routes
- `/` : page de diagnostic
- `/health` : état du service
- `/api/team-search?q=Arsenal` : proxy vers `/api/search?q=Arsenal`
- `/api/schedule/2026-11-27` : proxy vers `/api/schedule/2026-11-27`

## Sécurité
Ne mets jamais la clé dans `index.html`, Git ou une capture d'écran. Configure-la uniquement dans les variables d'environnement Render.

Le schéma des réponses JSON n'est pas présumé. Le premier test permettra de découvrir les noms exacts des champs et des logos.
