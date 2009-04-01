# Makefile for building all docs

DESTDIR = build

PDF_SRC = user-man/gtkmvc-userman.pdf \
          tutorial/tex/gtkmvc-tutorial.pdf \
          quickstart/build/latex/gtkmvc-quickstart.pdf
# ----------------------------------------------------------------------

HTML_DESTDIR = ${DESTDIR}/html
PDF_DESTDIR = ${DESTDIR}/pdf
PDF_DESTS = $(addprefix ${PDF_DESTDIR}/, $(notdir ${PDF_SRC}))

all: pdf html

pdf: ${PDF_DESTS}

html: htmldest

clean: 
	cd user-man && ${MAKE} clean
	cd tutorial/tex && ${MAKE} clean
	cd quickstart && ${MAKE} clean 

distclean: 
	rm -rf ${DESTDIR}
	cd user-man && ${MAKE} distclean
	cd tutorial/tex && ${MAKE} distclean
	cd quickstart && ${MAKE} clean

# --------------------------------------------------------------------
${PDF_SRC} : pdfbuild

pdfbuild:
	cd user-man && ${MAKE} pdf
	cd tutorial/tex && ${MAKE} pdf
	cd quickstart && ${MAKE} latex && cd build/latex && \
	   ${MAKE} all-pdf && mv quickstart.pdf gtkmvc-quickstart.pdf

${PDF_DESTS} : ${PDF_SRC} ${PDF_DESTDIR}
	cp ${PDF_SRC} ${PDF_DESTDIR}/



${PDF_DESTDIR}:
	mkdir -p ${PDF_DESTDIR}

${HTML_DESTDIR}:
	mkdir -p ${HTML_DESTDIR}


htmlbuild: 
	cd user-man && ${MAKE} html
	cd tutorial/tex && ${MAKE} html
	cd quickstart && ${MAKE} html

htmldest: htmlbuild ${HTML_DESTDIR}
	rm -rf ${HTML_DESTDIR}/userman
	cp -r user-man/html ${HTML_DESTDIR}/userman
	rm -rf ${HTML_DESTDIR}/tutorial
	cp -r tutorial/tex/html ${HTML_DESTDIR}/tutorial
	rm -rf ${HTML_DESTDIR}/quickstart
	cp -r quickstart/build/html ${HTML_DESTDIR}/quickstart
