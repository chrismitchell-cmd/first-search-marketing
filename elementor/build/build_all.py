"""Build every Elementor template (header, footer, 15 pages) in one run so element IDs are unique across files."""
import sys, os, glob, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from fsel import template, save
import header_footer, pages_a, pages_b, pages_c
PAGES = [('01-home', 'Home', pages_a.home), ('02-about-us', 'About Us', pages_a.about), ('03-why-choose-us', 'Why Choose Us', pages_a.why),
         ('04-services', 'Services', pages_a.overview), ('05-service-single-seo-sample', 'Service (single) · SEO sample', pages_b.service),
         ('06-framework-stage-firstchoice-sample', 'Framework stage · FirstChoice sample', pages_b.pillar), ('07-events', 'Events', pages_b.events),
         ('08-resources', 'Resources', pages_b.resources), ('09-befirst-training', 'BeFirst Training', pages_b.training), ('10-contact-us', 'Contact Us', pages_b.contact),
         ('11-case-study-single-sample', 'Case study (single) · sample', pages_c.case_study), ('12-blog-post-single', 'Blog post (single)', pages_c.blog),
         ('13-podcast-video-single-sample', 'Podcast / Video (single) · sample', pages_c.resource), ('14-event-single-sample', 'Event (single) · sample', pages_c.event),
         ('15-location-page-seo-portsmouth-sample', 'Location page · SEO Portsmouth sample', pages_c.location)]
os.makedirs('../templates/pages', exist_ok=True)
for f in glob.glob('../templates/pages/*.json'): os.remove(f)
save('../templates/header.json', header_footer.HEADER)
save('../templates/footer.json', header_footer.FOOTER)
for slug, title, fn in PAGES:
    save(f'../templates/pages/{slug}.json', template('First Search · ' + title, 'single-post' if 'Blog post' in title else 'page', fn()))
ids = []
def walk(e): ids.append(e['id']); [walk(c) for c in e.get('elements', [])]
for f in glob.glob('../templates/**/*.json', recursive=True): [walk(e) for e in json.load(open(f))['content']]
print('templates', len(glob.glob('../templates/**/*.json', recursive=True)), 'elements', len(ids), 'all ids unique', len(ids) == len(set(ids)))
