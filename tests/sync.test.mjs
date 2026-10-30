// node --test tests/ : dist/, empreintes, comparaison et copie vers une application.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildDist, writeDist, checkDist, compareApp, writeApp, DIST_FILES } from '../tools/lib/sync.mjs';

const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const tmp = () => fs.mkdtempSync(path.join(os.tmpdir(), 'kdx-sync-'));

test('dist : tous les fichiers déclarés existent, le manifeste porte la version et une empreinte par fichier', () => {
  const { files, manifest, version } = buildDist(repo);
  for (const n of Object.keys(DIST_FILES)) assert.ok(files[n] && files[n].length > 0, n);
  assert.equal(manifest.kdxUi, version);
  assert.equal(Object.keys(manifest.files).length, Object.keys(DIST_FILES).length);
  assert.match(manifest.files['kdx-ui.css'].sha256, /^[0-9a-f]{64}$/);
});

test('dist : la version est écrite dans kdx-bridge.js (le marqueur disparaît)', () => {
  const { files, version } = buildDist(repo);
  const js = files['kdx-bridge.js'].toString('utf8');
  assert.ok(!js.includes('KDX_UI_VERSION') && js.includes(`version: "${version}"`));
});

test('dist : construction déterministe (deux fois les mêmes octets)', () => {
  const a = buildDist(repo).files, b = buildDist(repo).files;
  for (const n of Object.keys(a)) assert.ok(a[n].equals(b[n]), n);
});

test('checkDist : à jour après écriture, périmé après modification', () => {
  const out = tmp(); writeDist(repo, out);
  assert.deepEqual(checkDist(repo, out), []);
  fs.appendFileSync(path.join(out, 'kdx-ui.css'), '/* modifié à la main */');
  assert.deepEqual(checkDist(repo, out), ['kdx-ui.css']);
  fs.rmSync(path.join(out, 'icons.js'));
  assert.deepEqual(checkDist(repo, out).sort(), ['icons.js', 'kdx-ui.css']);
});

test('compareApp / writeApp : absent -> écrit -> ok -> modifié -> diffère', () => {
  const dist = tmp(), app = tmp(); writeDist(repo, dist);
  const profile = { name: 'essai', rootAbs: app, files: { 'kdx-ui.css': 'ui/theme.css', 'themes.css': 'ui/themes.css' } };
  assert.deepEqual(compareApp(profile, dist).map(r => r.state), ['absent', 'absent']);
  writeApp(profile, dist);
  assert.deepEqual(compareApp(profile, dist).map(r => r.state), ['ok', 'ok']);
  fs.appendFileSync(path.join(app, 'ui', 'theme.css'), '\n.x { border-radius: 4px; }');
  assert.deepEqual(compareApp(profile, dist).map(r => r.state), ['diff', 'ok']);
});

test('writeApp écrit kdx-sync.json ; kdx-verify.mjs repère une copie modifiée à la main', async () => {
  const { execFileSync } = await import('node:child_process');
  const dist = tmp(), app = tmp(); writeDist(repo, dist);
  const profile = { name: 'essai', rootAbs: app, manifest: 'ui/kdx/kdx-sync.json', files: { 'kdx-ui.css': 'ui/kdx/kdx-ui.css', 'themes.css': 'ui/kdx/themes.css', 'kdx-verify.mjs': 'tools/kdx-verify.mjs' } };
  writeApp(profile, dist);
  const run = () => { try { return { code: 0, out: execFileSync('node', ['tools/kdx-verify.mjs', 'ui/kdx/kdx-sync.json'], { cwd: app, encoding: 'utf8' }) }; } catch (e) { return { code: e.status, out: e.stdout }; } };
  assert.equal(run().code, 0);
  fs.appendFileSync(path.join(app, 'ui', 'kdx', 'themes.css'), '\n/* retouché */');
  const r = run();
  assert.equal(r.code, 1); assert.match(r.out, /MODIFIÉ\s+ui\/kdx\/themes\.css/);
  fs.rmSync(path.join(app, 'ui', 'kdx', 'kdx-ui.css'));
  assert.match(run().out, /ABSENT\s+ui\/kdx\/kdx-ui\.css/);
});
