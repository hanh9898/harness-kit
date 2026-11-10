#!/usr/bin/env python3
"""Check repository text, commit messages, and pull-request metadata for language violations.

English prose is a review requirement. This deterministic check detects accented
Vietnamese text, including decomposed Unicode; it cannot classify unaccented prose.
Escaped code points in source-format adapters and test data remain valid ASCII.
"""
import argparse
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

FORBIDDEN = re.compile(
    "[\u00c0-\u00c3\u00c8-\u00ca\u00cc-\u00cd\u00d2-\u00d5\u00d9-\u00da\u00dd"
    "\u00e0-\u00e3\u00e8-\u00ea\u00ec-\u00ed\u00f2-\u00f5\u00f9-\u00fa\u00fd"
    "\u0102\u0103\u0110\u0111\u0128\u0129\u0168\u0169\u01a0\u01a1\u01af\u01b0\u1ea0-\u1ef9]"
)


def violations(text, label):
    """Report locations without printing potentially sensitive source contents."""
    return [f"{label}:{line_no}: use English text"
            for line_no, line in enumerate(text.splitlines(), 1)
            if FORBIDDEN.search(unicodedata.normalize("NFC", line))]


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.PIPE)


def text_violations(data, label):
    try:
        return violations(data.decode("utf-8"), label)
    except UnicodeDecodeError:
        return []  # Binary assets are not prose.


def check_files(root, staged=False):
    names = git(root, "ls-files", "-z").decode("utf-8").split("\0")
    errors = []
    for name in filter(None, names):
        errors += violations(name, "tracked path")
        if staged:
            data = git(root, "show", f":{name}")
        else:
            path = root / name
            if not path.exists():
                continue  # A working-tree deletion carries no new text.
            data = path.read_bytes()
        errors += text_violations(data, name)
    return errors


def check_commits(root, revision):
    errors = []
    for sha in git(root, "rev-list", revision).decode().splitlines():
        errors += text_violations(git(root, "show", "-s", "--format=%B", sha), f"commit {sha[:12]}")
    return errors


def check_history(root, revision):
    errors = []
    for entry in git(root, "rev-list", "--objects", revision).decode().splitlines():
        sha, _, name = entry.partition(" ")
        if not name:
            continue
        errors += violations(name, f"historical path {sha[:12]}")
        if git(root, "cat-file", "-t", sha).strip() == b"blob":
            errors += text_violations(git(root, "cat-file", "blob", sha), f"blob {sha[:12]} {name}")
    return errors


def check_event(path):
    event = json.loads(path.read_text(encoding="utf-8"))
    errors = []
    for kind in ("pull_request", "issue", "comment", "review"):
        for field in ("title", "body"):
            value = event.get(kind, {}).get(field)
            if value:
                errors += violations(value, f"{kind}.{field}")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--staged", action="store_true", help="read indexed contents instead of working files")
    parser.add_argument("--commits", action="store_true", help="also check reachable commit messages")
    parser.add_argument("--history", action="store_true", help="also check reachable historical file contents")
    parser.add_argument("--all-refs", action="store_true", help="check every ref, not just HEAD")
    parser.add_argument("--message-file", type=Path, help="check only a commit-message file")
    parser.add_argument("--event-file", type=Path, help="also check GitHub event metadata")
    args = parser.parse_args(argv)
    try:
        if args.message_file:
            errors = violations(args.message_file.read_text(encoding="utf-8"), "commit message")
        else:
            errors = check_files(args.root, args.staged)
            revision = "--all" if args.all_refs else "HEAD"
            if args.commits:
                errors += check_commits(args.root, revision)
            if args.history:
                errors += check_history(args.root, revision)
        if args.event_file:
            errors += check_event(args.event_file)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"ERROR: cannot complete English checks: {error}", file=sys.stderr)
        return 2
    for error in errors:
        print(error, file=sys.stderr)
    print(f"English check: {len(errors)} violations." if errors else "English check passed.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
