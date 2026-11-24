// Builds the print files for the 6 x 4 in referral / loyalty card.
//   node build.js
// Outputs (next to this file):
//   program-card-print.pdf      2 pages, 6.25 x 4.25 in each (0.125 in bleed), front then back
//   proof-front.png, proof-back.png   trimmed to 6 x 4 in at 300 dpi, for review
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const url = 'file://' + path.join(__dirname, 'index.html');
  const p = await b.newPage({ viewport: { width: 700, height: 1000 } });
  await p.goto(url); await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: path.join(__dirname, 'program-card-print.pdf'), width: '6.25in', height: '4.25in', printBackground: true, preferCSSPageSize: true });
  // proofs: 96 css px per inch, scaled to 300 dpi, cropped to the trim (bleed removed)
  const s = 300 / 96, q = await b.newPage({ viewport: { width: 700, height: 1000 }, deviceScaleFactor: s });
  await q.goto(url); await q.evaluate(() => document.fonts.ready);
  await q.addStyleTag({ content: 'body{display:block!important;padding:0!important;background:#fff}' });
  for (const [i, name] of [[0, 'front'], [1, 'back']]) {
    const box = await (await q.$$('.side'))[i].boundingBox(), bl = 12;   // 0.125 in = 12 css px
    await q.screenshot({ path: path.join(__dirname, `proof-${name}.png`), clip: { x: box.x + bl, y: box.y + bl, width: box.width - 2 * bl, height: box.height - 2 * bl } });
  }
  await b.close(); console.log('built');
})();
