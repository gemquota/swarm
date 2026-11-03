# Intent — R-058 exclude governance master from public sync allowlist

Arbiter R-058 (2026-11-04): leave governance/master/** and archive/**/governance/master
out of swarm's public sync allowlist until Gem's direct words name them and Safeguard
re-checks. Do not delete already-published files; no history rewrite; no force-push.
Do not edit scripts/refresh_and_push.sh.

Also R-057 gap logged separately in /workspace/governance/github-log.md (md Pages).
