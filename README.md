# RestockRally

Static sneaker release, restock and raffle news site for restockrally.com.

Build: `python3 src/build.py` writes to docs/ (served by GitHub Pages from main /docs).
Edit data in src/data.py and articles in src/articles.py. Every fact needs a source.

## Legal hold gate (JI Ventures rule, 27 Oct 2026)
`src/legal_gate.py` runs inside `build.py` twice: flagged articles are never rendered (saved as HOLD_REVIEW drafts in
/workspace/content-review/drafts/restockrally and queued in queue.jsonl), and a full-site backstop restores docs/ and exits 3
if any built page is held. Install hooks with `cp src/hooks/* .git/hooks/` (pre-commit and pre-push run the gate; Pages
deploys on push). Image or media rights go in `src/content_rights.json`; legal notices or complaints in `src/legal_holds.json`.
Held items publish only with Joshua's approval of the exact sha256 in /workspace/content-review/approvals.jsonl. Never self-approve.
