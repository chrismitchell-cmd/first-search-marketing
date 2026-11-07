from comp import *
from pages_a import GEO
from pages_b import ev_row, EVENTS, rel_cards

def crumbs(items):
    return '<nav class="fs-crumbs" aria-label="Breadcrumb">' + ' › '.join(f'<a href="{u}">{t}</a>' if u else f'<span aria-current="page">{t}</span>' for t, u in items) + '</nav>'
def back(label, url): return f'<a class="fs-back" href="{url}">← {label}</a>'

# ======================= CASE STUDY =======================
def case_study():
    glance = col(heading('At a glance', 'p', 'fs-eyebrow'),
                 html('<dl class="fs-facts fs-facts--stack"><div><dt>Client</dt><dd>[Client name]</dd></div><div><dt>Industry</dt><dd>[Family dental practice]</dd></div>'
                      '<div><dt>Location</dt><dd>[Town], NH</dd></div><div><dt>Partnership</dt><dd>Six-month partnership, [renewed]</dd></div>'
                      '<div><dt>Services</dt><dd><span class="fs-pill">SEO</span> <span class="fs-pill">Local Ties</span> <span class="fs-pill">Website</span> <span class="fs-pill">Reviews &amp; Referrals</span></dd></div></dl>'),
                 button('Get results like these', '/contact-us/', align='justify'), wpct=32, cls='fs-gcard', p=pad(28), gap_=12, s={'position': 'sticky'})
    story = col(eyebrow('The challenge'), heading('Great reviews in person. <span class="fs-gt">Invisible online.</span>'),
                text('<p>[DRAFT: replace with the client’s real story] Patients loved the practice, but new ones couldn’t find it. A search for “dentist near me” showed three competitors in the map pack, and the practice’s own listing sat on page three with an old phone number and 18 reviews.</p>'
                     '<p>They had tried a national agency before. They got a monthly report full of impressions and clicks, and no idea whether any of it turned into appointments.</p>'),
                w('blockquote', {'blockquote_content': 'We knew we were good at what we do. We just weren’t showing up when people were looking.', 'author_name': '[Client name], [Title]', 'tweet_button': ''}, 'fs-pull'),
                heading('The goal', 'h3'),
                icon_list(['Rank in the top three of the map pack for the practice’s main services', 'Turn website visits into booked appointments, not just clicks', 'Build a steady flow of new reviews without awkward asks'], cls='fs-checks'),
                wpct=62, gap_=16)
    stages = [('thought', 'Get found first.', 'Rebuilt the Google Business Profile, fixed listings across [40] directories and wrote service pages for every treatment.', 'SEO · Local Ties'),
              ('choice', 'Get chosen.', 'Added online booking, clear new-patient offers and click-to-call on every page, so visitors could book in two taps.', 'Website · Lead Generation'),
              ('referral', 'Get referred.', 'Automated review requests after every visit, and a simple referral thank-you that patients actually use.', 'Reviews & Referrals · Automation')]
    approach = section(sec_head('Our approach', 'What we did, stage by stage.'),
                       row(*[con(heading(str(n), 'p', 'fs-step-num'), html(f'<p style="text-align:center">{plogo(k, n == 3, 22)}</p>'), heading(h, 'h3'), text(d, '', 'center'),
                                 text(f'<p><small>{sv}</small></p>', 'fs-eyebrow', 'center'), cls='fs-gcard fs-step' + (' fs-step-hl' if n == 3 else ''), gap_=8, p=pad(64, 28, 32, 28),
                                 s={'width': PCT(31), 'width_mobile': PCT(100)}) for n, (k, h, d, sv) in enumerate(stages, 1)], gap_=28, align='stretch', cls='fs-steps'),
                       cls='fs-dark', title='Approach')
    chart = ('<div class="fs-bars" role="img" aria-label="New-patient leads per month rose from 12 before the partnership to 41 in month six.">'
             + ''.join(f'<div class="fs-bar{" fs-bar--base" if i == 0 else ""}"><span>{v}</span><i style="height:{v * 2}%"></i><small>{m}</small></div>'
                       for i, (m, v) in enumerate([('Before', 12), ('M1', 15), ('M2', 19), ('M3', 24), ('M4', 29), ('M5', 35), ('M6', 41)])) + '</div>')
    return [
        section(row(con(html(back('All case studies', '/case-studies/')), html('<p><span class="fs-type fs-type--case">Case study</span> [Industry] · [Town], NH</p>'),
                        heading('From invisible on Google <span class="fs-gt">to booked out three weeks ahead.</span>', 'h1', 'fs-h1-rule'),
                        text('How [Client name] went from page three of Google to the top of the map pack, and turned searches into a full calendar, in [six months].', 'fs-hero-lead'),
                        html('<p class="fs-k">Framework stages</p><p>' + ' '.join(f'<a class="fs-plogo-chip" href="/first{k}/">{plogo(k, size=17)}</a>' for k in ('thought', 'choice', 'referral')) + '</p>'), gap_=18),
                    con(image('assets/img/design/case-dental.webp', 'fs-img-frame', '100%', alt='[Client photo]'), p=pad(0)), cls='fs-hero', gap_=56),
                cls='fs-geo', title='Hero', bg_img=GEO),
        trust([('+242%', 'monthly leads [sample]'), ('#1', 'in the Google map pack'), ('112', 'Google reviews, up from 18'), ('3 wks', 'booked out ahead')]),
        section(row(glance, story, gap_=48, align='flex-start'), title='Story'),
        approach,
        section(sec_head('The results', 'Six months, <span class="fs-gt">measured monthly.</span>', 'Every number below comes from the monthly report the client gets from us, in plain English. [Sample figures]'),
                row(col(heading('New-patient leads per month', 'h3'), text('<p><small>Calls, form fills and online bookings</small></p>'), html(chart), wpct=50, cls='fs-gcard', p=pad(26)),
                    col(heading('Before → after', 'p', 'fs-eyebrow'), table((('Monthly leads', '12', '41'), ('Map pack position', '#9', '#1'), ('Google reviews', '18', '112'), ('Website conversion', '0.8%', '4.6%'), ('Cost per lead', '$94', '$31'))),
                        wpct=46, cls='fs-purple-card fs-dark', p=pad(28), gap_=12), gap_=28, align='stretch'),
                cls='fs-geo', title='Results', bg_img=GEO),
        section(row(vid('assets/img/design/case-dental.webp', '[Client name] on working with First Search', '[1:20]'),
                    con(eyebrow('In their words'), heading('“We stopped wondering where the next patient was coming from.”'), text('[Two or three sentences from the client about what changed for the business and for them personally.]', 'fs-lead'),
                        heading('[Client name]', 'p', 'fs-sig'), text('[Title], [Business]', 'fs-eyebrow'), gap_=12), cls='fs-hero', gap_=48), title='Client video'),
        section(sec_head('More results', 'More partner <span class="fs-gt">success stories.</span>'),
                rel_cards([('case', 'Case study', 'Sep 26, 2026', '[Client name]: building a referral engine', 'Read the case study', '#'),
                           ('case', 'Case study', 'Sep 12, 2026', '[Client name]: a rebrand and a new website', 'Read the case study', '#'),
                           ('case', 'Case study', 'Aug 29, 2026', '[Client name]: paid ads that pay for themselves', 'Read the case study', '#')]),
                link_u('See all resources', '/resources/'), cls='fs-geo', title='More case studies', bg_img=GEO, align='center'),
        quiz(),
        cta_banner('Want results like these?', 'Start with a 30-minute strategy call. We’ll show you where your marketing stands and what to fix first.'),
    ]

# ======================= BLOG POST =======================
ARTICLE = '''<p class="fs-dek">[Sample article: replace with the real post] A customer asks their phone for “a dentist near me that takes new patients.” The assistant reads out three names. If you aren’t one of them, you never had a chance to compete.</p>
<p>AI search hasn’t replaced Google. It sits on top of it. And it rewards the same thing good local marketing always has: a clear, consistent, trustworthy presence everywhere customers look.</p>
<div class="fs-callout"><b>The short version</b><p>AI tools pull from your Google Business Profile, your website, your reviews and the directories that mention you. Make all four accurate, specific and consistent, and you become the easy answer.</p></div>
<h2 id="s1">What “AI search” actually means for a local business</h2>
<p>When someone asks an AI assistant a question, it doesn’t search the way you do. It gathers what it can find about businesses that match, then summarizes. Three things decide whether you’re in that summary:</p>
<ul><li><b>Can it find you?</b> Your name, address and phone number need to match everywhere.</li><li><b>Does it understand you?</b> Your website has to say plainly what you do, where and for whom.</li><li><b>Does it trust you?</b> Recent, detailed reviews are the strongest signal you control.</li></ul>
<h2 id="s2">Start with your Google Business Profile</h2>
<p>Your profile is the single most-read source about your business. Fill in every field, choose the most specific category, add your services with descriptions, and post at least twice a month.</p>
<h2 id="s3">Write pages that answer real questions</h2>
<p>AI tools quote pages that answer a question directly. One page per service, with a clear first paragraph, prices or ranges where you can, and the towns you serve, beats one long “Services” page every time.</p>
<blockquote class="fs-pull">“Write for the customer’s question, not for the algorithm. The algorithm is trying to find the best answer to that question.”<cite>Chris Mitchell</cite></blockquote>
<h2 id="s4">Make reviews do the talking</h2>
<p>Assistants lean on reviews to decide who’s “best.” Ask every happy customer, make it a two-tap link, and reply to every review. Specific reviews (“they fixed our furnace the same day in Exeter”) help more than five stars alone.</p>
<h2 id="s5">A 30-day checklist</h2>
<ol><li>Audit your name, address and phone on Google, Apple Maps, Bing, Yelp and Facebook.</li><li>Complete every field of your Google Business Profile.</li><li>Rewrite your homepage’s first paragraph to say what you do, where and for whom.</li><li>Create one page for each core service.</li><li>Set up an automatic review request after every job.</li></ol>
<h2 id="s6">Where this fits in the FirstSearch Framework</h2>
<p>Showing up in AI search is part of <a href="/firstthought/">FirstThought</a>: getting found wherever customers look. It only works if <a href="/firstbrand/">FirstBrand</a> is solid first, because AI can only repeat what your brand clearly says.</p>'''
def blog():
    side = col(w('table-of-contents', {'title': 'In this article', 'headings_by_tags': ['h2'], 'marker_view': 'bullets', 'minimize_box': ''}, 'fs-toc'),
               heading('Share', 'p', 'fs-eyebrow'), w('share-buttons', {'share_buttons': [{'_id': uid(), 'button': 'facebook'}, {'_id': uid(), 'button': 'linkedin'}, {'_id': uid(), 'button': 'email'}], 'view': 'icon', 'shape': 'circle', 'skin': 'framed'}),
               wpct=24, gap_=14, s={'position': 'sticky'})
    body = col(w('theme-post-content', {}, 'fs-prose'), text(ARTICLE, 'fs-prose fs-sample-content'),
               con(row(image('assets/img/design/scorecard.png', '', 100), con(eyebrow('Free Framework Quiz'), heading('Is your business the easy answer?', 'h3'), text('Score your marketing across all four stages in about five minutes.'), gap_=6), gap_=20),
                   button('Take the quiz', '/framework-quiz/'), cls='fs-purple-card fs-dark', p=pad(28), gap_=14),
               w('author-box', {'source': 'current', 'show_avatar': 'yes', 'show_name': 'yes', 'show_biography': 'yes', 'link_to': 'posts_archive'}, 'fs-gcard fs-author'),
               wpct=70, gap_=28)
    return [
        section(con(html(back('All articles', '/resources/')), html('<p><span class="fs-type fs-type--blog">Blog</span></p>'),
                    w('theme-post-title', {'header_size': 'h1'}, 'fs-h1-rule'),
                    w('theme-post-excerpt', {}, 'fs-hero-lead'),
                    w('post-info', {'icon_list': [{'_id': uid(), 'type': 'author', 'show_avatar': 'yes'}, {'_id': uid(), 'type': 'date'}, {'_id': uid(), 'type': 'custom', 'custom_text': '7 min read'}]}, 'fs-byline'),
                    w('theme-post-featured-image', {'image_size': 'full'}, 'fs-img-frame'), gap_=18, s={'max_width': px(1080)}),
                cls='fs-geo', title='Article header', bg_img=GEO, align='center'),
        section(row(side, body, gap_=56, align='flex-start'), title='Article'),
        section(row(col(heading('One useful marketing idea a week.'), text('Real stories and practical tips like this one, straight to your inbox. No fluff, unsubscribe any time.'), wpct=50),
                    col(form([('email', 'Email address', True, 'you@business.com')], 'Subscribe', 'Newsletter'), wpct=45), gap_=40), cls='fs-grad', title='Newsletter'),
        section(sec_head('Keep reading', 'More from <span class="fs-gt">the blog.</span>'),
                w('posts', {'_skin': 'cards', 'cards_columns': '3', 'cards_posts_per_page': 3, 'cards_meta_data': ['date'], 'cards_show_excerpt': 'yes', 'cards_excerpt_length': 16,
                            'cards_read_more_text': 'Read the article', 'posts_post_type': 'related', 'related_fallback': 'fallback_recent'}, 'fs-posts'),
                cls='fs-geo', title='Related posts', bg_img=GEO),
        cta_banner('Want help putting this into practice?', 'Book a free 30-minute call and we’ll look at how your business shows up today.'),
    ]

# ======================= PODCAST / VIDEO =======================
def resource():
    chapters = [('0:00', 'Welcome and this week’s question'), ('3:05', 'Why effort isn’t the problem'), ('10:12', 'The three decisions that matter more than budget'),
                ('21:30', 'Case example: doubling leads without more ad spend'), ('33:30', 'Your one action for this week')]
    player = con(html('<div class="fs-embed-ph">[Podcast: paste your Buzzsprout / Spotify episode embed here.<br>Video: delete this widget and use the Video widget below.]</div>'),
                 video('', 'assets/img/design/chris-cutout.webp', 'fs-video'), cls='fs-gcard', p=pad(18), gap_=16)
    notes = col(heading('In this episode', 'h2'),
                text('<p>Chris and [guest name] talk about why most small businesses don’t fail from lack of effort but from lack of clarity, and how a simple framework beats a bigger budget.</p>'
                     '<p>They walk through a real example of a [industry] business that doubled its leads without spending more on ads, just by fixing what happened after someone found them.</p>'),
                heading('Key takeaways', 'h3'),
                icon_list(['A bigger ad budget can’t fix a leaky website or slow follow-up', 'Pick the one stage of the customer journey that’s weakest and fix that first', 'Track leads and revenue, not impressions and likes'], cls='fs-checks'),
                heading('Chapters', 'h3'), html('<ol class="fs-chapters">' + ''.join(f'<li><span>{t}</span> {l}</li>' for t, l in chapters) + '</ol>'),
                w('toggle', {'tabs': [{'_id': uid(), 'tab_title': 'Read the full transcript', 'tab_content': '<p>[Full transcript, generated from the episode and lightly edited. Helps SEO and accessibility.]</p>'}]}, 'fs-faq'),
                wpct=62, gap_=14)
    side = col(con(heading('On this episode', 'p', 'fs-eyebrow'), image_box('assets/img/team/chris.webp', 'Chris Mitchell', 'Host · Owner & Digital Partner', '', 'left', 'p'),
                   image_box('assets/img/design/bg-geometric.jpg', '[Guest name]', '[Title, Business]', '', 'left', 'p'), cls='fs-gcard fs-gcard--thin', p=pad(22), gap_=10),
               con(heading('Mentioned in this episode', 'p', 'fs-eyebrow'), icon_list(['The FirstSearch Framework', 'FirstChoice: turning attention into booked business', 'Free Framework Quiz'], 'fas fa-arrow-right', links=['/services/#framework', '/firstchoice/', '/framework-quiz/']),
                   cls='fs-gcard fs-gcard--thin', p=pad(22), gap_=8),
               con(heading('Never miss an episode', 'p', 'fs-eyebrow'), heading('New episodes every [other Tuesday].', 'h3'), text('Practical marketing for local business owners, in about 30 minutes.'),
                   button('Subscribe', '#', 'fs-btn-white'), cls='fs-purple-card fs-dark', p=pad(26), gap_=10), wpct=34, gap_=20)
    return [
        section(con(html(back('All podcast episodes', '/resources/')), html('<p><span class="fs-type fs-type--podcast">Podcast</span> Episode [24] · October 2, 2026 · [42] min</p>'),
                    heading('Ep. 24: <span class="fs-gt">Strategy beats size.</span>', 'h1', 'fs-h1-rule'),
                    text('Why the local businesses that win aren’t the ones with the biggest budgets, and the three decisions that matter more than spend.', 'fs-hero-lead'),
                    player, gap_=18, s={'max_width': px(1080)}), cls='fs-geo', title='Header + player', bg_img=GEO, align='center'),
        section(row(notes, side, gap_=48, align='flex-start'), title='Show notes'),
        section(sec_head('More episodes', 'Keep <span class="fs-gt">listening.</span>'),
                rel_cards([('podcast', 'Podcast', '[XX] min · Sep 25, 2026', 'Ep. [XX]: Local ties, the marketing that happens offline', 'Listen to the episode', '#'),
                           ('podcast', 'Podcast', '[XX] min · Sep 11, 2026', 'Ep. [XX]: Turning customers into your sales team', 'Listen to the episode', '#'),
                           ('podcast', 'Podcast', '[XX] min · Aug 28, 2026', 'Ep. [XX]: Why growth is a system', 'Listen to the episode', '#')]),
                link_u('See all resources', '/resources/'), cls='fs-geo', title='More episodes', bg_img=GEO, align='center'),
        quiz(),
        cta_banner('Ready to put this into practice?', 'Book a free 30-minute call and we’ll show you where to start.'),
    ]

# ======================= EVENT =======================
def event():
    agenda = [('9:00', 'Welcome, coffee and your starting score', ''), ('9:30', 'Build the foundation', 'brand'), ('10:45', 'Get found first', 'thought'), ('12:00', 'Lunch and networking', '-'),
              ('12:45', 'Get chosen', 'choice'), ('2:00', 'Get referred', 'referral'), ('3:00', 'Build your 90-day plan, one on one', ''), ('3:45', 'Q&amp;A and next steps', '-')]
    ag = '<ol class="fs-agenda">' + ''.join(f'<li class="{"brk" if k == "-" else ""}"><span class="t">{t}</span><b>{l}</b>{plogo(k, size=15) if k not in ("", "-") else ""}</li>' for t, l, k in agenda) + '</ol>'
    reg = section(row(col(eyebrow('Reserve your seat'), heading('Save your spot.'), text('Only [8] seats left. Reserve yours now.', 'fs-lead'),
                          icon_list(['Printed FirstSearch workbook', 'Breakfast, lunch and coffee', 'Your scored Framework audit', 'A 90-day plan to take home', 'Recording of the teaching sessions'], cls='fs-checks'),
                          text('<p><b>[8] of 30</b> seats left [live from ticketing]</p>'), wpct=44),
                      col(form([('text', 'Full name', True, '', '50'), ('email', 'Email', True, '', '50'), ('text', 'Business name', True, '', '50'), ('tel', 'Phone (optional)', False, '', '50'),
                                ('number', 'Seats', True, '1', '50'), ('textarea', 'What do you most want to get out of it? (optional)', False, '')], 'Continue to payment', 'Event registration'),
                          text('<p><small>[Refund / cancellation policy] Can’t make it? We’ll send you the recording. Paid seats: connect Stripe or your ticketing plugin.</small></p>', '', 'center'),
                          wpct=52, cls='fs-gcard', p=pad(30), gap_=10), gap_=40, align='flex-start'), cls='fs-dark', title='Register')
    reg['settings']['_element_id'] = 'register'
    return [
        section(row(con(html(back('All workshops', '/events/')), html('<p><span class="fs-type fs-type--case">In-person workshop</span> <span class="fs-pill">Full Framework</span></p>'),
                        heading('BeFirst Live: <span class="fs-gt">the full-day framework workshop.</span>', 'h1', 'fs-h1-rule'),
                        text('One day, all four stages of the FirstSearch Framework, worked through on your own business. You’ll leave with a scored audit and a 90-day plan.', 'fs-hero-lead'),
                        html('<dl class="fs-facts"><div><dt>When</dt><dd><b>Thursday, November 12</b>9:00 AM to 4:00 PM</dd></div><div><dt>Where</dt><dd><b>[Venue name]</b>Hampton, NH</dd></div><div><dt>Investment</dt><dd><b>$149 per seat</b>[Early-bird pricing]</dd></div></dl>'),
                        row(button('Reserve your seat', '#register', 'fs-btn-lg'), link_u('Add to calendar', '#'), gap_=24), gap_=18),
                    con(html('<div class="fs-date fs-date--lg"><b>12</b><span>Nov<small>Thursday</small></span></div>'),
                        w('countdown', {'countdown_type': 'due_date', 'due_date': '2026-11-12 09:00', 'show_seconds': '', 'label_days': 'days', 'label_hours': 'hours', 'label_minutes': 'mins'}, 'fs-countdown'),
                        text('<p><b>[8] of 30</b> seats left</p>'), cls='fs-purple-card fs-dark', p=pad(32), gap_=16), cls='fs-hero', gap_=56),
                cls='fs-geo', title='Hero', bg_img=GEO),
        section(sec_head('Why come', 'You’ll leave with a <span class="fs-gt">plan, not just notes.</span>'),
                value_cards([
                    ('growth.webp', 'A scored audit', 'Score your own marketing across all four stages, with help in the room.'),
                    ('lead-gen.webp', 'A 90-day plan', 'Walk out with the three moves that will make the biggest difference first.'),
                    ('team.webp', 'A local network', 'Meet other New Hampshire owners working on the same problems.')], 3), cls='fs-geo', title='Outcomes', bg_img=GEO),
        section(row(col(eyebrow('The agenda'), heading('How the time <span class="fs-gt">is spent.</span>'), text('A full day, broken into short teaching blocks followed by hands-on time on your own business.', 'fs-lead'),
                        text('<p><small>[Agenda subject to small changes]</small></p>'), wpct=36), col(html(ag), wpct=60), gap_=48, align='flex-start'),
                cls='fs-geo', title='Agenda', bg_img=GEO),
        section(row(col(heading('This is for you if', 'p', 'fs-eyebrow'), heading('You run a local business and want marketing that adds up.', 'h3'),
                        icon_list(['You own or market a small or mid-sized local business', 'You’re doing “a bit of everything” and not sure what’s working', 'You want a clear plan you can act on right away'], cls='fs-checks'),
                        wpct=48, cls='fs-gcard', p=pad(34), gap_=12),
                    col(heading('It’s not the right fit if', 'p', 'fs-eyebrow'), heading('You’re looking for a quick hack.', 'h3'),
                        icon_list(['You want overnight results without changing anything', 'You’re shopping for a sales pitch. There isn’t one.', 'You’d rather we did it all for you. <a href="/contact-us/">Let’s talk instead.</a>'], 'fas fa-times'),
                        wpct=48, cls='fs-purple-card fs-dark', p=pad(34), gap_=12), gap_=28, align='stretch'), title='Fit'),
        section(row(col(eyebrow('Your host'), heading('Led by <span class="fs-gt">Chris Mitchell.</span>'),
                        text('<p>Chris is the Owner and Digital Partner at First Search Marketing. He built the FirstSearch Framework from years of working with New Hampshire businesses, and he teaches it the same way he uses it with partners: plainly, practically and with real examples.</p><p>You’ll also meet [team member], who walks through the hands-on parts and answers questions one on one.</p>'),
                        heading('Chris Mitchell', 'p', 'fs-sig'), text('Owner &amp; Digital Partner', 'fs-eyebrow'), wpct=55),
                    col(image('assets/img/design/chris-cutout.webp', '', '100%', alt='Chris Mitchell'), wpct=40), gap_=48), cls='fs-geo', title='Host', bg_img=GEO),
        section(row(col(eyebrow('Getting there'), heading('Where we’ll <span class="fs-gt">be.</span>'), text('<p><b>[Venue name]</b><br>[Street address], Hampton, NH 03842</p>'),
                        icon_list(['<b>Parking</b> [Free parking on site]', '<b>Doors open</b> 8:30 AM. Coffee is on.', '<b>Bring</b> a laptop and your last three months of marketing numbers, if you have them.'], 'fas fa-map-marker-alt', 'fs-checks'),
                        link_u('Get directions', '#'), wpct=44),
                    col(w('google_maps', {'address': 'Hampton, NH 03842', 'zoom': px(13), 'height': px(340)}, 'fs-map'), wpct=52, cls='fs-gcard', p=pad(0)), gap_=40), title='Location'),
        reg,
        faq('Good questions before <span class="fs-gt">you sign up.</span>', [
            ('Is this a sales pitch?', 'No. You’ll learn the same framework we use with partners and leave with a plan you can run yourself. If you want help afterwards, you know where we are.'),
            ('Do I need to prepare anything?', 'Bring a laptop. If you have them, your last three months of marketing numbers (website visits, calls, leads) make the hands-on parts more useful.'),
            ('Can I bring someone from my team?', 'Yes. Add more seats in the registration form. Owners and the person who handles marketing get the most out of it together.'),
            ('What if I can’t make it?', '[CONFIRM refund policy] Let us know up to [48 hours] before and we’ll move you to a future date. Everyone who registers gets the recording.'),
            ('Is it right for my industry?', 'The framework works for any local, service-based business: trades, health and wellness, professional services, retail and more. The examples are all from New Hampshire businesses.')]),
        section(sec_head('Can’t make this one?', 'More upcoming <span class="fs-gt">workshops.</span>'), con(*[ev_row(*EVENTS[i]) for i in (2, 4, 5, 6)], gap_=12),
                link_u('See the full calendar', '/events/'), title='More workshops', align='center'),
        cta_banner('Rather have us do it with you?', 'Book a free 30-minute strategy call and we’ll look at your marketing together.'),
    ]

# ======================= LOCATION (sample: SEO in Portsmouth) =======================
def location():
    facts = ('<dl class="fs-facts fs-facts--stack"><div><dt>Service</dt><dd>SEO for local businesses</dd></div><div><dt>Area served</dt><dd>Portsmouth and Rye, New Castle, Greenland</dd></div>'
             '<div><dt>Nearest office</dt><dd>Hampton, NH · about 15 minutes</dd></div><div><dt>Pricing</dt><dd>Fixed monthly retainer [from $X]</dd></div>'
             '<div><dt>Timeline</dt><dd>First map-pack movement in [60 to 90] days</dd></div><div><dt>Guarantee</dt><dd>Results guaranteed in writing</dd></div></dl>')
    inc = [('analytics', 'SEO audit', 'Where you rank, why, and what’s holding you back.'), ('analytics', 'Keyword research', 'The searches your customers actually use.'),
           ('local', 'Google Business Profile', 'Optimized, posted to weekly and kept accurate.'), ('seo', 'On-page optimization', 'Titles, content and structure tuned for every service.'),
           ('local', 'Local citations', 'Consistent listings across the directories that matter.'), ('analytics', 'Technical SEO', 'Speed, indexing and structured data fixed.')]
    near = ['Rye', 'New Castle', 'Greenland', 'Newington', 'Kittery, ME']
    other = ['Website Design', 'Advertising', 'Social Media Marketing', 'Local Ties', 'Reviews & Referrals']
    schema = '''<script type="application/ld+json">{"@context":"https://schema.org","@graph":[
{"@type":["LocalBusiness","ProfessionalService"],"@id":"https://befirstsearch.com/#business","name":"First Search Marketing","url":"https://befirstsearch.com/","telephone":"+1-603-518-8090","address":{"@type":"PostalAddress","streetAddress":"1 Merrill Industrial Drive, Unit #4","addressLocality":"Hampton","addressRegion":"NH","postalCode":"03842","addressCountry":"US"},"areaServed":[{"@type":"City","name":"Portsmouth"},{"@type":"City","name":"Rye"},{"@type":"City","name":"New Castle"},{"@type":"City","name":"Greenland"},{"@type":"City","name":"Newington"},{"@type":"City","name":"Kittery"}]},
{"@type":"Service","@id":"https://befirstsearch.com/services/seo/portsmouth-nh/#service","name":"SEO in Portsmouth, NH","serviceType":"SEO","provider":{"@id":"https://befirstsearch.com/#business"},"areaServed":{"@type":"City","name":"Portsmouth","containedInPlace":{"@type":"State","name":"New Hampshire"}},"isRelatedTo":{"@type":"Service","name":"SEO","url":"https://befirstsearch.com/services/seo/"}},
{"@type":"WebPage","@id":"https://befirstsearch.com/services/seo/portsmouth-nh/","url":"https://befirstsearch.com/services/seo/portsmouth-nh/","name":"SEO Services in Portsmouth, NH","dateModified":"2026-10-29","about":{"@id":"https://befirstsearch.com/services/seo/portsmouth-nh/#service"},"reviewedBy":{"@type":"Person","name":"Chris Mitchell","jobTitle":"Owner & Digital Partner"}}]}</script>'''
    return [
        section(row(con(html(crumbs([('Home', '/'), ('Services', '/services/'), ('SEO', '/services/seo/'), ('Portsmouth, NH', '')])),
                        html(f'<p><span class="fs-pill fs-pill--purple">Serving Portsmouth, NH</span> <a class="fs-plogo-chip" href="/firstthought/">{plogo("thought", size=15)}</a></p>'),
                        heading('SEO <span class="fs-gt">in Portsmouth, NH</span>', 'h1', 'fs-h1-rule'),
                        text('First Search Marketing provides local SEO for Portsmouth, NH businesses: Google Business Profile optimization, local service pages, review growth and monthly reporting tied to calls and leads. We’re a family-owned agency in Hampton, about 15 minutes away, with results guaranteed in writing.', 'fs-hero-lead'),
                        row(button('Get a free Portsmouth SEO audit', '/contact-us/', 'fs-btn-lg'), link_u('About our SEO service', '/services/seo/'), gap_=24, s={'flex_wrap': 'wrap'}),
                        text('<p><small>Reviewed by <b>Chris Mitchell</b>, Owner &amp; Digital Partner · Updated <time datetime="2026-10-29">October 29, 2026</time></small></p>'), gap_=18),
                    con(heading('SEO in Portsmouth at a glance', 'p', 'fs-eyebrow'), html(facts), w('google_maps', {'address': 'Portsmouth, NH', 'zoom': px(12), 'height': px(180)}, 'fs-map'),
                        cls='fs-gcard', p=pad(26), gap_=12), cls='fs-hero', gap_=56),
                cls='fs-geo', title='Hero + key facts', bg_img=GEO),
        section(row(col(eyebrow('SEO · Portsmouth'), heading('Why SEO works differently in Portsmouth.'),
                        text('<p>Portsmouth is one of the most competitive small markets in New England for local search. Downtown restaurants, shops and service businesses compete for the same “near me” searches as visitors from across the Seacoast and beyond, and many of those searches happen on a phone a few blocks away.</p>'
                             '<p>That changes what matters. Proximity, a complete Google Business Profile and recent, detailed reviews carry more weight here than in a quieter town. Seasonal traffic means your visibility needs to be strongest in the months you can least afford to miss. And businesses around Pease and the Route 1 corridor are often competing for regional, not just local, searches. [Add 1–2 specifics from real Portsmouth clients or searches]</p>'
                             '<p>Our approach for Portsmouth businesses starts with the map pack, then builds service and neighborhood pages that answer the questions people actually ask, so you show up in Google and in AI answers like ChatGPT and Google’s AI Overviews.</p>'), wpct=60),
                    col(testimonial('“[Short quote from a Portsmouth client about their results]”', '[Client name], [Business], Portsmouth', 'Google review'),
                        wpct=36, cls='fs-purple-card fs-dark', p=pad(32)), gap_=48), title='Local context (write per town)'),
        section(sec_head('What you get', 'What’s included in SEO <span class="fs-gt">for Portsmouth businesses.</span>', 'The same complete SEO service every partner gets, focused on the customers and searches that matter in Portsmouth.'),
                row(*[col(image_box(f'assets/img/icons/{i}.webp', t, d, 'fs-tile', 'left'), wpct=31, cls='fs-gcard fs-gcard--thin', p=pad(20)) for i, t, d in inc], gap_=20, wrap=True, align='stretch'),
                link_u('See everything included in our SEO service', '/services/seo/'), cls='fs-geo', title='What’s included (summary + link up)', bg_img=GEO, align='center'),
        section(row(col(heading('[Portsmouth client] · [Industry]', 'p', 'fs-eyebrow'), heading('From page three to the map pack in [five] months.', 'h3'),
                        table((('Map pack position', '#9', '#2'), ('Calls from Google', '[18]/mo', '[57]/mo'), ('Google reviews', '[31]', '[104]'))), link_u('Read the full story', '/case-studies/'),
                        wpct=52, cls='fs-purple-card fs-dark', p=pad(30), gap_=14),
                    col(eyebrow('How it works'), heading('Getting started <span class="fs-gt">in Portsmouth.</span>'),
                        icon_list(['<b>Free audit</b> · We review how your business shows up in Portsmouth today, against your top local competitors.', '<b>Your roadmap</b> · A clear plan with the three moves that will make the biggest difference first.',
                                   '<b>Monthly results</b> · We do the work and report every month in plain English, tied to calls and leads.'], 'fas fa-check-circle', 'fs-checks'), wpct=44), gap_=40), title='Local proof'),
        faq('SEO in Portsmouth: <span class="fs-gt">common questions.</span>', [
            ('How much does SEO cost for a Portsmouth business?', 'Our SEO is part of a fixed monthly retainer [from $X], with no long-term lock-in beyond the six-month partnership. The exact scope depends on how competitive your service is in Portsmouth and how many locations you serve.'),
            ('How long does it take to rank in Portsmouth?', 'Most Portsmouth businesses see map-pack movement within [60 to 90] days and steady lead growth by month six. Highly competitive categories downtown can take longer.'),
            ('Do I need an office in Portsmouth to rank there?', 'Not necessarily. Google weighs how close a business is to the person searching, so a Portsmouth address helps for Portsmouth searches. If you serve Portsmouth from nearby, we optimize your service area, local pages and reviews. We never use virtual or fake addresses, which break Google’s guidelines.'),
            ('Can we meet in person?', 'Yes. Our office is in Hampton, about 15 minutes from downtown Portsmouth, and we’re happy to meet at your business.')]),
        section(sec_head('Around the Seacoast', 'Serving Portsmouth and the towns around it.'),
                row(col(heading('SEO in nearby towns', 'h3'), icon_list([f'SEO in {t}' for t in near], 'fas fa-map-marker-alt', links=[f'/services/seo/{t.lower().replace(", me", "-me").replace(" ", "-")}-nh/' if 'ME' not in t else '/services/seo/kittery-me/' for t in near]), wpct=48, cls='fs-gcard', p=pad(26), gap_=10),
                    col(heading('Other services in Portsmouth', 'h3'), icon_list([f'{s} in Portsmouth' for s in other], 'fas fa-arrow-right', links=['#'] * len(other)), wpct=48, cls='fs-gcard', p=pad(26), gap_=10), gap_=24, align='stretch'),
                html(schema), title='Internal links + schema'),
        cta_banner('Ready to be the first name people find?', 'Book a free 30-minute call. We’ll show you how your business shows up locally today.'),
    ]
