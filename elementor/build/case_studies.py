"""Case study content, one dict per client. pages_f.case_study_page() turns a dict into the Elementor page
(every block a native widget, so it stays editable in Elementor). New client = copy PROGRESSIVE_DENTAL, change
the words, numbers and images, add it to CASES. Images: assets/img/... paths; None = "replace with your image"
placeholder. Text in [brackets] = still to fill in."""

PH = None   # image placeholder

PROGRESSIVE_DENTAL = {
    'slug': 'progressive-dental-care',
    'client': 'Progressive Dental Care',
    'industry': 'Dental practice',
    'location': 'South Portland, ME',
    'since': 'late 2025',
    'partnership': 'Since late 2025 · ongoing',
    'logo': 'assets/img/case/progressive-dental-logo-new.webp',
    # hero: the client video (paste the link in the Video widget); cover image, caption, length
    'video': ('assets/img/design/case-dental.webp', 'Progressive Dental Care on working with First Search', '[1:20]'),
    'h1': ('Progressive Dental Care:', 'from 12 leads a month to 100+.'),
    'lead': 'After a change in ownership and an agency that never delivered, Progressive Dental Care came to us for a rebrand, a digital marketing engine '
            'and a social strategy. For the first time in the practice’s history, more new patients now come from digital marketing than from referrals.',
    'stages': ['brand', 'thought', 'choice', 'referral'],
    'stats': [('100+', 'digital leads a month, up from 12'), ('#2', 'average map pack position, up from #17'),
              ('239', 'Google reviews (4.9★), up from 75'), ('1K+', 'average social views, up from 110')],

    # the client
    'about': 'Progressive Dental Care is a dental practice in South Portland, Maine, with a strong, long-standing team and patients who love them. '
             'When new owners took over the practice, they set out to make it more modern and more comfortable for patients, without losing the '
             'people and values that made it special.',
    'before': 'During the ownership change, the practice hired an agency that specialized in “transitions”. The results never came. New patients still '
              'arrived almost entirely through referrals, the brand looked dated next to the practice the new owners were building, and online they '
              'were hard to find: an average map pack position of #17, 75 Google reviews and about 12 digital leads a month. At the end of 2025, they came to us.',
    'quote': None,   # (quote, 'Name, Title') about the problem before working together
    'services_short': ['Branding', 'Website', 'Analytics', 'CRM', 'SEO', 'Advertising', 'Social Media', 'Lead Generation', 'Reviews & Referrals'],
    'goals_h2': 'Three things they <span class="fs-gt">came to us for.</span>',
    'goals': [('idea.webp', 'A modern brand that’s still them',
               'A rebrand that kept the core values of an already strong team, in a more modern, comfortable style that fits where the new owners are taking the practice.',
               'new logo, positioning and website'),
              ('lead-gen.webp', 'More leads than referrals',
               'A digital marketing strategy (SEO, reviews and advertising) that finally brings in more new patients than word of mouth.',
               'digital leads outpace referrals'),
              ('social.webp', 'Show the experience',
               'A social strategy that shows the comfortable, patient-first experience and the knowledge, expertise and warmth of the team and office.',
               'more views, more followers, more trust')],

    # the plan: services in the plan / not yet, per stage
    'plan_h2': 'The FirstSearch Framework, built for Progressive Dental.',
    'plan_lead': 'Nine services working together across all four stages of the patient journey.',
    'plan': {'brand': (['Branding & Content Creation', 'Website', 'Analytics', 'CRM'], []),
             'thought': (['SEO', 'Advertising', 'Social Media'], ['Local Ties']),
             'choice': (['Lead Generation', 'Advertising', 'Social Media'], ['Marketing Automation']),
             'referral': (['Reviews & Referrals', 'Social Media'], ['Loyalty', 'Marketing Automation'])},

    # how we did it: (stage, when, title, text, services)
    'phases': [('brand', 'First', 'Build the foundation.',
                'A brand new logo, brand positioning and a full website redesign: the modern look, feel and expertise the practice needed, built around the team they already had. Analytics and a CRM track every new patient.',
                'Branding · Website · Analytics · CRM'),
               ('thought', 'Then', 'Get found and get chosen.',
                'We went deep on local SEO, review generation and advertising, so the practice shows up first in South Portland and every search can turn into a booked new patient.',
                'SEO · Reviews · Advertising · Lead Generation'),
               ('referral', 'Now', 'Show the experience.',
                'Social media that builds trust before the first visit: the comfortable, patient-first experience, the team’s expertise and the friendly, caring office.',
                'Social Media')],

    # results: (title, target, result, result note, status 'done' | 'now')
    'results_lead': 'Every number comes from the monthly report Progressive Dental Care gets from us, in plain English.',
    'goal_results': [('A modern brand that’s still them', 'New logo, positioning and website', 'Launched', 'all three, built around the team’s values', 'done'),
                     ('More leads than referrals', 'Digital leads outpace referrals', '12 → 100+', 'digital leads a month, now ahead of referrals', 'done'),
                     ('Show the experience', 'More views, followers and trust', '110 → 1K+', 'average views, and +40% followers', 'now')],
    # where new patients come from: [(label, width %, 'dig' | 'ref')] for before and now
    'mix': {'before': [('Referrals', 70, 'ref'), ('Digital · 12/mo', 30, 'dig')],
            'now': [('Digital · 100+/mo', 62, 'dig'), ('Referrals', 38, 'ref')],
            'note': '<p><b>A first for the practice:</b> new patients from digital marketing now outnumber referrals, for the first time since it opened. '
                    '[Bar widths are illustrative: set the real split if you have referral numbers.]</p>'},
    'table': [('Digital leads a month', '12', '100+'), ('Average map pack position', '#17', '#2'), ('Google reviews', '75', '239'),
              ('Average social views', '110', '1K+'), ('Social followers', '–', '+40%'), ('Top source of new patients', 'Referrals', 'Digital')],

    # see the work: one tab each
    'proof': [
        {'tab': 'Branding', 'kind': 'rows',
         'rows': [('Logo', 'assets/img/case/progressive-dental-logo-old.webp', 'assets/img/case/progressive-dental-logo-new.webp'),
                  ('Business cards', PH, PH), ('Signage', PH, PH)],
         'h3': 'A brand that looks like the practice feels.',
         'p': 'A brand new logo and positioning that kept the warmth and values of the team, with a modern, comfortable style that carries from the business cards to the sign out front.',
         'kpis': [('New', 'logo and brand identity'), ('Modern', 'positioning, same core values'), ('1', 'consistent look, everywhere')]},
        {'tab': 'SEO heatmap', 'kind': 'pair', 'labels': ('Before · late 2025', 'Now'), 'images': (PH, PH),
         'h3': 'Ranking first, across South Portland.',
         'p': 'Each dot on the map is a spot around the practice, showing where Progressive Dental Care ranks when someone there searches “dentist near me”. Green means top 3.',
         'kpis': [('#2', 'average map pack position, from #17'), ('15', 'places climbed'), ('[XX%]', 'of the map in the top 3')]},
        {'tab': 'Reviews', 'kind': 'rating', 'before': ('Before · late 2025', '[X.X]', '75'), 'after': ('Now', '4.9', '239'),
         'h3': 'Reviews that match the care.',
         'p': 'A friendly, automatic review request after every visit, so happy patients say so where new patients are looking. More reviews helped lift the practice from #17 to #2 in the map pack.',
         'kpis': [('239', 'Google reviews, from 75'), ('3x', 'the reviews'), ('4.9★', 'average rating')]},
        {'tab': 'Leads', 'kind': 'leads', 'before': '12', 'after': '100+',
         'sources': [('Google Business Profile', 86), ('Website forms and booking', 64), ('Google Ads', 48), ('Social media', 30), ('Referrals', 18)],
         'h3': 'Leads you can count.',
         'p': 'Every call, form and booking lands in the CRM with where it came from, so Progressive Dental Care knows exactly what is working.',
         'kpis': [('100+', 'digital leads a month, from 12'), ('8x', 'the leads'), ('#1', 'source of new patients: digital, a first for the practice')]},
        {'tab': 'Website', 'kind': 'browser', 'images': (PH, PH),
         'h3': 'A website built to book patients.',
         'p': 'A full redesign that finally matches the practice: modern, comfortable and built to turn visitors into new patients. [Add what changed.]',
         'kpis': [('[X.X%]', 'visitors who book or call'), ('[X.Xs]', 'load time on mobile'), ('[+XX%]', 'time on site')]},
        {'tab': 'Social posts', 'kind': 'phone', 'images': (PH, PH),
         'h3': 'Social that shows the experience.',
         'p': 'Posts that show what it’s like to be a patient: the comfortable, patient-first experience, the team’s knowledge and expertise, and a friendly, caring office.',
         'kpis': [('1K+', 'average views, from 110'), ('9x', 'the views'), ('+40%', 'followers')]},
    ],

    # in their words: the owners' Google reviews
    'reviews_h3': 'What the owners say <span class="fs-gt">about working with us.</span>',
    'reviews': [('First Search Marketing has done a phenomenal job with our business. Their approach is comprehensive and respectful of our nuanced requests — '
                 'together, we’ve significantly improved our SEO, built a new website, and tackled social media (my least favorite). I would recommend First Search '
                 'to anybody looking to improve their business through marketing services.', 'Ned Gold, Owner'),
                ('My business partner and I have been working with First Search for about six months and we were starting pretty much from ground zero with our '
                 'marketing. We didn’t really even know where to start but the whole process has been easy and approachable and we couldn’t be happier with the '
                 'results thus far. I cannot recommend Chris and his team enough!', 'Pat Wilson, Owner')],

    # what's next
    'next_lead': 'With the brand, website and lead engine in place, the focus now is social: building trust by showing patients the comfortable experience '
                 'and the expert, caring team before they ever walk in.',
    'next': ['Keep growing views and followers with content that shows the team and the office',
             '[Next move 2, e.g. a series on the team’s expertise and treatments]', '[Next move 3, e.g. patient experience stories]'],

    'more': [],   # other case studies: (label, date, title, url); the section shows once there are some
}

CASES = [PROGRESSIVE_DENTAL]
