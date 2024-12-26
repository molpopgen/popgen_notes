---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Gene trees and DNA data

This section emphasizes that our *data* are the outcome of a graphical process.
Namely, the long-term process of individuals reproducing within a pedigree structure gives rise to trees that connect present-day genomes.

The type of data that we typically deal with will be DNA sequence *genotypes*.
The following text output shows diploid genotypes for five individuals.
The genome position of each site labels the remaining columns and each genotype is written down as `allele 1/allele 2`.

```{code-cell} python
:tags: ["remove-input"]
import os
import msprime
import tskit
```

From this *variation table*, you can read off whether or not each individual is a heterozygote or a homozygote for each of the possible alleles.

The variation table shown here is the output of a computer simulation.
The simulation created the gene tree with mutations shown in {numref}`msprime_gene_tree_example_with_mutations`.
This gene tree looks similar to those seen earlier when we discussed pedigrees.
However, there are the following differences:

* The time scale is quite a bit longer!
  Compare the y axis in {numref}`msprime_gene_tree_example_with_mutations` to {numref}`simulated_pedigree_2_trees`.
* There is a single common ancestor of all of our sample nodes.
  The reason why there is a single ancestor node is because we have done something like
  simulate a pedigree forwards in time until all of our present day individuals are the descendants
  of some (long dead) ancestor.
  What we have actually done is more clever, and we've instead simulated *backwards* in time
  using approaches that we will describe later.

We can get from {numref}`msprime_gene_tree_example_with_mutations` to our variation table
using the logic described in {numref}`species_trees` to trace from ancestral to derived states along a tree.

```{attention} Test yourself!

You should be able to do the following:

* Reconstruct the variation table from the tree in {numref}`msprime_gene_tree_example_with_mutations`.
* Determine which DNA state is ancestral, and which is derived, for each column in the variation table.
* Build a variation table from scratch using the data in {numref}`msprime_gene_tree_example_with_mutations_2`.
```

Variation tables like those shown here leave a few things implicit/unsaid:

* The source of the data is unstated.
*  If this was DNA sequence data, how much DNA was sequnced?
*  If this was "SNP chip" data, what are the properties of the genotyping chips?

Further, for the gene trees:

* We only show the sites where mutations occurred.
* Therefore, you can assume that all other sites have the *ancestral state* for all sampled individuals/nodes.

```{code-cell} python
:tags: ["remove-input"]
ts = msprime.sim_ancestry(5, population_size=10000, sequence_length=100, random_seed=91234)
ts = msprime.sim_mutations(tree_sequence=ts, random_seed=123458, rate=5e-7)
tables = ts.tables
tables.compute_mutation_parents()
ts = tables.tree_sequence()
```

```{code-cell} python
:tags: ["remove-input"]
variant_dict = {}
individuals = [i.id + 1 for i in ts.individuals()]
for v in ts.variants():
    genotypes = []
    for i in ts.individuals():
        genotype =(v.alleles[v.genotypes[i.nodes[0]]], v.alleles[v.genotypes[i.nodes[1]]])
        genotypes.append(f"{genotype[0]}/{genotype[1]}")
    variant_dict[str(int(v.site.position))] = genotypes
variant_dict["individual"] = individuals
```

```{code-cell} python
:tags: ["remove-input"]
import polars as pl
df = pl.DataFrame(variant_dict)
print(df)
```

```{code-cell} python
:tags: ["remove-input"]
mutation_labels = {}
for m in ts.mutations():
    ancestral = ts.site(m.site).ancestral_state
    pos = ts.site(m.site).position
    mutation_labels[m.id] = f"{pos}: {ancestral} -> {m.derived_state}"
node_labels = {}
for i in ts.individuals():
    for n in i.nodes:
        node_labels[n] = f"{i.id + 1}: {int(n) + 1}"
ts.draw_svg("msprime_gene_tree_example_with_mutations.svg", size=(800, 600), y_axis=True, x_axis=False, y_ticks=[100, 1000, 10000, 40000], mutation_labels=mutation_labels, node_labels=node_labels);
```

```{figure} msprime_gene_tree_example_with_mutations.svg
:name: msprime_gene_tree_example_with_mutations

The gene tree that is the true evolutionary history of our variation table.
```

```{code-cell} python
:tags: ["remove-input"]
ts = msprime.sim_ancestry(3, population_size=10000, sequence_length=100, random_seed=815238)
ts = msprime.sim_mutations(tree_sequence=ts, random_seed=582158, rate=8e-7)
tables = ts.tables
tables.compute_mutation_parents()
ts = tables.tree_sequence()
mutation_labels = {}
for m in ts.mutations():
    ancestral = ts.site(m.site).ancestral_state
    pos = ts.site(m.site).position
    mutation_labels[m.id] = f"{pos}: {ancestral} -> {m.derived_state}"
node_labels = {}
for i in ts.individuals():
    for n in i.nodes:
        node_labels[n] = f"{i.id + 1}: {int(n) + 1}"
ts.draw_svg("msprime_gene_tree_example_with_mutations_2.svg", size=(800, 600), y_axis=True, x_axis=False, y_ticks=[100, 1000, 10000, 15000], mutation_labels=mutation_labels, node_labels=node_labels);
```

```{figure} msprime_gene_tree_example_with_mutations_2.svg
:name: msprime_gene_tree_example_with_mutations_2

Test yourself!
```
