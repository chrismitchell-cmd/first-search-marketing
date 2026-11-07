"""Raise the specificity of every rule in site-settings.css by prefixing selectors with `body[class*="elementor-kit-"]`.

Why: Elementor writes default widget styles from Global Colors / Fonts into each page's CSS, e.g.
`.elementor-widget-heading .elementor-heading-title { color: <Primary> }`. That file loads after the
Site Settings CSS and has the same specificity, so it wins. The kit attribute counts as a class, so our rules win every tie.
Idempotent: selectors that already start with body/html/:root are left alone."""
import re, sys

K = 'body[class*="elementor-kit-"]'  # Elementor puts .elementor-kit-N on <body>: counts as a class
def prefix_selector(sel):
    s = sel.strip()
    if not s: return s
    if s.startswith(K) or re.match(r'^(body|html|:root)\b', s): return s
    if s.startswith('[class*="elementor-kit-"]'): return 'body' + s
    return K + ' ' + s

def split_selectors(sel):
    out, depth, cur = [], 0, ''
    for ch in sel:
        if ch in '([': depth += 1
        elif ch in ')]': depth -= 1
        if ch == ',' and depth == 0: out.append(cur); cur = ''
        else: cur += ch
    out.append(cur)
    return out

def transform(css):
    out, i, n = [], 0, len(css)
    stack = []  # 'at' or 'rule'
    buf = ''
    while i < n:
        if css.startswith('/*', i):
            j = css.index('*/', i) + 2
            out.append(buf); buf = ''
            out.append(css[i:j]); i = j; continue
        ch = css[i]
        if ch == '{':
            head = buf
            lead = head[:len(head) - len(head.lstrip())]
            h = head.strip()
            if h.startswith('@'):
                stack.append('at'); out.append(head + '{')
            else:
                stack.append('rule')
                sels = split_selectors(h)
                out.append(lead + ', '.join(prefix_selector(x) for x in sels) + ' {')
            buf = ''; i += 1; continue
        if ch == '}':
            out.append(buf + '}'); buf = ''
            stack.pop(); i += 1; continue
        if ch == ';' and stack and stack[-1] == 'rule':
            out.append(buf + ';'); buf = ''; i += 1; continue
        buf += ch; i += 1
    out.append(buf)
    return ''.join(out)

if __name__ == '__main__':
    p = sys.argv[1]
    s = open(p, encoding='utf-8').read()
    open(p, 'w', encoding='utf-8').write(transform(s))
