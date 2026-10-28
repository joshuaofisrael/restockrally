import os, json, html, re, shutil, datetime
from data import SITE, RELEASES, RESTOCKS
from articles import ARTICLES
import sys, subprocess, legal_gate
# Legal hold gate layer 1: a flagged article is never rendered (saved as HOLD_REVIEW draft + queue.jsonl instead).
ARTICLES=[a for a in ARTICLES if legal_gate.gate_article(a)]
OUT=os.path.join(os.path.dirname(__file__),"..","docs"); OUT=os.path.abspath(OUT)
U=SITE["url"]; N=SITE["name"]; Y=SITE["year"]
e=html.escape
def slug(s): return re.sub(r"[^a-z0-9]+","-",s.lower().replace("'","")).strip("-")
def nice(d): return datetime.date.fromisoformat(d).strftime("%B %-d, %Y")
LEGAL=f"© {Y} Joshua Israel Ventures LLC. All rights reserved. {N} is a trade name of Joshua Israel Ventures LLC, a Florida limited liability company."
pages=[]
ORG={"@type":"NewsMediaOrganization","@id":U+"/#org","name":N,"url":U+"/","logo":{"@type":"ImageObject","url":U+"/assets/logo.svg"},"parentOrganization":{"@type":"Organization","name":"Joshua Israel Ventures LLC"}}
NAV=[("/releases/","Release Calendar"),("/restocks/","Restocks"),("/raffles/","Raffles"),("/news/","News")]
def head(title,desc,path,ld):
    t=f"{title} | {N}" if path!="/" else f"{N}: {SITE['tagline']}"
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(t)}</title><meta name="description" content="{e(desc[:155])}"><link rel="canonical" href="{U}{path}">
<meta name="robots" content="index,follow,max-image-preview:large"><meta property="og:site_name" content="{N}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc[:155])}"><meta property="og:url" content="{U}{path}"><meta property="og:type" content="{'article' if path.startswith('/news/') and path!='/news/' else 'website'}"><meta name="twitter:card" content="summary">
<link rel="icon" href="/assets/logo.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/site.css"><link rel="alternate" type="application/rss+xml" href="/feed.xml" title="{N}">
<script>window.__rrGaId={json.dumps(SITE['ga_id'])};window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('consent','default',{{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied',functionality_storage:'denied',personalization_storage:'denied',security_storage:'granted',wait_for_update:500}});</script><script defer src="/consent.js"></script>
<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@graph":[ORG]+ld})}</script></head>"""
def chrome(body,path):
    nav="".join(f'<li><a href="{h}"{" aria-current=\"page\"" if path.startswith(h) else ""}>{t}</a></li>' for h,t in NAV)
    return f"""<body><a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap header-bar"><a class="brand" href="/"><img src="/assets/logo.svg" alt="" width="34" height="34"><span class="brand-name">{N}</span></a>
<p class="header-charge"><span class="dot" aria-hidden="true"></span>On the drop</p>
<nav class="utility" aria-label="Company"><a href="/about/">About</a><a href="/contact/">Contact</a></nav></div>
<nav class="topics" aria-label="Sections"><div class="wrap"><ul class="topic-list">{nav}</ul></div></nav><div class="road-line" aria-hidden="true"></div></header>
<main id="main" tabindex="-1"><div class="wrap">{body}</div></main>
<footer class="site-footer"><div class="road-line" aria-hidden="true"></div><div class="wrap footer-grid">
<nav aria-label="Coverage"><h2>Coverage</h2><ul><li><a href="/releases/">Release Calendar</a></li><li><a href="/restocks/">Restocks</a></li><li><a href="/raffles/">Raffles</a></li><li><a href="/news/">News</a></li></ul></nav>
<nav aria-label="Company links"><h2>{N}</h2><ul><li><a href="/about/">About</a></li><li><a href="/contact/">Contact Us</a></li><li><a href="/sources-ethics/">Sources &amp; Ethics</a></li><li><a href="/corrections/">Corrections</a></li></ul></nav>
<nav aria-label="Legal and feeds"><h2>Legal and feeds</h2><ul><li><a href="/terms/">Terms</a></li><li><a href="/privacy/">Privacy</a></li><li><a href="/disclaimer/">Disclaimer</a></li><li><a href="/copyright/">Copyright &amp; DMCA</a></li><li><a href="/affiliate-disclosure/">Affiliate Disclosure</a></li><li><button type="button" class="consent-link" data-consent-open="1">Cookie choices</button></li><li><a href="/feed.xml">RSS</a></li></ul></nav>
</div></footer></body></html>"""
def write(path,title,desc,body,ld=None,index=True):
    crumbs=[]
    if path!="/":
        parts=[p for p in path.strip("/").split("/")]
        items=[{"@type":"ListItem","position":1,"name":"Home","item":U+"/"}]
        acc=""
        for i,p in enumerate(parts):
            acc+="/"+p
            items.append({"@type":"ListItem","position":i+2,"name":title if i==len(parts)-1 else p.replace("-"," ").title(),"item":U+acc+"/"})
        crumbs=[{"@type":"BreadcrumbList","itemListElement":items}]
    h=head(title,desc,path,(ld or [])+crumbs)+chrome(body,path)
    if not index: h=h.replace('content="index,follow,max-image-preview:large"','content="noindex"')
    d=os.path.join(OUT,path.strip("/"))
    if not path.endswith(".html"): os.makedirs(d,exist_ok=True)
    open(os.path.join(d,"index.html") if not path.endswith(".html") else d,"w").write(h)
    if index: pages.append(path)
shutil.rmtree(OUT,ignore_errors=True); os.makedirs(OUT)
shutil.copytree(os.path.join(os.path.dirname(__file__),"static"),OUT,dirs_exist_ok=True)
REL=[dict(name=r[0],brand=r[1],date=r[2],price=r[3],sku=r[4],buy=r[5],src=r[6],slug=slug(r[0].replace("(Women's)","womens"))) for r in RELEASES]
REL.sort(key=lambda r:r["date"])
def relrow(r):
    return f'<li class="rel" data-brand="{e(r["brand"])}" data-date="{r["date"]}" data-price="{r["price"]}"><time datetime="{r["date"]}">{datetime.date.fromisoformat(r["date"]).strftime("%b %-d")}</time><span class="rel-main"><a href="/shoes/{r["slug"]}/">{e(r["name"])}</a><span class="meta">{e(r["brand"])} · {e(r["sku"])}</span></span><span class="price">${r["price"]}</span></li>'
# shoe pages
for r in REL:
    buy="".join(f'<li><a class="buy-btn" href="{e(u)}" rel="noopener">{e(l)}</a></li>' for l,u in r["buy"])
    body=f"""<article class="story-page"><p class="story-kicker"><span class="chip">{e(r['brand'])}</span> <time datetime="{r['date']}">{nice(r['date'])}</time></p>
<h1>{e(r['name'])}</h1><p class="dek">Releases {nice(r['date'])} at ${r['price']} retail (US), according to <a href="{e(r['src'][1])}">{e(r['src'][0])}</a>.</p>
<dl class="facts"><div><dt>Release date</dt><dd>{nice(r['date'])}</dd></div><div><dt>Retail price</dt><dd>${r['price']}</dd></div><div><dt>Style code</dt><dd>{e(r['sku'])}</dd></div><div><dt>Brand</dt><dd>{e(r['brand'])}</dd></div></dl>
<aside class="buy-box" aria-labelledby="wtb"><h2 id="wtb">Where to buy</h2><ul>{buy}</ul><p class="small">Links go to the official retailer. Dates, prices and stock can change; the retailer's page has the final word. We do not sell shoes. See our <a href="/affiliate-disclosure/">affiliate disclosure</a>.</p></aside>
<section class="sources"><h2>Source</h2><ol><li><a href="{e(r['src'][1])}">{e(r['src'][0])}</a></li></ol></section>
<p><a href="/releases/">Back to the release calendar</a></p></article>"""
    ld=[{"@type":"Product","name":r["name"],"sku":r["sku"],"brand":{"@type":"Brand","name":r["brand"]},"releaseDate":r["date"]}]
    write(f"/shoes/{r['slug']}/",r["name"]+" release date and price",f"{r['name']} releases {nice(r['date'])} for ${r['price']}. Style code {r['sku']}, where to buy and sources.",body,ld)
# calendar
brands=sorted({r["brand"] for r in REL})
opts="".join(f'<option>{e(b)}</option>' for b in brands)
cal=f"""<h1>Sneaker release calendar</h1><p class="dek">Upcoming sneaker release dates with retail prices and style codes. Filter by brand, date and price. Every row links to a shoe page with a where to buy box and its source.</p>
<form class="filters" id="filters" onsubmit="return false"><label>Brand <select id="f-brand"><option value="">All brands</option>{opts}</select></label>
<label>From <input type="date" id="f-from"></label><label>To <input type="date" id="f-to"></label>
<label>Max price <select id="f-price"><option value="">Any</option><option>150</option><option>200</option><option>250</option></select></label>
<label>Sort <select id="f-sort"><option value="date">Date</option><option value="price">Price</option></select></label></form>
<p id="count" class="small" aria-live="polite">{len(REL)} releases</p><ul class="rel-list" id="rel-list">{''.join(relrow(r) for r in REL)}</ul>
<p class="small">Sources: retail prices and dates come from the brand's own pages where available, and otherwise from the release calendars credited on each shoe page.</p><script src="/assets/calendar.js" defer></script>"""
write("/releases/","Sneaker release dates calendar","Fast, filterable sneaker release calendar: dates, retail prices and style codes for Nike, Jordan, adidas and more, with where to buy links.",cal)
# restocks
rs="".join(f'<li class="rel"><time datetime="{d}">{datetime.date.fromisoformat(d).strftime("%b %-d")}</time><span class="rel-main"><strong>{e(n)}</strong><span class="meta">{e(w)}{" · "+e(k) if k else ""} · reported by <a href="{e(su)}">{e(sn)}</a></span></span><span class="price">{"$"+str(p) if p else "See retailer"}</span></li>' for n,d,w,p,k,(sn,su) in RESTOCKS)
write("/restocks/","Sneaker restocks log","A sourced log of recent sneaker restocks: what came back, where, at what retail price, and who reported it.",f"<h1>Sneaker restocks</h1><p class='dek'>Recent restocks, newest first. Each entry links to the original report. Stock moves fast, so check the retailer right away.</p><ul class='rel-list'>{rs}</ul><p><a href='/news/october-2026-sneaker-restocks-nike-mind-air-bakin/'>Read the October restocks roundup</a></p>")
write("/raffles/","Sneaker raffles and draws","How sneaker raffles and draws work, and the open raffles we have verified with the retailer.",
"""<h1>Sneaker raffles and draws</h1><p class="dek">We list a raffle only after we confirm it on the retailer's own page. There are no verified open raffles on this page right now.</p>
<h2>How raffles work</h2><p>A raffle or draw lets you enter for the chance to buy a pair at retail. Retailers pick winners at random and charge only the winners. Nike runs many launches on the SNKRS app as timed draws. Enter only through the retailer's own site or app, never through a link that asks for a fee to enter.</p>
<h2>Staying safe</h2><ul><li>Check the web address belongs to the retailer.</li><li>No genuine retailer raffle charges an entry fee.</li><li>Watch for winner emails that ask you to pay through a new link; go to the retailer directly instead.</li></ul>
<p>See the <a href="/releases/">release calendar</a> for upcoming dates.</p>""")
# articles
ART=sorted(ARTICLES,key=lambda a:a["date"],reverse=True)
for a in ART:
    srcs="".join(f'<li><a href="{e(u)}">{e(t)}</a> <span class="source-meta">{e(p)}, {nice(d)}</span></li>' for t,u,p,d in a["sources"])
    body=f"""<article class="story-page"><header class="article-head"><p class="story-kicker"><span class="chip">{e(a['category'])}</span> <time datetime="{a['date']}">{nice(a['date'])}</time></p><h1>{e(a['title'])}</h1><p class="byline">By the {N} desk</p><p class="dek">{e(a['description'])}</p><p class="last-updated">Last updated <time datetime="{a['date']}">{nice(a['date'])}</time></p></header>
<div class="prose">{a['body']}</div><section class="sources" aria-labelledby="sh"><h2 id="sh">Sources</h2><ol>{srcs}</ol></section></article>"""
    ld=[{"@type":"NewsArticle","headline":a["title"],"description":a["description"],"datePublished":a["date"]+"T09:00:00Z","dateModified":a["date"]+"T09:00:00Z","mainEntityOfPage":U+"/news/"+a["slug"]+"/","author":{"@type":"Organization","name":N+" desk","url":U+"/about/"},"publisher":{"@id":U+"/#org"},"isBasedOn":[s[1] for s in a["sources"]]}]
    write(f"/news/{a['slug']}/",a["title"],a["description"],body,ld)
cards="".join(f'<li class="story-card"><p class="story-kicker"><span class="chip">{e(a["category"])}</span> <time datetime="{a["date"]}">{nice(a["date"])}</time></p><h3><a href="/news/{a["slug"]}/">{e(a["title"])}</a></h3><p>{e(a["description"])}</p></li>' for a in ART)
write("/news/","Sneaker news","Sourced sneaker release and restock news.",f"<h1>Sneaker news</h1><ul class='story-grid'>{cards}</ul>")
today="2026-10-27"; up=[r for r in REL if r["date"]>=today][:8]
home=f"""<section class="hero"><h1 class="visually-hidden">{N}</h1><p class="hero-kicker">Release dates, restocks and raffles</p><p class="hero-lead">The fastest way to see what drops next, what it costs and where to buy it.</p><p><a class="buy-btn" href="/releases/">Open the release calendar</a></p></section>
<section aria-labelledby="up"><h2 id="up" class="section-title">Dropping next</h2><ul class="rel-list">{''.join(relrow(r) for r in up)}</ul><p><a href="/releases/">Full calendar</a></p></section>
<section aria-labelledby="ln"><h2 id="ln" class="section-title">Latest news</h2><ul class="story-grid">{cards}</ul></section>
<section aria-labelledby="rs"><h2 id="rs" class="section-title">Recent restocks</h2><ul class="rel-list">{rs}</ul></section>"""
write("/",N,"Fast sneaker release calendar, restock log and raffle guide with prices, style codes and where to buy links. Every fact sourced.",home,[{"@type":"WebSite","name":N,"url":U+"/","publisher":{"@id":U+"/#org"}}])
# static pages
def page(path,title,desc,body,legal=False,index=True):
    if legal: body+=f'<p class="legal-line">{LEGAL}</p>'
    write(path,title,desc,f'<article class="page-body"><h1>{title}</h1>{body}</article>',index=index)
page("/about/","About "+N,"About "+N+", a sneaker release and restock news site.",f"<p>{N} tracks sneaker release dates, restocks and raffles with one rule: every date, price and claim links to its source. We favor brand pages first, then credited release calendars and reporting.</p><p>We built the site to load fast on a phone, so you can check a drop in seconds. Questions or tips? <a href='/contact/'>Contact us</a>.</p>")
page("/contact/","Contact Us","Contact the "+N+" desk with tips, corrections or questions.",f"""<p>Send a tip, a correction or a question. We read every message.</p>
<form class="contact-form" action="{SITE['contact_endpoint']}" method="POST" id="cf">
<input type="hidden" name="_subject" value="{N} contact form"><input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false"><input type="hidden" name="_next" value="{U}/contact/thanks/">
<p class="hp" aria-hidden="true"><label>Leave this empty <input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></p>
<p><label for="n">Name</label><input id="n" name="name" required autocomplete="name"></p><p><label for="em">Email</label><input id="em" type="email" name="email" required autocomplete="email"></p>
<p><label for="m">Message</label><textarea id="m" name="message" rows="6" required></textarea></p><input type="hidden" name="_ready" id="ready" value=""><p><button type="submit" class="buy-btn">Send</button></p></form>
<p class="small">We use your message only to reply. We never sell it.</p><script src="/assets/contact.js" defer></script>""")
page("/contact/thanks/","Thanks","Message sent.","<p>Thanks, your message is on its way. <a href='/'>Back to the homepage</a>.</p>",index=False)
page("/sources-ethics/","Sources & Ethics","How "+N+" sources and checks sneaker news.","<p>Every fact links to a named source in the sentence. We prefer the brand's own product and launch pages, then credited release calendars and reporting. We write in our own words, quote briefly with attribution, report company announcements as what the company says, and label any opinion. We do not invent quotes, prices or dates. Images are official brand press images with credit, or embeds; we do not use AI images of real products.</p>")
page("/corrections/","Corrections","How to request a correction on "+N+".","<p>If we got something wrong, <a href='/contact/'>tell us</a>. We fix errors quickly and note material corrections at the end of the article.</p>")
page("/terms/","Terms of Use","Terms of use for "+N+".",f"<p>By using {N} you agree to these terms. The site is operated by Joshua Israel Ventures LLC, a Florida limited liability company, under the trade name {N}.</p><h2>Information only</h2><p>Content is general news and information. Release dates, prices and stock change, and the retailer's page controls. We are not a retailer and do not sell, hold or ship products.</p><h2>Third party links</h2><p>We link to retailers and sources we do not control and are not responsible for their content, offers or practices.</p><h2>Limitation of liability</h2><p>To the fullest extent permitted by law, the site is provided as is, without warranties, and we are not liable for any loss arising from its use, including a missed release or a purchase decision.</p><h2>Intellectual property</h2><p>Brand names and product names belong to their owners and are used only to identify products. See our <a href='/copyright/'>Copyright and DMCA policy</a>.</p><h2>Governing law</h2><p>These terms are governed by the laws of the State of Florida, United States, without regard to conflict of law rules, and disputes will be resolved in the courts located in Florida.</p><h2>Changes</h2><p>We may update these terms; the date below shows the latest version. Last updated October 27, 2026.</p>",legal=True)
page("/privacy/","Privacy Policy","How "+N+" handles your data, including Google Analytics 4.",f"<p>This policy explains what data {N} collects. Last updated October 27, 2026.</p><h2 id='google-analytics'>Google Analytics 4</h2><p>With your consent, we use Google Analytics 4, a service from Google LLC, to measure visits and improve the site. Google Analytics 4 loads only after you click Accept in our cookie banner. It sets cookies such as _ga and collects data like pages viewed, device type and approximate location. We turn off Google signals and ad personalization. You can change your choice any time with the Cookie choices button in the footer. See <a href='https://policies.google.com/technologies/partner-sites'>how Google uses data from sites that use its services</a>.</p><h2>Cloudflare Web Analytics</h2><p>We may use Cloudflare Web Analytics, a privacy focused tool that does not use cookies, to count page views.</p><h2>Contact form</h2><p>Messages are delivered by FormSubmit to our inbox and used only to reply.</p><h2>Advertising and affiliate links</h2><p>If we add advertising (such as Google AdSense) or affiliate links, partners may use cookies subject to your consent where required. We will update this policy first.</p><h2>Your rights</h2><p>You can ask us to access or delete data you sent us through the <a href='/contact/'>contact form</a>. We do not sell personal information.</p><h2>Children</h2><p>The site is not directed to children under 13.</p>",legal=True)
page("/disclaimer/","Disclaimer","Disclaimer for "+N+".",f"<p>{N} publishes news and information about sneaker releases, restocks and raffles. It is not purchasing, financial or resale advice. Dates, prices, sizes and stock come from cited sources and can change at any time; always confirm with the retailer. {N} is independent and is not affiliated with or endorsed by Nike, Jordan Brand, adidas or any other brand or retailer mentioned. Product names and trademarks belong to their owners.</p>",legal=True)
page("/copyright/","Copyright & DMCA","Copyright and DMCA policy for "+N+".",f"<p>We write original text and use only official brand press images with credit, or embeds. If you believe content on {N} infringes your copyright, send a notice through our <a href='/contact/'>contact form</a> with: your contact details, the work you claim is infringed, the URL of the material, a statement of good faith belief that the use is not authorized, a statement that the notice is accurate and that you are the owner or authorized to act, and your signature. We remove material promptly on a valid notice and may restore it on a valid counter notice.</p>",legal=True)
page("/affiliate-disclosure/","Affiliate Disclosure","Affiliate and advertising disclosure for "+N+".",f"<p>{N} may earn a commission when you buy through some retailer links on this site, at no extra cost to you. Right now our where to buy links are plain links to official retailers. When a link becomes an affiliate link, this page and the link label will say so. Commissions never decide what we cover or how we rank releases.</p>",legal=True)
write("/404.html","Page not found","Page not found.","<h1>Page not found</h1><p>Try the <a href='/releases/'>release calendar</a> or the <a href='/'>homepage</a>.</p>",index=False)
# seo files
sm="".join(f"<url><loc>{U}{p}</loc><lastmod>2026-10-27</lastmod></url>" for p in pages)
open(f"{OUT}/sitemap.xml","w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>')
bots=["Googlebot","Bingbot","OAI-SearchBot","GPTBot","ChatGPT-User","PerplexityBot","ClaudeBot","Claude-SearchBot","Google-Extended","Applebot","Applebot-Extended","CCBot","DuckDuckBot"]
open(f"{OUT}/robots.txt","w").write("".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)+f"User-agent: *\nAllow: /\n\nSitemap: {U}/sitemap.xml\n")
open(f"{OUT}/{SITE['indexnow_key']}.txt","w").write(SITE["indexnow_key"])
open(f"{OUT}/CNAME","w").write("restockrally.com\n"); open(f"{OUT}/.nojekyll","w").write("")
open(f"{OUT}/llms.txt","w").write(f"# {N}\n\n> {SITE['tagline']}. Sourced sneaker release dates, restocks and raffles.\n\n## Key pages\n- [Release calendar]({U}/releases/)\n- [Restocks]({U}/restocks/)\n- [Raffles]({U}/raffles/)\n- [News]({U}/news/)\n- [Sources & Ethics]({U}/sources-ethics/)\n\n## Articles\n"+"".join(f"- [{a['title']}]({U}/news/{a['slug']}/): {a['description']}\n" for a in ART))
items="".join(f"<item><title>{e(a['title'])}</title><link>{U}/news/{a['slug']}/</link><guid>{U}/news/{a['slug']}/</guid><pubDate>{datetime.date.fromisoformat(a['date']).strftime('%a, %d %b %Y')} 09:00:00 +0000</pubDate><description>{e(a['description'])}</description></item>" for a in ART)
open(f"{OUT}/feed.xml","w").write(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{N}</title><link>{U}/</link><description>{SITE["tagline"]}</description>{items}</channel></rss>')
# Legal hold gate layer 2: full-site backstop. If any built page is held, put docs/ back to the last committed version and fail.
if legal_gate.main([]) != 0:
    root=os.path.dirname(OUT)
    subprocess.run(["git","checkout","--","docs"],cwd=root); subprocess.run(["git","clean","-fdq","docs"],cwd=root)
    print("HOLD_REVIEW: build refused, docs/ restored to the last published version"); sys.exit(3)
print(len(pages),"pages")
