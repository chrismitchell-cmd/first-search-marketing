// Split site-settings.css into a small global stylesheet (Site Settings > Custom CSS) and per-template CSS.
// A selector goes global when every custom class it names (fs-*, sn-*, fsx-*) is used by the header or
// footer, or by at least SHARED templates; otherwise it is copied into each template that uses all its classes,
// on the template's first container (Advanced > Custom CSS), so Elementor writes it to that page's own CSS file.
// Elementor loads the kit (Site Settings) CSS before page and theme-template CSS, so moved rules still come after
// the global ones exactly as they did in the single file; checked by comparing computed styles of every element.
// Selectors whose classes no template uses are dropped. Source order is kept within each output.
// Usage: node split_css.js            -> writes ../global.css and patches ../templates/**/*.json
//        node split_css.js --dry      -> sizes only
// Needs: npm install (postcss, cssnano) in this folder.
const fs = require('fs'), path = require('path'), zlib = require('zlib');
const postcss = require('postcss'), cssnano = require('cssnano');

const ROOT = path.join(__dirname, '..');
const T = path.join(ROOT, 'templates');
const SHARED = 18;          // used by this many of the page templates -> global
const DRY = process.argv.includes('--dry');
const sp = require('postcss-selector-parser');
const CUSTOM = /^(fs|sn|fsx)-/;
// Alternatives of custom classes a selector needs: :is()/:where()/:has() lists are either-or, :not() needs nothing.
function alts(sel) {
  const prod = (A, B) => A.flatMap(a => B.map(b => new Set([...a, ...b])));
  const seq = nodes => nodes.reduce((acc, n) => {
    if (n.type === 'class') return CUSTOM.test(n.value) ? prod(acc, [new Set([n.value])]) : acc;
    if (n.type === 'pseudo' && /^:(is|where|has|matches|-webkit-any)$/.test(n.value)) return prod(acc, n.nodes.flatMap(x => seq(x.nodes)));
    return acc;   // :not(), elements, attributes, combinators
  }, [new Set()]);
  let out; sp(root => { out = seq(root.nodes[0].nodes); }).processSync(sel); return out;
}

const walk = d => fs.readdirSync(d, { withFileTypes: true }).flatMap(e =>
  e.isDirectory() ? walk(path.join(d, e.name)) : e.name.endsWith('.json') ? [path.join(d, e.name)] : []);
const files = walk(T).sort();
const isHF = f => /\/(header|footer)\.json$/.test(f);
// strip any CSS this script added before, so a re-run starts clean
const load = f => { const j = JSON.parse(fs.readFileSync(f, 'utf8')); if (j.content[0].settings) delete j.content[0].settings.custom_css; return j; };
const tpl = Object.fromEntries(files.map(f => [f, load(f)]));
const tokens = Object.fromEntries(files.map(f => [f, new Set(JSON.stringify(tpl[f]).match(/[A-Za-z0-9_-]+/g))]));
const pages = files.filter(f => !isHF(f));

const count = {};
for (const f of pages) for (const t of tokens[f]) if (/^(fs|sn|fsx)-/.test(t)) count[t] = (count[t] || 0) + 1;
const global = new Set(files.filter(isHF).flatMap(f => [...tokens[f]]));
for (const [c, n] of Object.entries(count)) if (n >= SHARED) global.add(c);

const src = postcss.parse(fs.readFileSync(path.join(ROOT, 'site-settings.css'), 'utf8'));
const out = { global: postcss.root() };
for (const f of pages) out[f] = postcss.root();

// copy node (rule or keyframes) into dst under the same chain of at-rules, reusing the last block when it matches
function place(dst, chain, node) {
  let parent = dst;
  for (const a of chain) {
    const last = parent.last;
    if (last && last.type === 'atrule' && last.name === a.name && last.params === a.params) parent = last;
    else { const n = postcss.atRule({ name: a.name, params: a.params }); parent.append(n); parent = n; }
  }
  parent.append(node);
}
function visit(node, chain) {
  if (node.type === 'comment') return;
  if (node.type === 'atrule' && /keyframes|font-face/.test(node.name)) return place(out.global, chain, node.clone());
  if (node.type === 'atrule' && node.nodes) return node.each(n => visit(n, [...chain, node]));
  if (node.type === 'atrule') return place(out.global, chain, node.clone());   // @import etc.
  if (node.type !== 'rule') return;
  const g = [], per = new Map();
  for (const sel of node.selectors) {
    const A = alts(sel);
    if (A.some(set => [...set].every(c => global.has(c)))) { g.push(sel); continue; }
    for (const f of pages) if (A.some(set => [...set].every(c => tokens[f].has(c)))) { if (!per.has(f)) per.set(f, []); per.get(f).push(sel); }
  }
  if (g.length) place(out.global, chain, node.clone({ selectors: g }));
  for (const [f, sels] of per) place(out[f], chain, node.clone({ selectors: sels }));
}
src.each(n => visit(n, []));

const minify = async root => (await postcss([cssnano({ preset: ['default', { mergeRules: false }] })]).process(root.toString(), { from: undefined })).css;
const kb = n => (n / 1024).toFixed(1) + ' KB';
(async () => {
  const g = await minify(out.global);
  console.log('global', kb(g.length), '(gzip', kb(zlib.gzipSync(g).length) + ')');
  if (!DRY) fs.writeFileSync(path.join(ROOT, 'global.css'), g + '\n');
  let max = 0;
  for (const f of pages) {
    const c = await minify(out[f]);
    if (/\bselector\b/.test(c)) throw new Error('the word "selector" would be rewritten by Elementor in ' + f);
    max = Math.max(max, g.length + c.length);
    console.log(kb(c.length).padStart(9), ' total', kb(g.length + c.length).padStart(9), ' ', path.relative(T, f));
    if (!DRY) { const j = tpl[f]; j.content[0].settings = j.content[0].settings || {}; if (c) j.content[0].settings.custom_css = c; fs.writeFileSync(f, JSON.stringify(j, null, 1)); }
  }
  console.log('largest page total', kb(max),);
})();
