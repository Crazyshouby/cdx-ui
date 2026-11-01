# Contrat de fenêtre CDX

Toutes les applications CDX ont des fenêtres **sans cadre système** dont le cadre (barre de titre, boutons, bords) est dessiné par la page. La page *demande*, l'hôte natif *exécute*.
Ce contrat est la liste unique de ces demandes ; `cdx-bridge.js` les traduit vers le transport de chaque hôte, `cdx-frame.js` les déclenche depuis le HTML de la charte.

## Page → hôte

| Demande (`cdx.win.*`) | Quand | KIRC (Tauri) | AudioLinker (chaînes) | Applications C# (JSON) |
|---|---|---|---|---|
| `ready()` | la page est chargée, la fenêtre peut s'afficher | `invoke("win_ready")` | — | `{cmd:"win.ready"}` |
| `drag("start")` | appui sur la barre de titre | `win_drag {phase:"start"}` | `dragstart` | `{cmd:"win.drag"}` (boucle de déplacement native) |
| `drag("move")` | mouvement du pointeur (au plus un par image) | `win_drag {phase:"move"}` | `dragmove` | inutile |
| `drag("end")` | relâchement | `win_drag {phase:"end"}` | `dragend` | inutile |
| `resize("start", edge)` | appui sur une poignée (`.grip-rz`, `.rz[data-e]`) | `win_drag {phase:"rstart"}` (coin seulement) | `resizewin` (coin seulement) | `{cmd:"win.resize", edge}` |
| `resize("move"/"end")` | suite du glissement | `rmove` / `end` | — | inutile |
| `shade()` | double appui < 400 ms (ou bouton) | `win_shade` | `shade` | `{cmd:"win.shade"}` *(à implémenter côté hôte)* |
| `max()` | double appui avec `data-dblclick="max"`, bouton agrandir | `win_zoom` | — | `{cmd:"win.max"}` |
| `min()` | bouton réduire | — | — | `{cmd:"win.min"}` |
| `close()` | bouton fermer | `win_close` | `closepanel` | `{cmd:"win.close"}` |
| `title(texte)` | le titre change | — | — | `{cmd:"win.title", t}` |

Codes de bord (`edge`, valeurs `HT*` de Windows) : 10 gauche · 11 droite · 12 haut · 13 haut-gauche · 14 haut-droite · 15 bas · 16 bas-gauche · 17 bas-droite.
Un « — » signifie : la demande est sans effet sur cet hôte (aujourd'hui), sans erreur.

## Hôte → page

| Événement (`cdx.on(type, fn)`) | Valeur | Effet par défaut de `CdxFrame.init()` |
|---|---|---|
| `active` | `true` si Windows a activé la fenêtre | classe `active` sur `<body>` (cadre et titre à l'accent) |
| `shade` | `true` si la fenêtre est enroulée | classe `shaded` sur `<body>` |
| `theme` | nom de l'accent (`rouge`, `bleu`…) | attribut `data-theme` de `<html>` (le rouge n'en porte pas) |

Transport des événements : Tauri `listen(type)` (charge utile = valeur) ; AudioLinker et applications C# : message `{ "type": "active", "value": true }` (objet ou texte JSON).

## Ce que chaque hôte doit fournir

- **Minimum** : `close`, `drag`, `active`. Un hôte qui ignore le reste reste conforme (les demandes inconnues sont sans effet).
- **Fenêtre redimensionnable** : `resize` ; l'hôte peut déléguer à Windows (`WM_NCLBUTTONDOWN` avec le code de bord, comme le fait l'hôte C#).
- **Aimantation** : à la charge de l'hôte (10 px d'attraction, 2 px d'écart, 0 au bord de l'écran : `tokens.json`, `snap_distance` et `snap_gap`).
- **Un thème** : l'hôte relit les réglages communs (`%APPDATA%\CDX\suite.json`, phase 2) et envoie `theme` ; en attendant, chaque application reste maîtresse du sien.

## Qui l'utilise (30/10/2026)

Un seul code de cadre, `cdx-frame.js` sur `cdx-bridge.js`, pour toutes les applications : KIRC (transport `tauri`, écoute limitée à la fenêtre courante),
AudioLinker (transport `strings`, `data-cdx-host="strings"` sur `<html>`), l'Explorateur et le navigateur de cdx-windows (transport `webview2`). Chaque application en
reçoit une copie par `charte-sync` ; la page ne garde que ses besoins propres (menu de fenêtre de KIRC par l'événement `cdx:menu`, messages d'état d'AudioLinker).
Les essais : `tests/bridge.test.html` (les trois transports simulés), `AudioLinker/tools/ui_smoke.py` (le transport `strings` sur la vraie page), `KIRC/tests/e2e.mjs`
(la vraie application), `cdx-windows/tests/cadre.ps1` (les vraies fenêtres de l'Explorateur et du navigateur).

## Écarts connus

- Les hôtes C# ignorent `win.shade` et `win.ready` (sans erreur) ; ils n'envoient pas `active`.
- KIRC n'a pas de commande `min` ni de `title` ; AudioLinker n'a pas d'agrandissement.
- L'aimantation existe dans KIRC (`app.rs::drag`, `SNAP_DIST`, `SNAP_GAP`) et, depuis le 01/11/2026, dans l'hôte C# de cdx-windows (`Cdx.Host/Snap.cs`, corrige le rectangle de `WM_MOVING` / `WM_SIZING`, voisines = toutes les fenêtres de la suite) ; pas dans AudioLinker.
- Les pages du shell (barre, Démarrer, centre rapide) n'ont pas de cadre à déplacer : elles n'utilisent que le pont (`cdx.on`) par `host.js`.
- KIRC prend le menu contextuel de CdxFrame (`CdxFrame.menu`) ; il n'a pas de dialogue modal. Le menu des périphériques d'AudioLinker (cases, listes déroulantes, pastilles de couleur) est plus riche que `CdxFrame.menu` : il reste le sien.
