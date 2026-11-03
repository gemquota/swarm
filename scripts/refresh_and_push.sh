#!/usr/bin/env bash
# Refresh swarm rating/review JSON from box governance data, then commit
# (and optionally push) only data/ changes. Engineer runs this from a
# daily routine. Does not schedule itself.
#
# Safeguard gates:
# - hard-stop on gitleaks or content-check hit
# - staged diff paths must be data/ only (abort otherwise)
# - every run (including aborted) appends a line to
#   /workspace/governance/github-log.md (bot=Engineer, account=gemquota)
#
# Usage:
#   scripts/refresh_and_push.sh           # build + commit data/ only; no push
#   scripts/refresh_and_push.sh --push    # same, then push current branch
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GOV_LOG="/workspace/governance/github-log.md"
BRANCH="$(git -C "$ROOT" rev-parse --abbrev-ref HEAD)"
TS="$(TZ=Australia/Brisbane date '+%Y-%m-%d %H:%M:%S AEST')"
DO_PUSH=0
STATUS="started"
DETAIL=""
COMMIT_SHA=""

log_line() {
  local action="$1"
  local extra="${2:-}"
  mkdir -p "$(dirname "$GOV_LOG")"
  {
    printf -- '- %s bot=Engineer account=gemquota repo=gemquota/swarm visibility=PUBLIC action=%s branch=%s' \
      "$TS" "$action" "$BRANCH"
    if [[ -n "$COMMIT_SHA" ]]; then
      printf ' commit=%s' "$COMMIT_SHA"
    fi
    if [[ -n "$extra" ]]; then
      printf ' note="%s"' "$extra"
    fi
    printf '\n'
  } >>"$GOV_LOG"
}

abort() {
  local reason="$1"
  STATUS="aborted"
  DETAIL="$reason"
  log_line "refresh_aborted" "$reason"
  echo "ABORT: $reason" >&2
  exit 1
}

trap 'if [[ "$STATUS" == "started" ]]; then log_line "refresh_aborted" "unexpected exit"; fi' EXIT

cd "$ROOT"

if [[ "${1:-}" == "--push" ]]; then
  DO_PUSH=1
fi

# 1) Rebuild JSON from box governance sources
python3 "$ROOT/scripts/build_review_data.py" || abort "build_review_data.py failed (fail-closed)"

# 2) Content grep on data/ (emails, tokens, phones, casino/pokies/BIE/gambling)
CONTENT_HITS="$(
  grep -EniE \
    '(@[A-Za-z0-9._%+-]+\.[A-Za-z]{2,})|([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})|(ghp_[A-Za-z0-9]+)|(github_pat_[A-Za-z0-9_]+)|(sk-[A-Za-z0-9]{20,})|(\+?[0-9][0-9\-\s]{8,}[0-9])|\b(casino|pokies|gambling|BIE)\b' \
    "$ROOT"/data/*.json 2>/dev/null || true
)"
if [[ -n "$CONTENT_HITS" ]]; then
  abort "content-check hit in data/: $(echo "$CONTENT_HITS" | tr '\n' ' ' | head -c 200)"
fi

# 3) gitleaks on data/ and scripts touched by refresh
GITLEAKS_BIN="${GITLEAKS_BIN:-/tmp/gitleaks}"
if [[ ! -x "$GITLEAKS_BIN" ]]; then
  abort "gitleaks binary missing at $GITLEAKS_BIN"
fi
GITLEAKS_OUT="$(mktemp)"
if ! "$GITLEAKS_BIN" detect --redact --no-banner --no-git --source "$ROOT/data" -f json -r "$GITLEAKS_OUT" >/dev/null 2>&1; then
  abort "gitleaks hit in data/ (see scan output)"
fi
rm -f "$GITLEAKS_OUT"

# 4) Stage only data/ and verify staged paths
git -C "$ROOT" add -- data/
STAGED="$(git -C "$ROOT" diff --cached --name-only)"
if [[ -z "$STAGED" ]]; then
  STATUS="ok_noop"
  log_line "refresh_noop" "no data/ changes"
  echo "No data/ changes to commit."
  STATUS="done"
  exit 0
fi
BAD="$(echo "$STAGED" | grep -vE '^data/' || true)"
if [[ -n "$BAD" ]]; then
  git -C "$ROOT" reset -q HEAD --
  abort "staged paths outside data/: $(echo "$BAD" | tr '\n' ' ')"
fi

# 5) Commit data/ only
git -C "$ROOT" -c user.name='Engineer' -c user.email='engineer@users.noreply.github.com' \
  commit -m "data: refresh ratings and review graphs JSON

Built from /workspace/governance reviews and assessments on the box.
Allowlisted fields only (date, bot, rating, scores, outcome)."
COMMIT_SHA="$(git -C "$ROOT" rev-parse HEAD)"

# 6) Optional push (caller must pass --push; default is local commit only)
if [[ "$DO_PUSH" -eq 1 ]]; then
  # Re-check staged/committed tree is still data/-only vs previous
  PREV="$(git -C "$ROOT" rev-parse HEAD~1)"
  CHANGED="$(git -C "$ROOT" diff --name-only "$PREV" HEAD)"
  BAD2="$(echo "$CHANGED" | grep -vE '^data/' || true)"
  if [[ -n "$BAD2" ]]; then
    abort "commit touched non-data paths: $(echo "$BAD2" | tr '\n' ' ')"
  fi
  git -C "$ROOT" push -u origin "$BRANCH" || abort "git push failed"
  log_line "refresh_push" "data/ only"
else
  log_line "refresh_commit" "data/ only; push skipped"
fi

STATUS="done"
echo "OK: $COMMIT_SHA (push=$([[ $DO_PUSH -eq 1 ]] && echo yes || echo no))"
