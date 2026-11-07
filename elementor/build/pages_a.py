from comp import *

SERVICES = [  # slug, name, icon, summary, stages
 ('branding-content-creation', 'Branding & Content Creation', 'idea', 'A brand people recognize and trust, with content that sounds like you everywhere.', ['brand']),
 ('website', 'Website', 'seo', 'A fast, clear website built to turn visitors into calls and bookings.', ['brand']),
 ('analytics', 'Analytics', 'growth', 'Know exactly which marketing brings in customers, in plain English.', ['brand']),
 ('crm', 'CRM', 'network', 'One place for every lead and customer, so nothing slips through the cracks.', ['brand']),
 ('seo', 'SEO', 'analytics', 'Show up first on Google, the map and in AI answers.', ['thought']),
 ('advertising', 'Advertising', 'advertising', 'Paid ads that reach the right local people and turn clicks into booked jobs.', ['thought', 'choice']),
 ('social-media', 'Social Media', 'social', 'Social that gets you found, turns followers into customers and keeps them talking.', ['thought', 'choice', 'referral']),
 ('local-ties', 'Local Ties', 'local', 'Get known in your community through the partners and groups customers trust.', ['thought']),
 ('lead-generation', 'Lead Generation', 'lead-gen', 'Offers, lead magnets and landing pages that turn visitors into leads.', ['choice']),
 ('marketing-automation', 'Marketing Automation', 'automation', 'Follow-up that happens on its own, so leads hear back fast and customers come back.', ['choice', 'referral']),
 ('loyalty', 'Loyalty', 'team', 'Programs that keep customers coming back and choosing you every time.', ['referral']),
 ('reviews-referrals', 'Reviews & Referrals', 'conversation', 'More five-star reviews and a steady stream of referrals, without awkward asks.', ['referral']),
]
GEO = 'assets/img/design/bg-geometric.jpg'

# ======================= HOME =======================
def home():
    return [
        hero('Digital Marketing Agency Services', 'Be the business your <span class="fs-gt">customers find first.</span>',
             'Invest your time and efforts on running your business. Leave the other stuff to a digital marketing agency like us.',
             link=('Explore the Framework', '#framework'),
             media=con(component('hero-phone'), p=pad(0), s={'width': px(440), 'width_tablet': PCT(100), 'width_mobile': PCT(100)})),
        trust([('4.9★', 'on Google · [XX] reviews'), ('10+', 'years in digital marketing'), ('NH', 'Family-owned in Hampton')]),
        problem('Sound familiar?', 'You’re spending on marketing. You just <span class="fs-gt">can’t tell what it’s doing.</span>',
                [('growth.webp', 'You don’t know what’s working.', 'Reports full of impressions and clicks, but no clear line to calls, leads or revenue. You’re paying for activity, not answers.'),
                 ('network.webp', 'You have tactics, not a strategy.', 'A few posts here, an ad there, a website that hasn’t changed in years. Nothing connects, so nothing compounds.'),
                 ('handshake.webp', 'You’ve been burned before.', 'Long contracts, vague promises, and an agency that went quiet the moment the invoice cleared. Trusting the next one feels like a risk.')],
                'None of that is a you problem. <span class="fs-sky">It’s a system problem.</span>'),
        section(component('framework'), boxed=False, title='Framework (interactive)', p=pad(0)),
        guarantee(),
        stats([(47, 'average increase in leads', '%', ''), (1200, 'five-star reviews generated for partners', '', ''),
               (94, 'partner retention rate', '%', ''), (10, 'years building marketing systems', '+', '')]),
        case_reviews(),
        steps('', 'How it works', 'Four steps from “I don’t know what’s working” to a system you can see.', [
            ('Book your strategy call.', 'A [30-minute] conversation about where your marketing is today and where the gaps are. No pitch deck, no pressure.'),
            ('Get your roadmap.', 'We map your business against the FirstSearch Framework and lay out exactly what we’ll do, in what order, and what results we’re committing to.'),
            ('We build and run it.', 'Our team executes across every channel in your plan, from brand and website to ads, SEO, automation and reviews.'),
            ('See the results.', 'Monthly reporting in plain English, tied to leads and revenue, not vanity metrics. You’ll always know what’s working.')]),
        three_ways(),
        faq('Questions owners <span class="fs-gt">ask us</span>', [
            ('What exactly does the FirstSearch Guarantee cover?', '[Plain-English summary of the guarantee: what’s guaranteed, how it’s measured, and what happens if it’s missed.]'),
            ('Why a six-month commitment?', 'Real marketing compounds. SEO, brand recognition, reviews and automation take time to build momentum, and the first months lay the foundation for everything after. Six months is enough time to show real, measurable results, and short enough that you’re never locked in for years.'),
            ('How much does a partnership cost?', 'Every partnership is a fixed monthly retainer, so you’ll never get a surprise invoice. Partnerships start at [$X,XXX]/month, and your exact investment is set in your roadmap based on your goals.'),
            ('What kinds of businesses do you work with?', 'We work with established local and service businesses that are ready to invest in long-term growth. [List of core industries.]'),
            ('Do I need to be in New Hampshire?', '[We’re based in Hampton and love working with NH businesses, but we partner with businesses across [region].]'),
            ('Why do you only work with 25 businesses?', 'Because quality doesn’t scale infinitely. Capping our partner list means every client gets real strategy and senior attention, not a junior account manager juggling forty accounts.'),
            ('How will I know if it’s working?', 'You’ll get monthly reporting in plain English, tied to the numbers that matter: leads, calls, bookings and revenue. No vanity metrics and no black boxes.'),
            ('Who owns my accounts, website and content?', '[You do. Your website, ad accounts, content and data belong to your business, always.]'),
            ('What if I’m not ready to hire an agency?', 'Start with our DIY options. The FirstSearch Blueprint, online course and coaching program give you the same framework we use with our partners. Or take the Framework Quiz to see where your marketing stands today.')]),
        cta_banner(),
    ]

# ======================= ABOUT =======================
TEAM = [('chris', 'Chris Mitchell', 'Owner & Digital Partner', 'Your go-to contact', 'Your direct contact. Chris leads the team with vision and expertise and builds every partner’s strategy.'),
        ('jordyn', 'Jordyn Reardon', 'Digital Operations Manager [CONFIRM title]', 'Keeps every project on track', 'Makes sure every marketing action item is planned, completed and moving your business forward.'),
        ('jacob', 'Jacob Ekroth', 'Lead Graphic Designer', 'Makes your brand pop', 'Brings brands to life through visuals, graphics, brand assets, social posts and more.'),
        ('lindsey', 'Lindsey Mitchell', 'Social Media Manager', 'On point with social', 'The behind-the-scenes social guru, scheduling and measuring the success of your social activity.'),
        ('casey', 'Casey Van Zilen', 'Brand Specialist', 'Tells your story on video', 'Tells your brand’s story, mission, vision and values through compelling video and content.')]
def flip(img, name, role, tag, bio):
    """Team card: Elementor Flip Box. Front = photo, tag pill, name, role, "Get to know" pill; back = bio and quick facts.
    Edit the photo (Front > Background), the name (Title) and the text (Description) in the panel; the look is the fs-team CSS."""
    first = name.split()[0]
    return w('flip-box', {
        'background_a_type': 'classic', 'background_a_background': 'classic', 'background_a_image': {'url': asset(f'assets/img/team/{img}.webp'), 'id': '', 'source': 'library'},
        'background_a_size': 'auto', 'background_a_position': 'bottom center', 'background_a_repeat': 'no-repeat',
        'graphic_element': 'none', 'title_text_a': name,
        'description_text_a': f'<span class="fs-tm-role">{role}</span><small class="fs-tm-tag">{tag}</small><span class="fs-tm-flip">Get to know {first}</span>',
        'title_text_b': name,
        'description_text_b': f'<span class="fs-tm-role">{role}</span><span class="fs-tm-bio">{bio}</span><span class="fs-tm-facts"><span><b>Hometown</b>[Town, NH]</span>'
                              f'<span><b>Favorite spot</b>[A local favorite]</span><span><b>Ask me about</b>[A hobby or passion]</span></span>',
        'button_text': '', 'background_b_background': 'classic', 'background_b_color': '#250762',
        'height': px(460), 'border_radius': px(30), 'flip_effect': 'flip', 'flip_direction': 'left', 'vertical_position_a': 'bottom',
        'vertical_position_b': 'top', 'alignment_a': 'left', 'alignment_b': 'left'}, 'fs-team-card')
def about():
    values = [('trust.webp', 'Accountability', 'We take full ownership of every decision, every dollar and every result, for our clients and for each other.', 'Results guaranteed in writing, and a monthly report you can actually understand.'),
              ('conversation.webp', 'Collaboration', 'We don’t work for you, we work with you. No black boxes, no guessing, no surprises from day one.', 'You see the plan, approve the priorities and always know what’s being worked on.'),
              ('idea.webp', 'Curiosity', 'We stay genuinely invested in your business, always looking for the next opportunity to help you grow.', 'We bring ideas to you, not just finished tasks.'),
              ('handshake.webp', 'Partnership', 'We build long-term relationships rooted in trust, transparency and continuous improvement, not short-term wins.', 'A capped client list, so every partner gets real attention.')]
    return [
        hero('About First Search Marketing', 'We put local businesses first. <span class="fs-gt">It’s in our name.</span>',
             'A family-owned digital marketing agency in Hampton, NH, with big-agency strategy and the personal attention only a local partner can offer.',
             link=('Meet the team', '#team'), media=vid('assets/img/design/team-group.webp', 'Meet the First Search team', '[1:45]')),
        trust([('10+', 'years in digital marketing'), ('25', 'partner businesses, maximum'), ('NH', 'Family-owned in Hampton')]),
        section(row(col(eyebrow('A note from our founder'), heading('Why I started <span class="fs-gt">First Search.</span>'),
                        text('<p>[DRAFT for Chris to rewrite with his real story] I kept meeting local business owners who had done everything right. They worked hard, treated customers well and still couldn’t figure out why the phone wasn’t ringing.</p>'
                             '<p>Most of them had already hired an agency. They’d signed a long contract, received a report full of numbers they didn’t understand, and watched the results never show up. They weren’t failing from lack of effort. They were failing from lack of clarity.</p>'
                             '<p>So we built something different: a framework that treats marketing as a system across the whole customer journey, a team that works with you instead of for you, and a guarantee that puts our results in writing.</p>'),
                        heading('Chris Mitchell', 'p', 'fs-sig'), text('Owner &amp; Digital Partner', 'fs-eyebrow'), wpct=55),
                    col(image('assets/img/design/chris-cutout.webp', '', '100%', alt='Chris Mitchell, Owner and Digital Partner'),
                        html('<blockquote class="fs-quote-chip">“Marketing success comes from clear strategy, not hacks, trends or oversized budgets.”<cite>Chris Mitchell</cite></blockquote>'), wpct=42, gap_=0), gap_=48),
                cls='fs-geo', title='Founder note', bg_img=GEO),
        section(row(col(heading('Our mission', 'p', 'fs-mv-k fs-mv-k--target'), heading('Put businesses first.', 'h3', 'fs-mv-h'),
                        text('To put businesses first by building tailored, framework-driven strategies that deliver measurable growth, while educating and empowering business owners with the tools, knowledge and partnerships they need to thrive.', 'fs-mv-p'),
                        wpct=48, cls='fs-mv-card fs-mv-navy', p=pad(48), gap_=0, s={'padding_mobile': pad(30)}),
                    col(heading('Our vision', 'p', 'fs-mv-k fs-mv-k--eye'), heading('The trusted partner for local businesses.', 'h3', 'fs-mv-h'),
                        text('To be the trusted partner and go-to resource for local businesses and entrepreneurs, setting a new standard for digital marketing through proven systems, expert teams and a family-oriented culture rooted in long-term success.', 'fs-mv-p'),
                        wpct=48, cls='fs-gcard fs-mv-card fs-mv-light', p=pad(48), gap_=0, s={'padding_mobile': pad(30)}),
                    gap_=28, align='stretch', cls='fs-mv fs-nostyle'), title='Mission and vision', s={'background_background': 'classic', 'background_color': '#FFFFFF'}),
        section(sec_head('What we believe', 'Our point of view.'),
                heading('“Marketing success comes from clear strategy, authentic brand alignment, and continuous improvement of the entire customer journey, <span class="fs-gt">not hacks, trends, or oversized budgets.</span>”', 'p', 'fs-belief', 'center'),
                row(*[con(heading(f'0{n}', 'p', 'fs-step-num'),
                          w('icon', {'selected_icon': {'value': STEP_ICONS[n % 4], 'library': 'fa-solid'}, 'align': 'left', 'primary_color': '#FFFFFF' if n == 3 else '#3299D5', 'size': px(44)}, 'fs-step-icon'),
                          heading(t, 'h3'), text(f'<p><b>{k}</b></p>'), text(d),
                          cls='fs-gcard fs-step' + (' fs-step-hl' if n == 3 else ''), gap_=10, p=pad(64, 28, 32, 28), s={'width': PCT(31), 'width_mobile': PCT(100)})
                      for n, (t, k, d) in enumerate([
                          ('Strategy beats size', 'You don’t need a massive budget to win. You need a proven strategy.', 'Most businesses don’t fail from lack of effort. They fail from lack of clarity.'),
                          ('Authenticity always wins', 'Trust isn’t built through gimmicks. It’s built through consistency.', 'Businesses that stay true to their brand, their purpose and their people don’t just grow. They endure.'),
                          ('Growth is a system', 'Any business can scale by improving the entire customer journey.', 'Growth isn’t one moment. It’s momentum built over time.')], 1)],
                    gap_=28, align='stretch', cls='fs-steps'), cls='fs-dark', title='Beliefs'),
        section(sec_head('Our core values', 'Four values, and what they look like <span class="fs-gt">when you work with us.</span>'),
                value_cards(values),
                cls='fs-geo', title='Core values', bg_img=GEO),
        section(sec_head('Our team', 'The people behind <span class="fs-gt">your marketing.</span>', 'A full marketing team at a fraction of the cost of hiring one. Small in size, serious in results. [CONFIRM: current team members and titles]'),
                row(*[con(flip(*t), cls='fs-tm-col') for t in TEAM], gap_=28, wrap=True, align='stretch', justify='center', cls='fs-team-grid fs-nostyle'),
                cls='fs-team-sec', title='Team', s={'_element_id': 'team', 'background_background': 'classic', 'background_color': '#EEF0F9'}),
        section(row(col(eyebrow('The FirstSearcher Manifesto'), heading('Fueling growth. Taking action. Building a legacy.'),
                        text('A FirstSearcher is a business owner who has stopped chasing hacks and trends and decided to build something that lasts. It’s the standard we hold ourselves to, and the one we help every partner live by.', 'fs-man-lead'),
                        icon_list(['<b>I take action.</b> Every move follows the FirstSearch Framework.', '<b>I build a brand that lasts.</b> One customers trust and respect.',
                                   '<b>I get attention.</b> In front of the right people at the right time.', '<b>I make the choice clear.</b> At every stage of the customer journey.',
                                   '<b>I turn customers into advocates.</b> They refer, recommend and spread my brand.', '<b>I invest in growth.</b> Marketing is my path to long-term success.',
                                   '<b>I stay committed.</b> Consistency, strategy and execution, every single day.'], 'fas fa-check', 'fs-man-pts'),
                        text('<p>This is my business. My vision. My legacy.<em>And I will Be First Search.</em></p>', 'fs-man-end'), wpct=58, gap_=0, cls='fs-man-copy'),
                    col(image('assets/img/design/manifesto.webp', 'fs-man-art', '100%', alt='The FirstSearcher Manifesto: I take action. I build a brand that lasts. I get attention. I make the choice clear. I turn customers into advocates. I invest in growth. I stay committed.'),
                        wpct=37, cls='fs-man-art-col'), gap_=72, s={'flex_gap_tablet': gap(40)}),
                button('Let’s Talk!', '/contact-us/', 'fs-btn-lg', 'center'), cls='fs-dark fs-manifesto', title='Manifesto', gap_=40),
        section(sec_head('In our community', 'We practice local <span class="fs-gt">ties, too.</span>', 'The same community presence we build for our partners, we build for ourselves, right here in New Hampshire.'),
                cards_grid([[image('assets/img/design/bg-geometric.jpg', 'fs-img-frame', '100%', alt='[Photo: community event]'), heading(t, 'h3'), text('[One line on your involvement]')]
                            for t in ['[Chamber or networking group]', '[Local sponsorship]', '[Workshop, talk or partnership]']]),
                cls='fs-geo', title='Community', bg_img=GEO),
        section(row(col(heading('Want to join the team?', 'h2', 'fs-band-h'), text('We’re growing, and we’re always glad to meet people who care about doing great work for local businesses.', 'fs-band-p'), wpct=65, gap_=8),
                    button('See open roles', '/careers/', 'fs-btn-grad fs-btn-lg'), justify='space-between', s={'flex_align_items_mobile': 'flex-start'}), cls='fs-dark fs-band', title='Careers band',
                p={'unit': 'px', 'top': '48', 'right': '24', 'bottom': '48', 'left': '24', 'isLinked': False}),
        con(cls='fs-geo fs-band-spacer', inner=False, title='Spacer (under the careers band)', bg_img=GEO, minh=230,
            s={'min_height_tablet': px(200), 'min_height_mobile': px(170)}),
        cta_banner('Let’s grow your business together.', 'Start with a 30-minute conversation about where your marketing is today.'),
    ]

# ======================= WHY CHOOSE US =======================
def why():
    comp = [('network.webp', 'Customized and holistic', 'We tailor every strategy to your industry, your customers and your goals. No templates, no one-size-fits-all.', 'Your roadmap is built from your business, your market and your goals, not a pre-set package.'),
            ('growth.webp', 'Data-driven and results-oriented', 'Every decision is backed by data and measured against real growth and a positive return on investment.', 'Every monthly report ties our work to leads, calls and revenue.'),
            ('team.webp', 'An extension of your team', 'A full marketing team at a fraction of the cost of hiring one. Small in size, serious in results.', 'A strategist, designers and specialists for less than one in-house hire.'),
            ('local.webp', 'A local business you can trust', 'Family-owned and NH-based, bringing big-agency strategy with the personal attention only a local partner can offer.', 'We’re in Hampton, NH. Meet us in person, and always reach a real person.')]
    return [
        hero('Why First Search Marketing', 'You’ve heard the promises before. <span class="fs-gt">Here’s what’s different.</span>',
             'If you’ve been burned by an agency, you already know the pattern: a long contract, a report you can’t decode and results that never show up. We built First Search to be the opposite of that.',
             link=('See the guarantee', '#guarantee'), media=vid(caption='Why owners switch to First Search', length='[2:00]')),
        trust([('25', 'partner businesses, maximum'), ('6', 'month partnership, not a multi-year lock-in'), ('✓', 'results guaranteed in writing')]),
        section(sec_head('Side by side', 'Not all marketing help <span class="fs-gt">is created equal.</span>',
                         'You have three real options for growing your marketing: do it yourself, hire a typical agency, or partner with us. Here’s how they compare on the eight things that decide whether your marketing actually works.'),
                cmp_table(), text('[CONFIRM: every comparison claim must be fair and defensible]', 'fs-cmp-note', 'center'), cls='fs-geo', title='Comparison', bg_img=GEO, gap_=40),
        stage_cards(),
        section(sec_head('Our core competencies', 'What we’re built <span class="fs-gt">to do well.</span>'),
                value_cards(comp), cls='fs-geo', title='Competencies', bg_img=GEO),
        guarantee(),
        stats([(47, 'average increase in leads', '%', ''), (1200, 'five-star reviews generated for partners', '', ''), (0, 'partner retention [CONFIRM]', '%', ''), (4.9, 'average Google rating', '★', '')]),
        section(sec_head('Proof', 'Don’t take our <span class="fs-gt">word for it.</span>'), row(*[col(review(q, n), wpct=48) for q, n in REVIEWS], gap_=28, align='stretch'), review_schema(REVIEWS),
                link_u('Read all [XX] Google reviews', '#'), cls='fs-geo', title='Reviews', bg_img=GEO, align='center'),
        steps('', 'What working with us looks like', 'No black boxes. You always know what’s happening.', [
            ('Kickoff and onboarding.', '<b>Week 1</b> · Your welcome kit, account access, goals and the people you’ll work with.'),
            ('Your roadmap.', '<b>Month 1</b> · Your plan across all four stages, with the results we’re committing to.'),
            ('Progress updates.', '<b>Every week</b> · Updates on work and progress from our team by email. [CONFIRM cadence]'),
            ('Report and check-in.', '<b>Every month</b> · Results in plain English, what we learned, and what’s next.')]),
        paths(),
        capacity(),
        faq('Questions before you <span class="fs-gt">choose us</span>', [
            ('What exactly does the guarantee cover?', '[Plain-English summary of the guarantee: what’s guaranteed, how it’s measured, and what happens if it’s missed.]'),
            ('Why a six-month partnership?', 'Real marketing compounds. SEO, brand recognition, reviews and automation take time to build momentum. Six months is enough to show measurable results, and short enough that you’re never locked in for years.'),
            ('How is this different from the last agency I hired?', 'A complete strategy instead of disconnected tactics, reporting tied to leads and revenue, a capped client list, and results guaranteed in writing.'),
            ('Do I own my accounts, website and content?', '[CONFIRM] Yes. Everything we build for your business belongs to your business.'),
            ('What if I’m not ready for a partnership?', 'Start with the BeFirst Community or 1:1 coaching. Many partners start there and move up when they’re ready to hand it off.')]),
        cta_banner('See the difference for yourself.', 'A 30-minute strategy call. No pitch deck, no pressure.'),
    ]

# ======================= SERVICES OVERVIEW =======================
def overview():
    return [
        hero('Our services', 'Everything your marketing needs, <span class="fs-gt">built as one system.</span>',
             'Twelve services, organized around the four stages of the FirstSearch Framework. We don’t sell them as a menu. We build the right mix into one plan for your business.',
             link=('Browse all services', '#all-services'), media=vid(caption='Our services, explained in 3 minutes', length='[3:00]')),
        trust([('12', 'services, one plan'), ('4', 'stages of the customer journey'), ('1', 'fixed monthly retainer')]),
        stage_explorer(SERVICES),
        service_grid(SERVICES),
        delivery_band(),
        quiz(),
        faq('Questions about <span class="fs-gt">our services</span>', [
            ('Can I pick only certain services?', 'Every partnership is built from the services your plan needs, so you won’t pay for things that don’t move your business. What we don’t do is sell services one at a time, because marketing works as a system.'),
            ('How do you decide which services my plan includes?', 'On your strategy call and in your roadmap, we score your business across all four stages. Your plan starts with the weakest stage, then builds out as results come in.'),
            ('Why are some services in more than one stage?', 'Because they do more than one job. Social Media, for example, helps people discover you, turns followers into leads and keeps customers engaged. Each service page shows what it does at each stage.'),
            ('Do I own my accounts and assets?', '[CONFIRM] Yes. Your website, ad accounts, social profiles, content and data belong to your business.'),
            ('Can I learn to do this myself instead?', 'Yes. The BeFirst Community gives you the course, Blueprint and webinars for every stage for $88/month, and coaching is available from $500/month.')]),
        cta_banner('Find out where to start.', 'A 30-minute strategy call to see which stage is holding your business back.'),
    ]
