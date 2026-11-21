# Contextual internal links between 12 Nov news and evergreen guides.
RELATED = {
    "pharrell-adidas-virginia-adistar-jellyfish-kh6728-sneakersnstuff-november-21": [
        ("/news/adidas-don-issue-8-solar-turbo-ki9285-november-21-2026/", "adidas D.O.N. Issue 8 Solar Turbo, out the same morning"),
        ("/news/sneaker-releases-november-1-7-2026/", "November 1 to 7 roundup, including the earlier Jellyfish code"),
        ("/news/whitaker-group-adidas-campus-00s-do-not-duplicate-dash-grey-la6870-november-20/", "Whitaker Group adidas Campus 00s"),
        ("/news/adidas-shoe-size-chart-us-uk-eu/", "adidas shoe size chart"),
    ],
    "how-nike-snkrs-draw-and-line-launches-work": [
        ("/news/snkrs-exclusive-access/", "What SNKRS Exclusive Access is"),
        ("/news/air-jordan-4-bred-november-27-2026/", "Air Jordan 4 Bred, a later date on the SNKRS calendar"),
        ("/news/air-jordan-11-space-jam-2026-december-12-ct8012-900-235-jumpman-jam/", "Air Jordan 11 Space Jam, 12 December"),
        ("/news/corteiz-nike-shox-r419-metallic-silver-iq9951-001-november-20/", "Corteiz x Nike Shox R419"),
    ],
    "jordan-tatum-5-south-beach-november-12": [
        ("/news/nike-sizing-by-model/", "Nike sizing by model: charts, conversions and how to measure"),
        ("/news/nike-style-code-lookup/", "How to look up a Nike style code or SKU"),
        ("/brands/jordan/", "Jordan sneaker releases, restocks and news"),
    ],
    "carhartt-wip-nike-air-max-goadome-low-november-12": [
        ("/news/nike-style-code-lookup/", "How to look up a Nike style code or SKU"),
        ("/news/snkrs-exclusive-access/", "What SNKRS Exclusive Access is, and how Exclusive Draw differs"),
        ("/brands/nike/", "Nike sneaker releases, restocks and news"),
    ],
    "asap-rocky-puma-suede-94-navy-november-12": [
        ("/news/how-stockx-and-goat-verify-sneakers/", "How StockX and GOAT verify sneakers before they reach you"),
    ],
    "melitta-baumeister-nike-air-rift-rocker-november-12": [
        ("/news/snkrs-exclusive-access/", "What SNKRS Exclusive Access is, and how Exclusive Draw differs"),
        ("/news/nike-sizing-by-model/", "Nike sizing by model: charts, conversions and how to measure"),
        ("/brands/nike/", "Nike sneaker releases, restocks and news"),
    ],
    "union-nike-dunk-low-fatigue-november-13": [
        ("/news/snkrs-exclusive-access/", "What SNKRS Exclusive Access is, and how Exclusive Draw differs"),
        ("/news/nike-style-code-lookup/", "How to look up a Nike style code or SKU"),
        ("/news/how-to-check-a-nike-box-label-for-authenticity/", "How to read a Nike box label, and what it can tell you"),
        ("/brands/nike/", "Nike sneaker releases, restocks and news"),
    ],
    "nocta-nike-air-modmax-pink-spell": [
        ("/news/nike-style-code-lookup/", "How to look up a Nike style code or SKU"),
        ("/news/snkrs-exclusive-access/", "What SNKRS Exclusive Access is, and how Exclusive Draw differs"),
        ("/news/how-to-check-a-nike-box-label-for-authenticity/", "How to read a Nike box label, and what it can tell you"),
        ("/brands/nike/", "Nike sneaker releases, restocks and news"),
    ],
    "nike-sizing-by-model": [
        ("/news/jordan-tatum-5-south-beach-november-12/", 'Jordan Tatum 5 "South Beach" drops today at 10 a.m. ET for $135'),
        ("/news/melitta-baumeister-nike-air-rift-rocker-november-12/", "Melitta Baumeister x Nike women's Air Rift Rocker drops today on SNKRS at $220"),
        ("/brands/nike/", "Nike sneaker releases, restocks and news"),
    ],
    "nike-style-code-lookup": [
        ("/news/jordan-tatum-5-south-beach-november-12/", 'Jordan Tatum 5 "South Beach" drops today at 10 a.m. ET for $135'),
        ("/news/nocta-nike-air-modmax-pink-spell/", 'Drake\'s NOCTA x Nike Air Modmax "Pink Spell": $180, style IQ6711-600, date still firming up'),
        ("/news/union-nike-dunk-low-fatigue-november-13/", 'Union x Nike Dunk Low "Fatigue" set for 13 November on SNKRS at $130'),
    ],
    "snkrs-exclusive-access": [
        ("/news/melitta-baumeister-nike-air-rift-rocker-november-12/", "Melitta Baumeister x Nike women's Air Rift Rocker drops today on SNKRS at $220"),
        ("/news/union-nike-dunk-low-fatigue-november-13/", 'Union x Nike Dunk Low "Fatigue" set for 13 November on SNKRS at $130'),
        ("/news/carhartt-wip-nike-air-max-goadome-low-november-12/", "Carhartt WIP x Nike Air Max Goadome Low launches today on Carhartt WIP, wider release 20 November"),
    ],
    "how-to-check-a-nike-box-label-for-authenticity": [
        ("/news/union-nike-dunk-low-fatigue-november-13/", 'Union x Nike Dunk Low "Fatigue" set for 13 November on SNKRS at $130'),
        ("/news/nocta-nike-air-modmax-pink-spell/", 'Drake\'s NOCTA x Nike Air Modmax "Pink Spell": $180, style IQ6711-600, date still firming up'),
    ],
    "how-stockx-and-goat-verify-sneakers": [
        ("/news/union-nike-dunk-low-fatigue-november-13/", 'Union x Nike Dunk Low "Fatigue" set for 13 November on SNKRS at $130'),
        ("/news/asap-rocky-puma-suede-94-navy-november-12/", "A$AP Rocky x PUMA Suede '94 in faded navy releases today at $120"),
    ],
}


def related_nav(slug, e):
    items = RELATED.get(slug) or []
    if not items:
        return ""
    lis = "".join(f'<li><a href="{e(h)}">{e(n)}</a></li>' for h, n in items)
    return (
        '<nav class="related-links" aria-label="Related reading">'
        "<h2>Related reading</h2>"
        f"<ul>{lis}</ul>"
        "</nav>"
    )
