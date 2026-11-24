"""First Search Marketing email signature: animated images + Outlook-safe HTML.

    python3 build.py [ASSET_BASE_URL]

ASSET_BASE_URL is the public address of this folder (the one holding img/) (no trailing slash), e.g. a jsDelivr link to this
repo or your WordPress Media folder. Email clients load signature images from the web, so they must be public.

Outputs:
  img/logo-animated.gif     190 x 65 shown (2x file): the pin hops and a shine sweeps the wordmark
  img/icon-*.gif            30 x 30 shown: website, Instagram, LinkedIn, Facebook, with a staggered shine
  img/verified.gif          15 x 15 shown: badge next to the name
  img/book-a-meeting.gif    102 x 30 shown: gradient button with a shine
  signature.html            the signature only (paste this)
  index.html                preview page with a "Copy signature" button and setup steps

Every GIF starts on a complete still frame, so classic Outlook for Windows (which shows only the first frame)
still shows the full design.
"""
import os, sys, html
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
FONTS = os.path.join(REPO, 'gift-box/program-card/fonts/')
IMG = os.path.join(HERE, 'img'); os.makedirs(IMG, exist_ok=True)
BASE = next((a for a in sys.argv[1:] if not a.startswith('--')), '.').rstrip('/')

# ---------------- signature details: edit these ----------------
ME = dict(
    name='Chris Mitchell',
    title='Owner & Digital Partner',
    company='First Search Marketing LLC',
    phone='(603) 518-8090', phone_link='tel:+16035188090',
    email='chris@befirstsearch.com',
    website='https://befirstsearch.com/',
    # Instagram, LinkedIn and Book a meeting: your current customesignature links (they redirect to the right pages).
    # Swap in the direct addresses when you have them, then re-run this script.
    instagram='http://track.customesignature.com/r/813005',
    linkedin='http://track.customesignature.com/r/813006',
    facebook='https://www.facebook.com/p/First-Search-Marketing-LLC-100063771473527/',
    book='http://track.customesignature.com/r/813002',
)

NAVY = (37, 7, 98); SKY = (50, 153, 213); AQUA = (114, 204, 216); ROYAL = (23, 79, 162); WHITE = (255, 255, 255)

def font(name, size): return ImageFont.truetype(FONTS + name, size)
def grad(size, c0=AQUA, c1=ROYAL, diag=True):
    w, h = size; g = Image.new('RGB', size); px = g.load()
    for y in range(h):
        for x in range(w):
            t = ((x / max(1, w - 1)) * .65 + (y / max(1, h - 1)) * .35) if diag else x / max(1, w - 1)
            px[x, y] = tuple(round(a + (b - a) * t) for a, b in zip(c0, c1))
    return g
def shine(img, mask, t, width=.22, strength=.75):
    """Diagonal white band across img where mask is set; t from 0 to 1 moves it left to right."""
    w, h = img.size; band = Image.new('L', (w, h), 0); d = ImageDraw.Draw(band)
    cx = -w * .4 + t * w * 1.8; bw = w * width
    d.polygon([(cx - bw, h), (cx, h), (cx + h * .6, 0), (cx + h * .6 - bw, 0)], fill=int(255 * strength))
    band = band.filter(ImageFilter.GaussianBlur(w * .02)); band = ImageChops.multiply(band, mask)
    out = img.copy(); out.paste(Image.new('RGB', (w, h), WHITE), (0, 0), band); return out
def save_gif(frames, durations, name):
    """frames: RGB images on white. Shared palette keeps colours steady between frames."""
    # palette from every frame, with the colour nearest white snapped to pure white (the email background)
    sheet = Image.new('RGB', (frames[0].width, frames[0].height * len(frames)))
    for k, f in enumerate(frames): sheet.paste(f, (0, k * f.height))
    pal = sheet.quantize(colors=255, method=Image.Quantize.MEDIANCUT)
    p = pal.getpalette()[:765]; cols = [tuple(p[i:i + 3]) for i in range(0, len(p), 3)]
    wi = min(range(len(cols)), key=lambda i: sum((255 - c) ** 2 for c in cols[i])); p[wi * 3:wi * 3 + 3] = [255, 255, 255]; pal.putpalette(p)
    q = []
    for f in frames:   # Pillow's palette lookup is approximate: put pure-white pixels on the white entry explicitly
        qf = f.quantize(palette=pal, dither=Image.Dither.NONE)
        qf.paste(wi, (0, 0, f.width, f.height), f.convert('L').point(lambda v: 255 if v >= 254 else 0)); q.append(qf)
    q[0].save(os.path.join(IMG, name), save_all=True, append_images=q[1:], duration=durations, loop=0, optimize=True, disposal=1)
    print('saved', name, os.path.getsize(os.path.join(IMG, name)) // 1024, 'KB')
def ease_out(t): return 1 - (1 - t) ** 3

# ---------------- animated logo panel ----------------
# The logo sits on the white box texture (bg-geometric, the brand's light section background) with the gradient
# stripe along the bottom, like the gift box lid. Four animation styles; LOGO_STYLE picks the one in the signature.
LOGO_STYLE = 'ping-reveal'  # 'hop', 'ping', 'ping-reveal', 'sweep' or 'search'
PW, PH = 210, 84            # shown size in the email (the file is 2x for sharp screens)
import math
def logo_parts():
    S = 2; W, H = PW * S, PH * S
    geo = Image.open(os.path.join(REPO, 'assets/img/design/bg-geometric.jpg')).convert('RGB')
    sc = H * 2.1 / geo.height; geo = geo.resize((round(geo.width * sc), round(geo.height * sc)), Image.LANCZOS)
    bg = geo.crop((geo.width - W - 40, 30, geo.width - 40, 30 + H))                    # the tiled part of the texture
    from PIL import ImageOps                                    # tiles in soft cool greys: shading shows, seams stay light
    g = ImageOps.autocontrast(bg.convert('L'), cutoff=2).filter(ImageFilter.GaussianBlur(.6))
    lo, hi = (226, 226, 234), (255, 255, 255)
    bg = Image.merge('RGB', [g.point(lambda v, a=a_, b=b_: int(a + (b - a) * v / 255)) for a_, b_ in zip(lo, hi)])
    fade = Image.linear_gradient('L').rotate(90).resize((W, H))                        # whiter behind the wordmark
    bg.paste(Image.new('RGB', (W, H), WHITE), (0, 0), fade.point(lambda v: int(v * .35)))
    stripe = 6
    bg.paste(grad((W, stripe), diag=False), (0, H - stripe))
    logo = Image.open(os.path.join(REPO, 'assets/img/logo.png')).convert('RGBA')
    lw = round(W * .8); logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
    pin_w = round(98 * lw / 533) + 4
    pin, word = logo.crop((0, 0, pin_w, logo.height)), logo.crop((pin_w, 0, logo.width, logo.height))
    x0 = (W - lw) // 2; y0 = (H - stripe - logo.height) // 2 + 2
    corner = Image.new('L', (W, H), 0); ImageDraw.Draw(corner).rounded_rectangle([0, 0, W - 1, H - 1], radius=16, fill=255)
    return dict(W=W, H=H, bg=bg, pin=pin, word=word, pin_w=pin_w, x0=x0, y0=y0, corner=corner, stripe=stripe)

def logo_frame(P, hop=0, squash=0., angle=0., t=None, sweep=None, rings=(), glint=0., grow=1., reveal=1., fade=1.):
    W, H = P['W'], P['H']; f = P['bg'].copy(); pin = P['pin']; x0, y0 = P['x0'], P['y0']
    tipx, tipy = x0 + P['pin_w'] * .46, y0 + pin.height - 4
    if sweep is not None:                                       # light across the tiles: brighten and warm the texture
        f = shine(f, Image.new('L', (W, H), 255), sweep, width=.3, strength=.85)
    for r, a in rings:                                          # location ping: flat rings from the pin tip
        m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
        d.ellipse([tipx - r, tipy - r * .3, tipx + r, tipy + r * .3], outline=int(255 * a), width=3)
        f.paste(Image.new('RGB', (W, H), SKY), (0, 0), m.filter(ImageFilter.GaussianBlur(.6)))
    sh = Image.new('L', (W, H), 0); r = P['pin_w'] * (.3 - hop / 260)                   # pin shadow
    ImageDraw.Draw(sh).ellipse([tipx - r, tipy - 3, tipx + r, tipy + 4], fill=int(70 - hop * 1.5))
    f.paste(Image.new('RGB', (W, H), (170, 170, 190)), (0, 0), sh.filter(ImageFilter.GaussianBlur(3)))
    p = pin
    if squash: p = pin.resize((pin.width + int(squash * 6), pin.height - int(squash * 6)), Image.LANCZOS)
    px, py = x0 - int(squash * 3), y0 - hop + int(squash * 6)
    lay = Image.new('RGBA', (W, H))                             # pin and wordmark on one layer
    if angle:                                                   # tilt around the tip
        big = Image.new('RGBA', (pin.width * 3, pin.height * 2)); big.paste(p, (pin.width, 0), p)
        big = big.rotate(angle, resample=Image.BICUBIC, center=(pin.width * 1.46, pin.height - 4))
        lay.paste(big, (px - pin.width, py), big)
    else:
        lay.paste(p, (px, py), p)
    wd = P['word']; wx, wy = x0 + P['pin_w'], y0
    if grow != 1.:                                              # grow the wordmark only, from its left edge (clear of the pin)
        cy = wy + wd.height / 2
        wd = wd.resize((round(wd.width * grow), round(wd.height * grow)), Image.LANCZOS); wy = round(cy - wd.height / 2)
    wl = Image.new('RGBA', (W, H)); wl.paste(wd, (wx, wy), wd)
    if reveal < 1. or fade < 1.:                                # wipe in from the left with a soft edge, or fade
        edge = 40; xr = wx - edge + (wd.width + 2 * edge) * reveal
        ramp = Image.new('L', (W, 1)); ramp.putdata([max(0, min(255, int(255 * (xr - x) / edge))) for x in range(W)])
        a = ImageChops.multiply(wl.split()[3], ramp.resize((W, H)))
        if fade < 1.: a = a.point(lambda v: int(v * fade))
        wl.putalpha(a)
    lay.alpha_composite(wl)
    f.paste(lay, (0, 0), lay)
    if t is not None: f = shine(f, wl.split()[3], t, width=.12, strength=.7)
    if glint:                                                   # sparkle on the magnifier lens
        gx, gy, gr = x0 + P['pin_w'] * .36, y0 + pin.height * .27, 9 * glint
        m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
        d.polygon([(gx, gy - gr * 1.6), (gx + gr * .25, gy - gr * .25), (gx + gr * 1.6, gy), (gx + gr * .25, gy + gr * .25),
                   (gx, gy + gr * 1.6), (gx - gr * .25, gy + gr * .25), (gx - gr * 1.6, gy), (gx - gr * .25, gy - gr * .25)], fill=255)
        f.paste(Image.new('RGB', (W, H), WHITE), (0, 0), m.filter(ImageFilter.GaussianBlur(.5)))
    out = Image.new('RGB', (W, H), WHITE); out.paste(f, (0, 0), P['corner'])          # rounded corners on white
    ImageDraw.Draw(out).rounded_rectangle([0, 0, W - 1, H - 1], radius=16, outline=(227, 226, 234), width=2)
    return out

def logo_gifs():
    P = logo_parts(); F = lambda **k: logo_frame(P, **k)
    still = F()
    def run(name, steps, hold=2600, tail=600):
        frames, dur = [still], [hold]                           # still first frame: classic Outlook shows only this
        for kw, ms in steps: frames.append(F(**kw)); dur.append(ms)
        frames.append(still); dur.append(tail); save_gif(frames, dur, f'logo-{name}.gif')
    # 1. hop: the pin hops and lands, then a shine crosses the wordmark
    run('hop', [(dict(hop=y), 45) for y in (6, 11, 14, 15, 14, 11, 6, 0)] + [(dict(squash=1.), 55), (dict(squash=.5), 55)]
        + [(dict(hop=y), 45) for y in (3, 5, 3, 0)] + [(dict(t=i / 13), 50) for i in range(14)])
    # 2. ping: location rings ripple out from the pin tip, then the lens sparkles
    st = []
    ring = lambda k: [(6 + (k - d) * 4.2, max(0, 1 - (k - d) / 7)) for d in (0, 3, 6) if 0 <= k - d < 8]
    for k in range(12):
        g = 1 + .07 * math.sin(math.pi * min(1, k / 10))      # the wordmark grows and settles back while the rings ripple
        st.append((dict(rings=ring(k), grow=g), 70))
    run('ping', st)
    # 2b. ping-reveal: the wordmark fades out, then wipes back in from left to right while the rings ripple
    st = [(dict(fade=v), 60) for v in (.6, .25, 0)]
    n = 22
    for k in range(n):
        st.append((dict(rings=ring(k) if k < 14 else (), reveal=ease_out(k / (n - 1))), 65))
    run('ping-reveal', st, tail=400)
    # 3. sweep: a soft light passes over the tile texture and the logo, like light across the box
    run('sweep', [(dict(sweep=i / 17), 55) for i in range(18)] + [(dict(t=i / 11), 50) for i in range(12)])
    # 4. search: the pin tilts left and right like it is scanning, then the lens sparkles
    run('search', [(dict(angle=a), 55) for a in (3, 6, 7, 6, 3, 0, -3, -6, -7, -6, -3, 0, 2, 0)]
        + [(dict(glint=g), 50) for g in (.4, .8, 1, .8, .4)])

# ---------------- social icons ----------------
def glyph(kind, n):
    """White glyph on transparent, n x n."""
    g = Image.new('L', (n, n), 0); d = ImageDraw.Draw(g); c = n / 2; lw = max(2, round(n * .075))
    if kind == 'web':
        r = n * .27; d.ellipse([c - r, c - r, c + r, c + r], outline=255, width=lw)
        d.ellipse([c - r * .45, c - r, c + r * .45, c + r], outline=255, width=lw)
        d.line([c - r, c, c + r, c], fill=255, width=lw)
        for k in (-.5, .5): yy = c + r * k; xx = r * .86; d.line([c - xx, yy, c + xx, yy], fill=255, width=max(1, lw - 1))
    elif kind == 'instagram':
        r = n * .26; d.rounded_rectangle([c - r, c - r, c + r, c + r], radius=r * .55, outline=255, width=lw)
        rr = r * .45; d.ellipse([c - rr, c - rr, c + rr, c + rr], outline=255, width=lw)
        dd = n * .035; d.ellipse([c + r * .55 - dd, c - r * .55 - dd, c + r * .55 + dd, c - r * .55 + dd], fill=255)
    elif kind == 'linkedin':
        f = font('Poppins-Bold.ttf', round(n * .42)); bb = d.textbbox((0, 0), 'in', font=f)
        d.text((c - (bb[2] + bb[0]) / 2, c - (bb[3] + bb[1]) / 2), 'in', font=f, fill=255)
    elif kind == 'facebook':
        f = font('Poppins-Bold.ttf', round(n * .5)); bb = d.textbbox((0, 0), 'f', font=f)
        d.text((c - (bb[2] + bb[0]) / 2, c - (bb[3] + bb[1]) / 2), 'f', font=f, fill=255)
    return g
def circle_icon(kind, n, big=4):
    N = n * big; base = Image.new('RGB', (N, N), WHITE)
    m = Image.new('L', (N, N), 0); ImageDraw.Draw(m).ellipse([1, 1, N - 2, N - 2], fill=255)
    base.paste(grad((N, N)), (0, 0), m); base.paste(Image.new('RGB', (N, N), WHITE), (0, 0), glyph(kind, N))
    return base, m
def icon_gif(kind, i):
    n = 60; big, m = circle_icon(kind, n)
    still = big.resize((n, n), Image.LANCZOS)
    frames, dur = [still], [1800 + i * 160]
    for k in range(10):
        f = shine(big, m, k / 9, width=.3, strength=.55).resize((n, n), Image.LANCZOS); frames.append(f); dur.append(45)
    frames.append(still); dur.append(1500 - i * 160)
    save_gif(frames, dur, f'icon-{kind}.gif')

def verified_gif():
    n = 30; N = n * 4; base = Image.new('RGB', (N, N), WHITE)
    m = Image.new('L', (N, N), 0); d = ImageDraw.Draw(m)
    pts = []
    import math
    for k in range(24):                                   # scalloped badge
        a = math.pi * 2 * k / 24; r = N * (.48 if k % 2 == 0 else .42); pts.append((N / 2 + r * math.cos(a), N / 2 + r * math.sin(a)))
    d.polygon(pts, fill=255); base.paste(grad((N, N), SKY, ROYAL), (0, 0), m)
    ImageDraw.Draw(base).line([(N * .3, N * .52), (N * .44, N * .66), (N * .71, N * .36)], fill=WHITE, width=round(N * .09), joint='curve')
    still = base.resize((n, n), Image.LANCZOS); frames, dur = [still], [2600]
    for k in range(8): frames.append(shine(base, m, k / 7, width=.35, strength=.6).resize((n, n), Image.LANCZOS)); dur.append(50)
    frames.append(still); dur.append(800)
    save_gif(frames, dur, 'verified.gif')

def button_gif():
    S = 4; W, H = 102 * 2, 30 * 2; BW, BH = W * S // 2, H * S // 2
    big = Image.new('RGB', (BW, BH), WHITE); m = Image.new('L', (BW, BH), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, BW - 1, BH - 1], radius=BH // 2, fill=255)
    big.paste(grad((BW, BH), diag=False), (0, 0), m)
    d = ImageDraw.Draw(big); f = font('Poppins-SemiBold.ttf', round(BH * .36)); label = 'Book a meeting'
    bb = d.textbbox((0, 0), label, font=f); tx = (BW - (bb[2] - bb[0])) / 2 - bb[0]; ty = (BH - (bb[3] - bb[1])) / 2 - bb[1]
    d.text((tx, ty), label, font=f, fill=WHITE)
    small = lambda im: im.resize((W, H), Image.LANCZOS)
    still = small(big); frames, dur = [still], [2200]
    for k in range(14): frames.append(small(shine(big, m, k / 13, width=.14, strength=.5))); dur.append(45)
    frames.append(still); dur.append(700)
    save_gif(frames, dur, 'book-a-meeting.gif')

# ---------------- HTML ----------------
FONT = "Inter, 'Segoe UI', Arial, sans-serif"
def signature_html():
    e = html.escape; u = lambda p: f'{BASE}/{p}'
    def a(href, inner, style='text-decoration:none;'):
        return f'<a href="{e(href)}" target="_blank" style="{style}">{inner}</a>'
    def icon(kind, href, alt):
        return (f'<td style="padding:0 4px 0 0;">' + a(href, f'<img src="{u("img/icon-" + kind + ".gif")}" width="30" height="30" alt="{alt}" '
                f'style="display:block;border:0;width:30px;height:30px;">') + '</td>')
    txt = f'font-family:{FONT};font-size:12px;line-height:18px;'
    return f'''<table cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;font-family:{FONT};">
<tr><td style="padding:15px;border:1px solid #E3E2EA;border-radius:8px;background-color:#ffffff;" bgcolor="#ffffff">
<table cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;"><tr>
<td valign="top" align="left" style="padding:0;">
  <table cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">
    <tr><td style="padding:0 0 8px 0;">
      <table cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;"><tr>
        <td valign="middle" style="font-family:{FONT};font-size:20px;line-height:24px;font-weight:bold;color:#250762;white-space:nowrap;">{e(ME['name'])}</td>
        <td valign="middle" style="padding-left:6px;"><img src="{u('img/verified.gif')}" width="15" height="15" alt="" style="display:block;border:0;width:15px;height:15px;"></td>
      </tr></table>
      <div style="{txt}color:#3299D5;white-space:nowrap;">{e(ME['title'])}</div>
    </td></tr>
    <tr><td style="{txt}font-weight:bold;color:#250762;white-space:nowrap;">{e(ME['company'])}</td></tr>
    <tr><td style="{txt}white-space:nowrap;">{a(ME['phone_link'], e(ME['phone']), 'text-decoration:none;color:#2F2E36;')}</td></tr>
    <tr><td style="{txt}white-space:nowrap;">{a('mailto:' + ME['email'], e(ME['email']), 'text-decoration:none;color:#2F2E36;')}</td></tr>
    <tr><td style="padding:10px 0 0 0;">
      <table cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;"><tr>
        {icon('web', ME['website'], 'Website')}{icon('instagram', ME['instagram'], 'Instagram')}{icon('linkedin', ME['linkedin'], 'LinkedIn')}{icon('facebook', ME['facebook'], 'Facebook')}
        <td style="padding:0 0 0 4px;">{a(ME['book'], f'<img src="{u("img/book-a-meeting.gif")}" width="102" height="30" alt="Book a meeting" style="display:block;border:0;width:102px;height:30px;">')}</td>
      </tr></table>
    </td></tr>
  </table>
</td>
<td style="padding:0 0 0 15px;border-right:2px solid #72CCD8;font-size:1px;line-height:1px;">&nbsp;</td>
<td valign="middle" align="center" style="padding:0 0 0 15px;">{a(ME['website'], f'<img src="{u("img/logo-" + LOGO_STYLE + ".gif")}" width="{PW}" height="{PH}" alt="First Search Marketing" style="display:block;border:0;width:{PW}px;height:{PH}px;">')}</td>
</tr></table>
</td></tr></table>'''

def pages():
    sig = signature_html()
    open(os.path.join(HERE, 'signature.html'), 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><title>Email signature</title></head><body>\n{sig}\n</body></html>\n')
    open(os.path.join(HERE, 'index.html'), 'w').write(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>First Search Marketing · Email signature</title>
<style>
body {{ margin: 0; background: #F4F4F6; font: 15px/1.6 Inter, 'Segoe UI', Arial, sans-serif; color: #2F2E36; }}
main {{ max-width: 760px; margin: 0 auto; padding: 40px 24px 60px; }}
h1 {{ margin: 0 0 6px; font: 800 28px/1.2 Poppins, Arial, sans-serif; color: #250762; }}
.stripe {{ height: 8px; background: linear-gradient(90deg, #72CCD8, #174FA2); }}
.card {{ margin: 24px 0; padding: 28px; border-radius: 16px; background: #fff; box-shadow: 0 18px 40px -24px rgba(37,7,98,.35); }}
button {{ padding: 12px 22px; border: 0; border-radius: 999px; background: linear-gradient(90deg, #72CCD8, #174FA2); font: 600 15px Poppins, Arial, sans-serif; color: #fff; cursor: pointer; }}
#ok {{ margin-left: 12px; font-weight: 600; color: #1F78B4; }}
h2 {{ margin: 0 0 8px; font: 700 18px Poppins, Arial, sans-serif; color: #250762; }}
ol {{ margin: 0; padding-left: 20px; }} li {{ margin: 4px 0; }}
</style></head><body><div class="stripe"></div><main>
<h1>Email signature</h1><p>Click <b>Copy signature</b>, then paste it into your email signature settings.</p>
<div class="card"><div id="sig">{sig}</div></div>
<p><button id="copy" type="button">Copy signature</button><span id="ok" hidden>Copied. Now paste it into Outlook.</span></p>
<div class="card"><h2>New Outlook, Outlook on the web</h2><ol>
<li>Settings (gear) &gt; Account &gt; Signatures &gt; New signature.</li>
<li>Click in the signature box and paste (Ctrl+V or Cmd+V). Save.</li>
<li>Pick it as the default for new messages and replies.</li></ol></div>
<div class="card"><h2>Classic Outlook for Windows</h2><ol>
<li>File &gt; Options &gt; Mail &gt; Signatures &gt; New.</li>
<li>Paste into the edit box and click OK. The logo and icons show their still first frame here; people using new Outlook, Apple Mail, Gmail and phones see the animation.</li></ol></div>
<div class="card"><h2>Outlook for Mac</h2><ol>
<li>Outlook &gt; Settings &gt; Signatures &gt; +.</li><li>Paste, name it, and close the window to save.</li></ol></div>
</main>
<script>
document.getElementById('copy').addEventListener('click', function () {{
  var r = document.createRange(); r.selectNode(document.getElementById('sig'));
  var s = getSelection(); s.removeAllRanges(); s.addRange(r); document.execCommand('copy'); s.removeAllRanges();
  document.getElementById('ok').hidden = false;
}});
</script></body></html>
''')
    print('wrote signature.html, index.html with assets from', BASE)

def options_page():
    global LOGO_STYLE
    keep = LOGO_STYLE; blocks = []
    names = dict(hop='1 · Hop: the pin hops and lands, then a shine crosses the name',
                 ping='2 · Ping: location rings ripple from the pin while the name grows and settles back',
                 **{'ping-reveal': '2b · Ping reveal: the rings ripple while the name appears from left to right'},
                 sweep='3 · Sweep: a soft light passes across the box texture and the name',
                 search='4 · Search: the pin tilts side to side like it is scanning, then the lens sparkles')
    for k in ('ping', 'ping-reveal', 'hop', 'sweep', 'search'):
        LOGO_STYLE = k; blocks.append(f'<section><h2>{names[k]}</h2><div class="card">{signature_html()}</div></section>')
    LOGO_STYLE = keep
    open(os.path.join(HERE, 'logo-options.html'), 'w').write(f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Email signature · logo animation options</title><style>
body {{ margin: 0; background: #F4F4F6; font: 15px/1.6 Inter, Arial, sans-serif; color: #2F2E36; }}
main {{ max-width: 760px; margin: 0 auto; padding: 36px 24px 60px; }}
h1 {{ margin: 0 0 4px; font: 800 26px Poppins, Arial, sans-serif; color: #250762; }}
h2 {{ margin: 28px 0 10px; font: 700 16px Poppins, Arial, sans-serif; color: #250762; }}
.card {{ padding: 24px; border-radius: 16px; background: #fff; box-shadow: 0 18px 40px -24px rgba(37,7,98,.35); }}
.stripe {{ height: 8px; background: linear-gradient(90deg, #72CCD8, #174FA2); }}
</style></head><body><div class="stripe"></div><main><h1>Logo animation options</h1>
<p>Each plays about every 4 seconds. All four start on the same still logo, which is what classic Outlook for Windows shows.</p>
{''.join(blocks)}</main></body></html>''')
    print('wrote logo-options.html')

if __name__ == '__main__':
    if '--html-only' not in sys.argv:
        logo_gifs(); verified_gif(); button_gif()
        for i, k in enumerate(('web', 'instagram', 'linkedin', 'facebook')): icon_gif(k, i)
    pages(); options_page()
