all: graph

graph: nge.tex
	pdflatex nge.tex
tex: nge.json
	python3 generate_tex.py
from-data: tex graph

clean:
	rm -rf nge.aux nge.log nge.pdf
