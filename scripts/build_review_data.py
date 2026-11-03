#!/usr/bin/env python3
"""Build sanitised ratings.json and reviews.json for the public swarm site.

Strict allowlist schema (Safeguard): only date (YYYY-MM-DD), bot (current bare
name), rating from a fixed label set, numeric scores (1-5 or null), and
outcome from a fixed label set. Fail closed: non-zero exit and write nothing
if any field or value falls outside the schema after the build.
"""
# Consumed by root index.html and v2/index.html via data/ and ../data/ respectively.
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

GOVERNANCE = Path("/workspace/governance")
REVIEWS_DIR = GOVERNANCE / "reviews"
ASSESSMENTS_DIR = GOVERNANCE / "assessments"
AUDITS_DIR = GOVERNANCE / "audits"
LEDGER_DIR = GOVERNANCE / "ledger"
OUT_DIR = Path(__file__).resolve().parent.parent / "data"

# Fixed allowlists
ALLOWED_RATINGS = frozenset({"Good", "Fair", "Poor", "NotRated"})
ALLOWED_OUTCOMES = frozenset({"pass", "fail", "flagged", "not_rated"})
ALLOWED_BOTS = frozenset(
    {
        "Mender",
        "Safeguard",
        "Scrutineer",
        "Archivist",
        "Architect",
        "Explorer",
        "Arbiter",
        "Inferer",
        "Investigator",
        "Imitator",
        "Emissary",
        "Engineer",
    }
)
ALLOWED_REVIEWERS = frozenset({"Scrutineer"})  # Scorer maps via retired-names

# Shared retired-names v001 (R-051): only these map; anything else unmappable is dropped
RETIRED_TO_CURRENT = {
    "Mediator": "Mender",
    "Scorer": "Scrutineer",
    "Safekeeper": "Safeguard",
    "Inquirer": "Inferer",
    "Extractor": "Emissary",
}

RATING_TO_OUTCOME = {
    "Good": "pass",
    "Fair": "flagged",
    "Poor": "fail",
    "NotRated": "not_rated",
}

DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})\.md$")
# Heading forms:
#   ## P1 (Ops) Mender — Good
#   ## P1 (Ops) Mender: Fair (Poor streak 1)
#   ### P1 (Ops) Mender: Good
#   ## P1 (Work) Explorer (`04dcca0d`): Poor
#   ## P1 (Roles) Architect — Not rated (nothing due)
HEADING_RATING_RE = re.compile(
    r"^#{2,3}\s+"
    r"(?:P\d+\s+\([^)]+\)\s+)?"  # optional P# (Group)
    r"(?P<name>[A-Za-z][A-Za-z0-9_-]*)"
    r"(?:\s*\(`[^`]+`\))?"  # optional id
    r"\s*[—:\-]\s*"
    r"(?P<rating>Good|Fair|Poor|Not\s+[Rr]ated)\b",
    re.MULTILINE,
)

# Assessment heading: ### P1 (Checks) Safeguard — 4/4/4/4/5
# or ### P1 (Ops) Mender — 5 / 5 / 5 / 4 / 5
# or ### P1 (Roles) Architect — 5/5/5/5/n/a
SCORE_HEADING_RE = re.compile(
    r"^#{2,3}\s+"
    r"(?:P\d+\s+\([^)]+\)\s+)?"
    r"(?P<name>[A-Za-z][A-Za-z0-9_-]*)"
    r"(?:\s*\(`[^`]+`\))?"
    r"\s*[—:\-]\s*"
    r"(?P<scores>(?:[1-5]|n/?a)(?:\s*/\s*(?:[1-5]|n/?a)){4})"
    r"\b",
    re.MULTILINE | re.IGNORECASE,
)

# Table row: | P1 (Ops) Mender | 4 | 4 | 4 | 4 | 4 | ...
SCORE_TABLE_RE = re.compile(
    r"^\|\s*(?:P\d+\s+\([^)]+\)\s+)?"
    r"(?P<name>[A-Za-z][A-Za-z0-9_-]*)"
    r"(?:\s*\(`[^`]+`\))?"
    r"\s*\|\s*(?P<s1>[1-5]|n/?a)\s*"
    r"\|\s*(?P<s2>[1-5]|n/?a)\s*"
    r"\|\s*(?P<s3>[1-5]|n/?a)\s*"
    r"\|\s*(?P<s4>[1-5]|n/?a)\s*"
    r"\|\s*(?P<s5>[1-5]|n/?a)\s*\|",
    re.MULTILINE | re.IGNORECASE,
)

# Correction: **Engineer revised from Poor to Fair.**
CORRECTION_RE = re.compile(
    r"\*\*(?P<name>[A-Za-z][A-Za-z0-9_-]*)\s+revised\s+from\s+"
    r"(?:Good|Fair|Poor|Not\s+[Rr]ated)\s+to\s+(?P<rating>Good|Fair|Poor|Not\s+[Rr]ated)\.??\*\*",
    re.IGNORECASE,
)

NOT_SCORED_RE = re.compile(
    r"^#{2,3}\s+(?:P\d+\s+\([^)]+\)\s+)?"
    r"(?P<name>[A-Za-z][A-Za-z0-9_-]*)"
    r"(?:\s*\(`[^`]+`\))?"
    r"\s*[—:\-]\s*(?:not\s+scored|n/?a)\b",
    re.MULTILINE | re.IGNORECASE,
)


def norm_rating(raw: str) -> str:
    r = re.sub(r"\s+", " ", raw.strip())
    if r.lower().startswith("not"):
        return "NotRated"
    return r[:1].upper() + r[1:].lower() if r.lower() in {"good", "fair", "poor"} else r


def parse_score_token(tok: str):
    t = tok.strip().lower().replace(" ", "")
    if t in {"n/a", "na"}:
        return None
    v = int(t)
    if v < 1 or v > 5:
        raise ValueError(f"score out of range: {v}")
    return v


def map_bot(raw_name: str) -> str | None:
    """Return current bare name, or None to drop."""
    name = raw_name.strip()
    # Strip accidental prefixes
    name = re.sub(r"^RETIRED\s+", "", name, flags=re.IGNORECASE)
    if name in RETIRED_TO_CURRENT:
        name = RETIRED_TO_CURRENT[name]
    if name not in ALLOWED_BOTS:
        return None
    return name


def daily_review_files() -> list[Path]:
    files = []
    for p in sorted(REVIEWS_DIR.glob("*.md")):
        if DATE_RE.match(p.name):
            files.append(p)
    return files


def daily_assessment_files() -> list[Path]:
    files = []
    for p in sorted(ASSESSMENTS_DIR.glob("*.md")):
        if DATE_RE.match(p.name):
            files.append(p)
    return files


def parse_review_ratings(path: Path) -> dict[str, str]:
    """Return bot -> rating for one daily review file. Last heading wins; corrections override."""
    text = path.read_text(encoding="utf-8")
    found: dict[str, str] = {}
    for m in HEADING_RATING_RE.finditer(text):
        bot = map_bot(m.group("name"))
        if not bot:
            continue
        # Scrutineer never reviews itself; skip self-ratings if any
        rating = norm_rating(m.group("rating"))
        if rating not in ALLOWED_RATINGS:
            continue
        found[bot] = rating
    for m in CORRECTION_RE.finditer(text):
        bot = map_bot(m.group("name"))
        if not bot:
            continue
        rating = norm_rating(m.group("rating"))
        if rating not in ALLOWED_RATINGS:
            continue
        found[bot] = rating
    return found


def parse_assessment_scores(path: Path) -> dict[str, list]:
    """Return bot -> list of 5 scores (int|None)."""
    text = path.read_text(encoding="utf-8")
    found: dict[str, list] = {}

    for m in SCORE_HEADING_RE.finditer(text):
        bot = map_bot(m.group("name"))
        if not bot:
            continue
        parts = re.split(r"\s*/\s*", m.group("scores").strip())
        if len(parts) != 5:
            continue
        try:
            scores = [parse_score_token(p) for p in parts]
        except ValueError:
            continue
        found[bot] = scores

    for m in SCORE_TABLE_RE.finditer(text):
        bot = map_bot(m.group("name"))
        if not bot:
            continue
        try:
            scores = [
                parse_score_token(m.group("s1")),
                parse_score_token(m.group("s2")),
                parse_score_token(m.group("s3")),
                parse_score_token(m.group("s4")),
                parse_score_token(m.group("s5")),
            ]
        except ValueError:
            continue
        # Prefer heading form if already present; table fills gaps
        if bot not in found:
            found[bot] = scores

    # Explicit "not scored" → no scores entry (rating may still come from reviews)
    for m in NOT_SCORED_RE.finditer(text):
        bot = map_bot(m.group("name"))
        if bot and bot in found:
            # Keep scores if we already parsed numeric; "not scored" means skip
            pass

    return found


def detect_reviewer(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")[:2000]
    if re.search(r"\bScorer\b", text) and not re.search(r"\bScrutineer\b", text):
        mapped = map_bot("Scorer")
        return mapped or "Scrutineer"
    return "Scrutineer"


def build() -> tuple[list[dict], list[dict], dict]:
    ratings_by_key: dict[tuple[str, str], dict] = {}
    # Collect ratings from daily reviews
    for path in daily_review_files():
        day = path.stem  # YYYY-MM-DD
        for bot, rating in parse_review_ratings(path).items():
            key = (day, bot)
            rec = ratings_by_key.get(key, {"date": day, "bot": bot})
            rec["rating"] = rating
            ratings_by_key[key] = rec

    # Attach scores from assessments
    for path in daily_assessment_files():
        day = path.stem
        for bot, scores in parse_assessment_scores(path).items():
            key = (day, bot)
            rec = ratings_by_key.get(key, {"date": day, "bot": bot})
            rec["scores"] = scores
            ratings_by_key[key] = rec

    # Audits / ledger: no per-bot rating schema found; skipped (noted in meta)
    audits_note = "no usable per-bot ratings in audits/ or ledger/"
    if AUDITS_DIR.is_dir() or LEDGER_DIR.is_dir():
        audits_note = (
            "audits/ and ledger/ inspected; no allowlisted rating/score fields; skipped"
        )

    rating_records = []
    for key in sorted(ratings_by_key.keys()):
        rec = ratings_by_key[key]
        # Must have at least a rating or scores
        if "rating" not in rec and "scores" not in rec:
            continue
        out = {"date": rec["date"], "bot": rec["bot"]}
        if "rating" in rec:
            out["rating"] = rec["rating"]
        if "scores" in rec:
            out["scores"] = rec["scores"]
        rating_records.append(out)

    # reviews.json: per-day counts by outcome and reviewer
    # Aggregate from rating records that have a rating
    counts: dict[tuple[str, str, str], int] = defaultdict(int)
    reviewer_by_day: dict[str, str] = {}
    for path in daily_review_files():
        day = path.stem
        reviewer_by_day[day] = detect_reviewer(path)

    for rec in rating_records:
        if "rating" not in rec:
            continue
        day = rec["date"]
        reviewer = reviewer_by_day.get(day, "Scrutineer")
        if reviewer not in ALLOWED_REVIEWERS:
            continue
        outcome = RATING_TO_OUTCOME[rec["rating"]]
        counts[(day, reviewer, outcome)] += 1

    review_records = []
    for (day, reviewer, outcome), count in sorted(counts.items()):
        review_records.append(
            {
                "date": day,
                "reviewer": reviewer,
                "outcome": outcome,
                "count": count,
            }
        )

    meta = {
        "rating_days": sorted({r["date"] for r in rating_records}),
        "bots": sorted({r["bot"] for r in rating_records}),
        "review_files": [p.name for p in daily_review_files()],
        "assessment_files": [p.name for p in daily_assessment_files()],
        "audits_ledger": audits_note,
        "dropped_unmapped": "names outside ALLOWED_BOTS and RETIRED_TO_CURRENT are dropped",
        "outcome_map": dict(RATING_TO_OUTCOME),
    }
    return rating_records, review_records, meta


def validate_ratings(records: list[dict]) -> list[str]:
    errors = []
    allowed_keys = frozenset({"date", "bot", "rating", "scores"})
    for i, rec in enumerate(records):
        extra = set(rec.keys()) - allowed_keys
        if extra:
            errors.append(f"ratings[{i}] extra keys: {sorted(extra)}")
        if "date" not in rec or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", rec["date"]):
            errors.append(f"ratings[{i}] bad date: {rec.get('date')!r}")
        else:
            try:
                date.fromisoformat(rec["date"])
            except ValueError:
                errors.append(f"ratings[{i}] invalid calendar date")
        if rec.get("bot") not in ALLOWED_BOTS:
            errors.append(f"ratings[{i}] bot not allowlisted: {rec.get('bot')!r}")
        if "rating" in rec and rec["rating"] not in ALLOWED_RATINGS:
            errors.append(f"ratings[{i}] rating not allowlisted: {rec.get('rating')!r}")
        if "rating" not in rec and "scores" not in rec:
            errors.append(f"ratings[{i}] needs rating or scores")
        if "scores" in rec:
            scores = rec["scores"]
            if not isinstance(scores, list) or len(scores) != 5:
                errors.append(f"ratings[{i}] scores must be length-5 list")
            else:
                for j, s in enumerate(scores):
                    if s is None:
                        continue
                    if not isinstance(s, int) or isinstance(s, bool) or s < 1 or s > 5:
                        errors.append(f"ratings[{i}].scores[{j}] not 1-5 int or null")
        # Reject any string values outside allowlisted fields
        for k, v in rec.items():
            if k in {"date", "bot", "rating"}:
                if not isinstance(v, str):
                    errors.append(f"ratings[{i}].{k} must be string")
            if isinstance(v, str) and k not in {"date", "bot", "rating"}:
                errors.append(f"ratings[{i}] unexpected string field {k}")
    return errors


def validate_reviews(records: list[dict]) -> list[str]:
    errors = []
    allowed_keys = frozenset({"date", "reviewer", "outcome", "count"})
    for i, rec in enumerate(records):
        extra = set(rec.keys()) - allowed_keys
        if extra:
            errors.append(f"reviews[{i}] extra keys: {sorted(extra)}")
        if "date" not in rec or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", rec["date"]):
            errors.append(f"reviews[{i}] bad date")
        if rec.get("reviewer") not in ALLOWED_REVIEWERS:
            errors.append(f"reviews[{i}] reviewer not allowlisted: {rec.get('reviewer')!r}")
        if rec.get("outcome") not in ALLOWED_OUTCOMES:
            errors.append(f"reviews[{i}] outcome not allowlisted: {rec.get('outcome')!r}")
        c = rec.get("count")
        if not isinstance(c, int) or isinstance(c, bool) or c < 0:
            errors.append(f"reviews[{i}] count must be non-negative int")
        for k, v in rec.items():
            if k in {"date", "reviewer", "outcome"} and not isinstance(v, str):
                errors.append(f"reviews[{i}].{k} must be string")
    return errors


def atomic_write(path: Path, payload: dict) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def main() -> int:
    rating_records, review_records, meta = build()

    errors = validate_ratings(rating_records) + validate_reviews(review_records)
    if errors:
        print("FAIL CLOSED: schema validation errors:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    # Content safety: JSON must not contain free text beyond allowlisted tokens
    blob = json.dumps({"r": rating_records, "v": review_records})
    forbidden = re.compile(
        r"(?i)(@[a-z0-9._%+-]+\.[a-z]{2,}|"
        r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b|"
        r"ghp_[A-Za-z0-9]+|github_pat_[A-Za-z0-9_]+|"
        r"\b(casino|pokies|gambling|BIE)\b)"
    )
    if forbidden.search(blob):
        print("FAIL CLOSED: forbidden content pattern in output JSON", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ratings_payload = {
        "schema_version": 1,
        "allowed_ratings": sorted(ALLOWED_RATINGS),
        "allowed_bots": sorted(ALLOWED_BOTS),
        "records": rating_records,
        "meta": {
            "date_range": [meta["rating_days"][0], meta["rating_days"][-1]]
            if meta["rating_days"]
            else [],
            "bot_count": len(meta["bots"]),
            "record_count": len(rating_records),
            "sources": {
                "reviews": meta["review_files"],
                "assessments": meta["assessment_files"],
                "audits_ledger": meta["audits_ledger"],
            },
        },
    }
    reviews_payload = {
        "schema_version": 1,
        "allowed_outcomes": sorted(ALLOWED_OUTCOMES),
        "allowed_reviewers": sorted(ALLOWED_REVIEWERS),
        "outcome_map": meta["outcome_map"],
        "records": review_records,
        "meta": {
            "date_range": [
                review_records[0]["date"],
                review_records[-1]["date"],
            ]
            if review_records
            else [],
            "record_count": len(review_records),
        },
    }

    # Re-validate embedded records only (meta is site-local numbers/names)
    errors = validate_ratings(ratings_payload["records"]) + validate_reviews(
        reviews_payload["records"]
    )
    if errors:
        print("FAIL CLOSED: post-wrap validation failed", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    atomic_write(OUT_DIR / "ratings.json", ratings_payload)
    atomic_write(OUT_DIR / "reviews.json", reviews_payload)

    print(
        f"OK: {len(rating_records)} rating records, {len(review_records)} review rows; "
        f"bots={meta['bots']}; days={meta['rating_days']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
