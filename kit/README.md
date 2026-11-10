# Kit

Resource library for designing, building, and reviewing an agent harness. It includes pieces, rules, team patterns, delegation guidance, and source-backed guides and workflows. The retrieval CLI is read-only.

## Discover by topic

Start with the five topic families, descend into one subcategory, then inspect one resource:

```
scripts/kit browse
scripts/kit browse 01
scripts/kit browse 1.3
scripts/kit inspect lego:A04
```

`categories.csv` defines the topic hierarchy. `catalog.csv` assigns each resource to one primary subcategory with a classification rationale. A resource's exact key is `kind:id`, so a category such as `1.1` cannot be confused with a rule identifier. Source group and topic labels remain resource metadata; the browse hierarchy comes from the catalog.

Browse lists bounded summaries. Inspect prints one resource's fields, sources, and classification. Classification does not increase source certainty or prove that a host supports the resource. Topic families describe concerns shared across agent environments.

## Source and verification

Retained resources keep their identifiers unless the identifier itself names a product-specific recipe. `resources.json` holds guides and workflows with explicit applicability, prerequisites, instructions, standards, verification steps, sources, and capability scope. `checked_on` records a documentation check; verification steps describe work to perform, not successful runtime results. A synthesized workflow is marked `inferred` even when its individual source facts are directly documented.

## Host-independent guidance

Normative content states a concrete behavior, its conditions, and the evidence needed to check it. Capability-dependent resources require checking that capability in the actual environment. Product-specific command names, configuration keys, fixed limits, and incidental implementation behavior belong to the environment's current documentation. Remove a resource when stripping those details leaves no useful guidance beyond another resource.

Source URLs and source labels retain their provenance, including product names. They do not turn a source's implementation detail into a universal requirement. Generalizations from a product-specific source are marked `inferred` (or retain a weaker evidence status); a changed rule loses any gate claim that its previous exact quotation supported.

Use applicable resources before forming interview suggestions, carry their guidance into implementation, and supply their standards to review. When a resource is incomplete or unsupported for the current host, expose the gap rather than treating its presence as proof.

Edit each resource in its source file and update its catalog assignment when its primary topic changes. Content is not copied into the catalog. The maintained core catalog is checked with `python3 tools/check_kit.py` from the repository root. This validator is not a personal-resource approval workflow.

## Vocabulary

- **Lego**: one row of `legos.csv`.
- **Rule**: one row of `rules.csv`, a checkable instruction with its source.
- **Pattern**: one row of the table in `patterns.md`, a way to shape a team of agents.
- **Rung**: how heavy a piece is. One of `instruction-file | skill | script-cli | mcp`, lightest first. The values are the English forms of the four rungs: instruction file, skill, script or CLI, MCP.
- **Certainty**: how well sources support a row. One of `stated | inferred | open | partial`.
  - `stated`: a source says it in so many words.
  - `inferred`: the research drew it from sources that do not say it directly.
  - `open`: not checked, or sources disagree.
  - `partial`: support comes from a source that was read only in part. A row with such a source is never marked higher than `partial`.
- **Verified on**: date a rule was last re-checked against its source. Empty until someone checks it.

In `sources`, `note:R24` means "research note 24", an internal note, not a link. `practice:` means the piece is supported only by observed use. In `rules.csv`, a bare source id such as `K08` is the id used in the research; most carry a link next to them.

## Source-specific lookups

```
scripts/kit list            # groups: letter, name, piece count
scripts/kit list A          # one line per piece in group A
scripts/kit show B01        # one piece in full, by id or exact name
scripts/kit list P          # team patterns, one line each; scripts/kit show P6 for one
scripts/kit list delegation # four axes and seven steps, one line each
scripts/kit show axis1      # one axis; step3 for one step; combine for how the axes combine
```

There is no command that prints the whole store. Rules also have focused commands: `kit list rules` (gate rules only), `kit list rules <topic>`, `kit show <rule id>` (for example `1.03`). An empty gate list means no current rule has the evidence required for that gate status; browse the applicable topics instead. Use taxonomy browsing when a need spans resource types.

## Where the data came from

A one-time script, `skills/harness/harness-evolve/scripts/generate_kit.py`, read the research reports and wrote the five data files. Numbers, ids, certainty and source links are parsed from the reports. The free text was Vietnamese, so it was translated by hand block by block into `skills/harness/harness-evolve/scripts/seed/`; the script stops if a seed block does not match a report id or count. Run it again only into an empty directory:

```
python3 skills/harness/harness-evolve/scripts/generate_kit.py --reports <reports dir> --dest <new dir>
```

It refuses to write if any output file already exists, so a hand-edited kit is never replaced.

## More

- Columns and rules for editing the CSV: [COLUMNS.md](COLUMNS.md)
- Checks (run from the repo root): `python3 -I tools/check_kit.py`, `python3 -I tools/check_boundary.py --strict`, `python3 -m pytest`
