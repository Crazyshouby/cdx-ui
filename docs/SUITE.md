# La suite CDX : réglages communs et bus de messages

Les applications de la suite (cdx-shell, cdx-explorer, cdx-browser, cdx-repos, Audio Linker, Messages) restent des programmes séparés. Elles partagent deux choses, volontairement
minimes : un **fichier de réglages** (l'accent) et un **bus de messages** (des tubes nommés). Aucun démon central : si une application ne tourne pas, les autres
continuent, et ce qui lui était destiné se perd sans bruit (ou la lance, voir §3.5).

## 1. Réglages communs : `%APPDATA%\CDX\suite.json`

```json
{ "version": 1, "accent": "jean" }
```

| Champ | Valeurs | Rôle |
|---|---|---|
| `version` | `1` | version du format ; un fichier d'une version inconnue est ignoré |
| `accent` | `rouge` `marine` `ambre` `jean` `tramway` `sarcelle` `chocolat` `lavande` `oxygene` `couchant` `techno` `reve-bleu` `reve-vert` `reve-violet` `lagon` `turquoise` | le thème de toute la suite (les seize apparences de KDX de `tokens.json` ; les anciens noms `bleu` `vert` `violet` `charbon` sont encore lus et ramenés au nom actuel) |

Règles :

- **Absent, illisible, accent inconnu** : l'accent précédent est gardé, ou `rouge` au premier lancement. Une application ne plante jamais pour un `suite.json` abîmé.
- **Écriture atomique** : écrire `suite.json.tmp` puis le renommer (`MoveFileEx` avec remplacement, `File.Move(…, true)`, `fs::rename`). Un lecteur ne voit jamais un fichier à moitié écrit.
- **Lecture à chaud** : chaque application relit le fichier à l'ouverture, puis surveille sa date de modification et sa taille (sondage toutes les 250 ms : plus simple et
  aussi fiable qu'une notification de dossier, pour un coût nul). Elle applique le nouvel accent sans redémarrer : la suite se recolore en moins d'une seconde.
- **Dérogation** : une application peut offrir un accent à elle. Messages garde son réglage « thème » ; il ne suit la suite que lorsqu'il est sur sa valeur par défaut (`cdx`).
- **Qui écrit** : `cdx-shell.exe --accent <nom>` (et, plus tard, un sélecteur dans le centre rapide). Une application n'écrit jamais autre chose que `accent`.
- Les réglages propres à chaque application restent chez elle (`%APPDATA%\CDX\Messages`, `%APPDATA%\cdx-audio_linker`, `%LOCALAPPDATA%\CdxShell`).

## 2. Le bus : un tube par application

Chaque application qui veut **recevoir** ouvre un tube `\\.\pipe\cdx.<nom>`, nom ∈ `shell`, `explorer`, `browser`, `repos`, `terminal`, `audio_linker`, `messages` (et `transfers`, `notes`, `agenda`, `mail`, `pilote`, `youtube`, décrits dans leurs applications ; `youtube` reçoit `show`, comme Dépôts).

- **Sécurité** : le tube n'est accessible qu'à l'utilisateur courant (descripteur de sécurité : un seul droit, celui du SID de l'utilisateur ; sous .NET `PipeOptions.CurrentUserOnly`),
  les connexions distantes sont refusées (`PIPE_REJECT_REMOTE_CLIENTS`), la première instance est créée avec `FILE_FLAG_FIRST_PIPE_INSTANCE` (un autre processus ne peut pas
  occuper le nom avant nous).
- **Format** : du JSON, un objet par ligne (`\n`), UTF-8, **64 Ko au plus par ligne** (au-delà, la connexion est coupée).

```json
{ "type": "open-url", "from": "messages", "data": { "url": "https://example.org/" } }
```

| Champ | Rôle |
|---|---|
| `type` | le nom du message, de la forme `domaine-action` ou `domaine.action` ; **liste blanche propre à chaque application** (§3) |
| `from` | le nom de l'émetteur (informatif : le tube n'est de toute façon ouvert qu'à l'utilisateur courant) |
| `data` | un objet, dont les champs sont définis par le type ; peut être omis |

- **Rien n'est évalué** : un message est une donnée, jamais du code ni une commande de shell. Chaque application **valide** `type` (liste blanche), puis chaque champ de `data`
  (type JSON, longueur, valeurs admises). Un message hors liste, mal formé ou invalide est **ignoré** et noté dans le journal ; il ne ferme pas la connexion.
- **Sans réponse par défaut** : l'émetteur ouvre le tube, écrit une ou plusieurs lignes, referme (« tire et oublie »). Si le tube n'existe pas, l'application n'est pas lancée.
- **Connexions longues** : une application peut garder la connexion ouverte pour **recevoir** des messages poussés (Audio Linker envoie `audio.state` à chaque changement).
  Le premier message de l'abonné peut être `audio.get`, qui demande l'état tout de suite.
- **Plusieurs émetteurs** : un serveur accepte plusieurs connexions simultanées (8 au plus) ; les lignes d'une même connexion arrivent dans l'ordre.

## 3. Les messages, par destinataire

### 3.1 `cdx.shell` (la barre)
| `type` | `data` | Effet |
|---|---|---|
| `notify` | `title` (texte, ≤ 80), `text` (texte, ≤ 400), `level` (`info` `warn` `error`, défaut `info`) | une notification : la barre affiche une cloche et le nombre de notifications non vues, le centre rapide les liste (50 au plus, la plus récente en haut) |

Émetteurs : **Messages** (messages privés et mentions, en plus de la notification de Windows), **cdx-browser** (téléchargement terminé ou échoué), **Audio Linker** (erreurs et avertissements du groupe ; une même ligne n'est pas répétée avant 10 s).

### 3.2 `cdx.explorer`
| `type` | `data` | Effet |
|---|---|---|
| `open-path` | `path` (chemin absolu d'un dossier ; absent = Documents) | ouvre une fenêtre sur ce dossier |
| `select` | `path` (chemin absolu d'un fichier ou d'un dossier) | ouvre le dossier parent avec l'élément sélectionné |

Émetteur : **cdx-browser** (« Afficher dans le dossier » d'un téléchargement ; l'Explorateur est lancé au besoin, et l'explorateur de Windows reste le repli).

### 3.3 `cdx.browser`
| `type` | `data` | Effet |
|---|---|---|
| `open-url` | `url` (`http:` ou `https:` seulement, ≤ 2000 ; absent = onglet vide) | ouvre l'adresse dans un nouvel onglet |
| `open-file` | `path` (chemin absolu d'un fichier qui existe, d'une extension affichable : `.html` `.htm` `.pdf` `.svg` `.png` `.jpg` `.jpeg` `.gif` `.webp` `.bmp` `.txt` `.mp3` `.ogg` `.wav` `.mp4` `.webm`) | ouvre le fichier dans un nouvel onglet (`file:///`) |

Émetteurs : **Messages** (`open-url` : un lien cliqué s'ouvre dans le navigateur CDX s'il tourne ou s'il est installé, sinon dans celui de Windows), **cdx-explorer** (`open-file` : le double-clic sur un fichier de ces types).

### 3.4 `cdx.audio_linker`
| `type` | `data` | Effet |
|---|---|---|
| `audio.get` | — | demande l'état |
| `audio.toggle` | — | démarre ou arrête le groupe |
| `audio.volume` | `v` (entier 0 à 100), `commit` (booléen) | volume du groupe ; `commit` l'enregistre et rafraîchit les fenêtres d'Audio Linker |
| `audio.mute` | `on` (booléen) | coupe ou rétablit le son du groupe |
| `audio.setup` | `name` (nom d'un setup existant, ≤ 200) | joue ce setup |

Audio Linker répond par des messages `audio.state` (`running`, `starting`, `volume`, `muted`, `playing`, `setups` = liste de `{name, count}`), à la connexion et à chaque changement.
Un seul abonné à la fois pour l'instant.

### 3.4b `cdx.repos` (Dépôts)
| `type` | `data` | Effet |
|---|---|---|
| `show` | — | passe la fenêtre de Dépôts devant (c'est ce que fait un second lancement de `cdx-repos.exe`) |

Dépôts est en lecture seule : il ne reçoit que `show`. Il émet `open-path` vers l'Explorateur (« Ouvrir le dossier ») et `open-url` vers le navigateur (« Voir sur GitHub », adresses des hébergeurs connus seulement : github.com, gitlab.com, bitbucket.org, codeberg.org),
tous deux lancés au besoin ; le repli est l'explorateur et le navigateur de Windows.

### 3.4c `cdx.terminal` (Terminal)
| `type` | `data` | Effet |
|---|---|---|
| `show` | — | passe la fenêtre du terminal devant (c'est ce que fait un second lancement de `cdx-terminal.exe` sans argument) |
| `open-path` | `path` (chemin absolu d'un dossier ; un fichier donne son dossier) | ouvre un **onglet** dont le shell démarre dans ce dossier, et passe la fenêtre devant (second lancement `cdx-terminal.exe <dossier>`, « Ouvrir dans un terminal » de l'Explorateur) |

Un chemin qui n'est pas un dossier existant est refusé. L'Explorateur envoie `open-path` au terminal CDX et le lance au besoin (chemin de `apps.json`) ; le repli est Windows Terminal, puis `cmd.exe`.

### 3.4d Le canal de pilotage `cdx.<nom>.pilot` (cdx-windows)
À côté de son tube du bus, chaque programme de cdx-windows ouvre un tube **de commande** `cdx.<nom>.pilot` (utilisateur courant, une ligne reçue → une ligne rendue), par lequel
**Pilote** (le chat avec Claude, `cdx-pilote`) le commande : `state` (son état), `cmd <json>` (une commande de sa page, validée comme si elle venait d'elle), et ce que le programme ajoute
(le navigateur : `page.text`, `page.find`, `page.click`, `page.fill`, `page.scroll`, `page.shot`, des scripts fixes sur l'onglet actif). Jamais `eval` : exécuter du JavaScript reçu reste
le fait du canal de test `.ctl`, qui n'existe qu'avec `debug.txt`. Un message refusé rend `ERREUR …`.

### 3.5 Lancer la destination absente
`%APPDATA%\CDXpps.json` donne, pour chaque nom, le chemin de l'exécutable : `{ "browser": "C:\…\cdx-browser.exe" }`. Chaque programme y écrit son propre chemin au démarrage. Un émetteur qui
veut atteindre une application absente (un lien cliqué dans Messages, par exemple) lance cet exécutable avec la cible en argument (`cdx-browser.exe <adresse>`) : au démarrage, l'application la traite,
et si elle tourne déjà, sa **seconde instance** retransmet l'argument à la première par ce même bus (`open-url`, `open-path`) puis s'arrête. L'émetteur ne lance que les noms de la liste
des applications (§2), jamais un chemin reçu d'ailleurs.

### 3.6 Essais isolés
Trois variables d'environnement, réservées aux essais, évitent de toucher aux vrais programmes : `CDX_PIPE_PREFIX` (remplace `cdx.` dans le nom des tubes et sépare aussi le verrou d'instance unique),
`CDX_SUITE_DIR` (remplace `%APPDATA%\CDX`) et `CDX_DATA_DIR` (remplace `%LOCALAPPDATA%\CdxShell`, côté cdx-windows).

## 4. Clients

| Langage | Où | Contenu |
|---|---|---|
| C# | `cdx-windows/src/Cdx.Host/Bus.cs`, `Suite.cs` | serveur (liste blanche), émetteur, lecture et écriture de `suite.json` |
| Rust | `cdx-ui/bus/rust` (crate `cdx-bus`) | émetteur, lecture de `suite.json`, sondage |
| C++ | `cdx-ui/bus/cpp/cdx_bus.h` | en-tête seul : émetteur, ligne de message, lecture de `suite.json` |

Chaque client a sa suite de tests de protocole (message valide, type inconnu, champ invalide, ligne trop longue, utilisateur autre). Le script d'intégration
`cdx-windows/tests/bus.ps1` vérifie l'ensemble de bout en bout.
