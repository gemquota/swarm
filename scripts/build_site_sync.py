#!/usr/bin/env python3
"""Allowlist sync of selected governance HTML/MD from /workspace/governance.

Copies ONLY paths listed in ALLOWLIST into ROOT/governance/. Does not commit
or push. Does not publish the whole governance tree.

Content gate (on allowlisted paths only): refuses to auto-copy a file whose
text matches emails, common token prefixes, phone-like numbers, or the words
casino/pokies/gambling/BIE (same spirit as refresh_and_push.sh). Gate hits are
listed under manual_required in docs/development/site_sync_report.json and
need hand curation — the gate is not a claim that the public site is free of
those materials.

R-058 (2026-11-04): governance/master/** and archive/**/governance/master are
explicitly excluded from this public sync allowlist until Gem's direct words
name those documents and Safeguard re-checks. Already-published copies stay in
the repo (no history rewrite). This script must never add them to ALLOWLIST.
"""
from __future__ import annotations

import fnmatch
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
GOV = Path("/workspace/governance")
OUT_REPORT = ROOT / "docs" / "development" / "site_sync_report.json"
BNE = ZoneInfo("Australia/Brisbane")

# Relative paths under governance/ on both sides (site dest = ROOT/governance/...)
# Site-only HTML wrappers (in-force.html etc.) are rebuilt on the site side from
# curated markdown; they are not expected under /workspace/governance.
ALLOWLIST = (
    "cartography/role-map-interactive.html",
    "reviews/2026-10-15-governance-authority-responsibility.html",
    "reviews/2026-10-10-governance-io-report.html",
    "rulings/R-054-approval-authority.md",
    "rulings/in-force.md",
    "rulings/annex-history.md",
)

# R-058: never sync these into the public site via this script (or any future
# allowlist expansion). Patterns match relative paths under governance/ AND
# repo-relative paths under archive/**/governance/master.
EXCLUDE_PATTERNS = (
    "master",
    "master/**",
    "**/governance/master",
    "**/governance/master/**",
    "archive/**/governance/master",
    "archive/**/governance/master/**",
)

# Same spirit as refresh_and_push.sh content grep (word-boundary for BIE/gambling family)
# Phone-like: +E.164 or AU local; deliberately excludes ISO dates (YYYY-MM-DD)
# and short SVG/path number runs that tripped the refresh.sh digit pattern on HTML.
CONTENT_RE = re.compile(
    r"("
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    r"|ghp_[A-Za-z0-9]+"
    r"|github_pat_[A-Za-z0-9_]+"
    r"|sk-[A-Za-z0-9]{20,}"
    r"|\+\d{10,15}"
    r"|(?<![\d-])0[2-9]\d{8}(?!\d)"
    r"|\b(casino|pokies|gambling|BIE)\b"
    r")",
    re.IGNORECASE,
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def is_excluded(rel: str) -> bool:
    """True if rel (posix, no leading slash) matches an R-058 exclude pattern."""
    norm = rel.replace("\\", "/").lstrip("./")
    for pat in EXCLUDE_PATTERNS:
        if fnmatch.fnmatch(norm, pat):
            return True
        # Also treat any path segment equal to master under a governance/master prefix
        if "/governance/master/" in f"/{norm}/" or norm == "master" or norm.startswith("master/"):
            return True
    return False


def assert_allowlist_excludes_master() -> None:
    bad = [rel for rel in ALLOWLIST if is_excluded(rel)]
    if bad:
        raise SystemExit(
            "FAIL R-058: ALLOWLIST must not include governance master paths: "
            + ", ".join(bad)
        )


def main() -> int:
    assert_allowlist_excludes_master()
    if not GOV.is_dir():
        print("FAIL: /workspace/governance missing", file=sys.stderr)
        return 1

    copied: list[dict] = []
    unchanged: list[str] = []
    missing: list[str] = []
    manual: list[dict] = []
    errors: list[str] = []
    skipped_excluded: list[str] = []

    for rel in ALLOWLIST:
        if is_excluded(rel):
            skipped_excluded.append(rel)
            errors.append(f"R-058 exclude hit on allowlist entry: {rel}")
            continue
        src = GOV / rel
        dst = ROOT / "governance" / rel
        if not src.is_file():
            missing.append(rel)
            continue
        raw = src.read_bytes()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            manual.append({"path": rel, "reason": "not utf-8"})
            continue
        hit = CONTENT_RE.search(text)
        if hit:
            manual.append(
                {
                    "path": rel,
                    "reason": "content-gate",
                    "match": "[redacted-gate-hit]",
                }
            )
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        src_hash = sha256_bytes(raw)
        if dst.is_file() and sha256_bytes(dst.read_bytes()) == src_hash:
            unchanged.append(rel)
            continue
        shutil.copy2(src, dst)
        copied.append({"path": rel, "sha256": src_hash, "bytes": len(raw)})

    report = {
        "schema": 2,
        "generated_at": datetime.now(BNE).strftime("%Y-%m-%d %H:%M:%S AEST"),
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_root": str(GOV),
        "allowlist": list(ALLOWLIST),
        "exclude_patterns": list(EXCLUDE_PATTERNS),
        "exclude_note": (
            "R-058: governance/master/** and archive/**/governance/master are "
            "out of the public sync allowlist pending Gem direct words + Safeguard re-check. "
            "Already-published copies are not deleted by this script."
        ),
        "copied": copied,
        "unchanged": unchanged,
        "missing_source": missing,
        "manual_required": manual,
        "skipped_excluded": skipped_excluded,
        "errors": errors,
        "ok": not errors and not missing,
        "auto_clean": not manual and not missing and not errors,
    }
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in (
        "ok", "auto_clean", "copied", "unchanged", "missing_source",
        "manual_required", "skipped_excluded", "exclude_patterns",
    )}, indent=2))
    # Non-zero only on hard errors. Gate hits are expected → exit 0.
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
