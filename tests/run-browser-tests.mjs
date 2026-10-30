// Lance les pages de test (tests/*.test.html) dans un Chrome headless séparé, servies par un petit serveur local temporaire à la racine du dépôt,
// et affiche leur sortie (#out). Code de sortie 1 si une page signale un échec.
//   node tests/run-browser-tests.mjs [page.test.html ...]
import http from 'node:http';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
const run = promisify(execFile);   // asynchrone : le serveur ci-dessous doit continuer à répondre pendant que Chrome charge la page

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1')), '..');
const chrome = ['C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'].find(p => fs.existsSync(p));
if (!chrome) { console.error('Ni Chrome ni Edge trouvés'); process.exit(2); }
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.json': 'application/json' };
const srv = http.createServer((req, res) => {
  const f = path.join(root, decodeURIComponent(req.url.split('?')[0]));
  if (!f.startsWith(root) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404).end(); return; }
  res.writeHead(200, { 'content-type': types[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res);
});
await new Promise(r => srv.listen(0, '127.0.0.1', r));
const port = srv.address().port;
const pages = process.argv.length > 2 ? process.argv.slice(2) : fs.readdirSync(path.join(root, 'tests')).filter(f => f.endsWith('.test.html'));
let failed = false;
for (const p of pages) {
  const prof = fs.mkdtempSync(path.join(os.tmpdir(), 'kdx-test-'));
  try {
    const { stdout: dom } = await run(chrome, ['--headless=new', '--no-first-run', '--disable-component-update', '--disable-background-networking', `--user-data-dir=${prof}`, '--virtual-time-budget=8000', '--dump-dom', `http://127.0.0.1:${port}/tests/${p}`], { encoding: 'utf8', timeout: 60000, maxBuffer: 16 << 20 });
    const m = /<pre id="out">([\s\S]*?)<\/pre>/.exec(dom);
    const out = m ? m[1].replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&amp;/g, '&') : '(aucune sortie)';
    console.log(`== ${p}\n${out}`);
    if (!/RÉSULTAT : TOUT EST BON/.test(out)) failed = true;
  } catch (e) { console.log(`== ${p}\nERREUR : ${e.message.split('\n')[0]}`); failed = true; }
  finally { fs.rmSync(prof, { recursive: true, force: true }); }
}
srv.close();
process.exit(failed ? 1 : 0);
