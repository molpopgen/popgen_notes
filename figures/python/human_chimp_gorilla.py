import tskit

tables = tskit.TableCollection(1000.0)
human = tables.nodes.add_row(tskit.NODE_IS_SAMPLE, 0.0)
chimp = tables.nodes.add_row(tskit.NODE_IS_SAMPLE, 0.0)
gorilla = tables.nodes.add_row(tskit.NODE_IS_SAMPLE, 0.0)
hc_ca = tables.nodes.add_row(0, 6.0)
hgc_ca = tables.nodes.add_row(0, 12.0)
tables.time_units = "mya"

for child, parent in [
    (human, hc_ca),
    (chimp, hc_ca),
    (gorilla, hgc_ca),
    (hc_ca, hgc_ca),
]:
    tables.edges.add_row(
        child=child, parent=parent, left=0, right=tables.sequence_length
    )


tables.sort()

treeseq = tables.tree_sequence()
treeseq.draw_svg(
    "figures/human_chimp_gorilla.svg",
    size=(500, 500),
    node_labels={0: "Human", 1: "Chimp", 2: "Gorilla", 3: "H/C", 4: "H/C/G"},
    x_axis=False,
    y_axis=True,
)

style = [
    ".a3.n0 > .edge {stroke: cyan; stroke-width: 2px}",
    ".a3.n1 > .edge {stroke: red; stroke-width: 2px}",
    ".a4.n2 > .edge {stroke: purple; stroke-width: 2px}",
    ".a4.n3 > .edge {stroke: pink; stroke-width: 2px}",
]

treeseq.draw_svg(
    "figures/human_chimp_gorilla_colored_edges.svg",
    size=(500, 500),
    node_labels={0: "Human", 1: "Chimp", 2: "Gorilla", 3: "H/C", 4: "H/C/G"},
    x_axis=False,
    y_axis=True,
    style="".join(style),
)

# Add some sites and mutations
s0 = tables.sites.add_row(100.0, ancestral_state="A")
s1 = tables.sites.add_row(42.0, ancestral_state="T")
s2 = tables.sites.add_row(800.0, ancestral_state="T")

m0 = tables.mutations.add_row(s0, node=human, time=4, derived_state="G")
m1 = tables.mutations.add_row(s1, node=hc_ca, time=7.2, derived_state="C")
m2 = tables.mutations.add_row(s2, node=gorilla, time=11, derived_state="A")

# We copy b/c we want to modify again
# below to add multiple hits so we need a pre-sorted
# version for our sanity.
tcopy = tables.copy()
tables.sort()
treeseq = tables.tree_sequence()

mutation_labels = {
    i: f"{int(treeseq.site(treeseq.mutation(i).site).position)}: {treeseq.site(treeseq.mutation(i).site).ancestral_state} -> {treeseq.mutation(i).derived_state}"
    for i in range(treeseq.num_mutations)
}

treeseq.draw_svg(
    "figures/human_chimp_gorilla_with_mutations.svg",
    size=(500, 500),
    node_labels={0: "Human", 1: "Chimp", 2: "Gorilla", 3: "H/C", 4: "H/C/G"},
    mutation_labels=mutation_labels,
    x_axis=False,
    y_axis=True,
)

tables = tcopy
m3 = tables.mutations.add_row(s2, node=gorilla, time=1, derived_state="C")
m4 = tables.mutations.add_row(s1, node=chimp, time=0.5, derived_state="T")
tables.sort()
tables.build_index()
tables.compute_mutation_parents()
treeseq = tables.tree_sequence()
assert treeseq.num_mutations == 5
mutation_labels = {
    i: f"{int(treeseq.site(treeseq.mutation(i).site).position)}: {treeseq.site(treeseq.mutation(i).site).ancestral_state} -> {treeseq.mutation(i).derived_state}"
    for i in range(treeseq.num_mutations)
}

for k, v in mutation_labels.items():
    mutation_parent = treeseq.mutation(k).parent
    if mutation_parent != tskit.NULL:
        anc_state = treeseq.mutation(mutation_parent).derived_state
        mutation_labels[k] = (
            f"{int(treeseq.site(treeseq.mutation(k).site).position)}: {anc_state} -> {treeseq.mutation(k).derived_state}"
        )

treeseq.draw_svg(
    "figures/human_chimp_gorilla_with_multiple_hits.svg",
    size=(500, 500),
    node_labels={0: "Human", 1: "Chimp", 2: "Gorilla", 3: "H/C", 4: "H/C/G"},
    mutation_labels=mutation_labels,
    x_axis=False,
    y_axis=True,
)
