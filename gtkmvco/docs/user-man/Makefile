# ---------------------------------------------------------
PDF_DEST = gtkmvc-userman.pdf
MAIN = pygtkmvc
TOPDIR = ../..
# ---------------------------------------------------------

pdf: ${PDF_DEST}

clean:
	rm -f ${BUILT} *~ 

distclean: clean
	rm -f ${TOP_TEX} ${PDF_DEST}

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

