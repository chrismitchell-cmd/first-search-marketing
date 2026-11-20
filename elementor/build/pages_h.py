"""Blog post: "Top 2027 marketing trends to scale your business" (blog-2027-marketing-trends.html), built only from
native Elementor widgets (no HTML widgets): Text Editor for paragraphs, lists and links, Headings for chips and labels,
Table of Contents and Share Buttons in the sidebar, Blockquote, Form. Paste it into a post in the Blog category."""
from comp import *
from pages_a import GEO
from pages_d import latest

def H(t, cls, tag='p', url=None, align=None):
    h = heading(t, tag, cls, align)
    if url: h['settings']['link'] = {'url': url, 'is_external': '', 'nofollow': ''}
    return h
def ns(*kids, cls='', **kw):
    return con(*kids, cls=(cls + ' fs-nostyle').strip(), **kw)

STAGE = {'brand': 'FirstBrand', 'thought': 'FirstThought', 'choice': 'FirstChoice', 'referral': 'FirstReferral'}
def meta(stages, belief):
    """Stage chip(s) linked to the stage pages, then the belief tag."""
    return ns(H('Stage', 'fs-bl-k'), *[H(plogo(k), 'fs-bl-stage', url=f'/first{k}/') for k in stages], H('Belief', 'fs-bl-k fs-bl-k2'), H(belief, 'fs-bl-belief'),
              d='row', gap_=10, align='center', wrap=True, mobile_col=False, cls='fs-bl-meta')
def doit(t):
    return con(H('Try this in 2027', 'fs-bl-doit-k'), text(f'<p>{t}</p>', 'fs-bl-doit-p'), cls='fs-bl-doit', gap_=4, p=pad(18, 22))
def h2(t): return heading(t, 'h2', 'fs-bl-h2 fs-plain')
def p(*paras): return text(''.join(f'<p>{x}</p>' for x in paras), 'fs-bl-p')

TRENDS = [
    ('1. Real people beat polished content', ['brand'], 'Authenticity always wins',
     ['AI can now produce a blog post, a stock-style photo or a slick ad in seconds. That means the internet is filling up with content that all looks and sounds the same. In 2027, the businesses that stand out will be the ones that look like themselves: real owners, real teams, real customers, real places.',
      'This is <a href="/firstbrand/">FirstBrand</a> work. Know what makes you different, say it the same way everywhere, and put your actual people at the center of it. A clear, consistent brand is also what every other trend on this list depends on.'],
     'Replace three stock photos on your website with real photos of your team, your space or your work. Then make sure your logo, colors and one-line description match on your website, Google profile and social pages.'),
    ('2. Be the answer, not just a search result', ['thought'], 'Strategy beats size',
     ['More customers are asking ChatGPT, Google’s AI Overviews and voice assistants questions like “who’s the best roofer near me?” and getting a short list of names back, before they ever click a link. The good news for local businesses: these tools favor clear, specific, trustworthy information over big ad budgets.',
      'Being that answer is <a href="/firstthought/">FirstThought</a>: getting found first, wherever customers look. AI can only repeat what you’ve clearly said, so pages that plainly answer what you do, where and for whom matter more than ever.'],
     'Write one page for each core service you offer, with a first paragraph that says exactly what it is, who it’s for and the towns you serve. Then ask an AI assistant about your business and see what it says.'),
    ('3. The map is still the front door', ['thought'], 'Strategy beats size',
     ['For local businesses, the Google map pack is still where most buying decisions start, and it’s one of the few places a small business can outrank a national brand. A complete, active Google Business Profile, consistent listings across the web and a steady flow of fresh reviews will keep doing more for most local businesses than almost any new channel.'],
     'Fill in every field of your Google Business Profile, choose your most specific category, add your services and post to it twice a month. Small, consistent effort here compounds.'),
    ('4. Short video from your own team', ['thought', 'choice'], 'Authenticity always wins',
     ['Short-form video isn’t new, but in 2027 it’s how people decide whether they like you before they ever call. The videos that work best for local businesses aren’t polished productions. They’re the owner explaining something useful, a team member showing how a job gets done, or a customer sharing what changed for them.',
      'Done consistently, video gets you found (FirstThought) and helps people choose you (<a href="/firstchoice/">FirstChoice</a>), because they already feel like they know you.'],
     'Film one 30 to 60 second video a week answering a question customers ask you all the time. Use your phone. Post it everywhere, including your Google profile.'),
    ('5. Speed to lead, with automation doing the heavy lifting', ['choice'], 'Growth is a system',
     ['Most lost leads aren’t lost to a competitor. They’re lost to silence. Someone fills out a form, nobody answers for a day, and they’ve already booked with whoever called back first. In 2027, the businesses that win will reply in minutes, not hours, and AI-assisted automation makes that possible without hiring more staff.',
      'This is FirstChoice: turning attention into booked business. An instant text back, a simple follow-up sequence and a CRM that shows every lead and where it came from will often grow revenue faster than doubling your ad spend.'],
     'Time how long it takes your business to respond to a new web inquiry. If it’s more than an hour, set up an automatic text and email reply, and a reminder for your team to call.'),
    ('6. Own your audience', ['choice', 'referral'], 'Strategy beats size',
     ['Ad costs keep climbing, privacy rules keep tightening and social platforms keep changing what they show. The one audience no platform can take away is the one you own: your email and text list, built from customers and people who’ve raised their hand.',
      'A simple, useful monthly email keeps you top of mind, brings past customers back and makes every future campaign cheaper. It’s one of the highest-return moves a local business can make, and it doesn’t need a big budget.'],
     'Make sure every customer and every lead lands in one list, with permission to contact them. Then send one genuinely useful email a month. No hard sell.'),
    ('7. Turn happy customers into your best marketing', ['referral'], 'Growth is a system',
     ['Reviews and referrals have always mattered. In 2027 they matter twice: people trust them more than ads, and Google and AI tools use them to decide who’s “best.” Most businesses have plenty of happy customers. They just never ask them in a way that’s easy.',
      'This is <a href="/firstreferral/">FirstReferral</a>: a friendly, automatic review request after every job, a simple referral thank-you and small touches that bring customers back. It’s the stage most businesses skip, and the one that makes every other stage cheaper.'],
     'Set up a two-tap review link and send it automatically after every job. Reply to every review, good or bad, within a few days.'),
]
MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def blog_cards(items):
    cards = []
    for r in items:
        y, m, d = r['date'].split('-')
        cards.append(con(con(image('assets/img/icons/idea.webp', 'fs-bl-cardico', None, 'center', ''), cls='fs-bl-cardtop', justify='center', align='center', p=pad(26)),
                         con(ns(H('Blog', 'fs-bl-type'), H(f'{r.get("meta", "")} · {MON[int(m) - 1]} {int(d)}, {y}', 'fs-bl-cmeta'), d='row', gap_=10, align='center', mobile_col=False),
                             heading(r['title'], 'h3', 'fs-bl-ct3'), link_u('Read the article', '/blog/'), gap_=10, p=pad(24)),
                         cls='fs-gcard fs-gcard--thin fs-gcard--hover fs-bl-card', gap_=0, p=pad(0), s={'width': PCT(31), 'width_mobile': PCT(100)}))
    return row(*cards, gap_=24, align='stretch')

def blog_2027():
    # 1. header (light): back link, pills, centred title + rule, lead, byline, featured image
    pills = ns(H('Blog', 'fs-bl-type'), H('The FirstSearch Framework', 'fs-bl-topic', url='/services/#framework'), H('Marketing strategy', 'fs-bl-topic', url='/services/'),
               d='row', gap_=8, align='center', justify='center', wrap=True, mobile_col=False)
    byline = ns(image('assets/img/team/chris.webp', 'fs-bl-avatar', None, 'center', 'Chris Mitchell'),
                con(H('Chris Mitchell', 'fs-bl-by-n'), H('Owner & Digital Partner', 'fs-bl-by-s'), gap_=0),
                con(H('[January 2027]', 'fs-bl-by-n'), H('9 min read', 'fs-bl-by-s'), gap_=0, cls='fs-bl-by-date'),
                d='row', gap_=14, align='center', mobile_col=False, cls='fs-bl-byline', p=pad(8, 22, 8, 8))
    head = section(con(H('← All articles', 'fs-bl-back', url='/resources/', align='center'), pills,
                       heading('Top 2027 marketing trends <span class="fs-gt">to scale your business.</span>', 'h1', 'fs-h1-rule fs-center', 'center'),
                       text('Every January brings a new list of “must-do” marketing trends. Most of them are noise. Here are the seven worth your time in 2027, and how each one fits into a system that actually grows a local business.', 'fs-hero-lead', 'center'),
                       byline, con(image('blog/2027-marketing-trends.webp', 'fs-bl-feat-img', '100%', 'center',
                                         'Top 2027 marketing trends to scale your business: Chris Mitchell in front of the FirstSearch Framework wheel'), cls='fs-gcard fs-bl-feat', p=pad(0)),
                       gap_=20, align='center', s={'max_width': px(1080)}),
                   cls='fs-geo', title='Article header', bg_img=GEO, align='center')

    # 2. article (white): contents + share | the post
    side = col(w('table-of-contents', {'title': 'In this article', 'headings_by_tags': ['h2'], 'marker_view': 'numbers', 'minimize_box': ''}, 'fs-toc'),
               heading('Share', 'p', 'fs-eyebrow'),
               w('share-buttons', {'share_buttons': [{'_id': uid(), 'button': 'facebook'}, {'_id': uid(), 'button': 'linkedin'}, {'_id': uid(), 'button': 'email'}],
                                   'view': 'icon', 'shape': 'circle', 'skin': 'framed'}),
               wpct=24, gap_=14, cls='fs-bl-side')
    body = [text('<p>We’ll be honest: we don’t chase trends. Our whole point of view is that marketing success comes from clear strategy, authentic brand alignment and continuous improvement of the entire customer journey, not hacks, trends or oversized budgets.</p>', 'fs-bl-dek'),
            p('So why write a trends post? Because some changes really are worth acting on. The trick is knowing which ones. A trend is only worth your time if it makes your system stronger. If it’s just something shiny to bolt on, skip it.'),
            con(con(image('assets/img/icons/idea.webp', '', None, 'center', ''), cls='fs-bl-callico', justify='center', align='center'),
                con(H('The short version', 'fs-bl-call-h'), text('<p>In 2027, the local businesses that grow will be the ones customers can find, trust and choose at every step: real, human brands that show up in AI answers and the map, follow up fast, own their audience and turn happy customers into their best marketing.</p>', 'fs-bl-call-p'), gap_=4),
                d='row', gap_=16, align='flex-start', mobile_col=False, cls='fs-bl-callout', p=pad(22, 24)),
            h2('How we chose these trends'),
            p('Every trend on this list passed the same test: our three beliefs about how businesses grow.'),
            text('<ul><li><b>Strategy beats size.</b> You don’t need a massive budget to win. You need a proven strategy. If a trend only works for big brands with big budgets, it’s not on this list.</li>'
                 '<li><b>Authenticity always wins.</b> Trust isn’t built through gimmicks. It’s built through consistency. If a trend asks you to be someone you’re not, it’s not on this list.</li>'
                 '<li><b>Growth is a system.</b> Any business can scale by improving the entire customer journey. So each trend below is matched to the stage of the <a href="/services/#framework">FirstSearch Framework</a> it strengthens.</li></ul>', 'fs-bl-p')]
    for n, (t, stages, belief, paras, act) in enumerate(TRENDS, 1):
        body += [h2(t), meta(stages, belief), p(*paras), doit(act)]
        if n == 4:   # Framework Quiz, halfway down
            body.append(con(con(H('Free Framework Quiz', 'fs-bl-q-k'), heading('Which stage is holding you back?', 'h3', 'fs-bl-q-h'),
                                text('Score your marketing across all four stages in about five minutes, then see exactly where to start.', 'fs-bl-q-p'), gap_=6),
                            button('Take the quiz', '/framework-quiz/', 'fs-btn-white'), d='row', gap_=24, align='center', cls='fs-purple-card fs-dark fs-bl-quiz', p=pad(28)))
    body += [h2('The real trend: a system, not a checklist'),
             p('Look at the list again. None of these work on their own. Real content needs a clear brand. AI search needs good pages and good reviews. Fast follow-up needs leads to follow up on. Reviews need customers who were looked after.',
               'That’s why we built the <a href="/services/#framework">FirstSearch Framework</a>: four stages, one connected system. Build the foundation (FirstBrand), get found first (FirstThought), get chosen (FirstChoice) and get referred (FirstReferral). Fix the weakest stage first, and every trend you add works harder.'),
             w('blockquote', {'blockquote_content': 'Don’t ask which trend to chase. Ask which stage of your customer journey is leaking, and fix that first.',
                              'author_name': 'Chris Mitchell', 'tweet_button': ''}, 'fs-pull'),
             h2('Three ways to put this to work in 2027'),
             p('However you like to work, there’s a way to make 2027 your strongest year yet:'),
             text('<ul><li><b>Let us run it.</b> Our team becomes your marketing department and puts every stage of the framework to work for you, with plain-English reporting every month. <a href="/services/">See our services</a>.</li>'
                  '<li><b>Build it with us.</b> You do the work, with an expert in your corner. One-on-one coaching builds your 2027 plan with you and keeps you accountable. <a href="/befirst-training/#coaching">See BeFirst Coaching</a>.</li>'
                  '<li><b>Learn it yourself.</b> The BeFirst Community, our online course and the FirstSearch Blueprint teach you the same system we use with our partners. Or join a free <a href="/events/">live workshop</a>. <a href="/befirst-training/">See BeFirst Training</a>.</li></ul>', 'fs-bl-p'),
             p('Not sure which is right for you? <a href="/contact-us/">Book a free 30-minute call</a> and we’ll look at your marketing together. No pitch, just a plan.'),
             ns(H('Topics', 'fs-bl-k'), *[H(t, 'fs-bl-topic', url=u) for t, u in [('The FirstSearch Framework', '/services/#framework'), ('Branding & content', '/services/branding-content-creation/'),
                                                                                   ('SEO', '/services/seo/'), ('Lead Generation', '/services/lead-generation/'), ('Reviews & Referrals', '/services/reviews-referrals/')]],
                d='row', gap_=8, align='center', wrap=True, mobile_col=False, cls='fs-bl-tags')]
    article = section(row(side, col(*body, wpct=70, gap_=16), gap_=56, align='flex-start'), title='Article', s={'boxed_width': px(1160)})

    # 3. author (white), newsletter (gradient), related (light), CTA
    author = section(row(image('assets/img/team/chris.webp', 'fs-bl-author-img', None, 'center', 'Chris Mitchell'),
                         con(H('Written by', 'fs-bl-q-k'), heading('Chris Mitchell', 'h3', 'fs-bl-author-h'),
                             text('Owner and Digital Partner at First Search Marketing. Chris builds every partner’s strategy and teaches the FirstSearch Framework at workshops across New Hampshire.', 'fs-bl-p'),
                             link_u('Meet the team', '/about-us/#team'), gap_=6),
                         gap_=28, align='center', cls='fs-gcard fs-bl-author', p=pad(28)),
                     title='Author', s={'boxed_width': px(920)},
                     p={'unit': 'px', 'top': '0', 'right': '24', 'bottom': '80', 'left': '24', 'isLinked': False})
    news_form = form([('email', 'Email address', True, 'you@business.com')], 'Subscribe', 'Newsletter', 'fs-news-form')
    news_form['settings'].update({'show_labels': '', 'button_width': '30'}); news_form['settings']['form_fields'][0]['width'] = '70'
    news = section(row(col(heading('One useful marketing idea a week.', 'h2', 'fs-bl-news-h'),
                           text('Real stories and practical tips like this one, straight to your inbox. No fluff, unsubscribe any time.', 'fs-bl-news-p'), wpct=52, gap_=8),
                       col(news_form, wpct=44), gap_=40, cls='fs-grad fs-bl-news', p=pad(40, 44)), title='Newsletter', cls='fs-geo', bg_img=GEO)
    related = section(sec_head('Keep reading', 'More from <span class="fs-gt">the blog.</span>'), blog_cards(latest(lambda r: r['type'] == 'blog')),
                      link_u('See all resources', '/resources/'), cls='fs-geo', title='Related posts', bg_img=GEO, align='center')
    return [head, article, author, news, related,
            cta_banner('Ready to make 2027 your strongest year?', 'Book a free 30-minute call and we’ll find the stage holding your business back.')]
