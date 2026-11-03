#!/usr/bin/env python3
"""Allowlist sync of public hub HTML/MD from /workspace/governance.

Fail-closed: copies only listed relative paths; refuses any file whose text
matches the same content gate as refresh_and_push.sh (emails, tokens, phones,
casino/pokies/gambling/BIE). Writes a machine-readable report to
data/site_sync_report.json. Does not commit or push.

Paths that fail the gate are listed under manual_required — Engineer must
curate those by hand (strip or paraphrase) before publishing.
"""
from __future__ import annotations

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


def main() -> int:
    if not GOV.is_dir():
        print("FAIL: /workspace/governance missing", file=sys.stderr)
        return 1

    copied: list[dict] = []
    unchanged: list[str] = []
    missing: list[str] = []
    manual: list[dict] = []
    errors: list[str] = []

    for rel in ALLOWLIST:
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
        "schema": 1,
        "generated_at": datetime.now(BNE).strftime("%Y-%m-%d %H:%M:%S AEST"),
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_root": str(GOV),
        "allowlist": list(ALLOWLIST),
        "copied": copied,
        "unchanged": unchanged,
        "missing_source": missing,
        "manual_required": manual,
        "errors": errors,
        "ok": not errors and not missing,
        "auto_clean": not manual and not missing and not errors,
    }
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("ok", "auto_clean", "copied", "unchanged", "missing_source", "manual_required")}, indent=2))
    # Non-zero only on hard errors (missing gov root already handled). Gate hits are expected → exit 0.
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
