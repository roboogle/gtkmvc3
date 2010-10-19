# Makefile for building all docs

DESTDIR = _build

PDF_SRC = manual/_build/latex/gtkmvc-userman.pdf \
          tutorial/_build/latex//gtkmvc-tutorial.pdf \
          quickstart/_build/latex/gtkmvc-quickstart.pdf \
          api/_build/latex/gtkmvc-reference.pdf
# ----------------------------------------------------------------------

HTML_DESTDIR = ${DESTDIR}/html
PDF_DESTDIR = ${DESTDIR}/pdf
PDF_DESTS = $(addprefix ${PDF_DESTDIR}/, $(notdir ${PDF_SRC}))

all: pdf html

pdf: ${PDF_DESTS}

html: htmldest

clean: 
	cd manual && ${MAKE} clean
	cd tutorial && ${MAKE} clean
	cd quickstart && ${MAKE} clean 
	cd api && ${MAKE} clean

distclean: clean
	rm -rf ${DESTDIR}

# --------------------------------------------------------------------
${PDF_SRC} : pdfbuild

pdfbuild:
	cd manual && ${MAKE} latex && cd _build/latex && ${MAKE} all-pdf
	cd tutorial && ${MAKE} latex && cd _build/latex && ${MAKE} all-pdf
	cd quickstart && ${MAKE} latex && cd _build/latex && ${MAKE} all-pdf
	cd api && ${MAKE} latex && cd _build/latex && ${MAKE} all-pdf

${PDF_DESTS} : ${PDF_SRC} ${PDF_DESTDIR}
	cp ${PDF_SRC} ${PDF_DESTDIR}/



${PDF_DESTDIR}:
	mkdir -p ${PDF_DESTDIR}

${HTML_DESTDIR}:
	mkdir -p ${HTML_DESTDIR}


htmlbuild: 
	cd manual && ${MAKE} html
	cd tutorial && ${MAKE} html
	cd quickstart && ${MAKE} html
	cd api && ${MAKE} html

htmldest: htmlbuild ${HTML_DESTDIR}
	rm -rf ${HTML_DESTDIR}/userman
	cp -r manual/_build/html ${HTML_DESTDIR}/userman
	rm -rf ${HTML_DESTDIR}/tutorial
	cp -r tutorial/_build/html ${HTML_DESTDIR}/tutorial
	rm -rf ${HTML_DESTDIR}/quickstart
	cp -r quickstart/_build/html ${HTML_DESTDIR}/quickstart
	rm -rf ${HTML_DESTDIR}/reference
	cp -r api/_build/html ${HTML_DESTDIR}/reference
