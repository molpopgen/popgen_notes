FINAL:=tree_thinking.pdf tree_thinking.html
FIGS:=figures/human_chimp_gorilla.svg \
      figures/human_chimp_gorilla_colored_edges.svg \
      figures/human_chimp_gorilla_with_mutations.svg \
      figures/human_chimp_gorilla_with_multiple_hits.svg \
	  figures/trio.png

all: $(FINAL) $(FIGS)

tree_thinking.html: tree_thinking.ipynb $(FIGS)
	jupyter nbconvert --execute --no-input --to html tree_thinking.ipynb

tree_thinking.pdf: tree_thinking.ipynb $(FIGS)
	jupyter nbconvert --execute --no-input --to pdf tree_thinking.ipynb

figures/human_chimp_gorilla.svg: figures/python/human_chimp_gorilla.py
	python $<

figures/human_chimp_gorilla_colored_edges.svg: figures/python/human_chimp_gorilla.py
	python $<

figures/human_chimp_gorilla_with_mutations.svg: figures/python/human_chimp_gorilla.py
	python $<

figures/human_chimp_gorilla_with_multiple_hits.svg: figures/python/human_chimp_gorilla.py
	python $<

figures/trio.png: figures/R/trio.R
	R --no-save --quiet < $<

clean:
	rm -f $(FINAL) $(FIGS)
