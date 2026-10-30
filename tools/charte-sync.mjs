// node tools/charte-sync.mjs --check <application> [--dist dossier]     compare les copies de l'application à dist/ ; code 1 au moindre écart
// node tools/charte-sync.mjs --write <application> [--dist dossier]     copie dist/ vers l'application (phase 3 : une branche par application)
// <application> : nom d'un profil de tools/apps/<nom>.json (chemins des copies de la charte dans l'application).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadProfile, compareApp, writeApp, checkDist } from './lib/sync.mjs';

const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);
const mode = args.find(a => a === '--check' || a === '--write');
const di = args.indexOf('--dist'), dist = di >= 0 ? path.resolve(args[di + 1]) : path.join(repo, 'dist');
const name = args.filter((a, i) => !a.startsWith('--') && args[i - 1] !== '--dist')[0];
if (!mode || !name) { console.error('usage : node tools/charte-sync.mjs --check|--write <application> [--dist dossier]'); process.exit(2); }

const file = fs.existsSync(name) ? name : path.join(repo, 'tools', 'apps', name + '.json');
if (!fs.existsSync(file)) { console.error('profil introuvable : ' + file); process.exit(2); }
const stale = di < 0 ? checkDist(repo, dist) : [];
if (stale.length) { console.error('dist/ est périmé (' + stale.join(', ') + ') : lancer node tools/build-dist.mjs'); process.exit(2); }
const profile = loadProfile(file, repo);

if (mode === '--write') { for (const f of writeApp(profile, dist)) console.log('copié : ' + f); process.exit(0); }
const rows = compareApp(profile, dist);
let bad = 0;
for (const r of rows) { console.log(`${r.state === 'ok' ? 'OK    ' : r.state === 'diff' ? 'DIFFÈRE' : 'ABSENT '}  ${r.path}  (dist/${r.name})`); if (r.state !== 'ok') bad++; }
console.log(rows.length ? `${profile.name} : ${bad ? bad + ' copie(s) à synchroniser sur ' + rows.length : 'à jour'}` : `${profile.name} : aucune copie déclarée (voir « notes » du profil)`);
process.exit(bad ? 1 : 0);
