# Swarm hub v2

Culled duplicate of the live hub after Phase A.

## Shared components (single source for root + v2)

| Need | Path |
|------|------|
| Theme CSS | `../assets/hub-theme.css` |
| Ratings / reviews JSON | `../data/` (written by root `scripts/build_review_data.py` / `refresh_and_push.py`) |
| Governance master, R-054, in-force | `../governance/...` |
| Observatory | `../observatory.html` |
| Workspace map | `../workspace-map.html` |
| Role map | `../governance/cartography/role-map-interactive.html` |
| Auto-update scripts | `../scripts/` |

Do not reintroduce dated master editions, review snapshot HTML, or annex history into this tree without an explicit decision. Improvement ideas: see `PROPOSALS.md`.
