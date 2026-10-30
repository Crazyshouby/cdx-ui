// node --test tests/ : une règle de charte-lint, un cas conforme, un cas en écart.
import test from 'node:test';
import assert from 'node:assert/strict';
import { lintText, parseAllow, allowedBy, loadPalette } from '../tools/lib/lint.mjs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const palette = loadPalette(repo);
const rules = css => lintText(css, { file: 't.css', palette }).map(v => v.rule);

test('radius : 0 conforme, tout arrondi en écart', () => {
  assert.deepEqual(rules('.a { border-radius: 0; }'), []);
  assert.deepEqual(rules('.a { border-radius: 0 0 0 0; }'), []);
  assert.deepEqual(rules('.a { border-radius: 3px; }'), ['radius']);
  assert.deepEqual(rules('.a { border-radius: 50%; }'), ['radius']);
  assert.deepEqual(rules('.a { border-top-left-radius: 4px; }'), ['radius']);
  assert.deepEqual(rules("el.style.borderRadius = '6px'"), ['radius']);
});

test('weight : pas de gras, y compris dans le raccourci font', () => {
  assert.deepEqual(rules('.a { font-weight: 400; }'), []);
  assert.deepEqual(rules('.a { font-weight: normal; }'), []);
  assert.deepEqual(rules('.a { font-weight: 700; }'), ['weight']);
  assert.deepEqual(rules('.a { font-weight: bold; }'), ['weight']);
  assert.deepEqual(rules('.a { font: 700 14px sans-serif; }'), ['weight']);
  assert.deepEqual(rules('.a { font: 14px/16px var(--font); }'), []);
});

test('size : multiples de 14 px seulement', () => {
  for (const ok of ['14px', '28px', '56px', '112px', 'inherit', '1em', 'var(--x)']) assert.deepEqual(rules(`.a { font-size: ${ok}; }`), [], ok);
  for (const bad of ['12px', '13px', '10.5px', '16px', 'small', '1.2em']) assert.deepEqual(rules(`.a { font-size: ${bad}; }`), ['size'], bad);
  assert.deepEqual(rules('.a { font: 14px/13px var(--font-log); }'), []);
  assert.deepEqual(rules('.a { font: 12px/16px sans-serif; }'), ['size']);
});

test('blur : ombres dures seulement', () => {
  assert.deepEqual(rules('.a { box-shadow: 4px 5px 0 rgba(0,0,0,.5); }'), []);
  assert.deepEqual(rules('.a { box-shadow: inset 1px 1px 0 #666, inset 2px 2px 0 #444; }'), []);
  assert.deepEqual(rules('.a { box-shadow: 0 4px 12px rgba(0,0,0,.4); }'), ['blur']);
  assert.deepEqual(rules('.a { text-shadow: 0 1px 2px #000; }'), ['blur']);
  assert.deepEqual(rules('.a { backdrop-filter: blur(8px); }'), ['blur']);
  assert.deepEqual(rules('.a { filter: brightness(1.35); }'), []);
});

test('gradient : les dégradés doux hors définition de jeton sont des écarts, pas les motifs répétés', () => {
  assert.deepEqual(rules('.a { background: linear-gradient(#000, #333); }').includes('gradient'), true);
  assert.deepEqual(rules('  --bar: linear-gradient(var(--bar-top), var(--bar-bot));'), []);
  assert.deepEqual(rules('.a { background: repeating-linear-gradient(135deg, #fff 0 2px, #333 2px 5px); }'), []);
  assert.deepEqual(rules('.a { background: radial-gradient(circle, #fff, #000); }').includes('gradient'), true);
});

test('couleurs : jetons et gris neutres permis, gris teintés et couleurs inconnues signalés', () => {
  assert.deepEqual(rules('.a { color: #00ff00; }'), []);            // jeton (vert)
  assert.deepEqual(rules('.a { color: #fff; background: #000; }'), []);
  assert.deepEqual(rules('.a { background: #1c1c1c; }'), []);       // gris neutre
  assert.deepEqual(rules('.a { color: #a7afb2; }'), ['gray-tint']);  // gris bleuté d'AudioLinker
  assert.deepEqual(rules('.a { color: #353038; }'), ['gray-tint']);  // gris violacé
  assert.deepEqual(rules('.a { color: #2a5ae0; }'), ['color']);      // bleu vif hors jetons
  assert.deepEqual(rules('.a { color: #bbc; }'), ['gray-tint']);
});

test('lignes embarquées en base64 et commentaires ignorés', () => {
  assert.deepEqual(rules(`src: url(data:font/woff2;base64,${'A'.repeat(500)}) format('woff2'); border-radius: 9px;`), []);
  assert.deepEqual(rules('/* border-radius: 9px; font-weight: 700; */'), []);
});

test('numéros de ligne', () => {
  const v = lintText('.a { color: #fff; }\n.b { border-radius: 4px; }\n', { file: 'x.css', palette });
  assert.equal(v.length, 1); assert.equal(v[0].line, 2); assert.equal(v[0].file, 'x.css');
});

test('exceptions justifiées', () => {
  const allow = parseAllow('# commentaire\nradius\tkdx-ui.css\t.orb\tvoyant rond de la charte\n*\tvendor/\t\ttiers\n');
  const v1 = { rule: 'radius', file: 'a/kdx-ui.css', text: '.orb { border-radius: 50%; }' };
  const v2 = { rule: 'radius', file: 'a/kdx-ui.css', text: '.btn { border-radius: 4px; }' };
  const v3 = { rule: 'size', file: 'vendor/x.css', text: 'font-size: 11px' };
  assert.equal(allowedBy(v1, allow).reason, 'voyant rond de la charte');
  assert.equal(allowedBy(v2, allow), undefined);
  assert.ok(allowedBy(v3, allow));
});
