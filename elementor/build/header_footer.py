import sys; sys.path.insert(0, '.')
from fsel import *

SVC = {
 'brand':    ('Build the foundation', [('Branding & Content Creation', 'branding-content-creation'), ('Website', 'website'), ('Analytics', 'analytics'), ('CRM', 'crm')]),
 'thought':  ('Get found first',      [('SEO', 'seo'), ('Advertising', 'advertising'), ('Social Media', 'social-media'), ('Local Ties', 'local-ties')]),
 'choice':   ('Get chosen',           [('Advertising', 'advertising'), ('Social Media', 'social-media'), ('Lead Generation', 'lead-generation'), ('Marketing Automation', 'marketing-automation')]),
 'referral': ('Get referred',         [('Social Media', 'social-media'), ('Marketing Automation', 'marketing-automation'), ('Loyalty', 'loyalty'), ('Reviews & Referrals', 'reviews-referrals')]),
}
def menu_list(items):
    return '<ul class="fs-menu-list">' + ''.join(f'<li><a href="{u}"><b>{t}</b><span>{d}</span></a></li>' for t, d, u in items) + '</ul>'

def stage_col(k):
    job, svcs = SVC[k]
    h = (f'<a class="fs-stage-link" href="/first{k}/">{plogo(k)}<small>{job}</small></a>'
         '<ul class="fs-svc-list">' + ''.join(f'<li><a href="/services/{s}/">{n}</a></li>' for n, s in svcs) + '</ul>')
    return con(html(h), w=None, s={'flex_grow': 1, 'width': {'unit': '%', 'size': 24, 'sizes': []}})

panel_about = con(html(menu_list([('About Us', 'Our story, values and the team behind your marketing', '/about-us/'),
                                  ('Why Choose Us', 'How we compare, and the FirstSearch Guarantee', '/why-choose-us/')])),
                  cls='fs-mega', p=pad(14), s={'width': px(380)})
mega_cta = con(
    heading('What we do', 'p', 'fs-eyebrow'),
    html('<div class="fs-mega-cta"><a class="fs-big" href="/services/">All services<span>12 services, one system</span></a>'
         '<a class="fs-big" href="/services/#framework">The FirstSearch Framework<span>Four stages, one customer journey</span></a></div>'),
    button('Let’s Talk!', '/contact-us/', 'fs-btn-white'),
    cls='fs-purple-card fs-mega-cta', p=pad(26), gap_=12, s={'width': px(280), 'flex_shrink': 0})
panel_do = con(con(*[stage_col(k) for k in SVC], d='row', gap_=8, mobile_col=True, s={'flex_grow': 1}),
               mega_cta, d='row', cls='fs-mega', p=pad(22), gap_=22, s={'width': px(1180), 'width_tablet': {'unit': '%', 'size': 100, 'sizes': []}})
panel_grow = con(html(menu_list([('Events', 'Workshops and live trainings, online and in Hampton', '/events/'),
                                 ('Resources', 'Articles, client stories, podcasts and videos', '/resources/'),
                                 ('BeFirst Training', 'The Community, Blueprint and 1:1 coaching to grow it yourself', '/befirst-training/')])),
                 cls='fs-mega', p=pad(14), s={'width': px(420)})
panel_contact = con()

items = [('About First Search', True, ''), ('What We Do', True, '/services/'), ('Grow Your Marketing', True, ''), ('Contact Us', False, '/contact-us/')]
menu = {'id': uid(), 'elType': 'widget', 'widgetType': 'n-menu', 'settings': {
    'menu_items': [dict({'_id': uid(), 'item_title': t, 'item_dropdown_content': 'yes' if dd else ''},
                        **({'item_link': {'url': u, 'is_external': '', 'nofollow': ''}} if u else {})) for t, dd, u in items],
    'item_layout': 'horizontal', 'open_on': 'hover', 'content_width': 'fit_to_content', 'breakpoint_selector': 'tablet',
    'menu_item_title_distance_from_content': px(14), '_css_classes': 'fs-nav'},
    'elements': [panel_about, panel_do, panel_grow, panel_contact]}

header_row = con(
    w('theme-site-logo', {'image_size': 'full', 'width': px(220), 'link_to': 'home'}),
    menu,
    button('Let’s Talk!', '/contact-us/', 'fs-header-cta'),
    d='row', mobile_col=False, cls='fs-header-row', justify='space-between', align='center', gap_=32, minh=112,
    s={'min_height_mobile': px(76), 'padding': pad(0, 24), 'padding_mobile': pad(0, 16), 'flex_wrap': 'nowrap'})
header = con(con(header_row, boxed=True, inner=True, s={'padding': pad(0)}),
             con(cls='fs-stripe', minh=10, s={'padding': pad(0)}),
             inner=False, cls='fs-header', gap_=0, p=pad(0),
             s={'sticky': 'top', 'sticky_on': ['desktop', 'tablet', 'mobile'], 'sticky_effects_offset': 30, 'background_background': 'classic', 'background_color': '#FFFFFF'})
# Hide the header CTA on phones (the mobile menu has Contact Us)
header_row['elements'][2]['settings'].update({'hide_mobile': 'hidden-mobile'})
# The header is an exact copy of the design's header (logo, mega nav, CTA, mobile menu, stripe) in one HTML widget,
# so it doesn't depend on Elementor's Menu feature. Edit menu text and links inside that widget.
from comp import component
header = con(component('header', 'fs-site-header-w'), inner=False, cls='fs-site-header', gap_=0, p=pad(0), title='Header (design)',
             s={'sticky': 'top', 'sticky_on': ['desktop', 'tablet', 'mobile'], 'sticky_effects_offset': 30, 'z_index': 100,
                'background_background': 'classic', 'background_color': '#FFFFFF'})
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
