# Evolutionary graphs

(species_trees)=
## Species trees

The following image shows the relationship of three species -- human, chimpanzee, and gorilla.
The y axis depicts time in the *past*, which is increasing from the bottom to the top of the image.
The time units are "millions of years ago", or `mya`.


```{figure} ../figures/human_chimp_gorilla.svg
:name: human_chimp_gorilla

A "species tree" showing the relationship between three species: human, chimpanzee, and gorilla.
```

The image contains the following elements:

1. *nodes*: a node is a vertex on the graph that represents an ancestor or a terminal "tip".
   On this tree, tips are shown as squares and branching points are circles.
   This graph has three terminal tips, which are our modern day species (human/chimp/gorilla).
   This graph has two ancestor nodes, which are associated with *branching points*, meaning that there is more than one line moving from the node towards the present time.
   On thise tree, these branching point nodes are the *common ancestors* of our species.
   The human/chimpanzee common ancestor is labelled `H/C` and the common ancestor of `H/C` and gorilla
   is labelled `H/C/G`.
2. *edges*: edges are the lines connecting the nodes.  In this image, the y axis represents time.
    Thus, the lengths of the edges are in units of *millions of years*.

A set of *nodes* connected by *edges* is a *graph*. A graph with no cycles (nodes connected by edges to form "loops") is a *tree*.

In most use cases in evolutionary biology, we call an *edge* a *branch* because we call the graph a tree!!

Further, because the graph is oriented with respect to *time in the past*, we can say things like the following:

1. The human/chimp common ancestor existed 6 million years ago.  We get this simply from looking at our image. (Although we'd usually get this information from some file that we use to plot the tree.)
2. The human/chimp/gorilla common ancestor existing 12 million years ago.
3. Human and chimps are more closely related to each other than either one is to the gorilla.  We make this statement because:
    1. The human/chimp common ancestor occurred in the more recent past than the common ancestor or human/gorilla (which is the same node as the chimp/gorilla common ancestor.)
    2. Therefore, there is more *time during which evolution (change) occurred* between human/gorilla (and also chimp/gorilla) than there is between human and chimp.

To illustrate this final point in more detail, let us show the same tree with each branch given a different color:


```{figure} ../figures/human_chimp_gorilla_colored_edges.svg
The same species tree as {numref}`human_chimp_gorilla` with the branches now colored.
```

We have the following branches and *branch lengths*:

| Ancestor (parent) | Descendant (child) | Color | Length (mya) |
|-----|-----|-----|-----|
|H/C/G|H/C|Pink|6|
|H/C/G|Gorilla|Purple|12|
|H/C|Human|Cyan|6|
|H/C|Chimp|Red|6|

We get the branch lengths directly from the tree.  For example, human exists now (0 mya) and the `H/C` node is 6mya ago. The branch length is therefore $6-0=6$.

Evolutionary change accumulates over time.
This accumulation is the result of mutations that mutations that affect organismal phenotypes.
In order to become species differences, the mutations have to "stick around" long enough to spread through entire species.

We can use our branch lengths to ask how much evolutionary time has occurred between our three "tip" species.
For example:

1. 6 million years separate human from the `H/C` node.
2. 6 million years separate chimp from the `H/C` node.
3. Therefore $6 + 6 = 12$ million years separate modern humans from contemporary chimpanzees.

This simple calculation illustrates a general principle:

The amount of evolution that has occurred between two species on a tree is a function of the **sum** of the branch lengths separating them.
We say "is a function of" because we also need to consider how quickly phenotypes or DNA sequences change per unit time.

### Evolutionary change on trees

Let us expand on our previous discussion, using DNA changes as a concrete example.
The following graphic shows our tree with three mutations added.
The notation for a mutation is: `Position: ancestral state -> derived state`.
In words, we read these labels as, "At Position X in the genome, the DNA sequence changed from `ancestral state` to `derived state`."

The ancestral state is usually the DNA state that was present in the node that is ancestral to (more ancient than) the mutation.
The positions of each mutation on a branch represent when they occurred in the past.
For example, at position 800, the `H/C/G` node has a `T`.
At about 11mya, this position changed from `T` to `A` on the branch leading from `H/C/G` to Gorilla.
The result is that most or all individuals that are modern gorillas will have an `A` at position 800.

We can write down the logic required to figure out how to determine the DNA sequence at a specific position for our tip nodes:

1. Identify the `derived` state of the change. (`A` at position 800.)
2. Identify the `branch` that the mutation occurs on. (The `H/C/G` to Gorilla branch for this mutation.)
3. Trace from the mutation down to each tree tip, making sure to follow all branching points along the way. This step is easy for position 800 -- there is only one branch all the way down to the Gorilla tip node.  The derived state is present in all of the tips.

Position 800 is not very interesting, but position 42 is!
Let's perform our steps:

1. The derived state of this mutation is `C`.
2. It occurs on the `H/C/G` to `H/C` branch.
3. Tracing down the tree to the present day, we find that the tips are Human and Chimp. Therefore, human and chimp *both* have a `C` at position 42 of the genome!

```{figure} ../figures/human_chimp_gorilla_with_mutations.svg
:name: human_chimp_gorilla_with_mutations
Adding mutations to our species tree.
```

(multiple_hits)=
### Multiple mutations at a site

Unfortunately, biology is quite messy.
Above, we noted that the ancestral state is "usually" the one found at the ancestor node.
We had to say "usually" because the same site in a genome can change multiple times.
This occurs when there is a lot of evolutionary time on a branch.
(In other words, when it is long.)
Mutations happen every generation, and over long time periods, the same site can be "hit" more than once by a mutation.

The following graphic illustrates such "multiple hits":

```{figure} ../figures/human_chimp_gorilla_with_multiple_hits.svg
:name: human_chimp_gorilla_with_multiple_hits

A species tree where multiple mutations have occurred at the same position during evolution.
```

We now have additional mutations that occurred at positions 42 and 800.
When mutations occur at the same position, the *ancestral* state is the *derived* state of the previous mutation at that position.  For example, at position 42, we have a mutation from `T` to `C` about 7 million years ago and then another from `C` to `T` about 0.5 million years ago on the branch leading to chimpanzees.  The result of this chain of events is that humans have a `C` at this position yet the chimp has a `T` because the second "hit" reverted the DNA sequence back to the original ancestral state (`T`).

Similarly, a second mutation at position 800 on the gorilla branch leads to a final state of `C` at position 800.

Multiple mutations at the same position mean that we need to update our logic.
As we trace a mutation at a site, we start with the most ancient mutation.
For each mutation we encounter, we record its derived state.
If we encounter another mutation at the same state, we replace the previous derived state with the value from the more recent mutation.
We have to take care to recognize when different branches can have different derived states at a given site.  Position 42 is an example of this phenomenon because the most recent mutation is more recent than the split of humans and chimpanzees.

### Summary

1. Trees are graphs that describe the relationship among the tip nodes.
2. In biology, the tips of trees represent things that we study -- extant species, individuals sampled from modern populations, etc..
   1. Tips need not be associated with the present time. We are now able to sequence DNA from preserved samples.  For example, we have genome sequences from extinct species like the wooly mammoth and the Neanderthal.
4. The ancestral (non-tip) nodes are the ancestors of the tips, meaning that they existed in the past.
5. Branch lengths usually indicate "how much evolution" has occurred on the branch. The examples in this section are in units of time.
6. We can trace changes on the trees from the past to the present.  These changes tell us the "state" of the tips. The examples here all trace changes in DNA sequence from the past to the present.

(pedigrees_gene_trees)=
## Pedigrees and "gene trees"

{numref}`trio` shows a simple pedigree called a "trio."
Trios consist of two parents with a single offspring.
This pedigree uses standard notation:
1. Males (individuals producing sperm) are shown as squares.
2. Females (individuals producing eggs) are shown as circles.

The individuals in the pedigree have numeric labels starting with 1 (one).
Individuals at the top of the pedigree are ancestors to those appearing nearer the bottom.

```{figure} ../figures/trio.png
:name: trio

A "trio" pedigree.
```

The edges that connect parents to children in a pedigree represent *meiosis*.
In other words, parental chromosomes were replicated (and mutated and recombined), and then a single new chromosome was passed down to an offspring.

If we consider the case of autosomal inheritance in diploid organisms like humans, then each individual contains two copies of the genome, one inherited via sperm and the other via egg.

The principles of Mendelian inheritance tell us that:

1. The two parents in {numref}`trio` each have two genomes. 
   Let's label the genomes of parent 1 as `1` and `2`.
   Let's label the genomes of parent 2 as `3` and `4`.
2. Ignoring some details of meiosis for now (mutation and recombination), individual 3
   will inherit genome `1` half the time and genome `2` half the time from parent `1`.
   Likewise, parent 1 will pass on either genome `3` or genome `4` with equal probability.

When discussing autosomal inheritance in diploids, we will adopt the following convention for `genome` labels:

* For an *individual* in the pedigree with label $i$, that individual's two genomes will be labelled $2i - 1$ and $2i$

For example, individual `7` in a pedigree will have genomes $2\times 7 - 1 = 13$ and $2\times 7 = 14$.
This convention will allow us to track both *genes* and *individuals*.

```{figure} ../figures/trio.svg
:name: trio_tree


An example of *genome* inheritance, given the pedigree structure in {numref}`trio`.
The node labels are `individual: genome`.
The values given for `genome` follow the convention described in the main text and individual
labels are identical to {numref}`trio`.
```

Figure {numref}`trio_tree` shows an example of "gene dropping" applied to the pedigree from {numref}`trio`.
Following our labelling convention described above, we see that the offspring individual (number 3) inherited its first genome (3) from genome 2 which was found in the parent individual labelled 1.
The other genome came from genome 3 in individual 2.

Figure {numref}`trio_tree` is a new type of graph that we may call a "gene tree".
The nodes in a gene tree usually refer to gene (or genome) sequences and their ancestors.
Figure {numref}`trio_tree` takes the extra step of tracking the specific *individual* to which each genome belongs or belonged.

Fundamentally, gene trees display:

1. Nodes, which refer to *genomes*. 
2. The height of the node in the tree indicate its *birth time*.
   In {numref}`trio_tree`, the `y` axis is in units of generations in the past.
   Thus, the genomes belonging to the parents exist (or existed) one generation ago.
   Each node gets a unique label.
3. Edges display the transmission of one genome to another.

{numref}`two_sibs` shows a pedigree with two siblings.
{numref}`two_sibs_gene_dropping` and {numref}`two_sibs_gene_dropping_2` show two examples of genome inheritance given this pedigree.
In {numref}`two_sibs_gene_dropping` , both offspring inherit the same two alleles while in {numref}`two_sibs_gene_dropping_2`, the two siblings inherit different alleles from each parent for both of their genomes.

```{attention} Take a moment to practice!
It is probably a good idea to make sure that you really understand what these images are showing.
Instead of skimming over the graphics, take some time to make sure that you understand how the `individual: genome` annotations in {numref}`two_sibs_gene_dropping` and {numref}`two_sibs_gene_dropping_2` map on to the pedigree in {numref}`two_sibs`.

See {numref}`gene_dropping_appendix` if you need more help on how these images work.
```

```{figure} ../figures/two_sibs.png
:name: two_sibs

A pedigree with two siblings.
```


```{figure} ../figures/two_sibs.svg
:name: two_sibs_gene_dropping

One example of "gene dropping" onto the pedigree from {numref}`two_sibs`.
```

```{figure} ../figures/two_sibs_2.svg
:name: two_sibs_gene_dropping_2

Another example of "gene dropping" onto the pedigree from {numref}`two_sibs`.
```

The pedigree shown in {numref}`multigen_pedigree` shows multiple generations of a family, ending with two sets of cousins.
Individuals 11 and 12 are first cousins (sharing grandparents) to individuals 13 and 14.

```{figure} ../figures/multigen_pedigree.png
:name: multigen_pedigree

A multigeneration pedigree.
```

Starting with these sets of cousins, we can imagine starting to trace their genomes back in time until we reach the grand-parental generation. For example, for each genome of the two genomes in individual 11, the genome came either from individual 7 or from 8. If it came from 7, then we know that it came from one of the two grandparents labelled 1 or 2.  But if it came from 8, then the grandparent of that genome was either 3 or 4. Therefore, in order for our cousins to have inherited a genome from the same common ancestor, the pathways of inheritance for those genomes must trace back to the grandparent couple 3 and 4. Further, the genomes must come from the same grandparent and then they must come from the *same genome* from that shared grandparent. If all of this happens, then we say that the two genomes have "coalesced" into their common ancestor.

{numref}`multigen_pedigree_tree` shows the result of "gene dropping" onto this pedigree.
We see that all four cousins share a genome descended from genome 5 of grandparent 3.

The tree in {numref}`multigen_pedigree_tree` shows several interesting features:

* Our pedigree ({numref}`multigen_pedigree`) contains six grandparents (two generations ago), yet only four of them (individuals 2, 3, 5, and 6) contributed alleles to the grandchildren.
* For those grandparents that did contribute to the genomes of their grandchildren, all of them only passed on one of their two possible alleles.
* Turning to the parental generation (1 generation ago), we see that all four parents contributed genes to the final generation, yet only individual 10 passed on a copy of each of their alleles.
* There are multiple occasions where a single allele was passed on to more than one offspring.
  For example, allele 5 was passed from individual 3 to individuals 8 and 9.
  When an allele is transmitted to multiple descendant nodes, we get a branching pattern in our tree.
  When an allele is transmitted to only a single descendant in the tree, we get straight lines, or "unary transmission" of the gene copy.
  An example of unary transmission starts with allele 11 in grandparent 6.
  It is passed to individual 10, becoming allele 20.
  It is then passed on to individual 14, becoming allele 28.
* There are 4 distinct trees shown in this image!


```{figure} ../figures/multigen_pedigree.svg
:name: multigen_pedigree_tree

Genome inheritance on the pedigree from {numref}`multigen_pedigree`.
```

We may also note that much of the information in {numref}`multigen_pedigree_tree` is not especially useful in understanding the ancestry of the alleles found in our present-day individuals (those born 0 generations ago).
There are many unary nodes, including unary nodes ancestral to nodes associated with branching events. 
{numref}`multigen_pedigree_tree_simplified` shows a "simplified" version of this image with unary transmission events removed and we stop at the most recent common ancestor of any set of nodes.
This simplified tree is the *minimal* graph that we require to describe the *ancestral history* of the alleles in our present-day individuals.
This simplified representation illustrates an important concept -- the important information in a gene tree is the *branching structure* that illustrates the relationship among our sample of alleles/genomes.
This branching relationship is completely analogous to what we discussed for species trees in {numref}`species_trees`.

```{figure} ../figures/multigen_pedigree_simplified.svg
:name: multigen_pedigree_tree_simplified

The tree(s) from {numref}`multigen_pedigree_tree` simplified to only show non-unary inheritance and to stop at the most recent common ancestor of each node.
```

{numref}`multigen_pedigree_tree` and {numref}`multigen_pedigree_tree_simplified` also reveal something that may be surprising.
These gene trees come from a small familial pedigree ({numref}`multigen_pedigree`).
However, we noted above that only 3/4 of the grandparents have directly contributed DNA to the most recent generation.
In other words, "direct" DNA connections to even recent ancestors are quickly lost.
This loss is due to the randomness of the "Mendelian lottery".
At an autosomal locus a given allele is only passed on to half of an individual's offspring.
Further, humans tend to have few offspring.
Few offspring implies few chances to pass on genes, meaning that there is a high likelihood that an individual does *not* pass both of their alleles on to the next generation.

(simulated_pedigrees_strict_monogamy)=
## Pedigrees in randomly mating populations

The pedigrees and gene trees discussed in {numref}`pedigrees_gene_trees` were the standard familial pedigrees that we are used to from medical genetics.

In this section, we look at pedigrees that are the *random* outcome of an evolutionary model.
We get the pedigrees by computer simulation.

In words the details of the model are:

* There are $N$ diploid founder individuals.
* For all but the final generation, exactly $N/2$ individuals are female and the remaining $N/2$ are male.
* $N$ does not change each generation.
* To generate the next generation:
    * Randomly pair each female with exactly one male, forming monogamous pairings.
    * Each pair has the same average fecundity (number of offspring).
    * We keep sampling pairs at random and recording births until we have made $N$ offspring.
    * We track the parents of each offspring each generation
* For the final generation, we randomly assign male/female status.

Using the simulated outputs, we can make the same kinds of plots that we discussed in {numref}`pedigrees_gene_trees`

### A small example

{numref}`simulated_pedigree_1` shows a pedigree with 4 founders and a total of 4 generations.
You will notice some individuals connected by two horizontal lines instead of the usual one.
Due to the small population size ($N$), close relatives may be paired as parents.
We say that offspring of such pairings are the product of "consanguineous" matings, which is just another way of saying inbreeding.
The two horizontal lines indicate parings that result in inbred offspring.

{numref}`simulated_pedigree_1_trees` and {numref}`simulated_pedigree_1_simplified_trees` show the unsimplified and simplified patterns of allele transmission, respectively.
These graphics should look very similar to those from {numref}`pedigrees_gene_trees`, showing rapid loss of both genealogical and genetic ancestors.

```{figure} ../figures/simulated_pedigree_1.png
:name: simulated_pedigree_1

A random pedigree starting with 4 founders and then evolving for 3 more generations of random mating.
The double horizontal lines indicate parents that are close relatives.
Their offspring are therefore inbred.
```


```{figure} ../figures/simulated_pedigree_1.svg
:name: simulated_pedigree_1_trees

An unsimplified gene tree from the pedigree in {numref}`simulated_pedigree_1`.
```


```{figure} ../figures/simulated_pedigree_1_simplified.svg
:name: simulated_pedigree_1_simplified_trees

The simplified version of the gene trees from {numref}`simulated_pedigree_1_trees`.
```

### A larger example

{numref}`simulated_pedigree_2` shows a pedigree with 6 founders and 10 generations of random mating.
The gene trees are in {numref}`simulated_pedigree_2_trees` and {numref}`simulated_pedigree_2_simplified_trees`.


```{figure} ../figures/simulated_pedigree_2.png
:name: simulated_pedigree_2

A random pedigree starting with 6 founders and then evolving for 9 more generations of random mating.
The double horizontal lines indicate parents that are close relatives.
The arcs connect an individual from where it occurs in a sibship (the set of offspring of a given pair of parents) to where that same individual is a parent.
The arcs are necessary due to the density of individuals in the pedigree.
```


```{figure} ../figures/simulated_pedigree_2.svg
:name: simulated_pedigree_2_trees

An unsimplified gene tree from the pedigree in {numref}`simulated_pedigree_2`.
```

As with the smaller example in the previous section, we see rapid loss of ancestry.
However, we should note that, of the 10 generations of random mating, we the common ancestors of individual alleles are obtained by at most 4 generations into the past ({numref}`simulated_pedigree_2_simplified_trees`).


```{figure} ../figures/simulated_pedigree_2_simplified.svg
:name: simulated_pedigree_2_simplified_trees

The simplified version of the gene trees from {numref}`simulated_pedigree_2_trees`.
```

## Pedigrees and population genetics

The previous sections on pedigrees and gene trees illustrate that there are two genealogical structures in natural populations.
First, there is the pedigree, which is a graph representing the relationships among *individuals*.
Second, there is a "gene tree" of the actual transmission of DNA across generations.

The field of population genetics is mostly concerned with the second structure (the gene tree).
While it is recognized that the structure of this gene tree depends on the structure of the true pedigree of the population, we rarely have detailed information about pedigrees.
What we can obtain rather easily is genetic information from contemporary individuals.
In some cases, we can also obtain genetic information from ancient individuals.
For example, it is relatively common now to sequence "ancient DNA" from human remains.
In some cases, the samples are over 1000 years old!
We also now have draft genome sequences of individuals from extinct hominid species such as the Neanderthal. Much of modern population genetics involves making inferences about the evolutionary history of one or more populations using such genomic data.

## Mutations on gene trees

This section will describe how to interpret gene trees with mutations.

The image at the top of {numref}`mutation_on_simulated_pedigree_2` is the gene tree from {numref}`simulated_pedigree_2_trees`.
We have added *mutations* to the tree, which are indicated in red.
The mutations are placed on the branch of the tree where they occurred and given arbitrary integer identifiers.
This panel shows us a lot of detail about the evolutionary history:

* This gene tree is not simplified.
* Therefore, we see that a mutation is placed in between two nodes on a branch that corresponds to a specific meiosis.
* For example, the mutation labelled 3 occurs on the branch between individuals 26 and 32.
* This mutation therefore occurred during meiosis in individual 26 and was first present in individual 32.

The second two rows of {numref}`mutation_on_simulated_pedigree_2` indicate the *subtrees* that correspond to two of the mutations.
To obtain the subtree, we first start at a mutation.
Then, we move towards the present day (the bottom of the trees image) and follow each branching point until we get to individuals born zero generations ago.
Along the way, we change the color of each branch from black to red.

Note that the two subtrees differ in size!
The subtree for mutation 2 leads to 5 alleles present in individuals born zero generations ago.
The subtree for mutation 3 leads to 9 alleles present in individuals born zero generations ago.
Further, these two subtrees lead to some of the same present-day alleles.
Let's combine these ideas:

* Present day alleles in a subtree carry a copy of the mutation[^this_is_only_true_under_infinite_sites].
* An allele carries a copy of each mutation for every subtree that it is in.
  For example, allele 110 found in individual 55 carries both mutations 2 and 3.

[^this_is_only_true_under_infinite_sites]: This statement is only true if all mutations occur at different *positions* in the genome.
If this is not the case, then we have to account for "multiple hits" to understand the final state of our present-day alleles.
See {numref}`multiple_hits` for a discussion of this in the context of species trees.
The fundamental idea is the same.

We can further note that:

* The number of *copies* of a mutation in the present day depends on the number of alleles that are tips of the subtree.
* The number of copies will roughly correspond to the *age* of the allele.
  Mutations that arose longer ago are deeper in the tree (farther back in the past) and will be ancestral to large subtrees.

```{attention} Test yourself!
Now is a good time to test yourself:

1. How many present-day geomes inherit mutation 0 in the top image of {numref}`mutation_on_simulated_pedigree_2`?
2. What about mutations 1, 4, and 5? (Consider them separately.)
3. The node labels in this image follow our `individual: genome` convention.
   Therefore, you should be able to figure out which individuals:
   * Are heterozygous for mutation 2
   * Are homozygous for mutation 2
   * Are heterozygous for mutation 3
   * Are homozygous for mutation 3

   As an added test, you can work out the two-locus genotypes considering mutations 2 and 3 together.
```

```{figure} ../figures/simulated_pedigree_2_mutations_combined.png
:name: mutation_on_simulated_pedigree_2

Mutations on gene trees.
The top image is the gene tree from {numref}`simulated_pedigree_2_trees`.
(That gene tree is based on simulating gene dropping on the pedigree shown in {numref}`simulated_pedigree_2`.)
The gene tree has had 6 mutations added.
The mutations are shown in red on the branches where they occur and are labelled with integers.
The middle image is the subtree that is defined by the descendants of mutation 2.
The bottom image is the subtree that is defined by the descendants of mutation 3.
```

{numref}`mutation_on_simulated_pedigree_2_simplified` shows the *simplified* version of the uppermost image of {numref}`mutation_on_simulated_pedigree_2`.
By removing unary nodes, etc., we lose the precise details about when each mutation originated.
In practice, we usually do not have access to genetic information from all individuals in a pedigree.
Therefore, this figure is a bit closer to our empirical reality.

```{figure} ../figures/simulated_pedigree_2_with_mutations_simplified.svg
:name: mutation_on_simulated_pedigree_2_simplified

Simplified representation of the top image from {numref}`mutation_on_simulated_pedigree_2`.
While unary transmissions have been removed, there are branches connecting most recent common ancestor nodes to mutations.
These branches are not edges because they do not end in a node!
Rather, they are a plotting device that connects *when* a mutation happened in the past to the *most ancient node* descending from the mutation event.
```

