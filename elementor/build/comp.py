"""Shared page sections, matching the approved prototype."""
from fsel import *

PCT = lambda n: {'unit': '%', 'size': n, 'sizes': []}
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
    return section(row(*cells, gap_=24, justify='space-between'), cls='fs-dark', title='Trust band',
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
    right = con(eyebrow(eb), heading(h2), *items, heading(close, 'p', 'fs-close'), gap_=16)
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
    tabs = nested_tabs([(f'first{k}', stage_panel(k)) for k in STAGES], 'fs-stage-tabs')
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
                         'fas fa-check-circle', 'fs-check-pills', links=['', '', '', '/guarantee-terms/']), wpct=65)
    photo['settings']['flex_justify_content'] = 'flex-end'   # photo sits on the section's bottom edge, copy starts at the top (as in the HTML)
    return section(row(photo, copy, gap_=48, align='stretch', s={'flex_direction_mobile': 'column-reverse'}), cls='fs-geo', title='Guarantee', bg_img='assets/img/design/bg-geometric.jpg')

# ---------- Stats band ----------
def stats(items):
    return section(row(*[col(counter(n, l, sfx, pre), wpct=23, align='center') for n, l, sfx, pre in items], justify='space-between'),
                   cls='fs-grad', title='Stats', p={'unit': 'px', 'top': '64', 'right': '24', 'bottom': '64', 'left': '24', 'isLinked': False})

# ---------- Case study + reviews ----------
REVIEWS = [('“We contacted Chris at First Search after a bad experience with a national brand company. He was able to fix our website and get our Google profile up and running. Chris and his team are very professional and always did what was right for our success.”', 'Steven McGibbon'),
           ('“My business partner and I have been working with First Search for about six months and we were starting pretty much from ground zero with our marketing. We didn’t really even know where to start but the whole process has been easy and approachable and we couldn’t be happier with the results thus far.”', 'Patrick Wilson')]
def table(rows, head=('Metrics', 'Before', 'After')):
    t = f'<table class="fs-table"><thead><tr><th>{head[0]}</th><th class="b">{head[1]}</th><th aria-hidden="true"></th><th class="a">{head[2]}</th></tr></thead><tbody>'
    t += ''.join(f'<tr><th scope="row">{m}</th><td class="b">{b}</td><td class="ar">→</td><td class="a">{a}</td></tr>' for m, b, a in rows)
    return html(t + '</tbody></table>')
def review(q, who):
    return con(html(f'<div class="fs-review"><div class="fs-stars">★★★★★</div><blockquote>{q}</blockquote><cite>{who} <span>· Posted on Google</span></cite></div>'),
               cls='fs-gcard', p=pad(26))
def case_reviews(client='[Client name] · [Industry, NH town]', h3='[From invisible on Google to booked out three weeks ahead]',
                 rows=(('Monthly leads', '12', '41'), ('Map pack position', '#9', '#1'), ('Google reviews', '18', '112'))):
    case = col(image('assets/img/design/case-dental.webp', 'fs-img-frame', '100%'),
               heading(client, 'p', 'fs-eyebrow'), heading(h3, 'h3'), table(rows), link_u('Read the full story', '/case-studies/'),
               wpct=56, cls='fs-purple-card fs-dark', p=pad(24), gap_=16)
    revs = col(*[review(q, n) for q, n in REVIEWS], link_u('Read all [XX] Google reviews', '#'), wpct=40, gap_=22)
    return section(row(case, revs, gap_=40, align='flex-start'), cls='fs-geo', title='Case study + reviews', bg_img='assets/img/design/bg-geometric.jpg')

# ---------- How it works ----------
STEP_ICONS = ['fas fa-search', 'fas fa-route', 'fas fa-cogs', 'fas fa-chart-line']
def steps(eb, h2, sub, items):
    """Numbered step cards, as in the HTML: line icon, optional label (e.g. "Days 1 to 14"), title and text, left-aligned.
    items: (title, text) or (label, title, text)."""
    cards = []
    for n, it in enumerate(items, 1):
        lab, t, d = it if len(it) == 3 else (None, *it)
        hl = n == len(items)
        ic = w('icon', {'selected_icon': {'value': STEP_ICONS[(n - 1) % 4], 'library': 'fa-solid'}, 'align': 'left',
                        'primary_color': '#FFFFFF' if hl else '#3299D5', 'size': px(44)}, 'fs-step-icon')
        kids = [heading(str(n), 'p', 'fs-step-num'), ic]
        if lab: kids.append(heading(lab, 'p', 'fs-step-label'))
        kids += [heading(t, 'h3'), text(d)]
        cards.append(con(*kids, cls='fs-gcard fs-step' + (' fs-step-hl' if hl else ''), gap_=10, p=pad(64, 28, 32, 28),
                         s={'width': PCT(round(100 / len(items)) - 3), 'width_mobile': PCT(100), 'margin_mobile': {'unit': 'px', 'top': '70', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': False}}))
    return section(sec_head(eb, h2, sub), row(*cards, gap_=56, align='stretch', cls='fs-steps', s={'flex_gap_tablet': gap(28)}),
                   cls='fs-dark', title='How it works', gap_=24)

# ---------- Three ways to work with us ----------
def three_ways(h2='Three ways to <span class="fs-gt">become a FirstSearcher</span>',
               lead='Work with our team, learn the system yourself, or get guided by us while you do the work.', eb='Work with us'):
    partner = row(
        col(image('assets/img/logo.png', '', 220), heading('We work with 25 businesses. That’s it.', 'h3'),
            text('Capping our partner list means every client gets senior attention, real strategy and a team that knows their business. When the spots are full, they’re full.'),
            text('<p><b>[6]</b> of 25 partner spots open.</p>', 'fs-eyebrow'), vid('assets/img/design/team-group.webp'), wpct=46),
        col(heading('Is a partnership right for you?', 'h3'),
            row(col(heading('A fit if you:', 'h4'), icon_list(['Have an established business ready to grow', 'Want a long-term partner, not a vendor', 'Are ready to commit for six months', 'Care about leads and revenue, not likes'], cls='fs-checks'), wpct=50, cls='fs-purple-card fs-dark', p=pad(20), gap_=8),
                col(heading('Not a fit if you:', 'h4'), icon_list(['Want overnight results', 'Are shopping for the cheapest option', 'Want marketing done to you, not with you'], 'fas fa-times'), wpct=50, cls='fs-soft-box', p=pad(20), gap_=8), gap_=14, align='stretch'),
            icon_list(['Fixed monthly retainer', 'Six-month partnership', 'Results guaranteed in writing', 'A dedicated local team'], 'fas fa-check-circle', 'fs-check-pills'),
            row(text('<p>Partnerships start at <b>$X,XXX</b>/month.</p>'), button('Let’s Talk!', '/contact-us/'), justify='space-between', s={'flex_direction_mobile': 'column'}),
            wpct=54, cls='fs-gcard', p=pad(30), gap_=16), gap_=28, align='stretch')
    def wt_res(img, h, p_, link, url, price):
        return row(con(image(img, '', None, 'center'), cls='fs-wt-img'),
                   con(heading(h, 'h4'), text(p_), link_u(link, url), gap_=4, cls='fs-wt-body'),
                   html(f'<span class="fs-wt-price">{price}</span>'), gap_=18, cls='fs-wt-res', p=pad(16, 0, 16, 0), s={'flex_direction_mobile': 'row', 'flex_wrap_mobile': 'wrap'})
    diy = row(col(image('assets/img/design/befirst-training.png', '', 240), heading('Learn the system. Run it yourself.', 'h3'),
                  text('The same framework we use with our partners, packaged so you can implement it at your own pace. Start with an $8 workbook, or get everything in the Community.'),
                  video('', 'assets/img/design/course-mockup.webp', 'fs-video'), wpct=46, gap_=16),
              col(heading('Your DIY resources', 'h3'),
                  wt_res('assets/img/design/blueprint-book.webp', 'The FirstSearch Blueprint', 'The exact SOPs, worksheets and checklists we use with every client.', 'Get the Blueprint', '/befirst-training/#blueprint', '$8'),
                  wt_res('assets/img/design/course-mockup.webp', 'BeFirst Online Course', 'A founder-led video walkthrough of the entire framework, one stage at a time.', 'Explore the course', '/befirst-training/#course', '[$XX]'),
                  wt_res('assets/img/design/befirst-training.png', 'BeFirst Community', 'The course, Blueprint, live webinars and weekly content, all in one membership.', 'Join the Community', '/befirst-training/#community', '$88/mo'),
                  wt_res('assets/img/icons/team.webp', 'Live trainings and webinars', 'Hands-on workshops, online and in Hampton, on every stage of the framework.', 'See upcoming events', '/events/', '[Free to $XX]'),
                  text('<p>Not sure where to start? <a href="/befirst-training/">Compare every option in BeFirst Training</a>.</p>', 'fs-wt-more'),
                  wpct=54, cls='fs-gcard', p=pad(30), gap_=0), gap_=28, align='stretch')
    coach = row(col(image('assets/img/design/befirst-coaching.png', '', 240), heading('You do the work. We guide every step.', 'h3'),
                    text('1:1 strategy sessions with our team, built entirely around your business. You implement; we bring the plan, the expertise and the accountability.'),
                    video('', 'assets/img/design/chris-cutout.webp', 'fs-video'), wpct=46, gap_=16),
                col(heading('BeFirst Coaching', 'h3'),
                    html('<div class="fs-coach-price"><div><b>$500</b><span>/month</span><small>One 1:1 session a month</small></div><div><b>$1,000</b><span>/month</span><small>A session every two weeks</small></div></div>'),
                    icon_list(['A personalized action plan after each session', 'Between-session support by email or chat [CONFIRM]', 'Includes the BeFirst Community at 50% off'], cls='fs-checks'),
                    text('<p><b>Best for:</b> owners who want an expert sounding board and accountability.</p>'),
                    button('Book a coaching call', '/befirst-training/#coaching'), wpct=54, cls='fs-gcard', p=pad(30), gap_=16), gap_=28, align='stretch')
    tabs = nested_tabs([('1 · Partner with our team', con(partner, p=pad(0))), ('2 · Do it yourself', con(diy, p=pad(0))), ('3 · Get guided by us', con(coach, p=pad(0)))], 'fs-ways-tabs')
    return section(sec_head(eb, h2, lead), tabs, cls='fs-geo', title='Three ways', bg_img='assets/img/design/bg-geometric.jpg', gap_=32)

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
    b = button(label, url, 'fs-btn-lg', 'center'); b['settings']['align_mobile'] = 'justify'
    return con(b, inner=False, boxed=True, title='Overlapping button', cls='fs-overlap',
               p={'unit': 'px', 'top': '0', 'right': '24', 'bottom': '0', 'left': '24', 'isLinked': False},
               s={'margin': {'unit': 'px', 'top': '-46', 'right': '0', 'bottom': '-46', 'left': '0', 'isLinked': False}, 'z_index': 3})

# ---------- Generic helpers ----------
def cards_grid(cards, per_row=3, gap_=24, cls='fs-gcard', p_=28):
    wp = {2: 48, 3: 31, 4: 23}[per_row]
    return row(*[col(*c, wpct=wp, cls=cls, p=pad(p_), gap_=12, align=None) for c in cards], gap_=gap_, align='stretch', wrap=True)
