#!/usr/bin/env python3
"""Generate evaluation probes from the live catalog instead of hardcoded Q&A.

Questions and expected values are derived from index/index.json, so the test
set follows the data. Abstention probes use synthetic references that are
guaranteed not to be in the vault.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent.parent
INDEX_JSON = ROOT / "index" / "index.json"


def note_stem(entry: Dict[str, Any]) -> str:
    ref = str(entry.get("ref", ""))
    return re.sub(r"[^A-Za-z0-9]+", "-", ref).strip("-")


def generate(index_json: Path = INDEX_JSON) -> List[Dict[str, Any]]:
    data = json.loads(index_json.read_text(encoding="utf-8"))
    cases: List[Dict[str, Any]] = []

    def add(question: str, expected: List[str], entry: Dict[str, Any]) -> None:
        cases.append({
            "question": question,
            "expect_refusal": False,
            "expected": [str(value) for value in expected],
            "source": note_stem(entry),
        })

    with_ics = [e for e in data if e.get("ics")]
    with_price = [e for e in data if isinstance(e.get("price_chf"), (int, float))]
    with_tc = [e for e in data if e.get("technical_committee")]
    with_type = [e for e in data if e.get("type")]

    for entry in with_ics[:3]:
        add(f"What are the ICS tags of {entry['ref']}?", [entry["ics"]], entry)
    for entry in with_price[:3]:
        add(f"What is the price of {entry['ref']}?",
            [entry["price_chf"], "CHF"], entry)
    for entry in with_tc[:2]:
        add(f"Which technical committee owns {entry['ref']}?",
            [str(entry["technical_committee"]).split()[0]], entry)
    for entry in with_type[:2]:
        add(f"What type of document is {entry['ref']}?", [entry["type"]], entry)

    existing = {str(e.get("ref", "")).lower() for e in data}
    for fake in ["IEC 99999:2099", "IEC 65000-1:2099", "ISO 88888:2099"]:
        if fake.lower() not in existing:
            cases.append({
                "question": f"What is the price of {fake}? Give me its ICS and price.",
                "expect_refusal": True,
                "expected": [],
                "source": "",
            })
    return cases


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cli", action="store_true",
                        help="print ready-to-run agent-loop.py commands")
    args = parser.parse_args()
    for case in generate():
        if args.cli:
            print(f'python3 tools/agent-loop.py "{case["question"]}"')
        else:
            print(("REFUSE " if case["expect_refusal"] else "ANSWER ") + case["question"])
