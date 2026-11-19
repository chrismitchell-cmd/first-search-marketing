"""Case study page (case-study-progressive-dental.html), built only from native Elementor widgets so every word,
number and image is editable in Elementor. One function, any client: the content comes from a dict in
case_studies.py. Light (geometric) and purple sections alternate down the page."""
from comp import *
from pages_a import GEO

def H(t, cls, tag='p', url=None, align=None):
    h = heading(t, tag, cls, align)
    if url: h['settings']['link'] = {'url': url, 'is_external': '', 'nofollow': ''}
    return h
def ns(*kids, cls='', **kw):
    """Container whose widgets keep their own CSS look (the build's typography pass skips fs-nostyle)."""
    return con(*kids, cls=(cls + ' fs-nostyle').strip(), **kw)
def img(path, alt='', cls=''):
    """An image, or the "replace with your image" placeholder when path is None."""
    return image(path or 'assets/img/case/placeholder.webp', cls, '100%', 'center', alt or ('Replace with your image' if not path else ''))
def arrow(): return H('→', 'fs-cs-arrow', align='center')
def kpis(items):
    return ns(*[con(H(n, 'fs-cs-kpi-n', align='center'), H(l, 'fs-cs-kpi-l', align='center'), gap_=4, cls='fs-cs-kpi', p=pad(16, 12)) for n, l in items],
              d='row', gap_=10, align='stretch', cls='fs-cs-kpis', mobile_col=True)

def proof_panel(t):
    k = t['kind']
    if k == 'rows':        # e.g. branding: logo, business cards, signage, each before -> after
        vis = [ns(H('Before', 'fs-cs-cap'), H('', 'fs-cs-cap'), H('After', 'fs-cs-cap'), d='row', gap_=12, mobile_col=False, cls='fs-cs-ba-head')]
        for label, b, a in t['rows']:
            vis.append(ns(ns(con(img(b), cls='fs-cs-imgbox is-before'), arrow(), con(img(a), cls='fs-cs-imgbox'), d='row', gap_=12, align='center', cls='fs-cs-ba'),
                          H(label, 'fs-cs-ba-label', align='center'), gap_=6))
    elif k == 'pair':      # e.g. SEO heatmap exports
        vis = [ns(*[con(H(lab, 'fs-cs-cap'), con(img(im), cls='fs-cs-imgbox'), gap_=8) for lab, im in zip(t['labels'], t['images'])], d='row', gap_=16, cls='fs-cs-pair')]
    elif k == 'rating':    # Google rating before -> now
        def card(lab, score, cnt, before):
            return con(H(lab, 'fs-cs-cap'), H(t.get('name', 'Google rating'), 'fs-cs-rate-name'), H(f'{score} <span>{"★★★★☆" if before else "★★★★★"}</span>', 'fs-cs-rate-score'),
                       H(f'{cnt} Google reviews', 'fs-cs-rate-cnt'), gap_=4, cls='fs-cs-rate' + (' is-before' if before else ''), p=pad(18))
        vis = [ns(card(*t['before'], True), arrow(), card(*t['after'], False), d='row', gap_=12, align='center', cls='fs-cs-ba')]
    elif k == 'leads':     # leads a month before -> now, and where they come from
        def box(lab, n, before):
            return con(H(lab, 'fs-cs-cap', align='center'), H(n, 'fs-cs-lead-n', align='center'), H('digital leads a month', 'fs-cs-lead-l', align='center'),
                       gap_=2, cls='fs-cs-leadbox' + (' is-before' if before else ''), p=pad(16))
        rows = [ns(H(name, 'fs-cs-src-name'), con(con(cls='fs-cs-src-fill', s={'width': PCT(wd)}), cls='fs-cs-src-track'), H('[XX]', 'fs-cs-src-n'),
                   d='row', gap_=12, align='center', mobile_col=False, cls='fs-cs-src') for name, wd in t['sources']]
        vis = [ns(box('Before', t['before'], True), arrow(), box('Now', t['after'], False), d='row', gap_=12, align='center', cls='fs-cs-ba'),
               H('Where new-patient leads come from now [last 90 days, set the bar widths and numbers]', 'fs-cs-src-h'), con(*rows, gap_=10)]
    elif k == 'browser':   # website screenshots in browser frames
        vis = [ns(*[con(H(lab, 'fs-cs-bbar'), img(im), gap_=0, cls='fs-cs-browser' + (' is-before' if n == 0 else '')) for n, (lab, im) in enumerate(zip(('Before', 'After'), t['images']))],
                  d='row', gap_=14, align='flex-end', cls='fs-cs-pair')]
    else:                  # 'phone': social posts in phone frames
        p0, p1 = t['images']
        vis = [ns(con(H('Before', 'fs-cs-pcap', align='center'), img(p0), gap_=6, cls='fs-cs-phone is-before', p=pad(10)), arrow(),
                  con(H('After', 'fs-cs-pcap', align='center'), img(p1), gap_=6, cls='fs-cs-phone', p=pad(10)), d='row', gap_=14, align='center', cls='fs-cs-ba')]
    copy = con(heading(t['h3'], 'h3', 'fs-cs-ph3'), text(t['p'], 'fs-cs-pp'), kpis(t['kpis']), gap_=14)
    return con(row(con(*vis, gap_=14, s={'width': PCT(55), 'width_mobile': PCT(100)}), con(copy, s={'width': PCT(41), 'width_mobile': PCT(100)}), gap_=40),
               cls='fs-gcard fs-cs-panel', p=pad(32), s={'padding_mobile': pad(20)})

def case_study_page(c):
    name = c['client']
    # 1. hero (light)
    stages = ns(*[H(plogo(k), 'fs-cs-stage', url=f'/first{k}/') for k in c['stages']], d='row', gap_=10, wrap=True, mobile_col=False, cls='fs-cs-stages')
    left = con(ns(H('← All case studies', 'fs-cs-back', url='/resources/'), gap_=0),
               ns(H('Case study', 'fs-cs-type'), H(f'{c["industry"]} · {c["location"]}', 'fs-cs-meta'), d='row', gap_=10, align='center', mobile_col=False, wrap=True),
               heading(f'{c["h1"][0]} <span class="fs-gt">{c["h1"][1]}</span>', 'h1', 'fs-h1-rule'), text(c['lead'], 'fs-hero-lead'),
               ns(H('Framework stages in this project', 'fs-cs-k'), stages, gap_=10), gap_=18)
    photo = con(image(c['photo'], 'fs-cs-photo-img', '100%', 'center', c['photo_alt']),
                ns(image(c['logo'], 'fs-cs-logo-img', None, 'left', f'{name} logo'), H(f'Partner since {c["since"]}', 'fs-cs-since'), d='row', gap_=12, align='center',
                   mobile_col=False, cls='fs-cs-logo'), cls='fs-gcard fs-cs-photo', p=pad(0))
    hero = section(row(left, photo, cls='fs-hero', gap_=56), cls='fs-geo', title='Hero', bg_img=GEO,
                   p={'unit': 'px', 'top': '90', 'right': '24', 'bottom': '100', 'left': '24', 'isLinked': False})

    # 3. the client + goals (light)
    story = [eyebrow('The client'), heading(f'Meet {name.rsplit(" ", 1)[0]} <span class="fs-gt">{name.rsplit(" ", 1)[1]}.</span>', 'h2'), text(c['about']),
             heading('Where they were', 'h3'), text(c['before'])]
    if c.get('quote'):
        story += [text(f'<p>“{c["quote"][0]}”</p>', 'fs-cs-pull'), H(c['quote'][1], 'fs-cs-pull-by')]
    facts = [('Client', name), ('Industry', c['industry']), ('Location', c['location']), ('Partnership', c['partnership'])]
    glance = con(H('At a glance', 'fs-cs-glance-k'),
                 *[ns(H(k, 'fs-cs-dt'), H(v, 'fs-cs-dd'), gap_=2, cls='fs-cs-fact') for k, v in facts],
                 ns(H('Services', 'fs-cs-dt'), icon_list(c['services_short'], '', 'fs-cs-pills'), gap_=6, cls='fs-cs-fact'),
                 button('Get results like these', '/contact-us/', align='justify'), cls='fs-gcard fs-cs-glance', gap_=10, p=pad(26))
    goals = value_cards(c['goals'], 3, label='Target'); goals['settings']['css_classes'] += ' fs-cs-goals'   # icon on top, as in the design
    client = section(row(con(*story, gap_=16, s={'width': PCT(62), 'width_mobile': PCT(100)}), con(glance, s={'width': PCT(34), 'width_mobile': PCT(100)}),
                         gap_=48, align='flex-start'),
                     sec_head('The goals', c['goals_h2']), goals,
                     cls='fs-geo', title='The client', bg_img=GEO, gap_=40)

    # 4. the plan (purple framework block, overlapping button)
    cards = []
    for n, k in enumerate(STAGES, 1):
        on, off = c['plan'].get(k, ([], []))
        cards.append(con(H(f'Stage {n}', 'fs-stage-n'), heading(plogo(k), 'h3', 'fs-rel-logo'), text(STAGES[k][0], 'fs-rel-p'),
                         icon_list(on, 'fas fa-check', 'fs-cs-svcs') if on else None,
                         icon_list(off, 'far fa-circle', 'fs-cs-svcs fs-cs-svcs--off') if off else None,
                         H(f'Explore {STAGE_NAME[k]}', 'fs-rel-why', url=f'/first{k}/'), cls='fs-gcard fs-rel fs-cs-plan-card', gap_=12, p=pad(28)))
    legend = ns(H('In the plan', 'fs-cs-leg fs-cs-leg--on'), H('Not part of this plan yet', 'fs-cs-leg fs-cs-leg--off'), d='row', gap_=26, justify='center', mobile_col=False, wrap=True)
    plan = section(sec_head('The plan', c['plan_h2'], c['plan_lead']), row(*cards, gap_=24, align='stretch', wrap=True, cls='fs-rel-grid fs-nostyle'), legend,
                   button('Get a plan like this', '/contact-us/', 'fs-btn-lg', 'center'), cls='fs-dark fs-fwblock', title='The plan', gap_=40,
                   p={'unit': 'px', 'top': '72', 'right': '24', 'bottom': '140', 'left': '24', 'isLinked': False},
                   s={'padding_mobile': {'unit': 'px', 'top': '56', 'right': '16', 'bottom': '96', 'left': '16', 'isLinked': False}})

    # 5. how we did it (light): numbered step cards, last one highlighted
    steps_ = []
    for n, (k, when, t, d, svcs) in enumerate(c['phases'], 1):
        hl = n == len(c['phases'])
        steps_.append(con(H(str(n), 'fs-step-num'), H(plogo(k), 'fs-cs-step-logo'), heading(t, 'h3'), H(when, 'fs-cs-when'), text(d), H(svcs, 'fs-cs-step-svc'),
                          cls='fs-gcard fs-step' + (' fs-step-hl' if hl else ''), gap_=8, p=pad(64, 28, 32, 28),
                          s={'width': PCT(round(100 / len(c['phases'])) - 3), 'width_mobile': PCT(100),
                             'margin_mobile': {'unit': 'px', 'top': '70', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': False}}))
    how = section(sec_head('How we did it', 'Three phases, <span class="fs-gt">one connected system.</span>'),
                  row(*steps_, gap_=56, align='stretch', cls='fs-steps'), cls='fs-geo fs-cs-how', title='How we did it', bg_img=GEO, gap_=24)

    # 6. results (purple): goal cards, where new patients come from, before -> after table
    gcards = []
    for n, (t, target, res, note, st) in enumerate(c['goal_results'], 1):
        gcards.append(con(ns(H(f'Goal {n}', 'fs-cs-gr-n'), H('In progress' if st == 'now' else 'Achieved', 'fs-cs-hit' + (' fs-cs-hit--now' if st == 'now' else '')),
                             d='row', justify='space-between', align='center', mobile_col=False),
                          heading(t, 'h3', 'fs-cs-gr-h'), ns(H('Target', 'fs-cs-gr-k'), H(target, 'fs-cs-gr-t'), gap_=2),
                          ns(H(res, 'fs-cs-gr-r'), H(note, 'fs-cs-gr-s'), gap_=4, cls='fs-cs-gr-res'),
                          cls='fs-gcard fs-cs-gr', gap_=12, p=pad(26), s={'width': PCT(31), 'width_mobile': PCT(100)}))
    def mixbar(parts):
        return ns(*[con(H(lab, 'fs-cs-mix-t'), cls=f'fs-cs-mix-{kind}', s={'width': PCT(wd)}, p=pad(0, 14)) for lab, wd, kind in parts],
                  d='row', gap_=0, mobile_col=False, cls='fs-cs-mix-bar')
    mix = con(heading('Where new patients come from', 'h3', 'fs-cs-mix-h'), H('New-patient leads, digital marketing vs referrals', 'fs-cs-mix-sub'),
              H('Before', 'fs-cs-cap'), mixbar(c['mix']['before']), H('Now', 'fs-cs-cap'), mixbar(c['mix']['now']), text(c['mix']['note'], 'fs-cs-mix-note'),
              cls='fs-gcard fs-cs-mix', gap_=10, p=pad(28), s={'width': PCT(48), 'width_mobile': PCT(100)})
    ba = con(H('Before → after', 'fs-cs-ba-k'), table(c['table']), cls='fs-purple-card fs-dark fs-cs-batable', gap_=12, p=pad(28), s={'width': PCT(48), 'width_mobile': PCT(100)})
    results = section(sec_head('The results', 'Goals set. <span class="fs-gt">Goals hit.</span>', c['results_lead']),
                      row(*gcards, gap_=24, align='stretch', cls='fs-nostyle'), row(mix, ba, gap_=28, align='stretch'),
                      cls='fs-dark fs-cs-results', title='The results', gap_=36)

    # 7. see the work (light): one tab per proof type
    work = section(sec_head('See the work', 'Before and after, <span class="fs-gt">up close.</span>',
                            'The real work behind the numbers: the new brand, rankings, reviews, leads, website and social, each with the results it produced.'),
                   nested_tabs([(t['tab'], proof_panel(dict(t, name=name))) for t in c['proof']], 'fs-cs-tabs fs-nostyle'),
                   cls='fs-geo', title='See the work', bg_img=GEO, gap_=32)

    # 8. in their words (purple): video + quote, then the client's Google reviews
    v_img, v_cap, v_len = c['video']; q, long_q, who, role = c['voice']
    voice = section(row(vid(v_img, v_cap, v_len), con(eyebrow('In their words'), heading(q, 'h2', 'fs-cs-voice-h'), text(long_q, 'fs-lead'),
                                                      heading(who, 'p', 'fs-sig'), text(role, 'fs-eyebrow'), gap_=12), cls='fs-hero', gap_=48),
                    row(con(eyebrow('Their Google reviews'), heading(c['reviews_h3'], 'h3', 'fs-cs-rev-h'), gap_=8), H(c['reviews_note'], 'fs-cs-soon') if c.get('reviews_note') else None,
                        justify='space-between', align='flex-end', gap_=20),
                    row(*[review(rq, rw) for rq, rw in c['reviews']], gap_=24, align='stretch'),
                    cls='fs-dark fs-cs-voice', title='In their words', gap_=40)

    # 9. what's next (light)
    nxt = section(row(col(eyebrow('What’s next'), heading('The work doesn’t stop at <span class="fs-gt">good results.</span>'), text(c['next_lead'], 'fs-lead'), wpct=50),
                      col(icon_list(c['next'], cls='fs-checks'), button('Let’s talk about your business', '/contact-us/'), wpct=45, gap_=22),
                      cls='fs-gcard fs-cs-next', gap_=48, p=pad(48), s={'padding_mobile': pad(28)}),
                  cls='fs-geo', title='What’s next', bg_img=GEO)

    band = trust(c['stats']); band['settings']['css_classes'] += ' fs-cs-trust'   # same size for every number, whatever it is
    out = [hero, band, client, plan, how, results, work, voice, nxt]
    if c.get('more'):   # (purple) more case studies, then the quiz (light)
        from pages_b import rel_cards
        out.append(section(sec_head('More results', 'More partner <span class="fs-gt">success stories.</span>'),
                           rel_cards([('case', lab, d, t, 'Read the case study', u) for lab, d, t, u in c['more']]),
                           cls='fs-dark', title='More case studies', align='center'))
        out.append(quiz())
    out.append(cta_banner('Want results like these?', 'Start with a 30-minute strategy call. We’ll show you where your marketing stands and what to fix first.'))
    return out
