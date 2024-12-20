import msprime
import tskit

ts = tskit.load("figures/simulated_pedigree_2.trees")

ts = msprime.sim_mutations(ts, rate=1e-2, random_seed=12454)

# make the node labels as per our standards
# for the book...
node_labels = {}
for n in ts.nodes():
    node_labels[n.id] = f"{n.individual + 1}: {n.id + 1}"
node_label_style = ".node > .lab {font-size: 80%}"
ts.draw_svg(
    "figures/simulated_pedigree_2_with_mutations.svg",
    size=(1000, 400),
    node_labels=node_labels,
    x_axis=False,
    y_axis=True,
    style=node_label_style,
)

num_samples_below_mutation = {}
for tree in ts.trees():
    for m in tree.mutations():
        num_samples_below_mutation[m.id] = tree.num_samples(m.node)

subtree = 0
for m in ts.mutations():
    if num_samples_below_mutation[m.id] > 1:
        mut_style = (
            f".m{m.id} .node .edge, "  # the descendant edges
            f".mut.m{m.id} line, "  # activate the hidden line between the mutation and the node
            f".mut.m{m.id} .sym "  # the mutation symbols on the tree and the axis
            "{stroke: red; stroke-width: 2px}"
            f".mut.m{m.id} .lab"
            "{fill: red}"  # colour the label in red too
        )
        ts.draw_svg(
            path=f"figures/simulated_pedigree_2_with_mutations_subtree{subtree}.svg",
            size=(1000, 400),
            node_labels=node_labels,
            x_axis=False,
            y_axis=True,
            style=node_label_style + mut_style,
        )
        subtree += 1

tables = ts.tables
idmap = tables.simplify(filter_individuals=False, filter_nodes=False)
ts = tables.tree_sequence()

ts.draw_svg(
    "figures/simulated_pedigree_2_with_mutations_simplified.svg",
    size=(1000, 400),
    node_labels=node_labels,
    x_axis=False,
    y_axis=True,
    style=node_label_style,
)

subtree = 0
for m in ts.mutations():
    if num_samples_below_mutation[m.id] > 1:
        mut_style = (
            f".m{m.id} .node .edge, "  # the descendant edges
            f".mut.m{m.id} line, "  # activate the hidden line between the mutation and the node
            f".mut.m{m.id} .sym "  # the mutation symbols on the tree and the axis
            "{stroke: red; stroke-width: 2px}"
            f".mut.m{m.id} .lab"
            "{fill: red}"  # colour the label in red too
        )
        ts.draw_svg(
            path=f"figures/simulated_pedigree_2_with_mutations_simplified_subtree{subtree}.svg",
            size=(1000, 400),
            node_labels=node_labels,
            x_axis=False,
            y_axis=True,
            style=node_label_style + mut_style,
        )
        subtree += 1
