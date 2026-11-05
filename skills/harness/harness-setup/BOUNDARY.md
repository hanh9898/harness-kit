# Boundary: three questions, two labels

Classify every item the flow turned up (tool, document, data, role, script). Two labels only:

- `shared`: names nothing about this project; works unchanged in another project.
- `project`: carries this project's name, data, paths, tools or roles. Business documents, data snapshots and tools that process them are `project` harness too.

Put these to the user in order, one per turn, for the items not yet settled; stop at the first answer that settles each item. A suggested label is a proposal until the user answers.

1. **Own names or values?** Project name, machine path, entry from a project log, project-only tool or role. Yes: `project`.
2. **Delete test.** Carry it into another project: still true and still runs? Yes: `shared`.
3. **Direction.** Does the `shared` part point back at the project? Yes: the dependency is upside down. Move the pointer into the `project` side, or split the item.

Where people can see the item (its visibility) is a note on the item, never a third label.

A `shared` tool stays under `harness/tools/` and the record notes it as a candidate for the kit; kit changes go through a change to the plugin.
