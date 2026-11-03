# v2 improvement proposals (not implemented)

Review of the culled v2 hub after Phase A UI work and the process-of-elimination pass. These are proposals only; none of the items below have been built in this change set.

## Especially: Assistant tab

1. **Responsive stepper, not a 12-column grid**  
   Replace the request / contract / paste / staged cards with a single-column mobile stepper (1 Describe → 2 Copy package → 3 Paste response → 4 Stage). Keep a two-column layout from `md` breakpoints up. Reduces scroll thrash at 375px and clarifies the happy path.

2. **Sticky action bar on small screens**  
   Pin “Copy LLM task package”, “Validate response”, and “Export staged JSON” in a bottom safe-area bar on viewports under 600px so primary actions stay reachable without hunting past tall textareas.

3. **Package size meter and scope previews**  
   Show approximate character/token size of the task package as scope changes. Offer “preview context” that expands the sliced page text before copy, so users know what the model will see and can shrink scope when near limits.

4. **Response intake helpers**  
   - One-tap “Paste from clipboard” when the Permissions-Policy allows it.  
   - Strip accidental Markdown fences before `JSON.parse`.  
   - Inline path highlights for the first validation error (field name + JSON pointer).  
   - Example valid `needs_input` / `no_change` / `ready` payloads behind a disclosure.

5. **Staged-change UX**  
   Render staged sets as expandable cards with per-change accept/reject, source links opened in a new tab, and a “copy review brief” that summarises only accepted rows for human review outside the browser. Keep storage browser-local; never imply repository writes.

6. **Accessibility pass specific to Assistant**  
   Associate every control with visible `<label>`s (already mostly true), announce validation outcomes via a polite live region with role clarity, ensure textarea focus rings meet contrast on both themes, and make the contract list a description list for screen readers.

7. **No silent authority**  
   Keep the hard rule that this tab never calls an LLM API and never holds credentials. If a future optional connector is added, gate it behind an explicit opt-in and a separate security review; default remains copy/paste.

8. **Contract discovery**  
   Surface a short “what this protocol rejects” cheat-sheet next to the paste box (unknown keys, fence wrappers, invented approvals) so first-time users fail less often.

## Hub chrome and navigation

9. **Icon tab density**  
   Audit icon metaphor clarity with a short preference test (Governance shield vs scales; Observatory eye vs radar). Consider a user setting “always show labels” for people who dislike icon-only chrome.

10. **Tooltip discovery on mobile**  
    Long-press tooltips are easy to miss. Add a first-visit coach mark (“Press and hold a tab for its guide”) and an optional “?” control that opens the same multi-tier content in a dialog.

11. **Observatory embed height**  
    Replace fixed `75vh` iframes with ResizeObserver-based height matching the embedded view, or promote Observatory views to in-page components so double scrollbars disappear.

12. **Hash deep links in the header**  
    Reflect nest selection in the document title (`Governance · R-054 · Swarm`) for bookmarks and shared links.

## Content and governance surface

13. **Single document shell**  
    Finish generalising `assets/hub-theme.css` into a tiny static generator (or build step) so Master, rulings, and any future HTML share one shell, one nav, and one print stylesheet.

14. **Summary vs Master drift**  
    Generate the Governance Summary tables from the same structured source as R-054 / in-force (or annotate Summary rows with source locators) so the digest cannot silently diverge.

15. **Explicit “as-of” stamps**  
    Every framed documentary page should show an as-of date and source revision in the hub chrome above the iframe, not only inside the document.

16. **Retire remaining dated review HTML from the live root eventually**  
    v2 already dropped Authority and I&O snapshots from navigation. When Gem agrees, move the root hub to the same current-only set and keep those reports only under `/archive/`.

## Data and automation

17. **Dual-hub smoke check**  
    Extend `validate_observatory.py` (or a sibling) to assert that `v2/index.html` resolves `../data/*.json`, `../observatory.html?embed=1`, and shared governance URLs, so a root move cannot break v2 silently.

18. **Charts empty-state**  
    When ratings/reviews JSON is missing or empty, show a calm empty card instead of a console error only — especially important for archive copies that may intentionally omit live data refreshes.

19. **Archive integrity**  
    Add a small `archive/2026-11-03/MANIFEST.sha256` generated at freeze time so future agents can prove the freeze was not silently edited.

## Workspace and performance

20. **Workspace map weight**  
    `workspace-map.html` is large. For v2, consider a summarised map page plus “open full map” rather than always framing the full document.

21. **Lazy nest iframes**  
    Only set `iframe.src` when a nest panel is first selected (keep `loading="lazy"` as today, and clear or park hidden frames on low-memory mobiles).

## Out of scope reminders

- Do not implement these proposals in the same change set that created v2.  
- Do not delete or rewrite `/archive/2026-11-03/`.  
- Do not weaken Assistant’s proposal-only boundary.
