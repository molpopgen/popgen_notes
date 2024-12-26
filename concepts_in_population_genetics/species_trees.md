(species_trees)=
# Species trees

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

## Evolutionary change on trees

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
## Multiple mutations at a site

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

## Summary

1. Trees are graphs that describe the relationship among the tip nodes.
2. In biology, the tips of trees represent things that we study -- extant species, individuals sampled from modern populations, etc..
   1. Tips need not be associated with the present time. We are now able to sequence DNA from preserved samples.  For example, we have genome sequences from extinct species like the wooly mammoth and the Neanderthal.
4. The ancestral (non-tip) nodes are the ancestors of the tips, meaning that they existed in the past.
5. Branch lengths usually indicate "how much evolution" has occurred on the branch. The examples in this section are in units of time.
6. We can trace changes on the trees from the past to the present.  These changes tell us the "state" of the tips. The examples here all trace changes in DNA sequence from the past to the present.

