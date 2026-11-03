#!/usr/bin/env python3
"""Assert v2 hub resolves shared data, observatory embeds, and governance URLs."""
from __future__ import annotations
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []

def resolve(base: Path, href: str) -> Path | None:
    parsed = urlparse(href)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    return (base / parsed.path).resolve()

def main() -> int:
    v2 = ROOT / "v2" / "index.html"
    if not v2.exists():
        ERRORS.append("v2/index.html missing")
        print("\n".join(ERRORS)); return 1
    text = v2.read_text(encoding="utf-8")
    # required markers
    for needle in ("../data/", "../observatory.html", "../governance/", "arch-diagrams-root", "assistant-ux.js"):
        if needle not in text:
            ERRORS.append(f"v2/index.html missing marker {needle!r}")
    # data files
    for name in ("ratings.json", "reviews.json", "architecture.json"):
        p = ROOT / "data" / name
        if not p.exists():
            ERRORS.append(f"missing {p.relative_to(ROOT)}")
    # iframe / link targets under v2
    for m in re.finditer(r'(?:src|data-src|href)="([^"]+)"', text):
        href = m.group(1)
        if href.startswith("#") or href.startswith("mailto:"):
            continue
        # strip query
        path_part = href.split("?",1)[0]
        target = resolve(v2.parent, path_part)
        if target is None:
            continue
        if not str(target).startswith(str(ROOT)):
            continue
        if not target.exists():
            ERRORS.append(f"v2 broken local ref {href!r} -> {target}")
    # root still has redirects for moved reviews
    for name in (
        "governance/reviews/2026-10-10-governance-io-report.html",
        "governance/reviews/2026-10-15-governance-authority-responsibility.html",
    ):
        p = ROOT / name
        if not p.exists():
            ERRORS.append(f"missing redirect stub {name}")
        else:
            body = p.read_text(encoding="utf-8")
            if "archive/reviews" not in body:
                ERRORS.append(f"{name} is not a redirect into archive/reviews")
        archived = ROOT / "archive" / "reviews" / Path(name).name
        if not archived.exists():
            ERRORS.append(f"missing archived review {archived.relative_to(ROOT)}")
    # freeze unmodified marker: MANIFEST lives outside freeze
    if (ROOT / "archive" / "2026-11-03" / "MANIFEST.sha256").exists():
        ERRORS.append("MANIFEST must not be written inside archive/2026-11-03/")
    if not (ROOT / "archive" / "MANIFEST-2026-11-03.sha256").exists():
        ERRORS.append("missing archive/MANIFEST-2026-11-03.sha256")
    if ERRORS:
        print("\n".join("FAIL: " + e for e in ERRORS))
        return 1
    print("PASS: dual-hub smoke checks")
    return 0

if __name__ == "__main__":
    sys.exit(main())
