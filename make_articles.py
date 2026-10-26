#!/usr/bin/env python3
"""Grooming-tips articles (and the /grooming-tips hub), written from Wylie's answers.
Builds <slug>.html from contact.html's header/footer. Then run build.py for zh-tw / zh-cn.
Needs: pip install opencc-python-reimplemented
"""
import re, json
import opencc
S2 = opencc.OpenCC('tw2sp')
BOOK = 'https://book.kokonipets.com/book'
BYLINE = ("By the Kokoni grooming team, led by Wylie Shen (12+ years of grooming experience)",
          "KOKONI 美容團隊撰寫，由擁有 12 年以上經驗的 Wylie Shen 帶領")

def ul(items):
    return '<ul class="why-list">' + ''.join('<li>%s</li>' % i for i in items) + '</ul>'

ARTICLES = [
 dict(slug='poodle-teddy-bichon-grooming-schedule',
  title=("How Often Should You Groom a Poodle, Teddy Bear Cut or Bichon? | Kokoni",
         "貴賓、泰迪、比熊多久剪一次毛？| KOKONI 寵物美容（聖蓋博）"),
  desc=("How often to groom Poodles, teddy bear cuts, Bichons, Maltese, Shih Tzus, Yorkies and Doodles, from the groomers at Kokoni Pet Salon in San Gabriel.",
        "貴賓、泰迪、比熊、瑪爾濟斯、西施、約克夏和 Doodle 多久要剪一次毛？聖蓋博 KOKONI 寵物美容師告訴你。"),
  h1=("How Often Should You Groom a Poodle, Teddy or Bichon?", "貴賓、泰迪、比熊多久要剪一次毛？"),
  sub=("Short answer: every 4–6 weeks for an easy-care cut, and every 4 weeks for a fluffy Asian Fusion teddy bear look.",
       "簡單來說：好整理的日常造型每 4–6 週一次，蓬鬆的精緻泰迪熊造型每 4 週一次。"),
  sections=[
   (("Poodles and teddy bear cuts", "貴賓與泰迪造型"),
    ("<p>For our easy-care <a href=\"/compare-styles\">Simply Cute</a> style, we recommend a groom every <strong>4–6 weeks</strong>. For the rounder, fluffier <a href=\"/asian-fusion-dog-grooming\">Asian Fusion</a> teddy bear look, come in every <strong>4 weeks</strong>. If you keep the coat 1 inch long or longer, every <strong>2–4 weeks</strong> works best.</p>",
     "<p>好整理的<a href=\"/compare-styles\">日常造型</a>，建議每 <strong>4–6 週</strong>美容一次。比較圓潤蓬鬆的<a href=\"/asian-fusion-dog-grooming\">精緻造型</a>（泰迪熊造型），建議每 <strong>4 週</strong>一次。如果毛留到 1 吋或更長，每 <strong>2–4 週</strong>一次最理想。</p>")),
   (("Bichons", "比熊"),
    ("<p>Bichons are on about the same schedule as Poodles and teddy bear cuts: every 4–6 weeks for a simple style, every 4 weeks for a fuller, rounded look.</p>",
     "<p>比熊的美容週期跟貴賓、泰迪差不多：簡單造型每 4–6 週一次，蓬鬆圓潤的造型每 4 週一次。</p>")),
   (("Maltese, Schnauzers, Shih Tzus, Yorkies and Doodles", "瑪爾濟斯、雪納瑞、西施、約克夏和 Doodle"),
    ("<p>Straight-coated breeds like Maltese, Schnauzers, Shih Tzus and Yorkies also do best every <strong>4–6 weeks</strong>. You can stretch it to <strong>8 weeks at most</strong>; after that, the coat almost always tangles and gets dirty. Doodles are bigger dogs with a lot of coat, so we recommend every <strong>4 weeks</strong>.</p>",
     "<p>瑪爾濟斯、雪納瑞、西施、約克夏這類直毛的狗，也是每 <strong>4–6 週</strong>一次最好，<strong>最多可以延到 8 週</strong>，超過的話幾乎一定會打結、變得很髒。Doodle 體型大、毛量多，建議每 <strong>4 週</strong>一次。</p>")),
   (("What happens if you wait too long", "間隔太久沒剪會怎樣"),
    (ul(["The coat starts to smell and gets dirty faster.", "Tangles turn into mats, and heavy mats often mean the only safe option is a short shave (<a href=\"/matted-dog-hair\">here's why</a>).", "Trapped dirt and moisture can lead to skin problems."]),
     ul(["毛會開始有味道，也更容易髒。", "小結變成大毛結，嚴重的話最安全的做法往往只能剃短（<a href=\"/matted-dog-hair\">原因在這裡</a>）。", "卡在毛裡的髒污和濕氣可能引起皮膚問題。"]))),
   (("Brushing at home between visits", "兩次美容之間，在家怎麼照顧"),
    ("<p>Brushing every day is ideal, and at least <strong>3 times a week</strong>. Use a <strong>slicker brush</strong> first to open up the coat, then follow with a <strong>metal comb</strong> to make sure it runs through smoothly all the way to the skin.</p>",
     "<p>最理想是每天梳毛，至少<strong>一週 3 次</strong>。先用<strong>針梳（slicker brush）</strong>把毛梳開，再用<strong>排梳（金屬直梳）</strong>梳順，確認可以一路梳到皮膚。</p>")),
  ],
  faq=[(("Is it OK to wait 8 weeks?", "可以等到 8 週再剪嗎？"),
        ("For straight-coated breeds, 8 weeks is the maximum. For Asian Fusion styles, we recommend no more than 6 weeks, or the shape and coat become hard to maintain.",
         "直毛品種最多 8 週。精緻造型建議不要超過 6 週，否則造型和毛況會很難維持。"))]),

 dict(slug='puppy-first-grooming',
  title=("Your Puppy's First Grooming: Age, Vaccines & How to Prepare | Kokoni",
         "幼犬第一次美容：幾個月、疫苗、怎麼準備 | KOKONI 寵物美容（聖蓋博）"),
  desc=("When can a puppy get groomed, which vaccines are needed, what happens at the first visit and how to prepare at home. Tips from Kokoni Pet Salon in San Gabriel.",
        "幼犬幾個月可以美容？需要哪些疫苗？第一次美容做什麼、在家怎麼準備？聖蓋博 KOKONI 寵物美容師的建議。"),
  h1=("Your Puppy's First Grooming: What to Know", "幼犬第一次美容：你需要知道的事"),
  sub=("Most puppies can have their first full groom at around 4 months old, once their vaccines are complete.",
       "大部分幼犬在大約 4 個月大、打完疫苗後，就可以第一次完整美容。"),
  sections=[
   (("When can a puppy get groomed?", "幼犬幾個月可以美容？"),
    ("<p>Once your puppy has finished the <strong>Distemper series (2 shots)</strong> and the <strong>Rabies</strong> shot, they're ready for a first groom. For most puppies, that's at around <strong>4 months old</strong>.</p>",
     "<p>幼犬打完<strong>犬瘟熱疫苗（2 劑）</strong>和<strong>狂犬病疫苗</strong>後，就可以開始第一次美容。大部分幼犬大約是 <strong>4 個月大</strong>的時候。</p>")),
   (("What to bring", "要帶什麼"),
    ("<p>Please bring vaccine records showing the <strong>expiration dates</strong>. A paper copy or a photo on your phone both work. Those two vaccines, Distemper and Rabies, are all we require.</p>",
     "<p>請帶顯示<strong>疫苗到期日</strong>的記錄，紙本或手機照片都可以。我們只需要犬瘟熱和狂犬病這兩種疫苗。</p>")),
   (("Our tip: start with a short visit", "我們的建議：先來一次短短的拜訪"),
    ("<p>Before the first full groom, bring your puppy in for a quick <a href=\"/dog-nail-trimming\">nail trim</a> and a light brush. It's short, low-stress, and lets your puppy meet the groomer and get to know the salon first.</p>",
     "<p>第一次完整美容之前，可以先帶幼犬來店裡<a href=\"/dog-nail-trimming\">剪指甲</a>、簡單梳毛。時間短、壓力小，讓狗狗先認識美容師和環境。</p>")),
   (("What happens at the first groom", "第一次美容會做什麼"),
    ("<p>A full groom includes nail grinding, ear cleaning, teeth brushing, gland expression, paw pad trim, sanitary trim, a bath and a haircut. It usually takes about <strong>2 hours</strong>. Pricing is the same as our regular grooming.</p>",
     "<p>完整美容包括磨指甲、清耳朵、刷牙、擠肛門腺、修腳底毛、衛生修剪、洗澡和剪毛，大約需要 <strong>2 小時</strong>。價格與一般美容相同。</p>")),
   (("How to prepare at home", "在家可以怎麼準備"),
    (ul(["Turn on a hair dryer near your puppy so they get used to the air and the sound.", "Brush them gently, even if the coat is still short.", "Touch their face, chin, paws and legs.", "Give a treat with every step, so each one feels like a good thing."]),
     ul(["在狗狗旁邊開吹風機，讓牠習慣吹風的感覺和聲音。", "就算毛還短，也輕輕幫牠梳毛。", "常常摸摸牠的臉、下巴、腳掌和四肢。", "每一步都配合零食，讓狗狗覺得這些都是好事。"]))),
   (("Common first-visit worries, and how we handle them", "第一次來常見的狀況，我們怎麼處理"),
    (ul(["<strong>Scared of water or the dryer:</strong> we slow down and put cotton in the ears to soften the noise.", "<strong>Won't stand on the table:</strong> we gently help them up, never forcing it.", "<strong>Nervous about clippers or scissors:</strong> we let them see and sniff the tools first, then introduce the touch slowly."]),
     ul(["<strong>怕水或吹風機：</strong>我們會放慢動作，在耳朵裡塞棉花減少噪音。", "<strong>在美容桌上不敢站：</strong>慢慢、溫柔地幫牠站起來，絕不勉強。", "<strong>怕電剪或剪刀的聲音和觸碰：</strong>先讓牠看看、聞聞工具，再慢慢用工具輕碰，讓牠習慣。"]))),
  ],
  faq=[(("Is there a special puppy price?", "幼犬第一次美容有特別價格嗎？"),
        ("No, a puppy's first groom is priced the same as a regular groom. A walk-in nail trim beforehand is $15.",
         "沒有，幼犬第一次美容和一般美容價格相同。事先來剪指甲（免預約）是 $15。"))]),

 dict(slug='matted-dog-hair',
  title=("Matted Dog Hair: What to Do, and Why Shaving Is Sometimes Best | Kokoni",
         "狗狗毛打結怎麼辦？為什麼有時候只能剃短 | KOKONI 寵物美容（聖蓋博）"),
  desc=("Where mats form, when they can be brushed out, why de-matting can hurt and when a short shave is kinder. De-matting prices and prevention tips from Kokoni Pet Salon.",
        "毛結常在哪裡出現、什麼時候可以梳開、為什麼硬梳會痛、什麼時候剃短反而比較好。KOKONI 寵物沙龍的開結價格與預防建議。"),
  h1=("Matted Dog Hair: What to Do, and Why Shaving Is Sometimes Kinder", "狗狗毛打結怎麼辦？為什麼有時候剃短反而比較好"),
  sub=("Mild mats can often be brushed out. Mats that sit tight against the skin, or cover the whole body, are safer and kinder to shave.",
       "輕微的毛結通常可以梳開；緊貼皮膚、或全身都是的毛結，剃掉對狗狗比較安全，也比較不痛。"),
  sections=[
   (("Where mats usually form", "毛結通常出現在哪裡"),
    ("<p>The most common spots are the <strong>legs</strong>, <strong>behind the ears</strong> and under the <strong>chin</strong>: places that rub, get wet or are easy to miss when brushing.</p>",
     "<p>最常見的位置是<strong>四肢</strong>、<strong>耳朵後面</strong>和<strong>下巴</strong>，這些都是容易摩擦、弄濕或刷毛時容易漏掉的地方。</p>")),
   (("Brush out or shave? How we decide", "梳開還是剃掉？我們怎麼判斷"),
    ("<p>We look at how close the mats are to the skin and whether they've joined together. If they're <strong>pressed flat against the skin</strong>, <strong>connected into one mat</strong>, or <strong>spread all over the body</strong>, shaving is the safest option.</p>",
     "<p>我們看毛結有多貼近皮膚，以及是否連成一片。如果毛結<strong>完全貼著皮膚</strong>、<strong>連成一大片</strong>，或<strong>全身都有</strong>，剃掉是最安全的做法。</p>")),
   (("Why forcing mats out hurts", "為什麼硬梳會讓狗狗受傷"),
    ("<p>A mat is hair tangled tightly together. Pulling it apart tugs on the skin, which is painful. Repeated pulling can irritate the skin or cause inflammation, and the ongoing soreness can leave a dog feeling down after going home, sometimes even refusing to eat.</p>",
     "<p>毛結是毛髮緊緊糾纏在一起形成的，梳開時會拉扯皮膚，狗狗會覺得痛。不斷拉扯可能讓皮膚過敏或發炎，持續的疼痛也可能讓狗狗回家後情緒低落，甚至不吃飯。</p>")),
   (("How we talk with you about it", "我們會怎麼跟你溝通"),
    ("<p>If the mats are severe, we'll explain honestly that they can't be fully worked out, and that trying would be very uncomfortable for your dog. If the mats can be removed, we'll let you know it will pull on the skin, and that if your dog reacts strongly, we'll stop rather than push through.</p>",
     "<p>如果毛結太嚴重，我們會老實告訴你，勉強梳也無法完全解開，而且狗狗會非常不舒服。如果毛結可以解開，我們會先說明過程會拉扯皮膚；如果狗狗反應太大，我們會停下來，不會硬做。</p>")),
   (("De-matting prices", "開結價格"),
    (ul(["<strong>$20:</strong> a few mats on the head or legs", "<strong>$40:</strong> mats on both the head and legs", "<strong>$60:</strong> mats all over the body"]) + "<p>De-matting is added to a bath or grooming package.</p>",
     ul(["<strong>$20：</strong>頭或四肢少量毛結", "<strong>$40：</strong>頭和四肢都有毛結", "<strong>$60：</strong>全身都有毛結"]) + "<p>開結需搭配洗澡或美容方案。</p>")),
   (("How to prevent mats", "怎麼預防打結"),
    (ul(["Brush as often as you can, especially after the dog park or playing with other dogs.", "If you bathe your dog at home, dry and brush them <strong>completely</strong>. Damp coats mat fast.", "Keep to a regular grooming schedule (<a href=\"/poodle-teddy-bichon-grooming-schedule\">how often?</a>)."]),
     ul(["盡量多梳毛，特別是去完狗公園、跟其他狗玩之後。", "如果在家幫狗洗澡，一定要<strong>完全</strong>吹乾、梳開，半乾的毛最容易打結。", "固定時間來美容（<a href=\"/poodle-teddy-bichon-grooming-schedule\">多久一次？</a>）。"]))),
  ],
  faq=[(("Will the coat grow back after a shave?", "剃掉之後毛會長回來嗎？"),
        ("For most single-coated breeds like Poodles, Bichons and Maltese, yes, and starting fresh with regular brushing is often the easiest path. Double-coated breeds are different; see our article on shaving double-coated dogs.",
         "大部分單層毛品種（貴賓、比熊、瑪爾濟斯等）會長回來，剃短後配合定期梳毛，往往是最輕鬆的重新開始。雙層毛品種則不同，請看我們關於雙層毛剃毛的文章。"))]),

 dict(slug='shaving-double-coated-dogs',
  title=("Should You Shave a Double-Coated Dog in Summer? | Kokoni Pet Salon",
         "雙層毛的狗（博美、柴犬、哈士奇）夏天可以剃毛嗎？| KOKONI 寵物美容"),
  desc=("Why groomers avoid shaving huskies, Pomeranians, Samoyeds and Corgis, what to do instead to keep them cool, and when shaving is the right call. From Kokoni Pet Salon in San Gabriel.",
        "為什麼不建議幫哈士奇、博美、薩摩耶、柯基剃毛？夏天怎麼讓牠們涼快？什麼情況才需要剃？聖蓋博 KOKONI 寵物沙龍的說明。"),
  h1=("Should You Shave a Double-Coated Dog in Summer?", "雙層毛的狗夏天可以剃毛嗎？"),
  sub=("Usually not. Shaving can damage a double coat so it grows back poorly, or not at all. A trim and a de-shed works better.",
       "通常不建議。剃毛可能傷害雙層毛，導致毛長不好甚至長不回來。修短加上除廢毛效果更好。"),
  sections=[
   (("Which dogs have a double coat?", "哪些狗是雙層毛？"),
    ("<p>Common double-coated breeds include <strong>Huskies, Pomeranians, Alaskan Malamutes, Samoyeds and Corgis</strong>. They have a soft undercoat beneath a longer outer coat.</p>",
     "<p>常見的雙層毛品種有<strong>哈士奇、博美、阿拉斯加、薩摩耶和柯基</strong>。牠們在較長的外層毛下面，還有一層柔軟的底毛。</p>")),
   (("Why we generally don't shave them", "為什麼我們基本上不剃"),
    (ul(["The coat may <strong>not grow back</strong> properly, or at all.", "Bare skin is exposed to <strong>sunburn</strong>.", "Shaving can damage the coat and seriously change how your dog looks for a long time."]),
     ul(["毛可能<strong>長不回來</strong>，或長得不正常。", "皮膚直接暴露，容易<strong>曬傷</strong>。", "剃毛可能損傷毛髮，長時間嚴重影響外觀。"]))),
   (("What to do instead in hot weather", "天氣熱時，可以怎麼做"),
    ("<p>We <strong>trim the coat shorter without shaving it down to the skin</strong>, and add <strong>de-shedding</strong> ($15–$30) to clear out the loose undercoat. That lets air move through the coat while keeping its protection.</p>",
     "<p>我們會<strong>把毛修短，但不剃到皮膚</strong>，再加上<strong>除廢毛（De-shedding）</strong>（$15–$30），清掉鬆脫的底毛，讓空氣能在毛裡流通，同時保留毛的保護作用。</p>")),
   (("When shaving is the right call", "什麼情況下會剃"),
    ("<p>We only shave a double-coated dog when it's the safest option:</p>" + ul(["The dog has <strong>severe matting</strong>.", "The dog <strong>bites or reacts very strongly</strong> to brushing and grooming."]) + "<p>Before we shave, we'll explain that it may damage the coat and it might not grow back, and we'll only go ahead with your agreement. If neither situation applies, we'll respectfully decline to shave.</p>",
     "<p>只有在剃毛是最安全的選擇時，我們才會幫雙層毛的狗剃毛：</p>" + ul(["狗狗有<strong>嚴重毛結</strong>。", "狗狗對梳毛和美容<strong>會咬人或反應非常激烈</strong>。"]) + "<p>剃之前，我們會先說明剃毛可能損傷毛髮、可能長不回來，取得你的同意後才會進行。如果都不是以上情況，我們會婉拒剃毛。</p>")),
  ],
  faq=[(("Does shaving keep a double-coated dog cooler?", "剃毛會讓雙層毛的狗比較涼快嗎？"),
        ("Not really. A healthy, de-shedded double coat helps protect against heat and sun. Removing the loose undercoat does more for comfort than shaving.",
         "其實不會。健康、除過廢毛的雙層毛反而能幫忙隔熱、防曬。清掉鬆脫的底毛，比剃毛更能讓狗狗舒服。"))]),
]

HUB = dict(slug='grooming-tips',
  title=("Dog Grooming Tips from Our Groomers | Kokoni Pet Salon, San Gabriel", "狗狗美容小知識 | KOKONI 寵物沙龍（聖蓋博）"),
  desc=("Practical dog grooming advice from the Kokoni grooming team in San Gabriel: grooming schedules, puppy's first groom, matted hair and double-coated dogs.",
        "聖蓋博 KOKONI 美容團隊的實用狗狗美容知識：多久剪一次毛、幼犬第一次美容、毛打結、雙層毛剃毛。"),
  h1=("Grooming Tips from Our Groomers", "美容師的狗狗美容小知識"),
  sub=("Straight answers to the questions we hear most at the salon.", "我們在店裡最常被問到的問題，直接回答給你。"))

CSS = """
    /* ── Articles ── */
    .city-hero { background: #D8EBFD; padding: 56px 80px 48px; text-align: center; }
    .city-hero h1 { font-family: 'DM Serif Display', serif; color: #1C4F95; font-size: 2.3rem; font-weight: 400; line-height: 1.2; margin-bottom: 14px; }
    .city-hero .city-sub { color: #1C4F95; font-weight: 600; font-size: 1.05rem; max-width: 720px; margin: 0 auto 12px; line-height: 1.6; }
    .city-hero .byline { font-size: 0.85rem; color: #555; }
    .city-cta { display: flex; gap: 14px; justify-content: center; flex-wrap: wrap; margin-top: 24px; }
    .city-cta a { text-decoration: none; font-weight: 700; border-radius: 30px; padding: 12px 26px; font-size: 0.95rem; }
    .city-cta .cta-book { background: #F07840; color: #fff; }
    .city-cta .cta-call { background: #fff; color: #1C4F95; border: 2px solid #1C4F95; }
    .article { max-width: 820px; margin: 0 auto; padding: 24px 24px 48px; }
    .article h2 { font-family: 'DM Serif Display', serif; color: #1C4F95; font-size: 1.6rem; font-weight: 400; margin: 36px 0 12px; }
    .article p, .article li { line-height: 1.8; }
    .article p { margin-bottom: 10px; }
    .article a { color: #1C4F95; font-weight: 600; }
    .why-list { list-style: none; display: grid; gap: 10px; margin: 8px 0 12px; }
    .why-list li { padding-left: 26px; position: relative; }
    .why-list li::before { content: '✓'; position: absolute; left: 0; color: #46BFBF; font-weight: 800; }
    .city-faq dt { font-weight: 700; color: #1C4F95; margin-top: 14px; }
    .city-faq dd { margin: 6px 0 0; line-height: 1.8; }
    .tips-cards { display: grid; grid-template-columns: repeat(2, 1fr); gap: 18px; margin-top: 12px; }
    .tips-cards a { display: block; background: #EDF6FB; border-radius: 16px; padding: 22px; text-decoration: none; }
    .tips-cards h3 { color: #1C4F95; font-size: 1.1rem; margin-bottom: 6px; }
    .tips-cards p { color: #2c2c2c; font-weight: 400; margin: 0; }
    .also-links { display: flex; flex-wrap: wrap; gap: 10px; }
    .also-links a { background: #fff; border: 1.5px solid #1C4F95; color: #1C4F95; border-radius: 20px; padding: 6px 16px; text-decoration: none; font-weight: 600; font-size: 0.9rem; }
    @media (max-width: 900px) {
      .city-hero { padding: 40px 24px 36px; }
      .city-hero h1 { font-size: 1.8rem; }
      .tips-cards { grid-template-columns: 1fr; }
    }
"""

def tw(x): return x  # zh-TW as written
def build_page(slug, title, desc, i18n_extra, body_html):
    base = open('contact.html', encoding='utf-8').read()
    base_i18n = json.loads(re.search(r'const I18N = (\{.*?\n\});', base, re.S).group(1))
    start = base.index('<!-- ══════════════════════════════\n     WELCOME STRIP')
    end = base.index('<!-- ══════════════════════════════\n     INFO STRIP')
    i18n = {k: v for k, v in base_i18n.items() if k.startswith(('nav_', 'footer_', 'info_', 'sister_'))}
    for k, (en, zh) in i18n_extra.items():
        i18n[k] = {'en': en, 'zh-TW': zh, 'zh-CN': S2.convert(zh)}
    h = base[:start] + body_html + base[end:]
    h = h.replace('<a href="/contact" class="active" data-i18n="nav_contact">', '<a href="/contact" data-i18n="nav_contact">')
    url = 'https://www.kokonipets.com/' + slug
    h = re.sub(r'<meta name="description" content="[^"]*"', '<meta name="description" content="%s"' % desc, h)
    h = re.sub(r'<link rel="canonical" href="[^"]*"', '<link rel="canonical" href="%s"' % url, h)
    h = re.sub(r'<meta property="og:url" content="[^"]*"', '<meta property="og:url" content="%s"' % url, h)
    h = re.sub(r'<meta property="og:type" content="[^"]*"', '<meta property="og:type" content="article"', h)
    for p in ('og:title', 'og:description'):
        h = re.sub(r'<meta property="%s" content="[^"]*"' % p, '<meta property="%s" content="%s"' % (p, title if 'title' in p else desc), h)
    for p in ('twitter:title', 'twitter:description'):
        h = re.sub(r'<meta name="%s" content="[^"]*"' % p, '<meta name="%s" content="%s"' % (p, title if 'title' in p else desc), h)
    h = re.sub(r'<title>[^<]*</title>', '<title>%s</title>' % title, h)
    h = h.replace('    </style>', CSS + '    </style>', 1)
    h = re.sub(r'const I18N = \{.*?\n\};', lambda m: 'const I18N = ' + json.dumps(i18n, ensure_ascii=False, indent=2) + ';', h, count=1, flags=re.S)
    open(slug + '.html', 'w', encoding='utf-8').write(h)
    print('wrote', slug + '.html')

def el(tag, key, en, attrs=''):
    return '<%s%s data-i18n="%s">%s</%s>' % (tag, attrs, key, en, tag)

def hero(t, key_pre=''):
    return ('<section class="city-hero">\n  ' + el('h1', 'a_h1', t['h1'][0]) + '\n  ' + el('p', 'a_sub', t['sub'][0], ' class="city-sub"') +
            ('\n  ' + el('p', 'a_by', BYLINE[0], ' class="byline"') if t is not HUB else '') +
            '\n  <div class="city-cta">' + el('a', 'cta_book', 'Book an appointment', ' href="%s" class="btn-book cta-book" target="_blank" rel="noopener"' % BOOK) +
            el('a', 'cta_call', 'Text or call (626) 621-4646', ' href="tel:6266214646" class="cta-call"') + '</div>\n</section>\n')

COMMON = {'cta_book': ("Book an appointment", "立即預約"), 'cta_call': ("Text or call (626) 621-4646", "簡訊或來電 (626) 621-4646"),
          'a_by': BYLINE, 'more_h': ("More grooming tips", "更多美容小知識"), 'faq_h': ("Quick answer", "快速問答"),
          'svc_more': ("See our services &amp; prices", "查看服務與價格")}

for a in ARTICLES:
    tx = dict(COMMON); tx['a_h1'] = a['h1']; tx['a_sub'] = a['sub']; tx['meta_title'] = a['title']; tx['meta_description'] = a['desc']
    body = hero(a) + '<article class="article">\n'
    for i, ((hen, hzh), (ben, bzh)) in enumerate(a['sections']):
        tx['s%d_h' % i] = (hen, hzh); tx['s%d_b' % i] = (ben, bzh)
        body += '  ' + el('h2', 's%d_h' % i, hen) + '\n  ' + el('div', 's%d_b' % i, ben) + '\n'
    body += '  ' + el('h2', 'faq_h', COMMON['faq_h'][0]) + '\n  <dl class="city-faq">'
    for j, ((qen, qzh), (aen, azh)) in enumerate(a['faq']):
        tx['f%d_q' % j] = (qen, qzh); tx['f%d_a' % j] = (aen, azh)
        body += el('dt', 'f%d_q' % j, qen) + el('dd', 'f%d_a' % j, aen)
    body += '</dl>\n  ' + el('h2', 'more_h', COMMON['more_h'][0]) + '\n  <div class="also-links">'
    for b in ARTICLES:
        if b is a: continue
        k = 'l_' + b['slug'].replace('-', '_'); tx[k] = b['h1']
        body += el('a', k, b['h1'][0], ' href="/%s"' % b['slug'])
    body += el('a', 'svc_more', COMMON['svc_more'][0], ' href="/services"') + '</div>\n</article>\n\n'
    build_page(a['slug'], a['title'][0], a['desc'][0], tx, body)

# hub
tx = dict(COMMON); tx['a_h1'] = HUB['h1']; tx['a_sub'] = HUB['sub']; tx['meta_title'] = HUB['title']; tx['meta_description'] = HUB['desc']
body = hero(HUB) + '<article class="article">\n  <div class="tips-cards">'
for b in ARTICLES:
    k = 'c_' + b['slug'].replace('-', '_')
    tx[k + '_t'] = b['h1']; tx[k + '_p'] = b['sub']
    body += '<a href="/%s">%s%s</a>' % (b['slug'], el('h3', k + '_t', b['h1'][0]), el('p', k + '_p', b['sub'][0]))
body += '</div>\n</article>\n\n'
build_page(HUB['slug'], HUB['title'][0], HUB['desc'][0], tx, body)

