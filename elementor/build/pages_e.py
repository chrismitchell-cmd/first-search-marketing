"""One page per workshop, built on the event page design (event.html / singles/single-event), from Elementor widgets
only (no HTML widgets): every date, time, chip, fact and agenda line is a Heading or Text Editor you can edit.
The calendar (dates, seats) and each workshop's title, stage, description and outcomes come from comp.py
(CALENDAR / _W), the same data the Events page lists, so the two never disagree. A workshop that runs on several
dates (BeFirst Live) gets one page with a "Pick your date" section and a date choice in its registration form."""
from comp import *
from pages_a import GEO

DAYS = {'Mon': 'Monday', 'Tue': 'Tuesday', 'Wed': 'Wednesday', 'Thu': 'Thursday', 'Fri': 'Friday', 'Sat': 'Saturday', 'Sun': 'Sunday'}
MNUM = {m: i for i, m in enumerate(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], 1)}

# per workshop: outcome card texts (one per outcome), icons, agenda [(time, item, stage | '' | '-' for Q&A/breaks)]
PAGE = {
    'framework-in-2-hours': (
        ['See how the four stages fit together, and why skipping one leaks customers from the others.',
         'Score your business with help in the room and find the stage that is holding everything else back.',
         'Leave with three small, specific moves you can make before next week.'],
        ('growth.webp', 'lead-gen.webp', 'team.webp'),
        [('3:00', 'Welcome and your starting score', ''), ('3:15', 'The four stages in plain English', 'full'),
         ('3:45', 'Score your business, with help in the room', ''), ('4:15', 'Your three quick wins for this week', ''), ('4:40', 'Q&amp;A and next steps', '-')]),
    'build-a-brand-people-trust': (
        ['Write the one sentence that says what you do, who it is for and why you are different.',
         'Name the values and the edge that customers can actually feel when they deal with you.',
         'Check every place customers meet your brand, so it looks and sounds like one business.'],
        ('idea.webp', 'trust.webp', 'social.webp'),
        [('3:00', 'Welcome and a quick brand check', ''), ('3:15', 'What makes a brand trusted on sight', 'brand'),
         ('3:45', 'Hands-on: write your value statement', 'brand'), ('4:15', 'Audit your touchpoints', 'brand'), ('4:40', 'Q&amp;A and next steps', '-')]),
    'befirst-live-full-day-workshop': (
        ['A plan for all four stages, finished in the room with our team.',
         'The numbers to watch at every stage, so you know what is working.',
         'Three clear first moves and the confidence to start them on Monday.'],
        ('growth.webp', 'analytics.webp', 'team.webp'),
        [('9:00', 'Welcome, coffee and your starting score', ''), ('9:30', 'Build the foundation', 'brand'), ('10:45', 'Get found first', 'thought'),
         ('12:00', 'Lunch and networking', '-'), ('12:45', 'Get chosen', 'choice'), ('2:00', 'Get referred', 'referral'),
         ('3:00', 'Build your 90-day plan, one on one', ''), ('3:45', 'Q&amp;A and next steps', '-')]),
    'local-seo-and-ai-search': (
        ['The profile settings, photos and posts that move you up the map pack.',
         'The handful of searches that actually bring local customers, and where you rank for them.',
         'How AI search tools describe your business today, and what changes their answer.'],
        ('local.webp', 'seo.webp', 'analytics.webp'),
        [('3:00', 'Welcome and a live search of your business', ''), ('3:15', 'How Google and the map pack choose', 'thought'),
         ('3:45', 'Hands-on: tune up your Google Business Profile', 'thought'), ('4:15', 'AI search: being the answer', 'thought'), ('4:40', 'Q&amp;A and next steps', '-')]),
    'website-lead-machine': (
        ['A lead magnet your customers will want, outlined and ready to build.',
         'An offer that makes the next step easy to say yes to.',
         'The follow-up that turns a download or a form into a booked call.'],
        ('lead-gen.webp', 'investment.webp', 'email.webp'),
        [('3:00', 'Welcome and introductions', ''), ('3:15', 'What makes a website turn visitors into leads', 'choice'),
         ('3:45', 'Live website reviews (bring yours)', 'choice'), ('4:15', 'Hands-on: map your follow-up', 'choice'), ('4:40', 'Q&amp;A and next steps', '-')]),
    'reviews-referrals-loyalty': (
        ['A review request that goes out on its own at the right moment.',
         'A referral reward that is easy to explain and worth sharing.',
         'A simple program that gives customers a reason to come back.'],
        ('conversation.webp', 'handshake.webp', 'trust.webp'),
        [('3:00', 'Welcome and where your customers come from', ''), ('3:15', 'Reviews: asking without the awkwardness', 'referral'),
         ('3:45', 'Referrals: rewards that get shared', 'referral'), ('4:15', 'Hands-on: outline your loyalty program', 'referral'), ('4:40', 'Q&amp;A and next steps', '-')]),
    'ads-that-pay-for-themselves': (
        ['A Google or Meta campaign plan for one offer, ready to launch.',
         'Cost per lead and cost per customer, and how to read them every week.',
         'A starting budget built from your numbers, not a guess.'],
        ('advertising.webp', 'analytics.webp', 'investment.webp'),
        [('3:00', 'Welcome and what your ads are for', ''), ('3:15', 'Google vs Meta: which one, when', 'thought'),
         ('3:45', 'Hands-on: plan a campaign for one offer', 'choice'), ('4:15', 'Measure what matters', ''), ('4:40', 'Q&amp;A and next steps', '-')]),
    'marketing-automation-for-busy-owners': (
        ['The three automations every local business should have running, mapped for yours.',
         'The groups on your list that need different messages.',
         'A welcome series that introduces your business while you get on with your day.'],
        ('automation.webp', 'network.webp', 'email.webp'),
        [('3:00', 'Welcome and what to automate first', ''), ('3:15', 'The three automations that pay off fastest', 'choice'),
         ('3:45', 'Hands-on: map your first automations', 'choice'), ('4:15', 'Segments and a welcome journey', 'referral'), ('4:40', 'Q&amp;A and next steps', '-')]),
}
PAGES = WORKSHOPS + list(UPCOMING)   # one page each: calendar workshops, then coming-soon ones
assert set(PAGE) == set(PAGES), 'every workshop in comp.CALENDAR / UPCOMING needs an entry here'

def H(t, cls, tag='p', url=None):
    h = heading(t, tag, cls)
    if url: h['settings']['link'] = {'url': url, 'is_external': '', 'nofollow': ''}
    return h
def nostyle(*kids, cls='', **kw):
    """Container whose widgets keep their own CSS look (the typography pass skips fs-nostyle)."""
    return con(*kids, cls=(cls + ' fs-nostyle').strip(), **kw)

def title_html(t):
    if ':' in t:
        a, b = t.split(':', 1); return f'{a}: <span class="fs-gt">{b.strip()}.</span>'
    w = t.split(); return ' '.join(w[:-2]) + f' <span class="fs-gt">{" ".join(w[-2:])}.</span>'
def stage_tag(k, cls='fs-evp-tag'):
    return H('Full Framework', f'{cls} fs-evp-tag--full') if k == 'full' else H(plogo(k), f'{cls} fs-evp-tag--stage')

def big_date(m, d, day):
    """22 / Oct Thursday, the large gradient date (was an HTML block)."""
    return nostyle(H(d, 'fs-evp-dd'), con(H(m, 'fs-evp-dm'), H(day, 'fs-evp-dw'), gap_=0), d='row', gap_=14, align='center', mobile_col=False, cls='fs-evp-date')
def mini_date(m, d, wd):
    return nostyle(H(m, 'fs-evp-sm'), H(d, 'fs-evp-sd'), H(wd[:3], 'fs-evp-sw'), gap_=0, align='center', justify='center', cls='fs-evp-mini')
def date_row(idx, btn_url, btn='Reserve your seat'):
    """One calendar row (mini date, stage tag, title, time · place, button) for a given CALENDAR index."""
    k, m, d, wd, t, tm, fm, loc, pr, seats, *_ = EVENT_LIST[idx]
    return con(mini_date(m, d, wd),
               nostyle(stage_tag(k), H(t, 'fs-evp-rh', 'h3'), H(f'{tm} · {fm} · {loc}', 'fs-evp-rmeta'), H(seats, 'fs-evp-rseats'), gap_=6, s={'flex_grow': 1}),
               button(btn, btn_url, 'fs-evp-rbtn'), d='row', gap_=20, align='center', mobile_col=True,
               cls='fs-gcard fs-gcard--thin fs-gcard--hover fs-evp-row', p=pad(18, 24))

def event_page(slug):
    """A dated workshop from CALENDAR, or (soon) a workshop in UPCOMING: no date yet, paid, takes waitlist sign-ups."""
    soon = slug in UPCOMING
    dates = [i for i, w in enumerate(EVENT_SLUGS) if w == slug]
    first = dates[0] if dates else 0
    outtxt, icons, agenda = PAGE[slug]
    many = len(dates) > 1
    if soon:
        k, t, desc, outs = UPCOMING[slug]
        fact_rows = [('When', 'Date coming soon', 'A full day, 9:00 AM to 4:00 PM'), ('Where', VENUE[0], VENUE[1]), ('Investment', '[Price] per seat', 'Paid workshop · waitlist gets early-bird pricing')]
    else:
        k, m, d, wd, t, tm, fm, loc, pr, seats, desc, outs = EVENT_LIST[first]
        year = CALENDAR[first][1]
        day = DAYS.get(wd, wd); month = MONTH_NAME[m]
        fact_rows = [('When', f'{day}, {month} {d}', f'{tm}' + (f' · also {len(dates) - 1} more dates' if many else '')), ('Where', VENUE[0], VENUE[1]), ('Investment', pr, seats)]

    facts = nostyle(*[con(H(a, 'fs-evp-fk'), H(b, 'fs-evp-fv'), H(c, 'fs-evp-fs'), gap_=4, cls='fs-evp-fact') for a, b, c in fact_rows],
                    d='row', gap_=0, cls='fs-evp-facts')
    if soon:
        card = con(nostyle(H('Coming soon', 'fs-evp-soon')), nostyle(H('A full-day, paid version of the workshop, with our team in the room all day.', 'fs-evp-soon-p')),
                   nostyle(H('Join the waitlist to hear the date first and get early-bird pricing.', 'fs-evp-seats')), cls='fs-purple-card fs-dark', p=pad(32), gap_=14)
        wl = button('Join the waitlist', '#register', 'fs-btn-lg')
        # same look as the other pages' "Reserve your seat"; the row is fs-nostyle so the typography pass leaves it alone
        wl['settings'].update({'typography_typography': 'custom', 'typography_font_family': 'Poppins', 'typography_font_weight': '600',
                               'typography_font_size': {'unit': 'px', 'size': 22, 'sizes': []}, 'typography_line_height': {'unit': 'em', 'size': 1.2, 'sizes': []}})
        ctas = row(wl, link_u('See the free workshops', '/events/'), gap_=24, cls='fs-nostyle')
    else:
        card = con(big_date(m, d, day),
                   w('countdown', {'countdown_type': 'due_date', 'due_date': f'{year}-{MNUM[m]:02d}-{int(d):02d} 15:00', 'show_seconds': '',
                                   'label_days': 'days', 'label_hours': 'hours', 'label_minutes': 'mins'}, 'fs-countdown'),
                   nostyle(H(seats, 'fs-evp-seats')), cls='fs-purple-card fs-dark', p=pad(32), gap_=16)
        ctas = row(button('Reserve your seat', '#register', 'fs-btn-lg'), link_u('See all dates' if many else 'Add to calendar', '#dates' if many else '#'), gap_=24)
    hero = section(row(con(nostyle(H('← All workshops', 'fs-evp-back', url='/events/'), cls='fs-evp-backw'),
                           nostyle(H('In-person workshop', 'fs-evp-type'), stage_tag(k), d='row', gap_=8, align='center', mobile_col=False, wrap=True, cls='fs-evp-chips'),
                           heading(title_html(t), 'h1', 'fs-h1-rule'), text(desc, 'fs-hero-lead'), facts, ctas, gap_=18),
                       card, cls='fs-hero', gap_=56),
                   cls='fs-geo', title='Hero', bg_img=GEO)

    outcomes = section(sec_head('Why come', 'You’ll leave with a <span class="fs-gt">plan, not just notes.</span>'),
                       value_cards([(ic, o, x) for ic, o, x in zip(icons, outs, outtxt)], 3), cls='fs-geo', title='Outcomes', bg_img=GEO)

    rows = [nostyle(H(a, 'fs-evp-at'), H(l, 'fs-evp-al'), H(plogo(st, size=15), 'fs-evp-as') if st not in ('', '-', 'full') else None,
                    d='row', gap_=16, align='center', mobile_col=False, cls='fs-evp-ag' + (' is-break' if st == '-' else ''), p=pad(16, 20))
            for a, l, st in agenda]
    agenda_sec = section(row(col(eyebrow('The agenda'), heading('How the time <span class="fs-gt">is spent.</span>'),
                                 text(('A full day' if soon else 'Two hours') + ', broken into short teaching blocks followed by hands-on time on your own business.', 'fs-lead'),
                                 text('<p><small>Agenda subject to small changes.</small></p>'), wpct=36),
                             col(con(*rows, gap_=10, cls='fs-evp-agenda'), wpct=60), gap_=48, align='flex-start'),
                         cls='fs-geo', title='Agenda', bg_img=GEO)

    pick = None
    if many:
        pick = section(sec_head('Pick your date', f'{len(dates)} dates to <span class="fs-gt">choose from.</span>',
                                                'Same free workshop, same two hours. Choose the Thursday that works for you, then reserve below.'),
                       con(*[date_row(i, '#register', 'Choose this date') for i in dates], gap_=12), cls='fs-geo', title='Dates', bg_img=GEO)
        pick['settings']['_element_id'] = 'dates'

    fit = section(row(col(heading('This is for you if', 'p', 'fs-eyebrow'), heading('You run a local business and want marketing that adds up.', 'h3'),
                          icon_list(['You own or market a small or mid-sized local business', 'You’re doing “a bit of everything” and not sure what’s working',
                                     'You want a clear plan you can act on right away'], cls='fs-checks'), wpct=48, cls='fs-gcard', p=pad(34), gap_=12),
                      col(heading('It’s not the right fit if', 'p', 'fs-eyebrow'), heading('You’re looking for a quick hack.', 'h3'),
                          icon_list(['You want overnight results without changing anything', 'You’re shopping for a sales pitch. There isn’t one.',
                                     'You’d rather we did it all for you. <a href="/contact-us/">Let’s talk instead.</a>'], 'fas fa-times'),
                          wpct=48, cls='fs-purple-card fs-dark', p=pad(34), gap_=12), gap_=28, align='stretch'), title='Fit')

    host = section(row(col(eyebrow('Your host'), heading('Led by <span class="fs-gt">Chris Mitchell.</span>'),
                           text('<p>Chris is the Owner and Digital Partner at First Search Marketing. He built the FirstSearch Framework from years of working with New Hampshire businesses, and he teaches it the same way he uses it with partners: plainly, practically and with real examples.</p>'),
                           heading('Chris Mitchell', 'p', 'fs-sig'), text('Owner &amp; Digital Partner', 'fs-eyebrow'), wpct=55),
                       col(image('assets/img/design/chris-cutout.webp', '', '100%', alt='Chris Mitchell'), wpct=40), gap_=48), cls='fs-geo', title='Host', bg_img=GEO)

    place = section(row(col(eyebrow('Getting there'), heading('Where we’ll <span class="fs-gt">be.</span>'),
                            text(f'<p><b>First Search Marketing</b><br>{VENUE[1]}</p>'),
                            icon_list(['<b>Parking</b> [Free parking on site]', '<b>Doors open</b> ' + ('8:30 AM' if soon else '2:45 PM') + '. Coffee is on.',
                                       '<b>Bring</b> a laptop and, if you have them, your last three months of marketing numbers.'], 'fas fa-map-marker-alt', 'fs-checks'),
                            link_u('Get directions', 'https://maps.google.com/?q=1+Merrill+Industrial+Drive+Unit+4+Hampton+NH+03842'), wpct=44),
                        col(w('google_maps', {'address': '1 Merrill Industrial Drive, Unit 4, Hampton, NH 03842', 'zoom': px(15), 'height': px(340)}, 'fs-map'),
                            wpct=52, cls='fs-gcard', p=pad(0)), gap_=40), title='Location')

    fields = [('text', 'Full name', True, '', '50'), ('email', 'Email', True, '', '50'), ('text', 'Business name', True, '', '50'), ('tel', 'Phone (optional)', False, '', '50')]
    if soon:
        fields.append(('textarea', 'What would you most want to get out of a full day? (optional)', False, ''))
        reg = section(row(col(eyebrow('Join the waitlist'), heading('Be first to <span class="fs-gt">hear the date.</span>'),
                              text('Seats will be limited. Waitlist members hear about the date first and get early-bird pricing.', 'fs-lead'),
                              icon_list(['Printed FirstSearch workbook', 'Breakfast, lunch and coffee', 'Your scored Framework audit', 'A 90-day plan to take home',
                                         'Recording of the teaching sessions'], cls='fs-checks'), wpct=44),
                          col(form(fields, 'Join the waitlist', f'Waitlist: {t}'),
                              text('<p><small>No payment now. We’ll email you when registration opens.</small></p>', '', 'center'),
                              wpct=52, cls='fs-gcard', p=pad(30), gap_=10), gap_=40, align='flex-start'), cls='fs-dark', title='Waitlist')
        fields = None
    if many:
        fields.append(('select', 'Which date?', True, '', '50', [f'{DAYS.get(EVENT_LIST[i][3], EVENT_LIST[i][3])}, {MONTH_NAME[EVENT_LIST[i][1]]} {EVENT_LIST[i][2]}' for i in dates]))
    if fields is not None:
      fields.append(('number', 'Seats', True, '1', '50'))
      fields.append(('textarea', 'What do you most want to get out of it? (optional)', False, ''))
      reg = section(row(col(eyebrow('Reserve your seat'), heading('Save your spot.'),
                          text(f'Free to attend. Only 8 seats per session, so reserve yours now.', 'fs-lead'),
                          icon_list(['Printed FirstSearch workbook', 'Coffee and snacks', 'Hands-on help from our team', 'A plan to take home'], cls='fs-checks'), wpct=44),
                      col(form(fields, 'Reserve my free seat', f'Registration: {t}'),
                          text('<p><small>Free to attend. Can’t make it after all? Let us know so we can give your seat to someone else.</small></p>', '', 'center'),
                          wpct=52, cls='fs-gcard', p=pad(30), gap_=10), gap_=40, align='flex-start'), cls='fs-dark', title='Register')
    reg['settings']['_element_id'] = 'register'

    if soon:
        qas = [('When is it?', 'We’re setting the first date now. Join the waitlist and you’ll hear it before anyone else, with early-bird pricing.'),
               ('How is it different from the free workshop?', 'The free two-hour workshop walks you through the framework. BeFirst Live is a full day with our team in the room, so you finish your plan for all four stages before you leave.'),
               ('Is this a sales pitch?', 'No. You’ll learn the same framework we use with partners and leave with a plan you can run yourself.'),
               ('Can I bring someone from my team?', 'Yes. Owners and the person who handles marketing get the most out of it together.'),
               ('Is it right for my industry?', 'The framework works for any local, service-based business: trades, health and wellness, professional services, retail and more. The examples are all from New Hampshire businesses.')]
    else:
      qas = [('Is this a sales pitch?', 'No. You’ll learn the same framework we use with partners and leave with a plan you can run yourself. If you want help afterwards, you know where we are.'),
           ('Is it really free?', 'Yes. There’s no cost to attend. Seats are limited to 8 per session so everyone gets hands-on help, which is why we ask you to reserve.'),
           ('Do I need to prepare anything?', 'Bring a laptop. If you have them, your last three months of marketing numbers (website visits, calls, leads) make the hands-on parts more useful.'),
           ('Can I bring someone from my team?', 'Yes. Add more seats in the registration form. Owners and the person who handles marketing get the most out of it together.'),
           ('What if I can’t make it?', 'Let us know and we’ll release your seat or move you to another date.'),
           ('Is it right for my industry?', 'The framework works for any local, service-based business: trades, health and wellness, professional services, retail and more. The examples are all from New Hampshire businesses.')]

    # next four other workshops on the calendar after this one's first date (one row per workshop)
    seen, nxt = {slug}, []
    for i in (list(range(len(EVENT_LIST))) if soon else list(range(first + 1, len(EVENT_LIST))) + list(range(0, first))):
        if EVENT_SLUGS[i] not in seen: seen.add(EVENT_SLUGS[i]); nxt.append(i)
    more = section(sec_head('Start with a free one' if soon else 'Can’t make this one?', ('Free workshops' if soon else 'More upcoming') + ' <span class="fs-gt">on the calendar.</span>' if soon else 'More upcoming <span class="fs-gt">workshops.</span>'),
                   con(*[date_row(i, event_url(EVENT_LIST[i])) for i in nxt[:4]], gap_=12),
                   link_u('See the full calendar', '/events/'), title='More workshops', align='center')
    return [x for x in [hero, outcomes, agenda_sec, pick, fit, host, place, reg, faq('Good questions before <span class="fs-gt">you sign up.</span>', qas), more,
                        cta_banner('Rather have us do it with you?', 'Book a free 30-minute strategy call and we’ll look at your marketing together.')] if x]
