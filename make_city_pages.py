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
    .af-photo { display: block; width: 100%; max-width: 420px; border-radius: 16px; margin: 20px 0 4px; }
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
    return body_template(others)

def body_template(others):
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

# ── Service page: walk-in nail trimming ─────────────────────────────
NAIL = {
 'meta_title': ("Dog Nail Trimming, Walk-ins Welcome | Kokoni Pet Salon, San Gabriel",
                "狗狗剪指甲 歡迎 Walk-in | KOKONI 寵物沙龍（聖蓋博）"),
 'meta_description': ("Walk-in dog nail trimming for $15 at Kokoni Pet Salon in San Gabriel, near Arcadia, Temple City, Alhambra and Pasadena. No bath needed. Text or call (626) 621-4646.",
                "聖蓋博 KOKONI 寵物沙龍提供狗狗剪指甲服務，$15，不用洗澡，歡迎 walk-in。鄰近阿凱迪亞、天普市、阿罕布拉、帕薩迪納。簡訊或來電 (626) 621-4646。"),
 'city_h1': ("Dog Nail Trimming — Walk-ins Welcome", "狗狗剪指甲，歡迎 Walk-in"),
 'city_sub': ("Quick, gentle nail trims for $15 at Kokoni Pet Salon in San Gabriel. No bath or appointment needed.",
              "聖蓋博 KOKONI 寵物沙龍，快速又溫柔的剪指甲服務，$15，不用洗澡，也不用預約。"),
 'city_intro': ("Long nails can make walking uncomfortable and change the way your dog stands. Stop by during our opening hours for a quick trim — our groomers handle every paw calmly and carefully, even for dogs who are nervous about having their feet touched.",
                "指甲太長會讓狗狗走路不舒服，甚至影響站姿。營業時間內直接過來就可以快速修剪。美容師會冷靜、細心地處理每一隻腳，就算是怕被摸腳的狗狗也一樣。"),
 'cta_book': ("Get directions", "開始導航"),
 'cta_call': ("Text or call (626) 621-4646", "簡訊或來電 (626) 621-4646"),
 'svc_h': ("Prices", "價格"),
 'svc1_t': ("Nail trimming — $15", "剪指甲 $15"),
 'svc1_p': ("Walk-ins welcome during opening hours. No bath needed.", "營業時間內歡迎 walk-in，不用洗澡。"),
 'svc2_t': ("Add-ons", "加購項目"),
 'svc2_p': ("Pads trim $10 · Ear cleaning $10 · Teeth brushing $10 · Gland expression (external) $15",
            "腳掌修毛 $10 · 耳道清潔 $10 · 刷牙 $10 · 肛門腺清潔（外部）$15"),
 'svc3_t': ("Need a full groom?", "需要完整美容？"),
 'svc3_p': ("Every bath and haircut already includes a nail trim. Book online for a full groom.",
            "每次洗澡和美容都已經包含剪指甲。完整美容請線上預約。"),
 'svc_link': ("See all services &amp; pricing →", "查看所有服務與價格 →"),
 'why_h': ("Before you come in", "來店前須知"),
 'why1': ("<strong>Opening hours:</strong> Monday, Wednesday–Friday and Sunday, 9:00am–5:00pm (closed Tuesdays &amp; Saturdays).",
          "<strong>營業時間：</strong>週一、週三至週五、週日，上午 9:00 – 下午 5:00（週二、週六公休）。"),
 'why2': ("<strong>Text or call ahead</strong> if you'd like to check how busy we are.",
          "想知道店裡忙不忙，可以先<strong>傳簡訊或打電話</strong>問我們。"),
 'why3': ("<strong>No vaccine records needed</strong> for a walk-in nail trim. (Full grooms require Rabies, Bordetella and Distemper vaccines.)",
          "walk-in 剪指甲<strong>不需要疫苗記錄</strong>。（完整美容需要狂犬病、犬舍咳和犬瘟熱疫苗。）"),
 'why4': ("<strong>Address:</strong> 1381 E Las Tunas Dr #11, San Gabriel, CA 91776.",
          "<strong>地址：</strong>1381 E Las Tunas Dr #11, San Gabriel, CA 91776。"),
 'faq_h': ("Common questions", "常見問題"),
 'faq1_q': ("Do I need an appointment for a nail trim?", "剪指甲需要預約嗎？"),
 'faq1_a': ("No — walk-ins are welcome during opening hours. You can text or call ahead to check how busy we are.",
            "不需要，營業時間內歡迎直接過來。也可以先傳簡訊或打電話問我們忙不忙。"),
 'faq2_q': ("How do I know my dog's nails are too long?", "怎麼知道狗狗的指甲太長了？"),
 'faq2_a': ("If you can hear the nails clicking on the floor, it's usually time for a trim.",
            "如果狗狗走路時聽得到指甲敲地板的聲音，通常就該剪了。"),
 'route_h': ("", ""), 'route_p': ("", ""), 'route_btn': ("", ""),
 'also_h': ("We welcome dogs from", "我們歡迎來自這些城市的狗狗"),
}

def nail_body():
    others = ''.join('<a href="/dog-grooming-%s" data-i18n="city_%s">%s</a>' % (s, s.replace('-', '_'), o['en']) for s, o in CITIES.items())
    html = body_template(others)
    html = re.sub(r'<section class="city-section">\s*<h2 data-i18n="route_h"></h2>.*?</section>\n', '', html, count=1, flags=re.S)
    html = html.replace('href="https://book.kokonipets.com/book" class="btn-book cta-book" target="_blank" rel="noopener" data-i18n="cta_book"',
                        'href="%s" class="cta-book" target="_blank" rel="noopener" data-i18n="cta_book"' % DIRECTIONS)
    return html


# ── Service page: Asian Fusion grooming ─────────────────────────────
ASIAN = {
 'meta_title': ("Asian Fusion Dog Grooming (Korean & Japanese-Style) | Kokoni, San Gabriel",
                "韓系、日系精緻造型狗狗美容 | KOKONI 寵物沙龍（聖蓋博）"),
 'meta_description': ("Asian Fusion dog grooming in San Gabriel: Korean and Japanese-style round faces and teddy bear cuts, hand-scissored by Wylie Shen's team at Kokoni Pet Salon. Prices from $110.",
                "聖蓋博 KOKONI 寵物沙龍的精緻造型（Asian Fusion）：韓系、日系圓臉與泰迪熊造型，由 Wylie Shen 團隊手工剪裁。價格 $110 起。"),
 'city_h1': ("Asian Fusion Dog Grooming in San Gabriel", "聖蓋博 韓系、日系精緻造型狗狗美容"),
 'city_sub': ("Korean and Japanese-style round faces, fluffy coats and teddy bear cuts, shaped by hand at Kokoni Pet Salon.",
              "韓系、日系的圓臉、蓬鬆毛量和泰迪熊造型，在 KOKONI 寵物沙龍以手工剪裁完成。"),
 'city_intro': ("Asian Fusion is our most detailed style. Instead of clipping the body short, we leave the coat longer and shape it with scissors, so your dog ends up with a soft, round face, rounded ears and an even, fluffy body. It's the look many people know from Korean and Japanese grooming salons.",
                "精緻造型是我們最講究細節的造型。我們不把身體的毛剃短，而是保留較長的毛，用剪刀一點一點修出形狀，讓狗狗有柔和的圓臉、圓耳朵，以及均勻蓬鬆的身形。這就是很多人在韓國、日本寵物美容店看到的樣子。"),
 'cta_book': ("Book an appointment", "立即預約"),
 'cta_call': ("Text or call (626) 621-4646", "簡訊或來電 (626) 621-4646"),
 'route_h': ("How we create the look", "我們怎麼做出這個造型"),
 'route_p': ("It starts in the bath. After a Hydra luxury shampoo and conditioner, we hand-dry and straighten the coat, much like a blow-out at a hair salon, to give it volume. Only a fluffed, even coat can be scissored into a truly round muzzle, face and ears. Because it's all done by hand, Asian Fusion takes longer than a standard haircut.",
             "一切從洗澡開始。用 Hydra 頂級洗毛精和護毛素洗完後，我們用手工吹乾、把毛吹直，就像在髮廊吹整頭髮一樣，讓毛有蓬度。只有蓬鬆均勻的毛，才能剪出真正圓潤的嘴邊、臉型和耳朵。因為全程手工，精緻造型需要的時間比一般剪毛長。"),
 'route_btn': ("Compare with our Simply Cute style →", "跟日常造型比較 →"),
 'svc_h': ("Asian Fusion prices", "精緻造型價格"),
 'svc1_t': ("Up to 15 lbs — $110", "15 磅以下 $110"),
 'svc1_p': ("16–30 lbs $130 · 31–50 lbs $190 · 51–70 lbs $240. Includes bath, hand blow-out, nail trim, ear cleaning and teeth brushing.",
            "16–30 磅 $130 · 31–50 磅 $190 · 51–70 磅 $240。包含洗澡、手工吹整、剪指甲、清耳朵和刷牙。"),
 'svc2_t': ("Doodles — from $130", "Doodle $130 起"),
 'svc2_p': ("16–30 lbs $170 · 31–50 lbs $240 · 51–70 lbs $290. Doodle coats need extra time and care.",
            "16–30 磅 $170 · 31–50 磅 $240 · 51–70 磅 $290。Doodle 的毛需要更多時間和照顧。"),
 'svc3_t': ("Over 70 lbs or matted?", "超過 70 磅或毛打結？"),
 'svc3_p': ("Please ask us first. Prices are a quote and can change with size, coat length and the style you choose.",
            "請先跟我們聯絡。價格僅供參考，會依體型、毛長和選擇的造型調整。"),
 'svc_link': ("See all services &amp; pricing →", "查看所有服務與價格 →"),
 'why_h': ("Who grooms your dog", "誰幫你的狗狗美容"),
 'why1': ("<strong>Wylie Shen</strong>, founder of Kokoni and Unicorn Pet Grooming, specializes in Japanese-style grooming, with a focus on precision, softness and balance.",
          "<strong>Wylie Shen</strong> 是 KOKONI 和 Unicorn Pet Grooming 的創辦人，專精日系美容，重視精準、柔和與比例。"),
 'why2': ("<strong>Trained at</strong> the Animal Behavior College and 4 Dog Grooming Academy, with animal rescue work since 2011.",
          "<strong>畢業於</strong> Animal Behavior College 和 4 Dog Grooming Academy，2011 年起投入動物救援。"),
 'why3': ("<strong>3rd place</strong> at the 2023 Groom Expo West Rescue Round-Up.",
          "<strong>2023 年 Groom Expo West Rescue Round-Up 第三名。</strong>"),
 'why4': ("<strong>One dog at a time.</strong> Long, detailed sessions are calmer when a groomer can focus on one dog.",
          "<strong>一次專心照顧一隻狗狗。</strong>時間較長的精緻造型，更需要美容師專心陪伴。"),
 'faq_h': ("Is Asian Fusion right for my dog?", "精緻造型適合我的狗狗嗎？"),
 'faq1_q': ("Can every dog have an Asian Fusion cut?", "每隻狗都可以做精緻造型嗎？"),
 'faq1_a': ("Not every coat or personality suits it. The style needs a longer coat and a dog that's comfortable with a longer session. For a first appointment, text us a photo and we'll tell you honestly whether Asian Fusion or our easy-care Simply Cute style is the better fit.",
            "不是每種毛質或個性都適合。這個造型需要較長的毛，狗狗也要能接受較長的美容時間。第一次預約前，歡迎傳照片給我們，我們會老實告訴你精緻造型還是好整理的日常造型比較適合。"),
 'faq2_q': ("How much upkeep does it need at home?", "在家需要多少照顧？"),
 'faq2_a': ("More than a short cut. A longer, fluffy coat needs regular brushing at home to stay tangle-free and keep its round shape between visits.",
            "比短毛造型多。較長、蓬鬆的毛需要在家定期梳理，才不會打結，也能在兩次美容之間保持圓潤的造型。"),
 'also_h': ("We welcome dogs from", "我們歡迎來自這些城市的狗狗"),
}

def asian_body():
    others = ''.join('<a href="/dog-grooming-%s" data-i18n="city_%s">%s</a>' % (s, s.replace('-', '_'), o['en']) for s, o in CITIES.items())
    html = body_template(others)
    html = html.replace('<a class="route-btn" href="%s"' % DIRECTIONS, '<img class="af-photo" src="bath-haircut-asian-fusion.avif" alt="Dog with a round Asian Fusion teddy bear face after grooming at Kokoni Pet Salon" />\n  <a class="route-btn" href="/compare-styles"', 1)
    html = html.replace('<a class="route-btn" href="/compare-styles" target="_blank" rel="noopener"', '<a class="route-btn" href="/compare-styles"', 1)
    return html

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

PAGES_OUT = [('dog-grooming-' + s, common(c), lambda s=s, c=c: body(s, c)) for s, c in CITIES.items()] + \
            [('dog-nail-trimming', NAIL, nail_body), ('asian-fusion-dog-grooming', ASIAN, asian_body)]

for name, texts, make_body in PAGES_OUT:
    url = 'https://www.kokonipets.com/' + name
    i18n = {k: v for k, v in base_i18n.items() if k.startswith(('nav_', 'footer_', 'info_', 'sister_'))}
    for k, (en, tw) in texts.items():
        i18n[k] = {'en': en, 'zh-TW': tw, 'zh-CN': S2.convert(tw)}
    for s, o in CITIES.items():
        i18n['city_' + s.replace('-', '_')] = {'en': o['en'], 'zh-TW': o['zh'] + ' ' + o['en'], 'zh-CN': S2.convert(o['zh']) + ' ' + o['en']}
    h = base[:start] + make_body() + base[end:]
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
    open(name + '.html', 'w', encoding='utf-8').write(h)
    print('wrote', name + '.html')
