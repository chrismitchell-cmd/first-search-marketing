from comp import *
from pages_a import SERVICES, GEO

DOC_SVG = '<svg viewBox="0 0 24 24" width="36" height="36" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/></svg>'
PLAY = '<span class="fs-rplay"><svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path fill="currentColor" d="M7 4.8v14.4a1 1 0 0 0 1.5.9l11.3-7.2a1 1 0 0 0 0-1.8L8.5 3.9A1 1 0 0 0 7 4.8Z"/></svg></span>'
WAVE = '<svg aria-hidden="true" width="150" height="48" viewBox="0 0 150 48" fill="none"><g stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".9"><path d="M4 20v8M14 12v24M24 18v12M34 6v36M44 16v16M54 10v28M64 20v8M74 14v20M84 4v40M94 16v16M104 10v28M114 20v8M124 14v20M134 18v12M144 22v4"/></g></svg>'
def card_media(t, meta=''):
    """Coloured media header for a resource card, matching the prototype."""
    if t == 'video':
        dur = meta.split(' · ')[0] if ':' in meta.split(' · ')[0] else ''
        return con(html(PLAY + (f'<span class="fs-rdur">{dur}</span>' if dur else '')), cls='fs-rmedia fs-rm-vid', bg_img='assets/img/design/chris-cutout.webp',
                   p=pad(0), justify='center', align='center')
    if t == 'podcast': return html(f'<div class="fs-rmedia fs-rm-pod">{PLAY}{WAVE}</div>')
    if t == 'case': return html('<div class="fs-rmedia fs-rm-case"><b>[XX]%</b><span>[more leads in 90 days]</span></div>')
    return html(f'<div class="fs-rmedia fs-rm-blog"><span class="fs-art">{DOC_SVG}</span></div>')
def rel_cards(items):
    """items: (type, label, meta, title, cta, url)"""
    return row(*[col(card_media(t, meta), con(html(f'<p class="fs-card-meta"><span class="fs-type fs-type--{t}">{lab}</span> {meta}</p>'), heading(ti, 'h3'), link_u(cta, u), p=pad(24), gap_=10),
                     wpct=31, cls='fs-gcard fs-gcard--thin fs-gcard--hover fs-rcard', p=pad(0), gap_=0) for t, lab, meta, ti, cta, u in items], gap_=24, align='stretch')

# ======================= SERVICE (sample: SEO) =======================
def service():
    inc = [('analytics', 'SEO audit', 'Where you rank, why, and what’s holding you back.'), ('analytics', 'Keyword research', 'The searches your customers actually use.'),
           ('local', 'Google Business Profile', 'Optimized, posted to weekly and kept accurate.'), ('seo', 'On-page optimization', 'Titles, content and structure tuned for every service.'),
           ('local', 'Local citations', 'Consistent listings across the directories that matter.'), ('analytics', 'Technical SEO', 'Speed, indexing and structured data fixed.'),
           ('idea', 'AI search visibility', 'Content and data that AI tools can understand and quote.'), ('network', 'Content and links', 'Helpful articles and local links that build authority.'),
           ('growth', 'Monthly rankings report', 'Rankings, traffic and calls from search.')]
    fw = section(sec_head('Where this fits in your framework', 'Get found first.', 'SEO lives in FirstThought. Its job is to put your name in front of people at the exact moment they’re looking.'),
                 row(col(image('assets/img/framework-wheel.webp', '', '100%', 'center', 'The FirstSearch Framework wheel, FirstThought highlighted'), wpct=45),
                     col(html(f'<span class="fs-plogo-chip">SEO in {plogo("thought", size=26)}</span>'), heading('Be the first name customers see.', 'h3'),
                         text('We optimize your website, Google Business Profile and local presence so search engines and AI tools recommend you first.'),
                         heading('What we do', 'p', 'fs-eyebrow'),
                         icon_list(['Keyword research based on how local customers actually search', 'Google Business Profile optimization and weekly posts', 'Service and location pages that rank and convert', 'Technical fixes, speed and structured data for AI search'], cls='fs-checks'),
                         link_u('Explore the FirstThought stage', '/firstthought/'), wpct=55, cls='fs-gcard', p=pad(36), gap_=14), gap_=48),
                 button('Let’s Talk!', '/contact-us/', 'fs-btn-lg', 'center'), cls='fs-dark fs-dark-round', title='Framework fit', gap_=40)
    fw['settings']['_element_id'] = 'framework'
    rel = [s for s in SERVICES if s[0] in ('website', 'reviews-referrals', 'local-ties')]
    return [
        hero('SEO · FirstThought', 'Be the first business <span class="fs-gt">customers find.</span>',
             'Show up first when people near you search for what you sell: on Google, on the map and in AI answers.',
             link=('See how it fits the framework', '#framework'), media=vid()),
        trust([('4.9★', 'on Google · [XX] reviews'), ('10+', 'years in digital marketing'), ('NH', 'Family-owned in Hampton')]),
        problem('Sound familiar?', 'Customers are searching for you. <span class="fs-gt">They’re finding your competitors.</span>',
                [('analytics.webp', 'You’re not in the map pack.', 'For most local searches, the top three map results get the calls. If you’re not there, you’re invisible.'),
                 ('idea.webp', 'AI search skips you.', 'ChatGPT and Google’s AI answers recommend businesses they can understand and trust. Most local sites give them nothing to work with.'),
                 ('growth.webp', 'SEO feels like a black box.', 'You’ve paid for SEO before and never saw clear rankings, traffic or calls.')],
                'The fix isn’t tricks. <span class="fs-sky">It’s giving Google and AI every reason to recommend you.</span>'),
        fw,
        section(sec_head('What’s included', 'Everything it takes to <span class="fs-gt">do SEO properly.</span>'),
                row(*[col(image_box(f'assets/img/icons/{i}.webp', t, d, 'fs-tile', 'left'), wpct=31, cls='fs-gcard fs-gcard--thin', p=pad(20)) for i, t, d in inc], gap_=20, wrap=True, align='stretch'),
                text('<p><b>Covers:</b> Google Search, Google Maps, Bing, Apple Maps and AI search tools like ChatGPT and Gemini [CONFIRM]</p>', 'fs-soft-box', 'center'),
                cls='fs-geo', title='What’s included', bg_img=GEO),
        steps('', 'Your first 90 days.', 'What the first three months of SEO look like with our team.', [
            ('Audit and research', '<b>Days 1 to 14</b> · Rankings, competitors and keywords mapped for your market.'),
            ('Fix the foundation', '<b>Days 15 to 30</b> · Google Business Profile, technical issues and key pages fixed first.'),
            ('Build authority', '<b>Days 31 to 60</b> · New service and location content, citations and local links.'),
            ('Measure and expand', '<b>Days 61 to 90</b> · Report rankings and calls, then go after the next set of keywords.')]),
        case_reviews(h3='[Client name]: from page three to the map pack', rows=(('[Map pack position, up from #X]', '[XX]', '#[X]'), ('[More calls from Google]', '[XX]', '[XX]%'))),
        three_ways('Three ways to <span class="fs-gt">get it done.</span>', 'Have our team run it, learn to do it yourself, or do it yourself with a coach in your corner.'),
        section(sec_head('Works best with', 'SEO is stronger as part of the system.'),
                row(*[col(image_box(f'assets/img/icons/{i}.webp', n, d, 'fs-tile', 'top'), link_u(f'Explore {n}', f'/services/{s}/'), wpct=31, cls='fs-gcard', p=pad(26), gap_=8)
                      for s, n, i, d, _ in rel], gap_=24, align='stretch'), cls='fs-dark', title='Related services'),
        section(sec_head('From our resources', 'Learn more <span class="fs-gt">about SEO</span>'),
                rel_cards([('blog', 'Blog', '7 min read · Oct 9, 2026', 'Showing up in AI search: what local businesses need to know', 'Read the article', '/blog/showing-up-in-ai-search/'),
                           ('blog', 'Blog', '6 min read · Oct 6, 2026', 'Why your Google Business Profile matters more than your website', 'Read the article', '#'),
                           ('case', 'Case study', 'Oct 5, 2026', '[Client name]: from page three to the map pack', 'Read the case study', '/case-studies/')]),
                link_u('See all SEO resources', '/resources/'), cls='fs-geo', title='Resources', bg_img=GEO, align='center'),
        faq('SEO <span class="fs-gt">questions</span>', [
            ('How long does SEO take?', 'Most businesses see movement in 60 to 90 days, with stronger results building over six months. SEO compounds, which is why it’s part of a six-month partnership.'),
            ('Can you guarantee #1 rankings?', 'No one honestly can. What we guarantee is the result in your roadmap, measured in leads, not just rankings.'),
            ('What is AI search?', 'Tools like ChatGPT, Gemini and Google’s AI Overviews now answer “who should I call?” questions. We make sure your business is one they can find, understand and recommend.'),
            ('Do I need a new website for SEO?', 'Not always. We’ll tell you honestly whether your site can rank, or if it’s holding you back.'),
            ('Can I buy SEO on its own?', 'No. Every service is delivered as part of a FirstSearch partnership, because SEO works best alongside the rest of your marketing system. Your plan includes every service your business needs.')]),
        cta_banner('Be the first business customers find.', 'Let’s look at where you rank today, and what it would take to be first.'),
    ]

# ======================= PILLAR (sample: FirstChoice) =======================
SELFCHECK = '''<div class="fs-selfcheck">
<ul>%s</ul>
<div class="fs-sc-result"><p class="fs-sc-score"><b>0</b> of 5</p><h3>This stage is likely holding you back.</h3><p>People are finding you, but too few become leads and customers. Small fixes here often pay off fastest.</p>
<a class="elementor-button" href="/framework-quiz/">Take the full Framework Quiz</a></div></div>
<script>(function(){var r=document.currentScript.previousElementSibling,b=r.querySelector('.fs-sc-score b'),h=r.querySelector('.fs-sc-result h3');
var t=['This stage is likely holding you back.','This stage is likely holding you back.','There is room to grow here.','There is room to grow here.','This stage is in good shape.','This stage is a strength.'];
r.addEventListener('change',function(){var n=r.querySelectorAll('input:checked').length;b.textContent=n;h.textContent=t[n];});})();</script>'''
def pillar():
    stmts = ['Your website has a clear offer or lead magnet for people who aren’t ready to call yet.', 'Every new lead gets a reply within five minutes, even after hours.',
             'People who visit but don’t act see your business again through retargeting.', 'Leads who aren’t ready yet get helpful follow-up until they are.',
             'You know your cost per lead and how many leads become customers.']
    sc = SELFCHECK % ''.join(f'<li><label><input type="checkbox"> <span>{s}</span></label></li>' for s in stmts)
    svcs = [('advertising', 'Advertising', 'Retargeting and conversion campaigns that turn warm audiences into booked jobs.'), ('social', 'Social Media', 'Offer-driven posts and DM automations that turn followers into leads.'),
            ('lead-gen', 'Lead Generation', 'Offers, lead magnets and landing pages that give every visitor a next step.'), ('automation', 'Marketing Automation', 'Instant replies, nurture sequences and booking that close leads while you work.')]
    slugs = ['advertising', 'social-media', 'lead-generation', 'marketing-automation']
    here = '<ol class="fs-here">' + ''.join(f'<li class="{"on" if k == "choice" else ""}"><a href="/first{k}/"><i>{n}</i>{plogo(k)}<small>{STAGES_JOB[k]}</small></a></li>' for n, k in enumerate(STAGES, 1)) + '</ol>'
    check = section(con(row(col(eyebrow('Self-check'), heading('How strong is <span class="fs-gt">your FirstChoice?</span>'), text('Tick every statement that’s true for your business today.'), wpct=40),
                            col(html(sc), wpct=58), gap_=40, align='flex-start'), cls='fs-gcard', p=pad(40)),
                    cls='fs-geo', title='Self-check', bg_img=GEO)
    check['settings']['_element_id'] = 'check'
    return [
        hero('The FirstSearch Framework · Stage 3: FirstChoice', 'Turn attention into <span class="fs-gt">booked business.</span>',
             'Getting found is only half of it. FirstChoice is where interested people become leads, and leads become customers, through offers, follow-up and campaigns built to convert.',
             link=('Take the 60-second self-check', '#check'), media=vid()),
        section(row(col(image('assets/img/framework-wheel.webp', '', '100%', alt='The FirstSearch Framework, stage 3 of 4 (FirstChoice) highlighted'), wpct=40),
                    col(eyebrow('You are here'), heading('Stage 3 of 4 in the FirstSearch Framework.'), html(here), wpct=55), gap_=48), cls='fs-dark', title='You are here'),
        problem('What it looks like when this stage is weak', 'Signs FirstChoice is <span class="fs-gt">holding you back.</span>',
                [('growth.webp', 'Traffic, but no leads.', 'People visit your website and social, then leave without a trace.'),
                 ('automation.webp', 'Leads go cold.', 'Inquiries wait hours for a reply, and the first business to respond gets the job.'),
                 ('advertising.webp', 'Ads that don’t pay back.', 'Clicks and reach look fine, but the cost per customer is too high, or nobody knows what it is.')],
                'People found you. <span class="fs-sky">This is where they decide.</span>'),
        check,
        section(sec_head('Services in this stage', 'Four services. One goal: be the obvious choice.', 'Each one has a specific job in FirstChoice. Select a service to see everything it includes.'),
                row(*[col(image_box(f'assets/img/icons/{i}.webp', n, d, 'fs-tile', 'top'), link_u(f'See {n}', f'/services/{s}/'), wpct=23, cls='fs-gcard', p=pad(24), gap_=8)
                      for (i, n, d), s in zip(svcs, slugs)], gap_=20, align='stretch', wrap=True),
                button('Let’s Talk!', '/contact-us/', 'fs-btn-lg', 'center'), cls='fs-dark fs-dark-round', title='Services in this stage', gap_=32),
        section(sec_head('How they work together', 'Capture the lead, <span class="fs-gt">then close it.</span>', 'Lead generation and paid campaigns bring people to a decision point. Automation and fast follow-up make sure they choose you. One without the other leaks leads.'),
                row(col(heading('Capture', 'h3'), text('Give interested people a reason to raise their hand.'), image_box('assets/img/icons/lead-gen.webp', 'Lead Generation', 'Offers and landing pages', 'fs-tile'), image_box('assets/img/icons/advertising.webp', 'Advertising', 'Retargeting and conversion campaigns', 'fs-tile'), wpct=32, cls='fs-gcard', p=pad(26), gap_=12),
                    col(image('assets/img/framework-wheel.webp', '', '100%', 'center', 'You are here: FirstChoice'), wpct=28),
                    col(heading('Convert', 'h3'), text('Respond first, follow up well and make booking easy.'), image_box('assets/img/icons/automation.webp', 'Marketing Automation', 'Instant replies and nurture', 'fs-tile'), image_box('assets/img/icons/social.webp', 'Social Media', 'DM automations and offers', 'fs-tile'), wpct=32, cls='fs-gcard', p=pad(26), gap_=12), gap_=24),
                cls='fs-geo', title='How they work together', bg_img=GEO),
        section(sec_head('What we measure', 'How you’ll know you’re being chosen.'),
                row(*[col(heading(h, 'h3'), text(d), text(f'<p><small>{src}</small></p>', 'fs-eyebrow'), wpct=23, gap_=6)
                      for h, d, src in [('Leads per month', 'New inquiries, calls and bookings from every channel.', 'CRM, call tracking'), ('Conversion rate', 'The share of visitors who become leads, by page and offer.', 'Google Analytics'),
                                        ('Lead response time', 'How fast new leads hear back, day and night.', 'CRM'), ('Cost per lead and per customer', 'What each lead, and each new customer, actually costs.', 'Ad platforms, CRM')]],
                    gap_=24, align='stretch', wrap=True), cls='fs-grad', title='What we measure'),
        case_reviews(h3='[Client name]: paid ads that pay for themselves', rows=(('[Cost per lead, down from $XX]', '[XX]', '[$XX]'), ('[New leads per month]', '[XX]', '[XX]'))),
        three_ways('Three ways to get <span class="fs-gt">this stage working.</span>', 'Have our team build it for you, learn the system yourself, or get guided by us.'),
        faq('Questions about <span class="fs-gt">this stage</span>', [
            ('What is the difference between FirstThought and FirstChoice?', 'FirstThought gets you found. FirstChoice turns the people who find you into leads and customers. Lots of visibility with weak conversion wastes money, and great conversion with no visibility has nothing to convert.'),
            ('What is a lead magnet?', 'Something valuable a visitor gets in exchange for their contact details, like a checklist, guide, quiz or free estimate. It captures people who aren’t ready to call yet.'),
            ('How fast should we respond to new leads?', 'Within five minutes if you can. The first business to respond usually wins the job, which is why we automate the first reply.'),
            ('Will automation feel impersonal?', 'Not when it’s done well. Every message is written in your voice, kept short and handed to a real person when it matters.'),
            ('Can I hire you for just this stage?', 'Every partnership covers the full framework, with priorities set around your weakest stage. If FirstChoice is where you’re losing customers, that’s where your plan starts. Prefer to work on it yourself? The BeFirst Community covers every stage.')]),
        cta_banner('Become the obvious choice.', 'Let’s look at where leads slip away today, and how to catch them.'),
    ]
STAGES_JOB = {'brand': 'Build the foundation', 'thought': 'Get found first', 'choice': 'Get chosen', 'referral': 'Get referred'}

# ======================= EVENTS =======================
EVENTS = [('full', 'Oct', '22', 'Thu', 'The FirstSearch Framework in 60 minutes', '12:00 to 1:00 PM · Online · Live on Zoom', 'online'),
          ('brand', 'Oct', '27', 'Tue', 'Build a brand people trust on sight', '12:00 to 1:30 PM · Online · Live on Zoom', 'online'),
          ('thought', 'Nov', '4', 'Wed', 'Get found first: local SEO and AI search', '12:00 to 1:30 PM · Online · Live on Zoom', 'online'),
          ('full', 'Nov', '12', 'Thu', 'BeFirst Live: the full-day framework workshop', '9:00 AM to 4:00 PM · In person · [Venue], Hampton, NH', 'inperson'),
          ('choice', 'Nov', '17', 'Tue', 'Turn your website into a lead machine', '8:30 to 10:30 AM · In person · [Venue], Hampton, NH', 'inperson'),
          ('referral', 'Dec', '2', 'Wed', 'Reviews, referrals and loyalty that sell for you', '12:00 to 1:30 PM · Online · Live on Zoom', 'online'),
          ('thought', 'Dec', '8', 'Tue', 'Ads that actually pay for themselves', '12:00 to 1:30 PM · Online · Live on Zoom', 'online'),
          ('choice', 'Jan', '13', 'Wed', 'Marketing automation for busy owners', '12:00 to 1:30 PM · Online · Live on Zoom', 'online')]
def ev_row(k, m, d, wd, t, meta, fmt):
    tag = '<span class="fs-pill fs-pill--purple">Full Framework</span>' if k == 'full' else f'<span class="fs-plogo-chip">{plogo(k, size=17)}</span>'
    return row(html(f'<div class="fs-date"><small>{m}</small><b>{d}</b><span>{wd}</span></div>'),
               con(html(tag), heading(t, 'h3'), text(f'<p>{meta}</p>', 'fs-card-meta'), gap_=6, s={'flex_grow': 1}),
               button('Reserve your seat', '/events/sample-event/' + ('?format=online' if fmt == 'online' else '')),
               cls='fs-gcard fs-gcard--thin fs-gcard--hover', p=pad(18, 24), gap_=20)
def events():
    feat = EVENTS[0]
    return [
        hero('Workshops and live trainings', 'Learn the system. <span class="fs-gt">Leave with a plan.</span>',
             'Hands-on workshops, online and in Hampton, built on the same framework we use with every partner. Pick the stage you want to work on, or take on the whole thing in a day.',
             cta=('See the calendar', '#calendar'), media=vid()),
        section(row(col(html('<span class="fs-pill fs-pill--purple">Next up</span> <span class="fs-pill">Full Framework</span>'),
                        heading('The FirstSearch Framework <span class="fs-gt">in 60 minutes</span>', 'h2'),
                        text('A fast, founder-led walkthrough of how the four stages fit together, and how to spot which one is holding your business back right now.'),
                        html('<dl class="fs-facts"><div><dt>When</dt><dd><b>Thursday, October 22</b>12:00 to 1:00 PM</dd></div><div><dt>Where</dt><dd><b>Online</b>Live on Zoom</dd></div><div><dt>Investment</dt><dd><b>Free</b>Open registration</dd></div></dl>'),
                        row(button('Reserve your seat', '/events/sample-event/?format=online', 'fs-btn-lg'), link_u('Add to calendar', '#'), gap_=24), wpct=58),
                    col(heading('You’ll leave with', 'h3'), icon_list(['A clear picture of the full framework', 'Your weakest stage, identified', 'Three quick wins to try this week'], cls='fs-checks'),
                        wpct=38, cls='fs-purple-card fs-dark', p=pad(32), gap_=14), gap_=40), title='Featured event'),
        section(sec_head('The calendar', 'More upcoming <span class="fs-gt">workshops</span>', 'Replace these sample rows with a Loop Grid of your Events (newest first) once the Events post type is set up.'),
                con(*[ev_row(*e) for e in EVENTS[1:]], gap_=14), cls='fs-geo', title='Calendar', bg_img=GEO, s={'_element_id': 'calendar'}),
        section(row(col(heading('Want a workshop for your team or group?'), text('We run private sessions for business teams, chambers and networking groups, in person or online.'), wpct=65),
                    button('Request a private workshop', '/contact-us/', 'fs-btn-white fs-btn-lg'), justify='space-between'), cls='fs-dark', title='Private workshops',
                p={'unit': 'px', 'top': '56', 'right': '24', 'bottom': '56', 'left': '24', 'isLinked': False}),
        quiz(),
        cta_banner('Rather have us do it with you?', 'Book a free 30-minute strategy call and we’ll look at your marketing together.'),
    ]

# ======================= RESOURCES =======================
def resources():
    posts = w('posts', {'_skin': 'cards', 'cards_columns': '3', 'cards_posts_per_page': 9, 'cards_meta_data': ['date'], 'cards_show_excerpt': 'yes',
                        'cards_excerpt_length': 18, 'cards_read_more_text': 'Read more »', 'cards_show_badge': 'yes', 'cards_badge_taxonomy': 'category',
                        'pagination_type': 'load_more_on_click', 'load_more_spinner': {'value': 'fas fa-spinner', 'library': 'fa-solid'}}, 'fs-posts')
    filt = w('taxonomy-filter', {'selected_element': '', 'taxonomy': 'category'}, 'fs-filter')
    return [
        hero('Resources', 'Marketing you can <span class="fs-gt">actually use.</span>',
             'Articles, client stories, podcast episodes and videos from our team. Filter by format or by the part of your marketing you want to fix.',
             cta=('Browse resources', '#library'), media=vid()),
        section(row(col(image('assets/img/design/case-dental.webp', 'fs-img-frame', '100%'), wpct=48),
                    col(html('<span class="fs-pill fs-pill--purple">Featured case study</span>'), heading('[Client name]: from page three to the map pack', 'h2'),
                        text('How a local business went from invisible on Google to the top three map results, and what that did for their phone.'),
                        table((('Map pack position', '#9', '#1'), ('Calls from Google', '[18]/mo', '[57]/mo'))),
                        button('Read the case study', '/case-studies/'), wpct=48, gap_=14), gap_=40), title='Featured', cls='fs-geo', bg_img=GEO),
        section(sec_head('The library', 'Every resource, <span class="fs-gt">in one place.</span>', 'Use the filter to show blogs, case studies, podcasts or videos.'),
                filt, posts, cls='', title='Library', s={'_element_id': 'library'}),
        section(row(col(heading('One useful marketing idea a week.'), text('Real stories and practical tips from our newsletter. No fluff, unsubscribe any time.'), wpct=50),
                    col(form([('email', 'Email address', True, 'you@business.com')], 'Subscribe', 'Newsletter'), wpct=45), gap_=40),
                cls='fs-grad', title='Newsletter'),
        quiz(),
        cta_banner('Want help putting this into practice?', 'Book a free 30-minute call and we’ll look at how your business shows up today.'),
    ]

# ======================= BEFIRST TRAINING =======================
def training():
    tbl = ('<div class="fs-table-wrap"><table class="fs-table"><thead><tr><th>What matters</th><th><span class="fs-pill">1 · You do it</span><br>Learn it yourself<br><small>BeFirst Community</small></th>'
           '<th><span class="fs-pill">2 · We do it together</span><br>Build it with us<br><small>1:1 Coaching</small></th><th class="a"><span class="fs-pill">3 · We do it for you</span><br>Let us run it<br><small>Strategic partnership</small></th></tr></thead><tbody>'
           '<tr><th>Who does the work</th><td>You do</td><td>You do, with a coach</td><td class="us"><b>Our team does</b></td></tr>'
           '<tr><th>Investment</th><td><b>$88</b>/month<br><small>Or start with the $8 Blueprint</small></td><td><b>$500</b>/month<br><small>$1,000/month to meet every two weeks</small></td><td class="us"><b>[$X,XXX]</b>/month<br><small>Fixed retainer, six-month partnership</small></td></tr>'
           '<tr><th>What’s included</th><td>Course, Blueprint, live webinars and weekly content</td><td>Everything in the Community, plus 1:1 strategy sessions</td><td class="us">A full team running every stage, with monthly reporting</td></tr>'
           '<tr><th>Your time</th><td>The most</td><td>Moderate</td><td class="us">The least</td></tr>'
           '<tr><th>Results guaranteed</th><td class="no">No</td><td class="no">No</td><td class="us"><b>✓ Yes, in writing</b></td></tr>'
           '<tr><th>Best for</th><td>Owners who like to learn, then do</td><td>Owners who want an expert sounding board and accountability</td><td class="us">Owners who want it done right, without doing it themselves</td></tr>'
           '<tr><th>Next step</th><td><a href="#community">See the Community</a></td><td><a href="#coaching">See coaching</a></td><td class="us"><a href="#partnership">See the partnership</a></td></tr>'
           '</tbody></table></div>')
    comm = section(sec_head('1 · Learn it yourself', 'Everything you need, <span class="fs-gt">in one membership.</span>'),
                   row(col(image('assets/img/design/befirst-training.png', '', 220, alt='BeFirst Marketing Training'), heading('The BeFirst Community', 'h3'),
                           text('The full framework, the tools to apply it, and new content every week, all for one flat monthly rate.'),
                           icon_list(['<b>The BeFirst online course,</b> with new modules released over time', '<b>The FirstSearch Blueprint,</b> every SOP, worksheet and checklist',
                                      '<b>Live webinars</b> on every stage of the framework', '<b>Weekly content,</b> released to members before anyone else',
                                      '<b>First notice of workshops and events,</b> before seats open to the public'], cls='fs-checks'), wpct=55, gap_=14),
                       col(heading('$88<small>/month</small>', 'p', 'fs-price'), text('<p><b>Founding member rate</b> · Annual: 2 months free</p>'),
                           text('<p><b>Lock in the founding rate.</b> Join now and keep this price for as long as you stay. The rate goes up as the Community grows.</p>'),
                           button('Join the Community', '#', 'fs-btn-white fs-btn-lg', 'justify'), text('<p><small>[Cancel anytime. Access ends when your membership does.]</small></p>'),
                           wpct=40, cls='fs-purple-card fs-dark', p=pad(36), gap_=12), gap_=0, cls='fs-gcard', p=pad(0), align='stretch'),
                   heading('Or start with one piece', 'h3', '', 'center'),
                   row(col(row(image('assets/img/design/blueprint-book.webp', '', 120), con(heading('Included with the Community', 'p', 'fs-eyebrow'), heading('The FirstSearch Blueprint', 'h4'),
                           text('The exact SOPs, worksheets and checklists we use with every client.'), button('Get the Blueprint', '#'), gap_=6), gap_=20, s={'flex_direction_mobile': 'row'}), wpct=48, cls='fs-gcard', p=pad(24)),
                       col(heading('Coming soon', 'p', 'fs-eyebrow'), heading('[Book title]', 'h4'), text('The FirstSearch Framework, told through real stories. Join the waitlist to hear first.'),
                           form([('email', 'Email address', True, 'you@business.com')], 'Join the waitlist', 'Book waitlist'), wpct=48, cls='fs-gcard', p=pad(24), gap_=8), gap_=24, align='stretch'),
                   cls='fs-geo', title='Community', bg_img=GEO)
    comm['settings']['_element_id'] = 'community'
    coach = section(sec_head('2 · Build it with us', 'Your business. Your plan. A coach in your corner.'),
                    row(col(image('assets/img/design/chris-cutout.webp', '', '100%', alt='Chris Mitchell, BeFirst coach'), wpct=40, cls='fs-purple-card', p=pad(0)),
                        col(image('assets/img/design/befirst-coaching.png', '', 200, alt='BeFirst Marketing Coaching'), heading('BeFirst Coaching', 'h3'),
                            text('1:1 strategy sessions with our team, built entirely around your business. No course required. Every session works on your numbers, your plan and what’s next.'),
                            heading('$500<small>/month</small>', 'p', 'fs-price'), text('<p>One 1:1 session a month · <b>$1,000/month</b> to meet every two weeks</p>'),
                            icon_list(['[XX]-minute 1:1 strategy sessions', 'A personalized action plan after each session', 'Accountability on what you committed to', '[Between-session support, e.g. email or chat]'], cls='fs-checks'),
                            text('<p><b>Coaching clients save 50% on the Community.</b> Add the course, Blueprint and weekly content for $44/month.</p>', 'fs-soft-box'),
                            button('Book a coaching call', '#', 'fs-btn-lg'), wpct=58, gap_=12), gap_=0, cls='fs-gcard', p=pad(0), align='stretch'),
                    row(col(heading('Hands-on workshops', 'h3'), text('Work on your own business with our team in the room, online or in Hampton.'), wpct=60), link_u('See the full calendar', '/events/'), justify='space-between'),
                    con(*[ev_row(*EVENTS[i]) for i in (1, 3, 4)], gap_=12),
                    cls='fs-dark fs-dark-round', title='Coaching', gap_=28)
    coach['settings']['_element_id'] = 'coaching'
    part = section(sec_head('3 · Let us run it', 'Hand it off. Get <span class="fs-gt">results in writing.</span>'),
                   row(col(image('assets/img/design/team-group.webp', '', '100%', alt='The First Search Marketing team'), eyebrow('Partner with our team'),
                           heading('Your marketing, run by our team. Results guaranteed in writing.', 'h3'),
                           text('We work with 25 businesses. That’s it. Every partner gets real strategy, senior attention and a team that knows their business.'),
                           button('Book your strategy call', '/contact-us/', 'fs-btn-white fs-btn-lg'), text('<p>From [$X,XXX]/month · [X] of 25 spots open</p>'),
                           wpct=56, cls='fs-purple-card fs-dark', p=pad(32), gap_=12),
                       col(con(row(image('assets/img/design/guarantee-seal.webp', '', 100), con(heading('The FirstSearch Guarantee', 'h3'),
                               text('If we don’t deliver [the lead growth in your roadmap], [we keep working at no cost until we do].'), gap_=6), gap_=18, s={'flex_direction_mobile': 'row'}), cls='fs-gcard', p=pad(24)),
                           review(*REVIEWS[0]), wpct=40, gap_=20), gap_=28, align='stretch'),
                   cls='fs-geo', title='Partnership', bg_img=GEO)
    part['settings']['_element_id'] = 'partnership'
    compare = section(sec_head('Three ways to work with us', 'Pick how much you <span class="fs-gt">want to do yourself.</span>'), html(tbl),
                      cls='fs-geo', title='Compare', bg_img=GEO)
    compare['settings']['_element_id'] = 'compare'
    return [
        hero('BeFirst Training', 'One proven system. <span class="fs-gt">Three ways to put it to work.</span>',
             'Every option runs on the FirstSearch Framework, the same system we use with every partner. The only difference is how much of the work you want to do yourself.',
             cta=('Compare the three ways', '#compare'), link=('Explore the Community', '#community'), media=vid()),
        compare, quiz(), comm, coach, part,
        faq('Questions before <span class="fs-gt">you choose</span>', [
            ('Which path is right for me?', 'It comes down to how much of the work you want to do yourself. If you like to learn and implement, start with the Community. If you want an expert working through your plan with you, choose coaching. If you want it done for you with results guaranteed, book a strategy call. The Framework Quiz will also recommend a path based on your score.'),
            ('What happens if I cancel my Community membership?', '[CONFIRM] You keep access through the end of your billing period. After that, access to the course, Blueprint and weekly content ends, and if you rejoin later it will be at the current rate, not your founding rate.'),
            ('Will my Community price go up?', 'Not while you stay a member. The rate you join at is locked in. The price goes up for new members as the Community grows.'),
            ('Is the Community included with coaching?', 'No. Coaching is 1:1 time built entirely around your business, so it works on its own. Coaching clients can add the Community at 50% off if they want the course, Blueprint and weekly content too.'),
            ('What is the difference between a webinar and a workshop?', 'Webinars are live trainings where you watch and learn, and they are included with the Community. Workshops are hands-on: you work on your own business with our team guiding you, and you leave with something finished.'),
            ('Can I switch paths later?', 'Yes. Plenty of owners start in the Community, add coaching when they want more guidance, and move to a partnership when they are ready to hand it off.'),
            ('What is your refund policy?', '[PLACEHOLDER: refund terms for the Community, coaching and the Blueprint]')]),
        cta_banner('Not sure where to start?', 'Take the free Framework Quiz, or book a 30-minute call and we’ll point you to the right path.'),
    ]

# ======================= CONTACT =======================
def contact():
    book = col(heading('Book your free 30-minute consultation', 'h3'), text('Pick a time that works for you. On the call, we’ll cover:'),
               icon_list(['Where your marketing stands today', 'Which stage of the framework is holding you back', 'Whether a partnership, coaching or the Community fits best'], cls='fs-checks'),
               html('<div class="fs-embed-ph">[Paste your GoHighLevel calendar embed code here: replace this HTML widget’s content]</div>'),
               text('<p><small>All times Eastern.</small></p>'), wpct=48, cls='fs-gcard', p=pad(32), gap_=14)
    msg = col(heading('Send us a message', 'h3'), text('Have a question first? Tell us a little about your business.'),
              form([('text', 'Full name', True, '', '50'), ('email', 'Email', True, '', '50'), ('tel', 'Phone (optional)', False, '', '50'), ('text', 'Business name', True, '', '50'),
                    ('url', 'Website (optional)', False, 'https://', '50'),
                    ('select', 'What can we help with?', True, '', '50', ['Choose one', 'A marketing partnership', 'The BeFirst Community', '1:1 coaching', 'Workshops and events', 'Speaking or press', 'Careers', 'Something else']),
                    ('textarea', 'Message', True, ''),
                    ('select', 'How did you hear about us? (optional)', False, '', '100', ['Choose one', 'Google search', 'Social media', 'Referral from a friend or client', 'Workshop or event', 'Podcast', 'Other']),
                    ('acceptance', 'SMS consent', False, '', '100', '[CONFIRM wording for A2P 10DLC compliance] I agree to receive text messages from First Search Marketing about my inquiry. Message frequency varies. Message and data rates may apply. Reply STOP to opt out or HELP for help. Consent is not a condition of purchase. See our Privacy Policy and Terms.')],
                   'Send message', 'Contact'), wpct=48, cls='fs-gcard', p=pad(32), gap_=14)
    two = section(sec_head('Two easy ways to start', 'Book a time, or drop us a line.'), row(book, msg, gap_=28, align='flex-start'), cls='fs-dark', title='Book + message')
    two['settings']['_element_id'] = 'book'
    find = [('local.webp', 'Call', '603-518-8090', 'Talk to a real person on our team', 'Call now', 'tel:+16035188090'),
            ('email.webp', 'Email', 'chris@befirstsearch.com', '[CONFIRM: general inbox, e.g. hello@]', 'Send an email', 'mailto:chris@befirstsearch.com'),
            ('local.webp', 'Visit', '1 Merrill Industrial Drive, Unit #4', 'Hampton, NH 03842', 'Get directions', 'https://maps.google.com/?q=1+Merrill+Industrial+Drive+Unit+4+Hampton+NH+03842'),
            ('team.webp', 'Office hours', 'Monday to Thursday', '[9:00 AM to 5:00 PM] [CONFIRM] · Closed Friday to Sunday', '', '')]
    return [
        hero('Contact us', 'Let’s talk about <span class="fs-gt">your marketing.</span>',
             'Book a free 30-minute consultation, or send us a message. We reply within [one business day].',
             cta=('Book a call', '#book'), link=('Send a message', '#book'), media=vid()),
        two,
        section(sec_head('Find us', 'Prefer to reach <span class="fs-gt">out directly?</span>'),
                row(*[col(image_box(f'assets/img/icons/{i}', f'<small>{k}</small><br>{v}', s, 'fs-tile', 'top', 'p'), link_u(c, u) if c else None,
                          wpct=23, cls='fs-gcard', p=pad(26), gap_=8) for i, k, v, s, c, u in find], gap_=20, align='stretch', wrap=True),
                w('google_maps', {'address': '1 Merrill Industrial Drive, Unit 4, Hampton, NH 03842', 'zoom': px(14), 'height': px(320)}, 'fs-map'),
                cls='fs-dark fs-office', title='Find us', bg_img='assets/img/design/team-group.webp',
                s={'background_position': 'center center', 'background_overlay_background': 'classic', 'background_overlay_color': '#250762',
                   'background_overlay_opacity': {'unit': 'px', 'size': 0.92, 'sizes': []}}),
        steps('After you book', 'What happens next.', '', [
            ('You get a confirmation.', 'A calendar invite and a reminder before the call, by email and text if you opted in.'),
            ('A quick questionnaire.', 'A few short questions about your business, so we can come prepared. [CONFIRM]'),
            ('Your 30-minute call.', 'We look at what’s working, what isn’t and the best path forward. No pitch deck, no pressure.')]),
        section(row(col(heading('Already a partner?', 'p', 'fs-eyebrow'), heading('Get support on your account.', 'h3'),
                        text('Contact your team directly so your request goes straight to the right person.'), button('Client support', '#', 'fs-btn-white'), wpct=48, cls='fs-purple-card fs-dark', p=pad(36), gap_=12),
                    col(heading('Not ready to talk yet?', 'p', 'fs-eyebrow'), heading('Start learning on your own.', 'h3'),
                        text('Take the free Framework Quiz to see where your marketing stands, or start learning in the BeFirst Community.'),
                        link_u('Take the Framework Quiz', '/framework-quiz/'), link_u('Explore BeFirst Training', '/befirst-training/'), wpct=48, cls='fs-gcard', p=pad(36), gap_=12), gap_=28, align='stretch'),
                cls='fs-geo', title='Other ways', bg_img=GEO),
    ]
