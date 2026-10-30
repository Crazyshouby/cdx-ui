// node tools/build-dist.mjs [--check]
// Construit dist/ (les fichiers que les applications embarquent + MANIFEST.json avec version et empreintes). --check : n'écrit rien, code 1 si dist/ est périmé (CI).
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { writeDist, checkDist } from './lib/sync.mjs';

const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..'), out = path.join(repo, 'dist');
if (process.argv.includes('--check')) {
  const stale = checkDist(repo, out);
  console.log(stale.length ? 'dist/ PÉRIMÉ : ' + stale.join(', ') + '\n→ node tools/build-dist.mjs' : 'dist/ à jour');
  process.exit(stale.length ? 1 : 0);
}
console.log('dist/ écrit (kdx-ui ' + writeDist(repo, out) + ')');
