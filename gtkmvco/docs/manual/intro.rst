Introduction
************

This document contains information about the functionalities and the
architecture of a Model-View-Controller and Observer Infrastructure
(*MVC-O* from here on) for *PyGTK* version 2. The aim is to supply the
essential information in order to make developers able to effectively
use, modify and extend the infrastructure, for easily creating
new applications based on it.


Section :doc:`install` gives information about the required
dependencies, the installation, the distribution and the license of
*gtkmvc3*.

Section :doc:`motiv` tries to motivate the usage of *gtkmvc3*, by
discussing the context which the framework is thought to operate, and
its main goals.

Section :doc:`arch` briefly gives an overview of the general
architecture for a *GUI* application based on Python and the GTK
toolkit, showing all major parts, and how these depend on each other.
In this general picture, the proposed *MVC-O* framework is also
collocated, to provide an initial idea of how an hypothetical
application based on it should be organized.

Section :doc:`mvco` describes the basement of a *GUI* application, the
*MVC-O* Infrastructure.

Sections :doc:`impl` and :doc:`exam` supply some further details
about implementation, via many examples. The examples aim to make more
concrete the ideas described in all previous sections.

Section :doc:`adapt` presents a new important feature provided since
version 1.2.0, *Adapters* that make easier exploit the
framework when a default behaviour is expected. 

Finally, section :doc:`progen` briefly discusses how a project based on
*MVC-O* can be easily created from scratch by using a little application
that is provided with version 1.2 and later.
