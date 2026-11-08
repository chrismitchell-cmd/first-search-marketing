import sys; sys.path.insert(0, '.')
from fsel import *

SVC = {
 'brand':    ('Build the foundation', [('Branding & Content Creation', 'branding-content-creation'), ('Website', 'website'), ('Analytics', 'analytics'), ('CRM', 'crm')]),
 'thought':  ('Get found first',      [('SEO', 'seo'), ('Advertising', 'advertising'), ('Social Media', 'social-media'), ('Local Ties', 'local-ties')]),
 'choice':   ('Get chosen',           [('Advertising', 'advertising'), ('Social Media', 'social-media'), ('Lead Generation', 'lead-generation'), ('Marketing Automation', 'marketing-automation')]),
 'referral': ('Get referred',         [('Social Media', 'social-media'), ('Marketing Automation', 'marketing-automation'), ('Loyalty', 'loyalty'), ('Reviews & Referrals', 'reviews-referrals')]),
}
def _link(u): return {'url': u, 'is_external': '', 'nofollow': ''}
def dd_item(title, desc, url):
    """One row in a small dropdown: bold page name + one-line description, the whole row is the link."""
    return con(heading(title, 'p', 'fs-dd-t'), text(desc, 'fs-dd-d'), cls='fs-dd-item', gap_=2, p=pad(14, 16), s={'html_tag': 'a', 'link': _link(url)})
def dd_panel(*items):
    return con(*items, cls='fs-dd', gap_=2, p=pad(12), s={'width': px(380)})

def stage_col(k):
    job, svcs = SVC[k]
    head = con(heading(plogo(k), 'p', 'fs-mm-stage'), text(job, 'fs-mm-job'), cls='fs-mm-head', gap_=4, p=pad(8, 10, 14, 10),
               s={'html_tag': 'a', 'link': _link(f'/first{k}/')})
    lst = icon_list([n for n, _ in svcs], icon='', cls='fs-mm-svcs', links=[f'/services/{x}/' for _, x in svcs])
    return con(head, lst, cls='fs-mm-col', gap_=0)

def big_link(title, sub, url):
    return con(heading(title, 'p', 'fs-mm-big-t'), text(sub, 'fs-mm-big-s'), cls='fs-mm-big', gap_=2, p=pad(12, 14), s={'html_tag': 'a', 'link': _link(url)})

panel_about = dd_panel(dd_item('About Us', 'Our story, values and the team behind your marketing', '/about-us/'),
                       dd_item('Why Choose Us', 'How we compare, and the FirstSearch Guarantee', '/why-choose-us/'))
mega_cta = con(heading('What we do', 'p', 'fs-mm-k'), big_link('All services', '12 services, one system', '/services/'),
               big_link('The FirstSearch Framework', 'Four stages, one customer journey', '/services/#framework'),
               button('Let’s Talk!', '/contact-us/', 'fs-mm-btn'), cls='fs-mm-cta', gap_=10, p=pad(24))
panel_do = con(con(con(*[stage_col(k) for k in SVC], d='row', gap_=26, cls='fs-mm-cols', mobile_col=True), mega_cta,
                   d='row', gap_=30, cls='fs-mm-in', mobile_col=True, p=pad(34, 24, 38, 24)),
               cls='fs-mm', gap_=0, p=pad(0))
panel_grow = dd_panel(dd_item('Events', 'Workshops and live trainings, online and in Hampton', '/events/'),
                      dd_item('Resources', 'Articles, client stories, podcasts and videos', '/resources/'),
                      dd_item('BeFirst Training', 'The Community, Blueprint and 1:1 coaching to grow it yourself', '/befirst-training/'))
panel_contact = con(p=pad(0))

items = [('About First Search', True, ''), ('What We Do', True, ''), ('Grow Your Marketing', True, ''), ('Contact Us', False, '/contact-us/')]
CHEV = {'value': 'fas fa-chevron-down', 'library': 'fa-solid'}
menu = {'id': uid(), 'elType': 'widget', 'widgetType': 'mega-menu', 'settings': {
    'menu_items': [dict({'_id': uid(), 'item_title': t, 'item_dropdown_content': 'yes' if dd else ''},
                        **({'item_link': _link(u)} if u else {})) for t, dd, u in items],
    'item_layout': 'horizontal', 'open_on': 'hover', 'content_width': 'fit_to_content', 'breakpoint_selector': 'tablet',
    'menu_item_icon': CHEV, 'menu_item_icon_active': {'value': 'fas fa-chevron-up', 'library': 'fa-solid'},
    'menu_item_title_distance_from_content': px(18), 'menu_toggle_icon_normal': {'value': 'fas fa-bars', 'library': 'fa-solid'},
    '_css_classes': 'fs-nav'},
    'elements': [panel_about, panel_do, panel_grow, panel_contact]}

logo = image('assets/img/logo.png', 'fs-hdr-logo', None, 'left', 'First Search Marketing')
logo['settings'].update({'link_to': 'custom', 'link': _link('/')})
header_row = con(logo, menu, button('Let’s Talk!', '/contact-us/', 'fs-header-cta'),
                 d='row', mobile_col=False, cls='fs-header-row', align='center', gap_=32, minh=112,
                 s={'min_height_tablet': px(88), 'min_height_mobile': px(76), 'padding': pad(0), 'padding_tablet': pad(0, 24), 'padding_mobile': pad(0, 16), 'flex_wrap': 'nowrap'})
stripe = con(cls='fs-stripe2', minh=14, p=pad(0),
             s={'min_height_mobile': px(8), 'background_background': 'gradient', 'background_color': '#72CCD8', 'background_color_b': '#174FA2',
                'background_gradient_type': 'linear', 'background_gradient_angle': {'unit': 'deg', 'size': 90, 'sizes': []}})
header = con(con(header_row, boxed=True, inner=True, cls='fs-header-box', s={'padding': pad(0)}), stripe, inner=False, cls='fs-header', gap_=0, p=pad(0), title='Header',
             s={'sticky': 'top', 'sticky_on': ['desktop', 'tablet', 'mobile'], 'sticky_effects_offset': 30, 'z_index': 100,
                'background_background': 'classic', 'background_color': '#FFFFFF'})
header_row['elements'][2]['settings'].update({'hide_mobile': 'hidden-mobile'})
HEADER = template('First Search · Header', 'header', [header])

# ---------------- Footer ----------------
col = lambda title, *kids: con(heading(title, 'h4', 'fs-col-title'), *kids, gap_=14, s={'width': {'unit': '%', 'size': 22, 'sizes': []}, 'width_mobile': {'unit': '%', 'size': 100, 'sizes': []}})
links = lambda pairs: icon_list([t for t, _ in pairs], icon='', links=[u for _, u in pairs])
# Footer logo: the logo in its white glowing box, as one PNG (design/footer-logo.png). The PNG includes 36px of glow
# around the box, so negative margins line the box up with the content edge.
footer_logo = image('assets/img/design/footer-logo.png', '', 305, alt='First Search Marketing')
footer_logo['settings'].update({'link_to': 'custom', 'link': {'url': '/', 'is_external': '', 'nofollow': ''},
                                '_margin': {'unit': 'px', 'top': '-36', 'right': '0', 'bottom': '-36', 'left': '-36', 'isLinked': False}})
# Newsletter: email field and Subscribe button on one line (stacked on phones), labels hidden, as in the design
newsletter = form([('email', 'Email address', True, 'you@business.com', '70')], 'Subscribe', 'Newsletter', 'fs-news-form')
newsletter['settings'].update({'show_labels': '', 'button_width': '30', 'button_width_mobile': '100', 'column_gap': px(10), 'row_gap': px(10),
                               'success_message': 'Thanks! You’re on the list.'})
newsletter['settings']['form_fields'][0]['width_mobile'] = '100'
top = con(
    con(footer_logo, heading('We put your <span class="fs-gt">business first.</span>', 'p', 'fs-tagline'), gap_=18,
        s={'width': {'unit': '%', 'size': 48, 'sizes': []}, 'width_mobile': {'unit': '%', 'size': 100, 'sizes': []}}),
    con(heading('The FirstSearcher monthly', 'h3'),
        text('One practical marketing play for local businesses, every month. No spam.'),
        newsletter,
        cls='fs-news', gap_=8, s={'width': {'unit': '%', 'size': 46, 'sizes': []}, 'width_mobile': {'unit': '%', 'size': 100, 'sizes': []}}),
    d='row', justify='space-between', align='center', gap_=40, p=pad(0, 0, 40, 0))
cols = con(
    col('About First Search', links([('About Us', '/about-us/'), ('Why Choose Us', '/why-choose-us/'), ('Contact Us', '/contact-us/'), ('Careers', '/careers/')])),
    col('What We Do', links([('All services', '/services/'), ('The FirstSearch Framework', '/services/#framework')]),
        html('<div class="fs-stage-links">' + '<br>'.join(f'<a href="/first{k}/">{plogo(k, True)}</a>' for k in SVC) + '</div>')),
    col('Grow Your Marketing', links([('Events', '/events/'), ('Resources', '/resources/'), ('BeFirst Training', '/befirst-training/'), ('Framework Quiz', '/framework-quiz/')])),
    col('Get in touch',
        w('icon-list', {'icon_color': '#FFFFFF', 'icon_size': px(18), 'text_indent': px(12), 'icon_list': [
            {'_id': uid(), 'text': '1 Merrill Industrial Drive, Unit #4, Hampton, NH 03842', 'selected_icon': {'value': 'fas fa-map-marker-alt', 'library': 'fa-solid'}, 'link': {'url': 'https://maps.google.com/?q=1+Merrill+Industrial+Drive+Unit+4+Hampton+NH+03842', 'is_external': 'on', 'nofollow': ''}},
            {'_id': uid(), 'text': '603-518-8090', 'selected_icon': {'value': 'fas fa-phone', 'library': 'fa-solid'}, 'link': {'url': 'tel:+16035188090', 'is_external': '', 'nofollow': ''}},
            {'_id': uid(), 'text': 'chris@befirstsearch.com', 'selected_icon': {'value': 'fas fa-envelope', 'library': 'fa-solid'}, 'link': {'url': 'mailto:chris@befirstsearch.com', 'is_external': '', 'nofollow': ''}}]}, 'fs-ct'),
        w('social-icons', {'social_icon_list': [
            {'_id': uid(), 'social_icon': {'value': 'fab fa-facebook-f', 'library': 'fa-brands'}, 'link': {'url': 'https://www.facebook.com/p/First-Search-Marketing-LLC-100063771473527/', 'is_external': 'on'}},
            {'_id': uid(), 'social_icon': {'value': 'fab fa-instagram', 'library': 'fa-brands'}, 'link': {'url': '#', 'is_external': 'on'}},
            {'_id': uid(), 'social_icon': {'value': 'fab fa-linkedin-in', 'library': 'fa-brands'}, 'link': {'url': '#', 'is_external': 'on'}}],
            'shape': 'circle', 'icon_size': px(17), 'icon_padding': {'unit': 'em', 'size': 0.75, 'sizes': []}, 'icon_spacing': px(10), 'align': 'left',
            'icon_color': 'custom', 'icon_primary_color': 'rgba(255,255,255,0.1)', 'icon_secondary_color': '#FFFFFF', '_margin': {'unit': 'px', 'top': '22', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': False}}, 'fs-social')),
    d='row', justify='space-between', gap_=32, p=pad(40, 0), s={'border_border': 'solid', 'border_width': {'unit': 'px', 'top': '1', 'right': '0', 'bottom': '1', 'left': '0', 'isLinked': False}, 'border_color': 'rgba(255,255,255,0.14)'})
bottom = con(text('© 2026 First Search Marketing LLC · Family-owned in Hampton, NH'),
             text('<a href="/privacy-policy/">Privacy policy</a> &nbsp; <a href="/terms/">Terms</a>'),
             d='row', justify='space-between', align='center', cls='fs-bottom', p=pad(22, 0, 0, 0))
footer = con(con(top, cols, bottom, boxed=True, inner=True, s={'padding': pad(0)}),
             inner=False, cls='fs-footer', p={'unit': 'px', 'top': '140', 'right': '24', 'bottom': '40', 'left': '24', 'isLinked': False}, gap_=0,
             s={'padding_tablet': {'unit': 'px', 'top': '110', 'right': '24', 'bottom': '40', 'left': '24', 'isLinked': False},
                'padding_mobile': {'unit': 'px', 'top': '110', 'right': '16', 'bottom': '40', 'left': '16', 'isLinked': False}})
footer_bar = con(cls='fs-stripe', inner=False, minh=10, p=pad(0))
FOOTER = template('First Search · Footer', 'footer', [footer, footer_bar])
