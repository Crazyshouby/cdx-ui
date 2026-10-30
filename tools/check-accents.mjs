// node tools/check-accents.mjs
// La liste des accents (rouge, bleu, vert…) est écrite à la main dans plusieurs programmes (clients du bus, kdx-windows, KIRC) : tokens.json en est la source,
// ce contrôle vérifie que chaque fichier de tools/accents.json les connaît tous (entre guillemets) et n'en invente aucun. Un fichier absent (dépôt voisin non
// présent, en CI par exemple) est signalé et ignoré ; un fichier présent qui s'écarte fait échouer.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..'), dev = path.dirname(repo);
const tokens = JSON.parse(fs.readFileSync(path.join(repo, 'tokens.json'), 'utf8'));
const names = ['rouge', ...Object.keys(tokens.themes).filter(n => n !== 'rouge')];
const cfg = JSON.parse(fs.readFileSync(path.join(repo, 'tools', 'accents.json'), 'utf8'));
let bad = 0, seen = 0;
for (const f of cfg.files) {
  const file = f.path.startsWith('kdx-ui/') ? path.join(repo, f.path.slice(7)) : path.join(dev, f.path);
  if (!fs.existsSync(file)) { console.log('absent (ignoré)  ' + f.path); continue; }
  seen++;
  const text = fs.readFileSync(file, 'utf8');
  const alias = f.alias || {};
  const missing = names.filter(n => !new RegExp('["\'`]' + (alias[n] || n) + '["\'`]').test(text));
  if (missing.length) { console.log('ÉCART  ' + f.path + '  manque : ' + missing.join(', ')); bad++; }
  else console.log('ok     ' + f.path);
}
console.log(bad ? `${bad} fichier(s) ne connaissent pas tous les accents de tokens.json (${names.join(', ')})` : `${seen} fichier(s) cohérents avec tokens.json (${names.length} accents)`);
process.exit(bad ? 1 : 0);
