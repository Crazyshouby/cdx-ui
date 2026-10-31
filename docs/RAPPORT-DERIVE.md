# Rapport de dérive à la charte CDX-UI

Version de la charte : **1.0.0** · généré le 2026-10-31 par `node tools/drift-report.mjs`.
Les comptes sont des **déclarations** (lignes de CSS / HTML / JS), pas des éléments affichés. Une copie identique à `dist/` n'est pas recomptée (elle se contrôle à la source) ; une exception propre à une application est déclarée, avec sa raison, dans `tools/apps/<application>.allow` et comptée à part (« tolérés »).
Les règles sont celles de `CHARTE.md` §8 ; la charte elle-même passe le même contrôle avec 18 exceptions justifiées dans `charte-lint.allow`.

## Vue d'ensemble

| Application | fichiers | radius | weight | size | blur | gradient | gray-tint | color | **total** | tolérés |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| AudioLinker | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 |
| cdx-frames | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 |
| cdx-windows (shell, Explorateur, Navigateur) | 41 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 44 |
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

C++ (Win32) + WebView2. Les pages sont assemblées par cmake/InlineAssets.cmake (marqueurs /*@cdx-ui.css@*/, /*@themes.css@*/, /*@fonts.css@*/ dans common.css, remplacés par les copies de cdx/) puis embarquées en RCDATA. cdx/ est une copie exacte de la charte et du client du bus (charte-sync), contrôlée en CI par tools/cdx-verify.mjs. icons.js reste le jeu de pictogrammes propre à AudioLinker (tools/pixel_icons.py dessine, tools/pixel_engine.py est le moteur commun).

**0 écart(s)** (+ 0 toléré(s) avec raison) dans 8 fichier(s) examiné(s), 12 copie(s) identique(s) de la charte non recomptée(s).

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
| `cdx/cdx-ui.css` | `cdx-ui.css` | identique | 27970 / 27970 |
| `cdx/themes.css` | `themes.css` | identique | 2572 / 2572 |
| `cdx/fonts.css` | `fonts.css` | identique | 15338 / 15338 |
| `cdx/cdx_bus.h` | `cdx_bus.h` | identique | 6589 / 6589 |
| `tools/cdx-verify.mjs` | `cdx-verify.mjs` | identique | 1868 / 1868 |
| `tools/pixel_engine.py` | `pixel_engine.py` | identique | 3394 / 3394 |
| `cdx/cdx-bridge.js` | `cdx-bridge.js` | identique | 4431 / 4431 |
| `cdx/cdx-frame.js` | `cdx-frame.js` | identique | 11827 / 11827 |
| `cdx/cdx-frame.css` | `cdx-frame.css` | identique | 2123 / 2123 |
| `cdx/tokens.json` | `tokens.json` | identique | 4695 / 4695 |
| `tools/charte-lint.mjs` | `charte-lint.mjs` | identique | 2815 / 2815 |
| `tools/lib/lint.mjs` | `lint.mjs` | identique | 6715 / 6715 |

## cdx-frames

Rust, pas de page web : la palette et les mesures du cadre sont des constantes Rust (paint.rs), à rapprocher de tokens.json (generated/tokens.rs).

**Constantes de `paint.rs` contre `tokens.json`**

| constante Rust | jeton | identique | remarque |
|---|---|---|---|
| `RING = 6` | `frame_ring + frame_outline = 6` | oui | anneau de cadre : 5 px + 1 px de contour noir (CHARTE.md §4) |
| `TITLE = 21` | `title_height = 21` | oui | barre de titre |
| `BUTTON = 14` | `title_button_size = 14` | oui | boutons de titre |

Couleurs écrites dans `paint.rs` : `#333333`, `#cc0000`, `#880000`, `#440000`, `#320000`, `#c30000`, `#555555`, `#222222`, `#111111`, `#0c0c0c`, `#8f8f8f`, `#444444`, `#8a8a8a`.
Toutes sont des jetons de la charte.

## cdx-windows (shell, Explorateur, Navigateur)

C# + WebView2, trois programmes (cdx-shell, cdx-explorer, cdx-browser) autour de la bibliothèque Cdx.Host. Les pages sont servies depuis web/ par l'hôte virtuel cdx.shell ; web/cdx/ est une copie exacte de la charte (charte-sync). Les pages _test-*.html sont ignorées.

**0 écart(s)** (+ 44 toléré(s) avec raison) dans 41 fichier(s) examiné(s), 13 copie(s) identique(s) de la charte non recomptée(s).

| fichier | radius | weight | size | blur | gradient | gray-tint | color |
|---|---:|---:|---:|---:|---:|---:|---:|

**Ce que l'application emploie réellement**

- tailles de police : `28px` ×1, `14px` ×1, `11px` ×1 (la charte : une seule, 14 px)
- arrondis : — (la charte : aucun)
- graisses : `400` ×2, `inherit` ×2, `100` ×2 (la charte : aucune)
- couleurs hors jetons : **15** valeurs distinctes, dont `#2e3436` ×1, `#4e9a06` ×1, `#c4a000` ×1, `#3465a4` ×1, `#75507b` ×1, `#06989a` ×1

<details><summary><code>weight</code> : undefined (exemples)</summary>

- `web/terminal/terminal.css:4` — `@font-face { font-family: 'KIRC Pixel Mono'; font-style: normal; font-weight: 100 900; src: url(/terminal/fonts/kirc-pixel-mono.ttf) format(`
- `web/terminal/terminal.css:5` — `@font-face { font-family: 'KIRC Pixel Mono'; font-style: italic; font-weight: 100 900; src: url(/terminal/fonts/kirc-pixel-mono-italic.ttf) `
- `web/terminal/vendor/addon-webgl.js:1` — `!function(e,t){"object"==typeof exports&&"object"==typeof module?module.exports=t():"function"==typeof define&&define.amd?define([],t):"obje`

</details>

<details><summary><code>size</code> : undefined (exemples)</summary>

- `web/terminal/terminal.js:32` — `fontFamily: FONT, fontSize: 14, lineHeight: 1,                // lineHeight 1 : la case fait la hauteur de la police (14 px), les caractères`
- `web/terminal/vendor/addon-webgl.js:1` — `!function(e,t){"object"==typeof exports&&"object"==typeof module?module.exports=t():"function"==typeof define&&define.amd?define([],t):"obje`
- `web/terminal/vendor/addon-webgl.js:1` — `!function(e,t){"object"==typeof exports&&"object"==typeof module?module.exports=t():"function"==typeof define&&define.amd?define([],t):"obje`

</details>

<details><summary><code>blur</code> : undefined (exemples)</summary>

- `web/terminal/vendor/xterm.css:266` — `box-shadow: var(--vscode-scrollbar-shadow, #000) 0 6px 6px -6px inset;`
- `web/terminal/vendor/xterm.css:274` — `box-shadow: var(--vscode-scrollbar-shadow, #000) 6px 0 6px -6px inset;`
- `web/terminal/vendor/xterm.css:284` — `box-shadow: var(--vscode-scrollbar-shadow, #000) 6px 0 6px -6px inset;`

</details>

<details><summary><code>gray-tint</code> : undefined (exemples)</summary>

- `web/terminal/vendor/xterm.js:1` — `!function(e,t){if("object"==typeof exports&&"object"==typeof module)module.exports=t();else if("function"==typeof define&&define.amd)define(`
- `web/terminal/vendor/xterm.js:1` — `!function(e,t){if("object"==typeof exports&&"object"==typeof module)module.exports=t();else if("function"==typeof define&&define.amd)define(`
- `web/terminal/vendor/xterm.js:1` — `!function(e,t){if("object"==typeof exports&&"object"==typeof module)module.exports=t();else if("function"==typeof define&&define.amd)define(`

</details>

<details><summary><code>color</code> : undefined (exemples)</summary>

- `web/terminal/vendor/xterm.js:1` — `!function(e,t){if("object"==typeof exports&&"object"==typeof module)module.exports=t();else if("function"==typeof define&&define.amd)define(`
- `web/terminal/vendor/xterm.js:1` — `!function(e,t){if("object"==typeof exports&&"object"==typeof module)module.exports=t();else if("function"==typeof define&&define.amd)define(`
- `web/terminal/vendor/xterm.js:1` — `!function(e,t){if("object"==typeof exports&&"object"==typeof module)module.exports=t();else if("function"==typeof define&&define.amd)define(`

</details>

**Copies de la charte** (comparées à `dist/`)

| copie dans l'application | source (dist/) | état | octets (app / dist) |
|---|---|---|---|
| `web/cdx/cdx-ui.css` | `cdx-ui.css` | identique | 27970 / 27970 |
| `web/cdx/themes.css` | `themes.css` | identique | 2572 / 2572 |
| `web/cdx/fonts.css` | `fonts.css` | identique | 15338 / 15338 |
| `web/cdx/icons.js` | `icons.js` | identique | 48984 / 48984 |
| `tools/cdx-verify.mjs` | `cdx-verify.mjs` | identique | 1868 / 1868 |
| `web/cdx/cdx-bridge.js` | `cdx-bridge.js` | identique | 4431 / 4431 |
| `web/cdx/cdx-frame.js` | `cdx-frame.js` | identique | 11827 / 11827 |
| `web/cdx/cdx-frame.css` | `cdx-frame.css` | identique | 2123 / 2123 |
| `web/cdx/tokens.json` | `tokens.json` | identique | 4695 / 4695 |
| `tools/charte-lint.mjs` | `charte-lint.mjs` | identique | 2815 / 2815 |
| `tools/lib/lint.mjs` | `lint.mjs` | identique | 6715 / 6715 |
| `web/cdx/cdx-columns.js` | `cdx-columns.js` | identique | 3984 / 3984 |
| `web/cdx/cdx-split.js` | `cdx-split.js` | identique | 4949 / 4949 |

## KIRC

Tauri (Rust). Les pages sont chargées depuis ui/ (frontendDist) ; ui/cdx/ est une copie exacte de la charte (charte-sync), contrôlée en CI par tools/cdx-verify.mjs. kirc.css ne garde que la mise en page de KIRC.

**0 écart(s)** (+ 24 toléré(s) avec raison) dans 3 fichier(s) examiné(s), 14 copie(s) identique(s) de la charte non recomptée(s).

| fichier | radius | weight | size | blur | gradient | gray-tint | color |
|---|---:|---:|---:|---:|---:|---:|---:|

**Ce que l'application emploie réellement**

- tailles de police : `14px` ×10, `28px` ×2, `42px` ×1 (la charte : une seule, 14 px)
- arrondis : — (la charte : aucun)
- graisses : — (la charte : aucune)
- couleurs hors jetons : **21** valeurs distinctes, dont `#ff8a3c` ×2, `#f58a1a` ×1, `#8a3a00` ×1, `#ff3030` ×1, `#2a5ae0` ×1, `#4a6aff` ×1

<details><summary><code>gradient</code> : undefined (exemples)</summary>

- `ui/kirc.css:57` — `background: radial-gradient(ellipse 70% 90% at 50% 130%, #f58a1a 0, #8a3a00 38%, transparent 72%), linear-gradient(#050505, #2c2c2c);`
- `ui/kirc.css:61` — `color: transparent; background: linear-gradient(#fff 0, #b9b9b9 45%, #444 55%, #9a9a9a); -webkit-background-clip: text; background-clip: tex`

</details>

<details><summary><code>color</code> : undefined (exemples)</summary>

- `ui/kirc.css:57` — `background: radial-gradient(ellipse 70% 90% at 50% 130%, #f58a1a 0, #8a3a00 38%, transparent 72%), linear-gradient(#050505, #2c2c2c);`
- `ui/kirc.css:57` — `background: radial-gradient(ellipse 70% 90% at 50% 130%, #f58a1a 0, #8a3a00 38%, transparent 72%), linear-gradient(#050505, #2c2c2c);`
- `ui/kirc.css:154` — `.mem.r0 { border-left-color: #ff5cf0; } .mem.r1 { border-left-color: #ff8a3c; } .mem.r2 { border-left-color: #ff3030; }`

</details>

**Copies de la charte** (comparées à `dist/`)

| copie dans l'application | source (dist/) | état | octets (app / dist) |
|---|---|---|---|
| `ui/cdx/cdx-ui.css` | `cdx-ui.css` | identique | 27970 / 27970 |
| `ui/cdx/themes.css` | `themes.css` | identique | 2572 / 2572 |
| `ui/cdx/fonts.css` | `fonts.css` | identique | 15338 / 15338 |
| `ui/cdx/icons.js` | `icons.js` | identique | 48984 / 48984 |
| `src-tauri/src/cdx_bus.rs` | `cdx_bus.rs` | identique | 11367 / 11367 |
| `tools/cdx-verify.mjs` | `cdx-verify.mjs` | identique | 1868 / 1868 |
| `ui/cdx/cdx-bridge.js` | `cdx-bridge.js` | identique | 4431 / 4431 |
| `ui/cdx/cdx-frame.js` | `cdx-frame.js` | identique | 11827 / 11827 |
| `ui/cdx/cdx-frame.css` | `cdx-frame.css` | identique | 2123 / 2123 |
| `ui/cdx/tokens.json` | `tokens.json` | identique | 4695 / 4695 |
| `tools/charte-lint.mjs` | `charte-lint.mjs` | identique | 2815 / 2815 |
| `tools/lib/lint.mjs` | `lint.mjs` | identique | 6715 / 6715 |
| `ui/cdx/cdx-columns.js` | `cdx-columns.js` | identique | 3984 / 3984 |
| `ui/cdx/cdx-split.js` | `cdx-split.js` | identique | 4949 / 4949 |

## Lecture

- Les applications C# (shell, Explorateur, Navigateur) lisent la charte sans copie : leur dérive se mesure par ce rapport, pas par synchronisation.
- Rien n'est corrigé ici : la phase 3 du plan traite KIRC, `cdx-frames` puis AudioLinker, une branche et une version mineure chacune, après validation de ce rapport.
