import os, json, html, re, shutil, datetime
from zoneinfo import ZoneInfo
from data import SITE, RELEASES, RESTOCKS
from articles import ARTICLES
from guides_2026_11_12 import GUIDES_1112
from guides_where_2026_11_12 import GUIDES_WHERE_1112
from related import RELATED
ARTICLES=ARTICLES+GUIDES_1112+GUIDES_WHERE_1112
import sys, subprocess, legal_gate
# Legal hold gate layer 1: a flagged article is never rendered (saved as HOLD_REVIEW draft + queue.jsonl instead).
ARTICLES=[a for a in ARTICLES if legal_gate.gate_article(a)]
def _asof():
    raw=os.environ.get("BUILD_ASOF")
    if not raw: return datetime.datetime.now(datetime.timezone.utc)
    dt=datetime.datetime.fromisoformat(raw)
    if dt.tzinfo is None: dt=dt.replace(tzinfo=datetime.timezone.utc)
    return dt.astimezone(datetime.timezone.utc)
NOW=_asof()
def pub_dt(a):
    raw=a.get("publish") or (a["date"]+"T09:00:00+00:00")
    dt=datetime.datetime.fromisoformat(raw)
    if dt.tzinfo is None: dt=dt.replace(tzinfo=datetime.timezone.utc)
    return dt.astimezone(datetime.timezone.utc)
# A publish time in the future stays out of pages, the sitemap, RSS and listings.
ARTICLES=[a for a in ARTICLES if pub_dt(a)<=NOW]
OUT=os.path.join(os.path.dirname(__file__),"..","docs"); OUT=os.path.abspath(OUT)
U=SITE["url"]; N=SITE["name"]; Y=SITE["year"]
e=html.escape
def slug(s): return re.sub(r"[^a-z0-9]+","-",s.lower().replace("'","")).strip("-")
def nice(d): return datetime.date.fromisoformat(d).strftime("%B %-d, %Y")
def stamp(a):
    if a.get("publish"):
        dt=pub_dt(a)
        et=dt.astimezone(ZoneInfo("America/New_York"))
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ"), nice(et.date().isoformat())+" at "+et.strftime("%-I:%M %p")+" ET"
    return a["date"], nice(a["date"])
LEGAL=f"© {Y} Joshua Israel Ventures LLC. All rights reserved. {N} is a trade name of Joshua Israel Ventures LLC, a Florida limited liability company."
pages=[]
ORG={"@type":"NewsMediaOrganization","@id":U+"/#org","name":N,"url":U+"/","logo":{"@type":"ImageObject","url":U+"/assets/logo.svg"},"parentOrganization":{"@type":"Organization","name":"Joshua Israel Ventures LLC"}}
NAV=[("/releases/","Release Calendar"),("/restocks/","Restocks"),("/raffles/","Raffles"),("/guides/","Guides"),("/news/","News")]
def head(title,desc,path,ld,image=None):
    t=f"{title} | {N}" if path!="/" else f"{N}: {SITE['tagline']}"
    card="summary_large_image" if image else "summary"
    ogimg=f'<meta property="og:image" content="{U}{image}">' if image else ""
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="msvalidate.01" content="942EB99DB458637348E2ADBDEBDAA7AE">
<title>{e(t)}</title><meta name="description" content="{e(desc[:155])}"><link rel="canonical" href="{U}{path}">
<meta name="robots" content="index,follow,max-image-preview:large"><meta property="og:site_name" content="{N}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc[:155])}"><meta property="og:url" content="{U}{path}"><meta property="og:type" content="{'article' if path.startswith('/news/') and path!='/news/' else 'website'}">{ogimg}<meta name="twitter:card" content="{card}">
<link rel="icon" href="/assets/logo.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/site.css"><link rel="alternate" type="application/rss+xml" href="/feed.xml" title="{N}">
<script>window.__rrGaId={json.dumps(SITE['ga_id'])};window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('consent','default',{{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied',functionality_storage:'denied',personalization_storage:'denied',security_storage:'granted',wait_for_update:500}});</script><script defer src="/consent.js"></script>
<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@graph":[ORG]+ld})}</script><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5681559774142917" crossorigin="anonymous"></script></head>"""
def chrome(body,path):
    nav="".join(f'<li><a href="{h}"{" aria-current=\"page\"" if path.startswith(h) else ""}>{t}</a></li>' for h,t in NAV)
    return f"""<body><a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap header-bar"><a class="brand" href="/"><img src="/assets/logo.svg" alt="" width="34" height="34"><span class="brand-name">{N}</span></a>
<p class="header-charge"><span class="dot" aria-hidden="true"></span>On the drop</p>
<nav class="utility" aria-label="Company"><a href="/about/">About</a><a href="/contact/">Contact</a></nav></div>
<nav class="topics" aria-label="Sections"><div class="wrap"><ul class="topic-list">{nav}</ul></div></nav><div class="road-line" aria-hidden="true"></div></header>
<main id="main" tabindex="-1"><div class="wrap">{body}</div></main>
<footer class="site-footer"><div class="road-line" aria-hidden="true"></div><div class="wrap footer-grid">
<nav aria-label="Coverage"><h2>Coverage</h2><ul><li><a href="/releases/">Release Calendar</a></li><li><a href="/restocks/">Restocks</a></li><li><a href="/raffles/">Raffles</a></li><li><a href="/guides/">Guides</a></li><li><a href="/brands/">Brands</a></li><li><a href="/style-codes/">Style code lookup</a></li><li><a href="/news/">News</a></li></ul></nav>
<nav aria-label="Company links"><h2>{N}</h2><ul><li><a href="/about/">About</a></li><li><a href="/contact/">Contact Us</a></li><li><a href="/sources-ethics/">Sources &amp; Ethics</a></li><li><a href="/corrections/">Corrections</a></li></ul></nav>
<nav aria-label="Legal and feeds"><h2>Legal and feeds</h2><ul><li><a href="/terms/">Terms</a></li><li><a href="/privacy/">Privacy</a></li><li><a href="/disclaimer/">Disclaimer</a></li><li><a href="/copyright/">Copyright &amp; DMCA</a></li><li><a href="/image-policy/">Image policy</a></li><li><a href="/affiliate-disclosure/">Affiliate Disclosure</a></li><li><button type="button" class="consent-link" data-consent-open="1">Cookie choices</button></li><li><a href="/feed.xml">RSS</a></li></ul></nav>
</div></footer><script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "eac63f2b5dbc4539a2d95249baab6472"}}'></script></body></html>"""
# AdSense low-value-content fix (20 Nov 2026): thin release-data pages listed in src/thin-noindex.txt
_THIN=set()
try:
    _THIN={l.strip().strip("/") for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"thin-noindex.txt")) if l.strip() and not l.startswith("#")}
except FileNotFoundError:
    pass
def write(path,title,desc,body,ld=None,index=True,lastmod=None,image=None):
    if path.strip("/") in _THIN: index=False
    crumbs=[]
    if path!="/":
        parts=[p for p in path.strip("/").split("/")]
        items=[{"@type":"ListItem","position":1,"name":"Home","item":U+"/"}]
        acc=""
        for i,p in enumerate(parts):
            acc+="/"+p
            items.append({"@type":"ListItem","position":i+2,"name":title if i==len(parts)-1 else p.replace("-"," ").title(),"item":U+acc+"/"})
        crumbs=[{"@type":"BreadcrumbList","itemListElement":items}]
    h=head(title,desc,path,(ld or [])+crumbs,image)+chrome(body,path)
    if not index: h=h.replace('content="index,follow,max-image-preview:large"','content="noindex"')
    d=os.path.join(OUT,path.strip("/"))
    if not path.endswith(".html"): os.makedirs(d,exist_ok=True)
    open(os.path.join(d,"index.html") if not path.endswith(".html") else d,"w").write(h)
    if index: pages.append((path, lastmod or "2026-10-27"))
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
<p class="small">Find any pair by its code in our <a href="/style-codes/">sneaker style code index</a>{(' or read <a href="/news/nike-style-code-lookup/">how to look up a Nike style code</a>') if r['brand'] in ('Nike','Jordan') else ''}.</p>
<aside class="buy-box" aria-labelledby="wtb"><h2 id="wtb">Where to buy</h2><ul>{buy}</ul><p class="small">Links go to the official retailer. Dates, prices and stock can change; the retailer's page has the final word. We do not sell shoes. See our <a href="/affiliate-disclosure/">affiliate disclosure</a>.</p></aside>
<section class="sources"><h2>Source</h2><ol><li><a href="{e(r['src'][1])}">{e(r['src'][0])}</a></li></ol></section>
<p><a href="/releases/">Back to the release calendar</a></p></article>"""
    lm="2026-10-29" if r["date"]>="2026-10-29" and r["sku"] in ("A23933C-832","KK2813") else "2026-10-27"
    rtitle=f"{r['name']} ({r['sku']}) release date and price"
    if len(rtitle)>70: rtitle=f"{r['name']} ({r['sku']}) release date"
    if len(rtitle)>70: rtitle=f"{r['name']} ({r['sku']})"
    rdesc=f"{r['name']} releases {nice(r['date'])} for ${r['price']}. Style code {r['sku']}, where to buy and sources."
    ld=[{"@type":"Product","name":r["name"],"sku":r["sku"],"brand":{"@type":"Brand","name":r["brand"]},"releaseDate":r["date"]},
        {"@type":"NewsArticle","headline":rtitle,"description":rdesc,"datePublished":lm+"T00:00:00Z","dateModified":lm+"T00:00:00Z","mainEntityOfPage":U+"/shoes/"+r["slug"]+"/","author":{"@type":"Organization","name":N+" desk","url":U+"/about/"},"publisher":{"@id":U+"/#org"},"isBasedOn":[r["src"][1]]}]
    write(f"/shoes/{r['slug']}/",rtitle,rdesc,body,ld,lastmod=lm)
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
write("/releases/","Sneaker release dates calendar","Fast, filterable sneaker release calendar: dates, retail prices and style codes for Nike, Jordan, adidas and more, with where to buy links.",cal,lastmod=NOW.date().isoformat())
# style code index: one lookup table, every code links to its shoe page
_codes=sorted(REL,key=lambda r:r["sku"].upper())
_rows="".join(f'<tr data-q="{e((r["sku"]+" "+r["name"]+" "+r["brand"]).lower())}"><td><code>{e(r["sku"])}</code></td><td><a href="/shoes/{r["slug"]}/">{e(r["name"])}</a></td><td>{e(r["brand"])}</td><td><time datetime="{r["date"]}">{nice(r["date"])}</time></td><td>${r["price"]}</td></tr>' for r in _codes)
_sc=f"""<h1>Sneaker style code lookup</h1><p class="dek">Type a style code (the SKU printed on the box label and the size tag) to find the shoe, its release date and retail price. {len(_codes)} codes from our release calendar, each linked to a sourced shoe page.</p>
<p><label for="sc-q">Search by code or name </label><input id="sc-q" type="search" placeholder="e.g. {e(_codes[0]["sku"])}" autocomplete="off"></p>
<div class="table-wrap"><table class="sc-table"><thead><tr><th scope="col">Style code</th><th scope="col">Shoe</th><th scope="col">Brand</th><th scope="col">Release date</th><th scope="col">Retail (US)</th></tr></thead><tbody id="sc-body">{_rows}</tbody></table></div>
<h2>Where to find a style code</h2><p>Nike and Jordan print the style code on the box label and on the tag inside the shoe, in the form of six characters, a dash and three digits. adidas and New Balance use their own article or model codes. See <a href="/news/nike-style-code-lookup/">how to look up a Nike style code</a> and <a href="/news/how-to-check-a-nike-box-label-for-authenticity/">how to check a Nike box label</a>.</p>
<p class="small">Codes, dates and prices come from the source cited on each shoe page. A code that is not listed here is not yet in our <a href="/releases/">release calendar</a>.</p>
<script>document.getElementById("sc-q").addEventListener("input",function(){{var q=this.value.trim().toLowerCase();document.querySelectorAll("#sc-body tr").forEach(function(t){{t.hidden=q&&t.dataset.q.indexOf(q)<0;}});}});</script>"""
write("/style-codes/","Sneaker style code lookup: find a shoe by SKU","Look up a sneaker by its style code or SKU: shoe name, brand, release date and retail price for every pair in our sourced release calendar.",_sc,[{"@type":"Dataset","name":"Sneaker style code index","description":"Style codes (SKUs) with shoe name, brand, release date and US retail price, each linked to a sourced shoe page.","url":U+"/style-codes/","creator":{"@id":U+"/#org"},"isAccessibleForFree":True}],lastmod=NOW.date().isoformat())
# restocks
rs="".join(f'<li class="rel"><time datetime="{d}">{datetime.date.fromisoformat(d).strftime("%b %-d")}</time><span class="rel-main"><strong>{e(n)}</strong><span class="meta">{e(w)}{" · "+e(k) if k else ""} · reported by <a href="{e(su)}">{e(sn)}</a></span></span><span class="price">{"$"+str(p) if p else "See retailer"}</span></li>' for n,d,w,p,k,(sn,su) in RESTOCKS)
write("/restocks/","Sneaker restocks log","A sourced log of recent sneaker restocks: what came back, where, at what retail price, and who reported it.",f"<h1>Sneaker restocks</h1><p class='dek'>Recent restocks, newest first. Each entry links to the original report. Stock moves fast, so check the retailer right away.</p><ul class='rel-list'>{rs}</ul><p><a href='/news/october-2026-sneaker-restocks-nike-mind-air-bakin/'>Read the October restocks roundup</a></p>")
write("/raffles/","Sneaker raffles and draws","How sneaker raffles and draws work, and the open raffles we have verified with the retailer.",
"""<h1>Sneaker raffles and draws</h1><p class="dek">We list a raffle only after we confirm it on the retailer's own page. There are no verified open raffles on this page right now.</p>
<h2>How raffles work</h2><p>A raffle or draw lets you enter for the chance to buy a pair at retail. Retailers pick winners at random and charge only the winners. Nike runs many launches on the SNKRS app as timed draws. Enter only through the retailer's own site or app, never through a link that asks for a fee to enter.</p>
<h2>Staying safe</h2><ul><li>Check the web address belongs to the retailer.</li><li>No genuine retailer raffle charges an entry fee.</li><li>Watch for winner emails that ask you to pay through a new link; go to the retailer directly instead.</li></ul>
<p>See the <a href="/releases/">release calendar</a> for upcoming dates.</p>""")
# articles
ART=sorted(ARTICLES,key=lambda a:pub_dt(a),reverse=True)
_BYART={a["slug"]:a for a in ART}
_OKIMG=legal_gate.rights()
_GUIDE_SLUGS={"how-online-sneaker-raffles-work","how-nike-snkrs-draw-and-line-launches-work","snkrs-exclusive-access","adidas-confirmed-app-raffle-queue-invite","snkrs-vs-retailers","how-to-spot-a-fake-sneaker-release-ad-or-raffle","what-is-a-sneaker-restock-and-how-to-catch-one","how-restocks-work-at-nike-foot-locker-and-finish-line","air-jordan-4-bred-2026-where-to-buy","air-jordan-11-green-screen-where-to-buy","adidas-ae-3-lucid-pink-where-to-buy","nike-sizing-by-model","adidas-shoe-size-chart-us-uk-eu","new-balance-shoe-widths-explained","nike-kids-shoe-sizes-c-and-y-explained","how-stockx-and-goat-verify-sneakers","how-to-check-a-nike-box-label-for-authenticity","nike-style-code-lookup","can-you-return-snkrs-launch-sneakers-nike-terms-of-sale","shipping-delays-mail-order-rule"}
_STOP={"the","and","for","with","from","this","that","your","how","what","when","where","who","are","was","were","has","have","its","into","over","than","then","them","they","will","just","back","out","off","all","new","low","high","retro","release","releases","date","dates","november","december","october","january","february","march","sneaker","sneakers","shoes","shoe","pair","pairs","nike","adidas","jordan","air","balance","pro","protro","womens","women","mens","men","size","sizes","2026","2025","today","tomorrow","yesterday","tonight","launches","launch","launched","still","coming","first","official","images","live","now","went","available","price","retail","returns","return","dropping","drops","drop","week","weeks","original","colorway","colourway","friday","saturday","sunday","monday","tuesday","wednesday","thursday"}
_CAT_GUIDES={
 "Jordan":["how-nike-snkrs-draw-and-line-launches-work","nike-style-code-lookup","nike-sizing-by-model","how-to-spot-a-fake-sneaker-release-ad-or-raffle"],
 "Nike":["how-nike-snkrs-draw-and-line-launches-work","nike-style-code-lookup","snkrs-vs-retailers","how-to-spot-a-fake-sneaker-release-ad-or-raffle"],
 "adidas":["adidas-confirmed-app-raffle-queue-invite","adidas-shoe-size-chart-us-uk-eu","how-online-sneaker-raffles-work"],
 "New Balance":["new-balance-shoe-widths-explained","how-online-sneaker-raffles-work","nike-style-code-lookup"],
 "Restocks":["what-is-a-sneaker-restock-and-how-to-catch-one","how-restocks-work-at-nike-foot-locker-and-finish-line","how-to-spot-a-fake-sneaker-release-ad-or-raffle"],
 "Raffles":["how-online-sneaker-raffles-work","how-to-spot-a-fake-sneaker-release-ad-or-raffle","how-nike-snkrs-draw-and-line-launches-work"],
 "Guides":["how-nike-snkrs-draw-and-line-launches-work","what-is-a-sneaker-restock-and-how-to-catch-one","nike-style-code-lookup"],
 "Release Dates":["nike-style-code-lookup","how-to-spot-a-fake-sneaker-release-ad-or-raffle","how-online-sneaker-raffles-work"],
}
_INTENT=[
 (re.compile(r"restock",re.I),["what-is-a-sneaker-restock-and-how-to-catch-one","how-restocks-work-at-nike-foot-locker-and-finish-line"]),
 (re.compile(r"raffle|\bdraw",re.I),["how-online-sneaker-raffles-work","how-to-spot-a-fake-sneaker-release-ad-or-raffle","how-nike-snkrs-draw-and-line-launches-work"]),
 (re.compile(r"SNKRS|style code",re.I),["how-nike-snkrs-draw-and-line-launches-work","nike-style-code-lookup","snkrs-exclusive-access"]),
 (re.compile(r"\bsize|sizing|width",re.I),["nike-sizing-by-model","nike-kids-shoe-sizes-c-and-y-explained","new-balance-shoe-widths-explained"]),
 (re.compile(r"\badidas|confirmed",re.I),["adidas-confirmed-app-raffle-queue-invite","adidas-shoe-size-chart-us-uk-eu"]),
 (re.compile(r"new balance",re.I),["new-balance-shoe-widths-explained"]),
 (re.compile(r"reebok|asics|puma|converse",re.I),["how-online-sneaker-raffles-work","how-to-spot-a-fake-sneaker-release-ad-or-raffle","what-is-a-sneaker-restock-and-how-to-catch-one"]),
 (re.compile(r"stockx|goat|authentic|box label",re.I),["how-stockx-and-goat-verify-sneakers","how-to-check-a-nike-box-label-for-authenticity"]),
]
def _toks(a):
    out=set()
    for w in re.findall(r"[a-z0-9]+",(a["title"]+" "+a["slug"]).lower()):
        if w in _STOP: continue
        if len(w)>3 or any(c.isdigit() for c in w): out.add(w)
    return out
def _ov(ta,tb):
    s=0
    for w in ta&tb: s+=1 if w.isdigit() else 4
    return s
def _add_pick(picked,seen,b):
    if not b or b["slug"] in seen: return
    img=b.get("image")
    if not img or img not in _OKIMG: return
    seen.add(b["slug"]); picked.append(b)
def pick_related(a):
    picked=[]; seen={a["slug"]}
    for href,_name in RELATED.get(a["slug"],[]):
        m=re.search(r"/news/([^/]+)/",href)
        if m: _add_pick(picked,seen,_BYART.get(m.group(1)))
    ta=_toks(a); cands=[]
    for b in ART:
        if b["slug"] in seen: continue
        s=_ov(ta,_toks(b))
        if a.get("category") and a.get("category")==b.get("category") and a.get("category") not in ("Release Dates","Guides"): s+=2
        if s>=4: cands.append((s,pub_dt(b),b))
    cands.sort(key=lambda x:(x[0],x[1]),reverse=True)
    for _s,_dt,b in cands:
        _add_pick(picked,seen,b)
        if len(picked)>=4: break
    if len(picked)<4:
        blob=a["title"]+" "+a["slug"]+" "+re.sub(r"<[^>]+>"," ",a.get("body",""))[:400]
        slugs=list(_CAT_GUIDES.get(a.get("category"),[]))
        for rx,gs in _INTENT:
            if rx.search(blob): slugs.extend(gs)
        for s in slugs:
            if len(picked)>=4: break
            _add_pick(picked,seen,_BYART.get(s))
    return picked[:4]
def next_html(items,heading):
    if len(items)<3: return ""
    lis="".join(f'<li><a href="/news/{b["slug"]}/"><img src="{e(b["image"])}" alt="" width="160" height="90" loading="lazy" decoding="async"><span>{e(b["title"])}</span></a></li>' for b in items)
    return f'<nav class="next-reads" aria-label="{e(heading)}"><h2>{heading}</h2><ul class="next-read-list">{lis}</ul><p class="small">Story photos are <a href="/image-policy/">AI-generated</a>.</p></nav>'
def insert_mid(body,block):
    if not block: return body
    parts=body.split("</p>")
    if len(parts)>=4: return "</p>".join(parts[:2])+"</p>"+block+"</p>".join(parts[2:])
    h=body.find("</h2>")
    if h!=-1: return body[:h+5]+block+body[h+5:]
    return body+block
_LINK_RULES=[
 (re.compile(r"\bstyle codes?\b",re.I),"/style-codes/"),
 (re.compile(r"\bSNKRS\b"),"/news/how-nike-snkrs-draw-and-line-launches-work/"),
 (re.compile(r"\bFoot Locker\b"),"/news/how-restocks-work-at-nike-foot-locker-and-finish-line/"),
 (re.compile(r"\braffles?\b",re.I),"/news/how-online-sneaker-raffles-work/"),
 (re.compile(r"\brestocks?\b",re.I),"/news/what-is-a-sneaker-restock-and-how-to-catch-one/"),
 (re.compile(r"\brelease calendar\b",re.I),"/releases/"),
]
def autolink(body,a):
    rules=list(_LINK_RULES)
    title=a["title"]; cat=a.get("category") or ""
    if re.search(r"\bJordan\b",title) or cat=="Jordan": rules.append((re.compile(r"\bJordan\b"),"/brands/jordan/"))
    elif re.search(r"\badidas\b",title,re.I) or cat=="adidas": rules.append((re.compile(r"\badidas\b"),"/brands/adidas/"))
    elif re.search(r"New Balance",title) or cat=="New Balance": rules.append((re.compile(r"\bNew Balance\b"),"/brands/new-balance/"))
    elif re.search(r"\bNike\b",title) or cat=="Nike": rules.append((re.compile(r"\bNike\b"),"/brands/nike/"))
    existing=set(re.findall(r'href="([^"]+)"',body))
    parts=re.split(r"(<[^>]+>)",body)
    in_a=in_h=0; added=0; used=set()
    for i,part in enumerate(parts):
        if part.startswith("<"):
            if re.match(r"<a\b",part,re.I): in_a+=1
            elif re.match(r"</a\b",part,re.I): in_a=max(0,in_a-1)
            elif re.match(r"<h[1-6]\b",part,re.I): in_h+=1
            elif re.match(r"</h[1-6]\b",part,re.I): in_h=max(0,in_h-1)
            continue
        if in_a or in_h or added>=3: continue
        for rx,href in rules:
            if href in existing or href in used: continue
            if href.rstrip("/")==f"/news/{a['slug']}": continue
            m=rx.search(part)
            if not m: continue
            part=part[:m.start()]+f'<a href="{href}">{m.group(0)}</a>'+part[m.end():]
            used.add(href); added+=1
            break
        parts[i]=part
    return "".join(parts)
def background_links(a,picked):
    used={f"/news/{b['slug']}/" for b in picked}
    links=[]
    def add(href,text):
        if href in used or any(h==href for h,_ in links): return
        links.append((href,text)); used.add(href)
    blob=(a["title"]+" "+a["slug"]).lower()
    if "jordan" in blob or a.get("category")=="Jordan": add("/brands/jordan/","Jordan hub: dates, stories and buying guides")
    elif "adidas" in blob or a.get("category")=="adidas": add("/brands/adidas/","adidas hub: dates, stories and buying guides")
    elif "new balance" in blob or a.get("category")=="New Balance": add("/brands/new-balance/","New Balance hub: dates, stories and buying guides")
    elif re.search(r"nike|snkrs|kobe|dunk|foamposite",blob) or a.get("category")=="Nike": add("/brands/nike/","Nike hub: dates, stories and buying guides")
    is_guide=a["slug"] in _GUIDE_SLUGS or a.get("category")=="Guides"
    if is_guide:
        add("/guides/","All sneaker guides"); add("/style-codes/","Style code lookup"); add("/releases/","Release calendar")
    elif a.get("category")=="Restocks" or "restock" in blob:
        add("/restocks/","Restock log"); add("/news/what-is-a-sneaker-restock-and-how-to-catch-one/","What a sneaker restock is, and how to catch one"); add("/news/how-to-spot-a-fake-sneaker-release-ad-or-raffle/","How to spot a fake release ad or raffle"); add("/guides/","Sneaker guides")
    elif a.get("category")=="Raffles" or "raffle" in blob:
        add("/raffles/","Raffles and draws"); add("/news/how-online-sneaker-raffles-work/","How online sneaker raffles work"); add("/guides/","Sneaker guides")
    else:
        add("/releases/","Release calendar"); add("/guides/","Sneaker guides"); add("/style-codes/","Style code lookup")
    ta=_toks(a); later=[]
    for b in ART:
        if b["slug"]==a["slug"] or pub_dt(b)<=pub_dt(a): continue
        if _ov(ta,_toks(b))>=4: later.append(b)
    if later:
        later.sort(key=pub_dt,reverse=True)
        b=later[0]
        add(f"/news/{b['slug']}/","Later coverage: "+b["title"])
    return links,is_guide
_REL_OK=_REL_SHORT=0
for a in ART:
    srcs="".join(f'<li><a href="{e(u)}">{e(t)}</a> <span class="source-meta">{e(p)}, {nice(d)}</span></li>' for t,u,p,d in a["sources"])
    iso,label=stamp(a)
    published=pub_dt(a).strftime("%Y-%m-%dT%H:%M:%SZ")
    if a.get("updated"):
        raw=a["updated"]; mod_dt=datetime.datetime.fromisoformat(raw[:10]+"T18:00:00+00:00") if len(raw)<=10 else datetime.datetime.fromisoformat(raw)
        if mod_dt.tzinfo is None: mod_dt=mod_dt.replace(tzinfo=datetime.timezone.utc)
        pub=pub_dt(a)
        if mod_dt<pub: mod_dt=pub
        modified=mod_dt.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        mod_label=nice(mod_dt.astimezone(ZoneInfo("America/New_York")).date().isoformat())
        lastmod=mod_dt.astimezone(datetime.timezone.utc).date().isoformat()
    else:
        modified,mod_label,lastmod=published,label,a["date"]
    fig=""
    if a.get("image"):
        fig=f'<figure class="story-figure"><img src="{e(a["image"])}" alt="{e(a.get("image_alt") or a["title"])}" width="1280" height="720"><figcaption>AI-generated image. <a class="src" href="/image-policy/">Source</a></figcaption></figure>'
    prose=a["body"]
    if len(re.findall(r'href="(/[^"]+)"',prose))<3: prose=autolink(prose,a)
    reads=pick_related(a)
    if len(reads)>=3: _REL_OK+=1
    else: _REL_SHORT+=1
    prose=insert_mid(prose,next_html(reads,"Read next"))
    end=next_html(reads,"Keep reading")
    bglinks,is_guide=background_links(a,reads)
    bg_h="More on this" if is_guide else "Background"
    bg=""
    if bglinks:
        blis="".join(f'<li><a href="{href}">{e(text)}</a></li>' for href,text in bglinks)
        bg=f'<aside class="background-reads" aria-label="{e(bg_h)}"><h2>{bg_h}</h2><ul>{blis}</ul></aside>'
    body=f"""<article class="story-page"><header class="article-head"><p class="story-kicker"><span class="chip">{e(a['category'])}</span> <time datetime="{iso}">{e(label)}</time></p><h1>{e(a['title'])}</h1><p class="byline">By the {N} desk</p><p class="dek">{e(a['description'])}</p><p class="last-updated">Last updated <time datetime="{modified}">{e(mod_label)}</time></p></header>
{fig}<div class="prose">{prose}</div><section class="sources" aria-labelledby="sh"><h2 id="sh">Sources</h2><ol>{srcs}</ol></section>{end}{bg}</article>"""
    ld=[{"@type":"NewsArticle","headline":a["title"],"description":a["description"],"datePublished":published,"dateModified":modified,"mainEntityOfPage":U+"/news/"+a["slug"]+"/","author":{"@type":"Organization","name":N+" desk","url":U+"/about/"},"publisher":{"@id":U+"/#org"},"isBasedOn":[s[1] for s in a["sources"]]}]
    if a.get("image"): ld[0]["image"]=U+a["image"]
    write(f"/news/{a['slug']}/",a["title"],a["description"],body,ld,lastmod=lastmod,image=a.get("image"))
cards="".join(f'<li class="story-card"><p class="story-kicker"><span class="chip">{e(a["category"])}</span> <time datetime="{stamp(a)[0]}">{e(stamp(a)[1])}</time></p><h3><a href="/news/{a["slug"]}/">{e(a["title"])}</a></h3><p>{e(a["description"])}</p></li>' for a in ART)
write("/news/","Sneaker news","Sourced sneaker release and restock news.",f"<h1>Sneaker news</h1><ul class='story-grid'>{cards}</ul>",lastmod=max((a["date"] for a in ART), default="2026-10-27"))
# guides hub: evergreen how-to and where-to-buy pages, grouped by task
GUIDE_GROUPS=[("Raffles, draws and drops",["how-online-sneaker-raffles-work","how-nike-snkrs-draw-and-line-launches-work","snkrs-exclusive-access","adidas-confirmed-app-raffle-queue-invite","snkrs-vs-retailers","how-to-spot-a-fake-sneaker-release-ad-or-raffle"]),
 ("Restocks and where to buy",["what-is-a-sneaker-restock-and-how-to-catch-one","how-restocks-work-at-nike-foot-locker-and-finish-line","air-jordan-4-bred-2026-where-to-buy","air-jordan-11-green-screen-where-to-buy","adidas-ae-3-lucid-pink-where-to-buy"]),
 ("Sizing and fit",["nike-sizing-by-model","adidas-shoe-size-chart-us-uk-eu","new-balance-shoe-widths-explained","nike-kids-shoe-sizes-c-and-y-explained"]),
 ("Authenticity and style codes",["how-stockx-and-goat-verify-sneakers","how-to-check-a-nike-box-label-for-authenticity","nike-style-code-lookup"]),
 ("Returns and shipping",["can-you-return-snkrs-launch-sneakers-nike-terms-of-sale","shipping-delays-mail-order-rule"])]
_BY={a["slug"]:a for a in ART}
def guide_li(sl):
    a=_BY.get(sl)
    return f'<li class="story-card"><h3><a href="/news/{a["slug"]}/">{e(a["title"])}</a></h3><p>{e(a["description"])}</p></li>' if a else ""
ghub="<h1>Sneaker guides</h1><p class='dek'>Evergreen how-to pages for buying sneakers at retail: how raffles and drops work, where restocks come from, sizing by brand, and how resale platforms check pairs. Every guide cites the brand or store's own pages.</p>"
for gname,sls in GUIDE_GROUPS:
    lis="".join(guide_li(x) for x in sls)
    if lis: ghub+=f"<section><h2 class='section-title'>{e(gname)}</h2><ul class='story-grid'>{lis}</ul></section>"
ghub+="<p>Browse by brand: <a href='/brands/nike/'>Nike</a>, <a href='/brands/jordan/'>Jordan</a>, <a href='/brands/adidas/'>adidas</a> and <a href='/brands/new-balance/'>New Balance</a>. Look up a pair by SKU in the <a href='/style-codes/'>style code index</a>. For dates, see the <a href='/releases/'>release calendar</a>, the <a href='/restocks/'>restocks log</a> and the <a href='/raffles/'>raffles page</a>.</p>"
_gl=[_BY[x]["date"] for _,sls in GUIDE_GROUPS for x in sls if x in _BY]
write("/guides/","Sneaker guides: raffles, restocks, sizing and authenticity","How sneaker raffles, drops and restocks work, brand size charts, and how resale platforms verify pairs. Sourced evergreen guides.",ghub,[{"@type":"CollectionPage","name":"Sneaker guides","url":U+"/guides/"}],lastmod=max(_gl) if _gl else "2026-11-12")
import hubs
BRAND_LIST=hubs.build_hubs(ART,REL,write,e,relrow,stamp,NOW.date().isoformat(),U)
HOME_BRANDS=" · ".join(f'<a href="/brands/{b["slug"]}/">{e(b["name"])}</a>' for b in BRAND_LIST)
HOME_GUIDES="".join(f'<li><a href="/news/{x}/">{e(_BY[x]["title"])}</a></li>' for x in ["how-online-sneaker-raffles-work","what-is-a-sneaker-restock-and-how-to-catch-one","nike-sizing-by-model","adidas-shoe-size-chart-us-uk-eu","new-balance-shoe-widths-explained","how-stockx-and-goat-verify-sneakers"] if x in _BY)
today=NOW.date().isoformat(); up=[r for r in REL if r["date"]>=today][:8]
home=f"""<section class="hero"><h1 class="visually-hidden">{N}</h1><p class="hero-kicker">Release dates, restocks and raffles</p><p class="hero-lead">The fastest way to see what drops next, what it costs and where to buy it.</p><p><a class="buy-btn" href="/releases/">Open the release calendar</a></p></section>
<section aria-labelledby="up"><h2 id="up" class="section-title">Dropping next</h2><ul class="rel-list">{''.join(relrow(r) for r in up)}</ul><p><a href="/releases/">Full calendar</a></p></section>
<section aria-labelledby="ln"><h2 id="ln" class="section-title">Latest news</h2><ul class="story-grid">{cards}</ul></section>
<section aria-labelledby="gd"><h2 id="gd" class="section-title">Sneaker guides</h2><ul>{HOME_GUIDES}</ul><p><a href="/guides/">All guides</a> · Brand hubs: {HOME_BRANDS}</p></section>
<section aria-labelledby="rs"><h2 id="rs" class="section-title">Recent restocks</h2><ul class="rel-list">{rs}</ul></section>"""
write("/",N,"Fast sneaker release calendar, restock log and raffle guide with prices, style codes and where to buy links. Every fact sourced.",home,[{"@type":"WebSite","name":N,"url":U+"/","publisher":{"@id":U+"/#org"}}],lastmod=NOW.date().isoformat())
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
page("/sources-ethics/","Sources & Ethics","How "+N+" sources and checks sneaker news.","<p>Every fact links to a named source in the sentence. We prefer the brand's own product and launch pages, then credited release calendars and reporting. We write in our own words, quote briefly with attribution, report company announcements as what the company says, and label any opinion. We do not invent quotes, prices or dates. News images are original editorial pictures made for this site and are AI-generated; each links to our <a href='/image-policy/'>image policy</a>. They are not photographs of a product. We do not use third-party photos.</p>")
page("/corrections/","Corrections","How to request a correction on "+N+".","<p>If we got something wrong, <a href='/contact/'>tell us</a>. We fix errors quickly and note material corrections at the end of the article.</p>")
page("/terms/","Terms of Use","Terms of use for "+N+".",f"<p>By using {N} you agree to these terms. The site is operated by Joshua Israel Ventures LLC, a Florida limited liability company, under the trade name {N}.</p><h2>Information only</h2><p>Content is general news and information. Release dates, prices and stock change, and the retailer's page controls. We are not a retailer and do not sell, hold or ship products.</p><h2>Third party links</h2><p>We link to retailers and sources we do not control and are not responsible for their content, offers or practices.</p><h2>Limitation of liability</h2><p>To the fullest extent permitted by law, the site is provided as is, without warranties, and we are not liable for any loss arising from its use, including a missed release or a purchase decision.</p><h2>Intellectual property</h2><p>Brand names and product names belong to their owners and are used only to identify products. See our <a href='/copyright/'>Copyright and DMCA policy</a>.</p><h2>Governing law</h2><p>These terms are governed by the laws of the State of Florida, United States, without regard to conflict of law rules, and disputes will be resolved in the courts located in Florida.</p><h2>Changes</h2><p>We may update these terms; the date below shows the latest version. Last updated October 27, 2026.</p>",legal=True)
page("/privacy/","Privacy Policy","How "+N+" handles your data, including Google Analytics 4 and Google AdSense.",f"<p>This policy explains what data {N} collects. Last updated November 5, 2026.</p><h2 id='google-analytics'>Google Analytics 4</h2><p>With your consent, we use Google Analytics 4, a service from Google LLC, to measure visits and improve the site. Google Analytics 4 loads only after you click Accept in our cookie banner. It sets cookies such as _ga and collects data like pages viewed, device type and approximate location. We turn off Google signals and ad personalization. You can change your choice any time with the Cookie choices button in the footer. See <a href='https://policies.google.com/technologies/partner-sites'>how Google uses data from sites that use its services</a>.</p><h2>Cloudflare Web Analytics</h2><p>We may use Cloudflare Web Analytics, a privacy focused tool that does not use cookies, to count page views.</p><h2>Contact form</h2><p>Messages are delivered by FormSubmit to our inbox and used only to reply.</p><h2>Advertising and affiliate links</h2><p>We may show advertisements through Google AdSense. Google and other third-party advertising vendors may use cookies and similar technologies to serve, measure and personalize ads, including based on your visits to this and other sites, subject to your consent where required. You can opt out of personalized advertising at <a href='https://adssettings.google.com'>https://adssettings.google.com</a>. See <a href='https://policies.google.com/technologies/ads'>how Google uses advertising cookies</a>. Affiliate links, when we use them, are described on our <a href='/affiliate-disclosure/'>affiliate disclosure</a>.</p><h2>Google advertising cookies and your choices</h2><p>Third-party vendors, including Google, use cookies to serve ads based on a user’s prior visits to this website or other websites. Google’s use of advertising cookies enables it and its partners to serve ads based on your visit to this site and/or other sites on the Internet. You may opt out of personalized advertising by visiting <a href='https://adssettings.google.com/' rel='nofollow noopener'>Google Ads Settings</a>. Alternatively, you can opt out of a third-party vendor’s use of cookies for personalized advertising at <a href='https://www.aboutads.info/choices/' rel='nofollow noopener'>aboutads.info/choices</a>. For more information, see <a href='https://policies.google.com/technologies/partner-sites' rel='nofollow noopener'>how Google uses information from sites or apps that use its services</a>.</p><h2>Your rights</h2><p>You can ask us to access or delete data you sent us through the <a href='/contact/'>contact form</a>. We do not sell personal information.</p><h2>Children</h2><p>The site is not directed to children under 13.</p>",legal=True)
page("/image-policy/","Image policy","Where the pictures on "+N+" come from.",f"<p>News images on {N} are AI-generated editorial illustrations made for this site. They are not photographs of the product, the release or any real person, and we do not use third-party photos.</p><p>Each image carries a \"Source\" link under it that leads to this page.</p>")
page("/disclaimer/","Disclaimer","Disclaimer for "+N+".",f"<p>{N} publishes news and information about sneaker releases, restocks and raffles. It is not purchasing, financial or resale advice. Dates, prices, sizes and stock come from cited sources and can change at any time; always confirm with the retailer. {N} is independent and is not affiliated with or endorsed by Nike, Jordan Brand, adidas or any other brand or retailer mentioned. Product names and trademarks belong to their owners.</p>",legal=True)
page("/copyright/","Copyright & DMCA","Copyright and DMCA policy for "+N+".",f"<p>We write original text. News images are original editorial pictures made for this site and are AI-generated; each links to our <a href='/image-policy/'>image policy</a>. They are not photographs of a product, and we do not use third-party photos. If you believe content on {N} infringes your copyright, send a notice through our <a href='/contact/'>contact form</a> with: your contact details, the work you claim is infringed, the URL of the material, a statement of good faith belief that the use is not authorized, a statement that the notice is accurate and that you are the owner or authorized to act, and your signature. We remove material promptly on a valid notice and may restore it on a valid counter notice.</p>",legal=True)
page("/affiliate-disclosure/","Affiliate Disclosure","Affiliate and advertising disclosure for "+N+".",f"<p>{N} may earn a commission when you buy through some retailer links on this site, at no extra cost to you. Right now our where to buy links are plain links to official retailers. When a link becomes an affiliate link, this page and the link label will say so. Commissions never decide what we cover or how we rank releases.</p>",legal=True)
write("/404.html","Page not found","Page not found.","<h1>Page not found</h1><p>Try the <a href='/releases/'>release calendar</a> or the <a href='/'>homepage</a>.</p>",index=False)
# seo files
sm="".join(f"<url><loc>{U}{p}</loc><lastmod>{lm}</lastmod></url>" for p,lm in pages)
open(f"{OUT}/sitemap.xml","w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>')
bots=["Googlebot","Mediapartners-Google","Bingbot","OAI-SearchBot","GPTBot","ChatGPT-User","PerplexityBot","ClaudeBot","Claude-SearchBot","Google-Extended","Applebot","Applebot-Extended","CCBot","DuckDuckBot"]
open(f"{OUT}/robots.txt","w").write("".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)+f"User-agent: *\nAllow: /\n\nSitemap: {U}/sitemap.xml\n")
open(f"{OUT}/ads.txt","w").write("google.com, pub-5681559774142917, DIRECT, f08c47fec0942fa0\n")
open(f"{OUT}/{SITE['indexnow_key']}.txt","w").write(SITE["indexnow_key"])
open(f"{OUT}/CNAME","w").write("restockrally.com\n"); open(f"{OUT}/.nojekyll","w").write("")
open(f"{OUT}/llms.txt","w").write(f"# {N}\n\n> {SITE['tagline']}. Sourced sneaker release dates, restocks and raffles.\n\n## Key pages\n- [Release calendar]({U}/releases/)\n- [Restocks]({U}/restocks/)\n- [Raffles]({U}/raffles/)\n- [Guides]({U}/guides/)\n- [Brand hubs]({U}/brands/)\n- [Sneaker style code lookup]({U}/style-codes/)\n- [Nike]({U}/brands/nike/)\n- [Jordan]({U}/brands/jordan/)\n- [adidas]({U}/brands/adidas/)\n- [New Balance]({U}/brands/new-balance/)\n- [News]({U}/news/)\n- [Sources & Ethics]({U}/sources-ethics/)\n\n## Articles\n"+"".join(f"- [{a['title']}]({U}/news/{a['slug']}/): {a['description']}\n" for a in ART))
items="".join(f"<item><title>{e(a['title'])}</title><link>{U}/news/{a['slug']}/</link><guid>{U}/news/{a['slug']}/</guid><pubDate>{pub_dt(a).strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate><description>{e(a['description'])}</description></item>" for a in ART)
open(f"{OUT}/feed.xml","w").write(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{N}</title><link>{U}/</link><description>{SITE["tagline"]}</description>{items}</channel></rss>')
# Legal hold gate layer 2: full-site backstop. If any built page is held, put docs/ back to the last committed version and fail.
if legal_gate.main([]) != 0:
    root=os.path.dirname(OUT)
    subprocess.run(["git","checkout","--","docs"],cwd=root); subprocess.run(["git","clean","-fdq","docs"],cwd=root)
    print("HOLD_REVIEW: build refused, docs/ restored to the last published version"); sys.exit(3)
print(len(pages),"pages")
print(f"next-reads: {_REL_OK} articles with 3 or more, {_REL_SHORT} with fewer")
