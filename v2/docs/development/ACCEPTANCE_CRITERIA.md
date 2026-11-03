# Swarm Hub Implementation Acceptance Criteria

## General

- [ ] No user-facing label implies live observation or enforcement without evidence from the relevant runtime.
- [ ] Every material curated claim links to a source and has an explicit epistemic status.
- [ ] Unknown, stale, contradicted, and excluded are visually distinguishable without relying on colour alone.
- [ ] Source time, observation time, effective time, and publication time are not conflated.
- [ ] Missing items in an incomplete snapshot are not represented as absent.
- [ ] Public pages contain no credentials, secret values, private profiles, or private conversation content.
- [ ] Interactive controls work with keyboard and on mobile layouts.
- [ ] Search and filters operate on the data currently displayed and provide a useful empty state.
- [ ] No runtime action is triggered by an informational UI or simulation.

## Phase 0: baseline and threat model

- [ ] Threat boundaries, attack scenarios, assets, limitations, and incident response are documented.
- [ ] Findings F01–F20 map to a phase and verification requirement.
- [ ] Public/private publishing assumptions are explicit.

## Phase 1: provenance and temporal truth

- [ ] Every seeded claim is labelled DOCUMENTED and links to an authoritative source file.
- [ ] The UI says when data is a static curated catalogue.
- [ ] Runtime state and runtime ledger are shown as not connected, not empty or healthy.
- [ ] Missing timestamps/revisions are shown as unknown, not fabricated.

## Phase 2: authority model

- [ ] Identity, role, capability, policy authority, delegation, approval, execution, and verification are distinct schema concepts.
- [ ] The policy explorer reports required checks and source references without declaring a real action authorised.
- [ ] Relayed approval is not silently upgraded to direct approval.
- [ ] High-impact publication and GitHub push requirements link to R-054.

## Phase 3: ledger

- [ ] No synthetic operational events are presented as real events.
- [ ] Empty/disconnected state explains that no feed is connected and does not imply no events occurred.
- [ ] Event schema supports provenance, action/approval references, results, verifier, and hash linkage.
- [ ] Integrity caveats state that hashes alone do not authenticate event creators.

## Phase 4: graph and contradiction checks

- [ ] Entity and edge types are explicit and validated.
- [ ] Source-backed edges retain provenance.
- [ ] Deterministic checks produce reproducible results from declared inputs.
- [ ] Documented open questions are not mislabeled as runtime-detected contradictions.
- [ ] Inferred relationships are distinct from explicit documented relationships.

## Release gate

The first implementation PR can close only its static-site and schema criteria. Runtime enforcement, live state, a trusted event stream, complete snapshot coverage, and historical analytics remain OPEN until separate integrations supply verifiable evidence.
