import tskit

tables = tskit.TableCollection(1000.0)
node_1 = tables.nodes.add_row(time=1.0)
node_2 = tables.nodes.add_row(time=1.0)
node_3 = tables.nodes.add_row(time=1.0)
node_5 = tables.nodes.add_row(time=0.0, flags=tskit.NODE_IS_SAMPLE)
node_6 = tables.nodes.add_row(time=0.0, flags=tskit.NODE_IS_SAMPLE)
node_7 = tables.nodes.add_row(time=0.0, flags=tskit.NODE_IS_SAMPLE)
node_8 = tables.nodes.add_row(time=0.0, flags=tskit.NODE_IS_SAMPLE)
tables.edges.add_row(parent=node_1, child=node_5, left=0, right=tables.sequence_length)
tables.edges.add_row(parent=node_2, child=node_7, left=0, right=tables.sequence_length)
tables.edges.add_row(parent=node_3, child=node_6, left=0, right=tables.sequence_length)
tables.edges.add_row(parent=node_3, child=node_8, left=0, right=tables.sequence_length)
tables.sort()
ts = tables.tree_sequence()
node_labels = {
    node_1: "1",
    node_2: "2",
    node_3: "3",
    node_5: "5 (1)",
    node_6: "6 (3)",
    node_7: "7 (2)",
    node_8: "8 (3)",
}
ts.draw_svg(
    path="figures/two_sibs_appendix.svg",
    size=(400, 400),
    x_axis=False,
    y_axis=True,
    node_labels=node_labels,
)
