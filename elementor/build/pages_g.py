"""Video page: "First Search Marketing in two minutes" (video-first-search-in-two-minutes.html), built only from native
Elementor widgets (no HTML widgets) so every word, link and timestamp is editable in Elementor."""
from comp import *
from pages_a import GEO
from pages_d import latest

def H(t, cls, tag='p', url=None, align=None):
    h = heading(t, tag, cls, align)
    if url: h['settings']['link'] = {'url': url, 'is_external': '', 'nofollow': ''}
    return h
def ns(*kids, cls='', **kw):
    return con(*kids, cls=(cls + ' fs-nostyle').strip(), **kw)

V = dict(
    meta='[Month Day, 2026] · [1:45]',
    title='First Search Marketing <span class="fs-gt">in two minutes.</span>',
    lead='Who we are, the three ways we help local businesses grow, what we believe and the values behind every partnership, in under two minutes.',
    intro='<p>First Search Marketing is a <a href="/about-us/">family-owned digital marketing agency in Hampton, New Hampshire</a>. We help local businesses become '
          'the first name their customers find, trust and choose, with the <a href="/services/#framework">FirstSearch Framework</a>: four stages, one connected system, '
          'instead of a pile of tactics.</p>',
    ways=[('Let us run it: our agency.', 'Our team becomes your marketing department, running every stage of the framework, from branding and your website to SEO, ads, social, '
           'leads and reviews, with plain-English reporting every month. <a href="/services/">See our services</a>.'),
          ('Build it with us: coaching.', 'You do the work, with an expert in your corner. One-on-one coaching builds your plan with you and keeps you accountable. '
           '<a href="/befirst-training/#coaching">See BeFirst Coaching</a>.'),
          ('Learn it yourself: training.', 'The BeFirst Community, our online course, the FirstSearch Blueprint and <a href="/events/">live workshops</a> teach you the same system '
           'we use with our partners. <a href="/befirst-training/">See BeFirst Training</a>.')],
    beliefs=[('Strategy beats size.', 'You don’t need a massive budget to win. You need a proven strategy.'),
             ('Authenticity always wins.', 'Trust isn’t built through gimmicks. It’s built through consistency.'),
             ('Growth is a system.', 'Any business can scale by improving the entire customer journey.')],
    values=[('Accountability.', 'We take full ownership of every decision, every dollar and every result.'),
            ('Collaboration.', 'We don’t work for you, we work with you. No black boxes, no surprises.'),
            ('Curiosity.', 'We stay genuinely invested in your business, always looking for the next way to help you grow.'),
            ('Partnership.', 'Long-term relationships rooted in trust and transparency, not short-term wins.')],
    outro='<p>Want to know who’s behind it all? <a href="/about-us/#team">Meet the team</a>, or read <a href="/why-choose-us/">why local businesses choose us</a>.</p>',
    take=['One connected system, the FirstSearch Framework, sits behind everything we do',
          'Three ways to work with us: we run it, we coach you, or you learn it yourself',
          'Strategy beats size, authenticity always wins, and growth is a system',
          'Accountability, collaboration, curiosity and partnership guide every relationship'],
    chapters=[('0:00', 'Who we are'), ('0:15', 'Let us run it: our agency'), ('0:32', 'Build it with us: coaching'), ('0:47', 'Learn it yourself: BeFirst Training'),
              ('1:02', 'What we believe'), ('1:22', 'Our core values'), ('1:38', 'Let’s talk')],
    transcript=[('0:00', 'Hi, I’m Chris Mitchell, owner of First Search Marketing. We’re a family-owned digital marketing agency in Hampton, New Hampshire, and we help local businesses become the first name their customers find, trust and choose. Everything we do runs on the FirstSearch Framework: four stages, one connected system.'),
                ('0:15', 'Most of our partners let us run it. Our team becomes your marketing department, handling your brand, website, SEO, ads, social, leads and reviews, with plain-English reporting every month.'),
                ('0:32', 'If you’d rather do the work yourself with an expert in your corner, our one-on-one coaching builds your plan with you and keeps you accountable.'),
                ('0:47', 'And if you want to learn the system on your own, BeFirst Training gives you the online course, the FirstSearch Blueprint, live workshops and our BeFirst Community.'),
                ('1:02', 'Whichever way you work with us, three beliefs guide everything we do. Strategy beats size: you don’t need a huge budget, you need a clear plan. Authenticity always wins: trust is built through consistency, not gimmicks. And growth is a system: real momentum comes from improving the whole customer journey.'),
                ('1:22', 'We hold ourselves to four values: accountability for every decision and every dollar, collaboration with no black boxes, curiosity about your business, and partnership for the long term.'),
                ('1:38', 'That’s First Search Marketing. If you’re ready to put your business first, let’s talk.')],
    ment=[('About First Search Marketing', '/about-us/'), ('Meet the team', '/about-us/#team'), ('The FirstSearch Framework', '/services/#framework'),
          ('Our services (let us run it)', '/services/'), ('BeFirst Coaching (build it with us)', '/befirst-training/#coaching'),
          ('BeFirst Training (learn it yourself)', '/befirst-training/'), ('Upcoming workshops', '/events/'), ('Why choose us', '/why-choose-us/'), ('Let’s talk', '/contact-us/')],
)

def bullets(items):
    """Check list with a bold lead-in; Icon List text takes inline HTML, so each line stays editable."""
    return icon_list([f'<b>{b}</b> {t}' for b, t in items], 'fas fa-check', 'fs-checks fs-vp-list')

MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
def video_cards(items):
    """Native related-video cards: cover image, Video pill + date, title, link (Loop Grid on the live site)."""
    cards = []
    for r in items:
        y, m, d = r['date'].split('-')
        cards.append(con(image('assets/img/design/chris-cutout.webp', 'fs-vp-cover', '100%', 'center', ''),
                         con(ns(H('Video', 'fs-vp-type'), H(f'{MON[int(m) - 1]} {int(d)}, {y}', 'fs-vp-meta'), d='row', gap_=10, align='center', mobile_col=False),
                             heading(r['title'], 'h3', 'fs-vp-ct3'), link_u('Watch the video', '/videos/'), gap_=10, p=pad(24)),
                         cls='fs-gcard fs-gcard--thin fs-gcard--hover fs-vp-card', gap_=0, p=pad(0), s={'width': {'unit': '%', 'size': 31, 'sizes': []}, 'width_mobile': {'unit': '%', 'size': 100, 'sizes': []}}))
    return row(*cards, gap_=24, align='stretch')

def video_fsm(v=V):
    # 1. header + player (light): back link, pills, centred title with the rule, lead, Video widget in the gradient frame
    head = section(con(H('← All videos', 'fs-vp-back', url='/videos/', align='center'),
                       ns(H('Video', 'fs-vp-type'), H(v['meta'], 'fs-vp-meta'), d='row', gap_=10, align='center', justify='center', mobile_col=False, wrap=True),
                       heading(v['title'], 'h1', 'fs-h1-rule fs-center', 'center'), text(v['lead'], 'fs-hero-lead', 'center'),
                       con(video('', 'assets/img/design/chris-cutout.webp', 'fs-video'), cls='fs-gcard', p=pad(18)),
                       gap_=18, align='center', s={'max_width': px(872)}),
                   cls='fs-geo', title='Header + player', bg_img=GEO, align='center')

    # 2. notes (white): about, three ways, beliefs, values, takeaways, chapters, transcript | presenter, mentioned, subscribe
    chapters = con(*[ns(H(t, 'fs-vp-ct'), H(l, 'fs-vp-cl'), d='row', gap_=16, align='center', mobile_col=False, cls='fs-vp-ch', p=pad(12, 16))
                     for t, l in v['chapters']], gap_=8)
    transcript = w('toggle', {'tabs': [{'_id': uid(), 'tab_title': 'Read the full transcript',
                                        'tab_content': ''.join(f'<p><b>{t} · Chris:</b> {l}</p>' for t, l in v['transcript'])}]}, 'fs-faq')
    notes = col(heading('About this video', 'h2'), text(v['intro']),
                heading('Three ways to work with us', 'h3', 'fs-vp-h3'), bullets(v['ways']),
                heading('What we believe', 'h3', 'fs-vp-h3'), bullets(v['beliefs']),
                heading('Our core values', 'h3', 'fs-vp-h3'), bullets(v['values']), text(v['outro']),
                heading('Key takeaways', 'h3', 'fs-vp-h3'), icon_list(v['take'], cls='fs-checks'),
                heading('Chapters', 'h3', 'fs-vp-h3'), chapters, transcript, wpct=62, gap_=14)
    side = col(con(heading('Presented by', 'p', 'fs-eyebrow'), image_box('assets/img/team/chris.webp', 'Chris Mitchell', 'Owner & Digital Partner', '', 'left', 'p'),
                   cls='fs-gcard fs-gcard--thin', p=pad(22), gap_=10),
               con(heading('Mentioned in this video', 'p', 'fs-eyebrow'), icon_list([l for l, _ in v['ment']], 'fas fa-arrow-right', 'fs-vp-ment', links=[u for _, u in v['ment']]),
                   cls='fs-gcard fs-gcard--thin', p=pad(22), gap_=8),
               con(heading('More like this', 'p', 'fs-eyebrow'), heading('Subscribe on YouTube.', 'h3'),
                   text('Short, practical marketing videos for local business owners, every [week].'), button('Subscribe on YouTube', '#', 'fs-btn-white'),
                   cls='fs-purple-card fs-dark', p=pad(26), gap_=10), wpct=34, gap_=20)
    notes_sec = section(row(notes, side, gap_=48, align='flex-start'), title='Notes', s={'boxed_width': px(1092)})

    # 3. more videos (light), quiz, CTA
    more = latest(lambda r: r['type'] == 'video')
    return [head, notes_sec,
            section(sec_head('More videos', 'Keep <span class="fs-gt">watching.</span>'), video_cards(more), link_u('See all resources', '/resources/'),
                    cls='fs-geo', title='More videos', bg_img=GEO, align='center'),
            quiz(),
            cta_banner('Ready to put your business first?', 'Book a free 30-minute call and we’ll show you where to start.')]
