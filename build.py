#!/usr/bin/env python3
"""Generate the Chinese versions of the site from the English pages.

Edit the English pages (index.html, services.html, ...) and their I18N
translations, then run:  python3 build.py
It rewrites zh-tw/*.html, zh-cn/*.html, the hreflang tags on every page,
and sitemap.xml. Needs: pip install beautifulsoup4
"""
import re, json, os, glob
from bs4 import BeautifulSoup

SITE = 'https://www.kokonipets.com'
PAGES = ['index', 'meet-us', 'services', 'faq', 'contact', 'compare-styles'] + \
        sorted(f[:-5] for f in glob.glob('dog-grooming-*.html'))
LANGS = {'zh-TW': 'zh-tw', 'zh-CN': 'zh-cn'}
HREFLANG = {'en': 'en', 'zh-TW': 'zh-Hant', 'zh-CN': 'zh-Hans'}

# Titles / descriptions for pages whose I18N has no meta_title / meta_description
META = {
  'meet-us': {
    'zh-TW': ('認識我們 | KOKONI 寵物美容沙龍 | 聖蓋博 San Gabriel',
              '認識聖蓋博 KOKONI 寵物沙龍的美容師團隊。以溫柔專業的手法照顧每隻毛孩，重視牠們的舒適與安全。'),
    'zh-CN': ('认识我们 | KOKONI 宠物美容沙龙 | 圣盖博 San Gabriel',
              '认识圣盖博 KOKONI 宠物沙龙的美容师团队。以温柔专业的手法照顾每只毛孩，重视它们的舒适与安全。')},
  'services': {
    'zh-TW': ('狗狗美容服務與價格 | KOKONI 寵物沙龍 | 聖蓋博 San Gabriel',
              '查看聖蓋博 KOKONI 寵物沙龍的狗狗美容服務與價格：全套美容、洗澡修剪、幼犬初次美容等，歡迎線上預約。'),
    'zh-CN': ('狗狗美容服务与价格 | KOKONI 宠物沙龙 | 圣盖博 San Gabriel',
              '查看圣盖博 KOKONI 宠物沙龙的狗狗美容服务与价格：全套美容、洗澡修剪、幼犬初次美容等，欢迎在线预约。')},
  'faq': {
    'zh-TW': ('常見問題 | KOKONI 寵物美容沙龍 | 聖蓋博 San Gabriel',
              'KOKONI 寵物美容常見問題：疫苗與安全、價格、預約方式，以及第一次來店須知。'),
    'zh-CN': ('常见问题 | KOKONI 宠物美容沙龙 | 圣盖博 San Gabriel',
              'KOKONI 宠物美容常见问题：疫苗与安全、价格、预约方式，以及第一次来店须知。')},
  'contact': {
    'zh-TW': ('聯絡我們與營業時間 | KOKONI 寵物美容沙龍 | 聖蓋博 San Gabriel',
              '聯絡聖蓋博 KOKONI 寵物美容沙龍：線上預約、導航或來電 (626) 621-4646。週一、週三至週五、週日營業（採預約制）。'),
    'zh-CN': ('联系我们与营业时间 | KOKONI 宠物美容沙龙 | 圣盖博 San Gabriel',
              '联系圣盖博 KOKONI 宠物美容沙龙：在线预约、导航或来电 (626) 621-4646。周一、周三至周五、周日营业（预约制）。')},
  'compare-styles': {
    'zh-TW': ('日常造型 — 簡單可愛 | KOKONI 寵物美容 | 聖蓋博',
              '聖蓋博 KOKONI 寵物美容的「簡單可愛」日常造型介紹，以及與亞洲風格造型的差別，幫您選出最適合愛犬的造型。'),
    'zh-CN': ('日常造型 — 简单可爱 | KOKONI 宠物美容 | 圣盖博',
              '圣盖博 KOKONI 宠物美容的“简单可爱”日常造型介绍，以及与亚洲风格造型的区别，帮您选出最适合爱犬的造型。')},
}

def url(page, lang):
    pre = '/' + LANGS[lang] if lang in LANGS else ''
    path = '' if page == 'index' else '/' + page
    return SITE + ((pre + path) or '/')

def hreflang_block(page):
    lines = ['<!--hreflang-->']
    for lang, code in HREFLANG.items():
        lines.append('<link rel="alternate" hreflang="%s" href="%s" />' % (code, url(page, lang)))
    lines.append('<link rel="alternate" hreflang="x-default" href="%s" />' % url(page, 'en'))
    lines.append('<!--/hreflang-->')
    return '\n  '.join(lines)

def set_hreflang(html, page):
    html = re.sub(r'\s*<!--hreflang-->.*?<!--/hreflang-->', '', html, flags=re.S)
    return html.replace('</head>', '  ' + hreflang_block(page) + '\n</head>', 1)

def set_faq_schema(html):
    """FAQPage structured data built from the questions visible on the page."""
    html = re.sub(r'\s*<!--faq-schema-->.*?<!--/faq-schema-->', '', html, flags=re.S)
    soup = BeautifulSoup(html, 'html.parser')
    items = []
    for it in soup.select('.faq-item'):
        q, a = it.select_one('.faq-q span'), it.select_one('.faq-a')
        if q and a:
            items.append({'@type': 'Question', 'name': q.get_text(' ', strip=True),
                          'acceptedAnswer': {'@type': 'Answer', 'text': a.get_text(' ', strip=True)}})
    if not items:
        return html
    data = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': items},
                      ensure_ascii=False, indent=2)
    block = '<!--faq-schema-->\n  <script type="application/ld+json">\n%s\n  </script>\n  <!--/faq-schema-->' % data
    return html.replace('</head>', '  ' + block + '\n</head>', 1)

def load_i18n(html):
    m = re.search(r'const I18N = (\{.*?\n\});', html, re.S)
    return json.loads(m.group(1))

def localize(html, page, lang):
    i18n = load_i18n(html)
    folder = LANGS[lang]
    soup = BeautifulSoup(html, 'html.parser')
    soup.html['lang'] = lang
    for el in soup.select('[data-i18n]'):
        v = i18n.get(el['data-i18n'], {}).get(lang)
        if v is not None:
            el.clear()
            el.append(BeautifulSoup(v, 'html.parser'))
    for el in soup.select('[data-i18n-placeholder]'):
        v = i18n.get(el['data-i18n-placeholder'], {}).get(lang)
        if v is not None:
            el['placeholder'] = v
    for b in soup.select('.lang-btn'):
        cls = [c for c in b.get('class', []) if c != 'lang-active']
        if b.get('data-lang') == lang:
            cls.append('lang-active')
        b['class'] = cls
    if page in META:
        title, desc = META[page][lang]
    else:
        title = i18n['meta_title'][lang]
        desc = i18n['meta_description'][lang]
    soup.title.string = title
    for sel, val in [('meta[name="description"]', desc), ('meta[property="og:description"]', desc),
                     ('meta[name="twitter:description"]', desc), ('meta[property="og:title"]', title),
                     ('meta[name="twitter:title"]', title), ('meta[property="og:url"]', url(page, lang))]:
        tag = soup.select_one(sel)
        if tag:
            tag['content'] = val
    soup.select_one('link[rel="canonical"]')['href'] = url(page, lang)
    out = str(soup)
    out = out.replace("var PAGE_LANG = 'en';", "var PAGE_LANG = '%s';" % lang)
    # relative assets -> absolute, since these pages live one folder down
    out = re.sub(r'''(\s(?:src|href|poster)=")(?!https?:|//|/|#|mailto:|tel:|data:|javascript:)([^"]+)"''', r'\1/\2"', out)
    out = re.sub(r'''url\((['"]?)(?!https?:|//|/|data:|#)''', r'url(\1/', out)
    # internal page links -> same language (also inside I18N strings: href=\"/faq\")
    pages = '|'.join(p for p in PAGES if p != 'index')
    def link(m):
        q1, p, frag, q2 = m.group(1), m.group(2) or '', m.group(3) or '', m.group(4)
        return 'href=%s/%s%s%s%s' % (q1, folder, '/' + p if p else '', frag, q2)
    out = re.sub(r'href=(\\?")/(%s)?(#[^"\\]*)?(\\?")' % pages, link, out)
    out = set_hreflang(out, page)
    return set_faq_schema(out) if page == 'faq' else out

def sitemap():
    rows = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for page in PAGES:
        for lang in HREFLANG:
            rows.append('  <url>\n    <loc>%s</loc>' % url(page, lang))
            for l2, code in HREFLANG.items():
                rows.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s" />' % (code, url(page, l2)))
            rows.append('    <xhtml:link rel="alternate" hreflang="x-default" href="%s" />\n  </url>' % url(page, 'en'))
    rows.append('</urlset>\n')
    return '\n'.join(rows)

if __name__ == '__main__':
    for page in PAGES:
        src = page + '.html'
        html = open(src, encoding='utf-8').read()
        html = set_hreflang(html, page)
        if page == 'faq':
            html = set_faq_schema(html)
        open(src, 'w', encoding='utf-8').write(html)
        for lang, folder in LANGS.items():
            os.makedirs(folder, exist_ok=True)
            open(os.path.join(folder, src), 'w', encoding='utf-8').write(localize(html, page, lang))
    open('sitemap.xml', 'w', encoding='utf-8').write(sitemap())
    print('Built', len(PAGES) * 2, 'Chinese pages + sitemap.xml')
