#!/usr/bin/env python3
"""Single source of runtime configuration for all tools.

Every value can be overridden by an environment variable. Run
`python3 tools/config.py --show` for the effective configuration and live
catalog/index statistics instead of hardcoding them in documentation.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Callable, TypeVar

T = TypeVar("T")

ROOT = Path(__file__).resolve().parent.parent
INDEX_JSON = ROOT / "index" / "index.json"


def env(name: str, default: T, cast: Callable[[str], T] = str) -> T:
    value = os.environ.get(name)
    return cast(value) if value is not None else default


OLLAMA_URL = env("OLLAMA_URL", "http://localhost:11434").rstrip("/")
OLLAMA_MODEL = env("OLLAMA_MODEL", "qwen3.5:2b")
EMBED_MODEL = env("EMBED_MODEL", "nomic-embed-text")

NUM_CTX = env("NUM_CTX", 98304, int)
NUM_PREDICT = env("NUM_PREDICT", 8192, int)
TEMPERATURE = env("TEMPERATURE", 0.6, float)
TOP_P = env("TOP_P", 0.95, float)
TOP_K_SAMPLE = env("TOP_K_SAMPLE", 20, int)
MIN_P = env("MIN_P", 0.0, float)
JUDGE_TEMPERATURE = env("JUDGE_TEMPERATURE", 0.0, float)
JUDGE_PREDICT = env("JUDGE_PREDICT", 512, int)

TOP_K = env("TOP_K", 5, int)
RRF_K = env("RRF_K", 60, int)
HYBRID = env("HYBRID", "1") == "1"
REQUEST_TIMEOUT = env("REQUEST_TIMEOUT", 240, int)

KEEP_ALIVE = env("KEEP_ALIVE", "10m")
EMBED_NUM_CTX = env("EMBED_NUM_CTX", 8192, int)
CHUNK_SIZE = env("CHUNK_SIZE", 800, int)
CHUNK_OVERLAP = env("CHUNK_OVERLAP", 100, int)
MIN_CONTENT = env("MIN_CONTENT", 50, int)

RAG_INDEX = Path(env("RAG_INDEX", str(ROOT / "index" / "embeddings.json")))


def show() -> None:
    print("== Runtime configuration ==")
    for name in sorted(
        key for key, value in globals().items()
        if key.isupper() and isinstance(value, (str, int, float, bool, Path))
    ):
        print(f"{name}: {globals()[name]}")

    catalog = json.loads(INDEX_JSON.read_text(encoding="utf-8"))
    notes = sorted(p for p in (ROOT / "standards").glob("*.md")
                   if p.name not in {"index-standards.md", "classics.md"})
    print("\n== Live data ==")
    print(f"catalog entries: {len(catalog)}")
    print(f"standard notes:  {len(notes)}")
    print(f"Markdown files:  {sum(1 for p in ROOT.rglob('*.md') if '.git' not in p.parts)}")
    if RAG_INDEX.exists():
        index = json.loads(RAG_INDEX.read_text(encoding="utf-8"))
        print(f"RAG index:       {index.get('chunks')} chunks / {index.get('files')} files "
              f"({index.get('model')})")
    else:
        print("RAG index:       not built (run tools/build-index.py)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--show", action="store_true", help="print effective config and live stats")
    args = parser.parse_args()
    if args.show:
        show()
    else:
        parser.print_help()
