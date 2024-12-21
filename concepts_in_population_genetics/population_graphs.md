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

# Population graphs

```{code-cell} python
:tags: ["remove-input"]
import demes
import demesdraw
import matplotlib.pyplot as plt

from myst_nb import glue
```

```{code-cell} python
:tags: ["remove-input", "remove-output"]
yaml = """
description: The Jouganous et al (2017) demographic model for YRI, CEU, and
  CHB. Parameters are given in Table 2.
time_units: years
generation_time: 29
doi:
  - https://doi.org/10.1534/genetics.117.200493
demes:
  - name: ancestral
    description: Equilibrium/root population
    epochs:
    - end_time: 312e3
      start_size: 11273
  - name: AMH
    description: Anatomically modern humans
    ancestors: [ancestral]
    epochs:
    - end_time: 125e3
      start_size: 23721
  - name: OOA
    description: Bottleneck out-of-Africa population
    ancestors: [AMH]
    epochs:
    - end_time: 42.3e3
      start_size: 3104
  - name: YRI
    description: Yoruba in Ibadan, Nigeria
    ancestors: [AMH]
    epochs:
    - start_size: 23721
      end_time: 0
  - name: CEU
    description: Utah Residents (CEPH) with Northern and Western European Ancestry
    ancestors: [OOA]
    epochs:
    - start_size: 2271
      end_size: 39611
      end_time: 0
  - name: CHB
    description: Han Chinese in Beijing, China
    ancestors: [OOA]
    epochs:
    - start_size: 924
      end_size: 83772
      end_time: 0
migrations:
  - demes: [YRI, OOA]
    rate: 15.8e-5
  - demes: [YRI, CEU]
    rate: 1.10e-5
  - demes: [YRI, CHB]
    rate: 0.48e-5
  - demes: [CEU, CHB]
    rate: 4.19e-5
"""
fig, ax = plt.subplots()
graph = demes.loads(yaml)
demesdraw.tubes(graph, ax=ax);
glue("jouganous-model", fig)
```

```{glue:figure} jouganous-model
:figwidth: 300px
:name: "jouganous-model-fig"

A graphical model of relationships between multiple human populations.
From bottom to top, time moves to the past.
Each population gets a different color and the width is proportional to the population size at a given time in the past.
Thick arrows represent founding events.
For example, the thick green arrow from `OOA` to `CEU` means that the latter population arose from the former.
The thinner arrows refer to continuous migration between populations. 
The color of the arrow tip refers to the *source* of migration and the arrow points at the *destination*.
The population labels are defined in {numref}`jouganous-model-labels`.
This image is plotted using parameters inferred from human genotype data by {cite:t}`Jouganous2017-tg`.
```

```{list-table} Population labels
:header-rows: 1
:name: jouganous-model-labels

* - AMH
  - Anatomically modern humans
* - OOA
  - Out of Africa population
* - YRI
  - Yoruba in Ibadan, Nigera
* - CEU
  - Utah Residents (CEPH) with Norther and Western European ancestry
* - CHB
  - Han Chinese in Beijing, China
```
