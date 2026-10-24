#!/usr/bin/env python3
"""Create the city landing pages (dog-grooming-<city>.html) from contact.html's
header/footer and the content below. Run once after editing CITY content,
then run build.py for the Chinese versions. Needs: pip install opencc-python-reimplemented
"""
import re, json
import opencc
S2 = opencc.OpenCC('tw2sp')

DIRECTIONS = 'https://www.google.com/maps/dir/?api=1&destination=1381+E+Las+Tunas+Dr+%2311+San+Gabriel+CA+91776'

CITIES = {
 'arcadia': dict(en='Arcadia', zh='阿凱迪亞',
  intro=("From the Santa Anita area to the neighborhoods around the LA County Arboretum, Arcadia dog owners don't have to go far for careful, unhurried grooming. Kokoni is just west of Arcadia on Las Tunas Drive in San Gabriel.",
         "從 Santa Anita 一帶到洛杉磯郡植物園（LA County Arboretum）附近的社區，阿凱迪亞的狗主人不用跑太遠，就能享有細心、不趕時間的美容服務。KOKONI 就在阿凱迪亞西邊，位於聖蓋博的 Las Tunas Drive 上。"),
  route=("Las Tunas Drive runs from Arcadia through Temple City into San Gabriel. Head west on Las Tunas and you'll reach us at 1381 E Las Tunas Dr #11.",
         "Las Tunas Drive 從阿凱迪亞經過天普市一路通到聖蓋博。沿著 Las Tunas 往西開，就會抵達我們的店：1381 E Las Tunas Dr #11。"),
  faq=("How far is Kokoni from Arcadia?",
       "We're in San Gabriel, just west of Arcadia along Las Tunas Drive — a simple drive with no freeway needed.",
       "KOKONI 離阿凱迪亞多遠？",
       "我們在聖蓋博，就在阿凱迪亞西邊的 Las Tunas Drive 上，不用上高速公路，開車很方便。")),
 'temple-city': dict(en='Temple City', zh='天普市',
  intro=("Kokoni sits on Las Tunas Drive — the same street that runs through downtown Temple City — so getting your dog to a groom is easy.",
         "KOKONI 就在 Las Tunas Drive 上，也就是貫穿天普市市中心的那條路，帶狗狗來美容非常方便。"),
  route=("From downtown Temple City or the Temple City Park area, head west on Las Tunas Drive. We're at 1381 E Las Tunas Dr #11, San Gabriel.",
         "從天普市市中心或天普市公園（Temple City Park）一帶，沿 Las Tunas Drive 往西開，就到我們的店：1381 E Las Tunas Dr #11, San Gabriel。"),
  faq=("Is Kokoni a good fit for nervous or senior dogs?",
       "Yes. We work patiently and gently. Please tell us about any health conditions so we can adjust the grooming process.",
       "KOKONI 適合容易緊張或年紀大的狗狗嗎？",
       "適合。我們會耐心、溫柔地進行美容。如果狗狗有任何健康狀況，請事先告訴我們，我們會調整美容流程。")),
 'alhambra': dict(en='Alhambra', zh='阿罕布拉',
  intro=("From Main Street to the neighborhoods around Almansor Park, Alhambra families can reach Kokoni in San Gabriel without getting on the freeway.",
         "不論您住在 Main Street 附近，還是 Almansor Park 周邊的社區，從阿罕布拉到聖蓋博的 KOKONI 都不用上高速公路。"),
  route=("Take Main Street east — it continues as Las Tunas Drive in San Gabriel — and follow it to 1381 E Las Tunas Dr #11.",
         "沿 Main Street 往東開，進入聖蓋博後會接上 Las Tunas Drive，繼續開到 1381 E Las Tunas Dr #11 就到了。"),
  faq=("What's the difference between Simply Cute and Asian Fusion?",
       "Simply Cute is a shorter, easy-care cut that keeps your dog tidy between visits. Asian Fusion keeps the body hair longer and uses hand scissoring for a soft, rounded look — it takes longer and needs more upkeep.",
       "日常造型和精緻造型有什麼不同？",
       "日常造型是較短、好整理的剪法，讓狗狗在兩次美容之間都保持整潔。精緻造型會保留較長的毛，用手工剪刀修出圓潤可愛的造型，需要較長時間，平常也需要多一點照顧。")),
 'san-marino': dict(en='San Marino', zh='聖馬力諾',
  intro=("San Marino borders San Gabriel, so Kokoni is close by whether you live near Huntington Drive or Lacy Park.",
         "聖馬力諾就在聖蓋博隔壁，不論您住在 Huntington Drive 還是 Lacy Park 附近，到 KOKONI 都很近。"),
  route=("Take San Gabriel Boulevard or Rosemead Boulevard south to Las Tunas Drive. We're at 1381 E Las Tunas Dr #11 — tap Get directions below for turn-by-turn directions.",
         "沿 San Gabriel Boulevard 或 Rosemead Boulevard 往南開到 Las Tunas Drive，我們的地址是 1381 E Las Tunas Dr #11。點下方的「開始導航」可以看詳細路線。"),
  faq=("Do you groom doodles?",
       "Yes. Doodles have their own pricing because their coat needs extra time and care.",
       "你們有幫 Doodle 美容嗎？",
       "有的。Doodle 的毛需要較多時間和照顧，所以有另外的價格。")),
 'pasadena': dict(en='Pasadena', zh='帕薩迪納',
  intro=("Whether you're in East Pasadena, Hastings Ranch or closer to Old Pasadena, Kokoni in San Gabriel is an easy trip south for calm, one-on-one grooming.",
         "不論您住在東帕薩迪納、Hastings Ranch 還是 Old Pasadena 附近，往南開一小段路，就能到聖蓋博的 KOKONI 享受安靜、一對一的美容。"),
  route=("From the 210 Freeway, take Rosemead Boulevard south to Las Tunas Drive. We're at 1381 E Las Tunas Dr #11, San Gabriel.",
         "從 210 號高速公路下 Rosemead Boulevard，往南開到 Las Tunas Drive。我們的地址是 1381 E Las Tunas Dr #11, San Gabriel。"),
  faq=("Can I stay during the grooming?",
       "For safety and focus, we don't allow owners to stay during the grooming session.",
       "美容時我可以在旁邊陪嗎？",
       "為了安全和讓美容師專心，美容過程中不開放主人陪同。")),
}

def common(c):
    en, zh = c['en'], c['zh']
    return {
     'meta_title': ("Dog Grooming near %s, CA | Kokoni Pet Salon in San Gabriel" % en,
                    "%s %s 附近狗狗美容 | KOKONI 寵物沙龍（聖蓋博）" % (zh, en)),
     'meta_description': ("Gentle, one-on-one dog grooming for %s pets at Kokoni Pet Salon in San Gabriel. Baths, haircuts and Asian Fusion styling. Book online or call (626) 621-4646." % en,
                    "%s附近的狗狗美容：KOKONI 寵物沙龍位於聖蓋博，一對一溫柔美容，提供洗澡、剪毛與精緻造型。線上預約或來電 (626) 621-4646。" % zh),
     'city_h1': ("Dog Grooming near %s" % en, "%s %s 附近的狗狗美容" % (zh, en)),
     'city_sub': ("Gentle, one-on-one grooming at Kokoni Pet Salon in San Gabriel — a short drive from %s." % en,
                  "聖蓋博 KOKONI 寵物沙龍，一對一溫柔美容，從%s開車過來很近。" % zh),
     'city_intro': c['intro'],
     'route_h': ("Getting here from %s" % en, "從%s怎麼來" % zh),
     'route_p': c['route'],
     'route_btn': ("Get directions", "開始導航"),
     'svc_h': ("Grooming services", "美容服務"),
     'svc1_t': ("Bath &amp; Brushing", "洗澡 &amp; 梳毛"),
     'svc1_p': ("Bath, hand blow-dry, nail trim, ear cleaning and teeth brushing. From $50.",
                "洗澡、手工吹整、剪指甲、清耳朵和刷牙。$50 起。"),
     'svc2_t': ("Simply Cute Everyday Style", "日常造型"),
     'svc2_p': ("A shorter, easy-care haircut that keeps your dog clean and comfortable between visits.",
                "較短、好整理的剪法，讓狗狗在兩次美容之間都乾淨舒服。"),
     'svc3_t': ("Asian Fusion Style", "精緻造型"),
     'svc3_p': ("Longer body hair and skilled hand scissoring for a soft, rounded look.",
                "保留較長的毛，以手工剪刀修出圓潤可愛的造型。"),
     'svc_link': ("See all services &amp; pricing →", "查看所有服務與價格 →"),
     'why_h': ("What to expect at Kokoni", "在 KOKONI 美容是什麼樣子"),
     'why1': ("<strong>One-on-one grooming.</strong> We focus on one dog at a time to keep stress low.",
              "<strong>一對一美容。</strong>一次專心照顧一隻狗狗，降低緊張感。"),
     'why2': ("<strong>Limited appointments.</strong> We keep each day's schedule small, so waiting time stays short.",
              "<strong>限量預約。</strong>每天只接有限的預約，減少等待時間。"),
     'why3': ("<strong>Clean, individual kennels</strong> whenever dogs need to be kept apart.",
              "<strong>乾淨的獨立籠位</strong>，需要分開時讓每隻狗狗都安全。"),
     'why4': ("<strong>Vaccines required.</strong> Rabies, Bordetella and Distemper vaccines are required for every dog, so everyone stays healthy.",
              "<strong>需要疫苗記錄。</strong>每隻狗狗都需要狂犬病、犬舍咳和犬瘟熱疫苗，保護大家的健康。"),
     'faq_h': ("Common questions", "常見問題"),
     'faq1_q': (c['faq'][0], c['faq'][2]),
     'faq1_a': (c['faq'][1], c['faq'][3]),
     'faq2_q': ("Do I need an appointment?", "需要預約嗎？"),
     'faq2_a': ("Yes — we groom by appointment only. Book online, or text or call (626) 621-4646.",
                "需要。我們採預約制，請線上預約，或傳簡訊、來電 (626) 621-4646。"),
     'cta_book': ("Book an appointment", "立即預約"),
     'cta_call': ("Text or call (626) 621-4646", "簡訊或來電 (626) 621-4646"),
     'also_h': ("We also welcome dogs from", "我們也歡迎來自這些城市的狗狗"),
    }

CSS = """
    /* ── City landing pages ── */
    .city-hero { background: #D8EBFD; padding: 56px 80px 48px; text-align: center; }
    .city-hero h1 { font-family: 'DM Serif Display', serif; color: #1C4F95; font-size: 2.4rem; font-weight: 400; line-height: 1.2; margin-bottom: 14px; }
    .city-hero .city-sub { color: #1C4F95; font-weight: 600; font-size: 1.05rem; margin-bottom: 18px; }
    .city-hero .city-intro { max-width: 720px; margin: 0 auto; line-height: 1.75; color: #2c2c2c; }
    .city-cta { display: flex; gap: 14px; justify-content: center; flex-wrap: wrap; margin-top: 26px; }
    .city-cta a { text-decoration: none; font-weight: 700; border-radius: 30px; padding: 12px 26px; font-size: 0.95rem; }
    .city-cta .cta-book { background: #F07840; color: #fff; }
    .city-cta .cta-call { background: #fff; color: #1C4F95; border: 2px solid #1C4F95; }
    .city-section { padding: 52px 80px; max-width: 1100px; margin: 0 auto; }
    .city-section h2 { font-family: 'DM Serif Display', serif; color: #1C4F95; font-size: 1.8rem; font-weight: 400; margin-bottom: 18px; }
    .city-section p, .city-section li { line-height: 1.75; }
    .route-btn { display: inline-block; margin-top: 16px; color: #1C4F95; font-weight: 700; text-decoration: none; border-bottom: 2px solid #46BFBF; }
    .svc-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
    .svc-card { background: #fff; border-radius: 16px; padding: 24px; box-shadow: 0 2px 10px rgba(28,79,149,0.08); }
    .svc-card h3 { color: #1C4F95; font-size: 1.05rem; margin-bottom: 8px; }
    .svc-link { display: inline-block; margin-top: 18px; color: #1C4F95; font-weight: 700; text-decoration: none; }
    .why-list { list-style: none; display: grid; gap: 12px; }
    .why-list li { padding-left: 28px; position: relative; }
    .why-list li::before { content: '✓'; position: absolute; left: 0; color: #46BFBF; font-weight: 800; }
    .city-faq dt { font-weight: 700; color: #1C4F95; margin-top: 14px; }
    .city-faq dd { margin: 6px 0 0; line-height: 1.75; }
    .city-band { background: #EDF6FB; }
    .also-links { display: flex; flex-wrap: wrap; gap: 10px; }
    .also-links a { background: #fff; border: 1.5px solid #1C4F95; color: #1C4F95; border-radius: 20px; padding: 6px 16px; text-decoration: none; font-weight: 600; font-size: 0.9rem; }
    @media (max-width: 900px) {
      .city-hero { padding: 40px 24px 36px; }
      .city-hero h1 { font-size: 1.9rem; }
      .city-section { padding: 40px 24px; }
      .svc-grid { grid-template-columns: 1fr; }
    }
"""

def body(slug, c):
    others = ''.join('<a href="/dog-grooming-%s" data-i18n="city_%s">%s</a>' % (s, s.replace('-', '_'), o['en'])
                     for s, o in CITIES.items() if s != slug)
    return """<!-- ══════════════════════════════
     CITY LANDING
══════════════════════════════ -->
<section class="city-hero">
  <h1 data-i18n="city_h1"></h1>
  <p class="city-sub" data-i18n="city_sub"></p>
  <p class="city-intro" data-i18n="city_intro"></p>
  <div class="city-cta">
    <a href="https://book.kokonipets.com/book" class="btn-book cta-book" target="_blank" rel="noopener" data-i18n="cta_book"></a>
    <a href="tel:6266214646" class="cta-call" data-i18n="cta_call"></a>
  </div>
</section>

<section class="city-section">
  <h2 data-i18n="route_h"></h2>
  <p data-i18n="route_p"></p>
  <a class="route-btn" href="%(dir)s" target="_blank" rel="noopener" data-i18n="route_btn"></a>
</section>

<div class="city-band">
<section class="city-section">
  <h2 data-i18n="svc_h"></h2>
  <div class="svc-grid">
    <div class="svc-card"><h3 data-i18n="svc1_t"></h3><p data-i18n="svc1_p"></p></div>
    <div class="svc-card"><h3 data-i18n="svc2_t"></h3><p data-i18n="svc2_p"></p></div>
    <div class="svc-card"><h3 data-i18n="svc3_t"></h3><p data-i18n="svc3_p"></p></div>
  </div>
  <a class="svc-link" href="/services" data-i18n="svc_link"></a>
</section>
</div>

<section class="city-section">
  <h2 data-i18n="why_h"></h2>
  <ul class="why-list">
    <li data-i18n="why1"></li><li data-i18n="why2"></li><li data-i18n="why3"></li><li data-i18n="why4"></li>
  </ul>
</section>

<div class="city-band">
<section class="city-section">
  <h2 data-i18n="faq_h"></h2>
  <dl class="city-faq">
    <dt data-i18n="faq1_q"></dt><dd data-i18n="faq1_a"></dd>
    <dt data-i18n="faq2_q"></dt><dd data-i18n="faq2_a"></dd>
  </dl>
</section>
</div>

<section class="city-section">
  <h2 data-i18n="also_h"></h2>
  <div class="also-links">%(others)s</div>
</section>

""" % {'dir': DIRECTIONS, 'others': others}

def fill_english(html, i18n):
    # put the English text into each data-i18n element so the page works without JS
    def rep(m):
        key = m.group(2)
        return m.group(1) + i18n[key]['en'] + m.group(3) if key in i18n and m.group(4) == '' else m.group(0)
    return re.sub(r'(<(?:h1|h2|h3|p|a|li|dt|dd)\b[^>]*data-i18n="([^"]+)"[^>]*>)()()(?=</)', lambda m: m.group(1) + i18n[m.group(2)]['en'] if m.group(2) in i18n else m.group(0), html)

base = open('contact.html', encoding='utf-8').read()
base_i18n = json.loads(re.search(r'const I18N = (\{.*?\n\});', base, re.S).group(1))
start = base.index('<!-- ══════════════════════════════\n     WELCOME STRIP')
end = base.index('<!-- ══════════════════════════════\n     INFO STRIP')

for slug, c in CITIES.items():
    url = 'https://www.kokonipets.com/dog-grooming-' + slug
    texts = common(c)
    i18n = {k: v for k, v in base_i18n.items() if k.startswith(('nav_', 'footer_', 'info_', 'sister_'))}
    for k, (en, tw) in texts.items():
        i18n[k] = {'en': en, 'zh-TW': tw, 'zh-CN': S2.convert(tw)}
    for s, o in CITIES.items():
        i18n['city_' + s.replace('-', '_')] = {'en': o['en'], 'zh-TW': o['zh'] + ' ' + o['en'], 'zh-CN': S2.convert(o['zh']) + ' ' + o['en']}
    h = base[:start] + body(slug, c) + base[end:]
    h = h.replace('<a href="/contact" class="active" data-i18n="nav_contact">', '<a href="/contact" data-i18n="nav_contact">')
    title, desc = texts['meta_title'][0], texts['meta_description'][0]
    h = re.sub(r'<meta name="description" content="[^"]*"', '<meta name="description" content="%s"' % desc, h)
    h = re.sub(r'<link rel="canonical" href="[^"]*"', '<link rel="canonical" href="%s"' % url, h)
    h = re.sub(r'<meta property="og:url" content="[^"]*"', '<meta property="og:url" content="%s"' % url, h)
    for p in ('og:title', 'og:description'):
        h = re.sub(r'<meta property="%s" content="[^"]*"' % p, '<meta property="%s" content="%s"' % (p, title if 'title' in p else desc), h)
    for p in ('twitter:title', 'twitter:description'):
        h = re.sub(r'<meta name="%s" content="[^"]*"' % p, '<meta name="%s" content="%s"' % (p, title if 'title' in p else desc), h)
    h = re.sub(r'<title>[^<]*</title>', '<title>%s</title>' % title, h)
    h = h.replace('    </style>', CSS + '    </style>', 1)
    h = re.sub(r'const I18N = \{.*?\n\};', lambda m: 'const I18N = ' + json.dumps(i18n, ensure_ascii=False, indent=2) + ';', h, count=1, flags=re.S)
    h = fill_english(h, i18n)
    open('dog-grooming-%s.html' % slug, 'w', encoding='utf-8').write(h)
    print('wrote dog-grooming-%s.html' % slug)
