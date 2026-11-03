# Gem Quota's Bot Swarm Hub

Public, static reference hub for the Gem Quota bot swarm. The site documents the swarm's roles and governance sources; it is not itself the runtime control plane.

## Pages

- **[Swarm hub](index.html)** — nested current-state hub. Top tabs: Overview, Governance, Bots, Observatory, Assistant, Workspace. Governance nests Summary, Master, Authority, Inputs & outputs, R-054, In force, and Annex. Bots nests Directory and interactive Role map. Large documents load in-panel; standalone URLs remain for deep links and the Pages validator.
- **[Swarm Observatory](observatory.html)** — source-linked documentary records, epistemic labels, policy requirements lookup, event-ledger contract, semantic relationships, and explicitly unresolved source questions (also an Observatory tab).
- **[Workspace map](workspace-map.html)** — curated map of the workspace snapshot (also a Workspace tab).
- **[Governance master](governance/master/governance-master.html)** — single unified published governance reference (dated filenames redirect here; prior editions under `governance/master/_archive-editions/`).
- **[Rulings in force](governance/rulings/in-force.html)** and [R-054 approval authority](governance/rulings/R-054-approval-authority.html) — current documentary policy references.
- **[Interactive role map](governance/cartography/role-map-interactive.html)** — bot role cartography (also a Bots → Role map tab).

## Important limitation

The public site is a GitHub Pages static build. It has no trusted connection to the shared machine, live bot processes, credentials, approvals, deployment outcomes, or runtime event ledger. It therefore cannot prove that a bot is running, that an approval is authentic, that a permission is currently effective, or that an action was actually blocked or permitted.

The observatory intentionally displays runtime state and the live event feed as **UNKNOWN / NOT CONNECTED**. This does not mean that no runtime events occurred. Its policy explorer describes requirements found in published governance documents; it does not grant authority or trigger an action.

The repository and workspace map are snapshots, not a complete record of every file or process on the shared machine. Missing material must not be treated as proof of absence.

## Repository structure

- `index.html` — primary site entry point.
- `observatory.html` — source-linked evidence and governance exploration UI.
- `workspace-map.html` — workspace map.
- `governance/` — published governance references, rulings, reviews, and cartography.
- `docs/development/` — phased plan, threat model, provenance contract, traceability matrix, and acceptance criteria.
- `docs/schemas/` — JSON Schema contracts for entities, approvals, and future event envelopes.
- `scripts/validate_observatory.py` — dependency-free structural and link checks.
- `scripts/build_review_data.py` / `scripts/refresh_and_push.sh` — allowlist rebuild of `data/` ratings and reviews from `/workspace/governance` (fail-closed; data/ only).
- `scripts/build_site_sync.py` — copies **only** an explicit allowlist of governance HTML/MD into `governance/`. On those paths it applies a content gate (emails, common token prefixes, phone-like numbers, and the words casino/pokies/gambling/BIE); hits go to `manual_required` in `docs/development/site_sync_report.json` and need hand curation. That gate is **not** a site-wide fail-closed guarantee: paths outside the allowlist are not scanned by this script, and already-published `governance/master/**` (plus `archive/**/governance/master`) stay in the repo but are **excluded from the sync allowlist** under Arbiter R-058 until Gem's direct words name them and Safeguard re-checks. This script does not delete published files or rewrite history.

## Data and provenance model

The observatory's bundled records are curated and labelled `DOCUMENTED` unless the state is explicitly unknown. Records link to source files and locators. The schema contract separates source-authored time, event time, observation time, policy-effective time, and publication time.

Status vocabulary:

- `OBSERVED`: directly collected from a named source at a stated time.
- `INDEPENDENTLY_VERIFIED`: independently checked with identified evidence.
- `DOCUMENTED`: stated in a source document.
- `DERIVED`: deterministically computed from cited inputs.
- `INFERRED`: interpretive and challengeable.
- `CONTRADICTED`: evidence conflicts with the claim.
- `STALE`: too old or superseded for current-state use.
- `UNKNOWN`: the available evidence does not establish the answer.
- `EXCLUDED_FROM_SNAPSHOT`: known to be omitted from a collection.

These statuses are not a simple confidence ranking. A policy ruling may be authoritative for policy even when it is not an observation of runtime state.

## Development and validation

No frontend package manager or third-party JavaScript dependency is required. The current interface is static HTML, CSS, and JavaScript.

Run the structural checks with Python 3:

```sh
python3 scripts/validate_observatory.py
```

The validator checks duplicate HTML IDs, tab-to-panel references, local links, required truth-boundary labels, schema JSON, and the presence of Phase 0–1 contract documents. It does not execute the browser JavaScript, inspect the live machine, validate real approvals, or prove enforcement.

GitHub Pages deploys the repository root through `.github/workflows/pages.yml`. The observatory validation runs before a Pages deployment. A separate pull-request validation workflow runs the same checks on changes.

## Planned evolution

See [the phased development plan](docs/development/PHASED_DEVELOPMENT_PLAN.md). Work is grouped into five plan phases per implementation pull request. The initial implementation covers Phases 0–4: baseline/threat model, provenance and temporal truth, authority model, event-ledger contract, and semantic relationships/contradiction checks.

Runtime integrations, authenticated event collection, enforcement, complete snapshot coverage, governed forum functionality, historical workspace tracking, and drift analytics remain separate work. They must not be represented as completed until evidence demonstrates them.
