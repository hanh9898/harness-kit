# Resync a formal model to covered code

For each property, identify the last synchronized commit and the implementation
paths that can change its modeled state. Diff from that commit, including moved
code and new state writers. Separate irrelevant changes, intended contract
changes, model drift, and possible code bugs. Align model transitions with
atomic implementation steps. Advance the sync reference only after checking the
correspondence and rerunning the property. Do not weaken the property to pass.
