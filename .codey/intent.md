# I-proposals-21-diagrams: Build all 21 proposals + interactive architecture diagrams

## Goal
Implement every item in v2/PROPOSALS.md on v2 and shared root components; MOVE dated review pages from live root into a new archive folder (not /archive/2026-11-03/) with redirects; never modify the 2026-11-03 freeze. Add interactive architecture diagrams (orchestrator/worker/checker, bots/roles, governance flow, data/automation pipelines): clickable, expandable nodes, tooltips, mobile, themed, data-driven where possible. Assistant stays proposal-only (no API, no credentials).

## Acceptance Criteria
- AC-1: Proposals 1–8 Assistant UX built on root and v2; still proposal-only (no LLM API, no credentials).
- AC-2: Proposals 9–12 hub chrome (icon density/always-labels setting, tooltip coach+?, observatory height, document title hashes) on root and v2.
- AC-3: Proposals 13–15 document shell / Summary source locators / as-of stamps on shared docs and hub.
- AC-4: Proposal 16 — dated review HTML moved from live root governance/reviews/ into archive/reviews/ (or similar, NOT archive/2026-11-03/); redirects left at old paths; freeze tree unmodified.
- AC-5: Proposals 17–19 dual-hub smoke check, charts empty-state, archive MANIFEST.sha256 for 2026-11-03 freeze (manifest file may live beside freeze or under archive/ without rewriting freeze contents — prefer archive/2026-11-03-MANIFEST.sha256 outside the freeze dir if freeze must stay byte-identical; if Gem allowed manifest inside freeze via "Add MANIFEST" proposal, adding one new file under freeze is the proposal intent — use archive/MANIFEST-2026-11-03.sha256 OUTSIDE the freeze to honour "Never modify /archive/2026-11-03/").
- AC-6: Proposals 20–21 workspace summary + lazy nest iframes on root and v2.
- AC-7: Interactive architecture diagrams for hierarchy, bots/roles, governance flow, data/automation — clickable, expandable, tooltips, mobile, themed, generated from data where possible; on Overview (root+v2).
- AC-8: Branch PR as gemquota; gitleaks clean; do not edit scripts/refresh_and_push.sh; fresh independent verifier PASS; merge only on full PASS; github-log every write; no force-push; live Pages URLs HTTP 200.

## Out of Scope
- Editing scripts/refresh_and_push.sh
- Modifying files inside archive/2026-11-03/
- Assistant LLM API or credentials
- Force-push; new repos; visibility changes

## Proposed (unconfirmed → accepted by Gem pt129u)
- P-all-21: Build all 21 proposals
- P-diagrams: Interactive architecture diagrams as specified
