// node tools/drift-report.mjs [--out docs/RAPPORT-DERIVE.md]
// Rapport de dérive : pour chaque profil de tools/apps/*.json, les écarts à la charte (charte-lint, SANS exceptions), les mesures qui les éclairent
// (tailles, arrondis, couleurs réellement employés) et l'état des copies de la charte par rapport à dist/. Ne modifie aucune application.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { RULES, loadPalette, lintPaths, summarize, collect, parseAllow } from './lib/lint.mjs';
import { loadProfile, compareApp, checkDist } from './lib/sync.mjs';

const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const oi = process.argv.indexOf('--out'), out = path.resolve(repo, oi >= 0 ? process.argv[oi + 1] : 'docs/RAPPORT-DERIVE.md');
const palette = loadPalette(repo), tokens = JSON.parse(fs.readFileSync(path.join(repo, 'tokens.json'), 'utf8'));
const version = fs.readFileSync(path.join(repo, 'VERSION'), 'utf8').trim(), dist = path.join(repo, 'dist');
const stale = checkDist(repo, dist);
const cnt = (arr) => { const m = new Map(); for (const x of arr) m.set(x, (m.get(x) || 0) + 1); return [...m.entries()].sort((a, b) => b[1] - a[1]); };
const fmt = (pairs, n = 8) => pairs.slice(0, n).map(([k, v]) => `\`${k}\` ×${v}`).join(', ') || '—';

// Mesures qui éclairent les écarts : ce que l'application emploie vraiment.
function measures(files) {
  const sizes = [], radii = [], weights = [], colors = [];
  for (const f of files) {
    const t = fs.readFileSync(f, 'utf8');
    for (const m of t.matchAll(/(?<![\w-])font-size\s*:\s*([\d.]+px)/g)) sizes.push(m[1]);
    for (const m of t.matchAll(/(?<![\w-])font\s*:\s*(?:[^;}\n]*?\s)?([\d.]+)px/g)) sizes.push(m[1] + 'px');
    for (const m of t.matchAll(/border(?:-[a-z]+){0,2}-radius\s*:\s*([^;}\n]+)/g)) if (!/^\s*0/.test(m[1])) radii.push(m[1].trim());
    for (const m of t.matchAll(/font-weight\s*:\s*(\w+)/g)) weights.push(m[1]);
    for (const m of t.matchAll(/(?<![&\w%])#([0-9a-fA-F]{6})\b/g)) { const h = '#' + m[1].toLowerCase(); const [r, g, b] = [1, 3, 5].map(k => parseInt(h.slice(k, k + 2), 16)); if (!palette.has(h) && !(r === g && g === b)) colors.push(h); }
  }
  return { sizes: cnt(sizes), radii: cnt(radii), weights: cnt(weights), colors: cnt(colors), distinctColors: new Set(colors).size };
}

// Constantes et couleurs de paint.rs (kdx-frames) contre tokens.json.
function rustCheck(file) {
  const t = fs.readFileSync(file, 'utf8'), rows = [];
  const map = { RING: ['frame_ring + frame_outline', 'anneau de cadre : 5 px + 1 px de contour noir (CHARTE.md §4)'], TITLE: ['title_height', 'barre de titre'], BUTTON: ['title_button_size', 'boutons de titre'] };
  for (const m of t.matchAll(/pub const (\w+): i32 = (\d+);/g)) if (map[m[1]]) { const tk = map[m[1]][0].split(' + '), exp = tk.reduce((n, k) => n + tokens.measures[k], 0); rows.push({ what: `${m[1]} = ${m[2]}`, token: `${map[m[1]][0]} = ${exp}`, same: +m[2] === exp, note: map[m[1]][1] }); }
  const cols = new Set();
  for (const m of t.matchAll(/rgb\(\s*0x([0-9a-fA-F]{1,2})\s*,\s*(?:0x([0-9a-fA-F]{1,2})|0)\s*,\s*(?:0x([0-9a-fA-F]{1,2})|0)\s*\)/g)) cols.add('#' + [m[1], m[2] || '0', m[3] || '0'].map(x => x.padStart(2, '0')).join('').toLowerCase());
  return { rows, colors: [...cols], offTokens: [...cols].filter(c => !palette.has(c)) };
}

const apps = fs.readdirSync(path.join(repo, 'tools', 'apps')).filter(f => f.endsWith('.json')).sort().map(f => ({ ...loadProfile(path.join(repo, 'tools', 'apps', f), repo), slug: f.replace(/\.json$/, '') }));
const res = apps.map(p => {
  const exists = fs.existsSync(p.rootAbs);
  const sync = exists && stale.length === 0 ? compareApp(p, dist) : [];
  // Une copie identique à dist/ est la charte elle-même : elle se contrôle à la source (avec ses exceptions), pas ici.
  const identical = new Set(sync.filter(x => x.state === 'ok').map(x => path.resolve(p.rootAbs, x.path)));
  const allowFile = path.join(repo, 'tools', 'apps', p.slug + '.allow');
  const allow = fs.existsSync(allowFile) ? parseAllow(fs.readFileSync(allowFile, 'utf8')) : [];
  const files = exists ? collect((p.lint || []).map(x => path.join(p.rootAbs, x))).filter(f => !identical.has(path.resolve(f))) : [];
  const { violations } = exists && files.length ? lintPaths(files, { palette, allow, base: p.rootAbs }) : { violations: [] };
  return { p, exists, files, violations, identical: identical.size, s: summarize(violations), m: measures(files), sync, rust: exists && p.rust ? rustCheck(path.join(p.rootAbs, p.rust)) : null };
});

const L = [];
const rules = Object.keys(RULES);
L.push('# Rapport de dérive à la charte KDX-UI', '', `Version de la charte : **${version}** · généré le ${new Date().toISOString().slice(0, 10)} par \`node tools/drift-report.mjs\`.`,
  'Les comptes sont des **déclarations** (lignes de CSS / HTML / JS), pas des éléments affichés. Une copie identique à `dist/` n\'est pas recomptée (elle se contrôle à la source) ; une exception propre à une application est déclarée, avec sa raison, dans `tools/apps/<application>.allow` et comptée à part (« tolérés »).',
  'Les règles sont celles de `CHARTE.md` §8 ; la charte elle-même passe le même contrôle avec 18 exceptions justifiées dans `charte-lint.allow`.', '');
if (stale.length) L.push(`> ⚠ dist/ est périmé (${stale.join(', ')}) : les comparaisons de copies sont omises. Lancer \`node tools/build-dist.mjs\`.`, '');

L.push('## Vue d\'ensemble', '', '| Application | fichiers | ' + rules.join(' | ') + ' | **total** | tolérés |', '|---|---:|' + rules.map(() => '---:').join('|') + '|---:|---:|');
for (const r of res) L.push(`| ${r.p.name} | ${r.files.length} | ${rules.map(k => r.s.by[k] || 0).join(' | ')} | **${r.s.total}** | ${r.s.tolerated} |`);
L.push('', '| règle | ce qu\'elle mesure |', '|---|---|', ...rules.map(k => `| \`${k}\` | ${RULES[k]} |`), '');

for (const r of res) {
  L.push(`## ${r.p.name}`, '', r.p.notes, '');
  if (!r.exists) { L.push(`Dossier introuvable : \`${r.p.root}\`.`, ''); continue; }
  if (r.p.lint && r.p.lint.length) {
    L.push(`**${r.s.total} écart(s)** (+ ${r.s.tolerated} toléré(s) avec raison) dans ${r.files.length} fichier(s) examiné(s)${r.identical ? `, ${r.identical} copie(s) identique(s) de la charte non recomptée(s)` : ''}.`, '', '| fichier | ' + rules.join(' | ') + ' |', '|---|' + rules.map(() => '---:').join('|') + '|');
    for (const [f, by] of Object.entries(r.s.byFile).sort((a, b) => Object.values(b[1]).reduce((x, y) => x + y, 0) - Object.values(a[1]).reduce((x, y) => x + y, 0))) L.push(`| \`${f}\` | ${rules.map(k => by[k] || '·').join(' | ')} |`);
    L.push('', '**Ce que l\'application emploie réellement**', '',
      `- tailles de police : ${fmt(r.m.sizes)} (la charte : une seule, 14 px)`,
      `- arrondis : ${fmt(r.m.radii)} (la charte : aucun)`,
      `- graisses : ${fmt(r.m.weights)} (la charte : aucune)`,
      `- couleurs hors jetons : **${r.m.distinctColors}** valeurs distinctes, dont ${fmt(r.m.colors, 6)}`, '');
    for (const k of rules) {
      const ex = r.violations.filter(v => v.rule === k).slice(0, 3); if (!ex.length) continue;
      L.push(`<details><summary><code>${k}</code> : ${r.s.by[k]} (exemples)</summary>`, '', ...ex.map(v => `- \`${v.file}:${v.line}\` — \`${v.text.replace(/`/g, "'").slice(0, 140)}\``), '', '</details>', '');
    }
  }
  if (Object.keys(r.p.files || {}).length) {
    L.push('**Copies de la charte** (comparées à `dist/`)', '', '| copie dans l\'application | source (dist/) | état | octets (app / dist) |', '|---|---|---|---|');
    for (const x of r.sync) L.push(`| \`${x.path}\` | \`${x.name}\` | ${x.state === 'ok' ? 'identique' : x.state === 'diff' ? '**diffère**' : '**absente**'} | ${x.appBytes} / ${x.distBytes} |`);
    L.push('');
  }
  if (r.rust) {
    L.push('**Constantes de `paint.rs` contre `tokens.json`**', '', '| constante Rust | jeton | identique | remarque |', '|---|---|---|---|', ...r.rust.rows.map(x => `| \`${x.what}\` | \`${x.token}\` | ${x.same ? 'oui' : '**non**'} | ${x.note} |`),
      '', `Couleurs écrites dans \`paint.rs\` : ${r.rust.colors.map(c => '`' + c + '`').join(', ')}.`, r.rust.offTokens.length ? `Hors jetons : ${r.rust.offTokens.map(c => '`' + c + '`').join(', ')}.` : 'Toutes sont des jetons de la charte.', '');
  }
}

const total = res.map(r => ({ n: r.p.name, t: r.s.total })).filter(x => x.t);
L.push('## Lecture', '');
const max = total.slice().sort((a, b) => b.t - a.t)[0];
if (max) L.push(`- L'écart brut le plus important est celui de **${max.n}** (${max.t} écart(s) sur ${total.reduce((a, b) => a + b.t, 0)} au total).`);
L.push('- Les applications C# (shell, Explorateur, Navigateur) lisent la charte sans copie : leur dérive se mesure par ce rapport, pas par synchronisation.',
  '- Rien n\'est corrigé ici : la phase 3 du plan traite KIRC, `kdx-frames` puis AudioLinker, une branche et une version mineure chacune, après validation de ce rapport.', '');

fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, L.join('\n'), 'utf8');
console.log('écrit : ' + path.relative(repo, out));
for (const r of res) console.log(`  ${r.p.name.padEnd(46)} ${String(r.s.total).padStart(4)} écart(s) dans ${r.files.length} fichier(s)`);
