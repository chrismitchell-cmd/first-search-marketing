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
for path, _, tpl in built:
    save(f'../templates/{path}.json', tpl)
css = open('../site-settings.css', encoding='utf-8').read()
kit_settings = kit.build('../first-search-site-settings.zip', styler.kit_typography(presets), css)
json.dump(kit_settings, open('data/kit-preview.json', 'w'))
print('global font presets', len(presets))
ids = []
def walk(e): ids.append(e['id']); [walk(c) for c in e.get('elements', [])]
files = glob.glob('../templates/**/*.json', recursive=True)
for f in files: [walk(e) for e in json.load(open(f))['content']]
print('templates', len(files), 'elements', len(ids), 'all ids unique', len(ids) == len(set(ids)))
