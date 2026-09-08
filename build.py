# -*- coding: utf-8 -*-
"""בונה את עמודי האתר מתבנית משותפת + תוכן לכל עמוד."""
import os, re

NAV = [
    ("index.html", "עמוד הבית", None),
    (None, "השירותים שלנו", [
        ("laser.html", "הסרת שיער בלייזר"),
        ("skin-tags.html", "הסרת סרחי עור"),
        ("facials.html", "טיפולי פנים"),
        ("treatments.html", "טיפולים נלווים"),
    ]),
    ("about.html", "אודות", None),
    ("testimonials.html", "המלצות", None),
    ("faq.html", "שאלות ותשובות", None),
    ("gallery.html", "גלריה", None),
    ("contact.html", "צור קשר", None),
]

WA    = "https://wa.me/972549462663"
PHONE = "054-9462663"
TEL   = "tel:+972549462663"
MAIL  = "Revital.kaily@gmail.com"
FB    = "https://www.facebook.com/revital1994/?locale=he_IL"

def nav_html(cur):
    out = []
    for href, label, kids in NAV:
        if kids:
            out.append('<div class="drop"><button aria-expanded="false">%s <span aria-hidden="true">⌄</span></button><div class="drop-m">%s</div></div>'
                       % (label, "".join('<a href="%s">%s</a>' % k for k in kids)))
        else:
            cu = ' aria-current="page"' if href == cur else ''
            out.append('<a href="%s"%s>%s</a>' % (href, cu, label))
    return "\n      ".join(out)

def mnav_html():
    out = []
    for href, label, kids in NAV:
        if kids:
            out.append('<a href="laser.html">%s</a>' % label)
            out += ['<a class="sub" href="%s">%s</a>' % k for k in kids]
        else:
            out.append('<a href="%s">%s</a>' % (href, label))
    return "\n    ".join(out)

FOOTER = """<footer class="ftr">
  <div class="ftr-logo">
    <img src="assets/logo.png" alt="רויטל קיילי — קליניקה לאסתטיקה">
    <p style="margin:0;max-width:34ch">קליניקת בוטיק להסרת שיער בלייזר וטיפולי אסתטיקה בגבעת שמואל. 12 שנות ניסיון, מכשור InMode ויחס אישי.</p>
  </div>
  <div><strong>טיפולים</strong>
    <a href="laser.html">הסרת שיער בלייזר</a><a href="skin-tags.html">הסרת סרחי עור</a>
    <a href="facials.html">טיפולי פנים</a><a href="treatments.html">טיפולים נלווים</a></div>
  <div><strong>הקליניקה</strong>
    <a href="about.html">אודות רויטל</a><a href="testimonials.html">המלצות</a>
    <a href="gallery.html">גלריה</a><a href="faq.html">שאלות ותשובות</a></div>
  <div><strong>דברי איתי</strong>
    <a href="%(tel)s">%(phone)s</a>
    <a href="%(wa)s">וואטסאפ</a>
    <a href="mailto:%(mail)s">%(mail)s</a>
    <span>גבעת שמואל</span><span>א׳–ה׳ 09:00–20:00 · ו׳ 09:00–13:00</span>
    <a href="%(fb)s" target="_blank" rel="noopener">פייסבוק</a></div>
  <div class="ftr-btm">
    <span>© 2026 רויטל קיילי. כל הזכויות שמורות.</span>
    <span><a href="accessibility.html">נגישות</a> · <a href="privacy.html">מדיניות פרטיות</a> · <a href="terms.html">תנאי שימוש</a></span>
  </div>
</footer>""" % {"wa": WA, "tel": TEL, "phone": PHONE, "mail": MAIL, "fb": FB}

BOT = """<div class="ov" id="ov" role="dialog" aria-modal="true" aria-label="בדיקת התאמה">
  <div class="bot">
    <button class="bot-x" aria-label="סגירה">✕</button>
    <img class="bot-logo" src="assets/logo.png" alt="רויטל קיילי">
    <div class="bar"><i style="width:0"></i></div>
    <div id="bot-body"></div>
  </div>
</div>
<a class="wa-float" href="%(wa)s" aria-label="וואטסאפ">✆</a>
<div class="mbar">
  <a href="%(wa)s">וואטסאפ</a><a href="%(tel)s">חייגי</a><a href="contact.html">טסט חינם</a>
</div>""" % {"wa": WA, "tel": TEL}

SHELL = """<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<link rel="icon" href="assets/logo.png" type="image/png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,300;1,400;1,600&family=Assistant:wght@300;400;600&display=swap">
<link rel="stylesheet" href="assets/site.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"HealthAndBeautyBusiness",
 "name":"רויטל קיילי — קליניקה לאסתטיקה",
 "description":"קליניקת בוטיק להסרת שיער בלייזר וטיפולי אסתטיקה בגבעת שמואל",
 "telephone":"+972-54-946-2663",
 "email":"Revital.kaily@gmail.com",
 "address":{{"@type":"PostalAddress","addressLocality":"גבעת שמואל","addressCountry":"IL"}},
 "areaServed":"גבעת שמואל והסביבה",
 "sameAs":["https://www.facebook.com/revital1994/"],
 "openingHoursSpecification":[
   {{"@type":"OpeningHoursSpecification","dayOfWeek":["Sunday","Monday","Tuesday","Wednesday","Thursday"],"opens":"09:00","closes":"20:00"}},
   {{"@type":"OpeningHoursSpecification","dayOfWeek":"Friday","opens":"09:00","closes":"13:00"}}],
 "makesOffer":[
   {{"@type":"Offer","itemOffered":{{"@type":"Service","name":"הסרת שיער בלייזר"}}}},
   {{"@type":"Offer","itemOffered":{{"@type":"Service","name":"הסרת סרחי עור"}}}},
   {{"@type":"Offer","itemOffered":{{"@type":"Service","name":"טיפולי פנים"}}}},
   {{"@type":"Offer","itemOffered":{{"@type":"Service","name":"טיפולי פלזמה וחידוש עור"}}}}]}}
</script>
</head>
<body class="{body_class}">
<div class="beam" aria-hidden="true"><i></i></div>

<header class="hdr">
  <a class="logo" href="index.html" aria-label="רויטל קיילי — לעמוד הבית"><img src="assets/logo.png" alt="רויטל קיילי — קליניקה לאסתטיקה"></a>
  <nav class="nav" aria-label="ניווט ראשי">
      {nav}
  </nav>
  <a class="btn" href="contact.html"><span>לטסט אבחון חינם</span><span class="arw">←</span></a>
  <button class="burger" aria-expanded="false" aria-controls="mnav" aria-label="פתיחת תפריט"><span></span><span></span></button>
</header>

<nav class="mnav" id="mnav" aria-label="ניווט מובייל">
    {mnav}
</nav>

<main>
{content}
</main>

{footer}
{bot}
<script src="assets/site.js"></script>
</body>
</html>
"""

def ph(label, note=""):
    return '<div class="ph"><b>%s</b>%s</div>' % (label, '<small>%s</small>' % note if note else "")

def figure(src, alt, label, note="", cls="frame"):
    """תמונה אמיתית אם קיימת, אחרת פלייסהולדר."""
    if src and os.path.exists(src):
        return '<div class="%s"><img src="%s" alt="%s" fetchpriority="high"></div>' % (cls, src, alt)
    return '<div class="%s">%s</div>' % (cls, ph(label, note))

def write(name, title, desc, content):
    html = SHELL.format(title=title, desc=desc, nav=nav_html(name), mnav=mnav_html(),
                        content=content, footer=FOOTER, bot=BOT,
                        body_class="has-hero" if "sc-wrap" in content else "no-hero")
    open(name, "w", encoding="utf-8").write(html)
    print("  ", name, len(html)//1024, "KB")

# ===================== עמוד הבית =====================
HOME = """
<div class="sc-wrap">
<section class="sc" aria-label="הקליניקה במבט אחד">
  <div class="sc-half sc-half-r">
    %(sc_r)s
  </div>
  <div class="sc-half sc-half-l">
    %(sc_l)s
  </div>

  <div class="sc-mid">
    <p class="eyebrow">קליניקת בוטיק · גבעת שמואל</p>
    <h1>תראי בעצמך <em class="serif-it">שזה עובד</em> לפני שאת מתחייבת.</h1>
    <div class="sc-ring" aria-hidden="true"></div>
    <div class="sc-card">%(sc_c)s</div>
    <div class="sc-cta">
      <a class="btn btn-light" href="contact.html"><span>לטסט אבחון חינם</span><span class="arw">←</span></a>
      <button class="btn btn-ghost open-bot"><span>בדקי אם זה מתאים לך</span><span class="arw">←</span></button>
    </div>
  </div>

  <div class="sc-nav">
    <div class="sc-dots" role="tablist" aria-label="מעבר בין תצוגות">
      <button aria-current="true" aria-label="תצוגה 1"></button>
      <button aria-current="false" aria-label="תצוגה 2"></button>
      <button aria-current="false" aria-label="תצוגה 3"></button>
    </div>
    <span class="sc-count">01 / 03</span>
  </div>
  <div class="sc-hint" aria-hidden="true">גלי להחלפה <span>↓</span></div>
</section>
</div>

<div class="marq" aria-hidden="true"><div class="marq-t">
  <span>InMode Optimas</span><span>טסט אבחון ללא עלות</span><span>12 שנות ניסיון</span><span>יחס אישי</span>
  <span>גבעת שמואל</span><span>לנשים ולגברים</span>
  <span>InMode Optimas</span><span>טסט אבחון ללא עלות</span><span>12 שנות ניסיון</span><span>יחס אישי</span>
  <span>גבעת שמואל</span><span>לנשים ולגברים</span>
</div></div>

<section class="pillars">
  <article class="rv"><b>12</b><strong>שנות ניסיון</strong><p>ידע מקצועי שנבנה מטיפול לטיפול, לא מקורס.</p></article>
  <article class="rv rv-d1"><b>◈</b><strong>מכשור InMode</strong><p>מכשיר קליני מהמובילים בעולם — לא לייזר ביתי.</p></article>
  <article class="rv rv-d2"><b>♡</b><strong>רויטל איתך</strong><p>אותה מטפלת מהטסט הראשון ועד הטיפול האחרון.</p></article>
  <article class="rv rv-d3"><b>✓</b><strong>הוכחה לפני התחייבות</strong><p>רואות שזה עובד לפני שמשלמות שקל.</p></article>
</section>

<section class="section wrap" id="services">
  <div class="rv" style="max-width:680px;margin-bottom:clamp(44px,5vw,74px)">
    <p class="eyebrow">כל מה שהעור שלך צריך</p>
    <h2>לא עוד תפריט טיפולים.<br><em class="serif-it">מסלול שמתאים לך.</em></h2>
    <p class="lead" style="margin-top:20px">בחרי את מה שמעסיק אותך עכשיו. כל טיפול מתחיל באבחון והתאמה אישית — ולא בחבילה שנמכרת לכולן.</p>
  </div>
  <div class="svc">
    <div class="svc-list rv" role="tablist" aria-label="סוגי טיפולים">
      <button class="svc-item" role="tab" aria-selected="true" data-s="laser"><em>01</em><h3>הסרת שיער בלייזר</h3></button>
      <button class="svc-item" role="tab" aria-selected="false" data-s="tags"><em>02</em><h3>הסרת סרחי עור</h3></button>
      <button class="svc-item" role="tab" aria-selected="false" data-s="face"><em>03</em><h3>טיפולי פנים</h3></button>
      <button class="svc-item" role="tab" aria-selected="false" data-s="more"><em>04</em><h3>טיפולים נלווים</h3></button>
    </div>
    <div class="svc-panel rv rv-d1" id="svc-panel"></div>
  </div>
</section>

<section class="section dark wrap about" id="about">
  <div class="about-fig wipe">
    %(about)s
    <div class="stamp"><b>12</b><span>שנים של<br>עבודה מהלב</span></div>
  </div>
  <div>
    <p class="eyebrow on-dark rv">נעים להכיר, רויטל</p>
    <h2 class="rv rv-d1">מקצועיות היא לדעת לטפל.<br><em class="serif-it">אכפתיות היא לדעת להקשיב.</em></h2>
    <div class="rv rv-d2" style="margin-top:26px">
      <p class="lead">התחלתי, כמו הרבה, בעבודה במכונים — ושם גם הבנתי מה אני לא רוצה לעשות. ראיתי איך דוחסים לקוחות בלוח זמנים, איך עוברים מהר על אזור כדי להספיק את הבאה בתור, ואיך אחר כך התוצאה חלקית והלקוחה מאשימה את עצמה.</p>
      <p class="lead">כשפתחתי את הקליניקה שלי בגבעת שמואל החלטתי שזה יעבוד אחרת. קטן, אישי, ובקצב הנכון.</p>
      <div class="sig">רויטל</div>
      <a class="link-u" href="about.html" style="color:var(--gold-lt)">הסיפור המלא שלי <span>←</span></a>
    </div>
  </div>
</section>

<section class="section wrap">
  <div class="rv" style="display:flex;justify-content:space-between;align-items:flex-end;gap:30px;flex-wrap:wrap;margin-bottom:44px">
    <div>
      <p class="eyebrow">תוצאות מהקליניקה</p>
      <h2>פחות הבטחות.<br><em class="serif-it">יותר לפני ואחרי.</em></h2>
    </div>
    <a class="link-u" href="gallery.html">לגלריה המלאה <span>←</span></a>
  </div>
  <div class="grid-g rv rv-d1">%(gallery)s</div>
</section>

<section class="section sand wrap" id="stories">
  <div class="rv" style="display:flex;justify-content:space-between;align-items:flex-end;gap:30px;flex-wrap:wrap;margin-bottom:46px">
    <div><p class="eyebrow">הן כבר עברו את זה</p><h2>מה שאני לא יכולה<br><em class="serif-it">להגיד על עצמי.</em></h2></div>
    <div class="ctrls"><button class="prev" aria-label="הקודם">→</button><button class="next" aria-label="הבא">←</button></div>
  </div>
  <div class="story-wrap rv rv-d1" aria-live="polite">
    <article class="story on"><div class="qm">״</div><p>הגעתי בשביל עצמי, ואחרי חודש שלחתי גם את הבת שלי. סוף סוף מקום שאני סומכת עליו במאה אחוז.</p><footer><span class="av">ש</span><div><strong>ש׳, אמא לשתיים</strong><small>הסרת שיער בלייזר</small></div></footer></article>
    <article class="story"><div class="qm">״</div><p>ניסיתי לייזר ביתי שנתיים והייתי בטוחה שהבעיה בי. אצל רויטל ראיתי הבדל כבר אחרי הטיפולים הראשונים.</p><footer><span class="av">מ</span><div><strong>מ׳</strong><small>הסרת שיער בלייזר</small></div></footer></article>
    <article class="story"><div class="qm">״</div><p>לא הרגשתי שמנסים למכור לי. קיבלתי הסבר מדויק, התאמה לעור שלי ותוכנית ברורה. הגעתי לחתונה בלי לחשוב על זה בכלל.</p><footer><span class="av">ד</span><div><strong>ד׳, כלה</strong><small>הסרת שיער בלייזר</small></div></footer></article>
  </div>
  <div class="ribbon rv">
    <span>Google Reviews</span><b>4.9</b><span>★★★★★</span><span>על בסיס ביקורות לקוחות</span>
    <a href="testimonials.html">לכל ההמלצות ←</a>
  </div>
</section>

<section class="section wrap faq">
  <div class="rv">
    <p class="eyebrow">בלי סימני שאלה</p>
    <h2>כל מה שרצית<br><em class="serif-it">לדעת לפני.</em></h2>
    <p class="lead" style="margin:22px 0 26px">לא מצאת תשובה? כתבי לי בוואטסאפ — אני עונה בעצמי, לא בוט.</p>
    <a class="link-u" href="%(wa)s">שאלה אישית לרויטל <span>←</span></a>
  </div>
  <div class="acc rv rv-d1">%(faq)s
    <p style="margin-top:30px"><a class="link-u" href="faq.html">לכל השאלות והתשובות <span>←</span></a></p>
  </div>
</section>

<section class="band">
  <div><small>טיפ קטן לפני שמתחילות</small><br><strong>לא בטוחה אם לייזר מתאים לך?</strong></div>
  <span>כמה שאלות קצרות, וכיוון ראשוני — בלי להשאיר טלפון.</span>
  <button class="btn btn-light open-bot"><span>מתחילות בבדיקה</span><span class="arw">←</span></button>
</section>

<section class="section dark wrap contact" id="contact">
  <div>
    <p class="eyebrow on-dark rv">הצעד הראשון קטן</p>
    <h2 class="rv rv-d1">בואי לבדוק.<br><em class="serif-it">בלי להתחייב.</em></h2>
    <p class="lead rv rv-d2" style="margin:22px 0 38px">משאירות פרטים, רויטל חוזרת לשיחה קצרה, ומתאמות טסט אבחון ללא עלות.</p>
    <div class="rv rv-d3">
      <div class="step"><em>01</em><p><strong>וואטסאפ תוך דקה</strong>הודעה אישית ממני עם סרטון קצר על איך אני עובדת</p></div>
      <div class="step"><em>02</em><p><strong>שיחה תוך 24 שעות</strong>להבין מה מפריע ומה ניסית עד היום — בלי לחץ מכירה</p></div>
      <div class="step"><em>03</em><p><strong>טסט אישי בקליניקה</strong>צילום האזור, בדיקת זקיק השערה והסבר מלא</p></div>
      <div class="step"><em>04</em><p><strong>החלטה בנחת</strong>רק אם מתאים — בונות יחד תוכנית ומחיר שקוף</p></div>
    </div>
  </div>
  %(form)s
</section>
"""

FORM = """<form class="form rv rv-d1">
  <div class="form-h"><strong>טסט אבחון חינם</strong><small>כ־30 שניות וזה אצלנו</small></div>
  <label>איך קוראים לך?<input name="name" type="text" placeholder="שם מלא" required></label>
  <label>לאיזה מספר לחזור?<input name="phone" type="tel" placeholder="050-0000000" required></label>
  <label>מה מעניין אותך?<select name="interest">
    <option>הסרת שיער בלייזר</option><option>הסרת סרחי עור</option><option>טיפולי פנים</option>
    <option>טיפולים נלווים</option><option>עדיין לא בטוחה</option></select></label>
  <label>מה הכי מתאים לך?<select name="segment">
    <option>אמא — גם לי וגם לבת שלי</option><option>לפני חתונה</option><option>לפני גיוס או לימודים</option>
    <option>ניסיתי לייזר בעבר ולא עבד</option><option>פשוט נמאס לי לגלח</option><option>אני גבר</option></select></label>
  <label class="chk"><input type="checkbox" required><span>אני מאשרת קבלת שיחה או הודעה בנוגע לפנייה</span></label>
  <button class="btn" type="submit" style="justify-content:center"><span>אני רוצה לתאם טסט</span><span class="arw">←</span></button>
  <p class="note">הפרטים שלך נשארים אצלנו. בלי ספאם ובלי לחץ.</p>
  <div class="ok" role="status">קיבלנו, תודה! רויטל תחזור אלייך בקרוב.</div>
</form>"""

FAQ_ITEMS = [
 ("ראיתי מקומות זולים יותר — למה אצלך זה עולה יותר?",
  "אני מבינה לגמרי. ההבדל הוא במכשיר: InMode Optimas הוא מכשיר קליני מהמובילים בעולם ועולה מאות אלפי שקלים — זה לא מכשיר סיני זול ולא לייזר ביתי. בפועל את צריכה פחות טיפולים כדי לראות תוצאה אמיתית, אז ההשוואה הנכונה היא לא &quot;כמה עולה טיפול&quot; אלא &quot;כמה עולה לי להגיע לתוצאה&quot;. בואי לטסט החינם ואני אראה לך בדיוק את ההבדל."),
 ("כבר ניסיתי לייזר ביתי או במקום זול, וזה לא עבד",
  "זו בדיוק הסיבה שאת פה. הרבה מהלקוחות שלי הגיעו אחרי שניסו ולא ראו תוצאה — הבעיה לא הייתה בהן, אלא במכשור שלא היה חזק מספיק. בואי לטסט ותראי בעצמך, על הזקיק שלך, שזה מתנהג אחרת."),
 ("כמה טיפולים אני צריכה?",
  "תלוי באזור, בסוג השיער ובעור. סדרה סטנדרטית היא בדרך כלל בסביבות 10 טיפולים, במרווחים של 4-6 שבועות. בטסט אני בודקת את זקיק השערה ונותנת לך מספר ריאלי — לא מספר שנשמע טוב במכירה."),
 ("האם הטיפול כואב?",
  "תחושת עקצוץ קלה שנמשכת רגע. המכשיר עובד עם מנגנון קירור, ואני עוברת לאט ומווסתת את העוצמה לפי מה שנוח לך — אפשר לעצור ולהתאים בכל שלב. רוב הלקוחות מופתעות לטובה."),
 ("יש שיער שלא מגיב לטיפול?",
  "כן — שיער בהיר, בלונדיני, ג׳ינג׳י או לבן לא מגיב טוב ללייזר, כי אין בו מספיק פיגמנט שהלייזר יכול לפעול עליו. אני מעדיפה להגיד לך את זה מראש מאשר לקחת ממך כסף על משהו שלא יעבוד."),
]

def acc(items):
    return "".join('<details%s><summary>%s<i>＋</i></summary><p>%s</p></details>'
                   % (" open" if i == 0 else "", q, a) for i, (q, a) in enumerate(items))

# ===================== תבנית עמוד פנימי =====================
def phead(crumb, eyebrow, h1, lead, cta=True):
    return """<section class="phead wrap">
  <p class="crumb"><a href="index.html">עמוד הבית</a> · %s</p>
  <p class="eyebrow rv">%s</p>
  <h1 class="rv rv-d1">%s</h1>
  <p class="lead rv rv-d2">%s</p>
  %s
</section>""" % (crumb, eyebrow, h1, lead,
   '<div class="hero-cta rv rv-d3" style="margin-top:30px"><a class="btn" href="contact.html"><span>לטסט אבחון חינם</span><span class="arw">←</span></a><button class="btn btn-ghost open-bot"><span>בדקי אם זה מתאים לך</span><span class="arw">←</span></button></div>' if cta else '')

def closer(title, text):
    return """<section class="band">
  <div><small>הצעד הראשון</small><br><strong>%s</strong></div>
  <span>%s</span>
  <a class="btn btn-light" href="contact.html"><span>לתיאום טסט חינם</span><span class="arw">←</span></a>
</section>""" % (title, text)

# ===================== לייזר =====================
LASER = phead("הסרת שיער בלייזר", "השירות המרכזי בקליניקה",
  "הסרת שיער בלייזר<br><em class='serif-it'>בגבעת שמואל</em>",
  "מכשיר InMode Optimas, 12 שנות ניסיון, ועבודה איטית ומדויקת. את לא צריכה להאמין לי — בואי לטסט חינם ותראי בעצמך.") + """
<section class="section wrap two">
  <div class="rv">
    <h2>נשמע מוכר?</h2>
    <p class="lead" style="margin-top:20px">את מגלחת כל יומיים־שלושה. העור מגורה. לפני הים את מתכננת מראש. אולי כבר ניסית לייזר ביתי, אולי גם מכון זול — ואחרי חצי שנה השיער חזר בדיוק כמו שהיה. ואז את אומרת לעצמך: &quot;בטח גם פה זה לא יעבוד.&quot;</p>
  </div>
  <div class="prose rv rv-d1">
    <ul>
      <li>גילוח יומיומי שחוזר על עצמו בלי סוף, וגירוי בעור אחריו</li>
      <li>שערות חודרניות וכתמים כהים באזורי החיכוך</li>
      <li>ניסיון קודם עם לייזר ביתי או מכשיר זול שלא הניב תוצאה</li>
      <li>חשש להשקיע לפני חתונה, גיוס או תחילת לימודים — בלי לדעת אם זה בכלל יעבוד</li>
      <li>ואם את אמא: את לא רוצה שהבת שלך תעבור את מה שאת עברת שנים</li>
    </ul>
    <div class="callout"><strong>בגלל זה אני לא מבקשת ממך להאמין לי.</strong><p>אני מבקשת ממך לבוא ולראות. הטסט חינם, וההחלטה שלך.</p></div>
  </div>
</section>

<section class="section sand wrap">
  <div class="two">
    <div class="rv"><p class="eyebrow">איך זה עובד</p><h2>בשפה פשוטה,<br><em class="serif-it">בלי מונחים.</em></h2></div>
    <div class="prose rv rv-d1">
      <p>קרן הלייזר נספגת בפיגמנט שבתוך זקיק השערה והופכת לחום, שפוגע ביכולת של הזקיק לייצר שערה חדשה.</p>
      <p>הזקיק מגיב רק כשהשערה נמצאת בשלב הצמיחה שלה — ומכיוון שלא כל השערות בשלב הזה באותו זמן, צריך סדרת טיפולים במרווחים כדי לתפוס את כולן.</p>
      <p><strong>זו הסיבה שאף אחד לא יכול לסיים לך את זה בטיפול אחד</strong> — וכל מי שמבטיח לך את זה, לא מדייק.</p>
    </div>
  </div>
</section>

<section class="section wrap">
  <div class="rv" style="max-width:640px;margin-bottom:40px">
    <p class="eyebrow">ההבדל האמיתי</p>
    <h2>מה יש לי<br><em class="serif-it">שאין בלייזר ביתי.</em></h2>
  </div>
  <div class="rv rv-d1" style="overflow-x:auto">
  <table class="tbl">
    <thead><tr><th></th><th>לייזר ביתי / מכשיר זול</th><th>InMode Optimas בקליניקה</th></tr></thead>
    <tbody>
      <tr><td>עוצמה</td><td>נמוכה, מוגבלת בבטיחות לשימוש עצמי</td><td>עוצמה קלינית מלאה</td></tr>
      <tr><td>התאמה אישית</td><td>אין — עוצמה אחת לכולם</td><td>מותאמת לסוג העור ולעובי השיער שלך</td></tr>
      <tr><td>כיסוי האזור</td><td>את לא רואה איפה עברת</td><td>מעבר שיטתי ומבוקר, אזור אחר אזור</td></tr>
      <tr><td>ליווי</td><td>אין</td><td>רויטל, לאורך כל התהליך</td></tr>
      <tr><td>תוצאה</td><td>לרוב חלקית וחוזרת</td><td>תוצאה שנשארת</td></tr>
    </tbody>
  </table>
  </div>
</section>

<section class="section dark wrap">
  <div class="two">
    <div class="rv">
      <p class="eyebrow on-dark">מוצר הפרונט</p>
      <h2>הטסט החינם —<br><em class="serif-it">הוכחה, לא הבטחה.</em></h2>
      <p class="lead" style="margin-top:22px">לפני שאת משלמת שקל, את מגיעה לקליניקה לטסט קצר.</p>
    </div>
    <div class="rv rv-d1">
      <div class="step"><em>01</em><p><strong>צילום האזור</strong>תיעוד נקודת הפתיחה, כדי שיהיה מול מה להשוות</p></div>
      <div class="step"><em>02</em><p><strong>בדיקת זקיק השערה</strong>סוג השיער והעור שלך, והתאמת עוצמת הטיפול</p></div>
      <div class="step"><em>03</em><p><strong>הדגמה בפועל</strong>את רואה שהמכשיר עובד — כאן, עכשיו, על השיער שלך</p></div>
      <div class="step"><em>04</em><p><strong>תוכנית ומחיר</strong>כמה טיפולים, תוך כמה זמן, וכמה זה עולה. שקוף, בלי הפתעות.</p></div>
      <p style="margin-top:26px;color:rgba(250,247,241,.6)"><strong style="color:var(--gold-lt)">ומה לא יהיה שם:</strong> לחץ מכירה. באמת.</p>
    </div>
  </div>
</section>

<section class="section wrap">
  <div class="rv" style="max-width:620px;margin-bottom:40px">
    <p class="eyebrow">אזורי טיפול</p>
    <h2>איפה מטפלים</h2>
  </div>
  <div class="pillars rv rv-d1" style="border:1px solid var(--line)">
    <article><b>◈</b><strong>גוף</strong><p>רגליים מלאות או חצי · ידיים · גב · חזה ובטן · כתפיים</p></article>
    <article><b>◈</b><strong>אזורים אינטימיים</strong><p>בית שחי · ביקיני רגיל · ביקיני ברזילאי</p></article>
    <article><b>◈</b><strong>פנים</strong><p>שפה עליונה · סנטר · לחיים · צוואר</p></article>
    <article><b>◈</b><strong>גברים</strong><p>גב · חזה · כתפיים · קו זקן</p></article>
  </div>
</section>

<section class="section sand wrap">
  <div class="rv" style="max-width:640px;margin-bottom:40px">
    <p class="eyebrow">תוצאות אמיתיות</p>
    <h2>לפני ואחרי</h2>
    <p class="lead" style="margin-top:18px">כל תמונה כאן היא של לקוחה אמיתית, בהסכמתה. בלי עריכה ובלי תאורה מטעה.</p>
  </div>
  <div class="grid-g rv rv-d1">%(gallery)s</div>
</section>

<section class="section wrap two">
  <div class="prose rv">
    <h3>לפני הטיפול</h3>
    <ul>
      <li>לגלח את האזור יום לפני — לא שעווה, לא פינצטה ולא אפילציה</li>
      <li>להימנע מחשיפה לשמש ומשיזוף מלאכותי כשבועיים לפני</li>
      <li>להגיע בלי קרם או דאודורנט על האזור</li>
      <li>לעדכן אותי על כל תרופה או תהליך רפואי</li>
    </ul>
  </div>
  <div class="prose rv rv-d1">
    <h3>אחרי הטיפול</h3>
    <ul>
      <li>אודם קל למשך כמה שעות — נורמלי לגמרי</li>
      <li>להימנע משמש ישירה, סאונה ובריכה 48 שעות</li>
      <li>קרם הרגעה ומקדם הגנה</li>
      <li>לא לגלח עד שאני אומרת</li>
    </ul>
    <p style="color:var(--muted);font-size:14.5px">ההנחיות נמסרות גם בכתב בסוף כל טיפול.</p>
  </div>
</section>
""" + closer("מוכנה לראות אם זה עובד עלייך?", "טסט אבחון חינם — בלי עלות ובלי התחייבות.")

# ===================== סרחי עור =====================
SKINTAGS = phead("הסרת סרחי עור", "טיפול קצר, תוצאה מיידית",
  "הסרת סרחי עור —<br><em class='serif-it'>מהר ובלי דרמה</em>",
  "סרחי עור בצוואר, בבתי השחי או מתחת לחזה מפריעים לך? הסרה בקליניקה בגבעת שמואל, בטיפול קצר ומדויק, בלי ניתוח.") + """
<section class="section wrap two">
  <div class="rv">
    <p class="eyebrow">קודם כול — מה זה</p>
    <h2>שפיר לגמרי.<br><em class="serif-it">ומעצבן לגמרי.</em></h2>
  </div>
  <div class="prose rv rv-d1">
    <p>סרחי עור (Skin Tags, ובעברית גם &quot;יבלות עור&quot;) הם גדילי עור קטנים ורכים שתלויים על העור. הם שפירים לחלוטין ולא מסוכנים — אבל הם נתקעים בשרשרת, מתחככים בבגד, נחתכים בגילוח, ופשוט מציקים.</p>
    <h3>איפה הם מופיעים</h3>
    <ul><li>צוואר</li><li>בתי שחי</li><li>מתחת לחזה</li><li>מפשעה</li><li>עפעפיים</li><li>כל אזור חיכוך</li></ul>
    <h3>למה הם מופיעים</h3>
    <p>חיכוך מתמשך בין עור לעור או לבגד, שינויים הורמונליים (למשל בהיריון), נטייה גנטית, ולעיתים גם שינויי משקל. <strong>זה לא עניין של היגיינה</strong> — וזה נפוץ הרבה יותר משנדמה לך.</p>
  </div>
</section>

<section class="section dark wrap">
  <div class="two">
    <div class="rv"><p class="eyebrow on-dark">חשוב שתדעי</p><h2>למה לא לטפל<br><em class="serif-it">בזה לבד.</em></h2></div>
    <div class="prose rv rv-d1">
      <ul>
        <li><strong>קשירה או חיתוך בבית</strong> — עלולים לגרום לזיהום, לדימום ולצלקת</li>
        <li><strong>קרמים &quot;מסירי יבלות&quot;</strong> — מכילים חומרים חריפים שיכולים לכוות את העור סביב</li>
      </ul>
      <div class="callout" style="background:rgba(184,137,60,.1);border-color:rgba(184,137,60,.3)">
        <strong style="color:var(--gold-lt)">והכי חשוב</strong>
        <p style="color:rgba(250,247,241,.72)">לא כל נגע עור הוא סרח עור. יש נגעים שנראים דומה וצריכים בדיקה רפואית. אני בודקת מקרוב לפני כל טיפול, ואם משהו נראה לי לא אופייני — אני שולחת אותך לרופא עור לפני שאני נוגעת.</p>
      </div>
    </div>
  </div>
</section>

<section class="section wrap">
  <div class="two">
    <div class="rv">
      <p class="eyebrow">מהלך הטיפול</p><h2>ארבעה שלבים,<br><em class="serif-it">חצי שעה.</em></h2>
      %(fig_skintags)s
    </div>
    <div class="rv rv-d1">
      <div class="step" style="border-color:var(--line)"><em>01</em><p><strong>אבחון</strong><span style="color:var(--muted)">בדיקה מקרוב, ווידוא שמדובר בסרחי עור</span></p></div>
      <div class="step" style="border-color:var(--line)"><em>02</em><p><strong>הכנה</strong><span style="color:var(--muted)">ניקוי וחיטוי, ולפי הצורך חומר הרדמה מקומי</span></p></div>
      <div class="step" style="border-color:var(--line)"><em>03</em><p><strong>הסרה</strong><span style="color:var(--muted)">טיפול נקודתי ומדויק — כמה שניות לכל סרח</span></p></div>
      <div class="step" style="border-color:var(--line)"><em>04</em><p><strong>טיפוח והדרכה</strong><span style="color:var(--muted)">משחה מרגיעה והנחיות ברורות להמשך</span></p></div>
      <div class="callout">
        <p style="margin:0"><strong style="font-family:var(--body);font-size:15px">כמה זמן?</strong> 15-30 דקות, תלוי בכמות. רוב הלקוחות מסיימות בפגישה אחת.<br>
        <strong style="font-family:var(--body);font-size:15px">כואב?</strong> תחושת עקיצה קצרה. עם הרדמה מקומית — כמעט לא מרגישים.<br>
        <strong style="font-family:var(--body);font-size:15px">מתי חוזרים לשגרה?</strong> מיד. נשאר גלד קטן שנושר לבד תוך שבוע-שבועיים.</p>
      </div>
    </div>
  </div>
</section>

<section class="section sand wrap faq">
  <div class="rv"><p class="eyebrow">שאלות נפוצות</p><h2>מה ששואלים אותי<br><em class="serif-it">על סרחי עור.</em></h2></div>
  <div class="acc rv rv-d1">%(faq_tags)s</div>
</section>
""" + closer("מפריע לך כבר מזמן?", "בואי לאבחון — אגיד לך בדיוק מה אפשר לעשות וכמה זה עולה.")

FAQ_TAGS = [
 ("האם זה חוזר?","הסרח שהוסר לא חוזר. אבל אם הנטייה שלך היא לפתח סרחי עור, יכולים להופיע חדשים במקומות אחרים — זה לא כישלון של הטיפול, זו פשוט הנטייה של העור שלך."),
 ("נשארת צלקת?","בטיפול מקצועי, ברוב המקרים לא. השמירה על מקדם הגנה בחודש שאחרי הטיפול היא בדיוק מה שמונע כתם כהה."),
 ("כמה זה עולה?","תלוי בכמות ובאזור. באבחון אני נותנת לך מחיר מדויק לפני שמתחילים — בלי תוספות בדרך."),
 ("אפשר לשלב עם טיפול אחר?","בהחלט. הרבה לקוחות משלבות עם טיפול פנים או עם סדרת לייזר באותו ביקור."),
 ("זה מתאים לגברים?","כן, לגמרי. סרחי עור בצוואר ובבתי השחי נפוצים מאוד גם אצל גברים."),
]

# ===================== טיפולי פנים =====================
FACIALS = phead("טיפולי פנים", "אחרי אבחון, לא לפי קטלוג",
  "טיפולי פנים שמותאמים<br><em class='serif-it'>לעור שלך</em>",
  "אחרי 12 שנה בתחום למדתי שאין טיפול פנים אחד שמתאים לכולן. מתחילות מאבחון עור, ומשם בונות טיפול.") + """
<section class="section wrap two">
  <div class="rv">
    <p class="eyebrow">נקודת ההתחלה</p>
    <h2>הכול מתחיל<br><em class="serif-it">באבחון.</em></h2>
    %(fig_facial)s
  </div>
  <div class="prose rv rv-d1">
    <p>לפני הטיפול הראשון אני בודקת את העור שלך: סוג, רמת לחות, רגישויות, כתמים, פיגמנטציה, סימני גיל, והרגלי הטיפוח שלך בבית.</p>
    <p>רק אחרי זה אנחנו מחליטות מה עושים — <strong>ומה לא</strong>. לפעמים ההמלצה שלי היא לעשות פחות ממה שחשבת, וזה בסדר גמור.</p>
    <div class="callout">
      <strong>למה הרבה לקוחות לייזר עוברות גם לפנים</strong>
      <p>רוב הלקוחות מגיעות אליי בהתחלה בשביל הלייזר. אחרי כמה טיפולים, כשכבר יש בינינו אמון, הן שואלות &quot;ומה עם הפנים?&quot; — ומשם זה מתגלגל. אני כבר מכירה את העור שלהן, את הרגישויות ואת ההרגלים, ולכן הטיפול מדויק יותר.</p>
    </div>
  </div>
</section>

<section class="section sand wrap">
  <div class="rv" style="max-width:640px;margin-bottom:44px">
    <p class="eyebrow">סוגי הטיפולים</p>
    <h2>מה אפשר לעשות כאן</h2>
  </div>
  <div class="pillars rv rv-d1" style="border:1px solid var(--line)">
    <article><b>01</b><strong>ניקוי עור עמוק</strong><p>ניקוי יסודי, שחרור סתימות והחזרת נשימה לעור. הטיפול הבסיסי והמבוקש ביותר.</p></article>
    <article><b>02</b><strong>חידוש והבהרה</strong><p>לעור עייף, לא אחיד או עם כתמי פיגמנטציה. משפר מרקם וגוון ומחזיר זוהר.</p></article>
    <article><b>03</b><strong>עור בוגר</strong><p>מיקוד בהידוק, בגמישות ובקווים דקים.</p></article>
    <article><b>04</b><strong>עור רגיש ואקנה</strong><p>טיפול עדין ומרגיע, עם דגש על הרגעת דלקתיות ובניית שגרת בית נכונה.</p></article>
  </div>
  <p class="rv" style="color:var(--muted);font-size:14.5px;margin-top:22px">רשימת הטיפולים המדויקת והשמות המסחריים — להשלמה מול רויטל.</p>
</section>

<section class="section wrap two">
  <div class="prose rv">
    <h3>מה כולל טיפול</h3>
    <ul><li>ניקוי והכנה</li><li>אבחון מצב העור באותו יום</li><li>הטיפול עצמו</li><li>מסכה מותאמת</li><li>הרגעה והגנה</li><li>הדרכת טיפוח לבית</li></ul>
  </div>
  <div class="prose rv rv-d1">
    %(fig_mask)s
    <h3 style="margin-top:34px">כמה זמן וכל כמה זמן</h3>
    <p>טיפול נמשך בין 45 דקות לשעה וחצי, תלוי בסוג. התדירות המומלצת היא לרוב אחת ל-4 עד 6 שבועות, בהתאם לעור ולמטרה.</p>
    <div class="callout">
      <strong>לפני אירוע</strong>
      <p>לא עושים טיפול חדש בפעם הראשונה יומיים לפני חתונה. מתכננים מראש — ומגיעות לאירוע עם עור שכבר יודעות איך הוא מגיב.</p>
    </div>
  </div>
</section>
""" + closer("רוצה לדעת מה העור שלך באמת צריך?", "בואי לאבחון עור — נסתכל ביחד ונחליט מה נכון עבורך.")

# ===================== טיפולים נלווים =====================
TREATMENTS = phead("טיפולים נלווים", "ההמשך של התהליך",
  "טיפולים נלווים —<br><em class='serif-it'>ההמשך הטבעי</em>",
  "אחרי שפתרנו את נושא השיער אפשר להתקדם. טיפולים משלימים לחידוש, להידוק ולשיפור מרקם העור.") + """
<section class="section wrap two">
  <div class="rv">
    <p class="eyebrow">הטיפול המרכזי</p>
    <h2>פלזמה</h2>
    %(fig_plasma)s
  </div>
  <div class="prose rv rv-d1">
    <p>טיפול מתקדם לחידוש והידוק העור. הפלזמה מייצרת גירוי מבוקר ברקמה, שמעודד את העור לייצר קולגן חדש ולהתחדש מבפנים.</p>
    <h3>למה זה מתאים</h3>
    <ul><li>רפיון עדין של העור</li><li>קווים דקים</li><li>שיפור מרקם וגוון</li><li>אזורים עדינים כמו סביב העיניים</li></ul>
    <h3>מה מרגישים</h3>
    <p>תחושת חום ואודם קל שחולפים. הנחיות טיפוח מלאות נמסרות בסוף הטיפול.</p>
    <p style="color:var(--muted);font-size:14.5px">מספר הטיפולים נקבע רק אחרי אבחון אישי — תלוי במצב העור ובמטרה.</p>
  </div>
</section>

<section class="section sand wrap two">
  <div class="rv">
    <p class="eyebrow">גם אצלנו</p>
    <h2>חידוש והידוק,<br><em class="serif-it">הסרת נימים.</em></h2>
  </div>
  <div class="prose rv rv-d1">
    <p>טיפולים לשיפור גמישות ומרקם, כהמשך לתהליך הפנים או כטיפול עצמאי. גם כאן — מתחילים מאבחון, לא מקטלוג.</p>
    <h3>שילוב נכון של טיפולים</h3>
    <p>הרבה לקוחות רוצות &quot;לעשות הכול ביחד&quot;. אני בדרך כלל ממליצה אחרת: לעשות דברים בסדר הנכון ובמרווחים נכונים, כדי שהעור יספיק להתאושש ושנוכל לראות מה באמת עבד.</p>
  </div>
</section>

<section class="section dark wrap">
  <div class="two">
    <div class="rv"><p class="eyebrow on-dark">שקיפות</p><h2>מה אנחנו<br><em class="serif-it">לא עושים.</em></h2></div>
    <div class="rv rv-d1">
      <p class="lead">בקליניקה אני לא מבצעת הזרקות. אני מתמקדת בתחומים שאני מומחית בהם — הסרת שיער בלייזר, טיפולי פנים וחידוש עור.</p>
      <p class="lead">אם משהו שאת מחפשת לא בתחום שלי, אני אגיד לך את זה ישר, ואפנה אותך למי שכן. זה עדיף על פני שאני אנסה משהו שאני לא הכי טובה בו.</p>
    </div>
  </div>
</section>
""" + closer("לא בטוחה מה מתאים לך?", "זה בדיוק מה שהאבחון האישי נועד לו.")

# ===================== אודות =====================
ABOUT = """
<section class="section wrap about" style="padding-top:clamp(48px,5vw,84px)">
  <div class="about-fig wipe">
    %(about_portrait)s
    <div class="stamp"><b>12</b><span>שנים של<br>עבודה מהלב</span></div>
  </div>
  <div>
    <p class="crumb"><a href="index.html">עמוד הבית</a> · אודות</p>
    <p class="eyebrow rv">נעים להכיר</p>
    <h1 class="rv rv-d1">אני רויטל,<br><em class="serif-it">והקליניקה הזאת</em><br>היא הבייבי שלי.</h1>
    <p class="lead rv rv-d2" style="margin-top:24px">12 שנה בתחום הקוסמטיקה, קליניקת בוטיק בגבעת שמואל, ומכשיר InMode Optimas שבחרתי בכוונה.</p>
  </div>
</section>

<section class="section sand wrap two">
  <div class="rv"><p class="eyebrow">איך הגעתי לכאן</p><h2>מה שראיתי<br><em class="serif-it">במכונים.</em></h2></div>
  <div class="prose rv rv-d1">
    <p>התחלתי, כמו הרבה, בעבודה במכונים — ושם גם הבנתי מה אני <em>לא</em> רוצה לעשות.</p>
    <p>ראיתי איך דוחסים לקוחות בלוח זמנים. איך עוברים מהר על אזור כדי להספיק את הבאה בתור. ואיך אחר כך התוצאה חלקית, והלקוחה מאשימה את עצמה.</p>
    <p>כשפתחתי את הקליניקה שלי בגבעת שמואל, החלטתי שזה יעבוד אחרת. קטן, אישי, ובקצב הנכון.</p>
  </div>
</section>

<section class="section dark wrap two">
  <div class="rv">
    <p class="eyebrow on-dark">ההחלטה היקרה</p>
    <h2>למה השקעתי<br><em class="serif-it">במכשיר כזה יקר.</em></h2>
  </div>
  <div class="rv rv-d1">
    <p class="lead">אפשר לפתוח קליניקת לייזר עם מכשיר בעשירית המחיר. אני בחרתי אחרת, ואני אגיד לך בדיוק למה.</p>
    <p class="lead">הגיעו אליי יותר מדי נשים שכבר ניסו לייזר — ביתי, או במקום זול — ולא ראו תוצאה. והן הגיעו בטוחות שהבעיה בהן, שהשיער שלהן &quot;עקשן&quot;, שאולי זה פשוט לא עובד על כולן. <strong style="color:var(--gold-lt)">זה כמעט אף פעם לא נכון.</strong> הבעיה הייתה במכשור.</p>
    <p class="lead">אז אני עובדת עם InMode Optimas — מכשיר קליני מהמובילים בעולם, שעולה מאות אלפי שקלים. אני לא מספרת את זה כדי להצדיק מחיר. אני מספרת את זה כי זה ההבדל בין תוצאה לבין עוד ניסיון מאכזב.</p>
  </div>
</section>

<section class="section wrap">
  <div class="rv" style="max-width:640px;margin-bottom:44px">
    <p class="eyebrow">ארבעה עקרונות</p>
    <h2>איך אני עובדת</h2>
  </div>
  <div class="pillars rv rv-d1" style="border:1px solid var(--line)">
    <article><b>◈</b><strong>לאט</strong><p>עוברת עם ידית המכשיר אזור אחר אזור, בקצב שהטיפול דורש. לא בקצב של יומן עמוס.</p></article>
    <article><b>◈</b><strong>אישית</strong><p>אני זו שמקבלת אותך, מטפלת בך ומלווה אותך. אין צוות מתחלף ואין &quot;מי שפנויה עכשיו&quot;.</p></article>
    <article><b>◈</b><strong>בשקיפות</strong><p>אם השיער שלך בהיר ולא יגיב טוב ללייזר — אני אגיד לך את זה בטסט, ולא אקח ממך כסף.</p></article>
    <article><b>◈</b><strong>בלי לחץ</strong><p>בגלל זה הטסט חינם. עדיף שתראי במו עינייך ותחליטי, מאשר שתשלמי מתוך שכנוע.</p></article>
  </div>
</section>

<section class="section sand wrap two">
  <div class="rv">
    <p class="eyebrow">האווירה כאן</p>
    <h2>כמו לבוא<br><em class="serif-it">לחברה.</em></h2>
    %(fig_clinic)s
  </div>
  <div class="prose rv rv-d1">
    <p>אני לא רשמית ואני לא &quot;קוסמטיקאית מרוחקת&quot;. באות לפה לטיפול ויוצאות עם עוד סיפור טוב. לקוחות מספרות לי דברים שהן לא מספרות לאף אחד, ואני שומרת על זה.</p>
    <p>זה יחס של חברה — פשוט חברה שבמקרה יש לה מכשיר לייזר מקצועי.</p>
    <div class="callout">
      <strong>הדבר שהכי מרגש אותי</strong>
      <p>כשלקוחה מגיעה בשביל עצמה, ואחרי חודש שולחת לי הודעה: &quot;רויטל, אני מביאה גם את הבת שלי.&quot; זו המחמאה הכי גדולה שיש. כי אמא לא שולחת את הבת שלה למקום שהיא לא סומכת עליו במאה אחוז.</p>
    </div>
  </div>
</section>
""" + closer("רוצה להכיר?", "בואי לטסט אבחון חינם — נכיר, ותראי בעצמך איך אני עובדת.")

# ===================== המלצות =====================
TESTIMONIALS = phead("המלצות", "הן כבר עברו את זה",
  "מה שאני לא יכולה<br><em class='serif-it'>להגיד על עצמי</em>",
  "אני יכולה לספר לך כמה שאני רוצה שזה עובד. עדיף שתשמעי את זה מהן.", cta=False) + """
<section class="section wrap sand" style="padding-inline:var(--pad)">
  <div class="rv" style="display:flex;justify-content:space-between;align-items:flex-end;gap:30px;flex-wrap:wrap;margin-bottom:44px">
    <div><p class="eyebrow">בקולן</p><h2>סיפורים מהקליניקה</h2></div>
    <div class="ctrls"><button class="prev" aria-label="הקודם">→</button><button class="next" aria-label="הבא">←</button></div>
  </div>
  <div class="story-wrap rv rv-d1" aria-live="polite">
    <article class="story on"><div class="qm">״</div><p>הגעתי בשביל עצמי, ואחרי חודש שלחתי גם את הבת שלי. סוף סוף מקום שאני סומכת עליו במאה אחוז.</p><footer><span class="av">ש</span><div><strong>ש׳, אמא לשתיים</strong><small>הסרת שיער בלייזר</small></div></footer></article>
    <article class="story"><div class="qm">״</div><p>ניסיתי לייזר ביתי שנתיים והייתי בטוחה שהבעיה בי. אצל רויטל ראיתי הבדל כבר אחרי הטיפולים הראשונים.</p><footer><span class="av">מ</span><div><strong>מ׳</strong><small>הסרת שיער בלייזר</small></div></footer></article>
    <article class="story"><div class="qm">״</div><p>לא הרגשתי שמנסים למכור לי. קיבלתי הסבר מדויק, התאמה לעור שלי ותוכנית ברורה. הגעתי לחתונה בלי לחשוב על זה בכלל.</p><footer><span class="av">ד</span><div><strong>ד׳, כלה</strong><small>הסרת שיער בלייזר</small></div></footer></article>
    <article class="story"><div class="qm">״</div><p>הגעתי מאוד חששנית ורויטל פשוט עצרה, הסבירה לי הכול ועשתה טסט קטן. כבר מהפגישה הראשונה הרגשתי שאני בידיים טובות.</p><footer><span class="av">ר</span><div><strong>ר׳</strong><small>טיפולי פנים</small></div></footer></article>
  </div>
</section>

<section class="section wrap">
  <div class="rv" style="max-width:640px;margin-bottom:38px">
    <p class="eyebrow">בלי עריכה</p>
    <h2>הודעות שקיבלתי,<br><em class="serif-it">בהסכמתן.</em></h2>
    <p class="lead" style="margin-top:18px">אלה צילומי מסך אמיתיים מהטלפון שלי. לא ניסחתי אותם מחדש ולא ייפיתי.</p>
  </div>
  <div class="wa-grid rv rv-d1">%(wa_wall)s</div>
</section>

<section class="section sand wrap">
  <div class="rv" style="max-width:640px;margin-bottom:38px">
    <p class="eyebrow">תוצאות</p><h2>לפני ואחרי</h2>
  </div>
  <div class="grid-g rv rv-d1">%(gallery)s</div>
  <p class="rv" style="margin-top:24px"><a class="link-u" href="gallery.html">לגלריה המלאה <span>←</span></a></p>
</section>

<section class="section wrap two">
  <div class="rv">
    <p class="eyebrow">ביקורות גוגל</p>
    <h2>4.9 בגוגל</h2>
    <p class="lead" style="margin-top:18px">כל הביקורות של הקליניקה, בלי סינון ובלי עריכה.</p>
    <p style="margin-top:22px"><a class="link-u" href="#">לכל הביקורות בגוגל <span>←</span></a></p>
  </div>
  <div class="rv rv-d1">
    <div class="callout" style="margin:0">
      <strong>רוצה להיות הבאה שמספרת?</strong>
      <p>אם טיפלתי בך ובא לך לספר — אשמח מאוד. גם הקלטה קצרה בטלפון מושלמת, ממש לא צריך משהו מסודר.</p>
      <p style="margin:0"><a class="link-u" href="%(wa)s">לשלוח לי המלצה <span>←</span></a></p>
    </div>
  </div>
</section>
""" + closer("מוכנה להתחיל?", "טסט אבחון חינם, בלי עלות ובלי התחייבות.")

# ===================== שאלות ותשובות =====================
FAQ_FULL = {
 "מחיר וכדאיות": FAQ_ITEMS[0:1] + [
   ("כמה עולה סדרה?","תלוי באזור ובמספר הטיפולים שאת צריכה — וזה נקבע רק אחרי שאני בודקת את זקיק השערה שלך. בטסט את מקבלת מספר מדויק ושקוף, בלי הפתעות ובלי תוספות בדרך."),
   ("יש אפשרות לתשלומים?","כן. נדבר על זה בטסט ונמצא משהו שמסתדר לך."),
   ("הטסט באמת חינם?","כן, לגמרי. בלי עלות, בלי התחייבות ובלי &quot;מחיר מיוחד רק להיום&quot;. את מגיעה, רואה, ומחליטה בזמן שלך."),
 ],
 "הטיפול עצמו": [FAQ_ITEMS[2], FAQ_ITEMS[3],
   ("כל כמה זמן מגיעים?","בדרך כלל אחת ל-4 עד 6 שבועות, תלוי באזור. המרווח לא שרירותי — הוא נועד לתפוס את השערות בשלב הצמיחה שלהן."),
   ("כמה זמן לוקח טיפול?","תלוי באזור — מכמה דקות ועד כשעה. אני לא ממהרת ולא דוחסת לקוחות, אז את מקבלת את הזמן שהטיפול באמת דורש."),
   ("מתי רואים תוצאות?","הרבה לקוחות מרגישות ירידה כבר אחרי 2-3 טיפולים. התוצאה המשמעותית מצטברת לאורך הסדרה."),
   ("זה לצמיתות?","הזקיקים שמטופלים בהצלחה לא מייצרים שערה חדשה. עם זאת, שינויים הורמונליים לאורך החיים יכולים לעורר זקיקים חדשים, ולכן לפעמים מומלץ טיפול תחזוקה אחת לתקופה. אני מעדיפה להגיד לך את זה מראש ולא למכור לך &quot;לנצח&quot;."),
 ],
 "התאמה": [FAQ_ITEMS[1], FAQ_ITEMS[4],
   ("יש לי עור כהה — זה מתאים?","כן. המכשיר מאפשר התאמת פרמטרים לגוונים שונים. בטסט אני בודקת את סוג העור שלך ומתאימה בהתאם."),
   ("בהיריון או בהנקה?","בהיריון אני לא מטפלת. בהנקה — נדבר, זה תלוי באזור. בכל מקרה, אם את בתהליך רפואי כלשהו או נוטלת תרופות, חשוב שתעדכני אותי בטסט."),
   ("זה מתאים לגברים?","בהחלט. גב, חזה, כתפיים, קו זקן. אותו מכשיר, אותה שיטה, אותה דיסקרטיות."),
   ("מגיל כמה אפשר?","אני מטפלת בנערות מגיל 16, בליווי ובאישור הורה. הרבה מהלקוחות הצעירות שלי מגיעות בהפניה של אמא שכבר מטופלת אצלי."),
 ],
 "לפני ואחרי": [
   ("איך מתכוננים לטיפול?","לגלח את האזור יום לפני — לא שעווה, לא פינצטה, לא אפילציה. צריך שהזקיק יישאר במקומו. בנוסף, להימנע מחשיפה לשמש ומשיזוף מלאכותי כשבועיים לפני, ולהגיע בלי קרם או דאודורנט על האזור."),
   ("מה עושים אחרי?","אודם קל למשך כמה שעות זה נורמלי. להימנע משמש ישירה, סאונה ובריכה 48 שעות, להשתמש בקרם הרגעה ובמקדם הגנה, ולא לגלח עד שאני אומרת. הכול נמסר גם בכתב בסוף כל טיפול."),
   ("אפשר להתאמן אחרי?","עדיף לחכות 24 שעות — הזעה על עור שעבר טיפול עלולה לגרות אותו."),
 ],
 "לוגיסטיקה": [
   ("איפה הקליניקה?","בגבעת שמואל. אם את מהאזור — זה קרוב. אם את רחוקה יותר, כדאי שנבדוק ביחד שזה מסתדר לך לוגיסטית, כי סדרת טיפולים דורשת הגעה קבועה לאורך כמה חודשים."),
   ("אני שומרת שבת או מחפשת מטפלת אישה בלבד","הטיפול הוא אצלי בלבד — אישה, בקליניקה פרטית ודיסקרטית. יש לי לקוחות רבות מהקהילה הדתית באזור ואני מכירה את הרגישויות. אפשר לתאם שעה שנוחה לך."),
   ("מה קורה אם אני צריכה לבטל?","פשוט תודיעי לי מראש ונמצא תאריך אחר. אני מבקשת הודעה של 24 שעות לפחות, כדי שאוכל לתת את התור למישהי אחרת."),
   ('יש חניה? מה שעות הפעילות?','פרטי החניה ושעות הפעילות המלאות מופיעים בעמוד <a href="contact.html" style="border-bottom:1px solid var(--gold)">צור קשר</a>.'),
 ],
}

def faq_page_body():
    out = []
    for i, (group, items) in enumerate(FAQ_FULL.items()):
        out.append("""<section class="section wrap faq%s">
  <div class="rv"><p class="eyebrow">%02d</p><h2>%s</h2></div>
  <div class="acc rv rv-d1">%s</div>
</section>""" % (" sand" if i % 2 else "", i + 1, group, acc(items)))
    return "\n".join(out)

FAQPAGE = phead("שאלות ותשובות", "בלי סימני שאלה",
  "כל מה שרצית<br><em class='serif-it'>לדעת לפני</em>",
  "ריכזתי כאן את מה שהכי שואלים אותי. ענית לעצמך על הכול ועדיין יש שאלה? כתבי לי בוואטסאפ — אני עונה בעצמי, לא בוט.", cta=False) \
  + faq_page_body() + closer("נשארה לך שאלה?", "כתבי לי בוואטסאפ ואענה בעצמי.")

# ===================== גלריה =====================
GALLERY = phead("גלריה", "בלי סטוק, בלי פילטרים",
  "רגעים<br><em class='serif-it'>מהקליניקה</em>",
  "תוצאות אמיתיות, המכשור, והמקום שאליו את מגיעה. כל תמונת לקוחה מפורסמת בהסכמה בכתב.", cta=False) + """
<section class="section wrap">
  <div class="rv" style="max-width:620px;margin-bottom:34px"><p class="eyebrow">01</p><h2>לפני ואחרי</h2></div>
  <div class="grid-g rv rv-d1">%(gallery_full)s</div>
</section>

<section class="section sand wrap">
  <div class="rv" style="max-width:620px;margin-bottom:34px"><p class="eyebrow">02</p><h2>המכשור</h2>
    <p class="lead" style="margin-top:16px">InMode Optimas. זה מה שעומד מאחורי ההבדל בתוצאה.</p></div>
  <div class="grid-g rv rv-d1">%(gear)s</div>
</section>

<section class="section dark wrap">
  <div class="rv" style="max-width:620px;margin-bottom:34px"><p class="eyebrow on-dark">03</p><h2>וידאו מהקליניקה</h2>
    <p class="lead" style="margin-top:16px">כי חלק מהדברים פשוט צריך לראות בתנועה.</p></div>
  <div class="vid-grid rv rv-d1">
    <figure class="vid" style="margin:0"><video src="assets/video/clip-1.mp4" controls preload="metadata" playsinline></video><figcaption>מהקליניקה</figcaption></figure>
    <figure class="vid" style="margin:0"><video src="assets/video/clip-2.mp4" controls preload="metadata" playsinline></video><figcaption>מהקליניקה</figcaption></figure>
  </div>
</section>

<section class="section wrap">
  <div class="rv" style="max-width:620px;margin-bottom:34px"><p class="eyebrow">04</p><h2>הקליניקה</h2>
    <p class="lead" style="margin-top:16px">כדי שתדעי לאן את מגיעה עוד לפני שהגעת.</p></div>
  <div class="grid-g rv rv-d1">%(clinic)s</div>
</section>
""" + closer("רוצה לראות את זה במו עינייך?", "בואי לטסט חינם — תכירי את המקום, את המכשיר ואותי.")

# ===================== צור קשר =====================
CONTACT = phead("צור קשר", "הצעד הראשון קטן",
  "בואי לבדוק.<br><em class='serif-it'>בלי להתחייב.</em>",
  "משאירה פרטים ואני חוזרת אלייך אישית — לא מוקד, לא נציג. אני.", cta=False) + """
<section class="section dark wrap contact">
  <div>
    <p class="eyebrow on-dark rv">מה קורה אחר כך</p>
    <h2 class="rv rv-d1">ארבעה שלבים,<br><em class="serif-it">בקצב שלך.</em></h2>
    <div class="rv rv-d2" style="margin-top:34px">
      <div class="step"><em>01</em><p><strong>וואטסאפ תוך דקה</strong>הודעה אישית ממני עם סרטון קצר על איך אני עובדת ולמה זה שונה</p></div>
      <div class="step"><em>02</em><p><strong>שיחה תוך 24 שעות</strong>להבין מה מפריע ומה ניסית עד היום — בלי לחץ מכירה</p></div>
      <div class="step"><em>03</em><p><strong>טסט אישי בקליניקה</strong>צילום האזור, בדיקת זקיק השערה, הדגמה ותוכנית אישית עם מחיר שקוף</p></div>
      <div class="step"><em>04</em><p><strong>החלטה בנחת</strong>רק אם מתאים — מתחילות. בלי שאף אחד ינשוף בעורף.</p></div>
    </div>
  </div>
  %(form)s
</section>

<section class="section wrap">
  <div class="two">
    <div class="rv">
      <p class="eyebrow">פרטי הקליניקה</p>
      <h2>איפה אנחנו</h2>
      <table class="tbl" style="margin-top:26px">
        <tr><td>כתובת</td><td>גבעת שמואל<br><span style="color:var(--muted)">רחוב ומספר — להשלמה</span></td></tr>
        <tr><td>טלפון</td><td><a href="%(tel)s" style="border-bottom:1px solid var(--gold)">%(phone)s</a></td></tr>
        <tr><td>וואטסאפ</td><td><a href="%(wa)s" style="border-bottom:1px solid var(--gold)">שליחת הודעה ל-%(phone)s</a></td></tr>
        <tr><td>מייל</td><td><a href="mailto:%(mail)s" style="border-bottom:1px solid var(--gold)">%(mail)s</a></td></tr>
        <tr><td>פייסבוק</td><td><a href="%(fb)s" target="_blank" rel="noopener" style="border-bottom:1px solid var(--gold)">רויטל קיילי בפייסבוק</a></td></tr>
        <tr><td>שעות</td><td>א׳–ה׳ 09:00–20:00<br>ו׳ 09:00–13:00</td></tr>
        <tr><td>חניה</td><td><span style="color:var(--muted)">להשלמה</span></td></tr>
        <tr><td>נגישות</td><td><span style="color:var(--muted)">להשלמה</span></td></tr>
      </table>
    </div>
    <div class="rv rv-d1">
      <div class="frame" style="aspect-ratio:4/3;border-radius:var(--r-lg);overflow:hidden;position:relative;background:var(--sand-deep)">
        <div class="ph"><b>מפה — Google Maps</b><small>להטמעה עם הכתובת המדויקת</small></div>
      </div>
      <div class="callout">
        <strong>שאלה קטנה לפני?</strong>
        <p>לא חייבים טופס. כתבי לי בוואטסאפ — אני עונה בעצמי.</p>
        <p style="margin:0"><a class="link-u" href="%(wa)s">לוואטסאפ של רויטל <span>←</span></a></p>
      </div>
    </div>
  </div>
</section>
"""

# ===================== עמודי מדיניות =====================
PRIVACY = phead("מדיניות פרטיות", "השקיפות שלנו",
  "מדיניות<br><em class=\'serif-it\'>פרטיות</em>",
  "מה אנחנו אוספים, למה, וכמה זמן זה נשמר. בלי אותיות קטנות.", cta=False) + """
<section class="section wrap two">
  <div class="rv">
    <p class="eyebrow">עדכון אחרון</p>
    <p class="lead">ספטמבר 2026</p>
    <p style="color:var(--muted);font-size:14.5px;margin-top:26px">שאלה על הפרטיות שלך? כתבי לי ל־<a href="mailto:%(mail)s" style="border-bottom:1px solid var(--gold)">%(mail)s</a></p>
  </div>
  <div class="prose rv rv-d1">
    <h3>מי אנחנו</h3>
    <p>האתר מופעל על ידי רויטל קיילי, קליניקה לאסתטיקה בגבעת שמואל. לכל פנייה בנושא פרטיות: %(mail)s או %(phone)s.</p>

    <h3>איזה מידע נאסף</h3>
    <ul>
      <li><strong>מידע שאת מוסרת מרצונך</strong> — שם, טלפון, וסוג הטיפול שמעניין אותך, דרך טופס יצירת הקשר או בוט בדיקת ההתאמה.</li>
      <li><strong>מידע טכני</strong> — סוג הדפדפן, סוג המכשיר, ודפים שנצפו. נאסף בצורה מצטברת ואנונימית לצורך שיפור האתר.</li>
      <li><strong>מידע רפואי־אסתטי</strong> — נאסף רק בקליניקה עצמה, במסגרת האבחון, ולעולם לא דרך האתר.</li>
    </ul>

    <h3>למה המידע משמש</h3>
    <ul>
      <li>יצירת קשר חוזר ותיאום טסט אבחון</li>
      <li>התאמת המלצת הטיפול לצרכים שציינת</li>
      <li>שיפור האתר והשירות</li>
    </ul>
    <div class="callout">
      <strong>מה לא נעשה עם המידע</strong>
      <p>הפרטים שלך לא נמכרים, לא מושכרים ולא מועברים לצד שלישי למטרות שיווק. נקודה.</p>
    </div>

    <h3>העברה לצדדים שלישיים</h3>
    <p>המידע עשוי לעבור לספקי שירות שמסייעים בהפעלת הקליניקה — מערכת ניהול לקוחות, שירות דיוור, ספק אחסון האתר — וזאת רק לצורך מתן השירות ובכפוף להתחייבותם לשמירת סודיות. בנוסף, נעביר מידע אם נחויב לכך על פי דין.</p>

    <h3>כמה זמן נשמר המידע</h3>
    <p>פרטי פנייה שלא הבשילה לטיפול נשמרים עד 24 חודשים. פרטי לקוחות שקיבלו טיפול נשמרים כל עוד נדרש לצורך המשך הליווי ובהתאם לחובות שבדין.</p>

    <h3>עוגיות (Cookies)</h3>
    <p>האתר עשוי לעשות שימוש בעוגיות לצורך תפעול תקין ומדידת שימוש. אפשר לחסום עוגיות בהגדרות הדפדפן; חלק מהפונקציות עשויות להיפגע כתוצאה מכך.</p>

    <h3>הזכויות שלך</h3>
    <p>לפי חוק הגנת הפרטיות, התשמ״א־1981, יש לך זכות לעיין במידע שנאסף עלייך, לבקש את תיקונו, ולבקש את מחיקתו. פנייה בכתב ל־%(mail)s תטופל תוך זמן סביר.</p>

    <h3>אבטחת מידע</h3>
    <p>אנחנו נוקטים אמצעים סבירים לאבטחת המידע. עם זאת, אף מערכת אינה חסינה לחלוטין, ולכן איננו יכולים להתחייב לאבטחה מוחלטת.</p>

    <h3>שינויים במדיניות</h3>
    <p>מדיניות זו עשויה להתעדכן. תאריך העדכון האחרון מופיע בראש העמוד.</p>
  </div>
</section>
"""

ACCESS = phead("הצהרת נגישות", "לכולן ולכולם",
  "הצהרת<br><em class=\'serif-it\'>נגישות</em>",
  "האתר נבנה כך שיהיה שמיש עבור מגוון רחב של משתמשים, כולל אנשים עם מוגבלות.", cta=False) + """
<section class="section wrap two">
  <div class="rv">
    <p class="eyebrow">נתקלת בבעיה?</p>
    <h2>ספרי לי<br><em class="serif-it">ואתקן.</em></h2>
    <p class="lead" style="margin-top:20px">אם נתקלת בקושי בגלישה, בתוכן שלא נגיש לך, או בכל דבר שמונע ממך להשתמש באתר — אשמח לדעת ולטפל.</p>
    <table class="tbl" style="margin-top:24px">
      <tr><td>רכזת נגישות</td><td>רויטל קיילי</td></tr>
      <tr><td>טלפון</td><td><a href="%(tel)s" style="border-bottom:1px solid var(--gold)">%(phone)s</a></td></tr>
      <tr><td>מייל</td><td><a href="mailto:%(mail)s" style="border-bottom:1px solid var(--gold)">%(mail)s</a></td></tr>
      <tr><td>זמן טיפול</td><td>עד 14 ימי עסקים</td></tr>
    </table>
  </div>
  <div class="prose rv rv-d1">
    <h3>מה נעשה באתר</h3>
    <ul>
      <li>מבנה סמנטי תקין — כותרות היררכיות, אזורי ניווט מסומנים, וטקסט חלופי לתמונות</li>
      <li>ניווט מלא במקלדת, עם סימון ברור של האלמנט הממוקד</li>
      <li>ניגודיות צבע שנבדקה מול הרקעים, כולל טקסט מעל תמונות</li>
      <li>טפסים עם תוויות מקושרות ושדות חובה מסומנים</li>
      <li>כיבוד ההגדרה <span dir="ltr">prefers-reduced-motion</span> — למי שהגדיר במערכת ההפעלה צמצום תנועה, האנימציות באתר מבוטלות</li>
      <li>התאמה לגדלי מסך שונים ולהגדלת טקסט</li>
      <li>וידאו מתנגן ללא סאונד, ולא מופעל אוטומטית בלי הקשר</li>
    </ul>

    <h3>רמת הנגישות</h3>
    <p>האתר נבנה בהתאם להנחיות <span dir="ltr">WCAG 2.1</span> ברמה AA, ובהתאם לתקן הישראלי ת״י 5568 ולתקנות שוויון זכויות לאנשים עם מוגבלות (התאמות נגישות לשירות), התשע״ג־2013.</p>

    <h3>מגבלות ידועות</h3>
    <p>חלק מהתכנים באתר הם צילומים שהתקבלו מלקוחות, וייתכן שהתיאור החלופי שלהם אינו ממצה. אנחנו משפרים אותם באופן שוטף. אם נתקלת בתוכן שאינו נגיש — נשמח שתעדכני אותנו.</p>

    <h3>נגישות הקליניקה עצמה</h3>
    <p>פרטי הנגישות הפיזית של הקליניקה — כניסה, חניה ושירותים — יפורסמו כאן בקרוב. עד אז, מוזמנת להתקשר ולשאול לפני ההגעה ונשמח לסייע.</p>

    <div class="callout">
      <strong>הצהרה זו עודכנה</strong>
      <p>ספטמבר 2026. הנגישות נבדקת מחדש עם כל שינוי מהותי באתר.</p>
    </div>
  </div>
</section>
"""

TERMS = phead("תנאי שימוש", "הכללים",
  "תנאי<br><em class=\'serif-it\'>שימוש</em>",
  "מה מותר, מה אסור, ומה חשוב שתדעי לפני שאת מסתמכת על מה שכתוב כאן.", cta=False) + """
<section class="section wrap two">
  <div class="rv">
    <p class="eyebrow">עדכון אחרון</p>
    <p class="lead">ספטמבר 2026</p>
    <div class="callout" style="margin-top:26px">
      <strong>הכי חשוב</strong>
      <p>שום דבר באתר הזה אינו ייעוץ רפואי ואינו תחליף לאבחון אישי. התאמת טיפול נקבעת רק בקליניקה, פנים מול פנים.</p>
    </div>
  </div>
  <div class="prose rv rv-d1">
    <h3>הסכמה לתנאים</h3>
    <p>השימוש באתר מהווה הסכמה לתנאים אלה. אם אינך מסכימה להם — אנא הימנעי משימוש באתר.</p>

    <h3>התוכן באתר אינו ייעוץ רפואי</h3>
    <p>המידע באתר הוא כללי ומיועד להתרשמות בלבד. הוא אינו מהווה ייעוץ רפואי, אבחון או המלצת טיפול, ואין להסתמך עליו לקבלת החלטות בריאותיות. התאמת טיפול, מספר הטיפולים והתוצאה הצפויה נקבעים אך ורק באבחון אישי בקליניקה.</p>

    <h3>תוצאות טיפול</h3>
    <p>תוצאות טיפולי לייזר ואסתטיקה משתנות מאדם לאדם בהתאם לסוג העור, לצבע ולעובי השיער, למצב הורמונלי ולגורמים נוספים. תמונות ה״לפני ואחרי״ באתר משקפות תוצאות של לקוחות מסוימות ואינן מהוות הבטחה לתוצאה זהה.</p>

    <h3>קניין רוחני</h3>
    <p>כל התכנים באתר — טקסטים, תמונות, סרטונים, לוגו ועיצוב — הם קניינה של רויטל קיילי או של מי שהעניק רישיון לשימוש בהם. אין להעתיק, לשכפל, להפיץ או לעשות בהם שימוש מסחרי ללא אישור בכתב.</p>

    <h3>תמונות לקוחות</h3>
    <p>תמונות וצילומי הודעות של לקוחות מפורסמים באתר בהסכמתן. לקוחה המבקשת להסיר תוכן שלה מוזמנת לפנות ל־%(mail)s ונסיר אותו.</p>

    <h3>קישורים חיצוניים</h3>
    <p>האתר עשוי לכלול קישורים לאתרים ולרשתות חברתיות של צדדים שלישיים. אין לנו שליטה על תוכנם ואיננו אחראים לו.</p>

    <h3>זמינות האתר</h3>
    <p>אנו שואפים לזמינות מלאה, אך איננו מתחייבים לפעילות רציפה וללא תקלות. ייתכנו הפסקות לצורך תחזוקה או מסיבות שאינן בשליטתנו.</p>

    <h3>הגבלת אחריות</h3>
    <p>השימוש באתר הוא באחריותך בלבד. לא נישא באחריות לנזק ישיר או עקיף שייגרם כתוצאה מהסתמכות על תוכן האתר.</p>

    <h3>שינויים בתנאים</h3>
    <p>אנו רשאים לעדכן תנאים אלה מעת לעת. הנוסח המחייב הוא זה המופיע באתר במועד השימוש.</p>

    <h3>דין וסמכות שיפוט</h3>
    <p>על תנאים אלה יחולו דיני מדינת ישראל. סמכות השיפוט הבלעדית נתונה לבתי המשפט המוסמכים במחוז תל אביב.</p>
  </div>
</section>
"""

# ===================== הרכבה =====================
def cell(src, alt, tag=None, cls="g-cell", ph_label=None, ph_note=""):
    inner = ('<img src="%s" alt="%s" loading="lazy">' % (src, alt)) if (src and os.path.exists(src)) \
            else ph(ph_label or alt, ph_note)
    t = '<span class="g-tag">%s</span>' % tag if tag else ''
    return '<div class="%s">%s%s</div>' % (cls, inner, t)

GAL_HOME = "".join([
  cell("assets/ba-jaw.jpg", "לפני ואחרי — הסרת שיער בלייזר בקו הלסת", "לפני / אחרי"),
  cell("assets/ba-cheek-before.jpg", "לחי לפני סדרת טיפולי לייזר", "לפני · 21/11", "g-cell tall"),
  cell("assets/ba-neck-face.jpg", "לפני ואחרי — צוואר ולחי", "לפני / אחרי"),
  '<div class="g-quote">“להרגיש<br><em class="serif-it">נוח בעור שלך</em>”</div>',
  cell("assets/laser-men-back.jpg", "טיפול הסרת שיער בלייזר בגב, בקליניקה", "גם לגברים"),
  cell("assets/ba-armpit.jpg", "לפני ואחרי — בית שחי", "לפני / אחרי"),
])

GAL_FULL = "".join([
  cell("assets/ba-cheek-before.jpg", "לחי — לפני סדרת טיפולים", "לפני · 21/11", "g-cell tall"),
  cell("assets/ba-cheek-after.jpg", "אותה לחי — אחרי סדרת טיפולים", "אחרי · 18/01"),
  cell("assets/ba-jaw.jpg", "לפני ואחרי — קו לסת", "קו לסת"),
  cell("assets/ba-neck-face.jpg", "לפני ואחרי — צוואר ולחי", "צוואר"),
  cell("assets/ba-armpit.jpg", "לפני ואחרי — בית שחי", "בית שחי"),
  cell("assets/ba-face.jpg", "לפני ואחרי — פנים", "פנים"),
  cell("assets/ba-torso.jpg", "תוצאת הסרת שיער בלייזר בחזה ובבטן", "גברים · 4 טיפולים"),
  cell("assets/ba-neck.jpg", "לפני ואחרי — קו עורף", "קו עורף"),
  cell("assets/service-skintags.jpg", "לפני ואחרי — הסרת סרחי עור בצוואר", "סרחי עור"),
  cell("assets/service-plasma.jpg", "לפני ואחרי — הסרת נימים בפנים", "נימים"),
  cell(None, "", "", "g-cell", "לפני / אחרי — רגליים", "להשלמה"),
  cell(None, "", "", "g-cell", "לפני / אחרי — ביקיני", "להשלמה"),
])

GEAR = "".join([
  cell("assets/hero-inmode-leg.jpg", "ידית InMode בטיפול ברגליים", "InMode", "g-cell tall"),
  cell("assets/inmode-gear.jpg", "מגבת InMode ומשקפי מגן", "בקליניקה"),
  cell("assets/laser-men-back.jpg", "טיפול לייזר בגב", "בפעולה"),
  cell("assets/ed-laser.jpg", "ידית הלייזר בטיפול", "בפעולה"),
])

CLINIC = "".join([
  cell("assets/ed-lily-b.jpg", "פרט אווירה מהקליניקה", "אווירה", "g-cell tall"),
  cell("assets/px-glow.jpg", "עור אחיד וזוהר אחרי תהליך טיפולים", "תוצאה"),
  cell("assets/laser-men-back.jpg", "רויטל בטיפול בקליניקה", "בעבודה"),
  cell("assets/about-hands.jpg", "רויטל בעבודה בקליניקה", "מאחורי הקלעים"),
])

WA_WALL = "".join(
  '<figure><img src="assets/wa-%d.jpg" alt="הודעת לקוחה" loading="lazy"></figure>' % i
  for i in range(1, 10) if os.path.exists("assets/wa-%d.jpg" % i))

HERO_FIG  = figure("assets/hero-inmode-leg.jpg", "ידית מכשיר הלייזר InMode בטיפול הסרת שיער ברגליים",
                   "צילום הירו — רויטל בקליניקה", "יחס 4:5 · assets/revital-hero.jpg")
ABOUT_FIG = figure("assets/ed-consult.jpg", "אבחון אישי בקליניקה — בדיקת האזור לפני הטיפול",
                   "פורטרט של רויטל", "יחס 4:5 · assets/revital-portrait.jpg")
PORTRAIT  = figure(None, "", "פורטרט של רויטל", "יחס 4:5 · assets/revital-portrait.jpg")

def frame_ph(label, note="", ratio="16/11"):
    return '<div class="frame" style="aspect-ratio:%s;border-radius:var(--r-lg);overflow:hidden;position:relative;background:var(--sand-deep);margin-top:28px">%s</div>' % (ratio, ph(label, note))

def frame_img(src, alt, label, note="", ratio="16/11"):
    if os.path.exists(src):
        return '<div class="frame" style="aspect-ratio:%s;border-radius:var(--r-lg);overflow:hidden;position:relative;margin-top:28px"><img src="%s" alt="%s" loading="lazy" style="width:100%%;height:100%%;object-fit:cover"></div>' % (ratio, src, alt)
    return frame_ph(label, note, ratio)


# --- שקופיות ההירו: שני חצאים + כרטיס וידאו במרכז ---
def sc_slide(src, word, first=False):
    w = '<p class="sc-word">%s</p>' % word if word else ''
    pr = 'fetchpriority="high"' if first else 'loading="lazy"'
    return ('<div class="sc-slide%s"><img src="%s" alt="" %s>%s</div>'
            % (' on' if first else '', src, pr, w))

def sc_card(src, first=False, video=False):
    inner = ('<video src="%s" muted loop playsinline preload="metadata" poster="%s"></video>'
             % (src, "assets/ed-laser.jpg")) if video else ('<img src="%s" alt="" loading="lazy">' % src)
    return '<div class="sc-vid%s">%s</div>' % (' on' if first else '', inner)

# חצי ימין (נפתח מהקצה הימני), חצי שמאל (מהקצה השמאלי), והכרטיס המרכזי
SC_R = "".join([
  sc_slide("assets/ed-laser.jpg", "לייזר", first=True),
  sc_slide("assets/px-facial.jpg", "טיפולי פנים"),
  sc_slide("assets/laser-men-back.jpg", "גם לגברים"),
])
SC_L = "".join([
  sc_slide("assets/ed-skin.jpg", "תוצאות", first=True),
  sc_slide("assets/px-care.jpg", "טיפוח"),
  sc_slide("assets/ed-lily-a.jpg", "יחס אישי"),
])
SC_C = "".join([
  sc_card("assets/video/hero-1.mp4", first=True, video=True),
  sc_card("assets/video/hero-2.mp4", video=True),
  sc_card("assets/video/hero-3.mp4", video=True),
])

CTX = {
  "sc_r": SC_R, "sc_l": SC_L, "sc_c": SC_C,
  "wa": WA, "tel": TEL, "phone": PHONE, "mail": MAIL, "fb": FB, "form": FORM, "faq": acc(FAQ_ITEMS), "faq_tags": acc(FAQ_TAGS),
  "hero": HERO_FIG, "about": ABOUT_FIG, "about_portrait": PORTRAIT,
  "gallery": GAL_HOME, "gallery_full": GAL_FULL, "gear": GEAR, "clinic": CLINIC, "wa_wall": WA_WALL,
  "fig_skintags": frame_img("assets/service-skintags.jpg", "לפני ואחרי — הסרת סרחי עור", "טיפול סרחי עור", "assets/skintags-treatment.jpg"),
  "fig_facial":   frame_img("assets/px-facial.jpg", "אבחון וטיפוח עור הפנים", "אבחון עור", "assets/facial-diagnosis.jpg", ratio="4/5"),
  "fig_mask":     frame_img("assets/px-mask.jpg", "מסכת פנים בטיפול", "טיפול פנים", "assets/facial-mask.jpg"),
  "fig_plasma":   frame_img("assets/service-plasma.jpg", "לפני ואחרי — טיפול פלזמה", "טיפול פלזמה", "assets/plasma-treatment.jpg"),
  "fig_clinic":   frame_ph("חלל הקליניקה", "assets/clinic-space.jpg"),
}

PAGES = [
 ("index.html","רויטל קיילי | הסרת שיער בלייזר בגבעת שמואל","קליניקת בוטיק להסרת שיער בלייזר בגבעת שמואל. 12 שנות ניסיון, מכשור InMode Optimas ויחס אישי. טסט אבחון חינם — תראי בעצמך שזה עובד לפני שאת מתחייבת.",HOME),
 ("laser.html","הסרת שיער בלייזר בגבעת שמואל | רויטל קיילי","הסרת שיער בלייזר עם InMode Optimas ו-12 שנות ניסיון. טסט אבחון חינם — צילום האזור ובדיקת זקיק השערה לפני שאת מתחייבת.",LASER),
 ("skin-tags.html","הסרת סרחי עור בגבעת שמואל | רויטל קיילי","הסרת סרחי עור בקליניקה בגבעת שמואל — מהיר, מדויק ובלי ניתוח. אבחון אישי לפני כל טיפול.",SKINTAGS),
 ("facials.html","טיפולי פנים בגבעת שמואל | רויטל קיילי","טיפולי פנים מותאמים אישית בגבעת שמואל — ניקוי עמוק, חידוש עור והבהרה, אחרי אבחון עור אישי.",FACIALS),
 ("treatments.html","טיפולי פלזמה וחידוש עור | רויטל קיילי","טיפולי פלזמה, הידוק עור והסרת נימים בקליניקת בוטיק בגבעת שמואל, אחרי אבחון אישי.",TREATMENTS),
 ("about.html","על רויטל קיילי | קליניקת בוטיק בגבעת שמואל","12 שנות ניסיון בקוסמטיקה, מכשור InMode Optimas וקליניקת בוטיק בגבעת שמואל. הכירי את רויטל ואת דרך העבודה שלה.",ABOUT),
 ("testimonials.html","המלצות לקוחות | רויטל קיילי","מה מספרות הלקוחות של רויטל קיילי — סיפורים, הודעות אמיתיות ותמונות לפני ואחרי מקליניקת הלייזר בגבעת שמואל.",TESTIMONIALS),
 ("faq.html","שאלות ותשובות על הסרת שיער בלייזר | רויטל קיילי","כמה טיפולים, אם זה כואב, מה עם שיער בהיר, ולמה מכשור משנה. תשובות כנות מרויטל קיילי.",FAQPAGE),
 ("gallery.html","גלריה | קליניקת רויטל קיילי, גבעת שמואל","תוצאות לפני ואחרי, המכשור והקליניקה של רויטל קיילי בגבעת שמואל.",GALLERY),
 ("contact.html","צור קשר | רויטל קיילי, גבעת שמואל","לתיאום טסט אבחון חינם בקליניקה של רויטל קיילי בגבעת שמואל. משאירים פרטים ורויטל חוזרת אישית תוך 24 שעות.",CONTACT),
 ("privacy.html","מדיניות פרטיות | רויטל קיילי","איזה מידע נאסף באתר של רויטל קיילי, למה הוא משמש, כמה זמן הוא נשמר ומה הזכויות שלך.",PRIVACY),
 ("accessibility.html","הצהרת נגישות | רויטל קיילי","הצהרת הנגישות של אתר רויטל קיילי — מה נעשה, לפי איזה תקן, ואיך לדווח על בעיה.",ACCESS),
 ("terms.html","תנאי שימוש | רויטל קיילי","תנאי השימוש באתר רויטל קיילי, לרבות הבהרה שהתוכן אינו ייעוץ רפואי.",TERMS),
]

if __name__ == "__main__":
    print("בונה עמודים:")
    for name, title, desc, tpl in PAGES:
        write(name, title, desc, tpl % CTX)
    print("הושלם.")
