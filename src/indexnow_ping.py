"""Ping IndexNow (https://api.indexnow.org/indexnow) so search engines fetch changed
pages faster. Uses the key file build.py already writes to docs/<indexnow_key>.txt.

Usage:
  python3 src/indexnow_ping.py [--dry-run] [path ...]

With no paths given, only the sitemap URL is submitted. Paths may be either a
docs/-relative file path (e.g. "docs/news/foo/index.html") or a full URL; each
is converted to its canonical page URL. The sitemap URL is always included.
"""
import json, os, sys, urllib.request
from data import SITE

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)
DOCS = os.path.join(ROOT, "docs")
URL = SITE["url"]
KEY = SITE["indexnow_key"]
SITEMAP_URL = f"{URL}/sitemap.xml"
ENDPOINT = "https://api.indexnow.org/indexnow"

def to_url(path):
    """Map a docs/-relative file path (or an already-absolute URL) to a page URL."""
    path = path.strip()
    if not path:
        return None
    if path.startswith("http://") or path.startswith("https://"):
        return path
    rel = path[len("docs/"):] if path.startswith("docs/") else path
    rel = rel.lstrip("/")
    if rel.endswith("index.html"):
        rel = rel[: -len("index.html")]
    return f"{URL}/{rel}" if rel else f"{URL}/"

def build_url_list(paths):
    urls = []
    seen = set()
    for p in paths:
        u = to_url(p)
        if u and u not in seen:
            seen.add(u)
            urls.append(u)
    if SITEMAP_URL not in seen:
        urls.append(SITEMAP_URL)
    return urls

def ping(url_list, dry_run=False):
    body = json.dumps({
        "host": URL.split("://", 1)[1],
        "key": KEY,
        "keyLocation": f"{URL}/{KEY}.txt",
        "urlList": url_list,
    }).encode("utf-8")
    if dry_run:
        print("DRY RUN, would POST to", ENDPOINT)
        print(body.decode("utf-8"))
        return None
    req = urllib.request.Request(ENDPOINT, data=body, method="POST",
                                  headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status
    except urllib.error.HTTPError as err:
        return err.code

def main(argv):
    dry_run = "--dry-run" in argv
    paths = [a for a in argv if a != "--dry-run"]
    url_list = build_url_list(paths)
    status = ping(url_list, dry_run=dry_run)
    if dry_run:
        return 0
    print(f"IndexNow: submitted {len(url_list)} url(s), status {status}")
    for u in url_list:
        print(" ", u)
    return 0 if status in (200, 202) else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
