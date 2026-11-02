# Compatibilité : version de la charte et version des applications

La charte suit [SemVer](https://semver.org/lang/fr/) (`VERSION`, `dist/MANIFEST.json`) :

- **majeure** : un jeton, une classe ou un message du pont est retiré ou change de sens (une application doit être adaptée) ;
- **mineure** : un jeton, un composant, un accent ou un message est ajouté ;
- **correctif** : une valeur corrigée, sans changement de nom.

Chaque application copie `dist/` par `charte-sync` et garde la version dans son `cdx-sync.json` (champ `cdxUi`).

| cdx-ui | cdx-windows | cdx-messages (ex-KIRC) | AudioLinker | Notes |
|---|---|---|---|---|
| 2.2.0 | copie à jour, pas de release | copie à jour, pas de release | copie à jour, pas de release | **mineure** : vingt pictogrammes pour les applications tierces de la zone de notification (discord, steam, nvidia, amd, localsend, tailscale, obs, whatsapp, vlc, epic, battlenet, temperature, telephone, camera, adobe, medal, distant, ia, tennis, appli), rendus en un ton par la barre CDX ; 02/11/2026 |
| 2.1.0 | copie à jour, pas de release | 0.5.0 (renommage, pas encore publiée) | copie à jour, pas de release | **mineure** : les polices s'appellent « CDX Pixel », « CDX Pixel Log », « CDX Pixel Log Italic » et « CDX Pixel Mono » (ex-« KIRC Pixel… ») ; l'application `kirc` du bus s'appelle `messages` ; le pictogramme `kirc` s'appelle `messages` ; cdx-frames sort de la charte ; 02/11/2026 |
| 1.0.0 | 0.1.0 (installeur, pas de release) | 0.4.0 (tag `v0.4.0`, 31/10/2026) | 1.3.0 (tag `v1.3.0`, 31/10/2026) | première charte partagée ; clients du bus et accent de la suite compris ; suite renommée CDX le 31/10/2026 |
| 2.0.2 | copie à jour, pas de release | copie à jour, pas de release | copie à jour, pas de release | **correctif** : `snap_gap` passe de 2 à 0 px, l'aimantation colle les fenêtres bord à bord (demande de Valentin) ; 01/11/2026 |
| 2.0.1 | copie à jour, pas de release | copie à jour, pas de release | copie à jour, pas de release | **correctif** : le texte des boutons, onglets, menus, lignes de liste, sélecteurs et lignes d'état est centré au pixel (il était 1 à 2 px trop haut, 1 px trop à gauche dans les boutons) ; aucune hauteur ne change ; 01/11/2026 |
| 2.0.0 | copie à jour, pas de release | copie à jour, pas de release | copie à jour, pas de release | les seize thèmes de KDX ; **majeure** : les jetons `--tb-edge`/`--tb-low`/`--tb-grad`/`--tbb-*` ne sont plus écrits par `body.active` (lire `--t-*`), `kAccents`/`ACCENTS` deviennent `Theme` (plus de champs), les noms `bleu` `vert` `violet` `charbon` sont des alias ; 31/10/2026 |

Avant toute publication d'une application : son `cdx-sync.json` doit porter la version de charte de cette ligne, `node tools/cdx-verify.mjs` doit être vert, et `node tools/drift-report.mjs` (dans cdx-ui) ne doit montrer aucun écart non justifié.
Publier AudioLinker ou Messages avec la charte exige en plus la décision sur le nom « CDX » et sur la police (`CHARTE.md` §10).
