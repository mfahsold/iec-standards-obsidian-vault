#!/usr/bin/env python3
"""Build the local RAG index for the vault using Ollama embeddings.

Chunks follow Markdown headings; each embedded chunk gets a deterministic
contextual header (document ref + heading path). Output is gitignored:
index/embeddings.json. Requires only the Python standard library.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path
from typing import Any, Dict, Iterator, List, Tuple

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "index" / "embeddings.json"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
MIN_CONTENT = 50

REF_RE = re.compile(r'^ref:\s*"?([^"\n]+)"?', re.M)
TITLE_RE = re.compile(r'^title:\s*"?([^"\n]+)"?', re.M)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


def iter_sections(text: str) -> Iterator[Tuple[str, str]]:
    """Yield (heading_path, section_text), split on Markdown headings."""
    stack: List[Tuple[int, str]] = []
    body: List[str] = []

    def emit() -> Tuple[str, str]:
        return "/".join(title for _, title in stack), "\n".join(body).strip()

    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if match:
            yield emit()
            level = len(match.group(1))
            stack = [(lv, title) for lv, title in stack if lv < level]
            stack.append((level, match.group(2).strip()))
            body = []
        else:
            body.append(line)
    yield emit()


def split_paragraphs(text: str) -> List[str]:
    chunks: List[str] = []
    current = ""
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


def chunks_for_file(path: Path) -> List[Dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    ref_match = REF_RE.search(text) or TITLE_RE.search(text)
    ref = ref_match.group(1).strip() if ref_match else path.stem
    result: List[Dict[str, Any]] = []
    for heading, section in iter_sections(text):
        for chunk in split_paragraphs(section):
            header = f"Document: {ref}\nSection: {heading or 'Overview'}\n\n"
            result.append({
                "content": header + chunk,
                "display": chunk,
                "metadata": {
                    "source": str(path.relative_to(ROOT)),
                    "fileName": path.stem,
                    "ref": ref,
                    "heading": heading,
                    "chunk": len(result),
                },
            })
    for number, item in enumerate(result):
        item["id"] = f"{item['metadata']['source']}_{number}"
        item["metadata"]["chunk"] = number
    return result


def embed_batch(texts: List[str], url: str, model: str) -> List[List[float]]:
    if model.startswith("nomic-embed-text"):
        texts = [f"search_document: {text}" for text in texts]
    payload = {
        "model": model,
        "input": texts,
        "options": {"num_ctx": 8192},
        "keep_alive": "10m",
    }
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
    parser.add_argument("--output", default=os.environ.get("RAG_INDEX", str(OUTPUT)))
    args = parser.parse_args()
    output_path = Path(args.output)

    files = sorted(p for p in ROOT.rglob("*.md") if ".git" not in p.parts)
    if not files:
        print("No Markdown files found", file=sys.stderr)
        return 1

    documents: List[Dict[str, Any]] = []
    for path in files:
        documents.extend(chunks_for_file(path))

    vectors: List[List[float]] = []
    batch_size = 32
    for start in range(0, len(documents), batch_size):
        batch = documents[start:start + batch_size]
        vectors.extend(embed_batch([item["content"] for item in batch],
                                   args.url.rstrip("/"), args.model))

    for document, vector in zip(documents, vectors):
        document["vector"] = vector

    output_path.write_text(json.dumps({
        "model": args.model,
        "files": len(files),
        "chunks": len(documents),
        "embeddings": documents,
    }, ensure_ascii=False), encoding="utf-8")
    try:
        shown = output_path.relative_to(ROOT)
    except ValueError:
        shown = output_path
    print(f"Indexed {len(documents)} chunks from {len(files)} files -> {shown}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
