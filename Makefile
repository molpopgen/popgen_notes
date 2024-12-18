FINAL:=tree_thinking.pdf tree_thinking.html
FIGS:=figures/human_chimp_gorilla.svg \
      figures/human_chimp_gorilla_colored_edges.svg \
      figures/human_chimp_gorilla_with_mutations.svg \
      figures/human_chimp_gorilla_with_multiple_hits.svg \
	  figures/trio.png \
	  figures/trio.svg \
	  figures/two_sibs.png \
	  figures/two_sibs.svg \
	  figures/multigen_pedigree.png \
	  figures/multigen_pedigree.svg \
	  figures/multigen_pedigree_simplified.svg \
	  figures/simulated_pedigree_1.png \
	  figures/simulated_pedigree_1.svg \
	  figures/simulated_pedigree_1_simplified.svg \
	  figures/simulated_pedigree_2.png \
	  figures/simulated_pedigree_2.svg \
	  figures/simulated_pedigree_2_simplified.svg 
	
DATA:=figures/python/trio_tables.tables \
	  figures/python/trio.trees \
      figures/python/two_sibs_tables.tables \
	  figures/python/two_sibs.trees \
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

all: $(FINAL) $(FIGS) $(DATA)

tree_thinking.html: tree_thinking.ipynb $(FIGS) $(DATA)
	jupyter nbconvert --execute --no-input --to html tree_thinking.ipynb

tree_thinking.pdf: tree_thinking.ipynb $(FIGS) $(DATA)
	jupyter nbconvert --execute --no-input --to pdf tree_thinking.ipynb

figures/human_chimp_gorilla.svg: figures/python/human_chimp_gorilla.py
	python $<

figures/human_chimp_gorilla_colored_edges.svg: figures/python/human_chimp_gorilla.py
	python $<

figures/human_chimp_gorilla_with_mutations.svg: figures/python/human_chimp_gorilla.py
	python $<

figures/human_chimp_gorilla_with_multiple_hits.svg: figures/python/human_chimp_gorilla.py
	python $<

figures/trio.png: figures/R/plot_simple_pedigree.R figures/R/trio.txt
	Rscript --vanilla figures/R/plot_simple_pedigree.R figures/R/trio.txt $@

figures/trio.svg: pedigree_tools.py figures/python/trio.trees
	python pedigree_tools.py svg -i figures/python/trio.trees -o $@

figures/two_sibs.png: figures/R/plot_simple_pedigree.R figures/R/two_sibs.txt
	Rscript --vanilla figures/R/plot_simple_pedigree.R figures/R/two_sibs.txt $@

figures/two_sibs.svg: pedigree_tools.py figures/python/two_sibs.trees
	python pedigree_tools.py svg -i figures/python/two_sibs.trees -o $@

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

figures/simulated_pedigree_2_simplified.svg: pedigree_tools.py figures/simulated_pedigree_2.trees
	python pedigree_tools.py svg -i figures/simulated_pedigree_2.trees -o $@ --width 1000 --simplify

clean:
	rm -f $(FINAL) $(FIGS) $(DATA)
