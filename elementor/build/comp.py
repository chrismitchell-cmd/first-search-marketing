"""Shared page sections, matching the approved prototype."""
from fsel import *

PCT = lambda n: {'unit': '%', 'size': n, 'sizes': []}

import json as _json, os as _os
_RUNTIME = '''if(!window.__fsxTH){window.__fsxTH=1;(function(){
var SKIP=new Set(['i-chev','i-close','i-menu','i-arrow','i-left','i-right','i-play','i-google','i-facebook','i-instagram','i-linkedin','i-x','i-star','i-search']);
var DARK='.on-dark, .note, .booked, .btn, .navy-card, .step--hl, .vid, .scorecard, [data-noswap]';
function light(c){var m=c.match(/\\d+(\\.\\d+)?/g);if(!m)return false;return (m[0]*.299+m[1]*.587+m[2]*.114)>200;}
function swap(){document.querySelectorAll('.fsx svg use').forEach(function(u){var h=u.getAttribute('href');if(!h||h.slice(-3)==='--g')return;var id=h.slice(1);
if(SKIP.has(id)||!document.getElementById(id+'--g'))return;var svg=u.closest('svg');if(!svg||svg.closest(DARK)||light(getComputedStyle(svg).color))return;u.setAttribute('href',h+'--g');});}
var q;new MutationObserver(function(){cancelAnimationFrame(q);q=requestAnimationFrame(swap);}).observe(document.body,{childList:true,subtree:true});swap();})();}'''
def component(name, cls=''):
    """An exact copy of an interactive part of the approved HTML (markup, scoped CSS, icons, script) in an HTML widget."""
    d = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'data', 'components', name + '.json')))
    js = ("(function(){var cs=document.currentScript;var ROOT=(cs&&cs.closest('.fsx'))||[].slice.call(document.querySelectorAll('.fsx-" + name + ":not([data-fsx-init])')).pop();"
          "if(!ROOT||ROOT.getAttribute('data-fsx-init'))return;ROOT.setAttribute('data-fsx-init','1');" + _RUNTIME +
          "try{(() => {'use strict';const RM=matchMedia('(prefers-reduced-motion: reduce)').matches;const $=(s,el=ROOT)=>el.querySelector(s);"
          "const $$=(s,el=ROOT)=>[...el.querySelectorAll(s)];const wait=ms=>new Promise(r=>setTimeout(r,ms));\n" + d['js'] + "\n})();}catch(e){console.error('fsx-" + name + "',e);}})();")
    code = (f'<!-- First Search component: {name}. Exact copy of the approved design; edit text inside this HTML. -->\n'
            f'<div class="fsx fsx-{name}">{d["html"]}<script>{js}</script></div>\n<style>{d["css"]}</style>')
    return html(code, cls)
def mobile_w(e, n):
    e['settings']['width_mobile'] = px(n); return e
def col(*kids, wpct=50, gap_=20, cls='', align=None, justify=None, p=None, s=None):
    st = {'width': PCT(wpct), 'width_mobile': PCT(100)}
    if s: st.update(s)
    return con(*kids, gap_=gap_, cls=cls, align=align, justify=justify, p=p, s=st)
def row(*kids, gap_=32, align='center', justify=None, cls='', wrap=False, p=None, s=None):
    return con(*kids, d='row', gap_=gap_, align=align, justify=justify, cls=cls, wrap=wrap, p=p, s=s)

def sec_head(eb, h2, lead=None, align='center', tag='h2', cls=''):
    # gaps as in the HTML: eyebrow -> heading 14px, heading -> intro 18px
    ld = text(lead, 'fs-lead', align) if lead else None
    if ld: ld['settings']['_margin'] = {'unit': 'px', 'top': '4', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': False}
    kids = [eyebrow(eb, align) if eb else None, heading(h2, tag, '', align), ld]
    return con(*kids, gap_=14, cls=('fs-sec-head ' + cls).strip() if align == 'center' else cls, s={'max_width': px(880)} if align == 'center' else None)

# ---------- Hero ----------
def hero(eb, h1, lead, cta=('Let’s Talk!', '/contact-us/'), link=None, media=None, crumbs=None, pills=None, extra=None):
    left = [html(crumbs) if crumbs else None, html(pills) if pills else None, eyebrow(eb) if eb else None,
            heading(h1, 'h1', 'fs-h1-rule'), text(lead, 'fs-hero-lead')]
    btns = [button(cta[0], cta[1], 'fs-btn-lg')] if cta else []
    if btns: btns[0]['settings']['align_mobile'] = 'justify'   # full-width on phones, as in the HTML
    if link: btns.append(link_u(*link))
    if btns: left.append(row(*btns, gap_=28, s={'flex_direction_mobile': 'column', 'flex_align_items_mobile': 'stretch', 'flex_wrap': 'wrap', 'flex_gap_mobile': gap(18)}))
    if extra: left += extra
    return section(row(con(*[x for x in left if x], gap_=22), media or video('Watch the video'), cls='fs-hero', gap_=56),
                   cls='fs-geo', title='Hero', bg_img='assets/img/design/bg-geometric.jpg',
                   p={'unit': 'px', 'top': '90', 'right': '24', 'bottom': '100', 'left': '24', 'isLinked': False})

def vid(img='assets/img/design/chris-cutout.webp', caption='Watch the video', length='[2:00]', fit=None):
    """Hero video as in the design: navy panel, cover image, play button, "Video" tag and caption chip (all editable).
    Paste the YouTube link in the Video widget; the caption and length are the Text widget under it."""
    fit = fit or ('wide' if 'team-group' in img else 'cover' if 'case-' in img or 'course' in img else 'cut')
    v = video('', img, f'fs-w-video fs-w-video--{fit}')
    v['settings'].update({'aspect_ratio': '32', 'lightbox': '', 'show_play_icon': 'yes'})
    return con(v, text(f'<p><b>{caption}</b><span>{length}</span></p>', 'fs-w-cap'), cls='fs-w-vid fs-hero-vid')

# ---------- Trust band ----------
def trust(items):
    # as in the HTML: three equal columns, 24px apart, label 14px under the number, small gold star
    cells = [col(heading(n.replace('★', '<small class="fs-star">★</small>'), 'p', 'fs-trust-num', 'center'), text(l, 'fs-trust-label', 'center'),
                 wpct=round(100 / len(items), 2), gap_=14) for n, l in items]
    counter_js = html("<script>(function(){function run(){if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;document.querySelectorAll('.fs-trust-num .elementor-heading-title').forEach(function(h){if(h.getAttribute('data-fsc'))return;h.setAttribute('data-fsc','1');var t=h.firstChild;if(!t||t.nodeType!==3)return;var m=t.textContent.match(/^(\\\\d+(?:\\\\.\\\\d+)?)(.*)$/);if(!m)return;var end=parseFloat(m[1]),dec=(m[1].split('.')[1]||'').length,rest=m[2];t.textContent=(0).toFixed(dec)+rest;var io=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;io.disconnect();var t0=performance.now();(function tick(now){var p=Math.min((now-t0)/1400,1),k=1-Math.pow(1-p,3);t.textContent=(end*k).toFixed(dec)+rest;if(p<1)requestAnimationFrame(tick);})(t0);});},{threshold:.4});io.observe(h);});}if(document.readyState!=='loading')run();else document.addEventListener('DOMContentLoaded',run);})();</script>", 'fs-hidden-script')
    return section(row(*cells, gap_=24, justify='space-between', align='flex-start'), counter_js, cls='fs-dark fs-band', title='Trust band',
                   p={'unit': 'px', 'top': '52', 'right': '24', 'bottom': '56', 'left': '24', 'isLinked': False})

# ---------- Problem cards ("Sound familiar?") ----------
def problem(eb, h2, cards, close, art=None, numbered=False):
    """Problem section. cards: (icon file, title, text). numbered=True shows 1/2/3 tiles (service and stage pages),
    art: an image path, or a ready-made container for the left column."""
    if numbered:
        items = [con(row(html(f'<span class="fs-num-tile">{n}</span>'), con(heading(t, 'h3'), text(d), gap_=6, s={'flex_grow': 1}),
                         gap_=22, align='center', s={'flex_direction_mobile': 'row'}),
                     cls='fs-pcard fs-pcard-n', p=pad(22, 26)) for n, (i, t, d) in enumerate(cards, 1)]
    else:
        items = [image_box(f'assets/img/icons/{i}', t, d, 'fs-pcard') for i, t, d in cards]
    right = con(eyebrow(eb), heading(h2), *items, heading(close.replace('class="fs-sky"', 'class="fs-gt"'), 'p', 'fs-close'), gap_=16)
    if isinstance(art, dict):
        left = art
    else:
        left = con(image(art or 'assets/img/design/problem-art.png', '', '100%', alt=''))  # the illustration includes its own frame
    left['settings'].update({'width': PCT(39.5), 'width_mobile': PCT(100), 'flex_justify_content': 'center'})
    right['settings'].update({'width': PCT(56.6), 'width_mobile': PCT(100)})
    # phones: heading and cards first, illustration after (as in the HTML)
    return section(row(left, right, gap_=48, align='stretch', s={'flex_direction_mobile': 'column-reverse'}), cls='fs-geo', title='Problem', bg_img='assets/img/design/bg-geometric.jpg')

def art_card(top, h3, p_, stages):
    """Left card in the problem section of service / stage pages: icon or number, closing line, stage chips."""
    chips = ' '.join(f'<span class="fs-plogo-chip">{plogo(k, size=15)}</span>' for k in stages)
    return con(top, heading(h3, 'h3', '', 'center'), text(p_, '', 'center'), html(f'<p style="text-align:center">{chips}</p>'),
               cls='fs-gcard', p=pad(40, 32), gap_=14, align='center', justify='center')

# ---------- Framework (wheel + stage tabs) ----------
STAGES = {
 'brand':    ('Build a brand people trust on sight.', 'Your brand is the foundation everything else stands on. We define who you are, what makes you different, and how you show up, then make sure every touchpoint matches.', ['Brand strategy and messaging', 'Logo and visual identity', 'Website design and development', 'Brand video'], 'brand foundation', 'Explore brand and web services'),
 'thought':  ('Get found wherever customers look.', 'When someone needs what you do, you show up first: on Google, in the map pack, in AI answers and in their feed.', ['Local SEO and Google Business Profile', 'Paid search and social ads', 'Social media content', 'Local ties and community presence'], 'visibility', 'Explore SEO and advertising'),
 'choice':   ('Turn attention into booked business.', 'Visitors become leads and leads become customers, through clear offers, fast follow-up and campaigns built to convert.', ['Lead generation offers and landing pages', 'Retargeting campaigns', 'Marketing automation and follow-up', 'Conversion tracking'], 'conversion', 'Explore lead generation'),
 'referral': ('Make customers your best channel.', 'Happy customers become your sales team, with review systems, loyalty programs and referral campaigns that keep them coming back.', ['Review generation', 'Referral programs', 'Loyalty and retention campaigns', 'Customer email and SMS'], 'referral engine', 'Explore reviews and referrals'),
}
def stage_panel(k):
    h, d, items, quiz, link = STAGES[k]
    card = con(html(f'<span class="fs-plogo-chip">{plogo(k, size=30)}</span>'), heading(h, 'h3'), text(d),
               heading('What’s included', 'p', 'fs-eyebrow'), icon_list(items, cls='fs-checks'),
               text(f'<p><b>How strong is your {quiz}?</b> <a href="/framework-quiz/">Find out in the quiz.</a></p>', 'fs-soft-box'),
               link_u(link, f'/first{k}/'), cls='fs-gcard', p=pad(36), gap_=14)
    return con(card, p=pad(0))
def framework(eb='The FirstSearch Framework', h2='Marketing isn’t a pile of tactics. It’s a system.',
              lead='The businesses that win aren’t the ones with the biggest budgets. They’re the ones that show up at every stage, from the first time someone hears their name to the day that customer sends a friend their way. We call the owners who build that way FirstSearchers.',
              identity='Done with hacks and trends. Focused on building a brand that lasts. If that sounds like you, you’re already one of us.'):
    head = sec_head(eb, h2, lead)
    if identity:
        idt = text(f'<p><em>{identity}</em></p>', 'fs-identity', 'center')
        idt['settings']['_margin'] = {'unit': 'px', 'top': '8', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': False}
        head['elements'].append(idt)
    tabs = nested_tabs([(f'<span class="fs-plogo"><b>first</b>{k}</span>', stage_panel(k)) for k in STAGES], 'fs-stage-tabs')
    body = row(col(image('assets/img/framework-wheel.webp', '', '100%', 'center', 'The FirstSearch Framework wheel'), wpct=45),
               col(tabs, wpct=55), gap_=48)
    return section(head, body, button('Let’s Talk!', '/contact-us/', 'fs-btn-lg', 'center'),
                   cls='fs-dark fs-dark-round', title='Framework', gap_=40)

# ---------- Guarantee ----------
def guarantee():
    photo = col(image('assets/img/design/chris-cutout.webp', '', '100%', alt='Chris Mitchell, Owner and Digital Partner'),
                html('<blockquote class="fs-quote-chip">“I put our guarantee in writing because our clients deserve to know we’re as invested in their results as they are.”<cite>Chris Mitchell, Owner &amp; Digital Partner</cite></blockquote>'),
                wpct=31, gap_=0)
    copy = col(row(mobile_w(image('assets/img/design/guarantee-seal.webp', '', 140, alt='FirstSearch Guarantee: results in writing'), 90),
                   heading('Results, guaranteed.<br><span class="fs-gt">In writing.</span>', 'h2'), gap_=24, s={'flex_direction_mobile': 'row', 'flex_wrap_mobile': 'nowrap', 'flex_gap_mobile': gap(14)}),
               text('If we don’t deliver [the lead growth we commit to in your roadmap], [we keep working at no cost until we do].', 'fs-lead'),
               icon_list(['Fixed monthly retainer. No surprise invoices.', 'Six-month partnership, not a long lock-in.', 'Results defined up front, measured monthly.', 'Read the full guarantee terms.'],
                         'fas fa-check', 'fs-check-pills', links=['', '', '', '/guarantee-terms/']), wpct=65)
    photo['settings']['flex_justify_content'] = 'flex-end'   # photo sits on the section's bottom edge, copy starts at the top (as in the HTML)
    return section(row(photo, copy, gap_=48, align='stretch', s={'flex_direction_mobile': 'column-reverse'}), cls='fs-geo', title='Guarantee', bg_img='assets/img/design/bg-geometric.jpg')

# ---------- Stats band ----------
def stats(items):
    return section(row(*[col(counter(n, l, sfx, pre), wpct=23) for n, l, sfx, pre in items], justify='space-between'),
                   cls='fs-grad fs-stats', title='Stats', p={'unit': 'px', 'top': '64', 'right': '24', 'bottom': '64', 'left': '24', 'isLinked': False})

# ---------- Case study + reviews ----------
REVIEWS = [('“We contacted Chris at First Search after a bad experience with a national brand company. He was able to fix our website and get our Google profile up and running. Chris and his team are very professional and always did what was right for our success.”', 'Steven McGibbon'),
           ('“My business partner and I have been working with First Search for about six months and we were starting pretty much from ground zero with our marketing. We didn’t really even know where to start but the whole process has been easy and approachable and we couldn’t be happier with the results thus far.”', 'Patrick Wilson')]
def table(rows, head=('Metrics', 'Before', 'After')):
    """Before / after results table as an Essential Addons Data Table (editable in the panel).
    Cell CSS classes drive the design: m = metric name, b = before, ar = arrow, a = after (gradient)."""
    cols = [{'_id': uid(), 'eael_data_table_header_col': t, 'eael_data_table_header_css_class': c, 'eael_data_table_header_col_icon_enabled': 'false'}
            for t, c in ((head[0], 'm'), (head[1], 'b'), ('', 'ar'), (head[2], 'a'))]
    cells = []
    for m, bv, av in rows:
        cells.append({'_id': uid(), 'eael_data_table_content_row_type': 'row'})
        for txt, c in ((m, 'm'), (bv, 'b'), ('→', 'ar'), (av, 'a')):
            cells.append({'_id': uid(), 'eael_data_table_content_row_type': 'col', 'eael_data_table_content_type': 'textarea',
                          'eael_data_table_content_row_colspan': 1, 'eael_data_table_content_row_title': txt, 'eael_data_table_content_row_css_class': c})
    return w('eael-data-table', {'eael_data_table_header_cols_data': cols, 'eael_data_table_content_rows': cells,
                                 'table_alignment': 'center', 'eael_enable_responsive_header_styles': ''}, 'fs-dtable')
def testimonial(q, who, where='Posted on Google'):
    """Essential Addons Testimonial widget (stars on top, quote, name, source). Edit the text in the widget panel; the design comes from the fs-testi CSS."""
    return w('eael-testimonial', {'eael_testimonial_style': 'default-style', 'eael_testimonial_enable_avatar': '', 'image': {'url': '', 'id': ''},
                               'eael_testimonial_name': who, 'eael_testimonial_company_title': where, 'eael_testimonial_description': q,
                               'eael_testimonial_show_quote': '', 'eael_testimonial_enable_rating': 'yes', 'eael_testimonial_rating_number': 'rating-five',
                               'eael_testimonial_rating_position': 'top'}, 'fs-testi')
def review(q, who, where='Posted on Google'):
    """Google review card: the testimonial in a gradient-border card."""
    return con(testimonial(q, who, where), cls='fs-gcard fs-review-card', p=pad(34, 32, 30, 32))
def review_schema(items, business='First Search Marketing', url='https://befirstsearch.com/'):
    """Review structured data (JSON-LD) for the reviews shown on the page. Keep it in step with the review widgets."""
    data = {'@context': 'https://schema.org', '@type': 'ProfessionalService', 'name': business, 'url': url,
            'review': [{'@type': 'Review', 'author': {'@type': 'Person', 'name': who},
                        'reviewRating': {'@type': 'Rating', 'ratingValue': 5, 'bestRating': 5},
                        'reviewBody': q.strip('“”"'), 'publisher': {'@type': 'Organization', 'name': 'Google'}} for q, who in items]}
    return html('<script type="application/ld+json">' + _json.dumps(data, ensure_ascii=False) + '</script>', 'fs-hidden-script')
def case_reviews(client='[Client name] · [Industry, NH town]', h3='[From invisible on Google to booked out three weeks ahead]',
                 rows=(('Monthly leads', '12', '41'), ('Map pack position', '#9', '#1'), ('Google reviews', '18', '112')), schema=False):
    case = col(image('assets/img/design/case-dental.webp', 'fs-img-frame', '100%'),
               heading(client, 'p', 'fs-eyebrow'), heading(h3, 'h3'), table(rows), link_u('Read the full story', '/case-studies/'),
               wpct=56, cls='fs-purple-card fs-dark', p=pad(24), gap_=16)
    revs = col(*[review(q, n) for q, n in REVIEWS], link_u('Read all [XX] Google reviews', '#'), review_schema(REVIEWS) if schema else None, wpct=40, gap_=22)
    return section(row(case, revs, gap_=40, align='flex-start'), cls='fs-geo', title='Case study + reviews', bg_img='assets/img/design/bg-geometric.jpg')

# ---------- How it works ----------
STEP_ICONS = ['fas fa-search', 'fas fa-route', 'fas fa-cogs', 'fas fa-chart-line']
def steps(eb, h2, sub, items):
    """Numbered step cards, as in the HTML: line icon, optional label (e.g. "Days 1 to 14"), title and text, left-aligned.
    items: (title, text) or (label, title, text)."""
    cards = []
    for n, it in enumerate(items, 1):
        lab, t, d = it if len(it) == 3 else (None, *it)
        hl = n == len(items)   # last card: gradient, white text
        ic = w('icon', {'selected_icon': {'value': STEP_ICONS[(n - 1) % 4], 'library': 'fa-solid'}, 'align': 'left',
                        'primary_color': '#FFFFFF' if hl else '#3299D5', 'size': px(44)}, 'fs-step-icon')
        kids = [heading(str(n), 'p', 'fs-step-num'), ic]
        if lab: kids.append(heading(lab, 'p', 'fs-step-label'))
        kids += [heading(t, 'h3'), text(d)]
        cards.append(con(*kids, cls='fs-gcard fs-step' + (' fs-step-hl' if hl else ''), gap_=10, p=pad(64, 28, 32, 28),
                         animation='fadeInUp', animation_delay=(n - 1) * 350,
                         s={'width': PCT(round(100 / len(items)) - 3), 'width_mobile': PCT(100), 'margin_mobile': {'unit': 'px', 'top': '70', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': False}}))
    return section(sec_head(eb, h2, sub), row(*cards, gap_=56, align='stretch', cls='fs-steps', s={'flex_gap_tablet': gap(28)}),
                   cls='fs-dark', title='How it works', gap_=24)

# ---------- Three ways to work with us ----------
def three_ways(h2='Three ways to <span class="fs-gt">become a FirstSearcher</span>',
               lead='Work with our team, learn the system yourself, or get guided by us while you do the work.', eb='Work with us',
               spots_open=6):
    """'Three ways to work with us', built from native widgets so text, images, prices and videos are edited in the panel.
    Nested Tabs (tab titles: <i>number</i><span><b>title</b><small>subtitle</small></span>), each tab = intro column + gradient card.
    All of the look comes from the fs-ways CSS (section 29 of the Custom CSS)."""
    def intro(logo, logo_alt, h3, p_, vid_img, vid_fit, caption, length, extra=()):
        return con(image(logo, 'fs-w-logo' + (' fs-w-logo--sm' if logo.endswith('logo.png') else ''), None, 'left', logo_alt), heading(h3, 'h3', 'fs-w-h3'), text(p_, 'fs-w-lead'), *extra,
                   wvideo(vid_img, vid_fit, caption, length), gap_=16, cls='fs-w-intro')
    def wvideo(img, fit, caption, length):
        """Video widget with a cover image in a gradient frame, plus the caption chip and length (editable text)."""
        v = video('', img, f'fs-w-video fs-w-video--{fit}')
        v['settings'].update({'aspect_ratio': '32', 'lightbox': '', 'show_play_icon': 'yes'})
        return con(v, text(f'<p><b>{caption}</b><span>{length}</span></p>', 'fs-w-cap'), cls='fs-w-vid')
    def card(*kids):
        return con(*kids, cls='fs-gcard fs-w-card', gap_=0, p={'unit': 'px', 'top': '40', 'right': '40', 'bottom': '40', 'left': '40', 'isLinked': True},
                   s={'padding_tablet': pad(32), 'padding_mobile': pad(26)})
    def foot(p_html, label, url):
        return con(text(p_html, 'fs-w-foot-text'), button(label, url, 'fs-w-btn'), d='row', cls='fs-w-foot', gap_=gap(24, 14), wrap=True,
                   justify='space-between', align='center', mobile_col=False)
    def panel(left, right):
        return con(left, right, d='row', gap_=28, align='stretch', cls='fs-w-panel', mobile_col=False, s={'flex_direction_tablet': 'column'})

    # 1. Partner with our team
    spots = w('progress', {'title': '', 'percent': {'unit': '%', 'size': (25 - spots_open) * 4, 'sizes': []}, 'display_percentage': 'hide',
                           'inner_text': '', 'progress_type': ''}, 'fs-w-spots')
    spots_label = text(f'<p><b>{spots_open}</b> of 25 partner spots open.</p>', 'fs-w-spots-label')
    partner = panel(
        intro('assets/img/logo.png', 'First Search Marketing', 'We work with 25 businesses. That’s it.',
              'Capping our partner list means every client gets senior attention, real strategy and a team that knows their business. When the spots are full, they’re full.',
              'assets/img/design/team-group.webp', 'wide', 'Meet the team behind your marketing', '[1:45]',
              extra=(con(spots, spots_label, gap_=10, cls='fs-w-spotbox'),)),
        card(heading('Is a partnership right for you?', 'h3', 'fs-w-card-h'),
             con(con(heading('A fit if you:', 'h4'), icon_list(['Have an established business ready to grow', 'Want a long-term partner, not a vendor',
                                                               'Are ready to commit for six months', 'Care about leads and revenue, not likes'], 'fas fa-check', 'fs-w-list'),
                     cls='fs-w-fit fs-w-yes', gap_=10, p=pad(18, 18, 16, 18)),
                 con(heading('Not a fit if you:', 'h4'), icon_list(['Want overnight results', 'Are shopping for the cheapest option',
                                                                   'Want marketing done to you, not with you'], 'fas fa-times', 'fs-w-list'),
                     cls='fs-w-fit fs-w-no', gap_=10, p=pad(18, 18, 16, 18)),
                 d='row', gap_=14, align='stretch', cls='fs-w-fits'),
             icon_list(['Fixed monthly retainer', 'Six-month partnership', 'Results guaranteed in writing', 'A dedicated local team'], 'fas fa-check', 'fs-w-pills'),
             foot('<p>Partnerships start at <b>$X,XXX</b>/month.</p>', 'Let’s Talk!', '/contact-us/')))
    partner['settings']['_title'] = 'Partner with our team'

    # 2. Do it yourself
    def res(img, h, p_, link, url, price, icon=None):
        tile = con(w('icon', {'selected_icon': {'value': icon, 'library': 'fa-solid'}, 'primary_color': '#FFFFFF', 'size': px(40), 'align': 'center'}) if icon
                   else image(img, '', None, 'center'), cls='fs-w-img' + (' fs-w-img--ico' if icon else ''), justify='center', align='center')
        return con(tile, con(heading(h, 'h4'), text(p_), link_u(link, url), gap_=0, cls='fs-w-res-body'),
                   text(f'<p>{price}</p>', 'fs-w-price'), d='row', gap_=18, align='center', cls='fs-w-res', mobile_col=False)
    diy = panel(
        intro('assets/img/design/befirst-training.png', 'BeFirst Marketing Training', 'Learn the system. Run it yourself.',
              'The same framework we use with our partners, packaged so you can implement it at your own pace. Start with an $8 workbook, or get everything in the Community.',
              'assets/img/design/course-mockup.webp', 'cover', 'Inside BeFirst Training: how the DIY path works', '[3:10]'),
        card(heading('Your DIY resources', 'h3', 'fs-w-card-h'),
             con(res('assets/img/design/blueprint-book.webp', 'The FirstSearch Blueprint', 'The exact SOPs, worksheets and checklists we use with every client.', 'Get the Blueprint', '/befirst-training/#blueprint', '$8'),
                 res('assets/img/design/course-mockup.webp', 'BeFirst Online Course', 'A founder-led video walkthrough of the entire framework, one stage at a time.', 'Explore the course', '/befirst-training/#course', '[$XX]'),
                 res('assets/img/design/befirst-training.png', 'BeFirst Community', 'The course, Blueprint, live webinars and weekly content, all in one membership.', 'Join the Community', '/befirst-training/#community', '$88/mo'),
                 res(None, 'Live trainings and webinars', 'Hands-on workshops, online and in Hampton, on every stage of the framework.', 'See upcoming events', '/events/', '[Free to $XX]', icon='fas fa-users'),
                 gap_=0, cls='fs-w-reslist'),
             text('<p>Not sure where to start? <a href="/befirst-training/">Compare every option in BeFirst Training</a>.</p>', 'fs-w-more')))
    diy['settings']['_title'] = 'Do it yourself'

    # 3. Get guided by us
    def price_box(amount, note, cls):
        return text(f'<p><b>{amount}</b><span>/month</span></p><p><small>{note}</small></p>', 'fs-w-pbox ' + cls)
    coach = panel(
        intro('assets/img/design/befirst-coaching.png', 'BeFirst Marketing Coaching', 'You do the work. We guide every step.',
              '1:1 strategy sessions with our team, built entirely around your business. You implement; we bring the plan, the expertise and the accountability.',
              'assets/img/design/chris-cutout.webp', 'cut', 'What a BeFirst coaching session looks like', '[2:00]'),
        card(heading('BeFirst Coaching', 'h3', 'fs-w-card-h'),
             con(price_box('$500', 'One 1:1 session a month', 'fs-w-pbox--navy'), price_box('$1,000', 'A session every two weeks', 'fs-w-pbox--grad'),
                 d='row', gap_=12, align='stretch', cls='fs-w-pboxes'),
             icon_list(['A 1:1 strategy session with our team every month (or every two weeks)', 'A personalized action plan after each session',
                        'Accountability on what you committed to', 'Between-session support by email or chat [CONFIRM]',
                        'Includes the BeFirst Community at 50% off'], 'fas fa-check', 'fs-w-coach'),
             foot('<p><b>Best for:</b> owners who want an expert sounding board and accountability.</p>', 'Book a coaching call', '/befirst-training/#coaching')))
    coach['settings']['_title'] = 'Get guided by us'

    tt = lambda n, t, sub: f'<i>{n}</i><span><b>{t}</b><small>{sub}</small></span>'
    tabs = nested_tabs([(tt(1, 'Partner with our team', 'We build and run it for you, results guaranteed'), partner),
                        (tt(2, 'Do it yourself', 'BeFirst Training: learn the system at your pace'), diy),
                        (tt(3, 'Get guided by us', '1:1 coaching while you do the work'), coach)], 'fs-ways-tabs')
    tabs['settings']['breakpoint_selector'] = 'none'   # keep tabs on phones (stacked), as in the design
    head = sec_head(eb, h2, lead)
    return section(head, tabs, cls='fs-geo fs-ways', title='Three ways', bg_img='assets/img/design/bg-geometric.jpg', gap_=34,
                   p={'unit': 'px', 'top': '158', 'right': '24', 'bottom': '120', 'left': '24', 'isLinked': False},
                   s={'padding_tablet': {'unit': 'px', 'top': '112', 'right': '24', 'bottom': '92', 'left': '24', 'isLinked': False},
                      'padding_mobile': {'unit': 'px', 'top': '110', 'right': '16', 'bottom': '80', 'left': '16', 'isLinked': False}})

# ---------- FAQ ----------
def faq(h2, qas, eb='FAQ'):
    return section(sec_head(eb, h2), con(accordion(qas), s={'max_width': px(880), 'margin': {'unit': 'px', 'top': '0', 'right': 'auto', 'bottom': '0', 'left': 'auto', 'isLinked': False}}),
                   cls='fs-geo', title='FAQ', bg_img='assets/img/design/bg-geometric.jpg', gap_=32, align='center')

# ---------- Quiz callout ----------
def quiz(h2='Not sure which stage is holding you back?',
         lead='The free Framework Quiz scores your marketing across all four stages in about five minutes, then tells you exactly where to start.'):
    card = row(col(eyebrow('Free Framework Quiz'), heading(h2), text(lead, 'fs-lead'),
                   icon_list(['A score for each stage of the FirstSearch Framework', 'Your weakest stage, and what to fix first', 'Free, about five minutes, no sales call required'], cls='fs-checks'), wpct=55),
               col(image('assets/img/design/scorecard.png', '', '100%', alt='Sample FirstSearch scorecard'), button('Take the Framework Quiz', '/framework-quiz/', align='justify'),
                   text('<p>Sample scorecard. Yours is based on your answers.</p>', '', 'center'), wpct=42, gap_=14), cls='fs-gcard fs-quiz-card', gap_=48, p=pad(56), s={'padding_tablet': pad(40), 'padding_mobile': pad(28)})
    return section(card, cls='fs-geo', title='Quiz callout', bg_img='assets/img/design/bg-geometric.jpg')

# ---------- CTA banner above the footer ----------
def cta_banner(h2='Ready to unlock growth?', sub='[6] of 25 partner spots open. Let’s find out if you’re a fit.', label='Let’s Talk!', url='/contact-us/'):
    """Final call to action, as in the HTML: a gradient card pulled 110px up into the section above,
    with the footer purple behind its lower part (class fs-final). Spacing is set here, not in CSS."""
    card = con(con(heading(h2, 'h2', '', 'center'), text(sub, '', 'center'), gap_=10, align='center'),
               button(label, url, 'fs-btn-lg', 'center'),
               cls='fs-grad fs-cta-banner', gap_=26, align='center', p=pad(56, 86), s={'padding_tablet': pad(48, 48), 'padding_mobile': pad(40, 28)})
    sec = section(card, title='CTA banner', cls='fs-final', p={'unit': 'px', 'top': '0', 'right': '24', 'bottom': '0', 'left': '24', 'isLinked': False},
                  s={'margin': {'unit': 'px', 'top': '-110', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': False}, 'z_index': 2,
                     'padding_mobile': {'unit': 'px', 'top': '0', 'right': '16', 'bottom': '0', 'left': '16', 'isLinked': False}})
    return sec

def overlap_cta(label='Let’s Talk!', url='/contact-us/'):
    """Big button straddling the edge between two sections (HTML .cta-overlap): -46px margins, on top."""
    b = button(label, url, 'fs-btn-lg fs-btn-grad', 'center'); b['settings']['align_mobile'] = 'justify'   # gradient, as in the HTML
    return con(b, inner=False, boxed=True, title='Overlapping button', cls='fs-overlap',
               p={'unit': 'px', 'top': '0', 'right': '24', 'bottom': '0', 'left': '24', 'isLinked': False},
               s={'margin': {'unit': 'px', 'top': '-46', 'right': '0', 'bottom': '-46', 'left': '0', 'isLinked': False}, 'z_index': 3})

# ---------- Generic helpers ----------
def cards_grid(cards, per_row=3, gap_=24, cls='fs-gcard', p_=28):
    wp = {2: 48, 3: 31, 4: 23}[per_row]
    return row(*[col(*c, wpct=wp, cls=cls, p=pad(p_), gap_=12, align=None) for c in cards], gap_=gap_, align='stretch', wrap=True)


# ======================= Shared design blocks (match the approved HTML; look comes from the Custom CSS) =======================
# ---------- Comparison table (Essential Addons Data Table, class fs-cmp) ----------
CMP_ROWS = [  # label, icon (webp in assets/img/icons or line icon name), DIY, agency, First Search; "x" = no, "~" = it varies
    ('Strategy', 'roadmap', 'xWhatever there’s time to figure out', '~Often channel by channel, each service run separately', 'A framework-driven plan across every stage of the customer journey'),
    ('Results', 'growth.webp', 'xNot guaranteed', 'xRarely guaranteed', 'Guaranteed in writing'),
    ('Reporting', 'growth.webp', 'xUsually none', '~Varies, often impressions and clicks', 'Monthly, in plain English, tied to leads and revenue'),
    ('Who does the work', 'team.webp', '~One person, or you', '~Varies, often a rotating account team', 'A dedicated local team that knows your business'),
    ('Pricing', 'doc', '~Hourly, or your own time', '~Varies, add-ons are common', 'One fixed monthly retainer'),
    ('Commitment', 'handshake.webp', '~None', '~Varies by agency', 'Six-month partnership'),
    ('Your accounts and assets', 'trust.webp', 'You own them', '~Not always', 'You own them [CONFIRM]'),
    ('Attention', 'eye', 'xLimited by one person’s time', 'xNo cap on clients', 'Capped at 25 partners')]
def cmp_table(rows=CMP_ROWS):
    """Comparison table as an Essential Addons Data Table: every cell is editable in the panel (Content > row > cell).
    Cell CSS classes: k = what matters (navy), diy, ag, us (gradient). Marks: <span class="fs-mk fs-mk--no|mid|yes">."""
    MK = {'x': ('no', '✕'), '~': ('mid', '~'), 'y': ('yes', '✓')}
    head = [('What matters', 'k'), ('Freelancer or DIY', 'diy'), ('Typical agency', 'ag'), ('First Search Marketing', 'us')]
    cols = []
    for t, c in head:
        col_ = {'_id': uid(), 'eael_data_table_header_col': t, 'eael_data_table_header_css_class': c, 'eael_data_table_header_col_icon_enabled': 'false'}
        if c == 'us':
            col_.update({'eael_data_table_header_col_icon_enabled': 'true', 'eael_data_table_header_icon_type': 'image',
                         'eael_data_table_header_col_img': {'url': asset('assets/img/logo.png'), 'id': '', 'alt': 'First Search Marketing', 'source': 'library'},
                         'eael_data_table_header_col_img_size': 150})
        cols.append(col_)
    def cell(html_, c):
        return {'_id': uid(), 'eael_data_table_content_row_type': 'col', 'eael_data_table_content_type': 'editor', 'eael_data_table_content_row_colspan': 1,
                'eael_data_table_content_row_content': html_, 'eael_data_table_content_row_title': '', 'eael_data_table_content_row_css_class': c}
    cells = []
    for label, ico, diy, ag, us in rows:
        cells.append({'_id': uid(), 'eael_data_table_content_row_type': 'row'})
        tile = (f'<span class="fs-ct-tile"><img src="{asset("assets/img/icons/" + ico)}" alt="" /></span>' if ico.endswith('.webp')
                else f'<span class="fs-ct-tile fs-ct-tile--{ico}"></span>')
        cells.append(cell(f'<span class="fs-ct-k">{tile}<b>{label}</b></span>', 'k'))
        for v, c in ((diy, 'diy'), (ag, 'ag'), (us, 'us')):
            m = 'y' if c == 'us' else (v[0] if v[0] in 'x~' else 'y')
            t = v[1:] if v[0] in 'x~' else v
            cells.append(cell(f'<span class="fs-mk fs-mk--{MK[m][0]}">{MK[m][1]}</span><span>{t}</span>', c))
    return w('eael-data-table', {'eael_data_table_header_cols_data': cols, 'eael_data_table_content_rows': cells,
                                 'table_alignment': 'center', 'eael_enable_responsive_header_styles': ''}, 'fs-cmp')

# ---------- Framework stage cards (purple rounded block with the splash, four linked cards, overlapping button) ----------
STAGE_NAME = {'brand': 'FirstBrand', 'thought': 'FirstThought', 'choice': 'FirstChoice', 'referral': 'FirstReferral'}
def stage_cards(eb='Our framework', h2='A proven system, not a pile of tactics.',
                lead='The FirstSearch Framework makes sure your business is the one customers find, trust and choose first, at every stage of their journey.',
                btn=('Explore all services', '/services/'), title='Framework'):
    cards = []
    for n, k in enumerate(STAGES, 1):
        cards.append(con(heading(f'Stage {n}', 'p', 'fs-stage-n'), heading(plogo(k), 'h3', 'fs-rel-logo'), text(STAGES[k][0], 'fs-rel-p'),
                         heading(f'Explore {STAGE_NAME[k]}', 'p', 'fs-rel-why'),
                         cls='fs-gcard fs-rel', gap_=12, p=pad(28), s={'html_tag': 'a', 'link': {'url': f'/first{k}/', 'is_external': '', 'nofollow': ''}}))
    return section(sec_head(eb, h2, lead), row(*cards, gap_=24, align='stretch', wrap=True, cls='fs-rel-grid fs-nostyle'),
                   button(btn[0], btn[1], 'fs-btn-lg', 'center'), cls='fs-dark fs-fwblock', title=title, gap_=56,
                   p={'unit': 'px', 'top': '72', 'right': '24', 'bottom': '140', 'left': '24', 'isLinked': False},
                   s={'padding_tablet': {'unit': 'px', 'top': '64', 'right': '24', 'bottom': '110', 'left': '24', 'isLinked': False},
                      'padding_mobile': {'unit': 'px', 'top': '56', 'right': '16', 'bottom': '96', 'left': '16', 'isLinked': False}})

# ---------- Value / competency cards (navy cards, glowing white icon tile, "In practice" under a gradient line) ----------
def value_cards(items, cols=2):
    """items: (icon webp in assets/img/icons, title, text[, in practice])"""
    items = [(it + (None,))[:4] for it in items]
    return row(*[con(con(image(f'assets/img/icons/{i}', '', None, 'center', t), cls='fs-vtile', justify='center', align='center'),
                     con(heading(t, 'h3'), text(d, 'fs-vtext'), text(f'<p><em>In practice:</em> {p}</p>', 'fs-vip') if p else None, cls='fs-vbody', gap_=0),
                     d='row', cls='fs-vcard', gap_=24, align='flex-start', mobile_col=False, p=pad(24, 28, 26, 22), s={'padding_mobile': pad(20)})
                 for i, t, d, p in items], gap_=24, wrap=True, align='stretch', cls='fs-vcards fs-nostyle' + (' fs-vcards--3' if cols == 3 else ''))

# ---------- Ways to work with us: three priced paths on a "you do it / we do it" scale ----------
PATHS = [('Learn it yourself', 'BeFirst Community', '$88', '/month', ['The full online course', 'The FirstSearch Blueprint', 'Live monthly webinars', 'Weekly content and templates'],
          'you have time and want to learn the system.', ('See the Community', '/befirst-training/')),
         ('Build it with us', '1:1 Coaching', '$500', '/month and up', ['Everything in the Community', 'Strategy sessions with our team', 'A plan built around your business', 'Direct access between sessions'],
          'you’ll do the work but want an expert in your corner.', ('See coaching', '/befirst-training/#coaching')),
         ('Let us run it', 'Strategic partnership', '[$X,XXX]', '/month', ['Our team runs your marketing', 'Every stage of the framework', 'Monthly plain-English reporting', 'Results guaranteed in writing'],
          'you want it done right, without doing it yourself.', ('Let’s Talk!', '/contact-us/'))]
def paths(eb='Ways to work with us', h2='There’s an option <span class="fs-gt">for you.</span>',
          lead='Not ready for a partnership? Start where it makes sense and move up when you’re ready.', items=PATHS,
          quiz='<p>Not sure which fits? <a href="/framework-quiz/">Take the Framework Quiz</a> and we’ll point you to the right starting place.</p>'):
    scale = con(text('<p>You do the work</p>', 'fs-p2-end'), con(cls='fs-p2-bar'), text('<p>We do the work</p>', 'fs-p2-end'),
                d='row', gap_=14, align='center', mobile_col=False, cls='fs-p2-scale')
    cards = []
    for n, (k, h, pr, per, lst, who, b) in enumerate(items, 1):
        head = con(heading(str(n), 'p', 'fs-p2-n'), con(heading(k, 'p', 'fs-p2-k'), heading(h, 'h3', 'fs-p2-h'), gap_=4, cls='fs-p2-titles'),
                   d='row', gap_=14, align='center', mobile_col=False, cls='fs-p2-head')
        cards.append(con(head, heading(f'{pr}<small>{per}</small>', 'p', 'fs-p2-pr'), icon_list(lst, 'fas fa-check', 'fs-p2-list'),
                         text(f'<p><b>Best if:</b> {who}</p>', 'fs-p2-who'), button(b[0], b[1], 'fs-p2-btn'),
                         cls=f'fs-p2 fs-p2--{n}' + (' fs-dark' if n == 3 else ''), gap_=16, p=pad(30), s={'padding_mobile': pad(24)}))
    return section(sec_head(eb, h2, lead), scale, row(*cards, gap_=28, align='stretch', cls='fs-p2-grid fs-nostyle'), text(quiz, 'fs-p2-quiz', 'center'),
                   cls='fs-geo fs-paths', title='Paths', bg_img='assets/img/design/bg-geometric.jpg', gap_=26)

# ---------- Capacity band: "We work with 25 businesses" with the partner spots bar ----------
def capacity(h2='We work with 25 businesses. That’s it.',
             lead='Capping our partner list means every client gets senior attention and a team that knows their business.', spots_open=6):
    spots = w('progress', {'title': '', 'percent': {'unit': '%', 'size': (25 - spots_open) * 4, 'sizes': []}, 'display_percentage': 'hide',
                           'inner_text': '', 'progress_type': ''}, 'fs-cap-spots')
    return section(row(col(heading(h2, 'h2', 'fs-band-h fs-cap-h'), text(lead, 'fs-band-p'), wpct=60, gap_=14),
                       col(spots, text(f'<p><b>{spots_open}</b> of 25 partner spots open.</p>', 'fs-cap-label'), wpct=36, gap_=10),
                       gap_=40, justify='space-between', cls='fs-cap-row fs-nostyle'),
                   cls='fs-dark fs-band', title='Capacity', p={'unit': 'px', 'top': '56', 'right': '24', 'bottom': '56', 'left': '24', 'isLinked': False})


# ---------- Stage explorer: wheel + stage pills (Nested Tabs titles) | stage card with its services ----------
STAGE_DESC = {
    'brand': 'The foundation everything else stands on: who you are, how you look and sound, and the systems that track what’s working.',
    'thought': 'When someone needs what you sell, your business is the first name they see on Google, the map, AI answers and their feed.',
    'choice': 'Getting seen is half of it. These services turn visitors into leads and leads into booked customers.',
    'referral': 'Happy customers become your most trusted marketing channel, bringing themselves back and their friends with them.'}
WHEEL_FX = """<svg class="fs-wheel-svg" viewBox="0 0 1100 1100" aria-hidden="true"></svg>
<script>(function(){var sc=document.currentScript;if(!sc)return;function init(){var root=sc.closest('.fs-explorer');if(!root)return;var svg=sc.parentNode.querySelector('svg');
var C=550,RO=545,RI=168,NS='http://www.w3.org/2000/svg';function pt(r,a){var t=a*Math.PI/180;return (C+r*Math.sin(t)).toFixed(1)+' '+(C-r*Math.cos(t)).toFixed(1);}
function sec(a0,a1){return 'M'+pt(RO,a0)+'A'+RO+' '+RO+' 0 0 1 '+pt(RO,a1)+'L'+pt(RI,a1)+'A'+RI+' '+RI+' 0 0 0 '+pt(RI,a0)+'Z';}
function circ(r){return 'M'+(C-r)+' '+C+'a'+r+' '+r+' 0 1 0 '+(r*2)+' 0a'+r+' '+r+' 0 1 0 '+(-r*2)+' 0Z';}
var SH=[circ(RI),sec(0,118),sec(118,240),sec(240,360)];
function tabs(){return root.querySelectorAll('.e-n-tabs-heading .e-n-tab-title');}
function cur(){var t=tabs();for(var i=0;i<t.length;i++)if(t[i].getAttribute('aria-selected')==='true')return i;return 0;}
function path(d,c){var p=document.createElementNS(NS,'path');p.setAttribute('d',d);p.setAttribute('class',c);svg.appendChild(p);return p;}
function draw(){var a=cur();svg.innerHTML='';for(var i=0;i<4;i++)if(i!==a)path(SH[i],'fs-wz-soft');path(SH[a],'fs-wz-ring');
[1,2,3,0].forEach(function(i){var h=path(SH[i],'fs-wz-hit');h.addEventListener('click',function(){var t=tabs();if(t[i])t[i].click();});});}
draw();var hd=root.querySelector('.e-n-tabs-heading');if(hd&&window.MutationObserver)new MutationObserver(draw).observe(hd,{subtree:true,attributes:true,attributeFilter:['aria-selected']});}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();})();</script>"""
def stage_explorer(services, eb='The four stages', h2='Every service has a job in the customer journey.',
                   lead='Choose a stage to see what it does for your business and which services power it.', btn=('Let’s Talk!', '/contact-us/')):
    """services: (slug, name, icon, summary, stages). Nested Tabs: one tab per stage, its card lists the services that power it."""
    def card(k):
        rows = []
        for slug, n, i, _, st in [s for s in services if k in s[4]]:
            rows.append(con(con(image(f'assets/img/icons/{i}.webp', '', None, 'center', ''), cls='fs-ps-ico', justify='center', align='center'),
                            heading(n, 'p', 'fs-ps-n'), heading(f'{len(st)} stages', 'p', 'fs-ps-more') if len(st) > 1 else None,
                            d='row', gap_=14, align='center', mobile_col=False, cls='fs-ps-row',
                            s={'html_tag': 'a', 'link': {'url': f'/services/{slug}/', 'is_external': '', 'nofollow': ''}}))
        return con(heading(plogo(k), 'p', 'fs-ex-logo'), heading(STAGES[k][0], 'h3', 'fs-ex-h'), text(STAGE_DESC[k], 'fs-ex-desc'),
                   heading(f'Services that power {STAGE_NAME[k]}', 'p', 'fs-ex-label'), con(*rows, gap_=8, cls='fs-ps-list'),
                   button(f'Explore {STAGE_NAME[k]}', f'/first{k}/', 'fs-ex-btn'), cls='fs-gcard fs-ex-card', gap_=0)
    tabs = nested_tabs([(plogo(k), card(k)) for k in STAGES], 'fs-explorer-tabs')
    tabs['settings']['breakpoint_selector'] = 'none'
    wheel = con(image('assets/img/framework-wheel.webp', 'fs-wheel-img', '100%', 'center', 'The FirstSearch Framework wheel: firstbrand at the centre, surrounded by firstthought, firstchoice and firstreferral'),
                html(WHEEL_FX, 'fs-wheel-fx'), cls='fs-wheel')
    return section(sec_head(eb, h2, lead), con(wheel, tabs, cls='fs-explorer fs-nostyle'), button(btn[0], btn[1], 'fs-btn-lg', 'center'),
                   cls='fs-dark fs-fwblock', title='Framework explorer', gap_=56,
                   p={'unit': 'px', 'top': '72', 'right': '24', 'bottom': '140', 'left': '24', 'isLinked': False},
                   s={'_element_id': 'framework', 'padding_tablet': {'unit': 'px', 'top': '64', 'right': '24', 'bottom': '110', 'left': '24', 'isLinked': False},
                      'padding_mobile': {'unit': 'px', 'top': '56', 'right': '16', 'bottom': '96', 'left': '16', 'isLinked': False}})

# ---------- All services: native service cards + stage filter pills (small script; cards stay editable) ----------
SVC_FILTER = """<div class="fs-fpills" role="group" aria-label="Filter services by stage"></div><p class="fs-sv-count" aria-live="polite"></p>
<script>(function(){var sc=document.currentScript;if(!sc)return;function init(){var sec=sc.closest('.fs-allsvc');if(!sec)return;var grid=sec.querySelector('.fs-sv-grid');if(!grid)return;
var wrap=sc.parentNode,pills=wrap.querySelector('.fs-fpills'),count=wrap.querySelector('.fs-sv-count'),ORDER=['brand','thought','choice','referral'],LIMIT=6,filter='all',open=false;
var cards=[].slice.call(grid.children).filter(function(c){return c.classList.contains('fs-sv');});
cards.forEach(function(c){c._st=[].map.call(c.querySelectorAll('.fs-sv-pl .fs-plogo'),function(p){return p.textContent.trim().toLowerCase().replace(/^first/,'');});});
var more=document.createElement('div');more.className='fs-sv-more';more.innerHTML='<button type="button" aria-expanded="false"></button>';grid.parentNode.insertBefore(more,grid.nextSibling);
function logo(k){return '<span class="fs-plogo"><b>first</b>'+k+'</span>';}
function render(){var list=cards.filter(function(c){return filter==='all'||c._st.indexOf(filter)>-1;});var lim=filter==='all'&&!open?LIMIT:list.length;
cards.forEach(function(c){c.hidden=true;});list.forEach(function(c,i){c.hidden=i>=lim;});
pills.innerHTML=['all'].concat(ORDER).map(function(k){var n=k==='all'?cards.length:cards.filter(function(c){return c._st.indexOf(k)>-1;}).length;
return '<button type="button" class="fs-fpill" data-f="'+k+'" aria-pressed="'+(filter===k)+'">'+(k==='all'?'All services':logo(k))+'<span class="n">'+n+'</span></button>';}).join('');
count.textContent='Showing '+Math.min(lim,list.length)+' of '+cards.length+' services';
var b=more.querySelector('button');more.hidden=!(filter==='all'&&cards.length>LIMIT);b.textContent=open?'Show fewer services':'See more services ('+(cards.length-LIMIT)+' more)';b.setAttribute('aria-expanded',open);}
pills.addEventListener('click',function(e){var b=e.target.closest('.fs-fpill');if(!b)return;filter=b.getAttribute('data-f');open=false;render();});
more.addEventListener('click',function(e){if(!e.target.closest('button'))return;open=!open;render();});render();}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();})();</script>"""
SVC_ONE = {
    'branding-content-creation': 'Brand strategy, identity and content that make you recognizable everywhere.',
    'website': 'Fast, conversion-focused websites built to be found and to turn visitors into leads.',
    'analytics': 'Tracking and dashboards that show what’s working, in plain English.',
    'crm': 'One home for every lead and customer, set up so your team actually uses it.',
    'seo': 'Rank on Google, in the map pack and in AI search results.',
    'advertising': 'Google and Meta campaigns built around cost per lead, not clicks.',
    'social-media': 'Content that gets you found, chosen and talked about.',
    'local-ties': 'Partnerships, sponsorships and community presence that make you known offline.',
    'lead-generation': 'Offers, lead magnets and landing pages that turn interest into inquiries.',
    'marketing-automation': 'Follow-up, nurture and review requests that run on their own.',
    'loyalty': 'Programs that bring customers back again and again.',
    'reviews-referrals': 'Systems that turn happy customers into reviews and referrals.'}
def service_grid(services, eb='All services', h2='Twelve services. <span class="fs-gt">One connected system.</span>',
                 lead='Every service has a specific job in your customer journey. Filter by stage to see which services power it, or open any service to see exactly what’s included.'):
    """Each card is a linked container (icon, title, text, stage chips). The filter reads each card's stage chips,
    so adding a stage chip to a card is all it takes to list it under that stage."""
    cards = [con(image(f'assets/img/icons/{i}.webp', 'fs-sv-ico', None, 'left', ''), heading(n, 'h3', 'fs-sv-h'), text(SVC_ONE.get(slug, d), 'fs-sv-p'),
                 text('<p>' + ' '.join(f'<span class="fs-plogo-chip fs-plogo-chip--sm">{plogo(k)}</span>' for k in st) + '</p>', 'fs-sv-pl'),
                 cls='fs-sv', gap_=8, p=pad(24, 24, 22, 30), s={'html_tag': 'a', 'link': {'url': f'/services/{slug}/', 'is_external': '', 'nofollow': ''}})
             for slug, n, i, d, st in services]
    return section(sec_head(eb, h2, lead), html(SVC_FILTER, 'fs-sv-filter'), row(*cards, gap_=24, wrap=True, align='stretch', cls='fs-sv-grid fs-nostyle'),
                   cls='fs-geo fs-allsvc', title='All services', bg_img='assets/img/design/bg-geometric.jpg', gap_=0,
                   s={'_element_id': 'all-services'})

# ---------- Delivery band: copy + check chips | glass price box ----------
def delivery_band(eb='How it’s delivered', h2='No à la carte menu. One partnership, every service your plan needs.',
                  lead='Your strategy decides which services you need and in what order, starting with your weakest stage. Everything runs on one fixed monthly retainer, with results guaranteed in writing.',
                  chips=('Fixed monthly retainer', 'Six-month partnership', 'Guaranteed results'), price='From [$X,XXX]', per='per month', btn=('Let’s Talk!', '/contact-us/')):
    left = con(eyebrow(eb), heading(h2, 'h2', 'fs-band-h fs-cap-h'), text(lead, 'fs-band-p'), icon_list(list(chips), 'fas fa-check', 'fs-del-chips'), gap_=0, cls='fs-del-copy')
    box = con(heading(price, 'p', 'fs-pb-price'), text(per, 'fs-pb-per'), button(btn[0], btn[1], 'fs-btn-grad'), cls='fs-pricebox', align='center', gap_=0, p=pad(30))
    return section(con(left, box, d='row', gap_=40, align='center', cls='fs-del-row fs-nostyle'), cls='fs-dark fs-band', title='Delivery',
                   p={'unit': 'px', 'top': '80', 'right': '24', 'bottom': '80', 'left': '24', 'isLinked': False},
                   s={'padding_mobile': {'unit': 'px', 'top': '56', 'right': '16', 'bottom': '56', 'left': '16', 'isLinked': False}})


# ---------- Contact: "Find us" cards (navy, glowing icon tile, label, value, note, link) + map in a gradient frame ----------
def find_cards(items, eb='Find us', h2='Prefer to reach <span class="fs-gt">out directly?</span>', map_address=None):
    """items: (icon: webp in assets/img/icons or 'phone'/'clock' line icon, label, value, note, link text, url)"""
    cards = []
    for ico, k, v, note, go, url in items:
        tile = (con(image(f'assets/img/icons/{ico}', '', None, 'center', ''), cls='fs-fc-tile', justify='center', align='center') if ico.endswith('.webp')
                else con(cls=f'fs-fc-tile fs-fc-tile--{ico}'))
        kids = [tile, heading(k, 'p', 'fs-fc-k'), heading(v, 'p', 'fs-fc-v'), text(note, 'fs-fc-s')]
        if go:
            g = heading(go, 'p', 'fs-fc-go' + ('' if url else ' fs-fc-go--static'))
            # the footer link is stretched over the whole card (fs-card-link); the card itself is not an <a>,
            # which the browser would split into pieces around the widgets inside it
            if url: g['settings']['link'] = {'url': url, 'is_external': 'on' if url.startswith('http') else '', 'nofollow': ''}
            kids.append(g)
        cards.append(con(*kids, cls='fs-fcard' + (' fs-card-link' if url else ''), gap_=6, p=pad(28, 24, 28, 24)))
    kids = [sec_head(eb, h2), row(*cards, gap_=22, wrap=True, align='stretch', cls='fs-fcards fs-nostyle')]
    if map_address:
        kids.append(con(w('google_maps', {'address': map_address, 'zoom': px(14), 'height': px(340)}, 'fs-map'), cls='fs-gcard fs-map-card'))
    return section(*kids, cls='fs-geo', title='Find us', bg_img='assets/img/design/bg-geometric.jpg', gap_=36)

# ---------- Two "path" cards: navy card + gradient-border card (eyebrow, heading, text, button or links) ----------
def path_cards(left, right):
    """each: (eyebrow, heading, text, [(label, url, kind)]) - kind 'btn' or 'link'"""
    def card(spec, navy):
        k, h, p, actions = spec
        acts = [button(l, u, 'fs-pth-btn') if kind == 'btn' else link_u(l, u) for l, u, kind in actions]
        return con(heading(k, 'p', 'fs-pth-k'), heading(h, 'h3', 'fs-pth-h'), text(p, 'fs-pth-p'), con(*acts, gap_=12, cls='fs-pth-acts'),
                   cls=('fs-pth fs-pth--navy fs-dark' if navy else 'fs-gcard fs-pth'), gap_=12, p=pad(32, 30, 32, 30))
    return row(card(left, True), card(right, False), gap_=28, align='stretch', cls='fs-pths fs-nostyle')


# ======================= BeFirst Training blocks =======================
# ---------- Three-ways comparison (Essential Addons Data Table, class fs-wtbl; cell classes k / c1 / c2 / us) ----------
WAYS_ROWS = [
    ('Who does the work', '<b>You do</b>', '<b>You do, with a coach</b>', '<b>Our team does</b>'),
    ('Investment', '<b class="fs-wp">$88</b>/month<small>Or start with the $8 Blueprint</small>', '<b class="fs-wp">$500</b>/month<small>$1,000/month to meet every two weeks</small>',
     '<b class="fs-wp">[$X,XXX]</b>/month<small>Fixed retainer, six-month partnership</small>'),
    ('What’s included', 'Course, Blueprint, live webinars and weekly content', 'Everything in the Community, plus 1:1 strategy sessions', 'A full team running every stage, with monthly reporting'),
    ('Your time', '<span class="fs-wmeter"><i class="on"></i><i class="on"></i><i class="on"></i></span>The most', '<span class="fs-wmeter"><i class="on"></i><i class="on"></i><i></i></span>Moderate',
     '<span class="fs-wmeter"><i class="on"></i><i></i><i></i></span>The least'),
    ('Results guaranteed', '<span class="fs-wno">No</span>', '<span class="fs-wno">No</span>', '<span class="fs-wy">✓</span><b>Yes, in writing</b>'),
    ('Best for', 'Owners who like to learn, then do', 'Owners who want an expert sounding board and accountability', 'Owners who want it done right, without doing it themselves'),
    ('', '<a class="fs-wbtn" href="#community">See the Community</a>', '<a class="fs-wbtn" href="#coaching">See coaching</a>', '<a class="fs-wbtn fs-wbtn--white" href="#partnership">See the partnership</a>')]
def ways_table(rows=WAYS_ROWS):
    head = [('<span class="fs-ctag fs-ctag--k">What matters</span>', 'k'),
            ('<span class="fs-wh"><i>1</i><small class="fs-ctag fs-ctag--diy">You do it</small><b>Learn it yourself</b><em>BeFirst Community</em></span>', 'c1'),
            ('<span class="fs-wh"><i>2</i><small class="fs-ctag fs-ctag--ag">We do it together</small><b>Build it with us</b><em>1:1 Coaching</em></span>', 'c2'),
            ('<span class="fs-wh"><i>3</i><small class="fs-ctag fs-ctag--us">We do it for you</small><b>Let us run it</b><em>Strategic partnership</em></span>', 'us')]
    cols = [{'_id': uid(), 'eael_data_table_header_col': t, 'eael_data_table_header_css_class': c, 'eael_data_table_header_col_icon_enabled': 'false'} for t, c in head]
    def cell(h, c):
        return {'_id': uid(), 'eael_data_table_content_row_type': 'col', 'eael_data_table_content_type': 'editor', 'eael_data_table_content_row_colspan': 1,
                'eael_data_table_content_row_content': h, 'eael_data_table_content_row_title': '', 'eael_data_table_content_row_css_class': c}
    cells = []
    for r in rows:
        cells.append({'_id': uid(), 'eael_data_table_content_row_type': 'row'})
        for h, c in zip(r, ('k', 'c1', 'c2', 'us')): cells.append(cell(h, c + (' fs-wlast' if r[0] == '' else '')))
    return w('eael-data-table', {'eael_data_table_header_cols_data': cols, 'eael_data_table_content_rows': cells,
                                 'table_alignment': 'center', 'eael_enable_responsive_header_styles': ''}, 'fs-wtbl')

# ---------- Segmented price toggle (monthly / annual etc.). Edit the buttons' data in this HTML widget;
# the price and note are normal headings in the card (class fs-seg-price / fs-seg-note) ----------
def seg_toggle(options, dark=False):
    """options: [(label, price, unit, note, extra_badge)]"""
    btns = ''.join(f'<button type="button" aria-pressed="{"true" if n == 0 else "false"}" data-price="{p}" data-unit="{u}" data-note="{nt}">{l}'
                   + (f'<span class="fs-save">{x}</span>' if x else '') + '</button>' for n, (l, p, u, nt, x) in enumerate(options))
    js = ("<script>(function(){var s=document.currentScript;if(!s)return;var g=s.previousElementSibling;"
          "g.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;var box=g.closest('.fs-seg-scope');if(!box)return;"
          "[].forEach.call(g.querySelectorAll('button'),function(x){x.setAttribute('aria-pressed',x===b);});"
          "var p=box.querySelector('.fs-seg-price .elementor-heading-title'),n=box.querySelector('.fs-seg-note .elementor-heading-title');"
          "if(p)p.innerHTML=b.getAttribute('data-price')+'<small>'+b.getAttribute('data-unit')+'</small>';if(n)n.textContent=b.getAttribute('data-note');});})();</script>")
    return html(f'<div class="fs-seg{" fs-seg--dark" if dark else ""}" role="group">{btns}</div>{js}', 'fs-seg-w')

FEAT_ICONS = ['play', 'doc', 'live', 'mail', 'cal']
def community_block():
    feats = ['<b>The BeFirst online course,</b> <span>with new modules released over time</span>', '<b>The FirstSearch Blueprint,</b> <span>every SOP, worksheet and checklist</span>',
             '<b>Live webinars</b> <span>on every stage of the framework</span>', '<b>Weekly content,</b> <span>released to members before anyone else</span>',
             '<b>First notice of workshops and events,</b> <span>before seats open to the public</span>']
    flist = icon_list(feats, 'fas fa-check', 'fs-feat')
    for it, ic in zip(flist['settings']['icon_list'], FEAT_ICONS): it['_css_classes'] = ic
    left = con(image('assets/img/design/befirst-training.png', 'fs-comm-logo', None, 'left', 'BeFirst Marketing Training'),
               con(heading('The BeFirst Community', 'h3', 'fs-comm-h'), text('The full framework, the tools to apply it, and new content every week, all for one flat monthly rate.', 'fs-comm-p'), gap_=10),
               flist, cls='fs-comm-l', gap_=24, p=pad(52, 52, 52, 52), s={'padding_mobile': pad(30)})
    right = con(seg_toggle([('Monthly', '$88', '/month', 'Founding member rate', ''), ('Annual', '$880', '/year', 'Two months free, billed once a year', '2 months free')], dark=True),
                con(heading('$88<small>/month</small>', 'p', 'fs-seg-price fs-big-price'), heading('Founding member rate', 'p', 'fs-seg-note fs-price-note'), gap_=10),
                text('<p><b>Lock in the founding rate.</b> Join now and keep this price for as long as you stay. The rate goes up as the Community grows.</p>', 'fs-lock'),
                button('Join the Community', '#', 'fs-btn-white fs-btn-lg fs-full'), text('<p>[Cancel anytime. Access ends when your membership does.]</p>', 'fs-fine'),
                cls='fs-comm-r fs-dark fs-seg-scope', gap_=22, p=pad(52, 52, 52, 52), s={'padding_mobile': pad(30)})
    card = con(left, right, d='row', gap_=0, align='stretch', cls='fs-gcard fs-comm fs-nostyle')
    def piece(img_widget, kicker, h, p_, action):
        return con(con(img_widget, cls='fs-piece-img', justify='center', align='center'),
                   con(heading(kicker, 'p', 'fs-kicker'), heading(h, 'h4', 'fs-piece-h'), text(p_, 'fs-piece-p'), action, gap_=0, cls='fs-piece-body'),
                   d='row', gap_=24, align='center', cls='fs-gcard fs-piece fs-nostyle', p=pad(26))
    bp = piece(image('assets/img/design/blueprint-book.webp', '', None, 'center', 'The Marketing Blueprint workbook'), 'Included with the Community', 'The FirstSearch Blueprint',
               'The exact SOPs, worksheets and checklists we use with every client.',
               con(heading('$8', 'p', 'fs-amt'), button('Get the Blueprint', '#', 'fs-btn-navy'), d='row', gap_=20, align='center', mobile_col=False, cls='fs-piece-row'))
    wl = form([('email', 'Email address', True, 'you@business.com')], 'Join the waitlist', 'Book waitlist', 'fs-inline-form')
    wl['settings'].update({'show_labels': '', 'button_width': '40'}); wl['settings']['form_fields'][0]['width'] = '60'
    book = piece(text('<p><small>Coming soon</small><span>[Book title]</span><small>Chris Mitchell</small></p>', 'fs-book-ph'), 'Coming soon', '[Book title]',
                 'The FirstSearch Framework, told through real stories. Join the waitlist to hear first.', wl)
    return [card, heading('Or start with one piece', 'h3', 'fs-pieces-h'), row(bp, book, gap_=28, align='stretch', cls='fs-pieces fs-nostyle')]

def coaching_block(events):
    img = con(text('<p><i></i>1:1 strategy session</p>', 'fs-live'), image('assets/img/design/chris-cutout.webp', 'fs-coach-photo', None, 'center', 'Chris Mitchell, BeFirst coach'), cls='fs-coach-img')
    body = con(image('assets/img/design/befirst-coaching.png', 'fs-coach-logo', None, 'left', 'BeFirst Marketing Coaching'),
               con(heading('BeFirst Coaching', 'h3', 'fs-comm-h'), text('1:1 strategy sessions with our team, built entirely around your business. No course required. Every session works on your numbers, your plan and what’s next.', 'fs-comm-p'), gap_=10),
               seg_toggle([('Meet monthly', '$500', '/month', 'One 1:1 session a month', ''), ('Meet every two weeks', '$1,000', '/month', 'Two 1:1 sessions a month', '')]),
               con(heading('$500<small>/month</small>', 'p', 'fs-seg-price fs-big-price'), heading('One 1:1 session a month', 'p', 'fs-seg-note fs-coach-cad'),
                   d='row', gap_=gap(24, 10), align='flex-end', wrap=True, mobile_col=False, cls='fs-coach-price'),
               icon_list(['[XX]-minute 1:1 strategy sessions', 'A personalized action plan after each session', 'Accountability on what you committed to', '[Between-session support, e.g. email or chat]'],
                         'far fa-check-circle', 'fs-checks2'),
               text('<p><b>Coaching clients save 50% on the Community.</b> Add the course, Blueprint and weekly content for $44/month.</p>', 'fs-saver'),
               button('Book a coaching call', '#', 'fs-btn-navy fs-btn-lg'), cls='fs-coach-body fs-seg-scope', gap_=22, p=pad(48), s={'padding_mobile': pad(28)})
    card = con(img, body, d='row', gap_=0, align='stretch', cls='fs-gcard fs-coach fs-nostyle')
    def ws(k, m, d, wd, t, meta, fmt):
        tag = '<span class="fs-plogo-chip fs-plogo-chip--full">Full Framework</span>' if k == 'full' else f'<span class="fs-plogo-chip">{plogo(k)}</span>'
        return con(con(text(f'<p><small>{m}</small><b>{d}</b></p>', 'fs-datebox'), text(f'<p>{tag}</p>', 'fs-ws-tag'), d='row', gap_=14, align='center', mobile_col=False, cls='fs-ws-top'),
                   heading(t, 'h4', 'fs-ws-h'), text(f'<p>{meta}</p>', 'fs-ws-meta'), link_u('Reserve your seat', '/events/sample-event/' + ('?format=online' if fmt == 'online' else '')),
                   cls='fs-gcard fs-ws', gap_=12, p=pad(24))
    head = con(con(heading('Hands-on workshops', 'h3', 'fs-ws-head-h'), text('Work on your own business with our team in the room, online or in Hampton.', 'fs-ws-head-p'), gap_=6),
               link_u('See the full calendar', '/events/'), d='row', justify='space-between', align='flex-end', wrap=True, gap_=14, cls='fs-ws-head')
    return [card, head, row(*[ws(*e) for e in events], gap_=24, align='stretch', cls='fs-ws-grid fs-nostyle')]

def partner_block():
    main = con(con(image('assets/img/design/team-group.webp', 'fs-part-photo', None, 'center', 'The First Search Marketing team'), cls='fs-part-team'),
               eyebrow('Partner with our team'), heading('Your marketing, run by our team. Results guaranteed in writing.', 'h2', 'fs-part-h'),
               text('We work with 25 businesses. That’s it. Every partner gets real strategy, senior attention and a team that knows their business.', 'fs-part-p'),
               icon_list(['Fixed monthly retainer', 'Six-month partnership', 'Guaranteed results'], 'fas fa-check', 'fs-del-chips'),
               con(button('Book your strategy call', '/contact-us/', 'fs-btn-grad fs-btn-lg'), text('<p>From [$X,XXX]/month · [X] of 25 spots open</p>', 'fs-part-note'),
                   d='row', gap_=gap(22, 14), align='center', wrap=True, cls='fs-part-cta'),
               cls='fs-part-main fs-dark', gap_=0, p=pad(0, 56, 56, 56), s={'padding_mobile': pad(0, 28, 32, 28)})
    seal = con(image('assets/img/design/guarantee-seal.webp', 'fs-seal-img', None, 'center', 'FirstSearch Guarantee: results in writing'),
               con(heading('The FirstSearch Guarantee', 'h3', 'fs-seal-h'), text('If we don’t deliver [the lead growth in your roadmap], [we keep working at no cost until we do].', 'fs-seal-p'), gap_=8),
               d='row', gap_=20, align='center', mobile_col=False, cls='fs-gcard fs-seal-card', p=pad(26))
    rev = review(*REVIEWS[0]); rev['settings']['css_classes'] += ' fs-quote-card'
    side = con(seal, rev, gap_=24, cls='fs-part-side')
    return row(main, side, gap_=32, align='stretch', cls='fs-part fs-nostyle')


# ======================= Events page: filter band + featured event + workshop rows =======================
# Each workshop is a normal container (date box, stage chip, title, details, price, button). The filter script in the
# band reads each row's stage chip and its details line ("Online" / "In person"), so editing a row is all it takes.
EVENT_LIST = [  # stage, month, day, weekday, title, time, format, location, price, seats, desc, outcomes
    ('full', 'Oct', '22', 'Thursday', 'The FirstSearch Framework in 60 minutes', '12:00 to 1:00 PM', 'Online', 'Live on Zoom', 'Free', 'Open registration',
     'A fast, founder-led walkthrough of how the four stages fit together, and how to spot which one is holding your business back right now.',
     ['A clear picture of the full framework', 'Your weakest stage, identified', 'Three quick wins to try this week']),
    ('brand', 'Oct', '27', 'Tue', 'Build a brand people trust on sight', '12:00 to 1:30 PM', 'Online', 'Live on Zoom', '[Price]', '[XX] seats left',
     'Define what makes you different, write a value statement you can actually use, and audit every touchpoint for consistency.',
     ['A finished value statement', 'Your core values and competitive edge', 'A brand consistency checklist']),
    ('thought', 'Nov', '4', 'Wed', 'Get found first: local SEO and AI search', '12:00 to 1:30 PM', 'Online', 'Live on Zoom', '[Price]', '[XX] seats left',
     'How Google, the map pack and AI search tools decide who shows up first, and what you can fix in your profile and site this month.',
     ['A Google Business Profile tune-up list', 'Your top local keywords', 'An AI search visibility check']),
    ('full', 'Nov', '12', 'Thu', 'BeFirst Live: the full-day framework workshop', '9:00 AM to 4:00 PM', 'In person', '[Venue], Hampton, NH', '[Price]', '[XX] of [XX] seats left',
     'An immersive day working through every stage of the framework with our team. Bring your laptop and your real numbers. You leave with the plan finished, not homework.',
     ['A completed marketing roadmap', 'Your KPIs for every stage', 'Confidence to execute on Monday']),
    ('choice', 'Nov', '17', 'Tue', 'Turn your website into a lead machine', '8:30 to 10:30 AM', 'In person', '[Venue], Hampton, NH', '[Price]', '[XX] seats left',
     'Lead magnets, offers and follow-up that turn visitors into booked calls. We review real websites in the room, so bring yours.',
     ['A lead magnet idea and outline', 'An offer strategy that closes', 'A follow-up sequence map']),
    ('referral', 'Dec', '2', 'Wed', 'Reviews, referrals and loyalty that sell for you', '12:00 to 1:30 PM', 'Online', 'Live on Zoom', '[Price]', '[XX] seats left',
     'Build the systems that turn happy customers into your best marketing channel, without awkward asks.',
     ['A review request automation', 'A referral reward structure', 'A simple loyalty program outline']),
    ('thought', 'Dec', '8', 'Tue', 'Ads that actually pay for themselves', '12:00 to 1:30 PM', 'Online', 'Live on Zoom', '[Price]', '[XX] seats left',
     'How to plan, launch and measure Google and Meta ads around real leads and cost per acquisition, not impressions.',
     ['A campaign plan for one offer', 'The metrics that matter', 'A budget you can defend']),
    ('choice', 'Jan', '13', 'Wed', 'Marketing automation for busy owners', '12:00 to 1:30 PM', 'Online', 'Live on Zoom', '[Price]', '[XX] seats left',
     'The handful of automations every local business should have running, and how to set them up without a tech team.',
     ['Your first three automations mapped', 'Email list segments to build', 'A welcome journey outline'])]
# each workshop's page is /events/<slug>/ (pages_e.py builds them), in EVENT_LIST order
EVENT_SLUGS = ['framework-in-60-minutes', 'build-a-brand-people-trust', 'local-seo-and-ai-search', 'befirst-live-full-day-workshop',
               'website-lead-machine', 'reviews-referrals-loyalty', 'ads-that-pay-for-themselves', 'marketing-automation-for-busy-owners']
def event_url(e): return f'/events/{EVENT_SLUGS[EVENT_LIST.index(e)]}/' if e in EVENT_LIST else '/events/'
def stage_chip(k):
    return '<span class="fs-plogo-chip fs-plogo-chip--full">Full Framework</span>' if k == 'full' else f'<span class="fs-plogo-chip">{plogo(k)}</span>'

EV_FILTER_JS = """<div class="fs-evf"><div class="fs-evpills" role="group" aria-label="Framework stage"></div><div class="fs-evfrow"><div class="fs-seg fs-seg--dark fs-evformats" role="group" aria-label="Format"></div><p class="fs-evcount" aria-live="polite"></p></div></div>
<script>(function(){var sc=document.currentScript;if(!sc)return;function init(){var box=sc.parentNode,doc=document;
var items=[].slice.call(doc.querySelectorAll('.fs-evitem'));if(!items.length)return;
items.forEach(function(it){var c=it.querySelector('.fs-evchip');var t=c?c.textContent.trim().toLowerCase():'';it._st=t.indexOf('full')>-1?'full':t.replace(/^first/,'');
var m=it.querySelector('.fs-evmeta');var mt=m?m.textContent.toLowerCase():'';it._fm=mt.indexOf('in person')>-1?'inperson':'online';
var tg=it.querySelector('.fs-evtoggle');if(tg){tg.setAttribute('role','button');tg.setAttribute('tabindex','0');tg.setAttribute('aria-expanded','false');
function tog(){var open=!it.classList.contains('is-open');items.forEach(function(o){if(o!==it&&o.classList.contains('is-open')){o.classList.remove('is-open');var b=o.querySelector('.fs-evtoggle');if(b){b.setAttribute('aria-expanded','false');b.querySelector('.elementor-heading-title').textContent='Details';}}});
it.classList.toggle('is-open',open);tg.setAttribute('aria-expanded',open);tg.querySelector('.elementor-heading-title').textContent=open?'Hide details':'Details';}
tg.addEventListener('click',tog);tg.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();tog();}});}});
var empty=doc.querySelector('.fs-evempty'),more=doc.querySelector('.fs-evmore-h'),S={st:'all',fm:'all'};
var LBL={all:'All workshops',full:'Full Framework'};function lg(k){return LBL[k]||'<span class="fs-plogo"><b>first</b>'+k+'</span>';}
function render(){var byF=items.filter(function(i){return S.fm==='all'||i._fm===S.fm;});var list=byF.filter(function(i){return S.st==='all'||i._st===S.st;});
items.forEach(function(i){i.hidden=list.indexOf(i)<0;});
box.querySelector('.fs-evpills').innerHTML=['all','full','brand','thought','choice','referral'].map(function(k){var n=k==='all'?byF.length:byF.filter(function(i){return i._st===k;}).length;
return '<button type="button" class="fs-evpill" data-st="'+k+'" aria-pressed="'+(S.st===k)+'"><span>'+lg(k)+'</span><span class="n">'+n+'</span></button>';}).join('');
box.querySelector('.fs-evformats').innerHTML=[['all','All formats'],['online','Online'],['inperson','In person']].map(function(f){return '<button type="button" data-fm="'+f[0]+'" aria-pressed="'+(S.fm===f[0])+'">'+f[1]+'</button>';}).join('');
box.querySelector('.fs-evcount').textContent='Showing '+list.length+(list.length===1?' workshop':' workshops');
var rows=list.filter(function(i){return !i.classList.contains('fs-evfeat');});if(more)more.hidden=!rows.length;if(empty)empty.hidden=!!list.length;}
box.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;if(b.dataset.st)S.st=b.dataset.st;if(b.dataset.fm)S.fm=b.dataset.fm;render();});
if(empty)empty.addEventListener('click',function(e){if(e.target.closest('.fs-evclear')){e.preventDefault();S={st:'all',fm:'all'};render();}});
var tot=doc.querySelector('.fs-evtotal b');if(tot)tot.textContent=items.length;render();}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();})();</script>"""

def event_filter_band():
    return section(html(EV_FILTER_JS, 'fs-evfilter-w'), cls='fs-dark fs-band fs-evfilter', title='Workshop filter',
                   p={'unit': 'px', 'top': '24', 'right': '24', 'bottom': '24', 'left': '24', 'isLinked': False},
                   s={'padding_mobile': {'unit': 'px', 'top': '18', 'right': '16', 'bottom': '18', 'left': '16', 'isLinked': False}})

def featured_event(e):
    k, m, d, wd, t, tm, fm, loc, pr, seats, desc, outs = e
    fact = lambda a, b, c: text(f'<p class="k">{a}</p><p class="v">{b}</p><p class="s">{c}</p>', 'fs-fact')
    left = con(text(f'<p><span class="fs-chip-next">Next up</span> {stage_chip(k).replace("fs-plogo-chip", "fs-plogo-chip fs-evchip", 1)}</p>', 'fs-feat-chips'),
               heading(t, 'h2', 'fs-feat-h'), text(desc, 'fs-feat-desc'),
               con(fact('When', f'{wd}, {"October" if m == "Oct" else m} {d}', tm), fact('Where', fm, loc), fact('Investment', pr, seats), d='row', gap_=0, mobile_col=True, cls='fs-facts2'),
               text(f'<p>{fm} · {loc}</p>', 'fs-evmeta fs-sr'),
               con(button('Reserve your seat', event_url(e), 'fs-btn-navy fs-btn-lg'), button('Add to calendar', '#', 'fs-btn-grad fs-btn-lg fs-ical'),
                   d='row', gap_=10, wrap=True, cls='fs-feat-btns'),
               cls='fs-feat-l', gap_=22, p=pad(48), s={'padding_mobile': pad(28)})
    right = con(text(f'<p><b>{d}</b><span><span class="m">{m}</span><span class="w">{wd}</span></span></p>', 'fs-bigdate'),
                heading('You’ll leave with', 'h3', 'fs-feat-rh'), icon_list(outs, 'fas fa-check', 'fs-feat-checks'),
                cls='fs-feat-r fs-dark', gap_=18, p=pad(48), s={'padding_mobile': pad(28)})
    return con(left, right, d='row', gap_=0, align='stretch', cls='fs-gcard fs-evfeat fs-evitem fs-nostyle')

def event_row(e):
    k, m, d, wd, t, tm, fm, loc, pr, seats, desc, outs = e
    datebox = text(f'<p><span class="m">{m}</span><b>{d}</b><span class="w">{wd}</span></p>', 'fs-evdate')
    info = con(text(f'<p>{stage_chip(k).replace("fs-plogo-chip", "fs-plogo-chip fs-evchip", 1)}</p>', 'fs-evchip-w'), heading(t, 'h3', 'fs-ev-h'),
               text(f'<p>{tm} · {fm} · {loc}</p>', 'fs-evmeta'), gap_=6, cls='fs-evinfo')
    act = con(heading('Details', 'p', 'fs-evtoggle'),
              con(heading(pr, 'p', 'fs-evprice'), button('Reserve your seat', event_url(e), 'fs-btn-navy'),
                  text(f'<p>{seats}</p>', 'fs-evseats'), gap_=6, align='center', cls='fs-evbook'),
              d='row', gap_=18, align='center', mobile_col=False, cls='fs-evact')
    det = con(text(desc, 'fs-evdet-p'), con(heading('You’ll leave with', 'p', 'fs-evdet-h'), icon_list(outs, 'fas fa-check', 'fs-evdet-list'), gap_=10),
              d='row', gap_=32, cls='fs-evdet')
    return con(con(datebox, info, act, d='row', gap_=26, align='center', cls='fs-evrow-in', mobile_col=False), det, cls='fs-evitem fs-evrow', gap_=0)

def event_list(events=EVENT_LIST):
    empty = con(heading('No workshops match those filters right now', 'h2', 'fs-evempty-h'),
                text('Leave your email and we’ll let you know the moment the next one opens. Or clear your filters to see everything on the calendar.', 'fs-evempty-p'),
                form([('email', 'Email address', True, 'you@business.com')], 'Notify me', 'Workshop waitlist', 'fs-inline-form'),
                button('Clear filters', '#', 'fs-link-u fs-evclear'), cls='fs-gcard fs-evempty', gap_=18, align='center', p=pad(56, 28))
    empty['settings']['form_fields' if False else 'css_classes'] += ''
    f = empty['elements'][2]['settings']; f.update({'show_labels': '', 'button_width': '30'}); f['form_fields'][0]['width'] = '70'
    return section(featured_event(events[0]), heading('More upcoming <span class="fs-gt">workshops</span>', 'h2', 'fs-evmore-h', 'center'),
                   con(*[event_row(e) for e in events[1:]], gap_=18, cls='fs-evlist fs-nostyle'), empty,
                   cls='fs-geo', title='Workshops', bg_img='assets/img/design/bg-geometric.jpg', gap_=26,
                   p={'unit': 'px', 'top': '64', 'right': '24', 'bottom': '100', 'left': '24', 'isLinked': False}, s={'_element_id': 'calendar'})

def band_cta(h2, p_, btn, title):
    return section(row(col(heading(h2, 'h2', 'fs-band-h'), text(p_, 'fs-band-p'), wpct=65, gap_=8), button(btn[0], btn[1], 'fs-btn-grad fs-btn-lg'),
                       justify='space-between', s={'flex_align_items_mobile': 'flex-start'}), cls='fs-dark fs-band', title=title,
                   p={'unit': 'px', 'top': '48', 'right': '24', 'bottom': '48', 'left': '24', 'isLinked': False})

# ======================= Resources page: format tabs + search band, service sidebar, featured case study, cards =======================
RES_TYPES = {'blog': ('Blog', 'Read the article', '/blog/sample-post/'), 'case': ('Case study', 'Read the case study', '/case-studies/sample/'),
             'podcast': ('Podcast', 'Listen to the episode', '/podcast/sample/'), 'video': ('Video', 'Watch the video', '/videos/sample/')}
RES_GROUPS = [('brand', ['Branding & content', 'Website']), ('thought', ['SEO', 'Advertising', 'Social Media', 'Local Ties']),
              ('choice', ['Lead Generation', 'Marketing Automation', 'CRM']), ('referral', ['Loyalty', 'Reviews & Referrals']), ('', ['Analytics'])]
RES_ITEMS = [  # type, date label, meta, title, excerpt, tags, (metric, metric label)
    ('blog', 'Oct 9, 2026', '7 min read', 'Showing up in AI search: what local businesses need to know', 'AI tools are answering "who should I call?" questions. Here is how they decide which businesses to recommend.', ['SEO', 'Branding & content']),
    ('video', 'Oct 7, 2026', '10:24', 'The FirstSearch Framework in 10 minutes', 'Chris walks through all four stages and how they connect, with real examples from local businesses.', ['Branding & content', 'Lead Generation', 'Reviews & Referrals']),
    ('blog', 'Oct 6, 2026', '6 min read', 'Why your Google Business Profile matters more than your website', 'For most local searches, your profile is the first impression. Most owners have never touched theirs.', ['SEO', 'Local Ties']),
    ('case', 'Oct 5, 2026', '[Industry]', '[Client name]: from page three to the map pack', 'Rebuilding a Google profile and local SEO from the ground up.', ['SEO', 'Local Ties', 'Website'], ('[XX]%', '[More calls from Google]')),
    ('podcast', 'Oct 2, 2026', '[XX] min', 'Ep. [XX]: Strategy beats size', 'Why the smallest business in the market can still be the first one customers find.', ['Branding & content', 'Analytics']),
    ('video', 'Sep 30, 2026', '14:02', 'Setting up a CRM you will actually use', 'The simplest CRM setup for a local business, and the three fields that matter most.', ['CRM', 'Marketing Automation']),
    ('blog', 'Sep 29, 2026', '5 min read', 'Vanity metrics vs. growth metrics: what to actually track', 'Impressions feel good. Leads pay the bills. A plain-English guide to the numbers worth watching.', ['Analytics']),
    ('case', 'Sep 26, 2026', '[Industry]', '[Client name]: building a referral engine', 'Turning a loyal customer base into a steady stream of referrals.', ['Reviews & Referrals', 'Loyalty'], ('[XX]', '[New referrals per month]')),
    ('podcast', 'Sep 25, 2026', '[XX] min', 'Ep. [XX]: Local ties, the marketing that happens offline', 'Chambers, networking groups and community partners, and how to make them count.', ['Local Ties', 'Social Media']),
    ('blog', 'Sep 22, 2026', '8 min read', 'The five automations every local business should have running', 'Welcome, follow-up, review request, re-engagement and referral. What each one does and when it fires.', ['Marketing Automation', 'CRM']),
    ('video', 'Sep 18, 2026', '18:40', 'Building a Meta ad from scratch', 'Offer, audience, creative and tracking, start to finish in one sitting.', ['Advertising', 'Social Media']),
    ('blog', 'Sep 15, 2026', '4 min read', 'How to ask for reviews without feeling awkward', 'Timing, wording and the automation that does the asking for you.', ['Reviews & Referrals']),
    ('case', 'Sep 12, 2026', '[Industry]', '[Client name]: a rebrand and a new website', 'A full brand refresh and a site built to turn visitors into inquiries.', ['Branding & content', 'Website', 'Lead Generation'], ('[XX]%', '[More website inquiries]')),
    ('podcast', 'Sep 11, 2026', '[XX] min', 'Ep. [XX]: Turning customers into your sales team', 'Loyalty programs that local businesses can actually run.', ['Loyalty', 'Reviews & Referrals']),
    ('blog', 'Sep 8, 2026', '6 min read', 'Is your website a brochure or a lead machine?', 'Five signs your site is just sitting there, and what to change first.', ['Website', 'Lead Generation']),
    ('video', 'Sep 4, 2026', '11:15', 'Social posts that get engagement, not just likes', 'The post types that start conversations, and the ones to stop making.', ['Social Media', 'Branding & content']),
    ('case', 'Aug 29, 2026', '[Industry]', '[Client name]: paid ads that pay for themselves', 'Restructuring Google Ads around cost per lead instead of clicks.', ['Advertising', 'Lead Generation', 'Analytics'], ('[$XX]', '[Cost per lead]')),
    ('podcast', 'Aug 28, 2026', '[XX] min', 'Ep. [XX]: Why growth is a system', 'Improving the whole customer journey beats chasing one big win.', ['Marketing Automation', 'Analytics'])]
WAVE = '<svg aria-hidden="true" width="150" height="48" viewBox="0 0 150 48" fill="none"><g stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".9"><path d="M4 20v8M14 12v24M24 18v12M34 6v36M44 16v16M54 10v28M64 20v8M74 14v20M84 4v40M94 16v16M104 10v28M114 20v8M124 14v20M134 18v12M144 22v4"/></g></svg>'

def res_card(item):
    ty, dl, meta, t, ex, tags = item[:6]
    lab, cta, url = RES_TYPES[ty]
    if ty == 'blog': media = con(text('<p><span class="art"></span><span class="lbl">[Article image]</span></p>', 'fs-m-in'), cls='fs-media fs-m-blog')
    elif ty == 'case': media = con(text(f'<p><b>{item[6][0]}</b><span>{item[6][1]}</span></p>', 'fs-m-in'), cls='fs-media fs-m-case')
    elif ty == 'podcast': media = con(text(f'<p><span class="play"></span>{WAVE}</p>', 'fs-m-in'), cls='fs-media fs-m-pod')
    else: media = con(image('assets/img/design/chris-cutout.webp', 'fs-m-img', None, 'center', ''), text(f'<p><span class="play"></span><span class="dur">{meta}</span></p>', 'fs-m-in'), cls='fs-media fs-m-vid')
    sub = dl if ty == 'video' else f'{meta} · {dl}'
    body = con(text(f'<p><span class="fs-tpill fs-tpill--{ty}">{lab}</span><span>{sub}</span></p>', 'fs-ctype'), heading(t, 'h3', 'fs-rc-h'), text(ex, 'fs-rc-ex'),
               text('<p>' + ''.join(f'<span>{g}</span>' for g in tags) + '</p>', 'fs-ctags'), link_u(cta, url), gap_=10, cls='fs-rc-body', p=pad(22, 22, 24, 22))
    return con(media, body, gap_=0, cls='fs-gcard fs-rcard')

RES_JS = """<div class="fs-cats" role="group" aria-label="Format"></div>
<div class="fs-search"><label class="fs-sr" for="fs-res-q">Search resources</label><input id="fs-res-q" type="search" placeholder="Search by topic, like reviews or Google ads" autocomplete="off"></div>
<script>(function(){var sc=document.currentScript;if(!sc)return;function init(){var bar=sc.parentNode,doc=document,grid=doc.querySelector('.fs-rgrid');if(!grid)return;
var cards=[].slice.call(grid.querySelectorAll('.fs-rcard'));var side=doc.querySelector('.fs-rside-groups'),tools=doc.querySelector('.fs-rtools-w'),feat=doc.querySelector('.fs-rfeat'),
more=doc.querySelector('.fs-rmore'),empty=doc.querySelector('.fs-rempty'),PAGE=9;
var GROUPS=JSON.parse(side?side.getAttribute('data-groups')||'[]':'[]');
var MON={jan:0,feb:1,mar:2,apr:3,may:4,jun:5,jul:6,aug:7,sep:8,oct:9,nov:10,dec:11};
cards.forEach(function(c,i){var p=c.querySelector('.fs-tpill');c._ty=p?(p.className.match(/fs-tpill--(\\w+)/)||[])[1]:'';c._tags=[].map.call(c.querySelectorAll('.fs-ctags span'),function(s){return s.textContent.trim();});
c._txt=c.textContent.toLowerCase();var m=(c.querySelector('.fs-ctype')||c).textContent.match(/([A-Z][a-z]{2}) (\\d{1,2}), (\\d{4})/);c._d=m?new Date(+m[3],MON[m[1].toLowerCase()],+m[2]).getTime():-i;c._i=i;});
var S={cat:'all',tags:[],q:'',sort:'new',shown:PAGE};var TYPES=[['all','All'],['blog','Blogs'],['case','Case studies'],['podcast','Podcasts'],['video','Videos']];
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function render(){var q=S.q.trim().toLowerCase();var mQ=function(c){return !q||c._txt.indexOf(q)>-1;},mT=function(c){return !S.tags.length||c._tags.some(function(t){return S.tags.indexOf(t)>-1;});},
inC=function(c){return S.cat==='all'||c._ty===S.cat;};var base=cards.filter(function(c){return mQ(c)&&mT(c);});
var list=base.filter(inC).sort(function(a,b){return S.sort==='old'?a._d-b._d:b._d-a._d;});var tb=cards.filter(function(c){return mQ(c)&&inC(c);});
bar.querySelector('.fs-cats').innerHTML=TYPES.map(function(t){var n=t[0]==='all'?base.length:base.filter(function(c){return c._ty===t[0];}).length;
return '<button type="button" class="fs-cat" data-cat="'+t[0]+'" aria-pressed="'+(S.cat===t[0])+'"><span>'+t[1]+'</span><span class="n">'+n+'</span></button>';}).join('');
if(side)side.querySelector('.fs-rgroups').innerHTML=GROUPS.map(function(g){return '<div class="fs-grp"><p class="fs-grp-l">'+(g[0]?'<span class="fs-plogo"><b>first</b>'+g[0]+'</span>':'<span class="dot"></span>Across every stage')+'</p><div class="fs-tags">'+
g[1].map(function(t){var n=tb.filter(function(c){return c._tags.indexOf(t)>-1;}).length;return '<button type="button" class="fs-tag" data-tag="'+esc(t)+'" aria-pressed="'+(S.tags.indexOf(t)>-1)+'"><span>'+esc(t)+'</span><span class="n">'+n+'</span></button>';}).join('')+'</div></div>';}).join('');
if(side){side.querySelector('.fs-rclear').hidden=!S.tags.length;var sc2=side.querySelector('.fs-rside-n');if(sc2)sc2.textContent=S.tags.length||'';}
if(feat)feat.hidden=!(S.cat==='all'&&!S.tags.length&&!q);
if(tools){tools.querySelector('.fs-rcount').textContent='Showing '+Math.min(S.shown,list.length)+' of '+list.length+(list.length===1?' resource':' resources');
var act=[];if(S.cat!=='all')act.push(['cat','',TYPES.filter(function(t){return t[0]===S.cat;})[0][1]]);S.tags.forEach(function(t){act.push(['tag',t,t]);});if(q)act.push(['q','','"'+S.q.trim()+'"']);
var a=tools.querySelector('.fs-ractive');a.hidden=!act.length;a.innerHTML=act.length?'<span>Filtered by</span>'+act.map(function(x){return '<button type="button" class="fs-achip" data-rm="'+x[0]+'" data-v="'+esc(x[1])+'">'+esc(x[2])+' <span aria-hidden="true">✕</span></button>';}).join('')+'<button type="button" class="fs-textbtn" data-clear>Clear all</button>':'';}
cards.forEach(function(c){c.hidden=true;});list.forEach(function(c,i){c.hidden=i>=S.shown;grid.appendChild(c);});
if(more)more.hidden=!(list.length>S.shown);if(empty)empty.hidden=!!list.length;}
function clear(){S={cat:'all',tags:[],q:'',sort:S.sort,shown:PAGE};bar.querySelector('input').value='';render();}
doc.addEventListener('click',function(e){var b=e.target.closest('button,a');if(!b)return;
if(b.dataset.cat){S.cat=b.dataset.cat;S.shown=PAGE;render();}
else if(b.dataset.tag){var t=b.dataset.tag;S.tags=S.tags.indexOf(t)>-1?S.tags.filter(function(x){return x!==t;}):S.tags.concat([t]);S.shown=PAGE;render();}
else if(b.dataset.rm){if(b.dataset.rm==='cat')S.cat='all';if(b.dataset.rm==='tag')S.tags=S.tags.filter(function(x){return x!==b.dataset.v;});if(b.dataset.rm==='q'){S.q='';bar.querySelector('input').value='';}S.shown=PAGE;render();}
else if(b.hasAttribute('data-clear')||b.closest('.fs-rclear')||b.closest('.fs-rempty-btn')){e.preventDefault();if(b.closest('.fs-rclear')){S.tags=[];S.shown=PAGE;render();}else clear();}
else if(b.closest('.fs-rmore')){e.preventDefault();S.shown+=6;render();}
else if(b.closest('.fs-rside-toggle')){var sd=b.closest('.fs-rside');sd.classList.toggle('is-open');}});
bar.querySelector('input').addEventListener('input',function(e){S.q=e.target.value;S.shown=PAGE;render();});
var sel=doc.querySelector('.fs-rsort');if(sel)sel.addEventListener('change',function(e){S.sort=e.target.value;render();});render();}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();})();</script>"""

def resources_library(items=RES_ITEMS, groups=RES_GROUPS):
    import json as _j
    band = section(html(RES_JS, 'fs-cats-w'), cls='fs-dark fs-band fs-catsband', title='Resource tabs + search',
                   p={'unit': 'px', 'top': '0', 'right': '24', 'bottom': '0', 'left': '24', 'isLinked': False},
                   s={'padding_mobile': {'unit': 'px', 'top': '0', 'right': '16', 'bottom': '12', 'left': '16', 'isLinked': False}})
    side = con(html(f'<div class="fs-rside-groups" data-groups=\'{_j.dumps(groups)}\'><div class="fs-rside-head"><p class="fs-rside-t">Filter by service</p>'
                    '<button type="button" class="fs-rclear fs-textbtn" hidden>Clear</button></div>'
                    '<button type="button" class="fs-rside-toggle"><span>Filter by service <b class="fs-rside-n"></b></span><span class="chev" aria-hidden="true"></span></button>'
                    '<div class="fs-rgroups"></div></div>', 'fs-rside-w'),
               cls='fs-gcard fs-rside', p=pad(26, 22, 26, 22))
    feat = con(con(image('assets/img/design/case-dental.webp', 'fs-rfeat-img', None, 'center', ''),
                   text('<p><b>[XX]%</b><span>[Result metric, e.g. more calls from Google]</span><small>[Industry] · [Town], NH</small></p>', 'fs-rfeat-metric'), cls='fs-rfeat-l'),
               con(text('<p><span class="fs-chip-next">Featured case study</span></p>', 'fs-rfeat-badge'), heading('[Client name]: from page three to the map pack', 'h2', 'fs-rfeat-h'),
                   text('How a local business went from invisible on Google to the top three map results, and what that did for their phone.', 'fs-rfeat-p'),
                   button('Read the case study', '/case-studies/sample/', 'fs-btn-grad fs-btn-lg'), gap_=14, cls='fs-rfeat-r', p=pad(20, 40, 20, 40), s={'padding_mobile': pad(20, 8)}),
               d='row', gap_=0, align='stretch', cls='fs-rfeat fs-dark', p=pad(16))
    tools = html('<div class="fs-rtools-w"><div class="fs-rtools"><p class="fs-rcount" aria-live="polite"></p><label class="fs-sortbox">Sort <select class="fs-rsort">'
                 '<option value="new">Newest first</option><option value="old">Oldest first</option></select></label></div><div class="fs-ractive" hidden></div></div>', 'fs-rtools-x')
    grid = row(*[res_card(i) for i in items], gap_=24, wrap=True, align='stretch', cls='fs-rgrid fs-nostyle')
    more = button('Load more resources', '#', 'fs-btn-navy fs-btn-lg fs-rmore', 'center')
    empty = con(heading('Nothing matches those filters yet', 'h2', 'fs-evempty-h'), text('Try removing a tag or a word from your search. New resources go up every week.', 'fs-evempty-p'),
                button('Clear all filters', '#', 'fs-btn-navy fs-rempty-btn'), cls='fs-gcard fs-evempty fs-rempty', gap_=18, align='center', p=pad(56, 28))
    main = con(feat, tools, grid, more, empty, gap_=28, cls='fs-rmain')
    body = section(con(side, main, d='row', gap_=44, align='flex-start', cls='fs-rbody fs-nostyle'), cls='fs-geo', title='Resource library',
                   bg_img='assets/img/design/bg-geometric.jpg', p={'unit': 'px', 'top': '56', 'right': '24', 'bottom': '100', 'left': '24', 'isLinked': False},
                   s={'_element_id': 'library'})
    return [band, body]
