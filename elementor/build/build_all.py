"""Build every Elementor template in one run so element IDs are unique across files.
Output: elementor/templates/{header,footer}.json plus pages/, services/, framework/, singles/, location/."""
import sys, os, glob, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from fsel import template, save
import header_footer, pages_a, pages_b, pages_c, pages_d

T = []  # (folder/file, title, kind, builder)
T += [('pages/01-home', 'Home', 'page', pages_a.home), ('pages/02-about-us', 'About Us', 'page', pages_a.about),
      ('pages/03-why-choose-us', 'Why Choose Us', 'page', pages_a.why), ('pages/04-services', 'Services', 'page', pages_a.overview),
      ('pages/05-events', 'Events', 'page', pages_b.events), ('pages/06-resources', 'Resources', 'page', pages_b.resources),
      ('pages/07-befirst-training', 'BeFirst Training', 'page', pages_b.training), ('pages/08-contact-us', 'Contact Us', 'page', pages_b.contact)]
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
save('../templates/header.json', header_footer.HEADER)
save('../templates/footer.json', header_footer.FOOTER)
for path, title, kind, fn in T:
    save(f'../templates/{path}.json', template('First Search · ' + title, kind, fn()))
ids = []
def walk(e): ids.append(e['id']); [walk(c) for c in e.get('elements', [])]
files = glob.glob('../templates/**/*.json', recursive=True)
for f in files: [walk(e) for e in json.load(open(f))['content']]
print('templates', len(files), 'elements', len(ids), 'all ids unique', len(ids) == len(set(ids)))
