// dist/ (les fichiers que les applications embarquent, avec leurs empreintes) et la synchronisation vers une application.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

// nom dans dist/  <-  fichier source du dépôt
export const DIST_FILES = {
  'cdx-ui.css': 'cdx-ui.css', 'cdx-frame.css': 'cdx-frame.css', 'themes.css': 'themes.css', 'fonts.css': 'fonts.css', 'icons.js': 'icons.js',
  'cdx-bridge.js': 'cdx-bridge.js', 'cdx-frame.js': 'cdx-frame.js', 'cdx-columns.js': 'cdx-columns.js', 'cdx-split.js': 'cdx-split.js', 'cdx-tokens.h': 'generated/cdx-tokens.h', 'tokens.rs': 'generated/tokens.rs', 'cdx-verify.mjs': 'tools/cdx-verify.mjs', 'cdx_bus.h': 'bus/cpp/cdx_bus.h', 'cdx_bus.rs': 'bus/rust/cdx_bus.rs', 'tokens.json': 'tokens.json', 'pixel_engine.py': 'gen/pixel_engine.py', 'charte-lint.mjs': 'tools/charte-lint.mjs', 'lint.mjs': 'tools/lib/lint.mjs',
};

export const sha256 = buf => crypto.createHash('sha256').update(buf).digest('hex');
// Lecture avec les fins de ligne ramenées à LF : sous Windows (autocrlf) la copie de travail est en CRLF alors que git et la CI ont du LF ; sans cela les
// empreintes de MANIFEST.json diffèrent d'une machine à l'autre. Tout ce que dist/ contient est du texte.
const read = p => Buffer.from(fs.readFileSync(p).toString('latin1').replace(/\r\n/g, '\n'), 'latin1');

// Contenu de dist/ en mémoire : { nom: Buffer }, plus MANIFEST.json. Ne contient aucune date : deux constructions identiques donnent les mêmes octets.
export function buildDist(repo) {
  const version = fs.readFileSync(path.join(repo, 'VERSION'), 'utf8').trim();
  const files = {};
  for (const [name, src] of Object.entries(DIST_FILES)) {
    let buf = read(path.join(repo, src));
    if (name === 'cdx-bridge.js') buf = Buffer.from(buf.toString('utf8').replace('CDX_UI_VERSION', version), 'utf8');
    files[name] = buf;
  }
  const manifest = { cdxUi: version, files: Object.fromEntries(Object.entries(files).map(([n, b]) => [n, { sha256: sha256(b), bytes: b.length }])) };
  files['MANIFEST.json'] = Buffer.from(JSON.stringify(manifest, null, 2) + '\n', 'utf8');
  return { version, files, manifest };
}

export function writeDist(repo, outDir) {
  const { files, version } = buildDist(repo);
  fs.mkdirSync(outDir, { recursive: true });
  for (const [n, b] of Object.entries(files)) fs.writeFileSync(path.join(outDir, n), b);
  return version;
}

// dist/ est-il à jour par rapport aux sources ? Liste des fichiers périmés ou absents.
export function checkDist(repo, outDir) {
  const { files } = buildDist(repo), stale = [];
  for (const [n, b] of Object.entries(files)) { const p = path.join(outDir, n); if (!fs.existsSync(p) || !read(p).equals(b)) stale.push(n); }
  return stale;
}

// Un profil d'application : { name, root (relatif au dépôt cdx-ui ou absolu), files: { "nom dans dist": "chemin relatif à root" }, lint: [chemins relatifs à root], notes }.
export function loadProfile(file, repo) {
  const p = JSON.parse(fs.readFileSync(file, 'utf8'));
  p.rootAbs = path.resolve(repo, p.root);
  return p;
}

// ok | diff | absent pour chaque fichier déclaré ; + version de dist lue dans MANIFEST.json
export function compareApp(profile, distDir) {
  const rows = [];
  for (const [name, rel] of Object.entries(profile.files || {})) {
    const d = path.join(distDir, name), a = path.join(profile.rootAbs, rel);
    const state = !fs.existsSync(a) ? 'absent' : read(a).equals(read(d)) ? 'ok' : 'diff';
    rows.push({ name, path: rel, state, appBytes: fs.existsSync(a) ? fs.statSync(a).size : 0, distBytes: fs.statSync(d).size });
  }
  return rows;
}

export function writeApp(profile, distDir) {
  const done = [], manifest = { cdxUi: JSON.parse(read(path.join(distDir, 'MANIFEST.json')).toString('utf8')).cdxUi, files: {} };
  for (const [name, rel] of Object.entries(profile.files || {})) {
    const a = path.join(profile.rootAbs, rel);
    fs.mkdirSync(path.dirname(a), { recursive: true });
    fs.copyFileSync(path.join(distDir, name), a); done.push(rel);
    manifest.files[rel.split(path.sep).join('/')] ={ from: name, sha256: sha256(Buffer.from(read(a).toString('latin1').replace(/\r\n/g, '\n'), 'latin1')) };   // fins de ligne ignorées (voir cdx-verify.mjs)
  }
  // cdx-sync.json : ce que cdx-verify.mjs contrôle dans la CI de l'application (copies non modifiées à la main)
  if (profile.manifest) { fs.mkdirSync(path.dirname(path.join(profile.rootAbs, profile.manifest)), { recursive: true }); fs.writeFileSync(path.join(profile.rootAbs, profile.manifest), JSON.stringify(manifest, null, 2) + '\n'); done.push(profile.manifest); }
  return done;
}
