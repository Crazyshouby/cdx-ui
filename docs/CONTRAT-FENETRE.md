# Contrat de fenêtre KDX

Toutes les applications KDX ont des fenêtres **sans cadre système** dont le cadre (barre de titre, boutons, bords) est dessiné par la page. La page *demande*, l'hôte natif *exécute*.
Ce contrat est la liste unique de ces demandes ; `kdx-bridge.js` les traduit vers le transport de chaque hôte, `kdx-frame.js` les déclenche depuis le HTML de la charte.

## Page → hôte

| Demande (`kdx.win.*`) | Quand | KIRC (Tauri) | AudioLinker (chaînes) | Applications C# (JSON) |
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

| Événement (`kdx.on(type, fn)`) | Valeur | Effet par défaut de `KdxFrame.init()` |
|---|---|---|
| `active` | `true` si Windows a activé la fenêtre | classe `active` sur `<body>` (cadre et titre à l'accent) |
| `shade` | `true` si la fenêtre est enroulée | classe `shaded` sur `<body>` |
| `theme` | nom de l'accent (`rouge`, `bleu`…) | attribut `data-theme` de `<html>` (le rouge n'en porte pas) |

Transport des événements : Tauri `listen(type)` (charge utile = valeur) ; AudioLinker et applications C# : message `{ "type": "active", "value": true }` (objet ou texte JSON).

## Ce que chaque hôte doit fournir

- **Minimum** : `close`, `drag`, `active`. Un hôte qui ignore le reste reste conforme (les demandes inconnues sont sans effet).
- **Fenêtre redimensionnable** : `resize` ; l'hôte peut déléguer à Windows (`WM_NCLBUTTONDOWN` avec le code de bord, comme le fait l'hôte C#).
- **Aimantation** : à la charge de l'hôte (10 px d'attraction, 2 px d'écart, 0 au bord de l'écran : `tokens.json`, `snap_distance` et `snap_gap`).
- **Un thème** : l'hôte relit les réglages communs (`%APPDATA%\KDX\suite.json`, phase 2) et envoie `theme` ; en attendant, chaque application reste maîtresse du sien.

## Écarts connus à résorber (phases 1 et 3)

- Les hôtes C# n'implémentent pas encore `win.shade` ni `win.ready` ; ils n'envoient pas `active`.
- KIRC n'a pas de commande `min` ni de `title` ; AudioLinker n'a pas d'agrandissement.
- L'aimantation n'existe que dans KIRC (`app.rs::drag`, `SNAP_DIST`, `SNAP_GAP`).
