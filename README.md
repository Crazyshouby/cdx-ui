# kdx-ui : la charte graphique KDX, source unique

L'apparence KDX (Haxial) de KIRC, extraite pour toutes les applications de la suite : fenêtres sans cadre système, relief gris éclairé en haut à gauche, polices bitmap,
icônes pixel, une couleur d'accent par thème. Ce dépôt est la **source** ; KIRC, AudioLinker, `kdx-frames` et les applications Windows en consomment une copie
vérifiée par empreinte (`dist/`). Les règles sont dans `CHARTE.md`, le plan d'ensemble dans le plan de la suite (phases 0 à 6).

| Fichier | Rôle |
|---|---|
| `CHARTE.md` | la charte : principes, couleurs, typographie, mesures, composants, interdits, intégration, licences |
| `exemple.html` | guide de style vivant : tous les composants, sélecteur de thème |
| `tokens.json` | **source unique** des couleurs, des accents et des mesures |
| `kdx-ui.css` | composants et jetons (le bloc entre `tokens:begin` et `tokens:end` est généré) |
| `themes.css` | une rampe d'accent par thème (généré) ; le rouge est le défaut du `:root` |
| `kdx-frame.css`, `kdx-frame.js` | le cadre de fenêtre (barre de titre, poignées, enroulement), dialogue et menu contextuel |
| `kdx-bridge.js` | le pont vers l'hôte natif : un contrat de fenêtre, trois transports (Tauri, chaînes AudioLinker, WebView2 JSON) |
| `fonts.css`, `icons.js`, `polices/` | polices pixel (base64) et 40 icônes 16 × 16 ; le rouge des icônes suit l'accent |
| `generated/kdx-tokens.h`, `generated/tokens.rs` | les jetons pour C++ (AudioLinker) et Rust (`kdx-frames`, KIRC) |
| `dist/` | ce que les applications embarquent + `MANIFEST.json` (version, empreintes) |
| `tools/kdx-verify.mjs`, `tools/check-accents.mjs` | le contrôle des copies (copié dans chaque application, à mettre dans sa CI : `kdx-sync.json` donne l'empreinte de chaque copie) et celui de la liste des accents écrite à la main dans plusieurs programmes |
| `docs/ARCHITECTURE.md`, `docs/COMPAT.md` | le plan des quatre dépôts et leurs règles ; la version de la charte face à celle des applications |
| `docs/SUITE.md` | les réglages communs (`suite.json`) et le bus de messages entre applications, avec les messages de chacune |
| `bus/cpp/kdx_bus.h`, `bus/rust/kdx_bus.rs` | les clients C++ et Rust (le client C# est dans kdx-windows) ; chacun a ses tests de protocole |
| `docs/CONTRAT-FENETRE.md` | le contrat de fenêtre et sa correspondance avec les trois hôtes |
| `docs/RAPPORT-DERIVE.md` | état chiffré des écarts des quatre applications (`node tools/drift-report.mjs`) |
| `tools/`, `tests/`, `charte-lint.allow` | contrôle de charte, synchronisation, rapport, tests, exceptions justifiées |
| `gen/` | générateurs : polices (`gen_font.py`, `gen_font_gdi.py`), icônes (`pixel_icons.py`), assets (`gen_assets.py`), jetons (`gen_tokens.py`) |

## Utiliser

```html
<link rel="stylesheet" href="fonts.css"><link rel="stylesheet" href="kdx-ui.css"><link rel="stylesheet" href="themes.css"><link rel="stylesheet" href="kdx-frame.css">
<script src="icons.js"></script><script src="kdx-bridge.js"></script><script src="kdx-frame.js"></script>
<body class="active"><div class="win"><div class="tb">…boutons data-act="close|min|max|shade"…<span class="tb-title">Titre</span></div><div class="cb">…</div></div>
<script>KdxFrame.init().edges();</script>
```

## Commandes (Node ≥ 22, Python avec `fonttools` et `brotli`)

```
npm run verifier        # tout : jetons à jour, dist à jour, charte-lint propre, tests Node, tests de page (Chrome headless)
python gen/gen_tokens.py [--check]     # après une modification de tokens.json
node tools/build-dist.mjs [--check]       # après toute modification d'un fichier distribué
node tools/charte-lint.mjs <dossier>      # contrôle les règles de CHARTE.md §8 (--allow pour des exceptions justifiées)
node tools/charte-sync.mjs --check <app>  # compare les copies d'une application à dist/ (profils : tools/apps/*.json)
node tools/drift-report.mjs               # régénère docs/RAPPORT-DERIVE.md
python gen/gen_tokens.py --new-theme cuivre 25 0.9 1.0 "#ffcc99" "#3a1800" "#ffe090"   # ajoute un accent
```

## État (phase 0, 30/10/2026)

Fait et vérifié : jetons uniques (équivalence prouvée avec les valeurs d'origine : aucune n'a changé), module Rust compilé, contrat de fenêtre testé sur les trois transports
simulés, 14 tests Node, 35 vérifications de page, charte-lint propre sur la charte (18 exceptions justifiées), rapport de dérive recoupé avec les comptes faits à la main.

**Non vérifié** : `kdx-tokens.h` n'a pas été compilé (pas de compilateur C++ sur ce poste : à faire avec Visual Studio dans AudioLinker) ; le workflow `.github/workflows/check.yml`
n'a jamais tourné ; `kdx-frame.js` / `kdx-bridge.js` n'ont été essayés qu'avec des hôtes simulés, aucune application ne les utilise encore (phases 1 et 3) ; `win.shade` et `win.ready`
ne sont pas implémentés côté C#. Aucune application n'a été modifiée.
