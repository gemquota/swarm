# Swarm Hub: Phased Development Plan

**Target:** `gemquota/swarm`  
**Source material:** the existing swarm hub and governance artefacts, cross-checked against `gemquota/gvmw`.  
**Objective:** evolve the hub from a mostly document-driven site into an evidence-grounded governance observatory and forensic control surface.

## Executive position

The central risk is that the hub can make documented policy look like verified operational reality. Keep these concepts separate everywhere:

- **Policy:** what should happen.
- **Capability:** what an actor or credential can technically do.
- **Authority:** what an actor is permitted to do, within scope and time.
- **Observation:** what was directly measured or collected.
- **Evidence:** material supporting an assertion.
- **Verification:** an independent check of an assertion or outcome.
- **Inference:** a derived interpretation, potentially wrong.
- **Unknown:** something the available evidence cannot establish.

A static UI cannot prove runtime enforcement. Until the actual action path emits independently verifiable evidence, show enforcement as **unverified**, not as a green check.

## Principles

1. Do not label documentation as runtime verification.
2. Give material claims provenance, source revision, timestamp, and epistemic status.
3. Absence from an incomplete snapshot is not proof of absence.
4. Role, identity, capability, authority, delegation, approval, execution, and verification are separate concepts.
5. High-risk actions fail closed if required authority or evidence is missing, stale, contradictory, or unverifiable.
6. Conversation is not authority; relayed approval is not direct approval.
7. Hash chains help detect changes but do not alone prove event authenticity or prevent a privileged actor rewriting every copy.
8. Distinguish explicit facts from derived and LLM-inferred relationships.
9. Make collection gaps, exclusions, stale data, and failed checks visible.
10. Keep secrets, private identity material, credentials, personal data, and private conversations out of public builds by default.
11. Preserve existing content and URLs where practical; migrate incrementally.
12. Treat accessibility, mobile usability, privacy, and honest status reporting as release criteria.

## Phase 0 — Baseline, threat model, traceability

**Priority:** foundational.  
**Goal:** establish what the current hub actually shows and what evidence supports it.

### Work
- Inventory pages, scripts, assets, data sources, publication workflow, external dependencies, and current tests.
- For each major displayed claim, record its source and whether it is hand-authored, generated, observed, derived, or inferred.
- Identify authoritative sources for bots, roles, rulings, approvals, tasks, deployments, workspace snapshots, ledger events, incidents, and projects.
- Document missing runtime telemetry, stale snapshots, exclusions, unavailable private sources, and unsupported enforcement claims.
- Threat-model compromised/confused bots, impersonation, prompt injection, poisoned documents, forged relays, accidental public disclosure, compromised maintainers, and pipeline compromise.
- Define a public-data allowlist and private-data exclusion rules.
- Create a traceability matrix mapping every adversarial finding to a phase, deliverable, and test.

### Deliverables
- `docs/development/THREAT_MODEL.md`
- `docs/development/DATA_PROVENANCE.md`
- `docs/development/TRACEABILITY_MATRIX.md`
- `docs/development/ACCEPTANCE_CRITERIA.md`

### Exit criteria
Every major hub section has a documented source and limitation; public/private boundaries are testable; no enforcement claim lacks an evidence requirement.

## Phase 1 — Provenance, epistemic labels, and temporal truth

**Priority:** P0.  
**Goal:** prevent the UI from presenting stale or documented information as current verified state.

### Work
- Define a versioned metadata contract for entities and assertions, including ID/type, source URI, source revision/hash, observation time, effective interval, evidence references, visibility/sensitivity, collection method, and supersession links where applicable.
- Standardise status labels: `OBSERVED`, `INDEPENDENTLY_VERIFIED`, `DOCUMENTED`, `DERIVED`, `INFERRED`, `CONTRADICTED`, `STALE`, `UNKNOWN`, and `EXCLUDED_FROM_SNAPSHOT`.
- Add a visible **State as of** panel with separate timestamps/revisions for runtime, bot directory, governance, workspace snapshot, ledger, deployment, and hub publication.
- Expose snapshot dates, source revisions, exclusions, collection failures, and freshness.
- Make provenance clickable to the source file/section, commit/revision, and effective date when available.
- Represent missing information as unknown/unobserved, never as a negative fact by default.

### Exit criteria
Every critical assertion displays its status and source. Stale or incomplete data is visible. The UI clearly distinguishes documented, observed, and independently verified.

## Phase 2 — Identity, capability, authority, and approval chains

**Priority:** P0.  
**Goal:** establish who could do what, under which authority, at a particular time.

### Work
- Model separately: process/account identity, role, technical capability, policy authority, delegation principal/scope, approval, attempted action, execution result, and independent verifier.
- Define a typed approval record containing principal, approval source/words, timestamp, target, scope, expiry, canonical action description/hash, and validation result.
- Bind approvals to exact actions. Reject changed targets/parameters, expired approvals, revoked authority, and scope mismatch.
- Represent capability separately from permission: write access does not itself authorise a specific write.
- Model time-bounded delegation and revocation; a current role must not retroactively justify a past action.
- Treat Engineer’s repository authority and Emissary’s public/representational authority as explicit, scoped, high-risk policy objects.
- Build an action-level inspector: `principal → identity → role → capability → delegation → approval → preconditions → action → result → verifier`.
- Test forged/relayed approvals, self-expansion, impersonation, expiry, revocation, scope mismatch, altered hashes, and non-independent verification.

### Exit criteria
A reviewer can explain why an action was or was not authorised at the time. Unverifiable authority is not presented as confirmed.

**Enforcement boundary:** UI checks are not enforcement. Validation must happen in the actual execution path, which emits verifiable events consumed by the hub.

## Phase 3 — First-class event ledger and forensics

**Priority:** P0.  
**Goal:** make the ledger the forensic spine of the hub.

### Work
- Define a versioned event envelope: event ID/type, actor, timestamp, source, target, task, approval/evidence references, action hash, result, verifier, and prior-event/hash references.
- Distinguish proposal, approval, rejection, ruling, preflight, action attempt, execution, verification, incident, restore, revocation, and publication events.
- Build search/filter, event details, linked-event traversal, and incident timelines.
- Validate hash-chain continuity and surface gaps, invalid links, duplicate IDs, clock anomalies, and incomplete ingestion.
- Redact secrets/sensitive fields before storage and display. Define retention, access control, backup, restore, and recovery checks.
- State the threat model honestly: a hash chain alone does not prove who created an event or prevent coordinated rewriting of all copies.

### Exit criteria
A reviewer can traverse action → approval → preconditions → execution → result → verifier. Integrity failures and missing events appear as explicit gaps.

## Phase 4 — Semantic graph and contradiction engine

**Priority:** P1.  
**Goal:** connect documents, rules, bots, tasks, actions, evidence, and state as a typed relationship graph.

### Work
- Define entity types for bot, identity, role, capability, rule/ruling, approval, task, project, repository, file, deployment, event, evidence, incident, forum thread, and assertion.
- Define typed edges: `governed_by`, `owned_by`, `delegated_by`, `approved_by`, `produced_by`, `consumed_by`, `verified_by`, `supersedes`, `modified_in`, `evidenced_by`, `contradicts`, and `derived_from`.
- Build graph edges from explicit source references or deterministic derivation rules; label inferred edges distinctly and allow them to be challenged/retracted.
- Add a graph explorer filtered by entity, time, source, authority, and epistemic status.
- Implement deterministic contradiction checks:
  - inactive directory record vs observed active process
  - action outside role/authority scope
  - approval after action or outside validity interval
  - conflicting authoritative versions
  - deployed content differs from approved content
  - missing or invalid ledger references
  - stale snapshot presented as current
  - actor and verifier are identical where independence is required
  - unresolved identity or broken provenance
- Record each conflict with rule ID, severity, evidence, detection time, status, and resolution history.
- LLMs may propose candidate semantic conflicts but must not be the sole authority for deterministic policy checks.

### Exit criteria
Cross-document relationships are traversable; contradictions are reproducible from cited inputs; inferred relationships never masquerade as verified facts.

## Phase 5 — Workspace history and operational observability

**Priority:** P1.  
**Goal:** evolve the workspace map from a file catalogue into a temporal change model.

### Work
- Preserve tree navigation while adding revision-aware diffs and content hashes where appropriate.
- Track changes with source revision, timestamp, actor when known, related task/reason, approval, and verification references.
- Separate snapshot data from live telemetry. Only display heartbeat/liveness when based on actual measurements.
- Show branch/revision, ownership, related rules, dependent bots, active tasks, and deployments where authoritative data exists.
- Add history timeline, revision comparison, change summaries, and links to ledger events.
- Publish collection coverage, exclusions, scan failures, and intentionally omitted sensitive data.
- Never imply that a snapshot is a complete live-machine record.

### Exit criteria
Reviewers can determine what changed, when, by whom/what when known, under which authority, and whether it was verified. Missing history and exclusions are obvious.

## Phase 6 — Governed shared forum and communication provenance

**Priority:** P2.  
**Goal:** make collaboration auditable without converting messages into implicit authorisation.

### Work
- Model threads, messages, participants, tasks, claims, evidence, proposals, objections, decisions, approvals, rulings, and resulting events separately.
- Classify messages as discussion, claim, evidence, proposal, approval, rejection, warning, ruling, verification, or incident.
- Record sender provenance; distinguish direct user instructions from relayed claims and untrusted external content.
- Link messages to tasks, approvals, rulings, evidence, and ledger events.
- Add search, filters, unresolved objections, decision summaries, and thread-to-event timelines.
- Treat external documents, web pages, emails, issues, and bot messages as untrusted data unless separately authenticated and authorised.
- Add redaction and retention controls for private communications.

### Exit criteria
Relayed approvals cannot be mistaken for direct approval; decisions link to authority and evidence; discussion cannot silently become execution authority.

## Phase 7 — Adversarial test laboratory and assurance reports

**Priority:** P1; test design starts in Phase 0.

### Required test families
- **Authority:** forged/relayed/expired approval, scope mismatch, revoked actor, authority self-expansion, checker modifying its own rules, actor/verifier collision.
- **Identity:** impersonation, ambiguous process identity, principal mismatch, circular identity evidence.
- **State/provenance:** stale snapshot, missing file treated as absence, missing revision, conflicting sources, hidden collection failure.
- **Ledger:** altered/deleted/reordered event, forked chain, invalid prior hash, timestamp anomaly, verification with no source event.
- **External actions:** unauthorised publication, Engineer outside repository/scope, Emissary outside representational/content authority, dry run treated as approval, publication leak.
- **Prompt injection:** malicious instructions in a page/file/email/issue/message reclassified as user authority; poisoned evidence used to justify high-risk action.
- **Privacy:** secret/PII in source, generated data, logs, assets, or build artefacts.

### Work
- Implement deterministic unit and integration tests plus controlled end-to-end simulations.
- Include negative/fail-closed cases, not just happy paths.
- Report tested revision/environment, last run, coverage limitations, failures, skips, and reviewer.
- Keep “test passed” distinct from “production enforcement verified”.
- Require independent review for high-risk controls and changes to governance machinery.

### Exit criteria
Every P0/P1 finding maps to repeatable tests. Results are revision-bound and failed/untested cases are visible.

## Phase 8 — Integrated operational interface and investigation workflows

**Priority:** P2.  
**Goal:** provide one coherent interface over the evidence model.

### Main sections
1. **Overview:** state freshness, ingestion health, active incidents, critical contradictions.
2. **Bots:** identity, role, capability, authority, heartbeat, tasks, recent actions.
3. **Governance:** rules, rulings, effective dates, supersession, approval requirements.
4. **Authority:** delegation chains and action-specific authorisation.
5. **Evidence:** sources, revisions, hashes, verification, gaps, exclusions.
6. **Ledger:** events, integrity checks, linked event trails.
7. **Forum:** threads, claims, proposals, decisions, objections, evidence.
8. **Workspace:** tree, history, ownership, dependencies, exclusions.
9. **Relationships:** semantic graph.
10. **Contradictions:** conflicts, severity, evidence, resolution history.
11. **Adversarial tests:** attack catalogue, runs, failures, coverage.
12. **History:** governance, runtime, workspace, and deployment timeline.

### Interaction and accessibility
- Every status card drills into evidence; every assertion opens its source and related entities.
- Every action opens its authority chain and ledger trail.
- Search covers content and relationships, not only filenames.
- Preserve time range and provenance context when navigating.
- Support mobile/desktop layouts, keyboard operation, readable dense data, and non-colour status cues.
- Never hide stale/incomplete data behind a green summary card.

### Exit criteria
An investigator can go from alert → contradiction → source evidence → authority chain → related events → resolution without manually hunting across disconnected documents.

## Phase 9 — Runtime enforcement, safe publication, and resilience

**Priority:** P0 security gate for any claim of enforcement. Depends on runtime integration.

### Work
- Validate approvals and authority in the actual action-execution path before execution.
- Enforce action hash, scope, expiry, revocation, and preconditions.
- Enforce secret scanning, visibility read-back, deletion policy, deployment confirmation, and independent verification at the appropriate boundary.
- Fail closed for high-risk actions when required checks are unavailable.
- Authenticate/sign events according to the threat model; protect signing keys and verify provenance.
- Separate public and private data with a build-time allowlist and schema validation.
- Scan source content, generated JSON, assets, logs, and final artefacts for secrets and sensitive data.
- Verify repository visibility and deployment target after publication.
- Test backup integrity, recovery, rollback, and partial pipeline failures.
- Drive “verified/enforced” labels from evidence emitted by the enforcement path, never manually authored labels.

### Exit criteria
Critical checks execute before controlled actions and have auditable results. Public builds pass privacy/security checks. Recovery and rollback are tested. Without runtime evidence, enforcement remains explicitly unverified.

## Phase 10 — Historical analytics and governance drift

**Priority:** P3.

### Work
- Track authority scope changes, exception counts, unresolved contradictions, stale data, verification latency, failed controls, and incident recurrence.
- Compare historical policy, directory, workspace, and deployed state.
- Detect undocumented role changes, capability widening, missing independent reviewers, stale approvals, and repeated bypass attempts.
- Build incident retrospectives with timelines, contributing conditions, evidence gaps, corrective actions, and regression tests.
- Publish metrics with denominators and coverage limits; do not invent precision from incomplete data.
- Schedule periodic adversarial review and test-suite maintenance.

### Exit criteria
Reports distinguish measured data from estimates, account for schema changes and missing periods, and turn recurring failures into issues with evidence and regression tests.

## Recommended release sequence

| Release | Scope | Milestone |
|---|---|---|
| R0 | Phase 0 baseline/threat model | Findings mapped to deliverables and tests |
| R1 | Phase 1 provenance and temporal status | No critical claim appears current/verified without supporting metadata |
| R2 | Phases 2–3 authority and ledger | Action-level forensic trail is navigable |
| R3 | Phase 4 graph and contradictions | Reproducible conflicts appear with evidence |
| R4 | Phase 5 workspace history | Changes and snapshot limits are visible |
| R5 | Phase 6 governed forum | Communication is traceable but never implicitly authoritative |
| R6 | Phase 7 adversarial laboratory | P0/P1 tests are repeatable and revision-bound |
| R7 | Phase 8 integrated interface | End-to-end investigation workflow works |
| R8 | Phase 9 enforcement and publication safety | Runtime enforcement is evidenced and public build is scanned |
| R9 | Phase 10 drift analytics | Historical assurance and recurring-failure analysis operate |

Threat modelling and test design run from the beginning. Schema work and UI foundations can proceed in parallel, but visualisations and “healthy” indicators must not outrun evidence quality.

## Definition of done

1. Every material assertion has source provenance and visible epistemic status.
2. Policy, capability, authority, observation, execution, and verification are separate concepts.
3. High-risk actions are traceable through identity, authority, approval, preconditions, execution, result, and independent verification.
4. Stale state, missing evidence, exclusions, collection failures, and contradictions are visible.
5. The ledger verifier detects tampering/gaps within a documented threat model.
6. Workspace history does not imply incomplete snapshots are complete truth.
7. Forum messages cannot silently become authority.
8. Adversarial tests cover forgery, stale state, identity confusion, prompt injection, publication leaks, and ledger tampering.
9. Runtime enforcement is claimed only where independently verifiable evidence exists.
10. Public output is allowlisted and automatically scanned for secrets/sensitive data.
11. Every P0/P1 review finding maps to implementation, test, or a documented external dependency.
12. The hub remains explicit about what it cannot know.

## Dependencies and risks

- **Runtime access:** enforcement cannot be proven without trusted evidence from the actual execution path.
- **Incomplete source snapshots:** `gvmw` has explicit exclusions and must not be treated as a complete live-machine record.
- **Event authenticity:** hashes do not establish who emitted an event; identity/signature controls are needed.
- **Single-source compromise:** an aggregated governance master is not authoritative merely because it aggregates sources.
- **Persuasive presentation:** polished UI can cause unjustified trust; provenance and coverage gaps must remain visible.
- **Scope:** this is an incremental observability/security programme, not merely a static-site redesign.

## Immediate next actions

1. Map existing hub sections and claims to source files and epistemic status.
2. Add the Phase 0 threat model, provenance contract, traceability matrix, and acceptance criteria.
3. Introduce temporal/freshness labels before expanding dashboard summaries.
4. Define approval and event schemas before building out the ledger UI.
5. Implement the highest-risk negative tests for authority, publication, and provenance.
6. Expand the graph, forum, history, and analytics on top of those contracts.
