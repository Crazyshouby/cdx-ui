# Rapport de dérive à la charte KDX-UI

Version de la charte : **1.0.0** · généré le 2026-10-30 par `node tools/drift-report.mjs`.
Les comptes sont des **déclarations** (lignes de CSS / HTML / JS), pas des éléments affichés. Une copie identique à `dist/` n'est pas recomptée (elle se contrôle à la source) ; une exception propre à une application est déclarée, avec sa raison, dans `tools/apps/<application>.allow` et comptée à part (« tolérés »).
Les règles sont celles de `CHARTE.md` §8 ; la charte elle-même passe le même contrôle avec 18 exceptions justifiées dans `charte-lint.allow`.

## Vue d'ensemble

| Application | fichiers | radius | weight | size | blur | gradient | gray-tint | color | **total** | tolérés |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| AudioLinker | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 |
| kdx-frames | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 |
| kdx-windows (shell, Explorateur, Navigateur) | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 |
| KIRC | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 24 |

| règle | ce qu'elle mesure |
|---|---|
| `radius` | border-radius différent de 0 (aucun arrondi) |
| `weight` | graisse de police (pas de gras) |
| `size` | taille de texte hors multiples de 14 px |
| `blur` | ombre ou flou doux (ombres dures seulement) |
| `gradient` | dégradé doux hors jeton |
| `gray-tint` | gris teinté (les gris sont neutres) |
| `color` | couleur hors jetons |

## AudioLinker

C++ (Win32) + WebView2. Les pages sont assemblées par cmake/InlineAssets.cmake (marqueurs /*@kdx-ui.css@*/, /*@themes.css@*/, /*@fonts.css@*/ dans common.css, remplacés par les copies de kdx/) puis embarquées en RCDATA. kdx/ est une copie exacte de la charte et du client du bus (charte-sync), contrôlée en CI par tools/kdx-verify.mjs. icons.js reste le jeu de pictogrammes propre à AudioLinker.

**0 écart(s)** (+ 0 toléré(s) avec raison) dans 4 fichier(s) examiné(s), 8 copie(s) identique(s) de la charte non recomptée(s).

| fichier | radius | weight | size | blur | gradient | gray-tint | color |
|---|---:|---:|---:|---:|---:|---:|---:|

**Ce que l'application emploie réellement**

- tailles de police : `14px` ×2 (la charte : une seule, 14 px)
- arrondis : — (la charte : aucun)
- graisses : — (la charte : aucune)
- couleurs hors jetons : **0** valeurs distinctes, dont —

**Copies de la charte** (comparées à `dist/`)

| copie dans l'application | source (dist/) | état | octets (app / dist) |
|---|---|---|---|
| `kdx/kdx-ui.css` | `kdx-ui.css` | identique | 26370 / 26370 |
| `kdx/themes.css` | `themes.css` | identique | 2572 / 2572 |
| `kdx/fonts.css` | `fonts.css` | identique | 15338 / 15338 |
| `kdx/kdx_bus.h` | `kdx_bus.h` | identique | 6589 / 6589 |
| `tools/kdx-verify.mjs` | `kdx-verify.mjs` | identique | 1868 / 1868 |
| `kdx/kdx-bridge.js` | `kdx-bridge.js` | identique | 4431 / 4431 |
| `kdx/kdx-frame.js` | `kdx-frame.js` | identique | 8615 / 8615 |
| `kdx/kdx-frame.css` | `kdx-frame.css` | identique | 2123 / 2123 |

## kdx-frames

Rust, pas de page web : la palette et les mesures du cadre sont des constantes Rust (paint.rs), à rapprocher de tokens.json (generated/tokens.rs).

**Constantes de `paint.rs` contre `tokens.json`**

| constante Rust | jeton | identique | remarque |
|---|---|---|---|
| `RING = 6` | `frame_ring + frame_outline = 6` | oui | anneau de cadre : 5 px + 1 px de contour noir (CHARTE.md §4) |
| `TITLE = 21` | `title_height = 21` | oui | barre de titre |
| `BUTTON = 14` | `title_button_size = 14` | oui | boutons de titre |

Couleurs écrites dans `paint.rs` : `#333333`, `#cc0000`, `#880000`, `#440000`, `#320000`, `#c30000`, `#555555`, `#222222`, `#111111`, `#0c0c0c`, `#8f8f8f`, `#444444`, `#8a8a8a`.
Toutes sont des jetons de la charte.

## kdx-windows (shell, Explorateur, Navigateur)

C# + WebView2, trois programmes (kdx-shell, kdx-explorer, kdx-browser) autour de la bibliothèque Kdx.Host. Les pages sont servies depuis web/ par l'hôte virtuel kdx.shell ; web/kdx/ est une copie exacte de la charte (charte-sync). Les pages _test-*.html sont ignorées.

**0 écart(s)** (+ 0 toléré(s) avec raison) dans 11 fichier(s) examiné(s), 8 copie(s) identique(s) de la charte non recomptée(s).

| fichier | radius | weight | size | blur | gradient | gray-tint | color |
|---|---:|---:|---:|---:|---:|---:|---:|

**Ce que l'application emploie réellement**

- tailles de police : — (la charte : une seule, 14 px)
- arrondis : — (la charte : aucun)
- graisses : `400` ×2 (la charte : aucune)
- couleurs hors jetons : **0** valeurs distinctes, dont —

**Copies de la charte** (comparées à `dist/`)

| copie dans l'application | source (dist/) | état | octets (app / dist) |
|---|---|---|---|
| `web/kdx/kdx-ui.css` | `kdx-ui.css` | identique | 26370 / 26370 |
| `web/kdx/themes.css` | `themes.css` | identique | 2572 / 2572 |
| `web/kdx/fonts.css` | `fonts.css` | identique | 15338 / 15338 |
| `web/kdx/icons.js` | `icons.js` | identique | 48984 / 48984 |
| `tools/kdx-verify.mjs` | `kdx-verify.mjs` | identique | 1868 / 1868 |
| `web/kdx/kdx-bridge.js` | `kdx-bridge.js` | identique | 4431 / 4431 |
| `web/kdx/kdx-frame.js` | `kdx-frame.js` | identique | 8615 / 8615 |
| `web/kdx/kdx-frame.css` | `kdx-frame.css` | identique | 2123 / 2123 |

## KIRC

Tauri (Rust). Les pages sont chargées depuis ui/ (frontendDist) ; ui/kdx/ est une copie exacte de la charte (charte-sync), contrôlée en CI par tools/kdx-verify.mjs. kirc.css ne garde que la mise en page de KIRC.

**0 écart(s)** (+ 24 toléré(s) avec raison) dans 3 fichier(s) examiné(s), 9 copie(s) identique(s) de la charte non recomptée(s).

| fichier | radius | weight | size | blur | gradient | gray-tint | color |
|---|---:|---:|---:|---:|---:|---:|---:|

**Ce que l'application emploie réellement**

- tailles de police : `14px` ×10, `28px` ×2, `42px` ×1 (la charte : une seule, 14 px)
- arrondis : — (la charte : aucun)
- graisses : — (la charte : aucune)
- couleurs hors jetons : **21** valeurs distinctes, dont `#ff8a3c` ×2, `#f58a1a` ×1, `#8a3a00` ×1, `#ff3030` ×1, `#2a5ae0` ×1, `#4a6aff` ×1

<details><summary><code>gradient</code> : undefined (exemples)</summary>

- `ui/kirc.css:61` — `background: radial-gradient(ellipse 70% 90% at 50% 130%, #f58a1a 0, #8a3a00 38%, transparent 72%), linear-gradient(#050505, #2c2c2c);`
- `ui/kirc.css:65` — `color: transparent; background: linear-gradient(#fff 0, #b9b9b9 45%, #444 55%, #9a9a9a); -webkit-background-clip: text; background-clip: tex`

</details>

<details><summary><code>color</code> : undefined (exemples)</summary>

- `ui/kirc.css:61` — `background: radial-gradient(ellipse 70% 90% at 50% 130%, #f58a1a 0, #8a3a00 38%, transparent 72%), linear-gradient(#050505, #2c2c2c);`
- `ui/kirc.css:61` — `background: radial-gradient(ellipse 70% 90% at 50% 130%, #f58a1a 0, #8a3a00 38%, transparent 72%), linear-gradient(#050505, #2c2c2c);`
- `ui/kirc.css:158` — `.mem.r0 { border-left-color: #ff5cf0; } .mem.r1 { border-left-color: #ff8a3c; } .mem.r2 { border-left-color: #ff3030; }`

</details>

**Copies de la charte** (comparées à `dist/`)

| copie dans l'application | source (dist/) | état | octets (app / dist) |
|---|---|---|---|
| `ui/kdx/kdx-ui.css` | `kdx-ui.css` | identique | 26370 / 26370 |
| `ui/kdx/themes.css` | `themes.css` | identique | 2572 / 2572 |
| `ui/kdx/fonts.css` | `fonts.css` | identique | 15338 / 15338 |
| `ui/kdx/icons.js` | `icons.js` | identique | 48984 / 48984 |
| `src-tauri/src/kdx_bus.rs` | `kdx_bus.rs` | identique | 11367 / 11367 |
| `tools/kdx-verify.mjs` | `kdx-verify.mjs` | identique | 1868 / 1868 |
| `ui/kdx/kdx-bridge.js` | `kdx-bridge.js` | identique | 4431 / 4431 |
| `ui/kdx/kdx-frame.js` | `kdx-frame.js` | identique | 8615 / 8615 |
| `ui/kdx/kdx-frame.css` | `kdx-frame.css` | identique | 2123 / 2123 |

## Lecture

- Les applications C# (shell, Explorateur, Navigateur) lisent la charte sans copie : leur dérive se mesure par ce rapport, pas par synchronisation.
- Rien n'est corrigé ici : la phase 3 du plan traite KIRC, `kdx-frames` puis AudioLinker, une branche et une version mineure chacune, après validation de ce rapport.
