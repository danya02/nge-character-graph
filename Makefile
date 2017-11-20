all: graph

graph: nge.tex
	pdflatex nge.tex

clean:
	rm -rf nge.aux nge.log nge.pdf