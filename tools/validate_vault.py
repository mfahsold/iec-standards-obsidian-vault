#!/usr/bin/env python3
"""Validate the vault's data, links, and public-safety rules.

Run from anywhere:

    python3 tools/validate_vault.py

Exit code 0 means no errors. Warnings do not fail the build.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple
from urllib.parse import unquote, urlparse

import config  # noqa: E402

ROOT = config.ROOT
STANDARDS_DIR = ROOT / "standards"
INDEX_JSON = ROOT / "index" / "index.json"
INDEX_MD = ROOT / "index" / "index.md"
CATALOG_MD = STANDARDS_DIR / "index-standards.md"

REQUIRED_NOTE_FIELDS = [
    "ref",
    "title",
    "type",
    "status",
    "languages",
    "price_chf",
    "sources",
    "tags",
]
REQUIRED_INDEX_FIELDS = [
    "ref",
    "title",
    "type",
    "status",
    "languages",
    "price_chf",
    "sources",
    "tags",
]
ALLOWED_STATUS = {"active", "replaced", "withdrawn", "draft", "superseded"}

TEXT_EXTENSIONS = {
    ".md",
    ".json",
    ".sh",
    ".py",
    ".yml",
    ".yaml",
    ".txt",
    ".cff",
    ".toml",
    ".ini",
    ".cfg",
}
SKIP_DIRS = {
    ".git",
    ".obsidian",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}

ABSOLUTE_PATH_PATTERNS = [
    re.compile(r"/Users/[A-Za-z0-9._-]+"),
    re.compile(r"/home/[A-Za-z0-9._-]+"),
    re.compile(r"[A-Za-z]:\\Users\\"),
    re.compile(r"file:///"),
]

SECRET_PATTERNS = [
    re.compile(r"(?:ghp_|github_pat_|gho_|ghu_|ghs_|ghr_)[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(
        r"(?i)\b(password|passwd|secret|api[_-]?key|access[_-]?token)\b"
        r"\s*[:=]\s*['\"]?[^\s'\"]{8,}"
    ),
]

errors: List[str] = []
warnings: List[str] = []


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def error(message: str) -> None:
    errors.append(message)


def warning(message: str) -> None:
    warnings.append(message)


def iter_files() -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [
            name
            for name in dirnames
            if name not in SKIP_DIRS and not name.startswith(".git")
        ]
        for filename in filenames:
            yield Path(dirpath) / filename


def iter_text_files() -> Iterable[Path]:
    for path in iter_files():
        if path.suffix.lower() in TEXT_EXTENSIONS or path.name in {
            "Makefile",
            ".gitignore",
            ".gitattributes",
            ".editorconfig",
        }:
            yield path


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "":
        return ""
    if value in {"null", "~"}:
        return None
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(item) for item in inner.split(",")]
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        quote = value[0]
        inner = value[1:-1]
        if quote == '"':
            inner = inner.replace('\\"', '"').replace("\\\\", "\\")
        return inner
    try:
        if re.fullmatch(r"-?\d+", value):
            return int(value)
        if re.fullmatch(r"-?\d+\.\d+", value):
            return float(value)
    except ValueError:
        pass
    return value


def parse_frontmatter(text: str) -> Tuple[Dict[str, Any], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    end: Optional[int] = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break
    if end is None:
        return {}, text

    data: Dict[str, Any] = {}
    current_key: Optional[str] = None
    for raw in lines[1:end]:
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        stripped = line.strip()
        if stripped.startswith("- "):
            if current_key is None:
                continue
            if not isinstance(data.get(current_key), list):
                data[current_key] = []
            data[current_key].append(parse_scalar(stripped[2:]))
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        current_key = key
        value = value.strip()
        if value == "":
            data[key] = []
        else:
            data[key] = parse_scalar(value)
    return data, "\n".join(lines[end + 1 :])


def strip_code_fences(text: str) -> str:
    output: List[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            output.append("")
            continue
        output.append("" if in_fence else line)
    # Inline code often contains link examples such as `[x](y)` or `[[Note]]`.
    return re.sub(r"`[^`\n]*`", "", "\n".join(output))


def load_json(path: Path) -> Any:
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        error(f"missing file: {rel(path)}")
    except json.JSONDecodeError as exc:
        error(f"invalid JSON in {rel(path)}: {exc}")
    return None


def check_json_files() -> None:
    for path in [INDEX_JSON, ROOT / "meta" / "tags.json", ROOT / "meta" / "hotkeys.json"]:
        if path.exists():
            load_json(path)


def standard_note_paths() -> List[Path]:
    return sorted(
        path
        for path in STANDARDS_DIR.glob("*.md")
        if path.name not in {"index-standards.md", "classics.md"}
    )


def note_key(frontmatter: Dict[str, Any]) -> str:
    return str(frontmatter.get("name") or frontmatter.get("ref") or "")


def check_notes() -> Tuple[List[Dict[str, Any]], List[Path]]:
    notes: List[Dict[str, Any]] = []
    paths = standard_note_paths()

    for path in paths:
        text = path.read_text(encoding="utf-8")
        frontmatter, _ = parse_frontmatter(text)
        if not frontmatter:
            error(f"{rel(path)}: missing YAML frontmatter")
            continue

        for field in REQUIRED_NOTE_FIELDS:
            if field not in frontmatter:
                error(f"{rel(path)}: missing required field '{field}'")
            elif frontmatter[field] in (None, "", []) and field not in {"price_chf"}:
                error(f"{rel(path)}: empty required field '{field}'")

        status = str(frontmatter.get("status", "")).lower()
        if status and status not in ALLOWED_STATUS:
            warning(f"{rel(path)}: unusual status '{status}'")

        price = frontmatter.get("price_chf")
        if price is not None and not isinstance(price, (int, float)):
            error(f"{rel(path)}: price_chf must be a number or null")

        sources = frontmatter.get("sources")
        if not isinstance(sources, list) or not sources:
            error(f"{rel(path)}: sources must be a non-empty list")
        else:
            for source in sources:
                parsed = urlparse(str(source))
                if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                    error(f"{rel(path)}: invalid source URL '{source}'")

        key = note_key(frontmatter)
        if not key:
            error(f"{rel(path)}: missing ref/name")
        notes.append(
            {
                "path": path,
                "frontmatter": frontmatter,
                "key": key,
            }
        )

    return notes, paths


def check_index(notes: List[Dict[str, Any]]) -> None:
    data = load_json(INDEX_JSON)
    if not isinstance(data, list):
        error("index/index.json must contain a JSON array")
        return

    index_by_key: Dict[str, Dict[str, Any]] = {}
    for position, entry in enumerate(data, start=1):
        if not isinstance(entry, dict):
            error(f"index/index.json entry {position} is not an object")
            continue
        for field in REQUIRED_INDEX_FIELDS:
            if field not in entry:
                error(f"index/index.json entry {position}: missing '{field}'")
        key = str(entry.get("name") or entry.get("ref") or "")
        if not key:
            error(f"index/index.json entry {position}: missing ref/name")
            continue
        if key in index_by_key:
            error(f"index/index.json: duplicate key '{key}'")
        index_by_key[key] = entry

        sources = entry.get("sources")
        if isinstance(sources, list):
            for source in sources:
                parsed = urlparse(str(source))
                if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                    error(
                        f"index/index.json entry '{key}': invalid source URL '{source}'"
                    )
        else:
            error(f"index/index.json entry '{key}': sources must be a list")

        status = str(entry.get("status", "")).lower()
        if status and status not in ALLOWED_STATUS:
            warning(f"index/index.json entry '{key}': unusual status '{status}'")

    note_by_key = {note["key"]: note for note in notes}
    for key, note in note_by_key.items():
        if key not in index_by_key:
            error(f"note '{key}' is missing from index/index.json")
            continue
        entry = index_by_key[key]
        frontmatter = note["frontmatter"]
        for field in ["title", "type", "price_chf", "ics", "published", "technical_committee"]:
            if field in entry and field in frontmatter:
                if str(entry[field]) != str(frontmatter[field]):
                    warning(
                        f"'{key}': field '{field}' differs between note and index "
                        f"({frontmatter[field]!r} vs {entry[field]!r})"
                    )

    for key in index_by_key:
        if key not in note_by_key:
            error(f"index/index.json entry '{key}' has no matching note")


def check_catalog_coverage(notes: List[Dict[str, Any]]) -> None:
    for path in [INDEX_MD, CATALOG_MD]:
        if not path.exists():
            error(f"missing file: {rel(path)}")
            continue
        text = path.read_text(encoding="utf-8")
        for note in notes:
            stem = note["path"].stem
            ref = str(note["frontmatter"].get("ref", ""))
            if stem not in text and ref not in text:
                error(f"{rel(path)}: missing catalog entry for '{stem}'")


def build_stem_map() -> Dict[str, List[Path]]:
    mapping: Dict[str, List[Path]] = {}
    for path in iter_files():
        if path.suffix.lower() != ".md" and path.name not in {"LICENSE"}:
            continue
        mapping.setdefault(path.stem.lower(), []).append(path)
    return mapping


def resolve_markdown_target(source: Path, target: str) -> Optional[Path]:
    target = target.strip()
    if not target or target.startswith("#"):
        return None
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    parsed = urlparse(target)
    if parsed.scheme or target.startswith("//"):
        return None
    target = unquote(target.split("#", 1)[0].split("?", 1)[0])
    if not target:
        return None
    candidates: List[Path] = []
    if target.startswith("/"):
        candidates.append(ROOT / target.lstrip("/"))
    else:
        candidates.append(source.parent / target)
        # Obsidian users often write vault-root-relative markdown links
        # without a leading slash (e.g. "meta/licensing.md" from index/).
        candidates.append(ROOT / target)
    for candidate in candidates:
        candidate = Path(os.path.normpath(str(candidate)))
        for option in [candidate, Path(str(candidate) + ".md")]:
            if option.exists():
                return option
    return None


def resolve_wikilink(target: str, stem_map: Dict[str, List[Path]]) -> Optional[Path]:
    target = target.split("|", 1)[0].split("#", 1)[0].strip()
    if not target:
        return None
    if target.startswith("/"):
        candidate = ROOT / target.lstrip("/")
        if candidate.exists():
            return candidate
        if Path(str(candidate) + ".md").exists():
            return Path(str(candidate) + ".md")
        return None
    if "/" in target:
        candidate = ROOT / target
        if candidate.exists():
            return candidate
        if Path(str(candidate) + ".md").exists():
            return Path(str(candidate) + ".md")
        return None
    matches = stem_map.get(Path(target).stem.lower(), [])
    if matches:
        return matches[0]
    candidate = ROOT / target
    if candidate.exists():
        return candidate
    return None


def check_links() -> None:
    stem_map = build_stem_map()
    markdown_link = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    wikilink = re.compile(r"\[\[([^\]]+)\]\]")
    incoming: Dict[str, Set[str]] = {}

    for path in iter_files():
        if path.suffix.lower() != ".md":
            continue
        text = strip_code_fences(path.read_text(encoding="utf-8"))
        for match in markdown_link.finditer(text):
            target = match.group(1).strip()
            if target.startswith(("http://", "https://", "mailto:", "tel:", "data:")):
                continue
            if target.startswith("#"):
                continue
            resolved = resolve_markdown_target(path, target)
            if resolved is None:
                warning(f"{rel(path)}: broken markdown link '{target}'")
            else:
                incoming.setdefault(str(resolved), set()).add(str(path))

        for match in wikilink.finditer(text):
            target = match.group(1).strip()
            resolved = resolve_wikilink(target, stem_map)
            if resolved is None:
                warning(f"{rel(path)}: unresolved wikilink '[[{target}]]'")
            else:
                incoming.setdefault(str(resolved), set()).add(str(path))

    for path in standard_note_paths():
        sources = incoming.get(str(path), set()) - {str(path)}
        if not sources:
            warning(f"{rel(path)}: no incoming links (orphan note)")


def check_public_safety() -> None:
    for path in iter_files():
        if path.name == "embeddings.json":
            continue
        if path.suffix.lower() == ".pdf":
            error(f"PDF found in repository: {rel(path)}")
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS and path.name not in {
            "Makefile",
            ".gitignore",
            ".gitattributes",
            ".editorconfig",
        }:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        for pattern in ABSOLUTE_PATH_PATTERNS:
            # The validator itself contains the patterns it searches for.
            if path.name == "validate_vault.py":
                continue
            if pattern.search(text):
                error(f"{rel(path)}: absolute/local path detected ({pattern.pattern})")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                error(f"{rel(path)}: possible secret detected ({pattern.pattern})")


def check_block_quotes() -> None:
    for path in iter_files():
        if path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        block: List[str] = []
        start_line = 0

        def flush() -> None:
            nonlocal block, start_line
            if not block:
                return
            words = len(" ".join(block).split())
            if words > config.BLOCK_QUOTE_ERROR:
                error(
                    f"{rel(path)}:{start_line}: block quote has {words} words "
                    f"(limit {config.BLOCK_QUOTE_ERROR}; paraphrase or shorten)"
                )
            elif words > config.BLOCK_QUOTE_WARN:
                warning(
                    f"{rel(path)}:{start_line}: long block quote ({words} words; "
                    f"target <= {config.BLOCK_QUOTE_TARGET})"
                )
            block = []
            start_line = 0

        for number, line in enumerate(text.splitlines(), start=1):
            if line.lstrip().startswith(">"):
                if not block:
                    start_line = number
                block.append(line.lstrip()[1:].strip())
            else:
                flush()
        flush()


def main() -> int:
    print("== Vault validation ==")
    print(f"root: {ROOT}")
    print(f"files: {sum(1 for _ in iter_files())}")

    check_json_files()
    notes, paths = check_notes()
    print(f"standard notes: {len(paths)}")
    check_index(notes)
    check_catalog_coverage(notes)
    check_links()
    check_public_safety()
    check_block_quotes()

    for message in warnings:
        print(f"[WARN] {message}")
    for message in errors:
        print(f"[ERROR] {message}")

    print(f"\nSummary: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
