# Architecture de la suite CDX

Trois dépôts voisins (dans `Dev\CDX\` ; Audio Linker, autrefois le dépôt AudioLinker, vit dans cdx-windows depuis le 03/11/2026), un seul sens de circulation : **cdx-ui produit, les autres copient**.

```
cdx-ui  ──dist/──►  cdx-windows   web/cdx/       (charte)        + cdx-sync.json
        │           cdx-messages  ui/cdx/        (charte)        + src-tauri/src/cdx_bus.rs
        └──────────► cdx-windows  src/cdx-audio_linker/cdx/   (Audio Linker : charte + cdx_bus.h)
```

| Dépôt | Contient | Langage | Se construit avec |
|---|---|---|---|
| **cdx-ui** | la charte (jetons, composants CSS, cadre de fenêtre, pont), les générateurs (polices, pictogrammes, jetons), les clients du bus C++ et Rust, les contrôles (lint, synchro, accents), la documentation | CSS, JS, Python, Node | `npm run verifier` |
| **cdx-windows** | cdx-shell (barre, Démarrer, centre rapide), cdx-explorer, cdx-browser, la bibliothèque commune Cdx.Host, le client du bus C#, couche1 (cadre DWM), les maquettes | C# .NET 8, HTML/CSS/JS (WebView2) | `build.ps1` |
| **cdx-messages** | Messages : la messagerie (IRC, WhatsApp ; Tauri) | Rust, HTML/CSS/JS | `npm run build`, `cargo test`, `node tests/e2e.mjs` |
| **Audio Linker** (`cdx-windows/src/cdx-audio_linker`, ex-dépôt AudioLinker) | le mixeur multi-sorties | C++ (Win32, WASAPI), HTML/CSS/JS (WebView2) | `build.cmd tests` (dans son dossier) |

## Règles

1. **Une seule source** pour chaque chose. La charte et les générateurs sont dans cdx-ui ; une application n'a jamais son propre générateur de la charte.
2. **Les copies ne se modifient pas à la main.** `node tools/charte-sync.mjs --write <application>` (dans cdx-ui) les remplace et écrit `cdx-sync.json` (l'empreinte de chaque copie) ; la CI de l'application lance `node tools/cdx-verify.mjs <cdx-sync.json>` et échoue si une copie a été retouchée.
3. **La dérive se mesure** : `node tools/drift-report.mjs` compte les écarts de chaque application à la charte ; une exception est justifiée par écrit dans `tools/apps/<application>.allow`.
4. **Les listes écrites à la main restent cohérentes** : `node tools/check-accents.mjs` vérifie que chaque programme connaît tous les accents de `tokens.json`.
5. **Les applications se parlent par le bus** (`docs/SUITE.md`) et partagent un fichier de réglages (`%APPDATA%\CDX\suite.json`). Aucun programme n'en démarre un autre autrement que par son exécutable déclaré dans `apps.json`.
6. **Un dossier de build par application** (`bin\`, `build-dev\`, `src-tauri\target\`), jamais commité.

## Où trouver quoi

| Je veux… | Fichier |
|---|---|
| changer une couleur ou une mesure | `cdx-ui/tokens.json`, puis `python gen/gen_tokens.py` (un thème mesuré sur KDX : `kdx-reference/kdx.json`, puis `python gen/kdx_tokens.py`) |
| ajouter un thème | une capture de KDX pour `gen/kdx_reference.py`, ou la palette complète à la main dans `tokens.json` ; puis les listes des programmes (`node tools/check-accents.mjs`) |
| changer un composant (bouton, liste…) | `cdx-ui/cdx-ui.css` (+ `exemple.html`), puis `node tools/build-dist.mjs` |
| propager la charte | `node tools/charte-sync.mjs --write messages` (et `audio_linker`, `cdx-windows`) |
| ajouter un message du bus | `cdx-ui/docs/SUITE.md`, puis le client concerné (`cdx-windows/src/Cdx.Host/Bus.cs`, `bus/cpp`, `bus/rust`) |
| ajouter une page à la barre ou au centre rapide | `cdx-windows/web/shell/` et `src/Cdx.Shell/` |
| modifier une fenêtre de l'Explorateur ou du navigateur | `cdx-windows/web/explorer|browser/` et `src/Cdx.Explorer|Browser/` |
| régénérer l'icône de Messages | `python gen/gen_messages_icon.py <cdx-messages>/src-tauri/icons/source.png` |

## Essais

| Où | Commande | Ce que ça couvre |
|---|---|---|
| cdx-ui | `npm run verifier` | jetons à jour, dist à jour, lint de la charte, accents, tests Node, tests de page, comparaison à KDX (`tools/kdx-compare.py`) |
| cdx-windows | `cdx-shell --selftest-bus`, `--selftest-audio`, `--selftest-sys` ; `cdx-explorer --selftest-fs`, `--selftest-web` ; `cdx-browser --selftest-browser` | le bus, la liaison Audio Linker, les fichiers, les pages, le navigateur |
| cdx-windows | `tests\bus.ps1`, `tests\suite.ps1`, `tests\navigateur.ps1` | de bout en bout, isolé (voir SUITE.md §3.6) |
| cdx-messages | `cargo test`, `node tests/e2e.mjs` | 141 tests unitaires, 101 vérifications de la vraie application |
| cdx-windows/src/cdx-audio_linker | `build.cmd tests`, `python tools/ui_smoke.py build-dev/gen/ui.gen.html` | 5 tests unitaires (dont la reprise des réglages d'AudioLinker), la page principale |
