"""Approximate Elementor front-end rendering of the templates, for visual QA only (not shipped)."""
import json, sys, html as H, os
CSSV = []
def u(v): return f"{v['size']}{v.get('unit','px')}" if isinstance(v, dict) and 'size' in v else None
def box(v):
    if not isinstance(v, dict): return None
    un = v.get('unit', 'px'); return ' '.join(f"{v.get(k,'0') or 0}{un}" for k in ('top', 'right', 'bottom', 'left'))
def rule(eid, css, media=None):
    if css: CSSV.append((media, f'.elementor-element-{eid}{{{css}}}'))
def render(e, depth=0):
    s, eid = e['settings'], e['id']
    if e['elType'] == 'container':
        css = f"display:flex;flex-direction:{s.get('flex_direction','column')};"
        g = s.get('flex_gap');  css += f"gap:{g['row']}px {g['column']}px;" if g else 'gap:20px;'
        if s.get('flex_justify_content'): css += f"justify-content:{s['flex_justify_content']};"
        if s.get('flex_align_items'): css += f"align-items:{s['flex_align_items']};"
        if s.get('flex_wrap'): css += 'flex-wrap:wrap;'
        p = box(s.get('padding')); css += f'padding:{p};' if p else ('padding:10px;' if not e['isInner'] else '')
        if s.get('width'): css += f"width:{u(s['width'])};" + ('flex:0 0 auto;' if s['width']['unit'] == 'px' else '')
        if s.get('max_width'): css += f"max-width:{u(s['max_width'])};width:100%;"
        if s.get('min_height'): css += f"min-height:{u(s['min_height'])};"
        if s.get('flex_grow'): css += f"flex-grow:{s['flex_grow']};"
        if s.get('background_image'): css += f"background-image:url('{s['background_image']['url'].replace('https://befirstsearch.com/wp-content/uploads/first-search/', '../upload/first-search/')}');background-size:cover;background-position:center;"
        if s.get('background_color'): css += f"background-color:{s['background_color']};"
        if s.get('sticky'): css += 'position:sticky;top:0;'
        rule(eid, css)
        m = ''
        if s.get('flex_direction_mobile'): m += f"flex-direction:{s['flex_direction_mobile']};"
        if s.get('width_mobile'): m += f"width:{u(s['width_mobile'])};"
        if s.get('padding_mobile'): m += f"padding:{box(s['padding_mobile'])};"
        if s.get('margin_mobile'): m += f"margin:{box(s['margin_mobile'])};"
        rule(eid, m, '(max-width:767px)')
        if s.get('flex_direction') == 'row': rule(eid, 'min-width:0', None)
        inner = ''.join(render(c, depth + 1) for c in e['elements'])
        if s.get('content_width') == 'boxed':
            inner = f'<div class="e-con-inner" style="width:100%;max-width:1288px;margin:0 auto;display:flex;flex-direction:inherit;gap:inherit">{inner}</div>'
        idattr = f' id="{s["_element_id"]}"' if s.get('_element_id') else ''
        return f'<div class="e-con elementor-element elementor-element-{eid} {s.get("css_classes","")}"{idattr}>{inner}</div>'
    k = e['widgetType']; cls = s.get('_css_classes', '')
    def wrap(body, extra=''): return f'<div class="elementor-element elementor-element-{eid} elementor-widget elementor-widget-{k} {cls}" style="{extra}"><div class="elementor-widget-container">{body}</div></div>'
    al = s.get('align')
    if k == 'heading':
        t = s.get('header_size', 'h2'); return wrap(f'<{t} class="elementor-heading-title" style="{"text-align:" + al if al else ""}">{s["title"]}</{t}>')
    if k == 'text-editor': return wrap(f'<div style="{"text-align:" + al if al else ""}">{s["editor"]}</div>')
    if k == 'button':
        j = {'center': 'center', 'right': 'flex-end', 'justify': 'stretch'}.get(al, 'flex-start')
        return wrap(f'<div style="display:flex;justify-content:{j}"><a class="elementor-button" href="{s["link"]["url"]}" style="{"width:100%;text-align:center" if al == "justify" else ""}"><span>{s["text"]}</span></a></div>')
    if k == 'image':
        wv = u(s.get('width')); src = s['image']['url'].replace('https://befirstsearch.com/wp-content/uploads/first-search/', '../upload/first-search/')
        j = {'center': 'center', 'right': 'flex-end'}.get(al, 'flex-start')
        return wrap(f'<div style="display:flex;justify-content:{j}"><img src="{src}" alt="" style="max-width:100%;{"width:" + wv if wv else ""};height:auto;display:block"></div>')
    if k == 'theme-site-logo': return wrap('<img src="../../assets/img/logo.png" style="width:220px;height:auto;display:block" alt="logo">')
    if k in ('html',): return wrap(s['html'])
    if k == 'icon-list':
        items = ''.join(f'<li class="elementor-icon-list-item" style="display:flex;gap:10px;align-items:baseline;padding:4px 0">' + (f'<span class="elementor-icon-list-icon"><i style="font-style:normal">✓</i></span>' if it['selected_icon'].get('value') else '') + f'<span class="elementor-icon-list-text">{it["text"]}</span></li>' for it in s['icon_list'])
        return wrap(f'<ul class="elementor-icon-list-items" style="list-style:none;margin:0;padding:0">{items}</ul>')
    if k == 'image-box':
        src = s['image']['url'].replace('https://befirstsearch.com/wp-content/uploads/first-search/', '../upload/first-search/')
        pos = s.get('position', 'top'); t = s.get('title_size', 'h3')
        lay = 'display:flex;gap:20px;align-items:center' if pos == 'left' else 'text-align:left'
        return wrap(f'<div class="elementor-image-box-wrapper" style="{lay}"><figure class="elementor-image-box-img" style="margin:0 0 10px;width:{"96px" if pos == "left" else "72px"};flex:none"><img src="{src}" style="width:100%;display:block"></figure><div class="elementor-image-box-content"><{t} class="elementor-image-box-title" style="margin:0 0 6px">{s["title_text"]}</{t}><p class="elementor-image-box-description" style="margin:0">{s["description_text"]}</p></div></div>')
    if k == 'video':
        img = s.get('image_overlay', {}).get('url', '').replace('https://befirstsearch.com/wp-content/uploads/first-search/', '../upload/first-search/')
        return wrap(f'<div class="elementor-wrapper" style="aspect-ratio:16/9;background:#250762 url(\'{img}\') center bottom/contain no-repeat;display:grid;place-items:center;border-radius:28px"><span style="width:80px;height:80px;border-radius:50%;background:#fff;display:grid;place-items:center;font-size:30px;color:#250762">▶</span></div>')
    if k in ('accordion', 'toggle'):
        its = ''.join(f'<div class="elementor-accordion-item"><div class="elementor-tab-title{" elementor-active" if n == 0 else ""}">{t["tab_title"]}</div>' + (f'<div class="elementor-tab-content">{t["tab_content"]}</div>' if n == 0 else '') + '</div>' for n, t in enumerate(s['tabs']))
        return wrap(its)
    if k == 'counter': return wrap(f'<div style="text-align:center"><div class="elementor-counter-number-wrapper">{s.get("prefix","")}{s["ending_number"]}{s.get("suffix","")}</div><div class="elementor-counter-title">{s["title"]}</div></div>')
    if k == 'form':
        f = ''.join(f'<div class="elementor-field-group" style="width:{it.get("width","100")}%;padding:0 6px 12px;box-sizing:border-box"><label class="elementor-field-label">{it["field_label"]}</label>' +
                    ('<textarea class="elementor-field elementor-field-textual" style="width:100%;box-sizing:border-box"></textarea>' if it['field_type'] == 'textarea' else
                     f'<select class="elementor-field" style="width:100%"><option>{(it.get("field_options") or "").splitlines()[0] if it.get("field_options") else ""}</option></select>' if it['field_type'] == 'select' else
                     f'<label style="font-size:12px"><input type="checkbox"> {it.get("acceptance_text","")}</label>' if it['field_type'] == 'acceptance' else
                     f'<input class="elementor-field elementor-field-textual" placeholder="{it.get("placeholder","")}" style="width:100%;box-sizing:border-box">') + '</div>' for it in s['form_fields'])
        return wrap(f'<form class="elementor-form"><div style="display:flex;flex-wrap:wrap;margin:0 -6px">{f}</div><div class="elementor-widget-button" style="padding:0 0"><button class="elementor-button">{s["button_text"]}</button></div></form>')
    if k == 'n-menu':
        t = ''.join(f'<div class="e-n-menu-title"><span class="e-n-menu-title-text">{it["item_title"]}</span>{" ▾" if it.get("item_dropdown_content") else ""}</div>' for it in s['menu_items'])
        return wrap(f'<nav style="display:flex;gap:28px">{t}</nav>')
    if k == 'nested-tabs':
        t = ''.join(f'<div class="e-n-tab-title" aria-selected="{"true" if n == 0 else "false"}"><span class="e-n-tab-title-text">{it["tab_title"]}</span></div>' for n, it in enumerate(s['tabs']))
        return wrap(f'<div class="e-n-tabs"><div class="e-n-tabs-heading" style="display:flex;gap:10px;margin-bottom:18px">{t}</div><div class="e-n-tabs-content">{render(e["elements"][0])}</div></div>')
    if k == 'flip-box':
        src = s['background_a_image']['url'].replace('https://befirstsearch.com/wp-content/uploads/first-search/', '../upload/first-search/')
        return wrap(f'<div class="elementor-flip-box"><div class="elementor-flip-box__front" style="height:420px;background:#250762 url(\'{src}\') bottom/contain no-repeat;display:flex;align-items:flex-end;padding:20px;box-sizing:border-box;position:relative"><div class="elementor-flip-box__layer__overlay" style="position:absolute;inset:0"></div><div style="position:relative"><h3 class="elementor-flip-box__layer__title" style="margin:0">{s["title_text_a"]}</h3><div class="elementor-flip-box__layer__description">{s["description_text_a"]}</div></div></div></div>')
    if k in ('posts',):
        c = ''.join('<div class="elementor-post__card" style="background:#fff;padding:20px;height:220px"><span class="elementor-post__badge" style="color:#fff;padding:2px 10px">Blog</span><h3 class="elementor-post__title"><a>Post title</a></h3><a class="elementor-post__read-more">Read more »</a></div>' for _ in range(3))
        return wrap(f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:24px">{c}</div>')
    if k == 'taxonomy-filter': return wrap('<div style="display:flex;flex-wrap:wrap;gap:8px"><span class="fs-pill fs-pill--purple">All</span><span class="fs-pill">Blogs</span><span class="fs-pill">Case studies</span><span class="fs-pill">Podcasts</span><span class="fs-pill">Videos</span></div>')
    if k == 'google_maps': return wrap(f'<div style="height:{u(s.get("height")) or "300px"};background:#dfe6ef;border-radius:20px;display:grid;place-items:center">Google Map: {s["address"]}</div>')
    if k == 'social-icons': return wrap('<div style="display:flex;gap:8px">' + ''.join('<span class="elementor-social-icon" style="width:40px;height:40px;display:inline-block"></span>' for _ in s['social_icon_list']) + '</div>')
    if k == 'countdown': return wrap('<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px">' + ''.join(f'<div class="elementor-countdown-item" style="padding:12px;text-align:center"><div class="elementor-countdown-digits" style="font-size:32px">0{n}</div><div class="elementor-countdown-label">{l}</div></div>' for n, l in enumerate(['days', 'hours', 'mins'])) + '</div>')
    if k == 'blockquote': return wrap(f'<blockquote class="elementor-blockquote"><p>“{s["blockquote_content"]}”</p><cite class="elementor-blockquote__author">{s["author_name"]}</cite></blockquote>')
    if k == 'table-of-contents': return wrap('<div class="elementor-toc__header"><h4 class="elementor-toc__header-title">In this article</h4></div><ol style="padding-left:18px"><li class="elementor-toc__list-item-text">Heading one</li><li class="elementor-toc__list-item-text">Heading two</li></ol>')
    if k == 'share-buttons': return wrap('<div style="display:flex;gap:8px"><span style="width:40px;height:40px;border-radius:50%;border:1px solid #ddd;display:inline-block"></span><span style="width:40px;height:40px;border-radius:50%;border:1px solid #ddd;display:inline-block"></span></div>')
    if k.startswith('theme-post') or k in ('post-info', 'author-box'):
        return wrap(f'<div style="padding:14px;border:1px dashed #9FB7D9;border-radius:12px;color:#174FA2;font-size:14px">[{k}: filled from the post]</div>')
    if k == 'spacer': return wrap('<div style="height:20px"></div>')
    return wrap(f'<div style="color:red">[{k}]</div>')

def page(paths, out):
    CSSV.clear()
    body = ''
    for pth in paths: body += ''.join(render(e) for e in json.load(open(pth))['content'])
    css = open('../site-settings.css').read()
    rules = '\n'.join(r for m, r in CSSV if not m) + '\n@media (max-width:767px){' + '\n'.join(r for m, r in CSSV if m) + '}'
    doc = f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:ital,wght@0,400;0,500;0,600;0,700;0,800;1,500&display=swap" rel="stylesheet">
<style>body{{margin:0;background:#fff}} img{{max-width:100%}} *{{box-sizing:border-box}} .e-con{{min-width:0}} .elementor-widget{{min-width:0}} p{{margin:0 0 .6em}}</style>
<style>{rules}</style><style>{css}</style></head><body class="elementor-kit-5">{body}</body></html>'''
    open(out, 'w').write(doc)
if __name__ == '__main__':
    out = sys.argv[1]
    page([sys.argv[2]] if len(sys.argv) > 2 else [], out)
