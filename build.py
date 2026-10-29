#!/usr/bin/env python3
"""Build the Netlify site (dist/) from src/en.html: EN page, UA page, privacy page, redirects."""
import os, re, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = open(os.path.join(ROOT, "src", "en.html"), encoding="utf-8").read()
DIST = os.path.join(ROOT, "dist")
SITE = "https://www.pwglobaltrading.com"

UA = [
 ('<li class="chip tab"><i class="c-silver"></i>Silver</li><li class="chip tab"><i class="c-gold"></i>Gold</li><li class="chip tab"><i class="c-black"></i>Black</li>', '<li class="chip tab"><i class="c-silver"></i>Срібний</li><li class="chip tab"><i class="c-gold"></i>Золотий</li><li class="chip tab"><i class="c-black"></i>Чорний</li>'),
 ('<meta name="description" content="Supplier of aluminium beverage cans and lids: 200–500 ml stock formats from one pallet, custom offset-printed cans from 350,000 units. Shipping to the EU, UK, Ukraine, USA, Canada and the Middle East.">',
  '<meta name="description" content="Постачальник алюмінієвих банок для напоїв і кришок: складські формати 200–500 мл від однієї палети, банки з офсетним друком від 350 000 шт. Доставка в ЄС, Велику Британію, Україну, США, Канаду та на Близький Схід.">'),
 ('<a href="#cans">Cans</a>', '<a href="#cans">Банки</a>'),
 ('<a href="#lids">Lids</a>', '<a href="#lids">Кришки</a>'),
 ('<a href="#print">Custom print</a>', '<a href="#print">Друк</a>'),
 ('<a href="#about">About</a>', '<a href="#about">Про нас</a>'),
 ('<a href="#faq">FAQ</a>\n      <a class="lang" href="et/index.html" hreflang="et" lang="et">ET</a>\n      <a class="lang" href="ua/index.html" hreflang="uk" lang="uk">UA</a>',
  '<a href="#faq">Питання</a>\n      <a class="lang" href="../index.html" hreflang="en" lang="en">EN</a>\n      <a class="lang" href="../et/index.html" hreflang="et" lang="et">ET</a>'),
 ('Request a quote</a>', 'Запит ціни</a>'),
 ('<p class="eyebrow">Beverage cans &amp; lids supplier</p>', '<p class="eyebrow">Постачальник банок і кришок для напоїв</p>'),
 ('<h1>Aluminium cans and lids, from one pallet to full production runs</h1>', '<h1>Алюмінієві банки та кришки від однієї палети до великих виробничих серій</h1>'),
 ('PW Global Trading supplies plain and printed beverage cans and can ends to breweries, drinks producers and co-packers. Stock formats ship within days. Custom-printed cans start at 350,000 units per design.',
  'PW Global Trading постачає банки для напоїв без друку та з друком, а також кришки для пивоварень, виробників напоїв і копакерів. Складські формати відвантажуємо за кілька днів. Банки з вашим дизайном замовляються від 350 000 шт. на один дизайн.'),
 ('<a class="btn btn-ghost" href="#cans">See stock formats</a>', '<a class="btn btn-ghost" href="#cans">Складські формати</a>'),
 ('aria-label="Can formats from 200 ml slim to 500 ml standard"', 'aria-label="Формати банок від 200 мл slim до 500 мл standard"'),
 ('aria-label="Key figures"', 'aria-label="Основні показники"'),
 ('<dt>cans supplied every year</dt><dd>100M+</dd>', '<dt>банок постачаємо щороку</dt><dd>100 млн+</dd>'),
 ('<dt>years in beverage packaging</dt>', '<dt>років у пакуванні для напоїв</dt>'),
 ('<dt>minimum order for stock cans</dt><dd>1 pallet</dd>', '<dt>мінімальне замовлення зі складу</dt><dd>1 палета</dd>'),
 ('<dt>working days to deliver stock in the EU</dt>', '<dt>робочих днів доставки зі складу в ЄС</dt>'),
 ('<p class="eyebrow">Stock cans</p><h2>Formats in our warehouse</h2>', '<p class="eyebrow">Банки зі складу</p><h2>Формати на нашому складі</h2>'),
 ('Plain cans from permanent stock, sold by the full pallet. Mix formats on one delivery. Pallet data below is what arrives at your dock.',
  'Банки без друку з постійного складу, продаються повними палетами. Різні формати можна поєднати в одній поставці. Нижче наведено дані палети, яка приїде до вас.'),
 ('<th>Format</th><th>Finish</th><th class="num">Lid</th><th class="num">Cans per layer</th><th class="num">Layers</th><th class="num">Cans per pallet</th><th class="num">Pallet W × L × H, mm</th>',
  '<th>Формат</th><th>Колір</th><th class="num">Кришка</th><th class="num">Банок у шарі</th><th class="num">Шарів</th><th class="num">Банок на палеті</th><th class="num">Палета Ш × Д × В, мм</th>'),
 ('Stock cans ship with a silver end and silver tab. BPA-NI: internal lining made without bisphenol A. Other formats and finishes on request.', 'Банки зі складу постачаються зі срібною кришкою та срібним язичком. BPA-NI: внутрішнє покриття без бісфенолу А. Інші формати та кольори на запит.'),
 ('<p class="eyebrow">Lids / can ends</p><h2>Lids to match, or on their own</h2>', '<p class="eyebrow">Кришки</p><h2>Кришки до банок або окремо</h2>'),
 ('We supply aluminium ends together with our cans or as a separate order for your filling line. Lids are priced separately from cans.',
  'Постачаємо алюмінієві кришки разом з нашими банками або окремим замовленням для вашої лінії розливу. Кришки оплачуються окремо від банок.'),
 ('<i class="c-silver"></i>Silver</li>', '<i class="c-silver"></i>Срібляста</li>'),
 ('<i class="c-black"></i>Black</li>', '<i class="c-black"></i>Чорна</li>'),
 ('<i class="c-gold"></i>Gold</li>', '<i class="c-gold"></i>Золота</li>'),
 ('<p>For slim cans and 330 ml sleek cans with a 200 neck.</p>', '<p>Для банок slim і банок 330 мл sleek з горлом 200.</p>'),
 ('<p>For 330 ml sleek cans with a 202 neck and standard 330, 440 and 500 ml cans.</p>', '<p>Для банок 330 мл sleek з горлом 202 і стандартних банок 330, 440 і 500 мл.</p>'),
 ('<p>Classic B64 profile for lines set up for this end type.</p>', '<p>Класичний профіль B64 для ліній, налаштованих під цей тип кришки.</p>'),
 ('<p class="eyebrow">Custom print</p>', '<p class="eyebrow">Індивідуальний друк</p>'),
 ('<h2>Your design, printed on the can</h2>', '<h2>Ваш дизайн на банці</h2>'),
 ('Offset-printed cans for brands that have outgrown labels and sleeves. Send your artwork and we take it through production and delivery.',
  'Банки з офсетним друком для брендів, яким уже замало етикеток і sleeve. Надішліть макет, а ми проведемо його через виробництво та доставку.'),
 ('<b>Send artwork and volumes</b><span>Format, finish, quantity per design and delivery country.</span>',
  '<b>Надішліть макет і обсяги</b><span>Формат, оздоблення, кількість на дизайн і країна доставки.</span>'),
 ('<b>Approve the proof</b><span>We check the artwork against the can template before production.</span>',
  '<b>Затвердіть пробу</b><span>Перед виробництвом перевіряємо макет за шаблоном банки.</span>'),
 ('<b>Production and delivery</b><span>Lead time is agreed per order. We arrange transport to your plant.</span>',
  '<b>Виробництво та доставка</b><span>Термін узгоджуємо для кожного замовлення. Організовуємо доставку на ваш завод.</span>'),
 ('<dt>Printing</dt><dd>Offset</dd>', '<dt>Друк</dt><dd>Офсетний</dd>'),
 ('<dt>Finish</dt><dd>Gloss, matt, deep matt or tactile</dd>', '<dt>Оздоблення</dt><dd>Глянець, мат, глибокий мат або тактильний лак</dd>'),
 ('<dt>Formats</dt><dd>200–500 ml, incl. 355 and 473 ml</dd>', '<dt>Формати</dt><dd>200–500 мл, зокрема 355 і 473 мл</dd>'),
 ('<a href="#packaging">Packaging</a>', '<a href="#packaging">Пакування</a>'),
 ('<h3>Tab colours</h3>', '<h3>Кольори язичка</h3>'),
 ('<i class="c-red"></i>Red</li>', '<i class="c-red"></i>Червоний</li>'),
 ('<i class="c-blue"></i>Blue</li>', '<i class="c-blue"></i>Синій</li>'),
 ('<i class="c-green"></i>Green</li>', '<i class="c-green"></i>Зелений</li>'),
 ('<p>A coloured tab picks up your brand colour on the shelf.</p>', '<p>Кольоровий язичок підкреслює колір вашого бренду на полиці.</p>'),
 ('<h3>End and tab marking</h3>', '<h3>Маркування кришки та язичка</h3>'),
 ('<li>Engraved end</li><li>Laser-engraved or embossed tab</li><li>Tab with QR code or promo code</li><li>Punched tab</li>', '<li>Гравіювання на кришці</li><li>Лазерне гравіювання або тиснення на язичку</li><li>Язичок з QR-кодом або промокодом</li><li>Перфорований язичок</li>'),
 ('<p>QR and promo codes under the tab work well for loyalty and promotional campaigns.</p>', '<p>QR-коди та промокоди під язичком добре працюють у програмах лояльності та промоакціях.</p>'),
 ('Sheet thickness 0.218 or 0.222 mm. BPA-NI lining available. Made in DPG and BRC certified plants. Coloured tabs and marking are priced extra and available on request.', 'Товщина листа 0,218 або 0,222 мм. Доступне покриття BPA-NI. Виробництво на заводах із сертифікатами DPG і BRC. Кольорові язички та маркування оплачуються додатково й доступні на запит.'),
 ('<p class="eyebrow">Multipack packaging</p><h2>Shrink packs and trays</h2>', '<p class="eyebrow">Групове пакування</p><h2>Термоусадкова плівка та лотки</h2>'),
 ('Retail-ready multipack formats for filled cans, so your product goes from the filling line straight to the shelf.', 'Готові до роздрібу мультипаки для наповнених банок, щоб ваш продукт ішов з лінії розливу одразу на полицю.'),
 ('<small>pack</small></div><h3>Shrink film</h3><p>Cans wrapped in heat-shrink film.</p>', '<small>шт.</small></div><h3>Термоплівка</h3><p>Банки в термоусадковій плівці.</p>'),
 ('<small>pack</small></div><h3>Shrink film and tray</h3><p>Shrink film on a cardboard tray for extra stability.</p>', '<small>шт.</small></div><h3>Термоплівка та лоток</h3><p>Плівка на картонному лотку для більшої стійкості.</p>'),
 ('<small>pack</small></div><h3>Tray</h3><p>Open cardboard tray for cash-and-carry and HoReCa.</p>', '<small>шт.</small></div><h3>Лоток</h3><p>Відкритий картонний лоток для cash-and-carry та HoReCa.</p>'),
 ('<h3>Finishes</h3>', '<h3>Оздоблення</h3>'),
 ('<b>Gloss</b><span>Intense colour and a shiny, wet look.</span>', '<b>Глянець</b><span>Насичені кольори та блискучий «мокрий» вигляд.</span>'),
 ('<b>Matt</b><span>Soft surface, smooth to the touch.</span>', '<b>Мат</b><span>М\'яка поверхня, гладка на дотик.</span>'),
 ('<b>Deep matt</b><span>A stronger matt effect for a premium feel.</span>', '<b>Глибокий мат</b><span>Посилений матовий ефект для преміального вигляду.</span>'),
 ('<b>Tactile</b><span>Textured varnish you can feel in the hand.</span>', '<b>Тактильний лак</b><span>Фактурний лак, який відчувається в руці.</span>'),
 ('<h3>Special effects</h3>', '<h3>Спецефекти</h3>'),
 ('<b>Duo-Mix</b><span>Two designs in the same colour set, printed in one production run.</span>', '<b>Duo-Mix</b><span>Два дизайни в одній палітрі кольорів, надруковані за одну виробничу серію.</span>'),
 ('<b>High resolution</b><span>Photographic detail for key visuals and limited editions.</span>', '<b>Висока роздільність</b><span>Фотографічна деталізація для ключових візуалів і лімітованих серій.</span>'),
 ('<b>UV ink</b><span>Graphic elements that glow under UV light. Works with gloss, matt or tactile.</span>', '<b>UV-фарба</b><span>Елементи, що світяться в ультрафіолеті. Поєднується з глянцем, матом або тактильним лаком.</span>'),
 ('<b>Thermo ink</b><span>Graphic elements that change colour with temperature.</span>', '<b>Термофарба</b><span>Елементи, що змінюють колір залежно від температури.</span>'),
 ('Finishes other than gloss and all special effects are priced extra and available on request.', 'Оздоблення, крім глянцю, та всі спецефекти оплачуються додатково й доступні на запит.'),
 ('<dt>Minimum order</dt><dd>350,000 cans per design</dd>', '<dt>Мін. замовлення</dt><dd>350 000 банок на дизайн</dd>'),
 ('<dt>Lids</dt><dd>', '<dt>Кришки</dt><dd>'),
 ('<dt>Lead time</dt><dd>Agreed per order</dd>', '<dt>Термін</dt><dd>Узгоджується для замовлення</dd>'),
 ('<p class="eyebrow">About us</p>', '<p class="eyebrow">Про нас</p>'),
 ('A trading partner with stock, volume and logistics', 'Торговий партнер зі складом, обсягами та логістикою'),
 ('PW Global Trading OÜ has worked in beverage packaging and export trading for over ten years. Today we supply more than 100 million cans a year to breweries, beverage producers and co-packers.',
  'PW Global Trading OÜ понад десять років працює в пакуванні для напоїв та експортній торгівлі. Сьогодні ми постачаємо понад 100 мільйонів банок на рік пивоварням, виробникам напоїв і копакерам.'),
 ('We hold plain cans in stock for fast orders, take larger printed runs straight into production, and organise transport door to door with our forwarding partners. One contact handles your order from quote to delivery.',
  'Ми тримаємо банки без друку на складі для швидких замовлень, великі серії з друком запускаємо одразу у виробництво та організовуємо доставку «від дверей до дверей» з нашими експедиторами. Від запиту ціни до доставки ваше замовлення веде одна людина.'),
 ('Where our clients are', 'Де наші клієнти'),
 ('<li>European Union <span>EU</span></li>', '<li>Європейський Союз <span>EU</span></li>'),
 ('<li>United Kingdom <span>UK</span></li>', '<li>Велика Британія <span>UK</span></li>'),
 ('<li>Ukraine <span>UA</span></li>', '<li>Україна <span>UA</span></li>'),
 ('<li>United States <span>US</span></li>', '<li>США <span>US</span></li>'),
 ('<li>Canada <span>CA</span></li>', '<li>Канада <span>CA</span></li>'),
 ('<li>Middle East <span>ME</span></li>', '<li>Близький Схід <span>ME</span></li>'),
 ('<p class="eyebrow">FAQ</p><h2>Ordering and delivery</h2>', '<p class="eyebrow">Питання</p><h2>Замовлення та доставка</h2>'),
 ('<summary>Which countries do you ship to?</summary><p>We ship worldwide, except to Russia and Belarus. Most of our clients are in the EU, the UK, Ukraine, the USA, Canada and the Middle East.</p>',
  '<summary>У які країни ви доставляєте?</summary><p>Доставляємо по всьому світу, крім Росії та Білорусі. Більшість наших клієнтів у ЄС, Великій Британії, Україні, США, Канаді та на Близькому Сході.</p>'),
 ('<summary>What is the minimum order?</summary><p>One full pallet for stock cans. For custom-printed cans the minimum is 350,000 units per design.</p>',
  '<summary>Яке мінімальне замовлення?</summary><p>Одна повна палета для банок зі складу. Для банок з індивідуальним друком мінімум становить 350 000 шт. на один дизайн.</p>'),
 ('<summary>How fast do you deliver?</summary><p>Stock cans reach EU customers within 5 working days. On average we dispatch 48 to 72 hours after payment. Delivery dates for custom orders are agreed individually.</p>',
  '<summary>Як швидко ви доставляєте?</summary><p>Банки зі складу доставляємо клієнтам у ЄС протягом 5 робочих днів. У середньому відвантажуємо через 48–72 години після оплати. Терміни для індивідуальних замовлень узгоджуємо окремо.</p>'),
 ('<summary>Who organises transport?</summary><p>We do. We work with forwarders and courier companies and include transport in the quote. The price depends on order size, delivery speed and destination.</p>',
  '<summary>Хто організовує транспорт?</summary><p>Ми. Працюємо з експедиторами та кур\'єрськими компаніями й включаємо доставку в пропозицію. Ціна залежить від обсягу замовлення, швидкості та місця доставки.</p>'),
 ('<summary>Can I use my own forwarder?</summary><p>Yes, on request we can hand the goods to a forwarder you nominate.</p>',
  '<summary>Чи можу я використати власного експедитора?</summary><p>Так, на ваш запит передамо товар вказаному вами експедитору.</p>'),
 ('<summary>Are lids included with the cans?</summary><p>Lids are priced separately. You can order them with your cans or on their own.</p>',
  '<summary>Чи входять кришки у вартість банок?</summary><p>Кришки оплачуються окремо. Їх можна замовити разом з банками або окремо.</p>'),
 ('<p class="eyebrow">Contact</p>', '<p class="eyebrow">Контакти</p>'),
 ('<h2 style="margin-top:12px">Request a quote</h2>', '<h2 style="margin-top:12px">Запит ціни</h2>'),
 ('Tell us the format, quantity and delivery country. We reply within one working day.', 'Вкажіть формат, кількість і країну доставки. Відповідаємо протягом одного робочого дня.'),
 ('<small>Phone</small>', '<small>Телефон</small>'),
 ('data-copy="mail">Copy</button>', 'data-copy="mail">Копіювати</button>'),
 ('data-copy="tel">Copy</button>', 'data-copy="tel">Копіювати</button>'),
 ('<label>Leave empty <input', '<label>Залиште порожнім <input'),
 ('<label>Name<input', '<label>Ім\'я<input'),
 ('<label>Company<input', '<label>Компанія<input'),
 ('<label>Delivery country<input', '<label>Країна доставки<input'),
 ("<label class=\"full\">I'm interested in", '<label class="full">Мене цікавить'),
 ('<option>Stock cans</option><option>Custom-printed cans</option><option>Lids only</option><option>Cans and lids</option>',
  '<option>Банки зі складу</option><option>Банки з друком</option><option>Лише кришки</option><option>Банки та кришки</option>'),
 ('<label class="full">Formats and quantities<textarea', '<label class="full">Формати та кількість<textarea'),
 ('placeholder="e.g. 500 ml black matt, 6 pallets, 202 CDL silver lids"', 'placeholder="напр. 500 мл чорна матова, 6 палет, кришки 202 CDL срібні"'),
 ('type="submit">Send request</button>', 'type="submit">Надіслати запит</button>'),
 ('<nav aria-label="Footer"><a href="#faq">FAQ</a><a href="privacy.html">Privacy policy</a>', '<nav aria-label="Footer"><a href="#faq">Питання</a><a href="../privacy.html">Політика конфіденційності</a>'),
 ('const T={silver:"Silver",black:"Black",blackmatt:"Black matt",bwmatt:"Black/white matt",copy:"Copy",copied:"Copied",preview:"Preview only. On the live site this request goes to canorders@pwglobaltrading.eu.",ml:"ml",loc:"en-US"};',
  'const T={silver:"Срібляста",black:"Чорна",blackmatt:"Чорна матова",bwmatt:"Чорно-біла матова",copy:"Копіювати",copied:"Скопійовано",preview:"Це лише попередній перегляд. На сайті запит надійде на canorders@pwglobaltrading.eu.",ml:"мл",loc:"uk-UA"};'),
 ('aria-label="Main"', 'aria-label="Меню"'),
 ('aria-label="Footer"', 'aria-label="Посилання"'),
]

def translate(src, pairs, ml="ml"):
    out = src
    for a, b in pairs:
        n = out.count(a)
        if n == 0:
            raise SystemExit("missing: " + a[:80])
        out = out.replace(a, b)
    # format names in the stock table
    if ml != "ml":
        out = re.sub(r'\["(\d+) ml ', r'["\1 ' + ml + ' ', out)
    return out

PRIVACY_EN = """<title>Privacy Policy · PW Global Trading</title>
<meta name="description" content="How PW Global Trading OÜ processes personal data sent through pwglobaltrading.com.">
{style}
<header class="top"><div class="wrap"><a class="logo" href="index.html"><b>PW GLOBAL</b><span>Trading</span></a>
<nav class="menu" aria-label="Main"><a href="index.html#cans">Cans</a><a href="index.html#faq">FAQ</a><a class="btn btn-accent" href="index.html#contact">Request a quote</a></nav></div></header>
<main><section class="block"><div class="wrap legal">
<p class="eyebrow">Legal</p>
<h1 style="font-size:var(--s5);margin-block:12px 28px">Privacy policy</h1>
<p class="lead">Last updated: 29 October 2026</p>

<h3>1. Who we are</h3>
<p>The controller of your personal data is PW Global Trading OÜ, Narva mnt 13-27, 10151 Tallinn, Estonia, VAT EE102349708 ("we"). Contact for all privacy matters: <b>canorders@pwglobaltrading.eu</b>.</p>

<h3>2. What data we process and why</h3>
<ul>
<li><b>Quote requests and e-mails.</b> When you use the contact form or write to us, we process your name, company, e-mail address, delivery country and the content of your message. We use them to answer your request, prepare an offer and, if you order, to perform the contract. Legal basis: steps prior to entering into a contract and our legitimate interest in answering business enquiries (Art. 6(1)(b) and (f) GDPR).</li>
<li><b>Orders and invoices.</b> For orders we process company and contact details, delivery addresses and tax identification numbers to deliver goods and issue invoices. Legal basis: performance of a contract and legal obligations (Art. 6(1)(b) and (c) GDPR).</li>
<li><b>Technical data.</b> Our hosting provider records technical data such as IP address, browser type and time of access to deliver the website and keep it secure. Legal basis: legitimate interest (Art. 6(1)(f) GDPR).</li>
</ul>

<h3>3. Cookies and tracking</h3>
<p>This website does not use analytics, advertising or tracking cookies. Fonts are loaded from Google Fonts, which means your browser connects to Google servers and transmits your IP address.</p>

<h3>4. Who receives the data</h3>
<p>We share data only with providers who help us run our business: website hosting and form handling (Netlify, Inc.), e-mail hosting, accounting software, and forwarders and courier companies that deliver your order. Some providers may process data outside the EEA; in that case transfers are based on the European Commission's standard contractual clauses or an adequacy decision.</p>

<h3>5. How long we keep data</h3>
<p>Enquiries that do not lead to an order are deleted within 24 months. Order and invoice data are kept for as long as accounting and tax law requires, in Estonia currently 7 years.</p>

<h3>6. Your rights</h3>
<p>You have the right to access, correct and delete your data, to restrict or object to processing, and to data portability. Send your request to canorders@pwglobaltrading.eu. You can also lodge a complaint with the Estonian Data Protection Inspectorate (Andmekaitse Inspektsioon, www.aki.ee) or the supervisory authority in your country.</p>

<h3>7. Changes</h3>
<p>We may update this policy when our services or the law change. The current version is always published on this page.</p>
</div></section></main>
<footer><div class="wrap"><address>PW Global Trading OÜ · Narva mnt 13-27, 10151 Tallinn, Estonia · VAT EE102349708</address>
<nav aria-label="Footer"><a href="index.html#faq">FAQ</a><a href="privacy.html">Privacy policy</a></nav></div></footer>
"""

LEGAL_CSS = "<style>.legal{max-width:760px}.legal h3{font-size:var(--s3);margin:36px 0 10px}.legal p,.legal li{color:var(--fg)}.legal p+p{margin-top:12px}.legal ul{padding-left:20px;display:grid;gap:10px;margin:0}</style>"

BASE_CSS = "<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>"

def page(fragment, lang, path, alt=True):
    head_end = fragment.index("</style>") + len("</style>")
    head, body = fragment[:head_end], fragment[head_end:]
    url = SITE + path
    links = f'<link rel="canonical" href="{url}">\n'
    if alt:
        links += (f'<link rel="alternate" hreflang="en" href="{SITE}/">\n'
                  f'<link rel="alternate" hreflang="uk" href="{SITE}/ua/">\n'
                  f'<link rel="alternate" hreflang="et" href="{SITE}/et/">\n'
                  f'<link rel="alternate" hreflang="x-default" href="{SITE}/">\n')
    title = re.search(r"<title>(.*?)</title>", head).group(1)
    if title == "PW Global Trading":
        title = {"en": "Beverage Cans & Lids Supplier | PW Global Trading",
                 "uk": "Банки та кришки для напоїв | PW Global Trading",
                 "et": "Joogipurgid ja kaaned | PW Global Trading"}[lang]
        head = head.replace("<title>PW Global Trading</title>", f"<title>{title}</title>")
    desc = re.search(r'<meta name="description" content="(.*?)">', head).group(1)
    og = (f'<meta property="og:type" content="website">\n<meta property="og:title" content="{title}">\n'
          f'<meta property="og:description" content="{desc}">\n<meta property="og:url" content="{url}">\n')
    head = head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
    return (f'<!doctype html>\n<html lang="{lang}">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f'{BASE_CSS}\n{head}\n{links}{og}</head>\n<body>{body}</body>\n</html>\n')

def main():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(os.path.join(DIST, "ua"))
    os.makedirs(os.path.join(DIST, "et"))
    style = SRC[SRC.index("<style>"):SRC.index("</style>") + 8]
    ua = translate(SRC, UA, ml="мл")
    from lang_et import ET_VALUES
    if len(ET_VALUES) != len(UA):
        raise SystemExit(f"ET has {len(ET_VALUES)} strings, expected {len(UA)}")
    et = translate(SRC, [(k, v) for (k, _), v in zip(UA, ET_VALUES)])
    files = {
        "index.html": page(SRC, "en", "/"),
        "ua/index.html": page(ua, "uk", "/ua/"),
        "et/index.html": page(et, "et", "/et/"),
        "privacy.html": page(PRIVACY_EN.format(style=style + LEGAL_CSS), "en", "/privacy.html", alt=False),
        "_redirects": "https://pwglobaltrading.eu/*      https://pwglobaltrading.com/:splat  301!\nhttp://pwglobaltrading.eu/*       https://pwglobaltrading.com/:splat  301!\nhttps://www.pwglobaltrading.eu/*  https://pwglobaltrading.com/:splat  301!\nhttp://www.pwglobaltrading.eu/*   https://pwglobaltrading.com/:splat  301!\n/faq            /#faq          301\n/store-policy   /privacy.html  301\n/home           /              301\n",
        "robots.txt": f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n",
        "sitemap.xml": ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                        + "".join(f"  <url><loc>{SITE}{p}</loc></url>\n" for p in ["/", "/ua/", "/et/", "/privacy.html"])
                        + "</urlset>\n"),
    }
    for name, content in files.items():
        with open(os.path.join(DIST, name), "w", encoding="utf-8") as f:
            f.write(content)
    print("built:", ", ".join(files))

main()
