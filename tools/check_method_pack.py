#!/usr/bin/env python3
"""Check the released verification method pack and its core catalog overlay."""

import argparse
import csv
import json
import shutil
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True
sys.path[:0] = [str(ROOT / "kit/scripts"), str(ROOT / "tools")]
import check_boundary
import check_kit
import method_pack

RELEASE_IDS = {"opt-blind-comparison", "opt-shared-premise-probe", "opt-formal-model-resync"}
PROVENANCE_ALLOWLIST_SHA256 = "1234be6f9c7af8264fb24a93d37839dd0fbea0303936ead0eac7cfc2cf38b1c1"


def check_overlay(index, catalog, overlay):
    overlay.mkdir()
    core_ids = set()
    piece_fields = ()
    for name, keys in (("legos.csv", ["id"]), ("rules.csv", ["id"]),
                       ("piece-aliases.csv", ["legacy_id", "slug"]), ("groups.csv", []), ("gates.csv", [])):
        shutil.copyfile(catalog / name, overlay / name)
        with (overlay / name).open(encoding="utf-8", newline="") as stream:
            reader = csv.DictReader(stream, strict=True)
            header = reader.fieldnames or ()
            if len(header) != len(set(header)):
                raise ValueError(f"{name}:1: duplicate columns in catalog header.")
            if name == "legos.csv":
                piece_fields = header
            if keys:
                for row in reader:
                    core_ids.update(row[key] for key in keys)
    method_pack.require_disjoint(index, core_ids)
    pieces = overlay / "legos.csv"
    needs_newline = not pieces.read_bytes().endswith((b"\r", b"\n"))
    with pieces.open("a", encoding="utf-8", newline="") as stream:
        if needs_newline:
            stream.write("\n")
        writer = csv.DictWriter(stream, fieldnames=piece_fields)
        for identity, item in index["items"].items():
            writer.writerow(method_pack.catalog_row(identity, item))
    return check_kit.main(["--dir", str(overlay)])


def decoded_index_lines(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from decoded_index_lines(child)
    elif isinstance(value, list):
        for child in value:
            yield from decoded_index_lines(child)
    else:
        yield str(value)


def check_pack(pack, catalog):
    expected = {"index.json", "LICENSE", "guidance"} | {f"guidance/{i}.md" for i in RELEASE_IDS}
    entries = {path.relative_to(pack).as_posix(): path for path in pack.rglob("*")}
    if entries.keys() != expected or any(path.is_symlink() for path in entries.values()):
        raise ValueError("Pack files differ from the released file whitelist, or include symbolic links.")
    index = method_pack.read_index(pack)
    if index["items"].keys() != RELEASE_IDS:
        raise ValueError("The index must contain exactly the three released method IDs.")
    provenance = {identity: item["provenance"] for identity, item in index["items"].items()}
    encoded = json.dumps(provenance, sort_keys=True, separators=(",", ":")).encode()
    if method_pack.digest(encoded) != PROVENANCE_ALLOWLIST_SHA256:
        raise ValueError("The source URLs differ from the reviewed provenance allowlist.")

    with TemporaryDirectory(prefix="library-method-pack-") as directory:
        scratch = Path(directory)
        scan = scratch / "boundary"
        (scan / "guidance").mkdir(parents=True)
        license_text = method_pack.pack_file(pack, "LICENSE").decode("utf-8")
        (scan / "LICENSE").write_text(license_text, encoding="utf-8")
        for identity, item in index["items"].items():
            body = method_pack.read_body(pack, identity, item)
            (scan / "guidance" / f"{identity}.md").write_text(body, encoding="utf-8")
            del item["provenance"]["url"]
        (scan / "index.fields").write_text("\n".join(decoded_index_lines(index)), encoding="utf-8")
        if check_boundary.main(["--strict", "--root", str(scan)]):
            return 1
        return check_overlay(index, catalog, scratch / "catalog")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pack", type=Path, default=ROOT / "packs/verification-methods")
    parser.add_argument("--kit-dir", type=Path, default=ROOT / "kit")
    args = parser.parse_args()
    try:
        return check_pack(args.pack.resolve(strict=True), args.kit_dir)
    except (OSError, ValueError, RuntimeError, csv.Error, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
