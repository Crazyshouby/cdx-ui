# Charte graphique CDX-UI

L'interface de Messages (anciennement KIRC), mise au point pour être indiscernable de celle de KDX (Haxial Software), consignée ici pour
servir à d'autres projets. Tout ce qui suit est mesuré au pixel sur KDX 1.6 : les **seize apparences** de KDX sont les seize
thèmes de la charte (`kdx-reference/`, mesures brutes ; `tokens.json`, palette de chaque thème). Les valeurs « finales » sont
dans `cdx-ui.css` et `themes.css`, la page `exemple.html` montre chaque élément dans chaque thème, et `tools/kdx-compare.py`
mesure la charte contre KDX, point par point.

## 1. L'esprit

Des **fenêtres sans bordure système** posées sur un fond, chacune une fonction : cadre en relief, barre de titre,
panneau gris. Un monde **plat et gris**, éclairé **du haut gauche** : tout ce qui se manipule est en relief, tout ce
qui se lit ou se saisit est creusé. L'écran est lu comme un instrument : des **pixels nets** (police bitmap, aucun
lissage), **aucun arrondi**, une **seule couleur d'accent** qui dit quelle fenêtre est active.

Les cinq règles qui font que cela « ressemble à CDX » :

1. **Relief éclairé en haut à gauche.** Clair en haut et à gauche, sombre en bas et à droite, pour les boutons,
   cadres, barres de titre. Inverser l'éclairage (creux) pour les champs et listes.
2. **Les couleurs sont celles du thème.** Un composant n'écrit jamais une couleur : il lit les jetons (panneau, bouton,
   texte, champ, colonnes de liste, cadre actif, cadre inactif…). Seize palettes, mesurées sur les seize apparences de KDX,
   sombres ou claires, grises ou teintées. Le thème par défaut, *Clair-obscur rouge* (Evil Chiaroscuro), est fait de gris
   neutres (`#222`, `#333`, `#444`, `#555`, `#666`, `#888`), de champs noirs et de texte blanc.
3. **Aucun arrondi.** Les coins sont droits, ou chanfreinés de quelques pixels (deux pour les boutons de dialogue).
4. **Une couleur par rôle.** Le cadre actif (rouge par défaut) marque la fenêtre qui a le focus ; la mise en évidence
   (`--hl`) remplit un bouton enclenché ; l'anneau du bouton par défaut a ses couleurs (`--def-*`), qui ne sont pas toujours
   celles du cadre (dans KDX, Bubblegum Crisis a un titre violet et un anneau vert). Le vert, l'ambre et le rouge de statut
   ne signifient *que* ok, attention et problème, et ne changent pas avec le thème.
5. **Une taille, une graisse.** Tout le texte fait 14 px de police bitmap, interligne 16 px (13 px en console).
   Pas de gras. La hiérarchie se fait par la couleur, la position et le relief.

## 2. Couleurs

### Les jetons d'un thème

Chaque thème porte une palette complète, dans `tokens.json` (voir `THEME_GROUPS` dans `gen/gen_tokens.py`). Les valeurs
ci-dessous sont celles du thème par défaut, *Clair-obscur rouge* ; `themes.css` les remplace toutes pour les autres thèmes.

| Groupe | Jetons | Rouge | Rôle |
|---|---|---|---|
| Surfaces | `--panel` | `#333333` | panneaux (fond des fenêtres) |
| | `--btn`, `--btn-hover`, `--card-2` | `#333333`, `#3c3c3c`, `#2a2a2a` | boutons : face, survol, enfoncé (et menus déroulants) |
| | `--frame` | `#222222` | fond derrière les fenêtres |
| | `--ink`, `--field-ink`, `--own-ink` | `#000000`, `#00ff00`, `#ffffff` | champs et consoles : fond, texte, ses propres lignes |
| | `--col-a`, `--col-b`, `--list-text` | `#333333`, `#444444`, `#ffffff` | listes : colonnes impaires, paires, texte (KDX raye les listes par colonne) |
| | `--head`, `--head-text` | `#333333`, `#ffffff` | en-têtes de colonne |
| | `--sb-track`, `--sb-thumb`, `--sb-arrow` | `#2a2a2a`, `#333333`, `#888888` | barres de défilement : piste, pouce, flèches |
| | `--hl`, `--hl-text` | `#880000`, `#ffffff` | bouton enclenché (`.on`), badge « non lu » |
| Texte | `--text`, `--faint` | `#ffffff`, `#888888` | texte des panneaux, texte secondaire ou désactivé |
| | `--btn-text` | `#ffffff` | texte des boutons (noir sur les boutons gris clair de Lagon, blanc sur les boutons bleus de Rêve bleu) |
| | `--title-text`, `--tb-text` | `#ffffff`, `#ffffff` | texte de la barre de titre active, inactive |
| Contours | `--outline`, `--outline-active` | `#000000`, `#000000` | contour des fenêtres (inactive, active : bleu dans Techno électrique, blanc dans Lagon) |
| | `--btn-outline`, `--field-outline` | `#000000`, `#000000` | contour des boutons, des champs |
| | `--line` | `#555555` | filets entre les lignes d'une liste |
| Relief | `--hi`, `--hi2`, `--lo`, `--lo2` | `#666666`, `#444444`, `#111111`, `#222222` | arêtes d'un bouton : claires (extérieure, intérieure), sombres (idem) |
| | `--field-lo`, `--field-hi` | `#111111`, `#666666` | arêtes d'un champ creusé : sombre en haut à gauche, claire en bas à droite |
| | `--row-hover`, `--row-sel`, `--row-sel-ring` | `#3c3c3c`, `#404040`, `#757575` | ligne de liste survolée, sélectionnée, son filet |
| Cadre inactif | `--tb-edge`, `--tb-mid`, `--tb-low` | `#555555`, `#222222`, `#111111` | anneau de la fenêtre inactive, fond de ses boutons de titre |
| | `--tb-from`, `--tb-grad-mid`, `--tb-to` | `#0c0c0c`, `#222222`, `#8f8f8f` | dégradé du titre inactif (début, 9ᵉ ligne, fin) |
| Cadre actif | `--a-edge`, `--a-mid`, `--a-dark`, `--a-hover` | `#cc0000`, `#880000`, `#440000`, `#660000` | anneau de la fenêtre active, fond de ses boutons de titre, survol |
| | `--a-title-from`, `--a-title-mid`, `--a-title-to` | `#320000`, `#880000`, `#c30000` | dégradé du titre actif (début, 9ᵉ ligne, fin : le dégradé de KDX a un coude) |
| | `--bar-top`, `--bar-mid`, `--bar-bot`, `--a-spark`, `--accent` | `#e83c3c`, `#c01010`, `#8a0202`, `#ff8a74`, `#d41818` | barre de jauge, étincelle, accent d'application |
| | `--ic-accent`, `--ic-accent-dark` | `#e02020`, `#8a0202` | le rouge des icônes pixel suit le thème |
| | `--def-outline`, `--def-edge`, `--def-mid` | `#000000`, `#cc0000`, `#880000` | anneau du bouton par défaut (contour, bord, milieu) |
| Sélection | `--sel-bg`, `--sel-fg` | `#001177`, `#ff00ff` | sélection « marquée » (texte sélectionné, ligne mise en évidence d'une console) |
| | `--scheme` | `dark` | `color-scheme` des contrôles natifs (`light` pour les thèmes clairs) |

Les images qui ne peuvent pas lire un jeton (flèche des listes déroulantes, flèches de défilement) sont générées par thème
(`--sel-arrow`, `--sb-up`, `--sb-down`, `--sb-left`, `--sb-right`). Les noms de cdx-ui 1.x restent définis : `--muted`,
`--accent-2`, `--red-frame`, `--tb-grad`, `--tbb-fill`, `--tbb-hi`, `--tbb-lo`.

### Les seize thèmes

Les apparences de KDX 1.6, dans l'ordre de sa liste « Appearance ». Mesurées sur des captures (`gen/kdx_reference.py` →
`kdx-reference/kdx.json`), puis écrites dans `tokens.json` par `gen/kdx_tokens.py` ; ce qui n'est pas mesurable sur les
captures (le texte des champs, qui sont vides ; la sélection marquée) y est **choisi**, et dit tel.

| `data-theme` | Nom | Apparence KDX | Panneau | Texte | Champ | Titre actif | |
|---|---|---|---|---|---|---|---|
| `rouge` | Clair-obscur rouge | Evil Chiaroscuro | `#333333` | `#ffffff` | `#000000` | `#320000` → `#c30000` | sombre |
| `marine` | Marine et rose | Alternate Romp | `#233765` | `#ccdcff` | `#0f2351` | `#280a11` → `#b58b95` | sombre |
| `ambre` | Ambre CRT | Amber CRT | `#0a0a0a` | `#b53500` | `#448043` | `#431300` → `#da9900` | sombre |
| `jean` | Bleu jean | Blue Jeans | `#00002a` | `#ffffff` | `#000015` | `#001042` → `#0094d8` | sombre |
| `tramway` | Tramway | Blue Tram Café | `#1a0073` | `#00dc97` | `#000000` | `#5f2600` → `#ffb200` | sombre |
| `sarcelle` | Sarcelle | Bubblegum Crisis | `#193333` | `#ffffff` | `#000000` | `#290031` → `#b600c1` | sombre |
| `chocolat` | Chocolat framboise | Chocolate Raspberry | `#2c1200` | `#b39d7a` | `#0f0600` | `#20000e` → `#a97e92` | sombre |
| `lavande` | Lavande | Mach Lavender | `#dddddd` | `#000000` | `#ffffff` | `#666666` → `#e9e9e9` | clair |
| `oxygene` | Oxygène | Oxygen | `#9b999b` | `#ffffff` | `#666666` | `#252c37` → `#b0bbca` | clair |
| `couchant` | Clair-obscur couchant | Sunset Chiaroscuro | `#333333` | `#ffffff` | `#000000` | `#4d1700` → `#e79e00` | sombre |
| `techno` | Techno électrique | Techno Electric | `#424242` | `#efefef` | `#d3e7ff` | `#9c9c9c` → `#101010` | sombre |
| `reve-bleu` | Rêve bleu | The Dream Scheme (Blue) | `#969696` | `#000000` | `#224d8d` | `#0c1c34` → `#8fa5c5` | clair |
| `reve-vert` | Rêve vert | The Dream Scheme (Green) | `#969696` | `#000000` | `#125f68` | `#062326` → `#87aeb3` | clair |
| `reve-violet` | Rêve violet | The Dream Scheme (Purple) | `#969696` | `#000000` | `#323264` | `#121225` → `#9797b0` | clair |
| `lagon` | Lagon | Tropical Water | `#c8c8c8` | `#000000` | `#ffffff` | `#002c5f` → `#00bbff` | clair |
| `turquoise` | Turquoise | Turquoise Hilites | `#dddddd` | `#000000` | `#ffffff` | `#13265f` → `#97b1ff` | clair |

Anciens noms (cdx-ui 1.x), encore acceptés par `themes.css` et par les programmes : `bleu` → `jean`, `vert` → `reve-vert`, `violet` → `reve-violet`, `charbon` → `techno`, `cdx` → `rouge`.

### Statut (ne jamais détourner)

| Jeton | Valeur | Sens |
|---|---|---|
| `--green` | `#00ff00` | ok, connecté, fait |
| `--warn` | `#faa320` | attention, occupé, non lu |
| `--red` | `#ff5a4a` | problème, erreur |

Les **lignes de liste** ne se colorent pas : sélection = un peu plus clair que la liste, cernée d'un filet (`--row-sel`,
`--row-sel-ring`) ; survol = `--row-hover`.

## 3. Typographie

| Police | Usage | Taille / interligne | Particularités |
|---|---|---|---|
| **CDX Pixel** (`--font`) | toute l'interface | 14 px / 16 px | majuscules de 9 px, hauteur d'x de 7 px, espace entre lettres de 2 px |
| **CDX Pixel Log** (`--font-log`) | console, saisie sous la console | 14 px / 13 px | majuscules de 8 px, espace de 1 px, mots séparés de 7 px |
| **CDX Pixel Log Italic** (`--font-log-italic`) | actions, présence | 14 px / 13 px | version inclinée par lignes ; l'italique est une police à part |

Règles :

- **Rester à 14 px** (ou un multiple, si une version agrandie est un jour nécessaire) : un pixel de la police est
  un pixel CSS. Toute autre taille floute.
- **Pas de gras.** Une police bitmap n'a qu'une graisse ; l'épaissir d'un pixel fait se toucher les hampes de 2 px.
  Les boutons gardent `font-weight: 700` dans le CSS : sans effet visible sur la police, mais utile en repli
  (Segoe UI) si elle ne se charge pas.
- **Pas de lissage ClearType.** Dans Chromium / WebView2, lancer avec `--disable-lcd-text` (Tauri :
  `additional_browser_args`). Les polices du kit sont des **polices en couches (COLR v0)** : seul moyen trouvé pour
  obtenir des pixels purs sous WebView2, car DirectWrite floute en demi-pixel horizontal les glyphes ordinaires
  (ni le CSS ni une option ne l'empêchent). Conséquence : leur couleur vient de la couleur du texte CSS, mais elles ne
  se rendent pas dans un outil qui ne gère pas COLR.
- **Libellés de formulaire** terminés par « : » (`.form label[for]::after`).
- **Jeu de caractères** : latin complet avec accents, ponctuation française (« », …, —), flèches et quelques symboles.
  Régénérer avec `gen/gen_font.py` pour ajouter un glyphe.
- Repli : `"Segoe UI Symbol", "Segoe UI", sans-serif`.

## 4. Mesures

| Élément | Valeur |
|---|---|
| Barre de titre | 21 px : filet clair 1, dégradé 18, filet sombre 1 ; contour noir sous elle |
| Boutons de barre de titre | 14 × 14 px, glyphe 8 × 8, trait de 2 px blanc |
| Cadre de fenêtre | 5 px : quatre lignes concentriques + contour noir |
| Marge panneau → contenu | 5 px (8 px dans les dialogues de réglages, 12 px dans les dialogues simples) |
| Espacement entre éléments | 4–6 px (formulaires : 6 px de rang, 10 px de colonne) |
| Bouton de dialogue | hauteur 20 px, marge intérieure 14 px ; bouton par défaut : anneau de 3 px (milieu, bord, contour) aux coins chanfreinés |
| Bouton de barre / menu déroulant | hauteur 22 px, filet noir partagé (−1 px de marge) |
| En-tête de colonne | hauteur 22 px |
| Champ de texte | marge intérieure 3 × 6 px ; ligne de saisie de salon : 56 px de haut |
| Case à cocher | 14 × 14 px |
| Barre de défilement | 15 px ; à chaque bout une **paire** de flèches (haut et bas, ou gauche et droite), boutons de 13 px |
| Poignée de redimensionnement | triangle de 12 px dans le coin bas droit |
| Icône | 16 × 16 px (14 px dans une barre de titre) |
| Aimantation des fenêtres | 10 px d'attraction, 2 px d'écart (bord de l'écran : 0) |

## 5. Le relief

Trois recettes à `box-shadow`, toutes dans `:root`, composées des jetons de relief du thème (mesurés sur ses boutons) :

- **Relief** `--bevel` — bouton, onglet, en-tête, poignée de curseur :
  `inset 1px 1px var(--hi), inset 2px 2px var(--hi2), inset -1px -1px var(--lo), inset -2px -2px var(--lo2)`, contour `--btn-outline`.
  La case à cocher a un relief d'un seul pixel (`--hi`, `--lo`).
- **Enfoncé** `--bevel-down` — bouton pressé, onglet actif : le relief inversé et plus sombre.
- **Creux** `--sunken-border` (`--field-lo` en haut et à gauche, `--field-hi` en bas et à droite) + `--sunken-shadow`
  (le contour `--field-outline`, à l'intérieur, tout autour) — champ, liste, console, afficheur.
- **Cadre de fenêtre** `--ring` (`--tb-edge`, `--tb-mid`, `--tb-low`, contour `--outline`) et `--ring-focus` (`--a-edge`,
  `--a-mid`, `--a-dark`, contour `--outline-active`) — quatre lignes, la plus claire à l'extérieur en haut et à gauche, à
  l'intérieur en bas et à droite. Le cadre continue sous la barre de titre (ses quatre premiers pixels de chaque côté).

## 6. Composants

| Composant | Classe | Règle |
|---|---|---|
| Fenêtre | `.win` > `.tb` + `.cb` | `.win.active` (ou `body.active`) pour la fenêtre qui a le focus ; `.shaded` pour l'enrouler |
| Barre de titre | `.tb` | titre centré, sans ombre ; inactive = dégradé `--tb-*`, active = dégradé `--a-title-*` ; les jetons `--t-*` disent lequel |
| Boutons de titre | `.tb-btn` + `.tb-l` (fermer) `.tb-r` (enrouler) `.tb-r2` (agrandir) `.tb-m` (menu, hachuré) | |
| Bouton | `.btn` | relief, coins chanfreinés de 2 px, texte `--btn-text` ; désactivé `--faint` ; **enclenché** `.on` : rempli de `--hl`, texte `--hl-text` (le « Chat List » de KDX) |
| Bouton par défaut | `.primary` | un seul par dialogue ; anneau `--def-mid` / `--def-edge` / `--def-outline`, chanfreiné |
| Pile de boutons | `.stack > .sbtn` | colonne de boutons carrés partageant un filet ; une icône 16 px à gauche |
| Champ | `.text-input` | creux, fond `--ink`, texte `--field-ink` ; focus : anneau d'accent d'1 px |
| Menu déroulant | `select.btn` | bouton avec case de flèche séparée par un filet noir |
| Case à cocher | `.switch > input + .track` | plot en relief ; cochée : coche blanche seule |
| Curseur | `input[type=range]` | rigole noire, barre d'accent, poignée en relief |
| Groupe | `fieldset.grp > legend` | cadre gravé ; titre sur l'arête |
| Liste | `.list > .row-item` | lignes à filet ; barre d'état à gauche (6 px) ; **colonnes rayées** `--col-a` / `--col-b` sur toute la hauteur (`cdx-columns.js` pose `--cdx-stripes`) ; la liste qui a le focus porte l'anneau d'accent |
| En-tête de colonne | `.lhead > .lh` | bouton carré qui trie (`--head`, `--head-text`) ; `.on` = triangle |
| Onglets | `.tabs > .tab` | boutons carrés ; actif : enfoncé, texte blanc ; autres : `#888` |
| Afficheur | `.status` | bande noire creusée, texte vert, voyant (`.orb`) à gauche |
| Bandeau d'alerte | `.banner` | noir, cadre d'accent, texte ambre |
| Notification | `.toast` (`.ok`) | boîte noire, cadre rouge (problème) ou vert (fait), ombre portée dure |
| Menu contextuel | `.menu` | mini-cadre ; titre au dégradé de la barre de titre |
| Console | `.log > .ln.<genre>` | voir ci-dessous |
| Voyant | `.orb` (`.green`, `.amber`, `.red`) | 11 px, sphère dégradée ; `pulse` quand occupé |

### Genres de lignes d'une console

Nom de l'auteur dans sa couleur, texte en `--field-ink` ; **ses propres lignes** en `--own-ink` (blanc sur une console sombre) ; **action** rose en italique ;
**présence** (arrivée, départ) vert sombre en italique ; **sujet et modes** bleu ; **annonce** ambre ; **serveur**
gris ; **mise en évidence** fond bleu marine, filet rose ; **erreur et expulsion** rouge. Aucun gras.

### États d'un contrôle

| État | Rendu |
|---|---|
| Normal | relief, texte `--btn-text` |
| Survol | fond `--btn-hover` (listes : `--row-hover`) |
| Pressé | enfoncé : `--bevel-down`, fond `--card-2` |
| Enclenché (`.on`) | fond `--hl`, texte `--hl-text`, relief |
| Désactivé | texte `--faint`, curseur par défaut, pas de survol |
| Focus clavier | contour orange `--warn` de 2 px (champs et listes : anneau d'accent d'1 px à la place) |
| Sélectionné | liste : `--row-sel` + filet `--row-sel-ring` ; onglet : enfoncé |

## 7. Icônes

16 × 16 px, dessinées pixel par pixel, **contour noir d'1 px**, couleurs plates (palette de 20 valeurs dans
`gen/pixel_icons.py`), jamais lissées ni redimensionnées autrement qu'en multiples entiers. Exportées en SVG, une
`<path>` par couleur (`icons.js` : `pix("nom", taille)` renvoie le balisage, `fillPix()` remplit les
`[data-ic]`). Pour une nouvelle icône : ajouter son dessin dans `pixel_icons.py` et relancer la génération.

## 8. À ne pas faire

- Pas de `border-radius`, pas de dégradé « doux », pas d'ombre floue (les ombres sont dures : `4px 5px 0 rgba(0,0,0,.5)`).
- Pas de couleur de statut pour décorer ; pas de bleu « lien » hors des liens de console (`#5cf0ff`).
- Pas de `font-weight` pour hiérarchiser ; pas de taille autre que 14 px ; pas de `text-rendering` ou lissage.
- Pas de couleur écrite dans un composant, un gris neutre non plus : les thèmes sont clairs ou sombres, gris ou teintés ; on lit un jeton. Seules les couleurs de statut sont fixes.
- Pas de sélection colorée dans une liste ; pas de survol qui change la couleur du texte.
- Pas de bordure système : la fenêtre se dessine elle-même (voir section 9).
- Pas de plusieurs « boutons par défaut » dans un même dialogue.

## 9. Intégration dans un nouveau projet

1. Copier `cdx-ui.css`, `fonts.css`, `themes.css` et `icons.js` (ou tout le dossier `charte/`).
2. Dans la page : `<link>` vers `fonts.css`, `cdx-ui.css`, puis `themes.css` ; `<html data-theme="…">` pour le thème (un des seize de `tokens.json` ; rien ou `rouge` pour le défaut).
3. Structurer chaque fenêtre en `.win > .tb + .cb` (voir `exemple.html`). Mettre `body.active` (fenêtre unique) ou
   `.win.active` (plusieurs) selon le focus ; un écouteur `focus`/`blur` suffit sur le web.
4. **Application de bureau (Tauri 2 / WebView2)** : fenêtres sans décoration (`decorations(false)`), glisser par
   la barre de titre (commande native, pas `data-tauri-drag-region`, pour pouvoir aimanter), `additional_browser_args`
   avec `--disable-lcd-text`. Messages (`src-tauri/src/app.rs`) montre l'aimantation, l'enroulement, l'agrandissement et
   les onglets par fusion de fenêtres.
5. Les mises en page propres à l'application (colonnes, volets) vont dans le CSS du projet, pas dans `cdx-ui.css` :
   ce fichier ne contient que des composants.
6. Une liste à colonnes passe par `CdxColumns.init` : il pose les largeurs et les rayures par colonne.
7. Vérifier : aucune ligne de la page n'a `border-radius`, `font-weight` utile, ni couleur hors des jetons (`tools/charte-lint.mjs`).
   Comparer à `exemple.html` côte à côte, dans un thème clair aussi (Lavande, Lagon).

Régénérer les ressources : voir `README.md` (polices, icônes, thèmes).

## 10. Réserves de licence

- **Les formes des lettres de CDX Pixel et CDX Pixel Log reproduisent celles des polices de KDX** (relevées sur
  des captures de KDX 1.6) ; les glyphes manquants ont été dessinés pour Messages (alors KIRC). Elles restent l'œuvre de Haxial :
  avant de publier un projet qui les embarque, décider si on les garde ou si l'on redessine une police propre
  (`gen/gen_font.py` en est l'unique source).
- Les icônes (`pixel_icons.py`), les couleurs et les mesures sont dessinées ou relevées pour Messages.
- KDX est une marque de Haxial ; aucun lien avec Haxial. Un projet qui adopte cette charte doit le préciser s'il
  parle de CDX.

## 11. Jetons, cadre, pont et contrôle (cdx-ui 2.0)

- **Jetons** : `tokens.json` est la source des couleurs (la palette complète de chacun des seize thèmes), des alias et des mesures. `python gen/gen_tokens.py` en tire le bloc de
  jetons de `cdx-ui.css`, `themes.css`, `generated/cdx-tokens.h` (C++ : `cdx::kThemes`) et `generated/tokens.rs` (Rust : `THEMES`, `theme_id()`). On ne modifie jamais ces blocs à la main.
- **Référence KDX** : `python gen/kdx_reference.py <dossier des captures>` mesure les seize captures de KDX et écrit `kdx-reference/kdx.json` et les découpes de fenêtres ;
  `python gen/kdx_tokens.py` en déduit les thèmes de `tokens.json` (`--check` dans la CI). `python tools/kdx-compare.py` capture `tests/kdx-maquette.html` dans chaque thème
  et compare 46 points de couleur à KDX (`--keep` : planches côte à côte dans `build/kdx-compare/`). Un nouveau thème se mesure sur une capture, ou s'écrit en entier à la main.
- **Cadre de fenêtre** : `cdx-frame.js` (+ `cdx-frame.css`) branche la barre de titre, les poignées, l'enroulement, les boîtes de dialogue et les menus ; `cdx-bridge.js` traduit les demandes
  de fenêtre vers l'hôte (voir `docs/CONTRAT-FENETRE.md`). Une application n'écrit plus ce code.
- **Icônes** : le rouge des icônes pixel (`R`, `r` de `pixel_icons.py`) suit le thème par `--ic-accent` / `--ic-accent-dark` ; le rouge d'erreur (`E`, `e`) reste fixe, comme toute couleur de statut (§2).
- **Contrôle** : `node tools/charte-lint.mjs` applique le §8 (arrondis, gras, tailles hors multiples de 14, ombres floues, dégradés, gris teintés, couleurs hors jetons). Une exception se déclare
  dans `charte-lint.allow` **avec sa raison** ; sans raison, elle n'est pas acceptée.
- **Fenêtres imbriquées** : une fenêtre inactive posée dans une fenêtre active hérite des jetons de titre `--t-*` du cadre actif ; `cdx-frame.css` redonne ceux du cadre inactif à toute fenêtre non active.
- **Double appui** sur la barre de titre : `lastDown` démarre à `-Infinity` (un premier appui juste après le chargement ne compte pas comme double).
