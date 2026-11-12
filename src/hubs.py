# Brand topic hubs (added 12 Nov 2026): one evergreen page per major brand that collects upcoming releases,
# buying guides and every news story about that brand. Pages rebuild from articles and release data on each build.
import re
BRANDS = [
 {"slug":"nike","name":"Nike","rel":["Nike"],"kw":r"\b(nike|snkrs|kobe|foamposite|air max|dunk|air force|nocta|skims)\b","not_cat":["Jordan"],
  "intro":'Nike launches most limited pairs through the <a href="https://www.nike.com/launch">SNKRS launch calendar</a>, by Draw, Line or Exclusive Access. This page collects our Nike release dates, guides to how those launches work, and every Nike story we have published, each with its sources.',
  "guides":["how-nike-snkrs-draw-and-line-launches-work","snkrs-exclusive-access","snkrs-vs-retailers","nike-sizing-by-model","nike-kids-shoe-sizes-c-and-y-explained","nike-style-code-lookup","how-to-check-a-nike-box-label-for-authenticity","can-you-return-snkrs-launch-sneakers-nike-terms-of-sale"]},
 {"slug":"jordan","name":"Jordan","rel":["Jordan"],"kw":r"\b(jordan|aj\d+|spizike)\b","not_cat":[],
  "intro":'Jordan Brand retros and new models usually launch on Nike\'s <a href="https://www.nike.com/launch">SNKRS calendar</a> and at partner stores. This page collects our Air Jordan release dates, the guides that apply to Jordan launches, and every Jordan story we have published, each with its sources.',
  "guides":["how-nike-snkrs-draw-and-line-launches-work","snkrs-vs-retailers","how-online-sneaker-raffles-work","nike-sizing-by-model","nike-style-code-lookup","how-stockx-and-goat-verify-sneakers"]},
 {"slug":"adidas","name":"adidas","rel":["adidas"],"kw":r"\b(adidas|yeezy|wales bonner)\b","not_cat":[],
  "intro":'adidas releases limited pairs and collaborations through its <a href="https://www.adidas.com/us/confirmed">CONFIRMED app</a> by raffle, queue or invite. This page collects our adidas release dates, guides to CONFIRMED and adidas sizing, and every adidas story we have published, each with its sources.',
  "guides":["adidas-confirmed-app-raffle-queue-invite","adidas-shoe-size-chart-us-uk-eu","how-online-sneaker-raffles-work","how-stockx-and-goat-verify-sneakers"]},
 {"slug":"new-balance","name":"New Balance","rel":["New Balance"],"kw":r"\b(new balance|990v\d|abzorb)\b","not_cat":[],
  "intro":'New Balance sells many models in several widths, and its collaborations often launch through partner boutiques as well as its own site. This page collects our New Balance release dates, our width guide, and every New Balance story we have published, each with its sources.',
  "guides":["new-balance-shoe-widths-explained","how-online-sneaker-raffles-work","how-restocks-work-at-nike-foot-locker-and-finish-line","how-stockx-and-goat-verify-sneakers"]},
]
def brand_of(a, b):
    if a.get("category") in b["not_cat"]: return False
    if a.get("category") == b["name"]: return True
    return re.search(b["kw"], (a["title"]+" "+a["slug"].replace("-"," ")).lower()) is not None

def build_hubs(ART, REL, write, e, relrow, stamp, today, U):
    by = {a["slug"]: a for a in ART}
    links = []
    for b in BRANDS:
        if b["slug"] == "nike":
            news = [a for a in ART if brand_of(a, b) and not brand_of(a, BRANDS[1])]
        else:
            news = [a for a in ART if brand_of(a, b)]
        guides = [by[s] for s in b["guides"] if s in by]
        gslugs = {g["slug"] for g in guides}
        news = [a for a in news if a["slug"] not in gslugs and a.get("category") != "Guides"]
        up = [r for r in REL if r["brand"] in b["rel"] and r["date"] >= today]
        rel_html = f'<ul class="rel-list">{"".join(relrow(r) for r in up[:12])}</ul><p><a href="/releases/">Full release calendar</a></p>' if up else '<p>No upcoming dates for this brand are on our <a href="/releases/">release calendar</a> right now.</p>'
        g_html = "".join(f'<li><a href="/news/{g["slug"]}/">{e(g["title"])}</a></li>' for g in guides)
        n_html = "".join(f'<li class="story-card"><p class="story-kicker"><span class="chip">{e(a["category"])}</span> <time datetime="{stamp(a)[0]}">{e(stamp(a)[1])}</time></p><h3><a href="/news/{a["slug"]}/">{e(a["title"])}</a></h3><p>{e(a["description"])}</p></li>' for a in news)
        body = f"""<h1>{e(b['name'])} sneaker releases, restocks and news</h1><p class="dek">{b['intro']}</p>
<section aria-labelledby="up"><h2 id="up" class="section-title">Upcoming {e(b['name'])} releases</h2>{rel_html}</section>
<section aria-labelledby="gd"><h2 id="gd" class="section-title">{e(b['name'])} buying guides</h2><ul>{g_html}</ul><p>More in our <a href="/guides/">sneaker guides</a>.</p></section>
<section aria-labelledby="nw"><h2 id="nw" class="section-title">{e(b['name'])} news</h2><ul class="story-grid">{n_html or '<li>No stories yet.</li>'}</ul></section>
<p class="small">Other brands: {" · ".join(f'<a href="/brands/{x["slug"]}/">{e(x["name"])}</a>' for x in BRANDS if x is not b)}. See all <a href="/brands/">brand hubs</a>.</p>"""
        items = [{"@type":"ListItem","position":i+1,"url":U+"/news/"+a["slug"]+"/"} for i,a in enumerate(news[:30])]
        ld = [{"@type":"CollectionPage","name":f"{b['name']} sneaker releases, restocks and news","url":U+f"/brands/{b['slug']}/","mainEntity":{"@type":"ItemList","itemListElement":items}}]
        lm = max([a["date"] for a in news + guides] or ["2026-11-12"])
        write(f"/brands/{b['slug']}/", f"{b['name']} sneaker releases, restocks and news", f"{b['name']} release dates, restock news and buying guides in one place, with retail prices, style codes and sources for every story.", body, ld, lastmod=lm)
        links.append((b, len(news), len(up)))
    idx = "".join(f'<li class="story-card"><h3><a href="/brands/{b["slug"]}/">{e(b["name"])}</a></h3><p>{n} stories, {u} upcoming release dates on the calendar.</p></li>' for b,n,u in links)
    write("/brands/", "Sneaker brand hubs", "Release dates, restock news and buying guides grouped by brand: Nike, Jordan, adidas and New Balance.", f"<h1>Sneaker brand hubs</h1><p class='dek'>Every story and release date we track, grouped by brand. Each hub links to the guides that apply to that brand's launches.</p><ul class='story-grid'>{idx}</ul><p>Looking for how to buy? Start with our <a href='/guides/'>sneaker guides</a>.</p>", [{"@type":"CollectionPage","name":"Sneaker brand hubs","url":U+"/brands/"}], lastmod=today)
    return BRANDS
