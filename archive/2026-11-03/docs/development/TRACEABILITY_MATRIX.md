# Adversarial Findings Traceability Matrix

This matrix connects the initial review findings to the first implementation increment. A row marked **documented** is not a claim that runtime enforcement exists.

| ID | Finding / risk | Phase | Initial response in this PR | Remaining work / verification |
|---|---|---:|---|---|
| F01 | Policy is confused with enforcement | 0–1 | Threat model and explicit DOCUMENTED/UNKNOWN labels | Runtime telemetry and execution-path evidence in later PR |
| F02 | No clear temporal/current-truth model | 1 | Provenance contract separates event, observation, effective, and publication time | Add live freshness measurements when a trusted collector exists |
| F03 | Workspace map is catalogue-like | 4 | Typed graph model and relationships view foundation | Historical revisions and diffs in Phase 5 |
| F04 | Identity, role, capability, and authority are conflated | 2 | Separate schema concepts and policy lookup | Bind to authenticated runtime identities |
| F05 | Engineer GitHub write capability is broad | 2 | Source-linked documented policy lookup; no implied action approval | Runtime control/telemetry integration and tests |
| F06 | Emissary publication authority is high impact | 2 | Explicit publication policy requirements surfaced | Actual publication gate and post-publication read-back in Phase 9 |
| F07 | External content lacks provenance machinery | 0–1 | Provenance contract and untrusted-data boundary | Ingestion pipeline provenance in later PR |
| F08 | Ledger is underexposed | 3 | Ledger view with honest disconnected state and event schema | Connect authenticated append-only event source |
| F09 | Forum discussion can be confused with authority | 0, 2 | Trust-boundary rule documented | Forum classification and event linkage in Phase 6 |
| F10 | Hub is static despite dynamic-oversight framing | 0–1 | Static/live boundaries and source freshness made explicit | Runtime feed in a separate secured integration |
| F11 | Contradictions are not surfaced | 4 | Deterministic consistency checks over curated metadata; documented open questions shown separately | Expand to live sources and test corpus |
| F12 | Governance master can look like sole authority | 0–1 | Source locator and source links; no implicit precedence | Explicit supersession graph and source conflict resolver |
| F13 | gvmw snapshot is incomplete | 0–1 | Missing/excluded data semantics documented | Machine-readable snapshot coverage manifest |
| F14 | Semantic relationships are not first-class | 4 | Typed entity/edge model and relationship explorer | Ingest complete entity set and graph history |
| F15 | Evidence chain is hard to inspect | 1–3 | Source-linked records and schema contracts | Runtime action → evidence → verifier linkage |
| F16 | Trust gradient is missing | 1 | Nine-state epistemic vocabulary | Apply to all existing hub pages |
| F17 | No adversarial lab | 0 | Threat scenarios and acceptance criteria | Executable adversarial suite in Phase 7 |
| F18 | Polished UI can overstate confidence | 1 | Unknown and documented states visible in observatory | Usability review with realistic incomplete data |
| F19 | Public/private boundary is unclear | 0 | Threat model calls for allowlist and redaction | Build-time scanning/allowlist enforcement in Phase 9 |
| F20 | Historical governance and workspace drift invisible | 4 | Temporal contract and source revision model | Timeline and drift analytics in Phases 5 and 10 |

## Acceptance rule

Every finding must have a stable ID, implementation location, and a test or explicit dependency. A finding is not closed because a UI card was added. It closes only when its exit criterion is demonstrated and the evidence is linked.
