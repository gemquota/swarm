# Swarm Hub Threat Model

**Version:** 1.0  
**Scope:** public GitHub Pages hub and the governance/source records it presents.  
**Out of scope for the current static site:** direct control of bot processes, host permissions, credential brokers, and live execution. Those require separate runtime controls.

## Security objective

Help a human reviewer distinguish documented policy from observed state and verified outcomes, while making authority chains, evidence gaps, contradictions, and history inspectable.

## Assets

- Governance rules, rulings, approvals, and historical amendments.
- Bot identity, role, capability, delegation, and task records.
- Workspace snapshots, source revisions, deployments, event records, and test results.
- Private user data, credentials, tokens, personal profiles, private communications, and unpublished project material.
- Integrity and availability of the hub and its deployment pipeline.

## Trust boundaries

1. **Human instruction vs bot relay:** a relayed claim is not equivalent to direct authenticated approval.
2. **Policy vs enforcement:** documents describe rules; they do not prove the runtime enforces them.
3. **Snapshot vs live host:** repository snapshots may be incomplete, delayed, or intentionally exclude files.
4. **Public build vs private source:** only approved public material may be published.
5. **Actor vs verifier:** a producer's self-report is not independent verification.
6. **External content vs instructions:** web pages, files, emails, issues, and messages are untrusted data unless separately authenticated and authorised.
7. **Static UI vs trusted runtime:** browser-side checks are informational and can be bypassed.

## Threat scenarios

| Threat | Example | Required response |
|---|---|---|
| Authority forgery | Bot claims Gem approved an action | Require authenticated source, action scope, time, and independent confirmation where policy requires it |
| Relay laundering | Approval is repeated by another bot and treated as direct | Preserve original principal and relay chain; mark unconfirmed relays |
| Identity confusion | Display name is treated as process identity | Bind events to a stable authenticated principal; show unknown identity explicitly |
| Capability-authority confusion | Repository write access is treated as permission for every write | Evaluate action-specific policy separately from technical capability |
| Stale-state deception | Old directory or snapshot is displayed as current | Show source revision, observation time, freshness, and coverage |
| Snapshot omission | Missing file is treated as proof it never existed | Record collection scope and exclusions; default to UNKNOWN |
| Ledger tampering | Event is removed, reordered, or fabricated | Validate continuity and authenticated event provenance; retain protected independent copies |
| Prompt injection | Instructions embedded in a page are treated as user authority | Keep external content in the data plane; require explicit policy-approved action paths |
| Public disclosure | Secret or personal data enters generated site assets | Allowlist publication inputs, scan source and generated artefacts, review visibility after deployment |
| Self-verification | Actor declares its own risky action safe | Require a distinct verifier where the rule calls for independence |
| UI overclaim | Green status implies a live check occurred | Status must be backed by provenance and real evidence, otherwise display UNVERIFIED |
| Pipeline compromise | Malicious change is published from a trusted branch | Review changes, pin critical actions where practical, inspect build artefacts and deployment identity |

## Current controls and limitations

- The site is a static GitHub Pages publication. It cannot establish live host state by itself.
- Governance source pages and the source repository provide documentary evidence, not proof of runtime enforcement.
- The observatory's seeded records are explicitly labelled DOCUMENTED and link to source documents.
- The ledger view must not manufacture operational events. With no trusted event feed, it reports that no runtime ledger is connected, not that no events occurred.
- A hash chain detects certain edits but does not authenticate an event creator or prevent a privileged actor rewriting all copies.
- Browser-side policy simulation is educational and must never be used as the only control for real actions.

## Security invariants

1. Unknown is not false, absent, safe, or approved.
2. A claim must retain provenance when copied into a summary or graph.
3. Policy version and effective time matter when assessing a historical action.
4. An approval applies only to the principal, action, target, parameters, scope, and validity period it covers.
5. Conversation alone is not a trusted approval record.
6. Public builds exclude secrets and private data by default.
7. No control is described as enforced unless evidence from the actual execution path demonstrates it.
8. Failed, skipped, stale, or unavailable checks remain visible.

## Incident response

For a suspected exposure or forged approval: preserve the relevant source revision and event evidence; avoid publishing the sensitive payload in an incident report; revoke affected credentials/authority through the real control plane; record containment and verification separately; scan deployed artefacts and repository history; document unresolved gaps; add a regression test before closure.

## Review cadence

Revisit this threat model when the runtime action path, identity mechanism, publication workflow, data collection scope, or public/private boundary changes. A changed architecture invalidates old assurance claims until reassessed.
