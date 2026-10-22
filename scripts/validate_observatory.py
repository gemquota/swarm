#!/usr/bin/env python3
"""Dependency-free structural checks for the static swarm observatory."""
from __future__ import annotations

import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


class Document(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.tabs: list[tuple[str, str]] = []
        self.panels: set[str] = set()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if a.get("role") == "tab":
            self.tabs.append((a.get("aria-controls", ""), a.get("id", "")))
        if a.get("role") == "tabpanel":
            self.panels.add(a.get("id", ""))
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])


def check_html(path: Path) -> str:
    source = path.read_text(encoding="utf-8")
    parser = Document()
    parser.feed(source)
    duplicates = sorted({x for x in parser.ids if parser.ids.count(x) > 1})
    if duplicates:
        ERRORS.append(f"{path.relative_to(ROOT)}: duplicate IDs: {', '.join(duplicates)}")
    for panel, tab in parser.tabs:
        if not panel or panel not in parser.panels:
            ERRORS.append(f"{path.relative_to(ROOT)}: tab {tab!r} points to missing panel {panel!r}")
    for href in parser.links:
        parsed = urlparse(href)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        target = (path.parent / parsed.path).resolve()
        if not target.exists():
            ERRORS.append(f"{path.relative_to(ROOT)}: broken local link {href!r}")
    return source


def main() -> int:
    observatory = ROOT / "observatory.html"
    index = ROOT / "index.html"
    if not observatory.exists() or not index.exists():
        ERRORS.append("Expected index.html and observatory.html at repository root.")
    if ERRORS:
        print("\n".join("FAIL: " + e for e in ERRORS))
        return 1

    html = check_html(observatory)
    index_html = check_html(index)
    if 'href="observatory.html"' not in index_html:
        ERRORS.append("index.html does not link to observatory.html")
    for marker in ("STATIC DOCUMENTARY VIEW", "NOT CONNECTED", "UNKNOWN", "DOCUMENTED"):
        if marker not in html:
            ERRORS.append(f"observatory.html missing required truth-boundary marker {marker!r}")

    schema_dir = ROOT / "docs" / "schemas"
    expected = {
        "entity.schema.json": {"id", "type", "label", "status", "source", "visibility"},
        "approval.schema.json": {"id", "principal", "source", "issuedAt", "action", "validationStatus"},
        "event.schema.json": {"id", "type", "eventTime", "producer", "source", "status"},
    }
    for filename, required in expected.items():
        path = schema_dir / filename
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            ERRORS.append(f"{path.relative_to(ROOT)}: cannot parse JSON schema: {exc}")
            continue
        missing = required - set(schema.get("required", []))
        if missing:
            ERRORS.append(f"{filename}: required contract fields missing: {', '.join(sorted(missing))}")
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            ERRORS.append(f"{filename}: unexpected or missing JSON Schema draft declaration")

    for rel in (
        "docs/development/THREAT_MODEL.md",
        "docs/development/DATA_PROVENANCE.md",
        "docs/development/TRACEABILITY_MATRIX.md",
        "docs/development/ACCEPTANCE_CRITERIA.md",
    ):
        if not (ROOT / rel).is_file():
            ERRORS.append(f"Missing Phase 0–1 contract: {rel}")

    if ERRORS:
        print("\n".join("FAIL: " + e for e in ERRORS))
        return 1
    print("PASS: HTML tab/panel references, unique IDs, local links, truth-boundary markers, schemas, and Phase 0–1 documents.")
    print("LIMIT: structural checks only; no runtime state, browser execution, policy enforcement, or event authenticity is verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
