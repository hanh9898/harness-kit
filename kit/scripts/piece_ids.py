"""Canonical identifiers for supplied pieces and retired aliases."""

import csv
import re


SLUG = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*")
LEGACY_ID = re.compile(r"[A-Z][0-9]{2}")
MARKDOWN_SELECTOR = re.compile(r"combine|(?:p|axis|step)[0-9]+")
ALIAS_FILE = "piece-aliases.csv"


class PieceAliases:
    def __init__(self):
        self.by_legacy = {}
        self.by_slug = {}

    @classmethod
    def load(cls, kit_dir, entries, rule_ids):
        aliases = cls()
        try:
            stream = (kit_dir / ALIAS_FILE).open(encoding="utf-8", newline="")
        except FileNotFoundError:
            return aliases

        reserved = {identity.lower() for identity in rule_ids if identity}
        with stream:
            reader = csv.DictReader(stream, strict=True)
            try:
                if reader.fieldnames != ["legacy_id", "slug"]:
                    raise ValueError(f"{ALIAS_FILE}:1: expected columns legacy_id,slug")
                for row in reader:
                    slug, legacy = row["slug"] or "", row["legacy_id"] or ""
                    location = f"{ALIAS_FILE}:{reader.line_num}"
                    if None in row:
                        raise ValueError(f"{location}: extra cells; use one legacy_id,slug pair")
                    validate_slug(slug, reserved, location)
                    if not LEGACY_ID.fullmatch(legacy) or reserved_selector(legacy.lower(), reserved):
                        raise ValueError(f"{location}: invalid or reserved legacy_id `{legacy}`")
                    if legacy in aliases.by_legacy:
                        raise ValueError(f"{location}: duplicate legacy_id `{legacy}`; map it to only one slug")
                    if slug in aliases.by_slug:
                        raise ValueError(f"{location}: duplicate alias target `{slug}`; keep one legacy ID per slug")
                    aliases.by_legacy[legacy] = slug
                    aliases.by_slug[slug] = legacy
            except csv.Error as e:
                raise ValueError(f"{ALIAS_FILE}:{reader.reader.line_num}: malformed CSV ({e})") from e

        seen = {}
        for line, row in entries:
            slug = row.get("id") or ""
            validate_slug(slug, reserved, f"legos.csv:{line}")
            if slug in seen:
                raise ValueError(f"legos.csv:{line}: duplicate piece slug `{slug}` from line {seen[slug]}; keep one row per ID")
            seen[slug] = line
        return aliases

    def canonical(self, identity):
        return self.by_legacy.get(identity.upper(), identity)


def reserved_selector(identity, rule_ids):
    return identity in rule_ids or MARKDOWN_SELECTOR.fullmatch(identity) is not None


def validate_slug(slug, reserved, location):
    if (not SLUG.fullmatch(slug) or LEGACY_ID.fullmatch(slug.upper())
            or reserved_selector(slug, reserved)):
        raise ValueError(f"{location}: invalid or reserved piece slug `{slug}`; choose a descriptive ID")
