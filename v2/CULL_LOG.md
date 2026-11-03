# v2 cull log

## Removed

- v2/governance/master/_archive-editions — historical master edition archives
- v2/governance/master/governance-master-2026-10-22.html — superseded dated master snapshot; unified master is current
- v2/governance/master/governance-master-latest-2026-10-22.html — superseded dated master snapshot; unified master is current
- v2/governance/reviews — dated historical review snapshots (authority 2026-10-15, I/O 2026-10-10); superseded by live summary + R-054
- v2/governance/rulings/annex.html — near-duplicate of annex-history.html; annex tab removed from v2 hub
- v2/governance/rulings/annex-history.html — historical annex HTML removed from v2 hub; source md retained only if needed — removing html shell
- v2/governance/rulings/annex-history.md — historical annex content removed from v2 (outdated/historical record)
- v2/data — use shared ../data/ so auto-update scripts keep feeding both hubs
- v2/scripts — auto-update scripts live at repo root and write shared data/; avoid duplicate script trees
- v2/observatory.html — single shared component at ../observatory.html used by root and v2
- v2/workspace-map.html — single shared component at ../workspace-map.html used by root and v2
- v2/governance/cartography/role-map-interactive.html — single shared component at ../governance/cartography/role-map-interactive.html used by root and v2
- v2/governance/master/governance-master.html — single shared component at ../governance/master/governance-master.html used by root and v2
- v2/governance/rulings/R-054-approval-authority.html — single shared component at ../governance/rulings/R-054-approval-authority.html used by root and v2
- v2/governance/rulings/R-054-approval-authority.md — single shared component at ../governance/rulings/R-054-approval-authority.md used by root and v2
- v2/governance/rulings/in-force.html — single shared component at ../governance/rulings/in-force.html used by root and v2
- v2/governance/rulings/in-force.md — single shared component at ../governance/rulings/in-force.md used by root and v2
- v2/assets/hub-theme.css — single shared component at ../assets/hub-theme.css used by root and v2
- v2/governance/rulings — empty after cull
- v2/governance/master — empty after cull
- v2/governance/cartography — empty after cull
- v2/governance — empty after cull
- v2/assets — empty after cull

## Shared / merged path rewrites

- index path src="governance/master/governance-master.html" → src="../governance/master/governance-master.html"
- index path src="governance/rulings/R-054-approval-authority.html" → src="../governance/rulings/R-054-approval-authority.html"
- index path src="governance/rulings/in-force.html" → src="../governance/rulings/in-force.html"
- index path src="governance/cartography/role-map-interactive.html" → src="../governance/cartography/role-map-interactive.html"
- index path src="observatory.html?embed=1 → src="../observatory.html?embed=1
- index path href="observatory.html" → href="../observatory.html"
- index path src="workspace-map.html" → src="../workspace-map.html"
- index path href="workspace-map.html" → href="../workspace-map.html"
- index path fetch('data/ → fetch('../data/

## Governance nest kept in v2

- Summary, Master, R-054, In force
- Dropped: Authority review, Inputs & outputs, Annex (historical)


## Follow-up (proposals build)
- Live-root dated reviews moved to `archive/reviews/` with redirects; root hub nav matches v2 current-only set.
