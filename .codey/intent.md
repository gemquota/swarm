# I-hub-icons-theme-archive-v2: Theme docs, icon tabs, archive + v2 cull

## Goal
Phase A on the live hub: theme Master/R-054/In force/Annex to match the site; remove Observatory double nesting; mobile-fix Assistant (375px); replace text tabs with expanding icon tabs and multi-tier tooltips (hover/focus/long-press), accessible. Phase B: archive current site (tag + /archive/2026-11-03/), duplicate to /v2/, cull historical/outdated and merge duplicates in v2 only, write improvement proposals (especially Assistant) without implementing them.

## Acceptance Criteria
- AC-1: Master, R-054, In force and Annex documents use the hub colour/typography theme (light+dark), not bare default browser styling.
- AC-2: Observatory is no longer double-nested (hub tab + full observatory chrome/nav); embed or nest so there is a single navigation tier for observatory views while standalone observatory.html still works and validate_observatory still finds href="observatory.html".
- AC-3: Assistant tab is usable at 375px width (no horizontal overflow from the assistant layout; stacked cards; controls fit).
- AC-4: Top and nested tabs are icon tabs that expand to show the name when selected; each has a multi-level tooltip (purpose + sub-tabs) on hover, keyboard focus, and long-press; aria-labels and existing keyboard tab behaviour remain.
- AC-5: After Phase A, archive tag archive/swarm-site-2026-11-03 exists and /archive/2026-11-03/ is a frozen copy served by Pages; root site remains the live Phase A hub. No new repo; no visibility/settings changes.
- AC-6: /v2/ is a duplicate then culled: historical/outdated records removed inside v2 only; duplicates merged or generalised; archive and root outside v2 untouched; auto-update scripts still feed v2 (shared data/ or documented path).
- AC-7: v2/PROPOSALS.md (or docs path under v2) lists improvement proposals especially for Assistant, not implemented.
- AC-8: Branch PR as gemquota; gitleaks clean; fresh-context verifier marks each AC; merge only on full PASS; every write logged in /workspace/governance/github-log.md bot=Engineer account=gemquota; live URLs HTTP 200.

## Scope
- /workspace/swarm-site (gemquota/swarm)
- github-log appends

## Out of Scope
- New repository; force-push; visibility/settings; deleting outside v2 (except Phase A edits to live root); implementing v2 proposals; secrets.

## Proposed (unconfirmed)
- P-1: Shared assets/hub-theme.css for document pages; observatory ?embed=1 hides hero/nav with hub nest subtabs driving the view.
- P-2: Archive via git tag + rsync-style copy into archive/2026-11-03/; v2 via copy then cull.
