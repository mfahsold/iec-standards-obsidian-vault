#!/usr/bin/env python3
"""Build the local RAG index for the vault using Ollama embeddings.

Output is gitignored: index/embeddings.json. Requires only the Python
standard library.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "index" / "embeddings.json"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
MIN_CONTENT = 50


def split_chunks(text: str) -> List[str]:
    chunks: List[str] = []
    current = ""
    # Split on blank-line separated paragraphs.
    for paragraph in re.split(r"\n\s*\n", text):
        para = paragraph.strip()
        if not para:
            continue
        if len(current) + len(para) + 2 > CHUNK_SIZE:
            if current.strip():
                chunks.append(current.strip())
            current = current[-CHUNK_OVERLAP:] + para
        else:
            current += ("\n\n" if current else "") + para
    if current.strip():
        chunks.append(current.strip())
    return [chunk for chunk in chunks if len(chunk) >= MIN_CONTENT]


def embed_batch(texts: List[str], url: str, model: str) -> List[List[float]]:
    payload = {"model": model, "input": texts}
    request = urllib.request.Request(
        f"{url}/api/embed",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        return json.load(response)["embeddings"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=os.environ.get("EMBED_MODEL", "nomic-embed-text"))
    parser.add_argument("--url", default=os.environ.get("OLLAMA_URL", "http://localhost:11434"))
    args = parser.parse_args()

    files = sorted(p for p in ROOT.rglob("*.md") if ".git" not in p.parts)
    if not files:
        print("No Markdown files found", file=sys.stderr)
        return 1

    documents: List[Dict[str, Any]] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        for number, chunk in enumerate(split_chunks(text)):
            documents.append({
                "id": f"{path.relative_to(ROOT)}_{number}",
                "content": chunk,
                "metadata": {
                    "source": str(path.relative_to(ROOT)),
                    "fileName": path.stem,
                    "chunk": number,
                },
            })

    vectors: List[List[float]] = []
    batch_size = 32
    for start in range(0, len(documents), batch_size):
        batch = documents[start:start + batch_size]
        vectors.extend(embed_batch([item["content"] for item in batch],
                                   args.url.rstrip("/"), args.model))

    for document, vector in zip(documents, vectors):
        document["vector"] = vector

    OUTPUT.write_text(json.dumps({
        "model": args.model,
        "files": len(files),
        "chunks": len(documents),
        "embeddings": documents,
    }, ensure_ascii=False), encoding="utf-8")
    print(f"Indexed {len(documents)} chunks from {len(files)} files -> {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
