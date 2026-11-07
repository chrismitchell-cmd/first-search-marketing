"""Data-driven templates: one page per service, one per framework stage, and separate podcast / video singles.
Content comes from data/site-data.json, extracted from the approved prototypes (services.html, pillars.html, resource.html)."""
import json, os, re
from comp import *
from pages_a import SERVICES as SVC_LIST, GEO
from pages_b import rel_cards, STAGES_JOB
from pages_c import back

D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'site-data.json')))
SDATA = {s['slug']: s for s in D['SERVICES']}
ORDER = ['brand', 'thought', 'choice', 'referral']
ST = {'brand': (1, 'FirstBrand', 'Build the foundation'), 'thought': (2, 'FirstThought', 'Get found first'),
      'choice': (3, 'FirstChoice', 'Get chosen'), 'referral': (4, 'FirstReferral', 'Get referred')}
# data slug -> live URL slug and icon (from the site's service list)
URL = {'branding': 'branding-content-creation'}
ICON = {s[0]: s[2] for s in SVC_LIST}
def url_slug(s): return URL.get(s, s)
def svc_icon(s): return f'assets/img/icons/{ICON[url_slug(s)]}.webp'
def svc_url(s): return f'/services/{url_slug(s)}/'
H1 = {'branding': ['A brand people', 'trust on sight.'], 'website': ['A website that', 'brings in business.'],
      'analytics': ['Know exactly what’s', 'bringing in customers.'], 'crm': ['Never lose', 'another lead.'],
      'seo': ['Be the first business', 'customers find.'], 'advertising': ['Ads that pay', 'for themselves.'],
      'social-media': ['Social media that', 'brings in customers.'], 'local-ties': ['Be the name everyone', 'in town knows.'],
      'lead-generation': ['Turn visitors into', 'real leads.'], 'marketing-automation': ['Follow-up that', 'runs on its own.'],
      'loyalty': ['Turn one-time buyers', 'into regulars.'], 'reviews-referrals': ['Make happy customers', 'your best marketing.']}

def q(s):  # curly apostrophes, like the rest of the templates
    return s.replace("'", '’')
def lc(s): return s.lower().replace('seo', 'SEO').replace('crm', 'CRM')
def stages_text(st):
    l = [ST[k][1] for k in st]
    return l[0] if len(l) == 1 else ', '.join(l[:-1]) + ' and ' + l[-1]
def chips(st, size=15): return ' '.join(f'<span class="fs-plogo-chip">{plogo(k, size=size)}</span>' for k in st)

# Included-item icons: keyword -> one of the uploaded icon files
KW = [(r'audit|discovery|research|interview', 'growth'), (r'strateg|plan|roadmap|messag|position|value statement', 'idea'), (r'review', 'conversation'),
      (r'referral', 'handshake'), (r'loyal|reward|vip|perk', 'team'), (r'email|newsletter', 'email'), (r'\btext|sms|call|phone', 'conversation'),
      (r'automat|workflow|follow-up|nurture|sequence', 'automation'), (r'logo|identity|visual|guideline|template', 'idea'), (r'video|film|photo|content|copy|post|blog', 'social'),
      (r'report|dashboard|tracking|analytic|metric|measur|attribution', 'growth'), (r'crm|pipeline|contact|lead scor', 'network'), (r'\bai\b|answer', 'idea'),
      (r'google business|map|local|listing|citation', 'local'), (r'seo|keyword|rank|search', 'analytics'), (r'\bads?\b|campaign|retarget|paid|budget|bid', 'advertising'),
      (r'social|community|engag|influenc', 'social'), (r'event|sponsor|partner|chamber|network', 'handshake'), (r'lead|magnet|offer|form|landing', 'lead-gen'),
      (r'website|page|site|speed|mobile|design|build', 'seo'), (r'test|optimi|conver', 'growth')]
def icon_for(t, i):
    l = t.lower()
    for pat, ic in KW:
        if re.search(pat, l): return f'assets/img/icons/{ic}.webp'
    return f'assets/img/icons/{["trust", "idea", "investment", "growth"][i % 4]}.webp'

MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
RT = {'blog': ('Blog', 'Read the article'), 'case': ('Case study', 'Read the case study'), 'podcast': ('Podcast', 'Listen to the episode'), 'video': ('Video', 'Watch the video')}
RURL = {'blog': '/blog/', 'case': '/case-studies/', 'podcast': '/podcast/', 'video': '/videos/'}
def res_cards(items):
    out = []
    for r in items:
        y, m, d = r['date'].split('-'); dt = f'{MON[int(m) - 1]} {int(d)}, {y}'
        meta = dt if r['type'] in ('video', 'case') else f'{r["meta"]} · {dt}'
        out.append((r['type'], RT[r['type']][0], meta, q(r['title']), RT[r['type']][1], RURL[r['type']]))
    return rel_cards(out)
def latest(pred, n=3):
    rs = sorted([r for r in D['RESOURCES'] if pred(r)], key=lambda r: r['date'], reverse=True)
    if len(rs) < n: rs += [r for r in sorted(D['RESOURCES'], key=lambda r: r['date'], reverse=True) if r not in rs][:n - len(rs)]
    return rs[:n]

def case_rows(proof): return tuple((q(s), '[XX]', q(b)) for b, s in proof)

# ======================= SERVICE (one per service) =======================
def service(slug):
    s = SDATA[slug]; name = s['name']; st = s['stages']; multi = len(st) > 1
    h1 = H1[slug]
    def stage_card(k):
        R = s['role'][k]
        return con(con(html(f'<span class="fs-plogo-chip">{q(name)} in {plogo(k, size=24)}</span>'), heading(q(R['h']), 'h3'), text(q(R['d'])),
                       heading('What we do', 'p', 'fs-eyebrow'), icon_list([q(x) for x in R['items']], cls='fs-checks'),
                       text(f'<p><small>The number it moves</small><br><b>{q(R["metric"])}</b></p>', 'fs-soft-box'),
                       link_u(f'Explore the {ST[k][1]} stage', f'/first{k}/'), cls='fs-gcard', p=pad(36), gap_=14), p=pad(0))
    right = nested_tabs([(f'first{k}', stage_card(k)) for k in st], 'fs-stage-tabs') if multi else stage_card(st[0])
    fw = section(sec_head('Where this fits in your framework', q(s['roleTitle']), q(s['roleLead'])),
                 row(col(image(f'wheels/service-{slug}.webp', '', '100%', 'center',
                               f'The FirstSearch Framework wheel with the {name} spots highlighted'), wpct=45),
                     col(right, wpct=55), gap_=48),
                 button('Let’s Talk!', '/contact-us/', 'fs-btn-lg', 'center'), cls='fs-dark fs-dark-round', title='Framework fit', gap_=40)
    fw['settings']['_element_id'] = 'framework'
    inc_cards = []
    for i, (t, d, ks) in enumerate(s['included']):
        kids = [image_box(icon_for(t + ' ' + d, i), q(t), q(d), 'fs-tile', 'left')]
        if multi: kids.append(html(f'<p>{chips(ks, 13)}</p>'))
        inc_cards.append(col(*kids, wpct=31, cls='fs-gcard fs-gcard--thin', p=pad(20), gap_=8))
    rel = [SDATA[r] for r in s['related']]
    return [
        hero(f'{name} · {stages_text(st)}', f'{q(h1[0])} <span class="fs-gt">{q(h1[1])}</span>', q(s['lead']),
             link=('See how it fits the framework', '#framework'), media=vid()),
        trust([('4.9★', 'on Google · [XX] reviews'), ('10+', 'years in digital marketing'), ('NH', 'Family-owned in Hampton')]),
        problem('Sound familiar?', q(s['probTitle']),
                [(icon_for(h + ' ' + p, i).split('/')[-1], q(h), q(p)) for i, (h, p) in enumerate(s['problems'])],
                f'{q(s["close"][0])} <span class="fs-sky">{q(s["close"][1])}</span>', numbered=True,
                art=art_card(image(svc_icon(slug), 'fs-art-tile', 150, 'center', ''), q(s['close'][1]),
                             f'{q(s["close"][0])} We give {lc(name)} a clear job, and a number to hit.', st)),
        fw,
        section(sec_head('What’s included', f'Everything it takes to <span class="fs-gt">do {lc(name)} properly.</span>', align='left'),
                row(*inc_cards, gap_=20, wrap=True, align='stretch'),
                text(f'<p><b>{q(s["platforms"][0])}:</b> {q(s["platforms"][1])}</p>', 'fs-platforms'),
                cls='fs-geo', title='What’s included', bg_img=GEO),
        steps('', 'Your first 90 days.', f'What the first three months of {lc(name)} look like with our team.',
              [(w, q(h), q(p)) for w, h, p in s['process']]),
        case_reviews(h3=q(s['proofH']), rows=case_rows(s['proof'])),
        three_ways('Three ways to <span class="fs-gt">get it done.</span>', 'Have our team run it, learn to do it yourself, or do it yourself with a coach in your corner.', eb='Ways to get this done'),
        section(sec_head('Works best with', f'{name} is stronger as part of the system.'),
                row(*[col(image_box(svc_icon(r['slug']), r['name'], q(r['short']), 'fs-tile', 'top'), html(f'<p>{chips(r["stages"], 13)}</p>'),
                          link_u(f'Explore {r["name"]}', svc_url(r['slug'])), wpct=31, cls='fs-gcard', p=pad(26), gap_=8) for r in rel],
                    gap_=24, align='stretch'), cls='fs-dark', title='Related services'),
        section(sec_head('From our resources', f'Learn more <span class="fs-gt">about {lc(name)}</span>'),
                res_cards(latest(lambda r: s['tag'] in r['tags'])),
                link_u(f'See all {name} resources', '/resources/'), cls='fs-geo', title='Resources', bg_img=GEO, align='center'),
        faq(f'{name} <span class="fs-gt">questions</span>', [(q(a), q(b)) for a, b in s['faq']] + [
            (f'Can I buy {name} on its own?', f'No. Every service is delivered as part of a FirstSearch partnership, because {lc(name)} works best alongside the rest of your marketing system. Your plan includes every service your business needs for one fixed monthly retainer.')]),
        cta_banner(q(s['final'][0]), q(s['final'][1])),
    ]

# ======================= FRAMEWORK STAGE (one per stage) =======================
SELFCHECK = '''<div class="fs-selfcheck" data-verdicts='%s'>
<ul>%s</ul>
<div class="fs-sc-result"><p class="fs-sc-score"><b>0</b> of %d</p><h3>%s</h3><p class="fs-sc-sub">%s</p>
<a class="elementor-button" href="/framework-quiz/">Take the full Framework Quiz</a></div></div>
<script>(function(){var r=document.currentScript.previousElementSibling,v=JSON.parse(r.getAttribute('data-verdicts')),b=r.querySelector('.fs-sc-score b'),h=r.querySelector('.fs-sc-result h3'),p=r.querySelector('.fs-sc-sub');
r.addEventListener('change',function(){var n=r.querySelectorAll('input:checked').length,x=v[n<=2?0:n<=4?1:2];b.textContent=n;h.textContent=x[0];p.textContent=x[1];});})();</script>'''
def stage(k):
    P = D['P'][k]; n, label, sub = ST[k]
    nav = [s for s in SDATA if k in SDATA[s]['stages']]
    verd = json.dumps([[q(a), q(b)] for a, b in P['verdicts']]).replace("'", '&#39;')
    sc = SELFCHECK % (verd, ''.join(f'<li><label><input type="checkbox"> <span>{q(x)}</span></label></li>' for x in P['stmts']),
                      len(P['stmts']), q(P['verdicts'][0][0]), q(P['verdicts'][0][1]))
    here = '<ol class="fs-here">' + ''.join(
        f'<li class="{"on" if o == k else ""}"><a href="/first{o}/"><i>{ST[o][0]}</i>{plogo(o)}<small>{ST[o][2]}</small></a></li>' for o in ORDER) + '</ol>'
    check = section(con(row(col(eyebrow('Self-check'), heading(f'How strong is <span class="fs-gt">your {label}?</span>'),
                                text('Tick every statement that’s true for your business today.'), wpct=40),
                            col(html(sc), wpct=58), gap_=40, align='flex-start'), cls='fs-gcard', p=pad(56), s={'padding_mobile': pad(28)}),
                    cls='fs-geo', title='Self-check', bg_img=GEO)
    check['settings']['_element_id'] = 'check'
    j1, _, j2 = q(P['jTitle']).partition('. ')
    def tog_col(t):
        h, p, items = t
        return col(heading(h, 'h3'), text(q(p)), *[image_box(svc_icon(s), SDATA[s]['name'], q(d), 'fs-tile') for s, d in items],
                   wpct=32, cls='fs-gcard', p=pad(26), gap_=12)
    center = col(image(f'wheels/stage-{k}.webp', '', '100%', 'center', f'You are here: {label} on the FirstSearch Framework'),
                 heading(q(P['tog'][1][0]), 'h3', '', 'center'), text(q(P['tog'][1][1]), '', 'center'), wpct=28, gap_=8)
    per = {2: 48, 3: 31, 4: 23}.get(len(nav), 23)
    return [
        hero(f'The FirstSearch Framework · Stage {n}: {label}', f'{q(P["h1"][0])} <span class="fs-gt">{q(P["h1"][1])}</span>', q(P['lead']),
             link=('Take the 60-second self-check', '#check'), media=vid()),
        section(row(col(image(f'wheels/stage-{k}-numbered.webp', '', '100%', alt=f'The FirstSearch Framework, stage {n} of 4 ({label}) highlighted'), wpct=36),
                    col(eyebrow('You are here'), heading(f'Stage {n} of 4 in the FirstSearch Framework.'), html(here), wpct=60), gap_=48),
                cls='fs-dark', title='You are here'),
        problem('What it looks like when this stage is weak', f'Signs {label} is <span class="fs-gt">holding you back.</span>',
                [(icon_for(h + ' ' + p, i).split('/')[-1], q(h), q(p)) for i, (h, p) in enumerate(P['weak'])],
                f'{j1}.{" <span class=\"fs-sky\">" + j2 + "</span>" if j2 else ""}', numbered=True,
                art=art_card(html(f'<span class="fs-art-num">{n}</span>'), q(P['jTitle']), q(P['jLead']), [k])),
        check,
        section(sec_head('Services in this stage', q(P['sTitle']), f'Each one has a specific job in {label}. Select a service to see everything it includes.'),
                row(*[col(image_box(svc_icon(s), SDATA[s]['name'], q(P['svc'][s]), 'fs-tile', 'top'),
                          html(f'<p><small>Also in</small> {chips([o for o in SDATA[s]["stages"] if o != k], 13)}</p>') if len(SDATA[s]['stages']) > 1 else None,
                          link_u(f'See {SDATA[s]["name"]}', svc_url(s)), wpct=per, cls='fs-gcard', p=pad(24), gap_=8) for s in nav],
                    gap_=20, align='stretch', wrap=True),
                button('Let’s Talk!', '/contact-us/', 'fs-btn-lg', 'center'), cls='fs-dark fs-dark-round', title='Services in this stage', gap_=32),
        section(sec_head('How they work together', q(P['tTitle']), q(P['tLead'])),
                row(tog_col(P['tog'][0]), center, tog_col(P['tog'][2]), gap_=24), cls='fs-geo', title='How they work together', bg_img=GEO),
        section(sec_head('What we measure', q(P['mTitle'])),
                row(*[col(heading(q(h), 'h3'), text(q(d)), text(f'<p><small>{q(src)}</small></p>', 'fs-eyebrow'), wpct=23, gap_=6) for h, d, src in P['metrics']],
                    gap_=24, align='stretch', wrap=True), cls='fs-grad', title='What we measure'),
        case_reviews(h3=q(P['proofH']), rows=case_rows(P['proof'])),
        three_ways('Three ways to get <span class="fs-gt">this stage working.</span>', 'Have our team build it for you, learn the system yourself, or get guided by us.', eb='Ways to get this done'),
        faq('Questions about <span class="fs-gt">this stage</span>', [(q(a), q(b)) for a, b in P['faq']] + [
            ('Can I hire you for just this stage?', f'Every partnership covers the full framework, with priorities set around your weakest stage. If {label} is where you’re losing customers, that’s where your plan starts. Prefer to work on it yourself? The {label} module in the BeFirst Community covers it step by step.')]),
        cta_banner(q(P['final'][0]), q(P['final'][1])),
    ]

# ======================= PODCAST EPISODE / VIDEO (separate singles) =======================
MD = {
 'podcast': dict(back=('All podcast episodes', '/podcast/'), pill='Podcast', meta='Episode [24] · October 2, 2026 · [42] min',
     title='Ep. 24: <span class="fs-gt">Strategy beats size.</span>', lead='Why the local businesses that win aren’t the ones with the biggest budgets, and the three decisions that matter more than spend.',
     notes='In this episode', kind='episode', peopleH='On this episode',
     summary=['Chris and [guest name] talk about why most small businesses don’t fail from lack of effort but from lack of clarity, and how a simple framework beats a bigger budget.',
              'They walk through a real example of a [industry] business that doubled its leads without spending more on ads, just by fixing what happened after someone found them.'],
     take=['A bigger ad budget can’t fix a leaky website or slow follow-up', 'Pick the one stage of the customer journey that’s weakest and fix that first', 'Track leads and revenue, not impressions and likes'],
     chapters=[('0:00', 'Welcome and this week’s question'), ('3:05', 'Why effort isn’t the problem'), ('10:12', 'The three decisions that matter more than budget'),
               ('21:30', 'Case example: doubling leads without more ad spend'), ('33:30', 'Your one action for this week')],
     people=[('assets/img/team/chris.webp', 'Chris Mitchell', 'Host · Owner & Digital Partner'), ('assets/img/design/bg-geometric.jpg', '[Guest name]', '[Title, Business]')],
     ment=[('The FirstSearch Framework', '/services/#framework'), ('FirstChoice: turning attention into booked business', '/firstchoice/'), ('Free Framework Quiz', '/framework-quiz/')],
     sub=('Never miss an episode', 'New episodes every [other Tuesday].', 'Practical marketing for local business owners, in about 30 minutes.', 'Subscribe'),
     more=('More episodes', 'Keep <span class="fs-gt">listening.</span>')),
 'video': dict(back=('All videos', '/videos/'), pill='Video', meta='October 7, 2026 · 10:24',
     title='The FirstSearch Framework <span class="fs-gt">in 10 minutes.</span>', lead='A quick, whiteboard-style walkthrough of the four stages of the FirstSearch Framework, and how to spot which one is holding your business back.',
     notes='About this video', kind='video', peopleH='Presented by',
     summary=['Chris walks through FirstBrand, FirstThought, FirstChoice and FirstReferral, with one real example for each, then shows how they connect into one system instead of four separate projects.'],
     take=['Marketing works as a system across the whole customer journey', 'Each stage depends on the one before it, so start with the foundation', 'Your weakest stage limits the results of every other stage'],
     chapters=[('0:00', 'Why most marketing feels random'), ('1:12', 'FirstBrand: build the foundation'), ('3:35', 'FirstThought: get found first'),
               ('5:58', 'FirstChoice: get chosen'), ('8:00', 'FirstReferral: get referred'), ('9:30', 'Finding your weakest stage')],
     people=[('assets/img/team/chris.webp', 'Chris Mitchell', 'Owner & Digital Partner')],
     ment=[('The FirstSearch Framework', '/services/#framework'), ('Upcoming workshop: the Framework in 60 minutes', '/events/'), ('Free Framework Quiz', '/framework-quiz/')],
     sub=('More like this', 'Subscribe on YouTube.', 'Short, practical marketing videos for local business owners, every [week].', 'Subscribe on YouTube'),
     more=('More videos', 'Keep <span class="fs-gt">watching.</span>')),
}
def media(mode):
    d = MD[mode]
    if mode == 'podcast':
        player = con(row(con(html('<div class="fs-embed-ph" style="min-height:0;aspect-ratio:1/1">🎙<br><b>The FirstSearcher</b><br>Podcast<br><small>[Show artwork]</small></div>'),
                             s={'width': PCT(26), 'width_mobile': PCT(100)}),
                         con(heading('The FirstSearcher Podcast · Episode [24]', 'p', 'fs-eyebrow'), heading(re.sub('<[^>]+>', '', d['title']), 'h2'),
                             html('<div class="fs-embed-ph">[Podcast host embed: paste your Buzzsprout, Spotify or similar episode player here]</div>'),
                             html('<p class="fs-card-meta"><b>Listen on</b> <a href="#">Apple Podcasts</a> · <a href="#">Spotify</a> · <a href="#">YouTube</a> · <a href="#">RSS</a></p>'),
                             gap_=12, s={'width': PCT(72), 'width_mobile': PCT(100)}), gap_=24, align='center'),
                     cls='fs-gcard', p=pad(24))
    else:
        player = con(video('', 'assets/img/design/chris-cutout.webp', 'fs-video'), cls='fs-gcard', p=pad(18))
    notes = col(heading(d['notes'], 'h2'), text(''.join(f'<p>{p}</p>' for p in d['summary'])),
                heading('Key takeaways', 'h3'), icon_list(d['take'], cls='fs-checks'),
                heading('Chapters', 'h3'), html('<ol class="fs-chapters">' + ''.join(f'<li><span>{t}</span> {l}</li>' for t, l in d['chapters']) + '</ol>'),
                w('toggle', {'tabs': [{'_id': uid(), 'tab_title': 'Read the full transcript',
                                       'tab_content': f'<p>[Full transcript, generated from the {d["kind"]} and lightly edited. Helps SEO and accessibility.]</p>'}]}, 'fs-faq'),
                wpct=62, gap_=14)
    sb = d['sub']
    side = col(con(heading(d['peopleH'], 'p', 'fs-eyebrow'), *[image_box(img, n, r, '', 'left', 'p') for img, n, r in d['people']], cls='fs-gcard fs-gcard--thin', p=pad(22), gap_=10),
               con(heading(f'Mentioned in this {d["kind"]}', 'p', 'fs-eyebrow'), icon_list([l for l, _ in d['ment']], 'fas fa-arrow-right', links=[u for _, u in d['ment']]),
                   cls='fs-gcard fs-gcard--thin', p=pad(22), gap_=8),
               con(heading(sb[0], 'p', 'fs-eyebrow'), heading(sb[1], 'h3'), text(sb[2]), button(sb[3], '#', 'fs-btn-white'), cls='fs-purple-card fs-dark', p=pad(26), gap_=10),
               wpct=34, gap_=20)
    cta = 'Listen to the episode' if mode == 'podcast' else 'Watch the video'
    more = latest(lambda r: r['type'] == mode and 'Strategy beats size' not in r['title'] and '10 minutes' not in r['title'])
    return [
        section(con(html(back(*d['back'])), html(f'<p><span class="fs-type fs-type--{mode}">{d["pill"]}</span> {d["meta"]}</p>'),
                    heading(d['title'], 'h1', 'fs-h1-rule'), text(d['lead'], 'fs-hero-lead'), player, gap_=18, s={'max_width': px(872)}),
                cls='fs-geo', title='Header + player', bg_img=GEO, align='center'),
        section(row(notes, side, gap_=48, align='flex-start'), title='Notes', s={'boxed_width': px(1092)}),
        section(sec_head(d['more'][0], d['more'][1]), res_cards(more), link_u('See all resources', '/resources/'),
                cls='fs-geo', title=d['more'][0], bg_img=GEO, align='center'),
        quiz(),
        cta_banner('Ready to put this into practice?', 'Book a free 30-minute call and we’ll show you where to start.'),
    ]
def podcast(): return media('podcast')
def video_page(): return media('video')
