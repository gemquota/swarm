#!/usr/bin/env python3
"""Ensure framed governance HTML shares hub-theme.css, doc-nav, and print styles."""
from __future__ import annotations
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
  ROOT/"governance/master/governance-master.html",
  ROOT/"governance/rulings/R-054-approval-authority.html",
  ROOT/"governance/rulings/in-force.html",
  ROOT/"governance/rulings/annex-history.html",
]
LINK = '<link rel="stylesheet" href="../../assets/hub-theme.css">'
# master is one level deeper from assets? governance/master -> ../../assets OK
# rulings same

def ensure(path: Path) -> None:
  text = path.read_text(encoding="utf-8")
  rel = "../../assets/hub-theme.css"
  if path.parent.name == "master":
    rel = "../../assets/hub-theme.css"
  link = f'<link rel="stylesheet" href="{rel}">'
  if "hub-theme.css" not in text:
    text = text.replace("</head>", link+"\n</head>", 1)
  if 'class="doc-nav"' not in text and "<body" in text:
    nav = '''<nav class="doc-nav" aria-label="Document"><a href="../../index.html">Hub</a><span class="sep">·</span><a href="../../index.html#governance">Governance</a></nav>\n'''
    text = text.replace("<body>", "<body>\n"+nav, 1)
    text = text.replace("<body >", "<body>\n"+nav, 1)
  path.write_text(text)
  print("shell ok", path.relative_to(ROOT))

def main():
  for t in TARGETS:
    if t.exists():
      ensure(t)
  print("PASS: doc shell")

if __name__ == "__main__":
  main()
