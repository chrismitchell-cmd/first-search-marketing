"""Builds elementor/first-search-site-settings.zip: an Elementor Website Kit containing only Site Settings
(Elementor > Tools > Import/Export > Import). Format matches Elementor's import-export module (format 2.0):
manifest.json + site-settings.json ({settings, experiments})."""
import json, zipfile, datetime, os
from styler import SYSTEM_COLORS, CUSTOM_COLORS, typo_settings

def px(n): return {'unit': 'px', 'size': n, 'sizes': []}
def build(out_path, custom_typography, css):
    def ty(fam, fw, size=None, lh=None):
        d = {'typography_typography': 'custom', 'typography_font_family': fam, 'typography_font_weight': fw}
        if size: d['typography_font_size'] = px(size)
        if lh: d['typography_line_height'] = {'unit': 'em', 'size': lh, 'sizes': []}
        return d
    settings = {
        # Global Colors / Global Fonts
        'system_colors': [{'_id': i, 'title': t, 'color': c} for i, t, c in SYSTEM_COLORS],
        'custom_colors': [{'_id': i, 'title': t, 'color': c} for i, t, c in CUSTOM_COLORS],
        'system_typography': [dict({'_id': 'primary', 'title': 'Primary (headings)'}, **ty('Poppins', '700')),
                              dict({'_id': 'secondary', 'title': 'Secondary (subheads)'}, **ty('Poppins', '600')),
                              dict({'_id': 'text', 'title': 'Text (body)'}, **ty('Poppins', '400', 18, 1.6)),
                              dict({'_id': 'accent', 'title': 'Accent (UI, labels)'}, **ty('Inter', '500'))],
        'custom_typography': custom_typography,
        # Theme Style > Typography
        'body_color': '#1C1B22',
        'body_typography_typography': 'custom', 'body_typography_font_family': 'Poppins', 'body_typography_font_weight': '400',
        'body_typography_font_size': px(18), 'body_typography_line_height': {'unit': 'em', 'size': 1.6, 'sizes': []},
        **{f'h{n}_{k}': v for n in range(1, 7) for k, v in (('color', '#250762'), ('typography_typography', 'custom'), ('typography_font_family', 'Poppins'), ('typography_font_weight', '700'))},
        # Layout: HTML content width, no default container padding, 20px gaps
        'container_width': px(1240),
        'container_padding': {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': True},
        'space_between_widgets': {'column': '20', 'row': '20', 'unit': 'px', 'isLinked': True},
        'page_title_selector': 'h1.entry-title',
        # Background
        'body_background_background': 'classic', 'body_background_color': '#F8F7F7',
        # Custom CSS (Elementor Pro)
        'custom_css': css,
    }
    exp = {n: {'name': n, 'title': t, 'state': 'active', 'default': 'inactive', 'release_status': 'stable'}
           for n, t in (('container', 'Flexbox Container'), ('nested-elements', 'Nested Elements'), ('mega-menu', 'Menu'))}
    site_settings = {'content': [], 'settings': settings, 'experiments': exp}
    # Manifest in Elementor's current export format (import/export format 3.0)
    manifest = {
        'name': 'first-search-site-settings', 'title': 'First Search Marketing - Site Settings',
        'description': 'Global colors, global fonts, typography, layout, background and custom CSS for the First Search Marketing templates.',
        'author': 'First Search Marketing', 'version': '3.0', 'elementor_version': '3.30.0',
        'created': datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), 'thumbnail': False, 'site': 'https://befirstsearch.com',
        'site-settings': {'theme': False, 'globalColors': True, 'globalFonts': True, 'themeStyleSettings': True, 'generalSettings': True,
                          'experiments': True, 'customCode': False, 'customIcons': False, 'customFonts': False, 'classes': False, 'variables': False},
        'experiments': list(exp.keys()),
    }
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('manifest.json', json.dumps(manifest, indent=1))
        z.writestr('site-settings.json', json.dumps(site_settings, indent=1))
    return settings
