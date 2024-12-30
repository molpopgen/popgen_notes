MDFILES:=$(shell find . -type f -name '*.md')
INDEX:=_build/html/index.html
PDF:=_build/latex/concepts_in_population_genetics.pdf

all: html pdf

html: $(INDEX)
pdf: $(PDF)

$(INDEX): $(MDFILES)
	PYTHONPATH=.. jupyter book build -W .
		
$(PDF): $(MDFILES)
	PYTHONPATH=.. jupyter book build -W --builder pdflatex  .

clean:
	rm -rf _build
