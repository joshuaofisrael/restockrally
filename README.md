# RestockRally

Static sneaker release, restock and raffle news site for restockrally.com.

Build: `python3 src/build.py` writes to docs/ (served by GitHub Pages from main /docs).
Edit data in src/data.py and articles in src/articles.py. Every fact needs a source.

An article with a `publish` time (ISO 8601, with a timezone) is left out of the build until that instant. Times for the 29 Oct 2026 slots are London time, which is UTC+0 that day. `.github/workflows/publish-scheduled.yml` rebuilds on the hour from 11:00 to 19:00 UTC that day and commits `docs/` when a slot is due. `BUILD_ASOF=2026-10-29T11:00:00+00:00 python3 src/build.py` previews a later clock.

## Legal hold gate (JI Ventures rule, 27 Oct 2026)
`src/legal_gate.py` runs inside `build.py` twice: flagged articles are never rendered (saved as HOLD_REVIEW drafts in
/workspace/content-review/drafts/restockrally and queued in queue.jsonl), and a full-site backstop restores docs/ and exits 3
if any built page is held. Install hooks with `cp src/hooks/* .git/hooks/` (pre-commit and pre-push run the gate; Pages
deploys on push). Image or media rights go in `src/content_rights.json`; legal notices or complaints in `src/legal_holds.json`.
Held items publish only with Joshua's approval of the exact sha256 in /workspace/content-review/approvals.jsonl. Never self-approve.
