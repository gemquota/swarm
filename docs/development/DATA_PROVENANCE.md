# Data Provenance and Epistemic Status Contract

**Schema version:** 1.0.0  
**Applies to:** observatory entities, assertions, evidence, authority records, and events.

## Core rule

Every material statement must distinguish its source from the confidence or status assigned to it. A well-formatted claim is not evidence. The hub must never silently upgrade a documented statement to an observed or verified fact.

## Required provenance fields

| Field | Meaning |
|---|---|
| `id` | Stable identifier within the data set |
| `type` | Typed entity or assertion category |
| `label` | Human-readable name |
| `status` | One status from the vocabulary below |
| `source.uri` | Relative path or URL to the supporting source |
| `source.revision` | Commit, immutable version, or source revision when known |
| `source.locator` | Heading, ruling ID, row, or other locator |
| `observedAt` | Time of collection/observation, not the time the underlying event supposedly occurred |
| `effectiveFrom`, `effectiveTo` | Policy or fact validity interval, if known |
| `collectedBy` | Collector identity or method; use UNKNOWN when not available |
| `evidenceIds` | References to supporting evidence records |
| `visibility` | PUBLIC, PRIVATE, or RESTRICTED |
| `limitations` | Known gaps, scope limits, or caveats |

Optional fields must be omitted or explicitly UNKNOWN. Do not fabricate timestamps, actors, commit SHAs, or effective dates.

## Status vocabulary

- **OBSERVED:** directly collected from a named source at a stated time. Observation alone does not prove truth.
- **INDEPENDENTLY_VERIFIED:** checked by a distinct verifier using an identified method and evidence.
- **DOCUMENTED:** stated in a source document. This is the default for the current static governance catalogue.
- **DERIVED:** deterministically computed from cited inputs and a documented rule.
- **INFERRED:** interpretive relationship or claim; include rationale and uncertainty.
- **CONTRADICTED:** evidence conflicts with the claim or with another applicable source.
- **STALE:** exceeds a defined freshness window or has been superseded for current-state use.
- **UNKNOWN:** available evidence does not establish the answer.
- **EXCLUDED_FROM_SNAPSHOT:** intentionally or structurally omitted from a collection. This does not imply absence from the live system.

Statuses are not a numeric ranking. For example, OBSERVED is not automatically more authoritative than a signed governing ruling for a question about policy.

## Time model

Keep separate:
- source-authored time;
- event time, when an action happened;
- collection/observation time;
- policy effective interval;
- publication/deployment time;
- last successful verification time.

Never substitute one for another. If a source only gives approximate time, preserve that precision instead of inventing seconds.

## Supersession and conflict

- Preserve historical source records.
- A newer document does not automatically supersede an older one unless the governing rules or explicit source metadata establish that relationship.
- Record supersession as an explicit edge with source evidence and effective time.
- If two sources conflict and precedence cannot be resolved deterministically, mark the affected claim CONTRADICTED or UNKNOWN and open a review item.
- Resolved conflicts retain the original evidence and resolution trail.

## Snapshot and coverage semantics

Every snapshot should declare collection time, source revision, scope, exclusions, failed sources, and freshness policy. Missing items default to UNKNOWN. Use EXCLUDED_FROM_SNAPSHOT only when exclusion is documented. Never report "no events", "no secret", "not running", or "no approval" unless a sufficiently complete and trustworthy source supports that exact negative claim.

## Authority and event provenance

Approvals and events require a stable principal, source, time, action/target scope, and validation evidence. Relays preserve both the claimed origin and relay path. An event producer cannot independently verify its own event where policy requires an independent checker. Hash linkage is an integrity signal, not authentication by itself.

## Public output

Only publish allowlisted fields and public sources. Do not include secret values, tokens, private profiles, private chat contents, raw credentials, personal data, or unredacted incident payloads. A URL pointing to a public source is not permission to copy every related field into the public site.

## Static observatory behaviour

The current observatory:
- labels curated policy claims DOCUMENTED;
- displays source links and the source locator;
- reports runtime telemetry and ledger connectivity as UNKNOWN / NOT CONNECTED;
- does not synthesize action events or approvals;
- treats policy simulations as informational, not as real authorisation decisions.
