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
```

```{code-cell} python
---
mystnb:
  image:
    classes: shadow bg-primary
  figure:
    caption: |
      A single deme with constant population size
      continuing "infinitely" into the past.
    name: single_deme_constant_size
  tags: 
    remove-input
---
single_deme = """
time_units: generations
demes:
 - name: a_deme
   epochs:
    - start_size: 1000
"""
graph = demes.loads(single_deme)
demesdraw.tubes(graph);
```

```{code-cell} python
---
mystnb:
  image:
    classes: shadow bg-primary
  figure:
    caption: |
      A single deme with recent exponential growth
      starting 100 generations ago.
    name: single_deme_growth
---
single_deme = """
time_units: generations
demes:
 - name: a_deme_with_size_changes
   epochs:
    - start_size: 1000
      end_time: 100
    - end_size: 5000
"""
graph = demes.loads(single_deme)
demesdraw.tubes(graph);
```

```{figure} demesdraw.tubes(graph)```
