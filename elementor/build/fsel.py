"""Tiny builder for Elementor template JSON (Flexbox containers). Used to generate the First Search templates."""
import json, random, re

random.seed(20261106)
_ids = set()
def uid():
    while True:
        i = '%07x' % random.getrandbits(28)
        if i not in _ids:
            _ids.add(i); return i

# Images are served from the public GitHub repo, pinned to a commit so the URLs never change.
# Elementor downloads each one into the Media Library during import.
ASSET_COMMIT = '4d59b7976a0bacac8601ce9d2eba36ebb43a7779'
ASSET = f'https://raw.githubusercontent.com/chrismitchell-cmd/first-search-marketing/{ASSET_COMMIT}/elementor/upload/first-search/'
# Images re-exported after the first pin (the framework wheel fix) load from the commit that holds them.
WHEEL_COMMIT = 'f978e9f0c6a066562155908c1524a093df652243'
ASSET_V2 = f'https://raw.githubusercontent.com/chrismitchell-cmd/first-search-marketing/{WHEEL_COMMIT}/elementor/upload/first-search/'
def asset(path):
    """Prototype asset path (assets/img/...) -> hosted URL."""
    rel = re.sub(r'^assets/img/', '', path)
    return (ASSET_V2 if rel == 'framework-wheel.webp' or rel.startswith('wheels/') else ASSET) + rel

def px(n): return {'unit': 'px', 'size': n, 'sizes': []}
def pad(t, r=None, b=None, l=None, unit='px'):
    r = t if r is None else r; b = t if b is None else b; l = r if l is None else l
    return {'unit': unit, 'top': str(t), 'right': str(r), 'bottom': str(b), 'left': str(l), 'isLinked': len({t, r, b, l}) == 1}
def gap(n, row=None):
    row = n if row is None else row
    return {'unit': 'px', 'size': n, 'column': str(n), 'row': str(row), 'isLinked': n == row}

def con(*children, d='column', cls='', w=None, inner=True, boxed=False, gap_=None, justify=None, align=None,
        wrap=False, p=None, mobile_col=True, title=None, minh=None, bg_img=None, s=None, **extra):
    st = {'content_width': 'boxed' if boxed else 'full', 'flex_direction': d}
    if boxed: st['boxed_width'] = px(1240)  # same as the HTML: 1240px content + 24px side gutters
    if cls: st['css_classes'] = cls
    if w is not None:
        st['width'] = {'unit': '%', 'size': w, 'sizes': []} if isinstance(w, (int, float)) and w <= 100 and not isinstance(w, str) else w
        st['width_mobile'] = {'unit': '%', 'size': 100, 'sizes': []}
    if gap_ is not None: st['flex_gap'] = gap(gap_) if isinstance(gap_, int) else gap_
    if justify: st['flex_justify_content'] = justify
    if align: st['flex_align_items'] = align
    if wrap: st['flex_wrap'] = 'wrap'
    # Explicit padding everywhere: Elementor otherwise adds 10px to every container that has none.
    st['padding'] = (p if isinstance(p, dict) else pad(p)) if p is not None else pad(0)
    if d == 'row' and mobile_col: st['flex_direction_mobile'] = 'column'
    if title: st['_title'] = title
    if minh: st['min_height'] = px(minh)
    if bg_img:
        st.update({'background_background': 'classic', 'background_image': {'url': asset(bg_img), 'id': '', 'source': 'library'},
                   'background_position': 'center center', 'background_size': 'cover', 'background_repeat': 'no-repeat'})
    if s: st.update(s)
    st.update(extra)
    return {'id': uid(), 'elType': 'container', 'isInner': inner, 'settings': st, 'elements': [c for c in children if c]}

def section(*children, cls='', title=None, boxed=True, p=None, d='column', gap_=24, align=None, justify=None, bg_img=None, s=None):
    """Top-level full-width section with a boxed inner container."""
    inner = con(*children, d=d, boxed=False, gap_=gap_, align=align, justify=justify, s={'padding': pad(0)})
    return con(inner, cls=cls, inner=False, boxed=boxed, title=title, gap_=0, bg_img=bg_img,
               p=p if p is not None else {'unit': 'px', 'top': '100', 'right': '24', 'bottom': '100', 'left': '24', 'isLinked': False},
               s=dict({'padding_mobile': {'unit': 'px', 'top': '64', 'right': '16', 'bottom': '64', 'left': '16', 'isLinked': False}}, **(s or {})))

def w(kind, settings, cls=''):
    if cls: settings['_css_classes'] = cls
    return {'id': uid(), 'elType': 'widget', 'widgetType': kind, 'settings': settings, 'elements': []}

def heading(text, tag='h2', cls='', align=None):
    s = {'title': text, 'header_size': tag}
    if align: s['align'] = align
    return w('heading', s, cls)
def eyebrow(text, align=None): return heading(text, 'p', 'fs-eyebrow', align)
def text(html, cls='', align=None):
    if not html.lstrip().startswith('<'): html = f'<p>{html}</p>'
    s = {'editor': html}
    if align: s['align'] = align
    return w('text-editor', s, cls)
def button(label, url='#', cls='', align=None, size='md'):
    s = {'text': label, 'link': {'url': url, 'is_external': '', 'nofollow': ''}, 'size': size}
    if align: s['align'] = align
    return w('button', s, cls)
def link_u(label, url='#'): return button(label, url, 'fs-link-u')
def image(path, cls='', width=None, align=None, alt=''):
    s = {'image': {'url': asset(path) if not path.startswith('http') else path, 'id': '', 'alt': alt, 'source': 'library'}, 'image_size': 'full'}
    if width: s['width'] = {'unit': 'px', 'size': width, 'sizes': []} if isinstance(width, int) else {'unit': '%', 'size': int(width[:-1]), 'sizes': []}
    if align: s['align'] = align
    return w('image', s, cls)
def html(code, cls=''): return w('html', {'html': code}, cls)
def icon_list(items, icon='fas fa-check', cls='', links=None):
    lst = []
    for n, t in enumerate(items):
        it = {'_id': uid(), 'text': t, 'selected_icon': {'value': icon, 'library': 'fa-solid'} if icon else {'value': '', 'library': ''}}
        if links and links[n]: it['link'] = {'url': links[n], 'is_external': '', 'nofollow': ''}
        lst.append(it)
    return w('icon-list', {'icon_list': lst}, cls)
def image_box(img, title, desc, cls='fs-tile', pos='left', tag='h3'):
    return w('image-box', {'image': {'url': asset(img), 'id': '', 'source': 'library'}, 'title_text': title, 'description_text': desc,
                           'position': pos, 'title_size': tag, 'image_size': {'unit': '%', 'size': 30, 'sizes': []}}, cls)
def icon_box(icon, title, desc, cls='', pos='top', tag='h3'):
    return w('icon-box', {'selected_icon': {'value': icon, 'library': 'fa-solid'}, 'title_text': title, 'description_text': desc,
                          'position': pos, 'title_size': tag}, cls)
def video(caption='', img=None, cls='fs-video', url='https://www.youtube.com/watch?v=XHOmBV4js_E'):
    s = {'youtube_url': url, 'aspect_ratio': '169'}
    if img: s.update({'show_image_overlay': 'yes', 'image_overlay': {'url': asset(img), 'id': '', 'source': 'library'}})
    return w('video', s, cls)
def accordion(qas, cls='fs-faq'):
    return w('accordion', {'tabs': [{'_id': uid(), 'tab_title': q, 'tab_content': f'<p>{a}</p>'} for q, a in qas], 'title_html_tag': 'h3',
                           'selected_icon': {'value': 'fas fa-plus', 'library': 'fa-solid'}, 'selected_active_icon': {'value': 'fas fa-minus', 'library': 'fa-solid'},
                           'icon_align': 'left', 'tab_active_color': '#FFFFFF'}, cls)
def counter(end, title, suffix='', prefix=''):
    return w('counter', {'starting_number': 0, 'ending_number': end, 'suffix': suffix, 'prefix': prefix, 'title': title,
                         'duration': 1400, 'thousand_separator': 'yes', 'thousand_separator_char': ','})
def spacer(h): return w('spacer', {'space': px(h)})
def divider(): return w('divider', {})
def form(fields, button_text='Send message', name='Contact', cls=''):
    ff = []
    for f in fields:
        typ, label, req = f[0], f[1], f[2] if len(f) > 2 else True
        it = {'_id': uid(), 'custom_id': re.sub(r'\W+', '_', label.lower()).strip('_')[:20], 'field_type': typ, 'field_label': label,
              'placeholder': f[3] if len(f) > 3 else '', 'required': 'true' if req else '', 'width': f[4] if len(f) > 4 else '100'}
        if typ in ('select', 'radio', 'checkbox'): it['field_options'] = '\n'.join(f[5])
        if typ == 'acceptance': it['acceptance_text'] = f[5]
        ff.append(it)
    return w('form', {'form_name': name, 'form_fields': ff, 'button_text': button_text, 'button_size': 'md', 'show_labels': 'yes',
                      'success_message': 'Thanks! We got your message and will reply within one business day.'}, cls)
def plogo(stage, light=False, size=None):
    st = f' style="font-size:{size}px"' if size else ''
    return f'<span class="fs-plogo{" fs-plogo--light" if light else ""}"{st}><b>first</b>{stage}</span>'

def nested_tabs(tabs, cls=''):
    """tabs = [(title, container)]"""
    return {'id': uid(), 'elType': 'widget', 'widgetType': 'nested-tabs', 'settings': {
        'tabs': [{'_id': uid(), 'tab_title': t} for t, _ in tabs], '_css_classes': cls},
        'elements': [c for _, c in tabs]}

def template(title, kind, content, page_css=''):
    # Page layout "Elementor Full Width" + hidden page title, so sections run edge to edge like the HTML.
    ps = {'template': 'elementor_header_footer', 'hide_title': 'yes'} if kind in ('page', 'single-post') else {}
    if page_css: ps['custom_css'] = page_css
    t = {'version': '0.4', 'title': title, 'type': kind, 'content': content, 'page_settings': ps}
    return t

def _stable_ids(o):
    """Give every hosted image a stable non-empty id. Elementor only de-duplicates imported images
    (by URL hash) when the id is set, so each image lands in the Media Library once, not once per use."""
    if isinstance(o, dict):
        if isinstance(o.get('url'), str) and o['url'].startswith(ASSET) and not o.get('id'):
            import hashlib
            o['id'] = 700000 + int(hashlib.sha1(o['url'].encode()).hexdigest()[:6], 16) % 99999
        for v in o.values(): _stable_ids(v)
    elif isinstance(o, list):
        for v in o: _stable_ids(v)
def _real_widths(o):
    """Containers have no max-width setting: use width (px) + 100% on tablet/phone + align-self centre."""
    if isinstance(o, dict):
        st = o.get('settings') if o.get('elType') == 'container' else None
        if st and 'max_width' in st:
            st['width'] = st.pop('max_width')
            st.setdefault('width_tablet', {'unit': '%', 'size': 100, 'sizes': []})
            st['width_mobile'] = {'unit': '%', 'size': 100, 'sizes': []}
            st['_flex_align_self'] = 'center'
            st.pop('margin', None)
        for v in o.values(): _real_widths(v)
    elif isinstance(o, list):
        for v in o: _real_widths(v)
def _card_links(e):
    """A container rendered as <a> (html_tag 'a') gets split by the browser around the widgets inside it.
    Turn each one into a plain container with class fs-card-link and put its link on the card's title heading,
    which CSS stretches over the whole card. Title = first h3 heading, else a heading named *-n / *-logo, else the first heading."""
    st = e.get('settings', {})
    if e.get('elType') == 'container' and st.get('html_tag') == 'a' and (st.get('link') or {}).get('url'):
        heads = []
        def find(x):
            if x.get('widgetType') == 'heading': heads.append(x)
            for c in x.get('elements', []): find(c)
        for c in e.get('elements', []): find(c)
        pick = ([h for h in heads if h['settings'].get('header_size') == 'h3'] +
                [h for h in heads if any(k.endswith(('-n', '-logo')) for k in h['settings'].get('_css_classes', '').split())] + heads)
        if pick:
            pick[0]['settings']['link'] = st.pop('link'); st.pop('html_tag')
            st['css_classes'] = (st.get('css_classes', '') + ' fs-card-link').strip()
    for c in e.get('elements', []): _card_links(c)

def save(path, tpl):
    for e in tpl['content']: _card_links(e)
    _stable_ids(tpl)
    _real_widths(tpl)
    with open(path, 'w', encoding='utf-8') as f: json.dump(tpl, f, ensure_ascii=False, indent=1)
