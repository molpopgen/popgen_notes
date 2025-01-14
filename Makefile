# NOTE
# This Makefile uses ImageMagick commands that are deprecated in version 7.
# We do this intentionally because the GitHub action runner is using 
# Ubuntu 24.04 which runs version 6.
FINAL:=concepts_in_population_genetics/_build/latex/concepts_in_population_genetics.pdf \
       concepts_in_population_genetics/_build/html/index.html
FIGS:=figures/human_chimp_gorilla.svg \
      figures/human_chimp_gorilla_colored_edges.svg \
      figures/human_chimp_gorilla_with_mutations.svg \
      figures/human_chimp_gorilla_with_multiple_hits.svg \
	  figures/trio.png \
	  figures/trio.svg \
	  figures/two_sibs.png \
	  figures/two_sibs_markers.png \
	  figures/two_sibs_appendix.svg \
	  figures/two_sibs.svg \
	  figures/two_sibs_2.svg \
	  figures/multigen_pedigree.png \
	  figures/multigen_pedigree.svg \
	  figures/multigen_pedigree_simplified.svg \
	  figures/simulated_pedigree_1.png \
	  figures/simulated_pedigree_1.svg \
	  figures/simulated_pedigree_1_simplified.svg \
	  figures/simulated_pedigree_2.png \
	  figures/simulated_pedigree_2.svg \
	  figures/simulated_pedigree_2_mutations_combined.png \
	  figures/simulated_pedigree_2_simplified.svg 
	
DATA:=figures/python/trio_tables.tables \
	  figures/python/trio.trees \
      figures/python/two_sibs_tables.tables \
	  figures/python/two_sibs.trees \
	  figures/python/two_sibs.trees2 \
      figures/python/multigen_tables.tables \
      figures/python/multigen.trees \
	  figures/simulated_pedigree_1.records \
	  figures/simulated_pedigree_1.tables \
	  figures/simulated_pedigree_1.trees \
	  figures/R/simulated_pedigree_1.txt \
	  figures/simulated_pedigree_2.records \
	  figures/simulated_pedigree_2.tables \
	  figures/simulated_pedigree_2.trees \
	  figures/R/simulated_pedigree_2.txt

BOOKMDFILES:=$(shell find concepts_in_population_genetics/ -type f -name '*.md')

all: $(FINAL) $(FIGS) $(DATA)

concepts_in_population_genetics/_build/latex/concepts_in_population_genetics.pdf: $(FIGS) $(DATA) $(BOOKMDFILES)
	make -C concepts_in_population_genetics pdf

concepts_in_population_genetics/_build/html/index.html: $(FIGS) $(DATA) $(BOOKMDFILES)
	make -C concepts_in_population_genetics html

%.svg: popgen_notes_content/**.py
	python -m popgen_notes_content $(basename $(@F) .svg)

figures/human_chimp_gorilla.svg: popgen_notes_content/human_chimp_gorilla.py
figures/human_chimp_gorilla_colored_edges.svg: popgen_notes_content/human_chimp_gorilla.py
figures/human_chimp_gorilla_with_mutations.svg: popgen_notes_content/human_chimp_gorilla.py
figures/human_chimp_gorilla_with_multiple_hits.svg: popgen_notes_content/human_chimp_gorilla.py


figures/trio.png: figures/R/plot_simple_pedigree.R figures/R/trio.txt
	Rscript --vanilla figures/R/plot_simple_pedigree.R figures/R/trio.txt $@

figures/trio.svg: pedigree_tools.py figures/python/trio.trees
	python pedigree_tools.py svg -i figures/python/trio.trees -o $@

figures/two_sibs.png: figures/R/plot_simple_pedigree.R figures/R/two_sibs.txt
	Rscript --vanilla figures/R/plot_simple_pedigree.R figures/R/two_sibs.txt $@

figures/two_sibs_markers.png: figures/R/two_sibs_markers.R
	Rscript --vanilla $<

figures/two_sibs_appendix.svg: figures/python/two_sibs_appendix.py
	python $<

figures/two_sibs.svg: pedigree_tools.py figures/python/two_sibs.trees
	python pedigree_tools.py svg -i figures/python/two_sibs.trees -o $@

figures/two_sibs_2.svg: pedigree_tools.py figures/python/two_sibs.trees2
	python pedigree_tools.py svg -i figures/python/two_sibs.trees2 -o $@


figures/multigen_pedigree.png: figures/R/plot_simple_pedigree.R figures/R/multigen_pedigree.txt
	Rscript --vanilla figures/R/plot_simple_pedigree.R figures/R/multigen_pedigree.txt $@

figures/multigen_pedigree.svg: pedigree_tools.py figures/python/multigen.trees
	python pedigree_tools.py svg -i figures/python/multigen.trees -o $@

figures/multigen_pedigree_simplified.svg: pedigree_tools.py figures/python/multigen.trees
	python pedigree_tools.py svg -i figures/python/multigen.trees -o $@ --simplify

figures/python/trio_tables.tables: pedigree_tools.py figures/R/trio.txt
	python pedigree_tools.py dataframe-to-tables -i figures/R/trio.txt -o $@ -l 100

figures/python/trio.trees: pedigree_tools.py figures/python/trio_tables.tables
	python pedigree_tools.py treeseq -i figures/python/trio_tables.tables -o $@ -s 666

figures/python/two_sibs_tables.tables: pedigree_tools.py figures/R/two_sibs.txt
	python pedigree_tools.py dataframe-to-tables -i figures/R/two_sibs.txt -o $@ -l 100

figures/python/two_sibs.trees: pedigree_tools.py figures/python/two_sibs_tables.tables
	python pedigree_tools.py treeseq -i figures/python/two_sibs_tables.tables -o $@ -s 666

figures/python/two_sibs.trees2: pedigree_tools.py figures/python/two_sibs_tables.tables
	python pedigree_tools.py treeseq -i figures/python/two_sibs_tables.tables -o $@ -s 51251

figures/python/multigen_tables.tables: pedigree_tools.py figures/R/multigen_pedigree.txt
	python $< dataframe-to-tables -i figures/R/multigen_pedigree.txt -o $@ -l 100

figures/python/multigen.trees: pedigree_tools.py figures/python/multigen_tables.tables
	python pedigree_tools.py treeseq -i figures/python/multigen_tables.tables -o $@ -s 666

figures/simulated_pedigree_1.records: pedigree_tools.py
	python $< simulate -i 4 -g 4 -o $@ -s 666

figures/simulated_pedigree_1.tables: pedigree_tools.py figures/simulated_pedigree_1.records
	python pedigree_tools.py tables -i figures/simulated_pedigree_1.records -o $@ -l 10

figures/simulated_pedigree_1.trees: pedigree_tools.py figures/simulated_pedigree_1.tables
	python pedigree_tools.py treeseq -i figures/simulated_pedigree_1.tables -o $@ -r 0.0 -s 666

figures/R/simulated_pedigree_1.txt: pedigree_tools.py figures/simulated_pedigree_1.tables
	python pedigree_tools.py dataframe -i figures/simulated_pedigree_1.records -o $@

figures/simulated_pedigree_1.png: figures/R/plot_simple_pedigree.R figures/R/simulated_pedigree_1.txt
	Rscript --vanilla figures/R/plot_simple_pedigree.R figures/R/simulated_pedigree_1.txt $@

figures/simulated_pedigree_1.svg: pedigree_tools.py figures/simulated_pedigree_1.trees
	python pedigree_tools.py svg -i figures/simulated_pedigree_1.trees -o $@ --width 1000

figures/simulated_pedigree_1_simplified.svg: pedigree_tools.py figures/simulated_pedigree_1.trees
	python pedigree_tools.py svg -i figures/simulated_pedigree_1.trees -o $@ --width 1000 --simplify

figures/simulated_pedigree_2.records: pedigree_tools.py
	python $< simulate -i 6 -g 10 -o $@ -s 666

figures/simulated_pedigree_2.tables: pedigree_tools.py figures/simulated_pedigree_2.records
	python pedigree_tools.py tables -i figures/simulated_pedigree_2.records -o $@ -l 20

figures/simulated_pedigree_2.trees: pedigree_tools.py figures/simulated_pedigree_2.tables
	python pedigree_tools.py treeseq -i figures/simulated_pedigree_2.tables -o $@ -r 0.0 -s 666

figures/R/simulated_pedigree_2.txt: pedigree_tools.py figures/simulated_pedigree_2.tables
	python pedigree_tools.py dataframe -i figures/simulated_pedigree_2.records -o $@

figures/simulated_pedigree_2.png: figures/R/plot_simple_pedigree.R figures/R/simulated_pedigree_2.txt
	Rscript --vanilla figures/R/plot_simple_pedigree.R figures/R/simulated_pedigree_2.txt $@

figures/simulated_pedigree_2.svg: pedigree_tools.py figures/simulated_pedigree_2.trees
	python pedigree_tools.py svg -i figures/simulated_pedigree_2.trees -o $@ --width 1000

figures/simulated_pedigree_2_with_mutations.svg: figures/python/mutations_from_simulated_pedigree_2.py  figures/simulated_pedigree_2.trees
	python $< 

figures/simulated_pedigree_2_with_mutations_subtree0.svg: figures/python/mutations_from_simulated_pedigree_2.py figures/simulated_pedigree_2.trees
	python $<

figures/simulated_pedigree_2_with_mutations_subtree1.svg: figures/python/mutations_from_simulated_pedigree_2.py figures/simulated_pedigree_2.trees
	python $<

figures/simulated_pedigree_2_mutations_combined.png: figures/simulated_pedigree_2_with_mutations.svg  figures/simulated_pedigree_2_with_mutations_subtree0.svg figures/simulated_pedigree_2_with_mutations_subtree1.svg
	convert -append figures/simulated_pedigree_2_with_mutations.svg  figures/simulated_pedigree_2_with_mutations_subtree0.svg figures/simulated_pedigree_2_with_mutations_subtree1.svg $@

figures/simulated_pedigree_2_simplified.svg: pedigree_tools.py figures/simulated_pedigree_2.trees
	python pedigree_tools.py svg -i figures/simulated_pedigree_2.trees -o $@ --width 1000 --simplify

clean:
	rm -f $(FINAL) $(FIGS) $(DATA)
	rm -f figures/*.png figures/*.svg
	make clean -C concepts_in_population_genetics/
