/* רויטל קיילי — התנהגות משותפת */
document.documentElement.setAttribute('dir','rtl');
document.documentElement.setAttribute('lang','he');

/* ---- כותרת דביקה ---- */
const hdr=document.querySelector('.hdr');
if(hdr){const onScroll=()=>hdr.classList.toggle('stuck',scrollY>24);onScroll();addEventListener('scroll',onScroll,{passive:true})}

/* ---- תפריט מובייל ---- */
const burger=document.querySelector('.burger'),mnav=document.querySelector('.mnav');
if(burger&&mnav){
  burger.addEventListener('click',()=>{
    const open=mnav.classList.toggle('open');
    burger.setAttribute('aria-expanded',open);
    document.body.style.overflow=open?'hidden':'';
  });
  mnav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{
    mnav.classList.remove('open');burger.setAttribute('aria-expanded','false');document.body.style.overflow='';
  }));
}

function initPage(root){
root=root||document;

/* ---- חשיפה בגלילה ----
   כל מה שנמצא במסך הראשון נחשף מיד, כדי שהדף יהיה קריא בפריים הראשון.
   השאר נחשף בגלילה. */
const revealables=[...root.querySelectorAll('.rv,.wipe,.lines')];
const io=new IntersectionObserver(es=>es.forEach(e=>{
  if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}
}),{threshold:.01,rootMargin:'0px 0px -6% 0px'});
function primeAboveFold(){
  revealables.forEach(el=>{
    if(el.classList.contains('in'))return;
    if(el.getBoundingClientRect().top < innerHeight*0.92){el.classList.add('in');io.unobserve(el)}
  });
}
revealables.forEach(el=>io.observe(el));
requestAnimationFrame(primeAboveFold);
addEventListener('load',primeAboveFold);

/* ---- קו הלייזר: גיבוי ל-JS בדפדפנים בלי scroll timeline ---- */
const beam=document.querySelector('.beam i');
if(beam&&!CSS.supports('animation-timeline','scroll()')){
  const draw=()=>{
    const max=document.documentElement.scrollHeight-innerHeight;
    beam.style.transform='scaleY('+(max>0?Math.min(1,scrollY/max):0)+')';
  };
  draw();addEventListener('scroll',draw,{passive:true});addEventListener('resize',draw);
}

/* ---- סליידר עדויות ---- */
const stories=[...root.querySelectorAll('.story')];
if(stories.length){
  let si=0;const go=i=>{si=(i+stories.length)%stories.length;stories.forEach((s,n)=>s.classList.toggle('on',n===si))};
  const nx=root.querySelector('.ctrls .next'),pv=root.querySelector('.ctrls .prev');
  if(nx)nx.addEventListener('click',()=>go(si+1));
  if(pv)pv.addEventListener('click',()=>go(si-1));
  let timer=setInterval(()=>go(si+1),7500);
  const slider=root.querySelector('.story-wrap');
  if(slider){slider.addEventListener('mouseenter',()=>clearInterval(timer));
    slider.addEventListener('mouseleave',()=>{timer=setInterval(()=>go(si+1),7500)})}
}

/* ---- טפסים ---- */
root.querySelectorAll('form.form').forEach(f=>f.addEventListener('submit',e=>{
  e.preventDefault();
  const ok=f.querySelector('.ok');if(ok)ok.classList.add('on');
  const b=f.querySelector('button[type=submit]');if(b)b.innerHTML='<span>נשלח ✓</span>';
}));

}
initPage(document);
window.RK={initPage:initPage};

/* ---- בוט האבחון (פעם אחת לכל הדף) ---- */
(function(){
  const ov=document.getElementById('ov');if(!ov)return;
  const body=document.getElementById('bot-body'),bar=document.querySelector('.bar i');
  const lead={};let step=0;

  const STEPS=[
    {q:'היי! כמה שאלות קצרות ואני אגיד לך אם הטיפול מתאים לך — ומה ריאלי לצפות. לוקח פחות מדקה 🙂',
     t:'קודם כול, מה הכי מתאר אותך?',k:'segment',
     o:[['אמא — מחפשת גם לעצמי וגם לבת שלי','mom'],['מתחתנת בקרוב','bride'],['לפני גיוס / תחילת לימודים','army'],
        ['ניסיתי לייזר בעבר ולא ראיתי תוצאה','failed'],['פשוט נמאס לי לגלח','tired'],['אני גבר','man']]},
    {t:'איזה אזור הכי מפריע לך?',k:'area',
     o:[['רגליים','x'],['בית שחי','x'],['ביקיני','x'],['פנים','x'],['גב / חזה','x'],['כמה אזורים','x']]},
    {t:'מה צבע השיער באזור הזה?',k:'hair',
     o:[['כהה / חום / שחור','x'],['בלונדיני / ג׳ינג׳י / לבן / בהיר מאוד','OUT_HAIR']]},
    {t:'הקליניקה בגבעת שמואל, וסדרת טיפולים דורשת הגעה קבועה. מסתדר לך להגיע?',k:'geo',
     o:[['כן, אין בעיה','x'],['אני קרובה, נראה לי שכן','x'],['זה רחוק לי מדי','OUT_GEO']]},
    {t:'ואחרונה — מה הכי נכון לגבייך?',k:'intent',
     o:[['מחפשת תוצאה אמיתית ומוכנה להשקיע בשביל זה','x'],['רוצה קודם להבין כמה זה עולה ואז להחליט','x'],
        ['מחפשת בעיקר את המחיר הזול ביותר','SOFT']]}
  ];
  const OUTCOMES={
    mom:'הרבה אמהות מגיעות בדיוק כמוך — מטפלות בעצמן, ואחרי כמה טיפולים מביאות גם את הבת. בטסט החינם רויטל תבדוק את זקיק השערה שלך ותגיד לך תוך כמה זמן ריאלי גם את וגם הבת שלך תוכלו להפסיק להתעסק עם גילוח יומיומי — עם מספר טיפולים מדויק, לא הערכה באוויר.',
    bride:'יש לך תאריך — ולכן חשוב לתכנן נכון. בטסט החינם רויטל תבדוק את השיער שלך ותגיד לך בדיוק כמה טיפולים אפשר להספיק עד החתונה ומה התוצאה הריאלית עד אז. בלי הבטחות באוויר.',
    army:'עדיף להגיע לשם מסודרת. בטסט החינם רויטל תגיד לך תוך כמה זמן אפשר לפתור את נושא הגילוח לפני שהשגרה שלך משתנה, וכמה טיפולים זה דורש.',
    failed:'אני שומעת את זה כל יום, ורוב הסיכויים שהבעיה לא הייתה בך אלא במכשור. רויטל עובדת עם InMode Optimas — אחד ממכשירי הלייזר החזקים בעולם. בטסט החינם היא תבדוק את הזקיק שלך ותראה לך בפועל את ההבדל, לפני שאת משלמת שקל.',
    tired:'אז בואי נראה מה אפשר לעשות עם זה. בטסט החינם רויטל מצלמת את האזור, בודקת את זקיק השערה, ואומרת לך כמה טיפולים את צריכה ותוך כמה זמן. בלי עלות ובלי התחייבות.',
    man:'רויטל מטפלת גם בגברים — גב, חזה, כתפיים וקו זקן, בקליניקה פרטית ודיסקרטית. בטסט החינם היא תבדוק את האזור ותגיד לך כמה טיפולים זה דורש ומה ריאלי לצפות.'
  };
  const OUT={
    OUT_HAIR:{e:'🤍',h:'תודה על הכנות',p:'חשוב לי להגיד לך את האמת: שיער בהיר, בלונדיני או לבן לא מגיב טוב לטיפולי לייזר, כי אין בו מספיק פיגמנט שהלייזר יכול לפעול עליו. אני מעדיפה להגיד לך את זה עכשיו מאשר שתשקיעי כסף במשהו שלא יעבוד. אם בכל זאת תרצי להתייעץ — מוזמנת לכתוב לרויטל בוואטסאפ.'},
    OUT_GEO:{e:'🤍',h:'מבינה לגמרי',p:'סדרת לייזר דורשת הגעה קבועה אחת לכמה שבועות, ולא בא לי שתתחילי משהו שיהיה לך קשה להתמיד בו. אם תמצאי את עצמך באזור — הדלת פתוחה.'},
    SOFT:{e:'✦',h:'אני מכבדת את זה לגמרי',p:'חשוב לי רק לומר בשקיפות: אצל רויטל המחיר משקף מכשור מקצועי מהמובילים בעולם ועבודה איטית ומדויקת, ולכן זה לא המקום הכי זול. אם בכל זאת בא לך לראות את ההבדל במו עינייך — הטסט בכל מקרה חינם.',cta:true}
  };

  const open=()=>{step=0;render();ov.classList.add('on');document.body.style.overflow='hidden'};
  const close=()=>{ov.classList.remove('on');document.body.style.overflow=''};
  document.addEventListener('click',e=>{if(e.target.closest('.open-bot'))open()});
  ov.querySelector('.bot-x').addEventListener('click',close);
  ov.addEventListener('click',e=>{if(e.target===ov)close()});
  addEventListener('keydown',e=>{if(e.key==='Escape'&&ov.classList.contains('on'))close()});

  function render(){
    const s=STEPS[step];
    bar.style.width=Math.round(step/(STEPS.length+1)*100)+'%';
    body.innerHTML=(s.q?`<div class="bub">${s.q}</div>`:'')+
      `<h3>${s.t}</h3><div class="opts">${s.o.map(o=>`<button data-v="${o[1]}">${o[0]}</button>`).join('')}</div>`;
    body.querySelectorAll('.opts button').forEach(b=>b.addEventListener('click',()=>{
      lead[s.k]=b.textContent;
      const v=b.dataset.v;
      if(OUT[v])return renderOut(OUT[v],v);
      step++; step<STEPS.length?render():result();
    }));
  }
  function renderOut(o){
    bar.style.width='100%';
    body.innerHTML=`<div class="bot-out"><div class="em">${o.e}</div><h3>${o.h}</h3><p style="color:var(--muted);max-width:none">${o.p}</p>`+
      (o.cta?'<button class="btn" id="go"><span>רוצה לראות בכל זאת</span><span class="arw">←</span></button>'
           :'<a class="btn btn-ghost" href="https://wa.me/972549462663"><span>לוואטסאפ של רויטל</span></a>')+'</div>';
    const g=document.getElementById('go');
    if(g)g.addEventListener('click',()=>{step=STEPS.length;result()});
  }
  function result(){
    bar.style.width='100%';
    const key=(STEPS[0].o.find(o=>o[0]===lead.segment)||[,'tired'])[1];
    body.innerHTML=`<div class="bub">${OUTCOMES[key]||OUTCOMES.tired}</div>
      <h3>רק תשאירי פרטים ורויטל תחזור אלייך אישית</h3>
      <form id="bf"><input name="name" placeholder="שם מלא" required><input name="phone" type="tel" placeholder="טלפון" required>
      <button class="btn" type="submit"><span>שלחי — ורויטל תחזור אלייך</span><span class="arw">←</span></button></form>
      <p class="note" style="margin-top:12px">הפרטים שלך נשארים אצלנו. בלי ספאם ובלי לחץ.</p>`;
    document.getElementById('bf').addEventListener('submit',e=>{
      e.preventDefault();
      body.innerHTML='<div class="bot-out"><div class="em">✓</div><h3>קיבלנו!</h3><p style="color:var(--muted);max-width:none">שולחת לך עכשיו הודעת וואטסאפ עם סרטון קצר מרויטל.</p></div>';
    });
  }
})();

/* ---- לוח השירותים בעמוד הבית ---- */
window.RK.initServices=function(root){
  root=root||document;
  const panel=root.querySelector('#svc-panel');if(!panel)return;
  const S={
    laser:{n:'01',img:'assets/laser-men-back.jpg',alt:'טיפול הסרת שיער בלייזר עם מכשיר InMode',
      h:'לייזר שמתחיל בהתאמה, לא בהבטחה.',href:'laser.html',
      p:'אבחון סוג העור והשיער, טסט מקדים ובניית תוכנית ברורה עם InMode Optimas. עבודה איטית ומדויקת, אזור אחר אזור — בלי לדלג ובלי למהר.',
      li:['התאמה אישית לאזור, לגוון העור ולעובי השיער','מספר טיפולים ריאלי, לא מספר שנשמע טוב במכירה','לנשים ולגברים, בכל אזורי הגוף והפנים','רויטל איתך בכל מפגש']},
    tags:{n:'02',img:'assets/service-skintags.jpg',alt:'לפני ואחרי — הסרת סרחי עור בצוואר',
      h:'סרחי עור — מהר, מדויק ובלי דרמה.',href:'skin-tags.html',
      p:'גדילי עור קטנים בצוואר, בבתי השחי ובאזורי חיכוך. שפירים לגמרי — אבל נתקעים בשרשרת, נחתכים בגילוח ופשוט מציקים. הסרה בטיפול קצר.',
      li:['אבחון לפני כל טיפול — ומה שלא אופייני נשלח לרופא עור','15-30 דקות, לרוב בפגישה אחת','חזרה מיידית לשגרה','הנחיות ברורות לטיפול אחרי']},
    face:{n:'03',img:'assets/ba-neck-face.jpg',alt:'לפני ואחרי — שיפור מרקם וגוון עור הפנים',
      h:'טיפולי פנים שמותאמים לעור שלך — לא לתבנית.',href:'facials.html',
      p:'אין טיפול פנים אחד שמתאים לכולן. מתחילות מאבחון עור — סוג, לחות, רגישויות, פיגמנטציה והרגלי טיפוח — ורק אז מחליטות מה עושים, ומה לא.',
      li:['ניקוי עור עמוק','חידוש והבהרת עור','טיפול לעור רגיש או עם נטייה לאקנה','הדרכת טיפוח לבית']},
    more:{n:'04',img:'assets/service-plasma.jpg',alt:'מכשור InMode ומשקפי מגן בקליניקה',
      h:'טיפולים נלווים — ההמשך הטבעי של התהליך.',href:'treatments.html',
      p:'פלזמה, הידוק וחידוש עור, והסרת נימים. טיפולים משלימים שנקבעים אחרי אבחון אישי ולא מתוך קטלוג.',
      li:['פלזמה לחידוש והידוק','שיפור מרקם וגוון','הסרת נימים מורחבים','ללא הזרקות — רק מה שאני מומחית בו']}
  };
  function draw(k){
    const s=S[k];
    panel.innerHTML=
      `<div class="frame"><img src="${s.img}" alt="${s.alt}" loading="lazy" onerror="this.parentElement.innerHTML='&lt;div class=\\'ph\\'&gt;&lt;b&gt;${s.alt}&lt;/b&gt;&lt;/div&gt;'"></div>
       <div class="svc-body"><p class="eyebrow" style="margin-bottom:14px">${s.n}</p>
       <h4>${s.h}</h4><p style="color:var(--muted)">${s.p}</p>
       <ul>${s.li.map(x=>`<li>${x}</li>`).join('')}</ul>
       <a class="link-u" href="${s.href}">לעמוד המלא <span>←</span></a></div>`;
  }
  draw('laser');
  root.querySelectorAll('.svc-item').forEach(b=>b.addEventListener('click',()=>{
    root.querySelectorAll('.svc-item').forEach(x=>x.setAttribute('aria-selected','false'));
    b.setAttribute('aria-selected','true');draw(b.dataset.s);
  }));
};
window.RK.initServices(document);
