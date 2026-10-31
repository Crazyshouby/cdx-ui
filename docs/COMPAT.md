# Compatibilité : version de la charte et version des applications

La charte suit [SemVer](https://semver.org/lang/fr/) (`VERSION`, `dist/MANIFEST.json`) :

- **majeure** : un jeton, une classe ou un message du pont est retiré ou change de sens (une application doit être adaptée) ;
- **mineure** : un jeton, un composant, un accent ou un message est ajouté ;
- **correctif** : une valeur corrigée, sans changement de nom.

Chaque application copie `dist/` par `charte-sync` et garde la version dans son `cdx-sync.json` (champ `cdxUi`).

| cdx-ui | cdx-windows | KIRC | AudioLinker | Notes |
|---|---|---|---|---|
| 1.0.0 | 0.1.0 (installeur, pas de release) | 0.4.0 (tag `v0.4.0`, 31/10/2026) | 1.3.0 (tag `v1.3.0`, 31/10/2026) | première charte partagée ; clients du bus et accent de la suite compris ; suite renommée CDX le 31/10/2026 |
| 2.0.0 | copie à jour, pas de release | copie à jour, pas de release | copie à jour, pas de release | les seize thèmes de KDX ; **majeure** : les jetons `--tb-edge`/`--tb-low`/`--tb-grad`/`--tbb-*` ne sont plus écrits par `body.active` (lire `--t-*`), `kAccents`/`ACCENTS` deviennent `Theme` (plus de champs), les noms `bleu` `vert` `violet` `charbon` sont des alias ; 31/10/2026 |

Avant toute publication d'une application : son `cdx-sync.json` doit porter la version de charte de cette ligne, `node tools/cdx-verify.mjs` doit être vert, et `node tools/drift-report.mjs` (dans cdx-ui) ne doit montrer aucun écart non justifié.
Publier AudioLinker ou KIRC avec la charte exige en plus la décision sur le nom « CDX » et sur la police (`CHARTE.md` §10).
