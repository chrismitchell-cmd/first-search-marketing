"""Resources page, post-driven: a Loop Item card (filled from each post) and the library section (type tabs and service
filter = Elementor Taxonomy Filters, cards = Loop Grid), with Progressive Dental Care as the featured case study.
WordPress setup it expects: categories blog, case-studies, podcast, videos; service + stage tags (screenshots)."""
import json, urllib.parse
from comp import *
from pages_a import GEO

def dyn(name, **settings):
    """Elementor dynamic tag string, e.g. post-title / post-terms / post-url."""
    return f'[elementor-tag id="{uid()}" name="{name}" settings="{urllib.parse.quote(json.dumps(settings, separators=(",", ":")))}"]'
def H(t, cls, tag='p', url=None, align=None):
    h = heading(t, tag, cls, align)
    if url: h['settings']['link'] = {'url': url, 'is_external': '', 'nofollow': ''}
    return h
def ns(*kids, cls='', **kw):
    return con(*kids, cls=(cls + ' fs-nostyle').strip(), **kw)

# ---------- 1. Loop Item: one resource card ----------
def loop_item():
    """Card = featured image | type pill (category) + date | title | excerpt | tags | link, all from the post.
    The pill colour comes from the post's category class (category-blog, category-case-studies, ...)."""
    img = w('theme-post-featured-image', {'image_size': 'medium_large', 'link_to': 'custom', '__dynamic__': {'link': dyn('post-url')}}, 'fs-li-img')
    pill = H('Resource', 'fs-li-type'); pill['settings']['__dynamic__'] = {'title': dyn('post-terms', taxonomy='category', separator=' ', link='')}
    date = H('Date', 'fs-li-date'); date['settings']['__dynamic__'] = {'title': dyn('post-date', type='published', format='M j, Y')}
    title = H('Post title', 'fs-li-title', 'h3'); title['settings']['__dynamic__'] = {'title': dyn('post-title'), 'link': dyn('post-url')}
    ex = w('theme-post-excerpt', {'excerpt_length': 22}, 'fs-li-ex')
    tags = H('Tags', 'fs-li-tags'); tags['settings']['__dynamic__'] = {'title': dyn('post-terms', taxonomy='post_tag', separator=' · ', link='')}
    more = button('Read more', '#', 'fs-link-u fs-li-more'); more['settings']['__dynamic__'] = {'link': dyn('post-url')}
    body = con(ns(pill, date, d='row', gap_=8, align='center', mobile_col=False, wrap=True), title, ex, tags, more, gap_=10, cls='fs-li-body', p=pad(22, 22, 24, 22))
    return con(img, body, gap_=0, cls='fs-gcard fs-rcard fs-li', p=pad(0))

# ---------- 2. Library section ----------
FEATURED = dict(stat='8x', label='more digital leads a month', meta='Dental practice · South Portland, ME',
                title='Progressive Dental Care: from 12 leads a month to 100+.',
                text='A new owner, a dated brand and an agency that never delivered. A rebrand, local SEO, reviews and ads later, digital leads now outnumber referrals for the first time in the practice’s history.',
                url='/case-studies/progressive-dental-care/', img='assets/img/design/case-dental.webp')

def library(loop_item_id=''):
    f = FEATURED
    feat = con(con(image(f['img'], 'fs-rfeat-img', None, 'center', 'Progressive Dental Care'),
                   ns(H(f['stat'], 'fs-rf-n'), H(f['label'], 'fs-rf-l'), H(f['meta'], 'fs-rf-m'), gap_=2, cls='fs-rf-box', p=pad(14, 18)), cls='fs-rfeat-l'),
               con(H('Featured case study', 'fs-rf-badge'), heading(f['title'], 'h2', 'fs-rfeat-h'), text(f['text'], 'fs-rfeat-p'),
                   button('Read the case study', f['url'], 'fs-btn-grad fs-btn-lg'), gap_=14, cls='fs-rfeat-r', p=pad(20, 40, 20, 40), s={'padding_mobile': pad(20, 8)}),
               d='row', gap_=0, align='stretch', cls='fs-rfeat fs-dark', p=pad(16))
    grid = w('loop-grid', {'template_id': loop_item_id, '_skin': 'post', 'columns': 3, 'columns_tablet': 2, 'columns_mobile': 1,
                           'posts_per_page': 9, 'equal_height': 'yes', 'post_query_post_type': 'post', 'post_query_orderby': 'post_date', 'post_query_order': 'desc',
                           'pagination_type': 'load_more_on_click', 'load_more_spinner': {'value': 'fas fa-spinner', 'library': 'fa-solid'},
                           'nothing_found_message_text': 'Nothing matches that filter yet. New resources go up every week.'}, 'fs-lgrid')
    gid = grid['id']
    types = w('taxonomy-filter', {'selected_element': gid, 'taxonomy': 'category', 'show_first_item': 'yes', 'first_item_title': 'All',
                                  'exclude': ['uncategorized'], 'direction': 'horizontal'}, 'fs-tfilter fs-tfilter--types')
    tags = w('taxonomy-filter', {'selected_element': gid, 'taxonomy': 'post_tag', 'show_first_item': 'yes', 'first_item_title': 'All services',
                                 'multiple_selection': 'yes', 'logical_combination': 'OR', 'direction': 'horizontal'}, 'fs-tfilter fs-tfilter--tags')
    band = section(types, cls='fs-dark fs-band fs-catsband', title='Resource type tabs',
                   p={'unit': 'px', 'top': '14', 'right': '24', 'bottom': '14', 'left': '24', 'isLinked': False},
                   s={'padding_mobile': {'unit': 'px', 'top': '12', 'right': '16', 'bottom': '12', 'left': '16', 'isLinked': False}})
    side = con(H('Filter by service', 'fs-rside-t2'), tags, cls='fs-gcard fs-rside', gap_=14, p=pad(26, 22, 26, 22))
    main = con(feat, grid, gap_=28, cls='fs-rmain')
    body = section(con(side, main, d='row', gap_=44, align='flex-start', cls='fs-rbody fs-nostyle'), cls='fs-geo', title='Resource library',
                   bg_img='assets/img/design/bg-geometric.jpg', p={'unit': 'px', 'top': '56', 'right': '24', 'bottom': '100', 'left': '24', 'isLinked': False},
                   s={'_element_id': 'library'})
    return [band, body]
