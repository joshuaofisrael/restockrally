# Single source of truth. Every release row is copied from a cited source; keep "src" on each row.
SITE = {
  "name": "RestockRally",
  "url": "https://restockrally.com",
  "tagline": "Fast sneaker release dates, restocks and raffles",
  "contact_endpoint": "https://formsubmit.co/4497ee41a1200e746e967998473d21da",
  "ga_id": "G-LE2DZJFW6R",  # placeholder until the Personal assistant sends the real G- ID
  "indexnow_key": "8b8cf29951bb9ec34c151a1f184a21a0",
  "year": 2026,
}
SI = ("SoleInsider October 2026 calendar", "https://soleinsider.com/calendar/october-2026")
HOH = ("House of Heat, This Week's Biggest Sneaker Releases: October 26 to 31", "https://houseofheat.co/sneaker-releases-october-26-31-2026")
NIKE_BRAND = "https://www.nike.com/launch"
RELEASES = [
 # name, brand, date, price, sku, where-to-buy list [(label,url)], source
 ("Menace x adidas Adistar Control 5 \"Heat Signature\"","adidas","2026-10-27",180,"LB0086",[("adidas","https://www.adidas.com/us")],SI),
 ("Nocturnal x Nike SB Air Force 1 Low","Nike","2026-10-27",120,"IV6099-003",[("Nike SNKRS","https://www.nike.com/launch")],SI),
 ("Nike Air Max Ecstasy Plus \"Triple Black\"","Nike","2026-10-28",180,"IV7022-002",[("Nike SNKRS","https://www.nike.com/launch")],SI),
 ("Nike First Sight Shadow \"Cream\" (Women's)","Nike","2026-10-28",145,"HQ2410-200",[("Nike SNKRS","https://www.nike.com/launch")],SI),
 ("Air Jordan 3 \"Fireside\" (Women's)","Jordan","2026-10-30",205,"CK9246-200",[("Nike SNKRS","https://www.nike.com/launch")],SI),
 ("Nike Book 2 \"Oogie Boogie\"","Nike","2026-10-30",155,"IO7942-001",[("Nike SNKRS","https://www.nike.com/launch")],SI),
 ("Nike Caitlin 1 \"Jinx\"","Nike","2026-10-30",150,"JA4290-001",[("Nike SNKRS","https://www.nike.com/launch")],SI),
 ("Nike KD 19 \"Slim Reaper\"","Nike","2026-10-30",165,"IO8112-600",[("Nike SNKRS","https://www.nike.com/launch")],SI),
 ("Nike Kobe 3 Low Protro \"Mamba Eterno\"","Nike","2026-10-30",190,"IO6260-800",[("Nike SNKRS","https://www.nike.com/launch")],SI),
 ("Nike LeBron 24 \"Storm Drain\"","Nike","2026-10-30",200,"IX5103-001",[("Nike SNKRS","https://www.nike.com/launch")],SI),
 ("Air Jordan 14 \"Forest Green\"","Jordan","2026-10-31",215,"487471-300",[("Nike SNKRS","https://www.nike.com/launch")],SI),
 ("Air Jordan 4 \"Light Army\"","Jordan","2026-10-31",220,"JA5911-320",[("Nike SNKRS","https://www.nike.com/launch")],SI),
 ("Air Jordan 6 \"White Infrared\"","Jordan","2026-11-07",215,"CT8529-105",[("Nike SNKRS product page","https://www.nike.com/launch/t/air-jordan-6-white-infrared-white-and-light-crimson")],("Nike SNKRS: Air Jordan 6 White Infrared","https://www.nike.com/launch/t/air-jordan-6-white-infrared-white-and-light-crimson")),
 ("Air Jordan 11 \"Green Screen\"","Jordan","2026-11-14",255,"IQ5700-900",[("Nike SNKRS product page","https://www.nike.com/launch/t/air-jordan-11-green-screen")],("Nike SNKRS: Air Jordan 11 Green Screen","https://www.nike.com/launch/t/air-jordan-11-green-screen")),
 ("Nike LeBron XXIV \"Stars\"","Nike","2026-11-17",180,"IO8204-400",[("Nike.com","https://www.nike.com/a/lebron-24-release")],("Nike: LeBron XXIV release date, price and colorways","https://www.nike.com/a/lebron-24-release")),
]
RESTOCKS = [
 ("Nike Air Bakin High SP \"Black/Varsity Red\"","2026-10-22","Foot Locker (online)",170,"IQ5365-600",("CartTactic","https://carttactic.com/nike-air-bakin-high-black-varsity-red-restock-foot-locker/")),
 ("Nike Mind 001 and Mind 002","2026-10-15","Nike App and Nike.com",95,"",("Sole Retriever","https://www.soleretriever.com/news/articles/nike-mind-restock-release-date-october-2026")),
 ("Nike Air Max Phenomena","2026-10-07","Nike",155,"",("NJ.com","https://www.nj.com/shopping-deals/2026/10/nike-has-finally-restocked-the-sold-out-air-max-phenomena-sneaker-loafer.html")),
]
SIN = ("SoleInsider November 2026 calendar", "https://soleinsider.com/calendar/november-2026")
SNK=[("Nike SNKRS","https://www.nike.com/launch")]
RELEASES += [
 ("Nike Kobe 3 Low Protro \"Black\"","Nike","2026-11-01",190,"IV7127-002",SNK,SIN),
 ("Pharrell x adidas Adistar \"Jellyfish\"","adidas","2026-11-01",300,"KH6727",[("adidas","https://www.adidas.com/us")],SIN),
 ("Nike Air Foamposite Pro \"Mummy Duck\"","Nike","2026-11-03",230,"IZ7806-001",SNK,SIN),
 ("Air Jordan 11 MCS Cleat \"Space Jam\"","Jordan","2026-11-05",225,"JA7792-400",SNK,SIN),
 ("Nike Air Foamposite Pro \"FSU\"","Nike","2026-11-05",250,"IX2095-600",SNK,SIN),
 ("Nike Air Foamposite Pro \"LSU\"","Nike","2026-11-05",250,"IX2091-700",SNK,SIN),
 ("Nike Air Foamposite Pro \"Ohio State\"","Nike","2026-11-05",250,"IX2094-100",SNK,SIN),
 ("Victor Wembanyama x Nike GT Cut 4 \"State of Liberty\"","Nike","2026-11-05",210,"IW0737-300",SNK,SIN),
 ("New Balance 990v7 Made in USA","New Balance","2026-11-06",200,"U990GR7",[("New Balance","https://www.newbalance.com")],SIN),
 ("Union x Nike Dunk Low \"Bamboo\"","Nike","2026-11-06",130,"IF7380-200",SNK,SIN),
 ("Air Jordan 11 \"Magic Ball\" (Women's)","Jordan","2026-11-11",235,"IZ1800-200",SNK,SIN),
 ("Air Jordan 11 \"Lapis\" (Women's)","Jordan","2026-11-11",235,"IZ1800-400",SNK,SIN),
 ("Nike Kobe 8 Protro \"Shanghai Fireworks\"","Nike","2026-11-11",200,"IO6259-800",SNK,SIN),
 ("Nike Air Bakin \"Varsity Royal\"","Nike","2026-11-12",170,"IQ5365-400",SNK,SIN),
 ("Nike Air Foamposite One \"Phantom\"","Nike","2026-11-13",240,"IZ1476-001",SNK,SIN),
 ("Nike KD 19 \"Aunt Pearl\"","Nike","2026-11-13",170,"IO8111-600",SNK,SIN),
 ("Nike Ja 4 \"Code Red\"","Nike","2026-11-19",130,"IM4135-603",SNK,SIN),
 ("adidas Anthony Edwards 3 \"Lucid Pink\"","adidas","2026-11-20",130,"KH8545",[("adidas","https://www.adidas.com/us")],SIN),
 ("Air Jordan 3 \"Not Nice\"","Jordan","2026-11-21",215,"IF4396-001",SNK,SIN),
 ("Air Jordan 3 \"Lola Bunny\" (GS)","Jordan","2026-11-21",155,"IZ1694-600",SNK,SIN),
 ("Air Jordan 4 OG \"Bred\"","Jordan","2026-11-27",230,"IX8180-001",SNK,SIN),
 ("Nike Air Foamposite Pro \"Dr. Doom\"","Nike","2026-11-27",240,"HF0794-003",SNK,SIN),
]
SNWR=("Sneaker News","https://sneakernews.com/2026/10/25/sneaker-releases-october-25-31-2026/")
RESTOCKS = [
 ("Nike Air Max Goadome \"Black Pony Hair\"","2026-10-29","Nike and select stores",None,"",SNWR),
 ("adidas Adizero Adios Pro Evo 3","2026-10-29","adidas and select stores",None,"",SNWR),
] + RESTOCKS
RELEASES += [
 ("Converse SHAI 001 Lace Up \"Flare\"","Converse","2026-10-29",120,"A23933C-832",[("Nike SNKRS","https://www.nike.com/launch/t/shai-001-lace-up-flare")],("Nike SNKRS: SHAI 001 Lace Up Flare","https://www.nike.com/launch/t/shai-001-lace-up-flare")),
 ("Wales Bonner Karintha BW Army \"Black Pony\"","adidas","2026-10-29",200,"KK2813",[("adidas","https://www.adidas.com/us/wales-bonner-karintha-bw-army-black-pony-shoes/KK2813.html")],("adidas: Wales Bonner Karintha BW Army Black Pony","https://www.adidas.com/us/wales-bonner-karintha-bw-army-black-pony-shoes/KK2813.html")),
]
# 30 Oct 2026 slot: rows checked on Nike SNKRS product pages or the SoleInsider November calendar on 30 Oct 2026.
def _snkrs(t,u): return ([("Nike SNKRS product page",u)],("Nike SNKRS: "+t,u))
RELEASES += [
 ("Kobe Dunk Low Protro \"Anthracite and Sundial\"","Nike","2026-10-30",130,"IQ3922-001",*_snkrs("Kobe Dunk Low Protro Anthracite and Sundial","https://www.nike.com/launch/t/kobe-dunk-low-protro-anthracite-and-sundial-na")),
 ("Nike Air Max 97 \"Coppin State University\"","Nike","2026-10-30",190,"IW6991-400",*_snkrs("Air Max 97 Coppin State University","https://www.nike.com/launch/t/air-max-97-coppin-state-university-global-blue-and-midwest-gold")),
 ("Nike Air Max 97 \"North Carolina A&T\"","Nike","2026-10-30",190,"IW6992-100",*_snkrs("Air Max 97 North Carolina A&T","https://www.nike.com/launch/t/air-max-97-north-carolina-a-t-sail-and-sport-royal")),
 ("Nike Air Max 97 \"Mississippi Valley State University\"","Nike","2026-10-30",190,"IW6993-300",*_snkrs("Air Max 97 Mississippi Valley State University","https://www.nike.com/launch/t/air-max-97-mississippi-valley-state-university-court-green-and-black")),
 ("Nike Air Max Foamdome \"Eggplant\"","Nike","2026-11-05",265,"IX7255-506",*_snkrs("Air Max Foamdome Eggplant","https://www.nike.com/launch/t/air-max-foamdome-eggplant")),
 ("One Block Down x Nike Air Max 95 Big Bubble Lux","Nike","2026-11-06",200,"IM0704-001",*_snkrs("Air Max 95 Big Bubble Lux One Block Down","https://www.nike.com/launch/t/air-max-95-big-bubble-lux")),
 ("Nike SB Dunk Low \"Champagne\"","Nike","2026-11-06",130,"IQ0431-300",SNK,SIN),
 ("Nike Book 2 \"Chromaflair\"","Nike","2026-11-07",145,"FZ7013-003",SNK,SIN),
]
# Upgrade sources to Nike's own product pages where we opened them on 30 Oct 2026.
_UP={"487471-300":"https://www.nike.com/launch/t/air-jordan-14-forest-green","IO6260-800":"https://www.nike.com/launch/t/kobe-3-low-protro-mamba-eterno","JA7792-400":"https://www.nike.com/launch/t/jordan-11-mcs-space-jam-black"}
RELEASES=[(r[:5]+_snkrs(r[0].replace('"',''),_UP[r[4]])) if r[4] in _UP else r for r in RELEASES]
CTU=("CartTactic","https://carttactic.com/nike-air-more-uptempo-96-black-white-restock-foot-locker/")
RESTOCKS = [("Nike Air More Uptempo '96 \"Black/White\"","2026-10-29","Foot Locker (online)",170,"",CTU)] + [
 (r[0],r[1],r[2],230,"IO4635-001",("Sneaker News","https://sneakernews.com/2026/10/19/nike-air-max-goadome-pony-hair-io4635-001/")) if r[0].startswith("Nike Air Max Goadome") else r for r in RESTOCKS]
# 31 Oct 2026 slot: rows checked on Nike SNKRS product pages on 31 Oct 2026.
RELEASES += [
 ("Nike Blazy \"Tie Dye\"","Nike","2026-11-04",105,"IV7023-700",*_snkrs("Blazy Tie Dye Dark Sulfur and Sail","https://www.nike.com/launch/t/blazy-tie-dye-dark-sulfur-and-sail")),
 ("Nike Air Max Dolce Leather \"Black and Natural\" (Women's)","Nike","2026-11-04",170,"IR8665-001",*_snkrs("Women's Air Max Dolce Leather Black and Natural","https://www.nike.com/launch/t/women-s-air-max-dolce-leather-black-and-natural")),
 ("Nike Air Force 1 Low Premium \"What the LA\"","Nike","2026-11-05",125,"CT1117-100",*_snkrs("Air Force 1 Low Premium What the LA","https://www.nike.com/launch/t/air-force-1-low-premium-what-the-la")),
 ("Nike Air Max 95 Big Bubble \"Cacao Wow and Black\"","Nike","2026-11-10",190,"IX6347-200",*_snkrs("Air Max 95 Big Bubble Cacao Wow and Black","https://www.nike.com/launch/t/air-max-95-big-bubble-cacao-wow-and-black")),
 ("Nike Mind 002 Flyknit \"Black and Anthracite\"","Nike","2026-11-10",145,"IR2176-002",*_snkrs("Nike Mind 002 Flyknit Black and Anthracite","https://www.nike.com/launch/t/nike-mind-002-flyknit-black-and-anthracite")),
 ("Nike Air Max 90 \"Medium Olive and Sequoia\"","Nike","2026-11-13",170,"IV4504-201",*_snkrs("Air Max 90 Medium Olive and Sequoia","https://www.nike.com/launch/t/air-max-90-medium-olive-and-sequoia")),
 ("Nike Air Max 90 SP \"Black\"","Nike","2026-11-13",170,"IV4504-001",*_snkrs("Air Max 90 SP Black","https://www.nike.com/launch/t/air-max-90-sp-black")),
]
_UP2={"IO6259-800":"https://www.nike.com/launch/t/kobe-8-protro-shanghai-fireworks-laser-orange-and-safety-orange","IZ1800-200":"https://www.nike.com/launch/t/womens-air-jordan-11-magic-ball","IQ5365-400":"https://www.nike.com/launch/t/air-bakin-high-sp-varsity-royal-and-black"}
RELEASES=[(r[:5]+_snkrs(r[0].replace('"',''),_UP2[r[4]])) if r[4] in _UP2 else r for r in RELEASES]
RESTOCKS = [("Air Jordan 41 \"Ruby\"","2026-10-30","Nike (online)",205,"HV6474-601",("CartTactic","https://carttactic.com/air-jordan-41-ruby-restock-nike/"))] + RESTOCKS
