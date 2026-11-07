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

def vid(img='assets/img/design/chris-cutout.webp'):
    return con(video('', img, ''), cls='fs-gcard', p=pad(0), s={'overflow': 'hidden'})

# ---------- Trust band ----------
def trust(items):
    # as in the HTML: three equal columns, 24px apart, label 14px under the number, small gold star
    cells = [col(heading(n.replace('★', '<small class="fs-star">★</small>'), 'p', 'fs-trust-num', 'center'), text(l, 'fs-trust-label', 'center'),
                 wpct=round(100 / len(items), 2), gap_=14) for n, l in items]
    counter_js = html("<script>(function(){function run(){if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;document.querySelectorAll('.fs-trust-num .elementor-heading-title').forEach(function(h){if(h.getAttribute('data-fsc'))return;h.setAttribute('data-fsc','1');var t=h.firstChild;if(!t||t.nodeType!==3)return;var m=t.textContent.match(/^(\\\\d+(?:\\\\.\\\\d+)?)(.*)$/);if(!m)return;var end=parseFloat(m[1]),dec=(m[1].split('.')[1]||'').length,rest=m[2];t.textContent=(0).toFixed(dec)+rest;var io=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;io.disconnect();var t0=performance.now();(function tick(now){var p=Math.min((now-t0)/1400,1),k=1-Math.pow(1-p,3);t.textContent=(end*k).toFixed(dec)+rest;if(p<1)requestAnimationFrame(tick);})(t0);});},{threshold:.4});io.observe(h);});}if(document.readyState!=='loading')run();else document.addEventListener('DOMContentLoaded',run);})();</script>", 'fs-hidden-script')
    return section(row(*cells, gap_=24, justify='space-between'), counter_js, cls='fs-dark', title='Trust band',
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
                 rows=(('Monthly leads', '12', '41'), ('Map pack position', '#9', '#1'), ('Google reviews', '18', '112'))):
    case = col(image('assets/img/design/case-dental.webp', 'fs-img-frame', '100%'),
               heading(client, 'p', 'fs-eyebrow'), heading(h3, 'h3'), table(rows), link_u('Read the full story', '/case-studies/'),
               wpct=56, cls='fs-purple-card fs-dark', p=pad(24), gap_=16)
    revs = col(*[review(q, n) for q, n in REVIEWS], link_u('Read all [XX] Google reviews', '#'), review_schema(REVIEWS), wpct=40, gap_=22)
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
def cta_banner(h2='Ready to unlock growth?', sub='[6] of 25 partner spots open. Let’s find out if you’re a fit.', label='Let’s Talk!'):
    """Final call to action, as in the HTML: a gradient card pulled 110px up into the section above,
    with the footer purple behind its lower part (class fs-final). Spacing is set here, not in CSS."""
    card = con(con(heading(h2, 'h2', '', 'center'), text(sub, '', 'center'), gap_=10, align='center'),
               button(label, '/contact-us/', 'fs-btn-lg', 'center'),
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
