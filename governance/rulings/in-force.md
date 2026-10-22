# Rulings in force (current reference)

As of 22 Oct 2026, about 10:15pm AEST (UTC+10). This file lists every ruling in force, in its current form only. `rulings.md` stays the full log, and `annex-history.md` holds superseded text, old names and amendment history.

## Short codes used here
- **R-nnn**: an Arbiter ruling number in `rulings.md`.
- **RR-nnn**: a row in Safeguard's risk register (`risk/register.md`).
- **INC-nnn**: an incident record.
- **P1 to P5**: rollout phases in `phases.md`. All five are live (P3 and P4 since 15 Oct 11:30pm, P5 since 16 Oct 11:47am).
- **BIE**: material from the bie_tools bonus-data project (gambling-related data).
- **Codex**: `/workspace/governance/codex/`, where each bot's approved versions are kept. **CHANGELOG** is each bot's deploy record there.
- **Dry run**: Safeguard predicting what an action will do. It informs and never approves.
- **Scan**: Safekeeper checking a push for secrets.
- **Relay**: Gem's words passed on by another bot rather than given directly.
- **Deterministic check**: a fixed, rule-based check (hash, API read-back), as opposed to a bot's interpretation.
- **Digest**: Explorer's combined digest inbox, `/workspace/governance/digest/inbox/`.
- **gvmw**: the repo gemquota/gvmw (public, by Gem's choice).
- **v002 rule 6**: rule 6 of connector limits version 2 (no gambling or BIE content outward).

## Standing rule
- **Precedence**: Gem's authority, then environment reality, then deterministic checks, then a bot's interpretation. (log header)

## Authority
- **R-054** Who approves what. One consolidated ruling: see `R-054-approval-authority.md`. It replaces R-004, R-015, R-019, R-027, R-028, R-038, R-044, R-047, R-052, and the approval parts of R-045, R-046, R-048, R-049, R-051 and the R-040 exception.

## Verification and deployment
- **R-007** Deploying a live profile edit is Gem's, or a bot Gem delegated it to in Gem's own written words. No bot applies a profile edit on a relay.
- **R-008** A relayed approval isn't Gem's authority until the recording bot confirms it with Gem. The relaying bot can't be the only evidence for something in its own favour.
- **R-009** An unapproved draft binds no one. A deploy counts as confirmed when the live text matches a codex version whose CHANGELOG records Gem's approval.
- **R-010** (as updated 16 Oct) Archivist deploys on Gem's request in its own chat, or an Imitator-approved version after a 1:1 confirmation with Imitator and a Safeguard dry run. Gem-only cases still need Gem.
- **R-014** Gem may ratify profile writes after the fact; the process breach still stands. Explorer never writes live profiles, its own included.
- **R-018** (as updated 16 Oct) Gem's voice-call words count straight away. A call decision passed on by another bot counts after a 1:1 check with the bot that took the call. Self-benefiting relays still need Gem.
- **R-023** Codex version files are immutable. CHANGELOG is authoritative for deployment status.
- **R-029** "Deploy all" authorises the deployment and accepts in-scope Imitator approvals. It doesn't cure an approval Imitator couldn't give. Archivist records Gem's words before deploying.
- **R-035** Immutable includes appends. Archivist writes each version file complete before deploying, and later events go only in the CHANGELOG.
- **R-053** A bot's claim that something runs doesn't count without run evidence or an independent check (Engineer's routines are treated as not running until shown).

## Roles, routing and records
- **R-006** Mender detects and logs every stall. Arbiter only escalates an Architect stall to Gem (and tells Mender).
- **R-011** (as amended) Stall reports in `schedule.md` step 2 go to Mender, which owns `schedule.md`.
- **R-012** (as updated twice) Inquirer 0314faa4 owns Inquirer's duties; output from e613112b is verified too. (Inquirer and Inferer merging is approved under R-051.)
- **R-013** Gem may chat with any bot, dormant or not. Dormancy stops scheduled and bot-routed work. Safeguard review applies to all bots.
- **R-016** Mediator is live in P2 despite its "P4" title. The rename waits for Gem or Archivist on Gem's request.
- **R-017** "Assembler's role map" in any brief means Archivist.
- **R-021** `phases.md` wins over `directory.md` on phases and live bots. Explorer keeps `directory.md` in step until an owner is named.
- **R-024** Imitator's decision log is `/workspace/governance/approvals.md`.
- **R-025** `phases.md` sets the live set for Scorer's sampling.
- **R-026** "Messenger's digest" means Explorer's combined digest inbox.
- **R-039** A task Gem gives a named bot directly authorises it, with all safety rules applying. Routine repo work belongs to Engineer.
- **R-044 routing split / R-046** Explorer assigns new work; Mender keeps operational routing (run order, recovery, rerouting, stalls). The six redundancy versions are deployed on Gem's 7:54pm words. The "fold" option isn't approved.
- **R-051 (merges)** Gem approved: Mediator into Mender; Scorer with Scrutineer; Safeguard with Safekeeper; Inquirer with Inferer; the Extractor fold. Architect drafts; Gem approves checker merges. Every retirement needs an archive first. A merged checker pair still can't check its own work.

## Pushes, publishing and outward actions
- **R-020** Pushes to public or shared repos (other than Engineer on GitHub) need Gem's words for that push; Safeguard dry-runs first unless Gem named the push.
- **R-022** The 3:49am 10 Oct codey/complete-plans push was approved by Gem and isn't a breach.
- **R-031** (as amended and updated) bonus_scores_AU.xlsx is open to bots on the box. It isn't shared outside the box without Gem's own words naming the destination, in the publishing bot's own chat, after a Safeguard dry run. No bot, Arbiter included, lifts this hold. (gvmw's already-committed copies are covered by R-042.)
- **R-036** (time and push rule) Read "10:18am" as about 10:21am. A public or shared push needs Gem's words for that push; a dry run is never a go-ahead. (Doesn't apply to Engineer on GitHub, R-045.)
- **R-037** A public or production Vercel deploy needs Gem's words for that deploy; dry run first if Gem didn't name it.
- **R-040** (as amended and updated) Engineer didn't breach process on gvmw. After any repo is created or pushed: read back actual visibility, have another bot confirm it, and scan pushes to public or shared repos (gvmw excepted). Who made gvmw public is still unknown.
- **R-042** gvmw stays public as it is, by Gem's choice, including what was already pushed. New content and other destinations still fall under R-031.
- **R-043** (final) The 4f43fc9 push had Gem's words; Engineer has two process gaps on record.
- **R-045** Engineer is fully free on GitHub, public repos included. No secrets in pushes. The R-031 data hold still applies to other destinations.
- **R-040 exception** gvmw pushes skip the Safekeeper scan. All other public or shared repos still need it.
- **R-049 (deletions)** Scrapes, data, logs and scratch files may be deleted without a backup. Code, notes, configs and bot instructions need a verified off-computer backup first, checked by another bot. No mass wipes. Every deletion is logged. (Whether Imitator can approve these is governed by R-054 row 4.)
- **R-050** (as updated) VEPA and swarm may go public once Safekeeper reviews VEPA's gambling keywords and swarm's sqlite file. Codey is clear. MedB only from a clean clone. DayneK/slapred and gemquota/golf have an active exposure; rotation, removal, history and visibility are Gem's.
- **R-051 (other answers)** Approved: healthchecks.io free watchdog, governance backup on Google Drive, token broker stage 1 (inventory), approvals tied to an action hash, an off-computer ledger with restore power moved off Mender, the 11 checks, free options only. Not adopted: deletion gate, data classes and BIE wall, privacy check on gvmw.

## Breach and incident findings (records, still standing)
- **R-020/R-036** Imitator's ~10:21am 10 Oct VEPA backup push: process breach, not reverted; keeping or deleting the branch is Gem's call.
- **R-032/R-033** Explorer's 28 moves on 10 Oct: process breach, moves stand. The cache deletion was approved by Gem. The hold on `/workspace/backups/bie-caches-2026-10-10/` stays.
- **R-034** (final) Explorer's deletion of 120 browser captures: ratified by Gem. Explorer confirms any deletion Gem's words don't name, and backs up first.
- **R-031** Extractor's spreadsheet without a dry run: process breach, low harm.
- **R-041** Points 3 to 6 (corrections by Mediator, Imitator, Inquirer and Safeguard) stand.

- 2026-10-22 22:20 AEST: Gem confirmed Imitator may approve retirements and making projects public on its own, and that BIE means bie_tools gambling data (see R-054 update).
