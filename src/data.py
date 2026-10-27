# Single source of truth. Every release row is copied from a cited source; keep "src" on each row.
SITE = {
  "name": "RestockRally",
  "url": "https://restockrally.com",
  "tagline": "Fast sneaker release dates, restocks and raffles",
  "contact_endpoint": "https://formsubmit.co/4497ee41a1200e746e967998473d21da",
  "ga_id": "G-XXXXXXXXXX",  # placeholder until the Personal assistant sends the real G- ID
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
