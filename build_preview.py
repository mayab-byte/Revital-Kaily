# -*- coding: utf-8 -*-
"""מאגד את כל העמודים לקובץ אחד עם ניתוב פנימי — לקישור תצוגה."""
import base64, os, re, json

def datauri(path):
    ext = path.rsplit('.', 1)[1].lower()
    mime = 'image/png' if ext == 'png' else 'image/jpeg'
    return 'data:%s;base64,%s' % (mime, base64.b64encode(open(path, 'rb').read()).decode())

PAGES = ["index","laser","skin-tags","facials","treatments","about","testimonials","faq","gallery","contact"]

src = open("index.html", encoding="utf-8").read()
head = src.split("<head>")[1].split("</head>")[0]
title = re.search(r"<title>(.*?)</title>", head, re.S).group(1)
fonts = re.search(r'<link rel="stylesheet" href="https://fonts\.googleapis[^>]*>', head).group(0)

css = open("assets/site.css", encoding="utf-8").read()
js  = open("assets/site.js",  encoding="utf-8").read()

body = src.split("<body>")[1].split("</body>")[0]
chrome_top = body.split("<main>")[0]
chrome_bot = body.split("</main>")[1].replace('<script src="assets/site.js"></script>', "")

mains = {}
for p in PAGES:
    h = open(p + ".html", encoding="utf-8").read()
    mains[p] = h.split("<main>")[1].split("</main>")[0]

out = ("<title>%s</title>\n%s\n<style>%s</style>\n%s<main id=\"app\"></main>\n%s\n"
       "<script>window.__PAGES__=%s;</script>\n<script>%s</script>\n<script>%s</script>"
       % (title, fonts, css, chrome_top, chrome_bot,
          json.dumps(mains, ensure_ascii=False), js, """
/* ניתוב פנימי לגרסת התצוגה */
(function(){
  const app=document.getElementById('app');
  const route=()=> (location.hash.replace(/^#\\/?/,'')||'index').replace('.html','');
  function render(){
    const k=route(); const html=window.__PAGES__[k]||window.__PAGES__.index;
    app.innerHTML=html; scrollTo(0,0);
    document.querySelectorAll('.nav a,.mnav a').forEach(a=>{
      const t=(a.getAttribute('href')||'').replace('.html','').replace('#/','');
      a.toggleAttribute('aria-current', t===k);
    });
    window.RK.initPage(app); window.RK.initServices(app);
  }
  // הפניית כל קישור פנימי לניתוב
  document.addEventListener('click',e=>{
    const a=e.target.closest('a[href$=".html"]'); if(!a) return;
    e.preventDefault(); location.hash='/'+a.getAttribute('href').replace('.html','');
  });
  addEventListener('hashchange',render); render();
})();"""))

# הווידאו נשאר קובץ חיצוני — בתצוגה המאוחדת מוצג פלייסהולדר במקומו
out = re.sub(r'<figure class="vid"[^>]*>.*?</figure>',
  '<figure class="vid" style="margin:0;display:grid;place-content:center;text-align:center;gap:8px;color:#9C9186;padding:26px">'
  '<b style="color:#FAF7F1;font-size:17px">וידאו מהקליניקה</b>'
  '<small style="font-size:12px">מתנגן באתר עצמו · assets/video/</small></figure>', out, flags=re.S)

# הטמעת כל הקבצים כ-data URI
for a in sorted(set(re.findall(r'assets/[A-Za-z0-9_\-.]+\.(?:jpg|png)', out))):
    if os.path.exists(a):
        u = datauri(a)
        out = out.replace('"' + a + '"', '"' + u + '"').replace("'" + a + "'", "'" + u + "'")

dst = "/tmp/claude-0/-home-user-Revital-Kaily/552dee46-d387-5df5-98cb-fd0bc32c740f/scratchpad/revital-site.html"
open(dst, "w", encoding="utf-8").write(out)
print("preview:", len(out.encode()) // 1024, "KB ->", dst)
