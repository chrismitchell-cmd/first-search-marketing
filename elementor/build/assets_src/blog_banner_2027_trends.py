# Blog featured image, 1600 x 840: "Top 2027 marketing trends to scale your business" with Chris and the framework wheel
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import sys
A = '/home/user/first-search-marketing/assets/img/'
F = '/tmp/claude-0/-home-user-first-search-marketing/cbda635a-c308-5918-bc62-78d4657e8ad1/scratchpad/fonts/'
W, H, S = 1600, 840, 2            # draw at 2x, downscale at the end for clean edges
w, h = W * S, H * S
NAVY = (37, 7, 98); AQUA = (114, 204, 216); SKY = (50, 153, 213); ROYAL = (23, 79, 162)

def font(name, size): return ImageFont.truetype(F + f'Poppins-{name}.ttf', size * S)
def hgrad(size, stops):
    """Horizontal gradient image through colour stops [(pos 0..1, rgb)]."""
    gw, gh = size; g = Image.new('RGB', (gw, 1))
    px = g.load()
    for x in range(gw):
        t = x / max(1, gw - 1)
        for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
            if p0 <= t <= p1:
                k = (t - p0) / (p1 - p0 or 1); px[x, 0] = tuple(round(a + (b - a) * k) for a, b in zip(c0, c1)); break
    return g.resize((gw, gh))
def glow(cx, cy, r, color, alpha):
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).ellipse([cx - r, cy - r, cx + r, cy + r], fill=alpha)
    m = m.filter(ImageFilter.GaussianBlur(r * 0.45))
    return Image.new('RGB', (w, h), color), m

# background: navy with the site's light-blue splash
bg = Image.new('RGB', (w, h), NAVY)
for cx, cy, r, col, a in [(int(w * .98), int(h * .1), 760 * S, SKY, 150), (int(w * .02), int(h * 1.05), 620 * S, AQUA, 70), (int(w * .78), int(h * .62), 520 * S, ROYAL, 120)]:
    layer, m = glow(cx, cy, r, col, a); bg.paste(layer, (0, 0), m)
# faint geometric diagonals, like the site's background
lines = Image.new('L', (w, h), 0); d = ImageDraw.Draw(lines)
for x in range(-h, w, 260 * S): d.line([(x, h), (x + h, 0)], fill=22, width=2 * S); d.line([(x, 0), (x + h, h)], fill=14, width=2 * S)
bg.paste(Image.new('RGB', (w, h), (255, 255, 255)), (0, 0), lines)

# framework wheel, right, with a soft ring of light behind it
wheel = Image.open(A + 'framework-wheel.webp').convert('RGBA')
ws = 700 * S; wheel = wheel.resize((ws, ws), Image.LANCZOS)
wx, wy = w - ws + 90 * S, (h - ws) // 2 - 10 * S
layer, m = glow(wx + ws // 2, wy + ws // 2, int(ws * .56), AQUA, 90); bg.paste(layer, (0, 0), m)
bg.paste(wheel, (wx, wy), wheel)

# Chris, in front of the wheel, anchored to the bottom edge, with a soft shadow
chris = Image.open(A + 'design/chris-cutout.webp').convert('RGBA')
ch = 690 * S; cw = round(chris.width * ch / chris.height); chris = chris.resize((cw, ch), Image.LANCZOS)
cx = wx - int(cw * .02); cy = h - ch + 6 * S
sh = Image.new('L', (w, h), 0); sh.paste(chris.split()[3].point(lambda v: v * .55), (cx - 28 * S, cy + 10 * S))
bg.paste(Image.new('RGB', (w, h), (12, 2, 40)), (0, 0), sh.filter(ImageFilter.GaussianBlur(26 * S)))
bg.paste(chris, (cx, cy), chris)

# text block, left
d = ImageDraw.Draw(bg)
x0, y = 90 * S, 104 * S
# eyebrow chip
ef = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Bold.otf', 22 * S)
label = '2027 MARKETING TRENDS'; tw = d.textlength(label, font=ef) + 6 * len(label) * S
chip = Image.new('L', (int(tw + 44 * S), 50 * S), 0); ImageDraw.Draw(chip).rounded_rectangle([0, 0, chip.width - 1, chip.height - 1], 25 * S, fill=255)
bg.paste(hgrad(chip.size, [(0, AQUA), (1, ROYAL)]), (x0, y), chip)
cxp = x0 + 22 * S
for ch_ in label:
    d.text((cxp, y + 11 * S), ch_, font=ef, fill=(255, 255, 255)); cxp += d.textlength(ch_, font=ef) + 6 * S
y += 84 * S
# headline: white, then gradient
hf = font('ExtraBold', 76)
for line in ['Top 2027', 'marketing trends']:
    d.text((x0, y), line, font=hf, fill=(255, 255, 255)); y += 86 * S
for line in ['to scale your', 'business.']:
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).text((x0, y), line, font=hf, fill=255)
    bb = m.getbbox(); grad = hgrad((bb[2] - x0 + 10, bb[3] - y + 30 * S), [(0, AQUA), (.45, SKY), (1, (88, 140, 230))])
    full = Image.new('RGB', (w, h)); full.paste(grad, (x0, y)); bg.paste(full, (0, 0), m); y += 86 * S
# short aqua rule, then the four stages
y += 22 * S
d.rounded_rectangle([x0, y, x0 + 120 * S, y + 6 * S], 3 * S, fill=AQUA)
y += 34 * S
sf_b = font('ExtraBold', 22); sx = x0
for st in ['brand', 'thought', 'choice', 'referral']:
    fw = d.textlength('first', font=sf_b); tw2 = fw + d.textlength(st, font=sf_b)
    d.rounded_rectangle([sx, y, sx + tw2 + 32 * S, y + 44 * S], 22 * S, fill=(255, 255, 255))
    d.text((sx + 16 * S, y + 5 * S), 'first', font=sf_b, fill=SKY); d.text((sx + 16 * S + fw, y + 5 * S), st, font=sf_b, fill=NAVY)
    sx += tw2 + 32 * S + 10 * S

# logo, bottom left
logo = Image.open(A + 'logo-white.png').convert('RGBA'); lw = 220 * S
logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
bg.paste(logo, (x0, h - logo.height - 48 * S), logo)

# brand gradient stripe along the bottom
bg.paste(hgrad((w, 10 * S), [(0, AQUA), (1, ROYAL)]), (0, h - 10 * S))

out = bg.resize((W, H), Image.LANCZOS)
out.save(sys.argv[1], quality=90)
print('saved', out.size)
