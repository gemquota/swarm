# v2 improvement proposals — implemented

Gem approved all 21 items (pt129u, 12:40am AEST, 4 Nov 2026) plus interactive architecture diagrams.
Built on root hub and v2; shared assets under `assets/` and `data/architecture.json`.
Assistant remains proposal-only (no LLM API, no credentials).
`/archive/2026-11-03/` was not modified. Dated reviews moved to `archive/reviews/` with redirects at old paths.
Archive integrity manifest: `archive/MANIFEST-2026-11-03.sha256` (outside the freeze tree).

## Especially: Assistant tab

1. **Responsive stepper** — done (`assistant-layout` + progress steps; two-column from 701px).
2. **Sticky action bar** — done (`.assistant-sticky` under 600px).
3. **Package size meter and scope previews** — done (`#package-meter`, context preview).
4. **Response intake helpers** — done (clipboard paste, fence strip, JSON pointer errors, example payloads).
5. **Staged-change UX** — done (expandable sets, accept/reject, source links, review brief).
6. **Accessibility pass** — done (labels, polite live region, focus rings, contract as `dl`).
7. **No silent authority** — kept (proposal-only boundary in UI + package `safety_boundary`).
8. **Contract discovery** — done (rejects cheat-sheet beside paste / contract card).

## Hub chrome and navigation

9. **Icon tab density** — done (`Always show tab labels` preference).
10. **Tooltip discovery on mobile** — done (first-visit coach + `? Tab guide` dialog).
11. **Observatory embed height** — done (ResizeObserver fit in `hub-enhancements.js`).
12. **Hash deep links in the header** — done (document title `Section · Nest · Swarm`).

## Content and governance surface

13. **Single document shell** — done (`assets/hub-theme.css` print + `scripts/apply_doc_shell.py`).
14. **Summary vs Master drift** — done (source locator note on Summary pointing at R-054 / in-force).
15. **Explicit as-of stamps** — done (`.frame-meta` above framed panels).
16. **Retire dated review HTML from live root** — done (moved to `archive/reviews/`; redirects retained; root nav current-only).

## Data and automation

17. **Dual-hub smoke check** — done (`scripts/validate_dual_hub.py`).
18. **Charts empty-state** — done (calm empty cards when data missing).
19. **Archive integrity** — done (`archive/MANIFEST-2026-11-03.sha256` outside freeze).

## Workspace and performance

20. **Workspace map weight** — done (v2 summary + full map nest).
21. **Lazy nest iframes** — done (`data-src` until panel selected; park on small screens).

## Interactive architecture diagrams

Four data-driven views on Overview (root + v2): hierarchy, bots & roles, governance flow, data & automation — clickable, expandable, tooltips, mobile, themed (`assets/arch-diagrams.*`, `data/architecture.json`).
