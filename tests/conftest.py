import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KIT = ROOT / "kit"
KIT_CLI = KIT / "scripts" / "kit"
CHECK_KIT = ROOT / "tools" / "check_kit.py"
CHECK_BOUNDARY = ROOT / "tools" / "check_boundary.py"
TOKENS = ROOT / "boundary-tokens.txt"
COLUMNS = ["id", "group", "name", "summary", "needed_when", "rung", "certainty", "sources", "detail"]


def run(script, *args):
    return subprocess.run([sys.executable, "-I", str(script), *map(str, args)], capture_output=True, text=True)


def write_kit(root, rows, header=COLUMNS, groups=None):
    """Build a possibly invalid sample kit with legos.csv from dict rows and groups.csv
    (used groups default to names of the form `Group <id>`)."""
    root.mkdir(parents=True, exist_ok=True)
    if groups is None:
        groups = {r.get("group", ""): f"Group {r.get('group', '')}" for r in rows}
    (root / "groups.csv").write_text("id,name\n" + "".join(f"{g},{n}\n" for g, n in groups.items()), encoding="utf-8")
    with (root / "legos.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            w.writerow([r.get(c, "") for c in header])
    return root


def write_piece_aliases(root, *pairs):
    with (root / "piece-aliases.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["legacy_id", "slug"])
        writer.writerows(pairs)


def row(id, group="A", name=None, rung="instruction-file", **kw):
    base = dict(id=id, group=group, name=name or f"Piece {id}", summary=f"Summary {id}",
                needed_when=f"When {id}", rung=rung, certainty="high", sources="https://example.com", detail=f"Detail {id}")
    base.update(kw)
    return base
