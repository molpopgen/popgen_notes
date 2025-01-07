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

# The allele frequency spectrum

```{code-cell} python
:tags: ["remove-input"]
from collections import defaultdict
import matplotlib.pyplot as plt
import msprime
import tskit
from myst_nb import glue
from popgen_notes_content.patch_df_repr import patch_repr
```

```{code-cell} python
:tags: ["remove-input"]
ts = msprime.sim_ancestry(5, population_size=10000, sequence_length=1000, random_seed=19234)
ts = msprime.sim_mutations(tree_sequence=ts, random_seed=213458, rate=1.8e-7)
tables = ts.tables
tables.compute_mutation_parents()
ts = tables.tree_sequence()
```

```{code-cell} python
:tags: ["remove-input"]
variant_dict = {}
variant_dict_ms_style = {}
variant_dict_minor_allele_encoded_as_1 = {}
individuals = [i.id + 1 for i in ts.individuals()]
for v in ts.variants():
    assert len(v.alleles) == 2
    genotypes = []
    genotypes_ms_style = []
    genotypes_minor_is_1 = []

    ancestral = [False, False]
    for i,g in enumerate(v.alleles):
        if g == v.site.ancestral_state:
            ancestral[i] = True
    assert ancestral.count(True) == 1, f"{ancestral}, {g}, {v.alleles}, {v.site}"

    derived_allele_count = v.genotypes.tolist().count(1)
    derived_is_minor = derived_allele_count < len(v.genotypes)/2

    for i in ts.individuals():
        genotype =(v.alleles[v.genotypes[i.nodes[0]]], v.alleles[v.genotypes[i.nodes[1]]])
        genotypes.append(f"{genotype[0]}/{genotype[1]}")
        # The code below is wrong
        first = 1
        second = 1
        if ancestral[v.genotypes[i.nodes[0]]] is True:
            first = 0
        if ancestral[v.genotypes[i.nodes[1]]] is True:
            second = 0
        genotype_ms_style = f"{first}/{second}"
        genotypes_ms_style.append(genotype_ms_style)
        maf_based_encoding = [None, None]
        for a, anc in enumerate(ancestral):
            if anc is True:
                if derived_is_minor:
                    maf_based_encoding[a] = 0
                else:
                    maf_based_encoding[a] = 1
            else:
                if derived_is_minor:
                    maf_based_encoding[a] = 1
                else:
                    maf_based_encoding[a] = 0
        first = maf_based_encoding[v.genotypes[i.nodes[0]]]
        second = maf_based_encoding[v.genotypes[i.nodes[1]]]
        genotype_maf = f"{first}/{second}"
        genotypes_minor_is_1.append(genotype_maf)

    variant_dict[str(int(v.site.position))] = genotypes
    variant_dict_ms_style[str(int(v.site.position))] = genotypes_ms_style
    variant_dict_minor_allele_encoded_as_1[str(int(v.site.position))] = genotypes_minor_is_1
variant_dict["individual"] = individuals
variant_dict_ms_style["individual"] = individuals
variant_dict_minor_allele_encoded_as_1["individual"] = individuals

anc_state_per_site = {}
for i in ts.sites():
    anc_state_per_site[str(int(i.position))] = i.ancestral_state
```

```{code-cell} python
:tags: ["remove-input", "remove-output"]
import polars as pl
df = pl.DataFrame(variant_dict)
df = patch_repr(df)
glue("genotype-table", df);
```

```{code-cell} python
:tags: ["remove-input", "remove-output"]
df = patch_repr(pl.DataFrame(anc_state_per_site))
glue("anc_state_per_site", df);
```

```{code-cell} python
:tags: ["remove-input", "remove-output"]
df_ms = patch_repr(pl.DataFrame(variant_dict_ms_style))
glue("genotype-table-ms", df_ms);
```

```{code-cell} python
:tags: ["remove-input", "remove-output"]
df_maf = patch_repr(pl.DataFrame(variant_dict_minor_allele_encoded_as_1))
glue("genotype-table-maf", df_maf);
```

Consider the following autosomal genotype table for five diploid individuals:

```{glue:} genotype-table
```

The numbers refer to positions in the genome where there is variation in DNA sequence.

## Common data encodings

(ancestral_vs_derived_alleles)=
### Ancestral vs derived alleles

If we know that the *ancestral state* at each position is:

```{glue:} anc_state_per_site
```

Then, we can rewrite our variation table using `0` to represent the *ancestral* state and `1` for the *derived* state:

```{glue:} genotype-table-ms
```

(minor_vs_major_alleles)=
### Minor vs major alleles

For positions with two alleles, one is more common and the other more rare.
We call the rarer allele the *minor* allele.
The following table encodes our data such that `1` is the minor allele and `0` is the more common, or "major" allele:

```{glue:} genotype-table-maf
```

## Tabulating allele counts (and frequencies)

### Derived alleles

At each *position*, we obtain the *number of occurrences* of the derived allele by simply counting the number of times the value `1` appears in each column from the table shown in {numref}`ancestral_vs_derived_alleles`:

```{code-cell} python
:tags: ["remove-input"]
daf = {}
for key, value in variant_dict_ms_style.items():
    if key != "individual":
        temp = sum([i.count("1") for i in value])
        daf[key] = temp
df_ms_daf = patch_repr(pl.DataFrame(daf))
df_ms_daf
```

### Minor alleles

We can do the same exercise with respect to the *minor* allele by using the table from {numref}`minor_vs_major_alleles`:

```{code-cell} python
:tags: ["remove-input"]
maf = {}
for key, value in variant_dict_minor_allele_encoded_as_1.items():
    if key != "individual":
        temp = sum([i.count("1") for i in value])
        maf[key] = temp
df_maf = patch_repr(pl.DataFrame(maf))
df_maf
```

### From *counts* to *frequencies*

The previous two sections give us *counts* of how many times a derived or minor allele occurs in the sample.
To get the *frequency* of the allele, simply divide by the number of *genomes* in the sample.
For the examples here, variant tables refer to autosomal diploid genotypes.
Therefore, the number of genomes sampled is twice the number of individuals in the tables.


### Tabulating allele counts (and frequencies) into the "allele frequency spectrum"

The tables in the preceding section show us how many times the derived (or minor) allele appears at each position.

In this section we ask, "how many positions are there with a derived/minor allele at frequency $x$?".
In other words, how many positions are there with the derived mutation at frequency 1, 2, etc.?

(tabulating_derived_allele_counts)=
### Derived alleles

From the count table above, we can tabulate:

```{code-cell} python
:tags: ["remove-input"]
dafs = defaultdict(int)
for v in sorted(daf.values()):
    dafs[str(v)] += 1

dafs_df = patch_repr(pl.DataFrame(dafs))
dafs_df
```

This table tells is that there are four positions in our data where the derived allele is present in a single sample.
There is one position where the derived allele appears in 8 samples.
There is one position where the derived allele appears in 9 samples.

This table called the *allele frequency spectrum*.
We usually present it graphically ({numref}`fs_example`).

```{code-cell} python
:tags: ["remove-input", "remove-output"]
n = 2*ts.num_individuals
assert n == 10
fs = [0]*(n-1)
for k,v in dafs.items():
    fs[int(k)-1] = v

fig, ax = plt.subplots(1, 1, figsize=(8, 4))
ax.plot([i for i in range(1,n)], fs, ".-", ms=8, lw=1)
ax.set_xlabel("Number of copies of derived allele ($x$)")
ax.set_ylabel("Number of positions with $x$ copies")
ax.set_xticks([i+1 for i in range(n)])
ax.set_xlim((0, n))
ax.legend();
glue("fs_example", fig, display=False)
```

```{glue:figure} fs_example
:name: fs_example

An example of the "allele frequency spectrum" for data where the *derived* allele is known.
The x axis is the *count*, or *number of occurrences* in the sample of the derived allele at a given position in the genome.
The y axis is the number of genomic positions that have the same x axis value.
```

### Minor alleles

{numref}`minor_fs_example` shows the allele frequency spectrum for the same data with respect to the *minor* allele count.

```{code-cell} python
:tags: ["remove-input", "remove-output"]
mafs = defaultdict(int)
for v in sorted(maf.values()):
    mafs[str(v)] += 1

mafs_df = patch_repr(pl.DataFrame(mafs))
n = 2*ts.num_individuals
assert n == 10
fs = [0]*(n//2)
assert len(fs) == 5, f"{fs}, {len(fs)}"
for k,v in mafs.items():
    print(k,v)
    assert int(k) < len(fs), f"{k}, {len(fs)}"
    fs[int(k)-1] = v

fig, ax = plt.subplots(1, 1, figsize=(8, 4))
ax.plot([i for i in range(1,n//2 + 1)], fs, ".-", ms=8, lw=1)
ax.set_xlabel("Number of copies of minor allele ($x$)")
ax.set_ylabel("Number of positions with $x$ copies")
ax.set_xticks([i+1 for i in range(n//2 + 1)])
ax.set_xlim((0, n//2 + 1))
ax.legend();
glue("minor_fs_example", fig, display=False)
```

```{glue:figure} minor_fs_example
:name: minor_fs_example

An example of the "allele frequency spectrum" of the *minor* allele.
The x axis is the *count*, or *number of occurrences* in the sample of the minor allele at a given position in the genome.
The y axis is the number of genomic positions that have the same x axis value.
```

```{attention} Test yourself!

1. Make the table representation that corresponds to {numref}`minor_fs_example`.
   (For inspiration, see the table shown for derived allele counts in {numref}`tabulating_derived_allele_counts`.)
```

## Why the "allele frequency spectrum" is useful

1. Different evolutionary scenarios make different predictions about the shape of the frequency spectrum.
2. We can compare our observed spectrum to what theory predicts about a given model to ask if our data seem plausible under that model.
3. And/or we can *fit* (infer) the parameters of the model using our observed frequency spectrum.
   {numref}`jouganous-model-fig` is an example of fitting parameters to a demography model from frequency spectrum data.
   The frequency spectrum in that figure is a bit more complex, keeping track of mutation counts in all of the modern day sample populations.

## Notes, gotchas, etc., about the "allele frequency spectrum"

1. The nomenclature is poor.
   We call it a "frequency" spectrum but we are plotting *counts*.
2. This way to summarize the data has a few synonyms.
   "Site frequency spectrum" is probably the most common.
3. For the *derived* frequency spectrum, the range of the x axis is from 1 to $n-1$, where $n$ is the total number of *genomes* in the sample.
4. For the *minor allele* frequency spectrum, the range of the x axis is from 1 to $n/2$, where $n$ is the total number of *genomes* in the sample.
5. If the variation table from which a frequency is obtained is from biased data, then the plot may not look like what one predicts from first principles.
   For example, much of our theory assumes that we completely sequence a set of unrelated genomes.
   However, if we genotype a set of unrelated genomes at a set of positions that we already know are variable in the population, then the frequency spectrum shape will be affected!!
   Therefore the *provenance* of the data is critical to interpreting the plots.
