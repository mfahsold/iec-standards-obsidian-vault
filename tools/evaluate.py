#!/usr/bin/env python3
"""Evaluate the RAG pipeline against data-generated probes.

Default: retrieval + sufficiency decisions only (fast).
--generate: also generate answers and check expected strings/citations (slow).

Usage:
    python3 tools/evaluate.py
    python3 tools/evaluate.py --generate
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent.parent


def load_module(name: str):
    path = ROOT / "tools" / name
    spec = importlib.util.spec_from_file_location(name.replace(".py", ""), path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generate", action="store_true")
    args = parser.parse_args()

    al = load_module("agent-loop.py")
    probes = load_module("probes.py")
    cases: List[Dict[str, Any]] = probes.generate()
    url = os.environ.get("OLLAMA_URL", "http://localhost:11434").rstrip("/")
    model = os.environ.get("OLLAMA_MODEL", "qwen3.5:2b")
    embed_model = os.environ.get("EMBED_MODEL", "nomic-embed-text")
    top_k = int(os.environ.get("TOP_K", "5"))
    index_path = Path(os.environ.get("RAG_INDEX", str(al.DEFAULT_INDEX)))

    hits = decisions = answers = 0
    print(f"{'#':>2}  {'retrieval':<9} {'decision':<8} {'answer':<8}  question")
    for number, case in enumerate(cases, start=1):
        question = case["question"]
        retrieved = al.retrieve(question, index_path, url, embed_model, top_k)
        sources = [c["citationLabel"] for c in retrieved]
        expected_source = case.get("source", "")
        retrieval_ok = not expected_source or any(expected_source in s for s in sources)
        hits += int(retrieval_ok)

        contexts = al.structured_context(question, al.INDEX_JSON) + retrieved
        sufficient, _ = al.judge(question, contexts, url, model)
        decision_ok = sufficient != case["expect_refusal"]
        decisions += int(decision_ok)

        answer_ok = True
        if args.generate and decision_ok and sufficient:
            text = al.generate(question, contexts, url, model,
                               int(os.environ.get("NUM_CTX", "98304")),
                               int(os.environ.get("NUM_PREDICT", "8192")))
            lowered = text.lower()
            answer_ok = all(str(value).lower() in lowered for value in case.get("expected", []))
            answer_ok = answer_ok and "[Source:" in text
            answers += int(answer_ok)

        print(f"{number:>2}  {'OK' if retrieval_ok else 'MISS':<9} "
              f"{'OK' if decision_ok else 'FAIL':<8} "
              f"{('OK' if answer_ok else 'FAIL') if args.generate else '-':<8}  {question[:62]}")

    total = len(cases)
    print(f"\nRetrieval hit rate:  {hits}/{total}")
    print(f"Decision accuracy:   {decisions}/{total}")
    if args.generate:
        print(f"Answer accuracy:     {answers}/{total}")
    return 0 if decisions == total else 1


if __name__ == "__main__":
    sys.exit(main())
