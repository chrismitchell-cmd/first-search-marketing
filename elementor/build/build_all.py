"""Build every Elementor template in one run so element IDs are unique across files.
Output: elementor/templates/{header,footer}.json plus pages/, services/, framework/, singles/, location/."""
import sys, os, glob, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from fsel import template, save
import header_footer, pages_a, pages_b, pages_c, pages_d, styler, kit

T = []  # (folder/file, title, kind, builder)
T += [('pages/01-home', 'Home', 'page', pages_a.home), ('pages/02-about-us', 'About Us', 'page', pages_a.about),
      ('pages/03-why-choose-us', 'Why Choose Us', 'page', pages_a.why), ('pages/04-services', 'Services', 'page', pages_a.overview),
      ('pages/05-events', 'Events', 'page', pages_b.events), ('pages/06-resources', 'Resources', 'page', pages_b.resources),
      ('pages/07-befirst-training', 'BeFirst Training', 'page', pages_b.training), ('pages/08-contact-us', 'Contact Us', 'page', pages_b.contact)]
# which approved HTML page each template is measured against
PROTO = {'pages/01-home': 'home', 'pages/02-about-us': 'about', 'pages/03-why-choose-us': 'why', 'pages/04-services': 'overview',
         'pages/05-events': 'events', 'pages/06-resources': 'resources', 'pages/07-befirst-training': 'training', 'pages/08-contact-us': 'contact',
         'singles/single-blog-post': 'blog', 'singles/single-podcast-episode': 'podcast', 'singles/single-video': 'video',
         'singles/single-event': 'event', 'singles/single-case-study': 'case', 'location/location-page-seo-portsmouth-sample': 'location'}
for i, s in enumerate(pages_d.SDATA, 1):
    T.append((f'services/{i:02d}-{pages_d.url_slug(s)}', f'Service · {pages_d.SDATA[s]["name"]}', 'page', lambda s=s: pages_d.service(s)))
for i, k in enumerate(pages_d.ORDER, 1):
    T.append((f'framework/{i}-first{k}', f'Framework stage · {pages_d.ST[k][1]}', 'page', lambda k=k: pages_d.stage(k)))
T += [('singles/single-blog-post', 'Single · Blog post', 'single-post', pages_c.blog),
      ('singles/single-podcast-episode', 'Single · Podcast episode', 'single-post', pages_d.podcast),
      ('singles/single-video', 'Single · Video', 'single-post', pages_d.video_page),
      ('singles/single-event', 'Single · Event', 'single-post', pages_c.event),
      ('singles/single-case-study', 'Single · Case study', 'single-post', pages_c.case_study),
      ('location/location-page-seo-portsmouth-sample', 'Location page · SEO Portsmouth (sample)', 'page', pages_c.location)]

for f in glob.glob('../templates/**/*.json', recursive=True): os.remove(f)
for d in ('pages', 'services', 'framework', 'singles', 'location'): os.makedirs(f'../templates/{d}', exist_ok=True)
def proto_key(path):
    if path in PROTO: return PROTO[path]
    if path.startswith('services/'): return 'service:' + {'branding-content-creation': 'branding'}.get(path.split('-', 1)[1], path.split('-', 1)[1])
    if path.startswith('framework/'): return 'stage:' + path.split('first', 1)[1]
    return 'home'
built = [('header', 'home', header_footer.HEADER), ('footer', 'home', header_footer.FOOTER)]
for path, title, kind, fn in T:
    built.append((path, proto_key(path), template('First Search · ' + title, kind, fn())))
presets = styler.process([(pk, tpl) for _, pk, tpl in built])
# Overlapping buttons, as in the HTML:
#  - a big "Let's Talk!" that ends a section sits on the edge: section bottom padding 0, button on top, next section 46px up
#  - after "How it works"/"Your first 90 days" on Home, Why and service pages: a separate overlapping button
import comp
def is_big_btn(e): return e.get('widgetType') == 'button' and 'fs-btn-lg' in e['settings'].get('_css_classes', '')
for path, pk, tpl in built:
    c = tpl['content']
    if pk in ('home', 'why') or pk.startswith('service:'):
        for i, e in enumerate(c):
            if e['settings'].get('_title') == 'How it works':
                c.insert(i + 1, comp.overlap_cta()); break
    for i, e in enumerate(c[:-1]):
        inner = e['elements'][0] if e.get('elements') and e['elements'][0]['elType'] == 'container' else e
        last = inner['elements'][-1] if inner.get('elements') else None
        nxt = c[i + 1]
        if e['settings'].get('_title') == 'Overlapping button':
            continue
        if last and is_big_btn(last) and e['settings'].get('_title') not in ('Hero', 'CTA banner'):
            last['settings']['_z_index'] = 3
            last['settings']['align_mobile'] = 'justify'
            for suf in ('', '_tablet', '_mobile'):
                if isinstance(e['settings'].get('padding' + suf), dict): e['settings']['padding' + suf]['bottom'] = '0'
            if nxt['settings'].get('_title') not in ('CTA banner', 'Overlapping button'):
                nxt['settings']['margin'] = {'unit': 'px', 'top': '-46', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': False}
# Footer link lists rest at 86% white (white + gradient underline on hover), as in the design
def _foot(e):
    if e.get('widgetType') == 'icon-list':
        e['settings']['text_color'] = '#FFFFFFDB'; e['settings'].get('__globals__', {}).pop('text_color', None)
    for c in e.get('elements', []): _foot(c)
for e in header_footer.FOOTER['content']: _foot(e)
# Image boxes: no colour change on hover (Elementor turns the title Primary purple by default)
# How it works: four white cards with dark text
def _fix(e, in_step=False):
    st = e['settings']
    if e.get('widgetType') == 'image-box':
        g = st.setdefault('__globals__', {})
        if g.get('title_color'): g['hover_title_color'] = g['title_color']
        else: st['hover_title_color'] = st.get('title_color') or '#FFFFFF'
    if in_step and e.get('widgetType') == 'heading' and 'fs-step-num' not in st.get('_css_classes', ''):
        g = st.setdefault('__globals__', {})
        if in_step == 'hl': st['title_color'] = '#FFFFFF'; g.pop('title_color', None)
        else: st.pop('title_color', None); g['title_color'] = 'globals/colors?id=primary'
    if in_step and e.get('widgetType') == 'text-editor':
        g = st.setdefault('__globals__', {})
        if in_step == 'hl': st['text_color'] = '#FFFFFF'; g.pop('text_color', None)
        else: st.pop('text_color', None); g['text_color'] = 'globals/colors?id=text'
    if in_step and e.get('widgetType') == 'icon':
        st['primary_color'] = '#FFFFFF' if in_step == 'hl' else '#3299D5'
    cls = st.get('css_classes', '').split() if e['elType'] == 'container' else []
    step = in_step or (('hl' if 'fs-step-hl' in cls else True) if 'fs-step' in cls else False)
    for c in e.get('elements', []): _fix(c, step)
for _, _, tpl in built:
    for e in tpl['content']: _fix(e)
# The CTA banner is pulled 110px up: the section right above it always gets the FAQ spacing (230px, 170px on phones)
for path, pk, tpl in built:
    c = tpl['content']
    for i, e in enumerate(c[:-1]):
        if 'fs-final' not in c[i + 1]['settings'].get('css_classes', '') or e['settings'].get('min_height'): continue
        for suf, v in (('', 230), ('_tablet', 200), ('_mobile', 170)):
            pd = e['settings'].get('padding' + suf) or dict(e['settings'].get('padding') or {})
            if pd and int(float(pd.get('bottom') or 0)) < v:
                pd = dict(pd, bottom=str(v), isLinked=False); e['settings']['padding' + suf] = pd
# Final URLs (SEO plan): the Website service lives at /services/web-design/
URL_RENAMES = {'/services/website/': '/services/web-design/'}
def _renamed(t):
    j = json.dumps(t)
    for a, b in URL_RENAMES.items(): j = j.replace(a, b)
    return json.loads(j)
# Alt text on content images (icons stay decorative, empty alt)
ALT = {'befirst-training.png': 'BeFirst Marketing Training logo', 'befirst-coaching.png': 'BeFirst Marketing Coaching logo',
       'blueprint-book.webp': 'The FirstSearch Marketing Blueprint workbook', 'case-dental.webp': 'Client case study: a local dental practice',
       'course-mockup.webp': 'The BeFirst online marketing course on laptop and tablet', 'problem-art.png': 'Illustration of a business owner overwhelmed by marketing tasks',
       'chris-cutout.webp': 'Chris Mitchell, Owner and Digital Partner at First Search Marketing', 'scorecard.png': 'Sample FirstSearch Framework scorecard',
       'team-group.webp': 'The First Search Marketing team', 'logo.png': 'First Search Marketing'}
def _alts(e):
    if e.get('widgetType') == 'image':
        im = e['settings']['image']; fn = im['url'].rsplit('/', 1)[-1]
        if not im.get('alt') and fn in ALT: im['alt'] = ALT[fn]
    for c in e.get('elements', []): _alts(c)
for path, _, tpl in built:
    for e in tpl['content']: _alts(e)
for path, _, tpl in built:
    save(f'../templates/{path}.json', _renamed(tpl))
# split the stylesheet: small global CSS for Site Settings, the rest onto each template that uses it
import subprocess
subprocess.run(['node', 'split_css.js'], check=True)
css = open('../global.css', encoding='utf-8').read()
kit_settings = kit.build('../first-search-site-settings.zip', styler.kit_typography(presets), css)
json.dump(kit_settings, open('data/kit-preview.json', 'w'))
print('global font presets', len(presets))
ids = []
def walk(e): ids.append(e['id']); [walk(c) for c in e.get('elements', [])]
files = glob.glob('../templates/**/*.json', recursive=True)
for f in files: [walk(e) for e in json.load(open(f))['content']]
print('templates', len(files), 'elements', len(ids), 'all ids unique', len(ids) == len(set(ids)))
