"""Validate and read the optional Library method pack and its consumer binding."""

import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from stat import S_ISREG


CORE_FILES = ("legos.csv", "rules.csv", "piece-aliases.csv")
NODE = "Verification & feedback"
FACTS = ("compare-variants", "subjective-grading", "fully-objective",
         "repeated-same-gate", "shared-assumption", "formal-model-exists", "covered-code-changed")
SLUG = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*")
SHA256 = re.compile(r"[0-9a-f]{64}")
SOURCE = re.compile(
    r"https://github\.com/[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9_][A-Za-z0-9_.-]*"
    r"/blob/[0-9a-f]{40}(?:/[A-Za-z0-9_][A-Za-z0-9_.-]*)+"
)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Ambiguous duplicate JSON field: {key}.")
        result[key] = value
    return result


def digest(data):
    return hashlib.sha256(data).hexdigest()


def fields(value, names, label):
    if not isinstance(value, dict) or value.keys() != set(names.split()):
        raise ValueError(f"{label} must have exactly these fields: {names}.")


def matches(pattern, value):
    return isinstance(value, str) and pattern.fullmatch(value) is not None


def one_line(value):
    return isinstance(value, str) and bool(value.strip()) and value.splitlines() == [value]


def require_schema(value, names, label):
    fields(value, f"schema {names}", label)
    if type(value["schema"]) is not int or value["schema"] != 1:
        raise ValueError(f"Unsupported {label} schema.")


def require_list(value, allowed, label, *, nonempty=False):
    if (not isinstance(value, list) or (nonempty and not value)
            or any(not isinstance(x, str) or x not in allowed for x in value)
            or len(set(value)) != len(value)):
        raise ValueError(f"{label} must be a list of distinct supported values.")


def read_regular(path):
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
    with os.fdopen(fd, "rb") as stream:
        if not S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise ValueError(f"Expected a regular file: {path}.")
        return stream.read()


def pack_file(root, relative):
    path = root / relative
    if path.resolve(strict=True) != path:
        raise ValueError(f"Pack entries must not be symbolic links: {relative}.")
    return read_regular(path)


def read_index(root, expected=None):
    raw = pack_file(root, "index.json")
    if expected is not None and digest(raw) != expected:
        raise ValueError("Pinned method pack index digest does not match.")
    index = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object)
    require_schema(index, "items scenarios", "method index")
    items, scenarios = index["items"], index["scenarios"]
    if not isinstance(items, dict) or not items or not isinstance(scenarios, dict) or not scenarios:
        raise ValueError("The method index needs items and scenarios keyed by stable IDs.")
    for identity, item in items.items():
        if not identity.startswith("opt-") or not matches(SLUG, identity):
            raise ValueError(f"Invalid method ID: {identity}.")
        fields(item, "name summary needed_when kind node all none body_sha256 provenance", identity)
        if (not all(one_line(item[k]) for k in ("name", "summary", "needed_when"))
                or item["kind"] not in ("playbook", "principle") or item["node"] != NODE
                or not matches(SHA256, item["body_sha256"])):
            raise ValueError(f"Invalid method metadata: {identity}.")
        require_list(item["all"], FACTS, f"{identity}.all", nonempty=True)
        require_list(item["none"], FACTS, f"{identity}.none")
        if set(item["all"]).intersection(item["none"]):
            raise ValueError(f"Conflicting predicates: {identity}.")
        provenance = item["provenance"]
        fields(provenance, "url license", f"{identity}.provenance")
        if provenance["license"] != "MIT" or not matches(SOURCE, provenance["url"]):
            raise ValueError(f"Invalid pinned provenance: {identity}.")
    covered = set()
    for identity, scenario in scenarios.items():
        fields(scenario, "name ids", identity)
        if not matches(SLUG, identity) or not one_line(scenario["name"]):
            raise ValueError(f"Invalid scenario metadata: {identity}.")
        require_list(scenario["ids"], items, f"{identity}.ids", nonempty=True)
        covered.update(scenario["ids"])
    if covered != set(items):
        raise ValueError("Every method must belong to a scenario.")
    return index


def read_body(root, identity, item):
    content = pack_file(root, f"guidance/{identity}.md")
    if digest(content) != item["body_sha256"]:
        raise ValueError(f"Pinned method body digest does not match: {identity}.")
    return content.decode("utf-8")


def canonical_path(value):
    if isinstance(value, str):
        path = Path(value)
        if path.is_absolute() and str(path.resolve()) == value:
            return path
    raise ValueError("Binding paths must be absolute and canonical.")


@dataclass(frozen=True)
class Binding:
    store: Path
    device: int
    inode: int
    owner: str
    scope: str
    catalog: Path
    pack: Path
    files: dict
    index_sha256: str
    binding_sha256: str

    def target_matches(self, path, stat):
        return path == self.store and (stat.st_dev, stat.st_ino) == (self.device, self.inode)

    def require_scope(self, record):
        if (record["owner"], record["scope"]) != (self.owner, self.scope):
            raise ValueError("Method selection owner or scope does not match the Library binding.")

    def core_bytes(self):
        files = {name: read_regular(self.catalog / name) for name in CORE_FILES}
        if any(digest(raw) != self.files[name] for name, raw in files.items()):
            raise ValueError("Pinned core catalog digest does not match.")
        return files


def read_binding(path):
    raw = read_regular(path)
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object)
    require_schema(value, "owner scope store catalog pack", "method binding")
    store, catalog, pack = value["store"], value["catalog"], value["pack"]
    fields(store, "path device inode", "store")
    fields(catalog, "path files", "catalog")
    fields(catalog["files"], " ".join(CORE_FILES), "catalog.files")
    fields(pack, "path index_sha256", "pack")
    scope = value["scope"]
    if (not one_line(value["owner"]) or not one_line(scope) or
            (scope != "personal" and not (scope.startswith("project:") and Path(scope[8:]).is_absolute()))):
        raise ValueError("The method binding requires an owner and a Library scope.")
    if (type(store["device"]) is not int or store["device"] < 0
            or type(store["inode"]) is not int or store["inode"] < 1):
        raise ValueError("The method binding requires the store device and inode.")
    if (not matches(SHA256, pack["index_sha256"])
            or any(not matches(SHA256, pin) for pin in catalog["files"].values())):
        raise ValueError("Method pack and catalog pins must be lowercase SHA-256 digests.")
    return Binding(canonical_path(store["path"]), store["device"], store["inode"], value["owner"], scope,
                   canonical_path(catalog["path"]), canonical_path(pack["path"]), catalog["files"],
                   pack["index_sha256"], digest(raw))


def require_disjoint(index, core_ids):
    collisions = {i.casefold() for i in core_ids}.intersection(index["items"])
    if collisions:
        raise ValueError("Method IDs collide with core catalog IDs: " + ", ".join(sorted(collisions)))


def catalog_row(identity, item):
    return dict(id=identity, group="H", name=item["name"], summary=item["summary"],
                needed_when=item["needed_when"], rung="instruction-file", certainty="stated",
                sources=f"index.json#{identity}", detail=f"guidance/{identity}.md")
