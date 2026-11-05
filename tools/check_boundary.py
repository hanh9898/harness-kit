#!/usr/bin/env python3
"""Keep kit boundaries: report forbidden project-specific tokens in kit files.

  check_boundary.py [--root DIR] [--tokens FILE] [--strict]

Scan text files under --root (default: the repo's kit/ directory), excluding tests/ directories.
--tokens selects the forbidden list; default: boundary-tokens.txt at the repo root, outside kit/.
Each line is literal text or a regex prefixed with re:; inline comments follow whitespace and #.
# starts a comment. Report file:line, token and fix guidance. Defaults to warnings with exit 0;
--strict exits 1 for violations; exit 2 means the token list is unreadable. Uses only the standard library.
"""
import argparse
import re
import sys
from pathlib import Path

TOKENS_NAME = "boundary-tokens.txt"
SKIP_DIRS = {"tests", "__pycache__", ".pytest_cache", ".git"}


def load_tokens(path):
    """Return (label, compiled regex, note) entries from the token file."""
    out = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = re.search(r"\s+#\s", line)
        body, note = (line[: m.start()], line[m.end():]) if m else (line, "")
        body = body.strip()
        pattern = re.compile(body[3:]) if body.startswith("re:") else re.compile(re.escape(body))
        out.append((body, pattern, note.strip()))
    return out


def scan(root, tokens):
    hits = []
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root)
        if not p.is_file() or rel.name == TOKENS_NAME:
            continue
        if SKIP_DIRS & set(rel.parts[:-1]):
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for n, line in enumerate(text.splitlines(), 1):
            for label, pat, note in tokens:
                if pat.search(line):
                    hits.append((rel.as_posix(), n, label, note))
    return hits


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    REPO = Path(__file__).resolve().parent.parent
    ap.add_argument("--root", default=str(REPO / "kit"))
    ap.add_argument("--tokens", help=f"forbidden token file; default: {TOKENS_NAME} at the repo root")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args(argv)

    root = Path(a.root)
    tokens_file = Path(a.tokens) if a.tokens else REPO / TOKENS_NAME
    try:
        tokens = load_tokens(tokens_file)
    except (OSError, UnicodeDecodeError, re.error) as e:
        print(f"ERROR: cannot read forbidden token list {tokens_file} ({e}).\n"
              f"fix: create or repair {TOKENS_NAME}, or pass --tokens <file>.", file=sys.stderr)
        return 2
    hits = scan(root, tokens)
    for rel, n, label, note in hits:
        why = f" ({note})" if note else ""
        print(f"WARNING: {rel}:{n}: forbidden token `{label}`{why}\n"
              f"  fix: remove the token or use a neutral example; move project-specific content into that project's documentation.")
    print(f"{len(hits)} boundary violations." if hits else "Boundary clean.")
    return 1 if (a.strict and hits) else 0


if __name__ == "__main__":
    sys.exit(main())
