"""Canonical identifiers for supplied pieces; older catalogs have no legacy_id column."""

import re


SLUG = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*")
LEGACY_ID = re.compile(r"[A-Z][0-9]{2}")
MARKDOWN_SELECTOR = re.compile(r"combine|(?:p|axis|step)[0-9]+")


class PieceAliases:
    def __init__(self, entries=(), rule_ids=()):
        self.by_legacy = {}
        self.by_slug = {}
        reserved = {identity.lower() for identity in rule_ids if identity}
        seen = {}
        for line, row in entries:
            if "legacy_id" not in row:
                continue
            slug, legacy = row.get("id") or "", row["legacy_id"]
            if (not SLUG.fullmatch(slug) or MARKDOWN_SELECTOR.fullmatch(slug)
                    or LEGACY_ID.fullmatch(slug.upper()) or slug in reserved):
                raise ValueError(f"legos.csv:{line}: invalid or reserved piece slug `{slug}`; choose a descriptive ID")
            if slug in seen:
                raise ValueError(f"legos.csv:{line}: duplicate piece slug `{slug}` from line {seen[slug]}; keep one row per ID")
            seen[slug] = line
            if legacy == "":
                continue
            if not legacy or not LEGACY_ID.fullmatch(legacy) or legacy.lower() in reserved:
                raise ValueError(f"legos.csv:{line}: invalid or reserved legacy_id `{legacy}`; use a former piece ID or leave blank")
            if legacy in self.by_legacy:
                raise ValueError(f"legos.csv:{line}: duplicate legacy_id `{legacy}`; map it to only one slug")
            self.by_legacy[legacy] = slug
            self.by_slug[slug] = legacy

    def canonical(self, identity):
        return self.by_legacy.get(identity.upper(), identity)


def public_piece(row):
    return {key: value for key, value in row.items() if key != "legacy_id"}
