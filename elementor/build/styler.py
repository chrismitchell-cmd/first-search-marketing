"""Styling pass: writes the approved HTML's typography, colours and section spacing into each template
as native Elementor settings, linked to Global Colors / Global Fonts so they can be edited in Site Settings.

Source: data/proto-styles.json (measured from the HTML prototypes at 1440 / 1024 / 390 px).
- Widgets: matched to the prototype by their text; unmatched widgets take the style most often seen for the
  same role (widget, tag, classes, light/dark surface).
- Typography: grouped into Global Font presets (used 3+ times) or set inline on the widget.
- Colours: linked to Global Colors.
- Sections: top/bottom padding per device and centred section-head width from the matching HTML section."""
import json, os, re, html as H, hashlib
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(HERE, 'data', 'proto-styles.json')))

# ---------------------------------------------------------------- Global Colors
SYSTEM_COLORS = [('primary', 'Primary', '#250762'), ('secondary', 'Secondary', '#3299D5'), ('text', 'Text', '#1C1B22'), ('accent', 'Accent', '#174FA2')]
CUSTOM_COLORS = [
    ('fsbody', 'Body text', '#2F2E36'), ('fsmuted', 'Muted text', '#6B6A72'), ('fsskyink', 'Sky (small text)', '#1F78B4'),
    ('fswhite', 'White', '#FFFFFF'), ('fswhite92', 'White 92%', '#FFFFFFEB'), ('fswhite80', 'White 80%', '#FFFFFFCC'), ('fswhite70', 'White 70%', '#FFFFFFB3'),
    ('fsaqua', 'Aqua', '#72CCD8'), ('fsicesky', 'Light sky (on purple)', '#8FD5EE'), ('fslilac', 'Lilac (on purple)', '#D8D6EE'),
    ('fsgold', 'Star gold', '#F4B400'), ('fsdeep', 'Deep purple', '#1A0446'), ('fsbg', 'Page background', '#F8F7F7'),
    ('fssoft', 'Soft grey', '#F4F4F6'), ('fstint', 'Blue tint', '#EEF0F9'), ('fsgrey', 'Grey', '#D9D8D7'), ('fsline', 'Line', '#E3E2EA'),
]
SYSTEM_IDS = {c[0] for c in SYSTEM_COLORS}
HEX_OF = {i: hx for i, _, hx in SYSTEM_COLORS + CUSTOM_COLORS}
def _rgba(c):
    m = re.match(r'rgba?\(([^)]+)\)', c or '')
    if not m: return None
    v = [float(x) for x in m.group(1).split(',')]
    return (int(v[0]), int(v[1]), int(v[2]), v[3] if len(v) > 3 else 1.0)
def _hex(rgba):
    r, g, b, a = rgba
    return '#%02X%02X%02X' % (r, g, b) + ('' if a >= .999 else '%02X' % round(a * 255))
PALETTE = {}
for cid, _, hx in SYSTEM_COLORS + CUSTOM_COLORS:
    h = hx.lstrip('#'); a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
    PALETTE[(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))] = PALETTE.get((int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)), []) + [(a, cid)]
def color_ref(css_color):
    """-> ('global', id) or ('hex', '#..') or None"""
    v = _rgba(css_color)
    if not v: return None
    r, g, b, a = v
    opts = PALETTE.get((r, g, b))
    if opts:
        best = min(opts, key=lambda o: abs(o[0] - a))
        if abs(best[0] - a) <= .06: return ('global', best[1])
    if (r, g, b) == (142, 216, 240): return ('global', 'fsicesky')
    if (r, g, b) in ((201, 198, 234), (228, 226, 245)): return ('global', 'fslilac')
    return ('hex', _hex(v))

# ---------------------------------------------------------------- text helpers
def norm(t):
    t = H.unescape(re.sub(r'<br\s*/?>', '', t or ''))
    t = re.sub(r'<[^>]+>', '', t)
    return re.sub(r'\s+', ' ', t.replace('‘', "'").replace('’', "'").replace('“', '"').replace('”', '"').replace(' ', ' ')).strip().lower()
def paras(html_):
    ps = re.findall(r'<p[^>]*>(.*?)</p>', html_ or '', re.S)
    return [norm(p) for p in ps] if ps else [norm(html_)]

def strip_ph(t): return re.sub(r'\s+', ' ', re.sub(r'\s*\[[^\]]*\]\s*', ' ', t)).strip()
STRIPPED = {pk: {strip_ph(k): k for k in pg['d']['text']} for pk, pg in P.items()}
BTN_TAGS = ('a', 'button', 'span')
def tag_ok(part, tag):
    if part == 'button': return tag in BTN_TAGS
    if part == 'q': return True
    if part == 'item': return tag not in ('button', 'label')
    return tag not in ('button', 'a', 'label', 'option', 'select', 'input')
def lookup(page, txt, n=0, part=None):
    st = _lookup(page, txt, n, part)
    if st or not txt: return st
    # the design shows placeholders without brackets: "[30-minute]" -> "30-minute"
    nb = re.sub(r'\s+', ' ', txt.replace('[', '').replace(']', '')).strip()
    if nb != txt:
        st = _lookup(page, nb, n, part)
        if st and st.get('d'): return st
        for pk in P:
            if pk != page:
                st = _lookup(pk, nb, 0, part)
                if st and st.get('d'): return st
    alt = strip_ph(txt)
    if alt and alt != txt and len(alt) > 3:
        k = STRIPPED.get(page, {}).get(alt) or next((v.get(alt) for v in STRIPPED.values() if v.get(alt)), None)
        if k: return _lookup(page, k, n, part)
    return None
def _lookup(page, txt, n=0, part=None):
    """Style for this text: {d:{..}, t:{..}, m:{..}} from the same page first (n-th occurrence, so repeated
    text such as several "Let's Talk!" buttons each get their own size), else the most common elsewhere."""
    if not txt: return None
    def pick(lst, i):
        if lst and part: lst = [x for x in lst if tag_ok(part, x['tag'])] or None
        return lst[min(i, len(lst) - 1)] if lst else None
    def from_page(pk, i=0):
        pg = P.get(pk)
        if not pg or txt not in pg['d']['text']: return None
        return {w: pick(pg[w]['text'].get(txt), i) for w in ('d', 't', 'm')}
    s = from_page(page, n)
    if s: return s
    seen = Counter(); keep = {}
    for pk in P:
        s = from_page(pk)
        if s:
            k = json.dumps(s['d'], sort_keys=True); seen[k] += 1; keep[k] = s
    return keep[seen.most_common(1)[0][0]] if seen else None

# ---------------------------------------------------------------- widget parts
# (part name, settings prefix for typography, colour setting key, text getter)
def parts(w):
    s, k = w['settings'], w.get('widgetType')
    if k == 'heading': return [('title', 'typography', 'title_color', [norm(s.get('title'))])]
    if k == 'text-editor':
        if 'fs-prose' in s.get('_css_classes', ''): return [('prose', 'typography', 'text_color', [])]   # long-form article text
        return [('text', 'typography', 'text_color', [norm(s.get('editor'))] + paras(s.get('editor')))]
    if k == 'button': return [('button', 'typography', None, [norm(s.get('text'))])]
    if k == 'icon-list': return [('item', 'icon_typography', 'text_color', [norm(i.get('text')) for i in s.get('icon_list', [])])]
    if k == 'image-box': return [('ibtitle', 'title_typography', 'title_color', [norm(s.get('title_text'))]),
                                 ('ibdesc', 'description_typography', 'description_color', [norm(s.get('description_text'))])]
    if k == 'counter': return [('cnum', 'typography_number', 'number_color', [norm(f"{s.get('prefix', '')}{s.get('ending_number', '')}{s.get('suffix', '')}")]),
                               ('ctitle', 'typography_title', 'title_color', [norm(s.get('title'))])]
    if k in ('accordion', 'toggle'): return [('q', 'title_typography', None, [norm(t.get('tab_title')) for t in s.get('tabs', [])]),
                                             ('a', 'content_typography', 'content_color', [x for t in s.get('tabs', []) for x in paras(t.get('tab_content'))])]
    return []

SURF_DARK = ('fs-dark', 'fs-grad', 'fs-purple-card', 'fs-footer', 'fs-cta-banner')
SURF_LIGHT = ('fs-gcard', 'fs-soft-box', 'fs-header', 'fs-quiz-card')
def surface(stack):
    for cls in reversed(stack):
        c = cls.split()
        if any(x in c for x in SURF_LIGHT): return 'light'
        if any(x in c for x in SURF_DARK): return 'dark'
    return 'light'
def role(w, part, stack):
    s = w['settings']; cls = ' '.join(sorted(x for x in s.get('_css_classes', '').split() if x.startswith('fs-')))
    return (w.get('widgetType'), part, s.get('header_size', ''), cls, surface(stack))

# ---------------------------------------------------------------- typography values -> settings
def r05(x): return round(x * 2) / 2
def typo_values(st):
    d, t, m = st.get('d'), st.get('t'), st.get('m')
    v = {'fam': d['fam'], 'fw': d['fw'], 'd': r05(d['fs']), 'lh': d['lh'], 'ls': d['ls'], 'tt': d['tt'], 'st': d['st']}
    v['t'] = r05(t['fs']) if t else v['d']
    v['m'] = r05(m['fs']) if m else v['t']
    return v
def typo_key(v): return json.dumps(v, sort_keys=True)
def typo_settings(prefix, v):
    s = {f'{prefix}_typography': 'custom', f'{prefix}_font_family': v['fam'], f'{prefix}_font_weight': str(v['fw']),
         f'{prefix}_font_size': {'unit': 'px', 'size': v['d'], 'sizes': []}}
    if v['t'] != v['d']: s[f'{prefix}_font_size_tablet'] = {'unit': 'px', 'size': v['t'], 'sizes': []}
    if v['m'] != v['t']: s[f'{prefix}_font_size_mobile'] = {'unit': 'px', 'size': v['m'], 'sizes': []}
    if v['lh']: s[f'{prefix}_line_height'] = {'unit': 'em', 'size': v['lh'], 'sizes': []}
    if v['ls']: s[f'{prefix}_letter_spacing'] = {'unit': 'em', 'size': v['ls'], 'sizes': []}
    s[f'{prefix}_text_transform'] = v['tt'] or 'none'
    s[f'{prefix}_font_style'] = v['st'] or 'normal'
    return s
MAX_PRESETS, MIN_USES = 24, 10
def label_for(w, part):
    s = w['settings']; cls = s.get('_css_classes', '')
    if part == 'title':
        if 'fs-eyebrow' in cls: return 'Eyebrow'
        for c, n in (('fs-step-num', 'Step number'), ('fs-trust-num', 'Big number'), ('fs-close', 'Closing line'), ('fs-price', 'Price')):
            if c in cls: return n
        return {'h1': 'H1', 'h2': 'H2', 'h3': 'H3', 'h4': 'H4'}.get(s.get('header_size', 'h2'), 'Label')
    if part == 'text':
        if 'fs-trust-label' in cls: return 'Big number label'
        if 'fs-hero-lead' in cls: return 'Hero lead'
        if 'fs-lead' in cls: return 'Lead'
        return 'Body'
    return ROLE_NAME[part]
# article body text (blog / resources), as in the HTML: 17.5px, line height 1.75, body grey
_PR = {'tag': 'p', 'fs': 17.5, 'fw': '400', 'lh': 1.75, 'ls': 0, 'fam': 'Poppins', 'tt': 'none', 'st': 'normal', 'col': 'rgb(47, 46, 54)'}
PROSE = {'d': _PR, 't': _PR, 'm': dict(_PR, fs=16.5)}
ROLE_NAME = {'prose': 'Article text', 'cnum': 'Stat number', 'ctitle': 'Stat label', 'title': 'Heading', 'text': 'Text', 'button': 'Button', 'item': 'List', 'ibtitle': 'Card title', 'ibdesc': 'Card text', 'q': 'FAQ question', 'a': 'FAQ answer'}

# ---------------------------------------------------------------- walk
def walk(elements, fn, stack=()):
    for e in elements:
        cls = e['settings'].get('css_classes', '') if e['elType'] == 'container' else e['settings'].get('_css_classes', '')
        fn(e, stack)
        walk(e.get('elements', []), fn, stack + (cls,))

def first_heading(e):
    if e.get('widgetType') == 'heading' and e['settings'].get('header_size', 'h2') in ('h1', 'h2', 'h3'):
        return norm(e['settings'].get('title'))
    for c in e.get('elements', []):
        r = first_heading(c)
        if r: return r
    return None

DARK_CTX = ('fs-dark', 'fs-grad', 'fs-purple-card', 'fs-footer', 'fs-final', 'fs-cta-banner', 'fs-pcard', 'fs-step-hl', 'fs-steps')
def gradient_headings(tpl):
    """Same rule as the HTML: an H2 on a light section with no coloured words gets the gradient on the part after a
    line break, or on its last ~45% of words."""
    def visit(e, stack):
        if e.get('widgetType') != 'heading' or e['settings'].get('header_size', 'h2') != 'h2': return
        t = e['settings'].get('title', '')
        if '<span' in t or any(c in x for x in stack for c in DARK_CTX): return
        if re.search(r'<br\s*/?>', t):
            a, b = re.split(r'<br\s*/?>', t, 1)
            if b.strip(): e['settings']['title'] = f'{a}<br><span class="fs-gt">{b.strip()}</span>'
            return
        words = t.split()
        if len(words) < 2: return
        k = max(1, round(len(words) * 0.45))
        e['settings']['title'] = ' '.join(words[:-k]) + f' <span class="fs-gt">{" ".join(words[-k:])}</span>'
    walk(tpl['content'], visit)

def process(templates):
    """templates: list of (page_key, tpl). Mutates templates; returns kit typography presets."""
    for _, tpl in templates: gradient_headings(tpl)
    assign = []                     # (widget, prefix, colour key, part, role, style or None)
    role_styles = defaultdict(Counter); role_keep = {}
    for page, tpl in templates:
        occ = Counter()
        def visit(e, stack, page=page, occ=occ):
            if e['elType'] != 'widget': return
            # "Three ways" tabs: the whole look comes from the fs-ways CSS, so nothing is written on its widgets
            if any('fs-ways-tabs' in x or 'fs-nostyle' in x for x in stack): return
            for part, prefix, ckey, texts in parts(e):
                st = PROSE if part == 'prose' else None
                for t in texts:
                    st = lookup(page, t, occ[(part, t)], part)
                    if st and st.get('d'): occ[(part, t)] += 1
                    if st and st.get('d'): break
                    st = None
                rl = role(e, part, stack)
                if st:
                    k = json.dumps(st, sort_keys=True); role_styles[rl][k] += 1; role_keep[k] = st
                assign.append((e, prefix, ckey, part, rl, st))
        walk(tpl['content'], visit)
    # fallback by role, then by (widget, part, tag, surface)
    loose = defaultdict(Counter)
    for rl, cnt in role_styles.items():
        for k, n in cnt.items(): loose[(rl[0], rl[1], rl[2], rl[4])][k] += n
    def fallback(rl):
        c = role_styles.get(rl) or loose.get((rl[0], rl[1], rl[2], rl[4]))
        return role_keep[c.most_common(1)[0][0]] if c else None
    resolved = []
    for e, prefix, ckey, part, rl, st in assign:
        st = st or fallback(rl)
        if st and st.get('d'): resolved.append((e, prefix, ckey, part, st))
    # typography presets
    use = Counter(); names = {}
    for e, prefix, ckey, part, st in resolved:
        k = typo_key(typo_values(st)); use[k] += 1; names.setdefault(k, Counter())[label_for(e, part)] += 1
    presets = {}
    # the most common style for each main role always becomes a Global Font, then the most used of the rest
    by_label = defaultdict(Counter)
    for k, c in names.items():
        for lab, n in c.items(): by_label[lab][k] += n
    top = []
    for lab in ('H1', 'H2', 'H3', 'H4', 'Eyebrow', 'Hero lead', 'Lead', 'Body', 'Button', 'List', 'Card title', 'Card text', 'FAQ question', 'FAQ answer', 'Big number', 'Step number'):
        if by_label.get(lab):
            k = by_label[lab].most_common(1)[0][0]
            if k not in top: top.append(k)
    for k, n in use.most_common():
        if len(top) >= MAX_PRESETS: break
        if n >= MIN_USES and k not in top: top.append(k)
    for k in top:
        if True:
            v = json.loads(k)
            pid = 'fs' + hashlib.sha1(k.encode()).hexdigest()[:6]
            label = next((lab for lab in by_label if by_label[lab] and by_label[lab].most_common(1)[0][0] == k and lab in ('H1', 'H2', 'H3', 'H4', 'Eyebrow', 'Hero lead', 'Lead', 'Body', 'Button', 'List', 'Card title', 'Card text', 'FAQ question', 'FAQ answer', 'Big number', 'Step number')), None) or names[k].most_common(1)[0][0]
            extra = (' italic' if v['st'] == 'italic' else '') + (' caps' if v['tt'] == 'uppercase' else '')
            presets[k] = (pid, f"{label} · {v['d']:g}px {v['fw']}{extra}" + ('' if v['fam'] == 'Poppins' else f" {v['fam']}"), v)
    # write settings
    for e, prefix, ckey, part, st in resolved:
        s = e['settings']; g = s.setdefault('__globals__', {})
        v = typo_values(st); k = typo_key(v)
        # Typography is written on the widget itself (editable in its Style tab). It is not linked to a Global Font:
        # Elementor ignores a widget's own values when its linked global is missing, so a link would break the page
        # on any site where the Site Settings import hasn't landed.
        s.update(typo_settings(prefix, v))
        if ckey and st['d'].get('col') and st['d']['col'] != 'gradient':
            ref = color_ref(st['d']['col'])
            # Link only to Elementor's four built-in Global Colors (they exist on every site); everything else inline.
            if ref and ref[0] == 'global' and ref[1] in SYSTEM_IDS: g[ckey] = f'globals/colors?id={ref[1]}'
            elif ref: s[ckey] = ref[1] if ref[0] == 'hex' else HEX_OF[ref[1]]
    # sections: padding per device + section-head width
    for page, tpl in templates:
        secs = {w: {x['h']: x for x in P.get(page, {}).get(w, {}).get('sections', [])} for w in ('d', 't', 'm')}
        for e in tpl['content']:
            if e['elType'] != 'container': continue
            h = first_heading(e)
            if not h: continue
            key = next((x for x in secs['d'] if x == h[:80] or x.startswith(h[:40])), None)
            if not key: continue
            for w, suf in (('d', ''), ('t', '_tablet'), ('m', '_mobile')):
                x = secs[w].get(key)
                if not x: continue
                base = e['settings'].get('padding' + suf) or e['settings'].get('padding') or {}
                side = '16' if w == 'm' else '24'
                e['settings']['padding' + suf] = {'unit': 'px', 'top': str(max(0, x.get('padT', x['top']))), 'right': side, 'bottom': str(max(0, x.get('padB', x['bottom']))), 'left': side, 'isLinked': False}
            if secs['d'][key].get('align') == 'left':
                # the HTML's heading block is left-aligned in this section
                def to_left(c):
                    if c['elType'] == 'container' and 'fs-sec-head' in c['settings'].get('css_classes', ''):
                        c['settings']['css_classes'] = c['settings']['css_classes'].replace('fs-sec-head', '').strip()
                        c['settings'].pop('max_width', None)
                        for w_ in c['elements']:
                            if w_.get('widgetType') in ('heading', 'text-editor'): w_['settings']['align'] = 'left'
                        return True
                    return any(to_left(y) for y in c.get('elements', []))
                to_left(e)
            hw = secs['d'][key]['headW']
            def fix_head(c):
                if c['elType'] == 'container' and 'fs-sec-head' in c['settings'].get('css_classes', '') and 300 < hw < 1240:
                    c['settings']['max_width'] = {'unit': 'px', 'size': hw, 'sizes': []}
                    return True
                return any(fix_head(y) for y in c.get('elements', []))
            fix_head(e)
    # unique, readable names
    seen = Counter(n for _, n, _ in presets.values()); out = []
    for pid, name, v in presets.values():
        if seen[name] > 1 and v.get('lh'): name += f" lh {v['lh']:g}"
        out.append((pid, name, v))
    return out

def kit_typography(presets):
    out = []
    for pid, name, v in sorted(presets, key=lambda p: (-p[2]['d'], p[1])):
        d = {'_id': pid, 'title': name}; d.update(typo_settings('typography', v)); out.append(d)
    return out
