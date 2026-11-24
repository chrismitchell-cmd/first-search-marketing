// Builds the print files for the 6 x 4 in referral / loyalty card.
//   node build.js        (needs Python 3 with Pillow and img2pdf: pip install img2pdf)
// Outputs (next to this file):
//   program-card-print.pdf             2 pages, 6.25 x 4.25 in each (0.125 in bleed), front then back.
//                                      Each page is one 600 dpi image, so gradients, shadows and see-through
//                                      boxes print exactly as designed in any viewer or print software.
//   proof-front.png, proof-back.png    trimmed to 6 x 4 in at 300 dpi, for review
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const path = require('path');
const out = (f) => path.join(__dirname, f);
async function shoot(b, dpi, trim, names) {
  const p = await b.newPage({ viewport: { width: 700, height: 1000 }, deviceScaleFactor: dpi / 96 });
  await p.goto('file://' + out('index.html')); await p.evaluate(() => document.fonts.ready);
  await p.addStyleTag({ content: 'body{display:block!important;padding:0!important;background:#fff}' });
  const sides = await p.$$('.side'), bl = trim ? 12 : 0;   // 0.125 in = 12 css px
  for (let i = 0; i < names.length; i++) {
    const box = await sides[i].boundingBox();
    await p.screenshot({ path: out(names[i]), clip: { x: box.x + bl, y: box.y + bl, width: box.width - 2 * bl, height: box.height - 2 * bl } });
  }
  await p.close();
}
(async () => {
  const b = await chromium.launch();
  await shoot(b, 600, false, ['.print-front.png', '.print-back.png']);   // full bleed, 3750 x 2550 px
  await shoot(b, 300, true, ['proof-front.png', 'proof-back.png']);
  await b.close();
  execFileSync('python3', ['-c', `
import img2pdf, os
from PIL import Image
d = ${JSON.stringify(__dirname)}
pages = []
for n in ('front', 'back'):
    src = os.path.join(d, '.print-%s.png' % n); jpg = os.path.join(d, '.print-%s.jpg' % n)
    Image.open(src).convert('RGB').save(jpg, quality=95, subsampling=0, dpi=(600, 600)); os.remove(src); pages.append(jpg)
size = (img2pdf.in_to_pt(6.25), img2pdf.in_to_pt(4.25))
open(os.path.join(d, 'program-card-print.pdf'), 'wb').write(img2pdf.convert(pages, layout_fun=img2pdf.get_layout_fun(size)))
for f in pages: os.remove(f)
`]);
  console.log('built');
})();
