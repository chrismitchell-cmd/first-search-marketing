from fsel import ASSET
"""Approximate Elementor front-end rendering of the templates, for visual QA only (not shipped)."""
import json, sys, html as H, os
CSSV = []
def u(v): return f"{v['size']}{v.get('unit','px')}" if isinstance(v, dict) and 'size' in v else None
def box(v):
    if not isinstance(v, dict): return None
    un = v.get('unit', 'px'); return ' '.join(f"{v.get(k,'0') or 0}{un}" for k in ('top', 'right', 'bottom', 'left'))
def rule(eid, css, media=None):
    if css: CSSV.append((media, f'.elementor-9 .elementor-element.elementor-element-{eid}{{{css}}}'))
def render(e, depth=0):
    s, eid = e['settings'], e['id']
    if e['elType'] == 'container':
        # Same mechanics as Elementor: padding, gaps and width go through CSS variables on the element,
        # and .e-con reads them (so class rules in the Custom CSS behave exactly as on the live site).
        def pv(d):
            return f"--padding-top:{d.get('top','0') or 0}{d.get('unit','px')};--padding-right:{d.get('right','0') or 0}{d.get('unit','px')};--padding-bottom:{d.get('bottom','0') or 0}{d.get('unit','px')};--padding-left:{d.get('left','0') or 0}{d.get('unit','px')};"
        css = f"flex-direction:{s.get('flex_direction','column')};"
        g = s.get('flex_gap')
        if g: css += f"--row-gap:{g.get('row', g.get('size', 20))}px;--column-gap:{g.get('column', g.get('size', 20))}px;"
        if s.get('flex_justify_content'): css += f"justify-content:{s['flex_justify_content']};"
        if s.get('flex_align_items'): css += f"align-items:{s['flex_align_items']};"
        if s.get('flex_wrap'): css += 'flex-wrap:wrap;'
        if isinstance(s.get('padding'), dict): css += pv(s['padding'])
        if s.get('width'): css += f"--width:{u(s['width'])};" + ('flex:0 0 auto;' if s['width']['unit'] == 'px' else '')
        if s.get('max_width'): css += f"max-width:{u(s['max_width'])};margin-left:auto;margin-right:auto;"
        if s.get('min_height'): css += f"min-height:{u(s['min_height'])};"
        if s.get('flex_grow'): css += f"flex-grow:{s['flex_grow']};"
        if s.get('_flex_align_self'): css += f"align-self:{s['_flex_align_self']};"
        if s.get('background_image'):
            ov = ''
            if s.get('background_overlay_color'):
                c = s['background_overlay_color'].lstrip('#'); a = s.get('background_overlay_opacity', {}).get('size', .5)
                ov = f"linear-gradient(rgba({int(c[0:2],16)},{int(c[2:4],16)},{int(c[4:6],16)},{a}),rgba({int(c[0:2],16)},{int(c[2:4],16)},{int(c[4:6],16)},{a})),"
            css += f"background-image:{ov}url('{s['background_image']['url'].replace(ASSET, '../upload/first-search/')}');background-size:cover;background-position:{s.get('background_position','center center')};"
        if s.get('background_color'): css += f"background-color:{s['background_color']};"
        if s.get('sticky'): css += 'position:sticky;top:0;z-index:50;'
        rule(eid, css)
        t = ''
        if isinstance(s.get('padding_tablet'), dict): t += pv(s['padding_tablet'])
        if s.get('flex_direction_tablet'): t += f"flex-direction:{s['flex_direction_tablet']};"
        rule(eid, t, '(max-width:1024px)')
        m = ''
        if s.get('flex_direction_mobile'): m += f"flex-direction:{s['flex_direction_mobile']};"
        if s.get('width_mobile'): m += f"--width:{u(s['width_mobile'])};"
        if isinstance(s.get('padding_mobile'), dict): m += pv(s['padding_mobile'])
        if s.get('margin_mobile'): m += f"margin:{box(s['margin_mobile'])};"
        if s.get('flex_wrap_mobile'): m += 'flex-wrap:wrap;'
        if s.get('flex_align_items_mobile'): m += f"align-items:{s['flex_align_items_mobile']};"
        if s.get('flex_gap_mobile'): m += f"--row-gap:{s['flex_gap_mobile'].get('row', 20)}px;--column-gap:{s['flex_gap_mobile'].get('column', 20)}px;"
        rule(eid, m, '(max-width:767px)')
        inner = ''.join(render(c, depth + 1) for c in e['elements'])
        if s.get('content_width') == 'boxed':
            bw = u(s.get('boxed_width')) or '1140px'
            inner = f'<div class="e-con-inner" style="width:100%;max-width:{bw};margin:0 auto;display:flex;flex-direction:inherit;gap:inherit;align-items:inherit;justify-content:inherit">{inner}</div>'
        idattr = f' id="{s["_element_id"]}"' if s.get('_element_id') else ''
        return f'<div class="e-con e-flex elementor-element elementor-element-{eid} {s.get("css_classes","")}"{idattr}>{inner}</div>'
    k = e['widgetType']; cls = s.get('_css_classes', '')
    widget_style(e)
    def wrap(body, extra=''): return f'<div class="elementor-element elementor-element-{eid} elementor-widget elementor-widget-{k} {cls}" style="{extra}"><div class="elementor-widget-container">{body}</div></div>'
    al = s.get('align')
    if k == 'heading':
        t = s.get('header_size', 'h2'); return wrap(f'<{t} class="elementor-heading-title" style="{"text-align:" + al if al else ""}">{s["title"]}</{t}>')
    if k == 'text-editor': return wrap(f'<div style="{"text-align:" + al if al else ""}">{s["editor"]}</div>')
    if k == 'button':
        j = {'center': 'center', 'right': 'flex-end', 'justify': 'stretch'}.get(al, 'flex-start')
        return wrap(f'<div style="display:flex;justify-content:{j}"><a class="elementor-button" href="{s["link"]["url"]}" style="{"width:100%;text-align:center" if al == "justify" else ""}"><span>{s["text"]}</span></a></div>')
    if k == 'image':
        wv = u(s.get('width')); src = s['image']['url'].replace(ASSET, '../upload/first-search/')
        j = {'center': 'center', 'right': 'flex-end'}.get(al, 'flex-start')
        return wrap(f'<div style="display:flex;justify-content:{j}"><img src="{src}" alt="" style="max-width:100%;{"width:" + wv if wv else ""};height:auto;display:block"></div>')
    if k == 'theme-site-logo': return wrap('<img src="../../assets/img/logo.png" style="width:220px;height:auto;display:block" alt="logo">')
    if k in ('html',): return wrap(s['html'])
    if k == 'icon-list':
        def li(it):
            inner = (f'<span class="elementor-icon-list-icon"><i style="font-style:normal">✓</i></span>' if it['selected_icon'].get('value') else '') + f'<span class="elementor-icon-list-text">{it["text"]}</span>'
            url = (it.get('link') or {}).get('url')
            if url: inner = f'<a href="{url}" style="display:flex;gap:10px;align-items:baseline">{inner}</a>'
            return f'<li class="elementor-icon-list-item" style="display:flex;gap:10px;align-items:baseline;padding:4px 0">{inner}</li>'
        items = ''.join(li(it) for it in s['icon_list'])
        return wrap(f'<ul class="elementor-icon-list-items" style="list-style:none;margin:0;padding:0">{items}</ul>')
    if k == 'image-box':
        src = s['image']['url'].replace(ASSET, '../upload/first-search/')
        pos = s.get('position', 'top'); t = s.get('title_size', 'h3')
        lay = 'display:flex;gap:20px;align-items:center' if pos == 'left' else 'text-align:left'
        return wrap(f'<div class="elementor-image-box-wrapper" style="{lay}"><figure class="elementor-image-box-img" style="margin:0 0 10px;width:{"96px" if pos == "left" else "72px"};flex:none"><img src="{src}" style="width:100%;display:block"></figure><div class="elementor-image-box-content"><{t} class="elementor-image-box-title" style="margin:0 0 6px">{s["title_text"]}</{t}><p class="elementor-image-box-description" style="margin:0">{s["description_text"]}</p></div></div>')
    if k == 'video':
        img = s.get('image_overlay', {}).get('url', '').replace(ASSET, '../upload/first-search/')
        ar = {'169': '1.77777', '219': '2.33333', '43': '1.33333', '32': '1.5', '11': '1', '916': '0.5625'}.get(s.get('aspect_ratio', '169'), '1.77777')
        return wrap(f'<div class="elementor-wrapper elementor-open-inline"><div class="elementor-video"></div><div class="elementor-custom-embed-image-overlay" style="background-image: url({img});">'
                    f'<div class="elementor-custom-embed-play" role="button" aria-label="Play Video" tabindex="0"><svg aria-hidden="true" class="e-font-icon-svg e-eicon-play" viewBox="0 0 1000 1000"><path d="M838 162C746 71 633 25 500 25 371 25 258 71 163 162 71 254 25 367 25 500 25 633 71 746 163 837 254 929 367 979 500 979 633 979 746 933 838 837 929 746 975 633 975 500 975 367 929 254 838 162M808 192C892 279 933 379 933 500 933 621 892 725 808 808 725 892 621 938 500 938 379 938 279 896 196 808 113 725 67 621 67 500 67 379 108 279 196 192 279 108 383 62 500 62 621 62 721 108 808 192M438 392V642L642 517 438 392Z"></path></svg><span class="elementor-screen-only">Play Video</span></div></div></div>',
                    f'--video-aspect-ratio:{ar}')
    if k in ('accordion', 'toggle'):
        its = ''.join(f'<div class="elementor-accordion-item"><div class="elementor-tab-title{" elementor-active" if n == 0 else ""}"><span class="elementor-{'toggle' if k == 'toggle' else 'accordion'}-icon elementor-accordion-icon-left"><span class="elementor-accordion-icon-closed"><i class="fas fa-plus"></i></span></span><a class="elementor-{'toggle' if k == 'toggle' else 'accordion'}-title">{t["tab_title"]}</a></div>' + (f'<div class="elementor-tab-content">{t["tab_content"]}</div>' if n == 0 else '') + '</div>' for n, t in enumerate(s['tabs']))
        return wrap(its)
    if k == 'counter': return wrap(f'<div style="text-align:center"><div class="elementor-counter-number-wrapper">{s.get("prefix","")}{s["ending_number"]}{s.get("suffix","")}</div><div class="elementor-counter-title">{s["title"]}</div></div>')
    if k == 'form':
        f = ''.join(f'<div class="elementor-field-group elementor-column" style="width:{it.get("width","100")}%;padding:0 6px 12px;box-sizing:border-box">' + (f'<label class="elementor-field-label">{it["field_label"]}</label>' if s.get('show_labels', 'yes') else '') +
                    ('<textarea class="elementor-field elementor-field-textual" style="width:100%;box-sizing:border-box"></textarea>' if it['field_type'] == 'textarea' else
                     f'<select class="elementor-field" style="width:100%"><option>{(it.get("field_options") or "").splitlines()[0] if it.get("field_options") else ""}</option></select>' if it['field_type'] == 'select' else
                     f'<label style="font-size:12px"><input type="checkbox"> {it.get("acceptance_text","")}</label>' if it['field_type'] == 'acceptance' else
                     f'<input class="elementor-field elementor-field-textual" placeholder="{it.get("placeholder","")}" style="width:100%;box-sizing:border-box">') + '</div>' for it in s['form_fields'])
        sub = f'<div class="elementor-field-group elementor-column elementor-field-type-submit" style="width:{s.get("button_width", "100")}%;padding:0 6px 12px;box-sizing:border-box"><button class="elementor-button">{s["button_text"]}</button></div>'
        return wrap(f'<form class="elementor-form"><div class="elementor-form-fields-wrapper" style="display:flex;flex-wrap:wrap;margin:0 -6px">{f}{sub}</div></form>')
    if k == 'n-menu':
        t = ''.join(f'<div class="e-n-menu-title"><span class="e-n-menu-title-text">{it["item_title"]}</span>{" ▾" if it.get("item_dropdown_content") else ""}</div>' for it in s['menu_items'])
        return wrap(f'<nav style="display:flex;gap:28px">{t}</nav>')
    if k == 'nested-tabs':
        t = ''.join(f'<button id="e-n-tab-title-{eid}{n}" class="e-n-tab-title" aria-selected="{"true" if n == 0 else "false"}" data-tab-index="{n + 1}" role="tab" tabindex="{0 if n == 0 else -1}" aria-controls="e-n-tab-content-{eid}{n}" style="--n-tabs-title-order: {n + 1};"><span class="e-n-tab-title-text">{it["tab_title"]}</span></button>' for n, it in enumerate(s['tabs']))
        panels = ''
        for n, c in enumerate(e['elements']):
            h = render(c)
            panels += h.replace('<div class="e-con e-flex ', f'<div id="e-n-tab-content-{eid}{n}" role="tabpanel" data-tab-index="{n + 1}" class="{"e-active " if n == 0 else ""}e-con e-flex ', 1)
        js = ("<script>document.currentScript.parentNode.querySelectorAll('.e-n-tab-title').forEach(b=>b.addEventListener('click',()=>{const w=b.closest('.e-n-tabs');"
              "w.querySelectorAll('.e-n-tab-title').forEach(x=>x.setAttribute('aria-selected',x===b));w.querySelectorAll('.e-n-tabs-content>.e-con').forEach(p=>p.classList.toggle('e-active',p.id===b.getAttribute('aria-controls')));}));</script>")
        return wrap(f'<div class="e-n-tabs"><div class="e-n-tabs-heading" role="tablist">{t}</div><div class="e-n-tabs-content">{panels}</div>{js}</div>')
    if k == 'progress':
        pc = s.get('percent', {}).get('size', 50)
        return wrap(f'<div class="elementor-progress-wrapper" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="{pc}"><div class="elementor-progress-bar" data-max="{pc}" style="width:{pc}%"><span class="elementor-progress-text">{s.get("inner_text", "")}</span></div></div>')
    if k == 'flip-box':
        src = s['background_a_image']['url'].replace(ASSET, '../upload/first-search/')
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
    if k == 'icon':
        ic = {'fa-search': '⌕', 'fa-route': '⤳', 'fa-cogs': '⚙', 'fa-chart-line': '📈'}.get(s['selected_icon']['value'].split()[-1], '●')
        return wrap(f'<div class="elementor-icon-wrapper" style="text-align:{s.get("align", "center")}"><span class="elementor-icon" style="font-size:{u(s.get("size")) or "50px"};color:{s.get("primary_color", "#250762")};line-height:1">{ic}</span></div>')
    if k == 'eael-testimonial':
        stars = '<ul class="testimonial-star-rating">' + '<li><i class="fas fa-star" aria-hidden="true">★</i></li>' * 5 + '</ul>'
        return wrap(f'<div class="eael-testimonial-item clearfix {s["eael_testimonial_style"]} {s["eael_testimonial_rating_number"]}">{stars}<div class="eael-testimonial-content">'
                    f'<div class="eael-testimonial-text">{s["eael_testimonial_description"]}</div><p class="eael-testimonial-user">{s["eael_testimonial_name"]}</p>'
                    f'<p class="eael-testimonial-user-company">{s["eael_testimonial_company_title"]}</p></div></div>')
    if k == 'eael-data-table':
        th = ''.join(f'<th class="{c.get("eael_data_table_header_css_class", "")}"><span class="data-table-header-text">{c["eael_data_table_header_col"]}</span></th>' for c in s['eael_data_table_header_cols_data'])
        body, row = '', None
        for c in s['eael_data_table_content_rows']:
            if c['eael_data_table_content_row_type'] == 'row':
                if row is not None: body += f'<tr>{row}</tr>'
                row = ''
            else:
                row += f'<td class="{c.get("eael_data_table_content_row_css_class", "")}"><div class="td-content-wrapper"><div class="td-content">{c.get("eael_data_table_content_row_title", "")}</div></div></td>'
        if row is not None: body += f'<tr>{row}</tr>'
        return wrap(f'<div class="eael-data-table-wrap"><table class="tablesorter eael-data-table center" style="border-collapse:collapse"><thead><tr class="table-header">{th}</tr></thead><tbody>{body}</tbody></table></div>')
    if k == 'spacer': return wrap('<div style="height:20px"></div>')
    return wrap(f'<div style="color:red">[{k}]</div>')

# Elementor's own front-end defaults (container padding/gap) - loaded before the page's element CSS
EL_DEFAULTS = """
.elementor-widget-video .elementor-widget-container{overflow:hidden;transform:translateZ(0)}
.elementor-widget-video .elementor-wrapper{position:relative;aspect-ratio:var(--video-aspect-ratio)}
.elementor-custom-embed-image-overlay{position:absolute;top:0;left:0;width:100%;height:100%;background-size:cover;background-position:50%;cursor:pointer;text-align:center}
.elementor-custom-embed-play{position:absolute;top:50%;left:50%;transform:translate3d(-50%,-50%,0)}
.elementor-custom-embed-play svg{height:100px;width:100px;fill:#fff;filter:drop-shadow(1px 0 6px rgba(0,0,0,.3))}
.elementor-screen-only{position:absolute;top:-10000em;width:1px;height:1px;overflow:hidden}
.elementor-progress-wrapper{position:relative;background-color:#eee;color:#fff;height:30px;line-height:30px;border-radius:2px}
.elementor-progress-bar{display:flex;background-color:#69727d;width:0;font-size:11px;height:30px;line-height:30px;border-radius:2px;transition:width 1s ease-in-out}
.e-n-tabs{display:flex;flex-direction:column;gap:var(--n-tabs-gap,10px)}
.e-n-tabs-heading{display:flex;flex-wrap:wrap;gap:var(--n-tabs-title-gap,10px)}
.e-n-tab-title{display:flex;align-items:center;cursor:pointer;background-color:#F1F2F3;border:0;padding:10px 20px;font:inherit}
.e-n-tab-title[aria-selected=true]{background-color:#E6E9EC}
.e-n-tabs-content>.e-con:not(.e-active){display:none}

.e-con{--container-default-padding-top:0px;--container-default-padding-right:0px;--container-default-padding-bottom:0px;--container-default-padding-left:0px}
.e-con{--width:100%;--padding-top:var(--container-default-padding-top,10px);--padding-right:var(--container-default-padding-right,10px);
 --padding-bottom:var(--container-default-padding-bottom,10px);--padding-left:var(--container-default-padding-left,10px);--row-gap:20px;--column-gap:20px;
 display:flex;position:relative;min-width:0;width:var(--width);padding:var(--padding-top) var(--padding-right) var(--padding-bottom) var(--padding-left);
 gap:var(--row-gap) var(--column-gap)}
.e-con>.elementor-widget,.e-con-inner>.elementor-widget{max-width:100%}
@media (max-width:767px){.e-con.e-flex{--width:100%;flex-wrap:wrap}}
.elementor-heading-title{padding:0;margin:0;line-height:1}
.elementor-widget-text-editor p{margin-top:0;margin-bottom:.9rem}
"""
# Global Colors / Fonts as set in the README, emitted by Elementor in every page's post CSS (loads after the kit CSS)
P, T_ = '"Poppins",sans-serif', '"Inter",sans-serif'
EL_GLOBALS = f"""
.elementor-widget-heading .elementor-heading-title{{color:#250762;font-family:{P};font-weight:700}}
.elementor-widget-text-editor{{color:#1C1B22;font-family:{P};font-size:18px;font-weight:400;line-height:1.6em}}
.elementor-widget-button .elementor-button{{background-color:#174FA2;font-family:{T_};font-weight:500}}
.elementor-widget-image-box .elementor-image-box-title{{color:#250762;font-family:{P};font-weight:700}}
.elementor-widget-image-box .elementor-image-box-description{{color:#1C1B22;font-family:{P};font-size:18px;font-weight:400;line-height:1.6em}}
.elementor-widget-icon-list .elementor-icon-list-icon i,.elementor-widget-icon-list .elementor-icon-list-icon svg{{color:#250762;fill:#250762}}
.elementor-widget-icon-list .elementor-icon-list-item > .elementor-icon-list-text,.elementor-widget-icon-list .elementor-icon-list-item > a{{font-family:{P};font-size:18px;font-weight:400;line-height:1.6em}}
.elementor-widget-icon-list .elementor-icon-list-text{{color:#3299D5}}
.elementor-widget-accordion .elementor-accordion-title{{color:#250762;font-family:{P};font-weight:700}}
.elementor-widget-accordion .elementor-active .elementor-accordion-title{{color:#174FA2}}
.elementor-widget-accordion .elementor-tab-content{{color:#1C1B22;font-family:{P};font-size:18px;font-weight:400;line-height:1.6em}}
.elementor-widget-toggle .elementor-toggle-title{{color:#250762;font-family:{P};font-weight:700}}
.elementor-widget-toggle .elementor-tab-content{{color:#1C1B22;font-family:{P};font-size:18px;font-weight:400;line-height:1.6em}}
.elementor-widget-counter .elementor-counter-number-wrapper{{color:#250762;font-family:{P};font-weight:700}}
.elementor-widget-counter .elementor-counter-title{{color:#3299D5;font-family:{P};font-weight:600}}
"""
KIT = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'kit-preview.json')))
COLORS = {c['_id']: c['color'] for c in KIT['system_colors'] + KIT['custom_colors']}
TYPO = {t['_id']: t for t in KIT['system_typography'] + KIT['custom_typography']}
def kit_vars():
    out = ':root{' + ''.join(f'--e-global-color-{i}:{c};' for i, c in COLORS.items())
    tab, mob = '', ''
    for i, t in TYPO.items():
        for k, v in t.items():
            if not k.startswith('typography_') or k == 'typography_typography': continue
            prop = k[len('typography_'):]
            dev = ''
            if prop.endswith('_tablet'): prop, dev = prop[:-7], 't'
            elif prop.endswith('_mobile'): prop, dev = prop[:-7], 'm'
            val = f"{v['size']}{v.get('unit','px')}" if isinstance(v, dict) else v
            decl = f'--e-global-typography-{i}-{prop.replace("_", "-")}:{val};'
            if dev == 't': tab += decl
            elif dev == 'm': mob += decl
            else: out += decl
    return out + '}' + f'@media (max-width:1024px){{:root{{{tab}}}}}@media (max-width:767px){{:root{{{mob}}}}}'
SUB = {('heading', 'typography'): '.elementor-heading-title', ('heading', 'title_color'): '.elementor-heading-title',
       ('text-editor', 'typography'): '', ('text-editor', 'text_color'): '',
       ('button', 'typography'): '.elementor-button',
       ('icon-list', 'icon_typography'): '.elementor-icon-list-item > .elementor-icon-list-text', ('icon-list', 'text_color'): '.elementor-icon-list-text',
       ('image-box', 'title_typography'): '.elementor-image-box-title', ('image-box', 'title_color'): '.elementor-image-box-title',
       ('image-box', 'description_typography'): '.elementor-image-box-description', ('image-box', 'description_color'): '.elementor-image-box-description',
       ('accordion', 'title_typography'): '.elementor-accordion-title', ('accordion', 'content_typography'): '.elementor-tab-content', ('accordion', 'content_color'): '.elementor-tab-content',
       ('counter', 'typography_number'): '.elementor-counter-number-wrapper', ('counter', 'number_color'): '.elementor-counter-number-wrapper', ('counter', 'typography_title'): '.elementor-counter-title', ('counter', 'title_color'): '.elementor-counter-title',
       ('toggle', 'title_typography'): '.elementor-toggle-title', ('toggle', 'content_typography'): '.elementor-tab-content', ('toggle', 'content_color'): '.elementor-tab-content'}
PROPS = {'font_family': 'font-family', 'font_size': 'font-size', 'font_weight': 'font-weight', 'line_height': 'line-height',
         'letter_spacing': 'letter-spacing', 'text_transform': 'text-transform', 'font_style': 'font-style'}
def widget_style(e):
    s, k, eid = e['settings'], e.get('widgetType'), e['id']
    g = s.get('__globals__', {})
    for (wk, key), sub in SUB.items():
        if wk != k: continue
        sel = f'.elementor-9 .elementor-element.elementor-element-{eid}' + (' ' + sub if sub else '')
        if key.endswith('_color'):
            ref = g.get(key)
            col = f"var(--e-global-color-{ref.split('=')[1]})" if ref else s.get(key)
            if col: CSSV.append((None, f'{sel}{{color:{col}}}'))
            continue
        ref = g.get(f'{key}_typography')
        if ref:
            i = ref.split('=')[1]
            CSSV.append((None, sel + '{' + ''.join(f'{css}:var(--e-global-typography-{i}-{p.replace("_", "-")})' + (', sans-serif' if p == 'font_family' else '') + ';'
                                                  for p, css in PROPS.items() if f'typography_{p}' in TYPO.get(i, {}) or f'typography_{p}_tablet' in TYPO.get(i, {})) + '}'))
        elif s.get(f'{key}_typography') == 'custom':
            for dev, mq in (('', None), ('_tablet', '(max-width:1024px)'), ('_mobile', '(max-width:767px)')):
                decl = ''
                for p, css in PROPS.items():
                    v = s.get(f'{key}_{p}{dev}')
                    if v in (None, ''): continue
                    decl += f"{css}:{v['size']}{v.get('unit','px')};" if isinstance(v, dict) else f'{css}:{v}' + (', sans-serif' if p == 'font_family' else '') + ';'
                if decl: CSSV.append((mq, f'{sel}{{{decl}}}'))
EA_CSS = ''.join(open(f).read() for f in ['/tmp/claude-0/-home-user-first-search-marketing/cbda635a-c308-5918-bc62-78d4657e8ad1/scratchpad/ea/src/assets/front-end/css/view/testimonials.css'] if os.path.exists(f))
def page(paths, out):
    CSSV.clear()
    body = ''
    for pth in paths: body += ''.join(render(e) for e in json.load(open(pth))['content'])
    css = open('../site-settings.css').read()
    rules = '\n'.join(r for m, r in CSSV if not m)
    for mq in ('(max-width:1024px)', '(max-width:767px)'):
        rules += f'\n@media {mq}{{' + '\n'.join(r for m, r in CSSV if m == mq) + '}'
    doc = f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:ital,wght@0,400;0,500;0,600;0,700;0,800;1,500&display=swap" rel="stylesheet">
<style>body{{margin:0;background:#fff}} img{{max-width:100%}} *{{box-sizing:border-box}} .e-con{{min-width:0}} .elementor-widget{{min-width:0}} p{{margin:0 0 .6em}}</style>
<style>{kit_vars()}</style><style>{EL_DEFAULTS}</style><style>{EA_CSS}</style><style>{css}</style><style>{EL_GLOBALS}</style><style>{rules}</style></head><body class="elementor-kit-5"><div class="elementor elementor-9">{body}</div></body></html>'''
    doc = doc.replace('https://cdn.jsdelivr.net/gh/chrismitchell-cmd/first-search-marketing@4d59b7976a0bacac8601ce9d2eba36ebb43a7779/elementor/upload/first-search/', '../upload/first-search/')
    open(out, 'w').write(doc)
if __name__ == '__main__':
    out = sys.argv[1]
    page([sys.argv[2]] if len(sys.argv) > 2 else [], out)
