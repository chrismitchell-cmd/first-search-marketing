"""One page per workshop, built on the event page design (event.html / singles/single-event).
The calendar data (date, time, format, place, price, seats, outcomes) comes from EVENT_LIST in comp.py, the same
list the Events page shows, so the two never disagree. This file adds what only the event page needs:
slug, agenda, the outcome card texts and a year for the countdown. Dates are placeholders the client edits in Elementor."""
from comp import *
from pages_a import GEO
from pages_c import back

MONTHS = {'Jan': ('January', 1), 'Feb': ('February', 2), 'Mar': ('March', 3), 'Apr': ('April', 4), 'May': ('May', 5), 'Jun': ('June', 6),
          'Jul': ('July', 7), 'Aug': ('August', 8), 'Sep': ('September', 9), 'Oct': ('October', 10), 'Nov': ('November', 11), 'Dec': ('December', 12)}
DAYS = {'Mon': 'Monday', 'Tue': 'Tuesday', 'Wed': 'Wednesday', 'Thu': 'Thursday', 'Fri': 'Friday', 'Sat': 'Saturday', 'Sun': 'Sunday'}

# slug, year, start (24h, for the countdown), outcome card texts (one per EVENT_LIST outcome), agenda [(time, item, stage or '' or '-')]
EXTRA = [
    ('framework-in-60-minutes', 2026, '12:00',
     ['See how the four stages fit together, and why skipping one leaks customers from the others.',
      'Score your business live and find the stage that is holding everything else back.',
      'Leave with three small, specific moves you can make before next week.'],
     [('12:00', 'Welcome and how the hour works', ''), ('12:05', 'The four stages in plain English', 'full'),
      ('12:25', 'Score your business, live', ''), ('12:40', 'Three quick wins for this week', ''), ('12:50', 'Q&amp;A', '-')]),
    ('build-a-brand-people-trust', 2026, '12:00',
     ['Write the one sentence that says what you do, who it is for and why you are different.',
      'Name the values and the edge that customers can actually feel when they deal with you.',
      'Check every place customers meet your brand, so it looks and sounds like one business.'],
     [('12:00', 'Welcome and a quick brand poll', ''), ('12:10', 'What makes a brand trusted on sight', 'brand'),
      ('12:35', 'Hands-on: write your value statement', 'brand'), ('1:00', 'Audit your touchpoints', 'brand'), ('1:15', 'Q&amp;A and next steps', '-')]),
    ('local-seo-and-ai-search', 2026, '12:00',
     ['The profile settings, photos and posts that move you up the map pack.',
      'The handful of searches that actually bring local customers, and where you rank for them.',
      'How AI search tools describe your business today, and what changes their answer.'],
     [('12:00', 'Welcome and a live search of your business', ''), ('12:10', 'How Google and the map pack choose', 'thought'),
      ('12:35', 'Hands-on: tune up your Google Business Profile', 'thought'), ('1:00', 'AI search: being the answer', 'thought'), ('1:15', 'Q&amp;A and next steps', '-')]),
    ('befirst-live-full-day-workshop', 2026, '09:00',
     ['A plan for all four stages, built on your own business with our team in the room.',
      'The numbers to watch at every stage, so you know what is working.',
      'Three clear first moves and the confidence to start them on Monday.'],
     [('9:00', 'Welcome, coffee and your starting score', ''), ('9:30', 'Build the foundation', 'brand'), ('10:45', 'Get found first', 'thought'),
      ('12:00', 'Lunch and networking', '-'), ('12:45', 'Get chosen', 'choice'), ('2:00', 'Get referred', 'referral'),
      ('3:00', 'Build your 90-day plan, one on one', ''), ('3:45', 'Q&amp;A and next steps', '-')]),
    ('website-lead-machine', 2026, '08:30',
     ['A lead magnet your customers will want, outlined and ready to build.',
      'An offer that makes the next step easy to say yes to.',
      'The follow-up that turns a download or a form into a booked call.'],
     [('8:30', 'Coffee and introductions', '-'), ('8:45', 'What makes a website turn visitors into leads', 'choice'),
      ('9:20', 'Live website reviews (bring yours)', 'choice'), ('10:00', 'Hands-on: map your follow-up', 'choice'), ('10:20', 'Q&amp;A and next steps', '-')]),
    ('reviews-referrals-loyalty', 2026, '12:00',
     ['A review request that goes out on its own at the right moment.',
      'A referral reward that is easy to explain and worth sharing.',
      'A simple program that gives customers a reason to come back.'],
     [('12:00', 'Welcome and where your customers come from', ''), ('12:10', 'Reviews: asking without the awkwardness', 'referral'),
      ('12:35', 'Referrals: rewards that get shared', 'referral'), ('1:00', 'Hands-on: outline your loyalty program', 'referral'), ('1:15', 'Q&amp;A and next steps', '-')]),
    ('ads-that-pay-for-themselves', 2026, '12:00',
     ['A Google or Meta campaign plan for one offer, ready to launch.',
      'Cost per lead and cost per customer, and how to read them every week.',
      'A starting budget built from your numbers, not a guess.'],
     [('12:00', 'Welcome and what your ads are for', ''), ('12:10', 'Google vs Meta: which one, when', 'thought'),
      ('12:35', 'Hands-on: plan a campaign for one offer', 'choice'), ('1:00', 'Measure what matters', ''), ('1:15', 'Q&amp;A and next steps', '-')]),
    ('marketing-automation-for-busy-owners', 2027, '12:00',
     ['The three automations every local business should have running, mapped for yours.',
      'The groups on your list that need different messages.',
      'A welcome series that introduces your business while you get on with your day.'],
     [('12:00', 'Welcome and what to automate first', ''), ('12:10', 'The three automations that pay off fastest', 'choice'),
      ('12:35', 'Hands-on: map your first automations', 'choice'), ('1:00', 'Segments and a welcome journey', 'referral'), ('1:15', 'Q&amp;A and next steps', '-')]),
]
assert [x[0] for x in EXTRA] == EVENT_SLUGS, 'keep EXTRA in the same order as EVENT_LIST / EVENT_SLUGS in comp.py'
ICONS = [('growth.webp', 'lead-gen.webp', 'team.webp'), ('idea.webp', 'trust.webp', 'social.webp'), ('local.webp', 'seo.webp', 'analytics.webp'),
         ('growth.webp', 'analytics.webp', 'team.webp'), ('lead-gen.webp', 'investment.webp', 'email.webp'), ('conversation.webp', 'handshake.webp', 'trust.webp'),
         ('advertising.webp', 'analytics.webp', 'investment.webp'), ('automation.webp', 'network.webp', 'email.webp')]

def title_html(t):
    """Gradient on the part after the colon, or on the last two words."""
    if ':' in t:
        a, b = t.split(':', 1); return f'{a}: <span class="fs-gt">{b.strip()}.</span>'
    w = t.split(); return ' '.join(w[:-2]) + f' <span class="fs-gt">{" ".join(w[-2:])}.</span>'

def chip(k):
    return '<span class="fs-pill">Full Framework</span>' if k == 'full' else f'<span class="fs-plogo-chip">{plogo(k)}</span>'

def other_row(j):
    """Compact row for 'More upcoming workshops', linking to that event's own page."""
    k, m, d, wd, t, tm, fm, loc, *_ = EVENT_LIST[j]
    tag = '<span class="fs-pill fs-pill--purple">Full Framework</span>' if k == 'full' else f'<span class="fs-plogo-chip">{plogo(k, size=17)}</span>'
    return row(html(f'<div class="fs-date"><small>{m}</small><b>{d}</b><span>{wd[:3]}</span></div>'),
               con(html(tag), heading(t, 'h3', 'fs-evo-h'), text(f'<p>{tm} · {fm} · {loc}</p>', 'fs-card-meta'), gap_=6, s={'flex_grow': 1}),
               button('Reserve your seat', event_url(EVENT_LIST[j])), cls='fs-gcard fs-gcard--thin fs-gcard--hover', p=pad(18, 24), gap_=20)

def event_page(i):
    k, m, d, wd, t, tm, fm, loc, pr, seats, desc, outs = EVENT_LIST[i]
    slug, year, start, outtxt, agenda = EXTRA[i]
    online = fm.lower() == 'online'
    free = pr.lower() == 'free'
    month, mnum = MONTHS[m]; day = DAYS.get(wd, wd)
    kind = 'Online workshop' if online else 'In-person workshop'
    where_b, where_s = ('Online', loc) if online else (loc.split(',')[0], ', '.join(x.strip() for x in loc.split(',')[1:]) or 'Hampton, NH')
    price_s = 'Registration required' if free else '[Early-bird pricing]'

    hero = section(row(con(html(back('All workshops', '/events/')), html(f'<p><span class="fs-type fs-type--case">{kind}</span> {chip(k)}</p>'),
                           heading(title_html(t), 'h1', 'fs-h1-rule'), text(desc, 'fs-hero-lead'),
                           html(f'<dl class="fs-facts"><div><dt>When</dt><dd><b>{day}, {month} {d}</b>{tm}</dd></div>'
                                f'<div><dt>Where</dt><dd><b>{where_b}</b>{where_s}</dd></div>'
                                f'<div><dt>Investment</dt><dd><b>{pr if free else pr + " per seat"}</b>{price_s}</dd></div></dl>'),
                           row(button('Reserve your seat', '#register', 'fs-btn-lg'), link_u('Add to calendar', '#'), gap_=24), gap_=18),
                       con(html(f'<div class="fs-date fs-date--lg"><b>{d}</b><span>{m}<small>{day}</small></span></div>'),
                           w('countdown', {'countdown_type': 'due_date', 'due_date': f'{year}-{mnum:02d}-{int(d):02d} {start}', 'show_seconds': '',
                                           'label_days': 'days', 'label_hours': 'hours', 'label_minutes': 'mins'}, 'fs-countdown'),
                           text(f'<p><b>{seats}</b></p>', 'fs-ev-seats'), cls='fs-purple-card fs-dark', p=pad(32), gap_=16), cls='fs-hero', gap_=56),
                   cls='fs-geo', title='Hero', bg_img=GEO)

    outcomes = section(sec_head('Why come', 'You’ll leave with a <span class="fs-gt">plan, not just notes.</span>'),
                       value_cards([(ic, o, x) for ic, o, x in zip(ICONS[i], outs, outtxt)], 3), cls='fs-geo', title='Outcomes', bg_img=GEO)

    ag = '<ol class="fs-agenda">' + ''.join(f'<li class="{"brk" if s == "-" else ""}"><span class="t">{a}</span><b>{l}</b>'
                                             f'{plogo(s, size=15) if s not in ("", "-", "full") else ""}</li>' for a, l, s in agenda) + '</ol>'
    length = 'A full day' if not online and len(agenda) > 6 else ('An hour' if tm.endswith('1:00 PM') else 'A focused session')
    agenda_sec = section(row(col(eyebrow('The agenda'), heading('How the time <span class="fs-gt">is spent.</span>'),
                                 text(f'{length}, broken into short teaching blocks followed by hands-on time on your own business.', 'fs-lead'),
                                 text('<p><small>[Agenda subject to small changes]</small></p>'), wpct=36), col(html(ag), wpct=60), gap_=48, align='flex-start'),
                         cls='fs-geo', title='Agenda', bg_img=GEO)

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

    if online:
        place = section(row(col(eyebrow('How to join'), heading('Join from <span class="fs-gt">anywhere.</span>'),
                                text('<p>It’s live on Zoom, so you can ask questions and work on your own business as we go.</p>'),
                                icon_list(['<b>Your link</b> arrives by email as soon as you register.', '<b>Reminders</b> the day before and an hour before we start.',
                                           '<b>Bring</b> a laptop and, if you have them, your last three months of marketing numbers.',
                                           '<b>Can’t make it live?</b> Everyone who registers gets the recording.'], 'fas fa-check', 'fs-checks'), wpct=52),
                            col(html(f'<div class="fs-date fs-date--lg"><b>{d}</b><span>{m}<small>{day}</small></span></div>'),
                                text(f'<p><b>{tm}</b><br>Eastern time · {loc}</p>'), wpct=40, cls='fs-purple-card fs-dark', p=pad(32), gap_=16),
                            gap_=40, align='center'), title='How to join')
    else:
        place = section(row(col(eyebrow('Getting there'), heading('Where we’ll <span class="fs-gt">be.</span>'),
                                text('<p><b>[Venue name]</b><br>[Street address], Hampton, NH 03842</p>'),
                                icon_list(['<b>Parking</b> [Free parking on site]', f'<b>Doors open</b> 15 minutes before we start. Coffee is on.',
                                           '<b>Bring</b> a laptop and your last three months of marketing numbers, if you have them.'], 'fas fa-map-marker-alt', 'fs-checks'),
                                link_u('Get directions', '#'), wpct=44),
                            col(w('google_maps', {'address': 'Hampton, NH 03842', 'zoom': px(13), 'height': px(340)}, 'fs-map'), wpct=52, cls='fs-gcard', p=pad(0)),
                            gap_=40), title='Location')

    incl = (['Live teaching and Q&amp;A', 'The recording, sent to every registrant', 'A worksheet to follow along', 'Your three quick wins, in writing'] if online
            else ['Printed FirstSearch workbook', 'Coffee and snacks' if len(agenda) <= 6 else 'Breakfast, lunch and coffee', 'Hands-on help from our team',
                  'A plan to take home', 'Recording of the teaching sessions'])
    fields = [('text', 'Full name', True, '', '50'), ('email', 'Email', True, '', '50'), ('text', 'Business name', True, '', '50'), ('tel', 'Phone (optional)', False, '', '50')]
    if not free: fields.append(('number', 'Seats', True, '1', '50'))
    fields.append(('textarea', 'What do you most want to get out of it? (optional)', False, ''))
    note = ('<p><small>Free to attend. We’ll email your link and the recording.</small></p>' if free else
            '<p><small>[Refund / cancellation policy] Can’t make it? We’ll send you the recording. Paid seats: connect Stripe or your ticketing plugin.</small></p>')
    reg = section(row(col(eyebrow('Reserve your seat'), heading('Save your spot.'), text(f'{seats}. Reserve yours now.', 'fs-lead'),
                          icon_list(incl, cls='fs-checks'), wpct=44),
                      col(form(fields, 'Reserve my free seat' if free else 'Continue to payment', f'Registration: {t}'), text(note, '', 'center'),
                          wpct=52, cls='fs-gcard', p=pad(30), gap_=10), gap_=40, align='flex-start'), cls='fs-dark', title='Register')
    reg['settings']['_element_id'] = 'register'

    qas = [('Is this a sales pitch?', 'No. You’ll learn the same framework we use with partners and leave with a plan you can run yourself. If you want help afterwards, you know where we are.')]
    if online:
        qas += [('Do I need to prepare anything?', 'Just a laptop and a quiet half hour before. If you have them, your last three months of marketing numbers make the hands-on parts more useful.'),
                ('Will it be recorded?', 'Yes. Everyone who registers gets the recording and the worksheet, even if you can’t make it live.'),
                ('Do I need a Zoom account?', 'No. The link opens in your browser or the free Zoom app. Camera on is welcome but optional.')]
    else:
        qas += [('Do I need to prepare anything?', 'Bring a laptop. If you have them, your last three months of marketing numbers (website visits, calls, leads) make the hands-on parts more useful.'),
                ('Can I bring someone from my team?', 'Yes. Add more seats in the registration form. Owners and the person who handles marketing get the most out of it together.')]
    if not free:
        qas.append(('What if I can’t make it?', '[CONFIRM refund policy] Let us know up to [48 hours] before and we’ll move you to a future date. Everyone who registers gets the recording.'))
    qas.append(('Is it right for my industry?', 'The framework works for any local, service-based business: trades, health and wellness, professional services, retail and more. The examples are all from New Hampshire businesses.'))

    others = [j for j in range(len(EVENT_LIST)) if j != i][:4] if i < 4 else [j for j in range(len(EVENT_LIST)) if j != i][-4:]
    # rows are fs-nostyle (same look for every title; the typography pass would match some titles to the big hero heading)
    more = section(sec_head('Can’t make this one?', 'More upcoming <span class="fs-gt">workshops.</span>'), con(*[other_row(j) for j in others], gap_=12, cls='fs-nostyle'),
                   link_u('See the full calendar', '/events/'), title='More workshops', align='center')
    return [hero, outcomes, agenda_sec, fit, host, place, reg, faq('Good questions before <span class="fs-gt">you sign up.</span>', qas), more,
            cta_banner('Rather have us do it with you?', 'Book a free 30-minute strategy call and we’ll look at your marketing together.')]
