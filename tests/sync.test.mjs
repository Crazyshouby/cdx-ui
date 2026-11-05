// node --test tests/ : dist/, empreintes, comparaison et copie vers une application.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildDist, writeDist, checkDist, compareApp, writeApp, DIST_FILES } from '../tools/lib/sync.mjs';

const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const tmp = () => fs.mkdtempSync(path.join(os.tmpdir(), 'cdx-sync-'));

test('dist : tous les fichiers déclarés existent, le manifeste porte la version et une empreinte par fichier', () => {
  const { files, manifest, version } = buildDist(repo);
  for (const n of Object.keys(DIST_FILES)) assert.ok(files[n] && files[n].length > 0, n);
  assert.equal(manifest.cdxUi, version);
  assert.equal(Object.keys(manifest.files).length, Object.keys(DIST_FILES).length);
  assert.match(manifest.files['cdx-ui.css'].sha256, /^[0-9a-f]{64}$/);
});

test('dist : la version est écrite dans cdx-bridge.js (le marqueur disparaît)', () => {
  const { files, version } = buildDist(repo);
  const js = files['cdx-bridge.js'].toString('utf8');
  assert.ok(!js.includes('CDX_UI_VERSION') && js.includes(`version: "${version}"`));
});

test('dist : construction déterministe (deux fois les mêmes octets)', () => {
  const a = buildDist(repo).files, b = buildDist(repo).files;
  for (const n of Object.keys(a)) assert.ok(a[n].equals(b[n]), n);
});

test('checkDist : à jour après écriture, périmé après modification', () => {
  const out = tmp(); writeDist(repo, out);
  assert.deepEqual(checkDist(repo, out), []);
  fs.appendFileSync(path.join(out, 'cdx-ui.css'), '/* modifié à la main */');
  assert.deepEqual(checkDist(repo, out), ['cdx-ui.css']);
  fs.rmSync(path.join(out, 'icons.js'));
  assert.deepEqual(checkDist(repo, out).sort(), ['cdx-ui.css', 'icons.js']);
});

test('compareApp / writeApp : absent -> écrit -> ok -> modifié -> diffère', () => {
  const dist = tmp(), app = tmp(); writeDist(repo, dist);
  const profile = { name: 'essai', rootAbs: app, files: { 'cdx-ui.css': 'ui/theme.css', 'themes.css': 'ui/themes.css' } };
  assert.deepEqual(compareApp(profile, dist).map(r => r.state), ['absent', 'absent']);
  writeApp(profile, dist);
  assert.deepEqual(compareApp(profile, dist).map(r => r.state), ['ok', 'ok']);
  fs.appendFileSync(path.join(app, 'ui', 'theme.css'), '\n.x { border-radius: 4px; }');
  assert.deepEqual(compareApp(profile, dist).map(r => r.state), ['diff', 'ok']);
});

test('writeApp écrit cdx-sync.json ; cdx-verify.mjs repère une copie modifiée à la main', async () => {
  const { execFileSync } = await import('node:child_process');
  const dist = tmp(), app = tmp(); writeDist(repo, dist);
  const profile = { name: 'essai', rootAbs: app, manifest: 'ui/cdx/cdx-sync.json', files: { 'cdx-ui.css': 'ui/cdx/cdx-ui.css', 'themes.css': 'ui/cdx/themes.css', 'cdx-verify.mjs': 'tools/cdx-verify.mjs' } };
  writeApp(profile, dist);
  const run = () => { try { return { code: 0, out: execFileSync('node', ['tools/cdx-verify.mjs', 'ui/cdx/cdx-sync.json'], { cwd: app, encoding: 'utf8' }) }; } catch (e) { return { code: e.status, out: e.stdout }; } };
  assert.equal(run().code, 0);
  fs.appendFileSync(path.join(app, 'ui', 'cdx', 'themes.css'), '\n/* retouché */');
  const r = run();
  assert.equal(r.code, 1); assert.match(r.out, /MODIFIÉ\s+ui\/cdx\/themes\.css/);
  fs.rmSync(path.join(app, 'ui', 'cdx', 'cdx-ui.css'));
  assert.match(run().out, /ABSENT\s+ui\/cdx\/cdx-ui\.css/);
});
