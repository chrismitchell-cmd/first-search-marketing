"""Featured images for posts, 1600 x 900 (the Resources card shape), one shared brand look:
purple background with the light-blue glow and faint diagonals, headline left in Poppins, art right, white logo
bottom left, gradient stripe along the bottom.
Usage: python3 featured_images.py OUT_DIR FONT_DIR"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import sys, os
A = '/home/user/first-search-marketing/assets/img/'
OUT, F = sys.argv[1], sys.argv[2].rstrip('/') + '/'
W, H, S = 1600, 900, 2
w, h = W * S, H * S
NAVY = (37, 7, 98); AQUA = (114, 204, 216); SKY = (50, 153, 213); ROYAL = (23, 79, 162); WHITE = (255, 255, 255)

def font(name, size): return ImageFont.truetype(F + f'Poppins-{name}.ttf', size * S)
INTER = lambda size: ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Bold.otf', size * S)
def hgrad(size, stops):
    gw, gh = size; g = Image.new('RGB', (gw, 1)); px = g.load()
    for x in range(gw):
        t = x / max(1, gw - 1)
        for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
            if p0 <= t <= p1:
                k = (t - p0) / (p1 - p0 or 1); px[x, 0] = tuple(round(a + (b - a) * k) for a, b in zip(c0, c1)); break
    return g.resize((gw, gh))
GRAD = [(0, AQUA), (1, ROYAL)]
TEXTGRAD = [(0, AQUA), (.45, SKY), (1, (88, 140, 230))]
def glow(img, cx, cy, r, color, alpha):
    m = Image.new('L', img.size, 0); ImageDraw.Draw(m).ellipse([cx - r, cy - r, cx + r, cy + r], fill=alpha)
    img.paste(Image.new('RGB', img.size, color), (0, 0), m.filter(ImageFilter.GaussianBlur(r * .45)))
def rounded_mask(size, r):
    m = Image.new('L', size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], r, fill=255); return m
def shadow(img, box, r, blur=30, alpha=120, dy=18):
    m = Image.new('L', img.size, 0); x0, y0, x1, y1 = box
    ImageDraw.Draw(m).rounded_rectangle([x0, y0 + dy * S, x1, y1 + dy * S], r, fill=alpha)
    img.paste(Image.new('RGB', img.size, (10, 2, 35)), (0, 0), m.filter(ImageFilter.GaussianBlur(blur * S)))

# One background per post category, so a card's type reads at a glance on the Resources grid.
# base colour, top-right glow, bottom-left glow, centre-right glow
THEMES = {
    'case':    ((37, 7, 98),   (110, 60, 200), AQUA, (70, 20, 150)),  # brand purple
    'blog':    ((10, 38, 112), SKY,  AQUA, (40, 110, 200)),   # deep royal blue
    'video':   ((4, 58, 78),   AQUA, SKY,  (20, 120, 140)),   # deep teal
    'podcast': ((10, 14, 30),  (60, 90, 140), AQUA, (30, 50, 90)),  # midnight charcoal
}
def base(theme='case'):
    c, g1, g2, g3 = THEMES[theme]
    bg = Image.new('RGB', (w, h), c)
    glow(bg, int(w * .98), int(h * .08), 780 * S, g1, 150); glow(bg, int(w * .02), int(h * 1.05), 620 * S, g2, 70); glow(bg, int(w * .78), int(h * .62), 520 * S, g3, 120)
    lines = Image.new('L', (w, h), 0); d = ImageDraw.Draw(lines)
    for x in range(-h, w, 260 * S): d.line([(x, h), (x + h, 0)], fill=22, width=2 * S); d.line([(x, 0), (x + h, h)], fill=14, width=2 * S)
    bg.paste(Image.new('RGB', (w, h), WHITE), (0, 0), lines)
    return bg
def finish(bg, name):
    logo = Image.open(A + 'logo-white.png').convert('RGBA'); lw = 220 * S
    logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
    bg.paste(logo, (90 * S, h - logo.height - 56 * S), logo)
    bg.paste(hgrad((w, 10 * S), GRAD), (0, h - 10 * S))
    bg.resize((W, H), Image.LANCZOS).save(os.path.join(OUT, name), quality=90); print('saved', name)

def chip(bg, x, y, label):
    """Gradient pill with spaced capitals."""
    d = ImageDraw.Draw(bg); f = INTER(22); sp = 6 * S
    tw = sum(d.textlength(c, font=f) + sp for c in label) - sp
    m = rounded_mask((int(tw + 44 * S), 50 * S), 25 * S); bg.paste(hgrad(m.size, GRAD), (x, y), m)
    cx = x + 22 * S
    for c in label: d.text((cx, y + 11 * S), c, font=f, fill=WHITE); cx += d.textlength(c, font=f) + sp
    return y + 50 * S
def headline(bg, x, y, white_lines, grad_lines, size=78, lh=88):
    d = ImageDraw.Draw(bg); f = font('ExtraBold', size)
    for line in white_lines: d.text((x, y), line, font=f, fill=WHITE); y += lh * S
    for line in grad_lines:
        m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).text((x, y), line, font=f, fill=255)
        bb = m.getbbox(); full = Image.new('RGB', (w, h)); full.paste(hgrad((bb[2] - x + 10, bb[3] - y + 30 * S), TEXTGRAD), (x, y)); bg.paste(full, (0, 0), m); y += lh * S
    return y
def rule(bg, x, y):
    ImageDraw.Draw(bg).rounded_rectangle([x, y, x + 120 * S, y + 6 * S], 3 * S, fill=AQUA); return y + 6 * S
def pills(bg, x, y, items, logo=False):
    """White pills: stage logos (firstX) or plain labels."""
    d = ImageDraw.Draw(bg); f = font('ExtraBold' if logo else 'SemiBold', 22)
    for it in items:
        if logo:
            fw = d.textlength('first', font=f); tw = fw + d.textlength(it, font=f)
        else:
            tw = d.textlength(it, font=f)
        d.rounded_rectangle([x, y, x + tw + 32 * S, y + 44 * S], 22 * S, fill=WHITE)
        if logo:
            d.text((x + 16 * S, y + 5 * S), 'first', font=f, fill=SKY); d.text((x + 16 * S + fw, y + 5 * S), it, font=f, fill=NAVY)
        else:
            d.text((x + 16 * S, y + 6 * S), it, font=f, fill=NAVY)
        x += tw + 32 * S + 10 * S

X0 = 90 * S

# ---------- 1. Case study: Progressive Dental Care ----------
def case_study():
    bg = base('case')
    # right: practice photo in a gradient frame, logo card and the 8x stat card overlapping it
    fw_, fh_ = 760 * S, 560 * S; fx, fy = w - fw_ - 70 * S, 120 * S
    shadow(bg, (fx, fy, fx + fw_, fy + fh_), 40 * S)
    frame = rounded_mask((fw_, fh_), 40 * S); bg.paste(hgrad((fw_, fh_), [(0, AQUA), (1, ROYAL)]), (fx, fy), frame)
    ph = Image.open(A + 'design/case-dental.webp').convert('RGB').crop((560, 150, 1400, 830)); pw_, phh = fw_ - 16 * S, fh_ - 16 * S   # dentist + patient, no top band or profile overlay
    sc = max(pw_ / ph.width, phh / ph.height); ph = ph.resize((round(ph.width * sc), round(ph.height * sc)), Image.LANCZOS)
    ox = int((ph.width - pw_) * .6); oy = 0; ph = ph.crop((ox, oy, ox + pw_, oy + phh))
    bg.paste(ph, (fx + 8 * S, fy + 8 * S), rounded_mask((pw_, phh), 33 * S))
    # stat card
    d = ImageDraw.Draw(bg); cw, ch = 380 * S, 200 * S; cx, cy = fx - 70 * S, fy + fh_ - 150 * S
    shadow(bg, (cx, cy, cx + cw, cy + ch), 26 * S, alpha=150)
    bg.paste(Image.new('RGB', (cw, ch), WHITE), (cx, cy), rounded_mask((cw, ch), 26 * S))
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).text((cx + 28 * S, cy + 8 * S), '8x', font=font('ExtraBold', 104), fill=255)
    bb = m.getbbox(); full = Image.new('RGB', (w, h)); full.paste(hgrad((bb[2] - bb[0] + 20, bb[3] - bb[1] + 40 * S), TEXTGRAD), (bb[0], bb[1] - 10)); bg.paste(full, (0, 0), m)
    d.text((cx + 30 * S, cy + 128 * S), 'more digital leads a month', font=font('SemiBold', 25), fill=NAVY)
    # logo card, top right of the photo
    lg = Image.open(A + 'case/progressive-dental-logo-new.webp').convert('RGB'); lw = 250 * S; lg = lg.resize((lw, round(lg.height * lw / lg.width)), Image.LANCZOS)
    lx, ly = fx + 50 * S, fy - 40 * S; pad_ = 18 * S
    shadow(bg, (lx - pad_, ly - pad_, lx + lw + pad_, ly + lg.height + pad_), 20 * S, alpha=120, dy=10)
    bg.paste(Image.new('RGB', (lw + 2 * pad_, lg.height + 2 * pad_), WHITE), (lx - pad_, ly - pad_), rounded_mask((lw + 2 * pad_, lg.height + 2 * pad_), 20 * S))
    bg.paste(lg, (lx, ly))
    # left: label, headline, rule, results
    y = chip(bg, X0, 120 * S, 'CASE STUDY') + 40 * S
    y = headline(bg, X0, y, ['Progressive', 'Dental Care'], ['From 12 to 100+', 'leads a month.'], size=72, lh=82)
    y = rule(bg, X0, y + 22 * S) + 30 * S
    pills(bg, X0, y, ['#17 to #2 in the map pack', '75 to 239 reviews'])
    finish(bg, 'featured-progressive-dental-care.webp')

# ---------- 2. Blog: Top 2027 marketing trends (the banner, at the card shape) ----------
def wheel_and_chris(bg, ws=720, ch_h=720):
    wheel = Image.open(A + 'framework-wheel.webp').convert('RGBA'); ws = ws * S; wheel = wheel.resize((ws, ws), Image.LANCZOS)
    wx, wy = w - ws + 90 * S, (h - ws) // 2 - 10 * S
    glow(bg, wx + ws // 2, wy + ws // 2, int(ws * .56), AQUA, 90); bg.paste(wheel, (wx, wy), wheel)
    chris = Image.open(A + 'design/chris-cutout.webp').convert('RGBA'); chh = ch_h * S; cw = round(chris.width * chh / chris.height)
    chris = chris.resize((cw, chh), Image.LANCZOS); cx = wx - int(cw * .02); cy = h - chh + 6 * S
    sh = Image.new('L', (w, h), 0); sh.paste(chris.split()[3].point(lambda v: v * .55), (cx - 28 * S, cy + 10 * S))
    bg.paste(Image.new('RGB', (w, h), (12, 2, 40)), (0, 0), sh.filter(ImageFilter.GaussianBlur(26 * S)))
    bg.paste(chris, (cx, cy), chris)
def blog():
    bg = base('blog'); wheel_and_chris(bg)
    y = chip(bg, X0, 120 * S, '2027 MARKETING TRENDS') + 40 * S
    y = headline(bg, X0, y, ['Top 2027', 'marketing trends'], ['to scale your', 'business.'], size=76, lh=86)
    y = rule(bg, X0, y + 20 * S) + 32 * S
    pills(bg, X0, y, ['brand', 'thought', 'choice', 'referral'], logo=True)
    finish(bg, 'featured-top-2027-marketing-trends.webp')

# ---------- 3. Video: First Search Marketing in two minutes ----------
def video():
    bg = base('video'); wheel_and_chris(bg)
    y = chip(bg, X0, 120 * S, 'VIDEO · 2 MINUTES') + 40 * S
    y = headline(bg, X0, y, ['First Search', 'Marketing'], ['in two minutes.'], size=80, lh=90)
    y = rule(bg, X0, y + 20 * S) + 32 * S
    pills(bg, X0, y, ['Agency', 'Coaching', 'Training'])
    pills(bg, X0, y + 58 * S, ['3 beliefs', '4 core values'])
    finish(bg, 'featured-first-search-in-two-minutes.webp')

# ---------- 4. Podcast: reusable episode image (edit the episode label and title, re-run) ----------
def mic(bg, cx, cy, r):
    """Simple microphone mark in a glowing disc."""
    glow(bg, cx, cy, int(r * 1.5), AQUA, 70)
    d = ImageDraw.Draw(bg); d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE)
    mw, mh = int(r * .36), int(r * .78); top = cy - int(r * .55)
    m = Image.new('L', bg.size, 0); ImageDraw.Draw(m).rounded_rectangle([cx - mw // 2, top, cx + mw // 2, top + mh], mw // 2, fill=255)
    full = Image.new('RGB', bg.size); full.paste(hgrad((mw, mh), GRAD), (cx - mw // 2, top)); bg.paste(full, (0, 0), m)
    lw = max(4, int(r * .07)); a = int(r * .34)
    d.arc([cx - a, top + mh - a - int(r * .22), cx + a, top + mh + a - int(r * .22)], 0, 180, fill=ROYAL, width=lw)
    d.line([cx, top + mh + a - int(r * .22), cx, cy + int(r * .62)], fill=ROYAL, width=lw)
    d.line([cx - int(r * .2), cy + int(r * .62), cx + int(r * .2), cy + int(r * .62)], fill=ROYAL, width=lw)
    for i, rr in enumerate((1.25, 1.5, 1.75)):
        d.arc([cx - int(r * rr), cy - int(r * rr), cx + int(r * rr), cy + int(r * rr)], -35, 35, fill=(150, 200, 240), width=lw // 2 + 2)
        d.arc([cx - int(r * rr), cy - int(r * rr), cx + int(r * rr), cy + int(r * rr)], 145, 215, fill=(150, 200, 240), width=lw // 2 + 2)
def podcast(label='PODCAST · EPISODE 01', white=['Episode title', 'goes here'], grad=['in two lines.'], name='featured-podcast-template.webp'):
    bg = base('podcast'); mic(bg, int(w * .74), int(h * .46), 190 * S)
    y = chip(bg, X0, 120 * S, label) + 40 * S
    y = headline(bg, X0, y, white, grad, size=76, lh=86)
    y = rule(bg, X0, y + 20 * S) + 32 * S
    pills(bg, X0, y, ['Listen now'])
    finish(bg, name)

case_study(); blog(); video(); podcast()
