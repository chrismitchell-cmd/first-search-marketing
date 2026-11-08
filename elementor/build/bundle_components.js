// Bundle interactive components from the approved HTML into self-contained HTML-widget code for Elementor:
// markup (as rendered by the design, before its animation script runs), every CSS rule it uses (scoped to a
// wrapper class), the SVG icons it references, and its script. Output: data/components/<name>.json {html, css, js}
// Usage: NODE_PATH=... node bundle_components.js
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const ROOT = '/home/user/first-search-marketing/';
const OUT = path.join(__dirname, 'data', 'components');
fs.mkdirSync(OUT, { recursive: true });
const CDN = 'https://cdn.jsdelivr.net/gh/chrismitchell-cmd/first-search-marketing@4d59b7976a0bacac8601ce9d2eba36ebb43a7779/elementor/upload/first-search/';
const CDN2 = 'https://cdn.jsdelivr.net/gh/chrismitchell-cmd/first-search-marketing@f978e9f0c6a066562155908c1524a093df652243/elementor/upload/first-search/';
const LINKS = { 'contact.html': '/contact-us/', 'about.html': '/about-us/', 'why-choose-us.html': '/why-choose-us/', 'services-overview.html': '/services/',
  'events-resources.html': '/events/', 'ways-to-learn.html': '/befirst-training/', 'pillars.html': '/firstbrand/', 'services.html': '/services/', 'rebrand-homepage.html': '/' };

// Components: name, page, root selector, JS segment markers in the page's main script (start comment, end comment)
const COMPONENTS = [
  { name: 'hero-phone', page: 'rebrand-homepage.html', root: '.hero .phone', js: ['/* 1. Hero demo', '/* 4. Framework wheel'] },
  { name: 'framework', page: 'rebrand-homepage.html', root: 'section.framework', js: ['/* 4. Framework wheel', '/* 5. Guarantee popup'] },
  // "Three ways": tabs (click + arrow keys), partner-spots bar, video placeholders - from the design's shared script
  { name: 'ways', page: 'rebrand-homepage.html', root: 'section.ways2', jsCustom: [
    "$$('.wt-tabs').forEach(tl => {",
    "  const tabs = [...tl.querySelectorAll('[role=\"tab\"]')];",
    "  const sel = (t, focus) => { tabs.forEach(x => { const on = x === t; x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1;",
    "    const pnl = ROOT.querySelector('#' + x.getAttribute('aria-controls')); if (pnl) pnl.hidden = !on; }); if (focus) t.focus(); };",
    "  tabs.forEach((t, i) => { t.addEventListener('click', () => sel(t));",
    "    t.addEventListener('keydown', e => { const d = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key]; if (d) { e.preventDefault(); sel(tabs[(i + d + tabs.length) % tabs.length], true); } }); });",
    "});",
    "$$('.spots-bar[data-filled]').forEach(b => { if (!b.children.length) b.innerHTML = Array.from({ length: 25 }, (_, i) => '<span' + (i < +b.dataset.filled ? ' class=\"on\"' : '') + '></span>').join(''); });",
    "ROOT.addEventListener('click', e => { const v = e.target.closest('.vid-btn'); if (v) v.classList.toggle('is-playing'); });",
  ].join('\n') },
];

// Framework: write all four stage panels into the markup (readable by search engines without JS);
// the script then only switches which panel is visible.
function staticStages(html, css, js) {
  const a = js.indexOf('const PILLARS = ['), b = js.indexOf('];', a) + 2;
  const PILLARS = Function('return ' + js.slice(a + 'const PILLARS = '.length, b - 1))();
  const panel = (p, i) => `<div class="fw-stage" data-i="${i}"${i ? ' hidden' : ''}>
<div class="ptag-logo"><span class="plogo" role="img" aria-label="First${p.name}"><b>first</b>${p.name.toLowerCase()}</span></div>
<h3>${p.outcome}</h3>
<p class="fw-desc">${p.desc}</p>
<p class="inc-label">What's included</p>
<ul class="checks">${p.inc.map(x => `<li><svg class="icon" aria-hidden="true"><use href="#i-check"/></svg>${x}</li>`).join('')}</ul>
<p class="quizbox"><b>${p.quiz}</b> <a href="#" data-ph-link="Framework Quiz">Find out in the quiz.</a></p>
<a class="svc-link" href="/first${p.name.toLowerCase()}/">${p.link}</a>
</div>`;
  const slot = '<div class="fw-content" id="fw-content"></div>';
  if (!html.includes(slot)) throw new Error('framework: content slot not found');
  html = html.replace(slot, `<div class="fw-content" id="fw-content">${PILLARS.map(panel).join('\n')}</div>`);
  const h0 = js.indexOf('  const html = p => `'), h1 = js.indexOf('`;', h0) + 2;
  if (h0 < 0 || !js.includes('content.innerHTML = html(PILLARS[i])')) throw new Error('framework: script markers not found');
  js = js.slice(0, a) + js.slice(b, h0)
    + "  const stages = [...content.querySelectorAll('.fw-stage')];\n  const swap = i => stages.forEach((s, k) => { s.hidden = k !== i; });"
    + js.slice(h1);
  js = js.split('content.innerHTML = html(PILLARS[i])').join('swap(i)');
  css += '\n.fsx-framework .fw-stage[hidden]{display:none !important;}';
  return { html, css, js };
}

function mainScript(src) {
  const a = src.indexOf("<script>\n(() => {\n  'use strict';");
  const b = src.indexOf('</script>', a);
  return { a, b: b + 9, text: src.slice(a, b + 9) };
}

(async () => {
  const b = await chromium.launch();
  for (const C of COMPONENTS) {
    const src = fs.readFileSync(ROOT + C.page, 'utf8');
    const ms = mainScript(src);
    const jsSeg = C.jsCustom || ms.text.slice(ms.text.indexOf(C.js[0]), ms.text.indexOf(C.js[1]));
    // page copy without the main script: shared theme script still runs (gradient icons, brand icons, headings)
    const tmp = ROOT + '.__bundle_tmp.html';
    fs.writeFileSync(tmp, src.slice(0, ms.a) + src.slice(ms.b));
    const p = await b.newPage({ viewport: { width: 1440, height: 1000 } });
    await p.goto('file://' + tmp); await p.waitForTimeout(800);
    const res = await p.evaluate(({ rootSel, name, jsSeg }) => {
      const root = document.querySelector(rootSel);
      const inRoot = el => el === root || root.contains(el);
      // class / id / tag universe: the component, plus anything its script mentions
      const classes = new Set(), ids = new Set(), tags = new Set();
      [root, ...root.querySelectorAll('*')].forEach(e => { (e.getAttribute('class') || '').split(/\s+/).filter(Boolean).forEach(c => classes.add(c)); if (e.id) ids.add(e.id); tags.add(e.tagName.toLowerCase()); });
      (jsSeg.match(/class="([^"]+)"/g) || []).forEach(m => m.slice(7, -1).split(/\s+/).forEach(c => classes.add(c)));
      (jsSeg.match(/classList\.(?:add|remove|toggle)\('([\w-]+)'/g) || []).forEach(m => classes.add(m.match(/'([\w-]+)'/)[1]));
      (jsSeg.match(/<(\w+)[\s>]/g) || []).forEach(m => tags.add(m.slice(1, -1).toLowerCase()));
      ['is-in', 'is-on', 'on', 'is-fading', 'pop', 'pulse', 'ok', 'is-open'].forEach(c => classes.add(c));
      const W = '.fsx-' + name;
      const isOutsideAncestor = compound => {
        let ok = false;
        try {
          const ms = [...document.querySelectorAll(compound)];
          if (!ms.length) return false;
          ok = ms.every(m => !inRoot(m) && m.contains(root));
        } catch (e) { return false; }
        return ok;
      };
      const relevant = part => {
        const p = part.replace(/::?[\w-]+(\([^)]*\))?/g, m => m.startsWith(':not') ? '' : '');
        const cls = (part.match(/\.([\w-]+)/g) || []).map(c => c.slice(1));
        const idl = (part.match(/#([\w-]+)/g) || []).map(c => c.slice(1));
        if (/^\s*(:root|html|body)\b/.test(part) && !cls.length) return 'root';
        if (part.trim() === '*' || /^\s*\*(::?[\w-]+)?\s*(,|$)/.test(part)) return 'all';
        if (cls.some(c => !classes.has(c) && !ancestorClass(c))) return false;
        if (idl.some(i => !ids.has(i))) return false;
        if (!cls.length && !idl.length) {
          const t = (p.trim().split(/[\s>+~]+/).pop() || '').replace(/\[.*$/, '').toLowerCase();
          return tags.has(t) ? 'tag' : false;
        }
        try { const q = part.replace(/::?(before|after|placeholder|selection|marker|-webkit-[\w-]+)/g, '').replace(/:(hover|focus|focus-visible|focus-within|active|visited|disabled|checked)/g, ''); if (q.trim() && !document.querySelector(q) && !cls.every(c => classes.has(c) || ancestorClass(c))) return false; } catch (e) {}
        return true;
      };
      function ancestorClass(c) { let e = root.parentElement; while (e) { if (e.classList && e.classList.contains(c)) return true; e = e.parentElement; } return false; }
      const scope = part => {
        let s = part.trim();
        if (/^(:root|html|body)\b/.test(s)) return s.replace(/^(:root|html|body)/, W);
        // drop leading compounds that only match ancestors outside the component (e.g. ".hero" for ".hero .phone")
        const toks = s.split(/(\s*[>+~]\s*|\s+)/);
        while (toks.length > 2) {
          const c = toks[0].replace(/::?[\w-]+(\([^)]*\))?/g, '');
          if (c && isOutsideAncestor(c)) toks.splice(0, 2); else break;
        }
        s = toks.join('');
        return W + ' ' + s;
      };
      // Rebuild a rule's declarations. The browser serialises shorthands that use var() (e.g. "background: var(--grad)")
      // as empty longhands, so take the shorthand's own value whenever a longhand comes back empty.
      const SH = ['background', 'border-radius', 'border-top', 'border-right', 'border-bottom', 'border-left', 'border-color', 'border-width', 'border-style', 'border',
        'margin', 'padding', 'inset', 'font', 'flex', 'grid-template', 'grid-area', 'grid', 'gap', 'transition', 'animation', 'text-decoration', 'outline',
        'list-style', 'overflow', 'place-items', 'place-content', 'columns', 'mask', 'border-image'];
      const belongs = (sh, n) => sh === 'border-radius' ? n.endsWith('-radius') : sh === 'inset' ? ['top', 'right', 'bottom', 'left'].includes(n)
        : sh === 'gap' ? ['row-gap', 'column-gap'].includes(n) : sh === 'font' ? (n.startsWith('font') || n === 'line-height')
        : sh === 'place-items' ? ['align-items', 'justify-items'].includes(n) : sh === 'place-content' ? ['align-content', 'justify-content'].includes(n)
        : sh === 'border' ? (n.startsWith('border-') && !n.endsWith('-radius')) : n === sh || n.startsWith(sh + '-');
      const declText = st => {
        const out = [], done = new Set();
        for (const n of st) {
          const v = st.getPropertyValue(n), imp = st.getPropertyPriority(n) ? ' !important' : '';
          if (v !== '') { out.push(`${n}: ${v}${imp}`); continue; }
          const sh = SH.find(x => belongs(x, n) && st.getPropertyValue(x) !== '');
          if (sh && !done.has(sh)) { done.add(sh); out.push(`${sh}: ${st.getPropertyValue(sh)}${st.getPropertyPriority(sh) ? ' !important' : ''}`); }
        }
        return out.join('; ') + ';';
      };
      // Read the design's own CSS text (not the browser's re-serialised version, which drops var() shorthands)
      const parseCSS = css => {
        css = css.replace(/\/\*[\s\S]*?\*\//g, '');
        const rules = [], frames = []; let i = 0;
        const skipBlock = () => { let d = 1, j = i; while (d && j < css.length) { if (css[j] === '{') d++; else if (css[j] === '}') d--; j++; } const t = css.slice(i, j - 1); i = j; return t; };
        const block = at => {
          while (i < css.length) {
            const open = css.indexOf('{', i), close = css.indexOf('}', i);
            if (close !== -1 && (open === -1 || close < open)) { i = close + 1; return; }
            if (open === -1) { i = css.length; return; }
            const head = css.slice(i, open).trim(); i = open + 1;
            if (/^@(media|supports|container)\b/.test(head)) block(head);
            else if (/^@(-webkit-)?keyframes\b/.test(head)) frames.push({ name: head.split(/\s+/)[1], text: head + ' {' + skipBlock() + '}' });
            else if (head.startsWith('@')) skipBlock();
            else { const end = css.indexOf('}', i); rules.push({ at, sel: head, body: css.slice(i, end).trim() }); i = end + 1; }
          }
        };
        block(null);
        return { rules, frames };
      };
      const out = [], frames = new Set(), allFrames = [];
      for (const st of document.querySelectorAll('style')) {
        const { rules, frames: kfs } = parseCSS(st.textContent);
        allFrames.push(...kfs);
        for (const r of rules) {
          const parts = r.sel.split(/,(?![^(]*\))/);
          const kept = parts.filter(x => { try { return relevant(x); } catch (e) { return false; } });
          if (!kept.length) continue;
          let body = r.body.trim(); if (body && !body.endsWith(';')) body += ';';
          (body.match(/animation(?:-name)?:\s*([\w-]+)/g) || []).forEach(m => frames.add(m.split(':')[1].trim().split(/\s/)[0]));
          const rule = kept.map(scope).join(', ') + ' { ' + body + ' }';
          out.push(r.at ? `${r.at} { ${rule} }` : rule);
        }
      }
      const kf = allFrames.filter(k => frames.has(k.name)).map(k => k.text);
      // custom properties + base text styles from :root / body
      const vars = []; for (const sh of document.styleSheets) { let rs; try { rs = sh.cssRules; } catch (e) { continue; } for (const r of rs) if (r.type === 1 && /(^|,)\s*:root\s*(,|$)/.test(r.selectorText)) for (const n of r.style) if (n.startsWith('--')) vars.push(`${n}: ${r.style.getPropertyValue(n).trim()};`); }
      const bcs = getComputedStyle(document.body);
      // icons used (incl. gradient twins) + gradient defs
      const uses = new Set(); root.querySelectorAll('use').forEach(u => uses.add((u.getAttribute('href') || '').slice(1)));
      (jsSeg.match(/#([\w-]+)"/g) || []).forEach(m => uses.add(m.slice(1, -1)));
      [...uses].forEach(u => uses.add(u.replace(/--g$/, '') + '--g'));
      const sym = [...uses].map(u => document.getElementById(u)).filter(e => e && e.tagName.toLowerCase() === 'symbol').map(e => e.outerHTML).join('');
      const grads = [...document.querySelectorAll('svg defs linearGradient, svg defs radialGradient, svg > linearGradient')].map(e => e.outerHTML).join('');
      const sprite = `<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>${grads}</defs>${sym}</svg>`;
      return { html: root.outerHTML, css: out.join('\n'), kf: kf.join('\n'), vars: vars.join(' '), sprite,
        base: `font-family:${bcs.fontFamily};font-size:${bcs.fontSize};line-height:${bcs.lineHeight};color:${bcs.color};` };
    }, { rootSel: C.root, name: C.name, jsSeg });
    await p.close(); fs.unlinkSync(tmp);
    // post-process: rename the design's "e-con" class (Elementor uses it), absolute asset URLs, real page links
    let html = res.html.replace(/\be-con\b/g, 'fsx-con').replace(/(src|href)="assets\/img\/([^"]+)"/g, (m, a, f) => `${a}="${f === 'framework-wheel.webp' ? CDN2 : CDN}${f}"`)
      .replace(/href="([\w-]+\.html)(\?[^"#]*)?(#[^"]*)?"/g, (m, f, q, h) => `href="${(LINKS[f] || '/') + (h || '')}"`);
    let css = res.css.replace(/\be-con\b/g, 'fsx-con').replace(/url\(["']?(?:\.\.\/)?assets\/img\/([^"')]+)["']?\)/g, (m, f) => `url("${CDN}${f}")`);
    const W = '.fsx-' + C.name;
    const reset = `${W}{${res.vars} ${res.base} display:block;} ${W} *, ${W} *::before, ${W} *::after{box-sizing:border-box;}
${W} button{background:none;border:0;padding:0;margin:0;font:inherit;color:inherit;border-radius:0;text-transform:none;letter-spacing:inherit;box-shadow:none;cursor:pointer;}
${W} button:hover, ${W} button:focus{background:none;color:inherit;}
${W} a{color:inherit;text-decoration:none;background:none;} ${W} a:hover{color:inherit;}
${W} h1, ${W} h2, ${W} h3, ${W} h4, ${W} p, ${W} ul, ${W} ol, ${W} figure{margin:0;padding:0;} ${W} ul, ${W} ol{list-style:none;}
${W} img, ${W} svg{display:block;max-width:100%;height:auto;}`;
    css = reset + '\n' + css + '\n' + res.kf;
    // the design page's body background must not paint the widget (it shows as a box around the phone)
    css += `\n${W}{background:transparent !important;}`;
    let js = jsSeg.replace(/assets\/img\/([\w\/.-]+)/g, (m, f) => CDN + f).replace(/(['"`])([\w-]+\.html)(\?[^'"`]*)?\1/g, (m, q, f) => `${q}${LINKS[f] || '/'}${q}`)
      .replace(/pillars\.html\?pillar=\$\{([^}]+)\}/g, '/first${$1}/');
    if (C.name === 'framework') ({ html, css, js } = staticStages(html, css, js));
    fs.writeFileSync(path.join(OUT, C.name + '.json'), JSON.stringify({ html: res.sprite + html, css, js }, null, 1));
    console.log(C.name, 'html', html.length, 'css', css.length, 'js', js.length);
  }
  await b.close();
})();
