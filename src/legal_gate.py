"""RestockRally pre-publish legal hold gate (JI Ventures rule, Joshua, 27 Oct 2026; text in /workspace/content-review/RULE.md).
Two layers, both used by build.py and the git hooks (src/hooks/pre-commit, src/hooks/pre-push):
  1. check_article(a): runs on every article dict BEFORE it is rendered. A flagged article is NOT built; it is saved as
     /workspace/content-review/drafts/restockrally/<slug>.HOLD_REVIEW.json and one line per rule goes to queue.jsonl.
  2. main([paths]): full-site backstop over every built page in docs/ plus feed.xml and llms.txt. Exit 1 if anything is held.
A held item passes ONLY with a Joshua entry in /workspace/content-review/approvals.jsonl for site=restockrally.com, that
draft_path and the exact sha256. Bots never write approvals and never self-approve.
Code enforced: 2 (emails, phones, street addresses), 3 (hotlinked or unrecorded images/media; src/content_rights.json),
4 (every article and shoe page needs an external source link; every article needs a sources list), 6 (election wording),
8 (src/legal_holds.json blocks paths/slugs under notice, embargo or complaint). Keyword tripwires for 1, 5, 7.
Judgement only: whether an allegation is defamatory (1), whether a claim is actually true and sources agree (4),
whether advice is personalised (5), whether a headline overstates the evidence (7).
Usage: python3 src/legal_gate.py [--no-queue] [paths...]"""
import re, os, sys, json, glob, hashlib, datetime
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC); DOCS = os.path.join(ROOT, "docs")
CR = os.environ.get("CONTENT_REVIEW_DIR", "/workspace/content-review")
QUEUE, APPROVALS = os.path.join(CR, "queue.jsonl"), os.path.join(CR, "approvals.jsonl")
DRAFTS = os.path.join(CR, "drafts", "restockrally")
SITE, BOT = "restockrally.com", "Sneaker News Bot"
LEGAL = {p + "/index.html" for p in ("terms", "privacy", "disclaimer", "copyright", "affiliate-disclosure", "corrections", "sources-ethics", "contact", "contact/thanks", "about")}
R1 = re.compile(r"(?i)\b(fraud\w*|corrupt\w*|convicted|indicted|arrested|charged with|lawsuit|sued|scammers?|scammed|embezzl\w*|misconduct|dishonest\w*|cover[ -]?up|abused? by|accused of|allegedly|counterfeit(er|ers|ing)? by|ripp(ed|ing) off|steal\w* from)\b")
R5 = re.compile(r"(?i)\b(guaranteed (returns?|profit)|you should (buy|invest|sell)|investment advice|resell(ing)? for a guaranteed|sure(-| )fire profit|tax advice|legal advice for your|dosage|take \d+ ?mg)\b")
R6 = re.compile(r"(?i)\b(election|ballot|polling (place|station|location)|voter registration|register to vote|voting (day|date|deadline)|certified results?|absentee)\b")
R7 = re.compile(r"(?i)\b(official (partner|retailer of|site of)|endorsed by|in partnership with|sponsored by nike|authori[sz]ed (dealer|retailer) of|shocking|confirmed leak|100% (legit|confirmed))\b")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[a-z][\w.]*", re.I)
PHONE = re.compile(r"(?<![\d.])(\+?\d{1,2}[ .-])?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}(?!\d)")
STREET = re.compile(r"(?i)\b\d{2,5} [A-Z][a-z]+ (Rd|Road|St|Street|Ave|Avenue|Dr|Drive|Lane|Ln|Blvd|Court|Ct)\b")

def rights():
    p = os.path.join(SRC, "content_rights.json")
    return {k for k, v in json.load(open(p)).items() if v.get("licence") and v.get("evidence")} if os.path.exists(p) else set()
def holds():
    p = os.path.join(SRC, "legal_holds.json")
    return json.load(open(p)) if os.path.exists(p) else {}
def visible(s):
    return re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<script.*?</script>|<style.*?</style>|<head>.*?</head>", " ", s))
def ctx(t, m, w=60): return " ".join(t[max(0, m.start()-w): m.end()+w].split())

def text_flags(full, legal=False, contact_text=None):
    f = []
    if not legal:
        for m in R1.finditer(full): f.append((1, ctx(full, m), "HIGH: Joshua reviews. Do not soften wording to pass."))
        for m in R5.finditer(full): f.append((5, ctx(full, m), "Remove personalised advice or promised returns, then ChatGPT review."))
        for m in R7.finditer(full): f.append((7, ctx(full, m), "Check headline strength or implied affiliation, then ChatGPT review."))
    for m in R6.finditer(full): f.append((6, ctx(full, m), "HIGH: needs current election authority confirmation; Joshua reviews."))
    t = contact_text if contact_text is not None else full
    for m in EMAIL.finditer(t): f.append((2, m.group(0), "HIGH: remove contact detail; use the contact form."))
    for m in PHONE.finditer(t): f.append((2, m.group(0), "HIGH: remove phone number."))
    if not legal:
        for m in STREET.finditer(t): f.append((2, m.group(0), "HIGH: remove street address."))
    return f

def media_flags(s, ok):
    f = []
    for u in re.findall(r'<(?:img|video|source|iframe|embed)[^>]+?(?:src|srcset|poster)="([^"]+)"', s, re.I):
        u = u.split(",")[0].strip().split(" ")[0]
        if u not in ok:
            f.append((3, u, "No documented permission in src/content_rights.json; drop the asset or record the licence."))
    return f

def check_article(a, ok=None, hl=None):
    ok = rights() if ok is None else ok; hl = holds() if hl is None else hl
    full = " ".join([a.get("title", ""), a.get("description", ""), visible(a.get("body", ""))] + [s[0] for s in a.get("sources", [])])
    f = text_flags(full)
    f += media_flags(a.get("body", ""), ok)
    src = [s for s in a.get("sources", []) if str(s[1]).startswith("http") and "restockrally.com" not in s[1]]
    if not src: f.append((4, "no sources list with external URLs", "Add sources actually accessed, or hold."))
    if not re.search(r'href="https?://(?!restockrally\.com)', a.get("body", "")):
        f.append((4, "no in-text source link in body", "Link the source in the sentence."))
    key = "news/" + a.get("slug", "") + "/index.html"
    if key in hl or a.get("slug") in hl: f.append((8, "under legal hold: " + str(hl.get(key) or hl.get(a.get("slug"))), "HIGH: wait for Joshua; tell the Personal assistant."))
    return f

def approved(rel, sha):
    if not os.path.exists(APPROVALS): return False
    for line in open(APPROVALS):
        try: a = json.loads(line)
        except Exception: continue
        if a.get("site") == SITE and a.get("draft_path") == rel and a.get("sha256") == sha and str(a.get("approved_by", "")).lower().startswith("joshua"):
            return True
    return False

def queue(rel, sha, title, flags, srcs, draft, noq=False):
    seen = set()
    if os.path.exists(QUEUE):
        for line in open(QUEUE):
            try: q = json.loads(line); seen.add((q.get("site"), q.get("draft_path"), q.get("sha256"), q.get("rule")))
            except Exception: pass
    for rule in sorted({x[0] for x in flags}):
        fl = [x for x in flags if x[0] == rule]
        print("HOLD_REVIEW rule %d %s: %s" % (rule, rel, " | ".join(x[1] for x in fl[:3])))
        if noq or (SITE, rel, sha, rule) in seen: continue
        with open(QUEUE, "a") as q:
            q.write(json.dumps(dict(ts=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), site=SITE, bot=BOT, title=title,
                flagged=" | ".join(x[1] for x in fl[:5]), rule=rule, sources=srcs[:15], suggestion=fl[0][2], draft_path=draft, sha256=sha, status="HOLD_REVIEW")) + "\n")
        if rule == 8: print("RULE 8: tell the Personal assistant immediately, priority")

def gate_article(a, noq=False):
    """Returns True if the article may be built. Held articles are saved as drafts and queued."""
    flags = check_article(a)
    if not flags: return True
    blob = json.dumps(a, sort_keys=True, ensure_ascii=False); sha = hashlib.sha256(blob.encode()).hexdigest()
    rel = "articles/" + a["slug"]
    if approved(rel, sha): print("APPROVED (exact version)", rel); return True
    os.makedirs(DRAFTS, exist_ok=True)
    draft = os.path.join(DRAFTS, a["slug"] + ".HOLD_REVIEW.json")
    if not noq: open(draft, "w").write(json.dumps(dict(a, status="HOLD_REVIEW", sha256=sha), indent=1, ensure_ascii=False))
    queue(rel, sha, a.get("title", rel), flags, [s[1] for s in a.get("sources", [])], draft, noq)
    return False

def check_page(path, rel, ok, hl):
    s = open(path, encoding="utf-8").read()
    legal = rel in LEGAL
    if rel.endswith(".html"):
        hd = re.search(r"(?s)<head>.*?</head>", s); hd = hd.group(0) if hd else ""
        head = " ".join(re.findall(r"(?s)<title>(.*?)</title>", hd) + re.findall(r'name="description" content="(.*?)"', hd))
        body = visible(s); full = body + " " + head
    else:
        body = full = re.sub(r"<[^>]+>", " ", s)
    f = text_flags(full, legal, body)
    if rel.endswith(".html"): f += media_flags(s, ok)
    if re.match(r"(news|shoes)/[^/]+/index\.html$", rel):
        if not re.search(r'href="https?://(?!restockrally\.com)', s): f.append((4, "no external source link", "Add sources actually accessed, or hold."))
    if rel in hl: f.append((8, "under legal hold: " + str(hl[rel]), "HIGH: wait for Joshua; tell the Personal assistant."))
    return s, f

def main(argv):
    noq = "--no-queue" in argv; paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        paths = sorted(glob.glob(DOCS + "/**/*.html", recursive=True)) + [os.path.join(DOCS, x) for x in ("feed.xml", "llms.txt") if os.path.exists(os.path.join(DOCS, x))]
    ok, hl = rights(), holds(); held = 0
    for p in paths:
        p = os.path.abspath(p); rel = os.path.relpath(p, DOCS) if p.startswith(DOCS) else os.path.basename(p)
        s, f = check_page(p, rel, ok, hl)
        if not f: continue
        sha = hashlib.sha256(s.encode()).hexdigest()
        if approved(rel, sha): print("APPROVED (exact version)", rel); continue
        held += 1
        t = re.search(r"<title>(.*?)</title>", s)
        queue(rel, sha, t.group(1) if t else rel, f, sorted(set(re.findall(r'href="(https?://[^"]+)"', s)) - set()), rel, noq)
    print("legal_gate: %d file(s) checked, %d held" % (len(paths), held))
    return 1 if held else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
