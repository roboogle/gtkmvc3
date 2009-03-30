# ---------------------------------------------------------
PDF_DEST = gtkmvc-tutorial.pdf
MAIN = tutorial
TOPDIR = ../../..
# ---------------------------------------------------------

pdf: ${PDF_DEST}

html: html_build

clean:
	rm -f ${BUILT} *~ 

distclean: clean
	rm -f ${TOP_TEX} ${PDF_DEST}
	rm -f html

# ---------------------------------------------------------
SED = sed
LATEX = pdflatex
VERSION = $(shell python ${TOPDIR}/setup.py --version)
BUILT = $(addprefix ${MAIN}, .log .toc .aux)
META_TOP_TEX = ${MAIN}.tex.in
TOP_TEX = $(basename ${META_TOP_TEX})
TEX = $(wildcard *.tex)
TEX += ${TOP_TEX}

${PDF_DEST} : ${MAIN}.pdf
	mv $< $@

${MAIN}.pdf : ${TOP_TEX} ${TEX}
	${LATEX} $<
	makeindex $<
	${LATEX} $<	
	${LATEX} $<	

${TOP_TEX}: ${META_TOP_TEX}
	${SED} 's/$$version/${VERSION}/g' $< > $@ 

html_struct: ${TOP_TEX} 
	mkdir -p ./html
	mkdir -p ./html/figs/png
	cp ${TEX} ./html/
	cp figs/png/*.png ./html/figs/png/
	cp pygtkmvc.cfg ./html/

html_build: html_struct
	cd html && htlatex pygtkmvc "pygtkmvc"
